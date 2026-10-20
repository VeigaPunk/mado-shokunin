# SrcThemeAlternates — secondary P3/P5 candidates, reject/queue rulings

Round 18, wave 1, seat `MadoR18.SrcThemeAlternates` (leaf; no dispatch).
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. This seat wrote only this
report plus its own fetch receipts under
`.ufo/waves/round-18/fetch/SrcThemeAlternates/`. No lane gate was run; no tool was
installed or upgraded; no pacman/yay/expac, sudo, systemctl, journalctl, loginctl,
hyprctl, walker, elephant, swaybg, omarchy-* or screenshot command was run. Host
versions are file reads of `/var/log/pacman.log` only. No git or jj write was made in
the lane; `git ls-remote` (network-only) was used once per candidate repository to test
whether a pin could exist. Tags: `[OBS]` read/measured bytes, `[INF]` inference,
`[UNK]` unresolved.

Question: can any secondary blog, video, ArchWiki or AUR source document P3 (Walker)
or P5 (themes/wallpapers/swaybg) at the C2 bar, or must it be rejected/queued? The
primary tag-pinned walker, omarchy and swaybg rows are sibling-owned; this seat only
screens the alternate families.

## 0. Verdict summary

- **23 source locations opened** (10 P3, 13 P5); **6 leads left unopened** (named in
  §1.3). Every retained source body has a curl receipt; the YouTube watch page is the
  one attempted body over the 1 MiB cap and was skipped unsaved.
- **11 proposed rows** in §2: **2 queued** (Hyprland wiki App-launchers listing;
  pinned AUR walker/elephant PKGBUILDs) and **9 rejected** (ssp.sh blog, GitHub
  discussion, AUR web pages, omarchytheme gallery, omarchy-wsl2 fork manual, YouTube
  video, ArchWiki Sway, ArchWiki Hyprland, omarchythemes.dev docs).
- **No candidate qualifies for C2 credit.** C2 requires `mined` + tier A + upstream
  `https` + the surface keyword. The only opened tier-A alternate is the Hyprland wiki
  listing, and it is a one-paragraph ecosystem blurb, not Walker’s contract; it is
  queued as corroboration only. Every other opened alternate is tier C or a
  fork-scoped B and is rejected. The route notes should cite the sibling primary rows.
- **The one version-bound alternate is the pinned AUR PKGBUILD pair**: package
  versions `2.17.2-1`/`2.22.1-1` map to upstream tags `v2.17.2`/`v2.22.1` with
  tarball sha256s. It is packaging provenance only, not host-install proof and not a
  C2 credit row.
- **ArchWiki has no `Walker` article**: `index.php?title=Walker&action=raw` returned
  HTTP 404 with a 0-byte body (empty-input sha256 `e3b0c442…`); the
  `Category:Application_launchers` raw page (478 B) lists translations and see-also
  links, no Walker member `[OBS]`.
- **The video is unreadable in-cap**: the watch page was 1,240,950 B (>1 MiB), so it
  was skipped and not saved; only the 811 B oEmbed metadata was retained. A title and
  author cannot carry a theme/wallpaper contract.

## 1. Candidate inventory and rulings

### 1.1 P3 — Walker / Elephant alternates

