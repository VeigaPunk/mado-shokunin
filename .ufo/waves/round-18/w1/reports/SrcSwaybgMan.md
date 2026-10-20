# SrcSwaybgMan — swaybg(1) man-page source at upstream tag v1.2.2

Seat `MadoR18.SrcSwaybgMan`, round 18 (hyaku phase 2). Assignment: fetch
`swaybg.1.scd` from `github.com/swaywm/swaybg` at its latest tag with a
committed raw fetch receipt, record `-i`, `-m`, `-o` with verbatim quotes, and
record the host swaybg version as `[UNK]` (no package query was made).

Fence honoured: no pacman/yay/expac/checkupdates, no `sudo`, no systemctl or
compositor verb, no `swaybg`/`swaybg --version` execution, no input or
screenshot probe. Reads were HTTP GETs (curl, no auth/cookies) plus byte reads
of `~/.local/share/omarchy/**` files. No tool was installed or upgraded this
seat; the only tools used were `curl 8.23.0` and read-only `git ls-remote`.
No files outside this report and my own fetch directory were written.

Tags: `[OBS]` measured from fetched bytes or file bytes · `[INF]` inference
from measured parts · `[UNK]` unknown.

## §0 Axes

1. **Anchor fidelity** — every quoted word must resolve to a byte in a
   receipted body and a line number.
2. **Receipt completeness** — tag→commit pinned, raw body stored, digest named,
   reproducible on a second fetch.
3. **P5 usability** — the P5 route note can cite the upstream contract without
   inventing host behaviour.
4. **Harm** — zero host state touched; host binary stays `[UNK]`.

All four moved with one fetch set; no axis was traded against another.

## §1 Tag resolution and receipts

`git ls-remote --tags https://github.com/swaywm/swaybg` `[OBS]`, 2026-10-20:

```
ba4ba948ad2334d680abc114fee4f6f3bd134916  refs/tags/v1.2.1
dcb5ebc76adcfef81c1a275ae7ed21a7936cbd7c  refs/tags/v1.2.1^{}
3ca0f88fee1a0c83f26ffe2341207d84c7243e7a  refs/tags/v1.2.2
a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2  refs/tags/v1.2.2^{}
a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2  refs/heads/master
```

Latest tag = **v1.2.2**, peeled commit **a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2**;
`refs/heads/master` pointed at the *same* commit on 2026-10-20 `[OBS]` — so the
tag is the head, not a lagging branch point. Repository had no `v`-less 1.2.1
ref; the earlier attempt `refs/tags/1.2.1` returned nothing, which is why the
tag spelling was established before fetching.

Bodies saved under
`.ufo/waves/round-18/fetch/MadoR18.SrcSwaybgMan/`, one JSON line per fetch in
`receipts.jsonl` (6 lines, schema `mado-fetch-receipt-v1`):

| body | bytes | sha256 (prefix) | http | anchor role |
|---|---|---|---|---|
| `swaybg.1.scd` | 1124 | `68ed5503298fc845…` | 200 | the man-page **source** (scdoc) — options `-i`/`-m`/`-o` |
| `README.md` | 1026 | `a6720ded1ad3dcd0…` | 200 | compositor/protocol requirement |
| `main.c` | 21390 | `ff93e60c00f9b1b9…` | 200 | CLI parsing, defaults, layer-surface constant |
| `background-image.c` | 3993 | `9aea12fc179f7223…` | 200 | exact mode strings, image loader |
| `meson.build` | 3315 | `6e607771dbb03458…` | 200 | project version, `SWAYBG_VERSION` shape |
| `meson_options.txt` | 206 | `cf036e215c499a51…` | 200 | optional gdk-pixbuf feature |

Reproducibility `[OBS]`: all five v1.2.2 files were fetched twice (≈15:40Z and
15:41:10Z) and every digest matched across the two fetches; `meson_options.txt`
was fetched once afterwards. Every receipt carries its own `fetched_at`,
`bytes`, `sha256` and `tool` (`curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0`).
All URLs are tag-pinned `raw.githubusercontent.com/swaywm/swaybg/v1.2.2/<path>`,
`final_url` equals `url` (no redirect), `http_status` 200.

Reproduce (from the fetch dir):

