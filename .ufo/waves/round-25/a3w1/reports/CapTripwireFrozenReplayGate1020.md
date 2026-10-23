# CapTripwireFrozenReplayGate1020 — C2 row re-run at base `41cc04c8`

Seat: `MadoR25A3.CapTripwireFrozenReplayGate1020` (leaf, no spawns, no model parameter).
Row: `SCORECARD.md:1020`, section `### Capabilities (round 18)` (`SCORECARD.md:1016`), first-working round 18.
Base: `41cc04c8d593837a0d5078bffaacdaa163d12897`, read from the lane via `git show 41cc04c8:SCORECARD.md`
(1618 lines, sha256 `6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08`).
Nothing was run in the lane. No package installed or upgraded; no host file, service or compositor state touched.

## What was run

Sandbox clone (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE unset for the whole call):

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
(unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; \
 timeout 600 git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin \
   /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireFrozenReplayGate1020 && \
 git -C /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireFrozenReplayGate1020 checkout -q --detach 41cc04c8)
# -> 41cc04c8d593837a0d5078bffaacdaa163d12897
```

Tool under test in the clone: `tools/mado-tripwire.py`,
sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` (the round-23 restored classifier; not the
round-18 receipt's `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`).

Row's demonstration command, run from the clone root, then the row's selftest:

```
(unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; \
 timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen)
(unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; \
 timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen)
```

Supplementary (not in the row, used only to separate "replay broken" from "pin stale"):

```
cp -a <clone>/.ufo/waves/round-18/frozen /fast/scratch/hyaku/mado-r25a3/c2/tamper   # then XOR byte 0 of inputs/r13-root.jsonl
... python3 -I tools/mado-tripwire.py --frozen /fast/scratch/hyaku/mado-r25a3/c2/tamper
... python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-19/frozen
```

## Ledger line

| SCORECARD.md:1020 | tripwire frozen replay (gate entry) | Verify input digests, then compare the tripwire's verdict against a pinned expected verdict (0/1/2 codes) | works, exit 1: `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch` — all 5 input digests ok, missing_findings 0, 3 extra `package_query/pacman:-Q` that the r18 pin predates; selftest 31/31 exit 0; one-byte tamper copy exit 2 `snapshot_tampered`; round-19 baseline `frozen_match` exit 0 | `timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` | SCORECARD.md:1580 (round-24 status table, which supersedes the implied works of every earlier row); also SCORECARD.md:1134, 1191, 1330, 1391, 1458 |

## Verbatim output — `--frozen .ufo/waves/round-18/frozen` (3 lines, 1381 B)

```
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch
{"exit": 1, "expected_sha256": "4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9", "extra_findings": [{"class": "package_query", "file": "inputs/r13-root.jsonl", "line": 4, "rule": "pacman:-Q"}, {"class": "package_query", "file": "inputs/r14-source-safety.jsonl", "line": 2, "rule": "pacman:-Q"}, {"class": "package_query", "file": "inputs/r14-source-safety.jsonl", "line": 3, "rule": "pacman:-Q"}], "inputs": [{"ok": true, "path": "inputs/r15-libinput-events.jsonl", "sha256": "7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90"}, {"ok": true, "path": "inputs/r13-global-capture.jsonl", "sha256": "265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9"}, {"ok": true, "path": "inputs/r14-review-source-bar.jsonl", "sha256": "4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232"}, {"ok": true, "path": "inputs/r14-source-safety.jsonl", "sha256": "8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1"}, {"ok": true, "path": "inputs/r13-root.jsonl", "sha256": "24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11"}], "missing_findings": [], "outcome": "frozen_verdict_mismatch", "scan_exit": 1, "scan_label": "findings", "schema": "mado-tripwire-frozen-verdict-v1", "tool_sha256": "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84"}
exit=1
```

## Verbatim output — `--selftest .ufo/waves/round-18/tripwire/frozen` (34 lines, 979 B)

```
CASE match-findings ok
CASE match-clean ok
CASE verdict-missing-finding ok
CASE verdict-extra-finding ok
CASE verdict-exit-label ok
CASE known-miss-violated ok
CASE swapped-missing-extra ok
CASE tampered-input-byte ok
CASE missing-input ok
CASE extra-unlisted-input ok
CASE symlink-input ok
CASE symlinked-inputs-dir ok
CASE path-traversal ok
CASE absolute-input ok
CASE unreachable-line ok
CASE contradictory-exit-label ok
CASE label-clean-with-findings ok
CASE unknown-class ok
CASE known-miss-blank ok
CASE known-miss-unreachable ok
CASE expected-unlisted-file ok
CASE duplicate-input-path ok
CASE unpinned-entry ok
CASE malformed-expected-json ok
CASE wrong-schema ok
CASE match-permitted-only ok
CASE match-permit-partial ok
CASE unknown-key ok
CASE duplicate-json-key ok
CASE symlinked-frozen-dir ok
CASE symlinked-frozen-dir-target ok
SELFTEST_SCRIPT_SHA256: cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
SELFTEST_SUMMARY: 31/31 passed failed=[]
exit=0
```

## Verbatim output — tampered copy of the same snapshot (one byte flipped)

```
MADO_TRIPWIRE_FROZEN: snapshot_tampered
{"error": "snapshot does not match its pin", "exit": 2, "expected_sha256": "4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9", "extra_findings": [], "inputs": [{"ok": true, "path": "inputs/r15-libinput-events.jsonl", "sha256": "7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90"}, {"ok": true, "path": "inputs/r13-global-capture.jsonl", "sha256": "265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9"}, {"ok": true, "path": "inputs/r14-review-source-bar.jsonl", "sha256": "4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232"}, {"ok": true, "path": "inputs/r14-source-safety.jsonl", "sha256": "8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1"}, {"ok": false, "path": "inputs/r13-root.jsonl", "sha256": "24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11"}], "missing_findings": [], "outcome": "snapshot_tampered", "scan_exit": null, "scan_label": null, "schema": "mado-tripwire-frozen-verdict-v1", "tool_sha256": "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84"}
exit=2
```

## Verbatim output — round-19 baseline `--frozen .ufo/waves/round-19/frozen`

```
MADO_TRIPWIRE_FROZEN: frozen_match
{"exit": 0, "expected_sha256": "50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435", "extra_findings": [], "inputs": [{"ok": true, "path": "inputs/r15-libinput-events.jsonl", "sha256": "7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90"}, {"ok": true, "path": "inputs/r13-global-capture.jsonl", "sha256": "265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9"}, {"ok": true, "path": "inputs/r14-review-source-bar.jsonl", "sha256": "4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232"}, {"ok": true, "path": "inputs/r14-source-safety.jsonl", "sha256": "8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1"}, {"ok": true, "path": "inputs/r13-root.jsonl", "sha256": "24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11"}], "missing_findings": [], "outcome": "frozen_match", "scan_exit": 1, "scan_label": "findings", "schema": "mado-tripwire-frozen-verdict-v1", "tool_sha256": "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84"}
exit=0
```

## Supersession sweep over the whole SCORECARD.md at 41cc04c8

Searched all 1618 lines for `frozen`, `frozen_match`, `frozen_verdict_mismatch`, `snapshot_tampered`, `tripwire`,
and read every hit in context. Later text that bears on row 1020:

- `:1134` (round-19 committed results, C3): "Round-18 frozen baseline now reads `frozen_verdict_mismatch` (the change
  made visible); round-19 baseline `.ufo/waves/round-19/frozen` `frozen_match` (`50d2a45e…`)". This is the registered
  design: the r18 pin was deliberately left to go red when round 19 added the three `package_query/pacman:-Q` findings.
  Round-19 declared claims `:1085-1090` state the r18 `expected.json` `(file, line)` pairs as an *input population* of a
  different counter (`tw-recall.py`), not as a live gate.
