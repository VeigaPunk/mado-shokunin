# C2SourceRecon Report — mado round 52 (w1)

- Seat: `C2SourceRecon`
- Role: UFO-FSD scout / dispatcher-source recon (leaf; no subagent dispatch)
- Assignment: recon locally available pinned source on distinct dispatcher behavior beyond round 51; identify ≥4 propositions with exact source files/anchors and fresh URLs to open; source-only, no runtime. Verify PROVINCE boundary and held overlap.
- Status: complete

Reads-first order honored: `.ufo/waves/round-52/claims-frozen.md`, `.ufo/waves/round-52/registration.md`, then `PROVINCE.md`, `SKILL.md`, the round-51 entry, the held r25/r26/r50 entries, the round-51 fetch manifest, and the pinned bytes themselves. No claim or predicate edits. No tracked lane files touched; the only write is this report.

## Method

1. Established what round 51 already owns by reading `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` in full (its steps 1–9, held list, limits) and cross-checking the older held entries (`bind-table-r25.md`, `keybind-rule-semantics.md`, `dispatcher-semantics-r25.md`, `dispatcher-surface-and-request-grammar-r26.md`, `hyprland-bind-key-match-r50.md`).
2. Cross-checked against the live reject/overlap map in `.ufo/waves/round-52/w1/C2CoverageCritic.md` (R1–R7, D1–D4, A1–A6).
3. Grepped and range-read the locally pinned bytes under `.ufo/waves/round-51/fetch/` (Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f`; blobs `blob_verified: true` per `fetch-manifest.json`) for mechanisms not owned by any held entry.
4. Spot-verified the sibling draft `.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv` (20 anchors sampled across P01–P18) against the pinned bytes.
5. No fetches, no runtime, no package queries, no live reads, no installs, no git/jj mutation. Source checkout read-only throughout. Scratch `/fast/scratch/hyaku/mado-r52/C2SourceRecon/` was not needed (read-only recon); nothing created anywhere else.

## PROVINCE boundary verification — PASS

- Dispatcher/keybind source-read knowledge is inside the lane's province: `PROVINCE.md` round-38 addendum names the request-socket knowledge ground (including `hyprctl-flags-r28.md`) as "documentation/source-read knowledge … read-only byte work: no socket is ever connected"; the round-36 channel rule keeps English upstream code/documentation channels admissible for dispatcher-plane claims while localized documentation channels stay out. A dispatcher source entry under `corpus/knowledge/` is lane paperwork of exactly the kind every prior round's C2 entry has been (r45/r46/r51 refinements name such entries and their counters as lane record instruments).
- Refusal boundary respected: no compositor socket, no `hyprctl`, no process/compositor probe, no input capture, no screenshot, no package transaction, no host/config mutation. All evidence is file bytes under the lane repo and previously pinned fetch bytes.
- Widening flag: Subject 3 below (`exec` spawn chain) leans toward the process plane, which the province table assigns to tsukuroi; per PROVINCE "out of province → report, never absorb" it is reported as the critic's weakest candidate (D4, HIGH widening risk), not absorbed.

## Held-overlap verification — map and verdict

Held subjects (each verified against the cited entry this round):

| Mechanism | Owner | My check |
|---|---|---|
| Socket verb / request grammar, flag strip, `;` batch, Lua eval wrapper | `dispatcher-surface-and-request-grammar-r26.md` §A2 (S018 r39); r51 s8–9 | R1 — do not touch |
| `submap`/`pass`/`global`/`mouse`/`sendkeystate` semantics | r51 s4–6 (S367, S364) | R2 — do not touch; see P16 dissent below |
| Table population, name resolution, `Bad dispatcher` | r51 s1 | R3 |
| Parse-time validation of the dispatcher word; bind flag letters incl. `p`→dontInhibit, `l`, `r`, `c`/`g`; mutual exclusions | r51 s2; `bind-table-r25.md:31–50` (S162); `legacy-ConfigManager.cpp:1496–1552` confirmed on pinned bytes | R4 — parse-time only; the *runtime* effect of `dontInhibit` is unowned (see Subject 2) |
| `hl.dsp.*` documented Lua surface | r25/r26 | R5 |
| Argument-grammar generalization over the five read dispatchers | r51 s7 | R6 |
| Dispatcher inventory with live counts | `keybind-rule-semantics.md` §3 | R7 |
| Key match chain `KeybindManager.cpp:652–726`, multi-key match state, release-eligibility branches `:728/:747`, `modmaskAtPressTime` | `hyprland-bind-key-match-r50.md` (its step 17 cites `:728/:747` directly) | held — Subject 2 cites only `:643–651` (before the held chain) and `:842–851` (after the dispatch loop), never the held regions |

Registry tail (from the critic's exercised command): 306 rows, highest S369; the entry must add S370+ opened this round.

Verdict: a distinct subject exists without widening. Two are viable from locally pinned bytes plus small fresh opens; one sibling draft already occupies the strongest D1 surface.

## Candidate subject 1 (sibling-taken): `sendshortcut`/`sendkeystate` synthetic-event manufacture — C2EntryDraft

Status: drafted at `.ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md` + `proposition-map.tsv` (18 propositions P01–P18, proposed rows S370–S373, distinct-scope reopen wording present). My recon verdict on the draft:

- **Anchors verify.** Sampled 20 anchors across P01–P18 against the pinned bytes — all exact. Examples: `CVarList2 ARGS(args, 4);` (`legacy-DispatcherTranslator.cpp:592`), state alphabet `:597–604`, tail rebuild `:607`, save/repeat/restore `:612/:619–622/:624`, numeric/`code:`/`mouse:` branches `:540–547`, cache key `:557`, keysym scan `:565–566`, `key not found` `:574`, selector ternary `:582–586`, `sendKeyboardKey(S.m_timeLastMs, key - 8, …)` (`ConfigActions.cpp:1558`), `if (!window) return {};` `:1578–1579`, `Actions::sendKeyState` `:1601`, state fields `ConfigActions.hpp:114–117`.
- **Distinctness.** D1-shaped: r51 read only the argument *split* of these two (`:532–535`) and one `sendkeystate` parenthetical; the synthesis mechanics (state alphabet, repeat double-press, branch order, per-keyboard cache, stale timestamp + key−8, mods assert/clear, `Actions::sendKeyState` twin) are unowned. P01–P14, P17, P18 are unanswerable from held entries.
- **Dissent recorded (honest call, as requested by the draft seat):** P16 ("a second implementation exists as the action `Actions::sendKeyState`") is the exact fact of r51 step 6's parenthetical (`ConfigActions.cpp:1603–1615` cited there) — it sits inside critic reject item R2 and should be demoted to a held-cite or reframed as contrast. P15 (translator-side save/restore `:612/:624`) is adjacent-but-new (r51 cited the action side, not the dispatcher side) — keep with distinctness wording. P07's mechanism (uppercase + `contains`) partially restates held `bind-table-r25.md` S162 ground on `stringToModMask`; only the sendshortcut-path consequence (unknown words silently contribute no error and no bits, because `:223–225` has no else branch) is new — sharpen the wording to that consequence.
- **Provenance defect to fix (critic A2):** proposition-map anchors point into `.ufo/waves/round-51/fetch/` paths. The wave must re-open the four URLs this round (fetch into `round-52/fetch/`; expected bytes are pinned in `round-51/fetch/fetch-manifest.json` — `DispatcherTranslator.cpp` 35997 B sha256 `7248cbb8…`, `ConfigActions.cpp` 71407 B `a83abeb5…`, `ConfigActions.hpp` 6960 B `746c6f51…`, `KeybindManager.cpp` 39334 B `8d8f35fc…` — equality receipts are cheap), or word explicit criterion-17 distinct-scope reopens.
- **Row-anchor refinement:** S373's `m_keyToCodeCache` is declared in `KeybindManager.hpp:149` and filled from the translator (`:559–576`), not in `KeybindManager.cpp` — word the row over `KeybindManager.cpp:221` (`stringToModMask`) and cite the member via the hpp.
- **Resolution (same round):** the draft seat adopted all four points — P16 demoted to a held-cite from r51 step 6 (map now 17 props), P07 sharpened to the sendshortcut-path consequence with the S162 held line, the four URLs re-fetched this round into the seat's `fetch/` dir with 4/4 sha256-equal receipts to the round-51 pins (`fetch/verify.txt`), and S373 re-scoped to `stringToModMask` + the hpp-declared cache member. No dissent remains on Subject 1 from this seat.

## Candidate subject 2 (recommended fallback, fresh URLs): the shortcuts-inhibit execution gate

Mechanism: while any Wayland client holds a shortcuts inhibitor, bind dispatch is gated at two checkpoints in `handleKeybinds`, behind one config value and one per-bind field. Not on R1–R7; r50's held chain starts at `:652` (this subject cites only `:643–651` and `:842–851`); r51 step 4 name-dropped `:845–851` in one clause without tracing the gate — a criterion-17 distinct-scope reopen of `KeybindManager.cpp` completes it. The pinned wiki pages contain no occurrence of `disable_keybind_grabbing` or `shortcutsInhibit` (grep exercised, zero hits) — a documentation gap, useful only in Limits.

Propositions (quotes ≤25 words, all verified on pinned bytes this round):

- **P-A1 — one protocol global, two checkpoints, different effects.** Pre-dispatch, per-bind, during hit collection: `if (!k->dontInhibit && !*PDISABLEINHIBIT && PROTO::shortcutsInhibit->isInhibited()) continue;` (`Hyprland-KeybindManager.cpp:643`). Post-dispatch, whole-call: `res.error = "Keybind handling is disabled due to an inhibitor";` (`:849`, inside the `!found` branch `:844–851`).
- **P-A2 — both checkpoints share two independent bypasses.** The integer config `binds:disable_keybind_grabbing`: `static auto PDISABLEINHIBIT = CConfigValue<Config::INTEGER>("binds:disable_keybind_grabbing");` (`:603`); and the per-bind field: `bool dontInhibit = false;` (`Hyprland-KeybindManager.hpp:56`), set by flag `p` at parse time (held, `legacy-ConfigManager.cpp:1529`).
- **P-A3 — an inhibited unmatched key is still forwarded to the client.** `res.passEvent |= !found;` (`:842`) runs before the failure injection, so the call both passes the event and reports `success = false` with the inhibitor error (`:846–849`) — the compositor-side contract for "the game receives the key, the compositor bind does not fire".
- **P-A4 — the inhibit check runs before every other gate in the loop.** Order on pinned bytes: inhibit `:643` → `enabled` `:646` → session-lock `:649` → modmask/submap/shadowed `:652` (the held r50 chain starts here) → device `:654–662` → matching `:663–726`. Inhibition therefore prunes candidates first.
- **P-A5 — the gate reads the Wayland shortcuts-inhibit protocol state.** `#include "../protocols/ShortcutsInhibit.hpp"` (`Hyprland-KeybindManager.cpp:9`); `PROTO::shortcutsInhibit->isInhibited()` is the only predicate. What `isInhibited()` tracks (a client-held `zwp_shortcuts_inhibitor`) needs the protocol file — **fresh URL** (below). [INF] until opened.
- **P-A6 — two "inhibitor" words, two distinct checks.** `if (!k->locked && g_pSessionLockManager->isSessionLocked()) continue;` (`:649`) is a separate gate keyed on the bind's `l` flag; the held docs row for `l` (`keybind-rule-semantics.md:117`, "fires even while an input inhibitor (lockscreen) is active") names the session-lock gate, not the shortcuts-inhibit gate. An entry here disambiguates them — held entries never have.

Fresh URLs to open (both unpinned in every wave; manifest pattern `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>`):

- `src/protocols/ShortcutsInhibit.hpp` — the `isInhibited()` declaration and inhibitor set/reset (P-A5).
- `src/protocols/ShortcutsInhibit.cpp` — what client action sets the inhibited state (P-A5).

Coverage value: mechanism is host-relevant to the lane's own input-inhibit/session-lock globals classes, and it is execution (when a matched bind does *not* dispatch), squarely the frozen theme. Risk: r51's one-clause mention of `:845–851` — the entry must cite r51 for that line and claim only the untraced remainder (A5-style saturation-by-sequel avoided: P-A1's first-check fact, P-A2, P-A3, P-A4, P-A5, P-A6 are each unanswerable from held entries).

## Candidate subject 3 (weakest, report-only): `exec`/`execr` downstream spawn

Anchors (pinned `legacy-DispatcherTranslator.cpp`): dependency pinned at `#include "../supplementary/executor/Executor.hpp"` (`:4`); `exec` calls `Config::Supplementary::executor()->spawn(args)` (`:66`) and maps a nullopt to `Failed to start process. No closing bracket in exec rule.` (`:67–68`); success is a pid compared `> 0` (`:69`); `execr` calls `spawnRaw` (`:73`) with the different envelope `PROC && *PROC > 0` (`:74`). Fresh URLs: `src/supplementary/executor/Executor.hpp` + `.cpp` (bracket grammar = window rules applied to the new window — [INF] until opened). Per critic D4 this carries HIGH widening risk (process plane is tsukuroi's); acceptable only framed tightly as "the exec dispatcher's own execution". Reported, not recommended, given Subject 1 and Subject 2 exist.

## Candidate subject 4 (not recon'd in depth): Lua-provider `hl.dispatch` internals

Critic D2: cleanest provenance (fresh files under `src/config/lua/` at `efb50993`), r51 step 9 leaves it `[UNK]`. I did not locate exact filenames from local evidence and did not guess paths; listed for completeness. Subject 1 is already built and Subject 2 needs only two fresh files, so D2 is unnecessary this round.

## Recommendation to the build seats

1. Land Subject 1 (draft) after the four fixes above: re-open/fresh-fetch the four URLs (or word criterion-17 reopens), demote/reframe P16 against R2, sharpen P07 to the sendshortcut-path consequence, fix S373's hpp anchor, and add a per-proposition R1–R7 distinctness mapping (answers attack A1 — the counter is subject-agnostic).
2. Hold Subject 2 as the fallback if the draft's subject is judged R2-entangled beyond repair; its two fresh files and zero R1–R7 entanglement make it the strongest clean provenance.
3. Do not spend wave effort on Subject 3; Subject 4 only if both 1 and 2 fail.

## Commands / results exercised (all read-only, lane repo + pinned bytes)

- `grep -n 'dontInhibit\|disable_keybind_grabbing\|shortcutsInhibit\|isSessionLocked\|releasePending\|m_pressedSpecialBinds\|passEvent\|handleKeybinds' Hyprland-KeybindManager.cpp` → gate sites `:603/:638–641/:643/:649/:782–795/:842/:844–851`; callers `:409/:431/:502/:512/:523/:461–468`.
- Range reads `Hyprland-KeybindManager.cpp:348–443, 594–703, 699–873` → onKeyEvent press/release plumbing, the full hit-collection and dispatch loops, exact check order.
- `sed -n '1490,1560p' Hyprland-legacy-ConfigManager.cpp` → flag block `:1496–1541` incl. `case 'p': dontInhibit = true; break;` `:1529`; exclusivity `:1545–1552`.
- `grep -n 'supplementary/executor/Executor.hpp\|executor()->spawn\|spawnRaw\|No closing bracket' Hyprland-legacy-DispatcherTranslator.cpp` → `:4/:66/:68/:73`.
- `sed -n` sample of draft anchors (`:531/:540–547/:557/:565–566/:574/:582–586/:591–624`, `ConfigActions.hpp:114–117`, `ConfigActions.cpp:1537/:1554/:1558/:1578–1579/:1601`) → all exact.
- `grep -n 'm_keyToCodeCache\|keyToCode' …` → declared `Hyprland-KeybindManager.hpp:149`, filled `legacy-DispatcherTranslator.cpp:559–576`.
- `grep -rn 'disable_keybind_grabbing\|shortcutsInhibit\|ShortcutsInhibit' round-51/fetch/wiki-*.md` → zero hits (documentation gap for Subject 2).
- `python3 -c … fetch-manifest.json` → URL/sha256 template for fresh opens and the four draft re-fetch equality receipts.
- Held-entry reads: `corpus/knowledge/{hyprland-dispatcher-dispatch-r51, dispatcher-surface-and-request-grammar-r26, dispatcher-semantics-r25, bind-table-r25, keybind-rule-semantics, hyprland-bind-key-match-r50}.md`; `.ufo/waves/round-52/w1/C2CoverageCritic.md`; draft artifacts under `.ufo/waves/round-52/w1/C2EntryDraft/`.

## Limitations

- No fetches performed (scout seat, source-only, no runtime): Subject 2's P-A5 and Subject 3's bracket-grammar proposition are marked [INF] pending the wave's fresh opens; line numbers are from the pinned round-51 bytes and must be re-verified against the round-52 fetch.
- Sibling drafts were mid-flight; my Subject-1 verdicts are anchored to the draft artifact as read this round.
- Novelty judgment is seat-level (critic A1); this report supplies the overlap evidence, not a vote.

## Deliverables

- `.ufo/waves/round-52/w1/C2SourceRecon.md` (this file)

Report: .ufo/waves/round-52/w1/C2SourceRecon.md
