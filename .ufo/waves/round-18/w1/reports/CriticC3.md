# CriticC3 — attack on C3 (tripwire `--frozen` replay, probe → gate)

Seat: MadoR18.CriticC3 (critic, read-only). Inputs read: `PROTOCOL.md` §Gate standard (fleet root :375-424), `SKILL.md:525-590`, `SCORECARD.md` "Round 18 — declared claims", working-tree `tools/mado-tripwire.py` (sha256 `593b3aaf…46f`, the TwFrozenMode edit; HEAD/d9a5a18 is `962919ce…072`), suite `.ufo/waves/round-18/tripwire/frozen` (17 cases), round-17 evidence (`tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt`, `tripwire-vs-oracles.json`, `oracle-r13-r14.json`, `oracle-r15.json`, `session-index.json`), `w2/reports/RevengeUnparsed.md`, `corpus/lessons/round-17-verifier-spotcheck.md` R17-V4, `drafts/SkillRegistryDraft.md`, and the dispatch text for TwFrozenSnapshot/TwFrozenMode/TwFrozenSelftest/TwMissHelperFn.

I did not open any transcript. The frozen snapshot (`frozen-tripwire/`) did not exist yet when I read the tree, so findings about its expectations come from its dispatch spec and the receipts it is told to use. I ran no lane gate. My only executions were the tool and four mutants of it, all run from `/tmp/criticc3-*` against copies of the committed synthetic fixtures. The lab has been removed; the recipes are below.

## Verdict on the question

The frozen replay satisfies the *mechanics* of the PROTOCOL Two-evidences clause:
- every input is digest-pinned;
- an edited input gives `snapshot_tampered` (exit 2);
- a digest-less entry gives `unpinned_legacy`.

These are the items R17-V4 said were missing, and the 17/17 suite confirms them.

The replay does **not** turn the scan's verdict into a checked one. What it freezes is the classifier's output on a curated sample: it detects *changes* in the classifier, not whether a classification is correct. Its expected values are only partly independent of the tool:
- **Line+class level.** The host_mutation lines are backed by two sources the tool did not produce: the manual oracles and `/var/log/pacman.log`.
- **Rule level.** Every `rule` id, and every per-call split (e.g. `sudo` + `pacman:-S`), exists only in the tool's own receipts. Those receipts came from the f71ccbe-era tool (`7a98720e…`). They carry no tool sha (`grep -c tool_sha256` = 0 in all five files) and were not re-cut in 0ab1ccc.

So the move to `gate` is defensible only for the `--frozen` entry, read as "regression lock", and only after the must-fix items below. Otherwise it repeats R17-V1: an unbound tool revision behind a verdict.

## Counterexamples (strongest first)

### X1 — An unbound frozen verdict repeats R17-V1 (must-fix; calibration, operability)
- **Evidence.**
  - The output's `tool_sha256` is printed but not pinned. `SkillRegistryDraft` says so itself: "the pin binds inputs, not the tool digest".
  - The verdict JSON has no `measured_commit`.
  - PROTOCOL: "A verdict names the revision it was measured against."
  - At my read, the working-tree tool (`593b3aaf…`) differs from HEAD (`962919ce…`). Any receipt taken before the commit lands would therefore name a tool git never recorded, which is exactly R17-V1/V2.
- **Smallest correction.** L1 commits the frozen-run receipt (match + tampered copy) *after* the integration commit, with a first line `RECEIPT tool_sha256=… measured_commit=…`. Add it to `receipt-claims.json` so `mado-receipt-check` checks it against `git show REV:tools/mado-tripwire.py`, with PIPESTATUS captured (the F10 lesson).

### X2 — Expectations are self-derived at rule granularity (fixable; calibration)
- **Evidence.** In `tripwire-vs-oracles.json`, r13 `tripwire_only` contains `GlobalCapture:19 live_probe` and `GlobalCapture:19 package_query`; the oracle classes that call only as `host_mutation`. For one call on line 65 (the `hyprctl -j version` call, which also contains `pacman -Q`), `oracle-r13-r14.json` records a single class, `package_query`, where the tool reports two findings. The oracle assigns one class per call, so it cannot back multi-class findings.
- **Count.** Across the four incident records the receipts give 15 expected findings: GlobalCapture:19 = 4, ReviewSourceBar:41 = 2, OutputSpec:65 = 7, LibinputEvents:54 = 2.
  - All four lines have independent backing at `(line, host_mutation)` level: the oracle plus `pacman.log` :2410/:2422/:2423/:2429.
  - 2 of the 15 have no independent backing at any level.
  - For all 15, the `rule` value is tool vocabulary.
