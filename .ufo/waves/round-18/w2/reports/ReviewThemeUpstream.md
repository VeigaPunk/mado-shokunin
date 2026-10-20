# ReviewThemeUpstream — P5 `theme-route-r18.md` § Upstream contract spot-check (round 18, w2 FALSIFY)

- **Lane**: `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Target**: `corpus/knowledge/theme-route-r18.md` at `4c103b55b1ea5c3c555884afe3eb69b5189701b7`
  (baseline `d9a5a18`). Blob `49d2231fe66d5aaf62c5d16aeebfeb9d7a72d7c9`, sha256
  `b080bc479be42644cd3d2cf2cc5f4bdd44651cf137b1ee085353f23334a19f23`, 17,717 bytes, 145 lines;
  worktree identical (`git diff 4c103b5 -- corpus/knowledge/theme-route-r18.md` empty).
- **Scope**: the tag-selection paragraph and `## Upstream contract` (doc lines 32–72): omarchy
  v3.8.4 `omarchy-theme-set` / `-bg-next` / `-bg-set` / `-set-templates` / `default/hypr/autostart.conf`
  (S093), the matte-black payload (S094), and swaybg v1.2.2 (S092). Nothing else in the note.
- **Method**: independent `curl -sSL --max-time 60` re-fetch of all 10 tag-pinned raw bodies plus
  `default/themed` tree, `btop.theme.tpl` and the two `[OM]` tree pages; each fetch receipted under
  `.ufo/waves/round-18/fetch/ReviewThemeUpstream/receipts.jsonl` (schema `mado-fetch-receipt-v1`,
  body + sha256 + byte count + UTC time + tool). Digests compared 1:1 with the note author's
  `.ufo/waves/round-18/fetch/NoteTheme/receipts.jsonl`: **10/10 MATCH** on the raw files, byte counts
  equal. The two `[OM]` tree pages are the exception: they re-fetch to different bytes on every
  request (F6), so only their name lists could be compared; those reproduce exactly.
  Tag commits by `git ls-remote --tags` (read-only, outside the checkout). Host bytes read with
  `cat/grep/sha256sum/stat` only (`ORIG_HEAD`, `packed-refs`, the four scripts + autostart,
  `/var/log/pacman.log`). No `omarchy*`, `swaybg`, `pkill`, `pgrep`, `hyprctl`, `pacman`,
  `systemctl`, socket, screenshot or live probe; no write of any kind in the lane except this
  report and my fetch dir. **Installs: none.**
- **Verdict**: **no anchored claim in § Upstream contract is false.** 45 checks (4 tag-selection,
  41 anchored): 40 exact, 5 caveated — F2 (mechanism wording) and F3 (anchor range) low, F4/F5
  informational, F6 (tree-page digest instability) a reproducibility defect.
  Every quoted line fragment was found at the cited
  line and nowhere displaced. One real documentation defect (a front-matter pointer that does not
  resolve, F1), one reproducibility defect (F6), two low-severity precision issues (F2, F3), two
  informational notes (F4, F5). **C2 is not falsified by this section**: its claims reproduce
  against independently fetched tag bytes — every raw file exactly, the `[OM]` name lists exactly,
  the two `[OM]` page digests not at all (F6) — and the raw-file recheck path the note documents
  works.

## Claim-by-claim (every `[OT]/[OB]/[OS]/[OP]/[OA]/[OM]/[SW]/[SR]/[SM]/[SB]` citation, lines 32–72)

Legend: **exact** = the cited line(s) state what the sentence says; **exact\*** = claim true but
anchor/wording imprecise (see finding); **info** = true and classed as an observation.

