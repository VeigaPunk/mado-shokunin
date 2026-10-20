# AttackReadmeRows — round-17 Coverage-map rows and Frontier bullet

Target: `corpus/README.md` at lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`
(pushed) — rows `:42` (`idle-lock-route-r17.md`, surface P6) and `:43`
(`terminal-route-r17.md`, surface P4), and the round-17 Frontier bullet
`:119-125`. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Method: byte reads only (`cat -n`, `sed`, `grep`, `sha256sum`, `stat`, `wc`),
`git show|log|diff|ls-tree` (read verbs), `python3 -I measure.py`, the allowed
`sources-census.sh validate`, and `curl` of raw upstream bytes. No host probe,
no compositor/input/service/package command, no `sudo`/`pacman` in any form, no
git mutation. Installs: **none**.

A concurrent, uncommitted peer edit appeared mid-review (mtimes
`11:56:37-11:56:52 -0300`) touching `corpus/README.md`, `corpus/SOURCES.md`
(new `S071`), `corpus/knowledge/terminal-route-r17.md`, and
`corpus/lessons/round-17.md`. HEAD findings below were read from
`git show HEAD:<path>`; the worktree is called out separately.

## Verdict

The attack **fails on links, behaviour-freedom, and S-id range correctness at
HEAD**. It **succeeds on one scope claim**: the Frontier bullet
(`:119-121`) says "P4 terminal-emulator configs" moved onto sourced ground,
while the terminal note explicitly limits itself to Alacritty
(`terminal-route-r17.md:16`: "it covers Alacritty only, not foot, kitty or
ghostty"). Three low/informational issues remain around source binding and
version-pin compression.

## Checks run

### 1. Links resolve — pass

Every Markdown link in the two rows and the bullet resolves against
`corpus/`:

| line | target | exists |
|---|---|---|
| `README:42` | `SOURCES.md` | yes |
| `README:42` | `knowledge/idle-lock-plane.md` | yes (§11 at `idle-lock-plane.md:327`, heading `## 11. Unknowns`) |
| `README:43` | `SOURCES.md` | yes |
| `README:120` | `knowledge/idle-lock-route-r17.md` | yes |
| `README:121` | `knowledge/terminal-route-r17.md` | yes |

The note names in column 1 are backticked, not linked, matching every other
Coverage-map row (e.g. the round-16 row). No dangling link.

### 2. Claims match the notes — pass at HEAD, one scope exception in the bullet

| README phrase | note anchor | result |
|---|---|---|
| idle: "hypridle v0.1.8 and hyprlock v0.9.6" | `idle-lock-route-r17.md:27-29` tag selection; S065-S069 tag-pinned | tags live: `github.com/hyprwm/hypridle/releases/latest` → `tag/v0.1.8`; `hyprlock/releases/latest` → `tag/v0.9.6` |
| idle: "(listener timeouts, lock/sleep hooks, inhibit)" | `:31-62` (General keys, Listeners), `:54-62` (hyprlock) | matches |
| idle: "joined to the host's declared files by sha256 and line anchor" | `:64-105` Host declaration; all 8 hashes and cited lines re-checked | 8/8 hashes match disk; anchors match (see §4) |
| idle: "transitions and lock success stay `[UNK]`" | `:122-134` Unexercised behavior | matches |
| idle: "open unknowns in idle-lock-plane.md §11" | `:11-14` points at §11; §11 exists | matches |
| idle: "No lock, suspend or listener is triggered" | `:9-12` "no listener has fired, no lock has been taken"; `:111-120` prohibited probes | matches |
| P4 row: "Hyprland launch binding" | `terminal-route-r17.md:69`; `bindings.conf:2-3` | matches |
| P4 row: "`xdg-terminal-exec` v0.14.3" | `:18-49`; S056/S057 | raw bytes hash to SOURCES values |
| P4 row: "`xdg-terminals.list` (first entry `Alacritty.desktop`)" | `:70`; file lines 1-2 comments, line 3 entry | matches |
| P4 row: "Alacritty v0.17.0 config-import contract" | `:51-62`; S058 | tag live; `alacritty.5.scd` hash matches |
| P4 row: "Which terminal actually launches and reload effects stay `[UNK]`" | `:109-124` | matches (launch vs selection distinction preserved) |
| P4 row: "No terminal is launched" | `:12` "No terminal, launcher or compositor was run" | matches |

