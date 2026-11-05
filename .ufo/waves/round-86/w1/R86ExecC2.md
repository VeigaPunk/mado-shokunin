# R86ExecC2 — independent re-execution of claim C2 (runbook clause observations)

Seat: R86ExecC2 (executor, leaf). Wave: round-86 w1. Instrument: `quality/counters/c2-r86-clause-observations.py`
(read and run only — frozen, not edited). Freeze revision: `237ecf4e69a4986108f719f3beeafe111adaa033`.

## Execution note (fixture)

The frozen predicate binds `SKILL.md` and `tools/mado-barfoot.py` byte-equal to `--rev` (`tree=bound`).
The lane's working tree is now at `b33afc08` (two commits past freeze); `SKILL.md` differs from the
freeze bytes (`git diff 237ecf4e..HEAD -- SKILL.md` → +2 lines), so running the counter against the
live tree fails closed at setup:

```
$ python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev 237ecf4e... \
    --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
    --carried .ufo/waves/round-85/controls/c2-cases-r85.json \
    --scratch-root /fast/scratch/hyaku/mado-r86/R86ExecC2/c2
MADO_R86_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)
rc=2
```

Per lane precedent (r18/r19 `MutMeasureR17`/`MutGateOM` reports), the counter was re-executed against a
read-only git clone checked out detached at the freeze revision — no git/jj mutation of the lane:

```sh
S=/fast/scratch/hyaku/mado-r86/R86ExecC2
mkdir -p "$S/c2"
git clone --quiet --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$S/c2/repo"
git -C "$S/c2/repo" checkout --quiet --detach 237ecf4e69a4986108f719f3beeafe111adaa033
test "$(git -C "$S/c2/repo" rev-parse --show-toplevel)" = "$S/c2/repo"   # asserted
```

`mado-barfoot.py` is byte-identical between freeze and HEAD; `SKILL.md` is not — the clone is the
only way to measure the freeze bytes. The counter script itself was run from the lane path
(`/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py`),
unmodified; its self-check reads `__file__`, which is the frozen file.

## Result

Command (cwd = clone root):

```sh
cd /fast/scratch/hyaku/mado-r86/R86ExecC2/c2/repo
TMPDIR=/fast/scratch/hyaku/mado-r86/R86ExecC2/c2 python3 -I \
  /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py \
  --repo . --rev 237ecf4e69a4986108f719f3beeafe111adaa033 \
  --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
  --carried .ufo/waves/round-85/controls/c2-cases-r85.json \
  --scratch-root /fast/scratch/hyaku/mado-r86/R86ExecC2/c2/mut-scratch
```

Wall time ≈ 80 s (37 live executions + 37 mutant re-runs). **rc = 0.**

Final line, verbatim:

```
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 superseded=active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,omarchy-version,tray-items,tray-methods,version,waybar-process,workspaces-count mutants=37 killed=37 verdict=TARGET_MET rev=237ecf4e69a4986108f719f3beeafe111adaa033 tree=bound
```

Control line, verbatim:

```
MADO_R86_CONTROL: superseded=active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,omarchy-version,tray-items,tray-methods,version,waybar-process,workspaces-count status_classes=2/37 held_rule_new_case=0/1 new_case=border-size-int held_rule=round85(regex-kind-search,no-clause-observation)
```

Every `MADO_R86_PROBE` row reports `match=yes` with `clauses=…` equal to `declared=…`; every
`MADO_R86_MUTANT` row reports `killed=yes` (matched counts ranged 0/37–36/37; `negatives-skipped`
dropped all cases to 0/37, `samples-skipped` to 5/37). Full output retained in scratch during the run
(`/fast/scratch/hyaku/mado-r86/R86ExecC2/c2/run.txt`); scratch removed before yield per seat rules.

### New-witness row (SKILL.md, freeze rev)

The added runbook section `### Executable runbook rows (round 86)` binds case `border-size-int`
to SKILL.md line 320, verbatim:

```
| `set -o pipefail; hyprctl getoption general:border_size -j \| jq -r .int` | ok | unanchored `[0-9]+` matched against one whole line: a bare non-negative integer | 2 / 3 |
```

Case fields (from `.ufo/waves/round-86/controls/c2-cases-r86.json`): `kind=regex`,
`value="[0-9]+"` (unanchored), `anchor="line"`, `argv=["/bin/sh","-c","set -o pipefail; hyprctl
getoption general:border_size -j | jq -r .int"]`, samples `1`/`2`, negatives `0 extra` (rc 0),
`-1` (rc 0), `0` (rc 127). Held round-85 rule scores it 0/1 (`held_rule_new_case=0/1`); the r86 rule
matches it 1/1. Verified live on this host: `hyprctl getoption general:border_size -j | jq -r .int`
→ `0`, rc 0.

## Mutant population audit (mechanical)

