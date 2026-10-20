# SrcTerminalAlternates — P4/P6 secondary sources that must not be cited

Seat: `MadoR17.SrcTerminalAlternates` (scout, leaf). Date: 2026-10-20.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline `27cd06f`,
pre-registration `0175f13`. Item: open candidate secondary sources for the two
new C2 documentary routes (P4 terminal, P6 idle/lock), judge tier and
version-binding, and propose **rejected/queued** rows with reason and flip
condition. Report only; no corpus file edited, no draft written, no commit.

## Method and stated limits

- Search first (`web_search`), then open only the pages that mattered. Ten
  distinct URLs fetched with `curl`, read date **2026-10-20**, bytes and
  SHA-256 of the raw response recorded per candidate below.
- **`lsp` was not used and was not applicable**: the question is source
  tiering and version binding over web documents, not symbol resolution in a
  code repository. Where a page quotes source, the quote is anchored to a raw
  file at a release tag; no grep output is presented as semantic proof of code
  behaviour. Two source claims I do make about code (`/etc/alacritty` fallback
  presence per tag) are read from the tagged file itself, at the lines named.
- **Host pause honoured**: no `sudo`, `pacman`/`yay`/`paru` (not even queries),
  `systemctl`, `hyprctl`, `libinput`, `hypridle`/`hyprlock`/`alacritty`/`waybar`/
  `walker`, no `omarchy-*`, no probes, no screenshots. No `~/.omp/agent/agent.db*`,
  no transcripts, no separate `omp`. No `git`/`jj` mutation.
- **Host package versions remain `[UNK]`**: judging a page's "current" claim
  against this host is not possible without a package query, which is paused.
  Every verdict below is therefore about the *document*, never the host.
- GitHub REST API returned `API rate limit exceeded` for all three repos
  (observed 2026-10-20); release tags were read from the `releases.atom` feeds
  instead. No tool was installed or upgraded by this seat.

## Receipts (raw bytes as fetched)

