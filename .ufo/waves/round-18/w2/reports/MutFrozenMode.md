# MutFrozenMode — frozen replay mutation probe

## Scope and axes

- Producer revision: `abfbf35b1ed4d4a1eb294d525ef286be30f3886f` (receipts revision named by hash; no HEAD selector).
- Source extraction: `git show abfbf35b1ed4d4a1eb294d525ef286be30f3886f:tools/mado-tripwire.py` in `/home/vgpnk/Projects/shokunin/mado-shokunin`.
- Pristine source: **48852 bytes**, SHA-256 `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb`.
- Isolated laboratory: `/tmp/MadoR18-MutFrozenMode-z5sr1h7o`; 15 independent copies at `<laboratory>/M01..M15/mado-tripwire.py`. No stacked mutations.
- Axes: **operability** (frozen replay rejects a bad snapshot/verdict), **calibration** (actual mutant bite rather than assertion), **coverage** (digest, file identity, multiset, known-miss and verdict predicates).
- Scope respected: no lane source/fixture changes; only this report is written in the lane. No git/jj write, host probe, package-manager command, package install/update, network connection, delegation, or other application runtime.
- Mutation/restoration detector window (UTC): `2026-10-20T16:02:40.777083Z` → `2026-10-20T16:02:44.988278Z`.

## Detector and method

The identical bounded two-command detector was run on each copy before mutation, with its one mutation, and after exact-byte restoration. Independent copies ran in a four-worker thread pool; the two commands within a copy ran in the order shown. Every outer command had a 45-second timeout. The suite itself invokes its 17 frozen cases. No timeout occurred.

```sh
python3 -I /tmp/MadoR18-MutFrozenMode-z5sr1h7o/MNN/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen
python3 -I /tmp/MadoR18-MutFrozenMode-z5sr1h7o/MNN/mado-tripwire.py --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen
```

`MNN` is the literal M01 through M15 path in the embedded raw receipts. A mutant is killed only when its baseline and restoration both pass and the mutated detector fails. A baseline failure/timeout would be inconclusive, not a kill. Restoration is in a `finally` block and was completed for every copy.

## Observed result

**7 killed · 8 survived · 0 inconclusive (15 mutants).** All 15 pristine and all 15 restored selftests returned `SELFTEST_SUMMARY: 17/17 passed failed=[]` with exit 0; all pristine/restored real snapshots returned `MADO_TRIPWIRE_FROZEN: frozen_match` with exit 0. **Every mutated real-snapshot command also returned frozen_match/0**; the seven kills came from the synthetic selftest. All 90 outer commands completed; every stderr was empty.

| Mutant | One behavior-bearing change (original source line) | Mutated selftest | Real frozen replay | Verdict |
|---|---|---|---|---|
| M01 | snapshot-digest-compare, L980-981 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M02 | scan-redigest-compare, L1022 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M03 | unlisted-input-check, L965 | `SELFTEST_SUMMARY: 16/17 passed failed=['extra-unlisted-input']`; rc=1 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **killed** |
| M04 | snapshot-symlink-check, L946 | `SELFTEST_SUMMARY: 16/17 passed failed=['symlink-input']`; rc=1 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **killed** |
| M05 | unpinned-input-check, L969 | `SELFTEST_SUMMARY: 16/17 passed failed=['unpinned-entry']`; rc=1 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **killed** |
| M06 | key-ignores-class, L1034 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M07 | key-ignores-rule, L1034 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M08 | key-ignores-line, L1034 | `SELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']`; rc=1 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **killed** |
| M09 | key-ignores-file, L1034 | `SELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']`; rc=1 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **killed** |
| M10 | got-multiset-deduplicated, L1036 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M11 | expected-multiset-deduplicated, L1037 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M12 | known-misses-check, L1040 | `SELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']`; rc=1 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **killed** |
| M13 | label-compare, L1048-1049 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M14 | exit-compare, L1048-1049 | `SELFTEST_SUMMARY: 17/17 passed failed=[]`; rc=0 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **survived** |
| M15 | missing-findings-check, L1038 | `SELFTEST_SUMMARY: 16/17 passed failed=['verdict-missing-finding']`; rc=1 | `MADO_TRIPWIRE_FROZEN: frozen_match`; rc=0 | **killed** |

### Reading the kills precisely

