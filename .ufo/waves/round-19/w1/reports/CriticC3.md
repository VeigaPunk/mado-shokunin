# CriticC3 — C3's 6/6 is a training-set score: a 3-line regex hack reaches 6/6 and the re-pin accepts it, no non-guessing draft can reach 6/6, and "re-pin at the landed classifier" is circular by construction

Scope: attack C3 (`tw-recall.py`, 3/6 → 6/6) for overfitting, missing independent evidence, and circular
re-pin. Read-only in the lane. All tool variants were built in a `/tmp/critc3` clone at `17661e0` and run
there. Scratch helpers live in `/tmp/critc3/{harness,oracle,guess}.py` (not lane files).

Draft digests: `TwMissBashCVar.patch` 6911e949…, `TwMissHelperFn.patch` 6cf9ca69…,
`TwInstallerChannels.patch` 1acb8549…. Base tool `c1ae45a7…` is identical at 9c54c56 and 17661e0.
Variants: B = base+BashCVar `6c374a42…`, H = base+HelperFn `0bc5b26e…`, I = base+Installers `38e3ab72…`,
BI = merge-file(B,base,I) with 0 conflicts. `git apply --check` succeeds for each draft alone.

## 1. Counterexample: a regex hack scores 6/6 and the re-pin pipeline accepts it

