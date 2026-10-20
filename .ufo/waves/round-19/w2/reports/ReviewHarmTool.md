# ReviewHarmTool — partial

Target: `.ufo/waves/round-19/harm-watch.sh` at `01b80946d92b26370d3012a7da655d00dd135154`
(sha256 `077e1b4d05be67aca0587b240122f05eb2d4bb4f5955d93f368d46b0ae09238a`; worktree bytes
identical). All line numbers below are for the committed file, read via
`git show 01b80946…:.ufo/waves/round-19/harm-watch.sh`. Three questions answered:

1. **Does PASS ever certify a REV whose tool bytes differ from the worktree?** For 13 of
   14 commands: no. For the navigation group: **yes — proven end-to-end.**
2. **Are expected baselines separated from failures?** **Yes**, correctly and narrowly,
   verified against the real tool and the real round-18 frozen inputs.
3. **Does it ever invoke the live gate?** The static command list never does (only
   `--selftest`/`--regression`); the REV counting block is gate-free. But the navigation
   group executes whatever worktree block exists, so a divergent worktree SCORECARD could
   run the live gate through harm-watch and still yield PASS. Structural, not current.

## Finding 1 — HIGH: navigation group executes worktree-derived code under `measured_commit=<REV>` without gating; PASS is reachable with divergent bytes

`pin_assert` (lines 159–176) and `run_pinned` (201–216) enforce the header's promise:
byte mismatch → receipt `measured_commit=UNVERIFIED`, `status=skipped:pin_mismatch`,
`skip_result` → `FAILS+=1` (lines 149–156). I verified every command but one goes through
it: gate selftest/regression (219, 225), action-plan (231), tripwire suites loop (pin once
at 265, skip branches 285/291), frozen r18 (301/324), frozen r19 (332), r16/r17 measure
(341/347), tw-recall (353), fresh-pins (359), census pinned to fleet HEAD (421–434).

The exception is the SCORECARD counting block (lines 366–397). It computes
`SCARD_WT` vs `SCARD_REV` (377–382), but on `SCARD_STATE=mismatch` it only emits a NOTE
(386–387) and **still executes the worktree block** (`bash -s < "$NAV_BLOCK"`, line 393)
and records plain `OK` on rc 0 (396) — zero contribution to `FAILS`. The receipt (389)
writes `measured_commit=$REV_SHA` next to `tool_sha256=$BLOCK_SHA` where `$BLOCK_SHA` is
the worktree block's digest, **never compared to REV's block digest**. That contradicts
the script's own header invariant ("The receipt is only written with
measured_commit=<REV> after asserting that the worktree tool bytes equal REV's bytes …
the command is skipped — the aggregate run exits 1", lines ~9–16) and the exit contract
"Exit: 0 … every pin asserted" (line ~50): the SCORECARD pin is computed but never
asserted.

Proof (fixture harness; committed bytes with only lines 52–53 `ROOT=`/`FLEET=` redirected
to `/tmp/hwfx/repo`, `diff`-verified; stub tools committed at fixture REV
`629f90bb11eebb35d48d65c86a2affde16e6a5a7`; then only the worktree counting block replaced
with `echo NAV-WORKTREE-TAMPERED-BLOCK; touch /tmp/hwfx/TAMPERED-EXECUTED`):

```
$ HARM_TIMEOUT=20 OUTDIR=/tmp/hwfx/out REV=629f90bb… bash /tmp/hwfx/harm-watch-fixture.sh 629f90bb…
exit=0
HARM_WATCH: PASS
NOTE SCORECARD.md worktree differs from REV (mismatch); counting block read from worktree
OK  exit=0  group=navigation  harm-nav-fleet-round-1.txt  bash -s < …SCORECARD.md#Counting-command (REV=629f90bb…)
TALLY total runs=10 ok=10 fail=0 skip=0 baseline=0 blocking=0
receipt: RECEIPT tool=…SCORECARD.md#Counting-command tool_sha256=2cc00f0c… measured_commit=629f90bb… 
receipt: scorecard_sha256=458a147b… scorecard_state=mismatch block_sha256=2cc00f0c…
receipt body: NAV-WORKTREE-TAMPERED-BLOCK ; /tmp/hwfx/TAMPERED-EXECUTED created
```

