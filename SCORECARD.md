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

| 38 | calibration | both round-37 admission counters still passed the five recorded cribs (M37-5: self-receipt, quote floor, non-unique rows, forged snapshot, docconn) | v3 repairs landed — pin-bound Gate digests, unique registry rows, quote floor, lineage clauses (c1); internally-consistent live triplet with /proc binding (c2); repaired manifest+counters discriminate v2 13/19 → 19/19 (the frozen pair replays 18/19; see LOG errata) | `python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev <rev>` → admitted=2/2; `python3 -I quality/check-r38-discrimination.py --manifest .ufo/waves/round-38/controls/manifest.json` → controls=19 correct=19/19 |
| 38 | operability | the request-socket domain had no admission counter (PRED-C2-r38-v1 did not exist); corpus/knowledge held 0 request-socket entries | `quality/counters/c2-r38-request-ground.py` ships and admits 3/3 entries (flags vocabulary, the five-second live bound at the host's own commit, upstream 1 MiB/64 KiB ceilings) at rev efb0ec2 | `python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev HEAD` → admitted=3/3 TARGET_MET (before: admitted=0/3 at f6e3247) |
| 38 | coverage | corpus/knowledge held 0 request-socket entries at base `f6e3247` — `select instance`, `poll(pollfds`, `REQUEST_LIMIT`, `FOLLOW_QUEUE_LIMIT` 0 hits in `corpus/knowledge`; navigation 52/52 | three request-socket package entries admitted re-grounded — `hyprctl-flags-r28.md` (S221), `request-socket-live-bound-r8.md` (S158/S187/S258/S277), `request-limits-upstream-r31.md` (S253); navigation 52/52 → 55/55 (fraction 1.0 unchanged) | `python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev HEAD` → admitted=3/3 TARGET_MET (before: admitted=0/3 at f6e3247); `python3 -I quality/check-index.py --rev bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 --repo .` → indexed=55/55 missing=0 dangling=0 duplicates=0 |
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

- none retired in the historical arc; record with justification when an axis is retired.
- `sourced-art` — **retired round 36.** Published at 1.0 in round 32 as `10 × covered U-items /
  7`, dropped from the publication in round 34 while this list still read "none" (round-35
  spot-check routed the disagreement). Retired rather than republished: its denominator was the
  fixed U1–U7 uncovered-ground list, five of whose items have since been closed by admitted
  entries, so the fraction no longer measures the ground it was built for and a saturated 1.0
  would read as coverage progress it is not. `corpus/README.md`'s per-round frontier rows
  remain the measured record of that ground.


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

Round-25 pointer (append-only, repair R6): the `source-fragment collision screen` row's "current exits 0" is stale —
at round-24 base and tip `MistakeFix.py --registry corpus/SOURCES.md` prints `collisions=4`, exit 1 (round-24
section "Capability status", scope paragraph; closure `corpus/lessons/round-24-verifier-spotcheck.md:106-111`). See
`## Current state (round 25)` for the round-25 re-run.

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

## Round 14 — committed measurements and author verdicts

Measured content **`32118fc1014837b3a385c7a66abbdc59b1560835`**,
2026-10-20. Baseline **`873ff081b2ac363df771261b0ed950cba50d8988`**.
Exact revision-bound counting commands, run from this lane root:

```sh
python3 .ufo/waves/round-14/measure.py 873ff081b2ac363df771261b0ed950cba50d8988
python3 .ufo/waves/round-14/measure.py 32118fc1014837b3a385c7a66abbdc59b1560835
```

Both observation probes exited 0; the full commands, raw gate digest,
source joins, facets, per-case rows and unscored controls are committed
in `.ufo/waves/round-14/evidence/{before,after}.txt`.

| Claim / axis sub-axis | Before | After | Score delta | Verdict and boundary |
|---|---|---|---|---|
| C1 coverage / sourced current-art ground | U1–U4, 4/7, 5.7143/10 | U1–U5, 5/7, 7.1429/10; U5 facets/source reciprocity true | +1.4286 | locally verified improved; `knowledge/output-colour-boundaries-r14.md`, S047/S048/S041/S050. The counter measures structural joins; parent source/body inspection and AttackCoverage's actual-note review supply the semantic hand check. No full U5 feature coverage inferred. |
| C2 operability / exact non-regular-source diagnostics in the declared three cases | 0/3, 0.0000/10; overall failing runs 0/3 on these selected isolated fixtures | 3/3, 10.0000/10; overall failing runs 3/3 | +10.0000 on this finite policy subset | locally verified improved; each exact non-regular path is the sole FAIL row, all other class clauses absent, declared toggle collateral retained, detail identical under a second root. Not whole-domain operability saturation. |

The direct case is **default/hypr/windows.conf**, selected before the
baseline, not the draft ai-usage case. The unscored ai-usage-directory
control already exits 1 before and after via local inventory; baseline
blindness to every possible directory placement is explicitly rejected.
Order-swap is already detected before and after. File-symlink and
newline-regular controls pass before and after; direct-missing and
zero-match controls retain unresolved before and after. The all-directory
case retains the no_gaps NOTE collateral, not all-row equality.

### Harm watch and falsifiability

- Navigation **27/27 → 28/28**, missing/extra/duplicates empty — same
  revision counter's `navigation` field.
- `bash tools/mado-verify.sh --selftest`: **372/372**, exit 0.
  Receipt `evidence/gate-selftest.txt` carries measured commit and raw
  gate digest itself. The prior 310/310 is historical, not a fresh
  baseline-suite run.
- `bash tools/mado-verify.sh --no-live`: **29 PASS, 0 FAIL, 0 UNKNOWN,
  8 SKIP, 4 NOTE**, exit 0; `evidence/gate-file-plane.txt`. This is
  file-plane agreement and within-run config-byte stability only.
- Historical recut **10/10 KILLED**, new regular-target mutants
  **4/4 KILLED**, retained census mutants **8/8 KILLED**, each with
  GREEN control and restore OK. Exact harness invocations/output and
  result tables: `evidence/{regression-recut,regular-target-mutants,
  retained-census-mutants}.txt` and corresponding TSVs. They grade the
  documented derived executable, not excised R7/R8 machinery.
- Derived target PIN **cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96**;
  historical SPEC_SHA stays **c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8**.
  Full current gate SHA-256 **fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207**
  equals the frozen gate input. These are distinct digests by design.
- Frozen replay `python3 .ufo/waves/round-14/frozen/verify.py` verifies
  gate/harness digests first, then returns `frozen_match` and
  `MADO_REGRESSION: PASS`, exit 0; its `--selftest` is **12/12**, exit 0.
  `frozen/expected.json`, `evidence/frozen-*.txt` and
  `evidence/committed-bindings.json` bind these to the measured content.
- The exact contract auditor committed in `evidence/contract-red.txt`
  exits **1**, `REGULAR_TARGET_CONTRACT: FAIL detected=0/3`, on the
  baseline observations; the same auditor exits **0**, PASS 3/3, on
  delivered observations (`contract-green.txt`). Four new mutants also
  demonstrate the repaired policy can fail.
- The same standalone-header audit exits **1** on the unchanged
  round-13 selftest receipt (missing measured_commit/gate_sha256), and
  **0** on this round's selftest receipt — `evidence/provenance-{red,green}.txt`.
  R13-V3 is a demonstrated record correction, not an extra scored claim.

### Sources, trends and limits

Source registry **46 → 50**, tiers A/B/C **42/1/3 → 46/1/3**, statuses
mined/queued/rejected **34/8/4 → 38/8/4**, by the same revision counter.
S047/S048 are new protocol sources; S050 is a tagged static safety
caveat; S049 corrects retention wording, not knowledge expansion.
S041 used-by is the sole existing-row mutation, logged in the lesson.
Both maintained census commands exit 0; W04 warnings for S030/S042/S045
are retained. Conservative source-merge screen exits 0 at rows=50,
collisions=0; `evidence/source-merge.txt`.

Coverage and operability are improved on the declared rubrics. Freshness,
calibration, depth and adjacency have no additional scored move and no
retained harm observed. Trends: expansion improved (one new U5 entry),
quality improved (strict regular-target instrument plus static safety
boundary), discernment improved narrowly (outside R13-V1..V3 become
grounded criteria/corrections with failing controls). Current-round
non-author spot-check/admission remains pending parent closure.

The probe is not a semantic admission oracle: U4 facets are structural,
registry validity is separately checked by the maintained census, and
space-containing diagnostic paths are outside its three named cases.
The gate preserves newline-regular handling, but broad boundary hashing,
generic grammar, expanded-glob membership, historical theme mutation
coverage and live/rendered feature behavior remain unclaimed.
Saturation remains 9.0, stagnation window N=3; retired axes: none.

### Planned next round (intent only; no mission opened)

1. calibration — read the fresh outside round-14 spot-check, learn any
   disagreement and re-derive the current rubric before selecting a move.
2. coverage — bounded U6 input-debugging layer route from opened primary
   sources, without raw input capture, injection or kernel diagnosis.

All shortened `evidence/` and `frozen/` paths above resolve under
`.ufo/waves/round-14/`. SHONEN stays four author assertions.

## Round 15 — declared claim (2026-10-20)

Baseline: `ea0446fcb4840089f0e541d96350144506fb5d1d`.
**C1 coverage**, lowest non-retired current-art rubric: sourced U1–U5
5/7 (7.1429/10) → sourced U1–U6 6/7 (8.5714/10). Admit one
bounded input-debugging layer route, not raw input capture or successful
application delivery. Keep the seven-ground denominator and the U4/U5
body/provenance requirements from round 14. U6 requires the provenance
trio, exactly `covers: U6`, reciprocal mined A/B source joins S051/S052,
and `## Layer ladder`, `## Safe boundary`, `## Unexercised delivery`
with explicit `[UNK]` in the last section. Before measurement, source review
rejected reusing S007: S051 supersedes its composite/mutable description;
S052 adds the distinct input-XML scope. Existing S007 remains queued.
Counting command: `python3 .ufo/waves/round-15/measure.py REV`.
The probe counts structure; L1 must inspect source/body semantics separately.

R14-V1 provisional ancillary mutation-receipt precision is a lesson-backed,
unscored correction: preserve historical records and append an accurate
mapping to the committed derived target. No wrapper or new gate behavior.
The gate remains unchanged. Harm watch: exact gate digest, complete
navigation, source census and bounded no-live/selftest receipts.
No exploratory claim, new repertoire capability, promotion clearance,
kernel diagnosis, device/event reading, replay, input injection or
configuration/compositor mutation. L1 holds canonical planner seat;
PlanningWalk is the bounded data-walk mapping inside one 64-seat wave.

## Round 15 — committed measurement and honest-stop verdict

Measured content `5f13870491588703ea6c81ef390488c5d2eeb727`;
baseline `ea0446fcb4840089f0e541d96350144506fb5d1d`, 2026-10-20.
Both commands below actually ran, exit 0 (observation, not admission):

```sh
python3 .ufo/waves/round-15/measure.py ea0446fcb4840089f0e541d96350144506fb5d1d
python3 .ufo/waves/round-15/measure.py 5f13870491588703ea6c81ef390488c5d2eeb727
```

| Claim / axis | Before | After | Delta / verdict | Evidence |
|---|---|---|---|---|
| C1 coverage / sourced current-art documented routes | U1–U5, 5/7, 7.1429/10 | U1–U6, 6/7, 8.5714/10; U6 S051/S052 joins, inverse and four facets true | +1.4286, locally verified improved on this bounded structural rubric | `evidence/{before,after}.txt`; actual source/body hand check in lesson §Gate; new U6 note, not successful input delivery |

Only U6 is added; no prior U-item is lost. Navigation 28/28 → 29/29,
missing/extra/duplicates empty. Sources 50 → 52; A/B/C 46/1/3 → 48/1/3,
mined/queued/rejected 38/8/4 → 40/8/4. S007 stays queued; no existing
registry mutable field changed. Census before/after exits 0 with the
same historical W04 S030/S042/S045 warnings. Source-merge screen exits 0,
rows 52, collisions/errors 0. These are structural/source conformance,
not non-author clearance.

### Harm watch and safety outcome

- Gate digest unchanged:
  `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`.
  The measurement probe hashes committed bytes and never executes the gate.
- One fresh `bash tools/mado-verify.sh --selftest`: 372/372, exit 0.
  One fresh `bash tools/mado-verify.sh --no-live`: 29 PASS, 0 FAIL,
  0 UNKNOWN, 8 SKIP, 4 NOTE, exit 0. Receipts name measured commit and
  raw gate digest. `boundary.readonly` is config-byte equality **within
  that run**, not unchanged host packages or equality across revisions.
- R14-V1 static correction audit: exact same command exits 1,
  `receipt_mapping_missing`, at baseline; exits 0,
  `receipt_mapping_verified`, mapped 3, problems [], at measured content.
  It derives 117602-byte target `cd1d73d7…` from the original committed
  gate and preserves three receipts. No gate/mutant replay is claimed.
- The actual install-plan overlap guard is red (exit 1, libinput already
  installed); the new-only in-memory control is green (exit 0).
  Both are static fixture evidence, not real pacman operations or host repair.
- **Operability safety: harmed.** LibinputEvents performed the forbidden
  partial upgrade recorded in lesson M2. Existing suite success and limited
  orchestrator ABI checks do not erase that policy/host-state harm or prove
  no input regression. No further package operation or restart is attempted.

| Axis | Verdict |
|---|---|
| coverage | improved, bounded C1 measurement above |
| operability | harmed on host safety; gate behavior itself unchanged |
| freshness | unchanged, no fresh live-input or freshness score claim |
| calibration | unchanged, no scored move; uncertainty/safety debt explicit |
| depth | unchanged, no separate scored claim |
| adjacency | unchanged, kernel/driver diagnosis and remediation not absorbed |

**Round admission: not asserted; no-harm condition unmet.** Expansion improved
narrowly; quality harmed; discernment improved narrowly by applying outside
R14-V1 and a lesson-backed demonstrated safety guard, not current outside
agreement. SHONEN stays four `[~]`. No exploratory claim, capability-table
entry, promotion or retirement. Saturation 9.0 / stagnation window N=3
unchanged. Halt progression; only the operator may authorize host remediation.

All short `evidence/` pointers here resolve under `.ufo/waves/round-15/`.
The next study intent, only after operator clearance, is the remaining
U7 observation boundary; no next-round mission is opened by that intent.

## Round 16 — declared claims (2026-10-20)

Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` includes the
independent round-15 rejected-harmed closure. This explicit operator round
authorizes source-only learning, not host remediation or live-health clearance.

- **C1 coverage**, lowest active finite rubric: documented source routes
  U1–U6 6/7 (8.5714/10) → U1–U7 7/7 (10/10). U7 requires provenance,
  reciprocal mined A/B S053/S054, and the exact sections `Producer contract`,
  `Renderer boundary`, `Safe observation`, `Unexercised rendering` with
  `[UNK]` in the last. Prior U1–U6 checks remain unchanged. This is not
  full domain coverage or a claim to observe rendered module text.
  Command: `python3 .ufo/waves/round-16/measure.py REV`.
- **C2 operability / capability acquisition**: absent (0) → demonstrated (1)
  bounded static action-plan classifier, with persisted paused policy,
  self-invocation assertions, negative actual-incident-shaped input and
  digest-bound frozen run. Commands: `python3 tools/mado-action-plan.py
  --selftest`, `--plan PLAN --policy POLICY`, and `--frozen DIR`.
  No numeric rewrite of the old hermetic-suite score. This gate grades
  declared JSON actions; it neither intercepts tools nor repairs the host.

These claims are causally separable: U7 source admission needs no classifier;
the classifier needs no Waybar note. R15-V1/V2 become an append-only
QUALITY criterion superseding criterion 20 while the host pause holds and
a current SKILL safety instruction. Host recovery stays operator-owned;
no package query/transaction, service operation, live compositor or input
probe is part of this round. No exploratory claim or promotion request.
L1 holds the planner seat; PlanningWalk supplies a bounded data walk.

### Round-16 pre-measurement selection correction — C3 calibration

PlanningWalk correctly found an omitted active calibration row from round
12. The initial “coverage lowest” assertion above is superseded, not
retired away: calibration remains below coverage. Add **C3 calibration**
within the three-claim cap: append lesson-grounded criterion 22 on this
selection error, independently of the U7 note and the safety classifier.
Counting command remains `python3 .ufo/waves/round-16/measure.py REV`,
which separately reports the original literal `^[0-9]+\. .*lessons/`
numerator over all `^[0-9]+\. ` criteria. This old counter measures
same-line lesson citations, not all multiline semantic grounding or
current source truth. It is not silently replaced by a friendlier counter.
Baseline/delivered fractions will be recorded from committed inputs.
Criterion 21 also carries its own lesson on its first line; criterion 22
alone still gives a calibration increase if C2's criterion is removed.
C2's runnable capability remains independently verifiable without 22.
All three claims are measured; none is exploratory.

## Round 16 — committed results and bounded author verdicts

Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`; initial content
`9dcf248993a9622a5b016edec0003187141745d2`; corrected measured content
`1e31681e76b5e7caadd1c749e18669a3632a1c3b`.
Commands actually run, all paths below under `.ufo/waves/round-16/`:

```sh
python3 .ufo/waves/round-16/measure.py 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea
python3 .ufo/waves/round-16/measure.py 1e31681e76b5e7caadd1c749e18669a3632a1c3b
python3 -I tools/mado-action-plan.py --selftest
python3 -I tools/mado-action-plan.py --plan .ufo/waves/round-16/fixtures/tight-red.json --policy .ufo/waves/round-16/safety-policy.json
python3 -I tools/mado-action-plan.py --plan .ufo/waves/round-16/fixtures/tight-green.json --policy .ufo/waves/round-16/safety-policy.json
python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen
```

| Claim / axis | Before → after | Verdict / measured evidence |
|---|---|---|
| C1 coverage, documented custom-module observation route | 6/7, 8.5714 → 7/7, 10.0000; +1.4286 | improved on the finite route rubric; `evidence/before.json`, `after-final.json`, all U7 facets/reserved/inverse true; actual source/body reviewed by L1 and falsify seats, never inferred from markers alone |
| C2 operability capability | absent → working finite declared-kind/12-name classifier | improved **capability only**, not host recovery; final selftest 52/52 exit 0; frozen_match exit 0 over expected refused sudo plan; red/green plan controls exit 1/0; independent cases 32/32 at initial content, normal classifier unchanged by the frozen-pair fix |
| C3 calibration, original literal lesson-citation fraction | 12/20, 6.0000 → 14/22, 6.3636; +0.3636 | improved narrowly; lowest active scored axis worked; `before.json`, `after-final.json`; lesson M1/M2/M3 exact-id rows resolve |

Calibration's separate block-citation reading is 15/20 (7.5000) →
17/22 (7.7273), **not the score**. Exact inline counting command and output:
`evidence/calibration-readings.json`. This observes a structural rubric, not
general self-assessment truth. The scored gain depends on first-line lesson
citations for criteria 21/22; wrapped 18–20 stay uncounted. Without criterion
21, criterion 22 alone gives 13/21 (6.1905), still above baseline; C3 does
not require the safety classifier or the U7 note. Initial wrong selection
is preserved and corrected, not retired away. Same selection-audit command,
same baseline scores, only declared_axes changes: `selection-red.json`
exit 1, `selection-green.json` exit 0. PlanningWalk's block count is not
transcribed as the literal score.

The 7/7 denominator is now at its finite documentary ceiling; retain it as
harm watch, not a proxy for the coverage axis. **Retired: none.** Coverage
remains open across actual behavior, built-in module text, Walker/terminal/
theme/idle surfaces and the arc gap ledger. A subsequent coverage claim
needs a new declared rubric/baseline, never silently an eighth item divided
by seven. Saturation line 9.0 / N=3 unchanged; no stagnation waiver claimed.

### Demonstrated capability

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| finite declared-action classifier | Refuse blocked declared kinds, the 12 pinned argv[0] names, unknown kinds and malformed inputs; compare a digest-pinned declared-plan replay | `python3 -I tools/mado-action-plan.py --selftest` 52/52 and `--frozen .ufo/waves/round-16/frozen` frozen_match at corrected content; `evidence/action-selftest-final.json`, `action-frozen-final.json`, `committed-bindings.json` | 16 |

`plan_safe` is not arbitrary-command safety, credential/probe permission or
host prevention. Unlisted wrappers/interpreters/operands/destinations are
not analyzed; residual controls intentionally show that limit. The frozen
receipt binds executable and expected-file hashes to the measured commit;
in-directory pins alone do not authenticate a coordinated rewrite.

### Harm watch, defects and admission

First classifier selftest **51/52**, frozen run exit **2**, exposed M6's
double-colon expected-pair bug. Exact reachable pairs fixed it without
weakening a fixture; original red and final green receipts both retained.
Final executable SHA-256:
`226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3`.
Legacy gate unchanged `fba82a66…`; isolated selftest **372/372**, exit 0.
No legacy live or no-live host run, regression or sibling gate executed.

Navigation **29/29 → 30/30**, missing/extra/duplicates empty. Sources
**52 → 55**, A/B/C **48/1/3 → 51/1/3**, mined/queued/rejected
**40/8/4 → 43/8/4**; census before/end exit 0, historical W04
S030/S042/S045 retained. No existing source-row cells changed.

Per-axis: coverage improved (bounded); calibration improved (literal rubric);
operability improved only for the new runnable capability, while **host-safety
harm from R15-V1 remains carried, unresolved and operator-owned**. Freshness,
depth and adjacency unchanged, not freshly scored. No new host transaction
or tool install is evidenced. M4 misroot and M5 prohibited read-only package
query are real process defects, disclosed, not erased by green tests.

Trends: expansion improved (one sourced route and demonstrated repertoire);
quality improved narrowly for the instrument/source precision, with carried
host harm and process debt explicit; discernment improved through grounded
outside-closure follow-through and falsified M6, not fresh outside agreement.
**Admission not asserted; independent closure/operator disposition remains
required, and this round does not readmit round 15.** SHONEN stays four
author assertions. Both waves (64+32=96) ran before the wrap-up directive;
no new worker afterward. No next-round mission is opened.

## Round 17 — declared claims (2026-10-20)

Baseline `27cd06f` (includes the admitted round-16 closure and its routed
R16-V1/V2). Written before any round-17 wave. L1 holds the canonical planner
seat; wave items are bounded leaf work. Host pause carried: no package
query or transaction, service, compositor, input or screenshot operation;
config trees are read as file bytes only. R15-V1 stays operator-owned.

Axis re-derivation (QUALITY22, every active row under its recorded rule):
calibration literal 14/22 = **6.3636** (lowest active scored);
coverage U-route 7/7 (finite ceiling, harm watch); freshness file-plane
29/29 (r12, harm watch); operability hermetic 372/372 + classifier 52/52
(harm watch); depth/adjacency unscored. No stagnation waiver (capability
entered round 16).

- **C1 calibration (lowest axis).** Route R16-V1 (receipt cited for a
  verdict token it does not carry) into lesson `round-17.md` M1 and an
  append-only lesson-cited QUALITY criterion, with a label check shown to
  fail on the round-16 lesson line. Command:
  `git show REV:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'` over
  `grep -cE '^[0-9]+\. '`. Before 14/22 = 6.3636 → target ≥ 15/23.
- **C2 coverage — new declared rubric V (post-ceiling; U stays 7/7).**
  PROVINCE.md owned surfaces P1 Hyprland config tree, P2 Waybar, P3 Walker,
  P4 terminal-emulator configs, P5 themes/wallpapers, P6 screen/idle
  (hypridle/hyprlock). A surface is covered when an admitted
  `corpus/knowledge/` entry's first 15 lines carry `source:` citing a
  `mined` tier-A SOURCES row whose `used-by` names that entry, and the entry
  declares it: `surface: P<n>` (new entries) or the fixed legacy map
  `covers: U1|U2 → P1`, `covers: U7 → P2` (declared now, never widened in
  this round). Command: `python3 .ufo/waves/round-17/measure.py REV`.
  Baseline 2/6 = 3.3333 → target 4/6 (P6 idle/lock, P4 terminal) from
  sources opened this round. Documentary routes, not observed behaviour.
- **C3 operability — capability acquisition: post-hoc transcript
  tripwire.** `tools/mado-tripwire.py` reads OMP session JSONL and
  classifies only commands actually issued as `bash` tool calls (not text
  mentions) into host_mutation / package_query / live_probe. Before:
  absent at `27cd06f`. After: hermetic selftest N/N exit 0, and the real
  round-15 transcripts return the libinput `sudo pacman -S` call as
  host_mutation, agreeing with an independent oracle. Detection after the
  fact only — never interception, prevention or host repair.

Separable: C1 counts QUALITY text only; C2 needs no tool or criterion; C3
needs no note or criterion. Harm watch: hermetic selftest 372/372,
classifier selftest 52/52, U 7/7, navigation complete, census exit 0. No
exploratory claim.

### Round-17 pre-measurement corrections (append-only; advisers RevPreRegistration, CriticC2, RevRubricV)

- **Lowest axis.** The declaration names calibration (6.3636) lowest while
  declaring rubric V at 2/6 = 3.3333. V is a new coverage sub-axis created
  this round, so it is now the lowest active row. Both V (C2) and
  calibration (C1) are worked, so the lowest-axis obligation holds under
  either reading; the U-route 7/7 row is unchanged (harm watch).
- **Instrument.** `measure.py` was absent at `0175f13`. It was committed and
  bound before any note integration: `f52f43f` (sha256 `a280b3ab…`), then
  tightened — exact `surface: P<n>` line, legacy credit pinned to the three
  entries that held it at `27cd06f`, at least one cited mined tier-A row
  that is an upstream https source of kind docs/spec/code naming the
  surface, and a three-line content floor per required section — at
  `ab0bc9b` (sha256 `4023124f…`). Stricter only; baseline stays 2/6 under
  both (`evidence/measure-before.json`, `measure-instrument.json`).
- **C1 attribution.** Only criterion 23 is credited to C1 (target 15/23). A
  tripwire criterion was proposed and **not** added to QUALITY (it would be
  C3 work inflating C1's fraction). Semantic block-citation counter, per
  QUALITY 22, reported beside the literal one.
- **C3 pins.** Selftest suites `tripwire/core` and `tripwire/compound` must
  pass in full with case counts stated; the red anchor is the single file
  `MadoR15/MadoR15.LibinputEvents.jsonl` with finding tuple (line 54,
  `call_38165`, host_mutation, rules `sudo` and `pacman:-S`); agreement is
  checked against the independent oracles and against `/var/log/pacman.log`
  lines 2429-2437 (UTC 07:25:16Z = 04:25:16-0300).
- **Host pause.** "Paused host-wide" is an instruction to lanes, not a host
  fact: `/var/log/pacman.log:2440-3152` shows 13 non-lane runs on
  2026-10-20 07:45-09:39 (including `pacman -Syu`), none after round launch.
  R15-V1's current host state is `[UNK]` and operator-owned.

## Round 17 — committed results and bounded author verdicts

Measured with `python3 .ufo/waves/round-17/measure.py REV` (receipts
`evidence/measure-before.json`, `measure-final.json`): 27cd06f → f71ccbe.

| Claim / axis | Before → after | Verdict / evidence |
|---|---|---|
| C1 calibration, literal lesson-citation fraction | 14/22 = 6.3636 → 15/23 = 6.5217 (+0.1581) | improved narrowly; only criterion 23 added (append-only); semantic block counter 17/22 = 7.7273 → 18/23 = 7.8261 (QUALITY 22); label check `evidence/label-check-final.txt` EXPECT 7/7 exit 0, R16-V1 red line MISMATCH |
| C2 coverage, rubric V (PROVINCE P1-P6) | 2/6 = 3.3333 → 4/6 = 6.6667 | improved as declared, joined, documentary sourcing: P1/P2 inherited, P6 idle/lock route, P4 one Alacritty-only route; behaviour, launch and host binaries `[UNK]`; V cannot detect an invented row (wave-2 E1) — non-author re-open of S056-S071 required |
| C3 operability capability, post-hoc transcript tripwire | absent → present (`tools/mado-tripwire.py` sha256 `962919ce…` after the late P11 fix) | capability acquired, detection after the fact only; suites 9/9, 16/16, 33/33, 30/30 (`evidence/tripwire-selftest-*.txt`); anchor exit 1; adversarial 4/26 pinned as known limits; not prevention, not R15-V1 remediation |

Harm watch at `f71ccbe`: hermetic selftest 372/372 (`harm-legacy-selftest.txt`,
gate sha `fba82a66…` unchanged), classifier 52/52, U 7/7, navigation 32/32,
census exit 0 (three historical W04). Freshness: not re-measured. No axis
harmed by lane action; operability carries R15-V1 (operator-owned, `[UNK]`).
Sources 55 → 71 (A 51 → 64, C 3 → 6; mined 43 → 56, rejected 4 → 7).
Saturation 9.0 / N=3 unchanged; retired: none.

### Capabilities (round 17)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| post-hoc transcript tripwire | Classify commands issued in OMP session JSONL (bash; python eval `!`/`%%bash`/literal spawns; shell/python heredocs) into host_mutation / package_query / live_probe with exit 0/1/2 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening,w2-regressions}`; `evidence/tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt` | 17 |

### Planned (round 18; intent only)

1. operability/calibration — close the remaining tripwire misses that recur
   in real transcripts (variable `bash -c` recipes, helper-wrapped spawns) or
   record them as permanent limits; frozen replay to make it a gate.
2. coverage — P3 Walker or P5 theme sourced route under rubric V, with
   committed raw fetch receipts so a closure can tell fetched from invented rows.
3. freshness — re-anchor present-tense pins moved by the 2026-10-20 `-Syu`
   (walker 2.17.2, hyprland 0.56.2-4) by file bytes and pacman.log only.

## Round 18 — declared claims (2026-10-20)

Baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` (includes the admitted
round-17 closure `round-17-verifier-spotcheck.md`, routed R17-V1..V5).
Written before any round-18 wave. L1 holds the canonical planner seat;
wave items are bounded leaf work. Host pause carried: no package query or
transaction, service, compositor, input or screenshot operation; config
trees are read as file bytes only. R15-V1 stays operator-owned. Lane VCS is
jj-colocated; commits only through `scripts/hyaku/jj-lane.sh`.

Axis re-derivation (QUALITY 22; `python3 .ufo/waves/round-17/measure.py
d9a5a18`, instrument unchanged, `evidence/measure-before.json`):
calibration literal 15/23 = **6.5217** (lowest active scored);
coverage rubric V 4/6 = 6.6667 (P3 Walker, P5 themes open); coverage
U-route 7/7 (finite ceiling, harm watch); freshness file-plane 29/29
(r12, harm watch; not re-measured — live re-anchor is planned work, not
claimed); operability hermetic 372/372 + classifier 52/52 + tripwire
suites (harm watch); depth/adjacency unscored. No stagnation waiver
(capability entered round 17).

- **C1 calibration (lowest axis).** Route R17-V1/V2 (scan receipts
  without tool sha or measured revision; report cites the wrong tool sha),
  R17-V5 (instrument tightenings without committed mutant receipts) and the
  jj-audit finding JjAuditMado F10 (`tools/mado-verify.sh:3406` digests a
  failed `git show` as the empty-input sha and reports a local edit) into
  `lessons/round-18.md` `## Mistakes` and append-only lesson-cited QUALITY
  criteria, each with a runnable check shown able to fail. Command:
  `python3 .ufo/waves/round-17/measure.py REV` (`c1`: literal
  `^[0-9]+\. .*lessons/` over `^[0-9]+\. `). Before 15/23 = 6.5217 →
  target ≥ 18/26.
- **C2 coverage — rubric V (unchanged instrument).** Sourced documentary
  routes for **P3 Walker** and **P5 themes/wallpapers** from tier-A rows
  opened this round, each new credited row backed by a committed raw fetch
  receipt (body bytes, sha256, byte count, fetch time — R17-V3) so a closure
  can tell a fetched row from an invented one. Command:
  `python3 .ufo/waves/round-17/measure.py REV` (`c2`). Before 4/6 =
  6.6667 → target 6/6. Documentary routes, not observed behaviour; host
  binaries `[UNK]`.
- **C3 operability — capability acquisition: tripwire frozen replay
  (R17-V4).** `tools/mado-tripwire.py --frozen DIR` verifies the digest of
  every committed snapshot input before comparing a committed expected
  verdict (`frozen_match` 0 / `frozen_verdict_mismatch` 1 /
  `snapshot_tampered` or `frozen_error` 2); a committed snapshot of the
  real incident transcript lines; the registry row moves `probe` → `gate`.
  Before at `d9a5a18`: `--frozen` is a usage error (exit 2), no frozen
  baseline, registry `probe`. After: frozen run exit 0 `frozen_match`,
  a tampered copy exit 2 `snapshot_tampered`, frozen selftest suite N/N.

Separable: C1 counts QUALITY text only; C2 needs no tool or criterion; C3
needs no note or criterion. Routed jj-migration fixes (gate rc capture,
`.gitignore .ufo/state/`) are harm-watched defect repairs, not claims.
Harm watch: hermetic selftest N/N (re-cut if the gate moves), classifier
52/52, tripwire suites N/N, U 7/7, navigation complete, census exit 0.
No exploratory claim.

## Round 18 — committed results and bounded author verdicts

Measured with `python3 .ufo/waves/round-17/measure.py REV` (instrument sha256
`de4c422b…`, unchanged): before `d9a5a18` (`evidence/measure-before.json.txt`),
after `4c103b5` (`evidence/measure-after.json.txt`) and final `be886a3`
(`evidence/final/measure-final.json.txt`; identical c1/c2). Every receipt's first
line names `tool_sha256` and `measured_commit` (QUALITY 24).

| Claim / axis | Before → after | Verdict / evidence |
|---|---|---|
| C1 calibration, literal lesson-citation fraction | 15/23 = 6.5217 → 18/26 = 6.9231 (+0.4014) | improved narrowly; criteria 24-26 append-only, each with a check shown to fail: 24 `receipt-check.py` 21/21 exit 0 with 6 round-17 reds `MISSING_PROVENANCE`, `STALE`/`SHA_MISMATCH` controls; 25 `measure-mutants.py` 6/6 bites (loose `a280b3ab…` vs tight `de4c422b…`), re-run reproduced (w2 MeasureMutantsRerun); 26 OM9/OM10 (gate 389/389; old gate FAIL "local edit" on `e3b0c442…`, `gate-rc-redbefore.txt`; pipefail reverted → fails, w2 CriticC1W2/MutGateOM 8/8 killed). Semantic block counter 18/23 → 21/26. Outside critics: 24 was not green at `abfbf35` (anchored regex, PENDING claims) — fixed in `be886a3` |
| C2 coverage, rubric V (P1-P6) | 4/6 = 6.6667 → 6/6 = 10.0000 | improved as declared, documentary sourcing only: P3 `walker-route-r18.md` (S072-S091), P5 `theme-route-r18.md` (S092-S095). 24/24 new rows re-opened by non-author seats, all agree (lesson § Gate). Credited web rows 21/21 have a 200 receipt whose sha is in the anchor; 329 licensed bodies committed, 95 digest-only; fresh clone `fetch-verify` exit 1 only on 4 per-fetch HTML tree URLs in S094's secondary anchor (M7). Host rows S090/S091/S095 have no receipt by construction. Rubric V now saturated on its finite denominator: retained as harm watch; behaviour, rendered UI and running binaries stay `[UNK]` |
| C3 operability capability, tripwire frozen replay | `--frozen` usage exit 2 at `d9a5a18` (`evidence/tripwire-frozen-before.txt`) → gate entry | capability acquired: `--frozen .ufo/waves/round-18/frozen` `frozen_match` exit 0, one-byte tamper `snapshot_tampered` exit 2 (`evidence/final/`), frozen suite 31/31 (the `abfbf35` tool 17/31), provenance `match`; scan suites 9/16/33/30 unchanged; real-transcript re-cut identical. Change-detector over 5 pinned incident files (8 findings, 3 known misses), not classifier correctness, prevention or R15-V1 remediation |

Tool shas, labelled: tripwire `962919ce…` (`d9a5a18`, round-17 landed), `c87a31ef…`
(`4c103b5`/`abfbf35`), `c1ae45a7…` (`be886a3`, final). Gate `fba82a66…` →
`c9fb0cef…`; `PIN_MADO` `cd1d73d7…` → `20714096…`, regression 10/10 PASS.

Harm watch at `be886a3` (`evidence/final/harm-watch-summary.txt`, PASS): gate
selftest 372 → 389/389 (+17 OM9/OM10, none dropped), classifier 52/52, tripwire
9/9, 16/16, 33/33, 30/30, frozen 31/31, failsafe 1/1, U 7/7, navigation 32/32 →
34/34, census exit 0 (three historical W04). Freshness: not re-measured as a score;
SKILL erratum records the walker 2.17.0 → 2.17.2 move by file read. No axis harmed
by lane action. Host: `/var/log/pacman.log:3161-3169` records a `pacman -U zcode`
at 13:23 -03 during this round — no mado tool call issued it (seat scan
`evidence/final/tripwire-r18-seats.txt` clean in covered forms); actor `[UNK]`,
operator-owned; R15-V1 unchanged and operator-owned.
Sources 71 → 95 (A 64 → 88; mined 56 → 80). Saturation 9.0 / N=3 unchanged;
retired: none.

### Capabilities (round 18)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| tripwire frozen replay (gate entry) | Verify digests of committed incident transcript lines and compare the tripwire's verdict with a pinned expected verdict (0 match / 1 mismatch / 2 tampered, unpinned or baseline error) | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen`; `--selftest .ufo/waves/round-18/tripwire/frozen`; `evidence/final/tripwire-frozen-*.txt` | 18 |

### Planned (round 19; intent only)

1. operability — apply or reject the three tripwire drafts (`drafts/TwMissBashCVar.patch`,
   `TwMissHelperFn.patch`, `TwInstallerChannels.patch`), re-pinning the frozen
   baseline at the landed classifier; a jj command class.
2. coverage — a rubric beyond V (observed behaviour or module text), and a
   superseding row for S094 without HTML digests; PROVINCE refinement for the
   `~/.config/omarchy/**` path root (w2 ConnProvinceScope).
3. freshness — re-anchor the remaining 2.17.0-era pins and gate `walker` version pin.

C3 scope (residual check W3CriticC3Final, append): the frozen gate watches 5 rule
ids over 5 pinned files; known misses are annotations; eval-path coverage stays with
the scan suites; self-pinned rewrites still match. All `evidence/final/` receipts are
bound by `receipt-check.py` claims (`EXPECT_SUMMARY: 33/33`).

Correction (append; residual check W3CriticC1Final): "Every receipt's first line
names `tool_sha256` and `measured_commit`" above is too broad. It holds for the
measure, tripwire and frozen-provenance receipts (bound by `receipt-check.py`,
33/33). `evidence/gate-rc-redbefore.txt`, `regression-recut.txt`,
`gate-selftest.txt` and `measure-mutants.json` lack that header (two name the
uncommitted gate `2bdf5e8a…`): they are provenance only. Criterion 26's
reproducible red is the d9a5a18 block swapped into the landed gate (383/389, five
OM9 failures; w3 report `W3CriticC1Final.md`); the GateRerun receipts
`evidence/w2-gate-selftest.txt` (389/389) and `w2-gate-regression.txt` (PASS)
carry the header at `abfbf35`. Round-19: `:3479` worktree-hash status, M6 bite rule,
quoted-pair acceptance in `receipt-check.py`.

Residual-check corrections (append; w3 `MadoR18.W3NumbersAudit`,
`MadoR18.W3TripwireFinal`): `RETENTION.json` lists 103 digest-only bodies; 95 is
fetch-verify's count of digest-only receipt lines (8 retained bodies have no receipt
line and are never credited). "re-cut identical" means identical verdict JSON (the
files differ by the producer header). MutGateOM: 8/8 killed, of which m07 (`-z`
arm reorder) only by the R10 pin assertion. receipt-check controls also include
`NOT_ANCESTOR` and `PRODUCER_MISMATCH`. Frozen findings F1/F2 (blank-line pin on an
expected finding reads verdict mismatch; `link/.` bypasses the symlinked-dir check)
and `measure-mutants.py` defaulting `--out` to the lane are routed to round 19.

## Round 19 — declared claims (2026-10-20)

Baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` (includes the admitted
round-18 closure `round-18-verifier-spotcheck.md`, routed R18-V1..V4 plus the
carried frozen F1/F2, `measure-mutants.py --out`, jj-audit F6/F9/F16/F17 and the
three tripwire drafts). Written before any round-19 wave. L1 holds the canonical
planner seat; wave items are bounded leaf work. Host pause carried: no package
query or transaction, service, compositor, input or screenshot operation; config
trees and host binaries are read as file bytes only. R15-V1 stays operator-owned.
Lane VCS is jj-colocated; commits only through `scripts/hyaku/jj-lane.sh`.
Baseline receipts: `.ufo/waves/round-19/evidence/*-before.txt` (first line
`RECEIPT … tool_sha256=… measured_commit=9c54c56…`).

Axis re-derivation at `9c54c56` (QUALITY 22): calibration literal 18/26 =
**6.9231** (`python3 .ufo/waves/round-17/measure.py REV`, instrument `de4c422b…`
unchanged); coverage rubric V 6/6 (saturated, harm watch) and U-route 7/7 (harm
watch); operability hermetic suites 389/389 + classifier 52/52 + tripwire suites
(harm watch). Two bounded sub-axis rubrics are declared this round, before
measurement, because the routed defects sit on ground no existing rubric
counts:

- freshness / walker version-pin currency: `python3 -I
  .ufo/waves/round-19/fresh-pins.py REV`. Denominator fixed at `9c54c56`: owned
  files (corpus/knowledge/*.md, corpus/README.md, SKILL.md, PROVINCE.md, tools/*)
  whose bytes contain `2.17.0` — 13 files. Current = the file carries a line
  holding `2.17.2` and an `S###` row token. Before **2/13 = 1.5385** (lowest).
- operability / tripwire recall on the frozen real-incident lines: `python3 -I
  .ufo/waves/round-19/tw-recall.py REV`. Denominator fixed at `9c54c56`: the 6
  (file, line) pairs in `.ufo/waves/round-18/frozen/expected.json`
  (`expected_findings` ∪ `known_misses`), inputs digest-checked; numerator =
  lines on which `REV:tools/mado-tripwire.py --scan` reports ≥1 finding. Before
  **3/6 = 5.0000** (tool `c1ae45a7…`).

- **C1 calibration.** Route R18-V1 (S094 anchor cites per-fetch HTML digests),
  R18-V4 (S084 cites the unpinned docs.rs `latest` alias), R18-V3 (a supersession
  marked in two files while eleven owned files kept the old pin) and R18-V2
  (criterion 26's own red-before rests on a headerless receipt) into
  `lessons/round-19.md` `## Mistakes` and append-only lesson-cited QUALITY
  criteria, each with a runnable check shown red on a real `9c54c56` artifact.
  Before 18/26 = 6.9231 → target ≥ 21/29.
- **C2 freshness (sourced).** Re-anchor the walker pins: every file in the
  fixed set gains an in-file dated pointer (or a re-pinned value) citing a
  SOURCES row opened this round for the host walker bytes (binary rodata version
  literal + file digest, read as bytes) and the upstream release; the gate's
  `live.walker.version` pin and its selftest stub move with it. Before 2/13 →
  target 13/13. Live `walker --version` is not run (host pause): the row states
  file-byte evidence only.
- **C3 operability.** Apply or reject the three round-18 tripwire drafts
  (`TwMissBashCVar`, `TwMissHelperFn`, `TwInstallerChannels`), rebased on the
  `c1ae45a7…` tool, with every existing suite still all-pass; re-pin a round-19
  frozen baseline at the landed classifier (the round-18 baseline must then read
  `frozen_verdict_mismatch`, which is the change made visible). Before 3/6 →
  target 6/6.

Separable: C1 counts QUALITY text only; C2 needs no criterion or tool change
outside the gate's pin; C3 needs no note, row or criterion. Non-claim repairs
(harm-watched): S094 superseding row and S084 re-point (frontier step), PROVINCE
path-root line for `~/.config/omarchy/**`, frozen F1/F2, `measure-mutants.py
--out`, gate F6 (tip instead of `HEAD`) and F9 (`rev-parse --git-dir`), a
landedness check (F16). Harm watch: gate selftest N/N (re-cut if the gate
moves), classifier 52/52, tripwire suites N/N, frozen r18 suite 31/31, U 7/7,
rubric V 6/6, navigation complete, census exit 0. No exploratory claim.

## Round 19 — committed results and bounded author verdicts

Measured at `01b80946d92b26370d3012a7da655d00dd135154` (tools final; later commits
change prose and receipts only). Receipts: `.ufo/waves/round-19/evidence/harm/`
(`HARM_WATCH: PASS`, 22 runs, every file headed `RECEIPT … measured_commit=01b8094…`),
before receipts `evidence/*-before.txt` and their producer-bound re-cuts
`evidence/*-before-recut.txt` (lesson M5).

| Claim / axis | Before → after | Verdict / evidence |
|---|---|---|
| C1 calibration, literal lesson-citation fraction (`python3 .ufo/waves/round-17/measure.py REV`, `de4c422b…`) | 18/26 = 6.9231 → 20/28 = 7.1429 (+0.2198) | improved narrowly; **pre-registered target ≥ 21/29 missed** by decision: R18-V2 is recorded as an application of criterion 24, not a criterion 29 (CriticC1: restatement). 27 durable anchors (`anchor-durability.py`: red `9c54c56` `FLAGGED S084 S094` exit 1 → green `df84807` `flagged=0`); 28 supersession sweep (`supersede-sweep.py`: red `stale=11` → green `stale=0`). R18-V2: `receipt-check.py` reads the round-18 red-before receipts `MISSING_PROVENANCE`; header-bound re-cut `evidence/gate-swap-receipt.txt` 383 passed / 6 failed (five OM9 + R10) |
| C2 freshness, walker pin currency (`python3 -I .ufo/waves/round-19/fresh-pins.py REV`) | 2/13 = 1.5385 → 13/13 = 10.0000 (at `df84807` and `01b8094`) | improved as declared, **sourced** on S096 (host walker bytes opened this round: `/usr/bin/walker` sha256 `25240650…`, one literal `2.17.2` at offset 856,302, none `2.17.0`). Every credited line cites S090/S091/S096 (supersede-sweep ledger rows; README via the S072–S091 span). This is dated provenance, not re-measurement: `walker --version`, the running process and 2.17.2 behaviour stay `[UNK]`. Gate pin 2.17.0 → 2.17.2 with the PASS narrowed to "installed version matches pin; 2.17.0-era claims stay dated" |
| C3 operability, tripwire recall on the 6 frozen real-incident lines (`python3 -I .ufo/waves/round-19/tw-recall.py REV`) | 3/6 = 5.0000 (tool `c1ae45a7…`) → 6/6 = 10.0000 (tool `367be947…`) | improved on a six-line set the drafts were written for (overfit-prone by construction, lesson M7). Guards reported beside it: the three new findings are `package_query/pacman:-Q`, the class the round-18 known-miss notes name; zero findings on the 20 control lines; whole-corpus base-vs-merged diff lost 0 findings (w1 TwMerge-2; w2 RerunPrecision re-runs it). Round-18 frozen baseline now reads `frozen_verdict_mismatch` (the change made visible); round-19 baseline `.ufo/waves/round-19/frozen` `frozen_match` (`50d2a45e…`) |

Harm watch at `01b8094` (PASS): gate selftest 389 → 443/443 (+54 WL0-WL3, OM10A/B,
OM11-OM16; none dropped), regression PASS (`PIN_MADO` `05aea198…`), classifier 52/52,
tripwire suites 247/247 over 11 suites (two case edits, both reasoned: round-17
hardening `multiline-quoted-commit-clean` → `-vcs` and round-19 `eval-clean` →
`eval-literal-argv-commit`, because a real `git commit` is now a `vcs_write`
finding; host_mutation stays 0 in both), rubric V 6/6 (P5 via S092/S093/S097, P3 via
S072–S083/S085–S091/S098), U 7/7, navigation 34/34, census exit 0 (W04 now also
names S097/S094 sharing a URL; S094 is rejected). No owned axis harmed by lane action.
Sources 95 → 98 (A 88 → 91; mined 80 → 81; rejected 7 → 9). Saturation 9.0 / N=3
unchanged; retired: none.

Non-claim repairs landed: S097/S098 supersede S094/S084; PROVINCE `~/.config/omarchy/**`
path-root line; gate jj F6 (tip read only when `$tree/.jj` exists; plain-git detached
HEAD still reports MOVED) and F9 (`rev-parse --git-dir`); frozen F1/F2; tripwire classes
`tool_install` (permit-able) and `vcs_write`; `measure-mutants.py` no default lane
write; `landed-check.sh` (F16 narrowed: a probe, not a gate row). F17 stays
operator-owned: colocation is structural while `HYAKU_VCS=jj` (w1 JjIncidentScan).

### Capabilities (round 19)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| landedness check | Say whether each cited lane hash is an ancestor of the live remote tip (`LANDED`/`LOCAL_ONLY`/`MISSING`) without fetching or writing | `bash .ufo/waves/round-19/landed-check.sh LANE HASH...`; w1 `LandedCheck.md` (T1-T9 matrix) | 19 |

### Round 19 — wave-2 corrections to the results above (append-only)

Wave 2 (67 seats over `01b8094`, reports `.ufo/waves/round-19/w2/reports/`) re-ran every
counter and reproduced 18/26 → 20/28, 2/13 → 13/13 and 3/6 → 6/6. It narrowed the prose:
- C1 (CriticC1W2, CriticAdmission): improved, target missed. Criterion 28's walker entry is
  the C2 file set, so its green is not independent of C2; the ledger now also carries the
  S094→S097 and S084→S098 supersessions. Both checkers' limits are appended to QUALITY.
- C2 (CriticC2W2, RerunC2, RerunC1): read as "13/13 pointed; 5/13 name S096 on the
  crediting line; 0 walker facts re-measured on 2.17.2". The 2/13 baseline credited two
  round-18 lines (`corpus/README.md:44`, `walker-route-r18.md:1`); substantively 0/13
  before. Two pointers that called S096 "reserved" were corrected in place and seven notes
  carry appended wave-2 corrections (lesson M10).
- C3 (CriticC3W2, AdvHelperFn, AdvVcs, RerunC3, RerunPrecision): read as "3/6 → 6/6 on the
  six lines the drafts were written for; 5/6 without the HelperFn rule-B lead; the three new
  findings are `package_query/pacman:-Q` as the round-18 notes predict; 0 findings on the 20
  control lines; 0 findings lost across the real corpus". Rule B fires on 2 real lines
  (both true) but on 12/12 synthetic data-only shapes and does not mark its rows as leads;
  eval-surface VCS writes stay unseen. Limits, not admitted coverage (lesson M14).
- Harm watch: unchanged numbers; the round-17 hardening suite reads 32/33 under the
  pre-round tool after its one reasoned case edit (CriticHonestyW2 A7). Gate selftest showed
  two non-reproducible fixture-loss failures under concurrent seat runs (ScribeScorecardCheck,
  MutGateR19); every isolated run reads 443/443 → cause `[UNK]`.

### Round 19 — final state (append-only)

Tools final at `61eaa071161e401a370fbdc3000de1cfbf99e1cd` (gate `071d39d9…`, 4,160 L:
F5-F9 comment fixes, F6 rescue now requires `.jj` and equal `HEAD^{tree}`/tip tree,
OM1 PATH guard; `PIN_MADO` `f03e6cab…`). Final receipts `evidence/final/` (commit
`6963d34`), each headed `RECEIPT … measured_commit=61eaa07…`: C1 20/28, C2 13/13, C3
6/6; criterion 27 red `9c54c56` exit 1 / green exit 0; criterion 28 red exit 1 / green
exit 0 (three ledger entries); class scan (three `package_query/pacman:-Q`, 0 control
hits); frozen r19 `frozen_match`, r18 `frozen_verdict_mismatch`; token-join PASS; gate
selftest 452/452. Harm watch at `61eaa07` PASS (`evidence/final/harm/`: gate 452/452,
regression PASS, 11/11 suites, classifier 52/52, U 7/7, navigation 34/34, census exit
0). `python3 -I .ufo/waves/round-18/receipt-check.py .ufo/waves/round-19/receipt-claims.json`
→ `EXPECT_SUMMARY: 16/16`. Gate selftest 389 → 452 (+63), no prior assertion lost
(w2 CriticAdmission label diff at 443; the 9 added since are OM1 guard, OM17, WL1).

### Capabilities (round 19, addendum)

Tripwire classes `tool_install` and `vcs_write` are not entered as capabilities: their
w2 precision findings (help/dry-run rows, eval-surface misses, synthetic rule-B false
positives) are open.

### Planned (round 20; intent only)

1. operability/precision — tripwire: rule-B name-binding guard and lead tagging, `jj …
   --help`/`git --dry-run` carve-outs, eval-argv VCS coverage, `curl … | sh`, pip
   pre-verb options; adopt the w2 regression cases (AdvHelperFn 14, AdvVcs 6,
   AdvInstallers 6, AdvBashCVar, MutMergedTripwire 5) red-before → green; re-pin.
2. freshness — line-level pin currency (55 of 73 `2.17.0` lines without a same-line
   pointer, w2 ScribePlannedRow) and the same-morning moves the walker sweep missed:
   elephant 2.21.0 → 2.22.1, uwsm 0.26.7 → 0.27.1, hyprland 0.56.2-2 → -4, hyprtoolkit.
3. calibration — tool-honesty fixes routed by w2 SentinelToolSafety/ReviewHarmTool
   (harm-watch worktree block, supersede-sweep worktree ledger, frozen-repin README
   receipt without `measured_commit`, frozen pin-spelling normpath, anchor-durability
   exit code) as lesson-cited criteria with reds.

Final-state correction (append-only): after `0fa4125` the gate gained the F9 containment
`[ -e "$tree/.git" ]` before `rev-parse --git-dir` (w2 ReviewJjFinal: a `.git`-less tree
under `$HOME` resolved to the dotfiles repo) with scenario OM18. Tools final at
`7b4839d31d60af5bac40e3e74aec70e928601dfc` (gate `050efc72…`, 4,194 L, selftest 460/460,
regression PASS, `PIN_MADO` `367ff5ec…`). Final receipts and harm watch re-cut at
`7b4839d` (commit `d642ce5`): `HARM_WATCH: PASS`, C1 20/28, C2 13/13, C3 6/6, criterion
27/28 red→green unchanged; receipt claims re-pointed, `EXPECT_SUMMARY: 17/17` (adds the
post-wave seat scan). Gate selftest 389 → 460: the ten old OM10 assertions were replaced by
OM10A/B; no other prior assertion lost.

## Round 20 — declared claims (2026-10-20; repair round)

Baseline `1f7f995caa25627db804e996cccd87fe38a3a1b6` (round-19 tip `b435568` + the
closure `corpus/lessons/round-19-verifier-spotcheck.md`, which closed round 19
**rejected-harmed**: HelperFn rule B turns provably pure data — `BLOCK=frozenset(['pacman',
'-Q','hyprland'])` — into an ordinary `package_query` finding with no lead marker).
Pre-harm baseline for every no-harm comparison: `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.
Written before any round-20 wave. L1 (MadoR20) holds the canonical planner seat. Host
pause carried: no package query or transaction, service, compositor, input or screenshot
operation, no real `hyprctl` by L1 or any seat; host files are read as bytes only.

- **C1 operability / tripwire precision (sourced; R19-V3 first).** Counter
  `python3 -I .ufo/waves/round-20/tw-precision.py REV` (written in wave 1, committed
  before any tool edit). It runs `REV:tools/mado-tripwire.py --scan` (temp copy, `python3
  -I`, cwd = temp) on every case of the round-20 precision suite
  `.ufo/waves/round-20/precision/`, read at the commit that first lands the suite (that
  commit lands no tool change), and compares the exit code and the multiset of (class,
  rule, line, evidence) with the case's expectation. `evidence` is `observed` (the
  transcript states the command and its execution path: bash text, `!`/`%%bash`, a
  literal spawn, or a helper whose body is visible in the scanned transcript) or `lead`
  (a literal argv handed to a callee whose body is not visible). A row with no
  `evidence` key is an unmarked claim of execution: it matches `observed` and never
  `lead`. Families, each ≥ 4 cases, pre-declared: **P** pure containers/formatters
  (want clean), **S** binding/shadowing, **W** real wrapper misses (want observed), **H**
  help/dry-run non-writes (want clean) with write negatives (e.g. `git commit -n`, which
  is `--no-verify`), **L** invisible-body leads (want `lead`). Score = 10·passed/N.
  Before measured at `1f7f995` (tool `367be947…`) and at `9c54c56` (tool `c1ae45a7…`);
  target N/N. Admission guards (C1 fails if any breaks): `tw-recall.py` 6/6 unchanged
  and reported split observed/lead; zero findings on the 20 control lines; every P case
  also passes at `9c54c56` (the pre-harm reading is restored, not approximated); a
  whole-corpus diff of the `9c54c56` and final tools loses zero findings and classes
  every added row; every existing tripwire suite all-pass (a case edit only with its
  reason); round-19 frozen replay recorded (re-pinned for round 20 if the schema moves).
  Sourced on SOURCES rows opened this round (git help/dry-run semantics, jj help,
  Python builtins).
- **C2 calibration (lowest-scoring measured axis, 7.1429).** Counter `python3
  .ufo/waves/round-17/measure.py REV` (key `c1`, instrument unchanged). Before 20/28 =
  7.1429 → target 22/30 = 7.3333 with two lesson-cited criteria, each with a runnable
  check red on a real round-19 artifact: **29** an isolation harness fails closed — a
  setup failure aborts before any payload (red: the round-19 `inns.sh` `[ -e ] && mount
  && echo` shape, R19-V4; the check's payload is a canary file write, never a host
  probe); **30** a count stated in a SCORECARD/lesson/report claim is re-derived at the
  measured revision by a cited command (red: round 19's "155 transcripts" vs a
  154-file receipt, "5/13 name S096" vs 8/13 any-line / 6/13 first-line, "ten OM10
  assertions" vs nine labeled occurrences). R19-V1: round 19's ≥21/29 miss stays a miss;
  neither criterion restates 24, 27 or 28, and this target is registered fresh.

Separable: C1 is the tool, its suite and counter (no QUALITY text); C2 is QUALITY text
and two round-20 checkers (no tool change). Non-claim repairs (harm-watched, append-only):
R19-V2 S096 tally (any-match 8/13, first-match 6/13, five S090-only files; provenance, not
behaviour), R19-V4 incident record (154 files; written-script scan blindness;
self-report, not detection), R19-V5 (nine labeled OM10 occurrences, eight distinct),
R19-V6 (absolute lane paths in every seat item; dead seats uncredited). Reserved SOURCES
ids S099–S110 (L1-assigned). Harm watch: gate selftest N/N, regression PASS, classifier
52/52, tripwire suites N/N, U 7/7, rubric V 6/6, navigation complete, census exit 0. No
exploratory claim.

### Round-20 pre-measurement corrections (append-only; before any after-measurement)

Wave-1 advisers (CriticC2Inflation, RevCriterion30, ConnCriteriaFleet; reports under
`.ufo/waves/round-20/w1/reports/`) showed that registered criterion **30** ("a stated count
is re-derived at the measured revision by a cited command") restates criterion **10**
(`corpus/QUALITY.md:16`: "Report each count as `<n> — <command> <date>` and rederive it
from the named revision"), which the pre-registration's restatement screen (24/27/28) did
not check, and that its "5/13" red mixes a different counting rule and revision
(`01b8094`, cited-as-evidence) with the closure's `b435568` any-line/first-line counts.
Disposition, by R19-V1's own rule (no duplicate criterion): registered 30 is
**withdrawn**; the three round-19 tallies are recorded as an **application of criterion
10** (no new number), checked by `.ufo/waves/round-20/tally-check.py`, each tally with its
counting rule and revision named.

Replacement, registered here before any after-measurement and flagged for the closure as a
possible target-preserving swap: criterion **30′** — a detector change credited for recall
is admitted only beside its precision evidence: committed negatives of the shapes the new
rule could misread, read at the pre-change and changed tools, a whole-corpus diff against
the pre-change tool listing every added row, and a machine-readable `lead` marker on any
row the detector cannot tie to a visible execution path. Ground: the round-19 harm itself
(closure R19-V3; round-20 lesson M1); no criterion 1–28 covers detector precision. Red:
the closure's data-only frozenset artifact at `1f7f995` (unmarked ordinary finding); its
check is the C1 counter's P and L families, so 30′'s green is **not independent of C1**.
C2 target unchanged at 22/30 = 7.3333; if the closure rules 30′ a swap, the honest C2
reading is 21/29 = 7.2414 (criterion 29 only), reported beside it.

E4 amended by wave-1 evidence (CaseDryRunBash, CaseHelpDryRunEval, ScoutJjHelpEmpirical,
SrcJjHelp): `jj git push --dry-run` without `--ignore-working-copy` snapshots the working
copy and stays a `vcs_write`; `jj describe -m --help` is rejected by jj (exit 2, no op);
git `--help` is rewritten only at the first argument after the subcommand, `-h` among
options prints usage; `git commit --short|--porcelain|--long|-z` imply `--dry-run`;
`pull -n`, `merge -n`, `cherry-pick -n`, `add -N` and `commit -n` are writes.

## Round 20 — committed results and bounded author verdicts

Suite landed `f3da50488661509ce5d144c90f7780f8088e0903` (no tool change; 175 scored
cases from 13 blind case-author seats, 12 held out as outside the contract,
`assemble-suite.py`); tool repair `28c68378eccbd5f227cdc28a62406ff390e3540a` (tool sha256
`9613f510…`: TwRuleB v2 + TwVcsHelp + one L1 line, `env = bindings = None`, lesson M6).
Receipts `.ufo/waves/round-20/evidence/`, each headed `RECEIPT … measured_commit=28c6837…`
with the data revision in argv.

| Claim / axis | Before → after | Verdict / evidence |
|---|---|---|
| C1 operability, tripwire precision (`python3 -I .ufo/waves/round-20/tw-precision.py REV`, suite pin `f3da504`) | `1f7f995` 29/175 = 1.6571 (P 7/66, S 2/17, W 4/22, H 15/52, L 1/18) → `28c6837` 172/175 = 9.8286 (P 66/66, S 17/17, W 21/22, H 51/52, L 17/18); pre-harm `9c54c56` 110/175 = 6.2857 (P 66/66) | improved; **pre-registered target 175/175 missed by 3**: `W-CaseWrapperForms-class-method-instance` (case wants a stated miss; the tool now resolves the visible method body that spawns — a true detection), `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` (case wants `jj $c --help` clean; TwVcsHelp measured that a user alias with `--help` runs its command, so the tool keeps it), `L-AdoptW2-AdvHelperFn-b14` (a lead for a parameter callee inside a never-called def; not implemented). Cases were not edited after the result. Sourced on S099–S108, S111 (opened this round) |
| C1 guards | recall `tw-recall.py`: 6/6 at `28c6837` = **5 observed + 1 lead** (`r13-root.jsonl:4`; `tw-recall-split.py`); 20 control lines 0 findings; P at `9c54c56` 66/66 and at `28c6837` 66/66; held-out 0/12 → 0/12; existing suites 11/11 all-pass (`--selftest`, 247/247 cases) after 8 reasoned case edits that each add a finding (`r20_edit` fields; lesson Decisions) plus the `lead` marker on two lead cases; `--frozen round-19` `frozen_match`, `--frozen round-18` `frozen_verdict_mismatch` (unchanged expected red) | whole-corpus diff vs `9c54c56`: pending (wave 2) |
| C2 calibration (`python3 .ufo/waves/round-17/measure.py REV`, key c1) | 20/28 = 7.1429 → 22/30 = 7.3333 (QUALITY 29 fail-closed isolation; 30′ detector precision) | improved as registered after the pre-measurement correction; if the closure rules 30′ a target-preserving swap, the reading is 21/29 = 7.2414. 29: red `inns-r19-shape.sh` `FAIL_OPEN` 5/6 modes, exit 1 → green `isolate.sh` `FAIL_CLOSED` 6/6 + positive control, exit 0 (`evidence/crit29-*.txt`). 30′: red P 7/66, L 1/18 at `1f7f995` → green 66/66, 17/18 (not independent of C1). Round-19 tallies as an application of criterion 10: `tally-check.py` red 5/5 MISMATCH |

Non-claim repairs: R19-V2/V4/V5/V6 corrections in `corpus/lessons/round-20.md`
§Corrections; the round-19 C1 miss stays a miss (R19-V1). Sources 98 → 112 (S099–S112,
tier A, mined). Knowledge `corpus/knowledge/tripwire-precision-r20.md`; SKILL §"Reading
tripwire rows — observed vs lead; fail-closed harnesses (round 20)".

### Capabilities (round 20)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| tripwire evidence marker | Tell an observed command from a lead (argv stated, executing body not visible) on every finding row, and drop provably pure data | `python3 -I .ufo/waves/round-20/tw-precision.py 28c6837` (P 66/66, L 17/18); `tw-recall-split.py 28c6837` (5 observed + 1 lead) | 20 |
| harness fail-closed check | Show whether a stub/namespace harness runs its payload after any of six forced setup failures | `bash .ufo/waves/round-20/isolation-check.sh HARNESS` (`evidence/crit29-*.txt`) | 20 |

Round-25 pointer (append-only, repair R6): the `tripwire evidence marker` row's "L 17/18" was measured at `28c6837`
and is superseded: `tw-precision.py` gives L 15/18 at `8e5d9369` (round-24 section "Capability status", row
`tripwire evidence marker` = `fails`). See `## Current state (round 25)` for the round-25 re-run.

## Round 20 — attempt-2 recovery registration (2026-10-21)

Timing, stated plainly: the fixture populations below were committed by attempt 1 and the nine
`a2/fixtures/` were written before any attempt-2 tool edit, but this text is written after a
draft repair was developed and measured in a sandbox clone; it lands before that repair.

Attempt 1 (MadoR20) ended without a report after landing `f8576f7` (helper-recovered,
PHASE2 incident 6) and checkpoints `ed4bf22`, `38d1b36`; recovery coordinator
MadoR20Recovery reuses that work, claim base `1f7f995`, and holds the planner seat. Its
wave 2 (78 seats) falsified C1's no-harm reading on populations outside the scored suite,
all committed by attempt 1 at `f8576f7`/`38d1b36` before this registration:
AdvRecallShapes (49 certain real-execution shapes found by `9c54c56`/`1f7f995`, silent at
`28c6837`), AdvDepth/AdvLeadMarks (silent starred/lambda/asyncio shapes), AdvCrash
(13 transcripts flip to `internal RecursionError` exit 2 where `1f7f995` scans),
CorpusRuntime (a self-recursive helper costs ~N⁴: 30 s vs 0.07 s), AdvPureShapes (24
pure-stdlib `from`-import fixtures emit `lead` rows), RevToolDiffVcs (`jj -R git … git
push` and `jj -R bookmark … bookmark create` missed: measured writes), AdvVcsForms (31
measured non-writes flagged). C1 is therefore **not admissible at `28c6837`**; the
attempt-2 repair is part of C1 (same axis, same counter) and is measured by:

- C1 counter unchanged: `python3 -I .ufo/waves/round-20/tw-precision.py REV` (suite pin
  `f3da504`), target unchanged 175/175; every guard registered at `e629f73` unchanged.
- New guard counter `python3 .ufo/waves/round-20/a2/a2-guards.py REV --fixtures-rev PIN`
  over the frozen wave-2 fixture populations (recall 81 files, crash 172, pure 24 named by
  AdvPureShapes, AdvVcsForms 74 with its measured `truth`) plus nine attempt-2 fixtures
  (`a2/fixtures/`, written before any attempt-2 tool edit; `dotted-rebind-sp` was rewritten
  once before measurement because its first text bound `sp` to the stdlib `json` module,
  whose `run` does not exist — a fixture error, not a tool reading). Admission targets
  (no harm): `recall_lost` 0 (two exclusions declared by AdvRecallShapes itself: gap04
  old false positive, ar49 signal-contingent), `crash_flip` 0, `vcs_fn` 0, `dup_rows` 0,
  `timeouts` none; improvement targets: `pure_rows` 24 → 0, `vcs_fp` 31 → lower,
  `a2_mismatch` → 0.
- Whole-corpus diff (`w2/CorpusDiffV2/corpus-diff-v2.py`) from `9c54c56` (registered
  guard: 0 lost) and from `28c6837` to the attempt-2 tool, every lost row classed.

## Round 20 — attempt-2 results and bounded author verdicts (2026-10-21)

Tool v3 `3610e3ec76ab951043cbc41110d30f6f94a72ec2` and v3.1
`a8960de655e6ea8c0a3bf74f5542041d9fe25b39` (tool sha256 `a57d4fe9…`; v3.1 adds only the
unparsed-segment rule, lesson M15). Every number below was re-run by L1 MadoR20Recovery at
`a8960de` (receipts `.ufo/waves/round-20/a2/evidence/`, each headed `RECEIPT …
measured_commit=…`); none is carried from attempt 1 without a re-run.

| Claim / axis | Before → after | Verdict / evidence |
|---|---|---|
| C1 operability, tripwire precision (`python3 -I .ufo/waves/round-20/tw-precision.py REV`, suite pin `f3da504`) | `1f7f995` 29/175 = 1.6571 → `a8960de` 172/175 = 9.8286 (P 66/66, S 17/17, W 21/22, H 51/52, L 17/18), same three failing cases as `28c6837` | improved; **registered target 175/175 missed by 3** (unchanged reasons above; w2 AtkFailingThree reads two of the three wants as stale, 174/175, reported beside, no suite edit). Full suite incl. held-out 172/187 → 174/187 |
| C1 guards (registered at `e629f73`) | recall 6/6 = 5 observed + 1 lead, 20 control lines 0 findings (`recall-split-a8960de…`); P at `9c54c56` 66/66 and at `a8960de` 66/66; 11 suites all pass and `--frozen round-19` `frozen_match`, round-18 baseline mismatch unchanged (harm-watch PASS, `a2/evidence/harm/`); whole-corpus diff `9c54c56` → `a8960de`: **0 lost** on 7,889 stable files, 7,253 added rows in 99 class/rule/evidence groups (vcs_write observed 7,012 / lead 4, tool_install 208, live_probe 20, package_query observed 6 / lead 3) listed in `corpus-diff-9c54c56-vs-a8960de.json` | hold |
| C1 attempt-2 guards (registered `6a7d9ca`; `a2-guards.py REV --fixtures-rev 6a7d9ca`) | `28c6837` → `a8960de`: recall_lost 52 → 0, crash_flip 13 → 0, pure_rows 24 → 0, vcs_fn 0 → 0, vcs_fp 31 → 20, a2_mismatch 6 → 0, dup_rows 0 → 0, timeouts none → none; `hang-selfrec-40` 54.764 s → 0.037 s, `hang-mutual-24` 6.754 s → 0.050 s | hold (targets met; vcs_fp lower, not zero: abbreviations and `=false` forms stay findings) |
| C1 removal side from `28c6837` (`corpus-diff-28c6837-vs-a8960de.json`, classed in `…-classified.txt`) | lost 5 rows / 4 calls: 3 installer `--help`, 1 `git push -nv` (measured dry run), 1 `heapq.nlargest` data lead; 22 same-command lead duplicates dropped; added 10 (2 jj `-R` pushes, 6 lead rows in TabiR16/SoujiR18 cells, a git add/commit pair at `MadoR17.AttackRubricGaming.jsonl:38`) | every row classed; the v3 run of the same diff found M15, fixed in v3.1 |
| C2 calibration (`python3 .ufo/waves/round-17/measure.py REV`, key c1) | 20/28 = 7.1429 → `a8960de` 22/30 = 7.3333 | improved as registered; conservative reading 21/29 = 7.2414 if the closure rules 30′ a target-preserving swap. 29 re-verified at `a8960de` (`a2/evidence/iso/`): red 5/6 `FAIL_OPEN` exit 1, green 6/6 `FAIL_CLOSED` exit 0, four adversarial harnesses and four mutants exit 1. 30′'s legs hold at `a8960de` but did not catch M9 (a recall loss): recorded in QUALITY's attempt-2 note, a removal-side criterion queued for round 21 |

Frontier: SOURCES 112 → 115 (S113–S115 opened 2026-10-21, tier A, mined; census `validate`
exit 0); the sourced claim is C1's v3 stdlib purity split (S113 process side, S114
`json.dumps`, S115 `list2cmdline`). Mistakes mined this attempt: M9–M15
(`corpus/lessons/round-20.md`). Wave-2 dispositions: `.ufo/waves/round-20/a2/w2-dispositions.md`.
Harm watch at `a8960de`: gate selftest 460/460, regression PASS, classifier 52/52, U 7/7,
V 6/6 (c2 6, `u_routes` 7), navigation 35/35, census exit 0. Runtime: the two corpus
files w2 CorpusRuntime timed at 30 s / 14 s took 25.85 s / 4.77 s at `28c6837` and
0.062 s / 0.142 s at v3 in one L1 run (2026-10-21, host shared with other lanes).

### Capabilities (round 20, attempt 2; append-only)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| tripwire reached-body sweep | Report every visible body the executed text reaches but the call path does not follow (thread targets, callbacks, decorators, closures, dunders, scheduled coroutines, recursion, past-depth helpers) as a `lead` row instead of dropping it | `python3 .ufo/waves/round-20/a2/a2-guards.py a8960de --fixtures-rev 6a7d9ca` (`recall_lost` 0; 52 at `28c6837`) | 20 |
| detector removal-side guard | Count, for a tripwire change, the findings an older tool reported that the new one drops, the crash flips and the pure-data rows, over frozen adversarial populations | `a2/evidence/guards-before-28c6837.txt` vs `guards-after-a8960de….txt` | 20 |

### Final residual-review disposition (supersedes author verdicts above)

All eight attempt-2 reviewer/critic reports are under
`.ufo/waves/round-20/a2/review/`; none died. **C1: harmed**, despite the reproduced
172/175 count: ReviewV3Diff found recursive shell-string and callback-literal misses;
CriticPrecisionV3 found 18 new false leads and a missed `imaplib.IMAP4_stream` process;
ReviewRuntimeV3 exceeded 1,800 MiB on large assignment-only cells (old tools 80–167 MiB).
CriticRecallV3 also found a partialmethod miss dating from `28c6837`.
ReviewVcsV3 confirmed unflagged jj remote/bookmark/workspace writes under
`--ignore-working-copy` at both revisions, and newly exempted `add -Nn` / `commit -zn`
that still write Git objects or refresh the index (the write boundary was too broad
to call these no-writes). It also found bare `uv tool run --help` falsely flagged.
**C2: unprovable independently**, although its literal counter reproduces 22/30:
30′ reads C1's own evidence, so the two claims are not causally independent.
RerunAllV3 reproduced the fixed-population checks but whole-corpus counts drifted on
the unpinned live input; those totals are dated observations, not reproducible census.
ReviewDocsV3's three count/path/revision corrections landed before this disposition.
Final trend verdicts: expansion improved (sources and evidence), quality harmed
(counterexamples above), discernment improved (independent reviews surfaced and
retained the failures). Round admission is not claimed. Under the operator's wrap-up
instruction, unresolved behavioral defects are explicitly handed back to Main; no next
round was started, and no review report is outstanding.

## Round 21 attempt 1 — declared repair claims, before measurement

Base `794aaeb22b4bf35b2482a6779733b69343baff5b`; registration landed `0644c536224847ecbb0b6c530d55d142e24f86c9`, pre-measurement clarification/wave provenance `0caf5f3ef31a38d4dfc5c4a4b586619b2f6ad452`. MANIFEST rounds[387] and `corpus/lessons/round-20-verifier-spotcheck.md` remain authoritative: rounds 19/20 rejected-harmed; no retroactive admission or restored capability is inferred.

- **C1 operability:** actual residual recall/precision/body-binding/VCS/retained-memory repair, independently authored truth population frozen before implementation; score rubric `10 * matching new oracle cases / frozen new oracle cases`. Before and after command and measured revisions will be recorded only after observed runs. No true old finding may be silently lost; every whole-fixture-corpus removed/relabelled row needs adjudication. Resource population is 1000/2000/4000 shallow assignments under a strict 384-MiB address-space cap and 15-second timeout. Same direct `main` wrapper before/after isolates retained snapshots from the CLI's unrelated 512-MiB thread reservation; CLI behavior is checked separately. The unchanged round-20 benchmark stays historical: 172/175, three misses, no target weakening.
- **C2 calibration (lowest non-retired measured axis), capability acquisition:** a separate artifact-assessment integrity gate, its independently specified valid/invalid fixtures and actual input hashes. It does not run/read C1's classifier or counter; reverting C1 must leave its result unchanged. Before capability absent; after target all frozen artifact expectations, plus red on the actual old wrong-topic SHONEN assessment and green on a canonical corrected assessment. No synthetic permissive baseline or inflated criterion count. Timestamp/provenance checks bound artifact assertions, not omniscient proof that no unrecorded measurement happened.

Planned for this steered round only: seal oracle/resource/corpus populations, measure bounded red, integrate production repairs, final stable checks and independent advisory attacks, then report both actual verdicts. No next round or admission is pre-claimed; no saturation waiver, retirement or exploratory claim.

## Round 21 — measured delivered-code results (2026-10-21)

Code measured at `a6cef8984d3815775587ab634ce558e13338b0eb`: classifier SHA256 `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1`; assessment SHA256 `66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4`. The earlier failed integrations and their receipts remain history; only this revision is the delivered-code measurement below.

| Claim / axis | Before → after; counting command | Score delta / evidence / measured revision |
|---|---|---|
| C1 operability / frozen independent static-truth agreement | `python3 -I .ufo/waves/round-21/oracle/measure.py --tool tools/mado-tripwire.py`: `b96d1b888a111971b430dc653f5826dc041b26bd` primary8/35, supplemental5/17 → `a6cef8984d3815775587ab634ce558e13338b0eb` primary35/35, supplemental17/17. Primary eligibility and all normalizations/rejections were sealed before implementation; supplemental cases never enter its denominator. | Local rubric `10 × primary matches /35`:2.2857→10.0000, delta+7.7143. `evidence/oracle-before.json`, `evidence/final/oracle-delivered-a6cef89.json`. This is finite source-shape agreement, not desktop health or a global safety score. |
| C1 resource guard, same axis | `python3 -I .ufo/waves/round-21/resource/measure.py --tool tools/mado-tripwire.py --mode module-main` (and separately `--mode cli`): frozen1000/2000/4000 assignments, one child,384MiB/15s. At `eaec245` API4000 fails allocation(exit1), CLI all3 exit2 on stack reservation; at delivered code API3/3 and CLI3/3 are clean, zero findings/unparsed errors. | API RSS KiB before47164/132160/381464(failed) →20292/22852/28904; final CLI29200/31748/38916. Raw `evidence/resource-before-{module-main,cli}.json`, `evidence/final/resource-after-{module-main,cli}-a6cef89.json`. No claim that every call-heavy workload is linear; W2 ResourceMemory remains a named complexity limit. |
| C2 calibration / artifact-assessment capability | Before0 available gate (`git cat-file -e eaec245731926827c72b2fff47cb61afdf5d7c91:tools/mado-assessment.py` exits128, absent). After1 demonstrated gate: `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` gives20/20, including actual wrong-topic red and corrected-subject green; exact N/A mutant now fails1 with named finding. | Capability delta0→1, **no criterion-count or old-axis-score credit**. `evidence/final/assessment-delivered-a6cef89.json`, `assessment-na-a6cef89.json`, `assessment-mutation-a6cef89.json` (digest-check code mutant killed), `assessment-independence-a6cef89.json` (complete C2 stdout byte-identical with baseline-C1/changed-C1/absent-C1). All bind delivered code. Historical22/30 and21/29 remain conditional rejected-round accounting. |

### Removal side and unchanged old expectations

`python3 -I .ufo/waves/round-21/corpus/compare.py --before-tool .ufo/waves/round-21/evidence/tool-before.py --after-tool tools/mado-tripwire.py` uses all1356 committed fixture paths/17,478,844 bytes, manifestSHA `8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377`. Raw counter exits1 with108 error-bearing pairs:86 unchanged malformed/refused records,20 unchanged recursion limits,1 unchanged timeout,1 old allocation failure becoming evaluable. This is not an all-input green run. Zero new error flips;836 retained finding groups,104 added/relabelled,31 removed/relabelled. The authored static adjudication (`evidence/final/corpus-adjudication-a6cef89.json`) classes all31 as10 old false positives removed,19 evidence relabels,2 corrected **kwargs argument vectors; it identifies no lost true prior process finding. That is review evidence, not a malicious-classifier-proof oracle or a private live-session census.

Legacy screens at delivered code remain unchanged populations:11/11 scan/frozen selftest suites,247/247 assertions; r19 frozen_match; r18 expected old frozen_verdict_mismatch; six incident lines still detected. `tw-precision.py a6cef8984d3815775587ab634ce558e13338b0eb` now166/175 under the **unchanged** historic wants(P66/66,S17/17,W21/22,H47/52,L15/18): the old three disagreements persist and six additional disagreements reflect reset-invalidated helper leads and the strict commit/index-write boundary. Never call this175/175 or retroactively admit round20. The old A2 guard at a1e1b608 recorded recall_lost0/crash_flip0/vcs_fn0/a2_mismatch0/dup_rows0, plus two logging false leads; the delivered whole-corpus replay rechecks its exact24 pure inputs against fixture pin6a7d9ca, all hashes match and all24 emit0 findings. Its VCS26-vs20 old-truth disagreements are retained for effect-boundary adjudication, not hidden as a pass.

### Capabilities demonstrated this round

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| artifact-only assessment integrity | Validate declared chronology/order, actual input/expectation hashes, historical rejection disclosure and the four canonical SHONEN subjects, without a C1 dependency; distinguish clean/failed/could-not-evaluate, not authenticate identities or prove evidence sufficiency | `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures`; same C2 output under three C1 intervention states and killed digest-check mutant, receipts above |21|

Claim admission and current outside-lane admit/reject spot-check remain the non-author closure's duty. No exploratory claim, axis retirement, promotion, host recovery or next round is declared. The four fresh residual reviewers inspect these final repairs separately; their eventual findings/dispositions are retained with the report rather than pre-claimed here.

### Final residual disposition — supersedes any improvement/admission reading

**C1: harmed; not admitted.** `residual/FinalBindingReview.md` (current classifier SHA46c82902) reproduces wrong/missing rows with zero unparsed counters for captured-argument lifetime, unresolved-capture global leakage, returned-name rebinding and direct Thread.run; it also demonstrates synthetic-target-name collision. Thus35/35+17/17,247 existing assertions and the authored31-row removal review do not establish the declared binding repair/no-harm claim. Raw red counterexamples are retained. Parent Main explicitly confirmed this honest-stop disposition; no further behavior patch or next round was started.

**C2: improved as a separately demonstrated, bounded capability; round admission remains false.** Its20/20 fixture verdicts, actual wrong-topic/canonical subject pair, exact N/A rejection, code-mutant kill and complete C1-intervention equality are observed and independent. This does not authenticate assertions or evidence sufficiency. The repertoire row above records a working demonstration, **not an admitted capability or rank from a rejected round**. Historical criterion counts remain unchanged as claimed.

Fresh residuals:4 reviewers dispatched,3 completed,1 provider-dead (`FinalAssessmentReview`, Codex capacity error), none replaced; total round154 seats including65+84 validated waves, the inherited MapResiduals scout and these4 residual seats. `FinalRemovalReview.md` found no wrongly excused prior process loss among31 groups, but `FinalEvidenceReview.md` retained source-scope, unparsed-clean labeling and provenance limits. Complete A2 counts are at a1e1b60, not final a6cef89;166/175 remains the delivered legacy comparison. The `--dry` rationales are source/old-manifest-limited, not a newly retained execution receipt. No all-input-green, global precision, no-harm, promotion or host-recovery verdict is granted.

## Round 22 — explicitly authorized recovery registration

Base `741122d177ae8ff68a73768777f20484d5bdcbe4`; full pre-implementation specification:
`.ufo/waves/round-22/registration.md`.

- C1 operability: bounded repair of r21 F1–F5 lifetime/scope/returned-callable/direct-run/hygiene failures, six original fixtures plus independently authored sealed variants; target every eligible frozen expectation and no new true finding loss/error flip on the frozen1356-fixture comparator. No global semantic completeness claim.
- C2 calibration, lowest measured non-retired axis, capability acquisition: independent artifact-only evidence-tier/count audit; actual r19 C3 receipt must fail an observed6/6 assertion and accept only its correct observed5/6 plus lead1/6 scope; independent frozen validity fixtures, code-mutant kill and C1-intervention equality required. No criterion-count credit or retrospective r19 admission.

Scores and before/after outputs are not pre-claimed. Prior red receipts and the three-rejection streak remain in force pending an admitted non-author closure. Authorization is dispatch permission only. No r23.

## Round 22 — first measured facts, not admission

Raw truth seal `9185f1f9806b823a23ef9f5077a893e40e46e1b9` precedes production330de688; normalized fixtures are later materialized at `5c7b98312c2a89f8f59ae9d9f1c83895ed6cd065`. This distinction is explicit, not a claim that the normalized expected.json already existed before implementation.

| Claim / axis | Before → current measured facts | Counting command / revision / limit |
|---|---|---|
| C1 operability, finite independently specified source-shape agreement | baseline46c82902 **13/50** → changed classifier **50/50** new proposals; current full population **57/57**, including six original r21 inputs and r19's exact pure-data negative | `python3 -I .ufo/waves/round-22/oracle/measure.py --tool TOOL --group proposal` before; default full57 after with the proposal subset retained. Receipts `evidence/first/oracle-{before-new50,after-all57}.json`, measured at5c7b983. Local numeric rubric10×proposal passes/50:2.6→10, delta+7.4; not a global skill/no-harm score. |
| C2 calibration, independent evidence-audit capability | before tool absent (exit128); all46 fixed per-case codes/IDs match, but first two complete runner attempts remain could-not-evaluate on audit selftest/envelope defects | `python3 -I .ufo/waves/round-22/audit/measure.py --tool tools/mado-evidence-audit.py --fixtures .ufo/waves/round-22/audit/fixtures`; receipts `audit-after.json` at5c7b983 and `audit-after-corrected.json` ata607f3e. Later code71228fd fixes inventory grammar; no post-fix success is pre-claimed. No criterion-count credit. |

The literal registered unchanged-row historical5/1 green cannot be demonstrated: raw r19 is markerless, and eleven finding rows are not six incident lines. Original raw2 and explicitly derived0/1 cases are separate evidence, not a target-preserving rewrite or retroactive r19 admission. Main's non-author closure grades the actual capability and this strict-target limitation.

Fresh W2 dispatch:100 validated concrete attacks after W1's64; two additional production executor seats died and were not replaced, total166 seats. C1 no-harm, actual gate mutation/intervention and final verdicts remain subject to the recorded final evidence and fresh attacks. Planned: complete only this already-held recovery; no next round is authorized by this scorecard, and prior rejection receipts/streak remain until admitted non-author closure.

### Round 22 — withdrawal and strict target disposition

Final classifier is restored byte-for-byte to v2 `8c7420938369103010b2601f2f78b61a94247a2a` / SHA256cd9da20c; unsafe v3 callback-consumer sweep suppression is withdrawn. Original independent new-proposal measurement remains13/50→50/50 (2.6→10 finite rubric), and the unchanged full primary57/57 plus old35/35+17/17 pass on restored bytes (`evidence/resume/oracle-final.json`, `oracle-r21.json`). This finite score does **not** establish the broader registered no-harm/binding target: supplemental discovery is2/4, caller-frame leakage remains source-supported, and strict **C1 is unprovable/not admitted**. No global operability score or recovered capability is granted.

**C2 strict target is unprovable/not admitted**: unchanged r19 rows cannot satisfy a marker-required5/1 green. The separate bounded artifact audit is demonstrated46/46 named cases (42 distinct pinned case trees), and the actual digest-check code mutant gives44/46, exit1. This records capability availability0→1, not admitted repertoire/promotion credit or retrospective r19 admission. `evidence/resume/audit-final.json`, `audit-digest-mutant.json`; active-path intervention is reported separately after the revision-bound run.

Frozen no-harm evidence is bounded:1356 files,1214 retained finding groups,3 added/5 removed,107 unchanged error pairs, eight reduced unparsed counters, no unequal error pairs. All additions/removals/counter changes are retained and author-adjudicated in `evidence/resume/corpus-adjudication.json`; no all-input-green or independent global no-harm verdict. Eleven unchanged selftests247/247 and both API/CLI assignment and closure resource populations pass within384MiB/15s. All receipts carry exact code/fixture/runner hashes. Planned: close only this already-held r22 honestly; no r23 authorization or streak erasure.

Final bounded C2 intervention at `78b182400b048708a82cfb8b6a7e3bc5459fcc0e`:235/235 command-state runs match full outputs/exits across active-classifier baseline/changed/absent/FIFO/marker states, with sensitive positive controls and unchanged audit/fixture bytes (`evidence/resume/audit-active-path-intervention-final.json`). Initial whole-tree/empty-directory setup failures remain code2 records. Scope is only the staged active path, not universal noninterference. Fresh-clone standalone setup is the three pinned empty-directory recipe in SKILL.md.

Historical precision at `579109a6812f4d0a2dd47572caca241075c6021d`:166/175 unchanged, zero prior passing-case losses (`precision-final.json`, `precision-comparison.json`). Restored production bytes are the exact v2 revision above; C2 auditor SHA256277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca. Strict claim verdicts and original target denominators remain unchanged. No admitted capability row, score inflation, promotion, host recovery or next-round plan is added.

## Round 23 — repair-first recovery: registration, results and author verdicts (2026-10-22)

Registration `.ufo/waves/round-23/registration.md` (landed `6b383c46` before any production edit;
clarifications `a28e4815`, `4de44647` before any after-measurement). Base `e33ea304`. Measured tip
`3732c7a73244fab87558c704107418e5de01436c`; after-values re-derive from committed bytes with the
commands below (classifier extracted with `git show <rev>:tools/mado-tripwire.py`).

| Claim / axis | Before → after | Counting command | Evidence / measured commit |
|---|---|---|---|
| C1 operability, frozen 12-case repair set (repair of rounds[400]/[426] routed harms H3–H5) | 6/12 → **12/12** (local rubric 10 × passes/12: 5.0 → 10.0) | `python3 -I .ufo/waves/round-23/repair/measure.py --tool <extracted classifier>` | `evidence/repair-before-e33ea304.json`, `evidence/repair-after-3732c7a7.json`; classifier `e1dc8029…` at `03227ddf` |
| C2 coverage, sourced routes for the foot, kitty and ghostty trees (learning claim) | 0/3 → **3/3** | `python3 -I .ufo/waves/round-23/c2/count.py REV` (v2) | `evidence/c2-before-v2-e33ea304.json`, `evidence/c2-after-3732c7a7.json`; note at `c8cb3930`, errata `3732c7a7` |
| C3 calibration, SHONEN box 4 versus tracked lane tools without a PROVINCE row | 5 → **0** | `python3 -I .ufo/waves/round-23/c3/count.py REV` (v2) | `evidence/c3-before-v2-e33ea304.json`, `evidence/c3-after-3732c7a7.json`; PROVINCE at `2f1134f3`, correction `3732c7a7` |

No-harm guards for C1 at classifier `e1dc8029…` (`evidence/guards-fix5-scratch.json`, scratch clone of
the lane at that classifier): round-22 supplemental 4/4; round-22 primary 57/57; round-21 oracle
35/35 + 17/17; eleven selftests 247/247; precision 166/175 with the identical passing set; 1356-file
corpus comparator 0 added / 0 removed / 0 error flips, one reduced unparsed counter adjudicated as
a correction; four resource populations clean under 384 MiB / 15 s. Wave-2 base-versus-tip attack
fixtures: zero regressions at `e1dc8029…` (`evidence/attacks-fix5.txt`), after 1 + 13 + 11
regressions found at the first landed classifier `41489991…` and repaired.

Not repaired: H2, precision 172/175 → 166/175 (round 21). Three of the nine failing cases predate
round 21; the other six follow round 21's strict index-write boundary (S118) and reset-cleared lead
adjudication. Restoring them would undo the boundary the round-20 closure required; an L0 question
records the conflict with the repair-first ruling.

Author verdicts (closure decides admission): C1 improved (operability); C2 improved (coverage);
C3 improved (calibration). Other axes unchanged. No exploratory claim, no retirement, no
capability row (the repair is a fix, not a new capability). Probation checklist unchanged: four
`[~]`.

### Planned (round 24; intent only)

Freeze the wave-2 attack fixtures that found regressions (AttackEscapeGate, AttackRecallRegress,
AttackFrameScopes, CritClosureNeighbour) as a registered discovery population before any further
tripwire change; then return to province frontier work (Walker provider behaviour or rule attribution).

### Round 23 — final C1 disposition (append-only; supersedes the C1 row above)

C1 is withdrawn to base bytes. After the table above was written, wave-2 reports still showed
regressions against base at the repaired classifier `e1dc8029…` (AttackLateCell relay case, measured
at `3732c7a7`) and at the first landed classifier (ReClosureNeighbour, seven stored-callable rebind
shapes, measured at `2f1134f3`, not re-measured at `3732c7a7`). A trade is not an improvement, so
`tools/mado-tripwire.py` is restored to `cd9da20c…`; the candidate is kept at
`.ufo/waves/round-23/evidence/candidate-classifier-e1dc8029.py`. **C1 after-value at the landed tip:
6/12 — target 12/12 not met (honest stop).** Author verdict C1: unchanged (no production change).
C2 and C3 stand as recorded. Operability is not harmed: production bytes equal base.

## Round 24 — registration and C2 re-demonstration (2026-10-23)

Registration `.ufo/waves/round-24/registration.md` (landed before any data seat; control receipts in
`.ufo/waves/round-24/controls/`). Base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`. Claims: C1 coverage (Hyprland
window-rule attribution route, counter `python3 -I .ufo/waves/round-24/c1/count.py REV`, v2), C2 calibration
(capability table versus frozen re-demonstration, counter `python3 -I .ufo/waves/round-24/c2/count.py REV`).

### Capability status (round 24 re-demonstration)

Each capability in the tables above was re-run with its frozen command (`.ufo/waves/round-24/c2/manifest.json`,
sha256:`e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`) on the base tree. Status is what the
command did, not what the original row asserted. This table supersedes the implied `works` of every earlier row;
the earlier rows stay as written.

| capability | status | observed evidence |
|---|---|---|
| sources registry | works | census `mado ok`, exit 0 at `8e5d9369` |
| verdict gate (live + file plane) | works | `--no-live` prints a `MADO_VERIFY:` verdict, exit 0 at `8e5d9369`; live layer not exercised |
| hermetic self-test | works | `MADO_SELFTEST: N/N assertions passed`, exit 0 at `8e5d9369` |
| mutation regression with re-cut | works | `MADO_REGRESSION: PASS`, exit 0 at `8e5d9369` (tameshi `mutate-and-run.sh` consumed read-only) |
| post-hoc transcript tripwire | works | four round-17 selftest dirs all `SELFTEST_SUMMARY: n/n`, exit 0 at `8e5d9369` |
| tripwire frozen replay (gate entry) | works | `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`, exit 1 — the replay runs and reports; the mismatch is the frozen verdict, not a replay failure |
| landedness check | works | `LANDED <rev>`, at `8e5d9369` |
| tripwire evidence marker | fails | `tw-precision.py <rev>`: L 15/18 (P 66/66) at `8e5d9369`, not the row's L 17/18 (that was `28c6837`). Two reset-cleared helper leads (`L-CasePureCrossCell-reset-clears-helper`, `L-CaseLeadsInvisible-reset-cleared-helper`) pass at `28c6837` and fail now: round-21 harm H2, still unrepaired (`.ufo/waves/round-24/w1/reports/ScribeC2Evidence.md`) |
| harness fail-closed check | works | six forced setup failures classified, `POSITIVE_CONTROL_OK isolate.sh`, at `8e5d9369` |
| tripwire reached-body sweep | works | `a2-guards.py <rev>`: `recall_lost` 0, at `8e5d9369` |
| detector removal-side guard | works | same `a2-guards.py` run: removal, crash-flip and pure-row counters all 0, at `8e5d9369` |
| artifact-only assessment integrity | works | `mado-assessment.py --selftest`: pass = total, exit 0 at `8e5d9369` |

Scope of the table above (wave-2 correction, append-only; `.ufo/waves/round-24/w2/reports/AtkC2Calibration.md`): the
frozen C2 population is the 12 capability rows under `Capabilities` headings, not every capability row in this file.
Three repertoire rows sit under other headings and are outside the counted population; wave 2 re-ran them once at
`39c59630`: `digest-pinned frozen regression` (round 13) prints `MADO_FROZEN: MATCH`, exit 0; `finite declared-action
classifier` (round 16) prints `SELFTEST_SUMMARY: 52/52 passed`, exit 0; `source-fragment collision screen` (round 13,
line 437 "current exits 0") is **stale**: `MistakeFix.py --registry corpus/SOURCES.md` prints
`MISTAKE_FIX: COLLISION S120 -> S121`, `collisions=4`, exit 1, at base and tip alike (its selftest still passes 25/25).
The sentence "Each capability in the tables above was re-run" is therefore true only of the 12 counted rows. The
collision-screen mismatch is recorded here, not counted, and is routed to a later round.

## Round 24 — results and author verdicts (2026-10-23)

Measured at lane commit `eb14fa3d53d42c1568dd3fe2708c64eaf2024364` (receipts `.ufo/waves/round-24/evidence/c1-after-eb14fa3d.txt`,
`c2-after-eb14fa3d.txt`). Base `8e5d9369`.

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage: frontier "rule attribution" → sourced route (`corpus/knowledge/rule-attribution-r24.md`, S153–S168) | PASS_ROW 0, note absent → PASS_ROW 23/26 from 14 sources, README-indexed, `TARGET_MET` | `python3 -I .ufo/waves/round-24/c1/count.py REV` (v2, sha256:`b2f37c57…efc66`) | target met under the frozen v2 rule; the rule is shown weak (lesson M24-2): 12 of 23 passing rows carry attribution content and a generic-only note also meets it. The closure must judge the note itself. |
| C2 calibration: capability table vs frozen re-demonstration | 1/12 mismatches → 0/12 | `python3 -I .ufo/waves/round-24/c2/count.py REV` (sha256:`a2809501…`, manifest sha256:`e02c76d1…`) | target met over the 12 heading-scoped rows; the predicate wording says "capability table", which literally covers 15 rows — read that way three rows have no command and one (collision screen) is stale (lesson M24-5). |

No-harm at `eb14fa3d`: `tools/` byte-identical to base; round-23 C3 counter 0, round-23 C2 counter 3/3; census exit 0
(the same 7 W04 warnings as at start); removed lines 0 in LOG, SCORECARD, QUALITY, README, SOURCES; PROVINCE, SHONEN,
SKILL unchanged. Not claimed: the calibration literal lesson-citation rubric moves 23/32 = 7.1875 → 26/35 = 7.4286 as a
side effect of the routed QUALITY criteria 33–35; navigation 35/38 → 39/39 rows indexed. No capability row, no
exploratory claim, no retirement; probation checklist unchanged (four `[~]`).

### Planned (round 25; intent only)

Re-cut both counters before data on the M24-2/M24-5 lessons (distinct-sha256 documents and rule-context terms for C1;
full `Capability` population, REV-only meters and `works → fails` harm for C2); route the stale collision-screen row
and H2; harden the two QUALITY checks against the wave-2 survivors.

## Current state (round 25)

C2 of round 25 (calibration, **exploratory**: no counter, no score change claimed; verdict only from a named non-author
reviewer). One place that says, for every capability the file names, what it claims, what a fresh run at one base did,
how to re-run it, and which statement now governs. Base `41cc04c8d593837a0d5078bffaacdaa163d12897` (round-25 base);
each row was re-run by its own wave-a3w1 executor seat in a detached sandbox clone at that base (`timeout 600`,
`prlimit --as=4000000000`), and re-derived independently by a second reviewer seat (wave a3w2 for 14 rows, the
residual call for `:311`); all 15 re-checks agree, with nits only. Receipts: `.ufo/waves/round-25/a3w1/reports/Cap*.md`
(run), `.ufo/waves/round-25/a3w2/reports/Rc*.md` and `.ufo/waves/round-25/a3res/reports/RcMutationRegression311.md`
(re-check).

Population (enumerated from the base blob without a case-sensitive header filter; a3w1 `CritC2Ledger.md`): 15
capability identities in 9 tables whose first header cell is `Capability` (rows `:308-311`, `:437-438`, `:782`, `:919`,
`:1020`, `:1158`, `:1342-1343`, `:1409-1410`, `:1464`; a tenth such table, `:202`, holds only the `— none yet —`
placeholder `:204`), plus 12 repeated
status rows in the round-24 table (`| capability | status | observed evidence |`, `:1575-1586`), mapped below as the
earlier governing statement. Line numbers are at the base blob; this round inserted 5-line pointer paragraphs after
`:438` and after `:1343` (repair R6), so at this revision `:1342-1343` read `:1347-1348` and rows after them shift by 10.

| base row | capability | stated (abbreviated) | observed at `41cc04c8` (fresh run) | command (cwd = clone at base) | governs now |
|---|---|---|---|---|---|
| `:308` | sources registry | registry rows; every census command clean; mined rows join citing entries | works: `validate` `mado ok`, exit 0, 0 E-codes, 7 W04; 168 rows (row says 39: round-12 count) | `scripts/sources-census.sh validate --root <root>` | this row; r24 `:1575` agrees |
| `:309` | verdict gate (live + file plane) | read-only verdict over config plane and live hyprctl, exit 0/1/2 | works: `MADO_VERIFY: CLEAN (53 pass, 7 notes; file + live planes verified read-only)`, exit 0; usage exit 2; empty root exit 1 | `bash tools/mado-verify.sh` | this row; r24 `:1576` ran `--no-live` only — the live arm now observed |
| `:310` | hermetic self-test | 269 assertions over isolated fixtures | works: `MADO_SELFTEST: 460/460`, exit 0 (row's 269 is the round-12 count) | `bash tools/mado-verify.sh --selftest` | this row; r24 `:1577`; hermeticity caveat `:1179-1181` (two non-reproducible fixture-loss failures under concurrent runs) |
| `:311` | mutation regression with re-cut | 10-defect kill table vs derived target; SETUP + printed re-cut on a moved gate | works: `MADO_REGRESSION: PASS`, 10/10 killed, exit 0; pin-flipped copy SETUP exit 2, printed re-cut re-run 10/10 exit 0 | `MADO_VERIFY_HARNESS=<tameshi>/tools/mutate-and-run.sh bash tools/mado-verify.sh --regression` | this row; r24 `:1578` |
| `:437` | source-fragment collision screen | stop repeated active canonical URL; "current exits 0" | **fails as stated**: selftest 25/25 exit 0; historical registry exit 1 (S017→S030); current `corpus/SOURCES.md` exit 1, `collisions=4` | `python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md` | this ledger; pointer after the row (R6) |
| `:438` | digest-pinned frozen regression | verify gate/harness digests before replay; refuse tamper | works: `MADO_FROZEN: MATCH`, exit 0; selftest 12/12; one appended byte → `snapshot_tampered` exit 2 | `python3 .ufo/waves/round-13/frozen/verify.py` | this row |
| `:782` | finite declared-action classifier | refuse blocked kinds, 12 pinned argv[0] names, malformed input; frozen replay | works: selftest 52/52 exit 0; `--frozen` `frozen_match` exit 0; red plan exit 1, green plan exit 0 | `python3 -I tools/mado-action-plan.py --selftest` / `--frozen .ufo/waves/round-16/frozen` | this row |
| `:919` | post-hoc transcript tripwire | classify OMP JSONL commands into three classes, exit 0/1/2 | works, **command not runnable as written** (brace form exits 2: `--selftest` takes one DIR); per-dir 9/9, 16/16, 33/33, 30/30 exit 0 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/<dir>` per dir | this row; r24 `:1579` |
| `:1020` | tripwire frozen replay (gate entry) | verify digests, compare verdict with pinned expectation | works as designed, exit 1: `frozen_verdict_mismatch` (5/5 digests ok, 3 extra findings the r18 pin predates); tamper exit 2; r19 pin `frozen_match` exit 0 | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` | r24 `:1580`; an exit-0 reading of this row is wrong |
| `:1158` | landedness check | cited hash ancestor of live remote tip, no fetch/write | works: `LANDED` exit 0; `LOCAL_ONLY`/`MISSING` exit 1; non-hex exit 2 (remote tip observed at run time) | `bash .ufo/waves/round-19/landed-check.sh <lane> <hash>…` | this row; r24 `:1581` |
| `:1342` | tripwire evidence marker | observed vs lead on every finding row; drop pure data | **fails**: at base P 66/66 but L 15/18 (three lead cases give no finding); the row's literal command pins `28c6837` (L 17/18, historical) | `python3 -I .ufo/waves/round-20/tw-precision.py 41cc04c8` | r24 `:1582` (fails); pointer after the row (R6) |
| `:1343` | harness fail-closed check | payload never runs after any of six forced setup failures | works: six `FAIL_CLOSED`, positive control OK, exit 0 (`HARNESS` placeholder resolved to `.ufo/waves/round-20/isolate.sh`) | `bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/isolate.sh` | this row; r24 `:1583` |
| `:1409` | tripwire reached-body sweep | unfollowed reachable bodies reported as leads | works with the present tool: `recall_lost 0`, `crash_flip 0`, exit 0; at the row's own revision `a8960de` one `MemoryError` crash flip under the 4 GB cap (memory-contingent) | `python3 .ufo/waves/round-20/a2/a2-guards.py 41cc04c8 --fixtures-rev 6a7d9ca` (present tool) and `… a8960de …` (row's revision) | this row; r24 `:1584`; harm context `:1412-1420` |
| `:1410` | detector removal-side guard | count findings dropped, crash flips, pure-data rows | works: all guarded counters 0 at base, exit 0; before receipt `28c6837` reproduces `recall_lost 52` | `python3 -I .ufo/waves/round-20/a2/a2-guards.py 41cc04c8 --fixtures-rev 6a7d9ca` | this row; r24 `:1585` |
| `:1464` | artifact-only assessment integrity | chronology, hashes, rejection disclosure, four SHONEN subjects without C1 | works: selftest `pass=20 total=20`, exit 0, two runs byte-identical | `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` | this row; r24 `:1586` |

Read this way: 13 of 15 capabilities work at base; `:437` and `:1342` fail as stated (both already known, now with
pointers at their rows); four rows carry documentation defects a reader would trip on (`:919` command not runnable as
written, `:1343` placeholder argument, `:1020` exits 1 by design, `:310`/`:308` stale counts). Not claimed: any score
change, admission or restored capability. This section is bookkeeping for the next reader; the C2 verdict is the
non-author reviewer's.

## Round 25 — results and author verdicts (2026-10-23)

Registration `.ufo/waves/round-25/registration.md` (sections "Attempt 3" and "after the control receipts"). Base
`41cc04c8d593837a0d5078bffaacdaa163d12897`. C1 measured at lane commit `ef94763c6a75d1b0860091b19bb61c9bd7cda9e3`
(receipt `.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt`, one run, seed `ed0d8a943980d2f2`).

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 operability, capability acquisition (sourced): static Hyprland v0.56.2 bind-table resolver `tools/mado-binds.py` | `41cc04c8`: `tool=MISSING_TOOL`, `PRED-C1 (v4) cases_pass=0/41`, exit 1 → `ef94763c`: `cases_pass=41/41 embed_hits=0 verdict=TARGET_MET`, exit 0 | `python3 -I .ufo/waves/round-25/c1/count.py REV` (v4, sha256:`323a3849…42e2`; generator `count-v3.py` sha256:`8532d3e9…8375`) | target met under the frozen v4 rule; controls (10 shapes, landed `459dd17f` before data) best 37/41; v1 33/33, v2 37/37, v3 41/41 reported, not substituted |
| C2 calibration, exploratory: `## Current state (round 25)` ledger | no single present-tense place; round-24 status table covered 12 of 15 identities and ran `:309` `--no-live` only → 15 identities, each run fresh at base and re-derived by a second seat | none (exploratory) | judged by the named non-author reviewer (round report) |

### Capabilities (round 25)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| static bind-table resolver | Print, from config bytes only, the bind table Hyprland v0.56.2 would build from a hyprlang config tree (source graph, variables, comments, bind grammar, unbind), as the 18-field `hyprctl binds -j` array | `python3 -I tools/mado-binds.py --home DIR`; measured `python3 -I .ufo/waves/round-25/c1/count.py ef94763c` → 41/41 against Hyprland's own tables (`evidence/c1-after-v4-ef94763c.txt`) | 25 |

Scope limits found after data (residual call, not the predicate): `{{…}}` arithmetic expressions are evaluated by
Hyprland and left literal by the tool (`.ufo/waves/round-25/a3res/reports/ResC1Remeasure.md`, 9/10 hand-made trees
agree); binds created at runtime by exec'd commands are outside any static reading. Harm watch: at the measured commit
the round-23 C3 inventory counter read 1 (the PROVINCE row for the new tool landed in the next commit, `90224671`,
because the registration made that row depend on the measurement); it reads 0 from `90224671` on.

### Round 25 — C2 ledger errata after the non-author judgment (append-only; the ledger above is the judged object)

The named non-author reviewer (`.ufo/waves/round-25/a3res/reports/RevC2Judgment.md`) judged the ledger
`unprovable-but-better` and listed five errors; they are corrected here, not in the ledger rows:

- F1: the ledger's receipt sentence is wrong twice. As first written it said every row was re-derived by a wave-a3w2
  seat; while the review was running the author changed it to "wave a3w2 for 14 rows, the residual call for `:311`;
  all 15 re-checks agree". Both are false: a3w2 re-derived 12 rows (`:308`, `:309`, `:310`, `:437`, `:438`, `:782`,
  `:919`, `:1020`, `:1158`, `:1342`, `:1343`, `:1464`), the residual call re-derived `:311`, and `:1409` and `:1410`
  have one run each (a3w1 only). The results-table row above ("each run fresh at base and re-derived by a second
  seat") inherits the same error: 13 of 15 rows were re-derived.
- F2: row `:308`'s command is the fleet script `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
  --root <census root>`, not a lane-relative `scripts/sources-census.sh` (absent at base).
- F3: the R6 pointers added 5 lines after `:438` and 4 after `:1343`, so rows after `:1343` shift by 9, not 10.
- F4: row `:1158`'s `LANDED` verdicts depend on the remote tip observed at run time (`2896dc4a` for a3w1, `fa466833`
  for the a3w2 re-check); verdicts were equal at both.
- F5: row `:1410`'s "all guarded counters 0" leaves out `vcs_fp 26`, which the row's own receipt scopes out of the
  guard.

## Round 26 — results and author verdicts (2026-10-23)

Registration `.ufo/waves/round-26/registration.md` (C1 rule: section "C1 redesign before data: counter v2"). Base
`96101be523b2f6e897eee743d5b396b0225bf9ed`. Every expected value comes from Hyprland v0.56.2 itself in a headless,
session-isolated nested instance (`.ufo/waves/round-26/harness/oracle.py`; pilot `harness/pilot-receipt.txt`).

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage (sourced: S175–S177, S158, S162): the animation directive→entry expansion (`hyprctl animations -j`), held as `[INF]` at `corpus/knowledge/hyprctl-verification-layer.md:158`, becomes a measured tool `tools/mado-anims.py` + note `corpus/knowledge/animation-table-r26.md` | `96101be5`: `tool=MISSING_TOOL`, 0/41 (v1 receipt `evidence/c1-before-96101be5.txt`; v2 controls best 9/41) → `2b3487f7`: `PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET`, exit 0 (`evidence/c1-after-v2-2b3487f7.txt`, seed `4408656415ee7578`) | `python3 -I .ufo/waves/round-26/c1/count-v2.py REV` (sha256 `4ed70b54…6428`) | target met under the frozen v2 rule; controls (9 shapes, landed `1b0b91e9` before data) best 9/41 (w2 re-scores ≤13/41) |
| C2 operability: `tools/mado-binds.py` works on trees whose binds/variables use hyprlang `{{…}}` expressions, keeping round-25 behaviour on the 20-case V3 sample | `96101be5` (round-25 tool): `cases_pass=22/51` (`evidence/c2-before-96101be5.txt`) → `a496b02a`: `PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET`, exit 0 (`evidence/c2-after-a496b02a.txt`, seed `629fd25ee94fb42a`) | `python3 -I .ufo/waves/round-26/c2/count.py REV` (sha256 `b92c32da…16a8`) | target met; controls (6 shapes) best 24/51 |

Population check (QUALITY 37): `python3 -I .ufo/waves/round-26/quality/check-population.py --registration
.ufo/waves/round-26/registration.md` on both after-receipts → `POPULATION verdict=PASS`, exit 0. Evidence (landed round 27, `evidence/r26-population-after.txt`, sha256 `faf6df7e…23f98`): the sentence holds only because the registration at its commit already carried the C2-v2 paragraph — with the pre-v2 registration at `05319e0` the same two receipts give `verdict=FAIL`, exit 1 (hidden-dependency probe).

### Capabilities (round 26)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| static animation-table resolver | Print, from config bytes only, the `[nodes, beziers]` table Hyprland v0.56.2 would report (`hyprctl animations -j`) for a hyprlang config tree | `python3 -I tools/mado-anims.py --home DIR`; measured `count-v2.py 2b3487f7` → 41/41 against Hyprland's own tables | 26 |
| isolated Hyprland oracle | Run Hyprland v0.56.2 headless under a private tinywl in bubblewrap and read any `hyprctl -j` verb, with no contact with the live session | `python3 harness/pilot.py` (`harness/pilot-receipt.txt`: ISOLATED_OK, coredumps 1335→1335); w1 IsolationProbe 770/770 samples private | 26 |

Ledger repair (round-25 routed defect 7): rows `:1409`/`:1410` of `## Current state (round 25)` are now second-derived
(w1 Rc1409, Rc1410; reviewed by w2 ReviewRc): both agree; `:1410` holds under errata F5's scoping (`vcs_fp 26` outside
the guard).

Harm watch: `git diff --stat 96101be5 -- tools/` touches only `tools/mado-anims.py` (new) and `tools/mado-binds.py`
(C2; its round-25 behaviour is the counter's V3 half, 20/20 + BASE). Census `validate` exit 0 at start and end (rows
172 → 177). Host: Hyprland coredump records 1330 → 1338 this round (5 failed pilots, 3 seat probes; every counter
receipt delta 0) — lesson M26-1/M26-2/M26-6.

### Planned (round 27; intent only)

Successor harness (bwrap under `env -i`, symlink-safe snapshot, resource bounds); gate-check fixtures for the
surviving self-test/Q37/Q36 mutants; candidate frontier move: window/workspace rules tables (`hyprctl workspacerules
-j`) through the same oracle.

## Round 27 — results and author verdicts (2026-10-23, attempt 2)

Registration `.ufo/waves/round-27/registration.md` (frozen before any control or data seat; C1 rule chain v1→v4 retired pre-data under the kill rule, C2 counter v2). Base `543f0445e9d60bdfa026c54772d29e8b96bc844b`. Attempt 1 (phase-4 orchestrator) committed counters, controls, sealed H, and both C2 suites, then died before data; attempt 2 inherited, landed data, measured. Expected values come from Hyprland v0.56.2 itself in the isolated oracle (`harness/oracle.py`, coredump delta 0 on every receipt).

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage (sourced: S178–S182, S158, S162): the workspace-rule table (`hyprctl workspacerules -j`) becomes a measured lane tool `tools/mado-wsrules.py` + note `corpus/knowledge/workspace-rules-r27.md`; no lane tool or note derived it at base (`git grep -n -i "workspacerules\|workspace rule" 543f0445 -- tools corpus/knowledge` finds only verb mentions) | `543f0445`: `tool=MISSING_TOOL`, 0/41 (`evidence/c1v4-before-543f0445.txt`) → `20022a65`: `PRED-C1-r27-v4 cases_pass=41/41 verdict=TARGET_MET`, exit 0 (`evidence/c1-after-20022a65.txt`, official seed `4cfdf858277ad362`); 13 v4 controls best 32/41 (FileScope, `controls/v4/`) | `python3 -I .ufo/waves/round-27/c1/count-v4.py REV [--seed HEX] --jobs 6` (sha256 `635ae788…71a1`) | target met under the frozen v4 rule. Data rule: two independent builds; ExecWsToolA died mid-flight unreturned (its inherited bytes piloted 19/41, `evidence/c1-after-48b9434a.txt`, ONEMPTY cluster), ExecWsToolC returned and its bytes landed unmodified (`dcf5c8c0…a389`); provenance audit PROVENANCE_OK (w3 RevProvenance); 3/3 tool-level mutants killed on the 13-tree oracle probes (w3 MutWsTool) |
| C2 operability: the lane's two offline gates (`quality/counter-selftest.py`, `quality/population-suite.py`) fail when their subjects are broken | `543f0445`: suites missing, `green=0/8 w_killed=0/15` (`evidence/c2v2-before-543f0445.txt`) → measurement 1 at `48b9434a` (suites from ExecSuiteA1/B2 first-returned bytes): green=17/17, w_killed=15/15, h_killed=12/18 vs h_need=14, `verdict=TARGET_MISSED` (`evidence/c2-after-48b9434a.txt`); three named survivors (HeldC2-extra-disjunction, -unstable-conjunction, -embed-boundary). Registration repair flow: w4 seats built own class mutants from the public names (sealed H never read), ExecRepairA2's repair returned first and landed unmodified at `0b53bd86`; measurement 2: green=17/17, w_killed=15/15, h_killed=15/18 vs h_need=14, `verdict=TARGET_MET`, exit 0 (`evidence/c2-after-0b53bd86.txt`) | `python3 -I .ufo/waves/round-27/c2/count-v2.py REV --heldout /fast/scratch/hyaku/mado-r27/heldout --seal .ufo/waves/round-27/c2/heldout-seal.txt` (sha256 `4dfb34b5…09d3`) | target met at the final REV under the frozen v2 rule (the REV-parametric predicate at `0b53bd86`); measurement-1 miss retained as evidence; residuals: 3 surviving held-c1v2 rows (c1-counter subject) and H-set rotation advice (w3 CritC2Claim) routed |

Population check (QUALITY 37): `python3 -I .ufo/waves/round-26/quality/check-population.py --registration .ufo/waves/round-27/registration.md .ufo/waves/round-27/evidence/c1-after-20022a65.txt` → exit 2 UNREADABLE — the checker parses only distinct numeric totals and PRED-C2-r27(-v2) states open-ended targets (`green=all`, ratios); not a population mismatch (routed: extend Q37 for ratio/all targets). The C1 receipt's own counts are internally consistent: 41 CASE lines against the registered 41-case total.

### §6.6 erratum (round 29)

The round-27 report and this section's C1 row say "the tool's docstring and the
knowledge entry cite them [S178–S182]". The round-27 verifier spotcheck item 6
(`corpus/lessons/round-27-verifier-spotcheck.md`) found the sentence overclaims:
`tools/mado-wsrules.py`'s docstring cites the upstream source files
(`src/config/legacy/ConfigManager.cpp`, `src/config/shared/workspace/WorkspaceRuleManager.cpp`,
`ParserUtils.cpp`, …) — not `S###` ids; only `corpus/knowledge/workspace-rules-r27.md`'s
frontmatter cites the S178–S182 rows. Correction: the S### citation lives in the
knowledge entry frontmatter; the docstring citation is upstream-file-level. This was
the tenth routed record defect (r28 spotcheck's routed queue item 4); repaired here
append-only. No tool byte changes (the docstring's upstream citations stand as
source-level provenance).

### Capabilities (round 27)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| static workspace-rule table resolver | Print, from config bytes only, the JSON table Hyprland v0.56.2 reports (`hyprctl workspacerules -j`) for a hyprlang config tree (sources, variables with redefinition, `{{…}}`, merge-in-place, gaps shorthand, parseInt bools, on-created-empty) | `python3 -I tools/mado-wsrules.py --home DIR`; measured `count-v4.py 20022a65` → 41/41 against Hyprland's own tables; `python3 -I tools/mado-wsrules.py --home ~` matches live `hyprctl workspacerules -j` (closure re-derivable) | 27 |

Harm watch: `git diff --stat 543f0445 -- tools/` touches only `tools/mado-wsrules.py` (new); suites/repairs touch only `quality/`. Census `validate` exit 0 at end (rows 177 → 182; W04 duplicate-url warnings unchanged from round 26). Host: Hyprland coredump records 1338 → 1338 across both measurements and all w3/w4 seat probes (every receipt `HOST_SAFETY delta=0`).

### Planned (round 28; intent only)

C2 residual: H-set rotation on re-measurement (w3 CritC2Claim) and the two Q36-successor survivors (glob-case, marker-case, w2 MutQ36Successor); the ExactBool blind spot noted by w3 CritC1Claim (counter BOOLWORD values are exact words; the 13-tree `bools` probe is the discriminator); suite-A sandbox residuals (output-flood DoS, `.git` metadata leak, w3 CritC2Claim).

## Round 28 — record repairs

### round-27 harm-watch erratum

The false round-27 claim is at `SCORECARD.md:1767`:

> “Harm watch: `git diff --stat 543f0445 -- tools/` touches only `tools/mado-wsrules.py` (new); suites/repairs touch only `quality/`.”

At the lane tip, the tools diff instead reports:

```text
 tools/mado-binds.py   |   6 +
 tools/mado-wsrules.py | 851 ++++++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 857 insertions(+)
```

`git show b6650d583924d670c9e98594ffb1c6f25e8e7682 -- tools/mado-binds.py` shows this docstring hunk:

```diff
commit b6650d583924d670c9e98594ffb1c6f25e8e7682
+Environment limit (round-27 note, M26-10): environment variables are not imported into the
+config variable table, unlike hyprlang v0.6.8, which seeds variables from the process
+environment.  A `$NAME` supplied only by the environment stays literal, and `source = $VAR`
+using only an environment value is not followed.  Variables defined in the config tree are
+still expanded.
+
```

Classification: an introduced docstring/contract change was unrecorded by the harm watch. It makes no behavior change; the omission is an S3 record defect.

Correction: the `543f0445e9d60bdfa026c54772d29e8b96bc844b` → `4f610066efd90804b055c42ae20c41a7f44404f9` `tools/` diff changes both `tools/mado-wsrules.py` (new) and `tools/mado-binds.py` (six added docstring lines). The harm watch must include the latter's environment-limit note as a docstring-only change, not a behavior change.

## Round 28 — results and author verdicts (2026-10-24, attempt 1 after stale-claim reset; completing attempt)

Frozen registration `.ufo/waves/round-28/registration.md` (b84348d; counters hardened 123d8cd; pre-data controls K1*/K2 committed). Two claims: C1 operability (sourced S183, six-leg composite PRED-C1-r28), C2 calibration (nine-condition record audit PRED-C2-r28). This attempt inherited seven dead attempts' committed work (tip 317ff19) and completed measurement, the refpub leg, environment restoration, and the records. Waves: w1 39 seats (one batched dispatch), w1b 32 (registry, 0 reports), w2 34 (one batched task call, w2-run.json); 105 seats total.

