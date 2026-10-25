# MutPtrTipAncestor — mutation-tester report (round 36 wave 1)

Seat: `L1Mado36.MutPtrTipAncestor`. Role: mutation-tester.
Target: `PRED-PTR-r36-v1` = `quality/check-evidence-pointers.py`
(`c5d77733f54150a408185ecbe075c427acca10ca`-tree base, docstring `PRED-PTR-r36-v1`).

## Mutation applied (scratch copy only)

Copy: `/tmp/mutptr/gate-mutant.py` (cp of production gate; production file never
written). Two behavior-bearing changes in the `tip_axis_transcript` loop
(`quality/check-evidence-pointers.py:174-190` at base):

1. **Drop the ancestor test** — delete the `git merge-base --is-ancestor
   <candidate> <branch>` gate (lines 183-185): any `quality/receipts/axis-*.txt`
   with a 40-hex name is now a candidate.
2. **Drop the `rev=` match** — `MADO_AXIS:` `${ now only needs `mismatched=0`
   (line 188): acceptance no longer requires the receipt content to name its own
   hash.

Exact final mutant block (quoted from `/tmp/mutptr/gate-mutant.py:177-190`):

```python
    tip_axis_transcript = 0
    tip_detail = "none"
    for name in sorted(f for f in files if f.startswith("quality/receipts/axis-") and f.endswith(".txt")):
        candidate = name[len("quality/receipts/axis-"):-len(".txt")]
        if not HEX40.match(candidate):
            continue
        text = show(name)
        for line in text.splitlines():
            if line.startswith("MADO_AXIS:") and "mismatched=0" in line:
                tip_axis_transcript = 1
                tip_detail = f"{name}@{candidate}"
                break
        if tip_axis_transcript:
            break
```

## Fixture

`/tmp/mutptr/lane` = `git clone` of the lane at a pinned tree, then one fixture
commit `3177858a6a5a760e8512d58e8dac73f9d1352be5` on top:

- `quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt`
  **overwritten**: name hash `520c631d…` **is** an ancestor of the branch, content is
  `MADO_AXIS: mismatched=0 rev=a2c38305730ed86cbbe6129ec8ff023534c58edb`
  (`rev=` != name → honest must reject on the `rev=` check alone).
- `quality/receipts/axis-a2c38305730ed86cbbe6129ec8ff023534c58edb.txt`
  **added**: name hash `a2c38305…` is an **orphan commit** (`git commit-tree` on
  the empty tree), by definition not an ancestor of the branch; content carries
  `MADO_AXIS: mismatched=0 rev=a2c38305…` (honest must reject on the ancestor
  check alone).
- Stubs committed so all other observables stay green: cited receipt
  `axis-a3094c99…` (content not scanned), cited `RevSourceQuotes.md`, `.keep`
  files under both r35 scratch dirs (resolving the two `dangling_r35` =
  `dangling_r36` items), lesson disposition count updated `124` → `126` (actual
  `git ls-tree` count at the fixture tip).

Verified non-ancestor claim:
`git merge-base --is-ancestor a2c38305730ed86cbbe6129ec8ff023534c58edb master`
→ exit `1` (not an ancestor).

## Detector runs (exact quoted output)

Honest gate on the fixture (`--rev 3177858a… --branch 3177858a…`):

```
PRED-PTR-r36-v1 rev=3177858a6a5a760e8512d58e8dac73f9d1352be5 pointers_r35=8 dangling_r35=0 dangling_r35_closed=1 pointers_r36=34 dangling_r36=0 inherited_dirty=0 scratch_tracked=126 scratch_disposition_ok=1 tip_axis_transcript=0 setup=ok verdict=TARGET_MISSED
tip_axis: none
EXIT=1
```

Mutant gate on the same fixture:

```
PRED-PTR-r36-v1 rev=3177858a6a5a760e8512d58e8dac73f9d1352be5 pointers_r35=8 dangling_r35=0 dangling_r35_closed=1 pointers_r36=34 dangling_r36=0 inherited_dirty=0 scratch_tracked=126 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
tip_axis: quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt@520c631d2925807aadadb041eeda13f8b829b0c5
EXIT=0
```

Orphan-only branch `fixture-orphan-only` (receipts `axis-520c631d…` and
`axis-a3094c99…` removed; `axis-a2c38305…` remains), honest:

```
PRED-PTR-r36-v1 rev=723db7c532c6262eeb758c73416282e6510b2717 … tip_axis_transcript=0 setup=ok verdict=TARGET_MISSED
tip_axis: none
EXIT=1
```

Same orphan-only branch, mutant (tip_axis names the orphan hash — the
non-ancestor receipt is the one accepted):

```
PRED-PTR-r36-v1 rev=723db7c532c6262eeb758c73416282e6510b2717 … tip_axis_transcript=1 setup=ok verdict=TARGET_MISSED
tip_axis: quality/receipts/axis-a2c38305730ed86cbbe6129ec8ff023534c58edb.txt@a2c38305730ed86cbbe6129ec8ff023534c58edb
EXIT=1
```

Non-vacuity control (branch `fixture-no-receipts-all`: all `axis-*.txt` receipts
removed), mutant:

```
PRED-PTR-r36-v1 rev=38e13b1e25c832d49a3683671db4036f1bc05853 … tip_axis_transcript=0 setup=ok verdict=TARGET_MISSED
tip_axis: none
EXIT=1
```

## Verdicts

| Item | Verdict | Evidence |
|---|---|---|
| Mutant accepts the fabricated non-ancestor receipt | **KILLED** | orphan-only run: mutant `tip_axis_transcript=1` via `axis-a2c38305…@a2c38305…`; honest `tip_axis_transcript=0` |
| Mutant accepts without `rev=` match | **KILLED** | main fixture: mutant `TARGET_MET` on `axis-520c631d…` whose `rev=` is the orphan, `hash` own name |
| Honest gate rejects both fabrications | **PASS (control)** | honest `TARGET_MISSED`, `tip_axis_transcript=0`, exit 1, both fixtures |
| Mutant vacuity | **PASS (control)** | with zero receipts mutant reads `tip_axis_transcript=0` → `TARGET_MISSED` |
| Restoration | **PASS** | production sha256 `d1ba71e96715c3f7ce04a0b2e1758a3cc782884b6fa919db96107e01cb2d59dc` before and after; both scratch copies re-copied and `cmp`-identical to production |
| Production read-only | **PASS** | no write ever issued under `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/` or any production path; all mutations confined to `/tmp/mutptr/` |

Observation: the honest gate's `tip_axis_transcript` requires the receipt *name*
hash to be a branch ancestor **and** the content `rev=` to equal that name hash.
Because only one receipt wins (first sorted candidate that passes), a single
fabricated 40-hex receipt with a `MADO_AXIS: mismatched=0` line is sufficient for
the mutant to flip the observable, while the honest gate needs both constraints.

Tooling: no tools installed (only stock git/python3/sed/manual edit used). No
destructive commands run against any repository outside `/tmp/mutptr/`.
