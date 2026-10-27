# Falsify08 — C2 source quote/pin binding falsification

## Deliverables

- `.ufo/waves/round-52/w1/Falsify08.md` (this report)
- `.ufo/waves/round-52/w1/Falsify08/receipts/runs.log` (fixture driver transcript: commands, mutations, digests, counter output)
- `.ufo/waves/round-52/w1/Falsify08/receipts/work-{pristine,t1,t2,t2b,t3,t3b,t4}-probe.json` (counter probe records per run)

## Scope and axes

Axes: coverage and operability. Seat target: **C2 source quote/pin binding**. Attacked clause (frozen,
not edited): `claims-frozen.md` C2 — "each material factual proposition maps to a pinned source quote
<=25 words and explicit support rationale"; `registration.md` C2 — "each maps to an opened-this-round
`S###` row, a pin path/revision and exact located quote <=25 words … A counter checks proposition
count, row/pin/quote bindings and index." The attack is against the **binding mechanism** as
instantiated by the only committed implementation of that predicate, the production counter
`quality/counters/c2-r51-dispatch-entry.py` (clause b / `bind_row`), whose house pattern the round-52
counter is being built on. No claim or predicate was edited; no tracked lane file touched.

## Reproducible setup

- Fixture: `git clone /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r52/Falsify08/fixture`
  (HEAD `85d57a818c3707397e21c840b6498b105ba798aa`; `git rev-parse --show-toplevel` asserted to print
  the fixture dir before any fixture git mutation; lane repo itself read-only, uncommitted).
- Baseline digest check: `sha256sum -c .ufo/waves/round-51/fetch/SHA256SUMS` from fixture root →
  20/21 rows OK; sole FAILED row is the manifest's self-row (see hygiene finding).
- Scored command per run:
  `python3 quality/counters/c2-r51-dispatch-entry.py --repo <fixture> --rev <run-commit> --work <seat-workdir>`
- Each mutation was committed inside the fixture clone only (never pushed; fixture deleted after
  receipts were copied to this seat dir).

## Findings — four reproduced bypasses of the quote/pin binding, one red control

All counter outputs below are copied verbatim in `receipts/runs.log` and probe JSONs.

- **B1 — Pin provenance never verified (false provenance admitted). Reproduced: YES.**
  T1: appended one fabricated line to `.ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp`
  (977 lines; the cited span `:785` byte-intact): a seeded comment claiming a nonexistent
  `fabricatedemo` dispatcher registration. After fixture commit: file sha256
  `a4bfeb6ccfdcdad04f2f9efe0b8f264e8d9ef58fd202c11f0fb840ad9addee29` ≠ manifest `8d8f35fc…`;
  `git hash-object` `aaa64c1d…` ≠ recorded `git_blob_sha1` `4ab407ec…`. Production counter at the
  tampered revision: `b ok=1 rows=6/2 pins=6 … admitted=1/1 verdict=TARGET_MET exit=0`. The binding
  verifies the quote against lane-committed fetch bytes at `git show rev:path`
  (`bind_row`/`loader`, counter lines ~341-360) and never recomputes a digest. Repository-wide grep:
  no file under `quality/` references `SHA256SUMS` or `fetch-manifest`; no `c2-*` counter imports
  `hashlib`. The committed manifest pair (`.ufo/waves/round-51/fetch/SHA256SUMS`,
  `fetch-manifest.json` with upstream URLs + revisions + `git_blob_sha1`) is consumed by nobody at
  scoring time. Consequence for C2: a round's fetch bytes may diverge arbitrarily outside the quoted
  spans — or be fabricated outright — while every proposition binding still passes and the
  "independent non-author samples actual source truth" reviewer reads the same tampered copies.
  The frozen phrase "pin path/revision" is satisfied by *declaration*, not *verification*.

- **B2 — Containment, not exactness. Reproduced: YES.**
  T2: line 785 `m_dispatchers.find(` → `m_dispatchers.findex(` (the quoted call target renamed;
  semantics changed). Counter: `admitted=1/1 TARGET_MET`. `bind_row` tests
  `collapse(q) in hay` (counter line ~352) — substring containment — so any mutation that *extends*
  a quoted token keeps the quote "verified". This contradicts the predicate's word "exact".

- **B3 — Degenerate fallback quotes. Reproduced: YES.**
  T2b: line 785 `"mouse"` → `"m0use"` (non-prefix corruption of the quoted span). Counter still
  `admitted=1/1 TARGET_MET`. Instrumentation of the counter's own `bind_row` shows S364 bound with
  quote=`'mouse'` — `quote_candidates` runs `DQUOTE_RE` over the entry line and extracts the inner
  `"mouse"` from the intended backtick quote; when the full quote fails containment, the 1-word token
  still matches `k->mouse` in the corrupted line. A single token satisfies a row's "exact located
  quote" binding.

- **B4 — Disjunctive multi-path binding per row. Reproduced: YES.**
  T3b: corrupted 5 of 6 primary source-line spans non-prefix (`find`→`locate`, `Bad dispatcher`→
  `Bad dispatchex`, `Cannot set submap`→`submep`). Counter still `b ok=1 rows=4/2 admitted=1/1`.
  Cause: `anchored = [l for l in prose if re.search(r"\b%s\b" % rowid, l)]` — every prose line
  mentioning the row id is a binding candidate, and `bind_row` returns the first that verifies.
  S366 re-verified via a callout line quoting `return res.success ? "ok" : res.error;` at
  `Hyprland-HyprCtl.cpp:1157`; S367 via the degenerate token `setSubmap` at `:1664`. Corrupting the
  cited source-line span does not fail the row. (Corollary observed in T3: a failed row reports a
  misleading miss reason — the last unresolvable locator on an unrelated held-ground line —
  because `reason` is overwritten while scanning.)

