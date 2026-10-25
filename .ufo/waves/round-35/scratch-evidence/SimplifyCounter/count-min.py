#!/usr/bin/env python3
"""PRED-C1-r35-v1 counter (minimal form). exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage/drift."""
import argparse, json, re, stat, sys
from pathlib import Path

PREDICATE = (
    "PRED-C1-r35-v1: TARGET_MET iff closed_entries=3 AND closed_rows=8 AND open_cites=0, "
    "where a frozen cite is closed only when the entry path is a regular file inside the "
    "scored root, the registry holds exactly one well-formed row for that id whose used-by "
    "token set is exactly the admitted entries citing it, whose status is `mined`, whose "
    "recheck cell is a valid cadence token, whose cells contain no literal or escaped pipe, "
    "and whose anchor cell carries the sha256 of the named receipt; and the entry carries "
    "exactly one gate-quote line for that id whose quote is a contiguous substring of the "
    "receipt bytes and is 1-25 words long."
)
TARGET = {"closed_entries": 3, "closed_rows": 8, "open_cites": 0}
RECHECK = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|[A-Za-z][A-Za-z0-9 _-]*)$")


def die(msg):
    print(f"PRED-C1-r35-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def regular_bytes(root, rel):
    """Bytes of rel if every component under root is a non-symlink dir and the leaf a
    non-symlink regular file; None otherwise."""
    parts = Path(rel).parts
    if not parts or rel.startswith(("/", "\\")) or any(p in ("", ".", "..") for p in parts):
        return None
    try:
        if not all(stat.S_ISDIR(root.joinpath(*parts[: i + 1]).lstat().st_mode)
                   for i in range(len(parts) - 1)):
            return None
        cur = root / rel
        return cur.read_bytes() if stat.S_ISREG(cur.lstat().st_mode) else None
    except OSError:
        return None


def cells(line):
    s = line.split("|")
    return [p.strip() for p in s[line.startswith("|"):len(s) - line.endswith("|")]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--frozen", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    if not (fp := Path(args.frozen)).is_file():
        die("frozen-missing")
    spec = json.loads(fp.read_text())
    if spec.get("predicate") != PREDICATE or spec.get("target") != TARGET:
        die("predicate-or-target-drift")

    src = regular_bytes(root, "corpus/SOURCES.md") or b""
    rows = {}
    for l in src.decode("utf-8", "replace").splitlines():
        if m := re.match(r"^ {0,3}\|\s*(S[0-9]+)\s*\|", l):
            rows.setdefault(m.group(1), []).append(l)

    closed_entries = closed_rows = open_cites = 0
    for rel, ids in spec["entries"].items():
        eb = regular_bytes(root, rel)
        entry = eb.decode("utf-8", "replace") if eb else ""
        entry_closed = eb is not None
        citing = {sid: {r for r, i2 in spec["entries"].items() if sid in i2} for sid in ids}
        for sid in ids:
            rc = spec["receipts"][sid]
            blob = regular_bytes(root, rc["path"])
            needle = f"gate-quote: {sid} "
            qs = [l[len(needle):] for l in entry.splitlines() if l.startswith(needle)]
            rs = rows.get(sid, [])
            cs = cells(rs[0]) if len(rs) == 1 else []
            ok = (
                blob is not None
                and len(rs) == 1
                and len(cs) == 11
                and {t for t in (s.strip() for s in cs[10].split(",")) if t} == citing[sid]
                and cs[7] == "mined"
                and RECHECK.match(cs[9])
                and rc["sha256"] in cs[5]
                and len(qs) == 1
                and 1 <= len(qs[0].split()) <= 25
                and qs[0].encode() in blob
            )
            if ok:
                closed_rows += 1
            else:
                open_cites += 1
                entry_closed = False
        closed_entries += entry_closed
    met = (closed_entries == TARGET["closed_entries"]
           and closed_rows == TARGET["closed_rows"]
           and open_cites == TARGET["open_cites"])
    print(f"PRED-C1-r35-v1 closed_entries={closed_entries} closed_rows={closed_rows} "
          f"open_cites={open_cites} verdict={'TARGET_MET' if met else 'TARGET_MISSED'}")
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
