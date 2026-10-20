# SourceEra — Waybar 0.15.0 version-equivalence wording and tagged-source availability

Seat: `MadoR16.SourceEra` (reviewer, leaf member, read-only). Scope: wording of "Waybar 0.15.0 / v0.15.0 / 0.15.0-3" equivalence claims and availability of tagged sources for S053/S054. No edits to corpus, SKILL, SCORECARD, LOG or sibling files. No host probe, no package operation, no build, no run of any Waybar binary.

## Verdict

Tagged-source availability for S053 and S054 is **confirmed**, with hashes that match an independent fetch and the sibling `evidence/source-bindings.json`. The equivalence chain is **confirmed for source inputs only**: upstream tag `0.15.0` → GitHub archive → Arch `pkgver=0.15.0 pkgrel=3` PKGBUILD. Equivalence of the **installed host binary or installed man pages** to those sources is **not established** and must stay labelled `[INF]`. Several lane sentences conflate tag, printed version, and package revision; wording fixes are listed below. No finding is a blocker for S053/S054 admission.

## Findings by severity

### F1 — medium — "v0.15.0" / "0.15.0" / "0.15.0-3" are three different identifiers; lane wording conflates them

- Upstream tag name is `0.15.0`, with no `v`. Ref check: `https://api.github.com/repos/Alexays/Waybar/git/refs/tags/0.15.0` → `object.type = commit`, sha `90b209add8937514d0a987aa842e701bd8f1232e`. Lightweight tag (not annotated).
- The `v` is a print prefix. `src/client.cpp:265`: `std::cout << "Waybar v" << VERSION << '\n';` (flag `-v/--version` at `src/client.cpp:248`).
- `VERSION` comes from `meson.build:4` (`version: '0.15.0'`). It becomes a git-describe string only when the source root is a git toplevel (`meson.build` branch near the `git_path` check). A release-archive build gets plain `"0.15.0"`.
- Arch packaging: `pkgver=0.15.0`, `pkgrel=3`, source = `https://github.com/Alexays/Waybar/archive/$pkgver.tar.gz` (PKGBUILD lines 7-8, 60). `pkgrel` is a packaging revision, not an upstream version.
- Consequence: the pin string `Waybar v0.15.0` (`waybar-walker-semantics.md` §1 row `waybar`; `SKILL.md` "Version pins" line 22; `evidence/round-12/before-live.txt` `live.waybar.version`) is **consistent with** a release-archive build of tag `0.15.0` `[INF]`. It is not proof the host binary was built from it.
- Affected wording: "waybar v0.15.0" used as a version identity; "waybar 0.15.0" used in claims that actually mean the 0.15.0-3 package. Both should say which identifier is meant.
- Suggested wording: `upstream tag 0.15.0 (prints "Waybar v0.15.0"); Arch package 0.15.0-3 (pkgrel 3, release-archive source)`.

### F2 — medium — equivalence chain verified for source inputs; scope of "equivalent" must be stated

Verified (read-only, hashes computed here):

| Item | Value | Result |
|---|---|---|
| GitHub archive `0.15.0.tar.gz` | 355671 B, sha256 `21c2bbef88c40473c355003582f9331d2f9b8a01efdcce0935edfc5f6b023a3e` | fetched |
| b2sum of that archive | `3f0eb6cbf4ba…de95` | equals PKGBUILD `b2sums` (PKGBUILD line 61) |
| tarball `Waybar-0.15.0/src/modules/custom.cpp` | sha256 `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` | equals commit-raw hash |
| tarball `Waybar-0.15.0/man/waybar-custom.5.scd` | sha256 `efb6a63a…2d82` | equals commit-raw hash |
| tarball `Waybar-0.15.0/src/client.cpp` | sha256 `77c59b3d7a0116123f1495db52a8661761110e0872cb2808875c55fc7fea6324` | equals commit-raw hash |
| tarball `Waybar-0.15.0/meson.build` | sha256 `5e0baf9e…9ac4` | equals commit-raw hash |
| archive contains `.git/` | 0 entries | consistent with the non-git VERSION branch in F1 |

