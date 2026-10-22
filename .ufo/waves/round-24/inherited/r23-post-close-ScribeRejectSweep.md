# ScribeRejectSweep — C2 frontier rejection sweep for the terminal-tree routes (round 23, wave 1)

Seat: `MadoR23.ScribeRejectSweep` (scribe). Scope: the C2 frontier item — one rejection sweep
for the terminal-tree routes. Open third-party (community, tier C) pages that restate where
**foot**, **kitty** or **ghostty** read their configuration; open each by ordinary means; draft
the corresponding `corpus/SOURCES.md` registry rows with **status `rejected`**, the reason, and the
flip condition; draft the matching search-log line.

**Nothing was landed by me.** `corpus/SOURCES.md` was not edited, no corpus file was created or
edited, no product code, judge, commit, push, publish or deploy was touched. The only file written
in the lane repo is this report. The rows and the search-log line below are **drafts for the
integrator**, not applied changes.

Access date for every page below: **2026-10-22**.

---

## 1. What was done

### 1.1 Shape of the sweep — and why three pages, not one or two

The frontier item asked for "one or two" community pages. I opened **one page per terminal tree**
(foot, kitty, ghostty) — three pages — because the C2 claim it serves is scored per terminal
(`corpus/SOURCES.md` C2 counter: foot, kitty, ghostty, target 3/3), so a sweep that covers only one
tree leaves two thirds of the frontier un-swept. Each page is one distinct terminal, so each
rejection is independent and none is a duplicate of another.

I did **not** open upstream tier-A material as row candidates: the C2 source seats
(`SrcFoot` S140–S149/S152, `SrcKitty` S123–S133, `SrcGhostty` S134–S139/S150–S151) already own the
upstream rows for these routes. My sweep only produces the **negative** half of the evidence:
which tier-C restatements were tried and why each fails the bar. Upstream pages below were opened
**only as the yardstick** against which each community claim is judged; they are cited inside the
rejection reason, not proposed as new rows.

### 1.2 Host state observed (read-only, no change)

All three config trees exist on this host and no binary of any of the three is installed:

```
$ ls -la ~/.config/foot ~/.config/kitty ~/.config/ghostty
foot/foot.ini (516 B), foot/foot.ini.bak.20261003-190229 (513 B)
kitty/kitty.conf (954 B), kitty/kitty.conf.bak.20261003-190229 (953 B)
ghostty/config (1,325 B), ghostty/config.bak.20261003-190229 (1,322 B)

$ pacman -Q foot kitty ghostty          → error: package 'foot' was not found  (same for kitty, ghostty)
$ pacman -Qs '^(foot|kitty|ghostty)$'   → (no match)
$ command -v foot footclient kitty ghostty → all: not on PATH
$ ls /usr/share/applications | grep -Ei 'foot|kitty|ghostty' → (no match)
$ ls ~/.local/bin | grep -Ei 'foot|kitty|ghostty'          → (no match)
```

Consequence for the C2 route rows: for all three terminals the host fact is the **config file**
(a bytes-level artifact), not a running binary. `pacman -Q` was a read (allowed by the pacman
guard); no `-S/-Sy/-Syu/-U/-R` was issued and no package was installed or upgraded in this seat, so
there is no tool-install line to record.

### 1.3 Exact commands run (all read-only; ordinary fetch only)

