# RevGateRcFixPlan — review of the `omarchy.skill.vs_head` rc-capture fix (F10) and the F14 fixtures / PIN re-cut

Seat: `MadoR18.RevGateRcFixPlan` (reviewer, leaf). Date: 2026-10-20.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only review: no file in the
lane was written except this report; the gate was **not executed** (seat rule; executors run
their own scripts and fixtures, seats do not run lane gates).

Revisions reviewed (the file moved under me while I read it — GateRcFix is the sole writer):

| thing | value |
|---|---|
| baseline commit | `d9a5a18`; `git show d9a5a18:tools/mado-verify.sh` sha256 `fba82a66…` |
| pre-edit gate bytes | `fba82a66…` (identical to the d9a5a18 blob — verified with `git show … \| sha256sum`), 3,711 L |
| gate bytes at review | `sha256 2bdf5e8afbb617142e4a881943084f94c9513327b1de25170ad71db113983925`, 3,768 L, mtime `12:44:17 -0300` |
| derived regression target at review | `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744`, 2,460 L, `bash -n` OK |
| `PIN_MADO` at review | `cd1d73d7…` (**stale** — the re-cut was not landed yet) |

All line numbers below are for the 3,768-L revision above. The plan text I was asked to review
is the GateRcFix item (`…/round-18/w1/spec.json`, item `GateRcFix`): (1) capture the producer rc
at the `vs_head` row ``(`${PIPESTATUS[0]}` or read the blob to a variable first)`` and route
`rc≠0` to `UNKNOWN "cannot read HEAD:<rel> (rc=N)"`; (2) per-verb `STUB_GIT_*_RC` knobs;
(3) an OM scenario asserting `describe`/`rev-parse`/`show` rc 128 → `UNKNOWN`; (4) a red-before
receipt against the `d9a5a18` bytes; (5) the measured `PIN_MADO` re-cut; (6) a `--selftest`
receipt with the gate sha on its first line.

What actually landed differs from the plan's first option: the row now uses
`set -o pipefail` **inside** the command substitution plus `$?` — see §1. I review both the
plan's wording and the landed bytes, because the plan's wording is the recipe a re-derivation
would follow.

---

## 1. (a) Is the `PIPESTATUS` fix correct under `tmo` and the `set` options in force?

**Options in force.** `set -u` at `:82` is the only `set` option in the script; there is no
`set -e`, no global `pipefail`; the only `shopt` is `shopt -s nullglob` at `:2720`.
`tmo()` (`:121`) is `timeout 5 "$@"` when `timeout` is on PATH, else plain `"$@"`.
`row()` (`:108`) is a plain appender — nothing aborts on a non-zero command.

**The plan's literal `${PIPESTATUS[0]}` — wrong as written.** Measured in a `/tmp` lab that
reproduces the exact shape under `set -u` (real failing command, `tmo` wrapper, `sha256sum |
cut`):

```
blob=$(tmo … | sha256sum | cut -d' ' -f1); grc=${PIPESTATUS[0]}   →  grc=0
```

Two independent reasons, both fatal to that form:

1. The pipeline runs inside the command-substitution **subshell**; that subshell's
   `PIPESTATUS` is not visible in the parent.
2. Even if it were, the array is reset by the assignment itself: `blob=$(…)` is one simple
   command, so `${PIPESTATUS[0]}` is that command's status, which is the substitution's status,
   which is the **last** element of the inner pipeline (`cut`) = 0.

So a literal implementation would keep the bug while looking fixed. The only thing that would
catch it is OM9/OM10 themselves (the row would still be FAIL "local edit"), so the seat must not
weaken those assertions while chasing a red.

**The landed form — correct.** `:3453-:3471`, code at `:3460-:3461`:

```bash
local blob sw grc
blob=$(set -o pipefail; tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null \
  | sha256sum | cut -d' ' -f1); grc=$?
```

- `set -o pipefail` is scoped to the substitution subshell: it cannot leak, and it does not
  interact with `set -u` (no `-e` exists, so nothing aborts early).
- `$?` after the assignment is the pipeline status = last non-zero stage. Lab results in the
  same shape: failure → `rc=128` with `blob=e3b0c442…`; success → `rc=0` and `blob` identical to
  `sha256sum file` (`2751a3a2…`). The success path is byte-exact because the bytes still flow
  through the pipe; no variable round-trip.
- Under `tmo`: `timeout` wraps only `git`, so the pipeline's first status is `timeout`'s, which
  passes git's rc through (`timeout 5 bash -c 'exit 128'` → 128, measured) and yields 124 on a
  kill → `UNKNOWN`, never a compare of partial bytes. In the OM fixture `PATH` there is **no**
  `timeout` (the stub dir symlinks `bash grep sed … readlink` at `:686-:687` and omits it), so
  `tmo` executes the stub directly; both the live and the fixture path deliver 128. The fixture
  therefore exercises the same branch the host takes.
