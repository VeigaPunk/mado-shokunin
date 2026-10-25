# Admission bar — new `corpus/knowledge/` entry and new `corpus/SOURCES.md` row

Numbered checklist. Every rule quoted verbatim with source file and line.
Files: `~/Projects/shokunin/CORPUS.md` (fleet contract) and
`corpus/QUALITY.md` (lane admission bar).

## A. Sources both artifacts share

1. **Falsifiability.** "A corpus entry is falsifiable or marked opinion; no
   unverifiable claims." — CORPUS.md:26. Lane bar: "Every claim falsifiable or
   marked opinion." — corpus/QUALITY.md:347 (criterion 41, superseding 1).
2. **Source anchor.** "`knowledge/` entries cite a source: file path, command
   output, or URL." — CORPUS.md:24. Lane bar: "Every claim carries a source: a
   measured anchor (path:line, command, evidence id) — never oral knowledge."
   — corpus/QUALITY.md:348 (criterion 42, superseding 2).
3. **Layer separation.** "Observation, inference, and unknown stay separate."
   — corpus/QUALITY.md:349 (criterion 43, superseding 3).
4. **Append-only errata.** "Errata are append-only blocks." —
   corpus/QUALITY.md:350 (criterion 44, superseding 4). Fleet: "**Corrections
   are new entries, never rewrites.**" — CORPUS.md:53.
5. **Rejections kept.** "A rejection is kept, not silently dropped." —
   corpus/QUALITY.md:351 (criterion 45, superseding 5).
6. **No secrets.** "**No credential material**, session or private URLs, or
   `op://` references — ever." — CORPUS.md:129; fleet expansion at
   CORPUS.md:49-52.

## B. New `knowledge/` entry

7. **Provenance trio first.** "Each `knowledge/` entry opens with `source:`,
   `verified-at:` and `recheck:`" — CORPUS.md:18. Kaika rule: "**A new
   knowledge entry opens with its provenance trio.** `source:`, `verified-at:`
   and `recheck:` come first; when the source is external, `source:` cites its
   `S###` row in `corpus/SOURCES.md` alongside the URL and anchor." —
   CORPUS.md:163-166.
8. **Count carries command.** "Any number in a corpus entry (rows, files,
   lines, packages) is written as `<number> — <command> <date>`." —
   CORPUS.md:34-35.
9. **Negative claim carries sweep.** "'No counterexample', 'nothing handles
   X', 'absent everywhere' need the search command that produced the absence,
   or the claim is unverifiable." — CORPUS.md:39-41.
10. **Quote names its location.** "Frontmatter vs body, header comment vs
    code, script vs installed skill." — CORPUS.md:42-43.
11. **Index row is a claim.** "Write the row when the file exists, not
    before." — CORPUS.md:46-47.

## C. New `SOURCES.md` row — named contract items

12. **Contract version.** The registry is governed by "Contract v1 (kaika,
    2026-10-19, frozen), carried here in full from
    `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`." — CORPUS.md:66-67. "A change is
    a new contract version, never an edit to this section." — CORPUS.md:67-68.
    Lane pointer: "Source tiers and the registry live in SOURCES.md (contract
    v1); this bar governs claim admission only." — corpus/QUALITY.md:24.
13. **Gate fields.** "The round lesson's `## Gate` records, for every new row,
    the URL, the access date, and a ≤25-word quote with its location grounding
    `teaches`. Non-author verification re-opens a sample." —
    CORPUS.md:113-115. The Gate section itself carries "(candidates, admitted,
    rejected with reasons, spot-check result)" — CORPUS.md:19-20.
14. **Quote word bound.** "a ≤25-word quote with its location" — CORPUS.md:114.
15. **Recheck forms.** "`recheck` — ISO date or cadence (`90d`, `180d`,
    `on-release`)." — CORPUS.md:105-106.
16. **Used-by rule.** "`used-by` — repo-relative paths of the knowledge
    entries or lessons citing the row, comma-separated, or `—`." —
    CORPUS.md:107-108. `mined` status requires it: "`mined` (cited by ≥1 path
    in `used-by`)" — CORPUS.md:103-104. Census check: "mined rows whose
    used-by paths do not exist — must print nothing" — CORPUS.md:146-147.
17. **Append-only rows.** "**Append-only.** Only `status`, `recheck` and
    `used-by` change in place, and each change is logged old→new in the round
    lesson. A correction is a new row whose `teaches` opens `supersedes
    S0NN —`." — CORPUS.md:116-118. Ids: "`S` + 3 or more digits, the next
    unused; never reused." — CORPUS.md:89.
18. **Quoting a source the lane did not open — barred.** "**A row is a
    claim.** Write it only after opening the source in the round that writes
    the row." — CORPUS.md:112-113. `opened` is "ISO date the row's author
    opened the source" — CORPUS.md:105. Unopened material stays a lead:
    "## Leads (unopened)   bullets; a lead is not evidence and never a row" —
    CORPUS.md:83. The Gate quote therefore grounds `teaches` from the author's
    own open, and "Non-author verification re-opens a sample" —
    CORPUS.md:115.

## D. Remaining row-shape constraints (same table contract)

19. **No pipes.** "No `|` inside any cell." — CORPUS.md:89; 11-column shape
    (awk `NF=13`) — CORPUS.md:136-137.
20. **Anchor.** "exact section / heading / page / line plus revision (version,
    commit, or publication date). Never a bare homepage." — CORPUS.md:99-100.
21. **Tier.** Scoped to `scope`; A/B/C enum; "`community` is never A"; C is
    "lead only — never sole support for an admitted entry." — CORPUS.md:93-97.
22. **Status enum.** "`queued` … `mined` … `rejected` (kept — a rejection is
    evidence of taste)." — CORPUS.md:103-104. Rejected rows: "`REJECTED:
    <reason>; flip: <what would change the verdict>`" — CORPUS.md:101-102.
