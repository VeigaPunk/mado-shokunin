# mado round 98 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Round 98, hyaku run 15, attempt 1. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`,
branch `master`, base `35f3ce808788b11c063309b1b5ad0192754795ea` → lane tip
`6f61eff075243f564d1e7eed4823d7c521388a42`. Report `.ufo/reports/round-98/mado.md`.
This file is the outside discernment check; it is not lane work and it edits no lane-authored file.

## 1. Step-1 conformance

| item | result | pointer |
|---|---|---|
| report committed by the lane identity | **ok** | `git log --format='%an %H' -- .ufo/reports/round-98/mado.md` → four commits, all `mado-shokunin <mado@shokunin.local>` (`30ac2607`, `0a9f093c`, `47142ae2`, `38152387`) |
| `SHONEN` heading, one line per box | **ok** | `## SHONEN` + four `[~]` lines, each with a resolvable pointer; no `[x]` |
| every cited lane commit exists and is an ancestor of the branch | **ok** | `git merge-base --is-ancestor <h> master` for `06b6bf2a`, `a3471631`, `020af865`, `24ced668`, `b3c8e134`, `fa4445af`, `6f61eff0` → all true; `git cat-file -e` all present |
| lane repo clean and pushed | **ok** | `jj-lane.sh state` → `branch=master local=6f61eff0 remote=6f61eff0 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` = `6f61eff0` |
| round diff | **ok** | 7 commits, 116 files, +32325/−19; the only deletions are 19 `used-by` cells in `corpus/SOURCES.md` (allowed in place, old→new log committed) |
| prompt carries the template contract | **ok** | `diff templates/round-prompt.md .ufo/prompts/mado-round-98.md` lines 1–140 = substitutions only; §6 addendum; five child-lane items present (report path §4, commit-before-report §5, `SHONEN` §4/§5, commit-hash citation §4/§5, write scope §3/§5); L2 floor §3 = 8, equal to `MISSION.md` §L2 concurrency; §3 routes through the host table, no model alias in the lane repo |
| wave shape | **ok** | `w1/swarm-registry.json` 11 members: 4 executor, 2 mutation-tester, 1 scout, 1 scribe, 1 connector, 1 reviewer, 1 critic; attack 4/11 = 36 %; all 11 seat reports exist; no residual call; no dead seat |
| report lands last | **defect (status-neutral)** | the first report commit `30ac2607` (17:52:03) preceded the lane tip `6f61eff0` (17:52:29) by 26 s; the filed bytes were then rewritten in `0a9f093c`/`47142ae2`/`38152387` (+8/−5) without an erratum naming the superseded text (PROTOCOL "filed report is a record"; recurrence of the r97 spot-check's D1 in-place-rewrite half). The final report commit is after the tip and cites it, so the end state satisfies "lands last" |

Driver digest (`.ufo/watchdog.log`, mutable; copied): `2026-11-07T16:31:03-03:00 launch mado round=98
pgid=3734780 driver=hyaku-inline attempt=1`; `2026-11-07T17:53:18-03:00 complete mado round=98;
hyaku-inline attempt=1` (verified at lines 3221/3229 of the live log).

## 2. Claims — re-check

The two claims were re-derived with plain measurements over committed bytes (git/census/grep/wc/jq
counts). The lane's own counters and gates were **not executed** (PROTOCOL §Gate standard: the
integrator verifies committed evidence, never a sibling's gate); their committed receipts were read
and their inputs re-hashed.

### C1 — coverage (capability, new surface): the launch argv sequence

| check | command | observed |
|---|---|---|
| base absence | `git cat-file -e 35f3ce80:tools/mado-execargv.py` | `fatal: path 'tools/mado-execargv.py' exists on disk, but not in '35f3ce80…'`, rc 128 |
| tip presence and pin | `git show 6f61eff0:tools/mado-execargv.py \| sha256sum` | `49f7fecdc3bef99a077fe73ac12f5fe211d7ae8c41df5ddc949daf685405f713` = the report's `49f7fecd…f713` and the declaration's C1 candidate pin |
| frozen cases | `git show 6f61eff0:.ufo/waves/round-98/controls/execargv-cases-r98.json \| python3 -c …` | `cases` list 88, `classes` list 20, `glib2` `2.90.1-1`, `gio_sha256` `d2164260…`, `renderer_sha256` `182cf06c…` |
| frozen mutants | same over `execargv-mutants-r98.json` | 79 mutants, 20 classes, `candidate_sha256` `49f7fecd…` (matches the tool), 16 `not_observable`, 8 `equivalents` |
| fresh generator pin | `git show 6f61eff0:…/execargv-fresh-r98.py \| sha256sum` | `b7bc137a643c771f1cd88a3909d1650205b37a155869ade84adc419e3515357c` |
| frozen-run verdict | `receipts/c1-measured-r98.txt` | `MADO_EXECARGV_COUNT: TARGET_MET pred=PRED-C1-r98-v1 rev=a3471631… tool_sha256=49f7fecd… cases=88 correct=88 classes=20/20 mutants=79 killed=79/79 class_kills=20/20 fresh=60/60 fresh_seed=f00d3edcdb285ac0 control_naive=4/88 control_fieldcode=47/88 memoriser_fresh=0/60`; `selftest rc=0 checks=38 failed=0` |
| freeze pins match the tip bytes | `sha256sum` over the declaration's C1 rows | candidate `49f7fecd…`, counter `7ed2f8f6…`, cases `21cccc3a…`, mutants `32c207b3…`, genseed `b7bc137a…` — all equal |
| separability | `receipts/c1-at-base-r98.txt` | `SETUP_ERROR … tools/mado-execargv.py absent at 35f3ce80`, rc 2 |

**Verdict: improved** (evidence-verified: the counter's frozen-run verdict and self-test tally are
committed; the inputs re-hash to their pins). The file-URI encoding fix at `a3471631` is the
re-freeze the report names.

### C2 — operability: the SOURCES registry citation read-back

| check | command | observed |
|---|---|---|
| base absence | `git cat-file -e 35f3ce80:quality/check-sources-readback.py` | `fatal: path … exists on disk, but not in '35f3ce80…'`, rc 128 |
| tip presence and pin | `git show 6f61eff0:quality/check-sources-readback.py \| sha256sum` | `f1000bf11e88149695aa96229fcf2155929ebbb72a2cfa215d8c24e2f37bd8f5` = the report's `f1000bf1…d8f5` |
| counter pin | same over `quality/counters/c2-r98-sources-readback.py` | `e944fdacd1285a44e3026b0c8ccccf9dce5f6ec687ec047c2327e8cec61e6e0a` |
| registry rows | frozen census grep over `git show <rev>:corpus/SOURCES.md` | base 462 → tip 466; entries 118 → 119 |
| new rows | `grep -E '^\| *S(528\|529\|530\|531) *\|'` | S528-S531 all tier A, status `mined`, `used-by` = `corpus/knowledge/gio-exec-argv-r98.md` |
| repair, independent parse | python over base/tip `SOURCES.md` | 19 rows gained `used-by` paths; 24 added paths (21 repaired + 3 new-entry); **0 removed paths**; 4 new rows S528-S531; the 21 repaired pairs match the receipt's 21 `BASE_MISMATCH` lines |
| entry and index | `git show 6f61eff0:corpus/knowledge/gio-exec-argv-r98.md \| wc -l`; index count | entry 690 lines; `source:` cites S504 S506 S527 S528 S529 S530 S531; 119 knowledge files and 119 unique index rows in `corpus/README.md` |
| frozen-run verdict | `receipts/c2-measured-r98.txt` | `MADO_SOURCES_READBACK_COUNT: TARGET_MET all-legs-green`; `base_mismatches=21 expect=21 match=ok`; `gate_selftest=ok checks=21 failed=0`; `gate_findings=0 rows=462 entries=118 gate_rc=0`; `repaired=21/21`; `added_paths=21`; `planted=5/5`; `stub_flagged=1`; `census=ok`; counter selftest `checks=18 failed=0` (`c2-readback-r98-measured.txt`) |
| measured revision pinned | `git show a3471631:corpus/SOURCES.md \| sha256sum` | `719a96d5…` = the receipt's `rev_registry_sha256` |
| separability | `receipts/c2-at-base-r98.txt` | `SETUP_ERROR gate-absent-at-rev quality/check-sources-readback.py`, rc 2 |
| fleet census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | rc 0; 466 rows; 64 W04 + 1 W01 (S277 tier C mined, pre-existing); no E-codes |

**Verdict: improved** (evidence-verified). **Defect:** the report, SCORECARD and LOG say "gate
findings 0 over 466 rows / 119 entries"; the measured revision `a3471631` has **462 rows / 118
entries** (the receipt and the gate seat's report both say 462/118). The 466/119 state (`020af865`+)
was never gated with committed evidence. The claim's declared predicate pins `--rev a3471631`, which
passes; the prose overstates the measured state.

### No axis harmed

- `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `SKILL.md`, `corpus/README.md` diffs: **0 deletions**
  (append-only). The round's only deletions are the 19 `used-by` cells in `corpus/SOURCES.md`, which
  the SOURCES contract allows in place and the lesson logs old→new.
- Harm watch `receipts/harm-final-r98.txt`: 26 legs, 22 rc 0, four nonzero — `r90c1_portal_routing`
  (declared SETUP_ERROR since r93), `r95c1_mimesniff` and `r95c2_selftest_kills` (no
  counting-command argv in the harness), `r96c1_magictext` (known stale mutant pin). No new harm.
  **Defect:** the final 26 legs omit `r97c1_filetype` and `r97c2_counter_selftest` (both present in
  the 28-leg first run `harm-base-r98.txt`); the report's "round-97 leg set replayed at the records
  tip" overstates coverage.
- Ledger: my own parse of the gate's population rule (tools/ + `quality/*.py` +
  `quality/counters/*.py`) → 195 population, 195 ledger rows (the 196th `| \`<repo-relative path>\` |`
  line is the fenced grammar example), 0 uncovered — the report's `population=195 ledger_rows=195
  uncovered=0` reproduces.

## 3. Discernment spot-check

Sources re-opened 2026-11-07. GLib files fetched from the recorded URLs and hashed against the
lesson's digests; the spec and the installed man page re-read at their recorded locators.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S528 — `gdesktopappinfo.c` launch expansion | admit | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c (163369 B, sha256 `8e9ce1a8…5b0d`) | **agree** | the lesson's quote `/* If there is no macro default to %f. This is also what KDE does */` is at `:2738`; tier A is right for the implementation source; the anchor's `expand_application_parameters` range `:2700-2746` and the spawn loop `:3008-3186` both resolve |
| `corpus/knowledge/gio-exec-argv-r98.md` | admit | the same file, `gshell.c`, the spec page, `gio.1` | **agree** | the load-bearing citations resolve: `g_desktop_app_info_load_file` `:2098-2113`, `g_key_file_load_from_file` `:2108`, `%d`/`%n` dirname/basename `:2528-2539`/`:2621-2641`, `g_shell_quote` `:200-235`; the frontmatter cites S528-S531/S504/S506/S527; the entry's limits are stated |
| `%d`/`%n`/`%N` as unimplemented | reject as model fact | `gdesktopappinfo.c` `:2528-2539`, `:2621-2641` | **agree** | GLib 2.90.1 implements all four cases; the spec's "Deprecated" is not "unimplemented" |
| `Hidden=true` as a refusal | reject as model fact | `gdesktopappinfo.c` `:1206` (the only `Hidden` read), `:2098-2113` (load path) | **agree** | the filename constructor loads the keyfile without a hidden gate; the check lives in the desktop-id lookup |
| the `#`-bypass branch as a model fact | reject as model fact | `gdesktopappinfo.c` `:2557-2577` (`expand_macro_uri`), `:2600-2610` (`force_file_uri` only for `u`/`U`) | **agree** | the branch exists but is reachable only when `force_file_uri` is set; a local file URI's fragment is dropped before the call and a non-local URI answers the URI either way |
| the spec's `%i` "two arguments" wording | reject as model fact | `gdesktopappinfo.c` `:2661-2667`; spec rendered line 95 | **agree** | the source appends `--icon ` + the quoted icon name as one string; the tokenizer splits it into two argv entries, so the spec describes the result, not the append |
| S532 — `gio-tool-launch.c` | admit (lesson Gate table and the "S528-S532" Candidates row) | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c (3991 B, sha256 `16b4c868…6595a`) | **disagree (record, not decision)** | the source and the quote `args = g_list_append (args, g_file_new_for_commandline_arg (argv[i]));` at `:116` are real, so the admit decision is sound — but **no S532 row exists** in `corpus/SOURCES.md` (last row S531; census 466 = 462+4; the report itself says four rows) while the lesson lists it and `PROVINCE.md` cites "S528-S532" |

Newly written `SOURCES.md` rows re-opened for the ≤25-word quote rule: S528 (`/* If there is no macro
default to %f. This is also what KDE does */`, 15 words, `:2738`), S529 (`We always use single quotes,
because the algorithm is cheesier.`, 10 words, `gshell.c:202`), S530 (`Arguments may be quoted in
whole. If an argument contains a reserved character the argument must be quoted.`, 18 words), S531
(`Launch a desktop file from any location given.`, 8 words, `gio.1:221`). All four quotes are located
and within the word limit; all four digests match the fetched bytes.

## 4. Trend verdicts

- **expansion — improved.** 118 → 119 admitted knowledge entries and 462 → 466 registry rows; four
  new tier-A `mined` rows (S528-S531); the entry is on ground the coverage map did not hold (base: no
  lane tool answers a launch argv; the frontier bullet named launch); the SCORECARD capability row
  enters with the demonstrated run. Re-derived from committed bytes.
- **quality — improved.** C1 replaces "no lane tool answers a launch argv" with a measured sequence
  model behind 88 frozen cases / 20 classes / 79 mutants / a seeded fresh leg / three controls
  (naive 4/88, field-code 47/88, memoriser 0/60 fresh). C2 replaces "no read-back" with a gate, five
  planted controls and a 21-path repair. The harm watch replays the prior instruments. The record
  defects below are routed, not hidden.
- **discernment — improved.** Twelve mistakes are mined with witnesses (M98-1…M98-12, including the
  oracle's shared-file race, the counter/oracle materialisation drift, a label that could not be
  materialised, the launch-order race and the declaration's `%i` guard); the wave reversed seven of
  the L1's own sentences before the freeze; the fresh leg caught the file-URI encoding gap. The
  outside spot-check agrees on all six sampled gate decisions (two admits, four rejects) re-opened
  above; the seventh item (S532) is a landing defect, not a decision disagreement, and is routed.

## 5. Routed defects (status-neutral; the lane fixes them next round)

1. **S532 has no registry row.** The round lesson's `## Gate` table lists S532
   (`gio-tool-launch.c`, `:116`, sha256 `16b4c868…`) and the Candidates table admits "S528-S532", and
   `PROVINCE.md` cites "(S528-S532)", but `corpus/SOURCES.md` ends at S531 (466 = 462+4; the report
   says four rows). Add the S532 row (tier A, `mined`, `used-by` the entry) or correct the lesson and
   `PROVINCE.md` to S528-S531 — append-only, next round.
2. **The "466 rows / 119 entries" numbers are not the measured state.** The report, `SCORECARD.md`
   and `LOG.md` say the gate is green at 466/119; the measured revision `a3471631` has 462/118
   (`receipts/c2-measured-r98.txt`, `w1/R98MExecGate.md`). The 466/119 state (`020af865`+) was never
   gated with committed evidence. Re-run the gate at the records tip and commit the receipt, or
   correct the numbers.
3. **`SKILL.md`'s `mado-r98-execargv` row carries stale pins.** It pins `--expect-tool-sha256
   acfcc4f7…` and `--expect-mutants-sha256 5f074f70…`, the pre-re-freeze values; the committed tool
   and mutants are `49f7fecd…` and `32c207b3…`. A reader running the registry command hits
   SETUP_ERROR. Update the row to the freeze block's pins.
4. **`LOG.md` round-98 entry disagrees with its own receipts.** The fresh seed is
   `e2bf4d1b757e2e7b`, but the receipt and the report say `f00d3edcdb285ac0`; the entry says
   "Mistakes M98-1..M98-6" while the lesson holds M98-1…M98-12. Append a correction entry.
5. **The harm watch omits the round-97 counters.** The final 26 legs omit `r97c1_filetype` and
   `r97c2_counter_selftest` (both in the 28-leg first run `harm-base-r98.txt`); the report's
   "round-97 leg set replayed at the records tip" overstates. Replay them with a filled
   `SKILL-AT-MEASURED-REV`, or state why they are not replayable.
6. **M98-1's captured-by is `none`, but no `QUALITY.md` criterion cites the lesson.** `LEARNING.md`
   requires a criterion citing the lesson when no criterion caught a mistake. Add one next round, or
   cite the existing criterion that covers the class.
7. **Report ordering and in-place rewrite.** The first report commit (`30ac2607`, 17:52:03) preceded
   the lane tip (`6f61eff0`, 17:52:29); the filed bytes were rewritten in three later commits without
   an erratum (recurrence of the r97 spot-check's D1 in-place-rewrite half). Land the report after
   the tip and use an erratum for corrections.
8. **Loose commit attribution in the C2 prose.** The report's "21-cell repair … commit `06b6bf2a` …
   plus S504/S506/S527 gaining the C1 entry" conflates the 16-cell/21-path repair at `06b6bf2a` with
   the S504/S506/S527 additions at `020af865` (with the entry). The Landed-changes table is right;
   the prose should name both commits.

## 6. Operator notes (not lane defects)

- **SHONEN.** All four boxes look checkable by a non-author from committed evidence: box 1 by the
  `SKILL.md` registry rows (`:2979-2982`) and the entry's tables; box 2 by the C1 measured run and
  its receipt; box 3 by the entry's commands and the counter CLI; box 4 by the connector's 20-lane
  `PROVINCE.md` sweep — but that seat is the lane's own work, so outside-lane independence is still
  not established. Promotion is operator-owned; the lane filed `[~]` only and wrote no `[x]`.
- The round's instrument bytes are unchanged from `a3471631` to `6f61eff0` (tool `49f7fecd…`, gate
  `f1000bf1…`); the registry changed after the measured revision (the entry and its three `used-by`
  cells at `020af865`), which is the source of the 466/119 defect above.
- The claims reproduce at their landing revisions; the defects above are record/registry defects,
  not claim failures.
