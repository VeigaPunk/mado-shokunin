# W2 Attack07 — C2: does each proposition quote entail the full claim?

Seat: Attack07 (W2 attack #07, mado round 52). Target clause: C2's "each material factual
proposition maps to a pinned source quote <=25 words and explicit support rationale", the
counter clause "A committed counter checks proposition count, row/pin/quote bindings and
complete mapping", and the post-state "counter pass at final lane tip" (`claims-frozen.md`,
`claims.md`, `registration.md`). This is an attack, not a vote; all verdicts are
reproduced / not reproduced against the bytes named below. No claim/predicate was edited.

Artifacts under attack (working tree; lane tip is still frozen base `85d57a818c3707397e21c840b6498b105ba798aa`):

- entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` sha256 `bee0d143…ecb078`, 32 lines, 18 propositions P01–P18
- landed counter `quality/counters/c2-r52-proposition-entry.py` sha256 `5c7fb820…fb50c0a`, 47 lines
- W1 draft counter `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py` sha256 `55452a3d…8379fb`, 965 lines
- sources `.ufo/waves/round-52/fetch/` — all five SHA256SUMS entries verified OK this seat (independent re-open basis)

Entailment standard applied: quote + its pin span, at the pinned revision, must support every
material clause of the proposition as written. Quote-only gaps are reported separately from
pin-covered gaps. Counter claims are tested by execution, not transcription.

## Executed tests (all commands local, read-only on the fleet; fixtures in own scratch)

| # | Test | Command (abridged) | Outcome |
|---|---|---|---|
| T1 | landed counter vs landed entry at a commit | scratch repo `repo-a` (base-copy README/SOURCES + landed entry, committed); `python3 c2-r52-proposition-entry.py --repo repo-a --rev HEAD --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | `props=0 … verdict=TARGET_MISSED`, exit 1 — **the committed counter cannot parse its own target entry** |
| T2 | frozen no-work control | same counter, `--repo <lane> --rev 85d57a8…` | `entry=absent verdict=TARGET_MISSED`, exit 1 — control direction reproduces |
| T3 | default `--entry` path | same counter, defaults, repo-a@HEAD | `entry=absent` — default path is `…synthetic-key-dispatch-r52.md`, landed file is `…synthetic-dispatch-r52.md` |
| T4 | counter-shape entry, 40-word blob in anchor cell | repo-b fixture | `props=4 failures=0 verdict=TARGET_MET`, exit 0 — length gate does not bind the evidence text |
| T5 | counter-shape entry, conforming | repo-c fixture | `verdict=TARGET_MET` — isolates T1's cause as the table-shape mismatch |
| T6 | landed counter vs fabricated quotes | repo-e fixture: 4 propositions with invented quotes at real pins | `verdict=TARGET_MET`, exit 0 — quote binding is name-only; no source bytes are ever opened |
| T7b | W1 draft counter vs landed entry | scratch repo `repo-d`: real base commit 85d57a8 + landed tree/fetch committed on top (`ea1fec19…`); `python3 -I w1/C2CounterDraft/c2-r52-proposition-entry.py --repo repo-d --rev HEAD --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | `clauses_met=2/5 verdict=TARGET_MISSED`: (c) `P01–P04:anchor_no_fetch_root`; (d) `quotes_bound=17/18 … P16:quote_not_at_pin`; (e) `P01–P04:id_not_referenced` |

## Per-proposition entailment (independent re-open of fetch/ at efb5099; sha256sum -c OK)

All 18 quotes ≤25 whitespace words (max 19, P03); 17/18 verbatim inside the pin span;
rationales present and non-empty. Entailment failures and gaps:

| P | pin (fetch bytes) | quote | verdict |
|---|---|---|---|
| P01 | DispatcherTranslator.cpp:591-594 (quote at 592-593) | four-field parse + count rejection | **entailed** |
| P02 | :597-598 | guard enumerates down/repeat/up | **entailed** |
| P03 | :600-604 | keyState init 0; down→1, repeat→2 | **entailed** |
| P04 | :619-622 | second delegate call guarded by `keyState == 2 && result.success` | **entailed** |
| P05 | :607 | joins ARGS[0],[1],[3]; state field ARGS[2] omitted | **entailed** |
| P06 | :531-535 (quote at 532-533) | three-field gate | **entailed** |
| P07 | KeybindManager.cpp:221-225 (quote at 223-224) | toupper + `contains("SHIFT")` | **gap (minor)**: "known modifier names" plural — only SHIFT inside pin/quote; CAPS/CTRL/ALT/MOD2-5 at :226-240 are outside both |
| P08 | :540-543 exact | numeric>9 and `code:` branches assign parsed number | **entailed** |
| P09 | :544-547 (quote at 546-547) | `keycode < 272` → "invalid mouse button" | **gap (minor)**: "The `mouse:` path" scoping rests on pin line 544, not in the quote; rationale does not supply it |
| P10 | :565-566 exact | keymap-range loop + per-key symbol read | **gap (minor)**: "remaining key-name path" scoping rests on the unquoted else-branch at :548 |
| P11 | :557 exact | cache key = `format("{}{}", rc<uintptr_t>(KB.get()), KEY)` | **entailed** |
| P12 | :582-586 (quote at 583) | empty selector → nullptr | **partial**: second clause "written selector without a result is rejected" is evidenced by pin lines 585-586, not by the quote |
| P13 | ConfigActions.cpp:1558 exact | `sendKeyboardKey(S.m_timeLastMs, key - 8, …PRESSED)` | **entailed** |
| P14 | ConfigActions.hpp:117 exact | `m_timeLastMs = 0; // timestamp of last key/mouse event` | **entailed** |
| P15 | DispatcherTranslator.cpp:612 exact | `oldPassPressed` copy | **binding gap**: "before changing it" — the writes (:614-617) and restore (:624) are outside pin and quote; quote+pin never show any change to `m_passPressed` |
| P16 | ConfigActions.cpp:1554-1558,1576 | mods-then-key calls | **falsified (verbatim) + partial**: quote splices :1554 with :1558, eliding `if (S.m_passPressed == 1) { if (!isMouse)` — not a contiguous excerpt anywhere in the file (mechanical: `in_span=False`, and W1 draft counter `P16:quote_not_at_pin`); the "then clears the modifier state" clause rests on :1576 which is in the pin locator, not the quote — the rationale itself says "the clear call at 1576 is included in this locator", i.e. locator, not quote |
| P17 | DispatcherTranslator.cpp:619-622 (quote at 621-622) | guarded second delegate call | **falsified (subject)**: "`sendshortcut`'s repeat branch" — the repeat branch lives in `sendkeystate` (:591-627, `keyState` is its local); `sendshortcut` (:531-589) has neither a state field nor repeat logic; the pin's own context contradicts the proposition's attribution |
| P18 | :574 exact | `return …"sendshortcut: key not found"` | **falsified (localization)**: "inside the scan" — the return at :574 executes after the scan loop (:565-571) closes, inside the cache-miss branch; the rationale silently re-scopes to "keysym resolution branch" |

