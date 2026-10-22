# CritSeparability — wave-2 falsify: separability, no-harm, statement width

Seat `MadoR23.CritSeparability` (critic, leaf). Target: landed tip `2f1134f38930fc8b067d2d7f5bba126338faabdd`
(C1 `2e592aff`, C2 `c8cb3930`, C3 `2f1134f3`, linear on `4de44647`). No lane file edited except this report.
No tool installed or updated. `skill://godspeed` could not be read: no `godspeed` skill directory exists on
this host (`find / -xdev -type d -name godspeed` found nothing), so I worked from the assignment alone.

**Verdict line.** All three counters are causally separable and reproduce their registered before and after
values. C2 holds. C3's counter holds, but its PROVINCE wording is wider than the counter. C1's counter and
every registered guard hold, but C1 harms operability *outside* the guards. The tip silently misses executed
commands for callbacks stored through `global` or `nonlocal`. I reproduced this independently, and the
`nonlocal` form is a new confirmation.

## What I did

1. Cloned the lane to `/fast/scratch/hyaku/mado-r23/CritSeparability` (`git clone -q`). In that clone I built
   three revert trees off the tip with `git revert --no-edit`: `minusC1` `21bfd923`, `minusC2` `c60a0b91`,
   `minusC3` `acfda7f6`. All three reverts applied cleanly because the commits touch disjoint paths:
   - C1: `tools/mado-tripwire.py` plus two new `.ufo/` files.
   - C2: `corpus/SOURCES.md` and `corpus/knowledge/terminal-trees-r23.md`.
   - C3: `PROVINCE.md` only.
2. Ran each counter of record from inside the clone, one child at a time. C1's tool was extracted with
   `git show REV:tools/mado-tripwire.py`. The revisions were base `e33ea304`, C1's parent `4de44647`, each
   commit, the tip, and each revert tree. Commands:
   - `python3 -I .ufo/waves/round-23/repair/measure.py --tool out/tool-<k>.py`
   - `python3 -I .ufo/waves/round-23/c2/count.py <rev>`
   - `python3 -I .ufo/waves/round-23/c3/count.py <rev>`
3. Confirmed that no counter, fixture, or guard harness changed after the pre-measurement commit.
   `git log 6b383c46..2f1134f3 --` over `round-23/{repair,c2,c3}`, `round-22/replay.py`, `round-22/oracle`,
   `round-21/oracle` and `round-20/tw-precision.py` lists only `a28e481` and `4de4464`.
4. Checked coupling between claims, i.e. whether C2/C3 bytes can reach a C1 guard:
   - No lane tool reads `corpus/`, `SOURCES.md` or `PROVINCE.md` at runtime. The `mado-action-plan.py`
     hits at :552 and :589 are literal plan fixtures.
   - The corpus comparator (`round-21/corpus/compare.py`) reads a SHA-pinned snapshot manifest
     (`8e1cf206…`), not the live tree.
   - `tw-precision.py` reads only `tools/mado-tripwire.py` at REV plus a pinned suite.
5. Re-ran the cheap guards sequentially, on the tip tool and on the C1-reverted tool:
   - precision at the tip and at all three revert trees;
   - `round-22/residual-truth/measure.py`;
   - `round-22/oracle/measure.py`;
   - `round-22/replay.py --mode oracle`.

   I did **not** re-run the corpus comparator, the eleven selftest suites, or the resource populations,
   because the overlapping-comparator rule (routed defect 9c) applies and ReCorpus, ReSelftests and
   ReResource own those runs. For those I read `evidence/guards-candidateB-scratch.json`. Its tool sha256
   `41489991…` is byte-identical to the tip's classifier, so it does measure the landed bytes, but it is the
   L1's receipt, not my run.
6. Independent recall probe for C1. I authored three fixtures and committed them only in my clone (branch
   `crit-fixtures` `a6fd89c`, `crit/fixtures/`):

   | Fixture | sha256 |
   |---|---|
   | `SepGlobalHook` | `706c2661…fe639` |
   | `SepNonlocalHook` | `3195a3f7…c428` |
   | `SepDictControl` | `cc771f8c…0d0c` |

   Truth comes from `crit/run.py`, which reuses `repair/truth.py`'s `CHILD` recording fake `subprocess` and
   its `safe()` gate via `runpy`, under a 384 MiB address-space limit and a 15 s timeout. Scanning uses the
   round-21 `scan` helper. Command: `python3 -I crit/run.py out/tool-base_e33ea30.py out/tool-tip_2f1134f.py`
   (exit 0).

