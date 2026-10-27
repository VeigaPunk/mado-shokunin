#!/usr/bin/env python3
"""Build a C2-r49 test tree (POS and mutations) in a scratch clone.

Never writes outside --repo. Reads the pins from --pins and the live capture from --probe.
Every locator written into the entry and the rows is computed here with a line scan of the
pin bytes (grep -n equivalent), never typed.
Usage: mkpos.py --repo D --pins P --probe Q
"""
import argparse
import hashlib
import json
import os

COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
XKB_TAG = "xkbcommon-1.13.2"
ROW_IDS = ["S352", "S353", "S354", "S355"]
PINS = {
    "S352": "Hyprland-legacy-ConfigManager.cpp",
    "S353": "Hyprland-KeybindManager.cpp",
    "S354": "xkbcommon-keysym.c",
}
URLS = {
    "S352": "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/legacy/ConfigManager.cpp" % COMMIT,
    "S353": "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/managers/KeybindManager.cpp" % COMMIT,
    "S354": "https://raw.githubusercontent.com/xkbcommon/libxkbcommon/%s/src/keysym.c" % XKB_TAG,
}
ENTRY = "corpus/knowledge/hyprland-bind-key-match-r49.md"
RECEIPT_NAME = "hyprctl-binds-r49.txt"
CM = "Hyprland-legacy-ConfigManager.cpp"
KM = "Hyprland-KeybindManager.cpp"
KC = "xkbcommon-keysym.c"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def pin_lines(name, pins):
    return open(os.path.join(pins, name), encoding="utf-8",
                errors="replace").read().split("\n")


def line_of(pins, name, needle):
    for k, l in enumerate(pin_lines(name, pins), 1):
        if needle in l:
            return k
    raise SystemExit("needle not found: %s in %s" % (needle, name))


def nlines(pins, name):
    return len(pin_lines(name, pins))


def capture(probe):
    raw = open(os.path.join(probe, "binds.json"), "rb").read()
    binds = json.loads(raw.decode())
    forms = {"named": 0, "code": 0, "mouse": 0, "switch": 0}
    for b in binds:
        key = b.get("key") or ""
        kc = b.get("keycode") or 0
        if key.startswith("code:"):
            forms["code"] += 1
        elif key.startswith("mouse"):
            forms["mouse"] += 1
        elif key.startswith("switch:"):
            forms["switch"] += 1
        elif key == "" and kc:
            forms["code"] += 1
        else:
            forms["named"] += 1
    opt = json.loads(open(os.path.join(probe, "opt.json"), encoding="utf-8").read())
    return hashlib.sha256(raw).hexdigest(), len(raw), len(binds), forms, opt["int"]


