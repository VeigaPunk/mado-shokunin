# AttackLessonM1M3 — round-17 wave-2 falsification of lesson rows M1, M3, M4, M5

Seat: `MadoR17.AttackLessonM1M3` (leaf reviewer). Date 2026-10-20.
Target: `corpus/lessons/round-17.md:15-18` (§ Mistakes rows M1, M3, M4, M5)
at lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`.
HEAD moved to `f71ccbe` during the review (L1 wave-2 corrections); every
finding below is re-checked against that commit in the
[Post-review HEAD move](#post-review-head-move-f71ccbe) section.

Read-only. No commits, no git/jj mutation of the lane, no delegation, no
transcripts read (my item names none), no package/service/compositor/input
probe. **Installs: none.** Mutation tests ran only on a copy at
`/tmp/mado-r17-m3`; synthetic tripwire inputs are new files under `/tmp`
scanned with the shipped `--scan` mode.

What I resolved per row: every path/revision/anchor in the evidence and fix
cells; the captured-by names; and whether each fix has a receipt that shows
it failing. I reran `label-check.py`, ran `measure.py` at five revisions,
built the `/tmp` git copy of the corpus and exercised the four claimed
measure tightenings (including the legacy-path pin), and scanned synthetic
transcripts with `tools/mado-tripwire.py`.

## Outcome

| row | evidence pointers | captured-by | fix shown able to fail, with a receipt | verdict |
|---|---|---|---|---|
| M1 | all resolve | accurate | yes (`label-check.txt`, rerun identical) | **attack failed** — no broken pointer found |
| M3 | all resolve | accurate | **no** — "tightenings shown to bite" has no receipt; the two baseline receipts predate the tightened instrument and record no more than counts | 2 findings (F5, F6) |
| M4 | all resolve | partly accurate | **no** — the stated enforcement is blind to the install channels the wave itself permitted; "at dispatch" is contradicted by the only reminder records | 2 findings (F1, F2) |
| M5 | all resolve (numbers verify) | accurate | **no** — "Report" has no referent at HEAD; the re-measure has no command and no receipt | 3 findings (F3, F4, F7) |

All report references above resolve **in the worktree**. None of the
`w1/reports/` files is tracked at `988b858`; see F9.

At `f71ccbe`: F1 is addressed by the new M4 wording, F9 is resolved (149
report files tracked), and M1's exit-code wording is stale against the
hardened checker — see the Post-review section. F2-F7 stand unchanged.

## Findings (severity-ranked)

### F1 (high, M4) — "whether any seat ran a package command is checked by the C3 tripwire" is false for five installer channels, including the two the wave-1 context authorised

Row claim (`round-17.md:17`): *"Whether any seat ran a package command is
checked by the C3 tripwire over the round-17 transcripts, not asserted."*

Counterexample, executed against the shipped tool:

```text
$ cat /tmp/mado-r17-tripwire-only-installers.jsonl   # 5 bash toolCall records
npx cowsay hi
uv tool install ruff
pip install requests
npm -g install typescript
cargo install fd-find
$ python3 -I tools/mado-tripwire.py --scan /tmp/mado-r17-tripwire-only-installers.jsonl
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, ... "findings": []}
exit 0
```

A transcript containing five package-manager installs is labelled `clean`.
The same file with `sudo pacman -S cowsay` and `pacman -Q waybar` added does
flag them (`host_mutation` 2, `package_query` 1), so the blind spot is
specific, not a broken invocation.

Code anchors: `tools/mado-tripwire.py:41-43` (`CLASSES` unchanged),
`:72-76` (`HOST_MUTATION_BINS`, `PACKAGE_QUERY_BINS = {expac, pactree,
checkupdates, pacman-conf}`, `LIVE_PROBE_BINS`); `grep -n
"npx\|uv\|pip\|npm\|cargo" tools/mado-tripwire.py` returns **0** lines.
`classify_segment()` returns no finding for an unrecognised argv0.

Why this is not hypothetical for this round: the wave-1 context itself
authorises those channels —
`gen_w1.py:21` / `w1/spec.json .context` line 11: *"you may install or
upgrade tools that help the task — read RULES.md first; but all pacman
transactions are paused, so use only uv tool / npx / an official release
binary in ~/.local/bin"* — and the row's own cited evidence says the
tripwire cannot see them: `w1/reports/SentinelHostPause.md:45-51` (H2)
lists `npx`, `uv tool install`, `uv run`, `pip install`, `cargo install`,
`npm -g` as uncovered and states *"The transcript then shows only `npx foo`,
which C3's tripwire classifies as clean."* `w1/reports/SentinelHostPause.md:129`
repeats the same list as "unclassified".

The wave-1 `clean` receipt (`evidence/tripwire-r17-w1.txt`: 70 files,
counts 0/0/0, exit 0) therefore supports only "no pacman/sudo/… class hit",
not "no seat ran a package command". The M4 fix cell should say the latter,
or the tool should classify those channels.

### F2 (medium, M4) — "L1 sent a binding reminder to all 70 seats at dispatch" is not evidenced, and the reminder records that do exist place it mid-wave

Row claim (`round-17.md:17`): *"L1 sent a binding reminder to all 70 seats
at dispatch."*

- The artifacts that place the reminder in time put it **mid-wave**:
  `w1/reports/SentinelHostPause.md:35` (H1) — *"L1 had to send a mid-wave
  IRC reminder. That shows the spec text alone was not trusted to hold."* —
  and `w1/reports/CriticC3.md:141` — *"L1 had to countermand it by IRC."*
  A third report acknowledges a reminder without a time
  (`w1/reports/TamperRecut.md:60`: *"HOST PAUSE observed; L1 reminder
  acknowledged"*). None of the three places it at dispatch.
- The dispatch-time text is a shared context paragraph: `w1/spec.json`
  context line 10 `HOST PAUSE (binding): ...` (identical to
  `w1/dispatch.json .taskCall.context`; the 70 prompts in `.items` do not
  carry it — 0/70, and 0/70 contain "Tooling directive"). It is a pause
  paragraph, not a "reminder", and the very next context line (11) grants
  the `uv tool / npx` install permission above.
- No receipt is cited in M4's fix cell for this claim.

If "binding reminder" means the IRC countermand, "at dispatch" is false by
the cited report's own sentence; if it means the context paragraph, the
claim is true by construction but mis-described, and H1 says that text
alone was not trusted to hold. Either way the fix is not shown able to
fail with a receipt.

### F3 (medium, M5) — "Report ... say" has no referent at HEAD

Row claim (`round-17.md:18`): *"Report and SCORECARD say: the pause is an
instruction to lanes; ... R15-V1's current host state is `[UNK]` ..."*

`SCORECARD.md:892-895` does say all of that (verified). The **Report** does
not exist:

- `.ufo/reports/round-17/` contains `kagi.md, kaidoku.md, kake.md,
  kasegi.md, kotoba.md, kotodama.md, kumitate.md` — **no `mado.md`**.
- The lane's only round-17 report artifact is
  `.ufo/waves/round-17/drafts/ReportSkeleton.md`, whose line 105 is
  `- Host-wide pause in force: {{PAUSE_STATE}}.` — an unfilled placeholder.
  `w1/reports/CriticHonesty.md:42` confirms the slot is still to be filled
  at close.

So the row cites a source that does not yet say the sentence. If the intent
is prospective it must read "the report will state", and it still is not a
fix with a failure receipt.

### F4 (medium, M5) — the round-window re-measure has no command and no receipt

Row claim (`round-17.md:18`): *"the round-window count is re-measured at
close."* No command is given and no close receipt exists at HEAD.

The 13-count in the evidence cell is reproducible
(`sed -n '2440,3152p' /var/log/pacman.log | grep -c 'PACMAN] Running'` →
13), but QUALITY 10 (`corpus/QUALITY.md:16`) requires each count as
`<n> — <command> <date>`; the row gives `<n>` and a file/line range only.
`w1/reports/CriticHonesty.md:42` says *"Re-measure `<n>` at close with the
same grep"* but the lane contains no such grep line. At HEAD the fix is an
open promise, not a shown-to-fail mechanism.

The rest of F4's evidence cell verifies exactly:
`/var/log/pacman.log:2440-3152` contains 13 `[PACMAN] Running` lines from
07:45:36 to 09:39:21 on 2026-10-20 (lines 2440, 2448, 2454, 2461, 2462,
3064, 3085, 3091, 3092, 3125, 3126, 3132, 3152; all inside the range),
including the 09:15:30 `-Syu` with
`mkinitcpio 41.1-1 -> 42.2-1` (:2539), `hyprland 0.56.2-2 -> 0.56.2-4`
(:2733) and `linux 7.2.3.arch1-3 -> 7.2.11.arch1-1` (:2855). The file ends
at 09:39:21 (line 3160), so "0 lines from round launch 10:51 to
measurement" holds (launch 10:51:22 is itself receipted by
`w1/reports/CriticHonesty.md:18`). `CriticHonesty.md:18-26,40` and
`CriticC3.md:43-50` are the real capturers of this defect — captured-by is
accurate.

### F5 (medium, M3) — "Tightenings shown to bite" has no receipt; the cited baseline receipts predate the tightened instrument

Row claim (`round-17.md:16`): *"Instrument committed and bound before
integration (`f52f43f`, tightened `ab0bc9b`, sha256 `4023124f…`); baseline
2/6 re-measured with identical bytes at both. Tightenings shown to bite:
exact `surface: P<n>` line, pinned legacy paths, upstream-row surface
relevance, facet floor."*

The claim is **true in code** (anchors: exact-line T2 at
`measure.py:186-187`; pinned legacy T3 at `:126-141,267`; upstream
relevance T4 at `:132-133,242-246`; facet floor T5 at `:141,203`), but
nothing in the lane shows it biting:

- `evidence/measure-before.json` (rev `27cd06f`) and
  `evidence/measure-instrument.json` (rev `f52f43f`) are identical apart
  from `rev`/`commit` (verified by diff) and contain only C1/C2/C3 counts;
  neither contains a mutant case or a rejection. Both have mtime
  `11:11:09`, while `measure.py` has mtime `11:11:32` and commit `ab0bc9b`
  is `11:11:36` (`git log --format='%ci'`); the receipts therefore can only
  have been produced by the `f52f43f` instrument (`a280b3ab…`), never by
  `4023124f…`.
- "At both" in the sentence can only bind to the two instrument commits
  named in the same sentence (`f52f43f`, `ab0bc9b`); the two receipts are
  at `27cd06f` and `f52f43f`, so neither is a run of `ab0bc9b`.
- The only mutant probes in the lane are in
  `w1/reports/RevRubricV.md:13` (counter sha `7e37b6bc…`, 250 L) and its
  §3 V1-V3, i.e. probes against the **pre-tightening** counter showing the
  holes (multi-surface line credits six provinces, empty skeleton passes,
  metadata-only entries credit), not against the shipped tightened code.
- Neither receipt records the instrument sha256, so even the revision
  binding cannot be checked from the receipt alone.

I ran the four tightenings against `measure.py` sha `4023124f…` in
`/tmp/mado-r17-m3` (base: 4/6, `P1,P2,P4,P6`):

| mutant | result |
|---|---|
| `surface: P4 (terminal)` | 3/6 `P1,P2,P6`; rejected: "surface line must be exactly `surface: P<n>`" |
| `surface: P4 P6` | 3/6 `P1,P2,P6`; same MALFORMED rejection |
| idle `## Safe observation` cut to 2 non-empty lines | 3/6 `P1,P2,P4`; rejected: "sections under content floor: ## Safe observation" |
| terminal note source line reduced to S059 only | 3/6 `P1,P2,P6`; rejected: "no cited mined tier-A row is an upstream https source of kind docs/spec/code naming the surface" |
| both pinned P1 entries removed + a new `covers: U1` entry joined to S002 | 3/6 `P2,P4,P6`; the unpinned legacy entry earned no P1 credit (pin bites) |

