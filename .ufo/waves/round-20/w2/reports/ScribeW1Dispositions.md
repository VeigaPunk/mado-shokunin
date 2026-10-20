# ScribeW1Dispositions — partly falsified: L1 acted on most wave-1 findings with landed pointers, but 36 are not acted on and 25 are kept only as limits

## Behavior

Mapped every finding in the 33 wave-1 reports matching `Critic*`, `Rev*` (incl. `Revenge*`), `Sentinel*`, `Conn*` to a disposition in the landed files at lane tip `a4046a8216080d4004de3f268c62cf142095ac07`. Table: `.ufo/waves/round-20/w2/ScribeW1Dispositions/table.md` (sha256 `afa69867854c14a8be25c5fcaa2f0cdde50c082682fa0b8a80a6162778309c9e`, 225 rows). Reads were `git show a4046a8:<path>`; line pointers are at that commit. Nothing in the lane was edited; only the table and this report were written.

Disposition counts: FIXED 116, FIXED-PART 27, KEPT 25, RELOC 4, PENDING 3, NOT-ACTED 36, OUT-LANE 2, PROCESS 6, N/A 2 (four rows carry a compound disposition).

The falsification: the reading "L1 addressed the wave-1 review" does not hold for every finding. The C1 counter, the `tally-check.py` numerator fix, the isolation check's failure arms, and the S099–S112 source rows are repaired and pointed to. The corpus-diff harness, the counter's evidence/argv validation, the `exec`/`eval` purity rule, and several SKILL and tool wording items are not.

## Gates (checks this seat ran)

All run in `/tmp/mado-r20w2-ScribeW1Dispositions` (clone of `a4046a8`, `origin` removed). Parse-only or read-only; no fixture code was executed, no host command was run.

1. `python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json --set red --expect` → `TALLY_SUMMARY: set=red n=5 match=0 mismatch=5 error=0`, `EXPECT_SUMMARY: 5/5`, rc 0. `checker_sha256=21ce9dd57a47d975623aa9ca2bf53c3dadb8fa68b6f066a92461edba2fd2aea4`.
2. `--set green --rev a4046a8…` → `TALLY_SUMMARY: set=green n=4 match=4`, `EXPECT_SUMMARY: 4/4`, rc 0.
3. Numerator-swap exploit (CriticTally P1): registry with `line_regex "of (?P<stated>13) credited files name S096"` and `extract_regex "(?m)^denominator=(\d+)$"` → `ERROR swap stated=13 derived=none … extract_regex must begin (?m)^<key>= with <key> in current,first_line,any_line`. Closed.
4. `python3 -I .ufo/waves/round-17/measure.py a4046a8…` → `"c1": {"criteria": 30, "lesson_cited": 22, "score": 7.3333}`. Matches the declared 22/30; 30′ is one of the 30 criteria.
5. Tool fixture scans (`python3 -I tools/mado-tripwire.py --scan <fixture>`, fixtures written by this seat under `/tmp`):
   - vcs fixture (14 bash lines): clean for `jj log --help`, `git commit -n -h`, `git commit --dry-run -m x`, `git add -n .`, `git push -n origin master`, `jj describe -m --help`, `git --help commit`, `git clean -n`, `jj --ignore-working-copy git push --dry-run`; `observed` writes for `jj git push --dry-run`, `git commit -n -m x`, `git commit -m --help`, `jj diff -- --help` (snapshot), `git push origin master`. `observed_findings`/`lead_findings` present.
   - rule fixture (7 eval lines): `BLOCK=frozenset([...])` → no row; unbound `run_record(...)` → `lead`; `from x import *` then `frozenset([...])` → `lead`; `print = subprocess.run; print([...])` → `observed`; `exec("frozenset = unknown")` then `frozenset([...])` → `lead`; `from shlex import quote as q; q([...])` → no row; visible helper → `observed`.
   - exec fixture (2 eval lines): `exec("subprocess.run(['pacman', '-Q'])")` and `eval("__import__('subprocess').run(['pacman','-Q'])")` → `MADO_TRIPWIRE: clean`, exit 0, `eval_unparsed 0`. Silent false negative (RB-9).
6. Receipts read as bytes: `evidence/recall-split-final.txt` (`detected_observed 5, detected_lead 1, detected_unmarked 0`); `evidence/precision-heldout-final.txt` (12 of 12 `"pass": false`); `w1/corpus/pre-vs-harmed.json` (589 examples, all with `command`, 0 with `command_sha256`, 25 `<redacted>`); 11 `fetch/*/receipts.jsonl`.
7. Source-cell URL count in `corpus/SOURCES.md` S099–S112: S104=2, S107=2, S108=2 `https://` in the title/URL cell (census keys only the first).
8. `git grep` in `a4046a8` for `credentialId|thinkingSignature|providerPayload` under `.ufo/waves/round-20` → only the seat report itself.

## Findings (open items for L1, highest first)

