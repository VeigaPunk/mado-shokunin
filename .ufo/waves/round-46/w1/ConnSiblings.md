# ConnSiblings — mado round 46 w1 (input-device plane adjacency survey)

Seat: ConnSiblings (leaf). Date: 2026-10-26.
Task: read sibling lanes' PROVINCE.md (read-only), grep their corpora for
keyboard layout / xkb / input devices / hyprctl devices; report overlap with
mado's C2 entry, who owns what, and contested scope.

## Verdict

**No sibling lane claims or covers the Hyprland input-device plane.**
mado-shokunin owns it outright this round. The one live adjacency is the
already-adjudicated mado↔tsukuroi boundary (config semantics vs kernel/driver
hardware plane); round 46 is the first round mado grounds this plane, so no
sibling content overlaps S316-S325, no sibling SOURCES row collides with the
ten pins, and no sibling tool name collides with `tools/mado-devices.py`.

## What mado's C2 entry covers (the surveyed target)

`corpus/knowledge/hyprland-input-devices-r46.md` (L1 draft
`.ufo/waves/round-46/l1-draft/entry.md`), rows S316-S325: the chain from
`input { kb_* }` / `device { name = X ... }` config through hyprlang 0.6.8
parsing and Hyprland 0.56.2 per-device resolution to the keyboard XKB names
and pointer `scrollFactor` printed by `hyprctl devices -j`; plus virtual
keyboards (`hl-virtual-keyboard*`) and device-name normalization. Ten pins,
all under `raw.githubusercontent.com/hyprwm/{Hyprland,hyprlang,hyprland-wiki}`
at fixed revisions.

## Sibling corpus sweep (all 19 siblings, read-only)

