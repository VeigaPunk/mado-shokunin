# RevEvidenceLabelsR14 — round-14 receipt-label audit

Seat: `MadoR17.RevEvidenceLabelsR14` (leaf, no delegation). Date: 2026-10-20.
Audit target: `corpus/lessons/round-14.md` (read at lane HEAD `0175f13`, which is
the measured revision plus the append-only `97c3583` binding text) and
`SCORECARD.md` §"Round 14 — committed measurements and author verdicts"
(lines 496–593). Every `.txt`/`.json`/`.tsv` receipt cited there was opened and
compared against the claim it supports.

Axes: (A1) citation-to-recorded-verdict accuracy; (A2) coverage of the citation
surface (no cited receipt skipped); (A3) non-duplication — separate newly found
label defects from the already-learned R14-V1.

Method and limits: read-only. `git show <rev>:<path>`, `sha256sum`, plain file
reads, and one static text transform of `tools/mado-verify.sh` (marker-range
deletion, no execution). No gate, harness, selftest, mutant, frozen or census
run; no pacman/yay/paru (not even `-Q`), no sudo, no systemctl/hyprctl/live
probe, no jj, no OMP sessions read, no writes outside this report. No tools
installed or updated. No `lsp` device is mounted in this seat's tool inventory,
so caller/definition checks are not available; text and `git show` reads are
the literal fallback and are treated as literal evidence, not semantic proof.

## Findings

### F1 — MEDIUM, already learned as R14-V1: three mutation receipts label a provisional gate, not the delivered one

Claim side:

- `corpus/lessons/round-14.md:147` — "Content measured at `32118fc…`" and
  `:148-150` — "Full commands/stdout/stderr/exits are under
  `.ufo/waves/round-14/evidence/`; these are observed results".
- `corpus/lessons/round-14.md:170-175` — "`regression-recut.txt`: historical
  10/10 KILLED; new `regular-target-mutants.txt`: 4/4 KILLED; retained
  `retained-census-mutants.txt`: 8/8 KILLED. All GREEN controls/restore OK, all
  exits 0".
- `SCORECARD.md:536-541` — same three counts, "each with GREEN control and
  restore OK. Exact harness invocations/output and result tables:
  `evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt`
  and corresponding TSVs."

Recorded receipt bytes (mismatch is provenance, not verdict):

| receipt | line 3 | line 4 (`gate_sha256`) | `measured_commit` | MUTATE_DATE |
|---|---|---|---|---|
| `evidence/regression-recut.txt` | `input_binding: provisional worktree snapshot` | `ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b` | absent | `2026-10-20T05:58:44Z` (`:7`) |
| `evidence/regular-target-mutants.txt` | same | `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36` | absent | `2026-10-20T06:00:23Z` (`:7`) |
| `evidence/retained-census-mutants.txt` | same | `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36` | absent | `2026-10-20T06:01:00Z` (`:7`) |

The delivered gate digest for the claimed content is
`fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`
(verified: `git show 32118fc:tools/mado-verify.sh | sha256sum`; also
`evidence/committed-bindings.json` `sha256["tools/mado-verify.sh"]` and the
`gate_sha256` header of `evidence/gate-selftest.txt:4`). Neither `ef50e262…`
nor `d6d5eb27…` is that digest, and the three runs precede commit
`32118fc…` (06:03:28Z per the round-15 erratum).

The *verdicts* the lesson cites are nevertheless exactly what the receipts
record: `killed=10/10`, `4/4`, `8/8` (`:77`, `:46`, `:61`), `CONTROL: GREEN`
(`:10` each), `MUTATE_RESTORE: OK` (`:75`, `:44`, `:59`), receipt `exit=0`
(`:81`, `:50`, `:65`). So this is not a count contradiction: it is the
R16-V1 class of label defect — a receipt cited under a measurement claim whose
own header names a different measured object.

Independent static confirmation of the only relation recoverable from committed
bytes: applying the gate's own `mado_r7_target_build` marker-family deletion
(R7 REGRESSION, R7 SELFTEST, R8 BLOCK) to
`git show 32118fc:tools/mado-verify.sh` yields **117602 bytes**, SHA-256
`cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`, which equals
each receipt's `MUTATE_TARGET` (`:8`) and pristine/restore hash. This was a
deterministic text deletion in Python, not a gate run.

