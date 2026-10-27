#!/usr/bin/env python3
"""probe.py - score quality/check-session-material.py against round-49 receipt shapes.

Every fixture value is synthetic (reserved namespaces: /home/example,
synthetic-*).  The script prints class ids, rules and counts only - never a
value - so its stdout is safe to paste into a receipt.

The four positive controls are assembled from parts, exactly as the gate's own
selftest does, so this file's bytes never trip R1/R2/R3 by themselves.
"""

import importlib.util
import json
import os
import sys

GATE = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py"
HOME_LIMIT = 10

spec = importlib.util.spec_from_file_location("csm", GATE)
csm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csm)


def j(parts):
    return "".join(parts)


BIND_KEYS = ["modmask", "submap", "key", "keycode", "mouse", "catch_all",
             "description", "has_description", "dispatcher", "arg"]

BINDS_FULL = [
    {"modmask": 64, "submap": "", "key": "S", "keycode": 0, "mouse": False,
     "catch_all": False, "description": "synthetic terminal on workspace 1",
     "has_description": True, "dispatcher": "exec",
     "arg": "~/.config/hypr/scripts/synthetic-launch-term"},
    {"modmask": 64, "submap": "", "key": "slash", "keycode": 0, "mouse": False,
     "catch_all": False, "description": "", "has_description": False,
     "dispatcher": "exec", "arg": "/home/example/.local/bin/synthetic-menu --pick"},
    {"modmask": 65, "submap": "", "key": "Q", "keycode": 0, "mouse": False,
     "catch_all": False, "description": "synthetic lock screen",
     "has_description": True, "dispatcher": "exec",
     "arg": "sh -c 'synthetic-locker --private-profile'"},
]

BINDS_SHAPE = [
    {"modmask": 64, "submap": "", "key": "S", "keycode": 0, "mouse": False,
     "catch_all": False},
    {"modmask": 64, "submap": "", "key": "slash", "keycode": 0, "mouse": False,
     "catch_all": False},
]

DEVICES = [
    {"name": "synthetic-keyboard-1", "address": "/dev/input/event3", "layout": "br",
     "active_layout_index": 0, "capsLock": False, "numLock": False},
    {"name": "synthetic-mouse-1", "address": "/dev/input/event5", "scrollFactor": 1.0},
]

KEYMAP = """xkb_keymap {
xkb_keycodes "br+aliases(qwerty)" { include "evdev+aliases(qwerty)" };
xkb_types "pc+br" { include "complete" };
xkb_symbols "pc+br" {
    key <AD01> { type[Group1]="FOUR_LEVEL", [ q, Q, slash, question ] };
    key <AB11> { [ slash, question ] };
};
};
"""

KEYMAP_USER = """xkb_keymap {
xkb_symbols "pc+br+synthetic(override)" {
    key <AB11> { [ slash, question ] };
    key <I9> { [ XF86Launch1 ] };
};
};
"""

KEYMAP_VERBOSE = """xkbcommon: INFO: Include path failed: "/home/example/.config/xkb"
xkbcommon: INFO: Adding include path "/usr/share/X11/xkb"
xkb_keymap {
xkb_symbols "pc+br" { key <AB11> { [ slash, question ] }; };
};
"""

INPUT_CONF = """input {
    kb_layout = br
    kb_options = compose:caps
    follow_mouse = 1
    device {
        name = synthetic-keyboard-1
        sensitivity = 0
    }
}
"""

HYPR_CONF = """bind = SUPER, S, exec, ~/.config/hypr/scripts/synthetic-launch-term
bind = SUPER, slash, exec, /home/example/.local/bin/synthetic-menu
bind = SUPER SHIFT, Q, exec, synthetic-locker --private-profile
"""

BIND_KEYS_TABLE = """keysym            keycode  layout  level  mods
slash             AD01     0       3      [ Mod5 ]
slash             AD01     0       4      [ Shift Mod5 ]
slash             AB11     0       1      [ ]
"""


def rows(n, fmt):
    return "\n".join(fmt(i) for i in range(n)) + "\n"


