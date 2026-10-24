# mado — PROVINCE accuracy self-audit (round 4, lane M4-3)

**SELF-AUDIT — explicitly labeled.** This file is a self-audit: executed by
round-4 lane M4-3 (integrator-dispatched audit seat) against this repo's own
`PROVINCE.md`. All verdicts and counts carry `[~]` (asserted by the auditing
seat, not yet confirmed by the named non-author verifier). Per
`PROTOCOL.md:63-68`, only a named non-author verifier may write `[x]`;
**the named verifier closes SHONEN box 4** — this file does not close it
itself. §7 is the closure handoff; §8 lists every counting command so the
verifier can re-derive each number.

- Audited artifact: `PROVINCE.md`, 18 L, sha256
  `7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a` —
  unchanged since the mint commit `74d3b7b` (`git log -- PROVINCE.md` → 1
  commit). `[OBS]`
- Audit pass: 2026-10-14, commands run ~16:18–16:27 UTC (artifact span:
  scratch logs close 16:19:48Z–16:25:17Z; measurement verification closes
  16:27:04Z); read-only throughout (file bytes + read-only queries); no
  mutating verb executed; no secret content read (shape-only:
  names/sizes/modes/hashes); no network command; nothing written outside
  this file and `/tmp/w4-m4-3/`. `[OBS]`
- Concurrent edits: sibling lanes modified 5 corpus notes at 16:26:04Z and
  `SKILL.md` at 16:27:10Z (mid/post-read; consistent with the pending
  round-3 erratum list `[INF]`). Line anchors cited were current at read
  time and were re-verified by exact string at 16:27Z; where a number has
  drifted, resolve by string — e.g. the R3-1 §10 verb list read at `:433`
  resolves `:434`; the R3-2 boundary sentence read at `:20-21` still
  resolves `:20`.
- Not inspected, by discipline: window titles, `/proc/*/environ`,
  `hyprland.log` content, `.ufo/`/`.devin/` contents.
- Scratch logs (raw): `/tmp/w4-m4-3/` — `sweep.log`, `boundary-mtimes.log`,
  `live-checks.log`, `omarchy-probe.log`, `logs-and-id.log`,
  `r3-attribution.log`, `surfaces-extra.log`, `repo-scope.log`,
  `final-live.log`, `state-and-toggles.log`, `verify-deliverable.log`,
  `anchor-recheck.log`.
- Legend: `[OBS]` measured · `[INF]` inference from measured parts · `[UNK]`
  unknown · every count `[~]`.
- Counting convention: every count below names its command; like the
  round-1…3 notes, this file ends without a trailing newline (`wc -l` =
  editor view − 1; the round-1 obs (a) ambiguity is avoided by naming the
  command everywhere).

## §1 Claim census — 15/15 resolve `[~]`

