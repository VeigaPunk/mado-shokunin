# ReviewResolver — round 14 / w1 (U5 boundaries, regular-source targets)

Reviewer: `MadoR14.ReviewResolver` (leaf; no dispatch, no checks run, no writes beyond this report and its rendered copy).

## Bound bytes

Pass 1 (pre-edit, baseline):
- sha256 `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569`, git blob `656f1918…`, HEAD `873ff081`, clean.

Pass 2 (landed diff, this review):
- `tools/mado-verify.sh` sha256 `0a2bf860e7134b849b8a75fefccc95d32b8a7e0391650e9fd3ada4bb6c486948`, git blob `06d1e161eb833009d727b53d73dd82e57df7c502`, HEAD `873ff081`, worktree modified (`162 insertions, 11 deletions`).
- Diff read with `git diff HEAD -- tools/mado-verify.sh`. Line references below are to the new bytes.

External sources: none. Tools installed or updated: none.

## Pass 2 — landed diff against F1–F11

| ID | Finding | Status | Evidence (new bytes) |
|---|---|---|---|
| F1 | Direct `-e` accepted directories | **Closed** | Direct branch `[ -f "$x" ]` continue; `-e` only classifies `non-regular:` vs `unresolved:` (≈2570–2574) |
| F2 | Mixed glob must FAIL on any non-regular match | **Closed** | Every match tested with `[ -f "$m" ]`; each non-regular match named by `src_disp` (≈2555–2567); N11 covers the mixed case |
| F3 | All-directory glob fixture collateral | **Closed** | N10 asserts `hypr.toggle.no_gaps NOTE` (≈1213–1234) |
| F4 | Direct-directory target leaked into other rows | **Closed** | N9 targets `default/hypr/windows.conf`; asserts include_graph PASS, local inventory PASS, exactly one hypr FAIL |
| F5 | Distinct token, `~`-form names | **Closed, token spelling parent-mandated** | Token is `non-regular:` (hyphen), not `nonregular:`; `unresolved:` retained for missing/dangling/zero-match; names via `src_disp` (≈222–229) → `~/%q` |
| F6 | Whitespace paths | **Closed** | `mapfile -t gmatch < <(compgen -G …)` (no word splitting); `%q` escaping in `src_disp` |
| F7 | Symlink policy | **Closed, documented** | `-f` follows links; link→file accepted; link→directory `non-regular:`; dangling direct/glob → `unresolved:` (≈2560 `[ -L ] && [ ! -e ]`); policy stated in comment (≈2530–2538) |
| F8 | Glob detection on full `$x` incl. `$ROOT`; unescaped `$ROOT` into `compgen` | **Not applied (carry)** | Detection still `case "$x" in *'*'*)` and `compgen -G "$x"` (≈2549–2552). Low; see R1 |
| F9 | Glob detection only `*` | **Not applied (carry)** | Same case pattern. Low; no EXPECT entry uses `?`/`[` |
| F10 | R10 red / SETUP until L1 recut | **Acknowledged** | `PIN_MADO` untouched; re-cut note present; R10 (inside R7-SELFTEST block) compares derived target to pin |
| F11 | Order-swap fixture | **Closed** | N12 swaps monitors/input (file lines 14/15), asserts include_graph FAIL naming `line 11`, sources_resolve PASS, theme line-13 anchor PASS, exactly one hypr FAIL |

Also confirmed:
- Set checks (`missing:` / `extra:`) and order walk are unchanged.
- The resolver is read-only: `compgen`, `-f`, `-e`, `-L`, `mapfile`, `src_disp`. No writes.
- N9–N12 (1184–1280) sit outside the R7-SELFTEST block (434–613) and outside the R8 block (1281–1444). They are inside the target derivation, so the pin moves as the re-cut note says.
- Selftest has no global case-count assertion. The footer is `$n_pass/$n_pass`, so the added cases do not break a fixed total.
- `set -u` only (line 79); no `set -e`. A non-matching `compgen` (exit 1) does not abort the verdict.

