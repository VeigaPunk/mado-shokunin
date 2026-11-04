# R76ExecC2 — independent C2 execution

Axes: frozen-count agreement; label agreement; executable deletion reachability; scope preservation.

## Commands and exact evidence

All paths below are relative to the lane root unless absolute. The counting command ran from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
python3 -I quality/counters/c2-r76-shapes.py --repo . --rev cb713254ee9926e036e594312fdc61b57825526b --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf --controls .ufo/waves/round-76/controls/c2-cases-r76.json --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC2/run
```

| Command | rc | Contract line / observed result | Per-case disagreements |
|---|---:|---|---|
| Frozen C2 command above | 0 | `MADO_R76_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET rev=cb713254ee9926e036e594312fdc61b57825526b` | Candidate: none; base misses `callee-del-literal`, `callee-del-store`, `dynamic-key-del`, `dynamic-key-module-const` |
| Read-only module import; `is_reader(src)` and `has_guard(src)` on `cases[47:]` | 0 (Eval completed) | 12/12 expected pairs agree; no instrument contract emitted | None |
| `python3 -I -c <retained callee-del-literal-runtime.py contents>` | 0 | `AT_LAUNCH key_present=False`; `GIT_CHILD_RC=128` | None for deletion reachability |
| `python3 -I -c <retained callee-del-store-runtime.py contents>` | 0 | `AT_LAUNCH key_present=False`; `GIT_CHILD_RC=128` | None for deletion reachability |
| `python3 -I -c <retained dynamic-key-del-runtime.py contents>` | 0 | `AT_LAUNCH key_present=False`; `GIT_CHILD_RC=128` | None for deletion reachability |
| `python3 -I -c <retained dynamic-key-module-const-runtime.py contents>` | 0 | `AT_LAUNCH key_present=False`; `GIT_CHILD_RC=128` | None for deletion reachability |

Evidence directory: `.ufo/waves/round-76/w1/R76ExecC2/`.
- `counter-output.txt`: full unmodified combined stdout/stderr from the counting command.
- `counter-rc.txt`: exact exit status, `0`.
- `direct-labels.json`: all twelve source strings, expectations, actual pairs and disagreements; imported working-tree module SHA256 `2638d44f8da59fc847a9e17aa894c63b45b11bee4d1536f7ab0b894b02987ef8`. Import disabled bytecode writes.
- `runtime-receipt.json`: exact command arguments, stdout, stderr, return codes, git-init status and asserted fixture top-level for each runtime case.
- Four `*-runtime.py` files: exact `-c` payloads, retained as reproducibility evidence rather than production changes.

The command reports controls SHA256 `df9e89841ed560613d7a05ad50f345b2d6bbf0d8e40a98f51e8b8134492b3948` and confirms all 47 held controls carried unchanged. It agrees with the committed C2 measurement counts, with the explicitly requested freeze revision instead of that older receipt's revision. The pre-freeze baseline also identifies the same four base misses. No instrument was repaired.

## Twelve direct labels and source hand-check

Every row is a reader. Expected and measured pairs below use `(reader, guard)`.

| Case | Expected | Measured | Source-based rationale |
|---|---|---|---|
| callee-del-literal | (true,false) | (true,false) | Called helper deletes literal guard key from the original mapping before launch. |
| callee-del-store | (true,false) | (true,false) | Same cancellation, after a subscript guard store. |
| callee-del-param-rebound-live | (true,true) | (true,true) | Helper copies its argument before deletion; caller mapping retains guard. |
| dynamic-key-del | (true,false) | (true,false) | Single local binding resolves the deleted key to the guard key. |
| callee-del-other-key | (true,true) | (true,true) | Deletes PATH, not the guard. |
| callee-del-dead-branch | (true,true) | (true,true) | Delete is in literal-false branch. |
| callee-never-called | (true,true) | (true,true) | Deleting helper is never invoked. |
| callee-called-after-launch | (true,true) | (true,true) | Original guard is still present at launch; later deletion does not cancel it for that launch. |
| callee-del-param-rebound | (true,true) | (true,true) | Parameter is rebound to a different mapping; caller mapping is not deleted. See reachability caveat below. |
| dynamic-key-other | (true,true) | (true,true) | Key resolves to PATH. |
| dynamic-key-rebound | (true,true) | (true,true) | Final key value is PATH, not guard. |
| dynamic-key-module-const | (true,false) | (true,false) | Module constant resolves to guard key. |

Disagreements: **none**.

## Executable reachability

Four isolated fixture directories were created with `mktemp -d` under the assigned scratch root, then `git -C "$D" init -q`. `git -C "$D" rev-parse --show-toplevel` matched each exact directory (retained in the JSON receipt). No commit, index write, throwaway identity, fleet-repository mutation or external-state change was made.

Each payload executes the frozen source unchanged via `compile(..., '<fixture>', 'exec')`, supplies the missing `subprocess` import and calls `run(fixture_root)`. A Python trace observes the actual mapping immediately before the source's real subprocess launch; no mocked launcher or rewritten delete is used. All four original mappings lack the guard key at launch. Thus the callee and dynamic-key deletes really execute and remove the key.

The fixture repositories deliberately have no commits. Each real `git show HEAD:a` returns 128 and stderr `fatal: invalid object name 'HEAD'.`; each enclosing Python process returns 0 because the frozen source uses unchecked `subprocess.run`. These runs demonstrate deletion and launch reachability, **not** successful object retrieval or authenticated Git behavior. The exact stderr and child status are retained, not suppressed.

## Risks, limits and scope

- Hand inspection finds `callee-del-param-rebound` would raise `KeyError` when deleting the guard key from a newly rebound mapping containing only PATH, before its launch. This case was not among the four executable fixtures; its `(true,true)` label is a syntactic guard classification, not evidence of a reachable successful launch. The `...rebound-live` case supplies the non-raising copy counterpart.
- The JSON note says thirteen appended cases, but `59 - 47 = 12` and the frozen declaration lists twelve. The note also mentions a name-bound-after-delete negative absent from this frozen set. No frozen source or label was changed.
- The counter's retained diagnostic calls the base the held round-74 rule; its actual path is `quality/counters/c2-r75-shapes.py`. This is reported verbatim, not repaired.
- LSP tooling is unavailable in this seat's exposed inventory; function definitions were read directly. No symbol refactor was needed.
- Only the assigned counting command, direct classifier calls and four requested runtime fixtures were exercised. No build, lint, formatter or broader test suite ran. No tools were installed or upgraded.
- No production implementation changed; only this advisory report and its exclusive evidence directory were written outside scratch. Committed evidence was read only. Scratch was removed after retaining all cited receipts.
- Blockers: none for the assigned measurements. Any integration gates remain the parent's responsibility.

## Self-evaluation

Accuracy 4/5: exact outputs retained; runtime scope explicitly excludes successful Git reads. Completeness 4/5: all requested counts, twelve labels and four runtime cases covered; remaining eight runtime behaviors are source reasoning only. Clarity 4/5: per-case tables distinguish syntactic guards from runtime reachability, though full payloads live in linked evidence. Actionability 4/5: exact payloads and receipts retained; scratch must be freshly recreated to replay. Conciseness 4/5: detailed evidence adds length but avoids ambiguity. Overall 4.0/5. Improvements, in priority order: clarify the frozen note's case count and bound the rebound-negative wording at integration; keep any successful-Git-read exercise separate from this deletion-only claim. User agreement is an inference, not an observed outcome.
