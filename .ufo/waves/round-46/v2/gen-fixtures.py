#!/usr/bin/env python3
"""Writes quality/counters/c1-r46-fixtures-v2.json: the C1 fixtures of PRED-C1-r46-v2 with their expected output.

Each fixture is a contract case designed by the L1 from the reference contract (the docstring of
.ufo/waves/round-46/v2/mado-devices.py); its expected stdout and exit code are the reference's output on the
placeholder inputs, frozen as bytes. Placeholders {A} {B} {C} {D} are device names the counter substitutes per seed.
Run: python3 -I gen-fixtures.py <lane>   (writes <lane>/quality/counters/c1-r46-fixtures.json)
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ref", os.path.join(HERE, "mado-devices.py"))
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def kb(name, layout="us", variant="", options="", model="", rules=""):
    return ref.kb(name, layout, variant, options, model, rules)


def mouse(name, sf=-1.0):
    return ref.mouse(name, sf)


def D(kbs, mice=(), **extra):
    d = {"mice": list(mice), "keyboards": list(kbs), "tablets": [], "touch": [], "switches": []}
    d.update(extra)
    return d


HOST = ("input {\n  kb_layout = br\n  kb_options = compose:caps # ,grp:alts_toggle\n  repeat_rate = 40\n"
        "  touchpad {\n    scroll_factor = 0.4\n  }\n}\n")
BIG = "# " + "x" * 1048580 + "\n"

# (label, configs | "usage" | None (a directory), dump (dict, or bytes taken verbatim), stdin?)
CASES = [
    ("host", [HOST], D([kb("{A}", "br", options="compose:caps"), kb("hl-virtual-keyboard-{B}", "br", options="compose:caps")],
                       [mouse("{C}")]), False),
    ("host-stdin", [HOST], D([kb("{A}", "br", options="compose:caps")], [mouse("{C}")]), True),
    ("default-us", ["general {\n  gaps_in = 5\n}\n"], D([kb("{A}")]), False),
    ("default-not-us", ["general {\n}\n"], D([kb("{A}", "br")]), False),
    ("global-flat", ["input:kb_layout = de\ninput:kb_variant = nodeadkeys\n"], D([kb("{A}", "de", "nodeadkeys")]), False),
    ("global-differ-two", ["input:kb_layout = de\n"], D([kb("{A}", "us", variant="x")]), False),
    ("fallback", ["input {\n kb_layout = zz\n kb_variant = q\n}\n"], D([kb("{A}")]), False),
    ("fallback-not-when-declared-us", ["input {\n kb_variant = q\n}\n"], D([kb("{A}")]), False),
    ("device-block", ["input:kb_layout = br\ndevice {\n  name = {B}\n  kb_layout = de\n}\n"],
     D([kb("{A}", "br"), kb("{B}", "de")]), False),
    ("device-block-partial", ["input {\nkb_layout = br\nkb_options = compose:caps\n}\ndevice {\nname = {A}\nkb_layout = de\n}\n"],
     D([kb("{A}", "de", options="compose:caps")]), False),
    ("device-block-wrong-key-applies-global", ["input:kb_layout = br\ndevice {\nname = {A}\nkb_layout = de\n}\n"],
     D([kb("{A}", "br")]), False),
    ("device-empty-marker", ["input:kb_variant = intl\ndevice {\nname = {A}\nkb_variant = [[EMPTY]]\n}\n"], D([kb("{A}")]), False),
    ("global-empty-marker", ["input:kb_options = [[EMPTY]]\n"], D([kb("{A}")]), False),
    ("device-empty-rhs", ["input:kb_options = compose:caps\ndevice {\nname = {A}\nkb_options =\n}\n"], D([kb("{A}")]), False),
    ("bracket-flat", ["device[{A}]:kb_layout = fr\n"], D([kb("{A}", "fr")]), False),
    ("bracket-block", ["device[{A}] {\n  kb_layout = fr\n  kb_variant = azerty\n}\n"], D([kb("{A}", "fr", "azerty")]), False),
    ("bracket-name-with-space", ["device[my keyboard]:kb_layout = fr\n"], D([kb("my-keyboard")]), False),
    ("merge-blocks", ["device {\nname = {A}\nkb_layout = fr\n}\ndevice {\nname = {A}\nkb_variant = azerty\n}\n"],
     D([kb("{A}", "fr", "azerty")]), False),
    ("merge-bracket-and-block", ["device {\nname = {A}\nkb_layout = fr\n}\ndevice[{A}]:kb_options = ctrl:nocaps\n"],
     D([kb("{A}", "fr", options="ctrl:nocaps")]), False),
    ("later-file-wins", ["input:kb_layout = de\n", "input {\nkb_layout = br\n}\n"], D([kb("{A}", "br")]), False),
    ("later-line-wins-in-block", ["device {\nname = {A}\nkb_layout = de\nkb_layout = it\n}\n"], D([kb("{A}", "it")]), False),
    ("stale-block", ["device {\nname = Razer DeathAdder\nkb_layout = de\n}\n"], D([kb("{A}")]), False),
    ("case-exact-dump-name", ["device[keyboard-x]:kb_layout = de\n"], D([kb("Keyboard-X")]), False),
    ("stale-uppercase", ["device {\nname = {A}X\n}\n"], D([kb("{A}")]), False),
    ("matched-mouse-block", ["device {\nname = {C}\nsensitivity = 1\n}\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("matched-tablet-pad", ["device {\nname = {D}\n}\n"],
     D([kb("{A}")], tablets=[{"address": "0x3", "type": "tabletPad", "belongsTo": {"address": "0x4", "name": "{D}"}}]), False),
    ("matched-touch", ["device[{D}]:output = DP-1\n"], D([kb("{A}")], touch=[{"address": "0x5", "name": "{D}"}]), False),
    ("virtual", ["input:kb_layout = br\n"], D([kb("hl-virtual-keyboard-{B}", "us")]), False),
    ("virtual-plain-name", ["input:kb_layout = br\n"], D([kb("hl-virtual-keyboard", "us")]), False),
    ("no-keyboards", [HOST], D([], [mouse("{C}")]), False),
    ("no-keyboards-stale", ["device[{D}]:kb_layout = de\n"], D([], [mouse("{C}")]), False),
    ("mouse-block-factor", ["device {\nname = {C}\nscroll_factor = 0.5\n}\n"], D([kb("{A}")], [mouse("{C}", 0.5)]), False),
    ("mouse-global-not-reported", ["input:scroll_factor = 2\n"], D([kb("{A}")], [mouse("{C}", 2.0)]), False),
    ("mouse-touchpad-global-not-reported", [HOST], D([kb("{A}", "br", options="compose:caps")], [mouse("{C}", 0.4)]), False),
    ("mouse-clamp-high", ["device[{C}]:scroll_factor = 250\n"], D([kb("{A}")], [mouse("{C}", 100.0)]), False),
    ("mouse-clamp-low", ["device[{C}]:scroll_factor = -3\n"], D([kb("{A}")], [mouse("{C}", 0.0)]), False),
    ("mouse-stof-prefix", ["device[{C}]:scroll_factor = 0.7x\n"], D([kb("{A}")], [mouse("{C}", 0.7)]), False),
    ("mouse-stof-exponent", ["device[{C}]:scroll_factor = 15e-1\n"], D([kb("{A}")], [mouse("{C}", 1.5)]), False),
    ("mouse-stof-dangling-e", ["device[{C}]:scroll_factor = 2e\n"], D([kb("{A}")], [mouse("{C}", 2.0)]), False),
    ("mouse-stof-none", ["device[{C}]:scroll_factor = fast\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("mouse-round-half-even", ["device[{C}]:scroll_factor = 0.125\n"], D([kb("{A}")], [mouse("{C}", 0.12)]), False),
    ("mouse-float32", ["device[{C}]:scroll_factor = 0.335\n"], D([kb("{A}")], [mouse("{C}", 0.33)]), False),
    ("mouse-nan", ["device[{C}]:scroll_factor = nan\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("mouse-hex", ["device[{C}]:scroll_factor = 0x1p1\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("mouse-overflow", ["device[{C}]:scroll_factor = 1e39\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("mouse-bool", ["general {\n}\n"], D([kb("{A}")], [mouse("{C}", True)]), False),
    ("mouse-string", ["general {\n}\n"], D([kb("{A}")], [mouse("{C}", "-1.00")]), False),
    ("mouse-differ", ["device[{C}]:scroll_factor = 1.5\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("comment-escape", ["input:kb_options = a##b # c\n"], D([kb("{A}", options="a#b")]), False),
    ("comment-triple-hash", ["input:kb_options = a###b\n"], D([kb("{A}", options="a##b")]), False),
    ("comment-line", ["# input:kb_layout = de\n  # device[{A}]:kb_layout = de\ninput:kb_layout = br\n"],
     D([kb("{A}", "br")]), False),
    ("comment-after-brace", ["input { # keyboard\n  kb_layout = br\n} # end\n"], D([kb("{A}", "br")]), False),
    ("continuation", ["input:kb_layout = br,\\\nus\n"], D([kb("{A}", "br,us")]), False),
    ("continuation-spaces", ["input:kb_layout = br  \t\\\n,us\n"], D([kb("{A}", "br,us")]), False),
    ("continuation-last-line", ["input:kb_layout = de\ninput:kb_layout = br\\"], D([kb("{A}", "de")]), False),
    ("crlf", ["input {\r\nkb_layout = br\r\n}\r\n"], D([kb("{A}", "br")]), False),
    ("isspace-trim", ["input:kb_layout =\x0bbr\x0c\n"], D([kb("{A}", "br")]), False),
    ("variable", ["$lay = de\ninput:kb_layout = $lay\n"], D([kb("{A}", "de")]), False),
    ("variable-elsewhere-ignored", ["$mod = SUPER\nbind = $mod, Q, killactive\ninput:kb_layout = br\n"],
     D([kb("{A}", "br")]), False),
    ("expression", ["input:kb_layout = {{1+1}}\n"], D([kb("{A}")]), False),
    ("directive", ["# hyprlang if X\ninput:kb_layout = br\n# hyprlang endif\n"], D([kb("{A}", "br")]), False),
    ("flat-device-key", ["device:kb_layout = de\n"], D([kb("{A}")]), False),
    ("block-first-not-name", ["device {\nkb_layout = de\nname = {A}\n}\n"], D([kb("{A}")]), False),
    ("rename", ["device {\nname = {B}\nname = {A}\nkb_layout = de\n}\n"], D([kb("{A}")]), False),
    ("bracket-name-key", ["device[{B}]:name = {A}\n"], D([kb("{A}")]), False),
    ("kb-file", ["input:kb_file = ~/x.xkb\n"], D([kb("{A}")]), False),
    ("nested-not-input", ["general {\n  kb_layout = de\n}\n"], D([kb("{A}")]), False),
    ("inline-block-not-modelled", ["input { kb_layout = de }\n"], D([kb("{A}")]), False),
    ("input-touchpad-kb-ignored", ["input {\n  touchpad {\n    kb_layout = de\n  }\n}\n"], D([kb("{A}")]), False),
    ("missing-field", ["general {\n}\n"], D([{"name": "{A}", "layout": "us"}]), False),
    ("non-string-field", ["general {\n}\n"], D([dict(kb("{A}"), variant=None)]), False),
    ("block-reset-after-close", ["device {\nname = {B}\n}\ndevice {\nname = {A}\nkb_layout = de\n}\n"],
     D([kb("{A}", "de"), kb("{B}")]), False),
    ("not-compared-beats-differ", ["$x = 1\ninput:kb_layout = $x\n"], D([kb("{A}", "de")]), False),
    ("differ-beats-stale", ["input:kb_layout = de\ndevice[{D}]:kb_layout = fr\n"], D([kb("{A}")]), False),
    ("options-commas", ["input:kb_options = grp:alts_toggle,compose:caps,ctrl:nocaps\n"],
     D([kb("{A}", options="grp:alts_toggle,compose:caps,ctrl:nocaps")]), False),
    ("multi-layout", ["input {\nkb_layout = us,br\nkb_variant = ,abnt2\n}\n"], D([kb("{A}", "us,br", ",abnt2")]), False),
    ("model-rules", ["input {\nkb_model = pc105\nkb_rules = evdev\n}\n"], D([kb("{A}", model="pc105", rules="evdev")]), False),
    ("three-keyboards-mixed", ["input:kb_layout = br\ndevice[{B}]:kb_layout = us\n"],
     D([kb("{A}", "br"), kb("{B}", "br"), kb("hl-virtual-keyboard-{C}", "zz")]), False),
    ("unicode-name", ["device[t\u00e9clado]:kb_layout = fr\n"], D([kb("t\u00e9clado", "fr")]), False),
    ("extra-keys-ignored", ["general {\n}\n"], D([dict(kb("{A}"), extra=1)], extra=[1, 2]), False),
    # v2 additions (w1/ExecStofOracle, w1/ExecHyprlangOracleB, w1/CritToolSemantics)
    ("v2-hex-factor", ["device[{C}]:scroll_factor = 0x10\n"], D([kb("{A}")], [mouse("{C}", 16.0)]), False),
    ("v2-hex-fraction", ["device[{C}]:scroll_factor = 0X.8p1\n"], D([kb("{A}")], [mouse("{C}", 1.0)]), False),
    ("v2-hex-bare", ["device[{C}]:scroll_factor = 0x\n"], D([kb("{A}")], [mouse("{C}", 0.0)]), False),
    ("v2-inf-clamps-high", ["device[{C}]:scroll_factor = Infinity\n"], D([kb("{A}")], [mouse("{C}", 100.0)]), False),
    ("v2-neg-inf-clamps-low", ["device[{C}]:scroll_factor = -inf\n"], D([kb("{A}")], [mouse("{C}", 0.0)]), False),
    ("v2-overflow-unset", ["device[{C}]:scroll_factor = 4e38\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("v2-overflow-keeps-earlier", ["device {\nname = {C}\nscroll_factor = 2\nscroll_factor = 1e39\n}\n"],
     D([kb("{A}")], [mouse("{C}", 2.0)]), False),
    ("v2-flt-max-clamps", ["device[{C}]:scroll_factor = 3.4028235e38\n"], D([kb("{A}")], [mouse("{C}", 100.0)]), False),
    ("v2-underflow-unset", ["device[{C}]:scroll_factor = 1e-46\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("v2-subnormal-unset", ["device[{C}]:scroll_factor = 1e-40\n"], D([kb("{A}")], [mouse("{C}")]), False),
    ("v2-flt-min-stored", ["device[{C}]:scroll_factor = 1.17549435e-38\n"], D([kb("{A}")], [mouse("{C}", 0.0)]), False),
    ("v2-single-rounding", ["device[{C}]:scroll_factor = 0.00500000012107193470001220703125000000000000000000001\n"],
     D([kb("{A}")], [mouse("{C}", 0.01)]), False),
    ("v2-final-continuation-dropped", ["input:kb_layout = br\ninput:kb_layout = de\\\n"], D([kb("{A}", "br")]), False),
    ("v2-final-continuation-no-newline", ["input:kb_layout = br\ninput:kb_layout = de\\"], D([kb("{A}", "br")]), False),
    ("v2-directive-suffix", ["#hyprlangfoo if X\ninput:kb_layout = br\n"], D([kb("{A}", "br")]), False),
    ("v2-hyprlang-word-no-keyword", ["#hyprlangx a note\ninput:kb_layout = br\n"], D([kb("{A}", "br")]), False),
    ("v2-directive-noerror", ["# hyprlang noerror true\ninput:kb_layout = br\n"], D([kb("{A}", "br")]), False),
    ("v2-vt-before-directive", ["\x0b# hyprlang if X\ninput:kb_layout = br\n"], D([kb("{A}", "br")]), False),
    ("v2-source-in-block", ["device {\nname = {A}\nsource = x.conf\nkb_layout = fr\n}\n"], D([kb("{A}")]), False),
    ("v2-source-top-ignored", ["source = x.conf\ninput:kb_layout = br\n"], D([kb("{A}", "br")]), False),
    ("setup-usage-no-config", "usage", D([kb("{A}")]), False),
    ("setup-config-dir", None, D([kb("{A}")]), False),
    ("setup-not-object", ["general {\n}\n"], b"[]", False),
    ("setup-no-mice", ["general {\n}\n"], b'{"keyboards": []}', False),
    ("setup-mouse-not-object", ["general {\n}\n"], b'{"keyboards": [], "mice": [1]}', False),
    ("setup-name-not-string", ["general {\n}\n"], b'{"keyboards": [{"name": 7}], "mice": []}', False),
    ("setup-deep-json", ["general {\n}\n"], b"[" * 200000, False),
    ("setup-bad-utf8", ["general {\n}\n"], b'{"keyboards": [], "mice": [], "x": "\xff"}', False),
    ("setup-config-too-large", ["@BIG"], D([kb("{A}")]), False),
    ("setup-dump-too-large", ["general {\n}\n"], b"@BIGDUMP", True),
]


def expected(configs, dump):
    raw = dump if isinstance(dump, bytes) else json.dumps(dump).encode()
    if configs == "usage":
        return ["MADO_DEVICES: SETUP usage"], 2
    if configs is None:
        return ["MADO_DEVICES: SETUP unreadable"], 2
    if "@BIG" in configs or raw == b"@BIGDUMP":
        return ["MADO_DEVICES: SETUP too_large"], 2
    try:
        return ref.report(raw, configs)
    except ref.Setup as e:
        return ["MADO_DEVICES: SETUP %s" % e], 2


def main():
    lane = sys.argv[1]
    out = []
    for label, configs, dump, stdin in CASES:
        lines, rc = expected(configs, dump)
        out.append({"label": label, "configs": configs,
                    "dump": dump.decode("latin-1") if isinstance(dump, bytes) else dump,
                    "dump_bytes": isinstance(dump, bytes), "stdin": stdin, "expect": lines, "rc": rc})
    labels = [c["label"] for c in out]
    assert len(set(labels)) == len(labels)
    p = os.path.join(lane, "quality", "counters", "c1-r46-fixtures-v2.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=True)
        f.write("\n")
    print(len(out), "fixtures ->", p)
    for c in out:
        print(c["rc"], c["label"], c["expect"][-1][-40:])


if __name__ == "__main__":
    main()
