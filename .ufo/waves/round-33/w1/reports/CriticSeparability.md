# CriticSeparability — mado round 33, wave 1

Seat: critic. Task: state the command that verifies C1 with C2's verdict line
absent, state the command that verifies C2 with the two new knowledge files
absent, and run the C2 command against the current SCORECARD (files absent is
the current tree). No knowledge files created. Lane HEAD at measurement:
`9a46ccf3282117f960b8d53cd71599a91f388ee3`.

## Commands

### C1 verified with C2's verdict line absent

```sh
python3 -I .ufo/waves/round-33/c1/count.py --root . --frozen .ufo/waves/round-33/c1/frozen.json
```

C2's verdict line (`r33-claim-verdict: r32-C1 cited_entries=…` in SCORECARD.md)
cannot reach this counter: `c1/count.py:51-107` opens only `frozen.json`,
`corpus/SOURCES.md`, the two frozen entry paths, and the four fetch blobs under
`--root`. SCORECARD.md is never opened, so the line's presence or absence is
not an input. Absence confirmed in the measured tree:
`grep -c 'r33-claim-verdict' SCORECARD.md` → `0` (grep exit 1).

Observed output on the current tree (2026-10-24):

```
PRED-C1-r33-v1 closed_entries=0 closed_rows=0 open_cites=4 verdict=TARGET_MISSED
exit=1
```

Byte-identical to the frozen pre-data do-nothing receipt
`.ufo/waves/round-33/controls/c1-donothing.txt` — no verdict line existed and
none was needed.

### C2 verified with the two new knowledge files absent

```sh
python3 -I .ufo/waves/round-33/c2/count.py --repo . --scorecard SCORECARD.md
```

Neither `corpus/knowledge/waybar-module-text-route-r25.md` nor
`corpus/knowledge/event-delivery-limits-r26.md` is an input: `c2/count.py`
reads the `--scorecard` file and re-runs the frozen r32 counter inside a
`git archive <rev> corpus` extraction into a tempdir (`count.py:42-61`) —
git objects at the line's `rev=H`, never working-tree knowledge files.
Absence confirmed in the measured tree:
`ls corpus/knowledge/waybar-module-text-route-r25.md corpus/knowledge/event-delivery-limits-r26.md`
→ `No such file or directory` on both; `corpus/knowledge/` holds 46 notes.

## C2 run against the current SCORECARD — pasted output

```sh
$ python3 -I .ufo/waves/round-33/c2/count.py --repo . --scorecard SCORECARD.md
PRED-C2-r33-v1 claim_mismatch=1 reason=absent verdict=TARGET_MISSED
exit=1
```

Byte-identical to the frozen do-nothing receipt
`.ufo/waves/round-33/controls/c2-donothing.txt` (`reason=absent`, exit 1).

## Separability verdict: SEPARABLE

- C1 → TARGET_MISSED (0/0/4) with the verdict line absent; the counter has no
  read path to SCORECARD.md.
- C2 → TARGET_MISSED (`reason=absent`) with the knowledge files absent; the
  counter's only corpus access is a `git archive` of the rev named inside the
  scorecard line it parses.
- Note on the C2 output shape: in the `reason=absent` path the counter exits
  before invoking `r32_cited` (`count.py:73-81`), so `measured=` is not
  printed — consistent with the honest-control receipt; not a defect.
- Honest-stop line that would flip C2: `published=7 measured=7
  verdict_word=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047`
  (frozen honest control, `controls/RECEIPT.md`). No such line exists in the
  scorecard; nothing in this run admitted or forged it.

Kill rules honored: both commands printed `verdict=TARGET_MISSED` on the
un-landed tree — each claim is verifiable without the other having landed.
