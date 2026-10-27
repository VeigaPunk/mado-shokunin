# R53Five41 — scribe: C1 ledger-counter acceptance evidence and C2 P16–P18 repair draft

## Scope and registration

- Round 53, wave w1, item 41. Registration: `.ufo/waves/round-53/w1/swarm-registry.json` → `members.R53Five41 = {kind:spawn, agentId:null, role:scribe, item:null}` (read 2026-10-27). Leaf seat: no dispatch, no background jobs, no git/jj mutation.
- Governing prose: `.ufo/waves/round-53/claims-frozen.md:5-13`. C1 = a *newly committed*, scratch-aware counter with an explicit selftest that returns `TARGET_MET` on the production ledger and `TARGET_MISSED` on a no-work control **and each frozen forgery fixture**, with exact population coverage and non-self pointers, expressly structural (not semantic proof). C2 = an append-only correction of r52 propositions P16/P17/P18 against opened pinned bytes, a frozen counter that rejects the old entry bytes and accepts the corrected entry with quote/pin/proposition bindings, independent source-truth review, and **no expansion credit** unless an admitted entry rests on a source row opened this round plus uncovered ground per the coverage map.
- Axes named: **operability** (C1) and **coverage** (C2). No other axis is claimed or moved.
- Source-only round honoured: no network fetch, no live read, no producer execution, no package query, no host/config/compositor mutation. Disk guard before work: `df -h /fast` → `804G … 595G avail 26%` (`/tmp` 124G avail). Scratch: `/fast/scratch/hyaku/mado-r53/R53Five41`, removed at completion.

## 1. C1 — measured base state (what the r53 counter must beat)

All numbers below are re-derived at the frozen base `ad4bf2059bcfafe63671d262222908ee1fe8001c` from the revision, never the working tree.

**Population and ledger (§ exact commands in the trailer).**

```
population 82 ledger_rows 82
uncovered 0 dangling 0 dup 0
bad_pointer 0 self_pointer 0
```

Breakdown: `tools/` = 17, `quality/*.py` = 19, `quality/counters/*.py` = 46 → 82. The 82-row ledger at base `quality/tool-ledger.md` (sha256 `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`) parses to exactly 82 three-cell rows **only when fenced blocks are skipped**: the grammar example at `quality/tool-ledger.md:11-13` is a four-cell pipe row. The committed r51 counter does skip fences (`parse_rows`, `c1-r51-ledger.py:157-163`); the fence-blind failure was measured on the r52 landed rewrite, not on r51 (r52 `w2/Attack01.md` O1: `ledger_rows=83 … TARGET_MISSED`), so a new counter must keep the skip. Measured: every production row is 3-cell (`multi_cell` = none); the frozen control `c1-do-nothing.md` is 4-cell and unbackticked, so a parser that requires exactly three cells and a backticked first cell drops it and reports a coverage miss, **not** the self-pointer/context defect the freeze names (r52 `Attack01.md` O2, measured on the r52 landed 78-line rewrite: `uncovered=82`).

**No r52/r53 counter is committed.**

```
$ git ls-tree -r --name-only HEAD | grep -cE '^quality/counters/.*r5[23]'
0
```

So at base the C1 predicate is unmet by construction, and the r51 counter (`quality/counters/c1-r51-ledger.py`) is the only committed checker. Its declared fields are `population/ledger_rows/uncovered/dangling/bad_pointer/empty_desc/dup/selftest` — **no `self_pointer` and no `generic_desc`**. `empty_desc` is a placeholder-only regex (`PLACEHOLDER`, `:76`, applied at `:230`), so a semantically empty description such as `A tool.` is accepted; `bad_pointer` asks only that **one** pointer token resolve and contain the row's basename (`pointer_tokens`, `:173-195`, then `pointer_resolves`, `:196-208`) with no self-reference test anywhere, so a row that also names a legitimate document passes whatever the other token spells — the nine Attack02 laundering shapes pass by construction `[INF code-path]`. The `generic_desc`/`self_pointer` clauses were added by the r52 draft, and those are the clauses the r52 attacks falsified (Attack01 T2: 82/82 forged descriptions `TARGET_MET`; Attack02 P03–P09/P19–P21: nine spellings `TARGET_MET`). Its green on the production ledger is a property of the production bytes, not of the test: the base ledger contains exactly one occurrence of `tool-ledger.md` and it is prose (`quality/tool-ledger.md:3`), never a pointer cell.

