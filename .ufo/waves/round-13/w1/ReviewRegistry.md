# ReviewRegistry — mado-verify gate registry: census, draft fields, code-2 mode classification

Seat: `MadoR13.ReviewRegistry` (reviewer, leaf). Date of reads: 2026-10-20. Read-only; no build, test, lint, format, or gate run. No shared file edited.

## 0. Anchors and revisions

| Surface | Absolute path | Revision / identity | Note |
|---|---|---|---|
| Gate | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` | HEAD `7dcb785`, blob sha256 `ea798ad078f139f3…` (3,245 L) | All line anchors below are HEAD. The working copy is being edited in flight by GateImplement (sha256 `3fb2a695…` at read time); re-anchor after that lands. |
| Lane SKILL (registry home) | `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md` | HEAD, sha256 `9cf72a93…` | Unmodified in tree. |
| Lane scorecard | `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md` | working tree modified (round-13 wave edits, not mine) | Cited for the open registry item only. |
| Fleet protocol | `/home/vgpnk/Projects/shokunin/PROTOCOL.md` | last touched by `7c5b34f`; working tree clean | §Gate standard at :375-424, Registry bullet at :398-406. Cite by heading, not line. |
| Standing-use note | `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` | committed | §1 mode table, §5 maintenance rules. |
| Harness (mutable fleet artifact) | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` | tameshi HEAD `8742f5d`; file last changed by `606716f` | Read-only consumer. |
| Sibling convention | `/home/vgpnk/Projects/shokunin/kumitate-shokunin/SKILL.md:587`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:1705`, `/home/vgpnk/Projects/shokunin/souji-shokunin/SKILL.md:102` | committed | Format precedent only. |

## 1. Existing SKILL absence — census (run 2026-10-20)

| Command (cwd `mado-shokunin`) | Output | Reading |
|---|---|---|
| `grep -c '^## Gate registry' SKILL.md` | `0` | No registry heading. |
| `grep -cE '^\| *[a-z0-9-]+ *\| *(gate\|probe) *\|' SKILL.md` | `0` | No gate or probe row. |
| `grep -ci registry SKILL.md` | `1` (line 20: "tiered registry" = `corpus/SOURCES.md`) | Not a gate registry. |
| `grep -c 'mado-verify' SKILL.md` | `50` | Usage prose exists, no registry row. |
| `grep -n 'registry home' SCORECARD.md` | `:322` "gate registry row at `SKILL.md` (registry home, `PROTOCOL.md` §Gate standard)"; `:347` "Register the existing verdict instrument at its SKILL registry home." | Open item in the round-13 scorecard. |

Conclusion: the gate has no registry row at its registry home. Under PROTOCOL.md §Gate standard, Delivery (`:418-421`), closure "grades no gate conformant until its registry row exists at the lane's *registry home*."

Registry home is `SKILL.md`. PROTOCOL.md:398 says "a child lane's *registry home* is its own `SKILL.md`." The main-repo exception (`SCORECARD.md`) at :399-401 covers only `protocol` and `aggregator`, so it does not apply to mado.

Placement recommendation: a new top-level `## Gate registry` section, heading form from kumitate `SKILL.md:587`. Insert before `## Evidence trail & sources` (SKILL.md:399). Do not place it inside a `## Round-N` append, because append sections are historical.

Code-2 interpretation: "code2" is read as exit code 2 classified per mode. `grep -ri code2` over mado `SKILL.md`, `SCORECARD.md`, `LOG.md`, `tools/`, `corpus/`, `plans/` returns no hit; the token is not used in this tree.

## 2. Exact missing fields — draft registry rows

The eight PROTOCOL.md §Gate standard Registry fields are: name, `gate|probe`, entry command, verdict map (code → class), self-test command and spelling, pinned-value path, write scope, owner. The gate has three entry modes with different exit meanings, so one row per entry is drafted. Protocol fields are unchanged; notes follow the table.

