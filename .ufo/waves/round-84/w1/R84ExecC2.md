# R84ExecC2 — frozen C2 full counter receipt

## Result

**Setup error, exit 2; no TARGET_MET verdict.** All 33 live/fixture rows matched, including all 26 shape rows; 33 anchors and 33 rows passed setup binding. Fifteen guarded pipeline rows were present among the 31 carried rows. Twenty-eight mutants ran and were killed; the twenty-ninth (`pipeline-guard-stripped`) was not executed because its mutation anchor occurs twice in the frozen counter source.

Axes: operability, frozen-revision fidelity, capture hygiene. No production changes or optimization candidates were applied.

Frozen revision: `3f9eec3906ddd1492e8bc08325e83064f00111ea`.
Scratch: `/fast/scratch/hyaku/mado-r84/R84ExecC2`; a shared, no-checkout scratch clone materialized only 19 selected counter/control/tool/SKILL/fixture files. Its git top level was asserted before scratch checkout. No lane git/index/jj mutations.

## Invocation

Executed from scratch `repo/`:

```sh
python3 -I quality/counters/c2-r84-runbook.py --repo /fast/scratch/hyaku/mado-r84/R84ExecC2/repo --rev 3f9eec3906ddd1492e8bc08325e83064f00111ea --controls /fast/scratch/hyaku/mado-r84/R84ExecC2/repo/.ufo/waves/round-84/controls/c2-runbook-cases-r84.json --carried /fast/scratch/hyaku/mado-r84/R84ExecC2/repo/.ufo/waves/round-83/controls/c2-runbook-cases-r83.json --scratch-root /fast/scratch/hyaku/mado-r84/R84ExecC2/counter
```

## Interpretation and limitations

- Actual frozen failure: source line 162 contains the quoted anchor in the mutation declaration; line 224 contains the executable statement. `own_source.count(anchor)` therefore returns 2, and the frozen setup rule refuses the final mutant. The observed result cannot substantiate 29/29 kills or the full C2 predicate.
- The read-only fixture reported `unguarded=0 guarded=7`; the separate failed-producer row returned rc7 with plausible `b true`. This demonstrates contained pipeline masking and propagation, not failure of a host producer.
- All baseline rows matched; no mismatch attributable to changed desktop state was observed. The state-enum row returned rc3 and matched its declared state contract. Mutant children repeatedly read live state, so no invariant cross-child snapshot is claimed.
- Counter stdout already projects JSON replies to byte lengths. This receipt additionally redacts live/fixture output-value fields except the two synthetic pipefail rows; all probe names, matches, return codes, mutant results, control hash and the terminal setup error are retained. Raw JSON payloads, item addresses, credentials and session dumps were never saved. Child raw replies existed only in process memory.
- No unrelated builds, tests, formatters, service/config/compositor changes, installations, or tool upgrades. LSP unavailable in this seat's exposed tools; no symbol edits/refactors were needed.
- Parent action: resolve the nonunique final mutation anchor in a later permitted revision and run the full counter there; do not relabel this frozen run as a pass.

## Frozen input digests

- `SKILL.md`: `1056fb8c39c09efb77ed59341d01032152efa3f96ffbbd51f64f7c606e5ea7b4`
- `tools/mado-barfoot.py`: `72456666a31927dfc46f955f41b3aa57b2215a8fcd8dc736fc302d7b58830c7f`
- `quality/counters/c2-r84-runbook.py`: `53f47372a2d44cd07120815835c3cb3ec4e4dca8cb31954bf869292952598839`
- `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json`: `2e86b4b64b7b7b95fcfdb78e2463762a8f8dc7a299145a992170fdc59d4b5efe`
- `.ufo/waves/round-83/controls/c2-runbook-cases-r83.json`: `22ca4c1c495274f797d1eec8abb804974a02054d55657fd896507d972c05b3bf`

## Retained stdout (output-value redaction only)