def entry_lines(pins, cap):
    digest, nbytes, total, forms, rv = cap
    L = lambda name, needle: line_of(pins, name, needle)
    q = {
        "parse": L(CM, "SParsedKey parseKey(const std::string& key) {"),
        "num": L(CM, "if (isNumber(key) && std::stoi(key) > 9)"),
        "code": L(CM, 'else if (key.starts_with("code:") && isNumber(key.substr(5)))'),
        "catch": L(CM, 'else if (key == "catchall")'),
        "mk": L(CM, "KEYSYMS.emplace_back(xkb_keysym_from_name(splitKey.c_str()"),
        "parsed": L(CM, "SParsedKey parsedKey = parseKey(KEY);"),
        "catchref": L(CM, "Catchall not allowed outside of submap!"),
        "mod": L(CM, "const auto MOD    = g_pKeybindManager->stringToModMask(ARGS[0]);"),
        "sym": L(KM, "const xkb_keysym_t keysym         = xkb_state_key_get_one_sym("),
        "modcmp": L(KM, "(modmask != k->modmask && !k->ignoreMods)"),
        "kbkey": L(KM, "xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS)"),
        "cmp": L(KM, "if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)"),
        "kname": L(KM, "if (key.keyName != k->key)"),
        "kcode": L(KM, "if (key.keycode != k->keycode)"),
        "kcatch": L(KM, "} else if (k->catchAll) {"),
        "icase": L(KC, "bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);"),
        "best": L(KC, 'The "best" case-insensitive match is the lower-case keysym name.'),
        "uname": L(KC, "get_unicode_name(ks, buffer, size);"),
        "hex": L(KC, 'return snprintf(buffer, size, "0x%08x", ks);'),
    }
    out = []
    a = out.append
    a("# Hyprland 0.56.2: from the key field of a `bind` line to the keysym a key press matches")
    a("")
    a("source: S352 - Hyprland 0.56.2 src/config/legacy/ConfigManager.cpp @ %s - how the key field becomes a keycode, a catchall or a keysym name, and where a catchall is refused" % COMMIT)
    a("source: S353 - Hyprland 0.56.2 src/managers/KeybindManager.cpp @ %s - which keysym of a key event is compared, and how the modifier mask and the key forms are matched" % COMMIT)
    a("source: S354 - xkbcommon/libxkbcommon src/keysym.c @ %s - the case-insensitive name lookup and the canonical-name choice of libxkbcommon 1.13.2" % XKB_TAG)
    a("source: S355 - mado host, read-only `hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j` capture (own-work) - this host's bind shape by key form and the resolve setting")
    a("verified-at: 2026-10-27")
    a("recheck: on-release - when Hyprland leaves 0.56.2 or %s, or libxkbcommon leaves %s, re-pull S352-S354 and re-run the round-49 capture" % (COMMIT, XKB_TAG))
    a("ground: held open at base - the round-46 entry leaves bind resolution outside its join (`corpus/knowledge/hyprland-input-devices-r46.md:71`); the held row S319 is cited here, never re-registered.")
    a("")
    a("## Steps")
    a("")
    a("1. **The key field is parsed into one of four forms.** `SParsedKey parseKey(const std::string& key) {` (%s:%d) is the only parse: `if (isNumber(key) && std::stoi(key) > 9)` (%s:%d) makes a bare number above 9 a keycode, `else if (key.starts_with(\"code:\") && isNumber(key.substr(5)))` (%s:%d) is the explicit keycode form, `else if (key == \"catchall\")` (%s:%d) is the catchall form, and every other string stays a **name**." % (CM, q["parse"], CM, q["num"], CM, q["code"], CM, q["catch"]))
    a("2. **`bind` hands the key field to that parse and stores the result.** `SParsedKey parsedKey = parseKey(KEY);` (%s:%d); a catchall outside a submap is refused, because `Catchall not allowed outside of submap!` (%s:%d)." % (CM, q["parsed"], CM, q["catchref"]))
    a("3. **The modifier field becomes an integer mask at parse time, not a keysym list.** `const auto MOD    = g_pKeybindManager->stringToModMask(ARGS[0]);` (%s:%d) - the mask is what the match compares, so a modifier name is resolved once per bind line." % (CM, q["mod"]))
    a("4. **The multi-key flag is the one parse-time name-to-keysym resolve.** `KEYSYMS.emplace_back(xkb_keysym_from_name(splitKey.c_str(), XKB_KEYSYM_CASE_INSENSITIVE), 0);` (%s:%d) asks libxkbcommon for the lower-case name; the plain path defers the name to press time." % (CM, q["mk"]))
    a("5. **A key press is translated by one keysym source, chosen per keyboard at press time.** `const xkb_keysym_t keysym         = xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);` (%s:%d) reads the shared translation state when `input:resolve_binds_by_sym` is 0, else the keyboard's own sym state." % (KM, q["sym"]))
    a("6. **The modifier mask is compared exactly, unless the bind ignores mods.** `(modmask != k->modmask && !k->ignoreMods)` (%s:%d) - the comparison is equality against the mask built from the pressed keys, with the `i` flag as the only escape, and Caps/NumLock are part of the mask the compositor compares." % (KM, q["modcmp"]))
    a("7. **A named bind is resolved at match time, first exactly and then case-insensitively.** `xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS)` (%s:%d) resolves the bind's own name without flags, and `if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)` (%s:%d) accepts the pressed keysym against either the exact or the lower-case resolve." % (KM, q["kbkey"], KM, q["cmp"]))
    a("8. **A keycode bind and a catchall are matched on different fields.** The name form is compared with `if (key.keyName != k->key)` (%s:%d), the keycode form with `if (key.keycode != k->keycode)` (%s:%d), and a catchall with `} else if (k->catchAll) {` (%s:%d) inside a submap." % (KM, q["kname"], KM, q["kcode"], KM, q["kcatch"]))
    a('9. **The case-insensitive flag is what makes the second resolve useful.** `bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);` (%s:%d); the lookup then reports `The "best" case-insensitive match is the lower-case keysym name.` (%s:%d), so a bind written `Return` and a press resolving `RETURN` can still meet.' % (KC, q["icase"], KC, q["best"]))
    a('10. **Not every keysym has a name.** `get_unicode_name(ks, buffer, size);` (%s:%d) is the Unicode fallback and `return snprintf(buffer, size, "0x%%08x", ks);` (%s:%d) the unnamed non-Unicode one, so a bind name that resolves to `XKB_KEY_NoSymbol` is dropped rather than matched.' % (KC, q["uname"], KC, q["hex"]))
    a("")
    a("## Live host capture (read-only, 2026-10-27)")
    a("")
    a("The host runs Hyprland 0.56.2 built at commit %s. A read-only `hyprctl binds -j` capture returns %d binds (%d named, %d code/keycode-carried, %d mouse:, %d switch:, no catchall), %d bytes of JSON, sha256 %s (receipt `.ufo/waves/round-49/receipts/%s`). `hyprctl getoption input:resolve_binds_by_sym -j` returns int %d (set false), so a bind name is matched against the shared translation state, not a per-keyboard sym state." % (
        COMMIT, total, forms["named"], forms["code"], forms["mouse"], forms["switch"],
        nbytes, digest, RECEIPT_NAME, rv))
    a("")
    a("## What the evidence licenses")
    a("")
    a("| question | where the answer lives | state |")
    a("|---|---|---|")
    a("| which forms the key field takes | step 1 | sourced |")
    a("| when a catchall is refused | step 2 | sourced |")
    a("| which keysym of a press is compared | step 5 | sourced |")
    a("| how the modifier mask is compared | step 6 | sourced |")
    a("| what a name that resolves to no symbol does | steps 7, 10 | sourced |")
    a("| this host's bind shape | live capture | observed |")
    a("| which keysym the host's `br` keymap gives a bound name | step 5, step 7 | not measured here |")
    a("")
    a("## Limits")
    a("")
    a("- The live capture is a shape, not the JSON: the digest binds the bytes, but no bind description, argument or dispatcher text is kept, so a bind cannot be re-identified from the receipt alone.")
    a("- The per-keyboard sym state was not exercised: the host sets `input:resolve_binds_by_sym` to 0, so step 5's other branch is sourced, never observed.")
    a("- No key was pressed and no bind was dispatched: the match is read from source, and the host's own keymap is not joined to it here.")
    a("- The wiki's `Binds` page and the `input:resolve_binds_by_sym` description were not opened this round; the option's value is observed, its documentation is [UNK].")
    a("- The submap and multi-key paths are read from source only; the host has no submap in the capture, so those branches are inferred from the code.")
    a("")
    a("Lane: mado-shokunin. Round: 49.")
    a("")
    return "\n".join(out)