- **Red control T4 — counter is not a rubber stamp. Reproduced: YES.**
  `git rm` of 5 of 6 pin files → `b ok=0 rows=1/2 miss=…pin_file_absent… clauses_met=3
  admitted=0/1 verdict=TARGET_MISSED exit=1`. B1–B4 are specific defects in what the counter checks,
  not an absence of checking.

- **Hygiene finding (correction design input).** Committed `SHA256SUMS` includes a self-row
  (`.ufo/waves/round-51/fetch/SHA256SUMS` → digest `ab6c7355…`) that can never verify
  (self-referential), while `fetch-manifest.json` claims `"sums_self_row": "none — SHA256SUMS digests
  pins only"`. A digest-checking counter that verifies every row fails closed on this row; the
  self-row must be excluded.

- **Authenticity at base confirmed (exposure, not current corruption).**
  Source candidate: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`
  (same transport recorded in `fetch-manifest.json`), accessed 2026-10-27. Located quote: line 785
  `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`. sha256 of the
  fetched upstream bytes = `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40` =
  pristine fetch bytes = committed manifest digest. Round-51's pins are authentic upstream at the
  pinned revision; the finding is that nothing *enforces* this at scoring time.

## Affected axes and smallest safe correction

- **Coverage (C2):** B1 directly hollows the predicate's grounding — propositions can bind to quotes
  in bytes that never came from the pinned upstream revision, so "grounded in sources opened this
  round" degenerates to "grounded in bytes a lane seat committed". B2–B4 weaken each proposition's
  "exact located quote" binding independently.
- **Operability:** a counter that admits B1 fails its no-work-control duty in spirit: a control
  fabricated from self-sealed bytes would pass the same way the production entry does. T4 shows the
  floor works, so the correction is additive, not a rewrite.

**Smallest safe correction** (for `C2CounterDraft` before the counter is frozen; none of this amends
the frozen predicates, it implements them):

1. **Provenance:** for each pin a proposition binds, recompute sha256 of the pin file at the scored
   revision and compare to the round-52 committed fetch manifest (self-row excluded); fail closed on
   missing manifest or mismatch. Optionally also require `git hash-object` == recorded
   `git_blob_sha1`. Source-only, deterministic, no network at scoring time.
2. **Exactness:** verify the paired quote against the cited span by exact normalized match
   (whitespace-collapsed whole-span equality or word-boundary-anchored containment) — never raw
   `substring in haystack`; no fallback to shorter sub-spans; one authoritative quote per
   proposition; keep the ≤25-word cap and add a ≥4-word floor so single tokens cannot be "quotes".
3. **Path:** bind a proposition only at the locator on the line that names its `S###` row, not at any
   prose line mentioning the row id.

## Risks, dissent, and limitations

- The round-52 C2 counter did not exist at test time; B1–B4 are demonstrated against the production
  round-51 counter, the canonical committed implementation of the same frozen binding predicate.
  The exposure claim is predicate-level: neither `claims-frozen.md` nor `registration.md` compels
  the new counter to close B1–B4, so without the correction above the new counter can inherit all
  four holes and still meet its frozen text. This is the gap this seat was dispatched to name before
  scoring.
- Fixture-state chaining: T2's commit built on T1's committed file (both mutations present); this
  does not change B2's result (the `:785` containment check accepted `findex` with the manifest
  already mismatching) but is disclosed for exactness. T2b/T3b/T4 each reset to pristine base first.
- B4's dilution interacts with the predicate floor ("at least four substantive propositions"):
  per-proposition corruption can hide under the floor plus callout fallback paths.
- T3's misleading miss reason (`pin_unmapped:keybind-rule-semantics.md` masking a real
  `quote_not_at_pin`) is a diagnosability wart, not a pass/fail defect; recorded for the record.
- No installs (no tool needed beyond stock git/python3/curl). Scratch fixture and workdirs under
  `/fast/scratch/hyaku/mado-r52/Falsify08/` were removed after receipts were copied to the seat dir;
  the only writes under the lane root are this report and its receipt copies, as assigned. No
  package queries, live reads, probes, screenshots, producer execution, or source-checkout writes.

## Evidence

- `quality/counters/c2-r51-dispatch-entry.py` lines ~279-356 (`resolve_pin`, `quote_candidates`,
  `bind_row` containment test, `anchored` line selection, `MIN_ROWS` floor) — local repository evidence.
- `.ufo/waves/round-51/fetch/fetch-manifest.json` (upstream URLs, revisions, `git_blob_sha1`,
  `"sums_self_row": "none"`) and `SHA256SUMS` (self-row present) — local repository evidence.
- `.ufo/waves/round-52/receipts/c2-base.txt` — pristine counter baseline reproduced.
- `.ufo/waves/round-52/claims-frozen.md` C2 and `registration.md` C2 — attacked clauses (local evidence).
- Seat receipts: `receipts/runs.log`, `receipts/work-*-probe.json` (seven runs: pristine, T1, T2,
  T2b, T3, T3b, T4) — local seat evidence.
- External source candidate: raw.githubusercontent Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f`
  `src/managers/KeybindManager.cpp`, accessed 2026-10-27, sha256
  `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40`, located quote at line 785
  `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`.

## Report

- `.ufo/waves/round-52/w1/Falsify08.md`