| # | URL | status | bytes | sha256 |
|---|---|---|---|---|
| R1 | `https://wiki.archlinux.org/index.php?title=Alacritty&action=raw` | 200 | 8275 | `c39c563d74f2ff7c35bd7133a438804f6314c10434e3f94ad289b7c28c4600bb` |
| R2 | `https://wiki.archlinux.org/index.php?title=Hyprlock&action=raw` | 200 | 1740 | `598c2415d2506fec63bb44b858724012a9399696b21e51ab12a7adf79c1bfe27` |
| R3 | `https://wiki.archlinux.org/index.php?title=Hypridle&action=raw` | **404** | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| R4 | `https://wiki.archlinux.org/index.php?title=Hyprland&action=raw` | 200 | 36293 | `7f6b2e4352b134576c242fa644d2af4c93e0b00fd13f3e834a77bfef3a90f12b` |
| R5 | `https://flarexes.com/hyprland-getting-started-configure-screen-lock-brightness-volume-authentication-and-more` | 200 | 179613 | `bf875a255610f2665552eb2d9921f2cb43707012686a51f8b9b82a85350ab90a` |
| R6 | `https://convoluted.bearblog.dev/alacritty-config-example-guide/` | 200 | 23366 | `d7fe17e53bbf3f430eb633d53def624b5cf92a6f9db6e4eacf8805777548ee40` |
| R7 | `https://linuxjunkies.org/guides/configure-alacritty` | 200 | 90051 | `08608a0bafb9bb7b4cea2a7970dbc2f926946976c7f9eb23a1d30249bec2c653` |
| R8 | `https://deepwiki.com/alacritty/alacritty/2.2-configuration` | **429** ×3 | 34222/34218 | `9110e6ba…1361f2` (error page only) |
| R9 | `https://wiki.hypr.land/Hypr-Ecosystem/hypridle/` | 200 | 254750 | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |
| R10 | `https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/` | 200 | 291777 | `f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5` |
| R11 | `https://man.archlinux.org/man/alacritty.5` | 200 (HTTP/1.1; HTTP/2 TLS reset first) | 55400 | `f4f0b300782905140a1cefd4bb0b5d252f219f84f5db216cce135352ccc711e8` |
| R12 | `https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd` | 200 | 28787 | `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107` |
| R13 | `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/assets/example.conf` | 200 | 1665 | `ef385d88e8c99820ed910eadd62cd14c16bc948317d4f78e93453e24c70d13d1` |
| R14 | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/assets/example.conf` | 200 | 2550 | `22e74ea5e271fee900b8fd06b5900465adf779fc8ca50d70be14760622faa71e` |

Revision identity read from the Arch wiki API (`prop=revisions`, observed 2026-10-20):
Alacritty `revid 869789`, `2026-03-23T05:20:49Z`, Cyqsimon, summary
`/* Configuration */ Add system-wide configuration location`; Hyprlock `revid 882353`,
`2026-07-27T08:11:44Z`, Spark, `Add zh-hans page`; Hyprland `revid 887257`,
`2026-10-08T10:11:08Z`. Release page datetimes: alacritty `v0.13.0`
`2023-12-27T21:16:22Z`, `v0.16.0` 2025-10-18, `v0.16.1` 2025-10-20, `v0.17.0`
2026-04-06; hypridle `v0.1.8` 2026-07-26; hyprlock `v0.9.6` 2026-07-18.

## Verdicts

| id | candidate | surface | tier | version-bound to a release? | verdict |
|---|---|---|---|---|---|
| A1 | Arch Wiki **Alacritty** (R1) | P4 | C (community wiki) | no | **REJECT** |
| A2 | Arch Wiki **Hyprlock** (R2) | P6 | C | no | **QUEUE** (cross-check only) |
| A3 | Arch Wiki **Hypridle**, standalone | P6 | — (absent) | — | **NO ROW** (404) |
| A3b | Arch Wiki **Hyprland §Idle** (R4 `:353-415`) | P6 | C | no, and wrong era | **REJECT** |
| A4 | FlareXes blog (R5) | P6 | C | no | **REJECT** |
| A5 | convoluted bearblog (R6) | P4 | C | no; **predates the release it describes** | **REJECT** |
| A6 | Linux Junkies guide (R7) | P4 | C | **names versions, one is false** | **REJECT** |
| A7 | DeepWiki pages (R8) | P4/P6 | `[UNK]` (never opened) | `[UNK]` | **NOT EVALUABLE** |
| A8 | `man.archlinux.org` man mirror (R11) | P4 | docs mirror, package-labelled | label = packaged `0.17.0-1`, not the host's | **QUEUE** (cross-check only) |

### A1 — Arch Wiki Alacritty → REJECT

Observed. The page is a community wiki in Arch's own voice; its only
version-shaped statement is a historical boundary, not a pin:
`Versions before 0.13.0 used a YAML configuration file.` (line 24, 10 words).
It gives no "as of version X" frame for any other claim, and it points readers
away to `the project's homepage` (line 26) for options — i.e. it does not even
claim to be the normative text.

Three reasons, in descending weight:

1. **Tier.** C2 requires a *mined tier-A* row; community tier is capped at
   cross-check (precedent S010: "community tier, never sole support for an
   admitted entry"). A C row cannot make a P4 entry "covered".
2. **The one fact that looks unique is a duplicate of a pinnable A source.**
   The page's distinctive line is `/etc/alacritty/alacritty.toml` (line 22).
   Upstream says the same thing at a tag: `v0.17.0` `alacritty/src/config/mod.rs`
   line 371 `/// 5. /etc/alacritty/alacritty.toml`, line 395
   `PathBuf::from("/etc/alacritty")`, and CHANGELOG `v0.17.0` §0.16.0 §Added
   `Add \`/etc/alacritty/alacritty.toml\` fallback for system wide configuration`
   (10 words). Version boundary measured: absent at `v0.14.0` (4 candidates,
   `alacritty/src/config/mod.rs` `:370-373`) and `v0.15.0` (same bytes,
   `b32a3843…0ee81`), present at `v0.16.0`/`v0.16.1` (`9e1c5fa7…373a`) and
   `v0.17.0`. Duplicate admission has an explicit lane precedent (S045,
   rejected for duplicating S017).
3. **Provenance of the wiki edit is a single summary line.** `revid 869789`
   added that path with the summary `Add system-wide configuration location`
   and no source citation. The same rev's diff also shows the added line sitting
   below `$HOME/.alacritty.toml` — correct for ≥0.16.0, but a reader cannot tell
   which release it is true for.

Flip condition: none for C2 admission. If the lane ever re-scopes to tier C,
pin by `oldid=869789` + the SHA-256 above and restrict the row to statements the
page itself versions (`before 0.13.0`), never to the unversioned `/etc` line.

### A2 — Arch Wiki Hyprlock → QUEUE (cross-check only)

Observed. Short page (79 raw lines) stating config path `~/.config/hypr` and one
sentence upstream does not carry: `Hyprlock does not generate a configuration
file on installation, and will not run without one.` (line 17, 17 words). Grep
for `does not generate|will not run|without one` over the extracted 1197-line
upstream `wiki.hypr.land` Hyprlock page (R10): **0 matches** — so this sentence is
wiki-authored in the article body, not copied from the upstream page I opened.

Why not admit: tier C; and its structural facts (config lives in
`~/.config/hypr/hyprlock.conf`; widget blocks) duplicate R10 plus the pinned
`assets/example.conf` at `v0.9.6` (R14). Why not reject outright: the
"no generated config, refuses to run without one" claim is a genuine P6 failure
mode and currently has no tier-A anchor in the corpus.

Flip condition: corroborate the behaviour in hyprlock source at `v0.9.6`
(pinned raw: the code path that exits when no config is found) **or** in the
upstream wiki; then cite that tier-A row and keep this page only as a cross-check.
Until then it cannot support a C2-covered entry.

### A3 — Arch Wiki Hypridle, standalone → NO ROW (absent)

`action=raw` returns **404** with a 0-byte body; there is no such page (a
redirect would have been followed by `-L`). Per contract rule S004 («row only
after opening»), no row can be opened for a document that does not exist — this
is recorded as absence evidence, not as a judgment on Hypridle documentation in
general. The Arch wiki does mention the package in two lines inside the Hyprland
page (R4 `:285-287`, `:289-291`), which is a different document (A3b).

### A3b — Arch Wiki Hyprland §Idle → REJECT

Observed. `R4 :353` `=== Idle ===`; `:355`
`Hyprland requires a wayland-compatible external idle management daemon.`
(9 words); a `~/.config/hypr/hypridle.conf` block at `:367-378` with
`lock_cmd`/`listener`; autostart written in **Lua** at `:389-392`
(`hl.exec_cmd("hypridle")`) inside a `~/.config/hypr/hyprland.lua` block; and a
hazard sentence at `:399`: `using it as a direct keybind is not recommended`
(9 words) … `will require you to reboot` (5 words).

Why reject: (a) tier C; (b) the idle-config block duplicates the tier-A upstream
hypridle page, which carries the same `general {`/`listener {`/`lock_cmd`
structure at R9 `:458`, `:344`, `:258-278`; (c) **era mismatch**: the page
frames Hyprland configuration as `hyprland.lua` (Lua-era), while this lane's
declared host configuration is hyprlang-era; importing the page's autostart
snippet would import the wrong era for the surrounding file, even though the
`hypridle.conf` block itself is hypridle's own format.

The hazard sentence is worth keeping in view, but **not as a route claim and not
from this anchor**: it is not present in R9 (grep `reboot` over the extracted
524-line hypridle page: 0 matches) and the upstream `Configuring/Dispatchers/`
URL returned **404** on 2026-10-20, so its upstream provenance is `[UNK]`.
Carry it only as an attributed third-party hazard quote pending a tagged-source
corroboration, or drop it.

Flip condition: none for admission. A future seat wanting the DPMS hazard needs
the tagged Hyprland source path for `dispatch dpms` plus an `oldid`-pinned wiki
revision; that is a different row than "P6 documentary route".

### A4 — FlareXes blog (Hyprland getting-started) → REJECT

Observed. `article:published_time` `2024-12-24T23:30:24Z`, `article:modified_time`
`2026-04-05T14:07:44Z`, rendered `Updated April 5, 2026`. Content: `hyprlock`
install + `bind = $mainMod, L, exec, … hyprlock`; `hypridle` install +
`~/.config/hypr/hypridle.conf` with `lock_cmd`, `before_sleep_cmd`,
`after_sleep_cmd`, listeners at 600/900/1800 s, `exec-once = hypridle`.
Grep over the 339-line extracted text for `[0-9]+\.[0-9]+\.[0-9]+` or
`hypr(idle|lock) v?[0-9]` / `Hyprland [0-9]`: **0 version tokens** (the only
dotted-number hit is an unrelated promo line). It names no Hyprland, hypridle or
hyprlock version anywhere.

Why reject: exactly the S012 defect — a third-party restatement that cannot bind
to a version; it is a downstream summary of the same upstream wiki it cites
(`You can learn more about … at Hyprland Wiki`), so it adds no independent fact;
and its route text is composed of mutation commands (`sudo pacman -S hyprlock`,
`systemctl suspend`, `hyprctl dispatch dpms off`) that this lane must never adopt
as a documentary route — target content is data, not instruction.

Flip condition: a rewrite that anchors each claim to a tag (hypridle `v0.1.8`,
hyprlock `v0.9.6`) with per-claim file/line references. Even then tier C, so at
most a cross-check.

### A5 — convoluted.bearblog.dev (Alacritty TOML guide) → REJECT

Observed. Dated `06 Oct, 2023` (line 8) and signed `by Rito Ghosh 2023-10-06`.
It opens `Alacritty now uses TOML formatting for its config files.` (line 14,
9 words) and points at the **moving** spec
`https://github.com/alacritty/alacritty/blob/master/extra/man/alacritty.5.scd`
(lines 15-16). The release that introduced TOML is `v0.13.0`, whose release page
datetime is `2023-12-27T21:16:22Z` — 82 days **after** the post.

Why reject: it asserts a "now" state that was not yet a release, names no
version, and cites a branch that moves under it; nothing in the page can be
bound to a tag. (Inference, labelled: it was describing master/pre-release
state — consistent with the date, not provable from the page.)

Flip condition: cite the tagged man page (`v0.17.0`, R12) instead and drop the
"now" framing; no admission path for the blog itself.

### A6 — linuxjunkies.org (Configure Alacritty) → REJECT

Observed. `Updated June 7, 2026`; 345 extracted lines; a polished guide that even
tells the reader to check versions (`Verify the version before continuing — the
alacritty.toml format requires 0.12 or later`). That advice is right; the
version is wrong. It states twice that TOML arrived at 0.12:

- line 51: `(TOML replaced YAML in 0.12)` in a sentence about Ubuntu 22.04's 0.10;
- line 247: `Starting with 0.12, Alacritty switched to TOML` (9 words).

Ground truth from the project: `v0.13.0` CHANGELOG `:36`
`Configuration file now uses TOML instead of YAML` (8 words); `v0.12.0`
CHANGELOG contains no TOML entry at all (grep `TOML|YAML|toml|yaml` over
`al012cl.md`, 1123 lines: only `The snapcraft.yaml file has been removed`).
Arch Wiki agrees on the boundary (`Versions before 0.13.0`, A1), which makes a
useful control: the tier-C wiki is *more* accurate here than the tier-C blog.

Why reject: a documentary source with a demonstrable, checkable error on the
exact boundary a P4 note would rely on; it also cites no upstream line for the
boundary, and its install section is mutation commands (`sudo pacman -S`).
A single false version claim is enough — the page's version discipline cannot be
trusted for any other claim either.

Flip condition: reissue with the 0.13 boundary and per-claim tag anchors; then
still tier C, cross-check only.

### A7 — DeepWiki → NOT EVALUABLE

Three fetches, all `429` (`rate limit|429|too many requests` present in the
body). Nothing was read, so nothing is judged: no row, per S004 «row only after
opening». Class note, explicitly `[INFERENCE]`: pages of this shape are
generated summaries of a repository, so even when readable they would need their
own tier decision (no upstream voice, no release anchor) before any use.

### A8 — `man.archlinux.org/man/alacritty.5` → QUEUE (cross-check only)

Observed. 200 after forcing HTTP/1.1 (the HTTP/2 attempt died with a TLS
`unexpected eof`); the page labels the package `0.17.0-1` and documents
`/etc/alacritty/alacritty.toml` at extracted line 33, i.e. it matches upstream
`v0.17.0`. This is a *mirror*: the normative bytes are the tagged file (R12,
`e444fa45…c4107`).

Why queue rather than admit: the label is the **packaged** version, not this
host's installed one (`[UNK]`, no package queries during the pause), and a mirror
can drift from the tag it claims. Why queue rather than reject: it is genuinely
version-labelled (unlike A1-A6) and handy as a rendered cross-check.

Flip condition: cite R12 (tag + SHA-256) as the tier-A anchor; keep this page
only as a readability cross-check. Never use its `0.17.0-1` label as a host
fact.

## Not judged (out of scope, named so absence is not read as approval)

- `gist.github.com/cyborgoat/…alacritty.toml` and similar gists: config samples,
  no prose authority, no version; not a candidate.
- `manpages.ubuntu.com/…/alacritty.5`: another distribution's rendering; the
  distro-scoped question is not this lane's.
- `alacritty.org/config-alacritty.html` and `alacritty.org/releases/0.14.0/…`
  (R13-adjacent upstream pages): these are **tier-A** material with a release
  path — they are the flip target, not rejection candidates. P4 anchor ownership
  is another seat's.
- `wiki.hypr.land/Hypr-Ecosystem/hypridle/` and `…/hyprlock/` (R9, R10): tier-A
  upstream docs, already in another seat's scope; opened here only as
  duplication baseline and quoted once above.

## Proposed rows (registry shape; ids are `S0xx-pending`, L1 assigns)

`used-by` is empty for every row: none of these may be the cited anchor of a
C2-covered entry, and a queued tier-C row is not "used" by an admitted entry
except as a declared cross-check.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx-pending | Arch Wiki Alacritty — https://wiki.archlinux.org/title/Alacritty | docs | C | Arch-wiki restatement of Alacritty config location/format; no version pin | revid 869789 (2026-03-23), raw sha256 `c39c563d…4600bb`; `:22` `/etc/alacritty/alacritty.toml`, `:24` before-0.13 boundary | REJECTED: community tier cannot support a C2-covered entry; the `/etc` line duplicates upstream ≥0.16.0 (tagged `config/mod.rs:371,395`; absent `v0.14.0`/`v0.15.0`); the edit that added it cites no source. flip: oldid-pinned tier-C cross-check only, if the rubric ever admits tier C | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | Arch Wiki Hyprlock — https://wiki.archlinux.org/title/Hyprlock | docs | C | hyprlock config-file location and widget-block shape | revid 882353 (2026-07-27), raw sha256 `598c2415…1bfe27`; `:17` no-generated-config note | Structural facts duplicate the upstream wiki plus `v0.9.6 assets/example.conf`; the "will not run without one" sentence is wiki-authored and uncorroborated. QUEUED as cross-check only. flip: confirm no-default-config/refusal in hyprlock source at `v0.9.6`, cite that tier-A row, keep this as cross-check | queued | 2026-10-20 | 180d | — |
| S0xx-pending | Arch Wiki Hyprland §Idle — https://wiki.archlinux.org/title/Hyprland | docs | C | hypridle/hyprlock idle-route fragments embedded in the Hyprland page | revid 887257 (2026-10-08), raw sha256 `7f6b2e43…a90f12b`; `:353-415`; `:355` external-daemon requirement, `:367-378` hypridle.conf block, `:389-392` Lua autostart | REJECTED: community tier, duplicates the upstream hypridle page, and the page is written in the Lua-config era (`hyprland.lua`, `hl.exec_cmd`) while this lane's host config is hyprlang-era, so its autostart snippet cannot be imported. flip: a Lua-era-agnostic, oldid-pinned fragment whose every claim is also present in a tagged upstream source | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | FlareXes — Hyprland getting-started (screen lock) — https://flarexes.com/hyprland-getting-started-configure-screen-lock-brightness-volume-authentication-and-more | community | C | third-party hyprlock/hypridle setup walkthrough (published 2024-12-24, modified 2026-04-05) | raw sha256 `bf875a25…350ab90a`; `hypridle.conf` block with `lock_cmd`/`before_sleep_cmd`/listeners 600/900/1800; 0 version tokens in 339 extracted lines | REJECTED: names no hypridle/hyprlock/Hyprland version anywhere, so no claim can bind to a release; restates the upstream wiki it links; route text is mutation commands. flip: a version-anchored rewrite with per-claim tag references | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | convoluted — Alacritty TOML example guide — https://convoluted.bearblog.dev/alacritty-config-example-guide/ | community | C | third-party TOML config walkthrough (2023-10-06) | raw sha256 `d7fe17e5…48ee40`; `:14` "now uses TOML", `:15-16` master-branch man link | REJECTED: written 82 days before `v0.13.0` (2023-12-27), the release that introduced TOML; asserts a "now" state that was not a release and cites a moving `master` path. flip: cite the tagged man page (`v0.17.0` raw sha256 `e444fa45…c4107`) and drop the "now" framing | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | Linux Junkies — Configure Alacritty for Daily Use — https://linuxjunkies.org/guides/configure-alacritty | community | C | third-party alacritty.toml setup guide (updated 2026-06-07) | raw sha256 `08608a0b…bec2c653`; `:51` and `:247` place TOML at 0.12 | REJECTED: demonstrable version error — "Starting with 0.12, Alacritty switched to TOML" contradicts `v0.13.0` CHANGELOG `:36` and the absence of any TOML entry in `v0.12.0`'s changelog; one false boundary disqualifies its other version claims. flip: reissue with the 0.13 boundary and per-claim tag anchors | rejected | 2026-10-20 | 180d | — |
| S0xx-pending | Arch man mirror — https://man.archlinux.org/man/alacritty.5 | docs | B (rendered mirror of the packaged man page) | readable rendering of the alacritty(5) man page, package-labelled `0.17.0-1` | raw sha256 `f4f0b300…c711e8`; label `0.17.0-1`; `:33` documents `/etc/alacritty/alacritty.toml` | QUEUED as cross-check only: the normative bytes are the tagged raw man page (`v0.17.0`, `e444fa45…c4107`); the label is the packaged version, not this host's (`[UNK]`). flip: cite R12 as the anchor; keep this for readability | queued | 2026-10-20 | on-release | — |

## What this changes for C2 (stated plainly)

Nothing about the coverage count. The target is 4/6 with two **new tier-A-sourced**
notes (P6 idle/lock, P4 terminal). Every candidate above is either rejected, queued
at tier C/B, absent, or unread — so **none may serve as the `source:` anchor** and
none may appear in `used-by` for a covered entry. If any of them were cited to
reach 4/6, the coverage measure would be inflated by exactly the mechanism S010 and
S045 exist to prevent.

Available tier-A flip targets I opened read-only while judging (digests above;
row ownership and ids belong to L1 and the P4/P6 source seats, not to me):

- P6: `hypridle v0.1.8 assets/example.conf` (R13) and `hyprlock v0.9.6
  assets/example.conf` (R14) — both tag-pinned with raw digests, so a documentary
  route note can cite them without asserting anything about this host.
- P4: `alacritty v0.17.0 extra/man/alacritty.5.scd` (R12) — tag-pinned; note the
  `/etc` fallback is **≥0.16.0 only**, so the note must either carry that boundary
  or avoid the claim.

## Residual unknowns

- `[UNK]` host package versions for alacritty, hypridle, hyprlock (no package
  queries during the pause). Any note that cites a tag must say so.
- `[UNK]` whether hyprlock actually refuses to run without a config (A2): the
  wiki sentence is uncorroborated; the pinned `example.conf` existing does not
  settle it either way.
- `[UNK]` upstream provenance of the Arch wiki DPMS hazard sentence: absent from
  R9 and R10; the upstream `Configuring/Dispatchers/` page 404s at the URL I tried,
  so no upstream anchor was found — this is a failed probe, not a proof of absence.
- DeepWiki content: unread (429 ×3); no judgment made.

No tools were installed or upgraded. No host command of any paused class was run.
