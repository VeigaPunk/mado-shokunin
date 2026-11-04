# R80ConnSiblings — sibling-overlap scan (read-only, report-never-absorb)

Seat: connector, round 80 wave 1. Scope: find whether any other lane already claims the ground
this round's two claims stand on — C1 layer-surface composition / per-surface reserved
attribution (`applyExclusive`, `arrangeLayersForMonitor`, `CReservedArea`) and C2's
`omarchy-menu-keybindings` chord column and `systemctl --user is-active` state/rc rows — and
whether a sibling instrument already models a layer surface.

Read-only throughout. No file outside
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-80/w1/` was written; no git/jj
mutation, no host probe, no pacman, no campaign tool. No scratch directory was created because
no command in this seat needed one (every read was a `grep`/`sed`/`git log` read verb).

Commands actually run (from `/home/vgpnk/Projects/shokunin` unless noted):

```sh
grep -rn --include='*.md' --include='*.py' --include='*.json' --include='*.txt' \
  -e applyExclusive -e arrangeLayersForMonitor -e CReservedArea */corpus/
grep -rniE --include='*.md' -e 'exclusive ?zone' -e 'layer[- ]shell' -e 'waybar' \
  -e 'arrangeLayers' -e 'applyExclusive' -e 'reserved (area|band)' <each sibling>/corpus/
grep -rniE --include='*.md' -e 'usable area' -e 'usable box' -e 'logicalBox' -e 'logical box' \
  -e 'monitor.*reserved' */corpus/knowledge*
grep -rn --include='*.md' -e 'addreserved' -e 'omarchy-menu-keybindings' -e 'COPILOT KEY' \
  -e 'code:201' .   # whole fleet, incl. .ufo
grep -rniE --include='*.md' -e '\bchord\b' -e 'per-surface' -e 'surface attribution' */corpus/knowledge*
grep -rnE --include='*.md' 'is-active' */corpus/knowledge* | grep -E 'rc[ =]?3|exit|status'
find . -path '*/tools/*' -type f \( -iname '*layer*' -o -iname '*barfoot*' -o -iname '*footprint*' \
  -o -iname '*reserve*' -o -iname '*reserved*' \) -not -path './mado-shokunin/*'
grep -rliE 'layer.shell|exclusive|reserved.area|arrangeLayers' */tools/     # whole-tool content scan
grep -rniE 'layer.shell|exclusive.?zone|applyExclusive|reserved area|bar.?footprint' ~/.agents/skills
grep -rnE 'layer.shell|exclusive|bar footprint|reserved area|compositor' */PROVINCE.md */SKILL.md
ls -R /home/vgpnk/Projects/shokuknow/merge/mado/ ; grep -rniE 'addreserved|reserved|exclusive|layer.shell|footprint' that dir
cd mado-shokunin && git log --oneline -1 62dd798b && git rev-list --count 62dd798b..e10f7e9f \
  && git cat-file -e 62dd798b:tools/mado-barfoot.py
