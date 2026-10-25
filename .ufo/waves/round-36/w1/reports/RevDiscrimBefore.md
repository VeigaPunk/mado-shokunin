# RevDiscrimBefore — frozen before-measurement re-run and line audit

Seat: `L1Mado36.RevDiscrimBefore` (reviewer, wave 1, round 36). Lane: mado-shokunin.
Read-only on every production file. Writes: this report and `/tmp/w36-rev-discrim/`
(25 receipts, the counter's own `--receipts` output). No tool installs (python3
3.14.8 sufficed).

## 1. Re-run result — the frozen before-number reproduces exactly

Assigned command, run verbatim:

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-counter-discrimination.py \
    --profile r35 --manifest .ufo/waves/round-36/controls/manifest.json --receipts /tmp/w36-rev-discrim
…
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=14/25 label='round-35 frozen counters (unmodified)' verdict=TARGET_MISSED
EXIT=1
```

Byte-identity check vs the frozen receipt:

```
$ python3 -I quality/check-counter-discrimination.py --profile r35 --manifest \
    .ufo/waves/round-36/controls/manifest.json --receipts /tmp/w36-rev-discrim | \
    diff -u .ufo/waves/round-36/receipts/before-discrimination.txt -
DIFF_EXIT=0
```

Zero-diff: all 25 `control=` lines, all 10 `clause=` rows, and the
`MADO_DISCRIMINATION` summary reproduce `receipts/before-discrimination.txt`
verbatim. **14/25 confirmed** (14 `ok=1`, 11 `ok=0`), exit 1 = `TARGET_MISSED`.

Manifest count note (not a defect): the assignment text says "15 c1 controls"; the
frozen manifest at `.ufo/waves/round-36/controls/manifest.json` and the
registration table (`registration.md:132`) both carry **16** c1 controls (2 accept
+ 14 reject) and 9 c2 (1 accept + 8 reject) = 25. I audited all 25.

## 2. The mechanism under audit

`--profile r35` runs the **round-35 counters unmodified**
(`check-counter-discrimination.py:33-40`): `c1/count.py` per control `--root`
(`:144-146`), `c2/count.py` per `--repo` (`:158-159`), `observed_of` maps
`verdict=` or rc-2/none→`ERROR` (`:68-72`). c2 fixtures are generated to
`/tmp/mado-r36-mutants-r35` by `.ufo/waves/round-36/c2/gen-mutants.py` from the r35
ledgers (`gen-mutants.py:30-39`). `GIT_DIR=<lane>/.git` is exported (`:96`), so the
r35 c2 counter's `git -C <mutant> rev-parse <r34_tip>:<path>` queries the lane's
object store regardless of the mutated `--repo` bytes — that is exactly why the
blob-ledger mutations cannot fail under r35 (see F-D4 below).

Every `ok=0` is an instrument *accept* of a *reject* control (`observed=TARGET_MET`,
`expected=TARGET_MISSED`). Every reject fixture is genuinely illegitimate (each
differs from its accept base in one committed input — diffs quoted in §4/§5), so
**no `ok=0` line is a legitimate reject of a legitimate control; all eleven are
instrument blindness**.

## 3. Routed-defect attribution for each `ok=0`

| `ok=0` line | Routed defect | Evidence class (LANE/.ufo/waves/round-35) |
|---|---|---|
| `c1-shape-only` | **D3** — dead digest clause | `c1/count.py:174` dead store `digest = hashlib.sha256(blob).hexdigest()`; accepting conjunct `:192` `receipt["sha256"] in cs[5]` tests the *manifest's* string, never the bytes. `corpus/lessons/round-35-verifier-spotcheck.md:223-227` (D3), `w2/reports/RevC1Tip.md` F1 §4.1 (`count.py:174` store, `loaded_later=False`; m1b probe: appended receipt `889be5a1…` ≠ frozen `1d30e4a9…` still `TARGET_MET`). |
| `c1-fabricated-payload` | **D3** | Same dead store. The crib proves laundering: receipts read `THIS IS NOT A FETCHED RECEIPT / fabricated attestation …` yet `TARGET_MET` because quotes are substrings of the fabricated bytes and the anchor's frozen string is unchanged. |
| `c1-no-registry-heading` | **F2/E12** — registry-section gap | `rows_for` (`c1/count.py:118-124`) scans *every* line of `SOURCES.md`; no `## Registry` scoping. `w2/reports/RevC1Tip.md` F2 §4.2: m9b moved row → `TARGET_MET`; lane census flags `E12 S206 row outside Registry section`. |
| `c1-row-moved-out` | **F2/E12** | Same mechanism: S206 row verbatim under a new `## Leads (unopened)` heading still closes. |
| `c2-tip-stale` | **D4** — self-authored observables | `ledger_tip_ok` = `spec["r34_tip"] in text` substring test (`c2/count.py:113-131`, spot-check `:129-133`). Mutant replaces 4 tip-label hashes `dff3941→fa7ba113`; `dff3941` survives on the untouched "docs commit" line 17 → substring still hits, `ledger_tip_ok=1`. |
| `c2-tip-one-copy` | **D4** | Same substring test; one replaced label still passes (hash persists at lines 13/17/19/53). |
| `c2-blob-corrupt` | **D4** | Table row zeroed to `00…00` — never parsed; re-verification iterates `spec["frozen_blobs"]` (frozen spec), not the document's rows. |
| `c2-blob-row-deleted` | **D4** | Last table row deleted — same: doc table unread, spec list unchanged. |
| `c2-clause-deleted` | **D4** | `uncovered` iterates `ledger["live"]` (`count.py:88-101`): deleting `gate-quote-word-bound` removes it from the scan → fail-open on deletion (spot-check `:127-128`). |
| `c2-receipt-token` | **D4** | `MISSED = re.compile(r"verdict=TARGET_MISSED")` token grep (`count.py:32,99-100`); a 1-byte-content receipt still covers the clause. |
| `c2-receipt-unbound` | **D4** | `entry-symlink` receipt byte-replaced by `row-duplicate`'s receipt (still grep-hits); no clause↔receipt binding (spot-check D4: "bind clause receipts to clause ids"). |

