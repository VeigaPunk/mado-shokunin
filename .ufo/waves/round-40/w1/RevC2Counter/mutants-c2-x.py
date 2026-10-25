#!/usr/bin/env python3
"""Seat RevC2Counter-2: NEW mutants of the admitted C2 fixture, scored by the
frozen counter quality/counters/c2-r40-forms-entry.py (PRED-C2-r40-v1) at
5e7e88525cc539563de7746361b2650802e81809.

Fixture construction and scoring machinery are imported from the frozen
controls harness (.ufo/waves/round-40/ctl/run-c2-controls.py), so every
fixture repo is mktemp -d, git init -q, toplevel verified equal before the
first commit, throwaway identity passed with -c, and the counter runs with
python3 -I over revision-addressed reads. Nothing in the lane is written.
None of these mutants overlap the 20 shipped ones (N01..N20).
"""
import importlib.util
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CTL_PATH = os.path.join(LANE, ".ufo", "waves", "round-40", "ctl",
                        "run-c2-controls.py")
spec = importlib.util.spec_from_file_location("c2ctl", CTL_PATH)
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)

SRC = "corpus/SOURCES.md"
LES = "corpus/lessons/round-40.md"
ENTRY = ctl.ENTRY
NAME = os.path.basename(ENTRY)
S301 = ".ufo/waves/round-40/fetch/S301.html"
S302 = ".ufo/waves/round-40/fetch/S302.receipt.txt"
S303 = ".ufo/waves/round-40/fetch/S303.txt"

base = ctl.good()
G = ctl.after(base)

muts = {}


def mut(name, expect, fn):
    g = dict(G)
    fn(g)
    muts[name] = (expect, g)


# --- Wrong-pass candidates -------------------------------------------------

def x1(g):  # tool sha present but not on a line of its own
    t = g[S302].replace("tool sha256 %s\n" % ctl.sha(ctl.TOOL_SRC), "")
    t = t.replace("live getoption census over the host tree",
                  "live getoption census over the host tree "
                  "(tool sha256 %s)" % ctl.sha(ctl.TOOL_SRC))
    g[S302] = t
    g[LES] = g[LES].replace(ctl.sha(ctl.receipt_a()), ctl.sha(t))


mut("X01-sha-not-own-line", "PASS", x1)


def x3(g):  # count lines embedded mid-sentence, no standalone lines in entry
    prose = ("The census reported %s across the host tree, and %s."
             % (ctl.FORMS_LINE, ctl.LABELS_LINE))
    g[ENTRY] = g[ENTRY].replace(
        ctl.FORMS_LINE + "\n" + ctl.LABELS_LINE + "\n", prose + "\n")


mut("X03-counts-in-prose-line", "PASS", x3)


def x5(g):  # used-by merely contains the entry as a substring
    g[SRC] = g[SRC].replace(
        ctl.row("S301", "https://example.org/a.hpp"),
        ctl.row("S301", "https://example.org/a.hpp",
                used=ENTRY + ".draft-copy.md"))


mut("X05-usedby-longer-path", "PASS", x5)


def x7(g):  # the only index row sits inside a code fence
    g["corpus/README.md"] = base["corpus/README.md"] + \
        "```\n| `knowledge/%s` | new |\n```\n" % NAME


mut("X07-index-row-in-fence", "PASS", x7)


def x11(g):  # every GATE line indented by two spaces
    g[LES] = "\n".join(
        "  " + l if l.startswith("GATE ") else l
        for l in g[LES].splitlines()) + "\n"


mut("X11-gate-lines-indented", "PASS", x11)


def x13(g):  # stale gate line for S303 precedes the valid one
    bad = ('GATE S303 receipt=.ufo/waves/round-39/fetch/S303.txt sha256=%s '
           'quote="%s"' % ("0" * 64, ctl.QC))
    g[LES] = g[LES].replace(
        "GATE S303 receipt=.ufo/waves/round-40/fetch/S303.txt",
        bad + "\nGATE S303 receipt=.ufo/waves/round-40/fetch/S303.txt")


mut("X13-dual-gate-second-valid", "PASS", x13)

