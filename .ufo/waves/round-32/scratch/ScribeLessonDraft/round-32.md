author: mado

# Round 32 — assimilation of the Hyprland IPC/dispatcher package; predicate falsified, quarantine adjudicated

> SCRATCH DRAFT (`.ufo/waves/round-32/scratch/ScribeLessonDraft/round-32.md`),
> written mid-wave. All 32 seat reports landed by write time; the last
> (`ReviewEntryDispatch`) folded in — see Gate review layer.

Base: `256222890d935212874a09751ff9b7869943c2d7` (round-31 lane tip,
`registration.md:3`). Pre-round HEAD `91862344b9fddbb5b4c3a9977acc776632993799`
(post-closure r31 spot-check commit sits on top — same dual-base disclosure as
r31). Round: 32, attempt 1. Registration `.ufo/waves/round-32/registration.md`
(frozen before any data seat): two claims — C1 coverage (the Hyprland IPC
two-socket contract + dispatcher surface, frontier → core, on S186/S187/S188/
S189/S196) and C2 calibration (stale published axis table vs re-derived
counters).



## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M32-1 | scope | Staged `ipc-contract-r25.md` §2 quotes `force_idle` (S188:69) with only the first sentence of the cell; the dropped tail "Timers return to normal behavior upon the next activity. Do not use with a keybind directly!" is what ties the dispatcher to the L82 keybind warning the §2 INF builds on. | `w1/reports/ScoutDispatchersWiki.md` claim-5 row; `ScribeEntryDispatchers.md` delta 1; `fetch/S188.bin:69` | `none` — QUALITY 2 requires a measured anchor and the anchor was measured; the truncation lives inside the quoted span, caught by the round's own re-open seat, not by a criterion. | Scribe draft and landing copy re-quote the full cell — but the 28-word re-quote overshot into its own violation (M32-15). Shown able to fail: `awk 'NR==69' fetch/S188.bin` prints three sentences; the staged quote is one — resolving the staged quote against L69 is incomplete (fail); resolving the draft's full-cell quote is complete (pass). |
| M32-2 | scope | Staged `dispatcher-surface-and-request-grammar-r26.md` §1: a keyword-presence check finds `exec` "documented on both" the 0.56.0 and current-git pages — `exec` is a dispatcher name on **neither**: 0 dispatcher-table rows in `fetch/S196.bin` (the bare `exec` tokens are keybind-syntax prose: `exec, uwsm stop`, `exec, loginctl terminate-user`); 0 standalone-word hits in `fetch/S188.bin` (only `exec_cmd`/`exec_raw`). | `w1/reports/ScoutDispatchers0560.md` "`exec` … no" row; `w1/reports/CriticSourcedClaim.md` §S196; own greps: `grep -oE '\bexec\b' fetch/S188.bin` → `0`; `grep -oE '<td><code>exec\(' fetch/S196.bin` → `0` | `none` — the claim never landed; the staged keyword-presence method is itself the defect class (substring presence ≠ documented name). No criterion covers a claim's search method before admission. | `ScribeEntryDispatcherSurface` draft drops `exec` and names the verified set. Shown able to fail: the staged sentence asserts `exec` present on both; the two greps print 0 — the claim fails against both frozen copies; the corrected claim names only names present as dispatcher rows (pass). |
| M32-3 | number-drift | Staged `dispatcher-surface-and-request-grammar-r26.md` §1 INF "the same dispatcher vocabulary" across 0.56.0 and current-git — false: extracted name sets `S196 = 47 ⊆ S188 = 48`, delta `reload_config` (post-0.56 addition). The false clause **propagated** into the normalized registry row: `assimilation/append-block.md` S196 `teaches` ends "…the host's version carries the same dispatcher vocabulary". | `w1/reports/ScoutDispatchers0560.md` keyword verdict; `w1/reports/ScribeEntryDispatcherSurface.md` diff 2; `w1/reports/CriticSourcedClaim.md` S196=OVERSTATED; own extraction over `fetch/S{188,196}.bin` (47 ⊆ 48, only-188: `reload_config`) | `none` — the append transform copies staged `teaches` verbatim with no truth re-check (`ExecAppendTransform.md`: "Unlisted columns … are copied verbatim"). QUALITY 2 binds the claim to its source; nothing binds the row's prose to the entry's corrected facts. | Pending at write time: S196 `teaches` must be reworded before the append lands ("subset of current upstream, delta `reload_config`"). Shown able to fail: name-set `comm` prints `reload_config` (set difference non-empty, staged claim fails); a `teaches` naming the delta passes the same check. |
| M32-4 | number-drift | `w1/reports/ScribeEntryDispatcherSurface.md` states "**45** distinct names" but its own printed set contains **47**, and states "current = **46**" while the current-git extraction is **48**. | `w1/reports/ScribeEntryDispatcherSurface.md:24-32` (text) vs its list (:26-32, 47 members); `w1/reports/ScoutDispatchers0560.md:69` ("47"); own extraction. | `none` — seat-report arithmetic is not claim-admitted text; QUALITY 10's re-derivation rule covers published counts and this count was never re-derived. | Erratum in this lesson / report correction: counts are 47 (0.56.0) and 48 (current). Shown able to fail: counting the report's own printed list yields 47 ≠ 45 (fail); re-stating 47/48 passes. |
| M32-5 | reference-drift | Staged `ipc-contract-r25.md` S186 line pins are uniformly offset from the re-fetched bytes: grammar `(S186:7-12)` → `:19`; freeze note `(S186:15)` → `:21-23`; framing `(S186:18-25)` → `:30`; example `(S186:25)` → `:32`; sockets → `:14`/`:25`. S189 quote `// 10 max queued.` sits at `:34`, staged under `:14, :35`. | `w1/reports/ScoutIPCWikiCurrent.md` faithfulness table; `w1/reports/ScoutIPCEventMgr.md` Claim C nit; `w1/reports/CriticSourcedClaim.md` §S186 ("5 wrong locators") | `none` — QUALITY 2 requires the anchor and 27 requires reproducible bytes (both hold: URL+sha pinned); no instrument resolves per-line pins inside an entry. Caught by the item-10 re-open gate, not a criterion. | `ScribeEntryIPC` draft re-pins all five locators and moves the quote to S189:34. Shown able to fail: `sed -n '7,12p' fetch/S186.bin` does not contain "Basically, write" (staged pin fails); `sed -n '19p;30p;32p'` returns the quoted strings (draft pins pass). |
| M32-6 | attribution | Staged `ipc-contract-r25.md` §4: "The only textual difference in the extraction was the table's own `name` column header" — attributes a property of the *staging extraction* to the sources; both catalogue headers literally read `name | description | data`. | `w1/reports/ScribeEntryIPC.md` "Staged claims dropped" item 1 | `none` — a meta-claim about an extraction artifact; the re-open gate caught it, no criterion names the class. | Dropped in the scribe draft; the OBS keeps only "both catalogues carry the same 44 event names". Shown able to fail: the staged sentence asserts a source-level diff fact whose only evidence is the extraction process — unverifiable against source bytes (fail); the draft's sentence re-derives from the byte diff (pass). |
| M32-7 | vacuous | C1's frozen predicate is falsified in **both directions**: it counts matching lines, not the claimed set — a two-sided **junk** commit prints the target `entries=3 rows=5 cited_entries=3` (v1: five 11-col stub rows + three 13-byte entries; v2: five copies of `| S186 |`; v3: extra unregistered ids ride free) — and the **real** landing can't reach it either: with the three real scribe drafts sitting in the worktree the verbatim counter prints `entries=3 rows=0 cited_entries=5` — the third field counts `source:` *lines* (A cites three rows, B and C one each) while the target encodes citing *entries* = 3. v4-realistic-overcount predicted exactly this false negative; the live run confirms it. The K1 "do-nothing controls" test only *one-sided* commits — the attack they were meant to exclude passes them (`ExecThemeHoldCheck` ran both legitimately: (a) `0/5/0`, (b) `3/0/3` — (b)'s stubs print `cited_entries=3` only because each stub cites one id; the counting flaw surfaces only with the real multi-cite provenance). | `w1/reports/CriticC1Predicate.md` attacks 1/3/4; receipts `.ufo/waves/round-32/c2/controls/c1-predicate-attack/`; `w1/reports/ExecThemeHoldCheck.md` §3; own counter run on live worktree → `entries=3 rows=0 cited_entries=5` | `none` — the predicate was frozen before data seats per the round contract; K1 controls were registered as one-sided only; no criterion forces a junk-commit attack or a real-landing dry-run before freeze (the r30 CritPredicates precedent shows the same gap; claims then stood on review). | Out of round (target may not be narrowed after scoring): counter v2 = distinct-id set in `## Registry`, per-file word-boundary citation, cited-set equality, `used-by` reciprocity, substance floor, and `cited_entries` counting citing *files*, not `source:` lines. Shown able to fail: the verbatim counter prints the target on v1/v2 junk trees (fail) and a non-target `cited_entries=5` on the real landing (fail); a repaired counter rejects junk and prints `3` on the real files (pass — not run this round; verdict stands on non-author review per the r30 precedent). |
| M32-8 | survivor | Mutation sweep of the lane's existing gates (infrastructure, not the claim under test) leaves two mutants alive plus one pre-existing equivalent mutant: `check-index-rows.py` survives a hoisted dangling-row `continue` — a row whose named note does not exist escapes **all** per-row checks including a missing cited path (M2: `tree-m2` → `errors=0 warns=0` exit 0; the 10-case selftest has no dangling-row fixture); `check-index.py --selftest` survives a deleted assertion because its denominator is `len(checks)` run, not a pinned constant (M5: `11/11 assertions passed` exit 0 — and composite M5+M1 certifies `dangling=0` while self-green); `tree-m2b` shows a Holds cell naming a nonexistent note is accepted **as shipped** (MEG-S2 — backticked paths are existence-checked only in the Sources cell). | `w1/reports/MutExistingGates.md` M2/M5/MEG-S1/MEG-S2/MEG-S3; fixtures `.ufo/waves/round-32/scratch/MutExistingGates/fixtures/tree-m2{,b}` | `none` — the mutants survived *because* no fixture covered them; criterion 25 governs credited tightenings, not existing-gate coverage. Live-gate holes discovered this round; recorded as survivors for the routed repair. | Routed forward (not this round's instrument): a dangling-row fixture in `check-index-rows.py --selftest` and a pinned assertion count in `check-index.py --selftest`. Shown able to fail: today the M2 mutant prints `10/10 assertions passed` exit 0 while accepting `tree-m2` (fail); after the fix the same mutated copy must fail an assertion / exit nonzero (pass). |
| M32-9 | landing | `quality/check-axis-scores.py` — the counter the frozen C2 registration names (`registration.md:124`) — is **untracked**: `git ls-files quality/check-axis-scores.py` prints nothing; file exists only as a mid-wave worktree artifact outside seat write scope (L1 staging). | `w1/reports/ConnectorInstrumentReuse.md` (untracked, absent at base); `w1/reports/SentinelScope.md` §Observations; own `git ls-files` → 0 | QUALITY 8 — treat a path as landed only after confirming it exists at the named commit. The criterion exists; it has not yet been applied because no verdict yet cites the file. | Commit it via `jj-lane.sh` before the C2 counter is scored (also required by `ReviewReportContract` landed-changes list). Shown able to fail: `git ls-files quality/check-axis-scores.py` currently prints `0` lines (fail); after the commit it prints the path (pass). |
| M32-10 | scope | Scribe IPC draft asserts a host-version premise the cited sources can't carry: §3 heading "What the compositor implements at the host's own version" and comment "from the host's tag" — the sources document upstream v0.56.2 *bytes*; nothing cited binds the host to that version (the draft's own §5 admits the installed binary was not interrogated). | `w1/reports/ReviewEntryIPC.md` FAIL item 5; `scratch/ScribeEntryIPC/ipc-contract-r25.md:51,115` | `none` — QUALITY 16 says docs never promote to host facts without host measurement; the premise slipped because the lane's own prior record (S018/S158 host pin) exists but was never cited. Caught by the reviewer seat, not a gate. | Landing copy rewrites the §3 OBS to "the compositor's own implementation at the host's version v0.56.2" with S189 cited as the pinned tree — `grep -n "host's own version" corpus/knowledge/ipc-contract-r25.md` → no hit (scratch draft still fails, landing copy passes). |
| M32-11 | attribution | Scribe IPC draft L60–62 asserts "lightweight tag" for `v0.56.2` — **true** (the reviewer's own `git ls-remote --tags` re-run: `efb50993… refs/tags/v0.56.2`, no `^{}` peel line) but grounded in nothing: `(S189)` is a file:line anchor and the `git ls-remote` line exists in no committed wave receipt. | `w1/reports/ReviewEntryIPC.md` FAIL item 1; `scratch/ScribeEntryIPC/ipc-contract-r25.md:14,60` | `none` — QUALITY 42-adjacent (anchor must name a receipt that says it); the fact was verified post-hoc by the reviewer, not carried by any seat's output. Caught by review, not a gate. | Landing copy drops the tag-type assertion from the provenance header (`source: S189 … (v0.56.2)` only — `grep -n "lightweight" corpus/knowledge/ipc-contract-r25.md` → no hit; the scratch draft still prints it). |
| M32-12 | attribution | Staged `dispatcher-surface-and-request-grammar-r26.md` cites "(wave-1 row **S186**)" at `:22` for the current-git *dispatchers* page — S186 is the IPC `_index.md`, which documents no dispatcher API; the correct row is **S188** (draft-era renumbering residue: staged ids shifted +2 for ids ≥ draft-S187); a second `wave-` pointer at `:44` names "(wave-1 row S018)". Same-residue cluster exists in sibling staged entries (`event-delivery-limits-r26`, `event-queue-host-measurement-r28`) — outside this round's adoption set, named for the merger. | `w1/reports/ReviewUsedByClosure.md` M2 items 1-4; staged `dispatcher-surface-and-request-grammar-r26.md:22,44` | `none` — the package's own closure review found it; no lane instrument resolves prose-level `wave-N row` pointers against the staged registry. | Landing copy carries no `wave-` pointer at all — `grep -nE 'wave-[0-9]|row S1' corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` → no hit, while the staged file prints `:22` and `:44` (staged file still fails, landing copy passes). |
| M32-13 | vacuous | C2's frozen predicate is partially falsified: (a) the publication locator `flat.rfind("Axis table re-derived at")` cannot distinguish a publication from a *quotation* — a correctly-published r32 table followed by a correction entry that quotes the old stale line is shadowed, and the gate reports the quoted numbers as STALE ("a faithfully executed fix can poison its own gate" — C2's own fix instructs appending a correction); (b) a 400-char parse window silently truncates a legal publication; (c) the controls cover only the calibration comparator (single-axis), accept `mismatched>=1` where exactly 2 is the honest expectation, and carry no missing/shadowing control. Attacks 1/2/4 survive (fail-closed missing-publication, literal `A/B` equality, honest `NOT-RE-DERIVABLE` print); attacks 3/5 dead on locator + controls. | `w1/reports/CriticC2Predicate.md` attacks 3/5 + summary table; `check-axis-scores.py --selftest` `17/17` on current bytes | `none` — same freeze-before-attack gap as M32-7; K2 controls were registered without a shadowing or per-axis-perturbation leg. | Out of round (target `mismatched=0` stands): locator must name the publication, not any utterance (reserve the marker phrase to publications; errata cite `SCORECARD.md:<line>`); parse window = the axis sentence; per-axis perturbation + a publication-then-quoted-marker control; tighten (a) to `mismatched=2`; honest `checked=`/pass-domain floor. Shown able to fail: the critic's `published_fractions` demo — correct r32 publication + quoted old line reads `{'navigation':'43/43','calibration':'39/40','operability':'9/9'}` (fail); a publication-scoped locator reads the r32 values (pass). |