```
# web search (4 queries, ordinary search engine)
web_search "foot terminal emulator config file location ~/.config/foot/foot.ini blog guide"
web_search "kitty terminal config file location ~/.config/kitty/kitty.conf guide blog"
web_search "ghostty config file location ~/.config/ghostty/config guide blog"
web_search "foot terminal emulator configuration guide blog foot.ini customize 2025"

# ordinary fetch of the candidate community pages (curl, browser UA; no headless browser)
curl -sS -L --max-time 30 -A "Mozilla/5.0 ..." https://linuxjunkies.org/guides/configure-kitty
curl -sS -L --max-time 30 -A "Mozilla/5.0 ..." https://michaelbommarito.com/wiki/programming/tools/ghostty-configuration/
curl -sS -L --max-time 30 -A "Mozilla/5.0 ..." https://orioninsist.org/blog/optimized-foot-config-for-sway-wayland/
curl -sS -L --max-time 30 -A "Mozilla/5.0 ..." https://petronellatech.com/blog/ghostty-terminal-emulator-setup-configuration-guide-2026/   → HTTP 403
sha256sum <each file>            # twice per page, one second apart, to check byte stability

# upstream yardstick (read-only)
curl -sS https://sw.kovidgoyal.net/kitty/conf/  https://sw.kovidgoyal.net/kitty/kittens/themes/
curl -sS https://sw.kovidgoyal.net/kitty/changelog/  https://sw.kovidgoyal.net/kitty/glossary/
curl -sS https://ghostty.org/docs/config
curl -sS https://github.com/ghostty-org/ghostty/releases.atom
curl -sSL https://codeload.github.com/ghostty-org/ghostty/tar.gz/refs/tags/v1.2.3  → g-v1.2.3.tgz
curl -sSL https://codeload.github.com/ghostty-org/ghostty/tar.gz/refs/tags/v1.3.0  → g-v1.3.0.tgz
tar xzf g-v1.3.0.tgz ; tar xzf g-v1.2.3.tgz
curl -sS https://codeberg.org/dnkl/foot/raw/branch/master/README.md
curl -sS https://codeberg.org/dnkl/foot/raw/branch/master/doc/foot.ini.5.scd
curl -sS https://codeberg.org/dnkl/foot/raw/tag/1.25.0/doc/foot.ini.5.scd
curl -sS https://codeberg.org/dnkl/foot/raw/tag/1.26.0/doc/foot.ini.5.scd
curl -sS https://codeberg.org/dnkl/foot/raw/tag/1.26.0/CHANGELOG.md
curl -sS https://codeberg.org/api/v1/repos/dnkl/foot/git/refs/tags/{1.25.0,1.26.0}
curl -sS https://codeberg.org/api/v1/repos/dnkl/foot/git/tags/<tag-object-sha>

# extraction for line anchors (tag-stripped text, script+style+svg+noscript skipped)
python3 extract.py <file> '<regex>' '<regex>' ...      # prints raw bytes, raw sha256,
                                                        # extracted line count, extracted sha256, matching lines
```

No headless browser was used. No bot challenge, captcha or access control was encountered or
attempted: the one blocked URL returned a plain `HTTP 403` with a 5,989-byte error body and is
recorded as **unopened** below, never as a row.

### 1.4 Digests of everything cited

Community pages (each fetched twice, one second apart — **byte-identical both times**):

| page | raw bytes | raw sha256 | tag-stripped extracted lines | extracted-text sha256 |
|---|---|---|---|---|
| linuxjunkies.org/guides/configure-kitty | 94,846 | `6c9d2c6805ceaa9221a25e4aa6866a43d576ebb4dbd596f51f024534e98423a3` | 143 | `be24ed0d19fb963829a84be28d07b2110a30f75009554b91d3b4ad8a033ace72` |
| michaelbommarito.com/wiki/programming/tools/ghostty-configuration/ | 170,539 | `e6e45c62a01db01888e5c955e6d279ab47f6c91ef40e9889ac84aa7789a69f98` | 263 | `388f226376b39338d15263ccbe70cfbd6ce4b7326db432c72276b9f903379d3c` |
| orioninsist.org/blog/optimized-foot-config-for-sway-wayland/ | 38,927 | `961c39e837c63f4cae718248fa9b3c87df0defb74a81a0513883e82cf94a2b09` | 82 | `7d36e5c3ad51ed3eb7a60f494cb6631d9bd459f6d9b81af5e933b32aefb7f4e7` |

Upstream yardstick:

