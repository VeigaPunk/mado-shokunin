# R88MReviewC1 — C1 candidate + counter attack review (wave w1, round 88)

Scope: (1) diff `24ba2a9…:tools/mado-mako.py` → `.ufo/waves/round-88/build/mado-mako.c1.py`, every
changed line checked against mako 1.11.0 manual (`zcat man5/mako.5.gz | nl -ba`, sha256 f717848f… ✓)
and upstream v1.11.0 `criteria.c` / `types.c` / `config.c` (raw.githubusercontent, tag v1.11.0);
(2) full read of `quality/counters/c1-r88-mako-fields.py` (411 lines) + its borrowed r87 machinery
(`c1-r87-mako-criteria.py`, 687 lines) + `--selftest`; (3) audit of every NEW case in
`.ufo/waves/round-88/controls/mako-cases-r88.json` against its pins and the declaration contract —
without running the candidate on any authored case.

## Verified sound (evidence)

- Diff reviewed hunk-by-hunk (259-line unified diff; base.py 537 lines kept in scratch).
- `parse_boolean` (c1.py:159-166) uses `value.lower()`, matching upstream `types.c:19-26`
  `strcasecmp("true"/"false")` + `strcmp("1"/"0")` exactly — including non-ASCII: probes
  `invisible=TRUE` → `"1"` accepted; `invisible=falſe`, `invisible=ｔｒｕｅ` → refused (C byte
  semantics refuse them too; no Unicode char `.lower()`s into {t,r,u,e,f,a,l,s}; `str.lower()` —
  not `casefold()` — so the `'ſ'.casefold()=='s'` trap is avoided). 1/0 exact on both sides.
- Criteria booleans go through `parse_boolean` upstream (`criteria.c:370,378`): probes
  `[actionable=TRUE]` / `[expiring=False]` match ✓. Bare grammar matches `apply_criteria_field`
  (`criteria.c:296-314`): `[actionable]`→true, `[!actionable]`→false, `!` only on bare tokens
  (`[!actionable=x]` refused on both sides), bare non-boolean refused on both sides.
- Strings are strcmp-exact: `[summary=x]` vs `--summary Hello` → nomatch; `[summary=""]` matches
  `--summary ''` (empty input is a decided value, never "missing"); `[actionable="true"]` quoted
  boolean token matches. `--app-name ''` cannot occur in cases (counter refuses it, inherited r87).
- Style booleans: upstream `config.c` parses exactly icons/markup/actions/history/ignore-timeout/
  invisible with `parse_boolean` (config.c:593,621,623,644,650-651,653-654) = `BOOL_KEYS`; the
  manual documents each as `0|1` at L266/311/320/328/363/545 ✓; `normalize()` reports the manual's
  0|1 form (`invisible=TRUE` → `"1"`, `invisible=False` → `"0"`), invalid values refused.
- `summary~`/`body~` refused = declared limit; the manual gives `~` only to summary/body
  (L447-457), so the limit list is complete.
- A section mixing a mismatch and an undecided field → `nomatch`, no refusal (inherited r87 logic;
  faithful to manual L431-434 "matches when all of its fields match").
- Counter predicate (c1-r88:229-232) matches the declaration sentence conjunct-for-conjunct:
  `correct==n and killed==m and carried==22 and naive<n and globals<n and base<n`; exit map
  0/1/2; receipt label `MADO_MAKO_FIELDS`; score `10*correct/n`.
- Pins: mutants file sha256 `40645a28…` == declaration pin ✓; r87 counter sha256 `4d801c30…` ==
  `R87_COUNTER_SHA256` (asserted at runtime by `check_r87_pin` and by selftest) ✓; cases sha256
  checked against `--expect-cases-sha256` before `load_cases`; tool+mutants read from `--rev`,
  base tool from `--base-rev` via the same scrubbed-git real run path; counter self-hash printed.