### C2 — calibration (lowest active scored axis): committed measurements and author verdict

| Before → after | Counting command | Verdict |
|---|---|---|
| 1/9 conditions pass, `verdict=TARGET_MISSED` exit 1 (K2DoNothing control at the registration commit, `controls/K2DoNothing.txt`) → 9/9 `CHECK D1..D9 PASS`, `PRED-C2-r28 verdict=TARGET_MET` exit 0 at 77cdda86 | `python3 -I .ufo/waves/round-28/c2/count.py REV` — before receipt `evidence/` absent at registration, control `controls/K2DoNothing.txt`; after receipt `.ufo/waves/round-28/evidence/c2-after-77cdda86.txt` | locally verified improved (bounded): eight unresolved record conditions repaired in a frozen nine-condition audit, D9 retained (it passed pre-round at dac4aef — not an r28 gain); the lesson-citation rubric 26/35 is NOT re-scored by this claim (CritCalibration advisory §3) |

Honest residual: the round-27 spotcheck routed **ten** record defects; the frozen population measures nine. The omitted item (§6.6: report overclaims that the wsrules docstring cites S178–S182) is real and unclaimed — see RevengerNineDefects.md cross-cutting; carried to round 29 intent. C1/C2 share the D4/q36 witness artifact (CritCalibration §4) — disclosed, not independent.

