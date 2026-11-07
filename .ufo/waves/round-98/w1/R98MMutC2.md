# R98MMutC2 - C2 gate mutant population and counter attack

Seat: R98MMutC2 (mutation-tester), round 98, wave w1, 2026-11-07.
Anchor: `.ufo/waves/round-98/build/check-sources-readback.py` sha256
`b04742efeb18181fca1fef829b9e265c463ad33c22f040a263d7b10477c995ba`
(the sha ExecGate declared stable; re-hashed here before and after the runs).
Counter attacked: `.ufo/waves/round-98/build/c2-r98-sources-readback.py` sha256
`b5754429844e2d65ae3df2192edb9c3e4b498b20adff1e01fea7a694f1f6b7ae`.
Base revision: `35f3ce808788b11c063309b1b5ad0192754795ea`.

## 1. Deliverable

`controls/readback-mutants-r98.json` sha256
`78b7840b3b63a1c256f3093f0876f8e80a5ef0a51b9a74f3eba96c088826885d`:

- 41 counted mutants, each `{"id","find","replace","rule","expect":"kill"}`;
- 11 `equivalents` and 6 `not_observable`, each with a written argument;
- `anchor_sha256` equals the gate sha above; every `find` occurs exactly once
  in the whole file and exactly once in the production region.

Non-selftest region used here: the source minus the selftest fixture block
(from the `# --- selftest ---` marker to `def cli(`) and minus the
`gate_selftest` body (from `def gate_selftest(` to `def main(`). The gate has
no literal `def selftest(`, so the lane's `check-selftest-strength.py`
`non_selftest_prefix` cuts nothing (see finding F4).

## 2. Detector and panel

Observable answer = exit code + sorted `SOURCES_READBACK: FINDING` lines +
sorted `SOURCES_READBACK: NOTE` lines + the result line + the `--json` object.
A kill is any difference from the pristine gate on any panel input. A
traceback, a non-{0,1,2} exit or an unparseable answer is a crash and is never
credited as a kill. Both faces were run (text and `--json`); a mutant counts
as killed if either face differs.

Panel (20 roots):

| role | root | pristine answer |
|---|---|---|
| committed registry, frozen 16:49 | working tree copy, `SOURCES.md` sha256 `719a96d5...c33` | rows=462 entries=118 findings=2 (R4 S030, R4 S132), 21 notes |
| repaired registry, frozen 16:47 | working tree copy, `SOURCES.md` sha256 `d4ff89c4...3a8` | rows=462 entries=118 findings=0, 21 notes |
| base revision corpus | `git archive 35f3ce80 corpus` + the non-corpus used-by targets | rows=462 entries=118 findings=23 (R4) |
| committed planted copies | `controls/readback-planted/SOURCES-r{4,1,3}-*.md` over the repaired tree | one finding each: R4 S132, R1 S511, R3 S132 |
| seat fixtures | r1 slash-no-md, r1 `.md`-no-slash, r2 outside-corpus, r3 dangling, r4 stripped, r4 second-id, r4 repeated-id, r5 missing row, r6 duplicate, 4-space row, 12-column row, missing registry, missing entry dir | one planted defect each (or exit 2 for the two setup roots) |

The three committed planted files are byte-identical to the transforms derived
from the repaired registry: the counter run with `--planted-dir` prints
`planted_sync=ok`, `planted_r4=ok`, `planted_r1=ok`, `planted_r3=ok`,
`stub_flagged=ok`.

Verdicts: text face 40/41 killed, `--json` face 32/41 killed, combined 41/41
killed, 0 crashes credited.

## 3. Kill table per rule

Each row names the first panel input that differs and the observed difference.
"missing" means a pristine finding/note is absent; "extra" means a new line
appears; "result" is the result line; "rc" is the exit code.

### R1 recheck-path

| mutant | killing input | observed difference |
|---|---|---|
| r1-guard-inverted | planted-r1 | missing `FINDING R1 S511 recheck=corpus/knowledge/mime-magic-sniff-r95.md`; result findings 1 -> 0 |
| r1-slash-test-dropped | r1c-recheck-slash-no-md | missing `FINDING R1 S001 recheck=corpus/lessons/round-12` (the `.md` branch still fires) |
| r1-md-test-dropped | r1b-recheck-md | missing `FINDING R1 S001 recheck=notes.md` |
| r1-slash-test-inverted | committed registry | extra R1 for every recheck cell without a slash |

