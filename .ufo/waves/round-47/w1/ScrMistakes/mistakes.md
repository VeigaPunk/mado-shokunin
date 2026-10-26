# Round 47 mistakes — draft `## Mistakes` rows (seat ScrMistakes, w1 build, 2026-10-26)

Draft for `corpus/lessons/round-47.md` `## Mistakes` (the L1 integrates; nothing here is landed). Classes are the
`CORPUS.md:171-178` vocabulary (`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`,
`attribution`, `landing`, `provider`). Every row names what it attacks (path:line, or a command and its output) and, for
its fix, how the fix is shown able to fail. Locators were computed (`grep -n`, `git ls-tree`, `git status`), never typed;
every command and its output is in `receipts/` of this seat.

Mined from: `corpus/lessons/round-46-verifier-spotcheck.md` (§2 evidence table, §4-§6, the Limit notes),
`corpus/lessons/round-46.md` (M46-1..M46-16, `## Round-45 closure items`, `## Gate`), the fleet report
`.ufo/reports/round-46/mado.md`, `corpus/QUALITY.md` (criteria 1..90), `CORPUS.md:171-184`. The lane tip read for
state is `c24adef2` (the round-47 claims/registration commit, on top of the round-46 tip `edc14789` and the round-47 base
`60edb66e`); the data commit read for the defects is `1001bda0472f1fdc0679fb88ced5d159f5d32c62`.

Two instruments were written for the rows that had none and both are run in both directions:
`check91.py` (producer identity of a cited run receipt, criterion 91) and `check92.py` (produced vs committed set of a
seat directory, criterion 92). Both are seat instruments (provenance, not credit under criterion 25). Every located quote
below is checked by `verify-quotes.py --root <fleet root>` (`receipts/quote-check.txt`):
`QUOTE_CHECK: checked=25 failed=0`, exit 0; the same table with every locator shifted by one line reads `failed=22`,
exit 1, so the check can fail.

---

**M47-1** · class `provider` · evidence: the round-46 entry attributes the *landed* tool's live run to the pre-landing
draft's receipt. Entry `corpus/knowledge/hyprland-input-devices-r46.md:57` (`1001bda`, unchanged at HEAD) cites
`.ufo/waves/round-46/receipts/live-devices-host-l1.txt`; that receipt's own bytes name its producer at `:1` —
`l1-draft/mado-devices.py`, sha256 `b229efd0…` — and the landed tool `tools/mado-devices.py` at the same commit hashes
`3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f` (`git show 1001bda:tools/mado-devices.py | sha256sum`),
which is the producer named by the *other* receipt, `live-devices-host-r46.txt:1`. The sentence also says "one `input`
block in `~/.config/hypr/input.conf`" while the landed run's header names two configs with the omarchy default first
(`live-devices-host-r46.txt:3-5`, the same two-config order the closure recorded). Receipts:
`receipts/r1-producer.txt`, `receipts/r1-entry-locator.txt`. This is M46-5's class recurring in the very round that
mined it — the criterion was applied to the round-45 entry and not to the new one. ·
captured-by: 24 — applied by the round-46 non-author closure (`corpus/lessons/round-46-verifier-spotcheck.md:52` calls it
a "defect R1"), **missed by the lane's own quality control**: the C2 counter's clause j binds a locator and a keyword per
surface, not the truth of a sentence, and the docstring declares that residual (M46-11, M46-5). ·
fix: append an erratum under the entry citing `live-devices-host-r46.txt`, and correct the sentence's config count (the
landed run reads the omarchy default and the user file); the round's own QC runs the producer check before the data
commit, not only a later closure. Shown able to fail: `python3 -I .ufo/waves/round-47/w1/ScrMistakes/check91.py --repo .
--rev 1001bda… --entry corpus/knowledge/hyprland-input-devices-r46.md --tool tools/mado-devices.py` reads
`PRODUCER …live-devices-host-l1.txt producer=l1-draft/mado-devices.py … verdict=DIFFER` / `CHECK91: … verdict=DIFFER`,
exit 1, and the same command on the one-line-corrected entry (`corrected-entry.md`, `sed` of the receipt name, `diff` in
`receipts/check91-run.txt`) reads `verdict=AGREE`, exit 0.

