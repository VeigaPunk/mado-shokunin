# ExecSrcFocusGrab — report (w1, round 41)

Status: **complete, no blockers**. Scope: compositor-side facts for C2 (Hyprland's focus-grab implementation).

## Files written (seat-scoped only)

- `.ufo/waves/round-41/w1/ExecSrcFocusGrab/facts.md` — the `fact | quote | file:line | sha256 of file` table
  (72 rows), behaviour summary, and "what the source does NOT say".
- `.ufo/waves/round-41/w1/ExecSrcFocusGrab/verify.py` — verifier: re-hashes each receipt, asserts each quote occurs
  on the named line (whitespace-normalised), asserts <= 25 words, reports Gate-readiness under the C2 counter's own
  `norm()` (tags stripped, whitespace collapsed, 3-25 words), plus structural assertions.
- `.ufo/waves/round-41/w1/ExecSrcFocusGrab/verify.out` — run output: `checked=72 failed=0 gate_ready=48`, exit 0.
- `.ufo/waves/round-41/w1/ExecSrcFocusGrab/refetch.txt` — fresh curl of the three raw URLs, sha256 + `cmp` against
  the staged receipts.
- `.ufo/waves/round-41/w1/ExecSrcFocusGrab.md` — this report.

No tracked file, frozen receipt, counter, control, registry, or lesson was touched. No tool installs; no pacman; no
journal verb; no Wayland/compositor connection.

## Provenance (re-opened, not trusted)

| receipt | sha256 | bytes | refetch |
|---|---|---|---|
| `.ufo/waves/round-41/fetch/focus-grab-v1.xml` (hyprland-protocols `cd1aba6`) | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` | 5447 | `cmp OK` |
| `.ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp` (Hyprland `efb5099`) | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` | 6242 | `cmp OK` |
| `.ufo/waves/round-41/fetch/Hyprland-FocusGrab.hpp` (Hyprland `efb5099`) | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` | 2607 | `cmp OK` |

Raw URLs (as recorded in `refetch.txt`): `raw.githubusercontent.com/hyprwm/hyprland-protocols/cd1aba6bd78775825eb230b3a4274c48b6705eb7/protocols/hyprland-focus-grab-v1.xml`,
`.../hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/FocusGrab.cpp`, `.../FocusGrab.hpp`.
Fresh bytes are byte-identical to the staged receipts (all three `cmp OK`, 2026-10-25T20:08:08-03:00). All three are
>= 512 bytes and distinct, so each is admissible as a C2 `## Gate` receipt (clause d).

## Protocol surface (attacks: C2 "the protocol's interfaces and requests")

- Two interfaces, both version 1, six requests total, one event. Structural proof in `verify.out`:
  `OK xml interfaces=['hyprland_focus_grab_manager_v1', 'hyprland_focus_grab_v1'] versions=['1', '1']`,
  `OK xml requests=['create_grab', 'destroy', 'add_surface', 'remove_surface', 'commit', 'destroy']`,
  `OK xml events=['cleared']`; and `OK xml mentions '<enum' 0x`, `'error' 0x`, `'since=' 0x` — no protocol errors,
  no enums, no version-gated members.
- Purpose: `This protocol allows clients to limit input focus to a specific set` (focus-grab-v1.xml:34,
  sha `0bc60c14…`).
- The grab restricts focus while it exists and has at least one committed surface:
  `This interface restricts input focus to a specified whitelist of` (xml:62) /
  `surfaces as long as the focus grab object exists and has at least` (xml:63) /
  `one comitted surface.` (xml:64 — the source's own typo, quoted verbatim).
- Manager requests: `Create a surface grab object.` (xml:46); its `destroy` is
  `This doesn't destroy existing focus grab objects.` (xml:55), matching the implementation, where manager teardown
  only erases from `m_managers` (`std::erase_if(m_managers, …)` cpp:158, sha `53b762f7…`).

## Request semantics

- `add_surface`: `Add a surface to the whitelist. Destroying the surface is treated the` (xml:81) /
  `same as an explicit call to remove_surface and duplicate additions are` (xml:82) — duplicates ignored; and
  `Does not take effect until commit is called.` (xml:85). Implementation: duplicate add is a no-op via
  `if (iter == m_surfaces.end())` (cpp:75) and a new entry is created with
  `m_surfaces.emplace(surface, makeUnique<CFocusGrabSurfaceState>(this, surface));` (cpp:76).
- `remove_surface`: `the same as an explicit call to this function.` (xml:94), deferred
  (`Does not take effect until commit is called.`, xml:99), and
  `keyboard, another surface will be entered on commit.` (xml:97). Implementation splits by state:
  `if (iter->second->m_state == CFocusGrabSurfaceState::PendingAddition)` (cpp:82) erases immediately, otherwise
  `iter->second->m_state = CFocusGrabSurfaceState::PendingRemoval;` (cpp:85) defers to the next commit.
- Surface destruction routes through `commit(true);` (cpp:91) from `eraseSurface`, i.e. remove-only.
- `commit`: `Commit pending changes to the surface whitelist.` (xml:107);
  `If the list previously had no entries and now has at least one, the grab` (xml:109) /
  `will start. If it previously had entries and now has none, the grab will` (xml:110) / `become inert.` (xml:111).
  Implementation: commit applies removals (`m_grab->remove(iter->first.lock());`, cpp:119) and promotions
  (`m_grab->add(iter->first.lock());`, cpp:126), then
  `if (surfacesChanged) {` (cpp:137) → `start();` (cpp:139) if any surface is committed, else `finish(true);`
  (cpp:141).
- `destroy`: `Destroy the grab object and remove the grab if active.` (xml:117); implementation erases from
  `m_grabs` (`std::erase_if(m_grabs, …)`, cpp:162) and the destructor calls `finish(false);` (cpp:32) — no
  `cleared` on explicit destroy.

## Whitelist storage

- `std::unordered_map<WP<CWLSurfaceResource>, UP<CFocusGrabSurfaceState>> m_surfaces;` (Hyprland-FocusGrab.hpp:51,
  sha `dce47251…`), per-surface state machine `} m_state = PendingAddition;` (hpp:24) over
  `PendingAddition` / `PendingRemoval` / `Committed` (hpp:21-23). The seat grab keeps its own parallel list, changed
  only from commit (cpp:119, :126). Grab objects live in `std::vector<UP<CFocusGrab>> m_grabs;` (hpp:71), so several
  may exist; each owns exactly one `SP<CSeatGrab> m_grab;` (hpp:52).

## Empty-whitelist commit

- The "changed and nothing committed" path is `finish(true);` (cpp:141), and `finish` is guarded by
  `if (m_grabActive) {` (cpp:59). Consequence: an empty commit on a grab that never started emits nothing; an empty
  commit on an active grab clears the seat grab (`m_grab->clear();` cpp:65), drops the map
  (`m_surfaces.clear();` cpp:66) and sends `cleared` (`m_resource->sendCleared();` cpp:69). The XML does not state
  the never-started case — this is the code's answer, not the spec's.

## `cleared` — when and why

- Spec: `Sent when an active grab is cancelled by the compositor,` (xml:123) / `regardless of cause.` (xml:124), and
  the criteria are `Upon meeting implementation-defined criteria usually meaning a mouse or` (xml:72) /
  `touch input outside of any whitelisted surfaces, the compositor will` (xml:73) /
  `clear the whitelist, rendering the grab inert and sending the cleared` (xml:74).
- Implementation sends it from exactly three call sites, all `finish(true)`: the seat-grab callback
  `m_grab->setCallback([this]() { finish(true); });` (cpp:22), the empty-whitelist commit (cpp:141), and the
  surface-destroy commit when nothing committed remains (cpp:91 → :141). Explicit `destroy` uses `finish(false)`
  (cpp:32). [INFERENCE: the callback fires when the compositor ends/replaces the seat grab; the trigger lives in
  `CSeatGrab`, not in this receipt.]

## Input redirected, and focus outside the whitelist

- Redirected input is keyboard and pointer only: `m_grab->m_keyboard = true;` (cpp:20) and
  `m_grab->m_pointer  = true;` (cpp:21). Neither file contains the token `touch`
  (`OK Hyprland-FocusGrab.cpp mentions 'touch' 0x`, `…hpp… 0x` in `verify.out`), although the spec says
  `Mouse and touch events inside a whitelisted surface will be passed` (xml:66) /
  `to the surface normally, while events outside of a whitelisted surface` (xml:67) /
  `will clear the grab object. Keyboard events will be passed to the client` (xml:68).
- Focus of surfaces outside the whitelist: this file never unfocuses anything and never restores previous focus on
  clear. It moves keyboard focus into the whitelist with
  `Desktop::focusState()->rawSurfaceFocus(surface);` (cpp:108), after keeping it if it is already inside
  (`if (keyboardSurface && isSurfaceCommitted(keyboardSurface.lock()))`, cpp:96); with no committed surface it logs
  `LOGM(Log::ERR, "CFocusGrab::refocusKeyboard called with no committed surfaces. This should never happen.");`
  (cpp:110). Start also re-runs pointer motion (`g_pInputManager->simulateMouseMovement();`, cpp:54) and refocuses
  (`refocusKeyboard();`, cpp:55).

## Interaction with other grabs

- One seat grab at a time: `g_pSeatManager->setGrab(m_grab);` (cpp:50), installed once per active edge
  (`if (!m_grabActive) {`, cpp:48). The spec's `event. The same will happen if another focus grab or similar action`
  (xml:75) / `is started at the compositor's discretion.` (xml:76) is realised by the callback path (cpp:22) and by
  a careful teardown: `if (g_pSeatManager->m_seatGrab == m_grab)` (cpp:62) — a successor grab is not uninstalled by
  the predecessor's finish.

## Gate-ready quotes (3–25 words, present in the counter's `norm()` text)

Distinct, one per receipt, ready for `## Gate` lines (clause d/g); the full 48-item list is in `verify.out`:

- `focus-grab-v1.xml` (sha `0bc60c14…`): `This interface restricts input focus to a specified whitelist of` (xml:62, 10 words).
- `Hyprland-FocusGrab.cpp` (sha `53b762f7…`): `m_grab->setCallback([this]() { finish(true); });` (cpp:22, 4 words).
- `Hyprland-FocusGrab.hpp` (sha `dce47251…`): `std::unordered_map<WP<CWLSurfaceResource>, UP<CFocusGrabSurfaceState>> m_surfaces;` (hpp:51, 3 words).
- Alternative for the XML if a different id needs a distinct quote: `clear the whitelist, rendering the grab inert and sending the cleared` (xml:74, 11 words).
- Tag-bearing lines (`<interface …>`, `<request name="commit">`) are **not** Gate-ready: `norm()` strips tags, and
  `verify.out` marks them `gate=no`.

## What the source does NOT say (full list in facts.md)

1. Touch: no `touch` token in either implementation file, so nothing here says touch is redirected or clears the grab.
2. Where outside-click detection lives — `CSeatGrab` / input manager, not in these receipts.
3. What happens to focus of non-whitelisted surfaces, and no restore-previous-focus on clear.
4. The never-started empty-commit case (only the `m_grabActive` guard answers it).
5. Whether a no-op commit is observable (the code makes it silent, cpp:137).
6. Precedence between multiple simultaneous grabs — vector exists (hpp:71), ordering undefined.
7. The rule-level counterpart: no mention of rules, dispatchers, `hyprctl`, or config in either file.
8. Advertisement/host state: no registry, no client list, no portal (that is `xdph-journal.txt`, another seat).
9. Client obligations after `cleared`, and whether a grab can be re-armed on the same object.
10. Protocol errors for foreign surfaces or post-`cleared` commits (the XML defines no `error` at all).
11. Any `cleared` nuance when the destroyed surface was the only committed one beyond the generic commit path.

## Evidence

- `python3 -I verify.py` → exit 0, `checked=72 failed=0 gate_ready=48`; 3 receipt-hash lines plus 8 structural `OK`
  lines (interface list, request list, event list, two `touch` counts, three absence checks) precede the 72 row
  verdicts.
- `refetch.txt` → fresh sha256 identical to staged for all three; three `cmp OK`.
- Quotes: every one is a verbatim fragment of the named line, printed with its line number by `verify.py`
  (`verify.out`), and every one is <= 25 words.

## Risks / limits (honest)

- The three receipts are one commit each; they say nothing about other Hyprland versions or other compositors.
- The seat-grab mechanics (what makes the callback fire, whether touch is redirected by `CSeatGrab`) are outside
  these files and are marked `[INFERENCE]` where used.
- `facts.md` quotes are line-bounded fragments, so a few read as sentence halves; the location and hash are exact.
- No host-side claim is made here: no journal read, no compositor query, no `hyprctl` beyond the frozen facts.

Report: .ufo/waves/round-41/w1/ExecSrcFocusGrab.md
