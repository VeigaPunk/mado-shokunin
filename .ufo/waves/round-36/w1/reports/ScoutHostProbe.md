# ScoutHostProbe — harm watch, read-only (round 36, wave 1)

Seat: `L1Mado36.ScoutHostProbe` · Role: scout · Probe instant: 2026-10-25T07:42:57Z
(`date -u`). Scope: sha256 the declared host config planes and compare against
the lane's pins. Nothing written outside this report; nothing restarted;
no installs; no pacman transaction (pause honored — `pacman -Q` is a query).

## Commands run

1. `sha256sum ~/.config/hypr/*.conf ~/.config/waybar/config.jsonc ~/.config/waybar/style.css`
2. `sha256sum ~/.config/omarchy/current/theme/hyprlock.conf ~/.local/share/omarchy/config/hypr/{hypridle,hyprlock}.conf`
3. `sha256sum ~/.config/hypr/autostart.conf.bak.1791942509 ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/waybar/style.css.pre-ai-readability`
4. `wc -lc ~/.config/hypr/gkeep.conf` + `grep -c 'windowrule' ~/.config/hypr/gkeep.conf` (shape only — r12 deliberately did not record rule bodies or a sha)
5. `ls -la ~/.config/hypr/ ~/.config/waybar/`
6. `hyprctl version | head -3` · `pacman -Q hyprland waybar walker` · `omarchy version` · `git -C ~/.local/share/omarchy describe --tags` + `rev-parse --short HEAD` (all read-only/whitelisted)

## Current bytes vs lane pins

| File | Current sha256 | Lane pin (source) | Verdict |
|---|---|---|---|
| `hypr/ai-usage.conf` | `21e76af98ce791fa829b99d41a51014ec910a9db602e5a9806da233350ad423e` | `21e76af98ce7…` (hyprland-config-plane.md:29) | **MATCH** |
| `hypr/autostart.conf` | `5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46` | `5ace17016fe2…` (hyprland-config-plane.md:30) | **MATCH** |
| `hypr/bindings.conf` | `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581` | `e574a1ed0853…` (hyprland-config-plane.md:22) | **MATCH** |
| `hypr/envs.conf` | `04af5cdf028bf48897a5cebe77c720d4352925e159f7c2f8c7484396f1be9c49` | `04af5cdf028b…` (hyprland-config-plane.md:31) | **MATCH** |
| `hypr/gkeep.conf` | `3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949` | *no sha pin by design* — shape pin 264 B / 5 L / 3 `windowrule` (config-drift-r12.md:32,50) | **SHAPE MATCH** (5 L, 264 B, 3 windowrule) |
| `hypr/hypridle.conf` | `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` | `e7d3b8dd…` (SKILL.md:116; idle-lock-plane.md:62,69) | **MATCH** |
| `hypr/hyprland.conf` | `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` | current pin `ce7483f3…` (config-drift-r12.md:28,85); stale anchor `4f52854a…` (SKILL.md:318; hyprland-config-plane.md:21,36,218) | **MATCH vs current pin**; see F1 |
| `hypr/hyprlock.conf` | `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` | `b8d173dc…` (SKILL.md:116; idle-lock-plane.md:63,70) | **MATCH** |
| `hypr/hyprsunset.conf` | `3042e4a923030239f4edf7b1943f41f4ed57107550177130c96f3b215b226e22` | `3042e4a92303…` (hyprland-config-plane.md:28) | **MATCH** |
| `hypr/input.conf` | `3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4` | `3769c92ab766…` (hyprland-config-plane.md:23) | **MATCH** |
| `hypr/looknfeel.conf` | `777a4fdc8b61db4419c3392d43fbb549ceb868bf8eaa84d9bf278d6e40a8c1ea` | `777a4fdc8b61…` (hyprland-config-plane.md:25) | **MATCH** |
| `hypr/monitors.conf` | `69c9d8996dfdcd6747775e984a479c53a520bd2ef193d337e171927fdf6795ee` | `69c9d8996dfd…` (hyprland-config-plane.md:24) | **MATCH** |
| `hypr/xdph.conf` | `2fded88a27b89f33cbc2b64a1258117df74b591f39a84c78ec3504a7d3b09136` | `2fded88a27b8…` (hyprland-config-plane.md:32) | **MATCH** |
| `waybar/config.jsonc` | `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829` | `a408a33d…` (config-drift-r12.md:34) | **MATCH** |
| `waybar/style.css` | `8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf` | `8f335ca0…` (config-drift-r12.md:38) | **MATCH** |

