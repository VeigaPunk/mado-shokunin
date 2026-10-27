#!/usr/bin/env python3
"""check99 - a corpus-to-corpus locator resolves to one file and anchors the item it restates.

QUALITY criterion 99 (draft, round 48; extension of criterion 77). Criterion 77 reads a locator
into a *pinned receipt* and requires the cited range to carry the fact's identifier, but its
instrument (`quality/check-locators.py --fetch ...`) only resolves file names that exist in the
fetch directory: on the round-47 entry it reports `locators=0`, so every reference from one corpus
file to another is unread. Two shapes then survive:

  A. an unqualified basename that two different files match (`README.md` is both the lane's
     README and the pinned upstream README under `--fetch`), so the range resolves to a file that
     has fewer lines than the citation names;
  B. an `[UNK]` restatement whose range starts after the bullet that carries the item's head.

Rules: a locator resolves against the repo tree at `--rev`, trying the repo path, then each
`--root` (default `corpus/knowledge`, `corpus`), then `--fetch`; two matching files is AMBIGUOUS;
no match is UNRESOLVED. A range outside the file is OUT-OF-RANGE. When the citing line says
`[UNK]` and the cited file uses `- [UNK]` bullets, the range must start on the bullet line or on
a line that itself carries `[UNK]`.

Usage:
  check99.py --repo . --rev REV --citing <path-in-repo> [--fetch <dir-in-repo>]
Exit 0 = no violation, 1 = at least one, 2 = input unreadable.
"""
import argparse
import os
import re
import subprocess
import sys

TOK = re.compile(r"((?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.md):(\d+)(?:-(\d+))?")
BULLET = re.compile(r"^\s*-\s*\[UNK\]")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True, errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--citing", required=True)
    ap.add_argument("--fetch", default=None)
    ap.add_argument("--citing-text", action="store_true",
                    help="read --citing from disk instead of from --rev")
    a = ap.parse_args()

    if a.citing_text:
        try:
            citing = open(a.citing, encoding="utf-8", errors="replace").read()
        except OSError as exc:
            print("MISSING-CITING %s (%s)" % (a.citing, exc))
            return 2
    else:
        r = git(a.repo, "show", "%s:%s" % (a.rev, a.citing))
        if r.returncode:
            print("MISSING-CITING %s at %s" % (a.citing, a.rev))
            return 2
        citing = r.stdout

    roots = [""]
    if a.fetch:
        roots.append(a.fetch)
    roots += ["corpus/knowledge", "corpus"]

    cache = {}

    def show(path):
        if path not in cache:
            g = git(a.repo, "show", "%s:%s" % (a.rev, path))
            cache[path] = g.stdout if not g.returncode else None
        return cache[path]

    seen, bad, checked = set(), 0, 0
    lines = citing.splitlines()
    for idx, line in enumerate(lines, 1):
        for m in TOK.finditer(line):
            name, a1 = m.group(1), int(m.group(2))
            a2 = int(m.group(3)) if m.group(3) else a1
            if (name, a1, a2) in seen:
                continue
            seen.add((name, a1, a2))
            hits = [p for p in (os.path.join(rt, name) if rt else name for rt in roots)
                    if show(p) is not None]
            hits = list(dict.fromkeys(hits))
            if not hits:
                print("UNRESOLVED %s:%d-%d (line %d)" % (name, a1, a2, idx))
                bad += 1
                continue
            if len(hits) > 1:
                print("AMBIGUOUS %s:%d-%d -> %s (line %d)"
                      % (name, a1, a2, ",".join(hits), idx))
                bad += 1
                continue
            path = hits[0]
            body = show(path).splitlines()
            checked += 1
            if a1 < 1 or a2 > len(body):
                print("OUT-OF-RANGE %s:%d-%d (file has %d lines)" % (path, a1, a2, len(body)))
                bad += 1
                continue
            span = body[a1 - 1:a2]
            # rule B: an [UNK] restatement must include the bullet that carries the item head
            if "[UNK]" in line and any(BULLET.match(b) for b in body):
                if not (BULLET.match(span[0]) or any("[UNK]" in b for b in span)):
                    print("UNK-HEAD-CUT %s:%d-%d bullet_at=%d first=%r (citing line %d)"
                          % (path, a1, a2,
                             max([i for i, b in enumerate(body, 1)
                                  if BULLET.match(b) and i <= a1], default=0),
                             span[0], idx))
                    bad += 1
                    continue
            print("OK %s:%d-%d first=%r" % (path, a1, a2, span[0]))
    print("CHECK99: locators=%d checked=%d violations=%d verdict=%s"
          % (len(seen), checked, bad, "CUT" if bad else "OK"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
