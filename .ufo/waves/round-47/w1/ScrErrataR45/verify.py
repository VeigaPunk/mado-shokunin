#!/usr/bin/env python3
"""Receipt builder for ScrErrataR45 (round-47 w1, R4b errata of hyprland-monitor-rule-r45.md).

Every locator below was computed with grep -n before being written here; this script re-checks
each (file, line, text) triple and prints MATCH/MISMATCH, so the errata's locators are verified,
never typed blind.  No network, no writes outside the seat dir.
"""
import hashlib
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
FETCH = LANE / ".ufo/waves/round-45/fetch"
RECEIPTS = LANE / ".ufo/waves/round-45/receipts"
PINS = pathlib.Path(__file__).resolve().parent / "pins"

# (pin file, 1-based line, expected text contained in that line)
QUOTES = [
    ("Hyprland-Monitor.cpp", 264, "if (m_enabled && !monitorRule.m_disabled) {"),
    ("Hyprland-Monitor.cpp", 271, "return;"),
    ("Hyprland-Monitor.cpp", 275, "if (monitorRule.m_disabled) {"),
    ("Hyprland-Monitor.cpp", 283, "m_enabled = false;"),
    ("Hyprland-Monitor.cpp", 286, "return;"),
    ("Hyprland-Monitor.cpp", 302, "m_enabled = true;"),
    ("Hyprland-Monitor.cpp", 389, "Event::bus()->m_events.monitor.added.emit(m_self.lock());"),
    ("Hyprland-Monitor.cpp", 836, "if (!DELTALESSTHAN(bestMode->pixelSize.x, RULE->m_resolution.x, 1) || !DELTALESSTHAN(bestMode->pixelSize.y, RULE->m_resolution.y, 1) ||"),
    ("Hyprland-Monitor.cpp", 837, "!DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1))"),
    ("Hyprland-Monitor.cpp", 838, "requestedModes.push_back("),
    ("Hyprland-Monitor.cpp", 878, "for (auto const& mode : requestedModes | std::views::reverse) {"),
    ("Hyprland-Monitor.cpp", 903, "m_refreshRate = mode->refreshRate / 1000.f;"),
    ("Hyprland-macros.hpp", 40, "#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))"),
    ("Hyprland-MonitorState.cpp", 25, "m_listeners.monitorAdded   = Event::bus()->m_events.monitor.added.listen([this](PHLMONITOR m) {"),
]

RECEIPT_QUOTES = [
    (RECEIPTS / "live-monitors-host-l1.txt", 1, "l1-draft/mado-monitors.py"),
    (RECEIPTS / "live-monitors-host-l1.txt", 4, "# tool sha256 c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be"),
    (RECEIPTS / "live-monitors-host-l1.txt", 8, "verdict=OK"),
    (RECEIPTS / "live-monitors-host-l1.txt", 9, "# exit=0"),
    (RECEIPTS / "live-monitors-host-l1.txt", 6, "MADO_MON_RULE: n=1 sel=\"DP-1\" mode=3440x1440@100.00"),
    (RECEIPTS / "live-monitors-host-l1.txt", 11, '"refreshRate": 99.997'),
    (RECEIPTS / "live-monitors-host-r45.txt", 1, "landed tools/mado-monitors.py"),
    (RECEIPTS / "live-monitors-host-r45.txt", 4, "# tool sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609"),
    (RECEIPTS / "live-monitors-host-r45.txt", 7, 'verdict=AGREE'),
    (RECEIPTS / "live-monitors-host-r45.txt", 8, "verdict=OK"),
    (RECEIPTS / "live-monitors-host-r45.txt", 9, "exit=0"),
    (RECEIPTS / "live-monitors-host-r45.txt", 6, "MADO_MON_RULE: n=1 sel=\"DP-1\" mode=3440x1440@100.00"),
]

