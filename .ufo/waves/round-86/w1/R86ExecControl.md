# R86ExecControl — frozen do-nothing controls

Axes: calibration (C1 refusal-record discrimination); operability (C2 clause observation).
Freeze: `237ecf4e69a4986108f719f3beeafe111adaa033`.

## Findings

- C1 requested old CLI against r86 controls exits **2**, before scoring: its fixed population is 72, supplied population 75. There is **no CLI score**; do not label this TARGET_MISSED or 75/75. The supplementary diagnostic imports the unchanged frozen r85 module and calls its existing `run_cases` over all 75 cases: **75/75**, rc 0. No frozen code/constants/control data were edited.
- C1 r86 control: honest **75/75**, held r85 tool **75/75**, flooding **48/75**, held-rule flooding **75/75**; carried **72/72**, tool selftest **152/152**. Thus the useful discriminator is the scoring rule, not a tool change. The non-refusal 48 still score under flooding; this is not a claim that all flood outputs are refused.
- C2 old CLI: **36/36**, **33/37** kills, rc **1**, TARGET_MISSED. All four required survivors remain visible: `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped`, each **36/36 killed=no**.
- C2 new witness: `border-size-int` matches with observed anchors/samples/negatives **1/2/3**; **held_rule_new_case=0/1**. Honest rows **37/37**, shapes **27/27**, clauses **37/37**, rc 0 with MUTANTS_SKIPPED.

## Reproduction and isolation

The retained control runner extracts regular files/directories from `git archive` at the freeze into exclusive scratch and attaches a symlink to the existing object database for read-only `git show` / revision resolution. It performs no git mutation, commit, checkout, worktree registration or identity setup. Historical archive symlinks are excluded; measured C2 files/fixtures passed the instrument's own byte binding (`tree=bound`). All four independent controls run concurrently. Reproduce the complete battery with:

```sh
S=/fast/scratch/hyaku/mado-r86/R86ExecControl; mkdir -p -- "$S"; trap 'rm -rf -- "$S"' EXIT; TMPDIR="$S" /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/w1/ctrl-r86-controls.py "$S"
```

Driver rc: **0** means the receipt collector completed, **not** that every instrument returned zero. Individual return codes are retained below. Scratch is removed by the shell EXIT trap. Diagnostic counter runs deliberately use `--no-mutants`; no r86 mutant kill target is claimed by this seat.

## Exact battery commands, return codes and stdout

