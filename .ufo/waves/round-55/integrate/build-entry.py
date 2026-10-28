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
# ---- round-55 wave-2 audit corrections (R55W2AuditA-F, CritEntryProse; each replace must hit exactly once) ----
def sub(old, new):
    global text
    assert text.count(old) == 1, (text.count(old), old[:60])
    text = text.replace(old, new)
sub("it clamps rate and delay (K04, K05), stores numlock (K06)", "it floors rate and delay at zero with std::max (K04, K05), stores numlock (K06)")
sub("the stored clamped value and the unclamped config value differ", "the stored floored value and the unfloored config value differ")
sub("- How the hyprlang config layer enforces the min and max fields for the three keys (clamp, reject or ignore). The pins show the table declaration (K13, K14) and not the enforcement code.",
    "- How the config layer treats a value outside the declared min and max of the three keys. The pins show the table declaration (K13, K14) and no enforcement site. A wave-2 source review (R55W2RevToolSource, `.ufo/waves/round-55/w2/R55W2RevToolSource.md`) reports that the legacy `.conf` path registers values without a range and that min and max are enforced only for the Lua configuration; that is a pointer, not a lane row or pin, so it stays UNKNOWN here.")
sub("| E03 | IKeyboard declares m_numlockOn with initializer -1 on this line, so the declared numlock default is -1 and not 0 or 1. |",
    "| E03 | IKeyboard declares the member m_numlockOn with initializer -1 on this line, so a keyboard's stored numlock value starts at -1, not 0 or 1, until applyConfigToKeyboard assigns it (K06); this is the member initializer, not the config default (K15). |")
sub("| E07 | CWLSeatProtocol::updateRepeatInfo calls repeatInfo with rate and delayMs for each keyboard resource in the m_keyboards loop on this line. |",
    "| E07 | Line 608 calls k->repeatInfo(rate, delayMs) once per element k of the m_keyboards loop that line 607 opens. |")
sub("and the rate and delay are not both equal to the last sent values (K11, E10, K12).",
    "and the rate and delay are not both equal to the last pair the resource recorded (K11, E10, K12); the initial recorded values are not shown by the lane's pins. A second push, from the CWLKeyboardResource constructor when a client binds wl_keyboard, calls repeatInfo directly with the same stored fields and does not pass through the capability test of updateRepeatInfo (E14).")
sub("(K16, E12). applyConfigToKeyboard reads", "(K16, E12; K16 also requires a non-empty fallback name). applyConfigToKeyboard reads") if False else None
sub("returns the global value when the device value is absent or not set by the user (K16, E12).", "returns the global value when the device value is absent or not set by the user and the fallback name is non-empty (K16, E12).")
sub("K11, E13, E10 and K12 (per resource)", "K11, E13, E10 and K12 (per resource), E14 (the bind-time push)")
sub("Cells are generated from `frozen-tables.json` `c1.k` and `c1.h`;", "Cells are generated from `frozen-tables-v2.json` `c1.k` and `c1.h` (v1's `frozen-tables.json` differs only in K16's quote);")
sub("python3 -I .ufo/waves/round-55/freeze-verify.py\n", "python3 -I .ufo/waves/round-55/freeze-verify-v2.py\n")
sub("The first command must match `c1.pin_sha256` in `frozen-tables.json`. The `freeze-verify.py` line must end `OK`.", "The first command must match `c1.pin_sha256` in `frozen-tables-v2.json` (it prints the eleven lines of `SHA256SUMS.txt`: ten pins and the host captures). The `freeze-verify-v2.py` line must end `OK`; `freeze-verify.py` verifies the superseded v1 table and also ends `OK`.")
sub("The counter checks only the S-id URL suffix and status, so it would not catch these.", "The counter checks that a cited S-id is one unique registry row with eleven cells, status `mined`, a URL ending in the pin's repository path and (for Hyprland pins) containing the pinned commit; it does not read line-range anchors, so it would not catch these.") if "The counter checks only the S-id URL suffix and status, so it would not catch these." in text else None
sub("source: S316, S317, S318, S319, S052 (existing registry rows), S378, S379, S380 (new rows, opened 2026-10-28, written by the L1 at integration);",
    "source: S316, S317, S318, S319, S052 (existing registry rows), S378, S379, S380 (new rows, opened 2026-10-28) and S381, S382 (rows that correct the scope and teaches wording of S379 and S380; append-only registry, CORPUS rule 2);")
sub("- Whether any live client binds wl_keyboard at version 4 or later.", "- Whether any live client binds wl_keyboard at version 4 or later.\n- WHEN the three options are re-applied (a new keyboard, a config reload, `hyprctl keyword`): this entry holds only the setup caller (E08). A wave-2 source map (R55W2ScoutCallers, `.ufo/waves/round-55/w2/R55W2ScoutCallers/callers.md`) reports exactly two callers of applyConfigToKeyboard (setupKeyboard and the setKeyboardLayout loop) and five callers of setKeyboardLayout including the legacy reload path, and that repeat_delay is the one key without the input-device refresh flag on the dynamic path; that is a pointer, not a lane row or pin, so it stays UNKNOWN here.")
# E14: the bind-time push
text = text.replace("| E05 |", "| E14 | The CWLKeyboardResource constructor path pushes the active keyboard's stored rate and delay to the new wl_keyboard resource on this line, through repeatInfo directly. | S379 | Hyprland-protocols-core-Seat.cpp:350 | `repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate` |\n| E05 |", 1)
join = open(".ufo/waves/round-55/integrate/join-section.md").read()
text = text.replace("## Limits", join.rstrip("\n") + "\n\n## Limits", 1)
open("corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md", "w").write(text.rstrip("\n") + "\n")
print("written", len(text))
