# §10 id-collision guard + quarantine slice — evidence

Seat: ExecIdGuard (round 48, w1). Source of both commands: operator prompt
`/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-48.md` §10 — id-collision block at lines
528–534 (verbatim below), quarantine block at lines 569–572. Contract clauses implemented:
`/home/vgpnk/Projects/shokunin/CORPUS.md` census clause (0–3 leading spaces) and
`/home/vgpnk/Projects/shokunin/CORPUS.md` rule 2 (append-only ids).

Lane tip at round start: `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Writes: only
`.ufo/waves/round-48/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}` (the four paths
the §10 blocks name), this file, the seat report, and scratch under
`/fast/scratch/hyaku/mado-r48/ExecIdGuard/` (removed before yield). No lane/fleet tracked file was
edited; no git/jj verb run; no package transaction; shokuknow read-only (writes were redirected
into the lane's wave dir, never into `$S`).

## 1. Command run (exactly the §10 block, lines 528–534)

```bash
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"   # nonempty -> renumber in scratch
```

Run output (`wc -l`):

```
reg=276 staged=147 coll=84
```

The `$A` directory did not exist before this seat (`ls` → "No such file or directory"); it was
created by the block itself.

Input hashes (the exact bytes the extractor read):

```
6a71f3a48e3c9733aee7465106fd11c95108efe70552ec785c92927d8da39b62  mado-shokunin/corpus/SOURCES.md  (530 lines)
684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0  shokuknow/merge/mado/SOURCES.append.md
```

(`SOURCES.append.md` hash equals round 40's `684efe8c…` and round 47's `staged-ids` hash
`079d7538…`: the staged package has not moved since round 40.)

Output hashes:

```
aa4c19563cc50d7dfa3b9e1f17f0b6c760bd71f270722805f73fea64db4fa5f0  $A/reg-ids
079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d  $A/staged-ids
8d3561a174cf5b076aab33a2246e1b5ce90756c7f1616d0072a291a7fd19d343  $A/collisions
```

## 2. Id lists (both, complete)

- `$A/reg-ids` — **276** ids, `S001`–`S339`, no duplicates (`uniq -d` → 0 lines). Extractor row
  count = 276 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` = 276), so every
  registry row yields exactly one id. 63 gaps below the max S339 (S190–S195, S197–S200,
  S222–S252, S254–S257, S259–S276 … every id the lane never opened).
- `$A/staged-ids` — **147** ids, contiguous `S203`–`S349` (349 − 203 + 1 = 147), no duplicates.
  Byte-identical to round 40 and round 47 (`079d7538…`).

Drift since round 47 (base `reg-ids` 262, `collisions` 70): the lane opened 14 registry rows, and
because the staged set is fixed at S203–S349 every one of the 14 landed inside it — collisions went
70 → 84 with **0 removed** (`comm -23 round47/collisions round48/collisions` = 0 lines,
`comm -13` = 14 lines). This is the §10 risk ("the lane registry keeps moving after the package was
built").

## 3. Collision count and ids

**84 collisions** (nonempty → the §10 renumber rule is live):

```
S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219
S220 S221 S253 S258 S277 S278 S279 S280 S281 S282 S283 S284 S285 S286 S287 S288 S289
S290 S291 S292 S293 S294 S295 S296 S297 S298 S299 S300 S301 S302 S303 S304 S305 S306
S307 S308 S309 S310 S311 S312 S313 S314 S315 S316 S317 S318 S319 S320 S321 S322 S323
S324 S325 S326 S327 S328 S329 S330 S331 S332 S333 S334 S335 S336 S337 S338 S339
```

Structure: S203–S221 (19) + S253 + S258 + S277–S339 (63) = 84. Every one of these ids names a
different document on each side (lane row vs staged row), so every adopted id in this range must be
renumbered **by document** (URL/anchor is the evidence; the id follows it) before any append. The
lane registry is never rewritten (append-only, CORPUS.md rule 2).

Staged-citation impact (`source:` lines of the 65 staged knowledge files, 139 distinct ids):
**76 of the cited ids fall in the collision set** (S209–S212, S214–S221 name lane rows opened
rounds 9–17 that are a different document from the staged S209–S221; S253, S258, S277–S339 collide
with lane rows opened through round 47). The other 63 cited ids (S222–S252, S254–S257, S259–S276,
S340–S349) are free in the lane. No staged entry is adopted this round (`Assimilation: none`
posture of wave 4), so no renumber map is emitted; the freeze owner has the lists above.

## 4. Guard proof (scratch fixture, run once)

Contract the fixture attacks: census clause "Maintained parser accepts 0–3 leading ASCII spaces
before Markdown rows" (`/home/vgpnk/Projects/shokunin/CORPUS.md:152-154` region; round-40 seat
quoted it at `:152-154`) and §10's own sentence "a column-zero-only pattern false-greens an
indented collision".

