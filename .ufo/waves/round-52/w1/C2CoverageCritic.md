# C2CoverageCritic — round 52 coverage-novelty attack on the C2 claim

Seat: C2CoverageCritic (critic, leaf). Assignment: attack coverage novelty by comparing the held
corpus and round-51; identify overlap and whether a distinct subject exists without widening.
No claim or predicate edits; no tracked lane writes; source-only.

## Attacked item and predicate

- **Item attacked:** C2 — coverage, "proposition-bound dispatcher source entry" (claims-frozen.md;
  registration.md "C2 — coverage").
- **Predicate attacked:** "one new indexed entry on a **distinct** Hyprland dispatcher-execution
  mechanism", "grounded in **sources opened this round**", "≥4 substantive propositions; each maps
  to an opened-this-round `S###` row, a pin path/revision and exact located quote ≤25 words, with a
  written support rationale".
- **Thesis of this attack:** the frozen r52 counter is *subject-agnostic* — it checks proposition
  count, row/pin/quote bindings and index presence, nothing about subject overlap with held
  entries. A structurally perfect entry whose subject duplicates round-51 ground would pass the
  counter and add zero coverage. Subject distinctness is therefore a seat-level judgment; this
  report is the evidence for that judgment.

## Counterexample (strongest available from local evidence)

Take a round-52 entry whose subject is "the `hyprctl dispatch` socket verb and how its request
resolves a dispatcher name" — squarely inside the frozen wording "Hyprland dispatcher-execution
mechanism", easily sourced with fresh quotes ≤25 words from new rows on `HyprCtl.cpp`, ≥4
propositions, full bindings, index row. **Every material proposition it can state is already
entailed by held entries:** `dispatcher-surface-and-request-grammar-r26.md` amendment §A2
(S018 reopened round 39: `m_dispatchers.find`, `Invalid dispatcher`, the Lua eval wrapper, the `;`
batch split, flag stripping) and `hyprland-dispatcher-dispatch-r51.md` steps 8–9 (S366: strip,
first-space split, lookup, one-line reply; host branch selection). The entry passes the frozen
counter and the coverage axis gains nothing: **duplicate authority / premature saturation**.

