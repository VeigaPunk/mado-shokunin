#!/usr/bin/env python3
"""CritAssimV2 quote check: every quote printed in the report is re-found at its
computed locator. Lines were obtained with grep -n (see residue-line-numbers.txt,
landed-locators.txt, axes-and-final.txt); this script re-verifies containment.
Run: python3 quote-check.py > quote-check.txt
"""
import re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge"

def lines(path):
    return open(path, encoding="utf-8", errors="replace").read().split("\n")

# (label, path, line range (1-based inclusive), quote)
CASES = [
    ("r12 sig",       f"{STAGED}/gkeep-client-size-request-r12.md", (24, 24), "void CWindow::sendWindowSize(bool force) {"),
    ("r12 report",    f"{STAGED}/gkeep-client-size-request-r12.md", (26, 26), "const auto REPORTSIZE = realToReportSize();"),
    ("r12 emplace",   f"{STAGED}/gkeep-client-size-request-r12.md", (28, 28), "m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());"),
    ("r12 set_size",  f"{STAGED}/gkeep-client-size-request-r12.md", (31, 31), "xdg_toplevel.set_size"),
    ("r12 adopt",     f"{STAGED}/gkeep-client-size-request-r12.md", (52, 52), "no minimum-size request will adopt the size"),
    ("r12 complete",  f"{STAGED}/gkeep-client-size-request-r12.md", (59, 59), "The chain is now complete on both sides"),
    ("r12 rendered",  f"{STAGED}/gkeep-client-size-request-r12.md", (62, 62), "The rendered geometry of a gkeep window is 420\u00d7500"),
    ("r12 adopt long", f"{STAGED}/gkeep-client-size-request-r12.md", (52, 53), "no minimum-size request will adopt the size"),
    ("r13 cannot subst", f"{STAGED}/gkeep-rendered-geometry-record-r13.md", (39, 39), "it cannot substitute a different number"),
    ("r14 keys",      f"{STAGED}/gkeep-rendered-geometry-record-r14.md", (45, 47), "The keys in its note records are exactly three \u2014 `body`, `created`, `id`"),
    ("r14 both measured", f"{STAGED}/gkeep-rendered-geometry-record-r14.md", (49, 51), "both now measured and both empty on this host"),
    ("r9 fetchClass quote", f"{STAGED}/gkeep-rendered-geometry-chain-r9.md", (31, 31), "return m_xdgSurface->m_toplevel->m_state.appid;"),
    ("r9 rule quote", f"{STAGED}/gkeep-rendered-geometry-chain-r9.md", (39, 39), "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"),
    ("r9 app_id absent", f"{STAGED}/gkeep-rendered-geometry-chain-r9.md", (69, 69), "never mentions `app_id` (0 occurrences in the page)"),
    ("r9 S287 source", f"{STAGED}/gkeep-rendered-geometry-chain-r9.md", (11, 11), "wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules"),
    ("S164 fetchClass", f"{LANE}/.ufo/waves/round-44/fetch/Hyprland-Window.cpp", (1505, 1505), "return m_xdgSurface->m_toplevel->m_state.appid;"),
    ("S164 clamp",    f"{LANE}/.ufo/waves/round-44/fetch/Hyprland-Window.cpp", (2746, 2746), "clampWindowSize(MINSIZE, MAXSIZE"),
    ("S164 map line", f"{LANE}/.ufo/waves/round-44/fetch/Hyprland-Window.cpp", (2515, 2515), "Map request dispatched, monitor {}"),
    ("S164 sendWindowSize", f"{LANE}/.ufo/waves/round-44/fetch/Hyprland-Window.cpp", (1732, 1732), "void CWindow::sendWindowSize(bool force) {"),
    ("S165 size effect", f"{LANE}/.ufo/waves/round-24/fetch/S165.bin", (82, 82), "Resizes a floating window."),
    ("S165 precedence", f"{LANE}/.ufo/waves/round-24/fetch/S165.bin", (318, 318), "the _last_ match takes precedence"),
    ("S295 rule",     f"{LANE}/.ufo/waves/round-43/fetch/host-gkeep.conf", (4, 4), "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"),
    ("entry pins phrase", f"{LANE}/corpus/knowledge/hyprland-gkeep-size-request-r44.md", (40, 40), "outside this entry's pins"),
    ("entry not-among phrase", f"{LANE}/corpus/knowledge/hyprland-gkeep-size-request-r44.md", (79, 79), "not among the pins"),
    ("lesson r13 reason", f"{LANE}/corpus/lessons/round-44.md", (37, 37), "its Window.cpp half is superseded by held S164"),
    ("lesson r14 reason", f"{LANE}/corpus/lessons/round-44.md", (38, 38), "one whole-journal sweep outside this lane carries the entire absence claim"),
    ("lesson r15 flip", f"{LANE}/corpus/lessons/round-44.md", (39, 39), "a lane-committed sweep over this lane's own artifacts reproduces it"),
    ("lesson r9 reason", f"{LANE}/corpus/lessons/round-44.md", (40, 40), "its two distinctive links need the GTK default-size documentation page and the window-rules wiki, neither pinned this round"),
    ("lesson r13 ledger", f"{LANE}/corpus/lessons/round-44.md", (62, 62), "its two `Window.cpp` sources (onAck, the map request log line) are pinned here and are what the successor cites"),
    ("oracle map line", f"{LANE}/.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt", (11, 11), "window size: [420.00000, 500.00000]"),
    ("lesson r9 ledger", f"{LANE}/corpus/lessons/round-44.md", (65, 65), "the successor covers the class-is-app_id link from a pinned file instead"),
    ("gate xdg", f"{LANE}/.ufo/waves/round-44/fetch/xdg-shell.xml", (1149, 1153), "The width and height arguments specify a hint to the window about how its surface should be resized"),
    ("gate gkeep", f"{LANE}/.ufo/waves/round-44/fetch/gkeep-ui.py", (475, 476), "window.set_decorated(False) window.set_default_size(420, 500)"),
]

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

fails = 0
for label, path, (a, b), quote in CASES:
    body = "\n".join(lines(path)[a - 1:b])
    ok = norm(quote) in norm(body)
    print(f"{'PASS' if ok else 'FAIL'} {label} {path.split('/')[-1]}:{a}-{b}")
    fails += 0 if ok else 1
print(f"QUOTE-CHECK: {len(CASES) - fails}/{len(CASES)} passed")
sys.exit(1 if fails else 0)
