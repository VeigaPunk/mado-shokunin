# CritEntryOverreach — COMPLETE

Seat: w2 (hyaku run 8, round 43). Target: sentence-by-sentence overreach hunt on
`corpus/knowledge/hyprland-gkeep-geometry-r43.md` at 1959770657f1f8665097c1aed4be6c1cbb07139f
(sha256 `4d16b3fb…`, 80 lines). Freezes read: `registration.md` (b2e2efd6…), `registration-v2.md`
(496340dd…).

## Result

1 material defect + 10 precision/grading defects; provenance clean; C1/C2 verdicts not re-run and
not contradicted.

- **Material (entry line 48)**: "the size rule only acts through the floating algorithm … the rule's
  420x500 is inert" is refuted by `Window.cpp:2402-2408` (non-floating arm of `mapWindow` reads the
  same expression and calls `setPseudoSize`) + `Hyprland-WindowTarget.cpp:197-215` (tiled branch uses
  `m_pseudoSize` when pseudo). "A tiled window never takes this branch" itself holds
  (`floating()` = `m_window->m_isFloating`, `:281-282`), and "the tiler decides the box" holds
  (oracle `nofloat` 918x498).
- **Precision**: L56/row 27 `eval`/`repl` gap; L78 "every read verb"; L36 dot/newline; L34 locator;
  L60 locator; L62 oracle provenance; L62 grade split; row 25 stand-in client; row 28 "tiled".
- **Collateral**: `SKILL.md:270` TILED row repeats the same error (outside my write scope).

Every non-SUPPORTED sentence has exact replacement text in `findings.md`.

## Files (all inside this seat dir)

- `findings.md` — table + replacements + counterexample + impacted axes.
- `verify-quotes.py`, `verify-quotes.txt` — 53 quotes, 0 fails, `VERIFY: PASS`.
- `re2-probe.py`, `re2-probe.txt` — RE2 default-dot probe (`a.b` vs `"a\nb"` → False).
- `provenance-check.txt` — 7 upstream files re-fetched at efb5099 and `cmp`-identical to `fetch/`;
  w1 `window.cpp` pin identical to upstream (sha256 `d735d454…`).
- Trailer report: `.ufo/waves/round-43/w2/CritEntryOverreach.md`.

## Tooling record

`google-re2 1.1.20251105`, channel `uv pip` into
`/fast/scratch/hyaku/mado-r43/CritEntryOverreach/venv`; reason: run the entry's own regex through
the library `RegexMatchEngine.cpp` links rather than assert dot semantics from memory. No pacman, no
host write verb, no input injection, no compositor mutation. Scratch tree deleted at seat end.

## Not done (by assignment)

Counters/controls not re-run; `receipts/c1-after-data.txt`, `c2-after-data.txt`,
`live-geometry-host.txt` read as given. No edit to any frozen or tracked lane file.
