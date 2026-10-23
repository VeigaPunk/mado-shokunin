# CapSourcesRegistry308 — C2 row re-run (SCORECARD.md:308, `sources registry`)

Seat: `MadoR25A3.CapSourcesRegistry308` (C2 executor, wave a3w1). Lane read-only; all runs in a detached clone.

- Base: `41cc04c8d593837a0d5078bffaacdaa163d12897` (`41cc04c8`), `SCORECARD.md` sha256 `6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08`, `corpus/SOURCES.md` sha256 `58f6e47ba6b5539291aa4fc48388ae880d4c498e67568ca5e3b908d485ab1e5f` (408 L / 147,150 B).
- Row location: `SCORECARD.md:308`, under heading `### Capabilities (round 12)` (line 304) — inside the frozen C2 population ("the 12 capability rows under `Capabilities` headings", `SCORECARD.md:1588-1589`).

## Row as written (SCORECARD.md:308)

```
| sources registry | Curate where mado learns: 39 opened, scoped-tier rows (mined/queued/rejected), study paths, search log; every contract census command runs clean and every mined row joins to an entry that cites it | `corpus/SOURCES.md`; census block in `.ufo/evidence/round-12/after.txt` | 12 |
```

- Stated capability: `sources registry`.
- Evidence pointer: `corpus/SOURCES.md`; census block in `.ufo/evidence/round-12/after.txt` (present at base; its contract block is `after.txt:47-67`).
- Demonstration command: the row names none literally. Nearest documented forms, both run:
  (a) the maintained census command frozen for this row by round 24 — `.ufo/waves/round-24/c2/manifest.json` at base (blob sha256 `e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`, 10,054 B, matching `SCORECARD.md:1569`): `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root {CENSUS_ROOT}` (cwd = base tree; `{CENSUS_ROOT}` = a scratch dir holding `shokunin.conf` plus symlink `mado-shokunin -> {TREE}`);
  (b) the round-12 verbatim "SOURCES contract census" block, re-run literally from `after.txt:47-67`.

## Sandbox and exact commands

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin \
  /fast/scratch/hyaku/mado-r25a3/c2/MadoR25A3.CapSourcesRegistry308
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C /fast/scratch/hyaku/mado-r25a3/c2/MadoR25A3.CapSourcesRegistry308 checkout -q --detach 41cc04c8
# rev-parse HEAD -> 41cc04c8d593837a0d5078bffaacdaa163d12897 ; status --short -> empty

mkdir -p /fast/scratch/hyaku/mado-r25a3/c2/census-root
printf '# scratch census root for C2 re-run 41cc04c8\n' > /fast/scratch/hyaku/mado-r25a3/c2/census-root/shokunin.conf
ln -sfn /fast/scratch/hyaku/mado-r25a3/c2/MadoR25A3.CapSourcesRegistry308 \
  /fast/scratch/hyaku/mado-r25a3/c2/census-root/mado-shokunin

cd /fast/scratch/hyaku/mado-r25a3/c2/MadoR25A3.CapSourcesRegistry308
timeout 600 prlimit --as=4000000000 \
  bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /fast/scratch/hyaku/mado-r25a3/c2/census-root        # exit 0
timeout 600 prlimit --as=4000000000 \
  bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file corpus/SOURCES.md                                    # exit 0
timeout 600 prlimit --as=4000000000 \
  bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
  --root /fast/scratch/hyaku/mado-r25a3/c2/census-root        # exit 0
# then the after.txt:47-67 block verbatim (c1-c7 below), same clone/cwd
```

Provenance check of the only non-clean line in the round-12 C3 join loop: the clone was briefly checked out at round-24 base `8e5d9369` (`git checkout -q --detach 8e5d9369`), the join loop re-run (same two lines appear), then `git checkout -q --detach 41cc04c8` before deletion.

## Ledger line

| SCORECARD.md:308 | sources registry | Scoped-tier registry rows; every contract census command runs clean; every mined row joins to an entry that cites it | works at 41cc04c8: `sources-census.sh validate` prints `mado	ok`, exit 0, zero E-codes (rows 168, mined 149 / queued 10 / rejected 9, 7 W04 duplicate-URL warnings); round-12 contract block exit 0 with NF!=13 = 0, no duplicate ids, enums clean, every mined used-by path exists, and every mined row's used-by entry cites it; the row's `39 opened` is the round-12 count (168 rows at base) | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /fast/scratch/hyaku/mado-r25a3/c2/census-root` (cwd = clone @ 41cc04c8) | SCORECARD.md:1575 (round-24 status table: sources registry works, census `mado ok`, exit 0 at `8e5d9369`) |

