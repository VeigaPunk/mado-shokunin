# R56W2MutC1Harness — wave 2 (falsify): mutation test of the C1 control harness

Attacked item: the C1 control harness `quality/r56_ctl_c1.py` at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` — the twelve
frozen controls (registration §C1, amended by registration-v2 E5), the good-tree judgement, and the denominator. Question:
can a harness mutant still print `controls=12/12 verdict=OK` while a control is vacuous or measures the wrong defect?
Wave-1 kill evidence was each seat's own selftest; this seat supplies an independent differential battery.

Deliverables (absolute paths, all under the lane's `.ufo/waves/round-56/w2/R56W2MutC1Harness/`):
- `mutants.md` — the full report: 66-row mutant table with per-row outcome and killing oracle or equivalence argument,
  survivors in full, verified proposals, limits, reproduce steps.
- Drivers: `drive.py` (66 mutants x 40 oracles), `gen_stubs.py`, `extra_variants.py` (fixtures), `final_table.py`
  (classification), `verify_props.py` (P1–P3), `verify_p4.py` (P4), `write_md.py`.
- Receipts: `receipts.tar.gz` (per-mutant, per-oracle `.out`/`.err`/`.rc`, `PRISTINE/`, `run-full.log`, `summary.json`),
  `classes.json`, `proposals/` (`gold.json`, `summary.json`, `p4.txt`, patched module and output per run), `stubs/`, `wrappers/`.

Scratch `/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness/` was removed before yield; the deliverables above are copies.

## Commands and decisive output

Pristine, read-only against the lane, at the revision (the only harness run that touches the lane; writes only under `--work`):

```
python3 -I pristine/check-r56-controls.py --claim c1 --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 28fc86ac2359ec27406d8a2c63bef82ea6e947ed --work /fast/scratch/hyaku/mado-r56/R56W2MutC1Harness/run/base
-> MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK   (rc 0)
```

Determinism: two pristine runs on the scratch copy, stdout and stderr byte-identical.

Oracle expectations on the pristine module (checked, not assumed):
```
stub_green   -> MADO_R56_CONTROLS: claim=c1 good=ok controls=0/12 verdict=FAIL   (rc 1)
stub_reject  -> MADO_R56_CONTROLS: claim=c1 good=bad controls=0/12 verdict=FAIL  (rc 1)
w_stderr     -> good=ok controls=12/12 verdict=OK   (benign: registration mandates stderr only on the exit-2 path)
```

Battery and classification (`final_table.py`, from receipts):
```
mutants 66 · oracles 40 · killed 44 (66.7%)
  K-spec 25 (real / green / reject) · K-extra 16 · K-fix 3 (fixtures)
  W 5 (verdict-level survivors, wrong reason) · D 2 (diagnostic only) · E 15 (equivalent, argued)
