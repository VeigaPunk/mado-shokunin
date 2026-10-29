# Round 56 — frozen claims v2 (pre-data re-registration; `claims-frozen.md` is untouched)

Supersedes the predicate sentences of `claims-frozen.md` for C1 (control count), C2 (control count) and C3 (definition and
control count) as `registration-v2.md` states, with its change table E1-E11 and its disclosure of five v1 defects found by wave 1
before any real data. Everything not restated here stands as in `claims-frozen.md`. `frozen-tables-v2.json` sha256
`9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2`; `c3-name-only.tsv` sha256
`70653e095839dc82f248d77fa5a0117134406a8b9e23778d2d79bf7072c948ee`. Counters and harnesses embed the tables sha above.
The claims, axes and kill rules are those of `claims-frozen.md`; a falsified v2 predicate is an honest stop.

## C1 — coverage (sourced entry) — PRED-C1-r56-v2

Counter line (sentence unchanged): `MADO_AUTORELOAD_ENTRY: rev=<rev> rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`, exit 0
(`python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev <rev> --work <scratch>`), AND
`python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev <rev> --work <scratch>` prints
`MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK`, exit 0. Legs: registration.md §C1 + registration-v2 E2, E3, E4, E5.

## C2 — operability (capability acquisition) — PRED-C2-r56-v2

`python3 -I quality/check-r56-controls.py --claim c2 --repo . --rev <rev> --work <scratch>` stages and runs the tool on the 18 committed
and the 8 revealed hold-out fixtures as registration-v2 E6 defines, and prints
`MADO_R56_C2: rev=<rev> fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`, exit 0. Controls (registration-v2 E7):
`ctl/const-host.py` passes at most 1 of the 26; `ctl/empty.py` passes 0; `ctl/sibling-reader.py` passes 0 (staged layout);
`ctl/lookup-committed.py` passes 18/18 committed and 0/8 hold-out.

## C3 — calibration (registry back-reference consistency, token level, reviewed) — PRED-C3-r56-v2

`python3 -I quality/counters/c3-r56-used-by.py --repo . --rev <rev> --work <scratch>` prints
`MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none`, exit 0,
AND `python3 -I quality/check-r56-controls.py --claim c3 --repo . --rev <rev> --work <scratch>` prints
`MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK`, exit 0. Definitions: registration-v2 §C3-v2.
Before (base, `receipts/c3-base-v2.txt`): `entries=70 rows=319 missing=41 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24` (v1 token count 65; 24 name-only pairs exempt by the frozen allowlist).
Target: the sentence at the final content revision, with `used-by` edits only (cell 11), old→new logged in the lesson, and no change to any entry text. Do-nothing control:
the unchanged registry (41 missing), allow-everything (allow_sha), deleting citations (lost), filling everything (extra).
Report wording: "registry back-reference consistency (token level, 24 reviewed name-only exemptions)", not "calibration of confidence".

## Mistake-fix and exploratory items

M56-1 scope leg (anchor must cover the quoted line) stands, now also bounded by the pin's line count (E3). No exploratory claim.
