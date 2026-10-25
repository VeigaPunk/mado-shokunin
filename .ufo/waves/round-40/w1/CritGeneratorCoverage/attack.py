#!/usr/bin/env python3
"""CritGeneratorCoverage: which real spellings can a WRONG tool get right on the
C1 generator?  Each mutant below is the frozen reference live tool
(`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt`) with ONE defect that is wrong
only on a spelling class the generator never emits.  For every mutant we

  1. score it with the frozen counter's `--tool` switch
     (`quality/counters/c1-r40-live.py`, PRED-C1-r40-v1) and require
     fixtures=13/13, and
  2. run it on a hand-built home+stub that DOES use the class, and require the
     reference to label the row `agreement` (the truth) while the mutant
     labels it `mismatch` / `config-only` / fails.

A mutant that reaches 13/13 and is wrong on a real class proves the generator
cannot see that class.  Read-only: writes only under a mktemp -d.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r40-live.py")
REF = os.path.join(LANE, ".ufo", "waves", "round-40", "c1", "ctl-ref-tool.py.txt")
REV = "master"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

STUB = r'''#!%(py)s
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
table = json.load(open(os.path.join(here, "table.json")))
if sys.argv[1:3] != ["getoption", "-j"] or len(sys.argv) != 4:
    sys.stdout.write("bad request\n"); sys.exit(0)
rec = table.get(sys.argv[3])
sys.stdout.write("no such option\n" if rec is None else json.dumps(rec) + "\n")
'''

# ---------------------------------------------------------------- mutants
# name: (old, new, class the mutation is blind to, evidence for the class,
#        probe=(config, key, stub-record))
MUTANTS = {
    "X01-vec2-reply-swallowed": (
        '    forms = [f for f in ("int", "float", "str", "custom") if f in rec]\n'
        '    if not isinstance(rec, dict) or len(forms) != 1 or "set" not in rec:\n'
        '        raise CtlError("%s: unknown reply form from %s" % (key, hyprctl))',
        '    forms = [f for f in ("int", "float", "str", "custom") if f in rec]\n'
        '    if not isinstance(rec, dict) or len(forms) != 1 or "set" not in rec:\n'
        '        return None',
        "fifth reply form `vec2` (real: hyprctl getoption -j decoration:shadow:offset)",
        'hyprctl getoption -j decoration:shadow:offset -> '
        '{"option": "decoration:shadow:offset", "vec2": [0,0], "set": false}',
        ("decoration {\n    shadow {\n        offset = 5, 5\n    }\n}\n",
         "decoration:shadow:offset",
         {"option": "decoration:shadow:offset", "vec2": [5, 5], "set": True})),
    "X02-float-two-decimals": (
        "            return abs(float(d) - float(live)) < 1e-6\n",
        "            return abs(float(d) - float(live)) < 1e-6 and "
        "len(d.partition(\".\")[2]) == 2\n",
        "float declared with other than 2 decimals (host: 0.4)",
        ".config/hypr/input.conf:33  touchpad { scroll_factor = 0.4 }",
        ("input {\n    touchpad {\n        scroll_factor = 0.4\n    }\n}\n",
         "input:touchpad:scroll_factor",
         {"option": "input:touchpad:scroll_factor", "float": 0.4, "set": True})),
    "X03-str-empty": (
        "            return d == str(live).strip()\n",
        "            return bool(d) and d == str(live).strip()\n",
        "empty str value",
        ".config/hypr/input.conf:5  kb_model = '' ; live reply is \"str\": \"\"",
        ("input {\n    kb_model =\n}\n",
         "input:kb_model",
         {"option": "input:kb_model", "str": "", "set": True})),
    "X04-str-first-token": (
        "            return d == str(live).strip()\n",
        "            return d.split()[0] == str(live).strip()\n",
        "str value containing spaces",
        ".config/hypr/hyprlock.conf:29  font_family = JetBrainsMono Nerd Font",
        ("group {\n    groupbar {\n        font_family = JetBrainsMono Nerd Font\n"
         "    }\n}\n",
         "group:groupbar:font_family",
         {"option": "group:groupbar:font_family", "str": "JetBrainsMono Nerd Font",
          "set": True})),
    "X05-weight-no-lower": (
        "        return str(WEIGHTS.get(d.lower(), -1)) == str(live)\n",
        "        return str(WEIGHTS.get(d, -1)) == str(live)\n",
        "uppercase font-weight name",
        "ComplexDataTypes.hpp:163-169  parseWeight lowercases before the lookup",
        ("group {\n    groupbar {\n        font_weight_active = UltraHeavy\n    }\n}\n",
         "group:groupbar:font_weight_active",
         {"option": "group:groupbar:font_weight_active", "custom": "1000", "set": True})),
    "X06-weight-numeric": (
        "        return str(WEIGHTS.get(d.lower(), -1)) == str(live)\n",
        "        return str(WEIGHTS.get(d.lower(), -1)) == str(live) "
        "if not d.isdigit() else False\n",
        "numeric font-weight",
        "ComplexDataTypes.hpp:171  parseWeight falls back to std::stoi",
        ("group {\n    groupbar {\n        font_weight_active = 700\n    }\n}\n",
         "group:groupbar:font_weight_active",
         {"option": "group:groupbar:font_weight_active", "custom": "700", "set": True})),
    "X07-gradient-three-stops": (
        '            return bool(cols) and " ".join("%x" % c for c in cols)'
        ' + " %ddeg" % angle == str(live)\n',
        '            return bool(cols) and " ".join("%x" % c for c in cols[:3])'
        ' + " %ddeg" % angle == str(live)\n',
        "gradient with 4+ colour stops",
        "ConfigManager.cpp:126  gradient handler: max colors is 10",
        ("general {\n    col.active_border = rgba(11223344) rgba(55667788) "
         "rgba(99aabbcc) rgba(aabbccdd) 45deg\n}\n",
         "general:col.active_border",
         {"option": "general:col.active_border",
          "custom": "44112233 88556677 cc99aabb ddaabbcc 45deg", "set": True})),
    "X08-gap-nonneg-only": (
        '        if len(toks) == 4 and all(t.lstrip("-").isdigit() for t in toks):\n',
        '        if len(toks) == 4 and all(t.isdigit() for t in toks):\n',
        "gap with negative values",
        "ComplexDataTypes.hpp:95  parseGapData toInt = std::stoi (negatives kept)",
        ("general {\n    gaps_in = -1\n}\n",
         "general:gaps_in",
         {"option": "general:gaps_in", "custom": "-1 -1 -1 -1", "set": True})),
    "X09-gap-max-four": (
        '            return " ".join(str(x) for x in n[:4]) == str(live)\n',
        '            return len(n) <= 4 and " ".join(str(x) for x in n[:4])'
        ' == str(live)\n',
        "gap with 5+ values (hyprland uses the first four)",
        "ComplexDataTypes.hpp:114-118  default: uses varlist[0..3]",
        ("general {\n    gaps_out = 1 2 3 4 5\n}\n",
         "general:gaps_out",
         {"option": "general:gaps_out", "custom": "1 2 3 4", "set": True})),
    "X10-hex-eight-digits-only": (
        '    if v.startswith("0x"):\n        try:\n            return int(v, 16)\n',
        '    if v.startswith("0x"):\n        try:\n'
        '            return int(v, 16) if len(v) == 10 else None\n',
        "short `0x` hex (6 digits, or 0x1)",
        "ParserUtils.cpp parseHex -> strToNumber<uint64_t>: any hex length; "
        "gtest parseColor(\"1\") == 0x1",
        ("general {\n    col.inactive_border = 0xff0000\n}\n",
         "general:col.inactive_border",
         {"option": "general:col.inactive_border", "custom": "ff0000 0deg",
          "set": True})),
    "X11-hex-lowercase-only": (
        '        if len(inner) == 8:\n            try:\n                x = int(inner, 16)\n'
        '            except ValueError:\n                return None\n',
        '        if len(inner) == 8:\n            try:\n                x = int(inner, 16)\n'
        '            except ValueError:\n                return None\n'
        '            if inner != inner.lower():\n                return None\n',
        "uppercase hex digits",
        "ParserUtils.cpp parseHex/strToNumber: case-insensitive; "
        "gtest parseColor(\"#DEFFaDAA\") == 0xAADEFFAD",
        ("decoration {\n    shadow {\n        color = rgba(EE1A1A1A)\n    }\n}\n",
         "decoration:shadow:color",
         {"option": "decoration:shadow:color", "custom": "1aee1a1a 0deg",
          "set": True})),
    "X12-negative-angle": (
        '                if "deg" in tok:\n'
        '                    angle = int(tok[:tok.index("deg")])\n'
        '                    break\n',
        '                if "deg" in tok:\n'
        '                    angle = int(tok[:tok.index("deg")]) '
        'if tok[:tok.index("deg")].isdigit() else angle\n'
        '                    break\n',
        "negative gradient angle",
        "ConfigManager.cpp:120  gradient angle = std::stoi(token before deg)",
        ("general {\n    col.active_border = rgba(11223344) -45deg\n}\n",
         "general:col.active_border",
         {"option": "general:col.active_border", "custom": "44112233 -45deg",
          "set": True})),
    "X14-var-not-expanded": (
        '            if needle in rhs:\n'
        '                rhs = rhs.replace(needle, val)\n'
        '                matched = True\n',
        '            if False:\n'
        '                rhs = rhs.replace(needle, val)\n'
        '                matched = True\n',
        "$variable in a declared value",
        "themes/kanagawa/hyprland.conf:1,4  $activeBorderColor = rgb(dcd7ba) / "
        "col.active_border = $activeBorderColor",
        ("$activeBorderColor = rgb(dcd7ba)\n"
         "general {\n    col.active_border = $activeBorderColor\n}\n",
         "general:col.active_border",
         {"option": "general:col.active_border", "custom": "ffdcd7ba 0deg",
          "set": True})),
    "X15-source-ignored": (
        '    if lhs == "source":\n'
        '        handle_source(rhs, st, current_path)\n'
        '        return\n',
        '    if lhs == "source":\n'
        '        return\n',
        "`source =` layering (every one of the host's 70 keys but the main file's "
        "arrive through it)",
        "default/hypr/hyprland.conf sources looknfeel.conf/input.conf/... ; "
        "the whole 70-key census depends on it",
        ([(".config/hypr/hyprland.conf",
           "source = ~/.config/hypr/looknfeel.conf\n"),
          (".config/hypr/looknfeel.conf",
           "general {\n    gaps_in = 5\n}\n")],
         "general:gaps_in",
         {"option": "general:gaps_in", "custom": "5 5 5 5", "set": True})),
    "X16-expression-not-evaluated": (
        '        try:\n            rhs = expand_expressions(rhs)\n'
        '        except ExprError:\n'
        '            return  # hyprlang rejects the line; value is skipped\n',
        '        try:\n            pass\n'
        '        except ExprError:\n'
        '            return  # hyprlang rejects the line; value is skipped\n',
        "`{{ expr }}` arithmetic in a value",
        "hyprlang v0.6.8 config.cpp:619 parseExpression ({{ a + b }})",
        ("general {\n    gaps_in = {{ 2 + 3 }}\n}\n",
         "general:gaps_in",
         {"option": "general:gaps_in", "custom": "5 5 5 5", "set": True})),
    "X13-key-depth-collapse": (
        "    def declare(self, key, value, path, lineno):\n"
        "        layer = layer_of(path, self.home)\n",
        "    def declare(self, key, value, path, lineno):\n"
        '        key = key.split(":")[0] + ":" + key.split(":")[-1]\n'
        "        layer = layer_of(path, self.home)\n",
        "keys with two colons (29 of the host's 70)",
        "native-capture.jsonl: decoration:blur:brightness, group:groupbar:*",
        ("decoration {\n    blur {\n        brightness = 0.60\n    }\n}\n",
         "decoration:blur:brightness",
         {"option": "decoration:blur:brightness", "float": 0.6, "set": True})),
}



# ------------------------------------------------- model-defect probes
# These are NOT mutants: they show the frozen reference MODEL (shared verbatim
# by the counter's `gradient_text`/`hl_int`) mislabels a real class, so the
# generator cannot see it and the counter cannot either.
MODEL_PROBES = {
    "P1-alpha-floor-vs-round": (
        ("general {\n    col.active_border = rgba(20,21,22,0.5) 0deg\n}\n",
         "general:col.active_border",
         {"option": "general:col.active_border", "custom": "7f141516 0deg",
          "set": True}),
        "gradient token alpha is std::floor(a*255.F) (ParserUtils.cpp:88); the "
        "model rounds -> 0x80, hyprland's own gtest asserts parseColor("
        "\"rgba(20, 21, 22, 0.5)\") == 0x7F141516"),
    "P2-numeric-weight": (
        ("group {\n    groupbar {\n        font_weight_active = 700\n    }\n}\n",
         "group:groupbar:font_weight_active",
         {"option": "group:groupbar:font_weight_active", "custom": "700",
          "set": True}),
        "ComplexDataTypes.hpp:171 parseWeight falls back to std::stoi; model "
        "returns -1 for any non-name"),
    "P3-vec2-reply": (
        ("decoration {\n    shadow {\n        offset = 5, 5\n    }\n}\n",
         "decoration:shadow:offset",
         {"option": "decoration:shadow:offset", "vec2": [5, 5], "set": True}),
        "real getoption reply form; the tool exits 5 (claims a compositor "
        "failure) on a healthy compositor"),
}


def score(path):
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", LANE,
                        "--rev", REV, "--tool", path],
                       capture_output=True, text=True, env=ENV)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    m = re.search(r"fixtures=(\d+)/13", last)
    return (int(m.group(1)) if m else None), last


def make_case(tmp, name, config, table):
    d = os.path.join(tmp, name)
    os.makedirs(d)
    home = os.path.join(d, "home")
    os.makedirs(os.path.join(home, ".config", "hypr"))
    files = config if isinstance(config, list) else [
        (".config/hypr/hyprland.conf", config)]
    for rel, text in files:
        full = os.path.join(home, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    stub_dir = os.path.join(d, "stub")
    os.makedirs(stub_dir)
    stub = os.path.join(stub_dir, "hyprctl")
    with open(stub, "w") as fh:
        fh.write(STUB % {"py": sys.executable})
    os.chmod(stub, 0o755)
    with open(os.path.join(stub_dir, "table.json"), "w") as fh:
        json.dump(table, fh)
    return home, stub


def run_live(tool, home, stub):
    p = subprocess.run([sys.executable, "-I", tool, "--home", home, "--live",
                        "--hyprctl", stub], capture_output=True, text=True,
                       env=ENV, timeout=60)
    rows = None
    try:
        rows = json.loads(p.stdout) if p.stdout.strip().startswith("[") else None
    except ValueError:
        rows = None
    return p.returncode, rows, p.stderr


def main():
    ref = open(REF).read()
    tmp = tempfile.mkdtemp(prefix="mado-cgc-")
    try:
        ref_path = os.path.join(tmp, "ref.py")
        with open(ref_path, "w") as fh:
            fh.write(ref)
        n, ok = score(ref_path)
        print("REF fixtures=%s/13" % n)
        rows = []
        for name in sorted(MUTANTS):
            old, new, cls, ev, probe = MUTANTS[name]
            if ref.count(old) != 1:
                print("MUT %-28s MUTATION-TARGET count=%d SKIP"
                      % (name, ref.count(old)))
                rows.append(False)
                continue
            path = os.path.join(tmp, name + ".py")
            with open(path, "w") as fh:
                fh.write(ref.replace(old, new, 1))
            n, last = score(path)
            config, key, rec = probe
            home, stub = make_case(tmp, name, config, {key: rec})
            rc_ref, rows_ref, err_ref = run_live(ref_path, home, stub)
            rc_mut, rows_mut, err_mut = run_live(path, home, stub)

            def label(rs, k):
                if not rs:
                    return None
                for r in rs:
                    if r.get("key") == k:
                        return r.get("agreement")
                return "ABSENT"
            lr, lm = label(rows_ref, key), label(rows_mut, key)
            # the class is proven when the reference sees agreement and the
            # mutant does not (mismatch / config-only / exit 5 / absent)
            wrong = (lm != "agreement")
            good = n == 13 and wrong
            rows.append(good)
            print("MUT %-28s fixtures=%s/13 ref=%s(r%s) mut=%s(r%s) class_wrong=%d ok=%d"
                  % (name, n, lr, rc_ref, lm, rc_mut, int(wrong), int(good)))
            print("    class: %s" % cls)
            print("    evidence: %s" % ev)
        print("CGC: mutants=%d blind_and_wrong=%d/%d"
              % (len(rows), sum(rows), len(rows)))
        for name in sorted(MODEL_PROBES):
            probe, why = MODEL_PROBES[name]
            config, key, rec = probe
            home, stub = make_case(tmp, "probe-" + name, config, {key: rec})
            rc_ref, rows_ref, err_ref = run_live(ref_path, home, stub)
            lab = None
            if rows_ref:
                for r in rows_ref:
                    if r.get("key") == key:
                        lab = r.get("agreement")
            print("MODEL %-24s ref_label=%s rc=%s truth=agreement defect=%d"
                  % (name, lab, rc_ref, int(lab != "agreement")))
            print("    why: %s" % why)
            if rc_ref:
                print("    stderr: %s" % (err_ref.strip().splitlines() or [""])[-1][:120])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
