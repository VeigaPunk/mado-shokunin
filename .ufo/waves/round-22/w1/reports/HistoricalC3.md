# HistoricalC3 — r19 C3 six-line population: original markerless rows, later 5/1 interpretation, derived audit inputs

Artifact: `.ufo/waves/round-22/w1/historical-c3.json` v2 with attribution correction (sha256 `9ee6144d73342062fc1120afd2e4d4db4a52ec014f8a18744f116ab0dbebed7a`).

At AuditHarness's request, the artifact now carries the standard proposal fields at top level:

- **Top-level proposal** (`id`, `snapshot`, `claim`, `expected`, `rationale`): the derived six-row snapshot (digest `407f7500…76af`), claim 6/5/1 with 0 errors and `clean:false`, expected code 0 (`evidence_audit_clean`).
- **`derivation_provenance`:** names the unchanged raw receipt (path, sha256, commit, the digest of verdict line 3), the r19 counter receipt, the split authority `recall-split-final.txt`, the split producer, the receipt confirming the r19 output is markerless, the denominator, and the derivation steps.
- **`companion_proposals`:** the red r19 claim on the six-row snapshot; the red and green claims on the 11-row snapshot; and the markerless input, which is invalid. Each points to its snapshot by JSON pointer.

All provenance digests verify against both the committed bytes and the worktree bytes. Read at `eda932e`; the cited round-19/20/22 sources are byte-unchanged since `a963ce6`. Revised per the parent instruction and `audit-clarifications.md` (sha256 `db5e5c30…6176`, uncommitted). No detector, counter or payload was run. No private session was read, and nothing was installed.

## Result

- **No markerful r19 original exists.** The original r19 C3 rows are 11 findings on 6 incident lines, produced by tool `367be947` at `7b4839d`. None carries an `evidence` key. `recall-split-1f7f995.txt` runs the same tool and shows all 11 rows unmarked.
- **The original raw receipt is preserved unchanged** at `.ufo/waves/round-19/evidence/final/tripwire-frozen-scan-classes.txt` (sha256 `64648cca…f857`, committed `d642ce5`). It holds the r19 claim of `detected=6` and `unpermitted=11`. r19 never claimed an evidence split.
- **The 5 observed + 1 lead split is an explicit later interpretation.** It comes from the committed r20 split receipt `.ufo/waves/round-20/evidence/recall-split-final.txt` (sha256 `5165b728…f0a2`). That receipt was produced by r20 tool `9613f510` at `28c6837` over the same digest-pinned inputs. The r20 attempt-2 receipts at `3610e3e` (`16cf37cd…84b7`) and `a8960de` (`016975df…bbdd`) show identical markers. The artifact records this as `later_interpretation`, keyed by original row index, and never as an attribute of the original rows.
- **The markered snapshots are derived audit inputs**, not the original r19 output, not a new detector run, and not semantic precision evidence.
- **C2 cannot close r19 C3's semantic precision gap.** The prior r19 rejection (rejected-harmed) remains.

## Line classification (later interpretation)

| Incident line | Evidence | What the source text shows |
|---|---|---|
| `r15-libinput-events:1` | observed | literal bash `sudo pacman -S … libinput libinput-tools` |
| `r13-global-capture:1` | observed | literal bash `sudo pacman -S`, `wayland-info --version`, `pacman -Q` |
| `r14-review-source-bar:1` | observed | literal bash `sudo pacman -Sw --noconfirm wlr-protocols` |
| `r14-source-safety:2` | observed | recipe contains `pacman -Q …`; the same cell runs `subprocess.run(["bash","-c",recipe])` |
| `r14-source-safety:3` | observed | the `recipe2` rewrite keeps `pacman -Q hyprland`; the same cell runs `subprocess.run(["bash","-c",recipe2])` |
| `r13-root:4` | lead | `run_record('packages',['pacman','-Q',…],0)`; `run_record` is not bound by any definition, assignment or import in the 5 frozen lines |

Counted by row, the split is 10 observed + 1 lead. Three sources support it: the r20 tool marker, the author-lane critic `CriticC1Recall`, and this seat's reading of the frozen bytes. The non-author r19 spotcheck attributes `r13-root:4` to HelperFn rule B alone and gives no observed/lead verdict.

## Derived audit inputs

Digests use canonical JSON serialization and were rechecked after writing. Expected finding IDs are sorted unique lists, as the clarifications require.

| Input | How it was derived | Digest | Expected verdict |
|---|---|---|---|
| A: original rows, no markers | 11 rows cut down to the contract fields; no marker added | `9351abaa…32df` | code 2 (`evidence_audit_input_invalid`) for any claim |
| D1: rows plus later markers | 11 rows plus the later markers; `files[]` from the r19 receipt | `9507e816…e94b` | 11/11/0 gives code 1 (`lead_count_mismatch`, `observed_count_mismatch`); 11/10/1 gives code 0; 6/5/1 gives code 1 (`finding_count_mismatch`, `observed_count_mismatch`); `clean:true` gives code 1 (`findings_claimed_clean`) |
| D2: six-row line aggregate | one row per incident line plus the later markers | `407f7500…76af` | 6/6/0 gives code 1 (`lead_count_mismatch`, `observed_count_mismatch`); 6/5/1 gives code 0 |

**Attribution correction (per MadoR22).** r19 never claimed 6/6 observed. It claimed 6/6 detected (`tw-recall-after.txt`) and disclosed 5/6 without the HelperFn rule-B lead (`SCORECARD.md:1173` and `corpus/lessons/round-19.md:89`, both from `61eaa07`). Every claim in this file with `lead=0` and observed equal to the total is therefore a new counterfactual inflation probe against a derived snapshot. Those cases are now labelled `counterfactual-*-inflation` in the artifact; the earlier `r19-…-claim` labels are withdrawn and recorded under `attribution_correction`. The original receipt is untouched. Main's approved scope: the raw markerless input gets code 2 only, and the derived snapshots get code 0 or 1 only when honestly scoped as derived inputs.

## Gaps

1. **The markerful original is missing.** The 5+1 split exists only in later r20 receipts.
2. **Row and line counts differ.** "Five observed plus one lead" holds only for the six-row aggregate D2, which is a second derivation. D1 gives 10+1. Main or the AuditSchema seat must decide which derived input carries the green target.
3. **The r19 claim never stated a split.** It asserted only `detected=6` and `unpermitted=11`.
4. **Error counts are incomplete.** Only the original tool's counters are recorded (all 0). The later marker tool's counters on these inputs appear in no committed receipt.
5. **The lead holds only for the excerpt.** `r13-root:4` corresponds to `MadoR13.jsonl` source line 470. Committed evidence does not show whether source lines 99–469 defined `run_record`, and reading the session was out of scope.
6. **No outside-lane authority confirms the split.**
7. **The critic made a factual slip.** CriticC1Recall says `run_record` is "called once", but the tool-call code has 3 call sites. Its conclusion still holds.
8. **The receipt command is a label.** RECEIPT `cmd=scan_classes` is not a literal argv.
9. **The clarifications file is uncommitted.** Its digest is recorded in the artifact.

## Not claimed

This does not admit r19 C3's precision or general evidence, and it does not retroactively admit C3. Artifact consistency is not semantic truth.
