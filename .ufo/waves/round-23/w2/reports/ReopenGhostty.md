# ReopenGhostty: C2 source re-open at lane tip 2f1134f3 (round 23, wave 2)

Seat: MadoR23.ReopenGhostty (leaf, read-only).
Lane tip: `2f1134f38930fc8b067d2d7f5bba126338faabdd` (subject "round-23: C3 PROVINCE refinement accounts for every tracked lane tool", author date 2026-10-22 08:49:46 -0300).
Scope: `corpus/SOURCES.md` rows S134, S135, S136, S137, S138, S139, S150, S151 as they stand at the tip (tip snapshot lines 146-151 and 162-163), and the located quotes in `.ufo/waves/round-23/w1/reports/SrcGhostty.md`.
Scratch (downloads, extracted trees, tip snapshots, receipt): `/fast/scratch/hyaku/mado-r23/w2/ReopenGhostty/`. Receipt: `receipt.json` in that directory.
Lane writes: this file only. Lane access: read-only `git rev-parse`, `log`, `show`.
Installs and upgrades: none. No pacman, no sudo, no host change.

Tip snapshots (sha256): `corpus/SOURCES.md` = ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc (392 lines, 136,607 B). `corpus/knowledge/terminal-trees-r23.md` = 1038dbc4e2182ce368ffb8c9eb6a83274207a411b8e4cd4f0961c446b10a2c2e (95 lines, 16,085 B).

## 1. Verdicts per row

| Row | Re-opened (HTTP, bytes) | Digest check | Anchor lines | Located quotes (SrcGhostty) | Verdict |
|---|---|---|---|---|---|
| S134 | `ghostty.org/docs/config` 200, 111,894 B; raw `website@3755ed6e/docs/config/index.mdx` 200, 6,449 B | raw 73dee823...6bf69 = recorded; rendered cb79ca5d...b08b6b5 = recorded | §File Location 36-55, §Syntax 57-90, §Splitting 92-119, §Reloading 121-131 all present | C1 :44 ok. **C2 cited :44; the verbatim sentence is at :38 (mismatch).** C3 :99-100 ok (cited 99-101). C4 :123-124 ok. F1 :38 ok. F2 :41-43 and :51-52 ok | **mismatch (detail)**: one located-quote line pointer |
| S135 | `ghostty.org/docs/config/reference` 200, 1,268,048 B; raw `website@155c4cd7/docs/config/reference.mdx` 200, 147,739 B | raw f0215afc...4be6 = recorded; rendered fad11c9f...6f26 = recorded | §config-file 2490-2519, §config-default-files 2520-2528 present | C3 2494-2495 ok. §4 nested-include 2516-2518 ok (cited 2510-2518) | **confirmed** |
| S136 | github.com blob `v1.3.1/src/config/file_load.zig` 200, 306,597 B (embedded lines 166/166 exact); raw 200, 5,434 B | 96e8165c...4f ✓ = recorded; byte-identical to v1.3.1 tarball; tag 22efb0be -> 332b2aef | 9-15, 18-24, 27-50, 88-112 present | comment 18; subdir 14 and 23 ok | **confirmed** (anchor-cell gap, L3) |
| S137 | blob 200, 387,496 B (308/308 exact); raw 200, 9,739 B | 47da4a57...1949 = recorded; byte-identical | 23-29 and 56-101 present (env 25, default_subdir 27, env-as-is 80) | n/a (no quote) | **confirmed** |
| S138 | blob 200, 1,498,775 B (10,855/10,855 exact); raw 200, 410,678 B | 169a631b...acbe07c = recorded; byte-identical | 2425-2452, 2454-2465, 3986-3993, 3994-4062, 6401-6411 present | C1 3992-3993 ok; C3 2435-2436 ok; 4214 and 4216-4222 ok (inside `loadRecursiveFiles`, declared 4171) | **confirmed** (L3) |
| S139 | blob 200, 892,775 B (2,925/2,925 exact); raw 200, 103,328 B | 2bb25a3b...6c5847a7 = recorded; byte-identical | 1486-1503 and 2406-2450 present; GTK registration 1381-1388 (not in row) | C5 1486 ok; C4 1491 ok | **confirmed** |
| S150 | blob 200, 979,513 B (1,403/1,403 exact); raw 200, 59,504 B | 2ca56276...5040a91 = recorded; byte-identical | 535-561 (SIG_IGN 543, makeSignalSource 547, reloadConfig 551), 947-949, 1155 present | C4 550-551 ok | **confirmed** |
| S151 | blob `v1.2.3/src/config/Config.zig` 200, 1,339,850 B (9,016/9,016 exact); raw 200, 339,217 B | ed2eb047...1e = recorded; byte-identical to v1.2.3 tarball; tag ae9b7892 -> 6d2dd585 (2025-10-23) | 1987-1990, 3375-3380, 3411-3416 present | F1 3377 ok; defaultXdgPath 3414 ok | **confirmed** |

