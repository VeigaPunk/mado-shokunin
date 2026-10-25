# ScoutS209 — dated-backups sweep (read-only re-run, 2026-10-24)

## Per-copy results

Command:

```
for f in /home/vgpnk/.config/waybar/config.jsonc.bak*; do
  printf '%s\t%s\t%s\n' "$(stat -c '%y' "$f")" "$(grep -c omarchy-toggle-idle "$f")" "$f"
done
```

| mtime (stat %y) | `omarchy-toggle-idle` count | file |
|---|---|---|
| 2026-10-11 10:36:07.023252903 -0300 | 1 | config.jsonc.bak |
| 2026-10-03 17:44:32.097653608 -0300 | 1 | config.jsonc.bak.1791314470 |
| 2026-10-16 23:14:38.105347715 -0300 | 1 | config.jsonc.bak.1792203278 |
| 2026-10-17 17:02:56.289334445 -0300 | 1 | config.jsonc.bak.1792267376 |

Four copies, every one carries the handler exactly once — matches S209.receipt.txt lines 8–13 verbatim.

## Oldest copy

`/home/vgpnk/.config/waybar/config.jsonc.bak.1791314470` — mtime **2026-10-03** 17:44:32 -0300 (by `stat`, also line 16 of the receipt).

## 2026-10-03 vs 2026-10-06 — settled: both are correct, measuring different things

```
for e in 1791314470 1792203278 1792267376; do
  printf '%s -> %s\n' "$e" "$(date -d "@$e" '+%Y-%m-%d %H:%M:%S %z')"
done
```

| suffix epoch | decodes to | file mtime |
|---|---|---|
| 1791314470 | **2026-10-06** 16:21:10 -0300 | 2026-10-03 17:44:32 -0300 |
| 1792203278 | 2026-10-16 23:14:38 -0300 | 2026-10-16 23:14:38 -0300 (identical) |
| 1792267376 | 2026-10-17 17:02:56 -0300 | 2026-10-17 17:02:56 -0300 (identical) |

- Round entry's **2026-10-03** = the oldest copy's *file mtime* — supported by my `stat`.
- Merge package's **2026-10-06** = the oldest copy's *filename epoch* — supported by my `date -d @1791314470`.
- Interpretation: the suffix stamps when the snapshot was named/taken; the 10-03 mtime was preserved from the source (mtime-preserving copy). The two later copies show suffix == mtime, so only the oldest exposes the divergence.

Neither claim is wrong; they cite different clocks. If a single canonical "oldest copy date" is required, the mtime **2026-10-03** is the content's last-modified date and **2026-10-06** is the snapshot-creation date.

## Cross-check vs S209.receipt.txt

Identical file set, identical per-copy handler counts (all 1), identical oldest-copy identification and mtime. Receipt adds nothing conflicting.