Receipts (scratch, outside the lane): `/fast/scratch/hyaku/mado-r23/CritSeparability/out/`. That folder holds
`matrix.txt`, `c{1,2,3}-<k>.json`, `prec-<k>.json`, `resid-<k>.json`, `r22or-<k>.json`, `r21rep-<k>.json`
and `probe.json`.

## Separability matrix (measured)

| Revision | Tool sha | C1 repair | C2 | C3 (v2) |
|---|---|---|---|---|
| base `e33ea304` | `cd9da20c` | 6/12 | 0/3 | 5 |
| C1 parent `4de44647` | `cd9da20c` | 6/12 | 0/3 | 5 |
| C1 `2e592aff` (C2 parent) | `41489991` | **12/12** | 0/3 | 5 |
| C2 `c8cb3930` (C3 parent) | `41489991` | 12/12 | **3/3** | 5 |
| tip `2f1134f3` | `41489991` | 12/12 | 3/3 | **0** |
| tip − C1 | `cd9da20c` | 6/12 | 3/3 | 0 |
| tip − C2 | `41489991` | 12/12 | 0/3 | 0 |
| tip − C3 | `41489991` | 12/12 | 3/3 | 5 |

Each counter moves only at its own commit. Reverting any one commit returns only its own counter to the
before value and leaves the other two at their after values. My C1 results match the L1 receipts case-for-case:
- `repair-before-e33ea304.json` matches my run at the C1 parent.
- `repair-after-2f1134f3.json` matches my run at the tip.

C1 flips six cases: `ReturnedGlobalCallableShadow`, `ForwardExistingClosureWithoutFrameContamination`,
`ForwarderInvokesCallback`, `CallerLocalShadowsHelperGlobal`, `ForwarderPassesCallerArgument` and
`ForwarderInvokesFactoryClosure`. The other six already passed at base, including both H5 `present` cases.

## Guards (no-harm, registered)

| Guard | Tip | Tip − C1 | Source |
|---|---|---|---|
| r22 primary | 57/57 | 57/57 | my run |
| r21 oracle replay | 35/35 + 17/17 | 35/35 + 17/17 | my run |
| r22 residual (H3) | 4/4 | 2/4 | my run |
| precision | 166/175, same passing set at tip, −C1, −C2, −C3 | identical | my run |
| corpus comparator 1356 files | 0 added, 0 removed, 0 error flips, 0 unparsed-counter changes | — | L1 receipt only |
| selftests | 247/247 | — | L1 receipt only |
| resource (4 populations) | 3/3 each | — | L1 receipt only |

C2 and C3 cannot move any registered guard. Every guard consumes only classifier bytes plus frozen inputs, and
the classifier at tip − C2 and tip − C3 is byte-identical to the tip.

## Per-claim findings

### C1 operability — counter met, separable; **harm outside the guards (fixable defect)**

**Counterexample (reproduced independently).** Base flags both stores as a `lead`; the tip returns exit 0,
zero rows and zero unparsed. Both are silent misses of an executed `pacman -S`.

```python
import subprocess
def run():
    subprocess.run(["pacman", "-S", "r23sep-global-hook"])
def register(callback):
    global hook
    hook = callback
register(run)
hook()
```

| Fixture | Executed (fake subprocess) | Base | Tip |
|---|---|---|---|
| `SepGlobalHook` | `pacman -S r23sep-global-hook` | `host_mutation` lead, exit 1 | none, exit 0 |
| `SepNonlocalHook` (`nonlocal hook; hook = callback` inside `outer`) | `pacman -S r23sep-nonlocal-hook` | `host_mutation` lead, exit 1 | none, exit 0 |
| `SepDictControl` (dict store, same shape as the frozen `CallbackStoredInDict`) | `pacman -S r23sep-dict-control` | lead | lead (unchanged) |

- The global case independently corroborates AttackEscapeGate's `EscapeGlobalHook`.
- The `nonlocal` case is the variant that report left as `[INFERENCE]`. It is now measured.
- Separability: this harm belongs to C1 alone. The tool bytes at tip − C2 and tip − C3 equal the tip's.

**Impacted axes:**
- **Operability.** Recall loss on the primary detection, with no unparsed counter to signal it.
- **Calibration.** The guards were saturated on this mechanism: H5 is guarded by two `present` cases that
  already passed at base, so they could not detect a callback-sweep loss.
