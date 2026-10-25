# RevengerData — round-34 S201/S202 byte-for-byte re-fetch

Verdict: **CONFIRMED.** The lane's committed blobs are the exact upstream bytes published at tag `0.15.0` of `Alexays/Waybar`.

## Method

- Re-fetched live from the network on 2026-10-24 via `curl -fsSL` into `.ufo/waves/round-34/scratch/RevengerData/`.
- Compared sha256 and byte length against `.ufo/waves/round-34/fetch/S201.bin` / `S202.bin` and the digests recorded in `corpus/SOURCES.md` (lines 203–204, recorded as sha256 prefixes + lengths).
- Verified tag existence: `https://github.com/Alexays/Waybar/releases/tag/0.15.0` → HTTP 200; `https://github.com/Alexays/Waybar/tree/0.15.0` → HTTP 200.

## Digests

### S201 — src/modules/hyprland/backend.cpp @ 0.15.0

| Source | sha256 | Length |
|---|---|---|
| Live fetch (scratch/RevengerData/backend.cpp) | `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e` | 6550 B |
| Committed blob (fetch/S201.bin) | `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e` | 6550 B |
| SOURCES.md:203 | `799bf02f6d18ae04…` (prefix) | 6550 B |

Match: full sha256 equal; recorded prefix is a strict prefix of the full digest.

### S202 — src/modules/hyprland/window.cpp @ 0.15.0

| Source | sha256 | Length |
|---|---|---|
| Live fetch (scratch/RevengerData/window.cpp) | `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846` | 8324 B |
| Committed blob (fetch/S202.bin) | `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846` | 8324 B |
| SOURCES.md:204 | `5df496eb3cfe5cae…` (prefix) | 8324 B |

Match: full sha256 equal; recorded prefix is a strict prefix of the full digest.

## Tag authenticity

`0.15.0` is a real upstream tag: both the release page and the git tree resolve 200 under `github.com/Alexays/Waybar`. Raw URLs of the form `raw.githubusercontent.com/Alexays/Waybar/0.15.0/...` serve bytes pinned to that ref.

## Conclusion

Fetched bytes ≡ upstream bytes at tag 0.15.0 for both sources. No drift, no truncation, no substituted content. The SOURCES.md digest prefixes and lengths are accurate.
