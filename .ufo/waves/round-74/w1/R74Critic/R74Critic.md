# R74Critic — falsification review, round mado 74 wave 1

Seat: R74Critic (leaf, no dispatch). Method: committed bytes only, plus independent
re-derivation in scratch `/fast/scratch/hyaku/mado-r74/R74Critic/` (lanes rebuilt from the
committed `LANE_TEMPLATE`, both rules runpy'd from committed bytes). No git/jj mutation; no
writes outside my lane dir and scratch (scratch deleted at the end). No tools installed.

Verdicts: **C1 stands. C2 stands** — every frozen number reproduces from committed bytes; two
non-fatal blemishes are documented (§2, §5).

## 1. Target arithmetic re-derived from the receipts — CONFIRMED

- **C1** (`measurement-c1-r74.txt`, `cases=12 correct=12 base_correct=8`): exactly four
  `base_correct=no` scenario lines — `replay-captured`, `replay-no-witness`, `witness-mismatch`,
  `witness-last-wins` (each `expect=fail`, `base=pass` — the held round-72 rule credits all four
  replays). 12 − 4 = 8 = `base_correct`; candidate correct on all 12. The counter pins this:
  `FROZEN_CORRECT=12`, `FROZEN_BASE_CORRECT=8` (c1-r74-replay-witness.py:52-53), kill rule
  `TARGET_MET` iff both exact. Independent re-run of the twelve lanes with held+candidate credit:
  `correct=12/12 base_correct=8/12`, per-case verdicts and rc (0,1,1,2,1,1,1,1,1,1,1,1) match the
  receipt line for line.
- **C2** (`measurement-c2-r74.txt`, `controls=36/36 base_controls=32/36`): exactly four base-leg
  `correct=no` lines — `twohop-attr-store-dotted-call`, `twohop-attr-store-alias-call`,
  `environ-alias-call-guard`, `environ-alias-splat-guard` (all `guard=no` vs
  `expect_guard=yes`; base misses exactly the four new positives). 36 − 4 = 32. Counter pins
  `FROZEN_POPULATION=20 FROZEN_READERS=13 FROZEN_GUARDED=13 FROZEN_CONTROLS=36
  FROZEN_BASE_CONTROLS=32` (c2-r74-shapes.py:64-68). Independent runpy of held+candidate
  `classify` over all 36: held 32/36 with exactly those four misses, candidate 36/36. The
  population leg also checks out: 20 `MADO_R74_READER` lines, 13 `reader=yes guard=yes`, 7
  `reader=no`.

## 2. Case distinctness — CONFIRMED, one latent duplicate pair (C1)

Rebuilt all twelve lanes from the counter's committed `LANE_TEMPLATE` in scratch, ran each with a
fixed fresh nonce (`f1e2d3c4b5a69788`, ≠ stale `0123456789abcdef`), compared the **combined
stream** (`stdout+stderr` concatenated — the exact bytes `credit()` consumes) pairwise:

| mode | rc | combined sha256 (12 hex) |
|---|---|---|
| liar-success | 0 | `5000cf9cd114` |
| stderr-genuine | 1 | `5000cf9cd114` ← **identical to liar-success** |
| liar-kill | 1 | `c60fdd037ffd` |
| crash-stderr | 2 | `e4535c4a932f` |
| bare-failing | 1 | `8fcfd84d1c5e` |
| mismatch-detail | 1 | `99bf765dccc4` |
| last-wins-pass | 1 | `b65ea9d1bb5a` |
| last-wins-fail | 1 | `98be6240e67b` |
| replay-captured | 1 | `ae63fcfd3b88` |
| replay-no-witness | 1 | `1db21c7ce603` |
| witness-mismatch | 1 | `3e63137d8289` |
| witness-last-wins | 1 | `b6b4aee8a261` |

- `liar-success` and `stderr-genuine` emit **byte-identical combined output** (same FAIL line,
  witness, summary; only the stream split and exit status differ: rc 0 vs 1). Neither C1 rule
  sees rc or stream separation — `credit(out)` (r72) and `credit(out, nonce)` (r74) take the
  combined string only — so the twelve cases carry at most **eleven distinct rule-visible
  inputs**. Impact on the claim: none — both modes are frozen `expect=pass` and both rules
  answer `pass`; no scoring arithmetic moves. But the set's fault coverage is thinner than
  "twelve" suggests; this sits inside the declared limit "the twelve cases are fixture lanes,
  not fault coverage" and is worth a note in the next declaration, not a re-cut.
- All other 65 pairs are byte-distinct. The one-nonce-per-run design (one `secrets.token_hex(8)`
  shared by all twelve children in `measure()`) is what makes the pair collide; per-case nonces
  would not separate them either, since the duplicate is in the body bytes, not the nonce.
- **C2 new eight** (`twohop-attr-store-dotted-call`, `twohop-attr-store-alias-call`,
  `environ-alias-call-guard`, `environ-alias-splat-guard`, `twohop-attr-store-after-call`,
  `twohop-attr-store-replaced`, `environ-alias-no-store`, `environ-alias-rebound`): no duplicate
  `src` bytes pairwise, no duplicate names; across all 36, all `src` hashes distinct.

## 3. Held-leg provenance — CONFIRMED

- `--base-rev bd5a971532f37df85a78f6f566dd1e649b79de11` resolves (`git rev-parse …^{commit}` →
  itself; parent of the freeze commit `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`).
- Both counters load the held rule by `git show <resolved-base>:<path>` and `runpy` the bytes
  (c1-r74-replay-witness.py `extract()/measure()`; c2-r74-shapes.py:30-31,1289-1298) — not from
  the mutable working tree.
- sha256 at `bd5a9715` (== working tree, byte-identical):
  - `quality/counters/c1-r72-landing-controls.py` = `b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d` (matches the receipt's `role=base` line),
  - `quality/counters/c2-r73-shapes.py` = `95fd2b7b44ba773eab25349659ac92235f7ca133adaee78883aa9496ed3ec9a4` (matches `MADO_R74_BASE_COUNTER`).
- Candidate at the freeze rev `b73db77`: `c1-r74-witness-rule.py` = `6a6d77f4ad6777a01c49fa0c4e46a7d510e4f525c71a0c4c3f6280bb01394516` (matches receipt), `c2-r74-shapes.py` = `8a0fc3b24d66fb66f710b0c5c4ac0d8e83826960bc25fdf732652a9108497ab6`; both equal the working tree.

## 4. Freeze order — one-commit landing weakens strong provenance; no counterexample; stands with caveat

`b73db77` ("round-74: frozen claims, the pre-freeze control receipt and the two successor
instruments", author 02:24:52 -0300, commit 02:34:50 -0300) lands in **one** commit: the
declaration, `control-baseline-r74.txt`, both control JSONs, `proto/held-r74.py`, and all three
instruments (8 files, +2892). Git history therefore cannot prove the declaration or the frozen
sets **predated** the candidate instruments — temporal priority is simply not in the bytes; an
author could have co-designed target and rule before committing. What the committed bytes *do*
prove:

- The declaration's digests match the committed files: `17c9577…` (c1 cases), `4db4cc70…` (c2
  cases) — recomputed, exact.
- Both counters hash-check the controls at run time against those frozen digests (SetupError on
  drift), and C2 additionally re-extracts `.ufo/waves/round-73/controls/c2-cases-r73.json` at
  `--rev`, hash-checks `65e94644…` and asserts all 28 held cases byte-identical — the scored runs
  could not have used mutated data.
- **The order receipt is the baseline's held legs**: `control-baseline-r74.txt` ends
  `c1_correct=8/12 → TARGET_MISSED`, `c2_correct=32/36 → TARGET_MISSED` — the do-nothing control
  misses both targets pre-freeze, and both measurement receipts (which embed
  `rev=b73db773aaf…`, i.e. they are post-freeze runs, still untracked) independently reproduce
  exactly 8/12 and 32/36 in-run with the same per-case miss names. A target retro-fitted around a
  passing control would have to survive `base_correct==8` and `base_controls==32` pinned as
  exact kill-rule constants; it does, against rules that existed in round 72/73.
- **Counterexample search: none.** No committed receipt shows a do-nothing control meeting its
  target — held C1 tops out at 8/12 (needs 12), held C2 at 32/36 (needs 36).
- Residual, stated plainly: the baseline receipt carries no `rev=` stamp and the prototype that
  produced it is committed in the same commit, so "baseline before candidate" rests on the
  declaration's word plus the exact-base arithmetic above, not on commit ordering. A future
  round should stamp pre-freeze receipts with `rev=`/timestamp to close this.

## 5. Padding — carrying is real and enforced; four new C2 cases are not rule-discriminating

- **28 of 36 C2 cases are carried from round 73 — and honestly so.** First 28 of
  `c2-cases-r74.json` compare byte-identical (full object equality: name, src, both expectations)
  to `c2-cases-r73.json` (`65e9464450d58f803ca626f7b7ce6bc4712f46710ac5707602601cee9ecf230d` —
  matches `MADO_R74_HELD_CONTROLS carried=yes`); the counter re-verifies this every run. The
  carrying is the no-harm denominator, not inflation.
- **Not load-bearing between the two rules** (identical answer under held and successor — here
  the four new **negatives**): `twohop-attr-store-after-call`, `twohop-attr-store-replaced`,
  `environ-alias-no-store`, `environ-alias-rebound` — both rules answer `(True, False)` ==
  expected. The held rule passes them by omission; they are over-fire guards for the successor's
  new machinery (store after launch, dotted-path replacement, no store, alias rebinding), which
  is exactly the role the claim's "a rebinding … or a store after the launch not counted"
  sentence needs. Under the strict "flips between rules" definition, the only discriminating new
  cases are the four positives (§1) — and the kill rule `base_controls==32` **requires** that
  they are the only flips, so the arithmetic and the set agree.
- C1 analog: the four replay cases are the only base-discriminating cases (held credits all four;
  candidate rejects all four), pinned by `base_correct==8`.

## Bottom line

Both claims survive falsification on every committed byte I could reach: arithmetic exact,
held-leg provenance hash-verified at the named base rev, carrying enforced in-code, no
do-nothing counterexample. Two blemishes to carry forward, neither claim-breaking: (a) the C1
`liar-success`/`stderr-genuine` pair is rule-indistinguishable (byte-identical combined output;
only rc separates), capping distinct C1 rule inputs at 11 of 12; (b) one-commit freeze landing
leaves "frozen before data" provable only via the exact-base kill constants and the in-run
reproduced baseline, not via git ordering — stamp pre-freeze receipts with `rev=` next round.

Evidence commands (all read-only): `git rev-parse/show/ls-tree/status/log/cat-file` at
`bd5a9715`/`b73db77`; sha256sum of controls/counters; in-scratch rebuild+run of the 12 C1 lanes;
runpy of `credit`/`classify` from committed bytes over the frozen sets. Scratch deleted after
this report; nothing cited from scratch that is not reproduced above.
