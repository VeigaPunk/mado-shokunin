# AttackMetric — C2 three-case metric vs baseline detection (mado round 14, w1)

Seat: critic, leaf. Axes judged: coverage (not touched here), operability (C2).
Milestone: U5 boundaries and regular-source targets.
Status: read-only review. No gate run, no selftest, no measure run, no fixture built.
Writes: this file and `reports/AttackMetric.md` only. Tools installed or upgraded: none.

Inputs, read at the bytes present during review:
- committed baseline gate `873ff08:tools/mado-verify.sh`, sha256 `037b05dc…6569` (the working-tree bytes when the review started)
- working-tree gate after GateImplement's edit, sha256 `abdd7e94287657985062b03a9c8b53c571aa10b413df3794c34e02fd3f88840d` (uncommitted; +162/−11)
- `.ufo/waves/round-14/measure.py` (MeasureBuild, 335 lines)
- `SCORECARD.md:457-483` (round-14 declared claims)
- peer `reports/ReviewMeasure.md` (written before measure.py existed)

Line anchors `B:` point at the baseline gate. `W:` points at the working-tree gate.

## 1. What the baseline already detects (static read, [INFERENCE] until L1 measures)

The baseline owning row `hypr.root.sources_resolve` accepts any existing path. A direct target passes `[ -e ]` (B:2420), and a glob target passes `compgen -G` (B:2422), which also matches directories. So the owning row cannot see a directory in either position.

Several non-owning rows do already turn some directory replacements red, though their wording is misleading:

| Directory placed at | Baseline row that FAILs | Wording | Overall exit |
|---|---|---|---|
| any of the 7 `~/.config/hypr/*` direct targets (monitors, input, bindings, looknfeel, autostart, ai-usage, gkeep — all in `LOCAL`, B:2450+2456) | `hypr.local.inventory` via `[ -f "$H/$x.conf" ]` (B:2466) | `missing: <name>.conf` | 1 |
| `~/.config/omarchy/current/theme/hyprland.conf` | `theme.chain.hypr_include` via `[ ! -f "$C/omarchy/current/theme/$part" ]` (W:3407) | `target missing: current/theme/hyprland.conf` | 1 |
| any of the 9 `~/.local/share/omarchy/default/hypr/*` direct targets | none (no other row reads `default/hypr` except the envs orphan grep over `$H`) | — | 0 |
| toggle glob, all matches directories (`window-no-gaps.conf` turned into a dir) | none; `hypr.toggle.no_gaps` goes PASS→NOTE "toggle absent" (B:2512/2521), and a NOTE never flips the verdict | — | 0 |
| toggle glob, one regular match plus one directory | none | — | 0 |

**Counterexample to any "baseline is blind to directory sources" narrative:** for 8 of the 17 direct targets, a directory replacement already exits 1 at baseline, through rows other than the owner. Of the 17 direct-target classes, only the 9 omarchy defaults are fully silent at baseline, as are both glob shapes. Any claim of zero overall detection is true only for the fixtures chosen.

## 2. The landed fixtures chose the silent class, and the declared caution was not exercised

- The L1 brief to MeasureBuild said the direct case replaces `ai-usage.conf`. `SCORECARD.md:474-475` also warns that "local inventory may already detect the direct-directory case".
- The landed measure instead mutates `~/.local/share/omarchy/default/hypr/windows.conf` (`measure.py` `direct_directory`). The gate selftest N9 makes the same choice (W:1193-1210 asserts `hypr.local.inventory PASS` and exactly one hypr FAIL).

Consequence: the predicted baseline `overall_failing_runs` is **0/3** [INFERENCE] rather than the 1/3 the declared claim anticipated. This is not an invented zero. For the chosen fixtures it is a real false-green, and it isolates the owning row better.

But it does move away from the brief, and the declared overlap is never measured. If L1 then reports "overall detection 0/3 → 3/3" without context, the operability gain will read as larger than the predicate change justifies.

**Classification:** a fixable reporting defect, not grounds for the judge to reject. The windows.conf choice is legitimate as long as L1 declares it before the baseline run and the overlap is printed as a control (R2 below).

## 3. Hyprland semantics: the gate is stricter than runtime by policy (source opened)

