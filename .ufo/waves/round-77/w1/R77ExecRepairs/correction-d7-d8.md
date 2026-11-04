# D7/D8 — round-76 report and declaration pointers

Seat R77ExecRepairs, round 77, 2026-11-04. Lane HEAD `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7`.

## D7 — report pointer arithmetic

Wrong sentence: `.ufo/reports/round-76/mado.md:119-120`

> **No-harm watch** (`receipts/harm-watch-r76.txt`, re-executed at `587b2989`; the tip commit adds
> only that receipt and the census):

Measured at HEAD, the tip commit adds **only** the harm-watch receipt; the census landed earlier:

    $ cd /home/vgpnk/Projects/shokunin/mado-shokunin
    $ git diff-tree --no-commit-id --name-status -r 2308e12a
    M	.ufo/waves/round-76/receipts/harm-watch-r76.txt

    $ git diff-tree --no-commit-id --name-status -r e160d18e
    A	.ufo/waves/round-76/census-end-r76.txt
    A	.ufo/waves/round-76/measurement-c2-r76-final.txt
    A	.ufo/waves/round-76/receipts/harm-watch-r76.txt
    M	LOG.md
    M	SCORECARD.md
    M	corpus/knowledge/interprocedural-del-r76.md

    $ git diff --name-status 587b2989 2308e12a
    M	.ufo/waves/round-76/receipts/harm-watch-r76.txt

So the census (`census-end-r76.txt`) landed at `e160d18e`, not at the tip. Correction (append-only,
never rewriting the report):

> Correction (round 77): the tip commit `2308e12a` adds only
> `receipts/harm-watch-r76.txt` (`git diff-tree --no-commit-id --name-status -r 2308e12a`
> prints that single `M` row; `git diff --name-status 587b2989 2308e12a` agrees). The census
> `census-end-r76.txt` landed at `e160d18e` (`git diff-tree --no-commit-id --name-status -r
> e160d18e` prints `A .ufo/waves/round-76/census-end-r76.txt`).

Landed as the D7 item of `corpus/lessons/round-76.md:185` `## Corrections (round 77)`:

```markdown
- **D7 (pointer arithmetic).** The round-76 report says the tip commit adds "that receipt and
  the census"; measured, `git diff --name-status 587b2989 2308e12a` shows only
  `M .ufo/waves/round-76/receipts/harm-watch-r76.txt` (the census landed at `e160d18e`).
```

## D8 — declaration pointer

Wrong sentence: `.ufo/waves/round-76/claims-declaration-r76.md:166-168` (R2):

> every selftest tally quoted this round is committed as a receipt with its command, stdout and
> exit code under `.ufo/waves/round-76/receipts/`.

Measured at HEAD, the tallies are **not** under `receipts/`:

    $ git ls-tree --name-only 2308e12a .ufo/waves/round-76/receipts/
    .ufo/waves/round-76/receipts/harm-watch-r76.txt
    .ufo/waves/round-76/receipts/label-derivation-r76.txt
    .ufo/waves/round-76/receipts/repair-r76-c1-base-absent.txt
    .ufo/waves/round-76/receipts/repair-r76-c2-d3.txt

    $ git ls-tree --name-only 2308e12a .ufo/waves/round-76/w1/R76ExecC1/
    .ufo/waves/round-76/w1/R76ExecC1/count.txt
    .ufo/waves/round-76/w1/R76ExecC1/counter-selftest.txt
    .ufo/waves/round-76/w1/R76ExecC1/harness-selftest.txt
    … (label files and report.md)

    $ git ls-tree --name-only 2308e12a .ufo/waves/round-76/w1/R76ScoutChain/probes/
    .ufo/waves/round-76/w1/R76ScoutChain/probes/probe-c2-d3-d4.py
    .ufo/waves/round-76/w1/R76ScoutChain/probes/ran-c1-outcome-field.txt
    .ufo/waves/round-76/w1/R76ScoutChain/probes/ran-c1-per-case.txt
    .ufo/waves/round-76/w1/R76ScoutChain/probes/ran-c2-shapes.txt
    .ufo/waves/round-76/w1/R76ScoutChain/probes/ran-probe-c2.txt
    .ufo/waves/round-76/w1/R76ScoutChain/probes/ran-selftests.txt

Correction (append-only; fix the path, not the evidence):

> Correction (round 77): the quoted selftest tallies are committed at
> `w1/R76ExecC1/counter-selftest.txt`, `w1/R76ExecC1/harness-selftest.txt` and
> `w1/R76ScoutChain/probes/ran-selftests.txt` (each with command, stdout and rc), not under
> `receipts/` (`git ls-tree --name-only 2308e12a .ufo/waves/round-76/receipts/` lists only
> harm-watch, label-derivation and the two repair receipts).

Landed as the D8 item of `corpus/lessons/round-76.md:185` `## Corrections (round 77)`:

```markdown
- **D8 (declaration pointer).** `claims-declaration-r76.md` R2 says every quoted selftest tally
  is committed "under `.ufo/waves/round-76/receipts/`"; measured, the tallies are at
  `w1/R76ExecC1/counter-selftest.txt`, `w1/R76ExecC1/harness-selftest.txt` and
  `w1/R76ScoutChain/probes/ran-selftests.txt` (each with command, stdout and rc).
```
