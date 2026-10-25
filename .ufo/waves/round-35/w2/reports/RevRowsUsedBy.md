# RevRowsUsedBy — the eight rows' `used-by`, `status`, `opened`, `recheck` and the clauses that read them

Seat: reviewer (leaf, no dispatch). Round 35, wave 2 — falsify. Date: 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only on the lane; my writes are
under `.ufo/waves/round-35/scratch-evidence/RevRowsUsedBy/` only.

Evidence locus: the report body below is authoritative. Supporting files live at
`.ufo/waves/round-35/scratch-evidence/RevRowsUsedBy/` (the round-35 `scratch/` tree was
moved to `scratch-evidence/` at ~03:43 and the old path is not stable). That directory
holds `RELOCATION.md` (move/recovery record), `evidence.txt` (03:36 transcript, sha
`3dd4a384…`), `evidence-now.txt` (current-bytes re-run, 03:48:48), `cell-diff.txt`,
`usedby-table-now.txt`, `snapshot/` and `snapshot.sha256`.

## Observation timeline (all times -03:00, 2026-10-25)

| time | event | pin |
|---|---|---|
| 03:25:48 | rows S203–S210 written | SOURCES.md sha `848a7680…` |
| 03:30:31 | jj snapshot commit `d2b6972` | same registry sha, byte-recoverable |
| 03:34:26 | data commit `02088b4` lands the rows | `02088b4:corpus/SOURCES.md` = `848a7680…` |
| 03:35:08–43 | entries get `### Errata`; README updated | r12 `7f27ced0…`, r14 `583c708c…`, r15 `82c08a46…` |
| ~03:36 | **this seat's measurement** | `evidence.txt` sha `3dd4a384…` |
| 03:40:12 | **registry rows edited in place** | SOURCES.md sha `0bf117e2…` |
| 03:41:38 | r12 errata body refined | r12 `0bcef21f…` |
| 03:42:04 | commit `4f35c80` "wave-2 falsifications **as errata**" | `4f35c80:corpus/SOURCES.md` = `0bf117e2…` |
| 03:43 | `scratch/` moved to `scratch-evidence/` | 59 seat dirs, top-level files only |
| 03:45:09 | lesson gains wave-2 errata section | `corpus/lessons/round-35.md` |
| 03:51:25 | HEAD `7d708cf` (scorecard corrections) | registry still `0bf117e2…` |

The registry changed **after** my measurement. Everything below states which state it is
about; the live-data table is recomputed on the final observed bytes
`corpus/SOURCES.md` sha `0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51`
(pinned copy `snapshot/SOURCES.final-observed.md`).

## Axes

1. **Used-by provenance** — is each row's 11th cell *independently* equal to the set of
   admitted entries whose `source:` line names the id?
2. **Column truth** — are `status` / `opened` / `recheck` actually true of the tree?
3. **Clause fidelity** — does `PRED-C1-r35-v1` measure the value it names for each column?
4. **Repair integrity** — did the wave-2 repairs change the registry in the way the
   registry's own contract and the round's record say they did?

## 1. Independent used-by table (final observed `0bf117e2…`)

Built without the counter: parse every `corpus/knowledge/*.md` for `^source:\s*(S\d+)`,
intersect with the entries listed in `c1/frozen.json.entries` (the "admitted" set), and
compare that set with the row's 11th cell and with the frozen set. Non-admitted knowledge
entries were scanned too, for "and by nothing else".

| id | used-by cell (c11) | entries whose `source:` names it | frozen.json set | difference | status | opened | recheck | other citers |
|---|---|---|---|---|---|---|---|---|
| S203 | `corpus/knowledge/idle-lock-never-asked-r12.md` | same | same | **none** | mined | 2026-10-24 | on-change¹ | none |
| S204 | `corpus/knowledge/idle-lock-never-asked-r12.md` | same | same | **none** | mined | 2026-10-24 | on-change¹ | none |
| S205 | `corpus/knowledge/idle-lock-chain-armed-r14.md` | same | same | **none** | mined | 2026-10-24 | 90d | none |
| S206 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S207 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S208 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S209 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S210 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | 90d | none |

¹ At the 03:36 measurement S203 and S204 read `on-request`; the 03:40 edit changed both
to `on-change` (see F4). The used-by, status and opened cells are unchanged between the
two states.

8/8 rows: cell set = source-line set = frozen set; one token per cell; no id has a second
citer inside or outside the admitted set; every token resolves to an existing regular file
(census `E11` clean). **The used-by column is correct as data.**

## Findings

### F1 — HIGH: `used-by-exact` is bound to `frozen.json`, never to the entries

`c1/count.py:182-189`:

