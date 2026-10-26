#!/usr/bin/env python3
"""Locators and verification for the RevengerOmarchy report: every quote is located by
an actual grep in this run (no typed line numbers) and then re-verified as a substring
of that numbered line."""
import hashlib
import json
import pathlib
import subprocess

OM = pathlib.Path("/home/vgpnk/.local/share/omarchy")
FETCH = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch")
OUT = pathlib.Path(__file__).resolve().parent

# (label, file, quote)
QUOTES = [
    ("OM-mon-file", OM / "config/hypr/monitors.conf", "monitor=,preferred,auto,auto"),
    ("OM-gdk2", OM / "config/hypr/monitors.conf", "env = GDK_SCALE,2"),
    ("OM-gdk175", OM / "config/hypr/monitors.conf", "# env = GDK_SCALE,1.75"),
    ("OM-mon16", OM / "config/hypr/monitors.conf", "# monitor=,preferred,auto,1.6"),
    ("OM-mon1x", OM / "config/hypr/monitors.conf", "# monitor=,preferred,auto,1"),
    ("OM-portrait", OM / "config/hypr/monitors.conf", "monitor = DP-2, preferred, auto, 1, transform, 1"),
    ("OM-apple", OM / "config/hypr/monitors.conf", "monitor = DP-5, 6016x3384@60, auto, 2"),
    ("OM-ghost", OM / "config/hypr/monitors.conf", "monitor=DP-2,disable"),
    ("OM-ultrawide", OM / "config/hypr/monitors.conf", "ultrawide monitors like 34\" 3440x1440"),
    ("OM-src-toggles", OM / "config/hypr/hyprland.conf", "source = ~/.local/state/omarchy/toggles/hypr/*.conf"),
    ("OM-src-monitors", OM / "config/hypr/hyprland.conf", "source = ~/.config/hypr/monitors.conf"),
    ("OM-no-scale-notif", OM / "default/hypr/looknfeel.conf", "disable_scale_notification = true"),
    ("OM-cycle-keyword", OM / "bin/omarchy-hyprland-monitor-scaling-cycle", 'hyprctl keyword monitor "$ACTIVE_MONITOR'),
    ("OM-cycle-guard", OM / "bin/omarchy-hyprland-monitor-scaling-cycle", "grep -E '^[[:space:]]*monitor='"),
    ("OM-cycle-match", OM / "bin/omarchy-hyprland-monitor-scaling-cycle", '\"${ACTIVE_LINES[0]}\" =~ ^monitor=,preferred,auto,'),
    ("OM-cycle-sed", OM / "bin/omarchy-hyprland-monitor-scaling-cycle", 'sed -i -E "s|^(monitor=,preferred,auto,).*|'),
    ("OM-cycle-scales", OM / "bin/omarchy-hyprland-monitor-scaling-cycle", "SCALES=(1 1.25 1.6 2 3 4)"),
    ("OM-cycle-rate", OM / "bin/omarchy-hyprland-monitor-scaling-cycle", "REFRESH_RATE=$(echo \"$MONITOR_INFO\" | jq -r '.refreshRate')"),
    ("OM-internal-disable", OM / "bin/omarchy-hyprland-monitor-internal", 'echo "monitor=$INTERNAL,disable"'),
    ("OM-mirror-line", OM / "bin/omarchy-hyprland-monitor-internal-mirror", 'echo "monitor=$EXTERNAL, preferred, auto, 1, mirror, $INTERNAL"'),
    ("OM-mig-vrr", OM / "migrations/1776781957.sh", "monitor=,preferred,auto,auto,vrr,1"),
    ("OM-skill-format", OM / "default/omarchy-skill/SKILL.md", "monitor = eDP-1, 1920x1080@60, 0x0, 1"),
    ("HY-parser-stof", FETCH / "Hyprland-Parser.cpp", "m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));"),
    ("HY-parser-starts", FETCH / "Hyprland-Parser.cpp", 'if (value.empty() || value.starts_with("pref"))'),
    ("HY-ctl-refresh", FETCH / "Hyprland-HyprCtl.cpp", '"refreshRate": {:.5f},'),
    ("HY-mon-round", FETCH / "Hyprland-Monitor.cpp", "m_size            = (xfmd / m_scale).round();"),
    ("HY-mon-searchscale", FETCH / "Hyprland-Monitor.cpp", "float    searchScale = std::round(m_scale * 120.0);"),
    ("HY-mon-autoscale", FETCH / "Hyprland-Monitor.cpp", "const bool autoScale = RULE->m_scale <= 0.1;"),
    ("HY-mon-ppi200", FETCH / "Hyprland-Monitor.cpp", "if (PPI > 200 /* High PPI, 2x*/)"),
    ("HY-mon-ppi140", FETCH / "Hyprland-Monitor.cpp", "else if (PPI > 140 /* Medium PPI, 1.5x*/)"),
    ("HY-mon-scalechecks", FETCH / "Hyprland-Monitor.cpp", "if (!*PDISABLESCALECHECKS && (logicalSize.x != std::round(logicalSize.x)"),
    ("HY-rule-refresh-default", FETCH / "Hyprland-MonitorRule.hpp", "float                        m_refreshRate   = 60; // Hz"),
    ("HY-rule-mgr-erase", FETCH / "Hyprland-MonitorRuleManager.cpp", "std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });"),
    ("HY-rule-mgr-reverse", FETCH / "Hyprland-MonitorRuleManager.cpp", "for (auto const& r : m_rules | std::views::reverse) {"),
    ("HY-env-setenv", FETCH / "Hyprland-legacy-ConfigManager.cpp", "setenv(ARGS[0].c_str(), ARGS[1].c_str(), 1);"),
    ("HY-handlemon-varargs", FETCH / "Hyprland-legacy-ConfigManager.cpp", 'if (ARGS[1] == "disable" || ARGS[1] == "disabled" || ARGS[1] == "addreserved" || ARGS[1] == "transform")'),
]