| # | candidate | kind/tier | version binding found | ruling |
|---|---|---|---|---|
| P3-1 | ssp.sh second-brain, “Walker Launcher” — Simon Späti, created 2025-10-20, updated 2026-04-27, self-labelled “growing” | community / C | No Walker or Elephant release token. The only version token is `v1.0` for the files-provider rename (`:1558`); the page says “comes with Omarchy out of the box” (`:1555`) but names no Omarchy version. The page’s own edit history shows it is mutable (`+184/−0 words` on 2026-04-27). | **REJECT** — a mutable personal note cannot bind a claim to walker 2.17.2. Proposed row A. |
| P3-2 | GitHub discussion #2835, “A comprihensive walker guide for omarchy” (omacom/omarchy) | community / C | No Walker/Elephant version in the guide’s own claims (`:791`). The only version token is a later commenter’s environment, “Using Omarchy 3.2.0” (`:8927`), which is not the guide’s binding. Posted Oct 2025; later comments are visible in the fetched page. | **REJECT** — user-generated, versionless guide; the commenter’s version cannot be inherited. Proposed row B. |
| P3-3 | AUR `walker` package page | community / C | `Package Details: walker 2.17.2-1` (`:380`); Last Updated 2026-10-08 06:46 UTC (`:519`). Version matches `pacman.log:2929` by value only. | **REJECT** — mutable user-submitted packaging metadata, no immutable revision, no upstream behavior. Class row C. |
| P3-4 | AUR `walker-bin` page | community / C | `walker-bin 2.17.2-1` (`:380`); Last Updated 2026-10-08 20:54 UTC (`:541-542`). | Same class as P3-3; folded into row C, no separate row. |
| P3-5 | AUR `elephant` page | community / C | `elephant 2.22.1-1` (`:380`); Last Updated 2026-09-24 06:34 UTC (`:519`). Version matches `pacman.log:3095` by value only. | Same class as P3-3; folded into row C, no separate row. |
| P3-6 | AUR `walker` PKGBUILD at pinned commit `a801f3cc3be208a8cd188b2072087af1a413aecf` | code / C | `pkgver=2.17.2` (`:4`), `source=("${url}/archive/refs/tags/v${pkgver}.tar.gz")` (`:14`), tarball sha256 `e50c6060…` (`:15`). Immutable commit URL. | **QUEUE** — packaging bridge to tag `v2.17.2`; not host-install proof, not a C2 credit row. Proposed row D. |
| P3-7 | AUR `elephant` PKGBUILD at pinned commit `fa4ae49703d0f1a2b47d3a93f0a373fb404aff39` | code / C | `pkgver=2.22.1` (`:4`), tag source (`:13`), tarball sha256 `3d1d0d4c…` (`:14`). Immutable commit URL. | Same row D (aggregate, S020/S059 precedent). |
| P3-8 | ArchWiki `Walker` article | — | Raw request returned HTTP 404, 0 bytes. | **NO ROW** — absence, not a source. Evidence below. |
| P3-9 | ArchWiki `Category:Application_launchers` | docs / C | Raw page is 478 B; lists translations and “See also” links only; no Walker member. | **NO ROW** — the category does not carry Walker; negative census, not a row. |
| P3-10 | Hyprland Wiki, “App launchers” §Walker | docs / A | Page modified 2026-08-26; no Walker release in the paragraph. It says Walker has “various built-in modules” and “can be run as a service for faster startups” (`:506-508`). | **QUEUE** — authoritative *Hyprland ecosystem listing*, not Walker’s config contract. Proposed row E; secondary corroboration only. |

### 1.2 P5 — theme / wallpaper / swaybg alternates

