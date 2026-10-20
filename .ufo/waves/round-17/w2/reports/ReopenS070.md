# ReopenS070 — S070 re-opened at `988b858`, re-fetched 2026-10-20

Seat: `MadoR17.ReopenS070` (scout, leaf). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `988b858`.
Item: re-open source row **S070** (FlareXes, Hyprland getting-started, screen lock),
fetch with `curl`, digest raw where raw, and verify the row in `corpus/SOURCES.md`
plus its gate line in `corpus/lessons/round-17.md` — URL, verbatim quote at the
stated anchor, digest, tier/status/verdict. S070 is **rejected** with `used-by = —`,
so there is no citing note to mine; the job is to test whether the stated
rejection reason holds.

**Bottom line.** The rejection **holds**; four attacks on it failed. The
**anchors fail**: the row's `raw sha256` cannot be reproduced by anyone, because
this origin randomises its byte stream per request in two independent places, so
both the digest *and* the byte count are random draws. That is a defect in the
anchor, not in the verdict.

## Fetch receipts (observed)

`curl -sS -L`, no user-agent spoofing, eight fetches on 2026-10-20:

| # | HTTP | bytes | raw sha256 |
|---|---|---|---|
| 1 | 200 | 179614 | `bef7f1999589df031e343742dbe0ada0128687fd40c48838e665908627ed1f52` |
| 2 | 200 | 179614 | `411ec5fcea4f04ddb34e502edc879e2f320c3e236d35247a8e0c983d614d2595` |
| 3 | 200 | 179614 | `2933e9d498ccc91a04da0c2e6853f3cac687c707ba6185f374e56ca217740802` |
| 4 | 200 | 179614 | `04a642c37035d7b8adb6a76e3489f81c0508ffbebfa0304e1f4391ee2d2bd56a` |
| 5 | 200 | 179614 | `371075309d611fc3ec7049c91aaab9a5b80e8e32a03ec9b400cfafe445a82645` |
| 6 | 200 | 179613 | `effd4009f2b6ef71d1ca459957003029764fb1f3c3c88744d304fdc9c274e7d6` |
| 7 | 200 | 179613 | `eb49435c3f3ca149b27ea600caa115a9aa67989b9d6e09f5279224e9c34ecb93` |
| 8 | 200 | 179614 | `ada1b4ea218db774c775f6896167fabe86062493a9c4aff5fb4dbd2ff1846bf4` |

Eight fetches, eight distinct digests, same effective URL. Wave-1's receipt
(`.ufo/waves/round-17/w1/reports/SrcTerminalAlternates.md:40`) records
`179613` / `bf875a255610f2665552eb2d9921f2cb43707012686a51f8b9b82a85350ab90a`;
today's two 179613-byte fetches hash to `effd4009…` and `eb49435c…`, neither equal
to it. So `179613` does not imply wave-1's digest even in principle.

### Why it moves (observed)

Two independent randomisations, both outside article text:

1. A Hashnode CDN token mirrored into an `<a href>` at byte ~5615:
   `https://hashnode.dev/cdn-cgi/content?id=<b64>-<epoch>.<frac>-1.2.1.1-<b64>`.
   Its length varies 134–135 chars, which is exactly what flips the whole response
   between 179613 and 179614 bytes (fetches 6–7 vs the rest). [INFERENCE: the
   length variation *is* the cause; the correlation is 8/8.]
2. The Next.js RSC stream `self.__next_f.push([…])` is re-ordered per response.
   Exact char-level evidence, token-normalised fetch 1 vs fetch 5: the 29-byte
   fragment `17:I[80622,[],"IconMark"]\n` sits at offset 71390 in one body and at
   71288 in the other, with no other difference in that region. This is beyond the
   token and is what defeats a token-only normalisation.

Consequence: a *token-only* normalisation still gives **3 distinct digests over 8
fetches**. A stable byte-level anchor does exist — token replaced by `<TOKEN>` and
every `<script>…</script>` replaced by `<script/>` collapses to one digest,
`fd7a60fdaafb8a9a372176209be3f5769e274434e568ef9667230a036d7d5a63` (59593 bytes),
8/8 identical — but it is not what the row stores.

### The stable content anchor (observed)

Extraction recipe: drop `<script|style|svg|noscript>…</…>`, replace every tag with
a newline, unescape entities, keep non-empty trimmed lines.