lines_out = []
fails = []
for label, path, quote in QUOTES:
    res = subprocess.run(["grep", "-nF", "--", quote, str(path)], capture_output=True, text=True)
    if not res.stdout.strip():
        fails.append(f"MISSING {label}: {quote!r} not in {path}")
        lines_out.append(f"[MISSING] {label} {path}: {quote!r}")
        continue
    hits = res.stdout.rstrip("\n").splitlines()
    for h in hits:
        ln = int(h.split(":", 1)[0])
        text = h.split(":", 1)[1]
        lines_out.append(f"{path.name}:{ln}: {text.strip()}")
    # verify: quote is a substring of the cited line
    first = hits[0].split(":", 1)
    if quote not in first[1]:
        fails.append(f"VERIFY-FAIL {label}")
    words = len(quote.split())
    if words > 25:
        fails.append(f"TOO-LONG {label} ({words} words)")

# sha256 of every cited file
lines_out.append("")
lines_out.append("# sha256 of cited files")
for p in sorted({q[1] for q in QUOTES}):
    lines_out.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p}")
lines_out.append("")
lines_out.append("# omarchy provenance")
lines_out.append(subprocess.run(["git", "-C", str(OM), "log", "-1", "--format=%H %ad %s", "--date=iso"],
                                capture_output=True, text=True).stdout.strip())
lines_out.append("omarchy version file: " + (OM / "version").read_text().strip())
lines_out.append("")
lines_out.append("# verification: " + ("ALL QUOTES LOCATED AND VERIFIED (n=%d)" % len(QUOTES) if not fails else "FAILURES: " + "; ".join(fails)))
print("\n".join(lines_out))
(OUT / "receipt-quotes.txt").write_text("\n".join(lines_out) + "\n")
json.dump(fails, (OUT / "quote-fails.json").open("w"))
