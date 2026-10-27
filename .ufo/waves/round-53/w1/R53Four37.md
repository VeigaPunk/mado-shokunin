# R53Four37 — executable counter/fixture behaviour for frozen C1 and C2

Seat `R53Four37` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`ad4bf2059bcfafe63671d262222908ee1fe8001c` (lane HEAD, working tree clean except the untracked
round-53 wave directory). Axes in play: **operability** (C1 accountable instrument ledger) and
**coverage** (C2 proposition-grounded entry). Frozen claims read first:
`.ufo/waves/round-53/claims-frozen.md:5-7` (C1) and `:9-11` (C2), causal separation `:13`.
Routed r52 defects were read only as evidence: `corpus/lessons/round-52-verifier-spotcheck.md:36-40,69-75`.

This seat is an executor, not a non-author reviewer: nothing below is a source-truth *review*
verdict, and no seat report counts as one. No tracked lane file, script, template, state, fleet
file or shokuknow file was written; no git/jj mutation, commit, push, task, delegation or
background job was made in the lane. Scratch-only work, absolute paths, environment
`Python 3.14.8`.

## 0. Instruments built in scratch (deleted after this report)

| file | sha256 | what it is |
|---|---|---|
| `c1-r53-ledger-v3.py` | `fd21473d29ffd50d4c0b5c68bb462d7ea979020f91d57a78b1061da5333ef4bc` | C1 prototype: population, row uniqueness, resolvable non-self pointer with normalized identity + git-mode alias resolution, description context under two policies, `--selftest` |
| `c2-r53-prop-entry.py` | `926814a515b94c0c2c4eb06c78d8b7c31ece4c4265114bc873b9782c1595d5d9` | C2 prototype: table grammar, registry/pin/SHA binding, contiguous-quote-in-span, subject→enclosing-function binding, containment/sequence construct binding |
| `make-fixtures.py`, `make-c2-fixtures.py`, `make-alias-fixture.py` | `b869f8c6…`, `11ebe4ac…`, `e0156df3…` | fixture builders (C1 ledger byte sets, C2 corrected entry + six mutants, mode-120000 alias repo) |
| `run-c1-matrix.py`, `run-c2-matrix.py` | `5c718d3c…`, `3f664ef2…` | receipt drivers |

Both prototypes read every scored byte from `--rev` through `git show`/`ls-tree` (never the
working tree), write nothing, and refuse a `--work` inside the scored repository. Every fixture
commit asserted `git -C <fixture> rev-parse --show-toplevel` = the fixture directory first
(`.../fx`, `.../alias-fx`).

## 1. C1 — the target has no committed instrument at base; the pointer half is achievable, the context half is not

### 1.1 Base state (measured, no assumptions)

```
$ git -C <lane> ls-tree -r --name-only ad4bf2059bcfafe63671d262222908ee1fe8001c quality/counters/ | grep -Ec 'r5[23]'
0
$ git -C <lane> ls-tree -r --name-only ad4bf2059bcfafe63671d262222908ee1fe8001c | grep -E '^(tools/|quality/[^/]+\.py$|quality/counters/[^/]+\.py$)' | grep -v __pycache__ | wc -l
82
```

So the C1 target's "newly committed, scratch-aware counter" does not exist at the round base:
neither a `c1-r52` nor a `c1-r53` counter is committed, and only `quality/counters/c1-r51-ledger.py`
(82-row population, context-blind) is present. The r52 draft (`w1/C1CounterDesign/c1-r52-ledger.py`)
and the r52 working-tree rewrite were never committed (r52 closure measured the same absence,
`corpus/lessons/round-52-verifier-spotcheck.md:27-30`). **At base the C1 target is unmet, and the
production green arm can only be produced by the r51 predicate.**

### 1.2 Measured matrix — r51 (before) vs prototype (after) on identical fixture bytes

Fixtures were staged at `quality/tool-ledger.md` in a scratch clone, one commit each; the counter
under test scored that revision. `allself` and `generic-single` are the r52 forgery classes;
`F-all-committed` is the committed r52 forgery fixture
(`.ufo/waves/round-52/w2/Attack01/controls/F-all-forged.md`, copied byte-for-byte);
`F-all-v2` is a filter-aware forgery this seat built; `laundering-01..09` are the nine r52
self-reference spellings with the production pointer retained.