```markdown
## Gate registry

Registry home per PROTOCOL.md §Gate standard (Registry). Verdict vocabulary: `0` clean · `1` failed · `2` could-not-evaluate; any other exit code is could-not-evaluate. Pinned values live in the script, not here. Frozen counts are not pinned in this section.

| name | gate/probe | entry command | verdict map (code → class) | self-test command and spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-verify | gate | `bash tools/mado-verify.sh [--no-live\|--live] [--root DIR]` (env `MADO_VERIFY_ROOT`, `MADO_VERIFY_LIVE=auto\|yes\|no`); `--snapshot FILE` wraps this mode, exit = run verdict | 0 → clean (`MADO_VERIFY: CLEAN`) · 1 → failed (`MADO_VERIFY: DIVERGED`: a FAIL, or a required plane UNKNOWN; the counts line separates them) · 2 → could-not-evaluate (usage error; `--snapshot` refusal) · other → could-not-evaluate | `bash tools/mado-verify.sh --selftest`; spelling `--selftest` (function `selftest()`); green `MADO_SELFTEST: N/N assertions passed` rc 0; red `MADO_SELFTEST: FAILED` rc 2 | in `tools/mado-verify.sh`: `EXPECT` and `LOCAL` arrays (`verify()`), `OMARCHY_*_PIN` (omarchy plane), theme pins (`theme_plane()`) | none on live, `--no-live`, `--root`; `--selftest` writes only `/tmp/w5-mado-m52-selftest.*`; `--snapshot FILE` writes FILE only | mado-shokunin lane |
| mado-verify-regression | gate | `bash tools/mado-verify.sh --regression [--keep]` | 0 → clean (`MADO_REGRESSION: PASS`) · 1 → failed (`MADO_REGRESSION: FAIL`: measured kill table ≠ `TABLE_MADO`) · 2 → could-not-evaluate (`MADO_REGRESSION: SETUP`: missing tool, harness not found, spec or target sha ≠ pin, sweep refusal; or usage error) · other → could-not-evaluate | `bash tools/mado-verify.sh --selftest` (scenarios R1–R13, stub runner) | `PIN_MADO`, `SPEC_SHA`, `TABLE_MADO` in `tools/mado-verify.sh`; recorded spec in `mado_r7_spec_write()`; `HARNESS_SHA_RECORDED` is provenance only | `mktemp -d /tmp/mado-verify-regression.*`, removed on PASS, kept on FAIL/SETUP and with `--keep`; removes only `/tmp/w5-mado-m52-selftest.*` dirs named by its own run | mado-shokunin lane |
| mado-verify-snapshot-diff | gate | `bash tools/mado-verify.sh --snapshot-diff OLD NEW` (v1 receipts) | 0 → clean (`MADO_DIFF: SAME` or `DETAIL-CHANGED`) · 1 → failed (`MADO_DIFF: CHANGED`: a row class or scope field moved; a comparison result) · 2 → could-not-evaluate (`MADO_DIFF: SETUP`: missing, non-v1, or tampered receipt; usage) · other → could-not-evaluate | `bash tools/mado-verify.sh --selftest` (scenarios S1–S10) | none; v1 magic line `# mado-verify snapshot v1` in `mado_r8_load()` | none; reads two files only | mado-shokunin lane |

