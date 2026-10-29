# R56W2ConnCross — probe receipts (all reads/mutations on scratch copies; lane untouched)

REV scored: 28fc86ac2359ec27406d8a2c63bef82ea6e947ed (lane HEAD at attack: 19be88b6)

## P-harness — registered harnesses reproduce the lane-reported lines
```
python3 -I quality/counters/c1-r56-autoreload-entry.py --repo LANE --rev 28fc86ac… --work W
  MADO_AUTORELOAD_ENTRY: rev=28fc86ac… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   rc=0
python3 -I quality/counters/c3-r56-used-by.py   --repo LANE --rev 28fc86ac… --work W
  MADO_USED_BY: rev=28fc86ac… entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   rc=0
python3 -I quality/check-r56-controls.py --claim c1|c2|c3 --repo LANE --rev 28fc86ac… --work W
  c1: MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK                                   rc=0
  c2: r56_ctl_c2: fixture_commit=ok control_scores={'const-host': (1,0), 'empty': (0,0), 'sibling-reader': (0,0), 'lookup-committed': (18,0)}
      MADO_R56_C2: rev=28fc86ac… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET   rc=0
  c3: MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK   rc=0
```

## P1/P1b/P3 — S391 and its pin are outside every C1 leg
Frozen scope: registration-v2.md:75 "rows S383-S390"; frozen-tables-v2.json c1.new_row_ids = S383..S390 (8); c1.pin_sha256 has 8 pins (no Hyprland-PropRefresher.hpp). Integrated registry: 9 new rows S383–S391; entry `source:` line cites S391; E08/E09 quote Hyprland-PropRefresher.hpp:18/:21.
```
# P1b  empty S391 used-by cell (scratch copy, committed) -> C1 counter
  MADO_AUTORELOAD_ENTRY: … rows=30/30 … new_rows=8/8 verdict=TARGET_MET missed=none   rc=0
# P3   append "\n// TAMPERED\n" to .ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp -> C1 counter
  MADO_AUTORELOAD_ENTRY: … verdict=TARGET_MET missed=none   rc=0
# P6   drop ", S391 (PropRefresher.hpp)" from the entry source: line -> C1 counter
  MADO_AUTORELOAD_ENTRY: … verdict=TARGET_MET missed=none   rc=0
# P7   same S391 used-by corruption -> C3 counter (shared clone, base objects present)
  MADO_USED_BY: … entries=71 rows=328 missing=1 … verdict=TARGET_MISSED missed=missing   rc=1
```
.hpp pin self-consistency: sha256 37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0, 1322 B — matches S391 cell 07; not in frozen-tables-v2 pin_sha256 nor receipts/pins.sha256 (12 entries).

## P5 — freeze-order instrument is blind to the v2 contract files
check-freeze-order.py REQUIRED=("claims-frozen.md","registration.md"); OPTIONAL=("frozen-tables.json",) — the v2 files are not hashed.
```
python3 -I quality/check-freeze-order.py --repo CLONE --rev HEAD --round 56 --wave w1 --work W
  CLONE = shared clone at 28fc86ac…, then: printf '\nEDIT AFTER LAUNCH\n' >> .ufo/waves/round-56/registration-v2.md ; git commit
  MADO_FREEZE_ORDER: round=56 wave=w1 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T00:22:47.615Z verdict=OK reason=ok   rc=0
```

## P-cheat — E6 isolation depends on bwrap; absent, the answer key is reachable
Harness copies the tool to <work>/c2-tool-XXXX, stages each fixture at <work>/stage-N/<fid>/tree, export (with expected.out/rc/note.txt/args.json) at <work>/c2-export-XXXX; staged_run silently falls back to an unsandboxed run when shutil.which("bwrap") is None.
Probe: scratch copy of r56_ctl_c2.py with `_BWRAP = None` and TOOL=tools/cheat2.py (cheat derives the fid from the staged --config path and prints work/**/<fid>/expected.out; committed in the probe clone, never in the lane).
```
python3 -I quality/r56_ctl_c2_cheat3.py --repo CLONE --rev HEAD --work W
  r56_ctl_c2: fixture_commit=ok control_scores={'const-host': (1,0), 'empty': (0,0), 'sibling-reader': (0,0), 'lookup-committed': (18,0)}
  MADO_R56_C2: rev=HEAD fixtures=15/18 holdout=7/8 holdout_commit=ok controls=4/4 verdict=TARGET_MISSED
```
i.e. 22/26 fixtures pass with a tool that never parses a config; all four controls stay green; no control flags the channel. With bwrap present (this host) the sandbox hides the export; the harness never asserts bwrap.

