# CritPremiseC1 — round 48 w1 report (premise falsification, leaf seat)

Status: **complete**. Findings: `.ufo/waves/round-48/w1/CritPremiseC1/findings.md` (F1-F7, with the four assigned
questions answered and smallest safe corrections to the C1 claim wording). Receipts: same seat dir `receipts/`.

TL;DR:
- **Q2 yes** — warm answers differ from cold on this resolver; built and ran the cheapest case (same-size swap of the two
  list lines + mtime re-pin): warm prints `termA` (cache), cold prints `termB`, rc 0 both; reproduced inside the judge's
  exact bwrap sandbox.
- **F2 (schema-critical)** — the draft "prime … wait for the background save" cannot run inside the graded sandbox: bwrap
  `--die-with-parent` kills the forked `save_cache` at teardown, so no cache ever appears (matrix receipt). Prime outside
  or synthesize cache bytes.
- **F3 (schema-critical)** — host-primed cache hashes never match inside the sandbox: host `ls` prints resolved names,
  sandbox (no /etc) prints numeric ids (`1000 1000`); seed hash must use the in-sandbox listing (or amend clause i with a
  minimal passwd mapping).
- **Q3 yes** — stale-but-valid is reachable with an ordinary same-size in-place edit within one wall-clock minute (ls
  minute resolution); receipt `minute-probe.txt`.
- **Q4** — trust-every-well-formed-cache fails stale/invalid/disabled fixtures; cold-only fails warm-differ fixtures;
  shell-out is blocked only by keeping strace clause `r` on warm runs; the full-matrix implementation requires the exact
  `ls -LRl` byte emulation (shape cataloged in F4, from a traced real `ls` argv).
- **Q1 yes (for the tool)** — nothing executes the warm path today (tools/mado-terminal.py:82-85); the resolver's cache
  mechanism is already documented (xdg-terminal-selection-r47.md:25,41-43; README.md:110 lists it open).
- D1 HOME-unset re-verified: exit 1, empty stdout, `HOME: unbound variable` (xdg-terminal-exec:148).

Safety/compliance: no pacman, no terminal/GUI launch (pin ran only with `--print-*` + scratch `XDG_CACHE_HOME`), no
compositor verbs, no git/jj mutation, no tool installs (only `cp` of the 7 externals into scratch for bwrap). Scratch
`/fast/scratch/hyaku/mado-r48/CritPremiseC1` deleted after receipt copies (see cleanup note in seat receipts).
