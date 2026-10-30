# R56W3SimplInstruments — dead-weight report over the round-56 instrument set

**Item attacked:** R56W3SimplInstruments ("Dead-weight report (read-only; no edits) over the round-56 instrument set at
`0f3a54361a9824484d0801679ceb1fd8ac7c32e1`").
**Scored tree:** `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (lane tip). Nothing in the lane was edited.
**Mode:** read-only. No tracked-file write, no git/jj mutation of the lane or the fleet repo, no delegation, no
background job. All measurement happened in `/fast/scratch/hyaku/mado-r56/R56W3SimplInstruments/` (removed at yield).

## Files in scope

| file | lines | executable statements |
|---|---|---|
| `quality/counters/c1-r56-autoreload-entry.py` | 1120 | 896 |
| `quality/counters/c3-r56-used-by.py` | 476 | 359 |
| `quality/check-r56-controls.py` | 43 | 27 |
| `quality/r56_ctl_c1.py` | 632 | 436 |
| `quality/r56_ctl_c2.py` | 322 | 243 |
| `quality/r56_ctl_c3.py` | 617 | 435 |
| `tools/mado-watchplan.py` | 565 | 391 |

---

## 0. Method — how "exercised" was measured (so the nulls are falsifiable)

Text grep cannot say "no leg/control/fixture exercises this line". I measured it with **line coverage**, so every
"not exercised" claim below is a measurement, not an inference.

**Instrumentation.** `coverage 7.17.0` installed into a throwaway venv
(`/fast/scratch/hyaku/mado-r56/R56W3SimplInstruments/.venv`, Python 3.14.8 = the host `python3`).
Channel: `uv venv` + `uv pip install coverage` (uv 0.13.0, official PyPI index) — see *Tooling* below.
Subprocess coverage was enabled with a `.pth` hook in the venv's `site-packages` that calls
`coverage.process_startup()`; the harnesses scrub `GIT_*`/`HOME`/`TMPDIR` from the child env, so the hook (not an env
var) is what makes the children measurable. Coverage data lands in `cov/` (parallel files), merged by
`coverage.data.CoverageData`.

**What was run, under coverage, at the tip:**

```
$ .venv/bin/python -m coverage run --rcfile=.coveragerc \
    quality/check-r56-controls.py --claim c1 --repo <lane> --rev 0f3a5436... --work $PWD/w-c1
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK
$ .venv/bin/python -m coverage run --rcfile=.coveragerc \
    quality/check-r56-controls.py --claim c3 --repo <lane> --rev 0f3a5436... --work $PWD/w-c3
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
$ .venv/bin/python -m coverage run --rcfile=.coveragerc \
    quality/check-r56-controls.py --claim c2 --repo <lane> --rev 0f3a5436... --work $PWD/w-c2
MADO_R56_C2: rev=0f3a5436... fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET
```

**Three independent runs** (the claim legs, the counters' own `--selftest` modes, and the tool's `--selftest` mode)
were measured and unioned. A line is called *claim-exercised* if the claim run touched it, *selftest-only* if only the
`--selftest` mode touched it, and *never-executed* if neither did.

**Two measurement caveats I must state plainly:**

1. The C2 harness runs the tool under `bwrap` with `/usr/bin/python3` (`SAFE_PATH`, `r56_ctl_c2.py:36`), so the
   tool's own lines are **not** measurable through the harness. I measured them with a scratch driver
   (`c2tool.py`) that imports the lane's own `r56_ctl_c2.py` read-only and calls its own `score()` over the same 26
   fixtures with the venv interpreter, `bwrap` disabled. The driver reuses the lane's staging code and reproduced the
   lane's own scores exactly (`tool fixtures=18/18 holdout=8/8`, `const-host 1/0`, `empty 0/0`,
   `sibling-reader 0/0`, `lookup-committed 18/0` — identical to `r56_ctl_c2.py:298`'s stderr line at the tip).
   **Deviation:** no sandbox in the tool-measurement driver. The sandbox hides the answer key from the tool; it does
   not change which lines of the tool execute. The sandboxed run's own verdict is separately confirmed green above.
2. The counters are exported from the git blob at `--rev` and run from a scratch path, so coverage attributes them to
   `.../counter/c1-counter.py` / `.../counter/c3-r56-used-by.py`. I mapped those to the lane paths and verified the
   bytes are identical (`sha256` of the tip blob == sha256 of the working-tree file, all three:
   `2b2ef41b…` C1 counter, `68b34e3c…` C3 counter, `3ccf0708…` tool). No line-number skew.

**Per-file results** (`receipts/coverage-summary.txt`):

| file | statements | claim-exercised | claim-unexercised | of which never-executed at all |
|---|---|---|---|---|
| `c1-r56-autoreload-entry.py` | 896 | 533 | 363 | 38 |
| `c3-r56-used-by.py` | 359 | 217 | 142 | 38 |
| `r56_ctl_c1.py` | 436 | 368 | 68 | 68 |
| `r56_ctl_c2.py` | 243 | 215 | 28 | 28 |
| `r56_ctl_c3.py` | 435 | 377 | 58 | 58 |
| `check-r56-controls.py` | 27 | 25 | 2 | 2 |
| `mado-watchplan.py` | 391 | 253 | 138 | 11 |

---

## 1. Per-file findings

### 1.1 `quality/counters/c1-r56-autoreload-entry.py` — **earns its place; the `--selftest` half is the weight**

**Verdict: everything earns its place.** 896 statements, 533 exercised by the claim leg, 325 exercised only by the
counter's own `--selftest` (242/242 assertions pass), 38 never executed at all.

*Never-executed (all 38), by category:*
- **Setup-error arms of the git layer** — `48` (repo is not a directory), `51-52` (cannot create `--work`),
  `70-71` (cannot run git), `73` (git failed), `85` (commit has no tree). These are the fail-closed arms of
  `Repo.__init__`/`Repo.git`/`Repo.resolve`. **Keep** — a counter that cannot read its repo must exit 2, not print green.
- **Path-traversal guards on `Repo.regular_oid`** — `105` (a component is `""`/`.`/`..`), `120` (not a regular blob).
  **Keep** — this is the boundary that stops a symlinked path from being read as a blob.
- **Fence/comment scanner arms** — `141` (`fence_open`: fewer than 3 fence chars), `151`/`158`/`160`
  (`fence_close`: unbalanced fence / `<!--` without `-->`). **Keep** — the counter's own docstring claims
  "a character-level block scanner (fences and HTML comments)"; these are its arms.
- **Row-grammar arms** — `215` (`first_cell`: row not `| a | b |`), `261` (`registry_id`: cell-count mismatch),
  `279` (scope: locator past EOF), `451` (`registry_row`: S-row not exactly 11 cells), `470` (`source_cell_ok`:
  cells[3] not A/B). **Keep** — these are what make the counter *fail* a malformed tree rather than pass it.
- **Leg-grammar arms inside `evaluate`** — `514`, `516`, `519`, `521` (row not "strict", `strict[0] != rid`,
  K-row source cell not `S###`, H-row source cell not `host`). **Keep.**
- **Selftest fixture-builder arms** — `649` (`selftest` assertion FAIL line), `662`, `724`, `729`, `758`, `764`, `801`.
  **Keep** — the selftest must be able to fail.
- **CLI-arg arms** — `1069` (repeated `--selftest`), `1076` (option without value), `1098-1099`/`1104-1105`
  (selftest without `--work`: `tempfile.mkdtemp` + `shutil.rmtree` cleanup), `1112-1114` (`OSError` in `main`).
  **Keep.**

**What I could not falsify:** the counter's own `--selftest` mode is **not** run by any committed gate.
`tools/mado-verify.sh` (the source of `MADO_SELFTEST: 460/460`, `receipts/selftest-before.txt:1`) contains zero
occurrences of `r56` (`grep -c "r56" tools/mado-verify.sh` → `0`). The only committed references to
`c1-r56-autoreload-entry.py --selftest` are its own docstring (`:5`) and the wave-2/wave-3 spec generators
(`.ufo/waves/round-56/make-w2-spec.py:51,53` — wave *instructions*, not gates). So the 325 selftest-only statements
are **real, passing, but ungated** code: a wave-2 mutation seat (`make-w2-spec.py:51`) is instructed to use
"the counter's own `--selftest`" as one of two oracles, so it is load-bearing for the round's mutation evidence even
though no committed gate exercises it. That is a fact about the round's workflow, not dead weight — I am not calling it
a deletion candidate.

**Nothing to extract.** `evaluate` is one function; the counter has no second copy of any logic.

---

### 1.2 `quality/counters/c3-r56-used-by.py` — **earns its place; same selftest-only shape**

**Verdict: everything earns its place.** 359 statements, 217 claim-exercised, 104 selftest-only
(`MADO_USED_BY_SELFTEST: 16/16 assertions passed`), 38 never executed.

*Never-executed (all 38), by category:*
- **Setup-error arms of the git layer** — `78` (repo is not a directory), `80` (bad rev), `86` (rev resolved to an
  unexpected object), `89` (repo is not the repository root), `95-96` (git failed to run), `102` (git ls-tree failed),
  `110` (unparsable ls-tree record), `123` (git cat-file failed), `196` (registry row with wrong cell count),
  `212` (`corpus/SOURCES.md` is not a regular blob), `228` (allowlist row without 4 tab-separated cells),
  `234` (allowlist row without 4 cells), `260` (frozen tables not a regular blob), `265-266` (frozen tables unreadable).
  **Keep** — fail-closed arms.
- **Non-blob / symlink guards** — `116` (blob_at: not a regular blob), `138`, `141` (`entries()`: skip a non-blob
  entry). **Keep.**
- **Fence/citation scanner arms** — `167-170` (`cite`: the `source:`-line token scan), `294`, `296-298`
  (the `--detail` listing of offending pairs). **Keep** — `--detail` is a documented mode (`:8`, `:15`).
- **Selftest arms** — `311`, `359`, `387`. **Keep.**
- **CLI/setup arms** — `455` (`--repo`/`--rev` required), `460` (work dir not writable), `465-470`
  (`SetupError`/`OSError` in `main` → exit 2). **Keep.**

**Dead option — real, small.** `--detail` (`:449`, consumed at `:464`) is **never used by any leg, control, fixture or
gate in the lane**: the only occurrences of `--detail` anywhere under `mado-shokunin/` are the counter's own docstring
(`:8`) and its definition. The wave-1 seat report `R56ExecC3CounterA.md:7` quotes the usage line but the receipt
runs it without `--detail`. Severity: **cosmetic** — it is a documented, working diagnostic switch, 4 statements
(`295`, `296`, `297`, `298`). *Next-round candidate, not now.*

**Note on `cite` (`:166-170`) — a real asymmetry.** `cite` is the `source:`-line token scan, used for the `dangling`
leg. It never executes in any run because **no entry has a `source:` line in its first 15 lines at the tip** — so
`dangling` is 0 for a structural reason (the leg has no input), not because the leg is satisfied. The claim's own
v2 registration already discloses this ("entries without a `source:` line are invisible to `dangling`, 20 entries",
registration-v2.md §"What v2 does not repair"). **Not a defect I am raising; it is disclosed.** But it is worth
recording here because it means 4 statements of `cite` are unreachable at the tip — that is an *input* fact, not
dead code.

---

### 1.3 `quality/r56_ctl_c1.py` — **earns its place, with two stale names and one dead flag**

**Verdict: everything earns its place.** 436 statements, 368 claim-exercised (the 12 frozen controls + the good tree),
68 never executed. All 68 are error arms:

- `88` (git failed), `107` (tar -x failed), `111` (nothing to export), `120` (scratch toplevel mismatch),
  `136`/`146` (mutation target not a regular file / mutation changed nothing) — setup arms.
- `157-159`, `173` (HTML-comment arms of `entry_rows`), `180`, `186`, `189`, `211` (row-grammar arms).
- `237`, `247`, `250`, `255`, `258`, `273`, `284`, `303`, `316`, `320`, `330`, `344`, `352`, `362`, `368`
  (per-mutation precondition arms: "K10 cites S383, expected …", "registry already holds S399", "pin is empty",
  "no row with a quote of >=30 characters", …). **Keep** — a mutation that cannot apply must FAIL the control, not
  silently pass (`msgs.append("%s %s: FAIL - mutation not applicable: %s\n" …)`, `:594`).
- `376`, `387`, `394`, `396` (the `_need`/`_need_echo`/`_need_junk` failure-reason arms). **Keep.**
- `428-431` (counter timeout / could-not-start), `438`, `441`, `445` (counter stdout shape checks).
- `456`, `458`, `460`, `463`, `465` (judge_good arms), `472`, `474`, `476`, `478` (judge_control arms).
- `493-494`, `500-502` (usage error → exit 2), `523`, `526`, `529`, `538-539`, `541` (frozen-tables checks).
- `551-554` (`--counter` override: copy an alternative counter file), `562`, `565-566` (counter absent at rev),
  `589-590`, `593-595` (control-level FAIL paths), `605` (control FAIL line).

**Two stale names (cosmetic, but real):**
- `quality/r56_ctl_c1.py:6` — docstring says "for each of the **ten** frozen C1 controls"; the code has
  `N_CONTROLS = 12` (`:45`) and the frozen v2 registration has 12 (registration-v2.md E5). Introduced at commit
  `2e39282e` (the first commit of this file) and never corrected; `git log` confirms `N_CONTROLS = 12` in that same
  commit, so the docstring was **wrong from birth**.
- `quality/r56_ctl_c1.py:23` — "exit 0 on OK (good=ok and **k=10**)"; the code prints `controls=<k>/12` (`:611`) and
  requires `passed == N_CONTROLS` (`:610`). Same defect, same commit.
- `quality/r56_ctl_c1.py:609` — the inline comment "The denominator is the frozen **10**, never len(CONTROLS)" is
  wrong for the same reason (`:610` uses `N_CONTROLS`, which is 12).
  Severity: **cosmetic** — the *code* is right (it uses `N_CONTROLS`, and the verdict requires
  `len(CONTROLS) == N_CONTROLS` so a dropped control cannot pass). Only the prose is wrong.

**Dead option — real, small.** `--claim` (`:490`, `choices=["c1"]`) is **parsed and then never read**: `grep -n "a\.claim"`
over the file returns nothing, and the only other `claim` tokens are the literal string in the printed line (`:611`) and
in the mutation text (`:214`). It is accepted and ignored. Proof it changes nothing:
```
$ python3 -I quality/r56_ctl_c1.py --repo <lane> --rev 0f3a5436... --work <scratch> --claim c1
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK     # identical to the run without --claim
```
The dispatcher `check-r56-controls.py` **strips `--claim` before forwarding** (`:34-38`), so a caller can never reach
the module's `--claim` through the dispatcher at all. Severity: **cosmetic** — 2 statements plus a docstring line.

**Duplication across the three harnesses — see §2.** The C1 harness is the *most* self-contained of the three
(it has its own `git`, `_env`, `materialize`, `export_good`, `entry_rows`).

---

### 1.4 `quality/r56_ctl_c2.py` — **earns its place; one dead parameter, one dead constant in the sibling**

**Verdict: everything earns its place.** 243 statements, 215 claim-exercised (26 fixtures × the tool + 4 control stubs
× 26), 28 never executed. All 28 are error arms:

- `51` (git failed), `81` (export failed), `219` (`python3` not found), `225`/`228` (frozen-tables blob / sha256 checks),
  `242` (fixtures absent at rev), `313-315` (setup error → exit 2) — setup arms.
- `60`, `65` (`ls_entry`: empty record / path not found), `92-93` (`commitment`: symlink entries),
  `117-118` (timeout / spawn failure), `125` (`args.json` is not a list of strings),
  `150-151` (bwrap timeout / spawn failure), `177-178`, `180` (fixture read errors), `208` (usage error),
  `255` (`--holdout` is not a directory), `275` (holdout absent), `285-286` (a control stub missing) — arms.
- `141` — `raise Setup("bwrap is not installed: …")`. **Keep and note:** this arm is what makes the harness
  **fail closed** when `bwrap` is absent (wave-2 hardening `371d8234`, per the wave-2 sentinel). It never fires on this
  host because `bwrap` is present (`which bwrap` → `/usr/bin/bwrap`), so the harness ran sandboxed
  (`r56_ctl_c2: sandbox=bwrap`).

**Dead parameter — real, tiny.** `git(repo, work, *args, check=True, text=True)` (`:47`) has a `text=` parameter that
is **never passed and never used**: `grep -n "git(.*text=" quality/r56_ctl_c2.py` returns only the definition line
itself. The function always returns `subprocess.CompletedProcess` and every caller reads `.stdout`/`.returncode` as
bytes. Severity: **cosmetic** — one dead keyword argument.

**Note (not a defect): the `--holdout` and `--no-sandbox` flags are live, not dead.** They are unexercised by the
frozen claim (the claim reads the hold-out from the rev, `registration-v2.md` E6), but they are the mechanism by which
the wave-3 reseal seat (`R56W3ExecHoldoutReseal`) re-seals the hold-out. I exercised `--holdout` against the committed
hold-out and it produces the identical green verdict:
```
$ python3 -I quality/r56_ctl_c2.py --repo <lane> --rev 0f3a5436... --work <scratch> \
    --holdout <lane>/.ufo/waves/round-56/fixtures/c2-holdout
r56_ctl_c2: sandbox=bwrap fixture_commit=ok control_scores={'const-host': (1, 0), 'empty': (0, 0), 'sibling-reader': (0, 0), 'lookup-committed': (18, 0)}
MADO_R56_C2: rev=0f3a5436... fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET
```
So `--holdout` is exercised on demand; it is not dead weight.

---

### 1.5 `quality/r56_ctl_c3.py` — **earns its place; the biggest shared-helper surface**

**Verdict: everything earns its place.** 435 statements, 377 claim-exercised (the 9 frozen controls + the good tree),
58 never executed. All 58 are error arms:

- `91` (git failed), `140` (registry row with wrong cell count), `463` (git clone --shared failed),
  `466` (scratch toplevel mismatch), `471` (mutation target not a regular file), `478-480` (cleanup on exception) — setup.
- `100`, `104` (`blob_at`: not a blob / wrong path), `216` (`first_listing`: no row lists the entry),
  `236` (`mut_drop_one`: skipped entry), `241`/`247`/`254`/`260`/`266`/`280`/`330`/`337`/`343`/`351`
  (per-mutation precondition arms) — keep.
- `379-382` (counter timeout / could-not-start), `389`, `392`, `395`, `398`, `403`, `408`, `410`
  (counter-line grammar arms), `417`, `420`, `422`, `429`, `431`, `433`, `436`, `438` (judge arms) — keep.
- `495` (usage), `509` (`--rev` is not a commit), `514`/`516`/`519`/`523`/`526`/`530`/`534`/`537` (frozen-data checks),
  `546` (`--counter` is not a file), `550` (no counter at rev), `570` (control ineffective), `588` (counter run failed),
  `608-610` (unexpected exception → exit 2) — keep.

**Dead constant — real, tiny.** `ARCHIVE_PATHS = ["corpus", TABLES_PATH, ALLOW_PATH]` (`:49`) is defined and **never
used**: `grep -n "ARCHIVE_PATHS" quality/r56_ctl_c3.py` returns the single definition line. The C3 harness does not
`git archive` the archive paths at all — it `git clone --shared` the lane (`:459`) and mutates the clone in place
(the deliberate deviation D1 in its own docstring, `:25-27`, which explains why the clone is used instead of an
archive). Severity: **cosmetic** — one dead module constant.

**Stale docstrings (cosmetic, real):**
- `:6` — "The harness holds the **six** frozen controls"; the code has `N_CONTROLS = 9` (`:51`) and the frozen v2
  registration has 9 (registration-v2.md §C3-v2). Introduced at `2e39282e` with `N_CONTROLS = 9` already present
  (`git log` confirms) — **wrong from birth**.
- `:19` — "exit 0 only when good=ok and **k=6**"; the code prints `controls=<k>/9` (`:595`) and requires
  `k == N_CONTROLS` (`:594`). Same defect, same commit.
- `:2` and `:4` still say the claim is `PRED-C3-r56` / `PRED-C3-r56` while the frozen v2 claim is
  `PRED-C3-r56-v2` (claims-frozen-v2.md). The `:2` reference is to a **superseded** v1 name. Cosmetic: the printed
  line is correct (`claim=c3`), and the frozen file is never edited by this lane.

---

### 1.6 `quality/check-r56-controls.py` — **earns its place; the leanest file in the set**

**Verdict: everything earns its place.** 27 statements, 25 claim-exercised, **2 never executed**: `26-27`
(`print("MADO_R56_CONTROLS: SETUP usage"); return 2` — the unknown-claim arm). Keep: a dispatcher called with a bad
`--claim` must print nothing else and exit 2.

**One documentation defect — the dispatcher advertises flags that do not work for two of its three claims.**
The docstring (`:4`) says:
```
python3 -I quality/check-r56-controls.py --claim c1|c2|c3 --repo . --rev REV --work DIR [--counter PATH] [--holdout DIR]
```
But the dispatcher forwards **all** non-`--claim` arguments verbatim to the selected module (`:39-41`), and the three
modules accept different subsets:
- `--counter` is accepted by C1 (`:488`) and C3 (`:489`) but **not** by C2 (`r56_ctl_c2.py:202` accepts only
  `--repo --rev --work --holdout`).
- `--holdout` is accepted by C2 (`:202`) but **not** by C1 or C3.

Measured:
```
$ python3 -I quality/check-r56-controls.py --claim c2 --counter /tmp/x --repo <lane> --rev 0f3a5436... --work <scratch>
r56_ctl_c2: setup error: usage: --repo REPO --rev REV --work DIR [--holdout DIR] [--no-sandbox]
$ python3 -I quality/check-r56-controls.py --claim c1 --holdout /tmp --repo <lane> --rev 0f3a5436... --work <scratch>
r56_ctl_c1: error: unrecognized arguments: --holdout /tmp
MADO_R56_CONTROLS setup error: usage: --repo R --rev REV --work DIR [--counter PATH] [--claim c1]
$ python3 -I quality/check-r56-controls.py --claim c3 --holdout /tmp --repo <lane> --rev 0f3a5436... --work <scratch>
SETUP: usage: --repo PATH --rev REV --work DIR [--counter PATH] (each once, two-token form)
```
Severity: **cosmetic** — the behaviour is fail-closed and correct (an unsupported flag produces a setup error and exit
2, never a false green); only the usage line is over-broad. A reader following the docstring with `--claim c2
--counter PATH` gets a confusing error. Note the C1 error message is *doubly* confusing: it mentions `--claim c1`, the
one flag the dispatcher never forwards.

**Duplication:** this dispatcher is 43 lines and is the only place the three harnesses are joined. It has no duplication
of its own. It is the natural home for the shared helper module proposed in §2.

---

### 1.7 `tools/mado-watchplan.py` — **earns its place; the leanest dead weight of the set**

**Verdict: everything earns its place.** 391 statements, 253 claim-exercised (26 fixtures), 127 selftest-only
(`MADO_WATCH_SELFTEST: 86/86 assertions passed`), **11 never executed**.

*Never-executed (all 11):*
- `131` — `raise Setup("too_large")` for `MAX_TOTAL_BYTES` (64 MiB) exceeded in `read_limited`. **Keep** — a
  declared defensive budget (docstring divergence (8)).
- `181-182` — `expand()`: a glob that raises is treated as no-match. **Keep** — the docstring says "no match is
  ERROR nomatch".
- `196-197` — `Plan.__init__`: `os.path.realpath(root)` raising is swallowed. **Keep.**
- `212` — `add_event`: `MAX_EVENTS` (100 000) exceeded. **Keep** — declared budget (divergence (8)).
- `228` — `parse_file`: a listed file that cannot be read is listed, not parsed. **Keep** — declared behaviour.
- `308-309` — `os.path.realpath(path, strict=True)` raising for a symlink → the canonical watch is skipped. **Keep.**
- `324` — `read_getoption`: the file exists and is regular but the read fails. **Keep.**
- `398` — the selftest's `MADO_WATCH_SELFTEST: FAIL` line. **Keep.**

I spot-checked two of these by hand, and both behave as documented:
```
$ python3 -I tools/mado-watchplan.py --config /etc/hostname --getoption /nonexistent/go.json
MADO_WATCH: SETUP unreadable
$ python3 -I tools/mado-watchplan.py --config /tmp
MADO_WATCH: config=/tmp autoreload=on disable_autoreload=unset paths=1 unsupported=0 errors=0
MADO_WATCH: n=1 role=primary path=/tmp type=dir mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM via=main
```

**The one substantive gap: the tool's `--selftest` is not gated by any committed check either.**
`tools/mado-verify.sh` never mentions `mado-watchplan` (`grep -n "watchplan" tools/mado-verify.sh` → no hits). The
`--selftest` mode is exercised by the wave-3 spec (`make-w3-spec.py:55` asks for
`MADO_WATCH_SELFTEST: 86/86`) and by the wave-2 scribe (`R56W2ScribeRecords.md:43`), so it is live in the round's
workflow, but no committed gate runs it. Same status as §1.1/§1.2 — **not a deletion candidate**, but the round's
evidence for the tool rests on it, so it matters that nothing keeps it honest automatically.

**Nothing to extract.** The tool has no duplicated logic within itself.

---

## 2. Duplication across the three `r56_ctl_*` harnesses — worth extracting NEXT round, not now

The seat asks which duplication is worth extracting next round. I measured it structurally (AST, per-function
line ranges) rather than by eye: `receipts/duplication.txt`.

**Total shape:** `r56_ctl_c1.py` 633 lines / 36 functions, `r56_ctl_c2.py` 323 / 12, `r56_ctl_c3.py` 618 / 36.
Every one of the three is a **complete, standalone harness**: each has its own `Setup` exception, its own git wrapper,
its own environment scrubber, its own argument parser, its own `run(argv)` entry point and its own error path to
exit 2. There is **no shared module** — `check-r56-controls.py` only dispatches.

**Cluster-by-cluster, with the honest verdict:**

| cluster | c1 | c2 | c3 | verdict |
|---|---|---|---|---|
| git wrapper | `git` `:85-89` (5 L) | `git` `:47-52` (6 L) | `git` `:87-93` (7 L) | **extract** |
| env scrubber | `_env` `:72-82` (11 L) | `scrubbed_env` `:43-44` (2 L) | `git_env` `:75-84` (10 L) + `counter_env` `:368-370` (3 L) | **extract** |
| `Setup` class | `:62-63` | `:39-40` | `:66-67` | **extract** |
| child process run | `run_counter` `:419-450` (32 L) | `run_program` `:111-118` (8 L) + `staged_run` `:136-152` (17 L) | `run_counter` `:373-383` (11 L) | **partial** |
| verdict judging | `judge_good` `:453-466`, `judge_control` `:469-479` | — | `judge_good` `:415-424`, `judge_control` `:427-440`, `note_diverge` `:443-450` | **no** (see below) |
| counter-line parse | inline in `run_counter` `:432-450` (LINE_RE + LEG_RE + count extraction) | — | `parse_line` `:386-412` (LINE_RE + self-consistency) | **partial** |
| arg parsing | `parse` `:484-494` (argparse) | `parse` `:192-209` (hand-rolled two-token) | `parse_args` `:484-496` (hand-rolled two-token) | **partial** |
| `run` entry + exit-2 | `run` `:497-502` | `run` `:309-318` | `run` `:602-613` (+`execute` `:499-599`) | **extract** |
| blob/tree reading | `ls_present` `:92-99` + `export_good` `:102-111` | `ls_entry` `:55-65` | `blob_at` `:96-105` + `entry_blobs` `:108-120` | **extract** |
| scratch repo build | `materialize` `:114-128` (mktemp + `git init` + copytree + commit) | — | `build_scratch` `:454-480` (clone --shared + checkout + commit) | **no** (different mechanism) |
| registry/fence parsing | `entry_rows` `:150-174`, `_cells` `:184-190` | — | `split_row` `:132-141`, `parse_registry` `:144-153`, `fence_flags` `:162-178`, `cite_lines` `:181-185` | **no** (independent reimplementation is the point) |

**What I would extract next round (one new module, `quality/r56_ctl_common.py`), and why:**

1. **`Setup` + the `run(argv) → exit 2` wrapper** (3 copies: c1 `:62-63`/`:497-502`, c2 `:39-40`/`:309-318`,
   c3 `:66-67`/`:602-613`). ~30 lines, and the three copies already differ in their stderr prefix
   (`MADO_R56_CONTROLS setup error:` vs `r56_ctl_c2: setup error:` vs `SETUP:`). One class + one wrapper removes the
   drift. **Cheapest win.**
2. **The git wrapper + env scrubber** (c1 `:72-89`, c2 `:43-52`, c3 `:75-93` + `:368-370`). ~50 lines. The three
   differ in *substance*, not just spelling: c1 scrubs `GIT_CONFIG_GLOBAL=/dev/null`, c3 scrubs
   `GIT_CONFIG_NOSYSTEM=1`, c2 scrubs neither. Extracting must preserve each module's env exactly or the harnesses
   stop being independent — so this extraction is worth doing only with per-module env parameters, not a single
   merged dict. **Medium risk; do it carefully.**
3. **Blob/tree reading** (c1 `ls_present`+`export_good`, c2 `ls_entry`, c3 `blob_at`+`entry_blobs`). ~55 lines. Same
   caveat: each returns a slightly different shape (`set[str]` vs `(mode,typ)` vs `bytes|None`) and the callers depend
   on the difference. Extract as three thin wrappers over one `git ls-tree`/`cat-file` core.

**What I would NOT extract, and why:**

- **`judge_good` / `judge_control` (c1 `:453-479` vs c3 `:415-440`).** Same names, same intent — "did the counter
  print the green line / did it catch the mutant as registered" — but they judge *different* grammars: c1 compares a
  `GOOD_COUNTS` dict of six integers plus a `LEG_RE` leg vocabulary; c3 compares a leg **list** plus a self-consistency
  rule (`missed` must contain every nonzero count) plus an independent cross-check (`note_diverge`). Unifying them
  would either weaken the C3 self-consistency check or the C1 count check, or force a parameterised abstraction that is
  harder to read than the two copies. **Leave as is.**
- **The registry / fence / row parsers** (c1 `entry_rows`+`_cells`, c3 `split_row`+`parse_registry`+`fence_flags`+
  `cite_lines`, and the C3 counter's own `outside_fence_lines`+`cite`+`parse_registry`). These are *deliberately
  independent reimplementations*: the C3 harness docstring says so explicitly — "The harness recomputes
  missing/extra/dangling itself; a mutation that does not strictly raise the leg it targets … is a harness setup
  error, never a silently passed control" (`r56_ctl_c3.py:29-30`), and `note_diverge` (`:443-450`) exists precisely to
  *compare* the harness's numbers against the counter's and report a divergence. Sharing one parser between a counter
  and the harness that is supposed to audit it would destroy the independence that makes the control meaningful.
  **Leave as is — this is the one place where "duplication" is the feature.**
- **The scratch-repo builders** (c1 `materialize` `:114-128` vs c3 `build_scratch` `:454-480`). Different mechanisms
  on purpose: c1 builds a minimal repo from a `git archive` of only the counter-relevant paths (cheap, 13 copies);
  c3 clones the whole lane `--shared` so the *base* revision's objects exist for the `lost` control (documented
  deviation D1, `r56_ctl_c3.py:25-27`). A unified builder would have to carry both policies as flags — worse than two
  clear functions.

**Net:** roughly **135 lines** of the ~1574 harness lines are mechanically extractable without weakening any
independence property; roughly **120 lines** look like duplication but must stay. The honest recommendation for round 57
is: extract items 1-3 above, and record in the lesson that the judge/parse/scratch-repo "duplication" is deliberate
independence, not debt.

---

## 3. Dead options / flags — the complete list

| file:line | flag | status | severity |
|---|---|---|---|
| `quality/r56_ctl_c1.py:490` | `--claim c1` | **parsed, never read.** The dispatcher strips `--claim` before forwarding (`:34-38`), so it is unreachable via the documented entry point. Running the module with `--claim c1` changes nothing. | cosmetic |
| `quality/r56_ctl_c2.py:47` | `git(..., text=True)` | **dead parameter.** Never passed, never used; the function always returns `CompletedProcess` and callers read `.stdout` as bytes. | cosmetic |
| `quality/r56_ctl_c3.py:49` | `ARCHIVE_PATHS` | **dead constant.** Defined, never used (the C3 harness clones instead of archiving — deviation D1). | cosmetic |
| `quality/counters/c3-r56-used-by.py:449` | `--detail` | **never used** by any leg, control, fixture or gate. Documented diagnostic switch; works; 4 statements (`:295-298`). | cosmetic |
| `quality/check-r56-controls.py:4` | usage line advertises `[--counter PATH] [--holdout DIR]` | **wrong for 2 of 3 claims.** `--counter` is rejected by C2; `--holdout` is rejected by C1 and C3. Fail-closed behaviour, misleading message. | cosmetic |
| `quality/counters/c1-r56-autoreload-entry.py:5`, `quality/counters/c3-r56-used-by.py:9`, `tools/mado-watchplan.py:15` | the `--selftest` modes | **not dead** — exercised by the round's wave-2/wave-3 spec instructions and (for the tool) by `R56W2ScribeRecords.md:43`, but **by no committed gate**. See §4. | informational |

`--counter` on C1 (`:488`) and C3 (`:489`) and `--holdout` on C2 (`:202`) are **not** dead: they are the mechanism the
wave-2/wave-3 mutation seats use to point a harness at a mutant
(`make-w2-spec.py:51,53,55`, `make-w3-spec.py:73`: "the counter's `--selftest` AND `python3 -I
quality/check-r56-controls.py --claim c3 ... --counter <mutant>`"). I exercised `--counter` on C3 and it works:
```
$ python3 -I quality/r56_ctl_c3.py --repo <lane> --rev 0f3a5436... --work <scratch> --counter <lane>/quality/counters/c3-r56-used-by.py
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
```
and `--holdout` on C2 (§1.4).

---

## 4. The one substantive cross-cutting finding: the round's own instrument self-tests are ungated

**Severity: weakens the claim** (not blocking it — the frozen predicates themselves are unaffected).

- `quality/counters/c1-r56-autoreload-entry.py --selftest` → `242/242 assertions passed` (325 statements covered).
- `quality/counters/c3-r56-used-by.py --selftest` → `MADO_USED_BY_SELFTEST: 16/16 assertions passed` (104 statements covered).
- `tools/mado-watchplan.py --selftest` → `MADO_WATCH_SELFTEST: 86/86 assertions passed` (127 statements covered).

Together, **556 of the 2 787 statements across the instrument set (19.9 %) are reachable only through these three
modes** (C1 counter 325, C3 counter 104, tool 127 — the three harness modules have no selftest mode), and
**no committed gate runs any of them**:
```
$ grep -c "r56" tools/mado-verify.sh
0
$ grep -n "watchplan" tools/mado-verify.sh      # (no hits)
$ grep -rn "c1-r56-autoreload-entry.py --selftest\|c3-r56-used-by.py --selftest" --include=*.sh --include=*.py . | grep -v '/w[123]/'
./quality/counters/c1-r56-autoreload-entry.py:5:    (its own docstring)
./quality/counters/c3-r56-used-by.py:9:              (its own docstring)
./.ufo/waves/round-56/make-w2-spec.py:77: ...        (a wave instruction, not a gate)
```
The `MADO_SELFTEST: 460/460 assertions passed` in `receipts/selftest-before.txt:1` is `tools/mado-verify.sh --selftest`
and covers **none** of the round-56 instruments.

**Why it matters.** The frozen C2 claim rests entirely on the tool and its 26 fixtures; the tool's own selftest
(127 statements, 32% of the tool) is the only thing that exercises the tool's argument-grammar and budget arms. If the
tool's `--selftest` silently stopped asserting, the C2 gate would stay green — the gate scores the tool against
fixtures, never against the tool's own self-checks. Round 57 should wire the three selftests into a committed check
(e.g. `quality/check-counter-selftest.py` or a `mado-verify.sh` row) so the 556 statements are gated. **This is a
routed finding, not a change:** the frozen predicates are untouched by it.

---

## 5. Preserved contract (what I did NOT touch)

I made **no edit** to any lane file, at any revision. Verified after all measurement:

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git diff --stat 0f3a54361a9824484d0801679ceb1fd8ac7c32e1
(empty — tracked files byte-identical to the tip)
$ git status --porcelain | grep '^??' | grep -v '.ufo/waves/round-56/'
(empty — nothing new outside the round-56 wave tree)
```
No git/jj mutation of any kind (no add/commit/stash/checkout/reset/push, no `jj new/describe/squash`); no delegation;
no background job; no write outside `.ufo/waves/round-56/w3/R56W3SimplInstruments/` and
`/fast/scratch/hyaku/mado-r56/R56W3SimplInstruments/`; no write under `~/.config` or `~/.local`; no
`hyprctl` write command of any kind (this seat's item names no host read either — I ran no `hyprctl` at all).

**The frozen artifacts are untouched**: `claims-frozen.md`, `claims-frozen-v2.md`, `registration.md`,
`registration-v2.md`, `frozen-tables.json`, `frozen-tables-v2.json`, `c3-name-only.tsv`, `ctl/sibling-reader.py`,
the fixtures, and the hold-out are all byte-identical to the tip. I read `claims-frozen-v2.md` and `registration-v2.md`
to establish the contract and did not edit them.

**The three frozen gates still read green at the tip** (re-run under coverage, receipts `c1.out`, `c2.out`, `c3.out`):
```
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK
MADO_R56_C2: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
```

---

## 6. Deliverables

- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/simplify.md` — this document.
- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/coverage-summary.txt` — per-file statement counts, the
  claim-exercised / selftest-only / never-executed line ranges (machine-generated).
- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/duplication.txt` — the AST-level duplication census.
- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/c1.out`, `c2.out`, `c3.out` — the three gate verdicts
  produced by the coverage runs.

Scratch (removed at yield): `/fast/scratch/hyaku/mado-r56/R56W3SimplInstruments/` — the venv, `.coveragerc`,
`analyze.py` (coverage reader), `dup.py` (AST duplication census), `c2tool.py` (tool-coverage driver),
`cov/`, `cov-st/` (coverage data), and the measurement scratch dirs `w-c1/`, `w-c3/`, `w-c2/`, `f-c1/`, `f-c2/`,
`f1/`, `f3/`, `g-c2/`, `g-c3/`, `h-c1/`, `st-c1/`, `st-c3/`, `tmptest/`.

## 7. Tooling

Per the operator's tooling directive (2026-10-19) and `/home/vgpnk/.omp/agent/RULES.md`:

| tool | version | channel | reason |
|---|---|---|---|
| `uv` | 0.13.0 | preinstalled at `/home/vgpnk/.local/bin/uv` | venv + package install (used) |
| `coverage` | 7.17.0 | `uv pip install coverage` into a scratch venv (official PyPI) | line-level measurement of exercised vs unexercised code paths — the only way to make "no leg/control/fixture exercises this line" a measurement rather than a guess |

No pacman transaction was run or attempted (host-wide pacman guard is paused). No system Python, no `~/.local/bin`,
no PATH directory was modified. The coverage `.pth` hook was installed **only** inside the throwaway scratch venv's
`site-packages`, and the venv is deleted at yield.

## 8. What I could not verify

1. **Coverage of the C2 tool under `bwrap`.** The harness runs the tool under `bwrap` with `/usr/bin/python3`, so the
   sandboxed child's lines are not measurable by my venv-based instrumentation. I measured the tool's lines with the
   same fixtures and the lane's own staging code but **without** the sandbox. The sandboxed run's own verdict is
   confirmed green separately (`c2.out`), and the sandbox only restricts what the tool can see — but I did not prove
   line-for-line that the sandboxed and unsandboxed runs execute the same tool lines.
2. **Whether the wave-2/wave-3 mutation seats actually ran the `--selftest` oracles.** I read the spec generators
   (`make-w2-spec.py:51,53,55`, `make-w3-spec.py:73`) and the wave-2 seat reports I could see
   (`R56W2MutC1CounterA.md:11` — `242/242 assertions passed`; `R56W2ScribeRecords.md:43` — `82/82`); the wave-2
   wrap-up stopped two seats (`R56W2MutC3Counter`, `R56W2MutC2Harness`) with no reports, and wave 3's own mutation
   seats were still running when I wrote this. My §4 finding is therefore stated as "no **committed** gate runs them",
   which I did verify — not as "no seat ever ran them".
3. **`--detail` on the C3 counter** — I confirmed it is unused by any leg/control/fixture/gate and that it is
   documented in the counter's own docstring. I did **not** run it (it prints offending pairs to stderr; running it
   against the tip produces an empty list because the tip has `missing=0 extra=0`), so I did not confirm its output
   shape against a non-empty case.
4. **The `git clone --shared` in `r56_ctl_c3.build_scratch` (`:459`)** creates alternates pointing at the lane's
   object store. I confirmed the harness removes each clone before the next (`shutil.rmtree(d, …)` at `:592`, wave-2
   sentinel F7) and that the lane's `git status` is clean afterwards, but I did not audit the alternates file for
   dangling references after the run.
