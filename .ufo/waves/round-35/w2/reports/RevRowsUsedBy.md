# RevRowsUsedBy — the eight rows' `used-by`, `status`, `opened`, `recheck` and the clauses that read them

Seat: reviewer (leaf, no dispatch). Round 35, wave 2 — falsify. Date: 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only on the lane; every write is
under `.ufo/waves/round-35/scratch/RevRowsUsedBy/`. Repro driver:
`scratch/RevRowsUsedBy/run.sh`; full transcript: `scratch/RevRowsUsedBy/evidence.txt`;
snapshot of the observed bytes: `scratch/RevRowsUsedBy/snapshot/` + `snapshot.sha256`.

## Axes

1. **Used-by provenance** — is each row's 11th cell *independently* equal to the set of
   admitted entries whose `source:` line names the id?
2. **Column truth** — are the `status` / `opened` / `recheck` values on rows S203–S210
   actually true of the tree and the receipts?
3. **Clause fidelity** — does `PRED-C1-r35-v1` measure the value it names for each column?

## Observation window (important)

The corpus moved while this seat ran. At 03:35 local a sibling edited all three entries
(adding `### Errata (round 35, wave 2)`) and `corpus/README.md`. The SOURCES.md rows were
not touched (mtime 03:25:48). My snapshot is the post-repair state; the counter was re-run
after the edits and still prints `TARGET_MET` exit 0. Findings below are stated against the
snapshot hashes in `evidence.txt` §0.

## 1. Independent used-by table

Built without the counter: parse every `corpus/knowledge/*.md` for `^source:\s*(S\d+)`,
keep the entries listed in `c1/frozen.json.entries` ("admitted"), and compare that set with
the row's 11th cell and with the frozen set. Non-admitted knowledge entries were scanned
too, for "and by nothing else".

| id | used-by cell (cell 11) | entries whose `source:` names it | frozen.json set | difference | status | opened | recheck | other citers |
|---|---|---|---|---|---|---|---|---|
| S203 | `corpus/knowledge/idle-lock-never-asked-r12.md` | same | same | **none** | mined | 2026-10-24 | on-request | none |
| S204 | `corpus/knowledge/idle-lock-never-asked-r12.md` | same | same | **none** | mined | 2026-10-24 | on-request | none |
| S205 | `corpus/knowledge/idle-lock-chain-armed-r14.md` | same | same | **none** | mined | 2026-10-24 | 90d | none |
| S206 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S207 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S208 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S209 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | on-change | none |
| S210 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | same | same | **none** | mined | 2026-10-24 | 90d | none |

8/8 rows: cell set = source-line set = frozen set; one token per cell; no id has a second
citer inside or outside the admitted set; every token resolves to an existing regular file
(census `E11` clean). The live column is **correct as data**.

## Findings

### F1 — HIGH (core of the assignment): `used-by-exact` is bound to `frozen.json`, never to the entries

`c1/count.py:182-189`:

```python
if nf_ok and cs[10]:
    used_by = {t.strip() for t in cs[10].split(",") if t.strip()}
citing = {rel for rel, rel_ids in spec["entries"].items() if sid in rel_ids}
...
and used_by == citing
```

`citing` is a projection of the frozen spec. No `source:` line of any entry is read anywhere
in the counter. So the predicate sentence — "whose used-by token set is **exactly the
admitted entries citing it**" — is implemented as "equals the set the frozen spec says
cites it". That is row↔freeze agreement, not row↔entry provenance. The clause is not
vacuous (a wrong token does fail: below), but the provenance half is unmeasured.

Falsifiers on the post-repair snapshot (`base2` — the snapshot itself scores
`TARGET_MET`, exit 0), each an independent tree, counter unchanged:

| mutant | change to the entry text | counter |
|---|---|---|
| `src-drop-S204` | delete `source: S204 …` from r12 (S204 still cited by the row) | `closed_rows=8 … TARGET_MET` exit 0 |
| `src-retag-S204-S999` | retag that line to `source: S999 …` | `TARGET_MET` exit 0 |
| `src-drop-all-S205` | delete r14's only `source:` line (S205) | `TARGET_MET` exit 0 |
| `src-add-S204-r15` | **add** `source: S204 …` to r15, making it a second citer | `TARGET_MET` exit 0 |

