# SrcWalkerDocsSite — walker's official docs site at 2.17.2

Scope: does walker 2.17.2 link an official docs site or wiki from its README?
Open it (receipted), record whether it is versioned, judge tier (docs vs
community). No host binary was run; no lane file outside this report and
`.ufo/waves/round-18/fetch/SrcWalkerDocsSite/` was written.

## Verdict

**Yes, there is an official docs site, and no GitHub wiki.** README at tag
v2.17.2 (`readme-v2.17.2.md:5`, 233 lines, only occurrence) links
"GitBook Documentation/Wiki" → `https://benz.gitbook.io/walker/`. `GET
/walker/wiki` on GitHub returns 200 but redirects to the repo root
(`final_url https://github.com/abenz1267/walker`) — no wiki exists.

**The site is not versioned.** A 10-URL sitemap contains no version-scoped
path, the GitBook space metadata carries one `revision` and no `versions`
array, and the full-text aggregate (`llms-full.txt`, 605 lines) contains
**zero** Walker version tokens. Content is git-synced from the maintainer
repo `abenz1267/walker-wiki` (branch `master`, zero tags); its last commit is
`0fb918c588448b5db8beec66a0490ffdedf050ad`, 2026-02-15, while tag v2.17.2
points at `a515085f…`, committed 2026-10-08 — the docs predate the installed
binary by ~8 months.

**Tier: kind `docs`, tier A**, scoped as "unversioned/latest GitBook, current
revision dated 2026-02-15; a 2.17.2 anchor only through the backing repo
commit, never through the site URL". Rationale: maintainer-authored (space org
`xCFvQwZ0XVLSj2YebMIU`, git-sync to `abenz1267/walker-wiki`), linked from the
tagged README — this is upstream documentation, not a community restatement
(contrast S061/S062/S070, tier C, rejected). Precedent: S016/S063/S064 admit
maintainer wikis as tier A with the "Latest git" limitation stated in the
scope cell.

## Observed facts

Receipt ledger: `.ufo/waves/round-18/fetch/SrcWalkerDocsSite/receipts.jsonl`,
11 lines, each `sha256` re-verified equal to its saved body (0 mismatches).

| # | Fetch | status | bytes | sha256 (12) | body |
|---|---|---|---|---|---|
| F1 | `raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md` | 200 | 7926 | `9755f955d5c4` | `readme-v2.17.2.md` |
| F2 | `https://benz.gitbook.io/walker/` | 200 | 299666 | `a1be763ff9b1` | `gitbook-root.html` |
| F3 | `…/walker/sitemap.xml` | 200 | 213 | `fa6f0ab19077` | `gitbook-sitemap.xml` |
| F4 | `…/walker/sitemap-pages.xml` | 200 | 1677 | `75f752fb37e0` | `gitbook-sitemap-pages.xml` |
| F5 | `…/walker/walker-and-elephant` | 200 | 348136 | `739dd427d356` | `gitbook-walker-and-elephant.html` |
| F6 | `…/walker/llms.txt` | 200 | 742 | `829b700a1ef4` | `gitbook-llms.txt` |
| F7 | `…/walker/llms-full.txt` | 200 | 21504 | `bd4082d75c0e` | `gitbook-llms-full.txt` |
| F8 | `api.github.com/repos/abenz1267/walker-wiki/commits/master` | 200 | 6211 | `2508cb96b19f` | `api-walker-wiki-master-commit.json` |
| F9 | `api.github.com/repos/abenz1267/walker/commits/a515085f…` | 200 | 9315 | `4767b7522364` | `api-walker-v2.17.2-commit.json` |
| F10 | `api.github.com/repos/abenz1267/walker-wiki/git/trees/0fb918c…` | 200 | 2714 | `28dac92bff30` | `api-walker-wiki-tree.json` |
| F11 | `raw.githubusercontent.com/abenz1267/walker-wiki/0fb918c…/walker-and-elephant.md` | 200 | 695 | `52c9730fcd63` | `walker-wiki-walker-and-elephant.md` |

- **F1** — README v2.17.2 line 5: `[GitBook Documentation/Wiki](https://benz.gitbook.io/walker/)`;
  exactly one `benz.gitbook.io` occurrence in 233 lines.
