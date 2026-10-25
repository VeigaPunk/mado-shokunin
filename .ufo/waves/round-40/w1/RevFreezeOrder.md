# RevFreezeOrder — freeze audit, round 40 (hyaku 7, 2026-10-25)

Target: freeze commit `5e7e88525cc539563de7746361b2650802e81809` vs `.ufo/waves/round-40/registration.md`.
Lineage verified: `9fc511d` (base) → `5e7e885` (freeze) → `e2b51d3` (w1 spec/dispatch, tip);
`git merge-base --is-ancestor` confirms base is the freeze's parent (`git log --format='%H %P' -3`).

## Verdict

The freeze is **complete and pure**: all 14 committed files are declared by the registration,
nothing declared is missing, and no delivered tool, entry, registry row or Gate line is in it.
Both counting commands run as written against base and reproduce the frozen before-receipts
exactly. Both frozen control harnesses re-run to byte-identical results (18/18, 21/21).
Findings below are clause-audit observations; none blocks the freeze.

## Axis 1 — completeness: everything declared is in the commit

`git show --stat 5e7e885` lists exactly 14 files; every one is named by the registration:

| committed path | declared as |
|---|---|
| `.ufo/waves/round-40/registration.md` | "This file" |
| `quality/counters/c1-r40-live.py` | C1 predicate PRED-C1-r40-v1 |
| `quality/counters/c2-r40-forms-entry.py` | C2 predicate PRED-C2-r40-v1 (clauses a–h) |
| `.ufo/waves/round-40/ctl/run-c1-controls.py` | C1 harness |
| `.ufo/waves/round-40/ctl/run-c2-controls.py` | C2 harness |
| `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt` | "the reachability control (c1/ctl-ref-tool.py.txt…)" |
| `.ufo/waves/round-40/c1/native-capture.jsonl` | "the native-capture receipt" |
| `receipts/{axis-base,c1-before-base,c2-before-base,census-before,ctl-c1,ctl-c2,selftest-base}.txt` | base/control/round-start receipts |

Criterion-64 check: `git cat-file -e 5e7e885:<path>` → AT-FREEZE for both counters
(`quality/counters/c1-r40-live.py`, `quality/counters/c2-r40-forms-entry.py`) and all 12
round-40 paths, plus pre-existing `quality/check-axis-scores.py`, `tools/mado-verify.sh`,
`tools/mado-options.py`, `quality/check-index.py`, `corpus/lessons/round-39.md`.
Nothing extra: 1+2+2+7+1+1 = 14, all accounted for.

## Axis 2 — purity: no delivered data in the freeze

- All 14 `---` path lines in the patch are `--- /dev/null` (new files only); no path outside
  `.ufo/waves/round-40/` and `quality/counters/` is touched. No `tools/`, no `corpus/`, no
  registry file.
- "Gate" scan of the full patch (`grep -inE '\bgate'`, 27 hits): every hit is counter/harness
  source (GATE_RE at `quality/counters/c2-r40-forms-entry.py`, fixture builders in
  `ctl/run-c2-controls.py`), a control output line, or the registration's own meta-sentence
  "the entry, the registry rows and every Gate line are data and land after the freeze".
  No delivered Gate verdict line.
- Freeze immutability since freeze: `git diff --stat 5e7e885 HEAD -- .ufo/waves/round-40
  quality/counters` shows only *additions* (make-w1-spec.py, w1-dispatch.json, w1-run.err,
  w1-spec.json in `e2b51d3`); `git status --porcelain` on those paths shows only untracked
  wave dirs (`assimilation/`, `fetch/`, `w1/`, `w1.ready`). No counter, control, capture,
  receipt or registration byte has changed since the freeze.

## Axis 3 — criterion-64: counting commands run as written against base