No row is unopened. Every row URL returned HTTP 200. The one non-200, `raw.githubusercontent.com/ghostty-org/ghostty/v1.2.3/src/config/file_load.zig`, is a 404, as SrcGhostty recorded.

Mechanical check: 71 quote and anchor items were searched across the pinned bytes. 70 are found at their cited lines. 1 is found at a different line: S134 C2 (cited :44, found :38).

## 2. Findings by severity

### Medium

**M1. The C5 sweep statements are wrong or unsupported** (SrcGhostty §3 C5, line 169; lane note `terminal-trees-r23.md` row C5, line 52).
- "SIGUSR2 only (GTK app, macOS app delegate)" is false. `dist/linux/systemd.service.in:8-9` has `Type=notify-reload` and `ReloadSignal=SIGUSR2`.
- "SIGHUP only where a child process is signalled (`src/termio/Exec.zig`, `src/pty.zig`)": the literal pattern "SIGHUP" missed `posix.SIG.HUP`. `src/pty.zig:227` sits inside `childPreExec` (lines 213-227), where the forked child resets SIG.HUP to SIG_DFL before exec. The `Exec.zig` sites (1095, 1100, 1132, 1162, 1227) signal the child. No token hit installs a SIGHUP handler in ghostty's own process, so the conclusion holds.
- "sweep recorded in §4": §4 contains no sweep output. The only trace is the command in §1.2.
- Holds: zero hits for FileMonitor, GFileMonitor, inotify*, makeFileSystemObjectSource. Widened to EVFILT_VNODE, FSEventStream, FSEvents, NSFilePresenter, NOTE_WRITE, IN_MODIFY, watchFile, fswatch, g_file_monitor and NSFileCoordinator: also zero in 1,715 text files. The two kqueue hits are not config watchers (`Config.zig:3716` comment; `.github/DISCUSSION_TEMPLATE/issue-triage.yml:84`).

**M2. C4 says the SIGUSR2 route performs "a hard reload ... or a soft reload". The signal route is hard-only** (SrcGhostty §3 C4, line 168; note row C4, line 51).
- GTK: `handleSigusr2` calls `Action.reloadConfig(self, .app, .{})` (`src/apprt/gtk/class/application.zig:1492-1495`). `ReloadConfig.soft` defaults to false (`src/apprt/action.zig:858-863`).
- macOS: `func reloadConfig(soft: Bool = false)` (`macos/Sources/Ghostty/Ghostty.App.swift:139`). The SIGUSR2 handler calls `self.ghostty.reloadConfig()` with no argument (`macos/Sources/App/macOS/AppDelegate.swift:551`).
- S139's own teaches sentence ("it is a real reload (new config object)") is correct. The overstatement is in SrcGhostty C4 and the note row C4.

### Low

**L1. S134 C2 line pointer.** The quote "The configuration file is named `config.ghostty` (or `config` before 1.2.3)," is cited to `index.mdx:44`. It is verbatim at `index.mdx:38`; line 44 is the XDG default bullet. The same wrong pointer appears in SrcGhostty §3 C2 (line 166) and in note row C2 (line 49). Fix: cite :38.

