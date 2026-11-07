# R96MExecCounterC2 - round 96 w1 report (C2 counter + r90-argv control)

Seat: executor, C2 lane. Base revision `9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d`. Predicate implemented
exactly: **PRED-C2-r96-v1**, verbatim in the counter docstring; no sentence widened, no leg dropped.

## Deliverables

| file | sha256 | state |
|---|---|---|
| `.ufo/waves/round-96/quality-counters-c2-r96-selftest-kills.py` | `2bd9e5628993ceccf2739d0782a9cef7ff9ed5c6247336f5f3d07188eb4eb895` | final draft; L1 copies to `quality/counters/c2-r96-selftest-kills.py` |
| `.ufo/waves/round-96/controls/r90-c2-argv-r96.json` | `386a5a18f77bf6fa564f2a11498ef21f5c1e7ef461028a2956050d3af52ecda0` | final |
| `.ufo/waves/round-96/w1/R96MExecCounterC2.md` | - | this report |

(sha256 taken from the final bytes; the two robustness guards added after the first battery are inert for
well-formed kill-set/panel JSON, and the closing run below was executed against exactly these bytes.)

argv (all required unless noted): `--repo --rev --panel --expect-panel-sha256 --expect-gate-sha256
--expect-kills-sha256 --control-kills --expect-control-sha256 --r90-argv --expect-r90-argv-sha256
--scratch-root`, optional `--timeout 120 --workers 8`, and DRAFT-only `--draft-tool --draft-kills`
(either present -> draft mode: tool/kill-set bytes come from files instead of `<rev>`, verdict prefixed
`DRAFT_`, rc 3; the gate and the r90 counter are still materialised from `<rev>` and still sha-pinned).
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT. stdlib only; ASCII only; writes only under
`--scratch-root`; subprocess is used solely to drive the gate, the tool `--selftest` and the r90 counter,
exactly like the round-95 counter this adapts (QUALITY 162/165 bind the C1 candidate, not this driver;
the pattern is the committed round-95 precedent).

## Predicate -> implementation map

- pins: gate sha (`--expect-gate-sha256`), kill-set sha (`--expect-kills-sha256`), and `tool_pin` =
  kill-set `tool_sha256` == sha256 of `quality/check-receipt-presence.py` at `<rev>` (or `--draft-tool`).
- (i) `positive=VERDICT:rc` from the frozen gate on the unmodified tool WITHOUT `--allow-sha-drift`
  (must be `OK:0`), plus the tool's own `--selftest` result line parsed as `checks=6 failed=0` and the
  six labels derived from the selftest source (`^[ \t]+\("LABEL", ` over the `def selftest(` body,
  unique in order) and required == {OK-rc, OK-lines, MISSING-rc, MISSING-lines, SETUP-rc, SETUP-lines}.
- (ii) neutralisation: the tool's single `    failed = [n for n, ok in checks if not ok]` line is
  rewritten per label to `... and n != '<label>'`; each variant must stay green (rc 0, identical result
  line) and the gate must print `WEAK:1`; `neutralised_flagged=6/6`.
- (iii)/(iv) the panel (JSON list of `{id, kind: hand|neutral, find, replace, why}`; `{hand,neutral}`
  dict also accepted; optional `all` tolerated): every entry applied to the tool text (`find` exactly
  once), greenness enforced for all, `hand_flagged=h/H` (all WEAK:1), `neutral_ok=z/Z` (all OK:0),
  `len(neutral) >= 4` enforced; the hand minimum (>=30) is NOT enforced in code - it is the frozen
  panel's property, visible as `H` in the result line (same choice as the round-95 counter).
- (v) controls: `do_nothing_flagged` counts weak variants whose selftest result line changes (0 by
  construction because greenness is enforced - the do-nothing instrument is blind, as declared);
  `always_ok_flagged` must be 0 over the hand variants; `always_weak_positive` must not be `OK:0` on the
  unmodified tool; `control_hand_flagged=c/H` from `--control-kills` (sha-pinned) must satisfy `c < H`.
- (vi) `singleton_labels=s/6` (a kill whose `must_fail` is the label or a one-element list) must be 6/6;
  `labels_covered` printed alongside as telemetry.
- (vii) `gate_selftest=ok` (rc 0 of `python3 -I gate --selftest`).
- (viii) the r90 leg (below).

