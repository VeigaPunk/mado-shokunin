# SentProvenance — round-35 registration provenance check

Seat: SentProvenance (sentinel lane, leaf). Date: 2026-10-24.
Scope: every evidence pointer `.ufo/waves/round-35/registration.md` cites — frozen specs,
counters, clause ledger, control receipts, the eight fetch receipts, the re-issued blob
ledger, and the r34 tip. For each: does the path resolve, and does the recorded hash match
the bytes on disk / at the named revision?

Method: `git rev-parse <rev>:<path>` for blob ids, `git hash-object` for disk-vs-committed,
`sha256` over receipt bytes vs `c1/frozen.json`, `git merge-base --is-ancestor` for
ancestry, `git log --format=%H master -- <path>` for write-once history, and a live re-run
of all twelve control commands compared line-for-line against the committed receipts.

**Verdict: PASS on every pointer.** No missing path, no hash mismatch, no stale receipt.

## 1. Frozen specs and counters

| pointer | path resolves | recorded hash | check |
|---|---|---|---|
| `c1/frozen.json` (PRED-C1-r35-v1) | yes | none self-recorded | committed at `19e4ab3`; disk blob `273a16e03b45` == `HEAD:c1/frozen.json` |
| `c1/count.py` (C1 counter) | yes | none self-recorded | committed; disk blob `56ce2b5770c2` == HEAD; counter exits 2 on predicate drift, so an unpinned spec would die |
| `c2/frozen.json` (PRED-C2-r35-v1) | yes | none self-recorded | committed; disk blob `b67bdd92b310` == HEAD |
| `c2/count.py` (C2 counter) | yes | none self-recorded | committed; disk blob `15b398010ffd` == HEAD |
| `c1/clauses.json` (clause ledger, cited by c2 spec `clause_ledger`) | yes | none self-recorded | committed; disk blob `8c7b3b3de6e9` == HEAD |

The specs and counters carry no self-recorded digest; the meaningful pin is the commit —
all five are tracked at HEAD `19e4ab3171c1540c40d6b12097745af98053b07d` (the r35 freeze)
and the working-tree bytes are identical to the committed blobs.

## 2. Control receipts (12)

Each `controls/<name>.txt` records its command, its counter line and its exit code.
All twelve are committed (disk blob == HEAD blob). Recorded verdicts match the kill rule —
eleven `TARGET_MISSED` exit 1, `golden` `TARGET_MET` exit 0 — and the recorded
`PRED-* ... verdict=...` line is **identical** to a live re-run under
`PYTHONDONTWRITEBYTECODE=1` today:

| receipt | recorded | re-run | status |
|---|---|---|---|
| `controls/c1-donothing.txt` | MISSED exit 1 | MISSED exit 1 (`closed_entries=0 closed_rows=0 open_cites=8`) | OK |
| `controls/c1-entry-symlink.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-row-duplicate.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-row-extra-field.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-usedby-extra.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-status-queued.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-recheck-prose.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-digest.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-quote-absent.txt` | MISSED exit 1 | identical | OK |
| `controls/c1-quote-long.txt` | MISSED exit 1 | identical | OK |
| `controls/golden.txt` | MET exit 0 (`3/8/0`) | identical | OK |
| `controls/c2-donothing.txt` | MISSED exit 1 (`uncovered=1`) | identical, via `/fast/scratch/mado-r35/c2-donothing/frozen.json` (fixture present, 2026-10-24) | OK |

Control trees under `controls/<name>/` are committed too (156 tracked paths under
round-35). `c1-entry-symlink`'s injected defect (a symlinked entry path) is inside its own
tree — noted, not re-walked here.

## 3. Fetch receipts (8) — recorded sha256 vs disk

`c1/frozen.json` `receipts{}` records path + sha256 for each cite. Re-hashed bytes on disk:

| id | path | sha256 recorded | sha256 disk | status |
|---|---|---|---|---|
| S203 | `.ufo/waves/round-35/fetch/S203.receipt.txt` | `1b7fa87f…dd1646` | same | OK |
| S204 | `…/S204.receipt.txt` | `4cd5ba65…1c54ad` | same | OK |
| S205 | `…/S205.receipt.txt` | `f3387bfc…08ae1a` | same | OK |
| S206 | `…/S206.receipt.txt` | `1d30e4a9…0a938d5` | same | OK |
| S207 | `…/S207.receipt.txt` | `81c33e79…0adec59` | same | OK |
| S208 | `…/S208.receipt.txt` | `6e72f0db…d6ce4654` | same | OK |
| S209 | `…/S209.receipt.txt` | `a170c7a5…3bdd27c` | same | OK |
| S210 | `…/S210.receipt.txt` | `ef282e38…790b8726` | same | OK |

All eight also disk==committed at HEAD. (Full 64-hex digests in `c1/frozen.json` lines
26–57; prefix-truncated here.)

## 4. Blob ledger — `.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md`

Resolves; committed; disk blob `712d6bae2251` == HEAD. It names the r34 tip
`dff394109f3cc3d851309ad7c67dd3b35b46adf2` and lists seven blob ids. Re-derived with
`git rev-parse dff3941…:<path>` — all seven match both the ledger table and
`c2/frozen.json` `frozen_blobs[]`:

| path | recorded blob | at `dff3941` | status |
|---|---|---|---|
| `.ufo/waves/round-33/c1/count.py` | `4ab3db43…` | same | OK |
| `.ufo/waves/round-33/c1/frozen.json` | `60d1094b…` | same | OK |
| `.ufo/waves/round-33/c2/count.py` | `df563528…` | same | OK |
| `.ufo/waves/round-34/c1/count.py` | `49089c18…` | same | OK |
| `.ufo/waves/round-34/c1/frozen.json` | `0bfe0d86…` | same | OK |
| `.ufo/waves/round-34/c2/count.py` | `3a499a7e…` | same | OK |
| `.ufo/waves/round-34/c2/frozen.json` | `ef3392b4…` | same | OK |

Ledger §2 write-once claim re-verified: `git log --format=%H master -- <path>` returns
exactly one commit per path — `9a46ccf3282117f960b8d53cd71599a91f388ee3` for the three r33
paths, `3420e827bd7b21b1374b23245526554ffd20d096` for the four r34 paths. All four named
refs (`3420e827`, `fa7ba113`, `57622b84`, `dff3941`) resolve as commits.

The ledger's stale-label claim also re-verified: the r34 artifact it corrects,
`.ufo/waves/round-34/w1/reports/RevFrozenBlobs.md` (present, 5384 B), does label
`fa7ba11346116672352b5d41494141c5c4d738d0` as "Lane tip = master = HEAD" (line 8).

Caveat on wording: the ledger says "Round-34 lane tip = `master`". At check time `master`
has advanced to the r35 freeze `19e4ab3`; `dff3941` is its parent-chain member. The claim
was true when written (pre-freeze) and remains true as "r34 tip"; the `master` alias has
moved one commit.

## 5. r34 tip ancestry

`git merge-base --is-ancestor dff394109f3cc3d851309ad7c67dd3b35b46adf2 master` → exit 0.
Also an ancestor of `origin/master` (`19e4ab3` — fetched ref, pushed). `dff3941` is the
grandparent of current `master` via `6d754bd` → `19e4ab3`. CONFIRMED.

## 6. Ancillary observations (no defects)

- C2 counter re-run on the committed spec: `uncovered=0 retired=1 toctou_declared=1
  ledger_tip_ok=1 verdict=TARGET_MET` exit 0 — the frozen chain is internally
  self-consistent today, independent of my checks above.
- The three adopted corpus entries (`corpus/knowledge/idle-lock-*.md`) are absent on disk —
  expected: the freeze predates data; not a provenance defect.
- Untracked under round-35: `dispatch-w1.sh`, `dispatch.out`, `w1-spec.json`,
  `w1-taskcall.json`, `w1/`, `scratch/` — wave runtime, none cited by the registration.
- No pointer in the registration cites the merge package by hash; package paths are
  named read-only sources, out of this check's hash scope.
