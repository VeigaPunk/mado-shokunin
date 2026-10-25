# ExecC2Matrix — r34 calibration counter matrix

## Command

Every run, from `/home/vgpnk/Projects/shokunin/mado-shokunin` (so the
`--frozen` relative path resolves):

```bash
python3 .ufo/waves/round-34/c2/count.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --scorecard <CARD> \
  --frozen .ufo/waves/round-34/c2/frozen.json
```

Only `--scorecard` varies across rows.

## Matrix (`scratch/ExecC2Matrix/matrix.tsv`)

```tsv
card	exit_code	stdout
/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md	0	PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
.ufo/waves/round-34/controls/c2-junk-card.md	1	PRED-C2-r34-v1 published=128 measured=169 mismatch=1 verdict=TARGET_MISSED
.ufo/waves/round-34/controls/c2-reachable-card.md	0	PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
.ufo/waves/round-34/scratch/ExecC2Matrix/card-line128.md	1	PRED-C2-r34-v1 published=128 measured=169 mismatch=1 verdict=TARGET_MISSED
.ufo/waves/round-34/scratch/ExecC2Matrix/card-no-marker.md	1	PRED-C2-r34-v1 published=absent measured=169 mismatch=1 verdict=TARGET_MISSED
```

## Cards

- `SCORECARD.md` — real card; last `r34-s189-line:` at line 2108 publishes `line=169` → TARGET_MET.
- `controls/c2-junk-card.md` — junk control, single marker `line=128` → TARGET_MISSED.
- `controls/c2-reachable-card.md` — reachable control; last marker at its line 2108 publishes `line=169` → TARGET_MET.
- `scratch/ExecC2Matrix/card-line128.md` — created this seat; carries an earlier `line=169` marker then a later `line=128` marker, proving last-marker-wins → TARGET_MISSED.
- `scratch/ExecC2Matrix/card-no-marker.md` — created this seat; no `r34-s189-line:` substring anywhere → `published=absent`, TARGET_MISSED.

## Findings

- `measured=169` on every row: the pinned fetch `.ufo/waves/round-32/fetch/S189.bin` is a
  regular file, `nlink=1`, sha256 `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`
  (verified with `sha256sum`/`stat`), and its line 169 strip-equals
  `const size_t MAX_QUEUED_EVENTS = 64;` while line 128 does not (`sed -n '128p;169p'`).
- Only the `published` leg moves: the verdict hinges solely on the last `r34-s189-line:`
  marker in the card — `169` → exit 0, `128`/`absent` → exit 1.
- `c2-junk-card.md` and `card-line128.md` produce identical stdout; the counter cannot
  distinguish a wrong-line junk card from a superseded-marker card.
- stderr was empty on all five runs; no run hit exit 2 (`die`), so the frozen predicate
  matches the script's compiled-in `PREDICATE`.

## Tooling record

Installed or upgraded nothing. Runs used system `python3` (stdlib only) plus
coreutils `sha256sum`, `stat`, `sed` for verification.
