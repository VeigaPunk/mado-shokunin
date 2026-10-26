# Routed-defect ages — rounds 38–45 (read at round 46, 2026-10-26)

Source: `considerthese/2026-10-26.md` proposal 3 — "keep an age count per routed item so long-open ones
stand out". This file is that count, built from the eight non-author spot-checks r38–r45 and the closure
records the lane wrote in `corpus/lessons/round-{39,40,41,43,44,45}.md`.

## Method

- **Population.** Every bullet in section 6 of `corpus/lessons/round-{38..45}-verifier-spotcheck.md`
  (the section each closure routes "lane fixes next round" into). 45 bullets total.
- **Locators are computed**, never typed: line numbers come from `awk '/^## 6\./,0'` over each spot-check
  and `grep -n` over each lesson; every command and its output is in
  `.ufo/waves/round-46/w1/ScrRoutedAges/receipt.txt`.
- **Age convention.** `age = 46 − first_routed_round`, i.e. the number of round boundaries the item has
  survived at this round's freeze. Round 46 is running; a round-45 item therefore has age 1, a round-38
  item age 8. For closed items the column is `closed_round − first_routed_round`.
- **Dedup.** Later spot-checks sometimes re-list an earlier item with no state change (r42:90, r43:111,
  r44:102 restate r41:79; r44:117 and r45:118 restate r43:100 and r44:118). Those are marked `carried`
  and keep the first router's age; they are not counted twice.
- **Non-actionable rows** — operator-owned SHONEN boxes, driver-side notes, orchestrator spawn floors —
  are listed but excluded from the open count, because the lane cannot close them.
- No counter, tool, compositor read or host query was run. Nothing was re-run to decorate a status.

## Table 1 — every routed bullet, r38 → r45

`first routed` = spot-check file (`S38` = `round-38-verifier-spotcheck.md`) + computed line.

