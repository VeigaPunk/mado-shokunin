# mado round-9 record — scribe prep DRAFT (SCR-M9)

Draft v1 window: 2026-10-14 19:57–20:05Z (local 16:57–17:05 −03:00). Lane SCR-M9.
This file is scribe scratch product for the round-9 finalizer — **not the record**.
Nothing outside this file was written by this lane in the repo; scratch
`/tmp/w9-scr-m9/` (`selftest.log`, `nolive.log`, `live.log`, `regression.log`,
`anchors.log`, `rowids.txt`, `asserted-ids.txt`, `asserted-all.txt`). All probes
read-only: file reads, `wc`/`sha256sum`/`stat`/`grep`/`readlink`/`ls`, the gate's
own four modes, `hyprctl` read verbs, `pgrep -ax`, `busctl --user list`,
`omarchy theme current`. No substrate file under `~/.config`/`~/.local` written;
no live session disturbed; no socket connected; no network command; **no
`git status`/`fetch` on the omarchy checkout** (guard list respected this time —
the round-8 draft disclosed one such probe; this lane ran none).

Reading key: **⟨PENDING⟩** = must be resolved at finalization; every other
number names the command that produced it at v1 time. Tags: **[OBS]** measured,
**[INF]** inference from measured code/record, **[UNK]** unknown. Counts on
`.md` notes use `wc -l`; the gate's last line is unterminated — 2,887 by
`wc -l` / 2,888 editor view (the round-7/8 idiom). Shas are cited as measured
prefixes (16 hex) unless noted.

## 0. Round-9 frame

