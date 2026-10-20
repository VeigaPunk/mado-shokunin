# PtrWalkerDeep — R18-V3 freshness pointer appended to walker-deep.md; prior bytes verified unchanged, only 2.17.0 pin (line 27) dated

## Behaviour

Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/walker-deep.md` (sole writer this wave). One append-only block was added at the tail; no existing byte was changed.

## Findings

- F1 — version pins. `grep -n '2\.17\.0'` on the note returns exactly one line: `27:` (`walker --version` → `2.17.0`; pkg `2.17.0-1`). `grep -n '2\.17\.2'` returned nothing before the edit. The pointer therefore lists `lines 27`.
- F2 — before state: sha256 `0982ba066c72575a02732b99be5e6940ee72a437588b1fc2d2cac2ff9a576df8`, 38,403 B, 617 LF, final byte `_` (no trailing newline). Pre-edit copy kept at `/tmp/walker-deep.before-r19.md` (scratch).
- F3 — after state: sha256 `4096f386eb8642643bea31ec2dc9952de26a4011202895906285a5c2419f0f79`, 40,127 B.
  - `cmp -n 38403 /tmp/walker-deep.before-r19.md walker-deep.md` → identical (PREFIX_OK).
  - sha256 of the first 38,403 bytes of the new file → `0982ba066c72575a02732b99be5e6940ee72a437588b1fc2d2cac2ff9a576df8` (equals the before sha256).
- F4 — appended block occupies lines 619–626; heading `## Freshness pointer (round 19, 2026-10-20)` at line 620; four bullets at lines 622–626 (line 622 holds `2.17.2`, `S090` and `S096`). Block is 8 lines (under the 20-line cap). It sits below the existing `## Errata (append-only)` placeholder, because that is the file's tail; it is a pointer, not an errata entry.
- F5 — host bytes read for the pointer (file bytes only; no walker/elephant/pacman/systemctl run):
  - `sed -n 2929p /var/log/pacman.log` → `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`.
  - `sha256sum /usr/bin/walker` → `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`; `grep -a -o -E 'walker [0-9]+\.[0-9]+\.[0-9]+|2\.17\.[0-9]+'` → one match, `2.17.2` (no `2.17.0` literal matched).
  - `/etc/xdg/walker/config.toml`: 13,743 B, mtime 2026-10-08 11:14:32 -0300, sha256[:16] `3c5c6867d0216d0c8643` — differs from the note's L1 pin (13,220 B, `5b4e47b7d2314bf8`, mtime 2026-07-26). The 13,743 B size matches walker-route-r18.md WC.
  - `~/.config/walker/config.toml`: 1,336 B, sha256[:16] `fecf71fa4253803e` — unchanged vs the note's L2 pin.
- F6 — claim families classed in the pointer:
  - walker-version-bound and dated 2026-10-14: `--help` table (§5), embedded-default byte run at offset 784,064 (§2.1), struct/field-arity and error/fallback tokens (§2.2–2.3, §6.1, §6.3), `/etc/xdg` line anchors (§2.1–2.4, §4.2, §7.4).
  - elephant-bound and dated: `elephant version` 2.21.0 (line 28), listproviders census and plugin list (§4.1), ElephantConfig defaults and generated-doc counts. S090 line 3095 records elephant 2.21.0-1 -> 2.22.1-1.
  - not walker-version-bound, dated 2026-10-14 and not re-measured: elephant user TOML and menu Lua hashes, theme hashes, omarchy script anchors (§5, §7), process/session state (§1 PIDs, sockets, `hyprctl -j layers`, §7.1 binds). Only the user `config.toml` was re-read this round (unchanged).
  - [INFERENCE] a PID observed on 2026-10-14 runs the pre-upgrade image; not checked.
- F7 — `S096` is cited as the template requires, but no `S096` row exists in `corpus/SOURCES.md` (only `S090` at line 102 was found). The citation dangles until L1 registers S096 (reserved: host walker bytes). I did not write SOURCES.md.
- F8 — other owned-file pins: walker-deep-r9.md and walker-live-surface.md also carry 2.17.0 per walker-route-r18.md's header; they are outside this assignment and were not touched.

## Limits

- Not run: walker, elephant, omarchy-*, systemctl, journalctl, pacman (any form), hyprctl, live gate. Host reads were byte-level only (sha256sum, stat, grep -a, sed -n, cmp).
- Behaviour of the 2.17.2 binary is unobserved and stays [UNK]; no `strings` or help-text diff was run against 2.17.2, so the note's `--help` table and token lists are still unverified for 2.17.2.
- Did not compare the new `/etc/xdg/walker/config.toml` with the embedded default in the 2.17.2 binary.
- Did not re-measure elephant, omarchy, theme, or process state.
- Did not verify the pointer's `S090` line numbers beyond the SOURCES.md row text.

## Installs

none
