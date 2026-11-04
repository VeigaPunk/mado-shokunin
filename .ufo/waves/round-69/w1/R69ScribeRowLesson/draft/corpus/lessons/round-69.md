# mado round 69 — lesson

author: mado L1, integrated from one w1 wave; outside-lane closure remains authoritative.
date: 2026-11-03
base: `04093b83f73a841117d3b31dbb2a6063f4f2a454` (lane tip at round start; round 68 closed there)
measured content: `5fc29ae72e66b9347d576c796ee656aea2fdd04c` (receipts `measurement-c1-r69.txt`,
`measurement-c2-r69.txt`, `harm-watch-r69.txt`, committed at `6a5cefd2`)
frozen declaration: `.ufo/waves/round-69/claims-declaration-r69.md` @ `789a87f1a667b43dd759222a2f048bf8f75b43ce`
(blob `94bd13466f55116fe9d655e5be69557162b6cff8`, 11575 B, sha256
`ecd481ae3e21ff5653d21a1b2151bf95d327b1689d3a861172f047d83d924b43`; the working copy hashes to the
same blob as the freeze).
control set: `.ufo/waves/round-69/controls/c2-controls-r69.json`, sha256
`975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9` (11 cases; blob
`726771c5d42212711217175f189fbcc46bbdfcb6` at the freeze).
pre-freeze baseline: `.ufo/waves/round-69/control-baseline-r69.txt`, blob
`fd98cfb87aa6df93a95ce53f738d58d1a51f0686` (3731 B, sha256
`f2054c0edd768ab34dd6c9f7cf3180c91db471cbd3b2fad84da21dd027e86cee`).

## Outcome and boundaries

Two bounded claims on distinct axes, both frozen before candidate construction. The frozen rolls
are the declaration's fixed values; the declaration records no die or dice line, so the numbers
below are the rolls the round was played with, and the measured values are what those rolls
returned.

- **C1 calibration — the hardened control harness kills paired (decision + oracle) forgeries.**
  At the measured revision `quality/counters/c1-r69-paired-recipes.py` extracts
  `quality/counters/c1-r69-landing-controls.py` from `REV`, runs its `--selftest` (rc must be 0),
  applies each of the three frozen recipes R1/R2/R3 exactly once (`applicable=no` when a recipe's
  text does not occur exactly once), and counts a mutant killed iff its own `--selftest` exits
  nonzero; the same three recipes are applied at `--base-rev` to the round-68 harness, which must
  survive all three. Frozen rolls: `selftest=0 killed=3/3 applied=3/3 base=0/3`, bounded score
  `10 × killed / 3`, contract line
  `MADO_R69_PAIRED_RECIPES: selftest=<rc|absent> killed=<n>/3 applied=<k>/3 base=<m>/3 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>`.
  Measured at `5fc29ae7`: the extracted harness is 37647 B (sha256 `b374cfb8…`) and its selftest
  prints `MADO_R69_LANDING_CONTROLS_SELFTEST: 59/59 assertions passed`; the three mutants occur
  once each and die at 57/59, 58/59, 57/59 (`killed=yes`, rc 1); the base leg keeps the round-68
  harness green at 52/52 on all three (`killed=no`), so the final line reads
  `selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=5fc29ae72e66b9347d576c796ee656aea2fdd04c`
  with rc 0 (`measurement-c1-r69.txt`). Before, at the base `04093b83`, the scored harness is
  absent (`selftest=absent killed=0/3 applied=0/3 base=0/3` → 0.0000), and the do-nothing control
  applies the same recipes to the round-68 harness and reads `killed=0/3 applied=3/3`: all three
  survive its green 52/52 selftest (`.ufo/waves/round-69/control-baseline-r69.txt` § C1 base). The
  counter's own selftest is `MADO_R69_PAIRED_RECIPES_SELFTEST: 23/23` (harm watch).

