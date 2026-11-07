# R92MMutC2 — mutation probe of the C2 candidate (round 92, wave w1)

Seat R92MMutC2 (leaf, mutation tester). Target: `.ufo/waves/round-92/build/check-seat-reports.c2.py`.
Every counter invocation below is a **DRAFT** run (`--draft-check`); no number here is a measurement and
nothing was written under `.ufo/waves/round-92/receipts/`. Scratch `S=/fast/scratch/hyaku/mado-r92/R92MMutC2`
(deleted on exit). No installs. Lane files written by this seat: this report,
`controls/gate-defects-mutants-r92-mc.json` and `controls/gate-defects-battery-r92-mc.json`.

## 0. Bytes under test (hashes)

| artifact | sha256 |
|---|---|
| candidate, first half of the probe (author replaced it 23:13:50) | `be47235bf6b8d2cb8f38bd1740e977ccdc4066dd33e732876625b66546e4a876` |
| candidate, delivered-set runs (live file, snapshot `candidate-176fc066.py`) | `176fc066b49334921e4fd746de55db8106709c29dfe225430224c9d46ed1663a` |
| delivered mutants (20), `controls/gate-defects-mutants-r92-mc.json` | `6831bdbde4bdcc4400edaa9ec9ba3095687c761d5e1097da2d55b6040fe49e0c` |
| probe superset mutants (22, MC16/MC17 extra), not delivered | `803bb03ab2954fb44607450c9d3f9f83a7c4aefc76c8b149c1b79fe869ae7664` |
| delivered battery (41 = L1 snapshot 28 + 13), `controls/gate-defects-battery-r92-mc.json` | `c95cec97ac61d9884949399b61745d04b0f5919bbd83401c3b08b56eb9194dcf` |
| L1 battery snapshot (28 fixtures, taken 23:01) | `73ae3bde695c8e7a6c34ccd99c55586c360b41c98f5d8fd50d2373e5270392d0` |
| L1 mutants snapshot (14) | `689e17fa7d2143b56abca5bd43804470e7d0a3d25a8e74b96e612bed9e4d742f` |
| L1 mutants, 13 applicable to `176fc066` (N01 dropped) | `3b42e85b8edd81329e8e4a4c70f26a5bb3669d46a447147f9ec9f84569c5db6e` |
| `controls/r91-c2-argv-r92.json` | `d21b1979b8b42203c8d9c8d033ec71af8027ff79911adc348cddb9685df4b604` |
| `quality/counters/c2-r91-seat-reports.py` as read from `d992ef74` | `c74f5baae915a4669ece5033a35ba16f5db0131a2db9a6e83a702de9e932d486` |
| `quality/counters/c2-r92-gate-defects.py` at the delivered-set runs (replaced 23:19:59) | `0aa4d1f18c3f309a8ef5a7575f1a4bde84681d9f7843dea03fdca723de30945c` |

The candidate was a moving draft during w1: `be47235…` until 23:13:50, `176fc066…` after (the author added
the worktree directory-dispatch enumeration, the rev tree/gitlink enumeration and the matching docstring).
The counter also changed (23:19:59): the earlier copy scored mutants on the battery + selftest only; the
current copy adds a 60-fixture fresh leg (`fresh_battery`, seed = first 8 hex of the check sha =
`0x176fc066` = 393199718) and pins the round-91 counter read from `<rev>`. All delivered-set numbers below
are from the current counter; the earlier probe is summarised in §5 and labelled superseded.

## 1. Method

* 20 delivered mutants, find/replace on the round-92 surface: `paths()` (worktree directory dispatches, rev
  non-blob dispatches), `check_dispatch` (call order, symlink scope), dispatch parsing/guards, `inside()`,
  `unsafe()`, `tok()` vs file lookup order, trailer grammar (CRLF, trailing prose, inline mention,
  rendered/plain precedence), discovery regex scope, verdict, rounds dedupe. Two further probe mutants
  (MC16/MC17) weaken selftest assertions; they are predicate-equivalent and are **not** in the delivered file
  (§4).
* Detector: `python3 -I quality/counters/c2-r92-gate-defects.py --repo <lane> --rev
  d992ef7494b054591ee9104df1da49264678df5d --base-rev <same> --battery … --mutants … --expect-…-sha256 …
  --r91-argv … --expect-r91-argv-sha256 d21b19… --expect-r91-counter-sha256 c74f5baa… --scratch-root
  $S/cN --timeout 20 --draft-check $S/candidate-176fc066.py`. A mutant is killed iff it meets fewer than
  all `--battery` fixtures, or fewer than all 60 fresh fixtures, or its `--selftest` result line differs from
  the candidate's (`... checks=23 failed=0`).
