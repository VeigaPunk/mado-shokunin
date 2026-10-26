# MutC2V2 — mutation probe of PRED-C2-r44-v2 (round 44, wave w2)

Seat: MutC2V2 (leaf, no subagents, no background jobs). Target per tasking: the v2 tightenings — **T1-T4,
the exact census exemption, clause j** — of `quality/counters/c2-r44-gkeep-size-request-v2.py`
(sha256 `3246d2aa388b6e187a6c5c6176305ec32bda7a58a67fc57f6582e3fd769b4cfe`, unchanged by this seat; pristine
byte copy at `.ufo/waves/round-44/w2/MutC2V2/pristine-c2-counter-v2.py.txt`). 32 single edits (>= 20 required),
each run on the data commit `e46789213830597348fe96a351ae004d10587385` (must stay admitted) and on the ten
rejected controls of `.ufo/waves/round-44/ctl/run-c2-controls-v2.py`, rebuilt in scratch with that runner's own
functions. **Result: 11 killed, 3 equivalent, 18 survived → classified missing control.** No survivor changed
any verdict.

## Method

- Controls rebuilt in scratch (`/fast/scratch/hyaku/mado-r44/MutC2V2/ctl`, deleted at completion) by importing
  `run-c2-controls-v2.py` read-only and driving its own `positive/clone/commit/rd/wr` functions with
  `--repo` = lane, freeze `03fa5c618b089064a657b3d79d3d4272ae4b6894`, base
  `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`: P plus C2-BASE, STAGED-COPY, SHELL, R12-REPOINT, MINIMAL-QUOTES,
  HIDDEN-LINE, FORGED-PIN, FALSE-URL, PROSE-SIZE-REQUEST, ANCHOR-PAST-EOF — each a committed throwaway clone,
  `git rev-parse --show-toplevel` asserted equal to the clone before any commit. Data target: a `--shared
  --no-checkout` clone of the lane scored at `--rev e46789213830597348fe96a351ae004d10587385`.
- Baseline (pristine counter) green on all 12 targets: DATA and P `admitted=1/1` exit 0; the ten controls exit 1.
  Clause isolation observed at baseline: FORGED-PIN fails `d:0` (T1); FALSE-URL `e:0` (T2); PROSE-SIZE-REQUEST
  `h:0` (T3); ANCHOR-PAST-EOF `e:0` (T4); HIDDEN-LINE `g:0` (exemption); SHELL `g:0`+`j:0`.
- Each mutant = one count==1-asserted string replacement on a fresh copy of the pristine counter (exact old/new
  strings in `MutC2V2/mutants.json`; per-mutant sha256 + diff hunks in `MutC2V2/evidence.json`; the mutated line
  numbers below are computed from the pristine bytes, not typed). Run form:
  `python3 -I <mutant> --repo <tree> --rev <rev> --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f`.
- Verdict rule: KILLED if the data commit or P is rejected or any of the ten rejected controls is admitted;
  otherwise SURVIVED, classified equivalent (provably behavior-preserving) or missing control (behavior changes
  on inputs the battery does not contain).

## Result table

Line = `quality/counters/c2-r44-gkeep-size-request-v2.py:<line>` (computed).

