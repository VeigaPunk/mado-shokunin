# R97MReviewC2b — reviewer attack on C2 (counter self-invocation), round 97 wave w1b

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision
`e6152b589c2c6a28426c28263c4bcc3c46398be4` (branch `master`, lane HEAD == base at review time).
Scratch `/fast/scratch/hyaku/mado-r97/R97MReviewC2b`. Every probe is read-only against the lane; all
fixture repositories are clones under scratch (`git clone --no-hardlinks` of the lane, committed only
inside scratch). No lane file was written by this seat. Nothing was installed.

Status markers: **[MEASURED]** = command + output below; **[INFERENCE]** = reasoning only.
Scope: the final C2 artifacts (`build/c1-r96-magictext-selftest.v2.py`,
`build/c2-r96-selftest-kills-selftest.v2.py`, `build/c2-r97-counter-selftest.v2.py`,
`selftest-fixtures/`, `controls/counter-selftest-panel-v2.json`). The wave's final-draft sections are
at the end of this file; the w1-draft measurements in §1-§4 are the baseline the final bytes must
improve on and are marked as such.

---

## 0. Base state of the two counters — [MEASURED]

```
git show e6152b58:quality/counters/c1-r96-magictext.py | sha256sum
  9d3e1e76f2acf8c2219dd03157496363ddf9ff1a0089cc9aa090e5d0af42a7f7   64752 B
git show e6152b58:quality/counters/c2-r96-selftest-kills.py | sha256sum
  2bd9e5628993ceccf2739d0782a9cef7ff9ed5c6247336f5f3d07188eb4eb895   20512 B
```