* Fixture expectations were written from the round-91 residual defect report (R91MResidC2 §2b-§5) and the
  candidate docstring before any fixture was run. The candidate then met every one of them in every run
  (`met == fixtures`, `MC=13/13`), so no expectation was fitted to the check.

### Delivered-set runs (all against `176fc066`, current counter)

| run | battery | mutants | candidate | mutants killed |
|---|---|---|---|---|
| E5 | L1 snapshot, 28 | delivered 20 | `met=28/28 fresh=60/60 selftest=ok:checks=23 failed=0` | **8** (5 battery/fresh + 3 fresh-only: MC01, MC21, MC22) |
| E4 | delivered, 41 | delivered 20 | `met=41/41 fresh=60/60 MC=13/13 selftest=ok` | **20/20** |
| E6 | delivered, 41 | L1 13 applicable | `met=41/41 fresh=60/60` | **13/13** |

E4 summary line (verbatim):
`MADO_GATE_DEFECTS: DRAFT_TARGET_MET pred=PRED-C2-r92-v1 rev=draft:…/candidate-176fc066.py base_rev=d992ef74… fixtures=41 met=41 F1=5/5 F2=5/5 F3=3/3 F4=3/3 F5=4/4 MC=13/13 P=8/8 fresh=60/60 selftest=ok:SEAT_REPORTS_SELFTEST: checks=23 failed=0 mutants=20 killed=20 base_met=19 always_ok_met=7 always_refuse_met=11 r91_counter=TARGET_MET check_sha256=176fc066…`
E4 r91 leg: `MADO_SEAT_REPORTS: DRAFT_TARGET_MET pred=PRED-C2-r91-v1 … expectations=59 met=59 fresh=60/60
fresh_seed=393199718 selftest=ok … mutants=55 killed=55 base_met=0 always_ok_met=5 always_missing_met=0
receipt_presence_met=11 check_sha256=176fc066…`.
E5 (L1 battery alone) verdict is `DRAFT_TARGET_MISSED`: 12 of the 20 mutants survive it (they are killed by
the delivered battery in E4). Root cause is battery coverage, not candidate behaviour.

## 2. Delivered mutants and verdicts

`E5` = L1 battery 28 fixtures; `E4` = delivered battery 41 fixtures; both against `176fc066`.
"battery-only" means met < 41 with the selftest result line unchanged (the battery is the sole detector).