| M32-14 | landing | `.ufo/waves/round-30/w1/reports/` still carries 3 modified + 2 untracked files uncommitted since round 30 — `git status --porcelain` → ` M RevRecordsChain.md RevTrendExpansion.md SentScope.md; ?? RevTrendDiscernment.md SimplifierC2.md` — now stacked **underneath** round-32's own assimilation edits; any sweep commit entangles foreign r30 seat bytes with the r32 landing (fleet rule: pathspec-limited commits only, orchestrator sweep owed since r31). | `w1/reports/RevengerPriorDefects.md` row 10 + receipt R10; own `git status` re-run | captured by rule, not by gate — PROTOCOL commit-before-report + lane write-scope collide on orchestrator-owned artifacts; the collision's resolution (orchestrator sweep) has no owner deadline: r31 named it, r32 inherits it. | Pathspec-limited commits for every r32 landing (`git commit -- <path>`), never `commit -a`; orchestrator sweep of the r30 files before round-32 closure. Shown able to fail: `git status --porcelain -- .ufo/waves/round-30/w1/reports/` → non-empty (fail); after the sweep → empty (pass). |
| M32-15 | scope | Landing `dispatcher-semantics-r25.md:49` re-quotes the full S188:69 cell as one blockquote — **28 words**, over the 25-word Gate limit. The fix for M32-1 overshot: ScoutDispatchersWiki split that row into two ≤25-word fragments precisely to stay inside the limit; the draft re-joined them. | `w1/reports/ReviewEntryDispatch.md` Check 3; `corpus/knowledge/dispatcher-semantics-r25.md:49` (own `wc -w` → 28) | `none` — the corpus Gate `≤25-word located quote` rule exists; no instrument counted the landed blockquote. Caught by the entry reviewer. | Split the blockquote into the seat's two fragments, or trim to ≤25 words + prose tail. Shown able to fail: the landed blockquote counts 28 words (fail); splitting at the sentence boundary yields 18+10-word fragments, both verbatim (pass). |
| M32-16 | reference-drift | Both dispatcher drafts carry dangling pointers inherited from staging: `Queued in CANNOT-ANSWER.md` — file absent from lane tree, lane `.ufo/`, and merge tree — and `ground: F1 — "dispatcher behavior" in arc-synthesis §6 U1` — `arc-synthesis` resolves to no file. | `w1/reports/ReviewEntryDispatch.md` Check 4; recursive glob both trees → 0 hits | `none` — the pointers were inherited, never re-resolved; QUALITY 13's committed-path rule doesn't reach pointers declared inside draft text. | Landing copies carry neither pointer (grep → 0 hits — verified). Residual for the *staged package*: the same dangle exists in sibling staged entries — named to the merger, not fixed here. Shown able to fail: `grep -rn 'CANNOT-ANSWER\|arc-synthesis' corpus/knowledge/` → 0 hits while staged files print them (staged fail, landed pass). |

