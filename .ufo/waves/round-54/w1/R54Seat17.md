# R54Seat17 — C1 adversarial attack (item 17)

Axes: **operability** (PRED-C1-r54 errata source-truth verifier) and the
**integrity of the coverage claim it certifies**. Attacked predicate: the frozen
PRED-C1-r54 sentence (claims-frozen.md:20-30) and its six frozen controls
(registration.md:42-47), plus the §9 do-nothing control (claims-frozen.md:41-44).
Predicate unchanged; no lane edits; attack run at lane HEAD = base
`e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (no r54 counter landed yet — w1
executors in flight — so the attack is against the frozen contract itself,
exercised through reference implementations over byte-verified pin copies).

## Findings by severity

### HIGH — F1: the do-nothing counter reaches the target on every mechanically judged surface

The §9 sentence (claims-frozen.md:41-44) says an always-print counter "fails the
six control runs … an always-print counter accepts them → `controls<6/6`". That
rejection is **procedural, not mechanical**: the only surfaces the round's
artifacts define are (i) the frozen line + exit 0 at the scored revision, (ii)
committed per-control receipts ("the counter's own control run is committed per
control"), (iii) a self-reported `--selftest ≥ 30 assertions` (registration.md:50),
and (iv) w2's re-run of "both counting commands" — which re-runs at the honest
tree, exactly where the do-nothing counter's output is indistinguishable from an
honest counter's. A counter that reads no git objects satisfies (i) exactly; (ii)
and (iii) are plain text the same author fabricates; (iv) cannot catch always-MET.
Only an out-of-band grader constructing the six mutated trees itself and re-running
the landed counter per tree rejects it — a procedure the predicate sentence does
not contain, and the registration nowhere binds receipts to the counter's bytes or
to mutated-tree commit ids.

Executable reproduction (run at base; output verbatim):

```text
$ python3 -I do_nothing_c1.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
```

`do_nothing_c1.py` is 6 lines: parse `--repo/--rev/--work`, print the frozen line,
`sys.exit(0)` — zero git access. It prints the exact frozen target line at the
base revision. Smallest mechanical closure (recommendation only): grader-owned
control battery — the grader derives the six mutated trees from the registration
table (mutations are fully specified there), runs the landed counter per tree,
requires `TARGET_MISSED` + non-zero exit, and requires each committed receipt to
carry the counter blob hash and the mutated tree id it claims to record.

### HIGH — F2: the frozen judge-of-"verbatim" sentence is three-valued; one reading kills the honest tree, another admits whitespace-forged quotes, and no frozen control distinguishes them

registration.md:51-53 operationalizes clause (a) "occurring verbatim and
contiguous" (claims-frozen.md:24) as: *"exact byte contiguity after single-space
normalization of interior newlines ONLY where the frozen quote itself carries a
newline (P19/P21/P22 are single logical lines)"*. The parenthetical is factually
wrong about its own fixture: per the frozen anchors themselves (claims-frozen.md:25-28),
P19 spans pin lines 1554–1558, P21 spans 619–622, P22 spans 573–574 — only **P20**
is a single logical line. The committed entry stores P19/P21/P22 as single logical
lines (entry rows 17–20), while the pin bytes carry newline + indentation at every
join (byte dump below). Three contract-conforming readings of the judge sentence
therefore exist:

- **A literal**: interior `\n` → ` ` only, every other byte verbatim. The honest
  P19/P21/P22 quotes do NOT occur (pin joins are `\n` + 4/8/12/16 indentation
  spaces; the quote has exactly one space) → honest tree = quotes 1/4 =
  **TARGET_MISSED at the honest target** — the kill rule fires although every
  frozen fact is true (pins hash-verified, anchors byte-confirmed). Predicate
  unreachable as written.
- **B run-collapse**: `\s+` → ` ` on both sides. Honest tree verifies, but any
  quote differing from the pin only inside whitespace runs is admitted — a clause-(a)
  "verbatim" violation that prints `quotes=4/4 … TARGET_MET`.
- **C join-indent**: `\n\s*` → ` ` on both sides. Honest tree verifies and the
  forgery is rejected — but nothing in the frozen sentence selects C over A or B.

The six frozen controls reject under **all three** readings (matrix below), so the
control battery cannot select the intended semantics: a B-implementing counter
prints `verdict=TARGET_MET` with `controls=6/6` while accepting quotes that do not
occur verbatim. The freeze underdetermines its own verifier. Per the freeze rule
(claims-frozen.md:5-7) the fix is a pre-data re-registration (claims-frozen-v2)
pinning the normalization (C) and adding a whitespace-forgery control, e.g.
C1-CTL-7: P20 quote `…sendKeyboardMods(0,  0, 0, 0);` (double space) must be
rejected.

Byte evidence (cat -A; `$` = end of line) — pin copies verified against the
committed SHA256SUMS first (`sha256sum -c SHA256SUMS` → all `OK`):

```text
== Hyprland-ConfigActions.cpp 1553-1559 ==
$                                              <- 1553 blank
    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);$   <- 1554
$                                              <- 1555 blank
    if (S.m_passPressed == 1) {$               <- 1556
        if (!isMouse)$                         <- 1557
            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);$  <- 1558
