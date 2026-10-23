# ExecPopulationAfter — routed defect 6 (round-27 w1)

Seat `MadoR27.ExecPopulationAfter` (leaf). Scope: the round-26 SCORECARD population sentence (does it hold?) and the
launcher environment of the round-26 before-receipts. No counter, harness, W set, control or lane source was edited.
The only files written are the two below.

| path | sha256 | bytes |
|---|---|---|
| `.ufo/waves/round-27/evidence/r26-population-after.txt` | `faf6df7e07c9681e9aae81a8866eb69c6c5c593c98497bc423fe260f27323f98` | 3906 |
| `.ufo/waves/round-27/w1/reports/ExecPopulationAfter.md` | this file | — |

## Verdict

`ROUTED-DEFECT-6 / SCORECARD population sentence: holds — both after-receipts give POPULATION verdict=PASS, exit 0 — met`

(No `CONTROL <name> best:` line: this item is a routed repair, not a K1*/K2* control, and no control file was written.)

The SCORECARD sentence (`SCORECARD.md:1725-1726`):

> Population check (QUALITY 37): `python3 -I .ufo/waves/round-26/quality/check-population.py --registration
> .ufo/waves/round-26/registration.md` on both after-receipts → `POPULATION verdict=PASS`, exit 0.

It was true when committed and is true at the current tip. What the routed defect got right is that no **run receipt**
for it was committed; this evidence file is now that receipt.

## Exact commands and results

All three runs used the committed checker (`sha256 803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64`),
the committed registration (`c79bf244f696ccae9ef01aea8604f26c58ef9e34c9f7d8b9682548dee9875a01`), the C1 after-receipt
(`f5d6ccb2615f25947dacbf65604c4af6821ab459f2c1fb69d0ae8cfa7d4bc8fe`) and the C2 after-receipt
(`150a834aa4b32cb595ad8c454e3b4570a9a1e7e29b77c0053ced8d85974174c8`). Each was launched from
`/home/vgpnk/Projects/shokunin/mado-shokunin` under `env -i PATH=/usr/bin HOME=/home/vgpnk` so no live-session variable
reaches the process; the checker reads text and spawns nothing. Verbatim stdout and exit codes are in the evidence
file.

