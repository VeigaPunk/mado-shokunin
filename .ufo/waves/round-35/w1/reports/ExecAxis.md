# ExecAxis — calibration gate at tip

Scoped finding: `quality/check-axis-scores.py` run read-only at the current tip, plus its
`--selftest`. Gate is a pure read path — every check goes through `git show`/`git` plumbing and
committed script bytes run in a tempdir; nothing in the tree is mutated.

## Tip under test

- `ba507b2bb8c0ea69e411ddf19a12044fa6237e61` (jj `@`; git HEAD `19e4ab31...` has an identical
  tree — `git diff` between them is empty, so results are revision-equivalent).

## Gate output

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py \
    --rev ba507b2bb8c0ea69e411ddf19a12044fa6237e61 \
    --repo /home/vgpnk/Projects/shokunin/mado-shokunin
MADO_AXIS_ROW: axis=navigation published=47/47 derived=47/47 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/41 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=ba507b2bb8c0ea69e411ddf19a12044fa6237e61
exit=0
```

## Selftest output

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py --selftest
PASS parse-navigation
PASS parse-calibration
PASS parse-operability
PASS ignore-sourced-art
PASS stale-detected
PASS stale-rows
PASS nonzero-on-stale
PASS clean-is-zero
PASS clean-rows
PASS missing-publication-is-not-a-pass
PASS missing-instrument-is-not-a-pass
PASS one-perturbation-bites
PASS no-publication
PASS quoted-marker-does-not-shadow
PASS quoted-marker-keeps-operability
PASS long-publication-not-truncated
PASS navigation-perturbation-bites
PASS operability-perturbation-bites
MADO_AXIS_SELFTEST: 18/18 assertions passed
exit=0
```

## Axes the gate re-derives (frozen set, per script docstring lines 11-14)

| axis | instrument at `<rev>` | derived cell |
|---|---|---|
| navigation | `quality/check-index.py --rev <rev> --repo .` | `indexed=A/B` |
| calibration | `.ufo/waves/round-31/c2/count.py <rev>` | `resolved_active/active` |
| operability | `quality/check-index.py --selftest` | `A/B assertions passed` |

Comparison rule: the LAST unquoted "Axis table re-derived at …" line in `SCORECARD.md` is the live
publication; each published fraction must equal the re-derived fraction. Missing publication,
missing instrument, or unparsable cell counts as a mismatch, not a pass.

## In-step verdict

Yes — the published table is in step with the repo. Live publication is SCORECARD.md:2110
("Axis table re-derived at the round-34 data tree (criterion 22): navigation 47/47; calibration
resolved-active 41/41; operability selftest 12/12"). All three fractions re-derive identically at
tip; gate exits 0 with 0 mismatches.

Caveat: the publication's prose tag still names the round-34 data tree while the working tree now
carries round-35 material (`fetch/` receipts, `c1/`, `c2/` counters). The numbers stay in step, but
the annotation is one round behind; a subsequent index addition or scorecard entry will flip
navigation or calibration red until the line is re-published.