| # | candidate | kind/tier | version binding found | ruling |
|---|---|---|---|---|
| P5-1 | omarchytheme.com index (third-party gallery) | community / C | The only “Omarchy 3.6.0” tokens are inside fastfetch screenshot art (`:41`, `:79`, …), not a compatibility declaration. No theme-format contract, no revision. | Folded into row F (the Aetheria page is the concrete representative), no separate row. |
| P5-2 | omarchytheme.com, Aetheria theme page | community / C | Carries a theme release note “New, Omarchy 3.7+ (Plymouth) Unlock Screen” (`:144`) while its own fastfetch art shows Omarchy 3.6.0; gives install commands (`:146-149`) but never states the theme-format contract. | **REJECT** — community gallery; version note is ambiguous (feature label vs requirement) and no upstream anchor. Proposed row F. |
| P5-3 | omarchy-wsl2 fork manual, `05-theming.md` at `main` = `f90ccb1f427f10b1e2ff80738a89acd32d19b0cd` | docs / B | No Omarchy version. Documents `omarchy-theme-set` reloading “Hyprland, waybar and swaybg” (`:26`), a state path move (`:223`), and a theme fragment tree with `walker.css` (`:243`). Fork-specific helpers and env vars are the fork’s, not upstream’s. | **REJECT** — detailed but fork-scoped and unpinned to a release; cannot bind to host Omarchy v3.8.4. Proposed row G. |
| P5-4 | DHH, “Omarchy is out” (world.hey.com) | community / B | Maintainer launch post, 2025-06-26. Case-insensitive `theme` count over the body: **0**; it names Hyprland and Omarchy generally (`:53`). | **NO ROW** — out of P5 scope; no theming content to grade. |
| P5-5 | YouTube “Install Extra Wallpapers to Omarchy Themes” (OldJobobo) watch page | talk / C | Watch-page body 1,240,950 B > 1 MiB receipt cap; skipped unsaved. | **REJECT** — non-text content and no in-cap body. Proposed row H via oEmbed metadata. |
| P5-6 | YouTube oEmbed metadata for that video | talk / C | Title “Install Extra Wallpapers to Omarchy Themes”, author “OldJobobo”; 811 B. | Supports row H only; no content or version. |
| P5-7 | ArchWiki `Sway` §Wallpaper | docs / C | Revid 885570 (2026-09-12); no version pin. `:144`: sway’s wallpaper is “handled by a dedicated program”, with `swaybg` as the simplest example. | **REJECT** — community tier; documents sway’s own `output bg`/swaybg, not Omarchy’s theme chain or the host Hyprland surface. Proposed row I. |
| P5-8 | ArchWiki `Hyprland` §Desktop wallpaper | docs / C | Revid 887257 (2026-10-08); current Lua-era text; `:461` says Hyprland requires an external wallpaper application, using **hyprpaper** as the example (`:459-508`). | **REJECT** — community tier; hyprpaper/Lua-era, while the P5 chain is Omarchy theme state plus swaybg; no version binding. Proposed row J. |
| P5-9 | AUR `omarchy-theme-marketplace-git` page | community / C | `0.r0.g97ca8b7-1` (`:380`); Last Updated 2026-05-12 04:38 UTC (`:546`); description “Walker and Elephant theme marketplace for Omarchy”. | Same AUR web-page class as P3-3; folded into row C. |
| P5-10 | omarchythemes.dev, “field guide” theme documentation | community / B | Explicit version stamp: “Checked on Omarchy 4.0.0.alpha September 15, 2026” (docs root and colors page, body `:1`). This binds to a v4 alpha, not host v3.8.4; no tag or commit. | **REJECT** — version-mismatched third-party v4-alpha docs; useful only after a host move to Omarchy 4. Proposed row K. |
| P5-11 | omarchythemes.dev `/docs/colors` (colors.toml reference) | community / B | Same v4-alpha stamp; documents palette keys, derivation and template placeholders. | Same row K; folded into P5-10. |
| P5-12 | omarchypulse.com, “Making your own theme” | community / C | No version token in the extracted text; page carries the Omarchy 3 manual navigation and links omarchy.org/themes and omarchy-site (`:15`). [INF] third-party copy of the manual, not a distinct source. | **NO ROW** — duplicate class of the sibling-owned primary manual; no revision or version binding. |
| P5-13 | draculatheme.com/omarchy (third-party theme page) | community / C | No version token; install command `omarchy-theme-install https://github.com/catlee/omarchy-dracula-theme` (`:3-4`); theme-specific. | **NO ROW** — same theme-page class as P5-2; no theme-format contract or version; folded into row F’s class. |

### 1.3 Leads identified but not opened (not evidence)

1. `walkerlauncher.com` official docs — primary, sibling-owned (`SrcWalkerDocsSite`).
2. Hyprland wiki archived App-Launchers pages v0.47/v0.49/v0.51/v0.53 — version-
   mismatched ecosystem duplicates of P3-10.
3. `imbypass/walker` GitHub fork — fork surrogate, not upstream.
4. `omarchy.org/manual/themes` and `/manual/making-your-own-theme/` — primary manual,
   sibling-owned (`SrcOmarchyManualThemes`).
5. `basecamp/omarchy` `docs/theming.md` at tag `quattro` — primary upstream, sibling-
   owned (`SrcOmarchyThemeLayout` / `SrcOmarchyThemeHooks`).
6. `omarchy.org/themes/` extra-themes page — primary, sibling-owned.

## 2. Proposed SOURCES rows (`S0xx-pending`; L1 assigns ids)

Paste-ready, one line per row. Pending ids are placeholders: per
`SourcesRowShape.md` §1.2, `S0xx-pending` fails the `S\d{3,}` census and earns no C2
credit, so L1 must substitute real S072-S099 ids in the rows and the note heads in the
same change. All rows use lowercase `https://`; no cell contains a literal pipe.

