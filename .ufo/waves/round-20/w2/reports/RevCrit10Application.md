# RevCrit10Application — holds: all 5 red and 4 green tally entries point at the exact sentence, counting rule and revision they claim; one runbook defect (the QUALITY paragraph's bare command exits 2)

Seat: wave-2 FALSIFY, round 20. Item: does every red/green entry in
`.ufo/waves/round-20/tally-claims.json` and the "Round-20 application of criterion 10"
paragraph in `corpus/QUALITY.md:261-271` point at the exact sentence, rule and revision it
claims. All runs below are in my own clone `/tmp/mado-r20w2-RevCrit10Application`
(cloned at tip `a4046a8216080d4004de3f268c62cf142095ac07`, origin removed). Registry
sha256 `81eed3eb…74b3a48d`, checker sha256 `21ce9dd5…fd2aea4` — both equal to
`git show a4046a8:…` bytes; lane worktree clean for QUALITY.md, tally-claims.json,
tally-check.py.

## Checker executions (the item's named command, run)

- `--set red --expect` → 5/5 MISMATCH, `EXPECT_SUMMARY: 5/5`, exit 0.
- `--set green --rev a4046a8…` → 4/4 MATCH, exit 0.
- `--set all --rev a4046a8… --expect` → 9/9 on side, exit 0.
- Statement locations resolved: lesson round-19 **:124**, SCORECARD **:1167**, lesson
  round-19 **:108**, LOG **:1324**, SCORECARD **:1225** (all at `1f7f995caa25627db804e996cccd87fe38a3a1b6`);
  greens at round-20.md **:70, :62, :62, :74** at `a4046a8…` — exactly the line numbers the
  QUALITY paragraph cites.

## Sentence fidelity (red, pinned 1f7f995)

