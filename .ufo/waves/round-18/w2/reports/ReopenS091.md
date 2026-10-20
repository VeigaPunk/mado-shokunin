# ReopenS091 — non-author re-open of host row S091 (R17-V3)

Seat: MadoR18.ReopenS091. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`;
row at `corpus/SOURCES.md:103` (baseline integration `4c103b55b1ea5c3c555884afe3eb69b5189701b7`,
receipts `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`, read by hash only).
Read-only check: no git/jj write, no package query, no process/input/screenshot operation,
no walker/elephant execution, no socket. Host files read as bytes (`sha256sum`, `stat`,
`sed -n`, `wc -l`, `python3` byte read); `/var/log/pacman.log` only at the cited lines.

## Commands and observed output

```
$ sha256sum ~/.config/walker/config.toml /etc/xdg/walker/config.toml /usr/bin/walker
fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787  /home/vgpnk/.config/walker/config.toml
3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b  /etc/xdg/walker/config.toml
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker

$ stat -c '%n %s' ...            # 1336 / 13743 / 7039912
$ wc -l ...                      # 49 / 305
$ stat -c '%n | %s | %y' /etc/xdg/walker/config.toml /usr/bin/walker
/etc/xdg/walker/config.toml | 13743 | 2026-10-08 11:14:32.000000000 -0300
/usr/bin/walker             | 7039912 | 2026-10-08 11:14:32.000000000 -0300

