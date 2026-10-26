#!/usr/bin/env python3
"""Verify every quote used in findings.md against the receipt that carries it.

Each ledger entry is (file, line, quote). The check is: after collapsing runs of whitespace, the
quote is a substring of that physical line of that file (or of the joined `line`..`line+1` window
for the two quotes that legitimately span two source lines, marked span=2). Quotes are <= 25 words.

Files are addressed relative to the lane root passed as argv[1] (default: lane root of this seat).
"""
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/mado-shokunin"
W1 = ROOT + "/.ufo/waves/round-43/w1"
FETCH = ROOT + "/.ufo/waves/round-43/fetch"
REC = ROOT + "/.ufo/waves/round-43/receipts"

# (path, line, quote, span)
LEDGER = [
    (FETCH + "/Hyprland-RegexMatchEngine.cpp", 16,
     "return re2::RE2::FullMatch(other, *m_regex) != m_negative;", 1),
    (FETCH + "/Hyprland-RegexMatchEngine.cpp", 9,
     "m_regex    = makeUnique<re2::RE2>(regex.substr(9));", 1),
    (FETCH + "/Hyprland-RegexMatchEngine.cpp", 12,
     "m_regex = makeUnique<re2::RE2>(regex);", 1),
    (FETCH + "/Hyprland-DefaultFloatingAlgorithm.cpp", 49,
     "if (target->window() && target->window()->m_firstMap) {", 1),
    (FETCH + "/Hyprland-DefaultFloatingAlgorithm.cpp", 56,
     "const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);", 1),
    (FETCH + "/Hyprland-WindowTarget.cpp", 70,
     "if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) {", 1),
    (FETCH + "/Hyprland-WindowTarget.cpp", 71,
     "m_window->setBox(m_box.logicalBox);", 1),
    (FETCH + "/Hyprland-WindowTarget.cpp", 281,
     "bool CWindowTarget::floating() {", 1),
    (FETCH + "/Hyprland-WindowTarget.cpp", 197,
     "if (isPseudo() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) {", 1),
    (FETCH + "/Hyprland-WindowTarget.cpp", 215,
     "calcSize   = m_pseudoSize;", 1),
    (FETCH + "/Hyprland-Target.cpp", 10,
     "void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {", 1),
    (FETCH + "/Hyprland-Target.cpp", 11, "m_box = box;", 1),
    (FETCH + "/Hyprland-Target.cpp", 94, "m_pseudoSize = size;", 1),
    (FETCH + "/Hyprland-GeometricMovableAnimated.cpp", 19,
     "case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();", 1),
    (FETCH + "/Hyprland-GeometricMovableAnimated.cpp", 20,
     "case IGeometric::GEOMETRIC_CURRENT: return m_realSize->value();", 1),
    (FETCH + "/Hyprland-WindowRuleApplicator.cpp", 426, "static_.size = expr;", 1),
    (FETCH + "/Hyprland-WindowRuleApplicator.cpp", 424, "static_.size.reset();", 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 427,
     "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x),", 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 428,
     "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID,", 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 429,
     'escapeJSONStrings(!w->m_workspace ? "" : w->m_workspace->m_name),', 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 448,
     "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y),", 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 1111,
     "if (Config::mgr()->type() != Config::CONFIG_LUA)", 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 1112,
     'return "eval is only supported with the lua config manager";', 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 1119,
     'auto err = luaMgr->eval(code, request.starts_with("repl "));', 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 2042,
     'registerCommand(SHyprCtlCommand{"eval", false, evalRequest});', 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 2043,
     'registerCommand(SHyprCtlCommand{"repl", false, evalRequest});', 1),
    (FETCH + "/Hyprland-HyprCtl.cpp", 2054,
     "SP<SHyprCtlCommand> CHyprCtl::registerCommand(SHyprCtlCommand cmd) {", 1),
    (W1 + "/ExecGoalVsValue/pins/window.cpp", 2079, "m_firstMap      = true;", 1),
    (W1 + "/ExecGoalVsValue/pins/window.cpp", 2402, "if (m_ruleApplicator->static_.size) {", 1),
    (W1 + "/ExecGoalVsValue/pins/window.cpp", 2403,
     "const auto COMPUTED = calculateExpression(*m_ruleApplicator->static_.size);", 1),
    (W1 + "/ExecGoalVsValue/pins/window.cpp", 2408, "m_target->setPseudoSize(*COMPUTED);", 1),
    (W1 + "/ExecGoalVsValue/pins/omarchy-looknfeel-80-96.txt", 17,
     "animation = windowsIn, 1, 4.1, easeOutQuint, popin 87%", 1),
    (W1 + "/ExecGoalVsValue/pins/host-config-chain.txt", 34,
     "source = ~/.config/hypr/gkeep.conf", 1),
    (FETCH + "/host-gkeep.conf", 2,
     "windowrule = float on, match:class ^(org.omarchy.gkeep)$", 1),
    (FETCH + "/host-gkeep.conf", 3,
     "windowrule = center on, match:class ^(org.omarchy.gkeep)$", 1),
    (FETCH + "/host-gkeep.conf", 4,
     "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$", 1),
    (FETCH + "/host-gkeep.conf", 1, "No floating-window tag", 1),
    (FETCH + "/host-clients-r43.json", 50, '"class": "chromium",', 1),
    (FETCH + "/host-clients-r43.json", 51, '"floating": false,', 1),
    (FETCH + "/gkeep-ui-excerpt.py", 6, 'application_id="org.omarchy.gkeep",', 1),
    (FETCH + "/gkeep-ui-excerpt.py", 31,
     'window = Gtk.ApplicationWindow(application=self, title="gkeep")', 1),
    (FETCH + "/gkeep-ui-excerpt.py", 33, "window.set_default_size(420, 500)", 1),
    (FETCH + "/gkeep-ui-excerpt.py", 34, "self.board = Board(window)", 1),
    (W1 + "/ExecOracleGkeep/10-cases.txt", 2,
     "size=[420, 500] floating=True", 1),
    (W1 + "/ExecOracleGkeep/10-cases.txt", 6,
     "nofloat      rules=rules-nofloat.conf   err=None size=[918, 498] floating=False", 1),
    (W1 + "/ExecOracleGkeep/10-cases.txt", 10,
     "floatonly    rules=rules-floatonly.conf err=None size=[200, 200] floating=True", 1),
    (W1 + "/ExecOracleGkeep/10-cases.txt", 7,
     "size300      rules=rules-size300.conf   err=None size=[300, 300] floating=True", 1),
    (W1 + "/ExecOracleGkeep/20-observation.txt", 7, '"size": [420, 500]', 1),
    (W1 + "/ExecOracleGkeep/20-observation.txt", 7, '"floating": true', 1),
    (W1 + "/ExecOracleGkeep/40-monitor-requirement.txt", 2,
     "# Hyprland 0.56.2 never keeps an output, so mapWindow aborts and `clients -j` stays empty.", 1),
    (REC + "/live-geometry-host.txt", 10, "verdict=NO_MATCHING_CLIENT", 1),
    (REC + "/live-geometry-host.txt", 11, "exit=3", 1),
    (ROOT + "/quality/counters/c2-r43-gkeep-entry-v2.py", 357,
     "def host_census(new_ids, reg_rev, gates, receipts_raw, lines):", 1),
]

FAILS = 0
for path, line, quote, span in LEDGER:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    window = "\n".join(lines[line - 1:line - 1 + span])
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    ok = norm(quote) in norm(window)
    words = len(quote.split())
    status = "PASS" if ok else "FAIL"
    if not ok:
        FAILS += 1
    if words > 25:
        status += " (quote>25w)"
        FAILS += 1
    short = path.split("/mado-shokunin/")[-1]
    print(f"{status} {short}:{line}"
          f"{'-' + str(line + span - 1) if span > 1 else ''} ({words}w) {quote[:70]!r}")

with open(FETCH + "/Hyprland-HyprCtl.cpp", "r", encoding="utf-8") as fh:
    body = fh.read()
n = body.count("GEOMETRIC_CURRENT")
print(f"{'PASS' if n == 0 else 'FAIL'} GEOMETRIC_CURRENT occurrences in Hyprland-HyprCtl.cpp = {n}")
if n != 0:
    FAILS += 1

print(f"quotes={len(LEDGER)} fails={FAILS}")
print("VERIFY:", "PASS" if FAILS == 0 else "FAIL")
sys.exit(0 if FAILS == 0 else 1)