| # | anchor | assertion in the note | body evidence (independent fetch) | result |
|---|---|---|---|---|
| T1 | Tag selection | `ORIG_HEAD` and `packed-refs` both name `8fcc9d60…` for `refs/heads/master` and `refs/tags/v3.8.4` | `ORIG_HEAD` = `8fcc9d6048af…`; `packed-refs:2` = master, `:508` = tag, both `8fcc9d60…`; `HEAD` = `ref: refs/heads/master` | exact |
| T2 | Tag selection | omarchy `v3.8.4` tag commit = `8fcc9d6048af…` | `git ls-remote --tags basecamp/omarchy` → `8fcc9d60… refs/tags/v3.8.4` (lightweight, no `^{}` line) | exact |
| T3 | Tag selection | swaybg `v1.2.2` is the tag matching the host package | `/var/log/pacman.log:1158` `installed swaybg (1.2.2-1)`; `grep -c swaybg` = 2, lines 484 + 1158 | exact |
| T4 | Tag selection / SW row | swaybg tag commit `a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2`, peeled | `ls-remote` → tag object `3ca0f88f…`, peeled commit `a59ea3db…` | exact |
| 1 | `[OT:17]` | name: HTML tags stripped, lowercased, spaces→hyphens | `sed -E 's/<[^>]+>//g' \| tr '[:upper:]' '[:lower:]' \| tr ' ' '-'` | exact |
| 2 | `[OT:19-22]` | refuses a name with neither `themes/<name>` nor `~/.config/omarchy/themes/<name>` | `if [[ ! -d $OMARCHY_THEMES_PATH/$THEME_NAME ]] && [[ ! -d $USER_THEMES_PATH/$THEME_NAME ]]; then … exit 1` | exact |
| 3 | `[OT:29-30]` | official payload copied first, then user overrides, into `current/next-theme` | `cp -r "$OMARCHY_THEMES_PATH/$THEME_NAME/"* …` then `cp -r "$USER_THEMES_PATH/$THEME_NAME/"* …` | exact |
| 4 | `[OT:38]` | templates run before the swap | line 38 `omarchy-theme-set-templates`; swap at 41–42 | exact |
| 5 | `[OT:41-42]` | `current/theme` removed, `next-theme` moved in | `rm -rf "$CURRENT_THEME_PATH"` / `mv "$NEXT_THEME_PATH" "$CURRENT_THEME_PATH"` | exact |
| 6 | `[OT:45]` | writes `current/theme.name` | `echo "$THEME_NAME" >"$HOME/.config/omarchy/current/theme.name"` | exact |
| 7 | `[OT:48-50]` | calls bg-next unless `OMARCHY_THEME_SKIP_BACKGROUND=1`; swaybg relaunched inside the writer, not the restart list | `if [[ $OMARCHY_THEME_SKIP_BACKGROUND != "1" ]]; then omarchy-theme-bg-next; fi`; 53–62 has no swaybg | exact |
| 8 | `[OT:53-62]` | restarts waybar (only when running), swayosd, terminal, hyprctl, btop, opencode, mako, helix; swaybg absent | `if pgrep -x waybar …` + the seven `omarchy-restart-*` lines 56–62 | exact |
| 9 | `[OT:65-70]` | app setters foot, gnome, browser, vscode, obsidian, keyboard | six `omarchy-theme-set-*` calls, lines 65–70 in that order | exact |
| 10 | `[OT:73]` | calls the `theme-set` hook | `omarchy-hook theme-set "$THEME_NAME" >/dev/null` | exact |
| 11 | `[OB:6]` | theme name read from `current/theme.name` | `THEME_NAME=$(cat "$HOME/.config/omarchy/current/theme.name" 2>/dev/null)` | exact |
| 12 | `[OB:7-9]` | backgrounds from `~/.config/omarchy/backgrounds/<name>/` and `current/theme/backgrounds/` | the two `*_BACKGROUNDS_PATH` assignments (7–8) plus the link (9) | exact |
| 13 | `[OB:11]` | `find -L … -maxdepth 1 -type f`, NUL-safe sorted | `find -L "$USER_BACKGROUNDS_PATH" "$THEME_BACKGROUNDS_PATH" -maxdepth 1 -type f -print0 \| sort -z`, `mapfile -d ''` | exact |
| 14 | `[OB:14-17]` | zero backgrounds → `swaybg --color '#000000'` | line 17 `setsid uwsm-app -- swaybg --color '#000000'` (15–16 also `notify-send` + `pkill -x swaybg`, elided but not contradicted) | exact |
| 15 | `[OB:41]` | next entry with wrap-around | `NEXT_INDEX=$(((INDEX + 1) % TOTAL))` | exact |
| 16 | `[OB:46]` | `ln -nsf "$NEW_BACKGROUND" "$CURRENT_BACKGROUND_LINK"` | identical line 46 | exact |
| 17 | `[OB:49-50]` | `pkill -x swaybg` then `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill`; argument is the link | identical lines 49–50 | exact |
| 18 | `[OS:12]` | resolves argument with `realpath` | `BACKGROUND="$(realpath "$1")"` | exact |
| 19 | `[OS:21]` | sets link with `ln -nsf` | identical line 21 | exact |
| 20 | `[OS:24-25]` | relaunches swaybg on the link with `-m fill` | `pkill -x swaybg` / `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill` | exact |
| 21 | `[OS]` prose | second writer of the same link; does not touch `theme.name` | file has no `theme.name` reference; link is the same path as `[OB:9]` | exact |
| 22 | `[OP:6]` | built-in templates from `$OMARCHY_PATH/default/themed` | `TEMPLATES_DIR="$OMARCHY_PATH/default/themed"` | exact |
| 23 | `[OP:38]` | user `*.tpl` first, then built-in `*.tpl` | `for tpl in "$USER_TEMPLATES_DIR"/*.tpl "$TEMPLATES_DIR"/*.tpl` | exact |
| 24 | `[OP:43]` | render only when no output of that name exists in `next-theme`; payload beats template | `if [[ ! -f $output_path ]]` inside the loop; payload copied at `[OT:29-30]` before line 38 | exact\* (F4) |
| 25 | `[OP:43]` + prose | `btop.theme` (payload) beats `btop.theme.tpl` (template) | `default/themed` tree has `btop.theme.tpl`; raw fetch 200, 2,480 B; payload `btop.theme` is in the `[OM]` tree | exact |
| 26 | `[OA:5]` | `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill` | identical line 5 | exact |
| 27 | `[OA:5]` prose | retargeting the link changes the wallpaper without editing config | swaybg opens the path only when loading (`[SM:658-663]`; first load from `buffer_change` at 651–653); bg-next/bg-set relaunch after `ln -nsf` (`[OB:49-50]`, `[OS:24-25]`) | exact\* (F2) |
| 28 | `[OM]` | eight files: `btop.theme`, `colors.toml`, `icons.theme`, `neovim.lua`, `preview.png`, `preview-unlock.png`, `unlock.png`, `vscode.json` + `backgrounds/` | `"path":"themes/matte-black/…"` extraction: exactly those 8 plus `backgrounds` | exact |
| 29 | `[OM]` | backgrounds tree: `0-ship-at-sea.jpg`, `1-dark-waters.jpg`, `2-dot-hands.jpg`, `omarchy.png` | extraction of `themes/matte-black/backgrounds/*`: exactly those 4 | exact |
| 30 | `[OM]` | tree page SHA-256 `50c1ac25…` (theme), `9e1160a0…` (backgrounds) | these match the author's stored bodies and committed receipt lines; a fresh fetch differs on every request (F6). Three fetches of the theme URL in 5 min: `d0a92070…`/229,022 B, `30d3dc72…`/229,027 B, `de57cbaf…`/229,036 B; path lists identical | exact\* (F6) |
| 31 | `[OM]` | `colors.toml` 461 B, sha256 `dbdd13a6…` | 461 B, `dbdd13a629aac86d…ad03b66429d9e4b3…5601786` reproduced on re-fetch | exact |
| 32 | `[SW:19-31]` | `-c` colour, `-i` image, `-m` modes stretch/fill/fit/center/tile, default stretch, `solid_color` colour-only | man page 19–20, 25–26, 28–31 (`Default is _stretch_`; `solid_color` shows colour only) | exact |
| 33 | `[SW:19-31]` prose | per-output options via `-o` | `-o` is documented at 33–35, outside the cited range | exact\* (F3) |
| 34 | `[SM:521-529]` | parses `-i` into image path, `-m` into mode, logs invalid mode | 521 `case 'i'` → 522 `config->image_path = optarg`; 524 `case 'm'` → 526–528 `Invalid mode` log | exact |
| 35 | `[SM:575-577]` | image without `-m` defaults to stretch | `config->mode = config->image_path ? BACKGROUND_MODE_STRETCH : BACKGROUND_MODE_SOLID_COLOR` | exact |
| 36 | `[SM:658-663]` | loads each distinct image path in the render loop | loop 658–663 `if (!image->load_required) continue; … load_background_image(image->path)`; dedupe at 592–612 | exact\* (F5) |
| 37 | `[SB:24-46]` | opens with `gdk_pixbuf_new_from_file` (or `cairo_image_surface_create_from_png`), logs failure | 28 gdk-pixbuf, 41 cairo PNG fallback under `#else`; logs at 30–31, 43–45 | exact |
| 38 | `[SB:24-46]` prose | path opened as given; symlink resolves at open | `load_background_image(const char *path)` → `gdk_pixbuf_new_from_file(path, …)`; no `realpath`/`readlink` in the function | exact |
| 39 | `[SR:3-5]` | wallpaper utility for wlr-layer-shell + `wl_output` v4 | README 3–5 verbatim | exact |
| 40 | anchor table | URLs are the files actually fetched; `[OM]` final URL under `omacom/omarchy` | all 10 raw fetches 200 at the listed paths with matching bytes; tree page `final_url` = `github.com/omacom/omarchy/…` | exact |
| 41 | `[OT:29-30]` nuance | "official theme payload" is per-theme content copy | line 15 `OMARCHY_THEMES_PATH="$OMARCHY_PATH/themes"`; `themes/<name>` shorthand is the checkout root | exact |

