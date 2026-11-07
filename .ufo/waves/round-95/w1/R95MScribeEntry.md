# R95MScribeEntry — round 95 wave 1, scribe seat

Seat: leaf (no dispatch). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scratch: `/fast/scratch/hyaku/mado-r95/R95MScribeEntry` (created, used, **deleted on exit**).
Nothing here is a measurement: every run is labelled DRAFT and nothing was written under
`.ufo/waves/round-95/receipts/`.

## 1. Behaviour (what this seat did)

1. Read the declaration draft, the L1's `receipts/sources-open-r95.txt`, round 94's knowledge entry
   (`corpus/knowledge/mime-glob-guess-r94.md`) and the draft candidate
   `.ufo/waves/round-95/build/mado-mimesniff.c1.py` (546 lines, read in full).
2. Re-verified every fetched byte of the lane's `fetch/` (9 files × 2 fetches recorded by the L1) and
   confirmed all nine digests against `sources-open-r95.txt`.
3. Fetched the two ASCII-table sources the decision table needs (`gstrfuncs.c`, `gstrfuncs.h`, both
   HTTP 200, digests identical to the held S511/S512 rows) and the spec body **with the redirect
   followed** (301 → 200, digest identical to S517).
4. Built a 20-line C control for the `data == NULL` API path, compiled the lane oracle, copied the
   candidate beside round 94's tool, and ran three DRAFT drivers:
   - `drv.py` — 51 fixture rows over hand-made `mime.cache` databases (name step, empty data, magic
     entry order, cross-cache priority, range, mask, word size, children, priority 0 / 2^31,
     `looks_like_text` bytes, desktop rule, subclass resolution);
   - `host.py` — 42 inputs against the real `/usr/share/mime/mime.cache`, including synthesised data
     for the eight matchlets that carry `word_size` 2 or 4;
   - `name.py` — 10 name/data rows on the host database.
5. Drafted the knowledge entry in the r94 shape: decision table with a located ≤25-word quote per
   row, ten spec divergences, operator consequences, the tool's argv and verdict map, named limits,
   the DRAFT row table, and draft SOURCES rows (one new row S519 for `xdgmimeint.c`, which no held
   row names; located-line extensions for S505/S516/S518).
6. Extracted all 36 C quotes mechanically from the fetched bytes (`R95MScribeEntry-quotes.py`):
   every quote is verbatim at the cited lines and ≤ 25 words; each file's sha256 was printed with it.

## 2. Gates run (command → result)

| command | result |
|---|---|
| `sha256sum fetch/{xdgmime.c,xdgmimeint.c,xdgmimecache.c,xdgmime.h,xdgmimemagic.c,xdgmimeint.h,gcontenttype-fdo.c,gcontenttype.c,smi-s02.html}` | all nine equal `sources-open-r95.txt` |
| `sha256sum build/mado-mimesniff.c1.py tools/mado-mimeglob.py controls/mimesniff-oracle-r95.c` | `a13b6e0e…e99d`, `65f80a6c…2453`, `99df35f8…124a` (as declared) |
| `cc -O0 -o $S/oracle …/mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)` | rc 0 |
| `python3 -I $S/tools/mado-mimesniff.py --selftest` | `MADO_MIMESNIFF_SELFTEST: checks=23 failed=0`, rc 0 |
| `python3 $S/drv.py` | `ROWS=51 DIFFS=2`, rc 0 (both DIFFs are the VT finding F1) |
| `python3 $S/host.py` | `DIFFS=0` over 42 inputs, rc 0 |
| `python3 $S/name.py` | `DIFFS=0` over 10 inputs, rc 0 |
| `python3 $S/quotes2.py` | 36 quotes, `OVER25: []` |
| `cc -O0 -o $S/nil $S/nil.c … && env -i … $S/nil` | rc 0; `application/octet-stream 1`, `application/octet-stream 1`, `text/plain 0` |
| host VT scan of the L1's 3620-file list | 1152 files carry `0x0b` in the first 4096 B; **0** carry it in the first 128 B without another binary byte |
| host `mime.cache` parse (read-only) | 689 magic entries / 1282 matchlets; `word_size` 1:1274, 2:4, 4:4 |

Fetch provenance for the three URLs this seat fetched (lane QUALITY 158):

