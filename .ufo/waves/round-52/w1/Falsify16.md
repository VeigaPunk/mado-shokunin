# Falsify16 — round 52

## Deliverables

- `.ufo/waves/round-52/w1/Falsify16.md` (this report)
- `.ufo/waves/round-52/w1/Falsify16/attack_quote_pin_binding.py` (attack driver)
- `.ufo/waves/round-52/w1/Falsify16/results.txt` (run receipt, full variant output)
- `.ufo/waves/round-52/w1/Falsify16/fixtures/*.md` (7 forged entry fixtures, one per variant)

## Attacked clause

C2 frozen predicate (registration.md): "each maps to an opened-this-round `S###` row, a pin path/revision and exact located quote <=25 words, with a written support rationale". Sub-clauses under attack: (i) the **<=25-word** bound on the located quote, and (ii) the **exact located** property of the quote/pin binding (the locator must identify the lines the quote comes from).

## Method

The round-52 counter does not exist yet at base (that is the point: falsify before construction). The house pattern it will clone is the committed round-51 binding machinery `quality/counters/c2-r51-dispatch-entry.py` (`clause_b`/`bind_row`, lines 329-400: rowid-anchored lines -> LOC_RE locator -> manifest pin -> `git show rev:fetch/pin` bytes -> `at_lines` span -> whitespace-collapsed substring check). I drove that committed code, unmodified, against forged entry texts and **real pinned source bytes** `.ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp` at `HEAD` (== frozen base `85d57a818c3707397e21c840b6498b105ba798aa`, 975 lines). The driver imports the counter module read-only from the lane path, monkeypatches only `MIN_ROWS` (to isolate the per-row binding verdict from the round-51 two-row policy gate; round 52 sets its own proposition-count rule), and prints each variant's forged line, `clause_b` verdict, and the exact quote the matcher bound.

Reproduce:

```
python3 .ufo/waves/round-52/w1/Falsify16/attack_quote_pin_binding.py \
  /home/vgpnk/Projects/shokunin/mado-shokunin <outdir>
```

(`<outdir>` only receives `results.txt` and fixtures; use any scratch dir. The run uses only `git show` reads of the lane repo.)

## Results (from `results.txt`)

- **V0 honest green — as-expected (bound).** Real house-style quote `` `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`(Hyprland-KeybindManager.cpp:785) `` binds at the exact line. Harness is sound and exercises the true committed path (registry row S364 `mined`/`2026-10-27`, manifest pin, real pin bytes).
- **V1 over-length quote + fallback token — BYPASS REPRODUCED.** A fabricated **34-word** paired quote (not present anywhere in the pin file) at an honest narrow locator `:785` still binds, via the unrelated one-word backtick `` `m_dispatchers` `` elsewhere on the line (`matched quote: 'm_dispatchers'`). Root cause: `bind_row` treats `>25 words` as `continue` (filter), not failure, and then tries *every* quoted span on the line as fallback. The <=25-word requirement is not enforced.
- **V2a over-length quote fragments itself — BYPASS REPRODUCED.** A truthful **26-word** paired quote spanning real lines ~798-810 of the pin file binds against locator `:1-975` through an incidental **10-word fragment between the internal double quotes of its own text** (the `DQUOTE_RE` path of `quote_candidates`; `matched quote: ', k->handler); } else { // call the dispatcher Log::logger->log(Log::DEBUG,'`). The paired quote's own length is never enforced even with no separately planted token.
- **V2b whole-file range "locates" anything — BYPASS REPRODUCED.** The same compliant 24-word quote binds against locator `Hyprland-KeybindManager.cpp:1-975`, i.e. the entire 975-line file as haystack. Root cause: `LOC_RE` accepts `:(\d+)-(\d+)` ranges and `bind_row`/`at_lines` never bounds the span width (clamped only by file length).
- **V2c contrast — as-expected (unbound).** The identical 24-word quote at the narrow honest locator `:785` fails `quote_not_at_pin`. This pair (V2b bind / V2c fail) proves the quote lives at lines ~798-810 and that **only the unbounded range "located" it** — the exact-located property is vacuous whenever the cited range spans the file.
- **V2d combined — BYPASS REPRODUCED.** 26-word quote + fallback token + whole-file range binds: both sub-clauses defeated simultaneously.
- **V3 fabricated short quote at honest locator — as-expected (unbound).** The machinery is not trivially broken; fabrication at a narrow locator is still rejected. This also bounds the claim: the bypasses are about length/range discipline, not about the counter accepting arbitrary text.

Reproduced: **yes** for both attacked sub-clauses, against committed source bytes at the frozen base, with 3 independent bypass constructions (V1, V2a, V2b/V2d) plus honest green/red controls.

## Why this falsifies the C2 binding as specified

An entry whose material propositions each carry a 30-word "quote" pinned `file:1-<end>` passes the mechanical binding while violating the frozen predicate on every row. Worse, the fallback means the quote that "verifies" need not be the quote that supports the proposition at all. The round-52 counter, if it clones `bind_row`, admits such an entry; the outside source-truth reviewer would then be reviewing text the counter never actually bound. Required controls for the C2 counter under construction: (1) enforce the paired/primary quote's word count as a **failure**, not a skip; (2) verify only the span paired with the locator (no any-span-on-line fallback, or restrict fallback to an explicit `quote=` scope); (3) bound the cited line range (e.g. reject ranges wider than a small window) or require the quote's first occurrence to start within the cited span; (4) count words with the same tokenizer used to enforce the limit after normalizing internal quote fragmentation (extract backtick spans before `"`/`'` spans, or ignore fragments that are strict substrings of a larger quoted span on the same line).

## Limitations and dissent

- The attack targets the committed r51 binding machinery as the house pattern; the actual r52 counter may already diverge. If C2CounterDraft hardens the three controls above, these specific bypasses close. The falsification stands for "clone-of-r51" designs, which is the documented pre-construction state (registration: "new counter absent").
- Word counts asserted in the driver (26/24/34) are Python `str.split()` counts on whitespace-collapsed text; the counter's own `words()` is identical (`collapse(s).split()`), so no tokenizer discrepancy exists at r51.
- No new external sources were opened; quotes under test were extracted from the already-pinned lane bytes `.ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp` (Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`, per registry row S364), lines 785 and 798-810, accessed 2026-10-27 via `git show HEAD:...` (read-only). No package queries, live reads, probes, screenshots, producer execution, host/config mutation, or source-checkout writes were performed. No installs.
- Scratch `/fast/scratch/hyaku/mado-r52/Falsify16/` was removed after copying receipts into the seat dir.

## Report

- `.ufo/waves/round-52/w1/Falsify16.md`
- `.ufo/waves/round-52/w1/Falsify16/attack_quote_pin_binding.py`
- `.ufo/waves/round-52/w1/Falsify16/results.txt`
- `.ufo/waves/round-52/w1/Falsify16/fixtures/V0-honest-green.md`
- `.ufo/waves/round-52/w1/Falsify16/fixtures/V1-overlength-fallback-token.md`
- `.ufo/waves/round-52/w1/Falsify16/fixtures/V2a-overlength-fragments-itself.md`
- `.ufo/waves/round-52/w1/Falsify16/fixtures/V2b-wholefile-range-binds.md`
- `.ufo/waves/round-52/w1/Falsify16/fixtures/V2c-same-quote-narrow-range-fails.md`
- `.ufo/waves/round-52/w1/Falsify16/fixtures/V2d-overlength-plus-fallback-wholefile.md`
- `.ufo/waves/round-52/w1/Falsify16/fixtures/V3-fabricated-narrow-fails.md`
