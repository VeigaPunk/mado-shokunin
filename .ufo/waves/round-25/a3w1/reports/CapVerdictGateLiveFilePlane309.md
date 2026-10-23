# CapVerdictGateLiveFilePlane309 — C2 row re-run: SCORECARD.md:309 (`verdict gate (live + file plane)`)

Seat: `MadoR25A3.CapVerdictGateLiveFilePlane309` (leaf executor, C2 row contract). Wave: round-25 attempt 3, `a3w1`
(pre-data). Lane tip `1ed41fa8`; measured base `41cc04c8`.

## What I did

1. Read the named row in the base blob (`git -C <lane> show 41cc04c8:SCORECARD.md` → 1,618 lines, content
   sha256:`6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08`). Line 309 sits under
   `## Round 12 (kaika) — results` (line 276) in `### Capabilities (round 12)` (line 304):
   `| verdict gate (live + file plane) | Read-only verdict over the declared config plane and live hyprctl surfaces,
   exit 0/1/2, boundary check | \`bash tools/mado-verify.sh\` → \`MADO_VERIFY: CLEAN (52 pass, 8 notes …)\`,
   \`.ufo/evidence/round-12/gate-live-after.txt\` | 5 (re-demonstrated 12) |`.
   - Capability stated: read-only verdict over the declared config plane **and** live hyprctl surfaces, exit map
     0/1/2, with a read-only boundary check.
   - Demonstration command: `bash tools/mado-verify.sh` (bare = live read-only run against `$HOME`).
   - Evidence pointer: `.ufo/evidence/round-12/gate-live-after.txt` (present at `41cc04c8`, 66 lines). Its tail:
     `counts: pass=52 fail=0 unknown=0 skip=0 note=8` / `MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes
     verified read-only)` / `exit=0`. It carries no measured-commit or gate-sha header (round-12-era receipt shape).
2. Made the sandbox clone and detached at the base:
   ```
   unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
   mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
   git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapVerdictGateLiveFilePlane309
   git -C /fast/scratch/hyaku/mado-r25a3/c2/CapVerdictGateLiveFilePlane309 checkout -q --detach 41cc04c8
   # rev-parse HEAD → 41cc04c8d593837a0d5078bffaacdaa163d12897
   ```
   Gate under test: `tools/mado-verify.sh`, 4,194 lines,
   sha256:`050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` — byte-identical to the pin recorded at
   `SCORECARD.md:1221` (`050efc72…`, 4,194 L, selftest 460/460).
3. Re-ran the demonstration command in the clone, exactly as written, wrapped as the contract requires
   (`timeout 600`, `prlimit --as=4000000000`), GIT_* unset, no `MADO_VERIFY_ROOT` override (bare live run against
   `$HOME`):
   ```
   cd /fast/scratch/hyaku/mado-r25a3/c2/CapVerdictGateLiveFilePlane309 && {
     timeout 600 prlimit --as=4000000000 -- bash tools/mado-verify.sh; echo "exit=$?"; } 2>&1
   ```
4. grepped the whole SCORECARD.md at `41cc04c8` for later rows/text that supersede or contradict line 309
   (findings in the section below).

## Verbatim command output (complete, 66 lines; wall time ≈ 8.9 s)

