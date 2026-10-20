# MutFetchVerify — round 18 wave 2 mutation probe

Date: 2026-10-20T16:05:32Z. Seat: `MadoR18.MutFetchVerify`.

## Scope and axes

Target: `abfbf35b1ed4d4a1eb294d525ef286be30f3886f:.ufo/waves/round-18/fetch-verify.py`. This is a bounded mutation probe, not a claim-admission or integration judgment.

Axes: **byte-count enforcement; SHA-256 enforcement; schema rejection; verified-only row joins; exact UTF-8 quote matching; CLI exit mapping (0 valid / 1 rejected evidence / 2 usage)**. Isolation and exact restoration are held fixed. One single-line behavior change was made per axis, each in its own private `/tmp` copy; no two defects were combined.

Read first: `SCORECARD.md` round-18 declared claims and `corpus/lessons/round-18.md` (especially M6). The target is the receipts-commit verifier, not the integration-commit tool or a moving branch name.

## Result

**6 killed; 0 survived; 0 inconclusive.** The identical 51-case detector passed on every pristine copy and every exactly restored copy. It failed on each single-line mutant. There were 18 detector invocations and 918 subject-process executions (6 copies × 3 phases × 51 cases). These are newly built seat fixtures, not an assertion about a pre-existing regression suite.

| Mutant | Pristine | Mutated | Restored | Verdict |
|---|---|---|---|---|
| M1-bytes | 51/51, detector rc=0 | 49/51, detector rc=1 | 51/51, detector rc=0 | **KILLED** |
| M2-sha | 51/51, detector rc=0 | 47/51, detector rc=1 | 51/51, detector rc=0 | **KILLED** |
| M3-schema | 51/51, detector rc=0 | 48/51, detector rc=1 | 51/51, detector rc=0 | **KILLED** |
| M4-row-join | 51/51, detector rc=0 | 46/51, detector rc=1 | 51/51, detector rc=0 | **KILLED** |
| M5-quote | 51/51, detector rc=0 | 50/51, detector rc=1 | 51/51, detector rc=0 | **KILLED** |
| M6-exit | 51/51, detector rc=0 | 48/51, detector rc=1 | 51/51, detector rc=0 | **KILLED** |

**Important detector sensitivity:** M4 leaves the subject exit code at 1 on every affected case. It is killed by checking `ROW`/`QUOTE` states and the summary, not merely the exit code. An exit-only detector would miss this mutant on these fixtures. Conversely M6 preserves rejection text but incorrectly returns 0; checking only text would miss it.

## Provenance, commands, and bounds

Read-only extraction, exit 0, empty stderr:

```sh
git show abfbf35b1ed4d4a1eb294d525ef286be30f3886f:.ufo/waves/round-18/fetch-verify.py
```

The exact stdout bytes were saved under `/tmp/mado-r18-mut-fetch-verify-10l23aqc/fetch-verify.py` and copied to six private subjects. Source size: 9752 bytes; SHA-256: `f0e91f10649685544d534e4610302f2180a5ac42a92ffde5d154af6ec2cc10e3`.

Interpreter: `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`; executable `/usr/bin/python`. No tool was installed or updated. No package, host service, compositor, device, network, browser, REA, git-write, jj, or sibling-source operation was invoked.

Fixture setup (exit 0; created 51 cases and 81 fixture files):

```sh
python3 -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/probe.py setup
```

The following exact detector command was run once per phase (pristine, mutated, restored), without changing the detector, case table, or fixtures:

```sh
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/probe.py detect /tmp/mado-r18-mut-fetch-verify-10l23aqc/M1-bytes/fetch-verify.py
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/probe.py detect /tmp/mado-r18-mut-fetch-verify-10l23aqc/M2-sha/fetch-verify.py
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/probe.py detect /tmp/mado-r18-mut-fetch-verify-10l23aqc/M3-schema/fetch-verify.py
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/probe.py detect /tmp/mado-r18-mut-fetch-verify-10l23aqc/M4-row-join/fetch-verify.py
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/probe.py detect /tmp/mado-r18-mut-fetch-verify-10l23aqc/M5-quote/fetch-verify.py
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/probe.py detect /tmp/mado-r18-mut-fetch-verify-10l23aqc/M6-exit/fetch-verify.py
```

