#!/usr/bin/env python3
"""Verify every prose quote in corrections.md: <=25 words, at its computed locator, and present in a receipt.

Run from the lane root:  python3 .ufo/waves/round-50/w1/ScrCorrectionsR50/check-quotes.py
Exit 0 = all pass. Read-only: git show for one committed-revision locator, plain reads otherwise.
"""
import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[5]  # .../mado-shokunin
SEAT = pathlib.Path(__file__).resolve().parent
RECEIPTS = sorted((SEAT / "receipts").glob("*.txt"))
CORRECTIONS = SEAT / "corrections.md"

# (locator path or "<rev>:<path>", expected line number, quote)
QUOTES = [
    (".ufo/waves/round-49/registration.md", 22,
     "agrees with the judge on 57,865 random (keymap, keysym) pairs over 400 random RMLVO keymaps (L1 run)."),
    (".ufo/waves/round-49/w1/ExecRefKeysymB.md", 51, "24898 comparisons, 0 mismatched."),
    ("corpus/lessons/round-49.md", 26,
     "the non-author closure samples from the 2 drafted admits and 4 rejects above"),
    (".ufo/waves/round-49/w1/ScrRows/gate.md", 23,
     "REJECT `https://wiki.hypr.land/0.56.0/Configuring/Basics/Binds/`"),
    (".ufo/waves/round-49/w1/ExecControlsC1.md", 3, "status: complete 2026-10-27T02:57-03:00."),
    ("corpus/lessons/round-49-verifier-spotcheck.md", 27, "filed with 7 w1 seats unsettled"),
    (".ufo/waves/round-49/w1/ExecSessionTriage/ExecSessionTriage.md", 8,
     "triage every finding of the session-material gate at the base, both scopes"),
    (".ufo/waves/round-49/w1/SentPrivacy/report.md", 17, "The live instance already exists."),
    (".ufo/waves/round-49/w1/CritPremiseC2.md", 5,
     "Detailed counterexample, evidence, impacted axes, source hashes/locators, and smallest safe correction"),
    ("dd2e827e:.ufo/waves/round-49/w1/ExecControlsC1.md", 3, "status: running 2026-10-27T01:56-03:00"),
]


def line_at(locator: str, n: int) -> str:
    if ":" in locator and not locator.startswith(".") and not locator.startswith("c"):
        rev, path = locator.split(":", 1)
        out = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{path}"],
                             capture_output=True, text=True, check=True).stdout.splitlines()
        return out[n - 1]
    return (LANE / locator).read_text(encoding="utf-8").splitlines()[n - 1]


def main() -> int:
    receipts = {p.name: p.read_text(encoding="utf-8", errors="replace") for p in RECEIPTS}
    # quotes may wrap across lines in the prose; compare on normalized whitespace
    corrections = " ".join(CORRECTIONS.read_text(encoding="utf-8").split())
    failures = 0
    for locator, n, text in QUOTES:
        words = len(text.split())
        line = line_at(locator, n)
        at_line = text in line
        in_receipt = [name for name, body in receipts.items() if text in body]
        in_corr = text in corrections
        ok = words <= 25 and at_line and in_receipt and in_corr
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} words={words:2d} line={n:3d} at_line={int(at_line)} "
              f"receipts={','.join(in_receipt) or '-'} corrections={int(in_corr)} {locator}")
        if not ok:
            print(f"      quote: {text!r}")
            print(f"      source: {line[:160]!r}")
    print(f"QUOTE_CHECK checked={len(QUOTES)} failed={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
