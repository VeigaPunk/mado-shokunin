#!/usr/bin/env python3
"""Generate C1 counter mutants in scratch only. Run with -I.

Each mutant is a full copy of the scored tree (corpus/SOURCES.md, the three
entries, the eight receipts) with gate-quote lines and/or receipt bytes
rewritten in the copy. The frozen spec and the counter are the lane's own,
unmodified.
"""
import re
import shutil
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SCRATCH = LANE / ".ufo/waves/round-35/scratch/RevQuoteWords"
BASE = SCRATCH / "mut"
ENTRIES = {
    "corpus/knowledge/idle-lock-never-asked-r12.md": ["S203", "S204"],
    "corpus/knowledge/idle-lock-chain-armed-r14.md": ["S205"],
    "corpus/knowledge/idle-lock-offered-in-the-bar-r15.md":
        ["S206", "S207", "S208", "S209", "S210"],
}
ALL = [i for ids in ENTRIES.values() for i in ids]


def clone(dst: Path) -> Path:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(BASE, dst)
    return dst


def set_quote(root: Path, sid: str, quote: str) -> None:
    for rel, ids in ENTRIES.items():
        if sid not in ids:
            continue
        p = root / rel
        text = p.read_text()
        pat = re.compile(r"^gate-quote: " + re.escape(sid) + r" .*$", re.M)
        assert len(pat.findall(text)) == 1, (sid, rel)
        p.write_text(pat.sub("gate-quote: " + sid + " " + quote, text, count=1))
        return
    raise SystemExit("unknown sid " + sid)


def receipt(root: Path, sid: str) -> Path:
    return root / ".ufo/waves/round-35/fetch" / f"{sid}.receipt.txt"


def main() -> None:
    # A8: every quote is the bare token `located:`.
    r = clone(SCRATCH / "A8_placeholder_all")
    for sid in ALL:
        set_quote(r, sid, "located:")
    print("A8", r)

    # A1: a single placeholder quote (lower edge of 1..25).
    r = clone(SCRATCH / "A1_placeholder_one")
    set_quote(r, "S203", "located:")
    print("A1", r)

    # B25/C26: append a synthetic single-space run to the receipt copy and quote
    # it, so contiguity holds by construction. 25 must pass, 26 must fail.
    words = ("alpha%02d" % i for i in range(1, 27))
    words = list(words)
    for name, n, path in (("B25_body_25w", 25, SCRATCH / "B25_body_25w"),
                          ("C26_body_26w", 26, SCRATCH / "C26_body_26w")):
        r = clone(path)
        q = " ".join(words[:n])
        rp = receipt(r, "S203")
        rp.write_bytes(rp.read_bytes() + ("\n" + q + "\n").encode())
        set_quote(r, "S203", q)
        print(name, r, "|", q)

    # D: faithful paraphrase, not a substring -> substring test rejects it.
    r = clone(SCRATCH / "D_paraphrase")
    set_quote(r, "S206", "located: the bar opens the idle module on line 207 and clicks toggle idle on 208")
    print("D", r)

    # E: words spliced from two non-adjacent receipt spots -> contiguity rejects.
    r = clone(SCRATCH / "E_noncontig")
    set_quote(r, "S206", "custom/idle-indicator omarchy-toggle-idle")
    print("E", r)

    # H: S205's real located text planted on S206 -> id binding still holds.
    s205 = receipt(r, "S205").read_text().splitlines()
    q = [l for l in s205 if l.startswith("located: ")][0]
    r = clone(SCRATCH / "H_crossid")
    set_quote(r, "S206", q[len("located: "):])
    print("H", r, "|", q)

    # I: a second, well-formed gate-quote line for the same id -> exactly-once.
    r = clone(SCRATCH / "I_duplicate_line")
    p = r / "corpus/knowledge/idle-lock-never-asked-r12.md"
    p.write_text(p.read_text() +
                 "gate-quote: S203 located: install/first-run/ lists 12 scripts\n")
    print("I", r)

    # J: the w1 "shadow" form, no space after the colon.
    r = clone(SCRATCH / "J_shadow")
    p = r / "corpus/knowledge/idle-lock-never-asked-r12.md"
    p.write_text(p.read_text() +
                 "gate-quote:S203 shadow quote for the same id\n")
    print("J", r)

    # K: a data fragment from the receipt probe, 3 words -> proves the clause
    # would accept measurement bytes, which none of the eight delivered quotes do.
    r = clone(SCRATCH / "K_s205_data_3w")
    set_quote(r, "S205", "1667 /usr/bin/hypridle")
    print("K", r)

    # L: a prefix of the located line, 7 words -> partial summary still passes.
    r = clone(SCRATCH / "L_prefix_7w")
    set_quote(r, "S203", "located: install/first-run/ lists 12 scripts")
    print("L", r)

    # M: the registered c1-quote-long shape, rebuilt at 30 words.
    r = clone(SCRATCH / "M_body_30w")
    q = " ".join(words + ["beta%02d" % i for i in range(1, 5)])
    rp = receipt(r, "S203")
    rp.write_bytes(rp.read_bytes() + ("\n" + q + "\n").encode())
    set_quote(r, "S203", q)
    print("M", r, "|", q)

    # G: the receipt itself replaced by a fabricated one-liner, quote rewritten
    # to match. Tests whether the quote is bound to the receipt's real bytes.
    r = clone(SCRATCH / "G_fabricated_receipt")
    fake = ("# S203 receipt — fabricated\n"
            "located: fabricated claim about the host that was never observed\n")
    receipt(r, "S203").write_bytes(fake.encode())
    set_quote(r, "S203", "located: fabricated claim about the host that was never observed")
    print("G", r)


if __name__ == "__main__":
    sys.exit(main())
