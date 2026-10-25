# RevIndex — index completeness attack (round 35, wave 2)

Seat: `L1Mado35.RevIndex` (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Read-only attack; writes confined to `.ufo/waves/round-35/scratch/RevIndex/` and this file.

## Verdict

**The claim holds — at the assigned revision as well as on the working tree.**

- **At audit time** (master = `19e4ab31…`): `--rev master` reported `indexed=47/47` — a correct
  count of a 47-note universe from which the three round-35 notes were excluded (untracked
  then, their rows uncommitted). Rev mode could not test the claim on those bytes.
- **The lane has since committed them**: master is now `b632f0b98077…` (HEAD == master), and
  the three note blobs and `corpus/README.md` at master are byte-identical to the working tree.
  The same assigned command on the current master reports `indexed=50/50 missing=0 dangling=0
  duplicates=0 coverage=10.0000/10`, rc=0.
- Working tree / byte-identical scratch copy (`--root`): `indexed=50/50 … coverage=10.0000/10`,
  rc=0. Scratch snapshot committed then read with `--rev`: `50/50`, rc=0.
- Each of the three new notes has **exactly one** column-0 index row, and no row names a note
  outside the 50-note set (direct regex census, not just the gate's own verdict).
- Negative controls fire on all three failure modes for these exact entries (missing=1,
  duplicates=1, dangling=1; all rc=1). The gate is not vacuous here.

**Coverage: before (master `19e4ab31`) 47/47 = 10.0000/10; after (master `b632f0b9` and the
working tree) 50/50 = 10.0000/10.**

## 1. Assigned command — exact stdout and rc

**At audit time** (master `19e4ab31…`, the revision named in the assignment):

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
  python3 -I quality/check-index.py --repo . --rev $(git rev-parse master)
MADO_INDEX: rev=19e4ab3171c1540c40d6b12097745af98053b07d indexed=47/47 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
rc=0
```

Universe check at that rev: `git ls-tree master:corpus/knowledge` = 47 blobs;
`git show master:corpus/README.md | grep -cE '^\| `knowledge/[^`]+\.md`'` = 47;
`... | grep -c idle-lock` = 2 (only `idle-lock-plane.md`, `idle-lock-route-r17.md`).
`git ls-files` on the three round-35 notes = 0 (all `??`); `git diff --numstat -- corpus/README.md`
= 15 added lines (3 index rows + a 12-line prose section appended by a sibling late in the wave).

So on those bytes the three entries were **outside the measured universe** of `--rev master` by
construction. The assay required the working tree, so the tree was copied to scratch and
measured there. **The lane then committed** (`b632f0b`, "round-35: the last two seat reports … and
the scratch-evidence checkpoint"): master == HEAD == `b632f0b98077…`, and the three note blobs
plus `corpus/README.md` at master are byte-identical to the working tree (sha256 compare, SAME
for all four). Re-running the *same* assigned command now:

```
$ python3 -I quality/check-index.py --repo . --rev $(git rev-parse master)
MADO_INDEX: rev=b632f0b980772aad4be9ab20f8b26e9329d62239 indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
rc=0
```

Current master universe: 50 knowledge blobs (all three round-35 notes tracked, five names
containing `idle-lock`), 50 index rows in `master:corpus/README.md`. The rev-mode blindness was a
property of the pre-commit state, not of the tool, and the commit closed it.

## 2. Working tree and scratch measurements

```
$ python3 -I quality/check-index.py --root .
MADO_INDEX: root=. indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
rc=0
```

Scratch copy at audit time (rsync of `corpus/` + `quality/`, `.git`/`.jj`/`.ufo` excluded), README
sha256 `a3769bef…c5e83a` identical to the lane's. The whole `scratch/` tree was then **relocated**
(moved, not deleted) to `.ufo/waves/round-35/scratch-evidence/` at ~03:43–03:45; checkpoint commit
`4efaf63` carries only the four result files from this seat (`evidence.log`, `scratch-sha.txt`,
`run1.txt`, `run2.txt`) — the copied tree and the seven `neg-*/` trees were **not** checkpointed and
do not survive on disk. Output, quoted from the checkpointed log (restored byte-identically, see §5):

```
$ python3 -I quality/check-index.py --root .ufo/waves/round-35/scratch/RevIndex/repo
MADO_INDEX: root=.../scratch/RevIndex/repo indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
rc=0

$ python3 -I quality/check-index.py --repo .../scratch/RevIndex/repo --rev 285314d3fe9f58dfda5eb7adb4b693f82daa1e08
MADO_INDEX: rev=285314d3fe9f58dfda5eb7adb4b693f82daa1e08 indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
rc=0
```

A post-relocation **rebuild** (harness `rebuild.sh`, `evidence.rebuild.log`) reproduced a fresh copy
and commit `abad0092…` and the same `50/50` on current bytes; the rebuilt trees were swept in turn.
A rebuild is not evidence — its numbers are labelled as such, and the audited numbers above come
from the checkpointed original.

Per-note census (independent regex, lane working tree):

```
notes_total 50 row_occurrences 50 distinct_row_names 50
new_row idle-lock-never-asked-r12.md:      count=1 note_present=True
new_row idle-lock-chain-armed-r14.md:      count=1 note_present=True
new_row idle-lock-offered-in-the-bar-r15.md: count=1 note_present=True
notes_with_count_ne_1 []      rows_with_unknown_note []
```

Determinism: two consecutive `--root .` runs byte-identical, rc=0/0.
Gate self-test: `MADO_INDEX_SELFTEST: 12/12 assertions passed`, rc=0.
Supplementary fidelity gate on the lane tree: `MADO_INDEX_ROWS: root=. rows=50 errors=0 warns=0`,
rc=0 — the three new rows' cited paths (including `.ufo/waves/round-35/fetch/S203/…/S206`
receipts) resolve.

## 3. Negative controls (scratch copies of the same tree)

| variant | change to the 50/50 baseline | result | rc |
|---|---|---|---|
| `neg-missing` | delete the r12 row | 49/50 missing=1 | 1 |
| `neg-dup` | repeat the r12 row | 49/50 duplicates=1 | 1 |
| `neg-dangling` | retarget the r14 row to `…r99.md` | 49/50 missing=1 dangling=1 | 1 |
| `neg-spacerow` | two spaces after the pipe on the r15 row | 49/50 missing=1 | 1 |
| `neg-prose` | r15 only cited by a `- ` bullet (no leading pipe) | 49/50 missing=1 | 1 |
| `neg-fence` | r15 row moved inside a ``` fence | **50/50** | **0** |
| `neg-secondtable` | r15 row moved to an unrelated `## Unrelated table` | **50/50** | **0** |

Provenance: every row above was produced twice — pre-relocation (original log §10–§11) and again
by the post-relocation rebuild (`evidence.rebuild.log` §8) with identical strings and rc. The
control **trees** were never checkpointed and no longer exist, so the table is cited from the two
logs, not re-runnable from retained bytes.

## 4. Residual weakness (not a claim failure, but scope-defining)

`check-index.py` is a literal-row gate: any line at column 0 beginning ``| `knowledge/<name>.md` ``
counts regardless of table or section. Verified: a row inside a fenced code block and a row in an
unrelated table both certify `50/50 rc=0`. The docstring says so ("table context is unenforced …
an index row is a route, not a verdict"), so this is the gate behaving as documented — but a
`50/50` verdict must not be read as "the row sits in the coverage table". For the three round-35
notes the rows do sit in the coverage table (README lines 59–61, immediately before
`## Quality bar`), and `check-index-rows.py` on the real tree is clean.

Second, structural (now historical): `--rev` reads blobs at a commit only, so at audit time it
excluded the untracked notes and uncommitted rows — exactly the three entries under test, which is
why the assignment's copy-to-scratch clause was necessary. The lane has since committed them
(`b632f0b`, HEAD == master), and the same `--rev master` command now returns `50/50`. The durable
lesson: a wave judged before its commit is measured on the wrong universe; judge `--rev` on a
commit that contains the entries or use `--root`, and record which one was used.

## 5. Notes on method

- Copied-tree artifact: `check-index-rows.py --root` on the scratch copy reports 20
  `cited-path-missing` errors because the copy excluded `.ufo/` (the cited evidence lives there).
  That is my rsync's exclusion, **not** a lane defect; the lane run is `rows=50 errors=0 warns=0`.
- Concurrency: `corpus/README.md` changed under me mid-investigation (sha256 `7f348944b0e7…` →
  `a3769befe355…`, a sibling appending the prose section after the table). The scratch copy was
  refreshed and re-committed after that change; **every number above is pinned to README sha256
  `a3769befe3558c54c79c015910ba514a7009aa6a825e15f2bafdfd896fc5e83a`** (re-verified at end of
  run; the gate still reports 50/50 and 50 notes). It has since advanced twice —
  `3bb9865f…694f` (249 lines) then `de5b885a793f5a773ab1dc69016ea38e185e8f77b920d2ad7b300bc7c6310ac6`
  (254 lines) — and re-running on the latest bytes still gives `50/50` and
  `rows=50 errors=0 warns=0`, both rc=0. No lane file, counter, pairing, `SOURCES.md` row, jj
  state or git index was modified by this seat.
- Installs: none (no package manager transaction attempted; PACMAN pause irrelevant here).
- Evidence: `.ufo/waves/round-35/scratch/RevIndex/evidence.log` (commands + stdout + rc),
  `neg-*/` trees, `scratch-sha.txt`, `run1.txt`, `run2.txt`.

## Appendix — peer check requested by `L1Mado35.RevReadmeFrontier` (2026-10-25)

Peer sent four README-frontier items and addressed them to "the file you edited". **This seat did
not edit `corpus/README.md`** — it is read-only on the lane, and its only writes are the scratch
tree and this report. The README advances belong to other seats.

README at audit: `3bb9865fd12793f9adbb204175f33ca5ab69adb6103df2048bfc54300933694f`, 249 lines.
Re-run on these bytes: `check-index --root .` → `50/50`, rc=0; `check-index-rows --root .` →
`rows=50 errors=0 warns=0`, rc=0 (index side still clean after the advance).

| # | peer item | status | anchor evidence |
|---|---|---|---|
| 1 | L101–103 "No new consumer or transition measurement is claimed" is now false twice | **verified** | README:101–103 vs r14 §1 (`idle-lock-chain-armed-r14.md:15–17`: pid 1667, start lines) and README:238 ("measured ground"); split = consumer presence measured 2026-10-24, transitions unobserved (r14 §3 UNK, :36–37) |
| 2 | L241 "while leaving no state behind" overstates E2/E3/E5 | **verified** | r15:78–84 (E2 withdrawn "never taken it"; surviving claim is *no state in the toggles directory*), :87–93 (E3 withdrawn "built not to remember"; `omarchy-toggle-idle` writes no file but stops/starts the hypridle process), :100–102 (E5 scopes "leaves no trace" to on-disk). The journal scope record at 19:24:38/22:14:11 is the state E2's own inference rests on |
| 3 | L246 "hyprlock's own config" as still-open contradicts r17 | **verified** | r17:72–73 join `~/.config/hypr/hyprlock.conf` (`b8d173dc…`, 742 B/43 L) and its theme file (`3ef010e7…`) by sha256; r17:95–105 reads the keys; plane §4 is the line-anchor table. Real open item = plane `## 11. Unknowns` **item 4** (parse assurance: no read-only check; loading would mutate the session) |
| 4 | "the desktop never offers the choice" exists nowhere in `corpus/` | **falsified as stated** | `grep -rnF 'the desktop never offers the choice' corpus/` → r15:32 (*"The premise that the desktop never offers the choice was drawn from the setup path alone"*) and README:242 itself. r12 §3:36–37 carries it **line-wrapped** ("…never offers the" / "choice") — a single-line fixed-string grep misses it, which is likely why it read as absent. Attribution advice (name r12 §3:36 as the package's round-12 framing) is sound; the premise that the corpus lacks the string is not |

Net: items 1–3 are real inconsistencies in README prose (not in the index); item 4's factual
premise is wrong, though its attribution suggestion still improves the sentence. None of the four
changes the index verdict above.

Peer's amended citation `idle-lock-plane` **:335–337** for parse assurance is correct: item 4
spans lines 335–337 ("Whether `hyprlock.conf`/`hypridle.conf` parse cleanly … loading them would
mutate the session"). Index re-checked after the amendment on the then-current README
`de5b885a793f…0ac6` (254 lines): `50/50`, rc=0; `rows=50 errors=0 warns=0`, rc=0.