| id | defect (short) | first routed | state | closed in / evidence |
|---|---|---|---|---|
| R38-1 | re-register the C1 predicate, verify 19/19 | S38:84 | closed, age 1 | r39 — `receipts/c1-after-tip.txt` reads `controls=19 correct=19/19` (S39:33); freeze `457d1b1`, attempt-2 `d9b4e4a` |
| R38-2 | fleet-report addendum-5 erratum | S38:85 | closed, age 1 | r39 — `round-39.md:86-87` (erratum from seat `ScrErratum`) |
| R38-3 | regenerate `eventq-live-ss.txt` census-only + commit the after-receipt | S38:86 | **half closed, residual OPEN** | regeneration r39 (`round-39.md:88-89`, `ExecEventqSnapshot`); residual = the committed bytes themselves (Table 2) |
| R38-4 | composite of 10 instrument residuals (RevC1v3 F1/F2/F4, RevC2v3 F1/F2, MutC1/MutC2 gaps, LabratProcProof, LabratClockSkew, f551b70 request-ground set, SCORECARD staleness) | S38:87 | **OPEN** (only the SCORECARD sub-item closed, `round-39.md:90`) | no lesson r39–r45 names `RevC1v3`, `LabratProcProof` or `LabratClockSkew` again — `git grep -l` over `corpus/lessons` returns only S38:87's own file |
| R38-5 | 3 uncommitted seat reports in the worktree | S38:88 | closed, age 1 | r39 — `round-39.md:89-90`, landed in `457d1b1` |
| R39-D1 | C2 registered against a counter path absent at freeze | S39:93 | closed, age 1 | r40 — `round-40.md:68`; receipt `receipts/freeze-counter-check-v2.txt` @ `91f0a2b` |
| R39-D2 | S224 over-labelled "fabrication class" | S39:94 | closed, age 1 | r40 — `round-40.md:60` (append-only correction; lesson commit `3c80537`) |
| R39-D3 | 3 dead seats; write reports before returning | S39:95 | closed, age 1 | r40 — `round-40.md:70` (63 of 64 reports; the foreign path became QUALITY 71) |
| R40-1 | untracked `w1.ready.dispatched` | S40:91 | closed, age 1 | r41 — `round-41.md:59`, marker tracked in `60c3914`; recurred the same round as M41-3 → QUALITY 70 |
| R40-2 | commit the tip axis receipt `rev=fb49621…` | S40:92 | **OPEN** | r41 says "still open" (`round-41.md:62`); `ls .ufo/waves/round-40/receipts | grep -c axis` → `1` (`axis-base.txt`, no `axis-<sha>` receipt) |
| R40-3 | commit the fresh-nonce re-run of both v2 counters | S40:93 | **OPEN** | `round-41.md:65` "not done"; nonce `35a126304f681969` occurs in one tracked file only — the spot-check prose itself (`git grep -l` → `corpus/lessons/round-40-verifier-spotcheck.md`) |
| R40-4 | SHONEN boxes stay `[~]` | S40:94 | operator-owned | `round-41.md:68`; still four `[~]` at r45 (`round-45-verifier-spotcheck.md:121-122`) |
| R41-1 | two untracked scratch files `s-grow`, `s-size` | S41:77 | closed, age 1 | r42 — `round-42-verifier-spotcheck.md:24` ("absent; tree clean") at `a62f2e0` |
| R41-2 | tighten C1 (selftest teeth) and C2 (quote ends, captions) | S41:78 | **OPEN** | successors r43-D6 (S43:107), r44-D5 (S44:114); r45 rebuilt v2 counters for a new tool (`quality/counters/c1-r45-monitors-v2.py`) without retiring this row |
| R41-3a | S041 held-row citation | S41:79 | **OPEN** | carried verbatim at S42:90, S43:111, `round-44.md:102`; no state change recorded |
| R41-3b | tool ergonomics O1–O5 | S41:79 | **OPEN** | same carries |
| R41-4 | `PROVINCE.md:75` → `75-76` in the lesson citation | S41:80 | **OPEN** | `corpus/lessons/round-41.md:48` still writes `PROVINCE.md:75` at HEAD |
| R42-1 | no lesson, no `## Mistakes`, no sourced claim | S42:82 | closed, age 1 | r43 — `round-43.md:97` (this lesson is the repair; M43-4) |
| R42-2 | two prose locators off by 30+ lines | S42:83 | closed, age 1 | r43 — `LOG.md:2487` correction entry, commit `2a3707c` |
| R42-3 | C1 control tally stated three ways | S42:85 | closed, age 1 | r43 — `round-43.md:101`; definition in `.ufo/waves/round-43/registration.md:59` (`b2e2efd`) |
| R42-4 | SHONEN box 2 pointer does not resolve | S42:87 | closed, age 1 | r43 — `receipts/live-geometry-host.txt` @ `1959770` |
| R42-5 | L2 floor unmet: 0 seats spawned | S42:88 | orchestrator-side, status-neutral | recurs as the seat-floor half of r45-D1 (41 < 64) |
| R42-6 | attribution note on `8af0263` | S42:89 | no action (note only) | `round-43.md:107` |
| R42-7 | "still open from round 41" | S42:90 | carried (duplicate of R41-3a/3b, R41-4) | — |
| R43-D1 | under-cited refusal reason + mis-mapped receipt | S43:97 | closed, age 1 | r44 — `round-44.md:92`, errata E1/E2 at `round-44.md:196-206` (`74c606a`) |
| R43-D2 | S293 title / S290–S297 supersession | S43:100 | **OPEN** | deferred at `round-44.md:93` and again at `round-45.md:68`; `corpus/SOURCES.md:242` still reads "the client's request as input" |
| R43-D3 | SKILL.md TILED licence cell | S43:102 | closed, age 1 | r44 — `round-44.md:94`, correction in `e467892`; `grep -c 'read TILED as "not floating" only' SKILL.md` → `1` |
| R43-D4 | entry bare-path pointers + off-by-six locator | S43:104 | closed, age 1 | r44 — `round-44.md:95` (M44-4) |
| R43-D5 | seat count and published mistake range | S43:106 | closed, age 1 | r44 — `round-44.md:96`, errata E3 (`round-44.md:196-215`) |
| R43-D6 | predicate defects: C1 cheats 4/6 MET, C2 do-nothing 14/14 | S43:107 | closed by rebuild + retirement, age 1–2 | rebuilt r44 (`round-44.md:98`); residue listed as r44-D5; retired r45 (`round-45.md:68`, "round-44 counters not reused") |
| R43-D7 | no committed axis receipt at the tip | S43:109 | closed, age 1 | r44 — `receipts/axis-tip.txt` @ `8ac15c41`; the naming defect then closed r45 (`4d22eeb`, header names `ac3f9de`) |
| R43-D8 | duplicate driver `complete` line | S43:110 | driver-side, no action | `round-44.md:99` |
| R44-D1 | 4 live window titles in two tracked dumps | S44:98 | closed, age 1 | r45 — `round-45.md:66` (M45-1); verified at HEAD: `grep -c '"title"'` → `0` on both dumps |
| R44-D2 | SCORECARD after-values missing | S44:107 | closed, age 1 | r45 — `round-45.md:66` |
| R44-D3 | tip receipts name a pre-tip commit | S44:110 | closed, age 1 | r45 — `round-45.md:67-68`; `receipts/axis-tip.txt:1` names `ac3f9dee…` |
| R44-D4 | nonce-dependent "before" share | S44:112 | closed, age 1 (repair) | M45-6 (`round-45.md:61-62`): v2 before-state is deterministic |
| R44-D5 | open predicate defects in the r44 counters | S44:114 | closed by retirement, age 1 | `round-45.md:68` ("round-44 counters not reused"); defects recorded, not repaired |
| R44-D6 | S290–S297 supersession (still open from r43) | S44:117 | carried (duplicate of R43-D2) | — |
| R44-D7 | `w2/ConnCalibration.md` content mismatches | S44:118 | **OPEN** | `round-45.md:68-70` (recorded, not corrected) |
| R45-D1 | 41 seats < 64 floor; w2 falsification never ran | S45:102 | **OPEN** (in flight) | this round runs the w2 falsification: `.ufo/waves/round-46/registration.md:67-68` |
| R45-D2 | M45-2 undercounts the monitor-serial copies | S45:105 | **OPEN** | no r46 closure recorded at the freeze commit; the serial is deliberately not reproduced here |
| R45-D3 | gate has no `SKILL.md` registry row; 48 findings untriaged | S45:110 | **OPEN** | `grep -c check-session-material SKILL.md` → `0` at HEAD `e0be61e4` |
| R45-D4 | 4 MB untracked `MutC1Counter/results.json` | S45:114 | **OPEN** (partial) | file gone; `git status --porcelain` → `?? .ufo/waves/round-45/w1/MutC1Counter/results.digest.txt` — the digest line is written but **not committed** |
| R45-D5 | say the `output: null` seats are not evidence | S45:116 | **OPEN** | a disclosure exists at `.ufo/waves/round-45/registration-v2.md:7`; no wave README (`ls .ufo/waves/round-45 | grep -ci readme` → `0`) and no r46 lesson yet |
| R45-D6 | carry r44-D6 and r44-D7 | S45:118 | carried (duplicates) | — |

