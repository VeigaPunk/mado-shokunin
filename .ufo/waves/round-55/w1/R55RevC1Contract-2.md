# R55RevC1Contract-2 — report (round 55, wave w1, claim C1 attack)

Seat-name collision: a peer with the same seat name (`R55RevC1Contract`) wrote into the same directory and owns `R55RevC1Contract.md` and `attack.md`. I wrote to the no-clobber names `attack-2.md` and `R55RevC1Contract-2.md`, moved my own fixtures to `R55RevC1Contract/attack-2/`, and left the peer's files untouched.

## What I did
1. Read `claims-frozen.md`, `registration.md`, `frozen-tables.json` (C1 rows only) at the frozen commit `54dacbd8`.
2. Archived `corpus/` and `.ufo/waves/round-55/` from `54dacbd8` into a scratch fixture repo (`/fast/scratch/hyaku/mado-r55/R55RevC1Contract/base.*`), read-only on the lane (`git -C <lane> archive`).
3. Wrote my own §C1 checker (`c1check.py`), with `--cells strict` (frozen grammar) and `--cells gfm` (escape-aware).
4. Built junk entry J1 (copied frozen quotes, filler propositions, provenance trio, four registry rows, one README row), J2 (identifier-stuffed), J0, and three ablations; applied the seven frozen C1 controls to J1, each in a fresh scratch repo.
5. Probed the proposed clause on honest-looking sentences.

## Key outputs (trimmed)
```
base (freeze commit, no entry):  MADO_KBD_ENTRY: rev=HEAD rows=0/18 … verdict=TARGET_MISSED missed=entry_absent,provenance,index,row:K01…,new_rows
J1 strict:  … rows=17/18 … verdict=TARGET_MISSED missed=row:K16
J1 gfm:     MADO_KBD_ENTRY: rev=3c8bde4d… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none
J2 gfm:     … rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none
J0 gfm (K17 → S052): … sources=17/18 … missed=source_cell:K17
J1 without S378–S380 gfm: … sources=14/18 new_rows=0/3 missed=source_cell:K10,K11,K12,K18,new_rows
controls (gfm): absent→entry_absent; K04→quote:K04; K01 anchor→anchor:K01; K10→source_cell:K10; drop K17→row:K17; H02→quote:H02,host:H02; pin→tables_sha,pin_hash   (7/7 required legs present)
curl S381 URL → HTTP 404 ; curl S378 URL → HTTP 200
```

## Findings (scoped to C1)
- **F1 (predicate-blocking, grammar).** K16's frozen quote contains `||`; the grammar forbids `|` inside a cell, so `row:K16` fails for every entry under the literal reading. Needs an L1 ruling before scoring.
- **F2 (predicate-blocking, K17).** `source_cell:K17` needs a registry URL containing the frozen commit. S052 (wayland) has none, and wayland is not in `new_row_pins`. Only a constructed URL passes (S381, HTTP 404).
- **F3 (control ambiguity).** C1-CTL-6 needs `host:H02` to fire on the row's own quote, not on frozen equality; a first-leg-only counter fails the control.
- **F4 (control wording).** C1-CTL-7 "change one hex nibble … AND of its pin bytes" admits a consistent-change reading under which only `tables_sha` fires.
- **F5 (unnamed leg).** 40/20-character proposition minimums are not a named leg.
- **F6 (undefined term).** `sources=<c>/<d>` numerator undefined.
- **F7 (index exactness).** "exactly one README row" vs existing rows with notes after the path.
- **F8 (who writes new_rows).** The L1 writes S378–S380 "at integration" but the counter reads `--rev`; a seat rev fails unless the seat writes them.
- **Junk result.** Under the gfm reading, J1 satisfies all legs and all seven controls, so C1 as frozen does not discriminate content. Clause-level quantification is in `attack-2.md`.
- **Proposed clause (not frozen).** `prop_topic:<id>`: each K/H proposition contains `repeat`, `delay` or `numlock`. Stops J1 (0/24 pass), not J2 (22/24 pass), one false positive on 8 honest probes. Cannot be frozen now (predicate is frozen); next-round cost roughly one round. A stronger `prop_frozen:<id>` costs L1 authoring 24 sentences before the freeze.

## Deliverables
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC1Contract/attack-2.md` (the attack write-up)
- `.../w1/R55RevC1Contract-2.md` (this report)
- `.../w1/R55RevC1Contract/attack-2/`: `c1check.py`, `build_attack.py`, `build.log`, `results.json`, `J1-entry.md`, `J2-entry.md`, `probe.py`, `probe.txt`

## Not verified
- The frozen counter and harness were not run or read; my checker is my own reading (ambiguities listed above).
- No honest entry was written, so the false-positive rate of `prop_topic` is measured on 8 sentences only.
- The "human reviewer" rejections are my judgment.
- Two read-only `curl` GETs were made for the URL check; nothing else touched the network. `hyprctl` not run. No hold-out fixture touched.

## Tooling
None installed or upgraded. No pacman, no `~/.local/bin` changes.

## Cleanup
Scratch `/fast/scratch/hyaku/mado-r55/R55RevC1Contract/` removed before yield; receipts copied into `attack-2/` first. No tracked-file edits, no git mutation of the lane, no subagents.