- `:1110-1111` (round-19 declared claim C3): "re-pin a round-19 frozen baseline at the landed classifier (the round-18
  baseline must then read `frozen_verdict_mismatch`, which is the change made visible)" — the red is a required outcome,
  not a regression.
- `:1191` (round-19 final state): "frozen r19 `frozen_match`, r18 `frozen_verdict_mismatch`".
- `:1330` (round-20 C1 guards): "`--frozen round-19` `frozen_match`, `--frozen round-18` `frozen_verdict_mismatch`
  (unchanged expected red)".
- `:1391` (round-20 attempt 2 guards): "`--frozen round-19` `frozen_match`, round-18 baseline mismatch unchanged".
- `:1458` (round-21 legacy screens): "r19 frozen_match; r18 expected old frozen_verdict_mismatch".
- `:1566-1572` + `:1580` (round-24 `### Capability status (round 24 re-demonstration)`): the table preamble says "This
  table supersedes the implied `works` of every earlier row; the earlier rows stay as written", and its row reads
  `| tripwire frozen replay (gate entry) | works | MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch, exit 1 — the replay
  runs and reports; the mismatch is the frozen verdict, not a replay failure |`. That is the same observation this
  re-run produced at 41cc04c8, with the same nuance.
- `:1598-1607` (round-24 results) records C2 calibration 1/12 → 0/12 over the 12 heading-scoped rows, with no change to
  this row's status.

