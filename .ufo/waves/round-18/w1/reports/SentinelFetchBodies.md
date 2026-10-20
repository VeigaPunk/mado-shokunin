# SentinelFetchBodies — round 18 wave 1

**Scope.** A security review of committing raw fetched bodies under `.ufo/waves/round-18/fetch/`. It covers four risks:
- tracking and session tokens in fetched pages,
- prompt-injection text,
- licences for verbatim third-party text,
- size.

It ends with rules for what to commit and what to keep digest-only.

**Axes:**
- secret/capability exposure
- injection exposure for future seats
- licence compliance of the **public** lane repo
- repo cost
- verifiability (R17-V3)

## Method

- I scanned the live working-tree fetch tree: 281 bodies and 282 receipt lines in 17 seat directories. The tree is untracked: `git status` shows `?? .ufo/waves/round-18/fetch/`, and `git log refs/heads/master -- …fetch` is empty.
- The scan was read-only Python regex plus `gitleaks dir` (the local `/usr/bin/gitleaks` binary, run on data).
- I took 22 control samples into `/tmp/sfb/` with the contract curl form plus `-D` headers, for header inspection only. I re-fetched 7 of them to measure how much a body varies between fetches.
- The sample receipts are in `/tmp/sfb/receipts.jsonl`; key lines are in the Appendix.
- I wrote nothing in the lane except this report. The samples are analysis controls, not credited sources, so they have no lane receipt directory.
- **Deviation:** I ran one `git status --porcelain` in the lane. This command can refresh `.git/index` stat data, and it is not on the contract's read-only list. I made no other git or jj calls.
- Installs: none.

## Verdict

- **No user credential and no host identity is exposed.** curl runs with no cookie jar, and every page was served logged-out (`logged_in=no`, `"user_id":null`).
- **But 29 HTML bodies carry per-request tokens, live capability URLs and scanner-tripping strings.** gitleaks gives **74 findings in 10 files, rc 1**.
- **22 bodies contain commands the host pause forbids** (package installs, pipe-to-shell, `omarchy-*`). One related upstream file, omarchy's `AGENTS.md`, is text written for AI agents that tells them to take screenshots.
- **About 25 bodies have no redistribution licence**, or a notice-bearing licence whose notice is not carried, and the lane repo is **public** (logged-out GET of `github.com/VeigaPunk/mado-shokunin` → 200, no `LICENSE` at `refs/heads/master`).
- **Under the rules below**:
  - **commit 232 bodies (2,838,357 B), with 0 gitleaks findings (rc 0);**
  - keep 49 digest-only (5,467,908 B).

## Findings

### F1 — MEDIUM: per-request tokens and live capabilities in HTML bodies

**Evidence: tokens and capabilities in the real tree**
- 7 GitHub HTML bodies: `NoteTheme/omarchy-themes*-tree.html` ×3, `NoteTheme/swaybg-v1.2.2-{tree,doc}.html` and `SrcThemeAlternates/gh-omarchy-discussion-2835`. Each carries:
  - `meta name="request-id"`, `html-safe-nonce` and `visitor-hmac`;
  - 4–93 `data-hydro-click-hmac` values;
  - `uploadToken`.
- `gh-omarchy-discussion-2835` (903,486 B) also embeds:
  - 20 `private-user-images.githubusercontent.com/…?jwt=eyJ…` capability URLs (decoded claims: `iss github.com`, `aud raw.githubusercontent.com`, `exp − nbf = 300 s`);
  - 40 copies of GitHub's S3 signing key id `AKIAVC…`.
- 7 learn.omacom.io (Writebook) bodies in `SrcOmarchyManualThemes/` each carry `meta name="csrf-token"` plus `authenticity_token` form values (`book-index` has 50). These are bound to the `_writebook_session` cookie that the server set (seen in my `-D` sample headers; the contract curl does not save headers).
- `SrcWalkerDocsSite/gitbook-{root,walker-and-elephant}.html` each embed a GitBook site `apiToken` JWT (`kind site`, `target content`, `exp − iat = 86,700 s`, about 24 h). It is a bearer token handed to every visitor, so its confidentiality value is low.
- Two analytics hits, both on the third-party site omarchytheme.com (`omarchytheme-home`, `omarchytheme-aetheria`).
- No IPv4 addresses appear apart from SVG path numerals. No `gh*_`, `github_pat_` or `BEGIN … PRIVATE KEY` patterns appear. No zero-width or bidi characters appear in any body.