- Plan: `plans/round-9.plan.md` — **committed in the round-8 landing**
  (`12c8f08`), 231 L by `wc -l` / 15,136 B / sha `8630c91a75a2eb43…` (design
  lane PREP-M9, freeze 19:14Z at base `0c20a76` with round-8 work in flight).
  Axis move: **coverage + operability** — ONE move, three ordered stages:
  (a) the `theme` plane lands as gate rows from `theme-wallpaper-plane.md` §6
  (file rows + the two live rows `theme.wallpaper.live`,
  `theme.name.display_agree`; `theme.choice` stays NOTE); (b) the walker
  live-surface rows land from `walker-live-surface.md` §4/§5 (socket rows,
  D-Bus owner row, layer-invariant row) plus the `walker-deep.md` §10/§11
  errata append (substance = the note's §5 ledger); (c) census closure over
  the landed set + receipts — every widening carries its mutant and a re-cut
  `MADO_REGRESSION: PASS`, receipt lines quoted in the record.
- Ordering (plan `:167-175`): (a)/(b) are gated on the round-8 precondition
  set — (a8) stub discipline, (b8) omarchy plane landed, (c8) assertion
  floor — each resolved at dispatch from the round-8 record; if (a8) did not
  land, the live rows of (a)/(b) are exempted **by name** and only the
  file-plane halves ship. (c) rides (a) and (b).
- Anti-claim (as written, plan `:177-187`): a stubbed scenario proves row
  logic, never live values; an unfaithful stub shape is exempted by name,
  never faked; any unverifiable check reads UNKNOWN, never CLEAN; the theme
  choice stays NOTE (operator-owned); a MOVED anchor is reported first, never
  smoothed; no compositor/session mutation (no launcher open, no socket
  connect, no `omarchy theme set`, no restart); the theme tree, the omarchy
  checkout, the tameshi harness and sibling repos are read-only; no `git
  status`/`fetch` on the checkout; secrets shape-only.
- Measure (plan `:189-205`): regression verdict per landed revision; selftest
  count before → after with scenario ids; distinct asserted row ids before →
  after; plane census before → after by the counting command; helper-regex id
  count before → after; the two verdicts at the landed revision;
  `walker-deep.md` sha before → after (errata append); SKILL gate section
  gains the two planes and the landing receipts; SCORECARD move row + LOG
  entry carrying the commands; README coverage rows for the two round-7 notes
  plus round-8's; `corpus/lessons/round-9.md` chartered with its `## Gate`
  section and a non-author spot-check — or the round records why no
  independent seat exists.

### 0.1 Design-time pins in the plan are superseded by the round-8 landing [OBS]

The plan was frozen 19:14Z **while round 8 was still writing** (round-8
commit landed 19:55:09Z). Every gate number in the plan reads at the
round-7 revision `0c20a76`. Landed values (re-measured at v1, §1.2/§1.3):

| plan says (round-7 base) | landed at `12c8f08` [OBS] |
|---|---|
| gate `90d50cdd…`, 1,755 L / 75,771 B | `7da4ec50…`, **2,887 L** / 131,612 B, mtime 16:29:03 −03:00 |
| selftest `89/89` | **`217/217`** |
| `--no-live` CLEAN (17 pass, 2 notes), skip=1 | CLEAN (**20 pass, 3 notes**), `counts: pass=20 fail=0 unknown=0 skip=8 note=3` |
| live CLEAN (35 pass, 4 notes) | CLEAN (**43 pass, 7 notes**), `counts: pass=43 fail=0 unknown=0 skip=0 note=7` |
| census "106 `row` + 6 `row_from_rc`, 40 ids, six plane ids; hypr-live 57 / hypr 23 / waybar 17 / terms 10 / gate 3 / walker 2" | **162 `row` + 6 `row_from_rc` = 168 sites; 51 distinct ids; seven plane ids** — omarchy 56 / hypr-live 51 (+6 `row_from_rc` → 57 combined) / hypr 23 / waybar 17 / terms 10 / gate 3 / walker 2 |
| helper regexes six ids at `:352`, `:356`, `:371-375` | **seven ids** (`hypr\|hypr-live\|waybar\|walker\|terms\|omarchy\|gate`) at `:357`, `:361`, `:376-380` |
| "selftest asserts ≈11 of 40" | **22 of 51** asserted (§1.3; list measured) |
| regression `MADO_REGRESSION: PASS` target `c4c1afb7…a5171` | PASS, target **`d2bcdb31daea5d68…db62`** (three-family excision; my own run §1.2); spec `c7ee75b9…1dd8` unchanged; harness `cf41efaa…242c75` unchanged |
| walker rows `:1659-1667`, `live.theme.current` `:1673`/`:1677` | walker rows `:2540-2559`, `live.theme.current` `:2565`/`:2569`; `live_plane()` `:2300`, `omarchy_plane()` `:2610` |
| "no round-8 artifact committed at freeze" | round-8 landed: plane 7 `omarchy`, `--snapshot`/`--snapshot-diff`, sweep note, AUD-M8 + VER-M8 reports |
| debt: `corpus/lessons/` 0 entries; README 8 rows | still 0 entries (**ninth** round); README still 8 rows (nine notes now unrowed) |

The record must cite landed values; any finalizer arithmetic copied from the
plan ("106", "40", "89", `90d50cdd…`, "hypr-live 57") is a stale-base defect
(same class as round-7 §0 and round-8 §0.1).

### 0.2 Round-8 precondition resolution [OBS]

- **(a8) stub discipline + token contract — PARTIALLY SATISFIED.** The
  `omarchy` plane's live body landed **hermetically**: scenarios OM1–OM8
  install PATH stubs (`omarchy`, and a `git` stub answering
  `describe`/`rev-parse`/`show` from fixture blobs; unknown verbs refused
  rc 64) and drive the real row code through `--root` fixtures — a moved pin
  FAILs naming the pin, a missing stub reads UNKNOWN and never CLEAN, an
  equal-bytes copy reads MOVED as a copy, a worktree edit is detected without
  `git status`. **The hypr-live variant of the discipline did NOT land**: no
  `hyprctl` PATH stub exists; scenarios J/K/L are absent; no hypr-live row id
  entered the asserted set (SKILL §Round-8, "What did not land", re-read at
  v1). Consequence for round 9 under the plan's ordering clause: the live
  rows of (a)/(b) may ride the **omarchy** stub idiom (PATH-first stub +
  `--root` fixture); a read that idiom cannot carry faithfully (a session
  bus, a runtime-dir socket) is exempted **by name** and the exemption is
  counted — never faked.
- **(b8) omarchy plane landed — SATISFIED, and it is the plane-id namespace
  the regex widening consumes.** Plane id 7 `omarchy`, 11 rows (8 verdict +
  3 NOTE), registry namespace `omarchy.*`; D-1 resolved as NOTE with
  HELD|MOVED printed in the detail. Landed row ids (measured from the file,
  §1.3): `omarchy.version.cmd`, `.version.file`, `.git.tag`, `.git.head`,
  `.skill.link`, `.skill.sha`, `.skill.vs_head`, `.cmd.groups` (verdict);
  `.cmd.surface`, `.theme`, `.doc.drifts` (NOTE). The selftest helper regexes
  already carry all seven landed ids.
- **(c8) assertion floor — NOT SATISFIED.** The rc-6 arm of `row_from_rc` is
  byte-identical (still maps 6 → UNKNOWN; no white-box pin, no removal); the
  two usage arms (`--root` with no value; a bad `MADO_VERIFY_LIVE`) still
  have behavior but no assertion; `VERSION_STR` still self-labels
  "v1 (round 5 / M5-2)" (`:68`) and is now also copied into every snapshot
  receipt's `tool=` line; the boundary combined-hash prefix is still
  unasserted in a `sha_pin` detail. Consequence: round 9's stage (c) is
  *census closure + receipts*, not the assertion floor; whether the round
  also picks up the round-8 (c) residue is the round's choice, recorded, not
  assumed (the plan does not claim it).

## 1. Pre-state at v1 (round 8 landed; round 9 in flight)

1. **Repo identity** [OBS, 19:57:46Z and re-polled 20:00:09Z]: HEAD
   `12c8f08a35537b7d53b8e0252459dec16e550079` ("probation round 8 (training
   r7): see LOG", 2026-10-14 16:55:09 −03:00 = 19:55:09Z); `git status
   --porcelain` **empty** at both polls. `git show --numstat HEAD` (9 files,
   +2,689/−10): LOG +1/−0, SCORECARD +1/−0, SKILL +192/−1,
   `corpus/knowledge/gate-mutation-sweep-r8.md` +179, round-8 draft +658,
   `plans/round-9.plan.md` +232, `reports/r8-aud-m8.md` +128,
   `reports/r8-ver-m8.md` +157, `tools/mado-verify.sh` **+1,141/−9**.
   Pins (`wc -l` / bytes / sha256 prefix, all read at v1):
   SKILL.md 1097 L / 83,184 B / `32f32605e1e7d646…`;
   LOG.md 299 L / 22,498 B / `156e03033cfed8d1…`;
   SCORECARD.md 20 L / 9,079 B / `de0960be17d03b0a…`;
   SHONEN.md 12 L / 1,688 B / `edace65e13c8ad20…` (byte-identical since
   `c03c249` — 4/4 `[x]`, PROBATION COMPLETE; round-8 landing did not touch
   it);
   PROVINCE.md 18 L / 891 B / `7aad7b863dc3c10b…`;
   MINT.md 20 L / 919 B / `4408f66765729a44…`;
   AGENTS.md 6 L / 251 B / `66adcad6fd6cdd4b…`;
   `corpus/README.md` 19 L / 12,709 B / `2dd274f5e270e65b…` (**8 note rows**);
   `corpus/QUALITY.md` 8 L / 329 B / `1923c94f49788ade…`;
   `plans/round-9.plan.md` 231 L / 15,136 B / `8630c91a75a2eb43…` (committed
   in the round-8 landing; ends without trailing newline — `.` byte);
   `plans/round-8-record-draft.md` 657 L / 42,881 B / `b46d4c4cb9d5cb5e…`
   (committed **with 19 unfilled ⟨PENDING⟩ markers** — `grep -c PENDING` → 19;
   see §4f);
   `reports/r8-aud-m8.md` 127 L / 11,881 B / `4d8cd1cb163d810e…`;
   `reports/r8-ver-m8.md` 156 L / 9,997 B / `a96795039520e86a…`;
   `corpus/knowledge/gate-mutation-sweep-r8.md` 178 L / 10,946 B /
   `9d6435f5cdd52561…`;
   `corpus/knowledge/theme-wallpaper-plane.md` 394 L / 27,594 B /
   `8c578cc70e36506d…` (**unchanged since round 7** — the §6 spec is this
   round's stage-(a) input, never edited);
   `corpus/knowledge/walker-live-surface.md` 300 L / 19,203 B /
   `2bbb9609283f2d81…` (**unchanged since round 7** — §4/§5 input);
   `corpus/knowledge/walker-deep.md` 617 L / 38,403 B / `0982ba066c72575a…`
   (**unchanged** → its §10/§11 errata append is still owed);
   `corpus/knowledge/omarchy-drift-watch.md` 287 L / 18,714 B /
   `49f5a9a14776d83d…` (unchanged).
2. **Gate identity and runs** [OBS, my own runs 19:58:09–19:59:11Z; logs
   `/tmp/w9-scr-m9/`]: `tools/mado-verify.sh` **2,887 L by `wc -l` (2,888
   editor) / 131,612 B / sha256
   `7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f`**,
   mtime 2026-10-14 16:29:03.396 −03:00; re-hashed identical at 20:00:09Z.
   - `--selftest` → `MADO_SELFTEST: 217/217 assertions passed`, rc 0;
   - `--no-live` → `MADO_VERIFY: CLEAN (20 pass, 3 notes; file plane only —
     live layer skipped: --no-live)`, `counts: pass=20 fail=0 unknown=0
     skip=8 note=3`, rc 0; `gate boundary.readonly PASS` combined sha
     `bb2639d9a980…`;
   - live → `MADO_VERIFY: CLEAN (43 pass, 7 notes; file + live planes
     verified read-only)`, `counts: pass=43 fail=0 unknown=0 skip=0 note=7`,
     rc 0; boundary row same prefix; every `omarchy.*` pin reads HELD in the
     detail;
   - `--regression` → **`MADO_REGRESSION: PASS (case=mado-verify-hardened;
     target=d2bcdb31daea5d68dc7c586617939d71d525dbeab723e72b8c17644ad327db62)`**,
     rc 0, 33.6 s, `REGRESSION_DATE: 2026-10-14T19:58:37Z`;
     `REGRESSION_SPEC` sha `c7ee75b97c38ac8f…1dd8` (recorded pin matches);
     `REGRESSION_TARGET … match=yes`; `REGRESSION_TABLE … match=10/10
     recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`;
     `REGRESSION_CLEANUP: removed=10`; workdir
     `/tmp/mado-verify-regression.PFYhrE` removed on PASS; `REGRESSION_HARNESS`
     `cf41efaa…242c75` (recorded `b56c6e57…22bcb` — provenance, not gated).
   A `--no-live --root <empty dir>` run is **not** re-measured here; the
   round-7 recorded reading (DIVERGED, rc 1 — file plane fails closed) stands
   as the discipline the new file rows inherit.
3. **Census and suite coverage (before)** [OBS, my commands]: `row ` call
   sites `grep -cE '^[[:space:]]*row [a-z-]+ '` → **162**; `row_from_rc` call
   sites **6** (`:2366` `live.hypr.gaps_out`, `:2375` `live.hypr.kb_layout`,
   `:2400` `live.hypr.animations`, `:2436` `live.hypr.monitor_dp1`, `:2445`
   `live.hypr.scroll_factor`, `:2524` `live.waybar.layer` — all `hypr-live`;
   helper definition `:107`) → 168 sites. By first-arg plane prefix (row only):
   **omarchy 56 / hypr-live 51 / hypr 23 / waybar 17 / terms 10 / gate 3 /
   walker 2** = 162; adding the 6 `row_from_rc` sites → hypr-live 57 combined
   [OBS]. **Distinct row ids: 51** (`awk '{print $3}' | sort -u`), of which
   **21 are `live.*`** (all under `hypr-live`), 11 `omarchy.*`. Per-plane id
   counts: omarchy 11 / hypr-live 21 / hypr 9 / waybar 4 / terms 4 / walker 1
   / gate 1. **Distinct row ids asserted by the suite: 22 of 51** —
   `boundary.readonly`, `hypr.file.sha_pin`, `hypr.local.inventory`,
   `hypr.root.include_graph`, `hypr.root.orchestrator`, `live.plane`,
   the eleven `omarchy.*`, `term.alacritty.toml`, `term.cross.font_size`,
   `walker.config`, `waybar.config.parse`, `waybar.config.reload_style`
   [OBS, union of `st_row_has`/`st_row_detail` call targets]. The **seven**
   helper regex sites are `:357`, `:361`, `:376`, `:377`, `:378`, `:379`,
   `:380`, alternation
   `(hypr|hypr-live|waybar|walker|terms|omarchy|gate)` [OBS].
   Suite labels measured in the file: OM1–OM8 and S1–S10 families present;
   assertion count 217 (two runs of `st_eq`/`st_has`-class helpers; cite 217,
   not helper site sums).
4. **The two input specs** [OBS, notes unchanged since round 7]:
   - `theme-wallpaper-plane.md` §6 (`:265-304`) is the paste-ready 12-row
     spec for plane id `theme` / namespace `theme.*` (name.read; the five
     include/import chain rows + the walker_css/swayosd_css row, one row
     listing two ids; wallpaper.link; wallpaper.live; name.display_agree;
     choice NOTE; parts.declared_only NOTE). Its own re-anchoring notes: the
     note's §10 errata route sits at `:362` (append-only) — a re-anchoring is
     an appended erratum, never an edit.
   - `walker-live-surface.md` §4 (`:160-206`) is the measured surface: both
     sockets (`srwxr-xr-x`, 0 B, mtime 13:11:09), the `dev.benz.walker`
     D-Bus owner row (owner pid == walker pid), the layer invariant (a walker
     namespace must carry the walker pid; absence is a NOTE, never a
     pass/fail signal). §5 (`:207-241`) is the `walker-deep.md` §10/§11
     ledger owed to that note's owner.
   Measured anchors at v1 (all held; §5 spot-check 3): `theme.name` =
   `matte-black` (12 B); `omarchy theme current` → `Matte Black`;
   `~/.config/omarchy/current/background` symlink →
   `…/current/theme/backgrounds/0-ship-at-sea.jpg`;
   `~/.config/mako/config` symlink → `…/current/theme/mako.ini` (50 B link);
   swaybg pid 1203358 `/usr/bin/swaybg -i …/current/background -m fill`;
   `hyprctl -j layers` DP-1 level 0 `wallpaper` 1203358, level 2 `waybar`
   1203352, **no walker namespace**; walker 1203471
   `/usr/bin/walker --gapplication-service`, elephant 1203474;
   `busctl --user list` → `dev.benz.walker` owner **1203471** unique name
   `:1.23` (elephant: 0 matches); sockets
   `/run/user/1000/walker/walker.sock` and `…/elephant/elephant.sock` both
   `srwxr-xr-x` 0 B. The chain anchors the file rows cite: `hyprland.conf:13`
   `source = ~/.config/omarchy/current/theme/hyprland.conf`;
   `hyprlock.conf:1` same pattern; `waybar/style.css:1` `@import
   "../omarchy/current/theme/waybar.css";`; `alacritty.toml:1`
   `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]`;
   walker theme chain via `config.toml:3-4` → `omarchy-default/style.css:1`
   (note §4); `swayosd/style.css:1` (note §4). Theme dir at v1: 25 entries
   incl. `walker.css` / `swayosd.css` / `mako.ini` / `backgrounds/`.
5. **Fixture coverage for the chain rows** [OBS — gate code read, the
   self-check the plan's stage (a) does not state]: `build_fixture()`
   (`:222-341`) writes a `--root` tree with `hyprland.conf` whose theme
   `source` line is **fixture line 11** (host line 13 — a literal `:13`
   anchor needs the fixture re-cut or an anchor that means "the source line",
   recorded as a design decision, not smoothed), a theme dir holding only
   `hyprland.conf` / `theme.name` / `waybar.css`, `waybar/style.css`
   (`@import` present, target in the fixture theme dir), `alacritty.toml`
   (import present, target **absent**), `hyprlock.conf` as a bare
   `# fixture hyprlock` comment (no source line), and **no** `.config/mako/`,
   **no** `.config/swayosd/`, **no** `current/background` symlink, **no**
   runtime-dir/socket fixture. The builder sits **outside** all three marked
   block families (`MADO-R7-SELFTEST-BLOCK` `:384-563`, `MADO-R8-BLOCK`
   `:874-1037` and `:1452-1974`, `MADO-R7-REGRESSION-BLOCK` `:1049-1451`) →
   any fixture growth re-cuts `PIN_MADO` (`:1107`) and needs a fresh
   `MADO_REGRESSION: PASS` — that is precisely the plan's stage-(c) receipt.