- `corpus/lessons/round-19.md:124` = "155 round-19 transcripts, `--permit tool_install`): …"
  inside the post-wave seat-scan paragraph that names `evidence/final/tripwire-seat-scan.txt`
  and tool `367be947…`. Derive reads that same receipt: files=**154**, distinct_paths=154,
  jsonl_paths=154, header tool_sha256 `367be94773d8…`, measured_commit `0fa412525f…` — the
  note's facts hold, and the sentence's other numbers (host_mutation 0, live_probe 3,
  vcs_write 164) match the receipt's `counts=` line, so the entry binds the right artifact.
  Receipt blob `5982e233ddc2ed08` identical at `c7693eb`, `1f7f995`, `a4046a8` ("unchanged
  since c7693eb" holds).
- `SCORECARD.md:1167` = 'read as "13/13 pointed; 5/13 name S096 on the crediting line; …"';
  `corpus/lessons/round-19.md:108` = "C2 sourcing: 5 of 13 credited files name S096 on the
  crediting line"; `LOG.md:1324` = "`fresh-pins.py` 2/13 → 13/13 (5/13 name S096 on the
  crediting line; …". Derive (`pointer-token`, counter `fresh-pins.py@1f7f995`, AST-parsed,
  `in_scope` AST-identity enforced by the checker): PIN_REV `9c54c56…`, OLD `2.17.0`,
  denominator 13, current 13/13 (the sentences' "13/13 pointed" clause is true), first_line
  **6/13**, any_line **8/13**; exactly the five named files (arc-synthesis:392,
  closeout-r11:299, config-health-report-r3:1009, waybar-walker-plane:479,
  waybar-walker-semantics:467) carry no S096 on any pointer line, and each carries S090 on
  its first pointer line (`--token S090` → first_has_token=yes for all five), matching the
  lesson's "cite S090 only". The 5→6/8 MISMATCH is robust: it does not depend on the
  contested first-line vs any-line rule choice (5 differs from both).
- `SCORECARD.md:1225` = "the ten old OM10 assertions were replaced by OM10A/B" (its context
  line 1223 names `7b4839d`/`d642ce5`). Derive (`selftest-labels` old `9c54c56…` new
  `7b4839d…`): occurrences 390 (distinct 370) → 461 (440) as the note says; removed
  **9** occurrences / **8** distinct, all id OM10 (`removed_other_id_occurrences=0`),
  including the twice-occurring "OM10: the UNKNOWN names the rc" (old lines 841,842);
  added OM10A:6 + OM10B:8 — every micro-fact in the note checks. A raw `git diff
  9c54c56 7b4839d -- tools/mado-verify.sh | grep '^-' | grep -c OM10` = **10**, confirming
  the note's account of where the stale "ten" came from (the `# --- OM10:` banner line).

## Sentence fidelity (green, REV = a4046a8)

All four are real round-20 correction sentences matching exactly one line each, numbers =
derived: ":70 lists **154** files (not 155)"; ":62 S096 is **8/13 on any matching line** and
**6/13 on the first matching line**" (both greens resolve to this line via disjoint regexes);
":74 OM10 at `9c54c56` had **nine labeled assertion occurrences, eight distinct** (not ten),
replaced by OM10A six and OM10B eight". Each green's derive re-uses the red's counting rule
(pinned 40-hex everywhere) and MATCHes.

## Paragraph claims beyond the entries

- "the 5 was RerunC2's cited-as-evidence reading at `01b8094`" — exact:
  `.ufo/waves/round-19/w2/reports/RerunC2.md:71` "Tally: S096 cited as evidence **5/13**",
  with the run performed on bytes extracted via `git show 01b8094:…` (RerunC2.md:12-31); its
  own split (S090-only 5/13, S091-only 1/13) independently corroborates 8/13 any-line.
- Withdrawal: `SCORECARD.md:1285-1297` ("Round-20 pre-measurement corrections") records
  registered criterion 30 withdrawn as a restatement of criterion 10, citing
  `corpus/QUALITY.md:16`, which is indeed criterion 10's "rederive it from the named
  revision" text; replacement 30′ = today's QUALITY criterion 30 (precision). "append-only,
  no new number" matches.
- R19-V2/V4/V5 mapping matches `corpus/lessons/round-19-verifier-spotcheck.md:150,152,153`
  (V2 prescribes exactly 8/13 any-line + 6/13 first-line; V4 155→154; V5 ten→nine).
- Declared limit is honest: at `a4046a8` the stale sentences remain in place
  (SCORECARD:1167, LOG:1324) and the registry does not flag them — as the paragraph states.

## Findings

- **F1 (minor, runbook defect — QUALITY.md:263, L1's to fix).** The paragraph's quoted
  command `python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json`
  (no `--set`, no `--rev`) **exits 2 with 4 ERRORs** ("entry reads at REV; pass --rev"):
  green entries structurally require `--rev`, so the command as registered can never pass.
  Passing forms: `--set red --expect` (exit 0), `--set green --rev a4046a8…` (exit 0),
  `--set all --rev a4046a8… --expect` (EXPECT_SUMMARY 9/9, exit 0). Contrast criterion 30's
  own runnable check, which writes its placeholder (`tw-precision.py REV`); this paragraph
  should name the set/rev form. No entry is wrong — only the registered invocation.
- **F2 (info, doc/impl mismatch).** `tally-claims.json` entry_semantics says a fraction's
  two groups have "only '/' or 'of'" between them; the checker's CONNECTOR also accepts
  "out of" (`tally-check.py:747` `\s+(?:out\s+)?of\s+`). No entry uses it; harmless
  permissiveness, but the JSON's semantics text is narrower than the enforcement.

## Limits

- I verified the derives as implemented and their faithfulness to each note (constants
  AST-re-derived by the checker, per-file rows read, subcommand outputs cross-checked); I
  did not write a third independent counter. The pointer-token rule choice (first matching
  pointer line = "the crediting line") is a judgment, but the red MISMATCH survives either
  candidate rule.
- Out of scope, not run: other stale round-19 counts outside the registry (paragraph
  declares that limit; whole-corpus diff is another seat), and the C2 `measure.py` key c1
  rerun (RerunMeasure's item).
- All checks were read-only git in the clone; no lane writes, no VCS experiments.

## Installs

none
