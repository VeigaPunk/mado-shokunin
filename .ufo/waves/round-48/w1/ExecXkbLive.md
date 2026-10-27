# ExecXkbLive — C2 live receipt (xkbcli compile matrix, Hyprland kb_* plane)

Round 48 w1 (BUILD), lane mado-shokunin, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Seat scope: **the C2 live read-only receipt only** (`xkbcli compile-keymap` matrix on this host). The
knowledge entry `corpus/knowledge/xkb-keymap-compile-r48.md`, the SOURCES rows and the registry are
the integrator's/entry-owner's write; this seat wrote no tracked file.

## Axes named (godspeed)

1. **coverage / sourced-core** — every name class the entry needs (`kb_layout`, `kb_variant`,
   `kb_options`, `kb_model`, `kb_rules`) now has an executed rc + first `XKB-###` on this host, plus the
   include-path order that decides where a name is looked up.
2. **evidence freshness** — the receipt is regenerable, bounded and byte-stable across runs (two runs
   identical apart from the `date` line), so the entry can cite a command, not a memory.
3. **operability of the instrument** — `probe.sh` is a single read-only script; the matrix, the scratch
   symbols fixture and the compositor read are one invocation, so a recheck after a package update is cheap.

## Deliverables

| path (relative to lane root) | sha256 | note |
|---|---|---|
| `.ufo/waves/round-48/w1/ExecXkbLive/probe.sh` | `a40e486a01f903c1b29114b92fa52aef8d31ac9da78d40cf522303f2d47eb983` | bounded, read-only, `trap`-cleaned scratch; every xkbcli call pinned under `env -i` (see below); writes only `receipts/xkb-live.txt` |
| `.ufo/waves/round-48/w1/ExecXkbLive/receipts/xkb-live.txt` | `a0c488c87301054c253098c23bcb75bca40360d305c704a47cb1639d193db618` | 208 lines, 9 sections (§0-§8); **reproducible**: two consecutive runs differ only in line 2 (`date`) |

Reproducibility check actually run: `./probe.sh; cp receipts/… run1; ./probe.sh; diff <(grep -v '^date' run1) <(grep -v '^date' receipts/…)`
→ no diff. Locators below are receipt line numbers (computed with `grep -n`, not typed) unless a
`file:line` of another document is named.

Safety as executed: no compositor mutation, no terminal/GUI launch, no package transaction, no write to
`~/.cache` (`XDG_CACHE_HOME` is redirected into scratch and xkbcli never creates it — receipt:205-208),
no host config or binary touched. **Environment pinned**: every xkbcli call runs under
`env -i PATH=/usr/bin:/bin LC_ALL=C HOME=$S/pinhome XDG_CONFIG_HOME=$S/pinhome/.config`, so the caller's
`XKB_CONFIG_ROOT` / `XKB_CONFIG_EXTRA_PATH` / `XKB_LOG_LEVEL` / `XKB_DEFAULT_*` and user xkb dirs cannot
change the measurement; §7 varies those one at a time on purpose. `hyprctl` alone stays in the ambient
session env (it needs the compositor socket). Scratch `/fast/scratch/hyaku/mado-r48/ExecXkbLive` deleted at
the end.

## Findings

### F1 — the host's own RMLVO compiles, and that is the keymap the compositor reports

- Config shape (only `kb_*` values): `kb_layout = br`, `kb_options = compose:caps`; `kb_variant`,
  `kb_model`, `kb_rules` are absent → derived RMLVO `br` / `` / `compose:caps` (receipt:24, source lines
  `~/.config/hypr/input.conf:10-11`). The commented alternates are `# kb_layout = us,dk,eu` (`:5`),
  `# kb_variant = intl` (`:8`) and `# ,grp:alts_toggle` on the options line (`:11`).
- `xkbcli compile-keymap --layout br --options compose:caps` → **rc 0**, 2090 lines, 73079 bytes,
  sha256 `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81` (receipt:29-32).
