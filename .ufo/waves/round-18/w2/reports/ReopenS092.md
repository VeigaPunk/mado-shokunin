# W2 / ReopenS092 — non-author re-open of SOURCES row S092 (R17-V3)

Seat: `MadoR18.ReopenS092` (leaf; no dispatch). Date: 2026-10-20.
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only work: working-tree
bytes, `git show`/`git diff`/`git cat-file` on the lane (read-only git only, no
`git status`), `git ls-remote` from `/tmp`, and one `curl` set under
`.ufo/waves/round-18/fetch/ReopenS092/`. No jj command, no lane VCS write, no
package/service/compositor/input/screenshot/REA operation, no install or update
(nothing to record under the tooling directive).

Question: is S092 — a newly credited row (R17-V3) — byte-true, correctly tiered
and scoped, and used truthfully by `corpus/knowledge/theme-route-r18.md`, checked
against my own fetch rather than the author's?

## Commands run and their output

### 1. Re-fetch with receipts

```
cd .ufo/waves/round-18/fetch/ReopenS092
curl -sSL --max-time 60 -o <slug> -w '%{http_code} %{url_effective}' \
  https://raw.githubusercontent.com/swaywm/swaybg/v1.2.2/<swaybg.1.scd|README.md|main.c|background-image.c>
```

Output (code, bytes, sha256, slug):

```
200 1124  68ed5503298fc845df946416630bbc5ea1b6f8bc24ef2ee3e03a7efec8ae8618  swaybg.1.scd
200 1026  a6720ded1ad3dcd0c66928c8a77c102bed41013e472d7ffcbc532203275da242  README.md
200 21390 ff93e60c00f9b1b960fa0d3a939183f1a57f13514540f41c50067b850dd1a805  main.c
200 3993  9aea12fc179f7223751333931b3b29c8c3570a54fb633887afa3014d7bbe1bd0  background-image.c
```

Four `mado-fetch-receipt-v1` lines appended to
`.ufo/waves/round-18/fetch/ReopenS092/receipts.jsonl`, each with all nine fields
(schema, url, final_url, http_status, fetched_at UTC Z, bytes, sha256, body, tool =
`curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0`).

### 2. Digest reconciliation (row anchor vs every wave-1 receipt vs mine)

Receipts were enumerated mechanically over every
`.ufo/waves/round-18/fetch/*/receipts.jsonl` (JSON parse, filter `swaywm/swaybg`).
Exactly two wave-1 seats fetched these four URLs: `MadoR18.SrcSwaybgMan` and
`NoteTheme` (each also fetched two uncited meson files).

| file | row anchor sha256 (S092) | SrcSwaybgMan line/time | NoteTheme line/time | ReopenS092 time | verdict |
|---|---|---|---|---|---|
| swaybg.1.scd | 68ed5503…8618 | 1 / 15:41:10Z | 10 / 15:40:41Z | 15:59:56Z | all identical |
| README.md | a6720ded…a242 | 2 / 15:41:10Z | 8 / 15:40:33Z | 15:59:56Z | all identical |
| main.c | ff93e60c…a805 | 3 / 15:41:10Z | 11 / 15:40:41Z | 15:59:56Z | all identical |
| background-image.c | 9aea12fc…bd0 | 4 / 15:41:10Z | 17 / 15:41:57Z | 15:59:57Z | all identical |

Byte counts agree too (1124 / 1026 / 21390 / 3993). Persisted bodies were re-hashed
on disk, not just trusted from the receipt text: all four bodies in both wave-1
seats (and mine) hash to the sha256 each receipt claims. Three independent fetch
times (15:40–15:41Z and 15:59Z), three seats, one digest per file.

### 3. Tag pinning

```
cd /tmp && git ls-remote --tags https://github.com/swaywm/swaybg 'refs/tags/v1.2.2*'
3ca0f88fee1a0c83f26ffe2341207d84c7243e7a	refs/tags/v1.2.2
a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2	refs/tags/v1.2.2^{}
```

`v1.2.2` is an annotated tag object `3ca0f88f…` peeling to commit `a59ea3db…`, so
the row's "tag object peeled to a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2" is
exact. The URL is **tag-pinned** (the `v1.2.2` tag name is the path component,
not a commit id). It is not commit-pinned: a force-moved tag would change future
bytes, which is exactly why the anchor cell's raw sha256 and the committed
receipts matter; re-verification is a digest comparison, and today's bytes match.

### 4. Is the checked row the integrated one?

```
git cat-file -t 4c103b55b1ea5c3c555884afe3eb69b5189701b7   -> commit
git show 4c103b5:corpus/SOURCES.md | sha256sum            -> 9552071c0b286075…f26de
sha256sum corpus/SOURCES.md                               -> 9552071c0b286075…f26de
git show 4c103b5:corpus/knowledge/theme-route-r18.md | sha256sum -> b080bc479be4…9f23
sha256sum corpus/knowledge/theme-route-r18.md             -> b080bc479be4…9f23
git diff --stat 4c103b5 -- corpus/SOURCES.md corpus/knowledge/theme-route-r18.md
                                                          -> (empty)
```

The row and the citing note I read are byte-identical to the integration commit.

