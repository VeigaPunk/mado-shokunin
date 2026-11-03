# R66ScribeLesson — report

Seat: mado round 66, wave w1, scribe (lesson draft). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, observed HEAD
`ed980316e330703030d0c17b2a7098e058295b99`, frozen base
`eafd500fa7be76dca59e729435e231a5032cc037`, date 2026-11-03. Leaf: no subagents, no installs, no
pacman, no git/jj mutation in the lane or any sibling, no host/config/service/compositor change, no
credential/session reads, no r56-era material. Scratch `/fast/scratch/hyaku/mado-r66/R66ScribeLesson/`
was not created (no fixture was needed).

## Changed drafts

This seat changed no production file: it wrote no lane file outside
`.ufo/waves/round-66/w1/R66ScribeLesson/` plus the seat-spec report copy at
`.ufo/waves/round-66/w1/R66ScribeLesson.md`. The drafts are the lesson and the four append snippets
listed above; none is installed at its destination.

## Gates

No gate was run or claimed by this seat. Harness diagnostics ran (not by this seat): C1 and C2 each
baseline 1/4, candidate 4/4 in `--candidate-draft` mode — pre-integration diagnostics, not the
post-integration `--rev` score, and for C2 not the whole target (critic F1). The post-integration
re-score, the committed four-leg landing, the parent-owned driver run, the mutation/critic
disposition and the census end remain L1/peer gates. The r65 counters stay frozen as the C1/C2
baselines.

## Behavior

Read the frozen declaration and the r65 verifier spot-check routed items 1-4, the r65 lesson and the
r65 seat evidence (register forge, instrument critic, mutation battery), the round-66 process-defects
and marker-premise erratum, and the live r66 peer drafts (register counter, landing instrument,
driver, source row). Drafted the round lesson plus five integration snippets and an integration map.
No production file was written or edited by this seat.

## Deliverables (all in `.ufo/waves/round-66/w1/R66ScribeLesson/`)

- `round-66.md` — lesson draft: context and process limits; M66-1..M66-5 with class, evidence,
  captured-by, fix and observed-red status; observed/unobserved table; Gate (S435 draft, not
  admitted); Frontier; routed-defect ledger with identities and ages; notes for round 67.
- `quality-append-108.md` — QUALITY criterion 108: marker-plus-rc verdicts, distinct ERROR, actual
  child marker spelling, declared limits.
- `skill-registry-additions.md` — three SKILL Gate-registry rows (C1 counter, C2 driver, hardened
  landing instrument with the a-d verdict map).
- `tool-ledger-additions.md` — two ledger rows and the expected 106 -> 108 population note.
- `province-instrument-addendum.md` — append-only round-66 instrument paragraph.
- `INTEGRATION.md` — destination, insertion point and honest ordering for each snippet.
- `evidence.sh`, `scribe-evidence.txt` — re-runnable read-only receipt; every producer's own rc.
- `report.md` — this report (identical copy at `.ufo/waves/round-66/w1/R66ScribeLesson.md` per the
  seat-spec trailer path).

## Commands and rc

Full argv, output and rc are in `scribe-evidence.txt` (run by `bash evidence.sh`, rc 0). Summary:

