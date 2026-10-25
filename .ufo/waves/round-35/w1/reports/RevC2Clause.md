# RevC2Clause — clause-ledger attack on PRED-C2-r35-v1

**Seat:** RevC2Clause (reviewer), wave w1, 2026-10-24.
**Scope:** make `c2/count.py` print `verdict=TARGET_MET` without the repair it
claims to measure, using a scratch clause ledger whose clauses all carry a
control whose receipts kill nothing. Scratch dir:
`.ufo/waves/round-35/scratch/RevC2Clause/` (builder: `build.py`, committed
surfaces untouched; `--repo .` = lane root).

## What the counter actually checks (`c2/count.py`)

Drift guard covers **only** `spec["predicate"]` and `spec["target"]`
(lines 68–71). Every other spec field — `clause_ledger`, `blob_ledger`,
`r34_tip`, `toctou_clause`, `frozen_blobs` — is read from the frozen JSON under
test and is unchecked.

- `uncovered` (lines 82–92): a clause is covered if `not-load-bearing.reason` is
  truthy (checked **first**, control never resolved), else if
  `control.receipt` is a file whose text regex-matches `verdict=TARGET_MISSED`.
  `control.tree` is never read; the control is never executed; the receipt is
  never tied to the clause or to the counter.
- `retired` (lines 94–97): count of `retired[]` ids absent from `live`; needs
  `==1`. The id is a bare string — no clause ever had to exist.
- `toctou_declared` (lines 99–100): `declared == [spec["toctou_clause"]]` —
  exactly one declared clause, id pinned by the *unchecked* spec field.
- `ledger_tip_ok` (lines 102–124): `blob_ledger` must be a file containing
  `r34_tip` as a substring, then `git rev-parse <tip>:<path>` must equal
  `blob_id` for each `frozen_blobs` entry. With `frozen_blobs: []` the git loop
  is vacuous and only the substring check remains.

## Attacks that print TARGET_MET (all observed, exact output below)

Every run printed `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1
verdict=TARGET_MET`, exit 0:

1. **Handwritten receipts** (`frozen-fake-receipts.json`): 9 clauses each name
   `control.tree: controls/nonexistent-tree` and `receipt` →
   `scratch/RevC2Clause/receipts/fake-kill.txt`, a 3-line file I wrote whose
   only content is the literal string `verdict=TARGET_MISSED`. No control tree
   exists, nothing was ever run. Coverage = writing the magic string.
2. **Borrowed committed receipt** (`frozen-borrowed-receipt.json`): every
   clause's `receipt` points at the committed
   `controls/c2-donothing.txt` — which contains `verdict=TARGET_MISSED` at
   line 6 because it is the recorded do-nothing *kill* output. The receipt
   that documents the kill-rule doubles as a cover receipt for any clause.
3. **Vacuous `ledger_tip_ok`** (`frozen-vacuous-blobs.json`):
   `frozen_blobs: []` + `r34_tip: ""` + an **empty** `blob-ledger-empty.md`.
   `"" in text` is always true and the rev-parse loop never runs →
   `ledger_tip_ok=1` with zero git work. A second variant
   (`frozen-noop-ledger.json`) keeps the real tip string with a one-line ledger
   file and still passes — the ledger document is decorative; only the
   substring matters.
4. **Renamed TOCTOU clause** (`frozen-renamed-toctou.json`): spec field
   `toctou_clause` set to `my-invented-clause`; ledger declares exactly that
   id `not-load-bearing`. The pinned clause name is not part of the drift
   guard, so the "exactly the S_ISLNK/O_NOFOLLOW pair" requirement is
   unenforced.
5. **Absolute-path receipt escape** (`frozen-abs-receipt.json`):
   `repo / control["receipt"]` — `Path(repo) / "/abs/path"` resolves to the
   absolute path, so a receipt can live anywhere on the filesystem, outside
   `--repo` entirely. `..` traversal works the same way.
6. **Invented retirement** (all of the above): `retired: [{"id":
   "invented-retired-id"}]` satisfies `retired=1`. The r34 repair being
   "measured" — retiring `r34-word-bound-1-25` — is never named by the
   counter; any absent id counts.

## Boundary results (what correctly fails)

- **Two escape-hatch clauses** (`frozen-two-dodge.json`):
  `verdict=TARGET_MISSED`, `toctou_declared=0`. `declared` must equal
  `[toctou_clause]` exactly — the hatch admits exactly one dodger.
- **Bogus tip string** (`frozen-bad-tip.json`): `r34_tip` set to a string not
  present in the ledger file → `ledger_tip_ok=0`, `TARGET_MISSED`. The tip must
  appear in the file; but nothing constrains the file beyond that.
- **Missing `blob_ledger` file**: `is_file()` false → `ledger_tip_ok=0` (by
  construction; the file must exist, content may be empty).

## The `not-load-bearing` escape hatch — answer: yes, fully

`frozen-dodge.json` (clauses-dodge ledger): `o-nofollow-open` carries **both**
`control` (receipt path `receipts/DOES-NOT-EXIST.txt`, a file that does not
exist) **and** `not-load-bearing.reason`. The counter checks the hatch at
line 83–85 and `continue`s before ever resolving the control → covered.
Observed: `uncovered=0 … verdict=TARGET_MET`. So a clause that names a control
still dodges it entirely: the control's receipt is never opened, its tree never
needed to exist. Two constraints on the dodge: (a) only one clause may use it
(`toctou_declared` list-equality), and (b) `reason` must be truthy — but
`{"reason": true}` (a non-string) also passes (`frozen-dodge-bool.json`,
observed TARGET_MET), so "with a reason" is a truthiness check, not a
content check.

## What TARGET_MET on the committed spec actually attests

Against the committed `c2/frozen.json`, the attack surface shrinks but does
not close: `frozen_blobs` are pinned to real blob ids and genuinely verify via
`git rev-parse` (confirmed — `49089c18…` at `dff3941:…`), and `toctou_clause`
is pinned to `o-nofollow-open`. But `uncovered` still measures *"receipt files
containing the string `verdict=TARGET_MISSED`"* — the counter never executes a
control, never checks `control.tree`, never binds a receipt to its clause.
`retired=1` attests that one absent id is listed, not that a dead clause was
identified and removed. `ledger_tip_ok` attests that a markdown file contains
the tip string while the pinned blob table verifies — the re-issue document's
content beyond the substring is unchecked.

Net: the only clause of this predicate that cannot be satisfied cheaply is the
git-verified `frozen_blobs` table — and only because the committed spec pins
it. Everything else is satisfiable by writing strings.

## Robustness notes

- Unguarded `clause["id"]`, `control["receipt"]`, `ledger["live"]`,
  `spec["toctou_clause"]` → malformed ledgers crash with a traceback, exit 1,
  **no verdict line** — indistinguishable from TARGET_MISSED by exit code.
- `spec["predicate"]`/`target` drift guard is the predicate's only
  integrity anchor; a scratch spec is free to weaken everything else — which is
  the intended test surface, but means the drift guard is also the whole
  defense of `toctou_clause` and `frozen_blobs`.

## Reproduction

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
S=.ufo/waves/round-35/scratch/RevC2Clause
python3 $S/build.py   # rebuilds fixtures
for f in fake-receipts borrowed-receipt dodge two-dodge vacuous-blobs \
         noop-ledger renamed-toctou abs-receipt bad-tip dodge-bool; do
  python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen $S/frozen-$f.json
done
```