Tree-page **names** reproduce on fresh fetches: the two re-fetched pages yield exactly the eight
files and four background files above. Tree-page **digests** do not reproduce: the committed
`NoteTheme` lines record `50c1ac253df17986…` (229,027 B) and `9e1160a06501b0b7…` (218,578 B), while
four fresh fetches of the theme page and one of the backgrounds page produced a different byte
stream each time (theme: 229,022 / 229,027 / 229,036 / 229,036 B, four distinct digests;
backgrounds: 218,588 B). The diff is in `github.githubassets.com/assets/*.js` bundle hashes and
similar per-request page furniture. See F6.

## Findings

### F1 — MEDIUM (documentation, identity pointer): front-matter sends a closure to a section that has no raw digests

Doc line 1 (`source:`) says for S092: "swaybg v1.2.2 tag: … raw SHA-256 in § Upstream contract".
§ Upstream contract (lines 38–72) contains **no** raw SHA-256 for `swaybg.1.scd`, `README.md`,
`main.c` or `background-image.c`; the only digests there are the two tree-page hashes (line 64) and
`colors.toml` (line 65).

- Input: `git show 4c103b5:corpus/knowledge/theme-route-r18.md | grep -nE 'sha256|SHA-256'` →
  hits on lines 1, 2, 3, 64, 65, 76, 80, 96, 127 only; of those, only 64 (tree pages) and 65
  (`colors.toml`) fall inside § Upstream contract (38–72).
