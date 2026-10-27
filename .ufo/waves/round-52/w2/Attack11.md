# Attack11 — W2 attack #11: "C2 new source pins genuinely opened this round"

Seat: `Attack11` (connector). Axes: coverage, operability. Scope: C2 only. This is an attack
report, not a vote; no non-author judgment claimed. Checks ran 2026-10-27 against lane HEAD
`85d57a81` and the uncommitted landing in the working tree.

Reads-first honored: `claims-frozen.md`, `registration.md`, then the W1 reports
`C2SourceRecon`, `C2EntryDraft`, `C2CounterDraft`, `C2PinAudit`, `C2EntryQuality`,
`C2CoverageCritic`, `C2Novelty`, `RegistryContract`, `Falsify08`, `PlanDataWalk`, plus
`corpus/SOURCES.md`, `corpus/QUALITY.md:34-39` (rule 17), `corpus/lessons/round-52.md`,
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (landed), `quality/counters/c2-r52-proposition-entry.py` (landed).

## Verdict summary

The clause "grounded in sources opened this round" is **not verified by the landed
instrumentation and is not verifiable from the landing's provenance evidence**. Three
independent falsifiers reproduced; two structural findings compound them. No executed
receipt exists showing the committed counter ever emitted TARGET_MET on the landed entry.

---

## Attack 1 (REPRODUCED — counter identity): the landed counter is not the tested draft and fails the landed entry

Clause attacked: C2 "a new committed counter checks proposition count, row/pin/quote
bindings and complete mapping".

- `quality/counters/c2-r52-proposition-entry.py` (landed, untracked) sha256
  `5c7fb820e43c7f6782b6ebfc90d018c25d74976d9e8ab2a90df5e4c82fb50c0a`, 47 lines / 2584 B.
- Drafted/tested counter `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`
  sha256 `55452a3d6eab7cca2b20095f8678fbe936c8c65f241a561611a675defd8379fb`, 965 lines.
- The draft seat's integration note (C2CounterDraft.md:37) requires a **byte-identical**
  copy. The landed file is a different, much weaker implementation — every clause the
  draft tested (row freshness vs frozen base, anchor fetch-root, revision, quote-at-pin,
  mapping completeness, duplicate quote/claim) is absent.
- Reproduction:
  - `python3 quality/counters/c2-r52-proposition-entry.py --repo <lane> --rev HEAD --work <scratch>`
    → `C2_R52: entry=absent verdict=TARGET_MISSED` (default `--entry` still points at the
    draft slug `hyprland-synthetic-key-dispatch-r52.md`; the landed slug is
    `hyprland-synthetic-dispatch-r52.md`).
  - Fixture clone `git clone` → `85d57a81` → copied the exact landed bytes (entry, README,
    SOURCES, lesson, counter, `round-52/fetch/*`), committed → tip `81291929`. Stub run
    with `--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` →
    `props=0 rows=0 indexed=1 failures=1 miss=props verdict=TARGET_MISSED exit=1`.
    Its proposition regex expects cell 2 = `S###`; the landed table puts the proposition
    text there. Offline check: the exact regex matches 0 rows on the landed entry.
- Consequence: the counter that actually landed cannot produce a green on the actual entry.
  The draft's r-green receipt proves only a synthetic fixture; the stub proves nothing —
  the C2 target as landed has no passing receipt at any revision.
- Bonus falsifier inside the same file: `--base` is parsed (line 19) and **never used**;
  no `git show <base>:SOURCES.md` comparison exists, so the "opened this round" row check
  the draft enforced (`row_not_new`) is gone. The stub's only freshness signals are a
  string grep for `2026-10-27`, `mined`, and the entry path — all forgeable in the same
  commit that adds the row.

## Attack 2 (REPRODUCED — opened-this-round provenance): no verifiable opening receipt; the documented manifest is absent

Clause attacked: C2 "grounded in sources opened this round"; registration "each maps to an
opened-this-round `S###` row".

- `.ufo/waves/round-52/fetch/` holds 4 payloads + `README.txt` + `SHA256SUMS`.
  `sha256sum` confirms payload identity with the round-51 pins (all four EQUAL; also
  byte-equal to `w1/C2EntryDraft/fetch/`).
- `README.txt` claims "opened by lane L1 on 2026-10-27 via read URL" and defers details to
  a "round52 source-reopen manifest". `find .ufo/waves/round-52 -name '*reopen*' -o -name
  '*manifest*'` → **no such manifest exists anywhere**; unlike round 51, there is no
  `fetch-manifest.json` at all. The only transport receipt in the wave is the draft seat's
  self-authored `verify.txt` ("transport: curl -fsSL … HTTP 200 each"), which covers its
  own `w1/C2EntryDraft/fetch/` dir — not the top-level fetch the landed rows pin against.
- Provenance timing consistent with local copy, not URL opens: all four top-level payloads
  have mtimes inside a 3 ms window (10:47:09.559–.562), 44 min after the seat fetch
  (10:03). Distinct inodes (no hardlinks); `cp` is the parsimonious source. Byte equality
  proves upstream pin stability, not a round-52 open.
- W1 corroboration: `Falsify08` demonstrated this lane's pin/manifest bytes are consumed
  by nobody at scoring time; `C2EntryQuality` recorded that "a rehashed R51 cache proves
  byte identity, not fresh upstream access." `RegistryContract` held row admission pending
  exactly this evidence.
