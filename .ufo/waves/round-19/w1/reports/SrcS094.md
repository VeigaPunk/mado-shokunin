# SrcS094 — S097 re-anchors the matte-black payload on commit+tree+blob ids; S094's HTML digests retire

Deliverable: `.ufo/waves/round-19/drafts/SrcS094-row.md` (S097 row line, S094 in-place edit,
SOURCES notes paragraph, quotes, recheck commands, handoff). `corpus/SOURCES.md` was **not**
edited — it is L1-owned.

## 1. Observed facts

**Raw anchor reproduces.** `curl -sSL --max-time 60 -o .ufo/waves/round-19/fetch/SrcS094/colors.toml -w '%{http_code} %{url_effective}' https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml`
→ `200` and the same URL; 461 bytes; sha256 `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`,
equal to S094's credited raw digest. One receipt line in
`.ufo/waves/round-19/fetch/SrcS094/receipts.jsonl` (`http_status=200`, `bytes=461`,
`fetched_at=2026-10-20T17:06:08Z`, body re-hash equals the record).

**Content-addressed replacement for the HTML tree digests.** `git clone --depth 1 --branch v3.8.4 https://github.com/basecamp/omarchy /tmp/omarchy-v384`:

- `rev-parse v3.8.4` = `rev-parse v3.8.4^{commit}` = `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; `git ls-remote … refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'` returns that one line only ⇒ lightweight tag, no hidden peel.
- `v3.8.4:themes/matte-black` → `3fc08f954e5a3f67072a79a7c52d94e0a153b9ec`
  (8 blobs: btop.theme 2648 B, colors.toml 461 B, icons.theme 9 B, neovim.lua 150 B, preview-unlock.png 22524 B, preview.png 470315 B, unlock.png 2512 B, vscode.json 65 B).
- `v3.8.4:themes/matte-black/backgrounds` → `ff02c34193836c016d8e57bde56bcef5f3c64b4c`
  (4 blobs: 0-ship-at-sea.jpg 1681677 B, 1-dark-waters.jpg 1033920 B, 2-dot-hands.jpg 482067 B, omarchy.png 4491 B).
- Full `git ls-tree -l` listings with every blob id are in draft §2.2.

**Host bytes equal the tag, 12/12 (not just colors.toml as S094 claimed).** Each
`~/.config/omarchy/current/theme/<path>` sha256 was compared with `git cat-file blob <blob> | sha256sum`:
all eight theme files and all four backgrounds are IDENTICAL (per-file digests in draft §2.3).
`~/.local/share/omarchy/themes/matte-black/colors.toml` is also `dbdd13a6…`.
Host checkout identity: `git -C ~/.local/share/omarchy rev-parse HEAD` = `8fcc9d6…`,
`describe --tags` = `v3.8.4`.

**Scope sentence was false.** `ls -1A ~/.config/omarchy/themes/ | wc -l` → `0`;
`~/.local/share/omarchy/themes/` → 19 dirs; `git ls-tree -d --name-only v3.8.4:themes` → 19
dirs; sorted name sets `diff` → empty (identical). `~/.config/omarchy/current/theme.name` is a
12-byte file `matte-black`, sha256 `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b`.
So "the only theme on this host" holds only under the applied-theme reading; S097 states
"applied theme" plus the 19-dir census.

`~/.config/omarchy/current/theme/` = 24 files + `backgrounds/`: the 12 payload files are the
identical ones above; the other 16 (alacritty.toml, chromium.theme, foot.ini, ghostty.conf,
gum.env.conf, helix.toml, hyprland-preview-share-picker.css, hyprland.conf, hyprlock.conf,
keyboard.rgb, kitty.conf, mako.ini, obsidian.css, swayosd.css, walker.css, waybar.css) are
absent from the tag theme tree.

**Draft mechanics validated, not assumed.** The S097 line parses to 11 content cells
(`split("|")` → 13 with edge empties); its source cell holds exactly one https URL and it is
the receipted raw URL; the full 64-hex raw digest sits in the anchor cell — the three
`fetch-verify.py:33-47` credit conditions. The §4 edit snippet was run on `/tmp` copies of
`SOURCES.md`: output `changed cells: [8, 11] -> mined → rejected ; corpus/knowledge/theme-route-r18.md → —`,
and a whole-file compare shows line 106 only, 11 of 13 cells equal, differing cells exactly
status and used-by.

## 2. Inference

- The 16 extra `current/theme/` files are `omarchy-theme-set-templates` outputs (S093 names
  that writer). Presence/absence is observed; per-file provenance is `[INFERENCE]`.
- `~/.local/share/omarchy/version` (3.8.3) lags the checkout HEAD (`8fcc9d6…`, v3.8.4) because
  the file is not regenerated on update. `[INFERENCE]` — recorded as a caveat in S097's
  teaches cell so recheckers identify the checkout by HEAD, not by that file.

## 3. Unknowns

- `[UNK]` why `version` and HEAD disagree (no writer path read this round).
- `[UNK]` whether any of the 19 shipped themes other than matte-black has byte identity with
  the tag (only matte-black was compared).
- `[UNK]` whether a round-19 `fetch-verify` run will be clean end-to-end: only the S097 join
  was reasoned from the tool's rules, and sibling seats share the round-19 fetch root.

## Limits

- Did not run `fetch-verify.py` (not named by the item); §8 of the draft predicts
  `FETCH SrcS094/colors.toml ok` / `ROW S097 receipted` / `QUOTE S097 ok` from its docstring
  only.
- Did not edit `corpus/SOURCES.md`, `corpus/knowledge/theme-route-r18.md`, or any lesson; the
  note re-point and old→new log are handoff items 2–3 in the draft.
- No HTML page fetched this round, by design. No pacman/systemctl/compositor/live-gate call;
  host trees read as bytes and via read-only git (`rev-parse`, `describe`, `ls-tree`,
  `ls-remote`, `cat-file`). No jj command, no git write in the lane. Writes confined to
  `.ufo/waves/round-19/{fetch/SrcS094,drafts,w1/reports}`, plus `/tmp/omarchy-v384` and
  `/tmp/s094test*`.
- One fetch, one clone: the fetch receipt covers the raw URL only; the git identities are
  reproducible from the tag but are not receipt-schema records.

## Installs

none.
