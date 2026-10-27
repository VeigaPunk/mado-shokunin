# R53One1 — executable counter/fixture behavior for C1 and C2 at base `ad4bf20`

Seat `R53One1` (leaf executor). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c` (asserted `git rev-parse HEAD`; lane work
tree clean apart from untracked `.ufo/waves/round-53/`). Wave `w1`, round 53.
Axes attacked: **operability** (C1, accountable instrument-ledger counter) and **coverage**
(C2, proposition-bound r52 dispatcher entry repair). No live reads, no package queries, no
producer execution, no compositor/host mutation, no screenshots, no input capture. Source
checkout read-only; no commits, no jj, no background jobs, no installs, no pacman transaction.
Scratch `/fast/scratch/hyaku/mado-r53/R53One1/` only, removed before yield; `/fast` had
592 GiB free (27 % used), no ENOSPC.

## Predicates attacked (quoted from `.ufo/waves/round-53/claims-frozen.md`)

- **C1** — “a newly committed, scratch-aware counter with explicit selftest returns
  TARGET_MET on the production ledger, TARGET_MISSED on a no-work control and each frozen
  forgery fixture, with exact population coverage and non-self pointers. This is a bounded
  structural accountability check, not semantic proof.”
- **C2** — “append-only correction clearly repairs those three propositions against opened
  pinned source bytes; a frozen counter rejects the old bytes and accepts corrected entry
  with quote/pin/proposition bindings; independent reviewer checks source truth.”

The r52 spot-check's routed evidence is `corpus/lessons/round-52-verifier-spotcheck.md:38`
(P16 spliced, P17 misattributed, P18 mislocalized). This seat re-measured all three against
the pinned bytes rather than adopting that text.

## Result summary

| Claim | State at base `ad4bf20` | Measured discriminator | Target met at base? |
|---|---|---|---|
| C1 | only `quality/counters/c1-r51-ledger.py` exists; no `c1-r52-*`/`c1-r53-*` committed (`git ls-tree … quality/counters \| grep -c 'r5[23]'` → `0`) | r51 counter: production `82/82 TARGET_MET`; accepts generic-description, self-pointer and combined no-work ledgers (`clean=PASS`); rejects duplicate/bad-pointer/placeholder | **no** — new counter and frozen forgery fixtures absent |
| C2 | r52 entry indexed but uncorrected (`sha256 bee0d143…`); no `c2-r52/r53` production counter committed; no r53 entry, `fetch/`, or `registration.md` | P16 quote absent at pin; P17 pin inside `sendkeystate`, not `sendshortcut`; P18 return outside the scan loop. Draft r52 proposition counter: `17/18` quote bindings — only P16 rejected; a P16-only quote repair yields `18/18` while P17/P18 stay defective | **no** — correction and frozen counter absent |

## C1 — r51 counter at the base revision

Command and output (verbatim; clone/build work under scratch, removed by the counter):

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py \
    --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
    --work /fast/scratch/hyaku/mado-r53/R53One1/c1-prod
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ad4bf2059bcfafe63671d262222908ee1fe8001c)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
exit=0
```

Population breakdown at the rev: 17 `tools/*`, 19 `quality/*.py`, 46 `quality/counters/*.py`
= 82. The counter has no selftest of its own; its `selftest=ok` is
`quality/check-tool-ledger.py --selftest` (50/50). Production ledger has zero self-pointer
rows (its only `quality/tool-ledger.md` occurrence is prose at line 3).

### C1 bypass replay — the counter's own `parse_rows`/`describe` on forged ledgers

No commit is permitted, so each fixture was fed through the same module functions the CLI
uses for its independent measurement while population and pointer resolution still read the
real lane repo at the frozen rev (read-only `git ls-tree`/`git show`). Harness:
`probe_c1_r51_predicate.py` in scratch. Verbatim output:

```
C1_R51_SIM: pop=82 prod_rows=82 rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
C1_R51_SIM: variant=production       population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=0 clean=PASS
C1_R51_SIM: variant=generic-desc     population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=0 clean=PASS
C1_R51_SIM: variant=self-pointer     population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=0 clean=PASS
C1_R51_SIM: variant=no-work          population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=0 clean=PASS
C1_R51_SIM: variant=dup-row          population=82 ledger_rows=83 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=1 clean=FAIL
C1_R51_SIM: variant=bad-pointer      population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=71 empty_desc=0 dup=0 clean=FAIL
C1_R51_SIM: variant=placeholder-desc population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=82 clean=FAIL
```