**Frozen forgery fixtures that exist as bytes at base** (sha256 prefix, row count):

| fixture | sha256 | data rows | shape |
|---|---|---|---|
| `.ufo/waves/round-52/controls/c1-do-nothing.md` | `ad72f72f64708d1b` | 2 (+header+separator) | 4-cell, unbackticked, generic self-pointer prose |
| `.ufo/waves/round-52/controls/c1-row-context-control.md` | `72220dc53ef91c74` | 2 | valid 3-cell grammar, description `A tool.` |
| `.ufo/waves/round-52/w2/Attack01/controls/F-all-forged.md` | `d793c9ef352eaf51` | 82 | production pointers verbatim, 82 forged descriptions |
| `…/H2n-verify.sh-forged.md` | `859e45edf552867a` | 84 | single-row variant on the unfenced ledger |
| `…/H3n-c2r51-forged.md` | `92ed1e4686d56ad2` | 84 | single-row variant on the unfenced ledger |
| `…/H4n-nameonly-forged.md` | `86e953ee5485c97f` | 84 | own-name restatement |
| `.ufo/waves/round-52/w2/Attack01/production-ledger-nofence.md` | `cd2ff6039c74cdff` | 84 | base ledger with the fence removed |

**Gap the r53 freeze inherits.** "Each frozen forgery fixture" is not enumerable at base: Attack02's nine laundering shapes (P03–P09/P19–P21) exist only as generator code in `.ufo/waves/round-52/w2/Attack02/run-probes.sh:89-230`; no fixture bytes are persisted. A r53 counter cannot demonstrate `TARGET_MISSED` "for each" fixture whose bytes do not exist. Candidate materialisation from the generator (verified line refs): P03 bare ledger basename (`run-probes.sh:94`), P04 row own basename, P05 `./` prefix (`:120`), P06 trailing `)` inside backticks, P07 non-numeric `:x` suffix, P19 double slash, P20 leading slash, P21 case fold, P09 symlink mode `120000` to the instrument's own file (`:168`, `git ls-files -s` mode asserted at `:177`).

**Two mechanical constraints the r53 counter must satisfy that the freeze text implies but does not spell out.**

1. **Self-accounting without a self-pointer.** The counter lands in the population it measures: committing `quality/counters/c1-r53-*.py` moves `population` 82 → 83, and `uncovered=0` then forces a ledger row naming it, while "non-self pointers" forbids that row pointing at the counter or at the ledger. The pointer must be a different tracked file whose bytes contain the counter's basename. `.ufo/waves/round-53/` is untracked at base (`git ls-tree -r --name-only HEAD | grep -c round-53` → `0`; working tree `?? .ufo/waves/round-53/`), while `.ufo/waves/round-51/registration.md` **is** tracked — so a pointer to a round-53 registration resolves only if that file is committed in the same landed change. Alternatives that are tracked today: `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-53.md`.
2. **Scratch discipline is part of the predicate.** The frozen text says "scratch-aware". The r51 counter refused roots under `/tmp`, `/var/tmp`, `/dev/shm` (`c1-r51-ledger.py:68`) and redirected `HOME`/`TMPDIR`/`XDG_*` into `--work` for child processes (`:43-45`, implemented `:258`). A new counter that resolves the ledger from `--rev` in a clone, or that reads the caller's `--ledger` path, must state which it does — the r52 attacks used `--ledger` to feed forged bytes while instruments resolved at `--rev` (`Attack01.md` Limitations), which is the intended control mechanism and must stay documented.

