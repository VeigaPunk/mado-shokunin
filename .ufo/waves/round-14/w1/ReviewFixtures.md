# ReviewFixtures — mado-verify.sh fixture builder and selftest (mado-r14-w1)

Scope: read-only review of `tools/mado-verify.sh` fixture builder (`build_fixture`, lines 236–377), selftest scenarios (lines 379–1344), and the source resolver (`hypr.root.include_graph` / `hypr.root.sources_resolve`, lines ~2352–2442). Nothing was executed; no file was edited. Installs/upgrades in this lane: none.

## Findings by severity

### F1 (high, C2 operability) — `sources_resolve` accepts directory-shaped targets
- `verify()` line ~2420: direct targets pass on `[ -e "$x" ]`, which is true for a directory.
- Lines ~2421–2423: glob targets pass on `compgen -G "$x"`, which matches directories as well as files.
- Consequence: `source = ~/.config/hypr/gkeep.conf` where `gkeep.conf/` is a directory reads PASS "declared targets exist, member set exact". Hyprland would not load that source as a config file.
- Inconsistent with the census in the same plane: `hypr.local.inventory` (lines 2466, 2460) already uses `[ -f ]` and documents "directories are not loadable confs". The resolver should use the same rule.
- No selftest covers a directory-shaped direct or glob target (grep of selftest scenarios A–N, S, R, OM, T finds none).

Proposed resolver change (for GateImplement; not applied):
```bash
    local ndir=""
    for t in "${EXPECT[@]}"; do
      case "$t" in '~'*) x="$ROOT${t#\~}" ;; *) x="$t" ;; esac
      if [ -f "$x" ]; then continue; fi
      if [ -e "$x" ]; then ndir="$ndir $t"; continue; fi        # directory-shaped direct target
      case "$x" in
        *'*'*)
          local m reg=0 any=0
          for m in $x; do                                       # unquoted on purpose: glob expansion
            [ -e "$m" ] || continue
            any=1
            [ -f "$m" ] && reg=1
          done
          if [ "$reg" = 1 ]; then continue; fi
          if [ "$any" = 1 ]; then ndir="$ndir $t"; continue; fi  # glob matches only non-regular paths
          ;;
      esac
      tmiss="$tmiss $t"
    done
```
(Declare `local m reg any` once before the loop to keep `set -u` clean and avoid redeclaration inside the loop.)
Then extend the detail assembly:
```bash
      [ -n "$ndir" ] && tdetail="${tdetail:+$tdetail }nonregular:$ndir"
```
Keep the `unresolved:` token for absent targets and add a separate `nonregular:` token so existing assertions (N2 `st_not_has "unresolved:"`) keep their meaning. The PASS detail "declared targets exist, member set exact" becomes inaccurate; if it changes, update the A assertion at line ~932 in the same edit.

### F2 (medium, coverage) — no isolated source-order negative fixture
- The positional walk in `include_graph` (lines 2391–2396) is the only order check. No selftest swaps two source lines; N2 changes the set, T3 moves a line number, and N4/N7/N8 change membership or conditionals. The order failure path is therefore unexercised.
- Per the spec, this is a negative-fixture addition only. It must not be reported as an improvement: the order path already works; the fixture pins it.

Recommended isolated swap: `monitors.conf` (index 10, file line 14) and `input.conf` (index 11, file line 15) in `~/.config/hypr/hyprland.conf`. Both targets exist in the fixture and both are regular files. The swap keeps the set, every target, and the theme include at line 13 (the `theme.chain.hypr_include` anchor). Only the positional walk should fail.

Proposed case (insert after N8, line ~1169, outside every MADO marker pair):
```bash
  # N10: source ORDER only — two declared lines swapped; set, targets and the
  # line-13 theme anchor are untouched. Only the positional walk can fail.
  local NO="$NX/order-swap"
  mkdir -p "$NO"
  cp -a "$A/." "$NO/"
  sed -i '/^source = ~\/.config\/hypr\/monitors.conf$/{N;s/\(.*\)\n\(.*\)/\2\n\1/}' \
    "$NO/.config/hypr/hyprland.conf"
  n_out=$("$BASH_BIN" "$0" --root "$NO" --no-live 2>&1); n_rc=$?
  st_eq  "N10: exit 1 (order-only source swap)" 1 "$n_rc"
  st_row_detail "$n_out" hypr.root.include_graph FAIL \
    "line 11: got '~/.config/hypr/input.conf' want '~/.config/hypr/monitors.conf'" \
    "N10: the first out-of-order position is named"
  st_not_has "N10: no set-level extra or missing member" "$n_out" "extra: "
  st_row_has "$n_out" hypr.root.sources_resolve PASS "N10 (isolation: set and targets unchanged)"
  st_row_has "$n_out" hypr.local.inventory PASS "N10 (isolation: local set untouched)"
  st_row_has "$n_out" theme.chain.hypr_include PASS "N10 (isolation: line-13 anchor held)"
  st_counts_agree "$n_out" "N10: counts agree with rows"
```
Caveat: the `st_not_has "extra: "` line assumes no other row prints that token; GateImplement should confirm with a grep. Verify the sed on the copied fixture before relying on it. Do not run the selftest in this lane.

