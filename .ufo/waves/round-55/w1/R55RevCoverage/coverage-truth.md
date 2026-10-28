# Round 55 — C1 coverage truth at base 3b55b6e91e40f455dd56b2985e4ffc087ada92d5

Seat R55RevCoverage (leaf, read-only). Receipt: `receipts/base-grep.txt` in this directory (full grep output, exit codes, the
absent-entry check, the S-id ceiling and the round-55 fetch cross-check are reproduced there).

## 1. Verdict on the claim "the surface is uncovered at base"

**Confirmed for the surface the entry moves, refuted for the three option names as strings.**

- The per-keyboard source chain is uncovered in `corpus/knowledge`, `corpus/SOURCES.md`, `corpus/README.md`, `tools`, `SKILL.md`
  and `PROVINCE.md`. Zero hits at base for `repeat_info`, `m_repeatRate`, `updateRepeatInfo`, `SeatManager`, `protocols/core/Seat`,
  `IKeyboard.hpp`, `applyConfigToKeyboard` (apart from the r46 six-names paragraph, which does not touch repeat or numlock), `getDeviceInt`.
  Zero hits for the default values as repeat/delay figures. Max S-id at base is S377; `hyprland-keyboard-repeat-numlock-r55.md` is absent
  (`git cat-file -e` exit 128).
- The three option names do appear: 16 hits from the lane-specified grep, plus 4 more from a broad sweep for `numlock|repeat rate/delay`
  (README:122, config-option-table-r39:70, SKILL.md:76, plus the tool-level NumLock/numLock tokens). Every one is classified in §2.
