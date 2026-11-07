# R99MReviewRecords - the round-98 routed repairs and the round-99 record discipline

Seat: R99MReviewRecords (reviewer). Read-only; nothing edited. Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base `2cbaa141f42df9dfeee4d207cae6558a4dd59863`
(branch `master`). Snapshot 2026-11-07T18:26:30-03:00: rev `2cbaa141` plus the working tree
(`M LOG.md`, `M PROVINCE.md`, `M SKILL.md`, `M corpus/QUALITY.md`; `?? .ufo/waves/round-99/`,
`?? corpus/lessons/round-99.md`). `corpus/SOURCES.md` is unmodified. The tree moved while this
review ran (PROVINCE.md gained its round-99 refinement between the first and last check), so every
"open" below is the state at that snapshot, not a prediction.

Method: no lane gate or counter was executed (the spot-check standard; this seat is read-only).
Counts are this seat's own stdlib parser over `git show <rev>:<path>` bytes. The `lsp` device is
not available in this seat's toolset, so caller/definition checks are text/git only and are not
presented as semantic proof. The full command/observation log is
`.ufo/waves/round-99/receipts/review-records-r99.txt`.

## 1. The eight routed defects - status at the snapshot

| # | defect (spot-check section 5) | status | where |
|---|---|---|---|
| D1 | S532 has no registry row | **open** | `corpus/SOURCES.md` ends at S531 (466 rows / 119 entries); the round-99 lesson's Gate table declares S532-S534 (`corpus/lessons/round-99.md:15-17`), and `PROVINCE.md:615` already cites "S532, S533, S534", but no row exists |
| D2 | "466 rows / 119 entries" not the measured state | **open** | no committed receipt of `quality/check-sources-readback.py` at any rev in the wave (`receipts/` holds four files, none a gate run); the LOG erratum is correct but the SCORECARD row is not corrected |
| D3 | `SKILL.md` r98 rows' stale pins | **fixed in the working tree, uncommitted** | `SKILL.md:2980` now pins tool `49f7fecd...` and mutants `32c207b3...`; every pin in both rows re-derived below |
| D4 | `LOG.md` round-98 entry (seed, mistake count) | **fixed in LOG, uncommitted; incomplete** | `LOG.md:4654-4673`; the seed and the M98 count are right, the explanation of the wrong seed is unsupported, and `SCORECARD.md:5590` still carries the wrong seed |
| D5 | the harm watch omits the r97 counters | **not materialised at the snapshot** | no `controls/` dir and no panel at 18:26:30; the C2 panel is a wave deliverable (`R99MExecHarm`), so D5 cannot be judged yet (after the snapshot the build draft `build/harm-watch.py` and `controls/l1-control-naive.py` appeared; the panel and cases still do not exist) |
| D6 | no `QUALITY.md` criterion for M98-1's class | **criterion exists; citation and runnability defective** | `corpus/QUALITY.md:1289-1297` (criterion 170) - class right, pointers wrong, shown-able-to-fail not runnable |
| D7 | report ordering / in-place rewrite (process) | **not testable at the snapshot** | `.ufo/reports/round-99/mado.md` does not exist yet (the fleet-root report dir holds other lanes only) |
| D8 | loose C2 commit attribution | **fixed in LOG, uncommitted** | `LOG.md:4667-4670` names `06b6bf2a` and `020af865`; both halves verified |

## 2. D1 - the S532 row

The registry does not carry it. `grep -c 'S532' corpus/SOURCES.md` is 0; the last registry row is
S531 (`corpus/SOURCES.md:483`), and my parser reads 466 rows / 119 entries at `2cbaa141` (the same
as at `020af865`). The lesson's Gate table (`corpus/lessons/round-99.md:15-17`) declares three rows
(S532 `gio-tool-launch.c`, S533 `gutils.c`, S534 the spec's recognised keys), and the PROVINCE
refinement (`PROVINCE.md:615`) cites all three - so the tree now asserts rows the registry does not
hold. That is D1's own class, one round later.

The S532 material itself is right where it exists:

- URL re-opened by this seat: `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c`
  -> HTTP 200, 3991 B, sha256 `16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a`,
  equal to the lesson's and the fetch receipt's digest.
- The quote is at `:116` (`args = g_list_append (args, g_file_new_for_commandline_arg (argv[i]));`),
  as the lesson says.
- The `used-by` is unspecified: the lesson's Gate table has no `used-by` column, the round-98 entry's
  `source:` line cites S528-S531/S504/S506/S527 (not S532), and no round-99 knowledge entry exists
  (`ls corpus/knowledge | grep -c 'r99|round-99'` -> 0). The spot-check's "used-by the entry" needs a
  named entry; at the snapshot there is none.
- One of the three planned rows has a locator defect: the S533 quote is at `gutils.c:280-281`, not
  `:274-276` (the lesson and the fetch receipt both print `:274-276`). The S532 locator (`:116`) and
  the S534 locators (`:128`, `:130`) are right; the fetch receipt's other gutils locator (`:345-347`
  for the "Use the working dir..." quote, actually `:322`) is a separate defect (section 9.4).