The last one is the crisp one: in that tree the set of entries whose `source:` line names
S204 is `{r12, r15}`, the row's cell says `{r12}`, and the frozen clause says the cell is
"exactly the admitted entries citing it". C1 prints `TARGET_MET`.

Practical consequence: an entry may silently drop or gain a citation and the registry's
`used-by` plus C1 stay green. The lane's census does not close this either — `E11` only
checks that the named path exists (F6). Nothing in the toolchain compares a row's `used-by`
with the entry's `source:` block.

### F2 — HIGH: the `opened` column is never read

`grep -c opened .ufo/waves/round-35/c1/count.py` → `0` (exit 1). The predicate does not name
`opened`, and the implementation has no access to column 9. Mutants on `base2`:

| mutant | opened cell (all 8 rows) | counter |
|---|---|---|
| `opened-garbage` | `not-a-date` | `TARGET_MET` exit 0 |
| `opened-future` | `2099-01-01` | `TARGET_MET` exit 0 |

(The earlier battery also passed `1999-01-01` and an empty cell.) So `closed_rows=8` is no
evidence that `opened` is right. The live value is right, out-of-band: all eight receipts
open with `(host re-open 2026-10-24)` (`evidence.txt` §9), the entries carry
`verified-at: 2026-10-24`, and census `E08 --today 2026-10-25` passes. The claim should
not lean on C1 for this column.

### F3 — MEDIUM: "valid cadence token" means "any word starting with a letter"

`c1/count.py:46-48,138-146`: a recheck cell passes if it is an ISO date, `^\d+d$`, or
`^[A-Za-z][A-Za-z0-9 _-]*$`. `recheck-banana` (S205 → `banana`) → `TARGET_MET` exit 0.
By the same regex `on change` and `0d` pass; only an empty cell fails. This matches census
`E09`, so it is the lane's own rule, but the ledger's phrase "a valid cadence token" is
weaker than it reads: no vocabulary, no ordering, no due date.

Live coherence defects in the same column (both survive C1, both are `E09`-valid):

- **S209.** Row `recheck=on-change`; `corpus/README.md:61` states "recheck on-change
  (**S209, S210: 90d**)". S210 is `90d`; S209 is not. One of the two is wrong.
- **S203/S204 vs r12.** Rows are `on-request`; the citing entry's own header says
  `recheck: on-change` (`corpus/knowledge/idle-lock-never-asked-r12.md:10`), and
  `README.md:59` says "recheck on-request". `on-request` occurs on exactly these two rows
  in the whole registry (2/200) and is not among the symbolic examples the lane has
  enumerated (`on-release/on-change/on-session-change/on-gate-change/on-capture-change/
  on-compositor-release`, `.ufo/waves/round-18/w1/reports/SourcesRowShape.md:71`). The
  entry is the outlier and was not updated with its row.
- Freeze transfer: the pre-data golden row had `S203 recheck=on-change`; live is
  `on-request` (`evidence.txt` §6). The recheck cell changed after the control receipts
  were committed. New-row edits are legal, but the committed control did not exercise the
  live value.

### F4 — MEDIUM (live data, adjacent to `status`; route to the row owners)

The wave-2 errata rewritten into the entries at 03:35 now contradict **immutable** row
cells, and `status=mined` on those rows still counts:

| row cell (unchanged, 03:25) | entry erratum / README (03:35) |
|---|---|
| S203 `teaches`: "runs twelve first-run scripts … none of the twelve asks" | r12 E2: "thirteen items: 12 `bash …/*.sh` plus `omarchy-hook-install`" |
| S204 `scope`: "the idle lock was never asked about **and never toggled**" | r12 E1: the "never toggled" inference is **withdrawn** (null-channel reading) |
| S205 `teaches`: "the journal holds **two start lines**" | README:60: "**one** start line in the current boot's journal" |