Fixture construction (no repo, no git; `D=/fast/scratch/hyaku/mado-r48/ExecIdGuard/guard`):

```bash
D=/fast/scratch/hyaku/mado-r48/ExecIdGuard/guard; mkdir -p "$D"
R=/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
# scratch registry = the real header (SOURCES.md lines 1-12) + TWO 2-space-indented rows
sed -n '1,12p' "$R" > "$D/SOURCES.scratch.md"
printf '  | S002 | scratch indented row - proof fixture | own-work | A | guard proof | fixture:1 @ scratch | an indented row is a census row, so a column-zero-only extractor misses it | queued | 2026-10-26 | 180d | — |\n' >> "$D/SOURCES.scratch.md"
printf '  | S203 | scratch indented row - real-staged-id fixture | own-work | A | guard proof | fixture:2 @ scratch | proves the 0-3-space extractor collides with the live staged set | queued | 2026-10-26 | 180d | — |\n' >> "$D/SOURCES.scratch.md"
# staged fixture holding S002 (the trap id the §10 sentence names):
printf '| S002 | staged row - proof fixture | own-work | A | guard proof | fixture:1 @ scratch | staged collision fixture | queued | 2026-10-26 | 180d | — |\n' > "$D/staged.scratch.md"
```

(a) The indented row is a **row**, not code — the census validator accepts the scratch registry:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$D/SOURCES.scratch.md" --today 2026-10-26
file	ok	/fast/scratch/hyaku/mado-r48/ExecIdGuard/guard/SOURCES.scratch.md
census_exit=0
```

(b) The §10 guard (0–3 leading spaces) catches the indented collision — **nonempty**:

```
reg-ids.scratch:    S002 S203
staged-ids.scratch: S002
collisions.scratch: S002
coll_count=1
```

(c) Same guard, **live staged set** (`$A/staged-ids`, the real package), indented real-staged id
S203 — nonempty against the actual package, not a fixture:

```
collisions.live: S203
coll_live=1
```

(d) The column-zero-only pattern false-greens the very same registry:

```
reg-ids.zero lines=0
collisions.zero lines=0
```

Fixture hashes (K = scratch key, deleted before yield; rebuildable byte-identically from the
commands above):

```
23b50631a8335a3e3382c145bb26b3e5a7ec93761c132460217009de6ec74285  SOURCES.scratch.md
5b0d786582a40192ce32aa64f3b5eeeaec356f29ce957332bd04f259f4684573  staged.scratch.md
e00a970ea09326e69d010c66dc00e9ec97d281e978a8bd4f49b340c1cad780fc  reg-ids.scratch   (S002 S203)
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  staged-ids.scratch (S002)
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  collisions.scratch (S002)
5619ba4d2a1b501ac337336c6e5babff9784b2a59f3923589b29332dfade575d  collisions.live    (S203)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  reg-ids.zero       (empty)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  collisions.zero    (empty)
```

Verdict: the guard prints the indented S002 (fixture staged set) and S203 (live staged set); the
column-zero-only pattern prints nothing on the same bytes. Guard proven for this lane's first
append under §10.

## 5. Quarantine slice (exactly the §10 block, lines 569–575)

```bash
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/assimilation; mkdir -p "$A"
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
  {print $4, $5}' "$R" > "$A/quarantine-slice"    # every line must carry an S-id