## 3. D2 - the registry gate at the records tip

There is no committed receipt. The wave's `receipts/` holds `connector-sweep-r99.txt`,
`harm-r98c1-at-r99.txt`, `harm-r98c2-at-r99.txt`, `sources-open-r99.txt`; none is a
`quality/check-sources-readback.py` run, and no file in the wave carries a `SOURCES_READBACK:` line
from the gate (the two harm receipts mention the gate only in prose). The `harm-r98c2` note's
"the gate itself is green at the tip (rows=466 entries=119 findings=0)" is a prose claim inside a
counter-replay receipt, not the gate's own output.

My parser reproduces the numbers the spot-check used and shows what a gate run would say:

| rev | rows | entries | findings | detail |
|---|---|---|---|---|
| `35f3ce80` | 462 | 118 | 21 | all R4; 16 rows / 21 pairs (S457, S459, S460, S464, S465, S466, S470, S481, S484, S485, S493, S501, S502, S511, S512, S517) |
| `a3471631` | 462 | 118 | 0 | the round-98 measured revision (matches `c2-measured-r98.txt:33`) |
| `020af865` | 466 | 119 | 0 | the records state |
| `6f61eff0` | 466 | 119 | 0 | the r98 closure tip |
| `2cbaa141` | 466 | 119 | 0 | this round's base |

So the gate would be green at 466/119, but "would be" is not a committed receipt, and the spot-check
asked for the receipt. Two further record problems:

- `SCORECARD.md:5591` still says "gate findings 0 over 466 rows / 119 entries" while its own counting
  command pins `--rev a3471631...` (462/118). The row's text disagrees with the row's own command;
  the LOG erratum (`LOG.md:4671-4673`) corrects the LOG entry only and says "the numbers are not
  rewritten here", leaving the SCORECARD row untouched.
- Forward arithmetic: the lesson declares S532-S534, so the records tip after the D1 repair has
  469 rows (entries stay 119 unless a round-99 entry lands). The LOG erratum's "466 rows / 119
  entries is the records state" becomes stale the moment those rows land; the D2 receipt must report
  the post-repair count, not 466.

## 4. D3 - the two r98 rows' pins

Both rows re-derived against the committed artifacts at `2cbaa141`, `6f61eff0`, `a3471631` and
`020af865` (all four agree):

| row | flag | row value | committed sha256 | verdict |
|---|---|---|---|---|
| `mado-r98-execargv` (`SKILL.md:2980`) | `--expect-cases-sha256` | `21cccc3a...e370e` | `21cccc3ad94e99dff9cdb281a38b32579e9d3e6be14799a83b09499e466e370e` | ok |
| | `--expect-mutants-sha256` | `32c207b3...53bb` | `32c207b32d8aa6126ee949383e7ab992f53c76369310a3e7d88c2b6240ce53bb` | ok (was `5f074f70...`) |
| | `--expect-genseed-sha256` | `b7bc137a...357c` | `b7bc137a643c771f1cd88a3909d1650205b37a155869ade84adc419e3515357c` | ok |
| | `--expect-tool-sha256` | `49f7fecd...f713` | `49f7fecdc3bef99a077fe73ac12f5fe211d7ae8c41df5ddc949daf685405f713` | ok (was `acfcc4f7...`) |
| | `--expect-gio-sha256` | `d2164260...c462` | `/usr/bin/gio` `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` | ok |
| | self-test `checks=16` | 16 | `.ufo/waves/round-98/receipts/review-c1-r98.txt:49` prints `checks=16 failed=0 rc=0` | ok |
| `mado-r98-sources-readback` (`SKILL.md:2982`) | `--expect-gate-sha256` | `f1000bf1...d8f5` | `f1000bf11e88149695aa96229fcf2155929ebbb72a2cfa215d8c24e2f37bd8f5` | ok (already correct at r98) |
| | `--expect-base-mismatches 21` | 21 | my parser: 21 R4 at `35f3ce80` | ok |
| | self-test `checks=18` | 18 | `c2-readback-r98-measured.txt:17` prints `checks=18 failed=0` | ok |