Vocabulary classes with **no observed instance** this round (recorded so the
table is not read as a coverage claim): `stale-premise`, `provider`. (`stale-premise`
was a candidate against C2's registration premise — resolved **for** the
premise on adjudication: `SimplifierEvidence` smoked `quality/check-axis-scores.py`
at tip `50e6a8f` → `MADO_AXIS: checked=3 mismatched=2` (calibration 39/40→41/41
STALE, operability 9/9→12/12 STALE); `CriticC2Predicate` attack-1 rules the same
by convention evidence — the lane's own registration *consumes* the last
published table as its current self-assessment (it picks the lowest-axis
obligation from it), so the base-labeled 39/40 line is the live publication
and is stale against observed state. `ScoutLaneState`'s MATCH×3 compares
against the *after*-values the r31 entry embeds mid-paragraph — a different
question: "is the recorded after-state true" (yes) vs "does the republished
line track the tip" (no). Both readings recorded.)

All 32 seat reports landed. No fact in this draft is UNBACKED.
`RevengerPriorDefects` contributed a 10-row prior-defect regression (r31
lesson backfill owed; five UNCAPTURED criterion candidates registered as
round-33 material; M32-14 is its row-10 live residual).
(`ReviewUsedByClosure` wrote while the scribe drafts were still scratch-only,
so its "the L1's drafts do not exist" line is accurate-but-stale — its
verdicts run on the staged package alone; the landing copies were re-checked
for this draft.)

## Gate

Candidates considered (registration C1): three staged entries plus the five
registry rows they cite, all from the frozen shokuknow package
(`/home/vgpnk/Projects/shokuknow/merge/mado/`, read-only):

| entry | rows cited |
|---|---|
| `corpus/knowledge/ipc-contract-r25.md` | S186, S187, S189 |
| `corpus/knowledge/dispatcher-semantics-r25.md` | S188 |
| `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` | S196 (plus held row S018 — new anchors `:1132/:1149/:1151/:1309/:2096` outside the held ranges; `used-by` extension owed per `CriticThemeScope` §3) |

All five rows were re-opened by the L1's own wave on **2026-10-24** (frozen
fetches in `.ufo/waves/round-32/fetch/S*.bin`, byte-identical to the scout
scratch copies, sha256 prefixes matching the staged anchors —
`CriticSourcedClaim` re-verified independently). Per-row critic verdicts:
S186/S187/S188/S189 **GROUNDED**; S196 **OVERSTATED** (teaches carried M32-3's
false clause). Entry-side per-candidate verdicts (`CriticThemeScope`): all
three **ADMIT** — none is already held (closest held material is inventory-only:
`keybind-rule-semantics.md` covers the *hyprlang* dispatcher vocabulary, not
the Lua `hl.dsp.*` layer).

