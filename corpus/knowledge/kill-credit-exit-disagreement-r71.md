---
source: S442 (https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst, § subprocess.run capture_output paragraphs, :53-56 @ tag v3.14.8) and S435 (Bash exit-status vocabulary)
verified-at: 3868bc659621fd1ffeb46d8a2040b1f327ae3444
recheck: `python3 -I quality/counters/c1-r71-real-children.py --repo . --rev HEAD --base-rev c354f4d410b829d985b31560af9202d98655dad0 --scratch-root <scratch>` prints `TARGET_MET`
---

# Kill credit under exit-status disagreement (r71)

Claim: the landing control harness's M-Z kill credit follows the child's own parsed
failed-assertion summary **whatever the child's exit status**, and this is proven with four
real `bash` children whose exit status disagrees with their own summary.

## What changed

Round 70 froze `mz_killed = mz_rc != 0 and summary_shows_failure(out)` in
`quality/counters/c1-r70-landing-controls.py`. That still misses one real child class: a lane
whose assertions genuinely fail but whose exit status is 0 (broken status propagation) escapes
classification as a survivor, although the lane's own summary reports the failure. The exit
status cannot carry the assertion result — it is one bit about the process lifetime, with many
causes (held ground: S441's returncode paragraphs, S435's multi-cause vocabulary). Round 71's
successor harness `quality/counters/c1-r71-landing-controls.py` credits
`mz_killed = summary_shows_failure(out)` alone; the exit status stays visible in the
harness's own `MADO_R71_MUTANT M-Z` evidence line. The sole behavioral delta from the frozen
round-70 harness is that one conjunct (review-verified: `last_summary`, `summary_shows_failure`,
`outcome_exit`, `outcome_verdict` and the stream concatenation are byte-identical between the
two revisions; `w1/R71RevC1.md`).

## The four real-child scenarios

Each is a real `bash` child in a scratch git fixture the counter builds; in every scenario the
harness's M-Z leg deletes the frozen clause `[ "$citations" -gt 0 ] && ` (exactly once) and
runs the mutated lane:

| scenario | mutated lane behavior | truth | expected `mz` | held r70 harness | r71 harness |
|---|---|---|---|---|---|
| `liar-success` | deletion fails the zero-citation assertion; genuine `1/2` summary on stdout; **exit 0** | kill (assertion failed) | pass | `fail` (missed) | `pass` |
| `stderr-genuine` | deletion fails the assertion; genuine `1/2` summary on **stderr only**; exit 1 | kill | pass | `pass` | `pass` |
| `liar-kill` | assertions pass (`2/2`); exit 1 for an unrelated trailing failure | not a kill | fail | `fail` | `fail` |
| `crash-stderr` | exit 2, stderr noise, no summary | not a kill | fail | `fail` | `fail` |

Counting command (frozen):
`python3 -I quality/counters/c1-r71-real-children.py --repo . --rev 3868bc659621fd1ffeb46d8a2040b1f327ae3444 --base-rev c354f4d410b829d985b31560af9202d98655dad0 --scratch-root <scratch>`
→ `MADO_R71_REAL_CHILDREN: cases=4 correct=4 base_correct=3 verdict=TARGET_MET`, rc 0
(`.ufo/waves/round-71/measurement-r71.txt` § C1; first run at the instrument commit
`8e78a4ee` prints the identical counts). The do-nothing control — the held round-70 harness —
misses `liar-success` and only it (base_correct 3/4; pre-freeze receipt
`control-baseline-c1-r71.txt`). A stdout-only reader misses `stderr-genuine`; a stderr-only
reader misses `liar-success`: reading **both** streams (stdout then stderr, the round-70
concatenation order) is load-bearing (review matrix, `w1/R71RevC1.md` §2).

## Sourced ground

S442 supersedes S108 for this scope (CORPUS rule 2: a new row whose `teaches` opens
`supersedes S108 —`; S108's own cells are unchanged, its scope stays the `args` binding).
Fetched 2026-11-04 three times, byte-identical, sha256
`05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` (61,603 bytes — the digest
S108 already records). Located quotes: "If capture_output is true, stdout and stderr will be
captured." (:53) and "the internal Popen object is automatically created with stdout and
stderr both set to PIPE" (:54-55): a child's own report arrives on captured streams separate
from its exit status — the summary is the assertion signal and both streams are the reader's
duty. The returncode ground stays held (S441 rendered page, S435 vocabulary).

## Limits (all disclosed by the round's reviewer, `w1/R71RevC1.md`)

1. A **stale, canned, or echoed** failing summary earns kill credit (skipped-run and wrapper
   classes); the rule reads the child's report, it does not authenticate it, and a forged or
   stale summary is byte-indistinguishable from a genuine one.
2. Kill credit no longer evidences that the mutation **caused** the failing summary. Within
   the frozen four-mode fixture the link holds (the scenario branch is reachable only when the
   clause is deleted — verified on unmutated lanes); as a standing harness rule it does not.
3. The verdict-level flip vs round 70 cuts both ways: an instrument with broken status
   propagation and a failing summary now scores `TARGET_MET`/exit 0 on the full harness
   because the unmutated selftest leg and `outcome_exit` still key on exit status alone — the
   class C1 fixes for mutants persists one leg over in the same harness.
4. Multi-summary output resolves **last-wins** in stdout-then-stderr order (a stderr summary
   outranks a stdout summary by position, not chronology); round-70-identical, inherited.
5. The observed child exit codes are {0, 1, 2}; rc-gated credit variants agreeing on that set
   are indistinguishable on this fixture.
6. Four scenarios are a named set, not fault coverage; the fixture lane is the counter's own
   instrument, not the lane's real landing instrument.

The harness docstring's older sentence "a kill is credited on a failed assertion, never on a
broken child" is r70's wording and overclaims under the r71 rule (the F1 child runs no
assertion and is credited); this entry, not that sentence, states the rule.
