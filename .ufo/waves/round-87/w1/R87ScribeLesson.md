# R87ScribeLesson — round 87 lesson draft and scoped findings

Seat: R87ScribeLesson (leaf scribe, no dispatch). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin. Base `e4875ba5619053cc3f91bb2f4d819e189df4088c`.
Only this file is written. Scratch `/fast/scratch/hyaku/mado-r87/R87ScribeLesson/` removed on exit.

## 1. Findings in brief

- M87-1 confirmed by reading bytes: the `0/1` held-rule figure is printed by the r86 counter's model `held_case_correct()` (`quality/counters/c2-r86-clause-observations.py:574-593`, used at `:890`); the held round-85 counter is never called by either r86 counter (grep count 0, see §3).
- M87-2 found a second and third figure of the same root that the closure did not flag: `held_flooding=75/75` (`held_ok()` in `quality/counters/c1-r86-refusal-records.py:367-381`, called at `:639`) and the entry's line 144 "three of the four also score 75/75 under the held rule" (`w1/R86ReviewerC1.md:52` prints `rule=held_ok`). Both are re-implementations, not runs of `quality/counters/c1-r85-identity-causes.py::expected_ok` (`:306-332`).
- Mako manual pin defect: the declaration pins `/usr/share/man/man5/mako.5.gz` as sha256 `f717848f…`. That digest is of the **decompressed** roff text (`zcat | sha256sum`). The `.gz` file's own digest is `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670`. S493 names both.
- `corpus/CORPUS.md` does not exist (`find . -name 'CORPUS.md' -not -path './.git/*'` printed nothing). The mistake and gate layout was taken from `corpus/lessons/round-86.md`, which has the same sections.
- Census not run; `[[CENSUS]]` left for the L1 per the item.
- Installs: none. Read-only `pacman -Q` / `pacman -Qo` only (permitted by the pacman pause; no `-S`, `-Sy`, `-U`, `-R`).

## 2. Commands run and exit codes

| command | output (abridged) | rc |
|---|---|---|
| `sha256sum /usr/share/man/man5/mako.5.gz` | `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670` | 0 |
| `zcat /usr/share/man/man5/mako.5.gz \| sha256sum` | `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` (= declaration pin) | 0 |
| `wc -l -c` on the decompressed copy | `644 17209` | 0 |
| `pacman -Q mako`; `pacman -Qo /usr/share/man/man5/mako.5.gz` | `mako 1.11.0-1`; file owned by `mako 1.11.0-1` | 0, 0 |
| `grep -n` on decompressed copy (include, criteria, modes, `win`, `invisible`) | lines 45-48, 434-437, 616-634 (see S493 row) | 0 |
| `grep -in case` on decompressed copy | no output | 1 |
| `grep -c '^| S[0-9]' corpus/SOURCES.md` at base | `427` | 0 |
| `git ls-files corpus/knowledge \| wc -l`; `quality/counters`; `tools` | `107`; `108`; `26` | 0 |
| `find . -name 'CORPUS.md'` | (empty) | 0 |
| python count of `round-86/controls/c1-cases-r86.json` | cases 75, refusal 27, non-refusal 48, causes bound 10 | 0 |
| python count of `round-85/controls/c1-cases-r85.json` | cases 72, refusal 24, causes bound 9 (no `alloc-negative`) | 0 |
| `grep -c 'killed=no' receipts/control-held-rule-r86.txt` | 4 (regex-anchor-dropped, line-anchor-prefix, negatives-skipped, samples-skipped) | 0 |

## 3. M87-2 sweep (command and output)

Command: the greps below, run from the lane root on base bytes.

```
grep -no '[0-9]\+/[0-9]\+' corpus/knowledge/refusal-records-clause-observations-r86.md
grep -n 'def held\|held_ok(\|held_case_correct(\|rule=held' quality/counters/c1-r86-refusal-records.py quality/counters/c2-r86-clause-observations.py .ufo/waves/round-86/w1/R86ReviewerC1.md
grep -c 'c1-r85-identity-causes\|c2-r85-status-classes' quality/counters/c1-r86-refusal-records.py quality/counters/c2-r86-clause-observations.py
```