| mutant | line | attacks | verdict | evidence |
|---|---|---|---|---|
| m01-t1-digest-drop | 489 | T1 clause-d pin digest | killed | admitted FORGED-PIN (rc 0, all clauses 1, rev 5b7d261c…) |
| m02-t1-path-drop | 489 | T1 clause-d pin path | survived | identical on all 12 targets |
| m03-t1-digest-invert | 489 | T1 clause-d pin digest (sanity) | killed | broke P and DATA rc 1 (`d:0 e:0 g:0 h:0 i:0`) |
| m04-t2-invert | 552 | T2 clause-e+ pin URL | killed | broke P and DATA rc 1 (`e:0`) |
| m05-t2-nop | 552 | T2 clause-e+ pin URL | killed | admitted FALSE-URL (rc 0, all clauses 1, rev 9045a13a…) |
| m06-t2-held-skip | 546 | T2 clause-e+ held ids | survived | identical on all 12 targets |
| m07-t2-hash-drop | 552 | T2 clause-e+ fragment split | survived | identical on all 12 targets |
| m08-t3-guard-drop | 589 | T3 clause-h N0 guard | survived | identical on all 12 targets |
| m09-t3-defaultsize-drop | 592 | T3 clause-h set_default_size | survived | identical on all 12 targets |
| m10-t3-xdg-drop | 597 | T3 clause-h xdg_setSize | survived | identical on all 12 targets |
| m11-t3-x11-drop | 601 | T3 clause-h x11_configure | survived | identical on all 12 targets |
| m12-census-kept | 576 | exact census exemption | survived | identical on all 12 targets |
| m13-census-prefix | 576 | exact census exemption (v1 regression) | killed | admitted HIDDEN-LINE (rc 0, all clauses 1, rev 184ab33c…) |
| m14-census-norm | 576 | exact census exemption (whitespace) | survived | identical on all 12 targets |
| m15-census-atleast | 348 | census exactly-once | survived | identical on all 12 targets |
| m16-census-nop | 348 | census presence | survived | identical on all 12 targets |
| m17-j-window | 376 | clause-j header window | survived | identical on all 12 targets |
| m18-j-upper | 398 | clause-j locator upper bound | survived | identical on all 12 targets |
| m19-j-anchor-multi | 387 | clause-j anchor uniqueness | survived | identical on all 12 targets |
| m20-j-drop-surface | 364 | clause-j surface list | survived | identical on all 12 targets |
| m21-j-found-ignore | 400 | clause-j citation requirement | survived | verdicts unchanged; j:0→j:1 on STAGED-COPY, R12-REPOINT, MINIMAL-QUOTES, SHELL — all still rejected via `g:0` |
| m22-j-case | 395 | clause-j keyword case | survived | identical on all 12 targets |
| m23-j-anchor-absent | 354 | clause-j anchor presence (sanity) | killed | broke P and DATA rc 1 (`j:0`) |
| m24-t3-n0-one | 589 | T3 clause-h N0 guard | killed | admitted PROSE-SIZE-REQUEST (rc 0, all clauses 1, rev 9e88152b…) |
| m25-t4-loose | 567 | T4 anchor range check | killed | admitted ANCHOR-PAST-EOF (rc 0, all clauses 1, rev 63043674…) |
| m26-t4-crash | 566 | T4 anchor range parsing | killed | broke P and DATA rc 1, crash `ValueError: too many values to unpack (expected 2)` |
| m27-t1-held-only | 489 | T1 held ids included | killed | admitted FORGED-PIN (rc 0, all clauses 1, rev 5b7d261c…) |
| m29-j-lookbehind | 392 | clause-j locator word boundary | survived | identical on all 12 targets |
| m31-d-occurrences | 500 | clause-d quote once in receipt | survived | identical on all 12 targets |
| m32-d-cross-receipt | 512 | clause-d quote unique across receipts | survived | identical on all 12 targets |
| m33-census-hyprland-only | 576 | exact census exemption (one line) | survived | identical on all 12 targets |
| m35-t2-basename | 552 | T2 clause-e+ basename-only | killed | admitted FALSE-URL (rc 0, all clauses 1, rev 9045a13a…) |

## Killed — the tightenings' teeth, each proven against a named control

- **T1 digest binding** (clause d, :489): m01 drops the digest test → FORGED-PIN admitted; m27 applies the pin
  test to new ids only → FORGED-PIN admitted. The "held ids included" half of T1 is load-bearing and tested.
- **T2 exact pin URL** (clause e+, :552): m05 neuters the check → FALSE-URL admitted; m35 weakens it to a
  basename comparison → FALSE-URL admitted. The exact-URL form (not basename) is load-bearing and tested.