- M01–M10 byte-equal to the r87 mutant file ✓; all 19 anchors occur exactly once in the candidate ✓.
- r87 machinery reuse is sound (canon carried-check, materialize symlink support, `tool_verdict`,
  naive/globals controls, `exit_for` 0/1/2, scrubbed git env).
- Scratch hygiene: `evaluate`/`selftest` create one generation dir under `--scratch-root` and
  rmtree it in `finally`; nothing written outside it.
- Counter `--selftest --scratch-root $S`: 15/15 PASS, exit 0. Candidate tool `--selftest`:
  41/41 (`MADO_MAKO_SELFTEST: checks=41 failed=0`), exit 0.
- Base-tool control discriminates structurally: the r87 tool rejects the new CLI inputs
  (`--summary` etc., argparse exit 2), so `base_correct ≤ 22 < N_MIN=40` whenever any new-input
  case exists, and the predicate would honestly refuse a case set that adds no new surface.

## Findings

### F1 (HIGH) — repeated criteria fields: candidate refuses, upstream applies last-wins
- Where: `build/mado-mako.c1.py` `open_section` repeat refusal (`"criteria field … is repeated"`,
  inherited from base.py:274) colliding with the NEW bare/`!` boolean normalization
  (`value = "true"` / `key, value = key[1:], "false"`).
- Source: upstream `criteria.c` `apply_criteria_field` applies every token with no dedup and no
  error — a repeated key overwrites: `[actionable !actionable]` ≡ `[!actionable]`,
  `[app-name=a app-name=b]` ≡ `[app-name=b]`.
- Repro (candidate run): config `[actionable !actionable]\nwidth=9\n` with `--actionable false`
  → refusal `criteria field 'actionable' is repeated`, width stays 300; upstream applies the
  section (width 9). Same divergence for any repeated modelled field.
- Impact: this is r87-frozen behavior for the old fields, but `[actionable !actionable]` is a NEW
  reachable collision the new normalization creates (the r87 3-field surface could not produce a
  boolean repeat). Any w1 case covering repeats must expect upstream last-wins; a case expecting
  refusal is unsupported by the cited sources, and a case expecting last-wins sinks the candidate
  (correct < N → TARGET_MISSED). The authored case set covers no repeat, so the divergence is
  currently latent — it surfaces in residual r1 unless the declaration names it.
- Fix: either collapse repeats last-wins in `open_section` (no r87 frozen case exercises repeats —
  c01…c22 contain none — so the 22 carried cases are unaffected), or keep the refusal and declare
  it as a named limit in the C1 declaration BEFORE the freeze, ensuring no case expects last-wins.
  Resolve before freeze; do not let the case set and the tool disagree silently.

### F2 (LOW) — "undecided input is refused" reads stricter than the code in mixed sections
- `evaluate()` computes all mismatches first; a section mixing a mismatch and an undecided input
  returns `nomatch` with NO refusal. Repro: `[app-name=other summary=hello]` with only
  `--app-name me` → no refusal, width 300. Inherited r87 semantics, faithful to manual L431-434;
  recorded so the scribe's case expectations do not encode a refusal here — the source-supported
  expectation is `refusals:"none"` plus the section not applying.

### F3 (INFO) — r87 counter executes at import before its pin is checked
- `R87, R87_DIGEST = _load_r87()` runs the r87 module's top level before `check_r87_pin()` can
  abort; a tampered r87 counter would execute first. Defense-in-depth only: any tamper still
  fails the pin before any scoring (exit 2, never a verdict), and the freeze carries the digest.

### F4 (INFO) — carried check bounds the count, not the r87 file
- `carried == 22` is enforced but not `carried == len(r87 cases)`. Equivalent today (the frozen
  r87 file has exactly 22 cases — verified at base); harmless.

## Case-set audit (.ufo/waves/round-88/controls/mako-cases-r88.json, sha256 818b2bfce97b5f5c4f98ad1afc69775608af4ffd1ee4c272f0619cc4e0886ff1)

File appeared during the seat window; audited WITHOUT running the candidate on any case.