### F3 (medium, coverage) — directory-shaped targets have no negative fixture
Two cases needed, both isolating the resolver row:

- **N9 (direct):** replace the declared `gkeep.conf` file with a directory of the same name.
  ```bash
  local N9R="$NX/dir-direct"; mkdir -p "$N9R"; cp -a "$A/." "$N9R/"
  rm -f "$N9R/.config/hypr/gkeep.conf"; mkdir "$N9R/.config/hypr/gkeep.conf"
  ```
  Expected after F1: exit 1; `hypr.root.sources_resolve` FAIL with `nonregular: ~/.config/hypr/gkeep.conf`; `hypr.root.include_graph` PASS (order and set unchanged); `hypr.local.inventory` FAIL `missing: gkeep.conf` (the directory is outside the regular-file census, so it reads as missing — the same behaviour as N4). Before F1 the resolver reads PASS: this case is red until the fix lands, which is the intended negative.

- **N11 (glob):** the only match of `~/.local/state/omarchy/toggles/hypr/*.conf` is `window-no-gaps.conf`. Make it a directory:
  ```bash
  local N11R="$NX/dir-glob"; mkdir -p "$N11R"; cp -a "$A/." "$N11R/"
  rm -f "$N11R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  mkdir "$N11R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  ```
  Expected after F1: `hypr.root.sources_resolve` FAIL with `nonregular: ~/.local/state/omarchy/toggles/hypr/*.conf`; `hypr.root.include_graph` PASS. Side effect to assert explicitly: this same file is read by the no-gaps toggle row (line ~2511, `tog` check), so that row's outcome changes too. GateImplement must read lines ~2511–2525 and name that row's expected status in the case; it must not be left as an unexamined side effect.

Both directory cases sit outside the MADO-R7/R8 marker pairs (see F4).

### F4 (process, must be carried to L1) — derived regression target moves
- The header rule (lines 1370–1373, 1407–1416) says any edit outside the marked pairs moves the derived target and owes a re-cut by L1: PIN_MADO and TABLE_MADO are re-measured, never edited to match reality.
- The F1 resolver change (verify(), ~2404–2437) and the N9–N11/N10 selftest additions (~1056–1169) sit outside `MADO-R7-SELFTEST-BLOCK` (420–599) and before `MADO-R8-BLOCK` (1170). Both move the derived target.
- Do not place these cases inside the R8 pair to avoid the re-cut: that pair is excised by `mado_r7_target_build`, so a fixture placed there would dodge the pin rule. Report the re-cut owed instead.
- Until L1 re-cuts, `--regression` reads SETUP (exit 2), as the header states. That is the honest state.

### F5 (informational) — no new cases exist yet
- Searched `tools/mado-verify.sh` for U5 / output-management / colour scenarios and for directory- or order-shaped fixtures. None exist. The only colour-adjacent fixtures are the terminal theme includes written by `build_fixture` (alacritty, foot, kitty, ghostty at lines 349–376), read by the terminal rows at ~2638–2672. Those rows check size and padding, not output-management or colour boundaries.
- Nothing to inspect for "new cases when present". The findings above are proposals; the GateImplement seat owns the edit.

## Coverage and operability judgement
- Coverage (this lane): the source-order path is currently unexercised (F2); the directory-target path is unexercised and wrongly passing (F1/F3). Proposed N9–N11 cover both. No U5 output-management or colour boundary is added by this lane (F5); that work sits with other seats.
- Operability: F1's fix uses the existing `[ -f ]` rule and separate `nonregular:` token, so owning-row diagnostics stay stable. The `unresolved:` token and N2/N4 assertions keep their meaning.

## Verification gaps (explicit)
- No selftest was run, by instruction. The sed in N10, the glob loop in F1, and the N11 side effect on the toggle row are unverified; each must be checked by the main agent's single L1 run.
- Line numbers are from reads of the current file; they will shift after the GateImplement edit.

## Tooling
- No tools installed or upgraded in this lane.