- `grc` is assigned unconditionally on the only path that reaches it, so `set -u` is satisfied.

**Two caveats, neither blocking:**

1. With `pipefail`, `$?` is the *rightmost* non-zero status. `rc=N` is git's own rc only when
   git is the sole failing stage; if `sha256sum`/`cut` also fail, N is theirs and the message
   ("cannot read HEAD:… (rc=N)") misattributes the source. The comment at `:3458`
   ("git's own rc") is therefore slightly too strong. A temp-file capture
   (`git show >"$t"; grc=$?; blob=$(sha256sum <"$t")`) would make it exact; the pipefail form
   is the smaller diff and is correct for the failure class F10 names.
2. The plan's second option, "read the blob to a variable first", is **only** safe if the
   variable is not what gets hashed. `$( )` strips all trailing newlines, and no `printf`
   reconstruction is byte-exact for arbitrary blobs: measured, a file ending in one LF hashes
   differently through `printf '%s'`, and a file ending in none hashes differently through
   `printf '%s\n'`. If that route is ever taken, hash a temp file, never the variable.

**Verdict: landed fix correct; plan wording must not be implemented literally.**

---

## 2. (b) Is the `-z "$blob"` guard then dead?

**Yes — and it is still in the file.** `:3463-:3471` now reads:

```bash
if [ "$grc" != 0 ]; then      row … UNKNOWN "cannot read HEAD:$rel (rc=$grc) — …"
elif [ -z "$blob" ]; then     row … UNKNOWN "cannot read HEAD:$rel from the checkout"
elif [ "$blob" = "$sw" ]; then …
```

- Before the fix the guard was dead because `sha256sum` always prints a digest (even of empty
  input), so `blob` was never empty — F10's exact observation.
- After the fix it is dead **for a different reason**: `pipefail` now makes every stage failure
  set `grc≠0` (git, `sha256sum`, `cut`), and the outer guard at `:3450` already requires
  `have sha256sum`. A *successful* `sha256sum` always prints a digest, so `blob` can be empty
  with `grc=0` only if `sha256sum` exits 0 while printing nothing — not reachable with the real
  tool and not reachable by any fixture the suite builds (`$OMB/sha256sum` is a symlink to the
  real one). `cut`'s output is non-empty whenever its input is.
- Net effect: F10's "dead UNKNOWN arm" did not disappear, it **moved** one branch down. The
  live arm is now the rc arm; the dead arm is the `-z` arm. That is a strict improvement (the
  false FAIL is gone), but it leaves an untestable branch and a message ("cannot read HEAD:…
  from the checkout") that cannot describe a reachable state.
- An empty *blob* is legitimate (zero-byte file) and its digest is correctly compared; only the
  "unreadable" reading is dead. So the `-z` arm is not a guard against a real hazard.

**Recommendation (one of):** fold it into the rc arm —
`if [ "$grc" != 0 ] || [ -z "$blob" ]; then row … UNKNOWN "cannot read HEAD:$rel (rc=$grc) — …"`
— or delete the `elif`. If the seat wants to keep a belt, it must add a fixture that reaches it
(a `sha256sum` stub exiting 0 with no output, which would also perturb `omarchy.skill.sha`), and
that is not worth the fixture complexity for this round.

Also note the comment at `:3454-:3459` explains that the `-z` guard "could never fire" in the
*pre-fix* code, while the code immediately below keeps a `-z` guard that still cannot fire. The
comment is historically accurate but reads as if the guard had been addressed; it has not.

---

## 3. (c) Does the re-cut procedure need the derived-target excision only?

**Yes, and the re-cut is a one-shot — there is no fixed point.** The only artefact whose bytes
move is the derived target built by the three `sed` excisions in `mado_r7_target_build`
(`:1775-:1783`); the only records to update are `PIN_MADO` (`:1687`) and a dated re-cut comment,
with `TABLE_MADO` only if the measured table moves.

Evidence for the "no fixed point" claim: the pin, `SPEC_SHA`, `HARNESS_SHA_RECORDED` and
`TABLE_MADO` all live **inside** the excised `MADO-R7-REGRESSION-BLOCK` (`:1591-:2031`), and the
derived target contains no `PIN_MADO=` definition (the only occurrence in the derived bytes is a
static comment carried from the round-13 note). So editing the pin does not change the derived
target, and the re-cut does not need to iterate.

**What moved and why one re-cut covers it.** Both edits are outside every excised pair:
the row at `:3460-:3470`, and the stub + OM9 + OM10 at `:662-:684` / `:811-:848`.
Measured at review: `PIN_MADO=cd1d73d7…` vs derived `20714096…` → `--selftest` R10 (`:583`) is
red and `--regression` will print `REGRESSION_TARGET … match=no` (`:1937`), then
`REGRESSION_RECUT: bash <harness> --target <derived> …` (`:1940-:1941`) and exit 2 SETUP.

**Trap worth recording:** the OM pair is marked `MADO-R8-OMARCHY-BLOCK` (`:622-:849`), which the
exciser's `MADO-R8-BLOCK` patterns do **not** match (they match only the two exact pairs at
`:1416-:1579` and `:2032-:2554`). Measured on the current bytes: the derived target still
contains `STUB_GIT_SHOW_RC` and the OM scenarios, and it is what `--selftest` derives. So the
round-8 header sentence "a widening inside the pair needs no re-cut" applies only to the exact
`MADO-R8-BLOCK` pairs — **not** to the OM pair. Anyone adding OM assertions later still owes a
re-cut; the name is misleading, and the excision predicate should not be "fixed" to match it
without re-cutting.

