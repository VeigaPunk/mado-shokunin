# FetchBackfillR17 — R17-V3 receipt backfill for the 13 rows round 17 credited

Seat `MadoR18.FetchBackfillR17` (round-18 w1). Scope: re-fetch every https source in
`corpus/SOURCES.md` rows S056-S058 and S063-S069, hash the three host-file rows (S059,
S060, S071), and report per row whether the recorded digest reproduces and whether the
gate quote in `corpus/lessons/round-17.md:41-57` (§ Gate) is present at its anchor.
Read-only against the web and the host; nothing executed from any source. No corpus file
edited (L1 owns `SOURCES.md`), no git/jj write of any kind.

## Method

- Fetch client: `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2
  brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.70.0
  ngtcp2/1.25.0 nghttp3/1.18.0 mit-krb5/1.22.2`.
- Exact form: `curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}' URL`,
  no auth, no cookies, no session/private URLs. All ten answers were HTTP 200; no body
  exceeded 1 MiB (largest 291 777 B), so nothing was skipped.
- Raw bodies and one JSON line per fetch are under
  `.ufo/waves/round-18/fetch/FetchBackfillR17/` (`receipts.jsonl`, schema
  `mado-fetch-receipt-v1`, 10 lines, validated as JSON with the full field set).
- Recorded digests were parsed from the anchor column of each row in
  `corpus/SOURCES.md`; gate quotes and word counts were parsed from
  `corpus/lessons/round-17.md:41-57`, so this check binds to the committed texts rather
  than to a transcription.
- Raw-file anchors are file lines. `[HW:n]`/`[LW:n]` anchors are lines of the
  tag-stripped `<article>` text, reconstructed with the convention the round-17 verifier
  documented (`Review`/`AttackGateQuotesP6.md:220`): first `<article>`, `<br>`→newline,
  close-block→newline, strip tags, `html.unescape`, collapse whitespace, drop blanks.
  My independent extractor yields 175 lines (hypridle) and 680 lines (hyprlock) versus
  that verifier's 121/332; the two conventions split table cells/code blocks differently,
  but both put the gate quote on line 6 / line 7, and each quote is also a literal
  substring of the fetched raw HTML.
- Machine-readable result of every check: `fetch/FetchBackfillR17/quote-check.json`
  (`schema: mado-r17v3-backfill-v1`), which carries expected/fetched digests, bytes,
  anchor token, quote, observed word count, presence and line.

## Re-fetch results (S056-S058, S063-S069)

All ten rows: **recorded digest = fetched digest**. `bytes` is the fetched size and
agrees with the size recorded in round 17 where one was stated (S056 14 762; S057 44 020;
S058 28 787; wiki bodies 254 750 / 291 777).

| row | gate anchor | recorded = fetched (sha256) | bytes | digest | gate quote at anchor | quote words |
|---|---|---|---|---|---|---|
| S056 | `README.md:166` | `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40` | 14762 | match | yes — line 166, quote follows the `- ` list marker | 11 (gate says 11) |
| S057 | `xdg-terminal-exec:106` | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` | 44020 | match | yes — substring of line 106 | 4 (4) |
| S058 | `alacritty.5.scd:35-37` | `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107` | 28787 | match | yes — lines 35-37 joined (see note) | 16 (16) |
| S063 | `[HW:6]` | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` | 254750 | match | yes — whole article block 6 | 9 (9) |
| S064 | `[LW:7]` | `f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5` | 291777 | match | yes — whole article block 7 | 24 (24) |
| S065 | `[HR:6]` | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6` | 2598 | match | yes — substring of bullet line 6 | 10 (10) |
| S066 | `[HC:473]` | `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` | 29880 | match | yes — substring of line 473 | 5 (—) |
| S067 | `[HH:23]` | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` | 3611 | match | yes — substring of line 23 | 3 (—) |
| S068 | `[HM:61]` | `379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38` | 2587 | match | yes — substring of line 61 | 5 (5) |
| S069 | `[LR:5]` | `83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3` | 1458 | match | yes — substring of bullet line 5 | 4 (4) |

