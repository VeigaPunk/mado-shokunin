# ExecFetchDispatch — round-51 w1 fetch pins (C2 dispatcher surface)

Seat: executor (leaf). Lane: mado-shokunin. Round 51 / hyaku run 10, wave w1 (BUILD).
Inputs read: `.ufo/waves/round-51/claims.md` (C2 frozen predicate), `corpus/lessons/round-50-verifier-spotcheck.md`
(§6 routed defects), the round-50 pins under `.ufo/waves/round-50/fetch/`, `w1/ScoutDispatchMap.md`.
Scope executed: commit-pinned fetch of the Hyprland 0.56.2 keybind-dispatcher surface, its checksum manifest,
and the verification instruments that make every pin citable by the C2 scribes.

## Deliverables
- `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch/SHA256SUMS`
- `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch/fetch-manifest.json`
- `.ufo/waves/round-51/w1/ExecFetchDispatch/anchors.txt`
- `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch-all.sh`
- `.ufo/waves/round-51/w1/ExecFetchDispatch/verify-anchors.py`
- `.ufo/waves/round-51/w1/ExecFetchDispatch/receipts/verify.txt`
- `.ufo/waves/round-51/w1/ExecFetchDispatch/receipts/d4-m50-9-self-row.txt`

The pin tree itself is the directory `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch/` (19 pin files; a directory is
not a file declaration). Contents:

- `fetch/` — 19 pin files, byte-fetched with `curl -fsSL` from `raw.githubusercontent.com`
- `fetch/SHA256SUMS` — 19 rows over pin files only, no self row
- `fetch/fetch-manifest.json` — URL, revision, bytes, sha256, git blob sha1 per file
- `anchors.txt` — 75 verified `pin:line<TAB>quote` pairs for the C2 scribes
- `fetch-all.sh` — the reproducible pinned fetcher (`--out`/`--scratch`, blob-verified, self-row guard)
- `verify-anchors.py` — anchor checker with a hermetic `--selftest`
- `receipts/verify.txt` — fetch/anchor/sums/manifest/reproducibility transcript
- `receipts/d4-m50-9-self-row.txt` — routed D4 evidence (round-50 self-row, round-51 convention)

Report: .ufo/waves/round-51/w1/ExecFetchDispatch.md

## 1. Pins fetched (3 revisions, 19 files)

Hyprland @ `efb50993780079460b0cbed1363e2166a2de1d9f` (0.56.2, the round-50 code revision):

| pin | source path | bytes | sha256 |
|---|---|---|---|
| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | 39334 | `8d8f35fc…9342d4e40` |
| Hyprland-KeybindManager.hpp | src/managers/KeybindManager.hpp | 7936 | `cee22c13…51228dd1e0` |
| Hyprland-legacy-ConfigManager.cpp | src/config/legacy/ConfigManager.cpp | 90963 | `9db68cf4…1f65be62b` |
| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/DispatcherTranslator.cpp | 35997 | `7248cbb8…c1610fbe771` |
| Hyprland-legacy-DispatcherTranslator.hpp | src/config/legacy/DispatcherTranslator.hpp | 567 | `438c1e66…b3444e87` |
| Hyprland-ConfigActions.cpp | src/config/shared/actions/ConfigActions.cpp | 71407 | `a83abeb5…1b48a7637` |
| Hyprland-ConfigActions.hpp | src/config/shared/actions/ConfigActions.hpp | 6960 | `746c6f51…3091b7073` |
| Hyprland-ConfigManager.cpp | src/config/ConfigManager.cpp | 2597 | `c10dc1ce…541b01f366` |
| Hyprland-ConfigManager.hpp | src/config/ConfigManager.hpp | 2972 | `26b118b5…e39da38a` |
| Hyprland-HyprCtl.cpp | src/debug/HyprCtl.cpp | 97582 | `798b7c6c…247b91fa` |
| Hyprland-SharedDefs.hpp | src/SharedDefs.hpp | 1915 | `0b40cc83…cafe0087` |
| Hyprland-docs-hyprctl.1.rst | docs/hyprctl.1.rst | 2623 | `07cd7387…0e0ac166` |

hyprutils @ `a21e87b878e72ee5dfd375899e8b2ad0d0c4c0e1` (= tag `v0.14.2`, the version installed here as
`hyprutils 0.14.2-1`; Hyprland links it through `pkg-config hyprutils>=0.14.0` — `CMakeLists.txt:150` — so no commit
is derivable from the Hyprland pin):

