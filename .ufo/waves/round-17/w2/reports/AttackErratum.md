# AttackErratum — erratum R16-V1 (round 17, wave 2)

Target: `corpus/lessons/round-16.md:161-177` (erratum block) at lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60`. Lane worktree file is clean vs
HEAD (blob `fb31cd2…`, 177 lines, sha256 `5a8d2dbf…`); at verification time
the only other modifications in `git status` are sibling wave-2 edits to
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/terminal-route-r17.md`
and `corpus/lessons/round-17.md`, none in my target.

**Result: the attack failed. Every erratum claim reproduced; no counterexample
to the erratum was found.** Residual risks and verification gaps are in §3-§4.
No lane file was written except this report; no installs or host probes.

## 1. Append-only, byte level

Exact command and result:

```
$ git diff --numstat 27cd06f 988b858bd6049bc709807534fd725c05264f7e60 -- corpus/lessons/round-16.md
18	0	corpus/lessons/round-16.md
$ git diff --stat 27cd06f 988b858 -- corpus/lessons/round-16.md
 corpus/lessons/round-16.md | 18 ++++++++++++++++++
$ git diff 27cd06f 988b858 -- corpus/lessons/round-16.md | head -4
@@ -157,3 +157,21 @@ quality improved narrowly for the instrument/source precision while the
```

Independent byte proof:

- original at `27cd06f`: 12,478 bytes, sha256
  `6d47d6f3aefa2e259551f873a93b3bb0fd48a01e53fb5f895380be9c4d71eca5`;
  first 12,478 bytes at `988b858`: **same sha256**; new file 13,623 bytes
  (+1,145). The hunk starts at the last three context lines and adds 18 lines
  at EOF.
- `diff <(git show 27cd06f:corpus/lessons/round-16.md) <(git show 988b858:corpus/lessons/round-16.md | sed -n '1,159p')`
  is empty (`PREFIX-IDENTICAL`).
- Range contains exactly one touching commit:
  `3722ba4` (18 insertions, 0 deletions). `git diff --summary` is empty (mode
  unchanged, 100644). Working tree equals HEAD blob `fb31cd2…`.
- `4bfb236` vs `27cd06f` for the same file is empty, so the superseded lines
  131-132 were stable through the integrator spot-check commit.

No deletion, no rewrite, no reordering: append-only holds.

## 2. Claim-by-claim verification

