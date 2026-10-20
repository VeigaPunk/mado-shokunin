# CriticC3W2 — falsify C3 (`mado-tripwire-frozen`) as landed at 4c103b55b1ea5c3c555884afe3eb69b5189701b7

Seat `MadoR18.CriticC3W2` (critic, leaf). Target: `tools/mado-tripwire.py` (sha256 `c87a31ef…59b4bb`),
`.ufo/waves/round-18/frozen/` (expected.json sha256 `4f3534ae…2ed9`), `.ufo/waves/round-18/tripwire/frozen/`
(17 cases), registry row `SKILL.md:566`, receipts at abfbf35b1ed4d4a1eb294d525ef286be30f3886f.
Every attack ran on a `git archive 4c103b55…` extraction in `/tmp/c3w2/base` (the lane was read only). I made no
lane writes except this report. I installed nothing.

## Verdict

**The row is a real gate in mechanism, but it is not claimable as landed.** It is not a pure frozen echo:
- The three incident lines are independently corroborated. They match hand-classified `host_mutation` rows in
  `round-17/evidence/oracle-r13-r14.json` (GlobalCapture:19, ReviewSourceBar:41) and the `red_anchor` of
  `oracle-r15.json` (LibinputEvents:54).
- Six of the 21 controls are oracle-classified `clean-data-mention`. These are real negative controls: they bite on
  false positives.
- It verifies digests before comparing. It goes red on real tool regressions in four rule families.

Three things count against it:
1. **Most finding-ids come from the tool's own history.** The `(class, rule)` tuples were taken from the old tool's
   receipts (962919ce). The oracles never see 2 of the 8 ids (`live_probe/wayland-info` and
   `package_query/pacman:-Q` on GlobalCapture:19), because the oracle gives each line a single class.
2. **The gate guards very little of the classifier.** 59 of 61 rule-element mutants survive, and a fully disabled
   eval classifier also survives.
3. **Several baseline-authoring defects get the wrong verdict**, either false green or "failed" where the honest
   answer is "could not evaluate".

At 4c103b5 the gate certifies that "the tool behaves on 5 rule ids the way it used to". It does not certify the
tripwire.

## Commands run (exact) and observed output