- M03 accepts the unlisted-input fixture and is a direct negative-case kill.
- M04 still refuses the symlink during scan but gives `frozen_error` rather than `snapshot_tampered`; M05 still errors on the missing sha but gives `frozen_error` rather than `unpinned_legacy`. Both are **outcome-label kills**, not proof that the mutants execute or accept unsafe input.
- M08/M09 are killed by the known-miss fixture because the key is also used by the known-miss file/line comparison. This is real mutant bite, but does not demonstrate an independent wrong-file/wrong-line verdict fixture.
- M12 and M15 are direct known-miss and missing-finding kills.
- M01 survives because the second digest comparison still rejects static digest corruption. M02 survives because the supplied inputs are stable between the two reads. Do not interpret either as an observed accepted tampered snapshot.
- M06/M07 expose absent class-only/rule-only mismatch isolation; M10/M11 expose absent duplicate-key multiplicity isolation.
- M13/M14 both survive: `verdict-exit-label/expected.json:2,17` deliberately makes **both** expected exit and expected label wrong. Either unchanged predicate alone continues to reject that fixture, hiding the loss of the other.

## Exact mutations, targeted detector, and actual output

Line numbers are relative to the pinned source before mutation. Multiline expressions below are whitespace-normalized for readability; their one logical replacement is stated in full.

### M01 — snapshot-digest-compare: survived

- Expected detector: A mismatched pin must be snapshot_tampered/2; per-input ok must remain false.
- Original L980-981: `report[idx]["ok"] = (hashlib.sha256(data).hexdigest() == e["sha256"].strip().lower())`
- Mutant: `report[idx]["ok"] = True`
- Mutated SHA-256: `791605d719e7477c3e9f50985d0b43a0092b25605d02bcc7700baea5e2358b57`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 791605d719e7477c3e9f50985d0b43a0092b25605d02bcc7700baea5e2358b57
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M02 — scan-redigest-compare: survived

- Expected detector: A byte change between snapshot validation and scan must be snapshot_tampered/2.
- Original L1022: `if entry["sha256"] != e["sha256"].strip().lower():`
- Mutant: `if False:`
- Mutated SHA-256: `3b8fc218b01f106c7a209866ae448b46306eea603614eb559a71eb2a7bc6fa12`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 3b8fc218b01f106c7a209866ae448b46306eea603614eb559a71eb2a7bc6fa12
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M03 — unlisted-input-check: killed

- Expected detector: extra-unlisted-input must be snapshot_tampered/2.
- Original L965: `if rel not in listed:`
- Mutant: `if False:`
- Mutated SHA-256: `0cd36334e4fe5ce824ef4e09f305d3c04a37a0edd7af7ce11bf56c47db115d51`
- `--selftest` rc=1; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 0cd36334e4fe5ce824ef4e09f305d3c04a37a0edd7af7ce11bf56c47db115d51
SELFTEST_SUMMARY: 16/17 passed failed=['extra-unlisted-input']
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M04 — snapshot-symlink-check: killed

- Expected detector: symlink-input must be snapshot_tampered/2, not merely any exit 2.
- Original L946: `st = os.lstat(os.path.join(directory, rel))`
- Mutant: `st = os.stat(os.path.join(directory, rel))`
- Mutated SHA-256: `8646dc3bf14ea1a856749b30f625a608d7fa094d2190685a27e0a27c5dfdcaf4`
- `--selftest` rc=1; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered') got=(2, 'MADO_TRIPWIRE_FROZEN: frozen_error')
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 8646dc3bf14ea1a856749b30f625a608d7fa094d2190685a27e0a27c5dfdcaf4
SELFTEST_SUMMARY: 16/17 passed failed=['symlink-input']
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M05 — unpinned-input-check: killed

- Expected detector: unpinned-entry must be unpinned_legacy/2.
- Original L969: `unpinned = any("sha256" not in e for e in entries)`
- Mutant: `unpinned = False`
- Mutated SHA-256: `c25b4fa44ddb1fef332c88ff7c2d908123c5fd25b70a07c3da1779b2bb512fdc`
- `--selftest` rc=1; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: unpinned_legacy') got=(2, 'MADO_TRIPWIRE_FROZEN: frozen_error')
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: c25b4fa44ddb1fef332c88ff7c2d908123c5fd25b70a07c3da1779b2bb512fdc
SELFTEST_SUMMARY: 16/17 passed failed=['unpinned-entry']
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M06 — key-ignores-class: survived

- Expected detector: A class-only expected-finding mismatch must be frozen_verdict_mismatch/1.
- Original L1034: `return (f["file"], f["line"], f["class"], f["rule"])`
- Mutant: `return (f["file"], f["line"], "", f["rule"])`
- Mutated SHA-256: `e2eb46d1554cf3fe0c218c8f8a1f39a514065309883355b903d9d6b44b96dbd9`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: e2eb46d1554cf3fe0c218c8f8a1f39a514065309883355b903d9d6b44b96dbd9
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M07 — key-ignores-rule: survived

