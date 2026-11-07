# R95MProbeC1 — falsification probe: "the candidate equals GLib for every input a desktop program would pass"

Round 95, wave w1, seat R95MProbeC1. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Everything below is **DRAFT probe evidence** (not a measurement; no counter was run, nothing was written under
`receipts/`). Scratch: `/fast/scratch/hyaku/mado-r95/R95MProbeC1` (deleted after this report was written).

Inputs under test (read-only):

- candidate `tools/mado-mimesniff.py` = copy of `.ufo/waves/round-95/build/mado-mimesniff.c1.py`
  sha256 `a13b6e0e3b0c399892ff027309f942daa96e92713851e8d8cfb736b277cde99d`, next to a copy of round-94's
  `tools/mado-mimeglob.py` sha256 `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`;
- oracle `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` sha256
  `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a`, compiled in scratch with
  `cc -O0 ... $(pkg-config --cflags --libs gio-2.0)` (exit 0);
- host: glib2 `2.90.1-1`, shared-mime-info `2.5.1-2`, python `3.14.8-1`; shell env `HOME=/home/vgpnk`,
  `XDG_DATA_HOME=/home/vgpnk/.local/share`, `XDG_DATA_DIRS=/usr/local/share:/usr/share`
  (`/usr/local/share/mime` does not exist, so it contributes nothing).
- Oracle/cmd used for every label: `env -i LC_ALL=C HOME=<h> [XDG_DATA_HOME=<d>] XDG_DATA_DIRS=<list> <oracle>`.
  The tool was driven in-process through `Sniffer(mg.xdgmime_dirs(XDG_DATA_HOME, HOME, XDG_DATA_DIRS))`, i.e. the same
  dir list the CLI computes; CLI spot checks were also run (see "Reproducer" below).

Verdict: **the hypothesis is false**. Finding F1 is a data-driven divergence that needs no malformed fixture and
reproduces against the real host database; F2 and F3 are divergences on malformed `mime.cache` content (environment,
not data) that the frozen `wrap`/`bounds` classes can generate.

---

## F1 (HIGH) — `looks_like_text` admits U+000B; GLib does not

Candidate: `.ufo/waves/round-95/build/mado-mimesniff.c1.py:207-208`

```python
def looks_like_text(data: bytes) -> bool:
    return not any(b < 8 or 14 <= b < 32 or b == 127 for b in data)
```

This allows bytes 8..13, i.e. it treats VT (`0x0B`) as whitespace. GLib does not:
`fetch/gcontenttype-fdo.c:533-548` rejects a byte when
`g_ascii_iscntrl(c) && !g_ascii_isspace(c) && c != '\b'`, and the installed GLib's ASCII table has
`g_ascii_isspace(0x0B) == 0` while `g_ascii_isspace(0x0C) == 1`, `g_ascii_iscntrl(0x0B) == 1`
(`g_ascii_isspace` is the `G_ASCII_SPACE` table lookup, `/usr/include/glib-2.0/glib/gstrfuncs.h:85-86`; the table was
probed directly with a compiled `glib-2.0` test). So `0x0B` is a control character for GLib and `0x0C` (FF) is not.
The candidate also gets FF and BS right; **only `0x0B` differs**, in every data shape probed (see (g)).

Why it matters: a byte `0x0B` in the first 128 bytes of the data makes GLib's fallback return
`application/octet-stream` with `uncertain = TRUE` (or, with 2+ name types, the first name type with
`uncertain = TRUE`), while the candidate answers `text/plain` / the subclass-matched name type with `uncertain = 0`
(and can pick a different type when a name type derives from `text/plain`).

Evidence (DRAFT):

- `g-vt-minimal` (case): input 0 `data="a\x0b\n", name=NULL` — oracle `application/octet-stream\t1`,
  tool `text/plain` `uncertain=0`; input 1 `data="\x0b"` — same; input 2 `name=x.two, data="a\x0b z\x08"` —
  oracle `text/x-a\t1`, tool `text/x-a\t0`; inputs 3 `"\x08\x0b"`, 4 `" \x0b Z\r\tb\x80"`, 8 `"ab\x0bcd"` —
  oracle `application/octet-stream\t1`, tool `text/plain\t0`. Controls with `0x0C`/`0x08` agree.
- `g-byte-sweep` (case): 1026 inputs = 256 bytes x 4 shapes (`[b]`, `"\x08"+[b]`, `"\x0c"+[b]`, `"a"+[b]+"z"`)
  + 2 two-name-type inputs. Exactly 5 mismatches, all byte `0x0B` (decimal 11); all other 255 byte values agree.