## Table 2 — OPEN ledger (deduped, lane-actionable)

| id | defect (short) | first routed | rounds open | latest state evidence |
|---|---|---|---|---|
| R38-3 | 190,816 B `ss -xpa` table sits in the public tree and is not mentioned in `LOG.md` | S38:86 | **8** | `stat -c %s` → `190816` at HEAD; `git grep -c eventq-live-ss HEAD -- LOG.md` → exit 1 (no line) |
| R38-4 | 10-id instrument-residual composite never reconciled | S38:87 | **8** | no mention after S38 (grep over `corpus/lessons`) |
| R40-2 | `fb49621` tip axis receipt never committed | S40:92 | **6** | `round-40/receipts` has one `axis` file, the base |
| R40-3 | fresh-nonce re-run receipt never committed | S40:93 | **6** | nonce appears only in the spot-check prose |
| R41-2 | C1/C2 predicate tightening | S41:78 | **5** | re-routed as r43-D6, r44-D5; rebuilt for new counters only |
| R41-3a | S041 held-row citation | S41:79 | **5** | carried, unchanged |
| R41-3b | tool ergonomics O1–O5 | S41:79 | **5** | carried, unchanged |
| R41-4 | `PROVINCE.md:75` → `75-76` | S41:80 | **5** | `round-41.md:48` unchanged |
| R43-D2 | S290–S297 supersession / S293 title | S43:100 | **3** | deferred twice; `SOURCES.md:242` unchanged |
| R44-D7 | ConnCalibration mismatches | S44:118 | **2** | recorded, not corrected |
| R45-D1 | w2 falsification + 64-seat floor | S45:102 | **1** | being executed in this wave |
| R45-D2 | serial-copy undercount | S45:105 | **1** | not closed at the freeze |
| R45-D3 | gate registry row + 48-finding triage | S45:110 | **1** | `SKILL.md` count 0 |
| R45-D4 | `results.json` / digest commit | S45:114 | **1** | digest untracked |
| R45-D5 | `output: null` note in README/lesson | S45:116 | **1** | no README, no lesson |

## Count and ages

