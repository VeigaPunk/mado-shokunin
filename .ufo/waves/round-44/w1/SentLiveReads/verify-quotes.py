#!/usr/bin/env python3
"""Verify every quote this seat lifted from a source: it must occur on the cited line of the cited
file, and be <= 25 words. Locators are recomputed here (the cited line is checked, never trusted).

    python3 -I verify-quotes.py            # -> QUOTES: n/n verified
"""
import os
import sys

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge"
R43 = L + "/.ufo/waves/round-43/fetch"

QUOTES = [
    ("SKILL.md", L, 332, "for length/tags, never window titles"),
    ("SKILL.md", L, 296, "the match is Python `re.fullmatch`, which backtracks"),
    ("SKILL.md", L, 297, "an alternation under a repeat"),
    ("SKILL.md", L, 300, "treat exit 124 as"),
    ("SKILL.md", L, 315, "Read-verb whitelist."),
    ("Hyprland-HyprCtl.cpp", R43, 403, '"title": "{}"'),
    ("Hyprland-HyprCtl.cpp", R43, 430, "w->getPID()"),
    ("Hyprland-HyprCtl.cpp", R43, 1667, "Config::mgr()->getConfigValue(curitem)"),
    ("Hyprland-HyprCtl.cpp", R43, 2042, '{"eval", false, evalRequest}'),
    ("Hyprland-HyprCtl.cpp", R43, 2043, '{"repl"'),
    ("Hyprland-HyprCtl.cpp", R43, 2026, '"reloadshaders"'),
    ("Hyprland-HyprCtl.cpp", R43, 2117, "if (request.starts_with(cmd->name))"),
    ("Hyprland-HyprCtl.cpp", R43, 1312, "request.substr(9)"),
    ("tools/mado-tripwire.py", L, 255, "HYPRCTL_MUTATE"),
    ("tools/mado-tripwire.py", L, 258, '"eval"'),
    ("tools/mado-tripwire.py", L, 259, '{"-i", "--instance"}'),
    ("tools/mado-tripwire.py", L, 1246, '"--batch" in args'),
    ("quality/counters/c2-r44-gkeep-size-request.py", L, 75, "exactly one `recheck:`"),
    ("quality/counters/c1-r42-geometry.py", L, 453, "if got != want_out:"),
    (".ufo/waves/round-44/w1/ExecLiveHost/build-live-states.py", L, 22, "TIMEOUT = 30"),
    (".ufo/waves/round-44/w1/ExecLiveHost/build-live-states.py", L, 37, "timeout=TIMEOUT"),
    ("corpus/knowledge/theme-route-r18.md", L, 3,
     "no omarchy-*, omarchy theme, swaybg, pkill, pgrep, hyprctl, pacman, systemctl or live probe"),
    ("corpus/knowledge/idle-lock-route-r17.md", L, 3, "systemctl, hyprctl, loginctl, journalctl"),
    ("gkeep-client-size-request-r12.md", PKG, 13, "run `hyprctl clients -j`"),
    ("gkeep-client-size-request-r12.md", PKG, 66,
     "observation remains a single `hyprctl clients -j` reading"),
]


def line_of(path, n):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for k, line in enumerate(fh, 1):
            if k == n:
                return line
    return None


bad = 0
for name, root, n, quote in QUOTES:
    path = os.path.join(root, name)
    words = len(quote.split())
    line = line_of(path, n)
    ok = line is not None and quote in line and words <= 25
    if not ok:
        bad += 1
        print("FAIL %s:%d words=%d quote=%r line=%r" % (name, n, words, quote,
                                                        (line or "")[:160]))
print("QUOTES: %d/%d verified" % (len(QUOTES) - bad, len(QUOTES)))
sys.exit(0 if not bad else 1)