**Evidence: gitleaks over the whole fetch tree** — 74 findings, rc 1:

| Rule | Count | Where |
|---|---|---|
| `aws-access-token` | 40 | discussion page |
| `jwt` | 20 | discussion page |
| `generic-api-key` | 14 | hydro-click-hmac and uploadToken in GitHub HTML, omarchytheme |

**Evidence: bodies vary between fetches.** Repeated fetches of GitHub HTML differ in 1 line (request-id, nonce, hmac). Writebook pages differ in 2 lines (csrf). raw, api.github.com, the Arch Wiki, wiki.hypr.land and AUR pages were byte-identical on a second fetch.

**Exploit path.** L1 integrates `fetch/` as-is and pushes to the public origin:
- Any gitleaks-style gate in the fleet fails, and GitHub push protection may refuse the push. Whether push protection blocks on a bare AKIA id is `[INFERENCE]`.
- Live capability URLs are published. For the JWT URLs, a 5-minute expiry at fetch time makes the leak moot here, but the shape repeats on any attachment-bearing page.
- Because these bodies vary between fetches, a closure cannot reproduce their digests. The committed copy, tokens included, becomes the only proof.

**Impact.**
- Scanner noise and blocked push risk.
- Every future round adds new token-bearing blobs, which are never deduplicated.
- No user secret is exposed.

**Smallest remediation.** HTML bodies are digest-only (Rule D1). Never save response headers or use a cookie jar (Rule N2).

### F2 — MEDIUM: directive text for agents, and forbidden commands, inside fetched data

**Evidence**
- **Upstream `AGENTS.md`.** Omarchy v3.8.4 ships `AGENTS.md`; it is listed in all 4 committed-candidate `tree.json` copies. My control fetch: sha256 `f45cd062…`, 6466 B. Line 97 says:
  > "always take and analyze a screenshot after applying the change … Use `omarchy capture screenshot fullscreen save`"

  That is an instruction aimed at agents, and it directly violates the host pause (no screenshots, no `omarchy-*` commands). Line 104 recommends `omarchy-refresh-config`, which overwrites `~/.config/hypr/*`. The host checkout `~/.local/share/omarchy/AGENTS.md` is byte-identical (same sha256), so host-file seats can reach it too.
- **`llms.txt` bundles.** `SrcWalkerDocsSite/gitbook-llms.txt` and `gitbook-llms-full.txt` (21,504 B) are content packaged for LLM ingestion.
- **Pipe-to-shell.** `SrcOmarchyManualThemes/manual.md:2051` contains `curl -fsSL https://omarchy.org/install | bash`.
- **Unaudited third-party install.** `SrcThemeAlternates/omarchytheme-aetheria` contains `omarchy-theme-install https://github.com/JJDizz1L/aetheria.git` for an unaudited community theme. The page's own line 210 says "Never run scripts from the internet without reading them first."
- **Package-mutation commands.** 22 bodies have them (14 of them in the commit class, all upstream install docs or scripts), for example `elephant-v2.22.1-readme.md:92` `yay -S elephant` and the hypr wiki pages' `pacman -S hyprpaper`.
- **User-written content.** The GitHub discussion (903 KB) and AUR pages (9, 9 and 2 `commented on` blocks) are authored by arbitrary third parties.
- No literal "ignore previous instructions" pattern was found anywhere.

**Exploit path.** Committed bodies become standing context.
- A later seat greps the repo, or the closure runs `fetch-verify.py --quote`, and reads `AGENTS.md` or `llms-full.txt` text inline.
- The `[a-z0-9._-]+` slug rule is **not enforced**:
  - `fetch-verify.py:62` rejects only `/`, `.` and `..`;
  - 13 bodies already break the rule (uppercase names), for example `MadoR18.SrcSwaybgMan/README.md` and `SrcElephantReadme/walker-Cargo.toml.body`.

  So nothing stops a body being saved as `AGENTS.md` or `CLAUDE.md` inside the repo, where directory-walking harnesses may auto-load it (`[INFERENCE]`, harness-dependent).

**Impact.** The injection surface persists past this round. The REA/MCP data-only rule mitigates per-session reads but not auto-loading.