```

## Bottom line

**No sibling lane claims either round-80 ground.** Zero fleet hits for `applyExclusive`,
`arrangeLayersForMonitor`, `CReservedArea`, `addreserved`, `usable box`, `COPILOT KEY` or
`code:201` outside this lane. What exists is adjacency only — three siblings state or cede the
plane's ownership (kotoba, tsukuroi, game-dev-3d), four touch a neighbouring method or vocabulary
(tameshi, mori, kake, tabi), and one holds an unrelated artifact (kaidoku) — plus one stale-pin
trap in the fleet's overlap census that the L1 must not read as an adjudication. **No sibling
instrument models a layer surface** — the only such model in the fleet, in the shared skill set,
or in the fleet merge staging is mado's own `tools/mado-barfoot.py`.

## Table A — C1 ground (composition / per-surface attribution / exclusive / reserved)

| sibling | path:line | contested? | what mado should say in the report |
|---|---|---|---|
| game-dev-3d | `game-dev-3d-shokunin/PROVINCE.md:75` — "Desktop/compositor display behavior belongs to `mado-shokunin` (`../mado-shokunin/PROVINCE.md:3-12`)." | **no — explicit cession to mado** | Cite as the one sibling scope file that names this plane: the only cross-lane ruling on desktop/compositor behavior routes it *to* mado. Nothing to negotiate. |
| kotoba | `kotoba-shokunin/PROVINCE.md:72` — "mado owns the Hyprland/waybar/walker/terminal config plane and display behavior read-only; it states no split with kotoba and treats the omarchy skill as read-only documentation (mado `PROVINCE.md:10`), claiming no lane SKILL.md." | **no — cites mado's ownership** | Cite as the governing ownership statement for the whole plane. Note the axis it was measured on is skill-file/prompt-craft overlap, not subject matter (see Contradiction 1). |
| kotoba | `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md:66` and `:97`, `:122`; `…-round49.md:82` | **no — but a stale pin, not an adjudication** | Do **not** cite as "no sibling claims this ground". The row classifies `none` at pin `62dd798b`, which is **363 commits behind the round-80 base `e10f7e9f` and predates `tools/mado-barfoot.py` entirely** (`git cat-file -e 62dd798b:tools/mado-barfoot.py` → absent). It never saw the r77–r80 bar-footprint ground. |
| tsukuroi | `tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.md:84` — OUT-004, `../mado-shokunin/PROVINCE.md:3-16`, "Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior." | **no — cites mado's ownership** | Cite alongside the kotoba row as the second independent statement that the plane is mado's. Its "screen/idle behavior" wording covers C1's subject matter at the ownership level only. |
| tsukuroi | `corpus/knowledge/systemd-job-transaction-plane-r75.md:18` JT2 — "A JOB_START or JOB_VERIFY_ACTIVE job is redundant when the unit is already active or reloading, a JOB_STOP when inactive or failed…" | **no — adjacent vocabulary only** | Irrelevant to C1 (bar semantics, not unit jobs). Named here only so the C2 note below can draw the line: tsukuroi owns *job* semantics, not `is-active`'s CLI mapping. |
| tameshi | `tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md:5` ("mado-shokunin opted in"), `:7-8` ("mado-shokunin **read-only**; every mutant is a byte copy under `/tmp/…`"), `:244` ("**Add a live-plane scenario with a PATH-stub `hyprctl`**") | **no — method, not ground** | tameshi owns mutation craft and has already driven *mado's* tool read-only under opt-in. mado's SKILL.md:1190/1202/1204-1205 already cedes it. Report: the 22 r80 mutants are scored by mado's own counter (`c1-r80-multisurface.py`; no `tameshi`/`mutate-and-run` reference in either r80 counter), so r80 consumes tameshi's craft **without** touching the harness. The r6 `:244` recommendation (PATH-stub `hyprctl` live-plane scenario) is still open and stays tameshi's to make — mado must not absorb it. |
| kaidoku | `kaidoku-shokunin/corpus/knowledge/2026-10-13-crash-evidence.md:16,23` — waybar core `/var/lib/systemd/coredump/core.waybar.1000…zst` | **no — a waybar *binary artifact*, not the geometry ground** | Name it as the one sibling holding waybar bytes, and state the disjointness: kaidoku reads a crashed binary, mado reads declared config and the compositor's own replies. Nothing shared, nothing to cite in the claim itself. |
| mori | `mori-shokunin/corpus/knowledge/userspace-oom-killers-r12.md:14`; `earlyoom-invocation-scope-r30.md:1` (active-or-reloading set, systemd `unit.c`) | **no — different object** | Report only that mori's "monitor" hits are OOM monitors, not displays — so C1's monitor-reserved ground has no sibling reader at all. |

## Table B — C2 ground (chord column / `is-active` state+rc)

| sibling | path:line | contested? | what mado should say in the report |
|---|---|---|---|
| tabi | `tabi-shokunin/corpus/knowledge/chromium-modifier-chords-round-57.md:3` ("the Linux host's Chromium 155 headless surface now carries the modifier-chord…"), `:41` ("three real chords Control/Alt/Meta (bits 2/1/4 per S153)"); `webview2-control-keys-round-55.md:11,44-45` | **no — homonym only** | Say the word plainly: tabi's "chord" is a **browser input-event** construct (CDP key events, modifier bitmask), mado's is a **text shape** in `omarchy menu keybindings --print`'s left column. A future fleet census keyed on the token "chord" would merge them; the report should pre-empt that with one sentence naming the objects as disjoint. |
| kake | `kake-shokunin/corpus/knowledge/keeper-timer-inert.md:38` — `$ systemctl --user is-active  webzites-keeper.timer   # rc=3 → inactive` | **no — cite, not claim** | This is the only sibling statement of the exact `is-active` rc↔state semantic C2's matcher binds, and it is a **command comment**, not a claim row, about a different unit. Report: C2's `hypridle-is-active` row is mado's; the general rc semantics belong to `systemctl(1)`, and kake's line is an adjacent observation mado may cite but must not restate as new ground. |
| tsukuroi | `corpus/knowledge/memory-arm-ver-s8.md:135` — "rc=3 → `unknown=[C1 C2 C3]`, DEGRADED, never a pass"; `degraded-triage-r4.md:318` (`is-active` = inactive, unit enabled) | **no — host-operability method** | tsukuroi owns host operability and *uses* `is-active` as a probe verb; it does not own the verb's state/exit mapping. Report: mado's C2 matcher binds the verb's output **shape**, and the lane writes to no unit — the read-only boundary tsukuroi would care about is already in `PROVINCE.md:10` ("Never mutates a running compositor state") and the r80 refinement. |
| mori | `mori-shokunin/PROVINCE.md:3` (fleet/host liveness), `corpus/knowledge/userspace-oom-killers-r12.md:14` | **no — adjacency of purpose** | mori owns "whether the host is alive"; `is-active` is one of its verbs. mado's row is not a liveness claim, it is a *runbook row with a matcher*. Report should say mado adds no host-liveness surface and probes no unit beyond the one row round 79 left unexecuted. |
| mado's own prior corpus | `corpus/knowledge/keybind-rule-semantics.md:108`, `waybar-walker-plane.md:388`, `config-health-report-r3.md:253`, `corpus/SOURCES.md:424` (S473) | **self — already owned** | `code:201` → `COPILOT KEY` and the chord column are already mado ground from earlier rounds, and the shared `omarchy` skill does **not** carry them (`grep -nE '201\|COPILOT' ~/.agents/skills/omarchy/SKILL.md` → 0 hits). Report: C2's chord grammar extends an existing mado row, it does not open new ground. |
| shared `omarchy` skill (`~/.agents/skills/omarchy/SKILL.md`) | `:270`, `:274` — "View current bindings: `omarchy menu keybindings --print`" | **no — documentation surface, ceded** | The skill names the command as a *view* verb and carries no grammar, no `code:201` rewrite, no matcher. mado's `PROVINCE.md:10` already declares the skill read-only documentation. Report: the command is cited (SKILL.md:74 "omarchy skill:272-286"), the matcher is mado's. |

