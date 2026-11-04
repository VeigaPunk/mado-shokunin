# Round 85 — declaration-identity causes and producer status classes

Lane mado, hyaku run 15, one v1 wave. Base `5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`; instrument
freeze `3905311c75a39c5710413105865c0a1a7dd0116a`; successor `d7c40e6d1b9a7476f2ff48254d577799ce9901e4`.
Declaration `.ufo/waves/round-85/claims-declaration-r85.md`.

C1 (coverage) binds a declaration-identity refusal to its own `cause=` token over 72 frozen cases and
51 declared mutants; C2 (operability) binds each executable runbook row to a producer status class
(`ok` / `exact` / `signal`) over 36 frozen rows and 37 declared mutants. **C1's frozen predicate
verifies; C2's frozen instrument never ran a case, and the successor scores 36/36 rows but only
33/37 kills.** The round is an honest stop for C2. No capability is admitted here; outside-lane
closure is the integrator's.

Every number below is labelled: `re-executed` = run by this seat in this round; `evidence-verified`
= read from committed bytes or from another seat's committed receipt, not re-run here.

## Mistakes

| id / class | evidence pointer | captured-by | fix shown able to fail |
|---|---|---|---|
| **M85-1 / survivor** — round 84 bound a refusal by its *stage* only, so a tool that refused the right stage for the wrong reason scored | `corpus/lessons/round-84-verifier-spotcheck.md:108` (R1 carry-forward); the r84 scorer `quality/counters/c1-r84-namespaces.py:272-287`, whose refusal test is `rc == exp["rc"] and ("ERROR (stage=%s " % stage) in stdout` (`:277`) with no cause term at all | QUALITY **141** (added this round) — no prior criterion bound a refusal's *reason* | The r85 scorer `quality/counters/c1-r85-identity-causes.py:306-320` adds the cause clause (`:315-317` `cause = exp.get("cause")` … `(" cause=%s " % cause) not in stdout`), and the declared mutant `cause-dropped` (`:176-178`) deletes it. Re-executed at the freeze: `cases=72 correct=72 mutants=51 killed=51 … verdict=TARGET_MET` (`receipts/independent-score-r85.txt`, Run A). The fix is shown able to fail *as a case score*: a wrong-reason tool (`alloc-not-object` raised where `alloc-negative` belongs) still scores **72/72** (`w1/R85ReviewerC1.md`), because the carried `alloc-negative-refused` case declares no `expect.cause` — QUALITY 141's "include a negative observation" half is still open, and the ten-token vocabulary is bound by only nine witnesses. |
| **M85-2 / number-drift** — the frozen C2 declaration's own ancestry sentence is arithmetically impossible: it claims **nine** round-84 mutants were dropped, while its own list of 37 is 28 carried + 9 new | `claims-declaration-r85.md:103-109` ("The nine round-84 mutants whose rule lines the refactor moved are not carried"); AST enumeration of the two frozen counters (this seat, re-executed): `quality/counters/c2-r84-runbook.py:59-163` enumerates **29** names, `quality/counters/c2-r85-status-classes.py` enumerates **37**; the set difference is exactly one name — `rc-blind` — and the other 28 carry byte-identical `(anchor, replacement)` pairs | none — QUALITY **137** binds the *target* to the enumerated list (37 = 37 held), not the *ancestry claim*; nothing in the lane checks a declaration's statement of what it dropped | The dropped rule line is verified absent from the successor counter: the r84 anchor `"    if rc != 0:\n        return False\n    text = stdout.rstrip"` occurs **0** times in `quality/counters/c2-r85-status-classes.py` and once in the r84 counter — the blanket rc gate the mutant targeted was replaced by the status-class rule, and its behaviour is re-expressed as the *new* `any-nonzero` / `status-class-ignored` mutants. The round's own numbers are corrected here (1 dropped, 28 carried, 9 new); `w1/R85CriticClaims.md` defect 6 records the same discrepancy against the declaration. |
| **M85-3 / attribution** — the round-84 verifier's R3: the pre-scoring receipt lacked revision/hash attribution, so final input hashes bind *identity*, not *chronology*, and `tree=bound` is not full counter/control authentication | `corpus/lessons/round-84-verifier-spotcheck.md:110` (R3); still open at this round: `receipts/frozen-input-crosswalk-r85.json` states its own scope as "Post-execution identity comparison only; does not backdate no-work controls, source openings, or freeze chronology"; the successor counter still prints `tree=bound` in its contract line (`quality/counters/c2-r85-status-classes.py:840`) | none (R3 remains an open routed item; the L1 has not closed it) | The fix direction is exercised by the receipts that do bind identity: `receipts/independent-score-r85.txt` prints the input `sha256` of counter, tool, SKILL.md and all four control files at both `3905311c` and `d7c40e6d` (evidence-verified). Shown able to fail: that receipt states plainly that the C2 counter's own sha256 **changed between observations** (`e6894381…` at the freeze, `b4bde359…` at the successor), so a receipt that binds only the final bytes cannot establish which bytes were scored when — the C2 frozen run's instrument sha is, by the seat's own words, "not pinned by my run". |
| **M85-4 / survivor** — four declared C2 mutants survive the 36-row population because deleting a conjunct cannot lower an already-perfect score | `receipts/independent-score-r85.txt` (Run B2/B3, re-executed by that seat): `mutants=37 killed=33 verdict=TARGET_MISSED`; survivors `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped`, each `matched=36/36 killed=no`; independently reproduced in `w1/R85ReviewerC2.md` (cheats C and D, 36/36). For the two anchor mutants the cause is visible in the frozen control itself: the `version` row's value is already the strict anchored pattern `^Hyprland …[0-9a-f]{7,40} clean \([^)]*\)\.$` with `anchor: line`, and `omarchy-version` is `^[0-9]+\.[0-9]+\.[0-9]+$` (read from the freeze blob, this seat), so dropping the line-anchored matcher changes no verdict on these rows | QUALITY **140** (added this round) | The survivors are **retained** in the declared 37 and the target is **not** shrunk: the successor's own verdict line reads `TARGET_MISSED` rc 1. Shown able to fail: adding a contradictory negative to kill `negatives-skipped` would make the correct implementation fail, which QUALITY 140 forbids; the fix direction is an independently observable detector, not a new negative. |
| **M85-5 / survivor** — the C1 cause check is substring membership over the whole stdout, so a tool that floods every refusal with all nine cause tokens scores the full case set | `quality/counters/c1-r85-identity-causes.py:315-317` (substring search, not a parsed error record); `w1/R85ReviewerC1.md`: a flooding tool scores **72/72** with tool selftest 152/152 and kills only 48/51 (survivors `alloc-dup-cause-collapsed`, `ns-dup-cause-collapsed`, `ns-dup-level-blind`); `w1/R85CriticClaims.md` defect 5 (a pure `expected_ok` call accepts `cause=alloc-negative cause=alloc-not-object` together) | QUALITY **141** (added this round) | The declared mutants `alloc-dup-cause-collapsed` and `ns-dup-cause-collapsed` are the discriminating half and they die in the frozen run (`killed=51`). Shown able to fail: the case score alone cannot kill the flood — the *full* gate does, which is exactly the distinction QUALITY 141 draws ("Distinguish case-score holes from full-gate survivors"). |
| **M85-6 / scope** — `128+N` is Bash's encoding; POSIX only says "greater than 128", and a numeric 141 cannot distinguish death-by-SIGPIPE from an explicit `exit 141` | `quality/counters/c2-r85-status-classes.py:343-358` (`status_ok`, `signal` → `rc == 128 + status["signal"]`); `w1/R85ReviewerC2.md`: `status_ok({class: signal, signal: 13}, 141)` and `status_ok({class: exact, code: 141}, 141)` both return True | QUALITY **142** (added this round) | The successor counter's own docstring states the limit ("This status cannot distinguish a signalled child from explicit exit128+N. POSIX does not require this exact encoding") and the registry carries a rejected row for the converse (S490, see § Gate). Shown able to fail: the S490 flip condition is unmet by construction — the exit builtin's `exit 141` returns the same number (re-executed byte span, § Gate) — so no numeric-status-only proof of termination cause exists in this round. |
| **M85-7 / landing** — the frozen C2 counter refuses at setup before executing a single row, and the frozen `SKILL.md` cannot satisfy it anyway | `receipts/independent-score-r85.txt` Run B1 (re-executed by that seat): exit **2**, `MADO_R85_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)` — the `3905311c` blob of `SKILL.md` carries the round-84 section; in a clean clone of the freeze `w1/R85ReviewerC2.md` reproduces `ERROR (stage=setup carried case 'version' changes field 'negatives')`, and the frozen `SKILL.md:231` heading `### Executable runbook rows (round 84)` yields **0** command rows where the counter expects the round-85 heading with 36 | none — QUALITY **118** requires the declaration's counting command to be replayed verbatim, but its shown example is round 73's argv, not a carried-field preflight refusal | The forward repairs are exactly the four the successor commit makes (`git diff 3905311c d7c40e6d -- quality/counters/c2-r85-status-classes.py`: `STATUS_FIELDS` added to the carried comparison, the section heading renamed to round 85, the mutation anchor counted in the code region only, the `classes`/`len(classes)` print fixed) — and each is shown able to fail: the frozen bytes still refuse, so the frozen verdict remains unverified and no successor result retroactively admits it. |
| **M85-8 / reference-drift** — the declaration's source locators do not match the fetched documents, and one of the two cited endpoints was never reachable | `claims-declaration-r85.md` cites "POSIX.1-2024 XCU §2.9.3 *Pipelines*" and "GNU Bash Reference Manual §3.7.6 *Exit Status*"; the pinned POSIX page anchors Pipelines as **2.9.2** (`fetch/S488.bin`, `2.9.2 Pipelines` at byte 33656; `2.9.3 Lists` at 110936) and the reachable maintainer copy numbers Exit Status **3.7.5** (`fetch/S489-alt-tiswww.bin`); the GNU URL named by the declaration was unreachable in 5 attempts (curl rc 28) and is **not pinned** (`fetch/source-pins-r85.json`, key `S489`) | none | The registry rows cite what was actually opened: S488 anchors `Issue8 section2.9.2 Pipelines`, S489 anchors `Edition5.3 … section3.7.5 Exit Status` and names the maintainer URL. Shown able to fail: the pins file's own note ("Section number in this document is 3.7.5 not 3.7.6 (declaration locator differs)") is a self-contained, re-derivable locator check; a reader who greps the pinned bytes for `2.9.3 Pipelines` finds `2.9.3 Lists`. The declaration is frozen and was **not** rewritten. |
| **M85-9 / landing** — the freeze commit added two instruments with no instrument-ledger rows, so the lane's own ledger gate was red at the frozen revision | `receipts/harm-watch-r85.txt` block [2] (evidence-verified): `population=156 ledger_rows=154 uncovered=2 verdict=TARGET_MISSED` at `3905311c`, both uncovered paths being this round's two counters; the same checker at the base revision reads 154/154 uncovered 0 | QUALITY **139** (a new gate is registered at `SKILL.md`, not only in an instrument ledger) | The successor commit adds both ledger rows (`git diff 3905311c d7c40e6d --stat` → `quality/tool-ledger.md | 2 +`), and at `d7c40e6d` the checker reads `population=156 ledger_rows=156 uncovered=0` — with two **bad pointers** remaining, because both new rows point at `corpus/lessons/round-85.md`, which is not in that revision's tree (the checker scores committed blobs only; re-executed by this seat). Shown able to fail: the pointer resolves only once this lesson is committed, so the ledger gate stays red until then and the repair is verifiable rather than asserted. |
| **M85-10 / scope** — the declared C2 shape count reads as a diversity claim it is not | `claims-declaration-r85.md:100-102` (`shapes=26/26`); `quality/counters/c2-r85-status-classes.py:183-187` — 26 of the 36 frozen cases are of `SHAPE_KINDS`; the counter's `shapes=26/26` therefore counts shape-kind *rows*, not 26 distinct grammars (`w1/R85CriticClaims.md`, "requested checks that do not establish a defect") | none | The successor receipt prints `shapes=26/26` next to `cases=36`, and the two numbers are read together rather than alone; the lesson states the population the number counts. Shown able to fail: a reader who reads 26 as a grammar count is refuted by the counter's own constant list, which this lesson quotes. |

