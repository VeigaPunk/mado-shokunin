# SrcS094 — S097 superseding row for S094 without HTML digests (R18-V1)

Draft for L1 integration. Nothing here is applied: `corpus/SOURCES.md` is L1-owned.
Row placement: ascending id order after S096 (or after S095 if S096 has not landed yet).

## 1. Defect being closed

- `corpus/lessons/round-18-verifier-spotcheck.md:105` — the S094 secondary anchor is
  "GitHub tree HTML pages as sole support", re-fetched twice in the same minute:
  `1a3ddca5…` then `4d001dc8…`, so the digest rotates and cannot pin.
- `corpus/lessons/round-18-verifier-spotcheck.md:117` — R18-V1, routed fix: "Land the
  superseding row the lane planned (lesson M7)."
- `corpus/lessons/round-18.md:22` — M7 states the same rotation as the landing lesson.
- `corpus/SOURCES.md:106` — S094's anchor cell carries both HTML tree digests
  (`50c1ac253df17986…`, `9e1160a06501b0b7…`) beside the raw `colors.toml` digest
  `dbdd13a6…`. Only the raw digest reproduces.
- `corpus/knowledge/theme-route-r18.md:158-163` already records both corrections as an
  unapplied note: the tree digests are "fetch provenance, not pins", and "the only theme
  on this host" means the only *applied* theme.

## 2. New anchor evidence (commands actually run, 2026-10-20)

### 2.1 Raw payload, receipted

```
curl -sSL --max-time 60 -o .ufo/waves/round-19/fetch/SrcS094/colors.toml \
  -w '%{http_code} %{url_effective}' \
  https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
→ 200 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
wc -c colors.toml      → 461
sha256sum colors.toml  → dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786
```

Receipt line: `.ufo/waves/round-19/fetch/SrcS094/receipts.jsonl` (one line,
`schema=mado-fetch-receipt-v1`, `http_status=200`, `bytes=461`, `sha256=dbdd13a6…`,
`fetched_at=2026-10-20T17:06:08Z`, tool `curl 8.23.0 … libcurl/8.23.0`). Re-hash of the
stored body equals the receipt digest: true.

### 2.2 Content-addressed identities (`/tmp` shallow tag clone)

```
git clone --depth 1 --branch v3.8.4 https://github.com/basecamp/omarchy /tmp/omarchy-v384
git -C /tmp/omarchy-v384 rev-parse v3.8.4            → 8fcc9d6048af4cb0e3af8512c78049857a3b53dd
git -C /tmp/omarchy-v384 rev-parse v3.8.4^{commit}   → 8fcc9d6048af4cb0e3af8512c78049857a3b53dd
git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'
  → 8fcc9d6048af4cb0e3af8512c78049857a3b53dd  refs/tags/v3.8.4        (single line)
```

Single `ls-remote` line for the tag with no `^{}` line ⇒ lightweight tag; the tag name and
the commit are the same object, so `v3.8.4^{commit}` is not a hidden indirection.

```
git -C /tmp/omarchy-v384 rev-parse v3.8.4:themes            → 73b7b82475a6beed13ffb55b7af94c5ff0ff2043
git -C /tmp/omarchy-v384 rev-parse v3.8.4:themes/matte-black           → 3fc08f954e5a3f67072a79a7c52d94e0a153b9ec
git -C /tmp/omarchy-v384 rev-parse v3.8.4:themes/matte-black/backgrounds → ff02c34193836c016d8e57bde56bcef5f3c64b4c
```

`git ls-tree -l v3.8.4:themes/matte-black`:

| entry | blob | bytes |
|---|---|---|
| `backgrounds` | tree `ff02c34193836c016d8e57bde56bcef5f3c64b4c` | – |
| `btop.theme` | `c8cdcd02f5a5f88e43689760dd369d850a798f5f` | 2648 |
| `colors.toml` | `5e1a8ccae8462c78a6e9fc491c48cf6d2fc85231` | 461 |
| `icons.theme` | `a3c0a4ca6d3ca74fa7a2b04472bb028b08a7066a` | 9 |
| `neovim.lua` | `7b3f72b21147b49e33fd0e50e94d78afe74029d5` | 150 |
| `preview-unlock.png` | `e23b46655c978524461ef0a0389c86fbe339427d` | 22524 |
| `preview.png` | `ed9c7b47bc6c05833cfb74f9021b3456f07ca93f` | 470315 |
| `unlock.png` | `1a60e70947266dc423e32b2cea8bbd05d42acbd5` | 2512 |
| `vscode.json` | `7786fc79047a10cf2399c6809c77e95116dd51d8` | 65 |

`git ls-tree -l v3.8.4:themes/matte-black/backgrounds`:

| entry | blob | bytes |
|---|---|---|
| `0-ship-at-sea.jpg` | `4375ee2bdd039723d74994503700053114641b86` | 1681677 |
| `1-dark-waters.jpg` | `2afb1bcb16a5561ad883fdb47130c23cca70a940` | 1033920 |
| `2-dot-hands.jpg` | `b76792cb81eb35d68d9b442a8abbc286e9025d77` | 482067 |
| `omarchy.png` | `b34300c1a912dbc0c15ab268ce91142a7d536574` | 4491 |

Note `v3.8.4:themes/matte-black/theme.name` does not exist (round-18 note already recorded
the 404 probe); the theme's name is the directory name.

### 2.3 Host bytes equal the tag blobs (12/12, not just colors.toml)

Each host file's `sha256sum` was compared with `git cat-file blob <blob> | sha256sum` for the
same path. Result: 12/12 IDENTICAL — the 8 `themes/matte-black` files plus the 4
`backgrounds/` images under `~/.config/omarchy/current/theme/`.

```
colors.toml          dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786  IDENTICAL
btop.theme           e9ee6fb643852b378429fc382badef31180aac4cfdccf7201c6749d1999acda9  IDENTICAL
icons.theme          1c2342215182a8e2880028e03e679fad194dbdfa5155b55daf8386390526cfbc  IDENTICAL
neovim.lua           ec7df5fb1d3b7fc644fa0f69cd959ebc43fad8ebdb4aedfd01a5b1e387cd9778  IDENTICAL
preview-unlock.png   00ae994f78564d06c08b17eff733073217400b2bfa2f18405ae10e4b34afe212  IDENTICAL
preview.png          02bf70793f2617710885cc8e389d3d00186b46e1a5a3fe5ffebe776b4ae5ae18  IDENTICAL
unlock.png           ac806f14a214140f33e6c222879633ea24b194f59a86c59847e67bb379680c2d  IDENTICAL
vscode.json          18171ea89a57d4639b935d80a6b271c19a23e4ebe682cc0703144bb77474b83c  IDENTICAL
0-ship-at-sea.jpg    55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac  IDENTICAL
1-dark-waters.jpg    98f0c2b65a2587d114949e8125c22f891c993e0305ca36537bd9b7a9869e8a93  IDENTICAL
2-dot-hands.jpg      e8d73aa65be29bf9d0bec62f64add450485ca52367701ff683e0f2bd66f0791a  IDENTICAL
omarchy.png          63d002b2320cef0184d79bb44fbf4062780d2c083428acf16191344084b75a8f  IDENTICAL
```

`~/.local/share/omarchy/themes/matte-black/colors.toml` also hashes to `dbdd13a6…`
(9 entries: the same 8 files + `backgrounds/`).

The host checkout itself is the tag commit:

```
git -C ~/.local/share/omarchy rev-parse HEAD       → 8fcc9d6048af4cb0e3af8512c78049857a3b53dd
git -C ~/.local/share/omarchy describe --tags      → v3.8.4
cat ~/.local/share/omarchy/version                 → 3.8.3
```

The `version` file and the checkout HEAD disagree. `version` is not used by this row;
identify that checkout by HEAD/`describe`, never by `version`. Why the file lags is `[UNK]`
(likely not regenerated by the last update — `[INFERENCE]`).

### 2.4 Host theme set — scope correction