```text

## c1-held-r85-on-r86
COMMAND: TMPDIR=/fast/scratch/hyaku/mado-r86/R86ExecControl /usr/bin/python3 -I /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/quality/counters/c1-r85-identity-causes.py --repo /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --controls /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-86/controls/c1-cases-r86.json --carried /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-84/controls/c1-cases-r84.json --scratch-root /fast/scratch/hyaku/mado-r86/R86ExecControl/c1-held-r85-on-r86 --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee
RC: 2
MADO_R85_IDENTITY: ERROR (stage=setup control set carries 75 cases, frozen target expects 72)

## c1-r86-flood-and-held
COMMAND: TMPDIR=/fast/scratch/hyaku/mado-r86/R86ExecControl /usr/bin/python3 -I /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/quality/counters/c1-r86-refusal-records.py --repo /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --controls /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-86/controls/c1-cases-r86.json --carried /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-85/controls/c1-cases-r85.json --scratch-root /fast/scratch/hyaku/mado-r86/R86ExecControl/c1-r86-flood-and-held --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee --no-mutants
RC: 0
MADO_R86_CASE: name=host-top rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=bottom-bar rc=0 box=MATCH reserved=EQ band=30 expected=30 verdict=CLEAN correct=yes
MADO_R86_CASE: name=top-margin-int rc=0 box=MATCH reserved=EQ band=38 expected=38 verdict=CLEAN correct=yes
MADO_R86_CASE: name=top-margin-css-2 rc=0 box=MATCH reserved=EQ band=38 expected=38 verdict=CLEAN correct=yes
MADO_R86_CASE: name=top-margin-asym rc=0 box=MATCH reserved=EQ band=42 expected=42 verdict=CLEAN correct=yes
MADO_R86_CASE: name=bottom-margin rc=0 box=MATCH reserved=EQ band=46 expected=46 verdict=CLEAN correct=yes
MADO_R86_CASE: name=left-margin rc=0 box=MATCH reserved=EQ band=52 expected=52 verdict=CLEAN correct=yes
MADO_R86_CASE: name=right-margin rc=0 box=MATCH reserved=EQ band=46 expected=46 verdict=CLEAN correct=yes
MADO_R86_CASE: name=right-zero-margin rc=0 box=MATCH reserved=EQ band=40 expected=40 verdict=CLEAN correct=yes
MADO_R86_CASE: name=layer-bottom rc=0 box=MATCH reserved=EQ band=28 expected=28 verdict=CLEAN correct=yes
MADO_R86_CASE: name=output-exclusion rc=0 box=MATCH reserved=EQ band=24 expected=24 verdict=CLEAN correct=yes
MADO_R86_CASE: name=output-excluded rc=3 box=NOT_ON_MONITOR reserved=NOT_APPLIED band=None expected=None verdict=NO_BAR correct=yes
MADO_R86_CASE: name=width-with-margins rc=0 box=MATCH reserved=EQ band=34 expected=34 verdict=CLEAN correct=yes
MADO_R86_CASE: name=exclusive-false rc=0 box=MATCH reserved=NOT_APPLIED band=0 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=second-consumer rc=0 box=MATCH reserved=GT band=60 expected=34 verdict=CLEAN correct=yes
MADO_R86_CASE: name=reserved-differ rc=1 box=MATCH reserved=DIFFER band=26 expected=34 verdict=DIFFER correct=yes
MADO_R86_CASE: name=dynamic-cross rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=negative-margin-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=static-composed rc=0 box=MATCH reserved=EQ band=60 expected=60 verdict=CLEAN correct=yes
MADO_R86_CASE: name=static-other-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=static-exclusive-false rc=0 box=MATCH reserved=NOT_APPLIED band=26 expected=52 verdict=CLEAN correct=yes
MADO_R86_CASE: name=static-last-wins rc=0 box=MATCH reserved=EQ band=52 expected=52 verdict=CLEAN correct=yes
MADO_R86_CASE: name=static-source-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=overlay-compose-top rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R86_CASE: name=bottom-level-first rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R86_CASE: name=same-level-order rc=0 box=MATCH reserved=EQ band=62 expected=62 verdict=CLEAN correct=yes
MADO_R86_CASE: name=exclusive-edge-matched rc=0 box=MATCH reserved=EQ band=56 expected=56 verdict=CLEAN correct=yes
MADO_R86_CASE: name=anchor-unmatched rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=overlay-unexclusive-full rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=ls-area-invalid rc=0 box=MATCH reserved=EQ band=0 expected=0 verdict=CLEAN correct=yes
MADO_R86_CASE: name=negative-margin-skip rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=empty-box-skip rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=full-box-vs-usable rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=overflow-tie-negative rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=auto-dynamic-band-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=auto-corner-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=auto-all-four-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=auto-parallel-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=auto-left-dock rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=alloc-dyn-height-top rc=0 box=MATCH reserved=EQ band=34 expected=34 verdict=CLEAN correct=yes
MADO_R86_CASE: name=alloc-dyn-height-margin rc=0 box=MATCH reserved=EQ band=38 expected=38 verdict=CLEAN correct=yes
MADO_R86_CASE: name=alloc-dyn-width-dock rc=0 box=MATCH reserved=EQ band=60 expected=60 verdict=CLEAN correct=yes
MADO_R86_CASE: name=alloc-zero-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-negative-refused rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-unknown-namespace rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-explicit-ignored rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=alloc-composition-dyn-bar rc=0 box=MATCH reserved=EQ band=46 expected=46 verdict=CLEAN correct=yes
MADO_R86_CASE: name=extra-dyn-band-top rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R86_CASE: name=extra-dyn-band-dock rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=extra-dyn-band-explicit rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R86_CASE: name=extra-dyn-band-bottom rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R86_CASE: name=extra-dyn-band-zero-alloc rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-live-band-differs rc=1 box=DIFFER reserved=EQ band=34 expected=34 verdict=DIFFER correct=yes
MADO_R86_CASE: name=alloc-bool-refused rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-two-namespaces rc=0 box=MATCH reserved=EQ band=74 expected=74 verdict=CLEAN correct=yes
MADO_R86_CASE: name=bar-dyn-band-no-alloc rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-live-box-differs-composed rc=1 box=DIFFER reserved=EQ band=34 expected=34 verdict=DIFFER correct=yes
MADO_R86_CASE: name=bar-dyn-band-exclusive-false rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=duplicate-extra-namespaces rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=duplicate-bar-namespace rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=duplicate-allocation-keys rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-dup-key-equal rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-dup-key-interleaved rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-not-object rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-non-integer rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-empty-namespace rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-unknown-case-variant rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=ns-dup-bar rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=ns-dup-surface rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=ns-dup-cross-level rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=ns-case-distinct-accepted rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R86_CASE: name=live-dup-surface rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-negative-cause rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-bool-cause rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_CASE: name=alloc-float-band rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R86_MUTANT: skipped=yes reason=--no-mutants (the kill clause is not claimed by this run)
MADO_R86_BASE: correct=75/75 rule=held-r85-tool base_rev=2b6dd76b65de4dfe701db87db13b7e448b3538ee base_sha256=62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5
MADO_R86_CONTROL: sha256=f6dd9cdef7daa2e6b51c95f27cf8ebe8509188c551ff18ed42a176a08d8620bf carried=72/72 flooding=48/75 held_rule_flooding=75/75 flooding_sha256=3c5ec8b280e1c9d2e947afbc8a0991fe1174343c2026f26612dd10f71c4f3948
MADO_R86_REFUSALS: cases=75 correct=75 mutants=0 killed=0 base_correct=75/75 carried=72/72 tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=MUTANTS_SKIPPED rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5

## c2-held-r85-on-r85
COMMAND: TMPDIR=/fast/scratch/hyaku/mado-r86/R86ExecControl /usr/bin/python3 -I /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/quality/counters/c2-r85-status-classes.py --repo /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --controls /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-85/controls/c2-cases-r85.json --carried /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-84/controls/c2-runbook-cases-r84.json --scratch-root /fast/scratch/hyaku/mado-r86/R86ExecControl/c2-held-r85-on-r85
RC: 1
MADO_R85_CONTROLS: sha256=de8a68fe22799d4bf8366ab56c9d390559260dc8a70c3d1d7e0d03da98d23b64 cases=36
MADO_R85_PROBE: name=version row=0 kind=regex match=yes rc=0 stdout-bytes=127
MADO_R85_PROBE: name=configerrors row=1 kind=empty match=yes rc=0 stdout-bytes=2
MADO_R85_PROBE: name=monitors-size row=2 kind=regex match=yes rc=0 stdout-bytes=24
MADO_R85_PROBE: name=monitors-reserved row=3 kind=int4 match=yes rc=0 stdout-bytes=11
MADO_R85_PROBE: name=gaps-out row=4 kind=exact match=yes rc=0 stdout-bytes=21
MADO_R85_PROBE: name=kb-layout row=5 kind=exact match=yes rc=0 stdout-bytes=8
MADO_R85_PROBE: name=binds-count row=6 kind=int_range match=yes rc=0 stdout-bytes=4
MADO_R85_PROBE: name=layers-namespaces row=7 kind=sorted_unique match=yes rc=0 stdout-bytes=17
MADO_R85_PROBE: name=waybar-process row=8 kind=int_range match=yes rc=0 stdout-bytes=5
MADO_R85_PROBE: name=mako-mode row=9 kind=exact match=yes rc=0 stdout-bytes=8
MADO_R85_PROBE: name=omarchy-theme row=10 kind=exact match=yes rc=0 stdout-bytes=12
MADO_R85_PROBE: name=omarchy-version row=11 kind=regex match=yes rc=0 stdout-bytes=6
MADO_R85_PROBE: name=active-workspace row=12 kind=json_object_fields match=yes rc=0 stdout-bytes=20
MADO_R85_PROBE: name=layers-dump row=13 kind=levels_dump match=yes rc=0 stdout-bytes=748
MADO_R85_PROBE: name=monitors-dump row=14 kind=array_fields match=yes rc=0 stdout-bytes=1339
MADO_R85_PROBE: name=clients-count row=15 kind=int_range match=yes rc=0 stdout-bytes=2
MADO_R85_PROBE: name=workspaces-count row=16 kind=int_range match=yes rc=0 stdout-bytes=2
MADO_R85_PROBE: name=refuse-mode row=17 kind=refusal match=yes rc=3 stdout-bytes=93
MADO_R85_PROBE: name=refuse-scale row=18 kind=refusal match=yes rc=3 stdout-bytes=160
MADO_R85_PROBE: name=refuse-layer-background row=19 kind=refusal match=yes rc=3 stdout-bytes=85
MADO_R85_PROBE: name=refuse-output-space row=20 kind=refusal match=yes rc=3 stdout-bytes=92
MADO_R85_PROBE: name=omarchy-menu-keybindings row=21 kind=lines_shape match=yes rc=0 stdout-bytes=11618
MADO_R85_PROBE: name=keybindings-chords row=22 kind=chord_shape match=yes rc=0 stdout-bytes=6948
MADO_R85_PROBE: name=hypridle-is-active row=23 kind=is_active match=yes rc=3 stdout-bytes=9
MADO_R85_PROBE: name=keybindings-actions row=24 kind=action_column match=yes rc=0 stdout-bytes=4863
MADO_R85_PROBE: name=waybar-pgrep row=25 kind=pid_state match=yes rc=0 stdout-bytes=5
MADO_R85_PROBE: name=tray-owner row=26 kind=regex match=yes rc=0 stdout-bytes=14650
MADO_R85_PROBE: name=tray-interface row=27 kind=regex match=yes rc=0 stdout-bytes=2473
MADO_R85_PROBE: name=tray-methods row=28 kind=lines_shape match=yes rc=0 stdout-bytes=928
MADO_R85_PROBE: name=tray-items row=29 kind=int_range match=yes rc=0 stdout-bytes=2
MADO_R85_PROBE: name=tray-host-registered row=30 kind=bool_property match=yes rc=0 stdout-bytes=7
MADO_R85_PROBE: name=pipefail-demonstration row=31 kind=exact match=yes rc=0 stdout-bytes=37
MADO_R85_PROBE: name=producer-failure-propagated row=32 kind=producer_failure match=yes rc=7 stdout-bytes=7
MADO_R85_PROBE: name=status-ok-contained row=33 kind=exact match=yes rc=0 stdout-bytes=16
MADO_R85_PROBE: name=status-exit7-contained row=34 kind=exact match=yes rc=7 stdout-bytes=19
MADO_R85_PROBE: name=status-sigpipe-contained row=35 kind=exact match=yes rc=141 stdout-bytes=28
MADO_R85_MUTANT: name=int-range-lower-open matched=33/36 killed=yes
MADO_R85_MUTANT: name=json-required-ignored matched=34/36 killed=yes
MADO_R85_MUTANT: name=sorted-unique-dropped matched=35/36 killed=yes
MADO_R85_MUTANT: name=empty-accepted matched=35/36 killed=yes
MADO_R85_MUTANT: name=refusal-stage-blind matched=32/36 killed=yes
MADO_R85_MUTANT: name=refusal-rc-blind matched=32/36 killed=yes
MADO_R85_MUTANT: name=lines-any-line matched=34/36 killed=yes
MADO_R85_MUTANT: name=lines-min-lines-dropped matched=34/36 killed=yes
MADO_R85_MUTANT: name=chord-mod-word-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=chord-key-padded matched=35/36 killed=yes
MADO_R85_MUTANT: name=chord-arrow-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=chord-mod-duplicate-accepted matched=35/36 killed=yes
MADO_R85_MUTANT: name=chord-min-chords-dropped matched=35/36 killed=yes
MADO_R85_MUTANT: name=state-rc-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=state-enum-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=action-prefix-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=action-empty-accepted matched=35/36 killed=yes
MADO_R85_MUTANT: name=action-arrow-inside-accepted matched=35/36 killed=yes
MADO_R85_MUTANT: name=pid-rc-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=pid-numeric-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=pid-zero-accepted matched=35/36 killed=yes
MADO_R85_MUTANT: name=pid-single-only matched=35/36 killed=yes
MADO_R85_MUTANT: name=lines-shape-floor-dropped matched=34/36 killed=yes
MADO_R85_MUTANT: name=bool-shape-blind matched=35/36 killed=yes
MADO_R85_MUTANT: name=bool-false-refused matched=35/36 killed=yes
MADO_R85_MUTANT: name=lines-shape-any-line matched=35/36 killed=yes
MADO_R85_MUTANT: name=producer-rc-masked matched=35/36 killed=yes
MADO_R85_MUTANT: name=pipeline-guard-stripped matched=33/36 killed=yes
MADO_R85_MUTANT: name=any-nonzero matched=34/36 killed=yes
MADO_R85_MUTANT: name=status-class-ignored matched=34/36 killed=yes
MADO_R85_MUTANT: name=exact-any-nonzero matched=35/36 killed=yes
MADO_R85_MUTANT: name=signal-any-nonzero matched=35/36 killed=yes
MADO_R85_MUTANT: name=signal-as-exit matched=35/36 killed=yes
MADO_R85_MUTANT: name=regex-anchor-dropped matched=36/36 killed=no
MADO_R85_MUTANT: name=line-anchor-prefix matched=36/36 killed=no
MADO_R85_MUTANT: name=negatives-skipped matched=36/36 killed=no
MADO_R85_MUTANT: name=samples-skipped matched=36/36 killed=no
MADO_R85_CONTROL: superseded=active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,omarchy-version,tray-items,tray-methods,version,waybar-process,workspaces-count status_classes=2/36 substantive-before=receipt(control-c2-r85-unguarded.txt; the three fixtures unguarded report rc=0 for producers that exit7 and die by SIGPIPE, so the before-state matches no non-ok class)
MADO_R85_RUNBOOK: cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36 superseded=active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,omarchy-version,tray-items,tray-methods,version,waybar-process,workspaces-count mutants=37 killed=33 verdict=TARGET_MISSED rev=237ecf4e69a4986108f719f3beeafe111adaa033 tree=bound

## c2-r86-new-witness
COMMAND: TMPDIR=/fast/scratch/hyaku/mado-r86/R86ExecControl /usr/bin/python3 -I /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/quality/counters/c2-r86-clause-observations.py --repo /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --controls /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-86/controls/c2-cases-r86.json --carried /fast/scratch/hyaku/mado-r86/R86ExecControl/snapshot/.ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root /fast/scratch/hyaku/mado-r86/R86ExecControl/c2-r86-new-witness --no-mutants
RC: 0
MADO_R86_CONTROLS: sha256=a87f0ea480b36a8eec8592ccdffb6b1e3d60b183c343af2cc5c4563c23bd57d8 cases=37
MADO_R86_PROBE: name=version row=0 kind=regex match=yes clauses=anchors:1,samples:1,negatives:5 declared=anchors:1,samples:1,negatives:5 rc=0 stdout-bytes=127
MADO_R86_PROBE: name=configerrors row=1 kind=empty match=yes clauses=anchors:0,samples:0,negatives:4 declared=anchors:0,samples:0,negatives:4 rc=0 stdout-bytes=2
MADO_R86_PROBE: name=monitors-size row=2 kind=regex match=yes clauses=anchors:0,samples:2,negatives:4 declared=anchors:0,samples:2,negatives:4 rc=0 stdout-bytes=24
MADO_R86_PROBE: name=monitors-reserved row=3 kind=int4 match=yes clauses=anchors:0,samples:2,negatives:4 declared=anchors:0,samples:2,negatives:4 rc=0 stdout-bytes=11
MADO_R86_PROBE: name=gaps-out row=4 kind=exact match=yes clauses=anchors:0,samples:0,negatives:3 declared=anchors:0,samples:0,negatives:3 rc=0 stdout-bytes=21
MADO_R86_PROBE: name=kb-layout row=5 kind=exact match=yes clauses=anchors:0,samples:0,negatives:3 declared=anchors:0,samples:0,negatives:3 rc=0 stdout-bytes=8
MADO_R86_PROBE: name=binds-count row=6 kind=int_range match=yes clauses=anchors:0,samples:2,negatives:5 declared=anchors:0,samples:2,negatives:5 rc=0 stdout-bytes=4
MADO_R86_PROBE: name=layers-namespaces row=7 kind=sorted_unique match=yes clauses=anchors:0,samples:2,negatives:5 declared=anchors:0,samples:2,negatives:5 rc=0 stdout-bytes=17
MADO_R86_PROBE: name=waybar-process row=8 kind=int_range match=yes clauses=anchors:0,samples:2,negatives:4 declared=anchors:0,samples:2,negatives:4 rc=0 stdout-bytes=5
MADO_R86_PROBE: name=mako-mode row=9 kind=exact match=yes clauses=anchors:0,samples:0,negatives:3 declared=anchors:0,samples:0,negatives:3 rc=0 stdout-bytes=8
MADO_R86_PROBE: name=omarchy-theme row=10 kind=exact match=yes clauses=anchors:0,samples:0,negatives:3 declared=anchors:0,samples:0,negatives:3 rc=0 stdout-bytes=12
MADO_R86_PROBE: name=omarchy-version row=11 kind=regex match=yes clauses=anchors:1,samples:2,negatives:6 declared=anchors:1,samples:2,negatives:6 rc=0 stdout-bytes=6
MADO_R86_PROBE: name=active-workspace row=12 kind=json_object_fields match=yes clauses=anchors:0,samples:2,negatives:5 declared=anchors:0,samples:2,negatives:5 rc=0 stdout-bytes=20
MADO_R86_PROBE: name=layers-dump row=13 kind=levels_dump match=yes clauses=anchors:0,samples:1,negatives:2 declared=anchors:0,samples:1,negatives:2 rc=0 stdout-bytes=748
MADO_R86_PROBE: name=monitors-dump row=14 kind=array_fields match=yes clauses=anchors:0,samples:1,negatives:2 declared=anchors:0,samples:1,negatives:2 rc=0 stdout-bytes=1339
MADO_R86_PROBE: name=clients-count row=15 kind=int_range match=yes clauses=anchors:0,samples:2,negatives:4 declared=anchors:0,samples:2,negatives:4 rc=0 stdout-bytes=2
MADO_R86_PROBE: name=workspaces-count row=16 kind=int_range match=yes clauses=anchors:0,samples:2,negatives:4 declared=anchors:0,samples:2,negatives:4 rc=0 stdout-bytes=2
MADO_R86_PROBE: name=refuse-mode row=17 kind=refusal match=yes clauses=anchors:0,samples:1,negatives:3 declared=anchors:0,samples:1,negatives:3 rc=3 stdout-bytes=93
MADO_R86_PROBE: name=refuse-scale row=18 kind=refusal match=yes clauses=anchors:0,samples:1,negatives:3 declared=anchors:0,samples:1,negatives:3 rc=3 stdout-bytes=160
MADO_R86_PROBE: name=refuse-layer-background row=19 kind=refusal match=yes clauses=anchors:0,samples:1,negatives:3 declared=anchors:0,samples:1,negatives:3 rc=3 stdout-bytes=85
MADO_R86_PROBE: name=refuse-output-space row=20 kind=refusal match=yes clauses=anchors:0,samples:1,negatives:3 declared=anchors:0,samples:1,negatives:3 rc=3 stdout-bytes=92
MADO_R86_PROBE: name=omarchy-menu-keybindings row=21 kind=lines_shape match=yes clauses=anchors:0,samples:2,negatives:5 declared=anchors:0,samples:2,negatives:5 rc=0 stdout-bytes=11618
MADO_R86_PROBE: name=keybindings-chords row=22 kind=chord_shape match=yes clauses=anchors:0,samples:2,negatives:8 declared=anchors:0,samples:2,negatives:8 rc=0 stdout-bytes=6948
MADO_R86_PROBE: name=hypridle-is-active row=23 kind=is_active match=yes clauses=anchors:0,samples:3,negatives:4 declared=anchors:0,samples:3,negatives:4 rc=3 stdout-bytes=9
MADO_R86_PROBE: name=keybindings-actions row=24 kind=action_column match=yes clauses=anchors:0,samples:3,negatives:6 declared=anchors:0,samples:3,negatives:6 rc=0 stdout-bytes=4863
MADO_R86_PROBE: name=waybar-pgrep row=25 kind=pid_state match=yes clauses=anchors:0,samples:3,negatives:6 declared=anchors:0,samples:3,negatives:6 rc=0 stdout-bytes=5
MADO_R86_PROBE: name=tray-owner row=26 kind=regex match=yes clauses=anchors:0,samples:2,negatives:4 declared=anchors:0,samples:2,negatives:4 rc=0 stdout-bytes=14770
MADO_R86_PROBE: name=tray-interface row=27 kind=regex match=yes clauses=anchors:0,samples:2,negatives:3 declared=anchors:0,samples:2,negatives:3 rc=0 stdout-bytes=2473
MADO_R86_PROBE: name=tray-methods row=28 kind=lines_shape match=yes clauses=anchors:0,samples:2,negatives:3 declared=anchors:0,samples:2,negatives:3 rc=0 stdout-bytes=928
MADO_R86_PROBE: name=tray-items row=29 kind=int_range match=yes clauses=anchors:0,samples:3,negatives:4 declared=anchors:0,samples:3,negatives:4 rc=0 stdout-bytes=2
MADO_R86_PROBE: name=tray-host-registered row=30 kind=bool_property match=yes clauses=anchors:0,samples:2,negatives:5 declared=anchors:0,samples:2,negatives:5 rc=0 stdout-bytes=7
MADO_R86_PROBE: name=pipefail-demonstration row=31 kind=exact match=yes clauses=anchors:0,samples:1,negatives:1 declared=anchors:0,samples:1,negatives:1 rc=0 stdout-bytes=37
MADO_R86_PROBE: name=producer-failure-propagated row=32 kind=producer_failure match=yes clauses=anchors:0,samples:1,negatives:2 declared=anchors:0,samples:1,negatives:2 rc=7 stdout-bytes=7
MADO_R86_PROBE: name=status-ok-contained row=33 kind=exact match=yes clauses=anchors:0,samples:1,negatives:2 declared=anchors:0,samples:1,negatives:2 rc=0 stdout-bytes=16
MADO_R86_PROBE: name=status-exit7-contained row=34 kind=exact match=yes clauses=anchors:0,samples:1,negatives:3 declared=anchors:0,samples:1,negatives:3 rc=7 stdout-bytes=19
MADO_R86_PROBE: name=status-sigpipe-contained row=35 kind=exact match=yes clauses=anchors:0,samples:1,negatives:3 declared=anchors:0,samples:1,negatives:3 rc=141 stdout-bytes=28
MADO_R86_PROBE: name=border-size-int row=36 kind=regex match=yes clauses=anchors:1,samples:2,negatives:3 declared=anchors:1,samples:2,negatives:3 rc=0 stdout-bytes=2
MADO_R86_CONTROL: superseded=active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,omarchy-version,tray-items,tray-methods,version,waybar-process,workspaces-count status_classes=2/37 held_rule_new_case=0/1 new_case=border-size-int held_rule=round85(regex-kind-search,no-clause-observation)
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 superseded=active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,omarchy-version,tray-items,tray-methods,version,waybar-process,workspaces-count mutants=0 killed=0 verdict=MUTANTS_SKIPPED rev=237ecf4e69a4986108f719f3beeafe111adaa033 tree=bound
```