- Expected detector: A rule-only expected-finding mismatch must be frozen_verdict_mismatch/1.
- Original L1034: `return (f["file"], f["line"], f["class"], f["rule"])`
- Mutant: `return (f["file"], f["line"], f["class"], "")`
- Mutated SHA-256: `35c8d01353f64a86f1ef66687b1bafae09af50cdcc8890cbe6341eb1d13b9bbe`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 35c8d01353f64a86f1ef66687b1bafae09af50cdcc8890cbe6341eb1d13b9bbe
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M08 — key-ignores-line: killed

- Expected detector: Line attribution must affect finding identity and known-miss enforcement.
- Original L1034: `return (f["file"], f["line"], f["class"], f["rule"])`
- Mutant: `return (f["file"], 0, f["class"], f["rule"])`
- Mutated SHA-256: `7f2f535418f693d9a3ae032c5e18d5dc8aa99b3d110226f37366d31ce17820c2`
- `--selftest` rc=1; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 7f2f535418f693d9a3ae032c5e18d5dc8aa99b3d110226f37366d31ce17820c2
SELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M09 — key-ignores-file: killed

- Expected detector: File attribution must affect finding identity and known-miss enforcement.
- Original L1034: `return (f["file"], f["line"], f["class"], f["rule"])`
- Mutant: `return ("", f["line"], f["class"], f["rule"])`
- Mutated SHA-256: `54fc3dfb6b49f596c6d1041f8cc84a7247c2f48263de87e08d61ba270e554188`
- `--selftest` rc=1; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 54fc3dfb6b49f596c6d1041f8cc84a7247c2f48263de87e08d61ba270e554188
SELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M10 — got-multiset-deduplicated: survived

- Expected detector: An extra occurrence of an identical finding key must be frozen_verdict_mismatch/1.
- Original L1036: `got = Counter(key(f) for f in findings)`
- Mutant: `got = Counter(set(key(f) for f in findings))`
- Mutated SHA-256: `2ce6394ce21a463eb12a86431ba60d71361a58d0318526e40ddf95d3ffea4aba`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 2ce6394ce21a463eb12a86431ba60d71361a58d0318526e40ddf95d3ffea4aba
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M11 — expected-multiset-deduplicated: survived

- Expected detector: A missing occurrence of an identical pinned finding key must be frozen_verdict_mismatch/1.
- Original L1037: `expected = Counter(key(w) for w in pinned["findings"])`
- Mutant: `expected = Counter(set(key(w) for w in pinned["findings"]))`
- Mutated SHA-256: `2560b74be0f1e6eccd936bd445c02ae7d8a5472ad454eb8a5710502006d7bb54`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 2560b74be0f1e6eccd936bd445c02ae7d8a5472ad454eb8a5710502006d7bb54
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M12 — known-misses-check: killed

- Expected detector: known-miss-violated must be frozen_verdict_mismatch/1 even when expected findings otherwise match.
- Original L1040: `for miss in pinned["known"]:`
- Mutant: `for miss in []:`
- Mutated SHA-256: `adf35871736156e8cb24beaadf8eca2038ec0232253fb7fe40f8e38a6deba32c`
- `--selftest` rc=1; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: adf35871736156e8cb24beaadf8eca2038ec0232253fb7fe40f8e38a6deba32c
SELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M13 — label-compare: survived

- Expected detector: A label-only pinned-verdict mismatch must be frozen_verdict_mismatch/1.
- Original L1048-1049: `mismatch = (scan_exit != pinned["exit"] or scan_label != pinned["label"] or bool(missing) or bool(extra))`
- Mutant: `mismatch = (scan_exit != pinned["exit"] or bool(missing) or bool(extra))`
- Mutated SHA-256: `af66f07a3ec52c191a5ab07a061ababac17f449116a55647c6b5f477352dcb0f`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: af66f07a3ec52c191a5ab07a061ababac17f449116a55647c6b5f477352dcb0f
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M14 — exit-compare: survived