| id | mutated behaviour | E5 met / selftest | E4 met / selftest | verdict, detector |
|---|---|---|---|---|
| MC01 | worktree `paths()` drops dirs named like a dispatch (review-finding-1 regression) | 28 / same | 40 / same | killed, battery-only (`MC01-worktree-dir-dispatch`) |
| MC02 | worktree `size()` accepts any existing path (directory counts as present) | 28 / same | 40 / same | killed, battery-only (`MC02-dir-report`) |
| MC03 | dispatch regular-file check moved after the read (FIFO blocks again) | 21 / differs | 32 / differs | killed (F1 rev, F4 timeouts, and the two directory/tree dispatch fixtures; both channels) |
| MC04 | dispatch parse except narrowed (KeyError/TypeError escape as traceback) | 28 / same | 40 / same | killed, battery-only (`MC04-nonlist-tasks`) |
| MC05 | path tokenised before the file lookup (present non-ASCII report reported missing) | 28 / same | 40 / same | killed, battery-only (`MC05-nonascii-present`) |
| MC06 | rendered trailer loses CRLF tolerance | 28 / same | 40 / same | killed, battery-only (`MC06-crlf-rendered`) |
| MC07 | plain trailer loses CRLF tolerance | 28 / same | 40 / same | killed, battery-only (`MC07-crlf-plain`) |
| MC08 | rendered trailer accepts a path followed by prose | 28 / same | 40 / same | killed, battery-only (`MC08-trailing-prose`) |
| MC09 | rendered trailer no longer line-anchored (inline mention counts) | 28 / same | 40 / same | killed, battery-only (`MC09-inline-mention`) |
| MC10 | rendered/plain precedence swapped | 28 / same | 40 / same | killed, battery-only (`MC10-rendered-beats-plain`) |
| MC11 | discovery regex widened to nested `*-dispatch.json` payloads | 28 / same | 40 / same | killed, battery-only (`MC11-nested-payload`) |
| MC12 | `'..'` no longer unsafe | 28 / same | 40 / same | killed, battery-only (`MC12-dotdot-inside`) |
| MC13 | non-list `tasks` guard removed (crashes instead of setup error) | 28 / same | 40 / same | killed, battery-only (`MC04-nonlist-tasks`) |
| MC14 | non-string task body not guarded (SR04 becomes traceback) | 28 / same | 40 / same | killed, battery-only (`MC14-nonstring-task`) |
| MC15 | unsafe findings excluded from verdict and exit code | 23 / differs | 35 / differs | killed (F5-01/02/03/04, P-03, MC12-dotdot-inside; both channels) |
| MC16 | selftest F1 case loses `want_in` (probe only, not delivered) | 28 / same (E1, superset) | 41 / same (E2, superset) | SURVIVED — predicate-equivalent (§4) |
| MC17 | selftest F3 case no longer repeats the round (probe only, not delivered) | 28 / same (E1, superset) | 41 / same (E2, superset) | SURVIVED — predicate-equivalent (§4) |
| MC18 | `inside()` no longer calls `realpath` (parent-link escape looks inside) | 24 / differs | 37 / differs | killed (F5-01/02/03/04, both channels) |
| MC19 | rounds dedupe removed (reverse-sorted, duplicates counted) | 25 / differs | 38 / differs | killed (F3-01/02/03, both channels) |
| MC20 | worktree dispatch symlink refused only when it leaves the repository | 27 / differs | 40 / differs | killed (F1-02 + worktree selftest case, both channels) |
| MC21 | rev `paths()` drops non-blob dispatch paths (tree/gitlink vanishes) | 28 / same (fresh kills it) | 40 / same | killed, battery-only (`MC21-rev-tree-dispatch`) |
| MC22 | rev tree-prefix recording removed (directory dispatch never enumerated) | 28 / same (fresh kills it) | 40 / same | killed, battery-only (`MC21-rev-tree-dispatch`) |

Each of the 15 battery-only kills misses exactly one of the 13 new fixtures (E4 met=40 of 41); no mutant
needed the fresh leg to be killed in E4. In E5 the three enumeration mutants with `met=28` and an unchanged
selftest line (MC01, MC21, MC22) are killed by the fresh leg alone, which includes directory/tree dispatches.

## 3. Killing fixtures added (13; battery = L1 snapshot 28 + 13 = 41)

Every expectation below is stated in R91MResidC2 or in the candidate docstring; none was read off a run.
All are `--round 7` unless stated.

