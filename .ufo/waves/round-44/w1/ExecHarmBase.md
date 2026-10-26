# ExecHarmBase — round 44 w1, harm-check baseline at the base

Target: the **base side** of the round's no-harm comparison. Every command below was executed on a fresh clone of
`6a1a90528fe533cadee506a9fa3e9d13d15cc41f` (`mktemp -d -p /fast/scratch/hyaku/mado-r44/ExecHarmBase`, `git clone -q --shared`
of the lane, `git rev-parse --show-toplevel` verified == clone root, then `git -C <clone> checkout -q --detach 6a1a905…`).
Clone deleted; every citation points into this seat directory.

## Verdict

**14 of the 15 executed gates are green at the base; one is red for a pre-existing, clone-reproducible reason**
(`tools/mado-evidence-audit.py --selftest`, §F1). That row is a *base-red* row, so it is outside the no-harm set — it cannot be
“broken” by the round and it must never be cited as base-green. The base is otherwise clean: `verify 460/460`,
`options 211/211`, `globals 63/63`, `geometry 73/73`, `action-plan 52/52`, `assessment 20/20`, `tripwire 9/9 + 16/16 + 33/33`,
`check-index 60/60`, `check-index-rows rows=60 errors=0 warns=3`, `check-axis-scores 3× MATCH mismatched=0`,
`check-locators --selftest PASS`, `sources-census validate` exit 0.

Counts at the base: **tools 12** (11 `.py` + 1 `.sh`), **corpus/knowledge 60**, **registry rows 234**, **QUALITY criteria 81**
(numbers 1..81 contiguous, last = 81).

## §A The fifteen executed commands (CWD = clone root)

