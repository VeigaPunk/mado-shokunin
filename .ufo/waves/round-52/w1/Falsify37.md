# Falsify37 — C2 source proposition entailment

## Deliverables

- `.ufo/waves/round-52/w1/Falsify37.md` — this report
- `.ufo/waves/round-52/w1/Falsify37/pred-c2-r52-frozen.py` — checker implementing the frozen C2 checkable predicates; quote-binding half reuses the lane's production binding code (`quality/counters/c2-r51-dispatch-entry.py`) unmodified
- `.ufo/waves/round-52/w1/Falsify37/fixture-entry.md` — adversarial entry (byte-copy of the fixture's committed blob)
- `.ufo/waves/round-52/w1/Falsify37/fixture-README.md` — fixture README carrying the index row
- `.ufo/waves/round-52/w1/Falsify37/rebuild-fixture.sh` — rebuilds the two-commit fixture repo from lane base `85d57a8` + the two seat-dir copies; prints both revs
- `.ufo/waves/round-52/w1/Falsify37/run-rev.out` — checker output at the fixture rev (TARGET_MET)
- `.ufo/waves/round-52/w1/Falsify37/run-base.out` — checker output at the fixture base (control: TARGET_MISSED)
- `.ufo/waves/round-52/w1/Falsify37/pred-c2-r52-frozen.json` — probe record for the rev run

## Target/predicate attacked

C2 (coverage), `claims-frozen.md`: "each material factual proposition maps to a pinned source quote <=25 words and explicit support rationale", as enforced by "a new committed counter checks proposition count, row/pin/quote bindings and complete mapping", under the claim's own disclaimer "This is not automated semantic-entailment proof", with the sole entailment defense "an independent non-author samples actual source truth" (sampling, outside the counter verdict, no bound on sample coverage in the frozen text).

**Attack:** the checkable predicate set verifies quote *presence* — a verbatim, whitespace-collapsed substring of the pinned bytes at the cited line — never quote→proposition *support*. A proposition that its own pinned quote contradicts passes every checkable clause. Two bypasses demonstrated with one fixture:

- **B1 (declared-but-contradicted):** four declared propositions, each with a real mined row, a real pin at the revision, a real ≤25-word quote verbatim at the cited line, and a plausible written rationale — all four false against the pinned bytes.
- **B2 (undeclared claim):** "every material factual proposition is mapped" is enumerable only over *declared* propositions without semantics; a fifth material claim asserted in the entry prose, absent from the proposition table, is invisible to the complete-mapping check.

## Fixture

Two-commit git repo built in seat scratch from the frozen lane base (read-only `git archive` of `corpus` + `.ufo/waves/round-51/fetch` at `85d57a818c3707397e21c840b6498b105ba798aa`):

1. base commit: pristine base snapshot (entry absent);
2. rev commit: adds `corpus/knowledge/hyprland-dispatcher-entail-bypass-r52.md` (fresh prose; `source:`/`held:`/pin-manifest lines copied verbatim from the real round-51 entry at base, so every row/pin/quote binding is real) plus its `corpus/README.md` index row.

The entry declares four propositions in a `## Propositions` table (`id | proposition | row | pin | quote | locator | support rationale`), the round-52 mapping shape.

## The four propositions and their pinned contradictions

All quotes verified verbatim at the cited lines of the pinned bytes (Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f`, fetched round 51, accessed 2026-10-27; URLs in `corpus/SOURCES.md` rows S364/S366-S368 at base). Checker verdict and production cross-check (`prod_bind=ok` = the lane's own `bind_row` bound the line) from `run-rev.out`.

| P# | proposition (as declared) | quote (words) | row/pin/locator | why the pinned bytes contradict it |
|---|---|---|---|---|
| P1 | The socket dispatch path validates the requested dispatcher name against the translator's inner implementation table before calling anything. | `m_dispatchers.find(DISPATCHSTR)` (1) | S366 / `Hyprland-HyprCtl.cpp` / :1149 | The full pinned line is `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);` — the **outer** KeybindManager table (declared `Hyprland-KeybindManager.hpp:137`), not the translator's inner `m_dispMap` (`Hyprland-legacy-DispatcherTranslator.hpp:19`, whose `Bad dispatcher` refusal at `DispatcherTranslator.cpp:31-32` is a different site); the socket body returns `Invalid dispatcher` at `HyprCtl.cpp:1150-1151` before any call. The quote truncates away the `g_pKeybindManager->` qualifier that identifies the table. |
| P2 | A `pass` request issued through the socket takes the press-only replay branch. | `if (S.m_passPressed == 1) {` (5) | S367 / `Hyprland-ConfigActions.cpp` / :1487 | The only write of `m_passPressed` is the bind press path (`Hyprland-KeybindManager.cpp:804`, cleared `:814`); the socket body (`HyprCtl.cpp:1128-1157`) never writes it, so it keeps its default `-1` (`Hyprland-ConfigActions.hpp:114`) and the `else` branch at `ConfigActions.cpp:1499-1500` runs — both edges, not press-only. |
| P3 | The config parser rejects a bind whose dispatcher name is written in uppercase. | `std::ranges::transform(HANDLER, HANDLER.begin(), ::tolower);` (3) | S368 / `Hyprland-legacy-ConfigManager.cpp` / :1592 | The quoted transform **folds** the name; the find at `:1594` runs on the folded name and rejection at `:1596-1598` is for names absent after folding — uppercase spellings are accepted (`EXEC` == `exec`). The quoted line is the fold, not a rejection. |
| P4 | At key-press time Hyprland refuses a bind whose dispatcher name is missing from the map. | `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);` (9) | S364 / `Hyprland-KeybindManager.cpp` / :785 | A press-path miss only logs `Invalid handler in a keybind!` (`KeybindManager.cpp:797-800`, under the source's own comment "Should never happen, as we check in the ConfigManager") — no refusal; parse-time find+reject is `ConfigManager.cpp:1594-1598`. |

**B2 evidence:** chain item 5 of the fixture entry asserts "the socket path writes the press edge into the shared pass state before calling the dispatcher" — false per the same pins (no such write anywhere in `HyprCtl.cpp:1128-1157`; the only write is `KeybindManager.cpp:804`) — and appears in no proposition-table row, so complete-mapping (declared-only) cannot see it.

## Reproducible setup/command

```sh
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify37
SCR=/fast/scratch/hyaku/mado-r52/Falsify37/rebuild-check   # seat scratch; removed after
bash "$SEAT/rebuild-fixture.sh" "$SCR/fixture"
# → base_rev=a77023649081e524b56e559da65e55bfd7468b7e  rev=72ecb569d0e61aabc38dfdb510c307b1be013c51
python3 "$SEAT/pred-c2-r52-frozen.py" "$SCR/fixture" 72ecb569d0e61aabc38dfdb510c307b1be013c51 \
        a77023649081e524b56e559da65e55bfd7468b7e "$SCR"     # rev run
python3 "$SEAT/pred-c2-r52-frozen.py" "$SCR/fixture" a77023649081e524b56e559da65e55bfd7468b7e \
        a77023649081e524b56e559da65e55bfd7468b7e "$SCR"     # base control
```

First build used rev `aff36ea11264a45a937a35fe3ce6813de3407116` over base `cec5717…` with identical result; the seat-dir rebuild reproduces it from receipts alone.

## Actual result

Rev run (`run-rev.out`, exit 0):

```
P_C2_R52: a ok=1 index_row=`knowledge/hyprland-dispatcher-entail-bypass-r52.md` (MAD...
P_C2_R52: b ok=1 rows=6/2 pins=6
P_C2_R52: p ok=1 propositions=4 mapped=4/4 complete=True
P_C2_R52:   P1 row=S366 pin=Hyprland-HyprCtl.cpp quote_words=1 locator=Hyprland-HyprCtl.cpp:1149 rationale_words=15 prod_bind=ok
P_C2_R52:   P2 row=S367 pin=Hyprland-ConfigActions.cpp quote_words=5 locator=Hyprland-ConfigActions.cpp:1487 rationale_words=15 prod_bind=ok
P_C2_R52:   P3 row=S368 pin=Hyprland-legacy-ConfigManager.cpp quote_words=3 locator=Hyprland-legacy-ConfigManager.cpp:1592 rationale_words=17 prod_bind=ok
P_C2_R52:   P4 row=S364 pin=Hyprland-KeybindManager.cpp quote_words=9 locator=Hyprland-KeybindManager.cpp:785 rationale_words=15 prod_bind=ok
P_C2_R52: c ok=1 body_shingles=446 files=67+cand0 max=6.3% top=[6.3%:corpus/knowledge/hyprland-dispatcher-dispatch-r51.md, ...]
P_C2_R52: d ok=1 held=7/3 lines=8 untargeted=1 tokens=14
P_C2_R52: clauses=abpcd clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=72ecb569...
```

Base control (`run-base.out`, exit 1): `entry absent at rev` → TARGET_MISSED, as the frozen no-work control requires.

**Reproduced: yes** — the counter-side predicate set reports TARGET_MET on an entry whose four declared propositions are each contradicted or unsupported by the very pinned bytes they quote, and whose prose carries a fifth false material claim outside the mapping.

## Why the ≤25-word cap participates

Every quote is 1–9 words; the disambiguating context (the `g_pKeybindManager->` qualifier, the `else` both-edges branch, the fold-then-find sequence, the log-not-refuse follow-up) lies outside each quote. The cap is an upper bound with **no floor**: P1's quote is a single token and is admitted. The cap therefore structurally excludes the context that would defeat the false reading, while the verbatim-substring test is satisfied by any fragment of the line.

## What the claim's defenses do and do not cover

- The counter is structural by design — the round's own C2CounterDraft spec says "semantic entailment requires outside review" (`.ufo/waves/round-52/w1-spec.json`). It passes the fixture.
- "Independent non-author samples actual source truth" sits outside the counter verdict and is non-exhaustive by construction ("samples"); the frozen text sets no minimum sample coverage, so a TARGET_MET verdict on an entry containing contradicted propositions is not prevented by any checkable clause.
- Consequence: as a coverage guarantee, "each material factual proposition maps to a pinned source quote ≤25 words with explicit support rationale" is enforceable only as binding+presence — "every declared proposition has a real quote nearby". The claim's hedge acknowledges this; the residual risk is that TARGET_MET is then reportable for an entry whose propositions are false, i.e. the shipped metric cannot see the failure its own target names.
- Fix direction (not a predicate edit): bind each proposition to machine-checkable support — e.g. required co-located tokens or a negation/branch scan within the cited span ±N lines — and require the outside sample to cover every declared proposition, or restate the claim as binding-only so the verdict cannot be read as truth.

## Limitations

- The fixture entry is a seat-local adversarial artifact in scratch, not a lane claim; no lane-tree file was created or edited by the experiment (the seat dir and this report are the assigned writes); no S-row, pin, control, claim or predicate was modified.
- Sources are the already-locally-available round-51 pins at the frozen base; no new fetch, no network, no package query or install, no host/process/compositor read, no input capture, no screenshot, no producer execution. Checker execution is lane counter code operating on fixture bytes only.
- The checker mirrors the frozen checkable predicates; the actual round-52 counter was not landed when this investigation ran (C2CounterDraft had not published), so clause `p` is a faithful implementation of the registration text and the binding half is the production code verbatim — the result is a property of the frozen predicate set, not of one implementation.
- Which proposition each quote fails to support is judged here from quoted pinned lines; in-round, the claim's "independent non-author" review would arbitrate — which is precisely the defense this finding shows is load-bearing and unbounded.

## Dissent / failed controls

- No control malfunctioned: the base no-work control missed exactly as registered. The reported failure is the pass-side entailment gap (false entry passes) — the finding itself.
- Interpretation dissent, recorded honestly: sibling Falsify36 declined to execute even the predecessor counter under a producer-execution reading; I read SKILL.md's source-only boundary (`SKILL.md:40-44`, "producer execution" in the context of bar producers and "pure-read producers") as forbidding host producers, package queries and live reads, while running lane counter code against seat-local fixture bytes is the operation the registration's own C2 workflow prescribes ("runnable structural C2 counter/selftest against staged entry/registry fixture"). Both readings are defensible; this seat's execution touched no host state.

## Sources used (all already locally available; no new fetch)

- Registry rows S364, S366, S367, S368 (+ S365, S369 bound by clause b): `corpus/SOURCES.md` at base `85d57a8`, status mined, opened 2026-10-27; URLs `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/...` (KeybindManager.cpp/.hpp, HyprCtl.cpp, ConfigActions.cpp/.hpp, legacy-ConfigManager.cpp, legacy-DispatcherTranslator.cpp/.hpp, SharedDefs.hpp).
- Pins: `.ufo/waves/round-51/fetch/*` at base, Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, accessed 2026-10-27 (fetched round 51); located quotes as tabulated above, each verified verbatim at its cited line.
- Round-51 entry (source of the verbatim `source:`/`held:`/manifest lines): `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` at base.

## Report

Attacked item: C2 (source proposition entailment). Concrete bypass reproduced: yes. A seat-local fixture entry, rebuilt from lane base `85d57a8` plus seat-dir receipts, passes a faithful implementation of every checkable frozen predicate — proposition count 4/4, row/pin/quote bindings verified by the lane's own production `bind_row` (`prod_bind=ok` ×4), complete declared mapping, README index row, novelty 6.3% ≤ 30%, held 7/3 — verdict TARGET_MET — while all four declared propositions are contradicted or unsupported by the very pinned bytes they quote (outer-vs-inner table misattribution via a qualifier-truncating one-word quote; wrong replay branch for a socket `pass`; fold read as reject; press-path log read as refusal), and a fifth false material claim asserted in prose escapes the complete-mapping check entirely because mapping is enumerable only over declared propositions. The base no-work control still misses (entry absent), so the counter discriminates presence, not entailment; the claim's sole entailment defense (independent non-author sampling) sits outside the counter verdict and is non-exhaustive by construction, and the ≤25-word cap with no floor admits one-word quotes while structurally excluding the disambiguating context. Receipts: `.ufo/waves/round-52/w1/Falsify37/{pred-c2-r52-frozen.py,fixture-entry.md,fixture-README.md,rebuild-fixture.sh,run-rev.out,run-base.out,pred-c2-r52-frozen.json}`.