**Freeze-ordering finding (measured).** `claims-frozen.md:13` states "Control design and measurement must be frozen before data." At the base revision no round-53 control design is committed or frozen: `git ls-tree -r --name-only HEAD | grep -c round-53` → `0`, and the round directory holds only `claims-frozen.md`, `w1-spec.json`, `w1-dispatch.json` and the wave markers (working-tree observation, `w1.ready` / `w1.ready.dispatched` present). No registration file, no fixture manifest, no counter. Wave-1 seats are already measuring. Consequence for acceptance: the C1/C2 receipts must either (a) land the frozen control/fixture manifest in a change whose content precedes their own measurement revision — the only reading that satisfies the sentence — or (b) be recorded as a freeze-ordering defect at closure. A counter committed after the measurement it reports cannot retroactively freeze its controls; the r52 sequence (claims → regression-critical wave → counters drafted, then falsified) is exactly the pattern the sentence forbids.

**Acceptance matrix drafted for the r53 C1 builder** (each row is a required observable, no semantic claim):

| # | Condition | Required observable |
|---|---|---|
| 1 | production ledger at the landed rev | `TARGET_MET`, exit 0, `population` = independent `git ls-tree` count, `ledger_rows == population`, `uncovered=dangling=dup=bad_pointer=self_pointer=generic_desc=0` |
| 2 | no-work control `controls/c1-do-nothing.md` | `TARGET_MISSED`, exit 1, defect attributed to self-pointer/context, **not** to schema shape (the 4-cell form must be parsed or explicitly rejected as `SETUP`, never silently as coverage) |
| 3 | `c1-row-context-control.md` (`A tool.`) | `TARGET_MISSED` on description context alone |
| 4 | `F-all-forged.md` (82 forged descriptions) | `TARGET_MISSED`; if it still passes, the freeze is falsified and the honest-stop rule applies |
| 5 | `H2n`/`H3n`/`H4n` | `TARGET_MISSED` each |
| 6 | Attack02 P03–P09/P19–P21 materialised | `TARGET_MISSED` each via normalised identity (strip leading `/`, collapse `//`, fold case, cut non-numeric suffix, treat bare basename in the pointer region as self, and exclude git mode `120000`) |
| 7 | `--selftest` | runs without `--repo`/`--rev`, prints an explicit pass/total, exercises at least one red and one green arm |
| 8 | scratch | no write outside `--work`/`TMPDIR`; refuses a scratch root inside the scored repo |

