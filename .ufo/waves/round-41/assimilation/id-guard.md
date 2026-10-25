# Round-41 assimilation — id-collision guard (operator item 10)

Seat `ExecAssimIdGuard`, wave `w1`, round 41 (2026-10-25). Lane `mado-shokunin`, base
`ab2bfaab661c846d1de9d58c01651cd156a13949`, freeze `60c3914154333180450d5da27ba222d5763cc56a`.
Working directory: this one (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/assimilation`); the shokuknow checkout was read, never written.

Contract clauses this implements: `CORPUS.md:152-153` — "The maintained `scripts/sources-census.sh` CLI
accepts 0–3 leading ASCII spaces before" (Markdown table rows), so a column-zero-only extractor
false-greens an indented row; and `PROVINCE.md:75` — "documentation written in a localized channel — is
outside the province", which is why the Japanese-language staged rows (S230, S323) are mapped but are not
citable by the successor entry.

## 1. Command run (the procedure, verbatim)

```bash
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Result: **reg=219 staged=147 coll=27** (`wc -l` on the three files; `uniq -d` on each id file prints
nothing, so neither side holds a duplicate id).

Extractor coverage is total for these inputs, not merely non-empty: neither file holds a row at 4+
leading spaces (`grep -cE '^ {4,}\|[[:space:]]*S[0-9]{3,}'` = 0 for both), and the extracted counts equal
the row counts (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` = 219 / 147). A row at 4+ spaces would be
indented code under the contract and is absent here.

Inputs (the exact bytes the extractor read):

```
51a65515231b0a180f88c4fa1bc71482afa5f3eaeede4bdfbe6c4869493812ce  mado-shokunin/corpus/SOURCES.md            (469 lines, 219 registry rows)
684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0  shokuknow/merge/mado/SOURCES.append.md  (153 lines, 147 rows)
```

Outputs:

```
744a99450f29cd8f9db0bcf35dc26f832dbdc357ca141f3ef57be95e903e4424  $A/reg-ids
079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d  $A/staged-ids
aad91fd08891238d70923bff6da469fb558207fa752d41e8e9247576688e020a  $A/collisions
```

## 2. `reg-ids` — the lane registry (219 ids)

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012
S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024
S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036
S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048
S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060
S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072
S073 S074 S075 S076 S077 S078 S079 S080 S081 S082 S083 S084
S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096
S097 S098 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108
S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120
S121 S122 S123 S124 S125 S126 S127 S128 S129 S130 S131 S132
S133 S134 S135 S136 S137 S138 S139 S140 S141 S142 S143 S144
S145 S146 S147 S148 S149 S150 S151 S152 S153 S154 S155 S156
S157 S158 S159 S160 S161 S162 S163 S164 S165 S166 S167 S168
S169 S170 S171 S172 S173 S174 S175 S176 S177 S178 S179 S180
S181 S182 S183 S184 S185 S186 S187 S188 S189 S196 S201 S202
S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214
S215 S216 S217 S218 S219 S220 S221 S253 S258 S277 S278 S279
S280 S281 S282
```

Range: S001…S282, non-contiguous by design (append-only ids are never reused, so gaps below the
maximum are not free candidates). Row count cross-check: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'
corpus/SOURCES.md` = 219; `grep -cE '^ {1,3}\|' corpus/SOURCES.md` = 0 (the live registry is all
column zero today, which is why the guard must be proved on a fixture, not on the live file).

## 3. `staged-ids` — the staged append set (147 ids)

```
S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214
S215 S216 S217 S218 S219 S220 S221 S222 S223 S224 S225 S226
S227 S228 S229 S230 S231 S232 S233 S234 S235 S236 S237 S238
S239 S240 S241 S242 S243 S244 S245 S246 S247 S248 S249 S250
S251 S252 S253 S254 S255 S256 S257 S258 S259 S260 S261 S262
S263 S264 S265 S266 S267 S268 S269 S270 S271 S272 S273 S274
S275 S276 S277 S278 S279 S280 S281 S282 S283 S284 S285 S286
S287 S288 S289 S290 S291 S292 S293 S294 S295 S296 S297 S298
S299 S300 S301 S302 S303 S304 S305 S306 S307 S308 S309 S310
S311 S312 S313 S314 S315 S316 S317 S318 S319 S320 S321 S322
S323 S324 S325 S326 S327 S328 S329 S330 S331 S332 S333 S334
S335 S336 S337 S338 S339 S340 S341 S342 S343 S344 S345 S346
S347 S348 S349
```

Range: S203…S349, contiguous.

## 4. `collisions` — 27 ids already held by the lane

```
S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214
S215 S216 S217 S218 S219 S220 S221 S253 S258 S277 S278 S279
S280 S281 S282
```

Reading: the staged set re-lists 19 lane rows (S203–S221) plus S253, S258, S277 and the five rows
opened in round 40 (S278–S282). Any staged row among these **must** be renumbered in scratch before an
append; the lane registry is never rewritten.

## 5. Guard proof — the guard can fail, and the column-zero variant cannot

Fixture directory `$D` (a `mktemp -d`, removed after the hashes below were recorded; the files it held
are kept under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/assimilation/proof/`), no git, no repo, no write outside `/tmp` and this directory.

### F1 — the required fixture: a scratch registry copy holding one 2-space-indented `  | S002 |` row

```bash
sed -n '1,12p' corpus/SOURCES.md > "$D/SOURCES.f1.md"     # contract header + Registry header + separator
printf '  | S002 | ... | queued | 2026-10-25 | 180d | — |\n' >> "$D/SOURCES.f1.md"
printf '| S002 | ... | queued | 2026-10-25 | 180d | — |\n'   > "$D/staged.f1.md"
```

(a) the indented row is a census row, not code — the validator accepts the file with no finding:

```
### F1 census validate
file	ok	/tmp/tmp.peVC4V0sOT/SOURCES.f1.md
census_exit=0
```

(b) the specified 0–3-space guard sees it:

```
0-3 pattern : reg=1 (S002)  staged=1 (S002)  collisions=1  ->  S002
```

(c) the column-zero-only pattern false-greens it:

```
^\| pattern  : reg=0         staged=1 (S002)  collisions=0  ->  (empty)
```

`collisions` is nonempty for the indented fixture and empty for the column-zero extractor: the guard is
proved able to fail, and the defect it exists to catch is reproduced.

### F3 — the same proof on a copy of the *live* registry (a new id, indented, inside the table)

`S002` already exists at column zero in the live registry, so the live-copy variant uses an id the lane
does not hold (`S900`), inserted directly after the last registry row (line 231, still inside the table):

```
0-3 pattern : reg=220  staged=1 (S900)  collisions=1  ->  S900
^\| pattern  : reg=219  staged=1 (S900)  collisions=0  ->  (empty)
```

The 0–3 extractor sees one more row than the column-zero extractor, and that row is the injected one
(`comm -13` of the two id lists = `S900`). Census on that copy raises no finding of its own — no `S900`,
`E03` or `E12` line; the finding histogram of the F3 transcript is:

```
    247 E11
      1 W01
      7 W04
```

Those are baseline: the pristine `corpus/SOURCES.md` yields **247** `E11` lines and so does the F3 copy
(`247` each), so the fixture adds none.

### F2 — the validator's own witness (cross-check, not part of the requirement)

Inserting `  | S002 |` into a copy of the live registry makes the census report `E03 S002 duplicate id`,
i.e. the maintained parser also treats an indented row as a row. That is why F1, not F2, is the decisive
fixture: on the live copy the column-zero extractor still finds the *pre-existing* column-zero S002.

Fixture hashes (sha256):

```
93851bdb0ce0140b542b6be35609cad6bb80e504e4c99d667b84c6a59c454420  /tmp/tmp.peVC4V0sOT/SOURCES.f1.md
dc7052c4218de097d17f649844781931647cfa0e339bc7860b37edcf5289b668  /tmp/tmp.peVC4V0sOT/staged.f1.md
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  /tmp/tmp.peVC4V0sOT/f1.reg03
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  /tmp/tmp.peVC4V0sOT/f1.staged
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  /tmp/tmp.peVC4V0sOT/f1.coll03
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /tmp/tmp.peVC4V0sOT/f1.reg0
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /tmp/tmp.peVC4V0sOT/f1.coll0
d3f1cbfea0d0e9539f9aa12df459181a442ec6ed94b9d0f0ffa80724806dbbb9  /tmp/tmp.peVC4V0sOT/SOURCES.f3.md
164712415cf6b2daa2b4df44f697bae4b617c636e45e0fe7c2c58d2b2ffcbbc1  /tmp/tmp.peVC4V0sOT/staged.f3.md
e310d24a36c2b9ba2e2876ef01b44fe791757906b509f82142671410671d5e13  /tmp/tmp.peVC4V0sOT/f3.reg03
f4ca6bc50c78a70dae56dd25740edcc7e8b1c8e2e738727720918d033776320a  /tmp/tmp.peVC4V0sOT/f3.staged
f4ca6bc50c78a70dae56dd25740edcc7e8b1c8e2e738727720918d033776320a  /tmp/tmp.peVC4V0sOT/f3.coll03
744a99450f29cd8f9db0bcf35dc26f832dbdc357ca141f3ef57be95e903e4424  /tmp/tmp.peVC4V0sOT/f3.reg0
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /tmp/tmp.peVC4V0sOT/f3.coll0
```

## 6. Focus theme — the staged ids the successor entry draws on

The rows cited by the twelve staged files named in the round (via their `source:` lines), with
provenance (`<staged file>:<line>`):

| staged id | cited by |
|---|---|
| S227 | focus-control-surfaces-r28:8 |
| S229 | focus-control-surfaces-r28:9 |
| S230 | focus-control-surfaces-r28:10 |
| S273 | focus-grab-seat-semantics-r8:7 |
| S274 | focus-grab-seat-semantics-r8:6 |
| S275 | focus-grab-seat-semantics-r8:8 |
| S280 | focus-grab-seat-semantics-r8:9 |
| S288 | focus-grab-observed-semantics-r9:8 |
| S293 | focus-grab-observed-semantics-r9:10 |
| S294 | focus-grab-observed-semantics-r9:9 |
| S295 | focus-grab-focus-selection-r10:10 |
| S296 | focus-grab-focus-selection-r10:11 |
| S306 | focus-grab-mouse-target-r11:10 |
| S307 | focus-grab-mouse-target-r11:11 |
| S308 | focus-grab-mouse-target-r11:12 |
| S313 | focus-grab-whitelist-admission-r12:9 |
| S314 | focus-grab-whitelist-admission-r12:10 |
| S317 | focus-grab-keyboard-routing-r13:10 |
| S323 | focus-grab-keyboard-routing-r13:13 |
| S324 | focus-grab-keyboard-routing-r13:11 |
| S325 | focus-grab-keyboard-routing-r13:12 |
| S328 | focus-grab-protocol-live-on-host-r14:9 |
| S329 | focus-grab-protocol-live-on-host-r14:10 |
| S330 | focus-grab-protocol-live-on-host-r14:11 |
| S331 | focus-grab-protocol-live-on-host-r14:12 |
| S332 | focus-grab-protocol-live-on-host-r14:13 |
| S338 | focus-grab-has-no-client-here-r15:7 |
| S244 | privileged-client-surface-r29:8 |
| S218 | compositor-focus-manipulation-literature-r26:7 |
| S278 | wayland-input-security-literature-r8:6 |
| S279 | wayland-input-security-literature-r8:7 |

31 source lines, 31 distinct ids (no id is cited twice). Sorted:

```
S218 S227 S229 S230 S244 S273 S274 S275 S278 S279 S280 S288 S293 S294 S295 S296 S306 S307 S308 S313
S314 S317 S323 S324 S325 S328 S329 S330 S331 S332 S338
```

- **Forced renumber (4 ids, present in `collisions`):** `S218 S278 S279 S280` — the lane already holds
  these ids for other documents.
- **Identity-eligible (27 ids, absent from `collisions`):** `S227 S229 S230 S244 S273 S274 S275 S288 S293
  S294 S295 S296 S306 S307 S308 S313 S314 S317 S323 S324 S325 S328 S329 S330 S331 S332 S338` — free in
  the lane today, but see §7: adoption by identity is not what the map recommends, because several of
  these ids name *other* documents in the staged set.

Every one of the 31 staged rows was checked in `merge/mado/SOURCES.append.md`: each row's `source` cell
names the same document as the staged file's `source:` line (31/31 matched, 0 mismatched).

## 7. Renumber map — by DOCUMENT (URL → new id), never by arithmetic

The lane's registry tops at **S282**, so the first free lane id is **S283**; ids are append-only and
never reused, so gaps below S282 are not candidates. The staged theme cites **22 distinct documents**
across its 31 rows (the focus-grab XML is cited three times — S229, S274, S294 — `FocusGrab.cpp` four
times, `SeatManager.cpp` three times, arXiv 2604.18860 three times). The map assigns one id per
document, in the order the documents first appear in the staged files (file order: focus-control-surfaces-r28,
then the focus-grab series r8→r15, then privileged-client-surface-r29, compositor-focus-manipulation-literature-r26,
wayland-input-security-literature-r8):

| new lane id | document | staged citations (file:line(id)) | lane URL hits |
|---|---|---|---|
| `S283` | https://github.com/hyprwm/Hyprland/issues/565 | focus-control-surfaces-r28:8(S227) | 0 |
| `S284` | https://raw.githubusercontent.com/hyprwm/hyprland-protocols/main/protocols/hyprland-focus-grab-v1.xml | focus-control-surfaces-r28:9(S229)<br>focus-grab-seat-semantics-r8:6(S274)<br>focus-grab-observed-semantics-r9:9(S294) | 0 |
| `S285` | https://amgsk.dev/posts/hyprland-rules/ | focus-control-surfaces-r28:10(S230) | 0 |
| `S286` | https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/protocols/FocusGrab.cpp | focus-grab-seat-semantics-r8:7(S273)<br>focus-grab-focus-selection-r10:10(S295)<br>focus-grab-mouse-target-r11:12(S308)<br>focus-grab-whitelist-admission-r12:10(S314) | 0 |
| `S287` | lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt | focus-grab-seat-semantics-r8:8(S275) | 0 |
| `S288` | https://arxiv.org/abs/2604.18860 | focus-grab-seat-semantics-r8:9(S280)<br>focus-grab-keyboard-routing-r13:12(S325)<br>compositor-focus-manipulation-literature-r26:7(S218) | 0 |
| `S289` | https://quickshell.org/docs/v0.3.1/types/Quickshell.Hyprland/HyprlandFocusGrab/ | focus-grab-observed-semantics-r9:8(S288) | 0 |
| `S290` | lanes/mado/round9/fetch/host-compositor-log-scan.txt | focus-grab-observed-semantics-r9:10(S293) | 0 |
| `S291` | https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/protocols/FocusGrab.hpp | focus-grab-focus-selection-r10:11(S296) | 0 |
| `S292` | https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/managers/SeatManager.cpp | focus-grab-mouse-target-r11:10(S306)<br>focus-grab-whitelist-admission-r12:9(S313)<br>focus-grab-keyboard-routing-r13:10(S317) | 0 |
| `S293` | https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/managers/SeatManager.hpp | focus-grab-mouse-target-r11:11(S307) | 0 |
| `S294` | https://r.jina.ai/https://dfrws.org/wp-content/uploads/2025/05/Uncovering-Linux-desktop-espionage.pdf | focus-grab-keyboard-routing-r13:11(S324) | 0 |
| `S295` | https://www.lightning-assist.com/ja/blog/text-expander-wayland | focus-grab-keyboard-routing-r13:13(S323) | 0 |
| `S296` | lanes/mado/round14/fetch/host-focus-grab-portal-advertisement.txt | focus-grab-protocol-live-on-host-r14:9(S328) | 0 |
| `S297` | https://raw.githubusercontent.com/hyprwm/xdg-desktop-portal-hyprland/master/src/core/PortalManager.cpp | focus-grab-protocol-live-on-host-r14:10(S329) | 0 |
| `S298` | https://raw.githubusercontent.com/quickshell-mirror/quickshell/master/src/wayland/hyprland/focus_grab/grab.cpp | focus-grab-protocol-live-on-host-r14:11(S330) | 0 |
| `S299` | https://raw.githubusercontent.com/hyprwm/hyprland-protocols/main/README.md | focus-grab-protocol-live-on-host-r14:12(S331) | 0 |
| `S300` | https://raw.githubusercontent.com/hyprwm/hyprland-protocols/main/protocols/hyprland-input-capture-v1.xml | focus-grab-protocol-live-on-host-r14:13(S332) | 0 |
| `S301` | lanes/mado/round15/fetch/host-focus-grab-client-sweep.txt | focus-grab-has-no-client-here-r15:7(S338) | 0 |
| `S302` | https://blog.ce9e.org/posts/2025-10-03-wayland-security/ | privileged-client-surface-r29:8(S244) | 0 |
| `S303` | https://publications.mupuf.org/publication/2014/10/09/security-in-wayland-based-desktop-environments/ | wayland-input-security-literature-r8:6(S278) | 0 |
| `S304` | https://api.archives-ouvertes.fr/search/?q=halId_s:hal-04806278&fl=title_s,authFullName_s,conferenceTitle_s,producedDate_s,uri_s,abstract_s,docType_s&wt=json | wayland-input-security-literature-r8:7(S279) | 0 |

Rules that make this map safe to use:

1. **The citation moves with the document.** An entry's `source:` line is rewritten to the id of the URL
   it names. `old_id + offset` is never the rule: the staged ids and the new ids interleave — the map's
   `S288` is arXiv 2604.18860 while staged `S288` is the Quickshell doc page; the map's `S293` is
   `SeatManager.hpp` while staged `S293` is the round-9 host log — so arithmetic mis-points by
   construction.
2. **Duplicate citations collapse.** Three staged rows name the focus-grab XML and four name
   `FocusGrab.cpp`; each document takes exactly one new id, and the entry cites that id once per
   document, not once per staged file.
3. **No document is already in the lane.** The `lane_url_hits` column greps the document's URL token
   against `corpus/SOURCES.md` (0 hits for all 22). Broader check: 26 distinctive tokens covering the
   whole theme — `issues/565`, `hyprland-focus-grab-v1.xml`, `amgsk.dev`, `FocusGrab.cpp`,
   `host-focus-grab-and-timeout.txt`, `2604.18860`, `HyprlandFocusGrab`, `host-compositor-log-scan.txt`,
   `FocusGrab.hpp`, `SeatManager.cpp`, `SeatManager.hpp`, `dfrws.org`, `lightning-assist.com`,
   `host-focus-grab-portal-advertisement.txt`, `PortalManager.cpp`, `focus_grab/grab.cpp`,
   `hyprland-protocols`, `hyprland-input-capture-v1.xml`, `host-focus-grab-client-sweep.txt`, `ce9e.org`,
   `publications.mupuf.org`, `archives-ouvertes.fr`, `quickshell`, `focus_grab`, `focus-grab`,
   `focus grab` — each returns `grep -c -F` = **0**. No lane row can be re-pointed instead, so every
   document genuinely opens a new row (and the successor entry cannot inherit a citation it does not own).
4. **Two documents are mapped but not citable** (out-of-province, `PROVINCE.md:75`): S230 → `S285`
   (amgsk.dev, Japanese) and S323 → `S295` (lightning-assist.com `/ja/`, Japanese). The map keeps them
   because the staged set cites them; the successor entry must not.
5. **The new-id range overlaps the staged range** (S283–S304 ⊂ S203–S349). That is not a collision with
   the lane — it is the ordinary consequence of the staged package having reserved S203–S349 before this
   lane's rounds 40–41 appended S278–S282. The guard is `comm -12` against `corpus/SOURCES.md`, which is
   what §4 reports; it must be re-run at the append, not once at planning time.

## 8. Bounds and tool state

- Writes: `$A/reg-ids`, `$A/staged-ids`, `$A/collisions` (the three files the procedure names),
  `$A/focus-sources.txt`, `$A/renumber-map.tsv`, `$A/proof/*` (fixtures + hashes + census transcripts),
  this file, and the seat report `.ufo/waves/round-41/w1/ExecAssimIdGuard.md`. Nothing else; no tracked
  file edited; no write into the shokuknow checkout; no git/jj command of any kind (not even read-only);
  no compositor or Wayland verb; no package transaction; pacman untouched.
- Tools: none installed (coreutils `grep`/`sort`/`comm`/`sha256sum`, `python3`, and the repo's own
  `scripts/sources-census.sh validate`, read-only).
- Scratch: one `mktemp -d` (path recorded in `$A/proof/scratch-path.txt`), removed after the hashes were
  recorded; its fixtures survive as `$A/proof/SOURCES.f1.md`, `staged.f1.md`, `SOURCES.f3.md`,
  `staged.f3.md` and the derived id files.