```
ls -1A ~/.config/omarchy/themes/ | wc -l        → 0            (user theme dir empty)
ls -1 ~/.local/share/omarchy/themes/            → 19 dirs
git ls-tree -d --name-only v3.8.4:themes        → 19 dirs
diff of the two sorted name sets                → no output (SET_IDENTICAL)
```

The 19 names are `catppuccin catppuccin-latte ethereal everforest flexoki-light gruvbox
hackerman kanagawa lumon matte-black miasma nord osaka-jade retro-82 ristretto rose-pine
tokyo-night vantablack white`. `~/.config/omarchy/current/theme.name` is a 12-byte regular
file, `matte-black`, sha256 `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b`.

So "the only theme on this host" is false as written. It is true only under the
applied-theme reading (`current/theme.name`), and even then the honest statement is
"the applied theme", not "the only theme". S097 carries the corrected scope.

`~/.config/omarchy/current/theme/` holds 24 files + `backgrounds/`: the 12 payload files are
byte-identical to the tag (above) and the other 16 (`alacritty.toml`, `chromium.theme`,
`foot.ini`, `ghostty.conf`, `gum.env.conf`, `helix.toml`,
`hyprland-preview-share-picker.css`, `hyprland.conf`, `hyprlock.conf`, `keyboard.rgb`,
`kitty.conf`, `mako.ini`, `obsidian.css`, `swayosd.css`, `walker.css`, `waybar.css`) are
absent from the tag theme tree. S093 (`bin/omarchy-theme-set-templates`) is the declared
writer of such files `[INFERENCE]` for their per-file provenance; this draft claims only
presence/absence, never rendering.

## 3. Proposed S097 row (11 cells, single line)

Insert as one line; the source cell deliberately holds exactly one https URL (the receipted
raw URL) and no HTML/tree URLs, so `fetch-verify`'s first-URL join and anchor-digest join
both hit the receipt in 2.1.

```
| S097 | omarchy v3.8.4 matte-black theme payload (supersedes S094) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | code | A | upstream official payload for the matte-black theme, this host's applied theme (~/.config/omarchy/current/theme.name = matte-black, 12 B); not the host's only theme — 19 payload dirs ship under ~/.local/share/omarchy/themes with the same 19 names as the tag's themes/ tree, and ~/.config/omarchy/themes is empty | tag v3.8.4 → commit 8fcc9d6048af4cb0e3af8512c78049857a3b53dd (lightweight: git ls-remote refs/tags/v3.8.4 has no ^{} line and git rev-parse v3.8.4^{commit} agrees); themes/matte-black tree 3fc08f954e5a3f67072a79a7c52d94e0a153b9ec, blobs btop.theme c8cdcd02f5a5… 2648 B, colors.toml 5e1a8ccae846… 461 B, icons.theme a3c0a4ca6d3c… 9 B, neovim.lua 7b3f72b21147… 150 B, preview-unlock.png e23b46655c97… 22524 B, preview.png ed9c7b47bc6c… 470315 B, unlock.png 1a60e7094726… 2512 B, vscode.json 7786fc79047a… 65 B; themes/matte-black/backgrounds tree ff02c34193836c016d8e57bde56bcef5f3c64b4c, blobs 0-ship-at-sea.jpg 4375ee2bdd03… 1681677 B, 1-dark-waters.jpg 2afb1bcb16a5… 1033920 B, 2-dot-hands.jpg b76792cb81eb… 482067 B, omarchy.png b34300c1a912… 4491 B; raw themes/matte-black/colors.toml sha256 dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786, 461 B | supersedes S094 — anchors the payload by content-addressed identities (tag commit, two tree ids, per-file blob ids, raw colors.toml sha256) instead of per-fetch GitHub HTML tree digests; the 12 payload files under ~/.config/omarchy/current/theme are byte-identical to their v3.8.4 blobs and the host checkout HEAD is the tag commit, so host-to-tag payload provenance is observed for exactly those 12 files; the other 16 files in that directory are absent from the tag theme tree (template outputs, writer not established here); identify the host checkout by HEAD/describe, not by ~/.local/share/omarchy/version, which still reads 3.8.3; rendering and template consumption stay outside this row | mined | 2026-10-20 | on-release | corpus/knowledge/theme-route-r18.md |
```