Substituting the base rev for `<rev>` (the commands' only placeholder):

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev 9fc511ddce708327377161202f358ce37dc266ba
PRED-C1-r40-v1 clause=b rc=0 selftest=71/71
PRED-C1-r40-v1 fixture=gen0..gen7, probe0  ok=0 rc=2 (base tool: no --live; argparse usage error)
PRED-C1-r40-v1 fixture=fail0, bad0, missing0, hostile0  ok=0 (valid live run rc=2 first)
PRED-C1-r40-v1 clauses=a:1 b:0 g:1 k:0
PRED-C1-r40-v1: fixtures=0/13 tool=present verdict=TARGET_MISSED rev=9fc511ddce708327377161202f358ce37dc266ba
EXIT=1

$ python3 -I quality/counters/c2-r40-forms-entry.py --repo . --rev 9fc511ddce708327377161202f358ce37dc266ba
PRED-C2-r40-v1 hyprctl-getoption-native-forms-r40.md clauses=a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 admitted=0
PRED-C2-r40-v1: admitted=0/1 verdict=TARGET_MISSED rev=9fc511ddce708327377161202f358ce37dc266ba
EXIT=1
```

Both reproduce `receipts/c1-before-base.txt` and `receipts/c2-before-base.txt` line-for-line
(the receipts end `exit=1`; my runs print `EXIT=1` — same content). Counter docstrings match
the registration's predicate text: C1 = 13 fixtures (8 seeded + probe + 2 failure +
missing-program + hostile-probe), clauses a/b/g/k, TARGET_MET iff all hold and P=13;
C2 = clauses a–h as registered.

Receipt re-verification (all match the registration's declared numbers):
- `axis-base.txt` ≡ re-run `python3 -I quality/check-axis-scores.py --repo . --rev 9fc511d…`:
  navigation 56/56, calibration 51/51, operability 12/12, `MADO_AXIS: checked=3 mismatched=0`,
  exit 0.
- `census-before.txt`: exactly seven `W04` rows + one `W01` row + `ok … SOURCES.md`, `exit=0` —
  as declared.
- `selftest-base.txt`: `MADO_SELFTEST: 460/460 assertions passed`, exit 0.
- `ctl-c1.txt` ≡ re-run of frozen `ctl/run-c1-controls.py` (55 s): identical 18 lines,
  `CTL_C1: controls=18 correct=18/18`; REF-reachability 13/13 fixtures yet TARGET_MISSED
  (clause b), BASE-tool 0/13, 16 mutants all <13 (M10/M11/M16 at 12/13, rest 0/13).
- `ctl-c2.txt` ≡ re-run of frozen `ctl/run-c2-controls.py`: identical 21 lines,
  `CTL_C2: controls=21 correct=21/21`; N01–N20 all 0/1, control P 1/1.
- `native-capture.jsonl`: 70 non-blank lines; form distribution int 44 / float 5 / custom 13 /
  str 8 — exactly the declared distribution; every line a single-form
  `{"option","set",<form>}` object.

## Axis 4 — clause audit: universals and non-concrete after-states

Universal clauses the counters do **not** enumerate (all procedural, in Harm watch / freeze
discipline — none is claimed as counter-scored):
1. "Any later change to a counter, a control, the capture or a declared target is a new
   predicate" — freeze discipline; verified empirically here (no drift), not machine-enforced.
2. "`bash tools/mado-verify.sh --selftest` stays 460/460" — no counter runs mado-verify.sh;
   evidence is the base receipt only; round-end re-check is procedural.
3. "`quality/check-index.py` complete; only the C2 entry adds a row (baseline 56/56)" — C2
   clause f checks only the entry's own index row; index completeness/56/56 is not
   counter-enumerated.
4. "`quality/check-axis-scores.py` `mismatched=0`" at round end — not enumerated by either
   counter.
5. "No config tree, compositor state, service, sibling lane or fleet-repo path other than the
   report is written" — wave-level universal; only the tool-level slice is enumerated (C1
   per-fixture config-root-unchanged check + mutant M12).
6. "`hyprctl getoption -j` is the only compositor verb run" — tool-level slice enumerated
   (exact-argv fixture check + mutants M07/M16); wave-level slice procedural.

After-states that are not one concrete value:
- "at the data commit and the tip" (both targets) and "at the data tip" (kill rule): the data
  commit is necessarily unnamed at freeze and the tip moves; concreteness is deferred to
  judging, where the counters pin `rev=<full hash>`. Inherent, but a judge should read the
  verdict against the hash the counter prints, not the word "tip".
- `<rev>` placeholder in both counting commands (template; substituted with base here).
- Floors/ranges, each machine-checked as a bound: C1 clause b `n >= 79` (base observed
  71/71); C2 clause c "at least 2" new ids; clause d quote "3-25 words"; rows "0-3 leading
  spaces".

## Findings by severity

**Medium (declared value without an enforcing clause).**
Registration C2 declares the host census "62 agreement / 8 agreement*, 0 mismatch … the number
the receipt states", but PRED-C2 clauses a–h never require those numbers: clause h enforces
only internal consistency (`A+B+C+D == W+X+Y+Z+V == N >= 1`) and the forms line is not bound
to the capture's 44/5/13/8 either. A live receipt stating any other self-consistent counts
(e.g. 60/10/0) passes the counter. This sits inside the declared C2 residual ("a fabricated
self-consistent set passes"), so it is not a hidden gap — but judges must not cite the C2
verdict as evidence *for* 62/8/0; only the receipt bytes and the C1 out-of-distribution report
speak to those numbers.

**Low (harm-watch command resolves only from the fleet root).**
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`: the script
exists only in the fleet repo (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`;
confirmed present); the lane's `scripts/` is empty at base and at HEAD
(`git ls-tree --name-only <rev> scripts/` → nothing). The registration states no cwd; from the
lane root implied by the surrounding section the command does not resolve. The same command
shape is also the only identification of the "Census command" behind `census-before.txt`
(the receipt's output shape matches it); the registration never names the census command
itself.

**Low (moving alias in a quoted command).**
The axis receipt is introduced as `python3 -I quality/check-axis-scores.py --repo . --rev
master` "at base" — but `master` is a moving alias, now at `e2b51d3` (the w1 spec commit), so
the literal command no longer measures base. The frozen receipt pins
`rev=9fc511ddce708327377161202f358ce37dc266ba`, and my pinned re-run reproduces it exactly,
so the evidence stands; only the quoted command's wording is stale-prone.

**Informational.**
- "the round-start receipts" (plural): exactly one round-start receipt (`census-before.txt`)
  is in the freeze; the commit message's "base receipts" covers the rest. Wording only.
- C1 clause k names CAPTURE at REV — at base it correctly reads k:0 (capture does not exist at
  base); the declared "Before" line's clauses a:1 b:0 g:1 k:0 are internally consistent with
  that, and my re-run reproduces them.

## Residual risk / verification gaps

- I did not run any live compositor verb; the 62/8/0 census and the capture's provenance are
  outside this audit (seats re-derive; see Medium finding).
- Control-harness re-runs exercise the frozen harnesses against the frozen counters — they
  verify the receipts are honest, not that the fixtures cover every real-world conversion
  (that residual is declared in the registration for both claims).
- The w1 spec/dispatch commit `e2b51d3` and the untracked wave dirs are post-freeze wave
  infrastructure; contents not audited here (out of scope).
- No tools installed; no pacman; no writes outside this report; read-only git only.

Every command above was run in this session against
`/home/vgpnk/Projects/shokunin/mado-shokunin` at tip `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`.
