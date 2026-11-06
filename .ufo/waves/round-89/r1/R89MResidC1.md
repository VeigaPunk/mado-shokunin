# R89MResidC1 — reproduce and attack C1 on measured bytes

Verdict: **C1 VERIFIES.** Pins hold, the frozen command reproduces the receipt byte-for-byte, and 26
independently re-derived expectations (oracle + upstream criteria.c reading) agree with the case set.

## 1. Pins (step 1)

Scratch `S=/fast/scratch/hyaku/mado-r89/R89MResidC1`; every lane byte read via
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show <rev>:<path>`. All **17/17 PASS**:

| object | rev | sha256 (first 8) | expected | ok |
|---|---|---|---|---|
| quality/counters/c1-r89-mako-regex.py | F | 5b977141 | 5b977141 | PASS |
| quality/counters/c2-r89-survivor-kills.py | F | 73bd5201 | 73bd5201 | PASS |
| quality/counters/c1-r88-mako-fields.py | F | 3678425a | 3678425a | PASS |
| quality/counters/c2-r88-include-containment.py | F | f8e18b7c | f8e18b7c | PASS |
| controls/mako-cases-r89.json | F | 5fdca7db | 5fdca7db | PASS |
| controls/mako-mutants-r89.json | F | 5471bee2 | 5471bee2 | PASS |
| round-88/controls/mako-cases-r88.json | F | a0e81b19 | a0e81b19 | PASS |
| controls/survivor-mutants-r89.json | F | 9f25df3c | 9f25df3c | PASS |
| controls/survivor-cases-c1side-r89.json | F | c710a3e5 | c710a3e5 | PASS |
| controls/survivor-cases-c2side-r89.json | F | e02e2b4d | e02e2b4d | PASS |
| controls/mako-cases-r89-blind.json | F | a4fa66cf | a4fa66cf | PASS |
| controls/posix-ere-oracle.c | F | 42270192 | 42270192 | PASS |
| controls/gen-c1-cases-r89.py | F | 6cb73101 | 6cb73101 | PASS |
| build/mado-mako.c1.py | F | 6b4bc409 | 6b4bc409 | PASS |
| tools/mado-mako.py | F | c374d715 (=base tool) | c374d715 | PASS |
| **tools/mado-mako.py** | **A** | 6b4bc409 | 6b4bc409 | PASS |
| tools/mado-mako.py | base af998dcc | c374d715 | c374d715 | PASS |

Pairwise: `A:tools/mado-mako.py` is byte-identical to `F:.ufo/waves/round-89/build/mado-mako.c1.py`
(True), and `git rev-parse A^` = F. Freeze F = d8736135, C1 rev A = 099c662d, base = af998dcc.

## 2. Reproduction (step 2)

Ran the declaration's exact C1 argv with the seat's scratch: `python3 -I counter.py --repo <lane>
--rev 099c662d… --base-rev af998dcc… --cases $S/cases-r89.json` (extracted from F via `git show`,
sha-checked by the counter's own `--expect-cases-sha256` pin) `--expect-mutants-sha256 5471bee2…
--expect-r88-cases-sha256 a0e81b19… --scratch-root $S/run1` under `TMPDIR=$S`.

- **rc = 0**, stderr empty, 466 output lines.
- `diff` of receipt body (receipt minus its command-echo and `rc=` lines) vs my stdout: **empty —
  byte-identical**, all 466 lines (4 header, 141 case, 141 base-tool control, 141 python-re control,
  controls line, 37 mutant lines, final line).
- Final line equals the receipt's and the declaration's after-state: `MADO_MAKO_REGEX: TARGET_MET
  rev=099c662d… cases=141 correct=141 carried=61/61 mutants=37 killed=37 naive_correct=34
  globals_include_correct=35 base_tool_correct=78 python_re_correct=127 score=10.0000 …
  tool_sha256=6b4bc409… cases_sha256=5fdca7db…`; receipt records `rc=0`, mine was 0.
- The counter left `$S/run1` empty (its own cleanup claim exercised at runtime).

Two earlier runs of mine failed before any measurement (my extraction errors, not lane defects):
the r89 counter loads `c1-r88-mako-fields.py` from its own directory, and r88 loads
`c1-r87-mako-criteria.py` (`FileNotFoundError`, rc 1, empty stdout). After extracting both at F the
run reproduced. Chain note: the transitive pins hold — r89 pins r88 = 3678425a, r88 pins
r87 = 4d801c30 (extracted bytes matched), r87 loads nothing further. The r88 counter's only
subprocess git mutations are inside its selftest fixture (`user.name=mado-selftest`), not the lane.

## 3. Re-derived expectations (step 3)

Oracle built from the F bytes: `cc -O0 -o $S/ore controls/posix-ere-oracle.c` (regcomp
REG_EXTENDED|REG_NOSUB + regexec, no setlocale → C locale). My parse_criteria reading is from
upstream v1.11.0 criteria.c fetched from github raw (criteria.c:46-59 match_regex_criteria,
115-132 match_criteria strcmp/regex arms, 162-262 parse_criteria, 274-351 apply_criteria_field,
542-551 "Cannot set both"; include/enum.h:7-10 NORMAL=0 ESCAPE=1 QUOTE=2 QUOTE_ESCAPE=3 —
QUOTE_ESCAPE = QUOTE|ESCAPE, so `state &= ~ESCAPE` returns to QUOTE and the end-of-string checks at
criteria.c:228-241 fire on the right state). **26 cases re-derived, 0 disagreements** (need ≥15:
10 b, 11 r/n, 5 carried).

Oracle-run (pattern = post-tokenizer value; text = notification input) — every result equals the
case's expectation:

| case | pattern | text | oracle | expect | agree |
|---|---|---|---|---|---|
| r02 | `Wi-Fi` | `Setup Wi-Fi` | match | section applies | ✓ |
| r03 | `hel+o` | `say helllo` | match | applies | ✓ |
| r05 | `^[[:digit:]]+$` | `2026` | match | applies | ✓ |
| r06 | `\d` (config `\\d`, one backslash survives) | `d` | match (glibc: literal d) | applies | ✓ |
| r08 | `^.$` | `é` | nomatch (C locale, 2 bytes) | section not applied | ✓ |
| r14 | `1.0` (in quotes: QUOTE_ESCAPE drops `\`) | `1x0` | match | applies | ✓ |
| r23 | `` (empty value compiles) | `anything` | match | applies | ✓ |
| r31 | `1.0` (unquoted ESCAPE drops `\`) | `1x0` | match | applies | ✓ |
| r32 | `a(b` (first occurrence) | `x` | invalid | refused | ✓ |
| n04 | `a.b` | `a\nb` | match (no REG_NEWLINE) | applies | ✓ |
| b01 | `[b-d]` | `c` | match | applies | ✓ |
| b05 | `(ab)+` | `abab` | match | applies | ✓ |
| b07 | `\1` (config `\\1`) | `a` | invalid (backref w/o group) | refused | ✓ |
| b13 | `(x)` (config `\(x\)`) | `x` | match | applies | ✓ |
| b20 | `a.b` (config `a\.b`) | `axb` | match | applies | ✓ |
| b36 | `a)` | `a)` | match (literal `)`) | applies | ✓ |
| b38 | `[^[:digit:]]` | `a` | match | applies | ✓ |
| b44 | `gamma` vs body input `delta` (not summary) | `delta` | nomatch | not applied, no refusal | ✓ |

Derived from parse/apply semantics alone (no oracle needed): c15 `app-name="Google Chrome"` →
QUOTE keeps the space → token `app-name=Google Chrome`, strcmp match → applies ✓; c16
`app-name=Google\ Chrome` → ESCAPE drops `\`, keeps space → match → applies ✓; c22
`summary=hello summary~=hello` → criteria.c:542-546 refuses both-set → refusal ✓; c29
`app-name="alpha` → ends in QUOTE(2) → "Unmatched quote" (criteria.c:235-238) → refusal ✓; n07
`summary~="abc\` → ends QUOTE_ESCAPE(3), `state & QUOTE` → refusal ✓; b15 `summary~=Setup Wi-Fi` →
space splits, bare `Wi-Fi` names no field → apply fails → refusal ✓; b40 `summary~=abc\` → ends
ESCAPE(1) → "Trailing backslash" (criteria.c:239-241) → refusal ✓. Carried-coverage check:
`carried=61/61` printed by the rerun and byte-equality of the r88 file are consistent with the
superseded-id guard (c53 absent).

Locale pin cross-check on the candidate: sets `locale.setlocale(LC_ALL, "C")` (candidate-A.py:124)
before ctypes libc `regcomp(buf, raw, REG_EXTENDED|REG_NOSUB)` (:115-116,:144), no REG_NEWLINE
anywhere — matches M24/M34-killed behavior and the oracle's C-locale results.

No wrong expectation found; no corrected JSON.

## 4. Findings

- **F1 (minor, process, already closed at HEAD):** the measured receipt
  `.ufo/waves/round-89/receipts/c1-measured-A-r89.txt` was uncommitted at both F and A (it cannot
  exist at F and was written after A); round-88 lesson R4 flagged exactly this pattern. It is now
  tracked in the records commit 51bf076f (current lane HEAD), so the gap is closed; only the
  measurement-time window remains as history. Evidence: `git show F:<path>` and `git show A:<path>`
  both fail with "exists on disk, but not in …"; `git log --all -- <path>` → 51bf076f.
- **No behavioral defect found** in candidate, counter, cases, mutants, or controls.

Residual risk / gaps (all lane-named limits, not new): mako's live runtime not exercised (resolver
only); C-locale reading holds for this build only (candidate pins it; a future setlocale in mako
changes it); NUL-byte refusal not case-exercisable; my 26 re-derivations are all oracle- or
criteria.c-sourced — the two stance labels (r19, b25: missing-input refusal) were intentionally not
selected, so their tool-stance provenance was not independently re-checked. No verification of C2
(out of seat scope).

Verification commands run (rc in parentheses): 17 pin sha256 checks (all PASS); counter rerun ×3
(1 = missing-file dead step, 1 = dead step, **0 = reproduced, diff empty**); oracle build cc -O0
(0); 17 labeled oracle runs (all agree); 9 parse-semantics derivations (all agree); git read-only
show/rev-parse/log/ls-files. No installs performed. No mutating git/jj command touched the lane; no
credential material read. Scratch deleted on exit.