Captured-by column: a criterion number means the mined defect is now bound by that criterion in
`corpus/QUALITY.md`; `none` means no criterion in the lane binds it yet. QUALITY 140–142 were added
by the L1 in this round and cite this lesson; M85-2, M85-3, M85-6 (partly), M85-8 and M85-10 are not
yet captured by any criterion.

## Gate

### New registry rows opened this round (2026-11-04)

Three rows were added to `corpus/SOURCES.md`; before **422** rows, after **425** rows (counted by
this seat with `grep -c '^| S[0-9]'` over the working file and over `git show
5f174ca4:corpus/SOURCES.md`). Census at round start: exit 0 with the standing W04 duplicate-URL and
W01 S277 warnings, unfiltered (`receipts/census-start-r85.txt`).

| row | source, URL | access date | located quote (≤25 words) | scope | tier / status |
|---|---|---|---|---|---|
| **S488** | POSIX.1-2024 Shell & Utilities — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 2026-11-04 | "The exit status of the last (rightmost) command specified in the pipeline." (12 words) — pinned `fetch/S488.bin` bytes **133030–133104**, §2.9.2 Pipelines → Exit Status table, row *pipefail Enabled = no, Begins with ! = no* | the pipeline exit status when `pipefail` is disabled and the pipeline is not negated; Issue 8 also defines `pipefail`, so "last command" is the default-off rule, not a universal one | spec / **A** / mined / recheck 180d |
| **S488 (second clause)** | same pin | 2026-11-04 | "Otherwise, if the command terminated due to the receipt of a signal, the shell shall assign it an exit status greater than 128." (23 words) — pinned `fetch/S488.bin` bytes **109001–109128** (one newline between "status" and "greater", normalised to a space) | what POSIX actually says about a signal-terminated command: **greater than 128**, not the literal `128+N` | spec / **A** / mined (same row) |
| **S489** | Bash Reference Manual, maintainer copy — https://tiswww.case.edu/php/chet/bash/bashref.html (Edition 5.3, 2025-05-18) | 2026-11-04 | "When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status." (21 words) — pinned `fetch/S489-alt-tiswww.bin` bytes **239046–239200**; the raw span carries `<var class="var">N</var>` markup, and dropping the tags without leaving whitespace gives the quoted form (a whitespace-collapsing strip of the same span gives "N ," and "128+ N" — the same bytes, 24 tokens) | the numeric encoding of a fatal signal in **Bash**; it is not a POSIX-wide encoding guarantee and it is not a converse proof that 141 means SIGPIPE | docs / **A** / mined / recheck on-release |
| **S490 (rejected)** | same maintainer copy, §4.1 `exit` builtin — https://tiswww.case.edu/php/chet/bash/bashref.html#Bourne-Shell-Builtins | 2026-11-04 | "Exit the shell, returning a status of n to the shell's parent." (12 words) — pinned `fetch/S489-alt-tiswww.bin` bytes **266270–266361** | the proposed numeric-status-only proof of a producer's termination cause | docs / **A** / **rejected** / recheck 180d |