- Real host database (no fixture): `env -i LC_ALL=C HOME=<empty> XDG_DATA_DIRS=/usr/share oracle 0 <"a\x0b\n">`
  prints `application/octet-stream\t1`; the tool with `--data-dirs /usr/share` prints `type=text/plain`,
  `uncertain=0`. With `name=x.ts` the oracle prints `text/vnd.trolltech.linguist\t1`, the tool prints the same type
  with `uncertain=0`.
- Random differential fuzz (f): 260 synthetic caches x ~10 inputs = 2480 inputs, 38 mismatches — every one contains
  `0x0B` at index < 128, and no other cause was observed.

The tool's selftest cannot catch this: `selftest` check `s10` at `.ufo/waves/round-95/build/mado-mimesniff.c1.py:467`
asserts `g(a, None, b"ab\x0bcd") == ("text/plain", 0)` — it encodes the wrong rule. `--selftest` prints
`MADO_MIMESNIFF_SELFTEST: checks=23 failed=0` (exit 0).

Minimal fix: reject `0x0B` in `looks_like_text` (e.g. `b < 8 or b == 11 or 14 <= b < 32 or b == 127`) and change
`s10` to expect `("application/octet-stream", 1)`. (Note: the `0x0B`-binary decision in `_xdg_binary_or_text_fallback`
is already correct; only the second-stage `looks_like_text` filter is wrong.)

Reproducer (CLI, in scratch; both commands were run):

```
env -i LC_ALL=C HOME=$R/h XDG_DATA_DIRS=$R/s1:$R/s2 $S/oracle 0 $R/d_vt
# application/octet-stream	1   (rc 0)
python3 -I $S/tools/mado-mimesniff.py --json --data-home-unset --data-dirs "$R/s1:$R/s2" --home "$R/h" "$R/d_vt"
# {"results":[{"type":"text/plain","uncertain":0,"sniffed":"text/plain",...}]}   (rc 0)
```

with `$R/s1/mime/mime.cache` = `build_cache(globs=[("*.two","text/x-a",50),("*.two","app/x-b",50)], magic=[(90,"app/never",[{"start":0,"length":1,"value":b"\xde\xad"}])])`
and `$R/d_vt` = `a\x0b\n`.

---

## F2 (MEDIUM) — wrapped matchlet: the tool refuses where GLib's defined unsigned wrap returns "no match"

Candidate: `.ufo/waves/round-95/build/mado-mimesniff.c1.py:112-113`

```python
if i + value_length > M32:
    raise Unsupported("matchlet i + value_length passes 2^32 (memcmp past the data)")
```

GLib (`fetch/xdgmimecache.c:167-210`) computes `i + data_length` in `xdg_uint32_t`, so the addition wraps; when the
wrapped value is `> len`, `cache_magic_matchlet_compare_to_data` returns `FALSE` **without any memory access**. The
candidate refuses before applying the wrap and the `len` check.

Reproducer (case `j-wrap-answer`, class `wrap`): cache = `build_cache(magic=[(90,"app/wrap",
[{"start":0xFFFFFFF0,"length":8,"value":b"V"*20,"mask":None,"children":[]}])])`, data `b"xyz"` (3 bytes), name NULL.

- oracle: `text/plain\t0` (all eight loop iterations wrap to 4..11 > 3 → FALSE; fallback says text);
- tool: `MADO_MIMESNIFF: UNSUPPORTED matchlet i + value_length passes 2^32 (memcmp past the data)`, exit 3.

Control `j-wrap-crash` (same cache, data `b"xyzz"`, 4 bytes): the wrapped first sum is 4 <= 4, C proceeds to
`memcmp(cache->buffer + data_offset, data + 0xFFFFFFF0, 20)` and the oracle dies (`rc 139`, SIGSEGV) → label
`["UNSUPPORTED", null]`; the tool exits 3, which is correct there.

Minimal fix: mirror the wrap before deciding to refuse —
`wrapped = (i + value_length) & M32; if wrapped > len(data): return False; raise Unsupported(...)`.

---

## F3 (LOW/MEDIUM) — eager mime-string decode for matches GLib never dereferences