- **F1/tag** — `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'`
  returned a single line `a515085fd39fae80acc086c8fbfd9b7771a9a11d refs/tags/v2.17.2`
  (lightweight tag, no peeled `^{}` line ⇒ that hash is the commit). GitHub
  API F9: that commit is dated `2026-10-08T06:45:24Z`, message
  "fix: GTK 4.24 blur handling causing crash".
- **F2** — root page 200; extracted text ends with "Last updated / 1 year
  ago"; page is a Next.js/GitBook shell (`server: cloudflare`,
  `x-gitbook-route-type: static`).
- **F2/space metadata** (same body, escaped JSON): `gitSync` =
  `{installationProvider: github, installationStatus: active,
  repoName: abenz1267/walker-wiki, url: …/walker-wiki/tree/master,
  updatedAt: 2026-07-03T19:51:26.439Z}`; `revision: OXW0y1O2VvaZXpQheY4m`;
  `comments: 0`, `changeRequests: 16`; the substring `versions` occurs
  **0 times** in the entire 299666-byte root body.
- **F3/F4** — `sitemap.xml` only points at `sitemap-pages.xml`; the page
  sitemap lists exactly 10 URLs (`/`, `walker-and-elephant`,
  `installation-and-launching`, `providers`, `dmenu`, `faq`,
  `customization/{general-config,provider-actions,theme,custom-menus}`).
  None carries a version segment or `/v/` prefix.
- **F5** — `walker-and-elephant` page 200, text identical in substance to
  F11 modulo the H1 and `-`→`*` list markers (diff shows only those).
- **F6** — `llms.txt` advertises 10 `.md` page URLs; the `.md` endpoints are
  NOT reliable (see Gaps).
- **F7** — `llms-full.txt` is the whole space in 605 lines / 21504 bytes;
  `grep -cE '\b2\.[0-9]+(\.[0-9]+)?\b|v[0-9]+\.[0-9]+'` ⇒ **0**. The only
  dotted numerics are `0.1`, `1.5`, `0.5` (config/theme examples).
- **F8** — walker-wiki master = `0fb918c588448b5db8beec66a0490ffdedf050ad`,
  `2026-02-15T08:00:25Z`, "add missing providers"; F2's `revision.createdAt`
  is `2026-02-15T08:00:56.159Z` (31 s later — the sync event), and the space
  object is `rNR09gfm7YeuyalMUCgu`, title "Walker", `visibility: public`,
  `createdAt 2024-12-01`.
- **F10** — tree at that commit is flat markdown (`README.md`, `SUMMARY.md`,
  `dmenu.md`, `faq.md`, `installation-and-launching.md`, `providers.md`,
  `walker-and-elephant.md`, `customization/`); no version directory.
- **F11** — raw page at the pinned commit, 695 bytes,
  sha256 `52c9730fcd634ca40f87512738fc122d221423455b7a6946b8d4ae3350983b26`.
- `git ls-remote --tags https://github.com/abenz1267/walker-wiki` ⇒ 0 tags,
  refs `HEAD`/`master` only (plus `refs/pull/*`).

## Versioning judgement

| Question | Answer | Basis |
|---|---|---|
| Version selector / multiple site versions? | No | F2 space metadata single `revision`, no `versions`; F3/F4 no versioned paths |
| Version-scoped URLs (e.g. `/v/2.17.2/`)? | No | F4 sitemap, 10 URLs |
| Does the docs text name any Walker version? | No | F7, 0 matches for `2.x`/`vX.Y` |
| Is the content nevertheless pinnable? | Yes, via `walker-wiki@0fb918c` raw files | F10/F11, digest + line anchors |
| Does the site track 2.17.2? | [UNK] — content is 2026-02-15, binary tag 2026-10-08 | F8 vs F9 |

## Proposed SOURCES row (id reserved; drafts write `S0xx-pending`)