- `--rmlvo` fills the defaults `rules evdev`, `model pc105`, `variant ""` (receipt:47-52); `--kccgst`
  gives the component split `keycodes evdev+aliases(qwerty)`, `types complete`, `compat complete`,
  `symbols pc+br+inet(evdev)+compose(caps)`, `geometry pc(pc105)` (receipt:41-46). So on this host a
  layout name is looked up as `symbols/<name>`, a variant as the section inside that file, an option as
  `symbols/<group>(<name>)`.
- The live compositor agrees: `hyprctl devices -j` reports **10 keyboards, one distinct
  (layout,variant,options,active_keymap) tuple = (`br`,``,`compose:caps`,"Portuguese (Brazil)")**, active
  index 0, names replaced `kbd1..kbd10` (receipt:127-138). Hyprland 0.56.2 at `efb50993` (receipt:12).
  Read-only verbs only (`hyprctl version`, `hyprctl devices -j`).

### F2 — failure vs silent drop: the exact split (this is what maps onto Hyprland's fallback)

| class | command shape | rc | first stderr code | keymap effect | receipt |
|---|---|---|---|---|---|
| unknown layout | `--layout zz` | **1** | `XKB-338` `Couldn't find file "symbols/zz"` | none (empty stdout) | :55 |
| unknown rules | `--rules nope --layout br` | **1** | `XKB-338` `Couldn't find file "rules/nope"` | none | :63 |
| unknown variant | `--layout br --variant nope` | **1** | `XKB-661` `Couldn't process include statement for 'br(nope)'` | none | :57 |
| variant valid for a *different* layout | `--layout br --variant intl` | **1** | `XKB-661` `'br(intl)'` | none | :73 |
| variant on the wrong layout index | `--layout us,br --variant abnt2` | **1** | `XKB-661` `'us(abnt2)'` | none | :67 |
| unknown option | `--layout br --options nope:nope` | **0** | `XKB-595` `Unrecognized RMLVO option "nope:nope" was ignored` | **stdout byte-identical to `--layout br`** | :59, :86-87 |
| unknown option (other shapes) | `nope:caps`, `grp:nope`, `grp:alts_toggle:nope` | **0** | `XKB-595` each | whole option dropped, stdout byte-identical to baseline | :94-96 |
| unknown model | `--layout br --model nope` | **0** | none at all (0 stderr lines) | stdout byte-identical to baseline; `--rmlvo` still prints `model: "nope"` | :61, :86, :92 |

**Variant alignment**: `variant[i]` binds to `layout[i]` and an empty slot is a leading comma.
`--layout us,br --variant ,abnt2` → rc 0, symbols `pc+us+br(abnt2):2+inet(evdev)` (:65, :82); the same
pair with `abnt2` unshifted fails on `us(abnt2)` (:67); `--layout br,us --variant abnt2` is rc 0 (:69).

**More variants than layouts**: `--layout br --variant abnt2,intl` → **rc 0**, stderr
`Less layouts than variants: "br" vs. "abnt2,intl".`, and the *first* variant is still applied — stdout
is byte-identical to `--layout br --variant abnt2` and kccgst is `pc+br(abnt2)+inet(evdev)` (:71, :88-90).
A misplaced variant list therefore compiles silently into the first variant, not into the base layout.

**Warnings vs errors (verbosity)**: the host compile prints **0 stderr lines at default verbosity**; with
`--verbose` it prints 127, census `XKB-302` n=6 (deprecated keysym `masculine` in `br`), `XKB-461` n=49
(multiple symbols per level), `XKB-965` n=3 (`Caps_Lock`/`Alt_R` not in the symbol map) (receipt:33-38).
`XKB-595` and `Less layouts …` are **errors** and print without `--verbose`; those three warnings do not.

**Qualification on the `XKB-595` message (receipt §7a, :176-189)**: the drop is unconditional, the
*message* is not. Measured matrix (`rc=0` and `sha16=6ef2127653b0ca1a` in **every** row):
`XKB_LOG_LEVEL=0/3/5/10` (numeric below 20) and `critical` → **silent**; `=20`, `=30`, `error`,
`warning`, `none`, an unknown token (`bogus`, falls back to the default) and `debug` → message printed
(`debug` also emits 25 lines of chatter). So "dropped with a warning" is a statement about the default log
level, not about the compile.