| # | PROVINCE.md claim (line) | Live check (summary) | Result `[~]` |
|---|---|---|---|
| C1 | Domain: desktop/compositor craft — hypr/waybar/walker config plane + display behavior "on this host" (:1-4) | all declared path families resolve live (§2); corpus covers all five planes | HOLDS |
| C2 | Owns `~/.config/hypr/` incl. hyprland.conf, keybinds, rules, animations (:6-7) | dir exists; `hyprland.conf` 1,273 B with `grep -c '^source'` → 17; keybinds `bindings.conf` 2,879 B; rules `input.conf`/`ai-usage.conf` (+ sourced omarchy `windows.conf`); animations `looknfeel.conf` | HOLDS |
| C3 | Owns `~/.config/waybar/` (:7) | `config.jsonc` 6,068 B + `style.css` 1,887 B; sha256 = round-3 pins | HOLDS |
| C4 | Owns `~/.config/walker/` (:7) | `config.toml` 1,336 B; sha256 = round-3 pin | HOLDS |
| C5 | Owns terminal configs `alacritty\|foot\|kitty\|ghostty` (:7-8) | all four dirs + config files exist; programs: only `alacritty` on PATH (foot/kitty/ghostty not installed — same as MADO-3; F6) | HOLDS (config plane; alacritty the only live consumer) |
| C6 | Owns themes/wallpapers as declared files (:8-9) | `current/theme.name` 12 B; `current/theme/` 20+ files (incl. alacritty.toml, hyprland.conf, hyprlock.conf, mako.ini); `current/background` symlink → `theme/backgrounds/0-ship-at-sea.jpg` 1,681,677 B; `swaybg -i` consuming it (PID 1203358) | HOLDS |
| C7 | Owns screen/idle behavior (hypridle/hyprlock where present) (:9) | `hypridle.conf` 765 B, `hyprlock.conf` 742 B, `hyprsunset.conf` 363 B, `xdph.conf` 106 B present; live consumer caveat §6 | HOLDS (surface) |
| C8 | omarchy skill = documentation surface, read-only (:10-11) | `~/.agents/skills/omarchy/SKILL.md` only, `wc -l` → 392 L; mtime 2026-10-03 17:42 — untouched through rounds | HOLDS |
| C9 | All config trees READ-ONLY; probe/measure/recommend; operator applies (:11-12) | §3: zero writes in declared trees across rounds 1-3; one non-declared git-metadata caveat | HOLDS + caveat §3.5 |
| C10 | Refuses secrets in configs (shape-only → kagi) (:14) | §4: no secret values in repo; shape-only rules documented; `kagi-shokunin` exists | HOLDS |
| C11 | Refuses model endpoints (→ kama) (:14-15) | `kama-shokunin` exists; corpus scan: no endpoint content absorbed | HOLDS |
| C12 | Refuses model quality (→ kengaku) (:15) | `kengaku-shokunin` exists; corpus scan: no quality content absorbed | HOLDS |
| C13 | Never mutates a running compositor state (:15) | §3.4: read verbs only in rounds 1-3 (R2-1 §0 mutating-verb list; R2-2 boundary; R3-1 §10 `pkill` against scratch only); consumer-PID continuity through rounds 1-3 | HOLDS |
| C14 | Every claim is file-byte- or screenshot-verified (:16) | evidence classes in corpus (file bytes / hyprctl live / labeled `[INF-docs]` / consumer probe); screenshot instance: `grim -t ppm -`, `SKILL.md:203` (stdout only, nothing persisted per `SKILL.md:241`) | HOLDS |
| C15 | Out of province → report, never absorb (:18) | LOG reports out-of-province items (mint-shape defect → operator; grok-bot `[UNK]`); no absorption found in notes | HOLDS |

## §2 Surfaces — live detail `[OBS]`

- **hypr plane** — 13 files (12 active `.conf` + `autostart.conf.bak.1791942509`);
  full set re-hashed, 13/13 equal to the round-3 table (§8). `hyprland.conf`
  sources: 9 omarchy defaults (`~/.local/share/omarchy/default/hypr/…`),
  5 local (`monitors/input/bindings/looknfeel/autostart.conf`), 1 theme
  (`~/.config/omarchy/current/theme/hyprland.conf`), 1 state-toggles glob
  (`~/.local/state/omarchy/toggles/hypr/*.conf`), 1 plugin (`ai-usage.conf`)
  = 17 statements — the orchestrator reading is confirmed live.
- **waybar** — `config.jsonc` 6,068 B / `style.css` 1,887 B; live layer at
  level 2 (namespace `waybar`, PID 1203352 of the current session).
- **walker** — `config.toml` 1,336 B; `walker --gapplication-service`
  PID 1203471 (same runtime mode as round 3).
- **terminals** — `alacritty/alacritty.toml` 876 B; `foot/foot.ini` 516 B;
  `kitty/kitty.conf` 954 B; `ghostty/config` 1,325 B; all four hashes equal
  the round-3 F6-class pins (§8).
- **theme/wallpaper** — as C6; the theme tree also carries the terminal
  configs, i.e. the matte-black theme plane owns colors outside user configs
  (MADO-3 §6 unchanged).
- **idle/screen** — four consumer configs present (see C7); live state §6.
- **omarchy skill** — single file 392 L, untouched (C8).
- **adjacent, not declared** — `~/.config/mako/config` sha256 =
  R3-1 §10 pin `95bf0c86…` (no drift);
  `~/.local/state/omarchy/toggles/hypr/{flags.conf,window-no-gaps.conf}`
  present with 2026-10-03 mtimes — toggle override chain intact, untouched.

