# ScrMistakes — round 47 w1 (mado, hyaku run 9, 2026-10-26)

Seat: scribe, `## Mistakes` mining. Lane base `60edb66e`; state read at `c24adef2` (round-47 claims/registration
commit); defects read at the round-46 data commit `1001bda0472f1fdc0679fb88ced5d159f5d32c62` (the entry and tool are
unchanged since — `git log -1 -- corpus/knowledge/hyprland-input-devices-r46.md` → `1001bda0`).
Deliverable: `.ufo/waves/round-47/w1/ScrMistakes/mistakes.md` (6 rows M47-1..M47-6 + 5 proposed criteria 91-95, each
citing its row). Scratch `/fast/scratch/hyaku/mado-r47/ScrMistakes/` removed at exit; nothing here cites a scratch path.

## Behavior (what this seat did)

Read `corpus/lessons/round-46-verifier-spotcheck.md` (R1-R4, §2 evidence table, §4-§6, Limit notes),
`corpus/lessons/round-46.md` (M46-1..16, `## Round-45 closure items`, `## Gate`), the fleet report
`.ufo/reports/round-46/mado.md`, `corpus/QUALITY.md` (1..90), `CORPUS.md:171-184` (class vocabulary, "a fix is shown able
to fail") and `considerthese`-derived `w1/ScrRoutedAges/ages.md`. Then measured, read-only, in the lane: producer hashes of
the two live receipts vs the landed tool; worktree state of the round-46 seats; the registry (262 rows, last `S325`);
the session-material gate at HEAD; the guard state of the three C1 counters; the pyc in the frozen tree; and I ran
QUALITY 88's own check command as written.

Three seat instruments, each run in both directions:

| instrument | rule | red | green |
|---|---|---|---|
| `check91.py` | a cited run receipt's producer is the landed surface at the same rev (criterion 91) | `verdict=DIFFER`, exit 1, on the round-46 entry as landed (`:57` → `l1-draft/mado-devices.py`) | `verdict=AGREE`, exit 0, on the same bytes with the citation corrected (`corrected-entry.md`, one-line `sed`) |
| `check92.py` | a seat dir's produced set == its committed set (criterion 92) | `uncommitted=1 uncommitted_bytes=3282451`, exit 1, on `w1/ExecStofOracle` | `verdict=OK`, exit 0, on `w1/ExecSerialRule` (17/17) and `w1/ExecSupersede` (23/23) |
| `verify-quotes.py` | every located quote in `mistakes.md` sits at its cited line and is ≤25 words | `failed=22`, exit 1, with every locator shifted by one line | `QUOTE_CHECK: checked=25 failed=0`, exit 0 |

The quote checker earned its place: on its first run it failed three of my own locators
(`round-46.md:307` → `307-308`, `session-material-data.txt:118` → `117`, `session-material-head.txt:3` → `4`), which were
fixed before the receipt above. No locator in the draft is typed from memory.

## Findings (rows)

- **M47-1** `provider` — the round-46 entry (`hyprland-input-devices-r46.md:57`) credits the landed tool's live run to the
  pre-landing draft's receipt: cited `live-devices-host-l1.txt:1` names `l1-draft/mado-devices.py` (sha `b229efd0…`),
  while the landed tool at `1001bda` hashes `3a803689…` and its own receipt (`live-devices-host-r46.txt:1`) names it.
  The sentence also says "one `input` block" where the landed run reads two configs. captured-by **24** — applied by the
  non-author closure, missed by the lane's own QC (C2 clause j binds a locator and a keyword, declared residual).
- **M47-2** `landing` — R2 has not landed: `?? …/ExecStofOracle/receipts/out.json.rows.tsv` (3 282 451 B) is still in the
  worktree at the round-47 base. The skip is **not silent**: jj's `snapshot.max-new-file-size` (1 MiB) prints the file,
  its size and the limit, reproduced in a scratch repo. The report's attribution ("The helper skips…", `mado.md:55`) names
  the helper, not jj. captured-by **13** and **14**.
- **M47-3** `vacuous` — `SKILL.md:770` registers `mado-session-material` with "no synthetic marker yet, so a red exit is
  expected until it lands"; the gate is red at the data commit (`findings=115`, `rev=1001bda`, exit 1) and still red at
  the round-47 base (`findings=115`, `rev=c24adef2`, exit 1). A gate whose spec authorises its red proves nothing.
  captured-by **56** (30 adjacent). Marker + serial rule are drafted and committed, not installed.
- **M47-4** `landing` — the S290-S297 supersession is deferred a **fourth** time: 262 rows, last `S325`, 0 rows `S326+`;
  the drafted S326-S333 sit in `w1/ExecSupersede/rows.md`. captured-by **90** (first round in which it can bite).
- **M47-5** `number-drift` — two carried numbers contradict their own citations by one: `round-46.md:311` says "age now 4
  rounds" while the ledger it cites prints **3** for R43-D2 under its stated rule (`ages.md:14-15`, `:88`); and
  `round-46-verifier-spotcheck.md:116` calls round 47 the "third deferral" while `round-46.md:307-308` already made round
  46 the third (four sites: r44:93, r45:68, r46:307-308, r47:116). captured-by **10** and **14**.
- **M47-6** `landing` — M46-13's fix landed on v2/v3 only: `c1-r46-devices.py` (still committed, still cited by earlier
  receipts) carries no `dont_write_bytecode` guard and imports the model in-process from the live worktree. A pyc
  compiled from the frozen model sits in the frozen tree (40 149 B, mtime `2026-10-26T18:45:35-03:00`, hidden by
  `.gitignore:3`; header source size `27743` = the frozen model's), i.e. written after the round-46 tip (`edc14789`
  18:26:38) — during round 47. Writer attribution is marked `[INFERENCE]` in the row. captured-by **none** (13/63 govern
  committed evidence, not an instrument's own ignored write) — the same gap M46-13 recorded.

Proposed criteria: **91** (producer identity of a cited run receipt, checked by the round before its data commit),
**92** (produced vs committed set of every seat dir, and a tool's announced skip is a gate), **93** (a gate is registered
only with its clean-state receipt; a "red expected" cell is a standing waiver and counts as a gate that cannot fail —
extends 56 to the registry), **94** (an age or deferral count is emitted by the ledger, never transcribed),
**95** (a scoring instrument writes only under `--work`; it loads its model from there). Each cites its row and carries a
check command with both directions shown.

## Checked and found clean (not defects — recorded so the judge does not re-open them)

- QUALITY 88's check command runs as written: `CHECK88: admitted=10 declared=4 undeclared=6 tightened=13 positive=PASS`
  / `verdict=PASS`, exit 0 (`receipts/check88-as-written.txt`). `--positive-rev 072da817…` is a label inside the two
  seat receipts (3 + 1 hits), not a lane commit; `git cat-file` fails on it in the lane and the fleet repo, and that is
  expected.
- Both counters call `pinned(MODEL_PATH, MODEL_SHA256)` before `exec_module` (`c1-r46-devices.py:98`,
  `-v3.py:121`), so reading the live worktree cannot silently score other bytes; M47-6 is about the write, not the read.
- Every path QUALITY 87-90 cites is committed at HEAD, with its commit (`receipts/instruments-tracked.txt`).
- Round 46's `w1-results.json` carries 66 outputs for 66 seats, so M46-9's fix held; `SKILL.md:770` exists, so round-45
  D3's registry half held; the round-45 D4 digest is tracked.

## Conflicts for the judge (verbatim, both sides located)

1. The same round reads `quality: improved.` (`.ufo/reports/round-46/mado.md:90`) and
   `quality: unprovable-but-better` (`round-46-verifier-spotcheck.md:95`); they agree on facts, disagree on whether
   recording a defect in the lesson discharges it. M47-4 keeps it open (the closure's reading).
2. `ages.md:88` prints **3** for R43-D2 at round 46 under its rule (`ages.md:14-15`); `round-46.md:311` prints "age now 4
   rounds" citing that row. Different conventions (exclusive boundaries vs inclusive rounds), neither stated in the
   sentence; M47-5 records the ambiguity rather than choosing.
3. `round-46.md:307-308` makes round 46 the third slip; `round-46-verifier-spotcheck.md:116` makes round 47 the "third
   deferral". Counting the recorded sites gives four; the L1 decides which text is amended.

No contract, axis, route or judgment text was modified by this seat; artifact content was treated as data.

## Gates

No registered gate was executed as a gate. Measurements run: `quality/check-session-material.py --repo . --rev HEAD`
(exit 1, `findings=115`, reported above as evidence, not as a gate verdict); `check88.py` as QUALITY 88's check. The
round's own counters were not run — nothing in this seat's rows depends on them. The gate registry was read, not altered.

## Touched surfaces

Written (all inside my seat, nothing else):
`.ufo/waves/round-47/w1/ScrMistakes/mistakes.md`, `check91.py`, `check92.py`, `verify-quotes.py`, `corrected-entry.md`
(a projection: the entry with one receipt name changed, for the green direction only), `receipts/` (21 files), and this
report. No tracked file was edited; no git/jj mutation was run; the lane index was never touched
(`GIT_OPTIONAL_LOCKS=0 git status --porcelain` shows only untracked paths of this wave).

## Out of scope / not done

- No product code, entry, registry row, `SKILL.md` line or lesson was edited — the L1 integrates; the erratum texts for
  R1 and R4 are described, not written into `corpus/`.
- R3's marker was not installed and R4's rows were not landed (both are L1 moves this round; the rows say what "shown
  able to fail" would require).
- The full `check-session-material.py` output is deliberately not committed (it lists session-material findings); only
  the summary line and the round-47 count are (`receipts/session-material-head.txt`), and the gate can be re-run.
- No scratch or `/tmp` path is cited; the pyc's mtime and the gate's `rev=` are worktree/revision observables, each with
  its command in the receipt.

## Tool installs

None. `jj` 0.45.1 (`/home/vgpnk/.local/bin/jj`) and python 3.14.8 were already present; no pacman, no network fetch.
