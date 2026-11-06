# mado round 89 — claims declaration

L1: MadoR89 (planner seat held by the L1). Base revision `af998dcc41d48618ffe7afe0efc9354755a9244e` (master, = the
round-88 closure tip; `tools/mado-mako.py` there has sha256 `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237`,
the round-88 C2 tool). Hyaku run 15, attempt 1. Round shape: ONE v1 wave `w1` (12 seats, settled before the freeze) + at
most one residual call `r1` (≤4 attack seats) on the frozen and measured bytes; total ≤16.

## Inputs read before declaring

- `corpus/lessons/round-88-verifier-spotcheck.md` (non-author, closed `ok`): routed R1 (four C1 survivors), R2/R3 (four C2
  survivors; RM2C2 is a named limit, not a defect), R4 (records cited an uncommitted receipt), R5 (`*.ready.dispatched`
  markers left untracked).
- `.ufo/waves/round-88/r1/R88MResidMut.md` §3–§4 (the eight routed survivors and the cases the frozen sets lack).
- Round-88 named limit: "summary~/body~ refused; the host's five click-action sections stay unresolved".
- `considerthese/2026-11-06.md` proposal 1 (carry a survivor ledger; report the first later commit that kills one) and
  proposal 3 (read-only check against João's real theme files).
- Upstream mako v1.11.0 `criteria.c` 46-59 (`match_regex_criteria`), 115-132, 162-262 (`parse_criteria`), 332-351
  (`regcomp(..., REG_EXTENDED | REG_NOSUB)`), 542-550 ("Cannot set both"); the v1.11.0 tag tree has no `setlocale` call;
  `/usr/include/regex.h` 310/323; setlocale(3) 135-137 (a program starts in the "C" locale).
- Host: `~/.local/share/omarchy/default/mako/core.ini` lines 24-36 carry five `[summary~="…"]` sections.

Stagnation nudge: not claimed (a capability row entered at round 88). Every owned axis sits at 10, so the lowest-axis
obligation is a tie; C1 works coverage and C2 works operability.

## C1 — coverage (capability acquisition): summary~ / body~ matched the way mako 1.11.0 matches them

Surface moved (frontier → core): the two criteria fields this round adds — `summary~` and `body~` — become modelled. The
round-88 tool refused them by construction; it also refuses mako's second-pass fields `group-index` and `grouped`, and still
does after this round (named limit). The value passes through the criteria tokenizer as upstream's `parse_criteria` does (a
backslash escapes and is dropped before any next character, inside quotes too; only a space separates tokens; a trailing
backslash or an unmatched quote rejects the criteria), then every occurrence is compiled with libc
`regcomp(REG_EXTENDED | REG_NOSUB)` and the last one is matched with `regexec` (unanchored search), through ctypes, after the
tool sets `LC_ALL=C` — the v1.11.0 tree contains no `setlocale` call and a C program starts in the "C" locale (setlocale(3)),
while a bare Python process on this host starts in `en_US.UTF-8`, so the pin is load-bearing. A criteria section whose
summary~/body~ value `regcomp` rejects is refused; `summary` with `summary~` (or `body` with `body~`) is refused.

Count that would show it unmoved (prints 10 at base, 12 at the C1 revision):

```sh
git show <rev>:tools/mado-mako.py | python3 -c "import sys,re; t=sys.stdin.read(); m=re.search(r'MODELLED_FIELDS = \((.*?)\)', t, re.S); print(len(re.findall(r'\"[^\"]+\"', m.group(1))))"
```

- Candidate: `.ufo/waves/round-89/build/mado-mako.c1.py` (copied to `tools/mado-mako.py` only after the freeze).
- Counter: `quality/counters/c1-r89-mako-regex.py` (PRED-C1-r89-v1; machinery = the frozen round-88 counter, sha-pinned).
- Cases: `.ufo/waves/round-89/controls/mako-cases-r89.json`, N = 141: the 61 round-88 cases carried byte-equal (61 of the
  round-88 file's 62; c53-summary-tilde-refused, which asserted the refusal, superseded and absent — the counter raises a
  setup error if its id reappears), r01–r32 and n04/n04/n07 (L1-authored from the w1 review; generator
  `controls/gen-c1-cases-r89.py` with its own re-implementation of `parse_criteria`, verdicts from `controls/posix-ere-oracle.c`),
  then b01–b44 (R89MScoutCases, blind: authored without opening the candidate, `controls/mako-cases-r89-blind.json`).
