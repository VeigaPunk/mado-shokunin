# R76 population re-derivation (independent of the lane gate)

Seat: R76ScoutPopulation. Rev: `cb713254ee9926e036e594312fdc61b57825526b` (freeze v2).
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. No lane gate was executed; the
counter's own `classify()` was imported read-only from
`quality/counters/c2-r76-shapes.py` at measurement rev `755b339f…` only to name the
predicates after the bytes had been read.

## Method (bytes first)

```
git ls-tree -r --name-only cb713254… -- quality        # then filter /^quality/check-[^/]+\.py$/
git show cb713254…:<path> > scratch/at/<path>          # for each of the listed files
grep -c 'GIT_NO_REPLACE_OBJECTS' scratch/at/quality/check-*.py
```

Every count below is taken from the freeze-rev bytes, never from the worktree.

## Result

| # | file | names key | has `"git"` token + read verb (`is_reader`) | guard assignment site | guard handed to git | census guard |
|---|---|---|---|---|---|---|
| 1 | check-anchor-cover.py | yes | yes | :104 dict literal | `git_blob(..., env)` → `subprocess.run(..., env=env)` :22 | yes |
| 2 | check-axis-scores.py | yes | yes | :99, :122 | `subprocess.run(..., env=env)` :100, :123 | yes |
| 3 | check-control-receipts.py | yes | yes | :62 | `git()` → `subprocess.run(..., env=env)` :65 | yes |
| 4 | check-counter-discrimination.py | no | no | — | — (sets `GIT_DIR` only; no git argv) | no |
| 5 | check-deliverables.py | yes | yes | :96, :116 | `subprocess.run(..., env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))` | yes |
| 6 | check-evidence-pointers.py | yes | yes | :72 module `GIT_ENV` | `env=GIT_ENV` :82, :180, :212 | yes |
| 7 | check-freeze-order.py | yes | yes | :46 in `git_env()` | `env=git_env(work)` :189 | yes |
| 8 | check-index-rows.py | yes | yes | :57, :406 | `subprocess.check_output(..., env=env)` :58; fixture commit env :404 | yes |
| 9 | check-index.py | yes | yes | :50, :283 | `subprocess.check_output(..., env=env)` :51; fixture env :281 | yes |
| 10 | check-landed-contract.py | yes | yes | :57 | `subprocess.run(..., env=dict(...))` :55 | yes |
| 11 | check-locators.py | no | no | — | — | no |
| 12 | check-population.py | no | no | — | — | no |
| 13 | check-r38-discrimination.py | no | no | — | — | no |
| 14 | check-r55-controls.py | no | no | — | — | no |
| 15 | check-r56-controls.py | no | no | — | — | no |
| 16 | check-round-outcome-first.py | yes | yes | :74, :128 | `subprocess.run(..., env=dict(...))` :71, :126 | yes |
| 17 | check-session-material.py | yes | yes | :927, :984 | `subprocess.run(..., env=dict(...))` :925, :982 | yes |
| 18 | check-state-cite.py | no | no | — | — | no |
| 19 | check-tool-ledger.py | yes | yes | :109 in `git_env()` | `env=git_env()` :116, :128; `env=self.env` :484 | yes |
| 20 | check-wave-done.py | yes | yes | :187 in `git_env()` | `env=git_env()` :195; `env=self.env` :601; `env=env` :645 | yes |

**Derived counts: population=20, readers=13, guarded=13, unguarded=0.**

- `population` — 20 files match `^quality/check-[^/]+\.py$` at the freeze rev.
- `readers` — 13 files contain the literal `GIT_NO_REPLACE_OBJECTS`; the same 13 pass the
  counter's `is_reader` predicate (`["']git["']` token **and** a quoted read verb). No file
  matches one predicate and not the other (`XOR` set empty), so the count is not predicate-sensitive.
- `guarded` — in all 13 readers the occurrence is an assignment (`env["GIT_NO_REPLACE_OBJECTS"] = "1"`,
  the same as a dict-literal entry, or `GIT_NO_REPLACE_OBJECTS="1"` in a `dict(...)`/`os.environ`
  copy), and in every case that mapping reaches a `subprocess.*` call as `env=`. No reader only
  mentions the string in a comment or docstring. Handoff was checked by reading the call sites,
  including the three helper-style files (`git_env()` in check-freeze-order/check-tool-ledger/
  check-wave-done, `git_blob` in check-anchor-cover, `git()` in check-control-receipts).
- `unguarded` — 0: no reader has a guard assignment that fails to reach a git call.

This reproduces the committed receipt line exactly:
`.ufo/waves/round-76/measurement-c2-r76.txt` →
`MADO_R76_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET`.
An independent `classify()` pass over the same 20 byte blobs also returns 20/13/13/0.

## Population boundary (observation, not a count defect)

The reader predicate is "names the key", so a check that launches git **without** the guard
and never names the key is outside the population and cannot be seen by `unguarded=0`:

- `quality/check-r38-discrimination.py` invokes git six times (`clone :163`, `sparse-checkout
  :169/:170`, `checkout :172`, `add :181`, `commit :182`) with
  `ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}` (:39) and no
  `GIT_NO_REPLACE_OBJECTS`, so an ambient replacement configuration would reach those calls.
  It is counted `reader=no guard=no` because it never names the key.
- `quality/check-counter-discrimination.py` sets only `GIT_DIR` (:123) and runs fixture scripts,
  not git argv; it is genuinely not a reader.

Consequence for the claim: `unguarded=0` means "no *reader* lacks a guard", not "no check
invokes git unguarded". The frozen target only asserts the former, so this does not move the
verdict; it qualifies what the census can see.

## Carried-set check (independent)

`controls/c2-cases-r76.json` vs `controls/c2-cases-r75.json`:
47 round-75 cases present, 0 missing, 0 field-changed (name, src, expect_reader, expect_guard
compared as whole objects); 12 new names; total 59; `carried` field = 47. Byte-identity holds.

Doc nit: the frozen control file's own `note` says "thirteen appended: three interprocedural
cancellations … one dynamic-key delete … and eight negatives". 3+1+8 = 12, and 12 names are in
fact appended (47+12=59). The declaration table and the counts are consistent at 12; only the
prose word "thirteen" is wrong. The file is frozen (sha256 `df9e8984…`), so this is recorded,
not edited.
