# R82ConnSiblings — sibling-overlap scan for round 82 (C1 / C2)

Seat: `R82ConnSiblings` (connector, leaf, read-only). Lane: mado-shokunin, round 82, wave 1.
Scan base: lane `master` `6ea2386d49318a5f223097c78b5fe79c31b064f8` (the frozen declaration's base).
Sibling trees are read-only surfaces; nothing in a sibling tree was written, staged or copied.
Receipts for every command are in `R82ConnSiblings/receipts.txt`.

## 0. Verdict (item 3, stated plainly)

**No sibling lane claims either ground.** Neither (a) layer-shell/protocol surface sizing and the
client allocation, nor (b) the StatusNotifierWatcher / tray plane, is declared or claimed by any
other lane's `corpus/`, `SKILL.md` or `PROVINCE.md`. (The only out-of-corpus probe bytes on either
ground are a mirror of mado's *own* `tools/mado-verify.sh` — §4 row 11.)

Every sibling artefact a `tray` / `waybar` / `set_size` / `allocation` grep can surface is a
**different surface, a name collision, or a reflection of mado's own text**, itemised in §4. The
only sibling texts that touch this lane's grounds at all do so by *routing the ground to mado* or by
*quoting mado's own bytes*.

## 1. Method (reproducible)

- Roots: every `/home/vgpnk/Projects/shokunin/*-shokunin/` except `mado-shokunin` (20 sibling trees).
  Also checked the misnamed wrapper `kumitate-shokinin/` (does not match the glob): zero anchors.
- Per tree, exactly `corpus/`, `SKILL.md`, `PROVINCE.md` (seat spec).
- Term sets, case-insensitive fixed-string census (`grep -riF`), counts per lane:
  (a) `layer_surface`, `exclusive_zone`, `waybar`, `bar footprint`, `set_size`, `allocation`;
  (b) `StatusNotifier`, `busctl --user`, `tray`.
- `tray` re-run as a word-boundary match (`\btray(s)?\b`) because the substring count is dominated
  by `stray`, `array`, `Raycast`, `betray`; engine/bundle directories excluded from that pass.
- Then a **fleet-wide** grep (all files, fleet root included) for the two decisive anchors
  `layer_surface|exclusive_zone` and `StatusNotifier`, to catch mentions outside the scoped files.
- Lane revisions recorded at scan time:

| lane | HEAD | lane | HEAD |
|---|---|---|---|
| audio | `f9da7ee97e0b` | kama | `6da926f27e2d` |
| kaidoku | `369fa6e7fe1a` | kengaku | `614f00559c75` |
| kotoba | `1c8f37edf2e5` | kumitate | `a648a6f8f302` |
| tabi | `57b29bade4b0` | mori | `6056d0010250` |
| tameshi | `c8d40f5d4ed8` | kagi | `880824b1d3da` |
| tsukuroi | `06f1bbbb8037` | game-dev-3d | `39ca3973c786` |

## 2. Census (exact, over `corpus/` + `SKILL.md` + `PROVINCE.md`)

```
layer_surface    | NONE
exclusive_zone   | NONE
bar footprint    | NONE
StatusNotifier   | NONE
busctl --user    | tabi-shokunin=15
waybar           | audio-shokunin=2958 kaidoku-shokunin=14 kotoba-shokunin=4
                   tabi-shokunin=16 tameshi-shokunin=2 tsukuroi-shokunin=6
set_size         | audio-shokunin=636 game-dev-2d-shokunin=80 kaidoku-shokunin=1
                   mori-shokunin=2 tabi-shokunin=2
allocation       | audio=17 chousa=27 game-dev-2d=571 game-dev-3d=4960 kagi=1
                   kaidoku=51 kasegi=51 kengaku=2 kotodama=59 kumitate=11
                   mori=1065 revenger=10 tabi=43 tameshi=5 tsukuroi=38
tray (word-bnd)  | kake-shokunin=1 kotodama-shokunin=3   (all non-desktop, see §4)
```

Fleet-wide (all files, mado excluded), the decisive anchors occur **once** and not in a lane repo:
`exclusive_zone` at fleet-root `MANIFEST.json:43505`, inside mado's own round-77 defect text
(`D8 S460 locator set_exclusive_zone :152-190 …`). `layer_surface` does not occur at all.
`StatusNotifier` occurs only out of corpus scope: §4, rows 10-11.

**Sense check on the two broad terms — none of these is the claim's sense.**
- `set_size`: audio is a receipt field `set_size=1` in Xtensible metadata rows; game-dev-2d is Godot
  engine symbol text (`window_set_size`, `_set_size_2d_override`) inside exported binary bundles;
  mori is the systemd C source `increment_oomd_xattr(…, set_size(pids_killed))`; tabi is
  `ArraySet.prototype.size` in a vendored Playwright bundle; kaidoku is one binary-byte offset.
  None is the layer-shell `set_size` request.
- `allocation`: heap/object allocation (audio, game-dev-2d, kasegi, kumitate), engine RID allocation
  (game-dev-3d: `P11JoltShape3D`/`P10JoltBody3D` leaked-at-exit lines), k8s DRA / bandwidth
  (mori), btrfs `allocation/` sysfs (tsukuroi), ID allocation footers (tameshi, revenger), reader-object
  allocation (chousa), compute-optimal allocation (kengaku), cron/round budget (kagi), renderer quota
  allocation (tabi), dialect "reallocation" (kotodama), graph/reverse-edge allocation and
  `MaximumAllocationSize` (kaidoku). None is the client's declared band.

## 3. Ground (a) — layer-shell sizing and the client allocation

Zero occurrences of `layer_surface`, `exclusive_zone` and `bar footprint` in all 20 sibling trees;
no sibling declares a band, a zone, an arrangement box, or an allocation input. `allocation` and
`set_size` hits are the other senses above; `waybar` hits are other surfaces (§4).

The fleet does the opposite of contesting: three lanes **route the compositor plane to mado**.
These are positive exclusivity registrations, not claims:

- `game-dev-3d-shokunin/PROVINCE.md:75` — "Desktop/compositor display behavior belongs to
  `mado-shokunin` (`../mado-shokunin/PROVINCE.md:3-12`)."
- `kotoba-shokunin/PROVINCE.md:72` — mado row, relation **none**: "mado owns the
  Hyprland/waybar/walker/terminal config plane and display behavior read-only".
- `tsukuroi-shokunin/PROVINCE.md:124` — `OUT-004 | ADJ-03` against `mado-shokunin/PROVINCE.md`
  at `a4046a821608`, the same "Owns (surfaces)" text.
- `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md:66` — mado row,
  `SKILL.md | none | no | no` (kotoba records *no* SKILL.md overlap with mado).

One pointer must not be mistaken for evidence of this ground: kake's captured link label
"OS tuning / **Waybar limits**" (§5). It is a link label and a sitemap `<loc>`; the page body is
**not** captured, so it is not bytes about the client allocation. If the lane wants it, it is a new
source to open and pin under mado's own provenance rules — not a sibling receipt.

## 4. Hit-by-hit (item 2): lane, file:line, same ground or another surface

| # | lane | file:line | class |
|---|---|---|---|
| 1 | audio | `corpus/live/r80-scout/runs/00-baseline/pactl-clients.txt:7` (`61737 PipeWire waybar`); `corpus/live/r81-scout/receipts/s0-baseline.json:152-153`; `corpus/live/r80-scout/p7-linkauthority.json:424` | **different surface**: `waybar` as a PipeWire *client* in the audio graph (2 958 hits, all this class) |
| 2 | kaidoku | `corpus/knowledge/2026-10-13-crash-evidence.md:16`, `:50`; `corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md:29-30`, `:60` | **different surface**: `waybar` as a coredump artefact (`core.waybar…zst`, `coredumpctl debug 1728`) |
| 3 | kotoba | `PROVINCE.md:72`; `corpus/knowledge/sibling-overlap-census-round49.md:82`; `…-round74.md:66`, `:97` (the `waybar` hits; `:122` is the same mado row's `+118/-0` delta with no `waybar` token) | **recognition**: registers mado's ownership; records zero SKILL.md overlap |
| 4 | tabi | `corpus/adjacency-host-delta-r45.tsv:12` … `r59.tsv:157` (15 files, one row each); `corpus/adjacency-screen-browser.tsv:347` | **reflection**: the 15 `busctl --user` hits are verbatim quotations of `mado-shokunin/PROVINCE.md:35`; the 16th is a systemd user-scope name `app-Hyprland-waybar-…scope` |
| 5 | tameshi | `corpus/knowledge/mutation-case-mado-verify.md:114`, `:154` | **different surface, dependent on mado's tool**: `waybar/style.css` is the mutation path inside a recorded `mado-verify.sh` run; tameshi owns the mutation method, as `PROVINCE.md:35` already states |
| 6 | tsukuroi | `PROVINCE.md:124`; `corpus/knowledge/adjacency-anchors-r19.md:84` (+ `.json:58`); `corpus/knowledge/degraded-triage-r4.md:481`, `:500`; `corpus/knowledge/kill-event-deep-r8.md:141` | **recognition** (`OUT-004`) + **different surface**: `waybar` as a process inside a scope / a kill-event victim |
| 7 | game-dev-3d | `PROVINCE.md:75` | **routing to mado**: compositor display behaviour is mado's |
| 8 | kumitate | `SKILL.md:623` | **different surface**: disambiguates its mount-bind oracle from "the Hyprland `mado-binds.py` keybind file" |
| 9 | **kake** | `corpus/knowledge/freshness-pins.json:159` (`"omarchy-usage-tray"`); `.ufo/waves/round-82/capture/ds4cc-primary/body.bin:710`, `:1043`; `capture/ds4cc-sitemap/body.bin` | **name collision, not a claim**: `omarchy-usage-tray` is a *Waybar module product* ("14 AI usage meters on one chip … Quattro plugin or Waybar"). kake's ground is capture/freshness of public product pages; it asserts nothing about `org.kde.StatusNotifierWatcher` |
| 10 | tsukuroi (out of corpus scope) | `.ufo/waves/round-24/w1/ExecMirrorTimestamps/{host,official,stable}-extra-pkglist.txt:5294/5297` | **package census**: the package name `kstatusnotifieritem 6.31.0-1`; not a claim |
| 11 | tameshi (out of corpus scope) | `.ufo/evidence/round-25/mte-reports/bash-mado-verify.mte.json:187` | **mirror of mado's own bytes**: the recorded body of mado's `tools/mado-verify.sh`, containing the tray probe. Same ground, *self*-reflection, not contested |
| 12 | kumitate (out of corpus scope) | `.ufo/waves/round-50/r50/LabratSystemd.md:158` (`busctl --user status`) | **different surface**: a systemd lab note; `status`, no watcher name, no interface census |
| 13 | mori (r82) | `.ufo/waves/round-82/w1/Mo82C01Contract.md:193` (`"+SURFACE:lane.mado"`) | **different surface**: a fleet drift surface id in a contract critic; no protocol claim |
| 14 | kengaku (r82) | `.ufo/waves/round-82/w1/ConnectorR82.md:80`, `:96` | **disjoint ground**: a same-round connector that scanned mado's `quality/check-control-receipts.py` and `quality/population-suite.py` (routed-repair/population verifiers), not `tools/mado-barfoot.py` or either r82 counter |
| 15 | kama (r82) | `.ufo/waves/round-82/w1/CN01SiblingScan/receipts.txt:14-15` | **disjoint ground**: a same-round connector that read mado's `tools/mado-devices.py` and `tools/mado-monitors.py` (blame/introspection) |
| 16 | kotodama | `corpus/knowledge/civilizations/yoruba.md:73`; `corpus/knowledge/culture-material/furniture-interior-lexicon.md:76`; `corpus/lessons/round-57.md:93` | **unrelated**: a divination *tray*, a furniture *tray*, a museum *tray stand* |

Two rows matter enough to state separately:

- **Row 9 is the only `tray` token in any sibling corpus that is about a desktop bar.** It is a
  *module* (a Waybar chip), not a *tray item* (a StatusNotifier item), and kake's pin is a
  freshness pin on a product name. Naming it prevents a later reader from scoring it as a
  competing claim on the tray plane.
- **Row 4 is the only sibling occurrence of `busctl --user`, and it is not a probe.** The 15 hits
  are the same quoted sentence of `PROVINCE.md:35` carried through tabi's adjacency deltas; the
  adjudicated claim owner of that sentence is mado.

## 5. Nearest adjacent ownership (different surfaces; nothing to concede, one line each)

- `tsukuroi-shokunin/PROVINCE.md:10` — owns "systemd user units & timers (`systemctl --user`, unit
  files, failed states)". C2 reads the user **bus**, not units: bus-name ownership and an interface
  census. Different object and different verb.
- `mori-shokunin/PROVINCE.md:6` — owns fleet/host liveness (pid, start time). C2's `busctl --user
  list` row reads a PID **column** only to prove the name has a live owner; it does not claim
  process liveness. `PROVINCE.md:368` lists "D-Bus `Killed` signals" as mori's open **frontier** —
  a signal plane, not a name/interface census.
- `audio-shokunin` owns `waybar` **as an audio client**; `kaidoku-shokunin` owns it **as a core**;
  `tsukuroi-shokunin` owns it **as a process in a scope**; `tameshi-shokunin` owns the **mutation
  method** that consumes mado's tool. Each is a distinct surface; none is the bar's protocol
  sizing or its tray plane.

## 6. What this lane's report should name (paste-ready, no instrument change)

> **Boundary (C1).** No sibling lane claims the layer-shell sizing or client-allocation ground:
> across 20 sibling lane trees (`corpus/`, `SKILL.md`, `PROVINCE.md`) `layer_surface`,
> `exclusive_zone` and `bar footprint` occur zero times, and of the four lanes that name the
> compositor, three route it to mado (`game-dev-3d-shokunin/PROVINCE.md:75`,
> `kotoba-shokunin/PROVINCE.md:72`, `tsukuroi-shokunin/PROVINCE.md:124`) while the fourth
> (`kengaku-shokunin/PROVINCE.md:380`) names only the compositor/session sockets as a
> sandbox-escape surface.

> **Boundary (C2).** No sibling lane claims the tray plane: `StatusNotifier` occurs zero times in
> any sibling `corpus/`, `SKILL.md` or `PROVINCE.md`; the only desktop-bar `tray` token in a
> sibling corpus is `kake-shokunin/corpus/knowledge/freshness-pins.json:159`
> `omarchy-usage-tray`, the name of a Waybar **module** product pinned for capture freshness, not
> a StatusNotifier claim; the `busctl --user` occurrences in tabi's corpus are 15 verbatim
> quotations of `mado-shokunin/PROVINCE.md:35`.

> **Provenance (C2).** The three round-82 row classes extend a probe the lane already runs rather
> than introducing a surface: `tools/mado-verify.sh:3631-3634` emits `live.waybar.tray` from
> `busctl --user get-property fr.arouillard.waybar /StatusNotifierWatcher
> org.kde.StatusNotifierWatcher RegisteredStatusNotifierItems`, and `SKILL.md:156` already
> declares that command as the tray route; the new rows address the same watcher by its
> well-known bus name instead of the vendor name.

Supporting observation, **live and non-frozen** (shape only; must not enter the claim arithmetic or
be pasted as a receipt): one read-only `busctl --user list` at scan time returned
`fr.arouillard.waybar`, `org.kde.StatusNotifierHost-1720-2` and `org.kde.StatusNotifierWatcher`,
all with PID `1720`, process `waybar` — so both name forms resolved to one connection in that
sample, and the C2 row's bound shape (`org.kde.StatusNotifierWatcher` line, PID column a decimal in
1..4194304) was satisfied.

## 7. Affected axes, proposed move, risks, verification

**Axes named.** The round declares two: **coverage** (C1) and **operability** (C2). This seat's
output touches neither's arithmetic; it acts on the fleet's **adjacency/boundary** axis and, second
order, on operability (a row whose surface is already declared and already probed is cheaper to
defend than one that reads as new).

**Proposed move (one bounded synthesis).** In the C2 section only, add the two sentences of §6
("Boundary (C2)" and "Provenance") plus the one-line `kake` collision note from §4 row 9, and in the
C1 section add the "Boundary (C1)" sentence. Nothing else: no counter, control, case, mutation or
tool byte is touched, and no sibling artefact is cited as evidence about a ground it does not own.

Why this and not a probe: the two grounds are already unmatched in the fleet, but the *contradiction
that is not visible yet* is inside the lane — the province declares a tray **runtime fact** route
through the vendor name (`SKILL.md:156`, `tools/mado-verify.sh:3631-3634`) while the round-82 rows
address the watcher by its **well-known** name (`SKILL.md:274-276`). Stated explicitly, the new rows
read as the same plane through a second name form; unstated, the next critic has two `tray` access
paths and a sibling pin named `omarchy-usage-tray` to reconcile with nothing on the page saying how
they relate.

**Risks (stated, not smoothed).**
1. *Presence-bound row.* `busctl --user list` exits 0 whenever any name exists, so the row's
   outcome must stay the `org.kde.StatusNotifierWatcher` **line** (as `SKILL.md:274` binds it); a
   reader binding rc alone would read an absent watcher as clean. Naming this in the report is a
   prose clarification; the frozen counter's predicate decides the row, not this seat.
2. *One-sample identity.* "The vendor name and the well-known name are one connection" is
   observed once, not a protocol guarantee. The durable sentence is the byte-level one (both names
   in one `busctl --user list` at scan time), never "waybar always owns the well-known name".
3. *Non-frozen PID.* PID `1720` is host state; it must not be pasted into a receipt, a control or a
   frozen expectation. Shape only (three names, one PID, process `waybar`).
4. *Collision drift.* If §4 row 9 is not named, a later `tray` search over sibling corpora will
   find kake's pin and can be mis-scored as a second claim on the ground.
5. *Uncaptured page.* kake holds a link label and a sitemap `<loc>` for `ds4cc.com/omarchy-usage/`,
   never the body. Citing its "Waybar limits" label as bytes about waybar's limits would be a
   provenance breach under this lane's own rule (open the source, do not infer it).

**Verification (cheap, read-only).**
- Census replay: the loop in §1 over `*/{corpus,SKILL.md,PROVINCE.md}` must print `NONE` for
  `layer_surface`, `exclusive_zone`, `bar footprint`, `StatusNotifier`, and `tabi-shokunin=15` for
  `busctl --user`. Any new non-zero is a new claim and reopens this seat's verdict.
- `grep -n 'StatusNotifier' tools/mado-verify.sh` → `:3634` only, at base `6ea2386d`; the row it
  feeds is emitted at `:3631` (`row hypr-live live.waybar.tray UNKNOWN`), and `:3630` is the
  `have busctl` guard.
- `grep -n 'omarchy-usage-tray' kake-shokunin/corpus/knowledge/freshness-pins.json` → `:159`;
  `grep -c 'omarchy-usage/' kake-shokunin/.ufo/waves/round-82/capture/ds4cc-sitemap/body.bin` ≥ 1
  while `capture/manifest.json` lists only `/`, `/robots.txt`, `/sitemap.xml` — pointer, not body.
- Live, non-frozen: `busctl --user list --no-pager | grep -E 'StatusNotifier|arouillard'` → the
  same three names, one PID, process `waybar` (expect names, not the PID).

## 8. Tooling

No installs, no upgrades, no package transactions. Tools used: `grep`, `busctl` (read-only),
`git rev-parse` (read-only), `python3` (json inspection). No writes outside this seat's paths.

STATUS: ok