- **C2 operability — the guard census requires key position and dominance, not a mention.**
  At the measured revision `quality/counters/c2-r69-guard-dominance.py` reads the tracked
  `quality/check-[^/]+\.py` population, counts `GIT_NO_REPLACE_OBJECTS` only in key position of an
  environment mapping that reaches a git launch by one of three one-module flows (inline `env=`, an
  env-named binding or producer used at the call with no intervening rebinding, or a locally defined
  callee's env-named parameter), refuses constructions inside a literal-false branch, and scores
  every one of the 11 frozen cases on both `expect_reader` and `expect_guard`; it refuses a control
  file whose case count is not 11 or whose sha256 differs from the frozen digest. Frozen rolls:
  `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11`, bounded score
  `10 × guarded / readers` = 10.0000; the population is already 13/13 at `04093b83`, so the claim
  moves **discrimination**, not the count, and says so. Measured at `5fc29ae7`: the receipt lists
  all 20 population files (13 readers, each `guard=yes`, the other seven `reader=no guard=no`), all
  eleven cases `correct=yes`, the base classifier on the same cases `controls=7/11` (accepting
  `value-position-only`, `dead-branch-only`, `uncalled-helper`, `overwritten-env`), and the final
  line `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11
  verdict=TARGET_MET rev=5fc29ae72e66b9347d576c796ee656aea2fdd04c` with rc 0
  (`measurement-c2-r69.txt`). Before, at the base, the r69 counter does not exist (missing counter,
  rc 1), and its *rule* — the round-68 classifier — reads `controls=7/11` on the same frozen set
  (`control-baseline-r69.txt` § C2). The counter's own selftest is
  `MADO_R69_GUARD_DOMINANCE_SELFTEST: 32/32` (harm watch).

**Open harm item.** At the measured snapshot the hermetic gate reads `MADO_SELFTEST: 460/460`
(rc 0), the axis table reads `checked=3 mismatched=0` (rc 0) and all five instrument selftests read
rc 0, but `harm-watch-r69.txt` also records `landing_rc=2`: the standing landing instrument refused
its citecheck leg because `.ufo/waves/round-69/measurement-c1-r69.txt` was uncommitted at that run
(`citecheck path has uncommitted changes`). The declaration's harm watch requires
`MADO_LANDING_COUNTERS: GREEN`, so the standing instrument is **not established** at `5fc29ae7`;
the round re-runs it against the committed receipt and reports that run, rather than reading the
refusal as green.

**Not claimed.** Universal fault coverage; that R1/R2/R3 are the only forgeries; that an outside
attacker cannot reforge a printed line; runtime behaviour of the extracted instruments (the
harness's real-children leg stays the harm-watch leg); that R1/R2/R3 are equivalent to any
historical round-68 recipe (they are not, and recipe L is excluded as an equivalent mutant);
soundness of the dominance rule for arbitrary Python (a bounded syntactic approximation: one
module, one hop, no alias/attribute/container flow, no path-sensitivity beyond a literal-false
branch, no cross-module producer); that a guarded environment makes the guard effective at runtime
(the value is not interpreted, and `GIT_NO_REPLACE_OBJECTS=0` also disables); that the 20-file
population is the lane's whole reader set (r67's wider lexical set stays outside); that the
`quality/` register is exhaustive; state truth of any `PROVINCE.md` cell. Neither claim re-scores a
rule the lane already holds, and no alias or compatibility shim is added for a predecessor counter.

## Mistakes

| mistake | class | evidence | captured-by | fix and failure it can now show |
|---|---|---|---|---|
| M69-1: the round-68 reviewer's row L (`mz_killed = mz_rc != 0` → `mz_killed = mz_rc != 0 or mz_rc is None`) was recorded as a surviving credit widening and a forgery "reachable in a real measurement run". It is an equivalent mutant: the frozen text sits inside `try:` after `mz_rc = r.returncode`, so `mz_rc` is an int and the added disjunct is always false — the edit cannot change any printed line. | equivalent-mutant | `.ufo/waves/round-68/w1/R68RevC1.md:54` (row L "SURVIVED", rc=0 52/52), `:66` (finding 3, "credits a kill when the M-Z recipe itself errors") and `:74` ("survivors G and L are real credit forgeries reachable in a real measurement run"); `quality/counters/c1-r68-landing-controls.py:435,439` (`mz_rc = r.returncode`, then `mz_killed = mz_rc != 0`, both in the `try:` body); `.ufo/waves/round-69/control-baseline-r69.txt` § L probe — the recipe occurs once and the mutant keeps a green 59/59 selftest with `killed=no`, and the same edit kept the r68 harness green at 52/52. | `none` — r28's mutation-testing rule says equivalent mutants bound the denominator, but no QUALITY criterion required a frozen recipe to change a scripted case's printed line, so an edit that changes none was counted as a live mutant by the reviewer. | The frozen set excludes L and states the rule before freeze: every recipe must change a scripted case's printed line, and the failure it can already show is named (R1 the forged-credit case `forged credit is rc0 + TARGET_MET + missing=0`; R2 the unparseable-summary case; R3 the no-spawn assertion). Failure it can now show: the receipt's L probe — an edit that cannot change a printed line leaves the selftest green and `killed=no`, so it is a non-mutant, not a survivor; the landed set kills R1/R2/R3 where the r68 harness survives them. |
| M69-2: the round-68 C2 classifier counts the guard from any occurrence of the key string, so `{"LABEL": "GIT_NO_REPLACE_OBJECTS"}` in value position classified as guarded (measured `7/11` on the frozen set). | over-inclusion | `.ufo/waves/round-69/control-baseline-r69.txt` § C2 — `value-position-only r68=(True, True) proto=(True, False) expect=(True, False)`, and the same r68/proto/expect split for `dead-branch-only`, `uncalled-helper` and `overwritten-env`; `MADO_R69_C2_BASE: controls=7/11`, and the landed base leg re-reads the same `controls=7/11` (`measurement-c2-r69.txt`). | `none` — the r68 rule and its 11-case set did not distinguish key position, and no prior criterion tested a value-position mention. | The r69 rule counts the key only in key position of an environment mapping that reaches the git launch, with the four cases the r68 rule accepted as its red set; the same frozen set reads `controls=11/11` under the landed counter at `5fc29ae7`, and the frozen counter refuses a control file whose case count is not 11 or whose sha256 differs from `975ca3ba…`. Failure it can now show: the r68 `7/11` receipt above is the red state; the landed `11/11` is the green. |

A fix counts only on its named red/green evidence. M69-1's red is the L probe (a non-mutant read
as a survivor) and its green is the landed `killed=3/3 base=0/3`; M69-2's red is the frozen set
read `7/11` by the r68 rule and its green is the landed `controls=11/11 base_controls=7/11`.

