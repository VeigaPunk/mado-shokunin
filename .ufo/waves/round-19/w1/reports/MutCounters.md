# MutCounters — 4 mutants killed by data; 3 survived at both revisions; exact restoration

## Axes and scope

- **Calibration:** distinguish output-discriminating checks from unexercised safeguards.
- **Coverage:** probe five requested behavior classes with seven isolated one-line mutants (denominator and score in both counters).
- **Operability / isolation:** run identical bounded commands on pristine, mutated and exactly restored scratch bytes; leave canonical counters untouched.

Target lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Only this report was written inside the lane. All counter copies, clone metadata and raw probe receipts were confined to `/tmp/mado-r19-MutCounters-i78vnign`. No delegation, git/jj writes in the lane, live gate, host probes, web fetches or other runtime were used.

- **B:** `9c54c56` resolves to `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.
- **P:** `17661e0fa83f978fb659f5bb8fef47f0969f6945`.
- Python: `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`.
- A local `git clone --quiet --shared --no-checkout` supplied committed objects in the scratch tree; source script bytes were copied verbatim into the same four-level path topology, preserving their LANE calculation.
- Up to six independent counter subprocesses ran concurrently; each had a 30-second timeout. All runs used `python3 -I`, `GIT_OPTIONAL_LOCKS=0`, and scratch-repo cwd. No timeout occurred.

## Detector and baseline

The detector compares the **exact `(exit code, stdout, stderr)` tuple** for the same script path and requested revision across phases. A valid pristine run must exit 0 and produce JSON; otherwise that mutant/revision is inconclusive. A changed observable tuple is called **killed by data**, per this assignment; unchanged output is **survived**. The same command was repeated after exact byte restoration.

| Counter | B pristine | P pristine |
|---|---|---|
| tw-recall.py | 3/6; score 5.0 | 3/6; score 5.0 |
| fresh-pins.py | 2/13; score 1.5385 | 2/13; score 1.5385 |

Observed **42 executions** = 7 mutants × 2 revisions × 3 phases. All exited 0: `true`. All stderr strings were empty: `true`. There were **zero inconclusive baselines**. Both formula mutants, the POINTER mutant and the scope mutant changed output at both revisions; both denominator mutants and the digest-guard deletion did not.

**Important boundary:** all mutated scripts still exited 0. These are output-comparison kills, not an assertion that the scripts contain a built-in mutant-rejecting gate. An exit-code-only invocation would not distinguish any of these mutants.

## Mutants and observed outputs

Notation in the result columns: numerator/denominator; score. Each change below was the only changed source line in its own copy.

| Mutant | Canonical behavior point | B mutated | P mutated | Verdict at both |
|---|---|---|---|---|
| T-denominator | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tw-recall.py:49` | 3/6; 5.0 | 3/6; 5.0 | survived |
| T-digest | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tw-recall.py:58` | 3/6; 5.0 | 3/6; 5.0 | survived |
| T-score | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tw-recall.py:84` | 3/6; 4.2857 | 3/6; 4.2857 | killed by data |
| F-denominator | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/fresh-pins.py:58` | 2/13; 1.5385 | 2/13; 1.5385 | survived |
| F-pointer | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/fresh-pins.py:28` | 3/13; 2.3077 | 3/13; 2.3077 | killed by data |
| F-scope | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/fresh-pins.py:38` | 2/12; 1.6667 | 2/12; 1.6667 | killed by data |
| F-score | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/fresh-pins.py:81` | 2/13; 1.4286 | 2/13; 1.4286 | killed by data |

### Exact mutations

#### T-denominator

Unfreeze the incident-manifest/denominator source by reading requested REV instead of PIN_REV; leave emitted pin_rev unchanged.

Scratch copy: `/tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-denominator.py`; line 49.

Before:
```python
    exp = json.loads(show(PIN_REV, f"{FROZEN}/expected.json"))
```
After:
```python
    exp = json.loads(show(rev, f"{FROZEN}/expected.json"))
```

#### T-digest

Delete the input-digest guard (a single-condition guard-omission mutant).

Scratch copy: `/tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-digest.py`; line 58.

Before:
```python
            if hashlib.sha256(b).hexdigest() != inp["sha256"]:
```
After:
```python
            if False:
```

#### T-score

Add an off-by-one to the scoring denominator, without changing incident membership or detections.

Scratch copy: `/tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-score.py`; line 84.

Before:
```python
        "score": round(10 * det / len(rows), 4),
```
After:
```python
        "score": round(10 * det / (len(rows) + 1), 4),
```

#### F-denominator

Unfreeze OLD-token eligibility by scanning candidate bytes at requested REV, while leaving the candidate path listing pinned.

Scratch copy: `/tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-denominator.py`; line 58.

Before:
```python
        b = git("show", f"{PIN_REV}:{p}")
```
After:
```python
        b = git("show", f"{rev}:{p}")
```