### Adjacent surfaces mado should not touch (the third category, made explicit)

| neighbour | what it owns | boundary line mado's report should repeat verbatim |
|---|---|---|
| tsukuroi | host operability, system repair, unit/job semantics (`systemd-job-transaction-plane-r75.md` JT1–JT6) | mado runs the one `is-active` row and nothing else; no unit write, no service restart. `PROVINCE.md:10` "Never mutates a running compositor state" plus the r80 refinement ("No config tree, compositor, service or sibling repo is written by this round"). |
| tameshi | mutation craft and the `mutate-and-run.sh` harness | `SKILL.md:1202` — "read-only — a needed change is a recommendation to tameshi, never a patch". r80's mutants are mado's own counter, so the harness is not even loaded this round. |
| mori | fleet/host liveness, wave settlement, kill/OOM reporting | mado adds no liveness probe; the runbook row is a matcher, not a health claim. |
| kake | the web-property timer surface (`webzites-keeper.timer`) that owns the `rc=3` example | mado cites the semantic, never the property or its timers. |
| tabi | browser sessions and input-event evidence | mado's "chord" is text; tabi's is an event. No shared artifact. |
| kaidoku | shipped-artifact RE (the waybar core) | mado never reads the coredump; no byte of kaidoku's evidence is re-derived. |
| game-dev-3d | — (cedes the plane) | `game-dev-3d/PROVINCE.md:75` is a cession, so mado's report may cite it as the sibling that rules itself out. |

## Table C — does a sibling instrument already model a layer surface?