## Gate

- **ADMIT — S438, `git v2.56.0 Documentation/git.adoc`.** URL
  `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`, accessed
  2026-11-03 (three fetches, byte-identical, sha256
  `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`, 47005 bytes), anchored at
  `git.adoc:14` (SYNOPSIS carries `--no-replace-objects`), `:178-182` (the flag's documented
  equivalence) and `:927-929` (`GIT_NO_REPLACE_OBJECTS` in ENVIRONMENT). Located quote (18 words):
  "Setting and exporting this environment variable tells Git to ignore replacement refs and do not
  replace Git objects." Reason: the sentence makes the export the documented condition, which is
  exactly the dominance ground C2 measures — a guard that is merely constructed is not in effect
  for any child; only the environment handed to the process carries it. Registry mechanics: the
  census at round start is rc 0 with 374 data rows and the two standing W04 warnings (S394, S395);
  no row anywhere in the registry carries this URL (`grep 'Documentation/git.adoc'
  corpus/SOURCES.md` → no match), so S438 is not a duplicate of S436 (`git-replace.adoc`) or S437
  (`git-cat-file.adoc`) — same tag, different files — and it appends after S437 as the 375th row.
- **REJECT — a second row on the same file's `OPTIONS` sentence** (`git.adoc:178-182`:
  "--no-replace-objects" / "Do not use replacement refs to replace Git objects." / "This is
  equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable with any value.").
  Reason: the sentence documents a command-line flag's equivalence, not the environment handoff C2
  measures; admitted as its own row it would let the C2 entry cite text that says nothing about a
  mapping reaching a launch, and once both rows carry the same URL the census cannot tell the
  anchors apart — the entry would cite ground it does not have. Flip condition: a claim that
  measures flag propagation (the flag present in the child's argv) with one control that plants the
  flag and one that removes it; then the OPTIONS sentence is the right anchor and the row is
  admissible on its own.
- **Ordering note.** The census E11 rule reads every `mined` row's used-by path on disk, and both
  paths this row names (`corpus/knowledge/gate-guard-dominance-r69.md`,
  `corpus/lessons/round-69.md`) are round-69 deliverables; a minimal-registry census fixture with
  the row and both paths present reads `ok` rc 0, and the same fixture with the paths absent reads
  `E11 S438 missing used-by` rc 1. The row is a scribe draft: the declaration requires it to be
  opened independently by the scout and admitted only through the lane's Gate, so this section
  records a proposed admission, not an admission.
