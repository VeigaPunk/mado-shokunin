# mado round 86 — lessons

Round 86, hyaku run 15, fresh start after three rejected closures (r83, r84, r85). Two frozen claims
from the declaration carried in by the attempt-1 L1
(`.ufo/waves/round-86/claims-declaration-r86.md`), landed unchanged: C1 calibration (refusal
*records*) and C2 operability (clause observation). Freeze `237ecf4e69a4986108f719f3beeafe111adaa033`;
base `a722c60493f24f83429112e9123058835b2cdd82`.

## Mistakes

**M86-1 — a mutation anchor drifts when the function under it is refactored.**
Class: instrument authoring (frozen mutation population). Evidence: `.ufo/waves/round-86/receipts/
instrument-repair-r86.md`, run 1 — `MADO_R86_RUNBOOK: ERROR (stage=setup mutant regex-anchor-dropped
anchor occurs 0 times, not once)`, rc 2. The round-86 observation line was inserted *inside* the
branch the mutation addressed, so the anchor matched nothing and the instrument could not score at
all. Captured by: the counter's own `Setup` guard — it fired, which is why no verdict was invented
from it. Fix: anchor every mutation on the code that is on the scoring path today, and prove the
fix by running the counter before committing it (run 2 is that receipt, `matched=34/37`).

**M86-2 — a counter can contradict the target it prints.**
Class: frozen-predicate implementation. Evidence: `receipts/c2-anchor-only-r86.txt` — the printed
`declared` tuple says `anchors:1` while `case_correct` required `1 + samples + negatives`; the three
anchored cases (`version`, `omarchy-version`, `border-size-int`) could never pass, so the score was
34/37 with every mutant dead. The two readings differ on a real question: a negative refused by the
producer-status gate never reaches the anchor branch, so "one judgement of the live output" and "one
per sample" are different claims. Captured by: **the scored run** — `TARGET_MISSED`,
`matched=34/37`, `clauses_observed=34/37` — not by the selftest, which printed `114/114` at the same
revision: its anchor assertion drives the raw `OBS` dict, not a producer-status-refused negative
through `case_correct`. That selftest blind spot is open and routed below. Fix: one reading, written
down (the declared population is 1; the live call is snapshotted as `LIVE["anchors"]`), plus the
failing run kept as the receipt that the rule can fail.

**M86-3 — a mutation that targets the held control mutates nothing that scores.**
Class: mutation population integrity. Evidence: `receipts/c2-live-observation-r86.txt` — after the
`case_correct` refactor, `samples-skipped` and `negatives-skipped` anchored on
`for sample in case.get("samples", []):`, which lives only in `held_case_correct`; both survived at
37/37 while the scoring loops were untouched (`mutants=37 killed=35`). Captured by: the run's own kill
table. Fix: anchor on `for sample in samples:` / `for sample in negatives:` (run 4: `killed=37`), and
keep the survivor receipt.

**M86-4 — the round-85 spot-check's routed defects, disposition.**
Read `corpus/lessons/round-85-verifier-spotcheck.md` R1–R7 before declaring; the fresh-start rule
requires it.

| routed defect | disposition in r86 | evidence |
|---|---|---|
| R1 four clause-skipping survivors live on a perfect score | **closed for the declared population**: all four (`negatives-skipped`, `samples-skipped`, `regex-anchor-dropped`, `line-anchor-prefix`) die 37/37 | `receipts/c2-repaired-r86.txt` |
| R2 the cause test is stdout substring membership; all-cause flooding scores full | **closed**: record + negative observation, flooding 48/75 vs held 75/75 | `receipts/c1-r86.txt` |
| R3 numeric status cannot authenticate termination cause | **open** (retained, not re-argued); the r86 instruments keep the `ok`/`exact`/`signal` split declared and claim no termination cause | QUALITY 142 |
| R4 wave telemetry: null seat outputs beside a green wave check | **open**; r86 adds a QUALITY criterion, no instrument | QUALITY 145, `considerthese/2026-11-04.md` proposal 2 |
| R5 the append-only LOG correction for "old cells unchanged" landed | **retained** as a pointer; nothing restated | `LOG.md` round-85 corrections |
| R6 declaration source locators off by one; an unreachable endpoint recorded as unreachable | **applied**: S491/S492 locators are line numbers of the committed pins and are re-derived by the round's scout seat | this file, `## Gate` |
| R7 two L1 probe dirs created directly under the shared scratch root | **fixed for r86**: the only L1 scratch roots are `/fast/scratch/hyaku/mado-r86/l1/*`, inside the lane's own subtree; removed at round close | `receipts/cleanup-r86.json` |

