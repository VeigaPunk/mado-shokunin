# MutC2Real — mutation test of PRED-C2-r35-v1 against the real repo state

Seat: `L1Mado35.MutC2Real` (mutation-tester, leaf). Round 35, wave 2.
Lane repo (read-only): `/home/vgpnk/Projects/shokunin/mado-shokunin`
Scratch: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch/MutC2Real/`
Target predicate: `PRED-C2-r35-v1` — `.ufo/waves/round-35/c2/count.py` with `.ufo/waves/round-35/c2/frozen.json`.

## 1. Isolated copy

```
git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin scratch/MutC2Real/repo
```
- clone `HEAD` = `19e4ab3171c1540c40d6b12097745af98053b07d`; `cat-file -t dff394109f3cc3d851309ad7c67dd3b35b46adf2` → `commit`.
- `git -C repo status --porcelain` → empty, exit 0, before and after the whole probe series.
- `du -sh repo` = 213M (corpus/ + full history incl. the r34 tip objects the ledger check needs).
- Every lane byte the detector reads is identical to its scratch copy (`sha256sum` of lane path vs
  `scratch/MutC2Real/repo/<path>`):
  - `c2/frozen.json` `b6a8ac0181035c1e…`
  - `c1/clauses.json` `f0f1f8a09f62b80e…`
  - `ledger/RevFrozenBlobs-r35.md` `d7ac7fa8a40cab1a…`
  - `controls/c1-entry-symlink.txt` `a9a17b787b049cad…`

Detector invocation used for every run (cwd = the scratch clone):

```
python3 -I .ufo/waves/round-35/c2/count.py \
  --repo <abs scratch clone> --frozen .ufo/waves/round-35/c2/frozen.json
```

Baseline on pristine scratch bytes: `PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1
ledger_tip_ok=1 verdict=TARGET_MET`, **exit=0**. Baseline reproduced again at the end:
same line, **exit=0**.

Method per mutant: hash pristine bytes → apply exactly one mutation → run detector →
restore the saved pristine bytes → hash again → re-run detector. Driver:
`scratch/MutC2Real/driver.py`, `scratch/MutC2Real/probe2.py`; transcripts
`driver.out.txt`, `probe2.out.txt`; mutant bytes + unified diffs under `scratch/MutC2Real/mutants/`.

## 2. Result table

| # | Mutation | File | Detector (mutant) | Exit | Verdict |
|---|---|---|---|---|---|
| M1 | delete ` verdict=TARGET_MISSED` from a control receipt | `controls/c1-entry-symlink.txt` | `uncovered=1 … verdict=TARGET_MISSED` | 1 | **killed** |
| M2 | blank the `not-load-bearing` reason | `c1/clauses.json` | `uncovered=1 … toctou_declared=0 … TARGET_MISSED` | 1 | **killed** |
| M3a | alter **one** of the six tip labels | `ledger/RevFrozenBlobs-r35.md` | `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 TARGET_MET` | 0 | **survived — dead observable** |
| M3b | alter **all** tip labels | `ledger/RevFrozenBlobs-r35.md` | `ledger_tip_ok=0 … TARGET_MISSED` | 1 | **killed** |
| M3c | stale tip everywhere except the fenced repro command | `ledger/RevFrozenBlobs-r35.md` | `ledger_tip_ok=1 … TARGET_MET` | 0 | **survived — dead observable** |
| M3d | corrupt one blob id in the ledger's own table | `ledger/RevFrozenBlobs-r35.md` | `ledger_tip_ok=1 … TARGET_MET` | 0 | **survived — dead observable** |
| M4 | add a second `not-load-bearing` clause | `c1/clauses.json` | `… toctou_declared=0 … TARGET_MISSED` | 1 | **killed** |

Three of the four assigned defects are caught. The fourth (tip label) is caught only when the
mutant removes **every** occurrence of the hash from the document; the two realistic forms of the
same defect survive. Details below.

## 3. Per-mutant evidence

### M1 — remove a control receipt's TARGET_MISSED text · KILLED

File `controls/c1-entry-symlink.txt`, mutation = delete the substring ` verdict=TARGET_MISSED`
from the verdict line.

```
before   a9a17b787b049cad56b51cb6d8556832d51c49cec4f436e114e12b8771bbaf26
mutant   9b86da586ae767b9b26ec92d999dbab83cac244a7cf529f7179befed09c17f4c  (300 bytes, -22)
pristine exit=0 PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
mutant   exit=1 PRED-C2-r35-v1 uncovered=1 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MISSED
restored a9a17b787b049cad56b51cb6d8556832d51c49cec4f436e114e12b8771bbaf26  identical=True
restored exit=0 PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
```

Mechanism: `count.py:91` `MISSED.search(receipt.read_text())` fails, so the clause
`entry-regular` is counted uncovered. Live.

### M2 — drop the not-load-bearing declaration's reason · KILLED

`clauses.json`, `o-nofollow-open["not-load-bearing"]["reason"]` set to `""` (key kept, content
removed; the counter's `nl.get("reason")` is then falsy).

```
before   f0f1f8a09f62b80efd522d79b040f7c17a3f7df4e36876d3a271d8acaa1834e4
mutant   4f632983609a4a0b96d4ca1c71d759debe793620ce458c5ee14c3d832e48c8e2  (3058 bytes)
pristine exit=0 … uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
mutant   exit=1 … uncovered=1 retired=1 toctou_declared=0 ledger_tip_ok=1 verdict=TARGET_MISSED
restored f0f1f8a09f62b80efd522d79b040f7c17a3f7df4e36876d3a271d8acaa1834e4  identical=True
restored exit=0 … uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
```

Two observables fire at once (`uncovered` via the no-control branch at `count.py:82-85`,
`toctou_declared` via `count.py:100`), so the mutation cannot be attributed to one clause; the
verdict flips either way.

### M3a — alter one tip label · SURVIVED (dead observable)

Mutation: the line `- Round-34 lane tip = \`master\` = \`dff3941…\`` (line 13) now names the stale
`fa7ba11346116672352b5d41494141c5c4d738d0`.

