# MutTool — mutation probe: `tools/mado-geometry.py` (round-44 C1, wave w2)

Seat MutTool · lane mado-shokunin · 2026-10-26. Target: `tools/mado-geometry.py`, sha256
`1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4` (489 lines; byte-identical to the
reference `.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt`). Rules per registration-v2: mutants are
scratch copies only; the lane file was never written; detector receipts live in this seat dir.

**Detectors** (same bounded detectors on pristine, mutated, and restored bytes):

1. `python3 -I <tool> --selftest` — rc + `MADO_GEOMETRY_SELFTEST: k/n passed`.
2. `cd <lane> && python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo . --rev
   e46789213830597348fe96a351ae004d10587385 --work /fast/scratch/hyaku/mado-r44/MutTool --tool
   <mutant>` — run on every selftest survivor (28 runs).

**Baseline (pristine):** selftest 94/94 rc 0; counter TARGET_MET exit 0, clauses
`a:1 b:1 b4:1 b5:1 e:1 g:1 r:1`, fixtures 26/26 (`baseline-counter.txt`).

## Method

49 single-point mutants (one minimal edit each: operator/literal swap or one-line deletion),
concentrated on the round-44 lines — client_fsmode (13), evaluate verdict chain (11), report
verdict chain / NOT_COMPARED (10), states suffix (6), selftest state assertions (6), json.loads
path (1), docstring (1), tally literal (1). Every `old` fragment was asserted to occur exactly once
in the pristine source (`mutant-manifest.json`, 51 specs incl. 2 late fixes). Line numbers below are
computed (`grep -n`) against the pristine tool.

## Results

Selftest: 21 killed / 28 passed. Counter on the 28 survivors: 25 TARGET_MET, 3 TARGET_MISSED
(M20, M41, M48). M48's miss is a detector artifact — pristine fails under the same nonce (finding
F1) — so per the baseline-failure rule M48 is **inconclusive → survivor**, not killed. Final:
**26 survivors, 23 killed** (21 by selftest; M20 by counter fixtures; M41 by counter clause b5).

