#!/usr/bin/env python3
"""Verify every quote of report.md against its receipt: single-line substring, <=25 words, locator = grep -n line.
Usage: python3 verify-quotes.py   (reads receipts/ next to this file; prints one QUOTE line per row, exit 1 on any miss)"""
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__)) + "/receipts/"
Q = [
 ("C01","h_Hyprland_pull_11241.txt","Clamped to 0.0 - 100.0"),
 ("C02","wiki-commit-2c2e8eb9ad.txt","variables: per-device scroll_factor impld"),
 ("C03","release-v0.51.0-lines.txt","input: add per-device scroll-factor (#11241)"),
 ("C03b","release-v0.51.0-lines.txt","misc: remove commas from device names"),
 ("C04","h_Hyprland_issues_11240.txt","scroll_factor is not per-device. Make it."),
 ("C05","d_1313.txt","name matching matches the name not a class."),
 ("C06","d_12081.txt","Straight-up wrong, the quotes are wrong. You should not add any."),
 ("C06b","d_12081.txt","You're placing them inside of input. Each device config is supposed to be in it's own category not as a sub-category of input"),
 ("C07","d_13203.txt","device name changes frequently when I switch from wired to wireless connection."),
 ("C08","d_15083.txt","you just have to bind the toggle key to both devices:"),
 ("C09","d_10083.txt","that's XKB. My guess is that one of (us,de) doesn't have qwerty, in which case that is indeed invalid."),
 ("C10","d_15269.txt","Invalid keyboard layout passed. (rules: , model: , variant: gallium, options: , layout: us )"),
 ("C10b","d_15269.txt","it switched to qwerty by default."),
 ("C11","d_10159.txt","The layout used for the shortcuts is the first layout in input:kb_layout."),
 ("C11b","d_10159.txt","I noticed that kanata was available as a separate \"device\" and that it showed the actual active layout."),
 ("C12","h_omarchy_issues_9552.txt","The virtual keyboard also holds the main flag, so seat-wide reads describe it rather than the typed-on keyboard."),
 ("C12b","h_omarchy_issues_9552.txt","keyd's is keyd-virtual-keyboard, which does not match, so it competes in selectKeyboard()"),
 ("C13","h_omarchy_issues_8060.txt","Verified: hyprctl -j devices now reports the fcitx5"),
 ("C14","d_15586.txt","causes that variant to be applied to all keyboard"),
 ("C15","h_Hyprland_issues_443.txt","which loads only the layout specified inside the global input section."),
 ("C16","h_Hyprland_issues_2340.txt","hyprctl switchxkblayout -- --varmilo next"),
 ("C17","h_Hyprland_issues_7084.txt","This issue has been closed, as we are moving from issues to discussions."),
 ("C18","api_issue_4069.txt","This issue has been closed, as we are moving from issues to discussions."),
 ("C19","api_issue_8150.txt","This issue has been closed, as we are moving from issues to discussions."),
 ("C20","api_issue_9288.txt","Use a comma to separate multiple kb_options"),
 ("C21","d_12191.txt","config option <device:elan1203:00-04f3:307a-touchpad:enabled> does not exist."),
 ("C21b","d_12191.txt","Tag: v0.40.0, commits: 6436"),
 ("C22","wiki-0.56.0-Devices.txt","Since Hyprland 0.55, hyprlang is deprecated in favor of lua."),
 ("C22b","wiki-0.56.0-Devices.txt","The name can be easily obtained by checking the output of hyprctl devices."),
 ("C23","wiki-Variables-ecc06f3.md","Multiplier added to scroll movement for external mice."),
 ("C23b","wiki-Variables-ecc06f3.md","E.g. /usr/bin/fcitx5 will have hl-virtual-keyboard-fcitx5."),
 ("C24","d_14429.txt","Make name argument use regex cause modern usb input devices expose themselves as 15 devices"),
 ("C25","d_15129.txt","I think it should take one, probably one of the aforementioned."),
]
norm = lambda s: re.sub(r"\s+", " ", s.replace("`", "")).strip()
bad = 0
for qid, f, q in Q:
    n = len(q.split())
    hit = [i for i, l in enumerate(open(H + f, errors="replace").read().splitlines(), 1) if norm(q) in norm(l)]
    ok = bool(hit) and n <= 25
    bad += not ok
    print("QUOTE %s receipt=%s line=%s words=%d %s" % (qid, f, (",".join(map(str, hit[:3])) if hit else "-"), n, "OK" if ok else "MISS"))
sys.exit(1 if bad else 0)
