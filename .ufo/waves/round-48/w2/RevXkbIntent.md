# w2 / RevXkbIntent — reverse-check: does C2 explain actual host compile behavior without overclaim?

Round 48, wave w2 (FALSIFY), base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Target: `.ufo/waves/round-48/l1-draft/xkb-keymap-compile-r48.md` (C2 entry), its rows S340–S350, and the receipt
`.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt` (sha256 `ab5fa971…`, 14270 B — matches row S350).
Attack axes: pinned xkbcommon 1.13.2 / xkeyboard-config 2.48 semantics vs the entry's citations; xkbcli vs the Hyprland
`XKB_CONTEXT_NO_FLAGS` context on this host (hyprland 0.56.2-4); whether the entry limits compositor-side live claims and
the `kb_file` bypass; unsupported mechanisms or omitted failure conditions.

**Verdict: no predicate-breaking defect found.** Every load-bearing claim in the entry traced to pinned bytes at the cited
line numbers, and the receipt replayed byte-exact on this host today. Three LOW findings (evidence provenance drift, one
over-broad `kb_file` wording, one wrong over-hedge in Limits) and two strengthening notes. None changes a measured value,
an rc, or a digest.

## Findings by severity

### LOW-1 — receipt self-names a wrong generator path (provenance drift, frozen bytes)
`.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt:1` says
`generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh`; the generator actually lives at
`.ufo/waves/round-48/tools/make-xkb-receipt.sh` (the `say` line is hardcoded in the generator, tools/make-xkb-receipt.sh:12).
Row S350 names the correct `tools/` path. The wrong path is inside the frozen receipt digest (`ab5fa971…`), so repair means
re-generating → new digest → counter re-run; only possible pre-data. Evidence value unaffected: every measured value in the
receipt replayed byte-identical (see Verified).

### LOW-2 — `kb_file` Limits bullet drops the held failure condition (over-broad wording)
Entry Limits: "a **readable** `kb_file` makes every table here about names moot (round-46 step 4, held)."
The actual chain (Hyprland v0.56.2 `src/devices/IKeyboard.cpp:87-99`, byte-identical to held row S319's pin
`8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d`): fopen failure → names path; **a file that opens but
fails to compile returns NULL and falls through to the names path** — so a readable-but-uncompilable `kb_file` does NOT make
the names moot; the names table still decides the keymap. The cited held source (r46 step 4, `hyprland-input-devices-r46.md:33`)
states the correct conditional: "the names only when no keymap came from the file". The r48 wording omits that parse-failure
fallback. Suggested repair (prose, pre-data): "a `kb_file` that yields a keymap makes the tables moot; a file that opens but
does not compile falls back to the names".

### LOW-3 — Limits wrongly hedges the compositor's libxkbcommon build (over-hedge, weakens the entry)
Entry Limits: "The compositor links **its own libxkbcommon build**; the package is the same 1.13.2-1, but build options
(extra include paths, extension directories) are [UNK] for that binary." On this host that is false in the conservative
direction: `ldd /usr/bin/Hyprland` → `libxkbcommon.so.0 => /usr/lib/libxkbcommon.so.0` — the same object `/usr/bin/xkbcli`
is linked against (both owned by libxkbcommon 1.13.2-1; `pacman -Qo /usr/bin/xkbcli`). There is exactly one build, so the
include-path/extension-dir behavior the receipt observed IS the compositor's, and that [UNK] can be closed with the ldd line.
Evidence: `w2/RevXkbIntent/hyprland-xkb-sites.txt`.

### NOTE-1 — unstated but true and strengthening: input-format parity
The entry never states which keymap input format either side uses. Verified: Hyprland 0.56.2 compiles **every** keymap with
`XKB_KEYMAP_FORMAT_TEXT_V2` + `XKB_KEYMAP_COMPILE_NO_FLAGS` (11/11 call sites: IKeyboard.cpp:93,99,115,247,253,259,283;
KeybindManager.cpp:314,315,328; protocols/VirtualKeyboard.cpp:91), and libxkbcommon 1.13.2's xkbcli default input format is
the same `TEXT_V2` (`src/keymap-formats.h:13`, `DEFAULT_INPUT_KEYMAP_FORMAT XKB_KEYMAP_FORMAT_TEXT_V2`, pinned commit
`d1442aaa…`). I additionally probed the five failure classes under both `--input-format v1` and `v2`: identical rc (1,1,1,1)
and byte-identical stderr; host names kccgst identical (evidence: `w2/RevXkbIntent/replay-battery-2.txt`). So the receipt's
compile runs in exactly the compositor's format; recording that (plus the v1-superset property from the pinned xkbcommon.h
docs) would close the "receipt proves only its own binary" residual a bit further. Not an overclaim as written — the entry
explicitly limits to xkbcli-only results.