No later row retires the capability, drops `--frozen`, or claims a green r18 baseline. No contradiction found.

## Notes, risks, blockers

- **Row evidence pointer resolves only wave-relative.** `evidence/final/tripwire-frozen-*.txt` does not exist at the
  repo root at 41cc04c8 (`ls` → "No such file or directory"). The referenced receipts are
  `.ufo/waves/round-18/evidence/final/tripwire-frozen-match.txt`, `...-tampered.txt`, `...-selftest.txt`, each headed
  `RECEIPT tool=tools/mado-tripwire.py tool_sha256=c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd
  measured_commit=be886a3cd05cf27d47a976c69df2f5f556759c08`. So the acquisition evidence is preserved but is pinned to
  the round-18 tool, not to base bytes.
- **What "works" means here.** The capability sentence is the digest-verify + verdict-compare function with the
  0/1/2 outcome table, and all four outcomes reproduce at base: digests verify (5/5 `ok`, `expected_sha256`
  `4f3534ae…`), a stale pin reports `frozen_verdict_mismatch` exit 1, a one-byte tamper reports `snapshot_tampered`
  exit 2, and a current pin reports `frozen_match` exit 0 (round-19 baseline). The r18 *pin* is stale by design, so the
  literal exit code of the row's command is 1, not the 0 of the round-18 acquisition receipt. A closure reading "works"
  as "the row's command exits 0" would score this row `fails`; the round-24 table already records the narrower reading.
- **The mismatch is a classifier delta, not replay drift.** `extra_findings` are exactly the three
  `package_query/pacman:-Q` rows round-19's C3 targeted, and `missing_findings` is empty, so no earlier finding was
  lost at base bytes.
- **Risk to flag for the round-25 C2 population.** The row's demonstration command, as written, cannot yield exit 0 at
  any commit after round 19, because the pinned expected verdict lives inside the wave directory it names. A future C2
  counter that treats "exit 0" as the works predicate will mark this row stale every round. Suggested (not done here):
  point the row at `.ufo/waves/round-19/frozen` or state the expected exit code explicitly.
- **Blockers:** none. No counter was run (C2 is exploratory, no counter), no installs, no lane writes beyond this report.
- **Cleanup:** the clone and the tamper copy were deleted (`rm -rf /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireFrozenReplayGate1020
  /fast/scratch/hyaku/mado-r25a3/c2/tamper`). Raw captures kept as secondary copies at
  `/fast/scratch/hyaku/mado-r25a3/c2/{frozen-r18,frozen-r19,tamper-r18,selftest-r18-frozen}.txt`; every byte is
  reproduced verbatim above, so the report is self-contained.

## Verdict

Row `SCORECARD.md:1020` (`tripwire frozen replay (gate entry)`): **works** at 41cc04c8 in the row's own 0/1/2 sense —
exit 1 `frozen_verdict_mismatch` on the round-18 pin with digests intact, exit 2 on a tampered copy, exit 0 on the
round-19 pin, selftest 31/31 — and the stale r18 pin is already recorded as the intended red at `SCORECARD.md:1134`
and `:1580`. No capability regression observed at base bytes.
