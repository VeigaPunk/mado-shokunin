# ReviewThemeUnknowns — round 18 wave 2 (falsify)

Seat `MadoR18.ReviewThemeUnknowns` (leaf; no dispatch). Date 2026-10-20.
Target: `corpus/knowledge/theme-route-r18.md` at
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`. Working tree equals the commit:
`sha256sum` and `git show 4c103b55…:<path> | sha256sum` both
`b080bc479be42644cd3d2cf2cc5f4bdd44651cf137b1ee085353f23334a19f23`.
Comparison note `corpus/knowledge/theme-wallpaper-plane.md` both
`8c578cc70e36506d75d8fde8904c1493203b802bef4b173d441b8d1b1289a004`
(committed and working tree agree).

Scope: the note's last two sections — `## Safe observation` (:123-132) and
`## Unexercised behavior` (:134-145) — the "no runtime claims" property of the
note as a whole, and consistency with `theme-wallpaper-plane.md` §1–§4 and §11.
All line numbers below are the committed blob's. Host files were read as bytes
only (`sha256sum`, `stat`, `readlink`, `cat`, `sed -n`, `find`, `grep`);
committed fetch bodies were re-hashed, no new fetch was made and no fetch
receipt added. No package/service/compositor/process/REA operation; no lane VCS
write, no jj command, no `git status`. No tool install or update (none needed).

Axes (godspeed): **A1** label honesty (`[UNK]`/`[INF]` vs the bytes actually
available); **A2** completeness of the unexercised set for the four named
runtime areas (runtime application, swaybg process, reload effects,
non-atomic swap); **A3** consistency with `theme-wallpaper-plane.md`;
**A4** operability of the recheck recipe.

## Verdict

- Of the four named areas, three are present in § Unexercised behavior:
  swaybg process (:136), reload effects (:137, :139), runtime application only
  as consumer/render questions (:139, :140). **The non-atomic swap is absent**
  (F2). The write-side runtime-application question is answered instead by an
  unmarked assertion outside the section — "`current/next-theme` is absent
  (the swap completed)" (:87) (F1).
- **Consistency with `theme-wallpaper-plane.md` passes** on every pin, count,
  symlink, consumer line, version and symlink/count claim I re-read; no
  contradiction found (§ Consistency below). The note's "no contradiction"
  sentence (:121) is supported.
- No rubric-V count change follows from these findings. They are label,
  completeness and operability defects, not counterexamples to the pinned
  bytes.

## Findings

### F1 — high — unmarked runtime claim: "the swap completed" (:87)

`:87` reads:

> `current/next-theme` is absent (the swap completed). …

The parenthetical asserts a **past execution** of `omarchy-theme-set` through
the two-syscall swap at `[OT:41-42]`. Nothing measured in the note supports
that event uniquely:

- `next-theme` is created at `[OT:25-26]` and moved at `[OT:42]`. Absence of
  `next-theme` with `current/theme` present is also produced by (a) no run at
  all, (b) a run that exited at the name check `[OT:19-22]` before the staging
  dir was re-created, (c) an older writer without the staging dir, (d) manual
  removal. Only the kill-between-:41-and-:42 state is excluded by the presence
  of `current/theme` — and that state is exactly the non-atomic case F2 says is
  unlisted.
- The note's own header promises "Documentary route only. … no theme set was
  run … Unobserved behaviour is listed in § Unexercised behavior." The section
  contains no such bullet.
- The note marks the *same* inference correctly at `:138`: "inferred from the
  mtimes at 2026-10-03 17:49:02 `[INF]`". Same event, two labels.

What actually supports the inference (measured this review, not yet used by
the note): the write order is strictly increasing — 28 files under
`current/theme/` span `17:49:02.541927`–`.614233`, `theme.name` `.617593`,
`background` link `.620234` (−0300). That is the order of `[OT:29-30]` copy →
`[OT:41-42]` swap → `[OT:45]` name → `[OT:48-50]` bg-next. It remains
`[INF]`, not `[OBS]`.

