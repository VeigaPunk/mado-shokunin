# R56W3ScribeReportTables — seat report (round 56 mado, wave w3, attempt 2)

**Item attacked:** draft the round report's three evidence tables — (1) the Before→after table
(one row per claim: frozen counting command, before value at base `13f0acbe`, after value at the
attempt-2 final revision `<A2FINAL>`); (2) the round-shape paragraph; (3) the Sources & frontier
rows — from committed receipts, with no invented numbers.

**Outcome:** tables drafted and delivered at
`.ufo/waves/round-56/w3/R56W3ScribeReportTables/receipts/report-tables.md`.
Every "after" cell that depends on `<A2FINAL>` is `<PLACEHOLDER>` (the attempt-2 final revision
does not exist yet); every other cell is a measured value with its command and revision.

## What I did

1. Read the frozen inputs named by the item and the attempt-1 receipts:
   `claims-frozen-v2.md` (sha256 `187cf3d1…`), `registration-v2.md`, `frozen-tables-v2.json`
   (sha256 `9511151a…`, matches the embedded constant in all five tools), `receipts/at-final.txt`
   (sha256 `d36c6357…`), `receipts/before.txt` (`0aff26f8…`), `receipts/c3-base-v2.txt`
   (`46a6fd6f…`), `receipts/census-before-a2.txt` (`4792ac1c…`, untracked), `receipts/census-before.txt`
   (`ec80eec6…`), `receipts/attempt2-l1.txt` (untracked), `attempt2/{integration-plan,LOG-draft,s396-s397-draft}.md`,
   `corpus/lessons/round-56.md`, `LOG.md`, `SCORECARD.md`, `corpus/README.md`.
2. Re-ran all five frozen commands **plus the four harm-watch gates** against a read-only
   `git clone --shared` of the lane in scratch, at the base revision and at the lane tip
   `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. The lane's tracked files were never touched.
3. Re-derived the census (base and tip trees, `--file` mode on the extracted blobs) and diffed the
   warning sets to get "rows added by tier" and "new W04 rows" from the blobs, not from prose.
4. Measured the wave shapes from the spec/dispatch/results files rather than from the narrative.
5. Probed three registry `used-by` forms on scratch clones to test the frozen C3 `extra` leg
   against a lesson path, a knowledge path and a nonexistent path — this is what exposed D6.

## Exact commands and decisive output

Frozen gates, re-run by this seat (full logs in
`receipts/frozen-gates-reverified.txt` and `receipts/frozen-gates-at-base.txt`):

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 13f0acbe3a15da2d9c08357a576d91dcadc85273 --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=13f0acbe3a15da2d9c08357a576d91dc85273 rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8 verdict=TARGET_MISSED missed=tables_sha,entry_absent,index
rc=1

$ python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev 13f0acbe3a15da2d9c08357a576d91dcadc85273 --work <scratch>
MADO_R56_CONTROLS setup error: .ufo/waves/round-56/frozen-tables-v2.json absent at 13f0acbe3a15da2d9c08357a576d91dc85273
rc=2

$ python3 -I quality/check-r56-controls.py --claim c2 --repo . --rev 13f0acbe3a15da2d9c08357a576d91dc85273 --work <scratch>
r56_ctl_c2: setup error: frozen-tables.json is not a regular blob at rev
rc=2

$ python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 13f0acbe3a15da2d9c08357a576d91dc85273 --work <scratch>
c3-r56-used-by.py: setup error: frozen-tables-v2.json is not a regular blob at --rev
rc=2

$ python3 -I quality/check-r56-controls.py --claim c3 --repo . --rev 13f0acbe3a15da2d9c08357a576d91dc85273 --work <scratch>
SETUP: .ufo/waves/round-56/frozen-tables-v2.json is not a regular blob at 13f0acbe3a15da2d9c08357a576d91dc85273
rc=2
```

At the lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (identical to the attempt-1 measurement
at `8a7b7346`, because the claim surfaces are byte-identical between the two revisions):

```
MADO_AUTORELOAD_ENTRY: rev=0f3a5436… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none          rc=0
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK                                                                                                     rc=0
MADO_R56_C2: rev=0f3a5436… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET                                                              rc=0
  r56_ctl_c2: sandbox=bwrap fixture_commit=ok control_scores={'const-host': (1, 0), 'empty': (0, 0), 'sibling-reader': (0, 0), 'lookup-committed': (18, 0)}
MADO_USED_BY: rev=0f3a5436… entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none          rc=0
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK                                                                                                      rc=0
```