`no-work` is the population-complete control the r53 claim names: 82 unique rows, description
`tool`, pointer `quality/tool-ledger.md` (the ledger contains every instrument basename, so the
self-pointer resolves). `generic-desc` keeps the production pointers and replaces only the
description; `self-pointer` keeps the production descriptions and replaces only the pointer.
Both defect classes and their conjunction pass the r51 predicate; duplicate, unresolved
pointer and placeholder-description forgeries are caught. This reproduces the frozen “Before”
and the r52 verifier's bypass class with a population-complete shape (the r52 committed control
is only 2 rows — see below).

### C1 target-shape probe (scratch, not committed)

A ~7 KB scratch probe (`c1-r53-probe.py`) adds exactly the two missing checks — non-self
pointer (the ledger path is never an accepted pointer) and instrument-specific context
(description must be ≥4 words and share ≥1 ≥5-character token with the instrument's own bytes)
— plus exact coverage, duplicate and placeholder checks, and an explicit `--selftest`.
Selftest, verbatim:

```
SELFTEST case=good         want=PASS got=PASS {'uncovered': 0, 'dangling': 0, 'bad_pointer': 0, 'generic_desc': 0, 'dup': 0, 'self_pointer': 0}
SELFTEST case=generic-desc want=PASS got=PASS {'uncovered': 0, 'dangling': 0, 'bad_pointer': 0, 'generic_desc': 1, 'dup': 0, 'self_pointer': 0}
SELFTEST case=self-pointer want=PASS got=PASS {'uncovered': 0, 'dangling': 0, 'bad_pointer': 1, 'generic_desc': 0, 'dup': 0, 'self_pointer': 1}
SELFTEST case=dup          want=PASS got=PASS {'uncovered': 0, 'dangling': 0, 'bad_pointer': 0, 'generic_desc': 0, 'dup': 1, 'self_pointer': 0}
SELFTEST case=missing      want=PASS got=PASS {'uncovered': 1, 'dangling': 0, 'bad_pointer': 0, 'generic_desc': 0, 'dup': 0, 'self_pointer': 0}
C1_R53_PROBE: selftest=ok ratio=5/5
selftest_exit=0
```

Production path (ledger read from the rev, not the working tree) and the forgery matrix,
verbatim:

```
C1_R53_PROBE: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 generic_desc=0 self_pointer=0 dup=0 verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
  production exit=0
C1_R53_PROBE: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 generic_desc=82 self_pointer=0 dup=0 verdict=TARGET_MISSED rev=ad4bf20…
  generic-desc exit=1
C1_R53_PROBE: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=82 generic_desc=0 self_pointer=82 dup=0 verdict=TARGET_MISSED rev=ad4bf20…
  self-pointer exit=1
C1_R53_PROBE: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=82 generic_desc=82 self_pointer=82 dup=0 verdict=TARGET_MISSED rev=ad4bf20…
  no-work exit=1
C1_R53_PROBE: population=82 ledger_rows=83 uncovered=0 dangling=0 bad_pointer=0 generic_desc=0 self_pointer=0 dup=1 verdict=TARGET_MISSED rev=ad4bf20…
  dup-row exit=1
C1_R53_PROBE: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=71 generic_desc=0 self_pointer=0 dup=0 verdict=TARGET_MISSED rev=ad4bf20…
  bad-pointer exit=1
C1_R53_PROBE: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 generic_desc=82 self_pointer=0 dup=0 verdict=TARGET_MISSED rev=ad4bf20…
  placeholder-desc exit=1
```

So the C1 target shape is executable and discriminating on a population-complete ledger:
production `TARGET_MET`, each forgery class `TARGET_MISSED`, explicit selftest green. This is a
feasibility receipt in scratch, not the round's committed counter and not a frozen fixture set.

### The committed r52 C1 controls cannot isolate the named defects

`.ufo/waves/round-52/controls/c1-do-nothing.md` is 4 lines / 2 duplicate rows of
`tools/mado-verify.sh`; its “self-pointer” text sits in the description cell and its pointer
cell is `nothing | generic accountability pointer to this ledger itself`.
`.ufo/waves/round-52/controls/c1-row-context-control.md` is 2 duplicate rows with description
`A tool.` and pointer `PROVINCE.md:20`. Under the r51 predicate both are
`uncovered=81 dup=1` (and `bad_pointer=1` for do-nothing) against an 82-file population, and
under the scratch probe both are `uncovered=81 dup=1 generic_desc=1`. A counter's red verdict
on either control is therefore attributable to coverage/duplication before the non-self or
context checks are reached — the r52 registration's “fail … specifically for self-pointer/context
defects” is not exercised by the committed control shape.

## C2 — the three r52 propositions against the pinned bytes

Pins: `.ufo/waves/round-52/fetch/`, revision `efb50993780079460b0cbed1363e2166a2de1d9f`,
opened 2026-10-27 (README + `SHA256SUMS`; `sha256sum -c SHA256SUMS` → all 5 files `OK`).
Entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` at the rev hashes
`bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078`, identical in the working
tree; index row is `corpus/README.md:80`; 18 propositions `P01–P18`.

Verbatim measurement (scratch `verify_three_defects.py`):

```
P16 anchor 1554-1558:
  1554:    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
  1555:
  1556:    if (S.m_passPressed == 1) {
  1557:        if (!isMouse)
  1558:            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
P16 quote_collapsed_in_span=False
P16 clear_line_1576_in_quote=False
P16 clear_line=1576:g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
P17 sendshortcut_span=531-589 sendkeystate_span=591-627
P17 quote_line_621_inside_sendshortcut=False inside_sendkeystate=True
P17 sendshortcut_lines_mentioning_keyState_or_repeat=none
P17 repeat_branch_line=621 inside_sendkeystate=True
P18 scan_loop=565-571 return_line=574 inside_loop=False
P18 return_preceding_lines:
  571:            }
  572:
  573:            if (!keycode)
  574:                return {.success = false, .error = "sendshortcut: key not found"};
P18 return_after_loop_before_else=True
```

Located quotes (pinned bytes, `Hyprland-ConfigActions.cpp` / `Hyprland-legacy-DispatcherTranslator.cpp`):

- **P16 — spliced quote.** The quoted text joins `:1554` and `:1558`; `:1555-1557`
  (`if (S.m_passPressed == 1) { if (!isMouse)`) are elided, so the joined quote occurs nowhere
  contiguously (`quote_collapsed_in_span=False`). The “then clears” half rests on `:1576`,
  which is outside the quoted bytes. The proposition's substance (mods → key → clear) matches
  the code; the *quote* does not.
- **P17 — misattributed subject.** `sendshortcut` spans `531-589` and contains no
  `keyState`/repeat line. The quoted `if (keyState == 2 && result.success)` at `621-622` is
  inside `sendkeystate` (`591-627`), so “`sendshortcut`'s repeat branch” is false.
- **P18 — mislocalized.** The `key not found` return at `573-574` sits after the scan loop
  `565-571` (loop closes at `571`), inside the cache-miss `if` that opens before `559`; “inside
  the scan” is false.

### Counter behavior on those bytes (r52 draft proposition counter)

Committed wave artifact `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`
(r52 commit `56d6e705…`), run at the base rev with the real fetch root:

```
$ python3 -I …/c2-r52-proposition-entry.py --repo <lane> --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
    --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md \
    --fetch-root .ufo/waves/round-52/fetch --work <scratch>/work2
C2_R52: a ok=1 index_row=`knowledge/hyprland-synthetic-dispatch-r52.md` (round 52;...
C2_R52: b ok=1 propositions=18 ids=18 forms=table
C2_R52: c ok=0 rows_bound=0/18 distinct_rows=0 miss=P01:anchor_no_fetch_root,…
C2_R52: d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 policy=whitespace-collapsed pins_prior_equal=4/17 miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
C2_R52: e ok=0 prose_rows=4 prop_rows=4 manifest_rows=0 miss=P01:id_not_referenced,…
C2_R52: entailment=not-checked (outside non-author review)
C2_R52: clauses=abcde clauses_met=2 admitted=0/1 verdict=TARGET_MISSED rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
exit=1
```

`clause_d` (`c2-r52-proposition-entry.py:657-725`) compares the quoted words,
whitespace-collapsed, against the cited line span only. Its bound set names
`P01…P15,P17,P18` — i.e., **P17 and P18's defective bytes are admitted**; only P16 is rejected.
The same run's clause (`b`) also admits all 18 propositions structurally.

A P16-only quote repair (replace the spliced quote with the verbatim `:1554` line, leaving
P17/P18 untouched) makes that clause pass completely, verbatim:

```
C2_DRAFT: p16_only_repair_changed=True
C2_DRAFT: p16_only_repair clause_d=1 quotes_bound=18/18 quotes_raw=7/18 pins=4 policy=whitespace-collapsed pins_prior_equal=4/18
C2_DRAFT: p16_only_repair_bound_ids=P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18
C2_DRAFT: p17_still_present=True p18_still_present=True
```

Consequence for the C2 predicate: a quote/pin-binding counter *does* reject the old entry
(P16), but it cannot reject the P17 or P18 defect classes — those quotes are verbatim at their
pins. “A frozen counter rejects the old bytes” is therefore satisfiable only as “rejects the
old entry via P16” unless the r53 counter adds a binding the r52 shape lacks (for example a
subject/enclosing-symbol binding or a clause-relative location binding). The claim does not
name such a binding. Separately, clause (c) fails all 18 rows because the `SOURCES.md` anchors
(`S370`–`S373`, lines 320-323) name the pin and revision but not a fetch-root path, and clause
(e) fails because this entry's prose does not reference proposition ids; both failures are
independent of the three routed defects.

## Artifacts absent at base (measured)

- `git ls-tree -r --name-only ad4bf20 quality/counters | grep -c 'r5[23]'` → `0`; the only
  ledger counter is `c1-r51-ledger.py`, the only dispatcher C2 counter is
  `c2-r51-dispatch-entry.py`.
- `git ls-tree -r --name-only ad4bf20 corpus/knowledge | grep -c 'r53'` → `0`.
- `.ufo/waves/round-53/` contains only `claims-frozen.md`, `w1-spec.json`, `w1-dispatch.json`,
  `w1.ready*` and the `w1/` reports: no `registration.md`, no `controls/`, no frozen forgery
  fixture set, no `fetch/`.

## Risks and blockers (observations, no judgment)

1. **Freeze-before-data.** Round-53 has no `registration.md` / controls / frozen fixture set at
   measurement time, while `claims-frozen.md` requires “Control design and measurement must be
   frozen before data.” The fixtures in this report are seat-local scratch constructions, not
   the round's freeze; they must not be treated as the required frozen controls.
2. **C1 control shape.** Both committed r52 C1 controls are two-row, duplicate, non-population
   ledgers; a counter can fail them for coverage alone, so they cannot demonstrate the
   non-self/context checks the predicate names. A round-53 control needs one unique row per
   population file (82 at this rev) with the defect in the pointer/description cell.
3. **C2 defect discrimination.** No quote/pin-binding counter distinguishes P17/P18 from sound
   propositions; the old-entry rejection is carried entirely by P16. If the r53 counter is to
   reject all three defect classes, its binding grammar must be extended, and that extension
   needs to be frozen before measurement.
4. **Reviewer boundary.** This seat is an executor, not a non-author reviewer; nothing here is
   an admission or an entailment verdict. Source truth was re-measured directly against the
   pinned bytes and agrees with `corpus/lessons/round-52-verifier-spotcheck.md:38`.
5. **Source-opens.** No round-53 `fetch/` or new `S###` rows exist, so “an admitted entry rests
   on a source row opened this round” cannot be satisfied by a correction that reuses S370–S373;
   per the claim, no expansion credit can be claimed from this correction path.

## Trailer — paths (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`)

Read/opened (read-only):

- `quality/counters/c1-r51-ledger.py`
- `quality/check-tool-ledger.py`
- `quality/tool-ledger.md`
- `.ufo/waves/round-52/controls/c1-do-nothing.md`
- `.ufo/waves/round-52/controls/c1-row-context-control.md`
- `.ufo/waves/round-52/registration.md`
- `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`
- `.ufo/waves/round-52/fetch/{Hyprland-ConfigActions.cpp,Hyprland-legacy-DispatcherTranslator.cpp,README.txt,SHA256SUMS}`
- `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`
- `corpus/README.md`
- `corpus/SOURCES.md`
- `corpus/lessons/round-52-verifier-spotcheck.md`
- `.ufo/waves/round-53/claims-frozen.md`
- `.ufo/waves/round-53/w1-spec.json`

Written (only):

- `.ufo/waves/round-53/w1/R53One1.md`

Scratch (removed before yield): `/fast/scratch/hyaku/mado-r53/R53One1/` — harnesses
`c1-harness/probe_c1_r51_predicate.py`, `c1-harness/c1-r53-probe.py`,
`c1-harness/gen_fixtures.py`, `c2-checks/verify_three_defects.py`, fixture ledgers and counter
work dirs.

Report: .ufo/waves/round-53/w1/R53One1.md