Output (abridged): entry figures at lines 46-54, 102, 108-113, 137, 139, 144; `held` producers:
```
quality/counters/c1-r86-refusal-records.py:367:def held_ok(case, rc, stdout):
quality/counters/c1-r86-refusal-records.py:639:        held_flood, _ = run_cases(flood_path, cases, workroot, "held-flood", rule=held_ok)
quality/counters/c2-r86-clause-observations.py:574:def held_case_correct(case, rc, stdout):
quality/counters/c2-r86-clause-observations.py:890:                held_new_case = 1 if held_case_correct(case, rc, stdout) else 0
.ufo/waves/round-86/w1/R86ReviewerC1.md:52: ... rule=expected_ok ... and `rule=held_ok score= 75/ 75 SURVIVED`
```
Held-counter imports: `quality/counters/c1-r86-refusal-records.py:0`, `quality/counters/c2-r86-clause-observations.py:0`, grep rc 1 (no match).

Classification of the r86 entry's figures:

| figure (entry line) | producer | verdict |
|---|---|---|
| `held_flooding=75/75` (:52; also SCORECARD :5033, QUALITY 143, receipt `final-c1-r86.txt`) | `held_ok()` re-implementation, c1-r86 `:367-381` | model-sourced; not the held counter |
| `held_rule_new_case=0/1` (:112; SCORECARD :5034) | `held_case_correct()`, c2-r86 `:574-593` | model-sourced (M87-1) |
| "three of the four also score 75/75 under the held rule" (:144) | `held_ok` via `w1/R86ReviewerC1.md:52` | model-sourced (M87-2) |
| `flooding=48/75`, `base_correct=75/75`, `27`/`48` split, `10` causes bound, `9` in r85 | real record-rule run / control-file counts (verified above) | measured |
| `33/37` kills, four survivors | `receipts/control-held-rule-r86.txt` (r85 instrument run, `killed=no` ×4) | measured |
| `34/37`, `37/37`, `cases=37`, `3c5ec8b2…` flood sha | receipts `c2-anchor-only-r86.txt`, `c2-repaired-r86.txt`, `final-c1-r86.txt` | measured (receipt prints) |

Limit: the held round-85 counter's `expected_ok` and the r86 `held_ok` have the same refusal branch by reading; neither was executed against the flood output in this seat, and no receipt does so.

## 4. Declaration and item notes for the L1

- The S493 pin: name both digests (decompressed text `f717848f…` is the one the counter should bind; the `.gz` is `17ffc88c…`).
- F2 reproduction: the C2 predicate ("reproduces at REV") can be met while the held component stays a model. The Correction block says so.
- No SOURCES, SCORECARD, QUALITY, LOG or knowledge file was written by this seat; the blocks below are drafts for the L1 to append.

## 5. Lesson draft (one block)

````markdown
# mado round 87 — lessons

## Mistakes