- **T3 set_size_request rule** (clause h, :589): m24 disables the guard (`N0 == 1`) → PROSE-SIZE-REQUEST admitted.
- **Exact census exemption** (:576): m13 reinstates the v1 prefix exemption → HIDDEN-LINE admitted (all clauses
  1). The exact-two-lines form is load-bearing and tested.
- **T4 anchor range check** (:567): m25 drops the range test → ANCHOR-PAST-EOF admitted.
- Sanity kills (each rejects P and the data commit): m03 (digest test inverted), m04 (T2 comparison inverted),
  m23 (clause-j anchor made absent), m26 (T4 range parsing broken → unpack crash).

## Survivors — classification

**Equivalent (3)** — provably behavior-preserving, not battery gaps:

- **m08-t3-guard-drop** (:589): the `N0 == 0 and` conjunct is dead given the counter's own PINS table. Clause h
  requires gkeep-ui.py among the Gate receipts, and T1 forces any PINS-named receipt to carry the pinned sha256,
  so the census is always computed from the pinned bytes and N0 is always 0 (the pinned gkeep-ui.py has 0
  `set_size_request(` calls; grep of the entry at e467892 finds no `set_size_request(` token anywhere). Removing
  the conjunct cannot change any verdict. The check itself is load-bearing (m24).
- **m12-census-kept** (:576): feeding the two census lines back into the prose scan cannot flip anything — their
  `xdg_setSize`/`x11_configure` values are the computed ones by construction, they contain no
  `set_default_size(`/`set_size_request(` token, and they name no S-id, so clause g is unaffected.
- **m14-census-norm** (:576): exempting whitespace-variants of the census lines adds no hiding channel — a line
  whose normalized text equals a census line carries exactly the census words (no room for extra claim text),
  names no id, and scanning it never contradicts the computed values.

**Missing control (18)** — each is a loosening the ten rejected controls cannot distinguish; the battery, not the
predicate, is the gap. Severity and reproduction per item (reproduction = the mutant's old/new strings in
`MutC2V2/mutants.json`, applied at the named line, run per Method):

1. **HIGH — held-id asymmetry in T2** — m06-t2-held-skip (:546): the location==pin-URL loop restricted to
   `new_ids` leaves a held id's (S164) location unbound to its pin URL. FALSE-URL falsifies S301 (new) only, so
   the battery cannot see it. T1 got a held-id control (FORGED-PIN); T2 did not.
2. **HIGH — T3's default-size prose check untested** — m09-t3-defaultsize-drop (:592): dropping the
   `set_default_size(W, H)` prose check rejects nothing. CritC2Cheat's F5-DEFAULT-SIZE-PROSE forgery (one of the
   four T3 was built to close) has no counterpart control in the v2 battery — the battery dropped F5 when porting
   from the w1 forgery set. The data entry itself contains `set_default_size(420, 500)` on its S301 line
   (entry line 56 at e467892), so a wrong-value prose control is constructible.
3. **MEDIUM — T3's xdg/x11 prose checks untested** — m10-t3-xdg-drop (:597), m11-t3-x11-drop (:601): no control
   asserts a wrong `xdg_setSize=`/`x11_configure=` value in prose; FORGED-PIN recomputes the census line and is
   caught by T1 (`d:0`) regardless.
4. **MEDIUM — clause j never rejects alone** — m21-j-found-ignore (:400): with `found` ignored, the four controls
   that fail j (STAGED-COPY, R12-REPOINT, MINIMAL-QUOTES, SHELL) all still fail `g:0`. No control passes g and
   fails j (surface citations removed while the id-binding lines stay intact), so clause j's citation
   requirement is untested as an independent gate.
5. **MEDIUM — no specific surface is required** — m20-j-drop-surface (:364): deleting the gkeep-id surface from
   SURFACES rejects nothing; the battery never verifies that all twelve (or any one) surface citations exist.