```
curl -sSL --max-time 60 -o swaybg.1.scd -w '%{http_code} %{url_effective}' \
  https://raw.githubusercontent.com/swaywm/swaybg/v1.2.2/swaybg.1.scd
sha256sum swaybg.1.scd   # 68ed5503298fc845df946416630bbc5ea1b6f8bc24ef2ee3e03a7efec8ae8618
```

## §2 Upstream contract — the three assigned options, quoted

The man page is scdoc source; `# OPTIONS` is `swaybg.1.scd:17`, and the whole
option block is `:17-38`. Quotes are verbatim (scdoc emphasis markers kept)
with their line anchors; each is ≤25 words.

### `-i, --image`

`swaybg.1.scd:25-26`:

```
*-i, --image* <path>
	Set the background image.
```

Quote: "Set the background image." (`:26`).

`main.c:509` — `getopt_long(argc, argv, "c:hi:m:o:v", …)` `[OBS]`; the `i:`
colon makes the argument **required**. `main.c:521-523` stores the string
verbatim into `config->image_path` with no normalisation. There is no `~`
expansion anywhere in `main.c` or `background-image.c` (`grep -nE
'wordexp|getenv|HOME|g_build_filename'` returned nothing) `[OBS]`: the path is
passed straight to `gdk_pixbuf_new_from_file(path)` (`background-image.c:28`)
or `cairo_image_surface_create_from_png(path)` (`background-image.c:41`). Any
`~` in a declared argv must therefore be expanded by the *launcher*
(`uwsm-app`/Hyprland exec), not by swaybg `[INF]`.

### `-m, --mode`

`swaybg.1.scd:28-31`:

```
*-m, --mode* <mode>
	Scaling mode for images: _stretch_, _fill_, _fit_, _center_, or _tile_.
	Default is _stretch_. Use the additional mode _solid\_color_ to display
	only the background color, even if a background image is specified.
```

Three quotes, each under 25 words:
"Scaling mode for images: _stretch_, _fill_, _fit_, _center_, or _tile_."
(`:29`) · "Default is _stretch_." (`:30`) · "Use the additional mode
_solid\_color_ to display only the background color, even if a background image
is specified." (`:30-31`).

The accepted strings are six lowercase exact `strcmp` matches —
`stretch`, `fill`, `fit`, `center`, `tile`, `solid_color`
(`background-image.c:6-22`) `[OBS]` — so `-m Fill` is **not** accepted and is
not case-folded.

### `-o, --output`

`swaybg.1.scd:33-35`:

```
*-o, --output* <name>
	Select an output to configure. Subsequent appearance options will only
	apply to this output. The special value _\*_ selects all outputs.
```

Quotes: "Select an output to configure." (`:33`) · "Subsequent appearance
options will only apply to this output." (`:34`) · "The special value _\*_
selects all outputs." (`:35`).

The framing sentence is `swaybg.1.scd:13-15` "Without an output specified,
appearance options apply to all outputs." — the default block is `-o *`
(`main.c:502-503`) `[OBS]`.

### Adjacent surface, for completeness

`-c, --color <[#]rrggbb>` (`:19-20`, "Set the background color."), `-h,
--help` (`:22-23`), `-v, --version` (`:37-38`). `-v` prints
`"swaybg version " SWAYBG_VERSION` and exits **during option parsing**
(`main.c:540-543`), i.e. before `wl_display_connect` at `main.c:614` `[OBS]`.
Protocol requirement, `README.md:3-5`: "It is compatible with any Wayland
compositor which implements the wlr-layer-shell protocol and `wl_output`
version 4." (17 words).

## §3 Source semantics the man page does not state

These matter because a route note citing "the man page says default stretch"
would be incomplete. All `[OBS]` from `main.c` at the receipted digest.

1. **Default mode is conditional, not flat.** After parsing, a config with
   `mode == BACKGROUND_MODE_INVALID` receives
   `config->image_path ? BACKGROUND_MODE_STRETCH : BACKGROUND_MODE_SOLID_COLOR`
   (`main.c:574-577`). So `swaybg --color '#000000'` with no `-m` resolves to
   `solid_color`, not `stretch`. The man page's "Default is _stretch_." is true
   only when an image is present.
2. **A bad `-m` does not fail the process.** `main.c:525-528` logs
   `"Invalid mode: %s"` and `break`s; the mode stays `INVALID` and is then
   replaced by the default in (1). Case matters (`strcmp`), so a typo
   (`-m Fill`, `-m fill ` with trailing space) silently degrades to the
   default and still connects. A declared argv is therefore *intent*, not a
   guarantee of effect.