```
mado-verify.sh v1 (mado-shokunin round 5 / M5-2)
mode: live (read-only) | root: /home/vgpnk | hyprctl: yes
plane     check                           status  detail
hypr      hypr.file.root                  PASS    hyprland.conf present (32 L)
hypr      hypr.root.orchestrator          PASS    0 settings lines (pure orchestrator)
hypr      hypr.root.include_graph         PASS    18/18 sources, order exact, set exact
hypr      hypr.root.sources_resolve       PASS    declared targets exist, member set exact
hypr      hypr.local.inventory            PASS    13/13 active local confs, set exact
hypr      hypr.local.envs_orphan          PASS    sourced by nothing; declares 3 env vars (F3 stays open)
hypr      hypr.toggle.no_gaps             PASS    toggle declares gaps_in/gaps_out/border_size = 0
hypr      hypr.file.sha_pin               NOTE    hyprland.conf sha256 ce7483f35ab5… drifted from round-1 pin 4f52854a3c14…; re-verify anchors
hypr      hypr.backups                    NOTE    2 backup file(s) under ~/.config/hypr (S3 litter class)
hypr-live live.hypr.version               PASS    Hyprland 0.56.2 efb5099… (pin matches)
hypr-live live.hypr.instances             PASS    4 instances; targeting the session's own signature (no guessing)
hypr-live live.hypr.configerrors          PASS    empty (config loads clean)
hypr-live live.hypr.gaps_out              PASS    custom='0 0 0 0' set=True
hypr-live live.hypr.kb_layout             PASS    str='br' set=True
hypr-live live.hypr.zero_chrome           PASS    border_size=0, rounding=0 (toggle/style owns)
hypr-live live.hypr.animations            PASS    enabled=1
hypr-live live.hypr.binds_count           PASS    192 binds (file arithmetic closes)
hypr-live live.hypr.monitor_dp1           PASS    DP-1 3440x1440@99.997
hypr-live live.hypr.scroll_factor         PASS    scroll_factor=0.4
hypr-live live.consumer.hypridle          PASS    hypridle running (idle chain has a consumer)
hypr-live live.env.gdk_scale              PASS    GDK_SCALE=1
hypr-live live.env.nvd_backend            PASS    NVD_BACKEND unset (orphan envs.conf effect provably absent, F3)
hypr-live live.waybar.version             PASS    Waybar v0.15.0 (pin matches)
hypr-live live.waybar.process             PASS    waybar pid 1664
hypr-live live.waybar.layer               PASS    DP-1 level 2 pid 1664 3440x26
hypr-live live.waybar.tray                PASS    tray watcher answers: as 0
hypr-live live.walker.version             PASS    2.17.2 (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)
hypr-live live.walker.services            PASS    app-walker@autostart + elephant active
hypr-live live.theme.current              NOTE    omarchy theme current → 'Matte Black' (operator-owned; not a verdict input)
waybar    waybar.config.parse             PASS    JSONC parses (260 L, 6354 B)
waybar    waybar.config.reload_style      PASS    reload_style_on_change = true (style reloads; modules need restart)
waybar    waybar.config.bar_globals       PASS    layer=top, position=top, height=26
waybar    waybar.style                    PASS    style.css imports the theme css
walker    walker.config                   PASS    TOML parses; 4/4 keys match (focus/wrap/theme/hints)
terms     term.alacritty.toml             PASS    TOML parses
terms     term.alacritty.theme_import     PASS    imports omarchy/current/theme/alacritty.toml
terms     term.cross.font_size            PASS    12.5 in all 4 present configs (MADO-3 §3)
terms     term.cross.padding              PASS    padding 14 on both axes in all 4 present configs
omarchy   omarchy.version.file            PASS    HELD: version file '3.8.3' (P2 pin; == HEAD:version blob at the pinned HEAD)
omarchy   omarchy.skill.link              PASS    HELD: symlink into the checkout (one file; nothing to drift)
omarchy   omarchy.skill.sha               PASS    HELD: leaf sha256 becd149e4d1c… (P4 pin)
omarchy   omarchy.version.cmd             PASS    HELD: 'omarchy version' → 3.8.3 (P1 pin)
omarchy   omarchy.git.tag                 PASS    HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
omarchy   omarchy.skill.vs_head           PASS    worktree == HEAD blob (index-free; no local edit)
omarchy   omarchy.cmd.groups              PASS    HELD: all 11 skill groups present (56 live groups in --json --all)
omarchy   omarchy.cmd.surface             NOTE    HELD: 282 commands in --json --all (counter only, not a verdict input)
omarchy   omarchy.theme                   NOTE    HELD: 'Matte Black' (operator-owned; D-1: never a verdict input)
omarchy   omarchy.doc.drifts              NOTE    R2 carried: 5 *.d hook dirs live vs flat files in the skill text (MADO-3 §7); R1 route-table drift declared in the note, not re-derived here
theme     theme.name.read                 PASS    theme.name = 'matte-black' (one line, machine-name shape)
theme     theme.chain.hypr_include        PASS    line 13 imports current/theme/hyprland.conf (target exists)
theme     theme.chain.hyprlock            PASS    line 1 imports current/theme/hyprlock.conf (target exists)
theme     theme.chain.waybar_css          PASS    line 1 imports current/theme/waybar.css (target exists)
theme     theme.chain.alacritty           PASS    line 1 imports current/theme/alacritty.toml (target exists)
theme     theme.chain.mako_link           PASS    symlink → .config/omarchy/current/theme/mako.ini (inside .config/omarchy/current/theme)
theme     theme.chain.walker_css          PASS    package 'omarchy-default' style.css imports current/theme/walker.css (target exists)
theme     theme.chain.swayosd_css         PASS    style.css imports current/theme/swayosd.css (target exists)
theme     theme.wallpaper.link            PASS    symlink → .config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg (inside .config/omarchy/current/theme/backgrounds)
theme     theme.parts.declared_only       NOTE    declared-only, consumer absent: foot.ini(foot) kitty.conf(kitty) ghostty.conf(ghostty) helix.toml(helix) vscode.json(code) keyboard.rgb(asusctl)
gate      boundary.readonly               PASS    config plane byte-identical before/after (combined sha ddb0780742f8…)
counts: pass=53 fail=0 unknown=0 skip=0 note=7
MADO_VERIFY: CLEAN (53 pass, 7 notes; file + live planes verified read-only)
exit=0
```

