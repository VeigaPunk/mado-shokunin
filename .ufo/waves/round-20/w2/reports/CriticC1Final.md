# CriticC1Final — partly falsified: C1 numbers reproduce (29→172/175, guards green, no measured regression) but it is a scope-local repair — registered target 175 missed, held-out 0/12 unchanged (3 pre-harm passes unrecovered), and no-harm stands on a corpus diff that is still pending.

Item attacked: "Is C1 (29/175 → 172/175, target 175/175 missed by 3) an admissible improvement with no harm?"
Workspace: `git clone` of the lane at `/tmp/mado-r20w2-CriticC1Final`, origin removed. All commands run there (absolute paths below abbreviated to repo-relative; the clone is byte-identical to `a4046a8`).

## Reproduced measurements (ran every named check myself)

| Check | Command (run in `/tmp/mado-r20w2-CriticC1Final`) | Claimed | Observed |
|---|---|---|---|
| Precision @28c6837 | `python3 -I .ufo/waves/round-20/tw-precision.py 28c6837` | 172/175 | **172/175**, score 9.8286; fails = `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` |
| Precision @1f7f995 | same, `1f7f995` | 29/175 | **29/175**, score 1.6571 |
| Precision @9c54c56 | same, `9c54c56` | 110/175, P 66/66 | **110/175**, score 6.2857; P **66/66** ✓ |
| Held-out @28c6837 | `tw-precision.py 28c6837 --heldout` | 0/12 | **0/12**, score 0.0 |
| Held-out @9c54c56 / @1f7f995 | same revs `--heldout` | (in `before` fields) | **3/12** at 9c54c56 (fx3/fx8/fx9), **0/12** at 1f7f995 |
| Recall guard | `python3 -I .ufo/waves/round-20/tw-recall-split.py 28c6837` | 6/6 = 5 obs + 1 lead, 20 controls 0 | **detected_observed 5, detected_lead 1, undetected 0, control_findings 0** ✓ (lead = `inputs/r13-root.jsonl:4`) |
| 11 suites 247/247 | `python3 -I tools/mado-tripwire.py --selftest <dir>` ×11 | 247/247 | **247/247** (16+9+33+30+31+1+45+13+34+18+17; adversarial suite excluded — see below) |
| Frozen guards | `--frozen .ufo/waves/round-19/frozen`, `--frozen .ufo/waves/round-18/frozen` | match / expected red | `frozen_match` / `frozen_verdict_mismatch` (3 extra `pacman:-Q` rows, per registered expectation) |
| Suite pin hygiene | `git show f3da504:tools/mado-tripwire.py \| sha256sum` | suite lands with no tool change | tool identical at `1f7f995` and `f3da504` (`367be947…`); `28c6837` (`9613f510…`) touched **0** files under `precision/` |
| Whole-corpus diff vs 9c54c56 | `.ufo/waves/round-20/corpus-diff.py` exists; run assigned to CorpusDiffV2 / CorpusDiffIndependent | pending | **still pending** — the registered C1 admission guard ("loses zero findings") has no verdict yet |

## Findings

**F1 — The repair does not generalize off-suite: held-out 0/12 → 0/12, including 3 cases the harm itself broke.** At `9c54c56` the held-out counter passes `fx3-jj-log-version`, `fx8-uv-tool-install-help`, `fx9-pip-install-help` (verified: score 2.5); at `1f7f995` and `28c6837` all three fail. Got: `jj log --version` → `vcs_write jj:log` *observed* (jj 0.45.1 rejects it, rc 2 — S104's own `DisplayHelp | DisplayVersion` early-return; the repair's `jj_prints_help` exempts `-h/--help` but never `--version`); `uv tool install --help` → `tool_install uv:tool-install` *observed*; `pip install --help` → `tool_install pip:install` *observed*. Each is a **false "observed" row for a run that executes nothing** — the same defect class C1 claims to fix, still live outside the registered `git`/`jj` scope. The case files themselves say "EDGE (outside the TwRuleB/TwVcsHelp patch scope)", so this is registered scope-not-defect — but it proves the improvement is suite-local, and "pre-harm reading restored" is *not* true on this 12-case probe (P-family guard covers only the scored suite).

**F2 — The 3 scored misses decompose into two defects and one stale expectation:**
- `H-…-jj-var-verb-help` (`jj $c --help`, want clean): tool emits `vcs_write jj:$c` **observed**. Unknown verb + `--help` is deliberately fail-closed ("may be a config alias", tools/mado-tripwire.py:77-78) — a defensible conservative choice, but `observed` asserts an execution path the tool did not observe (unknown verb, unknown alias). An honest emission would be `lead`; this is **false provenance under the tool's own observed/lead contract**.
- `L-…-AdvHelperFn-b14` (`run_case('q', literal-argv)` where `run_case` is an opaque parameter): want `lead`, got nothing. A literal argv to an unresolvable callee is exactly the registered `lead` definition — the tool *under-reports* here (asymmetric with `class-method-instance` below).
- `W-CaseWrapperForms-class-method-instance` (`Runner().run(literal)`, class + method + call all visible): want clean, got `pacman:-Q` observed. The emitted finding is **semantically correct** (the transcript states argv and execution path; `callable_info` resolves `Call.func=Call` → class → method). The expectation is the stale artifact — E1/E2 scope names `def`/`lambda` helpers only. This miss is arguably a tool-vs-scope disagreement, not a precision error; [INFERENCE] had the expectation been `observed`, the score would be 173/175.