- Canonical URL: https://github.com/hyprwm/Hyprland/blob/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp#L1816-L1849
- Pinned revision: `efb50993780079460b0cbed1363e2166a2de1d9f` = tag `v0.56.2` (commit date 2026-08-05T14:13:21Z). Installed package: `hyprland 0.56.2-2` (`pacman -Q`, read-only package observation).
- Opened: 2026-10-20.
- Located quote (L1843-1845): `else if (std::filesystem::is_directory(file_status)) { Log::logger->log(Log::WARN, "source= skipping directory {}", value); continue;`
- Also observed: L1816-1819 returns the error `source= globbing error: found no match` on GLOB_NOMATCH. L1846-1848 skips other non-regular files with a WARN.
- Tier scope: A (upstream primary code). It covers legacy hyprlang `source=` handling at v0.56.2 only. It does not cover the lua config manager, and it was not exercised on the live compositor.
- Admit as review evidence for wording. This seat does not admit anything to `SOURCES.md`.
- Flip conditions: the host runs a non-0.56.x build or the lua manager, or upstream turns the directory branch into an error.

**Implication for the claim:**
- A missing direct target and a zero-match glob are Hyprland parse errors. The gate reports both as `unresolved:`, unchanged.
- Directory targets and directory glob matches are skipped silently with a WARN. The new `non-regular:` class (W:2566, W:2572) is therefore a gate fail-closed policy for content Hyprland quietly drops. It does not mirror a Hyprland error.
- For the mixed glob, the runtime result matches the clean fixture: the regular member loads and the directory is skipped. Refusing it is policy ("a non-loadable member of a declared include set is drift"), not detection of broken config.
- L1 must not word C2 as "the gate now catches config that Hyprland fails to load" for the mixed case.

**Classification:** a tradeoff the judge should accept only if it is labelled as policy. Without the label, it is false provenance.

## 4. Defects in the landed `measure.py` C2 predicate

Current credit rule: `exit == 1 and one sources_resolve row and FAIL and 'non-regular:' in detail and affected_basename in detail`.

| # | Counterexample gate (would wrongly score) | Why it scores now | Smallest fix |
|---|---|---|---|
| P1 | A gate that names **every** match of a glob as non-regular once any match is non-regular (e.g. `non-regular: …/dir.conf …/window-no-gaps.conf`) | Only a positive substring is checked. N11 has the negative assertion (W:1246-1247) but the measure does not. | Parse the `non-regular:` segment (up to ` missing:`/` extra:`) and require its whitespace-split set to equal exactly `{affected_path}`. `affected_path` is already computed but unused. |
| P2 | A gate that lists a directory under both `unresolved:` and `non-regular:` | `unresolved:` is never checked. | Require no `unresolved:` in the three scored details. This mirrors N9-N11 (W:1205, 1226, 1248). |
| P3 | A gate whose `non-regular:` clause names the glob pattern while some other clause carries the basename | Basename substring over the whole detail (`'dir.conf'`, `'windows.conf'`) | Fixed by P1 (exact display path inside the segment). |
| P4 | A gate whose diagnostic leaks the expanded temp root (src_disp removed) | Substring still matches. "Stable owning-row diagnostic" is never measured. | Build each scored case twice under different root names and require byte-identical `sources_resolve` detail; otherwise drop "stable" from the claim. |
| P5 | A collateral FAIL from another row (isolation broken) | Only inventory and toggle details are recorded, not compared. | Record the full FAIL row-id set. Require `{hypr.root.sources_resolve}` for D, G and M; expected `hypr.toggle.no_gaps` is PASS for D and M and NOTE for G. |

Not defects: the clean and order-swap controls are present and unscored. The denominator `total: 3` is a literal but matches `specs`, so derive it as `len(specs)` (same as ReviewMeasure H3). Host isolation holds: TemporaryDirectory, `--root <tree> --no-live`, revision-bound `git show`.

## 5. Missing controls that leave claimed behaviour unmeasured