| mutant | site (tool:line) | selftest | counter | verdict |
|---|---|---|---|---|
| M01-fsmode-in1 | 202 | 87/94 rc1 | – | killed |
| M02-fsmode-in2 | 202 | 91/94 rc1 | – | killed |
| M03-fsmode-in012-EQ | 202 | 94/94 | MET | survivor (equivalence) |
| M04-fsmode-boolinv | 202 | 84/94 rc1 | – | killed |
| M05-fsmode-float | 202 | 92/94 rc1 | – | killed |
| M06-fsmode-wrongkey | 201 | 85/94 rc1 | – | killed |
| M07-fsmode-ret1 | 203 | 67/94 rc1 | – | killed |
| M08-fsmode-absent1 | 204 | 67/94 rc1 | – | killed |
| M09-fsmode-in123 | 202 | 93/94 rc1 | – | killed |
| M10-fsmode-instr-EQ | 202 | 94/94 | MET | survivor (equivalence) |
| M11-fsmode-reorder-EQ | 202 | 94/94 | MET | survivor (equivalence) |
| M12-fsmode-notTrue | 202 | 94/94 | MET | survivor (equivalence, F3) |
| M13-fsmode-neg1 | 202 | 94/94 | MET | survivor (equivalence, F3) |
| M14-fs-ge2-EQ | 238 | 94/94 | MET | survivor (equivalence) |
| M15-max-ne0-EQ | 240 | 94/94 | MET | survivor (equivalence) |
| M16-label-FS-to-MAX | 239 | 89/94 rc1 | – | killed |
| M17-label-MAX-to-FS | 241 | 92/94 rc1 | – | killed |
| M18-if-not-floating | 242 | 81/94 rc1 | – | killed |
| M19-badsize-and-fs0 | 236 | 93/94 rc1 | – | killed |
| M20-tally-assign1 | 248 | 94/94 | MISSED 21/26 | killed (fixtures, F4) |
| M21-agree-and-fs0-EQ | 244 | 94/94 | MET | survivor (equivalence) |
| M22-fsmode-or0-EQ | 235 | 94/94 | MET | survivor (equivalence) |
| M23-nc-ge0 | 271 | 91/94 rc1 | – | killed |
| M24-nc-lt0 | 271 | 90/94 rc1 | – | killed |
| M25-nc-agree-ge0 | 271 | 93/94 rc1 | – | killed |
| M26-nc-rc0 | 272 | 91/94 rc1 | – | killed |
| M27-matched-and-nostate-EQ | 269 | 94/94 | MET | survivor (equivalence) |
| M28-nc-orform-EQ | 271 | 94/94 | MET | survivor (equivalence) |
| M29-nc-agree-lt1-EQ | 271 | 94/94 | MET | survivor (equivalence) |
| M30-states-ge0 | 276 | 80/94 rc1 | – | killed |
| M31-states-swap | 277 | 88/94 rc1 | – | killed |
| M32-states-dupmax | 277 | 89/94 rc1 | – | killed |
| M33-states-after-verdict | 279 | 89/94 rc1 | – | killed |
| M34-states-space | 275 | 81/94 rc1 | – | killed |
| M35-del-fullscreen-rc | 445 | 93/93 rc0 | MET | survivor (F2) |
| M36-del-fsmode-absent | 472 | 93/93 rc0 | MET | survivor (F2) |
| M37-del-fullscreen-not-agree | 447 | 93/93 rc0 | MET | survivor (F2) |
| M38-del-tiled-only-ok | 455 | 93/93 rc0 | MET | survivor (F2) |
| M39-del-fs-bool-ignored | 459 | 93/93 rc0 | MET | survivor (F2) |
| M40-del-ignored-mode-loop | 460-462 | 88/88 rc0 | MET | survivor (F2) |
| M41-json-decoder | 184 | 94/94 | MISSED b5:0 | killed (clause b5, F4) |
| M42-docstring-EQ | 73 | 94/94 | MET | survivor (doc-only) |
| M43-tally-reorder-EQ | 215-216 | 94/94 | MET | survivor (equivalence) |
| M44-nc-ne0-EQ | 271 | 94/94 | MET | survivor (equivalence) |
| M45-states-ne0-EQ | 276 | 94/94 | MET | survivor (equivalence) |
| M46-fs-in2-EQ | 238 | 94/94 | MET | survivor (equivalence) |
| M47-max-in1-EQ | 240 | 94/94 | MET | survivor (equivalence) |
| M48-differ-ne0-EQ | 267 | 94/94 | MISSED r:0 (artifact) | survivor (equivalence, F1) |
| M49-sizerules-lt1-EQ | 265 | 94/94 | MET | survivor (equivalence) |

Per-mutant counter outputs: `counter/<name>.txt`; summary `counter-summary.tsv`; selftest table
`selftest-results.tsv`.

## F1 — OPEN predicate defect: clause r is nonce-flaky; pristine can false-miss (severity MEDIUM)

**Attacks:** registration-v2 C1 clause r (the round-43 regression detector) and the registered kill
rule's reproducibility ("anything else at the data tip is a miss"). The v2 counter's clause r runs
`c1-r42-geometry.py` as a subprocess; r42's clause b2 samples 6 of 41 comparison sites by nonce
(`c1-r42-geometry.py:915-916`) and requires killed ≥ 4 (`:113`, KILL_NEED). A full sweep of all 41
sites on the pristine bytes (`site-sweep.txt`) shows **4 sites whose flip leaves the selftest green
(94/94)**: `read_regular:106` (the read loop), `read_regular:115` (the too_large raise), `run:290`
(stdin-vs-path branch), `run:292` (stdin too_large). The selftest cannot see them: it never performs
a successful file read (its three `read_regular` cases all raise before the size checks,
`mado-geometry.py:423-429`) and never calls `run()` in run mode (`--selftest` returns at
`mado-geometry.py:288-289`).

