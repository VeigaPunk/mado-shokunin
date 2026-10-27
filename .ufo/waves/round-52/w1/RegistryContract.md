# RegistryContract — round 52 source rows and lesson Gate

Axes: coverage and operability. Scoped review of the C2 source-entry proposal and source-admission/Gate contract; no frozen claim or predicate edits.

## Medium — do not append proposed source rows yet

The current candidate `.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv` assigns S370–S373, but its citations point to `.ufo/waves/round-51/fetch/` files. The registry ends at S369 (`corpus/SOURCES.md:313-318`); its search log ends with round 51 (`:561-571`), so no S370+ rows are admitted. This map is a proposal, not evidence of a round-52 source opening. The date on an existing S-row is 2026-10-27, but its round-51 pin path establishes that this evidence was already opened for round 51; reusing or rereading that local copy does not demonstrate the frozen requirement for a source opened this round. Do not append these rows or mark them `mined` until the source opening, pin, and admission checks are evidenced for round 52.

Candidate source details for traceability: S370's proposed source is the existing S365 URL, `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`; S365 records it as opened 2026-10-27 in round 51. The proposal's located quote at the old local pin is line 597: `if (STATE != "down" && STATE != "repeat" && STATE != "up")`. I read the local R51 pin only; no network/source fetch was made in this review, and this is not a round-52 opening receipt.

The candidate rows also reuse canonical URLs already in active rows: S370's DispatcherTranslator.cpp is S365 (whose scope already includes individual dispatcher argument parsing); S371's ConfigActions.cpp is S367; S373's KeybindManager.cpp is S364. `QUALITY.md:34-39` requires explicit repeated-URL/overlap review, with human review for genuinely distinct scopes; URL equality alone neither admits nor rejects a row. In particular, the existing R51 entry already describes `sendkeystate` saving/restoring `m_passPressed` (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:197-199`), overlapping proposed P15. Establish what is genuinely new, review the URL collisions, and prefer held-row reuse where adequate rather than appending duplicate source records. S372 is a proposed ConfigActions.hpp source not present among S364-S369; it still needs its own round-52 opening and located quote.

## Medium — several proposed quote cells do not support the whole mapped proposition

The source bytes were read from the already-local R51 pins to compare them with the proposal; that verifies the snippets' context, not round-52 admission. The table's support rationales often rely on source lines that are inside the locator but absent from the exact quote cell. Examples:

- P03 quotes only the `down`/`repeat` assignments, but also claims `up` defaults to zero. The initialization is line 600 (`uint32_t keyState = 0;`), omitted from the quote.
- P05 quotes construction of `modifiedArgs`, but its claim that this delegates to `sendshortcut` needs the later call at line 619, absent from the quote.
- P11 quotes construction of `KEYPAIRSTRING`, but its cache claim also requires the lookup/write at lines 559-576.
- P12's quote shows the selector ternary, but not the following error return at lines 585-586 needed for the non-empty unresolved-selector claim.
- P13 bundles timestamp origin, keycode adjustment, and modifier assertion/clear; its quote contains only the `sendKeyboardKey(... S.m_timeLastMs, key - 8, ...)` call, not the modifier calls at lines 1554/1576 or the timestamp field declaration at `Hyprland-ConfigActions.hpp:117`.
- P15 quotes saving the old state at line 612, not restoring it at line 624. P16 quotes only the action signature, not the repeat-on-success and restore behavior at lines 1612-1615.

These are repairable draft issues, not findings that an unlanded counter or entry accepted bad evidence. Make each exact quote sufficient for its proposition (or split propositions / provide multiple located quotes as the frozen format permits), retain a specific support rationale, and recheck every locator against the round-52 opened pin. The map currently has 16 proposition rows, but count does not cure incomplete proposition-to-quote support.

## Lesson Gate contract and admission order

The local contract is explicit: `corpus/SOURCES.md:3-7` identifies the SOURCES contract and says additions/reopens are recorded in a lesson; only status, recheck, and used-by may change in place, with each change logged old→new. `SOURCES.md:530-533` says an unopened lead is neither evidence nor a row. The working precedent is `corpus/lessons/round-51.md:5-18`: the `## Gate` block labels the C2 entry admitted, identifies each new row and its status/opened date/used-by, and records tier, kind, source URL, pin/line, exact located quote and word count; it also documents quote verification and collision/rejection decisions. For round 52, keep the Gate section prospective until round-52 openings and quote checks exist; only then record admitted rows and any append/reopen decisions. Do not copy the R51 Gate's admitted wording or opening date onto these R51 pins as if they were newly opened.

## Evidence and limitations

Read-only source inspection (no shell command, test, counter, producer, package query, live probe, or network fetch):
- Frozen contract: `.ufo/waves/round-52/claims-frozen.md`, `.ufo/waves/round-52/registration.md`.
- Proposal: `.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv`.
- Registry and Gate rules: `corpus/SOURCES.md:3-7,313-318,530-571`; `corpus/QUALITY.md:34-39`; `corpus/lessons/round-51.md:5-18`.
- Compared local source pins: `.ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp:531-627`, `Hyprland-ConfigActions.cpp:1554-1618`, `Hyprland-KeybindManager.cpp:221-242`, `Hyprland-ConfigActions.hpp:114-118`.

No round-52 source was opened for admission in this review; no external candidate URL has a round-52 access date or quote receipt. Scratch was not needed or created; no tool installed. At inspection, the registry contains S364-S369 only and the proposal map uses round-51 pins. Recommendation is hold source-row append/admission pending actual round-52 opening, quote support, and collision review; this report does not vote on either frozen claim.

## Deliverables
- `.ufo/waves/round-52/w1/RegistryContract.md`

## Report
[Report]