The pins also equal the round-98 freeze block (`claims-declaration-r98.md:282-288`). D3 is fixed in
the working tree; it is not committed, so a reader at `2cbaa141` still sees the stale row.

## 5. D4 - the LOG round-98 correction

Right: the measured seed is `f00d3edcdb285ac0`. The receipt has always printed it (one commit,
`020af865`; two occurrences), and `LOG.md:4660-4664` names it. Right: the mistake count is 12
(`grep -c '^\*\*M98-' corpus/lessons/round-98.md` -> 12), and `LOG.md:4665-4666` says so.

Not right: the correction's explanation that `e2bf4d1b757e2e7b` "is the generator's *input* seed
line". The generator's stdout is `FRESH_GEN: cases=N ok=A refused=B` plus a `FRESH_GEN_PIN` line -
there is no seed line; the counter prints `fresh_seed=<the same hex it passes as --seed>`
(`quality/counters/c1-r98-execargv.py:1088-1101`). The string occurs nowhere in the round-98 wave
except the LOG entry and the SCORECARD row; `git log -S` shows it entered the tree at `020af865` in
`LOG.md` and `SCORECARD.md`, never in a receipt. The honest correction is "the value is unsourced;
the measured seed is f00d3edc", not a provenance story.

Also not fixed: `SCORECARD.md:5590` still says "fresh 60/60 at seed `e2bf4d1b757e2e7b`". The LOG
erratum does not mention the SCORECARD, and the spot-check's D4 named the LOG entry while its
section 2 C1 table used the measured seed. The wrong value survives in a second record.

## 6. D6 - the QUALITY criterion for M98-1's class

