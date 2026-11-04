# R77RevClaims — review of the two frozen round-77 claims (wave w1)

Date 2026-11-04. Method: blob-exact re-derivation at the freeze rev `a83e9bee` — both counters
run from `git cat-file` bytes (counter blobs `ae5d27e7` = sha256 `56620959…`, `57383fc7` =
sha256 `056a9152…`), tool extracted by the counter at `--rev a83e9bee` (blob `41f3341f`, file
sha256 `409e78a4…`), controls at `7d6e2b1a…` / `597b2302…`. Receipts were not trusted; every
receipt line quoted below was reproduced by execution or read from committed bytes.
Labels: **[R]** re-executed this round, **[V]** evidence-verified from committed bytes (QUALITY 131).

## Verdict table

| claim | predicate | re-derived | agree/disagree | defect class |
|---|---|---|---|---|
| C1 counting clause | `MADO_R77_BARFOOT: cases=15 correct=15 mutants=5 killed=5 base_correct=8/15 tool_selftest=18/18 verdict=TARGET_MET rev=<hash>`, rc 0 | Blob-exact rerun rc 0; line matches the declaration's after-state sentence word for word, plus the Freeze-sanctioned extra `tool_sha256=409e78a4…` field [R] | agree | none at the pinned rev |
| C1 base clause | naive live-echo control prints `correct=8/15`, 8 < 15 | `MADO_R77_BASE: correct=8/15` printed; independent reimplementation of the control rule against the frozen JSON scores 8/15 with misses exactly {css-margins, drift-box, drift-reserved, malformed-layers, output-excluded, per-side-margin, wrong-edge-band} — the seven the declaration names [R] | agree | none |
| C1 case tuples | counter compares rc/box/reserved/verdict against each frozen expect | All 15 expects are exactly the quadruple `expected_ok` compares; 14 use the verdict path, `malformed-layers` alone uses the error path (`{"error": true, "rc": 2, "stage": "setup"}` → rc==2 and `ERROR (stage=setup` in stdout); 15 unique names; version `r77-v1` [V] | agree | none |
| C1 mutant anchors | 5 named anchors are semantic rules, not comments | Each anchor occurs exactly once in the frozen tool source and is a rule line: `LEVEL` dict, `if not bar["exclusive"]:`, `if bar["width"] > 1:`, `RESERVED_INDEX` dict, per-side margin assignment [V]; all 5 mutants killed 5/5 in the rerun [R] | agree | blemish (F3): `reserved-wrong-edge`'s replacement carries a stray trailing comma |
| C2 counting clause | `MADO_R77_RUNBOOK: cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12 verdict=TARGET_MET`, rc 0; base `executed=0 matched_by_read=12/12` | Blob-exact rerun rc 0 with exactly that line and base line; probes ran live in this session [R] | agree | frozen matcher is rc-blind (F2) |
| C2 anchors | each `skill_anchor` occurs in committed SKILL.md at the measured rev | 12/12 present at `a83e9bee:SKILL.md`, all inside the probe-table region (lines 204–227 of that rev); 9 distinct anchors for 12 cases [V] | agree | `omarchy-version` anchor under-names its command; printed `anchors=` is tautological (F4) |
| Live evidence | `fetch/live-*.json` sha256s cited in `receipts/pre-wave-evidence-r77.txt`; no unlabelled number | `live-layers-r77.json` = `46eb2481…`, `live-monitors-r77.json` = `e732af34…`, both cited verbatim in the receipt (grep hits 2) [V]; frozen tool re-run on those committed captures plus the host config reproduces the receipt's CONFIG/DECL/LIVE/RESULT/verdict lines exactly, rc 0 [R]; every number in both receipts is field-labelled, the gate line is labelled `MADO_SELFTEST: 460/460` [V] | agree | none |

