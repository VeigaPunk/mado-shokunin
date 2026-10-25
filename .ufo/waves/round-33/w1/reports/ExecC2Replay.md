# ExecC2Replay — C2 counter replay (round-33)

Scope: re-run `.ufo/waves/round-33/c2/count.py` against the real scorecard and both
control cards. No edits to `SCORECARD.md` or the counter. Re-executed at write time;
output below is what the commands actually printed.

## Run 1 — real scorecard

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c2/count.py \
    --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --scorecard /home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md
PRED-C2-r33-v1 claim_mismatch=1 reason=absent verdict=TARGET_MISSED
exit code: 1
```

## Run 2 — honest control card

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c2/count.py \
    --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --scorecard /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/controls/c2-honest-card.md
PRED-C2-r33-v1 claim_mismatch=0 reason=match published=7 measured=7 verdict_word=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MET
exit code: 0
```

## Run 3 — junk control card

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/c2/count.py \
    --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --scorecard /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-33/controls/c2-junk-card.md
PRED-C2-r33-v1 claim_mismatch=1 reason=mismatch published=3 measured=7 verdict_word=target-met rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MISSED
exit code: 1
```

## Findings

- Counter discriminates correctly: honest control passes (`TARGET_MET`, exit 0),
  junk control fails (`TARGET_MISSED`, exit 1) with `reason=mismatch`
  (published=3 vs measured=7).
- Real `SCORECARD.md` fails with `reason=absent`: the expected C2 claim row is not
  present in the published scorecard, so the counter reports `claim_mismatch=1`
  without a published/measured comparison. Verdict `TARGET_MISSED`, exit 1.
- `measured=7` is stable across both cards that reach measurement; pinned rev for
  the controls is `d9ed38166cc3be8ef4c52b41d66ad94010feb047`.