- **Shared blind spot.** `oracle_only` is empty in every round. The oracles also missed all three known misses, because the oracle scanned eval cells only when they start with `!`, and the misses are python `subprocess` cells. The oracle is a separate producer, but its failure modes overlap the tool's.
- **Smallest correction.** Give each `expected_findings` entry a `basis` value: `oracle+pacmanlog` | `oracle` | `revenge-unparsed` | `tool-receipt-f71ccbe`. Report the independent fraction in the round lesson, and in the registry row state "change-detector, not accuracy".

### X3 — A coordinated rewrite passes the gate (tradeoff the judge must accept knowingly; operability)
- **Lab results** (copies of the committed `match-findings` fixture):

| case | change | result |
|---|---|---|
| T1 | `sudo pacman -Syu` → `echo hello world`, digest re-pinned, `expected_findings: []`, exit 0, label `clean` | `frozen_match` rc 0 |
| T2 | same bytes, `permit: [all three classes]`, label `permitted_only`, exit 0 | `frozen_match` rc 0 (the incident now reads exit 0) |

  Both the digests and the expectations live in the same `expected.json`. The only external anchors are git history, `provenance.json` → round-17 `session-index.json` (committed fc6f960), and the `mado-frozen-provenance` probe. That probe reads live transcripts, which are mutable and may be rotated; if they are rotated it exits 2 permanently and the snapshot becomes the only copy.
- **Smallest correction.**
  - Require `permit == []` in this baseline, or reject a non-empty permit as `frozen_error`.
  - Add an `anchors` list: the 4 pacman.log transaction joins with `pacman.log:N` citations, which `--frozen` requires to be a subset of `expected_findings` (`frozen_error` otherwise). A re-pin cannot then drop the incident silently; doing so must delete a cited anchor, which shows in the diff.
  - Say in the lesson that this residual is append-only/git-review-only.

### X4 — The `MadoR13.jsonl:470` known miss is vacuous in a line snapshot (must-fix; false provenance)
- **Evidence.** `RevengeUnparsed.md` H2: `run_record` is "`def`ined at transcript line **437**". The invocation cell at 470 "contains **no spawn AST node**". Snapshotting 470 without 437 makes "no finding on 470" true by construction, for every future tool. The assertion can never fail.
- **Related scope gap.** TwMissHelperFn is scoped to "a shell function defined in the same command text". H2 is a *python* helper defined in *another cell*, so that rule cannot fix this real miss either.
- **Smallest correction.** Either snapshot line 437 together with 470 (provenance pairs for both), or drop 470 from `known_misses` and record it as "not representable in a line-local snapshot". Tell TwMissHelperFn/L1 that its draft rule does not cover H2.

### X5 — Known-miss and expectation authoring errors grade as tool failure, not could-not-evaluate (fixable; operability)
- **Evidence.** The suite case `known-miss-violated` lists line 1 in *both* `expected_findings` and `known_misses` ("deliberately wrong"). It passes as `frozen_verdict_mismatch` exit 1, so a self-contradictory `expected.json` is pinned as a *failed* verdict.
- **Lab results:**
  - **T4** (`expected_exit: 0` with `expected_label: findings`, an unsatisfiable baseline): `frozen_verdict_mismatch` rc 1, `missing=[] extra=[]`.
  - **T3** (`known_misses` naming `inputs/MadoR13.jsonl:470`, a file not listed in inputs, and `incident.jsonl:9999`): `frozen_match` rc 0. Neither file nor line is validated, so a typo silently disables the assertion.
  - **Mutant M1** (known-miss loop deleted) is caught only by that contradiction fixture. Without the contradiction, `known_misses` adds nothing beyond the multiset check, because a finding on an unexpected line is already `extra`.
- **Smallest correction.** In `validate_frozen`, return `frozen_error` (exit 2) when:
  - a known-miss `(file, line)` also appears in `expected_findings`;
  - a known-miss or expected file is not a listed input;
  - a line is past the end of its file;
  - the exit/label pair is inconsistent (`clean`/`permitted_only` ⇔ 0, `findings` ⇔ 1).

  Then re-point the `known-miss-violated` fixture to a consistent baseline in which a finding lands on a known-miss line that is *not* in `expected_findings`, and accept that this case reads as `extra`.

### X6 — The frozen selftest asserts no finding-level detail (fixable; operability, PROTOCOL Self-test)
- **Mutant lab** (copies of the working-tree tool, run with `--selftest .ufo/waves/round-18/tripwire/frozen`):

