# RcHarnessFailClosedCheck1343 — a3w2 recheck of CapHarnessFailClosedCheck1343

Scope: independently re-derive the C2 ledger line seat CapHarnessFailClosedCheck1343 wrote
(report `/.ufo/waves/round-25/a3w1/reports/CapHarnessFailClosedCheck1343.md`) for the
SCORECARD capability row `harness fail-closed check` at base `41cc04c8`.

## Method

1. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md` — row and
   context read directly at base revision.
2. Own sandbox clone, `GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE` unset:
   `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapHarnessFailClosedCheck1343`
   then `git checkout -q --detach 41cc04c8`.
   `HEAD=41cc04c8d593837a0d5078bffaacdaa163d12897`, `git status --porcelain` count 0,
   `unshare --user --map-root-user true` exit 0.
3. Demonstration run from clone root:
   `timeout 600 prlimit --as=4000000000 bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/isolate.sh`
4. Literal-placeholder probe:
   `timeout 600 prlimit --as=4000000000 bash .ufo/waves/round-20/isolation-check.sh HARNESS`

## Re-derived observations (all first-hand)

- Row text at SCORECARD.md:1343 verbatim as quoted by the seat:
  `| harness fail-closed check | Show whether a stub/namespace harness runs its payload after any of six forced setup failures | \`bash .ufo/waves/round-20/isolation-check.sh HARNESS\` (\`evidence/crit29-*.txt\`) | 20 |`
  under `### Capabilities (round 20)` — heading actually at line **1338**, not 1337
  (1337 is the preceding blank line; trivial prose off-by-one in the seat's context note).
- `git show 41cc04c8:SCORECARD.md | sha256sum` =
  `6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08`, `wc -l` = 1618 — matches seat.
- Worktree bytes at base: `isolation-check.sh` = `f7aa051faee522f3…` and `isolate.sh` =
  `89125ff7191f0d9179…` — byte-equal to the seat's figures.
- Demonstration run: exit **0**; six modes all `FAIL_CLOSED` (mount-nonzero, unshare-refused,
  mount-noop, partial-arm, missing-target, missing-stub); positive control prints
  `harness exit: 0; canary=present; execution-witness=present` then `POSITIVE_CONTROL_OK isolate.sh`;
  output framed by the same SCOPE lines. Line count = 58 stdout lines, matching the seat.
- Literal `HARNESS` probe: `COULD_NOT_EVALUATE HARNESS (harness path does not resolve)`, exit **2** —
  confirms the seat's substitution note (row's `HARNESS` is a placeholder; the documented argv
  binds `.ufo/waves/round-20/isolate.sh`).
- Evidence glob at base resolves to `crit29-isolate.txt` (v2 tool `2bf115db…`, `exit=0`,
  `POSITIVE_CONTROL_OK isolate.sh`, measured_commit `28c68378…`) and
  `crit29-inns-r19-shape.txt` (FAIL_OPEN negative, tail `exit=1` — the seat's
  "`CHECK_EXIT inns-r19-shape.sh=1`" is a paraphrase of the receipt's `exit=1` line, not verbatim).
- `a2/evidence/iso/crit29-isolate.txt` at base records `tool_sha256=f7aa051f…` =
  the base checker bytes, `measured_commit=a8960de…`, `exit=0` — seat's version-chain argument holds.
- `git log` for both scripts: v3 `f8576f7`, v2 `28c6837`, initial `f3da504` — matches seat.
- Supersede scan: preamble at line 1570 ("This table supersedes the implied `works` of every
  earlier row; the earlier rows stay as written."); round-24 status-table row at line **1583**
  `| harness fail-closed check | works | six forced setup failures classified, POSITIVE_CONTROL_OK isolate.sh, at 8e5d9369 |`;
  scope note at 1589–1598 confirms the 12-row Capabilities population. Seat's pointer
  `SCORECARD.md:1583` is correct; round-24 `works` and this re-run's `works` agree.
- Cleanup: zero `/tmp/mado-isolation-v3-check.*`/`-observer.*` leftovers, zero surviving
  processes (`pgrep`), clone deleted (`ls -d` → No such file or directory).
  No packages/services/config/compositor touched; no tool installs.

## Diff vs seat report

- Seat heading-line note "1337" vs actual 1338 — cosmetic prose slip, not in the ledger line.
- Seat paraphrased the inns receipt tail as `CHECK_EXIT …=1`; actual tail is `exit=1` — semantics correct.
- No copied-not-run evidence found: every quoted output line (six FAIL_CLOSED verdicts, positive
  control, COULD_NOT_EVALUATE text, exit codes) re-derives byte-for-byte under a fresh clone;
  transcript temp-dir names differ (`mado-isolation-v3-check.VbkOQX` vs `UpTKh0`), consistent
  with separate real runs, not reuse of the seat's captured text.
- No wrong-revision evidence: base `41cc04c8` exercised; superseding pointer is the correct
  round-24 row at a later revision, correctly labelled as superseding rather than the measured rev.
- No overclaim detected: the ledger line reports `works`, exit 0, six FAIL_CLOSED modes,
  POSITIVE_CONTROL_OK — all observed. The seat's own risk note (SCOPE line: fail-closed setup
  only, not containment) appropriately bounds it.
- No missed superseding text found in the retire/withdraw/supersede scan: no later row retires
  or contradicts this capability beyond the round-24 `works` row the seat cited.

## Verdict

RECHECK CapHarnessFailClosedCheck1343: agree — ledger line re-derives cleanly at 41cc04c8
(exit 0, 6/6 FAIL_CLOSED, POSITIVE_CONTROL_OK isolate.sh, execution-witness=present;
literal HARNESS form exits 2; superseding SCORECARD.md:1583 round-24 row correctly cited).
Only nits: heading actually at line 1338 (seat wrote 1337); inns tail paraphrased as
`CHECK_EXIT …=1` where the receipt literal is `exit=1`. Neither affects the ledger verdict.
