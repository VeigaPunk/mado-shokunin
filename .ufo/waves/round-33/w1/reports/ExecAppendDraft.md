# ExecAppendDraft — three census rows for S190, S191, S197

## Deliverable

`.ufo/waves/round-33/scratch/ExecAppendDraft/append-block.md` (3995 B) — a header
plus three 11-column rows matching the `corpus/SOURCES.md` registry schema, ready for
a later seat to append. `corpus/SOURCES.md` untouched.

Source material: staged rows at `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md`
lines 11 (S190), 12 (S191), 18 (S197).

## Normalizations applied (per seat prompt)

- `status` → `mined` (all three already `mined` staged)
- `opened` → `2026-10-24` (staged `2026-10-23`)
- `recheck` → `90d` (staged `on-release` prose stripped and recorded verbatim beside
  the block under "Stripped recheck prose")
- `used-by` → S190, S191 `corpus/knowledge/waybar-module-text-route-r25.md`;
  S197 `corpus/knowledge/event-delivery-limits-r26.md` (the staged S197 row also
  carried `host-bar-and-idle-binding-r26.md`; dropped per the exact-used-by rule and
  the frozen cite-map in `registration.md`, which binds S197 to
  `event-delivery-limits-r26.md` only)
- No literal or escaped pipe in any cell — verified by script (below)

## Anchor corrections folded in (evidence: w1 scout re-fetch reports)

The staged rows were opened before the scouts re-fetched the blobs; three staged
anchor ranges understate or miss the named symbols. I corrected them — gate-neutral
cells (the C1 counter checks id, quote, sha256, used-by only), accuracy gain only:

- S190 `anchor`: staged `:17-33` / `:77-99` / `:109-116` → corrected `:19-44`
  (`getSocketFolder`), `:77-139` (`socketListener`, `.socket2.sock` connect `:98`,
  1024-byte `fgets` buffer `:115`), `:141-150` (`parseIPC`). Verified by `grep -n`
  on `.ufo/waves/round-33/fetch/S190.bin`: function definitions at `:19`, `:77`,
  `:141`; `parseIPC` call at `:129` inside `socketListener`.
- S191 `anchor`/`teaches`: staged "IPC registration `:22-28`" and "subscribes to
  `activewindow` and `closewindow`" → corrected `:27-31` (five registrations:
  `activewindow`, `closewindow`, `movewindow`, `changefloatingmode`, `fullscreen`;
  `grep -n` on `fetch/S191.bin`). Markup claim confirmed in bytes by ScoutS191.
- S197 `anchor`/`teaches`: staged "`:804-821` (twelve event registrations)" →
  corrected `:803-829` (`registerIpc` full span): twelve unconditional
  (`:804-815`) plus two conditional — `windowtitlev2` (`:821`),
  `activewindowv2` (`:827`); `grep -n` on `fetch/S197.bin` matches ScoutS197's
  count of 14. `windowReprKey` fmt lines `:154-159` verified.

Digests unchanged and match `c1/frozen.json`: S190 `799bf02f…f9e` (6550 B),
S191 `5df496eb…46` (8324 B), S197 `1e19d926…e9` (41392 B).

## Validation

```
S190 cells=11 status=mined opened=2026-10-24 recheck=90d used-by=corpus/knowledge/waybar-module-text-route-r25.md
S191 cells=11 status=mined opened=2026-10-24 recheck=90d used-by=corpus/knowledge/waybar-module-text-route-r25.md
S197 cells=11 status=mined opened=2026-10-24 recheck=90d used-by=corpus/knowledge/event-delivery-limits-r26.md
OK: 3 rows, 11 cells each, no literal/escaped pipes in cells, used-by exact
```

(Python: assert no `\|`, 11 cells/row, status/opened/recheck normalized, used-by
exact match, no residual `on-release`/`2026-10-23` in row lines.)

## Notes for the appending seat

- Row order in the file: S190, S191, S197 — insert after S189 and before S196 if
  the registry remains id-sorted, or append at tail per the integrator's order.
- The stripped `on-release` recheck prose is preserved in the block for whoever
  wants the fuller re-check instruction; the schema cell is `90d` as required.