Cell census of the line above: 11 content cells, status at cell 8 (`mined`), recheck cell 10
(`on-release`), used-by cell 11. It contains one `|`-free prose only; do not reflow it.

Why each anchor element is durable, in one line: the commit is the tag's own object (no
peeling), the two tree ids are SHA-1 over entry names+modes+blob ids, each blob id is SHA-1
over the file bytes, and the raw `colors.toml` sha256 is the digest the fetch receipt
reproduces. None depends on HTML, tokens, rendering order or access date.

## 4. Proposed in-place S094 edit (status + used-by only)

`corpus/SOURCES.md:106`. Rule 2 allows only `status`, `recheck`, `used-by` to move in place;
both moves below are inside that set.

- status cell: ` mined ` → ` rejected `
- used-by cell: ` corpus/knowledge/theme-route-r18.md ` → ` — `

Apply atomically with the `theme-route-r18.md:1` re-point to S097 (handoff in §9); doing the
row first would leave a citation pointing at a rejected row.

Cell-scoped application + one-cell-change assertion. The last line is commented out: run it
once to print the change set, uncomment it to apply. Tested on a `/tmp` copy of the current
`SOURCES.md` (prints `changed cells: [8, 11]`, asserts pass).

```python
python3 - <<'PY'
import pathlib
p = pathlib.Path("corpus/SOURCES.md")
lines = p.read_text().splitlines(keepends=True)
i = next(n for n, l in enumerate(lines) if l.startswith("| S094 |"))
cells = lines[i].split("|")
assert len(cells) == 13 and cells[1].strip() == "S094", (len(cells), cells[1])
assert cells[8].strip() == "mined" and cells[11].strip() == "corpus/knowledge/theme-route-r18.md"
new = list(cells)
new[8] = " rejected "
new[11] = " — "
changed = [k for k in range(len(cells)) if new[k] != cells[k]]
assert changed == [8, 11], changed
print("changed cells:", changed, "->", cells[8].strip(), "→", new[8].strip(),
      ";", cells[11].strip(), "→", new[11].strip())
# apply: p.write_text("".join(lines[:i] + ["|".join(new)] + lines[i + 1:]))
PY
```

Expected print: `changed cells: [8, 11] -> mined → rejected ; corpus/knowledge/theme-route-r18.md → —`.

## 5. Proposed SOURCES notes-block paragraph (rejection reason lives here)

Append after the existing "Round 15 (2026-10-20)…" paragraph. `teaches`/`anchor` cannot move
in place, so this is where S094's reason must be readable in-file (same pattern as S030 at
`corpus/SOURCES.md:176`).

```
Round-19 R18-V1 supersession (2026-10-20): S094's secondary anchor was two
GitHub tree-page HTML digests, which rotate per fetch (round-18 spot-check
re-fetched one such page twice in the same minute: 1a3ddca5… then
4d001dc8…), so it cannot pin a payload. S097 re-anchors the same payload to
the tag's own commit 8fcc9d6…, the two git ls-tree tree ids and the raw
colors.toml sha256 dbdd13a6…; its source cell's first URL is the raw URL
that the .ufo/waves/round-19/fetch/SrcS094 receipt reproduces (200, 461 B).
S094 status mined → rejected in place, its used-by moved to — as
theme-route-r18.md re-points its source token to S097 (rule 2; old→new
logged in lessons/round-19.md). S094's teaches cell cannot change in place,
so its rejection reason lives here and in the lesson: superseded by S097 —
anchor credited per-fetch HTML digests (R18-V1); flip: supplied by S097.
S094's scope sentence "the only theme on this host" is false as written —
19 theme payload dirs ship in the checkout under ~/.local/share/omarchy/
themes and ~/.config/omarchy/themes is empty; only the applied-theme
reading (current/theme.name = matte-black) was ever true, and S097 carries
the corrected scope. The host ~/.local/share/omarchy/version file reads
3.8.3 while that checkout's HEAD is the v3.8.4 commit 8fcc9d6…; rows cite
the commit, not the version file.
```

