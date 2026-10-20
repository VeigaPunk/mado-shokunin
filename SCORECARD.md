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

Run from this lane repo with `REV` exported (baseline default). Exit 1
means missing, dangling or duplicate note rows; exit 0 means complete.
This counts navigation, not the truth or freshness of a note's claims.

```bash
REV="${REV:-bb08dd57f4b48bfb001a178e57b9c25e7040447f}" python3 - <<'PY'
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

### Reproducibility erratum — literal shell wrapper

The original Counting-command wrapper hardcoded the baseline REV despite
the caller-selection guidance. Earlier measurements selected REV for the
Python body; they did not establish that the published shell block honored
the caller. The wrapper now uses `${REV:-bb08dd57f4b48bfb001a178e57b9c25e7040447f}`;
export REV before copying the complete block to select another commit.

The corrected literal block, including its wrapper and heredoc, was supplied
unchanged to `bash -s`, with only the caller REV differing:
baseline `bb08dd57f4b48bfb001a178e57b9c25e7040447f` → 8/22, exit 1;
content `7cd7f331ae151845ebff7bd100c1073ebad49351` → 22/22, exit 0.
Script SHA-256:
`8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`.
Full outputs and invocation evidence:
`.ufo/evidence/fleet-round-1/counter-literal-{baseline.txt,candidate.txt,invocations.json}`.
This correction supersedes the earlier literal-command reproducibility
claim, not the measured navigation delta; round status remains blocked.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| — none yet — | | | |

Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout.

## Saturation

The lane's saturation line and stagnation window N are to be declared by the lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this conformance change.

## Planned

Populated by the lane at each round start per the `AXES.md` §SCORECARD.md contract; no entries declared by this conformance rollout.

## Retired

- none retired; record with justification when an axis is retired.


## Round 12 (kaika) — pre-registered claims, baselines and rubrics

Steered round 12 (fleet-ledger `.ufo/waves/kaika/steer.md`; prompt
`.ufo/prompts/mado-round-12.md` at ledger `12a5571`). Fleet round 1
(2026-10-15) stays LIVE-blocked and unadmitted; it is superseded, not
resumed (`LOG.md` round-12 entry). Written **before** any round-12 work;
baselines measured at `e1d81d48026b6b9c9e9614c3b6390240200110db`, outputs
in `.ufo/evidence/round-12/before*.txt`.

### Six-axis baseline (bounded rubrics; lane's own claims as denominator)

| Axis / sub-axis | Rubric | Counting command | Baseline @ `e1d81d4` |
|---|---|---|---|
| calibration / lesson-grounded admission criteria | `10 × criteria citing a lesson / criteria` | `grep -cE '^[0-9]+\. .*lessons/' corpus/QUALITY.md` over `grep -cE '^[0-9]+\. ' corpus/QUALITY.md` | 0/5 → **0.0000** (lowest) |
| freshness / file-plane gate agreement | `10 × PASS / (PASS+FAIL+UNKNOWN)` on `--no-live` | `bash tools/mado-verify.sh --no-live \| awk '$3=="FAIL"\|\|$3=="UNKNOWN"' \| wc -l` (and `$3=="PASS"`) | 28/29 → **9.6552**; FAIL+UNKNOWN = 1 (`hypr.root.include_graph`) |
| coverage / admitted-note reachability (fleet r1) | unchanged rubric, Counting command above | literal fence (sha `8b59b503…`) via `bash -s`, `REV=<commit>` | 22/22 → 10.0000 (saturated on its finite denominator; harm watch only) |
| coverage / sourced current-art ground (new) | `10 × covered U-items / 7`; an item is covered when an admitted `corpus/knowledge/` entry opens with `source:` citing a `mined` `corpus/SOURCES.md` row and names the item | `for f in corpus/knowledge/*.md; do head -n 15 "$f" \| grep -qE '^source:.*\bS[0-9]{3,}\b' && echo "$f"; done \| wc -l` (entries) + `grep -cE '^covers: U[1-7]' corpus/knowledge/*.md` | 0 entries, 0/7 → **0.0000** |
| operability / hermetic suite pass fraction | unchanged rubric | `bash tools/mado-verify.sh --selftest` | 268/268 → 10.0000 (harm watch) |
| depth | unscored: no bounded rubric exists; declared, not invented this round | — | — |
| adjacency | unscored: no bounded rubric exists; report-not-absorb duty tracked per round in the report | — | — |

Uncovered ground U (pre-registered; sources `corpus/knowledge/arc-synthesis.md`
§6 gap ledger and the kaika ART dossier `kaika-w1/mado-art.md:7-24`):
U1 per-window rule effects (`arc-synthesis.md` §6 "no rule-read verb");
U2 Hyprland configuration-language era (hyprlang → Lua; `SKILL.md:344`);
U3 XDG portal backend routing and ScreenCast lifecycle; U4 Wayland protocol
phase and compositor-advertised globals; U5 output management / colour
boundary; U6 kernel-input → Wayland debugging ladder; U7 Waybar module text
(`arc-synthesis.md` §6).

### Claims (3; distinct axes; causally separable)

1. **C1 — calibration (lowest axis).** Mine the lane's own mistakes into
   `corpus/lessons/round-12.md` `## Mistakes`; append `QUALITY.md` criteria,
   each citing its lesson. Before 0/5 → target ≥5 lesson-cited criteria.
2. **C2 — freshness.** Re-verify and re-anchor the 2026-10-17 gkeep drift
   append-only (new `corpus/knowledge/config-drift-r12.md`, `SKILL.md`
   erratum, gate baseline erratum per `omarchy-drift-watch.md` re-anchor
   protocol). Before FAIL+UNKNOWN = 1 → target 0.
3. **C3 — coverage, capability acquisition "sources registry".** Create
   `corpus/SOURCES.md` (contract v1) and admit entries on U1–U3. Before 0/7
   → target 3/7 (4.2857). The capability row enters only if every contract
   census command runs clean.

Harm watch (every claim): selftest stays N/N; `--regression` ends
`MADO_REGRESSION: PASS` (re-cut if the gate moves); navigation counter
stays complete (N/N, exit 0); no config tree, compositor state or sibling
repo is written. Exploratory claim: none.

### Saturation (declared this round)

Saturation line: **9.0** on every scored sub-axis. Stagnation window:
**N = 3** rounds without a capability row. Both drive the nudge
(`AXES.md` §The stagnation nudge).

## Round 12 (kaika) — results

Measured at the round's final content commit `6e3b75fab5613eabf684857b49b9a658672196ed` (content first landed at `5174e15`; the
post-integration fixes are in the LOG round-12 entry), 2026-10-19; full output
`.ufo/evidence/round-12/after.txt`, produced by `REV=6e3b75f bash .ufo/evidence/round-12/after-measure.sh`; every count printed beside its exact command (its header's dirty
path is `after.txt` itself, created by the redirection). Self-verdicts, pending the orchestrator's
non-author verification.

| Claim | Axis / sub-axis | Counting command | Before @ `e1d81d4` | After @ `6e3b75f` | Verdict |
|---|---|---|---|---|---|
| C1 | calibration / lesson-grounded admission criteria | `grep -cE '^[0-9]+\. .*lessons/' corpus/QUALITY.md` over `grep -cE '^[0-9]+\. '`, counting only criteria whose cited paths and `#mistakes M<n>` rows resolve (resolver loop in `after.txt`) | 0/5 → 0.0000 | 11/16 → **6.8750**; strict reading (lane incidents only; 15–16 rest on external traps): 9/16 → 5.6250 | improved (either reading) |
| C2 | freshness / file-plane gate agreement | `bash tools/mado-verify.sh --no-live \| awk '$3=="FAIL"\|\|$3=="UNKNOWN"' \| wc -l` (+ `$3=="PASS"`) | 1 FAIL; 28/29 → 9.6552 | 0; 29/29 → **10.0000** | improved — conditional on operator intent to keep gkeep (L0) |
| C2 | freshness / present-tense SKILL claims contradicted by live without an erratum (reviewer F2) | `grep -c '^> Erratum (round 12' SKILL.md` and `grep -c '^## Errata (round 12)' SKILL.md` (pointer after the `:40-46` paragraph + EOF section) | 1 (`SKILL.md:40-46`, no erratum) | 0 (both greps print 1) | improved (same claim) |
| C3 | coverage / sourced current-art ground (join: sourced entry × `mined` row naming it × distinct `covers:`) | loop in `after.txt` § C3 | 0/7 → 0.0000 | 3/7 (U1, U2, U3) → **4.2857** | improved; capability below |
| — | coverage / admitted-note reachability | literal Counting command fence (sha `8b59b503…`), `REV=6e3b75f` | 22/22 | 26/26, exit 0 | unchanged (not harmed) |
| — | operability / hermetic suite pass fraction | `bash tools/mado-verify.sh --selftest`; `--regression` with `MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` | 268/268; PASS @ `dc7c4141…` | 269/269 (+1: gkeep.conf removal case); PASS @ `538d178b…` (third re-cut, 10/10 KILLED) | unchanged at 10.0000 (not harmed; one assertion added) |
| — | depth | unscored (no bounded rubric) | — | — | unchanged; AXES contract defect carried (reviewer F7) |
| — | adjacency | unscored (no bounded rubric) | — | — | unchanged; gkeep reported, not absorbed; `LOCAL` widening dropped |

Observational, not claimed: freshness rubric (a) — knowledge entries opening with
`source:`/`verified-at:`/`recheck:` — 3/22 → 7/26 (the four round-12 entries). Lowest-axis statement
corrected (reviewer F4): at pre-registration calibration and coverage/sourced-art were **tied** at
0.0000; this round works both. The W1 STATE dossier had called the lowest axis indeterminate and
recommended freshness. U3–U6 derive from the ART dossier's `[INFERENCE]`-tagged uncovered-seam bullet
(`mado-art.md:12`); U2 and U3 had partial prior host footholds (`keybind-rule-semantics.md:31`,
`remaining-planes-census.md:227-233`) — the new entries add the upstream era/routing/lifecycle layer.
Gate bytes: `93e43f8f…` (3,231 L) → `ea798ad078f139f3…` (3,245 L / 151,131 B) (`sha256sum tools/mado-verify.sh` @ `6e3b75f`).

### Capabilities (round 12)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources registry | Curate where mado learns: 39 opened, scoped-tier rows (mined/queued/rejected), study paths, search log; every contract census command runs clean and every mined row joins to an entry that cites it | `corpus/SOURCES.md`; census block in `.ufo/evidence/round-12/after.txt` | 12 |
| verdict gate (live + file plane) | Read-only verdict over the declared config plane and live hyprctl surfaces, exit 0/1/2, boundary check | `bash tools/mado-verify.sh` → `MADO_VERIFY: CLEAN (52 pass, 8 notes …)`, `.ufo/evidence/round-12/gate-live-after.txt` | 5 (re-demonstrated 12) |
| hermetic self-test | 269 assertions over isolated fixtures | `bash tools/mado-verify.sh --selftest` → 269/269, `gate-selftest-after.txt` | 5 (re-demonstrated 12) |
| mutation regression with re-cut | Replays the 10-defect kill table against the gate's derived target; SETUP on a moved gate, re-cut via the printed command | `gate-regression-setup-3.txt`, `gate-recut-3.txt`, `gate-regression-after.txt` | 7 (re-demonstrated 12) |

Stagnation window resets: a capability entered this round.

### Planned (round 13)

1. freshness/operability — M13 set-blind census: `local.inventory` and `sources_resolve` compare
   observed vs expected sets and name missing/extra members (today 13 `*.conf` on disk, inventory reads
   12/12); covering mutant + re-cut.
2. coverage — one bounded U4–U7 entry from the queued paths in `corpus/SOURCES.md` (`wayland-info`
   and `libinput` are not installed: `.ufo/evidence/round-12/l2-scout.md`).
3. operability/calibration — gate registry row at `SKILL.md` (registry home, `PROTOCOL.md` §Gate
   standard) and bounded rubrics for depth and adjacency (reviewer F7).

### Retired

None.

## Round 13 — declared claims (2026-10-20)

Baseline revision: `7dcb785b7b943d03703181b218d7860a7b43007b`.
L1 holds the canonical planner seat; wave items are bounded leaf work.

- **C1 coverage (lowest scored sub-axis):** sourced current-art ground
  U1–U3 = 3/7 (4.2857/10) → U1–U4 = 4/7 (5.7143/10).
  Admit one U4 entry separating protocol phases, compositor-advertised
  globals and unexercised behavior. Count unique `covers: U[1-7]` joined
  to existing knowledge paths and mined source rows, not source-row volume.
- **C2 operability:** exact-set census detection, a new bounded sub-axis.
  Baseline `sources_resolve` misses a same-count declared-source substitution;
  `local.inventory` misses extra local files. Target: all four isolated negative cases (extra local,
  missing+extra local replacement, same-count source replacement, missing
  gkeep) fail with stable row ids and named missing/extra details, versus
  the same cases at the baseline. Score = 10 × cases with complete named-set diagnostics / 4.
  Preserve include order checks and source-target existence; extend the
  hermetic suite and re-cut mutation regression. Register the existing
  verdict instrument at its SKILL registry home.

The claims are causally separable: U4 source admission needs no gate change;
the census fix needs no U4 note. No exploratory claim. Harm watch:
existing hermetic suite and mutation regression remain green, navigation
remains complete, and domain configuration/state remains read-only.
The earlier planned depth/adjacency rubric expansion is not claimed this round.

Pre-verification rubric clarification (AttackClaims / ReviewCensus):
this is **not** overall defect-detection recall. Baseline `include_graph`
already detects source substitution and `sources_resolve` already detects
missing gkeep. The named-set score requires the responsible census row
(`sources_resolve` for source substitution, `local.inventory` for the
three local-file cases) to fail with every relevant missing/extra name.
The measuring command also prints overall run exits so existing detection
is not hidden. A finite four-case score never retires broader operability.
Harm watch also includes `--no-live` file-plane agreement. Expanded toggle
glob membership, arbitrary source syntax and directory/symlink policy are
not claimed by the four-case correction.

## Round 13 — committed measurements and author verdicts

Content measured at **`95cbc41fe5d5db121b89c2ddd1f953728663c5f4`**,
2026-10-20. Baseline **`7dcb785b7b943d03703181b218d7860a7b43007b`**.
Exact counting commands, from this lane root:

```sh
python3 .ufo/waves/round-13/measure.py 7dcb785b7b943d03703181b218d7860a7b43007b
python3 .ufo/waves/round-13/measure.py 95cbc41fe5d5db121b89c2ddd1f953728663c5f4
```

Both counters exit 0 because they are observation probes, not admission
verdicts. Complete outputs/commands/exits:
`.ufo/waves/round-13/evidence/before.txt` and `after.txt`.
The counter reads every counted note, registry and index from the named
revision. U4 additionally requires the three facet rows and matching
phase/advertisement/core-registry mined-source joins; metadata alone is
not a body-quality judgment. Source semantics were reviewed separately
(ProtocolPhases, GlobalDocs, AttackCoverage); outside closure remains pending.

| Claim / axis sub-axis | Before | After | Score delta | Verdict and evidence |
|---|---|---|---|---|
| C1 coverage / sourced current-art ground | U1–U3: 3/7, 4.2857/10 | U1–U4: 4/7, 5.7143/10; U4 facets 3/3 | +1.4286 | locally verified improved; `knowledge/wayland-protocol-boundaries-r13.md`, reciprocal mined rows S005/S040–S043/S046; revision counter `coverage` field |
| C2 operability / complete named-set diagnostics in the declared four cases | 0/4, 0.0000/10; overall failing runs already 3/4 | 4/4, 10.0000/10; overall failing runs 4/4 | +10.0000 on this finite diagnostic subset only | locally verified improved; revision counter `exact_set` field, actual FAIL rows and every missing/extra name; no full-domain saturation inferred |

### Harm watch and limits

- Navigation **26/26 → 27/27**, missing/extra/duplicate 0; same revision
  counter `navigation` field. Its finite score stays 10.0000.
- Hermetic suite **310/310**, exit 0 —
  `bash tools/mado-verify.sh --selftest`; current pass fraction 10.0000.
  The old 269/269 is the prior round's record, not a fresh baseline-suite run.
- File plane **29/29 verdict-bearing rows PASS**, FAIL+UNKNOWN 0, exit 0 —
  `bash tools/mado-verify.sh --no-live`; freshness fraction stays 10.0000.
  Eight live SKIPs are not agreement or a current full desktop-health verdict.
- Historical regression **10/10 KILLED** with unchanged spec
  `c7ee75b9…`; new clauses **8/8 covering mutants KILLED**, restore OK.
  Re-cut target `87910c39…`; complete commands and outputs in
  `.ufo/waves/round-13/evidence/{regression-recut,covering-mutants}.txt`.
- Frozen companion verifies input digests before replay, ends
  `frozen_match` and `MADO_REGRESSION: PASS`, exit 0; selftest 12/12.
  `frozen/expected.json` and `evidence/frozen-regression.txt` beneath the
  round directory provide the second evidence over committed inputs.
- Gate committed SHA-256
  `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569`
  equals the frozen gate input. S041 committed capture SHA-256
  `ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949`.
  Re-derivation command: `git show <measured-commit>:<path> | sha256sum`;
  exact paths/digests in `evidence/committed-bindings.json`.
- No other axis score is claimed moved. Depth/adjacency remain unscored
  and unchanged, not silently retired. Calibration criterion 17 learns
  the outside S030 disagreement; that frontier duty is not a third claim.
- Fixed in-round defects are disclosed: raw session metadata was briefly
  retained in scratch then removed; initial frozen selftest crashed then
  passed after its sole scoping correction. Final committed artifacts
  retain no raw session data. No retained axis harm was observed; outside
  adjudication decides admission.

### Sources and demonstrated repertoire

The same revision counter records SOURCES **39 → 46**:
tiers **A=35/B=1/C=3 → A=42/B=1/C=3**; statuses
**mined=27/queued=9/rejected=3 → mined=34/queued=8/rejected=4**.
Seven new A rows include one rejected duplicate-admission correction,
not seven knowledge entries. Required maintained census before/after
both exits 0; final warnings S030/S042/S045 are explicitly retained.
Source mutations and all new-row opening quotes are in lesson § Gate.

| Capability | What it can now do | Demonstrated evidence | First-working round |
|---|---|---|---|
| source-fragment collision screen | Stop a repeated active canonical URL despite different scope wording; preserve rejected history and valid supersedes links | `python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest` 25/25; real historical registry exits 1 naming S017/S030, current exits 0; `evidence/collision-*-corrected.txt` | 13 |
| digest-pinned frozen regression | Verify both committed gate/harness input digests before evaluating the recorded regression, with tamper refusal | `python3 .ufo/waves/round-13/frozen/verify.py` → `frozen_match`, exit 0; `--selftest` 12/12; `frozen/expected.json` | 13 |

These demonstrations belong to C1's frontier and C2's gate conformance,
not additional claims. Short `evidence/` and `frozen/` paths above resolve
under `.ufo/waves/round-13/`. Saturation line remains 9.0 and stagnation
window N=3; the finite diagnostic subset does not retire broad operability.

### Planned (round 14; intent only, no mission opened)

1. coverage — one bounded U5 output-management/colour boundary entry,
   grounded in exact owning-protocol revisions and retaining unexercised
   feature behavior as unknown.
2. operability — address the named directory-shaped source-target and
   source-order fixture limits with isolated negative cases and covering
   mutants, without attempting a full hyprlang parser.

Retired: none. **Admission and SHONEN clearance remain pending the parent's
fresh non-author closure after this report lands.**

## Round 14 — declared claims (2026-10-20)

Baseline `873ff081b2ac363df771261b0ed950cba50d8988`. L1 holds the
canonical planner seat; one campaign-validated 32-seat wave serves these
two causally separable claims, with no exploratory claim.

1. **C1 coverage:** the lowest non-retired scored axis is sourced
   current-art ground, 4/7 = 5.7143/10. Admit one substantive U5
   output-management/colour boundary note citing opened primary S047/S048
   with reciprocal mined joins: target 5/7 = 7.1429/10. Neither source
   rows nor advertisement imply tested output changes or HDR.
2. **C2 operability:** on the explicitly new regular-source-target
   subset, count three isolated directory-shaped cases (direct,
   all-directory glob, mixed file/directory glob) whose owning
   `hypr.root.sources_resolve` row fails with the named non-regular
   target and overall exit 1. Target 0/3 → 3/3; baseline observation
   still to be run, so zero is a falsifiable prediction, not a result.
   Print all overall exits separately. Before any baseline measurement,
   ReviewResolver moved the direct fixture from local ai-usage.conf
   to default/hypr/windows.conf to isolate this row. The local-directory
   overlap is an unscored control. Source-order swap preserves existing
   behavior, not a falsely claimed new capability.

The revision-bound counting command is
`python3 .ufo/waves/round-14/measure.py <revision>`.
Broader operability is not retired by its earlier finite 10/10 rubric.
No domain-source-tree mutation, client feature request, kernel diagnosis or promotion
clearance is authorized. R13-V1..V3 are lesson-backed corrections within
these claims/frontier duties, not a third axis claim.

Premeasurement predicate tightening (AttackMetric / AttackNoHarm):
`10 × credited cases / 3`; credit requires the exact expected `~/`
path under `non-regular:` with no unresolved/missing/extra class, only
the resolver FAIL row, the declared toggle PASS/NOTE collateral status,
and identical owning-row detail under a second isolated root. The
mixed case must not accuse its regular sibling. Clean/order/file-symlink/
newline-regular/ai-usage-overlap/direct-missing/zero-match controls
are outside the denominator. No baseline result has yet been observed.