SOURCES.md's own header says only `status`, `recheck`, `used-by` change in place, so these
cells cannot be repaired without a new row or an appended errata. C1 does not read them, so
`closed_rows=8` is unaffected — which is exactly why the mismatch is worth recording: the
8/8 covers four columns, not the row's truth. The entry-side repairs belong to the seats
that wrote them; this seat only records that the registry no longer matches its entries.

### F5 — info: `status` is the one column enforced exactly, and the live value is justified

`c1/count.py:190` is a literal `cs[7] == "mined"`; `status-Mined` (capital M) →
`TARGET_MISSED` exit 1. Census `E07` agrees, and all eight rows are legitimately `mined`:
each id is cited by an admitted entry, so `W03` (mined with `used-by —`) does not apply.
No defect.

### F6 — info: division of labour leaves `used-by` semantics with no independent guard

Census `E11` checks only that the used-by path exists. A tree whose S203 cell names the
existing `corpus/lessons/round-35.md` (i.e. a wrong but resolvable user) produces **no
`E11`/`E0x` line for S203**, while C1 correctly returns `TARGET_MISSED open_cites=1`
(`scratch/RevRowsUsedBy/m-usedby-lesson2`, `census-mut.txt`). So the only thing that can
reject a wrong-but-existing token is the frozen equality of F1 — whose reference set is
never checked against the entries. The chain is closed on itself.

## Non-findings (checked, clean)

- No difference of any kind between the eight cells and the independently reconstructed
  source-line sets (§1).
- No id cited by a non-admitted knowledge entry; no entry cites an id absent from rows.
- No duplicate ids, no duplicate rows, no extra cells for S203–S210; census `validate`
  on the live registry is `ok`, exit 0, with the seven pre-existing `W04` warnings on
  old ids (S030, S042, S045, S097, S119, S120, S121) and none on S203–S210.
- `status`/`opened`/`recheck` match the round-35 lesson's admit block
  (`corpus/lessons/round-35.md:67-83`, entries at `:84`): all eight `own-work`, tier A,
  `mined`, `opened 2026-10-24`.
- `usedby-dupe` and a reordered cell pass (set semantics) — harmless, not a defect.

## Residual risk and verification gaps

- Line/cell checks are textual: my independent scan matches `^source:\s*(S\d+)` at column 0;
  the three entries have no indented or comma-joined `source:` lines (`grep -nE
  "^[[:space:]]+source:"` empty), so the reconstruction is complete for this data.
- The entries and README were being edited concurrently (03:35, sibling seats). My snapshot
  hashes pin what I judged; a later edit that removes a `source:` line would invalidate
  §1's "as observed" statement without invalidating F1 (which predicts C1 stays green).
- F1's mutants change only entry/row text; `gate-quote` lines were left intact so the
  failure cannot be confused with the quote clauses.
- Out of scope, not exercised: gate-quote contents and word bounds, anchor digests
  (sibling `RevRowsDigest`), C2, the three entries' claim truth.
- Tooling: no installs or upgrades; only `python3 -I`, `sha256sum`, `stat`, `grep`, `git`,
  and the fleet `scripts/sources-census.sh` (read-only, stdout). No `pacman` transaction.

## Verdict

For the live data: **PASS** — 8/8 `used-by` cells equal the independently reconstructed
citing-entry sets and the frozen sets; every `status=mined` is supported by an admitted
entry; `opened 2026-10-24` is corroborated by the receipt headers and `E08`; every
`recheck` is accepted by `E09`, with two coherence defects to route (S209 vs README,
r12 entry vs its rows).

For the frozen counter: **FAIL on clause fidelity for this scope.** `used-by-exact`
measures row↔frozen agreement, not the entries that cite the id (four mutants, all
`TARGET_MET` exit 0); `opened` is never read (two mutants, both `TARGET_MET`); `recheck`
accepts any alphabetic word. The claim's live numbers are correct today, but the predicate
cannot prove two of the four columns it is credited with, and cannot notice a stale
`used-by` after an entry edit.
