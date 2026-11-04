# R81ConnSiblings — sibling-overlap scan, round 81 w1

Seat: `R81ConnSiblings` (connector, sibling-overlap). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round: 81, ONE v1 wave. Base `c702094ace5dd9b2b5e152951b4b2f4dd578f8b6`; freeze
`0e2ccd2a8692825cac534f57246053b276be9f13`.

Scope of writes: this report and `.ufo/waves/round-81/w1/R81ConnSiblings/` only. No sibling file, no
fleet-root tracked file, no `.ufo/state/`, no `SKILL.md`/`LOG.md`/declaration/controls/instrument was
written. Read-only across the fleet; no git or jj command was run at all (not even read-only ones — none
was needed). No subagent was dispatched. Scratch `/fast/scratch/hyaku/mado-r81/R81ConnSiblings` held
nothing that is cited below and was removed at exit.

**Every command and its literal output is in `R81ConnSiblings/sweep-*.txt`** (11 captures, plus
`sweep.sh` / `sweep2.sh` which regenerate them). Nothing below is paraphrased: each quoted line is
copied from a capture or from the committed bytes at the path named beside it.

---

## 0. What "this round's grounds" means here (the scan's targets)

Two grounds, as the frozen declaration states them
(`.ufo/waves/round-81/claims-declaration-r81.md:27-46`):

- **C1** — the composition's overflow rounding and its auto-zone gate: `CBox::round`'s coupled
  origin/far-edge rounding; gtk-layer-shell's auto exclusive zone gated on `horiz XOR vert` and sized
  from the allocation; the left-dock vertical gate and its attribution cell.
- **C2** — two new runbook matcher *classes*: an action-column matcher over
  `omarchy menu keybindings --print | cut -c36-`, and a `pgrep -x waybar` PID-list + exit-status pair.

The four things the seat asks about map onto those as: (a) layer-surface reserved-band / arrangement
modelling, (b) an auto-exclusive-zone implementation, (c) a runbook row grammar over omarchy output,
(d) a `pgrep`-shaped liveness matcher. I swept all four across the whole fleet.

Anchors a census should key on, captured at `.ufo/waves/round-81/w1/R81ConnSiblings/sweep-k-mado-rows.txt`:

| row | file:line (mado) | anchor string |
|---|---|---|
| action column | `SKILL.md:270` | `omarchy menu keybindings --print \| cut -c36-` |
| chord column (r80, predecessor) | `SKILL.md:268` | `omarchy menu keybindings --print \| cut -c1-35` |
| whole-line shape (r79) | `SKILL.md:267` | `omarchy menu keybindings --print` |
| PID state (r81) | `SKILL.md:271` | `pgrep -x waybar` |
| frozen int_range (r80, superseded) | `SKILL.md:254` | `pgrep -x waybar \| head -n 1` |

Frozen sets: `c2-runbook-cases-r81.json` 26 cases, containing **both** `waybar-process` (`kind=int_range`,
argv `pgrep -x waybar | head -n 1`) and `waybar-pgrep` (`kind=pid_state`, argv `pgrep -x waybar`);
`c1-cases-r81.json` 39 cases.

---

## 1. Q1 — does any sibling lane claim either ground?

### 1.1 Verdict

**No sibling lane claims either ground, and no sibling instrument implements either mechanism.** What
exists instead is (i) three sibling PROVINCE rows that *route the ground to mado*, (ii) a set of
form-neighbours on the `pgrep` side, and (iii) several lexical homonyms that a token-keyed census would
mis-merge. The `pgrep` side is the only one with real sibling activity; the layer-surface /
auto-exclusive-zone side is empty outside mado.

Evidence base: 21 `*-shokunin` directories (20 siblings + `mado`), instrument inventory at
`sweep-l1-instrument-dirs.txt`, four-family sweep at `sweep-d-lane-scope.txt` (lane sources, `.ufo/waves`
excluded) and `sweep-a-layer.txt` / `sweep-b-omarchy-output.txt` (whole fleet, `mado`/`.ufo`/`.scratch`
excluded), `sweep-l2-instrument-families.txt` (`*/tools */scripts */verifiers` only).

### 1.2 (a) layer-surface reserved-band or layer-arrangement modelling — **no claim**