Fix: delete the parenthetical, or replace it with
"`[INF]` mtime order: theme files < theme.name < background link, consistent
with [OT:29-45] but not proof", and add an `[UNK]` bullet for whether the
writer ran to completion with default environment.

### F2 — high — non-atomic swap absent from § Unexercised behavior ([OT:41-42]; :134-145)

The section's own charter is to list unobserved behaviour; the swap's
consequences are not listed anywhere. The upstream body (committed fetch body
`omarchy-theme-set-v3.8.4.sh`, sha256 `79069c80…9516`, matching the receipt and
`:120`) is:

- `:24` `# Setup clean next theme directory (for atomic theme config swapping)`
- `:41` `rm -rf "$CURRENT_THEME_PATH"`
- `:42` `mv "$NEXT_THEME_PATH" "$CURRENT_THEME_PATH"`

The comment at `:24` describes staging intent; the swap itself is two syscalls
and is not atomic to a concurrent reader. Consequences that belong in
§ Unexercised behavior, all unlisted:

1. **Window.** Between `:41` and `:42`, `current/theme` does not exist. On this
   host `current/background` is an absolute symlink to
   `current/theme/backgrounds/0-ship-at-sea.jpg` (`readlink`, 71 B), and
   `~/.config/hypr/hyprlock.conf:10` points at that link. Any consumer that
   opens the link or a `current/theme/...` path in the window sees a missing
   target. Whether any did, and how long the window lasts, is unobserved and
   must be `[UNK]` (no duration is claimed; the window is not measured).
2. **Interrupted run.** Killed between `:41` and `:42` the host is left with
   `next-theme` present, no `current/theme`, a stale `theme.name` (written
   later, at `:45`), and a dangling `current/background`. That is the inverse
   of the state F1 reads as completion; the note never distinguishes them.
3. **Name/dir non-atomicity.** `theme.name` is written at `:45`, after the
   swap, and read by the background writer at `[OB:6]`; name and tree are not
   updated together.
4. **Drift check.** The recheck recipe at `:127` reads several paths without a
   shared snapshot, so a concurrent theme set can make it report drift that is
   the window, not a host change.

Fix: add 2–3 `[UNK]` bullets covering the window, the interrupted-run state and
whether a consumer can observe either; mention that `:24`'s "atomic" is a
staging comment, not an atomicity property of `:41-42`.

### F3 — minor — the reload bullet under-claims what the fetched `main.c` already pins (:137)

`:137` says "the full `main.c` was not traced for re-load on output change".
The receipt body (`swaybg-v1.2.2-main.c`, sha256 `ff93e60c…a805`, 21,390 B) does
pin the mechanism:

- `:646-653` `if (output->dirty) { … if (output->config->image && buffer_change)
  { output->config->image->load_required = true; } }`
- `:658-663` the render loop calls `load_background_image(image->path)` when
  `load_required`; the path is re-opened, so a symlink is resolved at that
  moment.

So: no file watch — a `ln -nsf` retarget alone cannot reload a running swaybg;
a buffer-size change reloads from the same path. The remaining host unknown is
only whether a buffer change occurs (the writer path kills and relaunches
anyway, `[OB:49-50]`). This is an under-claim, not an error; narrowing the
bullet would make the section more informative.

### F4 — minor — the § Safe observation drift recipe does not run as written (:127-128)

`:128` prescribes `grep -n -E 'current/(theme|background)'` "on" directories,
"excluding `*.bak*` copies". Measured with an equivalent directory argument:

```
mkdir /tmp/grepform.atk; printf 'x\n' > /tmp/grepform.atk/a
grep -n -E 'current/(theme|background)' /tmp/grepform.atk
grep: /tmp/grepform.atk: Is a directory
rc=2
```

The form needs `-r` (`grep -Rn`) and `--exclude='*.bak*'`; as written it neither
recurses nor excludes. `:127`'s "re-run to detect drift" is otherwise sound but
reads multiple entries non-atomically (see F2 item 4). Note the note does
correctly exclude `.bak*` in prose (:76), so this is a recipe bug, not a
conceptual one.

