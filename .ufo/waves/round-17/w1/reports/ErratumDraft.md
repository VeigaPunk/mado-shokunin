# ErratumDraft report: R16-V1 tamper-control label

Scope: draft the append-only erratum for `corpus/lessons/round-16.md`, identify the
superseded text, state what the receipts record, and list other occurrences of the
mislabel in round-16 LOG.md and SCORECARD.md. Drafted only
`.ufo/waves/round-17/drafts/ErratumDraft.md`. No other product file touched.

## Findings

1. **Superseded text**: `corpus/lessons/round-16.md` lines 131–132 at baseline `27cd06f`
   (`git show 27cd06f:corpus/lessons/round-16.md`), identical to the working tree.
   Text: "Input tamper control returns **2 snapshot_tampered**, retained in /
   `frozen-tampered.json`. No fixture expectation was weakened."
2. **`evidence/frozen-tampered.json`** (sha256 `34a801bd…9722fa`, identical at baseline):
   `measured_commit` 9dcf248; `action_gate_sha256` `13d86fb0…dcdb73`; exit 2;
   stdout `MADO_PLAN: frozen_error`, detail `expected.json pair 1/'denied_executable:sudo'
   is unreachable`; `expected_exit` 2; `matched_exit` true. It is the M6 pair defect,
   firing before any digest check. It records `frozen_error`, not `snapshot_tampered`.
   `matched_exit` checks only the exit code, so it is coincidental agreement.
3. **Where `snapshot_tampered` is evidenced**: `evidence/action-selftest-final.json`
   (measured 1e31681, gate `226220ae…a5aea3`, exit 0). Raw line 12 contains
   `SELFTEST PASS frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered`
   and `SELFTEST PASS frozen-tampered-policy: want 2/snapshot_tampered got 2/snapshot_tampered`,
   summary `52/52 passed`. These are fixture self-invocations, not a retained CLI tamper run.
4. **Round-17 recut**: named in the erratum as
   `.ufo/waves/round-17/evidence/frozen-tampered-recut.json`, explicitly marked "to be
   produced" and not cited until it exists. Not produced by this seat.
5. **Other occurrences, round-16 LOG.md and SCORECARD.md**: none. Case-insensitive
   `grep -i 'tamper|snapshot'` over both files at the working tree, and `grep -n 'tamper'`
   at `27cd06f` for LOG.md, finds no round-16 reference to `frozen-tampered` or
   `snapshot_tampered`. The only SCORECARD hit near the topic is line 438 (round-13 row
   "with tamper refusal"), which describes a rule, not this receipt; it is correct and not
   a mislabel. LOG.md round-16 M6 section (≈lines 1204–1230) cites only
   `action-selftest.json`, `action-frozen.json`, and the `-final` receipts; no tamper claim.
6. **Other occurrences in round-16 tree (not LOG/SCORECARD, for the L1 list)**:
   - `corpus/lessons/round-16-verifier-spotcheck.md:164-166` — the routing itself (R16-V1),
     not a mislabel; it quotes a report phrase, see 7.
   - `.ufo/waves/round-16/w2/reports/AttackPlanSchema.md:45` and
     `AttackSelfinvoke.md:60` cite the fixture name `frozen-tampered-plan`, correctly
     (selftest fixture, not the receipt).
   - `.ufo/waves/round-16/evidence/action-selftest.json:12` (red, pre-fix) — contains the
     `frozen-denied-match` FAIL; `frozen-tampered-plan` PASS line; not a label claim.
7. **Unlocated quote**: the verifier spot-check quotes a report phrase
   "Tampered frozen input returns 2 `snapshot_tampered`". A case-insensitive search of
   `.ufo/waves/round-16` and `corpus` for "frozen input" / "Tampered frozen input" finds only
   the verifier's own quote and unrelated design phrases. The source report is not in this
   tree. L1 should check whether it lives in a fleet location before the erratum names it.
8. **Scope note**: `corpus/lessons/round-16-verifier-spotcheck.md` lines 72–73 cite the
   correct selftest lines; the verifier (R16-V1) says the fix is status-neutral (C2 rests
   on 52/52 + frozen_match).

## Commands run (all read-only; no pacman, sudo, systemctl, hyprctl, probes, or jj)

- `git --no-optional-locks rev-parse --show-toplevel`, `cat-file -t 27cd06f`,
  `show 27cd06f:<path>` (round-16.md, round-16-verifier-spotcheck.md, LOG.md, SCORECARD.md),
  `log --oneline -3 27cd06f`, `status --short`. No write or index mutation.
- `sha256sum` on `frozen-tampered.json` (working tree and baseline, match).
- `grep -n` / `grep -rn` / `sed -n` over the lane.
- Reads of `frozen-tampered.json`, `action-selftest-final.json` (incl. raw line 12),
  `action-frozen-final.json`, round-16 lesson and verifier spot-check.

## Tool installs or updates

None. No tool was installed or updated; no install channel was used.

## Out of scope observed

- `git status --short` shows untracked `.ufo/waves/round-17/gen_w1.py` and
  `.ufo/waves/round-17/w1/`, owned by sibling seats, not touched here.
- The verifier's routed items R16-V2 and R15-V1 are not in this draft's scope.

## Artifacts

- Draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/drafts/ErratumDraft.md`
- Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/w1/reports/ErratumDraft.md`

## Checks for L1 after integration

- Append the erratum draft to the end of `corpus/lessons/round-16.md` (append-only; the
  superseded lines stay). Assign no source id.
- Produce `.ufo/waves/round-17/evidence/frozen-tampered-recut.json` (CLI run at the
  corrected content) before the erratum cites it as evidence.
- Resolve item 7 (source of the quoted report phrase) before any erratum wording names it.
