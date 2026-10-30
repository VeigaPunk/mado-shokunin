# R56W3ScribeLessonA2 — attempt-2 lesson skeleton for `corpus/lessons/round-56.md`

Seat: scribe. Wave: w3 (attempt 2, 2026-10-30). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Tip scored/archived at: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. No tracked file was edited; no git/jj mutation was
run against the lane, the fleet repo or any sibling lane; no tool was installed; no scratch directory was needed (no
temporary file was created anywhere), so there is nothing to clean up.

## What I attacked

The item is a drafting item, not a measurement: **draft the attempt-2 lesson skeleton for `corpus/lessons/round-56.md`
(append section; the L1 fills findings)**. I attacked it on three axes:

1. **Completeness** — does the skeleton carry all four named components (section header line, wave paragraph scaffold with
   a seat/role/dead table keyed to seat names, a `## Gate (attempt 2)` scaffold with admit/reject slots for S396/S397 plus
   the re-verification receipts, a `## Registry changes (attempt 2)` paragraph scaffold)?
2. **No false settledness** — is every pending fact an explicit `<FINDINGS>` placeholder, so that nothing in the append
   block reads as admitted, measured or decided before the L1 fills it?
3. **Truth of the structural facts the skeleton does assert** — the seat roster and role mix (64 seats), the attempt-1 wave
   shape, the frozen revisions, the row count at the tip, and the receipt values quoted as prior evidence.

## What I did

Read-only reconnaissance first: the frozen contract (`claims-frozen-v2.md`, `registration-v2.md`, `registration.md`), the
attempt-1 lesson at the tip, the wave-3 seat roster (`w3-spec.json`), the attempt-1 and attempt-2 receipts
(`receipts/at-final.txt`, `receipts/attempt2-l1.txt`, `receipts/census-before-a2.txt`), the L1's draft rows
(`attempt2/s396-s397-draft.md`) and the sibling scribe/reviewer seat prompts (so the skeleton's fill map points at the right
deliverables and does not duplicate them). Then wrote the skeleton and verified its structure mechanically.

The skeleton keeps the attempt-1 lesson append-only and untouched: it is a separate file the L1 appends from. It carries
the frozen revisions as context (v1 `3423ae28`, v2 `323a69c9`, errata `15015e77`), states that attempt 2 does NOT re-freeze
or widen any predicate, and gives the L1 a fill map naming, for every placeholder, the seat report or receipt that fills it.

## Exact commands and output (trimmed to decisive lines)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56 && python3 -I -c "
import json,collections
s=json.load(open('w3-spec.json')); c=collections.Counter(it['role'] for it in s['items'])
print('items',len(s['items'])); print(dict(c))"
items 64
{'executor': 16, 'mutation-tester': 7, 'critic': 6, 'reviewer': 15, 'scout': 10,
 'connector': 2, 'simplifier': 1, 'scribe': 4, 'sentinel': 1, 'revenger': 2}
```

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/SOURCES.md \
    | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
332
```

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/lessons/round-56.md | grep -n '^## '
8:## Gate
57:## Registry changes old→new
64:## Mistakes
85:## Wave-2 findings applied and routed
91:## Considerthese and assimilation
96:## Census
```

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/lessons/round-55.md | grep -n '314\|317' | head
25:- Rows `314 → 317` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); new ids S378–S380, tier A, `mined`.
42:Start census command `… sources-census.sh validate …` → exit 0, `mado ok` (…/round-55/receipts/census-before.txt, 314 rows). End census: … (317 rows).
```

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git ls-tree --name-only 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 .ufo/waves/round-56/receipts/ && git status --porcelain | head -20
… at-final.txt axis-tip.txt before.txt c3-base-v2.txt census-before.txt freeze-verify-v2.txt freeze-verify.txt
  holdout-preveal.txt live-watchplan.txt pins-extra.sha256 pins.sha256 scope-replay-r55.txt selftest-before.txt
  used-by-old-to-new.md witness-v2.txt witness.txt