- Label provenance (stated before data): every r/n/b expectation comes from the C oracle (libc regcomp/regexec, C locale) after
  a parse_criteria re-implementation, except: r17/r18 (criteria.c 542-550 "Cannot set both"), n07/b40/b41 and r32's earlier
  occurrence (criteria.c 226-239 / apply order), and r19, b25 (tool stance: a field whose notification input was not supplied
  is refused, never guessed — a stance label, a regression pin, not independent ground truth).
- Mutants: `.ufo/waves/round-89/controls/mako-mutants-r89.json`, M = 37: round-88 M01–M22 byte-equal + M23–M37.
- **Predicate PRED-C1-r89-v1 (verbatim, = counter docstring):** TARGET_MET iff the candidate tool's correct count equals N,
  all M mutants are killed, the 61 carried round-88 cases are present unchanged, and the four controls (naive-toplevel,
  globals-include, base-tool, python-re) each score strictly below N.
- Concrete after-state: `correct=141` of `cases=141`, `killed=37` of `mutants=37`, `carried=61/61`, and each control < 141.
  Pre-freeze control receipt `receipts/c1-controls-prefreeze-r89.txt` prints the four control values on the frozen bytes.
- Before: the round-88 tool is the base-tool control (it refuses every summary~/body~ section); fields modelled 10.
- Kill rule: any conjunct false → TARGET_MISSED; a setup error (rc 2) is not a verdict and is not retried into green; the
  case and mutant files are the freeze bytes (sha256 below) — a post-freeze change is a new case set with a new predicate.

## C2 — operability: a runnable survivor gate kills seven of round 88's eight routed survivors

Surface moved: the lane's committed, runnable checks for `tools/mado-mako.py`. Before this round the routed survivors are
caught by no scored case set (the round-88 frozen sets kill 0 of the 7 countable) and by the tool's own `--selftest` for 3 of 7
(RM7C1, RM3C2, RM4C2: `receipts/c2-selftest-control-r89.txt`). The new gate `quality/counters/c2-r89-survivor-kills.py` —
the survivor list plus two supplementary case sets scored through the frozen round-88 machinery — re-runs at any revision and
prints, per survivor, killed / survived / crashed and whether the round-88 sets alone kill it (considerthese 2026-11-06
proposal 1, the survivor ledger). `tools/mado-mako.py` is not changed by C2. Axis note (R89MCritic F2 argued this is instrument
depth, i.e. quality-trend work): the move is a new runnable artifact whose stated outcome is produced by running it, which is
AXES.md's operability; it is not coverage or depth (§9).

- Survivors: `.ufo/waves/round-89/controls/survivor-mutants-r89.json` (8; RM2C2 excluded as the confirmed TOCTOU named limit).
- Supplementary sets: `controls/survivor-cases-c1side-r89.json` (4), `controls/survivor-cases-c2side-r89.json` (4).
- Label provenance of S (before data): 5 of 8 rest on a cited source — the four `s1-*` (criteria.c match_criteria strcmp,
  apply_criteria_field bare tokens; mako.5 L45) and `s2-double-slash` (config.c expand_config_path); `s2-trailing-slash`,
  `s2-root-is-a-file` and `s2-cycle-second-lexical-path` are tool-stance labels (regression pins). Of the 7 counted kills, 5
  rest on sourced labels and 2 (RM3C2, RM5C2) on stance labels.
- **Predicate PRED-C2-r89-v1 (verbatim, = counter docstring):** TARGET_MET iff (a) the measured tool is correct on every case
  of B ∪ S, (b) every survivor mutant except the declared crash-only RM6C2 is killed over B ∪ S (7 of 7), (c) the do-nothing
  control — the identical scoring over B alone — kills strictly fewer than 7.
- **RM6C2 is declared crash-only before data**, so seven of the eight survivors can stop surviving; RM6C2 stays alive and is
  scored and printed. Argument: the mutant compares the lexical target with a stack of resolved paths. Where every include
  edge is a non-symlink path, target == realpath(target) and the mutant behaves as the tool. A cycle that re-enters through a
  symlinked edge is missed by the mutant, which re-reads the same file and replays the same symlinked edge, so it recurses until
  RecursionError (exit 1). Hence no terminating input separates RM6C2 with a well-formed result, and the frozen round-88 kill
  rule (a crash is not a kill) cannot count it (R89MReviewC2 §3 confirmed it and tried four counterexamples). The round-88
  residual seat's "distinguishes" (FAIL exit=1) was that crash (lesson M89-1).
- Concrete after-state: `MADO_MAKO_SURVIVORS: TARGET_MET … cases=95 correct=95 counted=7 killed=7 do_nothing_B_only_killed=0`
  at the freeze revision, the receipt printing `tool_sha256=c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237`.
