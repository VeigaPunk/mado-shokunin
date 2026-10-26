#!/usr/bin/env python3
"""verify-quotes.py — every quote in SentLiveRun.md checked against its computed locator.

Each entry is (path relative to the lane root, first line, last line, exact substring). The
lines are read from the lane file, whitespace-joined across the range, and the substring must
appear in the join. Locators were computed with `grep -n`, never typed. A quote is rejected
when it is longer than 25 words.

usage: python3 verify-quotes.py [--repo /home/vgpnk/Projects/shokunin/mado-shokunin]
"""
import argparse, os, sys

REPO_DEFAULT = "/home/vgpnk/Projects/shokunin/mado-shokunin"
HERE = os.path.dirname(os.path.abspath(__file__))

Q = [
    ("SKILL.md", 225, 225, "clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT"),
    ("SKILL.md", 293, 294,
     "Host run 2026-10-26, no gkeep window open: the gkeep rule file declares `size 420 500` and the dump holds four tiled clients, so nothing matches."),
    ("SKILL.md", 299, 299, "clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT"),
    ("SKILL.md", 305, 307,
     "A rule regex inside the accepted alphabet with an alternation under a repeat, such as `(a|aa)+$`, makes the tool hang on a long class string"),
    ("SKILL.md", 309, 309, "timeout 5 python3 tools/mado-geometry.py"),
    (".ufo/waves/round-43/receipts/live-geometry-host.txt", 10, 10,
     "clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT"),
    (".ufo/waves/round-44/receipts/live-geometry-host-r44.txt", 1, 1,
     "tool sha256 1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4"),
    (".ufo/waves/round-44/receipts/live-geometry-host-r44.txt", 5, 5,
     "clients=3 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT"),
    (".ufo/waves/round-44/fetch-c1/Hyprland-HyprCtl.cpp", 431, 431, "getFullscreenModes(w).internal"),
    (".ufo/waves/round-44/fetch-c1/Hyprland-FullscreenController.hpp", 14, 14, "FSMODE_MAXIMIZED,"),
    ("tools/mado-geometry.py", 89, 89, "SAFE = re.compile"),
    ("tools/mado-geometry.py", 200, 200, "def client_fsmode(c):"),
    ("tools/mado-geometry.py", 277, 277, 'states = " maximized=%d fullscreen=%d"'),
    ("PROVINCE.md", 32, 32, "no compositor socket, no Wayland client, no network, no config tree, no process started"),
    (".ufo/waves/round-44/w1/ScrSkillProvince.md", 113, 113, 'names only "an alternation under a repeat"'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=REPO_DEFAULT)
    a = ap.parse_args()
    fails = 0
    lines_out = []
    for path, lo, hi, quote in Q:
        full = os.path.join(a.repo, path)
        try:
            body = open(full, encoding="utf-8", errors="replace").read().splitlines()
            joined = " ".join(body[lo - 1:hi])
        except (OSError, IndexError) as exc:
            lines_out.append("FAIL %s:%d-%d (%s)" % (path, lo, hi, exc))
            fails += 1
            continue
        ok = quote in joined
        if len(quote.split()) > 25:
            ok = False
            lines_out.append("FAIL %s:%d-%d quote longer than 25 words" % (path, lo, hi))
            fails += 1
            continue
        lines_out.append("%s %s:%d-%d  %r" % ("PASS" if ok else "FAIL", path, lo, hi, quote[:70]))
        if not ok:
            fails += 1
    summary = "VERIFY_QUOTES: %s (%d of %d verified)" % ("PASS" if not fails else "FAIL",
                                                        len(Q) - fails, len(Q))
    lines_out.append(summary)
    text = "\n".join(lines_out) + "\n"
    open(os.path.join(HERE, "verify-quotes.out"), "w").write(text)
    print(text, end="")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
