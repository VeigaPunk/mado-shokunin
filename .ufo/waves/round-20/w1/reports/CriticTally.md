# CriticTally — P2 tally-check (`566f93be`) closes the numerator-swap and every machine exploit I could construct; remaining risk is reviewer-bound only (contra-sweep, --path to prose, reports scope)


## Landed-implementation re-attack (tally-check.py `1ce05aa0…`, tally-claims.json `79ac2191…`)

Verified in `/tmp/mado-r20-CriticTally` (clone HEAD `e629f73`, files copied in; nothing in the lane touched, no fixture executed):

- `--set red` → 5/5 MISMATCH, exit 1; `--set red --expect` → `EXPECT_SUMMARY: 5/5`, exit 0; empty set → exit 2. The three shipped reds bite for the right reasons: 155→154 (JSON `files[]`, not line count), 5→6 (`first_line`, and the note discloses the 8/13 any-line reading), 10→9 (`selftest-labels` parses `selftest()` as shell: 9 labeled occurrences, 8 distinct — the `OM10` banner comment and diff-line count are structurally excluded, so my headline OM10 counterexample is dead).
- Dead attacks: hardcoded/ad-hoc `argv` (argv[0..3] allowlisted AND the derive is re-invoked as `sys.executable -I <HERE>` regardless of argv[2]); `stated` unbound (required `(?P<stated>)` must equal the field; "ten"→10 verified); mutable registry revs (40-hex-or-`REV` only); derive reading the statement file → `ERROR` (verified); derive rev ≠ statement rev (`--rev` arg to the checker resolved once); ambiguous `line_regex` (>1 match) → `ERROR`; registry-sha and full derive printed per entry.
- Coverage: the seat registered a fourth stale surface itself — `LOG.md:1324` "5/13" (found by `git grep`, my sweep confirms: at `1f7f995` the stating files are exactly `SCORECARD.md:1167`, `corpus/lessons/round-19.md:108`, `LOG.md:1324` — all three registered). Registered reds cover every stale claim surface at the pinned rev.

### Residual attack — LIVE, demonstrated: numerator/denominator swap false-green

`stated` is bound to *a* number in the line, not to *the asserted* number. Working exploit run:

```
statement line_regex: "of (?P<stated>13) credited files name S096"   ← captures the DENOMINATOR
stated: 13
derive extract_regex: "(?m)^denominator=(\d+)$"
→ MATCH demo-swap-denominator stated=13 derived=13   exit 0
```

…over `corpus/lessons/round-19.md:108@1f7f995`, the line that still asserts the stale "5 of 13". The checker certifies a claim that was never corrected: numerator 5 unchecked. Same shape: `stated` bound to any incidental true number in the claim line. Detectable today only by a reviewer reading `key=denominator` in the detail line — the MATCH row looks identical to a real green.

**Smallest safe correction (either suffices; both is cheap):**
1. For fraction-shaped claims, require `(?P<den>)` alongside `(?P<stated>)` in `line_regex` and compare `den` to the derived denominator (`pointer-token` already emits `denominator=`); i.e. claim `N of M` green-checks only when stated-N == derived-num AND captured-M == derived-den.
2. Restrict `COUNT_KEYS` extractable keys to headline counts: remove `denominator`, `pathless_entries`, `removed_unmatched_occurrences` (context/diagnostic outputs, not claim values). `current`, `distinct_paths`, `files`, `first_line`, `any_line`, `removed_occurrences`, `removed_distinct` all name an assertable count; `denominator` does not.

### Residual semantic-swap args (reviewer-bound today, cheap to pin)