Status: this exact defect is already routed and learned — outside
`corpus/lessons/round-14-verifier-spotcheck.md:169` (R14-V1: "retain
`input_binding: provisional worktree snapshot`, old whole-gate hashes … and no
measured_commit header. … these must not be read as standalone final-full-gate
receipts"), corrected by `corpus/knowledge/gate-standing-use.md:462-500`
(per-receipt header map: 267-assertion target control is not the 372-assertion
full gate; dates precede `32118fc…`), `corpus/lessons/round-15.md:14`, and
`.ufo/waves/round-15/receipt-correction.json`; acceptance recorded at
`corpus/lessons/round-16.md:21` ("R14-V1's explanatory correction was accepted
by outside closure"). It must not be re-routed as a new defect.

### F2 — LOW, scoping precision: the round's provenance audit covered one receipt, so the same class in three cited receipts was never mechanically checked

`corpus/lessons/round-14.md:16` records the rule created this round: "Future
round-14 standalone receipts carry resolved measured commit, raw gate SHA-256,
exact command and observed exit in the receipt itself." That rule is
forward-looking, and the three mutation receipts are **not** a violation of it:
they were written at 05:58:44Z, 06:00:23Z and 06:01:00Z, while the lesson file
carrying the rule has mtime 06:08:41Z and the binding commit `97c3583` is
06:10:29Z. The three also precede commit `32118fc…` (06:03:28Z). So F2 does not
claim an authoring-time breach.

The precision gap is scoping: the round's header audits
(`evidence/provenance-red.txt`, `evidence/provenance-green.txt`, and
`SCORECARD.md:556-560`) examined only `gate-selftest.txt`, while the same
"Exercised verification" section cites three other standalone receipts with no
`measured_commit` (all three) and a provisional `gate_sha256` (two distinct
values, `ef50e262…` and `d6d5eb27…`, neither the delivered gate). The check's
predicate would have flagged them; scoping it to one receipt is why F1 needed
an outside verifier to surface it. R14-V1's correction repairs the
interpretation but does not record this scoping lesson, and
`corpus/QUALITY.md:65`'s R14-V1 paragraph likewise addresses the historical
receipts, not the audit scope. For round 17 this is the directly reusable
"label check shown able to fail" input: iterate the predicate over every
receipt the lesson/SCORECARD cite, using the real round-14 bytes as red and
green cases (see Recommendation).

### F3 — INFO: the R16-V1 fact pattern exists in the round-14 frozen runner but no round-14 citation triggers it

`frozen/verify.py` maps *both* `snapshot_tampered` and `frozen_error` to exit 2
(document string in the file: "2 snapshot_tampered (missing/changed/escaping
input, nothing run); 2 frozen_error (bad expected.json or run could not
start)"). So an exit-2 receipt cannot by itself distinguish tamper from error.
Round 14, however, cites only `frozen_match` (exit 0) from
`frozen-regression.txt:24`, and ships no tampered-input receipt; no round-14
citation misstates a tampered/error verdict. The round-14 analog of R16-V1 is
therefore F1's provisional-header class, not an exit-2 misread, and neither
F1 nor F2 is a new contradiction of a recorded verdict.

## Citation-by-citation result (A2)

Legend: **ok** = the receipt records exactly the cited verdict/exit; **F1** =
verdict matches but receipt header names a provisional object (known).

| # | citation | claim | receipt's recorded verdict | result |
|---|---|---|---|---|
| 1 | `round-14.md:152-154` `before.txt` | U1–U4 4/7, nav 27/27, 0/3, all three case exits 0, receipt exit 0 | `count:4 score:5.7143`; `notes:27 indexed:27`; `detected:0 total:3`; three `overall_exit:0`; `exit=0` (`:248`) | ok |
| 2 | `round-14.md:155-160` `after.txt` | U1–U5 5/7, nav 28/28, 3/3, three case exits 1, facets/reserved/inverse true | `count:5 score:7.1429`; `28/28`; `detected:3 total:3`, `overall_failing_runs:3`; `facets`/`reserved`/`inverse` all true; `exit=0` (`:295`) | ok |
| 3 | `round-14.md:161-164` both | controls: order swap, file-symlink, newline, overlap, direct-missing, zero-match; toggle NOTE/PASS/PASS | `order_detected:true`, `regular_target_retained:true`, `regular_member_transported:true`, overlap `local_inventory FAIL missing: ai-usage.conf`, `unresolved_class_retained:true` ×2; direct PASS / all-directory NOTE / mixed PASS on both revisions | ok |
| 4 | `round-14.md:165-166` `gate-selftest.txt` | 372/372, exit 0, carries measured commit + raw digest | `MADO_SELFTEST: 372/372` (`:6`), `measured_commit: 32118fc…` (`:3`), `gate_sha256: fba82a66…` (`:4`), `exit=0` (`:10`) | ok |
| 5 | `round-14.md:167-169` `gate-file-plane.txt` | 29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0 | `counts: pass=29 fail=0 unknown=0 skip=8 note=4` (`:50`), `MADO_VERIFY: CLEAN (29 pass, 4 notes…)` (`:51`), `exit=0` (`:55`) | ok |
| 6 | `round-14.md:170-175` + `SCORECARD:536-541` mutant `.txt`s | 10/10, 4/4, 8/8 KILLED; GREEN; restore OK; TSVs retain each mutant | `killed=10/10`, `4/4`, `8/8`; `CONTROL: GREEN`; `MUTATE_RESTORE: OK`; `exit=0`; TSVs 10/4/8 rows | F1 (counts ok; headers provisional) |
| 7 | `round-14.md:173-175` derived target | `cd1d73…`; excised R7/R8 machinery out of scope | `MUTATE_TARGET … cd1d73…` in all three; static re-derivation = `cd1d73…` (117602 B) | ok |
| 8 | `round-14.md:176-179` frozen | input digests first; table 10/10; `MADO_REGRESSION: PASS`; `frozen_match`; exit 0; selftest 12/12 | `FROZEN_INPUT … verified` (`:6-7`), `match=10/10` (`:16`), `MADO_REGRESSION: PASS` (`:20`), `FROZEN_ID: frozen_match` (`:24`), `exit=0` (`:28`); `MADO_FROZEN_SELFTEST: 12/12`, `exit=0` | ok |
| 9 | `round-14.md:180-183` contract red/green | exit 1 `FAIL detected=0/3` baseline; exit 0 `PASS 3/3` delivered | `REGULAR_TARGET_CONTRACT: FAIL detected=0/3 revision=873ff08…`, `exit=1`; `PASS detected=3/3 revision=32118fc…`, `exit=0` | ok |
| 10 | `round-14.md:184-187` provenance red/green | exit 1 on unchanged round-13 receipt, missing measured_commit+gate_sha256; exit 0 new | `FAIL missing=measured_commit,gate_sha256`, `exit=1`; `PASS revision+digest+command`, `exit=0`; round-13 file unchanged since `95cbc41` | ok |
| 11 | `round-14.md:188-192` census + counters | both exit 0; W04 S030/S042/S045 retained; 46→50; 42/1/3→46/1/3; 34/8/4→38/8/4 | both `exit 0` with the three W04 lines; `before.txt` rows 46, after 50, tiers/statuses as cited | ok |
| 12 | `round-14.md:193-196` `source-merge.txt` | exit 0, rows=50, collisions=0; rejected/superseding history retained | `PASS registry=… rows=50 … collisions=0 rejected_history=2 supersedes=3 errors=0`, `exit=0` (`:12`) | ok |
| 13 | `round-14.md:197-199` `committed-bindings.json` | binds gate/measure/frozen/spec; gate `fba82a66…` = frozen input; harness `75ed93…` | all 7 digests re-computed with `git show 32118fc:<path>` = recorded; `frozen/gate.sh` = `fba82a66…`; harness `75ed93…` | ok |
| 14 | `round-14.md:200-202` `cleanup.json` | exact selftest dirs emitted by this round's runs, removed | 22 unique paths = the 22 `fixtures kept:` lines across the three receipts, 22/22 absent on disk, recut root absent | ok |
| 15 | `round-14.md:15` (M2) | fleet round-13 report says "byte-identical before/after"; 29 PASS / 0 FAIL / 0 UNKNOWN | fleet `.ufo/reports/round-13/mado.md:68` contains that phrase and count; round-13 `gate-file-plane.txt` `counts: pass=29 fail=0 unknown=0` | ok |
| 16 | `round-14.md:16` (M3) | round-13 `gate-selftest.txt` lacks measured revision/digest header | round-13 receipt has `command`/`cwd`/`stdout`/`exit` only; no `measured_commit`, no `gate_sha256` | ok |
| 17 | `round-14.md:138-141` | `source-bindings-pipefail.txt` binds each fetch with pipefail; tag vs peeled commit distinct | receipt runs `bash -o pipefail -c 'curl … | sha256sum'` ×3, `exit: 0`; `colour-release-binding.txt` lists `refs/tags/1.49` `a8d65d7f…` and `refs/tags/1.49^{}` `ee78491a…` | ok |
| 18 | `round-14.md:12-17` installs | OutputSpec `pacman -S` wlr-protocols `r112.a741f0a-1`; ReviewSourceBar `-Sw` download-only; no other seat install | `w1/reports/OutputSpec.md:10,99` and `ReviewSourceBar.md:48` match; grep of all 32 reports finds no other `sudo`/install line | ok |
| 19 | `SCORECARD:507-509` | both observation probes exited 0; full commands/digests under evidence | `before.txt`/`after.txt` `exit=0`, `command:` and `gate_sha256:` present | ok |
| 20 | `SCORECARD:511-521` table | C1 5.7143→7.1429; C2 0.0000→10.0000; failing runs 0/3→3/3 | exactly the `before.txt`/`after.txt` fields cited | ok |
| 21 | `SCORECARD:516-524` | direct case `default/hypr/windows.conf`; ai-usage control exits 1 via local inventory; order-swap detected; symlink/newline pass; direct-missing/zero-match unresolved; all-directory NOTE | `affected_path` = `…/default/hypr/windows.conf`; overlap `overall_exit:1` + `local_inventory FAIL`; `order_detected:true`; symlink/newline `overall_exit:0`; unresolved retained; toggle NOTE for all-directory only | ok |
| 22 | `SCORECARD:526-531` | nav 27/27→28/28; selftest 372/372 exit 0; prior 310/310 historical | nav fields; `gate-selftest.txt`; round-13 `gate-selftest.txt` `MADO_SELFTEST: 310/310` | ok |
| 23 | `SCORECARD:532-535` | no-live 29/0/0/8/4 exit 0 | `counts:` + `exit=0` | ok |
| 24 | `SCORECARD:542-545` | derived PIN `cd1d73…`; SPEC_SHA `c7ee75…`; gate `fba82a66…` = frozen input | `committed-bindings.json`; frozen receipt `REGRESSION_SPEC … c7ee75… (recorded pin matches)` (`:12`) and `FROZEN_INPUT: gate.sh … fba82a66…` (`:6`) | ok |
| 25 | `SCORECARD:546-550` | frozen `frozen_match` + `MADO_REGRESSION: PASS` exit 0; selftest 12/12; expected.json/bindings bind it | as row 8; `frozen/expected.json` digest = recorded binding | ok |
| 26 | `SCORECARD:551-555` | contract auditor red/green; four new mutants show repaired policy can fail | `contract-{red,green}.txt`; `regular-target-results.tsv` RT1–RT4 all KILLED exit 2 | ok |
| 27 | `SCORECARD:556-560` | header audit red on round-13 receipt, green on this round's | `provenance-{red,green}.txt`, exits 1/0 | ok |
| 28 | `SCORECARD:562-570` | registry 46→50, tiers/statuses, S041 sole mutation, census, merge screen | `before.txt`/`after.txt`; `git diff 873ff08 32118fc -- corpus/SOURCES.md` = 37 insertions/1 deletion, the deletion is S041's used-by cell only (col 11), four appended rows S047–S050 | ok |

Cross-checks performed on the registry and source quotes (beyond receipts,
because the lesson's Gate table cites them directly):

- S047 quote: installed `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml`
  has SHA-256 `65b0f82a…` (equal to the lesson's raw digest and the pipefail
  receipt) and contains "Even if the compositor succeeds to test a
  configuration, applying it may fail." inside the `test` request
  (`:486-487`). Plain file read; no package query.
- S048 quote: installed
  `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml`
  (`18a2678e…`) contains "This luminance range is only theoretical and may not
  correspond to the luminance of light emitted on an actual display." at
  `:1701-1702` in the `target_luminance` event (`:1692`).
- S049 capture: `globals.json` `captured_utc` = `2026-10-20T04:10:03Z`,
  `probe.display_socket` = `wayland-1`, `compositor.version` = `0.56.2` —
  matching the lesson's S049/S041 rows.
- M1 erratum is present in `corpus/knowledge/wayland-protocol-boundaries-r13.md:106-122`;
  U4's broad sentence is quoted and superseded, and S049's row says
  `supersedes S046 — … the diagnostic-binding evidence is unchanged`.
- M4 baseline pointer is literal: `git show 873ff08:tools/mado-verify.sh`
  uses `[ -e "$x" ]` and `compgen -G "$x"` for direct/glob targets
  (`:2420-2423`); `GateRecon.md:14-21` documents those false-greens.

## Verdict

- A1: **one label defect, zero verdict/count contradictions.** Every number,
  exit, marker and population cited by the round-14 lesson and its SCORECARD
  rows reproduces from the cited receipt. The single defect is F1 — the three
  mutation receipts' own headers name a provisional whole-gate object, not
  `32118fc…`/`fba82a66…`.
- A2: 28 citation groups checked; none skipped; TSVs, JSONs, frozen inputs and
  cleanup manifest included.
- A3: F1 is already learned as R14-V1 and corrected in round 15 (accepted by
  the round-16 outside closure). F2 (the round's header audit was scoped to
  `gate-selftest.txt`, so the same class in three cited receipts was never
  mechanically checked) is the only unrecorded precision point; it is a
  scoping lesson, not an authoring-time rule breach and not a new evidence
  contradiction, and it adds no count/axis harm.

## Recommendation for the round-17 label check (C1)

Use the round-14 bytes as the fail-capable fixture rather than a synthetic one:

- Predicate: for every receipt cited by a lesson/SCORECARD row as evidence of
  revision R, (a) if the receipt declares `measured_commit` it must equal R,
  and (b) if it declares `gate_sha256` it must equal
  `sha256(git show R:tools/mado-verify.sh)`; ancillary receipts with no
  `measured_commit` must either declare a derived-target hash that matches a
  statically derived target (as the three do) or be excluded from the claim.
- Red case (real bytes): `evidence/regression-recut.txt:4` `gate_sha256:
  ef50e262…` vs the delivered `fba82a66…` → FAIL; also
  `regular-target-mutants.txt:4` and `retained-census-mutants.txt:4`.
- Green case (real bytes): `evidence/gate-selftest.txt:3-4`
  (`measured_commit: 32118fc…`, `gate_sha256: fba82a66…`) and
  `evidence/gate-file-plane.txt:3-4`.
- Scope lesson: run the predicate over all cited receipts, not just the
  primary selftest receipt — F2 exists only because round 14 scoped it to one.

## Residual risk and verification gaps

- No execution: kill counts, table matches, selftest totals and exit codes are
  taken from committed receipts; I did not replay any gate, harness, frozen
  run, census or mutation sweep.
- S050's quoted TODO line was not re-fetched; it is corroborated by
  `AttackCoverage.md` (sha `148f12d7…`, stub `:352-354`) and by
  `implementation-source-binding.txt`'s digest only.
- The three provisional whole-gate hashes (`ef50e262…`, `d6d5eb27…`) cannot be
  recovered from committed bytes; only their derived target (`cd1d73…`) is
  re-derivable, which is what the round-15 erratum states.
- Semantic review of the U5 knowledge note beyond the M1 erratum and the two
  opened quotes is outside this audit; `AttackCoverage.md` remains authoring
  advice, not independent clearance.
- Host package versions remain as receipts record them (`pacman -Q` lines in
  `colour-source-binding.txt`); I issued no package query this round.