## §3 Boundaries held — mutations (rounds 1-3) `[~]`

1. **Repo scope.** `git log --all --name-only` (4 commits: `74d3b7b`,
   `65a2254`, `e1e1bb7`, `f9f58c0`): every path repo-internal (`SKILL.md`,
   `corpus/*`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `plans/*`, `AGENTS.md`,
   `MINT.md`, `PROVINCE.md`). No commit touches an external path.
   `PROVINCE.md` appears only in `74d3b7b`.
2. **Declared config trees.** `find ~/.config -maxdepth 4 -newermt
   "2026-10-14 09:40"` → 0 hits under `hypr/`, `waybar/`, `walker/`,
   `alacritty|foot|kitty|ghostty/`, `omarchy/`. All hits are other apps'
   state (obsidian, chromium, 1Password, Grok Bot, godot, fcitx, pulse, mpv,
   ai-usage — none a declared surface). Same result for
   `~/.local/state/omarchy` and `~/.agents` (0 hits).
3. **Byte pins.** 13/13 hypr + 4/4 terminals + waybar ×2 + walker ×1 +
   mako ×1 all equal the round-1…3 pins (§8). Rounds 1-3 commit timestamps
   (10:36 / 11:19 / 12:52 local) all precede this audit; zero drift.
4. **Compositor continuity.** Consumer PIDs recorded across rounds 1-3 are
   stable (waybar 1707, wallpaper 1710, walker 1808; `waybar` elapsed
   89,039 s at round-3 measure) — no restart is recorded or observable in
   rounds 1-3. The session restarted at 13:11:06 local, **after** round 3
   (§6): not attributable to rounds 1-3.
5. **Caveat — non-declared git metadata (the one qualifying finding).**
   `~/.local/share/omarchy/.git/index` mtime moved at 14:42:09Z, `.git` dir
   mtime at 15:42:18Z — both inside round-3 verification windows
   (R3-1 probe 14:38–14:47Z; scribe pass 15:38–15:47Z). Writer `[UNK]`;
   candidates: R3-1's own disclosed `git … status` probe
   (`waybar-walker-semantics.md:433`; `status --porcelain` quoted `:25`),
   the scribe's two-pin re-check, omarchy tooling, or the operator.
   Mechanism proven in scratch (`/tmp/w4-m4-3/gitmech/`): `git status
   --porcelain` refreshes the index stat cache — index mtime +1 s, tracked
   content sha unchanged. No tracked-content, refs, reflog (`logs/`
   untouched), or `FETCH_HEAD` change anywhere in the checkout (`find`).
   Classification: **git stat-cache metadata refresh in a non-declared
   installation checkout — no config tree, no content**. It does not
   falsify C9 (declared config trees read-only), but it qualifies the
   literal reading of the round-3 record's "Nothing under `~/.config/` or
   `~/.local/` was written" (`config-health-report-r3.md:20-21`) and is an
   erratum candidate (§Errata). Recommendation: use
   `git --no-optional-locks status` (or avoid `status` on foreign
   checkouts) and scope boundary sentences to named trees.
6. **Network.** No fetch evidence (no `FETCH_HEAD`/ref/reflog movement);
   R3-1 §10 declares `git ls-remote`/weather/update producers skipped; this
   audit ran no network command.

## §4 Boundaries held — secrets `[~]`

- **Repo scan** — `grep -rniE '(password|passwd|secret|token|api[-_ ]?key|
  bearer|credential)'` → 14 hits, all policy text or documented non-secret
  strings (shape-only rules `AGENTS.md:5`, `SKILL.md:31`,
  `PROVINCE.md:14`, `MINT.md:13,19`; hyprlock placeholder `"Enter Password"`
  `idle-lock-plane.md:158`; `1password --lock` lock-cmd/config mentions;
  walker CLI `--password` flag). Key-shaped scan
  (`sk-…|AKIA…|ghp_…|BEGIN … PRIVATE KEY`) → **0 matches**.
- **Shape-only practice** — documented: no window titles, no
  `/proc/*/environ`, `hyprland.log` untouched (R2-1 §0:19-21;
  R3-2 §0:21-23); secret-bearing material routes to kagi (C10). This audit
  replicated the discipline: client list read as pid+tags only (§6).
