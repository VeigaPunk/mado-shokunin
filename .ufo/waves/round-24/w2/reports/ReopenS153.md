# Reopen S153 — wave-2 reviewer findings

Seat: `MadoR24.ReopenS153` (reviewer, leaf). Lane HEAD: `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (verified with `git rev-parse HEAD`). Assignment: re-open SOURCES row S153, fetch its pinned raw URL, compare sha256/byte count with the row and the committed fetch receipt, confirm the pin resolves, and for each claim row citing S153 (A1) judge (a) quote verbatim, (b) claim true/not overreaching, (c) attribution content rather than generic rule mechanics. No lane file was modified except this report; no git/jj write, no host-state commands.

## 1. Source-row integrity (S153)

Row (corpus/SOURCES.md:165): `Hyprland rule engine implementation — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.cpp`, status `mined`, opened `2026-10-23`, used-by names the note, anchor `src/desktop/rule/Engine.cpp:14-16, 30-47, 54-55 @ efb50993780079460b0cbed1363e2166a2de1d9f; sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6; 1478 B`.

Checks performed:

| Check | Result |
|---|---|
| Fresh fetch of pinned raw URL | `curl -fsSL` OK; sha256 `1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6`, 1478 B |
| Committed fetch receipt `.ufo/waves/round-24/fetch/S153.bin` | sha256 identical (`1ecb7afa…addde6`), 1478 B |
| Row's recorded sha256/size | identical (above) |
| Pin resolves | commit `efb50993780079460b0cbed1363e2166a2de1d9f` exists in read-only clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`; `git show efb509…:src/desktop/rule/Engine.cpp` sha256 = same `1ecb7afa…` (tree bytes at pin equal the row and the receipt) |

The three byte sources (fresh fetch, committed S153.bin, pin's tree) are pairwise identical, and the row's recorded hash matches all three. Anchored lines verified: `registerRule` (14-16), `unregisterRule`/`cleanExecRules` (18-32), `updateAllRules` (34-48), `clearAllRules` (50-52), `rules()` (54-56).

**Source-row verdict: holds.** No integrity defect.

## 2. Claim row A1 (only row citing S153)

Row: `| A1 | The \`registerRule\` implementation appends each supplied rule to \`m_rules\`. | S153 | "void CRuleEngine::registerRule(SP<IRule>&& rule) { m_rules.emplace_back(std::move(rule)); }" |`

### (a) Quote occurs verbatim — holds (per the round's frozen definition)
The quote is not a contiguous byte substring: the pinned file splits it across three lines:
```
void CRuleEngine::registerRule(SP<IRule>&& rule) {
    m_rules.emplace_back(std::move(rule));
}
```
Under the frozen C1 predicate (`registration.md`, `c1/count.py` v2: "occurs verbatim (whitespace-collapsed)"), the collapsed quote is a substring of the collapsed bytes (verified programmatically: `re.sub(r"\s+"," ",src).strip()` contains the collapsed quote at span 279-370). The counter's own check `q in collapse(data)` passes: A1 → PASS_ROW. **Holds under the contract definition; strictly-as-contiguous it does not (newline+indent).** Note only, not a fail, because the frozen predicate explicitly defines verbatim as whitespace-collapsed.

### (b) Claim true of the quoted bytes, no overreach — holds
`registerRule(SP<IRule>&& rule)` performs exactly `m_rules.emplace_back(std::move(rule))` — appends each supplied rule to `m_rules`. The claim asserts no ordering semantics, no uniqueness, no host behavior, no evaluation order. Not overreaching.

### (c) Attribution content rather than generic rule mechanics — fails
A1 states registration/storage mechanics: a rule is appended to the engine's vector. It says nothing about which rule produced an effect, nor about what exposes rule identity (no `rules()` accessor, no name/identity exposure, no effect provenance). It is the *precondition* for the attribution route (the engine holds registered rules centrally), not an attribution statement. By the criterion "which rule produced an effect / what exposes rule identity", A1 does not qualify.

### A1 verdict: **partial** — (a) and (b) hold; (c) fails.

## 3. Counter interaction and impact

- `c1/count.py` at HEAD (offline mode, diagnostic) labels A1 `PASS_ROW`, `PASS_ROW=23`, `distinct_sources=14`, `readme_indexed=True`, `verdict=TARGET_MET`; the wave-1 counted receipt (c1-after-cf86f9e0.txt) reported the same 23/26 in counted mode. A1 passes only the mechanical predicate; the predicate cannot judge semantic support (registration.md explicitly delegates semantic re-reading to wave-2 reviewers).
- If A1 is excluded for failing (c): PASS_ROW=22, still ≥6 from ≥3 distinct sources, so C1's numeric target would still be met. The finding is therefore a row-scope defect (one counted row is not attribution content), not a target reversal.
- S153's `teaches` cell also records `updateAllRules` bulk refresh (`RULE_PROP_ALL` to all eligible windows/layers), which supports the note's *negative* sweep (no per-window attribution record in engine dispatch) — but that content is not what A1 asserts.

## 4. Verdict line

`VERDICT: partial` — S153 source integrity fully holds (pin resolves; sha256/size match row and committed receipt; all three byte sources identical); A1 quote is genuine and the claim is true; but A1 fails the attribution-content criterion (c) — it asserts generic rule registration/storage mechanics, not rule attribution.

## 5. Verification gaps / residual risk

- Counted-mode re-fetch was not re-run in this seat (offline mode used; counted receipt from wave 1 already exists and offline duplicate-` A1's label; counted vs offline differ only in refetch, which I performed manually and equals the recorded hash).
- Host behavior remains `[UNK]` per the note; A1 is a code claim only, so this does not affect it.
- No other claim row cites S153 (verified by grep over the note); A2-A26 are out of scope for this seat.