| command | observed result | rc |
|---|---|---|
| `git -C LANE rev-parse HEAD` / `git show -s --format='%H%n%cI%n%s' HEAD` | `ed980316…`; `2026-11-03T20:03:29-03:00` | 0 |
| `stat` registry + `w1.ready`; registry `createdAt` | registry `20:03:10.290 -03:00` / `2026-11-03T23:03:10.291Z`; ready `20:03:21.9 -03:00` | 0 |
| cell comparison of `corpus/SOURCES.md` at base and r65 tip | 99 rows both; `rows_added=[] rows_removed=[]`; S028 and S097 each `changed_cells=1 [('opened','2026-10-19'|'2026-10-20','2026-11-03')]`; `all_changed_rows=['S028','S097']` | 0 |
| `sed -n '65p' gate-live-r65.txt`; `sed -n '46p' gate-fileplane-r65.txt` | live: `MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)`; file-plane: `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)` | 0 |
| `grep` on `R65RevRegister/a3-forge-r65.txt` | `rows=8 groups=8/8 receipts=1 resolved=1 gate=ok verdict=TARGET_MET`; `FORGED_RC=0` | 0 |
| `sha256sum` r65 counter (seat draft and committed path) | both `2ccedc68…`; the forge receipt header records `6d28e6ca…` | 0 |
| `python3` read of `instr-mutants.json` | I1, I7, I8, I9 all SURVIVED with `19/19` | 0 |
| `grep` on I1/I7/I9/location-blind probes and critic §S5 | I1 `LANDING_LEG citecheck rc=0` + `GREEN`; I7 `files=21 citations=18 … TARGET_MET`; I9 `usedby rc=2` inside `RED`; location-blind `19/19`; S5 three rc=2 legs -> `RED` exit 1 | 0 |
| C1 candidate: `selftest.txt`, `genuine-base.txt`, `controls.json`, sha | 15/15; genuine base `TARGET_MET rev=eafd500f…`; baseline 1/4, candidate 4/4; sha `4e1b94ff…` | 0 |
| C2 landing: sha, selftest tail/count, report SHA line | `1671cebc…`; `58/58` (case 58 `empty population summary RED`); earlier `f0c8d74f…`/56 | 0 |
| C2 driver report grep | `selftest=0 landing=2 green=no verdict=TARGET_MISSED`; old instrument `unknown argument: --round` | 0 |
| harness sha (wave root vs seat copy) | wave root `218781fb…`; seat copy `84ec73dd…` (drift after the report) | 0 |
| harness c1/c2 candidate summaries | c1: baseline `correct=1/4`, candidate `correct=4/4 TARGET_MET mode=candidate`; c2: same | 0 |
| critic F1/F2 lines and mutation denominators | F1 count omits selftest + real landing; F2 empty-note corpus GREEN/0; C1 4/4 killed once selftest counted, C2 7/7 killed | 0 |
| sentinel-audit checks | `evidence-scope.txt` absent at HEAD (cat-file rc=128); driver argparse only `--repo`/`--rev`/`--scratch-root`; supporting quote is 18 words | 0 |
| `sed -n '368,371p' quality/check-tool-ledger.py` | prints `LEDGER: population=… verdict=… rev=…` (not `MADO_TOOL_LEDGER`) | 0 |
| `python3 quality/check-tool-ledger.py --repo . --rev HEAD` | `population=106 ledger_rows=106 … verdict=TARGET_MET rev=ed980316…` | 0 |
| age derivation `printf '%s\n' $((66-65))` | `1` | 0 |
| census start: warning count and trailer | 37 pre-existing W01/W04 lines; `exit=0` | 0 |
| `grep '^| S435 '` on the source-seat append | row present in `R66ScribeSources/SOURCES.append.md` | 0 |

## Observed / unobserved

Observed (with paths in the lesson and receipt): the two in-place `opened` edits; the r65 forged-cell
acceptance on the counter revision that ran; I1/I7/I9 mutation survival and the S5 crash-as-red
demonstration; the freeze-order timestamps; the actual `LEDGER:` marker; the C1 candidate's seat
selftest, controls and genuine-base run; the C2 candidate's 58/58 seat selftest at the final read
(not final); the driver's baseline TARGET_MISSED; the harness's `--candidate-draft` diagnostics (C1
and C2 each baseline 1/4, candidate 4/4); the mutation battery (C1 4/4 killed once selftest is
counted, C2 7/7); and the critic's F1 (count omits selftest + real landing) and F2 (empty-note
corpus GREEN/0).

Unobserved and left explicitly so: the post-integration `--rev` re-score of both claims; the
committed integrated four-leg landing GREEN at `--round 66`; the parent-owned driver run; the final
C2 selftest count after the empty-corpus fix; the r66 census end; S435 admission; any promotion. No
green placeholder was written for any of these.

## Findings for L1

0. **Integration state at the final read (23:16Z).** L1 had already installed
   `quality/landing-counters.sh` (sha256 `1671cebc…` at the final read, moved from `f0c8d74f…`),
   `quality/counters/c1-r66-register.py` (`4e1b94ff…`) and
   `quality/counters/c2-r66-landing-instrument.py` (`e4d62b3c…`) in the worktree, and the harness at
   `.ufo/waves/round-66/check-controls.py` (`218781fb…`). `quality/tool-ledger.md` had no r66 rows
   yet (`grep` for both basenames returned nothing), so a committed ledger check over those files
   would read `uncovered=2` until the ledger snippet is appended. No
   SKILL/PROVINCE/QUALITY/SOURCES edit was present yet. The harness seat copy now hashes
   `84ec73dd…` while the installed wave-root file is `218781fb…`, so the seat copy is not the
   installed bytes; do not treat them as interchangeable.

1. **The r65 forge is byte-bound to a superseded counter revision.** `a3-forge-r65.txt` records the
   counter it ran as `6d28e6ca…`; the committed `quality/counters/c1-r65-register.py` is
   `2ccedc68…`, and the seat draft now matches the committed bytes. No committed receipt binds the
   forge to the committed counter. The reviewer calls the A3 verdict structural and says counter
   bytes may move before landing (`R65RevRegister.md:83`); that is plausible but is a
   criterion-24-class provenance gap, not a byte-bound reproduction. The lesson records it under
   M66-2 and does not repair it.
2. **The landing draft moved during the wave.** It went `f72e579d…`/46 -> `f0c8d74f…`/56 ->
   `1671cebc…`/58; the last revision adds case 58 `empty population summary RED` after the critic's
   F2 empty-corpus finding. L1 says no final count is pinned yet; all numbers in this draft belong
   to the read-time bytes and must be re-pinned at integration.