The only sibling PROVINCE lines that mention the compositor plane are *disclaimers*, not claims
(`sweep-e-province.txt`):

- `game-dev-3d-shokunin/PROVINCE.md:75` —
  "`- Desktop/compositor display behavior belongs to \`mado-shokunin\` (\`../mado-shokunin/PROVINCE.md:3-12\`).`"
- `kotoba-shokunin/PROVINCE.md:72` — the census row for mado, classification **`none`**:
  "`mado owns the Hyprland/waybar/walker/terminal config plane and display behavior read-only; it
  states no split with kotoba and treats the omarchy skill as read-only documentation (mado
  \`PROVINCE.md:10\`), claiming no lane SKILL.md.`"
- `tsukuroi-shokunin/PROVINCE.md:124` — OUT-004, a *routing* row:
  "`Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and
  screen/idle behavior.`"

`kumitate-shokunin/PROVINCE.md` names no display ground at all (`:3` is
"`**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime`"), and
`game-dev-2d`, `kagi`, `kasegi`, `kengaku`, `lore`, `revenger`, `audio`, `chousa`, `kaidoku`, `kama`,
`kotodama`, `souji`, `tabi`, `tameshi`, `mori` carry no `tools/`+`scripts/`+`verifiers/` hit for the
family (`sweep-l2-instrument-families.txt` is a one-line file — see 1.6).

The API family (`applyExclusive|arrangeLayerArray|arrangeLayersForMonitor|CReservedArea|addreserved`)
outside mado is **6 files, none of them a sibling claim** (`sweep-l5-c1-attribution.txt`):

```
./.ufo/reports/round-77/mado.md
./.ufo/reports/round-79/mado.md
./.ufo/reports/round-80/mado.md
./kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt
./tabi-shokunin/.ufo/waves/round-34/w2/ConnSiblingDrift/mado.diff
./MANIFEST.json
```

Every one of those six is mado's own words copied elsewhere (§4). **Zero** sibling-lane source file
models a layer surface.

### 1.3 (b) auto-exclusive-zone implementation — **no claim, zero sibling implementations**

No sibling **source** file contains `exclusive zone`, `exclusive_zone`, `set_exclusive_zone`, `zwlr_layer`,
`arrangeLayerArray` or `arrangeLayersForMonitor` as a modelled mechanism; every fleet-wide occurrence of
`applyExclusive` / `arrangeLayerArray` / `arrangeLayersForMonitor` / `CReservedArea` / `addreserved`
outside mado is a copy of mado's own text or a package name (§4, `sweep-l5-c1-attribution.txt`). The bare
word `exclusive` occurs in siblings only as a different concept (§2, H1). The frozen ground's source
library appears in a sibling only as an installed
**package name** in tsukuroi's inventory captures — `gtk-layer-shell 0.10.1-1` at
`tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/host-extra-pkglist.txt:3081` and its four
sibling copies (`sweep-a-layer.txt`). Package identity is tsukuroi's ground; it models no behaviour, so it
is not an implementation of the zone and must not be counted as one.

### 1.4 (c) runbook row grammar over omarchy output — **no claim**

`sweep-b-omarchy-output.txt` first block is **empty**: no file outside mado and outside `.ufo`/`.scratch`
contains `omarchy-menu-keybindings`, `omarchy menu keybindings` or `cut -c36-`. No sibling `SKILL.md`
contains `omarchy-menu` or `cut -c` either (`sweep-f-skill.txt` — its only two lines are the `pgrep` rows
quoted in 1.5).

The nearest sibling artifact is a *form* neighbour, not the ground: `tabi-shokunin/SKILL.md:1343` is a
state-table row with a shell matcher, `ss -ltn | grep -c 10086; pgrep -x kimi-webbridge | wc -l`. It
binds a **count** (`→ 0`), not a PID list, and because the pipeline's status is `wc`'s, `pgrep`'s exit
status is discarded — the exact defect C2's `pid_state` kind exists to avoid. Different subject
(`kimi-webbridge`), different assertion, different lane. Homonym, not overlap.

### 1.5 (d) `pgrep`-shaped liveness matcher — **five sibling lanes, six process subjects, none the bar**

This is the one family with real sibling activity. `sweep-d-lane-scope.txt` (lane sources, `.ufo/waves`
excluded) and `sweep-c-pgrep.txt` (per-file counts) give the subjects:

| lane | file:line | subject | form |
|---|---|---|---|
| mori | `PROVINCE.md:48` (FR5) | `shokunin-watchdog` | *rule*: "`an unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity`" |
| mori | `SKILL.md:790` | `shokunin-watchd` | *rule*: "`exit 1 is absence for that one query; exit 2 or 3 and a missing binary are \`unavailable\`, never absence`" |
| mori | `tools/mori-census.sh:315, 3205-3206` | watchdog | stub harness: `printf '1234 bash /path/scripts/shokunin-watchdog.sh\n' > "$d/stub/pgrep"` + `printf 0 > "$d/stub/pgrep.rc"` |
| tabi | `SKILL.md:1343` | `kimi-webbridge` | `pgrep -x kimi-webbridge \| wc -l` (count, rc lost) |
| tabi | `corpus/knowledge/webbridge-revival-assessment.md:88` | `kimi-webbridge` | "`pgrep -x kimi-webbridge` → none" |
| kama | `tools/round64-c2-counter.py:264` | `llama-server` | real PID-set reader: "`Live llama-server pids (\`pgrep -x llama-server\`), zombies dropped through /proc/<pid>/stat`" |
| audio | `reports/round-77/r77-verifier.md:439` | `pw-record` | "`\`pgrep -x pw-record\` (or \`-f\` plus a \`/proc/<pid>/exe\` check) would measure`" |
| audio | `reports/round-88/r88-boundary.md:348` | `r88b_hog` | "`matches \`comm\` (\`yes\`), not \`argv[0]\` — so it found none`" |
| game-dev-2d | `corpus/live/r99-boundary/run_matrix.sh:53` | `yes` (load hog) | `host_yes() { pgrep -x yes \| wc -l; }` |
| game-dev-3d | `reports/round-97/r97-boundary.md:402` | `yes` | "`\`pgrep -x yes\` → **0**`" |
| chousa | `.ufo/waves/round-32/w2/RerunC1b.md:29` | `yes` | "`verified by \`pgrep -x yes\` =1 in a 3 s probe`" |

Two of these are genuinely close in *shape* to C2 and worth naming explicitly:

- **`kama-shokunin/tools/round64-c2-counter.py:264-283`** is the only sibling **implementation** of a
  PID-list reader: `subprocess.run(['pgrep','-x','llama-server'], …)`, then a `/proc/<pid>/stat` state
  read to drop zombies. It is a *set* extraction for a capacity counter over a model server, and it
  ignores the exit status entirely — it does not bind a state pair.
- **`mori-shokunin/SKILL.md:790`** is the only sibling **written rule** about reading a `pgrep` exit
  status. It is *compatible* with C2's `pid_state` (which fails any pair that is neither "rc 0 with a
  numeric PID list" nor "rc 1 with empty stdout", so a missing binary's 127 or a usage error's 2/3 is a
  fail rather than "not running"); see the frozen negative `{"out": "", "rc": 2}` in
  `c2-runbook-cases-r81.json` case `waybar-pgrep`.

