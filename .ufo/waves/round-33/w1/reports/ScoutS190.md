# ScoutS190 — re-fetch verification of S190 (Waybar 0.15.0 `backend.cpp`)

## Result: agree on identity, disagree on cited line ranges

## Re-fetch

- URL: `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp`
- Destination: `.ufo/waves/round-33/scratch/ScoutS190/S190.bin`
- Fetch: `curl -fsSL` succeeded on 2026-10-24; no error.

## Hash and size

```
$ sha256sum S190.bin
799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e  S190.bin
$ wc -c S190.bin
6550
```

- sha256: `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e` — **matches** the expected digest and the staged prefix `799bf02f6d18ae04`.
- Byte length: **6550 B** — matches the staged `6550 B`.

## Frozen quote

`$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr` is a contiguous
substring at **line 38** (`grep -F` hit, one line, no wrapping):

```
38:    spdlog::warn("$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr");
```

## Verdict vs the staged row

Staged row: `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` line 11 (S190).

**Agree** on all identity claims: URL/tag `0.15.0`, 6550 B, sha256 prefix
`799bf02f6d18ae04`, and the summary of behavior (`.socket2.sock` at `:98`,
`$XDG_RUNTIME_DIR/hypr` → `/tmp/hypr` fallback at `:38-39`, `substr(0,
find_first_of('>'))` event-name split at `:142`, 1024-byte buffer at `:115`).

**Disagree** on the three cited line ranges — they do not cover the symbols they
name on this file:

| Staged cite | Actual span (grep -n 'IPC::') | Finding |
|---|---|---|
| `:17-33` (`getSocketFolder`) | `19-44` | range ends inside the function; the frozen quote (`:38`) and `/tmp` fallback (`:39`) are outside it |
| `:77-99` (`socketListener`, 1024-byte event buffer) | `77-139` | the 1024-byte buffer is at `:115`, outside the cited range; `:98` is the socket-path line, not the buffer |
| `:109-116` (`parseIPC`) | `141-150` | `:109-116` is the `fdopen`/read-loop region inside `socketListener`; `parseIPC` opens at `:141` |

Note for whoever corrects the row: the event read is `fgets` into a 1024-byte
buffer (`:115-117`), so an event is actually consumed per line at up to 1024
bytes — the staged "reads at most 1024 bytes per event" gloss is consistent with
the code but the cite is not.

Corrected anchors: `getSocketFolder` `:19-44`, `socketListener` `:77-139`
(1024-byte buffer `:115`), `parseIPC` `:141-150`.