Pin bytes: `fetch/S488.bin` 357,953 B, sha256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`;
`fetch/S489-alt-tiswww.bin` 1,040,870 B, sha256 `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`
(evidence-verified from `fetch/source-pins-r85.json`; both byte-identical across their two fetches).
The S489 **GNU URL named by the frozen declaration**
(https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html) was **not pinned**: DNS
resolved it, but TCP connect to :443 timed out on both addresses in 5 attempts (curl rc 28) while
the POSIX host answered in the same window. No quote is taken from the GNU page; the `S489` registry
row is the maintainer copy, and the pins file records the unreachable endpoint under its own key
with no bytes.

### Rejects

- **S490 (registry row, rejected).** Reason: `exit 141` alone cannot uniquely prove signal 13,
  because an explicit `exit 141` returns the same number — the quote above is the builtin's own
  wording. **Flip:** separately observed termination metadata that distinguishes a normal exit from
  a signal death.
- **Reject: POSIX grounds the `128+N` form.** S488 says only "greater than 128"; the literal
  `128+N` is Bash's, and the frozen declaration's status table ("reported by a POSIX shell as
  128+N") over-claims it. **Flip:** a normative POSIX sentence that fixes the encoding, separately
  opened and scoped. The successor counter's docstring and SKILL.md row text already say
  "Bash documents 128+N for fatal signals (S489); POSIX does not require that exact encoding."
- **Reject: the declaration's §2.9.3 / §3.7.6 locators are usable as citations.** The pinned bytes
  say 2.9.2 (Pipelines) and 3.7.5 (Exit Status). **Flip:** a POSIX edition whose Pipelines section
  is numbered 2.9.3, opened and pinned.

### Registry changes, old → new

| row | cell | old | new |
|---|---|---|---|
| S486 | used-by | `corpus/knowledge/bar-footprint-namespace-discipline-r84.md, corpus/lessons/round-84.md` | `corpus/knowledge/bar-footprint-namespace-discipline-r84.md, corpus/lessons/round-84.md, corpus/knowledge/bar-footprint-identity-causes-r85.md` |
| S487 | used-by | `corpus/knowledge/runbook-producer-status-r84.md, corpus/lessons/round-84.md` | `corpus/knowledge/runbook-producer-status-r84.md, corpus/lessons/round-84.md, corpus/knowledge/runbook-status-classes-r85.md` |
| S488 | — | (absent) | new row, spec / A / mined / 2026-11-04 / 180d / used-by `corpus/knowledge/runbook-status-classes-r85.md, corpus/lessons/round-85.md` |
| S489 | — | (absent) | new row, docs / A / mined / 2026-11-04 / on-release / used-by `corpus/knowledge/runbook-status-classes-r85.md, corpus/lessons/round-85.md` |
| S490 | — | (absent) | new row, docs / A / **rejected** / 2026-11-04 / 180d / used-by `corpus/lessons/round-85.md` |

No `status`, `recheck` or `opened` cell of any pre-existing row changed. The two used-by appends
are the only edits to old rows. **Correction the L1 must land append-only:** the round's own
`LOG.md:4175` sentence "Registry422→425; old cells unchanged" is no longer accurate, because S486
and S487 used-by cells *did* change (by append). The L1 has said it will append that correction
after this lesson lands; the two rows and the exact old→new strings are the ones above.

## Considerthese

**Proposal 2 — "Check whether a claim stands when its wave-done receipt is red."** Still
unimplemented, and now measured rather than relayed.

The proposal points at `quality/check-wave-done.py` and at the rounds whose claims were published
while their wave receipt was red. This seat opened that checker and ran it across the reflection's
window (re-executed): `python3 quality/check-wave-done.py --repo . --rev
d7c40e6d1b9a7476f2ff48254d577799ce9901e4 --round N` for N = 57…84 prints
`verdict=MISSING` for exactly four rounds — **71, 79, 81, 83** — and `verdict=OK` for the rest.
The causes are visible in the same output: 11, 1, 5 and 3 seats respectively have blank outputs
(round 71: 11 blank; round 79: `R79Sentinel`; round 81: the two reviewers, the critic, the
mutation-tester and the sentinel; round 83: `R83ScoutSource`, `R83ConnSiblings`,
`R83ScribeEntry`).

What the lane published for those rounds (evidence-verified from `SCORECARD.md`): round 71's two
claim rows both read "improved on the frozen … set"; round 79's reads "improved on the frozen
twenty-three-case set"; round 81's two read "improved"; round 83's C2 reads "measured target met;
outside closure pending". So four rounds carry a published claim verdict while the lane's own
wave-done gate for that round is red — exactly the coupling the proposal asks about.

Why it is still unimplemented: QUALITY **102** binds a *report* to a wave results file whose seats
are settled, and QUALITY **103** binds a *report's* WAVE-DONE assertion to a committed receipt at
its integration revision. Neither binds a **published claim row's verdict** to that round's
wave-done verdict, and no instrument in `quality/` reads both: `quality/check-wave-done.py` is the
only file in the lane that mentions wave-done at all. A first implementation is therefore a check
that, for each round with a published claim row, the wave-done verdict at the scored revision is
`OK`. Shown able to fail: run it over rounds 57–84 at `d7c40e6d` and it must report the four reds
above — 71, 79, 81, 83 — while the current SCORECARD reads "improved" for 71/79/81 and "measured
target met" for 83's C2. The same red also warns that round 85's own wave cannot be called
settled until every dispatched seat is terminal.

Proposal 1 (the domain-share line) was already mined in round 84 and is not re-adopted here; this
round's line is written below on its own evidence. Assimilation: none — no shokuknow package and
no operator-authored `considerthese` file is edited.

## Domain share

Two new knowledge entries this round, and both answer a **desktop-surface** question the lane did
not hold: `knowledge/bar-footprint-identity-causes-r85.md` answers *which layer-surface declarations
the bar-footprint join refuses, and under which named cause* — the question a duplicate namespace or
an unknown allocation key raises about which surface owns which band; and
`knowledge/runbook-status-classes-r85.md` answers *what status a read-only runbook row's producer
must report, and how a guarded pipeline propagates it* — the question an omarchy/Hyprland probe
raises when its producer fails but its tail succeeds. Neither entry is about the lane's own gate.
The round's harness-side learning (QUALITY 140–142, the successor counter repairs, the four
survivors) is lane-internal and is deliberately **not** counted as a knowledge entry.

This count is a curation judgement, not a number the lane's own tool produced: the lane's
domain/meta counter `quality/ratio-domain-meta.py` cannot see rounds 84 and 85 at all, because its
heading pattern is `^##\s+Round\s+(\d+)` (`:61`) while those two `SCORECARD.md` sections are
titled `## Round84 …` (`:4912`) and `## Round85 …` (`:4967`) with no space after "Round" — so
`--from 84 --to 85` prints `domain=0 meta=0 window=84-85 default=0` (re-executed by this seat)
while `--from 83 --to 85` prints four rows, all from round 83. The heading drift is reported here
for the L1; the two entries above are counted by reading `corpus/knowledge/`.

