# SrcHyprlockWiki — hyprlock wiki page, source evidence

Seat: `MadoR17.SrcHyprlockWiki` (round 17, w1). Scope: one documentation page, read-only.
Item: open `https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/`; record page date marker,
section outline, and <=25-word quotes for authentication/PAM, the general
grace/immediate-render/ignore-empty-input options, and how hyprlock is launched and unlocks.
Report only; no host files, config trees, package queries or live probes touched.

## Fetch record

| Item | Observed |
|---|---|
| Page URL | `https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/` |
| Access date | 2026-10-20 |
| HTTP | 200, `server: cloudflare`, `content-length: 291777`, server `date: Tue, 20 Oct 2026 14:00:53 GMT` |
| Page selector shown | "Latest git" (nav label, verbatim) |
| Raw HTML SHA-256 | `f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5` |
| Article text extraction | local deterministic extraction of the `<article>` element, 683 lines, SHA-256 `11ad48c67425b0343eb340fa0feb0f24c05b10bbcf52accdd30b1703c1407a88` |
| Meta word count | `itemprop=wordCount content="2369"` |

Anchors below are given two ways: `page:Lnnn` = line in the extraction above (derived
artifact, not a server-stable anchor); `rev:Lnnn` = line in the matching Markdown source,
`content/Hypr Ecosystem/hyprlock.md` at commit `3b9e21cc9ee01f130667b3b94833614400d205c9`
(raw, 19,191 bytes, 471 lines, SHA-256 `9c000af527718ccc8648be669c53d2067e29f04a39074bbaf466eaccd7dbe597`).

## Page date marker

- Footer, verbatim: `Last updated on August 26, 2026`, marked up as
  `<time datetime=2026-08-26T14:50:40.000Z>August 26, 2026</time>`.
- Head meta, verbatim: `article:modified_time` = `2026-08-26T14:50:40+02:00`
  (also `itemprop=dateModified` = same string).
- Observed discrepancy, not reconciled: the footer `<time>` says `...T14:50:40.000Z`
  while the meta says the same wall clock with `+02:00`. Record both verbatim; do not
  treat either as a commit timestamp.

## Section outline (H1–H4, in page order)

H1 `hyprlock` (breadcrumb "Hypr Ecosystem") →
H2 `Command-line Arguments` → H2 `Configuration` → H3 `Variable Types` → H3 `General` →
H3 `Authentication` → H3 `Animations` → H4 `Keywords` → H4 `Animation Tree` →
H3 `System Configuration` → H2 `Keyboard Shortcuts and Actions` → H2 `Widgets` →
H3 `Monitor Selection` → H3 `Variable Substitution` → H2 `Widget List` →
H3 `General Remarks` → H3 `Shadowable` → H3 `Clickable` → H3 `Background` → H3 `Image` →
H3 `Shape` → H3 `Input Field` → H3 `Label` → H4 `Dynamic Labels` → H2 `User Signals`.

There is no "Installation", "Usage", "Autostart", "hypridle" or "Keybind" section on this page.

## Quotes (each <=25 words, verbatim from source; page typography noted where it differs)

| Topic | Quote | Words | Anchor |
|---|---|---|---|
| What it is | "hyprlock is a simple, yet fast, multi-threaded and GPU-accelerated screen lock for Hyprland." | 13 | rev:L6–7; page:L4–5 |
| Failure mode | "If no config file is found in any of the searched paths, hyprlock exits with an error and your session will not be locked." | 24 | rev:L10; page:L7 |
| `--grace` (CLI only) | "Set grace period in seconds before requiring authentication" | 8 | rev:L24; page:L22 |
| `--immediate-render` (CLI) | "Do not wait for resources before drawing the background (Same as general:immediate_render)" | 12 | rev:L25; page:L24 |
| `general:ignore_empty_input` | "Skips validation when no password is provided." | 7 | rev:L56; page:L57 |
| `general:immediate_render` | "Makes hyprlock immediately start to draw widgets. Backgrounds will render background:color until their background:path resource is available." | 17 | rev:L57; page:L61–62 |
| `general:fail_timeout` | "Milliseconds until the ui resets after a failed auth attempt" | 10 | rev:L61; page:L83 |
| `auth:pam:enabled` | "Whether to enable pam authentication." | 5 | rev:L69; page:L93 |
| `auth:pam:module` | "Sets the pam module used for authentication. If the module isn't found in /etc/pam.d, \"su\" will be used as a fallback." | 21 | rev:L70; page:L97 |
| `auth:fingerprint:enabled` | "Enables parallel fingerprint auth with fprintd." | 6 | rev:L71; page:L101 |
| Auth requirement | "At least one enabled authentication method is required." | 8 | rev:L77; page:L117 |
| Arch default lockout | "On Arch Linux, by default, hyprlock integrates with pambase through pam_faillock.so, which forces a 10 minute timeout after 3 failed unlocks." | 21 | rev:L118; page:L147 |
| Unlock signal | "SIGUSR1: Unlocks hyprlock. For example, you can switch to a another tty and run pkill -USR1 hyprlock." | 17 | rev:L470; page:L680 |

Page typography differs from the quoted source rows: the deployed page shows lowercase
`pam` (as does the matching old revision; current `main` uses uppercase `PAM`), uses
curly apostrophes/quotes in `pam:module`, and drops the trailing period after "fallback".
The source wording above is authoritative for the quote.

## Authentication / PAM (as documented)

- `pam:enabled` default `true`; `pam:module` default `hyprlock`, with `su` used as fallback
  when the module "isn't found in /etc/pam.d" (rev:L69–70; page:L92–97).
