#!/usr/bin/env python3
"""check-anchor-cover.py - candidate QUALITY criterion 107 (M56-1): a registry row's anchor covers the quoted line.

Reads git objects only (`git cat-file`), at --rev of --repo; writes nothing outside --work.

For every table row of --entry whose cell 3 is a registry id (S###) and whose cell 4 is `<file>:<N>`
(the K-row grammar of the round-56 registration §C1), the registry row of that id in corpus/SOURCES.md
at --rev must satisfy:
  NAME  = the last path component of the last http(s) URL in the registry row's source cell
          (the upstream file the row credits; for r56 pins this equals basename(pin_suffix[pin]));
  COVER = the registry row's anchor cell (cell 6) holds an occurrence of `NAME:` (preceded by a
          non-identifier character or start) followed by a comma-separated list of locators, the
          first item of which must be `N` or `N-M`; subsequent items continue the list only while
          they begin with digits; some locator range includes N (the quoted line).
Every failing row prints `MISS row=<id> sid=<S###> line=<N> name=<NAME> reason=<no-name|no-cover>`.

Output: `ANCHOR_COVER: row=<id> sid=<S###> line=<N> name=<NAME> locators=<list|none> verdict=OK|MISS`
then `CHECK107: rows=<n> covered=<k> miss=<m> verdict=OK|FAIL`; exit 0 OK, 1 FAIL, 2 setup error.
"""
import argparse
import os
import re
import subprocess
import sys

ROW_RE = re.compile(r"^\s{0,3}\|")
REG_ID_RE = re.compile(r"^\s{0,3}\|\s*S[0-9]{3,}\s*\|")
URL_RE = re.compile(r"https?://\S+")
PIN_RE = re.compile(r"^(?P<file>[^:\s]+):(?P<line>[0-9]+)$")
FENCE_RE = re.compile(r"^ {0,3}(```|~~~)")


def git_show(repo, rev, path, env):
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob", f"{rev}:{path}"],
                       capture_output=True, env=env)
    if r.returncode != 0:
        raise SystemExit(f"setup: absent {rev}:{path}")
    return r.stdout.decode("utf-8", errors="replace")


def cells_of(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def registry(text):
    rows = {}
    for line in text.splitlines():
        if REG_ID_RE.match(line):
            cells = cells_of(line)
            if len(cells) != 11:
                raise SystemExit(f"setup: registry row {cells[0]} has {len(cells)} cells")
            rows[cells[0]] = cells
    return rows


def entry_rows(text):
    out, fenced = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced or not ROW_RE.match(line):
            continue
        c = cells_of(line)
        if len(c) >= 4 and re.fullmatch(r"S[0-9]{3,}", c[2]):
            m = PIN_RE.match(c[3])
            if m:
                out.append((n, c[0], c[2], int(m.group("line"))))
    return out


def covers(anchor, name, line):
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r":")
    listed, hit = [], False
    for m in pat.finditer(anchor):
        rest = anchor[m.end():]
        first = re.match(r"([0-9]+)(?:-([0-9]+))?", rest)
        if not first:
            continue
        ranges = [(first.group(1), first.group(2))]
        pos = first.end()
        while True:
            nxt = re.match(r",\s*([0-9]+)(?:-([0-9]+))?", rest[pos:])
            if not nxt:
                break
            ranges.append((nxt.group(1), nxt.group(2)))
            pos += nxt.end()
        for lo, hi in ranges:
            lo_i, hi_i = int(lo), int(hi) if hi else int(lo)
            listed.append(f"{lo_i}-{hi_i}" if hi else f"{lo_i}")
            if min(lo_i, hi_i) <= line <= max(lo_i, hi_i):
                hit = True
    return hit, (",".join(listed) if listed else "none")


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--entry", required=True)
    ap.add_argument("--registry", default="corpus/SOURCES.md")
    ap.add_argument("--work", required=True)
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        print("MADO_ANCHOR: SETUP usage", file=sys.stderr)
        return 2
    os.makedirs(a.work, exist_ok=True)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": a.work, "TMPDIR": a.work,
           "LC_ALL": "C"}
    try:
        reg = registry(git_show(a.repo, a.rev, a.registry, env))
        rows = entry_rows(git_show(a.repo, a.rev, a.entry, env))
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2
    n = len(rows); covered = 0
    for lno, rid, sid, line in rows:
        cells = reg.get(sid)
        if cells is None:
            print(f"ANCHOR_COVER: row={rid} sid={sid} line={line} name=- locators=- verdict=MISS reason=no-registry-row")
            continue
        urls = URL_RE.findall(cells[1])
        name = urls[-1].rstrip(").,;").rsplit("/", 1)[-1] if urls else ""
        anchor = cells[5]
        hit, locs = covers(anchor, name, line) if name else (False, "none")
        ok = hit
        covered += ok
        reason = "" if ok else (" reason=no-cover" if name and locs != "none" else " reason=no-name")
        print(f"ANCHOR_COVER: row={rid} sid={sid} line={line} name={name or '-'} locators={locs} "
              f"verdict={'OK' if ok else 'MISS'}{reason if not ok else ''}")
    miss = n - covered
    print(f"CHECK107: rows={n} covered={covered} miss={miss} verdict={'OK' if miss == 0 and n else 'FAIL'}")
    return 0 if miss == 0 and n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