- N=59 (37 new + 22 carried), within the declared 40..64; ids unique; schema `mako-cases-r88-v1`.
- All 22 r87 frozen cases are canon-equal (json sort-keys) to the r87 file at base — carried check
  will see 22/22. Verified none of the 22 exercises repeated criteria keys.
- Structural conformance: every `expect.effective` value is a string; args keys valid except c51
  (F5); no app-name empty; all `mode` values strings/lists; urgency enum only.
- C1 separability holds: no new case passes `--read-root` (schema has no such input) and the only
  include lines are c13's in-home include (frozen r87) and c23's relative include, which the tool
  refuses before any open (manual L45-50) — nothing outside `--home` is read.

Per-case source audit of all 37 new cases — every expectation checked against the manual/upstream:

- Supported refusals (`present`): c23 relative include (manual L45-50, r87-frozen stance);
  c28/c40/c41/c52 undecided app-name/summary/app-icon/booleans (declared "never guessed" rule);
  c29 unmatched quote (manual L497-508); c50 `[actionable=yes]`/`[expiring=maybe]` and c56
  `icons=yes` (types.c parse_boolean refuses); c53 `[summary~=hello]` (declared limit).
- Supported matches/nomatches: c24 `[mode=default]` (manual L614-621 initial mode); c25-c27
  defaults (font `monospace 10`, layer `top`, border-size `2` — manual Default lines / DEFAULTS);
  c30-c39 app-icon/summary/body/category/desktop-entry exact strcmp match, case-sensitivity
  (c33) and mismatch-without-refusal; c42-c49 the full boolean grammar (true/false, 1/0, bare,
  `!`-negated, TRUE/FALSE, True/FaLsE — types.c strcasecmp); c48/c49 kill the M14 anchor;
  c54/c55 style booleans `invisible=true`→`"1"`, `icons=false`→`"0"` (normalize, manual 0|1
  form); c57/c58 the declaration's host DND pair (both `[mode=do-not-disturb]` sections match for
  notify-send, last wins → invisible "0"; other-app → "1"); c59 mismatch-beside-undecided →
  nomatch, no refusal (manual L431-434) — matches F2's reading, so the scribe encoded it
  correctly.
- No NEW case exercises repeated criteria fields, so F1's divergence is real but UNCOVERED by
  this case set: it cannot sink C1's verdict, but it stands as an undisclosed upstream deviation
  in the newly claimed surface (see F1).

### F5 (HIGH, blocks scoring) — c51-boolean-mismatching-flag has a typo'd arg
- Where: `.ufo/waves/round-88/controls/mako-cases-r88.json`, case c51, args
  `{"actionable": "false", "exiring": "false"}` — `exiring` is not a declared input.
- Evidence: running the counter's own `load_cases` on the authored bytes raises
  `SetupError: c51-boolean-mismatching-flag.args: unknown or non-object args`; the counting
  command would exit 2 (SETUP_ERROR, never a verdict) — the whole C1 run dies, not just c51.
- Intent is otherwise sound and source-supported: with the typo read as `expiring: "false"`, both
  sections mismatch → anchor/layer stay at defaults, `refusals: "none"` — exactly the recorded
  expectation. Fix: rename `exiring` → `expiring` before the freeze (the cases sha256 pinned in
  the freeze must be taken after this fix).
- Caution: deleting the bogus key instead would leave `[expiring=true]` undecided → refusal,
  contradicting the recorded `refusals: "none"`; the typo fix is the only consistent repair.

## Housekeeping

- Scratch: `/fast/scratch/hyaku/mado-r88/R88MReviewC1` (base.py, c1.diff, upstream sources,
  mako5.txt, probe dirs — all temp dirs removed); deleted at seat exit.
- Installs: none (all tooling present).
- Commands + exit codes: counter selftest exit 0; tool selftest exit 0; probes all exit 0;
  `git show`/`sha256sum` exit 0; no mutating git anywhere.