None of the six subjects is `waybar`, and no sibling lane states a claim over the bar's own liveness.
`mori` owns *fleet* liveness; `mado` owns the bar's state as a runbook row. The objects differ.

### 1.6 Each sibling's `tools/` — the seat's literal ask

`sweep-l1-instrument-dirs.txt` (directories and entry counts):

```
chousa-shokunin          tools=20
kaidoku-shokunin         tools=52
kama-shokunin            tools=132
kotodama-shokunin        tools=33
mado-shokunin            tools=27
mori-shokunin            tools=59
souji-shokunin           tools=151
tameshi-shokunin         tools=68
tsukuroi-shokunin        tools=116
kake-shokunin            scripts=42
kumitate-shokunin        scripts=36
tabi-shokunin            scripts=64
kotoba-shokunin          verifiers=78
```

`game-dev-3d`, `game-dev-2d`, `kagi`, `kasegi`, `kengaku`, `lore`, `revenger`, `audio` keep none of the
three; the three lanes the seat names by hand (`game-dev-3d`, `kotoba`, `kumitate`) keep `-`/`verifiers`/
`scripts` respectively, so a scan that only opens `tools/` would have reported a false clean for exactly
those three. That is why `sweep-d-lane-scope.txt` sweeps whole lane trees instead.