**M86-5 — inherited bytes are not inherited verdicts.** The attempt-1 L1 died before measuring, and
its counters shipped with three defects (M86-1..3) that only a run exposes. Class: inheritance
handling. Fix: attempt 2 ran both instruments before freezing anything, and the failing runs are
committed as receipts rather than deleted. A round that reuses in-flight work must run it first.

**M86-6 — a docstring's contract line is a declaration, and it can drift from the code.**
Class: bookkeeping drift (round 83 was rejected for exactly this shape: declared 38 against 39
killed). Evidence: `quality/counters/c1-r86-refusal-records.py` says `mutants=53 killed=53` while
`MUTANTS = 51` and the declaration's target is `killed == 51`; the printed line and the executable
predicate agree, only the prose does not. Captured by: **none** — nothing compares the docstring's
contract line to the constants. **Disposition: found and NOT fixed.** The L1 did edit the line to
51 during the wave, and `w1/R86ReviewerC1.md` caught the drift and named it a breach of the
declaration's freeze rule; the edit was reverted, the working tree returned to the frozen bytes, and
the defect is routed to r87 as its own repair with a control. A frozen instrument is not repaired
mid-round, even in prose.

**M86-7 — an attacker found four forgery classes the record rule scores 75/75.**
Class: claim scope. Evidence: `w1/R86ReviewerC1.md` S1-a/S1-b/S2-a/S2-b — an all-ten-token flood on
**stderr** (the counter captures stderr and never inspects it), a duplicate record shifted by one
leading space (`^`-anchored `re.M` hides it, so "exactly once" holds only at column 0), a flood on
the **result** path (no vocabulary check exists there at all), and a homoglyph flood (`а` U+0430 for
`a`, defeating a byte-substring vocabulary). Captured by: the wave's own attack seat — the frozen
case set carries none of these. Disposition: recorded as named limits of the entry and the claim;
the instruments stay frozen; the four classes are the next round's control additions.

## Wave findings routed to r87 (instruments stay frozen)

| finding | seat | severity | routed repair |
|---|---|---|---|
| `git` child inherits the whole environment and is resolved via `PATH`; an ambient `GIT_DIR` overrides `-C repo`, so `tree=bound` could bind a different repository | Sentinel F1 | high | pass an explicit environment and `git --git-dir`-free resolution; add a control that sets `GIT_DIR` to a decoy |
| the counter's own bytes are not bound to `--rev` (the receipt's `rev=` names a revision whose counter bytes may differ from the executing file) | Sentinel F2, C2 | medium | hash `__file__` into the printed contract and assert it against the blob at `--rev` |
| a count-preserving stub (increments kept, evaluations removed) passes every case-level clause; only the mutant population catches it | ReviewerC2 F1/F2 | medium | observe the evaluation result, not only the call (e.g. count sample matches, not loop iterations) |
| C2 judges a refusal by a stage substring while C1 judges the same tool's refusal as one record — two conventions for one stream | Connector §4 | medium | one versioned refusal-record parser owned by one module, kept out of the frozen populations |
| dead constants `BASE_EXPECT` (c1:37) and `EXACT_KINDS` (c2:198) | Connector §2 | low | delete with the successor |
| `--no-mutants` exits 0 with `killed=0`, and C1's branch returns 0 without evaluating the target | Sentinel F3 | medium | print a distinct `MUTANTS_SKIPPED` verdict and a non-zero exit, or drop the flag from the public contract |
| the foreign-token test exempts the record's own cause **by identity, not position**, so an own-cause echo tool scores 75/75 against a binding that forbids the token outside the record | Critic (a) | medium | track the record's cause field as a span, not a token, and add the echo tool to the control set |
| the C1 kill rule under-enumerates the target conjunction (tool selftest, `held_flooding`) and the carried/tree conditions are `Setup` errors rather than misses; `--no-mutants` prints `MUTANTS_SKIPPED` with rc 0 | Critic (b) | medium | one enumerated clause list in code, one miss for every `T`-false, and a non-zero rc for a skipped population |
| 17 counter mutants beyond the declared populations: **5 killed, 12 survived** — C1 `record-any-count`, `record-search-anywhere`, `negative-one-class`, `carried-check-skipped`, `rc-ignored-result-cases`, `tool-selftest-rc-free`, `stage-unchecked`; C2 `observed-all-constant`, `tree-bound-dropped`, `carried-field-drift`, `live-anchor-clause-dropped`, `live-anchor-declared` | MutationTester | high | each survivor is an executable doctored input in `w1/R86MutationTester.md`; the successor control sets carry them as cases (an `observed_all` that always increments, a dropped tree binding, a widened carried exemption) |
| the C2 selftest printed 114/114 at both revisions while the counter contradicted its own declared population; it asserts the raw `OBS` dict, never `case_correct` on a producer-status-refused negative | ScribeLesson M86-2 | medium | add a selftest case that drives each anchored control case through `case_correct` and asserts the declared verdict |
| the axis label moved coverage → calibration with no derived cell moving; the lane's instrumented calibration axis is resolved-active entries (86/86) | Critic (d) | medium | no repair this round: the label is the frozen declaration's; the dissent is recorded for the closure judge and the next declaration must name the cell its claim moves |

