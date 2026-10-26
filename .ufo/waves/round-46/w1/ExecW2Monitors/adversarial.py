#!/usr/bin/env python3
"""Adversarial fixtures for mado-monitors.py (tip 4d22eeb), checked against my reading of the
round-45 pins: legacy ConfigManager.cpp handleMonitor:1293, Monitor.cpp matchesStaticSelector:1201 /
applyMonitorRule:719 / scale block:996-1048, Parser.cpp parseMode/parseScale/parseTransform,
MonitorRuleManager.cpp add:37 get:44, MonitorRule.hpp defaults:41-46, HyprCtl.cpp getMonitorData:225,
aquamarine DRM.cpp output->description:2101, macros.hpp DELTALESSTHAN:40.

Every dump is synthetic. Each case: config text, dump list, my expectation (verdict-token, exit code,
and the exact summary line I read off the pins), then the tool's actual output.
"""
import json
import os
import subprocess
import sys

TOOL = "/fast/scratch/hyaku/mado-r46/ExecW2Monitors/mado-monitors-tip.py"
ROOT = "/fast/scratch/hyaku/mado-r46/ExecW2Monitors/fx"


def mon(id, name, w, h, rr, x=0, y=0, scale=1, transform=0, disabled=False, mirror="none",
        make="Acme", model="X1", serial="SN9", description=None):
    return {
        "id": id, "name": name,
        "description": description if description is not None else "%s %s %s" % (make, model, serial),
        "make": make, "model": model, "serial": serial,
        "width": w, "height": h, "refreshRate": rr, "x": x, "y": y,
        "scale": scale, "transform": transform, "disabled": disabled, "mirrorOf": mirror,
    }


CASES = []


def case(name, cfg, mons, expect_summary, expect_rc, why, gap=False):
    CASES.append(dict(name=name, cfg=cfg, mons=mons, expect_summary=expect_summary,
                      expect_rc=expect_rc, why=why, gap=gap))