## Residual findings from pass 2

**R1 — Low (carry of F8/F9).** Glob detection and `compgen` still operate on the ROOT-prefixed `$x`. A root containing `*`, `[` or `?` misroutes or mismatches. Mktemp fixture roots are safe. Fix: detect on `$t`, escape `$ROOT` before `compgen`.

**R2 — Low (new).** A glob with several dangling matches appends the declared `$t` to `tmiss` once per match (`tmiss="$tmiss $t"` inside the `for m` loop), so the `unresolved:` detail repeats the glob. Cosmetic. Fix: append once per glob, e.g. with a flag.

**R3 — Note (policy).** Symlinks are followed without a containment check: a link to a regular file outside `$ROOT` is accepted. This matches the stated policy (`-f` follows links). The theme plane enforces containment; the sources plane does not. [INFERENCE] Hyprland also reads through links. Document this as a deliberate choice, or add a containment check in a later round.

No actionable defect in N9–N12 fixture logic was found. Each asserted row, token and exit code matches the new resolver's output (checked against the code, not executed).

## Verification gaps

- No checks run, per lane bounds. Shell semantics are reasoned, not executed: `compgen -G` returns directory and dangling-symlink matches [INFERENCE]; `[ -f ]` dereferences links [INFERENCE from `test(1)`].
- Expected outputs of N9–N12 were checked by reading the fixture and resolver code. They were not run.
- Hyprland's own handling of directory or glob sources is not verified upstream.
- Re-cut of `PIN_MADO`/`TABLE_MADO` is L1's job; not reviewed here.

## Actions

- Pass-1 defects delivered to `MadoR14.GateImplement` (F1–F7, F10, isolation notes).
- Pass-2 reply to `MadoR14.GateImplement`: F1–F7 and F10–F11 closed; R1–R3 carried as Low/Note.
- L1: expect R10 red and SETUP until the pin is recut (F10).

## Final source review — ef50e262… (parent request: high/medium correctness only; no checks)

Bound: `tools/mado-verify.sh` sha256 `ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b`, 3711 lines, `git status --porcelain` shows ` M` only. Read-only review; nothing run.

High: none. Medium: none.

Checked against the bytes:
- Glob transport (2652–2659): NUL-delimited output from a nullglob subshell with `IFS=` set inside it; `gsub=( $x )` does pathname expansion without word splitting, so spaces and newlines stay inside one name. Zero matches yield an empty array → `unresolved:` (2660–2661).
- Dangling-once (2664–2669): `gdang` gives one `unresolved:` token per declared glob; non-dangling non-regular matches go to `non-regular:` through `src_disp`.
- Direct branch (2672–2675): `[ -f ]` follows links; `-e` only chooses between `non-regular:` and `unresolved:`.
- Exact helper `st_row_exact` (424–429): equality on the row detail after three fields; argument order matches its call sites.
- Fixtures N4 (1153), N9–N11 (1214, 1238, 1258), N13–N16 (1309–1364): each expected string matches the code path traced for that fixture. Traced, not run.
- Mutation anchors 2664 / 2673 / 2686 point at the glob guard, direct guard and `unresolved:` label in these bytes.

Correction to the GateImplement note: the N16 boundary-hash caveat does not apply. `boundary_hash` covers only `C="$ROOT/.config"` (3668), and the N16 file lives under `.local/state/omarchy/toggles/`, outside that scope. The boundary proof neither reads nor skips it. I could not locate a source for the reported `sha256sum` stderr on the gate path; left unverified.

Latent, Low, outside the high/medium scope: `boundary_hash` (237–245) feeds `find` output through `while read -r f`, so a newline-named file under `.config` would be split into two names and its hash silently omitted. Equality still holds, so no false DIVERGED; the proof is blind to such a file. No fixture exercises it.

Carried: F8/F9 (Low), R3 (note), R10 red until L1 recut.