| pin | source path | bytes | sha256 |
|---|---|---|---|
| Hyprutils-VarList.hpp | include/hyprutils/string/VarList.hpp | 1883 | `9ad2fcbd…b74fc43` |
| Hyprutils-VarList.cpp | src/string/VarList.cpp | 1189 | `b02df8d6…b166a36` |
| Hyprutils-VarList2.hpp | include/hyprutils/string/VarList2.hpp | 2905 | `0e484df5…441f2179` |
| Hyprutils-VarList2.cpp | src/string/VarList2.cpp | 5033 | `b8cacea7…b76cf26d` |

hyprland-wiki @ `d5f07c60e16fe03744aabb76e492117b7f7c4679`:

| pin | source path | bytes | sha256 |
|---|---|---|---|
| wiki-Dispatchers.md | content/Configuring/Basics/Dispatchers.md | 13337 | `39d0747a…095c1f494` |
| wiki-Binds.md | content/Configuring/Basics/Binds.md | 19526 | `3d8a2a68…54b17d628` |
| wiki-Using-hyprctl.md | content/Configuring/Advanced%20and%20Cool/Using-hyprctl.md | 7859 | `3489a75d…55ab3545` |

Exact digests are in `fetch/SHA256SUMS` and `fetch/fetch-manifest.json` (this table elides middles for readability only;
the files carry them in full).

Two-way integrity: every fetch is verified against the **git blob sha1 of the pinned tree** (recomputed from the fetched
bytes), not just against HTTP success — so a transcribed URL that resolves to a different revision would fail. The
hyprutils and wiki blob ids come from the GitHub tree API for their pinned revisions; the three shared with round 50 are
additionally byte-identical to the round-50 pins (`cmp_equal`, identical sha256 — `receipts/verify.txt` §5).

## 2. Mechanism anchors handed to the C2 scribes

`anchors.txt` holds 75 `pin:line<TAB>quote` rows, each quote a verbatim substring of that pin line (≤25 words), all
re-verified by `verify-anchors.py` (75/75 pass). This is exactly the shape C2 clause (b)/(d) needs: a row's quote must
be verbatim on its pin line, and a `held:` citation must name a line containing its key tokens.