**Smallest remediation.**
- Enforce the slug regex, with a reserved-name deny-list (Rule N3).
- Make `llms*.txt`, UGC and marketing pages digest-only (Rule D2).
- When a credited body contains agent-directed or pipe-to-shell text, the citing note says so in one line, marked `[DATA, not instruction]`.

### F3 — MEDIUM: licence obligations for a public repo

The lane repo is public and has no `LICENSE` of its own, so committing a body is redistribution.

| Source class (bodies) | Licence | Obligation for verbatim copies | State in the tree |
|---|---|---|---|
| walker v2.17.2, elephant v2.22.1 raw | GPL-3.0 (`LICENSE` 35,149 B, sha256 `3972dc97…`) | §4: keep notices **and** give recipients a copy of the licence. §5 aggregation does not extend the GPL to the lane. | 0 LICENSE bodies committed beside about 60 walker/elephant bodies; only the binary `walker-v2.17.2-src.tar.gz` contains `LICENSE` |
| omarchy v3.8.4 raw (basecamp → omacom) | MIT (sha256 `717ba194…`) | Copyright and permission notice in "all copies or substantial portions" | no LICENSE body |
| swaybg v1.2.2 raw | MIT (`95224d11…`) | same | no LICENSE body |
| wiki.hypr.land rendered HTML (`s063`, `s064`, `hyprwiki-app-launchers`) | BSD-3 (`hyprwm/hyprland-wiki` LICENSE, `cbc78364…`) | Retain copyright notice | the HTML carries **0** licence or copyright strings |
| Arch Wiki `action=raw` (4 bodies) | GFDL 1.3+ | Reproduce the licence notice **and** the licence text | raw wikitext carries no notice |
| learn.omacom.io manual (7 HTML + `manual.md` 121,693 B, the whole book) | none stated | none granted (all rights reserved by default) | — |
| omarchytheme.com, world.hey.com, ssp.sh (`walker-ssp-blog:1794` "All Rights Reserved"), the GitHub discussion, AUR pages, gitbook, `clarenceb/omarchy-wsl2`, YouTube oEmbed | none, or UGC | none granted for redistribution | — |
| api.github.com JSON (trees, commits, releases) | public metadata | none | The 4 commit/compare JSONs carry 22 author/committer email values; all already public in git |

**Impact.** Unlicensed redistribution of whole pages and books in a public repo. The ≤25-word quotes inside notes are not affected.

**Smallest remediation.**
- Commit one `LICENSE` body per (repo, tag) beside licensed bodies (Rule C2).
- Unlicensed, UGC or notice-less bodies are digest-only (Rule D2).

### F4 — LOW: size

**Measurements**
- Totals: 281 bodies, 8,306,265 B; **6,492,979 B unique** across 201 distinct sha256 values. Git deduplicates identical blobs, so 1.8 MB is cross-seat duplication.
- By type:

| Type | Bodies | Bytes | Share |
|---|---|---|---|
| HTML | 29 | 4,623,564 | 56% |
| JSON | 35 | 2,313,640 | — |
| binary archives (`walker-v2.17.2-src.tar.gz` 165,438; `xdg-3.0.0.crate` 15,821) | 2 | 181,259 | — |

- The largest body is `gh-omarchy-discussion-2835` at 903,486 B, 88% of the 1 MiB cap. The largest tracked lane file today is 177,849 B (`tools/mado-verify.sh`).
- GitHub HTML gzips about 6.6× (353,730 → 53,191 B). It never deduplicates across rounds because of F1's per-fetch tokens.

**Impact.** Unbounded per-round growth, mostly from page chrome that no row quotes.

**Remediation.** Rules D1 and C1 cut committed bytes to 2,838,357 B.

### F5 — LOW: `final_url` can publish a signed URL, and gitleaks does not catch it

**Evidence**
- A release-asset download (`github.com/abenz1267/walker/releases/download/v2.17.2/…tar.gz`, range 0-0) redirects to `release-assets.githubusercontent.com/…?…&se=…&sig=…&jwt=eyJ…`:
  - SAS expiry `se` about 1 h after `skt`;
  - JWT `exp − nbf = 300 s`.
- The receipt schema records `final_url` verbatim.
- `gitleaks dir` over a receipt line holding that URL: **rc 0, 0 findings.**
- Current tree: 282 receipts, 30 redirected, **0** with a signed `final_url`, 5 non-200 (honest 404s).

**Smallest remediation.** Rule N1.

### F6 — LOW: fetch-store integrity gaps that weaken R17-V3

