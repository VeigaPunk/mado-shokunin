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
  `10 × killed / 3`. At the base `510100c8` the score is 0/3: the scored harness is absent, and
  the same three recipes applied to `quality/counters/c2-r67-landing-controls.py` at the base
  all survive its green 47/47 selftest (`survivors=S1,S2,S3 killed=0/3 applied=3`).
- **C2 operability — the standing gates' git-object reads are guarded.** At the measured
  revision the frozen census over `quality/check-[^/]+\.py` reads 20 files from git objects,
  classifies 13 readers, and requires 13 guarded readers, 0 unguarded, plus 11/11 frozen
  classification cases. `population=20` and `readers=13` are part of the target; a repair may
  not shrink the denominator. Bounded score `10 × guarded / readers`. At the base
  `510100c8` the census reads `guarded=1 unguarded=12` (0.7692); the only guarded reader is
  `quality/check-tool-ledger.py`.

**Not claimed.** State truth of any PROVINCE cell; universal fault coverage; honest or
authenticated invocation; runtime behaviour of the gates or of the guard (the census classifies
committed source text, and the hazard probes sample gates, not the population); protection against a repository
already rewritten; object authenticity; exhaustive harness mutants; lane-wide coverage (the
wider lexical reader set from r67 remains outside this gate population); desktop, compositor,
session or service health; any `[x]`, promotion or axis retirement. Both claims are
finite-control claims and no wider guarantee is read out of a green count. Seat and wave
demonstrations are not the committed-revision measurement; the L1 landing block below carries
`TBD-INTEGRATION` for those values.

## Mistakes