### C1 — operability (sourced S183): per-leg results and author verdict

Command: `python3 -I .ufo/waves/round-28/c1/count.py REV` (composite, sha256 dcca084f…). Before: all six legs FAIL at 123d8cd (`evidence/c1-before.txt`). After at 77cdda86 — full vector, committed verbatim in `evidence/c1-after-77cdda86.txt`:

| Leg | Result at 77cdda86 | Basis |
|---|---|---|
| h1-rotation | composite FAIL rc=2 no-tally (H1 dir absent at closure) | after-state verified by committed w2 receipt `.ufo/waves/round-28/w2/reports/ReviewerSuiteMonotone.md`: new suite `h_killed=18/18 verdict=TARGET_MET`, green 17/17, w 15/15, exactly the three `held-c1v2` survivors flip SURVIVED→KILLED, monotone. H1 dependency was declared in the registration ("Leg 1 alone depends on the inherited ephemeral H1 directory"); `/fast/scratch/hyaku/mado-r27/heldout` was cleaned before closure |
| boolword-v5 | composite FAIL "normal=missing mutant=missing" — frozen guard pins count-v4.py at `3d7d301f…` vs committed `635ae788…` (pin never matched: verified at freeze 5198cc8 and r27 tip 20022a65) | leg's declared commands verified live at 77cdda86: `count-v5.py 77cdda86 --seed 28c1a8c0ffee0001` → `cases_pass=41/41 boolword_pass=2/2 verdict=TARGET_MET` exit 0; with `--tool-file ref-mutants/exactbool-tool.py` → `boolword_pass=0/2 verdict=TARGET_MISSED` exit 1. Oracle restored by byte-identical tinywl rebuild (both sha256 pins matched; `.ufo/waves/round-26/harness/build-tinywl.sh`; HOST_SAFETY coredumps 1338→1338) |
| h2-rotate | PASS seal-at-rev=True rc=0 TARGET_MET | committed H2 + seal at tip, frozen round-27 counter |
| refpub-kills | PASS seal-at-rev=True rc=0 `h_killed=12/12 h_valid=12 h_min_per_subject=4` | public reference set authored this attempt from the three committed public subjects (4 mutants + 2 benign rows each), sealed `c1/refpub-seal.txt`, scored by the frozen counter (receipt in run output; first draft's comment-only benign rows were AST-invalid and one anchor-class mutant survived — both iterated and caught by the counter itself) |
| q36-witness | PASS rc=0 names=True | committed runner + regenerated receipts (`quality/q36-successor-receipts.txt`, Q36WITNESS rows=4 failed=0) |
| q37-open-ended | PASS rc=0 r26sha=803e0096c994 | `quality/check-population.py` open-ended targets; frozen round-26 artifact untouched |

Composite at 77cdda86 prints `PRED-C1-r28 verdict=TARGET_MISSED` exit 1 — reported verbatim. Author verdict: **improved on committed evidence, with two declared/evidenced boundaries** — every leg's frozen predicate holds on committed bytes or committed receipts; the AND-bit is blocked by (a) the registration's own declared ephemeral-H1 boundary (environment cleaned pre-closure) and (b) a frozen-counter guard defect (v4 pin never matched; composite was never smoke-run before freeze). Both are reported for the operator; no leg's rule was changed after data.

### Harm watch and limits

`git diff --stat 317ff19..77cdda86` touches only `.ufo/waves/round-28/c1/{refpub,refpub-seal.txt}` and `quality/q36-successor-receipts.txt` — no `tools/`, no compositor/config writes, no sibling-lane writes. Census validate exit 0 start (182 rows) → end (183 rows, +S183); W04 duplicate-url warnings unchanged. Suicide/bystander check: Hyprland coredumps 1338→1338 on every oracle run this attempt. Bound: finite offline suites; no live-health or whole-domain operability claimed. Coverage U-route stays a harm watch; no U-item moved.

### Capabilities (round 28)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| rotating held-out mutation gate | Rotate and score a sealed held-out mutant set against the committed offline suites with the frozen counter (H2 rotated in-round; first public reference set scored 12/12) | `count-v2.py 77cdda86 --heldout .ufo/waves/round-28/c2/heldout2 …` TARGET_MET; refpub run 12/12 in `evidence/c1-after-77cdda86.txt` context; w2-run.json | 28 |

### Sources, saturation, planned

Sources 182 → 183 (A 175 → 176; mined 163 → 164; rejected 9; +S183 mined by `corpus/knowledge/mutation-testing-r28.md`, opened 2026-10-23, gate quote in lesson `## Gate`). Saturation 9.0 / N=3 unchanged; retired: none. Planned (round 29; intent only): new pre-data registration to fix the composite's count-v4 guard pin and re-run a smoke pass at freeze; the spotcheck §6.6 tenth record defect; ephemeral-input preservation policy (L0 question open).

## Round 29 — results and author verdicts (2026-10-24, attempt 1)

Registration `.ufo/waves/round-29/registration.md`, frozen `aeb4f58b`, re-frozen `3ae437ca`
(QUALITY-38 smoke caught the composite's stale `c1-r28` self-print label; fixed, re-frozen,
re-smoked; both receipts committed). Base `f652ca99` (round-28 closure: rejected-honest-stop;
the r28 records and its missed `PRED-C1-r28` stand untouched — this round registers new
predicates on repaired counters, never rewrites frozen bytes). Both claims verify at the
data commit `cb4e1c00`; receipts `.ufo/waves/round-29/evidence/c1-after-cb4e1c00.txt` and
`c2-after-cb4e1c00.txt`.

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 operability (sourced: S184 for the refpub/equivalent-mutant method): the round-28 six-leg composite is repaired — count-v4 guard pin `3d7d301f…` → committed `635ae788…71a1` (M28-1), leg h1 re-based per QUALITY 39 to the committed receipt `ReviewerSuiteMonotone.md` (M28-2) — and re-frozen with a freeze smoke run (QUALITY 38) | base `f652ca99`: `LEG boolword-v5 FAIL normal=missing mutant=missing`, `LEG h1-rotation FAIL rc=2 no-tally`, `PRED-C1-r28 verdict=TARGET_MISSED` exit 1 (`evidence/c1-before-f652ca99.txt`) → `cb4e1c00`: `LEG h1-receipt PASS`, `LEG boolword-v5 PASS normal=41/41 mutant=0/2`, all six legs PASS, `PRED-C1-r29 verdict=TARGET_MET` exit 0 (`evidence/c1-after-cb4e1c00.txt`); freeze smokes green at `aeb4f58b` and `3ae437ca` | `python3 -I .ufo/waves/round-29/c1/count.py REV` (counter sha256 `4fa91407…a3829`) | target met under the frozen rule; controls C1K1 (unrepaired r28 composite) and C1K2 (pin-only, h1 ephemeral) both MISS as registered (`controls/C1K1-r28composite.txt`, `controls/C1K2-pinonly.txt`) |
| C2 calibration (lowest active scored axis): the four round-28-closure routed defects are repaired in committed records — R1 guard-pin repair with red-before control, R2 ephemeral-input policy named at data time (QUALITY 39), R3 standalone v5 receipts committed, R4 §6.6 tenth-record erratum | base `f652ca99`: `CHECK R1..R4 FAIL`, `PRED-C2-r29 verdict=TARGET_MISSED` exit 1 (`controls/C2K1-donothing.txt`) → `cb4e1c00`: `CHECK R1..R4 PASS`, `PRED-C2-r29 verdict=TARGET_MET` exit 0 (`evidence/c2-after-cb4e1c00.txt`) | `python3 -I .ufo/waves/round-29/c2/count.py REV` | target met; each fix shown able to fail (R4 red: `CHECK R4 FAIL` at the do-nothing control; R3 red: `R3 FAIL` at freeze) |

Harm watch at `cb4e1c00`: `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460
assertions passed`, exit 0; census validate exit 0 (183 → 184 rows, +S184); `git diff --stat
f652ca99 cb4e1c00 -- tools/ corpus/knowledge/ SKILL.md PROVINCE.md quality/` touches no
tools/knowledge/skill bytes (SCORECARD/LOG/SOURCES/lessons + `.ufo/waves/round-29/` only);
no compositor/config mutation; every oracle receipt `HOST_SAFETY` coredumps 1338→1338.
Inherited finding, recorded not repaired (claim discipline): the navigation counter reads
41/43 at base and tip alike — `mutation-testing-r28.md` and `workspace-rules-r27.md` are
absent from `corpus/README.md` index rows (r27/r28 debt); routed to round 30. Calibration
lesson-citation rubric NOT re-scored by C2 (its four checks are routed repairs, not new
criteria); bounded scores unchanged this round.

### Capabilities (round 29)

No new capability row: the repaired composite re-demonstrates the round-28 "rotating
held-out mutation gate" (its row stands); the round's work is repair, not new repertoire.
The r29 composite runs end-to-end from committed bytes — recorded in the C1 row, not
pre-claimed as a capability.

### Sources, saturation, planned

Sources 183 → 184 (A 176 → 177; mined 164 → 165; queued 10; rejected 9; +S184 mined by
`.ufo/waves/round-29/registration.md` and `corpus/lessons/round-29.md`, opened 2026-10-24,
gate quote in the lesson). Saturation 9.0 / N=3 unchanged; retired: none. Planned
(round 30; intent only): the inherited navigation gap (41/43 — index the two missing
notes); re-dispatch the prepared wave-1 (33 seats, plan exit 0) if the operator lands the
route bindings; any operator ruling on the two answered-by-implementation L0 questions.

## Round 30 — results and author verdicts (2026-10-24, attempt 1)

Registration `.ufo/waves/round-30/registration.md` frozen `451e8b3c` (controls
and before-receipts committed pre-data; freeze smoke
`evidence/freeze-smoke-451e8b3c.txt` ran all three counters at the freeze).
Base `8f51071b` (round-29 closure: admitted; index gap routed). Data commit
`446dc396`. Axis selection re-derived every scored sub-axis at base
(criterion 22): calibration literal 0.7000 / resolved-active 0.7949 is
lowest; coverage-nav 0.9535; sourced-art and operability 1.0.

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage / admitted-note reachability (routed defect; sourced S185): index rows for `workspace-rules-r27.md`, `mutation-testing-r28.md` | `8f51071b`: `indexed=41/43 missing=2` exit 1 (`evidence/c1-before-8f51071b.txt`) → `446dc396`: `indexed=43/43 missing=0 dangling=0 duplicates=0` exit 0 (`evidence/c1-after-446dc396.txt`) | frozen literal fence (S185; the SCORECARD "Counting command" block) run at REV | target met; K1 do-nothing at base stays red |
| C2 calibration / lesson-grounded admission criteria (lowest scored axis): every active QUALITY criterion resolves a `lessons/` citation | `8f51071b`: literal 28/40, resolved-active 31/39, UNRESOLVED {1..5,38..40}, `PRED-C2-r30 verdict=TARGET_MISSED` exit 1 (`controls/C2K1-donothing.txt`) → `446dc396`: literal 40/52, resolved-active 40/40 = 1.0000, TARGET_MET exit 0 (`evidence/c2-after-446dc396.txt`); superseded {1-5,18-20,32,38-40} excluded per criterion 21→20 precedent | `python3 -I .ufo/waves/round-30/c2/count.py REV` | target met; K2 do-nothing names the 8 unresolved base criteria |
| C3 operability, capability acquisition (sourced S185): `quality/check-index.py` index-completeness gate | absent at base → at `446dc396`: gate prints `indexed=41/43` exit 1 at base rev, `indexed=43/43` exit 0 at tip, `MADO_INDEX_SELFTEST: 6/6` exit 0 (`evidence/c3-after-446dc396.txt`) | `python3 -I quality/check-index.py --rev REV --repo .` / `--selftest` | target met; K3: gate is red at base (cannot be vacuous) |

### Capabilities (round 30)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| index-completeness gate | Score the coverage map's index rows against `corpus/knowledge/*.md` at any committed revision or tree — reports missing/dangling/duplicate rows, refuses non-regular members | `python3 -I quality/check-index.py --rev REV --repo .` → `MADO_INDEX: indexed=N/N`; red at `8f51071b`, green at `446dc396`, `--selftest` 6/6 (`evidence/c3-after-446dc396.txt`) | 30 |
| index-completeness gate — corrected scope (w1 RevTrendExpansion F2) | Above is the *current* capability; the genuinely new surfaces are the plain-tree mode (`--root`), symlink/refusal semantics, `--selftest`, setup-error exit 2, and a lane-owned exit contract — revision-mode scoring pre-existed (fence via `REV=` since fleet round 1). Evidence at tip: `evidence/c3-repair-d72243e.txt` (`9/9` selftest; red `8f51071b`, green `446dc396`/`d72243e`); the original demonstration `evidence/c3-after-446dc396.txt` pins the pre-repair blob `df01b20f` and stays as its record. | `python3 -I quality/check-index.py --rev REV --repo .` / `--root` / `--selftest` | 30 |

Harm watch at `446dc396`: `MADO_SELFTEST: 460/460` exit 0; census validate
exit 0 (184 → 185 rows, +S185; W04 warnings re-checked under criterion 17 —
supersession/distinct-scope reuse only); `git diff --stat 8f51071b master --
tools/ corpus/knowledge/ SKILL.md PROVINCE.md` empty; no compositor/config
mutation.

### Sources, saturation, planned

Sources 184 → 185 (A 177 → 178 own-work; mined 165 → 166; queued 10;
rejected 9; +S185 gate quote in `corpus/lessons/round-30.md`). Saturation
9.0 / N=3 unchanged; retired: none. Planned (round 31; intent only): any
operator ruling on the two answered-by-implementation L0 questions;
semantic index-row accuracy (row text vs note contents — the fence counts
rows, not truth); residual QUALITY-line citation polish under the new
resolved-active rubric.

### Round-30 w1 erratum — C3 gate repair (append-only)

The orchestrator dispatched the prepared 33-seat wave between rounds; seat
reports land under `.ufo/waves/round-30/w1/reports/`. RevC1Fence S1–S6,
MutC3Gate F1/M3a and RevC3Gate H1 found `quality/check-index.py` (blob
`df01b20f…`) was a *strict superset* of the frozen fence it claims to
implement: `ROW_RE` `^\|\s*` vs the fence's `^\| `, `split()` vs
`splitlines()`, non-ASCII ls-tree quoting, `--root` printing a clean
`indexed=0/0` on a root with no `corpus/knowledge`, and a silent
`rev-parse master` default that can measure a stale bookmark. All classes
were latent on committed bytes (every registered receipt reproduces
verbatim; both tools print 41/43 and 43/43 at the same revisions).

Repair (this erratum's commit): the gate is rewritten fence-faithful —
literal `^\| ` row regex, `ls-tree -z` NUL parsing of blob entries, a
missing or empty `corpus/knowledge` is `SETUP_ERROR` exit 2 in both modes
(the fence is undefined there; no invented clean state), and `--rev` or
`--root` is now required (no silent `master` measurement). Selftest 6 → 8
cases: missing-dir setup error, fence-literal row forms (no-space,
double-space, tab, indented all count as missing), and a symlinked note
refusal. Receipt `.ufo/waves/round-30/evidence/c3-repair-d72243e.txt`:
`MADO_INDEX_SELFTEST: 8/8`, base `8f51071b` red `41/43` exit 1, data
`446dc396` and tip `d72243e` green `43/43` exit 0, bare invocation exit 2.

Claim status unchanged: `PRED-C3-r30` re-verified at `d72243e` (the
capability is the gate; its verdicts are identical under the repair).
Routed forward: fence/gate table-context laxity (both), C2 counter
resolves-citation-not-grounding, weak kill-rule shortcuts, own-work
circularity guard, and the SKILL gate-registry/selftest wiring —
see `corpus/lessons/round-30.md` w1 addendum. A seat-regenerated
`quality/q36-successor-receipts.txt` (ephemeral paths only, no verdict
moved) was reverted to committed bytes, same handling as round 29.

### Round-30 w1 erratum part 2 — counter repair + record corrections (append-only)

Continuation of the w1 erratum; lane tip at write: pending this commit.

- **Counter `count.py` repaired to the frozen rubric** (RevC2Counter S3–S6):
  `M<a>-M<b>` id ranges expand fully (was: endpoint singles only, so
  `M01-M07` checked 2 ids of 7); `M<a>-<b>` round-prefixed compounds stay
  literal regardless of `a<=b`; `SUPER_RE` accepts `<N1>-<N2>` on every
  list member (was: first only, losing `39, 40` in `1-5 and 38-40`);
  supersession is position-guarded ("later line"); `active=0` can never
  pass. Implementation repair only — output is byte-identical at
  `8f51071b`, `446dc396`, `d72243e`, `15ddd7d`; no verdict moves.
- **Gate repair v2** (RevC1Fence post-review addendum): `%(path)` C-quoting
  under `-z` dropped non-ASCII note names — now `git -c core.quotepath=off
  ls-tree -z`; selftest 8→9 cases adds a real git fixture (`café.md`,
  `a b.md`). Selftest `9/9`; base/data/tip verdicts unchanged
  (`evidence/c3-repair-d72243e.txt` refreshed).
- **Record repairs** (RevRecordsChain F1/F2; ScribeRecords D1/D2/D4):
  `evidence/freeze-smoke-451e8b3c-full.txt` re-captures all three legs
  with complete output (the old truncated file is kept);
  `evidence/selftest-d72243e.txt` commits the 460/460 harm-watch run;
  criterion row 48 regains criterion 32's normative accounting sentence
  (append-only text correction).
- **Errata noted, files not edited**: `registration.md:61` "12 lines
  superseded by rows 41–51" is off-by-one (line 20 is superseded by
  pre-existing row 21); SCORECARD's bare `controls/C2K1-donothing.txt`
  resolves under `.ufo/waves/round-30/`, not the repo root; the
  harm-watch head label says `446dc396` though the 460/460 tally was
  measured at `d72243e` (now receipted).
- **Recorded limit** (RevRecordsChain F3; RevC2Counter S7): the C2 rubric
  measures citation resolvability, not lesson derivation — rows 41–45
  legitimately resolve through M30-1 under the rubric, but the metric's
  name overstates; anchor+id section-scoped conjunction is routed to the
  round-31 counter v2 together with the fence/table-context tighten.

## Round 31 — results and author verdicts (2026-10-24, attempt 2)

Attempt 1 died pre-prompt (Kimi 429; no lane work). Round 30's non-author
admission stands; this round re-verified the routed w1 findings and repaired
them. Registration `.ufo/waves/round-31/registration.md` frozen `6803a999`
before the data commit `f621e3c0` (base `274f7355`, r30 tip). Axis table
re-derived at base (criterion 22): navigation 43/43 = 1.0; calibration
resolved-active 39/40 = 0.9750 (lowest — criterion 35's mis-scoped M23-7);
sourced-art 1.0; operability selftest 9/9 = 1.0. Three claims, three
distinct surfaces; each measured without the others.

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage / index-row *fidelity* surface (routed C1 blind spot): `quality/check-index-rows.py` — row inside the coverage-map table, ≥3 non-empty cells, defined S-ids, resolvable repo-relative artifact cites, Holds↔note overlap | absent at base → `274f7355`: `rows=43 errors=1` (`row-cells: knowledge/animation-table-r26.md` 2 cells) exit 1; `f621e3c0`: `rows=43 errors=0` exit 0 (3 glob WARN — ephemeral r12/r24 evidence dirs) | `python3 -I quality/check-index-rows.py --rev REV --repo .` / `--selftest` | target met; r26 row repaired; K1 red at base on the real defect |
| C2 calibration / resolved-citation rubric v2 (routed C2 loopholes): every grounding cite resolves — `file#anchor` slugged heading *in the named file*, spell form in file bytes, bare `round-<num>.md` non-empty; `outside` corroborates only; `active ≥ 30` bounds supersede-all | `274f7355`: literal 40/52, resolved 39/40, UNRESOLVED criterion 35 → `f621e3c0`: literal 42/54, resolved 41/41 = 1.0000 TARGET_MET (new rows 53–54 supersede 48; criterion 35's cite re-sectioned) | `python3 -I .ufo/waves/round-31/c2/count.py REV` | target met; K2: the frozen S8 miscite is UNRESOLVED at base |
| C3 operability / gate robustness (routed C3 findings): `--rev` pinned via `rev-parse --verify --end-of-options`; symlinked `corpus` ancestors REFUSED under `--root`; `--repo`+`--root` SETUP_ERROR; selftest 9→12 | `274f7355`: `indexed=43/43` + selftest 9/9 → `f621e3c0`: `indexed=43/43` + `12/12 assertions passed` (option-shaped rev, symlink ancestor, repo-under-root each refused with the right exit) | `python3 -I quality/check-index.py --selftest` / `--rev REV --repo .` | target met; hardened gate does not regress the honest 43/43 |

Negative controls committed (`.ufo/waves/round-31/c2/negative/`):
n1-empty → UNRESOLVED; n2-wrongfile → TARGET_MET (existence is the rubric;
relevance stays out of scope — routed forward as a residual cheat);
n3-section → UNRESOLVED; n4-collapse → FLOOR_VIOLATION on the
supersede-all drain. All receipts reproduce under `--active-min 2`.

### Capabilities (round 31)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| index-row fidelity gate | Score each coverage-map row's *shape* (table membership, cells, defined S-ids, resolvable artifact cites, Holds overlap) at a revision or tree — the surface the r30 fence was measured not to check | `python3 -I quality/check-index-rows.py --rev REV --repo .` → `MADO_INDEX_ROWS` | 31 |
| resolved-citation admissions counter v2 | Reject miscited/unverifiable grounding (wrong section, empty file, supersede-drain); the r30 counter stays frozen as the v1 record | `python3 -I .ufo/waves/round-31/c2/count.py REV` → `PRED-C2-r31-v2` | 31 |

Harm watch at `f621e3c0`: `git diff --stat 274f7355..72021ded -- tools/
corpus/knowledge/ SKILL.md PROVINCE.md` — touched only
`quality/check-index-rows.py` (new), `quality/check-index.py`,
`.ufo/waves/round-31/`, `corpus/QUALITY.md`, `corpus/README.md`; no
compositor/config mutation; misroot sweep at fleet root clean (only
`mado-shokunin/` exists). The 33 r30 w1 reports + swarm-registry.json
stay untracked orchestrator artifacts — preserved, not committed by this
lane. `quality/q36-successor-receipts.txt` untouched (peer-reported
restored to HEAD). Wave: `.ufo/waves/round-31/w1-spec.json` (15 seats)
PREPARED, not dispatched — expected seat surface; orchestrator dispatches.

### Sources, saturation, planned

Sources 185 unchanged. Saturation 9.0 / N=3 unchanged; retired: none.
Planned (round 32; intent only): the w1 falsification wave's findings;
semantic Holds↔note accuracy (overlap ≥5 words is syntactic — a row can
still paraphrase the wrong note); criterion-relevance grounding (a lesson
that contradicts its criterion still resolves); the r24 `S###.bin`
evidence path convention.

## Round 32 — results and author verdicts (2026-10-24, attempt 1)

Assimilation round (operator directive 2026-10-24, item 10). Registration
`.ufo/waves/round-32/registration.md` frozen before any data; data commit
`f5910876`; scratch cleanup `48f9fe09`; docs commit below. Axis table
re-derived at tip (criterion 22): navigation 46/46 = 1.0; calibration
resolved-active 41/41 = 1.0; sourced-art 1.0; operability selftest 12/12 = 1.0.
Two claims, two distinct surfaces; each measured without the other.

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage — the Hyprland IPC two-socket contract theme (frontier → core): 3 admitted entries + 5 registry rows, every source re-opened by the lane on 2026-10-24 | base `25622288`: `entries=0 rows=0 cited_entries=0` → tip: `entries=3 rows=5 cited_entries=3`; registry 185 → 190 rows; coverage map 43 → 46 rows over 46 notes (`indexed=46/46 missing=0 dangling=0 duplicates=0`) | the frozen shell counter in `.ufo/waves/round-32/registration.md` §C1 | target met; controls: rows-only and entries-only scratch copies both fall short of the target |
| C2 calibration (lowest scored axis) — the published axis table must not be stale against the counters it names | base `25622288`: `MADO_AXIS: checked=3 mismatched=2` (published calibration 39/40 vs derived 41/41; published operability 9/9 vs derived 12/12) exit 1 → tip: `mismatched=0` exit 0; the round's own commits moved navigation to 46/46, so the pre-fix tip measured `mismatched=3` | `python3 -I quality/check-axis-scores.py --rev <rev> --repo .` | target met; perturbation control `41/41` → `40/41` bites (`mismatched=1`) |

### Capabilities (round 32)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| published-axis staleness gate | Re-derive the lane's published axis fractions at a revision with the lane's own instruments and fail when the publication no longer matches the repo it describes | `python3 -I quality/check-axis-scores.py --rev <rev> --repo .` → `MADO_AXIS`; `--selftest` → `17/17` | 32 |

### Sources, saturation, planned

Sources 185 → 190 rows (S186, S187, S188, S189, S196 added; no row touched old→new;
no frontier row advanced). Saturation 9.0 / N=3 unchanged; retired: none.
Planned (round 33; intent only): the wave's open attacks — semantic Holds↔note
accuracy beyond the ≥5-words proxy, criterion-relevance grounding, the n2
relevance-free citation cheat, and the r24 `S###.bin` glob convention; plus the
lane hygiene defect this round shipped (seat scratch trees committed at
`f5910876`, removed at `48f9fe09` — the bytes stay in history).

## Round 33 — correction of the round-32 C1 row, and author verdicts (2026-10-24, attempt 1)

The round-32 C1 row above is not rewritten. It says target met and cites base
`25622288`. That short hash does not resolve. The full hash is
`256222890d935212874a09751ff9b7869943c2d7`. The frozen round-32 counter on
`d9ed38166cc3be8ef4c52b41d66ad94010feb047` prints `cited_entries=7`, not 3.
This line is the correction:

r33-claim-verdict: r32-C1 cited_entries=7 verdict=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047

Round-33 claims were frozen in `.ufo/waves/round-33/registration.md` before any
corpus append. C1's predicate was then killed by a seat, before data, and was
not rewritten.

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage — Waybar event-socket client (new surface, not a re-score of round 32) | lane tree before append: `closed_entries=0 closed_rows=0 open_cites=4 verdict=TARGET_MISSED`; after: same, because the entries were not appended | `python3 -I .ufo/waves/round-33/c1/count.py --root . --frozen .ufo/waves/round-33/c1/frozen.json` | honest stop / unprovable. A symlink crib under `.ufo/waves/round-33/scratch/CriticC1Junk/` prints `TARGET_MET`. The frozen kill rule is not a certification. The predicate was not changed after seats scored it. |
| C2 calibration (tied for lowest; every scored axis is 1.0 and a capability entered in round 32, so the stagnation nudge does not waive) — the published r32-C1 verdict must match a re-run | before: `claim_mismatch=1 reason=absent verdict=TARGET_MISSED` exit 1; after: `claim_mismatch=0 reason=match published=7 measured=7 verdict_word=honest-stop verdict=TARGET_MET` exit 0 | `python3 -I .ufo/waves/round-33/c2/count.py --repo . --scorecard SCORECARD.md` | target met on the correction line; the round-32 row above is not rewritten |

r34-s189-line: line=169

Axis table re-derived at the round-34 data tree (criterion 22): navigation 47/47 = 1.0; calibration resolved-active 41/41 = 1.0; operability selftest 12/12 = 1.0. Not an axis-score claim. The publication is updated so the existing gate does not go red when the new note is indexed.

## Round 34 — a counter that rejects the crib, then the data (2026-10-24, attempt 1)

Resumed round. A prior attempt froze the two predicates and landed the data
before its provider route died; this attempt inherited both, re-verified
them, and did not re-declare or narrow either. The round-33 counters are
NOT amended — their blob ids are identical at the round-33 freeze
`9a46ccf3282117f960b8d53cd71599a91f388ee3`, the round-33 tip
`69f72100bee31a60b811f8fbbe7796db883e17b3` and this round's tip.

Registration `.ufo/waves/round-34/registration.md` was frozen before any data
at `3420e827bd7b21b1374b23245526554ffd20d096`; the data landed afterwards at
`fa7ba11346116672352b5d41494141c5c4d738d0`. Both claims sit on the lowest
non-retired axes (coverage and calibration are tied at 1.0; a capability
entered in round 32, so the stagnation nudge does not waive). One wave, 64
seats, 25 of them attack roles (39%).

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 coverage — the Waybar event-socket client theme (frontier → core): one admitted entry `corpus/knowledge/waybar-module-text-route-r25.md` plus registry rows S201 and S202, both sources re-opened by the lane on 2026-10-24 | pre-data freeze `3420e827`: `PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` exit 1 → tip `fa7ba113`: `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` exit 0; registry 190 → 192 rows; navigation 46/46 → 47/47 | `python3 -I .ufo/waves/round-34/c1/count.py --root . --frozen .ufo/waves/round-34/c1/frozen.json` | target met on the frozen counter. Kill rule discharged by the committed pre-data receipts: the symlink crib, the symlinked-entry, symlinked-parent and symlinked-sources trees, the hardlink tree, the entries-only, rows-only and used-by-prefix trees and the do-nothing control ALL print `TARGET_MISSED` exit 1; only the regular-file golden tree prints `TARGET_MET`. The round-33 counter still prints `TARGET_MET` on its crib and was not replaced. Scoped honestly: a bounded documentary-route increment, not a surface move — the live bar module text stays open (`corpus/README.md` frontier U7). |
| C2 calibration (lowest scored axis, tied) — the published S189 queue-cap line number must match a re-read of the pinned fetch | before: the publication was absent, `PRED-C2-r34-v1 published=absent measured=169 mismatch=1 verdict=TARGET_MISSED` exit 1 → after: `published=169 measured=169 mismatch=0 verdict=TARGET_MET` exit 0 | `python3 -I .ufo/waves/round-34/c2/count.py --repo . --scorecard SCORECARD.md --frozen .ufo/waves/round-34/c2/frozen.json` | target met. The counter rejects a card whose last marker tail is `line=128` (`published=128 mismatch=1` exit 1) and a card with no marker at all (`published=absent mismatch=1` exit 1). The published line is `line=169`; `.ufo/waves/round-32/fetch/S189.bin` line 169 is `const size_t MAX_QUEUED_EVENTS = 64;` (sha256 `eea605dfe5ce09e1…`). The false round-32 row is still visible above and is NOT rewritten. |

Correction to the note appended by the data commit: that note wrote "operability
selftest 12/12". 12/12 is the operability AXIS fraction (the index
instrument's own assertions); the axis-gate selftest is **18/18**. The
committed transcript is `.ufo/waves/round-34/controls/axis-selftest.txt`
(selftest `MADO_AXIS_SELFTEST: 18/18 assertions passed` exit 0; live gate
`MADO_AXIS: checked=3 mismatched=0 rev=fa7ba11346116672352b5d41494141c5c4d738d0`
exit 0). This is a transcription repair of a published number, made by
appending; the axis table itself is unchanged.

### Capabilities (round 34)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| crib-rejecting coverage counter | Score a corpus admission with a counter that refuses symlinked, hardlinked and path-escaping evidence trees, and re-run that verdict from committed fixture bytes alone | `python3 -I .ufo/waves/round-34/c1/count.py --root . --frozen .ufo/waves/round-34/c1/frozen.json` → `TARGET_MET`; the same command over `.ufo/waves/round-34/controls/symlink-crib` → `TARGET_MISSED` exit 1 | 34 |

### Sources, saturation, planned

Sources 190 → 192 rows (S201, S202 added; no row touched old→new; no frontier
row advanced — the Waybar module-text frontier item U7 stays open because this
round documents the route, not the rendered module text). Saturation 9.0 / N=3
unchanged; retired: none.
Planned (round 35; intent only): the three findings this round's own wave
produced but did not fix — the `PRED-C1-r34-v1` word-bound clause is provably
dead code under its own frozen spec, the `S_ISLNK`/`O_NOFOLLOW` pair is
redundant against every static tree (TOCTOU-only), and the merge package's
id remap base ("registry ends at S196") is stale now that the lane registry
ends at S202.

## Round 35 — the idle-lock control surface lands; the ledger claim is falsified against itself (2026-10-24/25, two attempts)

Registration `.ufo/waves/round-35/registration.md` froze both predicates at
`19e4ab3171c1540c40d6b12097745af98053b07d` before any round-35 data. Attempt 1 dispatched the
64-seat wave 1 and died without a report; attempt 2 inherited the wave-1 evidence, landed the
data at `02088b4dff0da153df30ff174611d1257c92d0cd`, dispatched a 40-seat wave 2 against it, and
applied the wave-2 falsifications as append-only errata. Round shape: two v1 waves, 64 + 40 =
**104 seats** (wave 1: executor 13, scout 12, reviewer 11, critic 8, scribe 7, connector 4,
mutation-tester 3, sentinel 2, revenger 2, simplifier 2; wave 2: reviewer 21, executor 3,
mutation-tester 3, critic 3, sentinel 2, revenger 2, scout 2, scribe 2, simplifier 1,
connector 1). The §3 planner seat is held by the L1; the planning data-walk rode the
`connector`/`revenger` items, as the validator rejects a `planner` seat.

| Claim / axis | Before → after | Counting command | Author verdict |
|---|---|---|---|
| C1 **coverage** — the idle-lock control surface (frontier → core): three admitted entries + eight registry rows S203–S210, adopted from `merge/mado/` with ids re-pointed by document | freeze `19e4ab3`: `closed_entries=0 closed_rows=0 open_cites=8 TARGET_MISSED` exit 1 → data `02088b4`: `closed_entries=3 closed_rows=8 open_cites=0 TARGET_MET` exit 0 (re-run after every errata append, unchanged); registry 192 → 200 rows; navigation 47/47 → 50/50 | `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json` | **ADMITTED, with three routed defects** — the counter is shape-scored (dead `digest` clause; shape-only and fabricated-payload cribs both reach `TARGET_MET`: `controls-content/`), so its `TARGET_MET` is not truth evidence; wave-2 seats falsified three inferences in the admitted text (withdrawn by errata) and all eight receipts were re-opened and re-hashed 8/8; a one-line digest repair keeps the real root `TARGET_MET` and kills both cribs (round-36 claim) |
| C2 **calibration** — the lane's own evidence ledger: retire the r34 dead word-bound clause, split the S_ISLNK/O_NOFOLLOW pair, re-issue the frozen-blob ledger at the real r34 tip | r34 tip `dff3941` had no clause ledger (`error=clause-ledger-missing` exit 2) → `02088b4`: `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 TARGET_MET` exit 0 | `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json` | **NOT ADMITTED — the claim's substance is falsified.** The counter prints `TARGET_MET` exactly as its predicate says, but wave-2 seats showed: (a) `ledger_tip_ok` scores `TARGET_MET` on the round-34 defect itself (stale `fa7ba113` label, `MutC2Real` M3a/M3c/M3d, `RevTipLedger` control C) — the repaired label is not observed; (b) the round-34 "real tip" is disputed — `dff3941` was master for 0:17:37 and the last round-34-labelled commit is `6d754bd`; the blob ids verify identically at both; (c) `uncovered=0` is fail-open on clause deletion with its control, and covered-receipts are token greps (`RevC2Tip` F1/F2). Operator ruling required before this claim is counted as a repair |

**Axis table re-derived at `02088b4dff0da153df30ff174611d1257c92d0cd` plus the round-35 errata:** navigation 50/50; calibration 43/43; operability 12/12.

Three tied sub-axes sat at 1.0 at the round-34 tip (`navigation 47/47`, `calibration 41/41`,
`operability 12/12`) and the capabilities table gained a row in round 34, so the AXES.md
stagnation nudge does not waive the lowest-axis obligation; C1 and C2 sit on the lowest two.
No axis is claimed harmed: the index gate reads 50/50 exit 0, the axis gate re-derives all
three rows to MATCH, and the operability suite reads `MADO_SELFTEST: 460/460 assertions passed`
(byte-identical suite to the round-34 tip). Two measured defects are recorded rather than
hidden: the axis publication was stale for ~15 minutes while the data commit landed ahead of
this row (`mismatched=2`), and the pre-data `golden` control's rows differ from the shipped
registry in anchor/teaches cells, so the controls never exercise the live bytes.

### Capabilities (round 35)

None entered. The proposed row — "clause-ledger audit of an admission counter" — would
misdescribe what runs: wave-2 seats showed three of its four observables are self-authored
token checks that a clause deletion, a receipt substitution or a stale label all pass
(`RevC2Tip` F1–F5, `MutC2Real` M3a/M3c/M3d). A capability table row is a claim that the lane
can *do* the thing; this round can demonstrate it only in the degenerate sense of "audits
whatever ledger it is handed".

### Sources, saturation, planned

Sources 192 → 200 rows (S203–S210: eight `own-work` tier-A rows, all `mined`, opened
2026-10-24; no existing row's status/recheck/used-by changed; three new rows (S203, S204, S205) had
`scope`/`teaches`/`recheck` cells corrected in-round to match the entry errata
(`git diff --numstat 02088b4 HEAD -- corpus/SOURCES.md` → 3 insertions, 3 deletions)). Frontier advanced: the round-35
idle-lock offer route (consumer half measured; transitions remain open). Saturation 9.0 / N=3
unchanged; retired: none.
Planned (round 36; intent only): (1) bind the C1 digest to the bytes read and add the two
content cribs as committed controls — the patch and both miss receipts exist; (2) make
`ledger_tip_ok` parse the ledger's own table, cross-check the clause ledger against the
counter's clause set, and pin one tip definition; (3) census gaps found by `MutCensusRow`
(alphabetic recheck prose accepted; blank `used-by` silent; `used-by` unchecked on non-mined
rows); (4) the `used-by`/`opened` columns are not measured by C1 at all (`RevRowsUsedBy` F1/F2).

**Correction to the C1 before-state (append-only, found by wave-2 `CritAxisClaims`).** The
registration's before-state says the idle-lock *offer* "was never opened by this lane". That
overstates the gap: `knowledge/waybar-walker-semantics.md:139` already carried the waybar
run payload, tooltip and click, and `knowledge/idle-lock-plane.md:284-289` already reviewed
the offer at `dff3941`. What this round actually added is the menu surface (S208), the dated
bar-config copies (S209), the toggles directory (S210), the setup path (S203/S204) and live
chain liveness (S205). The claim still stands as a coverage move; its before-state was
larger than the registration said.

**Correction to the lowest-axis quote (append-only, same seat).** The round-32 publication
carried a fourth cell (`sourced-art 1.0`) that round 34 dropped while `## Retired` still
reads "none retired". The three-cell quote in the registration is therefore incomplete but
not wrong on value; the lowest-axis conclusion (two tied-lowest axes, no nudge waiver)
survives. Recorded for round 36: `sourced-art` must be retired explicitly or republished.

**Axis table re-derived at `7b745a1d943e5db5e8b9f8a7f4bee7af65b13990` (the first commit whose publication the gate parses; at `4f35c80` it read `mismatched=2`, calibration and operability NOT-PUBLISHED):** navigation 50/50; calibration resolved-active 43/43; operability selftest 12/12.

## Round 36 — the two admission counters are repaired and shown to discriminate; the records pass a pointer gate (2026-10-25, attempt 1)

Registration `.ufo/waves/round-36/registration.md`, frozen at
`dbf8b579aeac0f023aaf595770f1cb0049e4baa2` before any round-36 data. The round works the
two axes tied at the lowest published score (`calibration` and `operability`, both at
their rubric's 1.0 against a 9.0 saturation line) because the `AXES.md` stagnation nudge
does not apply: a capability row entered in round 34 and the window is 3 rounds.
Round shape: two v1 waves; wave 1 dispatched **64 seats** in one batched `task` call
(reviewer 17, mutation-tester 13, scout 12, executor 5, scribe 5, critic 5, sentinel 2,
connector 2, simplifier 2, revenger 1). The §3 planner seat is held by the L1; the
planning data-walk rode the connector and scout items, since the validator rejects a
`planner` seat.

| Claim / axis | Before → after | Counting command | Verdict |
|---|---|---|---|
| C1 **calibration** — the two round-35 admission counters are repaired and shown to discriminate (routed defects D3, D4) | `--profile r35` (the round-35 counters as frozen): `controls=25 correct=14/25 verdict=TARGET_MISSED` exit 1 → `--profile r36`: `controls=25 correct=25/25 verdict=TARGET_MET` exit 0. The eleven wrong lines in the before run are exactly the fabrication and document-observable classes the spot-check routed: `c1-shape-only`, `c1-fabricated-payload`, `c1-no-registry-heading`, `c1-row-moved-out` and seven of the eight `c2` mutants | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-counter-discrimination.py --profile <r35\|r36> --manifest .ufo/waves/round-36/controls/manifest.json --receipts .ufo/waves/round-36/controls/receipts[-r35]` | **improved** — the counters reject what they used to accept, and still accept the live bytes and a registry-shaped copy of them; the fail-open paths the spot-check named are now controls with `TARGET_MISSED` receipts. **Limit, stated:** nine of the fourteen `c1` rejects are derived from the heading-less round-35 trees, so they exercise the `row-in-registry` fence rather than their own clause; the digest binding is proven on fence-restored copies (`receipts/clause-attribution.txt`, wave-1 `ExecDigestCribs`, `MutC1CheckAnchor`), not by the frozen manifest alone |
| C2 **operability** — the lane's records pass an evidence-pointer durability gate (routed defects D2, D5, D8, D10) | `dangling_r35=2, dangling_r35_closed=0, inherited_dirty=10, scratch_disposition_ok=0, tip_axis_transcript=0, setup=missing-r36-sections → TARGET_MISSED` exit 1 → `dangling_r35=2, dangling_r35_closed=1, inherited_dirty=0, scratch_disposition_ok=1, tip_axis_transcript=1, setup=ok → TARGET_MET` exit 0 | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-evidence-pointers.py --rev <rev>` | **improved** — the gate is the deliverable and it is red before the repairs and green after, on the same command |

The claims are separable in what they *measure*, with one named one-way dependency. C1 reads
only the manifest, the two counters and the fixture generator; its result is unchanged with
`LOG.md`, `SCORECARD.md` and the round-36 lesson deleted (verified in a clean clone by wave-1
`CritLanding`). C2 reads only the lane's records, the tree at one revision and `git status`,
and its before state was measured before any round-36 record section existed. The dependency:
C2's *records* cite C1's artifacts, so C2's pointer set is only resolvable once C1's files are
committed — C2 can be measured without C1's *repair being correct*, never without C1's *files
existing*. That sentence replaces an earlier "neither reads the other's output", which the
same seat falsified by deleting C1's files and watching C2 go red.

No harm: the axis fractions below move up or stay; `tools/mado-verify.sh` is byte-identical
to the round-35 tip (`9113c7c0…`) and its suite reads `MADO_SELFTEST: 460/460 assertions
passed`; the registry census exits 0 before and after with the same seven pre-existing
`W04` warnings; no knowledge entry, config plane, compositor state or sibling repo is
touched.

### Capabilities (round 36)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| counter-discrimination audit | score an admission counter against a frozen manifest of accept and reject controls, so a degenerate instrument (always-accept, always-reject, crash) cannot reach the target | `quality/check-counter-discrimination.py`; 25/25 on the repaired counters, 14/25 on the frozen round-35 ones | 36 |
| evidence-pointer durability audit | re-derive, from committed bytes, every evidence pointer a round's records cite, the inherited uncommitted set, a named scratch disposition with its counted size, and a tip-revision axis transcript | `quality/check-evidence-pointers.py`; `TARGET_MISSED` before the repairs, `TARGET_MET` after | 36 |

(The repertoire's live rows are the per-round `### Capabilities (round N)` sections; the
table under `## Capabilities` is the fleet-round-1 rollout snapshot and is not maintained
by later rounds.)

**Adjacency boundaries for both rows (wave-1 `ConnOverlap`).** The mutation *method* belongs to
`tameshi-shokunin` (`tameshi/PROVINCE.md:3-5,7-11,29-36`), which names this lane's gate as a
read-only surface; `gen-mutants.py` and the discrimination gate therefore stay lane-internal
fixtures and are never offered as a reusable harness or a sibling service. The pointer-audit
*instrument class* already exists at `kaidoku` (`citation-drift-probe.py`), `kagi`
(`claim-ledger.sh citations`) and `chousa` (`verify-integrity`); C2's claim is exactly and only
"mado's own records pass this gate", not that the lane invented the ground. Nothing is
absorbed from either lane.

### Retirement (round 36): `sourced-art`

`sourced-art` was published at 1.0 in round 32 as `10 × covered U-items / 7`, was dropped
from the publication in round 34 while `## Retired` still read "none", and round 35's
spot-check recorded the discrepancy. It is **retired explicitly** here, not republished:
its denominator was the fixed seven-item uncovered-ground list U1–U7, five of which have
since been closed by admitted entries, so the fraction no longer measures what it was
built to measure and a saturated 1.0 would read as coverage progress it is not. The
ground itself stays measured by the per-round frontier rows in `corpus/README.md`. No
other axis is retired.

### Sources, saturation, planned

Sources 200 → 201 rows: **S211** (negative controls in observational studies, tier A,
`paper`, opened 2026-10-25, `used-by` exactly `corpus/lessons/round-36.md`; gate quote and
location in that lesson's `## Gate`). No row's `status`, `recheck` or `used-by` changed.
Frontier advanced: not on the domain plane — this round advances the lane's **instrument**
plane (two counters, two gates) and says so; the domain-vs-meta ratio for the last 30
commits is 3 domain / 27 meta (lesson M36-5, criterion 60). Saturation 9.0 / N=3
unchanged; retired: `sourced-art` (above). `Assimilation: none this round`.

Axis table re-derived at `520c631d2925807aadadb041eeda13f8b829b0c5` (this round's records
commit — the first revision where all five new criteria, including 61, are committed and the
publication itself is in the tree; at the data commit `a3094c9` the same publication reads
`47/47`, which the lane's red receipt records as `STALE`): navigation 50/50; calibration
resolved-active 48/48; operability selftest 12/12.

### Measured at (round 36, self-verdicts pending non-author closure)

- **C1.** Before at `4243d03`: `controls=25 correct=14/25 verdict=TARGET_MISSED`
  (`receipts/before-discrimination.txt` under the round-36 wave directory).
  After at `4d28b193e52f6cc8f04e81fda2664e018d62e209` (the revision both receipts name; the
  gate, manifest and frozen specs are bound by sha256 inside them):
  `controls=25 correct=25/25 verdict=TARGET_MET` (`receipts/after-discrimination.txt`).
  Clause attribution proved separately: `receipts/clause-attribution.txt` (every frozen
  crib re-scored from a copy with only the competing fence removed still dies with exactly
  one open cite).
- **C2.** Before at `4243d03`: `TARGET_MISSED` with `dangling_r35_closed=0`,
  `scratch_disposition_ok=0`, `tip_axis_transcript=0`, `setup=missing-r36-sections`
  (`receipts/before-pointers.txt`, whose header records the live-tree `inherited_dirty=10`
  the re-run cannot reproduce). After at `4d28b193e52f6cc8f04e81fda2664e018d62e209` (the revision both receipts name; the
  gate, manifest and frozen specs are bound by sha256 inside them):
  `TARGET_MET` with `dangling_r35_closed=1 dangling_r36=0 inherited_dirty=0
  scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok`
  (`receipts/after-pointers.txt`).
- **Harm watch at the same revisions.** `tools/mado-verify.sh --selftest` →
  `MADO_SELFTEST: 460/460 assertions passed`, gate blob `9113c7c0…` (byte-identical to the
  round-35 tip); `quality/check-index.py --rev 520c631 --repo .` → `indexed=50/50
  missing=0 dangling=0 duplicates=0`; census exit 0 with the same seven pre-existing `W04`
  warnings; no row's `status`/`recheck`/`used-by` changed.

### Planned (round 37; intent only)

1. Route the wave's `c2`-side finding that a *fixture* which cannot resolve its environment
   is a vacuous control into the manifest's own construction check (criterion 59's
   executable form).
2. Harden the tip-transcript observable: authenticate the transcript by its `MADO_AXIS_ROW:`
   rows (one per checked axis) rather than by three substrings (`RevAxisTranscriptAsk` F1).
3. Resume the shokuknow assimilation the round-35 evidence chain interrupted.
4. Move one domain-facing surface: the round-27 `tools/` plane is the last domain change;
   the ratio (criterion 60) is the forcing function.

## Round 37 — event-socket delivery: two entries on a new edge class, and a read-only subscriber census (2026-10-25, attempt 2)

Registration `.ufo/waves/round-37/registration.md`: frozen v1 at `8f0a9e3`, re-frozen v2 at
`893a8aadc80ab19bc163e366d674a8ac32feacd0` before any data (Amendment 1: the L1's own v1 golden
control was a token stub that met C1). Lowest-axis rule: all three published axes tie at their
maximum at base (`receipts/axis-base.txt`), so each is a lowest axis; C1 works coverage. Round
shape: one v1 wave of **38 seats** (wave-1 build + first falsifiers) plus one residual call of
**8** reviewer/critic seats; round total 46. The §3 planner seat is held by the L1.

| Claim / axis | Before → after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **coverage** (assimilation, sourced) — two entries land on a new edge class under the held IPC contract: what the compositor does to an event client that stops reading, and whether a removal is observable on this host | `admitted=0/2 verdict=TARGET_MISSED` exit 1 at `b4e47e9` → `admitted=2/2 verdict=TARGET_MET` exit 0 at `3f424257a1ea69cd2655770259ba00b423293f4f` | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r37-event-ground.py --repo . --rev <rev>` | **improved on the counter, with a named instrument limit**: wave-1 `CritC1Cheap` reached the same target with a 19-line self-receipt crib, so the counter is necessary, not sufficient; the content rests on the hand re-checks named in the lesson (every source re-fetched by a second seat, byte-identical) |
| C2 **operability** (capability acquisition) — `tools/mado-eventq.py` | `fixtures=0/10 readonly=0 live=0 tool=absent` exit 1 at `b4e47e9` → `fixtures=10/10 readonly=1 live=1 verdict=TARGET_MET` exit 0 at `3f424257a1ea69cd2655770259ba00b423293f4f` | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r37-eventq.py --repo . --rev <rev>` | **improved, with a named instrument limit**: the live clause is reachable with a snapshot built from the counter's own fixture rows (wave-1 `RevC2Code` F1) and `lagging`/`--expect-client` lack a discriminating case (F4, F5); the live receipt is corroborated independently by `receipts/eventq-live-proc-crosscheck.txt` (`/proc` shows the same two server inodes, `OVERALL: AGREE`) |

Separable: wave-1 `CritSeparability` measured each claim with the other's files deleted, both
directions, and neither verdict moved.

No harm: `tools/mado-verify.sh` unchanged (`MADO_SELFTEST: 460/460 assertions passed`); the four
lane gates touched by the `GIT_*` scrub print byte-identical plain output before and after
(`receipts/git-env-green.txt` against the red-before digests in
`w1/scratch/ExecPointerEnv/sweep.txt`); census exit 0 with the same seven `W04`; no existing
knowledge entry edited; no config, service or compositor state touched.

### Capabilities (round 37)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| event-socket subscriber census | list who holds the client end of Hyprland's `.socket2.sock`, each subscriber's unread bytes and the compositor's server fds, count the two removal markers, and say whether those markers are observable at all (`debug:disable_logs`) — from the kernel's socket table, never connecting | `tools/mado-eventq.py`; `quality/counters/c2-r37-eventq.py` 10/10 fixtures, `receipts/eventq-live.txt` (waybar pid 935660, socat pid 2293, `markers_observable=no`) | 37 |

Adjacency (wave-1 `ConnOverlap`): the tool reads ground five siblings also read — the journal
(tsukuroi, mori), `/proc` fd listings (souji), `ss` socket enumeration (kama), the mutation method
(tameshi). Shared evidence, not shared ownership; nothing is absorbed.

### Sources, saturation, planned

Sources 201 → 207 rows (S212–S217, tier A, `mined`, opened 2026-10-25); S189 and S201 `used-by`
extended (old→new in `corpus/lessons/round-37.md`). Assimilation: one package entry admitted
re-grounded, two refused (null channel). Domain-versus-meta ratio of the last 30 commits
(criterion 60): **3 domain / 27 meta**; this round's data commit `3f42425` is the first
domain-facing change since round 27. Saturation 9.0 / N=3 unchanged; retired: none this round.

Axis table re-derived at `3f424257a1ea69cd2655770259ba00b423293f4f` (the data commit; the records
commit adds no knowledge entry or criterion): navigation 52/52; calibration resolved-active 50/50; operability selftest 12/12.

### Planned (round 38; intent only)

1. Counter v3 for both round-37 instruments: bind each Gate receipt to `fetch/` and to a re-fetch
   digest (kills the self-receipt crib), and cross-check a live snapshot's server inodes against
   `/proc` (kills the fixture-row snapshot); add discriminating `lagging` and `--expect-client`
   cases.
2. The next desktop surface from `considerthese/2026-10-24.md` proposal 4, ranked by wave-1
   `ConnFrontier`: the config-option table (who owns each key, checked against `getoption`).


### Capabilities (round 38)

|Capability|What it can now do|Evidence pointer|First-working round|
|---|---|---|---|
| request-socket admission | admit a knowledge entry on the request socket only when every cited source id has a unique mined registry row, a pin-bound Gate receipt, a verbatim quote and the frozen lineage vocabulary — the crib classes of M37-5 close | `quality/counters/c2-r38-request-ground.py` admitted=3/3 at `efb0ec2`; controls 19/19 in `.ufo/waves/round-38/receipts/after-discrimination-v3.txt` | 38 |

Sources, saturation, planned: Sources 207 → 211 rows (S221, S253, S258, S277, `mined`,
2026-10-25); S158 and S187 `used-by` extended. Assimilation: 3 package entries admitted
re-grounded, 2 refused (null channel; follow-queue-vs-request conflation). Saturation 9.0 / N=3
unchanged; retired: none this round. Axis table re-derived at `bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5` (the round-38 tip; data commits `245065c`/`efb0ec2` add three indexed entries and no criterion, the records commits add neither): navigation 55/55; calibration resolved-active 50/50; operability selftest 12/12.

## Round 39 — the option-ownership table: a tool, its ground, and the re-registered discrimination pair (2026-10-25, attempt 2)

Registration `.ufo/waves/round-39/registration.md` (attempt-1 freeze `457d1b1`: C1 manifest,
base receipts) and its attempt-2 addendum `.ufo/waves/round-39/registration-a2.md` (freeze
`d9b4e4a65ad63ddcd0b86d2468f41508a131b7fa`, both C2/C3 counters and their controls committed
before any C2/C3 data). Lowest-axis rule: every published axis tied at its maximum at base
(`receipts/axis-base.txt`), so each is a lowest axis; C1 works calibration. Round shape: one
v2 wave `w1` of **64 seats** (dispatched by attempt 1, integrated by attempt 2); no residual
call; round total 64. The §3 planner seat is held by the L1.

| Claim / axis | Before → after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **calibration** — the repaired round-38 discrimination pair re-registered with a fresh freeze | frozen r38 manifest × unchanged counters `controls=19 correct=18/19 verdict=TARGET_MISSED` exit 1 at base `08be4eb` (`receipts/c1-redbefore.txt`) → re-frozen manifest `controls=19 correct=19/19 verdict=TARGET_MET` exit 0 at the freeze `457d1b1` and at the tip `3628472` (`receipts/c1-after-freeze-L1.txt`, `receipts/c1-after-tip.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json --rev <rev>` | **improved** (re-registration; the pair is the round-38 landed pair, so the move is calibration of the record, not new discrimination power) |
| C2 **operability** (capability acquisition) — `tools/mado-options.py`, the config-option ownership table | `fixtures=0/11 tool=absent verdict=TARGET_MISSED` exit 1 at base → `fixtures=11/11 tool=present verdict=TARGET_MET` exit 0 at the data commit `4ec582e68acaae647911e31334f0b018b4c772bf` and the tip (`receipts/c2-*.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c3-r39-options.py --repo . --rev <rev>` (`PRED-C3-r39-v2`) | **improved under v2, frozen before data; the v1 draft named by registration.md is an honest miss** — it was never in a freeze commit and could not reach MET for any tool (`w1/CritC2Control.md`, `w1/RevC2Counter.md`); the wave-built tool scores `1/11` under v2 (`c2/ctl-wave-v1.txt`) |
| C3 **coverage** (sourced) — `corpus/knowledge/config-option-table-r39.md` + S218/S219 (and S220) | `admitted=0/1 verdict=TARGET_MISSED` exit 1 at base → first data commit `3783961` `admitted=0/1` (clause g: the S219 OBS line wrapped its quote off the id's line; `c3/measure-first-data-commit.txt`) → `admitted=1/1 verdict=TARGET_MET` exit 0 at `362847279eccb77b22789a37cbbe3b83b205d49c` (entry-only rewrap; counter unchanged) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c4-r39-options-entry.py --repo . --rev <rev>` (`PRED-C4-r39-v1`) | **improved, with a disclosed first-data miss** for the operator to rule on; residual: a fabricated self-consistent set passes (control P) |

Separable: C2 met at `4ec582e` before any C3 data existed; C3's control P met with a dummy
tool in place of C2's (`c3/c4ctl-P.txt`), so C3 depends on *a* committed tool for its
own-work row, not on C2's verdict; C1 shares no file with either.

No harm: `tools/mado-verify.sh --selftest` `460/460` (`receipts/selftest-after.txt`); index
`indexed=56/56 missing=0 dangling=0 duplicates=0` (one new row; `receipts/nav-after.txt`,
seat ExecNavAfter); census exit 0 with the same seven W04 and one W01 as at base; the eventq
counter stays `fixtures=14/14 … TARGET_MET` with a census-only live receipt
(`w1/ExecEventqSnapshot/`); the held dispatcher entry gains an appended section only; no
config tree, service or compositor state touched.

### Capabilities (round 39)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| config-option ownership table | resolve every option key of a hyprlang config tree to its last declarer (owner file, line, layer) through the `source` graph — excluding handler calls (flag-variant binds, env/gesture) and keyed special-category fields per the host's own handler table — and label a `getoption` dump with the five divergence classes | `tools/mado-options.py` (selftest 71/71); `quality/counters/c3-r39-options.py` 11/11 at `4ec582e`; host tree: 70 options from 6 owner files (`.ufo/waves/round-39/fetch/S219.receipt.txt`) | 39 |

### Sources, saturation, planned

Sources 211 → 214 rows (S218, S219, S220; tier A; `mined`; opened 2026-10-25); S018, S162,
S173 `used-by` extended (old→new in `corpus/lessons/round-39.md`). Assimilation: the
dispatcher-surface amendment admitted re-grounded (S018, S196 re-opened); three other package
amendments not this round's theme; no staged row appended. Round-38 correction: its
"2 refused" line counts 3 refusals (r28, r29 journal, r29 socket-client), per the round-38
lesson. Domain-versus-meta ratio of the last 30 commits (criterion 60), measured at
`3628472`: **10 domain / 20 meta**. Saturation 9.0 / N=3 unchanged; retired: none.

Axis table re-derived at `362847279eccb77b22789a37cbbe3b83b205d49c` plus the round-39 records commit (one new indexed entry, criterion 64): navigation 56/56; calibration resolved-active 51/51; operability selftest 12/12.

### Planned (round 40; intent only)

1. Take one live `hyprctl getoption` dump (read-only) and merge it into the table: the §4
   labels against the running compositor, and the falsifiable consequence's live half.
2. Next shokuknow theme or considerthese proposal per the frontier.

## Round 40 - live option-table merge and the getoption native-forms entry (2026-10-25, attempt 1)

Registration `.ufo/waves/round-40/registration.md` (freeze `5e7e885`) re-registered as `registration-v2.md` (freeze `8122293`, before any data): the 64-seat wave `w1` falsified the v1 predicates (judge-leak cheat 13/13, forged log, echo selftest, seed replay, a fifth form `vec2`, a `[[BATCH]]` key injection). Lowest-axis rule: every published axis ties at its maximum (`receipts/axis-base.txt`). Round shape: one v2 wave of 64 seats, no residual call, total 64.

| Claim / axis | Before -> after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **operability** (capability) `--live` | v2 `fixtures=0/19` exit 1 at base -> see report for the data-tip receipt | `python3 -I quality/counters/c1-r40-live-v2.py --repo . --rev <rev>` | reported in the fleet report; v1 and v2 both scored |
| C2 **coverage** (sourced) native-forms entry | `admitted=0/1` at base -> see report | `python3 -I quality/counters/c2-r40-forms-entry-v2.py --repo . --rev <rev>` | reported in the fleet report; residual: fabricated self-consistent set passes |

### Capabilities (round 40)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| live option-table merge | query the running compositor with `hyprctl getoption -j` (one read verb, allowlisted keys, bounded reply) and label every declared key against its native reply with host conversions and angle inheritance | `tools/mado-options.py --live`; `.ufo/waves/round-40/fetch/census-receipt.txt` (62 agreement / 8 agreement* / 0 mismatch) | 40 |

### Planned (round 41; intent only)

1. Take the remaining package themes under PROVINCE (`ScoutMergeRest`); 2. an independent non-author re-run of both v2 counters with fresh nonces.

Axis table re-derived at `3c80537a54b4fd3b534f5cc3496a4bdc37c11371` plus the round-40 axis-line commit (two new indexed entries): navigation 58/58; calibration resolved-active 55/55; operability selftest 12/12.
