# Mado R14 w1 — ReviewCorrections: R13-V1..V3 correction paths

Seat: MadoR14.ReviewCorrections (reviewer, leaf). Date 2026-10-20. Lane `mado-shokunin`, HEAD `873ff08`.
Writes: this file and `reports/ReviewCorrections.md` only. Tools installed or upgraded: none.
Checks run: read-only only (`read` of files and committed blobs, `git show <rev>:<path> | sha256sum`, `wc`, JSON key queries). No gate, selftest, build, lint or regression run. No source opened on the web; no source-open rows apply.

## Verdict

All three routed items have a reachable correction path that leaves historical records untouched. Each path has a precondition that the main agent must assign, listed under Decisions.

| Item | Correction path | Reachable? | Precondition |
|---|---|---|---|
| R13-V1 retained-data wording | Appended errata block at the end of `corpus/knowledge/wayland-protocol-boundaries-r13.md` | Yes | No seat owns that file. L1 applies it at integration (D2). |
| R13-V2 boundary vs cross-revision equality | Appended block in `corpus/knowledge/gate-standing-use.md`; fleet report line stays unedited; gate row text stays unchanged | Yes | L1 applies at integration (D2). Fleet report stays as is (D3). |
| R13-V3 standalone receipt digest | Historical receipt untouched; appended binding note in `gate-standing-use.md`; forward path = `ReceiptBuild` wrapper | Forward path yes; in-wave binding conditional | Gate is uncommitted in-wave and wave forbids commits (D1). |

## Verified facts

F1. The U4 sentence is at `corpus/knowledge/wayland-protocol-boundaries-r13.md:43`, under `## Advertisement, binding and behavior`: "The retained S041 data is only registry interface/version headers: output identity, device paths, human-readable seat names, geometry, colourimetry and numeric registry names were discarded."
- `.ufo/waves/round-13/w1/globals.json` `globals[]` entries have key set `[interface, version]` only (`?q=.globals|map(keys)|unique`).
- Top-level keys are `captured_utc, compositor, excluded, global_count, globals, multiplicity, probe, schema, session_binding, set_sha256, tool, unique_interface_count`.
- `probe`, `tool`, `compositor` (keys: branch, commit, dirty, name, probe_command, probe_return_code, tag, version), `multiplicity`, and `session_binding` (keys: captured_utc, correlated, instance_count, probe_command, probe_return_code, unique_signature_match, wl_socket) are retained sanitized metadata.
- `excluded` lists the discarded categories: wl_output identity fields, logical output identifiers, colorimetry blocks, DRM lease device paths, dmabuf device/modifier blocks, seat name and capabilities, shm format table, presentation clock identifiers, registry numeric names.
- Conclusion: the sentence is too broad, as R13-V1 says. The session-correlation acknowledgement is in `## Host point sample` (lines 45–47), not in the paragraph directly after line 43. The erratum should cite the section, not "the following paragraph".

F2. Boundary wording.
- `tools/mado-verify.sh:2702-2703` compares `$after` with `$before` inside one run and emits `row gate boundary.readonly PASS "config plane byte-identical before/after (combined sha …)"`. That text occurs once in the gate.
- Round-13 receipt: `.ufo/waves/round-13/evidence/gate-file-plane.txt:47`, combined sha `3cb692751b4d…`, counts 29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0 (`:48-49`).
- Ambiguous statement: fleet report `.ufo/reports/round-13/mado.md:68`, "…CLEAN, exit 0; byte-identical before/after". It sits in the fleet root repo, which is read-only to this lane.
- Committed combined digests differ across receipts: `.ufo/evidence/round-12/before-no-live.txt` `364b4f5e672b…`; `.ufo/evidence/round-12/gate-no-live-after.txt` `48c882b98e97…`; round-13 `3cb692751b4d…`. The row compares only within one run, so cross-run equality cannot be inferred from it.
- `corpus/lessons/round-13.md:73` already says "boundary hash equal before/after this run". That is precise and needs no change.

