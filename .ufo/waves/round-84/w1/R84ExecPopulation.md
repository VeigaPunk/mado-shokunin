# R84ExecPopulation — isolated population and carry checks

Axes: C1 coverage, C2 operability, and registry completeness; preservation boundary: no production or host-state changes.

## Scope and method

Measured only frozen revision `3f9eec3906ddd1492e8bc08325e83064f00111ea`. Extracted eight named files with read-only `git show REV:PATH` into `/fast/scratch/hyaku/mado-r84/R84ExecPopulation`; no clone, git/jj mutation, live desktop probe, raw session capture, or credential access. Ran four independent subprocesses concurrently, synchronously collecting all results. Each subprocess used the scratch cwd, `python3 -I -B`, `LC_ALL=C`, and scratch `TMPDIR`; imports also disabled bytecode.

Independent `probe.py` imported both counters via `importlib.util.spec_from_file_location`; asserted each declared population equals its enumeration and expected target, plus mutation-name uniqueness. Parsed JSON internally without emitting its values. C1 comparison asserted entire first-58 case dictionaries equal the entire r83 set. C2 comparison asserted identical case order/names and key sets, with every changed field permitted by the frozen counter's `SUPERSEDED` mapping; additionally asserted exactly its 15 named cases changed, each in exactly `argv` and `skill_anchor`. No blanket allowance for all cases' anchors was used.

For the registry check, restricted matching to the frozen SKILL.md `## Gate registry` section, then counted table rows containing each exact `quality/counters/FILENAME` path. This is registry-row presence, not merely a whole-file textual mention.

## Exact retained results

Command: `python3 -I -B probe.py`; exit **0**.

```text
C1: constant=41 enumerated=41 unique_names=41 PASS
C2: constant=29 enumerated=29 unique_names=29 PASS
C1: total=61 carried_parsed_equal=58/58 added=3 PASS
C2: total=33 carried_allowed_equal=31/31 fully_unchanged=16 superseded=15 changed_fields=30 added=2 PASS
C2 superseded names: active-workspace,binds-count,clients-count,gaps-out,kb-layout,keybindings-actions,keybindings-chords,layers-namespaces,monitors-reserved,monitors-size,tray-items,tray-methods,version,waybar-process,workspaces-count
REGISTRY: c1-r82-allocation-band.py matching_rows=0
REGISTRY: c2-r82-runbook.py matching_rows=0
REGISTRY: c1-r83-surface-band.py matching_rows=0
REGISTRY: c2-r83-runbook.py matching_rows=0
REGISTRY: old_counter_rows_present=0/4 missing=4/4
```

Command: `python3 -I -B quality/counters/c1-r84-namespaces.py --selftest`; exit **0**.

```text
MADO_R84_BARFOOT_SELFTEST: 99/99
```

Command: `python3 -I -B quality/counters/c2-r84-runbook.py --selftest`; exit **0**.

```text
MADO_R84_RUNBOOK_SELFTEST: 98/98
```

Command: `python3 -I -B tools/mado-barfoot.py --selftest`; exit **0**.

```text
MADO_BARFOOT_SELFTEST: 139/139
```

All four subprocesses returned empty stderr.

## Frozen input SHA-256 pins

| Path | SHA-256 |
|---|---|
| `quality/counters/c1-r84-namespaces.py` | `3b9fd395c3cbf641dda777f8831d0f360952d10203e34ddccbe47621e727135e` |
| `quality/counters/c2-r84-runbook.py` | `53f47372a2d44cd07120815835c3cb3ec4e4dca8cb31954bf869292952598839` |
| `tools/mado-barfoot.py` | `72456666a31927dfc46f955f41b3aa57b2215a8fcd8dc736fc302d7b58830c7f` |
| `SKILL.md` | `1056fb8c39c09efb77ed59341d01032152efa3f96ffbbd51f64f7c606e5ea7b4` |
| `.ufo/waves/round-84/controls/c1-cases-r84.json` | `5c9ce3891e1ec4be1820d229bbcfddfa5b61cfbd0d02cc93252ac38c6dd9e883` |
| `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json` | `2e86b4b64b7b7b95fcfdb78e2463762a8f8dc7a299145a992170fdc59d4b5efe` |
| `.ufo/waves/round-83/controls/c1-cases-r83.json` | `e4409dabcf74f32307f14b31afb85091bca7d584771076bdb9a3b336bc9512c4` |
| `.ufo/waves/round-83/controls/c2-runbook-cases-r83.json` | `22ca4c1c495274f797d1eec8abb804974a02054d55657fd896507d972c05b3bf` |

## Findings, risks, and boundaries

- Population assertions and carried-case comparisons passed at the frozen revision. This does not establish mutation kill counts, full counter admission, or live runbook correctness; none was measured by this seat.
- The four old r82/r83 counter rows are concretely absent from the frozen gate registry: **0 present, 4 missing**. The r83 R1 registry debt therefore remains at this revision. Registry remediation belongs to L1; no production edits were made.
- No supported LSP interface is exposed in this seat's tool inventory; symbol navigation was unavailable. No refactor was attempted.
- No tool installation or update occurred. Used existing Python 3 and Git only.
- Only retained lane file: this report. Scratch snapshots and probe are removed after retaining results here. No blockers to the assigned checks; registry incompleteness is a finding, not a reason to suppress results.

## Output self-evaluation

Accuracy 4/5: exact outputs and frozen hashes retained; these isolated checks do not prove full predicates. Completeness 5/5: both populations, both carry checks, all three selftests, and all four registry rows checked. Clarity 4/5: method is explicit but no executable probe survives scratch cleanup. Actionability 4/5: names and counts identify registry debt; remediation is deliberately outside this seat. Conciseness 4/5: evidence pins lengthen the report but make the frozen inputs attributable. Overall **4.2/5**. Improvement priorities: L1 owns registry completion and post-integration verification; do not relabel these selftests as candidate scoring. Would the user agree? The requested concrete counts are supplied, with the missing rows disclosed and no production changes.