- Verdict: reproduced as an **evidentiary gap** — "opened this round" currently rests on a
  self-referential README assertion; the artifact that would corroborate it is missing.
  Limitation: I cannot prove a URL was not opened; the claim is unverifiable-as-evidenced,
  which is itself the attack surface the predicate tried to close.

## Attack 3 (REPRODUCED — QUALITY17 / Gate): rows admitted while their named preconditions stand open

Clause attacked: repeated-URL rows S370/S371/S373 (S370≡S365, S371≡S367, S373≡S364 same
URL+commit) and the registry-admission contract.

- Working-tree `corpus/SOURCES.md` admits S370–S373 as `mined` rows and itself records
  "**distinct-scope review remains outstanding**" (search-log line). `census-after.txt`
  flags the same three as `W04 duplicate url … across scopes` — a warning-only census,
  which `QUALITY.md:34` rule 17 explicitly says is *not* the review.
- The Gate contract (`corpus/lessons/round-52.md`) still says: rows are "drafts, not
  admitted … Review source URL collisions against prior rows before appending. Record each
  source URL, access date and located quote <=25 words here once verified." Its
  Admission/rejection section: "**pending final source audit**". The Gate record the
  contract requires was never written, yet the rows sit in the registry.
- Verdict: reproduced — the registry was mutated in the working tree ahead of the two
  artifacts (Gate record, distinct-scope review) that govern whether these rows may be
  admitted at all. If the review lands cleanly this is curable; as of inspection it is an
  admitted-row/precondition inversion.

## Attack 4 (REPRODUCED — landing drift): the landed entry is not the artifact any W1 audit reviewed

- Landed `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` is 32 lines — a stripped
  summary (title + table + footer). The audited `C2EntryDraft/entry-draft.md` is 251 lines
  with the mechanism prose, held-boundary disclosures, and `[INF]` markers. The
  `validate/` snapshot confirms the 32-line file is what was staged.
- Consequences, each mechanically verified:
  - Every proposition id is unreferenced by prose: the drafted counter's clause (e) emits
    `P01..P18:id_not_referenced` on the fixture tip. The map is orphaned from any prose.
  - Landed P04 and P17 map the same mechanism to the same quote region
    (`DispatcherTranslator.cpp:619-622`) — an inflated count the drafted counter's
    `duplicate_quote` rule exists to catch; the landed stub cannot even parse the rows.
  - Landed P16's quote sits one line below its pin's first anchor line
    (`ConfigActions.cpp:1555-1556` vs cited `:1554`), and the "then clears" half of the
    claim is never quoted — the same quote-support defect class RegistryContract/EntryQuality
    flagged in the draft, reintroduced in different words.
  - Landed SOURCES anchors carry `…; r52 fetch SHA256 …` — the drafted counter's clause (c)
    reports `anchor_no_fetch_root` on all 18 props (no `.ufo/waves/round-52` path present).
  - Net: the drafted counter on the fixture tip reports `clauses_met=2
    verdict=TARGET_MISSED` (a ok, b ok; c/d/e fail).
- The non-author truth samples (C2PinAudit, C2EntryQuality) ran against the draft; no
  non-author review covers the landed bytes the predicate is scored on.

## Attack 5 (OBSERVED — commitment state): nothing for C2 is committed

`git status`: `?? corpus/knowledge/hyprland-synthetic-dispatch-r52.md`,
`?? quality/counters/c2-r52-proposition-entry.py`, `?? corpus/lessons/round-52.md`,
`M corpus/README.md`, `M corpus/SOURCES.md`; `?? .ufo/waves/round-52/` (incl. `fetch/`).
HEAD is still the frozen base `85d57a81`; `git show HEAD:corpus/SOURCES.md | grep S370` →
0. The claim's "new committed counter" and "committed" pins/rows/entry exist only in the
working tree; at every committed revision target and control are indistinguishable. If a
later integration commit lands this, finding 1 (stub identity/grammar) still stands —
a commit will not repair the counter.

## Errors encountered / report-quality notes

- None blocking. The `w1/C2CounterDraft` receipts document counter-vs-draft-table defects
  fixed mid-flight; the landed 32-line entry re-derives the table (rewritten wording,
  same ids) — the draft TSV and landed md table differ in claim text and quotes, so
  `proposition-map.tsv` cannot be treated as the landing's map.
- No tip-side receipt exists for either counter (`receipts/` holds only `c1-base.txt`,
  `c2-base.txt`, the latter explicitly untrusted for the target per registration.md:15).

## Limitations

- Source-only attack: no network open was attempted (boundary respected); provenance
  findings are stated as evidence-absent, not proven-forgery.
- Fixture tests used a scratch clone at `/fast/scratch/hyaku/mado-r52/Attack11/fixture/lane`
  (`git rev-parse --show-toplevel` asserted before mutation); the lane repo was read-only.
- Whether the stub's failure is "wrong grammar" or "entry landed in wrong shape" is a
  judgment for the claim owner; either way the landed pair is non-functional.

## Report

- `.ufo/waves/round-52/w2/Attack11.md`
- Scratch: `/fast/scratch/hyaku/mado-r52/Attack11/` (cleaned on exit).