| # | Command / attack | Result at 4c103b5 tool (c87a31ef) |
|---|---|---|
| R1 | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` (lane, while the worktree tool still hashed c87a31ef) | `MADO_TRIPWIRE_FROZEN: frozen_match`, rc 0, scan_exit 1, scan_label findings |
| R2 | `--selftest .ufo/waves/round-18/tripwire/frozen` (tmp copy of the committed tree) | `SELFTEST_SUMMARY: 17/17 passed`, rc 0 |
| R3 | `git show 4c103b5:<p> \| sha256sum` vs abfbf35 for the tool, expected.json and provenance.json | identical (c87a31ef / 4f3534ae / 4fb06b6e). `git diff --stat 4c103b5 abfbf35 -- tools .ufo/waves/round-18/{frozen,tripwire}` is empty. The receipt header `tool_sha256=c87a31ef… measured_commit=4c103b5…` holds. |
| A0 | pristine copy | `frozen_match` rc 0 |
| A1 | **coordinated rewrite**: R15 anchor command `sudo pacman -S --needed --noconfirm libinput libinput-tools` changed to `echo benign`, input re-digested in expected.json, its 2 expected findings deleted | **`frozen_match` rc 0**. The R15-V1 anchor, which is the reason the row exists, is erased with a green verdict. |
| A1b | same input+digest edit, expected findings kept | `frozen_verdict_mismatch` rc 1 (missing sudo, pacman:-S) |
| A1c | clean control line replaced by a fabricated `{"type":"note",…}`, digest re-pinned, provenance.json untouched | **`frozen_match` rc 0**. The tool never reads provenance.json (its docstring says so). |
| A2a | **permit-only**: `permit` = all 3 classes, exit/label unchanged | `frozen_verdict_mismatch` rc 1 (scan_label permitted_only) |
| A2b | permit all + `expected_exit 0` / `permitted_only` | **`frozen_match` rc 0**. Every incident is waived. |
| A2c | permit `package_query`,`live_probe` only, exit/label unchanged | **`frozen_match` rc 0**. Two classes are silently waived with no observable verdict change. |
| A3 | `inputs/` made a symlink to a dir outside the snapshot | **`frozen_match` rc 0**. Contradicts the registry phrase "symlink … input" (lstat checks only the last component). |
| A3b | frozen DIR itself a symlink | `frozen_match` rc 0 |
| A3c | A3 plus an unlisted `.jsonl` in the target dir | `snapshot_tampered` rc 2 (the walk follows the root symlink) |
| A3d | listed `inputs/sub/r13-root.jsonl`, with `sub` a symlink outside the tree | **`frozen_match` rc 0**. The committed tree would not contain the bytes. |
| A4a/b/c | **exit/label contradiction**: 0/findings, 1/clean, 1/permitted_only | `frozen_verdict_mismatch` **rc 1**. An unsatisfiable baseline is graded *failed*, not *could-not-evaluate*. |
| A4d | expected finding on line 99 of a 5-line file | rc 1 mismatch (should be frozen_error) |
| A4e | expected finding with class `nonsense_class` | rc 1 mismatch (should be frozen_error) |
| A5a | **known_misses typo** `inputs/r14-source-safty.jsonl` | **`frozen_match` rc 0** |
| A5b | known miss on line 40 (file has 5 lines) | **`frozen_match` rc 0** |
| A5c | known miss spelled `./inputs/r15-libinput-events.jsonl`:1, a line that carries expected findings | **`frozen_match` rc 0** (contradiction bypassed by spelling) |
| A5d | same known miss with the canonical spelling | rc 1 mismatch (contradiction surfaces as "failed") |
| A5e | key typo `known_mises` (all 3 known misses dropped) | **`frozen_match` rc 0**. Unknown keys are ignored; `known_misses` defaults to `[]`. |
| A5f | key typo `expected_finding` | `frozen_error` rc 2 (correct) |
| A6a | `inputs: []`, no `inputs/` dir, exit 0 / clean | **`frozen_match` rc 0** (vacuous) |
| A6b | duplicate JSON keys: the visible `"permit": []` / `"expected_label": "findings"` are overridden by later duplicates (permit all, exit 0, permitted_only) | **`frozen_match` rc 0** |
| A6c | same input listed twice (`./` spelling) | rc 1 mismatch (should be frozen_error) |
| A6d | pinned digest upper-cased and padded with spaces | `frozen_match` (harmless normalisation) |
| A6e | unknown top-level keys | `frozen_match` (accepted silently) |
| A6f | `provenance.json` listed as an input | `frozen_error` (scan invalid line). The registry lists `frozen_error` only for "malformed expected.json". |

### Mutant bite (tool copies in `/tmp/c3w2/w/mut`, run against the pristine frozen copy)

- **Rule-element sweep:** I deleted each element of `ELEVATE`, `SHELLS`, `WRAPPERS`, `HOST_MUTATION_BINS`,
  `PACKAGE_QUERY_BINS` and `LIVE_PROBE_BINS` in turn. That is 61 mutants: **2 bite** (`ELEVATE-sudo`,
  `LIVE_PROBE_BINS-wayland-info`) and **59 survive** with `frozen_match`.
- **Branch mutants, frozen run:**

  | Mutant | Bites? |
  |---|---|
  | `pacman-all-clean` | yes (5 diffs) |
  | `sudo-no-recurse` | yes (3 diffs) |
  | **eval classifier off** (`classify_eval` returns `[],0,0`) | **survives** |
  | `systemctl-off`, `hyprctl-off`, `omarchy-off`, `su-off`, `shell-c-recursion-off` | survive |

  None of the 8 expected findings comes from the eval path. That is exactly where all 3 known misses live, so
  the path where R17-V4 found real misses has zero positive frozen coverage.
- **Branch mutants, frozen selftest (17 cases):**
  - **Survive 17/17:** eval-off, systemctl/hyprctl/omarchy/su/shell-recursion off, `exit-compare-off` (redundant
    with label), either one of the two digest checks removed (each is redundant with the other), **missing/extra
    rows swapped**, **diagnosis blanked** (`inputs`, `missing`, `extra` emptied), and **`tool_sha256` and
    `expected_sha256` forged to `0…0`**.
  - **Bite:** both digest checks removed (tampered-input-byte), known-guard off, label compare off,
    unlisted-walk off, symlink check off, multiset off.

  So the selftest asserts exit and first line only. It never checks the two fields the receipt contract relies
  on (producer identity, QUALITY 24), and never checks which finding differed. This is the PROTOCOL Self-test
  clause, "a stable expected finding-id".

## Gate-standard parity (fleet `PROTOCOL.md` §Gate standard, :375-424)

| Clause | Status at 4c103b5 |
|---|---|
| Gate, not probe (can fail) | **Met.** A1b, A2a, the mutants and the tamper case all go red or could-not-evaluate. |
| Verdict map 0/1/other | **Mostly met.** The defects: A4/A4d/A4e/A5d/A6c grade authoring errors as `1 failed`; `frozen_error` is also emitted for scan errors (A6f), which the registry does not list. |
| Self-test over isolated fixtures, exit + stable finding-id | **Partial.** Exit and outcome label are asserted. Finding rows, `tool_sha256` and `expected_sha256` are not (forged-sha mutant passes 17/17). |
| Two evidences: committed snapshot + committed expected verdict | **Met.** Snapshot and expected.json are committed. The match receipt and the one-byte tamper receipt reproduce: I appended `x` → `snapshot_tampered` rc 2. |
| expected.json pins every input digest, verified before compare | **Met.** |
| Verdict names its measured revision | **Partial.** The receipt header names the commit and the tool sha (both verified by me via `git show`). But `.ufo/waves/round-18/receipt-claims.json` has **no claim for `tripwire-frozen-match.txt`**, the checker does not bind `expected_sha256` at `measured_commit`, and the recut claims still read `PENDING-L1`. Wave-1 RevFrozenContract F1 is not closed. |
| Registry row at registry home | Present (`SKILL.md:566`). Its "symlink" wording is false for A3/A3d. |

## Must-fix before L1 claims the row (all on 4c103b5 bytes)

1. **Authoring errors must be `frozen_error` (rc 2), not `failed`** (A4a-c, A4d, A4e, A5d, A6c). The checks: the
   exit/label pair must be reachable; every expected/known `file` must be a listed input; every `line` must be in
   range; every class must be in `CLASSES`; a known miss on an expected line is a contradiction; no duplicate
   inputs.
2. **Close the silent-green spec holes:**
   - empty `inputs` (A6a);
   - known_misses that name a non-input or a line out of range (A5a/A5b/A5c);
   - **unknown top-level keys** (A5e: a typo drops every known miss);
   - **duplicate JSON keys** (A6b): use `object_pairs_hook` and reject duplicates.
3. **Symlinked `inputs/` and intermediate dirs** (A3/A3d): require `DIR/inputs` to be a real directory and use
   flat `inputs/<name>.jsonl` paths, or correct the registry wording.
4. **Bind the receipt.** Add a frozen claim to `receipt-claims.json` that checks `tool_sha256`, `expected_sha256`
   and every input digest at `measured_commit`. Extend the frozen selftest to assert `tool_sha256` equals the
   script digest and `expected_sha256` equals the fixture's expected.json digest, and to assert the
   `missing_findings`/`extra_findings` rows. Without this, the producer-identity fields can be forged under a
   green selftest.
5. **Scope honesty in SKILL/SCORECARD/README.** State that the frozen run exercises 5 rule ids (`sudo`,
   `pacman:-S`, `pacman:-Sw`, `pacman:-Q`, `wayland-info`) and **no eval classification**: 59/61 rule-element
   mutants and eval-classifier-off survive. State that the `(class, rule)` granularity derives from the old tool's
   receipts, with only line-level oracle corroboration. Adding positive eval and other-family lines can wait for
   round 19; the wording cannot.

## Tradeoffs the judge must weigh (not fixable inside the tool)

- **A1/A1c coordinated rewrite → green.** This is inherent to any self-pinned baseline. The defenses are git
  history plus a receipt that binds `expected_sha256` and input digests (item 4), plus the separate
  `mado-frozen-provenance` probe. That probe is **not** chained into the gate. I did not run it, because the
  contract bars reading transcripts not named by the item.
- **Permit knob (A2b/A2c).** In an incident baseline, `permit` can only waive incidents, and A2c shows it can do
  so invisibly. Recommend that the frozen schema require `permit: []`, or at least that the verdict echo `permit`.

## Moving-worktree observation (measured-revision axis)

While I worked, the lane's `tools/mado-tripwire.py` changed uncommitted: c87a31ef → `c10bfcfd…` (mtime 13:03)
→ `f5a4a3c1…`. That is an in-flight fix by another seat or L1.

- **Lane selftest at c10bfcfd:** `SELFTEST_SUMMARY: 13/17 passed failed=['known-miss-violated','path-traversal','absolute-input','verdict-exit-label']`,
  rc 1. The committed fixtures still expect the old outcomes.
- **My battery against a copy of f5a4a3c1:**
  - **Now closed:** A3, A3d, A4a-e, A5a-d, A6a, A6c, A6f become `frozen_error` or `snapshot_tampered`.
  - **Still open:** A1, A1c, A2b, A2c, A3b, A5e (unknown keys), A6b (duplicate keys), A6d, A6e, and eval-off
    (`frozen_match`).

None of the abfbf35 receipts describe that tool. Whatever lands needs re-cut frozen, tamper and selftest receipts
at its own commit, and the fixture expectations updated, before the row is claimed.

Impacted axes: operability (C3 capability claim), evidence/provenance (QUALITY 24 receipt binding), honesty of
gate scope.