```
# production at base, r51 committed counter
$ python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work <scratch>
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c   exit=0

# production at base, prototype
C1_R53: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=10 policy=adjacent ledger=quality/tool-ledger.md verdict=TARGET_MISSED rev=ad4bf2059…   exit=1
C1_R53: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=2 policy=cooccur  ledger=quality/tool-ledger.md verdict=TARGET_MISSED rev=ad4bf2059…   exit=1
```

| fixture (rev) | r51 committed | prototype `adjacent` | prototype `cooccur` |
|---|---|---|---|
| production `ad4bf205` | **MET** (context-blind) | MISS `generic_desc=10` | MISS `generic_desc=2` |
| no-work control, r52 frozen bytes `dfcfd1c8` | MISS `uncovered=81 dup=1 bad_pointer=1 checker=failed` | MISS `uncovered=81 dup=1 bad_pointer=1 self_pointer=1 generic_desc=1` | same, `self_pointer=1 generic_desc=1` |
| all-self pointers `b4e7620f` | **MET** (82/82) | MISS `self_pointer=82 bad_pointer=82` | MISS `self_pointer=82 bad_pointer=82` |
| generic-single `2f8e4b97` | **MET** | MISS `generic_desc=82` | MISS `generic_desc=82` |
| F-all committed `e185c7e2` | **MET** | MISS `generic_desc=82` | MISS `generic_desc=82` |
| F-all-v2 (filter-aware) `5bf5744c` | **MET** | MISS `generic_desc=4` | **MET** `generic_desc=0` |
| laundering-01 `9d610b36` … -09 `52f5ebfb` | MET on 07 and 09; MISS elsewhere only via `checker=failed` | MISS `self_pointer=1` each (9/9) | MISS `self_pointer=1` each (9/9) |
| mode-120000 alias `b6b724f6` | n/a | n/a | MISS `self_pointer=1 bad_pointer=1`; accountable-doc twin **MET** |
| `--selftest` | `selftest=ok` | `C1_R53_SELFTEST: 16/16 passed` exit 0 | — |

Exact laundering acceptance by the committed r51 counter (reproducing the r52 bypass class, not a
new inference):

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <fx> --rev 2a1e7bb4… --work <scratch>
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=2a1e7bb41eb8863a0402acb78f412c86f088ab05   exit=0   # `/quality/tool-ledger.md` + production pointer
```

Prototype attribution on the frozen control (both defect classes named, not only coverage):

```
C1_R53: population=82 ledger_rows=2 uncovered=81 dup=1 dangling=0 bad_pointer=1 self_pointer=1 generic_desc=1 policy=cooccur ledger=quality/tool-ledger.md verdict=TARGET_MISSED rev=dfcfd1c8…   exit=1
```

Alias probe (git mode `120000`, target `../tools/alpha.py`):

```
alias_rev=b6b724f6f8f79b42519a419963e85e169753512e mode=120000
ledger-self.md -> bad_pointer=1 self_pointer=1 generic_desc=0 verdict=TARGET_MISSED exit=1
ledger-doc.md  -> bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET   exit=0
```

### 1.3 C1 findings

**C1-F1 (base state, operability).** The frozen target requires a *newly committed* counter
"with explicit selftest returns TARGET_MET on the production ledger, TARGET_MISSED on a no-work
control and each frozen forgery fixture, with exact population coverage and non-self pointers"
(`claims-frozen.md:5-7`). At `ad4bf205` no such counter is committed (`grep -Ec 'r5[23]'` → 0),
so the target cannot be scored at base; the only executable green arm is the context-blind r51
predicate, which returns MET on both forgery classes here (`allself`, `generic-single`, `F-all`,
`F-all-v2`) and on two laundering spellings. This is a *measured* reproduction of the r52 routed
finding, not a restatement of it.

**C1-F2 (pointer/coverage half is achievable).** The prototype closes the whole measured pointer
family at population 82 with no false positive on production: normalized identity (case, leading
`/`, `./`, repeated slashes, `:N`/`:x` suffix, `#fragment`, basenames, symlink target) catches all
nine r52 laundering spellings plus the mode-120000 alias; the frozen control is charged
`self_pointer=1` and `generic_desc=1` as well as coverage; the accountable-document twin stays
MET; population is derived independently of the ledger and equals 82. The r51 counter returns MET
on all-self (82/82) and on generic-single, so the *before* state is real and the delta is
attributable to the normalization/identity rules, not to the fixture.