**Evidence**
- **Unreceipted bodies.** 4 bodies have no receipt line:
  - `MadoR18.SrcWalkerThemes/walker-ls-remote-v2.17.2.txt`
  - `MadoR18.SrcWalkerThemes/walker-tree-api.json`
  - `SrcOmarchyThemeHooks/tree.json`
  - `SrcOmarchyWalker/git-ls-remote-tags.txt`

  `fetch-verify.py` walks receipts only, so such bodies are invisible to it.
- **Symlinks pass.** `fetch-verify.py:65` `bpath.is_file()` follows symlinks. A body symlinked to a host file passes `ok` against that file's digest, while git commits only the link text. No symlinks exist now (`find -type l` is empty).
- **Seat directory names are inconsistent.** Three seats use `MadoR18.<Seat>/` instead of `<Seat>/`.

**Exploit path.** A seat can plant either of the following, and the receipt check will not object:
- an unreceipted "fetched" file;
- a symlinked one.

**Smallest remediation.** The FetchVerify owner adds:
- `is_symlink()` → `BAD_SCHEMA`;
- slug regex → `BAD_SCHEMA`;
- an `UNRECEIPTED_BODY` line for any file not named by a receipt.

## Recommended rules

### Commit raw body (C)

- **C1.** Commit only when **all** of these hold:
  - the URL is pinned to a tag or commit: raw.githubusercontent.com `<owner>/<repo>/<tag|sha>/…`, or api.github.com for refs, trees, commits or releases;
  - the content is text, not HTML;
  - it is ≤1 MiB;
  - it is byte-stable on re-fetch;
  - the repo has an OSI licence.
- **C2.** For every (repo, tag) with a committed body, commit that repo's `LICENSE` body once, with a receipt, in the same seat dir. An alternative is one shared `fetch/_licenses/<owner>-<repo>-<tag>-license`.
- **C3.** Before any commit, the fetch tree must pass three checks:
  - `gitleaks dir .ufo/waves/<round>/fetch` with rc 0;
  - the slug regex `^[a-z0-9][a-z0-9._-]*$`, with no symlinks;
  - every body named by exactly one receipt.

### Digest-only (D): commit the receipt line, gitignore the body

- **D1.** Any `text/html` body, or any body containing per-request tokens (csrf, nonce, hmac, request-id, `jwt=`, `sig=`, `apiToken`).
- **D2.** Any body without a redistribution licence carried with it:
  - blogs, marketplaces, Writebook or GitBook docs, `llms*.txt`;
  - AUR pages and PKGBUILDs;
  - YouTube oEmbed;
  - GitHub discussions, issues and comments (UGC);
  - Arch Wiki raw pages (GFDL needs the licence text);
  - rendered wiki.hypr.land HTML.

  Prefer the pinned raw source instead, for example `raw.githubusercontent.com/hyprwm/hyprland-wiki/<sha>/content/…md` plus its BSD-3 `LICENSE`.
- **D3.** Binary archives (`.tar.gz`, `.crate`). Commit the extracted cited file as a C1 body if it is licensed.
- **How to mark it.** Use a receipt field `"retain":"digest-only"` and save the body as `<slug>.nocommit`. In `.gitignore` (L1-owned), add `.ufo/waves/*/fetch/**/*.nocommit`. `fetch-verify` then reports `DIGEST_ONLY` for those rows: not `ok` for crediting a tier-A row, and not `MISSING`.

### Never (N)

