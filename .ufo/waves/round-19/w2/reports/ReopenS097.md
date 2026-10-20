# ReopenS097 — holds

Attacked row `corpus/SOURCES.md:109` (S097) at tip `01b80946d92b26370d3012a7da655d00dd135154`; worktree line sha256 `fcd9b35f3690bd1cdb64054fb205f8ac621b4a38947a5709920f7f83beeaa44b` equals the committed line's sha256. Four independent re-derivations (raw fetch, own tag clone, host scope listing, host checkout identity). No false claim found; two durability caveats that the row already frames correctly.

## Attack 1 — raw URL bytes vs the row's sha256/461 B

```
$ curl -sS -D headers.txt -o /tmp/ReopenS097/colors.toml -w 'http=%{http_code} bytes=%{size_download}\n' \
    https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
http=200 bytes=461
$ sha256sum /tmp/ReopenS097/colors.toml
dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786  colors.toml
$ sed -n '4p' /tmp/ReopenS097/colors.toml
background = "#121212"
fetched_at: 2026-10-20T18:02:50Z (UTC, from response `date:`)
```

Matches the row's `raw themes/matte-black/colors.toml sha256 dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786, 461 B`, the committed receipt `.ufo/waves/round-19/fetch/SrcS094/receipts.jsonl` (200 / 461 / dbdd13a6… / fetched_at 2026-10-20T17:06:08Z), and the Gate line `corpus/lessons/round-19.md:42` quote at `.ufo/waves/round-19/fetch/SrcS094/colors.toml:4` (3 words). Two fetches 57 min apart, identical bytes. The server `etag` (`e9dd015f…`) is not the content sha256 and is not cited by the row — correctly so; a 200 plus body digest is the receipt, not the header.

## Attack 2 — tag commit, tree ids, blob ids (own /tmp clone)

```
$ git clone --quiet --depth 1 --branch v3.8.4 https://github.com/basecamp/omarchy /tmp/ReopenS097-omarchy
$ git -C /tmp/ReopenS097-omarchy rev-parse HEAD; git -C … rev-parse v3.8.4^{commit}; git -C … describe --tags --exact-match HEAD
8fcc9d6048af4cb0e3af8512c78049857a3b53dd
8fcc9d6048af4cb0e3af8512c78049857a3b53dd
v3.8.4
$ git ls-remote https://github.com/basecamp/omarchy 'refs/tags/v3.8.4*'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4        # one line, no ^{} → lightweight
$ git rev-parse 'v3.8.4:themes/matte-black'          → 3fc08f954e5a3f67072a79a7c52d94e0a153b9ec
$ git rev-parse 'v3.8.4:themes/matte-black/backgrounds' → ff02c34193836c016d8e57bde56bcef5f3c64b4c
$ git ls-tree -l 'v3.8.4:themes/matte-black'
100644 blob c8cdcd02f5a5f88e43689760dd369d850a798f5f    2648  btop.theme
100644 blob 5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231     461  colors.toml
100644 blob a3c0a4ca6d3ca74fa7a2b04472bb028b08a7066a       9  icons.theme
100644 blob 7b3f72b21147b49e33fd0e50e94d78afe74029d5     150  neovim.lua
100644 blob e23b46655c978524461ef0a0389c86fbe339427d   22524  preview-unlock.png
100644 blob ed9c7b47bc6c05833cfb74f9021b3456f07ca93f  470315  preview.png
100644 blob 1a60e70947266dc423e32b2cea8bbd05d42acbd5    2512  unlock.png
100644 blob 7786fc79047a10cf2399c6809c77e95116dd51d8      65  vscode.json
040000 tree ff02c34193836c016d8e57bde56bcef5f3c64b4c       -  backgrounds
$ git ls-tree -l 'v3.8.4:themes/matte-black/backgrounds'
100644 blob 4375ee2bdd039723d74994503700053114641b86 1681677  0-ship-at-sea.jpg
100644 blob 2afb1bcb16a5561ad883fdb47130c23cca70a940 1033920  1-dark-waters.jpg
100644 blob b76792cb81eb35d68d9b442a8abbc286e9025d77  482067  2-dot-hands.jpg
100644 blob b34300c1a912dbc0c15ab268ce91142a7d536574    4491  omarchy.png
```

