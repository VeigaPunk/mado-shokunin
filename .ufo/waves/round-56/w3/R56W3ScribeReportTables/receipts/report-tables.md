# Round 56 mado — report evidence tables (attempt 2, wave w3)

Seat `R56W3ScribeReportTables` (scribe). Draft for the round-56 report's three evidence tables.
Every cell carries the revision it was measured at and the receipt or command that produced it.
Cells whose value does not exist yet are `<PLACEHOLDER>` — no value is carried forward as if it
were measured at the attempt-2 final revision.

Revisions used:

| name | value | what it is |
|---|---|---|
| base | `13f0acbe3a15da2d9c08357a576d91dcadc85273` | the frozen base (`frozen-tables-v2.json` `base` / `c3.base_rev`) |
| attempt-1 content revision | `8a7b734627b06583a9106fcc0940f0a180ff331d` | the revision `receipts/at-final.txt` measured at |
| lane tip | `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` | attempt-1 honest-stop commit (LOG, SCORECARD, lesson, wave-2 evidence, final receipts) |
| `<A2FINAL>` | `<PLACEHOLDER>` | the attempt-2 final revision — **not yet landed**; `git log 0f3a5436..HEAD` is empty and `origin/master` still prints `0f3a5436` |

Claim surfaces (`quality/`, `tools/`, `corpus/`, `.ufo/waves/round-56/frozen-tables-v2.json`,
`.ufo/waves/round-56/c3-name-only.tsv`) are byte-identical between `8a7b7346` and the lane tip
`0f3a5436`; the only difference is one line of `corpus/lessons/round-56.md` (the `## Census`
sentence). Command and output:

```
$ git -C <scratch>/lane diff --stat 8a7b734627b06583a9106fcc0940f0a180ff331d \
      0f3a54361a9824484d0801679ceb1fd8ac7c32e1 -- quality tools corpus \
      .ufo/waves/round-56/frozen-tables-v2.json .ufo/waves/round-56/c3-name-only.tsv
 corpus/lessons/round-56.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

All measurements below were produced by re-running the frozen commands against a read-only
`git clone --shared` of the lane in scratch
(`/fast/scratch/hyaku/mado-r56/R56W3ScribeReportTables/lane`, toplevel asserted equal to the
fixture dir before any git call; the lane itself was never mutated). Full logs:
`receipts/frozen-gates-at-base.txt`, `receipts/frozen-gates-reverified.txt`.

---

## Table 1 — Before → after, one row per claim

The frozen sentences are quoted verbatim from `.ufo/waves/round-56/claims-frozen-v2.md`
(sha256 `187cf3d1fa4c49d112b6b006e1a1df90205e35219c69782196b9e242c31d92e5`), which is never edited.
The **before** column is the base `13f0acbe`; the **after** column is the attempt-2 final revision
`<A2FINAL>`, which does not exist yet. The anchor column carries the attempt-1 measurement
(`8a7b7346`, receipt `receipts/at-final.txt`), re-verified by this seat at the lane tip — the value
the attempt-2 gates will have to reproduce unless attempt-2 edits a claim surface.

| claim (axis) | frozen counting command (from `claims-frozen-v2.md`) | before @ `13f0acbe` | after @ `<A2FINAL>` | anchor: attempt-1 @ `8a7b7346` (receipt `at-final.txt`; re-verified by this seat at tip `0f3a5436`) |
|---|---|---|---|---|
| **C1** coverage (sourced entry) | `python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev <rev> --work <scratch>` → `MADO_AUTORELOAD_ENTRY: rev=<rev> rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`<br>AND `python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev <rev> --work <scratch>` → `MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK` | counter: `rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8 verdict=TARGET_MISSED missed=tables_sha,entry_absent,index` (rc 1; the counter file itself is absent at base — `receipts/before.txt` "absent quality/counters/c1-r56-autoreload-entry.py"; the `tables_sha` leg is itself a consequence of `.ufo/waves/round-56/frozen-tables-v2.json` not existing at base)<br>harness: **cannot be run at base** — `MADO_R56_CONTROLS setup error: .ufo/waves/round-56/frozen-tables-v2.json absent at 13f0acbe` (rc 2)<br>coverage at base: `git grep -liE 'disable_autoreload\|ConfigWatcher\|IN_CLOSE_WRITE\|inotify_add_watch' 13f0acbe -- corpus/knowledge \| wc -l` → **0** (re-derived by this seat: 0 hits for each of the four terms across all 70 base entries) | `<PLACEHOLDER>` — attempt-2 final revision not landed | counter: `MADO_AUTORELOAD_ENTRY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` (rc 0)<br>harness: `MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK` (rc 0; 12 controls each PASS) |
| **C2** operability (capability acquisition) | `python3 -I quality/check-r56-controls.py --claim c2 --repo . --rev <rev> --work <scratch>` → `MADO_R56_C2: rev=<rev> fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET` | harness: **cannot be run at base** — `r56_ctl_c2: setup error: frozen-tables.json is not a regular blob at rev` (rc 2). Tool absent at base (`git ls-tree 13f0acbe tools/` → no `mado-watchplan.py`; `receipts/before.txt` "absent tools/mado-watchplan.py"); by absence `fixtures=0/18` | `<PLACEHOLDER>` — attempt-2 final revision not landed | `MADO_R56_C2: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET` (rc 0); `r56_ctl_c2: sandbox=bwrap fixture_commit=ok control_scores={'const-host': (1, 0), 'empty': (0, 0), 'sibling-reader': (0, 0), 'lookup-committed': (18, 0)}` |
| **C3** registry back-reference consistency (token level, 24 reviewed name-only exemptions) | `python3 -I quality/counters/c3-r56-used-by.py --repo . --rev <rev> --work <scratch>` → `MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none`<br>AND `python3 -I quality/check-r56-controls.py --claim c3 --repo . --rev <rev> --work <scratch>` → `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK` | counter: **cannot be run at base** — `c3-r56-used-by.py: setup error: frozen-tables-v2.json is not a regular blob at --rev` (rc 2). Baseline value of record is the receipt `receipts/c3-base-v2.txt` (base, v2 definitions): `entries=70 rows=319 missing=41 pairs=381 exempt=24 stale=0 conflict=0`; the v1 token count at base was `missing=65` (`receipts/before.txt`)<br>harness: **cannot be run at base** — `SETUP: .ufo/waves/round-56/frozen-tables-v2.json is not a regular blob at 13f0acbe` (rc 2) | `<PLACEHOLDER>` — attempt-2 final revision not landed | counter: `MADO_USED_BY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none` (rc 0)<br>harness: `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK` (rc 0; 9 controls each PASS) |

Harm-watch row (unchanged axes, for the same table's footnote):

| gate | before @ `13f0acbe` | anchor @ `8a7b7346` | re-verified by this seat at tip `0f3a5436` |
|---|---|---|---|
| `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed` (`receipts/selftest-before.txt`) | `460/460` | `460/460` (rc 0) |
| `python3 -I quality/check-index.py --repo . --rev <rev>` | `70/70` (`receipts/before.txt`) | `MADO_INDEX: … indexed=71/71 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | identical (rc 0) |
| `python3 -I quality/check-index-rows.py --repo . --rev <rev>` | — | `rows=71 errors=0 warns=3` (3 pre-existing `cited-glob-nomatch` WARNs) | identical (rc 0) |
| `python3 -I quality/check-tool-ledger.py --repo . --rev <rev>` | — | `LEDGER: population=97 ledger_rows=97 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` | identical (rc 0) |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | `mado ok` rc 0, 319 rows (`receipts/census-before.txt`) | `mado ok` rc 0, 332 rows | `mado ok` rc 0, 332 rows (`census --file` on the tip tree: `rows 332`, `tier.A 320`, `tier.B 5`, `tier.C 7`) |

---

## Table 2 — Round shape