**C1-F3 (context half cannot satisfy both arms).** The description clause is a lexical phrase
binder, and the two arms pull in opposite directions at the round base:

- strict adjacency rejects **10/82** production rows; the looser co-occurrence rule still rejects
  **2/82** production rows, and both rows are legitimate paraphrase summaries:
  `quality/counters/c1-r48-terminal-cache.py` — "PRED-C1-r48, superseded by v2: adds the
  warm-cache path of the terminal-selection prediction to the round-47 scoring." (bytes say
  "predicts which terminal … picks, INCLUDING the warm cache"; `warm cache` is filtered as
  own-name vocabulary because `cache` is in the instrument's filename) and
  `quality/check-tool-ledger.py` — "Derives the tracked-instrument population at a revision and
  checks its accountability ledger." (the pairing `accountability ledger` is excluded as generic
  vocabulary).
- the only rule that accepts 80/82 production rows (`cooccur`) accepts a semantically empty
  forgery **82/82**: `F-all-v2` keeps every production pointer cell verbatim and writes
  `Generic note text <pair> baseline.` where `<pair>` is any non-shebang adjacent word pair of
  that instrument's bytes chosen to satisfy the counter's own filters (e.g.
  `Generic note text fail closed baseline.`, `Generic note text static resolver baseline.`).
  Verdict line: `generic_desc=0 … verdict=TARGET_MET`.

Tightening the filters to reject the last two legitimate summaries removes the very pair
vocabulary the real descriptions depend on; loosening to accept them admits the forgery. There is
no setting of this clause shape that returns production MET *and* the forgery class MISSED — the
residual is the class, not one fixture. "Instrument-specific functional context" is a semantic
requirement (the frozen text itself says the check is structural, not semantic proof — the two are
in tension here).

**C1-F4 (unbound acceptance criterion).** "Each frozen forgery fixture" has no referent this
round: `claims-frozen.md` names no fixture set, `.ufo/waves/round-53/` carries no `controls/` or
fixture manifest, and the r52 controls were never frozen into r53. A counter cannot be shown to
miss "each" member of an unenumerated set; the criterion needs a committed fixture manifest (byte
hashes) before any counter can be accepted against it. Related precondition: committing the new
counter adds one population file (82→83), so its own ledger row and a self-pointer-free pointer
must land in the same cut-over (r52 measured the same arithmetic; `w2/Attack02.md` P17).

**C1-F5 (prototype limits, stated).** The context clause is lexical by construction; its filters
are a deny-list and a forger who reads them can satisfy them (`F-all-v2`). The counter does not
check pointer *quality* beyond identity (a shared registry document naming all basenames still
passes; r52 P14). It also treats any path token that resolves and names the row as evidence; a
cycle of two documents satisfies it (r52 P13). These are claim-boundary residuals, not measured
counter defects.

## 2. C2 — old r52 entry rejects on exactly P16/P17/P18; an append-only correction accepts

### 2.1 Pinned bytes (committed fetch, checksum-verified this round)

```
$ sha256sum -c SHA256SUMS      # .ufo/waves/round-52/fetch/
Hyprland-ConfigActions.cpp … OK
Hyprland-ConfigActions.hpp … OK
Hyprland-KeybindManager.cpp … OK
Hyprland-legacy-DispatcherTranslator.cpp … OK
exit=0
```

