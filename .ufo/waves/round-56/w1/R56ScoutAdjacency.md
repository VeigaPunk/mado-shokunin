# R56ScoutAdjacency — read-only adjacency scan (round 56, wave w1)

Seat: R56ScoutAdjacency (leaf; no subagents). Date: 2026-10-28. Scope: sibling lanes under
`/home/vgpnk/Projects/shokunin/*-shokunin` (mado-shokunin excluded) + `/home/vgpnk/Projects/kimi-shokunin`,
then mado `corpus/knowledge` at the pinned base rev `13f0acbe3a15da2d9c08357a576d91dcadc85273`.
Read-only throughout: no lane/sibling file edited, no git mutation, no hyprctl call, no tool installed
(the 2026-10-19 tooling authorization was not exercised — nothing was needed). Scratch
`/fast/scratch/hyaku/mado-r56/R56ScoutAdjacency/` was used only as command cwd and removed before yield.

## 1. Method — sibling sweeps (one `grep -rIl` per term)

Path list (identical all five sweeps; `D=` below):
the 20 sibling lanes `audio- chousa- game-dev-2d- game-dev-3d- kagi- kaidoku- kake- kama- kasegi- kengaku-
kotoba- kotodama- kumitate- lore- mori- revenger- souji- tabi- tameshi- tsukuroi-shokunin` under
`/home/vgpnk/Projects/shokunin/`, plus `/home/vgpnk/Projects/kimi-shokunin`. mado-shokunin excluded per spec.

```
grep -rIl -iE 'auto-?reload'      --exclude-dir=.git $D   # term "Hyprland config auto-reload" (hyphen/no-hyphen variants)
grep -rIl -i    'inotify'         --exclude-dir=.git $D   # term "inotify"
grep -rIl -i    'config reload'   --exclude-dir=.git $D   # term "config reload"
grep -rIl -i    'hyprctl reload'  --exclude-dir=.git $D   # term "hyprctl reload"
grep -rIl -i    'disable_autoreload' --exclude-dir=.git $D # term "disable_autoreload"
```

Raw hit lists saved as `sweep1-autoreload.txt` … `sweep5-disable_autoreload.txt` beside this report
(all five `.err` files are 0 bytes — no grep errors). Results:

| term | files hit | substantive corpus knowledge? |
|---|---|---|
| `auto-?reload` | 11 (chousa 4, kaidoku 4, kama 1, souji 2) | **No.** All are Devin provider-error logs or fetch caches: the JSON hits match the quota string “…to purchase on-demand usage or **turn on auto-reload**.” (verified by `grep -rioE '.{0,40}auto-?reload.{0,40}'`, 4/4 files identical boilerplate); kama’s hit is a fetched Prometheus blackbox-exporter README (`--config.enable-auto-reload`), a wave fetch cache, not lane knowledge. |
| `inotify` | ~150 (mori, tsukuroi, kama, kengaku, kotoba, souji, kagi, kaidoku, game-dev-3d, chousa, kumitate, tabi, tameshi) | Partly — see §2. Corpus-level: mori (systemd cgroup inotify), tsukuroi (inotifywait boot watcher). Rest is wave artifacts, vendored `node_modules` (kagi chokidar/node-gyp), fetched man pages/API dumps, harness scripts. |
| `config reload` | 4 (kagi 3, kotoba 1) | No — release-changelog bodies and `omp-live` binary strings. |
| `hyprctl reload` | **0** | — |
| `disable_autoreload` | **0** | — |

kimi-shokunin exists and was included in every sweep; it contributed **zero** hits on all five terms.
Note: sweeps ran over sibling **working trees** (untracked `.ufo/` wave artifacts included), so hit lists are
point-in-time and artifact-heavy; classification below separates the two.

## 2. Sibling classification — does anyone hold the surface?

