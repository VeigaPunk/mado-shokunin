# R89MExecForgery — forgery + counter attack on PRED-C1-r89-v1 (DRAFT)

Seat: R89MExecForgery (leaf, w1). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base revision `af998dcc41d48618ffe7afe0efc9354755a9244e`. **Every number below is DRAFT**: in-process
`score()` over draft case/mutant bytes, no receipts written under `.ufo/waves/round-89/receipts/`, no
frozen counter invoked. Nothing here is a measurement.

## 1. What was run (and against which bytes)

The lane moved while this seat ran: `build/mado-mako.c1.py`, `controls/mako-cases-r89.json` and
`controls/mako-mutants-r89.json` were all rewritten by other seats between 17:18 and 17:58, and the
**freeze landed at ~18:00–18:07** (declaration `## Freeze` filled; `receipts/c1-measured-A-r89.txt`).
My snapshot C is byte-identical to the frozen pins, so the snapshot-C numbers below are reproducible
against the frozen inputs (still DRAFT: I ran `score()` in-process, not the frozen counter CLI).
Three snapshots are reported, each pinned by sha256.

| snapshot | candidate | cases | mutants |
|---|---|---|---|
| A (as handed to me) | `2720922b1b92…229e` (44 189 B) | `d04e27fc…0431` (91 cases) | M01–M32 (32) |
| B (mid-wave) | — | — | `5471bee2…e35f` (37: M33–M37 added) |
| C (**= the freeze**) | `6b4bc409…3a98` (44 829 B, the L1's ordered-occurrence fix) | `5fdca7db…5672` (141 cases: blind-seat `b*`/`n*` appended) | `5471bee2…e35f` (37) |

Cross-check against the frozen receipt: my in-process snapshot-C candidate run gives
`correct=141 killed=37 controls naive 34 / globals 35 / base 78 / python-re 127`, exactly the numbers
`receipts/c1-measured-A-r89.txt:467` reports (`MADO_MAKO_REGEX: TARGET_MET … python_re_correct=127`).

Counter bytes: `drive6.py`/`drive7.py` (all snapshot-C numbers, and the counter attacks) loaded
`quality/counters/c1-r89-mako-regex.py` at its frozen sha256 `5b977141…634e`, with the pinned round-88
machinery `3678425a…cc1f`. `drive.py`/`drive2.py` ran before the counter file's 17:48 rewrite and used
an earlier revision of it (not preserved); their `correct/N` counts come from `tool_verdict` over the
pinned round-88 machinery and are unaffected, but their verdict labels are only as good as that
revision.

Method (exactly the seat item's call shape):

```python
m = importlib spec_from_file_location("/…/quality/counters/c1-r89-mako-regex.py")   # sys.argv untouched
cases = m.R88.load_cases(open(cases_path, "rb").read())
base_text = git -C <lane> show af998dcc:tools/mado-mako.py        # sha256 c374d715…92237
res = m.score(tool_text, base_text, cases, [], scratch, 61, declared=None, range_check=False)
```

With `mutants=[]` and `carried=61` literal, `killed == m == 0` and `carried == 61` hold by
construction, so those runs' verdicts are decided only by `correct == N` and the four controls. The
full-predicate runs pass the real mutant list and `declared=len(mutants)`.

Driver scripts (scratch, deleted at exit): `drive.py` (A), `drive2.py`/`drive3.py`/`drive4.py`
(B), `drive5.py` (A∪proposed), `drive6.py`/`drive7.py` (C, pinned). `prop/run.py`, `prop2.py`,
`probe_b32*.py` for single-case reproduction. Oracle: `cc -O0 -o oracle
.ufo/waves/round-89/controls/posix-ere-oracle.c` (exit 0) plus a local `REG_NEWLINE` variant
(`nl.c`, exit 0).

## 2. Per-forgery table (DRAFT)

All forgeries are edited copies of the candidate. Each keeps the counter's three fixed `PYRE_FORGERY`
anchors present exactly once and puts its deviation in a new code path, because the counter's
python-re control is derived by string substitution and a tool that removes an anchor is a
`SETUP_ERROR`, not a scored miss (see §3 F6).

Snapshot A, 91 cases, `mutants=[]` (so `correct/N` is the whole signal):

| forgery | wrongness | correct | failing cases |
|---|---|---|---|
| `forgery-a-refuse-regex-sections.py` | `summary~`/`body~` dropped from `MODELLED_FIELDS` (refuse every regex section) | **67/91** | r01–r10, r13–r16, r20, r21, r23–r30 (24) |
| `forgery-b-python-fullmatch.py` | Python `re.fullmatch` replaces libc `regexec` | **76/91** | r02, r03, r05–r13, r23–r25, r28 (15) |
| `forgery-c-python-search.py` | Python `re.search` (the counter's own python-re shape) | **81/91** | r05–r13, r25 (10) |
| `forgery-d-basic-regex.py` | `regcomp(..., REG_NOSUB)` — `REG_EXTENDED` dropped | **82/91** | r03, r04, r05, r11, r12, r13, r22, r29, r30 (9) |
| `forgery-e-locale-inherited.py` | `setlocale(LC_ALL, "C")` removed (inherits `LC_ALL=C.UTF-8`) | **88/91** | r08, r09, r25 (3) |
| `forgery-f-r88-quote-rule.py` | round-88 quote rule: inside quotes a backslash escapes only `"` and `\` | **90/91** | r14 (1) |
| `forgery-g1-two-regex-fields-or.py` | two regex fields OR-ed (naive edit) | 91/91 | none — but `SETUP_ERROR` with mutants: `mutant M26-regex-polarity: anchor occurs 0 times` |
| `forgery-g1-or-dead-and-line.py` | same OR, AND line kept as dead code | 91/91 | none; killed **31/32** (M26 survives) → TARGET_MISSED |
| `forgery-g1b-second-regex-ignored.py` | only the **first** regex field of a section is honoured | **91/91** | none; killed 32/32, controls 22/23/67/81 → **TARGET_MET** at snapshot A |
| `forgery-g2-reg-newline.py` | `regcomp(..., REG_EXTENDED\|REG_NOSUB\|REG_NEWLINE)` | **91/91** | none |

The `g2` 91/91 was measured with the pre-rename text; the on-disk file differs only in a local
variable name (`raw` → `data`, needed so it does not duplicate mutant M25's anchor) and was measured
again at snapshot C (139/141).

Snapshot C (141 cases, 37 mutants, pinned), the same two wrong tools:

| tool | correct | killed | controls (naive/globals/base/python-re) | verdict |
|---|---|---|---|---|
| candidate (`6b4bc409…`) | 141/141 | 37/37 | 34 / 35 / 78 / 127 | TARGET_MET |
| `g1b-second-regex-ignored` | 138/141 | 37/37 | 34 / 35 / 78 / 124 | TARGET_MISSED (b27, b32, b33) |
| `g2-reg-newline` | 139/141 | 34/37 | 34 / 35 / 78 / 79 | TARGET_MISSED (n04-reg-newline-dot-crosses-newline, n04-reg-newline-caret-after-newline) |

So both case-set gaps I found at snapshot A are **already closed at the live snapshot C** by blind-seat
cases (`b26`/`b27` two-regex-fields pair, `n04-reg-newline-*`). Findings F1/F2 below are therefore
"valid at the 91-case snapshot, closed at 141"; they would matter only if the freeze had pinned the
older file — it did not (the frozen pin is `5fdca7db…`, 141 cases).

## 3. Findings

### F1 — (snapshot A only) the case set does not require two regex fields in one section to AND — a wrong tool passes PRED-C1-r89-v1

`forgery-g1b-second-regex-ignored.py` honours only the first `summary~`/`body~` of a section
(`if not compiled: compiled[key] = pattern`), so `[summary~=alpha body~=beta]` applies whenever
`summary` matches, whatever `body` is. At snapshot A it scored **91/91, killed 32/32, controls
22/23/67/81 → `TARGET_MET`** — a full pass with a wrong matcher. Upstream requires both:
`criteria.c:115-131` matches `summary_pattern` and `body_pattern` as independent conjuncts.

Proposed cases (equivalent to the live `b26`/`b27`; ids `f01`/`f02` avoid the live `r31`/`r32` ids):

```json
{"id": "f01-two-regex-fields-body-misses",
 "home_files": {".config/mako/config": "anchor=top-right\n[summary~=^alpha body~=^beta]\nanchor=bottom-center\n"},
 "config": ".config/mako/config",
 "args": {"summary": "alpha", "body": "gamma"},
 "expect": {"effective": {"anchor": "top-right"}, "refusals": "none"},
 "pin": "criteria.c:115-131: summary_pattern and body_pattern are independent conjuncts"},
{"id": "f02-two-regex-fields-both-match",
 "home_files": {".config/mako/config": "anchor=top-right\n[summary~=^alpha body~=^beta]\nanchor=bottom-center\n"},
 "config": ".config/mako/config",
 "args": {"summary": "alpha one", "body": "beta two"},
 "expect": {"effective": {"anchor": "bottom-center"}, "refusals": "none"},
 "pin": "criteria.c:115-131: both pattern criteria must match"}
```

Oracle: `./oracle '^beta$' 'gamma'` → `nomatch`; `./oracle '^alpha' 'alpha one'` → `match`;
`./oracle '^beta' 'beta two'` → `match` (all exit 0). Measured: candidate passes both;
`g1b` fails `f01` and passes `f02` (`prop/run.py`, exit 0). The live set's `b27` is the same case and
already kills `g1b` (138/141 at snapshot C).

### F2 — (snapshot A only) no case carries a multi-line value, so `REG_NEWLINE` is undetectable

`forgery-g2-reg-newline.py` compiles with `REG_NEWLINE` added. At snapshot A it scored **91/91**;
every case value is single-line, so `^`, `$` and `.` behave identically. mako passes exactly
`REG_EXTENDED | REG_NOSUB` (`criteria.c:333-334,345-346`).

Proposed cases (equivalent to live `n04-*`):

```json
{"id": "f03-inner-newline-caret-not-anchored",
 "home_files": {".config/mako/config": "anchor=top-right\n[body~=^beta$]\nanchor=bottom-center\n"},
 "config": ".config/mako/config",
 "args": {"body": "alpha\nbeta"},
 "expect": {"effective": {"anchor": "top-right"}, "refusals": "none"},
 "pin": "criteria.c:345-346 regcomp(REG_EXTENDED|REG_NOSUB) without REG_NEWLINE: ^ and $ anchor at the string bounds only"},
{"id": "f04-dot-crosses-newline",
 "home_files": {".config/mako/config": "anchor=top-right\n[body~=alpha.beta]\nanchor=bottom-center\n"},
 "config": ".config/mako/config",
 "args": {"body": "alpha\nbeta"},
 "expect": {"effective": {"anchor": "bottom-center"}, "refusals": "none"},
 "pin": "POSIX ERE without REG_NEWLINE: . matches a newline"}
```

Oracle: `./oracle '^beta$' $'alpha\nbeta'` → `nomatch`; `./oracle 'alpha.beta' $'alpha\nbeta'` →
`match`; the `REG_NEWLINE` build (`./nl`, exit 0) flips both (`match` / `nomatch`). Measured:
candidate passes both, `g2` fails both. Independent corroboration: the mutation-tester's own
`M34-reg-newline-added` **survives** over snapshot A/B (candidate 33/37 at snapshot B) and is killed
only once `n04-*` is present (candidate 37/37 at snapshot C).

Both proposed-case sets load cleanly: `load_cases` accepts 91+4 = 95 cases (inside the counter's
70..110 range) and `carried_count` still returns `(61, 61)` (`check_cases.py`, exit 0).

### F3 — the measured tool can read the case file and echo the expectation: 141/141

`tool_verdict` (`quality/counters/c1-r87-mako-criteria.py:228-254`) checks exit 0, JSON on stdout, a
`refusals` list whose *content* is never inspected, and only the `effective` keys the case names —
extra keys are ignored. `materialize` (`:190-204`) writes only `home_files` into the home, so no
expectation is in `HOME`; but the case file is a readable repo file and the tool runs as the same uid.

`counter-expect-echo.py` = candidate + a lookup that reads
`.ufo/waves/round-89/controls/mako-cases-r89.json`, matches the case by (config text, argv) and prints
`expect.effective` plus a dummy refusal when `expect.refusals == "present"`. Result at snapshot C:
**141/141**, all cases. It only fails the predicate because the derived python-re control is the same
tool (`forged = 141 = N`). The three cases `c25`/`c26`/`c27` share one (config, argv) signature with
disjoint expected keys, so the echo emits their union and `tool_verdict` accepts the extra keys — the
case set's own duplicates make the echo trivial.

### F4 — `semantic_kill` is vacuous for a tool that can see it is not the candidate copy

`evaluate` writes the candidate as `<gen>/tool.py` and every mutant as `<gen>/mutant-<i>.py`, and
passes `TMPDIR=<gen>` to every run (`c1-r88-mako-fields.py:214-241`). A tool that compares its own
bytes with `$TMPDIR/tool.py` knows which role it is playing.

Measured with **semantically neutral** mutants (`old` → `old + "  # neutral"`):

| tool | mutants | killed |
|---|---|---|
| candidate | 37 neutral | **0/37** (snapshot A: 0/32) |
| `counter-self-detect.py` | the same 37 neutral | **37/37** |

So `killed == M` can be manufactured without any behavioural difference. `counter-self-detect.py`
adds one branch (`_role()` reads `$TMPDIR/tool.py`, and on a byte difference replaces the result with
a well-formed wrong one) and otherwise is the honest candidate: 141/141, 37/37, controls
34/35/78/0 → `TARGET_MET`.

### F5 — the whole predicate is satisfiable by a tool that implements none of the claim

`counter-full-role-aware.py` = candidate + (i) the case-file echo of F3, (ii) the self-detection of F4,
(iii) suppression of the echo when its own source contains the python-re substitution
(`b"return re.compile(pattern)"`), which is exactly what the derived control contains. Measured at
snapshot C: **correct 141/141, killed 37/37, controls naive 34 / globals 35 / base 78 / python-re 0 →
`TARGET_MET`**. The tool does not parse mako config, does not call `regcomp`, and does not implement
`summary~`/`body~`; it reads the answer key and fingerprints the harness. (At snapshot A the same
construction was measured before the echo was extended to union the three `c25`/`c26`/`c27`
signatures: 89/91, 32/32, controls 22/23/67/0 — the two misses were exactly those duplicate-signature
cases, which the union fix then covered.)

This is a counter-robustness finding, not a case-set finding: adding cases cannot fix it, because the
echo follows whatever the case file says. Candidate mitigations for the L1 (none applied here):
run the measured tool with the repo path masked (bubblewrap/unshare) **or** trace `openat` and fail
any read outside `HOME`/`--config`/`--read-root`; give every run its own generation directory with the
tool always named `tool.py` (defeats F4's filename/byte comparison); accept that a self-checksumming
tool can always defeat text-substitution mutants and say so in the receipt.

### F6 — negative results (no exploit found)

- **JSON on stderr**: `counter-stderr-json.py` prints the result to stderr and exits 0 → **0/141**
  (`bad-json` on every case). `tool_verdict` reads `proc.stdout` only.
- **Exit codes**: a non-zero exit is `exit=<rc>` and never a pass (`:231-232`); a crash is not a kill
  (`CRASH_PREFIXES`), and `semantic_kill` requires a well-formed differing result.
- **Submitting the literal python-re control shape**: rejected before scoring —
  `SetupError: forgery anchor '    lib = _libc()\n    buf = ctypes.create_string_buffer(REGEX_T_BYTES)\n
  if lib.regcomp(buf, raw, REG_EXTENDED | REG_NOSUB) != 0:\n        return None\n    return buf\n'
  occurs 0 times in the measured tool` (exit 2 path; observed with the first, anchor-removing draft of
  forgery b/c).
- **Naive OR edit**: `mutant M26-regex-polarity: anchor occurs 0 times in the measured tool` — the
  mutant conjunct rejects it (the anchor-preserving variant survives only M26, see the table).

### F7 — brittleness (side observation, not a forgery)

The counter's fixed `PYRE_FORGERY` and mutant anchors bind the candidate's *text*, not just its
behaviour: a candidate that renames a local in the matcher (e.g. `raw` → `data`) or repeats an
anchor-shaped line is a `SETUP_ERROR` (observed: `mutant M25-anchored-match: anchor occurs 2 times in
the measured tool` when a forgery's helper re-used the `raw = pattern.encode(...)` line). This is
sound as anti-evasion, but it means the freeze must pin the exact tool text, and any post-freeze
cosmetic edit is a setup error rather than a miss.

## 4. Files written

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-89/w1/forgeries/` (sha256 in the order
listed by `sha256sum *.py`):

```
42853932…979b  forgery-a-refuse-regex-sections.py
af53fa81…ee27  forgery-b-python-fullmatch.py
c5acead1…9fd1  forgery-c-python-search.py
4b061911…3a5f  forgery-d-basic-regex.py
f0a415f6…4fe3  forgery-e-locale-inherited.py
4500b149…ba54  forgery-f-r88-quote-rule.py
7853be28…19f2  forgery-g1-or-dead-and-line.py
89edd85f…9c33  forgery-g1-two-regex-fields-or.py     (naive OR; SetupError with mutants)
b54bd6f1…e2b1  forgery-g1b-second-regex-ignored.py
e4f362ca…9f9c  forgery-g2-reg-newline.py
ad88005e…5e20  counter-expect-echo.py
b732ae45…45a7  counter-full-role-aware.py
f7240183…8cec  counter-self-detect.py
853a0cb4…b31c  counter-stderr-json.py
```

Plus `w1/R89MExecForgery-results.json` (the machine-readable snapshot-C table). The forgery files on
disk were written from candidate `2720922b…229e` (17:26–17:41); the pinned snapshot-C measurements
rebuilt the same tools from `6b4bc409…3a98` in scratch, and every anchor was re-asserted to occur
exactly once there. Each file is self-contained and runs with `python3 -I`.

## 5. Verification actually run

Drivers whose exit status was captured directly (`; echo rc=$?`, no pipe):

- `python3 check_cases.py` → rc 0 (`load_cases` N=95, `carried_count` (61, 61)).
- `python3 check_setup.py` → rc 0 (both setup-error paths reproduced: `M26 … anchor occurs 0 times`,
  and the anchor-removing python-re shape).
- `python3 prop/run.py <candidate>` → rc 0 (4/4 proposed cases pass).
- `cc -O0 -o oracle …/posix-ere-oracle.c` → rc 0; `cc -O0 -o nl nl.c` → rc 0; oracle runs → rc 0.
- `sha256sum` over the pins and the forgery files → rc 0.

Drivers run with their output piped through `tail` (exit status therefore **not** captured; each
printed its complete table with no traceback, which is the evidence used):

- `python3 drive.py` (snapshot A, 8 forgeries, `mutants=[]`) → table §2.
- `python3 drive2.py` (snapshot A/B, 9 runs incl. the neutral-mutant pair).
- `python3 drive3.py` (g2 vs 37 mutants), `python3 drive4.py` (snapshot B, 3 tools).
- `python3 drive5.py` (91+4 cases, 37 mutants).
- `python3 drive6.py`, `python3 drive7.py` (snapshot C pinned, 9 runs; `pin/results.json`).

Not run (deliberately): the frozen counter end-to-end, any receipt under `receipts/`, any git/jj
mutation, the candidate's `--selftest`. The freeze landed while this seat ran (18:00–18:07); the
snapshot-C inputs are byte-identical to the frozen pins, but every number here is still an in-process
DRAFT run, not a measurement.

## 6. Risks / blockers for the L1

1. **The freeze took the 141-case file, which is what closes F1/F2.** At the 91-case snapshot two
   wrong tools passed (F1: 91/91, 32/32, `TARGET_MET`; F2: 91/91); at the frozen 141-case set the same
   two tools score 138/141 and 139/141 (`b27`, `b32`, `b33`, `n04-*`). No action needed if the frozen
   pins stand; if any of those cases is ever dropped, F1/F2 come back (`f01`–`f04` in §3 are the
   minimal replacements).
2. **PRED-C1-r89-v1 cannot tell an honest implementation from a tool that reads the case file**
   (F3/F5): `TARGET_MET`, 141/141, 37/37, controls 34/35/78/0, from a tool that implements nothing.
   The frozen receipt's `TARGET_MET` is sound *for the submitted bytes* — the candidate is honest —
   but the predicate has no anti-echo property, so it cannot be cited as evidence that the tool
   implements the claim. This is the most serious finding and is independent of the case set.
3. **`killed == M` is vacuous for a self-aware tool** (F4): 0/37 → 37/37 on semantically neutral
   mutants. Same scope note as (2).
4. **Churn**: candidate, case and mutant files all changed under this seat (three snapshots, §1). Any
   number quoted without its sha256 is unusable; the frozen pins (`6b4bc409`, `5fdca7db`, `5471bee2`,
   base `c374d715`) are the only ones that may be cited.
5. `M23`, `M25`, `M34` survive against the `g2` tool at snapshot C — that is an artefact of scoring a
   wrong tool, not a case-set gap; the candidate kills all 37.

## 7. Scratch

`S=/fast/scratch/hyaku/mado-r89/R89MExecForgery` was created with `mkdir -p`, used for every fixture,
pin and counter `--scratch-root`, and **removed on exit** (`rm -rf -- "$S"`); the results JSON was
copied into `w1/` first. No pacman transaction, no install, no PATH write, no credential read.
