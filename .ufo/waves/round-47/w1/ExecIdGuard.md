# ExecIdGuard — assimilation §10: id collision guard + quarantine slice (round 47 w1)

Seat: ExecIdGuard (leaf). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Task: run the id-collision guard for the lane against the staged merge file, prove the guard on an
indented fixture, and extract the mado quarantine slice. No judgment, no supersession, no integration.

## Inputs (pinned by hash, run 2026-10-26)

| input | sha256 |
|---|---|
| corpus/SOURCES.md (registry) | `2f5dfee8c97e05347a3e5f902dfd223d9f870a35647b4e4bc5e4a1c6ca2778ea` |
| /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md (staged) | `684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0` |
| /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md | `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` |

## 1. Id-collision guard — result: 70 collisions

Exact commands run (A = `.ufo/waves/round-47/assimilation`):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md          | grep -oE 'S[0-9]+' | sort > A/reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <staged>/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > A/staged-ids
comm -12 A/reg-ids A/staged-ids > A/collisions
```

| artifact | rows | range |
|---|---|---|
| A/reg-ids | **262** | S001 … S325 (registry tops at S325, matches the round prompt) |
| A/staged-ids | **147** | S203 … S349 (contiguous; 349−203+1 = 147) |
| A/collisions | **70** | S203–S221 (19), S253, S258, S277–S325 (49) |

Guard completeness: a pipe-led S-row at *any* indentation counts 262 (registry) and 147 (staged) —
identical to the guard's totals, so `^ {0,3}` missed no row in either real input. No duplicate ids
inside either file (`sort | uniq -d` empty for both).

Delta consequence (measured, not a ruling): staged minus registry = **77 free ids**;
53 of them lie at or below S325, only **24** (S326–S349) lie above the registry top.
So 70 staged rows sit on ids the registry already uses; another 53 sit on unused but
below-top numbers; 24 sit in the append range.

Collision semantics (support, not proof of sameness): comparing the source cells of the two rows per
collision id —

- literal source string differs for **70/70** (e.g. registry S203 `host omarchy first-run installer`
  (corpus/SOURCES.md:205) vs staged S203 `Hyprland IPC page — current upstream source`
  (SOURCES.append.md:7); registry S325 `Hyprland wiki Keywords page` (:274) vs staged S325
  `Temporal UI State Inconsistency in Desktop GUI Agents` (:129)).
- source **URL** equal for **2/70** — S221 (`…/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/`)
  and S253 (`…/a1c2428f79b3…/src/ipc/s1/Unix.cpp`): same source, restaged.
- URL different or absent for **68/70**; several are same-subject with different pins, so URL
  inequality overstates semantic conflict. The guard reports id identity only.

## 2. Indented-fixture proof — guard fires on `  | S002 |`

Scratch registry (2-space indented duplicate) and staged file, receipts in
`w1/ExecIdGuard/receipts/guard-proof-*.md`:

```
registry:            staged:
| id | source |     | id | source |
|---|--------|       |---|--------|
| S001 | a |         | S002 | b |          <- 2-space indent
  | S002 | b |       | S009 | c |

reg-ids = S001 S002   staged-ids = S002 S009   comm -12 -> S002  (nonempty)
```

Controls run the same pipeline:

| control | result |
|---|---|
| clean registry/staged, no overlap | collisions = 0 lines |
| `  | S002 |` (2-space) | S002 captured |
| `   | S002 |` (3-space, regex bound) | S002 captured |
| `    | S002 |` (4-space) | **not captured** — `^ {0,3}` blind spot; no such row exists in either real input today |
| indented table header `  | id | source |` | no id captured |

## 3. Quarantine slice — 13 mado rows

Exact command (output byte-for-byte in A/quarantine-slice):

```
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Counts: **13 rows**, ids S189 S195 S199 S200 S201 S205 S209 S222 S223 S224 S225 S228 S235.

| class | rows | register lines |
|---|---|---|
| `payload-absent` | **6** (S189 S195 S201 S205 S224 S228) | 141–146 |
| "the cited source could not be fetched, so no quote was checked" | **2** (S199 S200) | 349–350 |
| "the gate block named no locator, so no quote was checked" | **5** (S209 S222 S223 S225 S235) | 351–355 |

Shape note (reproduced exactly, not edited): rows 349–355 come from the register's second table
("Rows whose quotes were NEVER CHECKED") whose columns are `| lane | round | id | prose-class | cited source |`;
in those cells `$4` carries a trailing backtick (`S199\``), so the slice's two fields keep it and `$5`
holds the prose class. `grep -oE 'S[0-9]+'` on the slice still yields exactly the 13 ids.
One further `| \`mado\` | 6 |` line (register:248) is a per-lane **count table**, not a defect row,
and is correctly excluded by the `round[0-9]+` column condition.

## Files written

- `.ufo/waves/round-47/assimilation/reg-ids` (262 lines)
- `.ufo/waves/round-47/assimilation/staged-ids` (147 lines)
- `.ufo/waves/round-47/assimilation/collisions` (70 lines)
- `.ufo/waves/round-47/assimilation/quarantine-slice` (13 lines)
- `.ufo/waves/round-47/w1/ExecIdGuard.md` (this report)
- `.ufo/waves/round-47/w1/ExecIdGuard/receipts/` — `guard-proof.txt`, `guard-proof-registry.md`,
  `guard-proof-staged.md`, `guard-proof-deep-indent.md`, `staged-new-ids.txt`, `inputs-and-counts.txt`

No tracked file edited; no git/jj mutation; nothing outside the lane. Scratch
`/fast/scratch/hyaku/mado-r47/ExecIdGuard` (56K) deleted. No tools installed.

## Risks / limits

1. The guard compares **ids only**. It cannot tell a restaged row (S221, S253) from a conflicting
   reuse (68 ids); any merge filter keyed on it must decide by source, not by id alone.
2. Indentation bound `^ {0,3}`: rows indented 4+ spaces (none today) would escape silently.
3. Seven slice rows carry a trailing backtick in the id field; downstream parsers keyed on `$4`
   must strip it (`grep -oE 'S[0-9]+'` is safe).
4. Counts are pinned to the three input hashes above; a changed merge file invalidates them.
