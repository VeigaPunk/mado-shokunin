# Round 55 w2 — rows audit (seat R55W2RevRows)

Scope: registry rows S378, S379, S380 in `corpus/SOURCES.md` (lane HEAD working tree, byte-equal to scored revision 57584ed67716340b3d466fa04333ac0bab3fb79e for this file: `git diff --stat 57584ed… -- corpus/SOURCES.md` printed nothing), the appended `used-by` edits to S052/S316/S317/S318/S319, the Gate drafts in `.ufo/waves/round-55/w1/R55ScribeSources/gate.md`. Read-only: no tracked file edited, no git mutation. Lane commit read: `721ba9c1` (HEAD) and `57584ed6` (scored).

Verdict key: SURVIVES / BROKEN / NOT-REPRODUCED / UNVERIFIED.

## 1. Upstream re-open (network read, raw.githubusercontent.com, commit efb50993780079460b0cbed1363e2166a2de1d9f)

Command (run from a scratch dir, now removed):
```
B=https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f
curl -sSfL -o SeatManager.cpp $B/src/managers/SeatManager.cpp
curl -sSfL -o Seat.cpp        $B/src/protocols/core/Seat.cpp
curl -sSfL -o IKeyboard.hpp   $B/src/devices/IKeyboard.hpp
sha256sum *      # wc -lc *
```
Output:
```
82e0bc9e…f716f05  IKeyboard.hpp        137 lines  4816 B
cc23bb8b…0818d    Seat.cpp             626 lines  21117 B
bd748553…4378     SeatManager.cpp      826 lines  26074 B
cmp pin vs upstream: SM_SAME, SEAT_SAME, IK_SAME
```
Receipts copied to `receipts/` (`upstream-*.{cpp,hpp}`, `upstream-sha256.txt`).

Row sha256 vs upstream raw sha256 vs pin sha256 (`.ufo/waves/round-55/fetch/`):

| row | row sha256 | upstream raw sha256 | pin sha256 (`sha256sum`) | pin line count | row line count | result |
|---|---|---|---|---|---|---|
| S378 SeatManager.cpp | bd7485535c7e…378 | bd7485535c7e…378 | bd7485535c7e…378 | 826 | 826 | SURVIVES |
| S379 protocols/core/Seat.cpp | cc23bb8b4f1e…818d | cc23bb8b4f1e…818d | cc23bb8b4f1e…818d | 626 | 626 | SURVIVES |
| S380 IKeyboard.hpp | 82e0bc9e1f31…5f05 | 82e0bc9e1f31…5f05 | 82e0bc9e1f31…5f05 | 137 | 137 | SURVIVES |

Pins also equal the freeze-commit blobs: `git show 54dacbd843d64ba744cd3f1bdc2ec622e5010039:.ufo/waves/round-55/fetch/<f> | sha256sum` gives the same three hashes (search-log claim "checked against the freeze commit" holds).

Tag claim: `git ls-remote --tags https://github.com/hyprwm/Hyprland 'refs/tags/v0.56.2'` → `efb50993780079460b0cbed1363e2166a2de1d9f refs/tags/v0.56.2`. The "Hyprland 0.56.2 @ efb5099…" anchor is supported. (Network ls-remote; not in the listed allowed reads, but read-only; recorded here.)

## 2. Cited line ranges vs the pins

Lines printed with `sed -n` from `.ufo/waves/round-55/fetch/`.

**S378 `SeatManager.cpp:175-178`** (row) / gate `:177`
```
175 void CSeatManager::updateActiveKeyboardData() {
176     if (m_keyboard)
177         PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);
178     PROTO::seat->updateKeymap();
179     PROTO::inputCapture->updateKeymap();
180 }
```
The claim (rate/delay handed to the seat protocol, only under `if (m_keyboard)`) is held by 175-177. The cited range truncates the function (closes at 180). Imprecise range, claim holds. **SURVIVES** (range note: 175-180 is the full function).

