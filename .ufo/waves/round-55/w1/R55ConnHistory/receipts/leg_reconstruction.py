#!/usr/bin/env python3
# Reconstruction (NOT the counter): re-implements only the per-row legs that registration.md §C1 names
# (anchor, quote, source_cell, proposition length >= 40) so the forged-row case can be shown to pass them.
# Reads frozen-tables.json and the pins from the freeze export; the registry from base SOURCES.md; scratch only.
import json, re, sys

W = sys.argv[1]          # freeze-export/.ufo/waves/round-55
SRC = sys.argv[2]        # SOURCES.md at base (scratch copy)
T = json.load(open(f"{W}/frozen-tables.json"))
c1 = T["c1"]
COMMIT = c1["commit"]

reg = {}
for line in open(SRC, encoding="utf-8"):
    cols = [c.strip() for c in line.rstrip("\n").split("|")]
    if len(cols) > 9 and re.fullmatch(r"S\d{3}", cols[1] if cols[1].startswith("S") else ""):
        pass
    m = re.match(r"^\| (S\d{3}) \| (.*)$", line.rstrip("\n"))
    if not m:
        continue
    parts = [p.strip() for p in line.rstrip("\n").split(" | ")]
    sid = m.group(1)
    url = re.search(r"https?://\S+", m.group(2))
    reg[sid] = {"url": url.group(0) if url else "", "status": parts[7] if len(parts) > 7 else ""}

frozen = {r["id"]: r for r in c1["k"]}
ROW = re.compile(r"^\| (K\d\d) \| (.*?) \| (S\d{3}) \| ([^|]+?) \| `([^`]*)` \|$")

def legs(row_line):
    m = ROW.match(row_line)
    if not m:
        return "row-unparsed"
    rid, prop, sid, pincell, quote = m.groups()
    f = frozen[rid]
    failed = []
    if pincell != f"{f['pin']}:{f['line']}":
        failed.append(f"anchor:{rid}")
    if quote != f["quote"]:
        failed.append(f"quote-cell:{rid}")
    pin_lines = open(f"{W}/fetch/{f['pin']}", encoding="utf-8").read().split("\n")
    if f["quote"] not in pin_lines[f["line"] - 1]:
        failed.append(f"quote-in-pin:{rid}")
    r = reg.get(sid)
    suffix = c1["source_suffix"][f["pin"]]
    if not (r and r["url"].endswith(suffix) and COMMIT in r["url"] and r["status"] == "mined"):
        failed.append(f"source_cell:{rid}")
    if len(prop) < 40:
        failed.append(f"prop-len:{rid}")
    return "PASS" if not failed else "FAIL " + " ".join(failed)

honest = ("| K01 | applyConfigToKeyboard reads the keyboard repeat_rate through getDeviceInt, "
          "with input:repeat_rate as the global fallback. | S316 | Hyprland-InputManager.cpp:1220 | "
          "`getDeviceInt(devname, \"repeat_rate\", \"input:repeat_rate\");` |")
# Proposition contradicts the pinned legacy fallback (ConfigManager.cpp:1119 / getConfigValueSafeDevice,
# which returns the device value whenever it is set by the user). Quote, anchor and source are unchanged.
forged = ("| K01 | getDeviceInt ignores any per-device repeat_rate and always returns the global "
          "input:repeat_rate value for every keyboard. | S316 | Hyprland-InputManager.cpp:1220 | "
          "`getDeviceInt(devname, \"repeat_rate\", \"input:repeat_rate\");` |")
print("honest_row :", legs(honest))
print("forged_row :", legs(forged))
print("forged_prop_len:", len("getDeviceInt ignores any per-device repeat_rate and always returns the global input:repeat_rate value for every keyboard."))
print("S052_url_has_commit:", COMMIT in reg["S052"]["url"], "S052_status:", reg["S052"]["status"])
print("K17_row_legs_with_S052:", legs("| K17 | Repeat stops when the delay is disabled, per the protocol note on repeat delay. | S052 | wayland-1.26.0-wayland.xml:2741 | `will disable any repeating (regardless of the value of delay).` |"))