The clause-binding table corroborates: `clause=digest-match controls=3 missed=1`
(one of three killable), `clause=row-in-registry controls=2 missed=0` (zero of two
killable); all eight other named clauses `missed=1`.

## 4. Per-control audit — c1 (16)

Baseline: `controls/golden` is the r35 8-row crib. Each r35 control's four scored
text files were diffed vs `golden`; the eight receipts are byte-identical to live
in every c1 tree except the two content cribs (verified by `cmp` over the 12-file
scored set — `RevC1Tip.md:173-175` reports the same `differing=0`).

| control | Observed (receipt `/tmp/w36-rev-discrim/*.txt`) | Legitimacy (diff vs base) | Verdict |
|---|---|---|---|
| c1-live | `3/8/0` MET, ok=1 | Live tree; 8 rows inside `## Registry` (L205-212) | PASS |
| c1-golden-r36 | `3/8/0` MET, ok=1 | = golden + `## Registry` heading block only (entries, receipts `cmp`-identical) | PASS |
| c1-donothing | `0/0/8` MISSED, ok=1 | Rows deleted, all 3 entries absent | PASS |
| c1-digest | `2/7/1` MISSED, ok=1 | S210 anchor sha → 64 zeros (row cell, not receipt bytes) | PASS |
| c1-entry-symlink | `2/7/1` MISSED, ok=1 | `idle-lock-chain-armed-r14.md` is a symlink → `never-asked-r12.md` (`lrwxrwxrwx`, lstat-confirmed); S_ISLNK walk kills it | PASS |
| c1-quote-absent | `2/7/1` MISSED, ok=1 | S206 gate-quote text not a substring of the receipt | PASS |
| c1-quote-long | `2/7/1` MISSED, ok=1 | S203 gate-quote >25 words (script-dump paste) | PASS |
| c1-recheck-prose | `2/7/1` MISSED, ok=1 | S209 recheck cell `→ ` 90d - re-verify the fetch` (leading space + prose → invalid token) | PASS |
| c1-row-duplicate | `2/7/1` MISSED, ok=1 | Second `| S205 |` row appended → `len(rows)!=1` | PASS |
| c1-row-extra-field | `2/7/1` MISSED, ok=1 | S206 gains `| with an extra field` → 12 cells ≠ 11 | PASS |
| c1-status-queued | `2/7/1` MISSED, ok=1 | S208 status `mined` → ` queued ` | PASS |
| c1-usedby-extra | `2/7/1` MISSED, ok=1 | S207 used-by gains `corpus/knowledge/idle-lock-chain-armed-r14.md` → `used_by ≠ citing` | PASS |
| c1-shape-only | `3/8/0` **MET, ok=0** | Rows: all content cells `junk`, anchors keep frozen sha, status `mined`; receipts 36-151 B of filler (e.g. S206 = `void void void thud xyzzy void void`), quotes are substrings of that filler | FAIL = **D3** (receipt bytes unbound; correct reject) |
| c1-fabricated-payload | `3/8/0` **MET, ok=0** | All 8 receipts = self-labelled fabricated attestations (78 B each, no real bytes); quotes substring-match fabrications | FAIL = **D3** (launders fabricated evidence — `RevC1Tip` F1 §7 "the one defect that can launder fabricated evidence") |
| c1-no-registry-heading | `3/8/0` **MET, ok=0** | = `golden` tree: rows exist, file has zero `## Registry` heading | FAIL = **F2/E12** (correct reject) |
| c1-row-moved-out | `3/8/0` **MET, ok=0** | = golden-r36 except S206 row moved verbatim out of `## Registry` under new `## Leads (unopened)` | FAIL = **F2/E12** (mirrors `RevC1Tip` m9b probe exactly) |

