# R94MProbeC1 — C1 cache-vs-text probe: does GLib answer the same with and without mime.cache?

DRAFT seat report. Every run below is a **DRAFT** run (pre-freeze); nothing here is a measurement.

| item | value |
|---|---|
| seat | R94MProbeC1 (leaf; no spawn) |
| lane base | `a3de997289014e7dbf1d73ae206be1d6f8cdadd0` (master) |
| candidate | `.ufo/waves/round-94/build/mado-mimeglob.c1.py`, sha256 `0700915a260627cd521ea14b61dbb15aa7c3b067c0d287f04c07b39dfa72d63e` (pin matches) |
| oracle source | `.ufo/waves/round-94/controls/mimeglob-oracle-r94.c`, sha256 `9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11`; compiled binary sha256 `38cea1b00dd65bb2531921aeaf7f586f3524a62fa6823b4f2c49c910724239e2` |
| host | glib2 2.90.1-1, shared-mime-info 2.5.1-2, gcc 16.2.1, python 3.14.8, Linux 7.2.11-arch1-1 x64 |
| scratch | `/fast/scratch/hyaku/mado-r94/R94MProbeC1` (TMPDIR set explicitly; deleted on exit) |
| report | `.ufo/waves/round-94/w1/R94MProbeC1.md` |

Fetched sources (each `curl` HTTP 200; digests equal the L1 receipts): `xdgmimeglob.c`
`38ed8623…0734`, `xdgmimecache.c` `ccda4366…db69`, `xdgmime.c` `afb1c1c1…2410`,
`xdgmimeint.c` `c2364aa8…2f29`, `gcontenttype-fdo.c` `8a5b4f47…2d7c`.

## Method (DRAFT)

- 56 package-XML layouts in scratch, each generated from `packages/*.xml` with
  `update-mime-database <dir>/mime` (2.5.1). Each dir's `mime.cache` + `globs2` were produced by
  that command; 3 layouts were then post-edited to probe the mode boundary (`L43` cache deleted,
  `L44` cache version bytes 1.0, `L45` cache truncated to 20 B) and are reported separately.