Freeze chain checked [V]: `aeeef067` (base) is an ancestor of `a83e9bee`; `e4717a1c → a83e9bee`
diff is counter-only (+3/−2, the absolute-repo fix); tool blob identical at `e4717a1c` and
`a83e9bee`; both control sets untouched after the freeze (no commits); `make-cases-r77.py`
committed at the freeze (blob `f5a9d528`).

## Findings by severity

**F1 — Medium — post-freeze instrument drift (moving target).** The seat brief names three
instruments and the declaration as frozen, yet post-freeze commits rewrote them while this wave
ran: `tools/mado-barfoot.py` in `0fa69f41`, `bbca7469`, `2df46e29`, `9197405c`; the C1 counter in
`de627316` (mutant oracle); the C2 counter in `4a17b31f` (env discovery) and `bce906f3`
(matcher requires exit 0); the declaration itself in `de627316`, `e177c79b`, `9197405c`;
`corpus/lessons/round-77.md` did not exist at the freeze rev. HEAD moved during this review
(`8b7ef027` → `ee62bd7f`); at review time the frozen shas no longer name HEAD bytes. Not
falsification: each repair carries a red/green receipt and lesson/QUALITY entries, and the final
measurement commit `ee62bd7f` re-pins its measurement to `bce906f3`. But the frozen-instrument
story ("committed at the freeze commit, never rewritten") no longer describes HEAD; every
re-derivation must pin a rev, as this review and the receipts do.

**F2 — Low — frozen C2 matcher ignores rc and stderr for every expectation kind.** At
`57383fc7`, `matched()` inspects stdout only: (a) `configerrors` (kind `empty`) still matches if
`hyprctl` is absent or broken — the shell writes its diagnostic to stderr and exits 127 with
empty stdout, so a wrong state passes; (b) `version` (kind `contains`, `Hyprland 0.56.2`) also
matches `0.56.20`/`0.56.21` (prefix substring). `waybar-process`'s any-pid regex is a declared
shape-only limit, not a defect. Dispositioned post-freeze: `bce906f3` lands "C2 matcher requires
exit 0 (red/green)" plus QUALITY 135 naming the frozen-set gaps.

**F3 — Low — `reserved-wrong-edge` mutant kills partly by crash, not by wrong-edge semantics.**
Its replacement ends in a stray comma, so `RESERVED_INDEX` becomes a tuple and every case
reaching the reserved read dies with `TypeError: tuple indices must be integers or slices, not
str` (rc 1, no verdict) — demonstrated on the `host-top` fixture: mutated-with-comma rc 1
traceback; the same swap without the comma rc 1 `verdict=DIFFER`, i.e. the semantic kill also
stands [R]. Kill counts are unaffected. Dispositioned post-freeze: `de627316` replaces this
mutant with an oracle-based one.

**F4 — Info — C2 anchor bookkeeping.** The pre-loop gate aborts (Setup) if any anchor is
missing, so the printed `anchors=12/12` can never be lower — it is not an independent
measurement. `omarchy-version` anchors to `` `omarchy theme current` `` while its frozen argv
runs `omarchy version`; the bound row (line 215 at that rev) covers both commands and states
both samples, so the binding is right but the anchor under-names the executed command.
Nine distinct rows carry the twelve cases (three shared anchors).

## Residual risk and verification gaps

- This review pins `a83e9bee`; the post-repair instruments at `bce906f3`/`ee62bd7f` carry their
  own measurement receipt, which I did not re-derive (outside the frozen-claim scope).
- C2 is a point-in-time run on a live host: `monitors-size`, `monitors-reserved`, `binds-count`
  can drift after this session (declared limit); the version/configerrors/binds rows re-verified
  green during this review's rerun only.
- I checked existence and labelling of the declaration's cited sources (S457–S462 fetch files
  present at HEAD), not their content against the pinned upstream trees.
- Scratch `/fast/scratch/hyaku/mado-r77/R77RevClaims/` removed after writing this file; no host
  state written; read-only git and read-only probes only.