#### F-pointer

Accept a version mention without its same-line S### source token.

Scratch copy: `/tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-pointer.py`; line 28.

Before:
```python
POINTER = re.compile(r"2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2")
```
After:
```python
POINTER = re.compile(r"2\.17\.2")
```

#### F-scope

Omit the tools/ owned-file scope arm.

Scratch copy: `/tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-scope.py`; line 38.

Before:
```python
            or p.startswith("tools/"))
```
After:
```python
            or False)
```

#### F-score

Add an off-by-one to the scoring denominator, without changing ownership or pointer matches.

Scratch copy: `/tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-score.py`; line 81.

Before:
```python
        "score": round(10 * cur / len(rows), 4) if rows else None,
```
After:
```python
        "score": round(10 * cur / (len(rows) + 1), 4) if rows else None,
```

### What the data killed

- **T-score:** only `score` changed, 5.0 → 4.2857; `detected=3`, `incident_lines=6` and all rows were unchanged.
- **F-score:** only `score` changed, 1.5385 → 1.4286; `current=2`, `denominator=13` and all rows were unchanged.
- **F-pointer:** `current` increased 2 → 3 and `score` 1.5385 → 2.3077. `SKILL.md` became current solely on version mentions at lines **1825 and 1827**; the original regex found no pointer there. The existing current row `corpus/knowledge/walker-route-r18.md` also expanded its reported pointer lines from `[1]` to `[1, 2, 21, 22, 23]`. These row deltas were identical at B and P.
- **F-scope:** excluding tools removed exactly the noncurrent `tools/mado-verify.sh` row, reducing denominator 13 → 12 and raising score 1.5385 → 1.6667 while current stayed 2. The row delta was identical at B and P.

### Survivors / unguarded by this two-revision detector

- **T-denominator:** changing the source of the incident manifest from PIN_REV to requested REV left the full output byte-for-byte unchanged at both B and P. At B the revisions are deliberately identical; P also supplied no distinguishing observation for this mutation.
- **F-denominator:** using requested-REV bytes to decide whether a candidate contains OLD left all 13 denominator rows and the full output unchanged at both B and P. This probes denominator content pinning, not the separately pinned ls-tree path enumeration.
- **T-digest:** deleting digest rejection left full output unchanged at both B and P. These valid frozen inputs do not exercise the rejecting branch. This is a detector-coverage finding, **not** evidence that the original script lacks a digest check.

[INFERENCE] A separate contrast would be needed to establish kills for those safeguards: drift the incident manifest at a later requested revision; remove an OLD token while keeping an owned path; or supply a frozen input whose bytes do not match its recorded digest. Those contrasts were not executed and no contract or production code was changed to compensate.

## Commands and complete output ledger

Every command below ran with cwd `/tmp/mado-r19-MutCounters-i78vnign/repo`, once pristine, once mutated and once restored, using that same file path for all three phases:

```sh
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-denominator.py 9c54c56
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-denominator.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-digest.py 9c54c56
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-digest.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-score.py 9c54c56
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/tw-score.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-denominator.py 9c54c56
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-denominator.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-pointer.py 9c54c56
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-pointer.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-scope.py 9c54c56
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-scope.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-score.py 9c54c56
python3 -I /tmp/mado-r19-MutCounters-i78vnign/repo/.ufo/waves/round-19/fresh-score.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
```

Output IDs below reference the complete captured stdout and hashes in the next section; no stdout normalization was used for comparisons. All cells have exit 0 and stderr `""`.

| Mutant | Revision | Pristine output | Mutated output | Restored output | Restored exact tuple equals pristine |
|---|---|---|---|---|---|
| T-denominator | B | O01 | O01 | O01 | true |
| T-denominator | P | O02 | O02 | O02 | true |
| T-digest | B | O01 | O01 | O01 | true |
| T-digest | P | O02 | O02 | O02 | true |
| T-score | B | O01 | O03 | O01 | true |
| T-score | P | O02 | O04 | O02 | true |
| F-denominator | B | O05 | O05 | O05 | true |
| F-denominator | P | O06 | O06 | O06 | true |
| F-pointer | B | O05 | O07 | O05 | true |
| F-pointer | P | O06 | O08 | O06 | true |
| F-scope | B | O05 | O09 | O05 | true |
| F-scope | P | O06 | O10 | O06 | true |
| F-score | B | O05 | O11 | O05 | true |
| F-score | P | O06 | O12 | O06 | true |

### Captured stdout, deduplicated by exact bytes

The fenced JSON is captured stdout (including its final newline before the closing fence), not a reconstructed subset. Each ID also fixes exit code and stderr. Empty-stderr SHA-256 for every execution: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

#### O01

