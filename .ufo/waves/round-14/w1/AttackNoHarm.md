# AttackNoHarm — round 14 / w1 (critic, leaf, read-only)

Axes judged: **coverage**, **operability**. Milestone: U5 boundaries and regular-source targets.
Scope: does the in-flight regular-file resolver change harm existing parser, source-order, glob
behavior, or the mutation targets? I did not execute the gate, the selftest, the mutants, or the
counter. Every kill or survival below is a prediction from reading the code `[INFERENCE]`.

## Inputs observed

| Input | Identity |
|---|---|
| Committed gate (round-13 measured) | `037b05dcd3f86e12…6569`, last commit `95cbc41f` 2026-10-20 (= `frozen/expected.json` gate input) |
| Gate under review (GateImplement working tree, mid-flight) | sha256 `0a2bf860e7134b849b8a75fefccc95d32b8a7e0391650e9fd3ada4bb6c486948`, diff +162/−11 |
| Prior residuals | `corpus/lessons/round-13-verifier-spotcheck.md:203-205` (R13-V1..V3), `SCORECARD.md:387-423` |
| Mutation specs | `.ufo/waves/round-13/covering.spec` (P1–P8), embedded D1–D9/R1 (`SPEC_SHA c7ee75b9…`), `.ufo/waves/round-14/w1/regular-target.spec` (RT1–RT2) |
| Counter | `.ufo/waves/round-14/measure.py:213-297` |
| Packages (read-only `pacman -Q`) | hyprland 0.56.2-2, bash 5.3.15-1 |
| Live target types (read-only `stat`, no content) | all 17 direct declared targets are regular files and none is a symlink at its final component; the toggle glob matches 2 regular files (follow and nofollow) |

Upstream source opened (primary, tier A):
- URL: <https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/config/legacy/ConfigManager.cpp#L1824-L1850>
- Pinned revision: `efb50993780079460b0cbed1363e2166a2de1d9f`, tag v0.56.2, commit date 2026-08-05,
  accessed 2026-10-20. This tag matches the installed package version.
- Located quote (L1843-1844): `else if (std::filesystem::is_directory(file_status)) { … "source= skipping directory {}", value); continue;`
- Scope: legacy hyprlang `source=` handling only. The Lua path (`src/config/lua/ConfigManager.cpp:150-153`)
  also keeps only `is_regular_file` matches.
- **Admit** this source as a bound on the gate's claim wording. **Flip** if a later pinned Hyprland
  makes a directory match a config error. I did not register it as an S-row (S047/S048 are reserved
  elsewhere).

## Verdict

The landed design causes **no regression** to the existing parser, the exact-set check, the order
check, or the glob behavior on any fixture or on the live host. Findings F1–F4 are fixable gauge
gaps, not harms. F5 is a wording bound. F6 is an exotic-input tradeoff.

Preserved, from reading the code:
- `hypr.root.sources_resolve` keeps its row id. The PASS text is byte-identical
  (`declared targets exist, member set exact`, :2581), so `A` :943, `N1` :1087 and `measure.py`
  still match. No row was added, so the 29-row file-plane denominator does not move.
- The `missing:`/`extra:`/`extra: ''` naming and the positional walk in include_graph are untouched.
  This covers N2, N7 and D7 (:2510).
- A dangling direct symlink and an absent direct target both still land in `unresolved:`, as before.
  A zero-match glob also stays in `unresolved:`.
- Mutation anchors still occur exactly once in the derived target: P4 at :2546, P3 at :2578, D7 at :2510
  (its second copy, :1617, sits in the excised R7 block), RT1 at :2571, RT2 at :2565.
- New cases N9–N12 (:1185-1280) sit **before** `# >>> MADO-R8-BLOCK >>>` (:1281), so they survive
  `mado_r7_target_build` and can kill RT1/RT2. RT1 should die on N9 and RT2 on N10/N11.
- `PIN_MADO`/`SPEC_SHA` are unchanged. The round-14 re-cut record (:1529-1538) correctly says R10 reads
  red until L1 re-cuts. The frozen round-13 companion uses its own `frozen/gate.sh` copy, so this edit
  does not touch it.
- Live harm: none expected. Every live target is a regular file, so the live `sources_resolve` stays
  PASS and freshness 29/29 holds `[INFERENCE from stat; not run]`.
- N12 swaps monitors/input at file lines 14/15 and keeps the theme anchor at line 13. Its comment and
  the counter both label it a preservation control, not new detection. It complies with "do not claim".

## Findings

### F1 — N11 "regular member not refused" assertion is vacuous (operability, premature saturation)
- Counterexample: an over-refusing implementation names every match of a glob once any match is
  non-regular. Under `LC_ALL=C`, `compgen -G` sorts `dir.conf` before `window-no-gaps.conf`, so the
  detail becomes `non-regular: ~/…/dir.conf ~/…/window-no-gaps.conf`. The regular sibling is never
  preceded by `non-regular: `, so `st_not_has … "non-regular: ~/…/window-no-gaps.conf"` (:1246-1247)
  still passes. Scenario A has no directory, so it cannot catch this either.
- The counter has the same blind spot. `measure.py:240-243` checks that `dir.conf` appears and never
  checks that `window-no-gaps.conf` is absent, so this bug would still score C2 3/3.