## End measurements and known limits

- **C1, frozen, re-executed by `R85ExecScore` and independently by `R85ReviewerC1`:** `cases=72
  correct=72 mutants=51 killed=51 base_correct=62/72 carried=61/61 tool_selftest=152/152
  verdict=TARGET_MET` at `3905311c`, exit 0. The no-work control (held round-84 tool at the base
  revision) prints `correct=62/72` with the ten identity witnesses failing — the held tool refuses
  the right stages and prints no cause (`receipts/control-c1-r85-base.txt`).
- **C2, frozen:** the canonical counting command exits **2** at setup, before any row executes
  (`receipts/independent-score-r85.txt` Run B1; `w1/R85ReviewerC2.md` reproduces the carried-field
  refusal in a clean clone). The frozen C2 claim is **unverified**; a successor's green result
  cannot admit it.
- **C2, successor `d7c40e6d`:** `cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36
  rows=36/36 mutants=37 killed=33 verdict=TARGET_MISSED`, exit **1** — reproduced from a clean
  clone of `d7c40e6d` with identical output (same receipt). The target (37/37) is **not** met and
  is not shrunk: the four survivors stay in the declared population (M85-4).
- **Harm watch at the freeze** (`receipts/harm-watch-r85.txt`): note index 104/104 missing 0
  dangling 0 duplicates 0 (green); standing selftest 460/460 (green); axis scores checked 3
  mismatched 0 (green); sources census exit 0 with the standing W04/W01 warnings (green); **instrument
  ledger RED** — 156 population, 154 rows, uncovered 2 (M85-9). The red is reported, not suppressed.