```

== DispatcherTranslator.cpp 618-623 / 571-576 == same shape: blank line 620,
indentation 4/8 spaces at the P21 joins, 12/16 spaces at the P22 join (573-574).
Entry quote cells (entry rows 17,19,20) join these with single spaces.

Attack input (whitespace-forged entry, P20 cell): 
`g_pSeatManager->sendKeyboardMods(0,  0, 0, 0);` (double space; pin has single)
plus double-space joins in P19. Under B this prints MET; under A and C MISSED.

### LOW — F3: registration pin-manifest filename drift

registration.md:12 says the round-52 pins' hashes come from "its committed
`SHA256SUMS.txt`"; the committed file is `.ufo/waves/round-52/fetch/SHA256SUMS`
(no `.txt` — claims-frozen.md's causal-separability note names it correctly as
`(+SHA256SUMS)`, claims-frozen.md:81; round-54's own manifest IS `SHA256SUMS.txt`,
so only the C1 inventory drifts). A
counter written literally to the registration's C1 inventory looks for
`SHA256SUMS.txt`, finds nothing, and fails the pins leg on the honest tree — a
second false-kill trap alongside reading A. CTL-3 ("the tree's SHA256SUMS",
registration.md:44) is name-ambiguous for the same reason.

## Executable reproduction — reference-checker matrix

Method: reference checker `ref_check.py` (scratch, 110 lines) parses the P19–P22
rows from an entry file, finds the quote's line span in byte-verified pin copies
under normalization A/B/C, compares the found span against the entry-named anchor
plus the frozen side-claims (P19 1554-1558; P20 1576; P21 619-622 ∧ 591≤619∧622≤627;
P22 573-574 ∧ 573>571), recomputes pin sha256 against `SHA256SUMS`, and prints a
ref-labeled leg line. Entry variants: honest (base commit, via
`git show e25149fe:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`),
whitespace-forged, and CTL-1/2/5/6 mutations per the registration table.

```text
$ cd /fast/scratch/hyaku/mado-r54/R54Seat17/work
$ for m in A B C; do for e in honest forged-ws ctl1-splice ctl2-anchor ctl5-drop ctl6-pin; do
    python3 -I ref_check.py --mode $m --entry entry-$e.md --pins . ; done; done
```

Summary lines (verdict + leg arithmetic; full 19-run output observed):

| input | A literal | B run-collapse | C join-indent |
|---|---|---|---|
| honest base entry | `quotes=1/4 TARGET_MISSED` exit 1 | `4/4 TARGET_MET` exit 0 | `4/4 TARGET_MET` exit 0 |
| whitespace-forged | `0/4 TARGET_MISSED` | **`4/4 TARGET_MET` (false pass)** | `2/4 TARGET_MISSED` |
| CTL-1 splice | MISSED `1/4` | MISSED `quotes=3/4` | MISSED `3/4` |
| CTL-2 anchor :1575 | MISSED (span found at (1576,1576) ≠ entry's 1575) | MISSED `3/4` | MISSED `3/4` |
| CTL-5 drop P22 | MISSED `propositions=3/4` | MISSED `3/4` | MISSED `3/4` |
| CTL-6 pin → KeybindManager.cpp | MISSED (quote not found there) | MISSED `3/4` | MISSED `3/4` |

CTL-3 (hash nibble) and CTL-4 (P21 anchor → :573) exercise the hash leg and the
entry-vs-found anchor comparison respectively — both legs are normalization-independent
by construction and are exercised live by the `pins=4/4` leg (hash compare against
committed sums, `sha256sum -c` OK on the same copies) and the CTL-2 rows above;
I did not run separate CTL-3/CTL-4 fixtures — flagged as a coverage gap, not a run claim.

## Distinctness

Sibling w1 reports landed so far (Seats 10-13, 22, 23, 36) all attack C2
(quote-scope overclaim, host-join distinctness/aliasing, wrong-commit, index/provenance).
No sibling attacks C1; my inputs — do-nothing reachability on the judged surface,
whitespace-run forgery inside the judge sentence, `SHA256SUMS` name drift — are
distinct from the registered C1 control set and from each other.

## Residual risk and verification gaps

- No r54 counter existed at attack time (HEAD = base, w1 in flight); F1/F2 are
  demonstrated against the frozen contract via reference implementations over
  pin copies byte-verified against the committed SHA256SUMS. A landed counter
  should be re-attacked against the same matrix (w2's mandate).
- F1's severity depends on grader behavior not specified in the frozen files; if
  L1's scoring harness re-executes the six mutated trees itself, the do-nothing
  counter is caught and F1 reduces to "receipts are unbound self-attestation".
- CTL-3/CTL-4 not run as separate fixtures (reasoning + partial live coverage above).
- No tool installs or updates were made (nothing beyond stock python3/git/coreutils;
  RULES.md read pre-task as required).

## Bounds

Writes: this report + `/fast/scratch/hyaku/mado-r54/R54Seat17/` (cleaned before
yield). No lane, fleet, sibling, or source-repo writes; no git/jj mutations in the
lane (read-only `rev-parse`/`show`/`cat-file` only; no fixture commits needed);
no host/config/service/compositor reads; static committed pins only.