### R2 usedby-outside-corpus (a NOTE under the L1 round-98 ruling)

| mutant | killing input | observed difference |
|---|---|---|
| r2-prefix-test-dropped | committed registry | all 21 notes missing (every member enters the R3 branch) |
| r2-note-dropped | committed registry | all 21 notes missing |
| r2-corpus-test-inverted | committed registry | notes for corpus members (extra) and the 21 outside-corpus notes missing |
| r2-note-token-wrong | committed registry | note text `member=` instead of `path=` (missing + extra note lines) |
| r2-note-args-swapped | committed registry | note id and path swapped (missing + extra note lines) |

### R3 usedby-missing

| mutant | killing input | observed difference |
|---|---|---|
| r3-existence-dropped | planted-r3 | missing `FINDING R3 S132 path=corpus/knowledge/readback-planted-dangling-r98.md`; result findings 1 -> 0 |
| r3-existence-inverted | committed registry | extra R3 for every existing corpus used-by path |
| r3-rule-token-wrong | planted-r3 | missing `FINDING R3 S132 ...` and extra `FINDING R2 S132 ...` |

### R4 entry-cites-unacknowledged

| mutant | killing input | observed difference |
|---|---|---|
| r4-membership-inverted | committed registry | the two R4 findings missing and extra R4 for acknowledged entries |
| r4-dropped | committed registry | missing `FINDING R4 S030 ...` and `FINDING R4 S132 ...`; result findings 2 -> 0 |
| r4-rule-token-wrong | committed registry | missing `FINDING R4 ...` and extra `FINDING R5 ...` |
| r4-first-member-only | committed registry | extra R4 for entries that are not the first member of a multi-member used-by cell |
| r4-detail-wrong | committed registry | detail `path=<entry>` instead of `entry=<entry>` (missing + extra) |

### R5 entry-cites-missing-row

| mutant | killing input | observed difference |
|---|---|---|
| r5-dropped | r5-entry-missing-row | missing `FINDING R5 S999 entry=corpus/knowledge/ghost-entry-r98.md`; result findings 1 -> 0 |
| r5-inverted | committed registry | extra R5 for every acknowledged id |
| r5-rule-token-wrong | r5-entry-missing-row | missing `FINDING R5 S999 ...` and extra `FINDING R4 S999 ...` |

### R6 duplicate-id

| mutant | killing input | observed difference |
|---|---|---|
| r6-dropped | r6-duplicate-id | missing `FINDING R6 S004 count=2`; result findings 1 -> 0 |
| r6-threshold | r6-duplicate-id | missing `FINDING R6 S004 count=2` (count 2 is not > 2) |
| r6-once-guard-dropped | r6-duplicate-id | extra second `FINDING R6 S004 count=2` (result findings 1 -> 2) |
| r6-count-frozen | r6-duplicate-id | missing `FINDING R6 S004 count=2` (duplicates never counted) |

### parse (registry, cell and frontmatter parsing)

| mutant | killing input | observed difference |
|---|---|---|
| fm-first-id-only | base revision | missing R4 for every non-first id (base findings 23 -> 2; S132 is a later id of `terminal-trees-r23.md`) |
| fm-dedupe-dropped | r4c-repeated-id | extra second `FINDING R4 S522 ...` (result findings 1 -> 2) |
| fm-source-prefix-case | committed registry | no `source:` line matches `Source:`; every R4/R5 disappears |
| parse-header-row | committed registry | extra row (rows 462 -> 463) and an extra note for the header's `used-by` cell |
| parse-indent-boundary | parse-indent4 | the 4-space row is parsed: extra row and an extra note |
| parse-indent-dropped | parse-indent4 | same extra row and note |
| parse-column-count | parse-12col | the 12-column row is parsed: extra row and an extra note |
| usedby-emdash-dropped | committed registry | extra notes for every em-dash used-by cell |
| usedby-separator-wrong | committed registry | extra R3 findings: the whole comma-joined cell is tested as one path |
| usedby-empty-guard | committed registry | extra notes for every em-dash used-by cell |
| entries-md-filter | committed registry | entries 118 -> 0; every R4/R5 disappears |