F3. Standalone receipt provenance.
- `.ufo/waves/round-13/evidence/gate-selftest.txt` (blob `b093dc4b…` at `59cfbdc`, sha256 `de0f05e6…`, 9 lines) begins `command:`, `cwd:`, `stdout:`. It has no revision or digest header.
- Recovered binding, read-only: `git show 95cbc41:tools/mado-verify.sh | sha256sum` and `git show 59cfbdc:…` both give `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569`. This matches `committed-bindings.json` (`measured_commit` 95cbc41). The base `7dcb785` gate is `ea798ad0…`, a different file, so the receipt must not be bound to the base.
- `corpus/knowledge/gate-standing-use.md:364-402` (`## Current receipt — round 13`) cites the selftest receipt at `:372-373`. The binding appears only indirectly at `:368-370` ("bound to the measured content commit named in the round-13 SCORECARD and report").
- `.ufo/waves/round-14/w1/dispatch.json` task `ReceiptBuild` creates `.ufo/waves/round-14/receipt.py`: header with revision, `git show` blob sha and worktree sha; refuses on mismatch with exit 2; `--selftest` isolated, not run this round.

F4. Lane state. `git status` shows `SCORECARD.md` modified and round-14 files added. `tools/mado-verify.sh` is not modified yet. The gate becomes uncommitted once GateImplement edits it.

## Per-item acceptance checklist

### R13-V1 — retained-data wording

Affected current statement: `corpus/knowledge/wayland-protocol-boundaries-r13.md:43`. Blob sha256 at `59cfbdc`: `0a6a61c1…` (file is 104 lines).

- [ ] V1-1 Line 43 is not edited. Corrections are an appended block after the last line (currently 104), in the note's existing `## Limits` order. QUALITY.md #4 requires errata as append-only blocks.
- [ ] V1-2 The errata block quotes the old sentence verbatim and gives the new wording (draft below). It preserves old and new values, as QUALITY.md #6 requires.
- [ ] V1-3 The new wording names the record-level rule: `globals[]` records carry interface and version only. It names the top-level retained metadata explicitly (`probe`, `tool`, `compositor`, `multiplicity`, `global_count`, `unique_interface_count`, `set_sha256`, `session_binding`, `captured_utc`). It does not use the generic phrase "sanitized metadata" alone.
- [ ] V1-4 The block cites `excluded` as the discard list and asserts no retained device or output identity.
- [ ] V1-5 The block keeps the advertisement-only and no-feature-behaviour non-claims.
- [ ] V1-6 Not touched: `.ufo/waves/round-13/w1/globals.json` (blob sha `ced47240…`), `corpus/lessons/round-13-verifier-spotcheck.md`, `SOURCES.md` S041 row (already says "without retaining device/output identity"), `corpus/README.md` U4 row.
- [ ] V1-7 Optional, not required by V1 and not to be added unless the main agent expands scope: the discard list omits the shm format table, presentation clock identifiers and logical output identifiers.

Draft errata block (for L1 to apply after the last line of the note):

```
## Errata (append-only — add blocks, never edit above)

### R13-V1 (round 14, 2026-10-20) — retained-data wording
- Old text (line 43, unchanged above): "The retained S041 data is only registry interface/version headers: output identity, device paths, human-readable seat names, geometry, colourimetry and numeric registry names were discarded."
- Correction: the global records in `.ufo/waves/round-13/w1/globals.json` carry only `interface` and `version`. The same capture also retains sanitized top-level metadata: `probe`, `tool` (package and binary pins), `compositor` (commit and tag pins), `multiplicity`, `global_count`, `unique_interface_count`, `set_sha256`, and `session_binding` (correlation booleans, probe return code, capture time, socket name), as described under "Host point sample". The `excluded` list in the same file records the discarded categories.
- Non-claim: this correction adds no retained device or output identity and no feature behaviour. The advertisement-only boundary stands.
```

### R13-V2 — within-run boundary versus revision-output equality

Affected statements:
- S2a `.ufo/reports/round-13/mado.md:68` (fleet root): "byte-identical before/after". Read-only from this lane. Must not be rewritten.
- S2b `tools/mado-verify.sh:2703`: row text. It is accurate about its own scope. Do not change it. Changing it moves gate bytes away from `037b05dc…`, invalidates bindings, and requires a regression re-cut (`gate-standing-use.md` §5 rule 2; SOURCES S044).

- [ ] V2-1 The errata block states the scope of `boundary.readonly PASS`: the config-plane digest is equal at the start and end of one gate run. Cite `gate-file-plane.txt:47`, combined sha `3cb692751b4d…`.
- [ ] V2-2 The block states the row does not establish equality of outputs across revisions or runs. Cite the three differing combined digests in F2.
- [ ] V2-3 The block names the fleet report line 68 and reads it only as the within-run statement. The fleet file is not edited.
- [ ] V2-4 The block preserves the legitimate result: 29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0.
- [ ] V2-5 The block makes no new cross-revision byte-identity claim and runs no new measurement.
- [ ] V2-6 Verify at integration with `grep -c 'config plane byte-identical before/after' tools/mado-verify.sh` = 1. If GateImplement touched that line, stop and re-plan.
- [ ] V2-7 Placement: appended after line 402 of `corpus/knowledge/gate-standing-use.md`, following the `## Current receipt — round 13` precedent at `:364`. Do not edit the block above it.