PASS + exit 0 while the executed block provably differs from REV's block and performs an
uncommitted side effect. In the real lane right now `SCORECARD.md` **is** worktree-modified
(`git status`: `M SCORECARD.md`; whole-file sha `7731ede0…` vs REV `ba581ff4…`) — the
divergence is prose-only today (counting-block digest `8b59b503…` identical both sides,
matching the canonical receipt), so the retained canonical PASS
(`.ufo/waves/round-19/evidence/harm/`, all pins `state=ok`, `scorecard_state=ok`, 22 runs,
0 failures) is itself sound. The defect is in the mechanism, not that artifact.

## Finding 2 — MEDIUM (corollary of 1): the nav block is an ungated arbitrary-code entry point run at `$ROOT`

The block is executed with `cwd=$ROOT` (cd at line 66) via `bash -s`. A tampered worktree
block could invoke `bash tools/mado-verify.sh` with no flags — the live gate, the exact
thing the header promises ("Commands (never the live gate)", line ~19) — and the run could
still certify PASS. Not currently exercisable (block bytes match REV; REV's block is a
pure-python heredoc, no gate call), but "never the live gate" is enforced only for the
static command list, not for this group.

## Finding 3 — the frozen-baseline separation (Q2) is correct; one fragile dependency, failing safe

Section 5 (296–321): only the exact pairs `(0, frozen_match)` and
`(1, frozen_verdict_mismatch)` are routed to `record_baseline` (134–142, G_BASE counter,
never touches `FAILS`); every other rc/label combination — `frozen_error`,
`snapshot_tampered`, `unpinned_legacy`, missing label, timeout rc=124 — falls to
`record_result` and fails. Verified on real data:

```
$ python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen   # tool = REV bytes 367be947…
exit=1 ; stdout line 1 = "MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch" ; stderr empty
canonical summary line 15: BASELINE exit=1 … label=MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch … excluded
canonical harm-tripwire-frozen-round-19.txt line 2: MADO_TRIPWIRE_FROZEN: frozen_match
canonical verdict: HARM_WATCH: PASS (summary line 34), failures=0
```

`emit_frozen` prints the label as the tool's first stdout line
(`tools/mado-tripwire.py:1679`); the tool's only stderr write is the usage message
(`:2087`, arg error → exit 2), so `LABEL=$(sed -n '2p' "$OUT")` (line 310) hits the label
today. Fragility: if a future tool revision prints anything to stderr first (e.g. a
SyntaxWarning while compiling a frozen input — w1 observed exactly such a warning from
round-16 measure.py), the expected baseline flips to a FAIL. Direction is safe: false
failure, never a masked mismatch. Round-19 frozen (332) uses normal failure semantics as
documented.

## Finding 4 — LOW: pin-then-execute TOCTOU

`run_pinned` hashes the worktree file, then executes the **worktree path**; a mid-run
modification would execute bytes different from those certified in the receipt. The
guarantee is pin-time, not exec-time. Same family as Finding 1 but requiring a concurrent
writer; w1 observed sibling rewrites of `tools/mado-verify.sh` mid-wave, so the window is
not hypothetical in this lane's practice.

## Finding 5 — INFO: receipt/summary fidelity nits

- Nav receipt argv records `bash -s < …SCORECARD.md##Counting-command` where `<` and the
  pseudo-path are not real argv (actual invocation is a stdin redirect, line 393).
- Final summary line prints `pins=<path to harm-watch-pins.txt>` (line 456) — reads like a
  count.

## Limits

- The PASS-despite-divergence proof ran against a fixture copy (only `ROOT`/`FLEET` lines
  changed, `diff`-verified); I did not run harm-watch against the real lane (default
  OUTDIR would write lane evidence outside my scope; not needed for the mechanism).
- Read-only inspection of the canonical `.ufo/waves/round-19/evidence/harm/` run; I did
  not re-run the full real suite (sibling `RerunSuites`/`RerunGate` seats cover that).
- The real r18 frozen replay above was executed once by me for label-placement evidence.
- [UNK] whether L1 intends the SCORECARD pin to be advisory (visibility-only) by design;
  the header and exit-contract text say otherwise, which is the inconsistency reported.
- No web fetches; no installs.

## Installs

none