**M47-2** · class `landing` · evidence: R2 is round-45 D4's class again — evidence produced for a round and still not
committed a round later.
`GIT_OPTIONAL_LOCKS=0 git status --porcelain` at HEAD prints
`?? .ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv`; the file is 3 282 451 B; `git ls-files` over that
seat names 18 paths and not it; the seat directory's last commit is `7f793280`, and the round-46 report disclosed it
(`.ufo/reports/round-46/mado.md:55`). The report's own explanation, "The helper skips new files over 1 MiB inside a named
directory", mis-places the mechanism: the size cap is **jj's** `snapshot.max-new-file-size` (default 1 MiB), and it is not
silent — reproduced in a scratch repo (`receipts/jjfix-receipt.txt`): `jj file track -- root:"sub"` prints
`Warning: Refused to snapshot some files:` / `sub/big.bin: 2.0MiB (2097152 bytes); the maximum size allowed is 1.0MiB
(1048576 bytes)` plus four remedies, and `jj diff --summary` then stages only the small file. So the signal naming the
file, its size and the limit existed at the moment of the commit and was not acted on; `scripts/hyaku/jj-lane.sh:638` has
a 10 MiB rule for *named* files only, and the fleet addendum (`scripts/hyaku/lane-addendum.md:274-275`) states the 1 MiB
directory rule ("are skipped with a warning — name them as files"). Receipts: `receipts/r2-state.txt`,
`receipts/jjfix-receipt.txt`, `receipts/check92-run.txt`. ·
captured-by: 13 (evidence meant to outlive a round is a committed path) and 14 (a census names both sets — here the
produced set and the committed set of one seat directory, which no instrument compared). ·
fix: commit a digest line (sha256, size, row count) beside the seat's `out.json` and remove the working file, or track it
with `jj file track --include-ignored`; and every seat directory is inventoried against its tip before the round commits.
Shown able to fail: `python3 -I .ufo/waves/round-47/w1/ScrMistakes/check92.py --repo . --rev HEAD --dir
.ufo/waves/round-46/w1/ExecStofOracle` reads `UNCOMMITTED 3282451 …out.json.rows.tsv` /
`worktree=19 tracked=18 uncommitted=1 uncommitted_bytes=3282451 verdict=DIFFER`, exit 1, while the same command on
`…/w1/ExecSerialRule` (17/17) and `…/w1/ExecSupersede` (23/23) reads `verdict=OK`, exit 0.