Structural premises that hold: index row present (`corpus/README.md:80`), S370–S373 registered
(`corpus/SOURCES.md:320-323`) with `mined`, `2026-10-27`, 40-hex revision and this entry's path;
distinct slug and distinct mechanism scope from the r51 entry. A06/T6 below shows these checks
have no teeth in the landed counter, but the underlying facts verify.

## Attack items

- **A01 [high] — landed counter cannot parse the landed entry.** Clause: "A committed counter checks proposition count…" / "After: counter pass at final lane tip". Repro T1. The counter's row regex (`c2-r52-proposition-entry.py:28`) expects `| P## | S### | …`; the entry's table is `| P## | Proposition | S### | …`. `props=0` → TARGET_MISSED at any revision containing the entry. **Reproduced.**
- **A02 [high] — default entry path does not name the landed entry.** Repro T3; default `hyprland-synthetic-key-dispatch-r52.md` vs landed `hyprland-synthetic-dispatch-r52.md`. The W1 integration note (`C2CounterDraft.md`, "Integration for the L1") explicitly warned to change that constant; the landed copy carries the same stale default. **Reproduced.**
- **A03 [high] — no counter under which the landed bytes pass.** Repro T7b: the W1-mutation-tested draft counter (18/18 mutants caught, `quotes_bound=18/18` on the W1 staged draft) misses the landed state on clauses (c), (d), (e). Combined with T1: both available counters emit TARGET_MISSED against the landed pair. **Reproduced.**
- **A04 [high] — the landed counter is not the audited artifact.** 47 lines / sha `5c7fb820…` vs W1 draft 965 lines / sha `55452a3d…`. Lost: verbatim-in-pin-span binding, base-absence of rows ("opened this round"), completeness/distinctness mapping, fetch-root pin resolution, 3-word quote floor. No W1 report documents the landed bytes (grep over `.ufo/waves/round-52/` finds only the draft). Provenance gap at landing.
- **A05 [med] — counter "quote ≤25 words" gate binds the wrong cell and never fires.** The regex maps its `quote` variable to the 6th cell; in the entry that cell is the support class (`direct`). With the counter's own expected shape, a 40-word blob in the anchor cell passes (T4). On the landed entry the gate never runs at all (props=0). Manual audit: all 18 real quotes are ≤25 words — premise true, check absent.
- **A06 [med] — "row/pin/quote bindings" are name-only.** Repro T6: fully fabricated quotes at real pins → TARGET_MET. The landed counter never opens `fetch/` bytes; no pin resolution, no quote-to-source comparison. The claim's counter scope ("checks … row/pin/quote bindings") is over-scoped relative to the implementation; the entailment disclaimer does not cover this, because verbatim-in-span is mechanically checkable and was checked by the W1 draft.
- **A07 [med] — no green receipt exists for any landed pair.** `receipts/` holds only `c1-base.txt` and `c2-base.txt`; `c2-base.txt` is the **round-51** counter at base. W1 `r-green.txt`/`r-draft-fixed.txt` are the draft counter on a synthetic fixture / staged draft in scratch. The wave signal "counter draft r-green proves a separate synthetic fixture only, not landing" is confirmed — and stricter: the landed counter is a different artifact that has never been shown green against anything.
- **A08 [med] — "committed counter" / "final lane tip" unmet at review time.** Lane tip = frozen base `85d57a8…`; entry and both counters are untracked working-tree files (`git status --porcelain`). At the only existing revision the counter must miss (T2 — trivially). Limitation: landing may be pending by design mid-wave; the defect is that even a future commit of these bytes fails per A01/A03.
- **A09 [high] — P16 quote is a spliced, non-verbatim excerpt.** Clause: "exact located quote … explicitly supporting it". Repro: collapse `fetch/Hyprland-ConfigActions.cpp:1554-1558` and compare — `sendKeyboardMods(modMask, 0, 0, 0);` and `sendKeyboardKey(…PRESSED);` are separated by `if (S.m_passPressed == 1) { if (!isMouse)`; the entry's space-joined quote occurs nowhere in the file. Independently flagged by the W1 draft counter (T7b `P16:quote_not_at_pin`). The elided guard is material: the shown PRESSED call is branch-conditioned. **Reproduced.**
- **A10 [med] — P16's "then clears the modifier state" clause is not in the quote.** The clear call (`sendKeyboardMods(0, 0, 0, 0);`) is at ConfigActions.cpp:1576 — inside the pin locator, absent from the quote; the rationale cites the locator, not the quote. Pin-covered, quote-gap partial entailment.
- **A11 [high] — P17 misattributes the mechanism.** Clause: entailment of the full proposition. "sendshortcut's repeat branch" is contradicted by the pin's own function span (sendkeystate, :591-627); sendshortcut (:531-589) contains no `keyState`/repeat logic. The quote entails a guarded second delegate call; the proposition as written is false about the owner. **Reproduced.**
- **A12 [med] — P18 mislocalizes the error return.** "inside the scan" — the return at :574 is after the loop (:565-571). Rationale re-scopes without acknowledging the proposition text is wrong. **Reproduced.**
- **A13 [med] — P15's change-clause has no binding.** "saves the prior `m_passPressed` value before changing it": the only pinned/fetched evidence is the copy at :612; the writes (:614-617) and restore (:624) are outside pin and quote. Source truth confirms the writes exist, but the mapping does not locate them — the exact weak-binding shape this round was supposed to eliminate.
- **A14 [low] — P12 second clause rests on the pin, not the quote** (lines 585-586 carry the rejection guard). Pin-covered partial; quote alone covers clause 1 only.
- **A15 [low] — P07 generalizes beyond its pin.** "checks known modifier names using substring membership" — pin :221-225 shows the mechanism for SHIFT only; six more name groups at :226-240 are unpinned.
- **A16 [low] — P09/P10 subject attribution rests on unquoted context** ("`mouse:` path" ← :544; "remaining key-name path" ← :548). Minor; pins are within the branch bodies.
- **A17 [low] — P04/P17 map the same source fact twice** (both pin :619-622; P17's quote is a subset of P04's). The 18-proposition count includes one duplicated mechanism; "at least four substantive propositions" still holds, but the padding inflates the table.
- **A18 [med] — source-grounding premise: repeated URLs, no recorded distinct-scope review.** S370 ≡ S365 (DispatcherTranslator.cpp @ efb5099, confirmed directly), S371 ≡ S367 (ConfigActions.cpp), S373 ≡ S364 (KeybindManager.cpp, additionally S352); only S372 (ConfigActions.hpp) is a new URL — matching W1 C2PinAudit finding 2. Registration routes this to explicit QUALITY17 review to be recorded by the data seat; no such record exists in `corpus/lessons/round-52.md`, `corpus/SOURCES.md`, or the wave dir (grep). Cited regions are new relative to the r51 anchors, so the scope case is arguable — but it is unrecorded.
- **A19 [negative result] — mechanical quote premises hold.** 17/18 quotes verbatim inside pin spans at efb5099 (fetch SHA256SUMS verified OK); all ≤25 words; rationales present; four rows ≥ the frozen minimum. The entry's structural binding work is real; the failures are concentrated in A01–A14.
- **A20 [reproduced control] — no-work control behaves as claimed.** T2 and W1 `r-base.txt`: base → `entry=absent verdict=TARGET_MISSED` exit 1. The only C2 counter clause that reproduces cleanly end-to-end — and it is non-discriminating, since the worked state also misses (T1/T7b).

