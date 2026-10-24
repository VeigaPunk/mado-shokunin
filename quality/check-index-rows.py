#!/usr/bin/env python3
"""mado index-row fidelity gate (round 31, claim C1).

The completeness gate (`quality/check-index.py`, S185 fence semantics)
certifies that every `corpus/knowledge/*.md` note has exactly one index
row — it reads only the row's first cell, so it cannot see where the row
sits or what the row carries.  This gate reads the rest of the row, per
the round-30 w1 routed defects (CritPredicates A1–A4: empty-cell,
comment-hidden and code-block rows all satisfy the completeness fence;
RevC1Fence S6: "coverage-map table cells" unenforced; RevengerPrior D2:
the `animation-table-r26` row shipped no Sources cell; ScribeRowAccuracy
F1: a Holds cell overclaimed its note).

Checks (each row is a fence row — a line matching the fence's literal
``^\\| `knowledge/<name>.md` `` — inside the coverage-map table, the row
block following the `|Note|Holds|Sources|` header):

ERROR `row-outside-map`      a fence-shaped row anywhere else in the file
                             (second table, comment, fenced code block)
ERROR `row-cells`            a row must carry >=3 cells (Note, Holds,
                             Sources) with cells 2 and 3 non-empty
ERROR `cited-s-undefined`    every `S###` token in the row must resolve to
                             a SOURCES.md row id at REV
ERROR `cited-path-missing`   every backticked slash-path in the Sources
                             cell must exist at REV (`--rev`) or on the
                             filesystem (`--root`); `.md`-targets also
                             exist-check
WARN  `holds-no-overlap`     Holds cell shares no >=5-word sequence with
                             the note's own bytes (row may not quote the
                             note; semantic accuracy stays a review item)

Reads: `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*.md`
at a git revision (`--rev`, via `git show`/`git ls-tree` under `--repo`)
or on a plain filesystem tree (`--root DIR`; regular files only —
symlinked or non-regular members are REFUSED, ancestors realpath-checked).
Writes: nothing; stdout only.  `--selftest` runs a copy of itself inside
a private temporary directory it removes on exit.

Exit: 0 no ERROR finding; 1 >=1 ERROR finding or refused input;
2 setup error.  WARN lines never affect the exit code.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

ROW_RE = re.compile(r"^\| `knowledge/([^`]+\.md)`", re.M)
SRE = re.compile(r"\bS\d{3}\b")
BT_RE = re.compile(r"`([^`]+)`")
WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}")


def _git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", repo, *args], text=True, stderr=subprocess.STDOUT
    )


def load_rev(repo, rev):
    """Read README, SOURCES and the knowledge dir listing at REV."""
    import fnmatch

    try:
        sha = _git(
            repo, "rev-parse", "--verify", "--end-of-options",
            rev + "^{commit}",
        ).strip()
        readme = _git(repo, "show", f"{sha}:corpus/README.md")
        sources = _git(repo, "show", f"{sha}:corpus/SOURCES.md")
        names = _git(
            repo, "-c", "core.quotepath=off", "ls-tree", "-z",
            "--format=%(objecttype) %(path)",
            f"{sha}:corpus/knowledge",
        )
    except subprocess.CalledProcessError as exc:
        print(f"SETUP_ERROR: {exc.output.strip()}", file=sys.stderr)
        sys.exit(2)

    def note_text(name):
        try:
            return _git(repo, "show", f"{sha}:corpus/knowledge/{name}")
        except subprocess.CalledProcessError:
            return None

    def exists(path):
        try:
            _git(repo, "cat-file", "-e", f"{sha}:{path}")
            return True
        except subprocess.CalledProcessError:
            return False

    def exists_glob(pattern):
        try:
            out = _git(
                repo, "-c", "core.quotepath=off", "ls-tree", "-r", "-z",
                "--name-only", "--format=%(path)", sha, "--",
                os.path.dirname(pattern) or ".",
            )
        except subprocess.CalledProcessError:
            return False
        rx = pattern.replace("#", "[0-9]")
        return any(fnmatch.fnmatch(p, rx) for p in out.split("\0") if p)

    notes = {
        rec.split(" ", 1)[1]
        for rec in names.split("\0")
        if rec.startswith("blob ") and rec.split(" ", 1)[1].endswith(".md")
    }
    return readme, sources, notes, note_text, exists, exists_glob, f"rev={rev}"


def _refuse(path):
    print(f"MADO_INDEX_ROWS: REFUSED: non-regular member {path}")
    sys.exit(1)


def load_root(root):
    rroot = os.path.realpath(root)
    for cand in ("corpus", os.path.join("corpus", "knowledge")):
        ap = os.path.join(root, cand)
        if os.path.islink(ap):
            _refuse(ap)
        rp = os.path.realpath(ap)
        try:
            if os.path.commonpath([rroot, rp]) != rroot:
                _refuse(ap)
        except ValueError:
            _refuse(ap)
    rpath = os.path.join(root, "corpus", "README.md")
    spath = os.path.join(root, "corpus", "SOURCES.md")
    kdir = os.path.join(root, "corpus", "knowledge")
    for path in (rpath, spath):
        if os.path.islink(path) or not os.path.isfile(path):
            print(f"SETUP_ERROR: {path} not a regular file", file=sys.stderr)
            sys.exit(2)
    if os.path.islink(kdir) or not os.path.isdir(kdir):
        print(f"SETUP_ERROR: {kdir} not a directory", file=sys.stderr)
        sys.exit(2)
    for name in sorted(os.listdir(kdir)):
        fpath = os.path.join(kdir, name)
        if os.path.islink(fpath) or not os.path.isfile(fpath):
            _refuse(fpath)
    with open(rpath, encoding="utf-8") as fh:
        readme = fh.read()
    with open(spath, encoding="utf-8") as fh:
        sources = fh.read()
    notes = {n for n in os.listdir(kdir) if n.endswith(".md")}

    def note_text(name):
        p = os.path.join(kdir, name)
        if not os.path.isfile(p):
            return None
        with open(p, encoding="utf-8") as fh:
            return fh.read()

    def exists(path):
        return os.path.exists(os.path.join(root, path))

    def exists_glob(pattern):
        import fnmatch
        rx = pattern.replace("#", "[0-9]")
        return bool(_glob.glob(os.path.join(root, rx)))

    return readme, sources, notes, note_text, exists, exists_glob, f"root={root}"

RP_RE = re.compile(
    # lane-repo-relative artifact paths only; a sibling-repo prefix
    # (`tameshi-shokunin/tools/…`) or host path is not a lane citation.
    r"(?<![\w-]/)(?:\.ufo|tools|quality|corpus|scripts|templates)/[\w./#{}?*\[\]-]+"
)
GLOB_CHARS = re.compile(r"[*?{}\[\]#]")
WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}")
import glob as _glob


def table_region(readme):
    """Return (start, end) line span of the coverage-map table body —
    the rows following the `|Note|Holds|Sources|` header + separator."""
    lines = readme.splitlines()
    for i, line in enumerate(lines):
        norm = line.replace(" ", "")
        if norm.startswith("|Note|Holds|Sources|"):
            j = i + 1
            if j < len(lines) and re.match(r"^\|[\s|:-]+\|?\s*$", lines[j]):
                j += 1
            start = j
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            return start, j
    return None


def source_ids(sources):
    return set(re.findall(r"^\|\s*(S\d{3})\s*\|", sources, re.M))


def overlap(note, cell):
    """True iff the Holds cell plausibly quotes the note: a >=5-word
    sequence of note words appears in the cell, or >=5 distinct content
    words are shared (loose fallback; semantic accuracy stays review)."""
    nwords = WORD_RE.findall(note.lower())
    cwords = set(WORD_RE.findall(cell.lower()))
    if not nwords:
        return True
    hay = " ".join(WORD_RE.findall(cell.lower()))
    for i in range(len(nwords) - 4):
        if " ".join(nwords[i:i + 5]) in hay:
            return True
    shared = [w for w in nwords if w in cwords]
    return len(set(shared)) >= 5


def evaluate(readme, sources, notes, note_text, exists, exists_glob):
    errors, warns = [], []
    region = table_region(readme)
    lines = readme.splitlines()
    rows = [(i, m.group(1)) for i, l in enumerate(lines)
            for m in [ROW_RE.match(l)] if m]
    if region is None:
        errors.append("no-coverage-map-table: `|Note|Holds|Sources|` header absent")
        return errors, warns
    for i, name in rows:
        if not (region[0] <= i < region[1]):
            errors.append(f"row-outside-map: knowledge/{name} at line {i + 1}")
    ids = source_ids(sources)
    for i, name in rows:
        if not (region[0] <= i < region[1]):
            continue
        line = lines[i]
        cells = [c.strip() for c in line.split("|")]
        # leading/trailing pipes produce empty edge cells
        inner = cells[1:-1] if len(cells) >= 2 else cells
        if len(inner) < 3 or not inner[1].strip() or not inner[2].strip():
            errors.append(
                f"row-cells: knowledge/{name} at line {i + 1} "
                f"carries {len(inner)} cells (need 3 non-empty)"
            )
            continue
        holds, src = inner[1], inner[2]
        for sid in SRE.findall(line):
            if sid not in ids:
                errors.append(f"cited-s-undefined: {sid} in row knowledge/{name}")
        for tick in BT_RE.findall(src):
            # Only repo-relative artifact paths are verifiable: commands,
            # host paths (`/`, `~`) and bare words are skipped.  Glob
            # tokens (`*?[`) and `#` placeholders match against the named
            # directory's member list at REV (RevengerPrior check 4/6).
            for p in RP_RE.findall(tick):
                if GLOB_CHARS.search(p):
                    if not exists_glob(p):
                        warns.append(
                            f"cited-glob-nomatch: `{p}` in row knowledge/{name}"
                        )
                elif not exists(p):
                    errors.append(
                        f"cited-path-missing: `{p}` in row knowledge/{name}"
                    )
        nt = note_text(name)
        if nt is None:
            continue  # dangling row: the completeness gate owns this finding
        if not overlap(nt, holds):
            warns.append(
                f"holds-no-overlap: row knowledge/{name} at line {i + 1}"
            )
    return errors, warns


def report(tag, readme, sources, notes, note_text, exists, exists_glob):
    if not notes:
        print(f"SETUP_ERROR: empty note set ({tag})", file=sys.stderr)
        return 2
    errors, warns = evaluate(readme, sources, notes, note_text, exists, exists_glob)
    nrows = len(ROW_RE.findall(readme))
    print(
        f"MADO_INDEX_ROWS: {tag} rows={nrows} errors={len(errors)} "
        f"warns={len(warns)}"
    )
    for e in errors:
        print(f"ERROR {e}")
    for w in warns:
        print(f"WARN {w}")
    return 1 if errors else 0


def _run(tool, *args):
    return subprocess.run(
        [sys.executable, tool, *args], capture_output=True, text=True
    )


def _write_tree(root, note_names, rows, sources_rows=""):
    kdir = os.path.join(root, "corpus", "knowledge")
    os.makedirs(kdir, exist_ok=True)
    for name in note_names:
        with open(os.path.join(kdir, name), "w", encoding="utf-8") as fh:
            fh.write(f"# {name}\n\nThe quick brown fox jumps over the lazy dog.\n")
    with open(os.path.join(root, "corpus", "README.md"), "w", encoding="utf-8") as fh:
        fh.write(
            "# corpus\n\n|Note|Holds|Sources|\n|---|---|---|\n" + rows
        )
    with open(os.path.join(root, "corpus", "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write(
            "# SOURCES\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
            + sources_rows
        )


def selftest():
    tool = os.path.abspath(__file__)
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    with tempfile.TemporaryDirectory(prefix="mado-indexrows-") as tmp:
        # 1. clean tree: canonical 3-cell row citing a defined S-id.
        t1 = os.path.join(tmp, "clean")
        _write_tree(
            t1, ["a.md"],
            "| `knowledge/a.md` | The quick brown fox jumps over. | `source:` S001 |\n",
            "| S001 | x | code | A | s | a | t | mined | 2026-10-24 | 180d | corpus/knowledge/a.md |\n",
        )
        r = _run(tool, "--root", t1)
        check("clean tree exits 0 errors=0",
              r.returncode == 0 and "errors=0" in r.stdout)

        # 2. two-cell row (stranded Sources cell; RevengerPrior D2 shape).
        t2 = os.path.join(tmp, "twocell")
        _write_tree(
            t2, ["a.md"],
            "| `knowledge/a.md` | The quick brown fox jumps over. Sources S001. |\n",
            "| S001 | x | code | A | s | a | t | mined | 2026-10-24 | 180d | corpus/knowledge/a.md |\n",
        )
        r = _run(tool, "--root", t2)
        check("two-cell row is ERROR exit 1",
              r.returncode == 1 and "row-cells" in r.stdout)

        # 3. row in a second table + a row inside a comment (CritPredicates A3).
        t3 = os.path.join(tmp, "outside")
        _write_tree(
            t3, ["a.md"],
            "| `knowledge/a.md` | The quick brown fox jumps over. | `source:` S001 |\n"
            "\n| Other | x |\n|---|---|\n"
            "| `knowledge/a.md` | dup elsewhere | s |\n"
            "<!-- | `knowledge/ghost.md` | hidden | row | -->\n",
            "| S001 | x | code | A | s | a | t | mined | 2026-10-24 | 180d | corpus/knowledge/a.md |\n",
        )
        r = _run(tool, "--root", t3)
        check("rows outside the map are ERROR exit 1",
              r.returncode == 1 and "row-outside-map" in r.stdout)

        # 4. empty cells (CritPredicates A1).
        t4 = os.path.join(tmp, "emptycells")
        _write_tree(t4, ["a.md"], "| `knowledge/a.md` |  |  |\n")
        r = _run(tool, "--root", t4)
        check("empty cells are ERROR exit 1",
              r.returncode == 1 and "row-cells" in r.stdout)

        # 5. undefined S-id.
        t5 = os.path.join(tmp, "bads")
        _write_tree(
            t5, ["a.md"],
            "| `knowledge/a.md` | The quick brown fox jumps over. | `source:` S999 |\n",
        )
        r = _run(tool, "--root", t5)
        check("undefined S-id is ERROR exit 1",
              r.returncode == 1 and "cited-s-undefined: S999" in r.stdout)

        # 6. missing backticked path in the Sources cell.
        t6 = os.path.join(tmp, "badpath")
        _write_tree(
            t6, ["a.md"],
            "| `knowledge/a.md` | The quick brown fox jumps over. | `source:` S001; recheck `tools/nope.py REV` |\n",
            "| S001 | x | code | A | s | a | t | mined | 2026-10-24 | 180d | corpus/knowledge/a.md |\n",
        )
        r = _run(tool, "--root", t6)
        check("missing cited path is ERROR exit 1",
              r.returncode == 1 and "cited-path-missing" in r.stdout)

        # 7. Holds cell disjoint from the note is WARN, never an exit bump.
        t7 = os.path.join(tmp, "disjoint")
        _write_tree(
            t7, ["a.md"],
            "| `knowledge/a.md` | Quantum entanglement defies classical locality bounds. | `source:` S001 |\n",
            "| S001 | x | code | A | s | a | t | mined | 2026-10-24 | 180d | corpus/knowledge/a.md |\n",
        )
        r = _run(tool, "--root", t7)
        check("disjoint Holds is WARN exit 0",
              r.returncode == 0 and "holds-no-overlap" in r.stdout)

        # 8. --rev mode on a real git fixture (broken row).
        import shutil
        t8 = os.path.join(tmp, "gitfix")
        if shutil.which("git"):
            _write_tree(
                t8, ["a.md"],
                "| `knowledge/a.md` | two cells only |\n",
            )
            env = dict(
                os.environ,
                GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
            )
            for cmd in (
                ("git", "init", "-q", t8),
                ("git", "-C", t8, "add", "-A"),
                ("git", "-C", t8, "commit", "-qm", "t"),
            ):
                subprocess.run(cmd, check=True, capture_output=True, env=env)
            r = _run(tool, "--rev", "HEAD", "--repo", t8)
            check("--rev flags row-cells exit 1",
                  r.returncode == 1 and "row-cells" in r.stdout)

        # 9. missing corpus/README.md is a setup error, never a clean 0.
        t9 = os.path.join(tmp, "noreadme")
        os.makedirs(os.path.join(t9, "corpus", "knowledge"))
        r = _run(tool, "--root", t9)
        check("missing README is SETUP_ERROR exit 2",
              r.returncode == 2 and "SETUP_ERROR" in r.stderr + r.stdout)

        # 10. a symlinked knowledge member is REFUSED.
        t10 = os.path.join(tmp, "linksym")
        _write_tree(
            t10, ["a.md"],
            "| `knowledge/a.md` | The quick brown fox jumps over. | `source:` S001 |\n",
            "| S001 | x | code | A | s | a | t | mined | 2026-10-24 | 180d | corpus/knowledge/a.md |\n",
        )
        os.symlink(
            os.path.join(t10, "corpus", "knowledge", "a.md"),
            os.path.join(t10, "corpus", "knowledge", "link.md"),
        )
        r = _run(tool, "--root", t10)
        check("symlinked note refused exit 1",
              r.returncode == 1 and "REFUSED" in r.stdout)

    failed = [n for n, ok in checks if not ok]
    passed = len(checks) - len(failed)
    print(f"MADO_INDEX_ROWS_SELFTEST: {passed}/{len(checks)} assertions passed")
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
        data = load_root(args.root)
    elif args.rev:
        if args.rev.startswith("-"):
            print("SETUP_ERROR: --rev must be a revision, not an option",
                  file=sys.stderr)
            return 2
        data = load_rev(args.repo, args.rev)
    else:
        print("SETUP_ERROR: --rev or --root is required", file=sys.stderr)
        return 2
    readme, sources, notes, note_text, exists, exists_glob, tag = data
    return report(tag, readme, sources, notes, note_text, exists, exists_glob)


if __name__ == "__main__":
    raise SystemExit(main())