### NOTE-2 — reading hazard in the step-1 env receipt (no change needed)
Step 1's last sentence is precise ("with the flag, `XKB_DEFAULT_LAYOUT=zz` **reaches the rules**"), but the supporting
receipt run is a `--kccgst` component print (`pc+zz+inet(evdev)`, rc 0) — `--kccgst` never opens the symbols file, so that
rc 0 is not a compile success for `zz`. The entry does not claim it is; recorded here so no later reader cites that rc as a
compile result.

## Verified (attack results that found nothing)

- **Pins/trust root.** All 14 fetch copies' sha256 match the digests declared in `l1-draft/rows-c2.md` (`w2/RevXkbIntent/pins.sha256`);
  upstream re-fetch at the pinned commits byte-matches: rules.c `04dfd934…` @ `d1442aaa…`, rules.in `16389776…` @ `cf8d1151…`
  (`w2/RevXkbIntent/upstream-pin-check.txt`). Host package files byte-equal where the rows say so: `/usr/share/xkeyboard-config-2/rules/evdev`
  = `0cc48ee1…`, `symbols/br` = `8cf65550…`; `br` has exactly 11 `xkb_symbols` maps as claimed.
- **Receipt replays byte-exact** (libxkbcommon 1.13.2-1 / xkeyboard-config 2.48-1 / xkbcli 1.13.2, host today):
  positive `--layout br --options compose:caps` rc 0, keymap sha256 `efd487a3…` 2090 lines / 73079 bytes, empty stderr —
  byte-identical to the receipt; negatives rc (1,1,0) with XKB-338/661/769/822 for `zz`/`br(nope)`/`br(caps)`, XKB-595
  "No components returned" for `xfree98`, XKB-338+XKB-595 for `rules nope`, XKB-595 "was ignored" rc 0 for `nope:nope`;
  `--model nope` silent at warn level with geometry `pc(pc104)`; multi-layout pairings (`pc+br(nodeadkeys)+us:2+inet(evdev)`,
  ERROR "Less layouts than variants" with rc 0, `br,us --variant ,dvorak` → `us(dvorak):2`); defaults `pc+us+inet(evdev)`;
  env gate (`XKB_DEFAULT_LAYOUT=zz` ignored without the flag, reaches rules with `--enable-environment-names`);
  precedence probes rc 0/0 byte-identical, neither-path rc 1; root-override fallback warning visible only at warn level, rc 0.
  (`w2/RevXkbIntent/replay-battery-1.txt`, `replay-battery-2.txt`.) The counter's clause (f) window requirements and clause (r)
  replay expectations (rc 1,1,0 + named diagnostics + digest byte-compare) are all satisfiable against what I measured.
- **Hyprland NO_FLAGS context claim is true tree-wide.** v0.56.2 `src/` has exactly four `xkb_context_new` sites —
  IKeyboard.cpp:75, IKeyboard.cpp:226, KeybindManager.cpp:311, protocols/VirtualKeyboard.cpp:75 — **all** `XKB_CONTEXT_NO_FLAGS`,
  i.e. the compositor's contexts read the environment, exactly as step 1 says (the entry cites IKeyboard.cpp:75 as instance).
  Names passed as C strings, never NULL (IKeyboard.cpp:67-73). No `xkb_context_set_log_level`/`set_log_fn` anywhere in `src/`,
  so the library default (ERROR, context.c:503) governs the compositor's diagnostics too — step 8/9's "NULL is all Hyprland
  sees" and the warning-visibility story hold for the compositor, not just xkbcli.
