# ExecPtrFixtures — `tip_axis_transcript` negative fixtures

Seat: executor, mado round 36 wave 1. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Verdict: **PASS** — the gate's `tip_axis_transcript` conjunct discriminates all four fixture classes exactly as designed (each negative is caught, the positive passes), plus a bonus spoiler test. One finding: **F1 (minor)**, and one applicability caveat (the full TARGET_MET can not be reached at the freeze tip because the `-36 sections are not yet committed).

## 0. Honest positive transcript

The gate (PRED-PTR-r36-v1) accepts a committed `quality/receipts/axis-<40hex>.txt` iff `<40hex>` is an ancestor of the branch and some line `startswith("MADO_AXIS:")` contains `mismatched=0` and `rev=<40hex>` (`quality/check-evidence-pointers.py:174-190`; frozen wording `registration.md:106`, `c2/frozen.json`).

The assignment's prescribed producer is `quality/check-axis-scores.py --repo <lane> --rev <real commit>`. Run at the freeze tip `dbf8b579aeac0f023aaf595770f1cb0049e4baa2`:

```sh
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin \
  && python3 -I quality/check-axis-scores.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev dbf8b579aeac0f023aaf595770f1cb0049e4baa2
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=43/43 derived=43/43 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=dbf8b579aeac0f023aaf595770f1cb0049e4baa2
$ echo "EXIT=$?"   # EXIT=0
```

This is the honest receipt: `mismatched=0` at an ancestor (the freeze commit, current `master` tip). Saved verbatim as `/tmp/ExecPtrFixtures/receipt-dbf8b579-honest.txt` (4 lines).

## 1. Fixture copies

Five clones of the lane at `dbf8b579…`, each differing from the base only in committed `quality/receipts/` contents (plus, for A, one unreferenced non-ancestor commit object):

| Copy | Receipt file committed | Content |
|---|---|---|
| base | none | — |
| a-nonancestor | `axis-e8e2301db7faff215fce50189f298231c5fa52ad.txt` | honest transcript verbatim |
| b-mismatched | `axis-dbf8b579….txt` | honest transcript, `mismatched=0`→`mismatched=1` |
| c-revmismatch | `axis-dbf8b579….txt` | honest transcript, `rev=dbf8b579…`→`rev=ebf8b579…` |
| d-correct | `axis-dbf8b579….txt` | honest transcript verbatim |

For A, `e8e2301d…` was fabricated with `git commit-tree $(git rev-parse 'master^{tree}') -p master -m "fixture: never-merged tip"`; `git merge-base --is-ancestor e8e2301d… master` → exit 1 (proven non-ancestor; the hash is real, a child of the tip).

## 2. Gate runs and verdicts

Each run: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-evidence-pointers.py --repo <copy>` (gate source read from the live lane; checked repo is the copy).

Recap line (first line of output; exit status appended):

```
base  PRED-PTR-r36-v1 rev=master … tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED   BASE_EXIT=1
a     PRED-PTR-r36-v1 rev=master … tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED   A_EXIT=1
b     PRED-PTR-r36-v1 rev=master … tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED   B_EXIT=1
c     PRED-PTR-r36-v1 rev=master … tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED   C_EXIT=1
d     PRED-PTR-r36-v1 rev=master … tip_axis_transcript=1 setup=missing-r36-sections verdict=TARGET_MISSED   D_EXIT=1
```

Full D output (all other fields identical across copies except `tip_axis_transcript`/`tip_axis`):

```
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=0 tip_axis_transcript=1 setup=missing-r36-sections verdict=TARGET_MISSED
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
tip_axis: quality/receipts/axis-dbf8b579aeac0f023aaf595770f1cb0049e4baa2.txt@dbf8b579aeac0f023aaf595770f1cb0049e4baa2
```

Per-item verdicts (the conjunct under test is `tip_axis_transcript`; the exit code is `1` for every copy because of the uncommitted round-36 sections — see caveat):

- **Non-ancestor receipt (A): FAIL as intended.** `tip_axis_transcript=0`, `tip_axis: none`. The gate's `merge-base --is-ancestor` check rejects a receipt named for a non-ancestor commit even when its content is fully honest. `check-evidence-pointers.py:180-182`.
- **`mismatched=1` (B): FAIL as intended.** `tip_axis_transcript=0`. The substring `mismatched=0` is absent; `:185`.
- **`rev=` ≠ filename (C): FAIL as intended.** `tip_axis_transcript=0`. `f"rev={candidate}"` with `candidate` = filename hash does not match; `:185`.
- **Correct receipt (D): PASS as intended.** `tip_axis_transcript=1`, `tip_axis: quality/receipts/axis-dbf8b579….txt@dbf8b579…`.
- **Absence (base): FAIL as intended.** `tip_axis_transcript=0` — absence is never a pass.

## 3. Bonus: poisoning test (E)

Does a non-ancestor-named receipt beside a correct one invalidate the correct one? Copy = D + an `axis-903e4dc0143957582e8edbd025ebe218790a8f46.txt` (fabricated non-ancestor, honest content):

```
E     PRED-PTR-r36-v1 rev=master … tip_axis_transcript=1 setup=missing-r36-sections verdict=TARGET_MISSED   E_EXIT=1
tip_axis: quality/receipts/axis-dbf8b579aeac0f023aaf595770f1cb0049e4baa2.txt@dbf8b579aeac0f023aaf595770f1cb0049e4baa2
```

The non-ancestor receipt is skipped, not fatal; the correct sibling still scores. Sorting (`sorted(files)`) places `…dbf8…` before `…903e…` in this case, but either order behaves the same since the loop only breaks on a conforming candidate.

## 4. Findings

**F1 — MINOR: schema is not enforced on `MADO_AXIS:` lines.** The match is three bare substrings on any `MADO_AXIS:`-prefixed line (`:185`): `mismatched=0`, `rev=<filename-hex>`, and the prefix. A line like `MADO_AXIS: checked=3 mismatched=0 rev=dbf8b579…anything` passes; `mismatched=0x` would match the substring. The filename is strict (`HEX40`), the line is not. This is an upstream gate-design observation, not a fixture defect — each negative fixture was built to differ from the honest receipt in exactly one gate-checked dimension, and all four behave as documented.

**Applicability caveat — full TARGET_MET is unreachable at the freeze tip.** Every copy prints `setup=missing-r36-sections` and exit 1 because `LOG.md`/`SCORECARD.md` lack `## Round 36` sections and `corpus/lessons/round-36.md` is absent at `dbf8b579…` (the freeze commit predates round-36 records). The `tip_axis_transcript` conjunct is therefore measured as a component of the printed observable stream, not as a standalone exit-code flip. Once the round-36 sections land, the same D copy is the receipt class that can contribute to `TARGET_MET`.

**Noted, not mine:** `quality/receipts/` does not exist in the lane worktree; the seeded `.ufo/waves/round-36/quality-receipts/` directory is empty and is not the path the gate reads. `[INFERENCE]` on the seed's purpose — it is the production path's parent directory, not a gate input.

## 5. Tools installed

None. `python3` + `git` already present; no pacman transactions (paused host-wide per bounds). All fixture copies live under `/tmp/ExecPtrFixtures/`; the only lane write is this report.