**L2. C4 counts the SIGUSR2 route once and omits its packaged trigger.** `dist/linux/systemd.service.in:8-9` (`Type=notify-reload`, `ReloadSignal=SIGUSR2`) is a shipped trigger of the same signal. C4 should mention it, or say the signal has packaged triggers.

**L3. Anchor-cell coverage gaps.** The cited lines exist. The row cells are incomplete.
- S136 (tip SOURCES line 148) omits `file_load.zig` 52-87, the macOS Application Support pair (52-56 `config.ghostty`; 58-62 legacy `config`; 64-87 `preferredAppSupportPath`). Its teaches sentence depends on them. Its `preferredDefaultFilePath 88-112` range stops mid-function; the function ends at 121.
- S138 (line 150) omits `loadRecursiveFiles` (declared 4171), which C3 cites for 4214 and 4216-4222.
- S139 (line 151) omits the GTK registration at 1381-1388, which is what makes "handled in-process" true. Verified: `glib.unixSignalAdd(std.posix.SIG.USR2, handleSigusr2, self)` at 1384-1388.
- Some ranges end one or two lines before a closing brace (S137 56-101, S138 3994-4062, S139 1486-1503). Harmless.

### Info

**I1. F1 (rename boundary) is partly resolved by ancestry.** Commit `cbeb6890c9ec` (2025-10-12T20:48:06Z, "Add `.ghostty` extension to `config` (#8885)") is not an ancestor of v1.2.3 (`6d2dd585`). GitHub compare is diverged in both directions: cbeb to v1.2.3 is ahead 95, behind 537; v1.2.3 to cbeb is ahead 537, behind 95. The v1.2.3 text tree has zero `config.ghostty` hits and two `ghostty/config` default-path lines (`src/config/Config.zig:3414`, `src/config/edit.zig:104`). So S151's "rename is a later change" holds. F1's date argument ("before the v1.2.3 tagger date") does not show inclusion. What remains is site versus tags: the site's "(or `config` before 1.2.3)" boundary is contradicted by v1.2.3's own bytes. Upstream's comment says "Ghostty <1.3.0" (`file_load.zig:18`), and v1.3.0's `file_load.zig` is byte-identical to v1.3.1's (default `config.ghostty`). F1 should be restated as a site-versus-tag conflict.

**I2. Presentation.** `index.mdx:47-48` writes `Application\ Support` with a backslash. SrcGhostty §3 C1 drops it. Not a substantive mismatch.

**I3. The lane note's located-quote cells** (rows C1-C5) carry the same quotes and pointers as SrcGhostty §3, compared by reading tip snapshot lines 48-52. The only pointer error is L1.

**I4. Unverified parenthetical in S135.** The tip row cites `155c4cd7` as "(2026-03-13, the v1.3.1 reference refresh)". The date is confirmed (commit message "update refs", 2026-03-13T16:20:52Z), but "the v1.3.1 reference refresh" is inferred from the date. I did not read the commit's diff, so the characterisation is not verified. The pin itself is confirmed by its raw bytes.

## 3. Method and exact commands

Lane (read-only git only):
```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --verify '2f1134f38930fc8b067d2d7f5bba126338faabdd^{commit}'
git -C /home/vgpnk/Projects/shokunin/mado-shokunin log -1 --format='%H%n%ad%n%s' 2f1134f38930fc8b067d2d7f5bba126338faabdd
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:corpus/SOURCES.md > /fast/scratch/hyaku/mado-r23/w2/ReopenGhostty/SOURCES-at-2f1134f3.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:corpus/knowledge/terminal-trees-r23.md > /fast/scratch/hyaku/mado-r23/w2/ReopenGhostty/note-terminal-trees-r23-at-2f1134f3.md
```

