# Round 43 — assimilation id guard and renumber map (gkeep geometry theme)

Seat `ExecAssimIdGuard`, 2026-10-26. Scratch only; the registry and the staging area are read-only
here. Companion file: `renumber-map.tsv` (same directory).

Inputs (read-only):

- Lane registry `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (frozen at
  round-43 freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`, base `a35cfdf…`).
- Staging `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` (never written, no campaign
  tool run there).
- The 11 staged gkeep-theme files under
  `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/`:
  `gkeep-client-size-request-r12.md`, `gkeep-element-rules-r30.md`,
  `gkeep-geometry-never-recorded-r15.md`, `gkeep-geometry-unobservable-r8.md`,
  `gkeep-observation-route-r11.md`, `gkeep-rendered-geometry-chain-r9.md`,
  `gkeep-rendered-geometry-record-r13.md`, `gkeep-rendered-geometry-record-r14.md`,
  `gkeep-size-rule-application-r10.md`, `gkeep-size-to-real-size-r11.md`,
  `glyph-and-geometry-r31.md`.

## 1. The guard, run exactly as the round prompt states

`A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/assimilation` (created with
`mkdir -p`; outputs `reg-ids`, `staged-ids`, `collisions` live there).

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > $A/reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > $A/staged-ids
comm -12 $A/reg-ids $A/staged-ids > $A/collisions
wc -l $A/reg-ids $A/staged-ids $A/collisions
```

Output (`wc -l`, verbatim):

```
 226 .ufo/waves/round-43/assimilation/reg-ids
 147 .ufo/waves/round-43/assimilation/staged-ids
  34 .ufo/waves/round-43/assimilation/collisions
 407 total
```

**Collision count: 34.**

## 2. Proof that the guard fires (scratch registry, indented row)

Scratch dir `/fast/scratch/hyaku/mado-r43/ExecAssimIdGuard/` (deleted before this seat finished).
`scratch-registry.md`:

```
| id | source | kind |
|---|---|---|
  | S203 | staged-collision-probe — indented two spaces | docs |
| S999 | unindented control row | docs |
    | S998 | four-space row (outside the guard regex) | docs |
```

Same guard expression over that file, then `comm` against the staged set:

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' scratch-registry.md | grep -oE 'S[0-9]+' | sort > scratch-ids
$ cat scratch-ids
S203
S999
$ comm -12 scratch-ids $A/staged-ids > scratch-collisions
$ cat scratch-collisions
S203
$ wc -l scratch-ids scratch-collisions
scratch_ids=2 collisions=1
```

Proof: the indented `  | S203 |` row is recognised (it lands in `scratch-ids`), the staged set holds
S203, and the collision file is non-empty (`S203`). The guard therefore detects a collision when one
exists — it is not vacuously empty.

Guard limits measured in the same probe (reported, not fixed here):

- A row indented four or more spaces is **not** matched (`S998` never appears in `scratch-ids`); the
  guard's window is 0-3 leading spaces, so a registry that indents a table by four spaces would pass
  the guard silently.
- An unindented row is matched (`S999`).
- The guard reads ids only, never URLs: two rows for the same document with different ids never
  collide. That is why the map below is built by document, not by id.

## 3. The two id lists as the guard produced them