- **339 non-empty lines** — exactly the row's number, reproduced 8/8.
- sha256 of that text (joined with `\n`):
  **`0bdfa6ae62089b4c9ec0d72b72564cd077b4dcf42681191b53d173c350b27a24`** — identical
  across all eight fetches.

The 339 is *extractor-specific*, though: the same page with scripts retained gives
**384** non-empty lines. The row states no recipe, so a re-verifier using a
different extractor cannot land on 339.

## Row claims, checked against the page

Each line is an anchor into the 339-line extract (`:n`), except where the raw
bytes are the evidence.

| Claim in `corpus/SOURCES.md:82` | Result |
|---|---|
| URL is the page | **holds** — 200, `curl` followed no redirect off-origin |
| `published 2024-12-24, modified 2026-04-05` | **holds** — `<meta property="article:published_time" content="2024-12-24T23:30:24.703Z">`, `article:modified_time` `2026-04-05T14:07:44.263Z`; raw also carries the rendered `April 5, 2026` |
| `hypridle.conf` block with `lock_cmd` | **holds** — `:71` `~/.config/hypr/hypridle.conf`; `:74` `lock_cmd = pidof hyprlock || hyprlock`; `:75` `before_sleep_cmd = loginctl lock-session`; `:76` `after_sleep_cmd = hyprctl dispatch dpms on` |
| listeners 600/900/1800 | **holds** — `:80` `timeout = 600` (comment `:78` `# Lock the screen (10 min)`), `:85` `900` (`:83` 15 min), `:91` `1800` (`:89` 30 min) |
| 0 version tokens in 339 extracted lines | **holds, and survives a harder test** — see below |
| raw sha256 `bf875a25…350ab90a` | **fails as an anchor** — see Fetch receipts |

### Version-token scan (reproduced and widened)

Over the 339-line extract, the row's own expressions:

| expression | hits |
|---|---|
| `[0-9]+\.[0-9]+\.[0-9]+` | **1** — `:296` "Explore weird IPv4 notation: 8.8.2056, legacy parsing, browser behavior, URLs…" (the "unrelated promo line" the wave-1 note named) |
| `hypr(idle|lock) v?[0-9]` | **0** |
| `Hyprland [0-9]` | **0** |

Widened, still zero: `hypr[idlelock]{0,7}\D{0,12}\d+(\.\d+)*` → 0;
`\b(v|version\.?)\s*\d` → 0; `\b0\.\d+` → 0; `\b(latest|newest|recent)\b` → 0;
`hyprland-git` → 0. Raw-HTML grep for semver-shaped strings returns 8 matches, but
every one is SVG path data (`9.104.038`, `6.582.038`, `…-9.472c.405-.022.617.46…`)
or the promo's IPv4 notation; none is a software version and none lies in the
article body.

So: **the page names no Hyprland, hypridle or hyprlock version anywhere.** The
rejection's load-bearing reason is sound, not merely plausible.

### The gate line's quote

`corpus/lessons/round-17.md:57` renders the quote as
`You can learn more about … at Hyprland Wiki`.

Raw bytes at the anchor:

```html
<p>You can learn more about <code>hyprlock</code> configuration at
<a href="https://wiki.hyprland.org/Hypr-Ecosystem/hyprlock/" …>Hyprland Wiki</a>.</p>
```

Rendered sentence, 10 words:
`You can learn more about hyprlock configuration at Hyprland Wiki.`
The gate's ellipsis elides `hyprlock configuration` and the remainder is verbatim —
a legitimate ≤25-word elided quote. The extractor splits this one sentence across
`:59`–`:62` because each inline tag becomes a newline; in the DOM it is a single
paragraph.

One structural gap: the gate row states **no line anchor** (compare the S069 row
immediately above, which carries `[LR:5]`). The quote is at `:59-62`; that should
be written down.

### "Restates the upstream wiki it links" — qualified

Observed: the only places the page defers for configuration detail are
`wiki.hyprland.org/Hypr-Ecosystem/hyprlock/` (`:59-62`) and
`wiki.hyprland.org/Hypr-Ecosystem/hypridle/` (`:109-112`). It is a downstream
summary. Both links point at the **old** `wiki.hyprland.org` domain, not the
current `wiki.hypr.land` — consistent with the era drift noted below, and the same
old-domain trait S069 records for the `v0.9.6` README.

