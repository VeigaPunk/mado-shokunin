# ExecIdGuard — round 48 w1 · assimilation id guard + quarantine slice

Verdict: **guard proven, both §10 commands run verbatim; registry 276 ids, staged 147 ids,
84 collisions; quarantine slice 13 data rows; no staged entry touches XKB/keymaps/xkbcommon or the
terminal cache.** Nothing adopted, nothing appended, no lane or package file edited.

Source of the commands: `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-48.md` §10, id block
`:528-534`, quarantine block `:569-572`. Full evidence (commands, hashes, fixture bytes, transcripts):
`.ufo/waves/round-48/w1/ExecIdGuard/guard.md`.

## 1. Id collision check (exact §10 block)

```
reg=276 staged=147 coll=84
```

Artifacts (the four paths the §10 blocks name — the `assimilation/` dir did not exist before this
seat; the block's own `mkdir -p "$A"` created it):

| file | lines | sha256 | content |
|---|---|---|---|
| `.ufo/waves/round-48/assimilation/reg-ids` | 276 | `aa4c1956…4fa5f0` | `S001`–`S339`, no duplicates, 63 gaps |
| `.ufo/waves/round-48/assimilation/staged-ids` | 147 | `079d7538…0925d` | contiguous `S203`–`S349`, no duplicates |
| `.ufo/waves/round-48/assimilation/collisions` | 84 | `8d3561a1…d343` | S203–S221 (19), S253, S258, S277–S339 (63) |
| `.ufo/waves/round-48/assimilation/quarantine-slice` | 13 | `d9ea803d…d45d` | 6 payload-absent + 7 never-checked rows |

Registry input `corpus/SOURCES.md` sha256 `6a71f3a4…39b62`; staged input
`shokuknow/merge/mado/SOURCES.append.md` sha256 `684efe8c…7a27c0` (unchanged since round 40 — the
package has not moved). Drift against round 47: registry 262 → 276 (+14 rows), collisions 70 → 84
(+14, none removed), i.e. every row the lane opened since the round-47 base landed inside the fixed
staged range S203–S349. The staged-citation probe (`source:` lines of the 65 staged knowledge
files) yields 139 distinct ids, **76 of them inside the collision set** — any adopted entry would
need renumbering by document. No renumber map is emitted because this round adopts nothing
(`Assimilation: none` posture; wave-4 quarantine-first).

## 2. Guard proof (run once, scratch)

Fixture: real `corpus/SOURCES.md` header (lines 1–12) + one `  | S002 |` 2-space-indented row and
one `  | S203 |` indented row; staged fixture holding S002. Results:

- census validator: `file ok … census_exit=0` — the indented row is a **row**, not code.
- §10 0–3-space guard vs fixture staged set: `collisions.scratch = S002` (nonempty).
- §10 guard vs the **live** staged set: `collisions.live = S203` (nonempty against the real
  package, not a fixture).
- column-zero-only pattern on the same registry: `reg-ids.zero lines=0`, `collisions.zero lines=0`
  — the false-green §10 names.

Fixture hashes are in `guard.md` §4; the scratch tree
`/fast/scratch/hyaku/mado-r48/ExecIdGuard/` (2 KB) is deleted.

## 3. Quarantine slice (exact §10 awk)

13 rows, every line carries an S-id:

```
payload-absent (6)      S189 S195 S201 S205 S224 S228
never-checked / prose (7) S199 S200 S209 S222 S223 S225 S235
```

- Slice is **byte-identical to round 47's re-derivation** (`diff -u` clean); the register
  (`5afe1810…bad833`) has not moved.
- The register's `## By lane` cell says `| mado | 6 |` (`absent-defect-register.md:248`) while the
  register holds 13 data rows for this lane: the summary counts only `payload-absent` and omits the
  whole never-checked section — stale exactly as §10 warns. The summary row is excluded by the awk
  guard (no `roundN` in `$3`, no S-id in `$4`), as are the six absent rows at `:141-146` and the
  seven prose rows at `:349-355`.
- Lane already holds 4 of these ids as registry rows (S189, S201, S205, S209); the other 9 are not
  registry rows. All 13 stay quarantined; no hand-check verdict is claimed here.

## 4. XKB / keymap / terminal-cache probe on the staged knowledge

**No staged entry touches the XKB family or the terminal cache** (case-insensitive `grep -rniE`
over all 65 files of `merge/mado/knowledge/`, and over the whole `merge/mado/` package including
`MERGE-REPORT.md` + `amendments/`):

```
xkb=0  xkeyboard=0  keymap=0  xkbcommon=0  "terminal cache"=0  xdg-terminal=0  XTE_=0  XDG_CACHE_HOME=0
```

The only `cache`/`terminal` hits are unrelated: the waybar **AI-usage cache**
(`host-producer-outputs-r29.md:12,29,32,41,53,55`), "click opens a terminal"
(`host-bar-producers-r28.md:22`), and `Alacritty` windows in a `hyprctl clients` read
(`gkeep-geometry-unobservable-r8.md:24`, `gkeep-rendered-geometry-chain-r9.md:91`).
Consequence for the freeze: C2's `xkb-keymap-compile-r48.md` and C1's warm-cache path have **no
staged counterpart** — neither claim can be sourced from the package this round, and the
assimilation package neither helps nor collides with them.

## 5. Files changed

- `.ufo/waves/round-48/w1/ExecIdGuard.md` (this report)
- `.ufo/waves/round-48/w1/ExecIdGuard/guard.md` (full receipts)
- `.ufo/waves/round-48/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}` (named by the
  §10 command, which is why the write leaves the seat dir)
- nothing else; no tracked lane file edited; shokuknow read-only (its hash unchanged); no git/jj
  verb, no compositor verb, no package transaction, no process launched.

## 6. Risks / blockers

- **None blocking.** The guard is proven and the slice derived.
- Scope note for the L1: the `assimilation/` dir sits outside the seat dir but is the exact path the
  §10 command writes; if another seat also runs the id block, last writer wins on those four files
  (`staged-ids` is deterministic, `reg-ids` is deterministic, `collisions` is derivable from them).
- Register staleness is structural, not a one-off: any future slice from this register must
  re-derive, never cite `## By lane` (13 vs 6 this round).