| mistake | class | evidence | captured-by | fix and failure it can now show |
|---|---|---|---|---|
| M68-1: the r67 harness's `--selftest` never executes its `measure()` decision body, so a forced kill credit (`mr_killed = True`, and the frozen S1 form `mr_killed = True or bool(`) keeps the selftest green at 47/47 while the harness reports `killed=2/2`. | survivor | `corpus/lessons/round-67-verifier-spotcheck.md:181-183` (routed defect 3, `mr_killed = True`); `.ufo/waves/round-68/control-baseline-r68.txt:17-22` — S1 `mr_killed = bool(` occurs once in `quality/counters/c2-r67-landing-controls.py` at 510100c8 (blob `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58`, 30697 B), the mutant's selftest exits 0 with 47/47 assertions and `killed=no`, and `MADO_R68_BASE_CONTROL survivors=S1,S2,S3 killed=0/3 applied=3`. | `none` as an enforced r67 rule — the r67 claim accepted the harness selftest green, and the outside spot-check caught it first (defect 3). QUALITY 110(b) now records the rule: a credit must come from a test that drives the decision code. | The r68 C1 claim scores exactly this. `quality/counters/c1-r68-landing-controls.py` (at `40d2bef8`, blob `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527`, 36005 B) drives the real `measure()` with scripted children, and `quality/counters/c1-r68-selfmutants.py` (freeze blob `bdea8dc6b4455f45c59896a44f0bd4ede21c26b82c67e0618a05ac069ef50a85`, 12769 B) applies S1-S3 once each and requires each mutant's own `--selftest` to exit nonzero; the none-killed case asserts `killed=0/2 … TARGET_MISSED`. Failure it can now show: at 510100c8 S1 leaves the r67 harness green (`rc=0 assertions=47/47`); the r68 harness's own selftest at `40d2bef8` goes red under S1/S2/S3 (51/52, 51/52, 50/52, `R68RevC1`), and the frozen counter at `40d2bef8` prints `killed=3/3 … base=0/3 verdict=TARGET_MET` rc 0 (seat measurement; record landing `TBD-INTEGRATION`). |
| M68-2: the frozen C2 counting command passes `--scratch-root DIR`, but the counter committed at `e0727cda` has no such argument, so the exact declared command exits 2 with `unrecognized arguments`. | landing | Declaration `.ufo/waves/round-68/claims-declaration-r68.md:90-95`; counter at `e0727cda` (blob `8eb99a63e324fce18eda824d7aefa48d72650ff6abb7c4afa45def9191ce880e`, 13429 B) argparse lacks the flag; `R68ExecHazard` §2 found it; `.ufo/waves/round-68/c2-command-erratum-r68.txt` (committed at `2a39e741`) records red `rc=2`, then the same command at the base rev teaches `TARGET_MISSED` rc 1 and `--selftest` 18/18. | `none` at freeze; the executor's verbatim run caught it. QUALITY 110(a) now records the rule: a counter is frozen only after its declared command is run verbatim, and an argument the instrument does not accept is a freeze defect. | The L1 accepts the flag at `2a39e74142e3c3710db7af0f4d73a7a6eac64831` (blob `0e853b1b11b3f327bc2c0e6a4aa6ce32a5fc5561d9575b0bf1bc548c7f4dfea8`, 14057 B) and the selftest asserts the frozen argument set parses. Instrument only; no predicate, control-set or declaration byte changes. Failure it can now show: the erratum's red-before `rc=2` and the fixed command's base line are in the same file. |
| M68-3: the C2 census's verdict accepted `readers>0` and `unguarded==0` and all controls correct without requiring the frozen `population=20`/`readers=13`; deleting a repaired gate's object-read verbs yields `readers=12 guarded=12 unguarded=0 controls=11/11 verdict=TARGET_MET` rc 0. | scope | `R68RevC2` finding 1; `.ufo/waves/round-68/c2-denominator-erratum-r68.txt` (committed at `686d6345`): red line `readers=12 … TARGET_MET` rc 0 against the counter at `2a39e741`, green line `readers=12 … TARGET_MISSED` rc 1 against the fixed counter, `--selftest` 25/25. | `none` at freeze — the counter's verdict was looser than the frozen predicate; `R68RevC2` caught it. The fix carries its own red/green erratum. | `verdict_met()` at `686d6345` now requires `population==20` and `readers==13` as well as `unguarded==0` and every control correct; the selftest adds the five verdict assertions and the `update()`/annotated-binding guard cases (25/25). Failure it can now show: the same reader-deletion fixture reads `TARGET_MISSED` rc 1, so the denominator cannot be shrunk by deleting reads. |
| M68-4: the r67 C2 kill rule described a mechanism the delivered M-R control does not use — the rule said the candidate control run "exits nonzero on the mutant", while M-R's child exits 0 and is counted killed by the forged-credit flip. | reference-drift | `corpus/lessons/round-67-verifier-spotcheck.md:173-177` (routed defect 1); `.ufo/waves/round-67/measurement-c2-after.txt:19` at `caf131d6be04dd2ccc742636625c1ce196610522` — `MADO_R67_MUTANT M-R … rc=0 verdict=TARGET_MET missing=0 forged_credit=yes killed=yes`. | `none` — no QUALITY criterion compared a frozen kill-rule sentence with the control's printed observable; the outside spot-check caught it. QUALITY 96 covers a landed tool contract's out-of-contract list, not a kill-rule sentence. | The r68 predicates freeze the observable each counter prints: C1's kill is "the mutant's own `--selftest` exits nonzero", with the none-killed case asserting `killed=0/2 … TARGET_MISSED`; C2's predicate is the AST classification count with the 11 named control cases, not a child-exit sentence. Failure it can now show: the r67 M-R receipt reads `rc=0 … killed=yes`; under the r68 C1 rule an exit-0 mutant is not killed, so the rule cannot silently describe a different mechanism. |
| M68-5: the r67 "controls unchanged" sweep is path-vacuous — `git diff aa7fe5a1..HEAD -- controls` from the lane root matches no path, so it prints empty regardless of the change. | vacuous | `corpus/lessons/round-67-verifier-spotcheck.md:178-180` (routed defect 2); at lane head `92151a50cc79b40700cafab98488012089f67e34` / report `7111b67bec4c129ec49ef22d3b703262fd72ed36`, `git ls-tree -r --name-only 92151a50 \| grep -c '^controls/'` → `0`, while `git diff aa7fe5a1 92151a50 -- ':(glob)**/controls/**'` prints 15 lines, including `score-baseline-c2.py`'s default base `eafd500f` → `0b28ffb4` at `5f9ce459`; the frozen `c1-controls.json` is byte-identical at both revs. | QUALITY 62 — a zero count is evidence of absence only when the same channel is shown to carry the class being counted; the bare path was never positively probed. | The round-68 lesson and receipts use the explicit nested path and state the base correction beside the unchanged control set; failure it can now show: the bare path prints 0 lines on a diff whose nested path prints 15, so the sweep cannot be read as "controls unchanged". |

A fix counts only on its named red/green evidence. M68-1's green is the record-landing measurement;
M68-2 and M68-3 carry their red/green in the errata committed at `2a39e741` and `686d6345`; M68-4
and M68-5 are reference/process fixes with their red states at the named revisions.

## Gate

