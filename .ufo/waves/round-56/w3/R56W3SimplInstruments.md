# R56W3SimplInstruments — dead-weight report over the round-56 instrument set

**Seat:** R56W3SimplInstruments (read-only simplifier). **Scored tree:** `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`.
**Deliverable with all file:line pointers:** `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/simplify.md`.

## What I attacked

The seven round-56 instruments: `quality/counters/c1-r56-autoreload-entry.py`, `quality/counters/c3-r56-used-by.py`,
`quality/check-r56-controls.py`, `quality/r56_ctl_c1.py`, `r56_ctl_c2.py`, `r56_ctl_c3.py`,
`tools/mado-watchplan.py` — 3 787 lines, 2 787 executable statements.

## How I attacked it

"Which code paths does no leg/control/fixture exercise?" is not answerable by grep, so I measured it: `coverage 7.17.0`
in a throwaway scratch venv, with a `.pth` subprocess hook (the harnesses scrub the child env, so an env var would not
have reached the children). Three measured runs per instrument — the **claim** run, the instrument's own
**`--selftest`** mode, and for the tool a scratch driver that reuses the lane's own `r56_ctl_c2.score()` over the same
26 fixtures — unioned, then classified **claim-exercised / selftest-only / never-executed**. Full per-file line
ranges: `receipts/coverage-summary.txt`. Duplication measured by AST, not by eye: `receipts/duplication.txt`.

All three frozen gates re-run green at the tip under that instrumentation (`receipts/c1.out`, `c2.out`, `c3.out`):
```
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK
MADO_R56_C2: rev=0f3a5436... fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
```

## Findings, in one line each

**Per file — "code paths no leg/control/fixture exercises (name them by line)":**

| file | claim-exercised | selftest-only | never-executed | verdict |
|---|---|---|---|---|
| `c1-r56-autoreload-entry.py` | 533 / 896 | 325 | 38 | **earns its place** |
| `c3-r56-used-by.py` | 217 / 359 | 104 | 38 | **earns its place** |
| `r56_ctl_c1.py` | 368 / 436 | 0 | 68 | **earns its place** |
| `r56_ctl_c2.py` | 215 / 243 | 0 | 28 | **earns its place** |
| `r56_ctl_c3.py` | 377 / 435 | 0 | 58 | **earns its place** |
| `check-r56-controls.py` | 25 / 27 | 0 | 2 | **earns its place** |
| `mado-watchplan.py` | 253 / 391 | 127 | 11 | **earns its place** |

