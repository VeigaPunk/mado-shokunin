# D4 — the mined-mistake count for round 76

Seat R77ExecRepairs, round 77, 2026-11-04. Lane HEAD `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7`.

## Correct count: five mined mistakes (M76-1 … M76-5)

The lesson's `## Mistakes` table is the source of truth. Rows, measured at HEAD:

    $ cd /home/vgpnk/Projects/shokunin/mado-shokunin
    $ grep -c '^| M76-' corpus/lessons/round-76.md
    5

    $ grep -n '^| M76-' corpus/lessons/round-76.md
    48:| M76-1: label set v1 modelled the harness's `verdict=` as summary-green only; …
    49:| M76-2: label set v2 kept the echo-dropping outcome mutation …
    50:| M76-3: the pre-freeze control's mutant leg parsed `MADO_R76_*` rows with a regex …
    51:| M76-4: the C1 fixture template's first draft made `green-mutant`'s outcome expectation `pass` …
    53:| M76-5: the standalone pre-freeze control receipt (`control-baseline-r76.txt`) …

    $ grep -oE 'M76-[0-9]+' corpus/lessons/round-76.md | sort -u | wc -l
    5

Line 52 is blank (a table-rendering nit between rows 4 and 5, not a sixth row). Five distinct
ids; five table rows.

## The wrong counts in the record

| where | text | status |
|---|---|---|
| `.ufo/reports/round-76/mado.md:54` | "the lesson with **six** mined mistakes and two repair passes" | wrong (six) |
| `LOG.md:3789` (round-76 entry) | "**Four** mined (M76-1 … M76-4 …)" | wrong (four) |
| commit `81ca5d1b` message | "lesson with **four** mined mistakes" | wrong (four) |
| `.ufo/reports/round-76/mado.md:190-192` | "**Six** wave-found defects repaired … (F1/F3/F4/F6, D3 parameter binding, C1 `--base-rev` binding, C2 child env and scope-local cancellations)" | a *separate* tally, self-inconsistent: six said, eight named |

Keep the two tallies separate: **mined mistakes = 5** (lesson `## Mistakes` rows); the
wave-found-repair tally is a different count and the report's parenthetical names eight repairs
while saying six.

## Landed correction (verified present)

`corpus/lessons/round-76.md:185` opens `## Corrections (round 77)`; its D4 item reads:

```markdown
- **D4 (count).** The round-76 report says "six mined mistakes"; this lesson holds five rows
  (M76-1…M76-5), so the measured count is five — `grep -c '^| M76-' corpus/lessons/round-76.md`
  prints `5`. The report's six is the defect; the lesson and the LOG ("Four mined") also
  disagreed, and the lesson rows are the source of truth.
```

## LOG append (if the L1 corrects the LOG entry in place-append)

Append inside the round-76 LOG entry (after its **Mistakes** bullet):

```markdown
  Correction (round 77): five mined mistakes (M76-1…M76-5) — `grep -c '^| M76-'
  corpus/lessons/round-76.md` prints `5`; "Four mined" above is the stale count.
```
