# PRED-C1-r51 population audit

Revision: `56026fcb9800370ae04bc65952a6567181c398d0` (freeze). Exact frozen wording counts files under `tools/`, `quality/*.py`, and `quality/counters/*.py`.

Command used (tracked files, recursively):

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r --name-only 56026fcb9800370ae04bc65952a6567181c398d0
```

Independent path selection: include every `tools/` path (all extensions, nested paths), plus direct-child `quality/*.py` and direct-child `quality/counters/*.py`; `ls-tree -r` returns files only, so directories excluded. Counts from frozen-tree listing:

- `tools/`: 17 (16 Python files plus `tools/mado-verify.sh`)
- `quality/*.py`: 18
- `quality/counters/*.py`: 47
- Total: **82**

This includes nested files under tools regardless of extension; there are no additional nested tools entries in the tree listing. Quality directory matching is direct-child as the `*` notation specifies; deeper quality files excluded.

Counter claim: frozen C1 output at freeze revision reportedly `population=82`. Independently computed total is 82, so **set-count agrees: PASS**. The older base population of 79 is not a valid comparator for this freeze because the C1 checker and counter are additions by freeze.

Exact set: `tools/` (17 paths, listed by `ls-tree`):

```
tools/mado-action-plan.py
tools/mado-anims.py
tools/mado-assessment.py
tools/mado-binds.py
tools/mado-devices.py
tools/mado-eventq.py
tools/mado-evidence-audit.py
tools/mado-geometry.py
tools/mado-globals.py
tools/mado-hostguard.py
tools/mado-keysym.py
tools/mado-monitors.py
tools/mado-options.py
tools/mado-terminal.py
tools/mado-tripwire.py
tools/mado-verify.sh
tools/mado-wsrules.py
```

For the exact 65 quality paths (18 top-level + 47 counters), see the frozen tree query above; the independent selection is set-exact under the rule. The previous population manifest at `w1/ExecLedgerPopulation/population.json` is for round base `6ca8c559...` and reports 79; it is not the freeze population and cannot establish equality at 56026fcb.

## Finding

No actionable population mismatch identified: the independent freeze count is 82, matching the frozen counter's `population=82`. The former 79→81 numbers in w1 artifacts correspond to round base/data revision and are not evidence against freeze revision. This audits population only, not ledger row completeness or other C1 clauses.

## Deliverables

- `.ufo/waves/round-51/w2/RevC1Population/population-audit.md`

Report: `.ufo/waves/round-51/w2/RevC1Population.md`
