# ExecFetches — committed fetch-blob digest verification

Round 34 · wave 1 · executor report. Byte-for-byte re-verification of the committed
fetch blobs at commit `fa7ba11346116672352b5d41494141c5c4d738d0` (current `HEAD`).

## Method

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file blob \
  fa7ba11346116672352b5d41494141c5c4d738d0:.ufo/waves/round-34/fetch/<ID>.bin | sha256sum
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file blob \
  fa7ba11346116672352b5d41494141c5c4d738d0:.ufo/waves/round-34/fetch/<ID>.bin | wc -c
```

Registry digest: `corpus/SOURCES.md` rows S201 (line 203) / S202 (line 204), which
record the sha256 as a 16-hex prefix plus byte length. Frozen digest:
`.ufo/waves/round-34/c1/frozen.json` `fetches.<ID>.sha256` (full 64-hex).

## S201 — `.ufo/waves/round-34/fetch/S201.bin` — 6550 bytes

| Source | sha256 |
|---|---|
| blob (`git cat-file` → `sha256sum`) | `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e` |
| `corpus/SOURCES.md` row S201 | `799bf02f6d18ae04` (prefix; row also records `6550 B`) |
| `c1/frozen.json` `fetches.S201.sha256` | `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e` |

**AGREE.** Blob digest == frozen digest exactly; SOURCES.md prefix is a strict prefix
of the blob digest; SOURCES.md byte length (6550 B) == blob byte length (6550).

## S202 — `.ufo/waves/round-34/fetch/S202.bin` — 8324 bytes

| Source | sha256 |
|---|---|
| blob (`git cat-file` → `sha256sum`) | `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846` |
| `corpus/SOURCES.md` row S202 | `5df496eb3cfe5cae` (prefix; row also records `8324 B`) |
| `c1/frozen.json` `fetches.S202.sha256` | `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846` |

**AGREE.** Blob digest == frozen digest exactly; SOURCES.md prefix is a strict prefix
of the blob digest; SOURCES.md byte length (8324 B) == blob byte length (8324).

## Working-tree sanity check

`sha256sum` on the working-tree files under `.ufo/waves/round-34/fetch/` returns the
same two digests, and `git status --porcelain` reports no modifications to
`.ufo/waves/round-34/fetch`, `.ufo/waves/round-34/c1/frozen.json`, or
`corpus/SOURCES.md` — the working tree matches the committed blobs.

## Verdict

Both fetch blobs are byte-for-byte consistent with the frozen digests and the
registry rows. No mismatch on digest or byte length for S201 or S202.
