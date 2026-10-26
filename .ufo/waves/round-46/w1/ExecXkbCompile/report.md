# ExecXkbCompile — round 46 w1: can a read-only tool predict FALLBACK by compiling the declared names?

Probe run 2026-10-26 on the host, Hyprland 0.56.2 (`efb50993`), libxkbcommon 1.13.2 (`/usr/lib/libxkbcommon.so.0.13.2`),
xkeyboard-config 2.48-1 (as registered; the data tree probed is `/usr/share/xkeyboard-config-2`, the single include path
libxkbcommon reports).
Method: `ctypes` on the host library, the same call Hyprland makes — fresh `xkb_context_new(0)`, `xkb_keymap_new_from_names2`
with `XKB_KEYMAP_FORMAT_TEXT_V2` and `XKB_KEYMAP_COMPILE_NO_FLAGS`, then `xkb_keymap_layout_get_name` per layout.
Nothing was mutated, no compositor command beyond the allowed reads, no process started by the probe itself
(the two `hyprctl devices -j` reads in `verify-live.py` are the allowed dump read).

## Verdict

**Yes, with two hard conditions.** A compile-based mode reproduces the compositor's own layout name exactly
(10 of 10 keyboards, including the virtual one, `live-join.txt`), and it predicts the fallback branch for every
failing name set tried (`predict-cases.txt`, 15 cases, 0 disagreements with the printed-name join). It is not a
drop-in replacement: it is **environment-relative** (`XKB_CONFIG_ROOT` is authoritative, not additive —
`env-root-sensitivity.txt`) and it must model the `kb_file` short-circuit, or it will predict a fallback the
compositor never took (`Hyprland-IKeyboard.cpp:87`, `:98`).

## What the probe answers

### 1. Which declared names compile, and the layout name each yields (`probe-table.txt`)

| declared (rules, model, layout, variant, options) | compile | layout names |
|---|---|---|
| host `"" "" br "" compose:caps` | yes | `Portuguese (Brazil)` |
| `us` | yes | `English (US)` |
| defaults (`""` layout) | yes | `English (US)` |
| `br,us` + `compose:caps` | yes | `Portuguese (Brazil)`, `English (US)` |
| `br` + variant `nodeadkeys` | yes | `Portuguese (Brazil, no dead keys)` |
| `br,us` + variant `nodeadkeys` | yes | `Portuguese (Brazil, no dead keys)`, `English (US)` |
| typo layout `zz` | **NULL** | — |
| typo layout `brq` | **NULL** | — |
| `br` + variant `zzz` | **NULL** | — |
| `us` + variant `nodeadkeys` | **NULL** | — (us has no `nodeadkeys` in 2.48; `br` and `br,us` do) |
| layout `BR` (uppercase) | **NULL** | — (names are case-sensitive) |
| rules `zzz` | **NULL** | — |
| option `notanoption:x` | yes | `Portuguese (Brazil)` — silently ignored (`XKB-595`) |
| `compose:caps,notanoption:x` | yes | `Portuguese (Brazil)` |
| model `zzz` | yes | `Portuguese (Brazil)` — silently ignored |

So compile failure is a property of **rules, layout and variant only**: a sweep of 11 malformed or unknown option
strings (`foo`, `grp:`, `:`, `a:b:c`, `notanoption:x`, …) and 6 models (`zzz`, `pc10`, `PC105`, …) failed
0/11 and 0/6 (`options-sweep.txt`). An invalid option or model therefore never produces a keymap failure, and
therefore never produces a fallback in Hyprland either.

### 2. The names match Hyprland's fallback branch exactly (`live-join.txt`, `predict-cases.txt`)

`hyprctl devices -j` prints `active_keymap` from `getActiveLayout()`, which is
`xkb_keymap_layout_get_name` at `Hyprland-IKeyboard.cpp:313` (`const auto LAYOUTNAME = xkb_keymap_layout_get_name(KEYMAP, i);`),
surfaced at `Hyprland-HyprCtl.cpp:794` (`"active_keymap": "{}",`) via `Hyprland-HyprCtl.cpp:783`
(`const auto KM        = k->getActiveLayout();`). Recompiling each keyboard's *printed* rules reproduces that
string for every one of the 10 keyboards on this host, `active_keymap_mismatches=0`.

The fallback branch (`Hyprland-IKeyboard.cpp:101` `if (!m_xkbKeymap) {` … `:107` `memset(&XKBRULES, 0, sizeof(XKBRULES));`
… `:113` `m_currentRules.layout  = "us";` … `:115` recompile) was reproduced literally — all-NULL names with
`layout="us"` compiles to `English (US)`, so the post-fallback tuple Hyprland would print is
`layout='us' variant='' options='' model='' rules='' active_keymap='English (US)'`. Every case whose names fail
(typo layout, typo variant, typo rules, uppercase layout) lands on exactly that tuple, and every case whose names
compile keeps its declared tuple. The compile signal and the reference tool's FALLBACK rule agreed on all 15
declared-name sets (`signals_agree=True` each).