| file | bytes | sha256 |
|---|---|---|
| kitty `conf.html` (live built docs) | 577,387 | `08e6411024fdfc444e47750dadc28b7d87e0bd768695cc635690916e08a9703d` |
| kitty `kittens/themes.html` | 174,014 | `6b832a786a58b2f23c0fe6fa6b97506398f10428ac50bed104d4f09311c576a8` |
| kitty `changelog.html` | 696,785 | `2e4cdff1d73a440f11283e0a79d1986d86edb8e0849f3b5c194c50efdf2d59c3` |
| kitty `glossary.html` | 185,151 | `0795bd16677645b84d762974ff882f53753626fe446045a4d240f7c48db2a8c0` |
| ghostty.org/docs/config | 111,894 | `cb79ca5dcf496d81ed05862e1888958c307dc934988b3595926b2c17ab08b6b5` |
| ghostty releases.atom | 7,920 | `3c8c5420923d07e3b47b1f878cebd66016d546af2071a6dacbc95f0634f9c410` |
| ghostty v1.2.3 source tarball | 36,345,813 | `e17d39482fc70fba3d72f5f25c12e9d9a72b87dd45a61a854d9928e98b69edd8` |
| ghostty v1.3.0 source tarball | 37,412,762 | `3d05cbdb712ec19ecdc720a2757a09ebf79aaa8d90ae2ae5c0ddd5536ef31be6` |
| ghostty v1.2.3 `src/config/Config.zig` | 339,217 | `ed2eb047c44c3ad82d4e1e5d23240198e289e8bf34520c444105b4a3008a6e1e` |
| ghostty v1.3.0 `src/config/Config.zig` | 405,756 | `81f1a65eda978c1d20851f355ed970958c2c9fd6ecdd760b728c4dfd277298b5` |
| ghostty v1.3.0 `src/config/file_load.zig` | 5,434 | `96e8165c5a365808b7407d61f7073aa074189bcd96b3daa0a43d37f5e3d4c94f` |
| foot README @ master | 24,450 | `874e192a7f322421e6c762c18dadd47239f7a5366bc47b966d12b516fd6f626d` |
| foot `foot.ini(5)` @ 1.25.0 | 75,587 | `4ffb873a6219d40d36240071ae49a280a41e70c4fdcc86135e4d0210432e2e4a` |
| foot `foot.ini(5)` @ 1.26.0 | 72,338 | `f5cb482ae7518c656dc3e53bebde1054c6743186816d5b16f44d206fe2b8c279` |
| foot `foot.ini(5)` @ master | 76,752 | `4611cce41d79d747166711b611f82549952112788a0e3f74b3c8ea855708a782` |
| foot CHANGELOG.md @ 1.26.0 | 135,100 | `f516cf5b70768604be1188654a5362239c7a0727839e1ad4ab7c226822b3183b` |

---

## 2. Drafted SOURCES rows (11-column shape, **status `rejected`**)

Column order is `corpus/SOURCES.md`'s registry header:
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

**Id band S153–S155.** The other C2 seats' bands are S123–S133 (kitty), S134–S139 + S150–S151
(ghostty), S140–S149 + S152 (foot); S153 onward was unused in the wave-1 reports at the time of
writing. The integrator renumbers if bands collide.

