# Mado round 24 — registration (before any data seat)

Base: lane branch tip `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` (master; r23 closure commit on top of r23 tip
`fa819d56`). Dispatched 2026-10-23T03:02Z; scope freeze 05:02Z, hard stop 06:02Z. This file and both frozen
counters land before any data seat runs; the control receipts land after them and before data.

Anti-loop: rounds 20–23 all worked the tripwire classifier (operability) and r23 was rejected on it. This
round changes no file under `tools/` and works two other surfaces: a province frontier route (coverage) and
the lane's own capability self-assessment (calibration, the lowest scored axis — round-17 counter `c1`,
7.1875 as last recorded in `.ufo/waves/round-23/registration.md:48`, below the 9.0 saturation line, so no
stagnation waiver).

## Repair first — routed defects of `corpus/lessons/round-23-verifier-spotcheck.md` §7

Non-claim repairs, landed before the claims' data:

1. lesson-23 stale "note file does not yet exist" (:197-199) → append-only correction in lesson 23.
2. README round-23 bullet lacks the withdrawal → appended withdrawal pointer in `corpus/README.md`.
3. M23-4, M23-5, M23-7 `captured-by` none with QUALITY unchanged → lesson-cited QUALITY criteria (LEARNING
   §Understanding), each with a check shown able to fail; recorded in lesson 24.
4. sha256 prefixes printed like commit hashes → every sha256 in round-24 files and the report carries a
   `sha256:` label.
5. S149 anchor `:1014` spans `:1013-1014` → correction logged in lesson 24 (SOURCES is append-only except
   status/recheck/used-by, so the anchor cell is not edited; the lesson records the corrected span).
6. r23 C1 carry-forward: the wave-2 regression fixtures are frozen as a registered discovery population
   (copied byte-exact with a sha256 manifest) under `.ufo/waves/round-24/carry/`; no tripwire change.
7. H2 precision 166/175: L0 question at fleet `.ufo/l0-questions.md:103` still open; no action.

## Claims (two; distinct axes; causally separable)

### C1 — coverage (sourced): Hyprland window-rule *attribution* route

Surface moved: the `corpus/README.md` `## Frontier` item "Still open: rule *attribution*" (round-12 bullet)
moves to documentary sourced ground in a new entry `corpus/knowledge/rule-attribution-r24.md`, built only on
SOURCES rows opened 2026-10-23. The command that shows it unmoved is the same counter.

Frozen predicate (identical in `c1/count.py` and every receipt):

> PASS_ROW: a claim row `| A<n> | <claim> | S### | "<quote>" |` in corpus/knowledge/rule-attribution-r24.md at
> REV whose S### is a SOURCES.md row with status `mined`, opened `2026-10-23`, used-by naming the note, a source
> URL pinned to a tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or
> /hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched from that URL now,
> where the quote (<=25 words, containing a rule-topic word) occurs verbatim (whitespace-collapsed) in those
> bytes.

Counter: `python3 -I .ufo/waves/round-24/c1/count.py REV` (counted mode re-fetches every URL; `--offline` is
diagnostic only). Before at base: `PASS_ROW=0`, note absent, exit 1. **Target: `TARGET_MET` at the landed tip
= PASS_ROW ≥ 6 from ≥ 3 distinct S### rows and the note indexed by a `corpus/README.md` coverage-map row.**

### C2 — calibration (lowest axis): capability table versus re-demonstration

AXES calibration: "SHONEN.md/SCORECARD entries match observed repo state". SCORECARD's capability tables
(rounds 12–21, 12 named capabilities) assert what the lane can do; nothing has re-run them since.

Frozen predicate (identical in `c2/count.py`, `c2/README.md` and every receipt):

> MISMATCH: a capability named in a SCORECARD.md capability table at REV whose self-assessed status (its row in
> a `Capability status (round 24 re-demonstration)` table at REV if present, else `works`) differs from the
> observed status of its frozen manifest command run on the REV tree; a manifest capability absent from REV's
> capability tables also counts as MISMATCH.

Counter: `python3 -I .ufo/waves/round-24/c2/count.py REV` with the frozen `c2/manifest.json` (one
re-demonstration command and pass rule per capability, written from each row's own claim before any data).
Before at base: measured by the control wave's do-nothing receipt. **Target: `mismatches=0` at the landed tip.**
Validity rule: if the do-nothing control already scores 0 mismatches, C2 is void (a do-nothing control meets
it) and is reported as withdrawn before data, not re-scaled.

No exploratory claim. A miss under either predicate is reported as a miss; no predicate, target or manifest
rule changes after the control receipts land.

## Controls (fresh critic / mutation-tester seats, before data)

C1: do-nothing (base); junk note with fabricated quotes; off-topic real rows (r23 terminal sources renamed);
stale rows (S016–S020 opened 2026-10-19); self-fabricated fetch bytes with a matching recorded sha256;
label shortcut (valid ids, quote taken from another source). C2: do-nothing (base); all-`works` status table;
all-`fails` status table; capability rows deleted; status table keyed on names with shuffled statuses.
Each control is scored with the frozen counter and its receipt is committed before data.

## No-harm guards (each must hold at the landed tip)

- `git diff --quiet 8e5d9369 <tip> -- tools/` (production instruments byte-identical).
- r23 C3 counter `python3 -I .ufo/waves/round-23/c3/count.py <tip>` stays `0`.
- r23 C2 counter `python3 -I .ufo/waves/round-23/c2/count.py <tip>` stays `3/3`.
- Sources census exit 0 (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`).
- No removed line in SCORECARD.md, SOURCES.md, LOG.md, PROVINCE.md (`git diff --numstat` removals 0, except
  in-place SOURCES `status`/`recheck`/`used-by` cells logged old→new in lesson 24).
