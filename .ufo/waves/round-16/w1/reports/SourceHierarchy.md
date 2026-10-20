# SourceHierarchy — U7 Waybar module text: docs vs source vs host

Seat: `MadoR16.SourceHierarchy` (connector, leaf). Lane: mado-shokunin. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: U7 observation boundary only (not rendered verification). Source reading only.
Ground rules held: no installs or updates, no `pacman`/`pkill`/`hyprctl`/`busctl`/`waybar` execution, no screenshot, no service or compositor probe, no edits to registry or shared files. Only this report was written. Network reads were official upstream bytes (GitHub API/raw/codeload, Arch GitLab PKGBUILD) staged in scratch `/tmp/r16-u7/`.

## 1. Verdict

- **U7 stays an observation boundary.** The text chain from producer bytes to Waybar's rendering call is now pinned to source at tag `0.15.0`, and the host's Arch pin matches that tag's bytes. The rendered bar text (glyphs, fonts, markup validity, stale vs fresh, running process state) remains **UNK** and is not closed by any file read here.
- **No module-text query surface exists in 0.15.0.** CLI, signals, and IPC were checked in source. This upgrades the round-3 claim (`waybar-walker-semantics.md:102`, "no IPC/query verb") from documentation-scoped to `SRC-tag` for the 0.15.0 build.
- **Biggest U7 gap for this host:** both JSON modules that the host's own config relies on for `format: "{}"` depend on a placeholder rule that the 0.15.0 man page does not document. Source suggests it renders, but rendering is not observed. Labelled `[INF]` below.
- **Era:** host `waybar` has been upstream `0.15.0` since 2026-10-03 (pkgrel `-2`, then `-3` on 2026-10-11). The pacman log has no later waybar transaction. `master` is 1091 commits ahead and unreleased. Its docs are not host authority.

## 2. Axes

- **A1 authority**: which layer binds a claim (upstream source, upstream man page, Arch packaging, host bytes, historical measurement).
- **A2 era**: which upstream tag, host package, config bytes, and time window a claim belongs to.
- **A3 observation**: what can be established without live probes (static docs, static source, static host bytes, historical RUN payloads).
- **A4 boundary**: what stays `UNK` (rendered output, running-process state).

A move is kept only if it improves one axis and harms none. This report improves A1 and A2 and leaves A4 explicitly open.

## 3. Source authority ladder

| Tier | Artifact | Identity (read 2026-10-20) | Binds to |
|---|---|---|---|
| S-src | Upstream tag `0.15.0` source tree | commit `90b209add8937514d0a987aa842e701bd8f1232e` (GitHub commits API; tree API returned the same sha); release published 2026-02-06T20:15:36Z; latest release per API | shipped behavior, modulo build flags and compiler (`-Dexperimental=true`, `-Dcava=disabled`, PKGBUILD:65-72) |
| S-src-bytes | Tag archive | `https://github.com/Alexays/Waybar/archive/0.15.0.tar.gz`: sha256 `21c2bbef88c40473c355003582f9331d2f9b8a01efdcce0935edfc5f6b023a3e`; codeload archive identical | |
| S-pkg | Arch `waybar` PKGBUILD (main) | `pkgver=0.15.0`, `pkgrel=3`, no patch files, `b2sums` `3f0eb6cbf4…de95` (PKGBUILD:7-8, 61); **b2sum recomputed over the upstream archive matches exactly** | host package source = upstream tag bytes (A1 link) |
| S-doc | Upstream `man/waybar-custom.5.scd` at 0.15.0 | same tag | documented surface of the same tag |
| S-doc-host | Installed `/usr/share/man/man5/waybar-custom.5.gz` | package `waybar-0.15.0-3` | phrase-level match to S-doc (format replacements list, `interval` minimum text, `escape`) |
| H-cfg | `~/.config/waybar/config.jsonc` | sha256 `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829`, mtime 2026-10-17 20:02:56Z, 260 lines / 6,354 B (matches drift record `config-drift-r12.md:34`) | declared modules and signals |
| H-css | `~/.config/waybar/style.css` | sha256 `8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf` (matches drift record); `#custom-gkeep` at `style.css:143-155` | styling of classes |
| H-prod | gkeep producer and installer, `~/Projects/gkeep` HEAD `133b86717a02548aeaff3f1411bf301d936c5308` | `gkeep/waybar.py`, `gkeep/notes.py:40-48`, `gkeep/ui.py:122-135`, `install.sh:38-74`, `README.md:23` | the `custom/gkeep` text and tooltip |
| H-hist | Round-3 measurements `corpus/knowledge/waybar-walker-semantics.md` (2026-10-14), round-1 `waybar-walker-plane.md` and R4 errata | RUN payloads, pins before the gkeep drift | historical only |
| H-log | `/var/log/pacman.log`; `/var/lib/pacman/local/waybar-0.15.0-3/desc` | `[ALPM] installed waybar (0.15.0-2)` 2026-10-03T17:44:28-0300; `upgraded waybar (0.15.0-2 -> 0.15.0-3)` 2026-10-11T16:14:39-0300; no later waybar line | era boundary |
| X-master | `master` branch (`compare/0.15.0...master`: ahead_by 1091, behind_by 0) | unreleased | **not host authority**; used only to show doc drift |