6. **Record debt carried into round 9** [OBS, all still unpaid]:
   1. `corpus/README.md` — **8 note rows; nine notes unrowed**:
      `idle-lock-plane.md` (r4), `province-accuracy-selfaudit.md` (r4/r5),
      `walker-deep.md` (r5), `gate-mutation-proof.md`, `omarchy-drift-watch.md`,
      `remaining-planes-census.md` (r6), `theme-wallpaper-plane.md`,
      `walker-live-surface.md` (r7), `gate-mutation-sweep-r8.md` (r8). Ready
      text: round-4 draft §4b (`:300`), round-5 §4b (`:276`), round-6 §4b
      (`:258`), round-7 §4b (`:321`), round-8 §4b (`:435`).
   2. `SCORECARD.md:16-20` — rounds 4–8 are one-line stubs; full rows sit in
      the committed drafts (round-4 §4c `:311`, round-5 §4c `:287`, round-6
      §4c `:270`, round-7 §4c `:335`, round-8 §4c `:446`).
   3. `LOG.md` — rounds 4–8 entries are one-line summaries (round 8 at
      `:299`); the full M7-1 entry at `:297` is round 7's.
   4. Errata: `theme-wallpaper-plane.md` §10 (`:362`) is the append-only
      re-anchoring target for stage (a); `walker-deep.md` §10 (`:521`)/§11
      (`:533`) still owe the walker note's ledger (file sha unchanged since
      round 7); `gate-mutation-proof.md` §3 residuals stay per the rc-6
      decision that is still open; no repo-level errata block exists.
   5. The committed `plans/round-8-record-draft.md` keeps **19 ⟨PENDING⟩
      markers** — D1–D5 and the record-text slots were never filled after the
      landing. §4f supplies the measured fill for an appended erratum in the
      round-9 commit (never an edit of the committed text).
   6. `corpus/lessons/` still 0 entries (ninth round of the round-1 promise);
      the round-9 plan's measure line charters `corpus/lessons/round-9.md`
      with a `## Gate` section and a non-author spot-check — **first lesson
      file** if it lands (a lane's own subagent does not count as the
      non-author seat; `LEARNING.md:38-43`).