### F5 — minor — "3440×1440 output" is an unanchored display premise (:140)

`:140` says swaybg `-m fill` scaling is unknown "on the 3440×1440 output". The
figure has no anchor in this note. It is declared at
`~/.config/hypr/monitors.conf:10`
(`monitor = DP-1, 3440x1440@100, 0x0, 1`) and was live-probed in round 7
(`theme-wallpaper-plane.md` §3 item 3, `hyprctl -j layers`, geometry
`3440x1440`). As written inside an `[UNK]` bullet it reads as current runtime
fact. Fix: cite `monitors.conf:10` as declaration and/or the round-7 probe as
observation, or drop the number.

### F6 — minor — two cross-reference defects (:136, :87)

- `:136` cites "`theme-wallpaper-plane.md` §3.3". That note has no §3.3;
  `grep -n '3\.3'` matches only this line across both notes. Its §3 has four
  numbered items, the third ("Live", `:157-163`) being the PID/geometry probe.
  Use "§3 item 3 ('Live')".
- `:87` says the hook directory's sample "the hook runner skips" with no local
  anchor. The source (`bin/omarchy-hook:25`) is inherited from
  `theme-wallpaper-plane.md` §4.2 and was not re-read this round; cite that
  anchor.

### F7 — out of scope (seen while checking consistency; route to L1) — S092 digest pointer

`:1` claims S092's "raw SHA-256 in § Upstream contract". None of the four
swaybg digests appears in the note:
`grep -c 'ff93e60c\|68ed5503\|a6720ded\|9aea12fc' corpus/knowledge/theme-route-r18.md`
→ `0`. They live in `.ufo/waves/round-18/drafts/NoteTheme-rows.md:16` and in
the receipts. A closure following only the note cannot re-verify S092's raw
bytes; point at the draft/receipts. (Not a claim in the last two sections;
recorded because this review re-hashed those bodies.)

## Consistency with `theme-wallpaper-plane.md` — pass

All checks below are host-byte or committed-body reads at 2026-10-20; the
comparison note is `8c578cc7…`.

| Check | Route note | Measured | Verdict |
|---|---|---|---|
| `theme.name` | 12 B, `matte-black`, `48749715…` | 12 B, `matte-black`, `48749715228bfa…` | agree |
| `current/background` | 71 B symlink → `…/theme/backgrounds/0-ship-at-sea.jpg` | same, target 1,681,677 B, `55fa691a…` | agree |
| theme tree count | 24 files + 4 backgrounds | `find … -maxdepth 1 -type f` → 24; backgrounds → 4 | agree |
| eight ★ pins | waybar `a1807a17…`, swayosd `f88118e9…`, walker `f44cb450…`, hyprlock `3ef010e7…`, hyprland `79126bec…`, alacritty `8c3d1457…`, mako `95bf0c86…`, colors `dbdd13a6…` | all eight re-hash identical (`sha256sum`) | agree |
| btop pin | `e9ee6fb6…` | identical | agree |
| symlinks | mako config → `current/theme/mako.ini`; btop `current.theme` → `current/theme/btop.theme`; nvim relative symlink | `readlink` prints exactly those targets | agree |
| consumer lines | hyprland `:4`, `:13`; hyprlock `:1`, path `:10`; waybar `:1`; swayosd `:1`; alacritty `:1`; walker `:3-4` + style `:1` | `sed -n` prints the declared lines | agree |
| consumer hashes | `ce7483f3…`, `5ace1701…`, `b8d173dc…`, `8f335ca0…`, `6e3ba08f…`, `695301c8…`, `fecf71fa…`+`481267af…`, `95bf0c86…`, `e9ee6fb6…` | all re-hash identical | agree |
| walker import depth | seven `../` reach `/home/vgpnk` | import has 7 `../` segments | agree |
| host omarchy scripts | `79069c80…`, `ee482812…`, `638f265f…`, `acb6a668…` = tag | host hashes equal the committed fetch bodies and receipts | agree |
| user autostart | no swaybg line; line 5 is the grok-bot exec | same; the 2026-10-13 `.bak` also has no swaybg line | agree |
| pacman.log | `:484`, `:1158`, no upgrade line | `grep -n swaybg` returns exactly 484 and 1158 | agree |
| payload host-to-host | seven files identical to `themes/matte-black/` | all seven `sha256sum` pairs identical | agree |
| tag tree | eight files + `backgrounds/`; tree pages `50c1ac25…`, `9e1160a0…`; colors `dbdd13a6…` | request bodies re-hash to the receipt digests; tree HTML lists the eight names and `backgrounds` | agree |
| template count | 17 built-in − 1 (`btop.theme`) + 8 payload = 24 | `default/themed` holds 17 `*.tpl`; theme holds 24 | agree |