Two places where "failing names" is **wider** than "the compositor fell back", both from the source:

- **`kb_file` short-circuits the names.** `Hyprland-IKeyboard.cpp:87` (`if (!m_xkbFilePath.empty()) {`) tries the file at
  `:93`, and the names are only consulted at `:98` (`if (!m_xkbKeymap)`) — so with a compiling `kb_file` a set of names
  that would fail never runs. The file branch was exercised with `xkb_keymap_new_from_string` (TEXT_V2): a minimal
  `pc+br` map compiles to `Portuguese (Brazil)`, garbage returns NULL (`live-join.txt`). A `--xkb` mode must therefore
  compile the file first and, when it compiles, take the layout name from the file — the printed rules do not witness it.
- **Overridden keymaps ignore new names entirely.** `Hyprland-IKeyboard.cpp:61` (`if (m_keymapOverridden) {`) returns before
  any compile; `Hyprland-VirtualKeyboard.cpp:41` (`m_keymapOverridden = true;`) is what sets it. The virtual keyboard on
  this host happens to print `Portuguese (Brazil)` because its client sent the same map — a coincidence, not a compile result,
  which is why the reference tool keeps its VIRTUAL branch ahead of any compile-based verdict.

### 3. Environment dependence (`env-root-sensitivity.txt`, `include-path-matrix.txt`, `home-shadow.txt`, `xdg-root.txt`)

- **`XKB_CONFIG_ROOT` replaces the data root.** Pointed at an empty directory, **every** compile fails — `us` and the
  empty default included (`env-root-sensitivity.txt`). Pointed at the real `/usr/share/xkeyboard-config-2`, results are
  identical to the default. A probe whose environment differs from the compositor's therefore invents FALLBACKs.
- **Three additive, user-controlled include paths** prepend to the root and can supply a name that is absent from
  xkeyboard-config 2.48 (`include-path-matrix.txt`, `home-shadow.txt`): `XKB_CONFIG_EXTRA_PATH=<dir>` makes the searched
  set `[<dir>, /usr/share/xkeyboard-config-2]`, `XDG_CONFIG_HOME=<dir>` adds `<dir>/xkb`, and `HOME=<dir>` adds `<dir>/.xkb`.
  With a one-layout `symbols/zz` file in each of the three, the typo `zz` compiles to `Fake Shadow Layout` under all
  three variables and stays NULL under the default environment — **a compile probe can be made to predict a fallback
  that the compositor would not take, and to report a layout name that exists nowhere on the real system.**
- **Parity on this host today, shape-only.** The compositor's `/proc/1622/environ` is readable; it has `HOME` and
  `XDG_CONFIG_HOME`, and **0** variables whose name starts `XKB_` (names counted, no values read). The default include
  set is exactly one path, `/usr/share/xkeyboard-config-2`, with `~/.config/xkb`, `~/.xkb` and `/etc/xkb` reported as
  not addable — i.e. no user tree exists on this host. `XDG_DATA_DIRS` is not consulted (`xdg-root.txt`). Together with
  the 10/10 `active_keymap` equality this is why the probe is trustworthy *here*, and only here.
- **A `--xkb` mode must therefore pin the environment**: `XKB_CONFIG_ROOT` to the value the compositor resolved, and
  either refuse or report the presence of `XKB_CONFIG_EXTRA_PATH`, `XDG_CONFIG_HOME`-derived and `HOME`-derived trees.
  It cannot read the compositor's `/proc/<pid>/environ` to prove parity without leaving a pure config join.

## Could a future `--xkb` mode turn the entry's limit into a check?

Yes — and that is the specific limit it attacks. The draft entry declares it twice, at `entry.md:68`
(`The XKB compile itself is not reproduced`) and at `entry.md:24` (`the compile failure itself is not observed here`).
A config-only `--xkb` mode makes both checkable without a dump:

1. **Derive FALLBACK instead of inferring it.** "Printed `us` + four empties" is ambiguous between a genuine `us`
   config and a failed compile; the reference resolves it from the expected names, the compile resolves it from the
   data files. `us` and the empty default both compile to `English (US)` while `zz` is NULL, so declared-`us` is
   distinguishable from declared-`zz` even when no keyboard is present.
2. **Attribute the failure.** The printed tuple erases all five names at once; a bisect (each field alone against the
   defaults) names the culprit — `layout` for `zz`/`brq`/`BR`, `variant` for `br`+`zzz`/`us`+`nodeadkeys`, `rules` for `rules=zzz`,
   never `options` or `model` (`predict-cases.txt`, `culprit=` column).