kill rate excluding equivalent 86.3% (44/51) · excluding equivalent and diagnostic 89.8% (44/49)
spec-only oracles on the verdict-relevant set 51.0% (25/49)
```

Proposals (each applied to pristine and to the survivor; `verify_props.py`, `verify_p4.py`):
```
P1 pinned missed sets    pristine 12/12 | M23 7/12 | M24 11/12 | M25 11/12 | M58 11/12 | M60 11/12 | M55 12/12 | M56 12/12
P2 echo:K07 required     pristine 12/12 | M58 11/12 | M23 M24 M25 M60 12/12
P3 row locality          pristine 12/12 | M23 7/12 | M60 11/12 | M24 M25 M58 12/12
P4 H rows junked         pristine 12/12 | M25 11/12 | M24 12/12
fixture var_srcline2     pristine 12/12 | M63 11/12
fixture var_pinlink      pristine good=bad 10/12 | M15 good=ok 12/12 | M16 good=bad 11/12
```

## What was attacked, item by item

- The twelve registered mutations: each control's mutation is applied and the counter reports the required leg on the real
  counter (pristine 12/12). Vacuity mutants M33 (control 10 deletes S391 instead of S390), M34, M36 (control 1 applies no
  mutation), M30 (control 7 deletes K16 instead of K17), M61/M62 (wrong expected legs), M28 (scope anchor covers the line),
  M66 (control 5 re-points to S383), M26 (the planted number is admitted): every one is killed. No registered control is
  vacuous on the real counter.
- The good-tree judgement: M03, M43, M44, M45, M46, M50 killed (counts, exit status, stderr guard, verdict/missed `or`→`and`,
  grammar). Killed by the spec's green stub, reject stub or the real counter.
- The denominator: M02 (N=11), M47 (`and`→`or`): `good=ok controls=0/12 verdict=OK` on the always-green stub, killed.
  M57 equivalent for accepted inputs (tables sha pinned).
- Parsers and grammar: row, leg, regex, fence, comment, cell-count, separator and dup-row mutations (M04–M11, M18–M23, M48–M50)
  killed, but 10 of them only by my wrappers, stubs or variant trees (M04, M06, M08, M11, M18, M20, M21, M22, M48, M50); the frozen controls do not exercise them.
- Control-internal checks (`_need`, `_need_junk`, `_need_echo`, `_expected_leg`, `_clip`, `m_quote_echo` threshold): M37–M39,
  M55–M58 analysed; M58 is a real survivor (verdict-level, K07), M55/M56 diagnostic only.

## Defects found (severity per the seat rubric)

| # | defect | input that shows it | severity |
|---|---|---|---|
| 1 | Controls 2, 3, 4 (and 7, 8 by design) pass on a row-grammar fault they did not mutate: the verdict cannot tell the intended defect from a malformed row. | mutant M23 (`_join` separator `" |"`): `controls=12/12 verdict=OK` on the real counter; stderr shows `row:K04,num:K04` for control 3. | weakens the claim (12/12 is not sufficient evidence for controls 2–4); fixed by P3 (7/12) and P1 (7/12). |
| 2 | Control 2 (junk placeholders) does not pin the duplicate-proposition fault: H rows that share a placeholder pass. | mutant M60: `12/12`; stderr shows `row:H01,row:H02,row:H03`. | weakens; fixed by P3 (11/12) and P1 (11/12). |
| 3 | Control 2 lexical hole at K23: the frozen junk text shares the identifier `source` with K23's quote `source= skipping directory {}`, so K23 gets no `tok:` leg. The control passes with 32 of 33 rows lexically flagged. | pristine control 2 missed list (gold.json): tok legs for 32 rows, K23 absent; mutant M24 (token-disjoint junk for K rows) gets all 33. | weakens (one row of the junk control is not lexically junk); root-cause fix verified by M24's receipts (33/33, verdict unchanged); P1 kills M24 (11/12). |
| 4 | Control 2 does not require H rows to be junked. | mutant M25 (`for rid in ctx["k_ids"]`): `12/12`. | weakens; P4 kills (11/12, verified), P1 kills (11/12). |
| 5 | Control 11 (quote-echo) does not require the 30-character quote row K07; the threshold `>= 30` can drift to `>= 31` unseen. | mutant M58: `12/12`; stderr loses `echo:K07`. | weakens; P2 kills (11/12, verified), P1 kills (11/12). |
| 6 | The frozen battery (real, green, reject) kills 25 of 49 verdict-relevant non-equivalent mutants. Of the 24 others, 19 are reached only by my stubs, wrappers or variant trees (fence indent 4, closed comments, duplicate rows, six-cell rows, ~~~ fences, symlinked pin, source window) and 5 (M23–M25, M58, M60) by none of the battery. The harness's independence from the counter's own parser is therefore narrower than its 12 controls suggest. | `classes.json`: K-extra 16, K-fix 3, W 5 vs K-spec 25. | weakens (scope of the independent check); not a defect in the 12 controls. |
| 7 | Registration collateral lists are incomplete: the pristine harness prints `note: collateral legs beyond the registered ones` for controls 4, 5, 7, 8, 10, 11, 12 (control 7 alone adds five legs). | pristine stderr, control 7: `source_cell:K17,scope:K17,tok:K17,num:K17,echo:K17`. | cosmetic (no verdict effect; documentation gap in the registration). |
| 8 | Harness stderr embeds scratch commit SHAs (`rev=0000…, passed <sha>`), which change every run (commit timestamps), so stderr is not byte-stable across runs. | pristine stderr differs between runs on the `greenbadrev` stub until SHAs are normalized. | cosmetic (affects any golden diagnostic pin; normalize SHAs). |
| 9 | Counter stderr on a green run is ignored (`w_stderr` → `12/12 OK`). The registration does not forbid it. | wrapper `w_stderr`. | observation only. |

No blocking defect was found: none of the twelve registered controls is vacuous, and the good-tree judgement and the denominator
withstood every mutant aimed at them (the `and`→`or` denominator mutant M47 is caught by the always-green stub, as required).

## Equivalence (argued, not counted as kills)

15 mutants print identical stdout, exit status and normalized stderr under all 40 oracles and are equivalent for the frozen
inputs or for every input (M05, M12, M13, M17, M54 for every input; M14, M57 for every accepted input because the tables file
is hash-pinned and checked first; M27, M29, M31, M32, M35, M59, M65 as another instance of the same defect class; M01 is a
host-timing hazard — unloaded counter run 0.18 s, no TIMEOUT in any receipt). Two diagnostic-only mutants (M55, M56) change
only stderr notes or print width. M15, M16, M63 were equivalent on the frozen tree and are killed by the fixtures above.

## Tooling

No tool was installed or upgraded. Python 3.14.8 and git 2.56.0 were used as present. No pacman, no sudo, no compositor or
service change, no write under `~/.config` or `~/.local`, no write to any sibling lane, fleet repo or shokuknow repo. All git
commands on the lane were read-only (`show`, `ls-tree`, `cat-file`, `archive`, `rev-parse`); the scratch repo was built with
`git init` and a single `git archive` export, with the toplevel asserted before each commit.

## Not verified / limits

- The 66 mutants are a sample of one-line edit classes; kill rates describe this sample, not an exhaustive enumeration.
- The extra oracles (kitchen-sink, single-leg stubs, wrappers, variant trees) are mine; the frozen harness has no control for
  them. The spec-only figure (25/49) is reported beside the all-oracle figure.
- P1 pins the counter's current output; a legitimate counter change must regenerate the golden (maintenance cost).
- Proposals were verified on the real counter's tree and on each survivor; the proposal runs were not repeated across all 40 oracles.
- Equivalence is argued for this counter and this tree, not proved for all counters.
- Counter entailment (does the proposition say what the pin says) is out of scope for this seat, as the registration states.