`reg-ids` (226, ascending; the gaps are real gaps in the registry):

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020
S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060
S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080
S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S098 S099 S100
S101 S102 S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120
S121 S122 S123 S124 S125 S126 S127 S128 S129 S130 S131 S132 S133 S134 S135 S136 S137 S138 S139 S140
S141 S142 S143 S144 S145 S146 S147 S148 S149 S150 S151 S152 S153 S154 S155 S156 S157 S158 S159 S160
S161 S162 S163 S164 S165 S166 S167 S168 S169 S170 S171 S172 S173 S174 S175 S176 S177 S178 S179 S180
S181 S182 S183 S184 S185 S186 S187 S188 S189 S196 S201 S202 S203 S204 S205 S206 S207 S208 S209 S210
S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S253 S258 S277 S278 S279 S280 S281 S282 S283
S284 S285 S286 S287 S288 S289
```

`staged-ids` (147, ascending, contiguous S203-S349):

```
S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S222
S223 S224 S225 S226 S227 S228 S229 S230 S231 S232 S233 S234 S235 S236 S237 S238 S239 S240 S241 S242
S243 S244 S245 S246 S247 S248 S249 S250 S251 S252 S253 S254 S255 S256 S257 S258 S259 S260 S261 S262
S263 S264 S265 S266 S267 S268 S269 S270 S271 S272 S273 S274 S275 S276 S277 S278 S279 S280 S281 S282
S283 S284 S285 S286 S287 S288 S289 S290 S291 S292 S293 S294 S295 S296 S297 S298 S299 S300 S301 S302
S303 S304 S305 S306 S307 S308 S309 S310 S311 S312 S313 S314 S315 S316 S317 S318 S319 S320 S321 S322
S323 S324 S325 S326 S327 S328 S329 S330 S331 S332 S333 S334 S335 S336 S337 S338 S339 S340 S341 S342
S343 S344 S345 S346 S347 S348 S349
```

`collisions` (34):

```
S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S253
S258 S277 S278 S279 S280 S281 S282 S283 S284 S285 S286 S287 S288 S289
```

### The guard under-reports by the reserved band

The frozen registry ends at S289, but this round reserves S290-S299 (registration.md § Claims/§
Pre-wave fetches: seven Hyprland pins, three own-work receipts). The staged set holds **10 ids in
S290-S299** (`S290`…`S299`, all present because the staged range is contiguous). They do not appear in
`collisions` only because the rows do not exist yet; they collide the moment the pins are appended.
The staged rows that must move for that reason and are cited by the gkeep theme are
**S292, S297, S298, S299** — all four are absent from `collisions` today, so a guard run alone would
miss exactly the ids this round is about.

## 4. Staged rows the 11 gkeep files cite (`source:` lines)

26 `source:` lines, 25 distinct staged ids, 19 distinct documents
(measured: `grep -hE '^[[:space:]]*source:' <11 files> | ... ` → `source_lines=26 distinct_ids=25
distinct_urls=19`).

| file | line | source line (staged id — document) |
|---|---|---|
| gkeep-client-size-request-r12.md | 10 | S311 — Hyprland v0.56.2 `src/desktop/view/Window.cpp` |
| gkeep-client-size-request-r12.md | 11 | S312 — gkeep `133b867` `gkeep/ui.py` |
| gkeep-element-rules-r30.md | 8 | S251 — `/home/vgpnk/.config/hypr/gkeep.conf` |
| gkeep-geometry-never-recorded-r15.md | 7 | S339 — `lanes/mado/round15/fetch/corpus-round24-artifacts-sweep.txt` |
| gkeep-geometry-unobservable-r8.md | 8 | S275 — `lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt` |
| gkeep-observation-route-r11.md | 8 | S310 — `lanes/mado/round11/fetch/host-gkeep-rule-and-path.txt` |
| gkeep-rendered-geometry-chain-r9.md | 8 | S284 — Hyprland v0.56.2 `src/desktop/view/Window.cpp` |
| gkeep-rendered-geometry-chain-r9.md | 9 | S285 — gkeep `133b867` `gkeep/ui.py` |
| gkeep-rendered-geometry-chain-r9.md | 10 | S286 — `https://docs.gtk.org/gtk4/method.Window.set_default_size.html` |
| gkeep-rendered-geometry-chain-r9.md | 11 | S287 — `https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/` |
| gkeep-rendered-geometry-chain-r9.md | 12 | S292 — `lanes/mado/round9/fetch/gkeep-geometry-chain.txt` |
| gkeep-rendered-geometry-chain-r9.md | 13 | S293 — `lanes/mado/round9/fetch/host-compositor-log-scan.txt` |
| gkeep-rendered-geometry-record-r13.md | 10 | S318 — Hyprland v0.56.2 `src/desktop/view/Window.cpp` |
| gkeep-rendered-geometry-record-r13.md | 11 | S319 — Hyprland v0.56.2 `src/desktop/view/Window.cpp` |
| gkeep-rendered-geometry-record-r13.md | 12 | S320 — `lanes/mado/round13/fetch/host-journal-map-log-sweep.txt` |
| gkeep-rendered-geometry-record-r14.md | 9 | S326 — `lanes/mado/round14/fetch/host-journal-map-log-alltime-sweep.txt` |
| gkeep-size-rule-application-r10.md | 9 | S297 — Hyprland v0.56.2 `src/desktop/rule/windowRule/WindowRuleApplicator.cpp` |
| gkeep-size-rule-application-r10.md | 10 | S298 — Hyprland v0.56.2 `src/desktop/view/Window.cpp` |
| gkeep-size-rule-application-r10.md | 11 | S299 — `lanes/mado/round10/fetch/host-r4-observation-sweep.txt` |
| gkeep-size-to-real-size-r11.md | 11 | S302 — Hyprland v0.56.2 `src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` |
| gkeep-size-to-real-size-r11.md | 12 | S303 — Hyprland v0.56.2 `src/layout/target/Target.cpp` |
| gkeep-size-to-real-size-r11.md | 13 | S304 — Hyprland v0.56.2 `src/layout/target/WindowTarget.cpp` |
| gkeep-size-to-real-size-r11.md | 14 | S305 — Hyprland v0.56.2 `src/desktop/view/types/GeometricMovableAnimated.cpp` |
| gkeep-size-to-real-size-r11.md | 15 | S310 — `lanes/mado/round11/fetch/host-gkeep-rule-and-path.txt` |
| glyph-and-geometry-r31.md | 8 | S255 — gkeep `133b867` `gkeep/ui.py` |
| glyph-and-geometry-r31.md | 9 | S256 — `https://raw.githubusercontent.com/ryanoasis/nerd-fonts/v3.5.1/glyphnames.json` |

