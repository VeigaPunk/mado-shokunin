#!/usr/bin/env python3
"""verify.py - re-check the seat ScrSkill draft against its sources.

Every locator the draft cites is re-opened here and the promised token is searched inside the cited
line range. Structural checks: the decision table's cell count, the verdict vocabulary, the exit-map
order against the reference docstring, the quotes (<= 25 words, present in their source), the two host
lines against the L1 receipt, and a privacy sweep (no absolute home path, no session-material key).

Reads only: the lane's fetch pins, the reference draft, the frozen counters, SKILL.md, PROVINCE.md,
the L1 entry draft and receipts, and the host config files the draft names. Writes nothing; stdout only.
Usage: python3 -I .ufo/waves/round-46/w1/ScrSkill/verify.py   (cwd = the lane)
"""
import os
import re
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".."))
SEAT = os.path.join(LANE, ".ufo/waves/round-46/w1/ScrSkill")
DRAFT = os.path.join(SEAT, "skill.md")
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
ENTRY = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/entry.md")
L1_RECEIPT = os.path.join(LANE, ".ufo/waves/round-46/receipts/live-devices-host-l1.txt")
C1 = os.path.join(LANE, "quality/counters/c1-r46-devices.py")
C2 = os.path.join(LANE, "quality/counters/c2-r46-input-device-entry.py")
FETCH = os.path.join(LANE, ".ufo/waves/round-46/fetch")

fails = []
checked = 0