- Fingerprint is a second, parallel method: `fingerprint:enabled` default `false`,
  "parallel fingerprint auth with fprintd" (rev:L71; page:L100–101), with ready/present
  messages and a 250 ms retry delay.
- At least one enabled authentication method is required (rev:L77; page:L117).
- Arch-specific documentary claim: pambase + `pam_faillock.so` force a 10-minute timeout
  after 3 failed unlocks, configurable via `unlock_time`, `fail_interval`, `deny` in
  `/etc/security/faillock.conf` (rev:L118–119; page:L147–148). This is a statement about
  Arch defaults in documentation, not an observation of this host.
- Default keys listed for the password buffer: ESC, Ctrl+u, Ctrl+Backspace
  (section "Keyboard Shortcuts and Actions", rev:L121–129).

## Grace / immediate render / ignore empty input

- `--grace SECONDS` is documented only as a command-line argument on this page; there is
  no `general:grace` row in the `general` table. [Observed from the two tables.]
- `general:ignore_empty_input` default `false`: "Skips validation when no password is
  provided." (rev:L56).
- `general:immediate_render` default `false`: draws widgets immediately and paints
  `background:color` until `background:path` is available (rev:L57); the CLI
  `--immediate-render` is documented as the same setting (rev:L25).
- Related: `general:fail_timeout` default `2000` ms, UI reset after failed auth (rev:L61).

## How it is launched and unlocks

- **Launched:** the page documents no launch, autostart, keybind, systemd or `hypridle`
  procedure. It presents `hyprlock` as an executable: `hyprlock --help` for arguments
  (rev:L16), `--config FILE`, `--display NAME`, and config discovery in this order:
  `$XDG_CONFIG_HOME/hypr/hyprlock.conf`, `$HOME/.config/hypr/hyprlock.conf`, each
  `$XDG_CONFIG_DIRS` entry, `/etc/xdg/hypr/hyprlock.conf`, first match used; explicit path
  via `hyprlock --config <path>` (rev:L30–39; page:L32–37). The page footer navigation
  links to the separate `hypridle` page, but that is navigation, not content on this page.
  [UNK] on this page: any canonical launch method or idle-daemon integration claim.
- **Unlocks:** by authentication (PAM, optionally parallel fprintd fingerprint), or
  out-of-band by `SIGUSR1` ("Unlocks hyprlock", rev:L470; page:L680). `SIGUSR2` updates
  labels and images; it is not an unlock.
- The page also warns that with no config file found, "your session will not be locked"
  (rev:L10), so a documentary lock route cannot assume locking merely from the binary.

## Revision / freshness observation (matters for citing this page)

- The deployed page's edit link points to `content/Hypr%20Ecosystem/hyprlock.md`
  (`edit/main/content/Hypr%20Ecosystem/hyprlock.md` in the HTML). That path returns 404
  on `main` today; the wiki was restructured.
- Current `main` hosts the page at `content/hypr-ecosystem/user/hyprlock.md`
  (SHA-256 `28c0405ef7f5ca27031d4614d56c445b086e60423adca93f4d4e43dedbc9d8ac`,
  479 lines). Its last commit shown by the GitHub history page is
  `c04680a28301ab4b5ee5f94eaff5395efe28dbac` "Post-rewrite fixups (#1647)",
  committed `2026-09-18T14:40:42.000+02:00`; a prior path commit
  `cba1dbc509d3ab753cd1dbf48e50b7df25297ed9` "major wiki restructure..." is
  `2026-08-29T23:00:25.000+02:00`.
- The deployed article's wording matches the pre-restructure file at `3b9e21c...`
  (`content/Hypr Ecosystem/hyprlock.md`, SHA-256 `9c000af5...`, 471 lines): lowercase
  `pam`, "a another tty", type `str`, while current `main` has uppercase `PAM`,
  "another TTY", type `string`. [Observed string-level comparison; I did not diff whole
  files.]
- [INFERENCE] The deployed "Latest git" page is built from a revision older than current
  `main`, and its footer date (2026-08-26) is not the last-commit date of the current
  file (2026-09-18). Cite the page as dated 2026-08-26 with its own URL; do not present
  its bytes as current `main`, and do not treat tag/source/page as evidence of the host
  binary. Host hyprlock version and installed state remain [UNK] (no package queries,
  per pause).

## Bounded relevance to a P6 documentary route

This page can support only documentary statements: the documented config search paths,
PAM/fingerprint unlock semantics, `--grace`, `general:immediate_render`,
`general:ignore_empty_input`, `general:fail_timeout`, and `SIGUSR1`. It cannot support
"the host runs hyprlock", "the host is configured with PAM module hyprlock", or any
observed lock/unlock behaviour. Whether `$HOME/.config/hypr/hyprlock.conf` exists on this
host was not read in this item.

## Compliance and tooling

- No `sudo`, `pacman`/`yay`/`paru` (including read-only queries), `systemctl`, `hyprctl`,
  `hyprlock`/`hypridle`, notification, screenshot or live probe was run. Commands used:
  `curl` (page and raw source fetch), `sha256sum`, `wc`, `grep`, `sed`, `awk`, and a
  local Python text extraction of the already-downloaded HTML. No host config file was
  read. No tools were installed or updated.
- Reproduce: `curl -sS -o page.html https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/`
  then `sha256sum page.html` (expect `f69cff6b...`); raw matching revision:
  `curl -sS 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/3b9e21cc9ee01f130667b3b94833614400d205c9/content/Hypr%20Ecosystem/hyprlock.md'`
  (expect `9c000af5...`).
