# ExecXkbCompile — round 46 w1: FALLBACK predictable by compiling the declared names?

Probe run 2026-10-26 (host, Hyprland 0.56.2 `efb50993`, libxkbcommon 1.13.2, xkeyboard-config 2.48 data tree).
Full write-up and receipts: `.ufo/waves/round-46/w1/ExecXkbCompile/report.md` (+ scripts, `.txt` receipts, `probe-manifest.txt` there).
Method: `ctypes` on the host library doing exactly what `setKeymap` does — fresh `xkb_context_new(0)`,
`xkb_keymap_new_from_names2(..., XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS)`, then
`xkb_keymap_layout_get_name` per layout. No mutation; only the allowed `hyprctl devices -j` read in `verify-live.py`.

## Verdict

**Yes — the compile predicts the fallback branch, and reproduces the compositor's own layout name, but only inside a pinned environment and only with the `kb_file` short-circuit modelled.**

## Compile results (`probe-table.txt`)

- Compiles: host `br`+`compose:caps` → `Portuguese (Brazil)`; `us` and the empty default → `English (US)`;
  `br,us`+`compose:caps` → both names; `br`+variant `nodeadkeys` → `Portuguese (Brazil, no dead keys)`;
  `br,us`+`nodeadkeys` → both.
- Fails (NULL): typo layout `zz`, typo layout `brq`, `br`+variant `zzz`, **`us`+variant `nodeadkeys`** (no such variant in
  2.48, while `br` has one), uppercase layout `BR`, rules `zzz`.
- Does **not** fail: any invalid option or model tried — 0/11 option strings (`foo`, `grp:`, `:`, `a:b:c`, `notanoption:x`, …)
  and 0/6 models (`zzz`, `pc10`, `PC105`, …); both are silently ignored (`options-sweep.txt`). Compile failure is a property
  of rules/layout/variant only, so those two never cause a fallback in Hyprland either.

## Agreement with the live compositor (`live-join.txt`)

`hyprctl devices -j` prints `active_keymap` from `xkb_keymap_layout_get_name` (`Hyprland-IKeyboard.cpp:313`,
`Hyprland-HyprCtl.cpp:783`/`:794`). Recompiling each keyboard's printed rules reproduces `active_keymap` for **10 of 10**
keyboards, `active_keymap_mismatches=0` (including the virtual one, whose match is coincidence — see below).

## Agreement with Hyprland's fallback path (`predict-cases.txt`)

The fallback branch was reproduced literally: all-NULL names with `layout="us"` (`Hyprland-IKeyboard.cpp:107`,
`:113`, `:115`) compiles to `English (US)`, so after a failed compile the compositor would print
`layout='us' variant='' options='' model='' rules='' active_keymap='English (US)'`. On 15 declared-name sets the
compile verdict and the round-46 reference tool's FALLBACK rule agreed in every case (`join_vs_compile_disagreements=0`),
and the compile additionally attributes the culprit (`layout` for `zz`/`brq`/`BR`, `variant` for `br`+`zzz`/`us`+`nodeadkeys`,
`rules` for `rules=zzz`, never `options`/`model`).

Where "failing names" is wider than "the compositor fell back":

- **`kb_file` short-circuits the names.** `Hyprland-IKeyboard.cpp:87` (`if (!m_xkbFilePath.empty()) {`) tries the file at `:93`;
  the names are consulted only at `:98` (`if (!m_xkbKeymap)`). A compiling file map (`pc+br` → `Portuguese (Brazil)` via
  `xkb_keymap_new_from_string`) means a failing name set never runs — a `--xkb` mode must compile the file first.
- **Overridden keymaps ignore names.** `Hyprland-IKeyboard.cpp:61` (`if (m_keymapOverridden) {`) returns before any compile;
  `Hyprland-VirtualKeyboard.cpp:41` (`m_keymapOverridden = true;`) sets it. The host's virtual keyboard prints
  `Portuguese (Brazil)` because its client sent that map, not because its rules compiled — keep VIRTUAL ahead of any compile verdict.

## Could a `--xkb` mode turn the entry's "compile failure not observed" limit into a check?

Yes. That limit is stated at `entry.md:68` (`The XKB compile itself is not reproduced`) and `entry.md:24`
(`the compile failure itself is not observed here`). A config-only mode would (1) derive FALLBACK instead of inferring it —
`us` and the empty default compile to `English (US)` while `zz` is NULL, so "genuine us" and "declared zz" stop being
indistinguishable; (2) name the failing field, which the printed tuple erases; (3) predict before any dump exists and flag a
stale dump (printed names ≠ `us`+empty but uncompilable is impossible unless stale).

## Risks (measured here)

- **Environment is a hard dependency.** `XKB_CONFIG_ROOT` replaces the data root: pointed at an empty dir, *everything*
  fails, `us` included (`env-root-sensitivity.txt`). Three *additive* user paths prepend to the root —
  `XKB_CONFIG_EXTRA_PATH`, `$XDG_CONFIG_HOME/xkb`, `$HOME/.xkb` (`include-path-matrix.txt`) — and a one-layout `symbols/zz`
  in each makes the nonexistent `zz` compile to `Fake Shadow Layout` (`home-shadow.txt`). A mode must pin the root and
  report/refuse user trees; it cannot prove parity by reading the compositor's `/proc` env inside a pure config join.
- **Parity holds on this host today, shape-only:** the compositor's `/proc/1622/environ` is readable, has `HOME` and
  `XDG_CONFIG_HOME`, and **0** `XKB_*` names (names only, no values); default include set is the single
  `/usr/share/xkeyboard-config-2` with `~/.config/xkb`, `~/.xkb`, `/etc/xkb` not addable; `XDG_DATA_DIRS` unused.
- **stderr contract.** The library prints `xkbcommon: ERROR: [XKB-…]` on failure; the tool's contract keeps stderr empty.
  `xkb_context_set_log_level(ctx, XKB_LOG_LEVEL_CRITICAL)` + `xkb_context_set_log_fn(ctx, NULL, NULL)` keeps a failing compile
  silent — `stderr-silence.stderr` is 0 bytes while `zz` still returns NULL.
- **ABI.** `xkb_keymap_new_from_names2` is `@@V_1.11.0`; older libraries expose only `xkb_keymap_new_from_names` (no format arg).
- **Cost / determinism.** 1.17 ms per compile (200 compiles, `options-sweep.txt`); the 17-compile probe table is 0.051-0.054 s
  wall incl. startup; three runs identical (`timing-determinism.txt`).
- **Still invisible:** a runtime `hyprctl keyword`; a `kb_file` readable by the compositor but not the probe; a compositor
  started with a different `XKB_CONFIG_ROOT`.

Nothing installed; no scratch retained (`/fast/scratch/hyaku/mado-r46/ExecXkbCompile` removed); no tracked file edited.