```text
| S0xx-pending | ssp.sh second-brain — Walker Launcher note — https://www.ssp.sh/brain/walker-launcher/ | community | C | personal Omarchy Walker usage note, mutable growing page; no Walker/Elephant version pin | Updated 2026-04-27 (:748-749, self-labelled "growing"); :1555 and :1558; raw sha256 12c4e5b1c247097a6accfafd224adc868dc17ce21a3c87993d4497676c4ab20b (48,239 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#walker-ssp-blog, fetched 2026-10-20T15:41:16Z) | REJECTED: mutable personal second-brain note with no Walker/Elephant release token — the only version token is v1.0 for a provider rename — so its usage claims cannot bind to walker 2.17.2; flip: a dated, version-pinned rewrite with per-claim upstream tag anchors and a stable revision | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | GitHub discussion 2835 — A comprihensive walker guide for omarchy — https://github.com/basecamp/omarchy/discussions/2835 | community | C | user-generated Walker-in-Omarchy usage guide (posted Oct 2025; later comments visible); no Walker/Elephant release binding | page title :111; guide scope :791; later commenter's "Omarchy 3.2.0" :8927; final_url github.com/omacom/omarchy/discussions/2835; raw sha256 0f2ce2b21b34688d36241fa35e1ba50bffe54a6cb5885f67e71f8f4bb27e8bc9 (903,486 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#gh-omarchy-discussion-2835, fetched 2026-10-20T15:42:25Z) | REJECTED: user-generated guide with no Walker/Elephant version in its own claims; the only version token is a later commenter's environment, so it cannot bind to walker 2.17.2; flip: a maintainer-owned, release-pinned guide with per-claim tag anchors | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | AUR package pages — walker 2.17.2-1, walker-bin 2.17.2-1, elephant 2.22.1-1, omarchy-theme-marketplace-git 0.r0.g97ca8b7-1 — https://aur.archlinux.org/packages/walker | community | C | mutating AUR web metadata for Walker/Elephant/theme-marketplace packaging; not upstream contract and not host-install proof | walker :380 and :519 (2026-10-08 06:46 UTC; sha256 df43afc627d00b914ea50a282f865526f74bf6b980598ef2073bd3c9716c4ebf, 32,333 B); walker-bin :380 and :541-542 (2026-10-08 20:54 UTC; sha256 a36801745ecffa83abd26cf441b1be2c6320a1f2181d1ad7e8fccb1b5c3a08f8, 38,045 B); elephant :380 and :519 (2026-09-24 06:34 UTC; sha256 977a5657b83729c876ea4130d194f459e6e8dc81d2d6bb27e6fe6e2d061522b3, 20,937 B); marketplace :380 and :546 (2026-05-12 04:38 UTC; sha256 70f5cc2dc8323be11b993bcd753269da44e4ddf3b61f7d2e896beaaf9c7641e6, 23,527 B); all HTTP 200; receipts .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#aur-walker, #aur-walker-bin, #aur-elephant, #aur-omarchy-theme-marketplace, fetched 2026-10-20T15:41:16Z-15:41:18Z | REJECTED: AUR package pages are mutable user-submitted packaging metadata with no immutable revision; the walker/elephant version strings match pacman.log only by value, prove no host package origin and teach no upstream behavior; flip: cite pinned AUR PKGBUILD commits plus upstream tags, scoped to packaging only | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | Hyprland Wiki — App launchers §Walker — https://wiki.hypr.land/Useful-Utilities/App-Launchers/ | docs | A | current Hyprland wiki's one-paragraph Walker ecosystem listing (modules, service startup); not Walker's config contract | §Walker; page modified 2026-08-26; raw sha256 5d184b58f1e67233648f219124ffa2dcf76b765cc05f7ef406b776430d83fb5c (244,870 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#hyprwiki-app-launchers, fetched 2026-10-20T15:41:18Z); :506-508 | authoritative ecosystem listing names Walker's modules and service mode; use as secondary corroboration only, never as sole P3 support | queued | 2026-10-20 | 90d | — |
| S0xx-pending | AUR walker and elephant PKGBUILDs at pinned commits — https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=walker&id=a801f3cc3be208a8cd188b2072087af1a413aecf | code | C | AUR packaging bridge: pkgver 2.17.2-1 and 2.22.1-1 to upstream tags v2.17.2 and v2.22.1 with tarball digests; not host-install proof | walker PKGBUILD:4,14-15 at a801f3cc3be208a8cd188b2072087af1a413aecf; elephant PKGBUILD:4,13-14 at fa4ae49703d0f1a2b47d3a93f0a373fb404aff39; raw sha256 713a9009b875a57a03e1617084fae474500893998a88a1514bfc2919e4f2e314 (2,231 B) and 9beb80d4ecceb0f9ffd5045c8cea6a4f6fdcc3240bdc7e064412d06cede9f932 (746 B); HTTP 200; receipts .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#aur-walker-pkgbuild-pinned, #aur-elephant-pkgbuild-pinned, fetched 2026-10-20T15:44:24Z-15:44:25Z | pinned packaging metadata maps package versions to upstream tags and sha256 tarballs; package origin and binary equivalence remain [UNK] and it is not a C2 credit row | queued | 2026-10-20 | on-change | — |
| S0xx-pending | Omarchy Themes marketplace — Aetheria theme page — https://omarchytheme.com/themes/aetheria/ | community | C | third-party theme index/installer page; palette, install commands and a theme compatibility note, no theme-system contract | Aetheria :144-149; raw sha256 a84629d6ab294f62a6b910bb98ebad8aeac54cd5b5c559128ddc5113db779e78 (36,501 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#omarchytheme-aetheria, fetched 2026-10-20T15:41:17Z); index raw sha256 3f39f63147517846f5122395b0af9de0185ae23505e16b42319fcf81c66fc6aa (300,291 B; receipt #omarchytheme-home) | REJECTED: community theme gallery; its release note says "Omarchy 3.7+" while its own screenshot shows Omarchy 3.6.0, and it never states the theme-format contract or an upstream revision; flip: a tag-pinned theme repo plus the upstream theme-format document proving compatibility | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | omarchy-wsl2 fork manual — 05 Theming — https://raw.githubusercontent.com/clarenceb/omarchy-wsl2/f90ccb1f427f10b1e2ff80738a89acd32d19b0cd/docs/05-theming.md | docs | B | third-party WSL fork's theme procedure and fragment inventory (theme-set reload targets, state path, walker.css); fork-specific | :26, :223, :243 at main f90ccb1f427f10b1e2ff80738a89acd32d19b0cd; raw sha256 f55e239d2b7ef8f26476d5245109f1dfd2158420af43c18c83d5b97b1f1d8439 (8,033 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#omarchy-wsl2-theming-pinned, fetched 2026-10-20T15:46:32Z) | REJECTED: detailed but fork-specific and unpinned to a fork release; its theme-set and state-path claims name no Omarchy version and the helper/env vars are the fork's, so it cannot bind to host v3.8.4; flip: pin a tagged fork release and scope to the WSL fork, or use upstream maintainer docs | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | YouTube — Install Extra Wallpapers to Omarchy Themes (OldJobobo) — https://www.youtube.com/watch?v=-mNHs8wZSq4 | talk | C | video metadata only; watch page exceeds the 1 MiB receipt cap | oEmbed JSON line 1 title/author; sha256 25ccb34024e6680afa1dabb74f1a86e7670504d4292c492f5d54bfd327f040a6 (811 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#yt-oembed-extra-wallpapers, fetched 2026-10-20T15:42:25Z); watch page 1,240,950 B skipped and not saved | REJECTED: video content is not text and the watch page exceeds the 1 MiB receipt cap; oEmbed metadata carries no theme/wallpaper contract or version; flip: a published transcript or companion write-up pinned to a version | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | ArchWiki — Sway §Wallpaper — https://wiki.archlinux.org/title/Sway | docs | C | Arch-wiki's sway wallpaper example using swaybg; not the host compositor or Omarchy theme chain | §Wallpaper; revid 885570 (2026-09-12); raw sha256 e02098d5996b340aa6b2b1ecec527102b572bcda0044d43e4660c7f542b6155d (40,207 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#archwiki-sway-raw, fetched 2026-10-20T15:41:18Z); :144 | REJECTED: community tier cannot support a C2-covered entry; it documents sway's own output bg plus optional swaybg, not Omarchy's theme chain or the host Hyprland surface, and carries no version pin; flip: an oldid-pinned tier-C cross-check only if the rubric admits tier C, or upstream swaybg docs | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | ArchWiki — Hyprland §Desktop wallpaper — https://wiki.archlinux.org/title/Hyprland | docs | C | Arch-wiki's current Hyprland wallpaper example (hyprpaper, Lua era); not Omarchy's theme chain | §Desktop wallpaper; revid 887257 (2026-10-08); raw sha256 7f6b2e4352b134576c242fa644d2af4c93e0b00fd13f3e834a77bfef3a90f12b (36,293 B; HTTP 200; receipt .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#archwiki-hyprland-raw, fetched 2026-10-20T15:43:04Z); :459-508 | REJECTED: community tier; current text is Lua-era and uses hyprpaper, while the P5 chain is Omarchy theme state plus swaybg; no version binding to host v3.8.4; flip: an oldid-pinned tier-C cross-check only if the rubric admits tier C | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | Omarchy Themes docs — field guide and colors.toml reference — https://omarchythemes.dev/docs | community | B | third-party theme documentation checked on Omarchy 4.0.0.alpha (2026-09-15), not the host v3.8.4; 9 guides including colors.toml and templates | body :1 (single-line HTML) and /docs/colors :1; version stamp "Checked on Omarchy 4.0.0.alpha September 15, 2026"; raw sha256 57b5c9e30899d769f7e44daa1545188ba442f1a897c03a2a3ac8727ada4e6191 (46,940 B) and 5497340b232b7b18eea4fedddbaedaca8652d79edec7c01fda0c2991f82a19bc (55,181 B); HTTP 200; receipts .ufo/waves/round-18/fetch/SrcThemeAlternates/receipts.jsonl#omarchythemes-docs, #omarchythemes-colors, fetched 2026-10-20T15:52:57Z | REJECTED: version-mismatched — the site self-identifies as checked on Omarchy 4.0.0.alpha while the host checkout is v3.8.4; its theme-format claims cannot bind to the host, and it is third-party; flip: recheck when the host moves to Omarchy 4, citing this site's own version stamp and a stable revision | rejected | 2026-10-20 | 90d | — |
```

