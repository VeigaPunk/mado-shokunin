#!/bin/bash
# Verify every source quote used in findings.md against the frozen pins at the cited line.
# Pins: .ufo/waves/round-45/fetch (sha256 in receipts/fetch-sha256.txt)
F=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch
fail=0
chk() { # file line literal
  local got; got=$(sed -n "${2}p" "$F/$1")
  if printf '%s' "$got" | grep -qF -- "$3"; then
    printf 'OK   %s:%s  %s\n' "$1" "$2" "$3"
  else
    printf 'FAIL %s:%s  want=%s  got=%s\n' "$1" "$2" "$3" "$got"; fail=1
  fi
}
chk Hyprland-Monitor.cpp 996  'Vector2D logicalSize = m_pixelSize / m_scale;'
chk Hyprland-Monitor.cpp 997  'logicalSize.x != std::round(logicalSize.x)'
chk Hyprland-Monitor.cpp 1001 'float    searchScale = std::round(m_scale * 120.0);'
chk Hyprland-Monitor.cpp 1010 'for (size_t i = 1; i < 90; ++i)'
chk Hyprland-Monitor.cpp 1033 'failed to find a clean divisor'
chk Hyprland-Monitor.cpp 1035 'm_scale = getDefaultScale();'
chk Hyprland-Monitor.cpp 1402 'float CMonitor::getDefaultScale() {'
chk Hyprland-Monitor.cpp 992  'm_scale = RULE->m_scale;'
chk Hyprland-Monitor.cpp 655  'm_transform         = m_activeMonitorRule.m_transform;'
chk Hyprland-Monitor.cpp 250  'm_description = m_output->description;'
chk Hyprland-Monitor.cpp 255  'm_shortDescription = trim'
chk Hyprland-Monitor.cpp 1206 'm_description.starts_with(DESCRIPTIONSELECTOR)'
chk Hyprland-Monitor.cpp 1335 'configString(mirrorOf)'
chk Hyprland-Monitor.cpp 1340 'if (PMIRRORMON && PMIRRORMON->isMirror()) {'
chk Hyprland-Monitor.cpp 1345 'if (PMIRRORMON == m_self) {'
chk Hyprland-Monitor.cpp 836  '!DELTALESSTHAN(bestMode->pixelSize.x, RULE->m_resolution.x, 1)'
chk Hyprland-MonitorRuleManager.cpp 38  'std::erase_if(m_rules'
chk Hyprland-MonitorRuleManager.cpp 96  'm_rules | std::views::reverse'
chk Hyprland-MonitorRuleManager.cpp 97  'PMONITOR->matchesStaticSelector(r.m_name)'
chk Hyprland-MonitorRuleManager.cpp 104 'if (r.m_name.empty())'
chk Hyprland-MonitorRuleManager.cpp 108 'No rules configured. Using the default hardcoded one.'
chk Hyprland-MonitorRuleManager.cpp 110 'CMonitorRule fallbackRule;'
chk Hyprland-MonitorRuleManager.cpp 115 'fallbackRule.m_scale      = -1;'
chk Hyprland-MonitorRuleManager.cpp 46  'PROTO::outputManagement->getOutputStateFor(PMONITOR)'
chk Hyprland-Parser.cpp 111 'value.starts_with("pref")'
chk Hyprland-Parser.cpp 134 'stof(value.substr(value.find_first_of'
chk Hyprland-Parser.cpp 203 'if (m_rule.m_scale < 0.25F) {'
chk Hyprland-Parser.cpp 214 'if (!isNumber(value)) {'
chk Hyprland-Parser.cpp 220 'if (std::clamp(TSF, 0, 7) != TSF) {'
chk Hyprland-Parser.cpp 23  'if (args.size() < 10) {'
chk Hyprland-legacy-ConfigManager.cpp 1310 'if (r.m_name == parser.name()) {'
chk Hyprland-legacy-ConfigManager.cpp 1323 'std::stoi(std::string{ARGS[2]})'
chk Hyprland-legacy-ConfigManager.cpp 1331 'rule->m_reservedArea = area.value();'
chk Hyprland-legacy-ConfigManager.cpp 1341 'monitorRuleMgr()->add(std::move(parser.rule()));'
chk Hyprland-legacy-ConfigManager.cpp 1345 'parser.parseMode(std::string(ARGS[1]));'
chk Hyprland-legacy-ConfigManager.cpp 1378 'invalid syntax at'
chk Hyprland-legacy-ConfigManager.cpp 1384 'monitorRuleMgr()->add(std::move(parser.rule()));'
chk Hyprland-HyprCtl.cpp 277 'escapeJSONStrings(m->m_shortDescription)'
chk Hyprland-HyprCtl.cpp 285 'm->m_enabled ? "false" : "true"'
chk Hyprland-HyprCtl.cpp 286 'm->m_mirrorOf ? std::format("{}", m->m_mirrorOf->m_id) : "none"'
chk Hyprland-HyprCtl.cpp 321 'allMonitors = true;'
chk Hyprland-MonitorRule.hpp 46 'float                        m_refreshRate   = 60;'
chk hyprutils-String.cpp 59 "if (i == 0 && str.at(i) == '-')"
chk Hyprland-MonitorPositionController.cpp 24 'm->explicitPosition()'
chk Hyprland-MonitorPositionController.cpp 27 'm->moveTo(*POS);'
echo "quote-check: $([ $fail -eq 0 ] && echo ALL-OK || echo FAILURES)"
exit $fail