## r90-c2-argv-r96.json: provenance and replay semantics

Content = the frozen measurement argv of `quality/counters/c2-r90-receipt-presence.py`
(`.ufo/waves/round-90/claims-declaration-r90.md` "Measurement argv"; frozen TARGET_MET run recorded in
`.ufo/waves/round-90/receipts/c2-measured-r90.txt`; the DRAFT run in `c2-controls-prefreeze-r90.txt` has
the same shape plus `--draft-check`, which MUST NOT be replayed - it would score the r90 draft bytes and
print DRAFT_TARGET_MET). Placeholders: `@REV@` -> the C2 counter's `--rev`; `@BASE_REV@` -> the JSON's
`base_rev` field = `5041acf99e27263872bf0441ad5f9d4316152605`; `@SCRATCH@` -> a fresh scratch dir. The
counter materialises the r90 counter FROM `<rev>`, runs it with cwd = the repo (so `--repo .` and the
relative `--set/--mutants` paths resolve), and requires exit 0 plus a non-draft
`MADO_RECEIPT_PRESENCE: TARGET_MET` line.

`--base-rev` is pinned to the round-90 base and NOT substituted with the measured rev: at any post-r91
rev the tool exists and meets all 83 expectations, so the r90 counter's own base control
(`all(v < n for v in controls.values())`) would fail and the leg would be TARGET_MISSED by construction.
Every tip replay since round-91 pins exactly this sha: harm-final-r91.txt:75, -r92.txt:35, -r93.txt:83,
-r94.txt:86, -r95.txt:89. The set/mutants shas are unchanged frozen r90 inputs.

### Leg proof at the round-95 tip (pre-C2-change; the non-tautology control)

Run in scratch, counter materialised from `9f029f46...`, exit code 0:

```
MADO_RECEIPT_PRESENCE: TARGET_MET rev=9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d expectations=83 met=83 defects_detected=4/4 population=38 mutants=28 killed=28 base_check=absent base_met=0 do_nothing_met=44 smart_always_ok_met=46 always_missing_met=0 check_sha256=38a2ea60dc698c45957a3ad4af3132297dd2edb354d815e7ff3433c42bab47ca
```

`check_sha256=38a2ea60...` = the tool bytes at the round-95 tip (unchanged since the r91 D1 commit), so
the leg exercises real bytes and real commits (38-commit population, 28 mutants) - it can fail, and it
is the same command the freeze replay substitutes `@REV@` into.

## Validation of the counter (draft mode, wave bytes)

Wave artifacts used as shipped by the siblings:
`build/check-receipt-presence.c2.py` sha `be716a63662f326a771d96dc5324e89fe07abdff6949029cabb8b7f5d15ca962`
(selftest block after `main()`, needle at :322, selftest green `checks=6 failed=0`);
`build/check-receipt-presence.kills.json` sha `305d735fd665ad87566c7983f4e9163eaf323ad1ddb7a99a907e507c8a617495`
(7 kills, `tool_sha256` = draft sha; re-encoded to list `must_fail` after my first cross-check - same
seven kills and label sets, sha `aa2a4764...` was the earlier encoding);
`build/check-receipt-presence-draft.kills.json` sha `0c233a47b9d0b855ed92991079399c1e6cf32848d4016081057c569ea3aed0c7`
(3-kill subset control, gate-OK on the clean tool - see Finding F2).
Panel: `controls/selftest-panel-r96.json` sha `4332b488309309b81eccccabaff9322c5b7a54fcedd74079b58f50926f773982`
(37 entries: 31 hand + 6 neutral, the declared list-of-{id,kind,find,replace,why} schema) - the closing
rehearsal below runs the REAL panel; my earlier mechanics runs used a scratch-provisional 4+4 panel.

