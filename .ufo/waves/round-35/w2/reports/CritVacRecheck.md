# CritVacRecheck — the vacuity finding holds on the real data: the counter cannot tell the real tree from junk except through a free variable

Seat: critic (leaf, no dispatch). Date: 2026-10-25. Round 35, wave 2.
Scratch: `.ufo/waves/round-35/scratch/CritVacRecheck/` (`build.py`, `probe.py`, `manifest.json`,
`results.txt`, arms `T0`–`T6`, `c2/C1`–`C3`, `repair/`).

Question put to this seat: wave 1 showed a shape-only junk tree reaches `TARGET_MET`. Does the
round's **real** tree differ from that junk tree in any way the counter can see, or only in
content the counter cannot see? Answer with a differential on a copy whose entry prose is
deleted and whose receipts are same-length different bytes.

## Counterexample

A copy of the real round-35 tree in which the three entries are reduced to their `gate-quote`
lines alone (6,358 of 7,295 bytes deleted, 87.2%; zero non-quote lines remain) and each of the
eight receipts is rewritten to the same byte length with different bytes (7,675 of 8,468 bytes
changed, 90.6%; every new file's sha256 differs from the frozen digest recorded for it; the only
preserved span is the quoted sentence the entry already names) still prints:

```sh
$ python3 -I .ufo/waves/round-35/c1/count.py \
    --root .ufo/waves/round-35/scratch/CritVacRecheck/T3-both \
    --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

The real tree, the mutated copy, and the wave-1 junk tree are **field-for-field identical** to
c1. Direct answer to the wave-2 question: the real tree differs from the junk tree **only in
content the counter cannot see**, plus the quoted sentence itself, which the entry supplies as a
free variable. The real tree is honest — its receipts do match the frozen digests 8/8, verified
below — but that is a fact about the bytes, not about the counter.

## Differential: every c1 field, every arm

`T3-both` is the assignment's copy. `T4/T5` answer the boundary question (what *can* the counter
see?). `T6` degrades every registry cell c1 never reads. `T0` proves the copy method is faithful.

| arm | what it changes | closed_entries | closed_rows | open_cites | verdict | exit |
|---|---|---|---|---|---|---|
| real lane root | — | 3 | 8 | 0 | TARGET_MET | 0 |
| T0-real-copy | nothing (byte-identical copy) | 3 | 8 | 0 | TARGET_MET | 0 |
| T1-prose-deleted | entries = gate-quote lines only | 3 | 8 | 0 | TARGET_MET | 0 |
| T2-receipts-replaced | receipts same length, ≤96.7% bytes differ, quote span kept | 3 | 8 | 0 | TARGET_MET | 0 |
| **T3-both** | **T1 + T2** | **3** | **8** | **0** | **TARGET_MET** | **0** |
| T4-receipts-all-diff | receipts same length, 100% bytes differ (quote destroyed too) | 0 | 0 | 8 | TARGET_MISSED | 1 |
| T5-both-all-diff | T1 + T4 | 0 | 0 | 8 | TARGET_MISSED | 1 |
| T6-unread-junk | row cells 1–4,6,8 = `junk`; entry prose = one junk line | 3 | 8 | 0 | TARGET_MET | 0 |
| wave-1 junk tree (`CritVacuous`, untouched) | — | 3 | 8 | 0 | TARGET_MET | 0 |

Commands for the seven arms, run verbatim (all before writing this seat's report):

```sh
$ for arm in T0-real-copy T1-prose-deleted T2-receipts-replaced T3-both \
             T4-receipts-all-diff T5-both-all-diff T6-unread-junk; do
    python3 -I .ufo/waves/round-35/c1/count.py \
      --root .ufo/waves/round-35/scratch/CritVacRecheck/$arm \
      --frozen .ufo/waves/round-35/c1/frozen.json; echo "exit=$?"; done
