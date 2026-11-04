# R85ReviewerC2 — frozen C2 falsification

Revision: `3905311c75a39c5710413105865c0a1a7dd0116a`; base: `5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`.
Axes: operability (C2), with coverage of the status-class and matcher counterexamples. Recommendation: **C2 does not verify as declared at the freeze**. This is a review recommendation, not admission or integration.

Only the assigned report and reviewer scratch were written. A clean scratch clone had the exact frozen HEAD and zero working-tree changes. No successor edits were used. No tools installed. LSP device discovery returned `No such tool: xd://lsp`; semantic references/definition/diagnostics were unavailable. Findings below use pinned source inspection and explicit executions, not semantic-search claims.

## Findings, highest severity first

### High — canonical counting command refuses before executing any case

Frozen `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py:729-737` does not include `status` or `negatives` in its allowed carried supersessions. Running the full frozen counter against the clean frozen clone, with the frozen C2 controls and round-84 carried controls, produced:

```text
exit=2
MADO_R85_RUNBOOK: ERROR (stage=setup carried case 'version' changes field 'negatives')
```

The same setup refusal affected the separately constructed A/B/C executable cheats. Their canonical scores are **not produced**, not 0/36, and setup refusal is not evidence that a case killed a cheat. The diagnostic scores below deliberately bypass main's preflight by loading the frozen functions and invoking `case_correct` on captured live observations. They are not canonical TARGET_MET verdicts.

### High — frozen documented rows cannot satisfy the binding gate

Frozen `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md:231` names `### Executable runbook rows (round 84)`, while the C2 counter expects the round-85 heading. Its actual `command_rows` result on frozen SKILL.md is **0**. Changing only that heading in memory exposes **33**, not 36, rows; this is a diagnostic, not a repository change. Thus `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py:761-764` would independently refuse the frozen document even after the carried preflight were corrected.

The binding algorithm itself is appropriately bijective: exactly 36 rows; exactly one matching command cell per case; no row reused by another case; all 36 bound; and each executed argv must document the same command (`:761-782`). It does require exactly one SKILL.md row per case. The freeze simply does not supply those rows.

### High — four declared matcher mutants survive the same frozen population

I executed all 36 frozen argv commands once in the clean frozen clone, using the frozen counter's `run`, with TMPDIR inside reviewer scratch. Then I scored the same observations and unchanged frozen samples/negatives through each isolated cheat. Base `case_correct` scored **36/36**.

| Cheat | Isolated score | Killing evidence / survivor |
|---|---:|---|
| A: round-84 blanket `rc != 0` failure in `matches` | 34/36 | `status-exit7-contained` and `status-sigpipe-contained`; their live statuses and positive samples are nonzero. Their rc=0 negatives also become incorrectly accepted. |
| B: any nonzero for both exact and signal | 34/36 | `status-exit7-contained` accepts negative index 1 (rc=141); `status-sigpipe-contained` accepts negatives 1 and 2 (rc=7 and 128). Indices are zero-based. |
| C: `re.search` instead of line-anchored matching | **36/36** | **Survives**; neither version case kills it. Both frozen patterns already contain `^` and `$`; their suffix-extension negatives remain rejected without the separate line matcher. |
| D: drop the negative-sample loop | **36/36** | **Survives**; no case kills it. Removing a conjunct cannot reduce an already perfect score. |
| Additional: declared `line-anchor-prefix` | **36/36** | **Survives** for the same already-anchored-pattern reason. |
| Additional: declared `samples-skipped` | **36/36** | **Survives**; dropping the positive-sample conjunct also cannot reduce a perfect score. |
| Additional: signal class accepts any rc in 129..255 | **36/36** | **Survives**; signal-row negatives are only 0, 7, and 128, never another signal-like status. The population does not establish the *named* signal requirement against this cheat. |

These four declared survivors (`regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped`) disprove a semantic 37/37 kill claim over the frozen scoring population, independently of the setup blockers. I did not claim an observed full canonical kill total: that run stopped at setup.

Frozen source hashes used for these diagnostics:

```text
counter SHA256 e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471
controls SHA256 de8a68fe22799d4bf8366ab56c9d390559260dc8a70c3d1d7e0d03da98d23b64
```

### High — several accepted rows bypass their declared status class

`/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py:481-508` special-cases producer_failure, is_active, pid_state and refusal before reaching the status-class gate in `matches`. Frozen refusal rows declare `status: ok` but accept rc=3; `producer-failure-propagated` declares `ok` but accepts rc=7. I directly observed both behaviors using committed positive samples. Live `hypridle-is-active` also returned rc=3 and matched its special outcome. Thus “ok means exit 0” is not enforced for every row despite the universal declaration. The special outcomes may be useful, but the declared class and actual accepted status contradict one another.

### Medium — signal death is observationally indistinguishable from exact exit 141

The actual frozen guarded command produced:

```text
stdout: MADO_STATUS: sigpipe line 0
rc=141
```

The unguarded `status-sigpipe.sh | head -n 1` reports 0; guarded reports 141, as claimed on this host. The normal and exit7 fixtures report guarded 0 and 7 respectively. `status-sigpipe.sh | cat` reports 0 even with pipefail, confirming downstream closure is essential.

However `status_ok({class: signal, signal: 13}, 141)` and `status_ok({class: exact, code: 141}, 141)` both return True (`:345-358`). An explicit exit 141 is indistinguishable from shell-encoded SIGPIPE using this observation alone. The measurement verifies numeric 141, not independently that the producer died by SIGPIPE. No frozen case distinguishes these classes at the same numeric status.

### Medium — additional canonical blockers remain downstream

The mutation source-anchor check counts occurrences in the entire source, including the MUTATIONS declaration itself (`:803-806`). Direct counts in the frozen source were: refusal-stage-blind=3, refusal-rc-blind=3, signal-as-exit=3, line-anchor-prefix=2, negatives-skipped=2, samples-skipped=2. These anchors would be refused rather than meaningfully scored. To construct diagnostic D, I limited replacement to the executable `case_correct` function instead of changing its mutation-declaration string too.

Also `classes` is initialized as an integer (`:745`), incremented as an integer (`:752`), then passed to `len(classes)` (`:827`), which would raise TypeError if reached. This is a static downstream finding, not a claimed observed traceback.

## Residual risk and verification gaps

- All four requested cheats were constructed; A/B/C canonical executions refused at the frozen preflight; D and all four were successfully scored in the explicitly isolated predicate diagnostic. Canonical no-score and isolated score are intentionally distinct.
- No full 37-mutant canonical result exists from this review because the original run stopped at setup. No successor revision was reviewed or credited.
- The misspelled alternate controls pathname in the assignment was absent; the explicitly corrected frozen population `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/controls/c2-cases-r85.json` was used.
- Runtime identity/rerouting/resume contracts are not changed by this C2 surface. No saturation inference follows from these measurements.
- Reviewer scratch was removed after recording results. This report preserves the observed outputs and hashes; temporary files are not cited as durable evidence.

Self-check: accuracy 4/5 (canonical gate blocks an end-to-end kill total); completeness 5/5 (four cheats and three measured-path questions covered); clarity 4/5 (canonical versus isolated scoring requires explicit distinction); actionability 5/5 (line-specific blockers and exact surviving cheats); conciseness 4/5 (multiple independent blockers require detail). Overall 4.4/5. Highest-impact next action is to preserve the frozen refusal honestly and separately evaluate any successor without claiming frozen 37/37.
