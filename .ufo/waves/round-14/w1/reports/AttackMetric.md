# AttackMetric — rendered report (mado round 14, w1)

Status: critic review, read-only. Nothing was run: no gate, selftest, measure or fixture. No tools were installed or upgraded. The only writes are this file and `.ufo/waves/round-14/w1/AttackMetric.md`.

Bound bytes:
- baseline gate `873ff08` sha256 `037b05dc…6569`
- working-tree gate sha256 `abdd7e94…840d` (uncommitted)
- `.ufo/waves/round-14/measure.py`
- `SCORECARD.md:457-483`

## Counterexample

"Baseline detects zero directory sources" is false in general. A directory in place of any of the 7 `~/.config/hypr` direct targets already fails `hypr.local.inventory` (`missing:`, B:2466). In place of the theme include it fails `theme.chain.hypr_include` (`target missing`, W:3407). So 8 of the 17 direct targets already exit 1 at baseline [INFERENCE].

Only two groups are fully silent at baseline:
- the 9 omarchy `default/hypr` direct targets
- both glob shapes: `compgen -G` matches directories (B:2422), and the no_gaps row only drops to a NOTE

The landed measure and selftest (N9) put the direct case on `default/hypr/windows.conf`, not on the `ai-usage.conf` named in the L1 brief. That makes the predicted baseline overall exit 0/3. The zero is real for these fixtures but was never declared, and the caution at SCORECARD:474-475 is no longer measured.

## Source evidence (opened)

- Canonical URL: https://github.com/hyprwm/Hyprland/blob/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp#L1816-L1849
- Pinned revision: tag v0.56.2, commit date 2026-08-05. Installed version is `hyprland 0.56.2-2`.
- Opened: 2026-10-20.
- Quote: `else if (std::filesystem::is_directory(file_status)) { Log::logger->log(Log::WARN, "source= skipping directory {}", value); continue;`
- Tier: A, legacy `source=` handler only; not exercised on the live compositor.
- Decision: admitted as review evidence only.
- Flip: a non-0.56 build, the lua config manager, or an upstream change that makes this branch an error.

What this means for the claim:
- Directory sources and directory glob matches are skipped silently. A missing target or a zero-match glob is a Hyprland error.
- So `non-regular:` is a gate fail-closed policy, not a mirror of a Hyprland error.
- The mixed-glob case behaves like a clean config at runtime. Refusing it is policy and must be labelled as policy.

## Defects in the `measure.py` predicate

| # | Defect | Smallest fix |
|---|---|---|
| P1 | A gate that names every glob match as non-regular, including the regular sibling, still scores | Parse the `non-regular:` segment and require it to equal exactly the expected `~/` path; `affected_path` is already computed |
| P2 | `unresolved:` co-listing is never checked | Require no `unresolved:` in scored details |
| P3 | The basename check is a substring over the whole detail | Covered by P1 |
| P4 | "Stable" diagnostics are never measured, so a temp-root leak would pass | Rebuild each case under a second root and require a byte-identical detail, or drop "stable" from the claim |
| P5 | Isolation is not asserted | Require the FAIL row-id set to be {`hypr.root.sources_resolve`}; no_gaps D PASS, G NOTE, M PASS |

Missing unscored controls:
- R2 overlap: `ai-usage.conf` as a directory. Predicted baseline exit 1 via local inventory.
- R3 class retention: direct missing and zero-match glob should stay `unresolved:`, identical before and after.
- R4 symlink-to-regular: should PASS, or the gate comment's claim should be dropped.

## Rubric for L1 (before measuring)

Scored cases are D (`windows.conf` dir), G (the only toggle match is a dir) and M (`dir.conf` dir beside the regular toggle). A case earns credit only if all of these hold:

1. The fixture shape is asserted before the run.
2. Exit is 1 and the verdict is `DIVERGED`.
3. There is exactly one `sources_resolve` row, and it is FAIL.
4. The parsed `non-regular:` segment equals exactly the expected path.
5. The detail contains no `unresolved:`, `missing:` or `extra:`.
6. The FAIL row-id set is exactly {`hypr.root.sources_resolve`}.
7. The detail is byte-identical across two roots.

Score = 10 × Σcredit / |S|. Report baseline and after revisions separately.

Printed but never scored: overall exits, R2, R3, R4, the clean control, order-swap (N12 shape), and the round-13 four cases. Never fold these into a combined 7-case figure.

Claimable headline: owning-row named non-regular diagnostics 0/3 → 3/3, and overall exit on these fixtures 0/3 → 3/3, with the baseline already exiting 1 for 8 of 17 direct targets through non-owning rows.

Not claimable:
- baseline blindness to directories
- Hyprland errors on directory sources
- mixed-glob config breakage
- symlink, whitespace or multi-match-order policy
- operability saturation

## Classification

- P1-P5, R2 and R3 are fixable defects.
- The mixed-glob strictness is a tradeoff. The judge should accept it only when it is labelled as policy; otherwise reject it as false provenance.
- Harm watch: every live source target is a regular file under `stat -L`, so `--no-live` is predicted unchanged [INFERENCE]. L1 measures this once.

Checks for L1 to run: `python3 .ufo/waves/round-14/measure.py <baseline>` and `<after>` with the rubric fixes, `bash tools/mado-verify.sh --selftest`, `--no-live`, and the regression recut.