| check | result | what mado should say |
|---|---|---|
| sibling `tools/` filenames matching `*layer*`/`*barfoot*`/`*footprint*`/`*reserve*`/`*reserved*` outside mado | **none** (`find` over every `*/tools/*`, all depths) | No provenance debt: `tools/mado-barfoot.py` is the fleet's only bar-footprint/layer-surface model. |
| sibling `tools/` **file contents** for `layer.shell\|exclusive\|reserved.area\|arrangeLayers` | 8 sibling `tools/` trees match, **532 text lines, and 0 of them also mention `layer`/`surface`/`hypr`/`waybar`/`monitor`** — the hits fall in four unrelated families: `flock(2)` "exclusive" (`chousa tools/research-gate.sh:215,756,3964`), argparse `add_mutually_exclusive_group` / "are exclusive" usage strings (`kotodama:475`, `souji:1826`, `tameshi:1228`, `kama append-only-audit.py:1508`, `tsukuroi check-adjacency-anchors.py:806` and its `check-*.py` siblings), a `disposition: "exclusive"` JSON label (`kaidoku tools/round-41/c1-counter.py:492,554,563`), and "EXCLUSIVE result subsets" (`mori tools/mori-census.sh:1106`) | State it as a **verified negative with its measurement**: the only `exclusive` tokens in sibling tools are lock modes, CLI-flag conflicts and vocabulary words, and not one sibling tool line names a layer surface. Nothing to adopt, nothing to reconcile. |
| shared skills (`~/.agents/skills/*`) for `layer.shell\|exclusive.?zone\|applyExclusive\|reserved area\|bar.?footprint` | **none** | No shared-ability owner to defer to. |
| sibling `hyprctl` usage | one hit only: `tameshi …/mutation-case-mado-verify.md:46,48,141` — it drives **mado's** `mado-verify.sh` and starves `hyprctl` from PATH | Already covered by mado's cession (`SKILL.md:1190, 1202-1205`). No second instrument exists to cite. |
| mado's own instrument accounting | `PROVINCE.md:443-452` (Round-80 refinement) already names `--surfaces`, `c1-r80-multisurface.py`, `c2-r80-runbook.py`, and `bar-footprint-composition-r80.md` | Province is current at the freeze — **no inventory gap** for this round. The report can assert the tool accounting without a repair. |

## Fleet merge staging — `/home/vgpnk/Projects/shokuknow/merge/mado/`

- 71 markdown files; `MERGE-REPORT.md:3` — "Staged by `corpus-expansion-1`. **Nothing was written into the lane repo.**" 147 rows / 69 entries staged (rounds 1–16).
- Grep for `addreserved|exclusive|layer.shell|footprint|reserved` over the whole staged package returns **no ground-bearing entry** — only "preserved" (append-only amendment notices) and a truncated `S344` row.
- Nearest staged entries are **bar *content*, not bar *geometry***: `knowledge/corpus/knowledge/host-bar-producers-r28.md:1-12` (the §1 producer table: `custom/omarchy`, `custom/update`, `custom/gkeep`…), `host-bar-producers-r28.md`, `host-bar-producer-outputs-r29.md`, and `amendments/corpus/knowledge/waybar-module-text-route-r25.md` (amendment to a lane file that already exists).
- **Verdict: no staged entry touches round-80 ground.** Because the package is staged and not landed, r80 creates **no provenance debt** against it. It *does* leave one reconciliation for whenever it lands: `host-bar-producers-r28.md:34` asserts the host `~/.config/waybar/config.jsonc` is 6354 B against upstream's 5114 B — a byte claim about a file the lane's r77–r80 geometry entries also read. That is a future landing check, not an r80 claim.

## Contradictions, stated rather than smoothed

1. **The fleet's "none" is not a subject-matter ruling.** kotoba's census classification and its `PROVINCE.md:72` row measure SKILL.md/prompt-craft overlap ("it states no split with kotoba"), not whether a lane reads the same desktop object. Reading "mado = none" as evidence about layer surfaces would be a category error. Section header in the source says so: `sibling-overlap-census-round74.md:8` — "the classification rule (`:43-64`) … applied unchanged".
2. **The census is also stale in time.** Pin `62dd798b` = "round-41 verifier spot-check", **363 commits behind** the r80 base, and `tools/mado-barfoot.py` does not exist at that commit. Any dictum that "no sibling census needed because r74 already cleared mado" is unsupported.
3. **Evidence-token collision is a live risk, not a hypothetical.** tabi (browser chords) and mado (runbook chord column) now both use "chord"; mori, kake, tsukuroi all use `is-active`. Token-level fleet searches will produce false adjacencies. mado's report should discriminate by object, not by word.
4. **One open cross-lane item is being carried, not closed.** tameshi's `:244` recommendation (a live-plane scenario with a PATH-stub `hyprctl`) predates r80 and is still unimplemented. r80 neither implements it nor withdraws it; the report should name it as carried so it is not silently dropped by the wave.
5. **No contradiction to resolve between r80 and any sibling number.** The two places a sibling states something numeric near this ground — kake's `rc=3` comment and tsukuroi's JT2 vocabulary — are about different objects (a `.timer`, unit job redundancy) and agree with what C2 binds.

