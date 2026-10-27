# MutRoutedR3 — w2 falsification of the R3 synthetic-material marker gate (round 48)

Seat: `MutRoutedR3` (leaf; no subagents). Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; freeze commit
`3e6c848a` (read-only). Attack target: the marker-gate patch proposed for R3, delivered by
`.ufo/waves/round-48/w1/ExecSessionMarker/` (gate v2 `check-session-material.py` sha256
`82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f`, registry `session-material-waivers.txt`
`4d007fe8124523a1a8e2a021a182d5c65f0e99f74d3c69c7d3272289be12604e`, 48 rows, 48 sidecars, `install.sh`,
`verify-install.sh`). The patch exists, so the assigned probe ran in full. All evidence in
`receipts/` (this seat dir); the private replay tree lived under `/fast/scratch/hyaku/mado-r48/MutRoutedR3/`
and is deleted. No lane file outside this seat's evidence+report was created, edited or committed; no lane
git/jj state was touched (clone was `--shared`, commits used a scratch identity inside the clone only).

## 1. Detector and replay

Detector (bounded, identical at every state):
`python3 -I <tree>/quality/check-session-material.py --repo <clone> --rev HEAD [--no-waivers]`, rc 0/1/2 recorded.
Replay: `git clone --shared --no-checkout` of the lane, HEAD detached to base by plumbing
(`update-ref --no-deref` + `read-tree`; the gate reads the object DB, so no >1 MiB worktree checkout),
`install.sh` applied, committed; then one scratch commit per probe, each mutation followed by an exact-byte
restore commit (hash-proven) and a restored-state detector run. Drivers: `receipts/driver1.sh`,
`receipts/runner.sh`, `receipts/prep-gatecopy.sh`; commit list `receipts/out/commits.txt`; all raw gate outputs
`receipts/out/D*.txt`; timings `receipts/out/rcs.txt`.

## 2. Pristine reproductions (marked / unmarked / base)

| run | state | observed | rc | matches w1 receipt |
|---|---|---|---|---|
| D00 | gate v2 `--selftest` | `SELFTEST: passed=69/69 failed=0` | 0 | `receipts/00-selftest.txt` |
| D01 | base, tracked old gate | `files=19969 findings=128` (R1=33 R2=36 R3=57 R4=2) | 1 | `01-old-gate-at-base.txt` |
| D02 | install rev (marked) | `SESSION_MATERIAL_WAIVED: findings=49 files=47`; `files=20017 findings=100` (R1=33 R2=34 R3=10 R4=2 R5=21); CritW2Gate pair refused `rule-not-listed` | 1 | `11-verify-install.txt` |
| D03 | install rev `--no-waivers` | `findings=149` — the 49-finding drop is the marker layer alone | 1 | `05-no-waivers.txt` |
| PRE | + gate-copy target committed (`82c9053a…`) | `WAIVED findings=52 files=48`; `files=20018 findings=100`; 3 gate-copy WAIVERs (R1,R2,R3) | 1 | `12-as-landed.txt` (file-count differs only because this replay carries just the one target file) |

## 3. Planted-real and marker controls (one commit each, then restored)

Bytes planted: synthetic client dump `{"class": "org.example.fake", "title": "redacted"}` and planted-real
`{"title": "Example Domain"}` (IANA reserved; the F1 control value, no host value involved).

| probe | plant | observed | rc | verdict |
|---|---|---|---|---|
| P-b (D04) | synthetic dump, no marker, `.ufo/waves/round-48/w2/MutRoutedR3-fx/unmarked-clients.json` | `FINDING … rule=R1_CLIENT_DUMP count=1`; findings 100→101 | 1 | unmarked is counted — correct |
| P-a (D05) | same bytes + sidecar + registry row | `WAIVER file=…unmarked-clients.json rule=R1_CLIENT_DUMP kind=fixture`; `WAIVED findings=50 files=48`; findings back to 100 | 1 | marked synthetic is waived — correct |
| P-c (D06) | planted-real + well-formed marker pair at `.ufo/reports/session-clients.json` | `WAIVER_REJECTED … reason=path-outside-waves` + `FINDING … count=1`; findings=101 | 1 | forged marker outside `.ufo/waves/` fails closed — correct |
| P-c′ (D07) | planted-real + marker pair under waves (`forged-real.json`) | `WAIVER_REJECTED … reason=value-not-synthetic:title-not-synthetic` + `FINDING`; findings=102 | 1 | W4b refuses a real-shaped title under a forged fixture marker — correct; re-proves the F1 boundary at this revision |

## 4. Registry / sidecar mutations — expected reason, observed output, verdict

Every mutant: one committed byte-level change, detector run, exact restore, restored detector run.
Pristine anchors: registry `4d007fe8…`, C00 sidecar `33dc7993b8b0e00824f41ab6e1b258628f6d32def1da50c0829ff71d8d313e2a`,
gate bytes `82c9053a…`. Hash triplets per mutant in `receipts/mut-M*.{before,during,after}`;
M4/M7/M8 `.before` was captured after staging (tooling order), so the pristine anchor above is the seat source
byte-hash; every `.after` equals its anchor, i.e. every restore is byte-exact.

