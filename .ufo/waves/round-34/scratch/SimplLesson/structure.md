# Round-34 lesson — proposed structure (SimplLesson seat, 2026-10-24)

Shortest structure that satisfies the frontier contract. Three `##` headings, one
per named contract element. Every sub-block below is conditional on the data
existing; write the heading always, the body only if non-empty (write `none`).

## Exact headings

```
# Round 34 lesson
## Gate
## Mistakes
## Census
```

Header: `Author:` line, date, base tip hash, `registration.md` path. Two lines
max — round-33 form, not round-32's paragraph.

## `## Gate`

Contract rows it must carry (CORPUS.md SOURCES rule 1, rule 2; kaika lesson rule):

1. **Opened rows** — one table, one row per SOURCES row written this round
   (expected: S201, S202). Columns:

   `| row | URL | opened | located quote (≤25 words, <file>:<line>) | status |`

   URL + access date + located quote are mandatory per row; `opened` is the
   lane's own access date (2026-10-24), not a campaign staging date (r32 lesson).
   No second table for "re-opened sources" — rows re-opened but already in the
   registry go in one prose line (r33 style: "S189 PRESENT … not re-appended").

2. **Refusals** — one bullet or table row each: `item — reason — flip: <what
   would change the verdict>`. Rejected SOURCES candidates read
   `REJECTED: <reason>; flip: …` in their `teaches` cell; the lesson records the
   same pair.

3. **C2 publication** — one line: the appended SCORECARD marker
   `r34-s189-line: line=169 …` with its evidence pointer
   (`.ufo/waves/round-32/fetch/S189.bin:169`). Not a SOURCES row; kept here
   because the Gate is where this round's admit/publish decisions live.

4. **In-place row changes** — one prose line naming `status`/`recheck`/`used-by`
   changes old→new on pre-existing rows, or `none` (SOURCES rule 2).

5. Conditional single bullets, only if they occurred: quarantine hand-check
   verdicts; one mined `considerthese` item. Each is one bullet (r33 form), never
   a `###` block.

## `## Mistakes`

Kaika rule fields, verbatim: `class · evidence · captured-by · fix`. Either form:

- table `| class | evidence | captured-by | fix |` (r24, r32), or
- bullets `class: X. evidence: <pointer>. captured-by: <criterion|none>. fix: <…>` (r33 — shorter for ≤3 rows).

Rules the fix must satisfy (kaika): a fix is shown able to fail — ship the
red-before output that exits non-clean with the fix as the only delta, committed.
`captured-by` names the QUALITY criterion or protocol rule, or `none`.
Classes come from the mistakes vocabulary (`vacuous`, `survivor`, `stale-premise`,
`reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`).
If no mistake was mined: `none mined this round.` — keep the heading.

## `## Census`

Before/after pair, two code blocks or two lines each:

```
start: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
  → exit <rc>, `mado ok`, <N> W04 warnings (<ids>); receipt .ufo/waves/round-34/evidence/sources-start.txt
end:   same command → exit <rc>, rows <before>→<after>, tier A<a1>→<a2>/B../C.., status mined..→../queued../rejected..;
       receipt .ufo/waves/round-34/evidence/sources-end.txt
```

Hard requirement learned from routed defect M23-1 / r27-spotcheck: the printed
warnings and counts must match the committed receipt byte-for-byte — paste from
the receipt file, never retype the W04 id list. Row-count delta must equal the
number of rows appended in `## Gate` (r34 expectation: +2 if S201 and S202 land).

## What the short form drops vs round 33 — and why it is safe

- No `### Frontier` — the frontier verdict lives in the round report and
  SCORECARD; the lesson does not duplicate it. Contract names only Gate,
  Mistakes, census.
- No `###`-level sub-blocks — r33 proved Gate carries fine as labeled bullets;
  the quote table is the only required table.
- No id-collision / validate-before-append narrations — those are Gate evidence
  for a mass append (r32: 132 staged ids); for two rows they are one clause in
  the census end line if run at all.
- Alternative considered: fold the census pair into `## Gate` (r20–r24 did:
  "Start census … End census" inside Gate). That is one heading shorter, but a
  named `## Census` costs ~10 chars and makes the before/after pair unmissable
  for a spot-check grepping headings. Recommend the separate heading; folding is
  contract-conformant if the L1 prefers it.