- Smallest correction:
  1. Make N11 row-scoped. Extract the `hypr.root.sources_resolve` line and assert that it does not
     contain `window-no-gaps.conf`. Alternatively, rename the directory so it sorts after the regular
     member (e.g. `zz-dir.conf`).
  2. In the measure mixed case, add `'window-no-gaps.conf' not in src_detail`.

### F2 — the `unresolved:` class for an absent direct target is unguarded (operability)
- Counterexample mutant: change :2572 `if [ -e "$x" ]` to `if true`. Every absent target then reads
  `non-regular: ~/…`. N4 (:1145) only asserts the substring `~/.config/hypr/gkeep.conf`, which the
  mutant still emits. B asserts FAIL only. No positive `unresolved:` assertion exists anywhere
  (grep: 0 hits). The mutant survives, yet the code comment (:2535-2537) claims the class is "not
  repurposed".
- Smallest correction: add one line to N4:
  `st_row_detail … sources_resolve FAIL "unresolved: ~/.config/hypr/gkeep.conf"`.

### F3 — the dangling-glob-match arm and the zero-match arm have no fixture (coverage of claims)
- Mutant A: `[ -L "$m" ] && [ ! -e "$m" ]` → `false`.
- Mutant B: the zero-match line `            tmiss="$tmiss $t"` (:2562) → `:`. This lets a zero-match glob PASS.
- Both arms are new, independently mutable copies, and no fixture removes the toggle without adding
  a replacement or adds a dangling link. Both mutants survive `[INFERENCE]`.
- Mutant B removes behavior that the old shared path held without being tested. It is not a
  regression, but the split made it separately breakable.
- Smallest correction: one fixture for each arm, or state both arms as unexercised in GateImplement's
  report and the gate comment.

### F4 — the symlink policy is unverified in both directions (calibration of claims)
- Header :40-42 and comment :2532-2534 say "a link to a file passes" and "a symlink to a directory"
  is refused.
- No fixture source target is a symlink at its final component: `current/theme` is a real directory
  (:254, :311), and the only fixture links are for mako and the background.
- The live host has none either, per the `stat` nofollow column.
- A mutant `[ -f "$x" ]` → `[ -f "$x" ] && [ ! -L "$x" ]` survives.
- Smallest correction: one positive fixture (windows.conf replaced by a symlink to a regular file,
  expecting `sources_resolve` PASS), or downgrade the wording to "policy, not exercised".
  GateImplement was asked for "exact verification" of this policy.

### F5 — wording bound: the gate is stricter than Hyprland, which never rejects these targets (false-provenance guard)
- Hyprland v0.56.2 skips directory and non-regular glob matches with a WARN, loads the regular
  siblings, and returns no error (L1843-1849). A directory therefore never reaches
  `live.hypr.configerrors`, and the file-plane row is its only owner. That is the operability value.
- Current gate text makes no false Hyprland claim. Any LOG, SCORECARD or lesson prose must say
  "refuses what Hyprland silently skips". It must not say "Hyprland rejects" or "configerrors would show it".
- Hyprland's handling of a dangling glob match goes through `std::filesystem::status(value, ec)`
  (L1828-1832). With libstdc++ I expect `ec` to be set and the call to return "inaccessible" `[INFERENCE: libstdc++ ops.cc not
  opened]`. Do not cite it as verified.

### F6 — tradeoff: compgen line-splitting on newline filenames (operability, exotic)
- A regular toggle file whose name contains `\n` makes `mapfile` produce two fragments. One is an
  absent absolute path, which gets named `non-regular` (a mislabel). The other is relative, so its
  `-f` result depends on the CWD. The old code passed this case because it only checked for a match.
- `%q` in `src_disp` keeps the detail on one line, so the snapshot rule against multi-line details holds.
- Not worth widening scope. Record it as a known limit, or treat any non-`-e`, non-`-L` fragment as
  `unresolved:` rather than `non-regular:`.

Cosmetic, not harm:
- Several dangling matches repeat the pattern in `unresolved:`.
- `unresolved:` prints the raw declared member while `non-regular:` prints it `%q`-escaped. The two
  are identical for all 18 declared members.
- include_graph's `line N` is a source ordinal, while the theme anchor counts file lines. This
  ambiguity predates the round and N12's comment states it. Do not change it (it would move asserted
  strings).

## Impacted axes
- **Operability:** F1 and F2 let a mis-classifying resolver pass both the suite and the C2 counter.
  Fix them before claiming C2 detection as measured. F6 is a bounded limit.
- **Coverage / claim calibration:** F3 and F4 are code comments that claim untested behavior.
  F5 constrains prose only.
- **No harm** to the existing parser, the source order, the exact set, glob ≥1-match semantics, the
  read-only fence, the row ids or denominators, or the mutation targets (P1–P8, D1–D9/R1 anchors
  still occur exactly once; re-cut owed as documented).

## Owner hand-off (not done here; L1 runs once)
`bash tools/mado-verify.sh --selftest`; `--no-live`; L1 re-cut; `regular-target.spec` sweep plus
the F2/F3/F4 mutants above against the derived target; `round-13/covering.spec` re-sweep (P3/P4 anchors
still occur exactly once).

Tools installed/updated: none. The read-only scratch clone `/tmp/hl-src-ahn` (sparse upstream clone) has been removed.
