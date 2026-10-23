# RcTripwireFrozenReplayGate1020 — C2 ledger attack on CapTripwireFrozenReplayGate1020

Seat: `MadoR25A3.RcTripwireFrozenReplayGate1020` (reviewer, leaf, no spawns).
Under review: `MadoR25A3.CapTripwireFrozenReplayGate1020`, C2 re-run of SCORECARD.md:1020
("tripwire frozen replay (gate entry)") at base `41cc04c8d593837a0d5078bffaacdaa163d12897`,
report `.ufo/waves/round-25/a3w1/reports/CapTripwireFrozenReplayGate1020.md`.
Method: independent re-derivation — own clone, own runs, byte-level diff against the seat's
retained captures. Nothing run in the lane; clone deleted afterward. No installs.

## What was run (own sandbox, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset)

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/rc
timeout 600 git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin \
  /fast/scratch/hyaku/mado-r25a3/rc/CapTripwireFrozenReplayGate1020
git -C <clone> checkout -q --detach 41cc04c8   # rev-parse HEAD -> 41cc04c8d593837a0d5078bffaacdaa163d12897
cd <clone>
timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen
timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen
timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-19/frozen
# tamper: cp -a .ufo/waves/round-18/frozen ../tamper-tw; XOR byte 0 of inputs/r13-root.jsonl
timeout 600 prlimit --as=4000000000 python3 -I tools/mado-tripwire.py --frozen ../tamper-tw
```

## Comparison — every ledger claim reproduced

| Claim in ledger line | My observation | Match |
|---|---|---|
| row at `SCORECARD.md:1020`, under `### Capabilities (round 18)` at `:1016` | grep on `git show 41cc04c8:SCORECARD.md`: row text identical at line 1020, heading at 1016 | yes |
| base file 1618 lines, sha256 `6b6995ff…53ca08` | identical count and hash | yes |
| tool sha256 `cd9da20c…00ea84` (round-23 restored classifier) | `sha256sum tools/mado-tripwire.py` in clone identical | yes |
| `--frozen round-18` exit 1, `frozen_verdict_mismatch` | identical | yes |
| all 5 input digests ok, `expected_sha256 4f3534ae…` | identical (5/5 `ok:true`) | yes |
| `missing_findings` empty, 3 extra `package_query/pacman:-Q` (r13-root.jsonl:4, r14-source-safety.jsonl:2,3) | byte-identical JSON | yes |
| selftest 31/31 exit 0, `SELFTEST_SCRIPT_SHA256 cd9da20c…` | identical, 31 CASE lines in same order | yes |
| one-byte tamper → exit 2 `snapshot_tampered`, `r13-root.jsonl` `ok:false` | identical | yes |
| round-19 baseline `frozen_match` exit 0, `expected_sha256 50d2a45e…` | identical | yes |
| command form in ledger | matches the row's own `python3 -I tools/mado-tripwire.py --frozen …` spelling | yes |

Byte-level proof: re-ran all four commands to files and `diff`ed against the seat's retained
captures `/fast/scratch/hyaku/mado-r25a3/c2/{frozen-r18,frozen-r19,tamper-r18,selftest-r18-frozen}.txt`
— **all four IDENTICAL**. The embed `tool_sha256 cd9da20c…` is the round-23 tool, not the
round-18 acquisition receipt's `c1ae45a7…`, so the output cannot be a copied round-18 receipt
(those recorded `frozen_match`/exit 0). No copied-not-run evidence found.

## Superseding pointers — all verified verbatim at 41cc04c8

- `:1134` — "Round-18 frozen baseline now reads `frozen_verdict_mismatch` … round-19 baseline
  `frozen_match` (`50d2a45e…`)": verified.
- `:1085-1090` — r18 `expected.json` pairs named as tw-recall input population: verified.
- `:1110-1111` — "the change made visible": verified (line 1110 carries `frozen_verdict_mismatch`).
- `:1191`, `:1330`, `:1391`, `:1458` — all repeat r19 match / r18 expected red: verified.
- `:1566-1572` + `:1580` — round-24 status table preamble ("supersedes the implied `works` of
  every earlier row") and row ("`frozen_verdict_mismatch`, exit 1 — … not a replay failure"):
  verified verbatim. Same observation, same nuance as this re-run.
- `:1598-1607` — C2 calibration 1/12 → 0/12 over 12 heading-scoped rows: verified.

Own sweep: enumerated all `frozen`/`frozen_match`/`frozen_verdict_mismatch`/`snapshot_tampered`
hits (66 / 17 lines) at base; every post-1020 hit either is cited by the report or concerns a
different frozen artifact (frozen populations, oracle fixtures, other gates). No missed
superseding or contradicting text; no later row retires the capability or claims a green r18
baseline.

## Discrepancies found

- **Minor under-enumeration (immaterial):** the notes say the wave-relative evidence pointer
  resolves to three receipts; the glob `tripwire-frozen-*.txt` actually matches four files —
  `tripwire-frozen-selftest-redbefore.txt` (tool `c87a31ef…`, commit `abfbf35b…`, the red
  "before" selftest) is also present. Does not affect the ledger line.
- Nothing else: no wrong revision, no overclaim, no missed superseding text. The report's own
  caveats (row command can never exit 0 post-round-19; "works" is the 0/1/2 sense, not exit-0)
  are accurate and important — a C2 counter that treats exit 0 as the works predicate would
  wrongly fail this row.

## Cleanup

Clone and tamper copy deleted: `rm -rf /fast/scratch/hyaku/mado-r25a3/rc/{CapTripwireFrozenReplayGate1020,tamper-tw}`
(plus /tmp captures). The seat's own cleanup claim verified: its clone dir absent, only the
declared raw captures remain in `/fast/scratch/hyaku/mado-r25a3/c2/`. No lane writes besides
this report; no `__pycache__` left in the lane.

## Verdict

RECHECK CapTripwireFrozenReplayGate1020: agree — ledger line, exit codes, verbatim blocks,
command form and all six superseding pointers independently reproduced byte-for-byte at
41cc04c8; the only flaw is an immaterial under-enumeration of the round-18 evidence receipts
(four files match `tripwire-frozen-*.txt`, three named).
