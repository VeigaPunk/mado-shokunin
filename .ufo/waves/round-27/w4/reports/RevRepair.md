# RevRepair — audit of the round-27 w4 C2 repair candidates (suite A)

Seat: RevRepair, 2026-10-23. Reviewer seat; no lane file other than this report was written.
Scope: every `counter-selftest.py` delivered under `/fast/scratch/hyaku/mado-r27/repair/<SeatName>/`
plus each seat's own three class mutants. The sealed directory
`/fast/scratch/hyaku/mado-r27/heldout/` was never read (role forbids); the only sealed-set
signals used are the three public survivor names
(`HeldC2-extra-disjunction`, `HeldC2-unstable-conjunction`, `HeldC2-embed-boundary`,
`evidence/c2-after-48b9434a.txt`) and the public measurement-1 receipt.

## Baseline state (verified, not assumed)

* Committed suite A at measurement-1 REV `48b9434a0b0619b3896c9d80e8288ec2226c9ed8`:
  sha256 `7fd94b0431849d1be7dc99e120c2f5bd0105c6a1d122e9cd1a3327d30ef3c587`; identical bytes at
  lane tip `86f7355` (quality/counter-selftest.py), i.e. no repair has landed in the lane yet.
* Measurement-1 receipt (`evidence/c2-after-48b9434a.txt`): `green=17/17 b_valid=9
  w_killed=15/15 h_killed=12/18 h_need=14 h_valid=18 invalid=0 verdict=TARGET_MISSED`.
  Six suite-A H rows survived: three on the C1-counter subject (`held-c1v2-node-subset`,
  `held-c1v2-missing-version-guard`, `held-c1v2-extra-output-segment`) and the three C2-counter
  survivors named above, which are this wave's repair target.
* Sandbox: the lane was cloned with `git clone` to
  `/fast/scratch/hyaku/mado-r27/repair/RevLane` (tip `86f7355`); every counter run below is the
  frozen `python3 -I .ufo/waves/round-27/c2/count-v2.py 48b9434a… --suite-a-file … [--heldout D
  --seal F]` from that clone (bubblewrap sandbox, `--no-local` inner clones, `env -i
  PATH=/usr/bin`, 300 s suite timeout, 4 GB RLIMIT_AS — the counter builds all of it).
* Harness replication check (no override, no heldout): `green=8/8 w_killed=15/15` —
  identical to the public part of measurement 1 (`out-baseline.txt`).

## Independent reference mutants (RevRepair's own; yardstick, not a candidate)

Built only from the public subject `.ufo/waves/round-26/c2/count.py` and the three survivor
names (`ref-mutants/*.json`):

| id | old → new (single defect) | why it represents the named class |
|---|---|---|
| `rev-extra-disjunction` | `verdict[lab] = (nm == 0 and ne == 0, …)` → `… or nm + ne <= 1, …` | adds a tolerance disjunct; every committed suite-A probe mismatches with exactly (nm=1, ne=1) (`V3.compare` keys entries on all 18 `FIELDS`, so one changed field ⇒ 1 missing + 1 extra), sum 2 ⇒ invisible to all 18 field probes and to near-perfect; tolerates one defective entry per case |
| `rev-unstable-conjunction` | `if n1 or n2:` → `if n1 and n2:` | the two-BASE-run stability guard becomes a conjunction; the committed `c2-drift` probe diverges both ways (1,1) so it still fires ⇒ survives; a one-directional unstable oracle is now accepted |
| `rev-embed-boundary` | `EMBED_MIN = 12` → `EMBED_MIN = 13` | boundary shift; the 40-char `EMBED_ARG` fixture is still caught so `c2-embed`/`c2-embed-desc` pass ⇒ survives; 12-char embedded args are no longer flagged |

Fidelity run (committed suite bytes as suite A, reference mutants as held-out rows):
all three rows are VALID and `rc=0 SURVIVED` (`out-ref-vs-committed.txt`,
`h_killed=0/3`) — i.e. they are genuine surviving-class representatives, and any repair that
kills its own three class mutants with *behavioural* probes should also kill these.

## Candidate audits

*(filled per candidate below)*

## RECOMMENDATION

*(pending)*