```python
if nf_ok and cs[10]:
    used_by = {t.strip() for t in cs[10].split(",") if t.strip()}
citing = {rel for rel, rel_ids in spec["entries"].items() if sid in rel_ids}
...
and used_by == citing
```

`citing` is a projection of the frozen spec. No entry's `source:` line is read anywhere in
the counter. The predicate sentence — "whose used-by token set is **exactly the admitted
entries citing it**" — is implemented as "equals the set the frozen spec says cites it".
That is row↔freeze agreement, not row↔provenance. The clause is not vacuous (a wrong token
does fail: `usedby-lesson` below), but the provenance half is unmeasured.

Falsifiers, re-run on a base built from the **current** bytes (`evidence-now.txt`,
03:48:48; the base itself scores `TARGET_MET` exit 0). Each is an independent tree; the
counter and frozen spec are untouched:

| mutant | change to entry text | verdict |
|---|---|---|
| `src-drop-S204` | delete r12's `source: S204 …` (row S204 still names r12) | `TARGET_MET` exit 0 |
| `src-retag-S204-S999` | retag that line to `source: S999 …` | `TARGET_MET` exit 0 |
| `src-drop-all-S205` | delete r14's only `source:` line (S205) | `TARGET_MET` exit 0 |
| `src-add-S204-r15` | **add** `source: S204 …` to r15, a second citer | `TARGET_MET` exit 0 |

The last one is decisive: in that tree the set of entries whose `source:` line names S204
is `{r12, r15}`, the row's cell says `{r12}`, and the frozen clause calls the cell "exactly
the admitted entries citing it". C1 prints `TARGET_MET`. An entry may silently drop or gain
a citation and both the registry's `used-by` and C1 stay green.

### F2 — HIGH: the `opened` column is never read

`grep -c opened .ufo/waves/round-35/c1/count.py` → `0` (exit 1). The predicate does not
name `opened` and the implementation never touches column 9. Mutants on the current base:

| mutant | `opened` on all 8 rows | verdict |
|---|---|---|
| `opened-1999` | `1999-01-01` | `TARGET_MET` exit 0 |
| `opened-future` | `2099-01-01` | `TARGET_MET` exit 0 |
| `opened-garbage` | `not-a-date` | `TARGET_MET` exit 0 |
| `opened-empty` | `` (empty) | `TARGET_MET` exit 0 |

`closed_rows=8` is therefore no evidence that `opened` is right. The live value is right
out-of-band: all eight receipts open with `(host re-open 2026-10-24)` (quoted in
`evidence.txt` §9), the entries carry `verified-at: 2026-10-24`, and census
`E08 --today 2026-10-25` passes. The claim should not lean on C1 for this column.

### F3 — MEDIUM: "valid cadence token" means "any word starting with a letter"

`c1/count.py:46-48,138-146`: a recheck cell passes if it is an ISO date, `^\d+d$`, or
`^[A-Za-z][A-Za-z0-9 _-]*$`. Verdicts (`evidence-now.txt`):

| cell | verdict |
|---|---|
| `banana` | `TARGET_MET` exit 0 |
| `0d` | `TARGET_MET` exit 0 |
| `on change` | `TARGET_MET` exit 0 |
| `` (empty) | `TARGET_MISSED` exit 1 |

