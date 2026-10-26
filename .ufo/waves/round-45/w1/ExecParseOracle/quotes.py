#!/usr/bin/env python3
"""Verify every quotation used in report.md: the cited line of the cited file must equal the quote, and
the quote must be at most 25 words. Line numbers come from `grep -n`; this script is what proves the
pairing, so the report never carries a typed locator. Writes receipts/quotes.txt.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
F = ".ufo/waves/round-45/fetch/"
P = ".ufo/waves/round-45/w1/ExecParseOracle/pins/"
T = ".ufo/waves/round-45/l1-draft/mado-monitors.py"

QUOTES = [
    (F + "Hyprland-legacy-ConfigManager.cpp", 1293,
     'std::optional<std::string> CConfigManager::handleMonitor(const std::string& command, const std::string& args) {'),
    (F + "Hyprland-legacy-ConfigManager.cpp", 1299,
     'if (ARGS[1] == "disable" || ARGS[1] == "disabled" || ARGS[1] == "addreserved" || ARGS[1] == "transform") {'),
    (F + "Hyprland-legacy-ConfigManager.cpp", 1323,
     'area = {std::stoi(std::string{ARGS[2]}), std::stoi(std::string{ARGS[5]}), std::stoi(std::string{ARGS[3]}), std::stoi(std::string{ARGS[4]})};'),
    (F + "Hyprland-legacy-ConfigManager.cpp", 1341,
     'Config::monitorRuleMgr()->add(std::move(parser.rule()));'),
    (F + "Hyprland-legacy-ConfigManager.cpp", 1351,
     'while (!ARGS[argno].empty()) {'),
    (F + "Hyprland-Parser.cpp", 219, 'const auto TSF = std::stoi(value);'),
    (F + "Hyprland-Parser.cpp", 121,
     'm_rule.m_refreshRate = sc<float>(m_rule.m_drmMode.vrefresh) / 1000;'),
    (F + "Hyprland-Parser.cpp", 23, 'if (args.size() < 10) {'),
    (F + "Hyprland-Monitor.cpp", 773, 'if (RULE->m_resolution == Vector2D()) {'),
    (F + "Hyprland-Monitor.cpp", 1206,
     'return m_description.starts_with(DESCRIPTIONSELECTOR) || m_shortDescription.starts_with(DESCRIPTIONSELECTOR);'),
    (F + "Hyprland-MonitorRuleManager.cpp", 38,
     'std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });'),
    (F + "Hyprland-MonitorRuleManager.cpp", 97,
     'if (PMONITOR->matchesStaticSelector(r.m_name))'),
    (F + "Hyprland-MonitorRule.hpp", 46, 'float                        m_refreshRate   = 60; // Hz'),
    (P + "hyprlang-v0.6.8-src-config.cpp", 672, 'line = trim(line);'),
    (P + "hyprlang-v0.6.8-src-config.cpp", 691, "if (line[commentPos + 1] == '#') {"),
    (P + "hyprlang-v0.6.8-src-config.cpp", 701,
     'line       = line.substr(0, commentPos + 1) + line.substr(commentPos + 2);'),
    (P + "hyprlang-v0.6.8-src-config.cpp", 723,
     'auto         RHS = trim(line.substr(equalsPos + 1));'),
    (P + "hyprlang-v0.6.8-src-config.cpp", 53,
     "while (line.length() > 0 && line.at(line.length() - 1) == '\\\\') {"),
    (P + "include_hyprutils_string_String.hpp", 9,
     'bool             isNumber(const std::string& str, bool allowfloat = false);'),
    (F + "hyprutils-String.cpp", 11,
     'while (countBefore < in.length() && std::isspace(in.at(countBefore))) {'),
    (P + "src_string_VarList2.cpp", 67,
     'const auto ARG = trim(std::string_view{m_inString}.substr(argBegin, i - argBegin));'),
    (P + "src_string_VarList2.cpp", 41, 'escapedIndices.emplace_back(i - argBegin - 1);'),
    (P + "src_string_VarList2.cpp", 77, 'm_copyStrings.emplace_back(std::move(cpy));'),
    (T, 194, 'if toks and toks[0] == "modeline":'),
    (T, 224, 'if len(value) == 1 and value in "01234567":'),
    (T, 230, 'if "##" in body or "$" in body or "\\\\" in body:'),
    (T, 233, 'body = body.split("#", 1)[0]'),
    (T, 259, 'if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 6)):'),
    (T, 370, 'if rule["mode"] == "explicit":'),
    (P + "hyprlang-v0.6.8-src-config.cpp", 844, 'const bool UNSCOPED    = !h.name.contains(":");'),
    (P + "hyprlang-v0.6.8-src-config.cpp", 866,
     'if (UNSCOPED && HANDLERNAME != LHS && !h.options.allowFlags)'),
    (P + "hyprlang-v0.6.8-src-config.cpp", 832, 'auto [f, rv]    = configSetValueSafe(LHS, RHS);'),
    (T, 32, '"\\\\n"; a line is stripped of spaces and tabs at both ends. A line whose first token (up to a space, tab, `=`'),
    (T, 35, 'modelled; else it is cut at its first `#`, split on ",", and each field is stripped of spaces and tabs;'),
    (T, 38, '- field 1 `transform`: field 2 must be one digit 0-7, else the line adds one to `badrules`. The first rule'),
    (T, 41, '- field 1 `addreserved`: fields 2-5 must each fullmatch `-?[0-9]{1,6}`, else `badrules`. If a rule with'),
    (T, 48, '`highrr`, `highres`, `maxwidth` is that keyword; a first token `modeline` (any case) is modeline; else it'),
    (T, 487, '("addreserved-new", "monitor = DP-1, addreserved, 10, 0, 0, 0\\n", [mon("DP-1", x=50, scale=1.5)], "OK", 0, ["rule=1 differ=- verdict=AGREE"]),'),
    (F + "Hyprland-HyprCtl.cpp", 277,
     'm->m_id, escapeJSONStrings(m->m_name), escapeJSONStrings(m->m_shortDescription), escapeJSONStrings(m->m_output->make), escapeJSONStrings(m->m_output->model),'),
    (F + "Hyprland-legacy-ConfigManager.cpp", 606,
     'm_config->registerHandler(&::handleMonitor, "monitor", {false});'),
]


def main():
    bad = 0
    out = ["# quote verification: cited line == quote, <= 25 words"]
    for rel, lineno, quote in QUOTES:
        path = os.path.join(LANE, rel)
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().split("\n")
        actual = lines[lineno - 1].strip() if 0 < lineno <= len(lines) else "<past end>"
        words = len(quote.split())
        ok = actual == quote and words <= 25
        out.append("%s %s:%d  words=%d  %s" % ("OK  " if ok else "FAIL", rel, lineno, words, quote))
        if not ok:
            bad += 1
            out.append("     actual: %s" % actual)
    out.append("quotes=%d failed=%d" % (len(QUOTES), bad))
    text = "\n".join(out) + "\n"
    with open(os.path.join(HERE, "receipts", "quotes.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
