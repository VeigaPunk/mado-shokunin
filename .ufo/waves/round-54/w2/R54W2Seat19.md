# R54W2Seat19 — C1 P22 miss-branch entailment

Axes: **coverage** (whether source-backed proposition meaning is actually covered) and **operability** (whether the record instrument verifies only the frozen contract).

## Finding: “key not found” is narrowly a cache-miss scan failure, not an unqualified key-resolution failure

The frozen claim describes P22 as: “When key resolution leaves `keycode` unset after the scan, `sendshortcut` returns the `key not found` error from its cache-miss branch” (errata entry, P22 row). Its frozen quote and location are explicitly fixed at registration.md:30, and claims-frozen.md:22-28 requires the quote be verbatim/contiguous in the named pin and the anchor side-claim at `DispatcherTranslator.cpp:573-574 after line 571` hold. Reading the adjacent source exposes the qualifier the proposition correctly includes but a shortened assertion could lose: this error return is reached only in the key-name cache-miss branch after the scan, not for all unsuccessful key resolution.

Exact pinned source (`.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp`, pinned span):
- 531-534: `sendshortcut`; invalid argument count returns `sendshortcut: invalid args`.
- 540-548: numeric keycode, `code:` and `mouse:` key forms are resolved separately; low mouse button value returns `invalid mouse button`.
- 549-555: key-name resolution; absent keyboard returns `no kb`.
- 559-572: only if `m_keyToCodeCache` lacks `KEYPAIRSTRING`, scan `keycode_min..keycode_max`, setting `keycode`/cache on matching keysym; loop ends at 571.
- 573-574: `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};`.
- 575-580: cache-hit alternative assigns cached keycode; a subsequent, distinct `if (!keycode)` returns `sendshortcut: invalid key`.
- 582-586: nonempty window selector without a window returns `window not found`.

This supports the exact bounded P22 proposition: an unset keycode *after that scan* takes the specific miss-branch error. It does not entail a blanket claim such as “any key-resolution failure returns key not found”: no keyboard, invalid numeric/mouse inputs, cache-hit invalid key, invalid args, and missing window are distinct paths/messages. The keyword “after the scan” and “cache-miss branch” are material limitations, not optional prose.

## W1 relationship and execution status

The assigned W1 report `w1/R54Seat19.md` is absent in the lane (read returned `Path ... not found`). W1 results record R54Seat19's own item as a different, unrelated `--rev` success-line identity concern (w1-results.json:116-119); I do not attribute that report's contents to this P22 semantic review. Relevant corroboration: `w1/R54Seat34` notes the actual P22 anchor is 573-574 and scan closes at 571 (w1-results.json:208-209); `w1/R54Seat04` says the P22 side-claim is “after 571” (w1/R54Seat04.md:72-77). Separately, W1 reports repeatedly identify literal quote-byte/normalization ambiguity; that is not the semantic entailment question tested here.

The pinned C1 counter is absent: `glob quality/counters` showed no `c1-r54-errata-truth.py`; read of its exact path returned not found. Therefore the frozen invocation `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` was **NOT RUN (absent)**. No fixture or source mutation was made; this was a read-only inspection.

## Smallest safe correction

Preserve the existing scope whenever P22 is repeated or summarized: explicitly state “key-name cache-miss scan leaves `keycode` unset” and avoid generalizing to all key-resolution failures. No predicate/registration edits are proposed; if the pinned counter later checks only quote/anchor identity, semantic interpretation remains a separate review concern, not an implementation result.

## Trailer — commands and outputs

All paths below are relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`.

- `read .ufo/waves/round-54/claims-frozen.md` — output lines 22-28: C1 quote, anchor, and pin obligations; exit 0.
- `read .ufo/waves/round-54/registration.md` — output lines 25-34: P22 quote/anchor and side-claim `573 > 571`; exit 0.
- `read .ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp:500-562` and `:560-585` — output source spans summarized above; exit 0.
- `grep P22 corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` — output P22 proposition/qualifier: “When key resolution leaves `keycode` unset after the scan” and “cache-miss branch”; exit 0.
- `glob quality/counters` — no `c1-r54-errata-truth.py`; exit 0.
- `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa` — NOT RUN: counter absent, confirmed by glob and exact-path read (read output: `Path .../quality/counters/c1-r54-errata-truth.py not found`).
- Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat19` created and removed before yield; no scratch remaining. No installs.
