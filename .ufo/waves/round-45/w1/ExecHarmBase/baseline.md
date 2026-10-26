# Harm-watch baseline — round 45 w1, seat ExecHarmBase

Purpose: fix, verbatim, where every lane gate stands at the round-45 **base**
`0c89478af821a6424c9ac922eafe02e39630cf4f` and at the round-45 **freeze**
`22a8dedd02f507689c567777e0f20b5e645c8ce0`, so round-45 `w2` can compare the tip against a frozen
reading instead of against memory. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

All runs were read-only against the lane. Each rev was materialised as a separate `git clone --shared`
under `/fast/scratch/hyaku/mado-r45/ExecHarmBase/{base,freeze}`, checked out detached, and verified with
`git -C <clone> rev-parse HEAD` before the first gate (output `0c89478a…` / `22a8dedd…`). Nothing was
written into the lane: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain -- quality
tools corpus SCORECARD.md LOG.md` printed nothing after all runs, and the full-status snapshot
`gates/lane-status.txt` shows only the wave's own untracked dispatch files and `w1/` seat directories
(lane HEAD at that moment `ebdba13f7cb16d454763003d424398eec3bb2788`).

Receipts: `gates/*.txt` in this seat directory. Each gate run is recorded as `$ <command>`, the full
stdout+stderr, then `[exit N]`; the derived files carry their own headers (`blobs-*.txt`,
`lane-status.txt`, `normalized-diff.txt`, `quote-check.txt`). Every line quoted below is grep-verified verbatim against its receipt by
`gates/quote-check.txt` (locators computed by `grep -n`, never typed).

## 1. Verdict table

`base` = the gate run with the repo at `0c89478a…`, `freeze` = the gate run with the repo at `22a8dedd…`.
"committed" marks the runs that execute the gate script **as committed at that rev** instead of the lane's
current bytes; both forms were run for the two rev-reading quality gates.

| # | gate | base | exit | freeze | exit | receipt |
|---|---|---|---|---|---|---|
| 1 | `quality/check-axis-scores.py --rev <rev> --repo <clone>` (lane bytes) | `MADO_AXIS: checked=3 mismatched=0`; rows navigation 61/61, calibration 71/71, operability 12/12 all `verdict=MATCH` | 0 | identical | 0 | `gates/axis-{base,freeze}.txt` |
| 2 | same gate, **committed** bytes at that rev | identical | 0 | identical | 0 | `gates/axis-committed-*.txt` |
| 3 | `quality/check-index.py --rev <rev> --repo <clone>` (lane bytes) | `indexed=61/61 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 | identical | 0 | `gates/index-{base,freeze}.txt` |
| 4 | same gate, **committed** bytes at that rev | identical | 0 | identical | 0 | `gates/index-committed-*.txt` |
| 5 | `quality/counters/c1-r44-geometry-states-v2.py --repo <clone> --rev <rev> --work <scratch>` | `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET`; `clause=b rc=0 selftest=94/94`; `b4 sites=16 killed=16 need=12`; `b5 state_blind_selftest rc=1 selftest=86/94 failed=1`; inner `PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET` | 0 | identical (modulo masks, incl. the per-run nonce) | 0 | `gates/c1r44-{base,freeze}.txt` |
| 6 | `quality/counters/c2-r44-gkeep-size-request-v2.py --repo <clone> --rev <rev>` | `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET`; `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1` | 0 | identical | 0 | `gates/c2r44-{base,freeze}.txt` |
| 7 | `tools/mado-geometry.py --selftest` (committed bytes at that rev) | `MADO_GEOMETRY_SELFTEST: 94/94 passed` | 0 | identical | 0 | `gates/geometry-selftest-*.txt` |
| 8 | `tools/mado-verify.sh --selftest` (committed bytes at that rev) | `MADO_SELFTEST: 460/460 assertions passed` | 0 | identical | 0 | `gates/verify-selftest-*.txt` |
| 9 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (current lane tree) | 7 × `W04` (e.g. `S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes`), 1 × `W01` (`S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md`), final line names `mado-shokunin/corpus/SOURCES.md` | 0 | (same tree; census is not rev-scoped) | 0 | `gates/census.txt` |
| 10 | `quality/check-evidence-pointers.py --repo <clone> --rev <rev> --branch master` | `pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=35 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET` | 0 | identical | 0 | `gates/evidence-pointers-*.txt` |
| 11 | `quality/check-index-rows.py --repo <clone> --rev <rev>` | `rows=61 errors=0 warns=3` (3 × `WARN cited-glob-nomatch`) | 0 | identical | 0 | `gates/index-rows-*.txt` |
| 12 | `quality/check-index-rows.py --selftest` | `MADO_INDEX_ROWS_SELFTEST: 10/10 assertions passed` | 0 | identical | 0 | `gates/index-rows-selftest-*.txt` |
| 13 | `quality/check-locators.py --selftest` | `SELFTEST: cases=18 passed=18 locators=19 miss=6`, `SELFTEST: PASS` | 0 | identical | 0 | `gates/locators-selftest-*.txt` |
| 14 | `quality/ratio-domain-meta.py --repo <clone> --rev <rev> --from 44 --to 44` | `DOMAIN_META: domain=2 meta=0 window=44-44 default=0` | 0 | identical | 0 | `gates/ratio-domain-*.txt` |
| 15 | `quality/counter-selftest.py --c1 .ufo/waves/round-26/c1/count-v2.py --c2 .ufo/waves/round-26/c2/count.py --rev <rev> --scratch <scratch>` | `SELFTEST pass=59 total=59` | 0 | identical | 0 | `gates/counter-selftest-*.txt` |
| 16 | `quality/check-counter-discrimination.py --profile r36 --manifest .ufo/waves/round-36/controls/manifest.json --repo <clone> --no-receipts` | `MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25` | 0 | identical | 0 | `gates/counter-discrimination-*.txt` |
| 17 | `quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-38/controls/manifest.json --rev <rev> --sandbox-root <scratch>` | `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET` | 0 | identical | 0 | `gates/r38-discrimination-*.txt` |
| 18 | `quality/check-axis-scores.py --selftest` | `MADO_AXIS_SELFTEST: 18/18 assertions passed` | 0 | identical | 0 | `gates/axis-selftest-*.txt` |
| 19 | `quality/check-index.py --selftest` | `MADO_INDEX_SELFTEST: 12/12 assertions passed` | 0 | identical | 0 | `gates/index-selftest-*.txt` |
| 20 | `quality/population-suite.py --checker quality/check-population.py` | `SUITE verdict=FAIL fixtures=46 failed=9` | **1** | identical | **1** | `gates/population-suite-*.txt` |
| 21 | `quality/check-control-receipts.py --round 44 …` | `CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-44/controls/` | **1** | identical | **1** | `gates/control-receipts-*.txt` |
| 22 | `quality/check-control-receipts.py --round 35 --data-registry .ufo/waves/round-35/w1/reports/swarm-registry.json --repo <clone> --tip <rev> --seeds 2` | `receipts=100`, `order=ok gap_s=65`, `CONTROL_RECEIPTS verdict=FAIL` | **1** | identical | **1** | `gates/control-receipts-r35-*.txt` |

`identical` in the freeze column means: every verdict and metric line of the freeze run equals the base
run's after masking the clone root, the scratch/work/sandbox/fixture temp roots, the `mktemp` suffix, the
revision sha, the seed, the nonce and `sha256:` digests — the mask-pair diff is `gates/normalized-diff.txt`,
which prints `SAME (modulo masks)` for all 21 receipt pairs and `DIFFERS` for none.

Rows 1–19 are green at both revs. Rows 20–22 are **red at both revs, identically** — they are
pre-existing state, not round-45 movement (see §4).

## 2. Gate-plane byte identity (why "same at both revs" is a fact and not a coincidence)

Blob ids at both revs (computed with `git rev-parse <rev>:<path>`, `gates/blobs-base.txt`,
`gates/blobs-freeze.txt`; the two files differ only in their `tag rev` columns):

| path | blob |
|---|---|
| `quality/check-axis-scores.py` | `cdfc9a8193eb2ff85c86df1169411e9af853fe34` |
| `quality/check-index.py` | `d90767623a626be2fec81f5597469ab4bf63830d` |
| `quality/counters/c1-r44-geometry-states-v2.py` | `8e844b221a957173c3c557f371f7871b2a6e11cf` |
| `quality/counters/c2-r44-gkeep-size-request-v2.py` | `d24abcf7683bc59602db462c6a79b7a131c8a23f` |
| `tools/mado-geometry.py` | `d5f50df12ab32abd172d17b039c93daec2a94ff7` |
| `tools/mado-verify.sh` | `9113c7c05e586328f44ed6822a3d12ff34c47a36` |
| `corpus/SOURCES.md` | `71853a71d436464e6d7c6e821d7d2232cb43ef8e` |
| `corpus/README.md` | `c1966bd82527b580fff9bae4a4bc05bf6e0e6f7c` |
| `SCORECARD.md` | `379312d76182f0ba10b79e53786109d665871e97` |

The freeze commit adds 25 files and removes none (`git show --name-status 22a8dedd`): 23 under
`.ufo/waves/round-45/` (registration, pins, l1-draft, controls, before-receipts) plus the two round-45
counters, which do not exist at the base (`git ls-tree 0c89478a -- quality/counters/c1-r45-monitors.py
quality/counters/c2-r45-monitor-entry.py` prints nothing — `gates/r45-c1-base-absent.txt`,
`gates/r45-c2-base-absent.txt`). Their frozen blobs, for w2 to assert untouched:

| path | blob at `22a8dedd` |
|---|---|
| `quality/counters/c1-r45-monitors.py` | `6642ebfce65269a5d45b4ac97491465784f3c559` |
| `quality/counters/c2-r45-monitor-entry.py` | `61bd4bee0c98ec52280a407a402908aa302ff56e` |

(`gates/blobs-r45.txt`.) A normalised diff of every `*-base.txt` / `*-freeze.txt` pair in `gates/`
(scratch paths, mktemp suffixes, revs, seeds, nonces and `sha256:` digests masked) prints
`SAME (modulo masks)` for all 21 pairs: **no substantive difference** on any gate; the only unmasked
differences are the scratch directory names and the per-run nonce/seed.

## 3. Round-45 counters, pre-data (the "before" this baseline freezes)

- `quality/counters/c1-r45-monitors.py --repo <freeze clone> --rev 22a8dedd… --work <scratch>` →
  `PRED-C1-r45 clause=a tool=absent`, `PRED-C1-r45: fixtures=0/49 selftest=fail readonly=fail
  tool=absent verdict=TARGET_MISSED`, exit 1 (`gates/r45-c1-freeze.txt`). Matches
  `.ufo/waves/round-45/receipts/c1-before-base.txt`.
- `quality/counters/c2-r45-monitor-entry.py --repo <freeze clone> --rev 22a8dedd… --base 0c89478a…` →
  `PRED-C2-r45 hyprland-monitor-rule-r45.md clauses=a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0 j:0 admitted=0`,
  `PRED-C2-r45: admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`gates/r45-c2-freeze.txt`). Matches
  `.ufo/waves/round-45/receipts/c2-before-base.txt`.
- Neither counter exists at the base, so "base" for these two predicates is the absent instrument, not a
  scored run.

## 4. Red at both revs (pre-existing — w2 must not attribute these to round 45)

1. **`quality/population-suite.py`**: 46 fixtures, 9 fail, at both revs with output identical after masking
   the per-run fixture temp root (`gates/population-suite-{base,freeze}.txt`, `gates/normalized-diff.txt`). Failures name the fixture, not a round:
   `green-numerator-not-compared`, `red-denominator-larger`, `red-denominator-smaller`,
   `red-case-lines-and-denominator`, `red-registered-total-differs`, `red-second-summary-disagrees`,
   `red-first-summary-disagrees`, `exit2-cases-pass-space-before-equals`,
   `exit2-cases-pass-space-after-equals`. The suite and `quality/check-population.py` disagree about
   whitespace around `cases_pass =` and about which mismatching legs are permitted; the suite is the
   older round-27 instrument. Baseline verdict: **FAIL 9/46, unchanged**.
2. **`quality/check-control-receipts.py`** is per-round over `.ufo/waves/round-N/controls/`, a layout the
   lane stopped using after round 36. Round 44 keeps its controls under `.ufo/waves/round-44/ctl/` and
   `receipts/`, so the default glob finds none:
   `CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-44/controls/`. The last round
   that has the expected layout is 35; there the gate reads `receipts=100` and `order=ok gap_s=65` but the
   default shape list is unmet (`shapes_missing=EmptyArray|AllFalse,Junk,Echo,LabelKeyed,NoReader`), so it
   also prints `CONTROL_RECEIPTS verdict=FAIL`. Both invocations are **FAIL at base and at freeze**; this is
   an instrument/round-shape mismatch, recorded so w2 compares like with like and does not treat it as
   damage.

## 5. What w2 must hold invariant at the tip, and what is allowed to move

Invariant (a move in any of these is harm and must be reported as such):

| gate | invariant field(s) |
|---|---|
| axis gate | `mismatched=0`, all three rows `verdict=MATCH` |
| index gate | `missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, and `indexed=N/N` for **N = number of `corpus/knowledge/*.md` at the tip** (61 at the freeze; C2's new note makes it 62) |
| c1-r44-v2 | `fixtures=26/26 tool=present verdict=TARGET_MET` and inner `PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET` |
| c2-r44-v2 | `admitted=1/1 verdict=TARGET_MET` with `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1` |
| geometry selftest | `94/94` (the round-45 claims do not touch `tools/mado-geometry.py`, blob `d5f50df12ab32abd172d17b039c93daec2a94ff7`) |
| mado-verify selftest | `460/460` unless the tip legitimately edits `tools/mado-verify.sh` (blob `9113c7c05e586328f44ed6822a3d12ff34c47a36`); a changed count without that edit is harm |
| evidence-pointers | `verdict=TARGET_MET`, `dangling_r36=0`, `inherited_dirty=0`, `scratch_disposition_ok=1`, `tip_axis_transcript=1` |
| index-rows | `errors=0`; `warns` may only grow by a *cited-glob-nomatch* warn belonging to the new note |
| locators/index-rows/axis/index selftests | pass counts unchanged (18/18, 10/10, 18/18, 12/12) |
| counter-selftest / counter-discrimination / r38-discrimination | `pass=59 total=59`, `25/25`, `19/19` |
| population-suite | still `FAIL fixtures=46 failed=9` with the same nine names — a *different* failure set means someone edited `check-population.py` or the suite |
| r45 counters | blobs still `6642ebfce65269a5d45b4ac97491465784f3c559` / `61bd4bee0c98ec52280a407a402908aa302ff56e`; a data commit that edits a frozen counter is out of contract |
| lane status on the gate plane | `git status --porcelain -- quality tools corpus SCORECARD.md LOG.md` empty |

Allowed to move, by registration:

- `check-index` `indexed=61/61` → `62/62` and `corpus/README.md` grows one row (C2's note).
- axis `operability 12/12` → `13/13` (C1's tool selftest) and `navigation` may re-derive if the note is a
  navigation surface; either way `mismatched=0`.
- census `W04` count 7 → 9: S303 repeats S162's legacy `ConfigManager.cpp` URL and S307 repeats S158's
  `HyprCtl.cpp` URL, which the registration declares as W04, not errors. **Any other new `W04`, or a `W01`
  count above 1, is a finding.** Census `ok` line and exit 0 are invariant.
- `check-index-rows` `rows=61` → `62`, plus at most one new warn for the new note.

## 6. How to re-run this baseline at any other revision

```sh
S=/fast/scratch/hyaku/mado-r45/<seat>; mkdir -p "$S"
D=$(mktemp -d -p "$S"); git clone -q --shared /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
git -C "$D" checkout -q --detach <REV>; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
L=/home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I $L/quality/check-axis-scores.py --rev <REV> --repo "$D"
python3 -I $L/quality/check-index.py --rev <REV> --repo "$D"
python3 -I $L/quality/counters/c1-r44-geometry-states-v2.py --repo "$D" --rev <REV> --work "$S/w"
python3 -I $L/quality/counters/c2-r44-gkeep-size-request-v2.py --repo "$D" --rev <REV>
python3 -I "$D/tools/mado-geometry.py" --selftest
bash "$D/tools/mado-verify.sh" --selftest
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

The extended set is rows 10–22 of §1; `gates/` holds the exact argv for each, including the round-36/38/35
pinned inputs that the gates need and the r38 sandbox root (keep the sandbox under `/fast/scratch`).

## 7. Limits (what this baseline does not say)

- It states gate **verdicts**, not gate **teeth**. That each gate fails on the defect it names is a
  different measurement (the round-38 and round-44 controls, rows 5–6 and 16–17, cover part of it).
- `tools/mado-verify.sh --selftest` hardcodes `/tmp/w5-mado-m52-*` for its fixtures; I exported `TMPDIR`
  into the scratch tree, but that script's own `mktemp` path is fixed, so its fixtures lived in `/tmp`
  (small, removed by the script). Not cited as evidence.
- `population-suite.py` writes its fixtures under `$TMPDIR`, `counter-selftest.py` under `--scratch`,
  `check-r38-discrimination.py` under `--sandbox-root`; all three were pointed into
  `/fast/scratch/hyaku/mado-r45/ExecHarmBase` explicitly and deleted at the end of the seat.
- No compositor read was needed for this seat (`hyprctl` was not run); no host config, service or package
  was touched; `pacman` was not run.
- Rows 1, 3, 5, 6 ran the lane's **current** gate bytes against the rev; rows 2, 4, 7, 8 and 10–22 ran the
  gate script **as committed at that rev** (`<clone>/quality/…`); row 9 ran the fleet census script on the
  lane's current tree. The blobs in §2 are equal at both revs, so the distinction is immaterial here and is
  recorded only so a future reader can tell which binary produced which line.