**Accepted cases that the entry should record as healthy**: `grp:alts_toggle` alone → rc 0,
`pc+br+inet(evdev)+group(alts_toggle)` (:75, :84); host options + group
`compose:caps,grp:alts_toggle` → rc 0 (:77); the commented `us,dk,eu` + `intl` pair →
rc 0, `pc+us(intl)+dk:2+eu:3+inet(evdev)`, i.e. `intl` attaches to `us` and the pair would work if
uncommented (:79, :83).

### F3 — include-path order, and proof that a layout comes from a user path

`--verbose` on this host (receipt:100-105, measured under the pinned HOME/XDG): `$XDG_CONFIG_HOME/xkb`
(failed, absent), `$HOME/.xkb` (failed, absent), `/etc/xkb` (failed, absent), extension paths
`/usr/share/xkeyboard-config-2.d` and `/usr/share/xkeyboard-config.d` (absent), then
**`/usr/share/xkeyboard-config-2` added**. So the search order is `$XDG_CONFIG_HOME/xkb`, `$HOME/.xkb`,
the **extra path** (`/etc/xkb` by default, overridable with `XKB_CONFIG_EXTRA_PATH`), then the
xkeyboard-config root — and all three user paths are absent on this host (receipt:106-110).

Precedence is measured, not read off the log: a poisoned `symbols/zz` placed in each vector resolves in that
same order — `$XDG_CONFIG_HOME/xkb` → `dead_acute`, adding `$HOME/.xkb` still gives `dead_acute`,
`$HOME/.xkb` alone → `dead_greek`, `XKB_CONFIG_EXTRA_PATH` alone → `dead_circumflex`, `$HOME/.xkb` +
extra → `dead_greek` (receipt:195-201). The same poisoned `zz` also shows the F2 "unknown layout" verdict
is a statement about the **tree**: with the pinned tree `--layout zz` is rc 1 `XKB-338`, with a poisoned
user dir the identical command is rc 0 and compiles (:196-197).

Scratch fixture (one tiny `symbols/mado48`, `include "us(basic)"`, `<AD11>` distinguished by keysym;
body in receipt:112-116) proves which path supplies it:

- `XDG_CONFIG_HOME=<scratch>/cfg` (HOME without `.xkb`) → rc 0, AD11 = `dead_acute` (:117);
- `HOME=<scratch>/home` with `~/.xkb/symbols/mado48`, XDG pointed at an empty dir → rc 0, AD11 =
  `dead_greek` (:118);
- **no user path** (host defaults intact) → **rc 1, `XKB-338 Couldn't find file "symbols/mado48"`** (:119)
  — the layout compiles *only* through the user path that provides it; nothing in the xkeyboard-config
  root answers for it.

Flag behaviour: `--include <dir>` **replaces** the default list, so the run dies on `rules/evdev`
(`XKB-338`, :120); `--include <dir> --include-defaults` restores the defaults and compiles (:121);
with two include dirs the **first-listed wins** — `--include oa --include ob` yields `AD11=dead_acute`,
reversed yields `dead_greek` (:122-123).

### F4 — the compiler and the registry disagree about names (coverage trap for the entry)

- `xkbcli list` (the rules-XML registry): 184 models, 598 layout entries, 499 variant entries, no
  options list (receipt:141-142).
- `br` variants **advertised**: `nodeadkeys dvorak nativo nativo-us thinkpad thinkpad_nodeadkeys
  nativo-epo rus`; `br` symbols file **declares** `abnt2 nodeadkeys thinkpad thinkpad_nodeadkeys olpc rus
  dvorak nativo nativo-us nativo-epo sun_type6` (:143-144). **Every declared variant compiles rc 0**
  (:146-157), including `br(abnt2)` (:147), which the registry does not advertise — so a "not in
  `xkbcli list`" answer is not a compile failure.
- Same split for layouts: `symbols/eu` exists and `--layout eu` compiles rc 0 (2084 lines) although the
  registry lists no `eu` layout (:159). Layout/variant names resolve against files, not against
  `rules/evdev.xml`.
