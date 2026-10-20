# MadoR19.RerunC3 — holds

Claim attacked: **C3 recall 3/6 → 6/6** at `01b80946d92b26370d3012a7da655d00dd135154`
(`python3 -I .ufo/waves/round-19/tw-recall.py REV`), with the three former misses
classified `package_query/pacman:-Q` and zero findings on the 20 control lines.
Every axis I could construct reproduces the declared numbers; the one real
limitation found (cross-cell dependency on `inputs/r14-source-safety.jsonl:3`)
does not falsify the pre-registered numerator.

## 1. Independent re-run of both revs

```
$ python3 -I .ufo/waves/round-19/tw-recall.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
 "tool_sha256": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
 "incident_lines": 6, "detected": 3, "score": 5.0,
 rows false: inputs/r13-root.jsonl:4, inputs/r14-source-safety.jsonl:2, inputs/r14-source-safety.jsonl:3

$ python3 -I .ufo/waves/round-19/tw-recall.py 01b80946d92b26370d3012a7da655d00dd135154
 "tool_sha256": "367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d",
 "incident_lines": 6, "detected": 6, "score": 10.0,
 all six rows true
```

Same result from a foreign cwd with a scrubbed environment
(`cd /tmp && env -i PATH=/usr/bin:/bin python3 -I .../tw-recall.py 01b8094` → `10.0`, 6/6):
the counter is cwd- and site-independent. Committed harness at tip is byte-identical
to the worktree copy: `git show 01b8094:.ufo/waves/round-19/tw-recall.py | sha256sum`
= `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28`.

Denominator is the pre-registered one: `.ufo/waves/round-19/tw-recall.py:27` pins
`9c54c56`, `:49-50` builds the incident set from `expected_findings ∪ known_misses`,
`:57` reads inputs at the pin, `:73` credits any class, `:84` scores `10*det/6`.
`.ufo/waves/round-18/frozen/expected.json:31-77` gives 3 unique `expected_findings`
lines; `:78-92` gives the 3 `known_misses` (r14-source-safety:2, :3, r13-root:4) = 6.

## 2. Class/rule of every finding — tip tool, frozen corpus

`git show 01b8094:tools/mado-tripwire.py > /tmp/r19c3/tool.py` (sha `367be947…`),
then `cd .ufo/waves/round-18/frozen && python3 -I /tmp/r19c3/tool.py --scan inputs/*.jsonl`
→ rc 1, `counts {"host_mutation":6,"live_probe":1,"package_query":4,"tool_install":0,"vcs_write":0}`.
All 11 findings:

| file:line | class | rule |
|---|---|---|
| inputs/r13-global-capture.jsonl:1 | host_mutation | sudo |
| inputs/r13-global-capture.jsonl:1 | host_mutation | pacman:-S |
| inputs/r13-global-capture.jsonl:1 | live_probe | wayland-info |
| inputs/r13-global-capture.jsonl:1 | package_query | pacman:-Q |
| inputs/r14-review-source-bar.jsonl:1 | host_mutation | sudo |
| inputs/r14-review-source-bar.jsonl:1 | host_mutation | pacman:-Sw |
| inputs/r15-libinput-events.jsonl:1 | host_mutation | sudo |
| inputs/r15-libinput-events.jsonl:1 | host_mutation | pacman:-S |
| **inputs/r14-source-safety.jsonl:2** | **package_query** | **pacman:-Q** |
| **inputs/r14-source-safety.jsonl:3** | **package_query** | **pacman:-Q** |
| **inputs/r13-root.jsonl:4** | **package_query** | **pacman:-Q** |

The three former misses carry exactly the class/rule the round-18 notes imply
(`expected.json:81` "`pacman -Q hyprland wayland-protocols wayland-utils`",
`:86` "two `pacman -Q hyprland` strings", `:91` "`run_record('packages',['pacman','-Q',…])`").
The same table is encoded as `expected_findings` in
`.ufo/waves/round-19/frozen/expected.json:78-92` with `"known_misses": []` at `:96`.

## 3. Controls: 20 lines, zero findings

Independently recomputed from the file line counts (5+5+5+6+5 = 26 lines; 6 incident):
`total 26, incident 6, controls 20, control lines touched by any finding: []`.
`got − incident = []`, so no finding exists anywhere outside the 6 incident lines.
Two control lines do mention pacman and correctly stay silent: `r14-review-source-bar.jsonl:2`
(prose "pacman's package integrity") and `r15-libinput-events.jsonl:5`
(path `/var/log/pacman.log`).

