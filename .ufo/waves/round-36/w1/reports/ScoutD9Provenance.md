# ScoutD9Provenance — provenance-trio census of corpus/knowledge/

Lane: mado-shokunin. Read-only survey; one file written (this report).

## Method (command used)

For each `corpus/knowledge/*.md`, the trio members were located by the
line-anchored forms `^source:`, `^verified-at:`, `^recheck:` (the same
anchored `grep` the lane's own round-12 freshness check used —
`.ufo/evidence/round-12/after-measure.sh:20` runs
`head -n 15 "$f" | grep -q '^source:'` etc.). Equivalent one-liner:

```
for f in corpus/knowledge/*.md; do
  head -n 15 "$f" | grep -q '^source:' && \
  head -n 15 "$f" | grep -q '^verified-at:' && \
  head -n 15 "$f" | grep -q '^recheck:' && echo "OK  $f" || echo "MISS $f"
done
```

plus a full-file `grep -nE '^(source|verified-at|recheck):'` pass per file
to find where each member actually sits. Executed via a Python census over
`read().splitlines()` (same anchored `l.startswith(key)` semantics), so the
line numbers below are 1-based `file:line`.

Deviation noted: the prompt cites "CORPUS.md". No `CORPUS.md` exists
anywhere in the lane (`glob **/CORPUS.md` → no match; `ls corpus/` →
`QUALITY.md README.md SOURCES.md knowledge/ lessons/`). The trio
convention itself is real and documented in the lane (round-13/14 wave
prompts: "header trio (`source:`, `verified-at:`, `recheck:`)", head-15;
`.ufo/waves/round-13/w1/HistoricalRecon.md:122`,
`.ufo/waves/round-15/measure.py:5-7`). The survey was run against that
convention.

## Result: 29/50 carry the trio in the first 15 lines

50 knowledge notes total. 29 pass. All 29 carry the members in spec order
(`source:` ≤ `verified-at:` ≤ `recheck:` line number); `source:` may repeat
(YAML frontmatter list or several `source:` lines — e.g.
`dispatcher-surface-and-request-grammar-r26.md` lines 9-11,
`idle-lock-offered-in-the-bar-r15.md` lines 7-11).

### 21 files missing ≥1 member within head-15 — and where the trio actually sits

| File | `source:` | `verified-at:` | `recheck:` | Where the provenance actually lives |
|---|---|---|---|---|
| `animation-table-r26.md` | line 3 (frontmatter list, `- S175…S162`) | absent | absent | `source:` only, lines 3-8; nearest recheck-equivalent is the counter command `python3 -I .ufo/waves/round-26/c1/count-v2.py REV` at line 91; no `verified-at`/`recheck:` line anywhere in the file (100 L) |
| `bind-table-r25.md` | absent | absent | absent | no anchored trio line in the whole file (86 L); `author: mado` at line 1; S-ids appear only inline (`[S172, pinned …]`); round-25 recheck command `count-v4.py` is named in README index, not in the note |
| `config-health-report-r3.md` | absent | absent | absent | provenance is prose: "Probe window: 2026-10-14 14:40–14:48 UTC" line 3, method line 12; no trio line in 1017 L |
| `executor-test-sufficiency.md` | absent | absent | absent | version/sha256 ledger table lines 11-15; no trio line in 197 L |
| `gate-mutation-proof.md` | absent | absent | absent | "Date 2026-10-14" line 3; "Pins at write time" block lines 11-20; re-pin section line 145 ff; no trio line in 168 L |
| `gate-mutation-sweep-r8.md` | absent | absent | absent | "Date 2026-10-14" line 3; target pin line 16; no trio line in 179 L |
| `hyprctl-verification-layer.md` | absent | absent | absent | probe-window line 3; read-only statement line 17; no trio line in 308 L |
| `hyprland-config-plane.md` | absent | absent | absent | probe-window line 3, method line 5; no trio line in 268 L |
| `idle-lock-plane.md` | absent | absent | absent | probe-window line 7, method line 11; no trio line in 382 L |
| `keybind-rule-semantics.md` | absent | absent | absent | probe-window line 3, version pin line 8; no trio line in 316 L |
| `omarchy-drift-watch.md` | absent | absent | absent | "Measured 2026-10-14" line 3; gate pin lines 27+; re-anchor protocol ~line 284; no trio line in 287 L |
| `province-accuracy-selfaudit.md` | absent | absent | absent | audited-artifact pin lines 12-16; no trio line in 346 L |
| `remaining-planes-census.md` | absent | absent | absent | probe-window line 14, method line 16; no trio line in 348 L |
| `snapshot-diff-receipt-r9.md` | absent | absent | absent | "Date 2026-10-14" line 3; before/after gate shas lines 25-30; no trio line in 197 L |
| `terminals-and-omarchy.md` | absent | absent | absent | "Measured 2026-10-14" line 3; no trio line in 205 L |
| `theme-wallpaper-plane.md` | absent | absent | absent | probe-window line 12, method line 13; no trio line in 394 L |
| `walker-deep-r9.md` | absent | absent | absent | "Measured 2026-10-14 19:59Z" line 7; §1 identity pins line 53 ff; no trio line in 415 L |
| `walker-deep.md` | absent | absent | absent | measurement window line 4; evidence table line 25 ff; no trio line in 632 L |
| `walker-live-surface.md` | absent | absent | absent | "Measured 2026-10-14 18:20Z" line 6; §1 pins line 33 ff; no trio line in 315 L |
| `waybar-walker-plane.md` | absent | absent | absent | "Measured 2026-10-14" line 4; §1 inventory line 15 ff; no trio line in 484 L |
| `waybar-walker-semantics.md` | absent | absent | absent | "Measured 2026-10-14" line 4; version table line 20 ff; no trio line in 478 L |

Summary of the gap: 20 of the 21 misses are pre-trio-era notes (rounds
1-11 arc, dated 2026-10-14) plus `bind-table-r25.md`; their provenance is
in prose ("Measured/Probe window/Date" near lines 1-8) and in late-file
pins/errata, never as anchored header keys. `animation-table-r26.md` is
the only partial trio: `source:` at line 3, `verified-at:` and `recheck:`
nowhere. For the 20, "the line where the trio actually sits" does not
exist — the members are absent, not merely out of window; the table's
right column gives each file's de-facto provenance seat instead.

## Suggested append-only normalization policy (2 sentences)

On each affected note, append a short `## Provenance (normalized)` trailer
section — never edit the committed head or body — that restates the trio as
anchored `source:`/`verified-at:`/`recheck:` lines transcribed from the
note's own dated prose and pin blocks, tagged `[derived]` where a member
(typically `verified-at:`) had no explicit original statement. Gate the
trio on "anchored line present anywhere in file" rather than head-15 for
backfilled trailers, so the appended bytes normalize the ledger without
rewriting a single committed byte.