Anchor text actually observed at each hit (leading list markers trimmed for reading):

- **S056** — `- Each entry from the explicit selection list is checked for applicability:`
- **S057** — `--dir=workdir      set workdir of terminal.`
- **S058** — wraps across the recorded three lines; joined and whitespace-collapsed it is
  `Imports are loaded in order, skipping all missing files, with the importing file being
  loaded last. If a field is already present in a previous import, it will be replaced.`
  A single-line substring search fails by construction because the SCD source wraps at
  ~80 columns; the quote is complete across `35-37` and the sentence continues on line 37.
- **S063** — the exact whole line; its neighbouring blocks are `Hypr Ecosystem`/`hypridle`
  (1-3), `hypridle is Hyprland’s idle management daemon.` (4), `Configuration` (5), then
  the quoted line at 6.
- **S064** — the exact whole block; block 6 is the `Warning` heading immediately above it.
- **S065** — ` - support for dbus' loginctl commands (lock / unlock / before-sleep)`
- **S066** — `    if (MEMBER == "Lock") {`, inside `handleDbusLogin` (opens line 465,
  `// lock & unlock` at 466), i.e. the dbus Lock context the row claims.
- **S067** — `        bool                        ignoreInhibit     = false;`
- **S068** — `            Debug::log(CRIT, "ConfigManager: No hypridle.conf file found in:");`
  (the quote is the message substring, as the gate row states; the emitted literal carries
  a `ConfigManager: ` prefix).
- **S069** — ` - Uses the ext-session-lock protocol`

### Tag → commit resolution (remote refs only)

`git ls-remote https://github.com/<owner>/<repo> refs/tags/<tag> 'refs/tags/<tag>^{}'`:

| repo | tag | tag object / lightweight ref | peeled commit | comparison |
|---|---|---|---|---|
| `Vladimir-csp/xdg-terminal-exec` | `v0.14.3` | `065925df9f419008159258ae169018bfd23df71b` (lightweight) | — | equals the ref recorded in S056 |
| `alacritty/alacritty` | `v0.17.0` | `dc946285396bd3e251b6942af7e9961b74f76bee` | `94e7c8874e526b1e67b349d9ba30ddf81669119e` | equals the tag object and peeled commit recorded in S058 |
| `hyprwm/hypridle` | `v0.1.8` | `e5c01af0842bd66617f7004568df9406111d6e80` (lightweight) | — | newly recorded; rows S065-S068 name the tag but not its commit |
| `hyprwm/hyprlock` | `v0.9.6` | `b222d9b1f87e980cac379371df57913a53b99d7f` (lightweight) | — | newly recorded; row S069 names the tag but not its commit |

## Host-file rows (not fetched)

Byte reads only (`sha256sum`, `stat`, `sed`, `grep`); no command named in these files was
run. Every digest the rows record reproduces exactly today.

| row | path | current sha256 | bytes | vs recorded |
|---|---|---|---|---|
| S059 | `~/.config/hypr/bindings.conf` | `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581` | 2879 | match |
| S059 | `~/.config/xdg-terminals.list` | `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b` | 127 | match |
| S059 | `~/.config/alacritty/alacritty.toml` | `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8` | 876 | match |
| S059 | `~/.config/omarchy/current/theme/alacritty.toml` | `8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139` | 772 | match |
| S059 | `~/.config/alacritty/alacritty.toml.bak.20261003-190229` | `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a` | 873 | match |
| S060 | `/usr/share/xdg-terminal-exec/xdg-terminals.list` | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` | 1053 | match |
| S071 | `~/.local/share/applications/Alacritty.desktop` | `713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683` | 452 | match |
| S071 | `~/.local/share/omarchy/applications/Alacritty.desktop` | `713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683` | 452 | byte-identical claim confirmed |
| S071 | `/usr/share/applications/Alacritty.desktop` | `d420b0f418d9039f324bdb423181f874dee36c47ce2ab643435a4c04aac243d8` | 374 | digest not previously recorded; `X-Terminal` key claim confirmed |

Structural claims re-checked against those bytes:

- S059 `bindings.conf:2` is `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`;
  `xdg-terminals.list:3` is `Alacritty.desktop`; `alacritty.toml` is 28 lines, line 1 is
  `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]`, and
  `live_config_reload` occurs 0 times.
- S060 is 25 lines / 1053 bytes; line 3 is
  `# i.e. /usr/share/xdg-terminal-exec/xdg-terminals` (the gate quote). Its
  "byte-identical to upstream v0.14.3 list" clause was **not** re-tested: the upstream
  `xdg-terminals.list` is not among the URL rows assigned to this seat. The host digest
  matches the value S060 records.