Confirmation that the counter cannot catch this: `receipts/c2-base.txt` shows the *old* r51 counter
printing `admitted=1/1 verdict=TARGET_MET` at base `85d57a81` for the r51 entry itself —
registration explicitly distrusts that receipt for the r52 target ("the preceding entry already
exists, so the new counter must name a separate target slug and prove absent at base"). The same
structural shape passes for a subject-overlapping new entry; nothing in the r52 predicate measures
novelty against held corpus (contrast PRED-C2-r51 clause (c), the ≤30% word-8-gram shingle clause
— **absent** from the r52 predicate).

## Evidence — held-corpus coverage map of dispatcher-execution

Read this round (all local, lane repo at base `85d57a818c3707397e21c840b6498b105ba798aa`):

| Dispatcher-execution mechanism | Held coverage | Evidence (entry / step / row) |
|---|---|---|
| Lua dispatcher description semantics (`hl.dsp.*` describes, does not act; contents unstable) | `dispatcher-semantics-r25.md` (round-32 reopen, S188) | §1–§3 |
| 0.56.0 published dispatcher vocabulary and groups | `dispatcher-surface-and-request-grammar-r26.md` (S196) | §2 |
| Request-socket grammar vs dispatcher surface distinction | same (S186) | §3 |
| `dispatchRequest` name lookup, `Invalid dispatcher`, Lua eval wrapper, `;` batch split, flag strip | same, amendment §A2 (S018 reopened r39); r51 step 8 | `HyprCtl.cpp:1126–1157, 1309–1310, 2085–2096` |
| Dispatcher table population: 71 names, one forwarder; declared map type | `hyprland-dispatcher-dispatch-r51.md` step 1 (S364) | `KeybindManager.cpp:42–113, :785` |
| Translator inner table, `Bad dispatcher` refusal (unreachable from keybind) | r51 step 1 (S365) | `DispatcherTranslator.cpp:31–34, 797–867` |
| Bind parse-time validation, lowercasing, storage of dispatcher field | r51 step 2 (S368); held r50/r25 | `legacy/ConfigManager.cpp:1584–1633` |
| Press-path lookup, mouse rewrite, log-only miss | r51 step 3 | `KeybindManager.cpp:785, 799` |
| Repeat / long-press timer callbacks into the table | r51 step 3 | `KeybindManager.cpp:131, 154` |
| `m_passPressed` lifecycle (three-valued press field) | r51 step 4 (S367, S364) | `KeybindManager.cpp:804/814`; `ConfigActions.hpp:114` |
| `SDispatchResult` defaults (empty return = success, no swallow) | r51 step 4 (S369) | `SharedDefs.hpp:53–55` |
| `submap` write / refusal / alone-dispatch / reset ordering | r51 step 5 (S367) | `ConfigActions.cpp:1664–1681`; `KeybindManager.cpp:775–823` |
| `pass` / `global` / `mouse` / `sendkeystate` semantics, edge replay | r51 step 6 (S367) | `ConfigActions.cpp:1465–1650` |
| Argument splitting for sendshortcut, setprop, alterzorder, mouse, exec | r51 step 7 (S365) | `DispatcherTranslator.cpp:48–51, 532–535, 676, 684, 773` |
| `hyprctl dispatch` socket verb end-to-end + host branch | r51 steps 8–9 (S366) | `HyprCtl.cpp:1128–1157, 2036`; config-era held rule |
| 24-dispatcher declared inventory with live counts | `keybind-rule-semantics.md` §3 | `[INF-docs]`, no dispatch fired |
| Bind field grammar incl. dispatcher/arg fields | `bind-table-r25.md:38,52` (held) | cited by r51 "held ground" |
| Key match chain (the gate before dispatch) | `hyprland-bind-key-match-r50.md` | r51 opens: "picks up after the match" |

Registry tail check: 306 rows, highest `S369` (round-51's six rows). No r52 rows exist yet at
base; the entry must add S370+ rows opened this round.

## Reject list — subjects that would saturate (attacks R1–R7)

Any r52 entry whose subject is one of these duplicates held ground; every material proposition is
already entailed:

- **R1** the socket verb / request-side grammar (r51 s8–9; r26 §A2; `hyprctl-flags-r28.md`;
  `request-socket-live-bound-r8.md`; `request-limits-upstream-r31.md`; `ipc-contract-r25.md`).
- **R2** `submap` / `pass` / `global` / `mouse` / `sendkeystate` semantics (r51 s4–6).
- **R3** dispatcher-table population, name resolution, `Bad dispatcher` (r51 s1).
- **R4** parse-time validation of the dispatcher word (r51 s2; r50 match chain).
- **R5** the documented `hl.dsp.*` Lua surface (r25/r26 — documentation-tier anyway).
- **R6** argument-grammar generalization citing only the same five dispatchers (r51 s7).
- **R7** dispatcher inventory with live counts (`keybind-rule-semantics.md` §3).

## Distinct subjects that exist without widening

The predicate's theme is dispatcher **execution**; the following stay inside it:

- **D1 — per-dispatcher implementations beyond the five read.** r51's own Limits: "the other 66
  entries were counted, not read, so 'each dispatcher reads its own way' is established for those
  five and `[INF]` beyond them." Reading 4+ unread implementations (e.g. the workspace-focus
  family: how `workspace` / `movetoworkspace` resolve a name/id to a workspace object and monitor,
  in `ConfigActions.cpp` / `DispatcherTranslator.cpp` regions outside S365/S367's read scope) is a
  distinct mechanism, explicitly handed over by r51. **Row-collision caveat (attack A3):** those two
  file URLs already carry rows S365/S367 — QUALITY criterion 17 (the S030/S017 duplicate-screen
  precedent, plus the sanctioned S018 round-39 reopen precedent) requires explicit distinct-scope
  wording on any same-URL reopen; a silently overlapping new row is rejectable and would strand the
  entry.
- **D2 — Lua-provider `hl.dispatch(...)` execution internals** (`src/config/lua/` path at
  `efb50993`). r51 step 9 leaves this `[UNK]` (host takes the legacy branch; only the wrapper string
  is quoted, r26 §A2); r25 holds documentation only. Fresh files → fresh rows → cleanest
  provenance. No widening: it is the other dispatch front door, still dispatcher execution.
- **D3 — the `event` dispatcher's socket2 write path in code.** Held coverage is documentation-only
  (r25 §2, S188:59 "Send an event to socket2"). **Widening risk MEDIUM:** must stay on the
  dispatcher side of the boundary (what executing `event(name, data)` does), not the event-queue
  plane (`event-queue-observability-r37.md`, `event-delivery-limits-r26.md`).
- **D4 — `exec`'s downstream spawn chain.** r51 s7 stops at "hands the tail to the process
  executor". **Widening risk HIGH** (drifts into process management). Weakest candidate; only
  acceptable framed as the exec dispatcher's execution, and it is unnecessary given D1/D2.

## Attacks register (named item/predicate each)

- **A1 — duplicate authority / premature saturation** (item: C2 "distinct mechanism"; predicate:
  counter-pass). Counter-pass cannot demonstrate novelty; see Counterexample. **Fixable by seat
  review:** require a distinctness statement in the entry mapping each proposition against R1–R7
  and showing no held entry entails it; the outside source-truth reviewer (required by
  registration) should also confirm subject novelty, not only quote truth.
- **A2 — false provenance** (predicate: "sources opened this round"). Reusing `.ufo/waves/
  round-51/fetch/` pins as this-round evidence fails the predicate: rows must be S370+ opened this
  round with round-52 fetch receipts. Same URL+commit is admissible **only** as an explicit
  distinct-scope reopen per criterion 17 (precedent S018 r39). A new row worded over S364–S369's
  scope is rejectable like S030.
- **A3 — subject overlap via shared-file row scope** (D1-specific): see D1 caveat. The rows seat
  must word new rows as *per-dispatcher implementation semantics*, not "the translator" /
  "ConfigActions" generically.
- **A4 — widening** (predicate: theme is dispatcher execution; SCORECARD's own caution that
  out-of-theme moves "would read as coverage progress it is not"). D3/D4 drift toward the
  event-socket and process planes; D1/D2 do not. Prefer D1/D2.
- **A5 — saturation by sequel**: an entry whose propositions all require r51 conclusions as
  premises and add no new source fact (a restatement of "the socket path uses the same table")
  fails distinctness even with fresh rows. Each proposition must be unanswerable from held entries.
- **A6 — M51-2 inheritance**: r51's errata (lesson `corpus/lessons/round-51.md` M51-2) narrowed
  five conclusions (comma-preservation claim, config-time vs runtime error attribution,
  special-dispatcher count, mouse-reporting attribution, manager-branch inference). A new entry
  must take r51's **corrected** text (present at base `85d57a81`) as held ground and must not
  re-derive the withdrawn claims from scratch as if novel.

## Verdict

A distinct subject **exists without widening**: D1 (unread per-dispatcher implementations — the
surface r51's Limits explicitly hands over) and D2 (Lua-provider `hl.dispatch` internals) both
satisfy "distinct Hyprland dispatcher-execution mechanism". The reject list R1–R7 and attacks
A1–A6 are the fences. A1 is a **fixable defect** (guard by seat review + reviewer novelty check,
both already available in the round's process). None of the attacks requires amending the frozen
predicate; A1 is a process gap the canonical judge should close in judgment, not in the claim.

## Commands / results exercised

- `grep -n "^| S3[5-9][0-9]" corpus/SOURCES.md` → rows S350–S369 present; `grep -c "^| S"` → 306
  rows; highest row S369 (round-51). No round-52 rows at base.
- Read in full: `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`,
  `corpus/knowledge/dispatcher-semantics-r25.md`,
  `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`,
  `.ufo/waves/round-52/{claims-frozen.md,registration.md,mistake-candidate.md}`,
  `.ufo/waves/round-52/controls/c2-do-nothing.md`, `.ufo/waves/round-52/receipts/c2-base.txt`,
  `.ufo/waves/round-51/claims.md`, `corpus/lessons/round-51.md` (M51-2/M51-3),
  `corpus/QUALITY.md` (criteria 1–19 incl. 17), `corpus/README.md` index rows 56–57, 77–78, 115–116,
  `SCORECARD.md` coverage history, `PROVINCE.md` tool/surface table.
- Receipt `c2-base.txt` at base `85d57a81`: old counter `clauses_met=4 admitted=1/1
  verdict=TARGET_MET` — confirms the preceding entry exists at base and that counter-pass is
  structurally independent of novelty.

## Limitations

- I did not read the peers' in-flight drafts (seat dirs were still running at write time); this
  attack is against the claim and the held corpus, not against a specific draft. If C2EntryDraft
  lands inside R1–R7, A1 applies to it by name.
- Shingle-quantified overlap of any future entry cannot be computed here (no entry bytes); the r51
  baseline shows 0.1% max overlap was achieved for the r51 subject, so prose-level distinctness is
  attainable but is not the frozen gate.
- No package queries, live reads, probes, captures, screenshots, producer execution, host/config
  mutation; no installs; no git/jj mutation. Source checkout read-only.
- Scratch `/fast/scratch/hyaku/mado-r52/C2CoverageCritic/` created for this seat, nothing written;
  removed on exit. No `/tmp` evidence.

## Deliverables

- `.ufo/waves/round-52/w1/C2CoverageCritic.md` (this file)

## Report

- `.ufo/waves/round-52/w1/C2CoverageCritic.md`