Independent cross-check of the frozen kill-set (my own measurements, real gate, done on the earlier
string-form encoding `aa2a4764...`; the re-pinned list-form `305d735f...` carries the same seven kills
and label sets, and the closing rehearsal's positive leg re-proves all seven held): every `find` occurs
exactly once in the gate's mutable prefix, and each measured must_fail set agrees with the declared one
(ok-rc-exit-polarity->[OK-rc], ok-lines-verdict-polarity->[OK-lines], missing-rc-exit-2->[MISSING-rc],
missing-lines-off-by-one->[MISSING-lines], setup-rc-exit-0->[SETUP-rc],
setup-lines-marker-drift->[SETUP-lines], cited-count-double->[OK-lines]); 6/6 singleton labels covered.

Closing rehearsal, draft mode, `--rev 9f029f46...`, counter bytes `2bd9e562...`, REAL wave inputs (the
shipped panel 31 hand + 6 neutral, the shipped kill-set, the shipped control; only the tool/kill-set
bytes come from files instead of `<rev>`, which is the sole difference of the frozen run):

```
probe pos OK:0; probe 1..6 N:<each label> WEAK:1; probe 7..37 W:<31 hand ids> WEAK:1;
probe 38..43 Z:<6 neutral ids> OK:0
MADO_SELFTEST_KILLS: DRAFT_TARGET_MET pred=PRED-C2-r96-v1 rev=draft gate_pin=ok kills_pin=ok tool_pin=ok checks=6 labels=6/6 labels_covered=6/6 singleton_labels=6/6 positive=OK:0 neutralised_flagged=6/6 hand_flagged=31/31 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1 gate_selftest=ok control_hand_flagged=19/31 r90_leg=TARGET_MET r90_met=83/83 r90_killed=28/28 r90_check_sha256=38a2ea60dc698c45957a3ad4af3132297dd2edb354d815e7ff3433c42bab47ca tool_path=quality/check-receipt-presence.py kill_path=quality/selftest-kills/check-receipt-presence.json gate_sha256=2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b kills_sha256=305d735fd665ad87566c7983f4e9163eaf323ad1ddb7a99a907e507c8a617495 tool_sha256=be716a63662f326a771d96dc5324e89fe07abdff6949029cabb8b7f5d15ca962 control_sha256=0c233a47b9d0b855ed92991079399c1e6cf32848d4016081057c569ea3aed0c7
rc=3
```

R96MMutC2 independently measured the same panel against the same kill-set with the real gate (31/31
WEAK, 6/6 OK, every variant green with a byte-equal result line) - my rehearsal agrees probe for probe.
They deliberately shipped 31 hand entries: 7 further green weakenings are gate-blind against the landed
7-kill set (surfacable only with 4 extra kills, 38/38); the frozen sentence needs >=30, so 31/31 is the
correct shipped shape either way.

SETUP paths, re-run on the final counter bytes, both rc 2 as designed:

```
MADO_SELFTEST_KILLS: SETUP_ERROR pred=PRED-C2-r96-v1 absent at 9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d: quality/selftest-kills/check-receipt-presence.json (kill-set path pinned as quality/selftest-kills/check-receipt-presence.json)
MADO_SELFTEST_KILLS: SETUP_ERROR pred=PRED-C2-r96-v1 panel sha256 7a08f07e... != pinned
```

The first is the declared "before": frozen mode at the base revision stops SETUP_ERROR because the lane
holds neither the kill-set nor the changed tool there.

## Findings for the L1

- **F1 (resolved, dependency recorded): predicate leg (vi) needs the selftest-after-main layout.** In
  the base layout (`def selftest(` before `def main(`) the gate's `non_selftest_prefix()` makes main()
  unmutable, and within each arm the -rc and -lines checks read the same run (rc!=0 requires
  missing>=1 or a SETUP_ERROR, both of which change the printed lines), so singleton kills for the -rc
  labels are structurally impossible - R96MMutC2 independently measured the same reachable sets
  pre-move. The L1's amendment (whole selftest block moved to EOF, `if __name__` guard after it) puts
  main()/setup() into the mutable prefix and makes all six singletons reachable (exit-polarity and
  marker-drift mutants flip a check while leaving the printed lines byte-identical). My counter
  implements (vi) as written (singles==6 gates met). If the frozen tool ever reverts the move, (vi)
  goes red BY DESIGN - that is the honest reading of the frozen sentence, not a counter bug.
- **F2 (fixed during the wave): the first-draft control was degenerate.** The originally shipped
  `build/check-receipt-presence-draft.kills.json` (8 kills, 5 SURVIVED on the clean tool) is gate-WEAK
  on the UNMODIFIED tool, so it "flags" every hand variant trivially and `control_hand_flagged == hand`
  - the frozen leg (v) (`control_hand_flagged < hand`) could never hold; measured 5/5 before the fix.
  R96MExecKillsC2 replaced it with the 3-kill subset (`0c233a47...`, gate OK kills=3 held=3 on the
  clean tool). The 8-kill first attempt is preserved in their report appendix. The L1 must pin the
  SUBSET sha as `--expect-control-sha256`.
- **F3 (input dependency): the frozen panel must anchor to the final tool bytes.** My counter
  SETUP_ERRORs if any panel entry does not apply (`find` once) or does not keep the selftest green with
  an identical result line. R96MMutC2's panel must therefore be re-anchored to
  `be716a63...` (they measured against a provisional c2 tool and stated they re-anchor before yield).
  The counter enforces `neutral >= 4`; the hand >= 30 minimum is receipt-visible as `H`.

## Exact argv for the L1 to replay at the freeze

```sh
python3 -I quality/counters/c2-r96-selftest-kills.py --repo . \
  --rev <C2-measured-rev> \
  --panel .ufo/waves/round-96/controls/selftest-panel-r96-frozen.json \
  --expect-panel-sha256 <sha256 of the frozen panel file> \
  --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b \
  --expect-kills-sha256 <sha256 of quality/selftest-kills/check-receipt-presence.json at <rev>; the draft bytes hash 305d735fd665ad87566c7983f4e9163eaf323ad1ddb7a99a907e507c8a617495> \
  --control-kills .ufo/waves/round-96/build/check-receipt-presence-draft.kills.json \
  --expect-control-sha256 0c233a47b9d0b855ed92991079399c1e6cf32848d4016081057c569ea3aed0c7 \
  --r90-argv .ufo/waves/round-96/controls/r90-c2-argv-r96.json \
  --expect-r90-argv-sha256 386a5a18f77bf6fa564f2a11498ef21f5c1e7ef461028a2956050d3af52ecda0 \
  --scratch-root <SCRATCH>
```

No `--draft-*` flags: the frozen run scores the bytes at `--rev`. Expected: `TARGET_MET` rc 0 with
`r90_leg=TARGET_MET`. If the L1 freezes the control draft at a different path, substitute the path and
its sha. `--expect-control-sha256` above is already the real shipped artifact's sha; re-hash if the
sibling edits it again.

## Coordination trail (peer messages, quoted facts only in the reports named)

- R96MExecKillsC2: agreed the checks-list + single-needle selftest shape and the three build paths;
  they confirmed the L1's selftest-to-EOF amendment and shipped gate-green files; I reported F2, they
  replaced the control draft with the 3-kill subset and preserved the 8-kill appendix.
- R96MMutC2: panel schema confirmed (JSON list of {id,kind,find,replace,why}, no `all`, every entry
  measured green, >=4 neutrals); they independently measured the pre-move reachable FAIL sets that
  corroborate F1; dry-run offer stands for their anchored panel.

## Limits, risks

- The frozen-mode battery was validated in draft mode (file-backed tool/kill-set) because the changed
  bytes are not at any revision yet; the only difference at the freeze is `git show <rev>:path` vs file
  read - the byte paths, pins and gates are identical.
- The r90 leg costs minutes (83 expectations x (1 + 28 mutants + 4 controls) + 38-commit population,
  thread-pooled); the whole counter at freeze is minutes, not seconds.
- The counter never writes outside `--scratch-root`; scratch removed after validation; no tools
  installed, no host state touched, no network beyond nothing (no fetches were needed).
- Hand-minimum >=30 is enforced by the frozen panel's sha + the receipt's `hand_flagged=h/H`, not in
  code (round-95 precedent); everything else in (i)-(viii) is enforced in code as written.
- Honest limits of the six checks reported by R96MMutC2 (independent of the panel, consistent with the
  declaration's "the kill-set proves each committed kill is still caught ... not that the selftest is
  complete"): the draft dropped the base's fixture-except arm, so a broken fixture now exits 1 with
  EMPTY stdout (my variant greenness precheck treats a missing result line as not green -> SETUP_ERROR,
  so it can never silently read as all-SURVIVED); and seven production mutants survive the unmodified
  selftest (--worktree mode x4, candidates() bare `receipts/` fallback, expand() multi-brace, the hunk
  counter for consecutive added lines).
