# MutCensusRow — does `sources-census.sh validate` actually fail on this registry?

Seat: `L1Mado35.MutCensusRow` (mutation-tester, leaf). Round 35, wave 2.
Lane repo (read-only): `/home/vgpnk/Projects/shokunin/mado-shokunin`
Scratch: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch/MutCensusRow/`
Claim under attack: the census validator is load-bearing on the lane's registry (S203–S210, three
knowledge entries, eight receipts). Target row: **S207** (`corpus/SOURCES.md:209`).

## 1. Setup

```
mkdir -p scratch/MutCensusRow/{corpus,mutants,out}
cp  mado-shokunin/corpus/SOURCES.md  scratch/MutCensusRow/corpus/SOURCES.md
cp  scratch/MutCensusRow/corpus/SOURCES.md  scratch/MutCensusRow/pristine.SOURCES.md
```

`sha256sum` of lane file, scratch copy and pristine copy — all three identical:

```
848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80
```

**E11 resolution farm.** `--file` sets the used-by base to `dirname(file)/..`
(`sources-census.sh:498-501`), so the copy's parent must resolve every used-by path in the whole
registry, not just S207's. The registry cites `corpus/knowledge` (186), `corpus/lessons` (15),
`tools/*` (8), `.ufo/waves` (2), `quality/`, `SKILL.md`, `corpus/README.md`. Each mutant root
therefore gets read-only symlinks to those lane entries:

```bash
for e in <lane>/.[!.]* <lane>/..?* <lane>/*; do ln -s "$e" mutants/<name>/$(basename "$e"); done
for e in <lane>/corpus/*; do [ "$(basename "$e")" = SOURCES.md ] || ln -s "$e" mutants/<name>/corpus/; done
```

Without this, the *baseline* emits two false `E11` findings (`.ufo/waves/round-29/registration.md`,
`…round-30…`) — a probe artifact, confirmed by the real-lane run below.

Detector invocation, identical for every run:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file <mutant>/corpus/SOURCES.md --today 2026-10-25
```

`--today 2026-10-25`; every row's `opened` is `2026-10-24`, so E08 is not in play.

### Baseline (pristine bytes, no mutation)

```
bash … validate --file mutants/M00-baseline/corpus/SOURCES.md --today 2026-10-25
```

`rc=0`; last line `file<TAB>ok<TAB>…/M00-baseline/corpus/SOURCES.md`; seven pre-existing `W04`
warnings (S030, S042, S045, S097, S119, S120, S121). Same clean result from the lane's own file
(`--file mado-shokunin/corpus/SOURCES.md` → `rc=0`, 7 × W04). Baseline is clean, so any mutant
`rc=1` is attributable to the mutation.

## 2. Result table

One mutation at a time from pristine bytes; each mutant is an independent fixture
(`mutants/<name>/corpus/SOURCES.md`, hash recorded in `out/results.json`).

| # | Mutation on S207 | Expected | Observed on S207 | rc | Verdict |
|---|---|---|---|---|---|
| M01 | status `mined` → `queued` | (legal enum) | no E, no W | **0** | **survived — silent** |
| M02 | recheck `on-change` → `after the next hypridle release` | E09 | none | **0** | **survived — GAP** |
| M03 | used-by → `stray-token` | E11 | `E11 S207 missing used-by stray-token` | 1 | killed |
| M04 | delete the anchor cell | E01 | `E01 S207 fields=10` (NF=12) | 1 | killed |
| M05 | duplicate the row after S210 | E03 | `E03 S207 duplicate id` | 1 | killed |
| M06 | recheck → `after-hypridle-release` | E09 | none | **0** | **survived — GAP** |
| M07 | recheck → `30 days` | E09 | `E09 S207 recheck=30 days` | 1 | killed (control) |
| M08 | used-by emptied, pipes kept | E11 | none | **0** | **survived — GAP** |
| M09 | status → `watch` | E07 | `E07 S207 status=watch` | 1 | killed |
| M10 | status `queued` + used-by `stray-token` | E11 | none | **0** | **survived — GAP** |
| M11 | used-by → `…r15.md,corpus/knowledge/missing-mutant.md` | E11 | `E11 S207 missing used-by corpus/knowledge/missing-mutant.md` | 1 | killed (list split works) |
| M12 | id `S207` → `S20` | E02 | `E02` | 1 | killed |
| M13 | recheck → `—` | E09 | `E09 S207 recheck=—` | 1 | killed (control) |
| M14 | recheck emptied | E09 | `E09 S207 recheck=` | 1 | killed (control) |
| M15 | status → `Queued` | E07 | `E07 S207 status=Queued` | 1 | killed (case-sensitive) |
| M16 | status → `rejected` | (legal enum) | no E, no W | **0** | **survived — silent** |
| M17 | recheck → `2026-13-45` | E09 | `E09 S207 recheck=2026-13-45` | 1 | killed (ISO-shaped control) |
| M18 | status `rejected` + used-by `stray-token` | E11 | none | **0** | **survived — GAP** |

Raw stdout for every mutant: `out/<name>.txt`; machine ledger: `out/results.json`;
driver: `mutate.py` (`cd scratch/MutCensusRow && python3 -I mutate.py`).

## 3. Findings

**G1 — alphabetic-recheck gap: CONFIRMED on a real row (M02, M06).**
`symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }` (`sources-census.sh:582`) accepts any
letter-initial token, including multi-word prose. M02 sets S207's recheck to
`after the next hypridle release`; validate prints `file<TAB>ok` and exits **0**. M06
(`after-hypridle-release`) reproduces it without spaces, so the hole is the regex's first-character
class, not word splitting. Overdue mode does not recover it either:

```
bash … overdue --file mutants/M02-recheck-prose/corpus/SOURCES.md --today 2026-10-25
→ file<TAB>cadence<TAB>S207 recheck=after the next hypridle release opened=2026-10-24   rc=0
```

The row is filed as an unjudgeable symbolic cadence and is **never** reported overdue
(`symbolic → due=INVALID_EPOCH`, line 682). Wave 1's `RevValidate` alphabetic-recheck claim is
**confirmed, not refuted**, on this real registry. Scope of the gap: the free-form text survives
every cadence in the contract's symbolic vocabulary (`on-release`, `annual`, `on-change`) because
they are indistinguishable to the regex.

**G2 — a `mined` row with an empty used-by is invisible (M08).**
`usedby_findings` skips empty cells (`[ -n "$path" ] && [ "$path" != "—" ] || continue`, line 565)
and `W03` fires only on the literal `—` (line 673). So *blank* used-by produces no E and no W:
`rc=0`, `file ok`. Contrast the three declared states: `—` → W03; a real path → checked; blank →
nothing. A miner can therefore drop the knowledge pointer entirely and lose only the W03 signal it
would have got for `—`.

**G3 — E11 is enforced only for `status=mined` (M10, M18).**
Line 559 (`[ "$status" = mined ] || continue`) gates the whole existence sweep. M10 and M18 keep a
dangling `stray-token` but set status to `queued` / `rejected`: validate exits **0** with no
finding. The contract's own wording ("E11 used-by path missing on disk") is unconditional; the
implementation is conditional. A queued row that promises a knowledge entry can cite a
non-existent file forever. (M11 shows the complementary positive: comma-separated lists *are*
split and each element checked.)

**G4 — status downgrade is silent in validate (M01).**
Flipping S207 `mined → queued` keeps a populated used-by and a mined anchor/teaches. validate:
`rc=0`, no E, no W. Only the aggregate census moves, and it is not an error:

```
census baseline:  rows 200  status.mined 181  status.queued 10  status.rejected 9
census M01:       rows 200  status.mined 180  status.queued 11  status.rejected 9   rc=0
```

So a status flip is visible only as count drift downstream (relevant to the C1 frozen counts), never
as a validate finding — and, combined with G3, it simultaneously *disables* the used-by check for
that row.

**G5 — refuted candidate holes (controls).** The recheck check is not simply "anything goes":
`30 days` (M07), `—` (M13), empty (M14) and `2026-13-45` (M17) all raise E09, and overdue mode
emits no `cadence` line for them. Likewise status is strictly enumerated — `watch` and `Queued` are
E07, `queued`/`rejected` are not. Detection positives: M03/M11 (E11), M04 (E01), M05 (E03), M12
(E02), M09/M15 (E07) all fired as designed. M05 placed the duplicate non-adjacently (after S210),
so id dedupe is section-wide, not adjacency-based.

**Note, not a gap:** on `NF!=13` the validator prints E01 then `next` (lines 635-638), so a
deleted cell masks any simultaneous E05/E07/E09 on that row. The row is already non-clean, so this
changes severity reporting only, not the verdict.

## 4. Restoration evidence

The working copy was never mutated (each mutant is a separate fixture), so restoration is a
non-event and is verified rather than asserted:

```
sha256sum scratch/MutCensusRow/corpus/SOURCES.md
  → 848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80
cmp scratch/MutCensusRow/pristine.SOURCES.md scratch/MutCensusRow/corpus/SOURCES.md  → identical
sha256sum mado-shokunin/corpus/SOURCES.md
  → 848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80   (lane unchanged)
bash … validate --file scratch/MutCensusRow/corpus/SOURCES.md --today 2026-10-25
  → file<TAB>ok  rc=0
```

No writes outside `scratch/MutCensusRow/` and this report. No edits to lane corpus, counters,
controls, SOURCES.md, the fleet repo, `.jj`, or the Git index; no git/jj commands were run. No
package installs (pacman is paused host-wide; nothing was needed).

## 5. Unverified / out of scope

- Only this lane's registry was mutated; whether the same gaps fire on other lanes' registries is
  not tested here.
- I did not test a duplicate row placed *outside* `## Registry` (that path is E12, not E03), nor
  the interaction of E11 with symlinked/broken-directory used-by targets.
- G1–G4 are coverage findings against the documented checks; they do not by themselves falsify the
  frozen C1/C2 counters, which read different artifacts.