**These three rows are `rejected`, so they do not and must not count toward the C2 3/3 counter** —
`c2/count.py` only counts rows whose `status` cell is exactly `mined` and whose `opened` cell is
`2026-10-22`. A `rejected` row is taste evidence for the frontier (SOURCES contract rule 3,
"rejected rows kept as taste evidence"), and it records which tier-C restatements were tried so the
same pages are not re-opened in a later round.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S153 | Linux Junkies — Configure Kitty (Including Image Protocol) — https://linuxjunkies.org/guides/configure-kitty | community | C | third-party kitty setup guide restating where kitty reads its config file; page-stated update date 2026-06-07; no version anchor for the config-path claim | raw 94,846 B sha256 `6c9d2c6805ceaa9221a25e4aa6866a43d576ebb4dbd596f51f024534e98423a3` (two consecutive fetches byte-identical); tag-stripped extracted text 143 lines, sha256 `be24ed0d19fb963829a84be28d07b2110a30f75009554b91d3b4ad8a033ace72`; L17-18 `kitty --version` / `# kitty 0.35.2 created by Kovid Goyal`; L20 `Kitty reads ~/.config/kitty/kitty.conf on startup.`; L53 `Kitty ships with an built-in theme browser since version 0.23.`; JSON-LD `dateModified 2026-06-07T00:47:46.562Z`; against upstream `conf.html` 577,387 B sha256 `08e6411024fdfc444e47750dadc28b7d87e0bd768695cc635690916e08a9703d` L1306-1309 (`kitty looks for a config file in the OS config directories (usually … KITTY_CONFIG_DIRECTORY environment variable`) and upstream `changelog.html` 696,785 B sha256 `2e4cdff1d73a440f11283e0a79d1986d86edb8e0849f3b5c194c50efdf2d59c3` (0.35.2 [2024-06-22] at L917, 0.47.2 [2026-06-07] at L890, 0.49.2 [2026-10-01] at L882) | REJECTED: community tier cannot support a C2-covered entry (precedent S061/S062); the page's only kitty version token is a stale sample output — it presents `kitty 0.35.2` as the current kitty on a page dated 2026-06-07, but upstream released 0.35.2 on 2024-06-22 and released 0.47.2 on 2026-06-07, the same day, with 0.49.2 current since 2026-10-01, so the version token is contradicted by upstream's release history; and the config-path claim carries no version anchor and omits the `KITTY_CONFIG_DIRECTORY` / `kitty --config` override upstream states, so it cannot describe an era's route. flip: a version-pinned rewrite (e.g. "as of kitty 0.49.2") whose config-path sentence quotes upstream and names `KITTY_CONFIG_DIRECTORY` — usable only as a tier-C cross-check if the rubric ever admits tier C | rejected | 2026-10-22 | 180d | — |
| S154 | Mike Bommarito — ghostty terminal configuration — https://michaelbommarito.com/wiki/programming/tools/ghostty-configuration/ | community | C | third-party ghostty configuration walkthrough restating the config-file location and a per-version feature table; published 2025-08-13, last updated 2025-10-23 | raw 170,539 B sha256 `e6e45c62a01db01888e5c955e6d279ab47f6c91ef40e9889ac84aa7789a69f98` (two consecutive fetches byte-identical); tag-stripped extracted text 263 lines, sha256 `388f226376b39338d15263ccbe70cfbd6ce4b7326db432c72276b9f903379d3c`; L2 install one-liner writing `~/.config/ghostty/config`; L18-19 `ghostty looks for configuration at:` / `~/.config/ghostty/config`; L64 `not yet in a stable release - it only exists in the main branch development builds`; L238 `1.2.0 (current stable)`; L239 `main branch only (post-1.2.0): gtk scrollbar support`; against upstream ghostty.org/docs/config 111,894 B sha256 `cb79ca5dcf496d81ed05862e1888958c307dc934988b3595926b2c17ab08b6b5` L22 (`The configuration file is named config.ghostty (or config before 1.2.3),`), upstream releases.atom 7,920 B sha256 `3c8c5420923d07e3b47b1f878cebd66016d546af2071a6dacbc95f0634f9c410` (v1.2.3 2025-10-23, v1.3.0 2026-03-09, v1.3.1 2026-03-13), upstream v1.3.0 `src/config/file_load.zig` 5,434 B sha256 `96e8165c5a365808b7407d61f7073aa074189bcd96b3daa0a43d37f5e3d4c94f` L14 (`.{ .subdir = "ghostty/config.ghostty" }`) and L18-24 (legacy `ghostty/config`, comment `Ghostty <1.3.0 default path`), upstream v1.3.0 `src/config/Config.zig` 405,756 B sha256 `81f1a65eda978c1d20851f355ed970958c2c9fd6ecdd760b728c4dfd277298b5` L1387-1403 (`scrollbar` option) and upstream v1.2.3 `src/config/Config.zig` 339,217 B sha256 `ed2eb047c44c3ad82d4e1e5d23240198e289e8bf34520c444105b4a3008a6e1e` (0 occurrences of `scrollbar`) | REJECTED: community tier cannot support a C2-covered entry (precedent S061/S062); and the page contradicts upstream on the file it names — it states the ghostty config is at `~/.config/ghostty/config` and its own install one-liner writes that path, while upstream's current docs name the file `config.ghostty` (upstream keeps `config` only as the pre-1.3.0 legacy path, `src/config/file_load.zig` L18-24); its version table pins `1.2.0 (current stable)` and the gtk scrollbar as `main branch only`, yet upstream shipped v1.2.3 on 2025-10-23 (the page's own last-update day) and v1.3.0/v1.3.1 afterwards, and v1.3.0's `Config.zig` does carry a `scrollbar` option (L1387-1403) that v1.2.3's does not. flip: a rewrite that names the ghostty release it describes and quotes upstream for both file names and the legacy-path rule — usable only as a tier-C cross-check if the rubric ever admits tier C | rejected | 2026-10-22 | 180d | — |
| S155 | Orion Insist — Optimized Foot Config for Sway/Wayland Devs — https://orioninsist.org/blog/optimized-foot-config-for-sway-wayland/ | community | C | third-party foot.ini walkthrough restating the foot config-file location and shipping a full sample config; published and last modified 2025-11-08 | raw 38,927 B sha256 `961c39e837c63f4cae718248fa9b3c87df0defb74a81a0513883e82cf94a2b09` (two consecutive fetches byte-identical); tag-stripped extracted text 82 lines, sha256 `7d36e5c3ad51ed3eb7a60f494cb6631d9bd459f6d9b81af5e933b32aefb7f4e7`; **0 version-like tokens in the whole 82-line extraction**; L2 date `November 8, 2025`; L3 `which I store in ~/.config/foot/foot.ini`; L19 `# scrollback-lines (artık [scrollback] altında)`; L47 `[colors]`; L74 `[cursor].color: use colors.cursor instead`; L75 `[key-bindings].copy: not a valid action: copy`; against upstream foot README @ master 24,450 B sha256 `874e192a7f322421e6c762c18dadd47239f7a5366bc47b966d12b516fd6f626d` L81 (`$XDG_CONFIG_HOME/foot/foot.ini` (defaulting to …)), upstream foot `foot.ini(5)` @ 1.25.0 75,587 B sha256 `4ffb873a6219d40d36240071ae49a280a41e70c4fdcc86135e4d0210432e2e4a` L985 `# SECTION: colors` / L1133 `# SECTION: colors2`, upstream foot `foot.ini(5)` @ 1.26.0 72,338 B sha256 `f5cb482ae7518c656dc3e53bebde1054c6743186816d5b16f44d206fe2b8c279` L17-20 (search order `XDG_CONFIG_HOME/foot/foot.ini` then `XDG_CONFIG_DIRS/foot/foot.ini`), upstream foot `foot.ini(5)` @ master 76,752 B sha256 `4611cce41d79d747166711b611f82549952112788a0e3f74b3c8ea855708a782` L27 `*[colors-dark]*++` / L1025 `# SECTION: colors-dark, colors-light`, upstream foot CHANGELOG.md @ 1.26.0 135,100 B sha256 `f516cf5b70768604be1188654a5362239c7a0727839e1ad4ab7c226822b3183b` L78-79 and L119-125 | REJECTED: names no foot version anywhere (0 version tokens across 82 extracted lines), so no claim on the page can bind to a release; and the config dialect it teaches is contradicted by current upstream — the sample config uses the `[colors]` section with `cursor=` inside it and prescribes `colors.cursor` (L47, L74), while upstream foot 1.26.0 replaced `[colors]` with `[colors-dark]` (CHANGELOG L78), deprecated `[colors]` (L119) and removed `cursor.color` in favour of `colors-{dark,light}.cursor` (L125), and upstream's current `foot.ini(5)` documents `SECTION: colors-dark, colors-light`; the page itself warns "Configurations evolve. Blog posts and dotfiles get outdated." flip: a version-pinned rewrite (e.g. "as of foot 1.28.0") with per-claim upstream anchors naming the section names of that release — usable only as a tier-C cross-check if the rubric ever admits tier C | rejected | 2026-10-22 | 180d | — |

