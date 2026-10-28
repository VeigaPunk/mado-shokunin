# R55W2CritEntryProse — overclaim hunt, non-row prose of corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md

Scored revision: 57584ed67716340b3d466fa04333ac0bab3fb79e (equal to the lane worktree for this file; `cmp`-equal via `git show`).
Sections attacked: `What this entry settles`, `What stays UNKNOWN`, `Chain`, `Limits`, `How to verify`.
Row evidence: the K/H/E table rows in the same file, the pinned sources under `.ufo/waves/round-55/fetch/` (sha256 = `c1.pin_sha256`),
and the upstream re-fetch in scratch (see §8). Receipts copied to this directory. No lane file was edited; no git mutation.

Verdict vocabulary: SURVIVES = the sentence is entailed by its cited rows; ROW-GAP = entailed by the pinned source but NOT by the
rows it cites (the cited rows do not carry the fact); BROKEN = the sentence (or its check) is false or contradicted; UNVERIFIED = not checkable here.

## 1. What this entry settles

| # | Sentence (abridged) | Cited rows | Entailed by cited rows? | Pinned source (what I re-read) | Verdict |
|---|---|---|---|---|---|
| S1 | "applyConfigToKeyboard reads repeat rate, delay and numlock through getDeviceInt **with that fallback** (K01, K02, K03)" | K01-K03 | Partly. K01-K03 show the fallback *argument* passed to `getDeviceInt`. No row shows that `getDeviceInt` forwards it to `getConfigValueSafeDevice`. | legacy `ConfigManager.cpp:1132` `auto val = getConfigValueSafeDevice(dev, v, fallback);` (inside getDeviceInt 1131-1137). Line 1132 is quoted by no row; E01 quotes 1134. | ROW-GAP (source entails it) |
| S2 | "getConfigValueSafeDevice returns the global value when the device value is absent or not set by the user (K16, E12)" | K16, E12 | Yes. K16 (1119) tests `(!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty()`; E12 (1120) returns the global. The `!VAL \|\|` part sits outside the K16 quote but on the same line. | legacy 1119-1120 as above | SURVIVES |
| S3 | "IKeyboard::setKeymap reads numlock the same way (K08)" | K08 | Yes for the getDeviceInt call; "the same way" = same helper and fallback, which is S1's ROW-GAP. | IKeyboard.cpp:120 | SURVIVES (inherits S1 gap) |
| S4 | "applyConfigToKeyboard stores the rate and the delay as std::max(0, value) (K04, K05) and stores numlock unfloored (K06)" | K04, K05, K06 | Yes. | InputManager.cpp:1282-1284 `std::max(0, REPEATRATE)`, `std::max(0, REPEATDELAY)`, `= NUMLOCKON;` | SURVIVES |
| S5 | "The unchanged-config early return at line 1271 (K07) compares the config names with the stored fields." | K07 | Incomplete, not false. K07 quotes only `REPEATDELAY == … && REPEATRATE == …`. Line 1271 is a nine-term conjunction that also compares NUMLOCKON with m_numlockOn, RULES, MODEL, LAYOUT, VARIANT, OPTIONS and FILEPATH. The prose names no more than the row shows but says "the config names" as if they were the whole test. | InputManager.cpp:1271 (full line printed by my sed) | SURVIVES (narrowing needed: the test is not only repeat/delay) |
| S6 | "IKeyboard::setKeymap enters its NumLock lock block only when NUMLOCKON equals 1; the if has no else (K09)" | K09 (line 122 only) | "only when equals 1": yes from K09. "has no else": NOT on K09's line; rests on lines 122-131. | IKeyboard.cpp:122-131 printed by me: `if (NUMLOCKON == 1) {` … `    }` at 131, blank 132. No else. | SURVIVES (source); the How-to-verify commands do not print 123-131 (see H4) |
| S7 | "updateActiveKeyboardData sends the active keyboard's stored rate and delay to the seat protocol, and only inside its if (m_keyboard) guard (K10, E09)" | K10, E09 | Yes. Line 178 `PROTO::seat->updateKeymap();` is outside the if (unindented) — not quoted but not needed for the claim. | SeatManager.cpp:176-178 | SURVIVES |
| S8 | "CWLSeatProtocol::updateRepeatInfo calls repeatInfo per keyboard resource when the seat has keyboard capability (E06, E07)" | E06, E07 | Yes for the loop (E07) and the capability test (E06). The `return;` that makes the test a gate is line 605, quoted by no row (E13 quotes 443, the other guard). | Seat.cpp:603-608 | SURVIVES (ROW-GAP on line 605, minor) |
| S9 | "CWLKeyboardResource::repeatInfo sends repeat_info only when the owner is present, the resource version is 4 or later, and the rate and delay are not both equal to the last sent values (K11, E10, K12)" | K11, E10, K12 | **No.** K11 quotes only `m_resource->version() < 4`. The `!m_owner` term and the `rate == m_lastRate && delayMs == m_lastDelayMs` term are on line 442, quoted by no row. The `m_lastRate = rate;` assignment (line 444) is quoted by no row; E10 quotes only line 445 (`m_lastDelayMs = delayMs;`). K12 gives the send. | Seat.cpp:442-447 printed by me: `if (!m_owner \|\| m_resource->version() < 4 \|\| (rate == m_lastRate && delayMs == m_lastDelayMs)) return;` then 444-445 assignments, 447 send | ROW-GAP (source entails it; the cited rows do not) |
| S10 | "K13 … default 25 min 0 max 200; K14 default 600 min 0 max 2000; K15 numlock default false" | K13-K15 | Yes; K13/K14 quotes are the declaration text. | ConfigValues.cpp:277, 279, 280 printed | SURVIVES |
| S11 | "how the config layer enforces the range fields is UNKNOWN" | — (declaration only) | Yes (no enforcement code in pins; grep of legacy ConfigManager for `.min`/`.max` finds only unrelated keys at 862-868, 1969). | — | SURVIVES |

