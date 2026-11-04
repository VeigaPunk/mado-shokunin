# R74ExecC2 — independent frozen C2 replay

## Axes and disposition
Operability: reproduce the frozen census and 36 controls. Calibration: distinguish actual reproduction from stronger dominance-coverage claims. No-harm: read-only lane inspection, no production edits, no host changes. Measured result: TARGET_MET; the eight appended controls do not independently isolate every new dominance restriction.

## Executed commands and receipts
Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
python3 -I quality/counters/c2-r74-shapes.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root /fast/scratch/hyaku/mado-r74/R74ExecC2/run
python3 -I quality/counters/c2-r74-shapes.py --selftest --controls .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root /fast/scratch/hyaku/mado-r74/R74ExecC2/run
```

Counting rc: **0**; stderr: empty. Exact last line:

```text
MADO_R74_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=36/36 base_controls=32/36 verdict=TARGET_MET rev=b73db773aaf67c9b26c8cf1a4cd567dec3af11f4
```

The entire captured stdout is byte-identical to `.ufo/waves/round-74/measurement-c2-r74.txt`; last-line differences: none; stdout differences: none; rc difference versus the declared committed rc 0: none. The text receipt itself does not encode a process rc; the replay independently captured it.

Selftest rc: **0**; stderr: empty; stdout:

```text
MADO_R74_GUARD_SHAPES_SELFTEST: 86/86 assertions passed
```

Retained sibling evidence files: `counting.stdout.txt`, `counting.stderr.txt`, `counting.rc.txt`, `selftest.stdout.txt`, `selftest.stderr.txt`, `selftest.rc.txt`, `comparison.json`, `population.json`. `comparison.json` records `stdout_equal=true`, `differences=[]`, and `stderr_bytes=0`.

The committed C1 summary and pre-freeze baseline were also re-read, not changed: C1 reports 12/12 versus base 8/12; baseline C2 reports 32/36 and names the same four misses below. No C1 command was rerun by this seat.

## Exactly four held-classifier misses
The replay contains exactly these `leg=base ... correct=no` cases; all are reader=yes, guard=no, expected guard=yes:

| Case | One-based position among 36 | Appended? |
|---|---:|---|
| `twohop-attr-store-dotted-call` | 29 | Yes |
| `twohop-attr-store-alias-call` | 30 | Yes |
| `environ-alias-call-guard` | 31 | Yes |
| `environ-alias-splat-guard` | 32 | Yes |

Cases 29–36 are the eight appended cases (`controls/c2-cases-r74.json:173–220`); the four appended negatives are positions 33–36. Candidate classifies all 36 correctly, held base classifies 32 correctly.

## Alias implementation and dominance bounds
Read `object_alias_map` (1042–1056), `canonical_dotted` (1059–1066), `twohop_guard` (1069–1115), `environ_alias_names` (1118–1131), and `environ_alias_guard` (1146–1195), plus `copies_alias` (1134–1143), in `quality/counters/c2-r74-shapes.py`.

- `twohop-attr-store-dotted-call`: a single-assignment `r = cfg.runner` lets the earlier `r.env[KEY]` store canonicalize to the launch's `cfg.runner.env`, requiring store line < call line and no intervening assignment to that canonical path.
- `twohop-attr-store-alias-call`: the same single-assignment canonicalization works in reverse, joining an earlier `cfg.runner.env[KEY]` store to `env=r.env`, under the identical ordering/replacement restrictions.
- `environ-alias-call-guard`: a name assigned once to `os.environ`, with a prior guard-key store and no intervening key deletion, reaches the launch through exactly `dict(env)`.
- `environ-alias-splat-guard`: the same alias/store/order/deletion bounds reach the launch through exactly `{**env}`.

### Which negatives protect which bounds?
The intended analogues are `twohop-attr-store-after-call` for strict store-before-launch, `twohop-attr-store-replaced` for intervening replacement, `environ-alias-no-store` for requiring a guard-key store, and `environ-alias-rebound` for excluding rebound environment aliases. However, claiming that each independently kills removal of the corresponding **new-carrier** restriction would overstate the evidence:

1. Both twohop negatives store and launch at the same spelling `r.env`. In `twohop_guard`, neither side crosses the alias edge, so `if not (crossed_call or crossed_store): continue` rejects them regardless of its later ordering/replacement checks. [INFERENCE from source] Dropping only either new-carrier dominance check therefore does not make its corresponding frozen negative pass; their observed rejection can be furnished by held attribute logic instead.
2. `environ-alias-no-store` directly exercises absence of a store, not temporal dominance. [INFERENCE from source] Removing the store-presence requirement wholesale and crediting an alias binding alone would break this negative; removing only the early `if not stores` return still leaves an empty store loop and does not.
3. `environ-alias-rebound` contains **no guard-key store**, in addition to rebinding. [INFERENCE from source] Removing only the exactly-once assignment filter still leaves no stores, so this negative remains rejected; alias-only credit without the store requirement would break it, but a rebound-after-valid-store fixture is absent from the appended eight.
4. Neither appended environment negative isolates store-after-launch or intervening deletion. No one-to-one claim that all four positives have a uniquely bound-sensitive new negative is supported by these eight fixtures. No mutation experiment was run; these restriction-removal statements are source deductions, not observed mutant results.

The code's restrictions exist; the measured 36/36 result reproduces; the stronger assertion that these four negatives individually enforce every new restriction does not follow.

## Independent population census
Executed independently:

```sh
git ls-tree -r --name-only b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 -- quality
```

Filtered the returned paths with `^quality/check-[^/]+\.py$`: **20 files**, not 20 readers. Each matching file was separately read using `git show REV:path` and classified using the counter source independently extracted from the same frozen revision: **13 readers, 13 guarded, 0 unguarded**. Exact commands, filter, counts and all 20 per-file classifications are retained in `population.json`. This independently enumerates the population and replays the frozen classifier; it is not a second semantic guard implementation.

## Limits, safety and handoff
No production, corpus, global configuration, credential, service or sibling files were written. No git/jj mutation, installation, dispatch, broad verification or mutation testing occurred. LSP definition/reference tools were unavailable in this seat's exposed tool inventory; source navigation used text search and bounded reads rather than claiming an empty LSP result. Only this seat's evidence/report directory and assigned scratch were written; scratch was removed after evidence retention.

The report uses the explicit exclusive seat-directory path; the later flat report-path sentence conflicts with that hard write boundary and was not followed. No implementation changes are proposed. Parent may use the reproduced receipts for C2's finite target, while retaining the dominance-control coverage caveat. Declared source limits remain line-order rather than execution-order analysis, one alias edge, and syntactic rather than value interpretation.

Self-evaluation (accuracy/completeness/clarity/actionability/conciseness): 4/5 each, average 4.0. Concrete limitation: restriction-removal effects are source deductions, not a mutation run; the negative-coverage qualification adds necessary length. User-facing improvement: use the retained counts without upgrading them to comprehensive dominance coverage.