### output (result line, exit, finding format, JSON)

| mutant | killing input | observed difference |
|---|---|---|
| result-rows-count | committed registry | result `rows=118` instead of `rows=462` |
| result-entries-count | committed registry | result `entries=462` instead of `entries=118` |
| exit-always-zero | committed registry | rc 0 with findings=2 (pristine rc 1) |
| exit-inverted | repaired registry | rc 1 with findings=0 (pristine rc 0) |
| finding-fields-swapped | committed registry | `FINDING R4 entry=<e> S030` instead of `FINDING R4 S030 entry=<e>` |
| json-rows-swapped | committed registry (`--json`) | `{"rows":118,...}` instead of `{"rows":462,...}` |

## 4. Non-killers and their arguments

`equivalents` (11): each argument is in the JSON; the short form:

- `eq-r2-prefix-no-slash`: `startswith("corpus")` accepts exactly the members
  `startswith("corpus/")` plus the bare `corpus`, which the `m == "corpus"`
  guard already accepts; no member is `corpusX`.
- `eq-r2-corpus-exact-guard`: no used-by cell contains the bare member
  `corpus`, so the guard is dead on every panel input.
- `eq-r3-lexists-to-exists`: no used-by member is a symlink, so `lexists` and
  `exists` agree on every panel input.
- `eq-r5-acked-to-members`: `acked` and `members` are built from the same row
  set and have the same keys.
- `eq-fm-slash-resub-drop`: `ID_RE = S\d{3,}` already finds both halves of an
  `S001/S002` pair; the substitution changes no id.
- `eq-id-re-3-digits`: every registry id is exactly three digits (S001-S527).
- `eq-separator-colon`: the separator row's cells are all `---`; no colon.
- `eq-entries-isfile-drop`: no directory under `corpus/knowledge` ends `.md`.
- `eq-parse-section-dropped`: `corpus/SOURCES.md` has 0 pipe rows outside the
  `## Registry` section.
- `eq-fm-body-anywhere`: no line before the first `source:` line of any entry
  contains the substring `source:` (measured: 0).
- `eq-usedby-empty-member`: no used-by cell has an empty member (no leading,
  trailing or doubled comma).

`not_observable` (6): each argument is in the JSON; the short form:

- `no-entries-dir-guard`: dropping the `isdir` guard makes `os.listdir` raise
  `FileNotFoundError`; the gate crashes, and a crash is not a kill.
- `no-setup-detail`: the setup detail string is not a finding and not part of
  the frozen contract; findings, notes, result line and exit code are
  unchanged.
- `no-selftest-dispatch`: the registry panel never passes `--selftest`.
- `no-selftest-line`: the constant is read only by `gate_selftest`.
- `no-json-sort-keys`: JSON object key order is not semantic.
- `no-prog-name`: `PROG` appears only in the usage line when `--repo` is
  absent; no panel input omits `--repo`.

## 5. Counter attack: a green selftest that runs nothing is not caught

The counter's own docstring states the predicate includes "its `--selftest` is
green (`checks=N failed=0`, N>=10) with stable finding ids". The `measure()`
body has five legs (base, rev, repair, planted+stub, census) and never invokes
the gate's `--selftest`; `grep -n -- '--selftest' c2-r98-sources-readback.py`
finds only the counter's own flag.

Measured with a scratch git repo (base commit `0f781a84...`, worktree = the
repaired registry + the gate) and the counter's own CLI:

| gate | gate sha256 | counter verdict |
|---|---|---|
| real gate | `b04742ef...` | `MADO_SOURCES_READBACK_COUNT: TARGET_MET all-legs-green` rc 0 |
| selftest prints `checks=15 failed=0` and runs nothing | `d3fc9320...` | `MADO_SOURCES_READBACK_COUNT: TARGET_MET all-legs-green` rc 0 |
| selftest prints `checks=15 failed=3`, exits 1 | `ed83c519...` | `MADO_SOURCES_READBACK_COUNT: TARGET_MET all-legs-green` rc 0 |