## 3. Quote / receipt ledger (gate material)

Each line names the body, line anchor, ≤25-word quote, sha256, byte count, HTTP status
and receipt body. Quotes are rendered text from the raw bodies; HTML entities are
normalised only in this transcription, never in the stored body.

| proposed row | body:line | quote (≤25 words) | sha256 / bytes / status / fetched |
|---|---|---|---|
| A | walker-ssp-blog:1555 | “It’s rewritten in Rust and comes with Omarchy out of the box.” (11) | 12c4e5b1c247097a6accfafd224adc868dc17ce21a3c87993d4497676c4ab20b / 48,239 / 200 / 2026-10-20T15:41:16Z |
| B | gh-omarchy-discussion-2835:791 | “This guide documents everything I discovered, hoping it will be helpful for others” (13) | 0f2ce2b21b34688d36241fa35e1ba50bffe54a6cb5885f67e71f8f4bb27e8bc9 / 903,486 / 200 / 2026-10-20T15:42:25Z |
| C | aur-walker:380 | “Package Details: walker 2.17.2-1” (5) | df43afc627d00b914ea50a282f865526f74bf6b980598ef2073bd3c9716c4ebf / 32,333 / 200 / 2026-10-20T15:41:16Z |
| C | aur-walker-bin:380 | “Package Details: walker-bin 2.17.2-1” (5) | a36801745ecffa83abd26cf441b1be2c6320a1f2181d1ad7e8fccb1b5c3a08f8 / 38,045 / 200 / 2026-10-20T15:41:16Z |
| C | aur-elephant:380 | “Package Details: elephant 2.22.1-1” (5) | 977a5657b83729c876ea4130d194f459e6e8dc81d2d6bb27e6fe6e2d061522b3 / 20,937 / 200 / 2026-10-20T15:41:16Z |
| C | aur-omarchy-theme-marketplace:380 | “Package Details: omarchy-theme-marketplace-git 0.r0.g97ca8b7-1” (5) | 70f5cc2dc8323be11b993bcd753269da44e4ddf3b61f7d2e896beaaf9c7641e6 / 23,527 / 200 / 2026-10-20T15:41:18Z |
| D | aur-walker-pkgbuild-pinned:4 | “pkgver=2.17.2” (1) | 713a9009b875a57a03e1617084fae474500893998a88a1514bfc2919e4f2e314 / 2,231 / 200 / 2026-10-20T15:44:24Z |
| D | aur-elephant-pkgbuild-pinned:4 | “pkgver=2.22.1” (1) | 9beb80d4ecceb0f9ffd5045c8cea6a4f6fdcc3240bdc7e064412d06cede9f932 / 746 / 200 / 2026-10-20T15:44:25Z |
| E | hyprwiki-app-launchers:506 | “Walker is an extensible Wayland-native runner with various built-in modules” (12) | 5d184b58f1e67233648f219124ffa2dcf76b765cc05f7ef406b776430d83fb5c / 244,870 / 200 / 2026-10-20T15:41:18Z |
| F | omarchytheme-aetheria:144 | “New, Omarchy 3.7+ (Plymouth) Unlock Screen” (6) | a84629d6ab294f62a6b910bb98ebad8aeac54cd5b5c559128ddc5113db779e78 / 36,501 / 200 / 2026-10-20T15:41:17Z |
| G | omarchy-wsl2-theming-pinned:26 | “omarchy-theme-set normally reloads Hyprland, waybar and swaybg” (7) | f55e239d2b7ef8f26476d5245109f1dfd2158420af43c18c83d5b97b1f1d8439 / 8,033 / 200 / 2026-10-20T15:46:32Z |
| H | yt-oembed-extra-wallpapers:1 | “Install Extra Wallpapers to Omarchy Themes” (7) | 25ccb34024e6680afa1dabb74f1a86e7670504d4292c492f5d54bfd327f040a6 / 811 / 200 / 2026-10-20T15:42:25Z |
| I | archwiki-sway-raw:144 | “The displaying of a wallpaper in sway is handled by a dedicated program.” (14) | e02098d5996b340aa6b2b1ecec527102b572bcda0044d43e4660c7f542b6155d / 40,207 / 200 / 2026-10-20T15:41:18Z |
| J | archwiki-hyprland-raw:461 | “Hyprland requires a Wayland-compatible external application to manage desktop wallpapers.” (11) | 7f6b2e4352b134576c242fa644d2af4c93e0b00fd13f3e834a77bfef3a90f12b / 36,293 / 200 / 2026-10-20T15:43:04Z |
| K | omarchythemes-docs:1 | “Checked on Omarchy 4.0.0.alpha September 15, 2026” (7) | 57b5c9e30899d769f7e44daa1545188ba442f1a897c03a2a3ac8727ada4e6191 / 46,940 / 200 / 2026-10-20T15:52:57Z |