## Judgement

### kind — `docs` is right

The row's payload is documentary: the man page's option text, the README's
compatibility statement, plus the two code sites that implement the documented
default. This is a manual-first row that cites code to confirm implementation;
`docs` describes it correctly (rubric V accepts `docs`/`spec`/`code`, and the
kind is not a loophole here).

### tier A — a primary source for this scope

The source is the upstream swaywm repository at its release tag, not a mirror, a
third-party blog, a distro page or a package database. For the scope "what
swaybg's own option set/default/requirements are", the tag's own bytes are
primary. Tier A holds.

### scope and keyword

Scope: "upstream wallpaper utility swaybg: option set, default scaling mode,
image read by path; wlr-layer-shell requirement" — names both `wallpaper` and
`swaybg`, so rubric V's P5 surface keyword (theme/wallpaper/hyprpaper/swaybg) is
present in the scope cell itself, independent of the source cell.

I replicated the instrument's upstream filter on the committed row:
kind `docs` ∈ {docs,spec,code}; `https://` present in the source cell; keyword
present in source+scope; status `mined`; tier `A`; `used-by` split contains
`corpus/knowledge/theme-route-r18.md`. The note's head `source:` token S092
resolves through `mined_a()`, and the note declares exactly one `surface: P5`,
has all four required `##` headings with content above the floor, and 10 `[UNK]`
entries under `## Unexercised behavior`. The row is credited for the stated
reason, not by a legacy mapping or a stray keyword.

### teaches — every clause grounded

| teaches clause | bytes |
|---|---|
| `-i` sets the image path | `swaybg.1.scd:25-26`; `main.c:521-523` (`case 'i': config->image_path = optarg`) |
| `-m` sets the mode | `swaybg.1.scd:28-29`; `main.c:524-528` (parse + log invalid) |
| a path without `-m` defaults to stretch | `main.c:572-577`: `config->mode == BACKGROUND_MODE_INVALID` → `image_path ? STRETCH : SOLID_COLOR`; man page 29-30 "Default is _stretch_" |
| image opened by path at load time | `main.c:657-666`: `wl_list_for_each(image, &state.images, …)`, `load_background_image(image->path)`; `background-image.c:24-46`: `gdk_pixbuf_new_from_file(path)` / `cairo_image_surface_create_from_png(path)` |
| "each distinct image path" (note) | `main.c:597-610` dedups on `strcmp(image->path, config->image_path)` — literal |
| wlr-layer-shell requirement | `README.md:3-5` verbatim |

The stated limits are honest: nothing here shows which swaybg (if any) runs on
any host, nor whether a live process re-reads a retargeted symlink; the row says
so and excludes both.

### citing note — truthful

`corpus/knowledge/theme-route-r18.md:69-72` and `:137` cite exactly these ranges
and describe them accurately (option list, default stretch, parsing, load by
path, gdk-pixbuf/cairo fallback, wlr-layer-shell + `wl_output` v4). Line 137
keeps the re-read-on-retarget question as `[UNK]`, matching the row's limit.
Two cosmetic nits that change no fact:

1. Line 69's clause "Per-output options exist via `-o`" sits inside the
   `[SW:19-31]` bullet, but `-o` is at `swaybg.1.scd:33-35` (and `-v` at 37-38);
   the range under-covers a true statement.
2. Similarly, the row's scope phrase "option set" is anchored to 19-31, which
   covers `-c/-h/-i/-m` only. The `teaches` cell is narrower and true.

Neither is a false claim nor an invented observation; both are anchor-range
hygiene for the next reopen.

### Evidence hygiene

- Same URL has exactly two wave-1 receipts; both 200, same sha256. The two extra
  meson receipts (`MadoR18.SrcSwaybgMan` lines 5-6) are not cited by the row.
- Both seats' body files exist beside their receipts and hash to the recorded
  values (recomputed here), so a closure can reproduce the fetch rather than
  trust the row.
- My four receipts add a third independent read. No discrepancy anywhere.

## What this check does not establish

- Bytes as of a future date: the URL is tag-pinned, so only the sha256 anchor
  detects a moved tag (the row carries the anchor and `recheck: on-release`).
- Whether the host's `swaybg 1.2.2-1` package was built from this tag without
  patches, or whether any swaybg process is running — both excluded by the row
  and the note.
- The two implementation files were read, not compiled or executed.

## Verdict

agree. Row S092's four anchors re-fetch byte-identical (3 seats, 3 times), the
tag peel `a59ea3db…` resolves, tier A is primary for the P5 scope, `teaches` and
the citing note are truthful; only cosmetic anchor-range nits found.

GATE | S092 | https://raw.githubusercontent.com/swaywm/swaybg/v1.2.2/swaybg.1.scd | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS092/swaybg.1.scd:29-30 "Scaling mode for images: _stretch_, _fill_, _fit_, _center_, or _tile_. Default is _stretch_." (13 words) | 68ed5503298fc845df946416630bbc5ea1b6f8bc24ef2ee3e03a7efec8ae8618 | agree: four anchors re-fetched identical across three seats, tag peels to a59ea3db, tier-A P5 row and note truthful