7. **Live pins** [OBS, 20:00–20:01Z; point samples — a session restart
   invalidates them]: same session as rounds 7/8 (sockets' mtime 13:11:09
   local) — walker 1203471 / elephant 1203474 / swaybg 1203358 / waybar
   1203352, layers as §1.4, `XDG_RUNTIME_DIR=/run/user/1000`. These are the
   *values* a stub must imitate faithfully where stubbed; the substrate is
   never written.
8. **Round-9 lane activity at v1** (shape-only; no repo file landed):
   `git status --porcelain` clean at 19:57:46Z and 20:00:09Z; gate sha
   unchanged through both polls. Scratch seen (names/sizes only, **not
   read**): `/tmp/w9-mado-m9-2` (`before.txt`, `census.py`, `contexts.py`),
   `/tmp/w9-mado-m93` (`before.run.log`, `before.selftest.log`),
   `/tmp/w9-mado-m94` (`before-modes.log`, `live-probe.txt`, `poll.log`),
   `/tmp/w9-aud-m9-gate` (frozen `gate-7da4ec50.sh` + `poll.sh`),
   `/tmp/w9-ver-m9` (`baseline-live.log`, `poll.sh`); other `/tmp/w9-*`
   names are sibling-repo lanes. Lane labels are recorded by artifact
   self-label at finalization (round-5 lesson).

## 2. Deliverables and ⟨PENDING⟩ slots

### D1 (a) — the `theme` plane lands as gate rows ⟨PENDING⟩

Rows from `theme-wallpaper-plane.md` §6 (the note's table is the input, never
edited; a re-anchoring is an appended erratum to its §10, or the record).
File rows: `theme.name.read`; `theme.chain.{hypr_include, hyprlock,
waybar_css, alacritty, mako_link}`; `theme.chain.walker_css` /
`.swayosd_css` (installed-consumer-gated — NOTE when the consumer is not
installed, never a silent skip); `theme.wallpaper.link`; NOTE-only
`theme.parts.declared_only`. Live rows: `theme.wallpaper.live` (swaybg argv
names the background **symlink** with `-m fill`; level-0 `wallpaper` layer
pid == swaybg pid; NOTE if no swaybg, mirroring `live.consumer.hypridle`;
UNKNOWN if hyprctl unavailable) and `theme.name.display_agree` (`omarchy
theme current` equals the measured reader-rule of `theme.name`; a pair the
rule does not join is recorded, never forced; UNKNOWN if `omarchy` absent).
`theme.choice` stays NOTE always (operator-owned — today's
`live.theme.current`, unchanged). Exercise: file rows under the existing
`--root` fixture discipline (missing tree → FAIL/UNKNOWN, never CLEAN);
live rows under the **omarchy stub idiom** ((a8) resolution, §0.2) or
exempted by name with clause anchors. Scenario shape, round-8 idiom:
stubbed-clean → covered rows PASS; one stubbed pin MOVED → the named row
FAILs; stub absent with live requested → UNKNOWN, never CLEAN.
⟨PENDING: landed row ids (and the walker_css/swayosd_css split — one row or
two); plane token spelling; gate sha before → after; line/byte delta;
selftest 217 → 217+M with scenario ids; distinct asserted row ids 22 → ?;
the exemption list with clause anchors (or "none"); the extended spec sha +
`MADO_REGRESSION: PASS` receipt at the widened revision; the fixture re-cut
record (fixture line 11 vs host `:13`; which chain targets the fixture
grew).⟩

### D2 (b) — walker live-surface rows + the `walker-deep.md` errata ⟨PENDING⟩

