#!/usr/bin/env python3
"""mado round 25 C1 CONTROL seat CtlNoReader — shape NO-READER.

Shortcut shape under test: the tool never opens anything under HOME (or
anywhere else).  It accepts ``--home DIR``, ignores the value entirely, and
prints a fixed, plausible omarchy-style bind table written out longhand from
public omarchy default binds (omarchy's default/hypr/bindings/*.conf, e.g.
media.conf / tiling-v2.conf / utilities.conf).  No live capture was copied
into this file; the table is hand-written public-default knowledge.

The table is emitted in the exact 18-field shape of ``hyprctl binds -j``
(HyprCtl.cpp bindsRequest, Hyprland v0.56.2): the field names, the boolean
types, the integer ``modmask`` (SHIFT=1, CTRL=4, ALT=8, SUPER=64) and the
string-typed ``submap_universal``.

The point of this control is to score the shortcut, not to be right: a
fixed table cannot know the per-run perturbations the counter writes, nor the
exact live multiset, so this is expected to miss.  Whether it misses on the
multiset comparison alone or also on the embed check is the interesting part.

Reads: none.  Writes: none.  Network: none.  Compositor: none.
"""

import json
import sys

SUPER = 64
SHIFT = 1

# (locked, mouse, release, repeat, longPress, non_consuming, auto_consuming,
#  has_description, modmask, key, keycode, catch_all, description,
#  allow_input_capture, dispatcher, arg)
BINDS = [
    # --- media keys (public omarchy media.conf: bindeld = ...) ---
    (True, False, False, True, False, False, False, True, 0,
     "XF86AudioRaiseVolume", 0, False, "Volume up", False, "exec",
     "omarchy-swayosd-client --output-volume raise"),
    (True, False, False, True, False, False, False, True, 0,
     "XF86AudioLowerVolume", 0, False, "Volume down", False, "exec",
     "omarchy-swayosd-client --output-volume lower"),
    (True, False, False, True, False, False, False, True, 0,
     "XF86AudioMute", 0, False, "Mute", False, "exec",
     "omarchy-swayosd-client --output-volume mute-toggle"),
    (True, False, False, True, False, False, False, True, 0,
     "XF86AudioMicMute", 0, False, "Mute microphone", False, "exec",
     "omarchy-audio-input-mute"),
    (True, False, False, True, False, False, False, True, 0,
     "XF86MonBrightnessUp", 0, False, "Brightness up", False, "exec",
     "omarchy-brightness-display +5%"),
    (True, False, False, True, False, False, False, True, 0,
     "XF86MonBrightnessDown", 0, False, "Brightness down", False, "exec",
     "omarchy-brightness-display 5%-"),
    (True, False, False, True, False, False, False, True, SHIFT,
     "XF86MonBrightnessUp", 0, False, "Brightness maximum", False, "exec",
     "omarchy-brightness-display 100%"),
    (True, False, False, True, False, False, False, True, SHIFT,
     "XF86MonBrightnessDown", 0, False, "Brightness minimum", False, "exec",
     "omarchy-brightness-display 1%"),
    # --- workspaces (public omarchy tiling-v2.conf: bindd = SUPER, code:NN) ---
    (False, False, False, False, False, False, False, True, SUPER,
     "", 10, False, "Switch to workspace 1", False, "workspace", "1"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 11, False, "Switch to workspace 2", False, "workspace", "2"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 12, False, "Switch to workspace 3", False, "workspace", "3"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 13, False, "Switch to workspace 4", False, "workspace", "4"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 14, False, "Switch to workspace 5", False, "workspace", "5"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 15, False, "Switch to workspace 6", False, "workspace", "6"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 16, False, "Switch to workspace 7", False, "workspace", "7"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 17, False, "Switch to workspace 8", False, "workspace", "8"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 18, False, "Switch to workspace 9", False, "workspace", "9"),
    (False, False, False, False, False, False, False, True, SUPER,
     "", 19, False, "Switch to workspace 10", False, "workspace", "10"),
    (False, False, False, False, False, False, False, True, SUPER | SHIFT,
     "", 10, False, "Move window to workspace 1", False, "movetoworkspace", "1"),
    (False, False, False, False, False, False, False, True, SUPER | SHIFT,
     "", 11, False, "Move window to workspace 2", False, "movetoworkspace", "2"),
    (False, False, False, False, False, False, False, True, SUPER | SHIFT,
     "", 19, False, "Move window to workspace 10", False, "movetoworkspace", "10"),
    # --- utilities (public omarchy utilities.conf: bindd = SUPER, X, ...) ---
    (False, False, False, False, False, False, False, True, SUPER,
     "Q", 0, False, "Show keybindings", False, "exec", "omarchy-menu-keybindings"),
    (False, False, False, False, False, False, False, True, SUPER,
     "D", 0, False, "Application launcher", False, "exec", "omarchy-launch-walker"),
    (False, False, False, False, False, False, False, True, SUPER,
     "C", 0, False, "Clipboard manager", False, "exec",
     "omarchy-launch-walker -m clipboard"),
    (False, False, False, False, False, False, False, True, SUPER,
     "E", 0, False, "File manager", False, "exec",
     "uwsm-app -- nautilus --new-window"),
    (False, False, False, False, False, False, False, True, SUPER,
     "B", 0, False, "Web browser", False, "exec", "omarchy-launch-browser"),
    (False, False, False, False, False, False, False, True, SUPER,
     "T", 0, False, "Terminal", False, "exec", "uwsm-app -- xdg-terminal-exec"),
    (False, False, False, False, False, False, False, True, SUPER,
     "M", 0, False, "Main menu", False, "exec", "omarchy-menu"),
    (False, False, False, False, False, False, False, True, SUPER,
     "P", 0, False, "System menu", False, "exec", "omarchy-menu system"),
    (False, False, False, False, False, False, False, True, SUPER | SHIFT,
     "S", 0, False, "Screen capture", False, "exec", "omarchy-menu capture"),
    (False, False, False, False, False, False, False, True, SUPER,
     "S", 0, False, "Toggle floating window", False, "exec", "togglefloating"),
    (False, False, False, False, False, False, False, True, SUPER,
     "F", 0, False, "Toggle fullscreen", False, "exec", "fullscreen 0"),
    (False, False, False, False, False, False, False, True, SUPER,
     "W", 0, False, "Kill active window", False, "exec", "killactive"),
    (False, False, False, False, False, False, False, True, SUPER,
     "G", 0, False, "Toggle group", False, "exec", "togglegroup"),
    (False, False, False, False, False, False, False, True, SUPER,
     "J", 0, False, "Toggle split", False, "exec", "layoutmsg togglesplit"),
    (False, False, False, False, False, False, False, True, SUPER,
     "O", 0, False, "Toggle pop", False, "exec",
     "omarchy-hyprland-window-pop"),
    (False, False, False, False, False, False, False, True, SUPER,
     "L", 0, False, "Toggle layout", False, "exec",
     "omarchy-hyprland-workspace-layout-toggle"),
    (False, False, False, False, False, False, False, True, SUPER,
     "N", 0, False, "Notifications", False, "exec", "makoctl invoke"),
    (False, False, False, False, False, False, False, True, SUPER | SHIFT,
     "N", 0, False, "Dismiss last notification", False, "exec", "makoctl dismiss"),
    (False, False, False, False, False, False, False, True, SUPER | SHIFT,
     "D", 0, False, "Dismiss all notifications", False, "exec",
     "makoctl dismiss --all"),
]


def main(argv):
    # NO-READER: the --home argument is accepted and thrown away.  Nothing
    # under HOME (or anywhere else) is opened, stat'ed or listed.
    for i, a in enumerate(argv):
        if a == "--home" and i + 1 < len(argv):
            break

    out = []
    for (locked, mouse, release, repeat, longpress, nonconsuming, autoconsuming,
         hasdesc, modmask, key, keycode, catchall, desc, allowcap, disp, arg) in BINDS:
        out.append({
            "locked": locked,
            "mouse": mouse,
            "release": release,
            "repeat": repeat,
            "longPress": longpress,
            "non_consuming": nonconsuming,
            "auto_consuming": autoconsuming,
            "has_description": hasdesc,
            "modmask": modmask,
            "submap": "",
            "submap_universal": "false",
            "key": key,
            "keycode": keycode,
            "catch_all": catchall,
            "description": desc,
            "allow_input_capture": allowcap,
            "dispatcher": disp,
            "arg": arg,
        })
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