1. Both after-receipts (the sentence's run):

```
$ env -i PATH=/usr/bin HOME=/home/vgpnk python3 -I .ufo/waves/round-26/quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt .ufo/waves/round-26/evidence/c2-after-a496b02a.txt
POPULATION registration=.ufo/waves/round-26/registration.md predicates=PRED-C1-r26,PRED-C1-r26-v2,PRED-C2-r26
POPULATION receipt=.ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt pred=PRED-C1-r26-v2 cases_pass=41/41 case_lines=41 registered=41 agree=ok
POPULATION receipt=.ufo/waves/round-26/evidence/c2-after-a496b02a.txt pred=PRED-C2-r26 cases_pass=51/51 case_lines=51 registered=51 agree=ok
POPULATION verdict=PASS receipts=2 agree=2 mismatch=0 unreadable=0
exit=0
```

2. C1 after-receipt alone: `POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0`, `exit=0`.
3. C2 after-receipt alone: `POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0`, `exit=0`.

No run stderr, no exit 2, no re-run needed.

## Was the sentence true at its own commit?

Yes, measured against committed blobs, not only the worktree:

- registration at the SCORECARD commit `178d335` = `sha256 c79bf244…` = worktree = `HEAD` blob (`git hash-object` ==
  `git rev-parse HEAD:.ufo/waves/round-26/registration.md`, `8a3f5f1a…`).
- `git show 178d335:SCORECARD.md` = `sha256 de63aacf57a5855d5f2f1c442faa7e2ccc522baf96833d02a1b238f0261cba7e` = worktree
  `SCORECARD.md`.
- The two after-receipts and the checker are blob-identical to `HEAD` (`git hash-object` == `git rev-parse HEAD:<path>`).

Hidden dependency (measured, auxiliary section of the evidence file): with the pre-v2 registration at `05319e0`
(`sha256 ca98430f…`, no `PRED-C1-r26-v2` paragraph) the same two receipts give
`pred=PRED-C1-r26-v2 … registered=- agree=MISMATCH legs=registration_total`, `POPULATION verdict=FAIL`, `exit=1`.
So the sentence is true only because the registration at its commit already carried the v2 paragraph. The sentence
pins no hashes; recommendation to the L1 (I did not edit `SCORECARD.md` — not my write scope): cite
`.ufo/waves/round-27/evidence/r26-population-after.txt` and the four sha256 values beside it.

## Second half — launcher environment of the round-26 before-receipts

Trace inventory (the only trace that exists):

- `.ufo/waves/round-26/evidence/c1-before-96101be5.txt:1` — `$ python3 -I .ufo/waves/round-26/c1/count.py 96101be5`
- `.ufo/waves/round-26/evidence/c2-before-96101be5.txt:1` — `$ python3 -I .ufo/waves/round-26/c2/count.py 96101be5`
- No `env`/`PATH=`/`HOME=`/locale/cwd/`measured_at=` line in either file; the counter body records only the counter
  and oracle sha256, tool sha256, `seed=`, and the snapshot digest.
- The seeds (`d3e03b349a661890` C1, `6bc64fbee15a3eb9` C2) occur nowhere else under `.ufo/waves/round-26` or
  `round-27` (grep), so no seat transcript replays the same run and pins its environment.
- Contrast: both after-receipts record `$ env -i PATH=/usr/bin HOME=/home/vgpnk python3 -I … --jobs 6` plus
  `measured_at=` (`c1-after-v2-2b3487f7.txt:1-2`, `c2-after-a496b02a.txt:1-2`).
- Closest trace of how a base counter was launched in round-26 w1:
  `controls/K1DoNothing.txt:12` `command base: cd … && timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I
  .ufo/waves/round-26/c1/count.py 96101be5`, and `w1/reports/K2DoNothing.md:33-34`
  `prlimit --as=4000000000:8000000000 timeout 880 python3 -I .ufo/waves/round-26/c2/count.py 96101be5` — inherited
  seat environment, no `env -i`, different seeds (so re-runs, not the committed receipts).
- The round-26 verifier already noted the gap: `corpus/lessons/round-26-verifier-spotcheck.md:135` — "Both
  after-receipts and both residual re-measures were launched `env -i PATH=/usr/bin HOME=/home/vgpnk` (M26-5 mitigated
  for measurements); the two before-receipts record no `env -i` prefix (routed, item 6)."

Conclusion: the launcher environment of the committed before-receipts is **not recorded and not reconstructible**. The
header establishes only that the launcher was plain `python3 -I` under the producing seat's inherited environment (no
`env -i`, no wrapper recorded). The round-26 receipt bytes are frozen evidence — adding a line would change their
sha256 and break every counter/population citation — so the record is made here. The defect's forward fix is already
in force for round 27: `registration.md` §Host safety requires `env -i PATH=/usr/bin` for every nested run and receipt.

## Host safety and process hygiene

- `coredumpctl /usr/bin/Hyprland` records: 1338 before, 1338 after (delta 0). No Hyprland, oracle, `/dev/dri` node or
  live `hyprctl` was touched; no `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` reached any child (`env -i`).
- No tool installed or upgraded; no pacman; no service action.
- No git/jj write command: only read-only `git ls-files`, `git log`, `git show`, `git hash-object`, `git rev-parse`
  with `GIT_OPTIONAL_LOCKS=0` in the lane.
- No scratch tree created; `/fast` checked before use (`113G` free) and left untouched; no background process remains.

## Risks and limits

- The checker is count-level by design: PASS proves registration-total == printed denominator == `CASE` line count for
  both after-receipts; it does not re-derive the 41/41 or 51/51 case outcomes (the counters' own receipts do that).
- The PASS is contingent on the post-v2 registration (`c79bf244…`); see the sensitivity probe.
- Nothing is committed by this seat (no git/jj writes): the evidence file and this report are working-tree bytes for
  the L1 to commit.

Blockers: none.