From `walker-live-surface.md` §4/§5: socket rows (path, type `s`, mode, size
for `$XDG_RUNTIME_DIR/walker/walker.sock` and `…/elephant/elephant.sock`;
stat'd, **never connected**); the D-Bus owner row (`busctl --user list`
parse — `dev.benz.walker` owner pid == the walker pid; a mismatch FAILs);
the layer-invariant row (`hyprctl -j layers` — a walker namespace must carry
the walker pid; absence is a NOTE, never a pass/fail signal). The hermetically
hard question (measured at v1, §3.2): `--root` roots a `$HOME`-shaped tree;
the sockets live under `$XDG_RUNTIME_DIR` and the owner row reads the session
bus — neither is rooted by `--root` today. Accepted routes: a fixture runtime
dir carrying a real bound socket **with** an accepted override seam in the
row's read shape, a PATH-stub idiom for the verb, or exemption by name with
the exemption counted. The `walker-deep.md` §10/§11 errata append (substance
= the note's §5 ledger, append-only) is this claim's record-family clause.
⟨PENDING: landed row ids; the hermetic route actually taken (per row); the
`--root`/`XDG_RUNTIME_DIR` seam shape if one landed; exemptions by name;
`walker-deep.md` sha before → after and the appended block's location; the
regression receipt if any read lands outside the marked families.⟩

### D3 (c) — census closure + receipts ⟨PENDING⟩

The helper regexes (`:357`, `:361`, `:376-380` — seven ids at v1) widen to
the landed plane set (the seven + `theme` + the walker-live id — the exact
set is counted at dispatch, never assumed); the per-plane census is
re-reported before → after by the counting command. The defect spec extends
per newly covered clause and the sweep is re-cut at the landed revision
(the printed `REGRESSION_RECUT` command, then `PIN_MADO`/`TABLE_MADO` — both
inside the R7-REGRESSION block today, `PIN_MADO` at `:1107`);
`MADO_REGRESSION: PASS` with `MUTATE_RESTORE: OK` and target sha before =
after is the receipt — and the receipt lines (tool sha, target sha, table,
sweep) are quoted in the record (LOG + SKILL), not left only in `/tmp`. A
surviving mutant is a FINDING (append-only errata, not smoothed); widening
without a covering kill vehicle does not ship, and the round says why.
⟨PENDING: helper-regex id count before (7) → after; the census command and
its before → after output; the extended spec sha; the re-cut receipt (spec,
target, table, restore, workdir); any survivor + its finding text; the
verdict lines (`--no-live`/live counts) at the landed revision.⟩

### D4 — record debt (record work, not a new claim)

README rows (9 carried + round 9's); SCORECARD stubs 4–8 replaced + round-9
row; LOG round-9 entry (§4a) and optionally the fuller 4–7 entries; errata
status (§4e) incl. the round-8 draft closure (§4f). ⟨PENDING: which of the
carried items the round actually pays; every landed row quoted from the
measured artifact.⟩

### D5 — `corpus/lessons/round-9.md` charter ⟨PENDING⟩

Plan measure `:202-205`: chartered with its `## Gate` section and a
non-author spot-check (at least one admit and one reject) — or the round
records why no independent seat exists. The file would be the **first**
entry in `corpus/lessons/` (0 entries since round 1). ⟨PENDING: landed or
refused; if landed: line count/sha, the seat's identity (not the lane's own
subagent), one admit + one reject quoted; if refused: the recorded
reason.⟩

## 3. Clause maps — anchor → coverage (before state)

### 3.1 The §6 spec → today's gate anchors and fixture gaps

| Spec row | Read it needs | Gate site today [OBS] | Fixture state at v1 (§1.5) |
|---|---|---|---|
| `theme.name.read` | read `current/theme.name`, `^[a-z0-9-]+$` one line | no reader; fixture writes the file (`:281`) | file present (`matte-black`) |
| `theme.chain.hypr_include` | `hyprland.conf` source line + target exists | include-graph reader exists (`hypr.root.include_graph` asserted) | theme source at fixture **line 11** (host `:13`); target present |
| `theme.chain.hyprlock` | `hyprlock.conf:1` source + target | none | `# fixture hyprlock` — **no source line; target absent** |
| `theme.chain.waybar_css` | `style.css:1` import + target | `waybar.config.*` rows only | import present; target present |
| `theme.chain.alacritty` | `toml:1` import + target | none | import present; **target absent** |
| `theme.chain.mako_link` | symlink resolves inside `current/theme/` | none | **no `.config/mako/`** |
| `.chain.walker_css` / `.swayosd_css` | import line + target (consumer-gated) | none | walker `config.toml` present; **no swayosd dir** |
| `theme.wallpaper.link` | symlink inside `backgrounds/`, non-empty | none | **no `current/background`** |
| `theme.wallpaper.live` | `pgrep -ax swaybg` argv + `hyprctl -j layers` level 0 | **no swaybg reader**; layers reader exists for waybar (`:2524`) | no live fixture by design |
| `theme.name.display_agree` | `omarchy theme current` vs reader-rule | `omarchy` reader exists (`:2564-2569`, NOTE `live.theme.current`) | theme.name fixture + OM-style stub possible |
| `theme.choice` | — (NOTE always) | `live.theme.current` (`:2565`/`:2569`) | n/a |
| `theme.parts.declared_only` | `command -v` per §4.1 consumer | `have()` exists (`:103`) | n/a |

### 3.2 The walker surface → today's gate anchors and the hermetic routes

Today's walker sites are version + services only: `live.walker.version`
(`:2539-2547`, `have walker` guard), `live.walker.services` (`:2550-2559`,
`have systemctl`). `busctl` appears only for the waybar tray
(`:2526-2530`); `hyprctl -j layers` only for `live.waybar.layer`
(`:2524`). **No socket stat, no `pgrep -ax swaybg`, no runtime-dir read
exists** in the gate at v1 [OBS: `grep` for `walker.sock`/`elephant.sock` →
0 hits]. Route table for the finalizer:

| Row | Read | Can `--root` fixture it? | Plausible hermetic route |
|---|---|---|---|
| socket rows | `stat` two paths under `$XDG_RUNTIME_DIR` | no (runtime dir is not `$HOME`) | fixture runtime dir + a seam that honours an env override; else exempt by name + count |
| D-Bus owner | `busctl --user list` | no (session bus) | PATH stub for `busctl` returning a fixture line (OM idiom), else exempt by name |
| layer invariant | `hyprctl -j layers` | no (compositor IPC) | PATH stub for `hyprctl` (does **not** exist yet — the (a8) gap), else live-only + exemption |

Fidelity trap (carried from round-8 §3.1): the live readers degrade through
`have` guards to UNKNOWN — a stub absent with live requested must read
UNKNOWN, never CLEAN; parse arms return rc 3/4/5 (read/parse/mismatch),
never 6, so a corrupt fixture maps to FAIL via `row_from_rc`'s `*)` arm.

### 3.3 Suite plumbing new rows must clear

The helper plane regexes now carry seven ids at seven sites (`:357`, `:361`,
`:376-380`); any new plane token (`theme`, and whatever the walker-live rows
use) must extend all seven or its rows are invisible to the counts
(`st_counts_agree` is the fake-PASS catcher). The suite invokes `"$0"` for
its own runs; the *regression* path targets the mutant's copy — additions
inside the three marked families ride the existing re-cut; additions
**outside** every pair (a `build_fixture` change, a helper widening) make
`--regression` read SETUP with `REGRESSION_RECUT` until `PIN_MADO` is
re-cut — by design, never a stale PASS. `PIN_MADO` `:1107`, excisor
`:1197-1199`, `VERSION_STR` `:68` (still "round 5 / M5-2").

### 3.4 Residue not covered by round 9's claim [OBS]

Round-8's own unlanded items stand and are **not** in the plan's claim: the
hypr-live stub scenarios J/K/L (no `hyprctl` PATH stub), and the assertion
floor ((c8) §0.2 — rc-6 arm, the two usage arms, the version string, the
boundary prefix). The `theme` plane has **0 row sites** at v1
(`grep -cE '^[[:space:]]*row theme '` → 0); the walker live rows are version
+ services. The record should state the residue plainly rather than let the
round read as if the round-8 plan had landed whole.

## 4. Record text to apply

### 4a. LOG.md round-9 entry (append after `LOG.md:299`)

```
- 2026-10-14 — round 9 (training r8): (a) `theme` plane as gate rows —
  ⟨fill: landed row ids; file vs live split; the live rows' exercise route
  (stub idiom vs substrate); exemptions by name or none; selftest 217 → ?;
  asserted ids 22 of 51 → ?; MADO_REGRESSION: PASS at the widened revision⟩.
  (b) walker live-surface rows — ⟨fill: socket rows / D-Bus owner / layer
  invariant; the hermetic route or the counted exemption; walker-deep
  §10/§11 errata sha before → after⟩. (c) census closure + receipts —
  ⟨fill: helper regex 7 → ? ids; census 162+6 sites / 51 ids / 7 planes →
  ?; the re-cut receipt (spec, target, table, restore); survivors⟩. Gate sha
  `7da4ec50…` → ⟨fill⟩; `--no-live`/live verdicts ⟨fill⟩. Record debt
  repaid: README +⟨fill⟩ rows; SCORECARD stubs 4–8 + round 9; round-8 draft
  ⟨PENDING⟩s filled by appended erratum; `corpus/lessons/round-9.md`
  ⟨landed|refused, reason⟩. Boundary: gate + notes + substrate read-only; no
  substrate file written; no live session disturbed; no socket connected; no
  `git status` on the checkout.
- ⟨If only the file-plane halves land ((a8) partial as measured): say so —
  the live rows are exempted by name and counted; no widening headline
  under an unlanded clause.⟩
```

### 4b. `corpus/README.md` — coverage map rows

Apply the nine carried rows in order (ready text named in §1.6.1: round-4
draft §4b for `idle-lock-plane.md` + `province-accuracy-selfaudit.md`,
round-5 §4b for `walker-deep.md`, round-6 §4b for the three r6 notes,
round-7 §4b for the two r7 notes, round-8 §4b for `gate-mutation-sweep-r8.md`)
— **re-measure every pin at apply time**; the lands are unchanged at v1
(§1.1). Then one row per round-9 note as landed ⟨PENDING⟩ (composition
follows the existing row shape: note → holds → sources with the probe
window; write from the measured artifacts, never from this draft).

### 4c. `SCORECARD.md` — move-log rows

Replace the stubs `:16-20` with the committed full rows (sources in §1.6.2),
then append round 9:

```
| 9 | coverage + operability | round-8 gate: the `theme` plane was 0 row sites (two measured notes, not gate rows), the walker live surface (sockets / D-Bus owner / layer invariant) was unrowed, and the declared-coverage invariant had carried since round 5 | `theme` plane lands ⟨fill: row ids; file/live split; exercise route⟩; walker live rows land ⟨fill: ids; hermetic route or exemption⟩; census closure ⟨fill: 7 → ? plane ids; 51 → ? distinct ids; asserted 22 → ?⟩ | ⟨fill: receipt lines; gate sha `7da4ec50…` → ?; selftest 217 → ?; `--no-live`/live verdicts; scratch `/tmp/…`⟩ |
```

### 4d. SHONEN.md

No box move expected: 4/4 `[x]` since round 5; promotion is the
operator/integrator decision. Byte-identical at `edace65e13c8ad20…` unless
the finalizer edits an evidence line — if edited, re-apply the seed check
(`PROTOCOL.md:419-431`).

### 4e. Errata status

Append-only when applied: `theme-wallpaper-plane.md` §10 (`:362`) is the
re-anchoring target for stage (a); `walker-deep.md` §10 (`:521`)/§11 (`:533`)
owe the walker note's §5 ledger (r7 note routed it explicitly; file sha
unchanged at v1 → still owed until the round lands it); a helper widening
touches `gate-mutation-proof.md` §3's residuals only via the re-cut receipt.
No repo-level errata block exists.