## 5. Per-control audit — c2 (9)

Fixtures under `/tmp/mado-r36-mutants-r35/<id>/`: each copies
`c1/clauses.json`, `ledger/RevFrozenBlobs-r35.md`, and the nine clause receipts;
verified `cmp` per file — exactly the one mutated input differs per kind.

| control | Observed | Mutation (verified diff) | Verdict |
|---|---|---|---|
| c2-live | `uncovered=0 retired=1 toctou=1 tip_ok=1` MET, ok=1 | Lane repo itself | PASS |
| c2-tip-stale | all-four MET, ok=0 | 4 tip-label hashes → `fa7ba113…`; `dff3941` survives at doc line 17 (non-"tip" line, untouched) | FAIL = **D4** |
| c2-tip-one-copy | MET, ok=0 | 1 tip line → `fa7ba113…`; other mentions satisfy substring | FAIL = **D4** |
| c2-blob-corrupt | MET, ok=0 | row `.ufo/waves/round-33/c1/count.py` blob id → 40 zeros; doc table never parsed | FAIL = **D4** |
| c2-blob-row-deleted | MET, ok=0 | row `.ufo/waves/round-34/c2/frozen.json` deleted; spec's 7-blob list still verified from git | FAIL = **D4** |
| c2-clause-deleted | MET, ok=0 | `gate-quote-word-bound` clause block removed from `live`; `uncovered` can't see it | FAIL = **D4** |
| c2-receipt-token | MET, ok=0 | `c1-entry-symlink.txt` → `verdict=TARGET_MISSED\n` only; token grep satisfied | FAIL = **D4** |
| c2-receipt-unbound | MET, ok=0 | `c1-entry-symlink.txt` bytes replaced by `c1-row-duplicate`'s receipt | FAIL = **D4** |
| c2-retired-also-live | `uncovered=0 retired=0 toctou=0 tip_ok=1` MISSED, ok=1 | retired `r34-word-bound-1-25` re-appended to `live` with `not-load-bearing` | PASS — the one kind the r35 counter already kills (registration's demonstration-obligation exception) |

All nine c2 controls are legitimate fixtures; the seven `ok=0` are correct
rejects mis-accepted by D4's self-authored observables, not legit rejects of
legit controls.

## 6. Verdict

- **Before-measurement re-run: PASS** — byte-identical to the frozen
  `receipts/before-discrimination.txt`, `correct=14/25`, exit 1.
- **`ok=0` audit: PASS** — 11/11 failures attribute to the routed classes:
  2×D3 (dead digest), 2×F2/E12 (registry-section gap), 7×D4 (fail-open
  self-observables). No `ok=0` is a legitimate reject of a legitimate control.
- **Residual:** the prompt's "15 c1 controls" undercounts the frozen manifest by
  one (16 audited; manifest and `registration.md:132` agree). `c1-digest`
  exercises the *row-cell* read of the digest clause only (`RevC1Tip` F1 §4.1
  already notes it cannot exercise receipt bytes) — fine for r35 scoring, but the
  r36 repaired counter needs the content cribs, not `c1-digest`, as its
  receipt-bytes evidence; both exist in the manifest.