Shape check on the three drafts (run against the counter's own parser: registry regex
`^\| S\d{3} \|`, 11-cell split, `status` at cell 8, `opened` at cell 9): each row has exactly 11
cells, `status = rejected`, `opened = 2026-10-22`, `recheck = 180d`, `used-by = —`, and **no cell
contains a `|`**. Because `status = rejected` (not `mined`), the C2 counter
(`.ufo/waves/round-23/c2/count.py REV`) will **not** count these rows for any terminal — which is
the intended outcome: they are taste evidence, not route support. The route support for foot, kitty
and ghostty is the mined upstream set owned by the C2 source seats.

---

## 3. Drafted search-log line (style of `corpus/SOURCES.md` § Search log)

Appended after the last existing round block, in the same shape as the round-17/19/21/22 entries.
**Not applied** — the integrator merges it.

> **Round 23 (2026-10-22)**, bounded question: do third-party (tier C) pages that restate where
> foot, kitty or ghostty read their configuration carry enough to support a C2-covered route row,
> and if not, why not? Searched: four web queries (`foot terminal emulator config file location
> ~/.config/foot/foot.ini blog guide`; `kitty terminal config file location ~/.config/kitty/kitty.conf
> guide blog`; `ghostty config file location ~/.config/ghostty/config guide blog`; `foot terminal
> emulator configuration guide blog foot.ini customize 2025`), 2026-10-22; identified 56 candidate
> URLs across the four result sets (10 + 10 + 18 + 18, duplicates counted once per result set),
> screened 56 by title/host/format, opened 4 by ordinary fetch (linuxjunkies.org kitty guide,
> michaelbommarito.com ghostty wiki, orioninsist.org foot blog, petronellatech.com ghostty guide),
> included 3 opened community pages — all **rejected** (S153 kitty, S154 ghostty, S155 foot: tier C
> cannot support a C2-covered entry; the kitty page's version token 0.35.2 is contradicted by
> upstream's release history; the ghostty page names the pre-1.3.0 `config` filename and pins a
> stale "1.2.0 (current stable)" table; the foot page names no foot version at all and teaches the
> `[colors]`/`colors.cursor` dialect upstream deprecated in foot 1.26.0), excluded 53 (52 never
> opened: upstream official docs, man pages, ArchWiki/Gentoo wiki mirrors, YouTube results,
> reddit/forum threads, GitHub discussion threads, dotfile repositories, DeepWiki; plus
> petronellatech.com, which returned HTTP 403 and is recorded unopened). Upstream tier-A yardstick
> pages were read for the comparison only and are already owned by the C2 source seats
> (S123–S152). Stop: one community page per terminal tree was opened and each fails the bar on a
> named, checkable defect; the upstream rows for these routes already exist, so further tier-C
> opens could only repeat the same rejection class and none of these rows can count toward the
> C2 3/3 counter.