### 4f. Round-8 record closure (appended erratum, never an edit)

The committed `plans/round-8-record-draft.md` keeps 19 unfilled ⟨PENDING⟩
markers (§1.6.5). The measured fill, for an appended closure block in the
round-9 commit:

- D1 (a) — hypr-live stub scenarios J/K/L: **not landed**; no `hyprctl`
  PATH stub; no hypr-live id added to the asserted set. The stub discipline
  that *did* land is the `omarchy` plane's OM1–OM8 (PATH stubs + `--root`
  fixtures).
- D2 (b) — `omarchy` freshness plane, id 7: **landed**. 11 rows (8 verdict +
  3 NOTE); helper regexes widened six → **seven** ids (`:357`, `:361`,
  `:376-380`); every §6 constant HELD live (version 3.8.3 / file 3.8.3 / tag
  v3.8.4 / head 8fcc9d60 / skill link+sha becd149e / theme Matte Black,
  NOTE); `omarchy.skill.vs_head` shipped (index-free `git show`).
- D3 (c) — assertion floor: **not landed** (rc-6 still 6 → UNKNOWN;
  `VERSION_STR` still round-5 text, now also in snapshot receipts; both
  usage arms unasserted; boundary prefix unasserted).
- D4 — record debt: **not repaid** (README unchanged 8 rows; SCORECARD 4–8
  stubs; LOG one-liners; round-7 draft's 13 ⟨PENDING⟩s still unfilled).
- D5 — `corpus/lessons/round-8.md`: **not landed** (0 entries).
- Mid-draft v2a/v2b resolved: `plans/round-9.plan.md` was committed **with**
  the round-8 landing (the round-7 precedent, not the round-5/6 one); the
  gate's moving revision settled at `7da4ec50…` (2,887 L, selftest 217/217,
  PIN `d2bcdb31…`), independently confirmed by AUD-M8/VER-M8.

## 5. Scribe measurements and spot-checks (executed)

1. **Gate runs** (read-only, 19:58:09–19:59:11Z; logs `/tmp/w9-scr-m9/`):
   `--selftest` → `217/217` rc 0; `--no-live` → `counts: pass=20 fail=0
   unknown=0 skip=8 note=3` + CLEAN rc 0; live → `counts: pass=43 fail=0
   unknown=0 skip=0 note=7` + CLEAN rc 0; `--regression` → `MADO_REGRESSION:
   PASS` rc 0, 33.6 s, `REGRESSION_DATE 2026-10-14T19:58:37Z`, target
   `d2bcdb31…`, spec `c7ee75b9…`, table `match=10/10 flips=0`, cleanup
   `removed=10`, workdir removed on PASS (§1.2). Gate sha re-measured
   identical before and after, and again at 20:00:09Z.
2. **Census + suite coverage** (§1.3): 162 `row` + 6 `row_from_rc` = 168
   sites; prefix census omarchy 56 / hypr-live 51(+6 rc) / hypr 23 / waybar
   17 / terms 10 / gate 3 / walker 2; 51 distinct ids; asserted union 22
   (listed); seven helper regex sites carrying seven ids; `theme` plane 0
   row sites; `live.theme.current` NOTE at `:2565`/`:2569`; walker rows
   `:2539-2559`.
3. **Live anchors** (§1.4, re-run 20:00–20:01Z): all held — theme.name
   `matte-black` 12 B; `omarchy theme current` → `Matte Black`; background
   and mako symlinks resolve into `current/theme/`; swaybg 1203358 with the
   background symlink and `-m fill`; layers DP-1 level 0 `wallpaper`
   1203358 / level 2 `waybar` 1203352, no walker namespace; walker 1203471;
   `dev.benz.walker` owner 1203471; both sockets `srwxr-xr-x` 0 B, mtime
   13:11:09 (session unchanged since rounds 7/8).