Review layer: `ReviewUsedByClosure` — five appended rows hold closure in
**both directions** (every `source:` id resolves to a row naming the entry;
every `used-by` names a file that cites the row); adoption-time `used-by`
debts recorded (S018 + S158 are inline-cited by the entries without `source:`
lines — extension owed at adoption, matching `CriticThemeScope`). It also
found stale `wave-N row` id residue in three staged entries — the one inside
this round's adoption set is M32-12. `ReviewEntryIPC` — the scribe IPC draft
FAILED 2 blocking items (M32-10, M32-11), both corrected in the landing copy
which this seat re-checked; 15/15 quote-at-anchor checks, word limits,
provenance trio, sha256s and 44-event re-derivation all PASS.
`ReviewEntryDispatch` — pending; the dispatchers entry is unreviewed.

### ADMITS

| id | URL | access date | located quote (≤25 words, verbatim) |
|---|---|---|---|
| S186 | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md` | 2026-10-24 | `` `EVENT>>DATA\n` (`\n` is a linebreak) `` (frozen L30) |
| S187 | `https://wiki.hypr.land/0.56.0/IPC/` | 2026-10-24 | "any unclosed connections will cause Hyprland to freeze until the five-second timeout is reached" (Note callout; page revision `datetime="2026-05-02T03:38:58.000Z"`) |
| S188 | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md` | 2026-10-24 | "They do not invoke any action immediately, and their contents are not guaranteed to be stable at all." (L9) |
| S189 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp` | 2026-10-24 | `const auto  PATH          = g_pCompositor->m_instancePath + "/.socket2.sock";` (L21; `v0.56.2` tag resolved to this commit this round) |
| S196 | `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/` | 2026-10-24 | "Dispatchers return tables that describe an action you want to make … Their purpose is to be fed into `hl.bind()` or `hl.dispatch()`." (page intro; revision `datetime="2026-07-15T23:56:15.000Z"`) |