Fetches (plain HTTP GET, `curl -sSL -w 'HTTP %{http_code} bytes=%{size_download}' -o <scratch file> <url>`; no browser, no challenge handling):
- Eight raw pins: `raw.githubusercontent.com/ghostty-org/website/{3755ed6e…,155c4cd7…}/docs/config/{index,reference}.mdx`; `raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/{src/config/file_load.zig, src/os/xdg.zig, src/config/Config.zig, src/apprt/gtk/class/application.zig, macos/Sources/App/macOS/AppDelegate.swift}`; `raw.githubusercontent.com/ghostty-org/ghostty/v1.2.3/src/config/Config.zig`.
- Rendered pages: `https://ghostty.org/docs/config` and `https://ghostty.org/docs/config/reference`.
- Blob pages (each row's source URL): `https://github.com/ghostty-org/ghostty/blob/{v1.3.1,v1.2.3}/…` for S136, S137, S138, S139, S150 and S151.
- Tarballs: `https://codeload.github.com/ghostty-org/ghostty/tar.gz/refs/tags/{v1.3.1,v1.2.3}`.
- Raw v1.3.0 and v1.2.3 `src/config/file_load.zig` (F1 context): 200 and 404.

GitHub REST (unauthenticated): `repos/ghostty-org/ghostty/git/ref/tags/{v1.3.1,v1.2.3,v1.3.0}`; `…/git/tags/{22efb0be…,ae9b7892…,9a30bd63…}`; `…/commits/cbeb6890c9ec…`; `…/compare/cbeb6890…...6d2dd585…` and the reverse; `repos/ghostty-org/website/commits/{3755ed6e…,155c4cd7…}`.

Computed digests (`sha256sum`; each matches the row's recorded value where one is recorded):
```
73dee8238359099c19a80cf093c9fa7dca20bb0d6d14e8816491e8eb54d6bf69  S134 index.mdx @3755ed6e (6,449 B)
cb79ca5dcf496d81ed05862e1888958c307dc934988b3595926b2c17ab08b6b5  S134 rendered docs/config (111,894 B)
f0215afcce0488bbd2c49825005c73847f510098670a6d4a64e4da7837ba4be6  S135 reference.mdx @155c4cd7 (147,739 B)
fad11c9fe16421e3f91563a69e364e67e979c7664b7eecc499bb64f89deb6f26  S135 rendered docs/config/reference (1,268,048 B)
96e8165c5a365808b7407d61f7073aa074189bcd96b3daa0a43d37f5e3d4c94f  S136 file_load.zig v1.3.1 (5,434 B); same bytes at v1.3.0
47da4a574f6a3377b1476d604d9ff6f8b066fd8162f98b3d1a3f54ba26ef1949  S137 xdg.zig v1.3.1 (9,739 B)
169a631b9b62c5fa0b05ab0fe750240887b95b45f758c8b4a0e4ce069acbe07c  S138 Config.zig v1.3.1 (410,678 B)
2bb25a3b9a2ed7f73a7593536737d7ba0fc7e60370a953210b60119c6c5847a7  S139 application.zig v1.3.1 (103,328 B)
2ca56276a8525c593c3db2c939c27a5ac6f3273277105bd22e7f5ec485040a91  S150 AppDelegate.swift v1.3.1 (59,504 B)
ed2eb047c44c3ad82d4e1e5d23240198e289e8bf34520c444105b4a3008a6e1e  S151 Config.zig v1.2.3 (339,217 B)
265837d3026b433f0e6b4e49d43153b915b0a19513f7edd8a8e693c559bd415b  codeload v1.3.1 tarball (37,423,780 B)
e17d39482fc70fba3d72f5f25c12e9d9a72b87dd45a61a854d9928e98b69edd8  codeload v1.2.3 tarball (36,345,813 B)
```

Identity checks:
- Tarball `cmp` (`tar -xzf … --wildcards 'ghostty-1.3.1/…'`): raw S136, S137, S138, S139 and S150 are byte-identical to the v1.3.1 tarball. Raw S151 is byte-identical to the v1.2.3 tarball.
- Tag objects: v1.3.1 -> `22efb0be2bbea73e5339f5426fa3b20edabcaa11` -> commit `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`, tagger 2026-03-13T16:03:38Z, signature verified. v1.2.3 -> `ae9b7892fa099e2e72c4f913a593ad0c2f0d0286` -> commit `6d2dd585a5d87fa745d48188dd096ca6e63014d0`, tagger 2025-10-23T17:34:09Z, verified. v1.3.0 -> `9a30bd632708c3c1f01f201057048b366a8a70e5` -> commit `703d11c642a96af9e54b55b04f131bf3888948a9`, tagger 2026-03-09T15:52:26Z.
- Website commits: `3755ed6e…` dated 2026-04-01T15:49:58Z. `155c4cd7…` dated 2026-03-13T16:20:52Z ("update refs").
- Blob pages: each embeds the file as a JSON `rawLines` array. The array was compared element by element with the pinned raw bytes; all match exactly. The only length difference is the empty element after the final newline.

Mechanical checks (Python stdlib): 71 items, comment markers and whitespace normalised, substring search across each pinned file, reported with cited and found lines. 70 match at their cited lines. 1 does not (S134 C2). Rendered-page phrases (tag-stripped text) are present for the S134 and S135 statements I checked; spacing artefacts from tag stripping were read manually.

Sweeps (Python walk of the extracted trees, plus the grep tool with gitignore off): v1.3.1 has 1,715 text files; v1.2.3 has 1,192. Binary means NUL in the first 4 KiB.
- SIGUSR2: `AppDelegate.swift:543, 547, 550`; `application.zig:1486, 1491`; `dist/linux/systemd.service.in:9`.
- SIGHUP (literal): `src/termio/Exec.zig:1095, 1100, 1132, 1162, 1227`, all signalling the child.
- HUP tokens (`\bHUP\b`, `SIG.HUP`, `SIGHUP`): the same five plus `src/pty.zig:227` (`posix.SIG.HUP` inside `childPreExec`, a child-side reset to SIG_DFL) and `Exec.zig:1343` (`POLL.HUP`, a poll flag).
- File-watch APIs: zero hits (see M1).
- Binary-skipped files in v1.3.1: 3,829 in total. 3,711 are extensionless fuzz corpora under `test/fuzz-libghostty`; 92 are PNG, 15 TTF, 11 other. None is source-like.
- v1.2.3: `config.ghostty` has 0 hits. `ghostty/config"` appears at `src/config/Config.zig:3414` and `src/config/edit.zig:104`.

Ancestry: `cbeb6890c9ec4962ec7f5eae9506982d8eac994a` is not an ancestor of v1.2.3 (see I1). The compare results agree in both directions.

Installs: none. Tools used: curl, tar, sha256sum, cmp, the Python 3 standard library, and the read and grep tools. Receipt: `/fast/scratch/hyaku/mado-r23/w2/ReopenGhostty/receipt.json`.

## 4. Residual risk and verification gaps

- The upstream pages are live. The digests match this run's fetch; a later fetch may differ.
- The rendered-page check is a text-presence check, not byte-exact. The raw `.mdx` and `.zig` checks are byte-exact.
- Sweeps covered the extracted release tarballs, not a live checkout. The binary-skipped files are not source (see above).
- No runtime was exercised. The GTK and macOS reload behaviour is documentary: no app was run and no signal was sent.
- The lane's C2 counter (`.ufo/waves/round-23/c2/count.py`) was not run. Measuring C2 belongs to L1.
- The host-side facts in SrcGhostty §4 (`~/.config/ghostty/config`) were not re-read. They are out of scope, and no host probe was made.

## 5. Verdict

Verdict: S134 is a mismatch (detail): its pinned digests, anchor lines and most quotes hold, but the C2 quote is cited to `index.mdx:44` and sits at `:38`. S135, S136, S137, S138, S139, S150 and S151 are confirmed, and no row is unopened. Before C4 and C5 count as sourced, M1 (the C5 sweep) and M2 (the C4 hard/soft wording) need correcting in SrcGhostty §3 and in the lane note.
