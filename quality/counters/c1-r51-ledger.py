#!/usr/bin/env python3
"""c1-r51-ledger.py — PRED-C1-r51: the tracked lane-level tool ledger is complete and accountable.

Draft for `quality/counters/c1-r51-ledger.py` (mado round 51, w1 build, hyaku run 10).
The frozen predicate sentence from `.ufo/waves/round-51/claims.md`, copied byte-for-byte:

> PRED-C1-r51: `python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev <rev> --work <scratch>`
> exits 0 with final line `C1_R51: population=<P> ledger_rows=<P> uncovered=0 dangling=0
> bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=<rev>` where `P` is the number of
> files under `tools/`, `quality/*.py` and `quality/counters/*.py` at `<rev>`, each such file
> appears exactly once in `quality/tool-ledger.md` with a non-empty description and an
> accountability pointer naming an existing repo file that contains the file's basename; at the
> round base `6ca8c559a4a3d6d361101592116eea2bc7452437` the same command prints
> `verdict=TARGET_MISSED ledger=absent` and exits 1.

What it measures (never the working tree: every byte comes from `--rev` in a scratch clone):

``p``  population — one `git ls-tree -r --name-only <rev>` listing (so a pointer may name any file
       in the tree, including root records such as `PROVINCE.md`), filtered to every file under
       `tools/` (any extension, `__pycache__`/`.pyc`/`.pyo` excluded) plus the direct children
       `quality/*.py` and `quality/counters/*.py`. This is the predicate's `P`.
``l``  ledger — `quality/tool-ledger.md` at `<rev>` exists and parses into pipe-table rows whose
       first cell is a population path (fenced code blocks are documentation, never rows, as in
       the gate). `ledger_rows` counts every parsed row, so a duplicate row
       pushes `ledger_rows` above `P` and misses on its own; it is also reported as `dup=<n>`.
``u``  uncovered — population files with no row.
``d``  dangling — rows whose first cell is not a population path.
``b``  bad_pointer — rows with no pointer token naming a repo file that exists at `<rev>` and whose
       bytes contain the row file's basename.
``e``  empty_desc — rows whose description cell, after stripping markdown emphasis and backticks,
       is empty or punctuation only (a dash is not a description).

Clause ``max`` (second requirement of the predicate's command, not a separate number): the
checker at `--checker` — the lane's own `quality/check-tool-ledger.py` — read from the same
revision, run as `python3 -I <clone>/<checker> --repo <clone> --rev <rev>`, must print a `LEDGER:`
line whose six numbers equal this counter's own independent measurement and whose verdict is
`TARGET_MET`, and its `--selftest` must pass (`n/n passed` with n == total; a `selftest=ok` token is
accepted when no ratio is printed). The counter does not trust that line: a parroting checker whose
numbers disagree with the ledger's real shape misses, and so does a ledger whose bytes the checker
rubber-stamps.

Scratch: the clone is `git clone --shared --no-checkout` + `checkout --detach <rev>` created inside
`--work` (default: a fresh directory under the process temp dir, i.e. `TMPDIR` when set — no
hard-coded temporary path anywhere in this file), removed on exit together with a `--work`
directory this run created. Child processes get `HOME`, `TMPDIR` and the `XDG_*` homes under
`--work`, so a checker selftest never writes outside the scratch tree.

Exit codes: 0 = TARGET_MET, 1 = TARGET_MISSED (ledger absent or any field above non-zero), 2 =
setup error (bad `--repo`/`--rev`/`--work`/`--checker`, clone failure, checker timeout).

Usage:
  python3 -I c1-r51-ledger.py --repo <lane> --rev <rev> --work <scratch> [--checker quality/check-tool-ledger.py]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "c1-r51-ledger.py"
LEDGER_REL = "quality/tool-ledger.md"
DEFAULT_CHECKER = "quality/check-tool-ledger.py"
BASE_REV = "6ca8c559a4a3d6d361101592116eea2bc7452437"
RUN_TIMEOUT = 600
REFUSED_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
SELFTEST_FALLBACK_RC = 2

LEDGER_LINE = re.compile(r"^\s*LEDGER:")
FIELD = re.compile(r"\b([a-z_]+)=([^\s`]+)")
RATIO_PASSED = re.compile(r"(\d+)\s*/\s*(\d+)\s*(?:cases|checks|tests)?\s*(?:passed|ok)\b", re.I)
SELFTEST_FAIL = re.compile(r"selftest\s*[=:]\s*fail", re.I)
SELFTEST_OK = re.compile(r"selftest\s*[=:]\s*ok", re.I)
PLACEHOLDER = re.compile(r"^[\s\-–—_*`.]+$")
LINE_ANCHOR = re.compile(r":\d+(?:-\d+)?$")
EMPHASIS = "`*_ \t"


class SetupError(Exception):
    pass


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.setdefault("LC_ALL", "C.UTF-8")
    return env


def git(repo, *args):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True, env=git_env())
    if proc.returncode != 0:
        raise SetupError("git %s failed in %s: %s" % (
            " ".join(args), repo, proc.stderr.decode("utf-8", "replace").strip()[:400]))
    return proc.stdout


def resolve_rev(repo, rev):
    try:
        return git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}").decode().strip()
    except SetupError:
        raise SetupError("--rev %r does not resolve to a commit in %s" % (rev, repo))


def make_clone(repo, rev, work):
    clone = os.path.join(work, "clone-%d" % os.getpid())
    if os.path.exists(clone):
        shutil.rmtree(clone)
    try:
        git(work, "clone", "-q", "--shared", "--no-checkout", repo, clone)
    except SetupError as exc:
        raise SetupError("clone of %s failed: %s" % (repo, exc))
    try:
        git(clone, "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", rev)
    except SetupError:
        git(clone, "fetch", "-q", "--no-tags", "origin", rev)
        git(clone, "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", rev)
    head = git(clone, "rev-parse", "HEAD").decode().strip()
    top = git(clone, "rev-parse", "--show-toplevel").decode().strip()
    if head != rev:
        raise SetupError("clone HEAD %s != resolved rev %s" % (head, rev))
    if os.path.realpath(top) != os.path.realpath(clone):
        raise SetupError("clone toplevel %s != %s" % (top, clone))
    return clone


def listing(clone, rev):
    out = git(clone, "ls-tree", "-r", "--name-only", rev)
    return [p for p in out.decode("utf-8", "surrogateescape").splitlines() if p]


def population(paths):
    pop = []
    for path in paths:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            pop.append(path)
            continue
        for root in ("quality/counters/", "quality/"):
            if not path.startswith(root):
                continue
            rest = path[len(root):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
            break
    return sorted(set(pop))


def show(clone, rev, rel):
    return git(clone, "show", "%s:%s" % (rev, rel))


def parse_rows(text):
    rows = []
    fenced = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip(EMPHASIS) if cells else ""
        if not first or "/" not in first or first.startswith(":") or set(first) <= set("-: "):
            continue
        rows.append({
            "path": first,
            "desc": cells[1] if len(cells) > 1 else "",
            "pointer": " | ".join(cells[2:]) if len(cells) > 2 else "",
        })
    return rows


def pointer_tokens(cell):
    tokens = re.findall(r"`([^`\n]+)`", cell)
    if not tokens:
        tokens = re.split(r"[,;]|\s+", cell)
    out = []
    for token in tokens:
        token = token.strip(EMPHASIS)
        token = re.sub(r"^\./", "", token)
        token = LINE_ANCHOR.sub("", token)
        if not token or token.startswith(("/", "~", "$")):
            continue
        if any(ch in token for ch in "<>():#?*\"'"):
            continue
        if "/" not in token and not re.search(r"\.(md|py|sh|json|txt|ya?ml)$", token):
            continue
        out.append(token)
    return out


def pointer_resolves(clone, rev, files, row_path, pointer, cache):
    base = os.path.basename(row_path)
    for token in pointer_tokens(pointer):
        if token not in files:
            continue
        if token not in cache:
            try:
                cache[token] = show(clone, rev, token)
            except SetupError:
                cache[token] = b""
        if base.encode() in cache[token]:
            return True
    return False


def describe(pop, rows, clone, rev, files):
    """Independent measurement: returns the field dict plus detail lines."""
    in_pop = set(pop)
    seen = set()
    counts = {"uncovered": 0, "dangling": 0, "bad_pointer": 0, "empty_desc": 0, "dup": 0}
    details = []
    cache = {}
    for row in rows:
        path = row["path"]
        if path not in in_pop:
            counts["dangling"] += 1
            details.append("dangling path=%s" % path)
            continue
        if path in seen:
            counts["dup"] += 1
            details.append("dup path=%s" % path)
            continue
        seen.add(path)
        desc = row["desc"].strip(EMPHASIS)
        if not desc or PLACEHOLDER.match(desc):
            counts["empty_desc"] += 1
            details.append("empty_desc path=%s" % path)
        if not pointer_resolves(clone, rev, files, path, row["pointer"], cache):
            counts["bad_pointer"] += 1
            details.append("bad_pointer path=%s pointer=%r" % (
                path, row["pointer"].strip()[:120]))
    missing = sorted(in_pop - seen)
    counts["uncovered"] = len(missing)
    details.extend("uncovered path=%s" % p for p in missing)
    return {
        "population": len(pop),
        "ledger_rows": len(rows),
        "uncovered": counts["uncovered"],
        "dangling": counts["dangling"],
        "bad_pointer": counts["bad_pointer"],
        "empty_desc": counts["empty_desc"],
        "dup": counts["dup"],
    }, details


def sandbox_env(sandbox):
    env = {
        "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    for name, sub in (("HOME", "home"), ("TMPDIR", "tmp"),
                      ("XDG_CACHE_HOME", "home/.cache"), ("XDG_CONFIG_HOME", "home/.config"),
                      ("XDG_DATA_HOME", "home/.local/share"),
                      ("XDG_STATE_HOME", "home/.local/state")):
        path = os.path.join(sandbox, sub)
        os.makedirs(path, exist_ok=True)
        env[name] = path
    return env


def run_python(script, args, work, sandbox, timeout=RUN_TIMEOUT):
    try:
        proc = subprocess.run([sys.executable, "-I", script] + args, cwd=work,
                              capture_output=True, env=sandbox_env(sandbox), timeout=timeout)
    except subprocess.TimeoutExpired:
        raise SetupError("checker %s timed out after %ss" % (script, timeout))
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), \
        proc.stderr.decode("utf-8", "replace")


def checker_selftest(script, work, sandbox):
    rc, out, err = run_python(script, ["--selftest", "--work", os.path.join(sandbox, "selftest")],
                              work, sandbox)
    form = "with-work"
    if rc == SELFTEST_FALLBACK_RC and re.search(
            r"unrecognized arguments|no such option|invalid option", err or out, re.I):
        rc, out, err = run_python(script, ["--selftest"], work, sandbox)
        form = "bare"
    text = out + "\n" + err
    if rc != 0:
        return False, "failed", "exit=%s form=%s" % (rc, form)
    if SELFTEST_FAIL.search(text):
        return False, "failed", "fail-token form=%s" % form
    ratio = RATIO_PASSED.findall(text)
    if ratio:
        passed, total = int(ratio[-1][0]), int(ratio[-1][1])
        if total <= 0 or passed != total:
            return False, "failed", "ratio=%d/%d form=%s" % (passed, total, form)
        return True, "ok", "ratio=%d/%d form=%s" % (passed, total, form)
    if SELFTEST_OK.search(text):
        return True, "ok", "token-ok form=%s" % form
    return False, "failed", "no-ok-marker form=%s" % form


def checker_ledger(script, clone, rev, work, sandbox, mine):
    rc, out, err = run_python(script, ["--repo", clone, "--rev", rev], work, sandbox)
    line = None
    for candidate in out.splitlines():
        if LEDGER_LINE.match(candidate):
            line = candidate
    if line is None:
        return False, "no-line", "exit=%s" % rc, out, err
    fields = dict(FIELD.findall(line))
    parsed = {}
    for name in ("population", "ledger_rows", "uncovered", "dangling", "bad_pointer",
                 "empty_desc"):
        if not fields.get(name, "").isdigit():
            return False, "no-line", "missing=%s line=%r" % (name, line.strip()[:160]), out, err
        parsed[name] = int(fields[name])
    if fields.get("ledger") == "absent":
        return False, "absent", "line=%r" % line.strip()[:160], out, err
    if fields.get("verdict") != "TARGET_MET" or rc != 0:
        return False, "failed", "verdict=%s exit=%s" % (fields.get("verdict"), rc), out, err
    for name, value in parsed.items():
        if value != mine[name]:
            return False, "failed", "disagree %s checker=%d counter=%d" % (
                name, value, mine[name]), out, err
    if parsed["population"] != parsed["ledger_rows"]:
        return False, "failed", "population=%d ledger_rows=%d" % (
            parsed["population"], parsed["ledger_rows"]), out, err
    return True, "ok", "rev=%s" % fields.get("rev", "<none>"), out, err


def resolve_work(work):
    created = False
    if work is None:
        base = os.environ.get("TMPDIR") or None
        work = tempfile.mkdtemp(prefix="c1-r51-", dir=base)
        created = True
    work = os.path.abspath(work)
    if os.path.exists(work) and not os.path.isdir(work):
        raise SetupError("--work %s is not a directory" % work)
    try:
        os.makedirs(work, exist_ok=True)
    except OSError as exc:
        raise SetupError("--work %s is not creatable: %s" % (work, exc))
    if not os.access(work, os.W_OK | os.X_OK):
        raise SetupError("--work %s is not writable" % work)
    return work, created


def normalise_checker(value):
    rel = os.path.normpath(value).replace(os.sep, "/")
    if os.path.isabs(rel) or rel.startswith("..") or rel in (".", ""):
        raise SetupError("--checker must be a repo-relative path, got %r" % value)
    return rel


def main(argv=None):
    ap = argparse.ArgumentParser(description="PRED-C1-r51: tracked lane-level tool ledger")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--checker", default=DEFAULT_CHECKER)
    args = ap.parse_args(argv)

    work = None
    created = False
    clone = None
    try:
        repo = os.path.abspath(args.repo)
        if not os.path.isdir(repo):
            raise SetupError("--repo %s is not a directory" % repo)
        try:
            git(repo, "rev-parse", "--git-dir")
        except SetupError:
            raise SetupError("--repo %s is not a git repository" % repo)
        rev = resolve_rev(repo, args.rev)
        checker_rel = normalise_checker(args.checker)
        work, created = resolve_work(args.work)
        clone = make_clone(repo, rev, work)
        files = set(listing(clone, rev))
        pop = population(sorted(files))

        if LEDGER_REL not in files:
            print("detail: %s absent at %s" % (LEDGER_REL, rev[:12]))
            print("C1_R51: verdict=TARGET_MISSED ledger=absent population=%d rev=%s"
                  % (len(pop), rev))
            return 1

        ledger_text = show(clone, rev, LEDGER_REL).decode("utf-8", "replace")
        rows = parse_rows(ledger_text)
        mine, details = describe(pop, rows, clone, rev, files)
        for line in details:
            print("detail: %s" % line)

        selftest_rc, selftest_state, selftest_note = False, "absent", "checker-absent"
        sandbox = os.path.join(work, "sandbox-%d" % os.getpid())
        ledger_rc, ledger_state, ledger_note = False, "absent", "checker-absent"
        checker_script = os.path.join(clone, checker_rel)
        if checker_rel not in files:
            print("detail: checker %s absent at %s" % (checker_rel, rev[:12]))
        else:
            selftest_rc, selftest_state, selftest_note = checker_selftest(
                checker_script, work, sandbox)
            print("detail: checker selftest %s (%s)" % (selftest_state, selftest_note))
            if not selftest_rc and os.path.realpath(work).startswith(
                    tuple(os.path.realpath(r) for r in REFUSED_ROOTS)):
                print("detail: hint: the gate refuses --selftest work under %s"
                      % ", ".join(REFUSED_ROOTS))
            ledger_rc, ledger_state, ledger_note, out, err = checker_ledger(
                checker_script, clone, rev, work, sandbox, mine)
            print("detail: checker ledger %s (%s)" % (ledger_state, ledger_note))
            if not ledger_rc:
                for line in (out + err).strip().splitlines()[-12:]:
                    print("detail: checker: %s" % line)

        clean = (mine["population"] > 0 and mine["ledger_rows"] == mine["population"]
                 and not any(mine[k] for k in ("uncovered", "dangling", "bad_pointer",
                                               "empty_desc", "dup")))
        met = clean and selftest_rc and ledger_rc
        line = ("C1_R51: population=%d ledger_rows=%d uncovered=%d dangling=%d bad_pointer=%d "
                "empty_desc=%d selftest=%s" % (
                    mine["population"], mine["ledger_rows"], mine["uncovered"],
                    mine["dangling"], mine["bad_pointer"], mine["empty_desc"],
                    "ok" if selftest_rc else selftest_state))
        if mine["dup"]:
            line += " dup=%d" % mine["dup"]
        if not ledger_rc:
            line += " checker=%s" % ledger_state
        line += " verdict=%s rev=%s" % ("TARGET_MET" if met else "TARGET_MISSED", rev)
        print(line)
        return 0 if met else 1
    except SetupError as exc:
        print("C1_R51: setup=error detail=%s" % exc, file=sys.stderr)
        return 2
    finally:
        if clone and os.path.isdir(clone):
            shutil.rmtree(clone, ignore_errors=True)
        sandbox_left = os.path.join(work, "sandbox-%d" % os.getpid()) if work else None
        if sandbox_left and os.path.isdir(sandbox_left):
            shutil.rmtree(sandbox_left, ignore_errors=True)
        if created and work and os.path.isdir(work):
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