| # | Erratum claim | Anchor | Result |
|---|---|---|---|
| 1 | Superseded text is lines 131-132 at `27cd06f`: "Input tamper control returns **2 snapshot_tampered**, retained in `frozen-tampered.json`." | `git show 27cd06f:corpus/lessons/round-16.md` lines 131-132 | Exact. Line 131 ends "retained in"; line 132 begins "`frozen-tampered.json`." |
| 2 | That receipt is `.ufo/waves/round-16/evidence/frozen-tampered.json`, measured `9dcf248`, gate `13d86fb0…` | receipt JSON (blob `d00ba869…`, added at `1e31681`) | Field values exact: `measured_commit 9dcf248993…`, `action_gate_sha256 13d86fb0b34c…dcdb73` = `git show 9dcf248:tools/mado-action-plan.py \| sha256sum`. |
| 3 | Receipt records exit 2 `frozen_error` with detail "expected.json pair 1/'denied_executable:sudo' is unreachable" | receipt `exit`, `stdout` JSON | Exact: `exit: 2`, `finding: frozen_error`, detail byte-equal to the erratum's quote. |
| 4 | "the M6 pair defect fired before any digest check" | `git show 9dcf248:tools/mado-action-plan.py` | Pair-reachability check at lines 446-460; input read/digest loop at lines 462-472. Predicate is `want_finding.startswith(a + ":")` over entries already ending in `:`, so `"denied_executable:sudo"` tests against `"denied_executable::"` and fails. `frozen_error` is emitted before plan/policy are even read. |
| 5 | "`matched_exit: true` compared the exit code only" | receipt key set | Receipt keys: `label, measured_commit, action_gate_sha256, command, exit, stdout, stderr, expected_exit, matched_exit`. No `expected_finding`; `exit == expected_exit == 2`. The round-17 recut adds `expected_finding` + `matched`, i.e. the field the round-16 shape lacked. |
| 6 | `snapshot_tampered` is evidenced on the got-side of `frozen-tampered-plan` and `frozen-tampered-policy` in `action-selftest-final.json` (measured `1e31681`) and already in the red `action-selftest.json` (measured `9dcf248`) | both selftest receipts | Both receipts contain, verbatim: `SELFTEST PASS frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered` and the same for `-policy`. Final: exit 0, 52 PASS / 0 FAIL, measured `1e31681`, gate `226220ae…`. Red: exit 1, 51 PASS / 1 FAIL (`frozen-denied-match`), measured `9dcf248`, gate `13d86fb0…`. The tamper rows pass in both. |
| 7 | Round 17 re-receipted the CLI tamper control: `frozen-tampered-recut.json`, one-byte plan change, tampered exit 2 `snapshot_tampered`, untampered control exit 0 `frozen_match`, gate `226220ae…` | `.ufo/waves/round-17/evidence/frozen-tampered-recut.json` (blob `1199954a…`, committed `fc6f960`, worktree byte-identical) | Fields exact. Independently replayed from fresh copies of `.ufo/waves/round-16/frozen`: tampered run exit 2, stdout **byte-equal** to the receipt; control run exit 0, stdout **byte-equal**. Tamper reproduced as exactly one byte (0-based offset 175, `0x74→0x76`, `"libinput"`→`"libinpuv"`, length preserved, valid JSON); post-tamper sha256 `052c03b2…` matches both receipt and replay. `pristine_digests` (`e76090a3…`, `82bc7652…`, `fb134d8f…`) equal the files at `0175f13` and in the worktree. `action_gate_sha256 226220ae…` equals the tool at `0175f13`, `1e31681`, `HEAD`, and the worktree. |
| 8 | "The fleet report's line 64 sentence names no receipt; it is outside this lane repo and is not edited" | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mado.md:64` | The sentence is "Tampered frozen input returns2 `snapshot_tampered`; original receipt retained." It contains no receipt path or filename. The file is outside `mado-shokunin/` (fleet repo path), last commit `cd4c0ea` (2026-10-20 06:06), `git diff cd4c0ea HEAD` empty and worktree clean — not edited in round 17. The lane's own `corpus/lessons/round-16-verifier-spotcheck.md:64` is blank, so the cited sentence is unambiguously the fleet file. |
| 9 | "Routed into QUALITY 23 and `lessons/round-17.md` M1" | `corpus/QUALITY.md:111`; `corpus/lessons/round-17.md:15` | QUALITY 23 is the receipt-label criterion and cites R16-V1. Lesson M1 row exists at HEAD and in the worktree, names `round-16.md:131-132` at `27cd06f` against the `9dcf248` receipt. `label-check.py` run at current content: `LABEL R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks 'snapshot_tampered')`, greens ok, `EXPECT_SUMMARY: 7/7`, exit 1. |
| 10 | "Status-neutral for round-16 C2" | `round-16-verifier-spotcheck.md:172`; fleet report line 46 | Independent spot-check says verbatim: "Status-neutral: C2 rests on 52/52 + frozen_match." Fleet C2 verdict is "demonstrated classifier; final selftest52/52 and frozen_match exit0 at corrected content." Neither the 52/52 nor the frozen_match depends on the mislabeled tamper sentence; the two tamper selftest rows pass in both red and final receipts. |

## 3. Residual risks / low-severity observations

No high- or medium-severity counterexample exists. The following are wording
or evidentiary boundaries, not contradictions:

- **L1 — `matched_exit` semantics are inferred, not source-verified.** No
  round-16 receipt-generating harness is committed in the lane or the fleet
  `.ufo` tree; `grep -rln "action_gate_sha256"` finds only reports and JSON
  receipts. The erratum's "compared the exit code only" is supported by the
  receipt schema (no `expected_finding`) and by the recut's added
  `expected_finding`/`matched` fields, but the harness itself cannot be read.
  No counterexample; a strict reader should treat "compared" as "the recorded
  comparison."
- **L2 — fleet sentence is literal-but-narrow.** Line 64 says "original
  receipt retained," which a reader may resolve to the only tamper receipt,
  `frozen-tampered.json` — the one that records `frozen_error`. The erratum's
  "names no receipt" is literally true (no path/token join), but the sentence
  still repeats the unsupported `snapshot_tampered` claim by reference. The
  erratum never says the sentence is correct; it says the file is out of lane
  and unedited. Worth naming explicitly if the fleet report is ever revised.
- **L3 — revision cited is the containing commit, not the introducing commit.**
  The sentence was introduced at `4bfb236`; the erratum cites `27cd06f`.
  `git diff 4bfb236 27cd06f -- corpus/lessons/round-16.md` is empty, so the
  citation is true, but it is not the commit that added the line.
- **L4 — "the fleet report" is not path-qualified.** It resolves only by
  searching to `.ufo/reports/round-16/mado.md`. The lane file of the similar
  name has a blank line 64, so no ambiguity in fact, but the erratum gives no
  path.
- **L5 — round-16 tamper is not reproducible.** The receipt's command points
  at `/tmp/mado-r16-frozen-tamper-pt60l_e_`, which no longer exists. The
  erratum does not claim reproducibility of the round-16 run; it cites its
  recorded outcome and re-receipts the control at current content (which I
  reproduced). Only the current-content recut is replayable.

## 4. Verification gaps

- No harness source exists for the round-16 generic receipts, so the
  `matched_exit`-only claim rests on schema plus the recut's shape (L1).
- I did not re-run the round-16 `--selftest`; I read the committed red/final
  receipts. The round-17 CLI recut was re-run in `/tmp` copies with byte-exact
  stdout.
- I did not re-fetch any web source; everything is lane-local or a git object.
- Fleet-report authorship/editing beyond `git log`/`git diff` was not
  observable; the fleet repo shows no post-round-16 change to that file.

## 5. Install / mutation record

Installs: **none** (no pacman/sudo/uv/npx/pip/curl). No compositor, service,
input, package or host probes. Lane writes: this report only. All replay
writes were temporary copies under `/tmp` and were removed.