`/tmp/r19-toys/tool-toy.py` is the sibling FrozenRepinScript's own test mutant
(`.ufo/waves/round-19/w1/reports/FrozenRepinScript.md:55-73`). It adds a 3-line rule that emits
`package_query` whenever an eval cell's text matches `pacman['"]?\s*,\s*['"]?-Q|pacman\s+-Q`.

- **Frozen inputs (the C3 counter's exact procedure, via `/tmp/critc3/harness.py`):** `toy.py rc=1 recall=6/6 control_hits=0`.
  The 21 control lines stay clean.
- **Re-pin:** per that report (lines 68-73), `frozen-repin.py` returns `written`, all three known misses
  are dropped into `expected_findings`, and the `--frozen` replay gives `frozen_match`.
- **Held-out corpus.** I scanned all 4523 `*.jsonl` under `~/.omp/agent/sessions/-Projects-shokunin`
  (read-only, `xargs … --scan`) with base and toy. The toy adds **89 finding lines**; 86 of them are
  outside the 3 training lines. In a random sample of 8 eval hits, most were text, not execution:
  - `MadoR17.AdversarialFixtures.jsonl:35`: `base64.b64encode(b'pacman -Q libfoo')`
  - `MadoR18.W3TripwireFinal.jsonl:69`: a `cmds = ["pacman -Q", …]` fixture list
  - `MadoR17.RevengeUnparsed.jsonl:83`: `"pacman -Q" in code`
  - `MadoR15.jsonl:310`: a quoted receipt string
  - `MadoR18.MutTripwireScan.jsonl:89`: a mutant table

  `TsukuroiR12.MatrixCriticR.jsonl:44` (`r("pacman -Qo …")`) looks like a real call [INFERENCE].
  Precision in the sample is about 1–2 out of 8.

So `tw-recall.py` plus the round-19 re-pin cannot tell a principled classifier from a string grep.
**C3 has no precision term, and its frozen controls are vacuous** (§3). This is a defect in the measure,
not just a tradeoff.

## 2. The 6/6 target cannot be reached by any rule that does not guess

The denominator comes from 9c54c56 `expected.json`: 3 expected lines plus 3 `known_misses`.
- `r15:1`, `r13-global:1` and `r14-review:1` are literal `sudo pacman` lines. They are already detected,
  and no draft touches them.
- All 3 known misses are named in their own notes as draft targets ("TwMissBashCVar target" ×2,
  "TwMissHelperFn target" ×1). The movable part of C3 is therefore n=3 training items.

Measured recall on the pinned inputs:

| variant | recall | frozen r18 | own suite | other drafts' suites | r17/r18 suites (compound 16, core 9, hardening 33, w2 30, frozen 31) |
|---|---|---|---|---|---|
| base | 3/6 | frozen_match | — | bashcvar 9/15, helperfn 13/24, installers 1/13 | all pass |
| B | **5/6** (r14-source-safety:2,3 → package_query/pacman:-Q) | mismatch, extra = exactly those 2 | 15/15 | helperfn 13/24, installers 1/13 | all pass |
| H | **3/6** (r13-root:4 still missed) | frozen_match | **22/24** | bashcvar 9/15 | all pass |
| I | 3/6 | frozen_match | 13/13 | — | all pass |
| BI | 5/6 | mismatch (same 2) | 15/15 + 13/13 | helperfn 13/24 | all pass |
| H0 = d9a5a18+H (authored base) | 3/6 | — | 24/24 | — | — |

Why `r13-root:4` (source `MadoR13.jsonl:470`) is out of reach:
- It calls `run_record('packages',['pacman','-Q',…],0)`.
- `def run_record` is at source line **437**. The frozen snapshot pairs are `[[1,35],[2,94],[3,98],[4,470],[5,506]]` (9c54c56 `provenance.json`), so the definition is not in the pinned bytes.
- `tw-recall.py:49-63` reads inputs only from PIN_REV, so no re-pin can add line 437 to C3's denominator.
- H's author already stated that a same-text rule cannot catch line 470 (`.ufo/waves/round-18/w1/reports/TwMissHelperFn.md:76-91`).
- The only kind of rule that can score this line is one that guesses an unresolved callee: "a literal argv list passed to an undefined function". I parsed 4832 py eval cells across the corpus (`/tmp/critc3/guess.py`). That rule fires on exactly **1** line, `MadoR13.jsonl:470`, the training line itself.

Precision 1/1 on the training item is not evidence; such a rule cannot be falsified on the available real data.

**The honest ceiling is 5/6.** 6/6 is reachable only by guessing, or by rules like the §1 toy.

## 3. The frozen "controls" give no precision evidence for these mechanisms

I profiled the 21 non-incident lines of the 5 frozen inputs:
- 0 controls define a helper (`def`/`f() {`). The only helper-shaped line is the miss itself, `r14-source-safety:2`.
- Only `r13-root:2`, `r13-root:3` and one bash line per file contain assignments.

So "control_hits=0" for B and H is close to vacuous: no control exercises the shapes they resolve.

## 4. Held-out evidence I gathered (the kind C3 must carry)

Differential scan of the full corpus (4523 files, about 3.6 GB), with each variant compared to base:

- **B:** new findings = **2**, and both are its training lines (`MadoR14.SourceSafety.jsonl:152,155`).
  0 new findings elsewhere and 0 lost.
  `unparsed_spawns` drops from 3471 to 2896: B resolved 575 spawns that base left unparsed, and all of them came out clean.
  This is genuine precision evidence for B. It also shows the corpus has no held-out positive B could have recalled.
- **H:** **0** new findings on its target. It adds 6 findings on 5 held-out Kengaku lines:
  - `KengakuScopeAudit.jsonl:140` (`pgrep`/`ps` through `run(cmd)`, shell=True)
  - `OomClassTaxonomy.jsonl:100,130` (`rows(['journalctl',…])`)
  - `ProviderSecrecy.jsonl:92,99` (`run(["journalctl",…])`)

  By inspection these are true positives. This is H's only real recall evidence, and C3 ignores it.
  **Regression:** `eval_unparsed` rises from 465 to 482 (+17) across 4 held-out transcripts
  (`KotobaHistoricalMarking:110`, `W2RoundKotoba.R46Reviewer-2:57` +9, `MadoR18.NoteTheme:25` +5,
  `TameshiR17.X01DispositionV2:179` +2).
  Minimal repro: `fetch() { slug="$1"; python3 -c 'import sys; print(sys.argv[1])' "$slug"; }\nfetch a x` gives base 0 and H 1.
  The finding is kept, but the "could not analyse" counter now lies.
  - With the same function shape and a hidden `pacman -Q` inside the Python body, base and H both report the finding.
  - With a plain `sudo pacman -S "$slug"` body, base and H both report the finding.
  - So this is counter inflation, not a recall loss.
- **I:** 0 contribution to C3 (none of the 6 lines involves an installer). It adds 84 findings on
  82 held-out lines, a new class `tool_install` (91 counts). In a sample of 5 these were real invocations:
  `uv pip install`, `uv tool install`, `npm install -g`, `npx -y rea-agents@6.x`.
  The operator directive authorizes uv tool/npx installs, so whether this class is "finding" or
  "permitted" is a policy question C3 cannot see. Its acceptance needs its own held-out evidence; C3's 6 lines are irrelevant to it.
- **Held-out recall base rate:** an independent lexical oracle (`/tmp/critc3/oracle.py`; `pacman -X` in
  shell form, or `'pacman','-X'` in argv form, inside bash/eval toolCall args) finds 559 candidate
  lines, 187 of them undetected by base.
  - I inspected all 22 argv-form misses and sampled about 25 shell-form misses.
  - Every one except `MadoR13.jsonl:470` was text, not execution: fixture builders, grep patterns,
    heredoc docs, receipt strings, base64.
  - I did not inspect the remaining roughly 140 shell-form misses individually.

  [INFERENCE] There are essentially **no held-out real positives** for the B/H mechanisms in this corpus.
  Held-out recall has to come from non-author adversarial fixtures, not from mined transcripts.

## 5. Integration hazards hidden behind "apply or reject"

- **B+H do not compose.** `git merge-file` reports 5 conflict hunks (docstring, `classify_python`
  spawn loop, `os.exec*` args, `subprocess` arg/shell resolution).
  - B resolves literals with `literal_value(expr, cenv)` and a per-call module env.
  - H resolves them with `resolve(expr, env)` plus `spawn_scan` recursion into helper bodies.

  These are two competing authorities for "what literal does this expression denote". Landing both
  needs a third, hand-written resolver that **neither draft's fixture suite was written against**. A
  two-hop case (module var → helper arg) exists only in the merge. H+I has 1 conflict (`SHELL_IDENT` block); B+I has 0.
- **H rebased fails 2 of its own 24 fixtures**:
  - `sh-fn-positional-n` wants `package_query pacman`, got `host_mutation pacman`.
  - `sh-fn-single-quoted` fails the same way.

  The cause is round-18's failsafe pacman op (be886a3): a non-literal pacman op now maps to host_mutation.
  The pre-registration requires "every existing suite still all-pass". If these expectations are fixed
  by copying what the rebased tool emits, that is the same circularity as §6. They must be changed by
  citing the be886a3 failsafe rule as the spec.

## 6. Circularity of the round-19 re-pin

- The pre-registration (17661e0 `SCORECARD.md`, C3 bullet) says "re-pin a round-19 frozen baseline **at the landed classifier**".
- `frozen-repin.py` sets `expected_findings` = the tool's own findings, and its self-check replays with **the same tool** (`FrozenRepinScript.md:28,108-110`).
- So the round-19 `frozen_match` is a tautology for every flipped row. It is a change detector, with zero correctness content for newly detected lines.
- Contrast round 18: those expected values came from committed receipts and oracles, "never by running the tool on this snapshot" (9c54c56 frozen `README.md`).

What is *not* circular:
- `tw-recall.py` pins the denominator and inputs at 9c54c56 (`:27`, `:49-63`), so a round-19 re-pin cannot move C3's denominator.
- The repin's `finding_on_unexpected_line` refusal does guard control lines.

What remains circular or lax:
- The **class/rule** of each flipped known miss is taken from the tool, not checked against the note.
- `tw-recall.py:73` counts "any finding (any class)". A line can count as detected with the wrong class, for example `live_probe` on a `pacman -Q` recipe.
- `known_misses` rows can be dropped by any tool that fires on the line (§1 toy).

## Impacted axes

- **C3 operability:** the claimed 6/6 is unreachable without guessing; the honest ceiling is 5/6.
- **Honesty/provenance:** the re-pin turns tool output into "expected".
- **Harm watch:** H fails 2/24 of its own suite after the rebase; H inflates `eval_unparsed` by 17 on held-out transcripts.
- **Maintainability:** B and H are duplicate literal-resolution authorities.

## Smallest safe correction

1. **Restate C3's target as 5/6**, with `r13-root:4` kept as a named known miss (snapshot lacks
   `MadoR13.jsonl:437`). Alternatively reject any 6th hit unless it comes from a rule with a stated non-guessing spec.
   Do not count H toward C3; credit H only with its held-out Kengaku true positives.
2. **Add a precision companion to C3, computed by L1 with the same tool:** a held-out differential scan of the full
   session corpus against base. Accept only if:
   - new finding lines outside the 6 = the explicitly listed, inspected set (B: ∅; H: the 5 Kengaku lines; I: separately judged);
   - lost findings = ∅;
   - `eval_unparsed`/`unparsed_spawns` do not rise.

   Under this rule H's +17 must be fixed or explained, and the §1 toy is rejected (86 unlisted lines).
3. **Make the re-pin non-circular.** Require `diff(r19 expected, r18 expected)` to equal exactly:
   - `+ {r14-source-safety:2, r14-source-safety:3} × (package_query, pacman:-Q)`, where class and rule come from the 9c54c56 known_misses notes (which quote `pacman -Q hyprland …`), not from the tool;
   - `known_misses` keeping `r13-root:4` verbatim;
   - nothing else.

   The round-18 baseline should then read `frozen_verdict_mismatch` with `extra_findings` = exactly those 2 rows and `missing_findings` = [].
   Tighten `tw-recall.py` detection to `(file, line, note-derived class)`.
4. **Use non-author adversarial fixtures as the held-out recall evidence for B/H**, since the corpus has none. Seed them with real near-miss shapes from §4:
   - fixture-builder calls `fx(...)`/`rec(...)` carrying argv lists;
   - `"pacman -Q" in code` membership tests;
   - base64 of commands;
   - `cmds=[...]` lists that are printed, not run;
   - shell functions passing `"$slug"` to `python3 -c`.

   B and H must stay clean on the data-only shapes and keep their `eval_unparsed` honest.
5. **Merge B+H with one literal resolver**, then run all of bashcvar 15, helperfn 24 (with the 2
   failsafe expectations re-specified from be886a3, not copied from output), installers 13, and the r17/r18 suites on the merged tool.
6. **Decide I separately from C3**: it has no C3 lines, and its class collides with authorized npx/uv-tool use.

## Limits

- I did not apply the drafts to the lane, run the live gate, or run `tw-recall.py` itself. I re-implemented its procedure in `harness.py`: same PIN_REV inputs, `python3 -I --scan`, cwd = temp. Base reproduces 3/6.
- I did not build or test a merged B+H tool.
- Held-out true/false-positive labels come from sampled inspection only: about 8 toy hits, 5 I hits, 6 H hits, and about 47 oracle misses. The oracle is lexical and covers pacman only; walker/hyprctl/systemctl helper shapes were not mined.
- The corpus included live, growing transcripts (`MadoR19.SentinelVcsFixtures` changed between scans). Counts are as of 2026-10-20 ~14:07–14:15 local time.
- I did not audit `frozen-repin.py` code beyond its author's report.

## Installs

none