Candidate: `.ufo/waves/round-95/build/mado-mimesniff.c1.py:187` — `cache_magic_lookup` returns
`c.cstr(mo).decode(...), _s32(prio)` as soon as a matchlet matches. GLib's `cache_magic_compare_to_data`
(`fetch/xdgmimecache.c:241-274`) only stores `cache->buffer + mimetype_offset` and `*prio`; the pointer is
dereferenced later only if `prio > priority` (and `priority > 0`). With an entry whose priority is `0`, `0x80000000`,
or `0xFFFFFFFF`, GLib discards the pointer without reading it; the candidate reads (and refuses on) the string.

Reproducer (case `j-prio0-refuse`, class `bounds`): cache = `build_cache(magic=[(0,"app/zero",
[{"start":0,"length":2,"value":b"HI"}])])` with the entry's mime offset patched to `0xFFFFFFF0`, data `b"HI rest"`,
name NULL.

- oracle: `text/plain\t0` (match at prio 0 is discarded; no dereference; fallback text);
- tool: `MADO_MIMESNIFF: UNSUPPORTED cache string runs past the mapping`, exit 3.

Control `j-prio0-control` (`data="plain\n"`, matchlet does not match): both print `text/plain\t0`.
`j-wrap-*` and `j-prio0-*` labels were re-derived with the oracle at case-validation time (see validation below).

Caveat for the L1: forming `cache->buffer + 0xFFFFFFF0` is pointer arithmetic outside the object (ISO C UB), but no
byte is accessed and the oracle's answer is deterministic. If the L1 reads the declaration's named limit
"C undefined behaviour refused" as covering *formation* as well as access, F3 can be dropped; F2 cannot, because the
wrapped comparison is fully defined C.

Minimal fix: return `(mo, prio)` from `cache_magic_lookup` and decode the string only when `p > priority` and
`p > 0` at the call site (mirrors the C pointer life time).

---

## Probe results (counts)

All counts below are DRAFT probe runs; a row of `N` inputs means the oracle's own label for each input, compared with
the in-process candidate. `diffs` = records where `(type, uncertain)` or the refusal differs.

### (a) real user cache + system cache together — PASS

- `~/.local/share/mime/mime.cache` (read-only, 288 bytes, header 1.2): **magic section has 0 entries** →
  **types added by the user cache's magic: none** (`types_added_by_user_magic = []`). Its other sections are
  alias n=0, parent n=0, literal n=1, suffix n=1, glob n=0; the suffix entry is the `*.uproject` →
  `application/uproject` glob (a *name* effect, not magic).
- Combined run: 40 files under `/usr/share` × 4 name variants (`NULL`, own path, `x.uproject`, `file.ts`) = 160 pairs,
  oracle with the user cache copied at `$HOME/.local/share/mime/mime.cache` plus `/usr/share/mime/mime.cache`:
  **0 diffs**. User-cache effect vs system-only: 40/160 answers change (every `x.uproject` input answers
  `application/uproject\t0`), and the tool matches both configurations.
- Case `a-combined-user-system` (class `multicache`): 160 inputs, 0 mismatches (stores both cache files).

### (b) truncated real files, lengths 0..min(4096,size) — PASS

12 files (ELF `/usr/bin/ls`, PNG, gzip man page, TTF, WAV, `.desktop`, SVG, `.mo`, text `globs2`, OGG, ZIP,
JAR): **38,432 inputs, 0 diffs**; every length was compared, so the tool's flip points equal GLib's exactly.
Flip counts per file (N flips, boundaries included in the case): ls 3, png 3, gz 2, ttf 2, wav 3, desktop 2, svg 2,
mo 3, globs2 1, ogg 3, zip 3, jar 3. Examples: ELF `text/plain` at L=1..5, `octet-stream 1` at L=5, `x-executable`
at L=6; PNG `text/plain` → (L=7) `octet-stream 1` → (L=8) `image/png`; WAV `text/plain` → (L=4) `x-riff` →
(L=12) `audio/vnd.wave`.
Case `b-truncation-flips` (class `bounds`): 66 flip-neighbourhood inputs, 0 mismatches.

### (c) names with several types in `globs2` + real data — PASS

`/usr/share/mime/globs2` (1613 entries, 1374 globs) has 108 globs mapping to >1 type. 108 concrete names
(e.g. `x.ts` = text/vnd.trolltech.linguist + video/mp2t + application/typescript; `x.ogg` = 6 types;
`x.der` = 10 types; `x.m` = text/x-objcsrc + text/x-matlab; `x.asc` = 4; `x.key` = 3; `x.doc`, `x.exe`) × 9 data
samples (empty, text, binary, PNG, ELF, gzip, SVG, WAV, MO) = **972 pairs, 0 diffs**.
Case `c-name-conflicts` (class `order`): 972 inputs, 0 mismatches.