This matches census `E09` (the lane's own rule), so it is not a counter bug — but the
ledger's phrase "a valid cadence token" reads stronger than the implementation: no
vocabulary, no ordering, no due date. The live tokens (`on-change` ×6, `90d` ×2) are
`E09`-valid; `on-change` is the same token 26 other rows use.

The two live coherence defects I measured at 03:35 (README claiming `S209: 90d` against a
row reading `on-change`; entry r12 `recheck: on-change` against rows reading
`on-request`) **were repaired at 03:40** — rows went to `on-change`, README now reads
"recheck on-change (S210: 90d)" and "recheck on-change" for r12. That repair is the
subject of F4.

### F4 — HIGH (new; measured): the wave-2 repair rewrote registry cells in place and the record says it did not

The registry's own header (`corpus/SOURCES.md:6-7`) says:

> Only `status`, `recheck` and `used-by` change in place, each logged old→new in that
> round's lesson.

The 03:45 lesson (`corpus/lessons/round-35.md:181`) and `LOG.md` both say the wave-2
findings were "applied as append-only errata blocks (criterion 44), **not as rewrites**".

Measured against the pre-repair registry (sha `848a7680…`; byte-identical at the jj
snapshot `d2b6972` and at git commit `02088b4`) and the post-repair registry (sha
`0bf117e2…`, committed in `4f35c80`), **five cells changed**, four of them outside the
allowed set (`cell-diff.txt` has the full strings):

| row | cell | allowed in place? | old → new |
|---|---|---|---|
| S203 | `teaches` | **no** | "runs **twelve first-run scripts** … none of the twelve asks" → "runs **thirteen items**, twelve of them first-run scripts … none of the thirteen executed items asks" |
| S204 | `scope` | **no** | "…and the operator never made it afterwards either" → "…the journal's zero omarchy-toggle count is a null channel, and the daemon's stop/start is consistent with a toggle-off" |
| S204 | `teaches` | **no** | "…holds zero omarchy-toggle invocations" → "…holds zero omarchy-toggle invocations, which is a null channel rather than a negative" |
| S205 | `teaches` | **no** | "the journal holds **two start lines** on 2026-10-23" → "**one start line** in the current boot (two across two boots)" |
| S203 | `recheck` | yes | `on-request` → `on-change` |
| S204 | `recheck` | yes | `on-request` → `on-change` |

Consequences:

1. **The header rule is broken.** `teaches` and `scope` are not in the allowed set, yet
   they were rewritten in the same registry that declares them immutable.
2. **The required log is missing.** The two `recheck` changes are in the allowed set but
   no `old→new` record exists: `grep -n "old→new" corpus/lessons/round-35.md` has no such
   line for these rows (the only hit is line 134, about `registration.md`), and `LOG.md`
   does not name them either.
3. **The record is false.** `round-35.md:181` and `LOG.md` say "not as rewrites" while the
   registry bytes show four out-of-set rewrites. The errata blocks themselves are
   append-only; the *registry reconciliation* was not. The commit record carries the same
   misdescription: `4f35c80` is titled "round-35: wave-2 falsifications **as errata** —
   the shape-scored counter, the falsified ledger claim, the census gaps and the misroot",
   yet `git diff --numstat 02088b4 4f35c80 -- corpus/SOURCES.md` → `3 3`: the commit
   rewrites three row lines in place. The pre-repair and post-repair registries are both
   committed (`02088b4` = `848a7680…`, `4f35c80` = `0bf117e2…`), so the rewrite is
   git-visible as a diff — no reader has to trust this seat's snapshot. Seat
   `RevEntryR15` independently reports the same in-place rewrite from the entry side
   (five cells plus S205's rewording, `TARGET_MET` throughout).
4. **The repair improved content and destroyed provenance.** The live rows now agree with
   their entries (that is why the S203/S204 recheck and S209 README defects disappeared),
   but the recorded history no longer explains how. A reader comparing the lesson to the
   registry cannot reconstruct the change.

C1 is blind to all of this: `teaches`/`scope` are never read, and a `recheck` change
between two `E09`-valid tokens cannot fail. The counter stayed `TARGET_MET` through the
rewrite (`evidence-now.txt` §live counter), which is exactly the limit M35-2 names.

### F5 — info: `status` is the one column enforced exactly, and the live value is justified

`c1/count.py:190` is a literal `cs[7] == "mined"`; `status-Mined` (capital M) and
`status-queued` both → `TARGET_MISSED` exit 1. Census `E07` agrees, and all eight rows are
legitimately `mined`: each id is cited by an admitted entry, so `W03` (mined with
`used-by —`) does not apply. No defect.

### F6 — info: `used-by` semantics have no independent guard outside C1

Census `E11` checks only that the used-by path exists on disk. A tree whose S203 cell names
the existing `corpus/lessons/round-35.md` (wrong but resolvable) produces **no `E0x`
finding for S203** (`census-mut.txt`: `grep -c S203` → 0), while C1 returns
`TARGET_MISSED open_cites=1`. So the only thing that rejects a wrong-but-existing token is
the frozen equality of F1 — and the frozen set is never checked against the entries. The
chain closes on itself.

## Non-findings (checked, clean)

- No difference of any kind between the eight `used-by` cells and the independently
  reconstructed source-line sets (§1), in either observed state.
- No id cited by a non-admitted knowledge entry; no entry cites an id absent from rows.
- No duplicate ids or rows, no extra cells for S203–S210; census `validate` on the live
  registry is `ok`, exit 0, with the seven pre-existing `W04` warnings on old ids (S030,
  S042, S045, S097, S119, S120, S121) and none on S203–S210.
- `status`, `opened` and the final `recheck` values match the lesson's admit block
  (`corpus/lessons/round-35.md:67-83`): all eight `own-work`, tier A, `mined`,
  `opened 2026-10-24`.
- `usedby-dupe` (same token twice) and a reordered cell pass — set semantics, harmless.

## Residual risk and verification gaps

- The registry was edited after my measurement and is now committed: `02088b4` (03:34:26)
  carries the pre-repair `848a7680…`, `4f35c80` (03:42:04) the post-repair `0bf117e2…`,
  and HEAD `7d708cf` (03:51:25) still equals `0bf117e2…` in both tree and worktree. The
  report pins `0bf117e2…`; later edits are outside it.
- The 03:36 entry bytes for r12 and README are not recoverable (jj `d2b6972` predates r12;
  README was rewritten at 03:40). The source lines, `recheck` line and `gate-quote` lines
  this seat cites are identical in the recovered/current copies; the errata body is not
  what I measured. See `RELOCATION.md`.
- The mutation tables are re-runs on current bytes; the original 03:36 run (sha-pinned
  `evidence.txt`) gave the same verdicts for every case it covered.
- Out of scope, not exercised: gate-quote substrings and word bounds, anchor digests
  (sibling `RevRowsDigest`), entry claim truth, C2.
- Tooling: no installs or upgrades; `python3 -I`, `sha256sum`, `stat`, `grep`, `jj file
  show`, and the fleet `scripts/sources-census.sh` (read-only stdout). No `pacman`
  transaction.

## Appendix A — exact verdicts (durable)

Live, `corpus/SOURCES.md` sha `0bf117e2…`:

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-25
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
… (six more W04 on S042, S045, S097, S119, S120, S121) …
file	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

Mutation battery on `base-now` (`evidence-now.txt`, full list):

```
base-now (unmutated)   exit=0 TARGET_MET
src-drop-S204          exit=0 TARGET_MET
src-retag-S204-S999    exit=0 TARGET_MET
src-add-S204-r15       exit=0 TARGET_MET
src-drop-all-S205      exit=0 TARGET_MET
opened-1999            exit=0 TARGET_MET
opened-future          exit=0 TARGET_MET
opened-garbage         exit=0 TARGET_MET
opened-empty           exit=0 TARGET_MET
recheck-banana         exit=0 TARGET_MET
recheck-zero-d         exit=0 TARGET_MET
recheck-space          exit=0 TARGET_MET
recheck-empty          exit=1 TARGET_MISSED
status-Mined           exit=1 TARGET_MISSED
status-queued          exit=1 TARGET_MISSED
usedby-dupe            exit=0 TARGET_MET
usedby-reorder         exit=0 TARGET_MET
usedby-lesson          exit=1 TARGET_MISSED
usedby-dotprefix       exit=1 TARGET_MISSED
usedby-absolute        exit=1 TARGET_MISSED
```

Byte-recovery of the pre-repair registry:

```
$ jj file show -r d2b6972 corpus/SOURCES.md | sha256sum
848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80  -
$ grep SOURCES snapshot.sha256
848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80  .../snapshot/SOURCES.md
```

The same old and new bytes are in git, so F4 needs no snapshot at all:

```
$ git show 02088b4:corpus/SOURCES.md | sha256sum
848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80  -
$ git show 4f35c80:corpus/SOURCES.md | sha256sum
0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51  -
$ git diff --numstat 02088b4 4f35c80 -- corpus/SOURCES.md
3	3	corpus/SOURCES.md
$ git log -1 --format=%s 4f35c80
round-35: wave-2 falsifications as errata — the shape-scored counter, the falsified ledger claim, the census gaps and the misroot
$ git log -1 --format='%H %cI' HEAD
7d708cffad386606b403393522312a4a5cc01997 2026-10-25T03:51:25-03:00
$ git show HEAD:corpus/SOURCES.md | sha256sum
0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51  -
```

Counter clauses:

```
184:            citing = {rel for rel, rel_ids in spec["entries"].items() if sid in rel_ids}
189:                and used_by == citing
190:                and cs[7] == "mined"
191:                and valid_recheck(cs[9])
$ grep -c opened .ufo/waves/round-35/c1/count.py
0
```

## Verdict

For the live data: **PASS on the four columns as data** — 8/8 `used-by` cells equal the
independently reconstructed citing-entry sets and the frozen sets; `status=mined` is
supported for all eight; `opened 2026-10-24` is corroborated by the receipt headers and
`E08`; every `recheck` is `E09`-valid.

For the frozen counter: **FAIL on clause fidelity.** `used-by-exact` measures row↔frozen
agreement, not the entries that cite the id (four mutants, `TARGET_MET` exit 0); `opened`
is never read (four mutants, `TARGET_MET`); `recheck` accepts any alphabetic word.

For repair integrity: **FAIL.** Four `teaches`/`scope` cells outside the registry's allowed
in-place set were rewritten at 03:40, the two allowed `recheck` changes carry no `old→new`
log, and the lesson and `LOG.md` both describe the repair as "append-only … not as
rewrites". The live rows are now *more* coherent than at 03:36; the record of how they got
there is not.