**M47-3** · class `vacuous` · evidence: the round-46 gate landed with its red state pre-authorised, so its red proves
nothing. `SKILL.md:770` registers `mado-session-material` and its notes cell ends "no synthetic marker yet, so a red exit is
expected until it lands"; the round's only receipt for it reads
`SESSION_MATERIAL: files=18363 findings=115 rev=1001bda…` / `exit=1`
(`.ufo/waves/round-46/receipts/session-material-data.txt`, committed at `9879964`), and the gate is still red at the
round-47 base: `python3 -I quality/check-session-material.py --repo . --rev HEAD` prints
`SESSION_MATERIAL: files=18377 findings=115 rev=c24adef2…`, exit 1 (`receipts/session-material-head.txt`; it reads committed bytes at HEAD, where 0 of the
115 findings are in round-47 files — the count moves at that round's data commit, which is the point). A gate whose spec says "red is expected" cannot fail under its own spec — the
criterion-56 shape applied to the gate registry instead of to a counter clause. The marker and the prose serial rule were
drafted and committed (`.ufo/waves/round-46/w1/ExecSessionTriage/`, `…/ExecSerialRule/`) and not installed. ·
captured-by: 56 (a clause that cannot fail under its own spec is dead code — extended here to a registry cell), with 30
adjacent (a detector credited is admitted only beside its precision evidence; the gate's own false positives were
untriaged at the data commit). ·
fix: install the drafted marker (and the R5/R6 prose rules), re-run the gate to `findings=0` at the round-47 tip, and
replace the waiver sentence in `SKILL.md:770` with the clean-state receipt. Shown able to fail: the two sides are already
committed as seat receipts — `…/ExecSessionTriage/receipts/04-marked-49.txt` (base 97 → 48 with 49 waived),
`…/06-planted-real-dump.txt` (a planted real dump still flagged) and `…/07-tampered-waived-fixture.txt` (a tampered waived
fixture re-flagged) — so after install the gate must read `findings=0` on the marked set *and* still flag the planted
dump; today's receipt is red with the waiver standing, which is the red state of the fix.

**M47-4** · class `landing` · evidence: the S290-S297 supersession is deferred a **fourth** time. Registry at HEAD:
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 262 rows, last id `S325`, and
`grep -cE '^ {0,3}\|[[:space:]]*S3(2[6-9]|[3-9][0-9])[[:space:]]*\|'` → 0, so the drafted S326-S333 rows are still not
landed although `.ufo/waves/round-46/w1/ExecSupersede/rows.md` (committed `7f793280`) carries them census-clean; the ages
ledger has kept it open since round 43 (`.ufo/waves/round-46/w1/ScrRoutedAges/ages.md:55`, first routed `S43:100`).
The same route also still carries the round-45 entry's six non-supported sentence units and the round-44
`w2/ConnCalibration` errata. Receipt: `receipts/r4-deferral.txt`. ·
captured-by: 90 (registered this round at `QUALITY.md:454`; round 47 is the first round in which it can bite, and it does:
the item is past its third routing). ·
fix: land the drafted rows under round-47's own registration before any new claim, and land the two errata; the ages
ledger is recomputed at the round-47 tip. Shown able to fail: the two count commands above read `262` / `S325` / `0` at
HEAD — a landed supersession moves all three — and `age` is emitted by the ledger, not typed (see M47-5).

**M47-5** · class `number-drift` · evidence: two hand-carried numbers disagree with the instruments they cite, both by one.
(a) The lesson says the S290-S297 supersession's "age now 4 rounds (`w1/ScrRoutedAges/ages.md` R43-D2)"
(`corpus/lessons/round-46.md:311`), while the ledger it cites defines `age = 46 − first_routed_round`
(`ages.md:14-15`; a round-45 item has age 1, a round-38 item age 8) and prints **3** for R43-D2 in its own age column
(`ages.md:88`). 46 − 43 = 3; the lesson's 4 is the round-47 exclusive value or a 5-round inclusive count, i.e. it uses a
convention the ledger does not state. (b) The closure's routing text calls round 47 the "third deferral"
(`corpus/lessons/round-46-verifier-spotcheck.md:116`), while M46-16 already records round 46 as the third slip
("slips a third time", `corpus/lessons/round-46.md:307-308`), so round 47 is the fourth; the deferral sites are r44:93,
r45:68, r46:307-308 and r47:116. Receipts: `receipts/age-drift.txt`, `receipts/ages-derive.txt`. ·
captured-by: 10 (each count as `<n> — <command> <date>`, rederived from the named revision) and 14 (a census names both
sets; here the two readings of the same interval). ·
fix: an appended errata states the convention it uses ("3 round boundaries, the fourth round in which the item is
carried") and cites the ledger's cell or the ledger emits the sentence; a deferral count is derived from the round number
and the first-routing round by the same command. Shown able to fail: `python3 -c 'first=43; now=47; print(now-first)'
` → 4 (the ledger's rule at round 47) against `ages.md:88`'s **3** at round 46, and `grep -n` over the four deferral sites
prints four lines — so a typed "4" at round 46 and a typed "third" at round 47 each contradict their own citation by one.

**M47-6** · class `landing` · evidence: M46-13's fix landed on two of the three counters, and the bytecode artifact is
back in the tree the counters score. `quality/counters/c1-r46-devices-v3.py:76` and `…-v2.py:69` carry
`sys.dont_write_bytecode = True`; `quality/counters/c1-r46-devices.py` (v1, still committed and still the version the
earlier receipts cite) carries none (`grep -c dont_write_bytecode` → 0), and it imports the model in-process from the live
worktree (`c1-r46-devices.py:67-68`, `:98`). A pyc sits in the frozen round-46 tree at
`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc` — 40 149 B, mtime
`2026-10-26T18:45:35.561-03:00` (written after the round-46 tip, whose last commit is `edc14789` 18:26:38), hidden from `git status` by `.gitignore:3`,
and its header's source mtime/size equal the frozen model's (`27743` B), so it was compiled from that model. `[INFERENCE]`
the writer was an unguarded in-process import: the guarded import leaves no directory, a subprocess run of the model
leaves none either, and this seat ran no such import (its only import was of a scratch copy). Mechanism reproduced in scratch: the same import with the guard writes no
`__pycache__`, without it writes one (`receipts/pyc-header.txt`, `receipts/pyc-state.txt`). ·
captured-by: **none** — criteria 13 and 63 govern committed evidence, not an instrument's own ignored write into the tree
it scores; M46-13 recorded the same gap. ·
fix: every counter imports the pinned model from a copy under its `--work` (the pin already fails closed on byte drift, so
the copy costs nothing), v1 gets the guard or is retired, and a run's receipt carries a before/after inventory of the
scored tree. Shown able to fail: the before/after inventory around one run — the unguarded import creates
`__pycache__/mado-devices.cpython-314.pyc` beside the model, the guarded one leaves the directory absent
(`receipts/pyc-header.txt`), and the frozen tree's own pyc (above) is the red state the inventory names by path, size and
mtime.

---

## Proposed QUALITY criteria (next numbers after `QUALITY.md`'s last, 90)

**91.** A knowledge entry that cites a run receipt for a claim about a *landed* surface cites a receipt whose producer
line names that surface, at the same revision — and the round applies the check to its own entry before the data commit,
not only a later non-author closure. Check: `python3 -I .ufo/waves/round-47/w1/ScrMistakes/check91.py --repo . --rev REV
--entry <entry> --tool tools/<tool>.py` (prints one `PRODUCER` line per cited receipt and
`CHECK91: … differ= unparsed= absent= verdict=AGREE|DIFFER`). Shown able to fail: `verdict=DIFFER`, exit 1, on
`corpus/knowledge/hyprland-input-devices-r46.md` at `1001bda` (`:57` → `l1-draft/mado-devices.py`), and `verdict=AGREE`,
exit 0, on the same bytes with the citation corrected to `live-devices-host-r46.txt` (`.ufo/waves/round-47/w1/ScrMistakes/receipts/check91-run.txt`).
(lesson: lessons/round-47.md#mistakes M47-1)

**92.** A seat directory's produced set and its committed set are compared at the round tip and both are named: a tool's
own announced skip (size cap, ignore rule) is a gate for the integrator, not a footnote in the report, and a file the tool
announced is either committed (with `--include-ignored` where its size demands it, or a committed digest beside it) or its
retention is stated with that digest. Check: `python3 -I .ufo/waves/round-47/w1/ScrMistakes/check92.py --repo . --rev REV
--dir .ufo/waves/round-N/w1/<Seat>` (prints `UNCOMMITTED <bytes> <path>` lines and
`CHECK92: … worktree= tracked= uncommitted= uncommitted_bytes= verdict=`). Shown able to fail: `verdict=DIFFER`, exit 1,
on `w1/ExecStofOracle` at HEAD (`uncommitted=1 uncommitted_bytes=3282451`) and `verdict=OK`, exit 0, on
`w1/ExecSerialRule` (17/17) and `w1/ExecSupersede` (23/23) (`.ufo/waves/round-47/w1/ScrMistakes/receipts/check92-run.txt`).
(lesson: lessons/round-47.md#mistakes M47-2)

**93.** A detector is registered as a gate only with its clean-state receipt at the revision it scores: a registry cell
that declares a non-zero exit expected is a standing waiver, and a gate carrying one counts as a gate that cannot fail
(extends 56 from a counter clause to the gate registry) — the clean receipt and a planted-defect receipt that still trips
are both required at the same revision. Check: `grep -n 'expected until it lands' SKILL.md` must print nothing for a
registered gate, and the round carries `<GATE>: … findings=0` plus a planted-defect run reading `findings>0`. Shown able
to fail: `SKILL.md:770` carries the waiver and the round's only receipt reads `SESSION_MATERIAL: … findings=115` / `exit=1`
(the gate is red at `1001bda` and still red at the round-47 base, `files=18377 findings=115 rev=c24adef2`), while the
drafted marker's own receipts show the two sides (`04-marked-49.txt` 97→48, `06-planted-real-dump.txt` flagged).
(lesson: lessons/round-47.md#mistakes M47-3)

**94.** Every carried number about a routed defect is emitted by the ledger that owns it, never transcribed: an age is the
ledger's own cell (or the ledger prints the sentence), and a deferral count is derived from the round number and the
first-routing round by one command that appears in the lesson. Check: the lesson's age sentence and the ledger's cell for
the same id are read by one command; a disagreement is a violation. Shown able to fail: `ages.md:88` prints **3** for
R43-D2 at round 46 while `round-46.md:311` says "age now 4 rounds"; and the four deferral sites (r44:93, r45:68, r46:307-308,
r47:116) count four against the closure's "third deferral" at `round-46-verifier-spotcheck.md:116`.
(lesson: lessons/round-47.md#mistakes M47-4, M47-5)

**95.** A scoring instrument writes only under its `--work`: it loads its pinned model from a copy there, never by
in-process import from the tree it scores, and its receipt carries a before/after inventory of that tree. Check: run the
counter once and diff `find <scored tree> -newer <marker>` before and after; the inventory must be empty. Shown able to
fail: the unguarded import writes `__pycache__/mado-devices.cpython-314.pyc` beside the model while the guarded one leaves
no directory (`.ufo/waves/round-47/w1/ScrMistakes/receipts/pyc-header.txt`), and the frozen tree carries such a pyc with
today's mtime (40 149 B, `2026-10-26T18:45:35`) under `.gitignore:3`.
(lesson: lessons/round-47.md#mistakes M47-6)

## Applications of existing criteria

- M47-1 → 24 (producer identity), and it shows 24 needs the *declared surface* as well as the hash: the cited receipt's
  hash is honest, its producer is the draft.
- M47-2 → 13 (evidence outliving a round is a committed path) and 14 (a census names both sets); 79 is adjacent (a
  pointer to a `receipts/` path is satisfied while the *artifact* the pointer summarises is uncommitted).
- M47-3 → 56 (a clause or, here, a registry cell that cannot fail under its own spec is dead code); 30 adjacent (a
  detector credited needs its precision evidence — the 115 findings were untriaged at the data commit).
- M47-4 → 90 (a routed defect keeps one identity and an age; a third routing is mined as a `landing` mistake — round 47
  is the fourth).
- M47-5 → 10 (each count as `<n> — <command> <date>`, rederived) and 14.
- M47-6 → none; 13 and 63 govern committed evidence, not a counter's own ignored write, which is why M46-13 recorded the
  same gap and it recurs here.

## Conflicts recorded for the judge (verbatim, both sides located)

1. **The same round read as `improved` and as `unprovable-but-better`.** The lane's report says "**quality: improved.**"
   (`.ufo/reports/round-46/mado.md:90`) while the non-author closure says "**quality: unprovable-but-better**"
   (`round-46-verifier-spotcheck.md:95`) on the grounds that "the round-45 entry's six non-supported units are recorded in
   the lesson, not corrected". The two readings agree on the facts and disagree on whether recording discharges the
   defect; M47-4 keeps the item open, which is the closure's reading.
2. **Two counts of the same age.** `ages.md:88` prints **3** for R43-D2 under the rule stated at `ages.md:14-15`, and
   `round-46.md:311` prints "age now 4 rounds" citing that row. Neither is refuted by the other's arithmetic — they use
   different conventions (exclusive boundaries vs inclusive rounds), and neither file states which one the sentence uses;
   M47-5 records the ambiguity rather than choosing.
3. **"third deferral" at two rounds.** `round-46.md:307-308` records round 46 as the third slip; `round-46-verifier-spotcheck.md:116`
   calls round 47 the "third deferral". Both are corrected by counting the recorded sites (r44:93, r45:68, r46:307-308,
   r47:116 → four); M47-5 records the count, the L1 decides whether the closure's text or the lesson's is amended.

## Checked and found clean (so the judge does not re-open them)

- QUALITY 88's check command is runnable as written: it reads
  `CHECK88: admitted=10 declared=4 undeclared=6 tightened=13 positive=PASS` / `verdict=PASS`, exit 0
  (`receipts/check88-as-written.txt`). `--positive-rev 072da817…` is a label inside the two seat receipts (3 hits in
  `forge.out`, 1 in `tighten.out`), not a lane commit — `git cat-file` fails on it in the lane and in the fleet repo, and
  that is expected, not a defect.
- The counters' model pins fail closed on worktree byte drift: `c1-r46-devices.py:98` and `c1-r46-devices-v3.py:121` call
  `pinned(MODEL_PATH, MODEL_SHA256)` before `exec_module`, so a counter reading the live worktree cannot silently score
  other bytes (`receipts/model-load.txt`). M47-6 is about the write, not the read.
- Round 46's `w1-results.json` carries 66 outputs for 66 seats (closure §1), so M46-9's fix held; the shipped
  `mado-session-material` registry row exists (`SKILL.md:770`), so round-45 D3's routing half held; the round-45 D4 digest
  is committed (`git ls-files` lists four files in that seat, digest included).

## Receipt index (this seat)

| receipt | what it shows |
|---|---|
| `receipts/r1-producer.txt` | landed tool sha256 at `1001bda`, draft tool sha256, both live receipts' producer lines |
| `receipts/r1-entry-locator.txt` | `grep -n` locator of the entry sentence, the two receipts present at `1001bda` |
| `receipts/check91-run.txt` | check91 DIFFER (red) and AGREE (green), with the projection diff |
| `receipts/r2-state.txt` | `git status --porcelain`, file size, `git ls-files`, last commit of the seat dir |
| `receipts/jjfix-receipt.txt` | jj's `Refused to snapshot` warning in a scratch repo (the 1 MiB cap is announced) |
| `receipts/check92-run.txt` | check92 DIFFER (red, 3 282 451 B) and OK (green) on two clean seat dirs |
| `receipts/r34-state.txt` | `SKILL.md` registry row, the data-commit session-material receipt, drafted marker files, registry row count |
| `receipts/session-material-summary.txt` | the round-46 receipt's own summary line (`rev=1001bda`, `exit=1`) |
| `receipts/session-material-head.txt` | the same gate at the round-47 base (`rev=c24adef2`, `findings=115`, exit 1) |
| `receipts/r4-deferral.txt` | 262 rows, last `S325`, no S326+ row, the drafted ids, M46-16 and R4 locators |
| `receipts/age-drift.txt`, `receipts/ages-derive.txt` | the ledger rule and cell, the lesson sentence, the four deferral sites |
| `receipts/pyc-state.txt`, `receipts/pyc-header.txt` | the pyc in the frozen tree, its ignore rule, guards in v2/v3 vs v1, the guarded/unguarded repro |
| `receipts/check88-as-written.txt` | QUALITY 88's check run as written (PASS) |
| `receipts/instruments-tracked.txt` | every path QUALITY 87-90 cites is committed at HEAD, with its commit |
| `receipts/model-load.txt` | the model pin in v1 and v3, and the `exec_module` call sites |
| `receipts/quote-locators.txt` | `grep -n` locators for every quoted line in these rows |
