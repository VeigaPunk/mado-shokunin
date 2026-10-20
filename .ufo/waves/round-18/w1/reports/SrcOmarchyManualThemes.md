# SrcOmarchyManualThemes — Omarchy 3 manual, theme chapter (P5 / P3 documentary)

Seat `MadoR18.SrcOmarchyManualThemes` · scout · 2026-10-20 · lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`.
Item: open the Omarchy manual's theme page(s) with receipts; record the
version/date marker and quotes about theme switching, custom themes and
backgrounds; judge tier (official docs, unversioned).

Written by this seat: this report and
`.ufo/waves/round-18/fetch/SrcOmarchyManualThemes/**` only (8 body files +
`receipts.jsonl`). No corpus/SOURCES/QUALITY/SKILL/SCORECARD/LOG/PROVINCE or
`.gitignore` write; no git or jj write; no host binary, compositor, service or
package query; no pacman/sudo. Tooling: none installed (curl 8.23.0 and
python3 already present).

## 0. Axes this serves

- **C2 P5 (theme/wallpaper)** — a tier-A upstream docs row plus verbatim,
  receipt-anchored quotes for `corpus/knowledge/theme-route-r18.md`.
- **C2 P3 (walker)** — secondary only: the same book names walker as a styled
  consumer and documents `~/.config/walker/config.toml`; the P3 note's primary
  upstream row should stay Walker's own README/code row.
- C1/C3 untouched; no claim text or instrument touched.

## 1. Fetches — 8 receipts, all HTTP 200, raw bodies committed

Directory `.ufo/waves/round-18/fetch/SrcOmarchyManualThemes/`; one JSON line
per fetch in `receipts.jsonl` (`schema: mado-fetch-receipt-v1`, keys `url`,
`final_url`, `http_status`, `fetched_at`, `bytes`, `sha256`, `body`, `tool`).
All bodies re-hashed by this seat after writing: 8/8 match.

| body | url | bytes | sha256 | fetched (UTC) |
|---|---|---|---|---|
| `themes` | https://learn.omacom.io/2/the-omarchy-manual/52/themes | 33489 | `d7f4d12c46debca3c778e2af5df358e61f847c2673cc7d1dd69078330e4d29ab` | 2026-10-20T15:40:42Z |
| `backgrounds` | https://learn.omacom.io/2/the-omarchy-manual/89/backgrounds | 26413 | `7abca300dd3a1078921f12b2b3da1d26dd8e8e688c0528f770e88cafbb5ff3d1` | 2026-10-20T15:40:42Z |
| `extra-themes` | https://learn.omacom.io/2/the-omarchy-manual/90/extra-themes | 56306 | `810ffe119e04f6bdc2a416664dfa344f8291a182bcd8a1fbf318bea742557819` | 2026-10-20T15:40:43Z |
| `making-your-own-theme` | https://learn.omacom.io/2/the-omarchy-manual/92/making-your-own-theme | 28436 | `e527e4a70cd22fca38091809ce9b334e9d0e6a09d4ad71ec981b1c99edc31c9d` | 2026-10-20T15:40:43Z |
| `book-index` | https://learn.omacom.io/2/the-omarchy-3-manual | 168519 | `a00970d4ceb77c2da9e2a253034f8b6f4ff4bb31a8c72e45210cd77aba92a06e` | 2026-10-20T15:40:43Z |
| `manual.md` | https://learn.omacom.io/2/the-omarchy-manual.md | 121693 | `a2409deb5c87328da30afb35664f186088aad6b57278be53fc28592ac7885422` | 2026-10-20T15:41:42Z |
| `omarchy-cli` | https://learn.omacom.io/2/the-omarchy-manual/115/omarchy-cli | 28195 | `ef003b67e3e2ccea997063c7a76c8ee362d22077cffaff3910d5b5eb49b9cd59` | 2026-10-20T15:43:31Z |
| `dotfiles` | https://learn.omacom.io/2/the-omarchy-manual/65/dotfiles | 30455 | `b00ebd292a91482d11ef804e98971bcb3b6a0a9320147bdf88ed074f05c63b8f` | 2026-10-20T15:43:31Z |

`final_url` equals `url` for all 8 (no redirects). The `.md` URL is the
book's own whole-book export (frontmatter `title/author/url`), receipted
above.

No tag-pinned raw URL exists for this source: the manual exposes no tag,
commit or date. The receipt sha256 is therefore the only pin, exactly as
R17-V3 requires. No `git ls-remote` step applies (not a GitHub repo page).

### Tamper check (exercised)

A local verifier that re-reads `receipts.jsonl` and re-hashes each body
returned `8 receipts, mismatches: []` (exit 0); the same check on a `/tmp`
copy of the directory with one byte appended to `themes` returned
`mismatches: ['themes']` (exit 1). So the receipt set distinguishes the fetched
bytes from an altered copy.

### Re-fetch stability (probe, uncommitted)

The HTML pages are **not byte-stable per fetch**: each response embeds a fresh
`<meta name="csrf-token">` and search-form `authenticity_token`. A second
fetch of `52/themes` this session raw-sha
`f4c84e69adac8f0b02bcc19dbf86d8c15f24962e42c10b549d290a6adc95e413` vs the
committed `d7f4d12c…`; after masking those token values the diff is **0
lines**. The `.md` export has no tokens and re-fetched byte-identical
(`a2409deb…`). So a receipt pins the committed instance, not a digest a later
fetch must equal; any closure re-fetch must mask the two token values (or
compare `manual.md`).

## 2. Version / date marker (anchors in receipted bodies)

1. **Edition title.** `manual.md:1-5` YAML frontmatter:
   `title: "The Omarchy 3 Manual"`, `author: "DHH"`,
   `url: "https://learn.omacom.io/2/the-omarchy-manual"`. Every page's
   `<title>` repeats it, e.g. `themes:4`
   `<title>Themes · The Omarchy 3 Manual · DHH</title>`; breadcrumb
   `themes:153` links `The Omarchy 3 Manual`.
2. **Supersession banner (the closest thing to a version pin).**
   `manual.md:9` — Q24: "this is the legacy manual for Omarchy v3"; the same
   line says the latest release, "Quattro", has its own manual at
   `https://omarchy.org/manual/`.
3. **No content date, no content commit.** Body text carries no date on any
   fetched page; the HTTP response has **no `Last-Modified`** (HEAD at
   2026-10-20T15:40:56Z). Two response headers are *not* content pins:
   `x-version: 1.2.3` (Writebook app version) and
   `x-rev: a1bbbc817540498eb97b9966b3ef5b2bca547e96` (deployment revision).
   The header probe is **not** receipted because the response carries
   `Set-Cookie` session material; values recorded here as observation only.
4. **Temporal anchor = the receipts.** `fetched_at` per body above is the only
   time the bytes are known to have existed. A later re-fetch that changes a
   sha is a recheck trigger, not a contradiction.

Consequence: the manual is **major-pinned ("Omarchy 3", now declared legacy),
patch-unversioned**. It cannot bind statements to the host's v3.8.4 checkout;
host version facts must come from file reads (other seats).

## 3. Tier judgement

**Tier A — kind `docs`, official first-party, unversioned.**

- Provenance: the Omarchy manual (learn.omacom.io), frontmatter author DHH,
  page titles suffixed `· DHH`. This is the project's own documentation
  surface, not a community restatement — the same provenance class as S005
  (wayland-protocols README, tier A) and S009 (freedesktop architecture,
  tier A).
- The unversioned fact is a **scope/anchor** fact, not a tier demotion: S064
  (hyprlock wiki, tier A) is the precedent — its row states "Latest git" in
  scope. Here the scope must state "Omarchy 3 legacy manual, unversioned
  within v3; fetched 2026-10-20"; the receipt pins the actual bytes.
- It supports **declared-contract** claims about Omarchy 3 (what the manual
  says exists and how it tells users to drive it). It supports **no host
  fact** and nothing about the Quattro line. Because the site itself declares
  the manual legacy, the row's teaches/scope should keep the word "legacy" so
  a closure does not read it as current-release documentation.

## 4. Verbatim quotes (each ≤25 words; body line anchors)

Quotes are the **rendered** text (HTML `<em>/<code>` wrappers and `&gt;`
entities decoded); anchors point at the raw line in the receipted body.
`manual.md` anchors are the book's own markdown export.

| # | quote | anchor | supports |
|---|---|---|---|
| Q1 (6w) | "Omarchy comes with nineteen beautiful themes." | `themes:216` | built-in theme count |
| Q2 (18w) | "You can select between them via Style > Theme in the Omarchy Menu (Super + Alt + Space)" | `themes:216` | menu switching route |
| Q3 (14w) | "hop directly to the theme selector using Super + Ctrl + Shift + Space" | `themes:216` | direct hotkey route |
| Q4 (23w) | "Each theme styles the desktop, terminal, neovim, activity screen (btop), notifications (mako), top bar (waybar), application launcher (walker), and the lock screen (hyprlock)." | `themes:218` | theme→consumer list incl. walker, waybar, hyprlock |
| Q5 (18w) | "Themes have a set of background images that you can pick between using Super + Ctrl + Space." | `themes:220` | per-theme background sets; selection hotkey |
| Q6 (16w) | "Themes can also have a custom unlock design, which is used for the boot decryption process." | `themes:283` | theme→unlock (boot decryption) design |
| Q7 (8w) | "All the backgrounds for Omarchy live in ~/.config/omarchy/backgrounds/[theme]." | `backgrounds:216` | background file plane, one dir per theme |
| Q8 (18w) | "You can do this most easily by going to Install > Style > Background in the Omarchy Menu." | `backgrounds:218` | menu route to add backgrounds |
| Q9 (12w) | "You can find a huge collection of cool curated backgrounds on https://github.com/dharmx/walls." | `backgrounds:220` | external collection pointer (not a host fact) |
| Q10 (8w) | "You can add your own themes to ~/.config/omarchy/themes." | `making-your-own-theme:216` | custom theme directory |
| Q11 (13w) | "Just copy one of the existing ones as a base (look in ~/.local/share/omarchy/themes)" | `making-your-own-theme:216` | shipped theme base dir |
| Q12 (9w) | "The main file you have to tweak is colors.toml." | `making-your-own-theme:218` | custom theme's single source of colors |
| Q13 (17w) | "used to generate configurations for the terminal (Ghostty/Alacritty/Kitty), btop, Chromium, Hyprland, Hyprlock, Mako, SwayOSD, Walker, and Waybar" | `making-your-own-theme:218` | colors.toml→consumer generation incl. Walker/Waybar/Hyprlock |
| Q14 (18w) | "You can also use the included Aether application to create a new theme using a lovely GUI interface" | `making-your-own-theme:220` | Aether GUI authoring path |
| Q15 (19w) | "If you're making a light mode theme, drop an empty file called light.mode in the root of your theme." | `making-your-own-theme:224` | light-mode marker file contract |
| Q16 (14w) | "Themes supplied with unlock.png and preview-unlock.png images will be listed under Style > Unlock." | `making-your-own-theme:232` | unlock images→Style > Unlock listing |
| Q17 (6w) | "follow the naming convention of omarchy-[themename]-theme" | `making-your-own-theme:236` | distribution naming contract |
| Q18 (19w) | "You can install any of these themes by copying the GitHub URL and selecting Install > Style > Theme" | `extra-themes:216` | extra-theme install route (GitHub URL) |
| Q19 (11w) | "just use Remove > Style > Theme and select it there" | `extra-themes:216` | extra-theme removal route |
| Q20 (4w) | "omarchy theme set <name>" | `omarchy-cli:233` (help text "Apply a theme") | CLI switching route; `omarchy theme list` at `:232` |
| Q21 (13w) | "Controls your lock screen, but this is symlinked to your theme for styling." | `dotfiles:242` | `~/.config/hypr/hyprlock.conf` is theme-symlinked (row begins `:241`) |
| Q22 (11w) | "Controls your top bar design, but it's symlinked to your theme." | `dotfiles:250` | `~/.config/waybar/style.css` is theme-symlinked (row begins `:249`) |
| Q23 (7w) | "Controls your launcher that's run with Walker." | `dotfiles:254` | `~/.config/walker/config.toml` exists as walker's launcher config (row begins `:253`) |
| Q24 (8w) | "this is the legacy manual for Omarchy v3" | `manual.md:9` | version/supersession marker |
| Q25 (13w) | "The latest release of Omarchy, called Quattro, has its own manual at https://omarchy.org/manual/" | `manual.md:9` | current-line manual is elsewhere; this book is v3 |

Measured structure (not quotes): 19 `<em>` theme entries at
`themes:225-279` (Tokyo Night … White) and 19 unlock entries at
`themes:286-340`, matching "nineteen" (Q1). The extra-themes gallery carries
117 unique `https://github.com/...` links (one per theme repo); the manual
never states their content.

## 5. What the manual declares — and what it does not

Declared documentary contract for P5 (all from `themes`, `backgrounds`,
`extra-themes`, `making-your-own-theme`, plus `omarchy-cli`/`dotfiles`):

- Three switching routes: menu `Style > Theme` (Super+Alt+Space), direct
  selector Super+Ctrl+Shift+Space, CLI `omarchy theme set <name>` /
  `omarchy theme list` (Q2, Q3, Q20).
- 19 built-in themes; each restyles desktop, terminal, neovim, btop, mako,
  waybar, **walker**, hyprlock (Q1, Q4); theme-specific unlocks for boot
  decryption (Q6).
- Backgrounds are per-theme files under
  `~/.config/omarchy/backgrounds/[theme]`; added via
  `Install > Style > Background`; selected with Super+Ctrl+Space (Q5, Q7,
  Q8); an external curated collection is linked (Q9).
- Custom themes live in `~/.config/omarchy/themes`, copied from
  `~/.local/share/omarchy/themes`; `colors.toml` is the one file to edit and
  it **generates configs for** terminal apps, btop, Chromium, Hyprland,
  Hyprlock, Mako, SwayOSD, Walker, Waybar (Q10-Q13); Aether is a GUI
  authoring path (Q14); `light.mode`, `icons.theme` (raw
  `making-your-own-theme:228`), `unlock.png`/`preview-unlock.png` widen the
  theme contract (Q15, Q16); distribution uses public git plus the
  `omarchy-[themename]-theme` naming convention (Q17).
- Extra themes are installed by copying their GitHub URL into
  `Install > Style > Theme`, removed via `Remove > Style > Theme` (Q18, Q19).
- File-plane declarations: `~/.config/hypr/hyprlock.conf` and
  `~/.config/waybar/style.css` are **symlinked to the theme** (Q21, Q22);
  `~/.config/walker/config.toml` is walker's config but is **not** declared
  symlinked (Q23) — do not claim a theme→walker-config symlink from this
  source.

**Not declared (measured zero hits, case-insensitive, whole `manual.md`):**
`swaybg` 0, `hyprpaper` 0, `wallpaper` 0, `elephant` 0. Therefore this source
cannot support any "backgrounds are painted by swaybg/hyprpaper" claim, and it
cannot support walker's provider (`elephant`) semantics. Those remain `[UNK]`
from the documentary route; the backgrounds page documents **choices and file
locations only**, never the renderer. `walker` itself appears 4× in the whole
book: styled consumer (`manual.md:143`), clipboard-history provider
(`:666`), `~/.config/walker/config.toml` (`:1371`), and colors.toml target
(`:1987`) — no launcher/provider mechanics.

Also absent from the theme pages: hooks and reload/restart semantics (the
chapter text has no `hook`/`reload`/`restart` line). The only theme commands
shown are `omarchy theme list|set` plus `omarchy plymouth preview` for unlock
images (`making-your-own-theme:232`); the CLI help block is quoted output, not
a behavior description. The P5 note's "Unexercised behavior" section should
not borrow facts from here beyond what the quotes state.

## 6. Proposed SOURCES row (S0xx-pending; L1 assigns the id)

Paste-ready line (one table row; no inner `|` in cells). `used-by` names the
new P5 note; add `corpus/knowledge/walker-route-r18.md` **only if** that note
actually cites this id (the scope does name walker styling).

```
| S0xx-pending | The Omarchy 3 Manual (DHH) — theme chapter — https://learn.omacom.io/2/the-omarchy-manual/52/themes | docs | A | P5 theme/wallpaper documentary surface: theme switching, colors.toml→walker/waybar/hyprlock generation, background file plane, custom and extra theme acquisition; Omarchy 3 legacy manual, unversioned within v3 (host 3.8.4 not bound) | themes:216-283, backgrounds:216-220, extra-themes:216, making-your-own-theme:216-236, omarchy-cli:232-233, dotfiles:241-253, manual.md:2-9,740-741,1371,1552-2013 @ fetched 2026-10-20 (no content date or commit; body sha256 themes d7f4d12c…, backgrounds 7abca300…, extra-themes 810ffe11…, making e527e4a7…, manual.md a2409deb…; receipts .ufo/waves/round-18/fetch/SrcOmarchyManualThemes/receipts.jsonl) | theme switching via menu/hotkey/CLI `omarchy theme set`; 19 built-ins each styling walker/waybar/hyprlock; backgrounds under ~/.config/omarchy/backgrounds/[theme] chosen with Super+Ctrl+Space; custom themes in ~/.config/omarchy/themes driven by colors.toml; extra themes installed by GitHub URL; hyprlock.conf and waybar/style.css theme-symlinked; manual never names swaybg/hyprpaper/wallpaper/elephant | mined | 2026-10-20 | 180d | corpus/knowledge/theme-route-r18.md |
```

Why the C2 P5 row test passes: `source` names the theme chapter and carries
an upstream `https://` docs URL; `scope` names theme/wallpaper; status
`mined`; tier A; every credited quote sits in a receipted body above.

Duplicate-URL check: `git show d9a5a18:corpus/SOURCES.md | grep -c
'omacom.io'` → 0; this is a new source, not a W04 duplicate.

Two integration notes. (1) The bodies + `receipts.jsonl` are worktree files
until L1 commits the wave; commit
`.ufo/waves/round-18/fetch/SrcOmarchyManualThemes/**` together with the row so
the receipt is a **committed raw fetch receipt** (R17-V3). (2) The book's own
internal links use the old `manuals.omamix.org` host for the same book paths;
credit only the fetched `learn.omacom.io` bodies (`final_url` in each receipt).
Quoting an old-host URL would need its own receipt.

## 7. Re-verification (no network needed)

```sh
D=.ufo/waves/round-18/fetch/SrcOmarchyManualThemes
python3 - "$D" <<'PY'
import json,hashlib,os,sys
D=sys.argv[1]; bad=[]
for line in open(os.path.join(D,"receipts.jsonl")):
    r=json.loads(line); b=open(os.path.join(D,r["body"]),"rb").read()
    if len(b)!=r["bytes"] or hashlib.sha256(b).hexdigest()!=r["sha256"]: bad.append(r["body"])
print("receipts_ok" if not bad else "receipts_BAD "+repr(bad)); sys.exit(bool(bad))
PY
```

Anchors are checkable with `sed -n '216p' $D/themes` etc. The quote/sha set was
exercised clean (8/8) and against a one-byte mutant (fails on `themes`). A
re-fetch comparison must mask `csrf-token`/`authenticity_token` first (§1);
the raw body sha is not expected to repeat even when content is unchanged.

## 8. Gaps, risks, overlap

- **Documentary only.** No host observation; host binaries (swaybg, walker,
  elephant, hyprlock) stay `[UNK]`. This report never invokes them.
- **Drift risk.** The manual is unversioned and already marked legacy; it can
  change or be retired without a version bump. The receipt digests pin what
  was read; `recheck: 180d` (or an earlier closure re-fetch if the note
  claims currency) is the honest cadence.
- **Tier A is provenance, not recency.** The row must keep "legacy v3" and
  "unversioned" in scope so it is not used to bind v3.8.4 or Quattro.
- **Overlap.** Other seats cover the theme *code* (`bin/omarchy-theme-set*`,
  hooks, bg-next, swaybg man, host files); this report adds docs only and
  opens no row for those URLs. SrcOmarchyBackground fetched `bin/omarchy-menu`
  (a code fact, not this manual). No existing report or SOURCES row cites
  `learn.omacom.io`.
- **Extra-themes gallery** (117 GitHub links) is enumerated but not receipt-
  verified per repo; do not credit individual theme repos as sources from
  this row.
- The book export links legacy `manuals.omamix.org` paths internally; the
  fetched `final_url` is `learn.omacom.io` and is what the receipt records.

```
Report: .ufo/waves/round-18/w1/reports/SrcOmarchyManualThemes.md
```