- `--token` is enforced to occur in the statement line, but `--label-regex`, `--schema`, `--path`, `--function`, `--fail-helper`, `--counter` are not bound to the prose: a claim "the nine OM9 assertions" + `--label-regex '.*'` derives 9 (over OM10 labels) → MATCH on a wrong claim. `--token S096 --token S090` (duplicate flag, argparse last-wins) is only caught when the second token is absent from the line — verified S090 not on line 108 → ERROR, but on a line containing both it silently counts the last token. Pin: reject duplicate flags in derive.argv; require the claim's label family (`OM10`, receipt name, counter path) to appear as a word in the matched statement line, same mechanism as `--token`.
- `statement.rev: "REV"` is allowed on a **red** entry (verified: runs, MISMATCH at `--rev`). It fails closed (absent prose → ERROR), but it makes a red measure whatever --rev's prose says instead of a pinned historical staleness. Pin: red entries must be 40-hex; `REV` reserved for green.
- Reports are criterion-scope ("SCORECARD/lesson/report") but unregistered: `.ufo/waves/round-19/w2/reports/RerunC2.md:71` "S096 cited as evidence **5/13**" and `CriticC2W2.md:11,153` still state 5–6/13 framings at `1f7f995`. Defensible (they measure their own snapshot; the closure calls the discrepancy out) but it's a scope decision L1 should make explicit — either register them or narrow criterion wording to SCORECARD/lesson/LOG.
- `checker_sha256` is not printed; receipts hash the registry but not the checker bytes that produced them. One-line fix matching the lane's `tool_sha256=` convention.

### Verdict on the first build (P1, superseded by P2 below)

Spec defects from the first pass: 7 of 9 pinned or dead at P1. The two admitted gaps stand: mode-in-prose is reviewer-only (partly mitigated — `key=first_line` prints the mode per entry, so a reviewer sees the definition used), and there is no contra-sweep (a corrected claim can pass while a differently-phrased stale line survives in the same file — exactly what criterion 28 sweeps for at file level). The numerator-swap is the only machine-exploitable false-green found; recommend fix (1)+(2) above before the registry's green section fills in.

## P2 re-attack (tally-check.py `566f93be…`, claims `eaa5a151…`)

Re-verified in the same `/tmp/mado-r20-CriticTally` clone (files copied from the lane, run with `python3 -I`, cwd = clone):

