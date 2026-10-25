# ExecKnowledgeIndex — verify corpus index row @ fa7ba113

Scope: the `corpus/README.md` row naming `corpus/knowledge/waybar-module-text-route-r25.md`, added at commit `fa7ba11346116672352b5d41494141c5c4d738d0` ("round-34: admit the waybar event-socket entry after the frozen counter"). Verified in the lane working tree on 2026-10-24.

## Verdict: PASS — no broken paths, no missing ids

## The row (corpus/README.md:58, confirmed by `git show fa7ba113` diff)

| `knowledge/waybar-module-text-route-r25.md` (round 34; Waybar event-socket client) | The Hyprland backend derives a socket folder and warns when the runtime directory is absent. The window module registers for activewindow. Upstream bytes only; host bar use is unknown. | `source:` S201, S202 in [SOURCES](SOURCES.md); fetched bytes `.ufo/waves/round-34/fetch/S201.bin` and `.ufo/waves/round-34/fetch/S202.bin`; recheck 90d. |

## Path resolution (all regular files)

| Path named in row | Result |
|---|---|
| `corpus/knowledge/waybar-module-text-route-r25.md` | OK — regular file, 1227 bytes |
| `.ufo/waves/round-34/fetch/S201.bin` | OK — regular file, 6550 bytes |
| `.ufo/waves/round-34/fetch/S202.bin` | OK — regular file, 8324 bytes |

## S-id existence (corpus/SOURCES.md)

- S201 — line 203: Waybar 0.15.0 `src/modules/hyprland/backend.cpp`, 6550 B, sha256 prefix `799bf02f6d18ae04` — **recomputed sha256 matches** (`sha256sum` prefix = `799bf02f6d18ae04`). Back-reference column names `corpus/knowledge/waybar-module-text-route-r25.md`. Mined 2026-10-24, 90d recheck.
- S202 — line 204: Waybar 0.15.0 `src/modules/hyprland/window.cpp`, 8324 B, sha256 prefix `5df496eb3cfe5cae` — **recomputed sha256 matches**. Same back-reference, same dates.

## Row content requirements

- **Surface**: stated — backend socket-folder derivation + `$XDG_RUNTIME_DIR/hypr` fallback warning; window module `activewindow` registration. Matches the knowledge file's OBS lines (gate-quotes reproduced from the fetched bytes).
- **Provenance**: stated — `source:` S201, S202 with pointer to SOURCES.md and the two fetch-bin paths.
- **Recheck**: stated — `recheck 90d`, consistent with the `recheck: 90d` field in the knowledge file and the 90d column in SOURCES.md.

## Notes

- The knowledge file itself is well-formed: lane id, round 34, read-only substrate disclaimer, both gate-quotes present verbatim, and an explicit UNK boundary ("host bar use is unknown") — consistent with the row's "Upstream bytes only" caveat.
- No defects found in this scoped check.
