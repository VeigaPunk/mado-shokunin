# mado-shokunin — Scorecard

Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
Axes will be pinned with their counting commands as rounds land.

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 1 | coverage | seed at `74d3b7b`: `corpus/knowledge/` did not exist (0 files), coverage map 0 rows, SKILL.md cited 0 sources | 3 notes — `hyprland-config-plane.md` (217 L), `terminals-and-omarchy.md` (179 L), `waybar-walker-plane.md` (364 L), all `wc -l` — covering every PROVINCE-declared surface group: hypr plane incl. the separate consumers (hypridle/hyprlock/hyprsunset/xdph), waybar/walker/mako/swayosd, all four terminals + theme plane + omarchy skill anatomy; per-surface sweep: 12/12 PROVINCE keywords hit ≥1 note | `git ls-tree 74d3b7b corpus/knowledge/ \| wc -l` → 0; `git show 74d3b7b:corpus/README.md \| grep -cE '^\| '` → 1 (header row only); `wc -l corpus/knowledge/*.md` → 217 / 179 / 364; sweep `grep -il <kw> corpus/knowledge/*.md` for config/hypr, waybar, walker, alacritty, foot, kitty, ghostty, theme, wallpaper, hypridle, hyprlock, hyprsunset → each ≥1 note. Re-run 2026-10-14 (MADO-SCRIBE) |
| 1 | operability | seed SKILL.md: 22 L, 0 tables, 0 commands, 0 probes ("sections will land" placeholder) | SKILL.md 186 L: who-owns-it table 19 rows, read-only probe table 15 rows (each a command + observed sample; caption: executed 2026-10-14), omarchy-boundary routing table 5 rows, 6 mutating commands fenced operator-only; probe tools exist: 10/10 spot-checked names resolve on PATH. Named ceiling: 0 committed verdict gates — `find corpus -name '*.sh'` → 0, no `corpus/scripts/`; probes are prose + sample output, not re-runnable verdicts (round-2/3 work) | `git show 74d3b7b:SKILL.md \| wc -l` → 22; same `\| grep -cE '^\| '` → 0; `wc -l SKILL.md` → 186; per-section awk counts of `^\|` lines → 21/17/7 table lines = 19/15/5 data rows (minus header+separator); `command -v hyprctl omarchy makoctl busctl grim slurp hyprpicker systemctl pgrep jq` → 10/10 found. Re-run 2026-10-14 (MADO-SCRIBE) |
| 2 | depth | round-1 corpus at `65a2254`: file-byte evidence only — 0 claim→live pairs; the declared config plane had no live confirmation (round-1 named ceiling: "probes are prose + sample output, not re-runnable verdicts") | live-verification layer: `hyprctl-verification-layer.md` (MADO-R2-1, 280 L by `wc -l`) maps **56 `getoption` claim→live pairs (39+15+2) + 9 non-getoption pairs**, each classed in a falsifiable divergence vocabulary (`agreement`/`agreement*`/`live-default`/`mismatch`/`config-only`); census 52 agreement (6 `agreement*` = shadowed-declarer ownership proofs: toggle owns gaps/border/rounding, local owns `kb_layout`, theme owns borders), 4 `live-default`, **0 `mismatch`**; `keybind-rule-semantics.md` (MADO-R2-2, self-label MADO-4, 315 L by `wc -l`) reconciles **192/192 declared binds** against live `hyprctl binds -j` incl. flag counters and a 13-mask modmask histogram, 24-dispatcher inventory (semantics `[INF-docs]`, nothing fired), 1 live divergence finding (Alacritty `default-opacity*` tags) + 1 new drift finding (orphan `envs.conf`); freshness: round-1 notes re-measured (10 R2-E items, 1 real corrigendum mako 50→119 B); SKILL.md gains claim→evidence routing (4-row table) + 6 mutation-free safety rules | `wc -l corpus/knowledge/hyprctl-verification-layer.md corpus/knowledge/keybind-rule-semantics.md` → 280 / 315 (editor views 281/316, no trailing newline); awk data-row counts → §3 = 39+15+2 = 56, §4 = 9, §5 = 6, dispatcher table = 24; class census re-run → 51 `agreement` + 6 `agreement*` + 5 `live-default` over §3+§4 classed rows (§3-only: 52 incl. 6 starred + 4 live-default), 0 `mismatch`; live re-run: `hyprctl binds -j \| jq length` → 192, flag counters locked 26 / repeat 14 / release 1 / mouse 2 / has_description 190, `hyprctl configerrors` → empty rc=0, `hyprctl version` → 0.56.2 `efb5099…`; getoption spot-checks `general:gaps_in` → `custom: 0 0 0 0`, `input:kb_layout` → `br`, `input:touchpad:scroll_factor` → `float: 0.400000`, `dwindle:preserve_split` → `int: 1`; freshness `sha256sum ~/.config/hypr/hyprland.conf \| cut -c1-12` → `4f52854a3c14` = MADO-1 §2 = MADO-R2-1 §7, `printenv GDK_SCALE` → `1`, `NVD_BACKEND` → unset; `git show 65a2254:SKILL.md \| wc -l` → 186 → `wc -l SKILL.md` → 240, round-2 section = header + 4 routing rows; `grep -c '^\- \*\*R2-E'` → 4 / 2 / 4 across the three round-1 notes. Re-run 2026-10-14 (MADO-SCR) |
| 3 | depth | round-2 corpus at `e1e1bb7`: the waybar/walker plane had file-byte evidence only (round-1 note: inventory, drift diff, decision table; no module-by-module semantics, no bar-side live pair — round-2's live layer covered hyprctl surfaces only; the round-3 anti-claim branch — waybar introspection unavailable — was named in the plan) | semantics layer: `waybar-walker-semantics.md` (MADO-R3-1, 455 L by `wc -l`) — 13 tables / **89 data rows** incl. **19 module rows** (§3.1 2 + §3.2 8 + §3.3 9, each Displays/Source/Actions/Fails/Live), introspection ledgers §2.3/§6.8 (no IPC verb in waybar 0.15.0 → anti-claim branch applied, labeled), signal bus §4 (5 producers; RTMIN offset delivery measured: caught=45, procps-ng 4.0.7), style map §5 (14 rows; theme owns fg/bg only), walker key-by-key §6.2 (14 rows vs the 298-L packaged table) + `[columns]` correction §6.3, failure modes §7 (7 rows), 7 divergence candidates §8, boundary proof §10 (4 sha256 before/after equal, no network command run) | `wc -l corpus/knowledge/waybar-walker-semantics.md` → 455; `grep -c '^|'` → 115 = 13 headers + 13 separators + 89 data rows; per-section awk → §1 4, §2.1 8, §2.3 7, §3.1 2, §3.2 8, §3.3 9, §4 5, §5 14, §6.1 3, §6.2 14, §6.8 4, §7 7, §10 4 (first awk cut double-counted — halved, totals close 89); live re-runs: `waybar --version` → v0.15.0, `walker --version` → 2.17.0, `hyprctl -j layers` → level 2 `waybar` pid 1707 (level 0 `wallpaper` 1710), `busctl --user get-property fr.arouillard.waybar /StatusNotifierWatcher …RegisteredStatusNotifierItems` → `as 0`, `makoctl mode` → `default`, PIDs 1707/1808, `/sys/class/power_supply/` → 0 entries. Re-run 2026-10-14 15:38–15:47 UTC (MADO-B4, raw log `/tmp/mado-b4-r3b/verify.log`) |
| 3 | coverage | round-2 corpus at `e1e1bb7`: no full-plane re-verification existed (round-2 layer untested against drift), no severity-classed divergence register, no end-to-end domain task, no no-oral-context executor test; `git show e1e1bb7:corpus/README.md \| grep -c knowledge/` → 5 rows | e2e health pass + executor gate: `config-health-report-r3.md` (MADO-R3-2, 550 L) re-checks **20 round-1/2 claim families** (§1, all stand), zero config drift by sha256, **57/57 `getoption` 0 mismatch** (Appendix A census 46 `agreement` + 6 `agreement*` + 4 `live-default` + 1 extra), binds/flags/histogram/dispatchers/rules all equal; divergence register F1–F10 = 1×S1 + 2×S2 + 7×S3 (§0's summary says "6×" — off by one, scribe obs (a)), each with an operator recommendation; `executor-test-sufficiency.md` (MADO-R3-4, 196 L): SKILL-only executor pass, verdict **"Sufficient, end-to-end, against the version read"** — the no-oral-context SHONEN gate; round commit freezes SKILL sha `ef4c29e3…` (396 L) per the note's request | `grep -c '^### F'` → 10; `grep '^### F' … \| grep -c '(S3'` → 7 (S1/S2 by header tally → 1/2); Appendix A `\| (agreement\*?\|live-default\|extra …) \| uniq -c` → 46/6/4/1; coverage rows `awk '/^## 1\./,/^## 2\./' \| grep -c '^\| '` → 21 (header + 20); live: `hyprctl -j binds \| jq length` → 192, `hyprctl -j getoption general:gaps_out` → `{"custom":"0 0 0 0","set":true}` (the executor's claim row re-run independently), `sha256sum ~/.config/hypr/hyprland.conf \| cut -c1-16` → `4f52854a3c143dcf`, `pgrep -x hypridle` → rc=1 (F1), clients tags reproduce F2 (3982970/1784450 flagged, 275049 clean), `hyprctl -j instances \| jq -c '.[0].wl_socket'` → `"wayland-1"` (F8), `printenv NVD_BACKEND` → rc=1 (F3), omarchy two-pin re-measured 3.8.3 vs v3.8.4; `sha256sum SKILL.md` → `ef4c29e3…`, `git diff --stat HEAD -- SKILL.md` → +240/−83. Re-run 2026-10-14 15:38–15:47 UTC (MADO-B4, raw log `/tmp/mado-b4-r3b/verify.log`) |
| 4 | calibration | after round 3: SHONEN 2/4 — `[x]` SKILL tables + no-oral-context (MADO-R3-4); `[~]` e2e task + PROVINCE accuracy, both lane-asserted, no non-author verdict in-repo | named non-author verdicts land: VER-M3 — REPRODUCES (final §7.3) → box 2 `[x]`; VER-M4 — 15/15 province claims reproduce, no cross-domain bleed, box 4 OPEN one erratum wide (falsified self-audit count-convention line; close = append E1) → `[~]`/`[x]` per E1; round-3 pass now has an executable reviewer pack (MADO-R4-1 + corrected runner) + a fixed-run re-run | `wc -l /tmp/mado-r4-1-probe/repro-r3.sh` → 389; pack sha `70dff755278d…`, corrected runner sha `389a1bb7…`; fixed run → `checked 57; mismatches/missing: 0`; VER-M3 verdict sha256 `31d40550c8dee977…`; VER-M4 verdict sha256 `0f8c944713893b56…`; applied from r4 draft §4c at the close (SCR-M11, 2026-10-14; /tmp receipts ephemeral — [OBS-record]) |
| 4 | depth | round-3 corpus: the idle/lock surface held only scattered file-byte mentions (MADO-1 §8/§10, MADO-2 §5; hypridle absent, cause `[UNK]`) | `idle-lock-plane.md` (MADO-R4-2, 355 L by `wc -l` → 381 after ERR-M E2): 4 tables / 31 data rows (§2 3 configs; §2b 11 actuators; §5 10 chain steps; §6 7 options); provenance by sha256 identity; declared chain incl. script-defined lock/wake side-effects; runtime snapshot + live-idle UNKNOWN; mid-round session restart recorded (autostart start 16:11:08Z; silent exit ≤16:23:20Z) | `grep -c '^|'` → 39 = 4×(header+separator)+31; `sha256sum ~/.config/hypr/hypridle.conf` → `e7d3b8dd…` = shipped payload; journal quotes for the autostart start; `wc -l` → 355 → 381; note re-measured at apply 2026-10-14: 381 L / `a0597be96c10…` ✓ |
| 4 | freshness | pending errata carried since rounds 2–3 (R3-1 §8 ×7 on the waybar note; F8/envs closure; R3-2 §0 tally 6×→7×; SKILL typo already fixed) | ERR-M sweep applied all as append-only blocks in 5 files (list in LOG entry), each re-measured read-only 16:20–16:25Z; new owed errata identified by the verifier seats: note §2.3 dispatcher-tail prose, runner V2/V3 receipts, self-audit E1 | `git diff --stat` (5 files, +192/−9 at 16:27Z); per-file `wc -l` 587/302/474/462/381; `grep -c 'Errata (round 4)' corpus/knowledge/*.md` → one per touched file (re-measured at apply 2026-10-14: blocks persist in the 5 files; later notes quote them) |
| 5 | calibration | box 4 `[~]` since round 3; round-4 LOG left it open ("§8 re-run needed per the named verifier"); self-audit §7 names the closure procedure (`[x] <verifier-id>` in SHONEN.md) | box 4 `[x]` VER-M4B: all 25 §8 rows re-derived, durable pins byte-equal, 4 cross-class spot-checks, moved values cause-named, v4 addendum a byte-prefix append (no claim text changed) | verdict `/tmp/w5-ver-m4b-work/VERDICT.md` sha256 `f70fc3c70a11e91e…` (ephemeral); durable receipt `corpus/knowledge/province-accuracy-selfaudit.md` round-5 addendum 345 L sha `7c0a58208dea60e8…`; `head -c 17856` = `3014a84060c95710…`; spot-checks: `hyprland.conf` 1,273 B/29 L/`4f52854a3c143dcf`, `hyprctl version` 0.56.2 `efb5099…`, `binds` 192, declared-tree `find` 0; pins re-measured at apply 2026-10-14 (345 L / `7c0a58208dea60e8…`, head-prefix ✓) |
| 5 | operability | round-1 ceiling still standing after 4 rounds: `find corpus -name '*.sh'` → 0, no `corpus/scripts/`, no committed verdict gate | round-1 ceiling retired: `tools/mado-verify.sh` ships — declared planes vs live bytes + hyprctl read verbs, exit map 0/1/2, hermetic `--selftest`, read-only boundary check; green at landing: selftest 28/28 assertions + `MADO_VERIFY: CLEAN (35 pass, 4 notes)`; at the arc's close (applied 2026-10-14): `93e43f8f…` 3,231 L, selftest 268/268, live point sample DIVERGED (3 waybar fails — session state; row 11 carries it) | `wc -l tools/mado-verify.sh` → 1,098; sha `d7edaab4bf108625…`; selftest transcript `/tmp/w5-scr-m5/gate-selftest3.log` (ephemeral); live transcript `gate-live2.log`; mid-round red history: `MADO_SELFTEST: FAILED — 19 passed, 9 failed` at `5811b5f6…` (recorded, not smoothed); ladder r5 → r9 re-derived at the close (SCR-M11): `d7edaab4…` 1,098 L → `93e43f8f…` 3,231 L, selftest 28 → 268 (AUD-M10 C1 re-runs) |
| 6 | operability | round-5 gate selftest-green but never mutation-tested (a broken gate would block all widening) | gate proven to fail then hardened: selftest 28 → 53; the hardened gate (`c4c1afb7…`, 1,186 L) kills 10/10 of tameshi's mutants with `MUTATE_RESTORE: OK`; `gate-mutation-proof.md` + the omarchy drift watch (`omarchy-drift-watch.md`) + the remaining-planes census (`remaining-planes-census.md`) land | ladder cell re-derived (SCR-M11: `git show c8f6667:tools/mado-verify.sh` → `c4c1afb75dd1c8aa…`, 1,186 L / 50,126 B; selftest 53/53 re-run — AUD-M10 C1); 10/10 table + restore per `gate-mutation-proof.md`; wave-6 32-lane (2 rerouted alibaba→hyper) |
| 7 | operability + coverage | round-6 gate: provably falsifiable but its proof was a one-shot run (no re-runnable regression); theme/wallpaper and walker live-surface observed as notes only | gate `--regression` mode shipped (`90d50cdd…`, 1,755 L, selftest 89): replays the round-6 mutation case against the gate's recorded revision (excised-target sha proven identical), tameshi spec pinned `c7ee75b9…`; notes `theme-wallpaper-plane.md` + `walker-live-surface.md` land | ladder cell re-derived (SCR-M11: `git show 0c20a76:…` → `90d50cdd4d18410b…`, 1,755 L / 75,771 B; selftest 89/89 re-run — AUD-M10 C1); LOG `:297` (M7-1: `MADO_REGRESSION: PASS` 10/10 under harness `cf41efaa…`); wave-7 32-lane (3 rerouted alibaba→hyper) |
| 8 | operability + freshness | round-7 gate: post-hardening expectations held by the round's own runs only — no independent sweep against the 10/10 expectation; drift watch ad-hoc | post-hardening sweep re-ran the expectations (`gate-mutation-sweep-r8.md`, the 10-defect table D1–D9 + R1); the drift-watch arm + the snapshot-diff mode ship into the gate (`7da4ec50…`, 2,887 L, selftest 217) | ladder cell re-derived (SCR-M11: `git show 12c8f08:…` → `7da4ec5013583c91…`, 2,887 L / 131,612 B; selftest 217/217 re-run — AUD-M10 C1); wave-8 32-lane (2 rerouted alibaba→hyper) |
| 9 | coverage + operability | round-8 gate: the `theme` plane was 0 row sites (measured notes only); the walker live surface unrowed — carried from round 7 | `theme` plane as gate arms: 10 file rows / scenarios T1–T9, 27 row sites, the two live rows exempted by name; `walker-deep-r9.md` (398 L / `a5acfe0162c9e5cd…`); the snapshot-diff mode's first real receipt (`MADO_DIFF: CHANGED (rows 31→41; appeared=10)`; `snapshot-diff-receipt-r9.md`, 196 L); gate `93e43f8f…` (3,231 L, selftest 268) | ladder cell re-derived (SCR-M11: `git show de22dfd:…` → `93e43f8f…`, 3,231 L / 150,103 B; selftest 268/268 re-run — AUD-M10 C1 + SCR-M11 21:33Z); AUD-M9: C1 PASS, C1b NOT LANDED (walker live rows), C4 theme-mutant gap named; wave-9 32-lane (2 rerouted alibaba→hyper) |
| 10 | calibration + operability | round-9 state: no arc synthesis existed; the gate's limits lived across nine records; README/SCORECARD/lessons debt rounds deep | the ten-round synthesis (`arc-synthesis.md`, M10-1, 387 L / `a5b4833141461810…`: arc ledger, ladder re-derived 28→268, invariants, the three trends, gap ledger of 12 surfaces, classification 9 closed / 8 operator-owned / 12 unknown) + the gate's standing-use note (`gate-standing-use.md`, M10-2 + M10-3's cadence tick, 361 L / `aaa2e625253e881e…`: custody, invocation map, verdict vocabulary, cadence, residual ledger) | VER-M10: ladder cell-for-cell CONFIRMED (five revisions re-run 28/53/89/217/268, all rc 0); AUD-M10: C1–C4 + N1/N2 PASS, live point sample DIVERGED (F2 — waybar absent, session state), F1 name-rename / F3 harness moved / F4 env-arm nuance named; landed `f7bfc9f` (SKILL +89/−1 by numstat); wave-10 32-lane (1 rerouted alibaba→hyper) |
| 11 | calibration + freshness — THE FINAL ROW: the arc closes | round-10 state: the arc's terminal artifacts (synthesis, standing-use note) landed; every open item and the record debt awaited terminal disposition; no closeout existed | THE CLOSEOUT: `corpus/knowledge/closeout-r11.md` (M11-1 §1–§7 + M11-3's §8 append; 294 L by `wc -l` / 19,250 B / `670b5a396ecb8789…`; landed name — the plan's `arc-closeout.md` never landed, both values carried): handoff verified ((a10)/(b10) yes; (c10) partly), ladder + battery receipts, terminal disposition ledger (closed / operator-owned / unknown — no "carried"), freeze pins + handoff; first lessons entry `corpus/lessons/round-10.md` (M11-2; 226 L / `d7b4708e864fca29…` — `corpus/lessons/` 0 → 1 after ten rounds, non-author spot-check SC-A); `plans/completion-evidence.md` (PACK-M, 196 L); SKILL closed by M11-4's pointer append (1,424 → 1,545 L / `b9134091c031fade…`). Freeze pins: gate `93e43f8f…` (3,231 L / 150,103 B — unchanged rounds 9→11), synthesis `a5b4833141461810…`, standing-use note `aaa2e625253e881e…`, closeout `670b5a396ecb8789…` | SCR-M11 re-verification at the frozen revision (2026-10-14 21:33–21:35Z, logs `/tmp/w11-scr-m11/`): ladder re-derived 5/5 + the two identity rows; selftest 268/268 rc 0; `--no-live` CLEAN (29 pass, 4 notes); live DIVERGED (3 fail — waybar core-dumped 21:21:17Z per VER-M11 F0; 49 pass, 8 notes); `--regression` PASS (target `dc7c4141…`, spec `c7ee75b9…`, 10/10, flips 0, restore OK); snapshot pair `MADO_DIFF: SAME` (41→41); boundary `bb2639d9a980…` before/after; AUD-M11 C1/C2 + R1–R7 PASS (F1–F4 named) · VER-M11 ladder 20/20 + r10 4/4, F0/F4 named; wave-11 32-lane |

**Arc end.** The arc is closed. The gate is handed over at the frozen revision `93e43f8fe8b9bdd4…` (3,231 L / 150,103 B): the standing verdict is `bash tools/mado-verify.sh` (live, read-only; contract, invocation map, cadence and residual ledger in `corpus/knowledge/gate-standing-use.md`); the ten-round synthesis is `corpus/knowledge/arc-synthesis.md`; the closeout is `corpus/knowledge/closeout-r11.md`. No further round opens. Probation 4/4 `[x]` since round 5 (`SHONEN.md`); promotion is the operator/integrator decision, never self-declared. Applied at this close (SCR-M11): rows 4–5 from the drafts' ready text (pins re-measured 2026-10-14); rows 6–9 completed from the records + re-derived ladder cells (the r6–r9 §4c texts are ⟨fill⟩ templates, not ready text — finding recorded in LOG round 11); row 10 completed; row 11 added. Debt measured at this write: README 8 rows (notes unrowed), the synthesis epilogue, the standing-use revision line, the draft ⟨PENDING⟩ closures, walker-deep §10/§11 errata and the AGENTS pointer were not yet on disk — the settlement (M11-2) remains the named carrier; the round-11 commit is the remaining landing step.

**Live caveat at close.** The live plane reads DIVERGED while waybar is absent: VER-M11's journal receipt shows `systemd-coredump` — waybar (pid 3036215) dumped core at 21:21:17Z; cause `[UNK]`; no mado lane touched it; the bar's restart is operator-owned. The file plane is CLEAN and the config bytes are unchanged (boundary `bb2639d9a980…` green in every run).

## Fleet round 1 — coverage navigation (2026-10-15)

The explicit fleet-round-1 steer opens a new run after the historical arc
above; it does not renumber or rewrite that arc. Its inherited scorecard
had a move log but no numeric axis rows. The following bounded sub-axis
rubrics establish the starting comparison; they are not domain-mastery
scores, promotion verdicts, or evidence that the desktop is healthy.
The historical 4/4 `[x]` at arc close is not current promotion clearance:
`SHONEN.md` now retains four `[~]` assertions because outside-lane
independence is not established. This round's L2s are still the mado
authoring lane; none can supply that missing promotion authority.

| Axis / scored sub-axis | Starting score (0–10) | Counting rule and observed result | Measured commit | Last-change round |
|---|---|---|---|---|
| coverage / admitted-note reachability | 3.6364 | `10 × uniquely indexed existing knowledge notes / existing knowledge notes`; counting command below: 8/22, missing 14, dangling 0, duplicates 0 | `bb08dd57f4b48bfb001a178e57b9c25e7040447f` | fleet 1 initialization |
| operability / existing hermetic suite pass fraction | 10.0000 | `10 × passed assertions / total assertions` from `bash tools/mado-verify.sh --selftest`: `MADO_SELFTEST: 268/268 assertions passed`, exit 0; gate unchanged at measurement | `bb08dd57f4b48bfb001a178e57b9c25e7040447f` | fleet 1 initialization |

**Selection:** coverage is lower under these explicit local rubrics.
Assertion success is not a complete operability assessment; live behavior,
rendered UI, idle transitions and external verification remain unscored.
Completing navigation can reach 10 on this finite corpus without saturating
the province's broader coverage axis.

**Planned:** complete the admitted-note routes and add per-PROVINCE
navigation, keeping each source's date, errata and unknowns in force.
No new knowledge admission, gate widening, source-tree write or compositor
mutation is part of this move.

**Retired:** none. The scoring split makes the measured subset explicit;
broader coverage and operability remain open, not silently retired.

### Counting command

Run from this lane repo with `REV` set to the commit being measured. Exit 1
means missing, dangling or duplicate note rows; exit 0 means complete.
This counts navigation, not the truth or freshness of a note's claims.

```bash
REV=bb08dd57f4b48bfb001a178e57b9c25e7040447f python3 - <<'PY'
import os, re, subprocess
from collections import Counter
rev = os.environ["REV"]
def git(*args):
    return subprocess.check_output(["git", *args], text=True)
notes = {p for p in git("ls-tree", "--name-only", rev + ":corpus/knowledge").splitlines() if p.endswith(".md")}
index = git("show", rev + ":corpus/README.md")
rows = re.findall(r"^\| `knowledge/([^`]+\.md)`", index, re.M)
counts = Counter(rows)
missing = sorted(notes - counts.keys())
dangling = sorted(counts.keys() - notes)
duplicates = sorted(p for p, n in counts.items() if n != 1)
covered = sum(counts[p] == 1 for p in notes)
print(f"revision={rev} indexed={covered}/{len(notes)} missing={len(missing)} dangling={len(dangling)} duplicates={len(duplicates)} coverage={10*covered/len(notes):.4f}/10")
for kind, paths in (("missing", missing), ("dangling", dangling), ("duplicate", duplicates)):
    for path in paths:
        print(f"{kind}: knowledge/{path}")
raise SystemExit(1 if missing or dangling or duplicates else 0)
PY
```

## Fleet round 1 — interactive cutover, blocked before dispatch

**Status: LIVE, blocked and unadmitted; no new verified completed round.**
This continues the interrupted fleet round 1 rather than opening round 2.
The historical eleven-round arc is preserved; its launch numbering is not
a verified-round counter for this relaunched run.

Lowest LIVE measured sub-axis remains coverage / admitted-note reachability.
The candidate index now routes 22/22 existing notes; that finite denominator
does not retire broader coverage. The baseline was re-measured at
`bb08dd57f4b48bfb001a178e57b9c25e7040447f`: 8/22, missing 14,
dangling 0, duplicates 0, exit 1. Full output:
`.ufo/evidence/fleet-round-1/navigation-baseline.txt`.

Candidate-worktree smoke:
`.ufo/evidence/fleet-round-1/navigation-smoke.json` records 22/22,
missing/dangling/duplicate 0, seven province routes and 54 local Markdown
links with zero unresolved/outside-lane targets. The representative
SKILL → index → idle/lock note route preserves declaration versus observed
timing, the process/unit distinction, E2 turnover and UNKNOWN transitions.
This is navigation evidence, not a 32-scope semantic audit or live-health
measurement. The existing commit-based counting command above also measures
the delivered index; the committed-revision result is recorded separately
after the candidate content commit.

| Axis | Candidate verdict | Observable and limit |
|---|---|---|
| coverage | improved | Exact-target navigation 8/22 → 22/22; bounded scores 3.6364 → 10.0000. No new behavioral coverage or province saturation. |
| depth | unchanged | No new domain-knowledge entry or technical-depth claim admitted. |
| operability | unchanged | Existing gate remains SHA-256 `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`; `MADO_SELFTEST: 268/268 assertions passed`, exit 0. |
| freshness | unchanged | `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)`, exit 0; counts `pass=29 fail=0 unknown=0 skip=8 note=4`. Historical live claims are not refreshed. |
| calibration | unprovable-but-better | Candidate/admission, historical/current and assertion/independent-review distinctions are explicit; the outside-lane admit/reject spot-check is still absent. |
| adjacency | unchanged | PROVINCE and all substrate/sibling ownership remain unchanged; no outside defect absorbed. |

Full gate outputs and exit codes:
`.ufo/evidence/fleet-round-1/{selftest.txt,file-plane.txt,gates.json}`.
No axis is locally observed harmed, but this vector does **not** admit a
round whose required dispatch and outside spot-check are missing.

Learning trends: **expansion unchanged** (no new ground admitted);
**quality unchanged** (domain evidence retains dates/errata/unknowns);
**discernment unprovable-but-better** (explicit rejects and boundaries,
without an outside-lane admit/reject agreement sample).

Exactly 32 distinct proposed scopes passed canonical
`ufo-swarm-wave.mjs plan`, exit 0, `spawn=32 resume=0 total=32`.
This session made zero native task calls and started zero specialists.
Global role bindings and the connector fallback do not realize the
operator contract; exact missing bindings and owner action:
`.ufo/blocked/fleet-round-1-routing.json`.

**Planned:** operator/global authority owner supplies the requested
role-to-alias bindings and connector fallback, or explicitly revises that
contract. A fresh authorized interactive session resumes this same LIVE
round, performs its complete validated native batch, obtains the outside
admit/reject spot-check and re-measures before admission. No in-session
round loop and no push. **Retired:** none.

The operator's at-least-100 verified-round target remains outstanding:
this blocked partial round adds **0**. One blocked attempt is recorded here;
no three-consecutive-blocked stop or sound saturation is inferred.

Receipt/continuation debt is separate from local gate success:
`.ufo/blocked/fleet-round-1-receipt-binding.json` records the selected
direct-launch metadata and missing applicable expected receipt bag.
The owning integrator must supply that binding; no task key or unrelated
config digest is invented. No receipt was minted and Sighting completion
was not called. The complete canonical rendered payload is retained only
as `dispatch-preview.json` beside the validated plan; it is not dispatch
evidence and carries no recorded native agent handles.

### Committed candidate measurement

Content commit: `7cd7f331ae151845ebff7bd100c1073ebad49351`, authored
as `mado-shokunin <mado@shokunin.local>`. Running the Counting command
above with `REV=7cd7f331ae151845ebff7bd100c1073ebad49351` produced:

```text
revision=7cd7f331ae151845ebff7bd100c1073ebad49351 indexed=22/22 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
```

Full retained output:
`.ufo/evidence/fleet-round-1/navigation-committed.txt`.
The measured coverage-navigation score is 10.0000/10 at that commit,
versus 3.6364/10 at the baseline; the round is still LIVE/blocked,
not admitted or saturated. `SCORECARD.md`'s candidate verdict vector and
learning-trend limits above remain in force.