3. **The marker premise is integrated, not papered over.** The declaration's `MADO_TOOL_LEDGER`
   literal is contradicted by the actual child `LEDGER:` line; the candidate anchors the actual
   line, and the four C2 outcomes are unchanged. Closure may grade the literal mismatch.
4. **Freeze chronology is a disclosed miss.** The freeze commit is 19 s after the registry
   `createdAt` and 8 s after `w1.ready`; criterion 106's strict order is not met, and no
   chronological pass is claimed. The baseline control's pre-freeze execution is likewise not
   satisfied; baseline receipts are retained and a miss must stay a miss.
5. **M65-2's truth gap is explicitly not fixed.** The r66 C1 counter adds heading uniqueness,
   per-row receipts and the exact live line; invented state prose with valid pointers is a selftest
   pass case. Do not read its green as truth binding.
6. **S435 supports C2 exit vocabulary only.** It proves neither C1 register truth nor that a child
   ran. Its `used-by` names `corpus/lessons/round-66.md`, so the lesson must land with or before the
   row or the census E11 fires.
7. **Ledger arithmetic is a prediction.** Installing both `quality/counters/*.py` files yields
   `population=108 ledger_rows=108`; at draft time the ledger reads 106/106.
   `quality/landing-counters.sh` is outside the ledger population (`.sh` counts only under
   `tools/`) and belongs in the SKILL registry.
8. **The r65 counters stay frozen.** The frozen C1/C2 controls use the r65 instruments as the
   baseline at the same revision; no r66 snippet edits them.
9. **The frozen C2 count is narrower than the frozen target (critic F1).** The harness runs cases
   a-d only and prints `correct=4/4 TARGET_MET` without running the candidate selftest or a real
   four-leg landing, both of which the frozen C2 target names. Its diagnostics are useful, but that
   line alone must not be credited; wire the driver (`c2-r66-landing-instrument.py`, which measures
   both legs) or require the two legs separately. QUALITY 108 and the SKILL snippet carry this.
10. **The v2 landing candidate had a new false-green path (critic F2).** An empty-note corpus read
    `indexed=0/0` and GREEN/0 where the r65 bytes crashed red. The later `1671cebc…` draft adds
    selftest case 58 `empty population summary RED`; L1 still says no final count is pinned, so the
    56 -> 58 movement is read-time history, not an integration pin.
11. **Three snippet defects were caught by the sentinel audit and corrected.** (a) The ledger rows
    pointed at `receipts/evidence-scope.txt`, which is untracked at HEAD (`git cat-file -e` rc=128);
    both rows now point only at committed files (`claims-declaration-r66.md` and
    `w1-dispatch.json`), and the snippet records the untracked file as a commit-first item.
    (b) The SKILL driver entry command passed `--round 66`/`--citecheck-paths`, which the driver CLI
    does not accept (argparse has only `--repo`, `--rev`, `--scratch-root`); the row now uses the
    real CLI and states that round/receipts are internal. (c) The supporting quote is 18 words, not
    19; corrected. All three were corrected before integration; no production file was edited by
    this seat.

## Limitations

- I did not run the frozen control harness, the committed landing, the mutation battery, the critic
  pass, or the census end; those are peer/L1 gates. Harness and critic results are quoted from their
  retained summaries and reports, not re-measured here.
- I did not fetch any source. The S435 Gate block is quoted from the source seat's draft and is not
  re-opened or re-digested by this seat.
- I did not re-run the r65 forge against the committed counter; the finding is a byte comparison
  plus the reviewer's own structural caveat.
- Peer drafts were live-edited during the read; hashes, counts and even report text are read-time
  values, not integration-time pins.
- No peer report's internal claims were re-measured; their retained evidence paths were read.
- The lesson draft carries no landing measurement, no admission and no promotion claim.

## Out of scope

No production edits, no commits/pushes, no judge invocation, no git mutation, no installs, no host
changes, no source-row admission, no knowledge entry, no promotion.

## Artifact paths

- `.ufo/waves/round-66/w1/R66ScribeLesson/round-66.md`
- `.ufo/waves/round-66/w1/R66ScribeLesson/quality-append-108.md`
- `.ufo/waves/round-66/w1/R66ScribeLesson/skill-registry-additions.md`
- `.ufo/waves/round-66/w1/R66ScribeLesson/tool-ledger-additions.md`
- `.ufo/waves/round-66/w1/R66ScribeLesson/province-instrument-addendum.md`
- `.ufo/waves/round-66/w1/R66ScribeLesson/INTEGRATION.md`
- `.ufo/waves/round-66/w1/R66ScribeLesson/evidence.sh`
- `.ufo/waves/round-66/w1/R66ScribeLesson/scribe-evidence.txt`
- `.ufo/waves/round-66/w1/R66ScribeLesson/report.md`
- `.ufo/waves/round-66/w1/R66ScribeLesson.md` (seat-spec trailer copy)