- **Adjacent secret-shaped material found (not a declared surface, not
  read)** — `~/.config/ai-usage/` contains `env` (309 B, mode 600),
  `providers` (282 B, 600), `providers.bak.alibaba` (264 B, 600),
  `selected` (5 B); state written every ~5 min by `ai-usage.timer`
  (`systemctl --user list-timers`). Names/sizes/modes only — **no content
  read**; not mado-declared; routing to kagi unchanged if ever in scope.

## §5 Refusals / routing `[~]`

- Sibling provinces exist as directories: `kagi-shokunin`, `kama-shokunin`,
  `kengaku-shokunin`.
- Refusal text `PROVINCE.md:14-15`; roster-scan rationale `MINT.md:13-14`;
  routing also referenced in `plans/round-5.plan.md:33`.
- Corpus content scan (endpoint/quality/secret topic words) → no absorbed
  claims; hits confined to the refusal/routing text itself and plan/LOG
  narration.

## §6 Live-state delta since round 3 (intel for the box-3 reviewer) `[OBS]`

- **Session restarted at 13:11:06 local** (16:11:06Z) via SDDM/uwsm
  (`sddm-helper … uwsm start … hyprland.desktop`); machine boot was
  2026-10-13 11:02 — a session restart, not a reboot. Round-3 measured
  state is **pre-restart**; live-consumer findings should be expected to
  move.
- PIDs: Hyprland 1671→**1203316**; waybar 1707→**1203352**;
  wallpaper/swaybg 1710→**1203358**; walker 1808→**1203471**;
  elephant 1811→**1203474**. `hyprctl -j instances` → `wl_socket
  "wayland-1"` (unchanged); layers: level 2 `waybar` 1203352, level 0
  `wallpaper` 1203358.
- **hypridle lifecycle in the new session**: started 13:11:07
  (PID 1203349); observed running 13:19:48 local; **absent by 13:23:31**
  (`pgrep -ax hypridle` → rc=1; `ps -p` empty). F1-class intermittent
  behavior reproduces; cause `[UNK]`; time window ≈ 13:19–13:23 local.
  Reviewer should timestamp any hypridle check.
- **F2-class tags** — both current terminal windows carry
  `["default-opacity*","terminal*"]` (`hyprctl -j clients`, reduced to
  pid+tags; no titles read). Round-3's Alacritty PIDs are gone with the
  old session.
- **File-byte rows are unaffected** — all pins re-verified equal (§3.3);
  the delta is live-state only.

## §7 SHONEN box 4 — closure handoff `[~]`

Box: "No cross-domain bleed (PROVINCE.md still accurate)" — current mark
`[~]` in `SHONEN.md` (12 L) with pointer
`corpus/knowledge/config-health-report-r3.md §1`. Round-4 plan: "an audit
seat verifies every PROVINCE.md claim against live reality … — named,
closes box 4"; anti-claim: any non-reproduction or province violation keeps
the box open and says why.

Closure procedure for the named non-author verifier (a self-audit does not
self-close — `PROTOCOL.md:63-68`):

1. Re-run the §8 commands (read-only); spot-check ≥3 claims across
   different evidence classes (§1 rows; §3 pins).
2. If all reproduce: write `[x] <verifier-id>` with a pointer to this file
   in `SHONEN.md` — the only file change needed, and outside this file's
   write scope.
