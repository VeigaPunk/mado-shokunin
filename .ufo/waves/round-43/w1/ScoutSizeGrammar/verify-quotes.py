import sys
P='/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/'
Q=[('w1/ScoutSizeGrammar/pins/Hyprland-WindowRule.cpp',270,'auto parsed = Math::parseExpressionVec2(raw);'),
('w1/ScoutSizeGrammar/pins/Hyprland-Expression.cpp',36,'const auto spacePos = raw.find_first_of(" \\t\\n\\r\\f\\v");'),
('w1/ScoutSizeGrammar/pins/Hyprland-Expression.cpp',38,'expression vec2 requires two expressions separated by whitespace'),
('w1/ScoutSizeGrammar/pins/Hyprland-MiscFunctions.cpp',842,'}("true"sv, "yes"sv, "on"sv);'),
('w1/ScoutSizeGrammar/pins/Hyprland-Window.cpp',2010,'expr.addVariable("monitor_w", PMONITOR ? PMONITOR->m_size.x : 1920);'),
('fetch/Hyprland-DefaultFloatingAlgorithm.cpp',52,'set this here so that expressions can use it. This could be wrong of course.'),
('fetch/Hyprland-RegexMatchEngine.cpp',16,'return re2::RE2::FullMatch(other, *m_regex) != m_negative;'),
('w1/ScoutSizeGrammar/pins/Hyprland-TagKeeper.cpp',6,'const bool TAGGED   = m_tags.contains(MATCH) || (!strict && m_tags.contains(MATCH + "*"));'),
('w1/ScoutSizeGrammar/pins/Hyprland-src_config_legacy_ConfigManager.cpp',2028,'invalid field {}: missing a value')]
bad=0
for f,n,q in Q:
    L=open(P+f,errors='replace').read().split('\n')[n-1]
    ok=q in L and len(q.split())<=25
    bad+=not ok; print('PASS' if ok else 'FAIL',f,n)
sys.exit(bad)