Receipt-binding check this seat ran: every line above was matched against its
`receipts.jsonl` entry and the body bytes; `sha256(body) == receipt.sha256`,
`len(body) == receipt.bytes`, `receipt.http_status == 200` for all 15 lines. The
404 Walker body is deliberately excluded from the ledger (0 bytes, empty-input digest;
it may only be cited as absence).

## 4. Negative findings and host facts

- **ArchWiki P3 absence `[OBS]`.** `https://wiki.archlinux.org/index.php?title=Walker&action=raw`
  returned HTTP 404 with 0 bytes (receipt `#archwiki-walker-raw`; sha256 is the empty-
  input digest `e3b0c442…`). `Category:Application_launchers` raw is 478 B and lists
  translations plus “See also” (`archwiki-app-launchers-raw`); no Walker member. There
  is therefore no ArchWiki Walker page to reject or queue — only a negative census.
- **The watch page is unreadable in-cap `[OBS]`.** `https://www.youtube.com/watch?v=-mNHs8wZSq4`
  returned 1,240,950 bytes, above the 1 MiB fetch-receipt cap; it was not saved and has
  no receipt. Only the 811 B oEmbed JSON is retained. The title/author support the
  rejected row, never a content claim.
- **DHH post is out of scope `[OBS]`.** Case-insensitive `theme` count in the body is
  0; the post names Omarchy and Hyprland generally (`dhh-omarchy-out:53`). No row.