**M87-1 — a held-rule figure was printed by the lane's own model, not by the held counter.**
Class: number-drift. Evidence: `corpus/lessons/round-86-verifier-spotcheck.md` §2 (its R1: the report's `held_rule_new_case=0/1` comes from `c2-r86-clause-observations.py::held_case_correct()` at `:574-593`; the held round-85 counter's `case_correct` scores the witness 1/1); `corpus/knowledge/refusal-records-clause-observations-r86.md:112`; `SCORECARD.md:5034` (the round-86 C2 row). Captured by: none — the r86 selftest pinned the model to its own figure (`quality/counters/c2-r86-clause-observations.py:736-737`, `ok(not held_case_correct(anchor_case, 0, "0"), ...)`). Fix: C2 of this round (`quality/counters/c2-r87-control-fidelity.py` re-derives F1 by calling the held round-85 counter's `case_correct()` at the measured revision [[REV]]) plus the correction blocks in § Correction text. The frozen r86 selftest pin is not rewritten; it is routed to r88.

**M87-2 — the same root sits under two more r86 figures, and the closure checked them by reading, not by running.**
Class: number-drift. Evidence: the provenance sweep in `.ufo/waves/round-87/w1/R87ScribeLesson.md` §3. Found: (a) `held_flooding=75/75` at `corpus/knowledge/refusal-records-clause-observations-r86.md:52` (also `SCORECARD.md:5033`, `corpus/QUALITY.md:143`, `.ufo/waves/round-86/receipts/final-c1-r86.txt`) is printed by `held_ok()` in `quality/counters/c1-r86-refusal-records.py:367-381` (called at `:639`), a re-implementation of the held rule with a substring refusal branch; it is not a run of `quality/counters/c1-r85-identity-causes.py::expected_ok` (`:306-332`), and neither r86 counter imports a held counter. (b) "three of the four also score 75/75 under the held rule" (the entry's `:144`) comes from `.ufo/waves/round-86/w1/R86ReviewerC1.md:52`, which prints `rule=held_ok`, the same model. The closure's §2 checked `held_ok()` against its source by reading only. Captured by: none. Fix: the correction blocks state the provenance of each held figure; C2 of this round reconciles the printed F2 value (it does not run the held counter); routed to r88: a selftest that calls `c1-r85-identity-causes.py::expected_ok` over the flood output and over the three held-scoring forgeries.

## Gate

### New registry row opened this round (2026-11-05)

One row is added to `corpus/SOURCES.md`; before **427** rows, after **428** rows (`grep -c '^| S[0-9]' corpus/SOURCES.md` on the branch tip before and after this round's append).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S493 | mako(5), manual of mako 1.11.0-1 — file:///usr/share/man/man5/mako.5.gz | docs | A | mako config grammar (`include=`, criteria sections, precedence) on this host version; the installed file is owned by `mako 1.11.0-1` (`pacman -Qo`) | sha256 of the decompressed roff text `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` (644 lines, 17,209 B); the `.gz` file itself is sha256 `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670`; located quote at roff lines 436-437 | criteria precedence: "if multiple criteria match a notification, the last occurrence of any given style option will "win"." (16 words) | mined | 2026-11-05 | 90d | corpus/knowledge/mako-criteria-resolution-r87.md |

Access date 2026-11-05. The located quote is read from the decompressed bytes at lines 436-437 (the roff `\&` escapes are zero-width). The include rule at lines 45-48 is quoted in the entry, not in this row.

### Admit and reject candidates for the mako entry

- **Admit 1 — criteria precedence (S493 lines 434-437).** The manual fixes file order as the match order, and for a style option set by several matching criteria the last occurrence wins. C1's tool implements exactly this. **Flip:** a pinned manual of another mako version that states a different precedence, or a live run at the same revision where an earlier criterion wins.
- **Admit 2 — `include=` path (S493 lines 45-48).** "The path must be absolute or otherwise start with ~/." The tool refuses a relative include path rather than resolving it against a guessed directory. **Flip:** a manual version that accepts relative include paths; the pin covers 1.11.0 only.
- **Reject 1 — "`makoctl mode -a do-not-disturb` hides every notification on this host".** The manual states intent (lines 633-634), not an observed daemon outcome, and S493's scope is config grammar. No process was observed and the tool calls no `makoctl`. **Flip:** a receipt from a live `makoctl mode -a` at the same revision with a notification observed hidden. (Do-not-disturb on the waybar/walker plane stays with `waybar-walker-plane.md`.)
- **Reject 2 — "criteria matching is case-sensitive".** The pinned text says nothing about case: a case-insensitive search of the decompressed bytes prints nothing. **Flip:** a manual line or source row that states it, or a measured match at the pinned version.

## Census

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

- round start (base `e4875ba5619053cc3f91bb2f4d819e189df4088c`, before any work): exit [[CENSUS]] (must be 0); 427 rows; standing `W04` duplicate-URL warnings unfiltered.
- round end (after S493): exit [[CENSUS]]; 428 rows expected; L1 measures and records it here.

## Considerthese

Mined `considerthese/2026-11-04.md` proposal 7 ("mark each figure as relayed or re-measured"). That reflection says every count in it is relayed from `LOG.md`, which is the same unlabelled pattern M87-1 and M87-2 show. It lands as **QUALITY 146** below, a criterion and not an instrument.

**146. Every figure in a lane entry says whether it was re-measured or relayed.**
Every figure in a lane entry is labelled `[re-measured]` with the command that printed it, or `[relayed]` with its source (file and line, or receipt path). Shown able to fail: `corpus/knowledge/refusal-records-clause-observations-r86.md:52` and `:112` carried `held_flooding=75/75` and `held_rule_new_case=0/1` with no label; both were printed by models inside the r86 counters (M87-1, M87-2), not by the held counter. Source: `considerthese/2026-11-04.md` proposal 7, 2026-11-04. Limits: the label names the producer; it does not prove the producer is the held counter, and it does not make a relayed figure correct.

## Correction text

Append-only blocks for the L1. The superseded sentences stay as written.

### Target 1: `corpus/knowledge/refusal-records-clause-observations-r86.md` (append at end of file)

## Correction (round 87 — held-rule witness figure)

Figure id `F1_held_rule_witness_r86`. Superseded sentence, line 112, verbatim: "against the held rule's `held_rule_new_case=0/1` on the same witness and the round-85 instrument's". Re-derived value: **1/1** (the held round-85 counter scores the `border-size-int` witness correct). Method: import `quality/counters/c2-r85-status-classes.py` at the measured revision [[REV]] and call its `case_correct()` on the `border-size-int` case from `.ufo/waves/round-86/controls/c2-cases-r86.json`; its negatives (`0 extra`, `-1`, `0`) are refused and its samples (`1`, `2`) are accepted. Cause: M87-1 — the `0/1` was printed by `held_case_correct()` in `quality/counters/c2-r86-clause-observations.py` (`:574-593`), which ignores `anchor`, and not by the held counter. Pointer: `quality/counters/c2-r87-control-fidelity.py` (round 87, C2) re-derives this figure at its measured revision; the r86 sentence is not rewritten.

F2 reproduction (one line): `F2_flood_r86` reproduces as `flooding=48/75 held_flooding=75/75` (printed by `quality/counters/c1-r86-refusal-records.py`, as in `.ufo/waves/round-86/receipts/final-c1-r86.txt`). Provenance: the held component is `held_ok()` in that counter (`:367-381`), a re-implementation of the held rule and not the held round-85 counter, so the reproduction reconciles the printed number and does not measure the held counter.

### Target 2: `SCORECARD.md` (append at end of file)

## Correction (round 87 — held-rule witness figure)

Figure id `F1_held_rule_witness_r86`. Superseded sentence, the §Round86 C2 row at line 5034: "held rule 0/1 on the new anchor witness (`border-size-int`)". Re-derived value: **1/1**, by calling the held round-85 counter's `case_correct()` on `border-size-int` at the measured revision [[REV]] (negatives refused, samples accepted). Cause: M87-1 — the `0/1` came from the r86 model `held_case_correct()` (`quality/counters/c2-r86-clause-observations.py:574-593`), not from the held counter. Pointer: `quality/counters/c2-r87-control-fidelity.py` (round 87, C2) re-derives it.

F2 reproduction (one line): `F2_flood_r86` reproduces as `flooding=48/75 held_flooding=75/75` (§Round86 C1 row, line 5033, and `.ufo/waves/round-86/receipts/final-c1-r86.txt`). Provenance: the held value is printed by the r86 counter's `held_ok()` (`quality/counters/c1-r86-refusal-records.py:367-381`), a re-implementation, so this reconciles the printed number and does not measure the held counter.

## Domain share

Commands and numbers:

- Baseline (pre-round, `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-files corpus/knowledge | wc -l` at base `e4875ba5619053cc3f91bb2f4d819e189df4088c`): corpus/knowledge 107 files; quality/counters 108 files; tools 26 files.
- Planned adds, from the item paths in `.ufo/waves/round-87/w1-spec.json`:
  - desktop question: **1** entry — `corpus/knowledge/mako-criteria-resolution-r87.md` (the mako entry);
  - lane-internal: **3** — `quality/counters/c1-r87-mako-criteria.py`, `quality/counters/c2-r87-control-fidelity.py`, `.ufo/waves/round-87/controls/r86-figures-r87.json`;
  - tool, outside the two-way count: `tools/mado-mako.py` (reads the desktop's mako config; L1 classifies it).
- Round-end measure: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --name-only --diff-filter=A e4875ba5619053cc3f91bb2f4d819e189df4088c HEAD -- corpus/knowledge quality/counters tools .ufo/waves/round-87/controls` → desktop [[MEASURE]], lane-internal [[MEASURE]].
- Planned share: 1 desktop of 4 entry files (25 %). Round 86 added 1 lane-internal entry and no desktop entry.
````

## 6. Verification status

Checked by reading bytes and running commands named above. Not run by this seat: the lane counters (out of scope for scribes, per the item), the census (L1 fills `[[CENSUS]]`), and the mako tool. Placeholders in the draft: `[[CENSUS]]`, `[[MEASURE]]`, `[[REV]]` only.
