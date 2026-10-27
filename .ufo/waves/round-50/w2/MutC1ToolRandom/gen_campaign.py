#!/usr/bin/env python3
"""MutC1ToolRandom round-50 w2 campaign generator (deterministic, seeded).

Generates:
  - 400 random RMLVO keymap specs (xkeyboard-config 2.48 evdev rules)
  - 57,865 random (keymap index, keysym argument) pairs
  - an exotic spec list (multi-group, dead keys, LevelThree/LevelFive, compose)

Seeds are fixed integers committed to the seat dir; the full campaign spec is
written as JSON so the run is reproducible without re-running this generator.
"""
import json
import os
import random
import re
import sys

SEED_KEYMAPS = 0x52534B4D  # "RSKM"
SEED_PAIRS = 0x52504152    # "RPAR"
SEED_EXOTIC = 0x45584F54   # "EXOT"
N_KEYMAPS = 400
N_PAIRS = 57865
ALGO = "mutc1toolrandom-gen-v1"

LST = "/usr/share/X11/xkb/rules/evdev.lst"
HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"

def parse_lst(path):
    sections = {}
    cur = None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("! "):
                cur = line[2:].strip()
                sections[cur] = []
            elif cur and line.strip():
                sections[cur].append(line.split()[0])
    return sections

def parse_header_names(path):
    names = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"#define\s+XKB_KEY_([A-Za-z0-9_]+)\s+", line)
            if m:
                names.append(m.group(1))
    return names

