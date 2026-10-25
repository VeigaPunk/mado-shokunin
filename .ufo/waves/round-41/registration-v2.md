# mado round 41 — registration v2 (re-registration, frozen before any round-41 data)

Supersedes the predicates and the shape line of `registration.md` (freeze `60c3914154333180450d5da27ba222d5763cc56a`, base
`ab2bfaab661c846d1de9d58c01651cd156a13949`); the claims, their axes and the base are unchanged. Wave `w1` (34 seats, spec/dispatch
`cd950ec781149040cc73d71cd67c2b67452e7724`) falsified the v1 predicates **before any data commit** — no `tools/mado-globals.py`, no entry, no
registry row, no lane `corpus/lessons/round-41.md` had landed. The v1 counters stay in the tree as the superseded predicates; the claims bind
to the v2 predicates below, committed (with their controls, their reference and the receipts of those controls) in the v2 freeze, before the
data commits. Honest ordering: the v1 predicates were scored by w1 seats (`CritC1Cheat`, `ExecToolIndep`, `ExecC1ExtraMutants`, `ExecC2ExtraMutants`,
`CritC2Cheat`), so v2 was written after seats had seen v1 scores; v2 is strictly stronger than v1 on every point it touches (nothing
loosened except the b2 sample's name-substring exclusion, replaced by an exact one), and the operator rules which predicate binds - the report
gives both scores at the data tip.

**Shape (corrects `registration.md` line 4).** Two v1 waves: `w1` of 34 seats (build + first falsifiers, policy v1 band 32-64) and `w2` of
34 seats (falsify, dispatched after the data commit), round total 68, no residual call. The §3 planner seat is held by the L1.

## What the wave found, and where each finding is closed

| Finding (seat, report) | v1 consequence | v2 change |
|---|---|---|
| `CritC1Cheat` CH1/CH2, `RevC1Counter` 3: the live stub payload was base64 inside a readable script and a plaintext `journal.txt` sat beside it | live fixtures passed without running the program (24/24) | the program is a compiled execute-only (0111) ELF built per fixture (the tool cannot read it), no copy of the journal on disk, and it records `ran`; an unusable program must not have run |
| `CritC1Cheat` CH6/CH9, `RevC1Counter` 1: b2 satisfied by a path test (`mut<i>/`) or by a self-fingerprint | 6/6 mutants "killed" without a test | mutants run at the real tool's layout (opaque parent, `tool/`); new clause **b3**: the tool with a trailing comment, and `ast.unparse` plus one assignment, must still pass its selftest in full |
| `CritC1Cheat` CH10: b2 sample aimed away from the parser by renaming into `_run*`/`_check*` | b2 said nothing about the model | exclusion by exact function name (`selftest`, `main`, `usage`, and functions inside `selftest`); one of the six sites is forced into the function holding the final-line text and must be killed; kill counts `k != n` |
| `CritC1Cheat` CH8, `RevC1Counter` 2: clause g evaded by `getattr`, `**{}`, `globals()["eval"]` | g was not a guarantee | g denies `getattr/setattr/delattr/vars/globals/locals/breakpoint`, any `**` call unpacking, `__file__`, `sys.argv[0]`, `sys.executable`, `sys.modules`, string constants equal to `exec/eval/compile/__import__/system/popen/builtins/__builtins__/__file__` |
| `CritC1Cheat` CH4: a child interpreter did the work in `--journal-file` mode | invisible to g and to the PATH stub | file-mode runs execute under `RLIMIT_NPROC = 1` (`prlimit --nproc=1:1`): any spawn fails |
| `CritC1Cheat` CH3: NAME rule `\w` coincided on all fixtures | 24/24 | fixture `unicodename0` (valid UTF-8 non-ASCII name) and ASCII digit classes (`[0-9]`) in the contract |
| `RevC1Counter` 4/5: fixture identity learnable from directory names | fixed fixtures collapse to a lookup | opaque per-run directory names; sandbox detectability declared as a residual |
| `ExecC1ExtraMutants`: 13 of 42 further mutants survived | blind value domains | fixtures `vernum0`, `hostbyte0`, `levelcase0`, `expectlatest0`, `sortclass0`, `pidzeros0`, `bootpersist0`, `asciidigits0`, `unicodename0`; `livehang0` (N42) |
| `ExecDiffFuzz` (`ascii-digits`, `str-max`, `int-pid` variants scored 24/24) | contract under-determined | contract text: ASCII digits, numeric version max, PID as a string; the same fixtures |
| `ExecJournalFormat`: 5 of 6 `-o` formats gave a silent `NO_SESSIONS` on a file holding 78 adverts | a check that never ran looked clean | new `ignored=` field and verdict `UNRECOGNIZED_FORMAT` (exit 4); fixtures `unrec0`, `mixed0` |
| `RevRefTool` M1/M2: a FIFO as `--journal-file` hung; live output buffered whole | hang, 615 MB RSS | regular-file requirement (`O_NONBLOCK` open + `fstat`); incremental bounded read with a 30 s deadline; fixtures `fifo0`, `dir0`, `livehang0` |
| `RevC1Counter` 6, 8: no fixture for "not on PATH", for "the program is not run", a missing `bwrap` crashed the counter | docstring sentences unexercised | `livenopath0`, the `ran` record, `Setup` for a missing `bwrap`/`prlimit`/`gcc` |
| `CritC2Cheat` F1-F7, `RevC2Counter` H1-H4/M1-M5, `ExecC2ExtraMutants` (29 survivors) | nine forgeries and 29 mutants admitted | C2 v2: PINS (receipts of NEW ids are the pre-wave fetches, byte for byte), mode 100644, window-wide header rules and ghost-id refusal, calendar-valid `recheck`, location present and bound to the receipt name, held rows keep their used-by items, >= 3 new ids, quote exclusivity across cited receipts, one cited id per entry line, unfenced lesson, journal provenance floor (boot line, ascending distinct session starts), STAGED allowlist for ADMIT/REFUSE, REFUSE reason of >= 4 distinct words, localized markers over the whole row |

## Claims (unchanged in substance)

- **C1 — operability (capability acquisition): `tools/mado-globals.py`.**
  - **Predicate `PRED-C1-r41-v2`:** the docstring of `quality/counters/c1-r41-globals-v2.py` (the code is the same sentence): 39 fixtures + clauses a, b, b2, b3, g.
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r41-globals-v2.py --repo . --rev <rev>` (fresh nonce per run, replayable with `--nonce`).
  - **Before** (base): `fixtures=0/39 tool=absent verdict=TARGET_MISSED`, exit 1 (`receipts/c1-v2-before-base.txt`).
  - **Target:** `fixtures=39/39 tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the tip. **Kill rule:** anything else at the data tip is a miss, reported as an honest stop; no narrowing.
- **C2 — coverage (sourced): `corpus/knowledge/hyprland-focus-grab-r41.md`.**
  - **Predicate `PRED-C2-r41-v2`:** the docstring of `quality/counters/c2-r41-focus-entry-v2.py` (clauses a-i, PINS, STAGED).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo . --rev <rev>`.
  - **Before:** `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-v2-before-base.txt`).
  - **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0. **Kill rule:** as C1.
- **Separability** is unchanged: C1 reads only `tools/mado-globals.py`; C2 reads only the entry, registry, lesson, README and the pinned receipts (its journal is parsed by its own parser).

## Controls (committed receipts at this freeze)

- **C1:** `receipts/ctl-c1-v2.txt` — `CTL_C1V2`: the reference (`c1/ctl-ref-tool-v2.py.txt`) reaches TARGET_MET; three do-nothing controls, the v1 single-defect mutants (patterns re-derived for v2), ten v2 cheats (`K01-K10`: stub bytes read, cwd replay, `\w` names, child interpreter, `argv[0]` path test, `eval` via `getattr`, size fingerprint, kwargs unpacking, `globals()`, `__file__`) and the 42 `ExecC1ExtraMutants` mutants each score below MET.
- **C2:** `receipts/ctl-c2-v2.txt` — `CTL_C2V2`: control P (genuine pre-wave receipts, a fabricated-but-pinned set is the declared residual) is admitted under the real and the pin-patched counter; every other control scores `0/1` (forgeries under the real counter, clause mutants under a counter whose PINS also hold the fixture's receipts, so each is killed by its own clause).
- `receipts/freeze-counter-check-v2.txt` — criterion 64: every counter/checker path this file names exists at the v2 freeze.

## Residuals (declared)

- C1: a tool that **contains** the reference parser and table is an implementation; clause g is a heuristic over names; the sandbox is detectable; the judge's live program is unreadable but the tool could pass the live fixtures by running it and then reproducing the model. The host receipt (`--live`) is reported, not scored.
- C2: the pins are the trust root; a real receipt can be cited for a claim it does not support (the non-author closure's job); a held id's receipt is not pinned.
- A second falsification wave `w2` attacks both v2 predicates and the landed data; if it finds a hole the L1 reports it as an open defect of the predicate (no third registration after data).