def lines(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def span(path, a, b, needle, why):
    """needle must occur on some line in [a, b] (1-based, inclusive)."""
    global checked
    checked += 1
    src = lines(path)
    if b > len(src):
        fails.append("%s: %s has %d lines, cited range is %d-%d" % (why, os.path.basename(path), len(src), a, b))
        return
    hit = [i for i in range(a, b + 1) if needle in src[i - 1]]
    if not hit:
        fails.append("%s: %r not found in %s:%d-%d" % (why, needle, os.path.basename(path), a, b))


def present(path, needle, why):
    global checked
    checked += 1
    if needle not in open(path, encoding="utf-8", errors="replace").read():
        fails.append("%s: %r not found in %s" % (why, needle, os.path.basename(path)))


def main():
    draft = open(DRAFT, encoding="utf-8").read()
    ref = lines(REF)

    # 1. pin locators, each line range promised by the draft
    F = lambda n: os.path.join(FETCH, n)
    span(F("Hyprland-InputManager.cpp"), 1213, 1213, "void CInputManager::applyConfigToKeyboard", "pin 1213")
    for k in ("kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file"):
        span(F("Hyprland-InputManager.cpp"), 1226, 1231, 'getDeviceString(devname, "%s"' % k, "pin 1226-1231 " + k)
    span(F("Hyprland-InputManager.cpp"), 1274, 1274, "did not change", "pin 1274")
    span(F("Hyprland-InputManager.cpp"), 1286, 1286, "setKeymap(IKeyboard::SStringRuleNames", "pin 1286")
    span(F("Hyprland-InputManager.cpp"), 1379, 1382, 'deviceConfigExplicitlySet(devname, "scroll_factor")', "pin 1379")
    span(F("Hyprland-InputManager.cpp"), 1379, 1382, "std::clamp", "pin 1380")
    span(F("Hyprland-InputManager.cpp"), 1379, 1382, "std::nullopt", "pin 1382")
    span(F("Hyprland-InputManager.cpp"), 2119, 2130, "getNameForNewDevice", "pin 2119")
    span(F("Hyprland-InputManager.cpp"), 2119, 2130, 'std::to_string(dupeno)', "pin duplicate suffix")
    span(F("Hyprland-ConfigManager.cpp"), 1115, 1122, "getConfigValueSafeDevice", "pin 1115")
    span(F("Hyprland-ConfigManager.cpp"), 1115, 1122, "m_bSetByUser", "pin set-by-user fallback")
    span(F("Hyprland-ConfigManager.cpp"), 518, 518, 'addSpecialCategory("device", {"name"})', "pin 518")
    span(F("Hyprland-ConfigManager.cpp"), 1196, 1196, "deviceConfigExists", "pin 1196")
    span(F("Hyprland-ConfigValues.cpp"), 272, 272, '"input:kb_layout"', "pin 272")
    span(F("Hyprland-ConfigValues.cpp"), 272, 272, '"us"', "pin 272 default us")
    span(F("Hyprland-ConfigValues.cpp"), 296, 296, '"input:scroll_factor"', "pin 296")
    span(F("Hyprland-IKeyboard.cpp"), 60, 64, "m_keymapOverridden", "pin 60-64")
    span(F("Hyprland-IKeyboard.cpp"), 101, 116, 'm_currentRules.layout  = "us"', "pin 113 fallback")
    span(F("Hyprland-IKeyboard.cpp"), 101, 116, "couldn't have been loaded", "pin 101-116 error")
    span(F("Hyprland-HyprCtl.cpp"), 770, 770, '"scrollFactor": {:.2f}', "pin 770")
    for k in ("rules", "model", "layout", "variant", "options"):
        span(F("Hyprland-HyprCtl.cpp"), 788, 792, '"%s": "{}"' % k, "pin 788-792 " + k)
    span(F("Hyprland-MiscFunctions.cpp"), 777, 789, "deviceNameToInternalString", "pin 777")
    span(F("Hyprland-MiscFunctions.cpp"), 777, 789, "case ',':", "pin comma")
    span(F("Hyprland-protocols-VirtualKeyboard.cpp"), 12, 12, 'name = "hl-virtual-keyboard"', "pin 12")
    span(F("Hyprland-VirtualKeyboard.cpp"), 41, 41, "m_keymapOverridden = true", "pin 41")

    # 2. reference docstring / code locators
    span(REF, 19, 19, "join, not a blame", "ref 19")
    span(REF, 26, 26, "starts no process and opens no socket", "ref 26")
    for reason in ("usage", "unreadable", "too_large", "bad_json"):
        span(REF, 29, 34, reason, "ref 29-34 " + reason)
    span(REF, 36, 36, "argument order", "ref 36")
    span(REF, 71, 71, "never equals an expected name", "ref 71")
    span(REF, 87, 87, "unmodelled line can change any", "ref 87")
    span(REF, 80, 89, "MADO_DEVICES: keyboards=", "ref 80-89 summary")
    span(REF, 99, 99, "MAX_BYTES = 1048576", "ref 99")
    span(REF, 126, 130, "os.O_RDONLY | os.O_NONBLOCK", "ref 126")
    span(REF, 126, 130, "S_ISREG(os.fstat(fd).st_mode)", "ref 130")
    span(REF, 446, 447, "def selftest():", "ref 446")
    span(REF, 466, 466, "later-wins", "ref 466")

    # 3. counters
    span(C1, 9, 9, "ambient GIT_* removed", "c1 9")
    span(C1, 29, 29, "PATH starts with a directory holding executables", "c1 29")
    span(C1, 42, 42, "implementation of it", "c1 42")
    span(C2, 8, 8, "nothing in the lane is", "c2 8")
    span(C2, 58, 58, "twenty-eight surfaces", "c2 58")
    present(C1, "bubblewrap", "c1 bubblewrap clause")
    span(C1, 374, 375, '"PATH": "/usr/bin:/bin"', "c1 selftest PATH")
    span(C1, 241, 243, "os.path.realpath(repo)", "c1 hidden_paths contents")

    # 4. lane files the draft anchors to
    prov = lines(os.path.join(LANE, "PROVINCE.md"))
    span(os.path.join(LANE, "PROVINCE.md"), 32, 32, "tools/mado-geometry.py", "PROVINCE last table row")
    span(os.path.join(LANE, "PROVINCE.md"), 34, 34, "the inventory above covers every tracked file under", "PROVINCE 34")
    span(os.path.join(LANE, "PROVINCE.md"), 100, 100, "Round-45 refinement", "PROVINCE last line")
    skill = lines(os.path.join(LANE, "SKILL.md"))
    span(os.path.join(LANE, "SKILL.md"), 158, 158, "mado-geometry.py", "SKILL routing last row")
    span(os.path.join(LANE, "SKILL.md"), 225, 225, "mado-geometry.py", "SKILL probe last row")
    span(os.path.join(LANE, "SKILL.md"), 2100, 2102, "Monitor rule versus running output", "SKILL section tail")
    span(ENTRY, 53, 53, "hyprland input-device default_layout=us", "entry census line")

    # 5. the census line the draft pastes must equal the entry's line
    global checked
    checked += 1
    want = [l.strip() for l in lines(ENTRY) if l.strip().startswith("hyprland input-device default_layout=")][0]
    if want not in draft:
        fails.append("draft census line is not the entry's line verbatim")

    # 6. host run lines: the L1 capture, and this seat's own two captures (which disagree on the keyboard count)
    checked += 1
    summary10 = "MADO_DEVICES: keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK"
    summary9 = "MADO_DEVICES: keyboards=9 agree=9 differ=0 fallback=0 virtual=0 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK"
    virtual = ('MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-fcitx5" block=no layout="br" variant="" '
               'options="compose:caps" model="" rules="" kb_file=- differ=- verdict=VIRTUAL')
    l1 = open(L1_RECEIPT, encoding="utf-8").read()
    own = open(os.path.join(SEAT, "receipts/host-runs.txt"), encoding="utf-8").read()
    for line, receipts in ((summary10, (l1, own)), (summary9, (own,)), (virtual, (l1,))):
        for r in receipts:
            if line not in r:
                fails.append("receipt lacks: %s" % line[:70])
        if line not in draft:
            fails.append("draft does not carry: %s" % line[:70])

    # 7. the exit-map order in the draft is the docstring's order
    checked += 1
    chain = []
    for l in ref[86:89]:
        chain += re.findall(r"\b(NOT_COMPARED|DIFFER|NO_KEYBOARDS|STALE_BLOCK|OK) \(exit \d", l)
    order = chain
    if order != ["NOT_COMPARED", "DIFFER", "NO_KEYBOARDS", "STALE_BLOCK", "OK"]:
        fails.append("docstring verdict order unparsed: %r" % (order,))
    m = re.search(r"tested in that order — ([A-Z_]+, [A-Z_]+, [A-Z_]+, [A-Z_]+, [A-Z_]+)", draft)
    if not m or m.group(1).split(", ") != order:
        fails.append("draft exit-map order is not the docstring's: %r" % (m.group(1) if m else None,))

    # 8. the decision table: four cells per row, and every verdict the tool can print
    checked += 1
    rows = [l for l in draft.split("\n") if l.startswith("| `") and "|" in l]
    table = rows[rows.index(next(r for r in rows if r.startswith("| `AGREE`"))):]
    table = [r for r in table if r.count("|") == 5 and r.rstrip().endswith("|")]
    if len(table) < 13:
        fails.append("decision table rows with four cells: %d (< 13)" % len(table))
    for tok in ("AGREE", "DIFFER", "FALLBACK", "VIRTUAL", "MATCHED", "NO_SUCH_DEVICE",
                "NOT_COMPARED", "NO_KEYBOARDS", "STALE_BLOCK", "SETUP"):
        if "`%s`" % tok not in draft:
            fails.append("verdict token missing from the draft: %s" % tok)

    # 9. quotes: <= 25 words and present verbatim (whitespace-normalised) in the named source
    quotes = [
        ("It is a join, not a blame", "mado-devices.py:19", REF, 19, 19),
        ("It reads files and standard input only; it starts no process and opens no socket.", "mado-devices.py:26", REF, 26, 26),
        ("an unmodelled line can change any expectation", "mado-devices.py:87", REF, 87, 88),
        ("a missing or non-string value never equals an expected name", "mado-devices.py:71", REF, 70, 71),
        ("a tool holding a model of the contract is an implementation of it", "c1-r46-devices.py:42", C1, 42, 43),
        ("the inventory above covers every tracked file under", "PROVINCE.md:34", os.path.join(LANE, "PROVINCE.md"), 34, 34),
    ]
    for q, loc, path, a, b in quotes:
        checked += 1
        if len(q.split()) > 25:
            fails.append("quote over 25 words (%d): %s" % (len(q.split()), q))
        body = " ".join(lines(path)[a - 1:b])
        if " ".join(q.split()) not in " ".join(body.split()):
            fails.append("quote not found at %s: %s" % (loc, q))
        if " ".join(q.split()) not in " ".join(draft.split()):
            fails.append("quote not carried by the draft: %s" % q)

    # 9b. the draft states clause r's real scope, not a sandbox claim
    checked += 1
    for needle in ("PATH=/usr/bin:/bin", "/run/user/<uid>", "c1-r46-devices.py:241-243"):
        if needle not in draft:
            fails.append("draft does not carry the clause-r scope token: %r" % needle)

    # 10. privacy sweep: no absolute home path, no session-material key
    checked += 1
    for bad in ("/home/", "Serial", "initialTitle", "title\":", "ss -t"):
        if bad in draft:
            fails.append("draft carries forbidden token: %r" % bad)

    # 11. the tool is absent, as the draft's condition says
    checked += 1
    if os.path.exists(os.path.join(LANE, "tools/mado-devices.py")):
        fails.append("tools/mado-devices.py exists: the draft's 'absent at this seat's tip' is stale")

    # 12. every behaviour the decision table's next steps claim is observed in this seat's receipts
    hostr = open(os.path.join(SEAT, "receipts/host-runs.txt"), encoding="utf-8").read()
    synth = open(os.path.join(SEAT, "receipts/synthetic-verdicts.txt"), encoding="utf-8").read()
    observed = [
        (hostr, '{"option": "input:kb_layout", "str": "br", "set": true }', "getoption kb_layout"),
        (hostr, '{"option": "input:scroll_factor", "float": 1.000000, "set": false }', "getoption scroll_factor"),
        (hostr, "Failed to compile xkb_symbols", "xkbcli failure text"),
        (hostr, "/usr/bin/xkbcli", "xkbcli present"),
        (synth, "verdict=STALE_BLOCK", "STALE_BLOCK reached"),
        (synth, "rc=4", "rc 4 printed"),
        (synth, "verdict=NOT_COMPARED", "NOT_COMPARED reached"),
        (synth, "rc=5", "rc 5 printed"),
        (synth, "verdict=FALLBACK", "FALLBACK reached"),
        (synth, "verdict=NO_KEYBOARDS", "NO_KEYBOARDS reached"),
        (synth, "rc=3", "rc 3 printed"),
        (synth, "MADO_DEVICES: SETUP bad_json", "SETUP bad_json reached"),
        (synth, 'MADO_DEV_BLOCK: name="KBD" keys=1 verdict=NO_SUCH_DEVICE', "bracket name in capitals"),
        (synth, 'differ=layout verdict=VIRTUAL', "virtual with a contradicting block"),
    ]
    for body, needle, why in observed:
        checked += 1
        if needle not in body:
            fails.append("receipt lacks the observation for %s: %r" % (why, needle))

    for f in fails:
        print("FAIL " + f)
    print("VERIFY: checked=%d failed=%d" % (checked, len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
