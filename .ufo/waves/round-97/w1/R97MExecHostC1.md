# R97MExecHostC1 — host leg report (round 97, w1)

Seat deliverables, all present and frozen-ready. Everything below is measured on this
host (glib2 2.90.1-1, shared-mime-info 2.5.1-2, file 5.48-1, xdg-utils 1.2.1-2), base
rev `e6152b589c2c6a28426c28263c4bcc3c46398be4`.

## Files changed (lane-relative)

| file | sha256 | purpose |
|---|---|---|
| `controls/filetype-host-r97.txt` | `4f28035b4cfea0b3f6d8d9f5eb3efb630b2a09db4fc06fa141555e76a9a829a4` | 11834 absolute host paths + reason metadata |
| `controls/host-db-r97.json` | `0c6c0c0c7f62353777053bb77b33bca4cb01a23d0e5ab81eaa5c8d9d00518562` | 9-file host MIME DB manifest (8 text + mime.cache), bytes+sha256 |
| `controls/filetype-fresh-r97.py` | `c3143775d346921085a4f312eb596bc9b062abb11c3257aed47d9bba50bf7bf2` | seeded fresh case generator, labels measured live via gio (label entries are one-element lists per contract 2) |
| `receipts/host-leg-r97.txt` | (receipt) | census, manifest, DROP lists, volatility notes, dry run |
| `w1/R97MExecHostC1.md` | (this file) | report |

## 1. Host list (input 1 of 3) — census

11834 paths (floor was >=1800; declaration predicate wants >=1500). Chain:
12278 raw reasoned walk → 12042 after the credential filter (236 dropped, §3) →
11837 after the volatility pass (67 unreadable-at-freeze, 138 `/proc/<pid>≠1`) →
11834 after dropping 3 self-referential fd symlinks.

- Kinds: file 6403, dir 4473, symlink 850, chardev 94, blkdev 11, socket 3.
- Roots: /home 5640 (~/.config names only), /usr 5234 (mime tree 1170 = full
  `/usr/share/mime` depth≤3 incl. all 9 DB files, doc 1739, icons 600, bin 987,
  lib 593, applications 122, pixmaps 23), /etc 771, /dev 111, /sys 64, /proc 14
  (declared only, no per-pid paths).
- Oracle leg (measured): `env -i LC_ALL=C HOME=<empty> XDG_DATA_DIRS=/usr/share/mime
  /usr/bin/gio info -a standard::content-type` over the shipped population answered
  **11837/11837, 0 errors**; labels: text/plain 4984, inode/directory 4492,
  application/octet-stream 1899, application/x-zerosize 245, inode/symlink 96,
  inode/chardevice 95, inode/blockdevice 14, inode/socket 9, inode/fifo 3.

## 2. Host DB manifest (input 2 of 3)

Nine files with bytes+sha256 (full table in the receipt §2). Key facts:

- All eight text hashes equal the round-96 pins; globs2 equals the r94→r96 pin chain
  (`556ee69c8be2…958168e`) — no DB drift since round 94.
- `mime.cache` is 207520 B → loadable → a reachable `/usr/share/mime` is cache mode;
  the counter must copy only the 8 text files for a text-mode leg (recipe in the JSON).

## 3. Credential-shaped filter (L1 instruction, answered)

**236 dropped, 12042 kept** at filter time; the shipped list is 11834 after the
volatility passes. Breakdown: token 74, auth 71, .pem 53, shadow 4, .key 4, passwd 4,
keyring 4, secret 4, credential 3, .gnupg 1, dir-prefix 14
(`~/.config/{gh,anthropic,elevenlabs,omp}`, `~/.local/share/keyrings`, `~/.aws`,
`~/.docker`). Per-path DROP list with reasons: `receipts/host-leg-r97.txt` §4.

## 4. Fresh generator (input 3 of 3) — 20-case dry run

`python3 -I controls/filetype-fresh-r97.py --seed 97a1 --dir S/roots --count 20 --out S/env.jsonl`
(stdout = one JSON case per line; census on stderr):

- 20 cases, 72 paths, 0 dropped, 0 empty; all 15 classes present;
  db_modes text 16 / cache 1 / none 3.
- Label census: octet-stream 7, x-executable 1, x-zerosize 5, image/png 5,
  inode/blockdevice 6, inode/chardevice 12, inode/directory 14, inode/fifo 4,
  inode/socket 3, inode/symlink 8, text/plain 6, text/x-shellscript 1.
- Full 120-case run (same seed): 120 cases, 430 paths, 0 dropped, 0 empty, 15×8
  classes, text 49 / cache 33 / none 38, 17 distinct labels (receipt §3).
- Determinism: two 20-case runs byte-identical (cmp clean).
- Labels are measured at generation time by the installed gio
  (`d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`), never copied.