1. **RB-9 — `exec`/`eval` are pure in the tool and their string bodies are not parsed.** `tools/mado-tripwire.py:1405` lists `exec`, `eval`, `compile` in `PURE_ARG_CALLS`. Fixture output in gate 5 is clean for a spawn inside an `exec`/`eval` string. The limit is not listed in `corpus/knowledge/tripwire-precision-r20.md:82-93` or `SKILL.md:562-575`. RevSpecRuleB asked for this to be excluded or treated as opaque.
2. **CI-7 — `NEVER_RUNS` exits 1, not 2.** `.ufo/waves/round-20/isolation-check.sh:172-173`. CriticIsolation asked for unevaluable → exit 2. A host where `unshare` is refused would read as a criterion-29 failure, not as "could not evaluate".
3. **CO-F1..F3 — the counter does not split presence from evidence, does not compare `argv0`, and does not type-check `observed_findings`/`lead_findings`.** `.ufo/waves/round-20/tw-precision.py:99,105` (tuple = class, rule, line, evidence); no reference to the verdict count keys (grep). A row that omits `evidence` is counted as observed (`:87`); disclosed only in `corpus/lessons/round-20.md:18`.
4. **CN-D1..D3 — the corpus-diff harness is unchanged in the three ways CriticNoHarmDiff named.** `.ufo/waves/round-20/corpus-diff.py:99` (one `--scan` subprocess per file), `:220-221` (additions keyed on evidence, so an observed→lead relabel is an "added" row), `:127-137` (no `tool_call_id` join; `command` not compared). The whole-corpus guard is still "pending (wave 2)" (`SCORECARD.md:1330`), so no claim rests on it yet, but the guard's stated semantics ("classes every added row", "loses zero") are not yet valid.
5. **CO-sit3 — the held-out probe is reported as "0/12 → 0/12".** The committed receipt `evidence/precision-heldout-final.txt` shows 12 of 12 cases `"pass": false` at `28c6837`. The landed prose gives only "outside the contract". The implication (the repair does not generalise to unseen shapes in this probe) is not stated.
6. **C2-2 / R30-2 — the 5/13 red still compares unlike rules.** `.ufo/waves/round-20/tally-claims.json` entry `r19-scorecard-c2-5of13-s096` derives `first_line` (6/13) at `1f7f995` against a stated 5/13 that the lesson itself says is RerunC2's cited-as-evidence reading at `01b8094` (`corpus/lessons/round-20.md:61-68`). The disclosure is there; the registry still makes the comparison RevCriterion30 called a false red.
7. **SP-H3 — `isolate.sh` accepts any target path and inherits the environment and session sockets.** `.ufo/waves/round-20/isolate.sh:56-61` has no `/tmp` allowlist and no `env -u`. The limit is stated (`corpus/QUALITY.md:246-248`, `SKILL.md:563-575`), so this is KEPT, not hidden.
8. **SP-L4 — `harm-watch.sh` runs the first bash fence after "### Counting command" with no digest check.** `.ufo/waves/round-20/harm-watch.sh:396-415`. No `8b59b503…` comparison (grep). The navigation block is REV-pinned (`:7-9`), but execution is not.
9. **CQ-1 / RH-2 — the R19-V5 keep-open tail has no owner row.** Worktree-ledger (`supersede-sweep.py`), harm-watch provenance and the anchor-alias hole are not listed as open anywhere in the landed round-20 prose (grep for `anchor-alias`/`worktree` in `SCORECARD.md`, `corpus/lessons/round-20.md`, `LOG.md` returns none). `HarmWatch20.md:38` records it only in a wave-1 report.
10. **RS-E1a/b — "issued command" wording remains.** `SKILL.md:531` ("an issued command to disclose") and `SKILL.md:622` ("It records commands") are unchanged; the new section at `SKILL.md:542-566` is additive. RevSkillTripwireText asked for replacement.
11. **CSO-2 / CSO-4 — source rows do not follow the census rule the sibling seat derived.** S104, S107, S108 carry a second `https://` in the title/URL cell; S109 keys the peeled commit `d76cbf8f…` rather than the `v2.42.4` tag path.
12. **SP-H1 / SP-H2 / SP-M2 / SP-M4 — wave-1 dispatch text was not changed.** `.ufo/waves/round-20/gen_w1.py:46-48` has no PRECEDENCE clause and no `git remote remove origin` instruction; labrat context (SP-M4) and `--selftest` env clearing (SP-M2) are unchanged. The wave-2 dispatch context carries the corrected text (PROCESS rows); the landed generator does not.

## Limits

- Table completeness is by report: every finding line in the 33 reports was read; some reports' minor items were grouped into one row (e.g. CriticHonestyR20 A/B/C/D lists). Per-line exhaustiveness is not claimed beyond that grouping.
- [UNK] items: whether the harm-watch `--regression` gate returns SETUP on a harness sha mismatch (SP-M1); whether `reset` restores builtins in the tool (RB-2); whether `harm-watch.sh` REV pinning is exercised end to end (RH-1, not run); roster join of 85 w1 seats against `dispatch.json` (HR-D6, not run).
- Not run: `isolation-check.sh` and `isolate.sh` (canary harnesses; I did not execute them, and the cited receipts were read as bytes); `corpus-diff.py` (hour-scale); `sources-census.sh validate` (fleet script, 21 roots); `tw-precision.py` (its receipts exist in `evidence/`).
- `[V]` claims are limited to the commands listed under Gates. Other "FIXED" rows cite landed pointers without re-execution.
- Relocated corrections (RELOC rows) are append-only in `corpus/lessons/round-20.md`. The original lines in `round-19.md`, `SCORECARD.md:1133/1167/1225` and `LOG.md:1323-1325` are unchanged by design.
- Out of lane: `.ufo/reports/round-19/mado.md:109-110` (R19-V5 "ten" sentence) is a fleet-root file; not edited.

## Installs

none. This seat ran `git`, `python3 -I`, `grep`, `sha256sum` only. No pacman, sudo, hyprctl, systemctl, gate run, host probe, or package query.

## Touched surfaces

- Written: `.ufo/waves/round-20/w2/ScribeW1Dispositions/table.md`; `.ufo/waves/round-20/w2/reports/ScribeW1Dispositions.md`.
- Outside lane (scratch, not committed): `/tmp/mado-r20w2-ScribeW1Dispositions` (clone, `origin` removed) including `fx/*.jsonl`, `fx/swap.json`.
- Lane: read-only (`git show`, `git grep`, `git ls-tree`, `git diff --stat`).