- Expected detector: An exit-only pinned-verdict mismatch must be frozen_verdict_mismatch/1.
- Original L1048-1049: `mismatch = (scan_exit != pinned["exit"] or scan_label != pinned["label"] or bool(missing) or bool(extra))`
- Mutant: `mismatch = (scan_label != pinned["label"] or bool(missing) or bool(extra))`
- Mutated SHA-256: `74e96cdebe210830df9478ecbc4bc54c69c4b19a60f0f9a0073c17e359a95d9b`
- `--selftest` rc=0; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 74e96cdebe210830df9478ecbc4bc54c69c4b19a60f0f9a0073c17e359a95d9b
SELFTEST_SUMMARY: 17/17 passed failed=[]
MADO_TRIPWIRE_FROZEN: frozen_match
```

### M15 — missing-findings-check: killed

- Expected detector: verdict-missing-finding must be frozen_verdict_mismatch/1.
- Original L1038: `missing = expected - got`
- Mutant: `missing = Counter()`
- Mutated SHA-256: `35dba3e045281f204b9064e7b7bf4083a0f7b81d69445792a0ad313eac557937`
- `--selftest` rc=1; `--frozen` rc=0; stderr empty for both.

```text
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')
CASE verdict-extra-finding ok
CASE known-miss-violated ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE path-traversal ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE absolute-input ok
CASE verdict-exit-label ok
SELFTEST_SCRIPT_SHA256: 35dba3e045281f204b9064e7b7bf4083a0f7b81d69445792a0ad313eac557937
SELFTEST_SUMMARY: 16/17 passed failed=['verdict-missing-finding']
MADO_TRIPWIRE_FROZEN: frozen_match
```

## Fixture proposal per survivor

These are proposed detector additions, **not implemented or exercised in this assignment**. Expected kill behavior below is [INFERENCE] from the executed mutation and inspected code. No survivor is permission to weaken the frozen contract.

### M01: `tampered-input-byte-payload`

Extend the existing tampered-input-byte assertion to parse the JSON payload and require inputs[0].ok == false. The pristine code marks a digest-mismatched input false; this mutant marks it true and relies on the second digest check to reject it later. Expected: snapshot_tampered/2 plus a false per-input ok. This is a report-integrity/branch-coverage gap, not evidence that stable tampered input is accepted.

### M02: `snapshot-scan-digest-drift`

Add a deterministic Python in-process fixture using an isolated temporary snapshot. Wrap frozen_snapshot so it calls the real function, then changes a pinned input to different, valid, still-clean JSONL bytes before returning the original successful snapshot result. Invoke run_frozen. Pristine must produce snapshot_tampered/2 with "snapshot changed during scan"; bypassing the re-digest guard would reproduce the unchanged clean verdict and return frozen_match/0. No race timing, host command, or real transcript is needed.

### M06: `verdict-class-only`

Copy match-findings with correctly pinned bytes, exit 1, label findings, and all finding tuples except change only the expected sudo finding class from host_mutation to live_probe. Keep file, line and rule unchanged. Pristine should report one missing plus one extra and frozen_verdict_mismatch/1; the class-erasing key should return frozen_match/0.

### M07: `verdict-rule-only`

Copy match-findings with correctly pinned bytes, exit 1 and label findings. Change only the expected sudo finding rule to a different string (for example sudo:wrong); keep its class, file and line unchanged and leave the other expected finding intact. Pristine should return frozen_verdict_mismatch/1; the rule-erasing key should return frozen_match/0.

### M10: `verdict-extra-identical-key`

Create one synthetic assistant message on one JSONL line containing two separate bash toolCall items, each with command text pacman -Q test and different tool-call IDs. This is inert transcript data, never executed. Both findings have the same file/line/class/rule key because scan_file deduplicates only within each toolCall. Pin one occurrence, exit 1, label findings. Pristine should report one extra occurrence and mismatch/1; the observed-set mutant would collapse two to one and match/0.

### M11: `verdict-missing-identical-key`

Create one synthetic assistant message with one bash toolCall carrying inert command text pacman -Q test. Pin the same expected file/line/class/rule twice, exit 1, label findings. Pristine should report one missing occurrence and mismatch/1; the expected-set mutant would collapse the two expected rows to one and match/0.

### M13: `verdict-label-only`

Split the existing verdict-exit-label case: keep the real and expected findings equal and expected_exit = 1 (the correct value), but expected_label = clean (wrong; actual is findings). Pristine should mismatch/1 solely on label; the label-comparison mutant would match/0.

### M14: `verdict-exit-only`

Add the complementary split case: keep findings equal and expected_label = findings (correct), but expected_exit = 0 (wrong; actual is 1). Pristine should mismatch/1 solely on exit; the exit-comparison mutant would match/0.

## Restoration and fixture identity

Before every mutation and after every restoration, every copy had SHA-256 `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` and all 48852 bytes exactly equaled the `git show abfbf35b1ed4d4a1eb294d525ef286be30f3886f:tools/mado-tripwire.py` byte string. The after-restoration comparisons were byte equality, not only digest equality.

| Copy | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | Exact restored bytes |
|---|---|---|---|---|
| M01 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `791605d719e7477c3e9f50985d0b43a0092b25605d02bcc7700baea5e2358b57` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M02 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `3b8fc218b01f106c7a209866ae448b46306eea603614eb559a71eb2a7bc6fa12` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M03 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `0cd36334e4fe5ce824ef4e09f305d3c04a37a0edd7af7ce11bf56c47db115d51` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M04 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `8646dc3bf14ea1a856749b30f625a608d7fa094d2190685a27e0a27c5dfdcaf4` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M05 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `c25b4fa44ddb1fef332c88ff7c2d908123c5fd25b70a07c3da1779b2bb512fdc` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M06 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `e2eb46d1554cf3fe0c218c8f8a1f39a514065309883355b903d9d6b44b96dbd9` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M07 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `35c8d01353f64a86f1ef66687b1bafae09af50cdcc8890cbe6341eb1d13b9bbe` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M08 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `7f2f535418f693d9a3ae032c5e18d5dc8aa99b3d110226f37366d31ce17820c2` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M09 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `54fc3dfb6b49f596c6d1041f8cc84a7247c2f48263de87e08d61ba270e554188` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M10 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `2ce6394ce21a463eb12a86431ba60d71361a58d0318526e40ddf95d3ffea4aba` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M11 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `2560b74be0f1e6eccd936bd445c02ae7d8a5472ad454eb8a5710502006d7bb54` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M12 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `adf35871736156e8cb24beaadf8eca2038ec0232253fb7fe40f8e38a6deba32c` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M13 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `af66f07a3ec52c191a5ab07a061ababac17f449116a55647c6b5f477352dcb0f` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M14 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `74e96cdebe210830df9478ecbc4bc54c69c4b19a60f0f9a0073c17e359a95d9b` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |
| M15 | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | `35dba3e045281f204b9064e7b7bf4083a0f7b81d69445792a0ad313eac557937` | `c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb` | True |

Detector-input tree fingerprints before and after were equal. Fingerprint definition: sorted JSON records for every regular-file path, byte count and SHA-256, plus every symlink path/target, serialized with sorted keys and compact separators, then SHA-256. No source or fixture restoration was necessary in the lane, because none was edited.

| Input tree | Before / after tree SHA-256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen` | `21f8bc6ef1055062e3071bb820771aa46973daa5b890be3a1fa2fefaede73138` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen` | `bedba68228911124916322259ed776a148629c7a25162aed747d477896ce260a` |

## Raw detector receipts

Full argv, exit status, stdout, stderr, and measured duration for all 90 outer commands follow. Baseline and restoration are recorded per copy rather than inferred from a single shared run. These embedded receipts are the durable evidence; scratch JSON files need not survive.

```json
{
  "revision": "abfbf35b1ed4d4a1eb294d525ef286be30f3886f",
  "pristine_tool_sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
  "baseline": {
    "M01": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M01/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.526002,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M01/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.042417,
          "mode": "--frozen"
        }
      ]
    },
    "M02": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M02/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.541786,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M02/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.037818,
          "mode": "--frozen"
        }
      ]
    },
    "M03": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M03/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.524549,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M03/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.036726,
          "mode": "--frozen"
        }
      ]
    },
    "M04": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M04/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.537219,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M04/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.035929,
          "mode": "--frozen"
        }
      ]
    },
    "M05": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M05/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.570068,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M05/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.043066,
          "mode": "--frozen"
        }
      ]
    },
    "M06": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M06/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.556936,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M06/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.036271,
          "mode": "--frozen"
        }
      ]
    },
    "M07": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M07/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.54606,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M07/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.041367,
          "mode": "--frozen"
        }
      ]
    },
    "M08": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M08/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.547862,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M08/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.036508,
          "mode": "--frozen"
        }
      ]
    },
    "M09": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M09/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.56236,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M09/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.038462,
          "mode": "--frozen"
        }
      ]
    },
    "M10": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M10/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.554949,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M10/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.036618,
          "mode": "--frozen"
        }
      ]
    },
    "M11": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M11/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.564218,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M11/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.039881,
          "mode": "--frozen"
        }
      ]
    },
    "M12": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M12/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.562589,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M12/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.040268,
          "mode": "--frozen"
        }
      ]
    },
    "M13": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M13/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.544945,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M13/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.035498,
          "mode": "--frozen"
        }
      ]
    },
    "M14": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M14/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.527184,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M14/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.039978,
          "mode": "--frozen"
        }
      ]
    },
    "M15": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M15/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.522105,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M15/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.034375,
          "mode": "--frozen"
        }
      ]
    }
  },
  "mutated": {
    "M01": {
      "sha256": "791605d719e7477c3e9f50985d0b43a0092b25605d02bcc7700baea5e2358b57",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M01/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 791605d719e7477c3e9f50985d0b43a0092b25605d02bcc7700baea5e2358b57\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.482161,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M01/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"791605d719e7477c3e9f50985d0b43a0092b25605d02bcc7700baea5e2358b57\"}\n",
          "stderr": "",
          "seconds": 0.033356,
          "mode": "--frozen"
        }
      ]
    },
    "M02": {
      "sha256": "3b8fc218b01f106c7a209866ae448b46306eea603614eb559a71eb2a7bc6fa12",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M02/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 3b8fc218b01f106c7a209866ae448b46306eea603614eb559a71eb2a7bc6fa12\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.476132,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M02/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"3b8fc218b01f106c7a209866ae448b46306eea603614eb559a71eb2a7bc6fa12\"}\n",
          "stderr": "",
          "seconds": 0.033714,
          "mode": "--frozen"
        }
      ]
    },
    "M03": {
      "sha256": "0cd36334e4fe5ce824ef4e09f305d3c04a37a0edd7af7ce11bf56c47db115d51",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M03/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 1,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 0cd36334e4fe5ce824ef4e09f305d3c04a37a0edd7af7ce11bf56c47db115d51\nSELFTEST_SUMMARY: 16/17 passed failed=['extra-unlisted-input']\n",
          "stderr": "",
          "seconds": 0.482373,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M03/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"0cd36334e4fe5ce824ef4e09f305d3c04a37a0edd7af7ce11bf56c47db115d51\"}\n",
          "stderr": "",
          "seconds": 0.032274,
          "mode": "--frozen"
        }
      ]
    },
    "M04": {
      "sha256": "8646dc3bf14ea1a856749b30f625a608d7fa094d2190685a27e0a27c5dfdcaf4",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M04/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 1,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered') got=(2, 'MADO_TRIPWIRE_FROZEN: frozen_error')\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 8646dc3bf14ea1a856749b30f625a608d7fa094d2190685a27e0a27c5dfdcaf4\nSELFTEST_SUMMARY: 16/17 passed failed=['symlink-input']\n",
          "stderr": "",
          "seconds": 0.481997,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M04/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"8646dc3bf14ea1a856749b30f625a608d7fa094d2190685a27e0a27c5dfdcaf4\"}\n",
          "stderr": "",
          "seconds": 0.032732,
          "mode": "--frozen"
        }
      ]
    },
    "M05": {
      "sha256": "c25b4fa44ddb1fef332c88ff7c2d908123c5fd25b70a07c3da1779b2bb512fdc",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M05/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 1,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: unpinned_legacy') got=(2, 'MADO_TRIPWIRE_FROZEN: frozen_error')\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c25b4fa44ddb1fef332c88ff7c2d908123c5fd25b70a07c3da1779b2bb512fdc\nSELFTEST_SUMMARY: 16/17 passed failed=['unpinned-entry']\n",
          "stderr": "",
          "seconds": 0.476245,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M05/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c25b4fa44ddb1fef332c88ff7c2d908123c5fd25b70a07c3da1779b2bb512fdc\"}\n",
          "stderr": "",
          "seconds": 0.036505,
          "mode": "--frozen"
        }
      ]
    },
    "M06": {
      "sha256": "e2eb46d1554cf3fe0c218c8f8a1f39a514065309883355b903d9d6b44b96dbd9",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M06/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: e2eb46d1554cf3fe0c218c8f8a1f39a514065309883355b903d9d6b44b96dbd9\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.480841,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M06/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"e2eb46d1554cf3fe0c218c8f8a1f39a514065309883355b903d9d6b44b96dbd9\"}\n",
          "stderr": "",
          "seconds": 0.037612,
          "mode": "--frozen"
        }
      ]
    },
    "M07": {
      "sha256": "35c8d01353f64a86f1ef66687b1bafae09af50cdcc8890cbe6341eb1d13b9bbe",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M07/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 35c8d01353f64a86f1ef66687b1bafae09af50cdcc8890cbe6341eb1d13b9bbe\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.472248,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M07/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"35c8d01353f64a86f1ef66687b1bafae09af50cdcc8890cbe6341eb1d13b9bbe\"}\n",
          "stderr": "",
          "seconds": 0.034762,
          "mode": "--frozen"
        }
      ]
    },
    "M08": {
      "sha256": "7f2f535418f693d9a3ae032c5e18d5dc8aa99b3d110226f37366d31ce17820c2",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M08/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 1,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 7f2f535418f693d9a3ae032c5e18d5dc8aa99b3d110226f37366d31ce17820c2\nSELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']\n",
          "stderr": "",
          "seconds": 0.479902,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M08/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"7f2f535418f693d9a3ae032c5e18d5dc8aa99b3d110226f37366d31ce17820c2\"}\n",
          "stderr": "",
          "seconds": 0.033036,
          "mode": "--frozen"
        }
      ]
    },
    "M09": {
      "sha256": "54fc3dfb6b49f596c6d1041f8cc84a7247c2f48263de87e08d61ba270e554188",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M09/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 1,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 54fc3dfb6b49f596c6d1041f8cc84a7247c2f48263de87e08d61ba270e554188\nSELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']\n",
          "stderr": "",
          "seconds": 0.473473,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M09/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"54fc3dfb6b49f596c6d1041f8cc84a7247c2f48263de87e08d61ba270e554188\"}\n",
          "stderr": "",
          "seconds": 0.033454,
          "mode": "--frozen"
        }
      ]
    },
    "M10": {
      "sha256": "2ce6394ce21a463eb12a86431ba60d71361a58d0318526e40ddf95d3ffea4aba",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M10/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 2ce6394ce21a463eb12a86431ba60d71361a58d0318526e40ddf95d3ffea4aba\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.477895,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M10/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"2ce6394ce21a463eb12a86431ba60d71361a58d0318526e40ddf95d3ffea4aba\"}\n",
          "stderr": "",
          "seconds": 0.031655,
          "mode": "--frozen"
        }
      ]
    },
    "M11": {
      "sha256": "2560b74be0f1e6eccd936bd445c02ae7d8a5472ad454eb8a5710502006d7bb54",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M11/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 2560b74be0f1e6eccd936bd445c02ae7d8a5472ad454eb8a5710502006d7bb54\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.482849,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M11/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"2560b74be0f1e6eccd936bd445c02ae7d8a5472ad454eb8a5710502006d7bb54\"}\n",
          "stderr": "",
          "seconds": 0.031498,
          "mode": "--frozen"
        }
      ]
    },
    "M12": {
      "sha256": "adf35871736156e8cb24beaadf8eca2038ec0232253fb7fe40f8e38a6deba32c",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M12/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 1,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: adf35871736156e8cb24beaadf8eca2038ec0232253fb7fe40f8e38a6deba32c\nSELFTEST_SUMMARY: 16/17 passed failed=['known-miss-violated']\n",
          "stderr": "",
          "seconds": 0.466861,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M12/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"adf35871736156e8cb24beaadf8eca2038ec0232253fb7fe40f8e38a6deba32c\"}\n",
          "stderr": "",
          "seconds": 0.032124,
          "mode": "--frozen"
        }
      ]
    },
    "M13": {
      "sha256": "af66f07a3ec52c191a5ab07a061ababac17f449116a55647c6b5f477352dcb0f",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M13/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: af66f07a3ec52c191a5ab07a061ababac17f449116a55647c6b5f477352dcb0f\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.450443,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M13/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"af66f07a3ec52c191a5ab07a061ababac17f449116a55647c6b5f477352dcb0f\"}\n",
          "stderr": "",
          "seconds": 0.034696,
          "mode": "--frozen"
        }
      ]
    },
    "M14": {
      "sha256": "74e96cdebe210830df9478ecbc4bc54c69c4b19a60f0f9a0073c17e359a95d9b",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M14/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 74e96cdebe210830df9478ecbc4bc54c69c4b19a60f0f9a0073c17e359a95d9b\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.461945,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M14/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"74e96cdebe210830df9478ecbc4bc54c69c4b19a60f0f9a0073c17e359a95d9b\"}\n",
          "stderr": "",
          "seconds": 0.032587,
          "mode": "--frozen"
        }
      ]
    },
    "M15": {
      "sha256": "35dba3e045281f204b9064e7b7bf4083a0f7b81d69445792a0ad313eac557937",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M15/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 1,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding FAIL want=(1, 'MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch') got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match')\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: 35dba3e045281f204b9064e7b7bf4083a0f7b81d69445792a0ad313eac557937\nSELFTEST_SUMMARY: 16/17 passed failed=['verdict-missing-finding']\n",
          "stderr": "",
          "seconds": 0.462087,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M15/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"35dba3e045281f204b9064e7b7bf4083a0f7b81d69445792a0ad313eac557937\"}\n",
          "stderr": "",
          "seconds": 0.031333,
          "mode": "--frozen"
        }
      ]
    }
  },
  "restored": {
    "M01": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M01/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.468325,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M01/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.034286,
          "mode": "--frozen"
        }
      ]
    },
    "M02": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M02/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.477903,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M02/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.031042,
          "mode": "--frozen"
        }
      ]
    },
    "M03": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M03/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.464439,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M03/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.032312,
          "mode": "--frozen"
        }
      ]
    },
    "M04": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M04/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.472156,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M04/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.036166,
          "mode": "--frozen"
        }
      ]
    },
    "M05": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M05/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.470512,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M05/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.03635,
          "mode": "--frozen"
        }
      ]
    },
    "M06": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M06/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.476647,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M06/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.03498,
          "mode": "--frozen"
        }
      ]
    },
    "M07": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M07/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.468327,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M07/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.035994,
          "mode": "--frozen"
        }
      ]
    },
    "M08": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M08/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.471668,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M08/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.032189,
          "mode": "--frozen"
        }
      ]
    },
    "M09": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M09/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.48548,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M09/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.035301,
          "mode": "--frozen"
        }
      ]
    },
    "M10": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M10/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.489877,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M10/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.032921,
          "mode": "--frozen"
        }
      ]
    },
    "M11": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M11/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.488574,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M11/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.034025,
          "mode": "--frozen"
        }
      ]
    },
    "M12": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M12/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.486731,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M12/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.034748,
          "mode": "--frozen"
        }
      ]
    },
    "M13": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M13/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.480321,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M13/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.035237,
          "mode": "--frozen"
        }
      ]
    },
    "M14": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M14/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.485928,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M14/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.030931,
          "mode": "--frozen"
        }
      ]
    },
    "M15": {
      "sha256": "c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb",
      "runs": [
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M15/mado-tripwire.py",
            "--selftest",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen"
          ],
          "rc": 0,
          "stdout": "CASE match-findings ok\nCASE match-clean ok\nCASE verdict-missing-finding ok\nCASE verdict-extra-finding ok\nCASE known-miss-violated ok\nCASE tampered-input-byte ok\nCASE missing-input ok\nCASE extra-unlisted-input ok\nCASE symlink-input ok\nCASE path-traversal ok\nCASE unpinned-entry ok\nCASE malformed-expected-json ok\nCASE wrong-schema ok\nCASE match-permitted-only ok\nCASE match-permit-partial ok\nCASE absolute-input ok\nCASE verdict-exit-label ok\nSELFTEST_SCRIPT_SHA256: c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\nSELFTEST_SUMMARY: 17/17 passed failed=[]\n",
          "stderr": "",
          "seconds": 0.490587,
          "mode": "--selftest"
        },
        {
          "argv": [
            "python3",
            "-I",
            "/tmp/MadoR18-MutFrozenMode-z5sr1h7o/M15/mado-tripwire.py",
            "--frozen",
            "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen"
          ],
          "rc": 0,
          "stdout": "MADO_TRIPWIRE_FROZEN: frozen_match\n{\"exit\": 0, \"expected_sha256\": \"4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9\", \"extra_findings\": [], \"inputs\": [{\"ok\": true, \"path\": \"inputs/r15-libinput-events.jsonl\", \"sha256\": \"7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90\"}, {\"ok\": true, \"path\": \"inputs/r13-global-capture.jsonl\", \"sha256\": \"265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9\"}, {\"ok\": true, \"path\": \"inputs/r14-review-source-bar.jsonl\", \"sha256\": \"4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232\"}, {\"ok\": true, \"path\": \"inputs/r14-source-safety.jsonl\", \"sha256\": \"8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1\"}, {\"ok\": true, \"path\": \"inputs/r13-root.jsonl\", \"sha256\": \"24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11\"}], \"missing_findings\": [], \"outcome\": \"frozen_match\", \"scan_exit\": 1, \"scan_label\": \"findings\", \"schema\": \"mado-tripwire-frozen-verdict-v1\", \"tool_sha256\": \"c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb\"}\n",
          "stderr": "",
          "seconds": 0.032815,
          "mode": "--frozen"
        }
      ]
    }
  },
  "exact_bytes_restored": {
    "M01": true,
    "M02": true,
    "M03": true,
    "M04": true,
    "M05": true,
    "M06": true,
    "M07": true,
    "M08": true,
    "M09": true,
    "M10": true,
    "M11": true,
    "M12": true,
    "M13": true,
    "M14": true,
    "M15": true
  },
  "verdicts": {
    "M01": "survived",
    "M02": "survived",
    "M03": "killed",
    "M04": "killed",
    "M05": "killed",
    "M06": "survived",
    "M07": "survived",
    "M08": "killed",
    "M09": "killed",
    "M10": "survived",
    "M11": "survived",
    "M12": "killed",
    "M13": "survived",
    "M14": "survived",
    "M15": "killed"
  },
  "fixture_tree_sha256_before": {
    "selftest": "21f8bc6ef1055062e3071bb820771aa46973daa5b890be3a1fa2fefaede73138",
    "frozen": "bedba68228911124916322259ed776a148629c7a25162aed747d477896ce260a"
  },
  "fixture_tree_sha256_after": {
    "selftest": "21f8bc6ef1055062e3071bb820771aa46973daa5b890be3a1fa2fefaede73138",
    "frozen": "bedba68228911124916322259ed776a148629c7a25162aed747d477896ce260a"
  }
}
```