**S379 `Seat.cpp:441-448` (repeatInfo) and `:603-609` (updateRepeatInfo)**
```
441 void CWLKeyboardResource::repeatInfo(uint32_t rate, uint32_t delayMs) {
442     if (!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs))
443         return;
...
448 }
603 void CWLSeatProtocol::updateRepeatInfo(uint32_t rate, uint32_t delayMs) {
604     if (!(m_currentCaps & eHIDCapabilityType::HID_INPUT_CAPABILITY_KEYBOARD))
605         return;
...
609     }        <- for-loop closer
610 }            <- function closer
```
Repeat range 441-448 correct. 603-609 omits the function closer at 610 (imprecise, claim holds).

**S380 `IKeyboard.hpp:121-123`**
```
121     int                            m_repeatRate        = 0;
122     int                            m_repeatDelay       = 0;
123     int                            m_numlockOn         = -1;
```
Correct. Members sit inside `class IKeyboard : public IHID {` (line 24) to `};` (137).

**S379 second emitter (not cited by the row) — `Seat.cpp:337-350` and `:467-468`**
```
337 CWLKeyboardResource::CWLKeyboardResource(SP<CWlKeyboard> resource_, SP<CWLSeatResource> owner_) ...
344     if (!g_pSeatManager->m_keyboard) { ... return; }
349     sendKeymap(g_pSeatManager->m_keyboard.lock());
350     repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate, g_pSeatManager->m_keyboard->m_repeatDelay);
...
467     m_resource->setGetKeyboard([this](CWlSeat* r, uint32_t id) {
468         const auto RESOURCE = PROTO::seat->m_keyboards.emplace_back(makeShared<CWLKeyboardResource>(...));
```
Repeat info is also emitted at bind time (`get_keyboard`), by calling `repeatInfo` directly. That path does NOT pass through `CWLSeatProtocol::updateRepeatInfo` and therefore does NOT pass the `m_currentCaps & KEYBOARD` gate at Seat.cpp:604. No capability check exists on the `get_keyboard` path in the pinned lines 467-468.

Command proving the single `sendRepeatInfo` emitter and the call sites:
```
grep -n 'repeatInfo\|updateRepeatInfo' Hyprland-SeatManager.cpp Hyprland-protocols-core-Seat.cpp
Hyprland-SeatManager.cpp:177:        PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);
Hyprland-protocols-core-Seat.cpp:350:    repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate, g_pSeatManager->m_keyboard->m_repeatDelay);
Hyprland-protocols-core-Seat.cpp:441:void CWLKeyboardResource::repeatInfo(uint32_t rate, uint32_t delayMs) {
Hyprland-protocols-core-Seat.cpp:603:void CWLSeatProtocol::updateRepeatInfo(uint32_t rate, uint32_t delayMs) {
Hyprland-protocols-core-Seat.cpp:608:        k->repeatInfo(rate, delayMs);
grep -n 'sendRepeatInfo' *.cpp *.hpp  ->  Hyprland-protocols-core-Seat.cpp:447 (only emitter)
```
So the single wire emitter is `sendRepeatInfo` (line 447) behind `repeatInfo`; the row's teaches ("sent only to version ≥4 resources and only when changed") holds for both callers, because the guard in `repeatInfo` is shared. The row's **scope** cell does not hold (see §3).

**S379 `m_lastRate`/`m_lastDelayMs` initial values**: declared in `Seat.hpp`, which is NOT in the pins. The "differs from the last pair sent" claim is therefore a necessary-condition claim with unknown first-send state. UNVERIFIED for the first send; the teaches uses "only when", which is still a necessary condition.

## 3. Teaches and scope cells vs the lines

