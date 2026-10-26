#!/usr/bin/env python3
"""ExecErrataR45 (round-47 w2, R4b): re-derive every round-45 erratum by command.

Reads the lane read-only (pins, receipts, frozen counters), the w1 draft's pins, and this
seat's own pins. Prints MATCH/MISMATCH per assertion plus the append-only shape checks.
No network, no writes.

usage: verify-r45-errata.py [--lane DIR] [--seat DIR]
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SEAT = pathlib.Path(__file__).resolve().parent
FETCH = LANE / ".ufo/waves/round-45/fetch"
RECEIPTS = LANE / ".ufo/waves/round-45/receipts"
W1 = LANE / ".ufo/waves/round-47/w1/ScrErrataR45"
ENTRY = LANE / "corpus/knowledge/hyprland-monitor-rule-r45.md"
REV = "4d22eeb66c2835af8aaa3fac6ad838fa616aa663"
BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"

bad = 0


def ok(cond, label, detail=""):
    global bad
    bad += not cond
    print(f"{'MATCH   ' if cond else 'MISMATCH'} {label}{(' :: ' + detail) if detail else ''}")
    return cond


def lines(p):
    return p.read_text(errors="replace").splitlines()


def line_is(p, n, text, label):
    ls = lines(p)
    got = ls[n - 1] if 0 < n <= len(ls) else ""
    return ok(text in got, label, f"{p.name}:{n} = {got.strip()[:96]}")


def git(*args):
    return subprocess.run(["git", "-C", str(LANE), *args], capture_output=True, text=True)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    global LANE, SEAT, FETCH, RECEIPTS, W1, ENTRY
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=str(LANE))
    ap.add_argument("--seat", default=str(SEAT))
    args = ap.parse_args()
    LANE = pathlib.Path(args.lane)
    SEAT = pathlib.Path(args.seat)
    FETCH = LANE / ".ufo/waves/round-45/fetch"
    RECEIPTS = LANE / ".ufo/waves/round-45/receipts"
    W1 = LANE / ".ufo/waves/round-47/w1/ScrErrataR45"
    ENTRY = LANE / "corpus/knowledge/hyprland-monitor-rule-r45.md"

    print("== pins: the fourteen round-45 pins on disk vs receipts/fetch-sha256.txt ==")
    man = (RECEIPTS / "fetch-sha256.txt").read_text().splitlines()
    n_ok = 0
    for row in man:
        h, name = row.split(None, 1)
        p = FETCH / pathlib.Path(name.strip()).name
        n_ok += bool(p.exists() and sha(p) == h)
    ok(n_ok == len(man) == 14, "14/14 pins byte-identical", f"ok={n_ok}/{len(man)}")

    print("\n== pins fetched by w1 (ScrErrataR45/pins) vs its receipts/PINS.md ==")
    md = (W1 / "receipts/PINS.md").read_text()
    rows = re.findall(r"\|\s*`([^`]+)`\s*\|[^|]+\|\s*`([0-9a-f]{64})`", md)
    n_ok = sum(1 for name, h in rows if (W1 / "pins" / name).exists() and sha(W1 / "pins" / name) == h)
    ok(n_ok == len(rows) == 16, "16/16 w1 pins match PINS.md", f"ok={n_ok}/{len(rows)}")

    print("\n== pins fetched by this seat (pins/PINS.md) ==")
    self_pins = {
        "aquamarine-v0.15.1.tar.gz": "2f9de98c0bd1b7b1b09c576e390a2fef436449762fb334163c414f0c300296f2",
        "aquamarine-Null-v0.15.1.cpp": "9989fb17e3f95e22678b69c3683d74112c756155d36d8c4fa0c646a560c587b5",
        "aquamarine-Backend-v0.15.1.cpp": "4908c6f81e8183274c906eff4e0545555a7ac5842ba5a96df54c2383ec2620f7",
        "hyprland-ConfigManager-hpp-a9902ea.hpp": "389365c493c2507fe5be7f1c20670ef0af5308b585a3e71ad3fd3851009d9712",
    }
    n_ok = sum(1 for n, h in self_pins.items() if sha(SEAT / "pins" / n) == h)
    ok(n_ok == len(self_pins), "4/4 seat pins match pins/PINS.md", f"ok={n_ok}/{len(self_pins)}")

    print("\n== E1 (entry:84): the monitor-added emit is reached only by the enabled fall-through ==")
    mon = FETCH / "Hyprland-Monitor.cpp"
    line_is(mon, 108, "void CMonitor::onConnect(bool noRule) {", "E1 onConnect entry")
    line_is(mon, 264, "if (m_enabled && !monitorRule.m_disabled) {", "E1 :264 already-enabled branch")
    line_is(mon, 266, "applyMonitorRule(std::move(cpy));", "E1 :266 applies the rule")
    line_is(mon, 271, "return;", "E1 :271 returns before the emit")
    line_is(mon, 275, "if (monitorRule.m_disabled) {", "E1 :275 disabled veto")
    line_is(mon, 283, "m_enabled = false;", "E1 :283")
    line_is(mon, 286, "return;", "E1 :286 disabled path returns")
    line_is(mon, 302, "m_enabled = true;", "E1 :302 enabled fall-through")
    line_is(mon, 389, "Event::bus()->m_events.monitor.added.emit(m_self.lock());", "E1 :389 emit")
    emits = []
    for p in sorted(FETCH.iterdir()):
        if p.suffix in (".cpp", ".hpp"):
            for i, l in enumerate(lines(p), 1):
                if "monitor.added.emit" in l:
                    emits.append(f"{p.name}:{i}")
    ok(emits == ["Hyprland-Monitor.cpp:389"], "single monitor.added emit across the code pins", str(emits))
    line_is(FETCH / "Hyprland-MonitorState.cpp", 25, "m_listeners.monitorAdded   = Event::bus()->m_events.monitor.added.listen(", "E1 listener")
    line_is(W1 / "pins/Hyprland-Monitor-efb5099.hpp", 357, "m_enabled             = false;", "E1 fresh monitor disabled by default")

    print("\n== E2 (entry:96): the cited receipt is the L1 draft's, not the landed tool's ==")
    l1 = RECEIPTS / "live-monitors-host-l1.txt"
    r45 = RECEIPTS / "live-monitors-host-r45.txt"
    line_is(l1, 1, "l1-draft/mado-monitors.py", "E2 l1 receipt runs the draft")
    line_is(l1, 4, "# tool sha256 c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be", "E2 l1 receipt tool sha")
    ok(sha(LANE / ".ufo/waves/round-45/l1-draft/mado-monitors.py") ==
       "c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be", "E2 draft file hashes to the receipt's sha")
    for rev in (REV, BASE):
        out = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:tools/mado-monitors.py"],
                             capture_output=True).stdout
        ok(hashlib.sha256(out).hexdigest() ==
           "2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609",
           f"E2 landed tool sha at {rev[:8]}")
    ok(sha(LANE / "tools/mado-monitors.py") ==
       "2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609", "E2 landed tool sha on disk")
    line_is(r45, 4, "# tool sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609", "E2 r45 receipt tool sha")
    for n, t in ((7, "verdict=AGREE"), (8, "verdict=OK"), (9, "exit=0")):
        line_is(r45, n, t, f"E2 r45 receipt line {n}")
    ok(lines(l1)[2] == lines(r45)[2], "E2 same config hash line in both receipts", lines(r45)[2][:60])
    tracked = git("cat-file", "-e", f"{REV}:.ufo/waves/round-45/receipts/live-monitors-host-r45.txt").returncode == 0
    ok(tracked, "E2 replacement receipt is committed at the freeze commit")

    print("\n== E3 (entry:98): the closeness branch is determined ==")
    line_is(mon, 836, "if (!DELTALESSTHAN(bestMode->pixelSize.x, RULE->m_resolution.x, 1) || !DELTALESSTHAN(bestMode->pixelSize.y, RULE->m_resolution.y, 1) ||", "E3 :836 bound 1")
    line_is(mon, 837, "!DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1))", "E3 :837 bound 2")
    line_is(mon, 838, "requestedModes.push_back(", "E3 :838 push")
    line_is(FETCH / "Hyprland-macros.hpp", 40, "#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))", "E3 strict bound macro")
    line_is(mon, 878, "for (auto const& mode : requestedModes | std::views::reverse) {", "E3 :878 reverse iteration")
    line_is(mon, 903, "m_refreshRate = mode->refreshRate / 1000.f;", "E3 :903 applied rate recorded")
    line_is(l1, 6, 'MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00', "E3 declared rule")
    line_is(l1, 11, '"refreshRate": 99.997', "E3 applied rate in the dump")
    ok(abs(99.997 - 100.000) < 1, "E3 rate delta inside the strict 1 Hz bound", f"|99.997-100.000|={abs(99.997-100.0):.3f} < 1")
    # addBest3Modes sorts best-first, keeps three, inserts reversed -> back() is the closest mode
    src = mon.read_text()
    ok("requestedModes.insert_range(requestedModes.end(), sortedModes | std::views::reverse);" in src,
       "E3 back() is the closest mode (addBest3Modes reverses the best-first sort)")

    print("\n== E4 (entry:18): upstream main drops the legacy manager ==")
    cj = json.loads((W1 / "pins/hyprland-commit-a9902ea.json").read_text())
    ok(cj["sha"] == "a9902ea65f461af868497c4e74fed798ade0b1b0", "E4 commit sha", cj["sha"])
    ok(cj["commit"]["committer"]["date"] == "2026-07-22T16:35:10Z", "E4 commit date", cj["commit"]["committer"]["date"])
    ok(cj["commit"]["message"].splitlines()[0] == "config: remove legacy config support (#15539)", "E4 commit message")
    legacy = [f for f in cj["files"] if f["filename"] == "src/config/legacy/ConfigManager.cpp"]
    ok(bool(legacy) and legacy[0]["status"] == "removed" and legacy[0]["deletions"] == 2184,
       "E4 legacy manager removed with 2184 deletions",
       f"{legacy[0]['status']} deletions={legacy[0]['deletions']}" if legacy else "absent")
    ok((W1 / "pins/legacy-cfg-a9902ea.txt").read_bytes() == b"404: Not Found", "E4 legacy file 404s at that commit (14 bytes)")
    cfg = lines(W1 / "pins/hyprland-main-cfg-a9902ea.cpp")
    ok(not any("Legacy" in l for l in cfg), "E4 no Legacy occurrence in the main ConfigManager.cpp")
    ok(cfg[29].strip() == "g_mgr = makeUnique<Lua::CConfigManager>();" and
       cfg[32].strip() == "g_mgr = makeUnique<Lua::CConfigManager>();", "E4 only Lua::CConfigManager (lines 30, 33)")
    patch_cpp = [f["patch"] for f in cj["files"] if f["filename"] == "src/config/ConfigManager.cpp"][0]
    patch_hpp = [f["patch"] for f in cj["files"] if f["filename"] == "src/config/ConfigManager.hpp"][0]
    ok("-        case CONFIG_LEGACY: return \"hyprlang\";" in patch_cpp,
       "E4 .cpp drops the CONFIG_LEGACY case")
    ok("-        CONFIG_LEGACY = 0," in patch_hpp,
       "E4 .hpp drops the CONFIG_LEGACY enumerator (the enum lives in the header, not the .cpp)")
    hpp = lines(SEAT / "pins/hyprland-ConfigManager-hpp-a9902ea.hpp")
    ok(not any("CONFIG_LEGACY" in l for l in hpp) and any("CONFIG_LUA" in l for l in hpp),
       "E4 ConfigManager.hpp at a9902ea keeps CONFIG_LUA only", f"enum at :{hpp.index('    enum eConfigManagerType : uint8_t {') + 1}")

    print("\n== E5 (entry:106): non-DRM backends build no description at all ==")
    import tarfile
    tf = tarfile.open(SEAT / "pins/aquamarine-v0.15.1.tar.gz")
    hits = []
    for m in tf.getmembers():
        if not m.isfile() or not m.name.endswith((".cpp", ".hpp")):
            continue
        body = tf.extractfile(m).read().decode("utf-8", "replace").splitlines()
        for i, l in enumerate(body, 1):
            if "description" in l:
                hits.append(f"{m.name.split('/', 1)[1]}:{i}")
    ok(hits == ["include/aquamarine/output/Output.hpp:258",
                "src/backend/drm/DRM.cpp:2101",
                "src/backend/drm/DRM.cpp:2104"],
       "E5 across the whole v0.15.1 tag only DRM.cpp assigns a description", str(hits))
    for name in ("aquamarine-Null-v0.15.1.cpp", "aquamarine-Backend-v0.15.1.cpp"):
        ok("description" not in (SEAT / "pins" / name).read_text(errors="replace"),
           f"E5 {name} sets no description")
    line_is(W1 / "pins/aqua-Output.hpp", 258, "name, description, make, model, serial;", "E5 fields are default-empty strings")
    line_is(W1 / "pins/aqua-Wayland-v0.15.1.cpp", 168, "bool Aquamarine::CWaylandBackend::createOutput(const std::string& szName) {", "E5 Wayland createOutput")
    line_is(W1 / "pins/aqua-Headless-v0.15.1.cpp", 187, "bool Aquamarine::CHeadlessBackend::createOutput(const std::string& name) {", "E5 Headless createOutput")
    line_is(mon, 250, "m_description = m_output->description;", "E5 Hyprland copies the field")
    line_is(mon, 255, 'm_shortDescription = trim(std::format("{} {} {}", m_output->make, m_output->model, m_output->serial));', "E5 short description from make/model/serial")

    print("\n== E6 (entry:107): the line form is removed; monitor rules are not ==")
    line_is(W1 / "pins/hyprland-LuaBindingsConfigRules-a9902ea.cpp", 20, '#include "../../shared/monitor/Parser.hpp"', "E6 shared parser still included")
    line_is(W1 / "pins/hyprland-LuaBindingsConfigRules-a9902ea.cpp", 80, "inline constexpr SMonitorFieldDesc MONITOR_FIELDS[] = {", "E6 MONITOR_FIELDS")
    ok("CMonitorRuleParser& p" in (W1 / "pins/hyprland-LuaBindingsConfigRules-a9902ea.cpp").read_text(),
       "E6 MONITOR_FIELDS feed CMonitorRuleParser")
    line_is(W1 / "pins/hyprland-lua-cfg-a9902ea.cpp", 809, "Config::monitorRuleMgr()->scheduleReload();", "E6 lua manager drives the rule manager")
    line_is(W1 / "pins/hyprland-lua-cfg-a9902ea.cpp", 810, "Config::monitorRuleMgr()->ensureMonitorStatus();", "E6 second call")
    line_is(FETCH / "Hyprland-legacy-ConfigManager.cpp", 606, 'm_config->registerHandler(&::handleMonitor, "monitor", {false});', "E6 removed file carries the monitor keyword handler")
    line_is(ENTRY, 4, "S303 - hyprwm/Hyprland src/config/legacy/ConfigManager.cpp @ efb5099", "E6 S303 cites that file")

    print("\n== entry identity and append-only shape ==")
    ok(sha(ENTRY) == "128df1bd1055fcbb09f611c48286cd013e9d8bade992f4c17e81ba0615bb9c7b",
       "entry sha256 on disk", sha(ENTRY))
    shown = subprocess.run(["git", "-C", str(LANE), "show", f"{REV}:corpus/knowledge/hyprland-monitor-rule-r45.md"],
                           capture_output=True).stdout
    ok(hashlib.sha256(shown).hexdigest() == sha(ENTRY), "entry identical at the cited commit 4d22eeb")
    landing = subprocess.run(["git", "-C", str(LANE), "log", "--diff-filter=A", "--format=%H", "--",
                              "corpus/knowledge/hyprland-monitor-rule-r45.md"],
                             capture_output=True, text=True).stdout.split()
    ok(landing[:1] == ["ee6659b90f7bf69aa03283dba804dd90081b7ff5"],
       "entry landed in ee6659b (4d22eeb is the later tip-receipt commit)", f"landing={landing[:1]}")
    raw = ENTRY.read_bytes()
    ok(raw.endswith(b"\n"), "entry ends with a newline", f"last byte {raw[-1]:#04x}")
    el = raw.decode().splitlines()
    ok(el[-1].startswith("- Upstream main has removed the hyprlang line form"), "entry ends inside the `## Limits` list", el[-1][:60])
    ok(not any(l.startswith("## Errata") for l in el), "entry carries no errata section yet")
    heads = [l for l in el if l.startswith("## ")]
    ok(heads[-1] == "## Limits", "last section is `## Limits`", heads[-1])
    ok(len(heads) == 8, "entry has 8 column-0 H2 sections", f"n={len(heads)}")
    prec = 0
    tot = 0
    for p in sorted((LANE / "corpus/knowledge").glob("*.md")):
        ls = lines(p)
        for i, l in enumerate(ls):
            if l.startswith("## Errata"):
                tot += 1
                prec += bool(i and ls[i - 1].strip() == "")
    ok(tot == prec == 21, "corpus precedent: every `## Errata` heading is preceded by a blank line", f"{prec}/{tot}")
    drafted = (SEAT / "block-as-drafted.md").read_text()
    fixed = (SEAT / "block-fixed.md").read_text()
    ok(bool(re.search(r"\bS\d{3,}\b", drafted)), "as-drafted block carries an S### token (clause g risk)",
       str(re.findall(r"\bS\d{3,}\b", drafted)))
    ok(not re.search(r"\bS\d{3,}\b", fixed), "fixed block carries no S### token")
    line_is(SEAT / "block-as-drafted.md", 34, "(S303), so the `monitor =` line form is gone on main.",
            "H1 quote locator (block-as-drafted.md:34)")
    line_is(W1 / "errata.md", 93, "`CONFIG_LEGACY` enum from `src/config/ConfigManager.cpp`",
            "H3 quote locator (errata body:93)")
    line_is(SEAT / "block-fixed.md", 24, "the `Legacy`/`CONFIG_LEGACY` selection in",
            "H3: the appended block's own E4 wording")
    ok(drafted.startswith("## Errata"), "as-drafted block starts with the heading (no leading blank line)")
    ok(fixed.startswith("\n## Errata"), "fixed block starts with the blank line the corpus convention wants")
    import shutil
    cmark = shutil.which("cmark")
    if cmark:
        for label, text in (("as-drafted, no blank line", el and "\n".join(el) + "\n" + drafted),
                            ("as-drafted, blank line", "\n".join(el) + "\n\n" + drafted),
                            ("fixed", "\n".join(el) + "\n" + fixed)):
            html = subprocess.run([cmark, "--unsafe"], input=text, capture_output=True, text=True).stdout
            ok(bool(re.search(r"<h2[^>]*>Errata", html)), f"cmark renders the errata heading ({label})",
               f"h2={len(re.findall(r'<h2', html))} li={html.count('<li>')} "
               f"e_bullets={len(re.findall(r'<li>E[1-6]', html))}")
    else:
        print("SKIP cmark not installed")

    print(f"\nRESULT: mismatches={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