```

Result: **13 data rows**, every line carries an S-id (`grep -cE 'S[0-9]+'` = 13). Register hash
`5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`; slice hash
`d9ea803d2433942dac094a14e9223be086ad460502163df7faf6e2509d9bb45d`.

```
 S189   `payload-absent`
 S195   `payload-absent`
 S201   `payload-absent`
 S205   `payload-absent`
 S224   `payload-absent`
 S228   `payload-absent`
 S199`   the cited source could not be fetched, so no quote was checked
 S200`   the cited source could not be fetched, so no quote was checked
 S209`   the gate block named no locator, so no quote was checked
 S222`   the gate block named no locator, so no quote was checked
 S223`   the gate block named no locator, so no quote was checked
 S225`   the gate block named no locator, so no quote was checked
 S235`   the gate block named no locator, so no quote was checked
```

Notes that matter to the L1:

- Classes: **6 `payload-absent`** (register data rows at `:141-146`) + **7 never-checked /
  prose-class** (`:349-355`) = 13. The trailing backtick on the second class is the register's own
  cell formatting (`S199\``), present in the raw bytes; the id normalizes to S199.
- The slice is **byte-identical to round 47's re-derivation** (`diff -u` clean) — the register has
  not moved either; this is a re-derivation receipt, not a new slice.
- The register's `## By lane` summary cell reads `| \`mado\` | 6 |` (`:248`) while the data rows
  are 13 — the summary counts only the `payload-absent` class and omits the whole never-checked
  section, exactly the staleness §10 warns about ("its header AND `## By lane` summary totals are
  stale — derive your slice yourself"). The summary row is correctly excluded by the awk guard
  (`$3` holds no `roundN`, `$4` no S-id).
- Slice ids already held by the lane registry: S189, S201, S205, S209 (reg=1 each); S195, S224,
  S228, S199, S200, S222, S223, S225, S235 are not registry rows. Every row stays quarantined:
  nothing is adopted, appended or hand-checked by this seat (the wave-4 quarantine-first hand-check
  belongs to the round's own counter/lesson work, not to this guard seat).

## 6. Staged-entry topic probe (XKB family, terminal cache)

Scope asked: does any staged entry under
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/` touch XKB / keymaps / xkbcommon or the
terminal cache? **No.**

```
files=65
xkb            knowledge=0 package=0
xkeyboard      knowledge=0 package=0
keymap         knowledge=0 package=0
xkbcommon      knowledge=0 package=0
terminal cache knowledge=0 package=0
xdg-terminal   knowledge=0 package=0
```

(`package` = the whole `merge/mado/` tree including `MERGE-REPORT.md` and `amendments/`; case-
insensitive `grep -rniE`, so `XKB`/`Keymap`/`RMLVO`/`compose:caps`/`keysym` variants are covered —
the `xkb` term alone catches all of them.) The three `cache`/`terminal` hits that do exist are
unrelated: `host-producer-outputs-r29.md:12,29,32,41,53,55` (the **waybar AI-usage** cache file),
`host-bar-producers-r28.md:22` ("click opens a terminal"), and `gkeep-geometry-unobservable-r8.md:24`
/ `gkeep-rendered-geometry-chain-r9.md:91` (`Alacritty` windows in a `hyprctl clients` read). None
names `xdg-terminal-exec`, `XTE_*`, `XDG_CACHE_HOME`, or a keymap. So C2's XKB entry has **no
staged counterpart** and cannot be served from the assimilation package: it is a fresh-sourced
entry, and C1's warm-cache path likewise has no staged entry.

## 7. Bounds, tool state, cleanup

- Tools installed: none. Used coreutils `grep`/`sort`/`comm`/`awk`/`sha256sum`/`diff` and the
  repo's own `scripts/sources-census.sh validate --file` (read-only on a scratch file).
- Scratch: `/fast/scratch/hyaku/mado-r48/ExecIdGuard/` (guard fixtures ~2 KB) → removed before
  yield; free space seen: 612 G on `/fast`.
- No compositor verb, no package transaction, no background job, no subagent, no git/jj mutation,
  no write to `$S`, `/home/vgpnk/.cache`, or any PATH directory.
