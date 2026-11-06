author: hyaku closure (non-author integrator, @m_zfl)

# mado round 89 — verifier spot-check (non-author)

Round report `.ufo/reports/round-89/mado.md`; lane repo `mado-shokunin`, branch `master`; round base
`af998dcc41d48618ffe7afe0efc9354755a9244e`; freeze / C2 measured revision `d87361354b4d142287aac05bb973315749ef1fce`;
C1 measured revision `099c662dc55521e365cd4126132cdcda4efc54b6`; records `51bf076fd970106da854e11873b886528c3cffaf`;
round tip (closed) `16ee97b5a398d0d51b605670f35feb059a5487b6`. I did not author this round; every command below was run
by me against committed bytes (or the re-opened source) on this host, 2026-11-06. Driver digest (closure prompt;
verified against `.ufo/watchdog.log` lines 3034 and 3054 at read time):
`2026-11-06T17:04:06-03:00 launch mado round=89 pgid=2396541 driver=hyaku-inline attempt=1` /
`2026-11-06T18:25:29-03:00 complete mado round=89; hyaku-inline attempt=1`.

## 1. Conformance (step 1)

| item | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-89/mado.md` (fleet repo) | `mado-shokunin <mado@shokunin.local> 8ae0836694b5102dd1fc6392a086689b898679f9 2026-11-06T18:24:47-03:00`: after the lane tip (`16ee97b5` committed 18:23:53), before the driver `complete` (18:25:29) | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` | heading present; 4 `[~]` lines, one per canonical box, each with a pointer | pass |
| cited lane commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}`; `git merge-base --is-ancestor <h> master` over `af998dcc`, `d8736135`, `099c662d`, `51bf076f`, `16ee97b5` | all five exist; all ancestors of `master`. `git log af998dcc..16ee97b5` lists exactly the four round commits, all by `mado-shokunin` | pass |
| no uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `16ee97b5…` | pass |
| prompt carries the template contract | `diff <(sed -n 1,140p kimi-shokunin/templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/mado-round-89.md)` | only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions in §1–§5; §6 hyaku addendum, §7 scratch and run-15 notes follow; prompt committed `b14da214` (17:04:04) before the launch line (17:04:06) | pass |
| round-88 routed R5 (dispatch markers) | `git status --porcelain` empty; report cites freeze `d8736135` | closed | pass |

**Conformance defects (status-neutral):** see §5 D1 (receipts cited before committed, second round running) and D2
(gate registry rows absent from the registry home).

## 2. Claims (step 2)

Gate standard: I executed no lane gate, counter or tool `--selftest`. Counter verdicts are **evidence-verified**
(receipt tallies, revisions measured, pinned digests recomputed by me from committed bytes); the parts below marked
**re-measured** I derived myself with plain commands.

### C1 — coverage (capability): mako `summary~`/`body~` as libc POSIX ERE, C locale

| check | command (mine) | observed | kind |
|---|---|---|---|
| MODELLED_FIELDS before → after | `git show <rev>:tools/mado-mako.py` → `ast.literal_eval` of the `MODELLED_FIELDS = (…)` tuple, `len()` | `af998dcc`: 10; `16ee97b5`: 12 (adds `summary~`, `body~`) | re-measured |
| tool at A = frozen candidate; unchanged to tip | `git show 099c662d:tools/mado-mako.py \| sha256sum`; same for `d8736135:.ufo/waves/round-89/build/mado-mako.c1.py`; `git diff --quiet 099c662d 16ee97b5 -- tools/mado-mako.py` | both `6b4bc409750f…3a98`; no diff A→tip | re-measured |
| base tool digest | `git show d8736135:tools/mado-mako.py \| sha256sum` | `c374d71514f1…2237` = receipt `tool_sha256` for the C2 freeze run | re-measured |
| case set pin and composition | `git show d8736135:…/controls/mako-cases-r89.json \| sha256sum`; `jq '.cases\|length'` and id-prefix grouping | `5fdca7dbcce6…5672` = `--expect-cases-sha256`; 141 cases = c 61 + r 32 + n 3 + b 45 (agrees with the SCORECARD erratum, 45 not 44) | re-measured |
| mutant count | `jq '.mutants\|length'` on `mako-mutants-r89.json` | 37 | re-measured |
| controls and counters frozen | `git diff --quiet d8736135 16ee97b5 -- .ufo/waves/round-89/controls quality/counters` | no diff after the freeze | re-measured |
| **oracle labels independently re-derived** | my own script: libc via ctypes, `setlocale(LC_ALL,"C")`, `regcomp(REG_EXTENDED\|REG_NOSUB)` + `regexec(…,0,NULL,0)`, a replica of mako's `parse_criteria` (backslash takes the next char, `"` toggles, space splits), every occurrence compiled, last occurrence matched; applied to all r/n/b cases whose `oracle` is a single `summary~:` / `body~:` `match\|nomatch\|invalid` | **65/65 agree**, 0 disagree (15 multi-field / undecided / tokenizer cases skipped) | re-measured |
| counter verdict | `receipts/c1-measured-A-r89.txt` | `MADO_MAKO_REGEX: TARGET_MET rev=099c662d… cases=141 correct=141 carried=61/61 mutants=37 killed=37 naive_correct=34 globals_include_correct=35 base_tool_correct=78 python_re_correct=127`, `rc=0`; no `^case … FAIL` line; 78 `control base-tool … ok ok` lines = `base_tool_correct=78` | evidence-verified |
| pre-freeze controls | `receipts/c1-controls-prefreeze-r89.txt` | `BELOW_N cases=141 naive_correct=34 globals_include_correct=35 base_tool_correct=78 python_re_correct=127` | evidence-verified |
| residual reviewer | `r1/R89MResidC1.md` | C1 VERIFIES, receipt reproduced byte-identically (466/466 lines) | evidence-verified |