| fixture | kills | expectation and derivation |
|---|---|---|
| `MC01-worktree-dir-dispatch` | MC01 | A directory at a dispatch path is a setup error in worktree mode: rc 2, `contains "not a regular file"`. Docstring: "a dispatch that is not a regular file — a symlink or a directory in either mode …". |
| `MC02-dir-report` | MC02 | A directory at a trailer path is `SR01 missing`, rc 1, `missing=1 present=0`. R91MResidC2 §3 P17 and §4 fresh state `dir` -> SR01 (checked and correct); SR01 is "trailer path absent" (a non-empty file is required). |
| `MC04-nonlist-tasks` | MC04, MC13 | Dispatch with `taskCall.tasks = 5` -> rc 2, no findings. Docstring exit-2 rule "a dispatch that is not JSON or lacks taskCall.tasks"; the check itself raises `TypeError` for a non-list. |
| `MC05-nonascii-present` | MC05 | Present report at `.ufo/waves/round-7/r1/été.md` -> rc 0, `present=1`. R91MResidC2 §3 P14b: a present non-UTF-8 filename gives verdict OK rc 0; the F2 rule is a rendering rule, not a lookup rule. |
| `MC06-crlf-rendered` | MC06 | Rendered trailer ending CRLF, report present -> rc 0, `present=1`. R91MResidC2 §3 P7: CRLF rendered trailer recognised (checked and correct). |
| `MC07-crlf-plain` | MC07 | Plain residual trailer ending CRLF, report missing -> rc 1, `SR01`. Same P7 evidence for the plain grammar. |
| `MC08-trailing-prose` | MC08 | `Report: write your scoped findings to <path> (see note)` with the path present -> rc 1, `SR04`, `untrailed=1`. Docstring: "a path followed by prose is not one [a trailer]". |
| `MC09-inline-mention` | MC09 | `see: Report: write your scoped findings to <present path>` -> rc 1, `SR04`, `untrailed=1`. Docstring: "a mention inside a sentence … is not one". |
| `MC10-rendered-beats-plain` | MC10 | Rendered trailer to a present report plus a plain line to a missing one -> rc 0, `present=1`. Docstring: the plain line "is used when the rendered trailer is absent"; round-91 set F09 `rendered-beats-plain` labels this intended (§3 P17). |
| `MC11-nested-payload` | MC11 | A nested `round-7/reportdir/fixtures/w1-dispatch.json` payload plus a real `w1` wave -> rc 0, `rounds=1 waves=1 seats=1 present=1`. Docstring scope; R91MResidC2 §2b: the nested fixture payload is "correctly out of scope". |
| `MC12-dotdot-inside` | MC12 | Trailer path `.ufo/waves/round-7/w1/../w1/A.md` whose normalised file exists -> rc 1, `SR03`, `unsafe=1`. Docstring SR03 "with a '..' component"; §4 fresh state `dotdot` -> SR03. |
| `MC14-nonstring-task` | MC14 | Task body `5` -> rc 1, `SR04`, `untrailed=1`. R91MResidC2 §3 P2: a task object/number is SR04 untrailed (checked and correct). |
| `MC21-rev-tree-dispatch` | MC21, MC22 | rev mode, committed tree at `.ufo/waves/round-7/w1-dispatch.json/` (with a file inside) -> rc 2, `contains "not a regular file"`. Docstring: "a gitlink in --rev, a [directory] in either mode"; the candidate records tree prefixes so the wave cannot vanish. |

The L1 battery snapshot (28 fixtures) alone does not detect 12 of the 20 delivered mutants (E5); the 13
fixtures above are the set that detects all of them (E4). Two of them (`MC01-…`, `MC21-…`) also
detect the enumeration mutants that the counter's fresh leg happens to cover.

## 4. Equivalence: the two selftest-weakening probes (not delivered)

MC16 (`want_in` removed from the rev F1 selftest case) and MC17 (`[7, 7]` -> `[7]` in the F3 case) change
only the selftest fixture data. The checked program's behaviour is byte-identical on every battery and fresh
fixture, and the selftest still prints the same `SEAT_REPORTS_SELFTEST: checks=23 failed=0` line; the counter
reports `SURVIVED met=41 selftest=same` for both (run E2, superset file). Under PRED-C2-r92-v1's kill rule
("meets fewer fixtures or changes the selftest result line") they are therefore **equivalent mutants**, not
candidate defects; they are excluded from the delivered kill set so the set can be met.

Coverage finding (for the L1, not a contract change): the predicate's selftest leg pins only the result line
(exit 0, `checks=N failed=0`). A weakened-but-passing selftest assertion is invisible to it. If the selftest
is to carry weight beyond the count, a future predicate would have to pin the selftest's own failure
behaviour (e.g. inject a known regression and require a named `SEAT_REPORTS_SELFTEST_FAIL` line); that is a
new rule, not a fix to these bytes.

## 5. L1 mutants

`E6` = the 13 L1 mutants whose `find` still occurs exactly once in `176fc066`, scored on the delivered
41-fixture battery with the current counter. `old` = the full 14 on the superseded candidate `be47235…` +
L1 battery 28, old counter (run B).

| L1 id | old met / selftest (28) | E6 met / selftest (41) | verdict |
|---|---|---|---|
| N01 | 24 / differs | **not applicable**: `find` occurs 0 times in `176fc066` (`paths()` gained `+ sorted(self.others)`) | the L1 must regenerate this mutant against the frozen candidate |
| N02 | 24 / differs | 37 / differs | killed |
| N03 | 27 / differs | 40 / differs | killed |
| N04 | 25 / differs | 37 / differs | killed |
| N05 | 20 / differs | 31 / differs | killed |
| N06 | 23 / differs | 36 / differs | killed |
| N07 | 26 / differs | 39 / differs | killed |
| N08 | 26 / differs | 39 / differs | killed |
| N09 | 25 / differs | 38 / differs | killed |
| N10 | 24 / differs | 37 / differs | killed |
| N11 | 24 / differs | 37 / differs | killed |
| N12 | 25 / differs | 38 / differs | killed |
| N13 | 26 / differs | 39 / differs | killed |
| N14 | 27 / **same** | 40 / **same** | killed by battery only (F5-04 `parent-link-to-prefix-sibling`) |

