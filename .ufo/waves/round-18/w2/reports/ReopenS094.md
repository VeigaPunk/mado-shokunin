# Re-open S094 — non-author check (R17-V3)

Seat `MadoR18.ReopenS094` (leaf, no delegation). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Row under test:
`corpus/SOURCES.md:106` (S094, omarchy v3.8.4 matte-black payload), read at
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`; receipts commit
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Everything below was fetched,
read or hashed by this seat; nothing from the target tree was executed. No
tool was installed or upgraded.

## Verdict

**agree** on the credited artifact, the tag pin and every clause of `teaches`.
Two corrections are required to the row as written: the two HTML tree digests
in the anchor cell are per-fetch and cannot be re-derived by a non-author, and
the scope's parenthetical "the only theme on this host" is false as phrased.
Neither changes the tier, the kind or the P5 credit (details in § Findings).

## Commands run and output

    curl -sSL --max-time 60 -o colors.toml \
      -w '%{http_code} %{url_effective}\n' \
      https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
    -> 200 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
    wc -c colors.toml            -> 461
    sha256sum colors.toml        -> dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786

    git ls-remote --tags https://github.com/basecamp/omarchy 'v3.8.4*'
    -> 8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
    git ls-remote --tags https://github.com/omacom/omarchy 'v3.8.4*'
    -> 8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4

    curl ... https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black
    -> 200 https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black
       229036 B, sha256 6b355a468bfde1e31fa35e546c853f5a40c28933d94f71e48ceb9e9443eb972d
    (same URL fetched a second time)
    -> 200 https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black
       229036 B, sha256 3b18a612e8288e58dd93513cb8339345198e9eb8891822dc198f471b937bf9b8
    curl ... https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black/backgrounds
    -> 200 https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black/backgrounds
       218579 B, sha256 267618a4e4f7b50cc23902b7479e7dead0e0b900f531b237aad77612fc8b9551

    sha256sum /home/vgpnk/.config/omarchy/current/theme/colors.toml
              /home/vgpnk/.local/share/omarchy/themes/matte-black/colors.toml
    -> dbdd13a6…  dbdd13a6…
    cmp .ufo/waves/round-18/fetch/ReopenS094/colors.toml \
        /home/vgpnk/.config/omarchy/current/theme/colors.toml   -> identical (exit 0)

    cat ~/.config/omarchy/current/theme.name            -> matte-black
    sha256sum ~/.config/omarchy/current/theme.name      -> 48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b
    ls ~/.local/share/omarchy/themes/                   -> 19 dirs, catppuccin … white
    ls -a ~/.config/omarchy/themes/                     -> empty (only . and ..)

    python3 (re-hash each receipt against its body)
    -> 4/4 OK (colors.toml 461/dbdd13a6…, tree-theme.html 229036/6b355a46…,
       tree-theme-2.html 229036/3b18a612…, tree-bg.html 218579/267618a4…)

    diff <(git show 4c103b55…:corpus/SOURCES.md | awk 'NR==106') \
         <(awk 'NR==106' corpus/SOURCES.md)        -> identical (ROW_IDENTICAL_WORKTREE)

Receipts written by this seat: `.ufo/waves/round-18/fetch/ReopenS094/receipts.jsonl`
(4 lines, `mado-fetch-receipt-v1`, bodies beside them). My two tree fetches are
kept separately so the instability below is itself receipted.

## Digest comparison (credited URL)

| comparison | value | verdict |
|---|---|---|
| row anchor cell (`corpus/SOURCES.md:106`) | `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786` | equal |
| wave-1 `fetch/NoteTheme/receipts.jsonl:14` (present at `abfbf35`) | `dbdd13a6…`, 461 B, 2026-10-20T15:41:22Z, body `omarchy-themes-matte-black-colors.toml` (worktree-only; not committed); body re-hashed by this seat = `dbdd13a6…` | equal |
| wave-2 peer `fetch/ReviewThemeUpstream/receipts.jsonl:10` (not in `abfbf35`; a `gen_w2.py` seat) | `dbdd13a6…`, 461 B, 2026-10-20T16:00:32Z, body `omarchy-themes-matte-black-colors.toml` (worktree-only); re-hashed by this seat = `dbdd13a6…` | equal |
| this seat's fresh fetch | `dbdd13a6…`, 461 B, 2026-10-20T15:59:53Z | equal |
| host `~/.config/omarchy/current/theme/colors.toml` and `~/.local/share/omarchy/themes/matte-black/colors.toml` | `dbdd13a6…`, `cmp` identical | equal |

Census: exactly three `receipts.jsonl` lines in the round-18 fetch tree name
this exact URL (one committed wave-1 receipt, one wave-2 peer, mine); all are
`http_status` 200, 461 bytes and the same digest. No disagreeing receipt exists.
The `theme.name` probe at `NoteTheme/receipts.jsonl:15` is a 404 and is not
credited by the row.

At both commits under test the whole fetch tree holds only `receipts.jsonl`
files: `git ls-tree -r abfbf35 -- .ufo/waves/round-18/fetch/` (same at
`4c103b5`) is 21 files, all `.jsonl`, no body. So the committed evidence for
this row is the receipt line, not the body. For the credited URL that suffices:
the tag-pinned raw re-fetches byte-exact, so the R17-V3 non-author check passes
without the body.

## Tag pinning

`v3.8.4` resolves to `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` (one line, no
`^{}` peeled line, so a lightweight tag). The same hash answers from both
`basecamp/omarchy` and `omacom/omarchy`. The URL path segment is the ref name
`v3.8.4`, so the URL **is tag-pinned**, not branch-pinned; it cannot drift with
`master`. Residual caveat: a lightweight tag is a movable ref server-side, which
the row's `on-release` recheck guards. The tag hash matches
`theme-route-r18.md:21`.

Note for recheck: HTML tree URLs now redirect to `github.com/omacom/omarchy/…`
(the repository was renamed/moved), while `raw.githubusercontent.com/basecamp/omarchy/…`
still serves 200 without redirect. The row's raw URL is a legacy owner path; it
resolves today and to the same bytes, but a re-open should treat a future 404 on
it as an owner-path change, not a content change.

## Further files named in the source/anchor cells

The source cell names two tree listings; both were re-fetched.

| listing | anchor | wave-1 body | my fetch | names observed |
|---|---|---|---|---|
| `themes/matte-black` tree | `50c1ac253df17986b02b44bde7f2ddb0bdebdc66abda9e07a02041ee57e302ef` | `50c1ac25…` (229027 B) | `6b355a46…`, then `3b18a612…` (229036 B) | `btop.theme, colors.toml, icons.theme, neovim.lua, preview.png, preview-unlock.png, unlock.png, vscode.json, backgrounds/` |
| `themes/matte-black/backgrounds` tree | `9e1160a06501b0b761f17ded98b0671dd34ed8e42c083efffe533f2a8ed32575` | `9e1160a0…` (218578 B) | `267618a4…` (218579 B) | `0-ship-at-sea.jpg, 1-dark-waters.jpg, 2-dot-hands.jpg, omarchy.png` |

The anchor values are honestly recorded — `sha256sum` over the wave-1 body
files in the lane worktree reproduces `50c1ac25…` and `9e1160a0…` — but they
are **not re-derivable**, and the bodies are not in the commits under test:
`git ls-tree -r abfbf35 -- .ufo/waves/round-18/fetch/` (identical at
`4c103b5`) lists 21 `receipts.jsonl` files and no body file. The committed
artifact is the receipt line; the bytes are worktree-only. Two consecutive fetches of the same URL differ at the byte
level, and neither matches the anchor:

- my pair differs in 2 physical lines (the head token block) and normalizes
  (delete `visitor-payload`, `visitor-hmac`, `html-safe-nonce`, `request-id`)
  to one digest, `329eb7b9e4cb5b7484b8e4d33c0d5e196c0e8e317c45876b7f294c2b1a8dd0b1`;
- the wave-1 body does not normalize to that value (`b7b33ba4…`), and the
  residual 12-line diff is `fetch-nonce`, two `opengraph.githubassets.com`
  image hashes, button/tooltip UUIDs, and the embedded JSON;
- parsing the embedded JSON (`react-app.embeddedData` → `codeViewTreeRoute`)
  shows why: `fileTreeProcessingTime` (a timing), an `uploadToken`, and three
  per-session `csrf_tokens` differ between wave 1 and now. The listing itself
  is stable: both bodies give `refInfo.name = "v3.8.4"`, `refType = "tag"`,
  `path = "themes/matte-black"` (resp. `…/backgrounds`) and the identical
  `tree.items` name sets listed above.

So the two tree digests are one-shot observations of a tokenized page, not
anchors. This is the failure mode the round-18 lesson §Gate already excludes
for HTML pages ("per-fetch tokens make the digest irreproducible"); S094 keeps
such digests in its anchor cell without that caveat. The *names*, which are what
the row's `teaches` actually uses, do reproduce from the embedded JSON at the
tag, and they also match the checkout directory (`~/.local/share/omarchy/themes/matte-black/`:
the same eight files plus `backgrounds/` with the same four images).

## kind / tier / scope

- **kind `code`** — the row covers an upstream config/theme payload
  (`colors.toml`, `btop.theme`, `neovim.lua`, `vscode.json`); config bytes are
  already `code` in this registry (e.g. S020). Correct.
- **tier `A`** — the source is the upstream project's own repository at a tag,
  primary for the payload's bytes and listing. No secondary restatement is
  involved. Correct for that scope.
- **scope** — "upstream official theme payload for the matte-black theme"
  names the surface keyword `theme`, so the P5 keyword test
  (`.ufo/waves/round-17/measure.py:150` `SURFACE_KEYWORDS['P5']`) is satisfied
  by the source and scope cells, and `mined_a()` accepts it (status `mined`,
  tier A, `used-by` = `corpus/knowledge/theme-route-r18.md`). The parenthetical
  **"(the only theme on this host)" is false as written**: the host carries 19
  payload directories in `~/.local/share/omarchy/themes/` (`catppuccin`,
  `catppuccin-latte`, `ethereal`, `everforest`, `flexoki-light`, `gruvbox`,
  `hackerman`, `kanagawa`, `lumon`, `matte-black`, `miasma`, `nord`,
  `osaka-jade`, `retro-82`, `ristretto`, `rose-pine`, `tokyo-night`,
  `vantablack`, `white`; matte-black has 9 entries = 8 files + `backgrounds`).
  What is true: `~/.config/omarchy/themes/` is empty (no user themes) and
  `current/theme.name` is `matte-black`, so matte-black is the only theme
  *applied*. The parenthetical does not affect tier or the rubric, but it is a
  false host claim and should be corrected.
- **`teaches`** — grounded clause by clause: eight files plus a `backgrounds/`
  directory (tag tree, verified above); four images (tag tree, verified);
  `colors.toml` byte-identical to the host's current copy (`cmp` exit 0);
  "other payload bytes not compared" is true (`theme-route-r18.md:91` says the
  seven others were compared host-to-host only); "does not show which files are
  rendered by templates" is true (payload-vs-template precedence is `[OP:43]`
  source inference, not shown by the tree page).

## Is the citing note truthful?

`corpus/knowledge/theme-route-r18.md` (S094 in its `source:` line; the note
labels `[OM]` "names only" at :26):

- :64 names the eight files and the `backgrounds/` directory and lists the four
  images — verified from the tag tree's embedded JSON; truthful.
- :64 also repeats "Tree page SHA-256: 50c1ac25… (theme) and 9e1160a0…
  (backgrounds)" without saying the values are per-fetch. The values match the
  worktree bodies (no body is committed), but a non-author cannot reproduce
  them; the note inherits the row's defect.
- :65 (461 B, `dbdd13a6…`) and :86/:91 (`colors.toml` host pin
  `dbdd13a6…`, byte-identical) — verified; truthful.
- No claim in the note goes beyond the row on this surface; the payload-vs-render
  split is correctly marked `[INF]`/`[UNK]` at :92 and :141.

## Findings for L1

1. **D1 (row wording, must fix):** the two tree digests in the anchor cell are
   not re-derivable, and no committed body backs them (§ Further files:
   `git ls-tree` over `abfbf35`/`4c103b5` shows only `receipts.jsonl` under
   `fetch/`). Replace "tree listing sha256 …" with an observation stamp
   and the stable evidence, e.g. "tree listings read 2026-10-20T15:40:32Z /
   15:41:43Z, per-fetch HTML (not re-derivable); names from the embedded
   `codeViewTreeRoute` JSON at `refInfo.name=v3.8.4`, `refType=tag`". Mirror the
   caveat at `theme-route-r18.md:64`.
2. **D2 (scope, must fix):** "the only theme on this host" → "the only theme
   applied on this host (no user themes; 19 payloads ship in the checkout)".
3. **D3 (minor):** the source cell says "digest-only HTML", but 229,027 B and
   218,578 B of wave-1 HTML bodies exist in the worktree (not committed). Say
   "single-fetch HTML, worktree body".
4. **Not a defect:** the raw `colors.toml` credit is sound (byte-exact, three
   agreeing receipts, tag-pinned, host-identical), and the P5 keyword test and
   tier-A test pass.

GATE | S094 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS094/colors.toml:4 "background = \"#121212\"" (3 words) | dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786 | agree: 461 B reproduces byte-exact at tag v3.8.4=8fcc9d60 and three receipts agree; fix the anchor's per-fetch HTML digests and the scope's false "only theme"