3. **`-o` names are never validated.** `find_config` (`main.c:347-357`)
   compares strings and falls back to a `"*"` config only while
   `!output->config`; an exact-name block wins over `*` regardless of
   declaration order. An output name that matches nothing is not an error
   `[INF]`, so a typo means "no config for that output", not a diagnostic.
4. **Duplicate `-o` blocks merge, they do not replace.** `-o` first *stores*
   the previous block, then starts a fresh one (`main.c:530-539`), and
   `store_swaybg_output_config` (`main.c:453-474`) merges a same-named block
   field-by-field (only non-empty image/color and non-`INVALID` mode overwrite).
   Reading two blocks for one output as "last wins" would be wrong.
5. **Empty is not the same as absent.** Usage + `EXIT_FAILURE`
   (`main.c:563-566`) fires only when the config list is *already* empty at
   that check — reachable via trailing non-option arguments, which destroy
   every config first (`main.c:555-562`). A block that merely ends up with no
   image and no colour is removed **after** that check (`main.c:570-574`), so
   `swaybg -o DP-1` alone does **not** exit: it connects, then each output
   finds no config and is destroyed with a debug-level
   `"Could not find config for output …"` (`main.c:325-331`). The process
   stays alive rendering nothing — a live-looking background that paints no
   layer. Corrects the naive reading "an empty invocation fails fast".
6. **The layer namespace is a binary constant.** `zwlr_layer_shell_v1_get_layer_surface(…,
   ZWLR_LAYER_SHELL_V1_LAYER_BACKGROUND, "wallpaper")` (`main.c:308-310`),
   four-edge anchor (`:314-318`), exclusive zone `-1` (`:319`), empty input
   region (`:286-291`). An observed `hyprctl -j layers` namespace `wallpaper`
   is the program's own string, not host configuration — a useful independent
   cross-check for a declared-versus-live comparison.
7. **`--version` string shape depends on the build.** `meson.build:4` sets
   `version: '1.2.2'`, but `meson.build:41-52` replaces it with
   `1.2.2-<shortsha> (__DATE__, branch '<branch>')` when built from a git
   checkout with `git` available. A distro tarball build prints `swaybg version
   1.2.2`; a source build prints the compound string. A version read is
   therefore a build fact, and must be quoted exactly rather than parsed as a
   bare semver `[INF]`.
8. **Image formats.** `gdk-pixbuf` is an `auto` meson feature
   (`meson_options.txt`); without it only PNG decodes and the error text says so
   (`background-image.c:40-52`). A declared `.jpg` wallpaper implies the host
   binary was built with gdk-pixbuf — an inference, never a measurement here.

## §4 Host declaration — what P5 may cite (unchanged from the lane record)

Byte-read this seat `[OBS]`, no execution:

```
file: /home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf
size: 742 B   sha256: acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441
line 5: exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill
```

Checkout identity read as bytes only (no git command in that checkout):
`.git/HEAD` = `ref: refs/heads/master`, `.git/packed-refs` maps
`refs/heads/master` and `refs/tags/v3.8.4` to the same commit
**8fcc9d6048af4cb0e3af8512c78049857a3b53dd** `[OBS]` — i.e. the checkout is at
the v3.8.4 commit per the ref bytes, satisfying the round's "omarchy v3.8.4"
premise without invoking git.

Mapping declared tokens to the upstream contract:

| declared token | upstream anchor | reading |
|---|---|---|
| `swaybg` | `swaybg.1.scd:9` `*swaybg* [options...]` | the binary is invoked directly, not through a subcommand |
| `-i ~/.config/omarchy/current/background` | `:25-26` | image path; `~` must be expanded by `uwsm-app`/exec, swaybg never expands it (§2, §3) |
| `-m fill` | `:28-29` + `background-image.c:9-10` | exact lowercase `fill` is accepted; scales preserving ratio and centres (`background-image.c:72-88`) |
| *(no `-o`)* | `:13` | appearance options apply to **all** outputs — no per-output declaration exists in this file |
| *(no `-m` fallback path)* `--color '#000000'` (writer sibling, round-7 record) | `:19` grammar `[#]rrggbb` | `'#000000'` matches the documented grammar; with no image the default mode is `solid_color` (`main.c:575-577`) |