# T0..T3, T6: exit=0 TARGET_MET (3/8/0);  T4,T5: exit=1 TARGET_MISSED (0/0/8)
```

### The bytes, per receipt, in T3

| id | real B | arm B | bytes changed | quote span kept | sha(real) = frozen | sha(arm) = frozen |
|---|---|---|---|---|---|---|
| S203 | 3137 | 3137 | 3034 (96.7%) | 103 B | yes | no |
| S204 | 445 | 445 | 343 (77.1%) | 102 B | yes | no |
| S205 | 1194 | 1194 | 1092 (91.5%) | 102 B | yes | no |
| S206 | 929 | 929 | 818 (88.1%) | 111 B | yes | no |
| S207 | 705 | 705 | 613 (87.0%) | 92 B | yes | no |
| S208 | 768 | 768 | 663 (86.3%) | 105 B | yes | no |
| S209 | 905 | 905 | 809 (89.4%) | 96 B | yes | no |
| S210 | 385 | 385 | 303 (78.7%) | 82 B | yes | no |

`SOURCES.md` in T3 is **byte-identical** to the lane's (`sha256` prefix `848a7680c175f1ac…`), so
the registry side is unchanged: each row's anchor cell still carries the frozen digest string,
which is exactly what the implementation tests (`count.py:189`, `receipt["sha256"] in cs[5]`).
The computed digest at `count.py:174` is dead: AST scan gives `assignments to digest: [174]`,
`reads of digest: []`.

`T4` isolates the one receipt-content channel that *is* visible: with the same length but the
quoted sentence destroyed, `open_cites` moves 0→8. So the counter sees the quote's presence, not
the document.

## Differential: c2 (calibration)

copies under `scratch/CritVacRecheck/c2/` holding only the clause ledger, the ten control
receipts and the blob ledger (plus corpus in C1/C2, none at all in C3):

| repo | corpus present | uncovered | retired | toctou_declared | ledger_tip_ok | verdict | exit |
|---|---|---|---|---|---|---|---|
| real lane | real | 0 | 1 | 1 | 1 | TARGET_MET | 0 |
| C1-support-real | real copy | 0 | 1 | 1 | 1 | TARGET_MET | 0 |
| C2-support-mutated | **T3 mutated** | 0 | 1 | 1 | 1 | TARGET_MET | 0 |
| C3-ledger-only | **none** | 0 | 1 | 1 | 1 | TARGET_MET | 0 |

`strace` on C3: `corpus/` opens **0**, `knowledge/idle-lock*` opens **0**, `fetch/S2*` opens
**0**, `SOURCES.md` opens **0**; it opens `clauses.json`, the ten control receipts and the blob
ledger, then reaches `git` at the real repo root (`--repo` is not a containment boundary:
`git -C …/C3-ledger-only rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/mado-shokunin`,
and the seven blobs it re-verifies are all round-33/34 paths). c2's fields do not depend on the
corpus by design, and they did not move by one bit.

`strace` on c1/T3: it opens exactly `corpus/SOURCES.md`, the three entries, the eight receipts
and `frozen.json`; it opens **zero** cited host paths (`config.jsonc`, `omarchy-menu`, `idle.sh`,
`first-run`), zero census, zero real-corpus paths.

## Real vs junk: what the predicate actually sees

`probe.py` dumps the tuple `PRED-C1-r35-v1` reads for each cite (`entry_is_file`, `rows_for_id`,
`nf_cells`, `status`, `recheck_valid`, `frozen_sha_in_anchor`, `used_by_equals_citing`,
`quote_words`, `quote_in_blob`, `ok`).

- real lane vs T0 vs T3 vs T6: **IDENTICAL** on all eight cites.
- real lane vs wave-1 junk tree: the **only** differing field is `quote_words` (13,13,14,14,15,
  13,17,15 on the real tree vs 2 on every junk cite) — both inside the 1–25 bound, `ok=true` on
  every cite in both trees.

So the answer to the wave-2 question: the real tree differs from the junk tree **only in content
the counter cannot see**, plus the identity of the quoted sentence, which is a free variable the
entry itself supplies. There is no check whose value depends on the real tree being real. The
receipt bytes, their digests (which *are* true on the real tree, 8/8), the entry prose (6,358 B
of it), the registry's URL/title/source/claim cells, and the provenance of the quotes are all
outside the predicate. T6 shows the registry-side version of the same thing: replacing every
cell c1 does not read with `junk` moves nothing.

## Impacted axes

Round axes (registration): **coverage** (C1) and **calibration** (C2), the lowest non-retired
sub-axes; the other tied axes are untouched here.

- **Coverage** — impacted, and not merely at the margin. `closed_entries/closed_rows/open_cites`
  cannot distinguish the round's measurement from a tree that measured nothing: the claim "the
  corpus now measures the idle-lock offer surface" is not what `TARGET_MET` certifies.
- **Calibration** — not moved by corpus tampering (proved: C2 counts clause coverage of its own
  ledger). It becomes *coupled* the moment coverage is repaired, see below.
- **Receipt integrity** and **entry content** are sub-surfaces of coverage, not separate axes in
  this round; both are currently ungrounded.

## Smallest safe correction

The frozen predicate text already says: "…whose anchor cell carries **the sha256 of the named
receipt**…". The implementation substitutes `frozen.json`'s recorded value for the hash of the
bytes. That is implementation drift from the frozen text, not an over-broad spec — so the repair
needs no predicate re-freeze.

One added conjunct in `c1/count.py` (`digest` is already computed at line 174 and discarded):

```python
and digest == receipt["sha256"]          # the receipt bytes' sha256
and receipt["sha256"] in cs[5]           # and the row records it (unchanged)
```

Validated in `scratch/CritVacRecheck/repair/count_digest.py` (same `PREDICATE`/target strings, so
the frozen-spec check is untouched):

| tree | repaired counter | exit |
|---|---|---|
| real lane | TARGET_MET 3/8/0 | 0 |
| T0-real-copy | TARGET_MET 3/8/0 | 0 |
| `controls/golden` | TARGET_MET 3/8/0 | 0 |
| all 10 `controls/c1-*` | TARGET_MISSED each | 1 |
| **T3-both** | **TARGET_MISSED 0/0/8** | **1** |
| wave-1 junk tree | TARGET_MISSED 0/0/8 | 1 |
| T1-prose-deleted | TARGET_MET (residual) | 0 |
| T6-unread-junk | TARGET_MET (residual) | 0 |

Residuals, stated honestly: digest equality kills receipt-byte substitution (the assignment's
attack) but not prose deletion (T1) or junk in unread registry cells (T6). Prose presence is a
weaker, gameable clause; content truth is not obtainable from a static predicate at all.

Calibration coupling, verified: adding a live clause `digest-bytes-match` with no control gives
c2 `uncovered=1 verdict=TARGET_MISSED exit=1`; adding the T3 run receipt as its control restores
`uncovered=0 verdict=TARGET_MET exit=0`. So the repair is one line of code **plus** one control
tree + receipt + clause entry; shipping the line alone would break C2.

This is a fixable defect, not a tradeoff: golden and the real tree keep passing, every control
keeps failing, and the change restores the frozen text's meaning. What remains after the repair
is the part the canonical Rust judge must reject as admission evidence even when it passes: a
shape predicate cannot testify that any quote was read from the artifact it names, that any cited
path was observed, or that any entry asserts what its title says.

## One sentence

**The counter supplies admission evidence that twelve named files exist and line up — one
eleven-cell row per cite, used-by equals the frozen admit list, status `mined`, an in-vocabulary
recheck token, the recorded digest string inside the anchor cell, and a 1–25-word free-variable
line per cite occurring somewhere in a receipt file — and supplies no evidence that any receipt
is the document recorded, that any quote was located in the artifact it cites, that any entry
prose asserts a supported claim, or that any host path was observed: `TARGET_MET` is shape
closure, not measurement.**

## Scope and reproducibility

- Read-only on the lane: no corpus, counter, control, `SOURCES.md`, git index or jj state was
  modified. Everything written is under `.ufo/waves/round-35/scratch/CritVacRecheck/` and this
  report.
- No tool installs or upgrades.
- Raw command/output log: `.ufo/waves/round-35/scratch/CritVacRecheck/results.txt`; per-receipt
  length/digest/diff counts: `…/manifest.json`; arms are regenerated by `python3 -I
  .ufo/waves/round-35/scratch/CritVacRecheck/build.py`.
- One intermediate defect in my own harness is noted for audit: the first T6 arm replaced cell 0
  (the id, which `ROW_RE` reads) and mis-filtered `S20*` (excluding `S210`); it was
  corrected to junk only cells 1–4, 6, 8 of S203–S210 and re-run from scratch. The table above is
  the corrected run.