```text
MADO_R84_CONTROLS: sha256=2e86b4b64b7b7b95fcfdb78e2463762a8f8dc7a299145a992170fdc59d4b5efe cases=33
MADO_R84_PROBE: name=version row=0 kind=regex match=yes rc=0 out=[REDACTED live/fixture value; 102 characters]
MADO_R84_PROBE: name=configerrors row=1 kind=empty match=yes rc=0 out=[REDACTED live/fixture value; 2 characters]
MADO_R84_PROBE: name=monitors-size row=2 kind=regex match=yes rc=0 out=[REDACTED live/fixture value; 25 characters]
MADO_R84_PROBE: name=monitors-reserved row=3 kind=int4 match=yes rc=0 json-bytes=11
MADO_R84_PROBE: name=gaps-out row=4 kind=exact match=yes rc=0 out=[REDACTED live/fixture value; 22 characters]
MADO_R84_PROBE: name=kb-layout row=5 kind=exact match=yes rc=0 out=[REDACTED live/fixture value; 9 characters]
MADO_R84_PROBE: name=binds-count row=6 kind=int_range match=yes rc=0 out=[REDACTED live/fixture value; 5 characters]
MADO_R84_PROBE: name=layers-namespaces row=7 kind=sorted_unique match=yes rc=0 out=[REDACTED live/fixture value; 18 characters]
MADO_R84_PROBE: name=waybar-process row=8 kind=int_range match=yes rc=0 out=[REDACTED live/fixture value; 6 characters]
MADO_R84_PROBE: name=mako-mode row=9 kind=exact match=yes rc=0 out=[REDACTED live/fixture value; 9 characters]
MADO_R84_PROBE: name=omarchy-theme row=10 kind=exact match=yes rc=0 out=[REDACTED live/fixture value; 13 characters]
MADO_R84_PROBE: name=omarchy-version row=11 kind=regex match=yes rc=0 out=[REDACTED live/fixture value; 7 characters]
MADO_R84_PROBE: name=active-workspace row=12 kind=json_object_fields match=yes rc=0 json-bytes=20
MADO_R84_PROBE: name=layers-dump row=13 kind=levels_dump match=yes rc=0 json-bytes=748
MADO_R84_PROBE: name=monitors-dump row=14 kind=array_fields match=yes rc=0 json-bytes=1339
MADO_R84_PROBE: name=clients-count row=15 kind=int_range match=yes rc=0 out=[REDACTED live/fixture value; 3 characters]
MADO_R84_PROBE: name=workspaces-count row=16 kind=int_range match=yes rc=0 out=[REDACTED live/fixture value; 3 characters]
MADO_R84_PROBE: name=refuse-mode row=17 kind=refusal match=yes rc=3 out=[REDACTED live/fixture value; 94 characters]
MADO_R84_PROBE: name=refuse-scale row=18 kind=refusal match=yes rc=3 out=[REDACTED live/fixture value; 102 characters]
MADO_R84_PROBE: name=refuse-layer-background row=19 kind=refusal match=yes rc=3 out=[REDACTED live/fixture value; 86 characters]
MADO_R84_PROBE: name=refuse-output-space row=20 kind=refusal match=yes rc=3 out=[REDACTED live/fixture value; 93 characters]
MADO_R84_PROBE: name=omarchy-menu-keybindings row=21 kind=lines_shape match=yes rc=0 out=[REDACTED live/fixture value; 104 characters]
MADO_R84_PROBE: name=keybindings-chords row=22 kind=chord_shape match=yes rc=0 out=[REDACTED live/fixture value; 104 characters]
MADO_R84_PROBE: name=hypridle-is-active row=23 kind=is_active match=yes rc=3 out=[REDACTED live/fixture value; 10 characters]
MADO_R84_PROBE: name=keybindings-actions row=24 kind=action_column match=yes rc=0 out=[REDACTED live/fixture value; 109 characters]
MADO_R84_PROBE: name=waybar-pgrep row=25 kind=pid_state match=yes rc=0 out=[REDACTED live/fixture value; 6 characters]
MADO_R84_PROBE: name=tray-owner row=26 kind=regex match=yes rc=0 out=[REDACTED live/fixture value; 102 characters]
MADO_R84_PROBE: name=tray-interface row=27 kind=regex match=yes rc=0 out=[REDACTED live/fixture value; 102 characters]
MADO_R84_PROBE: name=tray-methods row=28 kind=lines_shape match=yes rc=0 out=[REDACTED live/fixture value; 102 characters]
MADO_R84_PROBE: name=tray-items row=29 kind=int_range match=yes rc=0 out=[REDACTED live/fixture value; 3 characters]
MADO_R84_PROBE: name=tray-host-registered row=30 kind=bool_property match=yes rc=0 out=[REDACTED live/fixture value; 8 characters]
MADO_R84_PROBE: name=pipefail-demonstration row=31 kind=exact match=yes rc=0 out='MADO_PIPEFAIL: unguarded=0 guarded=7'
MADO_R84_PROBE: name=producer-failure-propagated row=32 kind=producer_failure match=yes rc=7 out='b true'
MADO_R84_MUTANT: name=rc-blind matched=21/33 killed=yes
MADO_R84_MUTANT: name=int-range-lower-open matched=30/33 killed=yes
MADO_R84_MUTANT: name=json-required-ignored matched=31/33 killed=yes
MADO_R84_MUTANT: name=sorted-unique-dropped matched=32/33 killed=yes
MADO_R84_MUTANT: name=empty-accepted matched=32/33 killed=yes
MADO_R84_MUTANT: name=refusal-stage-blind matched=29/33 killed=yes
MADO_R84_MUTANT: name=refusal-rc-blind matched=29/33 killed=yes
MADO_R84_MUTANT: name=lines-any-line matched=31/33 killed=yes
MADO_R84_MUTANT: name=lines-min-lines-dropped matched=31/33 killed=yes
MADO_R84_MUTANT: name=chord-mod-word-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=chord-key-padded matched=32/33 killed=yes
MADO_R84_MUTANT: name=chord-arrow-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=chord-mod-duplicate-accepted matched=32/33 killed=yes
MADO_R84_MUTANT: name=chord-min-chords-dropped matched=32/33 killed=yes
MADO_R84_MUTANT: name=state-rc-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=state-enum-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=action-prefix-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=action-empty-accepted matched=32/33 killed=yes
MADO_R84_MUTANT: name=action-arrow-inside-accepted matched=32/33 killed=yes
MADO_R84_MUTANT: name=pid-rc-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=pid-numeric-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=pid-zero-accepted matched=32/33 killed=yes
MADO_R84_MUTANT: name=pid-single-only matched=32/33 killed=yes
MADO_R84_MUTANT: name=lines-shape-floor-dropped matched=31/33 killed=yes
MADO_R84_MUTANT: name=bool-shape-blind matched=32/33 killed=yes
MADO_R84_MUTANT: name=bool-false-refused matched=32/33 killed=yes
MADO_R84_MUTANT: name=lines-shape-any-line matched=32/33 killed=yes
MADO_R84_MUTANT: name=producer-rc-masked matched=32/33 killed=yes
MADO_R84_RUNBOOK: ERROR (stage=setup mutant pipeline-guard-stripped anchor occurs 2 times, not once)
```

Exit: `2`. Stderr: `0 bytes`. Elapsed: `11.894 seconds`.

## Deliverable self-evaluation

Accuracy 4/5: exact contract lines and exit retained; live output values deliberately omitted. Completeness 4/5: full assigned invocation ran, but the frozen setup defect prevents final mutant execution. Clarity 4/5: setup failure is separated from row success; receipt is long to retain per-row evidence. Actionability 4/5: exact duplicate source locations identified; remediation is outside this read-only seat. Conciseness 4/5: full receipt retained rather than summary only. Overall 4.0/5. Highest-impact improvement is an unambiguous mutation anchor in an authorized later revision; preserve this frozen miss. The user should agree that observed row success does not establish the full target.
