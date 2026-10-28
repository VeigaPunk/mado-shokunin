#!/usr/bin/env python3
"""R55ScribeEntryB generator (round 55, wave w1, seat draft). Writes entry.md.

K and H rows: the pin, line and quote cells are read from frozen-tables.json c1.k / c1.h. No quote is typed here.
E rows (extra facts; the frozen counter ignores them): the quote is the whole pin line at the stated line, stripped.
Prose refers to E rows by key as <E:key>; the key resolves to its E-number, so numbering cannot drift.
Usage: python3 -I gen_entry.py [--out PATH]   (default: entry.md next to this script)
"""
import hashlib
import json
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = os.path.join(LANE, ".ufo/waves/round-55")
FETCH = os.path.join(W, "fetch")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(HERE, "entry.md")

T = json.load(open(os.path.join(W, "frozen-tables.json"), encoding="utf-8"))
C1 = T["c1"]

# Source id of each pinned file (registration §C1: existing rows S316/S319/S318/S317/S052, new rows S378/S379/S380).
PIN_SID = {
    "Hyprland-InputManager.cpp": "S316",
    "Hyprland-IKeyboard.cpp": "S319",
    "Hyprland-ConfigValues.cpp": "S318",
    "Hyprland-legacy-ConfigManager.cpp": "S317",
    "wayland-1.26.0-wayland.xml": "S052",
    "Hyprland-SeatManager.cpp": "S378",
    "Hyprland-protocols-core-Seat.cpp": "S379",
    "Hyprland-IKeyboard.hpp": "S380",
}
for _pin, _ids in C1["new_row_pins"].items():
    for _id in _ids.split(","):
        _row = next(r for r in C1["k"] if r["id"] == _id)
        assert _row["pin"] == _pin and PIN_SID[_pin] in ("S378", "S379", "S380"), (_id, _pin)

# Propositions. Each binds to its own quote only (QUALITY 104). Mechanism claims are source-level.
PROP_K = {
    "K01": "applyConfigToKeyboard asks getDeviceInt for repeat_rate and passes input:repeat_rate as the global key.",
    "K02": "applyConfigToKeyboard asks getDeviceInt for repeat_delay and passes input:repeat_delay as the global key.",
    "K03": "applyConfigToKeyboard asks getDeviceInt for numlock_by_default and passes input:numlock_by_default as the global key.",
    "K04": "The stored repeat rate is the configured rate clamped below at zero, so a negative configured rate is stored as 0.",
    "K05": "The stored repeat delay is the configured delay clamped below at zero, so a negative configured delay is stored as 0.",
    "K06": "The keyboard's stored numlock state m_numlockOn is assigned the NUMLOCKON value read for this keyboard.",
    "K07": "The delay and rate equality with the stored values is one conjunct of the early-return test; if either differs, the test fails and the store runs.",
    "K08": "IKeyboard::setKeymap reads numlock_by_default for this keyboard's name through getDeviceInt, with input:numlock_by_default as the global key.",
    "K09": "The numlock lock bit is set inside the branch that runs when NUMLOCKON equals 1; pinned lines 122-131 show no else arm for it.",
    "K10": "When m_keyboard is non-null, updateActiveKeyboardData passes the active keyboard's m_repeatRate and m_repeatDelay to PROTO::seat->updateRepeatInfo.",
    "K11": "repeatInfo returns without sending when the wl_keyboard resource's version() is below 4.",
    "K12": "repeatInfo sends repeat_info to its wl_keyboard resource with the rate and delay it was given, once its guards have passed.",
    "K13": "The built-in default for input:repeat_rate is 25, with a declared range from 0 to 200.",
    "K14": "The built-in default for input:repeat_delay is 600 milliseconds, with a declared range from 0 to 2000.",
    "K15": "The built-in default for input:numlock_by_default is false, declared as a Bool option.",
    "K16": "getConfigValueSafeDevice returns the global fallback value when the device value is missing or was not set by the user and a fallback key is given.",
    "K17": "wayland.xml 1.26.0 says a repeat rate of zero disables any repeating, regardless of the delay value.",
    "K18": "IKeyboard declares m_repeatRate as an int with the initial value 0.",
}
PROP_H = {
    "H01": "input.conf line 14 declares repeat_rate = 40 inside the input block; a declaration in the file, not a client delivery.",
    "H02": "input.conf line 15 declares repeat_delay = 250 inside the input block; a declaration in the file, not a client delivery.",
    "H03": "input.conf line 18 declares numlock_by_default = true inside the input block; file text, not a live keyboard state.",
    "H04": "The committed getoption read returned input:repeat_rate with int 40 and set true; a read of the option, not a client delivery.",
    "H05": "The committed getoption read returned input:repeat_delay with int 250 and set true; a read of the option, not a client delivery.",
    "H06": "The committed getoption read returned input:numlock_by_default with int 1 and set true; a read of the option, not a keyboard LED.",
}

