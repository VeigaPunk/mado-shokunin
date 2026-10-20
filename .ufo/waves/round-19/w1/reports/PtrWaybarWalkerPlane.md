# PtrWaybarWalkerPlane — R18-V3 freshness pointer appended to waybar-walker-plane.md; prefix verified byte-for-byte

## Scope and behaviour

- Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/waybar-walker-plane.md` (sole writer this wave). Only append performed; no existing byte changed.
- `grep -n "2.17.0"` returned exactly lines 38, 197, 405 (of the original 475-line body).
- Appended block: heading `## Freshness pointer (round 19, 2026-10-20)` plus five bullets, at new lines 476-484. The first bullet (line 479) contains both `2.17.2` and `S090`.
- Claim families classified in the block:
  - version-bound (dated, not valid for 2.17.2): `walker --version` print (`:38`, `:197`, `:405`); `walker --help` flag list (`:196-197`).
  - process/unit state (dated, superseded by restart hooks): walker PID 1808 and 2026-10-13 start (`:31-33`, `:172`, `:404`); elephant `is-enabled` (`:181`) with elephant 2.21.0→2.22.1 not pinned here.
  - version-independent of the walker binary: user config 49 L / 1,336 B / sha `fecf71fa4253803e` (`:21`); omarchy launcher and restart anchors (`:169-188`). The walker-route-r18.md host declaration records the same sha prefix on 2026-10-20 (file bytes); this block does not re-assert it.
  - waybar/hypridle/hyprlock/swayosd version prints (`:37-40`): outside S090, not re-measured.
- Host pause respected: no pacman/systemctl/walker/omarchy/live-gate command; host files were not read by this seat.

## Hash and prefix check

| | sha256 | bytes | lines |
|---|---|---|---|
| before | `c5d7a3ebff9e68ac47ab462de1bfa7ee229c98a8e3a80df5ac5924dd62e77bfa` | 28392 | 475 (no trailing newline) |
| after | `69d1096c7b686647f67e61aa1e4288a870e384c839d4dd33c4763388c185f9aa` | 29729 | 483 newlines (484 lines, no trailing newline) |

- Prefix check: `head -c 28392 corpus/knowledge/waybar-walker-plane.md | sha256sum` → `c5d7a3eb…e62e77bfa`, equal to the before-hash. Pass.
- Appended tail: `tail -c +28393 … | sha256sum` → `0a2d0f26640ea8dbdbb15478b6d79eb636a5e2aa0fc6842468b0ebd6a0289329` (1,337 bytes).
- Side effect of the edit tool: the original file lacked a trailing newline; the tool supplied one, which sits inside the appended region (after the old final `.`). No old byte was altered.

## Findings

- F1 (R18-V3, this note): the note's walker version pins are at lines 38, 197, 405 and are now dated and marked, with pointer to S090 and walker-route-r18.md. Closed for this note.
- F2: walker-route-r18.md's own host declaration, not re-measured here, records the same config sha prefix as this note (`fecf71fa4253803e`) — cited as a comparison, not a new measurement.
- F3 [UNK]: whether the restarted walker process (restart hooks at `/var/log/pacman.log:3062`, `:3123`) runs the 2.17.2 binary is unknown; this block only says the PID 1808 state is stale.

## Limits

- No live host measurement this round (host pause). The walker binary's compiled-in version literal (the template's S096 item) was NOT read by this seat; S096 is not yet present in `corpus/SOURCES.md` and is owned by the binary-bytes row. The block therefore cites only S090 and does not claim a binary literal.
- Did not check other notes in corpus/knowledge for 2.17.0 pins (out of this seat's sole-writer scope).
- Did not edit corpus/SOURCES.md; no SOURCES row proposed beyond citing S090 as given.
- Blocks in the note beyond line 475 (errata R2-E4 line 405) were not rewritten; the line-405 pin remains as an append-only record.

## Installs

none