The **entire** four-family result over every sibling `tools/`, `scripts/` and `verifiers/` is one line
(`sweep-l2-instrument-families.txt`):

```
kama-shokunin/tools/round64-c2-counter.py:264:    """Live llama-server pids (`pgrep -x llama-server`), zombies dropped
rc=0 (1 = no hits)
```

(`mado-shokunin` shows `tools=27` because `ls -1` counts the `__pycache__` directory; kumitate's own
round-81 inventory counts `mado-shokunin/tools: 26 files`, which agrees with `tools=27` minus that
directory.)

---

## 2. Homonyms a census must not merge

Each is a token that is *identical* across two unrelated grounds. A census keyed on the word will
mis-attribute; a census keyed on **(subject, mechanism)** will not.

| # | token | mado's sense (this round) | sibling sense (must not merge) | witness |
|---|---|---|---|---|
| H1 | `exclusive` | gtk-layer-shell's auto exclusive **zone** / Hyprland's `exclusive` zone value | kaidoku: an extraction **disposition** — "`removed` is the extractor-determined disposition … `{diagnostic, kinds, disposition: "exclusive", …}`" (`kaidoku-shokunin/tools/round-41/c1-counter.py:492`); chousa: "`exclusive flock(2)`" (`chousa-shokunin/tools/research-gate.sh:215`) and "`--pin and --drift are mutually exclusive`" (`:8834`) | `sweep-a-layer.txt` |
| H2 | `reserved band` | the compositor's `reserved` array `[left, top, right, bottom]` | kasegi: a **package-id** band — "`four rows mapping package ids to a declared reserved band`" (`kasegi-shokunin/.ufo/waves/round-24/wave1/ConnSibling.md:161`) | `sweep-a-layer.txt` |
| H3 | `action column` | the output column right of ` → ` after `cut -c36-` | kaidoku: a **scored decision-table column** in the SquashFS triage table — `kaidoku-shokunin/SKILL.md:333`, `:364`, `:415`, `:434`, `:548`, `:517`; **233 files** in kaidoku alone. kotoba: "`A table with no action column at all is documentation, not a decision surface`" (`kotoba-shokunin/corpus/knowledge/anatomy-and-compression.md:113`); kama: a "next-action column" (`kama-shokunin/.ufo/waves/round-26/w2-falsify/advice/ConnectorAdjacency.md:42`) | `sweep-b-omarchy-output.txt` (per-lane counts: kaidoku 233, kotoba 12, tsukuroi 2, kama 2, chousa 2, tameshi 1, lore 1) |
| H4 | `composition` | *the* composition — the layer-surface composition under the bar's reserved band | kotoba: a harness record-map fixture **directory** — `verifiers/fixtures/compare-harness-independent/record-map-24-composition/` | §3.3 |
| H5 | `layer` | a Wayland layer-surface level 0–3 | game-dev-2d: `TileMapLayer` (`PROVINCE.md:17`); kumitate: "origin script layer" / "origin runtime layer" (`PROVINCE.md:12-13`) | `sweep-e-province.txt`, `game-dev-2d-shokunin/PROVINCE.md:17` |
| H6 | `pgrep -x` | the bar (`waybar`) | six other subjects: `hypridle` (merge package), `shokunin-watchdog` (mori), `kimi-webbridge` (tabi), `llama-server` (kama), `pw-record`/`r88b_hog` (audio), `yes`/`sleep`/`zenity` (game-dev-2d/3d, chousa) | §1.5 |
| H7 | `omarchy` | installed payloads under `~/.local/share/omarchy/bin/*` and the read-only skill at `~/.agents/skills/omarchy/` | kotoba: a skill-catalogue member and its **description text** (`record-map-24-composition`); kotoba's host-skill census ran on a *different root* — "`--skills-root C:/Users/jpvei/.zcode/skills`" (`kotoba-shokunin/.ufo/waves/round-82/receipts/after-host-skill-census-ledger.txt:2`) and has **0** `omarchy` rows (`sweep-i-kotoba.txt`); the older assimilation tree `shokuknow/lanes/mado/round15/fetch/omarchy-menu.sh` is a *different* file from the keybindings payload | `sweep-i-kotoba.txt` |
| H7b | `omarchy-menu` vs `omarchy-menu-keybindings` | `omarchy menu keybindings` → the keybindings **payload** | two distinct executables in one directory; `bin/omarchy-menu` dispatches "*`*Keybindings*) omarchy-menu-keybindings ;;`" (`mado-shokunin/.ufo/waves/round-18/fetch/SrcOmarchyBackground/bin_omarchy-menu:85`) | same |
| H8 | lane name | `mado-shokunin` | `kumitate-shokunin` (real lane) beside the **stray empty directory** `kumitate-shokinin/` (contains only `kumitate-shokinin/kumitate-shokunin/.ufo/waves`, no files, mtime `Oct 30 08:50`) | `sweep-l3-stray-lane-name.txt` |