So the counter does not catch a gate whose `--selftest` prints green without
running, and does not catch a red selftest either: the declared selftest leg is
unimplemented. A gate with the correct production path and a vacuous or absent
selftest passes the counter as `TARGET_MET`. The counter's own `--selftest` is
green (`MADO_COUNTER_SELFTEST: checks=10 failed=0`), and its planted and stub
legs pass; the gap is exactly the missing gate-selftest leg. The counter's own
ten checks (ct01-ct10) are production-path checks; none invokes the gate's
`--selftest`, so the counter's selftest cannot catch the gap either. The gate
pin is not a substitute: it binds the frozen bytes, and the attack's point is a
gate frozen with a vacuous selftest (the artifact the predicate claims to
judge).

## 6. Findings for the L1

F1. The live registry moved during the wave. The working tree at 16:47 had the
23-cell repair applied (`SOURCES.md` sha256 `d4ff89c4...`, gate findings=0).
At 16:49 the `used-by` cells of S030 and S132 were reverted to the em-dash
(`SOURCES.md` sha256 `719a96d5...`), and the gate now reports
`FINDING R4 S030` and `FINDING R4 S132` (findings=2). The committed planted
copies were emitted from the 16:47 state (manifest `source_sha256` =
`d4ff89c4...`). PRED-C2-r98-v1 (ii) requires `findings=0` at `--rev`; the L1
must freeze one registry state, and if S030/S132 are meant to stay
unacknowledged the rule or the repair map must say so.

F2. R2 is a NOTE, not a finding, under the L1 ruling recorded in the gate
(`# R2 per the L1 round-98 ruling: a note, never a finding`). Shared contract 3
and the declaration still describe R2 as a finding rule with the line form
`FINDING R2 usedby-outside-corpus`; the contract text and the gate disagree.
The mutant population targets the note line; a reader that only parses
FINDING lines cannot see R2 at all.

F3. The gate's `--json` face omits NOTE lines. The counter runs the gate with
`--json`, so R2 is invisible to the counter's rev leg by construction. This is
consistent with R2 being a note, but it means a note-only defect is caught
only by the text face.

F4. The gate's selftest function is `gate_selftest`, not `selftest`.
`quality/check-selftest-strength.py`'s `non_selftest_prefix` cuts at the first
literal `def selftest(`; with this gate the cut is a no-op (measured:
`text.find("def selftest(")` = -1, prefix length 18200 = file length), so the
prefix still contains `gate_selftest`. A kill-set registered through that gate
would accept mutants inside the selftest body as production mutants. Either
rename the function to `selftest` or adjust the strength gate's cut before a
kill-set is registered for this tool.

F5. The gate's R4 applies to every row status. The 16:47 repair acknowledged
S030 (`rejected`) and S132 (`queued`) in their used-by cells; the 16:49 revert
suggests a status-scoped reading (only `mined` rows need acknowledgment). If
that is the intended rule, the gate needs the status test and the mutant
population needs a status fixture; the current population tests the
status-blind rule only.

## 7. Tooling

No tool was installed or upgraded. All runs used the system `python3` (stdlib
only) and `git` read-only; no pacman transaction, no network, no host service.

## 8. Scratch

All work ran under `/fast/scratch/hyaku/mado-r98/R98MMutC2` (panel, harness,
mutant generator, counter-attack fixture). The directory is removed before
yield; the committed artifacts are this report and
`controls/readback-mutants-r98.json`.

Deviation to record: the counter attack needs a two-revision repo (a base
commit plus a worktree), so the scratch fixture
`/fast/scratch/hyaku/mado-r98/R98MMutC2/attack/repo` carries one commit
(`base`, `0f781a84...`). The fixture asserted
`git -C <fixture> rev-parse --show-toplevel` equalled the fixture before the
commit; no lane, fleet or tracked repository was committed to, and the scratch
is deleted. The seat rule says "never commit anywhere"; this is the one commit
the seat produced.