Attempt 1 (2026-10-28, run 11) ran two v1 waves: **w1 43 seats** (`w1-spec.json` `items` = 43;
`w1-dispatch.json` `counts` = `{"spawn": 43, "resume": 0, "total": 43}`) and **w2 35 seats**
(`w2-spec.json` `items` = 35; `w2-dispatch.json` `counts` = `{"spawn": 35, "resume": 0, "total": 35}`)
— **78 dispatched seats** in the round. Wave 1 settled **43/43**: `w1-results.json` carries
`seats: 43` with 43 result rows, all with a non-null `output`. Wave 2 reported **33 of 35**:
33 `<seat>.md` files exist under `w2/`, and the two seats without a report are
`R56W2MutC3Counter` (no directory, no report) and `R56W2MutC2Harness` (directory present, no
report) — both stopped at the operator wrap-up, neither is a finding. **No `w2-results.json`
exists**, so the committed wave-done gate cannot score the round:
`python3 -I quality/check-wave-done.py --repo . --rev 0f3a5436 --round 56` prints

```
WAVE wave=w1 ready=1 results=present seats=43 dispatched=43 settled=43 verdict=OK reason=none
WAVE wave=w2 ready=1 results=absent seats=0 dispatched=35 settled=0 verdict=MISSING reason=results-missing
MADO_WAVE_DONE: round=56 waves=2 settled=1 verdict=MISSING
```

rc 1. The round was therefore closed as an **honest stop**: the claims were never released to a
closure, the wave-2 findings were routed rather than all fixed, and no non-author verified anything
(`receipts/at-final.txt` ends `MADO_WAVE_DONE: not run; operator wrap-up stopped wave 2 (33 of 35
seats reported; w1 settled 43/43, results w1-results.json)`; lane commit `0f3a5436` is titled
"round-56: honest stop at operator wrap-up"; fleet report `.ufo/reports/round-56/mado.md` opens
"**Outcome: honest-stop (operator wrap-up, run 11).**").

Attempt 2 (2026-10-30, re-dispatch of the same round) runs **one v2 wave, w3, 64 seats**
(`w3-spec.json` `items` = 64; `w3-dispatch.json` `counts` = `{"spawn": 64, "resume": 0, "total": 64}`).
Role mix, read from `w3-spec.json` (sha256 `8036cd5efd5a57ca7efe6f999f65dccd7af8a5572fc1fe6622f840835b2e5098`;
the file is still an **untracked working-tree artifact** at the lane tip, `git ls-files` does not
list it): executor 16, reviewer 15, scout 10, mutation-tester 7, critic 6, scribe 4, connector 2,
revenger 2, simplifier 1, sentinel 1 — total 64; attack share (reviewer + critic + mutation-tester)
**28/64**, matching the `attack share 28/64` written in `attempt2/LOG-draft.md`.

**This file's WAVE-DONE is pending.** `w3-results.json` does not exist yet, and the seat reports
are still landing: 38 of 64 `<seat>.md` files were on disk at 2026-10-30T05:16Z (35 at 05:05Z,
32 at 04:55Z — the wave is in flight). By QUALITY 102 a report is committed only after every
dispatched wave has a results file with every seat settled, so the attempt-2 wave-done receipt and
the final settled-seat count are `<PLACEHOLDER>` until `w3-results.json` exists and all 64 seats
report.

---

## Table 3 — Sources & frontier