Report says before 78/141, fields 10 → after 141/141, fields 12: **matches**. Axis verdict: **coverage — improved**.

### C2 — operability: runnable survivor gate over round 88's routed survivors

| check | command (mine) | observed | kind |
|---|---|---|---|
| pins | `sha256sum` of `survivor-mutants-r89.json`, `survivor-cases-c1side-r89.json`, `survivor-cases-c2side-r89.json` at `d8736135` | `9f25df3c…04f0`, `c710a3e5…3c1a`, `e02e2b4d…12e` = the three `--expect-*` pins | re-measured |
| survivor population | `jq -r '.mutants[].id'` | 8 ids (RM2C1, RM3C1, RM5C1, RM7C1, RM3C2, RM4C2, RM5C2, RM6C2); RM6C2 declared crash-only → counted 7 | re-measured |
| supplementary cases | `jq '.cases\|length'` on both sides | 4 + 4 = 8; with the 87 round-88 B cases (control receipt) = 95 | re-measured |
| before: B-only control | `receipts/c2-controls-prefreeze-r89.txt` | `{'total': 87, … 'killed_full': 0, … 'counted': 7, 'verdict': 'TARGET_MISSED'}` → 0/7 | evidence-verified |
| before: r88 tool selftest | `grep -c 'selftest_distinguishes=yes' receipts/c2-selftest-control-r89.txt` | 3 of 8 rows (RM7C1, RM3C2, RM4C2); RM6C2 = no → 3/7 counted | re-measured (tally) |
| after | `receipts/c2-measured-F-r89.txt`; `receipts/c2-harm-at-A-r89.txt` | `TARGET_MET rev=d8736135… cases=95 correct=95 counted=7 killed=7 do_nothing_B_only_killed=0`; same verdict at `099c662d` with `tool_sha256=6b4bc409…` | evidence-verified |
| residual reviewer | `r1/R89MResidC2.md` §4 | C2 VERIFIES | evidence-verified |

Report says 0/7 (sets), 3/7 (selftest) → 7/7: **matches**. This also closes round-88 routed R1/R2; R3 (RM6C2) is
answered by the crash-only declaration made before data, upheld by R89MResidC2. Axis verdict: **operability — improved**.

### Harm watch

- `git diff af998dcc 16ee97b5 -- SCORECARD.md`: append-only (+35/−0), a new `## Round 89` section with claims table,
  capability row, named limits, errata. `git diff --numstat` lines with deletions: `corpus/SOURCES.md` 7/2 (S493/S494
  `used-by` rewritten, logged in the lesson), `quality/tool-ledger.md` 3/1 (mado-mako row updated), `tools/mado-mako.py`
  125/12 (the C1 change). `SKILL.md`, `PROVINCE.md` unchanged.
- `receipts/harm-final-r89.txt` (evidence-verified): `MADO_SELFTEST: 460/460`, `MADO_VERIFY: CLEAN (29 pass …)`,
  `MADO_INDEX … indexed=110/110 … coverage=10.0000/10`, `LEDGER: population=165 … uncovered=0 … TARGET_MET`,
  `MADO_MAKO_SELFTEST: checks=59 failed=0`, counter selftests 27/27, 18/18, 40/40, 28/28; every `rc=0`.
- Knowledge entries `git ls-tree --name-only <rev> corpus/knowledge/ | wc -l`: 109 → 110 (re-measured).
- No owned axis harmed.

| axis | verdict |
|---|---|
| coverage | improved |
| operability | improved |

## 3. Discernment spot-check (LEARNING.md)