$ python3  # byte read, binary never executed
len bin 7039912
bytes at off: b'force_keyboard_focus = false       # forces keyboard forcus '
match at off equal pkg: True
sha of slice 3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b
count exact occurrences of pkg bytes: 1
```

Every number in the row's anchor cell reproduces exactly: user config 1,336 B /
`fecf71fa…` / 49 L; `/etc/xdg` 13,743 B / `3c5c6867…` / 305 L; `/usr/bin/walker`
7,039,912 B / `25240650…`; the embedded default at offset 806,960 is byte-equal to the
packaged `/etc/xdg` file, appears exactly once in the binary, and its slice digest is
`3c5c6867…`.

Cross-checks:

- Packaged file equals the upstream v2.17.2 body: fetch receipt for
  `raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml` records
  13,743 B sha `3c5c6867…` (multiple seat receipts agree), and the saved body
  `fetch/NoteWalker/walker-v2.17.2-resources-config.toml` re-hashes to the same value.
- User config equals the omarchy checkout copy and the fetched v3.8.4 body:
  `sha256sum ~/.local/share/omarchy/config/walker/config.toml` =
  `fecf71fa…`; `fetch/NoteWalker/omarchy-v3.8.4-config-walker-config.toml` = `fecf71fa…`.
- Old-pin side of the `teaches` clause: `walker-deep-r9.md:57,64,69` pin binary
  6,661,264 B sha `64826a85…`, packaged 13,220 B sha `5b4e47b7…`, embedded offset
  784,064; `walker-live-surface.md:113-114` pin the same. The current values therefore
  are moved pins against the 2026-10-14 notes.
- `/var/log/pacman.log` cited lines, read as file lines only:
  `HP:1943` `2026-10-11T16:14:39-0300 … upgraded walker (2.16.2-1 -> 2.17.0-1)`;
  `HP:2929` `2026-10-20T09:16:46-0300 … upgraded walker (2.17.0-1 -> 2.17.2-1)`;
  `HP:3062` (09:18:25) and `HP:3123` (09:31:04) `running 'walker-restart.hook'`;
  `HP:3095` `2026-10-20T09:31:03-0300 … upgraded elephant (2.21.0-1 -> 2.22.1-1)`.
  All five anchors land on the stated lines.

## Judgement

### kind / tier / scope

- **kind `code`** — holds. The row names the host TOML configs and the ELF binary as
  primary artifacts, the same convention as S020 (host config files) and S013 (installer
  code). It is not a restatement of docs.
- **tier A** — holds. For the row's scope (what the host files contain) the files
  themselves are primary, and the anchor fixes them by size, line count and sha256; a
  non-author reproduces the values with three `sha256sum` calls. Nothing secondary sits
  between the scope and the anchor.
- **scope** — holds. "host walker config and binary file bytes on this host, read only"
  names the surface keyword `walker` (P3) and bounds the row to file bytes: it claims no
  runtime state, no process identity and no build fidelity. The citing note keeps those
  as `[UNK]` (`walker-route-r18.md:286-289`), so scope and use agree.

### `teaches` is grounded

1. "moved pins against the 2026-10-14 notes (walker 2.17.0 values superseded)" — true:
   the 2026-10-14 notes carry 13,220 B / `5b4e47b7…` and 6,661,264 B / `64826a85…` /
   offset 784,064; the host now carries 13,743 B / `3c5c6867…`, 7,039,912 B /
   `25240650…`, offset 806,960. (The user-config pin is unchanged at `fecf71fa…`; the
   row does not claim it moved, and the note lists it separately as equal to `OC`.)
2. "the embedded default equals the packaged file" — true: exact 13,743-byte slice at
   806,960 equals `/etc/xdg/walker/config.toml`, exactly one occurrence in the binary.

### the citing note uses it truthfully

`corpus/knowledge/walker-route-r18.md` (sha256 `3ff430a4627d4204ff14c1e9e92eb726a38244ad8c27d8bda412243dfb8fbf20`):

- line 1 (head `source:`) names S091 with the same three-file set and "sha256 in
  § Host declaration" — attribution matches the registry row.
- lines 180-183 table: the three digests, sizes and line counts are byte-for-byte what
  this check measured; the mtimes 2026-10-08 11:14:32 -0300 also match `stat`.
- lines 205-207: "the embedded default config is present exactly once, at file offset
  806,960, and the bytes `b[806960:806960+13743]` equal the `/etc/xdg` file" — measured
  `True`, with occurrence count 1.
- lines 236-242 (§ MOVED pins): old values match `walker-deep-r9.md` /
  `walker-live-surface.md` exactly; new values match the host; the offset move
  784,064 → 806,960 is correct.
- line 170: "Stock user config `OC` is the same 49-line file the host carries" — the
  fetched v3.8.4 body and the checkout copy both hash to `fecf71fa…`.
- lines 219-231 (§ Host version binding) cite the log lines verified above, and
  explicitly refuse to read a log line as a running-binary fact.

No statement found in the note that the row's bytes do not support. The note does not
claim a process probe, a package query, or binary-to-tag identity (kept `[UNK]`).

## Residuals (none change the verdict)

- S091 has no `mado-fetch-receipt-v1` line. That is inherent to a host row (there is no
  URL and no fetched body); its identity is the recorded digests plus the three
  `sha256sum` commands above. Rubric V credits it on tier/status/used-by alone
  (`measure.py` `mined_a`, no receipt join), and the committed after-measure
  (`evidence/measure-after.json.txt:60-85`) lists S091 in P3's `sources_ok`. The
  SCORECARD C2 wording ("each new credited row backed by a committed raw fetch
  receipt") is literally wider than lesson round-18 M6's "web row" narrowing; that is a
  wording gap in C2, not a defect in this row, and P3's credit does not depend on S091
  (upstream https rows S072-S078 supply the required upstream source).
- The row's plural "moved pins" covers the packaged config and binary, not the user
  config, whose pin is unchanged; the row states nothing to the contrary.
- Whether the author read the bytes with `sha256sum` vs `cat -n` is not reconstructable
  from the artifact and is immaterial: the bytes and every recorded value match.

GATE | S091 | /etc/xdg/walker/config.toml | 2026-10-20 | /etc/xdg/walker/config.toml:1 "force_keyboard_focus = false" (3 words) | 3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b | agree: all three anchor digests, sizes and line counts match; the 13,743 B packaged file occurs once in /usr/bin/walker at offset 806960; kind code, tier A and walker scope hold; teaches matches the 2026-10-14 pins; walker-route-r18.md:180-183,205-207,236-242 use them truthfully
