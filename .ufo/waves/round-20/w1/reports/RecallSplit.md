# RecallSplit — Added pinned incident evidence-split counter

## Implementation

Added `.ufo/waves/round-20/tw-recall-split.py`; left the registered round-19 counter unchanged. The script uses the same `PIN_REV`, frozen manifest, five input files, and digest checks as `.ufo/waves/round-19/tw-recall.py` (`.ufo/waves/round-20/tw-recall-split.py:15-18,41-66`). It scans only the requested revision's committed tripwire via `--scan` in a temporary directory (`:68-76`); it does not execute transcript fixtures.

For each of the six pinned incident lines it emits every finding's class, rule, and evidence marker, translating a missing evidence key to `unmarked` (`:81-108`). `totals.detected_observed`, `detected_lead`, and `detected_unmarked` count incident lines containing at least one finding of that marker (categories can overlap if a line has mixed markers); `undetected` counts incident lines with no findings. `finding_totals` separately counts finding rows by marker. It also derives the pinned 20 non-incident control lines and counts all findings on them (`:62-66,117-130`).

## Runs and retained output

Commands (both returned exit 0):

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tw-recall-split.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tw-recall-split.py e629f73
```

Baseline output:

```json
{
 "schema": "mado-tw-recall-split-r20-v1",
 "rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "commit": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "tool_sha256": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "incident_lines": 6,
 "totals": {
  "detected_observed": 0,
  "detected_lead": 0,
  "detected_unmarked": 3,
  "undetected": 3
 },
 "finding_totals": {
  "observed": 0,
  "lead": 0,
  "unmarked": 8
 },
 "control_lines": 20,
 "control_findings": 0,
 "rows": [
  {
   "file": "inputs/r13-global-capture.jsonl",
   "line": 1,
   "findings": [
    {
     "class": "host_mutation",
     "rule": "sudo",
     "evidence": "unmarked"
    },
    {
     "class": "host_mutation",
     "rule": "pacman:-S",
     "evidence": "unmarked"
    },
    {
     "class": "live_probe",
     "rule": "wayland-info",
     "evidence": "unmarked"
    },
    {
     "class": "package_query",
     "rule": "pacman:-Q",
     "evidence": "unmarked"
    }
   ]
  },
  {
   "file": "inputs/r13-root.jsonl",
   "line": 4,
   "findings": []
  },
  {
   "file": "inputs/r14-review-source-bar.jsonl",
   "line": 1,
   "findings": [
    {
     "class": "host_mutation",
     "rule": "sudo",
     "evidence": "unmarked"
    },
    {
     "class": "host_mutation",
     "rule": "pacman:-Sw",
     "evidence": "unmarked"
    }
   ]
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 2,
   "findings": []
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 3,
   "findings": []
  },
  {
   "file": "inputs/r15-libinput-events.jsonl",
   "line": 1,
   "findings": [
    {
     "class": "host_mutation",
     "rule": "sudo",
     "evidence": "unmarked"
    },
    {
     "class": "host_mutation",
     "rule": "pacman:-S",
     "evidence": "unmarked"
    }
   ]
  }
 ]
}
```

Repair-candidate output:

```json
{
 "schema": "mado-tw-recall-split-r20-v1",
 "rev": "e629f73",
 "commit": "e629f731172b8238caffe50f152217ce56535fb4",
 "tool_sha256": "367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "incident_lines": 6,
 "totals": {
  "detected_observed": 0,
  "detected_lead": 0,
  "detected_unmarked": 6,
  "undetected": 0
 },
 "finding_totals": {
  "observed": 0,
  "lead": 0,
  "unmarked": 11
 },
 "control_lines": 20,
 "control_findings": 0,
 "rows": [
  {
   "file": "inputs/r13-global-capture.jsonl",
   "line": 1,
   "findings": [
    {
     "class": "host_mutation",
     "rule": "sudo",
     "evidence": "unmarked"
    },
    {
     "class": "host_mutation",
     "rule": "pacman:-S",
     "evidence": "unmarked"
    },
    {
     "class": "live_probe",
     "rule": "wayland-info",
     "evidence": "unmarked"
    },
    {
     "class": "package_query",
     "rule": "pacman:-Q",
     "evidence": "unmarked"
    }
   ]
  },
  {
   "file": "inputs/r13-root.jsonl",
   "line": 4,
   "findings": [
    {
     "class": "package_query",
     "rule": "pacman:-Q",
     "evidence": "unmarked"
    }
   ]
  },
  {
   "file": "inputs/r14-review-source-bar.jsonl",
   "line": 1,
   "findings": [
    {
     "class": "host_mutation",
     "rule": "sudo",
     "evidence": "unmarked"
    },
    {
     "class": "host_mutation",
     "rule": "pacman:-Sw",
     "evidence": "unmarked"
    }
   ]
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 2,
   "findings": [
    {
     "class": "package_query",
     "rule": "pacman:-Q",
     "evidence": "unmarked"
    }
   ]
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 3,
   "findings": [
    {
     "class": "package_query",
     "rule": "pacman:-Q",
     "evidence": "unmarked"
    }
   ]
  },
  {
   "file": "inputs/r15-libinput-events.jsonl",
   "line": 1,
   "findings": [
    {
     "class": "host_mutation",
     "rule": "sudo",
     "evidence": "unmarked"
    },
    {
     "class": "host_mutation",
     "rule": "pacman:-S",
     "evidence": "unmarked"
    }
   ]
  }
 ]
}
```

## Findings and evidence

- `9c54c56` yields 3/6 incident lines detected (8 findings, all missing the evidence key); `r13-root.jsonl:4` and `r14-source-safety.jsonl:2-3` are undetected. Controls: 0 findings on 20 lines.
- `e629f73` yields 6/6 incident lines detected (11 findings, all missing the evidence key); the three former misses are each `package_query/pacman:-Q`. The control set remains clean: 0 findings on 20 lines.
- The output confirms recall and finding classes for these pinned revisions, but **does not establish observed-vs-lead provenance**: both selected tool revisions emitted no `evidence` key, correctly reported as `unmarked`.
- The first attempted run caught a syntax error in the new script's lane-root expression; line 15 was corrected, and both requested commands were rerun successfully above.
- LSP was unavailable in the exposed tool inventory; this was a new standalone script, with no existing symbol refactor requested or made.

## Limits

Only the two requested revisions and the frozen five-file corpus were run. No build, formatter, linter, other suites, whole-corpus scan, or host/live operation was performed. No install was required.

## Installs

none
