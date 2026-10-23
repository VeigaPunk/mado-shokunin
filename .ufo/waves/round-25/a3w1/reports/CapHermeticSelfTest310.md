# CapHermeticSelfTest310 — C2 row re-run: SCORECARD.md:310 (`hermetic self-test`)

Seat: `MadoR25A3.CapHermeticSelfTest310` (leaf executor, C2 row contract). Wave: round-25 attempt 3, `a3w1` (pre-data).

## What I did

1. Read the named row and its section at base `41cc04c8` (SCORECARD.md is 1,618 lines there). Line 310 sits under
   `## Round 12 (kaika) — results` (line 276) in `### Capabilities (round 12)` (line 304):
   `| hermetic self-test | 269 assertions over isolated fixtures | \`bash tools/mado-verify.sh --selftest\` → 269/269,
   \`gate-selftest-after.txt\` | 5 (re-demonstrated 12) |`.
   - Capability stated: hermetic self-test — 269 assertions over isolated fixtures.
   - Demonstration command: `bash tools/mado-verify.sh --selftest`.
   - Evidence pointer: `gate-selftest-after.txt` → `.ufo/evidence/round-12/gate-selftest-after.txt` (present at `41cc04c8`;
     its full committed content is two lines: `MADO_SELFTEST: 269/269 assertions passed` / `exit=0`).
2. Made the sandbox clone and detached at the base (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset throughout):
   ```
   mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
   env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapHermeticSelfTest310
   env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r25a3/c2/CapHermeticSelfTest310 checkout -q --detach 41cc04c8
   # rev-parse HEAD → 41cc04c8d593837a0d5078bffaacdaa163d12897
   ```
3. Re-ran the demonstration command in the clone exactly as written (timeout 600, prlimit --as=4000000000):
   ```
   cd /fast/scratch/hyaku/mado-r25a3/c2/CapHermeticSelfTest310 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 bash tools/mado-verify.sh --selftest; echo "exit=$?"
   ```
4. Grepped the whole SCORECARD.md at `41cc04c8` for later rows/text that supersede or contradict line 310 (findings below).

## Verbatim command output (complete; 2 lines)

```
MADO_SELFTEST: 460/460 assertions passed
exit=0
```

Wall time 26.30 s. Clone tree after the run: `git status --porcelain` printed nothing (0 lines) — the self-test left no
tracked or untracked change in the clone, consistent with isolated fixtures.

## Superseding / contradicting text in SCORECARD.md at 41cc04c8

- **Superseded count (grew, never regressed):** line 529 (round 13) `372/372`; line 1005 (round 18) `372 → 389/389`;
  line 1136 (round 19) `389 → 443/443`; line 1192 `452/452`; line 1221 (round 19 addendum) gate `050efc72…`, 4,194 L,
  `selftest 460/460`; line 1400 (round 20 attempt-2 harm watch at `a8960de`) `gate selftest 460/460, regression PASS`.
  The gate bytes at `41cc04c8` are `sha256:050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`, 4,194 lines —
  the same gate the round-19 addendum pinned at 460/460, so my 460/460 reproduces that row exactly.
- **Explicit supersession of the implied `works`:** line 1577, the round-24 capability-status table
  (`### Capability status (round 24 re-demonstration)`): `| hermetic self-test | works | MADO_SELFTEST: N/N assertions
  passed, exit 0 at 8e5d9369 |`, with the table's own note that it "supersedes the implied `works` of every earlier row".
- **Contradiction:** none. No later row reports the gate self-test failing or its assertion count dropping; the grep for
  failure wording returns only historical round-1..11 rows and unrelated frozen-runner/suite notes (e.g. line 420's
  "initial frozen selftest crashed" is a round-13 frozen-verdict runner, not `mado-verify.sh --selftest`).
- **Note on the evidence pointer:** the round-12 pointer file is accurate for round 12 (269/269, exit=0) but carries no
  measured-commit/gate-sha header; a later round (line 557) records that such headerless selftest receipts fail its
  provenance audit. Not a contradiction of the capability, only of the receipt's provenance completeness.

## Ledger line

```
| SCORECARD.md:310 | hermetic self-test | 269 assertions over isolated fixtures | observed at 41cc04c8: works — exit 0, MADO_SELFTEST: 460/460 assertions passed | bash tools/mado-verify.sh --selftest | SCORECARD.md:1577 (round-24 status: works, N/N at 8e5d9369); SCORECARD.md:1221,1400 (selftest 460/460) |
```

## Disposition

- Capability: **works** at `41cc04c8`; the row's numeric claim (269) is stale — the suite has grown monotonically to
  460/460, and later SCORECARD text already carries that count. The capability statement ("assertions over isolated
  fixtures") is not contradicted; the self-test ran hermetically (no tree writes, no live-surface dependency observed).

## Risks / caveats

- Count reproduction is exact (460/460, gate sha `050efc72…` matching the round-19/20 records); this is one run at the
  base, not a re-run sweep.
- I did not run `--regression` or the live gate: outside this row's demonstration command.
- Host state: no nested compositor, no write verb, no package changes, no tool installs. No processes left behind
  (`pgrep -af CapHermeticSelfTest310` empty); only pre-existing unrelated `/tmp/*mado*` host dirs exist.
- Sandbox clone at `/fast/scratch/hyaku/mado-r25a3/c2/CapHermeticSelfTest310` deleted after the run:
  `rm -rf /fast/scratch/hyaku/mado-r25a3/c2/CapHermeticSelfTest310` → exit 0; `ls /fast/scratch/hyaku/mado-r25a3/c2/`
  no longer lists it (only sibling seats' pre-existing artifacts remain, untouched).
