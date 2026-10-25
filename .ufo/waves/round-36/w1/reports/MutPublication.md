# MutPublication — mutation-tester seat, mado round 36 (residual attack pass, post-wave-1)

Task: prove the round-36 axis publication is actually checked. The gate under
attack is `quality/check-axis-scores.py`; the publication is the prose block in
`SCORECARD.md` that ends the r36 record ("Axis table re-derived at
`a3094c99…` (this round's data commit): navigation 50/50; calibration
resolved-active 48/48; operability selftest 12/12.").

Method: LANE was never edited. Every mutation ran in a throwaway
`git clone --shared` at `/tmp/mado-axis-mut-pub`, committed there (the gate reads
bytes with `git show <rev>:SCORECARD.md`, so only committed mutations are
visible to it), then the same detector was run on pristine, mutated and restored
bytes. Replay script `/tmp/mut-pub-replay.sh`; per-mutant receipts are in
`LANE/.ufo/waves/round-36/scratch/MutPublication/receipt-*.txt`.

## Baseline (pristine)

```
$ git clone --shared /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-axis-mut-pub
$ git -C /tmp/mado-axis-mut-pub rev-parse HEAD
2d905245b6a964e707139ff099265345bfed1854
$ sha256sum SCORECARD.md quality/check-axis-scores.py
74ad29d8e0c55118bc1c09d048aa497b38088bade309148b92384c883945c676  SCORECARD.md
1dfdb5a49222f4ffb74924ef86eb205e85cd22368727b84fe6f9457b515d0b24  quality/check-axis-scores.py
$ python3 quality/check-axis-scores.py --repo /tmp/mado-axis-mut-pub --rev master
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=48/48 derived=48/48 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=2d905245b6a964e707139ff099265345bfed1854
rc=0
```

The same command run against LANE itself (no clone) printed the identical three
`MATCH` rows and `mismatched=0`, rc 0 — the clone is not an environment change.

## Mutant A — published fraction 48/48 → 46/46

Smallest behaviour-bearing point: one number in the live publication.

```
$ sed -n '2294,2296p' SCORECARD.md     # after the edit
Axis table re-derived at `a3094c99ab85bec35534de2447552c47dd2b647f` (this round's data
commit): navigation 50/50; calibration resolved-active 46/46; operability selftest 12/12.

$ sha256sum SCORECARD.md
ec59f0e38bacf5f6cbd53f95b1183fecaa5872435916cdc67269bc4244d10d08  SCORECARD.md
$ python3 quality/check-axis-scores.py --repo /tmp/mado-axis-mut-pub --rev master
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=46/46 derived=48/48 verdict=STALE
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1 rev=d0bd9cd6984fdb051139744fc370bbbf60503b96
rc=1
```

**Verdict: KILLED (CONFIRMED).** Exactly the mutated axis is `STALE`,
`mismatched=1`, exit 1. `derived=48/48` is independently re-derived from
`.ufo/waves/round-31/c2/count.py` at the tested rev, so the gate is comparing
against a live derivation, not against the publication.

## Mutant B — delete the live publication line

```
$ python3 ... # delete the marker-led publication (SCORECARD.md:2294-2295)
$ sha256sum SCORECARD.md
9820175edfc9e5fc4422ff2d9f1b943f4c466190f4ec009cfdd24acb3592794c  SCORECARD.md
$ python3 quality/check-axis-scores.py --repo /tmp/mado-axis-mut-pub --rev master
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=43/43 derived=48/48 verdict=STALE
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1 rev=febc4876196ab6698086770a75ea4bc28ba36ed0
rc=1
```

**Verdict: KILLED (CONFIRMED) — does not pass.** With the live line gone the
parser falls back to the last remaining unquoted marker, the r35-era publication
(`calibration resolved-active 43/43`), and that fallback is itself `STALE`
against the r36 derivation. Fallback is not a pass here; see finding F-2 for the
residual risk in that rule.

## Mutant C — no publication at all

```
$ python3 ... # every "Axis table re-derived at" removed, including the two that
              # are split across a line break ("… docs commit below. Axis table\nre-derived at tip …")
raw regex hits: 6
markers after flatten: 0
$ sha256sum SCORECARD.md
f98538e16ea049607878c972f10467f2fb9f6415fe0bef9c0f29d01da4cd44b6  SCORECARD.md
$ python3 quality/check-axis-scores.py --repo /tmp/mado-axis-mut-pub --rev master
MADO_AXIS_ROW: axis=navigation published=- derived=50/50 verdict=NOT-PUBLISHED
MADO_AXIS_ROW: axis=calibration published=- derived=48/48 verdict=NOT-PUBLISHED
MADO_AXIS_ROW: axis=operability published=- derived=12/12 verdict=NOT-PUBLISHED
MADO_AXIS: checked=3 mismatched=3 rev=222756a7fea9303b757897579ee765b8644427ba
rc=1
```

**Verdict: KILLED (CONFIRMED) — a missing publication cannot pass.** All three
axes read `NOT-PUBLISHED`, `mismatched=3`, exit 1. Note for reproducers: the
pristine card carries **six** raw occurrences of the marker, and only two are
line-leading (`SCORECARD.md:2110`, `:2294`, per
`re.compile(r"Axis\s+table\s+re-derived\s+at")`): two more are bold-prefixed
(`:2179`, `:2230`) and two are wrapped mid-phrase (the sentences at `:2014` and
`:2063` end "… Axis table" and continue "re-derived at …" on the next line, which
the flatten reconstructs). A line-based `grep -v '^Axis table re-derived at'`
leaves four publications behind and the gate still parses one of them, so it is
not a "no publication" state; the receipt shows all six raw matches removed and
`markers after flatten: 0`.

## Findings (mutants that survived)

### F-1 — the named anchor commit is never checked (severity: minor, coverage)

```
$ python3 ... # publication anchor a3094c99… → deadbeefdeadbeefdeadbeefdeadbeefdeadbeef, fractions untouched
$ git cat-file -e deadbeefdeadbeefdeadbeefdeadbeefdeadbeef^{commit}
fatal: Not a valid object name deadbeefdeadbeefdeadbeefdeadbeefdeadbeef^{commit}
rc=128
$ python3 quality/check-axis-scores.py --repo /tmp/mado-axis-mut-pub --rev master
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=48/48 derived=48/48 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=a6eb2dcf29b2bda0e1eb042345f73e0683c69fd4
rc=0
```

**SURVIVED: green, rc 0, with an anchor that does not exist.** The gate parses
the three fractions and never touches the backticked commit inside the
publication, so "re-derived at `<sha>`" is unverified prose: a reader cannot tell
from the gate that the named data commit is real. The numeric contract still
holds at the tested rev, hence minor — but the round-36 claim is about the
publication as a whole, and its anchor is the one field the gate cannot see.

### F-2 — the gate reads committed bytes only; a dirty worktree publication is invisible (severity: minor)

```
$ git status --porcelain
 M SCORECARD.md
$ sha256sum SCORECARD.md
ec59f0e38bacf5f6cbd53f95b1183fecaa5872435916cdc67269bc4244d10d08  SCORECARD.md
2295:commit): navigation 50/50; calibration resolved-active 46/46; operability selftest 12/12.
$ python3 quality/check-axis-scores.py --repo /tmp/mado-axis-mut-pub --rev master
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=48/48 derived=48/48 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=2d905245b6a964e707139ff099265345bfed1854
rc=0
```

**SURVIVED: green while the on-disk card says 46/46.** By design the gate tests
a revision (`git show <rev>:SCORECARD.md`), so an uncommitted publication edit
cannot be detected — the same 46/46 line that Mutant A kills once committed.
Consequence: a cadence that runs the gate before the record commit reports green
on the previous publication. Not a contract violation (the docstring says
"revision under test"), but the receipt for a round must not be taken from a
dirty tree.

Also observed while probing: the "last unquoted marker" rule turns any sentence
ending "… Axis table" followed by "re-derived at …" after flattening into a
publication candidate (two such phrases exist in the r36 card). That is how
Mutant B's fallback engaged; it is not a false pass, because the candidate's
numbers are then checked like any other.

## Restoration evidence

LANE was read-only throughout: `SCORECARD.md` and `quality/check-axis-scores.py`
still hash `74ad29d8e0c55118bc1c09d048aa497b38088bade309148b92384c883945c676`
and `1dfdb5a49222f4ffb74924ef86eb205e85cd22368727b84fe6f9457b515d0b24`
(= the committed blobs at `2d90524`), and `git status --porcelain -- SCORECARD.md quality/`
lists only the pre-existing `M quality/check-evidence-pointers.py` from another seat.

Clone restored to the pristine commit and re-measured:

```
$ git log -1 --format=%H
2d905245b6a964e707139ff099265345bfed1854
$ git status --porcelain
(empty)
$ sha256sum SCORECARD.md quality/check-axis-scores.py
74ad29d8e0c55118bc1c09d048aa497b38088bade309148b92384c883945c676  SCORECARD.md
1dfdb5a49222f4ffb74924ef86eb205e85cd22368727b84fe6f9457b515d0b24  quality/check-axis-scores.py
$ python3 quality/check-axis-scores.py --repo /tmp/mado-axis-mut-pub --rev master
... mismatched=0 rev=2d905245b6a964e707139ff099265345bfed1854
rc=0
```

Gate selftest at the tested bytes: `MADO_AXIS_SELFTEST: 18/18 assertions passed`, rc 0.

Writes: `/tmp/mut-pub-replay.sh`, `/tmp/mado-axis-mut-pub/`, the receipts under
`LANE/.ufo/waves/round-36/scratch/MutPublication/`, and this report. No installs
(python3 + git only); no pacman transaction.

## Bottom line

The two assigned mutants are killed at the observable they target:
`calibration 46/46` vs `derived 48/48` → `STALE`/`mismatched=1`/rc 1; a fully
absent publication → `NOT-PUBLISHED` ×3/`mismatched=3`/rc 1; pristine → `mismatched=0`.
The publication is checked as a *value equality against a live re-derivation*.
What is not checked: the anchor commit the publication names (F-1, green with a
nonexistent sha) and uncommitted publication bytes (F-2, green with a dirty card).
Both are coverage findings for criteria 57–61, not contract changes.