| item | before | after | provenance |
|---|---|---|---|
| census `validate` (lane root) | `mado ok`, **exit 0**, 38 warning lines (36 W04 + 1 W01 + the `ok` line) — receipt `receipts/census-before-a2.txt` | `<PLACEHOLDER>` (attempt-2 final revision) | `census-before-a2.txt` is an **untracked** working-tree receipt (created 2026-10-30T01:48) and, unlike its predecessor `census-before.txt`, carries **no `rc=` line**; the exit code and the row count are **not** attested by that file. This seat re-ran the identical command against the tip tree: output byte-identical to the receipt (38 lines, diff empty) and **rc 0**; the 332-row figure comes from `census --file` on the tip blob (`file rows 332`) and from `grep -cE '^ {0,3}\|\s*S[0-9]{3,}\s*\|'` → 332 |
| registry rows (`corpus/SOURCES.md`) | 319 rows at base `13f0acbe` | `<PLACEHOLDER>` (334 expected by `attempt2/integration-plan.md` step 3, not landed) | base 319 re-derived by this seat (`git show 13f0acbe:corpus/SOURCES.md`); tip 332 re-derived the same way; `receipts/at-final.txt` records `332` |
| rows added by tier (round-56 total, attempt 1) | base tier counts `tier.A 308, tier.B 4, tier.C 7` → tip `tier.A 320, tier.B 5, tier.C 7` | Δ = **tier A +12, tier B +1, tier C +0**; the 13 new ids are **S383-S395** (A except **S390** = tier B, the inotify(7) man page); all `mined`, opened 2026-10-28 | `census --file` on the base and tip blobs; id/tier parse of both registry blobs by this seat (13 added, 0 removed, 0 kind/tier changed on pre-existing rows) |
| rows added by tier (attempt 2) | — | `<PLACEHOLDER>` — S396/S397 are drafted (`attempt2/s396-s397-draft.md`, tier B each) and not landed (`grep -c 'S396\|S397' corpus/SOURCES.md` → 0) | the two attempt-2 drafts disagree on the landing form: `s396-s397-draft.md` says both rows land `queued` with `used-by —`; `integration-plan.md` gives them `mined` with `used-by corpus/lessons/round-56.md`. A scratch probe of the **integration-plan** form (both rows inserted after S395 inside `## Registry`) gives `MADO_USED_BY: … entries=71 rows=334 missing=0 extra=0 … verdict=TARGET_MET` (rc 0) and census exit 0 — i.e. that form does not break the frozen gates, but the choice is the L1's and is not yet made |
| `used-by` cell 11 of existing rows | 23 existing rows gained 41 entry paths (comma-separated) | `<PLACEHOLDER>` (attempt 2: none recorded yet) | `receipts/used-by-old-to-new.md`; lesson `corpus/lessons/round-56.md` § "Registry changes old→new"; lesson records the first integration joined with spaces and the census reported E11 (M56-6) |
| frontier (README) | `corpus/README.md` line 82 (index row): `source:` S383-S395; line 117 (Frontier bullet): "rows S383-S391 plus the host pins" | `<PLACEHOLDER>` | the index row and the Frontier bullet disagree on the range: the bullet was written when only S383-S391 existed (`0ff41272`) and was not refreshed when S392-S395 were added (`b70f6a2c`). Not a claim surface, but the report's frontier sentence must not repeat the stale range |
| new census warnings vs base | base: 28 W04 + 1 W01 (S277) | tip: 36 W04 + 1 W01 | new W04 rows: **S384, S387, S388, S389, S392, S393, S394, S395** (same URL under a new scope); W01 on S277 changed its used-by text (now two paths). Derived by this seat from the two census receipts |

---

## Defects found while drafting (severity marked)