## Verdict on the seat question

Not reproduced as claimed. The entry's proposition→quote mapping entails the full claim for
13–14 of 18 propositions (with three minor scoping gaps); P16, P17, P18 fail quote-level
entailment as written (one spliced quote, one false subject, one false localization), and
P12/P15 carry clauses whose evidence lies outside the quote. Independently, the committed
counter cannot pass its own target entry at any revision (A01), the W1-audited counter also
misses the landed bytes (A03), and no landing green exists (A07). C2's counter-facing and
entailment-facing post-conditions are both unmet by the current bytes; the no-work control
(A20) and the entry's structural premises (A19) do reproduce.

Recommendation (non-binding): land the W1 draft counter (byte-identical per its integration
note) or regenerate the entry table in the landed counter's shape AND extend the landed
counter to bind quotes to fetch bytes; fix P16 (contiguous quote or per-clause rows), P17
(subject → sendkeystate), P18 (drop or re-scope "inside the scan"); record the QUALITY17
distinct-scope review for S370/S371/S373; produce a green receipt of the exact landed command
at a commit containing the pair.

## Residual risk and limitations

- Lane tip never moved off base during this review; every counter-vs-entry test ran on scratch
  fixtures (`repo-a`…`repo-e`) seeded from working-tree bytes plus the real base commit. A
  future landing could alter bytes; digests above pin what was judged.
- I did not fetch any URL (source-only boundary); source truth rests on `fetch/` bytes whose
  SHA256SUMS I re-verified, and on the immutable commit recorded in each registered URL.
- Entailment judgments on P07/P09/P10 marked "minor gap" are pin-covered; a reviewer accepting
  pin-context attribution would rate the mapping 15/18 with only P16–P18 failing.
- Provenance of the 47-line landed counter is unknown to this seat (no W1 or wave document
  names it); absence is recorded from grep over `.ufo/waves/round-52/`, not from L1 records.
- Report is an attack, not a vote; it scores nothing and edits no claim or predicate.

## Trailer

- Report: `.ufo/waves/round-52/w2/Attack07.md` (this file, paths relative to lane root `mado-shokunin/`)
- Scratch `/fast/scratch/hyaku/mado-r52/Attack07/` — fixtures `repo-a`…`repo-e`, `quote_check.py`, `quote_check2.py`, `counter_tests.sh` — removed on exit; nothing written outside this seat dir and scratch; no tracked-file edits; no git/jj mutation of any fleet repo (scratch fixture repos asserted `rev-parse --show-toplevel` before commits); no installs; no live reads, probes, or screenshots.
- Tooling: preinstalled `python3`, `git`, `sha256sum` only.
