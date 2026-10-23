# Round-24 carry — frozen round-23 wave-2 discovery population

Registered 2026-10-23. This directory freezes, byte-exact, the round-23 wave-2 regression and
discovery fixtures named by five wave-2 reports, and records one reference run of the base
classifier over all of them. **No file under `tools/` was changed.**

## Layout

```
carry/
  README.md          this file
  manifest.json      28 entries: path, origin path, sha256, bytes, report, reported status, base-scan result
  base-run.txt       base-classifier reference run, one block per fixture plus a summary table
  fixtures/<report>/*.jsonl
```

`<report>` is the wave-2 report basename: `AttackLateCell`, `AttackRecallRegress`,
`AttackFrameScopes`, `AttackEscapeGate`, `ReClosureNeighbour`.

| Population | Fixtures | Report | What the population tests |
|---|---|---|---|
| `AttackLateCell` | 5 | `.ufo/waves/round-23/w2/reports/AttackLateCell.md` | Late enclosing-cell rebinding: a local is rebound after a nested `def` and before the call, including calls through sibling relays and `nonlocal`; plus repeated invocations of one `outer` (frame keying). |
| `AttackRecallRegress` | 4 | `.ufo/waves/round-23/w2/reports/AttackRecallRegress.md` | Callback-store recall of the escape-gated sweep: callbacks stored through `AugAssign`, `AnnAssign`, a try/`except` `__call__`, a second unfollowed dunder call, and a closure stored in a dict. |
| `AttackFrameScopes` | 4 | `.ufo/waves/round-23/w2/reports/AttackFrameScopes.md` | Scope-chain identity: per-invocation frames (two invocations of one `def`), `own_names` over-approximation through a nested binder, and under-approximation for `match` capture binders. |
| `AttackEscapeGate` | 5 | `.ufo/waves/round-23/w2/reports/AttackEscapeGate.md` | Stores the escape gate did not see: `global` and `nonlocal` bare-name stores, `dict.update(k=callee)`, generator `yield`, and a wrapper closure. |
| `ReClosureNeighbour` | 10 | `.ufo/waves/round-23/w2/reports/ReClosureNeighbour.md` | Closure lifetime: the critic's three fixtures (loop late binding, nonlocal rebound, factory closure reads a rebound global) plus seven stored-callable neighbours where the stored value's free name is rebound after the handoff (subscript, attribute and `append` stores; direct and indirect calls). |

## Provenance and byte-exactness

Every fixture was copied with `shutil.copyfile` from its `origin_path` in `manifest.json`. After
each copy, `sha256(origin) == sha256(copy) == manifest.sha256` and `bytes` matches the file size.
All 28 copies verified.

- 19 fixtures are lane-resident copies of files under `.ufo/waves/round-23/`:
  - `w2/out/AttackLateCell/fixtures/` (4)
  - `w2/out/AttackRecallRegress/fixtures/` (4)
  - `w2/out/AttackFrameScopes/fixtures/` (4)
  - `w2/out/AttackEscapeGate/fixtures/` (4)
  - `w1/out/CritClosureNeighbour/fixtures/` (3, the critic fixtures that `ReClosureNeighbour` re-measured)
- 9 fixtures were scratch-resident when the reports were written and are frozen here for the
  first time:
  - `AttackLateCell/SecondFrameRelayInvokesFirstClosure` from
    `/fast/scratch/hyaku/mado-r23/w2/AttackLateCell/probes/fixtures/`. The report gives no sha256
    for it; its fenced Python block in the report is equal to the fixture's `code` payload
    (checked by extracting both and comparing).
  - `AttackEscapeGate/EscapeNonlocalHook` from
    `/fast/scratch/hyaku/mado-r23/w2/AttackEscapeGate-r2/fixtures/`; sha256 prefix `fcee11c1…4986`
    matches the report addendum.
  - The seven `ReClosureNeighbour` regressions (`W2c-1..4`, `W2e-1`, `W2e-2`, `W2f-2`) from
    `/fast/scratch/hyaku/mado-r23/w2/ReClosureNeighbour/w2/`. Their full sha256 prefixes match
    the report: `b7a8d94c…`, `e6c78baf…`, `ba2f8e4f…`, `9b16e20c…`, `35e30326…`, `71df6085…`,
    `5ebe6a97…`.