FIXTURES = {
    # --- host material this round's seats can put on disk ---------------
    "P01_binds_json_arg_home_and_script": json.dumps(BINDS_FULL, indent=2) + "\n",
    "P02_binds_table_arg": ("| modmask | key | dispatcher | arg |\n|---|---|---|---|\n"
                            "| 64 | S | exec | ~/.config/hypr/scripts/synthetic-launch |\n"
                            "| 64 | slash | exec | /home/example/.local/bin/synthetic-menu |\n"),
    "P03_bind_description_prose": ("binds: three custom ones name synthetic-project "
                                   "scratch terminals and a synthetic-locker profile.\n"),
    "P04_devices_json": json.dumps(DEVICES, indent=2) + "\n",
    "P05_keymap_verbose_paths": KEYMAP_VERBOSE,
    "P06_input_conf_paste": INPUT_CONF,
    "P07_ls_owner_columns": rows(12, lambda i: "-rw-r--r-- 1 example example %d "
                                 "2026-10-27 10:00 /home/example/.config/hypr/conf.d/%02d.conf" % (100 + i, i)),
    "P08_tilde_listing": rows(12, lambda i: "~/.config/hypr/conf.d/%02d-synthetic.conf" % i),
    "P09_inline_home_prefix": rows(12, lambda i: "/home/example/.config/hypr/conf.d/%02d.conf:%d:bind = SUPER, S, exec, synthetic" % (i, i + 1)),
    "P10_flat_ls_header": "/home/example/.local/share/applications:\n" + rows(
        12, lambda i: "-rw-r--r-- 1 example example 512 synthetic-app-%02d.desktop" % i),
    "P11_cache_text": ("1\tsynthetic-app\t/home/example/.local/share/applications/synthetic-app.desktop\n"
                       "2\tsynthetic-terminal\t--title=synthetic window title\n"
                       "3\tsynthetic-dir\t--dir=/home/example/Projects/synthetic\n"),
    "P14_hypr_conf_bind_lines": HYPR_CONF,
    "P15_keymap_user_override": KEYMAP_USER,
    "P16_scratch_root_listing": rows(12, lambda i: "/fast/scratch/synthetic/work-%02d/out.txt" % i),
    "P17_ps_aux_rows": ("USER PID %CPU %MEM COMMAND\n"
                        "example 4242 0.0 0.1 synthetic-locker --private-profile\n"
                        "example 4243 0.0 0.1 synthetic-agent --token-file\n") * 3,
    "P18_device_names_prose": ("keyboard list on the host: synthetic-keyboard-1, "
                                "synthetic-keyboard-2; pointer: synthetic-mouse-1.\n"),
    # --- controls: receipts the seats are told to produce (must be clean) -
    "K01_binds_shape_only": ("# command: hyprctl binds -j (fields key,keycode,modmask,mouse,catch_all,submap)\n"
                              "# raw sha256: " + "0" * 64 + "\n"
                              + json.dumps(BINDS_SHAPE, indent=2) + "\n"),
    "K02_keysym_table": BIND_KEYS_TABLE,
    "K03_compiled_keymap": KEYMAP,
    "K04_keysym_header_fragment": ("#define XKB_KEY_slash 0x02f\n"
                                    "#define XKB_KEY_Return 0xff0d\n"),
    # --- controls the gate is known to catch -----------------------------
    "C01_bare_home_listing_12": rows(12, lambda i: "/home/example/dir%02d/file.txt" % i),
    "C02_client_dump": j(['[{"class": "synthetic-term', 'inal", "ti', 'tle": "synthetic window ti',
                          'tle"}]']) + "\n",
    "C03_ss_row": j(['u_str ESTAB 0 0 * 3001 * 2001 users:(("synthetic-cli',
                      'ent",p', 'id=42,fd=7))']) + "\n",
    "C04_monitor_ident": j(['[{"seri', 'al": "SN0123456", "make": "Fake", ',
                            '"model": "FakePanel"}]']) + "\n",
}

MATERIAL = {k for k in FIXTURES if k.startswith("P")}


def score(name, text):
    findings = csm.scan_blob(text.encode("utf-8"), HOME_LIMIT)
    rules = sorted({rule for rule, _count, _detail in findings})
    return {"class": name, "material": name in MATERIAL,
            "bytes": len(text.encode("utf-8")), "rules": rules,
            "findings": [(r, c) for r, c, _d in findings]}


def main():
    out = [score(n, t) for n, t in FIXTURES.items()]
    missed = [r["class"] for r in out if r["material"] and not r["rules"]]
    caught = [r["class"] for r in out if r["material"] and r["rules"]]
    noise = [r["class"] for r in out if not r["material"] and r["rules"]]
    for r in out:
        print("%-34s %-8s bytes=%-6d rules=%s"
              % (r["class"], "material" if r["material"] else "control",
                 r["bytes"], ",".join(r["rules"]) or "NONE"))
    print()
    print("PROBE: fixtures=%d material=%d material_caught=%d material_missed=%d control_noise=%d"
          % (len(out), len(MATERIAL), len(caught), len(missed), len(noise)))
    print("MISSED: " + " ".join(missed))
    payload = {"gate": GATE, "gate_sha256": csm.sha256_hex(open(GATE, "rb").read()),
               "home_limit": HOME_LIMIT, "results": out,
               "material_caught": caught, "material_missed": missed,
               "control_noise": noise}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "probe-results.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