Exit: `0`; stderr: `""`; stdout SHA-256: `b61d93511bb517aa88d93099343e803d75af2e74a1ebdac647b737019045a556`.

```json
{
 "schema": "mado-tw-recall-r19-v1",
 "rev": "9c54c56",
 "commit": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "tool_sha256": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "incident_lines": 6,
 "detected": 3,
 "score": 5.0,
 "rows": [
  {
   "file": "inputs/r13-global-capture.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r13-root.jsonl",
   "line": 4,
   "detected": false
  },
  {
   "file": "inputs/r14-review-source-bar.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 2,
   "detected": false
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 3,
   "detected": false
  },
  {
   "file": "inputs/r15-libinput-events.jsonl",
   "line": 1,
   "detected": true
  }
 ]
}
```

#### O02

Exit: `0`; stderr: `""`; stdout SHA-256: `4b028d30a7c52c8202d156f5c6c6a0e1f11a78acc64feaacaa3341179b7a7541`.

```json
{
 "schema": "mado-tw-recall-r19-v1",
 "rev": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "commit": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "tool_sha256": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "incident_lines": 6,
 "detected": 3,
 "score": 5.0,
 "rows": [
  {
   "file": "inputs/r13-global-capture.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r13-root.jsonl",
   "line": 4,
   "detected": false
  },
  {
   "file": "inputs/r14-review-source-bar.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 2,
   "detected": false
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 3,
   "detected": false
  },
  {
   "file": "inputs/r15-libinput-events.jsonl",
   "line": 1,
   "detected": true
  }
 ]
}
```

#### O03

Exit: `0`; stderr: `""`; stdout SHA-256: `b532766350e5c6a7ce098c0265c278e5b4caf544a15f63846aaf616b21d718c9`.

```json
{
 "schema": "mado-tw-recall-r19-v1",
 "rev": "9c54c56",
 "commit": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "tool_sha256": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "incident_lines": 6,
 "detected": 3,
 "score": 4.2857,
 "rows": [
  {
   "file": "inputs/r13-global-capture.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r13-root.jsonl",
   "line": 4,
   "detected": false
  },
  {
   "file": "inputs/r14-review-source-bar.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 2,
   "detected": false
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 3,
   "detected": false
  },
  {
   "file": "inputs/r15-libinput-events.jsonl",
   "line": 1,
   "detected": true
  }
 ]
}
```

#### O04

Exit: `0`; stderr: `""`; stdout SHA-256: `a0f38df2838fa5f5610e839edcb6ada0b4b5acec551f93d3af1ce2d23487b9f6`.

```json
{
 "schema": "mado-tw-recall-r19-v1",
 "rev": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "commit": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "tool_sha256": "c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "incident_lines": 6,
 "detected": 3,
 "score": 4.2857,
 "rows": [
  {
   "file": "inputs/r13-global-capture.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r13-root.jsonl",
   "line": 4,
   "detected": false
  },
  {
   "file": "inputs/r14-review-source-bar.jsonl",
   "line": 1,
   "detected": true
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 2,
   "detected": false
  },
  {
   "file": "inputs/r14-source-safety.jsonl",
   "line": 3,
   "detected": false
  },
  {
   "file": "inputs/r15-libinput-events.jsonl",
   "line": 1,
   "detected": true
  }
 ]
}
```

#### O05