But it is **not a copy** of the pinned upstream example. I fetched
`https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/assets/example.conf`
(200, 1665 bytes, `ef385d88e8c99820ed910eadd62cd14c16bc948317d4f78e93453e24c70d13d1`
— byte-identical to wave-1's R13, so the pinned source is reproducible) and
diffed the keys/values:

| | S070 page (`:73-93`) | hypridle `v0.1.8` example |
|---|---|---|
| `general{}` keys | `lock_cmd`, `before_sleep_cmd`, `after_sleep_cmd` | same three |
| `after_sleep_cmd` | `hyprctl dispatch dpms on` | `hyprctl dispatch 'hl.dsp.dpms({action = "on"})'` |
| listener ladder | 600 / 900 / 1800 | 150 / 150 / 300 / 330 / 1800 |

So the page carries the upstream *schema* with a different, older-style
`dpms` invocation and a different ladder. That strengthens the reject (a stale
variant with no release label) but means the row's word "restates" should be read
as "downstream summary", not "duplicate text". [INFERENCE, labelled: the older
`hyprctl dispatch dpms on` form is pre-Lua-era relative to the `v0.1.8` example;
whether `v0.1.8` still accepts it is not established here and would require running
the binary, which this round forbids.]

### "Route text is mutation commands"

Verbatim in the extract: `:49` `sudo pacman -S hyprlock`; `:92`
`on-timeout = systemctl suspend`; `:86` `on-timeout = hyprctl dispatch dpms off`.
Also `:67` `sudo pacman -S hypridle`, `:108` `exec-once = hypridle`. The
characterisation holds.

## Findings

- **F1 (anchor, must fix).** `raw sha256 bf875a25…350ab90a` is unreproducible by
  construction: this origin emits a per-request CDN token and re-orders its RSC
  stream, so raw bytes — and even the byte count (179613/179614) — are random
  draws. Replace with the content anchor
  `0bdfa6ae62089b4c9ec0d72b72564cd077b4dcf42681191b53d173c350b27a24`
  (339 extracted lines, recipe above), optionally alongside the markup-normalised
  bytes `fd7a60fdaafb8a9a372176209be3f5769e274434e568ef9667230a036d7d5a63`.
  Drop the byte count or mark it "observed at open, unstable".
- **F2 (gate).** Gate row `corpus/lessons/round-17.md:57` carries no line anchor.
  Add `[LR:59-62]`; the quote itself is verbatim and within the 25-word cap.
- **F3 (reproducibility).** "339 extracted lines" only reproduces with an unstated
  extractor; keeping scripts gives 384. Either state the recipe in the anchor or
  rely on the text digest alone.
- **F4 (wording, optional).** "restates the upstream wiki" is a summary claim, not
  a copy claim; the page's `hypridle.conf` diverges from pinned `v0.1.8`
  (600/900/1800; `dpms on` vs `hl.dsp.dpms(...)`). Tighten or annotate.

No counterexample to the verdict was found. Attacks that **failed**: (i) any
version token anywhere — 0 under the row's regexes and 0 under four widened ones;
(ii) the quoted wiki sentence — present, verbatim, and inline as a single
paragraph; (iii) the config/ladder facts — all present at the lines named;
(iv) the dates — exact in `article:*_time` meta.

Registry hygiene: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
→ `mado  ok`, exit 0; no E/W finding touches S070 (the three W04s are S030, S042,
S045). Row has 11 fields / 12 pipes → NF=13, the contract shape; `community` at
tier C, status `rejected`, `recheck 180d`, `used-by —`.

## Limits

`lsp` is not applicable — the question is a web document's tiering and anchor
stability, not symbol resolution in a repository; no grep output is presented as
semantic proof of code. No host package fact was read or judged: every verdict is
about the *document*. Nothing was installed (installs: **none**). Tools used:
`curl`, `sha256sum`, `wc`, `od`, `sed`, `awk`, `grep`, `cmp`, `python3` stdlib
(`re`, `html`, `hashlib`, `difflib`), `git show`-class reads not needed,
`sources-census.sh validate`. No `sudo`, no `pacman`/`yay`/`paru` in any form, no
`systemctl`/`loginctl`/`hyprctl`, no compositor or input probe, no
screenshots, no `omp` process, no `agent.db`, no transcript read, no `git`/`jj`
mutation.