**Evidence-grade limit.** Rows 1–8 are structural. None of them licenses "the ledger is accountable" in any semantic sense; the r52 `Attack01.md` T2 ceiling (a real functional phrase copied out of the instrument's own bytes survives any lexical filter) is a *permanent* ceiling of this clause shape and must be repeated in whatever receipt lands.

## 2. C2 — reproduced source truth for P16/P17/P18 and a repair draft

**Entry identity.** `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` at base = sha256 `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078`, 18 propositions P01–P18, indexed at `corpus/README.md:80`. Pinned bytes: `.ufo/waves/round-52/fetch/`, `sha256sum -c SHA256SUMS` → all five entries `OK` (ConfigActions.cpp `a83abeb5…`, ConfigActions.hpp `746c6f51…`, KeybindManager.cpp `8d8f35fc…`, legacy-DispatcherTranslator.cpp `7248cbb8…`, README.txt `c53296ae…`). Those hashes equal the ones the registry rows carry (`corpus/SOURCES.md:320-323`), so the local copies are the row-bound bytes.

**Independent quote re-measure (18/18 rows, whitespace-collapsed, against the pin span):**

```
P01..P15,P17,P18  verbatim_anywhere=True  within_pin_span=True
P16               verbatim_anywhere=False within_pin_span=False
words: min 5, max 19 (P03)   → every quote ≤25 words
```

This reproduces the r52 spot-check field for field: **17/18 verbatim, P16 spliced**.

**P16 — spliced quote (mechanical, not a judgement).** Pin `Hyprland-ConfigActions.cpp:1554-1558,1576`. Lines 1554 and 1558 are separated by:

```
1555: (blank)
1556:     if (S.m_passPressed == 1) {
1557:         if (!isMouse)
```

The entry's space-joined quote `sendKeyboardMods(modMask, 0, 0, 0); sendKeyboardKey(…)` therefore occurs nowhere in the file, and the elided guard is material: the quoted `PRESSED` call is branch-conditioned. The proposition's second clause ("then clears the modifier state") rests on `:1576`, which is inside the locator but outside the quote — the r52 rationale itself says "the clear call at 1576 is included in this locator". So P16 fails on two surfaces: quote contiguity and quote-only support.

**P17 — quote true, subject false.** Pin `DispatcherTranslator.cpp:619-622`; quote verbatim. But the pin sits inside `sendkeystate`, whose body is `:591-627`; `sendshortcut` is `:531-589`. Measured on the bytes:

```
keyState in 531-589: 0      repeat in 531-589: 0
keyState in 591-627: 5      sendshortcut( calls in 591-627: 2
```

The proposition "`sendshortcut`'s repeat branch can invoke its delegate twice" is contradicted by the pin's own function boundary; the repeat branch belongs to `sendkeystate`, and the callee invoked twice is `sendshortcut`. P04 already states the same mechanic correctly and located, so P17 is a duplicate carrying a false owner.

**P18 — quote true, localization false.** Pin `:574`, quote verbatim. The enclosing loop is `:565-571`; `:573` is `if (!keycode)` and `:574` the return, both **after** the loop closes, inside the cache-miss `if` block (`:559-574`; the cache-hit `else` is `:575-576`). "inside the scan" is false; the r52 rationale silently re-scopes to "keysym resolution branch", which is true but is not what the proposition says.

**Append-only correction draft (prose only; NOT applied — no tracked edit made).** Insert as a new, dated section; keep P16–P18 in place and mark each `superseded-by:`:

```
## Correction 2026-10-27 (round 53) — P16–P18 re-grounded against the same pinned bytes

Supersedes P16, P17 and P18 above. Bytes: `.ufo/waves/round-52/fetch/`, revision
efb50993780079460b0cbed1363e2166a2de1d9f, SHA256SUMS verified this round.
P16, P17 and P18 are retained verbatim as history and must not be cited as admitted ground.

| ID | Proposition | Source row | Pin:anchor | Quote (<=25 words) | Support class | Why it supports |
|---|---|---|---|---|---|---|
| P16a | `Actions::pass` sends the keyboard modifier state before any key or pointer event. | S371 | Hyprland-ConfigActions.cpp:1554 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` | direct | The modifier send is the first seat call after the optional focus block. |
| P16b | The `PRESSED` key call is branch-conditioned on `m_passPressed == 1` and a non-mouse key. | S371 | Hyprland-ConfigActions.cpp:1556-1558 | `if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | The guard and the guarded call are one contiguous excerpt; the `passPressed == 0` branch at :1561-1565 sends `RELEASED`. |
| P16c | `Actions::pass` clears the keyboard modifier state after the key branch. | S371 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct | The clear call is at :1576, after the :1556-1574 branch tree; it is a separate contiguous excerpt, not spliced with P16a. |
| P17' | `sendkeystate`'s `repeat` branch invokes `sendshortcut` a second time only when the first call succeeded. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct | The repeat branch and the callee are both inside `sendkeystate` (:591-627); `sendshortcut` (:531-589) holds no `keyState`. Note: duplicates P04's mechanic; distinctness is a QUALITY matter, not a truth defect. |
| P17'' | `sendkeystate` writes `m_passPressed` to 1 for `down`/`repeat` and to 0 otherwise, after saving the prior value. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:614-615 | `if (keyState == 1 || keyState == 2) Config::Actions::state()->m_passPressed = 1;` | direct | The write is the branch that the P16b guard reads; the copy and the restore are at :612 and :624. |
| P18' | On a cache miss, `sendshortcut` returns the "key not found" error after the scan loop, not inside it. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:573-574 | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct | The enclosing loop is :565-571; :573-574 executes after it closes, inside the cache-miss `if` block (:559-574). |
```

Every quote above was validated contiguously (whitespace-collapsed) inside its named span, word counts 4/12/4/13/11/12, all ≤25. P17'' is offered so the correction adds a proposition that P04 does not already state, if the reviewer prefers distinctness over minimal re-attribution; both variants repair the misattribution.

**Counter discrimination requirement (C2 freeze clause "rejects the old bytes and accepts corrected entry").**

- Reject: at base `bee0d143…`, the P16 row's quote is not a contiguous substring of its pin span, so a byte-opening checker reports `quote_not_at_pin` and exits `TARGET_MISSED`. That clause alone discriminates old from corrected.
- Accept: corrected rows must pass four bindings simultaneously — (i) proposition text present, (ii) `Source row` names a `corpus/SOURCES.md` row with status `mined` and the entry's own path in its used-by cell, (iii) `Pin:anchor` resolves to a file whose basename is in the entry's pin manifest **and** whose revision is the pinned `efb5099…`, (iv) the quote is verbatim (whitespace-collapsed) inside the named line span and ≤25 words.
- Hazard to close: r52 `w2/Attack07.md` T6 — a counter that binds quote-to-pin **by name only** accepts invented quotes at real pins (`TARGET_MET`). "Quote binding" must therefore mean opening bytes at the pin span; a receipt must name the bytes' sha256 so the check is re-derivable without the worktree (QUALITY 63's witness rule).
- Shape hazard: r52 `Attack07.md` T1 — a row regex expecting `| P## | S### | …` against an entry whose table is `| P## | Proposition | S### | …` yields `props=0`. A r53 counter must declare its accepted table grammar in its docstring and selftest it, exactly as the r51 counter documents its citation grammar (`c2-r51-dispatch-entry.py:22-44`).

