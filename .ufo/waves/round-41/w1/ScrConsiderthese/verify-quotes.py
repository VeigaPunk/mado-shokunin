#!/usr/bin/env python3
"""Verify every quote this seat lifted: <=25 words, located at file:line, present in the
source line, and present in the seat's own artifacts (proposal.md, and the seat report).
Read-only. Writes quotes-receipt.txt beside itself."""
import pathlib, re, sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SEAT = LANE / ".ufo/waves/round-41/w1/ScrConsiderthese"
ARTIFACTS = [SEAT / "proposal.md", LANE / ".ufo/waves/round-41/w1/ScrConsiderthese.md"]

Q = [
    (1, "considerthese/2026-10-25.md", 5,
     "In this window `corpus/knowledge/` gained eight entries"),
    (2, "considerthese/2026-10-25.md", 50,
     "everything else is relayed from spot-checks"),
    (3, "considerthese/2026-10-25.md", 50,
     "I could pick one cited source line each day and re-open it."),
    (4, "considerthese/2026-10-25.md", 7,
     "What landed after the last reflection"),
    (5, "corpus/lessons/round-33.md", 28,
     "proposal 5 (verify one cited fact first-hand) was"),
    (6, "corpus/lessons/round-40.md", 146,
     "Count dead attempts and dirty closures from the watchdog digests"),
    (7, "corpus/lessons/round-39.md", 82,
     "is served by C1's re-registration"),
    (8, "corpus/lessons/round-38.md", 4,
     "v3 re-grounding counter discriminating the round-37 v2 cribs"),
    (9, "corpus/QUALITY.md", 367,
     "Every round report states the lane's last-30-commit domain-versus-meta ratio with its command"),
    (10, "corpus/lessons/round-32-verifier-spotcheck.md", 35,
     "TARGET MET on junk"),
    (11, "corpus/lessons/round-40.md", 166,
     "the proposals 1 and 3-6 of the same file stay open"),
    (12, "considerthese/2026-10-25.md", 38,
     "8 knowledge entries"),
]

art = {p: p.read_text() for p in ARTIFACTS if p.exists()}
out, ok = [], 0
for n, rel, lineno, quote in Q:
    src = (LANE / rel).read_text().splitlines()
    words = len(quote.split())
    in_src = lineno <= len(src) and quote in src[lineno - 1]
    where = [str(p.relative_to(LANE)) for p, t in art.items() if quote in t]
    good = words <= 25 and in_src and bool(where)
    ok += good
    line = (f"Q{n} {'PASS' if good else 'FAIL'} words={words} at={rel}:{lineno} "
            f"in_source_line={in_src} in_artifacts={where or 'NONE'} :: {quote}")
    out.append(line)
    print(line)
tail = f"MADO_QUOTES: passed={ok}/{len(Q)}"
out.append(tail)
print(tail)
(SEAT / "quotes-receipt.txt").write_text("\n".join(out) + "\n")
sys.exit(0 if ok == len(Q) else 1)
