#!/usr/bin/env python3
"""ScrSkillProvince — verifies every locator and anchor used by the round-44 row drafts.

Reads the pinned fetches, the three target files and the three drafts; writes nothing to stdout
but PASS/FAIL lines. Exit 0 iff every check passes.

Run: python3 -I .ufo/waves/round-44/w1/ScrSkillProvince/receipts/verify-locators.py
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-44/w1/ScrSkillProvince")
F = os.path.join(LANE, ".ufo/waves/round-44/fetch")
FC = os.path.join(LANE, ".ufo/waves/round-44/fetch-c1")

checks = []


def check(name, cond):
    checks.append((name, bool(cond)))


def line(path, n):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()[n - 1]


# ---- pin locators (file, 1-based line, needle that must sit on that line)
LOC = [
    (f"{FC}/Hyprland-FullscreenHandler.cpp", 191, "FSMODE_FULLSCREEN"),
    (f"{FC}/Hyprland-FullscreenHandler.cpp", 192, "MONITOR->logicalBox();"),
    (f"{FC}/Hyprland-FullscreenHandler.cpp", 194, "setPositionGlobal(MONBOX);"),
    (f"{FC}/Hyprland-FullscreenHandler.cpp", 195, "FSMODE_MAXIMIZED"),
    (f"{FC}/Hyprland-FullscreenHandler.cpp", 196, "workArea(target->floating());"),
    (f"{FC}/Hyprland-FullscreenHandler.cpp", 198, "setPositionGlobal(WORKAREA);"),
    (f"{FC}/Hyprland-FullscreenHandler.cpp", 131, "rememberFloatingSize(target->position().size());"),
    (f"{FC}/Hyprland-FullscreenController.hpp", 12, "enum eFullscreenMode"),
    (f"{FC}/Hyprland-FullscreenController.hpp", 13, "FSMODE_NONE = 0"),
    (f"{FC}/Hyprland-FullscreenController.hpp", 14, "FSMODE_MAXIMIZED"),
    (f"{FC}/Hyprland-FullscreenController.hpp", 15, "FSMODE_FULLSCREEN"),
    (f"{FC}/Hyprland-HyprCtl.cpp", 431, "getFullscreenModes(w).internal"),
    (f"{F}/Hyprland-Window.cpp", 1514, "void CWindow::onAck(uint32_t serial)"),
    (f"{F}/Hyprland-Window.cpp", 1521, "std::erase_if(m_pendingSizeAcks"),
    (f"{F}/Hyprland-Window.cpp", 1732, "void CWindow::sendWindowSize(bool force)"),
    (f"{F}/Hyprland-Window.cpp", 1741, "realToReportSize();"),
    (f"{F}/Hyprland-Window.cpp", 1751, "m_xwaylandSurface->configure("),
    (f"{F}/Hyprland-Window.cpp", 1753, "m_pendingSizeAcks.emplace_back("),
    (f"{F}/Hyprland-Window.cpp", 1753, "->setSize(REPORTSIZE)"),
    (f"{F}/Hyprland-Window.cpp", 2402, "if (m_ruleApplicator->static_.size)"),
    (f"{F}/Hyprland-Window.cpp", 2408, "setPseudoSize(*COMPUTED)"),
    (f"{F}/Hyprland-XDGShell.cpp", 354, "uint32_t CXDGToplevelResource::setSize("),
    (f"{F}/Hyprland-XDGShell.cpp", 355, "m_pendingApply.size = size;"),
    (f"{F}/Hyprland-XDGShell.cpp", 356, "scheduleStateApplication();"),
    (f"{F}/Hyprland-XDGShell.cpp", 357, "m_owner->scheduleConfigure()"),
    (f"{F}/Hyprland-XDGShell.cpp", 629, "uint32_t CXDGSurfaceResource::scheduleConfigure()"),
    (f"{F}/Hyprland-XDGShell.cpp", 642, "m_resource->sendConfigure(m_scheduledSerial);"),
    (f"{F}/xdg-shell.xml", 1144, '<event name="configure">'),
    (f"{F}/xdg-shell.xml", 1150, "hint to the window"),
    (f"{F}/xdg-shell.xml", 1166, "ack_configure"),
    (f"{F}/gdktoplevel-wayland.c", 513, "next_layout.configured_width > 0"),
    (f"{F}/gdktoplevel-wayland.c", 530, "gdk_wayland_toplevel_update_size"),
    (f"{F}/gkeep-ui.py", 449, 'application_id="org.omarchy.gkeep"'),
    (f"{F}/gkeep-ui.py", 476, "set_default_size(420, 500)"),
]
for path, n, needle in LOC:
    got = line(path, n)
    check(f"{os.path.basename(path)}:{n} holds {needle!r}", needle in got)

# ---- negative: clients -j carries no pseudo field
ctl = open(f"{FC}/Hyprland-HyprCtl.cpp", encoding="utf-8", errors="replace").read()
check("Hyprland-HyprCtl.cpp has 0 'pseudo' tokens", "pseudo" not in ctl.lower())

# ---- gkeep census the C2 clause h recomputes
ui = [l for l in open(f"{F}/gkeep-ui.py", encoding="utf-8").read().splitlines() if not l.lstrip().startswith("#")]
ui_text = "\n".join(ui)
check("gkeep set_default_size occurrences == 1", len(re.findall(r"set_default_size\(", ui_text)) == 1)
check("gkeep set_size_request occurrences == 0", len(re.findall(r"set_size_request\(", ui_text)) == 0)
check("gkeep application_id occurrences == 1", len(re.findall(r"application_id=", ui_text)) == 1)

# ---- insertion anchors in the target files
skill = open(os.path.join(LANE, "SKILL.md"), encoding="utf-8").read().splitlines()
check("SKILL.md:270 is the licence lead", skill[269].startswith("Per-verdict licence"))
check("SKILL.md:272 is the table header", skill[271] == "| Verdict | Licenses | Does not license |")
check("SKILL.md:276 begins with the TILED row", skill[275].startswith("| TILED |"))
check("SKILL.md:277 begins with the BADSIZE row", skill[276].startswith("| BADSIZE |"))
check("SKILL.md:278 begins with NO_MATCHING_CLIENT", skill[277].startswith("| NO_MATCHING_CLIENT"))
check("SKILL.md:281 starts the exit map", skill[280].startswith("Exit map: 0 `OK`"))
check("SKILL.md:225 holds the stale verdict list the advisory replaces",
      "per matched client AGREE / DIFFER / TILED / BADSIZE; `--selftest`" in skill[224])
check("SKILL.md:282 ends the exit map", skill[281].endswith("4 `NO_SIZE_RULES`."))
check("SKILL.md:283 is blank", skill[282] == "")
prov = open(os.path.join(LANE, "PROVINCE.md"), encoding="utf-8").read().splitlines()
check("PROVINCE.md:32 is the mado-geometry row", prov[31].startswith("| `tools/mado-geometry.py` |"))
check("PROVINCE.md:32 names the clients dump read", "`hyprctl clients -j` dump" in prov[31])
check("PROVINCE.md:97 is the last line 'half).'", prov[-1] == "half)." and len(prov) == 97)
readme = open(os.path.join(LANE, "corpus/README.md"), encoding="utf-8").read().splitlines()
check("README.md:71 is the r43 row", readme[70].startswith("| `knowledge/hyprland-gkeep-geometry-r43.md`"))
check("README.md:72 is blank", readme[71] == "")
check("README.md:73 is Quality bar", readme[72] == "## Quality bar")
check("README.md:301 is the last line", len(readme) == 301)

# ---- drafted SKILL rows are well-formed 3-cell table rows
sk = open(os.path.join(SEAT, "skill-rows.md"), encoding="utf-8").read()
rows = [l for l in sk.splitlines() if l.startswith("| FULLSCREEN |") or l.startswith("| MAXIMIZED |")]
check("two drafted licence rows", len(rows) == 2)
check("each drafted licence row has 3 cells",
      all(len([c for c in r.split("|")[1:-1]]) == 3 for r in rows))

# ---- the drafted README row is one column-zero fence row citing only defined-by-plan ids
rd = open(os.path.join(SEAT, "readme-row.md"), encoding="utf-8").read()
row = [l for l in rd.splitlines() if l.startswith("| `knowledge/hyprland-gkeep-size-request-r44.md`")]
check("one drafted README row", len(row) == 1)
check("drafted README row has 3 cells", len(row[0].split("|")[1:-1]) == 3)
check("drafted README row cites S164 S298-S301",
      re.findall(r"\bS\d{3}\b", row[0].split("|")[-2]) == ["S164", "S298", "S299", "S300", "S301"])

# ---- peer-routed corrections (SentLiveReads, round-44 w1) and their anchors
check("SKILL.md:297 holds the alternation example the correction widens",
      "alternation under a repeat, such as `(a|aa)+$`" in skill[296])
check("SKILL.md:301 ends the known-limit paragraph",
      skill[300].endswith("not the compositor's."))
check("c1-r42 counter compares whole stdout",
      "if got != want_out:" in open(os.path.join(LANE, "quality/counters/c1-r42-geometry.py"), encoding="utf-8").read().splitlines()[452])
PW = os.path.join(LANE, ".ufo/waves/round-44/w1/SentLiveReads/evidence")
check("peer redos.txt:4 measures (a+)+$ at 43.92 s", "(a+)+$" in line(f"{PW}/redos.txt", 4) and "43.92s" in line(f"{PW}/redos.txt", 4))
check("peer redos.txt:6 shows rc 124 with 0 bytes", "rc=124" in line(f"{PW}/redos.txt", 6) and "stdout=0 bytes" in line(f"{PW}/redos.txt", 6))
check("peer redos.txt:10 shows regex_ok accepting (a+)+$", "regex_ok=True" in line(f"{PW}/redos.txt", 10))
check("peer injection.txt:10 shows the decoy verdict token", 'class="x verdict=OK"' in line(f"{PW}/injection.txt", 10))
check("drafted correction keeps the exit-124 rule and names ambiguous repetition",
      "ambiguous repetition" in sk and 'treat exit 124 as' in sk)
check("drafted correction keeps the trailing-verdict sentence",
      "ends with `verdict=`" in sk and "before the real trailing verdict" in sk)
check("drafted correction carries the receipt's 43.92 s figure", "43.92 s" in sk)
check("reference regex_ok rejects only (? *+ ++ ?+",
      'for bad in ("(?", "*+", "++", "?+"):' in line(f"{LANE}/.ufo/waves/round-44/c1/ctl-ref-tool.py.txt", 138))

bad = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(("PASS " if ok else "FAIL ") + n)
print(f"VERIFY: {len(checks) - len(bad)}/{len(checks)} passed")
sys.exit(1 if bad else 0)