## Supplementary exit-map probes (same clone; read-only; **not** the demonstration command)

The row's claim names an exit map 0/1/2, so I probed the two non-clean arms without touching any substrate:

```
$ timeout 60 bash tools/mado-verify.sh --bogus
usage error: unknown argument '--bogus'
usage: mado-verify.sh [--no-live] [--live] [--root DIR] [--selftest] [--help]
  ... (usage text) ...
verdict: MADO_VERIFY: CLEAN|DIVERGED (...)   exit 0 / 1  (usage error: 2)
env: MADO_VERIFY_ROOT (config root), MADO_VERIFY_LIVE=auto|yes|no
exit=2
```

```
$ d=$(mktemp -d /tmp/vg309-root.XXXXXX); timeout 600 prlimit --as=4000000000 -- \
    bash tools/mado-verify.sh --no-live --root "$d"
...
gate      boundary.readonly               SKIP    no /tmp/vg309-root.JKMuHV/.config tree to hash
counts: pass=1 fail=14 unknown=7 skip=12 note=6
MADO_VERIFY: DIVERGED (14 fail, 7 unknown, 1 pass) — first fail: hypr.file.root (missing: /tmp/vg309-root.JKMuHV/.config/hypr/hyprland.conf)
exit=1
```

(Temp root removed: `rm -rf /tmp/vg309-root.JKMuHV`.)

## What the run shows

- **The capability works at `41cc04c8`**: exit 0, `MADO_VERIFY: CLEAN (53 pass, 7 notes; file + live planes verified
  read-only)`. The live layer was actually exercised, not skipped: `hyprctl: yes`, 4 Hyprland instances visible (other
  fleet seats' nested instances; the gate targets the session's own signature "no guessing"), and every `hypr-live.*`
  row (version pin `0.56.2`/`efb5099…`, configerrors empty, `binds_count` 192, monitor DP-1, waybar layer/pid, walker
  services, GDK_SCALE/NVD_BACKEND) returned PASS. The read-only boundary check ran and held: `gate boundary.readonly
  PASS config plane byte-identical before/after (combined sha ddb0780742f8…)`.
- **Exit map 0/1/2 confirmed** by the three runs above (0 live CLEAN, 1 DIVERGED on an empty root, 2 usage error).
- **The row's quoted numbers are round-12's, and they still reconcile.** The committed receipt
  (`.ufo/evidence/round-12/gate-live-after.txt`) is `pass=52 fail=0 unknown=0 skip=0 note=8`, `exit=0`. Today's run
  prints the same 60 row sites; an exact per-row diff shows exactly one status change:
  `live.consumer.hypridle NOTE → PASS` (round 12: "hypridle absent"; now: "hypridle running"). Hence 53/7. The other
  differences are same-status detail drift caused by today's session: `13/13` vs `12/12` local confs, `4 instances`
  vs `1 instance`, walker `2.17.2` vs `2.17.0`, waybar pid 1664 vs 1724, boundary digest, and tightened check wording
  (`set exact`/`member set exact`, git rows "at refs/heads/master"). No later gate logic regressed. Note the run reads
  today's live `$HOME` plane by design; the clone supplies only the gate bytes, not the substrate.
- **The demonstration command was runnable exactly as written** (bare live run); no nearest-form substitution was
  needed.

## Superseding / contradicting text in SCORECARD.md at `41cc04c8`

- **Superseded (current status), not contradicted:** line 1576, the round-24 re-demonstration table
  (`### Capability status (round 24 re-demonstration)`): `| verdict gate (live + file plane) | works | \`--no-live\`
  prints a \`MADO_VERIFY:\` verdict, exit 0 at \`8e5d9369\`; live layer not exercised |`. The table's preamble
  (lines 1568–1571) states it "supersedes the implied `works` of every earlier row; the earlier rows stay as written".
  That round-24 row deliberately exercised only the file plane; my run at `41cc04c8` exercises both planes, so the
  round-24 limitation does not hold at this base.
- **Same capability, file-plane-only readings:** line 122 (round-12 six-axis baseline, freshness):
  `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)`, exit 0; line 287 (round-12
  C2 freshness) scores `--no-live`; line 400 (planned round 13) and lines 533/653 (round 13/14) also record only
  `--no-live` runs (29 PASS). These are narrower readings of the gate, not contradictions of the live arm.
