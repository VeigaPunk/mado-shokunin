#!/usr/bin/env python3
"""Round-19 check for R18-V3: a supersession sweeps every owned mention.

Usage: supersede-sweep.py REV [--ledger PATH]

The ledger (default: supersessions.json next to this script) carries
{"schema": "...", "entries": [ENTRY, ...]} where each ENTRY is
  {"id": "walker-2.17.2", "old": "2.17.0", "new": "2.17.2",
   "since": "2026-10-20", "rows": ["S090", "S096"],
   "scope": ["corpus/knowledge/*.md", "corpus/README.md", "SKILL.md",
             "PROVINCE.md", "tools/*"]}
(`since` is documentation; `rows` defaults to []; a bare ENTRY list is also
accepted).

For each entry, every file matched by `scope` in the tree at REV whose bytes
contain `old` is classified by its lines:

  POINTED <path>  some line carries `new` and a permitted row token - one of
                  `rows`, or any `S###` when `rows` is empty. A span citation
                  (`S072-S091`, en/em dash or ASCII hyphen, second `S`
                  optional) covers every row in the range, the lane's own
                  citation convention (corpus/README.md cites `S072-S091`).
  STALE <path>    no line carries both: the old mention has no pointer.

`scope` globs match component-wise, so `*` never crosses `/`; paths are
lane-relative as `git ls-tree` reports them. A file absent at REV contains no
`old` bytes and is therefore not classified - deleting a mention also clears
it; the fixed 9c54c56 denominator lives in fresh-pins.py, not here.

Between entries a `# entry <id>` header is printed only when the ledger holds
more than one entry; a per-entry count line goes to stderr.

Exit: 0 no STALE, 1 any STALE, 2 usage or could-not-evaluate.
Reads committed bytes only (`git ls-tree`, `git show`); writes nothing.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "supersessions.json")
TOKEN = re.compile(r"\bS(\d{3})\b")
SPAN = re.compile(r"\bS(\d{3})\s*[\u2013\u2014-]\s*S?(\d{3})\b")


def usage(msg=None):
    if msg:
        print(f"supersede-sweep: {msg}", file=sys.stderr)
    print("usage: supersede-sweep.py REV [--ledger PATH]", file=sys.stderr)
    return 2


def git(*args):
    return subprocess.run(["git", "-C", LANE, *args], capture_output=True)


def glob_path(path, pattern):
    parts = path.split("/")
    pats = pattern.split("/")
    return len(parts) == len(pats) and all(fnmatch.fnmatchcase(p, q) for p, q in zip(parts, pats))


def load_ledger(path):
    try:
        with open(path, "rb") as fh:
            data = json.loads(fh.read().decode())
    except OSError as exc:
        raise ValueError(f"ledger {path}: {exc.strerror}") from None
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError(f"ledger {path}: {exc}") from None
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        entries = data.get("entries")
    else:
        entries = None
    if not isinstance(entries, list) or not entries:
        raise ValueError("ledger: no entries")
    seen = set()
    out = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"entry {i}: not an object")
        ident, old, new = entry.get("id"), entry.get("old"), entry.get("new")
        scope, rows = entry.get("scope"), entry.get("rows", [])
        if not isinstance(ident, str) or not ident:
            raise ValueError(f"entry {i}: id")
        if ident in seen:
            raise ValueError(f"entry {i}: duplicate id {ident}")
        seen.add(ident)
        if not isinstance(old, str) or not old or not isinstance(new, str) or not new:
            raise ValueError(f"entry {ident}: old/new must be non-empty strings")
        if old == new:
            raise ValueError(f"entry {ident}: old equals new")
        if not isinstance(scope, list) or not scope or not all(isinstance(s, str) and s for s in scope):
            raise ValueError(f"entry {ident}: scope must be a non-empty list of globs")
        if not isinstance(rows, list) or not all(isinstance(r, str) and re.fullmatch(r"S\d{3}", r) for r in rows):
            raise ValueError(f"entry {ident}: rows must be S### strings")
        out.append({"id": ident, "old": old, "new": new, "rows": rows, "scope": scope})
    return out


def covered_rows(line):
    rows = set()
    for m in SPAN.finditer(line):
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo <= hi:
            rows.update(range(lo, hi + 1))
    for m in TOKEN.finditer(line):
        rows.add(int(m.group(1)))
    return rows


def pointed(text, new, rows):
    permit = {int(r[1:]) for r in rows}
    for line in text.splitlines():
        if new not in line:
            continue
        here = covered_rows(line)
        if here & permit if permit else here:
            return True
    return False


def main():
    args = sys.argv[1:]
    rev, ledger_path = None, DEFAULT_LEDGER
    while args:
        arg = args.pop(0)
        if arg in ("-h", "--help"):
            print(__doc__)
            return 0
        if arg == "--ledger":
            if not args:
                return usage("--ledger needs PATH")
            ledger_path = args.pop(0)
        elif arg.startswith("--ledger="):
            ledger_path = arg.split("=", 1)[1]
        elif arg.startswith("-") or rev is not None:
            return usage(f"unexpected argument {arg}")
        else:
            rev = arg
    if rev is None:
        return usage()
    try:
        entries = load_ledger(ledger_path)
    except ValueError as exc:
        print(f"could_not_evaluate: {exc}", file=sys.stderr)
        return 2
    p = git("rev-parse", "--verify", rev + "^{commit}")
    if p.returncode != 0:
        print(f"could_not_evaluate: rev {rev}", file=sys.stderr)
        return 2
    commit = p.stdout.decode().strip()
    ls = git("ls-tree", "-r", "--name-only", "-z", commit)
    if ls.returncode != 0:
        print("could_not_evaluate: ls-tree", file=sys.stderr)
        return 2
    paths = [x for x in ls.stdout.decode("utf-8", "surrogateescape").split("\0") if x]
    stale_total = 0
    multiple = len(entries) > 1
    for entry in entries:
        scoped = [x for x in paths if any(glob_path(x, g) for g in entry["scope"])]
        if multiple:
            print(f"# entry {entry['id']}")
        files = pointed_n = stale_n = 0
        for path in sorted(scoped):
            b = git("show", f"{commit}:{path}")
            if b.returncode != 0:
                print(f"could_not_evaluate: git show {commit}:{path}", file=sys.stderr)
                return 2
            if entry["old"].encode() not in b.stdout:
                continue
            files += 1
            if pointed(b.stdout.decode("utf-8", "replace"), entry["new"], entry["rows"]):
                pointed_n += 1
                print(f"POINTED {path}")
            else:
                stale_n += 1
                print(f"STALE {path}")
        stale_total += stale_n
        print(f"supersede-sweep: {entry['id']} rev={commit} files={files} "
              f"pointed={pointed_n} stale={stale_n}", file=sys.stderr)
    return 1 if stale_total else 0


if __name__ == "__main__":
    sys.exit(main())
