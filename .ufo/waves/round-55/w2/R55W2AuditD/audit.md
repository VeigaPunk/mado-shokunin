# R55W2AuditD: sentence-to-pin audit of K11-K15 (hyprland-keyboard-repeat-numlock-r55.md)

Scope: rows K11, K12, K13, K14, K15 only. Lane revision 57584ed67716340b3d466fa04333ac0bab3fb79e. Pins at `.ufo/waves/round-55/fetch/` at Hyprland efb50993780079460b0cbed1363e2166a2de1d9f. Receipts: `receipts.txt` and `upstream-receipts/` in this directory.

Method: for each row, read the proposition, the cited pin line, and the neighbouring lines (K11/K12: Seat.cpp 441-447, plus 350 and 603-608; K13-K15: ConfigValues.cpp 276-281). Labels: SUPPORTED (the quote entails the proposition), HELD (stated as held/unknown with its boundary named), OVERREACH (stronger than the quote), UNSUPPORTED.

Upstream check: `curl` of raw.githubusercontent.com at efb50993780079460b0cbed1363e2166a2de1d9f for `src/protocols/core/Seat.cpp`, `src/config/values/ConfigValues.cpp` and `src/managers/SeatManager.cpp`. Each is byte-equal (`cmp`) to its committed pin, and each sha256 matches `SHA256SUMS.txt` (cc23bb8b..., a76f0507..., bd748553...). Also fetched, not lane-pinned: `Seat.hpp`, `ConfigValues.hpp`, `types/IntValue.hpp`, `types/IntValue.cpp` (same commit), used only for the adjacent findings below.

## Row table

| Row | Proposition (abridged) | Pin:line | Neighbour lines checked | Label | Evidence |
|---|---|---|---|---|---|
| K11 | One of the three OR-joined conditions on the guard of `CWLKeyboardResource::repeatInfo` is version below 4; the return is line 443 and is not quoted. | Seat.cpp:442 | 441 signature; 443 `return;`; 442 is `if (!m_owner \|\| m_resource->version() < 4 \|\| (rate == m_lastRate && delayMs == m_lastDelayMs))`. The top-level `\|\|` has three operands: `!m_owner`, `version() < 4`, and a parenthesised `&&`. | SUPPORTED | Quote found exactly once in the pin, at 442 (receipts.txt). Byte-equal upstream. |
| K12 | After the early return and the update of m_lastRate and m_lastDelayMs, repeatInfo calls sendRepeatInfo with rate and delayMs. | Seat.cpp:447 | 443 `return;`; 444-445 `m_lastRate = rate;` / `m_lastDelayMs = delayMs;`; 447 `m_resource->sendRepeatInfo(rate, delayMs);`. Sequence and arguments match. The `sendRepeatInfo` name is the generated method; the row does not claim its wire event, and nothing in the pins maps it to `repeat_info`. | SUPPORTED | Quote found exactly once, at 447. The row makes no claim beyond the call. Wire-event mapping is not claimed by K12 itself (see adjacent note A3). |
| K13 | `input:repeat_rate` is declared with default 25 and range fields min 0 and max 200. | ConfigValues.cpp:279 | 276-281 are the same `MS<...>("input:...", desc, default, {options})` shape. 279 is `MS<Int>("input:repeat_rate", "...", 25, {.min = 0, .max = 200, .refresh = ...})`. No second declaration of `repeat_rate` in any pinned .cpp. | SUPPORTED | Quote found once, at 279. "Default" is the third positional argument of `MS` = `makeConfigValue` (upstream ConfigValues.hpp:111-113 forwards `def`), stored as `m_default` (upstream IntValue.cpp:5-6). This last link is upstream, not lane-pinned. |
| K14 | `input:repeat_delay` is declared with default 600 and range fields min 0 and max 2000. | ConfigValues.cpp:280 | 279 (repeat_rate, above); 281 `input:sensitivity`. The line has no `.refresh`; the row does not claim one. | SUPPORTED | Quote found once, at 280. Same `makeConfigValue` / `m_default` link as K13. |
| K15 | `input:numlock_by_default` is a Bool option, default false, described as engaging numlock by default. | ConfigValues.cpp:277 | 276 `kb_file`; 278 `resolve_binds_by_sym` (also Bool, default false). Line 277 is `MS<Bool>("input:numlock_by_default", "Engage numlock by default.", false, {.refresh = ...})`. | SUPPORTED | Quote found once, at 277. The Bool type is the `MS<Bool>` token in the pin. `CBoolValue` is not fetched; the row does not state how Bool is parsed. |

Result: 5 of 5 rows SUPPORTED. No row is OVERREACH or UNSUPPORTED. Each row's boundary (no enforcement claim, no runtime claim, no wire claim) is already in the entry's Limits and UNKNOWN sections, and the rows themselves stay inside it.

## Adjacent findings (prose tied to K11/K12, not rows; reported, not counted)

These are neighbour-line effects the K11/K12 chain does not show. Each has its exact sentence, cited line, neighbour, and minimal corrected wording.

### A1. OVERREACH: the seat-push chain names one route; a second caller exists

