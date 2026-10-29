#!/usr/bin/env python3
"""lesson-facts-check.py - read-only facts behind the R56 lesson skeleton (R56W2ScribeLesson).

Reads lane git objects only (git show <rev>:<path>), at the integrated content revision and the
start base. Writes nothing. Prints: registry row counts, rows and used-by paths changed between
base and integrated revision, allowlist conflicts, and anchor coverage of every entry evidence row.
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "13f0acbe3a15da2d9c08357a576d91dcadc85273"
REV = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
ALLOW = ".ufo/waves/round-56/c3-name-only.tsv"


def show(rev, path):
    return subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def rows(text):
    out = {}
    for ln in text.split("\n"):
        if re.match(r"^\| S\d{3} \|", ln):
            c = [x.strip() for x in ln.split("|")[1:-1]]
            out[c[0]] = c
    return out


def cover(anchor, pin_file, n):
    for m in re.finditer(r"([A-Za-z0-9_.\-/]+):([0-9][0-9,\-]*)", anchor):
        name = m.group(1)
        if not (pin_file == name or pin_file == "Hyprland-" + name or pin_file.endswith("-" + name)):
            continue
        for tok in m.group(2).split(","):
            if not tok:
                continue
            if "-" in tok:
                a, b = tok.split("-")
                if int(a) <= n <= int(b):
                    return True
            elif int(tok) == n:
                return True
    return False


def main():
    b = rows(show(BASE, "corpus/SOURCES.md"))
    n = rows(show(REV, "corpus/SOURCES.md"))
    print(f"registry rows base={len(b)} rev={len(n)} added={sorted(set(n) - set(b))} removed={sorted(set(b) - set(n))}")
    changed = [k for k in b if k in n and b[k] != n[k]]
    appended = 0
    for k in changed:
        old = [x.strip() for x in b[k][10].split(",") if x.strip()]
        new = [x.strip() for x in n[k][10].split(",") if x.strip()]
        if [i for i, (x, y) in enumerate(zip(b[k], n[k])) if x != y] != [10]:
            print("NON-USED-BY CHANGE", k)
        appended += len([x for x in new if x not in old])
        if any(x not in new for x in old):
            print("USED-BY REMOVAL", k)
    print(f"rows with used-by change={len(changed)} appended used-by paths={appended}")

    allow = [line.split("\t") for line in show(REV, ALLOW).split("\n") if line.strip()]
    conflicts = [a[:2] for a in allow if a[1] in [x.strip() for x in n[a[0]][10].split(",")]]
    print(f"allowlist rows={len(allow)} conflicts(in used-by)={len(conflicts)}")

    ent = show(REV, ENTRY).split("\n")
    kinds = {"K": 0, "H": 0, "E": 0}
    misses = []
    for ln in ent:
        if not re.match(r"^\| [KHE]\d\d \|", ln):
            continue
        c = [x.strip() for x in ln.split("|")[1:-1]]
        rid, src, pin = c[0], c[2], c[3]
        kinds[rid[0]] += 1
        if src not in n:
            continue
        fname, line_no = re.match(r"(.+):(\d+)$", pin).groups()
        if not cover(n[src][5], fname, int(line_no)):
            misses.append((rid, src, pin))
    print(f"entry evidence rows K={kinds['K']} H={kinds['H']} E={kinds['E']}")
    print(f"anchor-not-covering rows={len(misses)}: {misses}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
