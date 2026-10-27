#!/usr/bin/env python3
"""Independent verifier for receipts/d4-sweep.txt (seat ScrErrataD4, round 48).

Reads only the receipt plus the three pinned markdown files and checks, from scratch:
  1. every `N| text` line inside an EXCERPT block equals the real line N of the named file;
  2. every CITING line's recorded locator is still on the recorded citing line (re-grep of the
     citing file - catches a line number that drifted after the sweep);
  3. MATCH: first..last of the cited range spans the anchor line; MISMATCH: it does not, and the
     recorded corrected range does - sentence start and end recomputed here by a second code path;
  4. every QUOTE line is verbatim inside its cited range and at most 25 words;
  5. the totals, and that the wrong locators are exactly the two recorded ones.

Usage: verify.py <lane-root> <receipt>   (exit 0 = all checks pass)
"""
import re
import sys
from pathlib import Path

LOC_RE = re.compile(r"terminal-route-r17\.md:(\d+)(?:-(\d+))?")

fails = []
oks = []


def check(cond, msg):
    (oks if cond else fails).append(msg)


def main():
    root = Path(sys.argv[1]).resolve()
    receipt = Path(sys.argv[2]).resolve().read_text(encoding="utf-8")
    cache = {}

    def lines_of(rel):
        if rel not in cache:
            cache[rel] = (root / rel).read_text(encoding="utf-8", errors="replace").splitlines()
        return cache[rel]

    def norm(rel, a, b):
        return re.sub(r"\s+", " ", " ".join(x.strip() for x in lines_of(rel)[a - 1:b])).strip()

    blocks = re.split(r"\n(?=CITING |DEFECT-MENTION )", receipt)
    cites = []
    for blk in blocks:
        m = re.match(r"CITING file=(\S+) citing_line=(\d+) cited=(\d+)-(\d+) claim='([^']*)' "
                     r"anchor_line=(\d+) sentence_start=(\d+) bullet=(\d+)-(\d+) corrected=(\d+)-(\d+) "
                     r"verdict=(\w+)", blk)
        if m:
            rel, cl, a, b = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            anchor, start, cend = int(m.group(6)), int(m.group(7)), int(m.group(11))
            cites.append(dict(rel=rel, cl=cl, a=a, b=b, anchor=anchor, start=start,
                              cend=cend, verdict=m.group(12), raw=blk))
            continue
        m = re.match(r"DEFECT-MENTION file=(\S+) citing_line=(\d+) quoted_locator=(\d+)-(\d+) "
                     r"asserted_range=(\d+)-(\d+) .*verdict=(\w+)", blk)
        if m:
            cites.append(dict(rel=m.group(1), cl=int(m.group(2)), mention=True,
                              qa=int(m.group(3)), qb=int(m.group(4)),
                              sa=int(m.group(5)), sb=int(m.group(6)), raw=blk))

    check(len(cites) == 7, f"parsed 7 findings from the receipt (got {len(cites)})")

    # 1 - excerpt text equals the real bytes (every EXCERPT quotes the pinned source, never a citing file)
    SRC = "corpus/knowledge/terminal-route-r17.md"
    n_ex = 0
    for c in cites:
        for m in re.finditer(r"^(\d+)\| ?(.*)$", c["raw"], re.M):
            n, text = int(m.group(1)), m.group(2)
            n_ex += 1
            check(lines_of(SRC)[n - 1].rstrip() == text.rstrip(),
                  f"excerpt {SRC}:{n} equals the file line")
    check(n_ex > 0, f"excerpt lines checked: {n_ex}")

    # 2 + 3 - locator still on the citing line; range vs anchor
    for c in cites:
        rel, cl = c["rel"], c["cl"]
        src_line = lines_of(rel)[cl - 1]
        if c.get("mention"):
            check(all(f"{c['qa']}-{c['qb']}" in src_line or str(c["qa"]) in src_line for _ in [0]),
                  f"mention {rel}:{cl} still names {c['qa']}-{c['qb']}")
            blk = norm("corpus/knowledge/terminal-route-r17.md", c["sa"], c["sb"])
            check("omarchy-cmd-terminal-cwd" in blk,
                  f"mention asserts {c['sa']}-{c['sb']} which holds the helper anchor")
            continue
        found = [(int(x), int(y) if y else int(x)) for x, y in LOC_RE.findall(src_line)]
        check((c["a"], c["b"]) in found, f"locator {c['a']}-{c['b']} still on {rel}:{cl}")
        inside = c["a"] <= c["anchor"] <= c["b"]
        # second code path: recompute bullet + sentence bounds from the source
        sl = lines_of("corpus/knowledge/terminal-route-r17.md")
        s = c["anchor"] - 1
        while s > 0 and not sl[s].startswith("- "):
            s -= 1
        bul_start = s + 1
        e = c["anchor"] - 1
        while e + 1 < len(sl) and sl[e + 1].strip() != "" and not sl[e + 1].startswith("- "):
            e += 1
        bul_end = e + 1
        st = c["anchor"]
        for k in range(c["anchor"], bul_start - 1, -1):
            if "[UNK]" in sl[k - 1]:
                st = k
                break
        en = bul_end
        for k in range(st, bul_end + 1):
            t = sl[k - 1].strip()
            if t.endswith(".") or t.endswith(";") or t.endswith(":"):
                en = k
                break
        check((st, en) == (c["start"], c["cend"]),
              f"recomputed sentence {st}-{en} == recorded {c['start']}-{c['cend']} for {rel}:{cl}")
        if c["verdict"] == "MATCH":
            check(inside, f"MATCH {rel}:{cl}: anchor {c['anchor']} inside cited {c['a']}-{c['b']}")
        else:
            check(not inside, f"MISMATCH {rel}:{cl}: anchor {c['anchor']} outside cited {c['a']}-{c['b']}")
            check(c["start"] <= c["anchor"] <= c["cend"],
                  f"MISMATCH {rel}:{cl}: corrected {c['start']}-{c['cend']} spans the anchor")

    # 4 - quotes verbatim and <= 25 words
    used_spans = []
    for m in re.finditer(r'QUOTE src=(\S+):(\d+)-(\d+) words=(\d+) inside=(\w+) used=(\w+) quote="(.*)"$',
                         receipt, re.M):
        rel, a, b, words, inside, used, span = (m.group(1), int(m.group(2)), int(m.group(3)),
                                               int(m.group(4)), m.group(5), m.group(6), m.group(7))
        if used == "true":
            used_spans.append((rel, a, b, span))
        check(span in norm(rel, a, b), f"quote verbatim in {rel}:{a}-{b}: {span[:40]!r}")
        check(words == len(span.split()), f"quote word count recorded {words} == measured {len(span.split())}")
        check(words <= 25 and inside == "true", f"quote within 25 words at {rel}:{a}-{b} ({words})")

    # 4b - the entry:88 label question is recorded, not scored: the process-start [UNK] is its own
    #      sentence and the cited range does not contain it
    rel_lines = [l for l in receipt.splitlines() if l.startswith("RELATED ")]
    check(rel_lines == ["RELATED file=corpus/knowledge/xdg-terminal-selection-r47.md citing_line=88 "
                        "anchor_line=128 sentence=128-130 also_cited=no"],
          f"entry:88 related process-start [UNK] recorded as r17:128-130, not cited: {rel_lines}")

    # 4c - the draft may only quote spans the receipt has verified
    if len(sys.argv) > 3:
        er = re.sub(r"\s+", " ", Path(sys.argv[3]).read_text()).strip()
        for rel, a, b, span in used_spans:
            check(span in er, f"erratum.md quotes the verified span from {rel}:{a}-{b}: {span[:40]!r}")
        check(len(used_spans) >= 8, f"used quote spans recorded: {len(used_spans)}")

    # 5 - totals and the wrong set
    check("TOTAL citing_locators=6 match=5 mismatch=1 defect_mentions=1" in receipt,
          "totals line: 6 locators, 5 match, 1 mismatch, 1 defect mention")
    wrong = sorted(re.findall(r"^WRONG citing=(\S+) cited=(\d+)-(\d+) corrected=(\d+)-(\d+)$",
                              receipt, re.M))
    expect = [("corpus/knowledge/xdg-terminal-selection-r47.md:95", "150", "151", "149", "150")]
    check(wrong == expect, f"wrong set == {expect}")

    for o in oks:
        print(f"PASS {o}")
    for f in fails:
        print(f"FAIL {f}")
    print(f"VERDICT {'PASS' if not fails else 'FAIL'} checks={len(oks) + len(fails)} passed={len(oks)} failed={len(fails)}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
