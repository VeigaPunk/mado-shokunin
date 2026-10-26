#!/usr/bin/env python3
"""Tightening candidates for PRED-C2-r46, computed from the counter's own helpers.
Usage: tighten.py <repo> <rev>...  -> one line of A..F per rev plus detail.
A quote line inside the row's anchor ranges      B README row: status enum, no redirect words
C receipts/ paths cited by the entry exist at BASE  D indented code block occurs verbatim in a pin
E uncited registry rows byte-identical to BASE      F a row added at REV shares no URL with any row
"""
import importlib.util
import re
import sys

SPEC = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r46-input-device-entry.py"
spec = importlib.util.spec_from_file_location("ctr", SPEC)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
FREEZE = "8c5434c60e03f147ee1f75ab195e8bc3f0db4dec"


def ids_of(text):
    out = []
    fenced = False
    for k, l in enumerate(text.splitlines()):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced = not fenced
            continue
        if fenced and k >= 20:
            continue
        m = c.SRC_RE.match(l)
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


def gates(lesson):
    g = {}
    for line in c.unfenced("\n".join(c.section(lesson, "## Gate"))):
        m = c.GATE_RE.match(line.rstrip("\n"))
        if m:
            g[m.group(1)] = m.groups()[1:]
    return g


def check(repo, rev, base):
    text = c.show(repo, rev, c.ENTRIES[0]).decode()
    reg = c.registry(c.show(repo, rev, "corpus/SOURCES.md"))
    regb = c.registry(c.show(repo, base, "corpus/SOURCES.md"))
    lesson = c.show(repo, rev, c.LESSON).decode()
    readme = c.show(repo, rev, "corpus/README.md").decode()
    ids, gl = ids_of(text), gates(lesson)
    res, why = {}, []

    # A: the gate quote's receipt line sits inside one of the row's anchor ranges
    okA = True
    for i in ids:
        row = reg.get(i, [[]])[0]
        g = gl.get(i)
        if len(row) != 11 or g is None:
            okA = False
            continue
        rb = g[0].split("/")[-1]
        at = c.quote_at(c.show(repo, rev, g[0]), re.sub(r"\s+", " ", g[2]))
        rng = [(int(a), int(b or a)) for a, b in
               re.findall(r"%s:(\d+)(?:-(\d+))?" % re.escape(rb), row[5])]
        if at is None or not any(a <= at <= b for a, b in rng):
            okA = False
            why.append("A:%s at=%s ranges=%s" % (i, at, rng))
    res["A"] = okA

    # B: README index row carries a status token, not a redirect
    rows = [l for l in c.unfenced(readme)
            if re.match(r"^\| `knowledge/%s`" % re.escape(c.ENTRIES[0].split("/")[-1]), l)]
    okB = len(rows) == 1
    if rows:
        cells = [x.strip() for x in rows[0].strip().strip("|").split("|")]
        okB = (len(cells) == 3 and cells[1].lower() in ("draft", "held", "adopted")
               and not re.search(r"\b(supersed\w*|replac\w*|obsolet\w*|instead|deprecat\w*)\b",
                                 rows[0], re.I))
        if not okB:
            why.append("B:%s" % cells[1][:60])
    res["B"] = okB

    # C: an entry-cited receipts/ path exists at the FREEZE commit with the same bytes
    okC = True
    for l in c.unfenced(text):
        for p in re.findall(r"(?<![\w.-])(\.ufo/waves/round-\d+/receipts/[A-Za-z0-9._-]+)", l):
            if c.show(repo, FREEZE, p) != c.show(repo, rev, p):
                okC = False
                why.append("C:%s" % p)
    res["C"] = okC

    # D: an indented (4-space) code run occurs verbatim in a pin, as T3 requires of fences
    pins = " ".join(re.sub(r"\s+", " ", (c.show(repo, rev, c.FETCH + p) or b"").decode(
        "utf-8", "replace")) for p in sorted(c.PINS))
    runs, cur = [], []
    for line in text.splitlines():
        if re.match(r"^    \S", line):
            cur.append(line)
        elif cur:
            runs.append("\n".join(cur))
            cur = []
    if cur:
        runs.append("\n".join(cur))
    bad = [r for r in runs if re.sub(r"\s+", " ", r).strip() not in pins]
    res["D"] = not bad
    if bad:
        why.append("D:%s" % bad[0].splitlines()[0].strip()[:50])

    # E: a registry row the entry never cites is unchanged from BASE
    okE = True
    for i, rr in reg.items():
        if i in ids:
            continue
        if regb.get(i) != rr:
            okE = False
            why.append("E:%s" % i)
    res["E"] = okE

    # F: every registry row born at REV is cited by the entry (no orphan rows)
    okF = True
    urls = {}
    for i, rr in reg.items():
        for r in rr:
            if len(r) == 11 and r[1].split():
                urls.setdefault(r[1].split()[-1].split("#")[0], set()).add(i)
    for i in reg:
        if i not in regb and i not in ids:
            okF = False
            why.append("F:orphan=%s" % i)
    res["F"] = okF

    # G: every surface is cited on a numbered chain step (prose), not on a bare index bullet
    body = [(k, l) for k, l in enumerate(c.unfenced(text)) if k >= 20]
    steps = [l for _, l in body if re.match(r"^\d+\.\s", l)]
    okG = len(steps) >= 5
    for rname, anchor, kw, label in c.SURFACES:
        blob = (c.show(repo, rev, c.FETCH + rname) or b"").decode("utf-8", "replace").split("\n")
        hits = [n for n, l in enumerate(blob, 1) if anchor in l]
        if len(hits) != 1:
            okG = False
            continue
        L = hits[0]
        pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
        found = any(re.match(r"^\d+\.\s", l) and re.search(kw, l, re.I)
                    and any(int(a) <= L <= int(b or a) and int(b or a) - int(a) <= c.JWIDTH
                            for a, b in pat.findall(l))
                    for _, l in body)
        if not found:
            okG = False
            why.append("G:%s" % label)
    res["G"] = okG
    dup = sorted({tuple(sorted(v)) for v in urls.values() if len(v) > 1})
    why.append("dup_url_groups=%d" % len(dup))
    return res, why


def main():
    repo, revs = sys.argv[1], sys.argv[2:]
    base = c.BASE_DEFAULT
    for rev in revs:
        r = c.resolve(repo, rev)
        res, why = check(repo, r, base)
        print("%s %s %s" % (r[:12], " ".join("%s=%d" % (k, int(v)) for k, v in sorted(res.items())),
                            "PASS" if all(res.values()) else "FAIL"))
        for w in why[:4]:
            print("   %s" % w)


if __name__ == "__main__":
    main()