- Whole-tree (outside the lane's grep scope): `repeat_info` / `m_repeatRate` occur in `.ufo/waves/round-15/*` reports and round-46/49/50/52
  fetch and receipt files, never in `corpus/knowledge`. So the protocol-side and source-side readings exist as wave evidence, not as corpus
  knowledge. Expansion credit applies to corpus ground only (see §3).

## 2. Classification of every hit (lane grep: `corpus/knowledge tools SKILL.md PROVINCE.md`, 16 lines)

| hit (base) | text (abridged) | class | what it claims |
|---|---|---|---|
| `corpus/knowledge/config-health-report-r3.md:546-548` | `input:repeat_rate` 40, `repeat_delay` 250, `numlock_by_default` 1, `set`, `agreement` | **sourced claim, host readback** [OBS] | live `getoption` equals the file's declared global value. Global option only. |
| `corpus/knowledge/config-health-report-r3.md:829-831` | same three rows, machine block | **sourced claim, host readback** (duplicate of 546-548 in another form) | same |
| `corpus/knowledge/hyprctl-verification-layer.md:132-134` | `L-IN:14 = 40` / `L-IN:15 = 250` / `L-IN:18 = true` → `int: 40 / 250 / 1`, `agreement` | **sourced claim, host readback** (legend: `agreement` = live equals resolved last declaration) | same; declarer lines cited |
| `corpus/knowledge/hyprland-input-devices-r46.md:34` | `numLock` in `hyprctl devices -j` is locked-modifier state, "not the `numlock_by_default` option" | **sourced claim** (Hyprland-HyprCtl.cpp:793-801) | disambiguation: the dump's numLock field is not the option |
| `corpus/knowledge/hyprland-input-devices-r46.md:70` | `repeat_rate`, `repeat_delay`, `numlock_by_default` "applied per device too but the dump prints none of them … they are UNK for this join" | **UNK / open note** | the exact open item C1 claims to close |
| `tools/mado-options.py:1345` | `repeat_rate = $r` inside a self-test fixture string | **passing mention** (test input) | none |
| `tools/mado-options.py:1407` | `input:repeat_rate` in an expected-key list of a self-test | **passing mention** (test) | none |
| `tools/mado-options.py:1495` | `row_of("input:repeat_rate")`, self-test "variable in user file" | **passing mention** (test) | none |
| `tools/mado-options.py:1584` | merged-row fixture `input:repeat_rate` value 40 | **passing mention** (test fixture) | none |
| `tools/mado-options.py:1607` | self-test `agreement` assertion on `input:repeat_rate` | **passing mention** (test) | none |

Classes present: sourced claim (3 host readback, 1 disambiguation), UNK note (1), gate row (none: no gate row names these options), passing mention (5, all in the tool's self-test).
No hit is a source-level claim about how the compositor applies the option to a keyboard.

Additional broad-sweep hits (not in the lane grep):

| hit | class |
|---|---|
| `corpus/README.md:122` | index narrative for r46: "the per-device settings the dump never prints (`repeat_rate`, `repeat_delay`, `numlock_by_default`, …)" — restates the r46 UNK; an index pointer, not a claim |
| `corpus/knowledge/config-option-table-r39.md:70` | `[INF]` ownership: the operator's `input.conf` owns "repeat 40/250, numlock" — passing, no keyboard-level claim |
| `SKILL.md:76` | route row "Keyboard layout / repeat / touchpad" → `hyprctl getoption input:kb_layout`; names no repeat option — passing |
| `tools/mado-devices.py:485` | stub keyboard JSON with `"numLock": False` — lock-state field, passing |
| `tools/mado-keysym.py:1719,1755,1756,1783,1846` | `NumLock` as an XKB virtual modifier/keymap entry — unrelated to the option, passing |

## 3. What the existing notes already claim, and whether C1 duplicates them

**Existing claims about the three options at base:**

1. Host readback (config-health-report-r3 §2.4 and machine block; hyprctl-verification-layer §3.2): the global options equal the declared
   values (40 / 250 / 1), `agreement`. These prove the *global* option is what the file says. They say nothing about any keyboard's
   effective value or about `wl_keyboard.repeat_info`.
2. r46 line 70: the three options are per-device-applicable and the dump does not print them — UNK for the join.
3. r46 line 34: the dump's `numLock` is lock state, not `numlock_by_default`.
4. r39 line 70: operator-owned by `input.conf` (INF).

**Duplication test per C1 row family:**

| C1 rows | ground at base | credit |
|---|---|---|
| H01–H06 (host pin quotes: `repeat_rate = 40`, `repeat_delay = 250`, `numlock`, and the getoption-side values) | the same 40 / 250 / 1 values are already `agreement` in config-health-report-r3 §2.4 (lines 546-548) and hyprctl-verification-layer (132-134). | **No expansion credit.** These rows restate held ground under a new pin. Label them as restatement in the entry or the index. |
| K rows on the source chain (SeatManager `updateActiveKeyboardData`, Seat `repeatInfo` / `updateRepeatInfo`, IKeyboard members `m_repeatRate`/`m_repeatDelay`/`m_numlockOn`, `applyConfigToKeyboard` per-device repeat and numlock, `getDeviceInt` fallback to global, built-in defaults 25/600/0, `std::max(0, …)` clamp) | none at base (§1 zero-hit list) | **Expansion credit.** Ground the lane did not hold. |
| K rows on the protocol side (`wl_keyboard.repeat_info`, S052 wayland 1.26.0) | no corpus note; `repeat_info` appears only in `.ufo/waves/round-15/w1/reports/WaylandKeyboard.md:125-126` and `ReviewKeyboard.md:16` (`wayland.xml:2732-2751`, not admitted to corpus). | **Expansion credit on corpus ground** only; the entry should cite the round-15 reading as prior wave evidence rather than present it as first-seen. |
| The open UNK at r46:70 | held as UNK | **Expansion credit** for closing it for these three names — provided the entry states per-keyboard effective values and does not re-present the global readback as per-keyboard verification. |

**Risks for integration (not edits; the seat does not touch tracked files):**

- r46:70 and corpus/README.md:122 remain UNK after the entry lands unless the L1 adds a cross-link. A reader would see both "UNK" and a sourced entry.
- r46:34 says the dump's `numLock` is lock state, not the option. A K row that says "numlock_by_default is verified by `hyprctl devices`" would contradict it. The entry must not conflate the two fields.
- The host readback "agreement" (config-health, hyprctl-verification-layer) means *global value equals declaration*. The new entry's `from=` / per-keyboard effective value is a different claim. The entry should say so, or a reader may take "agreement" as keyboard-level verification.

## 4. Cross-check of the S380 anchor (IKeyboard.hpp members :121-123)

- `.ufo/waves/round-55/fetch/Hyprland-IKeyboard.hpp` sha256 `82e0bc9e1f31f6342f193b0981000245b932719cf406988d98aba64f0f716f05`, matching the
  `SHA256SUMS.txt` line and the S363 row's recorded sha in `corpus/knowledge/hyprland-bind-key-match-r50.md:13`.
- Lines 120-123: `m_currentRules` (120), `m_repeatRate = 0` (121), `m_repeatDelay = 0` (122), `m_numlockOn = -1` (123). Matches the
  registration's S380 anchor `:121-123`.
- The round-46 receipt `.ufo/waves/round-46/w1/LabVirtualRules/receipts/IKeyboard.hpp` has the same sha and the same lines.

## 5. Not verified / limits

- Not run: the C1 counter, the C1 harness, the C1 controls, `mado-verify.sh --selftest`. Out of this seat's assignment.
- Not verified: the `efb50993` provenance of the round-46 receipt beyond its matching sha with the S363 row.
- Not verified: the full text of `corpus/SOURCES.md` S052 row beyond its first 260 characters.
- The sealed hold-out was not looked for or read.
- No host command was run in this seat.
- No tracked file was modified; no git mutation.