def main(out_path):
    sec = parse_lst(LST)
    layouts = [layout for layout in sec["layout"] if layout != "custom"]
    variants = sec["variant"]
    options = sec["option"]
    models = sec["model"]
    names = parse_header_names(HEADER)

    # variants are layout-specific: build layout -> [variants] from evdev.xml
    import xml.etree.ElementTree as ET
    rt = ET.parse("/usr/share/X11/xkb/rules/evdev.xml").getroot()
    lvar = {}
    for lay in rt.iter("layout"):
        ci = lay.find("configItem")
        if ci is None:
            continue
        nm = ci.find("name").text
        vs = []
        vl = lay.find("variantList")
        if vl is not None:
            for v in vl.findall("variant"):
                vci = v.find("configItem")
                if vci is not None:
                    vs.append(vci.find("name").text)
        lvar[nm] = vs
    rng = random.Random(SEED_KEYMAPS)
    specs = []
    seen = set()
    common_models = ["pc105", "pc104", "pc102", "pc86"]
    while len(specs) < N_KEYMAPS:
        if rng.random() < 0.7:
            model = rng.choice(common_models)
        else:
            model = rng.choice(models)
        nlay = rng.choices([1, 2, 3], weights=[55, 35, 10])[0]
        lay = []
        var = []
        used = set()
        for _ in range(nlay):
            l = rng.choice(layouts)
            if l in used:
                continue
            used.add(l)
            lay.append(l)
            vl = lvar.get(l, [])
            if vl and rng.random() < 0.55:
                var.append(rng.choice(vl))
            else:
                var.append("")
        if not lay:
            continue
        nopt = rng.choices([0, 1, 2, 3], weights=[45, 30, 15, 10])[0]
        opts = rng.sample(options, nopt) if nopt else []
        key = (model, tuple(lay), tuple(var), tuple(opts))
        if key in seen:
            continue
        seen.add(key)
        specs.append({
            "model": model,
            "layout": ",".join(lay),
            "variant": ",".join(var),
            "options": ",".join(opts),
        })

    # Pairs
    rngp = random.Random(SEED_PAIRS)
    u_forms = [f"U{i:04X}" for i in range(0x20, 0x2FFF)]
    invalid = ["NoSuchKeysym", "a_b_c_d_e_f", "XKB_KEY_a", "keysym_a", "DEAD_ACUTE_X"]
    dead_names = [n for n in names if n.startswith("dead_")]
    xf86_names = [n for n in names if n.startswith("XF86")]
    pairs = []
    for _ in range(N_PAIRS):
        ki = rngp.randrange(N_KEYMAPS)
        r = rngp.random()
        if r < 0.55:
            arg = rngp.choice(names)
        elif r < 0.62:
            arg = rngp.choice(u_forms)
        elif r < 0.68:
            arg = "0x%x" % rngp.randrange(1, 0x10000000)
        elif r < 0.74:
            arg = str(rngp.randrange(1, 0x10000000))
        elif r < 0.79:
            arg = rngp.choice(dead_names)
        elif r < 0.84:
            arg = rngp.choice(xf86_names)
        elif r < 0.93:
            arg = rngp.choice(invalid)
        else:
            arg = rngp.choice(names)
        pairs.append([ki, arg])

    # Exotic targeted specs (deterministic list; no RNG needed)
    exot_specs = [
        # multi-group
        {"model": "pc105", "layout": "us,ru", "variant": ",", "options": ""},
        {"model": "pc105", "layout": "us,ru", "variant": ",winkeys", "options": "grp:alt_shift_toggle"},
        {"model": "pc105", "layout": "us,de,fr", "variant": ",,", "options": "grp:ctrl_alt_toggle"},
        {"model": "pc105", "layout": "jp", "variant": "", "options": ""},
        {"model": "pc105", "layout": "kr", "variant": "", "options": ""},
        {"model": "pc105", "layout": "in", "variant": "", "options": ""},
        {"model": "pc105", "layout": "ara", "variant": "", "options": "grp:alt_shift_toggle"},
        {"model": "pc105", "layout": "il", "variant": "", "options": ""},
        {"model": "pc105", "layout": "th", "variant": "", "options": ""},
        {"model": "pc105", "layout": "kp", "variant": "", "options": ""},
        {"model": "pc105", "layout": "cn", "variant": "", "options": ""},
        {"model": "pc105", "layout": "tw", "variant": "", "options": ""},
        {"model": "pc105", "layout": "bg", "variant": ",phonetic", "options": "grp:lwin_toggle"},
        {"model": "pc105", "layout": "rs", "variant": ",latin", "options": "grp:menu_toggle"},
        # dead keys / intl
        {"model": "pc105", "layout": "us", "variant": "intl", "options": ""},
        {"model": "pc105", "layout": "us", "variant": "intl", "options": "compose:ralt"},
        {"model": "pc105", "layout": "us", "variant": "altgr-intl", "options": ""},
        {"model": "pc105", "layout": "br", "variant": "nativo-us", "options": ""},
        {"model": "pc105", "layout": "fr", "variant": "oss", "options": ""},
        {"model": "pc105", "layout": "de", "variant": "neo", "options": ""},
        # LevelThree / LevelFive
        {"model": "pc105", "layout": "us", "variant": "", "options": "lv3:ralt_switch"},
        {"model": "pc105", "layout": "us", "variant": "", "options": "lv3:menu_switch,compose:menu"},
        {"model": "pc105", "layout": "pl", "variant": "", "options": "lv3:lwin_switch"},
        {"model": "pc105", "layout": "de", "variant": "", "options": "lv5:rctrl_switch,lv3:ralt_switch"},
        {"model": "pc105", "layout": "gb", "variant": "extd", "options": "lv3:ralt_switch,compose:rwin"},
        # compose + keypad + misc
        {"model": "pc105", "layout": "us", "variant": "", "options": "compose:paus"},
        {"model": "pc105", "layout": "us", "variant": "", "options": "keypad:overlay1,keypad:pointerkeys"},
        {"model": "pc104", "layout": "us", "variant": "", "options": "ctrl:nocaps,shift:both_capslock"},
        {"model": "pc105", "layout": "latam", "variant": "", "options": "lv3:ralt_switch"},
        {"model": "pc105", "layout": "es", "variant": "deadtilde", "options": ""},
        {"model": "pc105", "layout": "se", "variant": "svdvorak", "options": "lv3:ralt_switch"},
    ]

    doc = {
        "algo": ALGO,
        "seeds": {"keymaps": SEED_KEYMAPS, "pairs": SEED_PAIRS, "exotic": SEED_EXOTIC},
        "n_keymaps": N_KEYMAPS,
        "n_pairs": N_PAIRS,
        "name_pool_size": len(names),
        "keymaps": specs,
        "pairs": pairs,
        "exotic": exot_specs,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
    print(f"wrote {out_path}: keymaps={len(specs)} pairs={len(pairs)} exotic={len(exot_specs)} names={len(names)}")

if __name__ == "__main__":
    main(sys.argv[1])