- 45 routed bullets; **23 closed** (22 within one round, 1 at two), **15 open**,
  7 bullets that are non-actionable or carried duplicates (42 ledger rows, of which 38 lane-actionable).
  Two of the 23 were closed by retirement rather than repair (R43-D6's residue, R44-D5).
- Open ages: `8, 8, 6, 6, 5, 5, 5, 5, 3, 2, 1, 1, 1, 1, 1` — **sum 58, mean 3.87, median 5,
  oldest 8** (R38-3 residual, R38-4).
- Distribution: 2 items ≥ 8 rounds old, 2 at 6, 4 at 5, 1 at 3, 1 at 2, 5 at 1.
- If only completed rounds are counted (to the r45 spot-check), every age drops by 1: oldest 7,
  open mean 2.87.

## What the age count shows

1. **Item identity, not the defect class, is what gets lost.** R38-4 routed ten distinct instrument
   defects as one bullet; none of the ten ids appears again, yet the same class returned as r43-D6 and
   r44-D5. A class can be re-fixed forever while its routed instance stays formally open.
2. **A repeated bullet looks new.** R41-3 has been re-listed verbatim in four consecutive spot-checks
   (S41:79, S42:90, S43:111, `round-44.md:102`); because section 6 is rebuilt each round, nothing in
   the record says "this is round five of the same item".
3. **Partial closure reads as closure.** R38-3's regeneration half was done in r39 and the leak half
   was never mentioned again; R45-D4 removed the 4 MB file but left the digest uncommitted. Both read
   as closed in a per-round skim.
4. **Legitimate closures by retirement are unlabelled.** R43-D6 and R44-D5 were closed by not reusing
   the counters. That is a defensible disposition, but without a `retired` state the next round's
   fresh counter defect looks unrelated to the old one.
5. **Seven of 45 bullets cannot be closed by the lane** (SHONEN, driver, spawn floor). Without an
   owner column they inflate the "still open" impression as much as real defects do.

## Proposed QUALITY criterion 87

> **87. Every routed defect has one row in a committed ledger, and its age is printed each round.**
> `corpus/QUALITY.md` next free number is 87 (`grep -n '^86\.' corpus/QUALITY.md` → line 420).
>
> The ledger `quality/routed-defects.tsv` carries one row per routed item with columns
> `id, first_round, first_locator, defect, owner (lane|operator|driver|orchestrator), state
> (open|closed|retired), closed_round, closed_commit, evidence`. Section 6 of each new spot-check is
> reconciled row-for-row: a bullet with no row, a row whose `first_locator` does not resolve by
> `grep -n` in that round's spot-check, or a repeated open item written as a new row instead of a
> carry of the existing id is a violation. A row moves to `closed` only with
> `git cat-file -e <closed_commit>:<artifact>`; a row closed because the instrument was retired
> carries `state=retired` and the receipt that retired it. Each round's lesson prints one computed
> line at its own revision —
> `ROUTED_AGES: bullets=<n> rows=<n> actionable=<n> closed=<n> open=<n> owner=<n> oldest=<age>@<id> mean=<x>`
> — and every open row with `age >= 4` prints `STALE <id> age=<n>`; the round then closes it,
> re-routes it with a written reason, or records it as deliberately carried. Age is
> `round − first_round`, computed from the ledger, never typed.
>
> Check (proposed, not implemented):
> `python3 -I quality/check-routed-ages.py --repo . --rev <rev> --ledger quality/routed-defects.tsv --spotchecks corpus/lessons/round-<38..N>-verifier-spotcheck.md`
> — it recomputes every `first_locator` with `grep -n`, diffs the newest section 6 against the ledger,
> verifies every `closed_commit:artifact` with `git cat-file -e`, and prints the `ROUTED_AGES` line
> plus `STALE`/`UNLEDGERED`/`DANGLING` rows; any of those rows is a violation.
>
> Shown able to fail (seed from this round's reading, at `b22ea56`): the ledger built from Table 1
> prints `bullets=45 rows=42 actionable=38 closed=23 open=15 owner=4 oldest=8@R38-3 mean=3.87`; a ledger that
> drops R38-4 as "old" prints `open=14` and must be rejected, and a ledger that adds R41-3 again
> under r44 prints `open=16` with a duplicate id and must be rejected. Both failure modes are
> observable without any host access.
>
> Ground: this reading (`considerthese/2026-10-26.md` proposal 3); the five findings above.

## Limits

- Statuses are as the closure documents record them. I re-opened **six** current-state claims myself
  (both r43 client dumps' title count, `eventq-live-ss.txt` size and `LOG.md` silence, `SOURCES.md`
  S293, the `check-session-material` row, the r45 digest's commit state, `PROVINCE.md:75`). The
  remaining "closed" rows cite their closure record, not a re-read artifact; each is marked with the
  lesson line that records it.
- Where a closure names no commit (R39-D2, R42-2's content, R43-D3's cell text), the table cites the
  lesson line or the commit that introduced the closing file, not a counter receipt.
- R45-D2's evidence is the spot-check's own count (24 copies). I did not re-grep the serial, because
  the serial must not be written anywhere.
- Round 46 is in progress; its own routed rows will appear in the r46 spot-check and are outside this
  table.