**Every never-executed line is an error arm**, not dead logic: setup/fail-closed arms of the git layer
(`c1:48,51-52,70-71,73,85`; `c3:78,80,86,89,95-96,102,110,123,196,212,228,234,260,265-266`), symlink/non-blob guards
(`c1:105,120`; `c3:116,138,141`), fence/comment and row-grammar arms (`c1:141,151,158,160,215,261,279,451,470,514,516,519,521`;
`c3:167-170`), the per-mutation precondition arms in the harnesses (all of `r56_ctl_c1`'s 24 `MutationError` raises
and `r56_ctl_c3`'s 11), the counter-line grammar arms (`r56_ctl_c1:438,441,445`; `r56_ctl_c3:389,392,395,398,403,408,410`),
the judge arms, the CLI/usage arms, and the tool's declared defensive budgets
(`mado-watchplan.py:131,181-182,196-197,212,228,308-309,324`). Each is a line that must be able to fire for the
instrument to *fail closed* — that is the contract. **I am deleting nothing.** Full line lists: `receipts/simplify.md` §1.

**Duplication worth extracting NEXT round (not now — the frozen artifacts are untouched):** roughly **135 of the
~1 574 harness lines** are mechanically extractable into one `quality/r56_ctl_common.py`: the `Setup` class and the
`run(argv) → exit 2` wrapper (3 copies), the git wrapper + env scrubber (3 copies, but each scrubs a *different* set of
`GIT_*`/`HOME`/`TMPDIR` keys — extracting must preserve each exactly or the harnesses stop being independent), and the
blob/tree readers (3 copies with 3 different return shapes). **Roughly 120 lines look like duplication and must stay**:
`judge_good`/`judge_control` (c1 `:453-479` vs c3 `:415-440`) judge different grammars (counts+leg-vocabulary vs
leg-list+self-consistency+independent cross-check); the registry/fence/row parsers are *deliberately independent*
reimplementations — `r56_ctl_c3.py:29-30` and the `note_diverge` diagnostic at `:443-450` exist precisely so the
harness audits the counter rather than sharing its code; and the two scratch-repo builders use different mechanisms on
purpose (c1 `materialize` `:114-128` archives only the counter-relevant paths; c3 `build_scratch` `:454-480` clones the
lane `--shared` so the `lost` control can read the base revision — documented deviation D1, `:25-27`).

**Dead options/flags — the complete list, all cosmetic:**
- `quality/r56_ctl_c1.py:490` — `--claim c1` is **parsed and never read**; the dispatcher strips `--claim` before
  forwarding (`check-r56-controls.py:34-38`), so it is unreachable via the documented entry point, and running the
  module with it changes nothing.
- `quality/r56_ctl_c2.py:47` — `git(..., text=True)` is a **dead parameter**: never passed, never used.
- `quality/r56_ctl_c3.py:49` — `ARCHIVE_PATHS` is a **dead constant**: defined, never used (the harness clones instead).
- `quality/counters/c3-r56-used-by.py:449` — `--detail` is **never used** by any leg/control/fixture/gate (only its own
  docstring mentions it). It works; it is a diagnostic switch.
- `quality/check-r56-controls.py:4` — the usage line advertises `[--counter PATH] [--holdout DIR]`, but `--counter` is
  rejected by C2 and `--holdout` is rejected by C1 and C3. The behaviour is fail-closed; the message is misleading.
- **NOT dead** (I checked each): `--counter` on C1/C3 and `--holdout` on C2 are the mechanism the wave-2/wave-3
  mutation seats use to point a harness at a mutant (`make-w2-spec.py:51,53,55`, `make-w3-spec.py:73`). I exercised
  both: `--counter` on C3 → `controls=9/9 verdict=OK`; `--holdout` on C2 → `fixtures=18/18 holdout=8/8 ... OK`.

**Stale names (cosmetic, and wrong from birth — `git log` confirms `N_CONTROLS` was already 12 / 9 in the first
commit of each file, `2e39282e`):** `r56_ctl_c1.py:6` "the **ten** frozen C1 controls" and `:23` "k=**10**" and `:609`
"the denominator is the frozen **10**" (all should be 12); `r56_ctl_c3.py:6` "the **six** frozen controls" and `:19`
"k=**6**" (should be 9); `r56_ctl_c3.py:2,4` still name the superseded `PRED-C3-r56` rather than `PRED-C3-r56-v2`.
The *code* is right in every case (`N_CONTROLS` drives the verdict, and `len(CONTROLS) == N_CONTROLS` is required so a
dropped control cannot pass) — only the prose is wrong.

## The one substantive cross-cutting finding

**Severity: weakens the claim (not blocking).** The three instruments' own `--selftest` modes cover **556 of the
2 787 statements (19.9 %)** — C1 counter 325, C3 counter 104, tool 127 — and **no committed gate runs any of them**:

```
$ grep -c "r56" tools/mado-verify.sh          # 0
$ grep -n "watchplan" tools/mado-verify.sh    # no hits (rc=1)
$ grep -rn "c1-r56-autoreload-entry.py --selftest\|c3-r56-used-by.py --selftest" --include=*.sh --include=*.py . | grep -v '/w[123]/'
./quality/counters/c1-r56-autoreload-entry.py:5:    (its own docstring)
./quality/counters/c3-r56-used-by.py:9:              (its own docstring)
./.ufo/waves/round-56/make-w2-spec.py:77: ...        (a wave instruction, not a gate)
```
The `MADO_SELFTEST: 460/460 assertions passed` in `receipts/selftest-before.txt:1` is `tools/mado-verify.sh --selftest`
and covers none of the round-56 instruments. The C2 claim rests entirely on the tool and its 26 fixtures; the tool's own
selftest (127 statements, 32 % of the tool) is the only thing exercising the tool's argument-grammar and budget arms. If
it silently stopped asserting, the C2 gate would stay green. **Routed finding for round 57** — wire the three selftests
into a committed check. The frozen predicates are untouched by this.

## Preserved contract

No edit to any lane file at any revision; no git/jj mutation of any kind; no delegation; no background job; no write
outside `.ufo/waves/round-56/w3/R56W3SimplInstruments/` and my scratch. Verified after all measurement:
`git diff --stat 0f3a5436...` → empty; `git status --porcelain | grep '^??' | grep -v '.ufo/waves/round-56/'` → empty.
The frozen artifacts (`claims-frozen*.md`, `registration*.md`, `frozen-tables*.json`, `c3-name-only.tsv`,
`ctl/sibling-reader.py`, the fixtures, the hold-out) are byte-identical to the tip. I ran no `hyprctl` command and read
no host config.

## What I could not verify

1. **Coverage of the C2 tool under `bwrap`.** The harness runs the tool sandboxed with `/usr/bin/python3`, so the
   sandboxed child's lines are not measurable by my venv instrumentation. I measured the tool's lines with the same
   fixtures and the lane's own staging code, sandbox off; the sandboxed run's own verdict is separately confirmed green.
   I did not prove line-for-line that sandboxed and unsandboxed runs execute the same tool lines.
2. **Whether the wave-2/wave-3 mutation seats actually ran the `--selftest` oracles.** I read the spec generators and
   the seat reports I could see (`R56W2MutC1CounterA.md:11` → `242/242`; `R56W2ScribeRecords.md:43` → `82/82`); two
   wave-2 seats were killed with no reports and the wave-3 mutation seats were still running. My finding is stated as
   "no **committed** gate runs them", which I did verify.
3. **`--detail` on the C3 counter** — confirmed unused by any leg/control/fixture/gate and documented; I did not run it
   against a non-empty case to confirm its output shape.
4. **The `git clone --shared` alternates** in `r56_ctl_c3.build_scratch` (`:459`) — I confirmed each clone is removed
   before the next (`:592`) and that the lane's `git status` is clean afterwards, but did not audit the alternates file.

## Deliverables

- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/simplify.md` — the full dead-weight report with every
  file:line pointer.
- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/coverage-summary.txt` — per-file statement counts and the
  claim-exercised / selftest-only / never-executed line ranges.
- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/duplication.txt` — the AST duplication census.
- `.ufo/waves/round-56/w3/R56W3SimplInstruments/receipts/c1.out`, `c2.out`, `c3.out` — the three gate verdicts.

Scratch `/fast/scratch/hyaku/mado-r56/R56W3SimplInstruments/` (venv, coverage data, analyzer scripts) is removed at
yield.

## Tooling

`coverage` 7.17.0 installed via `uv pip install` (uv 0.13.0, official PyPI) into a throwaway scratch venv, because
line-level coverage is the only way to make "no leg/control/fixture exercises this line" a measurement rather than a
guess. No pacman transaction was run or attempted (host-wide pacman guard is paused); no system Python, no
`~/.local/bin`, no PATH directory was modified; the coverage `.pth` hook lived only inside the throwaway venv.
