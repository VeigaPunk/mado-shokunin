# ExecMutBaseline — frozen control harnesses re-run from a clean sandbox clone

Round 40 (hyaku run 7), inline v2 wave w1. Seat target: run the frozen C1/C2 control
harnesses at the freeze commit from a throwaway clone, report both outputs verbatim,
timings, and any difference from the committed receipts.

**Verdict: both harnesses reproduce at the freeze commit, from a clone.**
`CTL_C1: controls=18 correct=18/18`, `CTL_C2: controls=21 correct=21/21`, both exit 0.
The only byte difference from the committed receipts is a trailing `exit=0` line the
harnesses do not emit (recording wrapper appended it). One hygiene finding: the C1
harness leaks one `/tmp/mado-c1ctl-*` directory per invocation.

## Method (exact commands)

```
S=$(mktemp -d)                                     # /tmp/tmp.VcocPz1Q6J
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin $S/lane
git -C $S/lane rev-parse --show-toplevel           # -> /tmp/tmp.VcocPz1Q6J/lane  (verified == $S/lane)
git -C $S/lane -c advice.detachedHead=false checkout -q 5e7e88525cc539563de7746361b2650802e81809
git -C $S/lane rev-parse HEAD                      # -> 5e7e88525cc539563de7746361b2650802e81809
cd $S/lane
python3 -I .ufo/waves/round-40/ctl/run-c2-controls.py     # default run
python3 -I .ufo/waves/round-40/ctl/run-c1-controls.py     # default run
MADO_CTL_REV=5e7e88525cc539563de7746361b2650802e81809 python3 -I .ufo/waves/round-40/ctl/run-{c1,c2}-controls.py   # pinned re-run
```

Environment: `python3 3.14.8`; sandbox on `/tmp`; no `hyprctl` verb was run by this seat
(the counter always passes `--hyprctl <stub>`: `quality/counters/c1-r40-live.py:490,555,566`;
the missing-program clause uses `no-such-dir/hyprctl` at `:565`). Sandbox working tree was
`git status --porcelain`-clean after both runs — the harnesses wrote nothing into the clone.
Sandbox removed (`rm -rf $S`, verified gone).

### `MADO_CTL_REV` / `master` question (resolved, no adjustment needed)

