# R56ExecUsedByFix — C3 registry fix (data only; no tracked file touched)

Deliverables in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecUsedByFix/`:
`fix.py`, `old-to-new.md` (the lesson's old->new log, 45 rows), `SOURCES.new.md` (fix.py output at base, for review),
`recount.py` + `recount.txt` (independent counter), `census-old.txt` / `census-new.txt` (census validate output).

## fix.py
`python3 -I fix.py --repo REPO --rev REV --out DIR [--sep SEP]`: reads `corpus/SOURCES.md` and `corpus/knowledge/*.md` (regular blobs, direct children) with `git ls-tree`/`git show` at REV only; fenced (``` / ~~~) lines do not count; writes `DIR/SOURCES.md`, `DIR/old-to-new.md`, `DIR/changes.tsv`. Only cell 11 of rows with missing pairs changes: existing cell text (incl. its leading/trailing padding) kept byte for byte, missing paths sorted and appended. Non-row ids (e.g. S383 before the S383 row exists, S243) are ignored. Exit 2 + stderr on setup error (bad rev, non-11-cell row, SOURCES.md not a regular blob).

## Run at base 13f0acbe3a15da2d9c08357a576d91dcadc85273
```
FIX: rev=13f0acbe... entries=70 rows=319 changed_rows=45 pairs=65
```
**45 rows, 65 pairs** (65 expected: matches).

Independent re-count (`recount.py`, own regexes/code, entries read from a `git archive` of base):
```
old entries=70 rows=319 missing=65 extra=0 dangling=0
new entries=70 rows=319 missing=0 extra=0 dangling=0
changed lines 45 bad (other than cell11 append): 0 unique ids 45
```
`diff old new`: 45 lines `<`, 45 `>`, line count identical, file tail byte identical; per changed line cells 1-10 and the text after cell 11 split equal, cell 11 = old text + appended paths. `old-to-new.md` lists exactly the 45 rows, and its set-difference of paths sums to 65.

Census: scratch lane mirror (`git archive` of base into scratch, registry replaced) then
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` -> **exit 0**, no E lines; output identical to the old registry's except W01 S277 text now shows its extended used-by (warning, as before) and the file path. (`--file` resolves the lane dir as the parent of the registry's dir, so the mirror must be a full lane tree: used-by paths such as `corpus/README.md`, `SKILL.md`, `quality/check-index.py` need to exist.)

Rerun at a later rev: tested on a scratch git repo (base corpus + a synthetic `hyprland-config-autoreload-r56.md` citing S002, S005, S100, S383 and a fenced S003) -> 71 entries, 47 rows/68 pairs; entry appended to S002, S005, S100 only; fenced S003 and non-row S383 ignored.

## Disagreements / ambiguities
1. **Separator.** The assignment says paths are "space-separated". `sources-census.sh` splits used-by on `,` only (lines 562): a space-joined cell yields one bogus path, tried live: 39 E11 findings, exit 1. fix.py therefore defaults to `, ` (the existing multi-entry convention, e.g. S277), which gives census exit 0; registration's counter uses a regex and is separator-blind. `--sep ' '` reproduces the literal reading. Chose the census-compatible one because exit 0 is an explicit acceptance item.
2. **"—" cells.** 8 changed rows (e.g. S007, S030) have used-by `—`; keeping it byte for byte gives `—, corpus/knowledge/...md`. Census skips `—` tokens (no E11) and W03 for those rows disappears. Cosmetically odd; dropping the `—` would violate the byte-for-byte rule, so not done. The L1 may prefer a different call.
3. Pair count 65 equals registration's baseline; rows changed is 45 (registration states pairs only).

## Not verified
The registration's own counters/harness (`quality/counters/c3-r56-used-by.py`, `check-r56-controls.py`) were not run (not part of the assignment/may not exist yet). The lane's `corpus/knowledge/hyprland-config-autoreload-r56.md` does not exist yet, so the final-rev behavior was only tested on the synthetic repo. No tools installed. Scratch dir removed.