# Extra rows: (key, sid, pin file, line, proposition). Quote = the stripped pin line. Order = E-number.
EXTRA = [
    ("upd_guard", "S378", "Hyprland-SeatManager.cpp", 176, "The guard on this line decides whether updateActiveKeyboardData calls updateRepeatInfo at all; with m_keyboard null the next line is skipped."),
    ("setkb_push", "S378", "Hyprland-SeatManager.cpp", 172, "setKeyboard calls updateActiveKeyboardData after it has re-pointed m_keyboard and the active flags."),
    ("bind_nokb", "S379", "Hyprland-protocols-core-Seat.cpp", 344, "A wl_keyboard bound while the seat has no keyboard takes the early return on the following lines and sends no keymap or repeat info from its constructor."),
    ("bind_send", "S379", "Hyprland-protocols-core-Seat.cpp", 350, "The constructor of a bound wl_keyboard calls repeatInfo with the active keyboard's stored rate and delay, after the keymap is sent."),
    ("ri_dedupe", "S379", "Hyprland-protocols-core-Seat.cpp", 442, "The repeatInfo guard also returns when the owner is missing or when the rate and delay equal the values this resource last stored."),
    ("ri_last", "S379", "Hyprland-protocols-core-Seat.cpp", 444, "The resource records the rate it is about to send in m_lastRate before calling sendRepeatInfo."),
    ("fan_caps", "S379", "Hyprland-protocols-core-Seat.cpp", 604, "updateRepeatInfo returns before the fan-out when the seat's current capabilities lack the keyboard bit."),
    ("fan_each", "S379", "Hyprland-protocols-core-Seat.cpp", 608, "updateRepeatInfo passes the same rate and delay to every bound wl_keyboard resource; each resource then applies its own guard."),
    ("wl_iface", "S052", "wayland-1.26.0-wayland.xml", 2573, "wayland.xml 1.26.0 declares the wl_keyboard interface at version 11."),
    ("wl_since4", "S052", "wayland-1.26.0-wayland.xml", 2732, "wayland.xml 1.26.0 introduces the repeat_info event at since 4, the level the version guard tests."),
    ("wl_created", "S052", "wayland-1.26.0-wayland.xml", 2736, "wayland.xml 1.26.0 says repeat_info is sent as soon as the wl_keyboard object has been created."),
    ("wl_negative", "S052", "wayland-1.26.0-wayland.xml", 2740, "wayland.xml 1.26.0 says negative values for rate or delay are illegal; the same paragraph carries the rate-zero sentence."),
    ("wl_rate_arg", "S052", "wayland-1.26.0-wayland.xml", 2748, "wayland.xml 1.26.0 describes the rate argument as the rate of repeating keys in characters per second."),
    ("wl_delay_arg", "S052", "wayland-1.26.0-wayland.xml", 2750, "wayland.xml 1.26.0 describes the delay argument in milliseconds from key down until repeating starts."),
    ("add_apply", "S316", "Hyprland-InputManager.cpp", 1195, "On keyboard add, applyConfigToKeyboard is called on the new keyboard before the seat is pointed at it."),
    ("add_setkb", "S316", "Hyprland-InputManager.cpp", 1197, "The new keyboard is handed to the seat through this call, after applyConfigToKeyboard has returned."),
    ("layout_apply", "S316", "Hyprland-InputManager.cpp", 1208, "setKeyboardLayout re-applies the per-keyboard configuration to every keyboard in m_keyboards."),
    ("early_test", "S316", "Hyprland-InputManager.cpp", 1271, "The early return that skips the store begins with the numlock comparison and continues with the delay and rate comparisons."),
    ("setkeymap_call", "S316", "Hyprland-InputManager.cpp", 1286, "applyConfigToKeyboard calls setKeymap with the five XKB names after it has stored the rate, delay and numlock values."),
    ("reload_guard", "S317", "Hyprland-legacy-ConfigManager.cpp", 976, "postConfigReload tests m_isFirstLaunch before it calls setKeyboardLayout."),
    ("reload_call", "S317", "Hyprland-legacy-ConfigManager.cpp", 977, "The one pinned caller of setKeyboardLayout is postConfigReload on this line, inside the not-first-launch guard."),
    ("override_return", "S319", "Hyprland-IKeyboard.cpp", 61, "setKeymap returns early when m_keymapOverridden is set, before it stores the new rules, so the seat push at the end of the function is not reached on that path."),
    ("keymap_push", "S319", "Hyprland-IKeyboard.cpp", 147, "setKeymap ends by calling updateActiveKeyboardData, which pushes the active keyboard's stored rate and delay into the seat protocol."),
    ("override_comment", "S380", "Hyprland-IKeyboard.hpp", 91, "The header comment says an implementation that overrides the keymap stops setKeymap from setting rules; virtual keyboards with custom maps are the example."),
    ("override_default", "S380", "Hyprland-IKeyboard.hpp", 94, "m_keymapOverridden is declared with the default value false; across the ten pinned files no other line assigns it."),
]
EID = {key: f"E{n:02d}" for n, (key, *_rest) in enumerate(EXTRA, start=1)}