H3 is the expensive one: 233 kaidoku files say "action column" and **none** of them is about a waybar row.
H7b is the subtle one: both commands appear in mado's own round-18 fetch tree, and only the second is the
C2 payload.

---

## 3. Q2 — the staged assimilation package `/home/vgpnk/Projects/shokuknow/merge/mado/`

Read only; nothing was executed there. Sweep: `sweep-g-merge-package.txt`; the command ran after an
explicit `cd` into the package (`$ pwd` → `/home/vgpnk/Projects/shokuknow/merge/mado`, 65 knowledge
entries, 4 amendments, 147 `S###` rows in `SOURCES.append.md`).

### 3.1 (a) layer-surface / reserved-band modelling — **no entry**

```
$ grep -rniE "\bexclusive\b|gtk-layer-shell|barfoot|footprint|reserved band|arrangeLayerArray" \
    knowledge/corpus/knowledge amendments/corpus/knowledge SOURCES.append.md MERGE-REPORT.md
(no output)
```

Zero lines. The package predates the lane's bar-footprint ground entirely: no `bar-footprint*` entry
exists in it, and the word `exclusive` does not occur once in 69 entries plus 147 source rows.

### 3.2 (b) auto-exclusive-zone implementation — **no entry**

Same zero result, same reason. The package's Waybar material is *module-text producer* material —
S207 (`backend.cpp`), S208 (`window.cpp`), S214 (`workspaces.cpp`), S224 (host `config.jsonc`), S228
(`idle.sh`), S231 (stock `config.jsonc`) — i.e. how a module's **text** is formed, never how a surface's
**zone** is computed. It cannot duplicate this round's C1 work.

### 3.3 (c) runbook row grammar over omarchy output — **no entry; one adjacent line, not a duplicate**