Six independent suites ran concurrently within each phase; each suite used at most three child Python processes, with a five-second bound per subject case. All phase-error lists and detector stderr were empty. Every detect invocation checked all fixture/case hashes against the original manifest before running the cases.

- Detector SHA-256: `7d263dae1c00844e05b0c351eef3528199b69805ecdbe679ad5a66a8099820da`.
- Case-table SHA-256: `c493c32bfce3f4c0c7b068cff7020ae1af6900d4096c0d655abc82f3704185c3`.
- Fixture-manifest SHA-256, unchanged in all phases: `0bba5cb1a25ce0520d84b7d017504b7da5f8c279bfc08b50f7f8a77b8d67fdb7`.
- Complete raw commands, expectations, return codes, stdout, stderr, phase digests, and restoration records: `/tmp/mado-r18-mut-fetch-verify-10l23aqc/results.json` (SHA-256 `d2c2400fb55d95bc9522a99d752b69050bb8069dc5d7b9cb727dc5e0902865e4`). This is a scratch convenience; essential witness outputs and the exact detector are preserved below in this report.

The detector requires the expected subject return code and exact stdout; it requires empty stderr for ordinary cases and the specified diagnostic fragment for usage cases. A pristine failure would have made the corresponding mutant inconclusive; none occurred.

## Single-defect mutants and actual witness outputs

All witness stderr below was empty. The command shown is the subject command actually issued by the detector; it was identical in all three phases for that copy. Output blocks are captured stdout, not predicted output.

### M1-bytes — KILLED

Expected detector: Reject a size mismatch even when the digest is correct.

Source line 71; the only mutation:

```diff
-if not is_int or want_bytes != actual_bytes:
+if not is_int:
```

Witness case: `bytes_mismatch`.

```sh
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/M1-bytes/fetch-verify.py --fetch-root /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/bad-bytes/fetch
```

pristine: subject rc=1; stderr empty.

```text
FETCH seat/body.txt BAD_BYTES want=28 got=27
SUMMARY receipts=1 ok=0 bad=1 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

mutated: subject rc=0; stderr empty.

```text
FETCH seat/body.txt ok
SUMMARY receipts=1 ok=1 bad=0 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

restored: subject rc=1; stderr empty.

```text
FETCH seat/body.txt BAD_BYTES want=28 got=27
SUMMARY receipts=1 ok=0 bad=1 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

All cases detecting this mutant: `bytes_mismatch`, `join_rejects_bad_bytes`.

### M2-sha — KILLED

Expected detector: Reject a wrong digest even when the byte count is correct.

Source line 81; the only mutation:

```diff
-if not isinstance(want_sha, str) or got_sha != want_sha.lower():
+if not isinstance(want_sha, str):
```

Witness case: `sha_mismatch`.

```sh
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/M2-sha/fetch-verify.py --fetch-root /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/bad-sha/fetch
```

pristine: subject rc=1; stderr empty.

```text
FETCH seat/body.txt BAD_SHA want=0000000000000000000000000000000000000000000000000000000000000000 got=41e44972d84321c01335c5199fe2b4d5a9b784539ffd34967788a8e54754a685
SUMMARY receipts=1 ok=0 bad=1 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

mutated: subject rc=0; stderr empty.

```text
FETCH seat/body.txt ok
SUMMARY receipts=1 ok=1 bad=0 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

restored: subject rc=1; stderr empty.

```text
FETCH seat/body.txt BAD_SHA want=0000000000000000000000000000000000000000000000000000000000000000 got=41e44972d84321c01335c5199fe2b4d5a9b784539ffd34967788a8e54754a685
SUMMARY receipts=1 ok=0 bad=1 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

All cases detecting this mutant: `sha_mismatch`, `join_rejects_bad_sha`, `quote_bad_sha_unreceipted`, `quote_ignores_invalid_matching_body`.

### M3-schema — KILLED

Expected detector: Reject a receipt tagged with the wrong schema.

Source line 59; the only mutation:

```diff
-if not isinstance(rec, dict) or rec.get("schema") != SCHEMA:
+if not isinstance(rec, dict):
```

Witness case: `schema_wrong`.

```sh
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/M3-schema/fetch-verify.py --fetch-root /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/bad-schema/fetch
```

pristine: subject rc=1; stderr empty.

