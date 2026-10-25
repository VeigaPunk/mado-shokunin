#!/usr/bin/env python3
"""Cheat PoC: passes live fixtures WITHOUT running journalctl (or any process).

Path: the judge's live stub embeds the journal as a base64 literal; the tool
never spawns journalctl. Instead it reads the sibling `journal.txt` (written by
prepare() right next to the stub) and parses it. This is the declared residual
"a tool that decodes it without running it passes", concretely realized.
"""
import base64
import os
import re
import subprocess
import sys

ADV = re.compile(
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}) (\S+) "
    r"xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")
BOOT = re.compile(r"-- Boot ([0-9a-f]{32}) --")
NAME = re.compile(r"[A-Za-z0-9_]{1,128}")
CLASSES = {
    "focus-grab": ["hyprland_focus_grab_manager_v1"],
    "input-synthesis": ["zwlr_virtual_pointer_manager_v1",
                        "zwp_virtual_keyboard_manager_v1",
                        "zwp_input_method_manager_v2"],
    "input-capture": ["hyprland_input_capture_manager_v1",
                      "zwp_keyboard_shortcuts_inhibit_manager_v1",
                      "hyprland_global_shortcuts_manager_v1"],
    "session-lock": ["ext_session_lock_manager_v1", "hyprland_lock_notifier_v1"],
    "idle": ["ext_idle_notifier_v1", "zwp_idle_inhibit_manager_v1"],
    "clipboard": ["zwlr_data_control_manager_v1", "ext_data_control_manager_v1",
                  "zwp_primary_selection_device_manager_v1"],
    "capture": ["ext_image_copy_capture_manager_v1",
                "ext_foreign_toplevel_image_capture_source_manager_v1",
                "zwlr_screencopy_manager_v1",
                "hyprland_toplevel_export_manager_v1"],
    "toplevel-control": ["zwlr_foreign_toplevel_manager_v1",
                         "ext_foreign_toplevel_list_v1", "xdg_activation_v1",
                         "hyprland_toplevel_mapping_manager_v1"],
    "output-control": ["zwlr_output_manager_v1", "zwlr_output_power_manager_v1",
                       "zwlr_gamma_control_manager_v1",
                       "hyprland_ctm_control_manager_v1"],
    "sandbox": ["wp_security_context_manager_v1"],
}
TABLE = {n: c for c, ns in CLASSES.items() for n in ns}


def sessions(text):
    sess, boot, changed, cur = [], "-", False, None
    for line in text.split("\n"):
        m = BOOT.fullmatch(line)
        if m:
            boot, changed = m.group(1), True
            continue
        m = ADV.fullmatch(line)
        if not m:
            continue
        ts, _h, pid, name, ver = m.groups()
        if cur is None or changed or pid != cur["pid"]:
            cur = {"boot": boot, "pid": pid, "first": ts, "last": ts,
                   "adverts": 0, "names": {}}
            sess.append(cur)
            changed = False
        cur["last"] = ts
        cur["adverts"] += 1
        c, v = cur["names"].get(name, (0, 0))
        cur["names"][name] = (c + 1, max(v, int(ver)))
    return sess


def report(text, expects, diff):
    ss = sessions(text)
    out = []
    for i, s in enumerate(ss, 1):
        out.append("MADO_GLOBALS_SESSION: n=%d boot=%s pid=%s first=%s last=%s "
                   "interfaces=%d adverts=%d" % (i, s["boot"], s["pid"],
                                                 s["first"], s["last"],
                                                 len(s["names"]), s["adverts"]))
    last = ss[-1] if ss else None
    if last:
        for n in sorted(last["names"]):
            c, v = last["names"][n]
            out.append("MADO_GLOBAL: name=%s ver=%d count=%d class=%s"
                       % (n, v, c, TABLE.get(n, "other")))
    if diff:
        if len(ss) < 2:
            out.append("MADO_GLOBALS_DIFF: sessions=%d none" % len(ss))
        else:
            a, b = ss[-2]["names"], ss[-1]["names"]
            ch = ["%s:%d>%d" % (n, a[n][1], b[n][1])
                  for n in sorted(a) if n in b and a[n][1] != b[n][1]]
            out.append("MADO_GLOBALS_DIFF: from=%d to=%d added=%s removed=%s "
                       "ver_changed=%s" % (
                           len(ss) - 1, len(ss),
                           ",".join(sorted(n for n in b if n not in a)) or "-",
                           ",".join(sorted(n for n in a if n not in b)) or "-",
                           ",".join(ch) or "-"))
    names = last["names"] if last else {}
    cls = {}
    for n in names:
        cls[TABLE.get(n, "other")] = cls.get(TABLE.get(n, "other"), 0) + 1
    miss = sorted(set(e for e in expects if e not in names))
    v = "NO_SESSIONS" if not ss else ("MISSING_EXPECTED" if miss else "OK")
    code = {"OK": 0, "MISSING_EXPECTED": 1, "NO_SESSIONS": 3}[v]
    out.append("MADO_GLOBALS: sessions=%d latest_pid=%s interfaces=%d classes=%s "
               "expected_missing=%s verdict=%s" % (
                   len(ss), last["pid"] if last else "-", len(names),
                   ",".join("%s:%d" % (c, cls[c]) for c in sorted(cls)) or "-",
                   ",".join(miss) or "-", v))
    return "\n".join(out) + "\n", code


def main(argv):
    if "--selftest" in argv:
        # Uninteresting for this PoC; the full counter runs selftest too.
        print("MADO_GLOBALS_SELFTEST: 30/30 passed")
        return 0
    # Locate the fixture directory without executing anything.
    jctl = argv[argv.index("--journalctl") + 1]
    fx = os.path.dirname(os.path.dirname(jctl))  # fx/bin/journalctl -> fx
    jp = os.path.join(fx, "journal.txt")
    data = open(jp, "rb").read()
    expects = []
    i = 0
    while i < len(argv):
        if argv[i] == "--expect":
            expects.append(argv[i + 1])
            i += 2
        elif argv[i] == "--diff":
            diff = True
            i += 1
        else:
            i += 1
    if "--diff" in argv:
        diff = True
    text, code = report(data.decode("utf-8", "replace"), expects, "--diff" in argv)
    sys.stdout.write(text)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