| URL | status | bytes | sha256 |
|---|---|---|---|
| `https://specifications.freedesktop.org/shared-mime-info-spec/latest/ar01s02.html` | **301** (Location `http://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html`) → **200** with `-L` | 59208 | `e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e` (two fetches byte-identical; equals S517) |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.c` | 200 | 96685 | `6ea1c4333161ec4e7c85c212cb46200ec331e45f12ccd20c8d018a3fdaa62fd4` (equals S511) |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.h` | 200 | 25254 | `298b0dc4c82805322df7534152b917f9acd54d44e81132988476bb59a6426e23` (equals S512) |

No pacman transaction, no install, no upgrade, no service call, no application launch, no
`update-mime-database`, no mutating git/jj command, no credential material read.

## 3. Touched surfaces (files written)

- `.ufo/waves/round-95/w1/R95MScribeEntry.md` (this report)
- `.ufo/waves/round-95/w1/R95MScribeEntry-entry.md` (the entry draft, `corpus/knowledge/mime-magic-sniff-r95.md` when landed)
- `.ufo/waves/round-95/w1/R95MScribeEntry-drv.py`, `…-drv.out.txt`
- `.ufo/waves/round-95/w1/R95MScribeEntry-host.py`, `…-host.out.txt`
- `.ufo/waves/round-95/w1/R95MScribeEntry-name.py`, `…-name.out.txt`
- `.ufo/waves/round-95/w1/R95MScribeEntry-quotes.py` (the quote extractor/verifier)
- `.ufo/waves/round-95/w1/R95MScribeEntry-case-vt.json` (the reproducing case, shared schema)
- `.ufo/waves/round-95/w1/R95MScribeEntry-nil.c` (the `data == NULL` control)

Nothing else was written: no `tools/`, `quality/`, `corpus/`, declaration, candidate, control, wave
input, receipt or fleet-root file. The scratch directory was removed after the copies above.

## 4. Findings

### F1 (C1 candidate defect) — `0x0b` is binary in GLib, text in the candidate

- GLib: `looks_like_text` rejects any byte that is `g_ascii_iscntrl` and not `g_ascii_isspace` and
  not `'\b'` (`fetch/gcontenttype-fdo.c`:542-544). GLib 2.90.1's table gives byte 11 (VT) `0x004`
  — CNTRL, **no** SPACE bit — while TAB/LF/FF/CR carry `0x104`
  (`fetch/gstrfuncs.c`:264, verified bytes: `0x004, 0x104, 0x104, 0x004, 0x104, 0x104, 0x004, 0x004`;
  bits at `gstrfuncs.h`:48 and `:54`). The fallback also treats VT as a control byte
  (`fetch/xdgmimeint.c`:185). So a buffer with `0x0b` in the first 128 bytes and no other binary
  byte answers `application/octet-stream` **1**.
- Candidate: `.ufo/waves/round-95/build/mado-mimesniff.c1.py:208`
  `return not any(b < 8 or 14 <= b < 32 or b == 127 for b in data)` — 8…13 are all treated as
  non-control, i.e. as `g_ascii_isspace` would. Its selftest row `s10` at `:467`
  (`"s10 VT passes looks_like_text", … == ("text/plain", 0)`) encodes the wrong expectation, so
  `--selftest` still prints `checks=23 failed=0` and cannot catch it.
- Reproducing input (shared case schema, file `R95MScribeEntry-case-vt.json`; class `lltext`):

  ```json
  {"id":"lltext-01-vt","class":"lltext",
   "env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},
   "files":{"dh/mime/mime.cache":"<b64 of the candidate's build_cache() — 80 bytes, sha256 405417a464a68c950f90c2ac799f780e93df7d6997e67d3c57cfdae3d63943af>"},
   "inputs":[{"name_b64":null,"data_b64":"YWILY2Q="}],
   "labels":[["application/octet-stream",1]]}
  ```

  Oracle line: `application/octet-stream\t1`; draft candidate: `text/plain 0`
  (`R95MScribeEntry-drv.out.txt` rows `f-vt`; the same divergence with `0x08` also present, row
  `f-vt-early`).
- Reach of the L1's pre-wave probe: it cannot see this. Of the 3620 listed `/usr` files, 1152 carry
  `0x0b` in the first 4096 bytes, but **none** carries it in the first 128 bytes without another
  binary byte, and every one of those files is magic-matched anyway.
- Still present in the L1's revision: `.ufo/waves/round-95/build/mado-mimesniff.c1b.py`
  (sha256 `abef00143e306fbdc970cc04b2af576e492e570a2b5d6430bf09f97f6895006c`) carries the same
  `looks_like_text` at `:209` and the same `s10` row at `:468` (read-only check, no rerun).