- **Host versions are file-read facts `[OBS]`.** `/var/log/pacman.log:2929` records
  `upgraded walker (2.17.0-1 -> 2.17.2-1)`; `:3095` records
  `upgraded elephant (2.21.0-1 -> 2.22.1-1)`. The AUR pages show the target versions
  by value; they do **not** show that the host package came from AUR rather than an
  official repository, and no binary was inspected. `[UNK]` package origin and byte
  equivalence.
- **No package out-of-date flag was observed on the fetched AUR pages.** In the walker
  page the only “Out of Date” strings are the search form’s label/selector
  (`aur-walker:327-329`), not a package flag `[OBS]`; the same form markup appears in
  the other three pages. Absence of a flag is not a freshness claim.
- **Aetheria’s version note is ambiguous `[OBS]`.** `:144` reads “New, Omarchy 3.7+
  (Plymouth) Unlock Screen” while the same page’s fastfetch art shows Omarchy 3.6.0.
  The page never says whether 3.7+ is a requirement, a feature label, or a theme
  release stream. That ambiguity is part of the rejection, not a hidden compatibility
  claim.
- **The clearest new P5 version stamp points away from the host `[OBS]`.**
  omarchythemes.dev says “Checked on Omarchy 4.0.0.alpha September 15, 2026” on both
  the docs root and the colors page. The host checkout is Omarchy v3.8.4, so a
  v4-alpha theme-format document is a future-version lead, not a host-v3 source; that
  is why row K is rejected despite being the most version-explicit alternate opened.
