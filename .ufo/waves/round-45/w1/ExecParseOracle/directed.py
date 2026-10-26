#!/usr/bin/env python3
"""Directed cases: each is one pinned C++ behaviour the reference tool cannot express, with the tool's
own output and the model's rule list side by side. Verdict-plane cases compare the tool's AGREE/DIFFER
against what applyMonitorRule would do with the same rule (Monitor.cpp:719-880).

Run: python3 directed.py  (writes receipts/directed.txt and prints it)
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
TOOL_PATH = os.path.join(LANE, ".ufo", "waves", "round-45", "l1-draft", "mado-monitors.py")
sys.path.insert(0, HERE)
import model as M  # noqa: E402

spec = importlib.util.spec_from_file_location("mado_monitors_ref", TOOL_PATH)
TOOL = importlib.util.module_from_spec(spec)
spec.loader.exec_module(TOOL)


def mon(name, desc="", desc_long="", w=3440, h=1440, rr=99.997, x=0, y=0, scale=1.0, transform=0):
    return {"id": 0, "name": name, "description": desc, "width": w, "height": h, "refreshRate": rr,
            "x": x, "y": y, "scale": scale, "transform": transform, "disabled": False,
            "mirrorOf": "none", "_desc_long": desc_long}


CASES = [
    # id, why, config, monitors
    ("V1-zero-mode",
     "Parser.cpp:139-141 stores (0,0) for '0x0'; Monitor.cpp:773 reads that as PREFERRED, so Hyprland "
     "picks the preferred mode, not a 0x0 mode. The tool compares width==0 and height==0 and says DIFFER.",
     "monitor = DP-1, 0x0, 0x0, 1\n",
     [mon("DP-1")]),
    ("V2-valid-modeline",
     "Parser.cpp:132-142: a validated modeline becomes resolution (hdisplay,vdisplay) and "
     "refreshRate vrefresh/1000, so applyMonitorRule requests that custom mode (Monitor.cpp:838-846); "
     "the tool marks the rule 'modeline' and never compares mode, so it reports AGREE for a live mode "
     "the rule does not describe.",
     "monitor = DP-1, modeline 419.00 3440 3448 3520 3680 1440 1443 1448 1481 +hsync -vsync\n",
     [mon("DP-1")]),
    ("V2b-malformed-modeline",
     "Parser.cpp:129-160: a modeline that fails parseModeLine (fewer than 10 args) falls through to the "
     "resolution branch and ends at (0,0) = preferred; the tool still reports mode=modeline.",
     "monitor = DP-1, modeline 419.00 3440\n",
     [mon("DP-1")]),
    ("V3-desc-long-description",
     "Monitor.cpp:1206 matches desc: against the long description OR the short one; the dump only "
     "carries the short one (HyprCtl.cpp:234), so the tool reports UNRULED. Declared in its docstring.",
     "monitor = desc:BOE 0x095F REV, 2880x1920@120, 0x0, 1.6\n",
     [mon("eDP-1", desc="BOE 0x095F", desc_long="BOE 0x095F REV A1", w=2880, h=1920, rr=120.0,
          scale=1.6)]),
    ("V4-dollar-in-comment",
     "hyprlang v0.6.8 config.cpp:697-706 strips the comment before the handler runs, so the value has no "
     "'$'; the tool tests the raw body for '$' before cutting the comment and reports NOT_COMPARED.",
     "monitor = DP-1, 3440x1440@100, 0x0, 1 # $x\n",
     [mon("DP-1")]),
    ("V5-transform-out-of-range",
     "Parser.cpp:235 std::stoi is unguarded: '99999999999' makes isNumber true and stoi throw "
     "out_of_range, which escapes handleMonitor. The tool reports badrules (no rule change).",
     "monitor = DP-1, 1920x1080, 0x0, 1\nmonitor = DP-1, transform, 99999999999\n",
     [mon("DP-1")]),
    ("V6-transform-leading-zero",
     "Parser.cpp:228-240: isNumber('03') is true and stoi('03') is 3, so the existing rule is copied "
     "with transform 3 (ConfigManager.cpp:1300-1314); the tool calls the value invalid and changes "
     "nothing.",
     "monitor = DP-1, 1920x1080, 0x0, 1\nmonitor = DP-1, transform, 03\n",
     [mon("DP-1")]),
    ("V7-addreserved-stoi-prefix",
     "ConfigManager.cpp:1336-1347 parses the four numbers with std::stoi (prefix): '+5' and '1.5' and "
     "'0x10' are accepted and a default rule is added at :1367; the tool requires "
     "-?[0-9]{1,6} and adds nothing.",
     "monitor = DP-1, addreserved, +5, 0, 0, 0\n",
     [mon("DP-1")]),
    ("V8-crlf-single-field",
     "hyprlang config.cpp:672/706 trims with std::isspace and CVarList2 trims each field, so a CRLF "
     "leaves no '\\r' in the selector; the tool strips only spaces and tabs, so its selector is "
     "'DP-1\\r' and the output is UNRULED.",
     "monitor = DP-1\r\n",
     [mon("DP-1")]),
    ("V8b-crlf-scale",
     "Same trim gap, on the last field: the tool sees scale '1\\r', finds no fullmatch and reports "
     "unsupported (NOT_COMPARED); Hyprland reads 1.",
     "monitor = DP-1, 3440x1440@100, 0x0, 1\r\n",
     [mon("DP-1")]),
    # positive controls: the two agree, so the harness is not reporting everything
    ("C1-newest-match",
     "MonitorRuleManager.cpp:37-42 erase+append; :107-117 reverse scan. Both agree.",
     "monitor = DP-1, 1920x1080, 0x0, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n",
     [mon("DP-1")]),
    ("C2-empty-fallback",
     "MonitorRuleManager.cpp:110-115: an empty selector never matches by name, the first one is the "
     "fallback. Both agree.",
     "monitor = , preferred, auto, 1\nmonitor = HDMI-A-1, 1920x1080@60, 0x0, 1\n",
     [mon("DP-1")]),
    ("C3-modifier-transform",
     "Parser.cpp:157-159 + ConfigManager.cpp:1300-1314: a valid single-digit transform copies the rule.",
     "monitor = DP-1, 3440x1440@100, 0x0, 1\nmonitor = DP-1, transform, 3\n",
     [mon("DP-1")]),
    ("C4-desc-prefix",
     "Monitor.cpp:1202-1206. Both agree.",
     "monitor = desc:Dell Inc. U34, 3440x1440@100, 0x0, 1\n",
     [mon("DP-1", desc="Dell Inc. U3415W X1")]),
    ("C5-scale-correction",
     "Parser.cpp:216-224: 0.2 < 0.25 becomes 1. Both agree.",
     "monitor = DP-1, 3440x1440@100, 0x0, 0.2\n",
     [mon("DP-1")]),
]


def run_case(cfg, mons):
    dump = [{k: v for k, v in m.items() if not k.startswith("_")} for m in mons]
    lines, rc = TOOL.report(json.dumps(dump).encode(), [cfg])
    mlist = [{"name": m["name"], "desc_short": m["description"], "desc_long": m["_desc_long"]}
             for m in mons]
    rules, assignments, unmodelled, escapes = M.simulate([cfg], mlist)
    return lines, rc, rules, assignments, escapes


def main():
    out = ["# directed cases: pinned C++ behaviour vs the reference tool", ""]
    for cid, why, cfg, mons in CASES:
        lines, rc, rules, assigns, escapes = run_case(cfg, mons)
        out.append("== %s ==" % cid)
        out.append("why: " + why)
        out.append("config: " + json.dumps(cfg))
        out.append("model rules: " + json.dumps([list(r.canon()) for r in rules]))
        out.append("model assignment: " + json.dumps(
            [[m["name"], a[0]] for m, a in zip(mons, assigns)]))
        if escapes:
            out.append("model exceptions: " + json.dumps(escapes))
        for line in lines:
            out.append("tool| " + line)
        out.append("tool rc=%d" % rc)
        out.append("")
    text = "\n".join(out) + "\n"
    with open(os.path.join(HERE, "receipts", "directed.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