### (d) cache version 1.1 vs 1.2, invalid headers mixed with valid caches — PASS on all mixed cases

8 cases x 10 pairs = **80 pairs, 0 diffs**: `mime.cache` minor 1 and minor 2 (identical answers; GLib accepts
`MINOR_VERSION_MIN=1 .. MINOR_VERSION_MAX=2` and the stored `minor` is never consulted — `fetch/xdgmimecache.c:134-147`);
invalid major 2 / minor 0 / minor 3 / 39-byte file / corrupt magic-list offset / all-section-offsets-OOB, each placed
*beside* a valid cache (user dir and system dir variants): the invalid cache is skipped and the valid one decides in
both implementations.
Boundary (not a case, declared limit): an invalid `mime.cache` **alone** (no other cache, no `globs2`/`globs`) →
the tool refuses with exit 3 (text mode) while GLib answers from its text-mode fallback; this is the declaration's
"cache mode only" limit, not a falsifier.
Also observed (not a case; empty-type corner): a valid cache whose magic mime offset points into the zero-filled tail
of the mapping returns `""` from GLib; the tool matches (`OBS-bad-string`, 10/10).

### (e) priority >= 2^31 and parent cycles, built with the tool's `build_cache` — PASS

- priorities `0x80000000`, `0x80000001`, `0xFFFFFFFF` are negative ints for GLib and are discarded (`prio > 0` guard);
  `0x7FFFFFFF` wins; `0` is ignored; 20 pairs, 0 diffs. Two-cache case (negative in user dir, 60 in system dir):
  20 pairs, 0 diffs.
- parent cycles `A<->C`, `A->C->A`, `A->C->B->A` (cycle escaped to reach a real ancestor), self-loop `S->S`,
  `D<->E`, and a cross-cache cycle `M->N` (cache 1) / `N->M` (cache 2): 36 pairs, 0 diffs; no hang (timeout 20 s).
Cases `e-prio-hi`, `e-prio-crosscache`, `e-cycle-parents`, `e-cycle-crosscache`.

### (f) supplementary: randomised differential fuzz of `build_cache` fixtures — 38 diffs, all F1

260 caches (1-2 per iteration), random priorities from a pool including the 2^31 edges, random matchlets with
ranges/masks/children, random aliases/parents/globs, random names and data: **2480 inputs, 38 diffs**, every one
contains `0x0B` at index < 128 and is explained by F1 (6 of the 38 also show a type difference and not just the
uncertain bit).

### (g) supplementary: exhaustive byte sweep of the text/binary classification — only 0x0B differs

1026 inputs as described above: **exactly 5 diffs, distinct bytes {11}**: `[0x0B]`, `"\x08\x0B"`, `"\x0C\x0B"`,
`"a\x0Bz"`, and one two-name-type input (`name=x.two, data="a\x0b z\x08"` → type equal, uncertain 1 vs 0).
Cases `g-byte-sweep` (1026 inputs, 5 mismatches) and `g-vt-minimal` (9 inputs, 6 mismatches).

### (h) supplementary: name cap (>10 glob matches), `inode/` special case, case-sensitive glob bit — PASS

Cache with 15 globs matching `x.many`, a literal `lit` pair, `*.caps` with the `0x100` (case-sensitive) weight bit,
and magic types `application/octet-stream` / `application/x-desktop`: 25 pairs, **0 diffs** (the 10-type cap, order,
and the case-sensitivity flag all match).

### (i) supplementary: corruption fuzz of cache bytes — classification only

3 seeds x 90 corrupted caches x 10 inputs = 2700 inputs, 426 diffs: 352 involve `0x0B` (F1); 57 are per-input
refusals on loadable-but-corrupted caches; 17 are text-mode refusals on caches whose header was corrupted (declared
limit). The 57 break down into (i) F2 (defined unsigned wrap, no access), (ii) F3 (pointer formed, never read), and
(iii) reads *past the mapping* that C performs and survives only by landing in another mapping (wild-pointer UB —
**not** used as evidence: those labels are ASLR-dependent). One example of (iii): a matchlet with a corrupt value
offset `0x5d70` in a 388-byte cache makes GLib `memcmp` a wild address and print `text/plain` on this run; the same
cache can crash on another layout. No case in the case file relies on such a label.

---