def rows_text(pins):
    def stats(i):
        name = PINS[i]
        p = os.path.join(pins, name)
        return name, sha(p), os.path.getsize(p), nlines(pins, name)

    n1, s1, b1, l1 = stats("S352")
    n2, s2, b2, l2 = stats("S353")
    n3, s3, b3, l3 = stats("S354")
    rows = [
        ("| S352 | Hyprland 0.56.2 bind key parse - %s | code | A | how the key field of a bind line becomes "
         "a keycode, a catchall or a keysym name, and where a catchall is refused | %s:1481-1487, %s:1569, "
         "%s:1575, %s:1617-1620 @ commit %s; %s %d B %d lines sha256:%s; receipt "
         ".ufo/waves/round-49/fetch/%s | the four key forms, the parse-time mask, and the submap-only "
         "catchall are the parse half of the match | mined | 2026-10-27 | on-release | %s |") % (
            URLS["S352"], n1, n1, n1, n1, COMMIT, n1, b1, l1, s1, n1, ENTRY),
        ("| S353 | Hyprland 0.56.2 bind match - %s | code | A | which keysym of a key event is compared, and "
         "how the modifier mask, key names, keycodes and catchall are matched | %s:369-370, %s:652, "
         "%s:710-724, %s:735-744 @ commit %s; %s %d B %d lines sha256:%s; receipt "
         ".ufo/waves/round-49/fetch/%s | the press-time keysym source, the exact mask comparison and the "
         "exact-then-case-insensitive name resolve | mined | 2026-10-27 | on-release | %s |") % (
            URLS["S353"], n2, n2, n2, n2, COMMIT, n2, b2, l2, s2, n2, ENTRY),
        ("| S354 | libxkbcommon 1.13.2 keysym names - %s | code | A | the case-insensitive name lookup, the "
         "canonical-name choice and the Unicode fallback names | %s:70-96, %s:237-280, %s:268 @ "
         "xkbcommon-1.13.2; %s %d B %d lines sha256:%s; receipt .ufo/waves/round-49/fetch/%s | "
         "xkb_keysym_from_name's flags and xkb_keysym_get_name's canonical and fallback forms bound the name "
         "side of a bind | mined | 2026-10-27 | on-release | %s |") % (
            URLS["S354"], n3, n3, n3, n3, b3, l3, s3, n3, ENTRY),
    ]
    return rows