3. **Predict before the dump, and cross-check a stale one.** A keyboard whose printed names are not `us`+empty can only
   have compiled, so a printed set that fails to compile is proof the dump is stale — a check the printed-name join cannot perform.

Implementation risks a `--xkb` mode must carry, all measured here:

- **stderr contract.** libxkbcommon writes `xkbcommon: ERROR: [XKB-…]` to stderr on failure, and the tool's contract
  keeps stderr empty on exit 0/1/3/4/5. `xkb_context_set_log_level(ctx, XKB_LOG_LEVEL_CRITICAL)` +
  `xkb_context_set_log_fn(ctx, NULL, NULL)` silences it: `stderr-silence.txt` shows `quiet zz -> None`,
  `quiet br -> ['Portuguese (Brazil)']`, and `stderr-silence.stderr` is **0 bytes**.
- **ABI.** `xkb_keymap_new_from_names2` is exported at `V_1.11.0` and present here (`nm -D`); the pre-1.11
  `xkb_keymap_new_from_names` has no format argument, so a mode on an older library must branch or fail setup cleanly.
- **Cost.** Measured in-process: **1.17 ms per compile** (200 compiles, `options-sweep.txt`); the whole probe
  table (16 cases + the fallback compile) finishes in 0.051-0.054 s wall including interpreter startup
  (`timing-determinism.txt`), so 2 compiles per keyboard plus a file compile is negligible.
- **Determinism.** Three consecutive runs produced identical tables (`deterministic_across_3_runs= True`).
- **Isolation.** The mode needs `/usr/share/xkeyboard-config-2` readable; the C1 counter's bubblewrap hides the
  repository, the lane and its parent, not `/usr` — [INFERENCE] compatible with clause i as written, but the mode
  must not read the compositor's `/proc` environment to prove parity (that is a process-table read outside a config join).
- **Environment pinning.** The mode must fix `XKB_CONFIG_ROOT` and account for the three *additive* user include
  paths (`XKB_CONFIG_EXTRA_PATH`, `$XDG_CONFIG_HOME/xkb`, `$HOME/.xkb`), each of which was shown to make a name
  that does not exist on this host compile to a fabricated layout name (`home-shadow.txt`).
- **What it still cannot see:** a runtime `hyprctl keyword` (compile depends on config, not on runtime state), a
  `kb_file` whose map is unreadable at probe time but readable by the compositor, and a compositor started with a
  different `XKB_CONFIG_ROOT` than the probe's shell.

## Evidence (all paths relative to this seat directory)

| file | what it shows |
|---|---|
| `xkb-probe.py` | the ctypes probe (16 declared-name cases + the literal fallback compile); `--json` mode |
| `probe-table.txt` | the compile table above, plus the `xkbcommon: ERROR` lines proving the failing names |
| `verify-live.py` | recompile each keyboard's printed rules from `hyprctl devices -j`; `kb_file` branch shape |
| `live-join.txt` | `keyboards=10 virtual=1 active_keymap_mismatches=0`; fallback tuple; file branch |
| `predict-table.py` / `predict-cases.txt` | 15 declared-name sets: compile, post-`setKeymap` tuple, reference verdict, xkb-mode verdict, culprit; `join_vs_compile_disagreements=0` |
| `timing-determinism.txt` | `deterministic_across_3_runs= True`, `approx_ms_per_compile= 3.16` |
| `options-sweep.py` / `options-sweep.txt` | 11 options and 6 models, 0/11 and 0/6 failing; `ms_per_compile=1.17` over 200 compiles |
| `stderr-silence.py` / `stderr-silence.txt` / `stderr-silence.stderr` | log silencing keeps a failing compile silent (0-byte stderr) |
| `env-root-sensitivity.txt` | compositor environ has 0 `XKB_*` names; `XKB_CONFIG_ROOT` empty ⇒ everything NULL; pinned to the real tree ⇒ default results; the default single include path |
| `include-path-matrix.txt` | searched sets under `XKB_CONFIG_EXTRA_PATH`, `XDG_CONFIG_HOME`, `HOME` — 2 paths each, the user dir first |
| `home-shadow.txt` | a one-layout `symbols/zz` under each of the three user paths makes `zz` compile to `Fake Shadow Layout`; NULL under the default environment |
| `xdg-root.txt` | `XDG_DATA_DIRS` is not consulted |
| `quote-check.py` / `quote-check.txt` | every quote above re-located by script at its `file:line` |
| `probe-manifest.txt` | sha256 of each receipt and script |

Nothing was installed (no package, no `uv`, no `npx`); no scratch survives (`/fast/scratch/hyaku/mado-r46/ExecXkbCompile` removed).
