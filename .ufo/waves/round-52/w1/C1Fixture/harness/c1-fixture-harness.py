#!/usr/bin/env python3
"""c1-fixture-harness.py — counter-agnostic red/green fixture harness for round-52 C1.

Seat: C1Fixture (mado round 52, w1).  Scope: the *harness* only.  It does not implement
the C1 predicate and it does not implement a counter.  It measures a candidate counter
against two fixtures and reports whether that counter exhibits the discrimination the
frozen claim requires.

    green  = the production ledger `quality/tool-ledger.md` at the frozen base revision
              -> the counter must exit 0 and print verdict=TARGET_MET
    red    = the frozen do-nothing control `.ufo/waves/round-52/controls/c1-do-nothing.md`
              committed in place of the production ledger
              -> the counter must exit 1, print verdict=TARGET_MISSED, and fail *for the
                 self-pointer / instrument-specific-context reason* (not merely because
                 the ledger is absent)

The counter is never imported and its source is never read: the harness passes
`--repo <fixture> --rev <fixture-rev> --work <case-work>` and reads stdout, stderr and
the exit status only.  Summary-line field names are matched through an alias set in the
profile JSON, so a counter author is free to spell a field `self_pointer=` or `selfptr=`.

Everything the harness writes lives under `--work` (a scratch directory) and, for the
evidence copies, under `--out`.  The lane repository is read-only for this harness: it is
cloned into the scratch tree, and a git-native integrity comparison of the lane working
tree is taken before and after the cases to prove no source-tree write happened.

Usage:
  python3 -I c1-fixture-harness.py \
      --repo <lane> --rev <rev> --counter <absolute path to counter .py> \
      --control <absolute path to control .md> --profile <profile.json> \
      --work <scratch dir> --out <evidence dir> [--cases green,red] \
      [--overlay <repo-relative path>[,<repo-relative path>]] \
      [--expect-final <file with "case<TAB>exact final line">]

Exit codes: 0 = every case matched its expectation, 1 = a case mismatched,
2 = setup error (bad arguments, clone/commit failure, unreadable inputs).
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DEFAULT_REV = "85d57a818c3707397e21c840b6498b105ba798aa"
DEFAULT_CONTROL = os.path.join(DEFAULT_REPO, ".ufo/waves/round-52/controls/c1-do-nothing.md")
LEDGER_REL = "quality/tool-ledger.md"
# Sibling seats legitimately write inside the round's own wave directory while this
# harness runs; those untracked paths are excluded from the integrity comparison so a
# concurrent seat cannot be mistaken for a harness write.
INTEGRITY_EXCLUDE_PREFIX = (".ufo/waves/round-52/",)
GIT_ENV = ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME",
           "GIT_COMMITTER_EMAIL", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")
COMMIT_SAFE = ["-c", "user.name=C1Fixture", "-c", "user.email=c1fixture@invalid",
               "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
RUN_TIMEOUT = 900


class SetupError(Exception):
    pass


# --------------------------------------------------------------------- git ----

def git_env():
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV}
    env["LC_ALL"] = "C.UTF-8"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def git(args, cwd, check=True):
    proc = subprocess.run(("git",) + tuple(args), cwd=cwd, capture_output=True,
                          env=git_env())
    if check and proc.returncode != 0:
        raise SetupError("git %s failed in %s: %s" % (
            " ".join(args), cwd, proc.stderr.decode("utf-8", "replace").strip()[:400]))
    return proc


def git_out(args, cwd):
    return git(args, cwd).stdout.decode("utf-8", "replace").strip()


# -------------------------------------------------- lane integrity snapshot --

def lane_integrity(repo, own_paths=()):
    """A git-native snapshot of the lane working tree.

    Views, hashed or counted separately:
      * the index's recorded blob ids for every tracked path (content identity),
      * the set of paths whose worktree content differs from the index,
      * the set of staged differences against HEAD,
      * the set of untracked paths outside the round's wave directory.

    Any write into the source tree — added, removed, modified or staged file — moves
    the hash.  This is the evidence for `lane_unchanged`.

    The round's wave directory (`.ufo/waves/round-52/`) is excluded from the strict
    views because sibling seats write there concurrently while this harness runs; a
    write there would otherwise be misreported as a harness write.  Its untracked path
    count is reported separately as `wave_untracked_count`, minus this seat's own
    paths, so the exclusion is visible rather than silent.
    """
    parts = {}
    index = git_out(["ls-files", "-s", "-z"], repo)
    parts["index"] = hashlib.sha256(index.encode("utf-8", "surrogateescape")).hexdigest()
    unstaged = git_out(["diff", "--name-only", "-z"], repo)
    parts["unstaged"] = hashlib.sha256(unstaged.encode("utf-8", "surrogateescape")).hexdigest()
    staged = git_out(["diff", "--cached", "--name-only", "-z"], repo)
    parts["staged"] = hashlib.sha256(staged.encode("utf-8", "surrogateescape")).hexdigest()
    all_untracked = [p for p in
                     git_out(["ls-files", "-z", "--others", "--exclude-standard"], repo).split("\0")
                     if p]
    untracked = [p for p in all_untracked if not p.startswith(INTEGRITY_EXCLUDE_PREFIX)]
    parts["untracked"] = hashlib.sha256(
        "\0".join(sorted(untracked)).encode("utf-8", "surrogateescape")).hexdigest()
    parts["untracked_count"] = len(untracked)
    parts["unstaged_count"] = len([p for p in unstaged.split("\0") if p])
    parts["staged_count"] = len([p for p in staged.split("\0") if p])
    wave = [p for p in all_untracked if p.startswith(INTEGRITY_EXCLUDE_PREFIX)
            and not any(p == own or p.startswith(own.rstrip("/") + "/") for own in own_paths)]
    parts["wave_untracked_count"] = len(wave)
    return parts


# The views that must be byte-identical before and after the run.  The counts are
# informational: sibling seats and this seat's own receipts change them legitimately.
STRICT_INTEGRITY_KEYS = ("index", "unstaged", "staged", "untracked")


def lane_unchanged(before, after):
    return all(before.get(key) == after.get(key) for key in STRICT_INTEGRITY_KEYS)


# -------------------------------------------------------- fixture building ----

def clone_at(repo, rev, dest):
    """A shared, no-checkout clone of the lane at REV inside the scratch tree.

    `--shared` borrows the lane's object store instead of copying it, so the fixture is
    cheap.  `--no-checkout` plus a symbolic HEAD keeps the fixture working tree empty:
    the counter reads the revision's bytes from the object store (`git show <rev>:<path>`
    or its own clone of this fixture), so materialising 24k working-tree files would buy
    nothing and cost minutes.
    """
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    git(["clone", "-q", "--shared", "--no-checkout", repo, dest], cwd=os.path.dirname(dest))
    git(["update-ref", "refs/heads/fixture", rev], cwd=dest)
    git(["symbolic-ref", "HEAD", "refs/heads/fixture"], cwd=dest)
    head = git_out(["rev-parse", "HEAD"], dest)
    if head != rev:
        raise SetupError("fixture clone HEAD %s != %s" % (head, rev))
    assert_toplevel(dest, dest)
    return dest


def assert_toplevel(path, expected):
    """Guard: a git mutation may only run inside the fixture it belongs to."""
    top = os.path.realpath(git_out(["rev-parse", "--show-toplevel"], path))
    if top != os.path.realpath(expected):
        raise SetupError("toplevel %s != fixture %s" % (top, expected))


def commit_tree_with(paths):
    """Commit `paths` (repo-relative -> bytes) onto HEAD of the fixture.

    The fixture working tree is not materialised; the commit is built with plumbing
    (`hash-object`, `update-index`, `write-tree`, `commit-tree`), so a fixture commit
    never depends on the lane's working tree bytes.
    """
    assert_toplevel(CWD[0], CWD[0])
    git(["read-tree", "HEAD"], cwd=CWD[0])
    for rel, data in paths.items():
        proc = subprocess.run(("git", "hash-object", "-w", "--stdin"), cwd=CWD[0],
                              input=data, capture_output=True, env=git_env())
        if proc.returncode != 0:
            raise SetupError("hash-object failed: %s" % proc.stderr.decode("utf-8", "replace"))
        blob = proc.stdout.decode().strip()
        git(["update-index", "--add", "--cacheinfo", "100644,%s,%s" % (blob, rel)],
            cwd=CWD[0])
    tree = git_out(["write-tree"], cwd=CWD[0])
    proc = subprocess.run(("git",) + tuple(COMMIT_SAFE) + ("commit-tree", tree, "-p",
                          git_out(["rev-parse", "HEAD"], CWD[0])),
                          cwd=CWD[0], input=b"fixture commit\n", capture_output=True,
                          env=git_env())
    if proc.returncode != 0:
        raise SetupError("commit-tree failed: %s" % proc.stderr.decode("utf-8", "replace"))
    commit = proc.stdout.decode().strip()
    git(["update-ref", "refs/heads/fixture", commit], cwd=CWD[0])
    return commit


CWD = [None]


def build_red_fixture(repo, rev, dest, control_bytes):
    """Clone the lane at REV and commit the frozen control in place of the ledger."""
    clone_at(repo, rev, dest)
    CWD[0] = dest
    return commit_tree_with({LEDGER_REL: control_bytes})


# ------------------------------------------------------- ledger mutations ----

def ledger_bytes_at(fixture, rev):
    proc = git(["show", "%s:%s" % (rev, LEDGER_REL)], cwd=fixture)
    return proc.stdout


def ledger_rows(text):
    """The pipe-table rows of a ledger, as (index, cells) pairs, fences skipped."""
    rows = []
    fenced = False
    for index, raw in enumerate(text.splitlines()):
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = line.strip("|").split("|")
        first = cells[0].strip().strip("`*_ ")
        if not first or "/" not in first or first.startswith(":"):
            continue
        rows.append((index, [c.strip() for c in cells]))
    return rows


def replace_row_cell(text, row_index, cell_index, value):
    lines = text.splitlines()
    row = lines[row_index]
    cells = row.strip("|").split("|")
    cells[cell_index] = " %s " % value
    lines[row_index] = "|" + "|".join(cells) + "|"
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def mutate_ledger(kind):
    """Return a function (original_bytes -> mutated_bytes) for one mutation kind.

    * `selfptr`  — one row's accountability pointer is redirected at the ledger file
                   itself.  The ledger's own bytes contain every instrument basename, so
                   this pointer *resolves*; only a counter that refuses a self-pointer
                   sees the defect.  The round-51 counter accepts it.
    * `generic`  — one row's description is replaced by a generic phrase with no
                   instrument-specific functional content.  It is not empty, so an
                   empty-description check does not see it.  The round-51 counter
                   accepts it.
    * `duprow`   — one row is duplicated, so the population is not unique.
    """
    def mutate_selfptr(text):
        rows = ledger_rows(text)
        if not rows:
            raise SetupError("ledger has no rows to mutate")
        index, cells = rows[0]
        return replace_row_cell(text, index, 2, "`%s`" % LEDGER_REL).encode("utf-8")

    def mutate_generic(text):
        rows = ledger_rows(text)
        if not rows:
            raise SetupError("ledger has no rows to mutate")
        index, cells = rows[0]
        return replace_row_cell(
            text, index, 1,
            "does things.").encode("utf-8")

    def mutate_duprow(text):
        rows = ledger_rows(text)
        if not rows:
            raise SetupError("ledger has no rows to mutate")
        index, cells = rows[0]
        lines = text.splitlines()
        lines.insert(index + 1, lines[index])
        return ("\n".join(lines) + ("\n" if text.endswith("\n") else "")).encode("utf-8")

    return {"selfptr": mutate_selfptr, "generic": mutate_generic,
            "duprow": mutate_duprow}[kind]


def build_mutation_fixture(repo, rev, dest, kind):
    """Clone the lane at REV and commit the production ledger with one defect injected."""
    clone_at(repo, rev, dest)
    CWD[0] = dest
    original = ledger_bytes_at(dest, rev)
    mutated = mutate_ledger(kind)(original.decode("utf-8", "replace"))
    return commit_tree_with({LEDGER_REL: mutated})


def build_green_fixture(repo, rev, dest, overlay):
    """Clone the lane at REV; the production ledger stays as it is at that revision."""
    clone_at(repo, rev, dest)
    CWD[0] = dest
    if not overlay:
        return rev
    paths = {}
    for rel in overlay:
        if rel == LEDGER_REL:
            raise SetupError("--overlay may not replace the ledger")
        src = os.path.join(repo, rel)
        if not os.path.isfile(src):
            raise SetupError("--overlay %s is not a file in the lane" % rel)
        with open(src, "rb") as fh:
            paths[rel] = fh.read()
    return commit_tree_with(paths)


# ------------------------------------------------------------- run a case ----

def sandbox_env(sandbox, work):
    env = {
        "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "TMPDIR": os.path.join(work, "tmp"),
    }
    for name, sub in (("HOME", "home"), ("XDG_CACHE_HOME", "home/.cache"),
                      ("XDG_CONFIG_HOME", "home/.config"),
                      ("XDG_DATA_HOME", "home/.local/share"),
                      ("XDG_STATE_HOME", "home/.local/state")):
        env[name] = os.path.join(sandbox, sub)
    for path in (env["TMPDIR"], env["HOME"], env["XDG_CACHE_HOME"], env["XDG_CONFIG_HOME"],
                 env["XDG_DATA_HOME"], env["XDG_STATE_HOME"]):
        os.makedirs(path, exist_ok=True)
    return env


def run_counter(counter, args, work, sandbox, timeout=RUN_TIMEOUT):
    try:
        proc = subprocess.run([sys.executable, "-I", counter] + args,
                              cwd=work, capture_output=True,
                              env=sandbox_env(sandbox, work), timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout after %ss" % timeout
    return (proc.returncode,
            proc.stdout.decode("utf-8", "replace"),
            proc.stderr.decode("utf-8", "replace"))


def final_line(text):
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()
    return ""


def fields_of(line):
    out = {}
    for key, value in re.findall(r"\b([a-z_]+)=([^\s`]+)", line):
        out.setdefault(key, value)
    return out


# ------------------------------------------------------------- the checks ----

def first_present(fields, names):
    for name in names:
        if name in fields:
            return name, fields[name]
    return None, None


def nonzero(field_value):
    try:
        return int(field_value) > 0
    except (TypeError, ValueError):
        return False


def evaluate(case, rc, out, err, profile, expected_line):
    """Return (ok, findings, evidence dict) for one fixture case.

    `case` names the fixture.  `red` is the frozen do-nothing control; `mut-<kind>` is a
    production ledger with exactly one defect injected, so the two defect classes can be
    told apart.  The required red signal set comes from the profile, keyed by case.
    """
    line = final_line(out)
    fields = fields_of(line)
    findings = []
    evidence = {
        "case": case, "exit": rc, "final_line": line, "fields": fields,
        "stdout_sha256": hashlib.sha256(out.encode("utf-8")).hexdigest(),
        "stdout_lines": len(out.splitlines()),
        "stderr_tail": err.strip().splitlines()[-6:],
    }

    if rc == 124:
        findings.append("counter timed out")
        return False, findings, evidence
    if rc == 2 and re.search(r"unrecognized arguments|no such option|invalid option",
                              (out + err), re.I):
        findings.append("counter rejected the frozen argument set (exit 2, usage error)")
        evidence["usage_error"] = True
        return False, findings, evidence

    verdict = fields.get("verdict")
    evidence["verdict"] = verdict
    if verdict is None:
        findings.append("no verdict= field on the final line")
        return False, findings, evidence

    if expected_line is not None:
        evidence["expected_final_line"] = expected_line
        evidence["final_line_matches_expected"] = (line == expected_line)
        if line != expected_line:
            findings.append("final line is not byte-equal to the expected line")

    if case == "green":
        if rc != 0:
            findings.append("exit %d, expected 0" % rc)
        if verdict != "TARGET_MET":
            findings.append("verdict %s, expected TARGET_MET" % verdict)
        if "absent" in fields:
            findings.append("ledger reported absent in the production fixture")
        for group in ("self_pointer", "context"):
            name, value = first_present(fields, profile["fields"].get(group, []))
            if name is not None and nonzero(value):
                findings.append("defect field %s=%s is non-zero on the green fixture"
                                % (name, value))
        return (not findings), findings, evidence

    # every other case is a failing (red-family) case
    if rc == 0:
        findings.append("exit 0, expected 1")
    if verdict != "TARGET_MISSED":
        findings.append("verdict %s, expected TARGET_MISSED" % verdict)
    if "absent" in fields:
        findings.append("ledger reported absent: the failure is a missing-ledger "
                         "failure, not a self-pointer/context failure")
    evidence["detail_self_hits"] = re.findall(profile["detail_self_regex"], out, re.I)
    evidence["detail_context_hits"] = re.findall(profile["detail_context_regex"], out, re.I)
    name, value = first_present(fields, profile["fields"].get("self_pointer", []))
    evidence["self_pointer_field"] = None if name is None else "%s=%s" % (name, value)
    name, value = first_present(fields, profile["fields"].get("context", []))
    evidence["context_field"] = None if name is None else "%s=%s" % (name, value)
    signals = {
        "self_pointer": bool(evidence["self_pointer_field"]
                             and nonzero(evidence["self_pointer_field"].split("=")[1]))
                        or bool(evidence["detail_self_hits"]),
        "context": bool(evidence["context_field"]
                        and nonzero(evidence["context_field"].split("=")[1]))
                   or bool(evidence["detail_context_hits"]),
    }
    evidence["red_signals"] = signals
    required = profile.get("required_red_signals", {})
    if isinstance(required, dict):
        required = required.get(case, required.get("default", []))
    missing = [s for s in required if not signals.get(s)]
    if missing:
        findings.append(
            "failure does not name the required defect signal(s): %s "
            "(a coverage-only failure — the counter notices rows are missing but never "
            "says why the control's rows are unaccountable)" % ", ".join(missing))
    return (not findings), findings, evidence


# ------------------------------------------------------------------- main ----

def read_expected_final(path):
    """Parse a "case<TAB>exact final line" file into a dict."""
    out = {}
    with open(path) as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            case, _, expected = line.partition("\t")
            out[case.strip()] = expected
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="C1 red/green fixture harness (round 52)")
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--rev", default=DEFAULT_REV)
    ap.add_argument("--counter", required=True,
                    help="absolute path to the candidate counter script")
    ap.add_argument("--control", default=DEFAULT_CONTROL)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--work", required=True, help="scratch directory for fixtures")
    ap.add_argument("--out", required=True, help="evidence directory")
    ap.add_argument("--cases", default="green,red")
    ap.add_argument("--overlay", default="",
                    help="comma-separated repo-relative files to add to the fixtures")
    ap.add_argument("--expect-final", default=None,
                    help="file with 'case<TAB>exact final line' expectations")
    args = ap.parse_args(argv)

    try:
        repo = os.path.abspath(args.repo)
        if not os.path.isdir(repo):
            raise SetupError("--repo %s is not a directory" % repo)
        counter = os.path.abspath(args.counter)
        if not os.path.isfile(counter):
            raise SetupError("--counter %s is not a file" % counter)
        control = os.path.abspath(args.control)
        if not os.path.isfile(control):
            raise SetupError("--control %s is not a file" % control)
        with open(args.profile) as fh:
            profile = json.load(fh)
        expected_final = read_expected_final(args.expect_final) if args.expect_final else {}
        work = os.path.abspath(args.work)
        out_dir = os.path.abspath(args.out)
        if os.path.realpath(work) in ("/tmp", "/var/tmp", "/dev/shm"):
            raise SetupError("--work must not be a system temp root: %s" % work)
        os.makedirs(work, exist_ok=True)
        os.makedirs(out_dir, exist_ok=True)
        rev = git_out(["rev-parse", "--verify", "%s^{commit}" % args.rev], repo)
        with open(control, "rb") as fh:
            control_bytes = fh.read()
        overlay = [p.strip() for p in args.overlay.split(",") if p.strip()]

        cases = [c.strip() for c in args.cases.split(",") if c.strip()]
        own_paths = [os.path.relpath(out_dir, repo)]
        before = lane_integrity(repo, own_paths)
        results = []
        for case in cases:
            if case == "green":
                fixture = os.path.join(work, "fixture-green")
                case_rev = build_green_fixture(repo, rev, fixture, overlay)
            elif case == "red":
                fixture = os.path.join(work, "fixture-red")
                case_rev = build_red_fixture(repo, rev, fixture, control_bytes)
            elif case.startswith("mut-"):
                kind = case[len("mut-"):]
                fixture = os.path.join(work, "fixture-%s" % case)
                case_rev = build_mutation_fixture(repo, rev, fixture, kind)
            else:
                raise SetupError("unknown case %r" % case)
            case_work = os.path.join(work, "work-%s" % case)
            os.makedirs(case_work, exist_ok=True)
            rc, out, err = run_counter(
                counter, ["--repo", fixture, "--rev", case_rev, "--work", case_work],
                case_work, os.path.join(case_work, "sandbox"))
            ok, findings, evidence = evaluate(case, rc, out, err, profile,
                                              expected_final.get(case))
            # Scratch confinement: the counter read a repository; it must not have
            # written into it.  The fixture worktree is empty by construction (the
            # fixture is a --no-checkout clone), so any file the counter left outside
            # `.git/` there is a write.  `git status` cannot be used for this: on a
            # no-checkout clone every tracked path reads as deleted.
            residue = []
            for root, dirs, files in os.walk(fixture):
                dirs[:] = [d for d in dirs if d != ".git"]
                for name in files:
                    residue.append(os.path.relpath(os.path.join(root, name), fixture))
            residue.sort()
            evidence["fixture_worktree_residue"] = residue
            evidence["scratch_files_after"] = sorted(
                os.path.relpath(os.path.join(root, name), case_work)
                for root, dirs, files in os.walk(case_work) for name in files)
            if residue:
                findings.append("counter wrote into the repository it reads: %s"
                                % ", ".join(residue[:5]))
                ok = False
            evidence.update({
                "expect": "TARGET_MET/exit 0" if case == "green" else
                          "TARGET_MISSED/exit 1 with self-pointer+context defect",
                "ok": ok, "findings": findings,
                "fixture": fixture, "fixture_rev": case_rev,
                "counter": counter,
                "control_sha256": hashlib.sha256(control_bytes).hexdigest(),
            })
            results.append(evidence)
            with open(os.path.join(out_dir, "%s.stdout.txt" % case), "w") as fh:
                fh.write(out)
            with open(os.path.join(out_dir, "%s.stderr.txt" % case), "w") as fh:
                fh.write(err)
        after = lane_integrity(repo, own_paths)
        lane_clean = lane_unchanged(before, after)
        summary = {
            "harness": "c1-fixture-harness.py",
            "seat": "C1Fixture",
            "round": 52,
            "repo": repo, "rev": rev, "counter": counter,
            "control": control,
            "control_sha256": hashlib.sha256(control_bytes).hexdigest(),
            "profile": os.path.abspath(args.profile),
            "overlay": overlay,
            "work": work,
            "lane_integrity_before": before, "lane_integrity_after": after,
            "lane_unchanged": lane_clean,
            "cases": results,
            "verdict": "PASS" if (all(r["ok"] for r in results) and lane_clean) else "FAIL",
        }
        with open(os.path.join(out_dir, "harness-summary.json"), "w") as fh:
            json.dump(summary, fh, indent=1, sort_keys=True)
        lines = []
        for r in results:
            lines.append("case=%s exit=%s verdict=%s ok=%s final=%r" % (
                r["case"], r["exit"], r.get("verdict"), r["ok"], r["final_line"]))
            for finding in r["findings"]:
                lines.append("  finding: %s" % finding)
        lines.append("lane_unchanged=%s" % lane_clean)
        lines.append("HARNESS: verdict=%s cases=%d" % (summary["verdict"], len(results)))
        print("\n".join(lines))
        return 0 if summary["verdict"] == "PASS" else 1
    except SetupError as exc:
        print("C1_FIXTURE_HARNESS: setup=error detail=%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
