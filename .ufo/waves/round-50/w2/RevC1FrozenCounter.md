# RevC1FrozenCounter — mado round 50 w2 (FALSIFY), seat report

Target: frozen counter `quality/counters/c1-r50-bind-entry.py` (PRED-C1-r50) and its data receipt.
Counter bytes verified: `git show 470bfd77:quality/counters/c1-r50-bind-entry.py | sha256sum`
= `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0` — identical at tip
`b4a79843` and equal to the registration's frozen hash. Seat dir:
`.ufo/waves/round-50/w2/RevC1FrozenCounter/`.

## Verdict: NO C1 KILL. Receipt + controls reproduce exactly; clause predicates all present in
code and match the published vector. ONE documentation defect (registration conflates two
counters' clause g) and ONE counter-code residual (F1 repair is incomplete on the
quote-locator path; a bare numeric band like `0:23` written as a quote locator still
resolves to a pin and can kill a true entry).

## Reproduced runs (clone `git clone -q --shared` at seat scratch, TMPDIR under scratch)

| run | rev | result | receipt |
|---|---|---|---|
| data run 1 | `906178b6…` | `clauses=a:1…r:1 admitted=1/1 verdict=TARGET_MET` rc=0 | `receipts/data-run1.txt` |
| data run 2 | `906178b6…` | byte-identical output modulo none (same bytes) | `receipts/data-run2.txt` |
| base | `8ae47b95…` | `a:0 admitted=0/1 TARGET_MISSED` rc=1 (entry_absent, short-circuit) | `receipts/base-run.txt` |

`diff` of the counter-emitted lines of `receipts/data-run1.txt` vs the pinned
`.ufo/waves/round-50/receipts/c1-at-data.txt` → **IDENTICAL** (every `PRED` line; the lane
receipt appends a harness `exit=0` trailer after the predicate sentence — its counter-final
line is the exact TARGET_MET sentence, kill rule satisfied).

## Clause-code map (all located, predicate verified against printed vector)

| clause | code | what it scores | receipt evidence |
|---|---|---|---|
| a | `score()` ~1173–1179 | entry present at REV, absent at BASE (precondition exits 2 otherwise) | `clause=a entry_absent` at base |
| b | `score()` ~1180–1248 | ≥3 head `source:` ids ≥S352, single 11-cell mined row each, `verified-at`/single `recheck`, no provenance outside head window, no ghost `S###`, README index row | `clause=b ids=10 … ok=1` |
| c | `clause_c` :488 | each head row sha256-binds a round-50 fetch pin; URLs carry frozen refs only; anchor ranges resolve to the row's own pins | 10 `clause=c id=S35x` lines, pins + ranges per row |
| d | `clause_d` :562 (+ `locators` :335, `QUOTE_RE` :578) | every quote with a locator occurs verbatim in a cited pin inside [a,b]; out-of-pin/uncited-pin locators fail | `clause=d quotes=85`, no failures |
| e | `clause_e` :611 | ≥6 `N.` steps, each with a locator-verified quote (bytes, not just range) | `clause=e steps=17 verified_steps=17` |
| f | `clause_f` :726 | the pinned receipt exists (100644, 512B–256KiB, absent at base), is shape-only, and the entry restates total/forms/digest/resolve | `clause=f receipt=…binds-live-r50.txt binds=192 forms=named:142,code:42,mouse:6,switch:2` |
| g | `clause_g` :815 | held S319 row byte-equal base↔rev, its round-46 pin digest recorded, entry cites S319, no new row re-registers its (repo,ref,path) | `clause=g held=S319 unchanged=1 pins=1 held_urls=1` |
| h | `clause_h` :928 | `## Limits` ≥3 bullets, ≥2 scoped words | `clause=h bullets=8 scoped=8` |
| i | `clause_i` :977 | lesson `## Gate` names every new ≥S352 row; each new row used by a new file; GROUND terms absent at BASE, ≥2 at REV; body-dup ≤5/40 and shingle overlap <0.15 | `clause=i new_rows=12 gate=1 ground_present=2/4 body=62 dup=0 overlap=0.013` |
| j | `clause_j` :885 + `TOPICS` :871 | each of 7 source-line topics covered by a step quote at a matching pin line | 7 `clause=j topic=… line=…` |
| r | `clause_r` :1123 (+ `live_binds` :1068) | live `/usr/bin/hyprctl binds -j` + `getoption` replay equals receipt's digest/total/forms/resolve | `clause=r replay=ok sha=9a47199e2297 binds=192` |

The published vector `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1` is exactly what the code
computes at `906178b6` (twice, identical), and `a:0` at base matches control `c00`.

## F1 attack (clause d numeric band)

`locators()` :335 has the round-50 repair: a token whose basename has no `[a-z_]` is not a
locator (skips `0:23`, `1:2`, `sha256:…`). Demonstrated: mutant **M1** appends
`Histogram sanity: modmask_histogram | 0:23, 1:2, 2:0 of 192 binds.` to the entry at
`d4ea328f` — all three numeric bands skipped, `d:1`, TARGET_MET (`receipts/mutant-M1.txt`).