- **Carried-field discipline (declared, verified):** C1's 61 carried cases are compared
  parsed-equal (control line `carried=61/61`); C2's 36-row control file is byte-identical to the
  freeze (`sha256 de8a68fe…`, both sides, this seat) — the frozen `version` row's value is the
  strict anchored pattern `^Hyprland [0-9]+\.[0-9]+\.[0-9]+ built from branch \S+ at commit
  [0-9a-f]{7,40} clean \([^)]*\)\.$` with `anchor: line` (read from the freeze blob and from the
  working file, this seat; the two agree), and the frozen `omarchy-version` row is
  `^[0-9]+\.[0-9]+\.[0-9]+$`. A transient forward experiment that unanchored those version patterns
  was discarded and the original values restored, so nothing here amends frozen data. The four
  survivors of M85-4 stand against these anchored values: `regex-anchor-dropped` and
  `line-anchor-prefix` cannot be killed by them because the patterns already carry `^`/`$` and the
  suffix-extension negatives are refused either way.
- **Known limits, not repaired this round:** the `alloc-negative` cause has no cause-bound witness;
  the C1 scorer accepts conflicting or flooded cause tokens on the case score alone; a numeric 141
  cannot distinguish SIGPIPE death from `exit 141`; the four C2 survivors stand; the C2 `signal`
  class is Bash's encoding, not a POSIX guarantee; the r84 R2 carried-field exemption is still
  broader than the declared supersessions; the r84 R3 receipt-attribution defect is still open;
  the frozen declaration's own ancestry sentence (M85-2) and locators (M85-8) were not rewritten,
  because the declaration is frozen history.
- **Not run by this seat:** the two round-85 counters' batteries (executed by `R85ExecScore` and
  the reviewers; quoted here as evidence-verified), the census end-run, the outside-lane
  admit/reject spot-check, and any promotion review. No tool was installed; pacman remains paused
  host-wide; no fleet-root, sibling-lane, operator, `.ufo/state/` or MANIFEST file was written.