6. **MEDIUM — census exactness/presence untested** — m15-census-atleast (:348, `== 1` → `>= 1`, duplicate census
   lines allowed); m16-census-nop (:348, census presence not required — an entry without the two census lines
   would pass h; SHELL stays rejected via g/j, so h's presence requirement is never isolated).
7. **MEDIUM — exemption granularity** — m33-census-hyprland-only (:576): exempting only the
   `hyprland sendWindowSize` line still admits the data and still rejects HIDDEN-LINE (whose hidden line is
   `gkeep client `-prefixed) — a claim line hidden behind the `hyprland sendWindowSize ` prefix is untested.
8. **LOW — clause j sub-forms untested** — m17-j-window (:376, header lines k < 20 allowed to satisfy j);
   m18-j-upper (:398, locator upper bound dropped — ANCHOR-PAST-EOF tests T4's registry anchor cell, a different
   mechanism, not clause j's own bound); m19-j-anchor-multi (:387, anchor uniqueness relaxed to existence);
   m22-j-case (:395, keyword match case-sensitive — the data entry's twelve citations all match
   case-sensitively); m29-j-lookbehind (:392, locator word-boundary dropped — a glued locator like
   `xgkeep-ui.py:455` untested).
9. **LOW — clause d quote-binding sub-forms untested** — m31-d-occurrences (:500, quote may occur several times
   in its own receipt); m32-d-cross-receipt (:512, cross-receipt quote-uniqueness loop removed — no control
   reuses one quote in two receipts).
10. **LOW — T1/T2 path forms untested** — m02-t1-path-drop (:489, a PINS-named receipt at
    `FETCH/<sub>/<name>` with the correct digest is admitted; clause i's coverage test compares basenames so it
    still counts); m07-t2-hash-drop (:552, the `#`-fragment split dropped; no battery location carries a
    fragment).

## For the L1

- The v2 predicate's tightenings held against single-edit attack: every loosening that admits a rejected control
  was killed. The 18 survivors are control-battery coverage gaps, not predicate holes; per the wave contract this
  is a report, not a re-registration.
- If the L1 wants the battery to carry the gaps, the natural controls are: a held-id FALSE-URL (S164's location
  rewritten), a DEFAULT-SIZE-PROSE forgery (CritC2Cheat F5 port), an xdg/x11 prose mismatch, a census-less entry,
  a `hyprland sendWindowSize `-prefixed hidden line, and a P-variant with one surface citation removed. Controls
  are frozen; this seat only records the gaps.
- Informational, predicate code: the `N0 == 0 and` conjunct at :589 is provably dead given the hardcoded PINS
  table (m08) — harmless; the check itself must stay (m24).

## Integrity

- Lane counter sha256 before = after = `3246d2aa388b6e187a6c5c6176305ec32bda7a58a67fc57f6582e3fd769b4cfe`;
  `git status --porcelain` on the lane shows no modified tracked file — only the new untracked w2 seat files
  (`.ufo/waves/round-44/w2/`). The pristine bytes are preserved at
  `MutC2V2/pristine-c2-counter-v2.py.txt` (sha256 equal to the lane file).
- All mutants were scratch copies; per-mutant hashes and diff hunks in `MutC2V2/evidence.json`; raw per-target
  outputs in `MutC2V2/results.json` and `MutC2V2/baseline.json`; harness script preserved as
  `MutC2V2/harness.py.txt`. Scratch `/fast/scratch/hyaku/mado-r44/MutC2V2` deleted at completion.
- No mutating git/jj anywhere in the lane or fleet; clones and commits only inside scratch with the fixture rule
  (`rev-parse --show-toplevel` asserted). No pacman or package transaction, no host-service or compositor
  mutation, no input injection, no Wayland-client connection; no compositor read was needed.
- Tooling record: no tools installed or updated (python3 stdlib only).

Report: .ufo/waves/round-44/w2/MutC2V2.md