| # | command | rc | summary |
|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` |
| 2 | `python3 -I tools/mado-options.py --selftest` | 0 | `MADO_OPTIONS_SELFTEST: 211/211 passed` |
| 3 | `python3 -I tools/mado-globals.py --selftest` | 0 | `MADO_GLOBALS_SELFTEST: 63/63 passed` |
| 4 | `python3 -I tools/mado-geometry.py --selftest` | 0 | `MADO_GEOMETRY_SELFTEST: 73/73 passed` |
| 5 | `python3 -I tools/mado-action-plan.py --selftest` | 0 | `SELFTEST_SUMMARY: 52/52 passed` |
| 6 | `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` | 0 | 20 cases, 20 pass, code 0 |
| 7 | `python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures` | **2** | `FileNotFoundError` → `could-not-evaluate` (§F1) |
| 8 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core` | 0 | `9/9 passed failed=[]` |
| 9 | `… --selftest .ufo/waves/round-17/tripwire/compound` | 0 | `16/16 passed failed=[]` |
| 10 | `… --selftest .ufo/waves/round-17/tripwire/hardening` | 0 | `33/33 passed failed=[]` |
| 11 | `python3 -I quality/check-index.py --rev 6a1a905… --repo .` | 0 | `indexed=60/60 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 12 | `python3 -I quality/check-index-rows.py --rev 6a1a905… --repo .` | 0 | `rows=60 errors=0 warns=3` (same 3 rows as round 43) |
| 13 | `python3 -I quality/check-axis-scores.py --rev 6a1a905… --repo .` | 0 | `nav 60/60 MATCH · calib 68/68 MATCH · oper 12/12 MATCH · mismatched=0` |
| 14 | `python3 -I quality/check-locators.py --selftest` | 0 | `cases=18 passed=18 locators=19 miss=6` / `flips=11 ok_to_miss=4 miss_to_ok=5` / `PASS` |
| 15 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | lane `ok` + 7×W04 + 1×W01 (warnings only, no E-code) |

Selftest enumeration was read from each tool's own usage/docstring, not assumed: eight of the twelve tools offer one;
`mado-anims.py`, `mado-binds.py`, `mado-eventq.py`, `mado-wsrules.py` have **none** (`grep -c -- '--selftest'` = 0 each), so
there was nothing to run for them. `check-index-rows.py`'s shipped usage is `[--rev REV] [--repo REPO] [--root ROOT] [--selftest]`
(its `-h`), so the assigned bare form cannot run and row 12 records the `--rev/--repo` mode.

## §F1 The one base-red gate: `tools/mado-evidence-audit.py --selftest` in a clone

```
$ python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures
{"code": 2, "error": "FileNotFoundError", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}   rc=2
```

Cause (measured, not inferred): the fixture manifest declares two **empty directories** as inputs and git cannot store an
empty directory, so no clone of any revision has them —
`{"kind":"directory","path":"cases/AuditRawPathEscape/root"}` and
`{"kind":"directory","path":"cases/AuditRawPathDotDotInternal/root/sub"}` in
`.ufo/waves/round-22/audit/fixtures/expected.json`; `git ls-tree -r --name-only 6a1a905 | grep -cE
'AuditRawPathEscape/root/|AuditRawPathDotDotInternal/root/sub/'` = **0** (same at HEAD). The live lane worktree has both
directories, untracked and invisible to `git status`.

Controlled A/B on the same clone (only those two directories created):
`mkdir -p …` → `{"code": 0, "result": "clean", "passed": 46, "total": 46, expected_sha256 b5df74b5…, tool_sha256 277eced2…}` rc=0,
and `git status --porcelain` stays empty. `git log --oneline --all -- <those case dirs>` returns the single landing commit
`5c7b9831` (round 22), so this is a round-22 property of the fixture set. **Any later receipt that calls this selftest green
must name where it obtained the two directories.**

## §F2 Differences against `.ufo/waves/round-43/w2/ExecHarmTip/harm.txt` (present, read in full)

That file measures the round-43 pair `a35cfdf → 1959770` with eight gates; this one measures the round-44 base only.

1. **Revision**: mine is 9 commits past `a35cfdf` (base is the round-43 verifier spot-check, 5 commits past the round-43 data
   commit and after `2a3707c`).
2. **Gate set**: theirs 8 commands, mine 15. New here: action-plan, assessment, evidence-audit, tripwire ×3, sources-census.
3. **geometry**: absent at their base, `73/73` at their data — `73/73` at my base.
4. **index**: their base 59/59 → data 60/60; my base is 60/60 (the round-43 entry is in the base tree).
5. **index-rows**: same shape and the same three warns at my base as at their data (`rows=60 errors=0 warns=3`).
6. **axis**: their data column was RED (published 59/59 & 63/63 vs derived 60/60 & 68/68, mismatched=2), and they predicted
   green at `2a3707c` with published 60/60 and 68/68. My base measures exactly that prediction: 3× MATCH, mismatched=0, rc 0.
   The round-43 lag window is closed before the round-44 base.
7. **locators**: my base summary is character-for-character their data-column line.
8. **verify/options/globals**: identical counts to their data column (460, 211, 63).
9. **Their file has no base-red gate; mine has one** (§F1, pre-existing).
10. **census**: not in their file; exit 0 with 8 contract warnings here. Both files decline the same five
    round-argument-dependent checkers (`check-control-receipts`, `check-population`, `counter-selftest`,
    `check-counter-discrimination`, `check-r38-discrimination`) for the same reason: their inputs are not named by the seat
    assignment.

Instrument watch: `tools/mado-geometry.py` at the base hashes `e3c2e471…`, i.e. byte-identical to the round-42 reference
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (`e3c2e471…`), and **not** round-44's reference `c1/ctl-ref-tool.py.txt`
(`8e871a00…`). The base tool is the unmodified round-43 instrument, as the round-43 harm receipt also recorded.

## Artifacts in this seat directory

```
34f762ac8e8fd8b9e9e4a242944f4ed66bb8e1c88ba4e3b9525520a0f20e3daf  harm-base.txt                    (full baseline, §A–§G + verbatim log)
a2b0afef071c3dbee0f58aa2ecd52d48a3f5c140dd51cca5c3a3fda244251aa9  gate-log.txt                     (the 15-gate driver output, unedited)
18e741d657c77e8c3a1731b0ec7dbc40f8b161f820a9f1b9469afe43efd86834  evidence-audit-after-mkdir.json  (§F1 A/B, post-mkdir 46/46)
```

## State and limits

- Scratch `/fast/scratch/hyaku/mado-r44/ExecHarmBase` (clone + driver) **deleted** after receipts were copied here.
- Lane footprint: no tracked file touched; `git -C <lane> status --porcelain` shows only untracked round-44 wave paths
  (this seat dir, `.ufo/waves/round-44/w1/`, `l1-draft/`, `w1.ready*`); `git status --porcelain -- tools/ quality/ corpus/
  SKILL.md PROVINCE.md` is empty.
- No tool was installed or updated; no pacman transaction; no compositor command; no host-service action.
- Not run, with reason: the five round-argument checkers named in §F2.10, and no live compositor read (a clone baseline has
  no live side).
- This file is the base side only; the no-harm verdict is the integrating seat's comparison of this baseline against the
  round's data commit.