Tier order for U7 claims: S-src (+ S-pkg byte link) > S-doc (same tag) > H-cfg/H-prod/H-log (static host) > H-hist (dated RUN) > X-master (never binds to host).

## 4. Doc vs source vs host, claim by claim

Anchors are tag `0.15.0` unless marked otherwise. "SRC" means source checked at the tag. "DOC" means `man/waybar-custom.5.scd` at the tag.

| # | Claim | DOC (tag) | SRC (tag) | Host (static / historical) | Status for U7 |
|---|---|---|---|---|---|
| C1 | No text query or IPC for module content | none stated | `client.cpp:248-254` options are `-v -c -s -l -b` only; `main.cpp:55-56`, `119-122` catch RT signals and broadcast; `bar.cpp:267-279` `ipc` key exists only under `HAVE_SWAY`, a sway bar-IPC client (`modules/sway/bar.cpp:17`); no module-content getter | host config has no `"ipc"` key (grep count 0); R3-1 §2.3 UNK | **SRC-tag: no query surface.** Rendered text stays UNK |
| C2 | Exec path | `exec` = script path (DOC:15-22) | `command.hpp:113-115`, `163`: `/bin/sh -c`, sets `WAYBAR_OUTPUT_NAME`; `command.hpp:28-40` reads until EOF and strips only the final newline | host `exec` uses `$OMARCHY_PATH` and `~/` (config:64, 89, 203) — shell expansion present; value of `$OMARCHY_PATH` inside waybar's env stays UNK (R3-1 §9.1) | SRC-tag; env value UNK |
| C3 | Hide conditions | `hide-empty-text` only (DOC:24-26) | `custom.cpp:164-166`: module hidden when `out` is empty **or** exit code ≠ 0; `custom.cpp:178`: hidden when `format` yields empty string or `hide-empty-text` with empty text | R3-1 §3.2 `custom/update` marked "non-zero exit renders: MAN-undocumented → UNK" | **Resolved at SRC-tag:** non-zero exit or empty stdout hides, it does not show stale text. Rendering check still UNK |
| C4 | JSON parse scope | JSON keys `text tooltip class percentage` (DOC:150-157); no "single line" rule | `custom.cpp:257-290`: only the **first** line is parsed (`break` at :290); `json.hpp:25-40` throws on invalid JSON | gkeep emits one line via `json.dumps` (`waybar.py` `render`); no multi-line output in host JSON producers verified here | SRC-tag. Master DOC adds the single-line rule, so the tag docs are silent on a real constraint |
| C5 | Invalid JSON behavior | silent | `custom.cpp:262` throws before label update → dispatcher `bar.cpp:570-576` catches and logs `spdlog::error`; `update()` does not reach `set_markup` (:181), so the **previous label text stays** | none | SRC-derived: stale text persists, error is log-only. Visual state cannot distinguish fresh from stale. **Observation boundary.** Log content UNK |
| C6 | `{alt}` placeholder and `alt`-keyed icons | DOC lists only `{text}` `{percentage}` `{icon}` (DOC:170-174); `format-icons` is array-only (DOC:63-65) | `custom.cpp:175-176`, `186-187` pass `fmt::arg("alt", alt_)`; `custom.cpp:262-269` read JSON `alt`; `ALabel.cpp:132-141` selects `format-icons[alt]` when `format-icons` is an object | voxtype `format-icons` object keyed `idle` / `recording` / `transcribing` (config:223-227); producer sets `alt` (R3-1 §3.2 `omarchy-voxtype-status:9`) | **SRC-tag supports the historical INF.** The shipped doc lags source; master DOC documents it. Rendered icon choice UNK |
| C7 | `{}` placeholder | default format `{text}` (DOC:60-61); `{}` not documented | ctor default `"{}"` (`custom.cpp:9`); `fmt::format` is called with **named** args only (`custom.cpp:175`) | host configs use `"format": "{}"` for `custom/gkeep` (config:242) and `custom/ai-usage` (config:254); R3-1 §3.2 notes the same | **[INF]: renders the `text` value** by fmt's positional fallback to the first `fmt::arg`. Not executed. Master DOC says `{}` equals `{text}` and forbids mixing with other placeholders. `test/` has no custom-module test at the tag. **Largest U7 gap for this host** |
| C8 | Fractional `interval` | `interval` typeof "integer or float", minimum 0.001 s (DOC:37-42) | `ALabel.cpp:24-31`: `static_cast<long>(asDouble()) * 1000`, so `0.5` becomes **1 ms** and `2.5` becomes 2 s; contradicts the documented minimum | host intervals all integer (config:68, 71, 91, 110, 148, 239, 249) | Doc-vs-source mismatch at the tag. **No host impact** (static config). Fixed on master (`ALabel.cpp` master lines 30-31 use `asDouble() * 1000`) |
| C9 | Signal refresh | signal `1..N`, `SIGRTMIN+N = SIGRTMAX`, no interval ⇒ signal is sole refresh (DOC:52-56) | `custom.cpp:23` (no interval ⇒ waiting worker), `138-141` (match `SIGRTMIN+signal`); `bar.cpp:518-521` broadcasts to all modules | host signals 7, 8, 9, 10, 11, 12 unique (config:67, 204, 210, 216, 250, 240); gkeep `ui.py:122-135` sends `SIGRTMIN+12`; R3-1 §4 delivery RUN-measured (SIGRTMIN=34) | **Consistent** across DOC, SRC, host, historical RUN |
| C10 | Markup vs escape | `escape` default false, "escape script output" (DOC:125-130) | `custom.cpp:181` `set_markup(str)`; unescaped text is Pango markup; `escape` branch `:233-274` | ai-usage sets `escape: false` (config:252) and emits markup (R3-1 §3.3 RUN); gkeep does **not** set `escape` and its tooltip is raw note text via `summary()` (`notes.py:40-48`) | SRC-tag. **[INF] markup-break risk** for note text containing `&` or `<`; GTK behavior not run. **Privacy boundary:** tooltip exposes first 60 characters of the latest note body |
| C11 | `tooltip-format` precedence | overrides script tooltip (DOC:120-124) | `custom.cpp:183-195` honors it when set; otherwise script tooltip; gkeep omits `tooltip-format` | gkeep uses script tooltip (config:236-245) | Consistent. Tooltip content UNK |
| C12 | `class` payload | string or array (DOC:157) | `custom.cpp:278-282` string or array; applied to label at `:201-202` (classes removed except id, :196-199) | gkeep `class` `empty`/`notes` (waybar.py); CSS `#custom-gkeep.empty` (style.css:153) | Consistent. Styled look UNK |
| C13 | Glyphs | none | none | gkeep text is glyph U+F249 + count (`waybar.py`); CSS font `JetBrainsMonoNL Nerd Font Mono` (style.css:143-152) | Font coverage and pixels **UNK** (no screenshot, barred) |
| C14 | Build flags | n/a | n/a | PKGBUILD:65-72 `-Dexperimental=true`, `-Dcava=disabled` | Recorded; not checked against binary |
| C15 | Binary-to-source identity | n/a | n/a | `/usr/bin/waybar` contains strings `try replacing` (fmt error path, `custom.cpp:209-215`), `hide-empty-text`, `format-icons` (each count 1, `grep -a -c`) | Weak static corroboration only. **Binary-to-source equivalence NOT established** |