Searched every `*-shokunin` corpus for: `hyprctl devices`, `kb_layout`,
`xkb`/`XKB`, `keyboard layout`, `keymap`, `scroll_factor`, `input device`,
`hyprland|hyprlang|xkbcommon`, `wayland|compositor`, `fcitx|libinput|
switchxkblayout`, and each lane's SOURCES.md for `hyprwm|hyprland|hyprlang|
xkbcommon` URL rows. Results:

- **Zero semantic hits.** No sibling corpus explains, measures or claims
  Hyprland input-device behavior, XKB name resolution, or `hyprctl devices`.
  All `xkb`/`keymap` hits are foreign to this plane: `libxkbcommon.so.0`
  library loads in audio-shokunin strace logs (e.g.
  `audio-shokunin/corpus/live/r73-boundary/logs/strace-mpv-file.log:84`),
  nvim runtime keymap files inside kaidoku-shokunin firmware-extraction
  evidence (`corpus/evidence/round-36/c1/K3/oracle.tsv:1028`), readline
  keymaps in chousa-shokunin's captured bash(1) man page
  (`.ufo/waves/round-35/w2/ScoutManBash/bash.1:7150`), sox `--keymap` in
  audio-shokunin's `sox_ng.c.txt:2068`.
- **Zero source-registry collisions.** Sibling `corpus/SOURCES.md` files
  (kaidoku, audio, game-dev-2d, game-dev-3d, lore, revenger, kasegi, chousa)
  hold **0** rows matching hyprwm/hyprland/hyprlang/xkbcommon. The only URL
  repeats of the ten pins are mado's own held rows (S317=S162/S303 legacy
  ConfigManager.cpp, S320=S158/S307 HyprCtl.cpp, S324=S173 hyprlang
  config.cpp, S321=S182 MiscFunctions.cpp, S319=S215 ConfigValues.cpp) —
  already declared W04 census warnings in the frozen registration.
- **Zero tool-name collision.** No sibling tracks a `*devices*` tool
  (`find */tools -name '*device*'` outside mado: none). mado's own
  `mado-binds.py` (keybind plane) is already disambiguated from kumitate's
  bwrap "binds" (`kumitate-shokunin/corpus/knowledge/counter-amendment-discipline.md:82`,
  `mount-order-and-bind-scope.md:15`); "devices" is unclaimed.

## Who owns what (PROVINCE-level)

- **mado-shokunin** owns the plane: `PROVINCE.md:6` — `~/.config/hypr/`
  (hyprland.conf, keybinds, rules, animations), waybar, walker, terminals;
  "Never mutates a running compositor state; every claim is file-byte- or
  screenshot-verified." The round-46 registration extends the allowed
  read-only compositor verbs to `hyprctl devices -j`; C1's counter even bans
  running `libinput`/`udevadm`/`journalctl` — the tool is config-plus-dump
  join only. Recorded at tsukuroi's adjacency anchors:
  `tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.md:84` (OUT-004).
- **tsukuroi-shokunin** owns the kernel/driver/input-hardware plane:
  `PROVINCE.md:11-14` (package state, systemd, journal/boot triage,
  driver/firmware). Its ADJ-03 routing row (`PROVINCE.md:48`) sends
  "configuration-level diagnosis" of desktop behavior to mado. The
  boundary was adjudicated in round 19:
  `tsukuroi-shokunin/.ufo/waves/round-19/falsify/FxInRes03.md:32` — the
   round-13 sibling-overlap claim that tsukuroi covers `/dev/input/event*`,
  `evtest`, `libinput debug-events` was narrowed: mado's
  "PROVINCE.md:6-9 does not list input devices"; kernel/driver belongs to
  tsukuroi, configuration-level desktop behavior routes to mado.
- tsukuroi's actual libinput corpus content is package-state only:
  `partial-upgrade-recheck-r15.md:5-25` (libinput 1.31.3-1→1.32.0-1 logged
  transaction), `pause-lift-gate-r24.md:27-32` (P2: no partial-upgrade
  residue; 1.32.0-1 installed and in sync), and round-15
  `AttackIncidentCause.md:18-20` (libinput udev callouts/quirks as kernel
  plane). No config-semantics overlap with S316-S325.
- All other lanes are farther out: tabi (browser craft) touches Hyprland
  only as process forensics (`corpus/knowledge/hygiene-sweep-r4.md:114-127`
  — session OOM/SIGSEGV); mori (observability) records the OOM kill inside
  `app-Hyprland-xdg-terminal-exec-…scope` (`observability-census-r1.md:93-94`);
  kumitate notes the `mado-binds.py` naming adjacency (above); tameshi's
  `mutation-case-mado-verify.md` is a method-level mutation case against
  mado's `mado-verify.sh` (declared-plane census), not the input plane;
  kake/kama/kengaku/kotoba mention Hyprland once each, incidentally
  (ops-automation table row, Hyprland unix-socket note, RSS census of the
  process, SKILL-overlap census classifying mado overlap=none —
  `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round49.md:82`).

## Contested scope to name

1. **The mado↔tsukuroi input boundary is live again this round.** Round 19's
   adjudication predates any mado input-device content; round 46 grounds the
   plane from the config side. The nearest-neighbour points: C2's step 6
   (virtual keyboards, the fcitx5 input method — S322/S323) and the Limits
   section's UNK-parked per-device libinput settings (sensitivity,
   accel_profile, …) and the un-reproduced XKB compile (xkeyboard-config
   file plane). No conflict observed — C2 parks all of these as UNK/out of
   scope, which is exactly the round-19 boundary. If a future tsukuroi round
   measures input-hardware health (evdev nodes, libinput quirks, keymap
   compile failures in the journal), it should cite this entry for the
   config-semantics half rather than re-derive it; likewise mado must not
   drift into `/dev/input` or `libinput debug-events` probing.
2. **fcitx5 coexistence:** tabi's evidence records `org.fcitx.Fcitx5.desktop`
   in a session autostart listing
   (`tabi-shokunin/corpus/evidence/tabi-r2-2-state/tabi-r2-2-status-2.txt:13`)
   — shape-only session state in tabi's browser-plane evidence. The
   input-method's virtual-keyboard naming semantics are mado's S323 pin
   territory. No ownership contest; noted so the two records can cross-cite.
3. **Hyprland process forensics stay with tsukuroi/mori/tabi** (OOM, SIGSEGV,
   session teardown); round-46's live `hyprctl devices -j` read is a
   config-agreement probe, not process forensics — distinct questions,
   distinct receipts.
4. **Hygiene adjacency (no action needed):** souji's fleet dedup census lists
   mado corpus files as byte-identical/duplicate incidental hits
   (`souji-shokunin/.ufo/waves/round-29/w1/deliver-sibling-overlap.tsv:413-432`),
   and tabi's round-34 `ConnSiblingDrift/mado.diff` is the prior-round
   precedent for this seat's task on the *monitor* plane. Neither touches
   input devices; the round-46 data commit should simply not re-introduce
   duplicated bytes.

## Method notes

- Read-only throughout: sibling PROVINCE.md + corpora + SOURCES.md only; no
  writes anywhere but this seat's two report files. No tools installed.
- Locators above are grep-computed, not typed. Quotes ≤ 25 words.
- Survey command set: `grep -ri` over each sibling corpus for the term set
  above; `find */tools -name '*device*'`; per-lane SOURCES.md
  `grep -icE 'hyprwm|hyprland|hyprlang|xkbcommon'`. All 19 sibling lanes
  enumerated from `/home/vgpnk/Projects/shokunin/*-shokunin/`.