| mutant | change | suite result |
|---|---|---|
| M1 | known-miss check deleted | 16/17, killed |
| M2 | `missing`/`extra` swapped | 17/17, survives |
| M3 | `rule` dropped from the comparison key | 17/17, survives |
| M4 | label ignored | 17/17, survives (mostly redundant with exit+findings) |

- **Cause.** Frozen-mode cases compare only the exit and the first line (`want_findings is ignored in this mode`, tool :1075). PROTOCOL Self-test asks for "a stable expected finding-id"; the outcome token qualifies, but the mismatch detail is unverified.
- **Smallest correction.** Let frozen cases carry `want_missing`/`want_extra` (multisets) compared against the verdict JSON. Add one fixture with the same class and a different rule (kills M3).

### X7 — The comparison key drops `tool_call_id` (fixable; operability)
- **Evidence.** `tripwire-r14.txt` gives `MadoR14.OutputSpec.jsonl:65` (one record carrying many calls, per the pacman-log join note) two `(package_query, pacman:-Q)` findings from different calls (`3_tool_f7209523…` and `0_tool_3128c103…`). The key `(file, line, class, rule)` collapses them to multiplicity 2. A regression that loses one call's finding while gaining a false one elsewhere on the same record is invisible. Every receipt finding already carries `tool_call_id`.
- **Smallest correction.** Add `tool_call_id` to `expected_findings` and to the key. It is already present in the receipts, so the cost is nil.

### X8 — Controls chosen by tool silence test nothing independent (fixable; operability)
- **Evidence.** The spec says "up to 4 clean assistant toolCall control lines" per file. Lines with no tool finding are clean only by the tool's own judgement. The oracles hold independent `clean-data-mention` labels: tokens as data, the false-positive surface. In `oracle-r13-r14.json`, GlobalCapture:65 call `call_c9814d3b…` is one; `oracle-r16.json` has 74 clean labels.
- **Smallest correction.** Draw the controls from oracle `clean`/`clean-data-mention` rows, with `basis: oracle` per line.

### X9 — Snapshot root does not resolve under PROTOCOL's frozen roots (must-fix, cheap; conformance)
- **Evidence.** PROTOCOL: "Frozen baseline names resolve under any `.ufo/waves/*/frozen` root". The planned root `.ufo/waves/round-18/frozen-tripwire` is not such a root. The lane precedents are `round-13/frozen`, `round-14/frozen` and `round-16/frozen`.
- **Smallest correction.** Use `.ufo/waves/round-18/frozen/` (round-18 has no other frozen root) or `.ufo/waves/round-18/frozen/tripwire/`, and update the registry entry.

### X10 — A symlinked `inputs/` or DIR escapes the leaf-only symlink check (low; operability)
- **Lab results:**
  - **T5:** `DIR/inputs` as a symlink to an outside directory holding identical bytes gives `frozen_match` rc 0.
  - **T6:** DIR itself a symlink gives `frozen_match`.
- **Cause.** `os.lstat` checks only the last path component (tool :938-941). A committed `inputs ->` symlink into `~/.omp` would replay "live" bytes and break on a fresh clone.
- **Smallest correction.** Require `os.path.realpath(join(DIR, path))` to stay under `realpath(DIR)`, and refuse when `inputs` is a symlink.

## Impacted axes

| axis | items |
|---|---|
| operability | C3 claim: X1, X3, X5–X8, X10 |
| calibration | X1, X2, X4: label honesty, a repeat of R17-V1 |
| conformance (PROTOCOL Two evidences / Registry) | X1, X9 |

No coverage impact.

## Must-fix before `probe → gate`

X1 (committed receipt binding the tool sha and measured commit), X4 (vacuous 470 assertion), X9 (frozen root path). The remaining items are fixable defects. X3 is a residual the judge must accept by name.

## Lab recipe (reproducible)

1. Copy `tools/mado-tripwire.py` to /tmp and apply the mutants:
   - M1: delete the `for miss in pinned["known"]` loop;
   - M2: swap `expected - got` and `got - expected`;
   - M3: key without `rule`;
   - M4: mismatch without the label term.
2. Run `python3 -I <copy> --selftest .ufo/waves/round-18/tripwire/frozen`.
3. For T1–T6, copy `.ufo/waves/round-18/tripwire/frozen/match-findings`, apply the stated edit, re-pin `inputs[0].sha256` with `hashlib.sha256`, and run `--frozen` with the working-tree tool.

## Tooling

No installs or updates.