4. **Boundary**: writes = this draft + `/tmp/w9-scr-m9/` only; no substrate
   file written; no live session disturbed; no socket connected; no network
   command; **no `git status`/`fetch` on the omarchy checkout**; no mutating
   `omarchy` verb.

## 6. Observations (v1)

(a) The plan's design-time base predates the round-8 landing by ~41 minutes
    and every gate number it carries is a round-7 value (§0.1). The finalizer
    must not copy "106", "40", "89", or `90d50cdd…` into the record without
    the landed re-measure — the same stale-base class rounds 7 and 8 both
    record.
(b) The precondition set resolved unevenly [OBS]: (a8) partial — the
    *omarchy* stub idiom landed, the hypr-live stub variant did not; (b8)
    satisfied incl. the regex widening; (c8) unsatisfied. The plan's
    ordering clause ("if (a8) did not land, live rows exempted by name")
    must therefore be applied **per row**, not per stage: a theme live row
    that can ride the omarchy idiom is exercisable; a socket/bus row likely
    is not (§3.2).
(c) The plan's stage (a) has a fixture-shape problem the plan does not
    state: the frozen fixture carries the theme include at **fixture line
    11** (host `:13`), a three-file theme dir, a source-less hyprlock
    fixture, and no mako/swayosd/background fixtures — any faithful chain
    test grows `build_fixture`, which sits outside every marked block and
    therefore re-cuts `PIN_MADO` (§1.5). That re-cut is the plan's own
    stage-(c) receipt; the two requirements are one mechanism, not two.
(d) The socket row's hermetic problem is structural, not cosmetic: `--root`
    roots a `$HOME`-shaped tree; `$XDG_RUNTIME_DIR` and the session bus sit
    outside it. Either the landed read shape accepts a seam, or the rows are
    exempt by name and counted — the plan's own fallback.
(e) The rc-6 arm and the two usage arms are now three rounds old (rounds
    6/7/8 recorded them). Round 9's (c) touches the helper neighbourhood; if
    it re-cuts `PIN_MADO` it may be the natural place to pin or remove the
    arm — but the plan does not claim it, so the record must not read it as
    landed.
(f) Record debt is now four rounds deep: README 8 rows (nine notes), SCORECARD
    4–8 stubs, LOG 4–8 one-liners, the round-8 draft's 19 ⟨PENDING⟩s, and
    `corpus/lessons/` empty for a ninth round. §4 carries ready-to-apply
    text; every round that lands notes without repaying deepens the hole.
(g) The live anchors all held a third time, and the sockets' mtime still
    equals the session start second (13:11:09) — no restart since rounds
    7/8 [OBS]. If any pin moves mid-round, the MOVED reading is the round's
    first finding, never an edit of the baseline.

## 7. Unknowns (v1)

1. Whether (a)/(b)/(c) land in-window, and at which gate revision; which
   rows ship vs are exempted **by name**; the exemptions' clause anchors.
2. Whether the `theme` §6 `walker_css`/`swayosd_css` split lands as one row
   or two; whether `theme.choice` stays exactly today's NOTE.
3. Whether the mako symlink row can be fixture-rooted under `--root` (a
   fixture home carries its own mako path) — counted at dispatch.
4. Whether the walker socket rows can be hermetically exercised (fixture
   socket vs override seam vs exemption by name) and whether a `busctl`
   stub is acceptable under the omarchy stub discipline.
5. Whether (c) re-cuts `PIN_MADO` and what spec/target shas the receipt
   carries; whether a mutant survives (a FINDING, not smoothed).
6. Whether the round pays any of the four-round record debt (§1.6) or defers
   again; whether `corpus/lessons/round-9.md` lands and who sits as its
   non-author seat.
7. Which lanes attest round 9 (AUD/VER scratch seen at v1 but no verdict
   artifact exists) and their self-labels — record by artifact self-label.
8. Whether round-8's unlanded residue (hypr-live stubs J/K/L; the assertion
   floor incl. the rc-6 decision) is picked up by any round-9 lane or stays
   carried.
9. Whether the gate stays at `7da4ec50…` through the round — every number in
   this draft is tied to that sha; the finalizer re-pins from the commit.

## 8. Falsifiable next-iterations (carry + new)

- Land (a) with the covered-row list, the file/live split, and the fixture
  re-cut recorded; state exemptions by name; re-run `--selftest` and the
  regression at the landed revision.
- (b) only with the hermetic route named per row (or the counted exemption);
  the sockets never connected; the errata append measured by sha.
- (c) with the helper-regex widening proven by a before/after id count and a
  `MADO_REGRESSION: PASS` carrying `MUTATE_RESTORE: OK` and target sha
  before = after; the receipt lines quoted in the record.
- Repay record debt (README 9 + round 9; SCORECARD 4–8 full rows + 9;
  round-8 draft ⟨PENDING⟩ fill as an appended erratum; LOG 4–7 fuller
  entries optionally).
- Charter `corpus/lessons/round-9.md` or record why no independent seat
  exists.
- Durability: fold receipt lines + tool/harness/target shas + gate sha into
  the record (scratch does not survive; the audit's kept workdirs are
  ephemeral).

## 9. Finalization checklist (mechanical, ordered)

1. Re-measure §1.1/§1.2 anchors; note drift as freshness rows; re-run the
   three verify modes and `--regression` at the revision being committed.
2. Read the landed (a) rows; list landed ids (incl. the split question);
   count assertions (217 → ?) and asserted ids (22 → ?); verify each live
   row is stub-backed per the (a8) resolution or exempted by name; verify
   the fixture re-cut and the extended spec sha.
3. For (b): verify each walker row's route (fixture/stat/busctl/layers); the
   sockets stat'd, never connected; the errata append's sha before → after.
4. For (c): verify the widened helper regex sites (all seven), the census
   before → after, the re-cut receipt (spec, target, table, restore,
   workdir), any survivor recorded as a finding.
5. Census before → after by the counting commands; quote `--no-live` and
   live verdicts at the committed revision.
6. Apply §4a (LOG), §4b (README), §4c (SCORECARD), §4d (SHONEN — likely
   no-op), §4e (errata), §4f (round-8 draft closure erratum).
7. Commit under the lane identity; freeze every cited sha in the entry; check
   the gate/harness/note shas appear; confirm no `git status` ran on the
   omarchy checkout during the round.
8. If (a)/(b) land only in file-plane form: record the unshipped live rows
   with their exemptions and keep this draft as the record's ancestry.

## 10. v2 updates (append as artifacts land)

**v1 cut (20:05Z): nothing landed.** `git status --porcelain` empty at
19:57:46Z and 20:00:09Z; gate sha `7da4ec50…` unchanged through both polls;
no new file under `corpus/knowledge/`, `corpus/lessons/`, `reports/`,
`tools/`; `plans/round-9-record-draft.md` (this file) is this lane's only
write. Lane activity is scratch-only (§1.8). Poll targets for the finalizer:
`sha256sum tools/mado-verify.sh` (≠ `7da4ec50…`), `grep -cE '^[[:space:]]*row
theme ' tools/mado-verify.sh` (today 0 — count row sites, not the word
`theme`, which appears throughout), `grep -c 'walker.sock' tools/mado-verify.sh`
(today 0), `bash tools/mado-verify.sh --selftest` count (>217),
`git status --porcelain`, `ls corpus/lessons/`.