`ctl/run-c1-controls.py:21` reads `MADO_CTL_REV` (default `master`) and `:86` hardcodes
`git -C LANE show master:tools/mado-options.py` for the BASE-tool control. In the clone the
local `master` is the lane's master tip `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`, one
commit **after** the freeze. Checked both:
- `git merge-base --is-ancestor 5e7e885… e2b51d3…` → yes (freeze is master's parent).
- `git diff --stat 5e7e885… e2b51d3… -- .ufo/waves/round-40 tools quality` → 4 files added, all
  w1 spec files (`make-w1-spec.py`, `w1-dispatch.json`, `w1-run.err`, `w1-spec.json`); no
  counter, no control, no tool change.
- `git show master:tools/mado-options.py | sha256sum` == `git show 5e7e885…:tools/mado-options.py | sha256sum`
  == `461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a` (neither has `--live`; grep count 0/0).

So `master` and the freeze are byte-equivalent for everything the counters read. Both runs
(default and pinned) were performed anyway; outputs are **byte-identical** (`diff` empty,
sha256 equal), so the pinning question is closed empirically, not only by inspection.

Frozen-artifact identity, sandbox@freeze vs lane@freeze (`git show <rev>:<path> | sha256sum`,
all SAME):

| path | sha256 |
|---|---|
| `.ufo/waves/round-40/ctl/run-c1-controls.py` | `59dded5e5039db2aba476f2239fc942adc0b94c47325ceede63d995e5b654c64` |
| `.ufo/waves/round-40/ctl/run-c2-controls.py` | `14ab2f2fe9dab59a2a1ee62c23b13333e41ddbdc83ae2a31507d6afc79ad7aa9` |
| `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt` | `f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa` |
| `quality/counters/c1-r40-live.py` | `192ff2d3d9de39b7a73ac439d4924e71ff8d308e0ecde38364f4e54c188115ea` |
| `quality/counters/c2-r40-forms-entry.py` | `b34dd357bbf31472a271fc849909e74bec98f0da265a26ed5ddbfa8df7a843db` |

## Output — C1 (verbatim, `c1-run-default.txt`, exit 0)

```
control=REF-reachability expected=fixtures=13/13 observed=fixtures=13/13 tool=present verdict=TARGET_MISSED ok=1
control=BASE-tool expected=fixtures=0/13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M01-all-agree expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M02-raw-compare expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M03-bool-exact expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M04-gradient-angle-ignored expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M05-gap-three-values-wrong expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M06-config-only-as-mismatch expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M07-extra-argv expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M08-set-ignored expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M09-shadow-ignored expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M10-hostile-probe-accepted expected=fixtures<13 observed=fixtures=12/13 tool=present verdict=TARGET_MISSED ok=1
control=M11-failure-swallowed expected=fixtures<13 observed=fixtures=12/13 tool=present verdict=TARGET_MISSED ok=1
control=M12-writes-config-root expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M13-no-normalisation-int expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M14-live-field-dropped expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M15-angle-inheritance-absent expected=fixtures<13 observed=fixtures=0/13 tool=present verdict=TARGET_MISSED ok=1
control=M16-probe-key-without-argv-check expected=fixtures<13 observed=fixtures=12/13 tool=present verdict=TARGET_MISSED ok=1
CTL_C1: controls=18 correct=18/18
```

## Output — C2 (verbatim, `c2-run-default.txt`, exit 0)

```
control=P-fabricated-self-consistent expected=admitted=1/1 observed=admitted=1/1 verdict=TARGET_MET ok=1
control=N01-no-entry expected=admitted=0/1 observed=admitted=0/1 clauses=a:0 b:0 c:0 d:0 e:0 f:1 g:0 h:0 ok=1
control=N02-entry-no-rows expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:0 d:1 e:0 f:1 g:1 h:0 ok=1
control=N03-gate-sha-wrong expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 ok=1
control=N04-quote-absent expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 ok=1
control=N05-quote-26-words expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 ok=1
control=N06-no-index-row expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:1 f:0 g:1 h:1 ok=1
control=N07-one-new-id-left expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 ok=1
control=N08-held-row-rewritten expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 ok=1
control=N09-duplicate-location expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 ok=1
control=N10-entry-line-lacks-quote expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 ok=1
control=N11-wrong-verified-at expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 ok=1
control=N12-staged-ids-as-is expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:0 d:0 e:1 f:1 g:0 h:1 ok=1
control=N13-status-candidate expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 ok=1
control=N14-receipt-outside-fetch expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 ok=1
control=N15-no-own-work-row expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 ok=1
control=N16-used-by-missing expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 ok=1
control=N17-receipt-tool-sha-stale expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 ok=1
control=N18-counts-disagree expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 ok=1
control=N19-labels-sum-wrong expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 ok=1
control=N20-lines-not-in-entry expected=admitted=0/1 observed=admitted=0/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 ok=1
CTL_C2: controls=21 correct=21/21
```

Both stderr streams were empty (`c1-run-default.err`, `c2-run-default.err`, 0 bytes).

## Timings

| run | rc | elapsed | method |
|---|---|---|---|
| C1 default (`REV=master`) | 0 | 55 949 ms | `date +%s%N` delta around the process |
| C1 pinned (`REV=5e7e885…`) | 0 | 53 909 ms | same |
| C2 default | 0 | ~1 040 ms | same (bash wall 1.04 s on the first capture) |
| C2 pinned | 0 | 1 078 ms | same |

C1 is ~54 s per invocation (18 counter runs, each spawning the tool over 13 fixtures);
C2 is ~1 s (21 fixture repos, each `mktemp -d` + 2 commits).

## Difference from the committed receipts

Committed receipts: `receipts/ctl-c1.txt`
sha256 `f9e38014dd2cb50a7e9d63c17f79d019ef0f264dfc5221bd779ae08e0cdaa961`,
`receipts/ctl-c2.txt` sha256 `22aaca32edc831c2d82f3ded61a803dbc58e6dd0c4e881e4e6cbdcc8018cfe1d`.

`diff` of my sandbox output vs each receipt (both runs, both rev modes) yields exactly one
hunk each:

```
=== C1 ===  19a20
> exit=0
=== C2 ===  22a23
> exit=0
```

That is: **every control line, every clause bitmap, every count line is byte-identical**;
the committed receipts carry one extra final line `exit=0` that neither harness prints
(neither harness writes to stdout after the `CTL_C*:` line — `run-c1-controls.py:113`,
`run-c2-controls.py` final print). `grep -rn 'exit=' .ufo/waves/round-40/ctl/ .ufo/waves/round-40/*.md`
returns nothing, so the line was appended by whatever shell recorded the receipt
(`… ; echo exit=$?`), not by an in-tree script. Not a predicate difference; the receipts
are faithful, plus a recorded exit status. Reproduced: `exit=0` in all four of my runs.

## Findings (each names its target)

1. **Both controls reproduce from a clone at the freeze commit.** Targets:
   `ctl/run-c1-controls.py` → `CTL_C1: controls=18 correct=18/18`; `ctl/run-c2-controls.py`
   → `CTL_C2: controls=21 correct=21/21`; both `rc=0`, stderr empty. Supports the registration's
   do-nothing/reachability and mutant claims (§C1 controls, §C2 controls) as reproducible outside
   the author's working tree.
2. **`MADO_CTL_REV` is not needed, and would not have helped if it were.** `ctl/run-c1-controls.py:86`
   hardcodes `master:tools/mado-options.py`, so the knob alone cannot move the BASE-tool control.
   Harmless here because sandbox `master` (`e2b51d3…`) and the freeze carry the byte-identical
   tool blob (`461f8c3c…`) and the only inter-commit diff is four w1 spec files. Pinned and
   default runs are byte-identical (`c1-run-default.txt` sha256 == `c1-run-pinned.txt` sha256
   `c2625316b2457beefe3d51c0c3f9d5ffeb8d3073acabe5afb2600fbf4c58041e`;
   C2 both `6f436e39077e9928a3883df46347d459de2df5d663c3259f3236f59203afdbc8`). Risk for a future
   round: if `master` ever gains a `--live` tool before the harness is re-run, `BASE-tool` would
   score 13/13 and CTL_C1 would fall to 17/18 with no code change — the `master` literal, not the
   predicate, would be the cause.
3. **C1 harness leaks a temp directory per invocation.** `ctl/run-c1-controls.py:74`
   `tmp = tempfile.mkdtemp(prefix="mado-c1ctl-")` has no matching `shutil.rmtree` anywhere in the
   file (only `run-c2-controls.py:213` cleans up; the counter cleans its own at
   `quality/counters/c1-r40-live.py:675`). Each run leaves ~700–860 KB. Evidence: 7
   `/tmp/mado-c1ctl-*` dirs existed after my runs; two were mine (17:50:51 `it7y21jd`, 17:52:13
   `sv1uu53u`, removed by this seat); five predate this seat (17:33:48, 17:35:00, 17:39:33,
   17:40:26, 17:41:26) — i.e. the leak also occurred when `receipts/ctl-c1.txt` was recorded. Left
   the five pre-existing dirs untouched (not mine). Hygiene only: it does not touch any scored
   clause.
4. **No host or lane mutation.** Sandbox `git status --porcelain` empty after both runs; the lane
   itself was only read (`git clone`, `git show`, `git diff`, `git rev-parse`, `git merge-base
   --is-ancestor`); no `hyprctl` verb run; no pacman; nothing written outside this seat directory,
   the report, and `/tmp`. Scratch removed: sandbox `/tmp/tmp.VcocPz1Q6J` and my two leaked
   `mado-c1ctl-*` dirs.

## Risks / caveats

- Local `git clone` hardlinks object files, so object *reads* are shared with the lane (read-only;
  no packfile was written — the sandbox tree stayed clean and no lane object was mutated).
- A single host (`python3 3.14.8`); fixture seeding is `sha256(REV:i)`, and both runs were
  byte-identical, so within-host determinism is shown for 2 runs per harness, not across versions.
- Tool installs: none needed (stdlib-only harnesses, `python3` present). No version/channel to
  record.

## Evidence files (this seat dir)

`c1-run-default.txt` (`c2625316…`), `c1-run-pinned.txt` (`c2625316…`),
`c2-run-default.txt` (`6f436e39…`), `c2-run-pinned.txt` (`6f436e39…`),
`c1-run-default.err` / `c2-run-default.err` (empty), `c1-run-default.meta`, `c2-run-default.meta`.

Report: `.ufo/waves/round-40/w1/ExecMutBaseline.md`