- `--set red --expect` → `EXPECT_SUMMARY: 5/5`, exit 0; fraction entries now display `5/13→6/13` (denominator carried through); `checker_sha256=566f93be…` is in the `TALLY_REGISTRY` header.
- **My demonstrated exploit is closed.** The original `/tmp/swap.json` (stated bound to "of 13", `key=denominator`) now ERRORs — `denominator` is no longer an extractable key.
- Fuzz results vs P2, all correct: fraction entry whose captured `(?P<stated>)`/`(?P<den>)` disagree with the derived pair → MISMATCH 5/13≠6/13 (exit 1); non-fraction key over a number inside a fraction → ERROR; `--label-id OM9` not in the statement line → ERROR; `statement.rev:"REV"` on a red entry → ERROR ("a red entry pins 40-hex revisions; REV is for green entries").
- New shape that MATCHes and is **documented-open, not a defect**: a registry entry can certify a *different, true* claim on the same line — `stated:13`, regex over the "13/13 pointed" half of `SCORECARD.md:1167` → MATCH 13/13 while the "5/13 S096" half stays stale in the same sentence. That is the same-line variant of the admitted no-contra-sweep gap: criterion 30 certifies the registered claim, never "this line/file is free of stale numbers."
- Remaining reviewer-bound surfaces (all admitted by the seat, none machine-demonstrable as false-green): `--path`/`--counter` not bound to prose (a transcript claim could name receipt A and derive from receipt B's files[]); no same-file contra-sweep; mode still a reviewer read (now mitigated — `key=first_line` + `token=S096` + the full derive print make the definition legible in the receipt); w2-report files (`RerunC2.md:71`, `CriticC2W2.md:11,153`) stating 5/13-era framings are unregistered — L1 scope call, defensible either way since they measure their own snapshot.
- Minor auditability suggestion, not a gate: the per-entry detail prints path:line but not the matched line text; printing it would let a reviewer see *which* claim on a multi-claim line was certified without opening the file.

**P2 verdict:** every exploit I could construct as a false-green is closed; the checker's mechanical guarantees are now: stated number(s) are quoted from the matched line (fraction claims fully bound), every count key names an assertable headline count, derive is self-subcommand-only over pinned 40-hex committed bytes, --token/--label-id bound to prose, REV green-only, polarity-aware exits, and the receipt carries checker+registry digests. Safe to integrate; the green section can fill.

P3 addendum (tally-check.py `21ce9dd5…`, claims unchanged `eaa5a151…`): the per-entry detail
now prints `claim="<matched span>"` — verified: `r19-scorecard-c2-5of13-s096` shows
`claim="13/13 pointed; 5/13 name S096 on the"`, `r19-scorecard-ten-om10` shows
`claim="the ten old OM10 assertions were replaced"`. Reds still 5/5 EXPECT-clean. The
multi-claim-line residual is now visible in the receipt itself.

Decisions taken (this seat, for L1): **keep** `r19-log-c2-5of13-s096` — `LOG.md:1324` is a
real stale stating surface at `1f7f995` (my sweep found it; criterion-30 completeness wants
one entry per stating file, not a fixed count). **Do not register** the w2-report statements
(`RerunC2.md:71`, `CriticC2W2.md:11,153`): the seat's re-derivation shows "5/13" was never a
token count at any revision — it is RerunC2's "cited as evidence" tally restated without its
qualifier, so the reports state a *different* claim measured on their own snapshot. L1 should
narrow criterion-30 wording to SCORECARD/lesson/LOG (normative surfaces) rather than register
the reports.

## First pass — spec-level attack (pre-landing; kept for the record of which pins were demanded)

Scope: the spec handed to seat `TallyCheck` (`.ufo/waves/round-20/w1/dispatch.json` task[18]:
registry entries `{id, statement:{rev,path,line_regex}, stated, derive:{argv,extract_regex}, note}`,
red+green sections, exit 0 all MATCH / 1 any MISMATCH / 2 any ERROR). At report time neither
`.ufo/waves/round-20/tally-check.py` nor `tally-claims.json` exists (untracked listing shows only
`corpus-diff.py`, `gen_w1.py`, `tw-precision.py`, `tw-recall-split.py`, `isolate*.sh`), so every
finding below is a spec-level defect that a faithful implementation would inherit — fixable now,
expensive to retrofit after the registry schema commits.

## Attack 1 — "choosing the matching definition": real, and the OM10 red already demonstrates it

A count claim is ambiguous whenever the prose omits its counting rule. All three round-19
staleness examples have at least two plausible derivations, and the *convenient* one can MATCH
the stale prose:

- **OM10 (the strongest counterexample — the red is escapable).**
  `git diff 9c54c56 7b4839d -- tools/mado-verify.sh` produces **10** removed lines containing
  `OM10` (9 `st_*` assertion calls + the `# --- OM10: describe/rev-parse rc≠0 …` banner comment).
  A derive of `count removed lines matching OM10` returns 10 → **MATCH** on SCORECARD:1225's
  "the ten old OM10 assertions", i.e. the check blesses the very claim the closure
  (`corpus/lessons/round-19-verifier-spotcheck.md`, R19-V5: nine labeled occurrences, eight
  distinct) proved stale. Only the narrower derivations bite: removed `st_` call lines → 9;
  distinct quoted assertion strings on removed lines → 8 (enumerated: `counts agree`,
  `describe rc=128`, `exactly two omarchy UNKNOWNs`, `no false head MOVED`,
  `no false tag MOVED`, `rev-parse rc=128`, `show succeeds`, `the UNKNOWN names the rc`).
  If the spec's `derive` subcommand is implemented as "lines removed containing the label",
  the red never fires and criterion 30's red evidence is silently vacated.
- **S096.** Verified at the pinned set (fresh-pins.py denominator: 13 files under PIN_REV
  `9c54c56` containing `2.17.0`, evaluated at `1f7f995`): any-matching-line 8/13, first-matching-
  line 6/13, five S090-only files — same numbers as the closure. The stale "5/13" mismatches both
  *today*, but the same prose matched by two different subcommand modes is the template: a
  registry entry that doesn't bind mode lets a future claim of "8/13" pass under `any` while a
  reviewer reading "the crediting line" understands first-line (6/13). Prose must name its
  counting rule or the entry must bind it.
- **Transcripts.** The receipt `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt`
  (blob `5982e233…`, sha256 `9572d2a6…`, committed at `1f7f995`) yields 154 by `"path":`
  occurrences and 154 by parsed `files[]` length — but **1** by `grep -c '"path":'` (the JSON is
  a single line) and 0 by counting `.jsonl` lines of the receipt itself. Line-count vs
  JSON-member-count vs substring-count gives {1, 154, 154}; a sloppy or hostile derive can pick
  the answer. Also note the 154 files are live-session digests; the derive must count the
  committed receipt's members, never the live session dir (host pause: live state is not
  committed bytes).