?? .ufo/waves/round-56/attempt2/
?? .ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html
?? .ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html
?? .ufo/waves/round-56/fixtures/c2-divergences/
?? .ufo/waves/round-56/make-w3-spec.py
?? .ufo/waves/round-56/receipts/attempt2-l1.txt
?? .ufo/waves/round-56/receipts/census-before-a2.txt
?? .ufo/waves/round-56/receipts/divergences-b.txt
?? .ufo/waves/round-56/w3-dispatch.json  ?? .ufo/waves/round-56/w3-run.err  ?? .ufo/waves/round-56/w3-spec.json
?? .ufo/waves/round-56/w3.ready  ?? .ufo/waves/round-56/w3.ready.dispatched  ?? .ufo/waves/round-56/w3/
```

```
$ python3 -I - <<'PY'   # structural check of the deliverable
t=open('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeLessonA2/receipts/lesson-a2-skeleton.md').read()
print('bytes',len(t)); print('FINDINGS',t.count('<FINDINGS'))
print('header',t.count('## Attempt 2 (2026-10-30 re-dispatch) — wave w3 settled'))
print('gate h2',t.count('## Gate (attempt 2)')); print('reg h2',t.count('## Registry changes (attempt 2)'))
print('seat rows',len([l for l in t.split('\n') if re.match(r'^\| \d+ \| `R56W3',l)]))
print('mentions != 1 per spec seat',[n for n in names if t.count('`%s`'%n)!=1])
PY
bytes 19916
FINDINGS 266
header 1
gate h2 1
reg h2 1
seat rows 64
mentions != 1 per spec seat []
```

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeLessonA2/receipts/lesson-a2-skeleton.md`
  — the append block (between `--- BEGIN APPEND BLOCK ---` and `--- END APPEND BLOCK ---`) plus the scribe-only fill map.
  Contents: the exact section header `## Attempt 2 (2026-10-30 re-dispatch) — wave w3 settled`; the wave paragraph
  (attempt-1 shape → attempt 2 = one v2 wave, 64 seats, role mix, and `<FINDINGS>` slots for seats reported / dead /
  results file / tip sha); the 64-row seat table (`# | seat | role | reported | dead | lesson input`, every cell a
  `<FINDINGS>` placeholder); `## Gate (attempt 2)` with Admitted (S396, S397 rows + a two-row quote table each), Rejected
  (reason + **Flip:** shape), and the re-verification receipts table (C1 counter, C1 controls, C2, C3 counter, C3 controls,
  selftest, index, tool ledger, census — each with the frozen command, an `<FINDINGS>` result line, seat and receipt path),
  plus the C3 caveat that a `used-by` path outside the entry set flips `TARGET_MET`;
  `## Registry changes (attempt 2)` (`319 → 332` stayed; `332 → 334` conditional on S396/S397 landing `queued` with
  `used-by —`; old→new table with `<FINDINGS>` cells).
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeLessonA2.md`.

## Findings (each with the input that shows it and a severity)

- **F1 — the attempt-2 evidence is uncommitted at the tip (weakens the attempt-2 provenance, not a frozen claim).**
  Input: `git status --porcelain` above — `attempt2/`, `fetch/man7-*.html`, `fixtures/c2-divergences/`,
  `receipts/attempt2-l1.txt`, `receipts/census-before-a2.txt`, `receipts/divergences-b.txt`, `w3-spec.json`,
  `w3-dispatch.json`, `w3/` are all untracked while the tip is `0f3a5436`. Consequence for this seat: the skeleton cannot
  cite a commit sha for the attempt-2 receipts, the S396/S397 pins or the wave roster, so those are `<FINDINGS>` slots, and
  the L1 must commit them before the lesson cites them. Severity: weakens the claim (provenance), blocks nothing that is
  frozen.
- **F2 — the C3 counter and the C3 harness fail closed when the frozen base is not present in the scratch repo (weakens
  the attempt-2 C3 re-verification if a seat does not fetch the base).** Input: `.ufo/waves/round-56/receipts/attempt2-l1.txt`
  — `$ c3 counter` → `c3-r56-used-by.py: setup error: base revision objects are absent: fail closed`, `rc=2`; `$ c3 controls`
  → `SETUP: frozen base revision 13f0acbe3a15da2d9c08357a576d91dcadc85273 is not readable in /fast/scratch/hyaku/mado-r56/L1/l1-verify
  (control 1 cannot run)`, `rc=0`. The same receipt records the passing re-runs after the base was fetched into the scratch
  repo (`MADO_USED_BY: … missing=0 extra=0 … exempt=24 verdict=TARGET_MET`, `controls=9/9 verdict=OK`). The skeleton's
  re-verification table names the frozen command for each seat but does not tell the L1 that a scratch export of the tip
  alone is not enough for C3. Severity: weakens (an attempt-2 C3 re-run that omits the base fetch produces a setup
  failure, not a counter verdict).
- **F3 — the S396/S397 byte hashes and quotes are L1-authored and not yet confirmed by an independent fetch (blocks the
  admission slots, not the lesson scaffold).** Input: `.ufo/waves/round-56/attempt2/s396-s397-draft.md` gives
  `sha256:98fe7feb…c3d6d` (11,345 B) and `sha256:f9e12387…52d8a1` (14,694 B) with candidate quotes at lines 88/93 and
  160/164/171. The skeleton's Admitted slots label both hashes "L1 draft byte values (NOT yet confirmed by an independent
  fetch)" and keep the quote text, pin line, "why the lane lacked it", status/tier/used-by and the second fetch as
  `<FINDINGS>`, with a fill map naming `R56W3ScribeGateA2`, `R56W3ScoutNewSrc1`, `R56W3ScoutNewSrc2` and
  `R56W3RevLessonGate`. Severity: blocks the claim (the admission of S396/S397) until a second independent fetch agrees.
- **F4 — S396/S397 must land `queued` with `used-by —`, or the C3 `extra` leg flips (weakens the C3 target if the rows
  are landed otherwise).** Input: `attempt2/s396-s397-draft.md` ("the frozen C3 counter's `extra` leg counts any used-by
  path outside the entry set, so a lesson path in `used-by` would flip `TARGET_MET` to `TARGET_MISSED` at the new tip") and
  the frozen definition in `registration-v2.md` §C3-v2 (`extra` = path in `USEDBY(S)` and path not an ENTRIES member).
  The skeleton's Registry-changes section therefore keeps `319 → 332` as stayed and makes `332 → 334` conditional on the two
  rows landing `queued` with `used-by —`. Severity: weakens the claim if ignored; the skeleton is written so it cannot be
  ignored silently.
- **F5 — the round-55 lesson still carries stale row counts; that correction does not belong in this skeleton (cosmetic
  here; a routed defect for its own seat).** Input: `git show 0f3a5436:corpus/lessons/round-55.md | grep -n '314\|317'`
  → line 25 "Rows `314 → 317`" and line 42 "… 314 rows … (317 rows)", while the registry has had 332 rows since round 56
  (332 at the tip). The owed append-only correction targets `corpus/lessons/round-55.md` and is owned by
  `R56W3ExecInherited` (deliverable `w3/R56W3ExecInherited/corrections/round-55-append.md`); the skeleton's fill map
  points at that seat and explicitly keeps the correction out of the round-56 file. Severity: cosmetic for this seat.
- **F6 — no wave-results artefact exists for w3 yet, so the "wave settled" wording is provisional (informational).**
  Input: the wave directory holds 64 seat directories and 57 `R56W3*.md` report files at the time of writing
  (`ls .ufo/waves/round-56/w3/ | grep -c '^R56W3'` → 57) and no `w3-results.json`; attempt 1's wave 2 likewise never wrote
  `w2-results.json` (`receipts/at-final.txt`, last line). The skeleton's "seats reported / dead / results file" line keeps
  all three as `<FINDINGS>` and the header line carries the spec's fixed wording "wave w3 settled" as instructed.
  Severity: informational.

## What I did not verify

- I did **not** re-run any frozen counter or harness (C1, C2, C3, selftest, index, ledger, census). This seat drafts prose
  scaffolding; the re-verification receipts quoted in the Gate section are the attempt-1 `receipts/at-final.txt` and the
  attempt-2 `receipts/attempt2-l1.txt` as read, not as re-measured by me.
- I did **not** verify any wave-3 seat's finding, adjudication, quote, byte hash or mutation result; every such slot in the
  skeleton is a placeholder, and the seat table's `lesson input` column is entirely `<FINDINGS>`.
- I did **not** confirm S396/S397's quotes, byte counts or 11-cell row shapes, and did not fetch either URL (the pinned bytes
  under `.ufo/waves/round-56/fetch/` are untracked; I read the L1's draft values only).
- I did **not** evaluate the attempt-2 `used-by` hedge audit, the C3 allowlist adjudication, the C1 forge re-attack or the
  C2 cheat re-verification; those seats own their verdicts.
- I could not settle the wave's own outcome (which seats report, which are dead, whether a `w3-results.json` will be
  written) — that is the operator's or the L1's to record, and the skeleton says so in place of a guess.
- No tool was installed or upgraded this seat (nothing was needed beyond `python3 -I`, `git` read-only and `grep`), so the
  operator tooling-authorization rule is not engaged; no pacman transaction was attempted.

## Note on role

This seat is a scribe: it drafted a skeleton for the L1 to fill. It is **not** a non-author reviewer of the lane — no
finding above is an independent verification of the round's claims, and every verdict in the skeleton is a slot, not a
judgment.