Sample from `corpus/lessons/round-89.md` `## Gate` → *Candidates considered*.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/mako-regex-criteria-r89.md` | admit | S500 tag tarball `https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0` re-fetched: sha256 `72d11d3f…7282` (matches the row); `criteria.c` 333-334 and 345-346 `regcomp(…, REG_EXTENDED \| REG_NOSUB)`, 335-336 invalid → `return false`, 48 `regexec(pattern, value, 0, NULL, 0)` (unanchored, no flags), 543/548 "Cannot set both"; `grep -rn setlocale` over the tree: 0 lines | agree | every rule the entry states (flags, unanchored search, C locale by absence of `setlocale`, invalid pattern rejects the criteria, the conflict rule) is in the upstream bytes at the cited lines, and my independent libc replica agrees with all 65 single-field oracle labels the entry's tool is scored on |
| modelling the fields with Python `re` | reject | my own run of `re.search` with the same tokenizer replica over the same 65 labelled cases | agree | Python `re` disagrees with the libc oracle on 12/65 (e.g. r05 `^[[:digit:]]+$` vs `2026`: oracle match, `re` nomatch; r06/r07 `\d` literal-d in ERE vs digit in `re`; r08 `^.$` vs `é` in the C locale; r10 GNU `\<foo\>`): a different question, as the reject reason says |
| calling `regcomp`/`regexec` without pinning the locale | reject | an earlier replica run of mine that omitted `setlocale` (the Python process inherits the environment's UTF-8 `LC_CTYPE`) | agree | without the pin r08 (`^.$` vs `é`) returned match and b42 (`^..$` vs `é`) nomatch, both contrary to the C-locale labels; with `setlocale(LC_ALL,"C")` both agree. The reject's M24 argument reproduces |

New `corpus/SOURCES.md` row re-opened: **S496** (`file:///usr/share/man/man3/regex.3.gz`). `sha256sum` →
`f79f05fd…be6ff` (matches the row); `zcat … \| nl -ba \| sed -n 77,84p` reads "Use POSIX Extended Regular Expression
syntax when interpreting *regex*. If not set, POSIX Basic Regular Expression syntax is used." — the Gate's quote
(19 words, ≤25) at the stated decompressed lines 77-84. Also re-opened S498 (`setlocale.3.gz`, sha256 `253d8b37…`,
lines 135-137 "On startup of the main program, the portable "C" locale is selected as default.") and S499
(`/usr/include/regex.h`, sha256 `ae656ea6…`, line 310 `#define REG_EXTENDED 1`, line 323 `#define REG_NOSUB (1 << 3)`):
all match.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` →
rc 0, `mado ok`, 55 `W04` + 1 `W01` (S277 tier C `mined`, already present in the round's start and end receipts —
pre-existing). Rows `grep -c '^| S[0-9]' corpus/SOURCES.md`: 430 at `af998dcc` → 435 at `16ee97b5` (re-measured).

## 4. Trend verdicts

- **expansion — improved:** one admitted entry on uncovered ground (knowledge 109 → 110; regex criteria, C locale,
  tokenizer), its `source:` citing mined rows S493/S494/S496–S500; five new tier-A `mined` rows (430 → 435); one
  capability row in `SCORECARD.md` (round 89, first-working 89).
- **quality — improved:** QUALITY criteria 148–149 appended (numbered criteria 48 → 50 by
  `grep -cE '^\*\*[0-9]+\.' corpus/QUALITY.md`), each tied to a mined mistake (M89-1, M89-2); the round-88 tool's
  silent defects (tokenizer escapes, refusal of the two fields) superseded by a version scored on 141 cases with 37/37
  mutants killed; residual critic findings F1–F4 corrected by appended errata, not rewrites; no admitted entry failed
  its re-check.
- **discernment — improved:** this non-author spot-check agrees with the gate on the admit and on two rejects, each
  re-derived from re-opened sources and my own replica.

## 5. Routed defects (lane must fix next round)

- D1 (record, repeat of r88 R4 / lane's M89-4): the records commit `51bf076f` cites `receipts/harm-final-r89.txt` and
  `receipts/census-end-r89.txt`, which first appear in `16ee97b5` (`git log --diff-filter=A`). Land the proposed
  receipt-presence check in round 90 and run it before the records commit.
- D2 (gate registry): `SKILL.md` registry rows stop at `mado-r86-*` (line 860); the round-87/88/89 counters, including
  this round's `c1-r89-mako-regex.py` and `c2-r89-survivor-kills.py` (called a "gate" in the report), are registered
  only in `quality/tool-ledger.md`. PROTOCOL §Gate standard, Registry/Delivery: the registry home of a child lane is
  its own `SKILL.md`; until the rows land there, closure grades these gates non-conformant (status-neutral).
- D3 (lane-routed, confirmed): R89MResidMut survivors RS01 (body~ earlier-invalid ignored), RS05 (quote start not
  started), RS12 (`group-index`/`grouped` accepted) survive 141/141 (`r1/R89MResidMut.md` lines 91, 95, 102) — add
  the killing cases in round 90.
- Note for the operator (promotion is operator-owned): the four SHONEN boxes carry concrete pointers; box 1 still
  points at a knowledge entry while `SKILL.md` is unchanged this round, so it is not fully checkable as worded.