```
$ grep -rn "omarchy-menu-keybindings" .
(no output)
$ grep -rniE "omarchy-menu|keybindings --print|menu keybindings" knowledge amendments MERGE-REPORT.md
knowledge/corpus/knowledge/idle-lock-offered-in-the-bar-r15.md:12:source: S337 — /home/vgpnk/.local/share/omarchy/bin/omarchy-menu — `§ the Toggle submenu's option list, and the case arm that dispatches it` — the desktop's own menu
```

One entry touches the *family*: `idle-lock-offered-in-the-bar-r15.md`, resting on **S337 =
`bin/omarchy-menu`**, "the Toggle submenu's option list, and the case arm that dispatches it".

**Would it duplicate a row this round adds? No.** Three reasons, each checkable:

1. **Different executable.** S337 is `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu`; the C2 row runs
   `omarchy menu keybindings`, whose payload is `bin/omarchy-menu-keybindings`
   (`.ufo/waves/round-80/fetch/S473.txt`, `--print` branch at `:243`).
2. **Different subject.** The entry's subject is *the idle-lock choice being offered in two surfaces*; the
   new row's subject is *the action column of the keybindings listing*.
3. **Different assertion kind.** The entry asserts a `grep -c` count on one dispatch arm; the new row
   asserts a 100-line floor plus per-line prefix/trim/no-second-arrow over a live listing.

The package also contains **no** `runbook` entry at all (`grep -rli runbook …` → rc 1), so nothing there
can be mistaken for a runbook-row claim.

### 3.4 (d) `pgrep`-shaped liveness matcher — **7 entries quote the form, none is the row**

```
$ grep -rn "pgrep" knowledge/corpus/knowledge amendments/corpus/knowledge
```

16 lines in 7 entries, all the *idle-daemon / recorder producer probe*:

- `host-bar-producers-r28.md:60` — `> "if pgrep -x hypridle >/dev/null; then"` (the bar's `custom/idle-indicator` producer, §2 "The one producer coupled to the idle plane");
- `idle-lock-runtime-state-r28.md:13,41,64,72,87`; `idle-toggle-and-daemon-lifecycle-r29.md:20,30`;
  `host-idle-lock-chain-r7.md:12,55,71`; `idle-lock-intent-mechanism-r8.md:68`;
  `idle-lock-intent-surface-r9.md:9,22,29`; `host-producer-outputs-r29.md:21`
  (`pgrep -f "^gpu-screen-recorder"`).

**Would any duplicate the new `waybar-pgrep` row? No.** The closest is `host-bar-producers-r28.md` §2,
and the differences are exactly the ones the round turns on:

1. **Subject.** Those entries quote a probe *inside the bar* asking about `hypridle`; the new row probes
   the **bar itself**.
2. **Assertion.** They quote the producer's **source line** (a byte-level fact about `idle.sh`); the new
   row asserts a **live PID-list/exit-status pair**.
3. **The row is absent.** No package entry carries a `waybar` process row at all, so nothing there is a
   duplicate of `pgrep -x waybar`.

The package does, however, supply the *reason* the `pid_state` kind is worth having: S228 records that the
idle producer "`emits an empty text when a hypridle process exists`", i.e. the host's own bar already
depends on process probes — which is why a frozen integer for the bar's PID (r80's `int_range` row) goes
DIFFER the moment the bar restarts.

---

## 4. Q3 — could a later r81 census mistake a sibling artifact for mado's?

**Yes — four artifacts, and one of them is a round-81 sibling artifact that already exists.** Each is
named below with the mechanism that puts mado's ground inside a file that is not mado's.

### 4.1 `kumitate-shokunin`'s round-81 capture carries mado's C1 instrument text — **36 lines**

`kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt`, produced by that
lane's own connector seat with:

```
$ grep -rIn -iE 'attack.?share|connector|planner|band[^a-z]|admission|preflight|pre-dispatch|godspeed' \
    kake-shokunin/scripts tabi-shokunin/scripts */tools