- The untracked design note `w1/out/ExecFullB/design-note.md:163` says the gate "errs toward sweeping (no lost
  findings)". These fixtures falsify that sentence. It is not in the landed record, but it is the design
  basis the L1 cited.

**Width.** The registered C1 statement (12/12 frozen set plus the named guards) is no wider than its counter,
and it holds. Any wider sentence fails, for example "H5 kept", "callback-store recall preserved" or
"no lost findings". The commit subject "escape-gated callback sweep" describes the mechanism and claims no
gain, which is acceptable.

**Smallest safe correction (advice):**
- In the tip's `parameter_escapes`, treat assignment of the parameter to a bare name that the function
  declares `global` or `nonlocal` as an escape. Equivalently, skip the gate and sweep whenever the receiver
  body contains an `ast.Global` or `ast.Nonlocal` naming the assignment target.
- Add `SepGlobalHook` and `SepNonlocalHook` (or AttackEscapeGate's equivalents) to a *next-round* frozen
  set. Under the registration's no-narrowing rule this round cannot re-target.

**Verdict C1:**
- The counter claim stands at 12/12 and the claim is separable.
- "No axis harmed" does **not** hold at discovery level.
- The L1 must record the recall regression rather than call C1 harm-free.

### C2 coverage — **holds**

- 3/3 at `c8cb3930` and at the tip; 0/3 at tip − C2. C1 and C3 do not affect it.
- Credited sources: foot S140, S141, S144–S149; kitty S123–S130, S133; ghostty S134–S139, S150, S151.
- The commit is append-only (+30 SOURCES rows, +1 note, 0 deletions).
- No duplicate S-ids. All 30 rows have 11 cells. Twenty-nine are `mined`, opened 2026-10-22, with used-by
  naming the note. S132 is `queued` and is not used by the note, which matches the note header.
- Nothing in the lane reads these files at runtime, so there is no harm to other axes.
- Width: the note scopes every route as documentary. It states that no binary is installed, nothing was run,
  and reload behaviour is `[UNK]`. That stays within the counter.
- Minor: the ghostty "C5" negative claim (no file watch and no SIGHUP across the v1.3.1 tree) rests on a
  sweep "recorded in §4", i.e. SrcGhostty's wave-1 report, not on a SOURCES row. The counter does not check
  it. This is labelled as a negative claim, so it is not over-claiming.
- The round-17 README paragraph (`corpus/README.md:122-124`, "foot, kitty and ghostty trees remain
  unsourced") stays in place as history, and the note's §Supersedes names it explicitly. That is consistent
  with the append-only rule.

### C3 calibration — counter holds; **statement wider than counter**

- 5 → 0 only at `2f1134f3`; reverting C3 alone restores 5.
- C1 adds no file under `tools/`, so C1 does not move C3. The diff is +10 lines, 0 deleted.
- SHONEN box 4 is untouched and still `[~]` at the tip.

**Counterexample to wording.** The new PROVINCE paragraph says the instruments "are named here so the province
accounts for every tracked tool it runs". The counter covers `tools/**` only.
- At the tip the lane tracks **130** `.py`/`.sh` files outside `tools/`, and none of them has a PROVINCE row.
  These are the harnesses the lane runs, such as `repair/measure.py`, `c2/count.py`, `c3/count.py`,
  `round-22/replay.py` and `round-21/corpus/compare.py`.
- C1 itself raised that number from 128 to 130 by adding `.ufo/waves/round-23/evidence/tool-base-cd9da20c.py`
  and `.ufo/waves/round-23/w1/out/L1/guards-used.py`.
- The counter also verifies only that a row exists with four non-empty cells, not whether its reads and
  writes are true.
- My spot check found no file-write calls in `mado-tripwire.py`, `mado-assessment.py` or
  `mado-evidence-audit.py`. `mado-action-plan.py` writes only under `tempfile.TemporaryDirectory`
  (:702–763). Both are consistent with their rows. `mado-verify.sh`'s row was not checked by me;
  ReviewProvinceTruth owns that check.

**Impacted axis:** calibration (a statement wider than its counter).

**Smallest safe correction:** an append-only clarification that the round-23 inventory covers the tracked tools
under `tools/`. `.ufo/waves/**` harnesses are round-scoped measurement scripts and are not province
instruments.

**Verdict C3:** the counter claim stands at 0. The paragraph's "every tracked tool it runs" must be narrowed to
`tools/` before scoring.

## Other observation (lane hygiene, not a claim harm)

`.ufo/waves/round-23/evidence/__pycache__/tool-base-cd9da20c.cpython-314.pyc` (untracked, 08:57) exists in
the lane. Some run imported the base copy without `-I`/`-B` inside the lane tree. It was not created by me:
all my runs used the scratch clone.

## Addendum — re-run at tip `3732c7a7` (L1 follow-up, 2026-10-22T12:08Z)

Scope: re-run only.
- New commits: C1 fix `03227ddf` (classifier sha256 `e1dc8029ced9fcc62d458b8143209605f34b60c9e4cfe6d8f66515c2efce4a47`)
  and the append-only corrections commit `3732c7a7` (PROVINCE.md and terminal-trees note).
- I extracted the classifier fresh with
  `git -C <lane> show 3732c7a7…:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/CritSeparability-r2/tool.py`
  (sha matches).
- Receipts: `/fast/scratch/hyaku/mado-r23/CritSeparability-r2/out/`.

**Fixture tally:**

| Comparison | REGRESSED | same-correct | improved |
|---|---|---|---|
| base `cd9da20c` vs new `e1dc8029` (my three fixtures) | 0 | 3 | 0 |
| previous tip `41489991` vs new `e1dc8029` | 0 | 1 | 2 |

| Fixture | Executed (fake subprocess) | Base | Previous tip | New tip |
|---|---|---|---|---|
| `SepGlobalHook` | `pacman -S r23sep-global-hook` | lead, exit 1 | none, exit 0 | lead, exit 1, unparsed 0 |
| `SepNonlocalHook` | `pacman -S r23sep-nonlocal-hook` | lead, exit 1 | none, exit 0 | lead, exit 1, unparsed 0 |
| `SepDictControl` | `pacman -S r23sep-dict-control` | lead | lead | lead |

**Separability at the new tip.** The single-commit reverts of `c8cb3930` and `2f1134f3` conflict, because
`3732c7a7` appends to the same files. So the C2 and C3 rows below are file-level claim reverts on top of the
new tip:
- C2 revert: `corpus/SOURCES.md` restored to `c8cb3930^` and the note removed.
- C3 revert: `PROVINCE.md` restored to `2f1134f3^`.
- C1 revert: `03227ddf` and `2e592aff` reverted, which yields classifier `cd9da20c`, i.e. base.

| Revision | Tool | C1 repair | C2 | C3 |
|---|---|---|---|---|
| `03227ddf` | `e1dc8029` | 12/12 | 3/3 | 0 |
| tip `3732c7a7` | `e1dc8029` | 12/12 | 3/3 | 0 |
| tip − C1 (both commits) | `cd9da20c` | 6/12 | 3/3 | 0 |
| tip − `03227ddf` only | `41489991` | 12/12 | 3/3 | 0 |
| tip − C2 (file-level) | `e1dc8029` | 12/12 | 0/3 | 0 |
| tip − C3 (file-level) | `e1dc8029` | 12/12 | 3/3 | 5 |
| tip − `3732c7a7` | `e1dc8029` | 12/12 | 3/3 | 0 |

Each counter still moves only under its own claim. The corrections commit `3732c7a7` moves no counter, even
though it touches both C2's file and C3's file.

**Guards on `e1dc8029` (my runs, sequential):**
- round-22 residual 4/4;
- round-22 primary 57/57;
- round-21 oracle replay 35/35 + 17/17;
- precision 166/175 with the identical passing set at the tip, tip − C2, tip − C3 and tip − `3732c7a7`.

The first replay attempt exited 2 with `setup_error: --tool must resolve inside the repository`, because I had
passed the extract outside the clone. I re-ran it on a byte-identical copy inside the clone, and it exited 0.
As before, I did not re-run the corpus comparator, the selftests or the resource runs.

**Verdicts updated:**
- **C1:** both of my counterexamples are repaired, with no fixture regressed against base. This verdict is
  limited to my three fixtures. AttackEscapeGate's other neighbours belong to that seat's re-run.
- **C2:** unchanged; holds.
- **C3:** the width finding is resolved by the `3732c7a7` correction, which states that the inventory covers
  `tools/` only and that `.ufo/waves/**` scripts are not inventoried. That scope correctly covers
  `03227ddf`'s added `w1/out/L1/l1-attacks.sh`, which brings tracked `.py`/`.sh` files outside `tools/` to 131.