Admit conditions carried forward: S196 lands only with its `teaches` erratum
(M32-3); S186/S189 land beside the re-pinned entry locators (M32-5). The
normalized append block (`assimilation/append-block.md`) passed the mirror
census `validate --file …` **exit 0** and the per-row schema review 5× PASS;
`opened` cells were advanced to the L1's own access date 2026-10-24 and the
staged `recheck` prose was reduced to cadence tokens with the stripped text
preserved verbatim in `assimilation/recheck-prose-stripped.md`. Note: the
mirror's `used-by` targets were placeholders (the real entries had not landed;
`ExecAppendTransform` caveats) — the live-landed re-run is owed at append time.
The collision guard ran before any append: registry S001–S185 vs staged
S186–S317 → **0 collisions**, proven able to fail on an indented-row fixture
(`ExecCollisionGuard`).

**Re-open executed (no new row — considerthese disposition, at most one per
contract):** proposal 3 of `considerthese/2026-10-23.md` (the frozen
"latest file"; `2026-10-24.md` exists and is named — `ReviewReportContract` flag 7)
— "re-open one cited line first-hand, read-only." Executed by
`ScoutConsiderThese`: S177 (`hyprutils v0.14.2` `AnimationConfig.cpp:63-64`)
re-fetched 2026-10-24 → 2354 B, sha256 `dbb5d50a…` byte-identical to the row's
anchor; "if a child isnt overridden, set the values of the parent" — agree, no
erratum needed.