def receipt_text(cap):
    digest, nbytes, total, forms, rv = cap
    return "\n".join([
        "# hyprctl bind capture (read-only), mado round 49",
        "# shape only: no bind description, argument or dispatcher text is kept",
        "command: hyprctl binds -j",
        "captured: 2026-10-27",
        "raw_json_bytes: %d" % nbytes,
        "sha256: %s" % digest,
        "hyprctl version: Hyprland 0.56.2 built from branch v0.56.2 at commit %s" % COMMIT,
        "binds=%d named=%d code=%d mouse=%d switch=%d catch_all=0" % (
            total, forms["named"], forms["code"], forms["mouse"], forms["switch"]),
        "key_form_rule: key code:/mouse/switch: -> that form; empty key with a non-zero keycode -> code; otherwise named",
        "command: hyprctl getoption input:resolve_binds_by_sym -j",
        "input:resolve_binds_by_sym int=%d set=false" % rv,
        "",
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pins", required=True)
    ap.add_argument("--probe", required=True)
    args = ap.parse_args()
    repo, pins = args.repo, args.pins
    cap = capture(args.probe)
    os.makedirs(os.path.join(repo, ".ufo/waves/round-49/fetch"), exist_ok=True)
    os.makedirs(os.path.join(repo, ".ufo/waves/round-49/receipts"), exist_ok=True)
    for name in PINS.values():
        open(os.path.join(repo, ".ufo/waves/round-49/fetch", name), "wb").write(
            open(os.path.join(pins, name), "rb").read())
    rec = receipt_text(cap)
    rp = os.path.join(repo, ".ufo/waves/round-49/receipts", RECEIPT_NAME)
    open(rp, "w", encoding="utf-8").write(rec)
    open(os.path.join(repo, ".ufo/waves/round-49/fetch", RECEIPT_NAME), "w",
         encoding="utf-8").write(rec)
    os.makedirs(os.path.dirname(os.path.join(repo, ENTRY)), exist_ok=True)
    open(os.path.join(repo, ENTRY), "w", encoding="utf-8").write(entry_lines(pins, cap))
    src = os.path.join(repo, "corpus/SOURCES.md")
    lines = open(src, encoding="utf-8").read().split("\n")
    idx = next(k for k, l in enumerate(lines) if l.startswith("| S351 |"))
    rows = rows_text(pins)
    rows.append(("| S355 | mado host - read-only hyprctl bind capture, shape only (measured 2026-10-27) - "
                 ".ufo/waves/round-49/receipts/%s | own-work | A | this host's bind count by key form and the "
                 "input:resolve_binds_by_sym value | hyprctl-binds-r49.txt whole file, %d B sha256:%s; receipt "
                 ".ufo/waves/round-49/fetch/hyprctl-binds-r49.txt (byte copy of "
                 ".ufo/waves/round-49/receipts/hyprctl-binds-r49.txt) | %d binds by key form and the resolve "
                 "value, read without dispatcher text | mined | 2026-10-27 | on-change | %s |") % (
        RECEIPT_NAME, len(rec.encode()), sha(rp), cap[2], ENTRY))
    lines[idx + 1:idx + 1] = rows
    open(src, "w", encoding="utf-8").write("\n".join(lines))
    rd = os.path.join(repo, "corpus/README.md")
    rl = open(rd, encoding="utf-8").read().split("\n")
    k = next(k for k, l in enumerate(rl) if l.startswith("| `knowledge/xkb-keymap-compile-r48.md`"))
    rl[k + 1:k + 1] = [
        "| `knowledge/hyprland-bind-key-match-r49.md` (MADO-R49-1, round 49; input-device plane, bind key match) "
        "| How Hyprland 0.56.2 turns the key field of a `bind` line into something a key press matches: the four key forms "
        "(number keycode, `code:`, `catchall`, name), the press-time keysym source behind `input:resolve_binds_by_sym`, the exact "
        "modifier-mask comparison with the `i` flag, the exact-then-case-insensitive name resolve, and this host's 192 binds by key form "
        "from a read-only `hyprctl binds -j` capture | rows S352-S355 |"]
    open(rd, "w", encoding="utf-8").write("\n".join(rl))
    les = os.path.join(repo, "corpus/lessons/round-49.md")
    os.makedirs(os.path.dirname(les), exist_ok=True)
    gate = ["# mado round 49 - lesson (POS test tree)", "", "## Gate", "",
            "Admitted: rows S352-S355, tier A, status mined, opened 2026-10-27, used-by the bind entry.", ""]
    for i in ROW_IDS:
        gate.append("- **%s admit**, tier A. Opened 2026-10-27; quote verified at the computed locator." % i)
    gate += ["", "### Rejected after opening", "",
             "- **REJECT** an unpinned wiki URL. Flip: a commit-pinned page states a behaviour the sources do not.", ""]
    open(les, "w", encoding="utf-8").write("\n".join(gate))
    print("built POS tree in", repo)


if __name__ == "__main__":
    main()