```text
FETCH seat/<line 1> BAD_SCHEMA schema-mismatch
SUMMARY receipts=1 ok=0 bad=1 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

mutated: subject rc=0; stderr empty.

```text
FETCH seat/body.txt ok
SUMMARY receipts=1 ok=1 bad=0 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

restored: subject rc=1; stderr empty.

```text
FETCH seat/<line 1> BAD_SCHEMA schema-mismatch
SUMMARY receipts=1 ok=0 bad=1 rows=0 unreceipted=0 quotes=0 quote_bad=0
```

All cases detecting this mutant: `schema_wrong`, `schema_missing`, `join_rejects_bad_schema`.

### M4-row-join — KILLED

Expected detector: Do not credit a row or quote through an integrity-failed receipt.

Source line 221; the only mutation:

```diff
-verified = [e for e in receipts if e["status"] == "ok"]
+verified = receipts
```

Witness case: `quote_bad_sha_unreceipted`.

```sh
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/M4-row-join/fetch-verify.py --fetch-root /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/bad-sha/fetch --sources /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/bad-sha/SOURCES.md --rows S072 --quote 'S072=Evidence needle'
```

pristine: subject rc=1; stderr empty.

```text
FETCH seat/body.txt BAD_SHA want=0000000000000000000000000000000000000000000000000000000000000000 got=41e44972d84321c01335c5199fe2b4d5a9b784539ffd34967788a8e54754a685
ROW S072 UNRECEIPTED
QUOTE S072 UNRECEIPTED
SUMMARY receipts=1 ok=0 bad=1 rows=1 unreceipted=1 quotes=1 quote_bad=1
```

mutated: subject rc=1; stderr empty.

```text
FETCH seat/body.txt BAD_SHA want=0000000000000000000000000000000000000000000000000000000000000000 got=41e44972d84321c01335c5199fe2b4d5a9b784539ffd34967788a8e54754a685
ROW S072 receipted
QUOTE S072 ok
SUMMARY receipts=1 ok=0 bad=1 rows=1 unreceipted=0 quotes=1 quote_bad=0
```

restored: subject rc=1; stderr empty.

```text
FETCH seat/body.txt BAD_SHA want=0000000000000000000000000000000000000000000000000000000000000000 got=41e44972d84321c01335c5199fe2b4d5a9b784539ffd34967788a8e54754a685
ROW S072 UNRECEIPTED
QUOTE S072 UNRECEIPTED
SUMMARY receipts=1 ok=0 bad=1 rows=1 unreceipted=1 quotes=1 quote_bad=1
```

All cases detecting this mutant: `join_rejects_bad_sha`, `join_rejects_bad_bytes`, `join_rejects_bad_schema`, `quote_bad_sha_unreceipted`, `quote_ignores_invalid_matching_body`.

### M5-quote — KILLED

Expected detector: Match quote UTF-8 bytes exactly, not with case folding.

Source line 257; the only mutation:

```diff
-if needle in bpath.read_bytes():
+if needle.lower() in bpath.read_bytes().lower():
```

Witness case: `quote_case_sensitive`.

```sh
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/M5-quote/fetch-verify.py --fetch-root /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/good/fetch --sources /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/good/SOURCES.md --rows S072 --quote 'S072=evidence needle'
```

pristine: subject rc=1; stderr empty.

```text
FETCH seat/body.txt ok
ROW S072 receipted
QUOTE S072 NOT_FOUND
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=1
```

mutated: subject rc=0; stderr empty.

```text
FETCH seat/body.txt ok
ROW S072 receipted
QUOTE S072 ok
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=0
```

restored: subject rc=1; stderr empty.

```text
FETCH seat/body.txt ok
ROW S072 receipted
QUOTE S072 NOT_FOUND
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=1
```

All cases detecting this mutant: `quote_case_sensitive`.

### M6-exit — KILLED

Expected detector: A missing quote must exit 1 even with all receipts and row joins valid.

Source line 273; the only mutation:

```diff
-sys.exit(1 if (bad or unreceipted or quote_bad) else 0)
+sys.exit(1 if (bad or unreceipted) else 0)
```

Witness case: `quote_absent`.

```sh
/usr/bin/python -I /tmp/mado-r18-mut-fetch-verify-10l23aqc/M6-exit/fetch-verify.py --fetch-root /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/good/fetch --sources /tmp/mado-r18-mut-fetch-verify-10l23aqc/fixtures/good/SOURCES.md --rows S072 --quote 'S072=not in body'
```

