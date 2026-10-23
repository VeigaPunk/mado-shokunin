# ExecCarryFreeze — round-24 wave 1 (executor)

Assignment: routed round-23 defect 6 / registration item 6 — freeze the round-23 wave-2
regression fixtures as a registered discovery population, without changing `tools/`.

**Verdict: population frozen and measured.** 28 fixtures from five wave-2 reports were copied
byte-exact into `.ufo/waves/round-24/carry/fixtures/<report>/`; `manifest.json` (path, origin
path, sha256, bytes plus report provenance), `README.md` and `base-run.txt` were written. The
base classifier (`sha256:cd9da20c…ea84`) was run once per fixture under 60 s / 384 MiB caps and
its output reproduces every base value the five reports state for these fixtures. No file under
`tools/` was edited; no git/jj write was run.

## 1. Population

Reports read in full: `.ufo/waves/round-23/w2/reports/{AttackLateCell,ReClosureNeighbour,
AttackRecallRegress,AttackFrameScopes,AttackEscapeGate}.md`. Fixtures named by those reports:

| Report | Fixtures | Report sha256 | Origin |
|---|---|---|---|
| `AttackLateCell` | 5 | `sha256:f5622d77…52644d` | 4 lane (`w2/out/AttackLateCell/fixtures/`), 1 scratch (`…/AttackLateCell/probes/fixtures/`) |
| `AttackRecallRegress` | 4 | `sha256:3cb5410c…d0118e` | 4 lane (`w2/out/AttackRecallRegress/fixtures/`) |
| `AttackFrameScopes` | 4 | `sha256:627a66b7…916555` | 4 lane (`w2/out/AttackFrameScopes/fixtures/`) |
| `AttackEscapeGate` | 5 | `sha256:21822b88…fad1d5` | 4 lane (`w2/out/AttackEscapeGate/fixtures/`), 1 scratch (`…/AttackEscapeGate-r2/fixtures/`) |
| `ReClosureNeighbour` | 10 | `sha256:245c2270…b6c326` | 3 lane (`w1/out/CritClosureNeighbour/fixtures/`), 7 scratch (`…/ReClosureNeighbour/w2/`) |

(Full hashes are in `manifest.json`; prefixes are abbreviated here only for width.)

Two scope decisions, stated so they can be overruled by the L1:

- `ReClosureNeighbour` names ten fixtures: the critic's three closure fixtures it re-measured, and
  its own seven stored-callable regressions (`W2c-1..4`, `W2e-1`, `W2e-2`, `W2f-2`). The report
  says its authored fixtures were "uncommitted scratch files under `w2/`" and that "the seven
  regressions would then need a committed repro" if the L1 required committed fixture data. This
  ticket is that requirement, so the seven are included and are frozen in the lane for the first
  time.
- Two addendum-named fixtures are also included: `AttackLateCell/SecondFrameRelayInvokesFirstClosure`
  (regressed at the repaired tip `3732c7a7`) and `AttackEscapeGate/EscapeNonlocalHook` (regressed at
  `2f1134f3`, repaired at `3732c7a7`). Both were scratch-resident and are named in their reports.

Excluded: exploratory sweep cases that the reports describe without naming a file, and the
`ReClosureNeighbour` diagnostic/round-20 reconstructions, which are scratch reconstructions rather
than named fixtures.

## 2. Freeze method and integrity

Copy: Python 3.14.8, `shutil.copyfile(origin, dest)` per fixture, then a read-back compare:

```
src_b = open(origin,'rb').read(); dst_b = open(dest,'rb').read(); assert src_b == dst_b
sha256(dst_b) -> manifest.sha256; len(dst_b) -> manifest.bytes
```

Result: **28/28 byte-identical**. `manifest.json` was then validated independently: every
`path` resolves under `carry/`, and every file's sha256 and byte count equal the manifest entry
(`bad: []`). Totals: 19 lane-origin fixtures, 9 scratch-origin fixtures, 12,828 fixture bytes.

Cross-checks that the scratch-origin copies are the measured bytes, not later edits:

- `ReClosureNeighbour` seven — report prefixes match the frozen files:
  `W2c-1 b7a8d94c…`, `W2c-2 e6c78baf…`, `W2c-3 ba2f8e4f…`, `W2c-4 9b16e20c…`,
  `W2e-1 35e30326…`, `W2e-2 71df6085…`, `W2f-2 5ebe6a97…` (full hashes in the manifest).
