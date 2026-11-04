# mado round 68 — lesson

author: mado L1, integrated from one w1 wave; outside-lane closure remains authoritative.
date: 2026-11-03
base: 510100c81e6cf63fec6be380c2f2f9c670f32cbc
frozen declaration: `.ufo/waves/round-68/claims-declaration-r68.md`, e0727cda15621766c35dcf8b70c211b6531aab45
(blob `1f3a2392f9140b6828511c5bc1f433e4417d9c04159ce061dde7fc9b549e5f12`, 9261 B).
control set: `.ufo/waves/round-68/controls/c2-controls.json`, sha256
`b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91` (11 cases; the same hash is read
at the worktree and at the freeze commit).
pre-freeze baseline: `.ufo/waves/round-68/control-baseline-r68.txt`, landed at
`2ca2bec39c42770a3176989f013e8c1cbbdb7df3` (blob `44551431b885cc60f3be52ed722b740887d908d696461681aab8e29baa1a8025`,
4985 B).

## Outcome and boundaries

Two bounded claims, both frozen before candidate construction.

- **C1 calibration — the control harness kills its own forged kill credit.** At the measured
  revision the frozen counter `quality/counters/c1-r68-selfmutants.py` extracts
  `quality/counters/c1-r68-landing-controls.py` from `REV`, runs its `--selftest`, applies the
  three frozen single-point recipes exactly once each, and requires each mutant's own
  `--selftest` to exit nonzero. Target `selftest=0 killed=3/3 applied=3/3`, bounded score
  `10 × killed / 3`. At the base `510100c8` the score is 0/3: the scored harness is absent,
  and the same three recipes applied to `quality/counters/c2-r67-landing-controls.py` at the
  base all survive its green 47/47 selftest (`survivors=S1,S2,S3 killed=0/3 applied=3`).
- **C2 operability — the standing gates' git-object reads are guarded.** At the measured
  revision the frozen census over `quality/check-[^/]+\.py` reads 20 files from git objects,
  classifies 13 readers, and requires 13 guarded readers, 0 unguarded, plus 11/11 frozen
  classification cases. `population=20` and `readers=13` are part of the target; a repair may
  not shrink the denominator. Bounded score `10 × guarded / readers`. At the base
  `510100c8` the census reads `guarded=1 unguarded=12` (0.7692); the only guarded reader is
  `quality/check-tool-ledger.py`.

**Not claimed.** State truth of any PROVINCE cell; universal fault coverage; honest or
authenticated invocation; runtime behaviour of the gates or of the guard (the census classifies
committed source text, and the hazard probe samples one gate); protection against a repository
already rewritten; object authenticity; exhaustive harness mutants; lane-wide coverage (the
wider lexical reader set from r67 remains outside this gate population); desktop, compositor,
session or service health; any `[x]`, promotion or axis retirement. Both claims are
finite-control claims and no wider guarantee is read out of a green count. Seat and wave
demonstrations are not the committed-revision measurement; the L1 landing block below carries
`TBD-INTEGRATION` for those values.

## Mistakes