So the fix is demonstrably able to fail — but the demonstration is not in
the lane, and M3's fix cell cites no receipt for it. This is the one
requirement of the assignment the row does not meet.

Baseline binding: rerunning the current `4023124f` instrument at `27cd06f`,
`f52f43f` and `ab0bc9b` yields 2/6 (`P1,P2`) each, and at `a9998d1` yields
4/6 (`P1,P2,P4,P6`); `measure-c2.json` at `a9998d1` matches. So no score
error — but the claim "baseline 2/6 ... at both" is not receipted for the
tightened instrument. SCORECARD's correction adds the same unbound sentence
(`SCORECARD.md` appended bullet: *"Stricter only; baseline stays 2/6 under
both (evidence/measure-before.json, measure-instrument.json)"* — both are
the `f52f43f` instrument).

### F6 (low, M3 residual) — the declared "(new entries)" clause is still not implemented

`SCORECARD.md` at `0175f13:848` declares the surface form for **new
entries** (`surface: P<n> (new entries)`). `measure.py` has no
baseline-existence check: any entry entering the `surface:` path is
credited, including a pre-existing one. `w1/reports/RevRubricV.md:67` (V1)
named this blocking. The four listed tightenings narrow the exploit (T4
upstream-relevance blocks the V1 example pairs [INFERENCE from
`measure.py:242-259` + the S051/S052 and S013-S015 rows]; SOURCES has no
walker/elephant/theme/wallpaper upstream row today, so P3/P5 cannot be
reached this way) but do not implement the declared clause. M3's row claims
only "stricter", so this is a residual mismatch, not a false statement in
the cell; it means the corrected instrument is still not the declared one.