Method: extracted `MUTATIONS` by importing the frozen file (37 entries — matches `MUTANTS = 37`).
Reproduced the counter's own exclusion — `body = source[:index("MUTATIONS = [")] +
source[index("\n]\n", lit_start)+3:]` — and counted each anchor in `body`. For each entry with
exactly one hit, the anchor's byte offset was converted to a file line and the enclosing function
was resolved from an AST of the literal-free body (line numbers mapped back to the real file by
the 113-line literal block). Result: **all 37 anchors occur exactly once outside the literal list,
and every one lands on the scoring path — none in `held_case_correct`, `selftest`, or the
module level.**

| mutant | file line | function |
|---|---|---|
| int-range-lower-open | 475 | matches |
| json-required-ignored | 358 | fields_ok |
| sorted-unique-dropped | 481 | matches |
| empty-accepted | 414 | matches |
| refusal-stage-blind | 537 | special_matches |
| refusal-rc-blind | 537 | special_matches |
| lines-any-line | 419 | matches |
| lines-min-lines-dropped | 419 | matches |
| chord-mod-word-blind | 442 | matches |
| chord-key-padded | 446 | matches |
| chord-arrow-blind | 433 | matches |
| chord-mod-duplicate-accepted | 444 | matches |
| chord-min-chords-dropped | 451 | matches |
| state-rc-blind | 520 | special_matches |
| state-enum-blind | 518 | special_matches |
| action-prefix-blind | 459 | matches |
| action-empty-accepted | 462 | matches |
| action-arrow-inside-accepted | 464 | matches |
| pid-rc-blind | 532 | special_matches |
| pid-numeric-blind | 527 | special_matches |
| pid-zero-accepted | 529 | special_matches |
| pid-single-only | 531 | special_matches |
| lines-shape-floor-dropped | 419 | matches |
| bool-shape-blind | 468 | matches |
| bool-false-refused | 468 | matches |
| lines-shape-any-line | 419 | matches |
| producer-rc-masked | 515 | special_matches |
| pipeline-guard-stripped | 260 | run |
| any-nonzero | 402 | matches |
| status-class-ignored | 402 | matches |
| exact-any-nonzero | 380 | status_ok |
| signal-any-nonzero | 382 | status_ok |
| signal-as-exit | 383 | status_ok |
| regex-anchor-dropped | 411 | matches |
| line-anchor-prefix | 392 | line_anchored |
| negatives-skipped | 563 | case_correct |
| samples-skipped | 559 | case_correct |

Notes on shared anchors (same anchor string serves two mutants — verified legal, one occurrence
each):

- `refusal-stage-blind` / `refusal-rc-blind` share the `return rc == value["rc"] and ("ERROR
  (stage=%s " …)` tail of `special_matches` (line 537); the two replacements differ
  (`"ERROR (" in stdout` vs dropping the rc conjunct).
- `lines-any-line` / `lines-min-lines-dropped` / `lines-shape-floor-dropped` /
  `lines-shape-any-line` all anchor on the `lines_shape` floor+all-match block (line 419); the
  replacements differ per mutant.
- `bool-shape-blind` / `bool-false-refused` share the `bool_property` return line (468).
- `any-nonzero` / `status-class-ignored` share the `status_ok` gate in `matches` (402).

Scoring-path check: `run` is invoked for every case argv (and every mutant re-run), `status_ok`,
`matches`, `special_matches`, `line_anchored`, `fields_ok` and `case_correct` are all called from
`case_correct`/`main`'s live loop — the path that produces `matched`, `shapes`, `clauses_observed`
and therefore rc. `held_case_correct` (lines 574–593) and `selftest` (601–769) contain none of the
37 anchors. **No mutant-only-mutates-the-held-control or selftest hole exists in this population.**

Caveat, stated not hidden: `pipeline-guard-stripped` anchors inside `run()` (line 260), which also
serves the counter's own bookkeeping subprocesses (`git show`, the mutant re-runs). It is on the
scoring path because it rewrites the argv that executes every runbook row; its kill (34/37) is
measured, not assumed.

## Findings / defects

None found in the instrument. One operational observation, not a defect: the counter cannot be run
against the lane working tree once the tree advances past the freeze revision — this is the frozen
`tree=bound` clause working as designed (it failed closed with rc 2, naming the file). Any later
seat re-running the exact seat command against `.` will hit the same setup error unless it also
uses a freeze-rev checkout; that is a property of the frozen predicate, reported for the fleet's
awareness.

## Verdict

C2 re-executed independently: **TARGET_MET reproduced** — rc 0, `matched=37/37`, `shapes=27/27`,
`anchors=37/37`, `rows=37/37`, `clauses_observed=37/37`, `mutants=37 killed=37`,
`held_rule_new_case=0/1`, `tree=bound`, `verdict=TARGET_MET` at rev `237ecf4e…`. Mutant audit:
37/37 anchors unique outside the literal list, all on the scoring path, zero held-control/selftest
holes.
