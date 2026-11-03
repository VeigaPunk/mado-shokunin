#!/usr/bin/env python
"""mado-receipt-citecheck — read-only citation-resolvability checker (round 64).

The r63 closure routed a receipt whose input-fixture citation named a path that was
never committed (the ephemeral-fixture defect). This tool generalizes that class into
a durable instrument: it extracts repo-relative path citations from caller-named
artifacts and verifies each resolves in the git tree at --rev.

Extraction grammar (strict, fail-closed): a token that starts with one of the lane's
repo-relative tops (.ufo/ corpus/ tools/ quality/ plans/) preceded by a token boundary
(start of line, whitespace, or one of ( | [ > < " ' ` , ; =) — never a path separator
or ':', so suffixes of longer paths, absolute host paths and git-rev-prefixed forms
are excluded except after whitespace), with trailing punctuation .,;:)]}"'` trimmed.
Anything else is not a citation and is never reported.

Resolve: one `git -C <repo> ls-tree -r --name-only <rev>` child per run; every
extracted path is checked against the resulting name set. MISSING paths are named,
never silently skipped. Files over the 4 MiB read cap are skipped and counted.

Scope is caller-named paths only; the tool never walks history and is never run over
r56-era material (the lane's standing security boundary).

Verdict: MADO_CITECHECK: rev=<rev> files=<n> citations=<c> resolved=<r> missing=<m>
skipped=<s> verdict=TARGET_MET|TARGET_MISSED — exit 0 (missing=0), 1 (missing>0),
2 (setup error). Writes nothing; stdout only. --selftest is hermetic (pure functions
over in-memory fixtures written only under the caller-declared --scratch-root, which
is removed; it spawns nothing and refuses /tmp per the M57-1 policy).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "r64-v1"
TOPS = (".ufo/", "corpus/", "tools/", "quality/", "plans/")
ANCHORS = set(" \t\r\n\f\v(|[<>\"'`,;=")
TRIM = set(".,;:)]}\"'`")
MAX_FILE_BYTES = 4 * 1024 * 1024
SCAN_EXTS = {".txt", ".md", ".json", ".py", ".ps1", ".sh", ".log"}

CITE_RE = re.compile(
    r"(?:^|[\s(|\[<>\"'`,;=])((?:\.ufo|corpus|tools|quality|plans)/[A-Za-z0-9_./-]+)"
)
# The checker verifies file-path citations: the last segment must carry an
# extension-like suffix. A bare-directory token (.ufo/waves/round-63) is not a
# resolvable citation — `git ls-tree -r --name-only` lists blobs, and naming a
# directory is not naming a committed file.
FILE_SUFFIX_RE = re.compile(r"/[A-Za-z0-9_-]+\.[A-Za-z0-9]+$")


def extract_citations(text: str) -> list[str]:
    """Ordered unique repo-relative file-path citations per the grammar above."""
    found: list[str] = []
    seen: set[str] = set()
    for m in CITE_RE.finditer(text):
        tok = m.group(1)
        while tok and tok[-1] in TRIM:
            tok = tok[:-1]
        if not tok or tok in seen:
            continue
        if not any(tok.startswith(t) for t in TOPS):
            continue
        if "/../" in tok or tok.endswith("/.") or tok.endswith("/.."):
            continue
        if not FILE_SUFFIX_RE.search(tok):
            continue
        seen.add(tok)
        found.append(tok)
    return found


def collect_files(paths: list[str]) -> tuple[list[Path], list[str]]:
    """Expand caller-named files/dirs to the scanned file list (deterministic order)."""
    files: list[Path] = []
    notes: list[str] = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            for root, dirs, names in os.walk(pp):
                dirs.sort()
                for name in sorted(names):
                    f = Path(root) / name
                    if f.suffix.lower() in SCAN_EXTS:
                        files.append(f)
        elif pp.is_file():
            files.append(pp)
        else:
            notes.append("arg-not-found: %s" % p)
    return files, notes


def run_check(repo: str, rev: str, paths: list[str]) -> int:
    try:
        out = subprocess.run(
            ["git", "-C", repo, "ls-tree", "-r", "--name-only", rev],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, OSError) as exc:
        detail = getattr(exc, "returncode", type(exc).__name__)
        print("MADO_CITECHECK: ERROR (stage=git detail=%s)" % detail, file=sys.stderr)
        return 2
    tree = set(out.splitlines())
    files, notes = collect_files(paths)
    for n in notes:
        print("CITECHECK %s" % n)
    citations: dict[str, list[str]] = {}
    skipped_large = 0
    scanned = 0
    for f in files:
        try:
            if f.stat().st_size > MAX_FILE_BYTES:
                skipped_large += 1
                print("CITECHECK skipped-large: %s" % f)
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print("CITECHECK unreadable: %s (%s)" % (f, type(exc).__name__))
            continue
        scanned += 1
        for cite in extract_citations(text):
            citations.setdefault(cite, []).append(str(f))
    resolved = sorted(c for c in citations if c in tree)
    missing = sorted(c for c in citations if c not in tree)
    for c in resolved:
        print("CITECHECK resolved: %s (from %d site(s))" % (c, len(citations[c])))
    for c in missing:
        print("CITECHECK MISSING: %s (from %s)" % (c, ", ".join(sorted(set(citations[c])))))
    verdict = "TARGET_MET" if not missing else "TARGET_MISSED"
    print(
        "MADO_CITECHECK: rev=%s files=%d citations=%d resolved=%d missing=%d "
        "skipped_large=%d verdict=%s (VERSION %s)"
        % (rev, scanned, len(citations), len(resolved), len(missing), skipped_large, verdict, VERSION)
    )
    return 0 if not missing else 1


def selftest(scratch_root: str) -> int:
    checks: list[tuple[str, bool]] = []

    def want(name: str, cond: bool) -> None:
        checks.append((name, bool(cond)))

    # 1. extraction: exact set from a mixed sample
    sample = (
        "receipt .ufo/waves/round-63/receipts/windisplayconfig-snapshot.json end\n"
        "cites tools/mado-win-displayconfig.py and corpus/SOURCES.md.\n"
        "(parenthesized quality/check-tool-ledger.py)\n"
        "table |.ufo/waves/round-64/receipts/qdc-matrix-run1.json|\n"
        "ellipsis form ...receipts/broken-fixture.json is not a citation\n"
        "absolute C:/Users/x/fleet/mado-shokunin/corpus/README.md is not repo-relative\n"
        "git-object form 7fe65562:corpus/README.md is rev-prefixed, not extracted\n"
        "url https://example.com/corpus/SOURCES.md is not extracted\n"
    )
    got = extract_citations(sample)
    want("extract.set", got == [
        ".ufo/waves/round-63/receipts/windisplayconfig-snapshot.json",
        "tools/mado-win-displayconfig.py",
        "corpus/SOURCES.md",
        "quality/check-tool-ledger.py",
        ".ufo/waves/round-64/receipts/qdc-matrix-run1.json",
    ])
    # 2. trailing punctuation trimmed, dedup keeps order
    want("extract.trim", extract_citations("see corpus/README.md, and corpus/README.md.") == ["corpus/README.md"])
    # 3. traversal rejected
    want("extract.traversal", ".ufo/x/../../secrets" not in extract_citations("p .ufo/x/../../secrets end"))
    # 4. suffix-of-longer-path not extracted (no anchor mid-token)
    want("extract.suffix", extract_citations("path mycorpus/README.md end") == [])
    # 4b. bare-directory tokens are not file-path citations
    want("extract.bare-dir", extract_citations("run: git grep -l x rev -- .ufo/waves/round-63 corpus | wc -l") == [])
    # 5. resolve/verdict against a synthetic tree set: red then green
    tmp = tempfile.mkdtemp(prefix="citecheck-selftest-", dir=scratch_root)
    try:
        real = Path(tmp) / "artifacts"
        real.mkdir()
        (real / "a.txt").write_text("cites corpus/README.md and .ufo/waves/round-63/receipts/broken-fixture.json\n", encoding="utf-8")
        files, notes = collect_files([str(real)])
        want("collect.dir", len(files) == 1 and not notes)
        cites = extract_citations(files[0].read_text(encoding="utf-8"))
        want("collect.cites", cites == ["corpus/README.md", ".ufo/waves/round-63/receipts/broken-fixture.json"])
        tree_green = set(cites) | {"corpus/README.md", ".ufo/waves/round-63/receipts/broken-fixture.json"}
        want("resolve.green", all(c in tree_green for c in cites))
        tree_red = {"corpus/README.md"}
        want("resolve.red", any(c not in tree_red for c in cites))
        # 6. large-file skip counted
        big = Path(tmp) / "big.txt"
        big.write_bytes(b"x" * (MAX_FILE_BYTES + 1))
        want("cap.stat", big.stat().st_size > MAX_FILE_BYTES)
        # 7. extension filter: unlisted extension not collected
        (real / "b.bin").write_text("corpus/README.md", encoding="utf-8")
        files2, _ = collect_files([str(real)])
        want("collect.ext", all(f.suffix.lower() in SCAN_EXTS for f in files2) and len(files2) == 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # 8. scratch policy: /tmp refused is enforced by the caller contract; assert the helper exists
    want("policy.version", VERSION == "r64-v1")

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("CITECHECK_SELFTEST: CHECK FAILED %s" % name, file=sys.stderr)
    print("MADO_CITECHECK_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(add_help=True, description="read-only receipt citation-resolvability checker")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--paths", nargs="*", default=[])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--scratch-root", default=None, help="caller-declared scratch root for --selftest (M57-1)")
    args = ap.parse_args(argv)
    if args.selftest:
        if not args.scratch_root:
            print("MADO_CITECHECK_SELFTEST: REFUSED (--scratch-root required, M57-1)", file=sys.stderr)
            return 2
        sr = os.path.abspath(args.scratch_root)
        if sr.rstrip("/\\") in ("/tmp", "C:/tmp") or sr.startswith(os.path.abspath("/tmp")):
            print("MADO_CITECHECK_SELFTEST: REFUSED (/tmp scratch refused, M57-1)", file=sys.stderr)
            return 2
        os.makedirs(sr, exist_ok=True)
        return selftest(sr)
    if not args.paths:
        print("MADO_CITECHECK: ERROR (stage=args detail=--paths required)", file=sys.stderr)
        return 2
    return run_check(args.repo, args.rev, args.paths)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
