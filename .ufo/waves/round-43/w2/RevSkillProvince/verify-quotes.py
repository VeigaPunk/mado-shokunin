#!/usr/bin/env python3
"""verify-quotes.py - RevSkillProvince seat: every quoted fragment in findings.md
must occur in the named source at the named line. Read-only; prints QUOTES: n/n."""
import sys

# (source path, 1-based line, exact fragment that findings.md quotes)
CASES = [
    # F1 fix-text quotes (worktree SKILL.md, post-data addition)
    ("SKILL.md", 290, "Known limit (round-43 wave w1, `RevRefTool` V1): the match is Python `re.fullmatch`, which backtracks."),
    ("SKILL.md", 295, '"no verdict", never as a verdict'),
    # F2 row quote
    ("PROVINCE.md", 32, "at most 1048577 B"),
    # F3 row quote
    ("SKILL.md", 271, "only that there was no size to compare (no `size` value, or not two integers)"),
    # tool docstring / code quotes
    ("tools/mado-geometry.py", 21, "larger than 1048576 bytes is too_large"),
    ("tools/mado-geometry.py", 22, "1048577 bytes"),
    ("tools/mado-geometry.py", 254, "data = stdin.read(MAX_BYTES + 1)"),
    ("tools/mado-geometry.py", 175, "v >= 0 for v in s):"),
    ("tools/mado-geometry.py", 172, "def client_size(c):"),
    ("tools/mado-geometry.py", 261, 'sys.stdout.write("\\n".join(lines) + "\\n")'),
    # Hyprland source quotes (pinned receipts)
    (".ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp", 395, '"size": [{}, {}],'),
    (".ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp", 2007, 'registerCommand(SHyprCtlCommand{"clients", true, clientsRequest});'),
    (".ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp", 427, "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x),"),
    (".ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp", 428, "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y),"),
    (".ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp", 448, "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y),"),
    (".ufo/waves/round-43/fetch/Hyprland-GeometricMovableAnimated.cpp", 19, "case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();"),
    (".ufo/waves/round-43/fetch/Hyprland-GeometricMovableAnimated.cpp", 20, "case IGeometric::GEOMETRIC_CURRENT: return m_realSize->value();"),
    (".ufo/waves/round-43/fetch/Hyprland-DefaultFloatingAlgorithm.cpp", 49, "if (target->window() && target->window()->m_firstMap) {"),
    (".ufo/waves/round-43/fetch/Hyprland-DefaultFloatingAlgorithm.cpp", 55, "if (WINDOW->m_ruleApplicator->static_.size) {"),
    (".ufo/waves/round-43/fetch/Hyprland-DefaultFloatingAlgorithm.cpp", 56, "const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);"),
    (".ufo/waves/round-43/fetch/Hyprland-WindowRuleApplicator.cpp", 422, "const auto& expr = std::get<Math::SExpressionVec2>(value);"),
    (".ufo/waves/round-43/fetch/Hyprland-WindowRuleApplicator.cpp", 426, "static_.size = expr;"),
    (".ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp", 16, "return re2::RE2::FullMatch(other, *m_regex) != m_negative;"),
    (".ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp", 7, 'if (regex.starts_with("negative:")) {'),
    # entry / receipts quotes
    ("corpus/knowledge/hyprland-gkeep-geometry-r43.md", None, '"size": [420, 500]'),
    (".ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt", None, '"size": [420, 500]'),
    (".ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt", None, '"floating": true'),
    (".ufo/waves/round-43/receipts/live-geometry-host.txt", None, "MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT"),
    (".ufo/waves/round-43/fetch/host-gkeep.conf", 4, "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"),
    (".ufo/waves/round-43/fetch/gkeep-ui-excerpt.py", 33, "window.set_default_size(420, 500)"),
]

ok = bad = 0
for path, ln, frag in CASES:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    if ln is None:
        hit = any(frag in l for l in lines)
    else:
        hit = ln <= len(lines) and frag in lines[ln - 1]
    if hit:
        ok += 1
    else:
        bad += 1
        print("MISS %s:%s %r" % (path, ln, frag[:60]))
print("QUOTES: %d/%d checks passed" % (ok, ok + bad))
sys.exit(0 if bad == 0 else 1)