3. If anything fails: keep `[~]`; record the failing claim, command, and
   observed value (append-only; do not edit this file's body).

This file's counts stay `[~]` until that closure lands.

## §8 Counts `[~]` — every count with its command

| Command | Result |
|---|---|
| `wc -l PROVINCE.md` / `sha256sum PROVINCE.md` | 18 L / `7aad7b863dc3c10b…` |
| `git log --all --name-only` | 4 commits, repo-internal paths only |
| `git log --format='%h %ci' -- PROVINCE.md` | `74d3b7b 2026-10-14 09:50:45 -0300` (1 commit) |
| `find ~/.config -maxdepth 4 -newermt "2026-10-14 09:40"` | 0 hits in declared trees (non-surface hits §3.2) |
| `find ~/.local/share/omarchy -newermt "2026-10-14 09:40"` | `.git/index` 14:42:09Z; `.git` dir 15:42:18Z — only entries |
| `find ~/.local/state/omarchy ~/.agents -newermt "…09:40"` | 0 hits |
| `sha256sum ~/.config/hypr/*.conf` + `autostart.conf.bak.…` | 13/13 equal R3-2 §2.1 pins (`hyprland.conf` `4f52854a3c143dcf…`; `bindings.conf` `e574a1ed08535e31…`; `looknfeel.conf` `777a4fdc8b61db44…`; `bak` `8b472371e78b7f8b…`) |
| `sha256sum ~/.config/waybar/style.css` | `8316c08ceaa7e3f0…` = R3-1 §10 pin |
| `sha256sum ~/.config/waybar/config.jsonc` | `07f7d663106b72e4…` = R3-1 §10 pin |
| `sha256sum ~/.config/walker/config.toml` | `fecf71fa4253803e…` = R3-1 §10 pin |
| Terminals `sha256sum` | `695301c86577c808…` alacritty / `3e88354476f2682e…` foot / `f875291ecfe64ebc…` kitty / `cb828c044b07d4fd…` ghostty = R3-2 §5 pins |
| `sha256sum ~/.config/mako/config` | `95bf0c86c955cc81…` = R3-1 §10 pin |
| `grep -c '^source' ~/.config/hypr/hyprland.conf` | 17 |
| `wc -l ~/.agents/skills/omarchy/SKILL.md` | 392 |
| `hyprctl version` / `hyprctl configerrors` | 0.56.2 `efb5099…` / empty, rc=0 |
| `hyprctl -j instances \| jq -c '.[0].wl_socket'` | `"wayland-1"` |
| `pgrep -x hypridle` | rc=0 PID 1203349 (16:19:48Z) → rc=1 (16:24:16Z) |
| `hyprctl -j layers` (namespace+pid) | `wallpaper` 1203358 / `waybar` 1203352 |
| `ps -eo pid,lstart,args` (consumers) | session start 13:11:06–13:11:07 local |
| `who -b` / `uptime -s` | boot 2026-10-13 11:02 / 10:57:58 |
| `systemctl --user list-timers --all` | `ai-usage.timer` (~5 min; LAST 13:16:28 local) |
| `ls -la ~/.config/ai-usage/` | env 309 B/600 · providers 282 B/600 · bak 264 B/600 · selected 5 B/644 |
| Secret scans (§4) | 14 policy-text hits / 0 key-shaped |
| Scratch mechanism test (`/tmp/w4-m4-3/gitmech/`) | index mtime `1791995056→1791995057`; content sha `ce013625…` unchanged |
| This file's count convention | no trailing newline (round-1…3 convention) — `wc -l` = editor view − 1 |

## §9 Unknowns

- U1 — Writer of the `~/.local/share/omarchy/.git` metadata touches: no
  line in the cited raw logs pins a command to the 14:42:09Z/15:42:18Z
  mtimes; candidate set in §3.5; timing + disclosed verb make R3-1's
  `git status` most plausible `[INF]`, not proven.
- U2 — Whether omarchy tooling or the operator ran the underlying git
  command (no fetch/ref/reflog evidence either way).
- U3 — Content of `~/.config/ai-usage/*` (secret-shaped; correctly not
  read; routes to kagi if ever in scope).
- U4 — Whether the F1-class hypridle exit recurs deterministically in this
  session (a single lifecycle observed: 13:11:07 → gone by 13:23:31; no
  journal read — exec-once process, not a user unit).
- U5 — SKILL.md round-2/3 authoring lane (carried `[UNK]` from LOG; not
  part of box 4; not audited here).

## Errata (append-only)

_None yet — corrections to this file append below; earlier text is never
edited. Candidates noted during the audit (not applied — write scope):_

- E-candidate 1: `config-health-report-r3.md:20-21` — scope "Nothing under
  `~/.config/` or `~/.local/` was written" to named trees, or carry the
  git-metadata caveat (§3.5).
- E-candidate 2: `waybar-walker-semantics.md:433` (read-time; resolves
  `:434` at the 16:27Z re-anchor) — note `git status`'s
  index stat-cache write side effect in the probe-verb list.

## Round-5 addendum — §8 re-run receipt (M5-1, box-4 close evidence) [OBS] `[~]`

Appended 2026-10-14 17:07Z (local 14:07, −03:00) by round-5 lane M5-1. This
block answers the recorded box-4 close condition — "§8 re-run owed / needed"
(`LOG.md:294`, round-4 entry; `MANIFEST.json` fleet round-4 note) = §7 closure
step 1: re-run the §8 commands (read-only) and spot-check ≥3 claims across
evidence classes. Append-only: nothing above was edited (base sha verified
immediately before this append). Read-only throughout; writes = this append +
scratch `/tmp/w5-mado-m5-1/` (`rerun.log`, `live.log`, `scans.log`, `gitmech/`;
ephemeral — the measurements below are the durable record). No network command;
no mutation verb; secrets shape-only (no content read). Times UTC unless marked
local (−03:00); pass window 17:03:51–17:07Z.

- **Base revision (pre-append, measured):** sha256 `3014a84060c95710…`; 264 L by
  `wc -l` = editor 265 − 1; last byte `.`; 17,856 B. The count-convention row is
  re-measured TRUE a third independent time (audit v3-era, VER-M4, this run).
  This append lands as **v4** — per VER-M4 §3, a later revision re-opens only
  the delta; the delta is this block.
- **VER-M4 finding carried:** all 15 PROVINCE claims reproduced; the sole
  falsified claim (v1/v2 count-convention line) was corrected in v3 pre-filing
  and accepted; final verdict `/tmp/w4-ver-m4-scratch/VERDICT.md` 120 L by
  `wc -l`, sha256 `1101c7bff5e6f6ee…` (scratch; ephemeral) — "any future
  change must append".

### §8 re-run — all 25 rows re-executed (four hash rows grouped; 22 lines)

| §8 row (abridged) | Recorded (audit) | Re-run observed 17:03–17:06Z | Verdict |
|---|---|---|---|
| `wc -l` · `sha256sum PROVINCE.md` | 18 L · `7aad7b863dc3c10b…b135a` | 18 L · `7aad7b863dc3c10b…b135a` | REPRODUCES |
| `git log --all --name-only` | 4 commits, repo-internal only | 5 commits (`+3d9ba45` = the round-4 commit), every path repo-internal | REPRODUCES (count moved by the round-4 commit itself) |
| `git log --format='%h %ci' -- PROVINCE.md` | `74d3b7b 2026-10-14 09:50:45 -0300`, 1 commit | equal | REPRODUCES |
| `find ~/.config -maxdepth 4 -newermt "09:40"` (declared-tree filter) | 0 | 0 (320 raw hits, all non-surface state: chromium, obsidian, Grok Bot, 1Password, …) | REPRODUCES |
| `find ~/.local/share/omarchy -newermt "09:40"` | `.git/index` 14:42:09Z; `.git` dir 15:42:18Z — only entries | index 11:42:09 local (= 14:42:09Z), unchanged; `.git` dir 13:23:14 local (one further metadata move, already witnessed by VER-M4 §2.2); still only entries | REPRODUCES (era note) |
| `find ~/.local/state/omarchy ~/.agents -newermt "09:40"` | 0 | 0 | REPRODUCES |
| `sha256sum ~/.config/hypr/*.conf` + `autostart.conf.bak.…` | 13/13 = R3-2 §2.1 pins | 13/13 equal (`21e76af9…` `5ace1701…` `e574a1ed…` `04af5cdf…` `e7d3b8dd…` `4f52854a…` `b8d173dc…` `3042e4a9…` `3769c92a…` `777a4fdc…` `69c9d899…` `2fded88a…` `8b472371…`) | REPRODUCES |
| waybar ×2 · walker · mako `sha256sum` | `8316c08c…` `07f7d663…` `fecf71fa…` `95bf0c86…` | equal | REPRODUCES |
| terminals `sha256sum` | `695301c8…` `3e883544…` `f875291e…` `cb828c04…` | equal | REPRODUCES |
| `grep -c '^source' ~/.config/hypr/hyprland.conf` | 17 | 17 | REPRODUCES |
| `wc -l ~/.agents/skills/omarchy/SKILL.md` | 392 | 392; sha `becd149e4d1c0767…`; mtime 2026-10-03 17:42 | REPRODUCES |
| `hyprctl version` · `configerrors` | 0.56.2 `efb5099…` · empty, rc=0 | equal (empty, rc=0, 0 B) | REPRODUCES |
| `hyprctl -j instances \| jq` | `"wayland-1"` | `"wayland-1"` | REPRODUCES |
| `pgrep -x hypridle` | rc=0 16:19:48Z → rc=1 16:24:16Z | rc=1 at 17:04:32Z; the on→off transition is not re-observable (state changed by design; F1-class) | REPRODUCES (era) |
| `hyprctl -j layers` (namespace+pid) | `wallpaper` 1203358 / `waybar` 1203352 | same PIDs — no restart since the audit session | REPRODUCES |
| `ps -eo pid,lstart,args` (consumers) | session start 13:11:06–13:11:07 local | 13:11:06–07 local (Hyprland 1203316, waybar 1203352, swaybg 1203358, walker 1203471, elephant 1203474) | REPRODUCES |
| `who -b` · `uptime -s` | boot 2026-10-13 11:02 · 10:57:58 | equal | REPRODUCES |
| `systemctl --user list-timers --all` | `ai-usage.timer` ~5 min; LAST 13:16:28 local | `ai-usage.timer` ~5 min; LAST 14:02:11 local | REPRODUCES (era values) |
| `ls -la ~/.config/ai-usage/` | 309 B/600 · 282 B/600 · 264 B/600 · 5 B/644 | equal (shape-only; no content read) | REPRODUCES |
| Secret scans (§4) | 14 policy-text hits / 0 key-shaped | 33 policy-text hits (pre-append; = VER-M4's post-growth 33) / 0 key-shaped | REPRODUCES (substance; count = repo growth, frozen since 16:28Z) |
| Scratch mechanism test | index mtime +1 s; content sha unchanged | `/tmp/w5-mado-m5-1/gitmech/`: index `1791997503→1791997504`; blob `ce013625…` unchanged | REPRODUCES |
| This file's count convention | no trailing newline; `wc -l` = editor − 1 | TRUE (264 = 265 − 1; last byte `.`) | REPRODUCES |

### Spot-checks (cross-class, ≥3 per §7 step 1) — 4 executed

1. File bytes — `hyprland.conf` 1,273 B / 29 L / `4f52854a3c143dcf…` (C2 row + §2 + VER-M4 §4.1).
2. Live read — `hyprctl -j binds` → 192; `configerrors` empty rc=0.
3. Repo scan — declared-tree `find` 0 hits; key-shaped scan 0; `git log --all` repo-internal only.
4. Live timeline — consumer lstart 13:11:06–07 local; `pgrep -x hypridle` rc=1 at 17:04:32Z.

### Verdict `[~]`

All 25 §8 rows re-derive from current reality; every durable row is byte-equal
(13/13 hypr, 4/4 terminals, waybar ×2, walker, mako, `PROVINCE.md`, omarchy skill).
The only moved values carry named causes: commit count 4→5 (the round-4 commit
`3d9ba45` itself), secret-hit count 14→33 (repo growth, = VER-M4 §2.2), the
omarchy `.git`-dir metadata mtime (one further move since the audit — already
witnessed; index/refs/tracked content unchanged). Era values (PIDs, timers,
hypridle state) re-measured live and labeled; no session restart since the audit.
**No falsification found.** §7 closure step 1 is satisfied at base `3014a840…`;
step 2 — the `[x] <verifier-id>` + pointer write in `SHONEN.md` (12 L, sha
`f6495fe68f42…` at this receipt's time; box 4 still `[~]` at `:11`) — remains the
named non-author verifier's edit, outside this block's scope.

### Unknowns added

- U6 — mover of the omarchy `.git`-dir mtime since the audit (one further move;
  metadata-only) — same class as U1/U2; candidates include a verifier's own read
  per the audit's E-candidate-1 mechanism.
- U7 — whether hypridle's traceless on/off recurs (F1; U4 stands).
- U8 — repo-scope counts (commits, secret hits) are era-stamped: sibling lanes
  write during this wave (`SKILL.md`, plans).