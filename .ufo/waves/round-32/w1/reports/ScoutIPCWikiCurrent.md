# ScoutIPCWikiCurrent — re-open S186 (hyprland-wiki IPC page, pinned)

**Fetch:** success. `curl -fsSL` on
`https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md`.

- Fetched bytes: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/scratch/ScoutIPCWikiCurrent/ipc_index.md`
- Byte length: **6539** (102 lines)
- sha256: **`535bc4c385a06162d3e7e356e1a13853f9c47598787f15c80883c2895d06d1a4`** (prefix `535bc4c385a0`)
- Access date: **2026-10-24**

## Located items (line numbers in fetched file)

| # | Item | Line(s) |
|---|------|---------|
| 1 | Request socket path `.socket.sock` | **14** (heading `## `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock``) |
| 2 | Event socket path `.socket2.sock` | **25** (heading `## `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock``) |
| 3 | Request grammar (flags + command + args) | **19** — `Basically, write `[flags]/command args`.` |
| 4 | Synchronous-evaluation / freeze rule | **21–23** (`[!NOTE]` block; rule text on **22**, close-socket advice on 23) |
| 5 | Event framing `EVENT>>DATA` | **30** — `` `EVENT>>DATA\n` (`\n` is a linebreak) `` |
| 6 | Event catalogue size | **44** event rows (table rows lines 38–81; header 36, separator 37) |

## Verbatim quotes (≤25 words each)

- Request socket (L14): `## `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock``
- Event socket (L25): `## `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock``
- Framing (L30): `` `EVENT>>DATA\n` (`\n` is a linebreak) ``

## Staged-entry faithfulness check

Staged entry: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/ipc-contract-r25.md`
(cites S186 = same pinned URL/commit; `verified-at: 2026-10-23`).

| Staged claim (quote) | Verdict |
|---|---|
| §1 "The request socket is `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock` … `Basically, write `[flags]/command args`." (S186:7-12) | **AGREE** on substance — path and grammar quote verbatim-accurate (L14, L19). Cited range `7-12` does not match this fetch (grammar is L19, socket L14); staged line numbers appear to come from a different extraction. |
| §1 "Hyprland evaluates connections to this socket completely synchronously, which means that any unclosed connections *will cause Hyprland to freeze*" (S186:15) | **AGREE** on substance — verbatim quote of L22. Cited line `15` is off (rule is L21–23). |
| §2 "The event socket is `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock` … `` `EVENT>>DATA\n` (`\n` is a linebreak) ``" (S186:18-25) | **AGREE** on substance — socket L25, framing L30 verbatim. Cited range `18-25` does not contain the framing line in this fetch (it's L30). |
| §2 "E.g.: `workspace>>2`" (S186:25) | **AGREE** on substance — exact text at L32; cited line `25` is the socket2 heading, not the example. |
| §4 "44 event names on both sides … none added and none removed" (S186 side) | **AGREE** — this fetch's catalogue contains exactly 44 event rows (L38–81). |

**Overall:** every S186-derived *claim* in the staged entry is faithful — all quoted
strings match the re-fetched bytes verbatim and the 44-event count is exact. The only
discrepancy is the `(S186:N)` / `(S186:N-M)` line citations, which are uniformly offset
from this fetch's numbering (e.g. grammar cited :7-12, actual :19; note cited :15,
actual :21-23; framing cited :18-25, actual :30). Content: faithful. Line pins: stale.

§3 (S189 implementation claims) and the S187 side of §4 are outside this re-open's
scope — only S186 was fetched.