**Expansion-credit boundary (measured, not assumed).** `git ls-tree -r --name-only HEAD corpus/knowledge | wc -l` → `68`; `git show HEAD:corpus/README.md | grep -cE '^\| \`knowledge/'` → `68`. The synthetic-dispatch ground is already indexed (row at `corpus/README.md:80`), and rows S370–S373 were opened 2026-10-27 **in round 52**, with `used-by` already naming the r52 entry. Under the freeze's wording the repair therefore earns **no expansion credit**: it rests on no row opened this round and covers no ground the map does not already hold. What would be needed for credit — a new registry row (S374+) on ground absent from the map, opened this round, plus an admitted entry resting on it — is unreachable source-only without new bytes, so this seat records the boundary rather than manufacturing novelty by re-opening r52 rows under a new number.

## 3. Draft lesson prose (for `corpus/lessons/round-53.md`; NOT applied)

Two routed r52 defects are still open at base and this is the prose that closes them if integration accepts it.

**(a) `## Gate` — per-row records for S370–S373** (CORPUS contract rule 1: URL, access date, ≤25-word located quote grounding `teaches`). Rows were registered in round 52; the quotes below were re-opened this round from the committed pinned copies, not re-fetched.

```
- S370 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp
  — accessed 2026-10-27 (r52 fetch, SHA256SUMS OK this round) — teaches `sendshortcut`/`sendkeystate`
  parsing and key resolution — quote (13 words, :531-533): `static SDispatchResult sendshortcut(const
  std::string& args) { CVarList2 ARGS(args, 3); if (ARGS.size() != 3)`
- S371 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp
  — accessed 2026-10-27 — teaches synthetic key/modifier delivery call order — quote (4 words, :1554):
  `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`
- S372 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.hpp
  — accessed 2026-10-27 — teaches shared action timestamp/state field declarations — quote (10 words,
  :117): `uint32_t m_timeLastMs = 0; // timestamp of last key/mouse event`
- S373 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp
  — accessed 2026-10-27 — teaches `stringToModMask` normalisation/membership — quote (5 words, :223-224):
  `std::ranges::transform(mods, mods.begin(), ::toupper); if (mods.contains("SHIFT"))`
```

**(b) `## Changes` replacement prose** (r52's section still reads "Pending final integration revisions and receipts", which the r52 closure already falsified — routed defect 2):

```
## Changes

Round-52 landed: `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (sha256 bee0d143…ecb078 at
ad4bf20), index row corpus/README.md:80, registry rows S370–S373 (corpus/SOURCES.md:320-323), pinned
bytes .ufo/waves/round-52/fetch/ (SHA256SUMS OK). Admission was not granted: the entry's P16 quote is
spliced and P17/P18 state false subject/localisation; a round-53 append-only correction re-grounds
those three against the same bytes. No C1 counter was committed in round 52; the C1 predicate is
measured from a newly committed counter only.
```

**(c) Mistake-class prose** (extends M52-1's class without overwriting it):

```
M53-1 · class `mechanical-vs-semantic evidence` · a green structural counter is not evidence of the
property its name suggests. Reproduced: the committed r51 pointer test has no self-reference check at all (nine
laundering spellings pass it), the r52 context test passes 82/82 forged one-line descriptions, and
the production ledger passes both. Fix: state the clause's ceiling in the receipt (lexical accountability only), keep the
forged fixture in the discrimination suite, and never let a production-only run stand as the
demonstration.
```

## 4. Routed r52 defects — status at the round-53 base, as evidence only

| # | Routed defect (`corpus/lessons/round-52-verifier-spotcheck.md:69-75`) | Status measured at `ad4bf20` |
|---|---|---|
| 1 | `round-52.md` `## Gate` lacks per-row URL/date/quote records for S370–S373 | **open** — `## Gate` (§C1/§C2/§Admission) contains instructions only; no row records (`corpus/lessons/round-52.md:5-21`) |
| 2 | `## Changes` stale ("Pending final integration revisions and receipts") | **open** — same text at `:23-25`; round-52 work did land at `56d6e70` |
| 3 | QUALITY 17 distinct-scope review owed for S370≡S365, S371≡S367, S373≡S364 | **open** — `corpus/QUALITY.md:34` defines the criterion; the S370–S373 registry cells (`corpus/SOURCES.md:320-323`) carry no review verdict and the lesson carries no record (W04 remains a warning) |
| 4 | P16–P18 repair or per-row `superseded` marking in the entry | **open** — entry unchanged at `bee0d143…`; defects recorded only in M52-1 and the W2 reports |
| 5 | No SHONEN box gained a new non-author verifier | **not re-measured here** — outside a scribe's source scope; the r52 closure records all four boxes `[~]` |

This seat is lane-dispatched and therefore **is not** a non-author reviewer; nothing in this report may be counted as independent review credit for either claim.

## 5. Axis accounting and harm check

| Axis | Claim | Move | Evidence |
|---|---|---|---|
| operability | C1 | **none landed**; acceptance matrix + the two unstated constraints (self-accounting row, fence/grammar/symlink rules) are drafted | §1; `population 82 → 83` arithmetic; `git ls-tree … grep -c r5[23]` → 0 |
| coverage | C2 | **none credited**; repair draft + discrimination contract defined; expansion credit explicitly withheld | §2; 17/18 verbatim reproduced; 68/68 indexed, ground already mapped |
| depth / freshness / calibration / adjacency | unchanged | no behavior asserted from source-only bytes; no docs-inference upgraded to host state | — |

No axis is harmed: this report writes one untracked wave file and nothing else. No tracked lane file, fleet file, sibling path, script/template/state/watchdog, or `shokuknow` target was written; no git/jj mutation, no install (`pacman` paused; no tool installed), no live read, probe, screenshot, or producer run. No claim admission is asserted.

## Trailer

**Attacked predicate.** C1 frozen structural operability predicate (`.ufo/waves/round-53/claims-frozen.md:5-7`): a newly committed scratch-aware counter, explicit selftest, `TARGET_MET` on the production ledger at `ad4bf2059bcfafe63671d262222908ee1fe8001c`, `TARGET_MISSED` on a no-work control and each frozen forgery fixture, exact population coverage, non-self pointers. C2 frozen coverage predicate (`:9-11`): append-only P16–P18 repair against opened pinned bytes, a frozen counter that rejects the old entry and accepts the corrected one with quote/pin/proposition bindings, independent source-truth review, and no expansion credit absent a row opened this round plus uncovered ground.

**Exact commands and outputs** (all read-only; cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`, scratch `S=/fast/scratch/hyaku/mado-r53/R53Five41`):

```
$ df -h /fast            → /dev/nvme1n1p2 804G 209G 595G 26% /fast
$ git ls-tree -r --name-only ad4bf2059bcfafe63671d262222908ee1fe8001c | wc -l            (tree captured to $S/tree-*.txt)
  python3 population filter over that listing → population 82 (tools 17 / quality/*.py 19 / counters 46)
$ git show ad4bf2059…:quality/tool-ledger.md | sha256sum
  → df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b
  fence-skipping parse → parsed_rows 82; all three-cell; multi_cell none
$ git ls-tree -r --name-only HEAD | grep -cE '^quality/counters/.*r5[23]'   → 0
$ git ls-tree -r --name-only HEAD | grep -c 'round-53'                     → 0
$ git ls-tree -r --name-only HEAD | grep -c 'round-51/registration.md'    → 1
$ git ls-tree -r --name-only HEAD .ufo/waves/round-51/ | head   → claims.md, fetch/… (tracked tree)
$ git status --porcelain                                                   → ?? .ufo/waves/round-53/   (only)
$ sha256sum corpus/knowledge/hyprland-synthetic-dispatch-r52.md
  → bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078
$ git show HEAD:corpus/knowledge/hyprland-synthetic-dispatch-r52.md | sha256sum   → bee0d143…ecb078 (identical)
$ cd .ufo/waves/round-52/fetch && sha256sum -c SHA256SUMS
  → ConfigActions.cpp OK / ConfigActions.hpp OK / KeybindManager.cpp OK /
    legacy-DispatcherTranslator.cpp OK / README.txt OK
  18-row quote check (whitespace-collapsed, in-span) → 17 verbatim; P16 verbatim_anywhere=False
  word counts: max 19 (P03), all <=25
$ awk 'NR>=531&&NR<=589' …DispatcherTranslator.cpp | grep -c keyState   → 0
$ awk 'NR>=591&&NR<=627' …DispatcherTranslator.cpp | grep -c keyState   → 5
$ awk 'NR>=591&&NR<=627' …DispatcherTranslator.cpp | grep -c 'sendshortcut(' → 2
  proposed-repair quote validation → 10/10 contiguous in named span, words 4/4/12/11/13/12/15/13/5/10
$ git ls-tree -r --name-only HEAD corpus/knowledge | wc -l            → 68
$ git show HEAD:corpus/README.md | grep -cE '^\| `knowledge/'         → 68
  independent ledger audit at base → population 82 ledger_rows 82 uncovered 0 dangling 0 dup 0
    bad_pointer 0 self_pointer 0
  fixture hashes → ad72f72f64708d1b / 72220dc53ef91c74 / d793c9ef352eaf51 / 859e45edf552867a /
    92ed1e4686d56ad2 / 86e953ee5485c97f / cd2ff6039c74cdff
  code-path reads (no execution) → c1-r51-ledger.py:76 PLACEHOLDER, :155-195 parse_rows/pointer_tokens,
    :196-208 pointer_resolves, :211-246 describe; c2-r51-dispatch-entry.py:22-44 citation grammar
```

**Newly opened external sources.** None. This round opened no URL and fetched no bytes; every source claim above rests on the committed pinned copies at `.ufo/waves/round-52/fetch/` (verified against `SHA256SUMS`), whose registry binding is the existing rows at `corpus/SOURCES.md:320-323` — revision `efb50993780079460b0cbed1363e2166a2de1d9f`, registered access date 2026-10-27, e.g. S370 teaches "`sendshortcut` and `sendkeystate` source-level argument parsing/key resolution" with the located quote `static SDispatchResult sendshortcut(const std::string& args) { CVarList2 ARGS(args, 3); if (ARGS.size() != 3)` at `Hyprland-legacy-DispatcherTranslator.cpp:531-533`. Their identity to the upstream revision at `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp` is inherited from the r52 fetch and is `[UNK]` on this round's own bytes; nothing here upgrades it.

**Tool installs.** None (pacman paused; no channel used).

**Scratch.** `/fast/scratch/hyaku/mado-r53/R53Five41` — created, used for the tree listing, ledger copy, and audit/quote receipts, then removed. No `/tmp` use. Nothing written outside the assigned report path.

Report path (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`): `.ufo/waves/round-53/w1/R53Five41.md`