## Case file (falsifiers), validated

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/w1/R95MProbeC1-cases.json`
sha256 `9c5198a909f73ce97928a199a42223eb9f2d2b4f5d6955d7246149f6b06068d1`, 2,880,685 bytes,
22 cases, 2418 inputs, classes `{mode 5, multicache 4, bounds 3, lltext 2, prio 2, subclass 2, wrap 2, nameN 1,
order 1}`, every `env` has `HOME={root}/h` and a non-null `XDG_DATA_DIRS`, every file is base64 in `files`.

Validation method: each case was materialised from the JSON, labelled afresh with the oracle in the case's exact
`env`, and then run through the candidate. **Fresh-label mismatches: 0/2418** (so every recorded label is the oracle's
own answer). Candidate mismatches (the falsifiers): 13/2418 —
`g-vt-minimal` 6/9, `g-byte-sweep` 5/1026, `j-wrap-answer` 1/1, `j-prio0-refuse` 1/1. The other 18 cases pass fully.

If the L1 merges this file into the frozen cases as-is, the current candidate will fail C1 on the four cases above;
the F1 fix (plus F2, and F3 if not covered by the named UB limit) is required first.

---

## Residual risk / verification gaps

- Not probed (time-boxed, by design): the text-mode (`globs2`/`globs`/`magic` files) path — declared out of scope;
  deep parent chains (no 1000+ chains); caches > 2^32 bytes; data lengths > 4096 (only through the 4096-byte
  truncations); filenames with non-UTF-8 basenames beyond the raw-byte glob path; locale other than C.
- The in-process driver computes the directory list exactly like the CLI; only a sample of cases was additionally
  exercised through the CLI (`g-vt-minimal` input 0 and the `j-*` cases were; the CLI exits 3 for any refused
  input, which is why those cases carry a single input each).
- Labels for the corruption-fuzz wild-pointer cases are ASLR-dependent and were deliberately excluded from the case
  file; the frozen counter must not build cases from `i2.py` candidates without checking that the oracle's read
  stays inside the mapping.
- The cases file is 2.9 MB (mostly the 207,520-byte `/usr/share/mime/mime.cache` copy in three cases and the 972
  name/data pairs); the L1 may trim inputs when merging without changing any label.

## Commands run (DRAFT; exit codes)

| command | exit |
|---|---|
| `cc -O0 -o "$S/oracle" .../mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)` | 0 |
| `python3 -I "$S/tools/mado-mimesniff.py" --selftest` | 0 (`checks=23 failed=0`) |
| `python3 a.py` (160 pairs) | 0, 0 diffs |
| `python3 b.py` (38,432 inputs) | 0, 0 diffs |
| `python3 c.py` (972 pairs) | 0, 0 diffs |
| `python3 d.py` (80 pairs + boundaries) | 0, 0 diffs on 8 cases; all-invalid boundary 10/10 refusals |
| `python3 e.py` (76 pairs) | 0, 0 diffs |
| `python3 f.py` (2,480 inputs) | 0, 38 diffs (all F1) |
| `python3 g.py` (1,026 inputs) | 0, 5 diffs (all byte 0x0B) |
| `python3 h2.py` (25 pairs) | 0, 0 diffs |
| `python3 i2.py 9502/9503/9504` (2,700 inputs) | 0, 426 diffs (classification above) |
| `python3 j.py` | 0: `j-wrap-answer` oracle text/plain 0 vs tool exit 3; `j-prio0-refuse` same |
| `python3 final.py` (assemble + validate) | 0, label mismatch 0/2418, tool mismatch 13/2418 |
| CLI repro `env -i ... oracle 0 d_vt` / `python3 -I ... mado-mimesniff.py --json ... d_vt` | 0/0, answers as in F1 |
| CLI repro wrap/prio0 (4 cases) | oracle 0/139/0/0; tool 3/3/3/0 as in F2/F3 |

Harness defects hit and fixed during the run (not tool defects): a `makedirs` FileExistsError in the first `a.py`
draft (fixed with `exist_ok=True`), an `sn=None` AttributeError in `d.py` for refusal cases (fixed), and a
relative-path oracle invocation that made the oracle exit 2 (recorded as UNSUPPORTED until the path was made
absolute — the F1 evidence above was re-run absolutely and via the CLI).

## Installs

None (no tool was installed or upgraded; pacman was not used).

## Files written

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/w1/R95MProbeC1-cases.json` (falsifiers, validated)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-95/w1/R95MProbeC1.md` (this report)

Scratch `/fast/scratch/hyaku/mado-r95/R95MProbeC1` was deleted after the cases file was written and re-validated;
nothing cited here lives only in scratch.
