#!/usr/bin/env python3
"""ScrSkillProvince quote verifier (round 41, w1) — read-only, writes nothing.

For every string this seat lifted or cited, check
  (1) it occurs at the named line (or anywhere, when line is None) of the named source,
  (2) it occurs in each seat draft that presents it (whitespace-normalised, so a wrapped
      line still matches),
  (3) it is <= 25 words.
Prints one line per item and a final tally; exit 0 iff nothing failed.
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-41/w1/ScrSkillProvince")
WS = re.compile(r"\s+")
TABLE_PIPE = re.compile(r"\\\|")  # markdown-table escape for a literal pipe

# (label, source path, line|None, needle, drafts that present it)
ITEMS = [
    # --- lifted quotes -------------------------------------------------------
    ("journal advert line", ".ufo/waves/round-41/fetch/xdph-journal.txt", 117,
     "Got interface: hyprland_focus_grab_manager_v1 (ver 1)", ["province-row.md"]),
    ("protocols README listing", ".ufo/waves/round-41/fetch/protocols-README.md", 17,
     "hyprland_focus_grab` -> for grabbing input focus, primarily for complex context menus.",
     ["province-row.md"]),
    ("compositor protocol class", ".ufo/waves/round-41/fetch/Hyprland-FocusGrab.hpp", 59,
     "class CFocusGrabProtocol : public IWaylandProtocol {", ["province-row.md"]),
    ("client cleared() comment", ".ufo/waves/round-41/fetch/quickshell-grab.cpp", 78,
     "the protocol will always send cleared() when the grab is deactivated,",
     ["province-row.md"]),
    ("client cleared() handler", ".ufo/waves/round-41/fetch/quickshell-grab.cpp", 98,
     "void FocusGrab::hyprland_focus_grab_v1_cleared() {", ["province-row.md"]),
    ("portal onGlobal signature", ".ufo/waves/round-41/fetch/xdph-PortalManager.cpp", 85,
     "void CPortalManager::onGlobal(uint32_t name, const char* interface, uint32_t version) {",
     ["province-row.md"]),
    ("portal log site", ".ufo/waves/round-41/fetch/xdph-PortalManager.cpp", 88,
     'Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);',
     ["province-row.md"]),
    ("cleared event", ".ufo/waves/round-41/fetch/focus-grab-v1.xml", 121,
     '<event name="cleared">', ["province-row.md"]),
    ("issue title", ".ufo/waves/round-41/fetch/issue-565.html", None,
     "New windows in inactive workspaces stealing focus", ["province-row.md"]),
    ("province inventory claim", "PROVINCE.md", 32,
     "covers every tracked file under `tools/`", ["province-row.md"]),
    ("province tail line", "PROVINCE.md", 95, "half).", ["province-row.md"]),
    ("reference control receipt", ".ufo/waves/round-41/receipts/ctl-c1.txt", 1,
     "control=P-reference expect=MET got=MET correct=1", ["skill-rows.md"]),
    ("reference verdict", ".ufo/waves/round-41/receipts/ctl-c1.txt", 1,
     "fixtures=24/24 tool=present verdict=TARGET_MET", ["skill-rows.md"]),
    ("sample focus-grab global", ".ufo/waves/round-41/w1/ScrSkillProvince/ref-run-journal.txt", None,
     "MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab",
     ["skill-rows.md"]),
    ("sample final line", ".ufo/waves/round-41/w1/ScrSkillProvince/ref-run-journal.txt", None,
     "MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,"
     "focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,"
     "sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- verdict=OK",
     ["skill-rows.md"]),
    ("sample session line", ".ufo/waves/round-41/w1/ScrSkillProvince/ref-run-journal.txt", None,
     "boot=7ab69ee4149c4811a3faf6c08c9d119b pid=1952", ["skill-rows.md"]),
    ("selftest line", ".ufo/waves/round-41/w1/ScrSkillProvince/ref-selftest.txt", None,
     "MADO_GLOBALS_SELFTEST: 47/47 passed", ["skill-rows.md"]),
    ("tool absent at HEAD", ".ufo/waves/round-41/w1/ScrSkillProvince/git-absent-head.txt", None,
     "fatal: path 'tools/mado-globals.py' does not exist in 'HEAD'", ["skill-rows.md"]),
    # --- identifiers cited by name (not lifted prose) ------------------------
    ("class table heading", "quality/counters/c1-r41-globals.py", 48,
     "Class decision table", []),
    ("exclusion token amgsk", "quality/counters/c2-r41-focus-entry.py", None,
     "amgsk.dev", ["province-row.md"]),
    ("focus rule no_initial_focus", "corpus/knowledge/keybind-rule-semantics.md", 225,
     "no_initial_focus", ["province-row.md"]),
    ("focus rule no_focus", "corpus/knowledge/keybind-rule-semantics.md", 229,
     "no_focus", ["province-row.md"]),
    ("focus rule stay_focused", "corpus/knowledge/keybind-rule-semantics.md", 232,
     "stay_focused", ["province-row.md"]),
    ("interface manager name", ".ufo/waves/round-41/fetch/focus-grab-v1.xml", 39,
     "hyprland_focus_grab_manager_v1", ["province-row.md"]),
    ("class table focus-grab", "quality/counters/c1-r41-globals.py", 49,
     "hyprland_focus_grab_manager_v1", ["skill-rows.md"]),
]

bad = 0
for label, rel, lineno, needle, drafts in ITEMS:
    path = os.path.join(LANE, rel)
    words = len(needle.split())
    ok_words = words <= 25
    ok_src, where = False, ""
    try:
        if lineno is None:
            ok_src = needle in WS.sub(" ", open(path, encoding="utf-8",
                                               errors="replace").read())
            where = "%s:anywhere" % rel
        else:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if i == lineno:
                        ok_src = needle in line
                        break
            where = "%s:%d" % (rel, lineno)
    except OSError as exc:
        where = "unreadable: %s" % exc
    ok_drafts = []
    for d in drafts:
        dp = os.path.join(SEAT, d)
        try:
            text = TABLE_PIPE.sub("|", WS.sub(" ", open(dp, encoding="utf-8").read()))
            ok_drafts.append((d, needle in text))
        except OSError:
            ok_drafts.append((d, False))
    good = ok_words and ok_src and all(v for _, v in ok_drafts)
    bad += 0 if good else 1
    print("%-4s %-26s words=%-2d src=%-3s %-62s drafts=%s" % (
        "OK" if good else "FAIL", label, words, "yes" if ok_src else "NO", where,
        ",".join("%s:%s" % (d, "y" if v else "N") for d, v in ok_drafts)))
print("QUOTE_CHECK: items=%d failed=%d" % (len(ITEMS), bad))
sys.exit(0 if bad == 0 else 1)