Harm watch at the tip: `MADO_SELFTEST: 460/460` (rc 0); `MADO_INDEX: … indexed=71/71 missing=0
dangling=0 duplicates=0 coverage=10.0000/10` (rc 0); `MADO_INDEX_ROWS: … rows=71 errors=0 warns=3`
(rc 0, three pre-existing `cited-glob-nomatch` WARNs); `LEDGER: population=97 ledger_rows=97
uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` (rc 0).

Wave shape, from the wave's own files:

```
$ python3 -c "…w1-spec.json…w2-spec.json…w3-spec.json…"
w1 items: 43  dispatch {'spawn': 43, 'resume': 0, 'total': 43}  reported .md 43  w1-results.json seats=43 results=43 (43 non-null outputs)
w2 items: 35  dispatch {'spawn': 35, 'resume': 0, 'total': 35}  reported .md 33  (no R56W2MutC3Counter.md, no R56W2MutC2Harness.md)
w3 items: 64  dispatch {'spawn': 64, 'resume': 0, 'total': 64}  reported .md 38 at 2026-10-30T05:16Z
w2-results.json exists: False        w3-results.json exists: False

$ python3 -I quality/check-wave-done.py --repo . --rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --round 56 --work <scratch>
WAVE wave=w1 ready=1 results=present seats=43 dispatched=43 settled=43 verdict=OK reason=none
WAVE wave=w2 ready=1 results=absent seats=0 dispatched=35 settled=0 verdict=MISSING reason=results-missing
MADO_WAVE_DONE: round=56 waves=2 settled=1 verdict=MISSING
rc=1
```

Sources, from the registry blobs (not from prose):

```
$ git show 13f0acbe:corpus/SOURCES.md | grep -cE '^ {0,3}\|\s*S[0-9]{3,}\s*\|'   → 319
$ git show 0f3a5436:corpus/SOURCES.md | grep -cE '^ {0,3}\|\s*S[0-9]{3,}\s*\|'   → 332
$ bash scripts/sources-census.sh census --file <base blob>   → file rows 319  tier.A 308 tier.B 4  tier.C 7  status.mined 298 queued 10 rejected 11
$ bash scripts/sources-census.sh census --file <tip  blob>   → file rows 332  tier.A 320 tier.B 5  tier.C 7  status.mined 311 queued 10 rejected 11
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
   … 38 lines …   mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md     rc=0
```

The census receipt cited by the item reproduces exactly: diff of `receipts/census-before-a2.txt`
against a fresh `validate` run on the tip tree is **empty** (38 lines each, rc 0).

C3 `extra`-leg probe on scratch clones (each a fresh `git clone --shared`; the mutation was a
committed edit to a *copy*):

```
S002 used-by += corpus/lessons/round-56.md        → MADO_USED_BY: … missing=0 extra=0 … verdict=TARGET_MET   rc 0
S002 used-by += corpus/lessons/does-not-exist.md  → MADO_USED_BY: … missing=0 extra=0 … verdict=TARGET_MET   rc 0
S002 used-by += corpus/knowledge/no-such-entry.md  → MADO_USED_BY: … missing=0 extra=1 … verdict=TARGET_MISSED rc 1  (missed=extra)
```

## Defects (input → severity)