## P-hash — the frozen `lost` hash covers 65 of 381 base pairs
```
PAIRS(base 13f0acbe) = 381 pairs; base-missing pairs = 65
sha256 over all 381 sorted "S###|path" lines + \n = 79545d6bc91df573a2cb24612d56d5b4705c92bc3dfad7a703ec31fe5aadd1b6
sha256 over the 65 missing-only lines      + \n = 630007b0a17540f45430068c9d9a38a731268e47e5fb9855887a7ae4f8d673ef
frozen-tables-v2.json c3.base_pairs_sha256 = 630007b0… ; c3.base_pair_count = 65
```
registration-v2.md:56 defines lost over PAIRS(base); the counter (c3-r56-used-by.py:246) implements the 65-subset; errata E12 discloses.

## P-loc — QUALITY-77 locator instrument on the integrated entry
```
python3 -I quality/check-locators.py --fetch .ufo/waves/round-56/fetch corpus/knowledge/hyprland-config-autoreload-r56.md
  CHECK_LOCATORS: locators=61 miss=6      (MISS at :21 :23 :24 :33 :135 :141; NOFRAG at :28 :137)
same command on the r55 entry with r55 pins: CHECK_LOCATORS: locators=38 miss=0
```
Misses are the checker's nearest-fragment attribution on multi-locator lines (e.g. :21 attributes `CConfigWatcher::update()` to pin line 33, which holds the K03 value line; the function header is line 32).

## P-doc — E8 "required verbatim" vs the committed docstring (whitespace/backtick-normalised)
item 1 VERBATIM · item 2 NOT (registered "glibc's is locale collation" → docstring "the C library's is locale collation") · item 3 VERBATIM · item 4 NOT ("as the watch's" → "as that watch's") · item 5 NOT ("; `watches=` counts add attempts, a missing path's `inotify_add_watch` result is never checked" → ", and `watches=` counts add attempts (a missing path's inotify_add_watch result is never checked by Hyprland)") · item 6 VERBATIM · item 7 NOT ("the value grammar and line grammar are the hyprlang 0.6.8 subset of this registration (…, R56ScoutHyprlang)" → "the value and line grammar is the hyprlang 0.6.8 subset of the registration (…); `misc:disable_autoreload` is a Bool option in Hyprland's table (ConfigValues.cpp:492) read as an integer (ConfigWatcher.cpp:33), so values above 1 are reachable only as the integer the watcher reads.")
No leg or harness reads the docstring (grep 'docstring|divergence' quality/r56_ctl_c2.py → none).

## P-cron — commit chronology (git log --format='%h %ci %s')
```
19be88b6 2026-10-28 22:04:27 -0300 wave 2 dispatch and registry
15015e77 2026-10-28 22:04:18 -0300 registration v2 errata (E12-E14), wave 2 spec generator
9c3ca28a 2026-10-28 22:01:22 -0300 wave 1 results and seat deliverables
28fc86ac 2026-10-28 22:00:24 -0300 C1 counter drops the bare content leg; tool ledger row fix
0ff41272 2026-10-28 21:59:02 -0300 integrate C1 entry, rows S383-S391, README/PROVINCE/SKILL, tool ledger, comma-separated used-by
2e39282e 2026-10-28 21:54:28 -0300 integrate C2 tool + harness, C3 counter + harness + used-by fix, C1 counter + harness, hold-out reveal
323a69c9 2026-10-28 21:44:35 -0300 registration v2 (pre-data), frozen tables v2, name-only allowlist, sibling-reader control
```
registration-v2-errata.md is ABSENT at 323a69c9 and at 28fc86ac (git ls-tree); it lands at 15015e77.

## P-checks — lane instruments on the integrated tree
```
python3 -I quality/check-index-rows.py  --root <exported tree at 28fc86ac>  -> MADO_INDEX_ROWS: rows=71 errors=0 warns=0   (base: 28 errors, blank-line split)
python3 -I quality/check-tool-ledger.py --repo LANE --rev 28fc86ac…                          -> LEDGER: population=97 ledger_rows=97 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET
w2-dispatch.json: grep -c 'ulimit|RLIMIT' = 0   (w1 dispatch QUALITY-98 finding not carried into w2)
SCORECARD.md diff 13f0acbe..28fc86ac: empty (no round-56 rows; "Planned (round 56; intent only)" only)
LOG.md: no round-56 entry; corpus/lessons/ has no round-56.md (C3 target "old→new logged in the lesson" unmet at rev; receipt receipts/used-by-old-to-new.md exists)
```
