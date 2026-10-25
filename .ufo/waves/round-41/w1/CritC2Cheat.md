# CritC2Cheat — forgeries against PRED-C2-r41-v1 (round 41, w1)

Seat `CritC2Cheat`. Target: the frozen C2 counter
`quality/counters/c2-r41-focus-entry.py` (clauses a–i). Deliverable:
`.ufo/waves/round-41/w1/CritC2Cheat/forgeries.md` plus the harness, the
tightening checker and three receipts in that directory.

## Result

Nine fixture repos (mktemp -d, `-C D`, toplevel verified before the first
commit, throwaway identity by `-c`; builders imported from
`.ufo/waves/round-41/ctl/run-c2-controls.py`, `main` never run). The frozen
counter **admits all nine** (`admitted=1/1`, exit 0). Eight are fabrications;
the ninth is a GENUINE-PROXY built from the real fetch bytes and the real
journal counts, used to prove each tightening does not reject the genuine set.

```
GENUINE-PROXY                admitted=1/1  tighten_fail=none
F1-invented-receipts-512     admitted=1/1  1 536 forged receipt bytes (3 x 512)
F2-invented-journal          admitted=1/1  4 691 B invented journal
F3-absent-package-paths      admitted=1/1  0 receipt bytes; ADMIT 111 B + REFUSE 118 B name absent files
F3b-space-only-refuse-reason admitted=1/1  109 B line, reason = 24 spaces (0 words)
F4-localized-redirect        admitted=1/1  6 120 B Japanese receipt behind https://t.co/9xQ2fG
F5-shared-boilerplate-quote  admitted=1/1  118 B footer appended to 6 receipts; all quotes are its substrings
F6-one-char-location         admitted=1/1  840 B receipt for https://example.org/confiq.cpp
F7-two-new-ids               admitted=1/1  2 365 B invented receipts; 2 new ids (docstring says >= 3)
FORGE_SUMMARY fixtures=9 admitted=9/9 genuine_proxy_clean=1
```

Receipt: `.ufo/waves/round-41/w1/CritC2Cheat/harness.log` (verbatim above,
plus the single-tightening matrix), `pins.log` (nine `pinned=1` sha256 matches
against `fetch/`), `quotes.log` (`QUOTE_CHECK quotes=6 unique_ok=6/6`).

## Forgery → clause → tightening

| forgery | clause that should have caught it | why it does not | tightening (kept by GENUINE-PROXY) |
|---|---|---|---|
| F1 invented 512-B receipts | d (receipt is the evidence) | d tests `len>=512`, sha, 3–25 words, `quote ⊆ receipt`; no content/provenance check (declared residual) | T1 frozen receipt sha256 pins |
| F2 invented journal | h (own-work saved journal of *this host*) | h parses whatever bytes the Gate line names; names/timestamps/boots unvalidated (declared residual) | T2 own-work receipt = pinned `fetch/xdph-journal.txt` |
| F3 absent package paths | i (assimilation set for the closure) | ADMIT/REFUSE are regex-matched; the staged package is never resolved — **beyond the declared residual** | T3 frozen staged-package allowlist |
| F3b space-only reason | i (`reason=<>=20 characters>`) | `REFUSE_RE` `(.{20,})$` matches spaces (`:90`) — beyond the residual | T3 `len(reason.split()) >= 4` |
| F4 localized behind redirect | i's province guard | four literal substrings on cell 1 only (`:91`, `:312`); redirector and `/jp/` evade; localized bytes live in the receipt | T4 decode+redirector+localization list+ASCII+content type, and T1 |
| F5 shared-boilerplate quotes | d/g (distinct quotes bound to the claim) | `quote ⊆ receipt` only, no cross-receipt exclusivity (declared residual, sharper) | T5 quote occurs in its own receipt and no other cited receipt |
| F6 one-char location | e (no duplicate location) | exact-token equality (`:271`); nothing binds location to receipt — beyond the residual | T6 location segment ⊆ receipt basename, and T1 |
| F7 two new ids | c per the docstring ("at least 3") | code is `len(new_ids) >= 2` (`:225`) — **code ≠ docstring**, beyond the residual | T7 `len(new_ids) >= 3` |

Each tightening is an addition over the counter's own parsers
(`.ufo/waves/round-41/w1/CritC2Cheat/tighten.py`); the matrix shows every
forgery refused by at least one tightening alone and GENUINE-PROXY admitted by
all seven.

## Tightenings rejected as unsafe (evidence)

- edit-distance-1 near-duplicate locations: rejects the genuine
  `Hyprland-FocusGrab.cpp` / `Hyprland-FocusGrab.hpp` pair (one char, `c`→`h`).
- location-basename equality with receipt basename: rejects the repo-prefixed
  fetch names (`fetch/Hyprland-FocusGrab.cpp` vs upstream
  `src/protocols/FocusGrab.cpp`); substring is required.
- subject-token rule (`focus_grab` in every cited receipt): rejects the genuine
  `fetch/xdph-PortalManager.cpp` (0 hits) — the semantic gap cannot be closed by
  a token rule, so it stays the non-author closure's job.
- raising `MIN_RECEIPT`: F1 passes at exactly 512 B; a forger pads (genuine min
  1 903 B).

## Residual after T1–T7

Fabricated bytes and paperwork are closed; the quote→claim binding is not (a
pinned receipt can be real and irrelevant). The freeze remains the trust root: a
forged fetch committed before the freeze is pinned as genuine.

## Files

- `.ufo/waves/round-41/w1/CritC2Cheat/forgeries.md` — full analysis, sizes,
  clauses, tightenings, reproduction commands.
- `build-forgeries.py`, `tighten.py`, `verify-quotes.py`, `forgeries.json`,
  `harness.log`, `pins.log`, `quotes.log` — same directory.

No lane file outside this seat directory was written; no git/jj mutation; no
package transaction; no Wayland/journal verb beyond the read-only reads already
frozen in `fetch/`. Tooling: none installed (python3 stdlib only).
