# NoteTheme — P5 theme and wallpaper documentary route (round 18)

Seat: `MadoR18.NoteTheme` (leaf, no delegation). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin. Read-only on host; no gate run; no SOURCES/QUALITY/SKILL/SCORECARD/LOG/lesson edits.

## Behavior

Drafted the P5 documentary route note `corpus/knowledge/theme-route-r18.md` (`surface: P5`), shaped on `corpus/knowledge/idle-lock-route-r17.md`. Head is four lines (`source:`, `verified-at:`, `recheck:`, `surface: P5`) then the title. Sections present: `## Upstream contract`, `## Host declaration`, `## Safe observation`, `## Unexercised behavior` (each has well over three non-blank lines; the last carries `[UNK]`). The note makes no observed-behaviour claim.

Does not contradict `corpus/knowledge/theme-wallpaper-plane.md`: `theme.name` pin (`48749715…`), the background link target, the 24-file `current/theme/` count, the eight ★ pins, and the mako/btop/neovim symlinks all re-measured identical. The round-7 live swaybg observation (PID 1203358, §3.3) was not repeated; the note marks it `[UNK]`.

## Gates

None run (lane rule: seats do not run gates). Main agent should run once after integration:
- `head -n 4 corpus/knowledge/theme-route-r18.md` shows `source:` on line 1 and `surface: P5` on line 4.
- `grep -n '^## ' corpus/knowledge/theme-route-r18.md` shows the four required headings.
- Replace every `S0xx-pending-{A,B,C,D}` token in the note (head line 1 and nowhere else) with the ids L1 assigns; the rows in `.ufo/waves/round-18/drafts/NoteTheme-rows.md` are the paste source.

## Touched surfaces

Created (allowed set only):
- `corpus/knowledge/theme-route-r18.md`
- `.ufo/waves/round-18/drafts/NoteTheme-rows.md` (draft SOURCES rows A-D with `S0xx-pending` ids, plus landing notes for L1)
- `.ufo/waves/round-18/fetch/NoteTheme/` — 17 fetched bodies and `receipts.jsonl` (17 JSON lines, schema `mado-fetch-receipt-v1`; each line's `sha256` and `bytes` re-checked against its body file: all match)
- `.ufo/waves/round-18/w1/reports/NoteTheme.md` (this report)

Scratch only under `/tmp` (`mktemp` bodies, `/tmp/nt_err`), all moved or discarded.

## Sources and receipts

Upstream, tag-pinned (`curl -sSL`, no auth):
- omarchy v3.8.4 `bin/omarchy-theme-set` (sha `79069c80…`), `bin/omarchy-theme-bg-next` (`ee482812…`), `bin/omarchy-theme-bg-set` (`638f265f…`), `bin/omarchy-theme-set-templates` (`01264122…`), `default/hypr/autostart.conf` (`acb6a668…`, HTTP 200), `themes/matte-black/colors.toml` (`dbdd13a6…`).
- omarchy v3.8.4 theme tree pages (`themes/matte-black`, `themes/matte-black/backgrounds`, `themes`) — GitHub pages; final URL redirects to `github.com/omacom/omarchy`.
- swaybg v1.2.2 `swaybg.1.scd` (`68ed5503…`), `README.md` (`a6720ded…`), `main.c` (`ff93e60c…`), `background-image.c` (`9aea12fc…`), and the repo tree page.
- Tag commits (`git ls-remote --tags`): omarchy `v3.8.4` = `8fcc9d60…`; swaybg `v1.2.2` = `a59ea3db…` (peeled).
- Non-credited 404s recorded honestly: swaybg `doc/swaybg.1.scd` and `doc/` tree (the man page is at repo root); a matte-black `theme.name` probe.

Host, file bytes only (`cat`, `readlink`, `stat`, `sha256sum`, `grep -n`):
- `~/.config/omarchy/current/{theme.name, background, theme/}`; `~/.config/omarchy/{backgrounds,themes,current/next-theme}` absence/emptiness; `hooks/theme-set.d/` (sample only).
- Consumer declarations: `hypr/hyprland.conf:4,13`, `hypr/hyprlock.conf:1,7-12`, `waybar/style.css:1`, `swayosd/style.css:1`, `alacritty/alacritty.toml:1`, walker `config.toml:3-4` and omarchy-default `style.css:1`, `mako/config` symlink, `btop/themes/current.theme` symlink, `btop/btop.conf:5`, `nvim/lua/plugins/theme.lua` symlink.
- Host omarchy bin/autostart bytes equal the tag bytes (three sha matches above).
- `/var/log/pacman.log` (file read): `installed swaybg (1.2.2-1)` at :1158; `grep -n swaybg` returns :484 and :1158 only.

## Findings

1. The theme-set ritual never restarts swaybg directly; swaybg is relaunched from `omarchy-theme-bg-next` (`[OT:48-50]`, `[OB:49-50]`), and `omarchy-theme-bg-set` does the same for an arbitrary image. Both retarget `current/background` with `ln -nsf`, so the autostart declaration (`[OA:5]`) names a link that is retargeted, not a file.
2. The 24-file `current/theme/` tree is 8 payload files + 16 template renders (17 `.tpl` minus `btop.theme`, which the payload wins; `[OP:43]`). Count consistent; rendered bytes not re-derived (`[UNK]`).
3. `colors.toml` is byte-identical between the tag payload and the host. The other seven payload files agree host-to-host and by name with the tag; their tag bytes were not fetched.
4. Swaybg opens the image by path when it loads (`[SM:658-663]`, `[SB:24-46]`). Whether a running process re-reads a retargeted link is `[UNK]`; the fetched files show no file watch, but `main.c` was grep-traced, not read in full.
5. Host consumer edges are as declared; walker's import is seven `../` from the omarchy-default directory, resolving to `~/.config/omarchy/current/theme/walker.css`. Mako, btop and neovim are symlinks into `current/theme/`. Every edge is declared-only; none of the running consumers was observed.

## Out of scope / not done

- No live probe: no `pgrep`, `hyprctl`, `swaybg`, `omarchy`, `pacman`, `systemctl`, or hook execution (host pause and "config trees read as bytes only").
- No P3 walker note (`walker-route-r18.md` not written by this seat; walker appears only as a P5 consumer edge).
- No SOURCES.md row, QUALITY criterion, SKILL, LOG or lesson edit; ids `S0xx-pending-A..D` are placeholders for L1.
- No gate rows proposed; `theme-wallpaper-plane.md` §6 remains the only gate spec.

## Tooling

No installs or upgrades. Used existing `curl 8.23.0`, `git` (ls-remote only), `python3` (receipt JSON and receipt re-check in /tmp), `sha256sum`, `stat`, `readlink`, `grep`. No pacman, sudo, or package query.

## Findings for the main agent (routed)

- Ids: L1 must assign four ids (A swaybg upstream docs/code; B omarchy writers/templates/autostart; C omarchy matte-black payload; D host P5 state and consumer declarations) and replace the four `S0xx-pending-*` tokens in the note head.
- Receipts 404 (`swaybg doc/…`, matte-black `theme.name`) are not credited; keep them only as recorded non-credited fetches.
- Byte-level check of the seven non-`colors.toml` payload files and the 1.68 MB `0-ship-at-sea.jpg` (above the 1 MiB fetch cap) remains open.