## 6. Located quotes (≤25 words, with body path:line)

1. `.ufo/waves/round-19/fetch/SrcS094/colors.toml:4` — `background = "#121212"` (5 words).
   Anchors that the fetched bytes are the theme payload itself, not an error/redirect body.
2. `~/.config/omarchy/current/theme.name:1` — `matte-black` (1 word, 12-byte file). Anchors
   the applied-theme reading of the corrected scope.

## 7. Recheck once landed (row `recheck: on-release`)

```
curl -sSL --max-time 60 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | sha256sum
# expect dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786  -
rm -rf /tmp/omarchy-v384 && git clone --depth 1 --branch v3.8.4 https://github.com/basecamp/omarchy /tmp/omarchy-v384
git -C /tmp/omarchy-v384 rev-parse v3.8.4^{commit} v3.8.4:themes/matte-black v3.8.4:themes/matte-black/backgrounds
# expect 8fcc9d6048af4cb0e3af8512c78049857a3b53dd, 3fc08f954e5a3f67072a79a7c52d94e0a153b9ec, ff02c34193836c016d8e57bde56bcef5f3c64b4c
git -C /tmp/omarchy-v384 ls-tree -l v3.8.4:themes/matte-black
sha256sum ~/.config/omarchy/current/theme/colors.toml ~/.config/omarchy/current/theme.name
```

## 8. `fetch-verify` expectation (read from the tool, not run)

`fetch-verify.py` credit requires: a 200 receipt whose `sha256` equals a ≥16-hex digest in the
row's **anchor** cell, and whose `url`/`final_url` equals the **first** https URL of the
**source** cell (`fetch-verify.py:33-47`; conflict rule `:24-30`). S097 satisfies all three
through the single receipt in §2.1; the commit and tree ids in the anchor are 40-hex, so they
could only prefix-credit an astronomically unlikely receipt, and the 12-hex blob prefixes fall
below the tool's 16-hex floor.

```
python3 .ufo/waves/round-18/fetch-verify.py \
  --fetch-root .ufo/waves/round-19/fetch \
  --sources corpus/SOURCES.md --rows S097 \
  --quote 'S097=background = "#121212"'
# expect: FETCH SrcS094/colors.toml ok / ROW S097 receipted / QUOTE S097 ok, exit 0
# (exit also depends on sibling seats' receipts in the same round-19 fetch root)
```

For contrast, the round-18 row fails today because the same tree URL was fetched twice with
different 200 digests (`CONFLICT`), which is exactly what S097 stops citing.

## 9. Handoff items for L1 (not done here)

1. Insert §3 after S096/S095; apply §4 to `corpus/SOURCES.md:106`; append §5 to the notes block.
2. Re-point `corpus/knowledge/theme-route-r18.md:1` `source:` token `S094` → `S097`, and convert
   its `:158-163` erratum bullets from future-tense correction to "landed in round 19 (S097)".
3. Log old→new in `corpus/lessons/round-19.md`: `S094 status mined → rejected`; `S094 used-by
   corpus/knowledge/theme-route-r18.md → —`; new row S097.
4. If the round-19 census expects S096–S105 contiguity, this row is S097 and must not be
   renumbered.

## Limits

- No `fetch-verify` run (item does not name it); the expectation in §8 is read from the
  tool's own docstring (`fetch-verify.py:2-60`) and its credit code, not observed.
- Host checkout `version` vs HEAD disagreement is recorded, not explained.
- The 16 non-payload files under `current/theme/` are counted and named; their writer is
  `[INFERENCE]` from S093, and no rendering claim is made.
- Nothing was fetched beyond the one raw URL and the one tag clone; no HTML page was fetched
  this round, by design.
- `~/.local/share/omarchy` was read with read-only git (`rev-parse`, `describe`); no lane
  write, no jj command, no host mutation.