Not verified and must stay `[INF]` or `[UNK]`:
- The host binary `/usr/bin/waybar` and its installed man pages. Not inspected (no host probe this round). Installed man pages are scdoc output, not the `.scd` bytes; no byte comparison was made.
- Arch `pkgrel` 1–2 history. Only the `main`-branch PKGBUILD was read.
- Build-option drift. The pkgrel-3 PKGBUILD builds with `--auto-features=enabled`, `-Dexperimental=true`, `-Dcava=disabled`, `-Dtests=enabled` (PKGBUILD lines 27-34). Upstream `meson_options.txt` defaults `experimental` to `false` and `cava` to `auto`. At tag `0.15.0`, `experimental` is not referenced in `meson.build` or any fetched `src/`/`include/` file, so it appears to be a no-op there `[INF, limited: did not grep every meson subdirectory file]`. `cava=disabled` removes the cava module, which matters only if the host config uses it `[UNK: host config not compared here]`.
- Therefore "waybar 0.15.0 behaves as tag 0.15.0" is equivalence of **source inputs**. Equivalence of **compiled behaviour** is not established.

### F3 — medium — "no IPC/query verb in waybar 0.15.0" is source-supported at tag scope; wording should be scoped

Tag-scope evidence (all 222 `src/` + `include/` files at `90b209a…`, fetched and grepped):
- No Waybar-served socket. There is no `listen(` and no server-side `bind(` in any file. `sigc::bind` and `std::bind` hits are unrelated.
- All `AF_UNIX` use is client-side: `src/modules/sway/ipc/client.cpp:67`; `src/modules/hyprland/backend.cpp:88-89` and `:181` (`getSocket1Reply`, which the source comments "basically hyprctl"); `src/modules/niri/backend.cpp:31-32`; `src/modules/wayfire/backend.cpp:101`.
- Sway bar IPC is opt-in. `src/bar.cpp:267-279` creates `BarIpcClient` only when bar `ipc` is `true`. `man/waybar.5.scd.in:133-136` says it subscribes to sway bar events and is controlled by `swaymsg bar` commands. This is inbound control via sway, not a Waybar query.
- Signals are controls. `src/main.cpp` handles `SIGUSR1`, `SIGUSR2`, `SIGINT`, `SIGCHLD` and `SIGRTMIN+1..SIGRTMAX`. `man/waybar.5.scd.in:218-251` documents SIGUSR actions as visibility or reload, and RTMIN as per-module refresh.
- CLI surface at tag: `src/client.cpp:248-254` lists `-v`, `-c`, `-s`, `-l`, `-b`. The semantics note's "config/style/log/bar only" (§2.3 row 102) omits `-v`; trivial.

Consequence: the anti-claim "no module-text query surface at 0.15.0" holds at tag scope. Waybar does perform outbound client IPC to Hyprland (and to sway/niri/wayfire when those are used). That is compositor-state reading, not module-text readout. Suggested wording: `no Waybar-served IPC or query surface (tag 0.15.0 source: no listen/bind); outbound client sockets exist for compositor state only`. The current "no IPC/query verb in waybar 0.15.0" should carry the tag qualifier. It appears in `waybar-walker-semantics.md` §2.3 row 102 and §6.8 context, `arc-synthesis.md:228,301`, `closeout-r11.md:42`, `README.md:17,57`, `SKILL.md:112`, `SCORECARD.md:14`, `LOG.md:167`, and `round-15/w1/reports/FrontierJoin.md`. Routing: these are owned by other seats or by L1; I have not edited them.

### F4 — medium — one UNK in the custom-module row is resolvable at tag source (rendering stays unobserved)

`corpus/knowledge/waybar-walker-semantics.md:136` (`custom/update` row, "Fails" column): "how a non-zero exit renders (text vs. kept value) is MAN-undocumented → **UNK**".

