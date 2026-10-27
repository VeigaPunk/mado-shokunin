# Round 54 — registration (frozen before any seat scores)

Base: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`. Frozen 2026-10-27T14:00-03:00 by the
L1 (canonical planner seat) after opening every C2 source itself; committed
before wave 1 dispatch. Rounds 39–48 pattern: predicate + finite fixture
inventory + named controls frozen pre-data; seats build to this contract.

## C1 fixture inventory (errata source-truth verifier)

Entry under test: `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`
(exists at base; committed round 53). Pins (`.ufo/waves/round-52/fetch/`,
hashes from its committed `SHA256SUMS.txt`):

| pin file | recorded sha256 (round-52) |
|---|---|
| `Hyprland-ConfigActions.cpp` | `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637` |
| `Hyprland-ConfigActions.hpp` | `746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073` |
| `Hyprland-KeybindManager.cpp` | `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40` |
| `Hyprland-legacy-DispatcherTranslator.cpp` | `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771` |

Frozen proposition table (the counter extracts the committed entry's P19–P22
rows and checks them against THIS table byte-for-byte modulo trailing spaces;
any drift is a TARGET_MISSED):

| ID | Pin file | Anchor | Quote (verbatim, contiguous) |
|---|---|---|---|
| P19 | `Hyprland-ConfigActions.cpp` | `:1554-1558` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` |
| P20 | `Hyprland-ConfigActions.cpp` | `:1576` | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` |
| P21 | `Hyprland-legacy-DispatcherTranslator.cpp` | `:619-622` | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` |
| P22 | `Hyprland-legacy-DispatcherTranslator.cpp` | `:573-574` | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` |

Anchor side-claims: P19 quote found spanning exactly lines 1554–1558;
P20 at exactly line 1576; P21 at exactly lines 619–622 with `591 ≤ 619` and
`622 ≤ 627`; P22 at exactly lines 573–574 with `573 > 571`.

C1 frozen controls (the counter must reject each; run against mutated
trees — the counter reads all inputs from `--repo`/`--rev` git objects, so a
control = a mutated copy of the scored tree):

| control | mutation | required verdict |
|---|---|---|
| C1-CTL-1 spliced-quote | P19 quote with `if (S.m_passPressed == 1) { if (!isMouse)` removed from the entry table | not contiguous → `quotes≤3/4` MISSED |
| C1-CTL-2 shifted-anchor | P20 anchor `:1576` → `:1575` in the entry | quote not at anchor → MISSED |
| C1-CTL-3 hash-tamper | one recorded sha256 in the tree's SHA256SUMS changed by one hex nibble | `pins≤3/4` MISSED |
| C1-CTL-4 wrong-range | P21 anchor moved to `:573` (outside 591–627) | anchor side-claim fails → MISSED |
| C1-CTL-5 dropped-proposition | entry table without the P22 row | `propositions≤3/4` MISSED |
| C1-CTL-6 swapped-pin | entry's P19 pin cell → `Hyprland-KeybindManager.cpp` | quote absent from that pin → MISSED |

Counter form: `--repo . --rev <rev>` prints the frozen `MADO_ERRATA_TRUTH:` line;
`--selftest` ≥ 30 assertions including one red run per control; `--work <dir>`
honours the scratch rule (no `/tmp` hardcode). Judge of "verbatim": exact byte
contiguity after single-space normalization of interior newlines ONLY where the
frozen quote itself carries a newline (P19/P21/P22 are single logical lines).

## C2 fixture inventory (uwsm-app environment entry)

Pins (`.ufo/waves/round-54/fetch/`, sha256 in its `SHA256SUMS.txt`, fetched
2026-10-27 at tag commit `0727985c9bae655bda488f87f99ea69a6ac1c003` — see
`fetch/README.txt`). Frozen rows to append to `corpus/SOURCES.md`:

| row | source (pinned URL) | located quote (≤25 words) | quote location |
|---|---|---|---|
| S375 | `https://raw.githubusercontent.com/Vladimir-csp/uwsm/0727985c9bae655bda488f87f99ea69a6ac1c003/README.md` | `Difference between environment state before and after preparation is exported into systemd user manager (and D-Bus activation environment if reference D-Bus implementation is used)` | `uwsm-0.27.1-README.md:117-118` |
| S376 | `https://raw.githubusercontent.com/Vladimir-csp/uwsm/0727985c9bae655bda488f87f99ea69a6ac1c003/man/uwsm-app.1.scd` | `uwsm-app client sends arguments to uwsm's app daemon via a pipe.` | `uwsm-0.27.1-uwsm-app.1.scd:60` |
| S377 | `https://raw.githubusercontent.com/Vladimir-csp/uwsm/0727985c9bae655bda488f87f99ea69a6ac1c003/uwsm/main.py` | `unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"` | `uwsm-0.27.1-main.py:3714` |

Row shape (all three): kind `docs`/`code` (S377 `code`), tier A, scope
uwsm-app environment/launch contract, status `mined`, opened `2026-10-27`,
recheck `on-release`, used-by the entry.

Entry: `corpus/knowledge/uwsm-app-environment-r54.md` — provenance trio
(`source:` citing S375–S377, `verified-at: 2026-10-27`, `recheck: on-release`),
the three pinned facts above, and host joins. Frozen host set (entry must cite
≥2 as `file:line`): `~/.local/share/omarchy/default/hypr/autostart.conf:1`,
`:2`, `:3`, `:4`, `:5`, `:6`; `~/.config/hypr/bindings.conf:2`;
`~/.local/share/omarchy/bin/omarchy-toggle-idle:9`.

C2 frozen controls (counter must reject each):

| control | mutation | required verdict |
|---|---|---|
| C2-CTL-1 forged-quote | S376 row quote → `sends arguments via a socket` | quote absent from pin → MISSED |
| C2-CTL-2 unregistered-id | entry `source:` cites S999 | registry leg fails → MISSED |
| C2-CTL-3 missing-trio | entry without a `source:` provenance line | clause (a) fails → MISSED |
| C2-CTL-4 not-indexed | README index row for the entry removed | clause (a) fails → MISSED |
| C2-CTL-5 wrong-commit | a row's URL pinned at `469a39a5…` (v0.26.6) | pin-commit leg fails → MISSED |
| C2-CTL-6 no-host-joins | entry text carries none of the frozen host set | clause (c) fails → MISSED |

Counter form: `--repo . --rev <rev>` prints the frozen `MADO_UWSM_ENTRY:` line;
`--selftest` ≥ 30 assertions incl. one red run per control; `--work <dir>`.

## Wave plan (frozen shape)

Wave 1 `w1`: 37-seat v1 build wave (policy v1, band 32–64): executors build
both counters and receipts to this contract; scribes draft entry/rows/lesson
skeletons to wave dirs; scouts re-verify ground is uncovered and sibling
overlap; connectors design separability checks; reviewers/critics/mutation-testers
attack THIS registration (gameability, do-nothing reachability, freeze
completeness); sentinel holds the safety fence; sonic runs mechanical baseline
receipts. Attack share = reviewer 5 + critic 3 + mutation-tester 2 = 10/37 (27%).

Wave 2 `w2`: 32-seat v1 falsify wave, dispatched only if w1 yields ≥32 distinct
attack items; fresh attackers re-run both counting commands, re-open all three
C2 sources, re-derive every receipt, attack both claims and every landed file.
Residual call ≤8 reviewer/critic seats only if w2 leaves <32 items; counted in
the round total.

Round total: 69 seats (64–128 band). L1 holds the planner seat (validator
rejects planner as a swarm role); no model is passed by any spec (host route
table decides).

## Honesty rules

A claim is judged only on its frozen predicate. If wave 1 falsifies a
predicate, the round re-registers pre-data under `claims-frozen-v2.md` (new
versioned file) or honest-stops; nothing in this file is edited after any seat
has scored. Receipts land under `.ufo/waves/round-54/receipts/`.