- Options inventory (`rules/evdev.lst`): 217 names, `grp:*` 45, `compose:*` 19; `grp:alts_toggle` =
  "Both Alts together", `compose:caps` = "Caps Lock" (:160-164).
- Data pins for the entry (sha256, computed on this host, receipt:165-172): `symbols/br`
  `8cf65550…3bf35e`, `symbols/group` `d9627728…f220000`, `symbols/pc` `e2e1c150…9421794`,
  `symbols/us` `d70b84ee…aa2739`, `rules/evdev` `0cc48ee1…d12132`, `rules/evdev.xml` `d075cd21…9a23e1`,
  `rules/evdev.lst` `1a3406eb…ed9022`. Package versions read from pkg-config, not from a transaction:
  libxkbcommon 1.13.2, xkeyboard-config 2.48 (receipt:8-11).

### F5 — mapping onto Hyprland's fallback (held, cited, not re-claimed)

The compile is exactly the input to Hyprland's step 4: the five names are stored before the compile, and
"if no keymap results, the stored rules are reset to layout `us`" (`corpus/knowledge/hyprland-input-devices-r46.md:33`,
step 4; rows S318/S319 `:42-43` — `input:kb_layout` default `us` at `ConfigValues.cpp:272`, and
`m_currentRules.layout = "us";` at `IKeyboard.cpp:113` after a failed compile). Fed by F2, the mapping is:

- **rc 1 + empty stdout** (`XKB-338` unknown layout/rules, `XKB-661` unknown or misaligned variant) is the
  only shape that can reach the fallback: those names do not compile, so the keyboard can print `us` with
  empty variants/options although the config names something else — the `DIFFER`/`FALLBACK` reading rule at
  `hyprland-input-devices-r46.md:61`.
- **rc 0 with an error message** (`XKB-595` unknown option, `Less layouts than variants`) is *not* a
  fallback: the keymap compiles, the keyboard keeps `br`, and the bad option/variant silently disappears
  (byte-identical stdout, F2). A config typo in `kb_options` is invisible in `hyprctl devices -j`; a typo
  in `kb_layout`/`kb_variant` shows up as `us`. Diagnostics must read the rc, not the presence of a message.
- Unknown `kb_model` is inert on this host (rc 0, no message, identical keymap), so it cannot trigger the
  fallback either.