### REJECTS

1. **`corpus/knowledge/compositor-focus-manipulation-literature-r26.md`** —
   staged entry (row S201, arXiv:2604.18860), the fourth candidate considered
   this round (`CriticThemeScope` §2). **Reason:** out of province on three
   independent grounds — its claims are an X11 threat-model preprint (no
   owned-surface claim: PROVINCE owns the config plane and display behavior
   *on this host*); its own §3 states no Hyprland-0.56.2 measurement exists;
   its own UNK requires running an untrusted client, which the lane may never
   do (permanently unclosable here). Its `ground: F1` line borrows U1
   ("per-window rule effects") for a source that cannot bind to it. The same
   row is a `payload-absent` quarantine slice member (below), adding a
   fabrication-class flag to the province refusal. **Flip:** admit only if
   (a) `PROVINCE.md` gains a dated refinement owning compositor-security
   literature as a mado surface, or (b) the source is re-scoped as a
   *corroborating row* under an entry whose claims live on an owned surface
   (a host-measured focus-grab note citing S201 as background) — S201 then
   rides as a mined `used-by` source, never as a standalone entry.
2. **`https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/`**
   — the queue-guessed URL for the 0.56.0 dispatcher surface. **Reason:** HTTP
   404 at staging and re-verified live 2026-10-24
   (`ScribeEntryDispatcherSurface`); the real path is `/Basics/Dispatchers/`
   (admitted as S196). **Flip:** re-open as a new row only if it later answers
   200 with a scope not already inside S196.