- `EscapeNonlocalHook` — report prefix `fcee11c1…4986` matches
  `sha256:fcee11c15640f829b3dd247aa33908f193ba0775310914cb77c9346e12c54986`.
- `SecondFrameRelayInvokesFirstClosure` — the report gives no sha256. I extracted the fixture's
  `arguments.code` and the fenced Python block from the report and compared them: equal.

## 3. Base-classifier reference run

Tool: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`,
`sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` — the same bytes as
`.ufo/waves/round-23/evidence/tool-base-cd9da20c.py`. Re-hashed after the run: unchanged.

Method: one child per fixture, driven by Python `subprocess.run` with
`preexec_fn` setting `RLIMIT_AS = 384 MiB`, `timeout = 60 s` (outer driver cap 90 s so `timeout`
owns the kill), cwd `carry/`, invocation:

```
timeout 60 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py \
  --scan fixtures/<report>/<fixture>.jsonl
```

28 runs, 0 errors, 0 timeouts, 0 stderr bytes: 18 exit 1 (findings), 10 exit 0 (no findings).
Verbatim stdout plus a parsed summary table is in `carry/base-run.txt`
(`sha256:a4f27aa772d1ae8be36942eceb71e09f9429150c98ef885c94834263bb9e5337`). The reports' own
seat runners (`probe.py`, `run.py`, `deliver.py`) were not re-run: they depend on seat-local
scratch files (base/tip tool copies, truth harnesses) and the round-21 `scan` helper, and derive
execution truth with a recording fake `subprocess`; this run records the classifier's own output,
which is what the ticket asked for.

## 4. Base results (from `base-run.txt`)

`exit·lead·obs·unparsed` = process exit, lead findings, observed findings, `unparsed_spawns`.

| Fixture | Base result |
|---|---|
| `AttackLateCell/LateEnclosingLocalViaRelay` | 1·0·1·0 — false observed `pacman -S r23w2-relay-foreign`; executed `-Q r23w2-late-cell` missed |
| `AttackLateCell/LoopClosureCalledAfterLoop` | 0·0·0·0 — silent |
| `AttackLateCell/NonlocalRebindThenCallInSibling` | 0·0·0·1 — disclosed |
| `AttackLateCell/SecondFrameInvokesFirstFrameClosure` | 1·0·1·1 — observed `-Q r23w2-first-invocation` |
| `AttackLateCell/SecondFrameRelayInvokesFirstClosure` | 1·0·1·1 — observed `-Q r23w2-first-relay` |
| `AttackRecallRegress/RecallConditionalAugAssignStore` | 1·1·0·0 — lead `-S r23y-aug-cond` |
| `AttackRecallRegress/RecallTryExceptDunderCall` | 1·1·0·0 — lead `-S r23y-try-dunder` |
| `AttackRecallRegress/RecallSecondCallDunder` | 1·1·0·0 — lead `-S r23y-second-dunder` |
| `AttackRecallRegress/RecallClosureStoredInDict` | 1·1·0·0 — lead `-S r23x-closure-dict` |
| `AttackFrameScopes/FrameReusedBySecondInvocation` | 1·0·1·0 — observed `-Q w2-afs-first-frame` |
| `AttackFrameScopes/FrameReusedBothClosuresCalled` | 1·0·2·0 — observed both `-Q w2-afs-both-*` |
| `AttackFrameScopes/NestedBinderFreezesLateGlobal` | 1·0·1·0 — observed `-Q w2-afs-late-global` |
| `AttackFrameScopes/MatchCaptureBinderNotOwned` | 0·0·0·1 — disclosed |
| `AttackEscapeGate/EscapeGlobalHook` | 1·1·0·0 — lead `-S r23w2-global-hook` |
| `AttackEscapeGate/EscapeDictUpdateKeyword` | 1·1·0·0 — lead `-S r23w2-dict-update` |
| `AttackEscapeGate/EscapeYieldGenerator` | 1·1·0·0 — lead `-S r23w2-yield` |
| `AttackEscapeGate/EscapeWrapperClosure` | 1·0·1·0 — observed `-S r23w2-wrapper-closure` |
| `AttackEscapeGate/EscapeNonlocalHook` | 1·1·0·0 — lead `-S r23w2-nonlocal-hook` |
| `ReClosureNeighbour/LoopClosuresLateBinding` | 0·0·0·0 — silent |
| `ReClosureNeighbour/NonlocalReboundAfterFactory` | 0·0·0·1 — disclosed |
| `ReClosureNeighbour/TwoFactoryClosureReadsReboundGlobal` | 1·0·1·1 — observed `-Q r23cc-global-at-call` |
| `ReClosureNeighbour/W2c-1…called-later` | 0·0·0·1 — disclosed |
| `ReClosureNeighbour/W2c-2…never-called` | 0·0·0·1 — disclosed |
| `ReClosureNeighbour/W2c-3…attribute…` | 0·0·0·1 — disclosed |
| `ReClosureNeighbour/W2c-4…append…` | 0·0·0·1 — disclosed |
| `ReClosureNeighbour/W2e-1…direct-call` | 1·0·1·1 — observed `-Q w2e-direct-final` |
| `ReClosureNeighbour/W2e-2…direct-call` | 1·0·1·1 — observed `-Q w2e-append-final` |
| `ReClosureNeighbour/W2f-2…factory-local` | 0·0·0·1 — disclosed |

Every row agrees with the base values stated in its report, including the abstentions
(`unparsed_spawns` 1 with no rows; `LoopClosureCalledAfterLoop` and `LoopClosuresLateBinding`
silent on both), the four `lead` rows in `AttackRecallRegress`, and the false observed row in
`LateEnclosingLocalViaRelay`. This is the check that the frozen bytes are the measured bytes.

## 5. Files written

Under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/carry/`:

| Path | Bytes | sha256 |
|---|---|---|
| `manifest.json` | 31,668 | `sha256:6063898fbaa5ebb8e1b01cc473c1a1fe48299b0acae4cdebf0dd840e363d2fca` |
| `README.md` | 7,447 | `sha256:fe5b0f207b6c2e74e2658d5b56c96d8889d31ade5a6c818932c975a4e85cea59` |
| `base-run.txt` | 35,581 | `sha256:a4f27aa772d1ae8be36942eceb71e09f9429150c98ef885c94834263bb9e5337` |
| `fixtures/<report>/*.jsonl` | 28 files, 12,828 total | per-file in `manifest.json` |

Plus this report. Nothing else in the lane was written by this seat: `tools/` has no `__pycache__`
or `.pyc`, and `tools/mado-tripwire.py` still hashes `cd9da20c…ea84`.

## 6. Observation vs inference

- Observation: the 28 copies are byte-identical to their origins and all base-scan outputs match
  the reports' base columns. No report claim beyond the base column was re-measured.
- Observation: no round-23 file names a post-repair (`3732c7a7`) verdict for the seven
  `ReClosureNeighbour` regressions, so their status at the r23 close tip is unmeasured; the
  manifest records `at_tip_3732c7a7: not measured` for those ten fixtures, where `not measured`
  covers the critic's three as well.
- [INFERENCE] The two addendum fixtures are useful population members because each was a measured
  regression at one tool state and a pass at another; the frozen bytes let a future tip be compared
  without recreating the shapes. This is why they were included, not because the r23 defect
  routing named them explicitly.
- Not established: any host behaviour. The fixtures are inert JSONL tool-call transcripts; this
  seat neither executed them nor re-derived execution truth. Host behaviour stays `[UNK]`.

## 7. Risks, limits, blockers

- Scratch origins are not durable. `/fast/scratch/hyaku/mado-r23/w2/` may be swept; the nine
  scratch-origin fixtures are now in the lane, so no re-copy is needed, but their `origin_path`
  values may stop resolving. `sha256` in the manifest remains the authority.
- The population is data only. It is referenced by no counter, no `tools/` code and no automated
  gate; wiring it into a future comparison is the L1's call.
- The REV-level no-harm guard (`git diff --quiet <base> <tip> -- tools/`) is the L1's to run; this
  seat only confirms the classifier bytes it ran.
- No blockers. No installs or updates. No git/jj write; no host change; no compositor or service
  interaction.

## 8. Command/receipt index

- Copy + hash verify: Python 3.14.8, `shutil.copyfile` + `assert src_b == dst_b`; output
  "28 fixtures copied, all byte-identical".
- Manifest build: Python, `json.dumps(indent=1)`; validation re-read every entry: `bad: []`,
  `base-run sha match: True`.
- Base run: 28 × `timeout 60 python3 -I …/tools/mado-tripwire.py --scan <fixture>` with
  `RLIMIT_AS` 384 MiB; `tool unchanged: True`; receipt `carry/base-run.txt`.

Verdict: **done** — registered discovery population frozen, manifest/README/reference run landed,
base behaviour reproduced 28/28, `tools/` untouched.