Admitted: **S437**, scoped to the lane's git object-read census — not a desktop fact. The row was
drafted by `R68ScribeKnowledge` at
`.ufo/waves/round-68/w1/R68ScribeKnowledge/draft/corpus/SOURCES-row.txt` (sha256
`cbf4cf5ef05b0ca3381b2a6b5222049607c0ad055a97a463e56ff8b0e1eaac05`, 1068 B, one line, 11 cells,
no literal or escaped pipe), and independently opened by `R68ScoutSources`
(`.ufo/waves/round-68/w1/R68ScoutSources.md`): the scout fetched the tag twice and the peeled
commit once (`cmp` rc 0), checked the 12 cited line quotes verbatim, the row's sha256/byte count,
the next id and the duplicate-URL scan, and counted the three C1 recipe texts 1x each in both
harnesses. The row is an append; the only existing-cell change is S436's used-by, recorded below.

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
- Reject (candidate row): `Documentation/git-config.adoc` @ v2.56.0 (sha256 `655541c2…`) — the
  config plane (`get`/`set`, `--replace-all`, deprecated forms), with zero `cat-file` and zero
  `GIT_NO_REPLACE_OBJECTS` occurrences; it cannot ground an object-read row. Flip: an admitted
  scope that turns on the config plane (e.g. whether a config key can flip replacement behaviour).
- Reject (claim, outside read): "`git cat-file -e` establishes object authenticity or integrity."
  The page says `-e` exits zero if the object "exists and is a valid object" (lines 49-52) and
  prints nothing unless the object is malformed (line 291) — existence and format validity, not
  provenance or content truth. Flip: a signature/verification sentence in the same file, or a
  lane instrument that pins object bytes to a digest rather than testing presence.
- Row nits from the scout, recorded not silently fixed: the draft anchor cited `:40`, `:44`, `:50`
  where the sentences wrap; the L1's appended S437 at `18d692f3` carries the corrected spans
  `:40-41,:44-45,:50-51`. The remaining teaches-cell nits are the abbreviation of
  `linkgit:git-rev-parse[1]` and the dropped nested quotes around `"replace"`. No shape or id
  defect; the appended bytes are the landing value.
- Recheck/status/used-by cell changes old→new: **S436 used-by only**. At `425d4b2f` the S436
  used-by cell is `corpus/lessons/round-67.md, corpus/knowledge/replace-ref-citation-boundaries-r67.md`;
  at `18d692f3` it is the same cell plus `corpus/knowledge/gate-git-read-guards-r68.md`. No recheck
  or status cell changes; S437 is an append. The new row's recheck is `90d`. The r68 SOURCES sweep
  paragraph appended at `18d692f3` says "No existing status, recheck, used-by or opened cell
  changed.", which contradicts that same commit's S436 used-by edit: the row-level change is the
  intentional one, and the sweep sentence is the drift.

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
tsukuroi's static-env instrument, and kagi's earliest guarded reader. The round's lane-instrument
records are the three counters/harness under `quality/counters/`, the twelve repaired gate files,
`SKILL.md`'s two new registry rows, `PROVINCE.md`'s round-68 refinement paragraph and QUALITY 110;
none moves the desktop frontier.

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
rev=<REV>` rc 0; bounded score 0.0000 → 10.0000. Seat measurement at `40d2bef8` (`R68RevC1`):
`selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0, with the three hand-applied
mutants red at 51/52, 51/52 and 50/52; the record landing re-run is `TBD-INTEGRATION`.