---

## 4. Conflicts found upstream — reported verbatim for the canonical Rust judge

These are **upstream-vs-upstream** discrepancies I noticed while building the yardstick. They are
not my seat's claim to resolve; I record them verbatim so the judge is not handed a false
"upstream says X" in the ghostty tree.

1. **ghostty config filename: upstream docs vs upstream source.** Upstream's configuration guide
   (`https://ghostty.org/docs/config`, fetched 2026-10-22, 111,894 B, sha256
   `cb79ca5dcf496d81ed05862e1888958c307dc934988b3595926b2c17ab08b6b5`) says, at extracted L22:
   > "The configuration file is named config.ghostty (or `config` before 1.2.3),"

   Upstream's own source at tag **v1.2.3** still uses only the old name: `src/config/Config.zig`
   L3414 `.{ .subdir = "ghostty/config" }` (339,217 B, sha256
   `ed2eb047c44c3ad82d4e1e5d23240198e289e8bf34520c444105b4a3008a6e1e`), and the whole v1.2.3 tree
   contains **0** occurrences of `config.ghostty` (36,345,813 B tarball, sha256
   `e17d39482fc70fba3d72f5f25c12e9d9a72b87dd45a61a854d9928e98b69edd8`). The rename to
   `config.ghostty` is visible in the **v1.3.0** tree (37,412,762 B, sha256
   `3d05cbdb712ec19ecdc720a2757a09ebf79aaa8d90ae2ae5c0ddd5536ef31be6`; 8 files mention
   `config.ghostty`), where `src/config/file_load.zig` L14 is
   `.{ .subdir = "ghostty/config.ghostty" }` and L18-24 keeps the legacy path with the upstream
   comment `Ghostty <1.3.0 default path`. So upstream's documentation says the rename happened
   "before 1.2.3" while upstream's source history puts it at **1.3.0**. The community page S154 is
   rejected on the *source* boundary (v1.2.3 had only `config`; v1.3.0 introduced
   `config.ghostty`), which is the boundary upstream's own source comment states.