- **Two new P5 pages add no source and no row `[OBS]`.** omarchypulse.com reproduces
  the Omarchy 3 manual navigation and links the upstream extra-themes page and
  omarchy-site repo (`:15`); it has no version token or revision `[INF] copy`.
  draculatheme.com/omarchy is a theme-specific install page with the same
  `omarchy-theme-install` command and no version (`:3-4`). They are accounted in §1.2
  as P5-12/P5-13 and deliberately not rowed.
- **Pins tested read-only `[OBS]`.** AUR walker `refs/heads/master` =
  `a801f3cc3be208a8cd188b2072087af1a413aecf`; AUR elephant master =
  `fa4ae49703d0f1a2b47d3a93f0a373fb404aff39`; omarchy-wsl2 main =
  `f90ccb1f427f10b1e2ff80738a89acd32d19b0cd`; Aetheria tag `aetheria-0.1` =
  `1f9093e9be4d7d24fba26310a6de753d45b2a522`; omarchy-theme-marketplace tag
  `v0.1.0` peeled commit = `97ca8b7288e5f6dd0eb5235d78857a6c901fe9b8`. The pinned PKGBUILD URLs
  returned byte-identical bodies to the unpinned `h=walker`/`h=elephant` fetches.
- **No new W04 is expected from these rows.** None of the first URLs in §2 matches an
  existing registry URL or another proposed row’s first URL. The queued Hyprland wiki
  row and the rejected ArchWiki rows are distinct hosts/paths from the sibling primary
  rows. Pending ids still fail the census until L1 substitutes them.

## 5. Search-log draft for L1 (`SOURCES.md` rule 5)

> From the `theme-alternates` seat (2026-10-20): question — which secondary blog,
> video, ArchWiki or AUR sources can document P3/P5 without duplicating the primary
> tag rows or inflating tier? Where: `web_search` seeds for omarchy theming, walker
> config, ArchWiki and AUR, then direct opens of every canonical page. Identified 29
> candidate locations; opened 23 (10 P3, 13 P5); proposed 11 rows (2 queued, 9
> rejected); 6 leads left unopened (official walker docs, archived Hypr wiki versions,
> an imbypass fork, the omarchy manual/themes pages and the quattro docs theming file —
> all primary or version-mismatched, sibling-owned). Excluded without a row: the
> ArchWiki Walker 404 and its category page (no Walker member), the DHH launch post
> (0 theme tokens), the omarchytheme index (same class as its Aetheria page), the
> omarchypulse manual copy (duplicate of the primary manual), the Dracula theme page
> (same class as Aetheria), and the AUR walker-bin/elephant/marketplace pages (folded
> into the AUR web-page class row). The YouTube watch page exceeded the 1 MiB receipt
> cap and is represented only by its oEmbed metadata. Stop: every named alternate
> family has a tier/version verdict; further opens would not change either.

## 6. Boundaries and remaining unknowns

- This report does not admit, mine, or edit any row; L1 owns ids, statuses, `used-by`
  edits and the final C2 note heads. The queued rows are **not** credited by the P3/P5
  notes, and the rejected rows must never appear in a note’s `source:` line.
- `[UNK]` host package origin (AUR vs official repository) and installed-binary
  equivalence; no pacman query or binary inspection was permitted.
- `[UNK]` actual video content; only its metadata was opened.
- `[UNK]` whether “Omarchy 3.7+” on the Aetheria page is a requirement or a release
  label; the rejection does not depend on resolving it.
- `[UNK]` whether L1 mines the queued Hyprland wiki or PKGBUILD rows; their scopes are
  deliberately secondary/packaging-only.
- `[INF]` the ArchWiki raw bodies correspond to the API-reported current revisions
  (Sway 885570, 2026-09-12; Hyprland 887257, 2026-10-08). An `oldid=` raw replay was
  attempted for Sway and returned a bot-challenge page, not article text; that
  challenge body was removed and is not relied on. The current-revision API response
  and the raw-body receipt are the retained evidence.
- `[INF]` the Hyprland wiki page was current at fetch time: its own modified timestamp
  is 2026-08-26 and the raw body was fetched 2026-10-20.
- No fetch used auth, cookies, session/private URLs or a non-curl client; the tool line
  recorded in each receipt is `curl 8.23.0 (x86_64-pc-linux-gnu) …`.
- Files written by this seat: this report and
  `.ufo/waves/round-18/fetch/SrcThemeAlternates/` (28 receipt lines for 28 distinct
  URLs; 28 bodies, one 404 empty body; the >1 MiB video body is absent by contract).