**What the registry must pin (definition axis):** the counting rule is part of the claim.
Minimal safe form — subcommands are *claim-specific, mode-exhausting* (e.g. `om10-assertions`
emits `{occurrences:9, distinct:8}`; `s096-credit` emits `{any:8, first:6}`; `scan-files` emits
`{files:154}`), the entry carries a `mode` key naming which emitted number is claimed, and the
checker's `line_regex` must match a mode-consistent phrasing in the prose — or simpler: the
prose is required to spell the rule ("first matching line", "distinct assertion texts") and the
checker treats a claim whose prose is mode-silent as ambiguous (ERROR), never silently picking.
A generic `count-token --regex X` subcommand recreates the OM10 cheat at the tool level and
must not exist.

## Attack 2 — "a derive command that hardcodes the answer": blocked only if the checker allowlists argv

The entry schema puts `derive.argv` under registry control. Nothing in the *schema* stops
`argv: ["bash","-c","echo 154"]`, `["python3","-c","print(154)"]`, or
`["git","show","REV:.ufo/waves/round-20/answers.txt"]` (a committed answers file — derivation
by cat). The seat spec says subcommands live inside tally-check.py, but that is an instruction
to the seat, not an enforceable property of the entry format; if the checker execs registry argv
verbatim, green claims self-certify forever (a hardcoded derive MATCHes at every future rev —
the exact stale-tally failure this criterion exists to catch, one layer down).

**What must be pinned:** `argv` shape — checker rejects any argv whose argv[0] is not the
checker's own path and argv[1] not in its subcommand table (anything else → exit 2 ERROR);
subcommand args are schema-fixed (revs, paths, entry id), never free strings; all rev args must
be 40-hex and every `git` read is `git show|ls-tree <sha>:<path>` — no HEAD, no branch name, no
worktree path. Additionally the derive's *data source* must not be the statement file: a
subcommand that reads `statement.path` to extract the number closes the loop (the prose
re-derives itself). Recommend the entry declare `source_path`/`source_rev` for the underlying
data (e.g. receipt path, the 13-file denominator, the diff endpoint pair) so a reviewer can
diff claim-source vs statement-path at a glance.

A residual, softer version survives any allowlist: `extract_regex` is per-entry, so a
subcommand emitting several numbers lets the registry regex-select whichever matches the claim.
Fix: each subcommand has one canonical output contract (fixed JSON key set printed by the
checker itself); `extract_regex` should be checker-owned per subcommand or deleted in favor of
the `mode` key.

## Attack 3 — "moving the prose": possible on the green side, and the red side needs total-match auditing