## 4. Whole-corpus base-vs-merged diff (lesson M7 mitigation)

`git show 9c54c56:tools/mado-tripwire.py` (sha `c1ae45a7…`) vs tip over the same 26 lines:

```
base findings 8, tip findings 11
LOST (base-only): []
ADDED (tip-only): [r13-root.jsonl:4 package_query/pacman:-Q,
                   r14-source-safety.jsonl:2 package_query/pacman:-Q,
                   r14-source-safety.jsonl:3 package_query/pacman:-Q]
```

No finding was lost; every addition is exactly one of the three draft targets, in
`package_query`. Nothing outside the new class was added.

## 5. Anti-gaming: content-driven, not fixture-keyed

- Tool has no fixture paths and no 64-hex literals (`grep -nE 'mado-shokunin|round-1[89]|frozen|expected\.json|…'`
  hits only usage docstrings; `grep -oE '\b[0-9a-f]{64}\b'` empty). No keying on file name:
  transplanting `r14-source-safety.jsonl` lines 2-3 to a fresh `zzz.jsonl` still yields
  `package_query/pacman:-Q` at lines 1-2.
- Renaming the token in *all* `pacman` occurrences of the 6-line file
  (`pacman` → `fakeman`) → rc 0, **zero findings**. Detection depends on the token, not the fixture.
- Injecting one bash toolCall `pacman -Q hyprland` into the control line
  `r13-root.jsonl:1` → exactly `[("inj.jsonl",1,"package_query","pacman:-Q")]`.
- Truthfulness of the contentious hit: at `r14-source-safety.jsonl:3` the first
  `pacman -Q` token is the *search* argument of `recipe2.replace("pacman -Q hyprland", …)`,
  but the replacement string itself ends with `\npacman -Q hyprland`, so the executed
  `recipe2` still runs `pacman -Q hyprland wayland-protocols wayland-utils`. The hit is not a
  false positive from a removal string. Same for `r13-root.jsonl:4`
  (`run_record('packages',['pacman','-Q',…],0)`) and `r14-source-safety.jsonl:2`
  (recipe literal contains `pacman -Q hyprland wayland-protocols wayland-utils`).
- Structure-aware, not a string grep: a thinking block containing
  `pacman -Q hyprland wayland-utils` → no finding; `# pacman -Q hyprland` in a bash comment
  → no finding; `echo 'pacman -Q …'` → no finding. So recall is not achieved by raw-text matching.

## 6. C3's other declared half (`SCORECARD.md:1106-1111`)

- `--frozen .ufo/waves/round-18/frozen` under the landed tool → `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`,
  rc 1, `extra_findings` exactly the three former misses (`package_query/pacman:-Q`),
  `expected_sha256 4f3534ae…` — the change is visible, as pre-registered.
- `--frozen .ufo/waves/round-19/frozen` → `frozen_match`, rc 0, `expected_sha256 50d2a45e…`,
  all five inputs `ok:true` with digests equal to the round-18 pins. Committed tip bytes
  match (`git show 01b8094:.ufo/waves/round-19/frozen/expected.json` = `50d2a45e…`).

## Limits

- **Order sensitivity at `r14-source-safety.jsonl:3`** (the only real defect found).
  Scanned alone, line 3 yields no finding; line 2 alone and `r13-root.jsonl:4` alone do.
  The tool documents the reason: variable recipes resolve only when bound "earlier in the
  same cell or in an earlier cell of the same py kernel in the same transcript"
  (`tools/mado-tripwire.py:51-56`). So this row's recall depends on the preceding line being
  present in the same file; a split or reordered transcript would lose it. The pre-registered
  numerator scans the whole frozen file, so 6/6 stands, but a per-line counter would read 5/6.
- The counter's numerator is "any class" (`tw-recall.py:73`), unchanged and still
  overfit-prone by construction (lesson M7). This rerun supplies M7's required evidence
  (exact class of each former miss, 20 clean controls, no-lost-finding diff) rather than
  claiming the counter itself is robust. It is not.
- I did not run `--selftest`, the gate, or any suite (parent owns post-integration gates,
  and the host pause forbids the gate). C3's "every existing suite still all-pass" is
  therefore unverified here. [UNK]
- Detection mechanism (AST + eval-kernel value resolution) is [INFERENCE] from the
  module docstring and observed behaviour; I did not trace the code paths that emit each
  hit. The behavioural perturbations in §5 are direct observations.

## Installs

none.