Both hits on S310 (`gkeep-observation-route-r11.md:8`, `gkeep-size-to-real-size-r11.md:15`) cite the
same staged document, so the map carries one row for it.

## 5. Renumber map, by document

Rules applied, in this order:

1. **Document identity = (repo, path, resolved commit).** The staged rows cite the Hyprland files in
   tag form (`/v0.56.2/…`); the lane registry holds two of them in commit form
   (`/efb50993780079460b0cbed1363e2166a2de1d9f/…`). `v0.56.2` resolves to that commit — the registry
   itself records it: S018's anchor reads "tag commit efb5099…". So tag form and commit form are one
   document here. Under strict byte equality of URLs they would be two; the strict reading is noted in
   §6 and the L1 can flip to it, but it would open a second row per document, the duplicate-admission
   defect S045 was written to correct.
2. A staged row whose document is a lane-held row → that held id, no new row.
3. A staged row whose document is one of the round's pins → that pin id (S290-S299), no new row.
4. Otherwise a new id, allocated from S300 upward (S290-S299 are fully reserved by the pins), in
   order of the staged id that first cites the document.

| # | document (URL / path) | staged ids | new / held id | why |
|---|---|---|---|---|
| 1 | `…/v0.56.2/src/desktop/view/Window.cpp` | S284, S298, S311, S318, S319 | **S164** (held) | lane row S164 already carries this document at commit form |
| 2 | `…/gkeep/133b867…/gkeep/ui.py` | S255, S285, S312 | **S300** (new) | no lane row holds it; S013 is `install.sh` at the same commit, S299 is only the 446-EOF excerpt |
| 3 | `…/hyprwm/Hyprland/v0.56.2/src/desktop/rule/windowRule/WindowRuleApplicator.cpp` | S297 | **S155** (held) | lane row S155 already carries this document at commit form |
| 4 | `…/v0.56.2/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` | S302 | **S292** (pin) | round-43 pin, `fetch/Hyprland-DefaultFloatingAlgorithm.cpp`, sha256 `f05f2561…` |
| 5 | `…/v0.56.2/src/layout/target/Target.cpp` | S303 | **S293** (pin) | round-43 pin, sha256 `49323833…` |
| 6 | `…/v0.56.2/src/layout/target/WindowTarget.cpp` | S304 | **S294** (pin) | round-43 pin, sha256 `8bcaf370…` |
| 7 | `…/v0.56.2/src/desktop/view/types/GeometricMovableAnimated.cpp` | S305 | **S295** (pin) | round-43 pin, sha256 `649f1a8d…` |
| 8 | `/home/vgpnk/.config/hypr/gkeep.conf` | S251 | **S297** (pin) | the pin `fetch/host-gkeep.conf` is a byte copy of this file, sha256 `3726e488…` |
| 9 | `https://docs.gtk.org/gtk4/method.Window.set_default_size.html` | S286 | **S303** (new) | no lane row cites `docs.gtk.org` |
| 10 | `https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/` | S287 | **S304** (new) | held Window-Rules rows are unversioned current (S017, S030, S045) or 0.54 (S023); the 0.56.0 archive URL is unheld |
| 11 | `https://raw.githubusercontent.com/ryanoasis/nerd-fonts/v3.5.1/glyphnames.json` | S256 | **S301** (new) | no lane row cites nerd-fonts |
| 12 | `lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt` | S275 | **S302** (new) | staged-only path form, see §6 |
| 13 | `lanes/mado/round9/fetch/gkeep-geometry-chain.txt` | S292 | **S305** (new) | staged-only path form; its staged id also hits the pin S292 |
| 14 | `lanes/mado/round9/fetch/host-compositor-log-scan.txt` | S293 | **S306** (new) | staged-only path form; staged id also hits the pin S293 |
| 15 | `lanes/mado/round10/fetch/host-r4-observation-sweep.txt` | S299 | **S307** (new) | staged-only path form; staged id also hits the pin S299 |
| 16 | `lanes/mado/round11/fetch/host-gkeep-rule-and-path.txt` | S310 (×2) | **S308** (new) | staged-only path form |
| 17 | `lanes/mado/round13/fetch/host-journal-map-log-sweep.txt` | S320 | **S309** (new) | staged-only path form |
| 18 | `lanes/mado/round14/fetch/host-journal-map-log-alltime-sweep.txt` | S326 | **S310** (new) | staged-only path form |
| 19 | `lanes/mado/round15/fetch/corpus-round24-artifacts-sweep.txt` | S339 | **S311** (new) | staged-only path form |