- Guaranteed legs via canonical first-occurrence combos: text-DB magic hit
  (uncertain #0: PNG bytes under `multi.dat` → `image/png`), cache-DB magic hit,
  none-DB name-fail (`certain #0`: `pic.png` → `application/octet-stream` with no
  database), the fast gate (`uncertain #3`), and the symlink loop under nofollow
  (`brok #0`). ERROR-labelled paths are dropped from cases (counted), so every fresh
  case is scoreable end-to-end; the refusal leg stays with the frozen case file.

## Findings for the L1 (falsifier-grade, none widen the claim)

1. **Self-referential labels are a real measurement hazard**: `/dev/stdin`,
   `/dev/stdout`, `/dev/stderr` answered `inode/fifo` in follow mode because gio's
   stat resolves them through the *querying process's own* `/proc/<pid>/fd` — the
   label depends on the caller's fd wiring, not the filesystem. Dropped from the
   frozen list with a counted note; any host leg someone rebuilds must exclude them.
2. **Volatile paths must not be frozen**: 138 `/proc/<pid>` entries (they rotate by
   design) and 67 paths unreadable at freeze (chromium/Brave session stores
   mid-rotation, exited PIDs) are excluded. Residual risk: a `~/.config` file present
   now could still vanish before the counter runs → one ERROR stat on the host leg.
   If that happens at freeze, re-run the walk recipe (report §5 of the receipt has the
   exact filters) rather than freezing today's bytes.
3. **Trailing slash is normalised by gio's path layer**: `sub/` and `h/` answered
   `inode/directory` like their bare forms (measured); the declaration's "trailing /
   → inode/directory uncertain" applies to the *guess* step (basename `/`), not to
   `gio info` on a real dir path. The frozen case seat should probe file+`/` (ENOTDIR)
   separately — my fresh cases only cover dir+`/`.
4. **Scratch anomaly (transient, resolved)**: two scratch files
   (`host-list-final.txt`, `dropped-volatile.txt`) vanished mid-session while sibling
   files in the same dir survived; both were regenerated deterministically from the
   surviving `host-list-filtered.txt`. No lane file was affected. Flagging in case a
   sibling seat is sweeping `/fast/scratch/hyaku/mado-r97/*` beyond its own dir.
5. **Sibling files in `controls/` I did not touch**: `harm-r97.sh`,
   `run-decl-counter.py`, `sanitize-host-list.py`, `filetype-cases-r97.json`,
   `filetype-probe-r97.py` (other seats' write scope; mine are the three files in the
   table above).

## Interface note for R97MExecCounterC1 (fresh leg)

- `--seed HEX` (any seed works; the counter seat draws it at measurement time and
  honours a `MADO_R97_FRESH_SEED` env override for L1 replay).
- `--dir D` caller-given, `--count N` default 120, `--out FILE` optional; validated
  at the counter's declared shape `--seed HEX --dir D --out F --count 140`.
- stdout: exactly one JSON object per case (pure JSONL, no progress lines):
  `id, class, db_kind, env, files, mode, attr, paths[], labels[], dropped_paths[]`.
- `labels[i]` corresponds to `paths[i]` and is contract-2 shaped: a one-element list
  `["<type>"]`; each case holds 1..12 paths after dropping; **no label is ever
  `"ERROR"`** (such paths are dropped, with counts in `dropped_paths`).
- `env` follows shared contract 2 (`HOME={root}/h`, `XDG_DATA_HOME={root}/dh`,
  `XDG_DATA_DIRS={root}/db`); `files` carries the db tree as base64 when db_kind is
  text/cache, `{}` for none; `db_kind`/`class`/`dropped_paths` are additive metadata
  beyond the contract's field list.

## Tooling record

No tools installed or upgraded (pacman paused host-wide; nothing needed beyond
stdlib + the installed gio). No services touched; every probe read-only; no
compositor, config, or credential reads. Scratch `S` deleted at completion; receipts
and controls copied into the wave tree first.

## Checks for the main agent / L1

```sh
sha256sum .ufo/waves/round-97/controls/filetype-host-r97.txt \
          .ufo/waves/round-97/controls/host-db-r97.json \
          .ufo/waves/round-97/controls/filetype-fresh-r97.py
# expect 4f28035b…a829a4 / 0c6c0c0c…18562 / c3143775…bf7bf2
python3 -I .ufo/waves/round-97/controls/filetype-fresh-r97.py --seed 9f3a \
  --dir <scratch>/roots --count 140 --out <scratch>/env.jsonl   # the counter seat's declared shape
# expect: cases=140 paths=506 dropped_paths=0 empty_cases=0 rc 0; stdout pure JSONL;
# every labels[] entry a one-element list, arity 1..12 (fresh labels are one-element lists)
grep -c '^DROP-CRED' .ufo/waves/round-97/receipts/host-leg-r97.txt   # expect 236
grep -vc '^#\|^$' .ufo/waves/round-97/controls/filetype-host-r97.txt # expect 11834
```
