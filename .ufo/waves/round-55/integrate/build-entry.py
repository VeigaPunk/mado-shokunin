#!/usr/bin/env python3
"""L1 integration script (round 55): builds corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md from the wave-1 draft
R55ScribeEntryA (propositions, chain, limits) with every K/H row's pin and quote cell GENERATED from
.ufo/waves/round-55/frozen-tables-v2.json, plus the L1's join/adjacency section. Run from the lane root."""
import json, re
A = ".ufo/waves/round-55/w1/R55ScribeEntryA/entry.md"
T = json.load(open(".ufo/waves/round-55/frozen-tables-v2.json"))["c1"]
src = open(A).read()
props = {}
for ln in src.split("\n"):
    m = re.match(r"\| ((?:K|H|E)\d\d) \| (.*?) \| (S\d{3}|host) \| (\S+) \| `(.*)` \|$", ln)
    if m:
        props[m.group(1)] = (m.group(2), m.group(3), m.group(4), m.group(5))
OVERRIDE = {
    "K16": "On this line getConfigValueSafeDevice tests whether the device value pointer is absent or not set by the user, together with a non-empty fallback name; the fallback return that follows is line 1120 and is not quoted here.",
    "K11": "One of the three OR-joined conditions on the guard line of CWLKeyboardResource::repeatInfo is that the resource version is below 4; the return that follows is line 443 and is not quoted here.",
}
def row(r, kind):
    p, s, _, _ = props[r["id"]]
    p = OVERRIDE.get(r["id"], p)
    return "| %s | %s | %s | %s:%d | `%s` |" % (r["id"], p, s, r["pin"], r["line"], r["quote"])
out = []
for ln in src.split("\n"):
    m = re.match(r"\| ((?:K|H)\d\d) \|", ln)
    if m:
        rid = m.group(1)
        r = next(x for x in T["k"] + T["h"] if x["id"] == rid)
        if rid == "K17":
            ln = row(r, "k").replace(props["K17"][0], "Continuing the sentence that line 2740 opens with \"A rate of zero\" (E11), the 1.26.0 wl_keyboard repeat_info description says it will disable any repeating regardless of the value of delay; the subject is on line 2740, the quote is line 2741.")
        else:
            ln = row(r, "k")
    out.append(ln)
text = "\n".join(out)
# E11: the subject of K17's sentence
text = text.replace("| E05 |", "| E11 | The repeat_info description opens the sentence that K17 finishes with the words `A rate of zero` at the end of this line. | S052 | wayland-1.26.0-wayland.xml:2740 | `A rate of zero` |\n| E05 |", 1)
text = text.replace("| E05 |", "| E12 | When the K16 condition holds, getConfigValueSafeDevice returns the global option looked up by the fallback name. | S317 | Hyprland-legacy-ConfigManager.cpp:1120 | `return m_config->getConfigValuePtr(fallback.c_str());` |\n| E13 | The guard line of repeatInfo is followed by a return on this line, so a true guard ends the call before the send. | S379 | Hyprland-protocols-core-Seat.cpp:443 | `return;` |\n| E05 |", 1)
text = text.replace("or not set by the user (K16).", "or not set by the user (K16, E12).", 1)
text = text.replace("K11, E10 and K12 (per resource)", "K11, E13, E10 and K12 (per resource)", 1)
text = text.replace("Registry anchor gaps, found by this seat and left for the L1 at integration (SOURCES.md is an integration surface, not edited here):", "Registry anchor gaps (registry rows are append-only, CORPUS rule 2, so they are recorded here rather than widened):")
join = open(".ufo/waves/round-55/integrate/join-section.md").read()
text = text.replace("## Limits", join.rstrip("\n") + "\n\n## Limits", 1)
open("corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md", "w").write(text.rstrip("\n") + "\n")
print("written", len(text))