### F7 (low, M5) — the cited line range ends mid-transaction

`/var/log/pacman.log:2440-3152` ends at line 3152, the `[PACMAN] Running`
line of the 09:39:21 `-Rns`; its completion lines are 3153-3160. The
13-run count and the 07:45-09:39 span are unaffected (all 13 start lines
are inside the range), but a reader checking "the range ends where the last
transaction ends" will not find it. No numeric error.

### F8 (informational, M1) — "outside `round-16-verifier-spotcheck.md` R16-V1" is ambiguous but resolves

`corpus/lessons/round-16-verifier-spotcheck.md:164-172` contains R16-V1 and
explicitly names `lesson round-16 l.131`; the defect is therefore *inside*
that R16-V1, not outside it. The only reading that fits is "recorded
outside this lesson, in the spotcheck". Not a broken pointer; a wording
risk for a future reader.

### F9 (low, M3/M4/M5 durability) — the cited seat reports are untracked at 988b858

`git ls-tree -r --name-only HEAD -- .ufo/waves/round-17/w1` returns only
`dispatch.json`, `record.json`, `spec.json`. The six report files the rows
rely on — `w1/reports/SentinelHostPause.md` (M4 evidence),
`w1/reports/CriticHonesty.md` and `w1/reports/CriticC3.md` (M5
captured-by), `w1/reports/RevPreRegistration.md`, `w1/reports/CriticC2.md`
and `w1/reports/RevRubricV.md` (M3 captured-by) — are untracked
(`git status`: `?? .ufo/waves/round-17/w1/reports/`), as are
`gen_w2.py` and `w2/spec.json` (M4's wave-2-context fix). A clean checkout
of the reviewed commit cannot resolve any of them; only the worktree can.
QUALITY 13 (committed path, or quoted lines + sha) is the lane's own rule
for evidence that outlives a round. If the reports are committed at close,
this closes; at `988b858` it is open. No on-disk file is missing.

## Post-review HEAD move (f71ccbe)

While this attack ran, L1 committed `f71ccbe` ("round-17: wave-2 corrections
(tripwire fixes + regression suite, ... label-check/measure hardening, wave
reports)"). The findings above are anchored to `988b858` as assigned; this
section re-checks each against the new HEAD so nothing already fixed is
re-reported.

| finding | status at `f71ccbe` |
|---|---|
| F1 | **addressed.** M4 now says *"whether any seat issued a package command **in the covered forms** is checked ... (`evidence/tripwire-r17.txt`: 149 files, 1 `live_probe` `ps` by RevSeparability, 133 unparsed spawns); `clean` would not mean no seat ran one."* I verified all three numbers against the **committed** receipt: 149 files, `('live_probe','ps','MadoR17.RevSeparability.jsonl',152)`, `sum(unparsed_spawns)=133`. The tool still has no npx/uv/pip/npm/cargo classifier: `git show f71ccbe:tools/mado-tripwire.py` on the five-installer transcript is still `MADO_TRIPWIRE: clean`. The corrected sentence is accurate; the blind spot remains, now disclosed. |
| F2 | **stands.** The "L1 sent a binding reminder to all 70 seats at dispatch" sentence is byte-identical at `f71ccbe`; the three reminder records still place it mid-wave (or at no time). |
| F3 | **stands.** Still no `mado.md` in `.ufo/reports/round-17/`; `drafts/ReportSkeleton.md:105` still holds `{{PAUSE_STATE}}`. |
| F4 | **stands.** M5 is unchanged; no close receipt and no command. |
| F5 | **stands.** The +12-line `measure.py` change at `f71ccbe` is the `## Registry` parser / duplicate-id fix from AttackRubricGaming E2, not a mutant run of the four tightenings; `measure-final.json` (untracked) is a count, not a failure receipt. I re-ran `f71ccbe`'s `measure.py` (`de4c422b…`): 2/6 at `27cd06f`/`f52f43f`/`ab0bc9b`, 4/6 at `a9998d1`/`f71ccbe` — the registry hardening changes no score. |
| F6 | **stands.** No baseline-existence ("new entries") check was added. |
| F7 | **stands.** M5's line range is unchanged. |
| F9 | **resolved.** `f71ccbe` tracks 149 files under `w1/reports` + `w2/reports`; `git ls-tree -r --name-only f71ccbe -- .ufo/waves/round-17/w1/reports .ufo/waves/round-17/w2/reports \| wc -l` = 149, including all six cited here. |

Two new observations at `f71ccbe`, neither a broken pointer:

1. **M1's `exit 1` is now a historical receipt.** The hardened
   `label-check.py` (`a6512a01…`) returns the *expectation* verdict: rerun
   now prints the same seven LABEL lines and `EXPECT_SUMMARY: 7/7`, but
   exit **0** (`evidence/label-check-final.txt`, untracked, records
   `exit=0`; the old tracked `evidence/label-check.txt` is `b890a5ca…` and
   exit 1). The red controls still show as `MISMATCH` in the LABEL lines,
   so the M1 fix still demonstrates the defect; the fix cell should either
   cite the final receipt or say "exit 0 under the hardened checker; the
   exit-1 record is the pre-hardening run". The untracked final receipt
   should be committed if it is the evidence of record.
2. **The worktree `evidence/tripwire-r17.txt` diverges from the tracked
   one.** Tracked at `f71ccbe`: `9f88e117…`, 149 files, 133 unparsed.
   Worktree: `136fc60c…`, 149 files, **136** unparsed (a concurrent rerun
   added three). M4's 133 matches the tracked receipt, so the row is correct
   now; if the worktree file is committed as-is, the 133 becomes wrong.

## M1 — attack failed

Every pointer and claim I checked resolves, and the fix reproduces:

- `round-16.md:131-132` at `27cd06f` is the offending sentence; the cited
  `.ufo/waves/round-16/evidence/frozen-tampered.json` has
  `measured_commit 9dcf248…`, `exit 2`, stdout `MADO_PLAN: frozen_error`
  ("expected.json pair 1/'denied_executable:sudo' is unreachable").
- `corpus/lessons/round-16-verifier-spotcheck.md:164-172` (R16-V1) describes
  exactly this and was present at `27cd06f`.
- The append-only erratum is at the end of `round-16.md`
  (`git diff 27cd06f HEAD -- corpus/lessons/round-16.md`: 18 insertions,
  0 deletions) and its "where snapshot_tampered is evidenced" line checks
  out: `action-selftest-final.json` (rev `4bfb236`, measured `1e31681`)
  carries `frozen-tampered-plan/policy: want 2/snapshot_tampered got
  2/snapshot_tampered`; `action-selftest.json` (rev `1e31681`) records
  measured `9dcf248` and carries the got-side token.
- `corpus/QUALITY.md:111` is criterion 23; `measure.py 3722ba4` reports
  criteria 23, lesson_cited 15 (the C1 15/23 claim is arithmetically right).
- `label-check.py` rerun at `988b858` reproduces `evidence/label-check.txt`
  exactly (the hardened checker at `f71ccbe` prints the same LABEL lines but
  exits 0; §Post-review):
  `R16-V1-red MISMATCH`, `frozen-match-green ok`,
  `spotcheck-selftest-final-green ok`, `want-side-only-mutant MISMATCH`,
  `superseded-commit-mutant MISMATCH`, `honest-red-green ok`,
  `recut-green ok`, `EXPECT_SUMMARY: 7/7`, exit 1. The mutant fixture
  `label-fixtures/want-only.json` exists and carries the token only on the
  want side (`want 2/snapshot_tampered got 2/frozen_error`).
- `frozen-tampered-recut.json`: tampered run exit 2 `snapshot_tampered`,
  control exit 0 `frozen_match`, both `matched: true`.

Two precision notes at `988b858`, not findings: (a) the cited receipt
`frozen-tampered.json` contains **zero** occurrences of `snapshot_tampered`
(verified at `1e31681` and in the worktree); the "substring check would
also have passed" sentence is true only for a check that scans a wider
evidence set (the red selftest receipt), not the cited receipt itself.
**Superseded at `f71ccbe`**: L1 rewrote this captured-by to
*"A plain substring check on `frozen-tampered.json` would have caught this
one (the token occurs 0 times there)"* — which matches my measurement.
(b) `spotcheck-selftest-final-green` is the receipt that does carry the
token; the red claim is correctly scoped to outcome-side tokens by the
script.

## Reproductions (all read-only or /tmp)

```text
python3 -I .ufo/waves/round-17/label-check.py                       # exit 1, 7/7 expected
python3 .ufo/waves/round-17/measure.py 27cd06f|f52f43f|ab0bc9b      # 2/6 each
python3 .ufo/waves/round-17/measure.py a9998d1|3722ba4             # 4/6; c1 15/23
git show 0175f13:SCORECARD.md | sed -n '821,865p'                   # declaration
git show 0175f13:.ufo/waves/round-17/measure.py                     # absent (cat-file 128)
git show f52f43f:...measure.py | sha256sum                          # a280b3ab…
git show ab0bc9b:...measure.py | sha256sum                          # 4023124f…
sed -n '2440,3152p' /var/log/pacman.log | grep -c 'PACMAN] Running' # 13
python3 -I tools/mado-tripwire.py --scan /tmp/...installers.jsonl   # clean, exit 0
python3 -I tools/mado-tripwire.py --scan /tmp/...mixed.jsonl        # flags sudo/pacman only
```

Working-tree note: `git status` shows uncommitted edits to
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/terminal-route-r17.md`
and the M2 row of `corpus/lessons/round-17.md` (M1/M3/M4/M5 rows unchanged).
All measure/fixture results above use committed revisions; no finding here
depends on the uncommitted bytes.

## Verification gaps

- Wave-2 transcripts are not named by my item and were not read; F1's wave-2
  coverage gap is asserted from the receipt set (only
  `evidence/tripwire-r17-w1.txt`, 70 files, exists at HEAD) and the
  wave-2 dispatch mtime (`14:52:54Z` local `11:52:54 -0300`), not from reading
  wave-2 session files.
- The wave-1 receipt itself records `1` unparsed spawn
  (`MadoR17.SentinelTranscriptRead.jsonl`) and `1` unparsed eval cell
  (`MadoR17.RevengeEvalBang.jsonl`); M4's "checked" sentence does not carry
  that caveat (the lesson's C3 section does).
- No close-time re-measure exists, so F4 cannot be tested against a close
  receipt; that is the point of the finding.

## Residual risk

- F1 is the one to fix first: the M4 fix's completeness sentence is the
  assurance a later reader will quote, and it is falsified by the tool's
  own documented class list and by a five-line transcript.
- F5 is a receipt defect, not a score defect: the tightened instrument
  behaves as claimed in an independent `/tmp` run, but the round's
  "shown able to fail" standard is not met by the committed evidence.
- M1 is clean on this attack; the only exposure is the ambiguous "outside"
  wording and the directory-wide-substring caveat, neither load-bearing.