Limits: exactly these three call-site recipes on this one harness; not a claim of universal
self-test soundness. The scripted children are stubs; the real child runs are a harm-watch
receipt, not part of this denominator. The C1 reviewer's break-the-selftest battery found
survivors beyond the frozen three, all within the declared boundary: paired decision+oracle
edits (D1/D2c), dropping `forged_credit` from the M-R gate (G), crediting a kill when `mz_rc is
None` (L), and removing the no-spawn guard (I). The counter scores the harness selftest exit,
not those wider shapes, and does not authenticate the harness.

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
unguarded=12 controls=11/11 verdict=TARGET_MISSED` rc 1; bounded score 0.7692 → 10.0000. Seat
measurement (`R68RevC2`, fixture carrying the twelve repaired drafts, rev `f17140c1`):
`population=20 readers=13 guarded=13 unguarded=0 controls=11/11 verdict=TARGET_MET` rc 0; the
record landing re-run is `TBD-INTEGRATION`.

Limits: the census classifies committed source text, not runtime behaviour. A guard set in a
branch never taken reads as guarded; a helper that receives its env from far away is classified
by the construction, not by dataflow to the call; a guard value is presence-tested, not
interpreted (`"0"`, `"false"` and `"1"` all count). The classifier's `carries_key` accepts any
constant equal to the key anywhere in an env-named binding or `env=` subtree, so
`env={"LABEL": "GIT_NO_REPLACE_OBJECTS"}` reads guarded although no guard key is set — the
declaration's "inside an `env=` keyword value" clause is wider than a key-position test, and this
is a disclosed over-acceptance beyond the comment/docstring/unrelated-dict rejects. At the freeze
bytes the classifier also missed an `env.update(GIT_NO_REPLACE_OBJECTS="1")` receiver and an
annotated env literal; both are named in the declaration's guard shapes, both are accepted after
`686d6345` (selftest 25/25), and the frozen 11 cases are unchanged. The guard does not protect a
repository already rewritten, authenticate objects, prove state truth or cover the wider 76-file
lexical reader set from r67; only `quality/check-*.py` is in the denominator, and the gates are
not executed by the census.

**Dominance is not seen.** `.ufo/waves/round-68/aux-dominance-r68.txt` records a repaired
`check-index.py` variant that builds the guard and then filters every `GIT_*` name, including
`GIT_NO_REPLACE_OBJECTS` itself: the census classifies it `guarded=yes`, while the gate reads the
forged bytes under a planted `refs/replace`. The correct repair stores the key after the purge;
the census is presence-only and cannot see the order. The hazard probe and the reviewer's
end-to-end sample exercise the correct shape (see below); the census count is the claim, and its
`guarded=13` does not mean every guard is ordered correctly.

### Auxiliary hazard probe (outside the denominator)

One repaired gate is run twice against a scratch repository carrying a planted `refs/replace`:
the base bytes must read the forged object and the repaired bytes the real one, with the gate's
clean-run verdict recorded. `R68ExecHazard` used `quality/check-axis-scores.py`: with
`orig=4b085e39db3d2c61b607f5533031cb122d63393b` replaced by
`forged=59ff15d5a0f32e6a4954335eb687c9a8c731b28e`, raw `git cat-file -p` prints `forged bytes`,
base `mod.git(D, "cat-file", "-p", orig)` prints `forged bytes` while the repaired draft prints
`original bytes`; the census classifier reads base `(reader=True, guard=False)` and repaired
`(reader=True, guard=True)`; all 12 probe checks passed. `R68RevC2` adds an end-to-end sample on
`quality/check-landed-contract.py`: with a planted replacement on the contract blob the base gate
reads the forged contract and returns `rc=1 … verdict=NARROWED`, while the repaired gate reads the
real blob and returns `rc=0 … verdict=OK`.

Sampling limit: this samples two of the twelve repaired gates, and both exercise the guard-after-
purge shape (the repaired env comprehension purges `GIT_*`, then stores
`env["GIT_NO_REPLACE_OBJECTS"]="1"`). It does not exercise the dominance negative control, which
the census would still count `guarded=yes` while the guard is erased by the later purge; the
probe is a sample of the repair, and the census count is the claim.

### Freeze-text conflicts and reviewer findings

1. The declaration's parenthetical at `.ufo/waves/round-68/claims-declaration-r68.md:114` names
   "frozen control cases 6, 8, 10, 11" as not-guards, but the frozen JSON's sixth case (the
   counter iterates its `cases` array in order) is `module-const-guard` with `expect_guard=true`.
   The non-guard cases by name are `comment-only-mention` (position 7), `docstring-only-mention`
   (8), `unrelated-dict-as-env` (10) and the non-reader `non-reader` (11). The counter scores by
   case name and expectation (`quality/counters/c2-r68-reader-guard.py:162-170` in the freeze
   bytes), so the predicate is unaffected; the parenthetical's index 6 is a frozen-text
   number-drift, reported here and not edited.
2. QUALITY 110's ground sentence names `M68-1` and `M68-2`. In the lesson integrated at
   `18d692f3`, `M68-2` is the M-R kill-rule row, not the frozen-command defect that QUALITY
   110(a) describes; this draft renumbers `M68-2` as the command defect (`landing` class) and
   moves the M-R kill rule to `M68-4`, so the criterion's ground matches its text. The L1 landing
   must reconcile the ids or amend the criterion's ground.
3. The C2 command and denominator defects are M68-2 and M68-3, with their errata at
   `.ufo/waves/round-68/c2-command-erratum-r68.txt` and
   `.ufo/waves/round-68/c2-denominator-erratum-r68.txt`. Both repairs are instrument-only; the
   predicate, the 11 control cases and the recipes are unchanged.
4. The C1 reviewer's after line is a seat measurement at `40d2bef8`, not the record landing; the
   C2 reviewer's 13/13 line is a fixture measurement with the twelve drafts, not the lane. The
   lane measurements at the record landing are in the L1 landing block.

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
- The final status of the integration chain at draft time (`40d2bef8` harness, `2a39e741`
  scratch-root, `686d6345` denominator/guard shapes, `425d4b2f` twelve gates/SKILL/PROVINCE/
  QUALITY 110) and the exact counter hash at the record landing.
