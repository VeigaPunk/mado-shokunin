# ScribeLog — round-34 LOG.md draft

Draft written to `.ufo/waves/round-34/scratch/ScribeLog/log.md`. LOG.md not
appended (per seat scope).

Format: matches the round-31/32/33 house style — `## Round 34 — <title>
(2026-10-24, attempt 2 — …)` then `Motivation:` / `Work:` / `Honest notes:`,
wrapped near 75 columns. Attempt 2 per the wave context: "a prior attempt
froze the claims and landed the data before its provider route died"
(w1-spec.json context). `Honest notes:` covers C2/notes beyond the two
mandated sections.

Required facts, all stated:

- r33 counter killed by a symlink crib — receipt
  `.ufo/waves/round-34/controls/r33-counter-on-its-crib.txt`:
  `closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET` exit 0 on
  the crib, `TARGET_MISSED` on the honest tree; first shown on
  `.ufo/waves/round-33/scratch/CriticC1Junk/` (SCORECARD round-33 C1 row).
- New counter PRED-C1-r34-v1 frozen at `3420e827bd7b21b1374b23245526554ffd20d096`
  — commit message "round-34: freeze C1 and C2 predicates and pre-data
  control receipts" (git show, 67 files: c1/ c2/ count.py + frozen.json,
  registration.md, 10 c1 + 3 c2 control receipts, control fixtures,
  fetched blobs).
- Data at `fa7ba11346116672352b5d41494141c5c4d738d0` — "round-34: admit the
  waybar event-socket entry after the frozen counter" (entry + S201/S202
  rows + README row + `r34-s189-line: line=169` + axis re-derivation).
- Repairs listed individually (lstat component walk, nlink=1, non-symlink
  root, relative no-dot paths, O_NOFOLLOW, 8 MB cap, sha pin, gate-quote
  substring clause, whole-token used-by; r33 counter unedited).

Verification run at write time (HEAD = fa7ba11):

- `python3 -I .ufo/waves/round-34/c1/count.py --root . --frozen
  .ufo/waves/round-34/c1/frozen.json` → `closed_entries=1 closed_rows=2
  open_cites=0 verdict=TARGET_MET` rc=0.
- `python3 -I .ufo/waves/round-34/c2/count.py --repo . --scorecard
  SCORECARD.md --frozen .ufo/waves/round-34/c2/frozen.json` →
  `published=169 measured=169 mismatch=0 verdict=TARGET_MET` rc=0.
- `python3 -I .ufo/waves/round-33/c1/count.py --root . --frozen
  .ufo/waves/round-33/c1/frozen.json` → `open_cites=4 verdict=TARGET_MISSED`
  rc=1 (r33 instrument stays frozen, unedited).
- All 10 committed c1 control receipts re-read: 9 TARGET_MISSED kills +
  golden TARGET_MET; c2 receipts: donothing/junk MISSED, reachable MET.
- `read_regular` hardening re-read at count.py:40-86.

Honest limits: verdicts are self-measured; non-author spot-check still owed.
Draft is scribe output — the L1/integrator decides whether to append.