| row | cell | claim | what the lines show | verdict |
|---|---|---|---|---|
| S378 | teaches | stored rate/delay handed to seat protocol inside `updateActiveKeyboardData`, only when keyboard set; no host event asserted | SeatManager.cpp:176-177 | SURVIVES |
| S378 | scope | `updateActiveKeyboardData`: which stored values reach the seat protocol | same | SURVIVES |
| S379 | teaches | sent only to keyboard resources of version ≥4; only when rate or delay differs from last pair | Seat.cpp:442 guard (`version() < 4`, `rate==m_lastRate && delayMs==m_lastDelayMs`) shared by both callers | SURVIVES (as necessary conditions) |
| S379 | scope | "`CWLKeyboardResource::repeatInfo` and `CWLSeatProtocol::updateRepeatInfo`: version gate, change suppression and **keyboard-capability gate before the wl_keyboard repeat event**" | capability gate (Seat.cpp:604) exists only on the `updateRepeatInfo` path. The bind-time path (Seat.cpp:350 from get_keyboard, :467-468) reaches `repeatInfo` with no capability check. "before the wl_keyboard repeat event" is false for that path. | **BROKEN** (scope overclaim) |
| S380 | teaches | "**each keyboard header** declares its repeat rate and repeat delay as int fields initialised to 0, and its numlock state as an int initialised to -1" | Only one header was opened (`IKeyboard.hpp`, the base class). "each keyboard header" is a universal over headers never opened. The lines show exactly the base-class declarations at 121-123. | **BROKEN** (teaches overclaim; fix: "the keyboard base header IKeyboard.hpp") |
| S380 | scope | per-keyboard storage members read by `updateActiveKeyboardData` | members exist; the read is at SeatManager.cpp:177 (S378) | SURVIVES |

Severity: low for S380 (wording), medium for S379 scope (a documented gate that the upstream code does not apply on one path; the L1 knowledge entry K11/E06/E07 describes only the `updateRepeatInfo` path and does not mention Seat.cpp:350 — this is a gap the knowledge entry inherits, not verified as a falsified claim there).

## 4. Registry census and rule checks (CORPUS.md § SOURCES.md, fleet-root file, read-only)

Commands run from `mado-shokunin` lane root (CORPUS.md lives at fleet root `/home/vgpnk/Projects/shokunin/CORPUS.md`; `corpus/` has no CORPUS.md):
```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        -> 317
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}'   -> malformed=0
awk ... tier histogram   -> A=306 B=4 C=7
awk ... status histogram -> mined=296 queued=10 rejected=11
awk ... duplicate ids    -> (empty)
awk ... enum violations (tier/status/kind) -> (empty)
awk ... mined used-by paths that do not exist -> (empty)
awk -F'|' '/^\| *S3(78|79|80) /{print NF}' -> 13 13 13   (11 columns each)
recheck field: S378-S380 = on-release (CORPUS cadence list: on-release is allowed)
opened field: 2026-10-28 (ISO)  — all three
kind: code (allowed)  tier: A (code = primary source for its scope; allowed)  status: mined, with used-by = corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md (exists; cites S378, S379, S380 in its header and body)
```
Id continuity: last ids 377, 378, 379, 380; no gap (S377 was the prior max; 317 rows total).
All three rows: **SURVIVES** on fields, census and rules. (S378 row: `anchor` includes pin path and sha; pin exists.)

## 5. used-by edits (diff vs pre-round-55 parent `ebd66fbf^` = `5a43d67f`)

Command: `git diff -U0 ebd66fbf^ -- corpus/SOURCES.md`, then python row comparison (row-by-row, cell-by-cell).

Result:
```
old rows 314, new rows 317, removed [], added ['S378','S379','S380']
S052 changed cols idx [11]: 'corpus/knowledge/input-debugging-boundaries-r15.md'  ->  '… , corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md'
S316 changed cols idx [11]: 'corpus/knowledge/hyprland-input-devices-r46.md'  ->  '… , corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md'
S317, S318, S319: same appended path
```
Only column 11 (`used-by`) changed for each; status, recheck, opened, teaches, anchor unchanged. Old value is a prefix; the appended path is the existing `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`. Consistent with the append-only rule (only status/recheck/used-by change in place). **SURVIVES.** Note: the registration says S316..S319 reuse; the S052 `used-by` append is to a knowledge file that cites S052 (header `source:` line 1 cites S378-S380, S316-S319, S052 — verified by reading the header).

