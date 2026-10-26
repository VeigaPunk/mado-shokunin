# MutC2V2Gates — report (mado r41 w2)

Attack: the v2 C2 counter's own gates. 37 single-edit mutants of
`quality/counters/c2-r41-focus-entry-v2.py` (frozen 294c6679 bytes; pristine
copy + mutants in `.ufo/waves/round-41/w2/MutC2V2Gates/`), each run through the
committed harness `.ufo/waves/round-41/ctl/run-c2-v2-controls.py` **imported by
path, never edited**, its `COUNTER` global repointed per run (driver
`mutrun.py`, `--only NAME` reproduces one mutant). Full table with edits,
observed outputs and line references: `.ufo/waves/round-41/w2/MutC2V2Gates/matrix.md`;
raw per-control results: `.../MutC2V2Gates/results.json`.

Baseline (pristine counter, my harness invocation): `CTL_C2V2: controls=67
correct=67/67` — the battery is valid before any mutation.

**Verdict: 16/37 NOTICED, 20/37 SURVIVED (coverage findings), 1 vacuous.**

## Finding 1 — OPEN DEFECT on the control harness (predicate evidence): pin-shadow breaks the "patched" scorer's stated purpose

The runner's docstring promises a fixture mutant is "killed by ITS clause, not
by the pin" (`run-c2-v2-controls.py:12`). False for any receipt whose basename
is one of the 9 pinned names: `patched_counter` (runner:158-165) inserts the
fixture's hashes BEFORE the original `PINS` entries, and a Python dict literal
keeps the last duplicate key, so the original pin shadows the patch.

Evidence (all reproduced this session):
- Direct: for the N04 fixture, the patched counter's
  `PINS["protocols-README.md"]` is `3c7007636e138898…` (original) while the
  fixture's bytes hash `513f00f4b89b2eb6…` → `pinEqualsFixture=False`; same for
  J17's `xdph-journal.txt` (`bf8fa91a…` vs `2cc1d12a…`).
- Differential: M06 (pin check deleted) flips F1, F3, Z1 **and W16**;
  M14/M15/M16 (their nominal clause-d check deleted) do NOT flip N04/N03/N05 —
  those controls are pin-killed, not clause-killed.
- Pin-shadowed controls: N03, N04, N05, J02, J03, J11, J16, J17, W14, W16, W17.
- Sub-finding: `W16-quote-across-html-blocks` never tests quote-across-HTML —
  its quote binds fine through the HTML normalizer; it only flips when the pin
  is removed (M06). Its kill is the pin-shadow artifact.

Status: controls and counter are frozen; reported open for the L1/round owner.
No third registration performed by this seat.

## Finding 2 — 20 gates of the counter have no sole kill in the committed battery (survived mutants)

Each row is a mutant the whole 67-control battery did not notice; full detail in
matrix.md §B. Classes:

- Clause-d content gates unexercised (all potential killers pin-shadowed):
  M14 quote∈own-receipt (:378), M15 sha256 binding (:374), M16 quote 3-25 words
  (:375), M13 exclusivity loop (:392-396, W15 is seen_quote-killed at :377),
  M08 receipt mode 100644 (:373, W14 pin-killed), M09 512-byte floor (:106,
  no control), M07 pinned-receipt-relocation sub-path (:370).
- Journal gates unexercised: M17 ≥2 sessions + M20 firsts-ascending (:431-432,
  J02/J17 pin-shadowed; J02's tail additionally has 0 boot lines and 37
  adverts), M18 ≥40 adverts and M19 ≥20 distinct interfaces (:431, no control
  in range), M21 `[LOG]`-only grammar (:116, J11 pin-shadowed).
- Header/registry floors: M03 ≥4 sources (:315), M05 header-recheck shape
  (:315, W07/W08 kill at row cells :329 instead), M10 ≥3 new ids (:343, N07
  killed by the per-id row rule :322), M23 lowercase-only ghost sub-path (:307,
  W02 killed by its uppercase body ghost), M34 duplicate index row (:454),
  M35 duplicate registry row (:322), M36 entry-at-BASE precondition (:486-487).
- M27 BAD_LOC scan (:467) has no sole kill: A05/F4 are clause-e kinship-killed
  (probe `e:0`) — a localized source with a kinship-consistent receipt name and
  location would pass every committed control.
- M22 (census anchor `^`, :113) is VACUOUS — `re.Pattern.match` anchors at
  position 0 anyway (probe: prose line does not match, bare line matches); no
  coverage claim is drawn from it.

Per the round contract these are coverage findings on the predicate's controls,
not permission to change the contract; the counter itself is not judged here.

## What held (16 noticed mutants)

Pin forgery cluster (M06 → F1/F3/Z1/W16 flip), STAGED-package discipline
(M11/M12 → A06/A07), ADMIT/REFUSE structure (M26/M28/M29 → A01/A03/A06/A08/A09/
A10), ghost+window+verified-at header checks (M01/M02/M04/M24 → W02/W03/W04/
W05/W06/N11), clause e (M25 → F6/N09/W13), registry mutations (M30/M31/M32/M33
→ N08/N13/N16/X05/X08-class), and over-strict breakage is caught by control P
(M37 shifts OPENED → P-real and P-patched fail). The battery is genuinely
load-bearing for 16 of 37 attacked gates.

## Evidence & hygiene

- All outputs recorded verbatim in matrix.md and results.json; every quoted
  source fragment ≤ 25 words with file:line, verified by grep against
  `c2-frozen-pristine.py` / the runner (line numbers in matrix.md are that
  grep output; runner docstring quote verified at runner:12).
- Restoration: counter sha256 before == after
  `a2226deb860230111b8835a4a76db69d3186c5f85ad7c67cbec972ea2ef6438c`; runner
  sha256 before == after
  `da8d4850d4e061ce78299a528ac53fab951d7d2225b85394c07e7a4a1b7cc9b5`;
  `git status --porcelain` on the counter path empty. Only seat-dir files
  written: `MutC2V2Gates.md`, `MutC2V2Gates/matrix.md`, `mutrun.py`,
  `probe.py`, `results.json`, `c2-frozen-pristine.py`, `mutants/M*.py` (37).
- Scratch: `/tmp/mutc2v2gates-tmp` removed by driver and probe; ~360 `c2p-*`/
  `mado-c2v2ctl-*` dirs in /tmp belong to other concurrently running seats
  (unmodified-runner leak) and were left alone.
- Tooling: nothing installed (system python3 3.14.8 + git sufficient). No
  pacman, no host services, no compositor sockets; git usage read-only in the
  lane; fixture repos are the runner's own throwaway identityless-commit
  tempdirs.