## Direct held-rule diagnostic (after CLI population refusal)

```sh
S=/fast/scratch/hyaku/mado-r86/R86ExecControl; mkdir -p -- "$S"; trap 'rm -rf -- "$S"' EXIT; TMPDIR="$S" /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/w1/ctrl-held-rule.py "$S"
```

RC: 0

```text
R86_CONTROL_DIRECT: rule=frozen-r85-run_cases cases=75 correct=75/75 scope=direct-function-not-cli-target
```

The direct diagnostic is separate evidence, not a repaired instrument or a CLI target result.

## Initial extraction failure

The first invocation of the same battery command above returned driver rc 1 before any counter ran. Python's safe tar extraction rejected an unrelated historical absolute symlink. Exact stderr follows; the retained runner excludes archive symlinks rather than following or rewriting them.

```text
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/w1/ctrl-r86-controls.py", line 24, in <module>
    archive.extractall(SNAP, filter='data')
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/tarfile.py", line 2483, in extractall
    tarinfo, unfiltered = self._get_extract_tarinfo(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~^
        member, filter_function, path)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/tarfile.py", line 2573, in _get_extract_tarinfo
    self._handle_fatal_error(e)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/usr/lib/python3.14/tarfile.py", line 2571, in _get_extract_tarinfo
    filtered = filter_function(unfiltered, path)
  File "/usr/lib/python3.14/tarfile.py", line 900, in data_filter
    new_attrs = _get_filtered_attrs(member, dest_path, True)
  File "/usr/lib/python3.14/tarfile.py", line 867, in _get_filtered_attrs
    raise AbsoluteLinkError(member)
tarfile.AbsoluteLinkError: '.ufo/waves/round-17/tripwire/hardening/symlink-target.jsonl' is a link to an absolute path
```

## Scope, risks and handoff

Changed only this report and the two exclusive `ctrl-*.py` drivers in its directory. No frozen instruments, controls, declaration, application files or another seat's report changed. No tool installations. LSP unavailable: no LSP tool is mounted; frozen Python interfaces were read directly, with no symbol refactor.

Blocking limitation: the requested r85 CLI cannot score the 75-case r86 population by construction. Its exact rc 2 is retained, with the direct unchanged-rule score separately identified. No other blocker. Live tray output sizes differed between concurrent C2 invocations; their declared shapes still matched. These receipts measure the frozen revision, not the evolving lane tip.

Self-evaluation: accuracy 4/5 (direct function evidence must not be confused with the old CLI); completeness 4/5 (old CLI population restriction prevents its requested numeric score); clarity 4/5 (full receipts are long but unabridged); actionability 5/5 (two retained drivers and shell commands); conciseness 4/5 (full stdout retained for audit). Overall 4.2/5. Highest-impact clarification already applied: distinguish rc 2/no score, direct score, and skipped-mutant diagnostics. User-agreement check: the requested distinctions and four survivors are explicitly evidenced.