Criterion 170 exists (`corpus/QUALITY.md:1289-1297`) and names the right class ("an instrument race
mistaken for a model rule"; the round-98 lesson's M98-1 is "instrument race mistaken for a model
rule", `corpus/lessons/round-98.md:11-26`). Three defects remain:

1. **Wrong section pointer.** The criterion says "the round-98 lesson's `## Gate` ... carry the
   corrected rule". The round-98 lesson's `## Gate` (`:151-198`) holds registry rows, rows touched
   and candidates; the corrected rule is in `## Mistakes` M98-1 (`:11-26`), whose Fix sentence is
   the append-only-record rule.
2. **Dangling pointer.** The criterion says "the round-99 entry's `## 12. Named limits`". No
   round-99 knowledge entry exists, and the round-98 entry's Named limits is `## 13. Named limits`
   (`corpus/knowledge/gio-exec-argv-r98.md:620`), not `## 12` (`:461` is `## 12. Measured probes`).
3. **Not runnable.** The "Shown able to fail" is narrative ("with one `probe.sh.out`, `%f` + `a,b,c`
   reads `A1=c.txt` ...") with no command, file or revision. Criteria 168 (`:1266`) and 169 (`:1276`)
   both carry exact commands; the round-98 lesson's M98-1 evidence names
   `.ufo/waves/round-98/receipts/control-naive-r98.json` run 1 and probe3, which the criterion could
   cite. The house bar (QUALITY criteria 2 and 6) requires a measured anchor and a re-derivation
   command.

Criterion 171 (M99-1) is better: it cites `lessons/round-99.md#mistakes M99-1` (the file exists,
untracked) and names both old and new values. Its shown-able-to-fail - and the lesson's M99-1
"Shown able to fail" it mirrors - uses `git show master:...`, a moving ref, where the house style
pins a revision; minor.

## 7. D8 - the C2 commit attribution

The erratum (`LOG.md:4667-4670`) names both commits, and both halves check out:

- `06b6bf2a`: `corpus/SOURCES.md` 16 insertions / 16 deletions - the 16-row / 21-path `used-by`
  repair (the 21 pairs over 16 rows are exactly the base R4 set my parser finds at `35f3ce80`).
- `020af865`: `corpus/SOURCES.md` gains the S504/S506/S527 `used-by` cells and the four new rows
  S528-S531, and `corpus/knowledge/gio-exec-argv-r98.md` (690 lines) lands.

The erratum's own re-derivation command
(`git log --oneline 06b6bf2a..020af865 -- corpus/SOURCES.md corpus/knowledge/gio-exec-argv-r98.md`)
prints only `020af865`; it proves the second half, not the first. A second command
(`git show --stat 06b6bf2a -- corpus/SOURCES.md`) is needed for the first half. Minor.

## 8. Remaining disagreements with the spot-check's own text

- **D4's sentence.** "The fresh seed is `e2bf4d1b757e2e7b`, but the receipt and the report say
  `f00d3edcdb285ac0`" reads as if the first value were the seed. The measured seed is
  `f00d3edcdb285ac0`; `e2bf4d1b757e2e7b` is an unsourced value in `LOG.md` and `SCORECARD.md`. The
  round-99 correction fixes the value but invents a provenance for the wrong one (section 5).
- **D2's three documents.** The spot-check names the report, `SCORECARD.md` and `LOG.md`. The LOG
  erratum addresses the LOG only; `SCORECARD.md:5591` still asserts 466/119 at a row whose command
  pins `a3471631` (462/118), and the report (fleet root) is untouched.
- **D5's first-run claim.** "Both present in the 28-leg first run" is right (28 `LEG` lines in
  `harm-base-r98.txt`, the two ids at lines 27-28). But the round-99 declaration's C2 "before"
  says the two "were noticed only by the outside spot-check"; the committed
  `harm-final-r98.txt:41-42` already names `r97c2_counter_selftest`'s omission, and that note landed
  at `fa4445af`, before the spot-check `2cbaa141`. For `r97c1_filetype` the spot-check is right; the
  sentence is half wrong.
- **D1's "the report says four rows"** reproduces: the LOG entry says 462 -> 466 rows (S528-S531).

## 9. New record defects in this round's own artifacts

1. **Declaration R4's line citation is wrong.** `claims-declaration-r99.md:45` cites
   `gdesktopappinfo.c:3116-3126` for `g_spawn_async_with_fds(info->path, ...)`; that range is the
   `gio-launch-desktop` wrapper path and the `wrapped_argv` construction. The spawn call is at
   `:3134`. The rule's semantics are right; the citation is not.
2. **Declaration R7's line citation is wrong.** `claims-declaration-r99.md:50-51` cites
   `gutils.c:352-356` for the `!IS_DIR` half; the load-gate `IS_DIR` test is at `:340` (the PATH-walk
   test is at `:487`), and `:352-356` is the absolute/relative return block.
3. **A declared refusal cause the contract cannot carry.** `claims-declaration-r99.md:48` declares
   the cause `cwd-failed`. The C1 CLI contract's cause list (Shared contract 1) is `load`,
   `no-terminal`, `program-not-found` plus the r98 `no-exec`, `desktop-file`, `exec-parse`; the
   oracle's error map (Shared contract 2) has no `cwd-failed` entry. A `Path=`-unenterable case
   cannot be represented in the case file's `expect.error` vocabulary. Either the contract or the
   rule must change before the freeze.
4. **The fetch receipt's gutils locators are wrong.** `sources-open-r99.txt:35` cites `:274-276` for
   the "Locates the first executable..." quote (it is at `:280-281`); `:36` cites `:345-347` for
   "Use the working dir as program path if provided" (it is at `:322` and `:479`). The lesson's S533
   row inherits the first error.
5. **The fetch receipt's locator claim is false for two files.** `sources-open-r99.txt:4-5` says the
   bytes are committed under `.ufo/waves/round-99/fetch/`; `gdesktopappinfo.c` and `gshell.c` are
   only in `.ufo/waves/round-98/fetch/` (hashes match the receipt). The round-99 fetch dir holds
   four files, the receipt lists five.
6. **An unlisted duplicate fetch.** `.ufo/waves/round-99/fetch/spec-terminal-path.html` (24174 B,
   sha256 `7bc0b640...c03d9`) is byte-identical to `spec-recognized-keys.html` - the same URL under a
   second name - and has no line in the fetch receipt. The receipt must account for every file in
   its own fetch dir.
7. **The round's own probe evidence aliases two cases.** `.ufo/waves/round-99/probe/c2/out.txt`
   (mtime 18:12:35.560) holds the c4 `h.desktop` record: `GDF=.../probe/c4/work/h.desktop`, and
   `c4/work/h.desktop` was written at 18:12:35.556. The c2 case's own desktops (`a.desktop`
   `Terminal=true`, `b.desktop` `Exec=nosuchprog-xyz %f`) have no surviving record. A shared sink
   overwrote one case's observation with the next - the M98-1 class in the round that writes
   criterion 170. `c1/out.txt` is a clean c1 record.