**Gap found (residual, not a kill):** the three QUOTE_RE consumers re-resolve locator
tokens WITHOUT the `[a-z_]` guard — `clause_d` :590, `clause_e` :635, `clause_j` :910 each
call `resolve_pin(token.rsplit(":",1)[0])` on whatever group 3 captured. `resolve_pin`
stem-containment maps `0` → `binds-live-r50.txt` (only pin whose stem contains "0"; `2`,
`5`, `6` → `SHA256SUMS`; measured against the 16 committed pins). So a quote written as
`"bins at zero" (0:23)` — a histogram band next to a quote — is still parsed as a locator.
Mutant **M2** adds exactly that line at `5d5e062f`: `clause=d quote_not_in_pin
line=136 pin=binds-live-r50.txt q='bins at zero'` → `d:0` TARGET_MISSED
(`receipts/mutant-M2.txt`). In the plain-locator path the same `0:23` is skipped (M1).
Impact: an entry that cites a quoted span and follows it with a numeric-band parenthetical
loses admission falsely — the F1 repair covers bare locators but not quote locators.
Direction is fail-closed (misses, never admits), so it cannot launder a bad entry; it can
only wrongfully MISS. Same gap exists in clause_e (a numbered step's quote with `(0:23)`
would lose its verified quote) and clause_j.

## f/r RECEIPT_NAME pin attack

`RECEIPT_NAME = ^binds-live-r50\.txt$` (:203) filters `cand` basenames at :737 (f) and
:1134 (r). Mutant **M3** `git mv`s the receipt to `binds-live-r50.txt.bak` at `897e48e7`:
`clause=f receipt_missing` → `f:0`, `clause=r no_receipt_found` → `r:0`, rest pass
(`receipts/mutant-M3.txt`). The pin rejects any other name; the entry's cited path must be
exactly the frozen name. Note S361's row is unaffected (its pin lives under `fetch/`, so
`c:1` stands — receipt naming is policed only by f/r, consistent with the docstring).

TMPDIR hardening verified: unset → `SETUP TMPDIR required for replay scratch` (rc 2);
`TMPDIR=/tmp` → refused; `TMPDIR` inside the scored repo → refused (all three observed).

## Clause g / "150 generated cases" / the two-nonce gap

**The frozen C1-r50 counter contains no sampling and no nonce.** `grep -n "nonce|random"`
over the counter is empty; `main()` (:1290) takes only `--repo/--rev/--base`. Clause g is
the deterministic held-S319 comparison above. Two same-rev runs are byte-identical
(receipts). Nothing varies run-to-run; nothing a nonce could change exists.

The `150 generated cases` machinery belongs to the round-49 C1 counter
`quality/counters/c1-r49-keysym.py` (`GEN = 150`, `grng = random.Random(nonce)`, `--nonce`
defaulting to `os.urandom`) — which is what w1/RevC1Counter reviewed (its report quotes
`g generated=150/150` and flags "two-nonce requirement remains a verification gap"). The
C2-r50 counter independently seeds `random.Random(args.nonce)` and derives fixture counts
`k_red = 40 + nonce%5`, `k_green = 40 + (nonce//7)%5` — there the case sets differ run-to-run
exactly when the nonce differs (50117 → 42 red/44 green; 778899 → 44/41, matching the
published receipts), i.e. deterministic per nonce, varied across nonces.

**Defect (documentation):** `registration.md:23` claims the C1 data receipt "covers the
w1/RevC1Counter two-nonce gap in that clause g's 150 cases are generated and judged at
count time inside the single run". For the frozen C1-r50 bytes this is false: its clause g
generates zero cases and accepts no nonce, so a single TARGET_MET run cannot "cover" a
two-nonce property that does not exist in this counter. The sentence conflates
`c1-r49-keysym.py`'s clause g (GEN=150, nonce-seeded) with `c1-r50-bind-entry.py`'s clause g
(held-row check). Residual risk: a reader trusting the registration believes C1 was scored
under adversarial sampling; it was not — C1's admission rests on deterministic byte checks
plus the live-socket replay (the declared residual). Recommendation to L1: correct the
parenthetical (or route the two-nonce closure to the counter that actually has the
machinery); the C1 claim itself is unaffected — the receipt and every control reproduce
under the frozen bytes.

## Findings by severity

1. **LOW–MED (counter code):** F1 numeric-band guard not applied to QUOTE_RE locator paths
   (clauses d/e/j); `0:23` post-quote still resolves to `binds-live-r50.txt` and MISSES a
   true entry. Fail-closed; cannot admit a bad entry. Evidence: mutant-M2.txt.
2. **LOW (registration docs):** registration.md:23 attributes nonce-seeded 150-case
   sampling to C1-r50's clause g; the frozen counter has no such machinery. Claim not
   affected; coverage claim about "the two-nonce gap" is unsupported by this receipt.
3. **NIT (kill-rule literalism):** pinned `receipts/c1-at-data.txt` appends `exit=0` after
   the predicate sentence; the sentence is the last counter-emitted line, satisfied in
   substance.

Supports, not attacks: all published receipts reproduce; controls' vectors match code
(c00 `a:0` early-exit observed); frozen sha256 verified at 470bfd77 and tip.

## Deliverables (all under this seat dir / this file)

- `receipts/data-run1.txt`, `receipts/data-run2.txt`, `receipts/base-run.txt` — re-runs.
- `receipts/mutant-M1.txt` — histogram tokens in body, still MET (F1 holds on locators()).
- `receipts/mutant-M2.txt` — quote `(0:23)` MISSES (F1 gap on QUOTE_RE path).
- `receipts/mutant-M3.txt` — renamed receipt → `f:0 r:0` (name pin holds).
- Fixture clones: `fix-M1`/`fix-M2`/`fix-M3` under seat scratch (deleted after copy-out).

No tools installed (none needed). No lane/fleet writes; all git mutation confined to
scratch fixture clones (toplevel asserted per clone).
