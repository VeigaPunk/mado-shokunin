#!/usr/bin/env python3
"""mado index-completeness gate (round 30, claim C3 / capability row;
repaired under the w1 RevC1Fence/MutC3Gate/RevC3Gate findings — see the
round-30 erratum in SCORECARD.md and corpus/lessons/round-30.md; hardened
further under the round-31 routed queue).

Navigation-completeness gate only: it checks that every admitted
`corpus/knowledge/*.md` note has exactly one index row in `corpus/README.md`.
The row set is byte-level rows matching the fence's literal regex
``^\\| `knowledge/<name>.md` `` — column-0 pipe, one literal space, backticked
name — the same semantics as the SCORECARD.md fleet-round-1 counting
command (source row S185).  Like the fence it does not require the row to
sit inside the coverage-map table (table context is unenforced in both;
row *fidelity* is `check-index-rows.py`'s job, not this gate's).
This gate says nothing about note truth, freshness, or the semantic
accuracy of the row text; an index row is a route, not a verdict.

Reads: `corpus/knowledge/` and `corpus/README.md` at a git revision
(`--rev`, resolved once via `git rev-parse --verify --end-of-options`
then read as `<sha>:path` — a crafted rev can never reach a `git show`
write path) or on a plain filesystem tree (`--root DIR`; regular files
only — symlinked or non-regular members are REFUSED, and `corpus/` or
the root itself being a symlink to an outside tree is refused too:
realpath containment on ancestors).  `--rev` counts blob entries only
(mode/space/non-ASCII names handled by `core.quotepath=off` + NUL
records); a symlinked note IS a blob at a rev — counted, fence parity —
while `--root` refuses it.  A missing or empty `corpus/knowledge` is a
setup error in both modes — the fence is undefined on an empty note set,
so this gate invents no clean state.
Writes: nothing; stdout only (SETUP_ERROR goes to stderr).  `--selftest`
writes ephemeral fixtures inside a private temporary directory it
removes on exit and runs a copy of itself as a child process.

Exit: 0 complete; 1 gap (missing/dangling/duplicate) or refused input;
2 setup error.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter

ROW_RE = re.compile(r"^\| `knowledge/([^`]+\.md)`", re.M)


def _git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", repo, *args], text=True, stderr=subprocess.STDOUT
    )


def load_rev(repo, rev):
    try:
        sha = _git(
            repo, "rev-parse", "--verify", "--end-of-options",
            rev + "^{commit}",
        ).strip()
        names = _git(
            repo, "-c", "core.quotepath=off", "ls-tree", "-z",
            "--format=%(objecttype) %(path)",
            sha + ":corpus/knowledge",
        )
        readme = _git(repo, "show", sha + ":corpus/README.md")
    except subprocess.CalledProcessError as exc:
        print(f"SETUP_ERROR: {exc.output.strip()}", file=sys.stderr)
        sys.exit(2)
    notes = {
        rec.split(" ", 1)[1]
        for rec in names.split("\0")
        if rec.startswith("blob ") and rec.split(" ", 1)[1].endswith(".md")
    }
    return notes, readme


def _refuse(path):
    print(f"REFUSED: non-regular member {path}")
    sys.exit(1)



def load_root(root):
    rroot = os.path.realpath(root)
    for cand in ("corpus",):
        ap = os.path.join(root, cand)
        if os.path.islink(ap):
            _refuse(ap)
        rp = os.path.realpath(ap)
        if os.path.commonpath([rroot, rp]) != rroot:
            _refuse(ap)
    kdir = os.path.join(root, "corpus", "knowledge")
    rpath = os.path.join(root, "corpus", "README.md")
    for path in (kdir, rpath):
        if os.path.islink(path):
            _refuse(path)
    if not os.path.isfile(rpath):
        print(f"SETUP_ERROR: {rpath} not a regular file", file=sys.stderr)
        sys.exit(2)
    if not os.path.isdir(kdir):
        print(f"SETUP_ERROR: {kdir} not a directory", file=sys.stderr)
        sys.exit(2)
    notes = set()
    for name in sorted(os.listdir(kdir)):
        fpath = os.path.join(kdir, name)
        if os.path.islink(fpath) or not os.path.isfile(fpath):
            _refuse(fpath)
        if name.endswith(".md"):
            notes.add(name)
    with open(rpath, encoding="utf-8") as fh:
        readme = fh.read()
    return notes, readme




def evaluate(notes, readme):
    counts = Counter(ROW_RE.findall(readme))
    missing = sorted(notes - set(counts))
    dangling = []
    duplicates = sorted(p for p, n in counts.items() if n != 1)
    covered = sum(1 for p in notes if counts.get(p) == 1)
    return covered, missing, dangling, duplicates


def report(tag, notes, readme):
    if not notes:
        # The fence is undefined on an empty note set (ZeroDivisionError);
        # report no invented clean state — a 0-note tree is a setup error.
        print(f"SETUP_ERROR: empty note set ({tag})", file=sys.stderr)
        return 2
    covered, missing, dangling, duplicates = evaluate(notes, readme)
    total = len(notes)
    score = 10 * covered / total
    print(
        f"MADO_INDEX: {tag} indexed={covered}/{total} "
        f"missing={len(missing)} dangling={len(dangling)} "
        f"duplicates={len(duplicates)} coverage={score:.4f}/10"
    )
    for kind, paths in (
        ("missing", missing),
        ("dangling", dangling),
        ("duplicate", duplicates),
    ):
        for path in paths:
            print(f"{kind}: knowledge/{path}")
    return 0 if not (missing or dangling or duplicates) else 1


def _run(tool, *args):
    return subprocess.run(
        [sys.executable, tool, *args],
        capture_output=True,
        text=True,
    )


def _write_tree(root, note_names, row_names, symlink_knowledge=False):
    kdir = os.path.join(root, "corpus", "knowledge")
    os.makedirs(kdir, exist_ok=True)
    for name in note_names:
        with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
            fh.write(f"# {name}\n")
    rows = "".join(f"| `knowledge/{n}` | holds | source |\n" for n in row_names)
    with open(os.path.join(root, "corpus", "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# corpus\n\n| Note | Holds | Sources |\n|---|---|---|\n" + rows)


def selftest():
    tool = os.path.abspath(__file__)
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    with tempfile.TemporaryDirectory(prefix="mado-index-") as tmp:
        # Case 1: complete tree — 3 notes, 3 rows.
        t1 = os.path.join(tmp, "complete")
        _write_tree(t1, ["a.md", "b.md", "c.md"], ["a.md", "b.md", "c.md"])
        r = _run(tool, "--root", t1)
        check(
            "complete exits 0 with indexed=3/3",
            r.returncode == 0 and "indexed=3/3" in r.stdout,
        )

        # Case 2: missing row — note has no index row.
        t2 = os.path.join(tmp, "missing")
        _write_tree(t2, ["a.md", "b.md"], ["a.md"])
        r = _run(tool, "--root", t2)
        check(
            "missing row exits 1 and names the note",
            r.returncode == 1 and "missing: knowledge/b.md" in r.stdout,
        )

        # Case 3: dangling row — index names a nonexistent note.
        t3 = os.path.join(tmp, "dangling")
        _write_tree(t3, ["a.md"], ["a.md", "ghost.md"])
        r = _run(tool, "--root", t3)

        # Case 4: duplicate row — one note indexed twice.
        t4 = os.path.join(tmp, "duplicate")
        _write_tree(t4, ["a.md"], ["a.md", "a.md"])
        r = _run(tool, "--root", t4)
        check(
            "duplicate row exits 1 and names the note",
            r.returncode == 1 and "duplicate: knowledge/a.md" in r.stdout,
        )

        # Case 5: symlinked member is refused, not followed.
        t5 = os.path.join(tmp, "symlink")
        os.makedirs(os.path.join(t5, "corpus"), exist_ok=True)
        os.symlink("/nonexistent", os.path.join(t5, "corpus", "knowledge"))
        with open(os.path.join(t5, "corpus", "README.md"), "w") as fh:
            fh.write("x\n")
        r = _run(tool, "--root", t5)
        check(
            "symlink member refused with exit 1",
            r.returncode == 1 and "REFUSED" in r.stdout,
        )

        # Case 6: no corpus/knowledge dir — a wrong root is a setup error,
        # never a clean 0/0 (the fence dies on an empty note set too).
        t6 = os.path.join(tmp, "noroot")
        os.makedirs(os.path.join(t6, "corpus"), exist_ok=True)
        with open(os.path.join(t6, "corpus", "README.md"), "w") as fh:
            fh.write("x\n")
        r = _run(tool, "--root", t6)
        check(
            "missing knowledge dir is SETUP_ERROR exit 2",
            r.returncode == 2 and "SETUP_ERROR" in r.stderr + r.stdout,
        )

        # Case 7: the row grammar is the fence's literal `^\\| ` —
        # no-space, double-space, tab and indented rows are NOT counted.
        t7 = os.path.join(tmp, "rowforms")
        _write_tree(t7, ["a.md", "b.md", "c.md", "d.md"], [])
        with open(os.path.join(t7, "corpus", "README.md"), "a") as fh:
            fh.write("|`knowledge/a.md` | h |\n")          # no space: not a row
            fh.write("|  `knowledge/b.md` | h |\n")         # two spaces: not a row
            fh.write("|\t`knowledge/c.md` | h |\n")          # tab: not a row
            fh.write("  | `knowledge/d.md` | h |\n")          # indented: not a row
        r = _run(tool, "--root", t7)
        check(
            "non-fence row forms count as missing, exit 1",
            r.returncode == 1 and "missing=4" in r.stdout,
        )

        # Case 8: a symlinked note is REFUSED (MutC3Gate M3a coverage).
        t8 = os.path.join(tmp, "linksym")
        _write_tree(t8, ["a.md"], ["a.md"])
        os.symlink(
            os.path.join(t8, "corpus", "knowledge", "a.md"),
            os.path.join(t8, "corpus", "knowledge", "link.md"),
        )
        r = _run(tool, "--root", t8)
        check(
            "symlinked note refused with exit 1",
            r.returncode == 1 and "REFUSED" in r.stdout,
        )

        # Case 9: --rev mode reads non-ASCII and space-bearing note
        # names correctly (quotepath=off + NUL records; RevC1Fence S3).
        import shutil
        t9 = os.path.join(tmp, "gitfixture")
        if shutil.which("git"):
            kd = os.path.join(t9, "corpus", "knowledge")
            os.makedirs(kd)
            for name in ("café.md", "a b.md"):
                with open(os.path.join(kd, name), "w", encoding="utf-8") as fh:
                    fh.write(f"# {name}\n")
            rows = "".join(f"| `knowledge/{n}` | h |\n" for n in ("café.md", "a b.md"))
            with open(os.path.join(t9, "corpus", "README.md"), "w", encoding="utf-8") as fh:
                fh.write(rows)
            env = dict(
                os.environ,
                GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
            )
            for cmd in (
                ("git", "init", "-q", t9),
                ("git", "-C", t9, "add", "-A"),
                ("git", "-C", t9, "commit", "-qm", "t"),
            ):
                subprocess.run(cmd, check=True, capture_output=True, env=env)
            r = _run(tool, "--rev", "HEAD", "--repo", t9)
            check(
                "non-ASCII + space names indexed at --rev, exit 0",
                r.returncode == 0 and "indexed=2/2" in r.stdout,
            )
        # Case 10: a crafted --rev is rejected before any git lookup can
        # turn it into a `git show --output=` write path (SentScope F5;
        # RevC3Gate L1).
        if shutil.which("git"):
            r = _run(tool, "--rev=--output=/tmp/x", "--repo", t9)
            check(
                "option-shaped --rev is SETUP_ERROR exit 2, no write",
                r.returncode == 2 and not os.path.exists("/tmp/x:corpus"),
            )

        # Case 11: --root refuses a symlinked corpus ancestor instead of
        # certifying the outside tree it resolves to (SentScope F2).
        t11 = os.path.join(tmp, "ancestor")
        foreign = os.path.join(tmp, "foreign")
        _write_tree(foreign, ["a.md"], ["a.md"])
        os.makedirs(t11, exist_ok=True)
        os.symlink(
            os.path.join(foreign, "corpus"), os.path.join(t11, "corpus")
        )
        r = _run(tool, "--root", t11)
        check(
            "symlinked corpus ancestor refused with exit 1",
            r.returncode == 1 and "REFUSED" in r.stdout,
        )

        # Case 12: --repo has no meaning under --root; silently ignoring
        # it was RevC3Gate L4. Both must not combine.
        r = _run(tool, "--root", t11, "--repo", "/nonexistent")
        check(
            "--repo with --root is SETUP_ERROR exit 2",
            r.returncode == 2 and "SETUP_ERROR" in r.stderr,
        )

    failed = [n for n, ok in checks if not ok]
    passed = len(checks) - len(failed)
    print(f"MADO_INDEX_SELFTEST: {passed}/{len(checks)} assertions passed")
    for n in failed:
        print(f"FAILED: {n}")
    return 0 if not failed else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rev", help="git revision to read the tree at")
    ap.add_argument("--repo", default=".", help="git repo for --rev mode")
    ap.add_argument("--root", help="filesystem tree root instead of a revision")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.root and (args.rev or args.repo != "."):
        print("SETUP_ERROR: --root takes neither --rev nor --repo", file=sys.stderr)
        return 2
    if args.root:
        notes, readme = load_root(args.root)
        return report(f"root={args.root}", notes, readme)
    if not args.rev:
        # No silent default: a bare invocation must name its revision —
        # `rev-parse master` measures the bookmark, not the lane tip
        # (RevC3Gate H1; RevC1Fence S5). Explicit rev only.
        print("SETUP_ERROR: --rev or --root is required", file=sys.stderr)
        return 2
    notes, readme = load_rev(args.repo, args.rev)
    return report(f"rev={args.rev}", notes, readme)


if __name__ == "__main__":
    raise SystemExit(main())
