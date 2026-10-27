#!/usr/bin/env python3
"""C1Evidence probe (round 52): read-only base-state measurements for the C1 evidence review.

Reads committed git objects only (`git -C <repo> ls-tree/show/rev-parse`); writes nothing.
Every number printed here is reproduced from the base tree, not from the round-51 receipt.

Usage: python3 -I probe_base.py [rev]   (default rev = the round-52 base)
"""
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
LEDGER = "quality/tool-ledger.md"
CONTROL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/controls/c1-do-nothing.md"
EMPH = "`*_ \t"
LINE_ANCHOR = re.compile(r":\d+(?:-\d+)?$")
GENERIC = set("""a an the of to and or for in on with at by from that this these those
is are be can may must not no only each every one two all any per as it its into via
read reads writing writes write prints print returns return gate check checks""".split())


def git(*args):
    p = subprocess.run(("git", "-C", REPO) + args, capture_output=True)
    if p.returncode:
        raise SystemExit("git %s: %s" % (" ".join(args), p.stderr.decode()[:300]))
    return p.stdout


def listing():
    return [x for x in git("ls-tree", "-r", "--name-only", REV).decode().splitlines() if x]


def population(paths):
    pop = []
    for path in paths:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            pop.append(path)
            continue
        for root in ("quality/counters/", "quality/"):
            if not path.startswith(root):
                continue
            rest = path[len(root):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
            break
    return sorted(set(pop))


def rows_of(text):
    rows, fenced = [], False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip(EMPH) if cells else ""
        if not first or "/" not in first or first.startswith(":") or set(first) <= set("-: "):
            continue
        rows.append(cells)
    return rows


def pointer_tokens(cell):
    toks = re.findall(r"`([^`\n]+)`", cell)
    if not toks:
        toks = re.split(r"[,;]|\s+", cell)
    out = []
    for t in toks:
        t = t.strip(EMPH)
        t = re.sub(r"^\./", "", t)
        t = LINE_ANCHOR.sub("", t)
        if not t or t.startswith(("/", "~", "$")):
            continue
        if any(ch in t for ch in "<>():#?*\"'"):
            continue
        if "/" not in t and not re.search(r"\.(md|py|sh|json|txt|ya?ml)$", t):
            continue
        out.append(t)
    return out


def main():
    files = set(listing())
    pop = population(sorted(files))
    cache = {}

    def body(p):
        if p not in cache:
            cache[p] = git("show", "%s:%s" % (REV, p))
        return cache[p]

    def resolves(row_path, pointer):
        base = os.path.basename(row_path)
        tried = []
        for tok in pointer_tokens(pointer):
            tried.append(tok)
            if tok in files and base.encode() in body(tok):
                return True, tried
        return False, tried

    print("REV=%s resolved=%s" % (REV, git("rev-parse", REV + "^{commit}").decode().strip()))
    print("c1_r52_paths_at_rev=%d" % len([p for p in files if "c1-r52" in p]))
    print("population=%d tools=%d quality_py=%d counters=%d" % (
        len(pop), len([p for p in pop if p.startswith("tools/")]),
        len([p for p in pop if p.startswith("quality/") and p.count("/") == 1]),
        len([p for p in pop if p.startswith("quality/counters/")])))

    ledger_text = body(LEDGER).decode("utf-8", "replace")
    rows = rows_of(ledger_text)
    paths = [r[0].strip(EMPH) for r in rows]
    descs = [(r[1].strip(EMPH) if len(r) > 1 else "") for r in rows]
    print("ledger_rows=%d cell_counts=%r" % (len(rows), sorted({len(r) for r in rows})))
    print("dup_paths=%d dup_descriptions=%d paths_outside_population=%d" % (
        len(paths) - len(set(paths)), len(descs) - len(set(descs)),
        len([p for p in paths if p not in set(pop)])))

    bad, self_targeted, targets = [], 0, {}
    for r in rows:
        p = r[0].strip(EMPH)
        ok, tried = resolves(p, " | ".join(r[2:]))
        if not ok:
            bad.append(p)
        if LEDGER in tried:
            self_targeted += 1
        elif ok:
            for t in tried:
                if t in files and os.path.basename(p).encode() in body(t):
                    targets[t] = targets.get(t, 0) + 1
                    break
    print("r51_semantics_bad_pointer=%d self_pointer_rows=%d distinct_pointer_files=%d" % (
        len(bad), self_targeted, len(targets)))
    for t, n in sorted(targets.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  pointer %3d %s" % (n, t))

    lens = sorted(len(d.split()) for d in descs)
    print("desc_words min=%d p25=%d median=%d p75=%d max=%d under6=%d" % (
        lens[0], lens[len(lens) // 4], lens[len(lens) // 2],
        lens[3 * len(lens) // 4], lens[-1], len([n for n in lens if n < 6])))

    def words(s):
        return [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_+-]{2,}", s)]

    zero = []
    for r in rows:
        p = r[0].strip(EMPH)
        desc = r[1] if len(r) > 1 else ""
        dt = {w for w in words(desc) if w not in GENERIC}
        bt = {w for w in words(body(p).decode("utf-8", "replace")[:4000]) if w not in GENERIC}
        if not (dt & bt):
            zero.append(p)
    print("desc_zero_distinctive_overlap_with_own_bytes=%d" % len(zero))
    for p in zero[:10]:
        print("  zero path=%s" % p)

    with open(CONTROL, "rb") as fh:
        ctext = fh.read()
    crows = rows_of(ctext.decode())
    print("control_bytes=%d control_data_rows=%d control_cell_counts=%r distinct_tools=%d" % (
        len(ctext), len(crows), sorted({len(r) for r in crows}),
        len({r[0].strip(EMPH) for r in crows})))
    for r in crows:
        print("  control_cells=%r" % (r,))
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        REV = sys.argv[1]
    sys.exit(main())
