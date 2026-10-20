# ErratumR17 draft (round 18)

## (a) Append-only erratum block for `corpus/lessons/round-17.md` (append after line 176)

```
## Erratum R17 (append-only, round 18)

Corrects lines 175-176 above. The original text reads, verbatim:

> `tripwire/w2-regressions` 30/30; tool sha256 `962919ce…`;
> all real-transcript receipts re-cut with identical counts.

The tool sha `962919ce…` is the landed tip tool (`0ab1ccc`, verified by
`git show 0ab1ccc:tools/mado-tripwire.py | sha256sum`). The receipt claim is
not supported by git. Read-only `git log` / `git show` at lane HEAD `d3a0000`
records:

- Under `962919ce…` (commit `0ab1ccc`) exactly one real-transcript receipt
  changed: `evidence/tripwire-r17.txt`. Its aggregate counts are unchanged
  (host_mutation 0, live_probe 1, package_query 0); its per-file entries are
  not (40 of 149 changed, including MadoR17.jsonl: sha256 `da1b4492…` /
  468 lines → `01229723…` / 540 lines).
- `evidence/tripwire-r13.txt`, `-r14.txt`, `-r15.txt`, `-r16.txt`,
  `tripwire-anchor-r15.txt` and `tripwire-pacmanlog-join.txt` were last
  changed at `f71ccbe` (tool `7a98720e…`). `git -C <lane> log --oneline --
  .ufo/waves/round-17/evidence/tripwire-r13.txt` (and the other five) lists
  only `f71ccbe` and `988b858`; `0ab1ccc` touched none of them.
- Counts were not identical across that re-measure. Aggregate counts for r13,
  r14 and r16 match, but per-file `unparsed_spawns` moved (0 → 1 or 2).
  `tripwire-r15.txt` aggregate `live_probe` moved 28 → 29. `tripwire-anchor-r15.txt`
  changed one finding's command text (`pacman -Fl libinput-tools 2` →
  `pacman -Fl libinput-tools`, line 29) while the finding count stayed at 8.
- The receipts carry no tool sha256 or measured-commit field, so the revision
  a receipt was measured under is recoverable only from git history.

So the `962919ce…` re-cut is recorded for `tripwire-r17.txt` alone. The other
six real-transcript receipts were last measured under `7a98720e…` (`f71ccbe`)
and have not been re-cut under the landed tool. Round-18 scan receipts that
name the tool sha and the measured commit are to be produced under
`.ufo/waves/round-18/evidence/tripwire-*.txt`; they do not exist at baseline
`d3a0000` and this erratum does not supply them.
```

## (b) R17-V2 carry-over sentence for the round-18 report

R17-V2 carry-over (calibration, minor): the round-17 before→after C3 row cites the f71ccbe tool sha256 `7a98720e…` (measured in that table; `measure-final.json` `c3.sha256` at rev `f71ccbe`), while the landed 0ab1ccc tool is `962919ce…` (round-17 report line 3; SCORECARD C3 row); both are cited here with those labels.
