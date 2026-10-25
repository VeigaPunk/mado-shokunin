# ScribeEntryWaybar — w1 report (round 33)

Seat: scribe, entry `corpus/knowledge/waybar-module-text-route-r25.md` (staged,
NOT written into `corpus/`). Sources: S190, S191 only.

## Deliverable

- Draft: `.ufo/waves/round-33/scratch/ScribeEntryWaybar/waybar-module-text-route-r25.md`
  (7089 B) — sourced only from the fetched bytes
  `.ufo/waves/round-33/fetch/S190.bin` and `S191.bin`.
- Registry append for S190/S191 is owned by ExecAppendDraft's staged block
  (`.ufo/waves/round-33/scratch/ExecAppendDraft/append-block.md`); this seat did
  not touch `corpus/SOURCES.md`.

## Gate-contract preflight (re-run at write time, 2026-10-24)

Against `.ufo/waves/round-33/c1/frozen.json`, mechanically (`python3`, pathlib +
hashlib, see transcript):

- `S190`: gate-quote line exact (`gate-quote: S190 $XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr`); quote contiguous substring of blob; blob sha256 `799bf02f6d18ae04…78bb4f9e` == frozen; digest string present in entry.
- `S191`: gate-quote line exact (`gate-quote: S191 m_ipc.registerForIPC("activewindow", this);`); quote contiguous substring of blob; blob sha256 `5df496eb3cfe5cae…570c9846` == frozen; digest string present in entry.
- `corpus/knowledge/waybar-module-text-route-r25.md` absent before/after — no corpus write. ALL-OK: True.

Line anchors in the draft were re-derived from the fetch bytes this round
(`grep -n` receipts in transcript): `getSocketFolder` :19-44 (fallback warn
:38), `socketListener` :77-139 (`.socket2.sock` connect :98, 1024-byte buffer
:115), `parseIPC` :141-150 (split at first `>` :142), `getSocket1Reply`
:178/:198, `getSocket1JsonReply` :236-237; window registrations :27-31,
markup route :58-64, `onEvent`→`dp.emit()` :240-241, `activeworkspace` query
:114, `lastwindowtitle` parse :164.

## Staged claims — verdicts

| Staged claim | Verdict | Basis |
|---|---|---|
| S190 teaches: socket-folder derivation, `/tmp/hypr` fallback, `.socket2.sock` subscription, event-name split, 1024-byte read | KEPT | S190:19-44, :38, :98, :141-150, :115 |
| S191 teaches: subscribes + builds text from title/initialTitle/class/initialClass, rewrite rules, GTK markup | KEPT | S191:27-31, :59-62, :63, :64 |
| Staged S190 anchors `:17-33`, `:77-99`, `:109-116` | DROPPED — stale; `:17-33` misses the :38 gate-quoted line, `:109-116` lands inside `socketListener`, not `parseIPC` | fetch bytes this round; agrees with ScoutS190 report |
| Staged S191 anchor `:22-28` + "subscribes to `activewindow` and `closewindow`" (original `SOURCES.append.md:12`) | DROPPED — understated; bytes carry five registrations :27-31 | fetch bytes; agrees with ScoutS191 report |
| Staged `recheck` cells (`on-release — re-pull at tag 0.15.0…`, ran 2026-10-23) | NOT carried into entry per lane instruction — entry uses `verified-at: 2026-10-24` / `recheck: 90d`; original prose stays recorded verbatim in append-block.md § Stripped recheck prose | lane dispatch |

No staged claim was found asserting anything beyond the two blobs (no host,
rendering or live-socket claim in the staged rows for S190/S191); the entry's
§4 records the dropped items and the non-claims explicitly.

## Notes for assimilation

- Entry header carries the tag-pinned raw URLs and full sha256 per source;
  fetch-blob paths are named as the byte anchors. `kind=code, tier=A`,
  `used-by=corpus/knowledge/waybar-module-text-route-r25.md` match the staged
  rows in append-block.md.
- Entry cross-references `ipc-contract-r25.md` §1-2 (compositor framing twin)
  and `waybar-observation-boundaries-r16.md` (rendering boundary); both exist in
  `corpus/knowledge/`.
- S190 staged `wc -c` says 6550 B — matches my `sha256sum`/`wc -c` receipt.