- Sentence: Chain, step 5: "Seat push: K10 with E09 (guard), E06 and E07 (seat protocol), K11, E13, E10 and K12 (per resource), E04, E05 and K17". Scope line 17 has the same single-route shape.
- Cited line: Seat.cpp:442 and 447 (K11, K12).
- Neighbour that matters: Seat.cpp:350 (pinned, not cited by any row):
  `repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate, g_pSeatManager->m_keyboard->m_repeatDelay);`
  It sits in the `CWLKeyboardResource` constructor (Seat.cpp:337-360) and sends the active keyboard's stored rate and delay when a client binds `wl_keyboard`. It does not pass through `updateActiveKeyboardData` (K10) or `CWLSeatProtocol::updateRepeatInfo` (E06, E07). It does pass through the same K11 guard.
- Why it matters: a reader following the chain would think the repeat values reach a client only on a seat-level keyboard change. On bind they reach it through Seat.cpp:350.
- Minimal correction (Chain step 5): "Seat push on keyboard change: K10 with E09 (guard), E06 and E07 (seat protocol), K11, E13, E10 and K12 (per resource). A second route is the wl_keyboard bind, where the `CWLKeyboardResource` constructor calls repeatInfo with the active keyboard's stored values (Hyprland-protocols-core-Seat.cpp:350; no row yet)." Adding a row for line 350 needs a registration errata, because registry rows are append-only.

### A2. OVERREACH: "not both equal to the last sent values" is false before the first send

- Sentence: Scope line 17: "CWLKeyboardResource::repeatInfo sends repeat_info only when the owner is present, the resource version is 4 or later, and the rate and delay are not both equal to the last sent values (K11, E10, K12)."
- Cited line: Seat.cpp:442 (K11), with 444-445 (the only writes to m_lastRate/m_lastDelayMs in the pinned file, grep verified).
- Neighbour that matters: `Seat.hpp:138-139` (upstream at efb50993, not lane-pinned): `uint32_t m_lastRate = 0;` and `uint32_t m_lastDelayMs = 0;`. Before any send, the comparison in line 442 is against 0 and 0, not against any sent value.
- Consequence (source level, [INFERENCE], not exercised): when the active keyboard's stored rate and delay are both 0, the first repeat_info is suppressed on both routes (Seat.cpp:350 and 608), because line 442 returns when both equal the initial 0/0. A stored 0/0 is reachable only if the clamped values can be 0; the table minimum is 0 (K13, K14) and K04/K05 clamp with max(0, x). Whether a client then uses its own default is outside the pins.
- Minimal correction: "...sends repeat_info only when the owner is present, the resource version is 4 or later, and the rate and delay are not both equal to the values of the previous send on that resource (0 and 0 before the first send, from the initialisers in Seat.hpp:138-139, not lane-pinned)."

### A3. HELD: the `sendRepeatInfo` to `repeat_info` mapping is not pinned

- Sentence: Scope line 17 says `repeatInfo` "sends repeat_info". K12 says only that it "calls sendRepeatInfo".
- The mapping of the generated method `sendRepeatInfo` to the `repeat_info` event comes from the wayland-scanner naming convention, plus the pinned 1.26.0 XML at wayland-1.26.0-wayland.xml:2732 (E04). No pin shows the generated code. K12 as written is SUPPORTED; the Scope wording is correct under the naming convention, which the entry should name as an inference. Minimal correction: "...sends repeat_info (through the generated `sendRepeatInfo`; the mapping is by naming convention, not pinned)."

### A4. Narrowing of the enforcement UNKNOWN (not an error; new evidence for the entry's own UNKNOWN)

- Entry line 22: "How the hyprlang config layer enforces the min and max fields for the three keys ... The pins show the table declaration (K13, K14) and not the enforcement code."
- Still true for the pins. Upstream (not lane-pinned, same commit): `CIntValue::value()` in IntValue.cpp returns `*m_val` or `m_default` with no test against `m_min` or `m_max`. The pinned ConfigValues.cpp:54, 68 and 82 use `m_min` and `m_max` only in the descriptions dump. So the range fields are stored and dumped; the class does not check them. The remaining unknown is the hyprlang side (`CConfigValue`). Minimal addition to UNKNOWN: "The CIntValue class stores min and max and does not test them in value() (upstream IntValue.cpp, not lane-pinned); the enforcement question is therefore in the hyprlang value read."

## Verification performed

- `sha256sum -c SHA256SUMS.txt`: all pins OK (receipts.txt).
- `cmp` of pins against upstream raw: Seat.cpp, ConfigValues.cpp, SeatManager.cpp byte-equal.
- Quote-substring check for K11-K15: each quote found exactly once, at the pinned line (python3 -I).
- Neighbour lines read with `read` and `sed -n` (receipts.txt).
- Host: no `hyprctl` or host read was used. K11-K15 are source rows.

## Not verified

- The hyprlang enforcement of min and max (outside the pins and outside the upstream files fetched here).
- The CBoolValue default and parse path (not fetched).
- The generated wayland-scanner `sendRepeatInfo` code (not fetched).
- Runtime behaviour of any value. These audits are source-level only.
- The `m_lastRate` / `m_lastDelayMs` initialisers were read from upstream Seat.hpp, not from a lane pin; the lane has no Seat.hpp pin.

## Lane statement

No lane file was edited. No git or jj mutation was run. No hyprctl keyword or dispatch was run. Scratch under /fast/scratch/hyaku/mado-r55/R55W2AuditD/ was removed. Only this directory (`w2/R55W2AuditD/`) and `w2/R55W2AuditD.md` were written. No mutation test was run; this is a read-only audit. No tools were installed.