## 2. What stays UNKNOWN

| # | UNKNOWN item | Settled elsewhere? | Verdict |
|---|---|---|---|
| U1 | "What the 'set': true field in host-getoption.json means. The pin records it; no pinned source row defines it." | **Yes, in the corpus.** `corpus/knowledge/hyprctl-getoption-native-forms-r40.md:20` (S158, HyprCtl.cpp:1701-1728 prints `"set": {}`) and `:26` (OBS S279, measured): "`set` is true for exactly the 70 options some file of the tree declares and false for the other 283 … so `set` separates 'a file says so' from 'the engine's default'." The entry's own Joining section points at that file. Consistency check on this host: the three keys are declared in host-input.conf lines 14, 15, 18 and all three read `"set": true` in host-getoption.json. The sentence "no pinned source row defines it" is literally true of this entry's pins and misleading as an UNKNOWN. | UNKNOWN WRONG-PLACED (settled by a held measurement, not by a pinned source row) |
| U2 | "How the hyprlang config layer enforces the min and max fields … not the enforcement code." | No. No pin or corpus row shows enforcement. | SURVIVES |
| U3 | "Whether a negative configured value can reach the early-return comparison … the stored clamped value and the unclamped config value differ … follows from K04, K05 and K07 and is [INFERENCE]" | The reach question is genuinely open (hyprlang parsing not pinned). The consequence is a deduction from K04/K05/K07, labelled INFERENCE, which is right. The word "clamped" is wrong: std::max(0, x) floors only (see C1). | SURVIVES (word "clamped" BROKEN, see C1) |
| U4 | "Which keyboard is m_keyboard at runtime, and therefore which stored rate and delay the seat protocol sends." | No row settles it. Observed but undefined: `hyprctl devices -j` (run now, read-only) lists one keyboard with `"main": true` — `hl-virtual-keyboard-fcitx5` — and every other keyboard `"main": false`. No corpus row defines the `main` field (grep of hyprland-input-devices-r46.md: no definition). The entry never mentions the field. | SURVIVES as UNKNOWN; add the unpinned `main` observation |
| U5 | "Whether any live client binds wl_keyboard at version 4 or later." | No. | SURVIVES (but see C5: the chain omits the bind-time send that would matter if they did) |
| U6 | "What the NumLock lock does on the host's own XKB keymap: K09 pins only the set-up line, not the keymap." | No corpus row covers numlock on the host keymap (grep of xkb-keymap-compile-r48.md and hyprland-input-devices-r46.md: none). Source-level effect (IKeyboard.cpp:124-130: if `XKB_MOD_NAME_NUM` index is valid, set the locked bit; then `updateModifiers(0,0,locked,group)`) is in the pinned file, not stated anywhere in the entry. | SURVIVES (host effect UNKNOWN); source effect is a settled item omitted from `settles` (see S-omission below) |
| U7 | "Whether any value reaches a client. No keypress, wl_keyboard event or client bind was observed" | No. The observation claim about this lane's runs is not re-checked here (UNVERIFIED for "observed"). | SURVIVES (observation claim UNVERIFIED) |