8. **The lesson's Gate rows and PROVINCE cite rows the registry does not carry.** Covered under D1;
   recorded here because the PROVINCE refinement (`PROVINCE.md:615`) is a second artifact asserting
   S532-S534.
9. **The SCORECARD r98 rows carry both stale values.** `SCORECARD.md:5590` has the wrong seed;
   `:5591` has the 466/119 claim at a row whose command pins `a3471631`. Neither is corrected by the
   round's erratum.
10. **The C1 replay receipt has no command header.** `harm-r98c1-at-r99.txt` is six lines of output
    (`rev=...` ... `rc=0`) with no argv, pins or scratch root; the C2 replay receipt
    (`harm-r98c2-at-r99.txt`) carries its command in a header. The C1 receipt cannot be re-run from
    its own text (QUALITY criterion 6/10). Minor.
11. **A precision issue in the C1 claim.** `claims-declaration-r99.md:24-26` says no lane tool
    answers "the post-prepend `argv[0]` program lookup". `tools/mado-mime.py` already models
    `g_find_program_for_path` at the base (`:45`, `:467`) for the default-application resolver. The
    composite launch-environment surface is new; R6's primitive is not. The claim should say the
    composite, not the primitive.

Verified correct in the declaration (not defects): R1 `:1976-2004` (call at `:1993`), R1b
`:1946-1960` (Path read, then TryExec, then Exec - the order claim holds), R2 `:2765-2778` (12
`known_terminals` rows), `:2797-2806`, `:2814-2830`, `:3027-3032` (message at `:3032`), R3
`:3053-3084` (test at `:3066-3068`, lookup at `:3077`; the message is at `:3093`), R5 `:3036-3040`,
R6 `gutils.c:300-500` (default PATH `/bin:/usr/bin:.` at `:388`, empty entry at `:469-476`,
`working_dir` join at `:479-484`). The declaration's `Assimilation: none` resolves to the external
root the round prompt names (`/home/vgpnk/Projects/shokuknow/merge/mado/`), which exists;
`MERGE-REPORT.md` has no launch/terminal/`Exec` mention and the closest staged entry
(`uwsm-app-daemon-unit-r7.md`) is the systemd unit plane, so the claim checks out. The connector
sweep's counts reproduce for four sampled lanes (audio 53/18, kaidoku 779/184, tsukuroi 573/106,
kotodama 31/0).

## 10. Residual risk and verification gaps

- **Snapshot, not closure.** D5 (the C2 panel), D7 (the report) and the C1/C2 counters, cases and
  panel are wave deliverables that did not exist at 18:26:30; their record discipline cannot be
  judged from this review. The tree also moved during the review (PROVINCE.md, then the C2 build
  draft `build/harm-watch.py` and `controls/l1-control-naive.py`; the C2 panel and the C1 cases are
  still absent), so a later reader must re-run the checks against the landed tip.
- **No gate execution.** The D2 counts are my parser, not the gate's output. They reproduce the
  round-98 receipt's 462/118/21 and the spot-check's 466/119, but a committed gate receipt is still
  the only artifact the spot-check's D2 accepts.
- **The records tip does not exist yet.** The D3/D4/D6/D8 repairs are uncommitted; D2's receipt
  cannot be at a committed tip until the L1 lands them, and the S532-S534 rows change the row count
  (466 -> 469) that the receipt must report.
- **The D1 repair is the load-bearing one.** Until S532-S534 land in `corpus/SOURCES.md`, the
  lesson's Gate table and `PROVINCE.md:615` cite ids the registry does not hold; the gate's R5 rule
  would flag them only if a knowledge entry cited them, so the registry census is the check that
  must catch it.
- **The probe aliasing (9.7) is a process risk, not just a record one.** The round's own C1 evidence
  is a shared sink; the counter's case file and the oracle must not inherit that pattern (the
  contract's oracle appends one record per spawn, which is the right shape).
