#!/usr/bin/env python3
"""mado round 78 — generate the frozen C2 runbook case set (shape-bound rows).

Seventeen read-only probes. A case is correct only when its live output matches the
declared expectation *and* every committed churn sample still matches while every
negative sample does not. The churn samples are plausible next-day outputs (a new
workspace id, a recycled pid, a different refresh rate, another bind count): they are
fixtures, not observations, and they are what separates a shape binding from a fixed
value binding.

Usage: python3 make-runbook-cases-r78.py --out c2-runbook-cases-r78.json
"""
import argparse
import json

VERSION_LINE = ("Hyprland 0.56.2 built from branch v0.56.2 at commit "
                "efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).")


def sh(argv):
    return ["/bin/sh", "-c", argv]


CASES = [
    {"name": "version", "argv": sh("hyprctl version | head -n 1"),
     "kind": "regex", "value": r"^Hyprland [0-9]+\.[0-9]+\.[0-9]+ ",
     "frozen": VERSION_LINE,
     "samples": [{"rc": 0, "out": "Hyprland 0.58.0 built from branch v0.58.0 at commit "
                   "0123456789abcdef clean (tag)."}],
     "negatives": [{"rc": 0, "out": "Hyprland (unknown build)"},
                   {"rc": 127, "out": VERSION_LINE}],
     "skill_anchor": "hyprctl version"},
    {"name": "configerrors", "argv": sh("hyprctl configerrors"),
     "kind": "empty", "value": None, "frozen": "",
     "negatives": [{"rc": 0, "out": "unknown option general:nope"},
                   {"rc": 127, "out": ""}],
     "skill_anchor": "hyprctl configerrors"},
    {"name": "monitors-size", "argv": sh(
        "hyprctl monitors -j | jq -r '.[0] | \"\\(.name) \\(.width)x\\(.height)@\\(.refreshRate)\"'"),
     "kind": "regex", "value": r"^\S+ [1-9][0-9]*x[1-9][0-9]*@[0-9]+(\.[0-9]+)?$",
     "frozen": "DP-1 3440x1440@99.99700",
     "samples": [{"rc": 0, "out": "DP-1 3440x1440@120.00000"},
                 {"rc": 0, "out": "HDMI-A-1 1920x1080@60.00000"}],
     "negatives": [{"rc": 0, "out": "DP-1 3440x1440@"},
                   {"rc": 0, "out": "DP-1 3440x1440@60.0x"}],
     "skill_anchor": "hyprctl monitors"},
    {"name": "monitors-reserved", "argv": sh("hyprctl monitors -j | jq -c '.[0].reserved'"),
     "kind": "int4", "value": None, "frozen": "[0,26,0,0]",
     "samples": [{"rc": 0, "out": "[0,40,0,0]"}, {"rc": 0, "out": "[8,26,8,26]"}],
     "negatives": [{"rc": 0, "out": "[0,26,0]"},
                   {"rc": 0, "out": "[-1,26,0,0]"}],
     "skill_anchor": "hyprctl monitors"},
    {"name": "gaps-out", "argv": sh("hyprctl getoption general:gaps_out | head -n 1"),
     "kind": "exact", "value": "custom type: 0 0 0 0", "frozen": "custom type: 0 0 0 0",
     "negatives": [{"rc": 0, "out": "custom type: 10 10 10 10"}],
     "skill_anchor": "hyprctl getoption <key>"},
    {"name": "kb-layout", "argv": sh("hyprctl getoption input:kb_layout | head -n 1"),
     "kind": "exact", "value": "str: br", "frozen": "str: br",
     "negatives": [{"rc": 0, "out": "str: us"}],
     "skill_anchor": "hyprctl getoption <key>"},
    {"name": "binds-count", "argv": sh("hyprctl binds -j | jq 'length'"),
     "kind": "int_range", "value": [1, 100000], "frozen": "192",
     "samples": [{"rc": 0, "out": "193"}, {"rc": 0, "out": "1024"}],
     "negatives": [{"rc": 0, "out": "0"}, {"rc": 0, "out": "-3"},
                   {"rc": 127, "out": "192"}],
     "skill_anchor": "hyprctl binds -j"},
    {"name": "layers-namespaces", "argv": sh(
        "hyprctl layers -j | jq -r '[to_entries[] | .value.levels | to_entries[] | "
        "select(.value|length>0) | .value[].namespace] | sort | join(\",\")'"),
     "kind": "sorted_unique", "value": {"must_include": ["waybar"]},
     "frozen": "wallpaper,waybar",
     "samples": [{"rc": 0, "out": "mako,wallpaper,waybar"},
                 {"rc": 0, "out": "walker,wallpaper,waybar"}],
     "negatives": [{"rc": 0, "out": "waybar,wallpaper"},
                   {"rc": 0, "out": "wallpaper,wallpaper,waybar"},
                   {"rc": 0, "out": ""}],
     "skill_anchor": "hyprctl layers -j"},
    {"name": "waybar-process", "argv": sh("pgrep -x waybar | head -n 1"),
     "kind": "int_range", "value": [1, 4194304], "frozen": "1720",
     "samples": [{"rc": 0, "out": "20011"}, {"rc": 0, "out": "999"}],
     "negatives": [{"rc": 0, "out": "0"}, {"rc": 1, "out": ""}],
     "skill_anchor": "pgrep -a"},
    {"name": "mako-mode", "argv": sh("makoctl mode"),
     "kind": "exact", "value": "default", "frozen": "default",
     "negatives": [{"rc": 0, "out": "do-not-disturb"}],
     "skill_anchor": "makoctl mode"},
    {"name": "omarchy-theme", "argv": sh("omarchy theme current"),
     "kind": "exact", "value": "Matte Black", "frozen": "Matte Black",
     "negatives": [{"rc": 0, "out": "Tokyo Night"}],
     "skill_anchor": "omarchy theme current"},
    {"name": "omarchy-version", "argv": sh("omarchy version"),
     "kind": "regex", "value": r"^[0-9]+\.[0-9]+\.[0-9]+$", "frozen": "3.8.3",
     "samples": [{"rc": 0, "out": "3.9.0"}, {"rc": 0, "out": "3.10.2"}],
     "negatives": [{"rc": 0, "out": "3.8"}, {"rc": 0, "out": "v3.8.3"},
                   {"rc": 127, "out": "3.8.3"}],
     "skill_anchor": "omarchy version"},
    {"name": "active-workspace", "argv": sh("hyprctl activeworkspace -j | jq -c '{id,name}'"),
     "kind": "json_object_fields", "value": {"fields": {"id": "int", "name": "str"}},
     "frozen": '{"id":1,"name":"1"}',
     "samples": [{"rc": 0, "out": '{"id":3,"name":"3"}'},
                 {"rc": 0, "out": '{"id":-99,"name":"special"}'}],
     "negatives": [{"rc": 0, "out": '{"id":"1","name":"1"}'},
                   {"rc": 0, "out": '{"id":1}'},
                   {"rc": 0, "out": '[]'}],
     "skill_anchor": "hyprctl activeworkspace"},
    {"name": "layers-dump", "argv": sh("hyprctl layers -j"),
     "kind": "levels_dump", "value": None,
     "samples": [{"rc": 0, "out": json.dumps({"HDMI-A-1": {"levels": {
         "0": [], "1": [], "2": [], "3": []}}})}],
     "negatives": [{"rc": 0, "out": json.dumps({"DP-1": {"levels": {"0": []}}})},
                   {"rc": 0, "out": "[]"}],
     "skill_anchor": "hyprctl layers -j"},
    {"name": "monitors-dump", "argv": sh("hyprctl monitors -j"),
     "kind": "array_fields",
     "value": {"min_items": 1, "fields": {"name": "str", "width": "positive_int",
                                         "height": "positive_int", "reserved": "int4",
                                         "scale": "number"}},
     "samples": [{"rc": 0, "out": json.dumps([{"name": "HDMI-A-1", "width": 1920,
                                               "height": 1080, "reserved": [0, 40, 0, 0],
                                               "scale": 1.0}])}],
     "negatives": [{"rc": 0, "out": json.dumps([{"name": "DP-1", "width": 3440,
                                                 "height": 1440, "reserved": [0, 26, 0],
                                                 "scale": 1.0}])},
                   {"rc": 0, "out": json.dumps([{"name": "", "width": 3440,
                                                 "height": 1440, "reserved": [0, 26, 0, 0],
                                                 "scale": 1.0}])}],
     "skill_anchor": "hyprctl monitors"},
    {"name": "clients-count", "argv": sh("hyprctl clients -j | jq 'length'"),
     "kind": "int_range", "value": [0, 100000], "frozen": "2",
     "samples": [{"rc": 0, "out": "7"}, {"rc": 0, "out": "0"}],
     "negatives": [{"rc": 0, "out": "-1"}, {"rc": 127, "out": "2"}],
     "skill_anchor": "hyprctl clients -j"},
    {"name": "workspaces-count", "argv": sh("hyprctl workspaces -j | jq 'length'"),
     "kind": "int_range", "value": [1, 1000], "frozen": "2",
     "samples": [{"rc": 0, "out": "12"}, {"rc": 0, "out": "1"}],
     "negatives": [{"rc": 0, "out": "0"}, {"rc": 0, "out": "ten"}],
     "skill_anchor": "hyprctl workspaces -j"},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    for case in CASES:
        case.setdefault("samples", [])
        case.setdefault("negatives", [])
    with open(args.out, "w") as fh:
        json.dump({"protocol": "mado-c2-r78-v1", "cases": CASES}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s: cases=%d shapes=%d"
          % (args.out, len(CASES),
             sum(1 for c in CASES if c["kind"] not in ("exact", "contains", "empty"))))


if __name__ == "__main__":
    main()
