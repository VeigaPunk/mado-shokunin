# R95MConnector — UFO-FSD Connector Report (Round mado 95, Wave w1)

**Seat**: `R95MConnector`  
**Role**: UFO-FSD connector / leaf member  
**Report target**: `.ufo/waves/round-95/w1/R95MConnector.md`  
**Base revision**: `4a2af6817024f6ed47084a5217c1825ae247f4fe` (`master`)  
**Declared axes**: C1 `coverage` (new surface, file bytes → MIME type via `mime.cache` MAGIC section), C2 `operability` (`check-selftest-strength.py` gate guards `mado-mimeglob.py` and `mado-portals.py`).

---

## 1. Sibling Sweep

We swept all sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` (read-only), checking `PROVINCE.md` and `corpus/knowledge/*.md` for MIME magic, content sniffing, `file(1)`, `libmagic`, and `shared-mime-info`:

1. **`audio-shokunin`**: References `--magic`, SoX autodetect, `libsndfile` + `libmagic` linkage, and container sniffing for audio formats (`act`, `au`, `wav`, etc.). Scope: audio container payloads and SoX driver flags.
2. **`chousa-shokunin`**: References `openat2` `RESOLVE_NO_MAGICLINKS`, RFC 5147 `text/plain` MIME entities, and gate baseline magic lines. Scope: syscall flags and kernel man page truth.
3. **`kagi-shokunin`**: References SQLite 3 format header magic string (`SQLite format 3\0`) in database state shape census (`PROVINCE.md:54`). Scope: local credential/state stores.
4. **`kaidoku-shokunin`**: References `file(1)` for ASAR/PE/ELF triage (`2026-10-13-asar-surface.md`, `2026-10-13-pe-surface.md`), `readelf` wrong-magic rejection, `NVUCODES` firmware magic, AppImage squashfs magic, and V8 bytecode magic `0xC0DE06C3`. Scope: reverse-engineering format heuristics.
5. **`revenger-shokunin`**: Holds extensive coverage of `magic(5)` (S176, Arch `core/file 5.48-1`), `file(1)` magic manual (S190, darwinsys/file), `libmagic` definitions, Corkami polyglot format abuse (S181), and format-specific magic bytes (Mach-O, PE, CLI metadata, MSF, Go pclntab). Scope: binary analysis and format disassembly.
6. **`souji-shokunin`**: References git pathspec magic `:(top)` and `GIT_LITERAL_PATHSPECS`. Scope: repository hygiene and git tree filtering.
7. **`tabi-shokunin`**: References PNG magic bytes in browser screenshot validation (`Page.captureScreenshot`), and HTTP response `mimeType`. Scope: browser automation (CDP / WebDriver BiDi).
8. **`tameshi-shokunin`**: References magic byte length probes in mutation testing. Scope: mutation harnesses.
9. **`tsukuroi-shokunin`**: References pacman hooks `30-update-mime-database.hook` and `shared-mime-info-remove-cache.hook` (`pacman-hook-order-r38.md:53,97`), and kernel module `VERMAGIC_STRING`. Scope: system update safety and package manager transaction hooks.

### Sibling Ownership Verdict
**No sibling lane owns XDG shared-mime-info or GLib MIME magic content sniffing.** `mado-shokunin` exclusively owns the XDG desktop/MIME stack (`mime.cache`, `globs2`, `magic`, `mimeapps.list`, `defaults.list`, portals, and desktop defaults).

### What `mado` must cite rather than absorb
- **`tsukuroi-shokunin`**: Pacman post-transaction hook `30-update-mime-database.hook` runs `/usr/bin/update-mime-database /usr/share/mime` to compile `packages/*.xml` into `mime.cache`. `mado` cites this hook as the system producer of `mime.cache`, but does not absorb hook ordering or pacman transaction lifecycle.
- **`revenger-shokunin`**: `file(1)` and `magic(5)` (darwinsys/file, libmagic) are reverse-engineering heuristics. `mado` cites `file(1)` as the distinct fallback classifier used by `xdg-utils` on unrecognised desktops, but does not absorb libmagic rule grammar or heuristic format signatures.

---

## 2. Callers and the GIO Substrate (QUALITY 154)

### 2.1 GLib 2.90.1 `glocalfileinfo.c` Fetch Receipts (QUALITY 158)
Fetched twice independently from upstream GitLab:
- **URL**: `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/glocalfileinfo.c`
- **Fetch 1**: HTTP 200, SHA-256 `b006a93d8a9733ad9245aba396ca7e3ee42019e214f3addd6e873dbd7d334497`
- **Fetch 2**: HTTP 200, SHA-256 `b006a93d8a9733ad9245aba396ca7e3ee42019e214f3addd6e873dbd7d334497`
- **Status**: Identical digests verified.

### 2.2 GIO Content Sniffing Lines in `gio/glocalfileinfo.c`
GIO's `g_file_query_info()` queries file attributes through `_g_local_file_info_get()`, calling internal helper `get_content_type()` (lines 1300–1378):
- **Line 1337**: Initial filename-only guess:
  ```c
  content_type = g_content_type_guess (basename, NULL, 0, &result_uncertain);
  ```
- **Line 1340**: Sniff precondition (`fast` is FALSE for `standard::content-type`, TRUE for `standard::fast-content-type`):
  ```c
  if (!fast && result_uncertain && path != NULL)
  ```
- **Line 1345**: Fixed stack buffer allocation (16 KiB):
  ```c
  guchar sniff_buffer[16384];
  gsize sniff_length;
  ```
- **Line 1351**: Sniff length determined by cache extents:
  ```c
  sniff_length = _g_unix_content_type_get_sniff_len ();
  ```
  `_g_unix_content_type_get_sniff_len()` in `gio/gcontenttype-fdo.c:55-66` calls `xdg_mime_get_max_buffer_extents()`, which in `gio/xdgmime/xdgmimecache.c:727-750` reads `max_extent` at byte offset 28 (the magic header section: `offset = GET_UINT32(cache->buffer, 24)`, reading `offset + 4`). On this host's `/usr/share/mime/mime.cache`, `magic_offset = 112992`, `num_entries = 689`, `max_extent = 18730`.
- **Lines 1352–1353**: Sniff length clamped to 16 KiB buffer:
  ```c
  if (sniff_length == 0 || sniff_length > sizeof (sniff_buffer))
    sniff_length = sizeof (sniff_buffer);
  ```
- **Lines 1356–1361**: Open file with `O_RDONLY | O_NOATIME | O_CLOEXEC`:
  ```c
  #ifdef O_NOATIME
    fd = g_open (path, O_RDONLY | O_NOATIME | O_CLOEXEC, 0);
    errsv = errno;
    if (fd < 0 && errsv == EPERM)
  #endif
      fd = g_open (path, O_RDONLY | O_CLOEXEC, 0);
  ```
- **Lines 1368–1374**: Read up to `sniff_length` bytes and call `g_content_type_guess` with data:
  ```c
  res = read (fd, sniff_buffer, sniff_length);
  (void) g_close (fd, NULL);
  if (res >= 0)
    {
      g_free (content_type);
      content_type = g_content_type_guess (basename, sniff_buffer, res, NULL);
    }
  ```
- **Lines 2065, 2080**:
  - `standard::content-type`: `fast = FALSE` (performs content sniffing).
  - `standard::fast-content-type`: `fast = TRUE` (skips content sniffing, filename only).

### 2.3 Programs on THIS Host Calling `g_content_type_guess` or `g_file_query_info`
1. **Direct `g_content_type_guess` callers**:
   - `/usr/bin/gtk4-rendernode-tool` (imports `g_content_type_guess` from `libgio-2.0.so.0`).
   - `/usr/bin/anydesk` (imports `g_content_type_guess`).
   - Python applications via `from gi.repository import Gio; Gio.content_type_guess(...)`.
2. **`g_file_query_info` content-sniffing callers (`standard::content-type`)**:
   - `/usr/bin/gio` (`gio info <file>` sniffs file data; observed on `/etc/os-release`: `standard::content-type: text/plain` vs `standard::fast-content-type: application/octet-stream`).
   - `/usr/bin/walker` (Hyprland application and file launcher; links `libgio-2.0.so.0` and imports `g_file_query_info`).
   - `/usr/bin/waybar` (links `libgio-2.0.so.0`).

### 2.4 Does `xdg-open` on Hyprland Use It?
**NO.** `xdg-open` on Hyprland does not use `g_content_type_guess`, GIO, or `mime.cache` content sniffing:
1. `/usr/bin/xdg-open` is a shell script from `xdg-utils 1.2.1-2`.
2. Line 1189 invokes `detectDE`.
3. In `detectDE()` (lines 441–558), `case "${XDG_CURRENT_DESKTOP}"` recognizes only `Cinnamon`, `ENLIGHTENMENT`, `GNOME*`, `KDE`, `DEEPIN`, `LXDE`, `LXQt`, `MATE`, `XFCE`, `X-Generic`. `Hyprland` matches none. Fallback session variables also find nothing.
4. Lines 1191–1193 set `DE=generic`.
5. Line 1261 dispatches `generic) open_generic "$url" ;;`.
6. In `open_generic()` (lines 1073–1110), line 1081 queries the file type:
   ```sh
   filetype="$(xdg-mime query filetype "$file" | sed "s/;.*//")"
   ```
7. In `/usr/bin/xdg-mime`:
   - `detectDE` leaves `DE` unrecognised; lines 1420–1422 hit `*) info_generic "$filename" ;;`.
   - In `info_generic()` (lines 844–852):
     ```sh
     if mimetype --version >/dev/null 2>&1; then
         DEBUG 1 "Running mimetype --brief --dereference \"$1\""
         mimetype --brief --dereference "$1"
     else
         DEBUG 1 "Running file --brief --dereference --mime-type \"$1\""
         /usr/bin/file --brief --dereference --mime-type "$1" 2> /dev/null
     fi
     ```
   - `command -v mimetype` returns exit 1 (not installed on host).
   - Line 851 executes `/usr/bin/file --brief --dereference --mime-type "$1"`.
8. **Conclusion**: On Hyprland, `xdg-open` uses `file(1)` (libmagic), completely bypassing GLib's `g_content_type_guess` and `mime.cache`. Contrast with `DE=gnome`, where `xdg-mime` calls `info_gnome` (line 811), running `gio info "$1" | grep standard::content-type`.

---

## 3. Assimilation Scope Check

We inspected `/home/vgpnk/Projects/shokuknow/merge/mado/` (read-only):
- Staged package: `corpus-expansion-1` (147 proposed source rows S203–S349, 69 staged knowledge entries).
- Inventory: All staged entries cover legacy rounds 1–16 / 25–31 (Hyprland window rules, IPC socket framing, gkeep geometry, idle-lock chain, Chinese/Japanese wiki translations).
- **Result**: Exactly **ZERO** staged entries touch MIME magic, content sniffing, `mime.cache`, or `xdgmime`. There is no pending assimilation on this topic.

---

## 4. Knowledge Entry Linking Sentences

The new entry `corpus/knowledge/mime-sniff-r95.md` (or `mime-magic-sniff-r95.md`) must be linked from three existing lane knowledge notes with these exact sentences:

1. **`corpus/knowledge/mime-glob-guess-r94.md`** (in §1 "Question and scope", updating "Out of scope", line 27):
   > "Content sniffing (`data != NULL`, which can override or break a tie, S518:620-690) is resolved in `corpus/knowledge/mime-sniff-r95.md`, which models GLib 2.90.1's `g_content_type_guess (name, data, len, &uncertain)` reading the MAGIC section of `mime.cache`."

2. **`corpus/knowledge/mime-default-resolution-r91.md`** (in §1 "The plane", updating line 29):
   > "How a file's name and initial bytes resolve to that MIME type is established upstream in `corpus/knowledge/mime-glob-guess-r94.md` (file name globs) and `corpus/knowledge/mime-sniff-r95.md` (content sniffing and magic section matching)."

3. **`corpus/knowledge/xdg-mime-default-resolution-r92.md`** (in §0 "Scope", updating line 24):
   > "MIME sniffing (`xdg-mime query filetype`, xdg-mime.in:577-591) under generic desktop sessions such as Hyprland delegates to `file(1)` via `info_generic` rather than GLib's `mime.cache` magic sniffer modeled in `corpus/knowledge/mime-sniff-r95.md`."

---

## 5. Non-Obvious Move (UFO-FSD Synthesis)

### 5.1 Evidence and Contradiction
Across the round's surfaces, three divergent content-sniffing behaviors coexist on this host:
1. **Raw in-memory sniffing** (`tools/mado-mimesniff.py` and `mimesniff-oracle-r95.c`): Evaluates `g_content_type_guess (name, data, len)` where `len` is caller-supplied. The round 95 host file test (`R95MExecHostC1`) reads only the first 4096 bytes (`sniffed (first 4096 bytes) data-only`).
2. **GIO local file info** (`gio info`, `walker`, GTK apps): `gio/glocalfileinfo.c:1345-1353` reads `sniff_length = _g_unix_content_type_get_sniff_len()`, which inspects `max_extent` at byte offset 28 of `mime.cache` (`18730` on this host) and clamps to `sizeof(sniff_buffer) = 16384` (16 KiB). Rules requiring offsets between 4096 and 16384 fire under GIO, but will not fire under a 4096-byte caller probe.
3. **Hyprland `xdg-open` / `xdg-mime`**: Falls through to `file(1)` (libmagic), completely ignoring `mime.cache` and producing diverging verdicts on formats where shared-mime-info and libmagic differ.

### 5.2 Affected Axes
- **`depth`**: Enriches technical precision by bridging the abstract `g_content_type_guess` library model to the concrete GIO file-sniffing substrate.
- **`calibration`**: Distinguishes raw byte-buffer matching limits (4096 B in counter host tests) from GIO's 16 KiB ceiling and `xdg-open`'s `file(1)` delegation.
- **Harms no axis**: Does not alter PRED-C1-r95-v1 or PRED-C2-r95-v1.

### 5.3 Proposed Move
1. **In `tools/mado-mimesniff.py` Python API**: Add `Sniffer.max_buffer_extents(self) -> int` reading byte offset 28 of the loaded `mime.cache` instances (mirroring `xdgmimecache.c:727-750`), exposing GIO's native sniff ceiling.
2. **In CLI**: Keep default behavior identical, but document that `--sniff-limit 16384` matches GIO's `g_file_query_info` `sniff_buffer` clamp (`glocalfileinfo.c:1353`).
3. **In `corpus/knowledge/mime-magic-sniff-r95.md`**: Add an explicit decision subsection "Substrate Sniffing Windows", formalizing the 3-way divergence on Hyprland:
   - GIO `standard::content-type`: `min(max_extent, 16384)` bytes.
   - Raw `g_content_type_guess`: arbitrary buffer.
   - `xdg-open`: `file(1)` (libmagic).

### 5.4 Risks
- Modifying the frozen candidate `tools/mado-mimesniff.py` during wave w1 would invalidate hash pins. **Mitigation**: The move is bounded as an integration recommendation for L1 `MadoR95` and `R95MScribeEntry`; no code edits are made by `R95MConnector`.

### 5.5 Verification
1. `python3 -c "import struct; b=open('/usr/share/mime/mime.cache','rb').read(); off=struct.unpack('>I',b[24:28])[0]; print(struct.unpack('>II',b[off:off+8]))"` prints `(689, 18730)`.
2. `gio info /etc/os-release` confirms `standard::content-type: text/plain` (sniffed) vs `standard::fast-content-type: application/octet-stream` (unsniffed).
3. `xdg-mime query filetype /etc/os-release` matches `file --brief --dereference --mime-type /etc/os-release` (`text/plain`).

---

## 6. Execution and Host Guard Verification

- Cleaned scratch: `/fast/scratch/hyaku/mado-r95/R95MConnector` created and will be removed before exit.
- No pacman mutations executed.
- No git mutations executed in lane or fleet.
- CWD maintained at `/home/vgpnk/Projects/shokunin`.