## Verbatim command output

### (a) frozen census command, scratch root — exit 0

```
mado	unlisted	/fast/scratch/hyaku/mado-r25a3/c2/census-root/mado-shokunin
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/fast/scratch/hyaku/mado-r25a3/c2/census-root/mado-shokunin/corpus/SOURCES.md
exit=0
```

`--file corpus/SOURCES.md` printed the same seven W04 lines plus `file	ok	.../corpus/SOURCES.md`, `exit=0`.

### (b) default census mode — exit 0

```
mado	unlisted	/fast/scratch/hyaku/mado-r25a3/c2/census-root/mado-shokunin
mado	rows	168
mado	tier.A	161
mado	tier.B	1
mado	tier.C	6
mado	status.mined	149
mado	status.queued	10
mado	status.rejected	9
FLEET	rows	168
FLEET	tier.A	161
FLEET	tier.B	1
FLEET	tier.C	6
FLEET	tier.invalid	0
FLEET	status.queued	10
FLEET	status.mined	149
FLEET	status.rejected	9
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

### (c) round-12 contract census block, verbatim, at base — exit 0

```
== c1: row count
168
exit=0
== c2: malformed rows (NF!=13)
0
exit=0
== c3: tier histogram
A=161 B=1 C=6 
== c4: status histogram
mined=149 queued=10 rejected=9 
== c5: duplicate ids
dup-check-done
== c6: enum check
enum-check-done
== c7: used-by existence
used-by-check-done
== c8: mined-row join
entry corpus/knowledge/hyprland-config-era-r12.md cites S030 without a mined row naming it
entry corpus/knowledge/terminal-trees-r23.md cites S132 without a mined row naming it
join-done
block_exit=0
```

Reading of c8: the row's claimed direction — every **mined row** joins to a used-by entry that cites it — printed nothing (clean). The two printed lines are the loop's reverse direction (an entry's `source:` cites an id whose row is not mined): `S030` is `rejected` (`corpus/SOURCES.md:42`, a rejected duplicate of the window-rules wiki page) and `S132` is `queued` (`corpus/SOURCES.md:144`; `corpus/knowledge/terminal-trees-r23.md:1` itself says "S132 stays queued and supports nothing"). Both lines are pre-existing at round-24 base `8e5d9369` and are not findings of the maintained census (`validate` emits no E-code for them; no diagnostic since, it is the C3 coverage loop, not a contract command).

## Supersession / contradiction grep over SCORECARD.md at 41cc04c8

- `grep -n "sources registry"` → `260` (round-12 claim), `308` (this row), `1575` (round-24 re-demonstration table).
- `SCORECARD.md:1566-1571`: round-24 table "supersedes the implied `works` of every earlier row"; `1575`: `| sources registry | works | census `mado ok`, exit 0 at `8e5d9369` |` — consistent with this re-run, no contradiction.
- `SCORECARD.md:1588-1596`: population scope note (12 rows under `Capabilities` headings; line 308 is in it). Names the `source-fragment collision screen` row (`SCORECARD.md:437`) as **stale** (`MISTAKE_FIX: COLLISION S120 -> S121`, `collisions=4`, exit 1). That is a different capability, outside the counted population, though it reads the same registry; it does not alter this row's census result.
- `SCORECARD.md:1608`: no-harm note "census exit 0" at `eb14fa3d`.
- No `Round 25` section exists in `SCORECARD.md` at base; nothing later in the file contradicts line 308.

## Notes, risks, blockers

- No tool installs, no package changes, no Hyprland/nested instance, no compositor verb of any kind (this item does not touch the C1 oracle). Only `sources-census.sh` (read-only: it writes only stdout) and read-only `git`/`awk`/`grep` in the clone.
- The row's "39 opened" is a dated round-12 count; the registry holds 168 rows / 149 mined at base. The capability (clean census + joins), not the number, is what round 24 froze and what this run re-demonstrated.
- S030 (rejected) and S132 (queued) are cited by two knowledge entries' `source:` lines; informational only, pre-existing, and S132 is declared non-supporting in its own entry. If a future round wants the reverse join to be zero-line output, those two citations (not the mined-row direction) are the rows to touch.
- Clone `/fast/scratch/hyaku/mado-r25a3/c2/MadoR25A3.CapSourcesRegistry308`, its `census-root`, and the two scratch TSVs were deleted after the run; `pgrep -af "sources-census|mado-r25a3/c2"` returned nothing. No blocker: all commands were runnable in the documented form and exited 0.