PIN_QUOTES = [
    (PINS / "hyprland-commit-a9902ea.json", None, '"config: remove legacy config support (#15539)"'),
    (PINS / "hyprland-commit-a9902ea.json", None, '"date": "2026-07-22T16:35:10Z"'),
    (PINS / "hyprland-commit-a9902ea.json", None, '"filename": "src/config/legacy/ConfigManager.cpp"'),
    (PINS / "hyprland-commit-a9902ea.json", None, '"filename": "src/config/ConfigManager.cpp"'),
    (PINS / "aqua-Output.hpp", 258, "name, description, make, model, serial;"),
    (PINS / "aqua-Wayland-v0.15.1.cpp", 168, "bool Aquamarine::CWaylandBackend::createOutput(const std::string& szName) {"),
    (PINS / "aqua-Wayland-v0.15.1.cpp", 181, "auto o  = outputs.emplace_back(SP<CWaylandOutput>(new CWaylandOutput(name, self)));"),
    (PINS / "aqua-Headless-v0.15.1.cpp", 187, "bool Aquamarine::CHeadlessBackend::createOutput(const std::string& name) {"),
    (PINS / "aqua-Headless-v0.15.1.cpp", 200, "auto output = SP<CHeadlessOutput>(new CHeadlessOutput(outputName, self.lock()));"),
    (PINS / "hyprland-lua-cfg-a9902ea.cpp", 809, "Config::monitorRuleMgr()->scheduleReload();"),
    (PINS / "hyprland-lua-cfg-a9902ea.cpp", 810, "Config::monitorRuleMgr()->ensureMonitorStatus();"),
    (PINS / "legacy-cfg-a9902ea.txt", 1, "404: Not Found"),
    (PINS / "hyprland-main-cfg-a9902ea.cpp", 30, "g_mgr = makeUnique<Lua::CConfigManager>();"),
    (PINS / "hyprland-main-cfg-a9902ea.cpp", 33, "g_mgr = makeUnique<Lua::CConfigManager>();"),
    (PINS / "hyprland-LuaBindingsConfigRules-a9902ea.cpp", 80, "inline constexpr SMonitorFieldDesc MONITOR_FIELDS[] = {"),
    (PINS / "Hyprland-Monitor-efb5099.hpp", 357, "m_enabled             = false;"),
]

# (file, 1-based line, expected text) for every sentence unit the errata rewrites
ENTRY = LANE / "corpus/knowledge/hyprland-monitor-rule-r45.md"
ENTRY_QUOTES = [
    (18, "upstream main already drops the legacy hyprlang manager (Hyprland a9902ea, 2026-07-22)"),
    (84, "that event fires only for an output whose rule enables it (Hyprland-Monitor.cpp:264 and Hyprland-Monitor.cpp:389)"),
    (96, "tools/mado-monitors.py reports AGREE and verdict OK, exit 0"),
    (98, "not proof of which branch ran"),
    (106, "a Wayland or headless backend builds its description differently and is not covered"),
    (107, "Upstream main has removed the hyprlang line form (Hyprland a9902ea)"),
]

# negative assertions: text that must be ABSENT from a pin
NEGATIVE = [
    (PINS / "hyprland-main-cfg-a9902ea.cpp", "Legacy"),
    (PINS / "aqua-Wayland-v0.15.1.cpp", "description"),
    (PINS / "aqua-Headless-v0.15.1.cpp", "description"),
]


def check(path: pathlib.Path, line, text, label):
    lines = path.read_text(errors="replace").splitlines()
    if line is None:
        hits = [i + 1 for i, l in enumerate(lines) if text in l]
        ok = bool(hits)
        where = f"lines={hits[:5]}"
    else:
        ok = 0 < line <= len(lines) and text in lines[line - 1]
        where = f"line={line}"
    print(f"{'MATCH' if ok else 'MISMATCH'} {label} {path.name}:{where} :: {text[:90]}")
    return ok


def main():
    bad = 0
    print("== round-45 fetch pins (quotes in the erratum) ==")
    for name, line, text in QUOTES:
        bad += not check(FETCH / name, line, text, "pin")
    print("== round-45 receipts (provenance findings) ==")
    for path, line, text in RECEIPT_QUOTES:
        bad += not check(path, line, text, "receipt")
    print("== round-47 pins fetched by this seat ==")
    for path, line, text in PIN_QUOTES:
        bad += not check(path, line, text, "pin47")

    print("== entry sentence units (hyprland-monitor-rule-r45.md, unchanged since 4d22eeb) ==")
    entry_sha = hashlib.sha256(ENTRY.read_bytes()).hexdigest()
    print(f"entry sha256 {entry_sha}  {ENTRY}")
    for line, text in ENTRY_QUOTES:
        bad += not check(ENTRY, line, text, "entry")

    print("== negative assertions (text that must be absent) ==")
    for path, text in NEGATIVE:
        n = path.read_text(errors="replace").count(text)
        print(f"{'MATCH' if n == 0 else 'MISMATCH'} absent {path.name} :: {text} occurrences={n}")
        bad += n != 0

    print("== description occurrences in non-DRM backend sources (v0.15.1) ==")
    for name in ("aqua-Wayland-v0.15.1.cpp", "aqua-Headless-v0.15.1.cpp", "aqua-Output-v0.15.1.cpp"):
        n = (PINS / name).read_text(errors="replace").count("description")
        print(f"{name}: description_occurrences={n}")
        bad += n != 0
    drm = (PINS / "aqua-DRM-v0.15.1.cpp").read_text(errors="replace").splitlines()
    print(f"aqua-DRM-v0.15.1.cpp:2101 :: {drm[2100].strip()}")

    print("== sha256 of every pin ==")
    files = sorted(list(FETCH.glob("*")) + list(RECEIPTS.glob("live-monitors-host-*.txt")) + list(PINS.glob("*")))
    for f in files:
        print(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f}")

    print(f"\nRESULT: mismatches={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