def resolve(text):
    def sub(m):
        assert m.group(1) in EID, m.group(1)
        return EID[m.group(1)]
    return re.sub(r"<E:(\w+)>", sub, text)


SETTLES = """- The per-keyboard inputs. `input:repeat_rate`, `input:repeat_delay` and `input:numlock_by_default` are read for each keyboard, with the global option as the fallback key [K01, K02, K03]; their built-in defaults and declared ranges are [K13, K14, K15]. Held at source level.
- The store. applyConfigToKeyboard clamps the rate and the delay below at zero, stores them with the numlock value, and then calls setKeymap [K04, K05, K06, <E:setkeymap_call>]. Held at source level.
- The seat push. updateActiveKeyboardData sends the ACTIVE keyboard's stored pair to the seat protocol and reads m_keyboard only [K10, <E:upd_guard>, <E:keymap_push>]. A keyboard that is not active is not what the seat pushes. Held at source level.
- The per-resource guards. repeatInfo sends nothing to a wl_keyboard resource below version 4 [K11], and nothing when the resource's owner is missing or when the pair equals the last pair that resource stored [<E:ri_dedupe>, <E:ri_last>]. The capability guard sits one level up [<E:fan_caps>]. Held at source level.
- Wayland 1.26.0 meanings. A rate of zero disables repeating whatever the delay is [K17]; negative values for rate or delay are illegal [<E:wl_negative>]; repeat_info exists from wl_keyboard version 4 [<E:wl_since4>]. Held as spec text; the Hyprland side is checked only at the lines quoted.
- The chain itself, from config to seat, is laid out below with the row that holds each step."""

UNKNOWN = """- Whether any real client binds wl_keyboard at version 4 or later, receives repeat_info, or applies the rate and delay it gets. No client was observed; nothing here describes any client's repeat behaviour.
- Whether the host's keyboards deliver 40 and 250 to clients. The host file and the getoption reads declare or report these values [H01-H06]; a declaration or a read is not a delivery to clients.
- Whether the first repeat_info at bind is sent. Seat.cpp:350 calls the guarded repeatInfo at bind, but the initial values of m_lastRate and m_lastDelayMs are declared in the Seat header, which is not pinned; if a stored pair equalled those initial values the guard would drop the first send. UNKNOWN from the pins.
- The body of getDeviceInt. Its pin is not in the set; the device-before-global rule is held only for getConfigValueSafeDevice [K16]. Its use of that predicate is an INFERENCE.
- Whether hyprlang range-checks input:repeat_rate and input:repeat_delay before applyConfigToKeyboard reads them. If a negative value reached the clamp it would be stored as 0 and, per K17, read as no repeat. That is a consequence of the chain, not an observation.
- Compositor-side key repeat. No pinned file reads m_repeatRate or m_repeatDelay except the seat push; whether any compositor-side repeat uses them is UNKNOWN.
- Numlock on clients. The lock bit is set in the keymap state [K09] and the modifier state is updated (IKeyboard.cpp:130); the path from there to a client's wl_keyboard modifiers is not traced in the pins. UNKNOWN.
- Overridden keymaps. m_keymapOverridden is read in the pins at IKeyboard.cpp:61 and declared at IKeyboard.hpp:94 with default false [<E:override_return>, <E:override_default>]. A file outside the pins that sets it true would change the early-return path; that reach is UNKNOWN."""

