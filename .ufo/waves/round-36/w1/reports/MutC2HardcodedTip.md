# MutC2HardcodedTip — mutation-tester seat, mado round 36 wave 1

Task: write a `/tmp` variant of C2 with the round-35 tip logic (hardcoded
`dff3941…` substring test plus spec-derived blob ids), run it against the four
r36-profile mutants `c2-tip-stale`, `c2-tip-one-copy`, `c2-blob-corrupt`,
`c2-blob-row-deleted`, and report which survive under the old logic and which
the round-36 rule kills.

## Instrument

`/tmp/c2-tip-variant.py` (sha256
`c482fd8a458dbb5b98f193b7f049e3a6cf7e86e6815dd5b7039b69aa7b7763b8`), one counter
with `--rule r35|r36` sharing the clause-scan machinery:

- `--rule r35` reproduces `.ufo/waves/round-35/c2/count.py` `ledger_tip_ok`
  verbatim (lines 113–131): `spec["r34_tip"] in text` (hardcoded
  `dff394109f3cc3d851309ad7c67dd3b35b46adf2`) then, per frozen-spec blob,
  `git rev-parse <r34_tip>:<path>` must equal the spec's `blob_id`. The blob
  ledger's own table is never parsed — the ids come from the spec.
- `--rule r36` implements the frozen `PRED-C2-r36-v1` tip rule
  (`.ufo/waves/round-36/c2/frozen.json` `tip_rule`): tip = newest commit whose
  subject names `round-34` via `git log -1 --format=%H --grep=round-34 master`
  → `6d754bd599caa7ab21c4c20b548c0fa83914ffce`; the doc must name the superseded
  r35 ledger; every 40-hex token on a tip-naming non-`supersedes` line must equal
  the computed tip (≥3 lines); every table row must name a frozen path whose blob
  id at the computed tip equals the row id; row set == frozen path set.
- Clause side under `--rule r35`: r35 scan (receipt contains
  `verdict=TARGET_MISSED`, or `not-load-bearing.reason`). Under `--rule r36`:
  r36 strict scan (live id set == frozen expected set; receipt records
  `TARGET_MISSED` and names the clause id; `retired` counts ids absent from live;
  exactly one declared `not-load-bearing` == `o-nofollow-open`).

Boundary note: mutants are `--profile r36` fixtures (they carry the r36 clause
ledger and r36 blob ledger), so the r35 counter could not be run unmodified —
its frozen spec points at the r35 ledger paths and its predicate/target strings
would die `predicate-drift`. The `--rule r35` path is a line-faithful port of
its `ledger_tip_ok` onto the fixture layout; `--repo` supplies file reads,
`--git` supplies `rev-parse` against the lane repo (fixtures are not repos).

## Commands

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
for d in c2-tip-stale c2-tip-one-copy c2-blob-corrupt c2-blob-row-deleted; do
  for rule in r35 r36; do
    python3 -I /tmp/c2-tip-variant.py \
      --repo /tmp/mado-r36-mutants-r36/$d --git . \
      --frozen .ufo/waves/round-36/c2/frozen.json \
      --r35spec .ufo/waves/round-35/c2/frozen.json --rule $rule
  done