- Expected per the pointer: a raw-digest block inside § Upstream contract (lines 38–72).
- Got: no digest between lines 38 and 72 except the tree-page and `colors.toml` values; the four
  S092 file digests appear only in `corpus/SOURCES.md` row S092 and
  `.ufo/waves/round-18/drafts/NoteTheme-rows.md`.
- Consequence: a closure following the note's own pointer cannot perform the line-2 recheck from the
  section it is sent to; it must fall through to the receipts. Not invented content — all four
  digests reproduce on independent fetch (see #32–#39): `68ed5503…`, `a6720ded…`, `ff93e60c…`,
  `9aea12fc…`.
- Minimal fix (one line): replace "raw SHA-256 in § Upstream contract" with "raw SHA-256 in
  `corpus/SOURCES.md` S092 / the fetch receipts".

### F2 — LOW (mechanism wording): link retarget alone does not repaint a running swaybg

Doc line 60: "The declaration names the link; retargeting the link changes the wallpaper without
editing config."

- Source: swaybg resolves the path only at load — `[SM:658-663]` calls
  `load_background_image(image->path)` inside the dispatch loop; the initial load is forced by
  `buffer_change` at 651–653; there is no file watch or `readlink`/re-load on symlink change in
  `main.c`. Both writers therefore `pkill -x swaybg` and relaunch after `ln -nsf`
  (`[OB:49-50]`, `[OS:24-25]`).
- Expected wording: "a newly launched swaybg opens the link; omarchy relaunches swaybg after
  retargeting". The note's `[UNK]` ("Whether the running swaybg re-reads the retargeted link") already
  concedes the gap, but the § Upstream contract sentence stands on its own and reads as a live
  repaint.
- Impact: none on the config-level claim (the image path is the link, not a theme file); could
  mislead an operator into expecting an instant wallpaper change after retargeting the link.

### F3 — LOW (anchor coverage): the `-o` sentence is outside `[SW:19-31]`

Doc line 69 cites `[SW:19-31]` for a sentence whose last clause is "Per-output options exist via
`-o`". `-o` is documented at `swaybg.1.scd:33-35`; the cited range ends at line 31 (the `-m`
description). The claim is true; the anchor is short. Fix: cite `[SW:19-35]`, or add `[SW:33-35]`
to the `-o` clause. No other `[SW]` clause overreaches: `-c` 19–20, `-i` 25–26, `-m` 28–31 all sit
inside the range.