## Detailed results

### 1. Exact-API search (the primary test)

`applyExclusive`, `arrangeLayersForMonitor`, `CReservedArea` return hits **only** under
`mado-shokunin/`: `corpus/SOURCES.md:408` (S457), `corpus/knowledge/bar-footprint-r77.md:3,15,29`,
`bar-footprint-margins-r78.md:3,32,63`, `bar-footprint-reserve-r79.md:3,12,14,24,42`,
`corpus/README.md:133,179`, and the lessons for rounds 77/78/79. No sibling file in any lane
mentions any of the three symbols.

### 2. Whole-fleet sweep for the round's distinctive literals

- `addreserved`: **0 hits outside mado** (the only non-lane hits are fleet-level
  `.ufo/reports/round-77|79/mado.md`, i.e. this lane's own campaign reports).
- `omarchy-menu-keybindings` / `COPILOT KEY` / `code:201`: **0 hits outside mado**; inside mado
  they are S208/S473 and `keybind-rule-semantics.md:108`.
- `usable area|usable box|logicalBox|logical box`: **0 sibling hits each** (counted per term).
  `monitor.*reserved` returns exactly **2 line-hits**, both `kumitate`
  (`corpus/knowledge/ops-watchers.md:162`, `remaining-scripts-census.md:652`), and both are false
  positives: one long line carries the word "monitor" inside `ufo-l0-monitor-error-v1` and the
  word "preserved" separately ("errno code preserved"). Not a display surface.

### 3. Lane-by-lane adjacency census (three ownership statements, four neighbours)

- **game-dev-3d** — cedes the plane outright (`PROVINCE.md:75`).
- **kotoba** — owns the overlap census *method* and the skill/prompt craft axis; states mado's
  ownership and claims nothing of the object (`PROVINCE.md:72`, census `:66/:97/:122`, `:82`).
- **tsukuroi** — owns host operability and systemd *job* semantics (`systemd-job-transaction-plane-r75.md`
  JT1–JT6, `memory-arm-ver-s8.md:135`); uses `is-active` as a verb, owns neither the verb's
  mapping nor any display object.
- **kake** — one incident note with the `rc=3 → inactive` comment (`keeper-timer-inert.md:38`),
  subject `webzites-keeper.timer`.
- **tameshi** — owns mutation craft; already instruments mado's tool read-only under opt-in
  (`mutation-case-mado-verify.md:5-8,51-52,244`); mado cedes at `SKILL.md:1190,1202-1205`.
- Plus two that only brush the surface: **tabi** (browser chord homonym) and **kaidoku** (waybar
  core-dump forensics, `2026-10-13-crash-evidence.md:16,23`).

### 4. What the report can therefore assert (and what it must not)

Can assert, with these anchors:

> "No sibling lane claims the round-80 ground: a whole-fleet search for `applyExclusive`,
> `arrangeLayersForMonitor`, `CReservedArea`, `addreserved`, the chord column's `code:201`, and
> the usable-box vocabulary returns hits only inside this lane; the two lane-scope statements
> that name the plane (`kotoba/PROVINCE.md:72`, `tsukuroi/…/adjacency-anchors-r19.md:84`) assign
> it to mado, and `game-dev-3d/PROVINCE.md:75` cedes it. No sibling instrument models a layer
> surface, and `staged merge/mado/` carries no entry on it. The only sibling instruments pointed
> at mado's bytes are tameshi's mutation harness, consumed read-only per `SKILL.md:1190-1205`."

Must **not** assert: that the round-74/49 kotoba census clears this ground (wrong axis, stale
pin), or that tabi's chord work is related (homonym), or that tameshi's `:244` item is closed
(carried).

STATUS: ok — nothing missing; no scratch dir was created because no seat command required one.