- **Historic live divergence, earlier and superseded:** line 30, "Live caveat at close. The live plane reads DIVERGED
  while waybar is absent …" — a round-11-era session-state caveat (operator-owned bar crash), before the round-12 live
  CLEAN that row 309 cites. No later row reports the live plane failing.
- **Named gate defect, routed and fixed:** line 954 (round-18 C1) carries `JjAuditMado F10` — "`tools/mado-verify.sh:3406`
  digests a failed `git show` as the empty-input sha and reports a local edit". At `41cc04c8` that pointer no longer
  resolves to the named code: line 3406 is now the UNKNOWN row inside `live_plane()`
  (`row hypr-live live.plane UNKNOWN "$reason; live checks unverified — verdict cannot be CLEAN"`). The defect itself is
  fixed in the base gate and guarded by self-test scenario OM9 (`tools/mado-verify.sh:872-884`: "a FAILING git show
  reads UNKNOWN, never a 'local edit'"). This is a stale line pointer in SCORECARD prose, not a contradiction of row
  309's capability.
- **Gate bytes pin matches base:** `SCORECARD.md:1221-1222` records the final gate as `050efc72…`, 4,194 L,
  selftest 460/460; the base blob is exactly that sha and length.
- **No later row under a `Capabilities` heading re-lists the gate.** The only later row naming the capability is the
  round-24 status row at line 1576 (cited above). Greps for `verdict gate`, `MADO_VERIFY`, `mado-verify`, `| gate`,
  `live plane`, `live layer`, `DIVERGED` over the whole file return only the lines cited above plus unrelated
  tripwire/classifier/frozen-runner rows and round-1..11 move-log rows.

## Ledger line

```
| SCORECARD.md:309 | verdict gate (live + file plane) | Read-only verdict over the declared config plane and live hyprctl surfaces, exit 0/1/2, boundary check | observed at 41cc04c8: works — exit 0, `MADO_VERIFY: CLEAN (53 pass, 7 notes; file + live planes verified read-only)`, `gate boundary.readonly` PASS (config plane byte-identical); exit 2 on a usage error and exit 1 on an empty root also observed | `timeout 600 prlimit --as=4000000000 -- bash tools/mado-verify.sh` (cwd = clone at 41cc04c8) | SCORECARD.md:1576 (round-24 status: works, `--no-live` only, live layer not exercised) |
```

## Risks, caveats, host safety

- The live arm is session-dependent. Today's gate saw 4 Hyprland instances (fleet seats' nested oracles) and still
  reported `live.hypr.instances PASS … targeting the session's own signature (no guessing)`; a future run with an
  ambiguous signature would read UNKNOWN and block CLEAN, by design. The row's numeric sample (52/8) is reproducible
  only in the round-12 receipt; at base the mechanism reproduces, the counts moved by one row (hypridle).
- Live verbs issued by the gate, disclosed because they exceed the four verbs enumerated in my seat bounds: `hyprctl
  version`, `hyprctl -j instances`, `hyprctl configerrors`, `hyprctl -j getoption` (general:gaps_out, input:kb_layout,
  general:border_size, decoration:rounding, animations:enabled, input:touchpad:scroll_factor), `hyprctl -j binds`,
  `hyprctl -j monitors`, `hyprctl -j layers`; plus read-only host reads (`systemctl --user is-active` ×2,
  `pgrep -x hypridle`, `pgrep -x waybar`, `omarchy version`, `omarchy --json --all`, `readlink`, `sha256sum`, and git
  read verbs `symbolic-ref`/`rev-parse`/`describe`/`for-each-ref`/`show` against the `~/.local/share/omarchy`
  checkout). **No compositor write verb** (no dispatch, keyword, reload, kill, batch), **no git write**, **no nested
  compositor started by me**, **no package or config change**. This is the row's own documented read-only command;
  its self-check confirmed the config plane was byte-identical before/after.
- One measurement run of the demonstration command at base (not a sweep); the two probe runs are labelled
  supplementary. Clone `git status --porcelain` after all runs: 0 lines (no tree writes).
- Cleanup: clone deleted (`rm -rf /fast/scratch/hyaku/mado-r25a3/c2/CapVerdictGateLiveFilePlane309`, path verified
  absent); the `mktemp` root under `/tmp` removed (no `/tmp/vg309-root.*` remains); no process from this seat survived
  (`pgrep -af CapVerdictGateLiveFilePlane309` → empty, rc=1; the `mado-verify`-matching processes still on the host are
  other seats' tameshi mutation harnesses under `/tmp/tameshi-r4-2-regression.*`, not mine). Scratch receipts kept
  outside the lane only: `/tmp/vg309-live.txt` (this run's stdout, 66 lines, byte-identical to the block above) and
  `/tmp/sc41.md` (base SCORECARD extract). No lane file was written except this report.