Draft errata block (for L1 to apply after the last line of `gate-standing-use.md`):

```
## Errata — round 14, R13-V2 (2026-10-20): boundary scope

- Scope of `gate boundary.readonly PASS`: in one gate run, the config-plane digest taken before the run equals the digest taken after it. Round-13 receipt: `.ufo/waves/round-13/evidence/gate-file-plane.txt:47`, combined sha `3cb692751b4d…`; counts 29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0.
- Not established by that row: byte-identical outputs across revisions or runs. Committed combined digests differ across receipts (`.ufo/evidence/round-12/before-no-live.txt` `364b4f5e672b…`; `.ufo/evidence/round-12/gate-no-live-after.txt` `48c882b98e97…`; round-13 `3cb692751b4d…`), and the row does not compare them.
- The phrase "byte-identical before/after" in `.ufo/reports/round-13/mado.md:68` (fleet root, not edited here) is to be read only as the within-run statement above. It does not establish cross-revision equality.
```

### R13-V3 — standalone receipt measured digest

Affected statements:
- S3a `.ufo/waves/round-13/evidence/gate-selftest.txt`: no revision or digest header. Historical receipt. Do not add a header in place.
- S3b `corpus/knowledge/gate-standing-use.md:372-373`: cites the receipt. The binding is indirect at `:368-370`.

- [ ] V3-1 `gate-selftest.txt` is unchanged (blob `b093dc4b…` at `59cfbdc`).
- [ ] V3-2 Historical: the gate-standing-use errata (V2 block, or a sibling V3 block) states the recovered binding, with the derivation command: `git show 95cbc41:tools/mado-verify.sh | sha256sum` = `037b05dc…`, equal at `59cfbdc`, matching `committed-bindings.json`. It also states that the receipt itself carries no header, and that the base `7dcb785` gate (`ea798ad0…`) is not the bound gate.
- [ ] V3-3 Forward: every standalone receipt in round 14 is produced by `.ufo/waves/round-14/receipt.py` (ReceiptBuild), not hand-assembled. Its header carries `revision` (the commit whose blob sha equals the worktree sha), the gate sha256, the command, the exit status, and the stable ids.
- [ ] V3-4 On sha mismatch, the wrapper refuses with exit 2 and writes no passing receipt. The `--selftest` covering matching and mismatching digests, exit propagation and stable ids is run once by L1 after the seats finish, not by seats.
- [ ] V3-5 Decision D1 must be resolved before V3 is claimed closed for round 14 (see below). A provisional receipt is labelled provisional and rebound at the integration commit (QUALITY.md criterion 7).

## Decisions for the main agent

- D1 (V3, blocking for closure). The wrapper binds to a committed `REV`. The round-14 gate will be uncommitted during the wave, and the wave forbids commits. A receipt produced in-wave cannot be bound to an existing commit, so the wrapper refuses. Options: (a) integrator commits the gate, then L1 runs `receipt.py`, which yields a bound receipt; or (b) the wrapper emits a provisional receipt labelled `binding: worktree-uncommitted` with the worktree sha, rebound at commit. Option (a) is cleaner; option (b) needs a ReceiptBuild change. Without one of them, V3 stays open for round 14.
- D2 (V1 and V2). Seats own only their artifact paths, and no seat owns the two knowledge notes. Without an explicit L1 integration step, both errata are unreachable in round 14. Assign them to L1 at integration.
- D3 (V2). Confirm that the fleet report `.ufo/reports/round-13/mado.md:68` stays unedited. The correction lives only in the lane's knowledge errata, citing that line.
- D4 (scope guard). GateImplement must not change `tools/mado-verify.sh:2703` (V2-6) or any text the V1/V2 errata cite.

## Residual risk

- The V2 row wording is accurate within its scope, but a reader can still misread "before/after". The errata reduce this and do not remove it.
- The V3 binding for round 13 rests on the derivation command and the committed-bindings file, not on the receipt's own content. This is status-neutral debt, as the lesson says.
- No live or behavioural claim was checked. None of the three items depends on one.