**Scope exception (finding F1).** Frontier bullet `:119-121` uses the raw
surface label "P4 terminal-emulator configs". SCORECARD `:843-844` defines P4
as "terminal-emulator configs", and PROVINCE `:7-8` owns
`~/.config/alacritty|foot|kitty|ghostty/`. All four trees exist
(`alacritty.toml` 876 B, `foot.ini` 516 B, `kitty.conf` 954 B,
`ghostty/config` 1325 B), and the note states at `:16` that it covers
Alacritty only. The Coverage-map row `:43` is correctly narrowed ("to the
Alacritty v0.17.0 config-import contract"); the Frontier bullet is not. The
following clause ("Alacritty reload effects") partially disambiguates but does
not withdraw the surface-wide first sentence. This is the concrete
claim-vs-note mismatch in scope. AttackP4Claims §Counterexample 5 independently
reached the same reading; I verified it from the note line and the rubric text.

### 3. No behaviour claim — pass

- Idle row: "Documentary upstream contract"; "Declared timings are not
  observed behaviour"; "transitions and lock success stay `[UNK]`"; "No lock,
  suspend or listener is triggered."
- P4 row: "Documentary route"; "Which terminal actually launches and reload
  effects stay `[UNK]`"; "No terminal is launched."
- Frontier bullet: "**documentary** sourced ground"; the still-open list names
  transitions, listener firing, lock success, stop-cause, actual launch,
  reload effects; "Host binaries stay `[UNK]`".
- `idle-lock-route-r17.md:9-12` and `terminal-route-r17.md:9-12` each disclaim
  observed behaviour in their own words.

No present-tense host-health or act-executed claim is inherited by the rows.

### 4. S-id ranges — pass at HEAD

Parsed `corpus/SOURCES.md` (70 registry rows at HEAD):

| range | status/tier | used-by |
|---|---|---|
| S056-S060 | all `mined`, tier A | `corpus/knowledge/terminal-route-r17.md` |
| S063-S069 | all `mined`, tier A | `corpus/knowledge/idle-lock-route-r17.md` |
| S061, S062 | `rejected`, tier C | — |
| S070 | `rejected`, tier C | — |

Contiguous, no gaps. The notes' first lines cite exactly those sets at HEAD
(`terminal-route-r17.md:1` → S056-S060; `idle-lock-route-r17.md:1` →
S063-S069). Rejected rows are omitted from the README ranges, as in the
round-14 row's admitted-only convention (`README:39` omits mined S049, whose
`used-by` is a different entry). `measure.py 988b858` returns C2 count **4**
(P1, P2, P4, P6 true; P3, P5 false), matching the Frontier bullet's
"P3 Walker and P5 theme/wallpaper sourced routes" open list and the declared
4/6 target. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin
mado` → `ok` (only pre-existing W04 duplicate warnings for S030/S042/S045).

### 5. Upstream pins behind the version words — pass

Re-fetched with `curl`, sha256 compared to `SOURCES.md`:

| source | sha256 | SOURCES |
|---|---|---|
| xdg-terminal-exec v0.14.3 README | `c7a1a8bb…a9d40` | S056 match |
| xdg-terminal-exec v0.14.3 script | `89f2be9a…27ac` | S057 match |
| alacritty v0.17.0 `alacritty.5.scd` | `e444fa45…4107` | S058 match |
| hypridle wiki | `b45c03dc…f640` | S063 match |
| hyprlock wiki | `f69cff6b…abf5` | S064 match |
| hypridle v0.1.8 README | `f5b852ee…81f6` | S065 match |
| hypridle v0.1.8 `Hypridle.cpp` | `2dd4d73d…2d75` | S066 match |
| hypridle v0.1.8 `Hypridle.hpp` | `f9e4e558…a2b8` | S067 match |
| hypridle v0.1.8 `main.cpp` | `379bf321…2a38` | S068 match |
| hyprlock v0.9.6 README | `83096def…50f3` | S069 match |
| system `xdg-terminals.list` (host + upstream) | `a2b5bf69…f034`, 1053 B | S060 match |

Host hashes also re-checked: idle 8/8 (`hypridle.conf` `e7d3b8dd…`, `hyprlock.conf`
`b8d173dc…`, theme `3ef010e7…`, three omarchy scripts, default autostart,
`hyprland.conf` `ce7483f3…`); P4 4/4 named files (`bindings.conf` `e574a1ed…`,
`xdg-terminals.list` `d035da57…`, `alacritty.toml` `695301c8…`,
`Alacritty.desktop` `713703ba…`) plus theme import `8c3d1457…`.

## Findings

### F1 — Medium — Frontier bullet overstates P4 scope

`README:119-121` claims P4 terminal-emulator configs moved onto sourced
ground; `terminal-route-r17.md:16` says "it covers Alacritty only, not foot,
kitty or ghostty". P4 is the four-tree surface (`SCORECARD:844`,
`PROVINCE:7-8`), all four trees exist, and only Alacritty has a route. The
Coverage-map row is scoped correctly; the bullet should say e.g. "P4 terminal
configs (Alacritty route only; foot/kitty/ghostty unsourced)". Wording only —
no count change and no behaviour claim. This is the one substantive
claim-vs-note counterexample.

### F2 — Low — At HEAD, `Alacritty.desktop` is named "by sha256" but bound to no S row

`README:43` names three host bytes; S059 (`SOURCES.md:71`) enumerates
`bindings.conf`, `xdg-terminals.list`, `alacritty.toml`, the theme import and
the `.bak`, but not the desktop entry. `grep 713703ba corpus/SOURCES.md` at
HEAD = 0 hits; the digest lives only at
`terminal-route-r17.md:74`. The row is not false (the digest matches disk at
`~/.local/share/applications/Alacritty.desktop`, `713703ba…`), but the Sources
cell `S056–S060` does not cover one of the three host bytes it names. The
concurrent worktree edit fixes exactly this with S071; S071 verifies: row at
worktree `SOURCES.md:83`, `used-by` names the note, digest `713703ba…` matches
disk, anchors `:7` (`Categories=System;TerminalEmulator;`) and `:14-17`
(`X-TerminalArg*`) match, and the file is byte-identical to
`~/.local/share/omarchy/applications/Alacritty.desktop`.

### F3 — Low — The in-flight S071 correction leaves the note's own source accounting stale

At worktree mtime `11:56:52 -0300`, `terminal-route-r17.md:1` and
`README:43` cite S071, but `:2` (`verified-at`) still says "SHA-256 values …
in corpus/SOURCES.md S056-S060" and `:132` still says "Source rows: …
S056-S060 (mined) and S061-S062 (rejected)". If committed as-is, the README
row's S range outruns the note's footer/verification pointer. Add S071 to
`:2` and `:132` before commit.

### F4 — Informational — Idle row compresses the note's wiki-unpinned caveat

`README:42` says "for hypridle v0.1.8 and hyprlock v0.9.6".
`idle-lock-route-r17.md:130` keeps `[UNK]` "Whether the wiki ("Latest git",
last updated 2026-08-26) matches the v0.1.8 and v0.9.6 tag bytes", and `:131`
says hyprlock source was not opened (wiki and README only). S063's scope
(`SOURCES.md:75`) explicitly says "not version-pinned to v0.1.8". The row is
true about the target versions (both tags verified live) and the source cell
points at S063/S064, which carry the caveat; a reader who stops at the row
could over-read pinning, especially for hyprlock keys. Not a false statement,
not behaviour.

### F5 — Nit — `surface P6` / `surface P4` tokens are undefined in the README chain

The only definition of P1-P6 is `SCORECARD.md:843-844`. `README` does not define
them and its Province-routes scope link points at `PROVINCE.md`, which lists
surfaces descriptively without P numbers. The Frontier bullet spells out P3/P5
("Walker", "theme/wallpaper") and P6/P4 in prose, so the labels are inferable
there; the two row labels are opaque without SCORECARD. Navigation nit only.

### F6 — Informational — "Host binaries stay `[UNK]`" is conservative but overbroad for the P4 script

`/usr/bin/xdg-terminal-exec` is a POSIX shell script, 44020 B, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` — byte-
identical to the v0.14.3 tag script (S057). That route's installed executable
identity is observed by file read, not `[UNK]`; the compiled
`hypridle`/`hyprlock`/`alacritty` binaries remain `[UNK]` (no tag-binary
binding). If "binaries" means compiled ELFs, the sentence is correct; if it
covers the script, it under-claims. The note's own version bullet
(`terminal-route-r17.md:114-119`) has the same nuance. Not an overclaim.

