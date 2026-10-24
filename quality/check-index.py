#!/usr/bin/env python3
"""mado index-completeness gate (round 30, claim C3 / capability row).

Navigation-completeness gate only: it checks that every admitted
`corpus/knowledge/*.md` note has exactly one index row in `corpus/README.md`.
The row set is the coverage-map table cells ``| `knowledge/<name>.md` `` — the
same semantics as the SCORECARD.md fleet-round-1 counting command (source row
S185).  This gate says nothing about note truth, freshness, or the semantic
accuracy of the row text; an index row is a route, not a verdict.

Reads: `corpus/knowledge/` and `corpus/README.md` at a git revision (`--rev`,
via `git ls-tree`/`git show` under `--repo`) or on a plain filesystem tree
(`--root DIR`; regular files only — symlinked or non-regular members are
REFUSED).  Writes: nothing; stdout only.  `--selftest` writes ephemeral
fixtures inside a private temporary directory it removes on exit and runs a
copy of itself as a child process.

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

ROW_RE = re.compile(r"^\|\s*`knowledge/([^`]+\.md)`", re.M)


def _git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", repo, *args], text=True, stderr=subprocess.STDOUT
    )


def load_rev(repo, rev):
    try:
        names = _git(repo, "ls-tree", "--name-only", rev + ":corpus/knowledge")
        readme = _git(repo, "show", rev + ":corpus/README.md")
    except subprocess.CalledProcessError as exc:
        print(f"SETUP_ERROR: {exc.output.strip()}", file=sys.stderr)
        sys.exit(2)
    notes = {n for n in names.split() if n.endswith(".md")}
    return notes, readme


def _refuse(path):
    print(f"REFUSED: non-regular member {path}")
    sys.exit(1)


def load_root(root):
    kdir = os.path.join(root, "corpus", "knowledge")
    rpath = os.path.join(root, "corpus", "README.md")
    for path in (kdir, rpath):
        if os.path.islink(path):
            _refuse(path)
    if not os.path.isfile(rpath):
        print(f"SETUP_ERROR: {rpath} not a regular file", file=sys.stderr)
        sys.exit(2)
    notes = set()
    if os.path.isdir(kdir):
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
    dangling = sorted(set(counts) - notes)
    duplicates = sorted(p for p, n in counts.items() if n != 1)
    covered = sum(1 for p in notes if counts.get(p) == 1)
    return covered, missing, dangling, duplicates


def report(tag, notes, readme):
    covered, missing, dangling, duplicates = evaluate(notes, readme)
    total = len(notes)
    score = (10 * covered / total) if total else 0.0
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
        check(
            "dangling row exits 1 and names the row",
            r.returncode == 1 and "dangling: knowledge/ghost.md" in r.stdout,
        )

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

        # Case 6: empty knowledge dir is a 0-note clean state, not an error.
        t6 = os.path.join(tmp, "empty")
        _write_tree(t6, [], [])
        r = _run(tool, "--root", t6)
        check(
            "empty tree exits 0 with indexed=0/0",
            r.returncode == 0 and "indexed=0/0" in r.stdout,
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
    if args.root and args.rev:
        print("SETUP_ERROR: choose --rev or --root, not both", file=sys.stderr)
        return 2
    if args.root:
        notes, readme = load_root(args.root)
        return report(f"root={args.root}", notes, readme)
    rev = args.rev
    if not rev:
        rev = _git(args.repo, "rev-parse", "master").strip()
    notes, readme = load_rev(args.repo, rev)
    return report(f"rev={rev}", notes, readme)


if __name__ == "__main__":
    raise SystemExit(main())