Settled items that are really unknown (the reverse check): none found among the five `settles` bullets. The closest is S9 (ROW-GAP, not unknown) and S1 (ROW-GAP).

## 3. Chain

| # | Chain step / sentence | Verdict | Evidence |
|---|---|---|---|
| C1 | Step 3: "it **clamps** rate and delay (K04, K05)". UNKNOWN U3 also says "the stored **clamped** value". Limits says the same lines "floor at zero … the line sets no upper bound". | **BROKEN (wording)**: std::max(0,x) floors; there is no clamp to 200 or 2000. The chain contradicts the entry's own Limits. The `settles` bullet correctly says "std::max(0, value)". | InputManager.cpp:1282-1283 |
| C2 | Step 3: "applyConfigToKeyboard is called from setupKeyboard (E08)." | ROW-GAP. E08 quotes line 1195 `applyConfigToKeyboard(keeb);` and says "setupKeyboard passes its keeb argument…", but the quoted line does not name setupKeyboard. The header `void CInputManager::setupKeyboard(SP<IKeyboard> keeb) {` is line 1135, quoted by no row (S316 range 1213-1295 excludes it, which Limits admits). Source-level: entailed (1195 is inside 1135-1205). | InputManager.cpp:1135, 1195 printed |
| C3 | Step 3: "Stored fields are declared in IKeyboard (K18, E03)." E03's proposition says "so the declared numlock default is -1 and not 0 or 1." | SURVIVES for the chain sentence. **Row E03's proposition overclaims**: -1 is the member initializer (IKeyboard.hpp:123); the declared numlock config default is `false` (K15); setKeymap reads NUMLOCKON directly, not m_numlockOn. | IKeyboard.hpp:121-123; ConfigValues.cpp:277 |
| C4 | Step 2: "getDeviceInt call sites K01, K02, K03, K08; E01 is the empty-value branch of getDeviceInt." | SURVIVES for E01 (line 1134, `if (!val)` at 1133 — checked). Same S1 ROW-GAP on the forwarding line 1132. | legacy 1131-1134 printed |
| C5 | Step 5: "Seat push: K10 with E09 (guard), E06 and E07 (seat protocol), K11, E13, E10 and K12 (per resource), E04, E05 and K17". Presented as the seat push. | **Omission (chain incomplete).** Seat.cpp:349-350 in the `CWLKeyboardResource` constructor calls `repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate, …m_repeatDelay)` at bind time, so a client that binds wl_keyboard at v4+ receives the stored values with no K10 call. It is the one path where a bind delivers a value, and the UNKNOWN "whether any live client binds v4+" is exactly its trigger. The chain does not name it. | Seat.cpp:336-352 printed |
| C6 | Step 5: "the 1.26.0 wl_keyboard repeat_info event and its rate-zero and negative-value rules" (E05 line 2740, K17 line 2741, E04 line 2732). | SURVIVES. Line 2740 holds both "Negative values for either rate or delay are illegal." and "A rate of zero"; 2741 holds "will disable any repeating (regardless of the value of delay)." The chain does not claim Hyprland implements the rules; Limits says so. | wayland-1.26.0-wayland.xml:2732, 2740-2741 printed |