**Procedure (as the gate itself prints it):**

1. `bash tools/mado-verify.sh --regression` on the final gate bytes → SETUP with the
   `REGRESSION_RECUT` line and a kept workdir; the derived target is
   `<workdir>/target.mado-verify.sh` (sha `20714096…` at this revision).
2. Run the printed command from the lane root (`--target` that derived file, `--defects` the
   written spec, `--suite 'bash "$MUTANT" --selftest'`, `--label mado-verify.sh`).
3. Require: `MUTATE_TARGET sha256=20714096…`, `CONTROL: GREEN` (the control now runs OM9/OM10
   too — 17 more assertions than the last recorded control), `D1..D9,R1: KILLED` (10/10),
   flips 0, inconclusive 0, `MUTATE_RESTORE: OK`, target sha unchanged before/after.
4. Set `PIN_MADO` to the **measured** `MUTATE_TARGET` sha (not to `20714096…` by hand — that is
   only the value if no further edit lands), add the dated re-cut record in the excised block;
   change `TABLE_MADO` only if the measured table moved.
5. Re-run `--selftest` (R10 green) and `--regression` (PASS). `SPEC_SHA` and
   `HARNESS_SHA_RECORDED` are untouched by this edit; the harness sha is provenance, not a gate
   (the live harness reads `0673d2e5…` at review, different from the recorded revision — that is
   the documented, non-gated behaviour).

Do not edit the gate between step 2 and step 4; any later byte invalidates the measurement. The
expected table is unchanged (the embedded spec has zero `omarchy` references — measured
`grep -c 'omarchy'` over the spec heredoc = 0 — so no mutant touches the new row or scenarios),
but that is an expectation: the re-cut measures it, and a moved row is recorded as measured,
never blessed.

---

## 4. (d) Which existing assertions might change count?

**New assertions:** OM9 = 8 (`:818-:830`), OM10 = 9 (`:839-:848`) → **+17**.
Therefore the pristine run should read `MADO_SELFTEST: 389/389 assertions passed` (372 + 17).
The regression control base is exact, not approximate: the pre-edit derived target is
byte-identical to the round-14 evidence (`cd1d73d7…`, 117,602 B, measured) whose control read
`MADO_SELFTEST: 267/267`, and the +17 is deterministic (each `st_*` call is one assertion), so
the re-cut control should read `284/284`. Both figures are *arithmetic* here — I did not run the
gate; the measured lines are owed receipts (see §6).

**The only existing assertion whose verdict changes is R10** (`:583`, derived target ==
`PIN_MADO`): red on the current intermediate bytes, green after the re-cut. It is the pin's
tripwire, not a defect.

**No existing count expectation moves**, because no existing scenario sets a `STUB_GIT_*_RC`
(the knobs default 0 and are per-`env`-invocation, so they do not leak):

- OM1: 11 rows, exactly one FAIL, same-bytes `vs_head` PASS — unchanged (success path untouched).
- OM3: two FAILs — unchanged. OM4: two `UNKNOWN`s — unchanged (no rc knob; `$OMB2` has the git
  stub). OM6: the `"local edit"` FAIL direction — unchanged, and now explicitly guarded from the
  other side by OM9's `st_not_has … "local edit"`. OM7: four FAILs — unchanged.
- OM10's `st_row_has omarchy.skill.vs_head PASS` is the success-path guard proving the rc fix did
  not stop the normal comparison.
- The gate hardcodes no assertion total (`grep -n '372' tools/mado-verify.sh` → no match), so
  nothing inside the gate needs a numeric edit.

**Docs/evidence that becomes stale (L1-owned — report the numbers, do not edit):**
`corpus/knowledge/gate-standing-use.md:438` (372/372), lessons round-14/15/16/17, the round-17
harm-watch expectation, and any text citing the regression control total. The F15 drift
(SKILL.md's older 268/268, hardcoded `/tmp/w5-mado-m52-selftest.*` at `:395` and
`/tmp/mado-verify-regression.*` at `:1909` ignoring `TMPDIR`) is outside this fix; changing
`:395` would also move the derived target and force the re-cut, so it must not be done here.