Located lines (pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f`; URLs from the registry
rows S370/S371, access date 2026-10-27, `corpus/SOURCES.md:320-321`):

```
531: static SDispatchResult sendshortcut(const std::string& args) {
532:     CVarList2 ARGS(args, 3);
533:     if (ARGS.size() != 3)
534:         return {.success = false, .error = "sendshortcut: invalid args"};
565:             for (xkb_keycode_t kc = keycode_min; kc <= keycode_max; ++kc) {
566:                 xkb_keysym_t sym = xkb_state_key_get_one_sym(ks, kc);
571:             }
573:             if (!keycode)
574:                 return {.success = false, .error = "sendshortcut: key not found"};
591: static SDispatchResult sendkeystate(const std::string& args) {
592:     CVarList2 ARGS(args, 4);
593:     if (ARGS.size() != 4)
594:         return {.success = false, .error = "sendkeystate: invalid args"};
619:     auto result = sendshortcut(modifiedArgs);
621:     if (keyState == 2 && result.success)
622:         result = sendshortcut(modifiedArgs);
---
1554:     g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
1556:     if (S.m_passPressed == 1) {
1557:         if (!isMouse)
1558:             g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
1576:     g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
```

Confirmed defects (measured, matching the r52 routed finding):

- **P16 spliced.** The quoted text joins line 1554 (`sendKeyboardMods(modMask, 0, 0, 0);`) and
  line 1558 (`sendKeyboardKey(S.m_timeLastMs, key - 8, …PRESSED);`) with one space; lines 1555
  (blank), 1556 (`if (S.m_passPressed == 1) {`) and 1557 (`if (!isMouse)`) stand between them, so
  the joined quote is nowhere contiguous in `Hyprland-ConfigActions.cpp`.
- **P17 misattributed.** The proposition says `sendshortcut`'s repeat branch; lines 619–622 lie
  inside `sendkeystate` (591–627, closing at `626: return result; 627: }`), while
  `sendshortcut` closes at 589. The delegate call is `sendshortcut`, the enclosing parser is
  `sendkeystate`.
- **P18 mislocalized.** The loop closes at 571; 573–574 are the post-loop `if (!keycode)` guard.
  The return at 574 is *after* the scan, not inside it.

### 2.2 Counter results on the old bytes, an absent entry, corrected bytes, and six single-defect mutants

Old entry at base (`corpus/knowledge/hyprland-synthetic-dispatch-r52.md`):

```
$ python3 -I c2-r53-prop-entry.py --repo <lane> --rev ad4bf205… --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md --work <scratch>
C2_R53: a ok=1 entry=corpus/knowledge/hyprland-synthetic-dispatch-r52.md indexed=1
C2_R53: b ok=1 props=18 grammar=1 word_cap=1 support=1 distinct=1
C2_R53: c ok=1 miss=none
C2_R53: d ok=0 miss=P16:quote_not_contiguous
C2_R53: e ok=0 miss=P17:subject(expected=sendshortcut owner=sendkeystate line=621)
C2_R53: f ok=0 miss=P18:inside_loop_claim_not_in_loop(line=574)
C2_R53: pins=4 quotes_bound=17/18 subject_ok=16/18 construct_ok=15/18
C2_R53: entailment=not-checked (outside non-author review)
C2_R53: clauses=abcdef clauses_met=3 admitted=0/1 verdict=TARGET_MISSED rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
exit=1
```

The correction is append-only: the old bytes stay and a `## Proposition map (round-53 correction)`
section carries P16 (1554–1558, contiguous call), a new P16b (1576 clear call), P17 re-attributed
to `sendkeystate` (619–622), and P18 re-scoped to the post-loop guard (573–574). The counter
scores the last proposition-map section (frozen with the grammar).

| arm (fixture rev) | clauses met | miss |
|---|---|---|
| absent entry (no-work) | 0/6 | `a ok=0 entry=absent` |
| old entry `ad4bf205` | 3/6 | d P16, e P17, f P18 |
| corrected `2b2ae813` | **6/6 MET** `props=19 quotes_bound=19/19 subject_ok=19/19 construct_ok=19/19` | none |
| m1 P16 spliced `bb5ac16b` | 3/6 | `P16:quote_not_contiguous` |
| m2 P17 subject→`sendshortcut` `60d7c278` | 4/6 | `P17:subject(expected=sendshortcut owner=sendkeystate line=621)` |
| m3 P18 "inside the scan" `ea565b05` | 5/6 | `P18:inside_loop_claim_not_in_loop(line=573)` |
| m4 P17 span→557-566 `e31ca2ca` | 3/6 | `P17:quote_outside_span(621-622 not in 557-566)` |
| m5 P16 quote >25 words `d2a1938c` | 2/6 | `b word_cap=0` and `P16:quote_not_contiguous` |
| m6 P01 row→S999 `11e4d0c9` | 2/6 | `P01:row_absent` |

The committed r52 draft counter cannot measure this entry at all: it fails on its own grammar,
not on a defect —

```
$ python3 -I .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py --repo <lane> --rev ad4bf205… --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md --fetch-root .ufo/waves/round-52 --work <scratch>
C2_R52: c ok=0 rows_bound=0/18 … miss=P01:anchor_no_fetch_root,…
C2_R52: d ok=0 quotes_bound=0/18 … miss=P01:pin_file_absent(Hyprland-legacy-DispatcherTranslator.cpp),…
C2_R52: clauses=abcde clauses_met=2 admitted=0/1 verdict=TARGET_MISSED rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
exit=1
```

Its clause (c) requires the registry anchor cell to name the fetch root, while the landed rows
S370–S373 name the file plus the fetch SHA256; so `rows_bound=0/18` is a grammar mismatch, exactly
the failure class r52 measured (`corpus/lessons/round-52-verifier-spotcheck.md:38-40`). A C2
counter for this entry must accept the row grammar that is actually committed.

### 2.3 C2 findings

**C2-F1 (defects confirmed on pinned bytes, not inferred).** P16 quote is spliced across
1554/1558 with 1555–1557 elided; P17's subject is wrong by function span (619–622 ⊂
`sendkeystate` 591–627, not `sendshortcut` 531–589); P18's return at 574 is after the loop that
closes at 571. All three are locally reproducible from the committed fetch bytes with
`sha256sum -c` exit 0.

**C2-F2 (structural discrimination is achievable for the three named defects).** A frozen counter
with quote-contiguity + quote-in-span + subject→enclosing-function + containment/sequence binding
rejects the old bytes on exactly d/e/f and accepts the append-only correction at 19 propositions
6/6, with six single-defect mutants isolating b/c/d/e/f. The accept arm moves no pointer/row bytes:
it reuses S370–S373 and the same fetch SHA256 values, so no claim of expansion credit attaches
(the frozen claim's own condition) and no new external source was fetched.

**C2-F3 (counter limits that a frozen r53 counter must state).**
- Multi-span pins are a bounding-box over-approximation: the old P16 anchor `1554-1558,1576`
  admits any quote line in 1554–1576; only the contiguity clause rejects. The correction splits
  the span instead of relying on that.
- The subject clause keys on a function name carried in backticks (or `name's`); a misattribution
  written without that shape evades it. It is a binding check, not entailment.
- Scoring the *last* `## Proposition map` section makes the append-only form work, but it also
  means a second section can shadow the first; the non-author review remains the only defence
  that the scored section is the claimed one.
- Row grammar coupling is load-bearing (r52 draft counter, §2.2): the counter must read the
  committed `| ID | Proposition | Source row | Pin:anchor | Quote | Support class | Why |` table.

**C2-F4 (review status).** My source-truth check is a seat measurement against committed bytes,
not the independent non-author review the frozen claim requires; that arm is still owed, and
until it lands the correction is unadmitted.

## 3. Routed r52 defects, as evidence only

`.ufo/waves/round-52/` holds the r52 controls and the falsification reports that produced the routed
items. Re-executed here on identical bytes: the r51 counter is MET on all-self (82/82), on the
one-sentence generic ledger, on F-all and on F-all-v2, and MET on the `/quality/tool-ledger.md`
(laundering-07) and `Quality/tool-ledger.md` (laundering-09) spellings; it is MISS on the frozen
no-work control and on the other seven laundering spellings. That reproduces the r52 bypass class
rather than assuming it; the attribution (four competing clauses on the committed control;
two-grammar disagreement) comes from `w1/MistakeMiner.md:2.1` and is not re-measured here.

## 4. Boundaries, risks, cleanup

- Writes: this report only. No tracked lane file, fleet file, script, template, state, watchdog or
  shokuknow write. At this seat's lane-state check, `git -C <lane> status --porcelain` printed only
  `?? .ufo/waves/round-53/`; later in the wave the lane also shows ` M corpus/SOURCES.md` and
  `?? corpus/lessons/round-53.md`, which are concurrent sibling seats' writes, not this seat's.
- Executions: stdlib Python prototypes against committed git objects and two scratch fixture repos
  (`fx` clone of the lane at base; `alias-fx` three-file repo). No live read, process/compositor
  probe, package query, input capture, screenshot, producer run, network fetch, install or update.
  No package/tool transaction was executed, so no tool-ledger entry is owed.
- Fixture repos are scratch-only and are deleted with the rest of `/fast/scratch/hyaku/mado-r53/R53Four37`;
  disk was checked before use (`/fast` 593 G free).
- Risks that matter for the round: (1) committing a new C1 counter without a frozen fixture
  manifest makes "each frozen forgery fixture" unscoreable; (2) the context clause's green arm
  fails on 2–10 real rows at base, so a frozen threshold must be chosen and justified before data;
  (3) the C2 accept arm depends on the last-table scoring rule and on the row grammar actually
  committed — both must be frozen with the counter; (4) entailment and the non-author review are
  outside every counter here.

## Report trailer

**Attacked predicate.** C1 frozen target: newly committed, scratch-aware counter with selftest,
production MET, no-work control and every frozen forgery fixture MISSED, exact population coverage
and non-self pointers (`claims-frozen.md:5-7`). C2 frozen target: append-only correction of P16
(spliced quote), P17 (misattributed subject), P18 (mislocalized anchor), with a frozen counter
rejecting the old bytes and accepting the corrected entry on quote/pin/proposition bindings
(`claims-frozen.md:9-11`).

**Exact command/output.** Reproduced in §1.1–§1.2, §2.1–§2.2 above, verbatim, with exit codes:
population derivation `82`; `ls-tree quality/counters | grep -Ec 'r5[23]'` → `0`; r51 production
`C1_R51: … verdict=TARGET_MET` exit 0; prototype production `generic_desc=10 policy=adjacent` /
`generic_desc=2 policy=cooccur`, both `TARGET_MISSED`; no-work control `self_pointer=1 generic_desc=1
uncovered=81 dup=1`; all-self `self_pointer=82`; generic-single and F-all `generic_desc=82`;
F-all-v2 `TARGET_MET` under `cooccur`; laundering 9/9 `self_pointer=1`; alias `self_pointer=1`
vs accountable twin MET; `C1_R53_SELFTEST: 16/16 passed`. C2: old entry `clauses_met=3`
(d P16, e P17, f P18), absent entry `0/6`, corrected `6/6 MET props=19`, mutants 2–5/6 each with
the named clause; r52 draft counter `clauses_met=2`, `rows_bound=0/18`.

**Newly opened source.** Pinned Hyprland 0.56.2 bytes at commit
`efb50993780079460b0cbed1363e2166a2de1d9f`, opened locally from the committed fetch copies
(`.ufo/waves/round-52/fetch/`, `sha256sum -c SHA256SUMS` exit 0) on 2026-10-27 — no network fetch.
URLs per registry rows `corpus/SOURCES.md:320-321`:
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`
and `…/src/config/shared/actions/ConfigActions.cpp`. Located quotes grounding the findings:
DispatcherTranslator.cpp:531-535 (`static SDispatchResult sendshortcut(const std::string& args) {` /
`CVarList2 ARGS(args, 3); if (ARGS.size() != 3)`), :565-574 (`for (xkb_keycode_t kc = keycode_min;
kc <= keycode_max; ++kc) {` … `}` at 571, then `if (!keycode)` / `return {.success = false, .error
= "sendshortcut: key not found"};` at 573-574), :591-594 (`static SDispatchResult
sendkeystate(const std::string& args) {` / `CVarList2 ARGS(args, 4); if (ARGS.size() != 4)`),
:619-622 (`auto result = sendshortcut(modifiedArgs);` / `if (keyState == 2 && result.success)` /
`result = sendshortcut(modifiedArgs);`); ConfigActions.cpp:1554 (`sendKeyboardMods(modMask, 0, 0,
0);`), :1556-1558 (`if (S.m_passPressed == 1) {` / `if (!isMouse)` / `sendKeyboardKey(S.m_timeLastMs,
key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`), :1576 (`sendKeyboardMods(0, 0, 0, 0);`).

Report path (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`):
`.ufo/waves/round-53/w1/R53Four37.md`
