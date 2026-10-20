# ReviewCensus — round 13 (mado-r13-w1) — review of the hypr exact-set census

Lane: `MadoR13.ReviewCensus` (reviewer, leaf). Scope: surgical source review of the baseline census and the proposed exact-set contract. No tests, builds, lint, formatters, or selftests were run. No shared files were edited. No external sources were opened, so no source admission or rejection is claimed.

## 0. Bytes bound (sha256, read-only)

| File | Revision / bytes | Read as |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` | HEAD `7dcb785`, blob `ea798ad078f139f3…`, 3,245 L | Baseline census. Recoverable with `git show HEAD:tools/mado-verify.sh`, which is a durable reference. |
| same file | `240f509…`, 3,392 L | Mid-review snapshot. Spec heredoc hash and anchor counts checked here. |
| same file | `b6fd9e5e…`, 3,392 L | Final bytes; §2 anchors re-checked here. The gate owner edited the file concurrently, so the line numbers below are for `b6fd9e5e` unless marked as baseline. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/GateLedger.md` | `5b5eb155…` | Sibling design draft. Treated as the proposed contract. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/spec.json` | — | Seat assignments (GateImplement, ReviewCensus). |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` | `75ed934d…` | Mutation harness, read only. Its `@old` rules at header line 63 and lines 360–364 were checked. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md` (M13, line 25); `corpus/QUALITY.md` criterion 14 (line 20) | — | Governing rule: "names both missing and extra members; pin module membership where it is a claim." |
| Host `~/.config/hypr` and `~/.local/state/omarchy/toggles/hypr` | read-only | Names and counts only; no content read. |

Tools: none installed, updated, or upgraded.

## 1. Verified facts (no finding)

- Baseline `hypr.root.include_graph` compares count, then position. A count mismatch is reported without names (baseline `:2226`). A positional mismatch is reported for the first differing index only (baseline `:2228–2235`). A same-count substitution therefore already FAILs. It is positional, not set-named. The SCORECARD wording "cannot detect same-count replacement" (`SCORECARD.md` C2) is inaccurate for the source list.
- Baseline `hypr.local.inventory` was presence-only over a 12-name array (baseline `:2262–2273`). No selftest scenario planted an extra local file. The only extra file in the suite is `extra.conf` appended as a source (scenario H).
- `st_row_has` checks row id and status only; the fourth argument is a description (`mado-verify.sh:391–397`). `st_row_detail` (`:398–404`) is the detail check. Scenario B asserts ids only.
- Recorded regression anchors are intact in the derived target (`R7/R8` pairs excised, as `mado_r7_target_build` does):
  - D6 `@old` `ai-usage autostart envs xdph)`: count 1 at `b6fd9e5e`.
  - D7 `@old` `if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then`: count 1.
  - The recorded spec heredoc body hashes to `c7ee75b97c38ac8f…`, which equals `SPEC_SHA` (`mado-verify.sh` `SPEC_SHA='c7ee75b9…'`). Verified by re-deriving the body as `mado_r7_spec_write` does.
- The harness aborts the entire sweep if any `@old` is not found exactly once (`mutate-and-run.sh:63, 360–364`). A changed anchor therefore produces `MADO_REGRESSION: SETUP` for the whole case, not one killed mutant.
- Live host, read-only: 18 `source =` lines, sha prefix `ce7483f3…` (matches the round-12 erratum). 13 regular `*.conf` names. These equal the proposed 13-name expected set. The two `.bak.<epoch>` files are excluded by the `*.conf` glob. No dangling links and no non-regular `*.conf`. Predicted outcome: no live FAIL at landing. Not run.
- Current gate (`b6fd9e5e`) `§2` design, as landed:
  - `LOCAL` stays the byte-verbatim 12-name literal and `LOCAL+=(gkeep)` appends the 13th name. This preserves D6.
  - Sources: missing and extra are named on a count mismatch and on a positional mismatch. The count `if` line is preserved for D7.
  - `sources_resolve` also compares membership.
  - Row ids are unchanged.
  - Scenarios N1–N4 map 1:1 to the four SCORECARD C2 cases: N1 extra local; N2 same-count source substitution (replacement target exists); N3 missing+extra local; N4 missing gkeep.

## 2. Findings (by severity)

### F1 — MEDIUM — duplicate source lines remain count-only and untested
- Anchor: `mado-verify.sh` ~`2339–2340` (`sdiff` names only `missing:` and `extra:`), and ~`2349–2352` (row detail `"$miss$sdiff"`).
- A pure duplicate (for example a second `source = ~/.config/hypr/input.conf`) yields count 19 against 18 with no named member. The detail is `19 source lines (expected 18)`. That is the M13 shape the round exists to remove. `dup` naming was in the GateLedger contract (§2 and N3) and did not land. `grep` for `dup:` returns 0.
- No selftest scenario plants a duplicate source. Scenarios N1–N4 and H do not cover it.
- Fix: add `dup:` names (for example `printf '%s\n' "${got[@]}" | sort | uniq -d`) to `sdiff`. Add one scenario and one covering mutant. Each new clause needs a covering mutant (`gate-standing-use.md` §4).

### F2 — MEDIUM — `toggles/hypr/*.conf` membership is unpinned (undetected same-count false green)
- Anchor: EXPECT literal `~/.local/state/omarchy/toggles/hypr/*.conf` (`mado-verify.sh:2326`). `sources_resolve` treats the glob as satisfied by at least one match (`compgen -G`, ~`2367–2368`). `include_graph` compares the literal pattern.
- Host measurement (names only): the glob expands to `flags.conf` and `window-no-gaps.conf`. Replacing `flags.conf` with a differently named file passes both source rows. That is an undetected same-count substitution inside the source census.
- The landed erratum (`2301–2306`) does not claim closure, which is correct. The GateLedger §6 errata draft says "M13 set-blind gap for the hypr plane closed". That wording overclaims and must not be appended as drafted.
- Recommendation: do not exact-pin toggle membership. The toggles directory is operator-written state, and exact pinning would turn the gate red on routine toggles. The gate's own omarchy-plane comment (`mado-verify.sh` ~`2786–2791` at the pre-change snapshot) treats operator-owned mutable state as NOTE, not FAIL. Keep it an explicit, named residual.

### F3 — LOW — the `*.conf` predicate silently drops some members
- Anchor: `mado-verify.sh` ~`2401–2403` (`[ -f "$x" ] && lobs+=(...)`).
- `[ -f ]` follows symlinks, excludes directories, and drops dangling links. A directory named `x.conf` or a dangling `y.conf` is neither missing nor extra, so it is invisible to an "exact" census.
- The GateLedger §4 measurement command uses `find -maxdepth 1 -type f -name '*.conf'`, which is a different predicate (it does not follow symlinks).
- Host: 0 dangling, 0 non-regular `*.conf` (measured). No live effect today.
- Fix: choose one predicate, use it in the gate and in the measurement command, and report non-regular or dangling `*.conf` as `extra:`. Add a fixture case (a dangling symlink) or document the exclusion.

### F4 — LOW — one root edit now flips two rows
- Anchors: `include_graph` FAIL at ~`2349–2352`; `sources_resolve` membership FAIL at ~`2363–2379`.
- A removed root line yields `missing:` on both rows. Row ids are unchanged, so isolation assertions in scenarios A, B, C, H, and N1–N4 still hold (they assert ids and status).
- GateLedger §2 says `sources_resolve` is "kept". That description is stale.
- Action: document the double report in the row text and in the standing-use note. The snapshot diff will show both rows moving.

### F5 — LOW — the GateLedger draft is superseded and must not be used as spec of record
- Its N-matrix (N1–N10, with N3 dup and N4 swap) is not the landed set (N1–N4 above). Its "root lines 1 and 2" wording is ambiguous: fixture lines 1–3 are comments, so the first source statements are at fixture lines 4–5.
- Its §6 errata drafts need rewording (F2). Its §5 claim that PIN moves is correct.

### F6 — LOW — the C2 score is not measured, and its baseline claim needs a rubric
- SCORECARD C2 defines four cases and a score of `10 × detected/4`, with "named missing and extra" as the detection criterion. The landed scenarios map 1:1 to those four cases.
- The baseline column is code-read inference only (GateLedger §7 says so). By code read of `HEAD` blob `ea798ad0…`, under a strict rubric (both `missing` and `extra` named): N1 undetected (PASS `12/12`); N3 names `missing` only; N2 positional only; N4 names an unresolved target but no `missing` token. That is 0/4 strict, at most 1/4 lenient.
- Measurement must be a red run on the `HEAD` blob in a scratch copy. That is for L1, not this lane. Record the rubric before measuring.

### F7 — LOW — policy decision not recorded: operator-added `*.conf` now means DIVERGED
- Any new operator-authored `~/.config/hypr/*.conf` turns the gate red. QUALITY criterion 14 and the spec support FAIL.
- Precedent in the same gate points the other way: operator-owned mutable state is NOTE (the omarchy plane comment, ~`2786–2791`). The two precedents are inconsistent unless the choice is recorded.
- Recommendation: keep FAIL (it matches the spec and criterion 14). Record in `gate-standing-use.md` that routine operator conf additions trigger DIVERGED and require an appended erratum plus a re-pin.

### F8 — INFO — regression re-cut is owed and expected; anchors are safe at `b6fd9e5e`
- `PIN_MADO` is still `538d178b…` (line ~`1392`). Any edit outside the excised pairs moves the derived target, so `--regression` reads SETUP until L1 recuts. This is documented (`REGRESSION_RECUT`).
- The earlier comment (the 3,391-line snapshot) said `SPEC_SHA` is re-cut. At `b6fd9e5e` it is unchanged (`c7ee75b9…`), and the comment at ~`2304` says so. Make sure no stale re-cut claim remains before L1 relies on it.
- Keep these two anchors verbatim in any future edit. Changing D6 or D7 `@old` text makes the whole regression SETUP. Changing `SPEC_SHA` or the spec heredoc is a provenance change and needs explicit approval, not a silent edit.

## 3. Not a finding (checked, no action)

- Stale `12 active local confs` header and comments were removed at `b6fd9e5e`. The round-12 erratum (`2292–2300`) is historical and correct.
- Live host state is set-equal to the proposed expectation (see §1).
- `LOCAL` now includes `gkeep` and fixture A has it, so the clean control stays PASS.

## 4. Residual risk and verification gaps

- Nothing was run (per assignment). Baseline outcomes are code-read, not measured (F6).
- The gate changed three times during this review (`ea798ad0` → `c2f0de32` → `240f5091` → `b6fd9e5e`). Findings are bound to the bytes named in §0 and anchor lines may move.
- Operator intent on `gkeep.conf` remains open (GateLedger §7).
- Toggle membership (F2) and non-regular or dangling `*.conf` (F3) are unmeasured residuals.

## 5. Checks for the main agent after all seats land (named, not run here)

1. `sha256sum tools/mado-verify.sh`; `wc -l tools/mado-verify.sh`. Record the sha.
2. `bash tools/mado-verify.sh --selftest` and `bash tools/mado-verify.sh --no-live`. Expect `hypr.local.inventory PASS "13/13 active local confs, set exact"`.
3. `bash tools/mado-verify.sh --regression`. Expect SETUP with `REGRESSION_RECUT` (PIN owed). Then run the printed recut, update `PIN_MADO` and `TABLE_MADO` from the measured table only, and re-run.
4. Measure the C2 baseline by red run on `git show HEAD:tools/mado-verify.sh` in scratch, against the N1–N4 cases, under the rubric fixed before measurement (F6).
5. Confirm F1 (dup) and F3 (predicate) are either fixed with covering mutants or recorded as named residuals.