**Reproduction (pristine, no mutant):** `C1R42_TMP=<scratch> python3 -I quality/counters/
c1-r42-geometry.py --repo . --rev e467892… --tool <pristine bytes> --nonce 77b2d6f40dc46c5a` →
`clause=b2 sites=41 killed=3/6 forced_dead=1`, `clauses=a:1 b:1 b2:0 b3:1 g:1`, fixtures 37/37,
**verdict=TARGET_MISSED** (`r42-pristine-nonce-77b2d6f4.txt`). The same pristine bytes under nonce
`m48probe` → all clauses 1, TARGET_MET (`r42-m48-nonce-m48probe.txt`). M48's batch run drew exactly
this nonce for clause r, hence its r:0; its own fixtures are 26/26 (`counter/M48-differ-ne0-EQ.txt`).

**Probability:** the forced site is drawn from the 7 summary-function sites (all visible per the
sweep); the other 5 are sampled from the remaining 40 (4 invisible, all non-summary). b2 fails iff
≥ 3 invisible sites are sampled: [C(4,3)·C(36,2) + C(4,4)·C(36,1)] / C(40,5) = 2556/658008 ≈
**0.39 % (1 in 257 nonces)**. The registered counting command draws a random nonce
(`c1-r44-geometry-states-v2.py:410`, `secrets.token_hex(8)`), so a re-run at the data tip
false-misses the landed data with that probability. The v2 counter's own clause b4 is unaffected
(it flips all sites deterministically, no sampling).

**Rule this triggers:** a mutant whose only failing clause is r must be baselined on pristine bytes
under the *same* nonce before being called killed. M48 was so baselined and is reported a survivor.

## F2 — coverage: deleting any single state selftest assertion is undetectable (severity LOW)

**Attacks:** the v2 predicate's teeth granularity (clauses b/b5 vs the selftest's redundancy).
Deleting any ONE of six state-related selftest assertions leaves the selftest green (93/93 or 88/88,
still ≥ 80 for clause b) and the counter TARGET_MET with all clauses 1 (receipts
`counter/M35…M40*.txt`). Clause b5 detects only a selftest whose state teeth are *all* gone; b4
counts non-selftest sites; nothing observes individual assertions. Per deletion, what it uniquely
pins and why the counter still holds:

- M35 `fullscreen-rc` (445): rc 5 for a fullscreen-only dump — also pinned by
  `state-with-tiled-not-compared` (453) and byte-exactly by fixtures fs0/max0. Redundant.
- M36 `fsmode-absent` (472): absent key → 0 — behaviorally pinned by every exact suffix-free summary
  line (e.g. `agree-line` 319). Redundant.
- M37 `fullscreen-not-agree` (447): agree=0 + fullscreen=1 — pinned exactly by `fullscreen-line`
  (444). Redundant.
- M38 `tiled-only-still-ok` (455): the only selftest assertion of the round-43 TILED-only-OK rule;
  the counter does not re-pin it at selftest level, but the mutant changes no behavior, so no clause
  moves. Redundant for these detectors.
- M39 `fullscreen-bool-ignored` (459): True → 0 — also pinned by `fsmode-values` (471). Redundant.
- M40 ignored-mode loop (460-462): 3/2.0/"2"/-1/0/null → non-state; `fsmode-values` (471) covers all
  but "2" and -1, and those two are chain-equivalent to 0 (see M13), so no behavioral hole opens.

This is a property of the predicate, not a defect in the landed tool (its selftest is intact);
reported as a coverage finding, no contract change implied.

## F3 — equivalence survivors; two unit-assertion gaps named (informational)

Equivalence proofs, one line each (single call site `fsmode = client_fsmode(c)` at 235; the chain
consumes fsmode only at 238 `== 2` and 240 `== 1`):

- M03 `f in (0,1,2)`: differs only at f=0, where both return 0 (202 vs the 204 fallback).
- M10 `f in (1,2,"2")`: the added element is unreachable — `isinstance(f, int)` (202) rejects str
  before membership.
- M11: conjuncts reordered; ∧ commutes over pure predicates.
- M12 `f is not True`: differs only at f=False → returns False; `False == 2` and `False == 1` are
  both false — identical to 0 at 238/240. **Gap:** `fsmode-values` (471) omits False.
