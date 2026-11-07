# R95MExecHostC1 — round 95 w1 report (host seat, C1 coverage arm)

DRAFT pre-freeze evidence, not a measurement. Lane: `mado-shokunin`; declared base `4a2af6817024f6ed47084a5217c1825ae247f4fe` (master); lane tip at seat start `497c6fcd372b817d8423dcd37ece08216012433c` = base + the w1 evidence commit only — `tools/` and `quality/` are byte-equal to base (verified: `git diff --stat 4a2af681..497c6fcd -- tools/ quality/` empty, rc=0; `git status --porcelain -- tools/ quality/` = 0 lines).

## 1. Frozen host file list (owned)

- Path: `.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt`
- **4911 absolute paths under /usr only**, sha256 `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87`, one path per line, sorted, deduped, includes 60 empty regular files (of 20,090 available) and 40 resolved symlink targets (realpath of /usr/bin symlinks).
- Deterministic command: `python3 .ufo/waves/round-95/w1/R95MExecHostC1-mklist.py` (rc=0). Algorithm in the script's docstring: one `os.walk('/usr', followlinks=False)` pass over readable regular files (path, size), 66 buckets, each a sorted (codepoint order, locale-free) list truncated to a fixed quota, union sorted and deduped; no time/randomness/locale/network. Full per-bucket table is printed by the script (elf-exec=350, elf-shlib=350, shebang=250, gz=350, xz=3, zst=30, bz2=30, zip=40, jar=53, icons=350, fonts=200, desktop=124, xml=250, html-json=250, doc=150, zoneinfo=120, terminfo=120, mimedb=18+3, pyscripts=200, perl=100, empty=60, sounds=45, vim=13, i18n=80, x11-drirc=60, glib2=60, certs=2, java=10, symlink-targets=40, gettext-mo=60, pdf=40, postscript=40, jpeg=40, gif=40, webp=98, audio=40, kbd-consolefonts=40, ar-static=40, icc=36, xml-dtd=21, ttc=14, woff=30, lo-templates=60, pyc=20, ico=18, elisp=8, wasm=8, bmp=8, mp3=1, lua=421, type1-fonts=4, netpbm=41, pcx=1, tga=2, bat=10, qml=30, hdr=13, exr=36, cur=140, glb=3, efi=3).
- **Variety: 62 distinct oracle types data-only (aim ≥ 60 met), 78 with the file's own path as the name.** Full lists: `w1/R95MExecHostC1-types-host-dataonly.txt`, `w1/R95MExecHostC1-types-host-names.txt`. Notable SMI-2.5.1-on-this-host findings baked into the hunt: `application/x-sharedlib` is unreachable data-only (the `\x7fELF` executable entry wins cache order for every ELF; confirmed on `/usr/lib/libsqlite3.so.0` and `/usr/lib32/libc_malloc_debug.so.0`), `font/collection` unreachable (all 14 `.ttc` → octet-stream), `image/svg+xml-compressed` (krita.svgz → application/gzip), `application/x-font-sfn` (all consolefonts are .gz), `text/troff` (uncompressed man → text/plain), plain `application/json` (non-$schema JSON → text/plain; only `$schema`-bearing files give `application/schema+json`). Types added beyond the obvious: portable-executable (.efi), wasm, gltf-binary (.glb), image/vnd.radiance (.hdr), image/x-exr, image/x-win-bitmap (.cur), image/x-portable-pixmap/-graymap, image/vnd.zbrush.pcx, image/x-tga, image/bmp, audio/mpeg, text/x-lua, text/x-qml, application/x-bat, application/x-font-type1 (.pfa/.pfb in groff).

## 2. DRAFT candidate-vs-oracle diff on the list (owned)

- Driver: `.ufo/waves/round-95/w1/R95MExecHostC1-run.py` (rc=0, `DRAFT TOTAL_DIFFS=0`).
- Candidate: scratch copy of `.ufo/waves/round-95/build/mado-mimesniff.c1.py` (sha256 `a13b6e0e3b0c399892ff027309f942daa96e92713851e8d8cfb736b277cde99d`) next to a copy of `tools/mado-mimeglob.py` (sha256 `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`) — both shas re-verified at copy time, equal to the declared pins. Oracle compiled in scratch from `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` (rc=0; glib2 2.90.1-1, shared-mime-info 2.5.1-2, `pacman -Q`).
- Four combos × 4911 files, one oracle process and one candidate process per combo, comparing (type, uncertain) per list index — **19,644 comparisons, 0 differences**; candidate exit 0 on every combo:

| combo | env (LC_ALL=C +) | name arg | distinct oracle types | diffs |
|---|---|---|---|---|
| host/dataonly | HOME=/home/vgpnk XDG_DATA_HOME=/home/vgpnk/.local/share XDG_DATA_DIRS=/usr/local/share:/usr/share (this shell's values; user cache `~/.local/share/mime/mime.cache` exists) | NULL | 62 | 0 |
| host/names | same | own path | 78 | 0 |
| synth/dataonly | HOME=$S/home XDG_DATA_HOME=$S/empty-dh (empty dir) XDG_DATA_DIRS=/usr/share | NULL | 62 | 0 |
| synth/names | same | own path | 78 | 0 |

- Host-env and synth-env answer sets are identical (types files diff-empty) — the user cache adds nothing on these inputs. No diff files were produced (no differences to cite).

## 3. Harm harness + base DRAFT run (owned)

- `.ufo/waves/round-95/w1/R95MExecHostC1-harm.sh` (usage from lane root: `MIMESNIFF=<candidate copy> bash .ufo/waves/round-95/w1/R95MExecHostC1-harm.sh REV SCRATCH`): the round-94 watch (`.ufo/waves/round-94/controls/harm-r94.sh`) + its L1 additions (the two round-94 gate runs) **plus `python3 -I "$MIMESNIFF" --selftest`** (MIMESNIFF env-overridable, default `tools/mado-mimesniff.py`, SKIP/rc=NA when not integrated yet) + a second pin diff (`git diff --stat 4a2af681..REV -- tools/ quality/`, empty = byte-equal to the round-95 base). Read-only in the lane: every writable component gets a scratch root under SCRATCH, `TMPDIR=$SCRATCH`; trailing note tells the L1 to append the r95 counters when they land (round-94 pattern).
- Base DRAFT run: rev `497c6fcd…`, MIMESNIFF=scratch candidate copy → **exit 0**; log at `w1/R95MExecHostC1-harm-base-draft.log`. All 18 commands rc=0 except the pre-annotated c1-r90 SETUP_ERROR (rc=2, expected per QUALITY 153): mado-verify selftest 460/460; verify --no-live CLEAN (29 pass/4 notes); check-index indexed=115/115 coverage=10.0000/10; ledger 182/182 TARGET_MET; mako 62/62; portals 28/28; mime 17/17; xdgmime 12/12; mimeglob 19/19; **mimesniff 23/23**; seat-reports 23/23; receipt-presence 6/6; strength selftest 11/11; gate OK kills=32/32, kills=19/19, kills=27/27; c2-r90 TARGET_MET expectations=83/83; c2-r92 TARGET_MET fixtures=45/45 fresh=60/60; c1-r90 SETUP_ERROR as expected; both pin diffs empty.

## Evidence index (exact commands, exit codes)

1. `cc -O0 -o "$S/oracle" .ufo/waves/round-95/controls/mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)` → rc=0 (binary sha256 `186537938e186727072bf911a86117918d505593e77617e53cfa246d425a3aa5`).
2. `python3 .ufo/waves/round-95/w1/R95MExecHostC1-mklist.py` → rc=0 (list sha256 `9d5947a7…`).
3. `python3 .ufo/waves/round-95/w1/R95MExecHostC1-run.py $S` → DRIVER_EXIT=0, DRAFT TOTAL_DIFFS=0.
4. `MIMESNIFF=$S/tools/mado-mimesniff.py bash .ufo/waves/round-95/w1/R95MExecHostC1-harm.sh 497c6fcd… $S/harm` → HARM_EXIT=0.
5. `sha256sum` of both tool copies at setup → match `a13b6e0e…` / `65f80a6c…`.

## Deviations, risks, notes

- No functional defects found in the candidate on 19,644 DRAFT host comparisons. This is a draft probe result, not the (iii) measurement — the counter owns that.
- The frozen list pins sha256 `9d5947a7…`; the counter must pin exactly this. If /usr content changes between freeze and measurement (host package updates — currently paused by PACMAN GUARD), the counter's host arm needs a rebuilt list.
- `/usr/lib/chromium/extensions` is unreadable to non-root; the walk skips it silently (it contributes no readable regular files). No other unreadable path in the buckets.
- No tools installed (cc/pkg-config/python3 present). Pacman guard respected (read-only `pacman -Q` only). No home files read except `~/.local/share/mime/mime.cache` existence/read via the tools under test (allowed database file).
- Scratch `$HYAKU_SCRATCH/mado-r95/R95MExecHostC1` deleted on exit after copying the cited artifacts above.