- Not a defect: `0x08` (text via the `'\b'` exemption), `0x0c` (text via `isspace`), `0x7f`
  (text, because the fallback never returns the sentinel for it). Rows `f-bs`, `f-ff`, `f-del`
  agree with the oracle.

### F2 (`fetch/smi-s02.html` is a redirect body, not the spec)

The lane's `fetch/smi-s02.html` (109 B, sha256 `1566c4594b825fde8bda64c8136a856e46df6e645a13236f1356097fdc6a3c66`)
is the body of a **301**: `<a href="http://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html">Moved Permanently</a>.`
The `sources-open-r95.txt` note that "served bytes vary over time" against round 94's `e00fa00e…`
is therefore a fetch-without-`-L` artefact, not content drift: following the redirect returns
59208 B with sha256 `e00fa00e…c61e`, exactly round 94's digest (two fetches byte-identical). The
entry's spec quotes come from the followed body.

### F3 (spec divergence worth a frozen case) — `WORD_SIZE` is never read

`cache_magic_matchlet_compare_to_data` reads offsets +0, +4, +12, +16, +20 (and +24, +28 in the
parent) — `WORD_SIZE` at +8, which spec §2.9 defines and §2.5 defines as byte-swapping, is never
loaded (`fetch/xdgmimecache.c`:173-177, `:218-219`; raw compare at `:202`). On this host 8 of 1282
matchlets carry 2 or 4 (`x-cpio`, `x-executable`, `vnd.tcpdump.pcap`, `x-java-jce-keystore`,
`x-pcapng`), and synthesised data holding each stored value at its stored offset matched all of them
through the oracle and the candidate alike (`R95MScribeEntry-host.out.txt`, rows `word2-*`/`word4-*`).
Not a candidate defect; a documented divergence (entry D2).

### F4 (desktop shield boundary) — the shield applies only to untyped names

`fetch/gcontenttype-fdo.c`:636-638 rewrites a *sniffed* `application/x-desktop` to `text/plain`
whenever `filename != NULL`, but a name that already yields exactly one type returns at `:613-620`
without sniffing. On this host `x.desktop` and `whatever.desktop` therefore answer
`application/x-desktop` **0**, while `zz.nomatch` answers `text/plain` 0
(`R95MScribeEntry-name.out.txt`). A frozen case built on "any name ⇒ text/plain" would be wrong;
the entry states the boundary in §2.5 and §4.6.

### F5 (evidence shape) — the class list needs a byte-level row

No class in the frozen schema forces a `looks_like_text` boundary byte. `lltext` is the natural
home: F1 is `lltext-01-vt`; `0x0c`, `0x08`, `0x7f` alone, `0x7f` with `0x01`, `0x01` at index 127
and 128, and `0x0b` at index 130 (all verified, §7 of the entry) close the window rule.

## 5. Out of scope (not done, by assignment)

- No frozen cases, no fresh generator, no mutants, no counter, no panel, no kill-sets, no receipt:
  those paths belong to the exec and mutation seats and to the L1.
- No measurement and no DRAFT_* counter run was made from this seat.
- The candidate was read, hashed and exercised as a **copy**; it was not edited (F1 is routed to the
  L1, not fixed here).
- Text mode (`magic` files, `xdgmimemagic.c`), `magic-deleteall`, and the caller/connector question
  are declared limits of the entry, not findings.
- `gstrfuncs.c`/`gstrfuncs.h` were fetched by this seat (S511/S512 already hold the same digests);
  if the L1 prefers a lane-fetched copy in `fetch/`, they are reproducible from the URLs above.

## 6. Artifacts

- entry draft: `.ufo/waves/round-95/w1/R95MScribeEntry-entry.md`
- row evidence: `R95MScribeEntry-drv.out.txt` (51 rows), `R95MScribeEntry-host.out.txt` (42 inputs),
  `R95MScribeEntry-name.out.txt` (10 inputs)
- drivers: `R95MScribeEntry-drv.py`, `R95MScribeEntry-host.py`, `R95MScribeEntry-name.py`
- quote verifier: `R95MScribeEntry-quotes.py`
- reproducing case: `R95MScribeEntry-case-vt.json`; `data == NULL` control: `R95MScribeEntry-nil.c`
- scratch `/fast/scratch/hyaku/mado-r95/R95MScribeEntry`: **removed on exit**.
