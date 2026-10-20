# PtrWalkerDeepR9 — R18-V3 freshness pointer appended to walker-deep-r9.md; prefix byte-identical

## Scope and behaviour

- Sole writer: `corpus/knowledge/walker-deep-r9.md` (append-only). No other file written.
- Edit: one block appended after the final line (`_End of note. …_`). The block is an H2 `## Freshness pointer (round 19, 2026-10-20)` with 5 bullets; first bullet contains both `2.17.2` and `S090` (and the reserved `S096` token) on one line, plus the route pointer `corpus/knowledge/walker-route-r18.md`.
- Every bullet is version-bound vs. not version-bound:
  - version-bound and dated: printed `--version` bytes, binary identity (sha256, size, mtime, BuildID, `.comment`, rodata offset 847,791), package row and `pacman -Qkk` count, help-family shas, packaged `/etc/xdg` default config size/sha, embedded-config offset 784,064;
  - not version-bound, dated 2026-10-14, not re-measured: user `config.toml` sha, autostart desktop sha, unit state, PIDs, socket stat, layer rows;
  - mechanism (read-once, no reload verb) cited to walker-route-r18.md for the v2.17.2 tree, live discriminator kept `[UNK]`;
  - 2.17.2 binary behaviour kept `[UNK]`.
- No new facts were added beyond the note, S090 and walker-route-r18.md.

## Lines of the note containing `2.17.0` (grep -n, pre-edit, 10 lines)

`30, 58, 60, 78, 103, 110, 111, 305, 316, 317`

All ten are cited in the new bullet 1 list and classified in bullets 2–3.

## Digests and prefix check

| | sha256 | bytes | lines (grep -c '' basis) |
|---|---|---|---|
| before (`/tmp/PtrWalkerDeepR9.old.md`, copy of note) | `a5acfe0162c9e5cd05cc3c2ab11dc9ad394d710e8673723feb1e39c3b39a48c7` | 24391 | 399 (no trailing LF on last line) |
| after (note) | `502cb61dd7aea3935178db4cd8b14172255fcc1e0b1d6598a79291c4df2ebb75` | 25976 | 407 |

- `head -c 24391 <note> | sha256sum` → `a5acfe01…48c7` (equals the before digest).
- `cmp -n 24391 /tmp/PtrWalkerDeepR9.old.md <note>` → identical (`PREFIX_IDENTICAL`).
- Appended region: 25976 − 24391 = 1585 bytes; the tool inserted one LF after the former last line (no content of the old prefix changed) plus the block.

## Host observations (file bytes only, this round)

- `sed -n '2925,2930p' /var/log/pacman.log` → line 2929: `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)` — confirms S090 line 2929.
- `sha256sum /usr/bin/walker` → `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`, which is not the note's 2.17.0 pin `64826a85…`. The note does NOT re-assert this value; the bullets say only that the binary identity is version-bound and superseded. The digest is recorded in walker-route-r18.md (§ Host declaration) and was not copied into the note (no new facts beyond the allowed sources).

## Findings

1. R18-V3 freshness pointer for walker-deep-r9.md: done, append-only, prefix verified.
2. The note's walker 2.17.0 pins are now explicitly dated and bound; no live value re-asserted.
3. The printed-version, binary-identity and package claims in the note are superseded for the host by S090 line 2929; the 2.17.2 behaviour remains `[UNK]`.

## Limits

- Did not re-measure any host file beyond the two reads above; did not open any walker, elephant, omarchy, systemd, pacman or compositor surface (host pause).
- Did not check the S090/S096 row text in corpus/SOURCES.md beyond the grep excerpt; S096 is a reserved id not yet present as a row in the note's sources (the header text was supplied by the assignment).
- Did not re-verify walker-route-r18.md's v2.17.2 source claims (cited only as the route pointer).
- Did not run any gate, selftest or `measure.py`.

## Installs

none