This closes the ground the round-46 entry left open at `hyprland-input-devices-r46.md:69` ("The XKB compile
itself is not reproduced") and the frontier line at `corpus/README.md:112`; it does **not** re-claim the
fallback itself, which stays at S318/S319.

### F6 — the compile's input set is environment-controlled; the receipt pins it and measures each knob

Raised as a hypothesis by peer SentHost-4 (`w1/SentHost.md` F4); every item below was re-run by this seat's
own probe, so the evidence is receipt §7 and not the peer file. The numeric log-level boundary (below 20
silent, 20 and above shown) is measured here independently and agrees with the peer's later ten-row sweep
(their `receipts/04-xkbcli-env.txt` §4); the symbolic `critical` row is also measured here.

| knob | observed (receipt) |
|---|---|
| caller's env at all | host RMLVO compiled under the ambient env and under `env -i` pinned env give the **same** sha `efd487a3…` (:175) — today, because this host's user xkb dirs are absent and no `XKB_*` var is set (:13) |
| `XKB_LOG_LEVEL` | suppresses or restores the `XKB-595` **message** only: numeric `0/3/5/10` (below 20) and `critical` → 0 stderr lines; `20`, `30`, `error`, `warning`, `none`, an unknown token, `debug` → message; rc 0 and `sha16=6ef2127653b0ca1a` in all 13 rows (:176-189) |
| `XKB_CONFIG_ROOT` | three different root strings for one host: unset → `/usr/share/xkeyboard-config-2`; `/nonexistent` → `/usr/share/X11/xkb`; an existing empty dir → that dir, where `rules/evdev` is missing and even a valid `--layout br` is rc 1 `XKB-338` (:190-194) |
| `XKB_CONFIG_EXTRA_PATH` | replaces the compiled-in `/etc/xkb` slot in the include chain, after `$HOME/.xkb` and before the root (:195-201) |
| `XKB_DEFAULT_{RULES,MODEL,LAYOUT,VARIANT,OPTIONS}` | **inert for `xkbcli`**: `XKB_DEFAULT_LAYOUT=zz`, `…RULES=nope`, `…OPTIONS=nope:nope` with `--layout br` give rc 0, 0 stderr lines and the baseline keymap (:202-204). The compositor reads these; this receipt does not exercise the compositor, so the entry must not read inertness here as inertness in Hyprland |

The empty-root row doubles as a positive assertion: **rc 0 means the root resolved**. When
`XKB_CONFIG_ROOT` names an empty directory even a valid `--layout br` is rc 1 `XKB-338
Couldn't find file "rules/evdev"` (:194), so a successful host compile is itself evidence that
`/usr/share/xkeyboard-config-2` was found — no need to quote an include-path list that carries scratch
paths once HOME is pinned.

What this costs the entry: the "unknown option is dropped **with a warning**" sentence must name the log
level (F2 qualification), and the "include paths searched" string must be quoted with the `XKB_CONFIG_ROOT`
state it was produced under. Both are already pinned in this probe, which is why the receipt is
reproducible on a machine whose user xkb dirs are later populated.

## Proposed SOURCES rows (for the entry owner; this seat wrote no corpus file)

Ids are free: the registry has 276 rows topping at S339. Proposed, in registry column order:

- `S340` — host xkeyboard-config 2.48 data set, `/usr/share/xkeyboard-config-2` (symbols/br
  `8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e`, rules/evdev.xml
  `d075cd216137780495984b9570d20434dc16ccd404a42065e3397a61939a23e1`, rules/evdev.lst
  `1a3406eb5243178870d3c27c1a70899eaeebf2270800eac27fa486ac25ed9022`, read 2026-10-26) — `dataset` —
  tier A — scope: which layout/variant/option names exist in the data the compiler reads — teaches: br
  declares 11 variants while evdev.xml advertises 8; `symbols/eu` is not a registry layout yet compiles;
  45 `grp:*` and 19 `compose:*` options — `mined`, opened 2026-10-26, recheck `on-release`,
  used-by `corpus/knowledge/xkb-keymap-compile-r48.md`.
- `S341` — libxkbcommon 1.13.2 `xkbcli compile-keymap` on this host (`/usr/bin/xkbcli` sha256
  `af42b0e68101722adab709a521ecaf4f52f27a4a1d355de8cc58a61c58a1bd1f`,
  `/usr/lib/xkbcommon/xkbcli-compile-keymap` sha256 `43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250`)
  — `deployment` — tier A — scope: RMLVO→KcCGST mapping, rc and first `XKB-###` for known/unknown names,
  include-path order and precedence, `--include`/`--include-defaults`, and the env knobs that change the
  answer (`XKB_LOG_LEVEL`, `XKB_CONFIG_ROOT`, `XKB_CONFIG_EXTRA_PATH`) — anchor:
  `.ufo/waves/round-48/w1/ExecXkbLive/receipts/xkb-live.txt` §2-§4 and §7 (208 lines,
  `a0c488c87301054c253098c23bcb75bca40360d305c704a47cb1639d193db618`), two runs identical apart from the
  date line, every xkbcli call under `env -i` — teaches: failure (`XKB-338`/`XKB-661`, rc 1) vs silent drop
  (`XKB-595`, rc 0, byte-identical keymap, message suppressible by log level) vs inert (`kb_model`,
  `XKB_DEFAULT_*`), variant-index alignment, variant overflow keeps the first, poisoned user dir outranks
  the root — `mined`, opened 2026-10-26, recheck `on-change` (dependency binary sha256), used-by
  `corpus/knowledge/xkb-keymap-compile-r48.md`.
- `S342` — host Hyprland keyboard RMLVO as configured, `~/.config/hypr/input.conf:10-11` (shape-only: the
  `kb_*` values and the commented alternates at `:5`, `:8`, `:11`) — `own-work` — tier A — scope: the
  concrete RMLVO the matrix was run for and what the live dump reports for it — anchor: receipt §1/§5,
  `hyprctl devices -j` 10 keyboards, one distinct tuple — teaches: config says `br`+`compose:caps`, the
  dump says `br`+`compose:caps`+"Portuguese (Brazil)", names replaced — `mined`, opened 2026-10-26,
  recheck `on-change`, used-by `corpus/knowledge/xkb-keymap-compile-r48.md`.

## Risks, limits, deviations

1. **No upstream source pin.** This receipt is binary behaviour on this host; the `XKB-###` meaning is
   cited only through the message text and the numeric code. If the entry states libxkbcommon internals
   (e.g. that `XKB-338` is `XKB_ERROR_INCLUDES`, or that the rules file is parsed before symbols), that
   needs a fetched pin of libxkbcommon 1.13.2 sources — not done in this seat.
2. **The fallback is not exercised live.** No `dispatch`/`keyword`/`reload`, so "the keyboard then prints
   `us`" remains sourced at S318/S319, never re-observed.
3. **Registry vs rules-XML.** Only `xkbcli list` and `rules/evdev.lst` were read; the XML's own grouping
   (which `<variant>` belongs to which `<layout>`) was inferred from the registry output. The 11-variant
   compile loop is the stronger evidence and is included.
4. **Guard deviation, disclosed.** Before switching to pkg-config metadata I ran two *read-only* package
   queries (`pacman -Qo /usr/bin/xkbcli`, `pacman -Q libxkbcommon xkeyboard-config`). No transaction, no
   sync, nothing installed; both matched the L1 host facts (1.13.2-1, 2.48-1). No further pacman call was
   made; the receipt pins versions from `/usr/lib/pkgconfig/xkbcommon.pc` and
   `/usr/share/pkgconfig/xkeyboard-config.pc`.
5. **Ghost ids.** `corpus/lessons/round-35.md:131,216` cite `S340`/`S342` although the registry has no such
   rows; the entry owner should open S340+ with that in mind (the lesson rows are a sweep table, not
   registry rows).
6. **Session material.** The receipt carries no device names, no home listing, no window titles; `$HOME`
   and the scratch path are rendered as literal `$HOME`/`$S` tokens (verified: `grep -c vgpnk` on the
   receipt = 0). Scratch removed; the only persistent artefacts are `probe.sh` and the receipt.
7. **The stray `tree.json` in the fleet root was not this seat.** This seat wrote exactly three paths, all
   absolute: `.ufo/waves/round-48/w1/ExecXkbLive/probe.sh`,
   `.ufo/waves/round-48/w1/ExecXkbLive/receipts/xkb-live.txt` and this report; `probe.sh` writes only
   `$SEAT/receipts/xkb-live.txt` and a `mktemp -d` under `/fast/scratch/hyaku/mado-r48/ExecXkbLive`, with
   no relative-path output (`find` on the fleet root shows no `tree.json` and no seat artefact outside the
   seat dir).
8. **Environment-controlled inputs.** The compile's input set is not only the flags: `XKB_LOG_LEVEL`,
   `XKB_CONFIG_ROOT`, `XKB_CONFIG_EXTRA_PATH` and the user xkb dirs change the message, the root string, or
   the tree that answers a name. This probe pins all of them (`env -i`, scratch HOME/XDG) and §7 measures
   each knob, so the receipt stays reproducible if this host's `~/.config/xkb` or `~/.xkb` is ever created —
   the ambient-equals-pinned result (:175) is a today-fact, not a guarantee. The hypothesis was raised by
   peer SentHost-4 (`w1/SentHost.md` F4); every row in §7 was re-run by this seat, so the evidence cited is
   the receipt, not the peer file.

## Tooling

Nothing installed or upgraded (no pacman transaction, no uv/npx/cargo/npm). Tools used as shipped:
`xkbcli` 1.13.2, `hyprctl` (Hyprland 0.56.2), coreutils, `python3` (stdlib only, for the `devices -j`
projection).