### F4 — INFO (omitted precondition): the template rule is gated on `next-theme/colors.toml`

Doc line 56 states the `[OP:43]` no-overwrite rule without the enclosing `[OP:18]`
`if [[ -f $COLORS_FILE ]]`: the entire render loop is skipped when the theme has no `colors.toml`.
The sentence is still true as a necessary condition, the payload-wins conclusion holds for
matte-black, and the count arithmetic in § Payload versus rendered is unaffected (matte-black ships
`colors.toml`). Corroborated: `default/themed` lists exactly 17 `.tpl` files and includes
`btop.theme.tpl` (raw 200, 2,480 B), so 8 + 17 − 1 = 24 is arithmetically sound. Suggested fix:
add `[OP:18]` to the citation.

### F5 — INFO (anchor precision): "distinct" comes from the dedupe block, not from 658–663

Doc line 71: "`[SM:658-663]` loads each distinct image path in the render loop." The distinctness
is established at `[SM:592-612]` (`strcmp` match against `state.images`, `calloc` only on miss);
658–663 is the load loop. Fix: `[SM:592-612,658-663]`. No truth issue.

### F6 — MEDIUM (reproducibility): the `[OM]` tree-page SHA-256 pins are per-fetch and do not reproduce

Doc line 64 pins "Tree page SHA-256: 50c1ac25… (theme) and 9e1160a0… (backgrounds)", and the
`recheck:` line tells a closure to "re-fetch the tag-pinned raw URLs … and compare SHA-256 with the
receipts". The tree pages fail that check by construction: GitHub serves a fresh HTML shell whose
`github.githubassets.com/assets/*.js` bundle hashes rotate between requests.

- Input: `curl -sSL --max-time 60 -o B https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black`,
  four times within five minutes.
- Expected if the cited digest were a content pin: constant bytes (the author's 229,027 B /
  `50c1ac25…`).
- Got: `d0a92070…`/229,022 B, `30d3dc72…`/229,027 B, `de57cbaf…`/229,036 B, `74ca97c2…`/229,036 B.
  `diff` against the committed body shows changed `assets/environment-*.js`, `github-elements-*.js`,
  `behaviors-*.js` and similar page furniture. The backgrounds page likewise re-fetched at
  218,588 B / `369f9439…` against the committed 218,578 B / `9e1160a0…`.
- What is stable: the `"path"` name lists — exactly the eight files and four backgrounds claimed
  (rows 28–29), extracted identically from fresh fetches. `colors.toml` (row 31) is a raw file and
  reproduces byte-for-byte.
- Consequence: the round's own Gate rejects "HTML pages as sole support (per-fetch tokens make the
  digest irreproducible)" and the anchor table marks `[OM]` "names only" — S094 is not sole-support
  (raw `colors.toml` is), but line 64 still presents page digests as if they were pins, and the S094
  `SOURCES` row records the same two digests as anchor text. A closure that takes them as pins gets
  a false mismatch on every attempt. Fix: mark the two digests as per-fetch observations (or drop
  them) and keep the name lists as the verifiable artifact. This is the R17-V2 shape (a cited
  number that does not reproduce), not invented content: the names and the raw `colors.toml` are
  real and reproduce.

## Commands run (all outputs reproduced)