- **R2 overlap control (unscored):** `~/.config/hypr/ai-usage.conf` turned into a directory. Predicted baseline: exit 1, `hypr.local.inventory FAIL missing: ai-usage.conf`, `sources_resolve PASS`. Predicted after: the same plus `sources_resolve FAIL non-regular: ~/.config/hypr/ai-usage.conf`. This makes the declared caution (`SCORECARD.md:474-475`) a measured fact, and shows the owning-row diagnostic as the only gain for that class.
- **R3 class-preservation controls (unscored, expected identical before and after):**
  - Direct missing: `windows.conf` removed. Expect `unresolved: ~/.local/share/omarchy/default/hypr/windows.conf` and no `non-regular:`.
  - Zero-match glob: empty toggles directory. Expect `unresolved: ~/.local/state/omarchy/toggles/hypr/*.conf`.
  - Without these, a gate that sends missing targets to `non-regular:` would be invisible to the measure. The gate comment at W:2535-2537 claims this class is retained.
- **R4 symlink-to-regular control (unscored):** the gate comment claims that following a file symlink yields PASS (W:2532-2533). Measure it as PASS or remove the claim. Symlinks to directories, dangling glob matches (W:2566 → `unresolved:`) and paths containing whitespace are not in the subset, so do not claim them.

## 6. Recommended rubric for L1 (fix before any baseline run)

Scored set S = {D, G, M}, built fresh by `build_fixture` from the measured revision:
- D: `~/.local/share/omarchy/default/hypr/windows.conf` is a directory.
- G: `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` is a directory and is the glob's only match.
- M: `~/.local/state/omarchy/toggles/hypr/dir.conf` is a directory beside the regular `window-no-gaps.conf`.

credit(c, rev) = 1 iff all of the following hold:
1. The fixture shape is asserted before the run (`is_dir()`, not a symlink). The G match set is {dir}. The M match set is {regular, dir}.
2. Exit is 1 and stdout carries `MADO_VERIFY: DIVERGED`.
3. There is exactly one `hypr.root.sources_resolve` row, and its status is FAIL.
4. The parsed `non-regular:` segment equals exactly {expected `~/`-display path}.
5. The detail has no `unresolved:` and no `missing:`/`extra:`.
6. The FAIL row-id set is {`hypr.root.sources_resolve`}. `hypr.toggle.no_gaps` is D PASS, G NOTE, M PASS.
7. A rebuild under a second root name yields a byte-identical `sources_resolve` detail.

Score = 10 × Σcredit / |S|, with |S| derived. Report baseline and after columns from two explicit revisions.

Printed but never scored:
- overall exits per case (predicted baseline 0/0/0 [INFERENCE])
- the R2 overlap control
- the R3 class controls
- the R4 symlink control
- the clean control and the order-swap control (N12 shape: include_graph `line 11` FAIL, sources_resolve PASS before and after)
- the round-13 four exact-set cases, kept as retention evidence

Do not fold this into the round-13 4-case score, and do not report a combined 7-case number.

Headline L1 may claim if measured: "row-owned named non-regular diagnostics on three isolated fixtures 0/3 → 3/3; overall verdict on these fixtures 0/3 → 3/3; the baseline already exits 1 for directory replacement of 8/17 direct targets through non-owning rows."

Must not claim:
- the baseline was blind to directories
- Hyprland errors on directory sources
- the mixed glob breaks config
- symlink or whitespace policy
- multi-match order stability: `LC_ALL=C` (B:80) makes compgen order deterministic [INFERENCE], but only one non-regular match per case is exercised
- any broad operability saturation

Selftest assertion growth (N9-N12) is a harm watch, not improvement: pass fraction stays 10.0 only if every assertion passes.

## 7. Harm watch observation (read-only)

Every live hyprland.conf source target resolves to a regular file under `stat -L`, and the toggle glob currently matches two regular files. Predicted: `--no-live` agreement is unchanged by the new predicate [INFERENCE: predicate applied to observed shapes, gate not run]. L1 measures this once.

## 8. Minor gate notes (for GateImplement; non-blocking)

- W:2566 appends the glob token `$t` to `tmiss` once per dangling match, so several dangling matches repeat the glob in `unresolved:`. This is cosmetic and outside the subset.
- The PASS text "declared targets exist, member set exact" (W:2581) is unchanged although the criterion is now regular-file. Keeping it preserves snapshot-diff SAME. This is a tradeoff and not false, since a regular file implies the path exists.

## Verification gaps

- No runs. Every baseline and after outcome above is a static prediction from the cited lines.
- The working-tree gate and measure are uncommitted, so the anchors bind to the bytes read at review time.
- Authoring review is not non-author promotion authority.