## Gate

### New registry rows opened this round (2026-11-04)

Two rows are added to `corpus/SOURCES.md`; before **425** rows, after **427** rows
(`grep -c '^| S[0-9]' corpus/SOURCES.md` over the branch tip before and after this round's append).

| row | source, URL | access date | located quote (≤25 words) | scope | tier / status |
|---|---|---|---|---|---|
| **S491** | RFC 7493 (I-JSON) §2.3 Object Constraints — https://www.rfc-editor.org/rfc/rfc7493.txt | 2026-11-04 | "Objects in I-JSON messages MUST NOT have members with duplicate names." (12 words) — pin `.ufo/waves/round-86/fetch/S491.bin` 12,849 B, sha256 `a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062`, **bytes 6364–6424, line 159** (§2.3 heading at line 157; the sentence carries one newline, after "duplicate") | duplicate member names in an I-JSON object are a **MUST NOT**, not the RFC 8259 §4 "SHOULD" the lane already holds as S486; it grounds *refusing* a duplicate-name object, not choosing among duplicates | spec / **A** / mined / recheck 180d |
| **S492** | CPython v3.14.8 `Doc/library/re.rst`, `fullmatch` — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst | 2026-11-04 | "If the whole *string* matches the regular expression *pattern*, return a corresponding Match." (14 words) — pin `.ufo/waves/round-86/fetch/S492.bin` 78,262 B, sha256 `d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48`, **bytes 39792–39901, line 957** (the `fullmatch` directive at line 955; the sentence carries one newline, normalised to a space in the quote) | `fullmatch` is whole-string, `re.search` is not: the ground for the `anchor: line` rows, where a prefix-accepting matcher must refuse a line that merely starts with the value | docs / **A** / mined / recheck on-release |

### Rejects

- **Reject: RFC 8259 alone grounds a duplicate-name refusal as a specification constraint.** S486
  (held) carries §4's "The names within an object SHOULD be unique" — a SHOULD. A refusal that cites
  only RFC 8259 over-claims. **Flip:** an I-JSON-mandated surface (`application/…+json` with the
  I-JSON profile) where the SHOULD becomes a MUST — S491 is exactly that, and it is why the pair is
  recorded together rather than S486 alone.
- **Reject: "the two anchors survivors were killed by the anchor branch".** Measured: the frozen r85
  patterns already carried `^`/`$`, so the two anchor mutants survived because the *branch* was never
  taken, not because the pattern was weak (r85 spot-check R1). The r86 kill is by the observation,
  and the mutant list keeps `regex-anchor-dropped` applying to the branch that exists. **Flip:** a
  case set in which an unanchored pattern is bound to an anchored row and the negative proves the
  difference — that is the `border-size-int` witness, and it is admitted.
- **Reject: citing the declaration's own prose as the source of a rule.** The declaration is the
  lane's frozen intent; it is not evidence. Every number in the knowledge entry is read from a
  committed receipt or produced by a command in this round.

## Census

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

- round start (before any work): **exit 0**, 425 rows, standing `W04` duplicate-URL warnings
  (S451–S456, S458, S465, S466, S470, S475, S477, S481, S490) — unfiltered, unchanged from r85.
- round end (after the two rows): see `LOG.md` round-86 entry and `receipts/census-end-r86.txt`.

## Considerthese

Mined `considerthese/2026-11-04.md` proposal 2 ("Check whether a claim stands when its wave-done
receipt is red"; the reflection states the r81 wave had five empty seats and a `MISSING` wave check).
It lands as **QUALITY 145**: a published claim row names its wave's settlement state, and a null
seat output is missing telemetry, never a settled seat. The r85 routed defect R4 was the same
observation from the other side; the criterion is the durable form, and proposal 2's own "I only
checked r81 by hand" is what it forbids the next round.

## Domain share

New knowledge entries this round: **1** — `refusal-records-clause-observations-r86.md`, a lane-internal
instrument entry (it answers "is this refusal/row authenticated", not a compositor question). New
tools: **0**. The desktop-facing surface this round touched is one runbook row
(`hyprctl getoption general:border_size -j`) and its live read; that is the eighth-round running
imbalance the 2026-11-04 reflection measures (5 of 22 entries desktop-facing across r63–r81), and
r86 does not correct it. Named, not hidden.
