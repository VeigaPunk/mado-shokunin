# MutC1Drop — mutation test of PRED-C1-r35-v1 admission counter

Seat: mado w1, round 35. Scope: clause-drop mutation testing of
`.ufo/waves/round-35/c1/count.py` (PRED-C1-r35-v1) over the 11 frozen control
trees under `.ufo/waves/round-35/controls/` (golden + 10 c1 trees).
Committed counter untouched (sha256
`78c2589286a2d70c9b109672c85cd4e9bcb85438bc80ab888d10b73ad12abad6`, git status
clean on `c1/`); all mutants are copies under
`.ufo/waves/round-35/scratch/MutC1Drop/mutants/mNN-*.py`.

## Method

Per mutant, exactly one clause of `count.py` is removed by single-string
replacement; every other conjunct stays byte-identical. Where a drop would
crash the interpreter (`IndexError`/`TypeError`/`AttributeError`), the affected
conjunct gets a guard that preserves "clause absent" semantics
(e.g. `(quote or "").encode() in blob` after dropping `blob is not None`).
Each mutant was run with the same invocation as the receipts:

```
python3 -I <mutant>.py --root <control> --frozen .ufo/waves/round-35/c1/frozen.json
```

Kill criterion per the task: mutant changes the **verdict** on ≥1 control.
Baseline re-run reproduced all 11 committed receipts byte-for-byte
(closed_entries / closed_rows / open_cites / exit code).

## Results matrix

| mutant | dropped clause (code conjunct) | kills | result |
|---|---|---|---|
| m01 | `blob is not None` (receipt readable) | — | **DEAD** |
| m02 | `row is not None` (exactly one row → first row wins) | c1-row-duplicate MISSED→MET | killed |
| m03 | `nf_ok` (row has exactly 11 cells) | — | **DEAD** |
| m04 | `used_by == citing` | c1-usedby-extra MISSED→MET | killed |
| m05 | `cs[7] == "mined"` | c1-status-queued MISSED→MET | killed |
| m06 | `valid_recheck(cs[9])` | c1-recheck-prose MISSED→MET | killed |
| m07 | `receipt["sha256"] in cs[5]` | c1-digest MISSED→MET | killed |
| m08 | `quote is not None` (exactly one gate-quote line) | counters move, verdict same | **verdict-DEAD**, counter-live |
| m09 | `1 <= len(words) <= 25` | c1-quote-long MISSED→MET | killed |
| m10 | `quote.encode() in blob` | c1-quote-absent MISSED→MET | killed |
| m11 | `read_regular` on entry path → `Path.read_bytes()` | — | **DEAD** |
| m12 | `os.O_NOFOLLOW` in final `open()` | — | **DEAD** (declared non-load-bearing; confirmed) |
| m13 | `S_ISLNK` reject in component walk | — | **DEAD** |
| m14 | `entry_closed = entry_bytes is not None` seed | — | **DEAD** |
| m15 | `st.st_nlink != 1` | — | **DEAD** |

Golden stays TARGET_MET under every killed mutant (drops only ever fail open
inside the cite conjunction; none of them fabricates a closed cite on golden).
Every killed mutant is killed by exactly its ledger-named control, 1:1 — no
cross-kills, no control kills more than its own clause.

## Dead clauses — named

Two clauses the ledger (`c1/clauses.json`) lists as **live with a named control**
are dead under the frozen spec:

1. **`row-well-formed`** (`nf_ok`, `len(cs) == 11`). Ledger names
   `c1-row-extra-field` as its control, and the committed receipt does record
   MISSED — but under m03 the mutant *still* misses, identically
   (`closed_entries=2 closed_rows=7 open_cites=1`). The control's extra cell is
   inserted between `teaches` and `mined`, shifting `cs[7]`→"with an extra
   field" and `cs[10]`→"on-change": the cite is killed by `status-mined` and
   `used-by-exact` *before* the field count can matter. The field-count clause
   is fully redundant against this control. Fix direction: extra cell at the
   used-by position (pipe inside `cs[10]`), or a 12-cell row whose shifted
   cells still satisfy the other clauses (e.g. extra cell after `recheck`).

2. **`entry-regular`** (`read_regular` on the entry path). Ledger names
   `c1-entry-symlink`; the control's r14 entry is a leaf symlink to
   `idle-lock-never-asked-r12.md` — a file whose gate-quote lines cover S203
   and S204 only. Followed, the entry reads fine but has no `gate-quote: S205`
   line, so the S205 cite fails on the quote clauses and `entry_closed` seeds
   False regardless. m11 output on `c1-entry-symlink` is identical to baseline
   (`7/1`). The control never actually exercises "entry must be a regular
   file". Fix direction: symlink the entry to a file that would *pass* if
   followed (e.g. the golden r15 content → S205 quote absent still, so symlink
   to a crafted file carrying a valid S205 quote), or point the symlink at a
   receipt-passing entry.

Dead non-ledger conjuncts (implementation checks no frozen control exercises):

- **`blob is not None`** — no control removes or breaks a receipt path.
- **`quote is not None`** — verdict-dead but *counter-live*: on
  `c1-entry-symlink` it reports `closed_rows=8 open_cites=0` (baseline 7/1).
  The cite it lets through is still verdict-masked by the unreadable-entry
  penalty (`closed_entries` stays 2 because `entry_closed` seeds False). Only
  mutant in the battery that changes any counter without flipping a verdict;
  nearest thing to a live clause among the dead.
- **`st.st_nlink != 1`**, **`entry_closed` readability seed**, **`S_ISLNK`
  component walk** — the walk is additionally masked for leaf symlinks by
  `S_ISREG(lstat)` and `O_NOFOLLOW`; the ledger's
  `o-nofollow-open` rationale ("S_ISLNK walk already rejects") inverts: for a
  leaf symlink all three reject, so neither is individually load-bearing.
- **`os.O_NOFOLLOW`** — declared not-load-bearing; mutation test confirms
  empirically.

## Files

- Mutants: `.ufo/waves/round-35/scratch/MutC1Drop/mutants/m01..m15-*.py`
- Generator/runner: `.ufo/waves/round-35/scratch/MutC1Drop/gen_and_run.py`
- Full per-run JSON: `.ufo/waves/round-35/scratch/MutC1Drop/results.json`