- S071 user-local entry: line 7 `Categories=System;TerminalEmulator;`; lines 14-17 carry
  the four `X-TerminalArg*` keys; `^X-Terminal` count is 4 in the user-local copy and 0 in
  `/usr/share/applications/Alacritty.desktop`.

## Limits and residual risks

1. **Wiki pages are mutable.** Both wiki digests reproduce today's bytes, but the pages
   are "Latest git" (modified 2026-08-26) with no commit pin — the round-17 seat reports
   record 404/403 on the upstream markdown/API route. A match is a same-day equality, not
   a permanent pin; rechecks must compare the recorded digest.
2. **`[HW:n]`/`[LW:n]` are extraction-relative.** The quote text is independently present
   in the raw HTML and lands on 6/7 under two different block conventions; the absolute
   line totals are not comparable across extractors.
3. **Anchors are literal text, not whole-line identity, for S057, S065-S069.** S068's
   quote is an interior substring of a `Debug::log(CRIT, …)` literal; S065/S069 are
   bullet interiors. This matches what the gate table claims ("located quote"), not more.
4. **S066 discrepancy is already closed.** The round-17 lesson logged the nibble erratum
   (`round-17.md:95`, `2dd4d73d4f5c…` → `2dd4d73d6f5c…`). Today's `SOURCES.md` carries
   the corrected value, which the fresh bytes match; no new discrepancy.
5. **Host digests are point-in-time.** All nine read paths matched their recorded values
   on 2026-10-20, so no drift is observable today; the rows stay `on-change`.
6. **A tag-pinned source never proves the host binary**, unchanged from round 17.

## Files written

Under `.ufo/waves/round-18/fetch/FetchBackfillR17/`:

- `s056-xtd-readme`, `s057-xtd-script`, `s058-alacritty-man`, `s063-wiki-hypridle`,
  `s064-wiki-hyprlock`, `s065-hypridle-readme`, `s066-hypridle-cpp`,
  `s067-hypridle-hpp`, `s068-hypridle-main`, `s069-hyprlock-readme` — raw bodies;
- `receipts.jsonl` — ten `mado-fetch-receipt-v1` lines (validated: 10 lines, schema and
  field set exact, numeric `http_status`/`bytes`);
- `quote-check.json` — per-row expected/fetched digest, bytes, anchor, quote, word count,
  presence, and the host-file digests.

This report: `.ufo/waves/round-18/w1/reports/FetchBackfillR17.md`.

No other lane files touched; no `SOURCES.md`, lesson, gate or registry edit (L1 owns
those); no git/jj write in the lane; no writes under `/home/vgpnk/Projects/shokunin`
outside `mado-shokunin`.

## Tooling and compliance

No tool installed or upgraded, so there is no tool record to add. Commands used were
`curl`, `sha256sum`, `stat`, `wc`, `sed`, `awk`, `grep`, `git ls-remote` (remote refs
only, never the lane repository) and `python3` stdlib. No pacman/yay/paru/expac/pactree/
checkupdates, `sudo`, `systemctl`, `journalctl`, `loginctl`, `hyprctl`, `libinput`,
`wayland-info`, `walker`, `elephant`, `swaybg`, `hyprpaper`, `waybar`, `alacritty`,
`hypridle`, `hyprlock`, `omarchy-*`, `notify-send`, screenshot or input/device probe was
run. Source text (including commands printed in README/wiki bodies) was treated as data,
never executed.