CHAIN = """1. Declared values. The three options have built-in defaults 25, 600 and false, with declared ranges 0-200 and 0-2000 for the first two [K13, K14, K15]. Held.
2. Per-keyboard read. applyConfigToKeyboard asks getDeviceInt for each name with its global key [K01, K02, K03]. Held: the call. getDeviceInt's body is not pinned (see UNKNOWN), so the device-first rule is held only through [K16].
3. Early-return test. The store is skipped when numlock, delay, rate and the five rule fields all match what is stored [K07, <E:early_test>]. Held.
4. Store. m_repeatRate and m_repeatDelay take the clamped values [K04, K05]; m_numlockOn takes NUMLOCKON [K06]; setKeymap is called with the five names [<E:setkeymap_call>]. Held.
5. Keymap. setKeymap reads numlock_by_default for the keyboard's name [K08]; it sets the numlock lock bit when the value is 1 [K09]; it ends by calling updateActiveKeyboardData [<E:keymap_push>]. The early return at IKeyboard.cpp:61-63 skips that end when m_keymapOverridden is set [<E:override_return>]. Held.
6. Seat push. updateActiveKeyboardData calls PROTO::seat->updateRepeatInfo with the active keyboard's pair when m_keyboard is non-null [K10, <E:upd_guard>]. Held.
7. Fan-out. updateRepeatInfo returns when the seat's current capabilities lack the keyboard bit [<E:fan_caps>]; otherwise it calls repeatInfo on each bound wl_keyboard resource [<E:fan_each>]. Held.
8. Guards and send. repeatInfo returns for a resource below version 4 [K11] or when the owner is missing or the pair is unchanged [<E:ri_dedupe>]; otherwise it stores the pair [<E:ri_last>] and sends repeat_info [K12]. Held.
9. Bind. A wl_keyboard bound while a keyboard is active receives its keymap and then the guarded repeatInfo with the active pair [<E:bind_send>]; with no keyboard it logs an error and returns [<E:bind_nokb>]. Held. Whether the first send can be suppressed is UNKNOWN (see above).
10. Triggers. Keyboard add calls applyConfigToKeyboard [<E:add_apply>] and then hands the keyboard to the seat [<E:add_setkb>]. A config reload on a non-first launch calls setKeyboardLayout [<E:reload_guard>, <E:reload_call>], which re-applies every keyboard [<E:layout_apply>]. Held.
11. Protocol meaning. wayland.xml 1.26.0 introduces repeat_info at version 4 [<E:wl_since4>], says it is sent as soon as the wl_keyboard exists [<E:wl_created>], gives the rate in characters per second and the delay in milliseconds [<E:wl_rate_arg>, <E:wl_delay_arg>], calls negative values illegal [<E:wl_negative>], and says a rate of zero disables repeating [K17]. Held as spec text.
12. Consequence. INFERENCE from steps 4-8 and 11: on an active keyboard, a changed rate or delay reaches each v4+ wl_keyboard resource whose stored pair differs, once the store and setKeymap have run; a non-active keyboard's values are not sent [K10]. A stored rate of 0 is forwarded as 0, because neither repeatInfo nor updateRepeatInfo tests for zero [K12, <E:fan_each>].
13. Numlock. numlock_by_default is stored [K06], the lock bit is set when it is 1 [K09], and the modifier state is updated. Whether a client sees NumLock on is UNKNOWN (see above)."""