## 4. Limits

| # | Sentence | Verdict | Evidence |
|---|---|---|---|
| L1 | "Source-level only, at the pinned tag commit efb50993780079460b0cbed1363e2166a2de1d9f." | SURVIVES, and now verified outside the rows. `hyprctl version` (read-only): `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`. Upstream raw at the commit and at `refs/tags/v0.56.2` gives sha256-identical InputManager.cpp and Seat.cpp to the pins (§8). The entry's rows cite the commit (S316-S380) but no row says it is the tag commit; the host self-report is the evidence. | §8 receipts |
| L2 | QUALITY 104: "the 'only' in K09 was checked against … 122-131 (no else branch)." | SURVIVES. Printed 122-132 (§7). | IKeyboard.cpp:122-132 |
| L3 | QUALITY 104: "the 'only' in K10 was checked against the single-statement if at SeatManager.cpp:176-177." | SURVIVES. Printed 170-182; the statement after the if at 178 is unindented, not inside the guard. | SeatManager.cpp:176-178 |
| L4 | "'Floored at zero' in K04 and K05 … the line sets no upper bound." | SURVIVES. This is the correct wording; it contradicts Chain step 3 (C1). | InputManager.cpp:1282-1283 |
| L5 | "K07 … does not state a runtime outcome." | SURVIVES. | — |
| L6 | "getDeviceInt's empty-value branch (E01) is shown by the source; whether the three keys ever reach it is UNKNOWN." | SURVIVES. Reaching it requires `getConfigValueSafeDevice` to return null, i.e. no global either; not pinned. | legacy 1119-1134 |
| L7 | "A quote proves … it does not prove that a proposition sentence is entailed by it." | SURVIVES (correct disclosure; this document is the entailment audit the entry asks for). | — |
| L8 | "The wl_keyboard protocol text … is cited for the event contract and not for Hyprland's implementation of it, which is K11 and K12." | SURVIVES as a boundary statement; K11 is only the version term, so the implementation claim is ROW-GAP as in S9. | — |
| L9 | Registry anchor gaps: S318 `ConfigValues.cpp:271-279` does not reach K14 at 280; S052 `wl_keyboard :2573-2699` does not reach K17 at 2741, E04 at 2732, E05 at 2740 (interface runs 2573-2752); S316 `1213-1295` does not reach E08 at 1195. | SURVIVES. Checked against corpus/SOURCES.md rows 64, 265, 267 and the pins (interface `<interface name="wl_keyboard"` at 2573, `</interface>` at 2752). | corpus/SOURCES.md:64,265,267; wayland pin 2571-2752 |
| L10 | "The counter checks only the S-id URL suffix and status, so it would not catch these." | **BROKEN (understated).** The counter's docstring (quality/counters/c1-r55-kbd-entry.py, `source_cell:<id>`) also requires: exactly one registry row with 11 pipe cells, the frozen commit in the URL for Hyprland pins, and a unique S-id. The conclusion (line-range anchors are not checked) still holds, because the counter never reads a registry line range. The word "only" is false. | counter docstring; run output §7 |

## 5. How to verify (each command run from the lane root, read-only)