- 9521 (name, mode) oracle comparisons over 364 distinct names; the oracle was run
  as a fresh process per mode with `env -i LC_ALL=C HOME=<root>/h [XDG_DATA_HOME=…] XDG_DATA_DIRS=…`.
  Cache mode = before moving any `mime.cache`; text mode = after moving every `mime.cache` out of
  the searched dirs (the hypothesis's "same dir with mime.cache removed").
- Candidate checked per layout in both modes with `python3 -I <tool> --json --home … --data-home …
  --data-dirs …`.
- Case-file labels are oracle answers recorded by re-materialising the case JSON alone (files
  decoded, no other files present) and re-running the oracle; the candidate was run on the same
  roots.

## Verdict

**Hypothesis FALSIFIED.** Cache mode and text mode disagree on 117 of 9521
filename-only answers (26 of 56 layouts). Restricted to the
53 layouts exactly as `update-mime-database` produced them (no post-edit): 102 of
9002 answers, 23 layouts. Nine independent mechanisms were isolated; every
mechanism has a minimal cache/text case pair below, and the candidate follows the oracle on all
of those pair cases in both modes. The hypothesis does hold on the other
30 layouts (listed under Controls).

Divergent layouts (DRAFT sweep):

| layout | mechanism | divergent answers | names tested |
|---|---|---|---|
| L08-full-simple-lowfull | F1 full-glob fold | 2 | 174 |
| L09-full-simple-highsimple | F1 full-glob fold | 2 | 174 |
| L10-full-casefold | F1 full-glob fold | 6 | 171 |
| L11-full-question | F1 full-glob fold | 3 | 169 |
| L14-full-two-fold | F1 full-glob fold | 8 | 176 |
| L16-literal-cs-vs-noncs | F2 literal order | 1 | 165 |
| L25-colon-simple | F3 colon | 7 | 170 |
| L26-colon-literal | F3 colon | 3 | 168 |
| L27-longline-pattern | F4 fgets | 5 | 171 |
| L28-longline-literal | F4 fgets | 3 | 169 |
| L31-weight-101 | F5 weight | 5 | 169 |
| L32-weight-200 | F5 weight | 5 | 169 |
| L35-weight-254 | F5 weight | 5 | 169 |
| L36-weight-neg | F5 weight | 5 | 169 |
| L39-dirs-weight-merge | F6 dirs merge | 6 | 169 |
| L40-dirs-deepest | F7 per-cache deep | 9 | 173 |
| L42-dirs-literal | F2 literal order | 1 | 165 |
| L43-mixed-globs-only | F8 mode dispatch | 5 | 173 |
| L44-bad-cache | F8 mode dispatch | 5 | 173 |
| L45-short-cache | F8 mode dispatch | 5 | 173 |
| L46-full-tie | F1 full-glob fold | 5 | 175 |
| L48-literal-vs-full | F1 full-glob fold | 4 | 171 |
| L53-cs-literal-abort | F9 cs literal abort | 3 | 165 |
| L54-longline-shortmt | F4 fgets | 7 | 172 |
| L55-cs-literal-same-dir | F9 cs literal abort | 3 | 165 |
| L56-weight-300 | F5 weight | 4 | 169 |

## Divergence mechanics, source anchors, and minimal pairs

Source line numbers are the fetched 2.90.1 files (receipt digests). One source subtlety worth
recording for the C1 model: the text full-glob guard is `if (n < 2)` (xdgmimeglob.c:469), but the
second simple-glob pass re-finds a plain suffix match on the original name, so a lowercase-name
suffix match counts twice (n=2) and the full list is skipped, as in cache mode (`if (n == 0)`,
xdgmimecache.c:706). I probed the n=1 corner: text reaches it only for a folded-only suffix match
(uppercase name) or a cs-only match. In the folded-only case the text full-list fnmatch runs on
the original uppercase name, which cannot match a generator-lowercased non-cs pattern, and the
cache runs its original-name fnmatch pass anyway (`if (n < 2)`, :708); a case-sensitive full
pattern with capitals is matched by both. Tested: `*.c` w50 + cs `*.[CH]` w70, `FOO.C` ->
`application/x-b` in both modes; hand-written `foo*` w70 + `*.c` w50, `foo.c` -> the `*.c` type in
both. No extra class.

### F1. Non-case-sensitive full globs are folded against the name only in cache mode

`update-mime-database` lowercases non-cs glob patterns in `globs2` (observed: `*.[CH]` -> `*.[ch]`, `*.JPG` -> `*.jpg`, `MakeFile` -> `makefile`). Text mode matches full globs with `fnmatch(pattern, file_name, 0)` on the **original** name and ignores the cs flag (xdgmimeglob.c:469-480). Cache mode first runs the fnmatch list against the **ASCII-lowercased** name for non-cs entries, then against the original name (xdgmimecache.c:706-709). An uppercase name whose lowercase form matches a non-cs full glob therefore answers in cache mode and does not in text mode. 7 layouts, 30 answers.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"full-01-cache","class":"fold","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDp0ZXh0L3gtY2g6Ki5bY2hdCg==","dh/mime/mime.cache":"AAEAAgAAAEAAAABEAAAASAAAAEwAAABUAAAAZAAAAHAAAAB0AAAAeAAAAHwqLltjaF0AAHRleHQveC1jaAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUAAAAAQAAACwAAAA0AAAAPAAAAAAAAAAAAAAAcAAAAAAAAAAAAAAAAAAAAAEAAAAA"},"names_b64":["Zm9vLkM="],"labels":[["text/x-ch",0]]}
{"id":"full-01-text","class":"fold","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDp0ZXh0L3gtY2g6Ki5bY2hdCg=="},"names_b64":["Zm9vLkM="],"labels":[["application/octet-stream",1]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F2. Literal lookup order: text exact-first, cache folded-first

Text checks an exact literal match first (all literals, cs or not) and only then folded non-cs literals (xdgmimeglob.c:442-467). Cache checks the folded literal table first, then the exact table (xdgmimecache.c:686-694). With a lowercase non-cs literal for type a and a capital case-sensitive literal of the same lowercase form for type b, `Makefile` answers b in text and a in cache. 2 layouts, 2 answers (`L16`, `L42` across two dirs).

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"literal-01-cache","class":"order","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWI6TWFrZWZpbGU6Y3MKNjA6YXBwbGljYXRpb24veC1iOk1ha2VmaWxlCjUwOmFwcGxpY2F0aW9uL3gtYTptYWtlZmlsZQo=","dh/mime/mime.cache":"AAEAAgAAAGQAAABoAAAAbAAAAIgAAACQAAAAlAAAAKAAAACkAAAAqAAAAKxhcHBsaWNhdGlvbi94LWIATWFrZWZpbGUAAAAAYXBwbGljYXRpb24veC1hAG1ha2VmaWxlAAAAAAAAAAAAAAAAAAAAAgAAADwAAAAsAAABPAAAAFgAAABIAAAAMgAAAAAAAACQAAAAAAAAAAAAAAAAAAAAoAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAA=="},"names_b64":["TWFrZWZpbGU="],"labels":[["application/x-a",0]]}
{"id":"literal-01-text","class":"order","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWI6TWFrZWZpbGU6Y3MKNjA6YXBwbGljYXRpb24veC1iOk1ha2VmaWxlCjUwOmFwcGxpY2F0aW9uL3gtYTptYWtlZmlsZQo="},"names_b64":["TWFrZWZpbGU="],"labels":[["application/x-b",0]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F3. A colon in a glob pattern is consumed by the globs2 field separator in text mode

`globs2` is `weight:mime:glob[:flags]`; the text reader splits at the first three colons and treats the remainder as flags (xdgmimeglob.c:656-700), so the pattern is truncated at the next colon. The binary cache is built from the in-memory pattern and keeps it whole. A pattern `*.x:y` matches `a.x:y` in cache and `a.x` in text; literal `pre:post` matches `pre:post` in cache and `pre` in text. 2 layouts, 10 answers.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"colon-01-cache","class":"simple","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWNvOioueDp5Cg==","dh/mime/mime.cache":"AAEAAgAAAEAAAABEAAAASAAAAEwAAACQAAAAlAAAAKAAAACkAAAAqAAAAKxhcHBsaWNhdGlvbi94LWNvAAAAAAAAAAAAAAAAAAAAAAAAAAEAAABUAAAAeQAAAAEAAABgAAAAOgAAAAEAAABsAAAAeAAAAAEAAAB4AAAALgAAAAEAAACEAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAoAAAAAAAAAAAAAAAAAAAAAEAAAAA"},"names_b64":["YS54Onk=","YS54"],"labels":[["application/x-co",0],["application/octet-stream",1]]}
{"id":"colon-01-text","class":"simple","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWNvOioueDp5Cg=="},"names_b64":["YS54Onk=","YS54"],"labels":[["application/octet-stream",1],["application/x-co",0]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F3b. Same serialization failure for a literal containing a colon

Same mechanism as F3 on a literal pattern. 2 answers in `L26`.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"colon-02-cache","class":"literal","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWNsOnByZTpwb3N0Cg==","dh/mime/mime.cache":"AAEAAgAAAEwAAABQAAAAVAAAAGQAAABsAAAAcAAAAHwAAACAAAAAhAAAAIhwcmU6cG9zdAAAAABhcHBsaWNhdGlvbi94LWNsAAAAAAAAAAAAAAAAAAAAAQAAACwAAAA4AAAAMgAAAAAAAABsAAAAAAAAAAAAAAAAAAAAfAAAAAAAAAAAAAAAAAAAAAEAAAAA"},"names_b64":["cHJlOnBvc3Q=","cHJl"],"labels":[["application/x-cl",0],["application/octet-stream",1]]}
{"id":"colon-02-text","class":"literal","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWNsOnByZTpwb3N0Cg=="},"names_b64":["cHJlOnBvc3Q=","cHJl"],"labels":[["application/octet-stream",1],["application/x-cl",0]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F4. globs2 lines over 254 bytes are split by `fgets(line, 255, f)` in text mode

`_xdg_mime_glob_read_from_file` reads with a 255-byte buffer (xdgmimeglob.c:643, with the upstream FIXME that lines greater than 255 chars do not work); the cache has no such limit. A long pattern or literal is truncated at 254 bytes in text mode and stops matching the intended name, while the cache matches it. 3 layouts, 15 answers. `fgets-03` isolates it with a 3-byte mime type and 259/258-byte lines (no long mime-type contribution).

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"fgets-03-cache","class":"fgets","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp4L3k6Ki5jY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjCjUwOngveTpsZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZAo=","dh/mime/mime.cache":"AAEAAgAAASwAAAEwAAABNAAAAUQAAA0cAAANIAAADSwAAA0wAAANNAAADThsZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZAB4L3kAAAAAAAAAAAAAAAABAAAALAAAASgAAAAyAAAAAQAAAUwAAABjAAAAAQAAAVgAAABjAAAAAQAAAWQAAABjAAAAAQAAAXAAAABjAAAAAQAAAXwAAABjAAAAAQAAAYgAAABjAAAAAQAAAZQAAABjAAAAAQAAAaAAAABjAAAAAQAAAawAAABjAAAAAQAAAbgAAABjAAAAAQAAAcQAAABjAAAAAQAAAdAAAABjAAAAAQAAAdwAAABjAAAAAQAAAegAAABjAAAAAQAAAfQAAABjAAAAAQAAAgAAAABjAAAAAQAAAgwAAABjAAAAAQAAAhgAAABjAAAAAQAAAiQAAABjAAAAAQAAAjAAAABjAAAAAQAAAjwAAABjAAAAAQAAAkgAAABjAAAAAQAAAlQAAABjAAAAAQAAAmAAAABjAAAAAQAAAmwAAABjAAAAAQAAAngAAABjAAAAAQAAAoQAAABjAAAAAQAAApAAAABjAAAAAQAAApwAAABjAAAAAQAAAqgAAABjAAAAAQAAArQAAABjAAAAAQAAAsAAAABjAAAAAQAAAswAAABjAAAAAQAAAtgAAABjAAAAAQAAAuQAAABjAAAAAQAAAvAAAABjAAAAAQAAAvwAAABjAAAAAQAAAwgAAABjAAAAAQAAAxQAAABjAAAAAQAAAyAAAABjAAAAAQAAAywAAABjAAAAAQAAAzgAAABjAAAAAQAAA0QAAABjAAAAAQAAA1AAAABjAAAAAQAAA1wAAABjAAAAAQAAA2gAAABjAAAAAQAAA3QAAABjAAAAAQAAA4AAAABjAAAAAQAAA4wAAABjAAAAAQAAA5gAAABjAAAAAQAAA6QAAABjAAAAAQAAA7AAAABjAAAAAQAAA7wAAABjAAAAAQAAA8gAAABjAAAAAQAAA9QAAABjAAAAAQAAA+AAAABjAAAAAQAAA+wAAABjAAAAAQAAA/gAAABjAAAAAQAABAQAAABjAAAAAQAABBAAAABjAAAAAQAABBwAAABjAAAAAQAABCgAAABjAAAAAQAABDQAAABjAAAAAQAABEAAAABjAAAAAQAABEwAAABjAAAAAQAABFgAAABjAAAAAQAABGQAAABjAAAAAQAABHAAAABjAAAAAQAABHwAAABjAAAAAQAABIgAAABjAAAAAQAABJQAAABjAAAAAQAABKAAAABjAAAAAQAABKwAAABjAAAAAQAABLgAAABjAAAAAQAABMQAAABjAAAAAQAABNAAAABjAAAAAQAABNwAAABjAAAAAQAABOgAAABjAAAAAQAABPQAAABjAAAAAQAABQAAAABjAAAAAQAABQwAAABjAAAAAQAABRgAAABjAAAAAQAABSQAAABjAAAAAQAABTAAAABjAAAAAQAABTwAAABjAAAAAQAABUgAAABjAAAAAQAABVQAAABjAAAAAQAABWAAAABjAAAAAQAABWwAAABjAAAAAQAABXgAAABjAAAAAQAABYQAAABjAAAAAQAABZAAAABjAAAAAQAABZwAAABjAAAAAQAABagAAABjAAAAAQAABbQAAABjAAAAAQAABcAAAABjAAAAAQAABcwAAABjAAAAAQAABdgAAABjAAAAAQAABeQAAABjAAAAAQAABfAAAABjAAAAAQAABfwAAABjAAAAAQAABggAAABjAAAAAQAABhQAAABjAAAAAQAABiAAAABjAAAAAQAABiwAAABjAAAAAQAABjgAAABjAAAAAQAABkQAAABjAAAAAQAABlAAAABjAAAAAQAABlwAAABjAAAAAQAABmgAAABjAAAAAQAABnQAAABjAAAAAQAABoAAAABjAAAAAQAABowAAABjAAAAAQAABpgAAABjAAAAAQAABqQAAABjAAAAAQAABrAAAABjAAAAAQAABrwAAABjAAAAAQAABsgAAABjAAAAAQAABtQAAABjAAAAAQAABuAAAABjAAAAAQAABuwAAABjAAAAAQAABvgAAABjAAAAAQAABwQAAABjAAAAAQAABxAAAABjAAAAAQAABxwAAABjAAAAAQAABygAAABjAAAAAQAABzQAAABjAAAAAQAAB0AAAABjAAAAAQAAB0wAAABjAAAAAQAAB1gAAABjAAAAAQAAB2QAAABjAAAAAQAAB3AAAABjAAAAAQAAB3wAAABjAAAAAQAAB4gAAABjAAAAAQAAB5QAAABjAAAAAQAAB6AAAABjAAAAAQAAB6wAAABjAAAAAQAAB7gAAABjAAAAAQAAB8QAAABjAAAAAQAAB9AAAABjAAAAAQAAB9wAAABjAAAAAQAAB+gAAABjAAAAAQAAB/QAAABjAAAAAQAACAAAAABjAAAAAQAACAwAAABjAAAAAQAACBgAAABjAAAAAQAACCQAAABjAAAAAQAACDAAAABjAAAAAQAACDwAAABjAAAAAQAACEgAAABjAAAAAQAACFQAAABjAAAAAQAACGAAAABjAAAAAQAACGwAAABjAAAAAQAACHgAAABjAAAAAQAACIQAAABjAAAAAQAACJAAAABjAAAAAQAACJwAAABjAAAAAQAACKgAAABjAAAAAQAACLQAAABjAAAAAQAACMAAAABjAAAAAQAACMwAAABjAAAAAQAACNgAAABjAAAAAQAACOQAAABjAAAAAQAACPAAAABjAAAAAQAACPwAAABjAAAAAQAACQgAAABjAAAAAQAACRQAAABjAAAAAQAACSAAAABjAAAAAQAACSwAAABjAAAAAQAACTgAAABjAAAAAQAACUQAAABjAAAAAQAACVAAAABjAAAAAQAACVwAAABjAAAAAQAACWgAAABjAAAAAQAACXQAAABjAAAAAQAACYAAAABjAAAAAQAACYwAAABjAAAAAQAACZgAAABjAAAAAQAACaQAAABjAAAAAQAACbAAAABjAAAAAQAACbwAAABjAAAAAQAACcgAAABjAAAAAQAACdQAAABjAAAAAQAACeAAAABjAAAAAQAACewAAABjAAAAAQAACfgAAABjAAAAAQAACgQAAABjAAAAAQAAChAAAABjAAAAAQAAChwAAABjAAAAAQAACigAAABjAAAAAQAACjQAAABjAAAAAQAACkAAAABjAAAAAQAACkwAAABjAAAAAQAAClgAAABjAAAAAQAACmQAAABjAAAAAQAACnAAAABjAAAAAQAACnwAAABjAAAAAQAACogAAABjAAAAAQAACpQAAABjAAAAAQAACqAAAABjAAAAAQAACqwAAABjAAAAAQAACrgAAABjAAAAAQAACsQAAABjAAAAAQAACtAAAABjAAAAAQAACtwAAABjAAAAAQAACugAAABjAAAAAQAACvQAAABjAAAAAQAACwAAAABjAAAAAQAACwwAAABjAAAAAQAACxgAAABjAAAAAQAACyQAAABjAAAAAQAACzAAAABjAAAAAQAACzwAAABjAAAAAQAAC0gAAABjAAAAAQAAC1QAAABjAAAAAQAAC2AAAABjAAAAAQAAC2wAAABjAAAAAQAAC3gAAABjAAAAAQAAC4QAAABjAAAAAQAAC5AAAABjAAAAAQAAC5wAAABjAAAAAQAAC6gAAABjAAAAAQAAC7QAAABjAAAAAQAAC8AAAABjAAAAAQAAC8wAAABjAAAAAQAAC9gAAABjAAAAAQAAC+QAAABjAAAAAQAAC/AAAABjAAAAAQAAC/wAAABjAAAAAQAADAgAAABjAAAAAQAADBQAAABjAAAAAQAADCAAAABjAAAAAQAADCwAAABjAAAAAQAADDgAAABjAAAAAQAADEQAAABjAAAAAQAADFAAAABjAAAAAQAADFwAAABjAAAAAQAADGgAAABjAAAAAQAADHQAAABjAAAAAQAADIAAAABjAAAAAQAADIwAAABjAAAAAQAADJgAAABjAAAAAQAADKQAAABjAAAAAQAADLAAAABjAAAAAQAADLwAAABjAAAAAQAADMgAAABjAAAAAQAADNQAAABjAAAAAQAADOAAAABjAAAAAQAADOwAAABjAAAAAQAADPgAAABjAAAAAQAADQQAAAAuAAAAAQAADRAAAAAAAAABKAAAADIAAAAAAAAAAAAAAAAAAA0sAAAAAAAAAAAAAAAAAAAAAQAAAAA="},"names_b64":["YS5jY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2Nj","TGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGQ="],"labels":[["x/y",0],["x/y",0]]}
{"id":"fgets-03-text","class":"fgets","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp4L3k6Ki5jY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjCjUwOngveTpsZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZAo="},"names_b64":["YS5jY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2Nj","TGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGQ="],"labels":[["application/octet-stream",1],["application/octet-stream",1]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F5. glob weight is a signed sentinel in globs2 and a masked 0xff value in the cache

`update-mime-database` 2.5.1 accepts a glob weight of 0..100 only; 101 or more (and negatives) is rejected with `Bad weight (-1)` and written as `-1` in `globs2`. Text mode's `atoi` gives weight -1 (lowest); the cache stores `weight & 0xff` = 255 (highest), cs bit clear (decoded from the cache: weight 255, `cs=False`). Two types on the same glob therefore flip winner. 5 layouts, 24 answers. The minimal pair uses weight 300 (>255) vs 50; the sweep also covers 101, 200, 254 and -5.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"weight-01-cache","class":"weight","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWxvOiouenoKLTE6YXBwbGljYXRpb24veC1oaToqLnp6Cg==","dh/mime/mime.cache":"AAEAAgAAAFQAAABYAAAAXAAAAGAAAACkAAAAqAAAALQAAAC4AAAAvAAAAMBhcHBsaWNhdGlvbi94LWhpAAAAAGFwcGxpY2F0aW9uL3gtbG8AAAAAAAAAAAAAAAAAAAAAAAAAAQAAAGgAAAB6AAAAAQAAAHQAAAB6AAAAAQAAAIAAAAAuAAAAAgAAAIwAAAAAAAAALAAAAP8AAAAAAAAAQAAAADIAAAAAAAAAAAAAAAAAAAC0AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA"},"names_b64":["YS56eg=="],"labels":[["application/x-hi",1]]}
{"id":"weight-01-text","class":"weight","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWxvOiouenoKLTE6YXBwbGljYXRpb24veC1oaToqLnp6Cg=="},"names_b64":["YS56eg=="],"labels":[["application/x-lo",1]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F5b. Negative XML weight, same sentinel

`weight="-5"` takes the same `-1` path; cache 255 beats 50, text -1 loses. 1 of the 5 F5 layouts.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"weight-02-cache","class":"weight","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LXBvczoqLnYKLTE6YXBwbGljYXRpb24veC1uZWc6Ki52Cg==","dh/mime/mime.cache":"AAEAAgAAAFQAAABYAAAAXAAAAGAAAACYAAAAnAAAAKgAAACsAAAAsAAAALRhcHBsaWNhdGlvbi94LW5lZwAAAGFwcGxpY2F0aW9uL3gtcG9zAAAAAAAAAAAAAAAAAAAAAAAAAQAAAGgAAAB2AAAAAQAAAHQAAAAuAAAAAgAAAIAAAAAAAAAALAAAAP8AAAAAAAAAQAAAADIAAAAAAAAAAAAAAAAAAACoAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA"},"names_b64":["YS52"],"labels":[["application/x-neg",1]]}
{"id":"weight-02-text","class":"weight","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LXBvczoqLnYKLTE6YXBwbGljYXRpb24veC1uZWc6Ki52Cg=="},"names_b64":["YS52"],"labels":[["application/x-pos",1]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F6. Duplicate (pattern, mime) across dirs keeps the first weight in text and MAX in cache

The text hash inserts a duplicate pattern+mime once and keeps the first weight (xdgmimeglob.c:100-120 dedupe, :222-272 no update on an existing mime). Each cache contributes its own entry and `filter_out_dupes` keeps `MAX(weight)` (xdgmimecache.c:641-665). s1 A `*.p` w50, s2 A `*.p` w90 + B `*.p` w60: text sorts A(50) below B(60) -> B; cache A(90) -> A. 1 layout, 6 answers.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"dirs-01-cache","class":"dirs","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":null,"XDG_DATA_DIRS":"{root}/s1:{root}/s2"},"files":{"s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWE6Ki5wCg==","s1/mime/mime.cache":"AAEAAgAAADwAAABAAAAARAAAAEgAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJBhcHBsaWNhdGlvbi94LWEAAAAAAAAAAAAAAAAAAAAAAQAAAFAAAABwAAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAADIAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA=","s2/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo5MDphcHBsaWNhdGlvbi94LWE6Ki5wCjYwOmFwcGxpY2F0aW9uL3gtYjoqLnAK","s2/mime/mime.cache":"AAEAAgAAAEwAAABQAAAAVAAAAFgAAACQAAAAlAAAAKAAAACkAAAAqAAAAKxhcHBsaWNhdGlvbi94LWIAYXBwbGljYXRpb24veC1hAAAAAAAAAAAAAAAAAAAAAAEAAABgAAAAcAAAAAEAAABsAAAALgAAAAIAAAB4AAAAAAAAADwAAABaAAAAAAAAACwAAAA8AAAAAAAAAAAAAAAAAAAAoAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAA=="},"names_b64":["YS5w"],"labels":[["application/x-a",1]]}
{"id":"dirs-01-text","class":"dirs","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":null,"XDG_DATA_DIRS":"{root}/s1:{root}/s2"},"files":{"s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWE6Ki5wCg==","s2/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo5MDphcHBsaWNhdGlvbi94LWE6Ki5wCjYwOmFwcGxpY2F0aW9uL3gtYjoqLnAK"},"names_b64":["YS5w"],"labels":[["application/x-b",1]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F7. Cache takes the deepest suffix match per cache, text takes one global deepest match

Text builds one hash across all dirs and the deepest suffix wins globally (xdgmimeglob.c:461-480). `cache_glob_lookup_suffix` runs per cache and each cache contributes its own deepest match (xdgmimecache.c:574-605, :696-705). s1 A `*.gz` w60, s2 B `*.tar.gz` w50: cache returns A(60) and B(50) -> A, uncertain 1; text returns only B -> certain 0. 1 layout, 9 answers.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"deep-01-cache","class":"deep","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":null,"XDG_DATA_DIRS":"{root}/s1:{root}/s2"},"files":{"s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWd6OiouZ3oK","s1/mime/mime.cache":"AAEAAgAAAEAAAABEAAAASAAAAEwAAACEAAAAiAAAAJQAAACYAAAAnAAAAKBhcHBsaWNhdGlvbi94LWd6AAAAAAAAAAAAAAAAAAAAAAAAAAEAAABUAAAAegAAAAEAAABgAAAAZwAAAAEAAABsAAAALgAAAAEAAAB4AAAAAAAAACwAAAA8AAAAAAAAAAAAAAAAAAAAlAAAAAAAAAAAAAAAAAAAAAEAAAAA","s2/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0ZXh0L3gtdGd6OioudGFyLmd6Cg==","s2/mime/mime.cache":"AAEAAgAAADgAAAA8AAAAQAAAAEQAAACsAAAAsAAAALwAAADAAAAAxAAAAMh0ZXh0L3gtdGd6AAAAAAAAAAAAAAAAAAAAAAABAAAATAAAAHoAAAABAAAAWAAAAGcAAAABAAAAZAAAAC4AAAABAAAAcAAAAHIAAAABAAAAfAAAAGEAAAABAAAAiAAAAHQAAAABAAAAlAAAAC4AAAABAAAAoAAAAAAAAAAsAAAAMgAAAAAAAAAAAAAAAAAAALwAAAAAAAAAAAAAAAAAAAABAAAAAA=="},"names_b64":["YS50YXIuZ3o="],"labels":[["application/x-gz",1]]}
{"id":"deep-01-text","class":"deep","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":null,"XDG_DATA_DIRS":"{root}/s1:{root}/s2"},"files":{"s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWd6OiouZ3oK","s2/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0ZXh0L3gtdGd6OioudGFyLmd6Cg=="},"names_b64":["YS50YXIuZ3o="],"labels":[["text/x-tgz",0]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F8. One valid cache switches every directory to caches-only; globs-only dirs are ignored

`xdgmime.c:645-646`: if any cache loaded, lookups use `_xdg_mime_cache_get_mime_types_from_file_name`; a directory that contributed only `globs2` is not consulted. A high-priority dir with `globs2` and no cache therefore disappears in cache mode and is read in text mode. 3 layouts, 15 answers (`L43` cache absent; `L44` version 1.0; `L45` 20-byte cache).

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"mode-01-cache","class":"mode","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWJhZDoqLmJhZAo=","s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LW1peDoqLm1peAo=","s1/mime/mime.cache":"AAEAAgAAAEAAAABEAAAASAAAAEwAAACQAAAAlAAAAKAAAACkAAAAqAAAAKxhcHBsaWNhdGlvbi94LW1peAAAAAAAAAAAAAAAAAAAAAAAAAEAAABUAAAAeAAAAAEAAABgAAAAaQAAAAEAAABsAAAAbQAAAAEAAAB4AAAALgAAAAEAAACEAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAoAAAAAAAAAAAAAAAAAAAAAEAAAAA"},"names_b64":["YS5iYWQ=","YS5taXg="],"labels":[["application/octet-stream",1],["application/x-mix",0]]}
{"id":"mode-01-text","class":"mode","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWJhZDoqLmJhZAo=","s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LW1peDoqLm1peAo="},"names_b64":["YS5iYWQ=","YS5taXg="],"labels":[["application/x-bad",0],["application/x-mix",0]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F9. Cache folded-literal search aborts on the first case-sensitive literal hit

`cache_glob_lookup_literal` in the folded pass returns 0 immediately when the found entry is case-sensitive (xdgmimecache.c:420-424), aborting the scan of later caches; the following exact pass compares the original name. Text's folded pass skips cs literals and continues to the next literal (xdgmimeglob.c:453-467). Two producible forms: across dirs (s1 cs literal `makefile` type b, s2 non-cs `makefile` type a) and inside one dir (type b cs, type a non-cs, same pattern). `MAKEFILE` -> cache `application/octet-stream` uncertain 1, text `application/x-a` certain 0 in both. 2 layouts, 5 answers.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"cs-01-cache","class":"cs","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":null,"XDG_DATA_DIRS":"{root}/s1:{root}/s2"},"files":{"s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWI6bWFrZWZpbGU6Y3MKNjA6YXBwbGljYXRpb24veC1iOm1ha2VmaWxlCg==","s1/mime/mime.cache":"AAEAAgAAAEgAAABMAAAAUAAAAGAAAABoAAAAbAAAAHgAAAB8AAAAgAAAAIRhcHBsaWNhdGlvbi94LWIAbWFrZWZpbGUAAAAAAAAAAAAAAAAAAAABAAAAPAAAACwAAAE8AAAAAAAAAGgAAAAAAAAAAAAAAAAAAAB4AAAAAAAAAAAAAAAAAAAAAQAAAAA=","s2/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWE6bWFrZWZpbGUK","s2/mime/mime.cache":"AAEAAgAAAEgAAABMAAAAUAAAAGAAAABoAAAAbAAAAHgAAAB8AAAAgAAAAIRhcHBsaWNhdGlvbi94LWEAbWFrZWZpbGUAAAAAAAAAAAAAAAAAAAABAAAAPAAAACwAAAAyAAAAAAAAAGgAAAAAAAAAAAAAAAAAAAB4AAAAAAAAAAAAAAAAAAAAAQAAAAA="},"names_b64":["TUFLRUZJTEU="],"labels":[["application/octet-stream",1]]}
{"id":"cs-01-text","class":"cs","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":null,"XDG_DATA_DIRS":"{root}/s1:{root}/s2"},"files":{"s1/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWI6bWFrZWZpbGU6Y3MKNjA6YXBwbGljYXRpb24veC1iOm1ha2VmaWxlCg==","s2/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDphcHBsaWNhdGlvbi94LWE6bWFrZWZpbGUK"},"names_b64":["TUFLRUZJTEU="],"labels":[["application/x-a",0]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

### F9b. Same abort with the two literals in one directory

One dir, type b `makefile` cs, type a `makefile` non-cs: the cache literal table keeps both; the folded binary search lands on the cs entry and returns 0, so `MAKEFILE`/`Makefile` are octet uncertain 1 in cache and `application/x-a` certain 0 in text (cache bytes deterministic across three regenerations, sha256 `1fa054b1483f2549…`). 1 layout, 2 answers.

Minimal pair (CASE FILE SCHEMA; `labels` are oracle answers, DRAFT re-verified on a bare
materialisation):

```json
{"id":"cs-02-cache","class":"cs","mode":"cache","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWI6bWFrZWZpbGU6Y3MKNjA6YXBwbGljYXRpb24veC1iOm1ha2VmaWxlCjUwOmFwcGxpY2F0aW9uL3gtYTptYWtlZmlsZQo=","dh/mime/mime.cache":"AAEAAgAAAFgAAABcAAAAYAAAAHwAAACEAAAAiAAAAJQAAACYAAAAnAAAAKBhcHBsaWNhdGlvbi94LWIAYXBwbGljYXRpb24veC1hAG1ha2VmaWxlAAAAAAAAAAAAAAAAAAAAAgAAAEwAAAAsAAABPAAAAEwAAAA8AAAAMgAAAAAAAACEAAAAAAAAAAAAAAAAAAAAlAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAA=="},"names_b64":["TUFLRUZJTEU=","TWFrZWZpbGU="],"labels":[["application/octet-stream",1],["application/octet-stream",1]]}
{"id":"cs-02-text","class":"cs","mode":"text","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh","XDG_DATA_DIRS":"{root}/s1"},"files":{"dh/mime/globs2":"IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LWI6bWFrZWZpbGU6Y3MKNjA6YXBwbGljYXRpb24veC1iOm1ha2VmaWxlCjUwOmFwcGxpY2F0aW9uL3gtYTptYWtlZmlsZQo="},"names_b64":["TUFLRUZJTEU=","TWFrZWZpbGU="],"labels":[["application/x-a",0],["application/x-a",0]]}
```

Candidate on this pair: 2/2 cases follow the oracle (cache/text: ['ok', 'ok']).

## Candidate fidelity (DRAFT)

| mode | layouts | equal to the oracle | refused (exit 3) | wrong answers |
|---|---|---|---|---|
| cache | 56 | 56 | 0 | 0 |
| text | 56 | 54 | 2 | 0 |

The two text-mode refusals are `L23-star-alone` and `L52-star-plus-suffix`, both containing a
bare `*` glob. `update-mime-database` writes it as `50:application/x-star:*`; GLib ignores it in
both modes (verified directly: `noext`, `a.b`, `foo.c` -> `application/octet-stream` uncertain 1),
but the candidate refuses the whole run:

```
$ python3 -I .ufo/waves/round-94/build/mado-mimeglob.c1.py --json --home <h> --data-home <dh> \
    --data-dirs <sd> noext a.b foo.c
MADO_MIMEGLOB: UNSUPPORTED <dh>//globs2: simple glob with an empty suffix
rc=3
```

That is a permitted refusal (exit 3), never a wrong answer, but it removes *every* answer for a
database that contains this producible row. The frozen generator/case set should either exclude
`<glob pattern="*">` or the tool should treat an empty-suffix simple glob as GLib does (a no-op
that never matches). Candidate `--selftest` (DRAFT): `MADO_MIMEGLOB_SELFTEST: checks=15 failed=0`,
rc 0.

## Controls: where the hypothesis holds (no divergence)

L01 disjoint simple globs; L02/L03 multi-extension depth both orders; L04/L05 weight order and
ties; L06/L07 cs simple globs; L12 full glob with a middle star; L13 escaped star; L15/L17/L18/
L19 literals incl. capitals and non-ASCII; L20/L21/L22 duplicate and multi-type globs; L23 bare
`*`/`**`; L24 `*.`; L29/L30 non-ASCII suffixes (neither mode matches, both octet); L33 weight
100 vs 99 (100 is the accepted maximum); L34 weight 0; L37/L38 glob-deleteall (neither mode
deletes inherited globs); L41 disjoint dirs; L47 literal vs a heavier simple glob (literal wins in
both); L49 cs simple glob with an uppercase pattern; L50 trailing slash (inode/directory both);
L51 HOME-only dir; L52 `*` + `*.txt`.

Mechanisms read but *not* observed as divergences, worth not re-probing: `__NOGLOBS__` is a
literal-to-nowhere in both modes (neither implements glob-deleteall across dirs); non-ASCII bytes
in a suffix never match in either mode (signed-char widening, xdgmimeglob.c:319 /
xdgmimecache.c:512); empty, `.` and `..` names agreed in every layout (e.g. `L24` `*.` matches the empty name and `.` in both modes); trailing `/` short-circuits before
the databases (gcontenttype-fdo.c:597-603); weights 0..100 are identical in both modes.

## Residual risk / verification gaps

- The sweep samples the layout space (56 layouts, 9 mechanisms); it is not a proof over every
  producible layout. The mechanisms map to four independent code differences (name folding for
  full globs, literal pass order, text-vs-binary serialization limits, and cache aggregation), so
  further classes are possible at the boundaries I did not exercise: >10 competing types (both
  sides cap at 10), cache minor 1.1, v1 `globs` fallback, offsets/bounds corruption (the candidate
  refuses some of these; the oracle may loop), and locale-dependent `fnmatch` (all runs used
  `LC_ALL=C`).
- Data sniffing is out of scope: the oracle passes `data=NULL, size=0`, so only the name path is
  exercised (`g_content_type_guess` conflict/tie logic at gcontenttype-fdo.c:613-620, 675-683 is
  still what turns `types` into the printed `uncertain`).
- The oracle is the installed glib2 2.90.1-1 binary; I did not rebuild glib from the fetched tag.
  The fetched files' digests match the L1 receipts, and every mechanism above is confirmed by
  observed behaviour, not only by source reading.
- Names are UTF-8 argv strings; invalid-UTF-8 names and NUL bytes are not exercised.

## Runs (all DRAFT; no installs)

| command | rc | result |
|---|---|---|
| `gcc -O1 -o $S/bin/oracle controls/mimeglob-oracle-r94.c $(pkg-config --cflags --libs gio-2.0)` | 0 | oracle built |
| `python3 $S/probe.py` | 0 | 56 layouts, 9521 name-runs, 117 divergences |
| `python3 $S/pairgen.py` | 0 | 16 pairs / 32 cases, candidate 32/32 |
| `python3 -I build/mado-mimeglob.c1.py --selftest` | 0 | checks=15 failed=0 |
| oracle/candidate bare-`*` repro | 0 / 3 | octet / UNSUPPORTED |

Dead step: the first attempt to patch the probe with an inline Python heredoc hit
`AssertionError` on the anchor text and the rerun used the unpatched files; the patch was redone
with `edit` and the rerun succeeded. No data from the failed patch step survives.

Scratch `/fast/scratch/hyaku/mado-r94/R94MProbeC1` is removed after this report is written.