Each entry also carries a `report_path` and the sha256 of that report in `manifest.json` under
`populations`, so the status text can be checked against the report bytes.

## Classifier measured

`base-run.txt` is the **base classifier**, i.e. the pre-C1 bytes:

| Field | Value |
|---|---|
| Path | `tools/mado-tripwire.py` (lane root) |
| sha256 | `sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` |
| Identity | byte-identical to `.ufo/waves/round-23/evidence/tool-base-cd9da20c.py` |
| Python | 3.14.8 |

The five reports measured two other tool states, which are **not** re-run here:

- old C1 tip `2f1134f3` — `sha256:41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`
- repaired tip `3732c7a7` — `sha256:e1dc8029ced9fcc62d458b8143209605f34b60c9e4cfe6d8f66515c2efce4a47`

Their verdicts are quoted per fixture in `reported_status` (`at_tip_2f1134f3`,
`at_tip_3732c7a7`). The reports' own runners (`probe.py`, `run.py`, `deliver.py`) were not re-run:
they depend on seat-local scratch and the round-21 `scan` helper, and they derive execution truth
with a recording fake `subprocess`. Only the classifier CLI itself was run, once per fixture.

## Reference run

```
cd .ufo/waves/round-24/carry
timeout 60 python3 -I ../../../../tools/mado-tripwire.py --scan fixtures/<report>/<fixture>.jsonl
```

One child per fixture, `RLIMIT_AS` = 384 MiB, wall timeout 60 s, `python3 -I`. Exit 0 means no
findings, exit 1 means findings. Result across the 28 fixtures: 18 exit 1, 10 exit 0, no error or
timeout. The exact stdout of every scan is in `base-run.txt`; the parsed values are also in
`manifest.json` under `entries[].base_scan`.

The run reproduces every base value the five reports state for these fixtures, including the
honest abstentions:

- `AttackLateCell`: `LateEnclosingLocalViaRelay` gives one false `observed` host mutation
  (`pacman -S r23w2-relay-foreign`) and misses the executed `pacman -Q r23w2-late-cell`;
  `NonlocalRebindThenCallInSibling` gives no rows with `unparsed_spawns` 1;
  `LoopClosureCalledAfterLoop` gives no rows with `unparsed_spawns` 0;
  `SecondFrame*` report the first-frame query row with `unparsed_spawns` 1.
- `AttackRecallRegress`: all four report the executed `pacman -S` as a `lead` row.
- `AttackFrameScopes`: three report the correct query at `observed`; `MatchCaptureBinderNotOwned`
  gives no rows with `unparsed_spawns` 1.
- `AttackEscapeGate`: four are `lead` rows and `EscapeWrapperClosure` is `observed`.
- `ReClosureNeighbour`: `W2c-1..4` and `W2f-2` give no rows with `unparsed_spawns` 1; `W2e-1/2`
  report the final query at `observed` with `unparsed_spawns` 1; `TwoFactoryClosureReadsReboundGlobal`
  reports the query at `observed` with `unparsed_spawns` 1.

## Limits

- The fixtures are inert JSONL transcripts. This freeze and the reference run did not execute
  them; execution truth used by the reports came from their recording fake-`subprocess` child and
  is not re-derived here. Host behaviour stays `[UNK]`.
- The seven `ReClosureNeighbour` regressions have no post-repair verdict at `3732c7a7` in the
  report or in any later round-23 file found by search, so their status at the r23 close tip is
  unmeasured. `LoopClosuresLateBinding`, `NonlocalReboundAfterFactory` and
  `TwoFactoryClosureReadsReboundGlobal` in that population were measured only at `2f1134f3`.
- The population is registered data, not a threshold. It is referenced by no counter and no file
  under `tools/`. A future comparison must name the tool sha it measured, and pass/fail must be
  derived from the reports' own rules rather than from this README.