- M13 `f in (-1,1,2)`: differs only at f=-1 → returns -1; `-1 == 2` and `-1 == 1` both false.
  **Gap:** `fsmode-values` (471) omits -1; the ignored-mode loop (460) tests -1 only through the
  chain, where -1 and 0 are indistinguishable.
- M14 `fsmode >= 2`, M46 `in (2,)`: fsmode ∈ {0,1,2} (client_fsmode 200-205 unmutated), so truth
  sets match at 238.
- M15 `fsmode != 0`, M47 `in (1,)`: reached only after the 238 branch failed → fsmode ∈ {0,1}.
- M21 `and fsmode == 0`: dead conjunct — the branch is reached only when fsmode is already 0.
- M22 `or 0`: `x or 0 ≡ x` for x ∈ {0,1,2}.
- M27: added conjunct always true — maximized/fullscreen tallies increment (248) only after
  `matched` (234), so states > 0 ⇒ matched > 0.
- M28: sum > 0 ⟺ (maximized > 0 or fullscreen > 0) for non-negative ints.
- M29/M44/M45/M48/M49: tallies and size_rules are non-negative ints → `<1 ⟺ ==0`, `!=0 ⟺ >0`.
- M43: dict-literal order; keys are accessed by name.
- M42: docstring text (73); no clause reads it (b4 walks FunctionDef bodies only).

If the L1 wants the "else 0" normalization pinned at unit level, the exact corrected selftest line
(content suggestion, L1 decides) is:

`chk("fsmode-values", [client_fsmode({"fullscreen": v}) for v in (1, 2, 0, 3, True, False, 2.0, "1", -1, None)], [1, 2, 0, 0, 0, 0, 0, 0, 0, 0])`

(computed locator `tools/mado-geometry.py:471`; adding False and -1 kills M12 and M13).

## F4 — counter teeth demonstrated by the two honest kills (informational)

- **M20** `tally[verdict.lower()] += 1` → `= 1` (248): survives selftest because **no selftest case
  asserts any verdict tally ≥ 2** — the multi-client cases assert counts of 1 (449/451/453/464) or
  per-client fields only (`float-rule-reported` 405 asserts `float_rule=` of two AGREE clients, not
  the summary; `other-counted` 381 counts rules, not verdicts). Killed by the counter's fixtures:
  fsclient0, fsmany0, sgen4, sgen8, sgen9 → fixtures=21/26 (`counter/M20-tally-assign1.txt`); clause
  r also fails (r42 fixtures 21/37). The 200-client fsmany0 lattice carries this tooth.
- **M41** `json.loads(...)` → `json.JSONDecoder().decode(...)` (184): behaviorally identical, and it
  defeats clause b5 — the state-blind copy's selftest stays green: "clause=b5 state_blind_selftest
  rc=0 selftest=94/94 failed=0" (`counter/M41-json-decoder.txt`, b5:0 → TARGET_MISSED). This
  demonstrates the *declared* residual "b5 binds the json.loads path only" is reachable with a
  one-line, zero-behavior-change edit; it is a killed mutant here, registered as confirmation of the
  declared residual, not a new hole.

## Restoration evidence

- The lane file was never written: sha256 `1da3ddae…31ff4` before the first probe and after all 49
  (`restored-check.txt`); `git status --porcelain -- tools/mado-geometry.py` → 0 lines.
- All mutants lived in scratch copies (`/fast/scratch/hyaku/mado-r44/MutTool/mutants/`, manifest
  `mutant-manifest.json`); the scratch tree is deleted at the end of this run — no cited path is in
  scratch.
- Restored-bytes detector run after all probes: pristine selftest 94/94 rc 0 (`restored-check.txt`).

## Tooling record

python 3.14.8 (system interpreter, `python3 -I` throughout). No tools installed (none needed);
no pacman transaction; no host-service or compositor mutation (no hyprctl calls at all); git used
read-only only (`rev-parse`-free; `status --porcelain` twice). Scratch dir
`/fast/scratch/hyaku/mado-r44/MutTool` deleted after this report was written.
