# Harm watch baseline — lane gates at base `b22ea56` and at the freeze `8c5434c`

Seat `ExecHarmBase` (mado round 46, wave w1, leaf executor). Read-only measurement: nothing in the lane was written except
this seat directory; all work ran in two throwaway clones under `/fast/scratch/hyaku/mado-r46/ExecHarmBase/`.

Purpose: give the L1 a before/after table for the data tip. Every row below was run twice — once against a clone checked out
at the round-46 **base** `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, once against a clone checked out at the **freeze**
`8c5434c60e03f147ee1f75ab195e8bc3f0db4dec` (freeze commit on top of the base: `git log --oneline -3` lists it directly
above the base).

## 0. Method

```
S=/fast/scratch/hyaku/mado-r46/ExecHarmBase
L=/home/vgpnk/Projects/shokunin/mado-shokunin
git clone -q --shared --no-checkout "$L" "$S/base"
git -C "$S/base" rev-parse --show-toplevel          # -> $S/base   (asserted before any use)
git -C "$S/base" checkout -q --detach b22ea56bff2faec39ce9ff75d2107eaf4612ecbe
git clone -q --shared --no-checkout "$L" "$S/freeze"
git -C "$S/freeze" rev-parse --show-toplevel        # -> $S/freeze (asserted)
git -C "$S/freeze" checkout -q --detach 8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
```

Host tools used: `python3` 3.14.8 (`-I` on every gate), `bubblewrap` 0.13.1 (clauses that sandbox), `git` read-only.
No compositor connection was made by this seat; no pacman, no host write, no input injection.

Gate-script identity across the three revisions (so "lane-path gate" and "rev-tree gate" are the same bytes):

| file | blob at base | blob at freeze | blob at `e0be61e4` (lane HEAD) |
|---|---|---|---|
| `quality/check-axis-scores.py` | `cdfc9a81` | `cdfc9a81` | `cdfc9a81` |
| `quality/check-index.py` | `d9076762` | `d9076762` | `d9076762` |
| `quality/check-index-rows.py` | `05c7255d` | `05c7255d` | `05c7255d` |
| `quality/check-evidence-pointers.py` | `c2dcdc9e` | `c2dcdc9e` | `c2dcdc9e` |
| `quality/check-session-material.py` | `9d60e4c1` | `9d60e4c1` | `9d60e4c1` |
| `quality/counters/c1-r45-monitors-v2.py` | `2c61f46d` | `2c61f46d` | `2c61f46d` |
| `quality/counters/c2-r45-monitor-entry-v2.py` | `7a966514` | `7a966514` | `7a966514` |
| `tools/mado-monitors.py` | `551eceef` | `551eceef` | `551eceef` |
| `tools/mado-geometry.py` | `d5f50df1` | `d5f50df1` | `d5f50df1` |
| `tools/mado-verify.sh` | `9113c7c0` | `9113c7c0` | `9113c7c0` |

`git diff --stat b22ea56 8c5434c -- quality tools corpus` prints exactly three added files
(`quality/counters/c1-r46-devices.py`, `c1-r46-fixtures.json`, `c2-r46-input-device-entry.py`, 4418 insertions);
`git diff --stat 8c5434c e0be61e4 -- quality tools corpus` is empty. So no gate was edited between the two revisions
being compared, and a gate's verdict can only move for data reasons.

## 1. Enumerated gates — base vs freeze

Commands are given in full in §3. "last line" is the final non-empty stdout line; receipts are in
`w1/ExecHarmBase/receipts/` (line numbers below are computed by `grep -n` in those files).

| # | gate | base last line | base exit | freeze last line | freeze exit | delta |
|---|---|---|---|---|---|---|
| 1 | `quality/check-axis-scores.py --rev/--repo` | `MADO_AXIS: checked=3 mismatched=0 rev=b22ea56bff…` (`base-axis.txt:4`) | 0 | `MADO_AXIS: checked=3 mismatched=0 rev=8c5434c60e…` (`freeze-axis.txt:4`) | 0 | none |
| 2 | `quality/check-index.py --rev/--repo` | `MADO_INDEX: rev=b22ea56bff… indexed=62/62 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` (`base-index.txt:1`) | 0 | same with `rev=8c5434c60e…` (`freeze-index.txt:1`) | 0 | none |
| 3 | `quality/counters/c1-r45-monitors-v2.py --repo --rev --work` | `PRED-C1-r45-v2: fixtures=81/81 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=b22ea56bff… seeds=45,1522954641` (`base-c1r45.txt:86`) | 0 | `… verdict=TARGET_MET rev=8c5434c60e… seeds=45,311901436` (`freeze-c1r45.txt:86`) | 0 | none (nonce differs by design) |
| 4 | `quality/counters/c2-r45-monitor-entry-v2.py --repo --rev` | `PRED-C2-r45-v2: admitted=1/1 verdict=TARGET_MET rev=b22ea56bff…` (`base-c2r45.txt:68`) | 0 | same, `rev=8c5434c60e…` (`freeze-c2r45.txt:68`) | 0 | none |
| 5 | `tools/mado-monitors.py --selftest` (clone tree) | `MADO_MONITORS_SELFTEST: 48/48 passed` (`base-tools-selftests.txt:9`) | 0 | identical (`freeze-tools-selftests.txt:9`) | 0 | none |
| 6 | `tools/mado-geometry.py --selftest` (clone tree) | `MADO_GEOMETRY_SELFTEST: 94/94 passed` (`base-tools-selftests.txt:7`) | 0 | identical (`freeze-tools-selftests.txt:7`) | 0 | none |
| 7 | `bash tools/mado-verify.sh --selftest` (clone tree) | `MADO_SELFTEST: 460/460 assertions passed` (`base-verify-selftest.txt:1`) | 0 | identical (`freeze-verify-selftest.txt:1`) | 0 | none |
| 8 | `scripts/sources-census.sh validate --root … mado` | live lane: `mado	ok	…/mado-shokunin/corpus/SOURCES.md` (`census-live.txt:11`), 10 W-lines, 0 E-lines | 0 | registered at the base clone: `base	ok	…/base/corpus/SOURCES.md` (`census-base.txt:11`); at the freeze clone: `freeze	ok	…/freeze/corpus/SOURCES.md` (`census-freeze.txt:11`) — same 10 warning lines (9×W04 + 1×W01) | 0 / 0 | none |

Census detail: the warning set is identical in all three arms — W04 on S030, S042, S045, S097, S119, S120, S121, S303, S307
and W01 on S277 (`census-live.txt:1-10`), no `E` code, no `FLEET` anomaly. The live lane tree is at `e0be61e4`, one commit
above the freeze, and its registry parses to the same finding set as the freeze clone.

## 2. Supplementary gates (same two revisions)

| gate | base | freeze | notes |
|---|---|---|---|
| `quality/check-index-rows.py --rev/--repo` | `MADO_INDEX_ROWS: rev=b22ea56bff… rows=62 errors=0 warns=3` (`base-index-rows.txt:1`) | same, `rev=8c5434c60e…` (`freeze-index-rows.txt:1`) | the 3 warns are the known `cited-glob-nomatch` rows (round-12 ×2, round-24 ×1) |
| `quality/check-evidence-pointers.py --repo --rev` | `PRED-PTR-r36-v1 … dangling_r36=0 … verdict=TARGET_MET` (`base-evidence.txt:1`) | identical verdict (`freeze-evidence.txt:1`) | |
| `quality/check-session-material.py --repo --rev` | `SESSION_MATERIAL: files=17070 findings=97 rev=b22ea56bff…` (`base-session-material.txt:99`), rules `R1=23 R2=26 R3=46 R4=2` (`:98`) | `files=17094 findings=97 rev=8c5434c60e…` (`freeze-session-material.txt:99`), same rule tallies (`:98`) | exit 1 at both — inherited red, see F5 |
| `quality/*.py --selftest` | axis `18/18` (`selftest-check-axis-scores.txt`), index `12/12`, index-rows `10/10`, locators `SELFTEST: PASS` (18 cases, 19 locators), session-material `22/22` (`selftest-check-session-material.txt`) | same five files are rev-identical (§0), exit 0 | |
| every `tools/*.py --selftest` | `base-tools-selftests.txt` | `freeze-tools-selftests.txt` — `diff` of the two files is empty | rc 0: action-plan 52/52, geometry 94/94, globals 63/63, monitors 48/48, options 211/211; rc 2 for anims/binds/eventq/tripwire/wsrules (no `--selftest` flag) and for assessment/evidence-audit (flag needs an argument) |
| `tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` | `MADO_PLAN: frozen_match` (`base-registered-gates.txt:2`) | same (`freeze-registered-gates.txt:2`) | exit 0 both |
| `tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` | exit 0 (`base-registered-gates.txt`) | exit 0 | |
| `tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures` | `{"code": 2, "error": "FileNotFoundError", …}` exit 2 (`base-registered-gates.txt:9`) | same, exit 2 (`freeze-registered-gates.txt:9`) | see F4 |
| `.ufo/waves/round-33/c2/count.py --repo --scorecard` | `PRED-C2-r33-v1 … verdict=TARGET_MET` (`base-registered-gates.txt:12`) | identical (`freeze-registered-gates.txt:12`) | exit 0 both |
| `quality/population-suite.py --checker quality/check-population.py` | `SUITE verdict=FAIL fixtures=46 failed=9 …` (`population-suite-base.txt:94`), exit 1 | identical (`population-suite-freeze.txt:94`), exit 1 | see F2 |
| `quality/population-suite.py --checker .ufo/waves/round-26/quality/check-population.py` | `SUITE verdict=PASS fixtures=46 failed=0 -` (`population-suite-r26checker.txt:47`), exit 0 | same (`freeze-population-suite-r26checker.txt:47`), exit 0 | see F2 |
| `quality/counter-selftest.py --c1 .ufo/waves/round-26/c1/count.py --c2 .ufo/waves/round-26/c2/count.py --rev …` | `SELFTEST pass=57 total=59` / `FAILED c1-version-guard,c1-version-missing-commit` / `exit=1` (`counter-selftest-r26-base.txt:446-448`) | identical (`counter-selftest-r26-freeze.txt:446-448`) | see F3 |
| `bash tools/mado-verify.sh --no-live` | rev-invariant script; run once from the freeze clone | `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)` (`no-live.txt:46`), exit 0 | file plane over the real host config, read-only |
| claim counters of this round (not gates) | `PRED-C1-r46: … tool=absent verdict=TARGET_MISSED` (`base-c1r46.txt:2`), `PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED` (`base-c2r46.txt:2`), both exit 1 | `PRED-C1-r46: … tool=absent verdict=TARGET_MISSED` (`freeze-c1r46.txt:2`), `PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED` (`freeze-c2r46.txt:2`), both exit 1 | see F6 |

**Delta summary: zero.** Every enumerated gate returns the same verdict at `b22ea56` and at `8c5434c`. Four invocations are
red at *both* revisions — `population-suite` (with the lane's current checker), `counter-selftest` (with the round-26
counters), the `evidence-audit` selftest in a clean checkout, and `check-session-material`'s 97 findings — and every other
invocation in §1–§2 is green at both. None of the four reds is caused by the freeze: each is reproduced identically, and
each is attributed to a commit at or before the base in §4.

## 3. Commands, verbatim

```
# 1/2 axis + index (per rev)
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py --rev <REV> --repo <CLONE>
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-index.py        --rev <REV> --repo <CLONE>

# 3/4 round-45 counters (per rev; --work outside the repo, its lane and that lane's parent)
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r45-monitors-v2.py \
        --repo <CLONE> --rev <REV> --work /fast/scratch/hyaku/mado-r46/ExecHarmBase/work-c1-<arm>
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r45-monitor-entry-v2.py \
        --repo <CLONE> --rev <REV>

# 5/6/7 tool self-tests, from the clone tree
cd <CLONE> && python3 -I tools/mado-monitors.py --selftest
cd <CLONE> && python3 -I tools/mado-geometry.py --selftest
cd <CLONE> && bash tools/mado-verify.sh --selftest

# 8 census (live lane, then each clone by explicit directory)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin <CLONE>

# supplementary
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-index-rows.py --rev <REV> --repo <CLONE>
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-evidence-pointers.py --repo <CLONE> --rev <REV>
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py --repo <CLONE> --rev <REV>
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/population-suite.py --checker <CLONE>/quality/check-population.py
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/population-suite.py --checker <CLONE>/.ufo/waves/round-26/quality/check-population.py
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counter-selftest.py \
        --c1 <CLONE>/.ufo/waves/round-26/c1/count.py --c2 <CLONE>/.ufo/waves/round-26/c2/count.py \
        --rev <REV> --scratch /fast/scratch/hyaku/mado-r46/ExecHarmBase/work-cs26<arm>
cd <CLONE> && bash tools/mado-verify.sh --no-live
```

`<REV>`/`<CLONE>` are `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`/`…/ExecHarmBase/base` and
`8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`/`…/ExecHarmBase/freeze`.

## 4. Findings

**F1 — round-45 closure D1, counter half: the never-run w2 falsification now runs, and both counters hold at both revs.**
`c1-r45-monitors-v2` reports `fixtures=81/81 generated=150/150 … verdict=TARGET_MET` (`receipts/base-c1r45.txt:86`,
`receipts/freeze-c1r45.txt:86`; nonces 1522954641 and 311901436, so the generated 150 are independent per run), and
`c2-r45-monitor-entry-v2` reports `admitted=1/1 verdict=TARGET_MET` with `clauses=a:1 b:1 … j:1`
(`receipts/base-c2r45.txt:68`, `receipts/freeze-c2r45.txt:68`). This is the counter re-run only; the semantic attack on
the round-45 tool/entry belongs to the attack seats. It supports closure D1 (`corpus/lessons/round-45-verifier-spotcheck.md:102`)
rather than closing it.

**F2 — `mado-r27-population-suite` (SKILL.md:725) is red at both revs with the lane's current checker, green with its own
recorded subject.** `quality/population-suite.py` (blob `31ece716`, unchanged since `5c1d4957`, round 27) FAILs 9 of 46
built-in fixtures against `quality/check-population.py` (blob `c8b47f76`, sha256 `17e99993…`, last touched by `317ff19c`,
round-28 integration): `green-numerator-not-compared, red-denominator-larger, red-denominator-smaller,
red-case-lines-and-denominator, red-registered-total-differs, red-second-summary-disagrees, red-first-summary-disagrees,
exit2-cases-pass-space-before-equals, exit2-cases-pass-space-after-equals` (`receipts/population-suite-base.txt:94`).
Against the round-26 checker the same suite is `PASS fixtures=46 failed=0` (`receipts/population-suite-r26checker.txt:47`),
and that round-26 checker is exactly the subject the round-27 evidence names
(`.ufo/waves/round-27/evidence/c2-after-0b53bd86.txt:4`, sha256 `803e0096…`, equal to the file's sha now). So the red is a
subject swap made in round 28, inherited unchanged by round 46 — not a round-46 harm, but the gate row's plain invocation
(`--checker PATH` with the lane's own checker) is red as published.

**F3 — `mado-r27-counter-selftest` (SKILL.md:724) is not executable as published at either rev.** With the round-26 counters
its verdict is `SELFTEST pass=57 total=59` and `FAILED c1-version-guard,c1-version-missing-commit`, exit 1
(`receipts/counter-selftest-r26-base.txt:446-448`, same at the freeze). The two failing checks are discrimination checks: the
mutated counters are expected to be *rejected* and are not (`ORACLE_VERSION=no`, e.g. `:159`, `:167`). The counter bytes are
the ones the round-26 green receipt pinned (`f98e264b…` c1, `b92c32d…` c2 — identical to `.ufo/waves/round-26/quality/counter-selftest-green.txt:3-4`),
so the drift is in the gate (current `quality/counter-selftest.py` sha256 `d72b7f1a…` vs the receipt's `0754f501…`). With the
round-27 counters the same command aborts instead of scoring: `AttributeError: module 'mado_r27_q_c2' has no attribute 'O'`
(`quality/counter-selftest.py:458`) — the gate binds a round-26 module attribute that `round-27/c2/count.py` does not have.
Consequence for this round: neither the round-45 nor the round-46 counters can be scored by a registered selftest gate; their
only selftest evidence is clause `s` inside the counters themselves.

**F4 — `mado-evidence-audit` (SKILL.md:2082) cannot be reproduced from committed bytes.** In a clean clone of either rev,
`python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures` exits 2 with
`{"code": 2, "error": "FileNotFoundError", …}` (`receipts/base-registered-gates.txt:9`, `receipts/freeze-registered-gates.txt:9`).
Cause: two fixture directories are **empty** and therefore cannot be committed —
`…/cases/AuditRawPathDotDotInternal/root/sub` and `…/cases/AuditRawPathEscape/root`. `git ls-tree -r` over those two case
dirs lists only `bundle.json`, `root/snapshot.json`, `bundle.json`, `outside.json`; the clones' tree holds 267 paths under
`fixtures/` while the lane working tree holds 269 (`receipts/base-fx.txt` vs `receipts/lane-fx.txt`). Creating the two
directories in the clone makes the same command exit 0 with `cases=46 failed=[]` at both revs
(`receipts/base-evidence-audit-after-mkdir.txt`, `receipts/freeze-evidence-audit-after-mkdir.txt`). The gate is therefore
green only where someone has run it before; any non-author verifying from a checkout sees red. Fix needs a tracked
placeholder whose presence does not change the two raw-path cases — L1-owned, not done here.

**F5 — `check-session-material` red is inherited, and the freeze adds 24 files without a single new finding.**
`files=17070 findings=97` at the base and `files=17094 findings=97` at the freeze, with identical rule tallies
`R1_CLIENT_DUMP=23 R2_PROC_TABLE=26 R3_MONITOR_IDENT=46 R4_HOME_LISTING=2` (`receipts/base-session-material.txt:98-99`,
`receipts/freeze-session-material.txt:98-99`). The round-45 data receipt already recorded `findings=97` at `ee6659b9`
(`.ufo/waves/round-45/receipts/session-material-data.txt:100`), and the closure accounts the split as 97 findings of which
49 are synthetic, i.e. the `48 pre-existing` of D3 (`corpus/lessons/round-45-verifier-spotcheck.md:54`, `:112`). So round 46
inherits exactly the D3 backlog and adds nothing; the gate stays red at the data tip unless D3 is worked.

**F6 — neither round-46 claim is pre-achieved at the base or at the freeze.** `PRED-C1-r46` reports `tool=absent`,
`fixtures=0/90 generated=0/150`, `verdict=TARGET_MISSED`, exit 1 (`receipts/base-c1r46.txt:2`, `receipts/freeze-c1r46.txt:2`),
and `PRED-C2-r46` reports `clauses=a:0 … j:0 admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/base-c2r46.txt:2`,
`receipts/freeze-c2r46.txt:2`) — the registered before-states (`.ufo/waves/round-46/registration.md`, C1 "Before (base)" and
C2 "Before (base)") reproduce verbatim at both revisions.

## 5. What the L1 should compare at the data tip

1. Rows 1–8 of §1 must stay green with identical metric lines (the axis/index counters may only grow their `derived=`/`indexed=`
   numbers, never mismatch).
2. `check-index-rows.py` must stay `errors=0`; a new corpus row or README row that breaks fidelity moves this line.
3. `check-session-material.py` must not exceed `findings=97` and must not gain an `R3`/`R4` finding; a *lower* number is the
   D3 work landing.
4. The census must stay `ok` with exactly the 10 inherited W-lines; a new E-code (E03 duplicate id, E04 shared URL+scope,
   E11 missing used-by) is the failure mode of the new S316-S325 rows.
5. `tools/mado-devices.py --selftest` and the C1/C2 counters are the claim side, not this baseline; F2/F3 show no registered
   gate will score them, so clause `s` inside `c1-r46-devices.py` is the only selftest evidence.
6. Rows F2–F4 should not be counted as regressions of round 46 — they are identical at base and freeze, and each is already
   attributed to a specific commit above.

## 6. Not run, with reason

| arm | why |
|---|---|
| `mado-verify.sh --live` | the host guard allows only `hyprctl version/devices -j/monitors [-j]/monitors all -j/getoption`; this gate also reads `instances`, `configerrors`, `binds`, `layers`. Deliberately not run. |
| `mado-verify.sh --regression`, `--frozen-regression`, `--source-merge` | need the sibling `tameshi-shokunin` mutation harness / per-round frozen dirs; out of this seat's lane and not a repo-rev property. |
| `mado-verify.sh --snapshot`, `--snapshot-diff` | need caller-supplied receipts (write a caller-chosen file); no receipt exists at either rev to compare. |
| `mado-r26-population`, `mado-r26/r27-control-receipts` | need a round data registry with `createdAt` and a registration carrying registered targets. `quality/check-population.py --registration .ufo/waves/round-45/registration-v2.md …` answers `POPULATION verdict=UNREADABLE … no **PRED-...** sentence with a supported target`, exit 2 (`receipts/check-population-r45.txt:1`). |
| host compositor probes | not part of a gate baseline; this seat made no compositor call. |

Scratch note: `/fast/scratch/hyaku/mado-r46/ExecHarmBase` (547 MB, deleted after this report) held the two clones and the
collection work dirs; every quoted line was copied into `w1/ExecHarmBase/receipts/` before deletion. No scratch path is
offered as evidence beyond naming where the command ran.