LIMITS = """- Source level only. Every chain step is a claim about the pinned source at efb50993. A seat re-read of `hyprctl version` on 2026-10-28 reported Hyprland 0.56.2 at efb50993; that is an observation of the build, not of the running keymap, of any keyboard, or of any client.
- No live receipt. This entry has no keypress, no wl_keyboard wire trace, and no `hyprctl devices -j` read. Nothing here is a claim about the running host beyond the H rows.
- Sentence-to-pin entailment is not proven by the frozen counter (QUALITY 104); a non-author sentence audit covers it.
- The sweeps behind this entry (callers of setKeyboard and setKeyboardLayout, writers of m_keymapOverridden and of m_repeatRate) cover the ten pinned files only. The scope of the m_keymapOverridden sweep is stated on <E:override_default>.
- wayland.xml is the 1.26.0 tag text, pinned by sha256; the Hyprland side is checked only at the lines quoted.
- The host input.conf pin is the file as of pin time. On 2026-10-28 the seat's read of ~/.config/hypr/input.conf had the same sha256 (3769c92a...). The seat's live getoption reads matched H04-H06. Those re-reads are observations of this seat, not pins. The host's hyprland.conf and any file it sources are not pinned, so a device block elsewhere is not excluded.
- Effective per-keyboard value on the host: not established here. `hyprctl devices -j` was not read by this seat; the C2 tool is the join for that.
- This entry does not claim that any toolkit or application reads repeat_info, binds version 4, or applies its own settings over the compositor's."""

HOWTO = """Run from the lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Every command reads only; scratch goes under a directory you name.

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
# 1. The round's freeze verifier: every frozen quote sits at its pin line, every pin hashes to its sha256.
python3 -I .ufo/waves/round-55/freeze-verify.py
# 2. This entry's rows against the pins at the freeze commit (committed bytes), with registry and sha checks.
python3 -I .ufo/waves/round-55/w1/R55ScribeEntryB/verify.py --lane /home/vgpnk/Projects/shokunin/mado-shokunin --rev 54dacbd843d64ba744cd3f1bdc2ec622e5010039 --entry .ufo/waves/round-55/w1/R55ScribeEntryB/entry.md --work /fast/scratch/hyaku/mado-r55/R55ScribeEntryB/check
# 3. One pin line by hand (SeatManager.cpp 175-178: updateActiveKeyboardData).
sed -n '175,178p' .ufo/waves/round-55/fetch/Hyprland-SeatManager.cpp
# 4. The protocol's rate-zero sentence (wayland.xml 1.26.0 lines 2740-2741).
sed -n '2740,2741p' .ufo/waves/round-55/fetch/wayland-1.26.0-wayland.xml
# 5. Host declarations and live reads (read-only).
sha256sum ~/.config/hypr/input.conf
hyprctl version
hyprctl getoption input:repeat_rate -j
hyprctl getoption input:repeat_delay -j
hyprctl getoption input:numlock_by_default -j
```

After integration, the frozen counter runs at the final revision: `python3 -I quality/counters/c1-r55-kbd-entry.py --repo . --rev <rev> --work <scratch>`. That counter is the L1's and is not run by this seat."""


def load_lines(name):
    with open(os.path.join(FETCH, name), "rb") as fh:
        return fh.read().decode("utf-8", "replace").split("\n")


def cell_ok(text, allow_pipe=False):
    assert ("|" not in text or allow_pipe) and "`" not in text and "\n" not in text, text[:80]
    return text


def row(rid, prop, sid, pin, line, quote):
    # K16's frozen quote contains "||" (logical or). The frozen grammar says no "|" in a cell; the quote is
    # emitted byte-equal to frozen-tables.json anyway (a conflict, reported as defect D-K16), never escaped.
    cell_ok(prop)
    cell_ok(quote, allow_pipe="||" in quote)
    return f"| {rid} | {prop} | {sid} | {pin}:{line} | `{quote}` |"