- Before: B alone kills 0/7 (`receipts/c2-controls-prefreeze-r89.txt`); tool selftest 3/7 (`receipts/c2-selftest-control-r89.txt`).
- Kill rule: as C1.
- Freeze sequencing: C2 is measured at the freeze revision, and the freeze commit does not change `tools/mado-mako.py` (the C1
  candidate stays under `build/` until after the freeze). C2's eight anchors occur exactly once in the C1 candidate too and B
  excludes c53, so the identical command re-runs at the C1 revision as a harm watch, not a claim element.

## Causal separation

C1's counter opens only its own cases, mutants, the round-88 case file and the base tool; no C2 file. C2 is measured where the
tool is still the round-88 tool. Neither needs the other's change (R89MCritic F8 STANDS).

## Named limits (before data)

- `group-index` and `grouped` (mako's second-pass fields) stay refused; a `[group-index=1]` section yields one refusal on both
  revisions.
- RM6C2 stays alive (crash-only). Mutation-tester N09 (refusal message text) is not observable by the case language; N10
  (free-before-use) is crash-only.
- Escaped `=` (`summary\=x`, upstream sets summary) and a standalone `""` token (upstream ignores it) are refused by the tool
  (R89MReviewC1 F2/F3; pre-existing at base, outside the claimed tokenizer rules).
- mako's runtime is not exercised: the resolver answers what the config would compute (no live notification is sent).
- The C-locale reading holds for this mako build (no setlocale in v1.11.0); a later mako that calls setlocale changes it.
- A NUL byte in a summary~/body~ value is refused (C strings stop at NUL; not exercised by a case).

## Draft run disclosure

Before the freeze the L1 and the w1 seats ran, on draft bytes: the candidate's `--selftest` (59/59), both counter selftests
(27/27, 18/18), controls-only runs, one draft C2 scoring over B ∪ S (95/95, 7 killed, RM6C2 crashed), draft C1 scorings
(91 cases: 91/91, 32/32; 141 cases with 37 mutants: 141/141, 37/37, controls naive 34, globals 35, base 78, python-re 127) and
the seats' differential fuzz (12 800 candidate/oracle comparisons, 0 disagreements). These were adequacy checks, not
measurements; the measured runs are the frozen commands below at the frozen revisions.

## Draft revisions (from the w1 seats, before the freeze)

1. R89MReviewC1 F1: an earlier invalid `summary~` occurrence in one header (`[summary~=a(b summary~=x]`) was accepted; upstream
   compiles each occurrence as it is applied. Fixed in the candidate (`ordered` occurrences compiled in order) + case r32 +
   mutant M37 + selftest check (59 checks).
2. R89MReviewC1 M33: outside-quote escape keeps its backslash — mutant M33 + case r31.
3. R89MMutTester N04/N07/N14 survivors — mutants M34 (REG_NEWLINE), M35 (dangling quote escape), M36 (trailing backslash) +
   cases n04 ×2, n07 (b40 already covered N14).
4. R89MScoutCases blind set b01–b44 appended unchanged; N 91 → 141, counter range 120..160, M 32 → 37.
5. R89MCritic F2–F11: axis note for C2; literal after-states; MODELLED_FIELDS count command; "two fields this round adds";
   label provenance for both claims; freeze sequencing; harm watch and named limits; the sourced-claim rows (C1's entry cites
   S496/S497/S498/S499 opened this round, from R89MScoutSources).
6. R89MReviewC2: READY, no change. R89MExecSelftest: all guards fail closed (rc 2). R89MExecHostDiff: base decides 4/9 host
   criteria sections (5 refusals per run), candidate 9/9 (0 refusals).

## Harm watch (run at the C1 revision; receipt `receipts/harm-final-r89.txt`)

C2 command re-run at the C1 revision; `bash tools/mado-verify.sh --selftest`; `bash tools/mado-verify.sh --no-live`;
`python3 -I quality/check-index.py --repo . --rev <records>`; `python3 -I quality/check-tool-ledger.py --repo . --rev <records>`;
`python3 -I tools/mado-mako.py --selftest --scratch-root DIR`; both counter selftests; the census.

## Freeze

Freeze = the lane commit that adds this section (its hash is recorded in SCORECARD.md / LOG.md and the report). Pins (sha256):

| file | sha256 |
|---|---|
| `quality/counters/c1-r89-mako-regex.py` | `5b977141ec1f21911c6247d250900bcd6ec35ae16213318e41ef8f5c4111634e` |
| `quality/counters/c2-r89-survivor-kills.py` | `73bd520125b1c63f344776bac506d0fb3ec251261a168641e31c6716803fc0d0` |
| `quality/counters/c1-r88-mako-fields.py` (pinned machinery) | `3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f` |
| `quality/counters/c2-r88-include-containment.py` (pinned machinery) | `f8e18b7c915fe831e6eaafcd09fad0af9ac23d89514317f131fb1ed409e96767` |
| `.ufo/waves/round-89/controls/mako-cases-r89.json` (N = 141) | `5fdca7dbcce6687d81aa31548e935a49fa39cee03117db41358068a0ded15672` |
| `.ufo/waves/round-89/controls/mako-mutants-r89.json` (M = 37) | `5471bee29b4ba5da7fa7e55d8b11003028b0eb4c7937bd8d114062491338e35f` |
| `.ufo/waves/round-88/controls/mako-cases-r88.json` (carried) | `a0e81b191fb0f80ca352699ede47962c1ac01c1ae8e9e15ccf50b1d7fab4a091` |
| `.ufo/waves/round-89/controls/survivor-mutants-r89.json` (8) | `9f25df3cac28d9085d2e7d2a89e6002df24f76e6c5264df98f83d4d32c8104f0` |
| `.ufo/waves/round-89/controls/survivor-cases-c1side-r89.json` (4) | `c710a3e5a2a0e88692de68c6dec9815f14f5964099ec7ef6fdb8cb20bb743c1a` |
| `.ufo/waves/round-89/controls/survivor-cases-c2side-r89.json` (4) | `e02e2b4de83410ab16fcf7ad92f5374c5178a3e49c80d6aa2c4994e0d04e612e` |
| `.ufo/waves/round-89/controls/mako-cases-r89-blind.json` (44, merged unchanged) | `a4fa66cf9c2c44d2a2fbdaacf7069521e4a4b796556a6d383819bc458b19464a` |
| `.ufo/waves/round-89/controls/posix-ere-oracle.c` | `4227019226073c975ae466b5753c938dcd3fdd9bd5701fd049297438460f8ce8` |
| `.ufo/waves/round-89/controls/gen-c1-cases-r89.py` | `6cb7310175e55214d0f39f3cfea89d300ade2c710592cfc2a366c588e3173669` |
| `.ufo/waves/round-89/build/mado-mako.c1.py` (C1 candidate, lands unchanged) | `6b4bc409750f493469ce789b6b6c0c072d6ab638ff7e90dc9b31d642ae673a98` |
| `tools/mado-mako.py` at the freeze (= base, round-88 tool) | `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237` |

Pre-freeze control receipts (committed in the freeze): `receipts/c1-controls-prefreeze-r89.txt`
(`MADO_MAKO_REGEX_CONTROLS: BELOW_N cases=141 naive_correct=34 globals_include_correct=35 base_tool_correct=78
python_re_correct=127`, rc 0), `receipts/c2-controls-prefreeze-r89.txt` (B alone: 0/7 killed),
`receipts/c2-selftest-control-r89.txt` (tool selftest: 3/7), `receipts/census-start-r89.txt` (rc 0).

Measurement commands (exact argv; `DIR` = `$HYAKU_SCRATCH/mado-r89/L1`):

C2, at the freeze revision `F`:

```sh
python3 -I quality/counters/c2-r89-survivor-kills.py --repo . --rev F --expect-survivors-sha256 9f25df3cac28d9085d2e7d2a89e6002df24f76e6c5264df98f83d4d32c8104f0 --expect-c1side-sha256 c710a3e5a2a0e88692de68c6dec9815f14f5964099ec7ef6fdb8cb20bb743c1a --expect-c2side-sha256 e02e2b4de83410ab16fcf7ad92f5374c5178a3e49c80d6aa2c4994e0d04e612e --scratch-root DIR
```

C1, at the C1 tool revision `A` (the commit after the freeze that copies the candidate to `tools/mado-mako.py` unchanged):

```sh
python3 -I quality/counters/c1-r89-mako-regex.py --repo . --rev A --base-rev af998dcc41d48618ffe7afe0efc9354755a9244e --cases .ufo/waves/round-89/controls/mako-cases-r89.json --expect-cases-sha256 5fdca7dbcce6687d81aa31548e935a49fa39cee03117db41358068a0ded15672 --expect-mutants-sha256 5471bee29b4ba5da7fa7e55d8b11003028b0eb4c7937bd8d114062491338e35f --expect-r88-cases-sha256 a0e81b191fb0f80ca352699ede47962c1ac01c1ae8e9e15ccf50b1d7fab4a091 --scratch-root DIR
```
