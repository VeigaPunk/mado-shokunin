# CritDivergence — oldest dated copy of the bar's configuration: 2026-10-06 vs 2026-10-03

Scoped question: the merge package's round-15 text dates the oldest dated copy
2026-10-06; the lane's own round-35 sweep dates it 2026-10-03. Which is right,
does it change a conclusion, and what must the admitted entry say.

## 1. The two readings measure different clocks — my own read

Files read directly (host, read-only, 2026-10-24):

- Merge package text:
  `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/idle-lock-offered-in-the-bar-r15.md`
  — `§2` says "the oldest from 2026-10-06 (S334)" quoting `"dated 2026-10-06 16:21"`;
  `§4` says "since at least 2026-10-06". Registry: `SOURCES.append.md:144` (now id
  **S340**) repeats "the oldest from 2026-10-06".
- Sweep artifact the package cites:
  `/home/vgpnk/Projects/shokuknow/lanes/mado/round15/fetch/host-waybar-dated-backups-sweep.txt:5`
  — `copy config.jsonc.bak.1791314470  dated 2026-10-06 16:21  idle-lock handler: 1`.
  Its `dated` column decodes the **filename epoch suffix** (1791314470 →
  2026-10-06 16:21:10 -0300).
- Lane sweep: `.ufo/waves/round-35/w1/reports/ScoutS209.md` and committed receipt
  `.ufo/waves/round-35/fetch/S209.receipt.txt:16` — `stat` mtime of
  `config.jsonc.bak.1791314470` = **2026-10-03 17:44:32.097653608 -0300**.

My own re-measurement (commands run, output above):

| file | filename epoch decodes to | `stat` mtime | `omarchy-toggle-idle` count |
|---|---|---|---|
| `config.jsonc.bak` | — | 2026-10-11 10:36:07 | 1 |
| `config.jsonc.bak.1791314470` | 2026-10-06 16:21:10 -0300 | **2026-10-03 17:44:32** | 1 |
| `config.jsonc.bak.1792203278` | 2026-10-16 23:14:38 | 2026-10-16 23:14:38 (== suffix) | 1 |
| `config.jsonc.bak.1792267376` | 2026-10-17 17:02:56 | 2026-10-17 17:02:56 (== suffix) | 1 |

Only the oldest copy's two clocks diverge: suffix epoch 10-06 vs mtime 10-03.
The backup tool preserved the source's mtime when it snapshotted — the copy's
bytes were already in their present state on 2026-10-03; the snapshot was taken
on 2026-10-06. The two later copies show suffix == mtime, which is why only the
oldest exposes the split.

## 2. Which is right

Both numbers are true, of different things:

- **2026-10-06** = when the oldest backup was *written* (filename epoch).
- **2026-10-03** = when the oldest backup's *content* was last modified.

The entry's claim is "how long the idle-lock choice has been on offer" — the
earliest attestation of `omarchy-toggle-idle` in a bar configuration. That
question is answered by the content's clock, not the snapshot's. The oldest
copy's bytes — handler included — existed on 2026-10-03. For the claim the
entry makes, **2026-10-03 is the right date**; the merge package's 2026-10-06
reports the snapshot operation and understates the evidence by three days.
(The sweep artifact's `dated` column is epoch-semantics; accurate as taken-dates,
insufficient for earliest-attestation claims.)

## 3. Does it change a conclusion

No substantive conclusion changes:

- "Every dated copy carries the handler" — unchanged (4/4, count 1 each,
  re-verified).
- "The offer is not new" — unchanged and strengthened: earliest attestation is
  *earlier* than the package claimed, so the offer has been on offer longer.
- The statelessness and no-trace findings (S210/S342: 2 toggle files, 0 naming
  the idle lock) — untouched.

What changes is only the earliest-attestation date: `since at least 2026-10-06`
must become `since at least 2026-10-03`, and any "oldest dated" figure should
name the measured mtime (ideally both clocks, to foreclose this exact
divergence recurring). The package text is wrong in the direction of
understating its own evidence — conservative but factually off.

## 4. What the admitted entry must say

§2 body line — replace "the oldest from 2026-10-06 (S334)" / quote
`"dated 2026-10-06 16:21"` with the measured fact, both clocks named:

> Every dated copy of the bar's configuration carries the `omarchy-toggle-idle`
> click handler; the oldest copy (`config.jsonc.bak.1791314470`) has mtime
> **2026-10-03 17:44:32 -0300** — its snapshot epoch decodes to 2026-10-06, so
> the snapshot was taken then with the file's earlier mtime preserved.

§4 line — "since at least 2026-10-06" → "**since at least 2026-10-03**".

Registry row (S340) teaches text — "the oldest from 2026-10-06" →
"the oldest copy's content is dated 2026-10-03 (mtime; the snapshot epoch is
2026-10-06)". The sweep artifact itself is a dated receipt — leave it; correct
by the entry's own text, per append-only rules.

Sibling edits needed: §1's OBS quote `> "dated 2026-10-06 16:21"` should be
re-anchored to the mtime figure or annotated as the snapshot epoch, else the
quote silently re-imports the wrong clock.

## 5. Observation for the record (not the scoped question)

The cited id drifted: the note's `source:` lines and `Cites:` name S329–S336,
but `SOURCES.append.md:144` now allocates the backups sweep as **S340** (S334 is
now the Japanese archived-article row) — the registry was renumbered after the
note was drafted. Any admission should re-sync the cite ids to the current
registry before landing, or the entry's provenance resolves to the wrong
artifacts.

## Receipts

- `stat`/`grep -c`/`date -d`/`sha256sum` output: this report §1 (ran 2026-10-24,
  lane repo, read-only).
- `config.jsonc.bak.1792203278` and `.1792267376` are byte-identical
  (sha256 `07f7d663…`), consistent with the gkeep drift record cited in earlier
  rounds; current `config.jsonc` differs (`a408a33d…`), handler still present.