2. **ghostty gtk scrollbar: page vs upstream, in both directions.** The community page says the
   gtk scrollbar "is not yet in a stable release - it only exists in the main branch development
   builds" (L64). Upstream v1.3.0's `src/config/Config.zig` L1387-1403 does ship a `scrollbar`
   option (v1.2.3's file has 0 occurrences), but the same upstream comment block says:
   > "This only applies to macOS currently. GTK doesn't yet support scrollbars."

   So the page's GTK-specific claim is still consistent with upstream, while its blanket "not in a
   stable release" framing is not. I rejected S154 on the file-name/version-table contradiction
   instead, which does not depend on this nuance.

3. **kitty version arithmetic on the community page.** The kitty guide's sample `kitty --version`
   output is `kitty 0.35.2`; upstream's changelog dates 0.35.2 to 2024-06-22, and the page's own
   `dateModified` is 2026-06-07 — the release date of upstream 0.47.2. The page also gets the
   themes-kitten boundary right (upstream `kittens/themes.html` L1310 `Added in version 0.23.0: The
   themes kitten`; upstream changelog 0.23.0 [2021-08-16] at L952), which is why the rejection cites
   the stale version token and the missing override rather than a wrong version boundary.

---

## 5. Out of scope for this seat (and not done)

- **No `corpus/SOURCES.md` edit.** The three rows in §2 and the search-log line in §3 are drafts;
  landing and renumbering is the integrator's (L1) call.
- **No `corpus/knowledge/terminal-trees-r23.md`** was created or edited — that note belongs to the
  connector seat, and the C2 counter reads it at a revision.
- **No upstream mined rows** were drafted: the tier-A rows for foot/kitty/ghostty are owned by the
  C2 source seats (S123–S152).
- **No claim, counter or gate was re-run.** The C2 counter `c2/count.py`, the C1 tripwire repair
  set, the round-21 oracle, the precision and selftest guards were **not executed in this seat** —
  this seat produced no code and no corpus file, so there was nothing to guard. Every number above
  is a page/byte-level fact I measured directly; no counter value is claimed.
- **No candidate patch and no guard results**: this seat is a scribe and produces no product code,
  so there is no patch to deliver and no guard to report. Nothing was run that could write to the
  lane's index, jj state or working copy; no `jj` command was issued at all.
- **Host untouched**: no package installed or upgraded (`pacman -Q` reads only), no `~/.config`
  file written, no service or display state touched, no second runtime invoked.

---

## 6. Artifact paths

- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ScribeRejectSweep.md`
- Sibling C2 seat reports in the same directory (for the id-band and mined-row cross-reference):
  `SrcFoot.md`, `SrcKitty.md`, `SrcGhostty.md`, `HostFoot.md`, `HostKitty.md`, `HostGhostty.md`,
  `ConnSibling.md`.
- Round-23 C2 counter of record: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/c2/count.py`
- Round-23 registration (the three claims): `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/registration.md`
- Prior-round evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/` and
  `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-22.md`
- Raw fetch scratch (this seat's `/tmp`, not durable): `lj-kitty.html`, `bommarito.html`,
  `orion.html`, `kitty-conf.html`, `kitty-themes.html`, `kitty-changelog.html`,
  `kitty-glossary.html`, `ghostty-config.html`, `ghostty-releases.atom`, `foot-readme.md`,
  `f125.scd`, `footman.scd`, `footman-master.scd`, `f126.md`, `c-v1.2.3.zig`, `c-v1.3.0.zig`,
  `g-v1.2.3.tgz`, `g-v1.3.0.tgz`, `x-v1.2.3/`, `x-v1.3.0/`. Digests for every one of these are in
  §1.4; none is retained in the lane, so a later round must re-fetch and re-digest rather than
  trust these bytes.

---

## 7. Verdict

**Sweep complete; three tier-C community pages opened by ordinary means and all three rejected**
(S153 kitty, S154 ghostty, S155 foot), each on a named, upstream-checkable defect — stale or
contradicted version token for kitty, contradicted config filename and stale version table for
ghostty, no version anchor at all plus a config dialect upstream deprecated in foot 1.26.0 for
foot. Two upstream-vs-upstream conflicts recorded verbatim in §4 for the judge (ghostty's
`config.ghostty` rename boundary: docs say "before 1.2.3", source says 1.3.0; and the gtk scrollbar
option's macOS-only scope upstream states against the page's "main branch only" framing). Draft
rows and the search-log line are in §2 and §3 for the integrator; **nothing was landed**, and these
`rejected` rows do not count toward the C2 3/3 counter, whose mined route support is the upstream
set S123–S152 owned by the C2 source seats. No patch and no guard results are claimed, because
this seat changed no code and ran no counter.