Adjacent pins re-verified (not in the declared glob): theme
`~/.config/omarchy/current/theme/hyprlock.conf` = `3ef010e72b5f…` —
MATCH (idle-lock-plane.md:64). `hypridle.conf`/`hyprlock.conf` remain
byte-identical to the shipped defaults `~/.local/share/omarchy/config/hypr/*`
(same shas — idle-lock-plane.md:66-70 claim re-verified).

Backup lineage confirmed: `hyprland.conf.bak.1792267376` = `4f52854a3c14…`
(the old MADO-1 pin itself, saved by the gkeep installer — config-drift-r12.md:133);
`autostart.conf.bak.1791942509` = `8b472371e78b…` (MATCH, hyprland-config-plane.md:33);
`style.css.pre-ai-readability` = `c9215e9ee305…` (MATCH, config-drift-r12.md:39).

Directory census: `~/.config/hypr/` holds 13 `*.conf` + 2 `.bak.*` (matches
r12's "live directory holds 13" — config-drift-r12.md:86); `~/.config/waybar/`
holds `config.jsonc` + `style.css` plus the 6 documented backups/intermediate.
No new files, no new `.bak` since the r12 records.

## Version pins (SKILL.md:22-25)

| Pin | Command | Observed | Verdict |
|---|---|---|---|
| Hyprland 0.56.2, commit `efb5099…` | `hyprctl version` | `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f` | **MATCH** |
| waybar v0.15.0 | `pacman -Q waybar` | `waybar 0.15.0-3` | **MATCH** |
| walker 2.17.0 | `pacman -Q walker` | `walker 2.17.2-1` | **DRIFT — already routed**: round-19 supersession ledger `walker-2.17.2` (old 2.17.0 → new 2.17.2; SKILL.md:624 registry row, `.ufo/waves/round-19/supersessions.json`). SKILL.md:22 text anchor is stale, known. |
| `omarchy version` 3.8.3 | `omarchy version` | `3.8.3` | **MATCH** |
| checkout `git describe` v3.8.4 @ `8fcc9d60` | `git -C ~/.local/share/omarchy` | `v3.8.4`, `8fcc9d604` | **MATCH** (dual pin intact) |

## Findings

- **F1 (S3, record-level): no new drift on any pinned plane.** All 14
  sha-pinned declared files equal their *latest* lane pins. The lone apparent
  mismatch — `hyprland.conf` vs the `4f52854a…` anchor still quoted at
  SKILL.md:318 and hyprland-config-plane.md:21/36/218 — is a documented,
  already-errata'd rotation (SKILL.md:56 round-12 erratum;
  config-drift-r12.md:28,85; the old bytes survive as
  `hyprland.conf.bak.1792267376`). Those stale anchors are historical
  citations, not live pins; no action beyond noting.
- **F2 (S3): `gkeep.conf` carries no sha256 pin anywhere in the lane** —
  config-drift-r12.md:50 records that rule bodies were "intentionally not
  recorded". It is covered only by shape (264 B/5 L/3 windowrule), which
  matches. Flagging so a later seat doesn't mistake the missing sha for an
  oversight; a byte-pin could be added if the policy that excluded it is
  revisited.
- **F3 (S3): walker binary is 2.17.2-1 while SKILL.md:22 pins 2.17.0** —
  the supersession is already ledgered (`.ufo/waves/round-19/supersessions.json`,
  scope covers SKILL.md); reported for completeness, not new.
- **No harm observed.** `~/.config/hypr` and `~/.config/waybar` mtimes are all
  ≤ 2026-10-20 (dirs Oct 17); nothing under the declared planes changed since
  the round-12 measurements. No writes, no restarts, no compositor mutations
  issued by this seat.

## Boundary statement

Substrate read-only before/after by construction: this seat ran only
`sha256sum`, `wc`, `grep -c`, `ls`, `pacman -Q`, `hyprctl version`,
`omarchy version`, `git describe/rev-parse`, `date`. No file written outside
this report; no service, daemon, or compositor touched; no package
transaction attempted.