- **Mutable rev.** `statement.rev` as `master`/`HEAD`/a short sha is a self-fulfilling pin:
  move or edit the prose, the check re-reads the new tip. Pin: 40-hex only; checker resolves
  `rev^{commit}`, prints the resolved sha in the receipt (`measured_commit=`-style header, the
  lane's existing receipt convention), and errors on non-hex.
- **No measured-REV knob for green.** The checker's only input is `tally-check.py REGISTRY`.
  A green entry's prose lands in the final integration commit — a hash unknowable when the
  registry is written, so green `statement.rev` is forced to be (a) a mutable ref (Attack 3a),
  (b) a hash that can't yet exist, or (c) a pinned historical hash that goes stale the moment
  the prose is touched again (green check stays green on yesterday's claim while today's prose
  reverts — the classic "check certifies an old revision" hole; the lane already names this in
  criterion 25/26 receipts as `measured_commit`). Smallest safe correction: give the checker a
  `REV` argument (like `measure.py REV`, `anchor-durability.py REV`); green statements are read
  at `REV`, reds at their pinned historical rev. Alternatively the registry's green statement
  pins a commit that *contains* the corrected prose and the criterion accepts staleness — the
  REV-argument form matches sibling checkers and is cheaper to audit.
- **Satisfying the regex while the stale claim survives.** `line_regex` existence is monotone:
  append "8/13 (corrected)" anywhere and a green entry MATCHes while "5 of 13 … crediting line"
  still stands at `corpus/lessons/round-19.md:108` (verified present at `1f7f995`) — the prose
  moved the *claim the registry watches* without removing the stale one. Criterion 28
  (`supersede-sweep.py`) already fights exactly this for `2.17.0`→`2.17.2`; criterion 30 needs
  the same hygiene at claim granularity. Pin: (i) the checker reports **all** lines matching
  `line_regex` in the file at rev, not the first, and `AMBIGUOUS`/ERROR when matches disagree
  on the stated number or mode; (ii) each entry names a `contra_regex` or, simpler, the checker
  greps the same file at the measured rev for other statements of the same quantity with a
  different number (for our three claims: `[0-9]+/?1?3? ?(?:of|/) ?1?3?` families are messy —
  the honest minimum is: green `line_regex` must match a line that *corrects in place or is
  marked as the correction*, and the red entry's prose stays red because it is historical);
  (iii) multi-file claims (the S096 count is stated at `SCORECARD.md:1167` *and*
  `lessons/round-19.md:108` at `1f7f995`; verified) need one entry per stating file, or a
  `statements:[]` list — a single-file entry leaves the sibling stale claim unmeasured.
- **Spelling.** "5/13" vs "5 of 13" (both present: SCORECARD uses `5/13`, the lesson uses
  `5 of 13`) and "ten" vs "10": a `line_regex` that only matches digits misses the numeral-word
  claim ("ten old OM10 assertions" has no digit). Either `line_regex` must cover the claimed
  form and `stated` is checked against the *matched line's* number (next section), or the entry
  carries a normalization table (one..twenty → digits). Pin this or the OM10 red silently
  cannot match its own prose.

## Attack 4 — `stated` is unbound from the text (the cheapest cheat of all)

The schema stores `stated` as a JSON field; the spec only requires `line_regex` to match a line
at rev. Two exploit directions:

- Registry claims `stated: 154` over a line that literally says "155" → derived 154 → MATCH →
  a *false green* certifying prose that is still wrong.
- Registry claims `stated: 6` over the "5/13" line → derived 8 → MISMATCH → a *manufactured red*
  satisfying "must MISMATCH" against any true statement.

**What must be pinned:** `stated` is not an input; it is extracted from the matched line. Put
the number capture in `line_regex` itself (`(\d+)` / a numeral-word map) and require the claim
to consist of exactly one captured number — or keep `stated` but fail with ERROR when the
matched line does not contain that token. Same for compound claims: "5 of 13" is numerator +
denominator; a derive that returns only the numerator green-checks a claim whose denominator
the registry quietly changed (8/14 would MISMATCH anyway here, but `8/13` over a 14-file set
under a redefined denominator is a real shape once the file set is arg-driven). Pin: compound
claims store `stated: {num: 5, den: 13}` and the subcommand emits both; MATCH requires both.

## Attack 5 — exit polarity: the spec's own red entries break the stated exit rule

"exit 0 all MATCH, 1 any MISMATCH" with red entries that "must MISMATCH" ⇒ the registry as
specified exits 1 forever, and a red entry that *matches* (the OM10 cheat above) can flip the
aggregate to 0 — exit 0 becomes *evidence of the bug*. Polarity must be explicit: each entry
carries `expect: match|mismatch` (or the checker derives it from the section), exit 0 iff every
entry lands on its expected side and no ERROR; a red-MATCH and a green-MISMATCH are the same
verdict class. Also pin: an empty "green" section is not vacuous-0 while reds remain — the
criterion's green receipt should name which entry ids greened (auditability, and it makes a
dropped red entry visible since the receipt then lists an unknown id).

## What the registry must pin — consolidated minimum for TallyCheck

1. `statement.rev` and every rev in `derive` args: 40-hex, resolved `^{commit}`, printed in the
   receipt; green statements read at the checker's `REV` argument (add it).
2. `stated` extracted from the matched line (capture group), compound claims as {num, den};
   numeral-word normalization for "ten".
3. Exactly-one-match or all-matches-agree on `line_regex` per file; one entry per stating file;
   a `contra`/sweep provision so the same file cannot keep a second line stating the same
   quantity differently at the measured rev.
4. `derive.argv` allowlisted to self-subcommands; per-subcommand fixed output contract (mode
   map), `mode` named in the entry and required to be legible in the prose (any-line vs
   first-line vs occurrences vs distinct vs file-count); derive inputs are committed data paths
   distinct from `statement.path`.
5. `expect` polarity per entry; exit 0 ⇔ all expectations met, no errors; the red set is
   enumerated by id in the criterion text / receipt so a dropped entry is detectable.

## Evidence index

- OM10 cheat: `git -C <lane> diff 9c54c56 7b4839d -- tools/mado-verify.sh | grep -c '^-.*OM10'`
  → 10 (banner comment included); `grep -c '^-.*st_.*OM10'` → 9; distinct quoted texts → 8
  (listed above). SCORECARD:1225 "the ten old OM10 assertions" verified at `1f7f995`.
- S096: reproduced closure counts — any-line 8/13, first-line 6/13, five S090-only files —
  via fresh-pins.py's denominator (PIN `9c54c56`, in-scope `2.17.0` files = 13) evaluated at
  `1f7f995`. Stale claims: `corpus/lessons/round-19.md:108` ("5 of 13 credited files name S096"),
  `SCORECARD.md:1167` ("5/13 name S096"), both at `1f7f995`.
- Transcripts: `lessons/round-19.md:124` "155 round-19 transcripts" at `1f7f995`; receipt
  `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt` blob `5982e233` at `1f7f995`,
  sha256 `9572d2a6…`, `"path":` occurrences = 154, `files[]` = 154, `grep -c` lines = 1.
- Spec text attacked: `.ufo/waves/round-20/w1/dispatch.json` task[18] "TallyCheck".

## Limits

- P1 findings superseded where noted; P2 (`566f93be`) verified by re-running the shipped reds
  plus five hostile registries in `/tmp/mado-r20-CriticTally` (clone HEAD `e629f73`). Not tried:
  regex-catastrophic-backtracking timing (a ReDoS `line_regex` would hang the check, not fake
  a verdict), and derive output > the match budget.
- Did not enumerate *every* line in the lane stating the three stale numbers beyond a `git
  grep` at `1f7f995` (found the three registered locations; w2-report occurrences are a
  documented scope decision for L1).
- The `contra_regex` sweep design is sketched, not prototyped; a naive regex for "same
  quantity, different number" will have false positives on fraction families.
- Line-citation erratum (seat's catch, fixed above): the stale "5 of 13" lesson line is
  `round-19.md:108` at `1f7f995`, not `:110` as an earlier draft of this report said.

## Installs

none.
