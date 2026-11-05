#!/usr/bin/env python3
"""mado round 87, C2 calibration: control-figure fidelity.

Predicate (frozen in .ufo/waves/round-87/claims-declaration-r87.md, section C2): TARGET_MET iff n = 2 and every figure is reconciled — it reproduces at REV, or an append-only correction block (a `Correction (round 87)` heading in the same file, naming the figure id and its re-derived value) exists.

Every input is read from REV with `git show REV:<path>`; the working tree is never read. Reconciliation files are the two
r86 record files named in CORRECTION_FILES. F1 is re-derived by calling the held round-85 counter's own case_correct on
the border-size-int case (never the r86 model). F2 is re-derived by re-running the round-86 C1 counter at the revision its
receipt names, with the controls that receipt pinned. A stated text absent from its file at REV is a setup error; the
figure file is never edited to match it.

Score = 10 * reconciled / n. Exit map: 0 target met, 1 target missed, 2 setup error (never a verdict).
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

FIGURE_SCHEMA = "r86-figures-r87-v1"
KINDS = ("held_rule_witness", "flood_pair")
R85_COUNTER = "quality/counters/c2-r85-status-classes.py"
R86_CASES = ".ufo/waves/round-86/controls/c2-cases-r86.json"
R86_RECEIPT = ".ufo/waves/round-86/receipts/final-c1-r86.txt"
C1_COUNTER = "quality/counters/c1-r86-refusal-records.py"
C1_CONTROLS = ".ufo/waves/round-86/controls/c1-cases-r86.json"
C1_CARRIED = ".ufo/waves/round-85/controls/c1-cases-r85.json"
CORRECTION_FILES = ("corpus/knowledge/refusal-records-clause-observations-r86.md", "SCORECARD.md")
CORRECTION_HEADING = "Correction (round 87"
HELD_CASE = "border-size-int"
GIT_SCRUB = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
             "GIT_ALTERNATE_OBJECT_DIRECTORIES")
HEADING = re.compile(r"^(#{1,6})(?:\s+(.*))?$")


class Setup(Exception):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_bytes(path, data):
    with open(path, "wb") as fh:
        fh.write(data)


def git_env(extra=None):
    env = dict((key, value) for key, value in os.environ.items() if key not in GIT_SCRUB)
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    if extra:
        env.update(extra)
    return env


def git_out(repo, *args):
    proc = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, env=git_env())
    if proc.returncode != 0:
        raise Setup("git %s failed: %s" % (args[0], proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def resolve_rev(repo, rev):
    proc = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, env=git_env())
    if proc.returncode != 0:
        raise Setup("unknown revision %s" % rev)
    return proc.stdout.decode("ascii").strip()


def git_bytes(repo, rev, path):
    try:
        return git_out(repo, "show", "%s:%s" % (rev, path))
    except Setup as exc:
        raise Setup("cannot read %s at %s: %s" % (path, rev, exc))


def load_figures(raw):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except ValueError as exc:
        raise Setup("figure file is not JSON: %s" % exc)
    if not isinstance(doc, dict) or doc.get("schema") != FIGURE_SCHEMA:
        raise Setup("figure file schema is not %s" % FIGURE_SCHEMA)
    figures = doc.get("figures")
    if not isinstance(figures, list) or not figures:
        raise Setup("figure file has no figures")
    for fig in figures:
        for key in ("id", "kind", "stated", "stated_at"):
            if key not in fig:
                raise Setup("figure missing field %s" % key)
        if fig["kind"] not in KINDS:
            raise Setup("figure %s has unknown kind %s" % (fig["id"], fig["kind"]))
        for loc in fig["stated_at"]:
            if "path" not in loc or "text" not in loc:
                raise Setup("figure %s has a stated_at entry without path/text" % fig["id"])
    return figures


def token_in(token, text):
    return re.search(r"(?<![0-9A-Za-z_])%s(?![0-9A-Za-z_])" % re.escape(token), text) is not None


def correction_blocks(text):
    """Yield (title, block) for each heading outside code fences; a block runs to the next heading of the same or higher level."""
    lines = text.splitlines()
    heads = []
    fence = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        match = HEADING.match(line)
        if match:
            heads.append((index, len(match.group(1)), (match.group(2) or "").strip()))
    for k, (index, level, title) in enumerate(heads):
        end = len(lines)
        for later_index, later_level, _ in heads[k + 1:]:
            if later_level <= level:
                end = later_index
                break
        yield title, "\n".join(lines[index:end])


def reconciles(fig_id, value, texts):
    for text in texts:
        for title, block in correction_blocks(text):
            if CORRECTION_HEADING in title and token_in(fig_id, block) and token_in(value, block):
                return True
    return False


def derive_held_rule(repo, rev, work):
    path = os.path.join(work, "c2_r85_status_classes.py")
    write_bytes(path, git_bytes(repo, rev, R85_COUNTER))
    try:
        spec = importlib.util.spec_from_file_location("c2_r85_status_classes", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cases = json.loads(git_bytes(repo, rev, R86_CASES).decode("utf-8"))["cases"]
        named = [case for case in cases if case.get("name") == HELD_CASE]
        if len(named) != 1:
            raise Setup("case %s is not unique in the r86 controls" % HELD_CASE)
        correct = bool(module.case_correct(named[0], 0, named[0]["frozen"]))
    except Setup:
        raise
    except Exception as exc:
        raise Setup("cannot evaluate held r85 counter: %s" % exc)
    return "%d/1" % int(correct)


def derive_flood(repo, rev, work):
    receipt = git_bytes(repo, rev, R86_RECEIPT).decode("utf-8", "replace")
    m_rev = re.search(r"^MADO_R86_REFUSALS: cases=\d+ .*?\brev=([0-9a-f]{40})\b", receipt, re.M)
    m_base = re.search(r"^MADO_R86_BASE: .*?\bbase_rev=([0-9a-f]{40})\b", receipt, re.M)
    m_ctl = re.search(r"^MADO_R86_CONTROL: sha256=([0-9a-f]{64})\b", receipt, re.M)
    if not (m_rev and m_base and m_ctl):
        raise Setup("receipt %s lacks rev, base_rev or control sha256" % R86_RECEIPT)
    measured = resolve_rev(repo, m_rev.group(1))
    base = resolve_rev(repo, m_base.group(1))
    flood_dir = os.path.join(work, "flood")
    run_dir = os.path.join(flood_dir, "run")
    os.makedirs(run_dir)
    counter = os.path.join(flood_dir, "c1-r86-refusal-records.py")
    controls = os.path.join(flood_dir, "c1-cases-r86.json")
    carried = os.path.join(flood_dir, "c1-cases-r85.json")
    write_bytes(counter, git_bytes(repo, measured, C1_COUNTER))
    controls_bytes = git_bytes(repo, measured, C1_CONTROLS)
    if sha256(controls_bytes) != m_ctl.group(1):
        raise Setup("r86 controls at %s differ from the receipt sha256" % measured)
    write_bytes(controls, controls_bytes)
    write_bytes(carried, git_bytes(repo, measured, C1_CARRIED))
    argv = [sys.executable, "-I", counter, "--repo", repo, "--rev", measured,
            "--base-rev", base, "--controls", controls, "--carried", carried,
            "--scratch-root", run_dir]
    env = git_env({"TMPDIR": flood_dir, "PYTHONDONTWRITEBYTECODE": "1"})
    try:
        proc = subprocess.run(argv, cwd=flood_dir, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=3600)
    except subprocess.TimeoutExpired:
        raise Setup("r86 C1 re-run timed out")
    out = proc.stdout.decode("utf-8", "replace")
    match = re.search(r"^MADO_R86_REFUSALS: cases=(\d+) .*?\bflooding=(\d+)/(\d+) "
                      r"held_flooding=(\d+)/(\d+) verdict=", out, re.M)
    if not match:
        raise Setup("r86 C1 re-run printed no refusals line (rc=%d)" % proc.returncode)
    return "flooding %s/%s; held %s/%s" % (match.group(2), match.group(3),
                                            match.group(4), match.group(5))


def evaluate(repo, rev, figures_path, scratch, expect_sha, flood_fn):
    full = resolve_rev(repo, rev)
    raw = git_bytes(repo, full, figures_path)
    fsha = sha256(raw)
    if expect_sha is not None and expect_sha.lower() != fsha:
        raise Setup("figure file sha256 %s differs from expected %s" % (fsha, expect_sha))
    figures = load_figures(raw)
    for fig in figures:
        for loc in fig["stated_at"]:
            text = git_bytes(repo, full, loc["path"]).decode("utf-8", "replace")
            if loc["text"] not in text:
                raise Setup("stated text absent from %s at %s (figure %s): %r"
                            % (loc["path"], full, fig["id"], loc["text"]))
    corrections = [git_bytes(repo, full, path).decode("utf-8", "replace") for path in CORRECTION_FILES]
    derive = {"held_rule_witness": derive_held_rule, "flood_pair": flood_fn}
    counter_sha = sha256(open(os.path.abspath(__file__), "rb").read())
    work = tempfile.mkdtemp(prefix="c2-r87-", dir=scratch)
    lines = []
    reproduced = reconciled = 0
    try:
        for fig in figures:
            derived = derive[fig["kind"]](repo, full, work)
            ok = derived == fig["stated"]
            rec = ok or reconciles(fig["id"], derived, corrections)
            reproduced += int(ok)
            reconciled += int(rec)
            lines.append("MADO_FIGURE: id=%s stated=%r rederived=%r reproduced=%s reconciled=%s"
                         % (fig["id"], fig["stated"], derived, "yes" if ok else "no",
                            "yes" if rec else "no"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    n = len(figures)
    met = n == 2 and reconciled == n
    lines.append("MADO_FIGURES: %s rev=%s n=%d reproduced=%d reconciled=%d score=%.4f "
                 "figures_sha256=%s counter_sha256=%s"
                 % ("TARGET_MET" if met else "TARGET_MISSED", full, n, reproduced, reconciled,
                    10.0 * reconciled / n, fsha, counter_sha))
    return (0 if met else 1), lines


FIG_DOC = {
    "schema": FIGURE_SCHEMA,
    "figures": [
        {"id": "F1_held_rule_witness_r86", "kind": "held_rule_witness", "stated": "0/1",
         "stated_at": [
             {"path": CORRECTION_FILES[0], "text": "held_rule_new_case=0/1"},
             {"path": "SCORECARD.md", "text": "held rule 0/1 on the new anchor witness"}]},
        {"id": "F2_flood_r86", "kind": "flood_pair", "stated": "flooding 48/75; held 75/75",
         "stated_at": [{"path": "SCORECARD.md", "text": "flooding 48/75 vs held 75/75"}]},
    ],
}
FIGURES_PATH = ".ufo/waves/round-87/controls/r86-figures-r87.json"
STUB_R85 = "def case_correct(case, rc, stdout):\n    return rc == 0 and stdout.strip() == case['frozen']\n"
GOOD_F1 = ("\n## Correction (round 87): F1_held_rule_witness_r86\n\n"
           "Re-derived by the held r85 counter as 1/1; the r86 0/1 came from the model.\n")


def stub_flood(repo, rev, work):
    return "flooding 48/75; held 75/75"


def run_git(directory, *args):
    proc = subprocess.run(["git", "-C", directory] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, env=git_env())
    if proc.returncode != 0:
        raise Setup("fixture git %s failed: %s" % (args[0], proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8", "replace").strip()


def make_repo(root, name, files):
    directory = os.path.join(root, name)
    os.makedirs(directory)
    run_git(directory, "init", "-q")
    top = run_git(directory, "rev-parse", "--show-toplevel")
    if os.path.realpath(top) != os.path.realpath(directory):
        raise Setup("fixture toplevel %s is not %s" % (top, directory))
    for path, content in files.items():
        full = os.path.join(directory, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        write_bytes(full, content.encode("utf-8"))
    run_git(directory, "add", "-A")
    run_git(directory, "-c", "user.name=mado-selftest", "-c", "user.email=selftest@invalid",
            "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture")
    return directory, run_git(directory, "rev-parse", "HEAD")


def fixture(root, name, corpus_extra="", score_extra="", f2_text=True, extra=None):
    files = {
        CORRECTION_FILES[0]: "# r86 corpus\n\nheld_rule_new_case=0/1\n" + corpus_extra,
        "SCORECARD.md": "# Scorecard\n\nheld rule 0/1 on the new anchor witness\n"
                        + ("flooding 48/75 vs held 75/75\n" if f2_text else "") + score_extra,
        FIGURES_PATH: json.dumps(FIG_DOC, indent=1) + "\n",
        R85_COUNTER: STUB_R85,
        R86_CASES: json.dumps({"cases": [{"name": HELD_CASE, "frozen": "0"}]}) + "\n",
    }
    files.update(extra or {})
    return make_repo(root, name, files)


def selftest(scratch):
    root = tempfile.mkdtemp(prefix="c2-r87-selftest-", dir=scratch)
    results = []

    def check(label, cond):
        results.append((label, bool(cond)))

    def attempt(name, flood=stub_flood, expect=None, f2_text=True, corpus_extra="", score_extra="",
                extra=None):
        repo, rev = fixture(root, name, corpus_extra, score_extra, f2_text, extra)
        try:
            return evaluate(repo, rev, FIGURES_PATH, root, expect, flood)
        except Setup as exc:
            return 2, ["MADO_FIGURES: ERROR (stage=setup %s)" % exc]

    try:
        f1 = "F1_held_rule_witness_r86"
        check("correction block with id and re-derived value reconciles",
              reconciles(f1, "1/1", [GOOD_F1]))
        check("bare correction heading does not reconcile",
              not reconciles(f1, "1/1", ["## Correction (round 87)\n\nnone\n"]))
        check("correction with wrong value does not reconcile",
              not reconciles(f1, "1/1", ["## Correction (round 87): %s\n\nstill 0/1\n" % f1]))
        check("correction naming only the id does not reconcile",
              not reconciles(f1, "1/1", ["## Correction (round 87): %s\n\nwrong.\n" % f1]))
        check("correction block ends at the next same-level heading",
              not reconciles(f1, "1/1", ["## Correction (round 87)\n\n## Later\n\n%s 1/1\n" % f1]))
        check("value match is token-bounded (21/12 is not 1/1)",
              not reconciles(f1, "1/1", ["## Correction (round 87): %s\n\n21/12\n" % f1]))

        code, lines = attempt("good", corpus_extra=GOOD_F1)
        check("both figures reconciled -> exit 0 TARGET_MET",
              code == 0 and lines[-1].startswith("MADO_FIGURES: TARGET_MET ")
              and "reconciled=2" in lines[-1] and "n=2" in lines[-1])
        code, lines = attempt("base")
        check("no correction for F1 -> exit 1 TARGET_MISSED score=5.0000",
              code == 1 and "TARGET_MISSED" in lines[-1] and "score=5.0000" in lines[-1])
        code, lines = attempt("bare", corpus_extra="\n## Correction (round 87)\n\nSee the held counter.\n")
        check("bare heading in corpus -> exit 1", code == 1 and "TARGET_MISSED" in lines[-1])
        code, _ = attempt("wrong", corpus_extra="\n## Correction (round 87): %s\n\nThe held rule scores 0/1.\n" % f1)
        check("wrong-value correction -> exit 1", code == 1)
        code, _ = attempt("other", extra={"notes/other.md": GOOD_F1})
        check("correction in another file -> exit 1", code == 1)
        code, lines = attempt("absent", f2_text=False)
        check("absent stated text -> exit 2 setup error",
              code == 2 and lines[-1].startswith("MADO_FIGURES: ERROR (stage=setup"))
        code, _ = attempt("sha", expect="0" * 64)
        check("figure sha256 mismatch -> exit 2", code == 2)
        code, _ = attempt("scope", corpus_extra="\n## Correction (round 87)\n\n## Later\n\n%s 1/1\n" % f1)
        check("heading scope: text after a same-level heading is ignored -> exit 1", code == 1)
        code, lines = attempt("f2fix", flood=lambda r, v, w: "flooding 47/75; held 75/75",
                              corpus_extra=GOOD_F1,
                              score_extra="\n## Correction (round 87): F2_flood_r86\n\n"
                                          "Re-derived flooding 47/75; held 75/75.\n")
        check("F2 corrected in SCORECARD -> exit 0 with reproduced=0 reconciled=2",
              code == 0 and "reproduced=0" in lines[-1] and "reconciled=2" in lines[-1])

        failed = [label for label, ok in results if not ok]
        for label in failed:
            print("MADO_FIGURES_SELFTEST_FAIL: %s" % label)
        print("MADO_FIGURES_SELFTEST: %d/%d" % (len(results) - len(failed), len(results)))
        return 0 if not failed else 1
    except Setup as exc:
        print("MADO_FIGURES_SELFTEST: ERROR (stage=setup %s)" % exc)
        return 2
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main(argv):
    ap = argparse.ArgumentParser(description="mado r87 C2 control-figure fidelity counter")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--figures", help="repo-relative path of the figure file, read at REV")
    ap.add_argument("--scratch-root")
    ap.add_argument("--expect-figures-sha256")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.scratch_root is None:
        print("MADO_FIGURES: ERROR (stage=setup usage: --scratch-root required)")
        return 2
    try:
        os.makedirs(args.scratch_root, exist_ok=True)
        scratch = os.path.abspath(args.scratch_root)
        if args.selftest:
            return selftest(scratch)
        if not (args.repo and args.rev and args.figures):
            raise Setup("usage: --repo, --rev and --figures are required")
        code, lines = evaluate(os.path.abspath(args.repo), args.rev, args.figures, scratch,
                               args.expect_figures_sha256, derive_flood)
        for line in lines:
            print(line)
        return code
    except Setup as exc:
        print("MADO_FIGURES: ERROR (stage=setup %s)" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
