# ExecHarmBase — harm watch baseline (mado r46 w1)

**Status: complete.** Every gate named in the seat spec was run at the base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`
and at the freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, in throwaway clones, read-only on the lane.

- Deliverable the L1 compares against: `.ufo/waves/round-46/w1/ExecHarmBase/baseline.md`
- Verbatim run outputs: `.ufo/waves/round-46/w1/ExecHarmBase/receipts/` (49 files, 464 KB)
- Lane files created/edited: only these two paths plus my seat directory. No tracked lane file touched
  (`git status --porcelain | grep -v '^??'` empty at the end; the untracked entries are other seats').

## Headline: delta zero between base and freeze

No gate moved. Ten gate/tool blobs are byte-identical at base, freeze and lane HEAD `e0be61e4` (§0 of the baseline); the
only tracked change between base and freeze is the three added round-46 counter files, and `git diff --stat 8c5434c e0be61e4
-- quality tools corpus` is empty. So every base-vs-freeze comparison below is a data comparison, not a gate comparison.

| gate | base | freeze |
|---|---|---|
| `quality/check-axis-scores.py --rev/--repo` | `checked=3 mismatched=0`, exit 0 | same, exit 0 |
| `quality/check-index.py --rev/--repo` | `indexed=62/62 missing=0 dangling=0 duplicates=0`, exit 0 | same, exit 0 |
| `quality/counters/c1-r45-monitors-v2.py` | `fixtures=81/81 generated=150/150 … TARGET_MET`, exit 0 | same, exit 0 |
| `quality/counters/c2-r45-monitor-entry-v2.py` | `admitted=1/1 TARGET_MET`, exit 0 | same, exit 0 |
| `tools/mado-monitors.py --selftest` | `48/48`, exit 0 | same |
| `tools/mado-geometry.py --selftest` | `94/94`, exit 0 | same |
| `bash tools/mado-verify.sh --selftest` | `460/460`, exit 0 | same |
| `sources-census.sh validate … mado` | `ok`, 10 warnings (9 W04 + 1 W01), 0 E, exit 0 | same |
| `check-index-rows` / `check-evidence-pointers` / `check-session-material` | `errors=0 warns=3` / `TARGET_MET` / `findings=97`, exit 1 | identical (session-material adds 24 files, 0 findings) |
| `quality/*.py --selftest` (5 gates), all `tools/*.py --selftest`, `action-plan --frozen`, `assessment --selftest`, `r33 c2/count.py` | green (see baseline §2) | identical |
| `mado-verify.sh --no-live` | rev-invariant: `MADO_VERIFY: CLEAN (29 pass, 4 notes)`, exit 0 | — |
| round-46 claim counters (not gates) | `PRED-C1-r46 TARGET_MISSED`, `PRED-C2-r46 TARGET_MISSED`, exit 1 | same |

Four invocations are **red at both revisions**, each inherited and each attributed in the baseline:

1. **`mado-r27-population-suite` (SKILL.md:725)** — `SUITE verdict=FAIL fixtures=46 failed=9` with the lane's current
   `quality/check-population.py` (blob `c8b47f76`, sha256 `17e99993…`, last touched by `317ff19c` round-28), but
   `PASS fixtures=46 failed=0` with the round-26 checker the round-27 evidence names as subject
   (`.ufo/waves/round-27/evidence/c2-after-0b53bd86.txt:4`, sha256 `803e0096…`). Subject swap, not round-46 harm; the
   published row's plain invocation is red.
2. **`mado-r27-counter-selftest` (SKILL.md:724)** — with the round-26 counters: `SELFTEST pass=57 total=59`,
   `FAILED c1-version-guard,c1-version-missing-commit`, exit 1, on counter bytes identical to the round-26 green receipt's
   pins; the gate file itself drifted (`d72b7f1a…` vs the receipt's `0754f501…`). With the round-27 counters it aborts:
   `AttributeError: module 'mado_r27_q_c2' has no attribute 'O'` (`quality/counter-selftest.py:458`). Consequence: no
   registered selftest gate can score the round-45 or round-46 counters; only their clause `s` does.
3. **`mado-evidence-audit` (SKILL.md:2082)** — its selftest exits 2 `FileNotFoundError` in any clean checkout, because two
   fixture directories are empty and therefore untracked (`round-22/audit/fixtures/cases/AuditRawPathDotDotInternal/root/sub`,
   `…/AuditRawPathEscape/root`; clone tree 267 paths vs lane 269). Creating them makes the same command pass `cases=46
   failed=[]` at both revs. A verifier reading committed bytes always sees red; needs a tracked placeholder that does not
   change the two raw-path cases (L1-owned).
4. **`check-session-material`** — exit 1 with `findings=97` at both revs (rules `R1=23 R2=26 R3=46 R4=2`), matching the
   round-45 data receipt (`.ufo/waves/round-45/receipts/session-material-data.txt:100`) and the closure's split of 48
   pre-existing + 49 synthetic (`corpus/lessons/round-45-verifier-spotcheck.md:54`, `:112`). Round 46 inherits D3 exactly.

## Round-45 closure D1 (counter half)

The never-run w2 falsification now runs: both round-45 v2 counters are `TARGET_MET` at the base *and* at the freeze, c1
with `81/81` fixtures and `150/150` nonce-generated cases under two different nonces (`1522954641`, `311901436`), c2 with
`clauses=a:1 … j:1`. This supports D1's counter half only; the semantic attack on round-45's tool and entry is not my seat.

## What the data tip must not move

1. Rows 1–8 of baseline §1 stay green with identical metric shapes; `derived=`/`indexed=` may only grow.
2. `check-index-rows errors=0` — a broken S316-S325 or README row moves this line.
3. `check-session-material findings` must not exceed 97 and must not gain R3/R4; a drop is D3 landing.
4. Census stays `ok` with exactly the 10 inherited W-lines; any `E0x` (duplicate id S316-S325, shared URL+scope, missing
   used-by) is the new rows' failure mode.

## Not run, with reason (also baseline §6)

`mado-verify --live` (host guard allows only version/devices/monitors/getoption; this gate also reads instances,
configerrors, binds, layers); `--regression`/`--frozen-regression`/`--source-merge` (need the sibling tameshi harness or
per-round frozen dirs); `--snapshot`/`--snapshot-diff` (needs caller receipts); `r26-population` and
`r26/r27-control-receipts` (need a registration with registered targets and a data registry with `createdAt`;
`check-population --registration round-45/registration-v2.md` answers `UNREADABLE … no **PRED-...** sentence`, exit 2).

## Tooling / safety

No tool installed (nothing needed). No compositor call, no pacman, no host write, no input injection. Scratch
`/fast/scratch/hyaku/mado-r46/ExecHarmBase` (547 MB, two `--shared` clones whose `rev-parse --show-toplevel` was asserted
equal to each clone before use) was deleted after the receipts were copied; no scratch path is used as evidence.

## Blockers

None.