## Residual risk and verification gaps

- Wiki S063/S064 have no tag commit; their pages are "Latest git". The row's
  version words therefore inherit the note's `[UNK]` wiki/tag equivalence for
  hyprlock key/default claims even though the wiki bytes re-fetched byte-equal
  today (`b45c03dc…`, `f69cff6b…`).
- `terminal-route-r17.md:16` scopes to Alacritty, but the note's `surface: P4`
  line cannot carry a qualifier without breaking `measure.py`'s exact
  `surface: P<n>` match (`measure.py:187-188`). A scope qualifier must live on
  another head line or in README/SCORECARD prose; that is a rubric-shape
  constraint, not a README text defect.
- Alacritty's installed ELF is not byte-joinable to the v0.17.0 man page;
  `[UNK]` for the running Alacritty binary is correct.
- The worktree is a moving target. F2/F3 are stated against HEAD `988b858`
  and worktree state at `11:56:37-11:56:52`; re-run `git diff` before commit.
- No live idle/lock/terminal/compositor probe was made; none is needed for
  these documentary claims.

## Reproduction commands

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git show HEAD:corpus/README.md | sed -n '42,43p;119,125p'
git show HEAD:corpus/knowledge/idle-lock-route-r17.md | sed -n '1p;26,29p;64,105p;122,134p'
git show HEAD:corpus/knowledge/terminal-route-r17.md | sed -n '1p;16p;64,78p;109,124p'
grep -nE '^\| S0(5[6-9]|6[0-9]|70)' corpus/SOURCES.md
python3 .ufo/waves/round-17/measure.py 988b858
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
# host hashes
sha256sum ~/.config/hypr/hypridle.conf ~/.config/hypr/hyprlock.conf \
  ~/.config/omarchy/current/theme/hyprlock.conf ~/.config/hypr/bindings.conf \
  ~/.config/xdg-terminals.list ~/.config/alacritty/alacritty.toml \
  ~/.local/share/applications/Alacritty.desktop
# upstream pins
curl -fsSL https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md | sha256sum
curl -fsSL https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec | sha256sum
curl -fsSL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | sha256sum
curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md | sha256sum
curl -fsSL https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd | sha256sum
```