So the P5 note can state, with two anchors each: the host *declares* one
all-outputs `fill` block over the `current/background` symlink, and the
observed layer namespace `wallpaper` equals the binary constant at
`main.c:310` — declaration and live layer agree for an independent reason.

Boundaries this seat did **not** establish: the host's actual `/usr/bin/swaybg`
argv, its build options, and its version. Host version = **`[UNK]`** — no
package query (`pacman -Q`, `-Si`, `expac`) was run, per the host-wide pause.
The lane's older record `corpus/knowledge/remaining-planes-census.md:245`
("swaybg 1.2.2-1", a round-6 package-shape capture) is documentary lane
evidence, not re-verified now, and its version string coinciding with the
fetched tag is not binary identity.

## §5 Safe observation vs unexercised behaviour

`## Safe observation` material for a P5 route note (documentary, no run):

- `swaybg --version` (or `-v`) needs no compositor: it prints and `exit`s
  inside `parse_command_line` before `wl_display_connect` (`main.c:540-543` vs
  `:614`). It is the cheapest identity read **when the host pause lifts** —
  but it is still executing a compositor-adjacent binary and was not run.
- A connect failure is distinguishable from a parse failure by message:
  `"Unable to connect to the compositor. If your compositor is running, check
  or set the WAYLAND_DISPLAY environment variable."` (`main.c:616-618`) — a
  diagnostic anchor that does not require reading the compositor.
- Reading the declaration is pure file bytes: `autostart.conf:5` above.

`## Unexercised behavior` material (must stay `[UNK]` in the note):

- `[UNK]` host swaybg version, build flags (gdk-pixbuf present?) and argv; no
  process, package or binary inspection was performed.
- `[UNK]` whether the host binary's option surface equals v1.2.2: the installed
  man page derives from some build of this source, and the host may lag or lead
  the tag. The tag's source never proves the host binary.
- `[UNK]` runtime behaviour: layer-surface creation, fractional-scale and
  viewporter negotiation (`main.c:282-319`), monitor hotplug reconfiguration,
  and actual pixel output. None was observed.
- `[UNK]` whether the declared `~` path is expanded by `uwsm-app` in the live
  session; only the file bytes of the declaration were read.

## §6 Proposed SOURCES row for L1 (id reserved; `S0xx-pending`)

| field | proposed value |
|---|---|
| id | `S0xx-pending` (L1 assigns from S072-S099) |
| source | swaybg man-page source — https://raw.githubusercontent.com/swaywm/swaybg/v1.2.2/swaybg.1.scd (tag page: https://github.com/swaywm/swaybg/blob/v1.2.2/swaybg.1.scd) |
| kind | code |
| tier | A |
| scope | swaybg(1) CLI appearance surface and layer-surface constant at tag v1.2.2 |
| anchor | `swaybg.1.scd:9-38`; `main.c:488-577`, `:308-319`, `:453-474` @ tag v1.2.2, commit `a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2`; sha256 `swaybg.1.scd 68ed5503…`, `main.c ff93e60c…`; receipts `.ufo/waves/round-18/fetch/MadoR18.SrcSwaybgMan/receipts.jsonl` |
| teaches | `-i <path>` sets the image with no path expansion; `-m` accepts exactly stretch/fill/fit/center/tile/solid_color with default stretch only when an image exists and solid_color otherwise; `-o` scopes appearance options per output with `*` for all; per-output blocks merge; the layer namespace is the constant `wallpaper` — so a declared argv names intent, not a guaranteed effect |
| status | mined |
| opened | 2026-10-20 |
| recheck | on-release |
| used-by | corpus/knowledge/theme-route-r18.md |

Row-level caveat to keep in the note: the tag's source never proves the host
binary (`[UNK]` version), and the man-page text is the scdoc source, not the
host's installed page.

## §7 Remaining unknowns (this seat)

1. Host swaybg version / package release — `[UNK]`, no query permitted.
2. Host binary build options (gdk-pixbuf, version-string shape) — `[UNK]`.
3. Host's installed `swaybg(1)` page vs v1.2.2 source — `[UNK]` (not read;
   would require reading package-owned files, outside this seat's assignment).
4. Whether the live session expands `~` in the declared `-i` argument —
   `[UNK]`; launcher behaviour, not swaybg's.
5. `-o` name validation and multi-output behaviour on the host — `[UNK]`; only
   source-level semantics are established.

Nothing here is a claim about observed host behaviour; §2-§3 are upstream
document/source facts, §4 is a file-byte declaration.