def build():
    pin_lines = {name: load_lines(name) for name in C1["pin_sha256"] if name.startswith(("Hyprland-", "wayland-"))}
    host_lines = {name: load_lines(name) for name in ("host-input.conf", "host-getoption.json")}

    k_rows, h_rows = [], []
    for r in C1["k"]:
        pl = pin_lines[r["pin"]]
        assert r["quote"] in pl[r["line"] - 1], ("frozen K quote not on its line", r["id"])
        assert len(PROP_K[r["id"]]) >= 40, r["id"]
        k_rows.append(row(r["id"], resolve(PROP_K[r["id"]]), PIN_SID[r["pin"]], r["pin"], r["line"], r["quote"]))
    for r in C1["h"]:
        hl = host_lines[r["pin"]]
        assert r["quote"] in hl[r["line"] - 1], ("frozen H quote not on its line", r["id"])
        assert len(PROP_H[r["id"]]) >= 20, r["id"]
        h_rows.append(row(r["id"], PROP_H[r["id"]], "host", r["pin"], r["line"], r["quote"]))

    e_rows = []
    for key, sid, pin, line, prop in EXTRA:
        text = pin_lines[pin][line - 1].strip()
        assert text, (pin, line)
        e_rows.append(row(EID[key], resolve(prop), sid, pin, line, text))

    wayland_sha = C1["pin_sha256"]["wayland-1.26.0-wayland.xml"]
    trio = [
        "source: S316 - hyprwm/Hyprland src/managers/input/InputManager.cpp @ efb50993 (v0.56.2): applyConfigToKeyboard, the per-keyboard repeat and numlock store, setKeymap, setKeyboardLayout",
        "source: S317 - hyprwm/Hyprland src/config/legacy/ConfigManager.cpp @ efb50993: getConfigValueSafeDevice fallback; postConfigReload calls setKeyboardLayout",
        "source: S318 - hyprwm/Hyprland src/config/values/ConfigValues.cpp @ efb50993: the input:repeat_rate, input:repeat_delay and input:numlock_by_default defaults and declared ranges",
        "source: S319 - hyprwm/Hyprland src/devices/IKeyboard.cpp @ efb50993: setKeymap, the numlock lock bit, the early return on m_keymapOverridden, the seat push at its end",
        f"source: S052 - Wayland core protocol wayland.xml, tag 1.26.0 (pin sha256 {wayland_sha}): wl_keyboard repeat_info, since 4",
        "source: S378 - hyprwm/Hyprland src/managers/SeatManager.cpp @ efb50993: updateActiveKeyboardData, setKeyboard (new row, round 55)",
        "source: S379 - hyprwm/Hyprland src/protocols/core/Seat.cpp @ efb50993: CWLKeyboardResource::repeatInfo, CWLSeatProtocol::updateRepeatInfo, the bind path (new row, round 55)",
        "source: S380 - hyprwm/Hyprland src/devices/IKeyboard.hpp @ efb50993: the members m_repeatRate, m_repeatDelay, m_numlockOn, m_keymapOverridden (new row, round 55)",
        "verified-at: 2026-10-28",
        "recheck: on-release - when `hyprctl version` leaves efb50993 or the wayland pin leaves tag 1.26.0 (or 90 days at the latest): re-pull the pins, re-run freeze-verify.py and this entry's verify.py, and re-read the host declarations and the three getoption values. Observed by the seat on 2026-10-28, not a pin: `hyprctl version` reported Hyprland 0.56.2 at efb50993.",
    ]

    hdr = "| id | proposition | source | pin | quote |\n|---|---|---|---|---|"
    out = []
    out += trio
    out += [
        "",
        "# Keyboard repeat rate, repeat delay and numlock on Hyprland 0.56.2: the chain from config to the seat, and what stays open",
        "",
        "Lane mado-shokunin, round 55, wave w1, seat R55ScribeEntryB (draft; the L1 integrates). Base 3b55b6e91e40f455dd56b2985e4ffc087ada92d5; freeze commit 54dacbd843d64ba744cd3f1bdc2ec622e5010039. Source-level at Hyprland efb50993 (v0.56.2) and wayland 1.26.0. Labels: held = read on a pinned line; INFERENCE = a step the pins do not state directly; UNKNOWN = not established.",
        "",
        "## What this entry settles",
        "",
        resolve(SETTLES),
        "",
        "## What stays UNKNOWN",
        "",
        resolve(UNKNOWN),
        "",
        "## The chain",
        "",
        resolve(CHAIN),
        "",
        "## Keyboard rows K01-K18 (generated from frozen-tables.json)",
        "",
        hdr,
    ]
    out += k_rows
    out += [
        "",
        "## Host rows H01-H06 (generated from frozen-tables.json)",
        "",
        "A declaration (input.conf) is what the host file says; a read (getoption) is what the live command returned at pin time. Neither is a delivery to clients.",
        "",
        hdr,
    ]
    out += h_rows
    out += [
        "",
        f"## Extra rows E01-E{len(EXTRA):02d} (the frozen counter ignores these; quotes are whole pin lines)",
        "",
        hdr,
    ]
    out += e_rows
    out += ["", "## Limits", "", resolve(LIMITS), "", "## How to verify", "", HOWTO, ""]
    return "\n".join(out)


if __name__ == "__main__":
    text = build()
    assert "<E:" not in text, "unresolved E reference"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"WROTE {OUT} bytes={len(text.encode('utf-8'))} sha256={hashlib.sha256(text.encode('utf-8')).hexdigest()}")