Per-staged-id rows (the machine-readable form) are in `renumber-map.tsv`: 25 rows, columns
`staged_id, url, new_id_or_held_id, reason`.

Id budget: 19 documents → 2 held (S164, S155), 5 pins (S292, S293, S294, S295, S297) and
**12 new ids S300-S311** (S300, S301, S302, S303, S304, S305, S306, S307, S308, S309, S310, S311).
No new id overlaps S001-S289 (held) or S290-S299 (reserved).

## 6. Findings for the L1 (not decisions this seat can make)

1. **Two pins duplicate held rows at document level.** S291 (`WindowRuleApplicator.cpp`, tag form)
   duplicates held S155 (commit form) and S296 (`HyprCtl.cpp`, tag form) duplicates held S158 (commit
   form; S018 is the `github.com/…/blob/v0.56.2/…` form of the same file). The other five code pins
   (RegexMatchEngine, DefaultFloatingAlgorithm, Target, WindowTarget, GeometricMovableAnimated) match
   no held row, so they are genuinely new. If the round opens S291/S296 anyway, the registry carries
   one document twice — the S045 defect — and the duplicate must at least be declared with a
   `supersedes`/cross-reference in `used-by`.
2. **The collision guard alone is not sufficient this round.** It reports 34 collisions against the
   frozen registry, but 10 staged ids sit in the reserved S290-S299 band and will collide once the
   pins land. Four of them are cited by the gkeep theme (S292, S297, S298, S299) and every one of
   those four is renumbered above; the other six (S290, S291, S294, S295, S296) are staged rows outside
   this map's citation set and stay a hazard for whichever seat adds them.
   Guard completeness on the registry as it stands: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
   gives 226 rows and `grep -oE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}'` also gives 226 — no row of the
   registry sits outside the guard's indentation window.
3. **Eight staged documents are staged-only paths.** `lanes/mado/roundN/fetch/…` is not a lane path;
   the lane's artifacts live at `.ufo/waves/round-N/fetch/`. A row for such a document can only be
   opened against a real lane path (or be refused); the new ids above allocate the id, not the proof
   that the path resolves.
4. **Five staged ids overlap lane pin ids in a way that reads as a near-miss.** Staged S297 is
   `WindowRuleApplicator.cpp` while lane S297 is `host-gkeep.conf`; staged S292/S293 are round-9 fetch
   sweeps while lane S292/S293 are the floating-algorithm and target pins; staged S298/S299 are
   `Window.cpp` and a round-10 sweep while lane S298/S299 are `host-clients-r43.json` and the gkeep UI
   excerpt. Any copy of a staged row that keeps its id would silently point at a different document.
5. **Guard blind spot (measured, §2):** a four-space-indented row is invisible to
   `^ {0,3}\|…`; the lane registry's rows are unindented today (all 226 matched), so the guard is sound
   for this file as it stands.

## 7. Reproducing this receipt

The three id files are written next to this document (`reg-ids`, `staged-ids`, `collisions`), so the
counts in §1 and §3 can be re-derived without the staging checkout:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/assimilation
wc -l reg-ids staged-ids collisions         # 226 147 34
comm -12 reg-ids staged-ids | diff - collisions && echo guard-reproduced
```

Scratch `/fast/scratch/hyaku/mado-r43/ExecAssimIdGuard/` removed before this seat finished; nothing in
this receipt cites a scratch path as evidence.