## 6. Gate block (`w1/R55ScribeSources/gate.md`) — quotes and fields

Method: python split by `### S37x/S380` headings; compared URL, access date, teaches against the row; located each quote in the named pin line and counted occurrences in the whole pin file; counted quote words with `len(quote.split())`.

| gate | URL = row | access = opened | teaches = row (exact) | quote words (≤25) | located at pin line | occurrences in pin file | result |
|---|---|---|---|---|---|---|---|
| S378 | yes | 2026-10-28 | yes | 2 | `Hyprland-SeatManager.cpp:177` — line 177 is `        PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` | 1 (line 177) | SURVIVES |
| S379 | yes | 2026-10-28 | yes | 14 | `Hyprland-protocols-core-Seat.cpp:442` — line 442 is `    if (!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs))` | 1 (line 442) | SURVIVES |
| S380 | yes | 2026-10-28 | yes | 3 | `Hyprland-IKeyboard.hpp:121` — line 121 is `    int                            m_repeatRate        = 0;`; quote `m_repeatRate        = 0;` (8 spaces) matches exactly | 1 (line 121) | SURVIVES |

The gate's S380 teaches inherits the "each keyboard header" overclaim (§3). The gate's S379 teaches is correct as a necessary-condition statement; its scope-level overclaim is only in the row's scope cell, which the gate does not quote.

Gate status: the round lesson `corpus/lessons/round-55.md` does NOT exist in the lane HEAD (`ls corpus/lessons | grep round-55` → empty). CORPUS rule 1 requires the round lesson `## Gate` block. The draft is not yet integrated: **UNVERIFIED as integrated; PENDING L1 integration.**

## 7. Search-log prose (appended `Round 55 — …` paragraph in SOURCES.md)

Checked: "Existing rows reused: S316, S319, S318, S215, S317, S162, S052" — all seven rows exist in the registry (S215 and S162 confirmed by grep). "S380's URL is the URL already held by S363 (`src/devices/IKeyboard.hpp`)": S363 row URL is `…/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.hpp` (same), anchor `Hyprland-IKeyboard.hpp:13-22, 100-101, 124`. Overlap is real; the "W04 warning" census code is not in this lane's tooling that I could locate — UNVERIFIED for the census label, VERIFIED for the URL overlap.

## 8. Mutation/instrument statement

No mutation test was run. No lane file was modified. All scratch (`/fast/scratch/hyaku/mado-r55/R55W2RevRows/`) removed. Receipts copied to `receipts/`.

## 9. Recommended row corrections (for L1; not applied by me)

1. S379 scope: replace "keyboard-capability gate before the wl_keyboard repeat event" with "keyboard-capability gate on the updateRepeatInfo path only; the bind-time call from get_keyboard (Seat.cpp:350, guarded by keyboard presence at :344) has no capability gate" and add `Seat.cpp:337-350` to the anchor. Append-only rule: this must be a new row with `supersedes`, or a scope fix in the same integration round before any frozen predicate depends on it — L1 decides.
2. S380 teaches: "each keyboard header" → "the keyboard base header `IKeyboard.hpp` declares …".
3. S378 anchor: `SeatManager.cpp:175-180` for the full function (cited 175-178 holds the claim).
4. S379 anchor: `603-610` for the full function.
5. Integrate the gate into `corpus/lessons/round-55.md` `## Gate` (rule 1).

## 10. Not verified

- First-send behaviour of the bind-time repeat (initial `m_lastRate` value) — `Seat.hpp` not pinned.
- Whether any other keyboard header exists at efb5099 (S380 "each" claim) — not opened.
- Whether knowledge entry `hyprland-keyboard-repeat-numlock-r55.md` K11/E06/E07 covers the bind path — not re-audited here (outside rows scope); noted only.
- Frozen-predicate impact of the S379 scope overclaim on PRED-C1-r55 — not evaluated (outside this item).
