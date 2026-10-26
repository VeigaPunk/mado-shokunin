# ExecHarmAfter — harm baselines at the round-41 data commit

Round 41 (hyaku run 7, 2026-10-25), inline v1 wave w2, seat `ExecHarmAfter`.
Attack: **"no axis is harmed" at the data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`**.
Everything below was **run**, not inferred: each block is the verbatim stdout+stderr of the command
named above it, captured to `out-*.txt` (sha256 manifest at the end). Comparison baseline:
`w1/ExecHarmChecks/baseline.md` (freeze `60c3914`, same commands).

## Environment (what the numbers are measured in)

| item | value |
|---|---|
| clone | `D=$(mktemp -d)` → `$D/lane` = `/tmp/tmp.uMwEMvEpVp/lane`, `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin "$D/lane"` |
| toplevel check | `git -C "$D/lane" rev-parse --show-toplevel` → `/tmp/tmp.uMwEMvEpVp/lane` (equals the clone root; no throwaway identity, no commit made) |
| checkout | `git -C "$D/lane" checkout -q 07f2641696b5ac73de1404ea737a9f27e9819aa1`; `rev-parse HEAD` → `07f2641696b5ac73de1404ea737a9f27e9819aa1` |
| data commit | `07f2641 round-41: data - tools/mado-globals.py, focus-grab entry, rows S283-S289, lesson` (6 files: `tools/mado-globals.py`, `corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/SOURCES.md` (+8/-1: S283-S289 rows, S037 used-by), `corpus/README.md` (+1 row), `corpus/lessons/round-41.md`, `.ufo/waves/round-41/fetch/xdph-installed-version.txt`) |
| python | `Python 3.14.8` (all `python3` calls used `-I`) |
| bash | `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)` |
| working dir | `cd "$D/lane"` for commands 1–6; command 7 ran from the fleet root (live lane tree, as assigned) |
| residue | `git -C "$D/lane" status --porcelain` after all runs → **empty** |

## The seven commands

| # | command (cwd = clone root at data commit) | exit | counted line |
|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | **0** | `MADO_SELFTEST: 460/460 assertions passed` |
| 2 | `python3 -I tools/mado-options.py --selftest` | **0** | `MADO_OPTIONS_SELFTEST: 211/211 passed` |
| 3 | `python3 -I quality/check-index.py --rev 07f2641… --repo .` | **0** | `MADO_INDEX: … indexed=59/59 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 4 | `python3 -I quality/check-index-rows.py` (bare) | **2** | `SETUP_ERROR: --rev or --root is required` |
| 4b | `python3 -I quality/check-index-rows.py --rev 07f2641… --repo .` (supplementary) | **1** | `MADO_INDEX_ROWS: … rows=59 errors=1 warns=3` — **NEW ERROR** |
| 5 | `python3 -I quality/check-axis-scores.py --repo . --rev 07f2641…` | **1** | `MADO_AXIS: checked=3 mismatched=1 rev=07f2641…` — **navigation STALE** |
| 6 | `python3 -I tools/mado-eventq.py --selftest` | **2** | `mado-eventq.py: error: unrecognized arguments: --selftest` |
| 7 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | **0** | `mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (9 TSV lines, same W-set) |

### 1. `bash tools/mado-verify.sh --selftest` — exit 0

```
MADO_SELFTEST: 460/460 assertions passed
```

1 line. **Identical to baseline (460/460)** — no assertion-count drop from the new tool. Output hash equals the baseline's `out-verify-selftest.txt` exactly.

### 2. `python3 -I tools/mado-options.py --selftest` — exit 0

```
MADO_OPTIONS_SELFTEST: 211/211 passed
```

1 line. Identical to baseline (211/211).

### 3. `python3 -I quality/check-index.py --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 --repo .` — exit 0

```
MADO_INDEX: rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 indexed=59/59 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
```

1 line. Navigation instrument. Baseline 58/58 → now 59/59: **B rose by exactly 1** (the one new `corpus/knowledge/*.md` note), the baseline-predicted value. `missing=0 dangling=0 duplicates=0` and `coverage=10.0000/10` unchanged.

### 4. `python3 -I quality/check-index-rows.py` (bare) — exit 2

```
SETUP_ERROR: --rev or --root is required
```

1 line. Identical to baseline (usage error, exit map 2; carries no row-fidelity signal).

### 4b (supplementary, labelled). `python3 -I quality/check-index-rows.py --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 --repo .` — **exit 1 (baseline: 0)**

```
MADO_INDEX_ROWS: rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 rows=59 errors=1 warns=3
ERROR row-cells: knowledge/hyprland-focus-grab-r41.md at line 70 carries 2 cells (need 3 non-empty)
WARN cited-glob-nomatch: `.ufo/evidence/round-12/getprop-*.txt` in row knowledge/window-rule-effects-getprop.md
WARN cited-glob-nomatch: `.ufo/evidence/round-12/drift-*.txt` in row knowledge/config-drift-r12.md
WARN cited-glob-nomatch: `.ufo/waves/round-24/fetch/S###.bin` in row knowledge/rule-attribution-r24.md
```

4 lines, exit 1. **Finding 1 (DATA defect).** 59 rows, **1 ERROR (new)** vs baseline 0, same 3 WARNs.
The ERROR names the new C2 entry's coverage-map row: `corpus/README.md:70`
(`git diff 60c3914..07f2641 -- corpus/README.md` shows exactly one inserted row, a
`| \`knowledge/hyprland-focus-grab-r41.md\` | <Holds prose> |` line). Per
`quality/check-index-rows.py:19-21,236-241`, a fence row must carry >=3 cells (Note, Holds,
Sources) with cells 2 and 3 non-empty; this row carries only Note + Holds — **the Sources cell
is missing** (every other row in the table ends with a third `| S### … |` cell). The gate
exits 1, so the data commit broke the baseline constraint `errors=0`; this must be fixed before
the round lands (add the Sources cell to `corpus/README.md:70`). Note: since the cell-count
check fails, the row's S-id and cited-path checks are *skipped* for that row today
(`continue` at line 241); the entry itself cites S037/S283–S289, all of which exist in
`corpus/SOURCES.md` at the rev (S283–S289 added by this same commit, S037 pre-existing).

### 5. `python3 -I quality/check-axis-scores.py --repo . --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1` — exit 1 (baseline: 0)

```
MADO_AXIS_ROW: axis=navigation published=58/58 derived=59/59 verdict=STALE
MADO_AXIS_ROW: axis=calibration published=55/55 derived=55/55 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1 rev=07f2641696b5ac73de1404ea737a9f27e9819aa1
```

4 lines, exit 1. **Finding 2 (open defect, expected).** Derived fractions the gate derives now:
- **navigation indexed/total = 59/59** — published line still says 58/58 → `STALE` (the only mismatch).
- **calibration resolved/active = 55/55** — MATCH (not harmed).
- **operability selftest = 12/12** — MATCH (not harmed).

The published axis line the L1 must publish: `SCORECARD.md:2493` reads
`Axis table re-derived at 3c80537a54b4fd3b534f5cc3496a4bdc37c11371` plus the round-40 axis-line commit (two new indexed entries): navigation 58/58; calibration resolved-active 55/55; operability selftest 12/12.` — the data commit did not touch SCORECARD.md (not in its 6-file list), so navigation must be re-published to **59/59** (fraction stays 1.0).

### 6. `python3 -I tools/mado-eventq.py --selftest` — exit 2

```
usage: mado-eventq.py [-h] [--ss-file SS_FILE] [--log LOG]
                      [--journal-file JOURNAL_FILE] [--disable-logs {0,1}]
                      [--expect-client EXPECT_CLIENT] [--socket2 SOCKET2]
                      [--snapshot-out SNAPSHOT_OUT]
mado-eventq.py: error: unrecognized arguments: --selftest
```

5 lines, exit 2. Identical to baseline: the file exists, the `--selftest` flag does not
(`grep -n selftest tools/mado-eventq.py` → empty) — the assignment's "if it exists" condition
resolves the same way: **no eventq selftest baseline** (its self-check is a live/substrate read,
which host-safety forbids). Gap, not a pass; unchanged.

### 7. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` — exit 0

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

9 lines (TSV), exit 0. **Identical to the w1 baseline capture byte-for-byte** (sha256
`858315d225193675535aafa5be0bfd7ee1fad308db763d22e2065021a097bcc3` = baseline's
`out-sources-census-validate.txt`) and identical on all 9 lines to the frozen
`receipts/census-before.txt` at the data commit (that receipt adds one trailing `exit=0` line).
The new S283–S289 rows introduce **no new W or E code**; `mado ok` holds. This command reads
the live lane tree (fleet root, as assigned), which may carry the L1's uncommitted edits; the
capture is still byte-identical to the freeze baseline.

## Differences from the w1 baseline (the harm report)

| instrument | baseline at `60c3914` | data commit `07f2641` | verdict |
|---|---|---|---|
| verify selftest | 460/460, exit 0 | 460/460, exit 0 | no change |
| options selftest | 211/211, exit 0 | 211/211, exit 0 | no change |
| index | 58/58, missing=0 dangling=0 duplicates=0, coverage=10.0000/10 | **59/59** (B +1), zeroes intact, coverage=10.0000/10 | expected, no harm |
| index rows (rev) | rows=58 errors=0 warns=3, exit 0 | rows=59 **errors=1** warns=3, **exit 1** | **DATA DEFECT** (missing Sources cell, `corpus/README.md:70`) |
| index rows (bare) | exit 2 SETUP_ERROR | exit 2 SETUP_ERROR | no change |
| axis scores | checked=3 mismatched=0, exit 0 | checked=3 **mismatched=1**, **exit 1**, navigation STALE 58/58 vs derived 59/59 | **open defect (expected)**: L1 must publish navigation 59/59 |
| eventq selftest | exit 2 unrecognized | exit 2 unrecognized | no change (gap) |
| census | `mado ok`, 7×W04 + 1×W01 (S277), exit 0 | identical bytes, `mado ok`, exit 0 | no change, no new E-code |

Derived axis fractions the L1 must publish: **navigation 59/59** (indexed/total; was 58/58),
calibration 55/55 (resolved/active), operability 12/12 (selftest).

## Residue (measured, not assumed)

- **Clone tree:** `git -C "$D/lane" status --porcelain` after all runs → **empty**.
- **`--selftest` scratch:** `tools/mado-verify.sh:1874-1878` removes its outer scratch on
  success; my verify ran ≈20:53:4x–20:54:11 (mtime of `out-verify.txt` 20:54:11). The two
  present `/tmp/w5-mado-m52-selftest.*` dirs carry mtimes **18:20 and 20:32 — both predate my
  run window** (siblings' leftovers; none removed). `ls -d /tmp/mado-options-st-*` → 0 entries.
- **Census:** read-only (`scripts/sources-census.sh:6`), no `--out`, stdout only.
- **Clone cleanup:** `/tmp/tmp.uMwEMvEpVp` removed after the captures; `ls -d
  /tmp/tmp.uMwEMvEpVp` afterwards → no such file. No other path was written outside the seat
  dir and the Report trailer; no git verb beyond read-only ones; no package transaction; no
  compositor/journal-client access (only `hyprctl version`-level host contact is permitted and
  none was needed).

## Output manifest (verbatim captures)

```
491e682b388398bed72af668ca2474fb8ba1fc0c3406d92aa27f20f6b008b260  out-axis.txt         (4 lines, exit 1 — STALE)
858315d225193675535aafa5be0bfd7ee1fad308db763d22e2065021a097bcc3  out-census.txt       (9 lines, exit 0 — byte-identical to baseline)
a282a04aae285089e7b04a56a8d694c85543fa5fd5a0437f577629e4a758717e  out-eventq.txt       (5 lines, exit 2 — identical to baseline)
09a9a6ec0f378712e08aa97d29834e4611d173f9d167a147d9f992238c91c0cf  out-index.txt         (1 line, exit 0 — 59/59)
647b6712816c655002f1c8b16ce98c40255b53363bee7fe9693c411cc648a007  out-options.txt       (1 line, exit 0 — identical to baseline)
3d2d8ba229e30d36601aac1ca563344b032255cdd193ce4323585999b1de9ba4  out-rows-bare.txt     (1 line, exit 2 — identical to baseline)
d5ad2b102c17ec11a5cc13c987adcc555c9acadf4b0b8c1a28d31d4dbdfbfcc6  out-rows-rev.txt      (4 lines, exit 1 — ERROR row-cells)
58e720ddd3eaf6aba84ad6d37efe309c3e6b5b1d3d9aede880e4230a62543d90  out-verify.txt        (1 line, exit 0 — identical to baseline)
```