```
# independent re-fetch, 10 bodies
curl -sSL --max-time 60 -o <slug> -w '%{http_code} %{url_effective}' <raw url at tag>
→ all 200; bytes/sha equal to NoteTheme receipts 1:1 (10 MATCH)
   omarchy-theme-set 2147 79069c8018a7d6d2…
   omarchy-theme-bg-next 1650 ee4828127755566d…
   omarchy-theme-bg-set 671 638f265f3a8e62e4…
   omarchy-theme-set-templates 1728 01264122666b3d49…
   default/hypr/autostart.conf 742 acb6a66862033edd…
   swaybg.1.scd 1124 68ed5503298fc845…   README.md 1026 a6720ded1ad3dcd0…
   main.c 21390 ff93e60c00f9b1b9…   background-image.c 3993 9aea12fc179f7223…
   themes/matte-black/colors.toml 461 dbdd13a629aac86d…

# tag commits
git ls-remote --tags https://github.com/basecamp/omarchy | grep v3.8.4
   8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
git ls-remote --tags https://github.com/swaywm/swaybg | grep v1.2.2
   3ca0f88fee1a0c83f26ffe2341207d84c7243e7a	refs/tags/v1.2.2
   a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2	refs/tags/v1.2.2^{}

# host tag selection and script identity
cat ~/.local/share/omarchy/.git/ORIG_HEAD        → 8fcc9d6048af4cb0e3af8512c78049857a3b53dd
grep -nE 'refs/(heads/master|tags/v3\.8\.4)$' ~/.local/share/omarchy/.git/packed-refs
  2:8fcc9d60… refs/heads/master
  508:8fcc9d60… refs/tags/v3.8.4
sha256sum ~/.local/share/omarchy/bin/omarchy-theme-set{,-bg-next,-bg-set,-set-templates} \
          ~/.local/share/omarchy/default/hypr/autostart.conf
  → 79069c80…, ee482812…, 638f265f…, 01264122…, acb6a668…  (all = tag bodies)

# host package line for the SW version premise
grep -c swaybg /var/log/pacman.log                      → 2
grep -n swaybg /var/log/pacman.log                      → :484 install cmdline, :1158 installed swaybg (1.2.2-1)

# tree listings (exact path extraction from the fetched HTML)
grep -oE '"path":"themes/matte-black[^"]*"'     ...tree.html → 8 files + backgrounds
grep -oE '"path":"themes/matte-black/backgrounds[^"]*"' ... → 4 jpg/png
grep -oE '"path":"default/themed/[^"]*"' ...default-themed-tree.html → 17 .tpl, incl. btop.theme.tpl
curl -o omarchy-btop-theme-tpl.bin .../v3.8.4/default/themed/btop.theme.tpl → 200, 2480 B

# tree-page digest stability (same URL, four fetches within five minutes) — F6
curl .../tree/v3.8.4/themes/matte-black
  → d0a92070… 229022 ; 30d3dc72… 229027 ; de57cbaf… 229036 ; 74ca97c2… 229036
diff committed body vs fresh body → changed assets/{environment,github-elements,behaviors}-*.js;
  the '"path"' list is identical
curl .../tree/v3.8.4/themes/matte-black/backgrounds
  → 369f9439… 218588   (committed receipt: 9e1160a0… 218578)

# pointer check for F1
git show 4c103b5:corpus/knowledge/theme-route-r18.md | grep -nE 'sha256|SHA-256'
  → 1, 2, 3, 64, 65, 76, 80, 96, 127; inside 38–72 only 64 (tree pages) and 65 (colors.toml)
```

Committed receipt identity: `git show 4c103b5:.ufo/…/fetch/NoteTheme/receipts.jsonl | sha256sum`
= `ed9ce52fbce86754129260a97d379251935184762dc52e4c59d77a9f4274027c` = the worktree copy
(17 lines, unchanged since integration).

## Residual risk and verification gaps

- **Body files are not committed.** `git ls-tree -r 4c103b5 -- .ufo/waves/round-18/fetch/` shows
  exactly one file per seat — `receipts.jsonl` — so a closure cannot compare body bytes offline; it
  must re-fetch (the method the receipts' `url` and the note's `recheck:` line prescribe). That path
  works for every raw file: my 10 independent re-fetches reproduce each digest and size. If C2's
  "body bytes" is read as *committed bodies*, that reading fails; read as *receipt records body
  identity, size and digest*, it holds. The two `[OM]` tree-page receipt digests are not
  re-verifiable at all (F6); for S094 the stable evidence is the raw `colors.toml` plus the name
  list, both of which reproduce.
- **No live observation** (host pause): no swaybg process, argv, layer surface, theme set, consumer
  reload or output scaling. The note's § Unexercised behavior lists the same gaps honestly; I
  exercised none of them and confirm none.
- **Out of this item's scope**: § Host declaration consumer pins, the 16 rendered files and the
  1.68 MB background (S095/host rows), the `[OM]` page-name claims beyond the two tree pages, and
  the rubric V instrument (C2's 6/6 is not adjudicated here beyond "this section is backed").
- **Not re-derived**: the 17 rendered files' bytes (inferred from templates + `colors.toml` by the
  note itself), and swaybg's behaviour on a live retarget (F2 stays a source-level statement; the
  note's `[UNK]` remains correct).
- **No installs or upgrades** were performed; no tool version changed this item.

Report: .ufo/waves/round-18/w2/reports/ReviewThemeUpstream.md