One row only — a companion row for `walker-wiki` would duplicate this row's
scope (cf. the S030→S045 duplicate-admission rejection). The pin lives in the
anchor cell instead.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx-pending | Walker official documentation (GitBook) — https://benz.gitbook.io/walker/ | docs | A | Walker launcher frontend/backend contract (docs name no version), config path and keys, launching/service model, dmenu flags, provider set; unversioned GitBook, content git-synced from abenz1267/walker-wiki@master (last commit 0fb918c, 2026-02-15) — not a 2.17.2 label | root 200 sha256 `a1be763ff9b1027b…`; `llms-full.txt` 605 lines sha256 `bd4082d75c0e514c…`, 0 version tokens; README v2.17.2:5 links the site (tag v2.17.2 = `a515085fd39f…`, lightweight); page `walker-and-elephant` text pinned at walker-wiki `0fb918c588448b5db8beec66a0490ffdedf050ad` (695 B, sha256 `52c9730fcd634ca4…`) | Walker is a frontend over an Elephant backend and the two are configured separately; `walker --gapplication-service` and `/run/user/1000/walker/walker.sock` are the documented warm-launch pair; config lives at `~/.config/walker/config.toml`; dmenu flags table and provider list are documented — no version pin, no host fact | mined* | 2026-10-20 | 90d | corpus/knowledge/walker-route-r18.md |

\*Status `mined` only if `corpus/knowledge/walker-route-r18.md` actually cites
this row; otherwise `queued`. The recheck is 90d because the site is a
mutable unversioned source whose content already trails the binary.

## Verbatim quotes a P3 note may use (each ≤25 words, line anchors in F7)

- `:8` "Walker is a frontend program that allows you to interact with a backend: Elephant." (12 words; identical at F11:3)
- `:103` "Elephant has to be running in order for Walker to function." (11 words)
- `:113` "This can be optimized, by keeping a Walker instance running with `walker --gapplication-service`" (13 words)
- `:117` "make Walker popup via a socket call, f.e. `nc -U /run/user/1000/walker/walker.sock`" (15 words)
- `:219` "Default path for configuration file is `~/.config/walker/config.toml`." (10 words)
- `:56` The install line is `yay -S walker` — an AUR route, never a host fact.

## What this row can and cannot support

- **Can**: upstream contract statements (frontend/backend split; separate
  configuration; documented service/socket warm-launch; config path; dmenu
  flag table; provider list incl. `bluetooth`, `nirisessions`), all as
  documentary `[INF-docs]`, dated 2026-02-15.
- **Cannot**: any 2.17.2-specific behavior or flag claim; any host fact; any
  claim that the documented `[providers.sets.omarchy]` example or provider
  list matches the installed 2.17.2 binary (site predates it by ~8 months).
- **C2 qualifier**: this row names "Walker" in both `source` and `scope`, is
  tier A, upstream https, and is receipted (F1/F2/F7) — it satisfies the
  P3 upstream-row requirement if the note cites it and its `used-by` names
  the note.

## Gaps / [UNK]

1. **`.md` endpoints unreliable**: `llms.txt` advertises per-page `.md`
   URLs, but `…/walker-and-elephant.md` timed out twice (60 s and 45 s, curl
   rc 28, 0 bytes); `llms-full.txt` and HTML served in ≤5 s. Do not cite the
   `.md` URLs; use F7/F11 bodies.
2. **"Last updated 1 year ago"** on F2/F5 conflicts with the backing repo's
   last commit (2026-02-15, 8 months). The relative label is imprecise; use
   the commit date. This is an observed inconsistency, not a conclusion
   about which is authoritative.
3. Whether the site content was updated for 2.15/2.16/2.17 is **[UNK]** —
   the site exposes no changelog, and content is older than the tag.
4. Host `walker`/`elephant` binaries were **not** run (host pause): all
   version facts come from `/var/log/pacman.log` file reads
   (walker 2.17.0-1 → 2.17.2-1 at `:2929`; elephant 2.22.1-1 at `:3095`),
   and the binary/docs correspondence on this host stays `[UNK]`.
5. Confidence: F1–F11 **high** (raw bodies, digest-verified); tier call
   **high** (maintainer link + git-sync); "docs track 2.17" **low/unknown**.

## Commands / compliance

- `curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}'` only;
  no auth, cookies or private URLs; every body ≤1 MiB and saved under
  `.ufo/waves/round-18/fetch/SrcWalkerDocsSite/`.
- Network git reads only: `git ls-remote` (walker tag, walker-wiki refs); the
  lane's git/jj state was read-only (`git rev-parse HEAD` = `d3a0000`) and
  untouched.
- No pacman/yay/paru, no systemctl/journalctl/hyprctl, no walker/elephant/
  omarchy-* invocation, no host probes, no tool installs, no subagents.
