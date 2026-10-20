# RevRecallControls — recomputation confirms 6/6 is row-presence recall, with one E1 lead

## Scoped verdict

The frozen denominator is six distinct `(file, line)` incident pairs, not eight finding rows; the five pinned inputs contain 26 lines, leaving 20 controls. The sole pair detected by HelperFn rule B alone is `inputs/r13-root.jsonl:4`. Under E1 this is a **lead** row because `run_record` has no visible body/binding in that transcript; it still counts in `tw-recall.py`'s numerator because the counter tests only `(file, line)` membership in `findings`. Thus a future 6/6 can mean all six pinned lines still have at least one finding, with five observed lines and one lead line; it cannot mean all six prove execution.

## Recomputed denominator and line sets

Source: `.ufo/waves/round-18/frozen/expected.json` read from `9c54c56`; SHA-256 `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`. Its `expected_findings` has eight rows on three distinct line-1 pairs; `known_misses` adds three distinct pairs. `tw-recall.py:50-51` unions those sets. The five pinned JSONL files total 26 lines (scanner per-file line counts: 5, 5, 5, 6, 5), so 26 − 6 = 20 controls.

| Input | Incident line(s) | 20 control line(s) |
|---|---:|---|
| `inputs/r15-libinput-events.jsonl` | 1 | 2–5 |
| `inputs/r13-global-capture.jsonl` | 1 | 2–5 |
| `inputs/r14-review-source-bar.jsonl` | 1 | 2–5 |
| `inputs/r14-source-safety.jsonl` | 2, 3 | 1, 4–6 |
| `inputs/r13-root.jsonl` | 4 | 1–3, 5 |

Direct `--scan` of those pinned bytes with the `9c54c56` tool (`c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`) returned exit 1 / `findings`, exactly eight expected rows, all on the three line-1 incident pairs. It detected 3/6 incident lines; `tw-recall.py 9c54c56` independently returned `incident_lines=6`, `detected=3`, `score=5.0`, with the three `known_misses` undetected.

The `e629f73` tool SHA-256 is `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`; `1f7f995:tools/mado-tripwire.py` independently hashes to the same value. Scanning the same inputs with this tool returned exit 1 / `findings`, 11 rows on exactly the six incident pairs; `tw-recall.py e629f73` returned 6/6 (score 10.0). Neither scan had a finding on any of the enumerated 20 controls. All fixture inputs were scanned as text and were never executed.

## Rule-B-alone attribution

The round-19 spotcheck says at `corpus/lessons/round-19-verifier-spotcheck.md:65` that `inputs/r13-root.jsonl:4` is the HelperFn rule-B-only hit and removing B leaves 5/6. I independently reproduced this with a temporary copy of the `e629f73` tool: replacing only the `hits.extend(helper_argv_leads(node, env))` emission at `tools/mado-tripwire.py:1431-1433` with `pass`, then scanning the same five frozen inputs, returned 10 rows and 5/6; `r13-root.jsonl:4` disappeared while the other five incident pairs remained. The output was still exit 1 / `findings`.

The same ablation explains the precision harm. The spotcheck's data-only `BLOCK=frozenset(['pacman','-Q','hyprland'])` fixture (derived in `/tmp`, SHA-256 `d7c37ac362414d64762ef64a6f1955fd59ff9382199557c72536a0f7d0300925`) scanned clean at `9c54c56`, produced an unmarked `package_query/pacman:-Q` finding at `e629f73`, and scanned clean with rule B ablated. Fixture code was not run. This proves rule B is the sole source of both this pure-data false positive and the `r13-root.jsonl:4` recall row. Repair needs to distinguish pure calls (E2) from invisible-body leads (E1); deleting the shared route alone loses the sixth hit.

## E1 classification and counter semantics

`r13-root.jsonl:4` calls `run_record('packages', ['pacman','-Q','wayland-utils','wayland','wayland-protocols','hyprland'], 0)`. I parsed the three eval-cell source strings from that JSONL transcript into Python ASTs without executing them: there are calls to `run_record`, no function/class definition, assignment, or import binding it, and all three eval `reset` flags are false. Therefore the literal pacman argv is handed to an unbound bare name whose body is not visible in the transcript: E1 classifies this as **`evidence: "lead"`**, not observed. The separate `run_record` call with the repository's `sources-census.sh` argv does not classify as a host command. No LSP device was mounted (`read xd://lsp` returned “No such tool”); the binding check used transcript AST inspection and the rule-B ablation, not grep output as semantic proof.

`tw-recall.py:73-74` builds `hit` from only `(file, line)` for each row in `verdict["findings"]`, then counts a pair as detected if it is in that set. It ignores class, rule, and evidence. Its lines 69–70 accept either scanner return code 0 or 1 and require parseable output, but do not enforce exit 1 or the `findings` label. E1 separately requires lead rows to remain in `findings` with exit 1 / label `findings`; if the corrected tool emits the required lead row on line 4, `tw-recall` still counts it. The pre-E1 `e629f73` row has no `evidence` key; under the registered comparison rule an absent key is interpreted as `observed`, which is not a sound E1 classification for this line.

## Meaning of “6/6 retained”

**It will mean:** at least one row in `findings` exists for each of the six fixed incident `(file, line)` pairs, whose denominator and source bytes are pinned to `expected.json` and the inputs at `9c54c56`. With E1 applied correctly and all six hits preserved, the expected split is **five observed incident lines plus one lead incident line**.

**It will not mean:**

- that `pacman -Q` is proven to have executed on `r13-root.jsonl:4`; E1 marks that line as a lead because the callee body is absent;
- that all six rows have unchanged class/rule or evidence quality—`tw-recall` ignores class, rule, and the `evidence` field;
- that the rule-B pure-data false positive or any broader precision issue is repaired—`tw-recall` is recall-only, so the pure-container and whole-corpus precision guards remain necessary;
- that the round-20 implementation actually achieved the split or the precision result. The 6/6 result measured here is `e629f73` (pre-E1); the ablation measured 5/6. The final round-20 tool must be checked separately.

## Findings (ordered by severity)

- **Informational — recall metric boundary:** “6/6 retained” is positional row presence, not six observed executions. In particular, the only rule-B-only pair is an E1 lead and still contributes to the numerator.
- No additional actionable finding within this scoped recomputation.

## Residual risk and verification gaps

The final round-20 implementation was not available/checked here. This report does not establish that it emits the required `observed_findings` / `lead_findings` split, fixes the pure-data false positive, preserves the 20 controls, or passes the broader precision and suite guards. No LSP device was mounted; this limitation is recorded above. No fixture code, host package command, host probe, or live operation was executed.

## Limits

Scope was the frozen denominator, 20 controls, rule-B attribution and E1/tw-recall semantics. No round-20 tool or precision suite was evaluated. No code was changed; only this report was written in the lane. Temporary scans, tool copies, and the data-only fixture were under `/tmp`.

## Installs

None.