- **Reset-to-us fallback matches held S319.** IKeyboard.cpp:101-116: failed compile → error overlay naming the rejected names,
  stored rules reset (`layout = "us"` at :113, rest empty), retry — the held quote is at the cited line of the same bytes.
- **kb_file bypass is explicitly limited.** Entry Limits names the bypass and cites r46 step 4; LOW-2 is a wording precision
  issue, not a missing limitation. Compositor-side live claims are explicitly limited twice: the licenses table row
  ("not run against the live compositor") and Limits ("The compositor half is held, not measured"), with S318/S319 cited as
  held and "never re-claimed" — consistent with the registration's separability language.
- **Pinned-source citations spot-checked at exact lines, all correct:** tools-compile-keymap.c:521, :587; context-priv.c:208, :218;
  context.c:317, :336, :503 (and append_default order 243-338: XDG→`$HOME/.config/xkb`, `$HOME/.xkb`, extra `/etc/xkb`,
  versioned-then-unversioned extension subdirs, root last, legacy-root fallback behind a warning — matches the receipt's
  verbose census); rules.c:524/530, :1259, :1297, :1986-1992, :2028-2036, :2063; xkbcomp.c:60-64 (`!CompileKeymap → false`),
  :157/:161; include.c:355, :501; messages-codes.h:116/:150; meson_options default-layout `us` at :46; symbols-br:47 quote;
  rules-evdev catch-all and `compose:caps` rows; r46 entry line 33 = its step 4.
- **Host config facts** (entry's "Live host run"): `~/.config/hypr/input.conf` lines 10-11 `kb_layout = br` / `kb_options =
  compose:caps`, sha `3769c92a…`; omarchy default line 3 `kb_layout = us`, sha `bee5aa68…` — both match the receipt exactly.

## Residual risk and verification gaps

- Whether the *running* compositor's environment carries any `XKB_DEFAULT_*` remains [UNK] by the entry's own design; I did
  not introspect the live Hyprland process (host guard: no process/environment probing beyond read-only file checks), so the
  entry's [UNK] stands unconfirmed and unrefuted. This does not affect any entry claim — step 1 is conditional.
- The wl_keyboard client-keymap path (VirtualKeyboard.cpp:91, `new_from_string` TEXT_V2, NULL → `noMemory`) and the
  per-bind translation path (KeybindManager.cpp:300-335, same NO_FLAGS/V2/NULL-reset pattern) are outside the entry's claims;
  r46 step 6 holds the virtual-keyboard surface. Consistent with the entry's held story; not cited, and need not be.
- The `rules.in` → installed `rules/evdev` generation mapping stays [UNK] per the entry (I verified the pinned rules.in bytes
  but did not re-run the meson generator); acceptable, the entry claims only the meson target's name.
- `pacman -Q`/`-Qo` queries printed an unrelated `error: openai-chatgpt: missing required signature` from the host package
  database. Read-only query only; no transaction run (host-wide pacman pause respected). No installs were performed by this seat.

## Work record

- Scratch: `/fast/scratch/hyaku/mado-r48/RevXkbIntent/` (created with `mkdir -p`; `ulimit -f 2048` set in every writer shell;
  total peak 9.3 MB — under the 2 GB budget). Largest output file: the abandoned Hyprland tarball at exactly 1,048,576 bytes —
  the 1 MiB/file ulimit cut it mid-write (curl error 23), demonstrating the guard; replaced by a streamed `curl | tar`
  extraction that wrote only sub-1MiB files. Scratch deleted after copying the evidence below.
- Evidence copied to `.ufo/waves/round-48/w2/RevXkbIntent/`: `pins.sha256`, `battery1.txt`, `battery2.txt`,
  `hyprland-xkb-sites.txt` (tree-wide sites + ldd + IKeyboard sha), `upstream-pin-check.txt`, `IKeyboard-0.56.2.cpp`
  (15,941 B, sha `8a800efe…` = held row S319's recorded digest). All files ≤ 15,941 B.
- No lane file, counter, fixture, registry, README, or sibling artifact was modified; no git/jj mutation; no compositor,
  input, or PATH-directory contact. Every xkbcli call was a compile/test/kccgst read verb with stdout/stderr into scratch.