# --- Expected-correct rejects (coverage the shipped 20 do not have) --------


def x2(g):  # receipt count lines with doubled internal spacing
    t = ctl.receipt_a().replace(
        ctl.FORMS_LINE, "forms int=44  float=5  str=8  custom=13").replace(
        ctl.LABELS_LINE,
        "labels agreement=62  agreement*=8  mismatch=0  config-only=0  "
        "live-default=0")
    g[S302] = t
    g[LES] = g[LES].replace(ctl.sha(ctl.receipt_a()), ctl.sha(t))


mut("X02-receipt-spacing-differs", "FAIL", x2)


def x4(g):  # two own-work new rows
    g[SRC] = g[SRC].replace(ctl.row("S301", "https://example.org/a.hpp"),
                            ctl.row("S301", "https://example.org/a.hpp",
                                    kind="own-work"))


mut("X04-two-own-work-rows", "FAIL", x4)


def x6(g):  # gate quote of two words (below the 3-word floor)
    q2 = "handlers gradients"
    g[S303] = q2
    g[LES] = g[LES].replace(ctl.sha(ctl.RECEIPT_C), ctl.sha(q2)).replace(
        '"%s"' % ctl.QC, '"%s"' % q2)
    g[ENTRY] = g[ENTRY].replace("**OBS** S303 %s." % ctl.QC,
                                "**OBS** S303 %s." % q2)


mut("X06-quote-two-words", "FAIL", x6)


def x8(g):  # new row's location collides with the HELD row's location
    g[SRC] = g[SRC].replace(
        ctl.row("S303", "https://example.org/c.cpp"),
        ctl.row("S303", "https://example.org/config.cpp"))


mut("X08-location-collides-held", "FAIL", x8)


def x9(g):  # quote occurs only inside a <script> block (stripped by norm)
    r = ("<html><body><script>if pgrep -x hypridle >/dev/null; then echo "
         "idle disabled</script></body></html>")
    g[S301] = r
    g[LES] = g[LES].replace(ctl.sha(ctl.RECEIPT_B), ctl.sha(r))


mut("X09-quote-only-in-script", "FAIL", x9)


def x10(g):  # recheck value `on-` followed by digits
    g[ENTRY] = g[ENTRY].replace("recheck: 90d", "recheck: on-2026-10-25")


mut("X10-recheck-on-date", "FAIL", x10)


def x12(g):  # legit index row plus a fenced duplicate (fence-blindness, 2 hits)
    g["corpus/README.md"] += ("Quoted below:\n\n```\n| `knowledge/%s` | new |"
                              "\n```\n" % NAME)


mut("X12-second-index-row-in-fence", "FAIL", x12)


def x14(g):  # new id carries a stale opened date
    g[SRC] = g[SRC].replace(
        ctl.row("S301", "https://example.org/a.hpp"),
        ctl.row("S301", "https://example.org/a.hpp", opened="2026-10-24"))


mut("X14-new-id-opened-stale", "FAIL", x14)


def x15(g):  # own-work receipt saved with CRLF line endings
    t = g[S302].replace("\n", "\r\n")
    g[S302] = t
    g[LES] = g[LES].replace(ctl.sha(ctl.receipt_a()), ctl.sha(t))


mut("X15-receipt-crlf", "FAIL", x15)


def main():
    rc, last = ctl.score(base, G, "baseline")
    print("baseline admitted-state expected=admitted=1/1 observed=%s rc=%d"
          % (last.split(" rev=")[0], rc))
    hits = 0
    for name, (expect, g) in sorted(muts.items()):
        rc, last = ctl.score(base, g, name)
        passed = rc == 0 and "admitted=1/1" in last
        obs = "PASS" if passed else "FAIL"
        ok = obs == expect
        hits += ok
        print("mutant=%s expected=%s observed=%s clauses=%s verdict=%s "
              "match=%d" % (name, expect, obs, ctl.score.clauses,
                            last.split(" rev=")[0].split(": ")[-1], ok))
    print("REV-X: mutants=%d expectations-met=%d/%d"
          % (len(muts), hits, len(muts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
