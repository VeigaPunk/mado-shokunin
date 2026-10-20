# W3CriticC3Final — re-run of the CriticC3W2 battery against `--frozen` at a210241

Seat `MadoR18.W3CriticC3Final` (critic, leaf).

**Target**
- Commit `a210241b5429fb3c3f9ad23f42863d6e6d9e5845` (master).
- `tools/mado-tripwire.py` sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`, unchanged since `be886a3`: `git diff --stat be886a3 a210241 -- tools .ufo/waves/round-18/frozen .ufo/waves/round-18/tripwire` is empty.
- `frozen/expected.json` sha256 `4f3534ae…2ed9`.

**Method**
- Work tree: `git clone /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/c3w3/base && git checkout a210241…`.
- Every attack ran on a copy of `.ufo/waves/round-18/frozen` under `/tmp/c3w3/w/<case>`, using `python3 -I /tmp/c3w3/base/tools/mado-tripwire.py --frozen <copy>` (cwd = clone).
- Mutants are tool copies under `/tmp/c3w3/w/mut/`.

**What I did not do**
- No lane write except this report.
- No git/jj write, no jj command, no package/host/service command.
- Nothing installed.
- I did not run `mado-frozen-provenance`, because it reads live host transcripts.

## Verdict

The w2 must-fix items 1-3 are closed at the final commit:
- authoring errors now give `frozen_error`;
- empty inputs, unknown keys and duplicate keys are refused;
- known-miss typos, out-of-range and blank lines are refused;
- a symlinked `inputs/` and a symlinked frozen dir are refused.

Still green (`frozen_match`):
- the inherent coordinated rewrite (A1, A1c);
- the by-design permit waivers (A2b, A2c);
- the whole eval path switched off;
- three new holes, N1-N3 below.

**The SCORECARD C3 wording is honest but incomplete. The SKILL registry row is stale and partly false at a210241.**
- The row still says "17 mode-frozen cases"; the suite and the SCORECARD say 31.
- Its verdict map omits the new `frozen_error` and `snapshot_tampered` triggers.
- It states no scope bound (5 rule ids, zero eval coverage).

The row was not edited after `4c103b5`: `git diff 4c103b5 a210241 -- SKILL.md` adds only the walker erratum.

## Battery: w2 attacks re-run (4c103b5 result from CriticC3W2.md → a210241 result observed)

Each cell shows outcome / rc and, where useful, the tool's `error` string.

| # | Attack | at 4c103b5 (w2) | at a210241 (this run) | status |
|---|---|---|---|---|
| A0 | pristine copy | match/0 | `frozen_match`/0, scan_label findings | — |
| A1 | **coordinated rewrite**: R15 anchor `sudo pacman -S --needed --noconfirm libinput libinput-tools` → `echo benign`, digest re-pinned, its 2 findings deleted | match/0 | **`frozen_match`/0** | still open (inherent) |
| A1b | same input+digest edit, findings kept | mismatch/1 | `frozen_verdict_mismatch`/1, missing 2 | red (correct) |
| A1c | r14-source-safety line 1 → fabricated `{"type":"note",…}`, re-pinned, provenance.json untouched | match/0 | **`frozen_match`/0** | still open (inherent; the tool never reads provenance.json) |
| A2a | permit all 3 classes, exit/label unchanged | mismatch/1 | `frozen_error`/2 "findings baseline lists no class outside permit" | now could-not-evaluate |
| A2b | **permit-only**: permit all 3 + `expected_exit 0`/`permitted_only` | match/0 | **`frozen_match`/0**, scan_label permitted_only | still open (every incident waived) |
| A2c | permit `package_query`,`live_probe`, exit/label unchanged | match/0 | **`frozen_match`/0** | still open; fixture `match-permit-partial` expects this |
| A3 | `inputs/` → symlink to a dir outside the snapshot | match/0 | `snapshot_tampered`/2 | closed |
| A3b | frozen DIR itself a symlink (`DIR`, `DIR/`) | match/0 | `snapshot_tampered`/2 "frozen directory is a symlink" | closed for these spellings (see N1) |
| A3c | A3 + unlisted `.jsonl` in the target | tampered/2 | `snapshot_tampered`/2 | unchanged |
| A3d | `inputs/sub/r13-root.jsonl`, `sub` a symlink outside | match/0 | `frozen_error`/2 "input path is not inputs/<name>.jsonl" | closed |
| A4a/b/c | exit/label 0/findings, 1/clean, 1/permitted_only | mismatch/1 | `frozen_error`/2 "unreachable exit/label pair" (×3) | closed |
| A4d | expected finding on line 99 | mismatch/1 | `frozen_error`/2 "past the end" | closed |
| A4e | expected class `nonsense_class` | mismatch/1 | `frozen_error`/2 "unknown class" | closed |
| A5a | known_misses file typo `r14-source-safty` | match/0 | `frozen_error`/2 "names an unlisted input" | closed |
| A5b | known miss line 40 (out of range) | match/0 | `frozen_error`/2 "past the end" | closed |
| A5c | known miss `./inputs/r15-…:1` (an expected line) | match/0 | `frozen_error`/2 "overlaps expected_findings" | closed |
| A5d | same, canonical spelling | mismatch/1 | `frozen_error`/2 "overlaps" | closed |
| A5e | key typo `known_mises` | match/0 | `frozen_error`/2 "unknown expected.json key(s)" | closed |
| A5f | key typo `expected_finding` | error/2 | `frozen_error`/2 | unchanged |
| A6a | `inputs: []`, no inputs dir, 0/clean | match/0 | `frozen_error`/2 "inputs is not a non-empty list" | closed |
| A6b | duplicate top-level keys override permit/exit/label | match/0 | `frozen_error`/2 "expected.json not JSON (ValueError)" | closed |
| A6c | same input listed twice (`./` spelling) | mismatch/1 | `frozen_error`/2 "input path is not inputs/<name>.jsonl" | closed |
| A6d | digest upper-cased + space-padded | match/0 | `frozen_match`/0 | harmless normalisation |
| A6e | unknown top-level keys | match/0 | `frozen_error`/2 | closed |
| A6f | `provenance.json` listed as an input | error/2 | `frozen_error`/2 (path rule) | unchanged |
| known-blank | known miss on a genuinely blank line (re-pinned file with `\n\n` appended) | — | `frozen_error`/2 "is blank" | closed |
| eval-off | `classify_eval` returns `[],0,0` | match | **`frozen_match`/0** | still open |

### New attacks (not in w2)

| # | Attack | Result | Note |
|---|---|---|---|
| **N1** | symlinked frozen dir passed as `DIR/.` or `DIR/inputs/..` | **`frozen_match`/0** (both) | `run_frozen` does `os.path.islink(directory.rstrip("/"))`, which is a spelling check. Fix: `os.path.islink(os.path.normpath(os.path.abspath(directory)))`. Low severity: the registered command uses the literal path, and `git ls-tree` shows that path is a tree with mode-100644 blobs, not a symlink. |
| N1b | ancestor dir symlinked (`LINK/frozen`) | `frozen_match`/0 | Acceptable. This is a host-layout fact, not a snapshot fact. |
| **N2** | `known_misses: []`, or the key removed | **`frozen_match`/0** (both) | The 3 "pinned" known misses carry no verdict weight. Any finding on any line outside `expected_findings` is already `extra`, so `known_misses` only adds validation. Shown by fixture `known-miss-violated` (want_extra 1). |
| N2b | fabricated known miss added on a clean control line (r14-source-safety:1) | **`frozen_match`/0** | The tool accepts a false "known miss" claim. |
| **N3** | unknown keys inside entries (`inputs[0].note`, `expected_findings[0].why`, `known_misses[0].nott`) | **`frozen_match`/0** | The top-level unknown-key rule does not extend to nested objects. Material only for a typo like `nott` (note dropped). |
| N3b | nested duplicate key (`"line": 1, "line": 1`) | `frozen_error`/2 | The hook applies at every level. Correct. |
| N4 | expected finding `rule: "no-such-rule"` | `frozen_verdict_mismatch`/1 (missing 1, extra 1) | Rule names are not validated, so an authoring error is graded *failed*. Residual of w2 must-fix 1. |
| N4b | expected finding on a blank line (re-pinned) | `frozen_verdict_mismatch`/1 (missing 1) | The blank-line check covers known_misses only. Same residual. |
| N5 | `expected_exit` `1.0` / `true` | `frozen_error`/2 "bad expected_exit" | Correct. |

## Mutant bite at a210241 (pristine frozen copy)

**Branch mutants, frozen run:**
- Survive with `frozen_match`: `eval-off`, `bang-off` (`!cmd` lines), `percent-bash-off` (`%%bash`), `tool-bash-off`, `systemctl-off`, `hyprctl-off`, `omarchy-off`, `su-off`, `shell-c-off`.
- Bite: `sudo-no-recurse` (mismatch, missing 3) and `pacman-all-clean` (mismatch, missing 4).

**Rule-element sweep:** I deleted each element of `ELEVATE`, `SHELLS`, `WRAPPERS`, `HOST_MUTATION_BINS`, `PACKAGE_QUERY_BINS` and `LIVE_PROBE_BINS` in turn. That is 61 mutants: **2 bite** (`ELEVATE-sudo`, `LIVE_PROBE_BINS-wayland-info`) and **59 survive**. This is identical to w2.

**Frozen selftest** (`--selftest .ufo/waves/round-18/tripwire/frozen`):
- Pristine: `SELFTEST_SUMMARY: 31/31`.
- These all still pass **31/31**: `forged-shas` (`tool_sha256` and `expected_sha256` emitted as `0…0`), `inputs-report-blank`, `rows-content-forged` (missing/extra rows replaced by junk of the same count), `eval-off`, `omarchy-off`.
- The suite now asserts outcome, exit and the missing/extra *counts*, so w2's swapped-rows and blanked-diagnosis mutants are dead. It still asserts neither producer identity nor finding identity.

**Where the eval path is actually guarded:** the four round-17 scan suites catch `eval-off`:
- core 8/9;
- compound 14/16;
- hardening 27/33;
- w2-regressions 27/30.

The gate's self-test cell lists those suites, so the classifier is covered by the probe suites, **not by the frozen gate**.

## Receipts (QUALITY 24 binding), checked by hand

`evidence/final/tripwire-frozen-{match,tampered,selftest}.txt` all hold:
- header `measured_commit=be886a3`, which is an ancestor of a210241;
- header `tool_sha256` equals `sha256(git show be886a3:tools/mado-tripwire.py)`, which equals the a210241 tool;
- for match and tampered: payload `tool_sha256` equals the header, payload `expected_sha256` equals `sha256(git show be886a3:…/expected.json)`, and every pinned input digest equals its `git show` bytes.

The redbefore receipt reads `SELFTEST_SUMMARY: 17/31 passed`, with 14 named failures. That matches the SCORECARD's "the abfbf35 tool 17/31".

`python3 -I .ufo/waves/round-18/receipt-check.py` → `EXPECT_SUMMARY: 21/21`. However, its three frozen claims (`r18-tripwire-frozen-{match,tampered,before}`) bind the **abfbf35-era** receipts in `evidence/` (tool `c87a31ef`). No claim covers the `evidence/final/` receipts that SCORECARD C3 cites. The binding holds today only because I checked it by hand.

## Wording judgement

**SCORECARD C3** (SCORECARD.md:998) — *honest, incomplete.*
- These facts reproduced:
  - `frozen_match` exit 0;
  - one-byte tamper gives `snapshot_tampered` exit 2;
  - frozen suite 31/31, with 17/31 at abfbf35;
  - "change-detector over 5 pinned incident files (8 findings, 3 known misses), not classifier correctness, prevention or R15-V1 remediation".
- "not classifier correctness" is true and is the right disclaimer.
- Omitted:
  - the detector watches **5 rule ids** (`sudo`, `pacman:-S`, `pacman:-Sw`, `pacman:-Q`, `wayland-info`), plus no-finding on the control lines;
  - it has **zero eval-path positives** (eval/`!`/`%%bash`/`tool.bash` off all stay green);
  - the "3 known misses" are annotations with no verdict effect (N2).
- The capabilities-table row (:1020) is accurate.

**SKILL.md:566 `mado-tripwire-frozen`** — *not honest as landed at a210241:*
1. **False:** "(17 mode-frozen cases; exit and first-line outcome)". The committed suite has 31 cases and asserts outcome, exit and missing/extra counts. SCORECARD:998/1006 say 31/31.
2. **Stale verdict map:**
   - `frozen_error` is described as "malformed expected.json" only. It now also fires on unknown/duplicate keys, unreachable or contradictory pins, known-miss overlap or blank lines, and scan errors.
   - A symlinked frozen dir gives `snapshot_tampered`; the row says "symlink … input" only.
   - "or a `known_misses` line differs" implies the known misses are enforced. Removing them is green (N2).
3. **Pinned-value cell:** "pins … 3 known misses" is true in bytes but non-binding.
4. **No scope bound:** w2 must-fix 5 (5 rule ids, no eval classification) was not carried into the row, the frozen README, or an erratum.

## Smallest safe corrections

1. **SKILL (append-only erratum to the row):**
   - self-test is 31 cases asserting exit, first line, JSON outcome/exit and missing/extra counts, not producer shas or finding identity;
   - `frozen_error` also covers the schema/reachability refusals;
   - a symlinked frozen dir gives `snapshot_tampered`;
   - scope: 5 rule ids, no eval-path positive (eval is guarded by the scan suites only);
   - `known_misses` are annotations.
2. **SCORECARD C3:** append "5 rule ids; no eval-path positive (eval-off: frozen green, scan suites red); known misses non-binding".
3. **Tool (round 19):**
   - `islink(normpath(abspath(DIR)))` (N1);
   - reject unknown keys in nested entries (N3);
   - a blank-line check for `expected_findings` and a validated rule vocabulary (N4/N4b);
   - echo `permit` in the verdict payload, or require `permit: []` for incident baselines (A2b/A2c).
4. **Selftest:** assert payload `tool_sha256 == SELFTEST_SCRIPT_SHA256` and `expected_sha256 == sha256(case expected.json)`, and assert the identity of the missing/extra rows, not just their count. The `forged-shas` and `rows-content-forged` mutants must go red.
5. **receipt-claims.json:** add claims for `evidence/final/tripwire-frozen-{match,tampered,selftest}.txt` at `be886a3`.

## Tradeoffs for the judge (not fixable in the tool)

- **A1/A1c coordinated rewrite gives green.** Any self-pinned baseline has this property. The defence is git history plus `mado-frozen-provenance`, which is not chained into the gate and was not run here.
- **Permit waivers (A2b/A2c).** The fixture `match-permit-partial` shows this behaviour is designed. In an incident baseline it can only waive incidents, and the verdict does not echo `permit` (payload keys: `exit, expected_sha256, extra_findings, inputs, missing_findings, outcome, scan_exit, scan_label, schema, tool_sha256`).

Impacted axes:
- operability: C3 scope honesty;
- evidence/provenance: final receipts not under receipt-check;
- registry honesty: SKILL row stale or false.

No axis is harmed by the landed tool change. It moved 18 w2 cases from match or mismatch to could-not-evaluate (A2a, A3, A3b, A3d, A4a-e, A5a-e, A6a, A6b, A6c, A6e) and opened none: N1-N3 were already green at 4c103b5.