pristine: subject rc=1; stderr empty.

```text
FETCH seat/body.txt ok
ROW S072 receipted
QUOTE S072 NOT_FOUND
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=1
```

mutated: subject rc=0; stderr empty.

```text
FETCH seat/body.txt ok
ROW S072 receipted
QUOTE S072 NOT_FOUND
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=1
```

restored: subject rc=1; stderr empty.

```text
FETCH seat/body.txt ok
ROW S072 receipted
QUOTE S072 NOT_FOUND
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=1
```

All cases detecting this mutant: `quote_absent`, `quote_case_sensitive`, `quote_multiple`.

## Restoration evidence

Each change was reversed with a surgical patch before its restored-phase detector was run. Every restored subject compared byte-for-byte equal to the originally extracted git blob, not merely semantically equal. The source hashes below were recorded by the detector. `P` is the original and restored SHA-256:

`P = f0e91f10649685544d534e4610302f2180a5ac42a92ffde5d154af6ec2cc10e3`

| Copy | Before | Mutated SHA-256 | Restored | Exact bytes restored |
|---|---|---|---|---|
| M1-bytes | P | `84a24a081c43832f4007344c7bd7cbda6c121851450ceb88cdff7a83bca47cfd` | P | true |
| M2-sha | P | `20941bc6802bf1fdb812d90e9599faff1f7af2d1646f8111270aa6e8762f05a9` | P | true |
| M3-schema | P | `68f7d72d9334b9e40a0792dd203ce539635767f3b2e59eb6704d2d4f336e13c7` | P | true |
| M4-row-join | P | `85c5d353c86178ed6d908b96b333ae49acbfe1a59bbd6016c1be72ede3c0f3cb` | P | true |
| M5-quote | P | `317d90c5d25d29c6343a4be6006bf83deb6204b8c5d25a002ec0d5814de46c23` | P | true |
| M6-exit | P | `90d0c5780f6723c280ff083141e50d71b20f1286561d87e7fa1c263ecb8511d3` | P | true |

Observation hashes canonicalize the captured `(case id, rc, stdout, stderr)` list, excluding the subject path and the expected outcomes. Every pristine and restored suite had the same full observation hash:

`6fc67e8b71ddddadf98d3854da84c0f66608d6060788243bee15d0d001c844cf`

| Copy | Mutated observation SHA-256 | Restored observations equal pristine |
|---|---|---|
| M1-bytes | `97a5302ebb09a28a5219f24c67a595b10333f036fd2e5370743cff4e59a08001` | true |
| M2-sha | `493a1d9183366a14e30d1b7105292cb11f9094483f601b4542fc3054a677c530` | true |
| M3-schema | `3a325061e70b1f6f4caeb9fb78d2877c8d686cffe427f243b0f81683e9f01e8c` | true |
| M4-row-join | `c0eb64a8b98a6e8d603223245f5e43f3d27ac087d2950bf0a1ad71cd8c03cea5` | true |
| M5-quote | `07991d8b3d41baae019683c7da8f1b0133e11bc16313df4d2d836007aba53a7f` | true |
| M6-exit | `40a05c1ef037d9124afb4a29dc39f07fa40e399aa00373ea9851b14fb8e42eb9` | true |

All six restored suites were 51/51, detector exit 0. All immutable fixture/case hashes still matched. The lane source was never edited; the only lane file written by this seat is this report. Scratch copies and fixture data remain under the private directory named above; no sibling file was removed.

## Fixture coverage and limits

The primary body is UTF-8 `Evidence needle\ncafé\nlast\n`, 27 bytes, SHA-256 `41e44972d84321c01335c5199fe2b4d5a9b784539ffd34967788a8e54754a685`. Its receipts use `https://example.test/source` and `https://example.test/final` as inert strings, not fetched URLs. Binary NUL/invalid-UTF-8 bytes and a 1,048,583-byte body exercise raw-byte hashing and the one-MiB chunk boundary.

The 51 fixed cases and their captured pristine return codes:

| Case | Subject rc |
|---|---|
| `valid_receipt` | 0 |
| `bytes_mismatch` | 1 |
| `bytes_bool` | 1 |
| `bytes_string` | 1 |
| `bytes_float` | 1 |
| `bytes_missing` | 1 |
| `sha_mismatch` | 1 |
| `sha_missing` | 1 |
| `sha_uppercase` | 0 |
| `schema_wrong` | 1 |
| `schema_missing` | 1 |
| `schema_nonobject` | 1 |
| `body_traversal` | 1 |
| `body_dot` | 1 |
| `body_empty` | 1 |
| `body_number` | 1 |
| `body_missing` | 1 |
| `json_malformed` | 1 |
| `binary_exact_bytes` | 0 |
| `sha_across_chunk_boundary` | 0 |
| `blank_lines_ignored` | 0 |
| `join_exact_url` | 0 |
| `join_final_url` | 0 |
| `join_anchor_sha` | 0 |
| `join_unmatched` | 1 |
| `join_url_not_prefix` | 1 |
| `join_sha_only_anchor` | 1 |
| `join_rejects_bad_sha` | 1 |
| `join_rejects_bad_bytes` | 1 |
| `join_rejects_bad_schema` | 1 |
| `rows_deduplicated` | 0 |
| `quote_found` | 0 |
| `quote_absent` | 1 |
| `quote_case_sensitive` | 1 |
| `quote_utf8` | 0 |
| `quote_without_rows` | 0 |
| `quote_unreceipted` | 1 |
| `quote_bad_sha_unreceipted` | 1 |
| `quote_multiple` | 1 |
| `quote_ignores_invalid_matching_body` | 1 |
| `empty_root_vacuous` | 0 |
| `usage_rows_need_sources` | 2 |
| `usage_quote_needs_sources` | 2 |
| `usage_bad_row` | 2 |
| `usage_absent_row` | 2 |
| `usage_absent_fetch_root` | 2 |
| `usage_absent_sources` | 2 |
| `usage_quote_no_equals` | 2 |
| `usage_quote_bad_row` | 2 |
| `usage_quote_empty` | 2 |
| `usage_unknown_option` | 2 |

All ordinary cases also require exact `FETCH`/`ROW`/`QUOTE`/`SUMMARY` output. Positive joins separately cover original URL, final URL, and literal anchor digest; negative joins cover unrelated URLs, URL-prefix lookalikes, digest text outside the anchor cell, and failed receipts. Quote controls include UTF-8, case sensitivity, multiple quotes, quote-only row selection, and a verified matching row whose only quote-bearing body failed integrity. Usage cases require exit 2 before any receipt stdout.

Observed boundary, not counted as a failure: an existing empty fetch root returns exit 0 with `SUMMARY receipts=0 ok=0 bad=0 rows=0 unreceipted=0 quotes=0 quote_bad=0`. The detector preserves this documented “every receipt” behavior rather than inventing a minimum-count contract. This probe does not establish receipt authenticity, URL provenance, fetched source truth, actual S072–S095 row coverage, hostile filesystem/race handling, or exhaustive input robustness. No current-branch source or real network receipt was substituted for the pinned artifact. No defect fix or contract change was made.

## Reproduction appendix — exact detector and fixture generator

This is the exact scratch `probe.py` whose digest is recorded above. Place it beside a `fetch-verify.py` extracted with the pinned `git show`, run `setup` once in a fresh private directory, apply the six one-line changes to the named copies, and invoke the same listed detector commands in each phase. Reverse each patch exactly before the restored phase. The absolute scratch directory is embedded only by setup; fixture generation and expected outcomes are otherwise deterministic.