**F3 — The 8 `r20_edit` suite edits all flip want 0→1 findings — one-directional, self-ratifying in shape — but each payload verifies.** I read all 8 case bytes and their `r20_edit` reasons: `class-body-deferred` (class body runs at def — correct per execution model), `py-helper-nonliteral-arg` / `py-lead-defined-nonliteral` (literal module binding → visible spawning helper), `py-helper-defined-after-call` (unbound at call → `lead`), `py-helper-redefined` (binding at call = the second visible def), `py-helper-vararg`, `py-helper-default-nonliteral`, `py-lead-nonliteral-var` (unbound callee → `lead`). Every added finding corresponds to a genuinely-executing command; the edits tighten the suite toward ground truth rather than laundering regressions. Residual caveat: the same author who wrote the repair edited the expectations, so the guard is weaker than an independent suite — mitigated by the reasons being checkable (and checking out).

**F4 — Excluded from 247 without stated exclusion.** The 11-suite / 247 figure silently excludes `.ufo/waves/round-17/w2/adversarial` (26 cases, `6/26` at `28c6837`). Legitimate — its note declares ideal-detector expectations ("every FAIL is an honest blind spot") — and it is *not* a regression (6/26 at 1f7f995 and 9c54c56; the repair actually fixed `eval-var-argv` and `eval-concat-argv`). But SCORECARD:1330's "11/11 all-pass" is precise only because the blind-spot suite was never in the 11; the composition (16+9+33+30+31+1+45+13+34+18+17) is documented at `corpus/lessons/round-19-verifier-spotcheck.md:89`. No falsification; a naming footgun for wave-2 reruns.

**F5 — No-harm is measured-everywhere-except-the-one-place-that-counts.** Recall 6/6, controls 0/20, P 66/66 at both revs, adversarial identical, frozen replays as expected — yet the pre-registered C1 guard "a whole-corpus diff of the `9c54c56` and final tools loses zero findings and classes every added row" has **no result** (`SCORECARD.md:1330` admits "pending (wave 2)"; corpus-diff.py exists unrun). The new evidence-kind machinery (`observed`/`lead`) changes row shape corpus-wide; only that diff can show whether a `9c54c56` finding was reclassified or dropped on real transcripts. Until CorpusDiff* seats report, "no harm" is unproven, not false.

## Admissibility verdict

- **Improvement: real and large** (29→172/175 on a suite the tool author could read but whose cases were authored blind; +62 scored cases vs pre-harm 110/175; adversarial blind spots only improved).
- **Target: missed** — 172/175 ≠ registered N/N; admission must record the miss, not round up.
- **Harm: none measured, one unmeasured** — every guard I ran is green or expected-red; the corpus-diff guard is open. Conditional on that diff losing zero findings, C1 is an admissible *partial* improvement: admit-as-partial (score 9.8286, not 10), carry the 3 scored misses + 3 unrecovered held-out regressions as named defects.
- **Smallest safe corrections** (ranked): (1) wait for/tie admission to the corpus-diff verdict — the only unrun registered guard; (2) exempt `--version` after a `JJ_HELP_VERBS` verb (S104: DisplayVersion returns before workspace load) — fixes `fx3`, a real unrecovered regression; (3) decide `class-method-instance` by editing the expectation to `observed` (finding is correct) *or* dropping `ast.Call` attribute resolution (re-check suite + held-out before choosing — the latter may break passing W cases); (4) emit `lead` for unresolved-Name calls with literal argv (fixes `b14`) and consider `lead`-marking `jj:$c --help` instead of `observed` (fixes the provenance stretch); (5) `uv|pip` help exemptions — same defect family as `fx3` but outside registered scope, so optional for admission, real for criterion 30's spirit.

## Limits
- Did not run `corpus-diff.py` (assigned to CorpusDiffV2/CorpusDiffIndependent; running it here would duplicate their item).
- Did not independently fetch S104/S103 to verify `DisplayVersion` early-return; relied on the committed SOURCES row and the case authors' probe claims — [INFERENCE] on jj internals, direct measurement on tool output.
- Held-out `want` readings are the case authors'; e.g. `a01` expects clean on a same-text `pacman()` shadow — consistent with registered E3 but unverified against real bash.
- Lane files untouched; all runs in `/tmp/mado-r20w2-CriticC1Final`. Lane reads were file-bytes only.

## Installs
none