## 5. Eras

| Era | Window | What is authoritative | Use for U7 |
|---|---|---|---|
| E-A upstream `0.15.0` | tag 2026-02-06; commit `90b209add…`. Includes the 2026-02-04 custom-module fixes (`c34b1b6a19` unhandled JSON exception in signal handlers, `0a8b7b096a`, `2b29c9a5d6`) | source + same-tag DOC | binding for the host binary |
| E-H1 host `0.15.0-2` | 2026-10-03T17:44:28-0300 | pacman log | historical round-1/3 window ends at the 0.15.0-3 rebuild |
| E-H2 host `0.15.0-3` | 2026-10-11T16:14:39-0300 → present | pacman log, local DB (`INSTALLDATE` 1791746079 = 2026-10-11T19:14:39Z), no later waybar line | current binary era. Same upstream bytes (pkgrel-only change). Build date 2026-08-31 |
| E-C1 config pre-gkeep | to 2026-10-17 ~20:02Z | drift record, `.bak.1792203278` / `.bak.1792267376` | historical config (249 L / 6,068 B / `07f7d663…`) |
| E-C2 config post-gkeep | 2026-10-17 20:02:56Z → present (unchanged on today's read) | current file hash `a408a33…` equals drift record | current declared modules |
| E-M master | unreleased, 1091 commits ahead of tag | master DOC and source | **Not host authority.** Cited only to show where docs moved (C6, C7, C8) |

Process-state era: `PID 1707` (R3-1, 2026-10-14) and later PIDs are session facts. A core dump on record (`LOG.md` round-11 entry, waybar `pid 3036215`, 21:21:17Z) means any earlier live reading is stale. No running-process fact is asserted here.

## 6. U7 observation boundary

Chain (tag 0.15.0), each arrow a source-anchored step:

`producer stdout (sh -c, command.hpp:113-131)` → `whole output read, final newline stripped (command.hpp:28-40)` → `per-return-type parse, first line only for JSON (custom.cpp:257-290)` → `empty/nonzero hide (custom.cpp:164-166)` → `fmt render with text/alt/icon/percentage (custom.cpp:175-176)` → `set_markup (custom.cpp:181)` → `GTK label and Wayland surface (not in source chain; UNK)`.

**Established without probes:**
- Shape of the producer contract and what the module does with each byte class (C2–C5, C12).
- That no query verb exists for module text in 0.15.0 (C1).
- Signal refresh is the only external trigger (C9).
- Declared host modules, signals, styles, and config hash (H-cfg, H-css).
- Historical producer payloads for indicators, voxtype, ai-usage, and gkeep-equivalent (R3-1 §3–4, dated 2026-10-14). These are payload facts, not rendered facts.

**Not established (must stay UNK):**
- Rendered glyphs, font coverage, pixels, geometry of text (C13).
- `{}` rendering (C7) and markup validity (C10).
- Stale vs fresh state visible on the bar (C5).
- Running process environment (`$OMARCHY_PATH`) and whether the running process loaded today's config bytes (drift record `config-drift-r12.md:117`).
- Any current producer output. Today's read ran no producer.

**Privacy constraint for any future observation:** tooltips from `custom/gkeep` contain the first 60 characters of the latest note body. An observation of the bar tooltip is a note-content read. Any future rendered check must exclude tooltip and class payloads or redact them before recording.

**Observation paths available in a future round, not authorized here:** a read-only GTK/AT-SPI tree read of the bar, a redacted screenshot, or a fixture harness that applies the same `fmt` format string to a fixed producer line in an isolated process. Each needs operator authorization, and none is in this round.

## 7. Discrepancies routed

| ID | Discrepancy | Owner / route |
|---|---|---|
| D1 | `{alt}` and alt-keyed `format-icons` are in source but not in the tag man page (C6). Master docs now have them | L1 SOURCES/knowledge; errata candidate against `waybar-walker-semantics.md` §3.2 "alt (undocumented)" → now SRC-supported for 0.15.0 |
| D2 | `{}` placeholder is undocumented at the tag and relied on by two host JSON modules (C7) | L1 (open gap; not closed) |
| D3 | Fractional `interval` truncates to whole seconds at the tag (C8). Documented as float | L1 knowledge note; no host impact |
| D4 | JSON parse uses only line 1; invalid JSON leaves stale text (C4, C5). Docs silent | L1 knowledge note |
| D5 | `waybar-walker-semantics.md` §3.2 says non-zero exit rendering is `UNK`. Source (tag) hides the module (C3) | errata candidate for the round-3 note's owner; not edited here |
| D6 | gkeep README says `custom/gkeep` is inserted on signal 12 "when that id is free"; `install.sh:38-74` checks only for the `"custom/gkeep"` string and has no signal-collision check. Current config has no collision (C9) | operator project `~/Projects/gkeep` (outside mado province; `config-drift-r12.md:109` already routes gkeep to the operator). Report only |
| D7 | "U7" is a reused label in other notes with different meanings: `walker-deep.md:403, 493, 496` (theme-set/walker sockets), `hyprctl-verification-layer.md:301` and `config-health-report-r3.md:401` (`instances` `wlSocket`). This report's U7 is only the Waybar module-text item (`SCORECARD.md` U-list; `arc-synthesis.md` §6) | L1 should qualify citations |
| D8 | gkeep tooltip is unescaped Pango markup on raw note text (C10) | operator project; [INF] risk, not run |

## 8. Proposed registry rows (for L1; not written)

Reserved ids per the contract: S053 (Waybar custom module man), S054 (custom.cpp). S055 is the closure own-work row and is not used here.

- **S053** | Waybar 0.15.0 `waybar-custom` man page, `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd` | docs | A | Tag-era documented custom-module surface; `interval`, `signal`, `format`, `format-icons`, `escape`, `return-type`, `FORMAT REPLACEMENTS`. Anchor: tag `0.15.0` commit `90b209add8937514d0a987aa842e701bd8f1232e`; lines 15-26, 37-42, 52-56, 58-65, 120-130, 150-174. Teaches: the tag docs omit `{alt}`, alt-keyed icons, `{}`, and the single-line JSON rule; doc absence is not runtime absence. Host installed man `waybar-custom.5.gz` matches on the format-replacements list, the interval minimum sentence, and the escape block. | opened 2026-10-20 | on-release |
- **S054** | Waybar 0.15.0 `src/modules/custom.cpp` plus `src/ALabel.cpp`, `include/util/command.hpp`, `src/main.cpp`, `src/bar.cpp`, `include/util/json.hpp` | code | A | Shipped custom-module behavior at the tag. Anchor: archive sha256 `21c2bbef88c40473c355003582f9331d2f9b8a01efdcce0935edfc5f6b023a3e`; b2sum `3f0eb6cb…de95` matches Arch PKGBUILD 0.15.0-3 pin. `custom.cpp` lines 9, 138-141, 162-166, 175-187, 257-290; `ALabel.cpp` 24-31, 132-141; `command.hpp` 28-40, 113-131; `main.cpp` 55-56, 119-122; `bar.cpp` 518-521, 570-576; `json.hpp` 25-40. Teaches: hide-on-empty-or-nonzero, first-line JSON, stale text on parse error, `{alt}` and alt-keyed icons, `{}` default, fractional-interval truncation, no query surface. Not established: binary-to-source equivalence, rendered output. | opened 2026-10-20 | on-release |
- **Optional, L1 decision (not reserved):** Arch `waybar` PKGBUILD `https://gitlab.archlinux.org/archlinux/packaging/packages/waybar/-/raw/main/PKGBUILD` (pkgver 0.15.0, pkgrel 3, b2sums pin, build flags). It binds the host package to the upstream tag. If admitted, use the next free id after the L1 registry state, not a guessed id.

Registry cells not to be copied from this report without L1 review: `status` for S053/S054 should be `mined`, with `used-by` set to the U7 knowledge note L1 creates.

## 9. Install, update and command record

- **Installs or updates:** none. No `pacman`, `uv`, `npm`, `cargo`, or binary download into `~/.local/bin`. The tooling directive was read; this round's contract forbids installs and none was needed.
- **Reads:** upstream GitHub API (`repos/Alexays/Waybar/git/trees/0.15.0`, `commits/0.15.0`, `tags`, `releases/latest`, `compare/0.15.0...master`, `commits?path=src/modules/custom.cpp`); `raw.githubusercontent.com` (tag and master `custom.cpp`, `ALabel.cpp`, `AModule.cpp`, `waybar-custom.5.scd`); `codeload.github.com` and `github.com/.../archive/0.15.0.tar.gz` (identical sha256); Arch GitLab PKGBUILD. Scratch in `/tmp/r16-u7/`.
- **Host reads (static):** `~/.config/waybar/config.jsonc`, `style.css` (hash and mtime only), `/usr/share/man/man5/waybar-custom.5.gz` (decompressed for text), `/var/lib/pacman/local/waybar-0.15.0-3/desc`, `/var/log/pacman.log` (grep), `/usr/bin/waybar` (`grep -a -c`, string presence only), `~/Projects/gkeep` source files (read), `~/Projects/shokunin/mado-shokunin` knowledge and logs (read).
- **Not run:** `waybar` (any form), `pkill`, `hyprctl`, `busctl`, `gkeep`, `ai-usage`, `omarchy-*` producers, `pacman` (any), `systemctl`, screenshot tools, any `/proc` read of waybar.

## 10. Limits

- Binary-to-source equivalence not established. The host binary was only string-checked.
- fmt version on host is `fmt-12.2.0-1` (`/var/lib/pacman/local`); the `{}` fallback behavior was not executed.
- GTK markup behavior and GTK tooltip failure modes were not executed.
- Master docs and master source are not host authority. They only show where docs moved.
- Host config state is as of today's static read (hash `a408a33…`, mtime 2026-10-17 20:02:56Z). It is not proof of what the running process loaded.
- No checks were run for verification. Checks the main agent should run once after integration: re-hash `/tmp/r16-u7/waybar-0.15.0.tar.gz` against `21c2bbef…` and `b2sum` against the PKGBUILD pin; `sources-census.sh validate` after L1 adds S053/S054.