Every prefix and size in the row's anchor cell matches (tag commit `8fcc9d60…`, both tree ids, all 8 + 4 blob ids/sizes). Linkage between raw URL and tree proven directly:

```
$ git -C /tmp/ReopenS097-omarchy hash-object /tmp/ReopenS097/colors.toml
5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231   # == v3.8.4:themes/matte-black/colors.toml
```

GitHub API corroboration (no auth; saved under /tmp/ReopenS097/api): `GET /repos/basecamp/omarchy/git/ref/tags/v3.8.4` 301 → `/repositories/994093166/git/ref/tags/v3.8.4` 200, 368 B, `object.type = "commit"`, `object.sha = 8fcc9d60…`; `GET …/commits/8fcc9d60…` 200, 4,723 B, same sha. Fetched 2026-10-20T18:04:49Z; sha256 `a503d17da45fecbe7a5293c41d29a8b88fa0bf0f4b22293ca16f415f7ac9efd9` (tagref) and `d561c04b34ee1ddd09f3bde58321937a51949cd17bbaa34b0a3e78863c950f9b` (commit). The 301 is a repo-id redirect, not a move of content; raw and git both resolve under `basecamp/omarchy`.

## Attack 3 — scope sentence (applied theme, 19 dirs, empty user dir)

Names only; no file bodies read from either theme dir.

```
$ cat -A ~/.config/omarchy/current/theme.name   → matte-black\n ; wc -c → 12
$ find ~/.local/share/omarchy/themes -mindepth 1 -maxdepth 1 -printf '%y\n' | sort | uniq -c
     19 d                                # all directories, no hidden entries
$ diff <(ls -1 ~/.local/share/omarchy/themes | sort) \
       <(git -C /tmp/ReopenS097-omarchy ls-tree --name-only 'v3.8.4:themes' | sort) && echo IDENTICAL_SETS
IDENTICAL_SETS
$ git -C /tmp/ReopenS097-omarchy ls-tree 'v3.8.4:themes' | awk '{print $2}' | sort | uniq -c
     19 tree
$ find ~/.config/omarchy/themes -mindepth 1 -maxdepth 1 | wc -l
0
```

The 19 names on both sides are `catppuccin catppuccin-latte ethereal everforest flexoki-light gruvbox hackerman kanagawa lumon matte-black miasma nord osaka-jade retro-82 ristretto rose-pine tokyo-night vantablack white`; each host dir carries 10–21 files (matte-black: 12). `theme.name` is exactly `matte-black\n` (12 B) and `~/.config/omarchy/current/theme/colors.toml` sha256 is `dbdd13a6…`, so the "applied theme" reading is supported by both the marker and the payload byte. Scope sentence holds as written.

## Attack 4 — host-to-tag provenance sentence and rejected-S094 supersession

```
$ for f in $(find ~/.config/omarchy/current/theme -type f -printf '%P\n' | sort); do
    h=$(git -C /tmp/ReopenS097-omarchy hash-object "$HOME/.config/omarchy/current/theme/$f")
    tag=$(git -C /tmp/ReopenS097-omarchy rev-parse -q --verify "v3.8.4:themes/matte-black/$f" 2>/dev/null || echo NONE)
    [ "$h" = "$tag" ] && st=MATCH || { [ "$tag" = NONE ] && st=ABSENT || st=DIFF; }
    printf '%-45s host=%s tag=%s %s\n' "$f" "${h:0:12}" "${tag:0:12}" "$st"; done
… 12 MATCH: backgrounds/{0-ship-at-sea.jpg,1-dark-waters.jpg,2-dot-hands.jpg,omarchy.png},
           btop.theme, colors.toml, icons.theme, neovim.lua, preview.png, preview-unlock.png,
           unlock.png, vscode.json
… 16 ABSENT: alacritty.toml chromium.theme foot.ini ghostty.conf gum.env.conf helix.toml
           hyprland.conf hyprland-preview-share-picker.css hyprlock.conf keyboard.rgb kitty.conf
           mako.ini obsidian.css swayosd.css walker.css waybar.css
… 0 DIFF
```