The note's agreement sentence (:121) and its "round-7 live swaybg observation
is not repeated" are accurate. No contradiction found with plane note §1–§4 or
§11; the plane note's `[UNK]` set (§11.1–§11.4) maps onto route items :139 and
:36/:137 for the parts the route covers.

## What I could not falsify

- The pins, counts, consumer declarations, symlinks and version claims listed
  above reproduce exactly; none is overstated.
- The upstream semantics quoted in § Upstream contract match the committed
  bodies I re-read: `[OT:17,19-22,29-30,38,41-45,48-50,53-73]`,
  `[OB:6-17,41,46,49-50]`, `[OS:12,21,24-25]`, `[OP:6,38,43]`, `[OA:5]`,
  `[SW]`/`[SM]`/`[SB]` as cited.
- The `[UNK]` items about the running swaybg, consumer reloads, rendering,
  unrendered template bytes, payload tag-equality, packaging, the skip
  variable and the declared-only consumers are honest: each names a probe not
  performed, and I could not close any of them under the pause.

## Residual risk and verification gaps

- No runtime observation was possible under the pause. F1/F2 are label and
  coverage defects; whether a real theme set leaves the window open, and for
  how long, is untested and remains `[UNK]` after this review too.
- The note's "1 MiB fetch cap" (:142) is not stated in the round contract text
  this seat received; I did not test it. The substantive claim (the 1.68 MB
  JPEG was not fetched upstream, so tag byte-equality is unknown) is true.
- No LSP device is mounted in this session (not in the tool inventory) and a
  Markdown note has no semantic server here; all checks are byte/text reads,
  not semantic proof.
- The hook-runner skip (`omarchy-hook:25`) and the pre-round-7 history behind
  the uniform mtimes were not re-opened; the mtime ordering is evidence of a
  writer-shaped sequence, not proof of which process wrote it.

## Commands run (with output)