| # | defect | input that shows it | severity |
|---|---|---|---|
| D1 | `claims-frozen-v2.md` attributes the C3 baseline string `entries=70 rows=319 missing=41 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24` to `receipts/c3-base-v2.txt`, but that receipt's literal line is `entries=70 rows=319 missing=41 pairs=381 exempt=24 stale=0 conflict=0` — the quoted string is **not** in the cited receipt | `receipts/c3-base-v2.txt` (1 line) vs `claims-frozen-v2.md` line 31 and `registration-v2.md` §C3-v2 | weakens the claim's *provenance*, not its numbers: the quoted values equal `frozen-tables-v2.json` `c3.baseline_v2` exactly (`entries 70, rows 319, missing 41, extra 0, dangling 0, conflict 0, stale 0, lost 0, exempt 24`), and 65−24 = 41 is consistent. The frozen files are never edited → **routed to round 57**, not fixed here |
| D2 | `receipts/census-before-a2.txt` (the attempt-2 "before" census cited for the Sources row) has **no `rc=` line**, unlike its predecessor `receipts/census-before.txt` (which ends `rc=0`), and contains no row count — so "exit 0, 332 rows" is not attested by the file the report cites | `receipts/census-before-a2.txt` (38 lines, last line `mado ok …`; `grep -c '^rc='` → 0) vs `receipts/census-before.txt` (31 lines, last line `rc=0`) | weakens — the cited receipt cannot carry the exit code it is cited for. This seat re-ran the identical command: byte-identical output, rc 0, 332 rows, so the *numbers* are safe; the receipt is the weak link |
| D3 | `receipts/census-before-a2.txt` and `receipts/attempt2-l1.txt` are **untracked** at the lane tip; `git ls-files --error-unmatch` fails for both | `git -C <lane> status --porcelain` → `?? .ufo/waves/round-56/receipts/attempt2-l1.txt`, `?? .ufo/waves/round-56/receipts/census-before-a2.txt`; `git ls-tree -r 0f3a5436 -- .ufo/waves/round-56/receipts` lists 16 files, neither among them | weakens — the attempt-2 evidence the report cites is not yet committed; it must be committed with the round, and the report's "committed receipts" framing holds only for the 16 tracked receipt files |
| D4 | `quality/r56_ctl_c2.py` raises `Setup("frozen-tables.json is not a regular blob at rev")` and `"frozen-tables.json sha256 differs from the embedded constant"`, but the file it actually reads is `TABLES = WAVE + "/frozen-tables-v2.json"` (v2) | `quality/r56_ctl_c2.py` line 31 vs lines 225 and 228 | cosmetic — message names the superseded v1 file; the bytes read and the sha checked are the v2 file's (`9511151a…`), so no gate is affected |
| D5 | `corpus/README.md` Frontier bullet says "rows S383-S391" while the index row says `source:` S383-S395 and the registry holds S383-S395 | `corpus/README.md` lines 82 and 117; `corpus/SOURCES.md` rows S383-S395; `git show b70f6a2c --stat` shows the S392-S395 commit touched only `corpus/SOURCES.md` and the entry | cosmetic — stale prose in a non-claim surface, but it is the sentence the report's frontier row would paraphrase |
| D6 | attempt-2 drafts conflict on the landing form of S396/S397 (`queued` + `used-by —` vs `mined` + `used-by corpus/lessons/round-56.md`), and the reason given in `s396-s397-draft.md` ("a lesson path in `used-by` would flip `TARGET_MET` to `TARGET_MISSED` at the new tip") is **not** what the counter does | `attempt2/s396-s397-draft.md` vs `attempt2/integration-plan.md`; probe on a scratch clone: adding `corpus/lessons/round-56.md` to a used-by cell leaves the counter at `extra=0 … verdict=TARGET_MET` (rc 0) — the counter's `USED_BY` regex only matches `corpus/knowledge/…md` (`quality/counters/c3-r56-used-by.py` line 51), so a lesson path is invisible to `extra`; whereas `corpus/knowledge/no-such-entry.md` **does** trip `extra=1` (rc 1) | weakens — the stated rationale for one form is wrong; the choice itself is the L1's. A probe of the integration-plan form (both rows, `mined`, lesson path) gives `rows=334 … verdict=TARGET_MET` (rc 0) and census rc 0, so neither form breaks a frozen gate. (Related: the C3 `extra` leg cannot see non-`corpus/knowledge` used-by paths at all — 41 existing used-by paths are outside `corpus/knowledge/`, e.g. `corpus/lessons/round-12.md`, `corpus/README.md`, `tools/mado-verify.sh`. That is the frozen `registration.md` §C3 definition, so it is a declared limit of the predicate, not a defect in it.) |

## Could not verify

- **`<A2FINAL>`** — the attempt-2 final revision does not exist. `git log 0f3a5436..HEAD` is empty in
  the lane, `origin/master` still prints `0f3a5436`, `w3-results.json` is absent, and 26 of the 64
  w3 seats had not reported at 2026-10-30T05:16Z. Every "after" cell in Table 1 and the "after"
  cells in Table 3 are therefore `<PLACEHOLDER>`.
- The attempt-2 **WAVE-DONE** receipt and the settled-seat count for w3 — pending (Table 2).
- The attempt-2 **role mix** is read from an untracked dispatch spec, not from a committed
  artifact (stated in Table 2); it may still change if the wave is re-dispatched.
- Nothing in the frozen claims was re-measured at a *different* predicate: the counters and
  harnesses were run unchanged, and no control, fixture, hold-out or table was edited.
- `MADO_WAVE_DONE` for attempt 2: not runnable (no `w3-results.json`); the attempt-1 line quoted
  above was produced by this seat at the lane tip and is *not* a substitute for it.

## Tooling

No tool was installed, upgraded or removed. Everything ran with the pre-existing `python3`
(`-I`), `git` and `bash` already on the host; no `pacman`, `uv`, `npm` or `cargo` transaction was
performed, so the pacman pause and the update-safety gate were not engaged.