28 files total = the row's "12 … byte-identical … the other 16 … absent from the tag theme tree". The parenthetical "template outputs" is corroborated by the tag itself even though the row leaves the writer `[UNK]`: `default/themed/` ships 17 `.tpl` files whose names are exactly those 16 plus `btop.theme.tpl` (btop.theme is already supplied by the theme tree, and `bin/omarchy-theme-set-templates:6-9,38,43` only fills absent outputs). `[INFERENCE]` that the host copies came from that script; the row does not claim it.

Host checkout identity, also as stated:

```
$ git -C ~/.local/share/omarchy rev-parse HEAD; git -C ~/.local/share/omarchy describe --tags
8fcc9d6048af4cb0e3af8512c78049857a3b53dd
v3.8.4
$ git -C ~/.local/share/omarchy remote -v → origin https://github.com/basecamp/omarchy.git ; status --porcelain → 0 lines
$ cat ~/.local/share/omarchy/version → 3.8.3   (6 B, newline)
$ git -C ~/.local/share/omarchy hash-object themes/matte-black/colors.toml → 5e1a8ccae846… (= tag blob)
```

Supersession side: at `01b80946`, S094 (`corpus/SOURCES.md:106`) is `rejected`, `used-by —`, `teaches` left as the historical mined text (rule 2 forbids rewriting it) — its false "(the only theme on this host)" scope is retained as history, and S097 carries the correction. S097 `teaches` opens `supersedes S094 —` as rule 2 requires; `used-by corpus/knowledge/theme-route-r18.md` exists and `corpus/knowledge/theme-route-r18.md:167-168` records the re-point and the 19-dir/applied-theme correction. Row shape: `NF=13` (11 cells), census `malformed=0`, no duplicate ids, tier `A`, status `mined`, opened `2026-10-20`, recheck `on-release`.

Checker re-run (not the gate): `python3 -I .ufo/waves/round-19/anchor-durability.py 01b80946… --rows S094,S097` → `skipped: S094 status=rejected` / `ROW S097 durable — sha256 over raw bytes at ref v3.8.4` / `SUMMARY … mined=1 durable=1 per_fetch_digest=0 unpinned_alias=0 flagged=0 receipt_files=57 bad_receipt_lines=0`, rc=0.

## Findings / overclaim attempt

No claim in S097 is false. The two things a reader could over-read are already correctly hedged by the row:

- **Mutable tag.** `v3.8.4` is an upstream ref; the durable part is the commit/tree/blob ids and the colors.toml sha256, which is exactly how the row frames it. If upstream retagged, the row's ids still re-obtain via the commit — the raw URL alone would not. `[INFERENCE]`, not observed drift: two fetches 57 min apart agreed.
- **`lightweight` observation is unreceipted.** The row's `git ls-remote … no ^{}` phrase has no committed receipt (the `fetch/SrcS094` receipt covers only the raw body). I reproduced it (one line, no `^{}`) and the API independently shows `object.type = "commit"`; the phrase is true, just not receipt-backed.

Also noted, outside S097's claims: `anchor-durability.py` classifies S097 `durable` structurally (`SHA64 in anchor` + pinned ref segment; `evaluate()` at `.ufo/waves/round-19/anchor-durability.py:302`) — it never compares the row's sha256 to a receipt digest. The truth of the digest rests on the fetch receipt and on my independent re-fetch, both equal.

## Limits

- Read-only: no gate run (needs `--selftest`/`--regression`, and a bare run is banned); no `fetch-verify.py` run (owned by the wave-2 RerunFetchVerify seat); no walker/pacman/service/compositor command; no lane edits. Only `/tmp/ReopenS097*` written.
- Clone is `--depth 1` at the tag: it proves the tag endpoint, commit, subtrees and blob contents; it cannot prove branch reachability or tag history, neither of which S097 claims.
- API results come from unauthenticated GitHub with 301→repo-id redirects; they corroborate, and no part of the row depends on them.
- `[UNK]`: none material for S097. Remaining: whether upstream ever force-moves `v3.8.4` (unobservable; content ids mitigate), and whether S095-class host theme consumers read these bytes (outside this row by its own last clause).

## Installs

None.