```
git -C . show 4c103b55…:corpus/knowledge/theme-route-r18.md | sha256sum
b080bc479be42644cd3d2cf2cc5f4bdd44651cf137b1ee085353f23334a19f23  -
sha256sum corpus/knowledge/theme-route-r18.md
b080bc479be42644cd3d2cf2cc5f4bdd44651cf137b1ee085353f23334a19f23  corpus/knowledge/theme-route-r18.md
# same equality for theme-wallpaper-plane.md: 8c578cc70e36…

sha256sum .config/omarchy/current/theme/{waybar,swayosd,walker}.css …   # 9 pins
a1807a17…, f88118e9…, f44cb450…, 3ef010e7…, 79126bec…, 8c3d1457…,
95bf0c86…, e9ee6fb6…, dbdd13a6…            # all equal to the note and plane §2.1
sha256sum .config/omarchy/current/theme.name
48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b
readlink .config/omarchy/current/background
/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
stat -c '%s %y %n' theme.name background
12 …17:49:02.617593239…; 71 …17:49:02.620233763…
find .config/omarchy/current/theme -type f | wc -l            -> 28 (24 + 4)
find .config/omarchy/current/theme -type f -printf '%T@ %p\n' | sort -n | sed -n '1p;$p'
1791060542.5419273580 …/backgrounds/0-ship-at-sea.jpg
1791060542.6142337620 …/waybar.css
test -e .config/omarchy/current/next-theme                     -> NEXT_ABSENT
test -d .config/omarchy/backgrounds                            -> USER_BG_ABSENT
find .config/omarchy/themes -mindepth 1 | wc -l                -> 0
find .config/omarchy/hooks/theme-set.d -maxdepth 1
.config/omarchy/hooks/theme-set.d
.config/omarchy/hooks/theme-set.d/show-theme-notification.sample

sed -n '1,14p' .config/hypr/hyprland.conf      # :4 autostart, :13 theme source
sed -n '1,12p' .config/hypr/hyprlock.conf      # :1 source, :10 background path
sed -n '1p' .config/waybar/style.css           # @import "../omarchy/current/theme/waybar.css"
sed -n '1p' .config/swayosd/style.css          # same form
sed -n '1p' .config/alacritty/alacritty.toml   # general.import = [ "…/current/theme/alacritty.toml" ]
sed -n '1,6p' .config/walker/config.toml       # :3 theme, :4 additional_theme_location
sed -n '1p' .local/share/omarchy/default/walker/themes/omarchy-default/style.css
  @import "../../../../../../../.config/omarchy/current/theme/walker.css";   # 7 × ../
readlink .config/mako/config .config/btop/themes/current.theme .config/nvim/lua/plugins/theme.lua
  …/current/theme/mako.ini ; …/current/theme/btop.theme ; ../../../../.config/…/neovim.lua
sha256sum .config/{hypr/hyprland.conf,hypr/autostart.conf,hypr/hyprlock.conf,…}
ce7483f3…, 5ace1701…, b8d173dc…, 8f335ca0…, 6e3ba08f…, 695301c8…, fecf71fa…, 481267af…
sha256sum .local/share/omarchy/bin/omarchy-theme-{set,bg-next,bg-set} \
          .local/share/omarchy/default/hypr/autostart.conf
79069c80…, ee482812…, 638f265f…, acb6a668…   # equal to committed fetch bodies
grep -n swaybg /var/log/pacman.log           # 484, 1158 only; 1158 = installed 1.2.2-1
find .local/share/omarchy/default/themed -maxdepth 1 -name '*.tpl' | wc -l   -> 17

nl -ba fetch/NoteTheme/omarchy-theme-set-v3.8.4.sh | sed -n '1,80p'
  24 # Setup clean next theme directory (for atomic theme config swapping)
  41 rm -rf "$CURRENT_THEME_PATH"
  42 mv "$NEXT_THEME_PATH" "$CURRENT_THEME_PATH"
nl -ba fetch/NoteTheme/omarchy-theme-bg-next-v3.8.4.sh | sed -n '1,60p'   # :46 ln -nsf, :49-50 pkill/setsid
nl -ba fetch/NoteTheme/swaybg-v1.2.2-main.c | sed -n '560,585p;640,670p'
  646-653  dirty → buffer_change → load_required = true
  658-663  wl_list_for_each(image …) load_background_image(image->path)
sha256sum fetch/NoteTheme/omarchy-theme-set-v3.8.4.sh   # 79069c80…9516 = receipt

mkdir /tmp/grepform.atk; printf 'x\n' > /tmp/grepform.atk/a
grep -n -E 'current/(theme|background)' /tmp/grepform.atk
grep: /tmp/grepform.atk: Is a directory            # rc=2 — :128 form not runnable
grep -n '3\.3' corpus/knowledge/theme-wallpaper-plane.md corpus/knowledge/theme-route-r18.md
  theme-route-r18.md:136   # no §3.3 in the plane note
grep -c 'ff93e60c\|68ed5503\|a6720ded\|9aea12fc' corpus/knowledge/theme-route-r18.md  -> 0
```

No file outside this report was written; no fetch receipt was added because
every upstream byte used here came from committed bodies whose digests I
re-hashed.