Tagged source at `90b209a` resolves the *design* of that question:
- `src/modules/custom.cpp:164-166` (`Custom::update()`): if `exec` or `exec-if` is a string and `output_.out` is empty **or** `output_.exit_code != 0`, then `event_box_.hide()`. The module is hidden, not shown with kept text.
- `exec-if` non-zero: `custom.cpp:51-53` (delay worker) and `:123-125` (waiting worker) set `can_update=false` and emit, which reaches the same hide branch.
- Continuous worker non-zero exit: `custom.cpp:86-93` sets `output_ = {exit_code, ""}` and emits, which again reaches the hide branch.
- The man page (`man/waybar-custom.5.scd`) does not state this. Only S054 does.

Suggested replacement for that cell: `hidden on non-zero exit or empty output per S054 (custom.cpp:164-166), tag 0.15.0 source; host rendering UNK`. The `[UNK]` on the host behaviour stays. This is an append-only errata candidate in the semantics note. That note is not in L1's listed ownership, so route to its owner or L1.

### F5 — low — the core `waybar(5)` source at the tag is a template, not `waybar.5.scd`

At `90b209a` the tree contains `man/waybar.5.scd.in` (12834 B, sha256 `3407241d8efa8e6f5132db050b22efbefc032db2436ad6640ff30dadaafc495d`, fetched) and no `man/waybar.5.scd`. The `.in` is generated by meson/scdoc under the `man-pages` feature (`meson_options.txt`). The lane cites "waybar(5)" for bar-level keys in `waybar-walker-semantics.md` §2.1 and §2.3, `arc-synthesis.md:228`, and `README.md:17`. No SOURCES row currently covers this file. S053 covers only `custom`. If a bar-level source row is added, the anchor should be the `.in` template plus its line numbers, not an installed man page.

### F6 — low — URL form uses a mutable tag ref

S053/S054 cite `.../Waybar/0.15.0/...`. The tag is lightweight, so `0.15.0` can be force-moved. Current bytes match the commit-pinned URL: `man/waybar-custom.5.scd` sha256 `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` (6656 B) and `src/modules/custom.cpp` sha256 `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` (8746 B). Both match `.ufo/waves/round-16/evidence/source-bindings.json`. Suggested: add the commit `90b209add8937514d0a987aa842e701bd8f1232e` to the recheck note, or cite the commit URL in the SOURCES row. Not blocking.

### F7 — info — S053/S054 claims spot-checked against bytes

- S053 `DESCRIPTION`: "The *custom* module displays either the output of a script or static text." Counted 13 whitespace words, matching the lesson.
- S054: `src/modules/custom.cpp:181` `label_.set_markup(str);` is inside `Custom::update()`, matching the lesson's quote.
- S053 section list (`DESCRIPTION`, `CONFIGURATION` with `exec`/`exec-if`/`return-type`/`interval`/`signal`, `RETURN-TYPE`, `FORMAT REPLACEMENTS`) is present in the fetched file.
- Both S053 and S054 rows already exist in `corpus/SOURCES.md:65-66`. No status, recheck or used-by changes were checked beyond the fields quoted here.

## Residual risk

- A host-version claim of the form "installed waybar is 0.15.0 upstream" rests on the `Waybar v0.15.0` print string. That is consistent with the source-archive build (F1) but does not prove it. Only a host-side `[OBS]` could tie the installed binary to the tag, and that is out of scope this round.
- Equivalence of compiled behaviour under pkgrel-3 flags is unverified (F2).
- The source route closes the documentary gap for the custom producer contract and the hide branch. It does not measure rendered text, which remains `[UNK]`.

## Verification gaps (not performed)

- No comparison of installed `/usr/bin/waybar` or installed man pages with tag bytes.
- No Arch PKGBUILD history for pkgrel 1–2.
- No exhaustive grep of every meson subdirectory for `experimental`.
- No build, no run, no test execution (per assignment).
- Tag list fetched with the first 10 entries only; no newer tag was checked, which is not needed for this pin.

## Tooling record

- Installs or updates this round: **none**. `~/.omp/agent/RULES.md` was read; installs are not authorized this round.
- Commands used were read-only: `curl` for GitHub API, raw and archive URLs; `sha256sum`, `b2sum`, `tar -tzf`/`-xzf` into `/tmp`; `python3` for filtering. No `pacman`, no `waybar` invocation, no service or compositor call.
- Not read: `~/.omp/agent/agent.db*`, credential or auth files.