| id | defect | input | severity |
|---|---|---|---|
| D1 | `claims-frozen-v2.md` and `registration-v2.md` quote the C3 baseline string `entries=70 rows=319 missing=41 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24` as the content of `receipts/c3-base-v2.txt`, but that receipt's literal line is `entries=70 rows=319 missing=41 pairs=381 exempt=24 stale=0 conflict=0` — the quoted string is not in the cited receipt | `receipts/c3-base-v2.txt` vs `claims-frozen-v2.md` line 31, `registration-v2.md` §C3-v2 | **weakens the claim's provenance, not its numbers.** The quoted values equal `frozen-tables-v2.json` `c3.baseline_v2` exactly, and 65 − 24 = 41 is consistent. Frozen files are never edited → **routed to round 57** |
| D2 | `receipts/census-before-a2.txt` has no `rc=` line (its predecessor `census-before.txt` ends `rc=0`) and no row count, so the "exit 0, 332 rows" the Sources row cites it for is not attested by that file | `receipts/census-before-a2.txt` (38 lines, last `mado ok …`); `grep -c '^rc='` → 0 | **weakens.** Re-running the identical command gives byte-identical output and rc 0, and `census --file` gives 332 — the numbers are safe, the receipt is the weak link |
| D3 | `receipts/census-before-a2.txt` and `receipts/attempt2-l1.txt` are untracked at the tip — the attempt-2 evidence the report cites is not committed | `git status --porcelain` → `?? …/receipts/attempt2-l1.txt`, `?? …/receipts/census-before-a2.txt`; `git ls-tree -r 0f3a5436 -- .ufo/waves/round-56/receipts` lists 16 files, neither among them | **weakens.** Must be committed with the round; "committed receipts" framing holds only for the 16 tracked files |
| D4 | `quality/r56_ctl_c2.py` error messages name `frozen-tables.json` while the file read is `TABLES = WAVE + "/frozen-tables-v2.json"` | `quality/r56_ctl_c2.py` line 31 vs lines 225 and 228 | **cosmetic.** The bytes read and sha checked are the v2 file's (`9511151a…`); no gate affected |
| D5 | `corpus/README.md` Frontier bullet says "rows S383-S391" while the index row says `source:` S383-S395 and the registry holds S383-S395 | `corpus/README.md` lines 82 and 117; `git show b70f6a2c --stat` shows the S392-S395 commit touched only `corpus/SOURCES.md` and the entry | **cosmetic.** Stale prose in a non-claim surface, but it is the sentence the report's frontier row paraphrases |
| D6 | The two attempt-2 drafts conflict on the landing form of S396/S397 (`queued` + `used-by —` vs `mined` + `used-by corpus/lessons/round-56.md`), and `s396-s397-draft.md`'s stated reason ("a lesson path in `used-by` would flip `TARGET_MET` to `TARGET_MISSED` at the new tip") is contradicted by the counter | `attempt2/s396-s397-draft.md` vs `attempt2/integration-plan.md`; probe above: a lesson path leaves the counter at `extra=0 … TARGET_MET`, because `USED_BY` in `quality/counters/c3-r56-used-by.py` line 51 matches only `corpus/knowledge/…md`; a `corpus/knowledge/no-such-entry.md` path **does** trip `extra=1` | **weakens.** The stated rationale for one form is wrong; the form itself is the L1's decision. A probe of the integration-plan form (both rows inserted inside `## Registry`) gives `entries=71 rows=334 … verdict=TARGET_MET` (rc 0) and census rc 0, so neither form breaks a frozen gate. Related declared limit (not a defect): the `extra` leg cannot see non-`corpus/knowledge` used-by paths at all — 41 existing used-by paths are outside `corpus/knowledge/` (e.g. `corpus/lessons/round-12.md`, `corpus/README.md`, `tools/mado-verify.sh`) |

No defect found in the frozen claims themselves: all five frozen sentences, the 12 C1 controls, the
4 C2 controls and the 9 C3 controls hold at the lane tip with the counters and harnesses run
unchanged.

## Deliverables (absolute paths)

- Tables draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeReportTables/receipts/report-tables.md`
- Re-verification log (tip): `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeReportTables/receipts/frozen-gates-reverified.txt`
- Re-verification log (base): `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeReportTables/receipts/frozen-gates-at-base.txt`
- Copy of the census receipt under audit: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeReportTables/receipts/census-before-a2-copy.txt`
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeReportTables.md`

## Not verified / out of scope

- `<A2FINAL>`: the attempt-2 final revision does not exist — `git log 0f3a5436..HEAD` is empty in
  the lane, `origin/master` still prints `0f3a5436`, `w3-results.json` is absent, and 26 of 64 w3
  seats had not reported at 2026-10-30T05:16Z. All "after" cells that depend on it are
  `<PLACEHOLDER>`.
- The attempt-2 WAVE-DONE receipt and the w3 settled-seat count: pending.
- The attempt-2 role mix is read from an untracked dispatch spec (`w3-spec.json`, sha256
  `8036cd5e…`), not from a committed artifact.
- I did not edit any tracked lane file, any fleet file, the registry, the lesson, the LOG or the
  SCORECARD; no git/jj mutation was performed against the lane or the fleet repo; no
  `hyprctl` keyword/dispatch/reload was run and nothing under `~/.config` or `~/.local` was
  written.

## Tooling

No tool installed, upgraded or removed; nothing to record for the operator's tooling ledger.
All work used the pre-existing `python3` (with `-I`), `git` and `bash`; no `pacman`, `uv`, `npm` or
`cargo` transaction, so the pacman pause and the update-safety gate were not engaged.

## Scratch

`/fast/scratch/hyaku/mado-r56/R56W3ScribeReportTables/` (one `git clone --shared` of the lane, one
probe clone per registry variant, exported census blobs) — **removed before yielding**; all
decisive output was copied into the deliverable directory first.