Mutable fleet dependency (regression row): `tameshi-shokunin/tools/mutate-and-run.sh`, resolved as `$MADO_R7_FLEET/tameshi-shokunin/tools/mutate-and-run.sh` or `MADO_VERIFY_HARNESS`. It is a sibling file that moves; the gate prints its sha as provenance and does not compare it. Named gap, see finding F2.
```

Field notes:

- The row set is per entry, not per file. A single file-level row would hide `2` meaning three different things (section 3).
- `kind` for snapshot-diff is `gate` because exit 1 is reachable. Reading CHANGED as "failed" is a lane judgment, and the row says so.
- Do not register frozen counts. The `--selftest` count changes whenever scenarios change (SKILL.md records 268 at HEAD, `:1488`). The expected values stay in the script, which satisfies "committed in the owning repo".

## 3. Mode classification of exit codes (code 2 is mode-sensitive)

Exit codes are read from HEAD `ea798ad0`. Helper-level `sys.exit(3/4/5)` calls inside the embedded Python heredocs are not traced here; see the verification gaps in the report.

| Mode | 0 | 1 | 2 — meaning | Class of 2 | Anchors (HEAD) |
|---|---|---|---|---|---|
| verify (default, `--no-live`, `--live`, `--root`) | CLEAN | DIVERGED: FAIL, or required plane UNKNOWN | usage error only: unknown argument, `--root` without dir, invalid `MADO_VERIFY_LIVE`. Never a verdict. | could-not-evaluate | header `:12-13`; main case `:3176-3182`; live switch `:3193-3199`; exits `:3239`, `:3246` |
| `--selftest` | all assertions pass (`MADO_SELFTEST: N/N`) | not produced | failing suite (`MADO_SELFTEST: FAILED`). Capability not established. | could-not-evaluate (not failed) | `:1211-1217`; scenario F asserts exit 2 at `:1007` |
| `--regression` | PASS | FAIL (table differs) | SETUP (tool/harness/spec/target/pin/sweep) or usage | could-not-evaluate | exit map `:1290-1291`; `run_regression()` `:1498`; harness path `:1508-1511`; `:1520-1521` provenance |
| `--snapshot FILE` (wrapper) | the run's verdict passes through | the run's verdict passes through | refusal: destination exists, inside `<root>/.config`, run exit outside 0/1, reconcile or write failure; or usage | could-not-evaluate | `:1765` REFUSED; doc `mado_r8_usage_note()` `:1711`; refusals `:1759-1766`, `:1802-1806` |
| `--snapshot-diff OLD NEW` | SAME or DETAIL-CHANGED | CHANGED | SETUP (missing, non-v1, tampered receipt) or usage | could-not-evaluate | `:2062-2063` SETUP `return 2`; `:2154`, `:2158` exit; `:1667-1670` doc |
| `--help` / `-h` | 0 | not used | not used | none (not a verdict) | `usage()` `:85-98`; mode helps at `:1605`, `:1739`, `:1755`, `:2029` |

Judgment calls for the lane:

- A red `--selftest` is `2`, not `1`. A reader who maps `2` to "usage" would miss that it is a failed capability test. The row must say "red self-test → could-not-evaluate".
- Verify-mode `1` covers both FAIL and UNKNOWN. The fleet fixes `1` as failed, so this is protocol-conformant, but an environment-blocked run reads as failed. The row's counts-line note is required, not optional.
- Verify mode never exits `0` while any row is UNKNOWN. Scenario C at `:958-972` is the regression point for that clause.

## 4. Findings (severity-ordered; detail in the report)

- **F1 High, closure defect.** No gate registry row at the registry home. Evidence: section 1 census. Fix: insert section 2 into `SKILL.md`. No code change needed.
- **F2 High, revision naming and mutable dependency.** The regression mode's harness is a sibling file whose sha has changed. Evidence: `git show <rev>:tools/mutate-and-run.sh | sha256sum` for each commit that touched it (section 5). Current sha `75ed934d…`. Recorded `HARNESS_SHA_RECORDED` `b56c6e57…` (commit `4494715`). Standing-use note §5 item 5 says "sha `cf41efaa…242c75` today, unchanged since the round-8 freeze" (commit `9f1d3c3`), which a later commit superseded. Fix: the row names the dependency and its current sha, and the regression line is read against that sha.
- **F3 Medium, verdict revision naming.** A plain verify verdict does not name the gate revision. `VERSION_STR` at `:77` is `mado-verify.sh v1 (mado-shokunin round 5 / M5-2)` with no sha. The revision appears only in snapshot receipts (`# gate-sha256`) and the `REGRESSION_TOOL` line. PROTOCOL.md:393 says "A verdict names the revision it was measured against". Fix: the row points to the snapshot receipt as the revision-bearing route. Do not change `VERSION_STR`. Standing-use §5 item 7 says it is load-bearing for the pin.
- **F4 Medium, mode-sensitive exit 2.** Four modes give `2` four meanings (section 3). Fix: the per-mode rows in section 2.
- **F5 Low, UNKNOWN collapses to 1.** Verify-mode `1` covers unverifiable planes (section 3). Fix: counts-line note in the row.
- **F6 Medium, stale protocol anchors.** Lane docs cite PROTOCOL.md at `:328-358`, `:360-408`, `:382-385`. At the current fleet tree, §Evidence is at `:343-373`, §Gate standard at `:375-424`, Registry at `:398-406`. Fix: the registry section cites by heading.
- **F7 Info, pin coupling.** `PIN_MADO` (`:1293`) hashes the gate with the R7 and R8 marker blocks excised (standing-use §5 item 6). Any edit outside those blocks, including the in-flight census change in `verify()` at `:2168`, moves the pin, so `--regression` reads SETUP until re-cut (standing-use §5 item 2). The row must say the pinned-value path includes the whole file.