| # | Command as written | Ran? | Prints what the text says? | Verdict |
|---|---|---|---|---|
| H1 | `sha256sum .ufo/waves/round-55/fetch/*` | yes, exit 0 | Prints 11 lines. The 10 pinned files match `c1.pin_sha256` (checked programmatically: all True). It also prints `SHA256SUMS.txt`, which is not in `c1.pin_sha256` and is covered by nothing. The text says the output "must match"; no command performs the comparison. | SURVIVES with caveat (manual match; unlisted 11th file) |
| H2 | `python3 -I .ufo/waves/round-55/freeze-verify.py` | yes, exit 0; last line `FREEZE_VERIFY: bad=0 frozen-tables.sha256=bf46c889… OK` | Ends OK as written. **But it verifies the superseded v1 table** (`frozen-tables.json`), and the entry's Source-rows text says "Cells are generated from `frozen-tables.json`" — false for K16: the cell holds the v2 quote `!VAL->m_bSetByUser) && !fallback.empty())`; the v1 quote is `if ((!VAL \|\| …` (`build-entry.py` reads `frozen-tables-v2.json`). The v2 verifier also passes (`freeze-verify-v2.py` → `FREEZE_VERIFY_V2: bad=0 … 13d6e2f9… OK`). The command never reads the markdown cells, and the C1 counter that does (`c1-r55-kbd-entry.py` → `TARGET_MET`, §7) is not listed. | BROKEN (stale table named; counter omitted); runs |
| H3 | `sed -n '1220,1223p;1271p;1282,1284p' …Hyprland-InputManager.cpp` | yes | Prints 1220, 1221, 1222(blank), 1223, 1271, 1282, 1283, 1284 — matches K01-K07. | SURVIVES |
| H4 | `sed -n '120,122p' …Hyprland-IKeyboard.cpp` | yes | Prints lines 120-122 (K08, K09). Does **not** print 123-131, so the "no else" claim in `settles` and Limits cannot be reproduced from the entry's own commands. | SURVIVES, verification gap |
| H5 | `sed -n '176,177p' …Hyprland-SeatManager.cpp` | yes | Prints `if (m_keyboard)` and the call (E09, K10). | SURVIVES |
| H6 | `cat …host-input.conf \| sed -n '14,15p;18p'` | yes | Prints `repeat_rate = 40`, `repeat_delay = 250`, `numlock_by_default = true` — H01-H03 exactly. | SURVIVES |
| H7 | `cat …host-getoption.json` | yes | Three lines equal to H04-H06, each with `"set": true` (the field U1 calls unexplained). | SURVIVES |
| H8 | `hyprctl getoption input:repeat_rate -j` (and repeat_delay, numlock_by_default) | yes, read-only | `{"option": "input:repeat_rate", "int": 40, "set": true }`, `…repeat_delay…250`, `…numlock_by_default…1` — identical to H04-H06 and to H7. | SURVIVES |
| — | Claim "Each quote is an exact substring of the named pin line (checked by the generator and by verify.py)" (Extra rows, not in the five sections but cited by Chain/Limits) | Checked by me: 13/13 E quotes are substrings of the named lines (§7). The "generator" (`integrate/build-entry.py`) does not check E quotes; the referent of "verify.py" is `w1/R55ScribeEntryA/verify.py` (wave-1 seat draft, line 92-105 checks E rows), which How to verify does not run. | SURVIVES on the fact; provenance of the check is misattributed | — |

## 6. Summary of defects, by severity