3. **Claim-level rejects (not rows):** the staged keyword claim "`exec`
   documented on both" (M32-2), the staged "same dispatcher vocabulary" claim
   (M32-3), and the staged "only textual difference was the `name` header"
   meta-claim (M32-6) — each rejected-and-corrected in the scribe drafts.

### Quarantine verdicts

Slice derived by `ExecQuarantineSlice` (register read-only; its header and
`## By lane` totals are stale — the slice was re-derived by the prescribed awk
filter into `assimilation/quarantine-slice`, **13 data rows**: 6
`payload-absent` + 7 never-checked (2 could-not-fetch, 5 "named no locator").
The register is never edited; defects below are named, not repaired.

| id | register class | verdict (this round's hand-check, `ExecQuarantineSlice`) |
|---|---|---|
| S189 | payload-absent | **PRESENT, adoptable** — quote verbatim at `fetch/S189.bin:128` (`formatEvent`); checker miss (JSON-escape fold). This seat's own `grep -n` independently prints `128:` — "refuse-the-register-verdict, not the row" (`CriticSourcedClaim` concurs). |
| S195 | payload-absent | **PRESENT, adoptable** — both quotes verbatim in the packaged zh-cn Hyprland doc (markup-embedded text miss). |
| S201 | payload-absent | **PRESENT — adopt only on re-anchor** — quotes live in the paper's full LaTeX source (lines 97, 430), **not** the cited abstract page; anchor must move to full text. (Same S201 refused above on province grounds — quarantine and province verdicts agree the row as cited is unusable, for different reasons.) |
| S205 | payload-absent | **PRESENT, adoptable** — both quotes verbatim as the last two `interwikimap` entries (live 200 + lane artifact). |
| S224 | payload-absent | **ABSENT — refuse as quoted** — the cited `"updated_at": "2026-10-23T22:52:44Z"` is absent from the rewritten cache file (current `"2026-10-24T23:01:21Z"`); a rotating timestamp — **stale, not fabrication**. Fix: re-quote a stable field (`"version": 2,` verifies) or the current value. |
| S228 | payload-absent | **PRESENT under quote-normalization** — cited straight quotes `"…"` vs the page's curly quotes `“…”` at line 1519; adopt with the corrected curly-quote string. |
| S199 | could-not-fetch | **UNVERIFIABLE** — remote answers HTTP 521; lane reader-proxy artifact corroborates both quotes verbatim (not live-verified). |
| S200 | could-not-fetch | **UNVERIFIABLE** — same 521; artifact corroborates both quotes (incl. `hl.dsp.exec_cmd("hyprlock")`). |
| S209 | named no locator | **UNVERIFIABLE** (prose cell) — but the gate block *does* name a locator (`hyprland.log` under `<HIS>`); claim re-verified consistent on successor state (0 markers in the new instance's log). |
| S222 | named no locator | **UNVERIFIABLE** (prose cell) — gate locator `~/.local/bin/gkeep` verified PRESENT (both quotes verbatim). |
| S223 | named no locator | **UNVERIFIABLE** (prose cell) — gate locator `~/.local/bin/ai-usage` verified PRESENT. |
| S225 | named no locator | **UNVERIFIABLE** (prose cell) — journal locator re-verified on successor state (0 markers in current 718-line output). |
| S235 | named no locator | **UNVERIFIABLE** (prose cell) — HIS dir rotated; claim holds on live state (`.socket.sock`/`.socket2.sock` 755 socket). |

**Counts: PRESENT 5 · ABSENT 1 (S224) · UNVERIFIABLE 7.** Five of six
`payload-absent` rows are checker misses (JSON-escape, markup-embedded text,
curly-vs-straight quotes, abstract-vs-full-text anchor), not fabrications;
S224's rotating timestamp is the only genuinely absent payload — refused as
quoted, re-quotable.

Register defects named (unrepaired): the `## By lane` summary undercounts
mado (lists 6; real slice is 13 — it counts only §1); §2 mado id cells carry a
stray trailing backtick; §2's "the gate block named no locator" is inaccurate
for all five mado gate rows (each names a host path or journal unit — the
checker did not treat non-HTTP locators as locators).

### Search-log note

Candidate source set came pre-staged (campaign package `S186`–`S317` under
`shokuknow/merge/mado/`); this round's own searches were all negative-result
sweeps: the guessed 0.56.0 dispatcher URL → 404 (twice, recorded); registry id
sweep → 0 collisions (`ExecCollisionGuard`); sibling-lane probe across 20 lanes
(`socket2|.socket.sock|hyprctl dispatch`) → 0 same-surface hits, 12 lanes with
incidental non-IPC mentions (`ConnectorSiblingOverlap`); `PROVINCE.md` grep for
IPC/dispatcher terms → 0 (recorded as boundary context, not a defect —
`CriticThemeScope` rules the three entries in-province as documentation of an
owned surface). `considerthese` mining: `ScoutConsiderThese` audited the seven
proposals in `considerthese/2026-10-23.md` (verdicts: 1 implemented, 2 partial,
4 unimplemented) and executed the one unimplemented lane-implementable proposal
(proposal 3, the S177 re-open above).

## Frontier

**Moved.** The L1's own re-grounding of the five sources is done and
independently re-verified (fetches frozen, sha/byte counts exact;
`CriticSourcedClaim` byte-compares). The append block is schema-normalized and
mirror-validated exit 0; the collision guard is proven able to fail (0 real
collisions, non-empty on the indented fixture); the candidate set is
adjudicated (3 admits + province reject with flip); the considerthese contract
was mined **and** one proposal was executed in-round — the first executed
proposal, not just a pointer. The quarantine slice is hand-checked end-to-end
(5 PRESENT / 1 ABSENT-stale / 7 UNVERIFIABLE) — the mado register slice is
closed; its stale `## By lane` header is named, not edited. `ExecThemeHoldCheck`
settles the frontier question with a real sweep: **no note holds the
two-socket request/event contract** — request-path held only as a hyprctl `-i`
routing fact (`bind-table-r25.md`), event-path implied only by one socat
consumer (`remaining-planes-census.md`), grammar and framing held nowhere, and
`gate-standing-use`/`arc-synthesis` list the surface as UNKNOWN by name. The
C2 gate bites for real: `SimplifierEvidence` smoked
`quality/check-axis-scores.py` at tip `50e6a8f` → `checked=3 mismatched=2`
(calibration and operability STALE against the published line).

C1's predicate is dead (`CriticC1Predicate`; M32-7) — the round-30 precedent
applies: the claim stands on data + non-author review, never on the counter.
Two readings of the C2 premise adjudicated (ScoutLaneState MATCH×3 vs the
gate's mismatched=2): the published line's *after*-values are true; the line
itself is still a base-value line consumed as the lane's current
self-assessment — `CriticC2Predicate` attack-1 rules the stale-publication
claim **survives by convention evidence**, with a wording repair (name the
currency convention, not falsity). Its attacks 3/5 kill parts of the *frozen
predicate* instead (rfind locator shadowed by quotations; single-axis
controls) — same species as C1's dead predicate, charged as M32-13.

**Not moved.** `corpus/SOURCES.md` carries 0 of the five rows
(`grep -cE '^\|\s*S(186|196)\s*\|' corpus/SOURCES.md` → `0`) and the five-row
append + the S196 `teaches` erratum (M32-3) have not landed. The three
knowledge entries exist in the worktree **untracked** (the live counter
already reads `entries=3 rows=0 cited_entries=5` — M32-7's false-negative arm
proven on the real landing before the append); the IPC entry's landing copy
carries the `ReviewEntryIPC` corrections (M32-10/11) and the dispatcher-surface
copy carries the id-pointer fix (M32-12). The C2 counter is untracked
(M32-9); the axis table is unpublished-for-r32; the README frontier bullet
("dispatcher behavior") is not yet retired (`corpus/README.md` has a 2-line
uncommitted index edit at write time); one wave seat remains pending —
`ReviewEntryDispatch` (dispatchers entry unreviewed) — and can still move the
record. `RevengerPriorDefects` names the round-33 material: the r31 lesson
backfill + five UNCAPTURED criterion candidates. Per
`considerthese/2026-10-24.md`'s own debt line, no `tools/` or
`corpus/knowledge/` change had landed since round 27 — this round ends that
domain-drift streak *iff* the append lands. `round-31.md` was never filed
(`RevengerPriorDefects` row 1; `git cat-file -e <base>:corpus/lessons/round-31.md`
→ rc=128); this draft is the first round-32 lesson text and must not become
the second unfiled one — landing it is part of closure.