## 5. Source opens (local; admission and flip)

| # | Source (absolute path) | Revision | Tier | Exact quote (≤25 words) | Location | Admission / rejection / flip |
|---|---|---|---|---|---|---|
| S-a | `/home/vgpnk/Projects/shokunin/PROTOCOL.md` | last touch `7c5b34f`; tree clean | A (fleet normative) | "a child lane's *registry home* is its own `SKILL.md`." | §Gate standard, Registry bullet, :398 | Admitted: sets the home (F1). |
| S-b | same | same | A | "Row fields: name, `gate\|probe`, entry command, verdict map (code → class), self-test command and spelling, pinned-value path, write scope, owner." | :401-402 | Admitted: eight fields (section 2). |
| S-c | same | same | A | "every other code a gate exits (`2`, `3`, `64`, …) is declared in its registry entry" | Verdict bullet, :380-381 | Admitted: per-mode map (section 3). |
| S-d | same | same | A | "A gate whose verdict depends on a mutable fleet artifact also ships a run over a committed input snapshot" | Two evidences bullet, :391-392 | Admitted as the clause that applies to the regression row (F2). Not invented: quoted. Whether it binds is for the lane. |
| S-e | same | same | A | "A verdict names the revision it was measured against: a gate grades the tree it runs on" | Two evidences bullet, :393 | Admitted (F3). |
| S-f | same | same | A | "closure grades no gate conformant until its registry row exists at the lane's *registry home*" | Delivery bullet, :420-421 | Admitted (F1 severity). |
| S-g | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` | HEAD `7dcb785` / `ea798ad0` | A (own gate) | "Exit map: 0 = CLEAN · 1 = DIVERGED … · 2 = tool/usage error (bad args; a failing --selftest)." | header `:12-13` | Admitted (section 3). |
| S-h | same | same | A | "(recorded revision %s — provenance, not gated)" | `run_regression()`, `:1520-1521` | Admitted (F2); this confirms the harness sha is not compared. |
| S-i | `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` | committed | A (own note) | "sha `cf41efaa…242c75` today, unchanged since the round-8 freeze" | §5 item 5 | Rejected as a current pin: superseded by commit `606716f`. Flip: harness now `75ed934d…`. |
| S-j | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` | HEAD `8742f5d` | B (sibling, read-only) | sha history: `b56c6e57…` (`4494715`), `cf41efaa…` (`9f1d3c3`), `75ed934d…` (`606716f`) | `git log -- tools/mutate-and-run.sh` | Admitted as the mutable dependency (F2). |
| S-k | `/home/vgpnk/Projects/shokunin/kumitate-shokunin/SKILL.md` | committed | B (sibling precedent) | "## Gate registry" | `:587` | Admitted as the heading form only. |

## 6. Verification gaps (for L1, not run here)

- No gate run. The exit table is static at HEAD `ea798ad0`. Re-check it against the post-GateImplement tree before the registry lands.
- Whether `--regression` PASSes against the current harness `75ed934d…` is unknown. The regression output will print the sha; record that line with the row.
- Python-helper exit codes `3/4/5` (in heredocs) are not traced to see whether they can reach the script exit. Any such path would be a sixth value outside the map.
- `EXPECT`/`LOCAL` names and anchors will move under GateImplement. The row cites symbols, so it survives; re-grep before landing.