1. C1 (BROKEN wording): Chain step 3 and U3 say "clamp"; the code floors only; Limits says so.
2. L10 (BROKEN): "The counter checks only the S-id URL suffix and status" — understated.
3. H2 (BROKEN): How to verify runs the superseded v1 verifier; the Source-rows statement "generated from frozen-tables.json" is false for K16; the v2 table and the counter are not in the verification path.
4. S9 (ROW-GAP): "sends only when the owner is present … not both equal to the last sent values" cites K11/E10/K12, which carry only the version term and the m_lastDelayMs assignment. The entailing text is lines 442 and 444, quoted by no row.
5. C5 (omission): Chain step 5 presents K10…K12 as the seat push and omits the bind-time send at Seat.cpp:350.
6. U1 (misplaced UNKNOWN): the `set` field meaning is settled by a held corpus measurement (native-forms-r40 `:26`, S279); the UNKNOWN says only that no pinned source row defines it.
7. S1 / C2 / S8 (ROW-GAP): links needed for "with that fallback" (1132), "called from setupKeyboard" (1135), and "when the seat has keyboard capability" (605) are source-entailed but cited by no row.
8. S5 (narrowing): the early-return test at 1271 compares nine terms; the prose names two.
9. H4 (verification gap): the no-else claim is not printed by any How-to-verify command (123-131 missing).
10. C3 (row-level): E03's proposition "declared numlock default is -1" overclaims (member initializer, not the config default).
11. U4 (missing observation): the host dump's unpinned `main: true` on `hl-virtual-keyboard-fcitx5` is not mentioned; still UNKNOWN.

## 7. Receipts (read-only, run now; output reproduced)

- `freeze-verify.py` (v1): exit 0, last line `FREEZE_VERIFY: bad=0 frozen-tables.sha256=bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490 OK` (file: `freeze-verify-run.txt`).
- `freeze-verify-v2.py`: exit 0, `FREEZE_VERIFY_V2: bad=0 frozen-tables.sha256=13d6e2f9c0dfe1287e2cd9a7d814d95a4fb0ff0ad7ce644aad7ead18af69a7b9 OK` (file: `freeze-verify-v2-run.txt`).
- `quality/counters/c1-r55-kbd-entry.py --repo <lane> --rev 57584ed67716340b3d466fa04333ac0bab3fb79e --work <scratch>`: exit 0, `MADO_KBD_ENTRY: rev=57584ed6… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` (file: `c1-counter-run.txt`). Counter is the only check that binds markdown cells to tables; it says nothing about prose.
- Extra-row check (E01-E13, Python, `re` over the entry table vs named pin line): 13/13 substring (E01 1134, E02 60, E03 123, E04 2732, E05 2740, E06 604, E07 608, E08 1195, E09 176, E10 445, E11 2740, E12 1120, E13 443).
- Table-vs-table (K/H quote cells vs frozen JSON): 23/24 equal to v2 and v1; K16 equal to v2 only (v1 differs).
- Unlisted line prints (receipts in `extra-receipts.txt`): IKeyboard 122-132 (no else), legacy 1131-1134 and 1119-1120, Seat 441-445 and 603-605, InputManager 1135 header and 1195 call, `hyprctl devices -j` keyboard `main` field (one `true`, `hl-virtual-keyboard-fcitx5`).
- `hyprctl version` (read-only): `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`.
- `sha256sum` of the 10 pins: 10/10 equal to `c1.pin_sha256`.

## 8. Upstream re-open (network read, raw URLs only)

Commit `efb50993780079460b0cbed1363e2166a2de1d9f` raw files, sha256 vs pins: ConfigValues, IKeyboard.cpp, IKeyboard.hpp, InputManager, SeatManager, legacy ConfigManager, protocols/core Seat — all equal. Tag `refs/tags/v0.56.2`: InputManager and protocols/core Seat — equal to the same pins. gitlab `1.26.0/protocol/wayland.xml` — `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, equal to the pin. Scratch copies were under `/fast/scratch/hyaku/mado-r55/R55W2CritEntryProse/upstream` and are removed before yield.

## 9. Not verified

- The meaning of `"main"` in `hyprctl devices -j` (U4): no pinned source and no corpus definition found; HyprCtl.cpp not re-read.
- Whether any live client binds wl_keyboard at v4+ (U5), and whether the NumLock modifier exists in the host keymap (U6): not observable from the allowed reads.
- The "observed" claim in U7 (no keypress or client bind observed): not re-checked against the lane's run logs.
- Whether the hyprlang parser accepts negative integers for these keys (U3): not pinned.