```
before   d7ac7fa8a40cab1aa52ee7b3bf87f7ff81de50f7fea6bb4925b960df67351fc5
mutant   70f81c2ce8398a940fd98e6958f28e0ba9fff30128d5fbd2ff8500a55554c485  (3143 bytes, ±0)
pristine exit=0 … ledger_tip_ok=1 verdict=TARGET_MET
mutant   exit=0 … ledger_tip_ok=1 verdict=TARGET_MET      <-- survived
restored d7ac7fa8a40cab1aa52ee7b3bf87f7ff81de50f7fea6bb4925b960df67351fc5  identical=True
restored exit=0 … ledger_tip_ok=1 verdict=TARGET_MET
```

Cause: `count.py:106` is `if spec["r34_tip"] in text:` — a document-wide substring test. The
document contains the hash six times (lines 5, 13, 17, 19, 35, 53), so changing any one of them
leaves the predicate satisfied. Note line 17 is labelled *"Round-34 docs commit"* and carries the
same hash; there is no positional or role check at all.

### M3b — alter all tip labels · KILLED

```
before   d7ac7fa8a40cab1aa52ee7b3bf87f7ff81de50f7fea6bb4925b960df67351fc5
mutant   2b2042c2b4f002bb445e1263fadb7bb7a7a5b93aaf5f94397859e4ec9581581d
mutant   exit=1 PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=0 verdict=TARGET_MISSED
restored d7ac7fa8a40cab1aa52ee7b3bf87f7ff81de50f7fea6bb4925b960df67351fc5  identical=True
restored exit=0 … ledger_tip_ok=1 verdict=TARGET_MET
```

So the `ledger_tip_ok` observable is live in the limit case only — when the token vanishes
entirely. That is a strictly weaker property than "the ledger names the round-34 tip".

### M3c — stale label everywhere except the fenced repro command · SURVIVED (dead observable)

The defect the ledger was re-issued to fix — a stale **label** with the conclusion left standing —
reproduced properly: every prose occurrence (intro, ref list, §1 heading, §3 verdict) names the
stale `fa7ba113…`, and the only surviving correct hash is inside the `git … rev-parse` snippet in
the fenced block (line 35).

```
mutant   5b9e65a84a257e118d4d55dcbb6cbadf7b1096028e8c61e6b25256f8b7902728
mutant   exit=0 PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   <-- survived
restored d7ac7fa8a40cab1aa52ee7b3bf87f7ff81de50f7fea6bb4925b960df67351fc5  identical=True
restored exit=0 … verdict=TARGET_MET
tip occurrences in mutant: 1   stale occurrences: 7
```