- **N1.** Never fetch release assets, attachments, `private-user-images` or any URL whose redirect carries `sig=`, `jwt=`, `token=` or `X-Amz-*`. If a redirect does carry one, record `final_url` with the query stripped and add `"final_url_query_stripped":true`.
- **N2.** Never use `-D`, `-v`, `--trace*` or `-c`/`-b` cookie jars, and never fetch logged-in, cookie-bearing or private URLs. The contract curl form already complies; the rule closes the variants.
- **N3.** Never name a body after a harness-loaded file: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.github/copilot-instructions.md`, `llms.txt`. The enforced lowercase slug regex already excludes the first three; use a `.body` suffix for the rest.

### Per-path disposition for the current tree (rules as stated)

**Commit (C): 232 bodies, 2,838,357 B; gitleaks rc 0, 0 findings.**
- The commit class contains:
  - all raw tag-pinned walker, elephant, omarchy (basecamp/omacom), swaybg, hypridle, hyprlock, alacritty, xdg-terminal-exec and adrg/xdg files;
  - api.github.com trees, commits and releases.
- It needs 4–6 LICENSE bodies added (C2).
- Its 14 package-command and 3 `AGENTS.md`-path mentions are data. The path mentions are tree listings, not the file itself.

**Digest-only (D): 49 bodies, 5,467,908 B.**
- **HTML (29):**
  - `FetchBackfillR17/s063-wiki-hypridle`, `s064-wiki-hyprlock` (round-17 credited rows: switch to pinned hyprland-wiki markdown, or keep digest-only with a re-fetch check, since these were byte-stable twice);
  - `MadoR18.SrcWalkerThemes/xdg-{basedirectories,lib-rs}.html`, `NoteWalker/xdg-crate-basedirectories.html`;
  - `NoteTheme/*.html` (5);
  - `SrcOmarchyManualThemes/*` HTML (7);
  - `SrcThemeAlternates/{aur-*,dhh-omarchy-out,gh-omarchy-discussion-2835,hyprwiki-app-launchers,omarchytheme-*,walker-ssp-blog}`;
  - `SrcWalkerDocsSite/gitbook-*.html`.
- **Unlicensed, third-party or UGC text (14):**
  - `SrcOmarchyManualThemes/manual.md`;
  - `SrcThemeAlternates/{archwiki-*(5),aur-*-pkgbuild(2),omarchy-wsl2-theming,yt-oembed-extra-wallpapers}`;
  - `SrcWalkerDocsSite/{gitbook-llms.txt,gitbook-llms-full.txt,gitbook-sitemap.xml,gitbook-sitemap-pages.xml}`.
- **Binary (2):** `NoteWalker/walker-v2.17.2-src.tar.gz`, `SrcWalkerConfigPaths/xdg-3.0.0.crate`.
- **Unreceipted (4):** the F6 list. Add receipts or delete.

**Coupling for L1.** Digest-only rows can still be credited, but only by re-fetch:
- Byte-stable docs (wiki.hypr.land, Arch Wiki raw) can be re-checked by re-fetch.
- Bodies that vary per fetch (GitHub and Writebook HTML) cannot be reproduced.

So a tier-A credited row should cite a C1 body. That is already the round's preference for tag-pinned raw sources.

## Appendix — control-sample receipts (`/tmp/sfb/receipts.jsonl`, not committed)

| Body | sha256 | Bytes | URL |
|---|---|---|---|
| `omarchy-agents-md` | `f45cd0620859eb36194e824975a055a1801e388f843c0773f3da5ccbea490b06` | 6466 | `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/AGENTS.md`, 200, 2026-10-20T15:42:22Z |
| `walker-license` = `elephant-license` | `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` | 35149 | — |
| `omarchy-license` | `717ba1949502290f8e47688ae2e323acd06c8ca47aec9f7596b15f678c1af4a2` | 1063 | — |
| `swaybg-license` | `95224d118a325daf31828afcca98cd958d53f0a7cdd856b50b1be8ac44832faf` | 1061 | — |
| `hyprland-wiki-license` | `cbc783648291b12a7b8af49ee6f42698f6a094b969400b64435d82de595a05d7` | 1516 | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/LICENSE` (branch, unpinned) |
| `gh-walker-html` | `303a98567abd…` (second fetch `b4eb0d9043f4…`) | 353730 | — |
| `omacom-manual` | `2b52b192fb59…` (second fetch `41eaf35494e1…`) | 168519 | — |
| `lane-repo-public` | `469030aff3ed…` | 262592 | `https://github.com/VeigaPunk/mado-shokunin`, 200 logged-out |

Tags resolved with `git ls-remote`:

| Tag | Object |
|---|---|
| walker `v2.17.2` | `a515085fd39fae80acc086c8fbfd9b7771a9a11d` (lightweight) |
| elephant `v2.22.1` | `8f1e21d6efe40b8b3953f95b9574f99f717caf91` |
| omarchy `v3.8.4` | `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` |
| swaybg `v1.2.2` | `3ca0f88f…` (tag object) → `a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2` (commit) |

Checks for L1 after integration:
- `gitleaks dir .ufo/waves/round-18/fetch` must give rc 0 over the committed set.
- `python3 .ufo/waves/round-18/fetch-verify.py` must run, with the symlink, slug and unreceipted-body extensions from F6.