**No L1 mutant is killed only by the selftest.** Every killed L1 mutant misses at least one battery fixture
(`met < fixtures`), so the battery leg alone kills each of them; N14 is the pure battery-only case (selftest
result line unchanged). The complementary fact: 13 of the 14 also change the selftest line, so the original
L1 battery + selftest pair has two independent detectors for them.

## 6. Candidate conformance observed in the draft runs

On `176fc066`, with the delivered battery, the candidate met 41/41 fixtures (F1 5/5, F2 5/5, F3 3/3,
F4 3/3, F5 4/4, MC 13/13, P 8/8), all 60 fresh fixtures, `--selftest` `checks=23 failed=0`, and the
round-91 frozen counter printed `DRAFT_TARGET_MET` for the same draft bytes (59/59 expectations, 60/60
fresh, 55/55 mutants). Controls in E4: base revision 19/41, always-OK 7/41, always-refuse 11/41.

## 7. Dead steps / live edits encountered

1. First invocation at 22:57 failed because the live L1 battery was rewritten mid-probe (27 -> 28 fixtures
   at 23:01): `MADO_GATE_DEFECTS: SETUP_ERROR sha256 mismatch …/gate-defects-battery-r92-l1.json:
   73ae3bde… != c923ac17…`. Fixed by freezing a snapshot (`73ae3b…`) and pinning it.
2. Runs at 23:15 failed because the candidate was replaced at 23:13:50: `MADO_GATE_DEFECTS: SETUP_ERROR
   mutant MC01: find occurs 0 times`. Fixed by snapshotting `176fc066…` and re-deriving MC01/MC21/MC22
   against the new `paths()`/`others` code.
3. Runs at 23:20 failed because the counter was replaced at 23:19:59:
   `c2-r92-gate-defects.py: error: the following arguments are required:
   --expect-r91-counter-sha256`. Fixed by pinning the round-91 counter bytes at `d992ef74`
   (`c74f5baa…`) and re-running the delivered set (E4/E5/E6).
4. Superseded probe (candidate `be47235…`, old counter, before the two rewrites): 17 mutants, L1 battery 28
   -> killed 3 (MC01-old form, MC03, MC15), 14 survived; delivered battery 39 -> killed 15, survivors
   MC16/MC17 only; L1 14 mutants -> killed 14/14 (N14 battery-only). The same coverage gaps were present
   before the author's 23:13 edit; the delivered numbers above supersede these.

## 8. Restoration / host safety / cleanup

* The candidate file was never modified by this seat: it was read (`sha256sum`, counter `--draft-check`
  copy) only. Its sha is `176fc066…` at the start and at the end of the delivered-set runs (and mtime
  23:13:50, i.e. the author's write). Every mutated check was materialised by the counter inside `$S` as
  `check-seat-reports.py` in an opaque directory, and removed with the scratch tree.
* No mutating git/jj ran in the lane; the counter's fixture repositories and the selftest's throwaway repos
  were created under `$S` with a fixture identity and a toplevel assertion. No `xdg-mime`/`xdg-open`/
  desktop-database command ran. No service, sysctl or package command ran; no installs.
* Scratch `$S` was deleted on exit after this report was written; nothing cited remains only there (the two
  control JSONs are in the lane and their sha256 are above).

## 9. What the L1 should take from this probe

1. The delivered 13 fixtures cover behaviour the 28-fixture L1 battery cannot see: directory reports,
   directory dispatches (both modes), non-blob rev dispatches, non-list `tasks`, non-string task bodies,
   present non-ASCII reports, CRLF in both trailer grammars, trailing prose, inline mentions,
   rendered-over-plain precedence, nested payload scope, and `..` components. Any frozen mutant set built
   on the L1 battery alone will contain survivors from these classes.
2. The delivered mutants file contains no equivalent mutants; its 20 mutants are all killed by the
   delivered battery (E4). MC16/MC17 document a selftest-coverage limit and must not be frozen into a
   kill set.
3. The candidate and counter changed twice during w1; `N01` no longer applies to the current candidate, and
   the L1 mutant set needs regeneration at the freeze. The L1 battery must be re-snapshotted at the freeze
   (my battery embeds the 23:01 snapshot; the live file is the authority).