**v2a (20:02:35Z): the round-9 gate lane has begun — the baseline moved.**
`tools/mado-verify.sh` is now modified in the worktree: sha
`5b6ace8e5a2fe3e2…`, **2,922 L / 134,263 B**, mtime 17:02:22.575 −03:00,
`git diff --numstat` **+42/−7** vs the committed revision. Readings at this
instant: `grep -cE '^[[:space:]]*row theme '` → **0** (no theme rows yet);
`grep -c 'walker.sock'` → **0**. `--selftest` on that in-flight revision
printed `MADO_SELFTEST: FAILED — 216 passed, 1 failed` — `R10: derived target
equals the recorded gate revision (got 'c3e3aac8…' want 'd2bcdb31…')`, i.e.
the pin-re-cut alarm firing because the additions sit outside the three
marked families (§3.3); the run's exit code was not measured through the
pipe. The file moved **again during the run** (sha `62f81516d8320e6a…`
immediately after). This is another lane's single-writer work; this scribe
lane read it, never touched it. Consequence for the record: every gate pin
in this draft names the **round-8-landed** revision `7da4ec50…` as the v1
baseline; the finalizer must re-pin from the commit, never from this note.
The poll targets above are live: re-run `sha256sum tools/mado-verify.sh` and
`bash tools/mado-verify.sh --selftest` before quoting anything.

**v2b (20:06:22Z): three round-9 artifacts are appearing — the theme rows
are landing, a walker note landed, and the next round's plan arrived.**
- `tools/mado-verify.sh` (in flight): sha `93e43f8fe8b9bdd4…`, 3,231 L,
  mtime 17:05:32 −03:00, `git diff --numstat` **+352/−8** vs the committed
  revision. **Theme row sites now exist**: `grep -cE '^[[:space:]]*row theme '`
  → 27; distinct theme ids so far
  `theme.name.read`, `theme.chain.walker_css`, `theme.chain.swayosd_css`,
  `theme.parts.declared_only` (in-flight list, not the landed set); distinct
  row ids 51 → **55**. `walker.sock` still 0 hits. Do not quote these as
  landed — the file is still moving.
- New note, **another lane's artifact**: `corpus/knowledge/walker-deep-r9.md`
  (self-label "Walker deep-note r9 — version/shape + config reload semantics
  (M9-2, round 9)"), 398 L / 24,391 B / `a5acfe0162c9e5cd…`. It is *not* the
  owed `walker-deep.md` §10/§11 errata append (that file's sha is still
  `0982ba066c72575a…` at this poll) — the record must not conflate them.
- `plans/round-10.plan.md` appeared (PREP-M10; 295 L / 19,322 B /
  `eca573b271e926e3…`), the next round's plan in-flight — the same pattern as
  rounds 5/6/7/8 (round 8 committed the round-9 plan with its landing; the
  finalizer decides, but this scribe lane did not write it).
- `plans/round-9-record-draft.md` is still this lane's only write; no
  `corpus/lessons/` entry yet; `git status` at the poll: gate modified, the
  three untracked files above.

**v2c (20:10:28–20:11Z): the theme plane is landing — rows, fixture re-cut,
and a green suite at the in-flight revision.** Poll readings, all tagged
in-flight (another lane's single-writer work; this scribe lane read it, never
touched it):
- `tools/mado-verify.sh`: sha `93e43f8fe8b9bdd4…`, 3,231 L / 150,103 B,
  mtime 17:05:32 −03:00 — **stable across three polls** (20:06:22Z,
  20:10:28Z, 20:10:43Z); `git diff --numstat` +352/−8 vs the committed
  revision.
- `--selftest` at that revision: **`MADO_SELFTEST: 268/268 assertions
  passed`** (green; 217 → 268 in flight). The previously failing R10 pin
  case is no longer the alarm at this point — the finalizer still re-runs the
  suite and `--regression` at the commit.
- **Theme rows now exist**: `grep -cE '^[[:space:]]*row theme '` → 27 sites;
  distinct theme ids seen in the `row theme` form so far
  `theme.name.read`, `theme.chain.walker_css`, `theme.chain.swayosd_css`,
  `theme.parts.declared_only` — plus helper-driven rows (`theme_*_row()`
  emitting `row theme "$id" …` around `:3016-3086`, e.g. the chain rows and
  the link/wallpaper rows); distinct row ids repo-wide 51 → **55** at v2b
  (re-count at the commit). `walker.sock` still **0** hits → the walker
  socket rows have not landed yet.
- **The fixture gaps recorded in §1.5 are being closed by this revision**
  (before-state of §1.5 re-confirmed against `git show HEAD:` — no mirror
  comment then): the fixture `hyprland.conf` now carries a three-line
  line-anchor comment putting the theme include at **fixture line 13** (the
  measured live anchor), and `build_fixture` writes
  `theme/{alacritty.toml,hyprlock.conf,mako.ini,walker.css,swayosd.css}`,
  `theme/backgrounds/0-fixture.jpg`, a `current/background` symlink, a
  `.config/mako/config` symlink, `.config/swayosd/style.css` and the walker
  theme css ([OBS] on the fixture tree my 20:02:35Z selftest run generated,
  `/tmp/w5-mado-m52-selftest.lCrUHY/<scenario>/`, kept on that run's
  failure; plus the worktree lines `:242`, `:300-311`). Scenario labels `T1`
  / `T8` (theme) appear in the suite.
- Helper regexes now carry **eight** ids — `(hypr|hypr-live|waybar|walker|
  terms|omarchy|theme|gate)` at `:387`, `:391`, `:406…` (widened as the plan's
  stage (c) requires; the exact site count is the finalizer's count).
- **New artifacts at this poll**: `reports/r9-ver-m9.md` — VER-M9, "round-9
  theme-arm verification (independent re-run: one arm's selftest case path +
  the live arm)", 139 L / 7,725 B / `98ec0c3b57a0d348…`, window 19:58–20:12Z,
  landing detected 20:02:13Z, stability 5 samples ~100 s (20:07:34Z); and
  (v2b) `corpus/knowledge/walker-deep-r9.md` (M9-2) and
  `plans/round-10.plan.md` (PREP-M10). The ledger files (LOG / SCORECARD /
  SKILL / README) were still untouched at 20:10Z; `corpus/lessons/` still 0
  entries.
- Consequence for the record: everything quoted in §0.1/§1.2/§1.3 is the
  v1 *before-state* at `7da4ec50…` and stays for provenance; the round's own
  numbers must come from the committed revision, and the §9 checklist
  re-runs from there.

⟨Append v2+ here as artifacts land: each update tagged with its own
measurement time; v1 numbers above stay for provenance. Re-run the §9
checklist from the landed revision, not from this draft's before-state.⟩