done
```

## Results (actual output lines)

Baseline — pristine lane inputs (`--repo .`):

```
PRISTINE rule=r35 uncovered=0 retired=1 toctou_declared=1 tip_ok=1 tip_why='substring+spec-ids ok' verdict=TARGET_MET   exit=0
PRISTINE rule=r36 uncovered=0 retired=1 toctou_declared=1 tip_ok=1 tip_why='computed=6d754bd599caa7ab21c4c20b548c0fa83914ffce lines=10 rows=7 all-verified' verdict=TARGET_MET   exit=0
```

Mutants:

```
c2-tip-stale        r35: tip_ok=1 tip_why='substring+spec-ids ok' verdict=TARGET_MET    exit=0
c2-tip-stale        r36: tip_ok=0 tip_why='tip-token fa7ba1134611… != computed 6d754bd599ca… line=round-34 lane tip `fa7ba113…`.' verdict=TARGET_MISSED exit=1
c2-tip-one-copy     r35: tip_ok=1 tip_why='substring+spec-ids ok' verdict=TARGET_MET    exit=0
c2-tip-one-copy     r36: tip_ok=0 tip_why='tip-token fa7ba1134611… != computed 6d754bd599ca…' verdict=TARGET_MISSED exit=1
c2-blob-corrupt     r35: tip_ok=1 tip_why='substring+spec-ids ok' verdict=TARGET_MET    exit=0
c2-blob-corrupt     r36: tip_ok=0 tip_why='row .ufo/waves/round-33/c1/count.py id 000000000000… != git 4ab3db435dd2… @computed-tip' verdict=TARGET_MISSED exit=1
c2-blob-row-deleted r35: tip_ok=1 tip_why='substring+spec-ids ok' verdict=TARGET_MET    exit=0
c2-blob-row-deleted r36: tip_ok=0 tip_why="row-set […6 paths] != frozen […7 paths]" verdict=TARGET_MISSED exit=1
```

All four mutants show `uncovered=0 retired=1 toctou_declared=1` on the clause
side — the tip/blob rule is the deciding observable in every case.

| Control | Mutation applied | r35 tip rule | r36 tip rule |
|---|---|---|---|
| `c2-tip-stale` | all 4 tip-line hexes → `fa7ba113` (stale label) | **SURVIVES** (`TARGET_MET`) | killed (`TARGET_MISSED`) |
| `c2-tip-one-copy` | 1st tip-line hex → `fa7ba113` | **SURVIVES** (`TARGET_MET`) | killed |
| `c2-blob-corrupt` | row 1 blob id → `0…0` | **SURVIVES** (`TARGET_MET`) | killed |
| `c2-blob-row-deleted` | last table row deleted | **SURVIVES** (`TARGET_MET`) | killed |

## Why they survive under r35 — the mechanism

`grep -c dff394109f3cc3d851309ad7c67dd3b35b46adf2` on each mutated ledger → **3**
for all four fixtures: the hardcoded tip survives untouched on the `supersedes`
line (L12–13), in the "Refs resolved" list (L23), and in §2's prose (L50-ish
range of the pristine file). The substring test does not parse which line *names*
the tip, so rewriting every tip-labelled token (`c2-tip-stale`) or one copy
(`c2-tip-one-copy`) leaves `tip_ok=1`. The blob check re-derives ids from the
*spec's* `frozen_blobs` list at the spec's `r34_tip` revision — all seven
`rev-parse dff3941:<path>` calls still return the spec ids because those paths
are byte-identical at `dff3941` and `6d754bd` — so a corrupted or deleted row in
the document is invisible. This is exactly the D4 fail-open the round-36 frozen
spec routes.

## Restoration evidence

Fixtures were treated read-only: no writes into `/tmp/mado-r36-mutants-r36`.
Post-run sha256 of each mutated ledger (unchanged from generation, verified by
`diff` against the lane's pristine `RevFrozenBlobs-r36.md` showing only the
intended mutation lines — quoted diffs obtained and matched):

- `c2-tip-stale` ledger `e95dff70b6daa537eedb088aa5660191df9d3bf9c3d964b66398e82253e7d05b`
- `c2-tip-one-copy` ledger `db70d97c969a048b137c18c418896df2c2ae653e48dc8db008e1839424ec6009`
- `c2-blob-corrupt` ledger `a18bb076c48d462f0f0624a222cc58d4246a41ee41de8d3589f92ed8496f38ca`
- `c2-blob-row-deleted` ledger `75d158cd4a012b0c3026228f2443e737b0a74e4639ec512413374ce757541e37`
- pristine lane: `clauses.json` `23896383e6012ed5e84eb3f47efdfe3248b9c15b1b2b5e22f33bcf11c0d7b44c`, `RevFrozenBlobs-r36.md` `25ca85c4ecd1c72d6c0cdc96f14c94d2d2d6ee16df4ee5b8fd8be08dcaae138d` (git-tracked, untouched).

(All four mutant `clauses.json` files hash `1762fde6…` — the generator's
re-serialised copy, differing from the lane file only by `indent=1` JSON
formatting, not content.)

Writes: `/tmp/c2-tip-variant.py`, this report. No production file touched; no
tool installs needed (python3/git only).

## Verdict

- Mutation probe: **killed under round-36 rule, survives under round-35 rule —
  4/4 fixtures.** The old tip logic is confirmed vacuous on exactly the attack
  class it was retired for (stale/rewritten tip label, doctored table), and the
  frozen r36 rule kills each mutation at the observable it targets:
  `tip-token != computed` (2), `row id != git blob id` (1), `row-set != frozen`
  (1). Baseline `TARGET_MET` under both rules → no fixture-defect ambiguity;
  mutant survival is a property of the r35 instrument, not the fixtures.
- Secondary observation (not a new claim): the hardcoded string the r35 rule
  greps for is *also* what the frozen spec's `supersedes` audit would have kept;
  the `supersedes` line exemption plus `min_tip_lines=3` is what prevents that
  same string from laundering the doc under r36.