| mistake | class | evidence | captured-by | fix and failure it can now show |
|---|---|---|---|---|
| M68-1: the r67 harness's selftest never runs its `measure()` decision body, so a forged kill credit survives a green selftest. | survivor | `corpus/lessons/round-67-verifier-spotcheck.md:181-183` (routed defect 3, `mr_killed = True`); `.ufo/waves/round-68/control-baseline-r68.txt:17-22` — recipe S1 `mr_killed = bool(` occurs once in `quality/counters/c2-r67-landing-controls.py` at 510100c8 (blob `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58`, 30697 B), the mutant's selftest exits 0 with 47/47 assertions and `killed=no`, and `MADO_R68_BASE_CONTROL survivors=S1,S2,S3 killed=0/3 applied=3`. | `none` as an enforced r67 rule — the r67 claim accepted the harness selftest green, and the outside spot-check caught it first. QUALITY 74 (a selftest's teeth must sample decision sites outside the `selftest` function) is the nearest standing rule but was not applied to this harness. | The r68 C1 claim scores exactly this. `quality/counters/c1-r68-selfmutants.py` (freeze blob `bdea8dc6b4455f45c59896a44f0bd4ede21c26b82c67e0618a05ac069ef50a85`, 12769 B) extracts the successor harness from `REV`, applies S1-S3 once each, and requires each mutant's own `--selftest` to exit nonzero; the scripted none-killed case asserts `killed=0/2 … TARGET_MISSED`. Failure it can now show: at 510100c8 the S1 recipe leaves the r67 harness green (`rc=0 assertions=47/47`, measured in the baseline receipt); at the measured revision the same recipe must make the successor's selftest exit nonzero, so the survivor cannot be counted as a kill (landing line `TBD-INTEGRATION`). |
| M68-2: the r67 C2 kill rule described a mechanism the delivered M-R control does not use — the rule said the candidate control run "exits nonzero on the mutant", while M-R's child exits 0 and is counted killed by the forged-credit flip. | reference-drift | `corpus/lessons/round-67-verifier-spotcheck.md:173-177` (routed defect 1); `.ufo/waves/round-67/measurement-c2-after.txt:19` at `caf131d6be04dd2ccc742636625c1ce196610522` — `MADO_R67_MUTANT M-R … rc=0 verdict=TARGET_MET missing=0 forged_credit=yes killed=yes`. | `none` — no QUALITY criterion compared a frozen kill-rule sentence with the control's printed observable; the outside spot-check caught it. QUALITY 96 covers a landed tool contract's out-of-contract list, not a kill-rule sentence. | The r68 predicates freeze the observable each counter prints: C1's kill is "the mutant's own `--selftest` exits nonzero", with the none-killed case asserting `killed=0/2 … TARGET_MISSED`; C2's predicate is the AST classification count with the 11 named control cases, not a child-exit sentence. Failure it can now show: the r67 M-R receipt reads `rc=0 … killed=yes`; under the r68 C1 rule an exit-0 mutant is not killed, so the rule cannot silently describe a different mechanism. |
| M68-3: the r67 "controls unchanged" sweep is path-vacuous — `git diff aa7fe5a1..HEAD -- controls` from the lane root matches no path, so it prints empty regardless of the change. | vacuous | `corpus/lessons/round-67-verifier-spotcheck.md:178-180` (routed defect 2); at lane head `92151a50cc79b40700cafab98488012089f67e34` / report `7111b67bec4c129ec49ef22d3b703262fd72ed36`, `git ls-tree -r --name-only 92151a50 \| grep -c '^controls/'` → `0`, while `git diff aa7fe5a1 92151a50 -- ':(glob)**/controls/**'` prints 15 lines, including `score-baseline-c2.py`'s default base `eafd500f` → `0b28ffb4` at `5f9ce459`; the frozen `c1-controls.json` is byte-identical at both revs. | QUALITY 62 — a zero count is evidence of absence only when the same channel is shown to carry the class being counted; the bare path was never positively probed. | The round-68 lesson and receipts use the explicit nested path and state the base correction beside the unchanged control set; failure it can now show: the bare path prints 0 lines on a diff whose nested path prints 15, so the sweep cannot be read as "controls unchanged". |

A fix counts only on its named red/green evidence. M68-1's green is the landing measurement; M68-2
and M68-3 are process/reference fixes with their red states at the named revisions, not new scored
capabilities.

| M68-4: the frozen C2 counting command passed `--scratch-root`, an argument the counter did not accept, so the declared command could not print its contract line (exit 2, "unrecognized arguments"). | stale-premise | `.ufo/waves/round-68/c2-command-erratum-r68.txt` — the counter blob at `e0727cda` exits 2 on the declared argv; `corpus/lessons/round-68.md` was drafted from the counter's docstring, not from a run. | `none` before this round; QUALITY 110(a) now requires the pre-freeze receipt to run the advertised invocation verbatim. | The counter accepts `--scratch-root` for interface parity and its selftest asserts the frozen argument set parses (`MADO_R68_READER_GUARD_SELFTEST: 25/25`); the errata receipt shows red-before `rc=2` and the same command printing `TARGET_MISSED rc=1` after. |
| M68-5: the C2 counter's verdict did not enforce the frozen denominator, so deleting every quoted object-read verb from one repaired gate scored `readers=12 … TARGET_MET rc=0` — a repair could shrink the population and still pass. | vacuous | `R68RevC2` finding 1 and `.ufo/waves/round-68/c2-denominator-erratum-r68.txt` — the pre-fix counter at `2a39e741` prints `population=20 readers=12 guarded=12 unguarded=0 … TARGET_MET` rc 0 on the verb-deleted fixture. | `none` at freeze; QUALITY 110(b)'s "the frozen sentence and the counter's code are the same sentence" is the rule it violated. | `verdict_met()` now requires `population==20` and `readers==13` beside `unguarded==0` and every control correct; the same fixture reads `TARGET_MISSED rc=1` and the selftest carries five denominator assertions (25/25). |

| M68-6: the C2 counter's verdict still accepted a truncated control set (`controls=10/10 … TARGET_MET`) after the first denominator fix, so the frozen `controls=11/11` was not enforced. | vacuous | `R68CriticClaims` B1; the pre-fix landed counter (sha256 `5a6b3865…0faa`) prints `TARGET_MET` with a ten-case `--controls` file, while the frozen predicate line carries `controls=11/11`. | QUALITY 110(b) again — the same "frozen sentence and counter code are one sentence" rule, caught by the critic this time. | `verdict_met()` now requires `controls_total == 11` (frozen constant) and the selftest asserts `verdict_met(20, 13, 0, 10, 10)` is False (26/26); the truncated-set run prints `TARGET_MISSED rc=1`. |

## Gate

Admitted: **S437**, scoped to the lane's git object-read census — not a desktop fact. The row was
drafted by `R68ScribeKnowledge` at
`.ufo/waves/round-68/w1/R68ScribeKnowledge/draft/corpus/SOURCES-row.txt` (sha256
`cbf4cf5ef05b0ca3381b2a6b5222049607c0ad055a97a463e56ff8b0e1eaac05`, 1068 B, one line, 11 cells,
no literal or escaped pipe), and independently opened by `R68ScoutSources` (its report is
`.ufo/waves/round-68/w1/R68ScoutSources.md`, landed; it re-fetched the same bytes three times
byte-identically and audited the entry's twelve cited quotes). The row is an append; no existing SOURCES cell is edited.

- Canonical URL: https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc
- Access date: 2026-11-03.
- Located quote, 18 words, DESCRIPTION lines 21-22 of the fetched bytes:
  "Output the contents or other properties such as size, type or delta information of one or
  more objects."
- Replacement-boundary sentence, 14 words, lines 198-199 of the same bytes:
  "Objects are presented as-is, without respecting the "replace" mechanism of
  linkgit:git-replace[1]." — the one documented `cat-file` mode that bypasses replacement; it
  bounds where the census vocabulary's reads can be redirected.
- Version pin: tag `v2.56.0` — tag object
  `2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled commit
  `a018953688f1b10bddf91bff8747068f5f4746a4`; host `git --version` prints
  `git version 2.56.0`. No `latest`/`main` anchor.
- Fetched-bytes sha256: `6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2`
  (16099 B, 470 lines).
- Row shape: 11 cells, no literal or escaped pipe; kind `docs`, tier `A`, status `mined`, opened
  `2026-11-03`, recheck `90d`, used-by `corpus/lessons/round-68.md`,
  `corpus/knowledge/gate-git-read-guards-r68.md`. Next unused id computed from the round-start
  census: max `S436`, 373 rows; `S437` occurs zero times in `corpus/SOURCES.md`, and no row
  carries this canonical URL (`grep -c 'git-cat-file.adoc'` → `0`).
- Admit for the outside spot-check: open the canonical URL at the `v2.56.0` tag; lines 21-22
  carry the quoted sentence and lines 198-199 the replacement exception; the bytes hash to
  `6c32dbda…`; the tag object peels to `a0189536…`; the host git agrees with the tag.
- Reject (claim, outside read): "`git cat-file -e` establishes object authenticity or integrity."
  The page says `-e` exits zero if the object "exists and is a valid object" (lines 49-52) and
  prints nothing unless the object is malformed (line 291) — existence and format validity, not
  provenance or content truth. Flip: a signature/verification sentence in the same file, or a
  lane instrument that pins object bytes to a digest rather than testing presence.
- Recheck/status/used-by cell changes old→new: **one**, in place and append-only:
  `S436` `used-by` old `corpus/lessons/round-67.md,
  corpus/knowledge/replace-ref-citation-boundaries-r67.md` → new `corpus/lessons/round-67.md,
  corpus/knowledge/replace-ref-citation-boundaries-r67.md,
  corpus/knowledge/gate-git-read-guards-r68.md`. The new entry cites S436 for the replacement
  mechanism itself; the used-by counter (missing=1) caught the missing back-reference before
  landing. No row's `recheck` or `status` cell is edited this round; S437 is an append.

## Frontier and scope

Census start: `.ufo/waves/round-68/census-start-r68.txt` (committed at `2ca2bec3`), exit 0,
373 rows at round start; the base row count is re-derived at `510100c8` by
`git show 510100c8:corpus/SOURCES.md | grep -c '^| *S[0-9]'` → `373`, ids running `S001` to
`S436` with 5 gaps. One row is appended this round; the end census, its exit and the end row
count are L1 landing measurements (`TBD-INTEGRATION`), not claimed here.

No desktop claim, no PROVINCE frontier move, no compositor/socket/service write, and no `[x]` or
promotion is part of either claim. Assimilation: **none**. The connector seat
(`.ufo/waves/round-68/w1/R68ConnSiblings.md`) screened the `shokuknow/merge/mado` package (147
staged rows, 94/147 id collisions, zero rows bearing on C1 or C2) and the `considerthese`
proposals (none fits without widening); no sibling theme is adopted. Prior art owed and cited
as prior art only: kaidoku's guard-ordering defect F2
(`.ufo/waves/round-23/w1/CounterGitIsolation.md:75-91`), kama's battery family
(`tools/round56-env-leg-battery.py`, `round58-battery-exec-check.py`, `round59-c1-counter.py`),
tsukuroi's static-env instrument, and kagi's earliest guarded reader. The connector's optional
A/B probe of a purge-shaped gate is not part of the frozen denominator (see Controls).

## Controls and limits

### C1 — three frozen recipes (finite denominator 3; score `10 × killed / 3`)

Counting command (run from the lane root; `REV` is the measured revision, `DIR` scratch):

```sh
python3 quality/counters/c1-r68-selfmutants.py --repo . --rev REV \
  --base-rev 510100c81e6cf63fec6be380c2f2f9c670f32cbc \
  --scratch-root DIR
```

| id | find (exact text) | replace |
|---|---|---|
| S1 | `mr_killed = bool(` | `mr_killed = True or bool(` |
| S2 | `mz_killed = mz_rc != 0` | `mz_killed = True` |
| S3 | `killed = int(mz_killed) + int(mr_killed)` | `killed = 2` |

The rules, frozen at the declaration:

- `selftest=0` is the scored harness `quality/counters/c1-r68-landing-controls.py` extracted from
  `REV`, run with `--selftest`.
- Each recipe must occur exactly once in the extracted harness and yield a compilable mutant; a
  recipe whose target text does not occur exactly once is `applicable=no` and never counts.
- A mutant is **killed** iff its own `--selftest` exits nonzero. The scripted none-killed case
  expects `killed=0/2 … TARGET_MISSED`, so any forced credit changes the asserted line.
- `--base-rev` is the do-nothing control: the same three recipes applied to
  `quality/counters/c2-r67-landing-controls.py` at the base rev, each surviving (selftest rc 0).

Baseline at `510100c8`: `MADO_R68_SELFMUTANTS: selftest=absent killed=0/3 applied=0/3 base=0/3
verdict=TARGET_MISSED` rc 1 — the scored harness does not exist, and at the same rev all three
recipes applied to the r67 harness survive its selftest (`survivors=S1,S2,S3 killed=0/3 applied=3`).
Target line: `MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=<n>/3 verdict=TARGET_MET
rev=<REV>` rc 0; bounded score 0.0000 → 10.0000.

Limits: exactly these three call-site recipes on this one harness; not a claim of universal
self-test soundness or that every forged credit is caught. The scripted children are stubs; the
real child runs are exercised separately as a harm-watch receipt, not part of this denominator.
The counter does not authenticate the harness and does not prove its own mutants exhaustive.

### C2 — population and eleven classification cases (finite denominator 13 readers; score `10 × guarded / readers`)

Counting command (run from the lane root):

```sh
python3 quality/counters/c2-r68-reader-guard.py --repo . --rev REV \
  --controls .ufo/waves/round-68/controls/c2-controls.json \
  --scratch-root DIR
```

- Population: every tracked file matching `quality/check-[^/]+\.py` at `REV`, enumerated from git
  objects, never the worktree (20 files at the base).
- Reader: the blob contains a `git` command token **and** at least one quoted verb from the frozen
  vocabulary `show, cat-file, ls-tree, rev-parse, diff-tree, log, merge-base, for-each-ref`
  (13 files at the base).
- Guarded: the blob's AST constructs the string `GIT_NO_REPLACE_OBJECTS` in a dict-literal key, a
  subscript store on an env-named target, an env-named binding, a `dict()`/`update()` keyword, or
  inside an `env=` keyword value. A comment, a docstring, a bare prose mention or an unrelated
  dictionary handed to `env=` is **not** a guard.

| control case | expect_reader | expect_guard |
|---|---|---|
| `guarded-env-dict` | yes | yes |
| `unguarded-env-dict` | yes | no |
| `inherited-env` | yes | no |
| `comprehension-env` | yes | no |
| `subscript-store-guard` | yes | yes |
| `module-const-guard` | yes | yes |
| `comment-only-mention` | yes | no |
| `docstring-only-mention` | yes | no |
| `dict-keyword-guard` | yes | yes |
| `unrelated-dict-as-env` | yes | no |
| `non-reader` | no | no |

Target line: `MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=11/11
verdict=TARGET_MET rev=<REV>` rc 0. Baseline at `510100c8`: `population=20 readers=13 guarded=1
unguarded=12 controls=11/11 verdict=TARGET_MISSED` rc 1; bounded score 0.7692 → 10.0000.

Limits: the census classifies committed source text, not runtime behaviour. A guard set in a
branch never taken reads as guarded; a helper that receives its env from far away is classified
by the construction, not by dataflow to the call; a guard value is presence-tested, not
interpreted (`"0"`, `"false"` and `"1"` all count). It does not protect a repository already
rewritten, authenticate objects, prove state truth or cover the wider 76-file lexical reader set
from r67; only `quality/check-*.py` is in the denominator, and the gates are not executed by the
census.

Two freeze conflicts are recorded verbatim rather than smoothed:

1. The frozen counting command passes `--scratch-root DIR`, but the counter bytes committed at
   `e0727cda` (`quality/counters/c2-r68-reader-guard.py`, blob
   `8eb99a63e324fce18eda824d7aefa48d72650ff6abb7c4afa45def9191ce880e`, 13429 B) have no such
   argparse option, so the command as written exits 2 with `unrecognized arguments: --scratch-root`.
   The L1 accepted the flag at `2a39e74142e3c3710db7af0f4d73a7a6eac64831` (seat-reported; landed
   blob `0e853b1b11b3f327bc2c0e6a4aa6ce32a5fc5561d9575b0bf1bc548c7f4dfea8`, 14057 B), so the
   landed counter parses the frozen command. No predicate, control-set or declaration byte changed.
   The landing block records the command actually run and the counter hash at the measured revision.
2. The declaration's parenthetical at `.ufo/waves/round-68/claims-declaration-r68.md:114` names
   "frozen control cases 6, 8, 10, 11" as not-guards, but the frozen JSON's sixth case (the counter
   iterates its `cases` array in order) is `module-const-guard` with `expect_guard=true`. The
   non-guard cases by name are `comment-only-mention` (position 7), `docstring-only-mention` (8),
   `unrelated-dict-as-env` (10) and the non-reader `non-reader` (11). The counter scores by case
   name and expectation (`quality/counters/c2-r68-reader-guard.py:162-170`), so the predicate is
   unaffected; the parenthetical's index 6 is a frozen-text number-drift, reported here and not
   edited.

### Auxiliary hazard probe (outside the denominator)

One repaired gate is run twice against a scratch repository carrying a planted `refs/replace`:
the base bytes must read the forged object and the repaired bytes the real one, with the gate's
clean-run verdict recorded. `R68ExecHazard` used `quality/check-axis-scores.py`: with
`orig=4b085e39db3d2c61b607f5533031cb122d63393b` replaced by
`forged=59ff15d5a0f32e6a4954335eb687c9a8c731b28e`, raw `git cat-file -p` prints `forged bytes`,
base `mod.git(D, "cat-file", "-p", orig)` prints `forged bytes` while the repaired draft prints
`original bytes`; the census classifier reads base `(reader=True, guard=False)` and repaired
`(reader=True, guard=True)`; all 12 probe checks passed.

Sampling limit: this samples one of the twelve repaired gates, and it exercises the guard-after-
purge shape (the repaired env comprehension purges `GIT_*`, then stores
`env["GIT_NO_REPLACE_OBJECTS"]="1"`). It does not exercise the connector's guard-before-purge
negative control (`check-index.py` A/B), which the census would still count `guarded=yes` while
the guard is erased by the later purge; the probe is a sample of the repair, and the census count
is the claim.

### Integration placeholders (L1 landing only)

Remaining `TBD-INTEGRATION` values are superseded by the landing block appended by the L1 at
integration; the draft's own text is unchanged.

- C1 measured line (`selftest=… killed=… applied=… base=… verdict=… rev=…`) with its exit code and
  receipt path; the final sha256 of `quality/counters/c1-r68-landing-controls.py` and the counter
  at the measured revision; the three per-recipe mutant lines/diffs; the base-control value.
- C2 measured line (`population=… readers=… guarded=… unguarded=… controls=… verdict=… rev=…`)
  with its exit code and receipt path; the final sha256 of the landed counter and of the twelve
  repaired gate files; the census end receipt.
- The appended S437 row bytes and sha256, the `corpus/README.md` index row, the end census exit
  and row count (373 → 374 expected; measured at landing).
- Wave settlement counts and the wave-done receipt; the record-landing revision; the harm-watch
  counters (navigation, used-by, ledger, citations).
- The `--scratch-root` resolution and the exact counter hash at the record landing.

## Landing (L1 integration)

Measured content `379e97f884a6cf7ed3ac96068b0165d63495524f`; measured commands and exit codes in
`.ufo/waves/round-68/measurement-final-r68.txt`, the selftest battery in
`measurement-selftests-r68.txt`, the preliminary run at `18d692f3` in
`measurement-preliminary-r68.txt`.

- C1 at `379e97f8`: `MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=0/3
  verdict=TARGET_MET rev=379e97f8…` rc 0; candidate harness sha256 `25470bc4…f5527`, selftest
  52/52; the three mutant diffs printed with their sha256; the base harness (sha256
  `a4376fa7…9b58`, 47/47) survives all three recipes (`S1,S2,S3 killed=0/3`).
- C2 at `379e97f8`: `MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0
  controls=11/11 verdict=TARGET_MET rev=379e97f8…` rc 0; selftest 25/25.
- Standing instrument at `379e97f8`, round-68 scope: `MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0
  ledger=0 citecheck=0)`; navigation `indexed=80/80`, used-by `entries=80 rows=374 missing=0`,
  ledger `population=113 ledger_rows=113 uncovered=0`, citations `11/11` resolved.
- Selftests: gate `MADO_SELFTEST: 460/460`; landing 62/62; C1 counter 26/26; C2 counter 25/25;
  harness 52/52; used-by 16/16; ledger 54/54; citecheck 12/12; wave-done 62/62.
- Criterion 107 on the new entry: `CHECK107: rows=8 covered=8 miss=0 verdict=OK` (eight evidence
  rows, all S437 + `git-cat-file.adoc:<line>`, `eof=unchecked` — the anchor names no `pin` path).
- Census exit 0 at both ends; rows 373 → 374 (S437 append; tier histogram shifts by one A); no
  existing `status`/`recheck` cell changed; S436 `used-by` changed as logged above.
- Axis publication: this round publishes a fresh axis table (`SCORECARD.md`, round-68 section)
  re-derived at `379e97f8`: navigation 80/80, calibration resolved-active 86/86, operability
  selftest 12/12 — closing the navigation staleness (71/71) left since round 56.
- Mutation battery (`w1/R68MutBattery.md`): the three harness recipes and the C2 classifier's
  reader/guard/control rules are killed by the counters' selftests; the *counters' own wiring* is
  not self-tested — mutants that drop the C1 base leg, count `recipe=none` as killed, invert the
  kill test, drop the `selftest rc 0` term or force `unguarded = 0` survive their selftests (the
  C2 `unguarded = 0` mutant forges the base line to `TARGET_MET`). Named residuals, outside the
  claims' denominators: the claim is the artifact measured by the frozen command, not a proof that
  the counter cannot be rewritten.
- Disclosed by the attack seats, not smoothed: C1 survivors under multi-point forgeries
  (`forged_credit` term dropped; `mz_rc is None` credited; the hermeticity guard removable) —
  RevC1; the C2 classifier's value-position over-inclusion (a key string in a value reads as a
  guard) and the guard-dominance hazard
  (`dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` filtered by `GIT_*` reads forged bytes while
  classified guarded) — RevC2 and the connector, receipts in `aux-dominance-r68.txt`; and the two
  counter defects M68-3/M68-4 fixed before landing with red-before receipts.

Mistake IDs as filed (closure note): M68-1 (r67 harness selftest never runs its decision body),
M68-2 (r67 kill-rule sentence did not describe the delivered observable), M68-3 (r67 "controls
unchanged" sweep is path-vacuous), M68-4 (the frozen C2 command passed an argument the counter did
not accept), M68-5 (the C2 verdict did not enforce the frozen population/reader counts). The
round-68 critic (B3) caught two rows sharing `M68-3`; the rows were renumbered before closure.

### Closure corrections from the critic seat

- **B1** (frozen `controls=11/11` unenforced): fixed as M68-6 above; instrument-only.
- **B2** (axis-posture numbers in the declaration cite `78/78`/`108/108` where the cited receipt
  reads `79/79`/`110/110`): the declaration is frozen and is not edited; the erratum is
  `.ufo/waves/round-68/axis-posture-erratum-r68.txt`, and the conclusion (all published sub-axes
  at their measured maximum) is re-derived at `379e97f8`.
- **B3** (duplicate `M68-3`): rows renumbered before closure (see the closure note below the table).
- **B4** (docstring token `recipe=none` vs emitted `applicable=no`): docstring corrected to the
  emitted token; the printed contract line never carried the token.
- **B5** (`CONTRACT_RE` only exercised on selftest literals): both `measure()` bodies now
  `fullmatch` the assembled line and fail closed (`rc 2`) on a format drift.
- **B6** (an uncalled dead guard satisfies the census; a planted replacement does not move such a
  gate): declared limit, restated in the entry's §5 dominance/no-dataflow bullets; the production
  twelve repairs are wired, one gate has a runtime hazard receipt, eleven have behaviour-identity
  runs only.
- **B7** (C1 already `TARGET_MET` at the harness cutover, before any seat returned): correct, and by
  design. The scored harness is the L1's own instrument, committed at `40d2bef8` (22:06:33), 8 s
  after the wave dispatch marker (22:06:25) and 43 s after the wave registry `createdAt`
  (22:05:50 local). The claim's Before state is the base rev `510100c8` and the freeze `e0727cda`
  (22:04:51) precedes the registry and the harness, so the chronology rule holds; the note for the
  closure is that no seat is credited with constructing the scored artifact — the seats attacked it
  and the counter measures it at the named revision.