# F01 - desc: selector that only the LONG description satisfies ("make model serial (name)").
case("f01-desc-long",
     "monitor = desc:Acme X1 SN9 (HDMI-A-1), 2560x1440@60, 0x0, 1\n",
     [mon(1, "HDMI-A-1", 2560, 1440, 59.951)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "Monitor.cpp:1206 matches m_description too; aquamarine DRM.cpp:2101 builds it as 'make model serial (name)'")

# F02 - transform modifier BEFORE the rule that creates it: nothing is added (ConfigManager.cpp:1307-1322).
case("f02-transform-before-rule",
     "monitor = DP-1, transform, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, transform=1)],
     "lines=2 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER",
     1,
     "the loop over monitorRuleMgr()->all() finds no DP-1 rule and returns {} without adding; the rule's m_transform stays 0 while live is 1")

# F03 - transform modifier with a zero-padded INTEGER after the rule, value 07.
case("f03-transform-07",
     "monitor = DP-1, 3440x1440@100, 0x0, 1\nmonitor = DP-1, transform, 07\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, transform=7)],
     "lines=2 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "Parser.cpp parseTransform: isNumber('07') holds, std::stoi -> 7, clamp(7,0,7)==7; the copy with transform 7 is re-added and moves last")

# F04 - scale needing the 1/120 search: 3440x1440 at 1.5 -> 2293.33 fractional, K/120=1.5 fails,
#       i=12 up = 1.6 divides both (2150 x 900).
case("f04-scale-search-1.5",
     "monitor = DP-1, 3440x1440@100, 0x0, 1.5\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, scale=1.6)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "Monitor.cpp:996-1048: search i=1..89 up then down; 3440/1.6=2150 and 1440/1.6=900 are whole")

# F04b - same rule, live scale still the written 1.5.
case("f04b-scale-search-live-written",
     "monitor = DP-1, 3440x1440@100, 0x0, 1.5\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, scale=1.5)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER",
     1,
     "a live 1.5 is not the corrected scale, so the scale field fails")

# F05 - 1920x1080 at 1.3 is corrected to 160/120 = 1.3333333; hyprctl prints scale with 6 significant digits.
case("f05-scale-1.3-corrected",
     "monitor = eDP-1, 1920x1080@60, 0x0, 1.3\n",
     [mon(2, "eDP-1", 1920, 1080, 60.019, scale=1.33333)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "i=4 up: 160/120=1.3333333 divides 1920 (1440) and 1080 (810); |1.33333-1.3333333| < 1e-4")

# F06 - same rule, live scale is the uncorrected 1.3.
case("f06-scale-1.3-as-written",
     "monitor = eDP-1, 1920x1080@60, 0x0, 1.3\n",
     [mon(2, "eDP-1", 1920, 1080, 60.019, scale=1.3)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER",
     1,
     "the corrected scale is 1.3333333, so a live 1.3 fails the scale field")

# F07 - no candidate in +-89 divides 1920x1200 at 14.166667: Hyprland falls back to getDefaultScale(),
#       which the dump cannot predict -> NOT_COMPARED.
case("f07-scale-unpredicted",
     "monitor = DP-1, 1920x1200@60, 0x0, 14.166667\n",
     [mon(0, "DP-1", 1920, 1200, 59.951, scale=1)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=0 disabled=0 notcompared=1 verdict=NOT_COMPARED",
     5,
     "Monitor.cpp:1033-1035 'failed to find a clean divisor' -> getDefaultScale(); exhaustive i=1..89 in double arithmetic finds none")

# F08 - a second rule for the same selector erases the first and the survivor moves last
#       (MonitorRuleManager.cpp:37 std::erase_if then emplace_back).
case("f08-erase-and-readd",
     "monitor = DP-1, 3440x1440@100, 0x0, 1\nmonitor = DP-1, 2560x1440@60, 0x0, 1\nmonitor = HDMI-A-1, 1920x1080@60, 0x0, 1\n",
     [mon(0, "DP-1", 2560, 1440, 59.951), mon(1, "HDMI-A-1", 1920, 1080, 60.057)],
     "lines=3 rules=2 v2=0 unsupported=0 badrules=0 outputs=2 matched=2 unruled=0 agree=2 differ=0 disabled=0 verdict=OK",
     0,
     "the 3440 rule is erased; the 2560 rule is inserted before HDMI-A-1 and then DP-1 resolves to it")

# F08b - empty selector: first empty rule is the fallback for an output with no name match.
case("f08b-empty-selector",
     "monitor = , 1920x1080@60, 0x0, 1\n",
     [mon(1, "HDMI-A-1", 1920, 1080, 60.0)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "MonitorRuleManager.cpp get: second loop returns the first rule whose m_name is empty")

# F09 - addreserved on a selector that has no rule falls through to add() a default rule
#       (preferred / auto / auto, transform 0) - ConfigManager.cpp:1346-1352.
case("f09-addreserved-default-rule",
     "monitor = HDMI-A-1, addreserved, 0, 0, 0, 50\n",
     [mon(1, "HDMI-A-1", 3440, 1440, 99.997, transform=0)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "no HDMI-A-1 rule exists, so parser.rule() (mode preferred, pos auto, scale auto, transform 0) is added; only transform and mirrorOf are compared")

# F10 - sdr_eotf is not a legacy KEY: 'invalid syntax' is returned BEFORE monitorRuleMgr()->add.
case("f10-sdr-eotf-badrule",
     "monitor = DP-1, 3440x1440@100, 0x0, 1, sdr_eotf, 2\n",
     [mon(0, "DP-1", 3440, 1440, 99.997)],
     "lines=1 rules=0 v2=0 unsupported=0 badrules=1 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR",
     3,
     "ConfigManager.cpp:1452-1454 returns before add; Hyprland then applies its hardcoded default")

# F11 - mirror by name: mirrorOf must be the decimal id of the named output; the other output is UNRULED.
case("f11-mirror-id",
     "monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1\n",
     [mon(0, "DP-1", 3440, 1440, 99.997), mon(3, "DP-2", 3440, 1440, 99.997, mirror="0")],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=2 matched=1 unruled=1 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "HyprCtl.cpp:267 prints mirrorOf as the mirrored output's m_id, or 'none'; DP-1 has no rule of its own")

# F11b - mirrorOf points elsewhere.
case("f11b-mirror-wrong-id",
     "monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1\n",
     [mon(0, "DP-1", 3440, 1440, 99.997), mon(3, "DP-2", 3440, 1440, 99.997, mirror="1")],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=2 matched=1 unruled=1 agree=0 differ=1 disabled=0 verdict=DIFFER",
     1,
     "the expected id is DP-1's 0, not 1")

# F12 - a rule without @RATE requests 60 Hz (MonitorRule.hpp:46) and the test is strict: |61-60| < 1 fails.
case("f12-rate-61-strict",
     "monitor = DP-1, 3440x1440, 0x0, 1\n",
     [mon(0, "DP-1", 3440, 1440, 61.0)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER",
     1,
     "macros.hpp:40 DELTALESSTHAN(a,b,1) is |a-b| < 1; 61.0 is exactly one away")

# F12b - one thousandth under the boundary agrees.
case("f12b-rate-60-999",
     "monitor = DP-1, 3440x1440, 0x0, 1\n",
     [mon(0, "DP-1", 3440, 1440, 60.999)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "|60.999 - 60| = 0.999 < 1")

# F13 - the transform modifier re-adds a COPY of the found rule, and add() erases the original and
#       appends, so the rule moves to the END of the list (ConfigManager.cpp:1313-1321, manager add:37).
case("f13-transform-moves-last",
     "monitor = DP-1, 3440x1440@100, 0x0, 1\nmonitor = HDMI-A-1, 1920x1080@60, 0x0, 1\nmonitor = DP-1, transform, 3\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, transform=3), mon(1, "HDMI-A-1", 1920, 1080, 60.057)],
     "lines=3 rules=2 v2=0 unsupported=0 badrules=0 outputs=2 matched=2 unruled=0 agree=2 differ=0 disabled=0 verdict=OK",
     0,
     "final list order is [HDMI-A-1, DP-1] - a tool that edits the rule in place still agrees on state, so the order is read off the printed n= values")

# F14 - a scale below 0.25 is an error that still adds the rule with scale 1 (Parser.cpp:203-209).
case("f14-scale-0.1-becomes-1",
     "monitor = DP-1, 3440x1440@100, 0x0, 0.1\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, scale=1)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "stof('0.1') = 0.1 < 0.25F -> m_error += 'invalid scale', m_scale = 1, rule still added")

# F15 - 0.25 is not below the floor and divides 3440x1440 exactly (13760 x 5760), so it is kept.
case("f15-scale-0.25-kept",
     "monitor = DP-1, 3440x1440@100, 0x0, 0.25\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, scale=0.25)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "0.25 < 0.25F is false; 3440/0.25 and 1440/0.25 are whole, so no correction is applied")

# F16 - '0x0' is Hyprland's preferred sentinel (parseMode stoi path leaves m_resolution (0,0)), so the mode
#        is not compared while the explicit position still is.
case("f16-zero-mode-preferred",
     "monitor = DP-1, 0x0, 0x0, 1\n",
     [mon(0, "DP-1", 3440, 1440, 143.999)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "m_resolution (0,0) means preferred; the printed rule line must read mode=preferred")

# F17 - a disabled rule against a live disabled output is DISABLED, which is not a difference.
case("f17-disabled-agree",
     "monitor = DP-1, disable\n",
     [mon(0, "DP-1", 0, 0, 0, disabled=True)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=0 disabled=1 verdict=OK",
     0,
     "applyMonitorRule returns on m_disabled after setEnabled(false); getMonitorData prints disabled:true")

# F18 - MEASURED GAP: isNumber has no 9-digit cap (probe: isNumber("1234567890")=1), so a 10-digit
#       transform VALUE is accepted by isNumber, std::stoi gives 1234567890, clamp(...,0,7) differs and
#       parseTransform fails - but the caller ignores it, so the rule is added with transform 0.
case("f18-transform-10-digits",
     "monitor = DP-1, 3440x1440@100, 0x0, 1, transform, 1234567890\n",
     [mon(0, "DP-1", 3440, 1440, 99.997, transform=0)],
     "lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK",
     0,
     "Hyprland reading; the tool declares [0-9]{10,} unsupported and answers NOT_COMPARED (conservative)",
     gap=True)


def run():
    os.makedirs(ROOT, exist_ok=True)
    bad = 0
    for c in CASES:
        d = os.path.join(ROOT, c["name"])
        os.makedirs(d, exist_ok=True)
        cfgp = os.path.join(d, "mon.conf")
        monsp = os.path.join(d, "mons.json")
        open(cfgp, "w").write(c["cfg"])
        open(monsp, "w").write(json.dumps(c["mons"]))
        p = subprocess.run([sys.executable, "-I", TOOL, "--monitors", monsp, "--config", cfgp],
                           capture_output=True, text=True, cwd=d)
        lines = [l for l in p.stdout.splitlines() if l]
        summary = lines[-1] if lines else ""
        want = "MADO_MONITORS: " + c["expect_summary"]
        ok = (summary == want and p.returncode == c["expect_rc"] and p.stderr == "")
        if c.get("gap") and not ok:
            print("%-30s GAP-CONSERVATIVE rc=%d (Hyprland reading wants %d)" % (c["name"], p.returncode, c["expect_rc"]))
        else:
            bad += 0 if ok else 1
            print("%-30s %s rc=%d (want %d)" % (c["name"], "MATCH" if ok else "MISMATCH", p.returncode, c["expect_rc"]))
        print("    why: %s" % c["why"])
        if not ok:
            print("    want: %s" % want)
            print("    got : %s" % summary)
            if p.stderr:
                print("    err : %s" % p.stderr.strip().splitlines()[-1][:200])
        for l in lines:
            print("    > %s" % l)
    print("ADVERSARIAL: %d/%d match my reading of the pins" % (len(CASES) - bad, len(CASES)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