No sibling holds the Hyprland config auto-reload surface. The two zero-hit terms (`hyprctl reload`,
`disable_autoreload`) are the C1 mechanism's own verbs and flag. Closest adjacent ground, by lane:

- **mori-shokunin** — owns *inotify as used by systemd cgroup accounting*: `corpus/knowledge/journal-alarm-routing-r14.md:61-62,144-146`
  (“the inotify watch additionally requires memory accounting… Slice units are not inotify-watched (`src/core/cgroup.c:2077-2078`)”)
  and `oom-evidence-loss-r38.md:49,78` (inotify `IN_MODIFY` / poll `POLLPRI` notification for `memory.events`, sourced S232,
  a tier-B gihyo.jp article). Inotify-on-procfiles semantics — different watch target, no config-tree watching, no Hyprland.
- **tsukuroi-shokunin** — owns *inotify-tools at boot*: `corpus/knowledge/boot-writers-r19.md:30,143` (`limine-snapper-watcher`
  uses `inotifywait`; fallback when absent), `corpus/SOURCES.md:43` (S037 omarchy issue #6629 “missing inotify-tools”), `SKILL.md:2021,2032,2051`.
  External watcher tooling, not in-Hyprland registration.
- **kama-shokunin** — wave artifacts only (not corpus): r50 `X8WitnessPort/watch.py` (libc inotify via ctypes on a witness dir)
  and r51 `J3CopyDecoy` (measured `CLOSE_WRITE`/`CREATE`/`MOVED_TO` on tar extraction). Methodological precedent for observing
  inotify event streams on this fleet, but about tar-replay witness dirs — no overlap with config-watch mechanics.
- **kengaku-shokunin** — passing mention only (`r14-scout-surfaces.md:343` “no inotify trace exists”).

Verdict on contested ground: none contested. mado owns Hyprland config auto-reload uncontested; the neighbourhood
treats inotify only for cgroup counters (mori) and boot-watcher tooling (tsukuroi). Those lanes keep their ground;
mado should not absorb them — a cross-reference pointer in the new entry's prose (not a registry row) is the most
that is warranted.

## 3. Mado `corpus/knowledge` mentions at base

Seat-specified command (run verbatim):

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -n -iE 'reload' 13f0acbe3a15da2d9c08357a576d91dcadc85273 -- corpus/knowledge | head -60
```

→ **99 matching lines in 28 files**; the spec's `head -60` shows the first 60, lines 61-99 retrieved separately
(full output: `mado-corpus-reload-grep.txt`, per-file counts: `mado-corpus-reload-counts.txt`, both beside this report).
Classification of every file (sourced claim / passing mention / open note, judged on the matched lines in context):

**Sourced claims — but about other surfaces or the reload *verb*, never the file-watch mechanism:**

| file:lines | claim | surface |
|---|---|---|
| `terminals-and-omarchy.md:131-132` | omarchy `SKILL.md:145` says Hyprland config has “auto-reload on save”; validate via `hyprctl reload` + `hyprctl configerrors` (`:147-148`); waybar does NOT auto-reload (`:159`) | **closest existing mention of Hyprland auto-reload itself** — a citation of omarchy's skill doc, no Hyprland source, no inotify/watch list/`disable_autoreload` |
| `config-drift-r12.md:67-68` | gkeep `install.sh:88-90` invokes `hyprctl reload` then `hyprctl configerrors`; “read, not executed” | hyprctl reload as installer apply/validate verb (own-work git read) |
| `rule-attribution-r24.md:155` | “Named rules first is the hyprlang reload order (`reloadRules`, `legacy/ConfigManager.cpp:946-966`)” | reload *ordering* internals, not the trigger |
| `hyprland-bind-key-match-r50.md:63,80` | xkb translation state rebuilt “after config reload” | downstream effect of a reload |
| `hyprland-keyboard-repeat-numlock-r55.md:26` | options re-applied on reload; legacy reload path callers (wave-2 pointer, not a lane row) | downstream effect |
| `output-colour-boundaries-r14.md:41` | `scheduleReload()` before later test/apply | output-config internal |
| `terminal-trees-r23.md` (10 lines) | foot: no runtime reload (S141-S149); kitty: `auto_reload_config` + F5 + SIGUSR1 (S123-S129); ghostty: keybind + SIGUSR2, **zero** `FileMonitor`/`inotify_init`/`GFileMonitor` occurrences (S139) | other apps' reload semantics — methodological precedent, not Hyprland |
| `terminal-route-r17.md:72,119` | alacritty `live_config_reload` default true; host file lacks the key | other app |
| `walker-deep-r9.md` (36), `walker-deep.md:163,454,512`, `walker-route-r18.md:77,96` | walker: no reload verb/D-Bus method/`CanReload=no`/no watch token; 2.17.2 tree has no `reload_config` | other app (dominant file of the sweep) |
| `waybar-walker-semantics.md:72,364`, `waybar-walker-plane.md:49,324` | waybar `reload_style_on_change: true` — style only, modules need restart | other app |
| `arc-synthesis.md:228-229`, `closeout-r11.md:43` | same walker/waybar rows, ledger form | other app |
| `terminals-and-omarchy.md:97` | `omarchy restart terminal` “Reload supported terminal emulators” | other app |

**Open notes (explicit [UNK]/not-investigated):**

- `hyprctl-getoption-native-forms-r40.md:88` — how a runtime `hyprctl keyword` override interacts with a reload: explicitly outside.
- `keybind-rule-semantics.md:267` — “config-reload history, or dynamic re-evaluation sequencing — not investigated”.
- `arc-synthesis.md:396`, `closeout-r11.md:302` — walker 2.17.2 binary live-reload behaviour [UNK].
- `terminal-route-r17.md:146-147` — alacritty reload effects on this host [UNK].
- `remaining-planes-census.md:271-272` — how swaybg is asked to reload on theme change: open.
- `walker-deep-r9.md:359` — live-reload discriminator listed among open discriminators.

**Passing mentions (safety boundaries / “nothing was reloaded” statements):** `config-health-report-r3.md:25,607`,
`hyprctl-verification-layer.md:15,236`, `input-debugging-boundaries-r15.md:77` (reload = mutation class),
`hyprland-config-era-r12.md:105,121`, `hyprland-dispatcher-dispatch-r51.md:284`, `rule-attribution-r24.md:91`,
`output-colour-boundaries-r14.md:91`, `config-drift-r12.md:110`, `config-option-table-r39.md:123`,
`hyprland-gkeep-geometry-r43.md:83`, `theme-route-r18.md:10`, `xkb-keymap-compile-r48.md:111`,
`terminal-trees-r23.md:110,112-113`, `wayland-protocol-boundaries-r13.md:43`, `arc-synthesis.md:228` (waybar row),
`walker-deep-r9.md` binary-token rows (`:175-178` etc.).

**Special case worth the wave's attention:** `config-health-report-r3.md:353` — an operator recommendation says
“add `source = ~/.config/hypr/envs.conf` … (**auto-reload applies it on save**…)”. The lane has previously *relied* on
Hyprland auto-reload as an assumed apply path without any mechanism entry behind it — exactly the gap C1 closes.
It is a passing mention today; the new r56 entry can cite it as motivation, not as source.

Corroboration: the frozen C1 before-census (0 hits for `disable_autoreload|ConfigWatcher|IN_CLOSE_WRITE|inotify_add_watch`
in `corpus/knowledge`) is consistent with this broader `reload` sweep — 99 mentions, all other-app semantics, reload-verb
boundaries, or downstream effects; zero mechanism coverage. Nothing in mado's own corpus contests C1's “surface moved”.

## 4. Ownership

Uncontested: **mado owns the Hyprland config auto-reload surface** (declaration → `CConfigWatcher` → inotify watches →
`CConfigManager::reload` → `hyprctl reload`, plus `misc:disable_autoreload`). No sibling has any hit on the mechanism
terms; sibling inotify ground (mori: cgroup counters; tsukuroi: inotifywait boot watcher; kama: wave-tooling event labs)
is distinct and stays with them. Report-not-absorb: nothing from siblings was copied into the lane; only pointers above.

## 5. Proposed adjacency record line

> `adjacency r56w1 scout (R56ScoutAdjacency): 20 sibling lanes + kimi swept read-only (grep -rIl, 5 terms): hyprctl reload=0, disable_autoreload=0; auto-reload=11 files all incidental (Devin quota strings, blackbox-exporter fetch cache); config reload=4 incidental (changelogs/strings); inotify≈150 files, corpus-level only mori (cgroup memory.events IN_MODIFY/POLLPRI, S232) and tsukuroi (inotifywait boot watcher, S037), kama r50-r51 wave labs — none Hyprland. Mado corpus/knowledge 'reload' at base 13f0acbe = 99 lines / 28 files: other-app reload semantics (walker 40, terminals 16, waybar 4), reload-verb safety boundaries, downstream effects, open [UNK]s — zero mechanism coverage of config auto-reload / watch list / disable_autoreload; nearest items: terminals-and-omarchy.md:131 (omarchy SKILL 'auto-reload on save' citation), config-health-report-r3.md:353 (recommendation assumes auto-reload applies on save, unbacked), config-drift-r12.md:67 (hyprctl reload in gkeep installer, read not executed). Surface uncontested — mado owns it.`

## 6. Defects / ambiguities in the input

1. **Seat command truncates its own output**: the specified `… | head -60` hides 39 of 99 matching lines. Reported both
   counts; full list archived. (No disagreement found between seat text and registration.md; the frozen claims file's
   narrower before-census is likewise 0 and unaffected.)
2. **`auto-?reload` regex choice**: the seat's term “Hyprland config auto-reload” has no byte-stable form; I swept the
   case-insensitive variant class `auto-?reload` (covers `auto-reload`/`autoreload`; `auto_reload` in code would also
   match `-iE` only with `[._-]?` — not swept; the `disable_autoreload` sweep covers the flag's own spelling). Documented
   as a judgment call, not a spec deviation.
3. **Working-tree sweeps**: sibling `.ufo/` wave artifacts and vendored `node_modules` are in the hit lists; a
   corpus-knowledge-only sweep would be cleaner but the spec asked for repo-wide `grep -rIl`. Both views given.
4. Devin-quota JSONs match `auto-?reload` only inside the provider error string “…turn on auto-reload.” — verified by
   token extraction, so no sibling has a real auto-reload claim hiding in those files.

## 7. Not verified / not run

- Sibling repos were read at working-tree state, not at pinned revisions — hit lists are point-in-time.
- The ~150 `inotify` artifact hits were classified by path/content class with spot-checks of the corpus-level and
  named-artifact files only; fetched man pages/API dumps/node_modules were not read line-by-line.
- No host reads (`hyprctl`, `~/.config/hypr`) were made — out of this seat's scope.
- Hold-out sealed: no H01-H08 path or file was sought or seen.

## 8. Deliverables

- Report: `.ufo/waves/round-56/w1/R56ScoutAdjacency.md` (this file)
- Evidence (same seat dir): `sweep1-autoreload.txt`, `sweep2-inotify.txt`, `sweep3-config-reload.txt`,
  `sweep4-hyprctl-reload.txt` (empty — 0 hits), `sweep5-disable_autoreload.txt` (empty — 0 hits),
  `mado-corpus-reload-grep.txt` (99 lines), `mado-corpus-reload-counts.txt` (28 files)
- Scratch `/fast/scratch/hyaku/mado-r56/R56ScoutAdjacency/` removed before yield.