Exit: `0`; stderr: `""`; stdout SHA-256: `bf7db8e833727b8aeefc146f5ce816aa93daa5da24b6a9c3fa76f797dbbd5d58`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "9c54c56",
 "commit": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 13,
 "current": 2,
 "score": 1.5385,
 "rows": [
  {
   "path": "SKILL.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "tools/mado-verify.sh",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

#### O06

Exit: `0`; stderr: `""`; stdout SHA-256: `c82206c00d11b530ffad0e092eb34f6fc57673b31ea97049c58935060897c3ef`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "commit": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 13,
 "current": 2,
 "score": 1.5385,
 "rows": [
  {
   "path": "SKILL.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "tools/mado-verify.sh",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

#### O07

Exit: `0`; stderr: `""`; stdout SHA-256: `e08953d591a1ac7cf438ef6d9ea4082da7fa315dd4dd74aa159b8f79e1f7b3c9`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "9c54c56",
 "commit": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 13,
 "current": 3,
 "score": 2.3077,
 "rows": [
  {
   "path": "SKILL.md",
   "current": true,
   "pointer_lines": [
    1825,
    1827
   ]
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1,
    2,
    21,
    22,
    23
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "tools/mado-verify.sh",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

#### O08

Exit: `0`; stderr: `""`; stdout SHA-256: `4144342533861969bbbe9a5408e6d87ea1254a77e5fdcf9a6a5f308a214f93bf`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "commit": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 13,
 "current": 3,
 "score": 2.3077,
 "rows": [
  {
   "path": "SKILL.md",
   "current": true,
   "pointer_lines": [
    1825,
    1827
   ]
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1,
    2,
    21,
    22,
    23
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "tools/mado-verify.sh",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

#### O09

Exit: `0`; stderr: `""`; stdout SHA-256: `ce73c58771a4e0decfea2e8da82984b86e8404b9f791bf444800f1ed8d03e7e7`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "9c54c56",
 "commit": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 12,
 "current": 2,
 "score": 1.6667,
 "rows": [
  {
   "path": "SKILL.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

#### O10

Exit: `0`; stderr: `""`; stdout SHA-256: `6288290731fb191b6a0fd5b4066959701ad864eaae447b650aeeaa764a3c7240`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "commit": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 12,
 "current": 2,
 "score": 1.6667,
 "rows": [
  {
   "path": "SKILL.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

#### O11

Exit: `0`; stderr: `""`; stdout SHA-256: `82f2092d300365aae8491b5be235429d1b894948a0bae4c45a1ffecf8ecf97f0`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "9c54c56",
 "commit": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 13,
 "current": 2,
 "score": 1.4286,
 "rows": [
  {
   "path": "SKILL.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "tools/mado-verify.sh",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

#### O12

Exit: `0`; stderr: `""`; stdout SHA-256: `536e2a1ddd9c92955a8ba8b567571271d428d4b3fc79fcbdda54dba2541d322a`.

```json
{
 "schema": "mado-fresh-pins-r19-v1",
 "rev": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "commit": "17661e0fa83f978fb659f5bb8fef47f0969f6945",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "denominator": 13,
 "current": 2,
 "score": 1.4286,
 "rows": [
  {
   "path": "SKILL.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/README.md",
   "current": true,
   "pointer_lines": [
    44
   ]
  },
  {
   "path": "corpus/knowledge/arc-synthesis.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/closeout-r11.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/config-health-report-r3.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/remaining-planes-census.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep-r9.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-deep.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-live-surface.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/walker-route-r18.md",
   "current": true,
   "pointer_lines": [
    1
   ]
  },
  {
   "path": "corpus/knowledge/waybar-walker-plane.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "corpus/knowledge/waybar-walker-semantics.md",
   "current": false,
   "pointer_lines": []
  },
  {
   "path": "tools/mado-verify.sh",
   "current": false,
   "pointer_lines": []
  }
 ]
}
```

## Restoration evidence

All seven scratch copies were restored from the original byte snapshots in a `finally` block, before the restored-phase detector executions. Each restored file compared byte-for-byte equal to its source snapshot, not merely semantically equal. All restored detector tuples matched their own pristine tuples at both revisions.

| Mutant | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | Exact restored bytes |
|---|---|---|---|---|
| T-denominator | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | `8aa394afcf237f0fde1bf1a6ed2013d9b27b94cd1cf1b954bed2a8dff0517784` | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | true |
| T-digest | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | `6f2a75edcdc767d2a3d834f767d52995df3fe2a359c98c4aad686d27badc53bd` | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | true |
| T-score | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | `485dc65ca5b3d5df17c65ec27ee9ab88eed90e826418bb07305d7f80bd23af80` | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | true |
| F-denominator | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | `4f54e83350ad158385a0fc65dab0de4034e76b57098ecaff1f4ad8975409b840` | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | true |
| F-pointer | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | `2c49e251191b961243afd736e7563f78e35449dec0cb92d1752aa0ab368f7f4f` | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | true |
| F-scope | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | `6734f71f731628ddc7cccf3681da58338adbb32e7c9a21154e85d491d7067fbe` | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | true |
| F-score | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | `a81bf20189b9b1d24b81be43b0585da4c348b25ba4755d2c23717e73ad0c49d0` | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | true |

Pre/post file hashes were stable across every one of the 42 counter executions: `true`.

Canonical lane counter hashes before/after the experiment:

| Canonical file | Before SHA-256 | After SHA-256 | Unchanged bytes |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tw-recall.py` | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28` | true |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/fresh-pins.py` | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789` | true |

Supplementary raw run records remain in `/tmp/mado-r19-MutCounters-i78vnign/receipts-all.json`; this report embeds all unique stdout plus the complete 42-run phase mapping, so the verdicts do not depend on retaining that temporary file.

## Limits

- Only the two assigned revisions and the seven documented one-line mutations were exercised. Survival is bounded to those data; it is not proof of equivalence or permission to change the invariant.
- The denominator probes deliberately unpin a behavior-bearing read; they do not rewrite the PIN_REV metadata constant. F-denominator leaves candidate path enumeration pinned. Other denominator failure modes were not tested.
- No deliberately corrupt input, additional revision, cross-line POINTER mutation, or other regex/scope variant was executed.
- This report records mutation evidence only: no judgement, integration, production changes, additional suites or live-environment verification.
- No web sources were opened.

## Installs

none