`--selftest` on the base bytes, run exactly as the C2 counter runs a counter
(`env -i PATH=/usr/bin:/bin HOME=… TMPDIR=… LC_ALL=C.UTF-8 python3 -I <copy> --selftest`, cwd = the
copy's dir):

```
c1.py --selftest  -> rc=2   "error: the following arguments are required: --repo, --rev, ... "
c2.py --selftest  -> rc=2   "error: the following arguments are required: --repo, --rev, --panel, ..."
```

No `MADO_COUNTER_SELFTEST` line in either stream. Clause (iv)'s base half ("refuse with rc 2 and 0/2
green") therefore holds on the base bytes; the discrimination is by the **absence of the result line**
— the base refusal's rc (2) is the same code a legitimate could-not-evaluate selftest uses.

## 1. w1 drafts (superseded; recorded because the final bytes must not inherit them) — [MEASURED]

`build/c1-r96-magictext-selftest.py` (sha at first read `e492c46d…41033b`, later `09037477…aad96b`,
still mid-write by its owner) and `build/c2-r96-selftest-kills-selftest.py`
(sha `2bd9e562…4eb895`, **byte-identical to the base counter** — no `--selftest` at all).

1. **`--selftest` is unreachable in the c1 draft.** `main()` calls `ap.parse_args()` with every
   production flag `required=True`; the `if a.selftest:` dispatch sits *after* `parse_args()`, so
   `python3 -I draft.py --selftest` dies in argparse with rc 2 and never reaches the branch
   (`_mado_counter_selftest` is defined in the draft — it is simply never called). Contract 4's
   self-invocation is therefore not implemented by the draft. [MEASURED]
2. **A production line was removed.** The draft's diff against base is 6 added / 1 removed lines, and
   the removed line is `    draft = bool(a.draft_tool)`. `draft` is still read at the result line
   (`word = ("DRAFT_" if draft else "") + …`, `rev={'draft:' + … if draft else … }`, `if draft:
   return 3`), so every production run of the draft raises `NameError: name 'draft' is not defined`.
   This is a production-line change, not a self-test addition. [MEASURED]
3. **Tautological checks in the draft's selftest block** — `check_green_target_met` returns `True`
   after a fixture-shape test; `check_result_format` returns `bool(re.compile(...).pattern)` (a
   constant); `check_no_scratch_left` asserts the fixture dir is non-empty; `check_mutant_mismatch`
   asserts that the dummy tool does *not* contain the mutant's `find`. None of these can fail because
   of the counter's behaviour. [MEASURED — source read]
4. **Missing fixtures print a passing result line.** The draft's fixture-absent branch prints
   `MADO_COUNTER_SELFTEST: checks=7 failed=0` and returns 2. A parser keyed on the result line sees
   `failed=0`; only the rc distinguishes it. That is the opposite of the stable-id property item 2
   asks for. [MEASURED — source read]
5. **The draft selftest reads the live lane path.** `check_wrong_rev` hardcodes
   `--repo /home/vgpnk/Projects/shokunin/mado-shokunin`, so the check is not hermetic over the
   committed fixtures. [MEASURED — source read]

`build/c2-r97-counter-selftest.py` (the w1 C2 counter, sha `5bb9a8b6…8aa5b8`) was run end-to-end
against a scratch clone fixture (§3) and against a stub-counter fixture (§5). Its measured defects:

6. **Registry derivation is tip-only and the base control is a constant.** It counts
   `SKILL.md` rows at `--rev` only and passes `registry_rows == 4`; the "before" leg is the literal
   `BASE_REV_FALLBACK = "e6152b58…"` used as a `git show` argument, so on any repo without that object
   the base control is vacuous (`base-control … rc=2` → `base_refuse=ok` regardless). [MEASURED]
7. **The always-OK metric is inverted.** Its control increments `always_ok_flagged` when the stub is
   *not* flagged (`if not stub_flagged: always_ok_flagged += 1`) and then requires
   `always_ok_flagged == 0`. Since the always-OK stub prints `checks=6 failed=0` and exits 0, it is
   never flagged, so the metric always equals the panel size. Measured on the real panel-shaped fixture:
   `always_ok_flagged=12` with `negative_ids=0/12` — the conjunct can never hold as written.
   [MEASURED]
8. **The panel's `counter` field is ignored.** Every broken row is executed against *this* counter
   (`own_bytes = open(__file__, "rb").read()`), so a `broken` row naming
   `quality/counters/c2-r96-selftest-kills.py` is exercised against the C2 counter instead. Per-counter
   attribution (the revised clause (iii)) is not derivable from the w1 code. [MEASURED — source read]
9. **`expect_line` is satisfied by a bare `SETUP_ERROR`.** The draft's broken rows match the substring
   `"SETUP_ERROR"` anywhere in the output, not the declared id line (`MADO_MAGICTEXT_COUNT: SETUP_ERROR`
   vs `MADO_SELFTEST_KILLS: SETUP_ERROR`); a counter that prints the wrong counter's vocabulary would
   still satisfy it. [MEASURED]
10. **The empty-panel control is a setup error.** `{"counters":[],"broken":[]}` →
    `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR … counter path 'quality/counters/c1-r96-magictext.py' has
    no panel entry`, rc 2. The declaration's "an empty panel flags none" control is therefore not
    exercised by the w1 code. [MEASURED]

## 2. Registry claim re-derived from `SKILL.md` (item 4, first half) — [MEASURED]

Derivation used (identical to the counters' own clause): a row is a line whose first non-blank
character is `|` that contains the artifact path as a substring. `SKILL.md` has **zero** fenced table
rows at base (469 unfenced table rows; 0 inside ```/~~~ fences), so fenced/fenced-blind counting
differences do not arise on this file today.

```
git show e6152b58:SKILL.md   (sha256 6a8754df2d6d0123b77db384ac85bef17baa378e0be2782a01ba79e069ff028d)
table_rows=469
tools/mado-mimetext.py                              rows=1  line 887
quality/counters/c1-r96-magictext.py                rows=0
quality/counters/c2-r96-selftest-kills.py           rows=0
quality/selftest-kills/check-receipt-presence.json  rows=0
TOTAL named-artifact rows = 1

working tree SKILL.md        (sha256 6a8754df…ff028d, i.e. unchanged)
table_rows=469, TOTAL = 1     (same four lines: 1/0/0/0)
```

The lane tip at review time **is** the base revision (`git log --oneline -1` → `e6152b58 …`), so
"at the wave tip" cannot yet be measured from a commit: the after-number is whatever the L1 lands. The
honest declared move is **1 → 4** (the row at `SKILL.md:887`, added by `5dd921b3`, plus the three
missing rows). Clause (iv)'s `registry=1->4` is the correct sentence; a counter that prints
`registry=0->4`, or asserts the before-count as a literal without reading `--base-rev`, is measuring a
false base.

Synthetic after-state check (fixture only, never written to the lane): a 4-row variant of the same
`SKILL.md` counts `TOTAL=4` (one row per artifact) with the same derivation; the w1 C2 counter printed
`registry rows=4/4` against it. [MEASURED]

## 3. Ledger membership (item 4, second half) — [MEASURED]

```
git show e6152b58:quality/tool-ledger.md | grep -n -E 'c1-r96-magictext|c2-r96-selftest-kills'
  225:| `quality/counters/c1-r96-magictext.py` | Read-only C1 counter (round 96): …
  226:| `quality/counters/c2-r96-selftest-kills.py` | Read-only C2 counter (round 96): …

python3 -I quality/check-tool-ledger.py --repo . --rev e6152b58
  LEDGER: population=188 ledger_rows=188 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 \
          verdict=TARGET_MET rev=e6152b589c2c6a28426c28263c4bcc3c46398be4     rc=0
```

Both counters satisfy `is_population` (`quality/check-tool-ledger.py:172-175`,
`^quality/counters/[^/]+\.py$`) and both are ledger rows at base, with resolving pointers
(`bad_pointer=0`). **Clause (v) is an invariant, not a movement**: it evaluates identically before and
after C2, and `check-tool-ledger.py` prints counts, not membership — the counter must read
`quality/tool-ledger.md` at `--rev` and find the two rows itself (as the revised clause says) if it
wants to print `ledger_members=2/2`.

Unrelated working-tree ledger edit: `tools/mado-mimetext.py` "`--selftest` 20 checks" → "50 checks".
The correction is right — the tool is byte-identical to base (`d5f174fc…b857cbd`) and prints
`MADO_MIMETEXT_SELFTEST: checks=50 failed=0` — but it is outside C2's declared change and outside this
seat's write scope. [MEASURED]

## 4. Clause-level falsifiability of PRED-C2-r97-v1 — [MEASURED, with two legs pending the final bytes]

| clause | can I falsify it? | how, and what it returned |
|---|---|---|
| (i) both `--selftest` green, `failed=0`, rc 0, `checks ≥ 6` each | yes | run each final counter's `--selftest` under the C2 counter's exact invocation (temp-dir copy, empty-ish env, cwd ≠ lane) and parse `MADO_COUNTER_SELFTEST: checks=N failed=0` + rc. Base bytes return rc 2 with no line (§0). |
| (ii) every frozen neutralisation flagged with its declared id (`negative_ids == panel`) | yes | apply each panel `find`→`replace` to the counter bytes, rerun `--selftest`, require rc 1 **and** the id in the output. Real behaviour changes are what count; a docstring/comment edit that changes no check outcome surfaces as `SURVIVED` (measured on the w1 draft: `SURVIVED … C2-4/5/6`). |
| (iii) every broken-input mode named with its declared id and exit, per counter | yes, once the panel carries `counter` | each `broken` row must be executed against the counter it names; the w1 code ran all rows against itself (§1.8). A bare `"SETUP_ERROR"` substring is too weak — the id line must name the right counter's vocabulary. |
| (iv) controls: base bytes refuse (rc 2, 0/2 green); always-OK stub flags none (`always_ok_flagged=0`); registry `1 → 4` re-derived at `--base-rev` and `--rev` | yes | base refusal measured (§0). Stub metric measured inverted in the w1 code (§1.7). Registry derivable both ways (§2): base 1, after 4. |
| (v) both counters are ledger rows at `--rev` (`ledger_members=2/2`), `check-tool-ledger.py … uncovered=0` | yes, but it is an invariant | measured true at base (§3); it cannot separate C2 from do-nothing and should be stated as "stays covered, population +0". |

## 5. Stub-counter control (item 3, last sentence) — [MEASURED on the w1 C2 counter]

Fixture: scratch clone, one commit, the c1 side = the w1 draft counter, the c2 side = a stub file that
prints `MADO_COUNTER_SELFTEST: checks=6 failed=0` and exits 0 without running a check (the panel's six
`find` strings embedded verbatim as comments so each still occurs exactly once). Run of the w1 C2
counter:

```
selftest quality/counters/c2-r96-selftest-kills.py rc=0 checks=6 failed=0 green=True
SURVIVED quality/counters/c2-r96-selftest-kills.py C2-4 / C2-5 / C2-6 …
negative_ids=0/12   ->  MADO_COUNTER_SELFTEST_COUNT: TARGET_MISSED
```

The stub **passes** the green leg (i) on its own printed line, and is caught only by the neutralisation
clause (ii): a counter that prints the result line without work cannot produce the declared ids. That
is the structural catch the declaration promises; it lives in (ii), not in (i), so (i) alone must never
be treated as evidence of a real selftest.

## 6. `build/c2-r97-counter-selftest.v2.py` — [MEASURED] (589 lines, final sha256 `291d7087…1289a11`;
reviewed through `e46d50e6…a5470b` → `45847d4b…225a31` → final)

Read end-to-end, compiled, and exercised against three scratch clones (fixture repositories with a
`selftest-fixtures/` tree, base revision present, 4-row registry variant). It fixes every w1 defect
1.6-1.10:

- `--base-rev` and `--expect-base-registry-sha256` are required flags; `SKILL.md` is read at **both**
  revisions, each sha-pinned, and the per-artifact counts are printed
  (`registry <artifact> base=<n> rev=<n>`, then `registry rows base=1 rev=4`). The result line carries
  `registry=1->4` — measured against the real base (`6a8754df…`) and a 4-row tip variant.
  [MEASURED]
- `broken` rows must name their `counter`, must use a known mode, only `1|2` exits, a per-counter
  minimum of 3, and (mutated-tool) a relative `path` that resolves under a fixture root; each row is
  executed against **its own** counter's bytes in its own layout, and per-counter counts are printed
  (`broken_c1=…/3 broken_c2=…/3`). [MEASURED — validation and execution paths]
- Neutralisation requires a **line-anchored** `MADO_COUNTER_SELFTEST_FAIL: <declared id>` and exit 1;
  a surviving edit is printed `SURVIVED`. [MEASURED]
- Ledger membership is read from `quality/tool-ledger.md` at `--rev` (`ledger row … present=True`,
  `ledger_members=2/2`) and the gate is run from a scratch copy with `--repo <repo> --rev <rev>`;
  `uncovered_ok` comes from the gate's own `LEDGER:` line. [MEASURED]
- Guards: bad `--base-rev` → `SETUP_ERROR … base-rev deadbeef not a commit` (rc 2); wrong
  `--expect-base-registry-sha256` → `SETUP_ERROR … SKILL.md sha256 != …` (rc 2); no fixture tree at
  `--rev` → `SETUP_ERROR … no .ufo/waves/round-97/selftest-fixtures* tree at --rev` (rc 2); a
  `mutated-tool` `path` with `..` → `SETUP_ERROR … needs a relative fixture 'path'` (rc 2); a counter
  with <3 broken rows → `SETUP_ERROR … has 2 broken rows < 3` (rc 2). ASCII only (0 non-ASCII
  bytes); stdlib imports only. [MEASURED]

Residual findings on the v2 C2 counter (none of them flips TARGET_MET on the frozen inputs, all of
them weaken what the receipt may claim):

- **R6.1 — the always-OK leg is constant by construction.** `stub_flagged` is computed from one
  fixed run of `ALWAYS_OK` (`checks=6 failed=0`, rc 0) per panel row; nothing about the candidate
  counter enters that expression, so `always_ok_flagged` is 0 for every candidate. Measured on a
  fixture where all 12 neutralisations survived (`negative_ids=0/12`) the metric still printed
  `always_ok_flagged=0`. The declared control ("the stub flags none") is therefore vacuously true;
  the seat's phrasing "the always-OK stub is **flagged**" cannot be confirmed — the stub is
  `flagged=False` on every row. This is the r96-style null baseline, not a discriminating control.
  [MEASURED]
- **R6.2 — `wrong-rev` is not a revision stimulus.** The mode truncates every fixture blob to 0
  bytes and runs the counter's `--selftest`; the counter is never given a revision, so the mode
  measures "empty fixtures", not "a counter at a different rev". The receipt must name the stimulus
  honestly (`wrong-rev` = zero-length fixtures). [MEASURED — source read]
- **R6.3 — `ledger_members` is a substring test over the whole ledger.** A row that merely *mentions*
  a counter path in its prose satisfies `any(p in ln …)`. The gate's `uncovered=0` is the real
  membership proof; the `ledger_members` conjunct alone is gameable. [MEASURED — source read]
- **R6.5 — the runner's undeclared `--fixture-dir` dependency: FIXED.** In sha `45847d4b…` every
  counter invocation (green leg, every neutralisation, every broken mode) was
  `python3 -I <counter> --selftest --fixture-dir <dir>`; neither the declaration's C2 text nor shared
  contract 4 names that flag, and a counter that does not declare it dies in argparse with rc 2 /
  `error: unrecognized arguments: --fixture-dir …` and no result line → `selftest_green=0/2`
  (mechanism reproduced with a strict-parser counter: rc 2 with the flag, rc 0 without). Routed to
  both executors; the final sha `291d7087…` retries once with the bare contract-4 spelling when the
  output carries "unrecognized arguments" and prints an `invocation …` detail line. A counter-side
  SETUP_ERROR is never retried, so the `missing-input` scene stays terminal. [MEASURED]

- **R6.6 — the line formats the runner accepts are exact.** Green: one line matching
  `^MADO_COUNTER_SELFTEST: checks=(\d+) failed=(\d+)\s*$` (re.M) and no `MADO_COUNTER_SELFTEST_FAIL: `
  anywhere in stdout+stderr. A failing check must print a line matching
  `^MADO_COUNTER_SELFTEST_FAIL: <declared id>\s*$` (id terminal, nothing appended). Trailing prose on
  either line ("… failed=0 (fixtures ok)") silently fails every leg. [MEASURED — `RESULT_RE`,
  `FAIL_PREFIX`, `fail_id_present`]
- **R6.4 — the neutralisation ids are the panel's, not the check's.** The counter proves that the
  declared id line appears and rc is 1; it does not prove the id names the neutralised check. A panel
  whose ids are a generic `…-selftest` id would pass on any failing check. Panel quality is the
  control here (R97MMutC2b's frozen bytes). [INFERENCE from source]

## 7. Registry counting: 1 → 5 under pair counting; fixed to artifacts-covered — [MEASURED] RESOLVED

In sha `e46d50e6…a5470b` the counter derived the registry count as *pairs* — for each of the four
artifacts, every line whose first non-blank character is `|` and that contains the path — and required
`reg_base == 1 and reg_rev == 4`.

The scribe's draft rows (`w1/drafts/skill-registry-rows-r97.md` §1) also amend the existing
`mado-selftest-strength` row's (TOOL, KILLSET) list by appending
```
, (`quality/check-receipt-presence.py`, `quality/selftest-kills/check-receipt-presence.json`, 7 kills; round 96)
```
inside that same row. I applied the three draft rows plus exactly that amendment to
`git show e6152b58:SKILL.md` in scratch and counted with the counter's own derivation:

```
table_rows=472
tools/mado-mimetext.py                              rows=1  (line 887)
quality/counters/c1-r96-magictext.py                rows=1  (line 2998)
quality/counters/c2-r96-selftest-kills.py           rows=1  (line 2999)
quality/selftest-kills/check-receipt-presence.json  rows=2  (lines 879 amended strength row, 3000)
TOTAL = 5
```

So under pair counting the honest after-state is **5 pairs over 4 artifacts** and `reg_rev == 4` fails
(`registry=1->5`). Routed to R97MExecCounterC2b.

**Resolved in sha `45847d4b…225a31`** (measured with the counter itself on a scratch clone whose
`SKILL.md` is that amended file):

```
registry tools/mado-mimetext.py base=1 rev=1 (table-row pairs)
registry quality/counters/c1-r96-magictext.py base=0 rev=1 (table-row pairs)
registry quality/counters/c2-r96-selftest-kills.py base=0 rev=1 (table-row pairs)
registry quality/selftest-kills/check-receipt-presence.json base=0 rev=2 (table-row pairs)
registry artifacts covered base=1 rev=4
MADO_COUNTER_SELFTEST_COUNT: TARGET_MISSED … registry=1->4 …
```

The counter now counts **artifacts covered** (per artifact ≥1 row; base 1, after 4) and still prints the
pair counts for the reader, which is the robust form and matches the predicate sentence. The pair-count
line is the evidence that the landing's registry really names the kill-set twice; the covered count is
what `registry=1->4` now means. [MEASURED]

## 8. Fixtures, panel and the two selftest-enabled counters

### 8.1 Fixtures landed (contract-4 path) — [MEASURED]

`.ufo/waves/round-97/selftest-fixtures/` (8 files, ASCII, 14:12):

```
f090273e…7316e4e4  c1-cases.json      (2 cases, class "header", inputs data_b64/name_b64)
e5f9d381…270ea21a  c1-mutants.json    (2 mutants, classes header/sect)
3ef502bf…075a3f69  c2-kills.json      (2 kills, tool quality/check-receipt-presence.py, tool_sha256 "")
305d735f…c8a617495  control-kills.json (the round-96 frozen kill-set bytes: sha == the r96 pin)
384055f9…33b9eb2d  dummy-tool.py      (the pinned dummy scored tool)
0c7ebb4a…e02217d  host-list.txt
2659cb3e…030901fa  panel.json         {"hand":[],"neutral":[]}
5941534b…879cdf4  r90-argv.json      (base_rev e6152b58…, argv with @REV@/@BASE_REV@/@SCRATCH@)
```

### 8.2 Frozen panel `controls/counter-selftest-panel-r97.json` (sha `a672c9fc…`) — [MEASURED] NOT YET ALIGNED

Shape: 8 checks for `quality/counters/c1-r96-magictext.py`, 8 for
`quality/counters/c2-r96-selftest-kills.py`, and **3** `broken` rows. Against the final runner's
`validate_panel` this panel is a `SETUP_ERROR` before any leg runs:

1. the `broken` rows carry no `counter` field (the runner requires a string naming one of the two
   counters) → `SETUP_ERROR broken row … malformed`/`names unknown counter`;
2. 3 broken rows total (the runner requires ≥3 **per counter** and prints `broken_c1=x/3 broken_c2=y/3`);
3. `expect_line` is the runner's own vocabulary (`MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR`), but a
   broken row runs a **counter**, whose line is `MADO_MAGICTEXT_COUNT: SETUP_ERROR` /
   `MADO_SELFTEST_KILLS: SETUP_ERROR` — the declared line can never appear;
4. no `mutated-tool` row carries the required relative fixture `path` (e.g. `dummy-tool.py`);
5. duplicate ids: `C1-green-target-met` twice and `C2-missing-panel` twice — one neutralisation printing
   that id would satisfy both rows, so `negative_ids == panel` is not 16 independent probes;
6. every find is anchored to w1-era text (`return bool(pat.pattern)`, `C1-fixture-parses`,
   `C1-green-target-met`), none of which is guaranteed in the final `.v2` bytes; each find must occur
   exactly once there.

Routed to R97MMutC2b with the exact runner contract. This panel is WIP; it is re-measured below when it
freezes.

### 8.3 The two counters — PENDING

`build/c1-r96-magictext-selftest.v2.py` and `build/c2-r96-selftest-kills-selftest.v2.py` did not exist at
14:31. The **w1** counter bytes (`build/c1-r96-magictext-selftest.py`, sha `cc39301e…9528aa`) were
previewed against the landed fixtures as a proxy:

```
# scratch copy with fixtures beside it, python3 -I c1.py --selftest, empty-ish env, cwd=/scratch
MADO_COUNTER_SELFTEST: checks=7 failed=0        rc=0
```

Seven checks, green — but the block still carries the tautologies 1.3 describes:
`C1-result-format` returns `bool(pat.pattern)` (a constant), `C1-no-scratch-left` asserts the fixture dir
is non-empty, `C1-mutant-mismatch` asserts `str.replace` removed the find, and `C1-green-target-met` only
asserts the fixture envelope. Its fixture resolution also ends in a hard-coded absolute lane path
(`/home/vgpnk/.../selftest-fixtures`), an ad-hoc `MADO_SELFTEST_FIXTURE_DIR` env override, and a
missing-fixtures branch that prints `checks=0 failed=1` (rc 2) — a result line with `failed≠0`, which the
runner treats as not green (correct) but which a line-only reader could mistake for a partial pass.

**Three-way fixture break on the w1 bytes (item 2), measured on a scratch clone** (`quality/counters/`
+ `.ufo/waves/round-97/selftest-fixtures/`, committed; `python3 -I <counter> --selftest`, cwd per case):

```
c1 counter (sha 377a34fe…)
  baseline (cwd=repo)      rc=0  MADO_COUNTER_SELFTEST: checks=7 failed=0   ids=[]
  baseline (cwd=/)         rc=0  checks=7 failed=0                          ids=[]
  A renamed fixture dir    rc=0  checks=7 failed=0                          ids=[]      <-- GREEN
  B cwd=/tmp               rc=0  checks=7 failed=0                          ids=[]
  C renamed c1-cases.json  rc=2  checks=0 failed=1   ids=['C1-fixture-could-not-evaluate']
  IDS_IDENTICAL_ABC = False

c2 counter (sha 861883b3…)
  A renamed fixture dir    rc=0  checks=7 failed=0                          ids=[]      <-- GREEN
  C renamed panel.json     rc=2  checks=0 failed=1   ids=['C2-fixture-could-not-evaluate']
```

**A passes because the counters' fixture resolution ends in a hard-coded absolute lane path**
(`_committed = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97/selftest-fixtures"`), so
the selftest reads the *developer's lane* whenever the local tree has no fixtures. Isolated proof: a
scratch copy with that string changed to a nonexistent path fails A exactly as C does:

```
MADO_COUNTER_SELFTEST_FAIL: C1-fixture-could-not-evaluate
MADO_COUNTER_SELFTEST: checks=0 failed=1
```

So (a) the selftest is not hermetic — the committed-fixtures claim is not what makes it green; (b) item 2's
"identical ids in all three breakages" fails (A green, C one id); (c) the missing-fixtures branch prints a
result line with `failed=1` rather than a bare stable failure id set.

If the final `.v2` bytes are a copy of these, the panel cannot neutralise them into the declared ids
(§8.2.6) and the green leg will pass while proving little. Items 1-3 of the seat are re-run at the final
bytes and reported in §9.