The surface, as it actually exists at 0.56.2 (note the claim text's names are approximate — see §3):

1. **Parse** — `CConfigManager::handleBind` (`legacy-ConfigManager.cpp:1492`) splits the bind line with
   `CVarList(value, numbArgs)` (`:1555`), takes `HANDLER = ARGS[2+…]` (`:1584`), the arg as `COMMAND = ARGS[3+…]`
   (`:1586`), lowercases the handler (`:1592`) and validates it against `m_dispatchers` at parse time (`:1594`),
   returning `Invalid dispatcher, requested …` (`:1598`) for unknown names. Because `CVarList` stops splitting at
   `lastArgNo` and keeps the remainder (`Hyprutils-VarList.cpp:20-21`, documented at `Hyprutils-VarList.hpp:10`), the
   4th bind field absorbs every later comma — `bind = SUPER, Q, exec, a, b` passes `a, b` to `exec`.
2. **Registry** — `CKeybindManager::CKeybindManager` fills `m_dispatchers` from a fixed name list
   (`Hyprland-KeybindManager.cpp:41` comment, `:84` submap entry, `:113` emplace) with one lambda that forwards to
   `Config::Legacy::translator()->run(name, args)`. `m_dispatchers` is public (`KeybindManager.hpp:114` class opens,
   `:137` member, `:155` private), which is why both `HyprCtl.cpp` and the config parser reach into it directly.
3. **Trigger** — `CKeybindManager::handleKeybinds` (plural) matches the pressed key against `m_keybinds`
   (`:652` mods/submap gate, `:700` catchall gate), then per hit resolves `m_dispatchers.find(k->mouse ? "mouse" :
   k->handler)` (`:785`), logs `Invalid handler in a keybind!` if absent (`:799`), and calls
   `DISPATCHER->second(k->arg)` (`:812`; mouse binds get `"1"`/`"0"` prefixed, `:810`). Unknown handlers are
   unreachable from a parsed config, so that branch is defensive only.
4. **Argument dispatch** — `CDispatcherTranslator::run` (`legacy-DispatcherTranslator.cpp:30`) looks the name up in
   `m_dispMap` (`:34`) and returns `{success=false, error="Bad dispatcher"}` otherwise (`:32`); each dispatcher then
   re-splits its own argument (`CVarList2` / `substr` per dispatcher).
5. **Submap special cases** — a `submap` hit suppresses event pass-through and stops evaluating further binds
   (`:775`, `:816`); after a non-submap dispatcher, the bind's `reset` field switches submap
   (`:820-823` → `Config::Actions::setSubmap`), and `setSubmap` sets the state at `ConfigActions.cpp:1674` (`reset`/empty
   clears it, `:1665-1666`). `submap` is a dispatcher too (`DispatcherTranslator.cpp:521`, `:839`), and catchall binds
   are legal only inside a submap (`legacy-ConfigManager.cpp:1620-1621`).
6. **hyprctl path** — `dispatchRequest` (`HyprCtl.cpp:1126`) strips the command word (`:1128`); under a lua config
   provider it rewrites the whole request into `hl.dispatch(...)` (`:1130`, `:1132`); otherwise it splits on the first
   space into `DISPATCHSTR` (`:1143`) and `DISPATCHARG` (`:1147`), looks up the same `m_dispatchers` (`:1150`),
   returns `Invalid dispatcher` (`:1151`), calls it (`:1153`) and prints `ok` or the error text (`:1157`). Which branch
   runs is decided by config-provider selection: a `.lua` main config selects the Lua manager, anything else the legacy
   manager (`Hyprland-ConfigManager.cpp:33-40`; enum `ConfigManager.hpp:28-29`). This host's plane is hyprlang
   (`~/.config/hypr/hyprland.conf`, no `.lua`), so it takes the legacy branch.
7. **Result type** — `SDispatchResult` defaults `passEvent=false`, `success=true` (`SharedDefs.hpp:52-55`), so a
   dispatcher that forgets to set `success=false` reports success to hyprctl and to the bind-passthrough logic.

## 3. Two wording corrections for the freeze (claims text vs source)

- `claims.md` C2 says `handleKeybind -> m_mDispatchers`. At `efb50993` the member is `m_dispatchers` (lowercase) and the
  function is `CKeybindManager::handleKeybinds` (plural). Nothing in the tree matches `m_mDispatchers`. A counter or
  entry that greps for the claim's spelling will find nothing; use the source spelling.
- The wiki at `d5f07c60` is **lua-era**: `wiki-Dispatchers.md:7-8` points at the 0.54 pages for "the old hyprlang
  syntax" ("Since Hyprland 0.55, hyprlang is deprecated in favor of lua"), and `Binds.md`/`Dispatchers.md` document
  `hl.bind()` / `hl.dsp.*` objects. The *string* dispatcher path
  (`bind = MODS, KEY, dispatcher, arg`, `hyprctl dispatch <name> <arg>`) is code-only at this revision. Round 50 rejected
  rendered 0.54 archive pages for lacking a commit anchor, so that boundary holds here too: cite the wiki for the
  dispatcher vocabulary, submap semantics and `hl.dispatch` shorthand — not for hyprlang bind syntax.

## 4. ScoutDispatchMap and additional requests

`w1/ScoutDispatchMap.md` was a 105-byte stub ("Status: investigating…", sha256 `eea88736…`) when this seat ran, so the
pin set was derived from my own read of the pinned tree as the ticket allows (`receipts/verify.txt` §9 records the stub
bytes/digest at run time). Mid-run, `ScrDispatchEntry` requested one more pin by message; it is included and its
independently fetched digest matches mine exactly (`receipts/verify.txt` §6):

- `Hyprland-SharedDefs.hpp` ← `src/SharedDefs.hpp` @ efb50993, 1915 B, sha256
  `0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087`.

I additionally pinned hyprutils `VarList`/`VarList2` (header + implementation) because the "argument splitting" clause of
C2 would otherwise be unsourced: the remainder rule lives in that library, not in Hyprland.

## 5. Routed item D4 / M50-9 (fetch checksum manifest self-row)

Receipt: `receipts/d4-m50-9-self-row.txt`. Findings, measured:

- `.ufo/waves/round-50/fetch/SHA256SUMS:7` carries `bb21f728…10054d07  SHA256SUMS`; the file's actual digest is
  `e2b91106…791ff0d` (1416 B), so `sha256sum -c` fails with exactly one mismatch and exits 1. The row is unverifiable by
  construction — the digest predates the row that contains it.
- Round-50 bytes were never touched: `git status --porcelain .ufo/waves/round-50/fetch` is empty; the file's last commit
  is `1b37a59e` (run-9 wrap-up). The defect is retired by convention instead: **pins only, meta artefacts never
  digested**. The round-51 manifest has `self_row_lines=0`, and `fetch-all.sh` hard-exits 6 if a `SHA256SUMS` line ever
  names `SHA256SUMS` (`fetch-all.sh:116`), so the class cannot recur silently.

## 6. Verification exercised (all committed receipts)

| Check | Command | Result |
|---|---|---|
| Anchor verifier selftest | `python3 -I verify-anchors.py --selftest --scratch <scratch>` | 6/6 cases, `wrong=0`, exit 0 (positive, wrong-quote, wrong-line, out-of-range, missing-pin, >25 words) |
| Anchor table vs pins | `python3 -I verify-anchors.py --pins fetch` | `anchors=75 pin_files=19 failed=0`, exit 0 |
| Checksum manifest | `cd fetch && sha256sum -c SHA256SUMS` | 19/19 OK, `self_row_lines=0`, exit 0 |
| Manifest vs disk | recompute sha256 + git blob sha1 per manifest row | `mismatched=0 unmanifested_pins=[]`, exit 0 |
| Commit binding | blob sha1 vs GitHub tree at each pinned revision | 19/19 match (enforced inside `fetch-all.sh`; a mismatch exits 5) |
| Round-50 consistency | `cmp` of the 3 shared pins + digest comparison | `cmp_equal` ×3, identical sha256 |
| Reproducibility | re-run `fetch-all.sh --out <scratch>/rerun` | `cmp_equal=19 differ=0`, `SHA256SUMS identical` |
| Scribe cross-check | SharedDefs digest vs `ScrDispatchEntry`'s own fetch | equal (`0b40cc83…`) |

Transport: `curl 8.23.0`, `-fsSL --max-time 90 --retry 2` per URL, `raw.githubusercontent.com` only; every response
status recorded as 200. Nothing was copied from a sibling seat's fetch dir; nothing was extracted from the round-50 pins.

## 7. Integration instructions for L1

1. `cp -a .ufo/waves/round-51/w1/ExecFetchDispatch/fetch/. .ufo/waves/round-51/fetch/` (or `mv`), byte-identical. The
   `SHA256SUMS` rows are bare basenames, so `cd .ufo/waves/round-51/fetch && sha256sum -c SHA256SUMS` keeps working
   after the move; no digest needs rewriting.
2. `fetch-manifest.json` is the "pin manifest" C2 clause (b) refers to — the entry must name pins by the basenames in
   it, and rows S364–S379 must quote lines that exist in those files (use `anchors.txt`).
3. Do not add a `SHA256SUMS` row for either meta artefact (D4).
4. If the freeze wants regen: `bash .ufo/waves/round-51/w1/ExecFetchDispatch/fetch-all.sh --out <dest> --scratch <dir>`
   (honours `--scratch`; never a hardcoded `/tmp`).

## 8. Tooling, host and scratch

- No tool installed or upgraded. Used only pre-installed `curl`, `python3` (3.14.8), `sha256sum`; `pacman` untouched.
- Config planes read only: `~/.config/hypr/` listing + `hyprland.conf` head (to establish the host's provider is hyprlang,
  not lua) and the installed `hyprutils` pkg-config version. No compositor socket was connected, no service touched, no
  file under `~/.config` written.
- Disk guard checked before the pass: `/fast` 295 G free, `/tmp` 124 G free — no ENOSPC risk for ~440 KB of pins.
- Scratch used: `/fast/scratch/hyaku/mado-r51/ExecFetchDispatch/` (recon downloads, staged fetch, rerun, selftest
  fixtures). **Deleted before yielding**; nothing of value lived only there — every receipt is copied into the seat dir.
- Writes were confined to the seat dir plus this report. No tracked file was edited; no git/jj mutation was run (read-only
  `git status` / `git log` only).

## 9. Risks and boundaries

- **Scout stub**: the recon seat contributed no requests; if it later names a source outside my 19, that source is
  unpinned. The 19 cover parse → registry → trigger → dispatch → submap → hyprctl → result type, plus the argument-splitting
  library, which is the whole declared clause surface.
- **hyprutils pin is tag-derived** (`v0.14.2` → commit `a21e87b8`), because Hyprland's dependency is a pkg-config range,
  not a submodule. It matches the installed `0.14.2-1`; a host on a different hyprutils minor could split arguments
  differently (the `allowEscape` behaviour of `CVarList2` is version-sensitive).
- **Lua dispatch path not pinned**: `src/config/lua/bindings/LuaBindingsDispatchers.cpp` (54 KB) exists at this revision
  but is outside the string-dispatcher clause; `HyprCtl.cpp:1130-1141` shows the wrapper and delegation, so the entry can
  state the branch without that file. Add it only if the freeze widens C2 to the lua object surface.
- **`ignoreMods`/release semantics** (`Hyprland-KeybindManager.cpp:728`, `:736`) touch `handleKeybinds` but belong to round 50's bind-match entry; they
  are cited in the pins but are not this fetch's claim.
