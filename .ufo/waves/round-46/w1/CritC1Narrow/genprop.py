#!/usr/bin/env python3
"""CritC1Narrow: build proposed catching fixtures for the surviving holes; verify ref passes them and the variant fails."""
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
SCR = "/fast/scratch/hyaku/mado-r46/CritC1Narrow"
SEAT = os.path.join(LANE, ".ufo/waves/round-46/w1/CritC1Narrow")


def kb(name, layout="us", variant="", options="", model="", rules=""):
    return {"address": "0x1", "name": name, "rules": rules, "model": model, "layout": layout, "variant": variant,
            "options": options, "active_layout_index": 0, "active_keymap": "x", "capsLock": False, "numLock": False,
            "main": False}


def mouse(name, sf=-1.0):
    return {"address": "0x2", "name": name, "defaultSpeed": 0.0, "scrollFactor": sf}


def dump(kbs, mice=(), **extra):
    d = {"mice": list(mice), "keyboards": list(kbs), "tablets": [], "touch": [], "switches": []}
    d.update(extra)
    return d


PROPOSALS = [
    # hole -> (variant, label, configs, dump, dump_bytes, stdin)
    ("P01-single-continuation", "continuation-three-lines",
     ["input {\n  kb_options = grp:alts_toggle,\\\ncompose:caps,\\\nctrl:nocaps\n}\n"],
     dump([kb("kbd-1", options="grp:alts_toggle,compose:caps,ctrl:nocaps")]), None, False),
    ("P02-source-unsupported", "source-line-not-unsupported",
     ["source = ~/.config/hypr/input.conf\ninput:kb_layout = br\n"], dump([kb("kbd-1", "br")]), None, False),
    ("P03-indented-directive", "directive-indented",
     ["input {\n  # hyprlang noerror true\n  kb_layout = br\n}\n"], dump([kb("kbd-1", "br")]), None, False),
    ("P04-comma-space-trim", "kb-options-space-after-comma",
     ["input:kb_options = grp:alts_toggle, compose:caps\n"],
     dump([kb("kbd-1", options="grp:alts_toggle, compose:caps")]), None, False),
    ("P05-bracket-input-ignored", "bracket-input-sets-global",
     ["input[usb]:kb_layout = de\n"], dump([kb("kbd-1", "de")]), None, False),
    ("P07-nonfinite-reported", "mouse-nan-reported-token",
     ["general {\n}\n"], None,
     b'{"keyboards": [{"name": "kbd-1", "layout": "us", "variant": "", "options": "", "model": "", "rules": ""}],'
     b' "mice": [{"name": "mouse-1", "scrollFactor": NaN}]}', False),
    ("P09-int-not-number", "mouse-int-scrollfactor",
     ["device[mouse-1]:scroll_factor = 2\n"], dump([kb("kbd-1")], [mouse("mouse-1", 2)]), None, False),
    ("P11-size-boundary", "config-exactly-max-bytes", ["@EXACT"], dump([kb("kbd-1")]), None, False),
    ("P13-stack-shared", "stack-reset-per-file",
     ["device {\n  name = mouse-1\n", "scroll_factor = 2\n"], dump([kb("kbd-1")], [mouse("mouse-1")]), None, False),
    ("P15-case-sensitive-special", "mouse-special-uppercase",
     ["device[mouse-1]:scroll_factor = NaN\n"], dump([kb("kbd-1")], [mouse("mouse-1")]), None, False),
    ("P16-virtual-contains", "virtual-prefix-not-substring",
     ["input:kb_layout = br\n"], dump([kb("usb-hl-virtual-keyboard-uinput")]), None, False),
    ("P19-brace-needs-space", "block-opener-no-space",
     ["input{\n  kb_layout = br\n}\n"], dump([kb("kbd-1", "br")]), None, False),
    ("P21-no-cr-strip", "leading-cr-directive",
     ["\r# hyprlang if X\ninput:kb_layout = us\n"], dump([kb("kbd-1")]), None, False),
    ("P22-bom-stripped", "config-bom-before-first-key",
     ["\ufeffinput:kb_layout = br\n"], dump([kb("kbd-1", "br")]), None, False),
    ("P23-switch-name-ignored", "matched-switch",
     ["device[switch-1]:kb_layout = de\n"], dump([kb("kbd-1")], switches=[{"address": "0x6", "name": "switch-1"}]), None, False),
]
EXACT_BYTES = "#" + "x" * 1048574 + "\n"   # exactly 1048576 bytes, all one comment line


def run(tool, args, d, data=None):
    p = subprocess.run([sys.executable, "-I", tool] + args, capture_output=True, input=data, cwd=d)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr


def main():
    out = []
    for variant, label, configs, d, dump_bytes, use_stdin in PROPOSALS:
        dd = tempfile.mkdtemp(dir=SCR, prefix="pf-")
        if dump_bytes is not None:
            raw = dump_bytes
        else:
            raw = json.dumps(d).encode()
        dp = os.path.join(dd, "devices.json")
        open(dp, "wb").write(raw)
        args = ["--devices", dp]
        for i, text in enumerate(configs):
            cp = os.path.join(dd, "c%d.conf" % i)
            body = EXACT_BYTES if text == "@EXACT" else text
            with open(cp, "w", newline="", encoding="utf-8") as f:
                f.write(body)
            args += ["--config", cp]
        rc_ref, out_ref, err_ref = run(REF, args, dd)
        var = os.path.join(SCR, "work-%s" % variant, "mado-devices.py")
        rc_var, out_var, err_var = run(var, args, dd)
        ok_ref = err_ref == b"" and out_ref.strip() != ""
        catch = (rc_ref, out_ref) != (rc_var, out_var) or err_var != err_ref
        entry = {"label": label, "hole": variant, "configs": configs, "stdin": use_stdin,
                 "dump_bytes": (dump_bytes.decode("utf-8", "backslashreplace") if dump_bytes is not None else None),
                 "dump": None if dump_bytes is not None else d, "rc": rc_ref,
                 "expect": out_ref.rstrip("\n").split("\n") if out_ref else []}
        out.append(entry)
        print("%-34s ref_rc=%d var_rc=%d catches=%s stderr_var=%r\n   ref_last=%r\n   var_last=%r" % (
            label, rc_ref, rc_var, catch, err_var[-60:],
            (out_ref.rstrip("\n").split("\n") or [""])[-1][:150],
            (out_var.rstrip("\n").split("\n") or [""])[-1][:150]))
        if not ok_ref:
            print("   !! reference output empty or stderr non-empty")
    os.makedirs(SEAT, exist_ok=True)
    with open(os.path.join(SEAT, "proposed-fixtures.json"), "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