```

The token `band[^a-z]` — intended for the *attack-share band*, not a compositor band — pulled in
`mado-shokunin/tools/mado-barfoot.py`'s docstring. `grep -c mado-shokunin` on that file → **36**. The lines
that matter:

```
216:mado-shokunin/tools/mado-barfoot.py:2:"""mado — bar footprint join: declared waybar config -> live layer box -> reserved band.
223:mado-shokunin/tools/mado-barfoot.py:47:  * Not modelled and named as a limit: a static `monitor … addreserved` band
225:mado-shokunin/tools/mado-barfoot.py:73:# The edge opposite the anchored one on the band axis: gtk-layer-shell's auto zone adds
226:mado-shokunin/tools/mado-barfoot.py:276:        raise Unmodelled("a negative margin can void or invert the exclusive band; not modelled")
```

A census that scans *files* for the ground phrases and reports the containing lane will report
`kumitate` as holding "`reserved band`", "`gtk-layer-shell`'s auto zone" and "`exclusive band`". It is a
character-for-character copy of mado's instrument, captured by accident, in a sibling's round-81 wave.

### 4.2 `tabi` holds a git diff of mado's tree — 126 lines

`tabi-shokunin/.ufo/waves/round-34/w2/ConnSiblingDrift/mado.diff` is a **patch of mado's own files**:

```
1:diff --git a/SKILL.md b/SKILL.md
14:diff --git a/corpus/knowledge/hyprland-monitor-rule-r45.md b/corpus/knowledge/hyprland-monitor-rule-r45.md
```

and it contains `addreserved` inside mado's round-45 monitor-rule prose:

```
59:+**OBS** S303 - field 1 is first tested for the modifier forms: `if (ARGS[1] == "disable" || …
   "addreserved" || …` (Hyprland-legacy-ConfigManager.cpp:1299). `addreserved` changes the
   same-selector rule's reserved area, …
```

`addreserved` is precisely the static-reserve API that C1's join composes under the bar's band (and the
one `mado-barfoot.py:47` names as its limit). A census grepping `addreserved` across lanes will find it in
tabi.

### 4.3 `.tower/quarantine` holds the compositor's tree listing at **r81's own pin**

`.tower/quarantine/fleet-root-strays-20261026T2055/tree.json` is the GitHub tree of
`https://api.github.com/repos/hyprwm/Hyprland/git/trees/efb50993780079460b0cbed1363e2166a2de1d9f` —
`sha= efb50993780079460b0cbed1363e2166a2de1d9f`, which is **the exact commit S479 pins for this round**
(`claims-declaration-r81.md`: "S479 = Hyprland `CMakeLists.txt` at `efb50993`") and the commit the frozen
receipt reports live: "`Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f`"
(`.ufo/waves/round-81/receipts/measurement-c2-r81.txt:3`). It lists:

```
1721:      "path": "protocols/wlr-layer-shell-unstable-v1.xml",
6835:      "path": "src/protocols/LayerShell.cpp",
6843:      "path": "src/protocols/LayerShell.hpp",
```

This is **nobody's** artifact — a quarantined fleet-root stray — yet it is the layer-shell protocol and
the compositor's `LayerShell` implementation, at the round's own pinned revision. It must be attributed to
"upstream source, quarantined stray", never to a lane.

### 4.4 `kotoba`'s fixture is called "composition" and carries `waybar`/`omarchy` text

`kotoba-shokunin/verifiers/fixtures/compare-harness-independent/record-map-24-composition/live.json` (and
its `record-map-24-control` twin) hold an omp skill-catalogue record map. Its `waybar` strings are the
**`omarchy` skill's own `description`**:

```
"REQUIRED for end-user customization of Linux desktop, window manager, or system config. Use when
editing ~/.config/hypr/, ~/.config/waybar/, … Triggers: Hyprland, window rules, animations,
keybindings, monitors, gaps, borders, blur, opacity, waybar, walker, … layer rules, workspace settings,
display config, and user-facing omarchy commands. Excludes Omarchy source development in
~/.local/share/omarchy/ and `omarchy dev` workflows.\n"
```

That single string contains `waybar`, `keybindings`, `layer rules` and `omarchy` — four of this round's
tokens — inside a directory literally named `…-composition`. It is skill-frontmatter text, kotoba's
ground, and has nothing to do with a bar.

### 4.5 How this finding prevents the mistake

A later census needs one rule per family, keyed on **subject + mechanism**, never on the token:

- **C1 (a)/(b).** Merge only on `applyExclusive` / `arrangeLayerArray` / `CReservedArea` / `addreserved`
  **in a file that computes a box, zone or attribution** — i.e. in an instrument or a corpus entry with a
  band/box subject. The bare words `exclusive`, `reserved`, `band`, `layer`, `composition` merge nothing
  (H1, H2, H4, H5). Files 4.1–4.3 are *copies or upstream listings*, recognisable because every hit line
  is prefixed with the mado path (`mado-shokunin/tools/…`) or is a `tree.json` path entry.
- **C2 (c).** Merge only on the **pair** (`omarchy menu keybindings` | `omarchy-menu-keybindings`) *and* a
  column operation (`cut -c`). `action column` alone is 233 kaidoku files (H3).
- **C2 (d).** Merge only when the pgrep **subject** matches *and* the assertion is a PID-list/exit-status
  pair. A count (`| wc -l`), an identity claim, or a different process name is another row (H6).
- **Attribution.** A file's lane is its **directory**, not the lane named inside its content. All four
  artifacts above live in `kumitate`/`tabi`/`.tower`/`kotoba` directories while carrying mado's words.

---

## 5. Contradiction observed while reading (reported, not absorbed)

Not my seat's ground, but a census will read these three artifacts together and they do not agree. Stated
plainly.

The round's C1 ground is described with **three different class sets** under one phrase:

1. `corpus/knowledge/bar-footprint-composition-r80.md:188-189` — the predecessor:
   "`four classes are wrong, all outside the frozen 33's declared shapes`", and §11 enumerates
   `:192` (1 centring past a negative tie), `:197` (2 auto zone on a dynamic band size),
   `:203` (3 auto on a corner/parallel anchor pair), `:205` (**4 a declared surface with no `exclusive` key**).
2. `claims-declaration-r81.md:27-28` — "`The bar-footprint join models the four reachable classes round 80
   recorded as \`NOT_MODELLED\``", but its item 4 is **the vertical gate and its band** (a left dock). That
   class is *not* in r80 §11's four; r80 lists the left/right attribution vector among things
   "`unpinned but *correct* in the tool (probed, no case)`" (`:210-211`).
3. `.ufo/reports/round-81/mado.md:14-15` — "`models the three reachable classes round 80 recorded as
   \`NOT_MODELLED\``", and `:155` narrows it: "`the round-80 entry's \`NOT_MODELLED\` class list (§11 items 1–3)`".
   Its enumerated third bullet is the `hyprutils >= 0.14.0` **pin**, which is a licence for the tag, not
   one of §11's classes.

So: 4 (r80) vs 4 (declaration, different membership) vs 3 (fleet report). Additionally, **r80 §11 item 4
is still open at r81**: `tools/mado-barfoot.py:633` still reads
`exclusive = item.get("exclusive", "auto")` (the protocol default is `0` per r80 `:206-207`), and **0 of
the 39 frozen cases** declares a surface without an `exclusive` key (checked over
`c1-cases-r81.json`: `surfaces declared without an exclusive key: 0`).

Consequence for a census: the only stable enumerator of this round's C1 ground is the **six new case
names** (`overflow-tie-negative`, `auto-dynamic-band-refused`, `auto-corner-edge`, `auto-all-four-edge`,
`auto-parallel-edge`, `auto-left-dock`) plus the 33 carried ones — never the phrase "the four classes".
Whether the count discrepancy is a declaration defect is the L1's call, not mine; I report that the three
artifacts disagree and that one r80 class has no r81 case.

---

## 6. Limits of this scan

- **Not verified by me: the dispatcher identity.** The C2 row's argv is `omarchy menu keybindings --print`;
  the claim cites the payload `bin/omarchy-menu-keybindings:164`. I did not open the host dispatcher
  `~/.local/share/omarchy/bin/omarchy` — it is outside the seat's pinned ground and outside the lane. What
  I can quote is the frozen receipt's **live** run of exactly that argv:
  "`MADO_R81_PROBE: name=keybindings-actions row=24 kind=action_column match=yes rc=0 out=' → Terminal\n → Tmux\n → Browser\n → File manager\n → Launch apps\n → Omarchy menu…'`"
  (`.ufo/waves/round-81/receipts/measurement-c2-r81.txt:24`), and the payload's `--print` branch at
  `S473.txt:243`. The row is live-verified; the dispatcher chain is `[INFERENCE]` from
  `bin/omarchy-menu:85` (`*Keybindings*) omarchy-menu-keybindings ;;`), which is a round-18 fetch inside
  mado, not a live read.
- **The fleet-root report appeared mid-scan.** An `ls .ufo/reports/round-81/` earlier in this scan did not
  list `mado.md`; a later `ls -la` shows it at `Nov 4 09:49` (concurrent L1 write, `TIPTIP` in its header).
  It is a mado artifact at the fleet root; I read it as evidence and did not touch it.
- **Two earlier sweep attempts were wrong and were re-run.** The first `sweep-b` dumped 500+ `action column`
  hits (a homonym, now quantified instead of quoted) and the first `sweep-g` never `cd`'d into the package,
  so its "no hit" was vacuous (rc 2, nonexistent paths). Both are fixed and the captures above are from the
  re-run; the discarded outputs are not cited.
- **Register-based, not exhaustive.** "Lane source" here means the files a lane tracks outside `.ufo/waves`;
  wave scratch inside `.ufo/waves` was included only for the per-file counts in `sweep-c-pgrep.txt`. A
  census that includes wave scratch will find far more `pgrep -x` noise (tabi's own `dnclone` and
  `CritNoHarm` copies dominate the count).

STATUS: ok