The §3 line now reads `PROVEN at the real round-34 tip \`fa7ba113…\`` and the detector still says
MET. This is the round-34 routed defect class, and C2 cannot see it.

### M3d — corrupt the ledger's own blob table · SURVIVED (dead observable)

One row of the frozen-blob table changed from `4ab3db435dd2e396402d1d83039e35082f1138fe` to
`0000000000000000000000000000000000000000`.

```
mutant   04a82c3be683189a6671f16e4cea5ffe768bfb40d7a23be71bef61ad5e93288e
mutant   exit=0 PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   <-- survived
restored d7ac7fa8a40cab1aa52ee7b3bf87f7ff81de50f7fea6bb4925b960df67351fc5  identical=True
restored exit=0 … verdict=TARGET_MET
```

Cause: `count.py:107-120` iterates `spec["frozen_blobs"]` and re-derives each id from git; the
ledger document's table is never parsed. The git re-verification is genuinely live (it is what
M3b kills), but the artifact's *claims* are decoration: a table that misstates every blob id would
still pass as long as one correct tip token remains in the text.

### M4 — add a second not-load-bearing clause · KILLED

`clauses.json`: `row-unique` (which also keeps its `control`) gains
`"not-load-bearing": {"reason": "Mutation probe: …"}`.

```
before   f0f1f8a09f62b80efd522d79b040f7c17a3f7df4e36876d3a271d8acaa1834e4
mutant   eafa90f3b233d8eb10c33440a08056da6cb963f6c4ba7e1f39546a917f1e419b  (3548 bytes, +105)
mutant   exit=1 PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=0 ledger_tip_ok=1 verdict=TARGET_MISSED
restored f0f1f8a09f62b80efd522d79b040f7c17a3f7df4e36876d3a271d8acaa1834e4  identical=True
restored exit=0 … uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
```

Mechanism: `count.py:100` `declared == [spec["toctou_clause"]]` is an exact single-element list
comparison; a second declaration breaks it. Live, and the failure is attributed to
`toctou_declared` alone while `uncovered` stays 0 — the cleanest single-axis kill of the four.

## 4. Findings

1. **Live and well-observed (3 of 4 assigned defects):** the per-clause control receipt verdict
   (M1: `uncovered`), the not-load-bearing reason presence (M2: `uncovered` + `toctou_declared`),
   the exactly-one-declaration invariant (M4: `toctou_declared`).
2. **Dead observable — `ledger_tip_ok` is a token-presence test, not a tip check (M3a, M3c):**
   six copies of the hash make any single label non-load-bearing, and a fully stale label with the
   right hash surviving only inside a repro snippet is scored MET. The r34 label defect is not
   actually gated by this clause; a stronger check would require the tip in a labelled position
   (e.g. a parsed `tip = <sha>` field) rather than anywhere in the text.
3. **Dead observable — the ledger's own blob table is unread (M3d):** `ledger_tip_ok` re-derives
   ids from `frozen.json` + git, never from the table it is named after. A ledger table can be
   arbitrarily wrong and score MET. The git re-verification itself is live only in the
   all-tokens-removed limit (M3b).
4. No mutation left the verdict MET besides the three reported above; M1/M2/M4/M3b each produced
   `verdict=TARGET_MISSED`, exit=1, as required.
5. Exit-code contract behaved as documented: 0 MET, 1 MISSED, no 2 (no predicate/target drift was
   induced; drift paths are outside this assignment).

## 5. Scope, integrity, tooling

- Writes were confined to `scratch/MutC2Real/` and this report. Nothing under `corpus/`,
  `.ufo/waves/round-35/c1|c2|controls|ledger|fetch`, `SOURCES.md`, the fleet repo, jj state or any
  sibling lane was touched. `/home/vgpnk/Projects/shokuknow` was not read or executed against.
- Restoration evidence: every mutant's `restored` sha256 equals its `before` sha256
  (`identical=True` in all seven runs), and a final pristine run printed the baseline MET line with
  exit=0. `git -C scratch/MutC2Real/repo status --porcelain` is empty after the series.
- No installs or upgrades were needed; no package manager was invoked (pacman is paused host-wide).
- Reproduction: `cd scratch/MutC2Real && python3 -I driver.py && python3 -I probe2.py`.