| mut | change | expected | observed (mutated run) | findings | restored run | verdict |
|---|---|---|---|---|---|---|
| M1 | registry row sha: `…03ddd88d`→`…03ddd88e` (C00_shipped) | `registry-sha-mismatch` | `WAIVER_REJECTED file=…C00_shipped/mons.json rule=R3_MONITOR_IDENT reason=registry-sha-mismatch` + FINDING `count=1 detail=objects=1 keys=serial+ident` | 101 | 100, waiver honoured | **killed** |
| M2 | registry row deleted (C00_shipped) | `unregistered` | `WAIVER_REJECTED … reason=unregistered` + FINDING | 101 | 100 | **killed** |
| M3 | registry kind `fixture`→`gate-copy` (C00_shipped) | `registry-kind-mismatch` | `WAIVER_REJECTED … reason=registry-kind-mismatch` + FINDING | 101 | 100 | **killed** |
| M4 | sidecar sha last char flipped (C00_shipped) | `sha-mismatch` | `WAIVER_REJECTED … reason=sha-mismatch` + FINDING | 101 | 100 | **killed** |
| M7 | sidecar grammar broken (`v1` dropped) | `marker-malformed` | `WAIVER_REJECTED … reason=marker-malformed` + FINDING | 101 | 100 | **killed** |
| M5 | sidecar file deleted (C00_shipped) | plain finding, no waiver line | `FINDING …C00_shipped/mons.json rule=R3_MONITOR_IDENT count=1` (no WAIVER/WAIVER_REJECTED line; files 20017→20016) | 101 | 100 | **killed** |
| M6 | gate-copy target bytes changed (one appended line at `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py`) | fail-closed | `WAIVER_REJECTED ×3 rule=R1/R2/R3 reason=sha-mismatch` + 3 FINDINGs (R1 count=4, R2 count=3, R3 count=1) | 103 | 100, `WAIVED findings=52 files=48`, target hash `82c9053a…` | **killed** |
| M8 | gate source changed (one appended line at `quality/check-session-material.py`), marker pair self-consistent | `gate-source-mismatch` | `WAIVER_REJECTED ×3 … reason=gate-source-mismatch` + 3 FINDINGs | 103 | 100 | **killed** |

8/8 mutants killed, 4/4 plant controls behave, 0 survivors, 0 inconclusive (every pristine baseline matched the
w1 receipts before each mutation). The gate is fail-closed in every direction attacked: registry sha/rules/kind,
sidecar sha/grammar/existence, target bytes, gate-source bytes, path scope, and value namespace.

## 5. Findings

1. **No invariant broken.** No surviving mutant; no basis to narrow or repair the frozen predicate, fixtures or
   claims from this seat. The marker gate patch is landable from base bytes: `install.sh` reproduces the
   measured state exactly (D02 = receipt 11 line-for-line, including the two CritW2Gate `rule-not-listed`
   rejections that are the F1 tightening working as declared).
2. **One doc-level inaccuracy (behavior unaffected).** `w1/ExecSessionMarker.md` §3.7 says an L1 edit of the
   gate-copy bytes "fails closed (`gate-source-mismatch`)"; the first refusal in that exact scenario is
   `sha-mismatch` (W2 sidecar-vs-blob is checked before W4a gate-source comparison — M6). `gate-source-mismatch`
   fires only when the marker pair is regenerated consistently around edited bytes while the gate source stays
   pinned (M8). Both are fail-closed and both print; the report's named reason is the second-line one. Prose
   erratum for the integrator, not a defect; per seat bounds I did not edit w1 files.
3. **Residuals confirmed, unchanged:** the standing 100 findings at the install revision (real identity classes
   + stale round-45/46/47 gate copies) remain red and operator-owned, exactly as the seat reports; nothing in
   this probe reaches a host session value (all plant bytes are reserved-namespace or IANA-reserved text).

## 6. Bounds, tooling, restoration

- Every writer shell ran `ulimit -Sf 2048` (1 MiB/file). Largest authored output file: 22 927 bytes
  (`receipts/out/old-gate-base.py`); all gate outputs ≤ 21 607 B (`receipts/largest-files.txt`). Scratch peak
  4.6 MB of the 2 GB budget; `rm -rf` verified (`/fast/scratch/hyaku/mado-r48/` has no `MutRoutedR3` entry).
- Disclosure: git's internal index write (`.git/index`, >1 MiB for ~20 k entries) cannot happen under a *hard*
  1 MiB cap, so the guard was applied as a soft limit (`ulimit -Sf`) and only the confined `gitx()` subshell
  around git index writes lifted the soft limit. No authored artifact exceeded 1 MiB; no host-level setting was
  changed.
- No pacman/package transaction (host pause respected), no installs, no compositor/input/GUI access, no
  `xdg-terminal-exec`, no serial/title/process-table/home output anywhere in this report or the receipts
  (gate outputs name files/rules/counts only — by the gate's own contract).
- Every clone commit asserted `git rev-parse --show-toplevel` = the clone dir before committing; scratch
  identity only; lane untouched (`git status` shows only this seat's `w2/MutRoutedR3/` evidence and this report
  as new untracked paths).