```python
#!/usr/bin/env python3
"""One bounded fixture detector for pristine, mutant, and restored fetch-verify bytes."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCHEMA = "mado-fetch-receipt-v1"
BODY = "Evidence needle\ncafé\nlast\n".encode("utf-8")
SHA = hashlib.sha256(BODY).hexdigest()
URL = "https://example.test/source"
FINAL = "https://example.test/final"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def summary(n=1, bad=0, rows=0, unreceipted=0, quotes=0, quote_bad=0):
    return (f"SUMMARY receipts={n} ok={n-bad} bad={bad} rows={rows} "
            f"unreceipted={unreceipted} quotes={quotes} quote_bad={quote_bad}")


def setup():
    cases = []
    fixtures = ROOT / "fixtures"
    fixtures.mkdir()

    def receipt(**changes):
        result = {"schema": SCHEMA, "url": URL, "final_url": FINAL,
                  "http_status": 200, "fetched_at": "2026-10-20T00:00:00Z",
                  "bytes": len(BODY), "sha256": SHA, "body": "body.txt",
                  "tool": "synthetic-fixture; no network"}
        result.update(changes)
        return result

    def fixture(name, rec=None, body=BODY, raw=None, source_url=URL,
                anchor="fixture lines 1-3", teaches="fixture source", exists=True):
        base = fixtures / name
        seat = base / "fetch" / "seat"
        seat.mkdir(parents=True)
        if exists:
            (seat / "body.txt").write_bytes(body)
        record = receipt() if rec is None else rec
        text = raw if raw is not None else json.dumps(record, ensure_ascii=False) + "\n"
        (seat / "receipts.jsonl").write_text(text, encoding="utf-8")
        (base / "SOURCES.md").write_text(
            "# Synthetic sources\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            f"| S072 | Fixture — {source_url} | docs | A | synthetic | {anchor} | {teaches} | mined | 2026-10-20 | on-release | synthetic.md |\n",
            encoding="utf-8")
        return base

    def check(name, base, expected, rc=0, extra=(), error=""):
        cases.append({"id": name,
                      "argv": ["--fetch-root", str(base / "fetch"), *extra],
                      "rc": rc,
                      "stdout": "\n".join(expected) + "\n" if expected else "",
                      "stderr_contains": error,
                      "stderr_empty": not error})

    good = fixture("good")
    ok = "FETCH seat/body.txt ok"
    check("valid_receipt", good, [ok, summary()])

    wrong_bytes = receipt(bytes=len(BODY)+1)
    bad_bytes = fixture("bad-bytes", wrong_bytes)
    bytes_line = f"FETCH seat/body.txt BAD_BYTES want={len(BODY)+1} got={len(BODY)}"
    check("bytes_mismatch", bad_bytes, [bytes_line, summary(bad=1)], 1)
    for name, value in [("bool", True), ("string", str(len(BODY))), ("float", float(len(BODY))), ("missing", None)]:
        rec = receipt(bytes=value)
        if name == "missing":
            del rec["bytes"]
        base = fixture("bytes-"+name, rec)
        check("bytes_"+name, base,
              [f"FETCH seat/body.txt BAD_BYTES want={value!r} got={len(BODY)}", summary(bad=1)], 1)

    bad_sha_rec = receipt(sha256="0"*64)
    bad_sha = fixture("bad-sha", bad_sha_rec)
    sha_line = f"FETCH seat/body.txt BAD_SHA want={'0'*64} got={SHA}"
    check("sha_mismatch", bad_sha, [sha_line, summary(bad=1)], 1)
    rec = receipt()
    del rec["sha256"]
    check("sha_missing", fixture("sha-missing", rec),
          [f"FETCH seat/body.txt BAD_SHA want=None got={SHA}", summary(bad=1)], 1)
    check("sha_uppercase", fixture("sha-upper", receipt(sha256=SHA.upper())), [ok, summary()])

    schema_line = "FETCH seat/<line 1> BAD_SCHEMA schema-mismatch"
    bad_schema = fixture("bad-schema", receipt(schema="mado-fetch-receipt-v0"))
    check("schema_wrong", bad_schema, [schema_line, summary(bad=1)], 1)
    rec = receipt()
    del rec["schema"]
    check("schema_missing", fixture("schema-missing", rec), [schema_line, summary(bad=1)], 1)
    check("schema_nonobject", fixture("schema-nonobject", ["not", "an", "object"]), [schema_line, summary(bad=1)], 1)
    for name, value in [("traversal", "../body.txt"), ("dot", "."), ("empty", ""), ("number", 1)]:
        check("body_"+name, fixture("body-"+name, receipt(body=value)),
              ["FETCH seat/<line 1> BAD_SCHEMA bad-body-field", summary(bad=1)], 1)
    check("body_missing", fixture("body-missing", exists=False), ["FETCH seat/body.txt MISSING", summary(bad=1)], 1)
    check("json_malformed", fixture("json-malformed", raw="{invalid\n"),
          ["FETCH seat/<line 1> BAD_JSON", summary(bad=1)], 1)

    binary = b"\x00\xff\r\n\x80binary\x00"
    check("binary_exact_bytes", fixture("binary", receipt(bytes=len(binary), sha256=digest(binary)), body=binary), [ok, summary()])
    big = b"Z" * ((1 << 20) + 7)
    check("sha_across_chunk_boundary", fixture("chunk-boundary", receipt(bytes=len(big), sha256=digest(big)), body=big), [ok, summary()])
    check("blank_lines_ignored", fixture("blank-lines", raw="\n  \n"+json.dumps(receipt())+"\n\n"), [ok, summary()])

    def joins(base, *extra):
        return ["--sources", str(base / "SOURCES.md"), *extra]

    row_ok = "ROW S072 receipted"
    row_bad = "ROW S072 UNRECEIPTED"
    check("join_exact_url", good, [ok, row_ok, summary(rows=1)], extra=joins(good, "--rows", "S072"))
    final = fixture("final-url", source_url=FINAL)
    check("join_final_url", final, [ok, row_ok, summary(rows=1)], extra=joins(final, "--rows", "S072"))
    by_sha = fixture("sha-anchor", source_url="https://example.test/other", anchor="sha256="+SHA)
    check("join_anchor_sha", by_sha, [ok, row_ok, summary(rows=1)], extra=joins(by_sha, "--rows", "S072"))
    unmatched = fixture("unmatched", source_url="https://example.test/unrelated")
    check("join_unmatched", unmatched, [ok, row_bad, summary(rows=1, unreceipted=1)], 1,
          joins(unmatched, "--rows", "S072"))
    prefix = fixture("url-prefix", source_url=URL+"-different")
    check("join_url_not_prefix", prefix, [ok, row_bad, summary(rows=1, unreceipted=1)], 1,
          joins(prefix, "--rows", "S072"))
    elsewhere = fixture("sha-outside-anchor", source_url="https://example.test/other", teaches=SHA)
    check("join_sha_only_anchor", elsewhere, [ok, row_bad, summary(rows=1, unreceipted=1)], 1,
          joins(elsewhere, "--rows", "S072"))
    for name, base, line in [("sha", bad_sha, sha_line), ("bytes", bad_bytes, bytes_line), ("schema", bad_schema, schema_line)]:
        check("join_rejects_bad_"+name, base, [line, row_bad, summary(bad=1, rows=1, unreceipted=1)], 1,
              joins(base, "--rows", "S072"))
    check("rows_deduplicated", good, [ok, row_ok, summary(rows=1)],
          extra=joins(good, "--rows", "S072,S072", "--rows", " S072 "))

    for name, quote, found in [("found", "Evidence needle", True), ("absent", "not in body", False),
                               ("case_sensitive", "evidence needle", False), ("utf8", "café", True)]:
        check("quote_"+name, good,
              [ok, row_ok, "QUOTE S072 "+("ok" if found else "NOT_FOUND"),
               summary(rows=1, quotes=1, quote_bad=0 if found else 1)], 0 if found else 1,
              joins(good, "--rows", "S072", "--quote", "S072="+quote))
    check("quote_without_rows", good, [ok, "QUOTE S072 ok", summary(quotes=1)],
          extra=joins(good, "--quote", "S072=Evidence needle"))
    check("quote_unreceipted", unmatched,
          [ok, row_bad, "QUOTE S072 UNRECEIPTED", summary(rows=1, unreceipted=1, quotes=1, quote_bad=1)], 1,
          joins(unmatched, "--rows", "S072", "--quote", "S072=Evidence needle"))
    check("quote_bad_sha_unreceipted", bad_sha,
          [sha_line, row_bad, "QUOTE S072 UNRECEIPTED", summary(bad=1, rows=1, unreceipted=1, quotes=1, quote_bad=1)], 1,
          joins(bad_sha, "--rows", "S072", "--quote", "S072=Evidence needle"))
    check("quote_multiple", good,
          [ok, row_ok, "QUOTE S072 ok", "QUOTE S072 NOT_FOUND", summary(rows=1, quotes=2, quote_bad=1)], 1,
          joins(good, "--rows", "S072", "--quote", "S072=Evidence needle", "--quote", "S072=not in body"))
    two = fixture("two-receipts", bad_sha_rec)
    other_body = b"Verified unrelated text\n"
    other = receipt(body="other.txt", bytes=len(other_body), sha256=digest(other_body))
    seat = two / "fetch" / "seat"
    (seat / "other.txt").write_bytes(other_body)
    with (seat / "receipts.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(other)+"\n")
    check("quote_ignores_invalid_matching_body", two,
          [sha_line, "FETCH seat/other.txt ok", row_ok, "QUOTE S072 NOT_FOUND",
           summary(n=2, bad=1, rows=1, quotes=1, quote_bad=1)], 1,
          joins(two, "--rows", "S072", "--quote", "S072=Evidence needle"))

    empty = fixtures / "empty"
    (empty / "fetch").mkdir(parents=True)
    check("empty_root_vacuous", empty, [summary(n=0)])
    check("usage_rows_need_sources", good, [], 2, ["--rows", "S072"], "--rows/--quote require --sources")
    check("usage_quote_needs_sources", good, [], 2, ["--quote", "S072=x"], "--rows/--quote require --sources")
    check("usage_bad_row", good, [], 2, joins(good, "--rows", "bad"), "bad row id: 'bad'")
    check("usage_absent_row", good, [], 2, joins(good, "--rows", "S999"), "row S999 not found in")
    check("usage_absent_fetch_root", good, [], 2, ["--fetch-root", str(ROOT / "absent")], "fetch root not a directory:")
    check("usage_absent_sources", good, [], 2, ["--sources", str(ROOT / "absent.md")], "cannot read --sources")
    check("usage_quote_no_equals", good, [], 2, joins(good, "--quote", "S072"), "--quote spec must be")
    check("usage_quote_bad_row", good, [], 2, joins(good, "--quote", "BAD=x"), "--quote spec has bad row id")
    check("usage_quote_empty", good, [], 2, joins(good, "--quote", "S072="), "--quote spec has empty text")
    check("usage_unknown_option", good, [], 2, ["--bogus"], "unrecognized arguments: --bogus")

    (ROOT / "cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    source = (ROOT / "fetch-verify.py").read_bytes()
    for name in ["M1-bytes", "M2-sha", "M3-schema", "M4-row-join", "M5-quote", "M6-exit"]:
        destination = ROOT / name / "fetch-verify.py"
        destination.parent.mkdir()
        destination.write_bytes(source)
    manifest = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in sorted(fixtures.rglob("*")) if p.is_file()}
    manifest["cases.json"] = digest((ROOT / "cases.json").read_bytes())
    (ROOT / "fixture-manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "fixture_files": len(manifest)-1,
                      "fixture_manifest_sha256": digest((ROOT / "fixture-manifest.json").read_bytes()),
                      "source_sha256": digest(source)}, indent=2))


def detect(subject):
    manifest_path = ROOT / "fixture-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    changed = [name for name, sha in manifest.items() if digest((ROOT / name).read_bytes()) != sha]
    if changed:
        raise RuntimeError(f"fixture bytes changed: {changed}")
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))

    def exercise(case):
        cmd = [sys.executable, "-I", str(subject), *case["argv"]]
        got = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=5)
        mismatch = []
        if got.returncode != case["rc"]:
            mismatch.append("exit")
        if got.stdout != case["stdout"]:
            mismatch.append("stdout")
        if ((case["stderr_empty"] and got.stderr) or
                (case["stderr_contains"] and case["stderr_contains"] not in got.stderr)):
            mismatch.append("stderr")
        return {"id": case["id"], "command": cmd, "rc": got.returncode,
                "stdout": got.stdout, "stderr": got.stderr, "mismatch": mismatch,
                "expected": {"rc": case["rc"], "stdout": case["stdout"],
                             "stderr_contains": case["stderr_contains"]}}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(exercise, cases))
    observations = [{key: rec[key] for key in ("id", "rc", "stdout", "stderr")} for rec in records]
    mismatches = [rec["id"] for rec in records if rec["mismatch"]]
    result = {"subject": str(subject), "subject_sha256": digest(subject.read_bytes()),
              "detector_sha256": digest(Path(__file__).read_bytes()),
              "fixture_manifest_sha256": digest(manifest_path.read_bytes()),
              "cases": len(cases), "passed": len(cases)-len(mismatches), "mismatches": mismatches,
              "observations_sha256": digest(json.dumps(observations, sort_keys=True, ensure_ascii=False).encode()),
              "records": records}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return bool(mismatches)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "setup":
        setup()
    elif len(sys.argv) == 3 and sys.argv[1] == "detect":
        sys.exit(detect(Path(sys.argv[2]).resolve()))
    else:
        raise SystemExit("usage: probe.py setup | probe.py detect SUBJECT")
```