---

## 5. Findings by severity

**High — plan text, not landed code.** A literal `${PIPESTATUS[0]}` after
`blob=$(pipeline)` is a silent no-op (`grc=0`, measured). Implemented that way, the F10 bug
survives and only OM9/OM10 expose it; there is a real incentive to "fix the test" instead. The
landed `pipefail`-inside-substitution form is correct; keep it and correct the plan's wording.

**Medium — landed.** The `-z "$blob"` arm (`:3465-:3466`) is now unreachable (any stage failure
sets `grc≠0`; `have sha256sum` pre-checked) and no fixture can reach it. F10's dead-UNKNOWN-arm
class is inverted, not removed. Fold into the rc arm or delete; do not keep an untestable branch
(§2).

**Medium — plan step 4 (red-before) is not executable as written.** "Run the new scenario's
assertions against the `d9a5a18` gate bytes" cannot be done literally: the old file has no
OM9/OM10, and the selftest always targets `$0`. Two receipts that do work, either or both:

- **(a) behavioural red on the baseline:** `git show d9a5a18:tools/mado-verify.sh > /tmp/old.sh`
  (sha `fba82a66…`, byte-identical to the pre-edit live gate), run *that* file's omarchy plane
  against the same OM fixture with a `show`-rc=128 git stub, and capture
  `omarchy.skill.vs_head FAIL … != HEAD blob e3b0c442… (local edit; …)` — the F10 measurement.
- **(b) assertion red on the new bytes:** copy the new gate to `/tmp`, revert only `:3460-:3461`
  to the old pipeline, run `--selftest`, and capture the OM9/OM10 failures. This is the
  "the new assertions bite" receipt and is cheap.

Record the gate sha the receipt ran in `gate-rc-redbefore.txt`; never overwrite the lane file.
At review, `gate-rc-redbefore.txt`, `regression-recut.txt` and `gate-selftest.txt` do not yet
exist under `round-18/evidence/` — they are pending, not defects.

**Low.** OM9/OM10 capture `om_rc` but assert no exit code. The FAIL+UNKNOWN composition implies
exit 1 and `st_counts_agree` pins the counts line, so this is a gap in strictness, not in the
fix; a `st_eq "OM9: exit 1"` would close it (+1 assertion → 390).

**Low.** The stub's rc knobs compare as strings (`[ "${STUB_GIT_…_RC:-0}" != 0 ]`, `:671-:679`):
a value like `00` would exit 0 while printing nothing, producing a *different* false FAIL
(`MOVED: describe … ''`). Not exercised; a `case` or arithmetic test removes the class.

**Low.** OM9's `st_not_has … "local edit"` also matches the success arm's text
"worktree == HEAD blob (index-free; no local edit)". In OM9 `vs_head` is UNKNOWN, so that arm is
never printed and the assertion is correct today; it is worth knowing that the check depends on
which arms fire in that run.

---

## 6. Residual risk and verification gaps

- **Gate not executed** (seat rule): the 389/389 total, the red-before row, and the 10/10 table
  are *owed receipts*. My rc claims come from a `/tmp` lab reproducing the identical pipeline
  shape under `set -u`, with `timeout` present and absent; the derived-target claims come from
  running the gate's own three `sed` excisions read-only on the current bytes.
- **Revision flux:** the file changed between reads (3,711 L `fba82a66…` → 3,768 L `2bdf5e8a…`).
  If GateRcFix edits again, every line number and the derived sha here must be re-derived;
  `PIN_MADO` must be set from the *measured* target at that final revision, not from
  `20714096…`.
- **R10/`--regression` are expected red/SETUP at the reviewed bytes** because the pin is stale.
  That is the pending re-cut, not a finding; do not "resolve" it by relaxing R10.
- **Expected-table assumption:** the 10 mutants do not mention omarchy (spec `grep -c` = 0), so
  the re-cut should reproduce the same table — but the control suite now includes OM9/OM10, and
  the re-cut must show `CONTROL: GREEN` with the new total, not merely "no new kills".
- **F15 scope:** hardcoded `/tmp` paths and stale doc counts are not touched by this fix. The
  receipt's gate-sha-first-line convention addresses provenance only; the docs are L1-owned.
- **Tooling:** nothing installed or upgraded for this review (no pacman/uv/npx call).

**Bottom line.** The landed rc capture is correct under `tmo` and `set -u` (the plan's
`${PIPESTATUS[0]}` variant is not); the `-z` guard is now dead and should be folded away; the
re-cut needs only the derived-target measurement and a measured `PIN_MADO` (no fixed point, one
measurement covers both hunks); and the only count that *must* move is the assertion total
(+17 → 389/389), with R10 red until the pin moves.
