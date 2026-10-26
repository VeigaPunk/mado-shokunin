# Mistakes — round-41 wave-2 additions (draft, M41-9..17)

Drafted by seat `ScrMistakesV2` (w2) for the L1 to integrate into
`corpus/lessons/round-41.md` under `## Mistakes`, after M41-8. Every evidence pointer below
resolves: `verify-pointers.py` in this seat dir checks each `path:line` (working tree; the
lessons file at the data commit via `git show 07f2641:`) against the quoted fragment, and its
output (`verify-pointers.out`) is the receipt.

**M41-9 - the v1 predicates were falsified by the w1 seats before any data commit; the claims
re-registered to v2.** Class: a predicate falsified after seats have scored it (the M41-7
disclosure pattern, realized). Evidence: the data-commit lesson's own re-registration paragraph —
`corpus/lessons/round-41.md:21` ("the w1 seats falsified v1 (`CritC1Cheat` 8 of 12 cheats
scored TARGET_MET; `ExecC1ExtraMutants` 13 of 42 mutants; `CritC2Cheat` 9 of 9 forgeries
admitted; `ExecC2ExtraMutants` 29 of 45)"); the primary measurement
`.ufo/waves/round-41/w1/CritC1Cheat.md:18` ("8 of 12 cheats scored TARGET_MET"); the ordering
disclosure `.ufo/waves/round-41/registration-v2.md:3-11` ("the v1 predicates were scored by w1
seats … so v2 was written after seats had seen v1 scores"). Captured-by: none — falsifying the
predicates was the w1 seats' job, not a rule's; the M41-7 disclosure rule is what made the
repair legal. Fix: landed — `registration-v2.md` re-registers the predicates before any data
commit, binds the claims to v2, and the lesson reports both scores at the data tip
(`registration-v2.md:5-11`). Shown able to fail: none — the failing runs are the cheat scores
themselves (`.ufo/waves/round-41/w1/CritC1Cheat/score-ch1.txt`:
`fixtures=24/24 … verdict=TARGET_MET`), not a control.

**M41-10 - the live-stub payload was readable without running the program: the C1 live fixtures
passed by reading the fixture, not executing it.** Class: counter-harness design — a "program"
whose behaviour can be read instead of executed. Evidence: CH1
`.ufo/waves/round-41/w1/CritC1Cheat.md:73-92` — `read_live` "reads the stub's own bytes,
decodes the base64 journal out of the `printf '%s' … | base64 -d` line" (`:75-77`), and the
probe measured `read_live_returned_payload=101 marker_created=0` (`:83`), i.e. the stub never
ran; CH2 `.ufo/waves/round-41/w1/CritC1Cheat.md:105-121` — `prepare` writes the journal to
`<fx>/journal.txt` even when the fixture is live (`:107`), and
`P2 read_live_returned_cwd_file=1 from_program=0` (`:115`); reproduced independently by
`.ufo/waves/round-41/w1/RevC1Counter.md:27` ("`live0` decode-cheat `rc=0 ok=1`"). Captured-by: none. Fix: landed in v2 — the live program is a compiled
execute-only (0111) ELF built per fixture, no copy of the journal on disk, and it records `ran`;
an unusable program must not have run (`registration-v2.md:20`). Shown able to fail:
`.ufo/waves/round-41/receipts/ctl-c1-v2.txt:49` (K01-stub-bytes-read →
`fixtures=33/39 … TARGET_MISSED`) and `:50` (K02-cwd-journal-replay →
`fixtures=33/39 … TARGET_MISSED`).

**M41-11 - the b2 teeth clause was satisfiable without a test: path tests, self-fingerprints and
renames killed all six sampled mutants.** Class: a teeth clause whose sample can be gamed.
Evidence: CH6 `.ufo/waves/round-41/w1/CritC1Cheat.md:166-174` — `basename(dirname(argv[0])) != "tool"`
prints `1/2 passed` and exits 1, scoring `killed=6/6`, while identical source minus those four
lines scores `0/6 killed and MISSED` (`:173`); CH9 `.ufo/waves/round-41/w1/CritC1Cheat.md:182-196`
— a rolling hash of the tool's own file fails any edit; CH10
`.ufo/waves/round-41/w1/CritC1Cheat.md:212-230` — renaming `parse`/`report`/`classify` into
`_run*`/`_check*` moves every sampled site out of the parser, yet all six are killed;
`RevC1Counter` reproduced b2's vacuity with the counter's own `teeth()`
(`.ufo/waves/round-41/w1/RevC1Counter.md:13-18`). Captured-by: none. Fix: landed in v2 — clause
b3 (a tool with a trailing comment plus an `ast.unparse` and one assignment must still pass its
selftest in full) and exact-name exclusion (`selftest`, `main`, `usage`, and functions inside
`selftest`), with one of the six sites forced into the summary-emitting function and kill counts
`k != n` (`registration-v2.md:21-22`). Shown able to fail:
`.ufo/waves/round-41/receipts/ctl-c1-v2.txt:53` (K05-selftest-argv0-path →
`fixtures=39/39` but `TARGET_MISSED`) and `:55` (K07-selftest-size-fingerprint →
`fixtures=0/39 … TARGET_MISSED`).

**M41-12 - five of six journal `-o` formats silently produce `NO_SESSIONS` on a non-empty
journal.** Class: overloaded verdict — "empty journal" and "journal in an unparsed shape" are
byte-identical observables. Evidence: `.ufo/waves/round-41/w1/ExecJournalFormat.md:23`
(`short` → `3 / NO_SESSIONS`; only `short-iso` parses), `:40-44` (finding 1: "byte-for-byte
the observable of a genuinely empty journal"), `:47` (the live leg has the same hole: a wrapper
emitting `-o short` yields `NO_SESSIONS`/exit 3, not `SETUP journalctl_failed`); `journalctl
--user -u … > f` without `-o` is byte-identical to `-o short` (`:44`) — the most natural capture
is the failing one. Captured-by: none. Fix: landed in v2 — new `ignored=` field and verdict
`UNRECOGNIZED_FORMAT` (exit 4), fixtures `unrec0`, `mixed0` (`registration-v2.md:29`). Shown
able to fail: none — the new fixtures carry it; no control isolates the class yet.

**M41-13 - `--journal-file` on a FIFO hangs forever, and `--live` output is buffered whole before
the size cap.** Class: unbounded blocking input in the reference tool. Evidence:
`.ufo/waves/round-41/w1/RevRefTool.md:18-19` (M1: "`open()` blocks, no timeout; verified
`timeout 4` → 124", reference lines 194–196) and `.ufo/waves/round-41/w1/RevRefTool.md:20-21`
(M2: "300 MB writer → 615 MB child peak RSS", reference lines 179–189). Captured-by: none (both
sit in the declared residual space). Fix: landed in v2 — regular-file requirement
(`O_NONBLOCK` open + `fstat`), incremental bounded read with a 30 s deadline; fixtures `fifo0`,
`dir0`, `livehang0` (`registration-v2.md:30`). Shown able to fail: none — the new fixtures carry
it.

**M41-14 - the C2 gate admitted eight fabrications and 29 extra mutants: the v1 C2 predicate did
not bind evidence to provenance.** Class: a coverage predicate that admits invented paperwork
(fabricated receipts, an invented journal, absent package paths, unmapped locations). Evidence:
`.ufo/waves/round-41/w1/CritC2Cheat.md:13` ("The frozen counter **admits all nine**"), `:27`
(`FORGE_SUMMARY fixtures=9 admitted=9/9 genuine_proxy_clean=1`), and the F1–F7 table `:36-45`;
`.ufo/waves/round-41/w1/RevC2Counter.md:18` (minimal forgery "passes at 9,220 committed bytes /
9 files") and `:30-37` (H1–H4); `.ufo/waves/round-41/w1/ExecC2ExtraMutants.md:43`
(`mutants=45 survivors=29/45`). Captured-by: none. Fix: landed in v2 — PINS (receipts of NEW
ids are the pre-wave fetch bytes), mode 100644, window-wide header rules and ghost-id refusal,
calendar-valid `recheck`, receipt-bound locations, held rows keep their used-by items, ≥3 new
ids, quote exclusivity across cited receipts, one cited id per entry line, unfenced lesson,
journal provenance floor (boot line, ascending distinct session starts), STAGED allowlist for
ADMIT/REFUSE, REFUSE reason of ≥4 distinct words, localized markers over the whole row
(`registration-v2.md:32`). Shown able to fail: `.ufo/waves/round-41/receipts/ctl-c2-v2.txt:14-19`
— F1–F6 all `observed=admitted=0/1` (F1 `:14`, F2 `:15`, F3 `:16`, F4 `:17`, F5 `:18`, F6
`:19`); control P admitted under both real and patched counters.

**M41-15 - the C1 control suite itself is nonce-flaky: a correct counter fails its own suite
~1-in-10 runs.** Class: a control suite whose verdicts depend on the nonce draw. Evidence:
`.ufo/waves/round-41/w1/MutC1CounterGates.md:35` ("the control suite itself is nonce-flaky
(~2/22 runs)") and `:37`, `:41-42` (M27/M39 each flipped to MET exactly once across 22 full-suite
draws (`:37`); "a *correct* counter fails its own suite as `correct=46/47` roughly 1-in-10 runs
overall, and the same lottery can" (`:41`) — `fake a "kill" in mutation testing.` (`:42`)). Captured-by: none. Fix: none —
declared limit: treat a single full-suite draw as noisy; the round's response was two retries
plus 40 targeted pristine draws (`.ufo/waves/round-41/w1/MutC1CounterGates/logs/`). Shown able
to fail: the observed flips are recorded in `.ufo/waves/round-41/w1/MutC1CounterGates/matrix.md`
and `logs/`; no control isolates the lottery.

**M41-16 - a kernel restart during w1 dropped every seat result from `w1-results.json`; the seat
reports survived on disk.** Class: driver/orchestrator persistence gap — the wave's result ledger
existed only in a session that died. Evidence: `.ufo/waves/round-41/w1-results.json:7-12` —
every one of the 34 records carries `"output": null` with the note "orchestrator kernel restarted
mid-wave; seat output was delivered to the orchestrator session but not retained — read the seat
report file in the wave dir" (first at `:11`); the dispatcher's own instruction to the report-
draft seat admits it (`.ufo/waves/round-41/make-w2-spec.py:80`: "the orchestrator's w1-results.json
carries no seat outputs because of a kernel restart, reports are on disk"); the 34 seat reports
exist as files (`.ufo/waves/round-41/w1/*.md`). Captured-by: none. Fix: persist each seat's
report path and exit into `w1-results.json` at seat completion (write-through), so the wave
ledger does not depend on orchestrator-session memory. Shown able to fail: none — no instrument
yet compares `w1-results.json` entries to the seat-report set.

**M41-17 - M41-5's shape-line defect is resolved by `registration-v2.md`'s corrected Shape
section.** Class: freeze-vs-dispatch mismatch repaired before data (closure of M41-5). Evidence:
`.ufo/waves/round-41/registration-v2.md:13-14` ("**Shape (corrects `registration.md` line 4).**
Two v1 waves: `w1` of 34 seats … and `w2` of 34 seats … round total 68"); the data-commit lesson
names the correction alongside the falsification (`corpus/lessons/round-41.md:21`); the M41-5
row itself stands at `corpus/lessons/round-41.md:117-122`. Captured-by: none (as M41-5). Fix:
landed — the v2 registration's rewritten Shape line is the repair M41-5 asked for. Shown able to
fail: none — no control compares a registration's seat count to the spec's item count (unchanged
from M41-5).
