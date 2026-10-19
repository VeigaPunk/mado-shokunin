# mado-shokunin — Iteration Log

- 2026-10-14 — round 0: minted as shonen (operator directive; see MINT.md).
  Probation: >=3 verified rounds before any roster row.
- 2026-10-14 — round 1: probation wave 1 (content lanes + audits dispatched
  from the mint session; dispatch write-scopes left this LOG to the scribe
  lane). Round-1 work sits uncommitted in the working tree
  (` M SKILL.md`, `?? corpus/knowledge/`) together with these three record
  files — landed-means-committed is for the wave integrator's commit
  (observation). Deliverables:
  MADO-1 → `corpus/knowledge/hyprland-config-plane.md` (217 L by `wc -l`):
  hypr inventory, include graph (17 `source` statements, `hyprland.conf` a
  pure orchestrator), override chain proven by `hyprctl getoption`
  (`general:gaps_out` 0 via toggle, not user `looknfeel.conf`;
  `input:kb_layout` br), 192 binds = 23+4+90+50+25 closing exactly,
  separate consumers (hypridle inactive, cause UNK §12), version pins §9,
  spot-checks §13.
  MADO-2 → `corpus/knowledge/waybar-walker-plane.md` (364 L): waybar/walker/
  mako/swayosd/idle-lock plane, style-vs-module reload split
  (`config.jsonc:2`), drift-vs-stock diff §6, falsifiable decision table §7,
  unknowns §8, rejections kept §9 (SUPER+SPACE ≠ Omarchy menu vs live list),
  errata §10.
  MADO-3 → `corpus/knowledge/terminals-and-omarchy.md` (179 L): only
  Alacritty installed of the four terminals; theme plane owns colors outside
  user configs (`theme.name` → matte-black); omarchy skill anatomy (392 L)
  incl. hooks drift — skill text shows flat files where the host has five
  `*.d` dirs (§7).
  Fourth deliverable → `SKILL.md` distillation (no lane header in the diff;
  authoring lane unknown to this scribe): seed 22 → 186 L (169 insertions,
  `git diff --stat`) — who-owns-it table 19 rows, read-only probe table
  15 rows, 6 mutating commands fenced operator-only, omarchy-boundary
  routing table 5 rows; every row citing MADO-N § anchors or omarchy-skill
  line anchors.
  Scribe verification (this entry; all commands re-run 2026-10-14):
  seed-vs-tree counts — `git show 74d3b7b:SKILL.md | wc -l` → 22 with 0
  table lines; tree SKILL.md → 186 L, 45 table lines across 3 tables;
  anchor spot-checks resolve — omarchy skill `wc -l` → 392 and `:300-305` =
  window-rules wiki re-fetch, `hyprland.conf:29` = `source =
  ~/.config/hypr/ai-usage.conf`; live pins corroborated — `hyprctl version`
  → 0.56.2, `omarchy version` → 3.8.3; probe-tool existence sweep 10/10 on
  PATH (hyprctl omarchy makoctl busctl grim slurp hyprpicker systemctl pgrep
  jq). Records written by this scribe: corpus/README.md coverage map 3 rows;
  SCORECARD move-log round-1 rows (coverage, operability) with counting
  commands.
  Observations: (a) the note files end without a trailing newline, so editor
  line counts (218/365/180, as quoted in SKILL.md "Round 1 sources") =
  `wc -l` + 1 (217/364/179) — quoting convention, not a defect, but counts
  should name their command; (b) `SHONEN.md` deviates from the canonical
  seed (PROTOCOL.md:419-428): header "# mado-shokunin — probation checklist"
  vs "# <name> — Promotion checklist", boxes paraphrased despite the file's
  "verbatim shape" claim — shared by all four lanes minted 09:50 today
  (header shape checked, contents not read); mint-time defect, flag for the
  operator / promotion gate — outside this entry's write scope;
  (c) `corpus/lessons/` is still empty — no `lessons/round-1.md` landed
  in-repo this round (CORPUS.md layout expects per-round lessons; the wave's
  knowledge landed under `knowledge/` instead).
  Unknowns: which lane authored the SKILL.md distillation; whether wave
  artifacts exist outside this repo (`.ufo/` checked shape-only, contents
  not read).
  Falsifiable next-iterations: an executable checklist + a first committed
  verdict gate (the operability ceiling named in SCORECARD round 1);
  verifier wiring for the SHONEN boxes; `lessons/round-2.md` to start the
  lessons ledger.
- 2026-10-14 — round 2: depth move — the live-verification layer (dispatch
  per `plans/round-2.plan.md`, ufo-round-plan-v1; axis set depth /
  operability / freshness; move = depth, anti-claim: hyprctl unavailable →
  layer documented as recipe + file-byte evidence only). Round-2 work sat
  uncommitted in the working tree from the content lanes; this scribe
  re-verified the claims it records and lands the round commit with this
  entry (landed-means-committed). Deliverables:
  MADO-R2-1 → `corpus/knowledge/hyprctl-verification-layer.md` (280 L by
  `wc -l`; editor view 281, no trailing newline): MADO-1's live layer —
  56 `getoption` claim→live pairs (39+15+2) + 9 non-getoption pairs, each
  with declaring chain and falsifiable class (agreement / agreement* /
  live-default / mismatch / config-only); census 52 agreement (6 starred =
  ownership proofs: toggle owns gaps/border, local owns `kb_layout`, theme
  owns borders), 4 live-default, **0 mismatch**; `set` flag as declarer
  discriminator; config-only surface §6 with a new drift finding — local
  `~/.config/hypr/envs.conf` sourced by nothing, its 3 NVIDIA vars unset
  live; substrate byte-identity vs MADO-1 §2 proven by sha256 (§7); read
  verbs whitelisted, mutating verbs banned (§0); anti-claim recipe §8;
  append-only errata §9 carries an unapplied MADO-1 candidate (write-scope
  discipline — correctly deferred, now applied by R2-3 as R2-E1).
  MADO-R2-2 (note self-labels MADO-4) →
  `corpus/knowledge/keybind-rule-semantics.md` (315 L by `wc -l`; editor
  view 316): 192 binds across 5 files reconcile 192/192 against live
  `hyprctl binds -j` — flag counters identical file-vs-live
  (d190/e14/l26/m2/r1), full modmask histogram (13 masks), order-
  insensitivity measured (both orderings → mask 73); 24-dispatcher
  inventory with semantics `[INF-docs]` — no dispatcher fired, claim
  boundary stated; window-rule evaluation order measured through the
  include graph (79 sourced statements) + matching-order decision table;
  live divergence finding §4.6: 2 of 3 Alacritty windows still carry
  `default-opacity*` → opacity product ≈0.9409/0.81 darker than intended,
  cause `[UNK]`; docs-drift caveat (current wiki lua-era, host 0.56.2
  still parses hyprlang; 0.54 archive cross-checked).
  MADO-R2-3 → append-only R2-E blocks on the three round-1 notes (4 / 2 /
  4 items): orphan `envs.conf` addition (R2-1 §9 candidate applied);
  mako config byte cell corrected 50→119 B (content sha unchanged —
  transcription error); SUPER+SPACE rejection sharpened to
  verified-false-direction (stock SUPER+SPACE → Walker, SUPER ALT+SPACE →
  Omarchy menu); grok-bot autostart re-measured absent at 11:00, cause
  `[UNK]`, no conclusion drawn; round-1 body length pins settled as a
  command-naming convention (217/364/179 by `wc -l` vs editor
  218/365/180); everything else re-measured identical.
  Fourth deliverable → `SKILL.md` distillation round-2 section (no lane
  header in the diff; authoring lane unknown to this scribe): 186 → 240 L;
  claim→evidence routing table (4 rows: file bytes / hyprctl live read /
  `[INF-docs]` / consumer-side probe — each licensing and barring claims)
  + divergence vocabulary + 6 mutation-free safety rules (read-verb
  whitelist, no firing, sha256 boundary proof, session material
  shape-only, unverifiable→UNKNOWN, scratch outside the substrate); the
  env-vars routing row corrected to the orphan finding with `printenv`
  probes; re-verified footer dated today.
  Scribe verification (this entry; all commands re-run 2026-10-14
  14:11–14:14 UTC, raw log `/tmp/mado-scr-r2b/`):
  counts — `wc -l` → 280 / 315 (new notes) and SKILL.md 240; awk data-row
  counts → §3 = 39+15+2 = 56, §4 = 9, §5 = 6, dispatcher table = 24;
  class census → 51 `agreement` + 6 `agreement*` + 5 `live-default` over
  §3+§4 classed rows (0 `mismatch`; consistent with the note's §3-only
  census 52 incl. 6 starred + 4 live-default); before-state —
  `git show 65a2254:SKILL.md | wc -l` → 186,
  `git show 65a2254:corpus/README.md | grep -cE '^\| .knowledge'` → 3,
  `git ls-tree 65a2254 corpus/knowledge/ | wc -l` → 3; live corroboration
  (read verbs only) — `hyprctl binds -j | jq length` → 192, flag counters
  locked 26 / repeat 14 / release 1 / mouse 2 / has_description 190,
  `hyprctl configerrors` → empty rc=0, `hyprctl version` → 0.56.2 commit
  `efb5099…`, getoption spot-checks `general:gaps_in` → `custom: 0 0 0 0`
  / `input:kb_layout` → `br` / `input:touchpad:scroll_factor` →
  `float: 0.400000` / `dwindle:preserve_split` → `int: 1`; freshness —
  `sha256sum ~/.config/hypr/hyprland.conf | cut -c1-12` →
  `4f52854a3c14` (= MADO-1 §2 = R2-1 §7), `printenv GDK_SCALE` → `1`,
  `NVD_BACKEND` → unset (orphan confirmed live); errata counts —
  `grep -c '^\- \*\*R2-E'` → 4 / 2 / 4. Records written by this scribe:
  corpus/README.md coverage map +2 rows (R2-1, R2-2) and round-2 addenda
  on the three round-1 rows; SCORECARD move-log round-2 depth row with
  the counting commands.
  Observations: (a) SKILL.md's round-2 sources paragraph quotes
  `keybind-rule-semantics.md` as "313 by `wc -l`" → measured **315**
  (the R2-1 quote, 280, is correct) — stale count in the distillation;
  errata candidate for the SKILL lane, outside this entry's write scope;
  (b) the keybind note self-labels MADO-4 while its assignment is
  MADO-R2-2 — both carried in the records (cosmetic, but roster-roster
  collisions bite at promotion time); (c) `corpus/lessons/` is still
  empty — no `lessons/round-2.md`; round-1's next-iteration item unmet a
  second round; (d) both new notes end without a trailing newline (same
  quoting convention as round 1 — every count above names its command);
  (e) no audit-lane verdicts are recorded in-repo this round (round 1's
  commit carried "admitted 3x ADMIT"); this entry records scribe
  verification only, audit verdicts remain with the integrator.
  Unknowns: which lane authored the SKILL.md round-2 section; whether
  round-2 audit lanes ran and where their verdicts live; `.ufo/` not
  inspected this round.
  Falsifiable next-iterations: promote R2-1 §8's anti-claim recipe + R2-2
  §5's reconciliation method into a committed executable verdict gate
  (`corpus/scripts/` — the round-1 operability ceiling still stands:
  `find corpus -name '*.sh'` → 0); fix the SKILL.md 313→315 quote;
  `lessons/round-2.md`; SHONEN box verifier wiring still open.
- 2026-10-14 — round 3: depth + coverage — the bar/launcher plane gets
  round-2's semantic treatment (MADO-R3-1) and the lane's first
  end-to-end task lands: a full config-health report across all four
  planes (MADO-R3-2); SHONEN gate evidence via a no-oral-context
  executor test (MADO-R3-4) against the SKILL sufficiency upgrade
  (MADO-R3-3). Dispatch per `plans/round-3.plan.md` (ufo-round-plan-v1;
  axis set depth + coverage; anti-claim: waybar introspection
  unavailable → file-byte evidence class only, labeled — branch
  confirmed live: no query verb in waybar 0.15.0, R3-1 §2.3). Round-3
  work sat uncommitted in the working tree; this scribe re-verified the
  claims it records and lands the round commit with this entry
  (landed-means-committed). Deliverables:
  MADO-R3-1 → `corpus/knowledge/waybar-walker-semantics.md` (455 L by
  `wc -l`; editor view 456): 13 tables / 89 data rows — module-by-module
  semantics for all 19 modules (§3.1 2 + §3.2 8 + §3.3 9; each row
  Displays/Source/Actions/Fails/Live under the OBS/MAN/RUN/INF/UNK
  legend), config-vs-man table §2.1, introspection ledgers §2.3/§6.8
  (anti-claim applied), signal bus §4 (RTMIN+7…11 consumers + 5
  producers; delivery re-proved: `pkill -x -RTMIN+11` → caught=45 under
  procps-ng 4.0.7, contradicting the `ai-usage:150-153` docstring),
  style map §5 (theme owns exactly fg/bg; 4 literal `#a55555` sites stay
  theme-independent), walker key-by-key §6.2 vs the 298-L packaged table
  incl. the `[columns]` correction §6.3 (grid columns, not "queried
  providers" — the user file's own inline comment is wrong), launch/
  restart paths + standing binds §6.7, failure modes §7, 7 divergence
  candidates §8 (voxtype `trap 'kill 0'` producer hazard — direct
  invocation killed the caller, exit 143 contained re-run; battery has
  no device on this host; omarchy version two-pin 3.8.3 vs v3.8.4),
  unknowns §9 (11), boundary proof §10 (4 substrate sha256 equal
  before/after, mtimes unchanged, no network command executed).
  MADO-R3-2 → `corpus/knowledge/config-health-report-r3.md` (550 L by
  `wc -l`; editor view 551): e2e pass 2026-10-14 14:40–14:48 UTC — §1
  re-checks all 20 round-1/2 claim families (all stand); zero config
  drift by sha256 since rounds 1–2; round-2 live layer holds: 57/57
  `getoption` re-measured byte-identical, **0 mismatch** (Appendix A:
  46 `agreement` + 6 `agreement*` + 4 `live-default` + 1 extra
  `rounding_power`); binds 192, flag counters, 13-mask histogram,
  24 dispatchers, 79 rule statements all equal; divergence register
  F1–F10 classed 1×S1 (F1 hypridle absent with journal-proven boot
  start — stop time/cause `[UNK]`; the declared 150 s/152 s idle-lock
  chain has no consumer) + 2×S2 (F2 Alacritty opacity-tag anomaly
  reproduces on the same PIDs, age ordering contradicts a stale-window
  story; F3 orphan NVIDIA env trio on a measured RTX 5070 host) + 7×S3
  (F4–F10), each with an operator recommendation (§7); record-level
  corrections forwarded, not applied (F8 → R2-1 §9 `wl_socket`;
  mako 50 B provenance resolved — the cell was the symlink's own size,
  config → theme `mako.ini`); new read-only `layers` verb added to the
  whitelist.
  MADO-R3-3 → `SKILL.md` sufficiency upgrade, 240 → 396 L by `wc -l`
  (`git diff --stat HEAD`: +240/−83): severity scale S1/S2/S3 from
  R3-2 §6, `layers` added to the hyprctl read-verb row, sibling round-3
  notes integrated, round-3 section self-labels MADO-R3-3 (`:377-381`);
  round-2 observation (a) resolved — the stale "313 by `wc -l`" quote
  fixed to 315 with a note at `:396-397`.
  MADO-R3-4 → `corpus/knowledge/executor-test-sufficiency.md` (196 L by
  `wc -l`; editor view 197): no-oral-context executor test — SKILL.md
  the only domain source, one claim verified end-to-end
  (`general:gaps_out` → `{"custom":"0 0 0 0","set":true}`, toggle-owned);
  per-step sufficiency classes over steps 0–9 (SUF-EXPLICIT ×8, one with
  a SUF-DERIVED extension; SUF-DERIVED ×1; N/A ×1); verdict **"Sufficient,
  end-to-end, against the version read"** (tested SKILL `016ecd68…`
  374 L, sha-pinned by 20-s polling); 4 gaps with in-pass resolutions;
  SKILL version ledger (5 shas, 14:38–14:57Z) whose UNK(5) asks the
  round commit to freeze the final SKILL sha — **this commit freezes
  `ef4c29e3…` (396 L)**, matching the note's post-landing errata
  observation exactly.
  Scribe verification (this entry; all commands re-run 2026-10-14
  15:38–15:47 UTC, raw log `/tmp/mado-b4-r3b/verify.log`):
  counts — `wc -l` → 455 / 550 / 196 / 396 (notes end without a trailing
  newline, editor views +1 — same convention; every count names its
  command); R3-1 table census `grep -c '^|'` → 115 = 13 headers +
  13 separators + **89 data rows**; R3-2 96 = 3 + 3 + **90** (§1
  coverage 20 + §2.1 13 + Appendix A 57); Appendix A class census
  `awk … \| sort \| uniq -c` → 46 + 6 + 4 + 1; F headers
  `grep -c '^### F'` → 10, S3 tally → 7; SKILL diff +240/−83;
  executor-cited anchors resolve in the frozen sha (`:48` claim text,
  `:296` embedded pin). Live corroboration (read verbs only) —
  `hyprctl version` → 0.56.2 `efb5099…`; `hyprctl -j binds | jq length`
  → 192; `hyprctl -j getoption general:gaps_out` →
  `{"custom":"0 0 0 0","set":true}` (the executor's claim row, re-run
  independently); `sha256sum ~/.config/hypr/hyprland.conf | cut -c1-16`
  → `4f52854a3c143dcf` (= MADO-1 §2 = R2-1 §7 = R3-2 §2.1 = SKILL pin);
  `pgrep -x hypridle` → rc=1 (F1); clients tags reproduce F2
  (3982970/1784450 flagged, 275049 clean); `instances` → `wl_socket`
  `"wayland-1"` (F8); `printenv NVD_BACKEND` → unset, rc=1 (F3); layers
  level 2 → `waybar` pid 1707, level 0 → `wallpaper` 1710;
  `waybar --version` → v0.15.0, `walker --version` → 2.17.0, PIDs
  1707/1808; tray `RegisteredStatusNotifierItems` → `as 0`; `makoctl
  mode` → `default`; `/sys/class/power_supply/` → 0 entries; omarchy
  two-pin re-measured (3.8.3 / v3.8.4). Records written by this scribe:
  corpus/README.md coverage map +3 rows (R3-1, R3-2, R3-4); SCORECARD
  move-log round-3 depth + coverage rows with the counting commands;
  SHONEN.md regenerated to the canonical seed with marks + verifier
  names (observation (d)).
  Observations: (a) R3-2 §0's verdict says "**6× S3 (F4–F10)**" but the
  register holds 7 S3 headers (tallies above) — an internal off-by-one
  in the summary only; the per-finding severities are consistent;
  erratum candidate for MADO-R3-2 §10, not applied (write scope).
  (b) SKILL.md `:103` and `:137` spell the tray bus name
  `fr.arrouillard.waybar` (double r); the live name is
  `fr.arouillard.waybar` (`busctl --user list`; R3-1 §1) — erratum
  candidate for the SKILL lane, not applied. (c) R3-1 §8's 7 divergence
  candidates on the round-1 waybar note and R3-2's F8 candidate for
  R2-1 §9 remain unapplied — correct append-only discipline (candidates
  live in the notes that found them), now spanning two rounds.
  (d) SHONEN.md mint-shape defect (round-1 observation (b)) healed this
  round: the file deviated from the canonical seed (paraphrased boxes,
  "probation checklist" header, "verifier: TBD" placeholders); it is
  regenerated verbatim per PROTOCOL.md:419-431 with marks per the :430
  spec (`[x] <verifier-id>` / `[~]` + resolvable pointer, one indented
  evidence line per box) — 2× `[x]` (MADO-R3-4, the non-author executor
  lane) and 2× `[~]` (e2e task, PROVINCE accuracy — no auditor verdict
  in-repo this round). The superseded text remains at the round-0
  commit. (e) `corpus/lessons/` is still empty — third round running;
  the round-1/2 next-iteration items are unmet a third time. (f) the
  committed verdict gate (`corpus/scripts/`) still does not exist
  (`find corpus -name '*.sh'` → 0) — the round-1 operability ceiling
  stands a third round. (g) severity-label caveat carried: the
  executor's row was classed S1 under the pre-replacement scale; the
  SKILL's adopted scale (R3-2 §6) re-labels it S3 — both records state
  this.
  Unknowns: round-3 audit-lane verdicts are not recorded in-repo (same
  as round 2 — they remain with the integrator); whether round-3 lanes
  wrote reports outside the repo (`.ufo/` not inspected this round);
  the SKILL lane's write window is closed as of this pass (last write
  14:57:22Z, scribe pass from 15:38Z) but the sha is only truly frozen
  at commit time.
  Falsifiable next-iterations: apply the pending errata (R3-1 §8's 7
  candidates to `waybar-walker-plane.md`; F8 to
  `hyprctl-verification-layer.md` §9; R3-2 §0 6→7; SKILL `arrouillard`
  typo); commit the executable verdict gate (`corpus/scripts/`);
  `lessons/round-3.md`; land an auditor verdict in-repo so the
  PROVINCE-accuracy box can move `[~]` → `[x]`; all four SHONEN boxes
  now carry marks — promotion itself stays the operator/gate decision
  per PROTOCOL.
- 2026-10-14 — round 4 (training r3): idle/lock plane (355 L); box-3 CLOSED (VER-M3: config-health report reproduces); box-4 stays [~] (VER-M4: §8 re-run needed per the named verifier); reproduction package for non-author re-runs. Axis moved: depth + calibration. Verifiers: VER-M3 | VER-M4. 32-lane wave (27+1+4 after an alibaba filter failure rerouted 4 lanes to hyper — recorded).
- 2026-10-14 — round 5 (training r4): first gate mado-verify.sh (selftest + live verdict); walker-deep note; SHONEN box 4 CLOSED by VER-M4B — PROBATION COMPLETE 4/4. Axis: operability + calibration. Verifiers: VER-M4B.
- 2026-10-14 — round 6 (training r5): gate proven to fail then hardened: selftest 28->53, the hardened gate kills 10/10 of tameshi's mutants; omarchy drift watch + remaining-planes census landed. Axis: operability. Verifiers: VER-M6 | AUD-M6.
- 2026-10-14 — round 7 (training r6), lane M7-1: `tools/mado-verify.sh` gains `--regression` — replays the round-6 mutation case against the gate's own recorded revision (the two MADO-R7 blocks excised; derived-target sha256 `c4c1afb7…a5171` proven identical to the revision whose table the record carries) with tameshi's 10-defect spec pinned at `c7ee75b9…1dd8` (written from an in-gate heredoc, sha re-checked on the written bytes) and suite `bash "$MUTANT" --selftest`. PASS requires all ten recorded kills, 0 flips, 0 inconclusive, control GREEN, `MUTATE_RESTORE: OK`, target sha unchanged — the plan §(a) `killed-delta<=1` tolerance is deliberately not applied (the target is byte-frozen, slack would hide a lost kill). Selftest 53 → 89 (+36: engine band/refusal cases on a hermetic stub runner, spec + derived-target byte checks, usage refusals, harness-missing SETUP). Runs: `bash tools/mado-verify.sh --selftest` → 89/89 rc 0; `bash tools/mado-verify.sh --regression` → `MADO_REGRESSION: PASS` 10/10 kept-evidence run under `/tmp/mado-verify-regression.ZswQEe` (11.99 s); a one-line widening outside the blocks → SETUP rc 2 + REGRESSION_RECUT hint; `--no-live` → CLEAN (17 pass, 2 notes), live → CLEAN (35 pass, 4 notes) — the verify path is byte-identical to `c4c1afb7`, which is the excision proof. Harness revision moved mid-round (`b56c6e57…22bcb` → `cf41efaa…242c75`; tameshi lane concurrent): printed as provenance, not gated, and the case still reproduced 10/10 under it. `--target/--defects/--suite` refused (usage, exit 2). Files: `tools/mado-verify.sh` only (+569/−0).
- 2026-10-14 — round 7 (training r6): gate --regression mode shipped; theme/wallpaper plane; walker live surface; the hardened gate verified under regression. Axis: operability + coverage. Verifiers: VER-M7 | AUD-M7.
- 2026-10-14 — round 8 (training r7): post-hardening sweep vs the 10/10 expectation; the drift watch arm + snapshot-diff mode; zero config mutation held. Axis: operability + freshness. Verifiers: VER-M8 | AUD-M8.
- 2026-10-14 — round 9 (training r8): theme plane as gate arms; walker deep-r9; the snapshot-diff mode's first real receipt across the round's own edits. Axis: coverage + operability. Verifiers: VER-M9 | AUD-M9.
- 2026-10-14 — round 10 (training r9): the arc synthesis (re-derivable; the gate-evolution ladder 28->268 selftest across 5 revisions independently CONFIRMED cell-for-cell); the gate standing-use runbook + the regression mode's first cadence receipt. Axis: calibration + operability. Verifiers: VER-M10 (cell-for-cell) | AUD-M10.
- 2026-10-14 — round 11 (training r10) — THE ARC CLOSES. The closeout round
  (charter `plans/round-11.plan.md`, 353 L / `4bde28aa5eef9600…`, committed
  with the round-10 landing): verify the round-10 handoff, settle every open
  item, freeze the revision, commit the arc-end record. This entry is the
  record lane's (SCR-M11) arc-end record; every number in it was re-measured
  read-only at the frozen revision (2026-10-14 21:33–21:35Z UTC; raw logs
  `/tmp/w11-scr-m11/`), and every artifact it names was read at its landed
  bytes 21:33Z–22:0xZ. Deliverables as landed in-window:
  M11-1 → `corpus/knowledge/closeout-r11.md` (closeout note; landed name —
  the plan's `arc-closeout.md` never landed, both values carried, AUD-M11
  F1): 294 L by `wc -l` (editor view 295) / 19,250 B / `670b5a396ecb8789…`;
  §1–§7 the M11-1 note, §8 the M11-3 append. It carries: the round-10
  handoff verification ((a10) yes — `arc-synthesis.md` 387 L /
  `a5b4833141461810…`; (b10) yes — `gate-standing-use.md` 361 L /
  `aaa2e625253e881e…`; (c10) partly — the LOG/SCORECARD one-liners landed,
  README/lessons/⟨PENDING⟩/errata/AGENTS did not), the ladder + battery
  receipts (§2), the terminal disposition ledger (closed / operator-owned /
  unknown — "carried" absent; every item named), the freeze pins and the
  handoff (§7), five open findings F1–F5 with both values.
  M11-3 → the closeout's §8 append (gate final-state receipt; window
  21:33:40–21:36:01Z): the whole battery re-run — selftest 268/268;
  `--no-live` CLEAN 29/4; live DIVERGED 3/49; regression PASS 10/10;
  snapshot pair `MADO_DIFF: CHANGED (rows 41→60; relabeled=7 appeared=20
  vanished=1; scope file-plane→live)` + self-diff control `SAME`; gate sha
  byte-identical before/after.
  M11-2 → `corpus/lessons/round-10.md` (226 L / 16,423 B /
  `d7b4708e864fca29…`): round 10's lesson, one wave late (the fleet
  pattern) — the arc's FIRST lessons entry after ten rounds of
  `corpus/lessons/` = 0; carries the `## Gate` section (candidates /
  admits / rejects with reasons) and a non-author spot-check (SC-A:
  battery + ladder re-derived; admits and rejects both covered).
  M11-4 → `SKILL.md` "Round-11 — the arc's end: final pointers" append,
  1,424 → 1,545 L by `wc -l` (`e9e67efe…` → `b9134091c031fade…`; +122/−1):
  the pointer map + reading route; it carries the F5 correction (both
  values) append-only.
  PACK-M → `plans/completion-evidence.md` (196 L / `e63272c4b555213b…`):
  the rounds-2–11 completion pack for the parent (one line per round,
  SHONEN status, debts; nothing re-adjudicated).
  Seat reports: `reports/r11-aud-m11.md` (AUD-M11; window 21:30–21:49Z;
  C1/C2 + R1–R7 PASS; live NAMED; findings F1 closeout naming / F2
  +90 vs +89 / F3 waybar / F4 harness; its own scratch-glide slip
  `gate.sha.after.txt` — visible in this lane's poll 21:36:42–21:37:02Z,
  removed by its own lane, no byte moved); `reports/r11-ver-m11.md`
  (VER-M11; ladder complete to the frozen revision, 20/20 + r10 4/4 cells;
  F0 = the waybar root cause — journal `systemd-coredump`, waybar pid
  3036215 core-dumped 18:21:17 −03 = 21:21:17Z; F4 = the synthesis
  epilogue still owed).
  Scribe verification (this entry; commands at 21:33–21:35Z UTC):
  gate ladder re-derived per arc commit — five distinct blobs + two
  identity rows: r5 `d7edaab4bf108625…` 1,098 L / 45,334 B; r6
  `c4c1afb75dd1c8aa…` 1,186 L / 50,126 B; r7 `90d50cdd4d18410b…` 1,755 L
  / 75,771 B; r8 `7da4ec5013583c91…` 2,887 L / 131,612 B; r9 and `f7bfc9f`
  `93e43f8fe8b9bdd4…` 3,231 L / 150,103 B; rounds 1–4 no gate file (the
  piped command reads the empty blob) — every cell equal to the records
  and to VER-M11/AUD-M11.
  Frozen revision's whole row: `--selftest` → `MADO_SELFTEST: 268/268
  assertions passed` rc 0; `--no-live` → `MADO_VERIFY: CLEAN (29 pass, 4
  notes; file plane only)`, boundary `bb2639d9a980…`; live → `MADO_VERIFY:
  DIVERGED (3 fail, 49 pass, 8 notes)` — the three waybar rows
  (`live.waybar.process/.layer/.tray`); `pgrep -x waybar` rc 1 directly;
  root cause now on record (VER-M11 F0: core dump 21:21:17Z; cause `[UNK]`;
  no lane touched it; the bar's restart is operator-owned); `--regression`
  → `MADO_REGRESSION: PASS` (target `dc7c4141449891cd…`, spec
  `c7ee75b97c38ac8f…` match, table 10/10, flips 0, `MUTATE_RESTORE: OK`;
  harness `75ed934d…` printed as provenance vs recorded `b56c6e57…`);
  snapshot pair → `MADO_DIFF: SAME (rows 41→41; all counters 0)`. Gate sha
  identical before/after every run.
  Live pins (read verbs only, 21:35Z): `hyprctl version` → 0.56.2
  `efb5099…`; `hyprland.conf` `4f52854a3c143dcf`; binds 192;
  `configerrors` empty rc 0; `wl_socket` `wayland-1`; `pgrep hypridle`
  rc 1; walker 1203471 / elephant 1203474 / swaybg 1203358; `NVD_BACKEND`
  unset; omarchy 3.8.3; theme Matte Black.
  Citation spot-check: `SKILL.md:1314` cites AUD-M9 as `7ad8eccdd8d213a5…`;
  the landed blob reads `866272eeda09bc08…` (166 L) — carried as F5, both
  values; the M11-4 append adds the correction, the base line stands.
  Record family movement (this lane's files, applied with this entry):
  LOG 301 L → 437 L (this arc-end entry); SCORECARD 22 L → 30 L (rows 4–5
  replaced with the drafts' ready text, pins re-measured; rows 6–9
  completed from the records + re-derived ladder cells; the malformed
  round-10 row completed; the round-11 final row, the arc-end statement
  and the live caveat added). Other record-family files as measured at
  this write: README 19 L / `2dd274f5e2…` (8 note rows — 22 notes now
  stand in `corpus/knowledge/`, unrowed), synthesis 387 L unchanged (the
  epilogue VER-M11 F4 still owed), standing-use 361 L unchanged (the
  revision line + F4 path correction owed), walker-deep 617 L /
  `0982ba066c…` unchanged (§10/§11 errata owed), AGENTS 6 L unchanged
  (pointer owed), the draft ⟨PENDING⟩ sets unchanged — the settlement
  (M11-2) remains the named carrier; the round-11 commit is the remaining
  landing step (HEAD `f7bfc9f` + the wave's dirty set at this write).
  The closeout round's three trend verdicts (plan §(c)): expansion —
  unchanged, by design (no new ground; the arc closes at 22 notes in
  `corpus/knowledge/`, no new frontier opened or promised); quality —
  improved where the settlement repaired with evidence (SCORECARD rows
  paid; the arc's first lessons entry; the SKILL pointer append; the
  closeout + its seat reports), with the harm-side named, not smoothed:
  F1 `…a5171` now carries ×2 new occurrences in the round-11 set
  (closeout `:77`/`:83`) — erratum owed; F4 synthesis epilogue owed; F5
  stale citation standing in the base SKILL line; the live plane moved
  (waybar crash); discernment — the verification sample AGREED cell-for-cell
  (this lane's ladder + battery; M11-3's battery; AUD-M11 C1/C2 + R1–R7;
  VER-M11's ladder 20/20) and the disagree side is the five findings, each
  reproduced with both values; the non-author spot-check landed with the
  lessons entry (SC-A) — the ten-round-standing harm-side fact (no
  lessons, no non-author check) is repaired this round.
  Freeze pins: gate revision `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`
  (3,231 L / 150,103 B by `wc -l`/`wc -c`; unchanged rounds 9 → 11); the
  synthesis `corpus/knowledge/arc-synthesis.md` (387 L /
  `a5b4833141461810…`); the standing-use note
  `corpus/knowledge/gate-standing-use.md` (361 L / `aaa2e625253e881e…`);
  the closeout `corpus/knowledge/closeout-r11.md` (294 L / `670b5a396ecb8789…`).
  THE ARC-END STATEMENT: the arc is closed. The gate is handed over at the
  frozen revision `93e43f8f…` — the standing verdict is `bash
  tools/mado-verify.sh` (live, read-only; the contract, invocation map,
  cadence and residual ledger live in
  `corpus/knowledge/gate-standing-use.md`). No further round opens.
  Probation 4/4 `[x]` since round 5 (VER-M3 | VER-M4B; `SHONEN.md`);
  promotion is the operator/integrator decision, never self-declared.
  Observations: (a) the live DIVERGED reading is a session-state fact with
  its root cause now on record — waybar core-dumped at 21:21:17Z (VER-M11
  F0); reconciliation is operator-owned (restart the bar); every `52 pass`
  live figure in the records is stale as of 21:21:17Z; (b) the registered
  findings are the round's disagree side and stay owed as appended errata
  (F1 including its new occurrences, F2, F3, F4, F5 — none smoothed);
  (c) the closeout landed under `closeout-r11.md`, not the plan's
  `arc-closeout.md` — the round-10 rename precedent repeats; both values
  carried; (d) the drafts' r6–r9 §4c SCORECARD "ready text" claim is
  verified false this pass — they carry ⟨fill⟩ templates; only r4 (3 rows)
  and r5 (2 rows) were applyable as written; the rows added here fill the
  templates from the records + re-derived ladder cells; (e) the settlement
  appends (README rows / synthesis epilogue / standing-use revision line /
  ⟨PENDING⟩ closures / walker-deep errata / AGENTS pointer) were measured
  NOT yet on disk at this write (22:08Z) — recorded as the named
  remainder, never as landed.
  Unknowns: whether the settlement appends land between this write and the
  commit; the round-11 commit sha (none observed; HEAD `f7bfc9f` at this
  write); waybar's crash cause and return time; whether the operator takes
  the promotion decision; `.ufo/` not inspected this round.

## 2026-10-15 — fleet round-1: admitted-corpus navigation

Trigger: the explicit fleet-round-1 steer follows the closed training arc.
At base `bb08dd57f4b48bfb001a178e57b9c25e7040447f`, the committed
`corpus/README.md` routes 8 of 22 existing knowledge notes; 14 are missing
from the index, with no dangling or duplicate targets. The reproducible
commit-based counter is in `SCORECARD.md` under “Counting command”; its
baseline invocation exits 1 and prints `indexed=8/22 missing=14 dangling=0
duplicates=0 coverage=3.6364/10`. This is navigation debt already named at
historical `LOG.md:383-388`, not a new desktop-behavior discovery.

The inherited scorecard had no numeric axis rows. This round initializes
bounded local sub-axis scores: admitted-note reachability 3.6364/10 and
the existing hermetic suite pass fraction 10/10. Only the lower navigation
subset is selected; no whole-domain completeness, axis saturation or
promotion is inferred. See `SCORECARD.md` fleet-round-1 scope and rubrics.

Initial uncommitted work was same-scope partial round work: the corpus
warning, the `SKILL.md` fleet-round-1 navigation appendix and the four
`SHONEN.md` `[~]` independence caveats. Preserve and complete it; no reset
of those bytes and no sweep of sibling-owned files. The historical
scorecard's “no further round” and 4/4 `[x]` frame does not supersede this
steer or supply current outside-lane promotion authority.

One native OMP `task` call dispatched MadoPlan (planner), MadoConnect
(connector), MadoExecConfig/MadoExecGate/MadoExecSynthesis (three
executors), MadoScribe (scribe), MadoRecon (scout), MadoReview (reviewer)
and MadoCritic (critic). All roles use the existing host routing; no model
parameter or routing edit. This is the canonical Shokunin host mapping,
not a claimed validated generic UFO wave. L1 alone integrates repo files.

Re-verification at the unchanged gate revision
`93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`:
`bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 268/268 assertions
passed`, exit 0; `bash tools/mado-verify.sh --no-live` → `MADO_VERIFY: CLEAN
(29 pass, 4 notes; file plane only — live layer skipped: --no-live)`, exit
0, counts `pass=29 fail=0 unknown=0 skip=8 note=4`, read-only boundary
`bb2639d9a980…` PASS. These are scoped results, not live desktop health.

Operator question appended to `.ufo/l0-questions.md`, identified by
`mado | round-1 | Ratify the relaunched round namespace, bounded score
rubrics and native craft dispatch shape`: no counter, driver, route table
or domain-tree changes; integrator owns that question's durable commit.

## 2026-10-15 — fleet round 1 interactive cutover: candidate retained, dispatch blocked

Motivating evidence: initial `git status --short --branch` showed same-scope
uncommitted LOG/SCORECARD/SHONEN/SKILL/corpus-index changes plus
`corpus/lessons/round-1.md`; HEAD was
`bb08dd57f4b48bfb001a178e57b9c25e7040447f`. Local `.ufo/` held only the
current interactive session material, not a landed fleet-round report or
receipt. Native session bodies were not read or swept into a commit.
The prior headless launch counter is not a completion. Historical training
rounds and reports were preserved; this is continuation of fleet round 1.

L1 plan saved before implementation:
`.ufo/plans/fleet-round-1-wwkd.md`. Canonical UFO §0/§5 and the full
Shokunin protocol load order, fleet read-only MISSION/AXES, and lane
SKILL/PROVINCE/QUALITY/MINT/SCORECARD/LOG were read. Current operator
instructions supersede the inherited push and nine-adviser dispatch frame.
No push, shared-ledger write, global configuration edit, route overlay,
new L1, native-session mutation or compositor mutation was performed.

Inherited candidate preserved: 14 missing-note rows, seven province routes,
Frontier limits, SKILL entry/filename correction, four SHONEN `[~]`
independence caveats and the fleet-round-1 lesson. No knowledge note or
gate implementation was rewritten. Append-only lesson/SKILL corrections
now qualify the inherited “completion”/“Admit” wording as provisional and
explicitly supersede the lesson's push requirement. This entry also
supersedes any inference from the preceding LOG entry that its old
nine-adviser batch meets the current dispatch contract.

Baseline re-measured, not recalled:
`.ufo/evidence/fleet-round-1/navigation-baseline.txt` records
`revision=bb08dd57f4b48bfb001a178e57b9c25e7040447f indexed=8/22 missing=14 dangling=0 duplicates=0 coverage=3.6364/10`,
exit 1. Candidate consumer smoke:
`.ufo/evidence/fleet-round-1/navigation-smoke.json` records 22/22 indexed,
zero missing/dangling/duplicates, seven province routes and 54 local links
with no broken or outside-lane target. The actual SKILL → index →
idle/lock note reading path reached config provenance, timing inference,
UNKNOWN transitions and session-turnover E2; no actuator was invoked.
The throwaway smoke initially skipped two table headers when only one
matched its filter; correcting that parser, not repository content,
completed the smoke. No permanent source-text test was added.

Dispatch evidence: exactly 32 honestly distinct scopes saved in
`.ufo/waves/fleet-round-1-interactive/spec.json` (22 note audits,
seven surface-route audits, connector, admission critic and provenance
scribe). Canonical `node .../scripts/ufo-swarm-wave.mjs plan --spec <spec>`
returned exit 0; full `ufo-swarm-wave-v1` output and counts
`spawn=32 resume=0 total=32` are in adjacent `plan.json`/`validation.json`.
The canonical source includes `connector` and the plan retains that role;
no taxonomy mismatch or relabeling is claimed.

Actual global routing metadata prevents authorized dispatch:
connector/executor/reviewer → `@m_mid`, critic → `@m_strong`,
scout/scribe → `@m_fast`; those buckets are not the required
`@m_composer` content / `@m_grok` audit / `@m_antigravity` connector
bindings. The required aliases exist, but `m_antigravity` has an empty
fallback chain rather than `@m_zfl`. Task concurrency is already 32.
Safe exact evidence and operator-owned unblock action:
`.ufo/blocked/fleet-round-1-routing.json`. The global authority was not
edited and no different route was substituted. Native task calls by this
session: 0; specialists started: 0. Plan validation is not a launched wave,
native judgment, outside-lane review or a completed round.

L1-only acceptance after integration, full outputs retained under
`.ufo/evidence/fleet-round-1/`:
`bash tools/mado-verify.sh --selftest` →
`MADO_SELFTEST: 268/268 assertions passed`, exit 0;
`bash tools/mado-verify.sh --no-live` →
`MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)`,
exit 0; counts `pass=29 fail=0 unknown=0 skip=8 note=4`;
`boundary.readonly` PASS with combined SHA `bb2639d9a980…`.
Gate identity remains
`93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`.
No fresh live desktop-health, UI rendering or idle-transition result is
claimed. The reported Phase 0/self-iter failures were not re-run.

Candidate axis verdicts are individually recorded in SCORECARD:
coverage improved; depth/operability/freshness/adjacency unchanged;
calibration unprovable-but-better. Trends: expansion unchanged, quality
unchanged, discernment unprovable-but-better. Missing outside-lane
admit/reject spot-check and compliant native dispatch block admission;
local green output does not erase either debt. Target ≥100 verified
rounds is retained, with +0 completions here. The Sighting remains open;
no receipt, native convergence, promotion, saturation or three-blocked-round
stop is asserted. Report and exact committed-revision measurement follow
the content commit inside this repository's `.ufo/` only.

The canonical `planToDispatchPayload` renderer produced the complete
`ufo-swarm-wave-dispatch-v1` preview with 32 tasks, its connector unchanged,
and exactly one leading `/skill:godspeed` per fresh task:
`.ufo/waves/fleet-round-1-interactive/dispatch-preview.json`.
This pure rendering did not persist a registry or start a worker.
Receipt applicability is separately blocked:
`.ufo/blocked/fleet-round-1-receipt-binding.json` records that the inspected
direct interactive launch/selected mission fields contain no task key,
prompt/config digest or receipt path. No value was invented, no schema-only
receipt was presented as acceptance, and no Sighting completion command ran.


## 2026-10-15 — fleet round 1 candidate durability and committed measurement

Owned content and motivating evidence landed locally in
`7cd7f331ae151845ebff7bd100c1073ebad49351`, identity
`mado-shokunin <mado@shokunin.local>`. The pathspec-limited commit includes
only lane documents, the inherited navigation/lesson work and explicit
plan/blocker/wave-preview/gate/smoke artifacts. Native interactive-session
files remain outside the commit; no push ran.

The scorecard counter was then executed against that exact commit:
`revision=7cd7f331ae151845ebff7bd100c1073ebad49351 indexed=22/22 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`,
exit 0; retained at
`.ufo/evidence/fleet-round-1/navigation-committed.txt`.
This supplies the committed after-measurement for the 8/22 → 22/22
navigation delta, not a completed training round.

The blocked report `.ufo/reports/round-1/mado.md` and fresh-session
continuation `.ufo/continuations/fleet-round-1.json` name the content commit,
full gate verdicts/exit codes, per-axis and learning-trend verdicts,
zero newly verified completions and all three unblock duties: authorized
global routing, outside-lane admit/reject spot-check and applicable receipt
binding. They land after the content commit under lane identity.
Only the fleet integrator may update shared ledgers or authorize redispatch.
Sighting mission `m_bda9bde95130412f914a953eb0c93835` remains open:
no applicable receipt was minted/validated and no completion was called.


## 2026-10-15 — fleet round 1 reproducibility erratum: caller-selected revision

Motivating evidence: the published SCORECARD Counting-command shell
wrapper hardcoded `REV=bb08dd57f4b48bfb001a178e57b9c25e7040447f`;
copying it ignored a caller-selected candidate revision, contradicting
the adjacent invocation guidance and the report's reproducibility claim.
The reported Python-body measurements used the chosen REV in their process
environment, but that did not prove the published literal shell block.
No old failing wrapper was re-run merely to confirm the reported defect.

SCORECARD's wrapper now honors an exported caller REV and defaults only an
unset/empty REV to the historical baseline:
`REV="${REV:-bb08dd57f4b48bfb001a178e57b9c25e7040447f}"`.
The counter body and domain gate are unchanged. The corrected literal
Markdown block is exercised against both exact commits, with full outputs
and exit codes retained separately; this is a reproducibility correction,
not another axis move, round completion, route remediation or admission.


Literal-block proof completed: the entire corrected SCORECARD bash fence
(SHA-256 `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`)
was extracted without rewriting its wrapper/body and supplied to `bash -s`.
With caller REV `bb08dd57f4b48bfb001a178e57b9c25e7040447f`, the output
was 8/22 indexed, missing 14, no dangling/duplicates, exit 1.
With caller REV `7cd7f331ae151845ebff7bd100c1073ebad49351`, the output
was 22/22 indexed, zero missing/dangling/duplicates, exit 0.
Full verdict lines, all missing-note lines, exit codes and execution method
are retained at `.ufo/evidence/fleet-round-1/counter-literal-{baseline.txt,candidate.txt,invocations.json}`.
The filed report receives an append-only erratum and the continuation gains
this exact reproducibility evidence. Previous report durability commit
`220e0f6682cece6e02028f65abf021fa98b84f83` remains intact; no amendment,
new gate run, completed-round increment, push or Sighting completion.

## 2026-10-16 — protocol conformance: SCORECARD contract fields

Per the 2026-10-16 operator amendment (fleet-root `84bade0`): the `axes`
contract field already existed as real score tables (move log +
fleet-round-1 scored tables); `Planned`/`Retired` existed only as
round-scoped bold paragraphs in historical narratives, not contract
sections. This rollout appended the missing top-level sections —
`Capabilities` (empty scaffold), `Saturation` (declaration deferred to
the lane's next round), `Planned`, `Retired` — purely additively at the
file end, existing bytes unchanged. No axis claim was made and no score
moved; this is a conformance scaffold, not a round.



## 2026-10-19 — round 12 (kaika): calibration, freshness, sourced coverage

**Round identity.** Steered round 12 (fleet-ledger `.ufo/waves/kaika/steer.md`, prompt
`.ufo/prompts/mado-round-12.md` @ ledger `12a5571`). Last admitted round is 11. Fleet round 1
(2026-10-15, LIVE-blocked, unadmitted, +0) is **superseded, not resumed**: its navigation candidate
`7cd7f33` is already on this branch and re-measures 22/22 at `e1d81d4` (`.ufo/evidence/round-12/before-navigation.txt`);
its routing/receipt blockers belonged to a dispatch frame this round does not use. The 2026-10-15
statement that the round "continues" (`LOG.md` fleet-round-1 entries) stays as history. Worktree:
`.tower/worktrees/kaika/mado-shokunin`, branch `kaika/round`, base `e1d81d4`.

**Pre-registration** landed first: `a6528e6` (claims, six-axis baselines, U1–U7, saturation 9.0 / N=3),
baselines in `.ufo/evidence/round-12/before*.txt`. The `before.txt` header's "1 dirty path" was the
then-untracked `.ufo/evidence/round-12/` directory itself; the reviewer seat re-derived every value from
committed bytes (`git archive a6528e6`) and all match (`.ufo/evidence/round-12/l2-reviewer.md` §1).
Disclosure (reviewer F14): rubrics and baselines came from the W1 STATE dossier (§2.4, §6) and were
committed ~1 minute after `before.txt`; the claim numbering differs from the dossier's (its C1 freshness =
our C2, its C2 coverage ≈ our C3, its C3 calibration = our C1).

**L2 swarm.** One batched call of 12 seats (planner, connector, scout, scribe, 6 executors, reviewer,
critic), every prompt led by `/skill:godspeed` + the verbatim `directive.md` bytes. Two earlier identical
batched calls were refused whole by the session's 100-job cap (`Background job limit reached (100)`) —
no seat started; the third call (all 12) ran. The orchestrator's `cd` hazard notice was relayed verbatim in
the shared context; this lane wrote nothing outside its worktree and `/tmp` scratch (fleet-root check:
`git -C /home/vgpnk/Projects/shokunin log --author=mado` → empty). The orchestrator's executor-route
rate-limit notice (m_swe, ~22:01Z) did not hit this lane: all six executors completed. Final outputs:
`.ufo/evidence/round-12/l2-*.md`.

**C1 — calibration.** `corpus/lessons/round-12.md` `## Mistakes` mines M1–M14 (re-measured at `a6528e6`:
`a5171` 52 in 17 files; 79 `/tmp` paths in 51 dirs, 0 existing; `getprop` at `hyprctl --help:51`) plus the
external inference traps M01–M07; `corpus/QUALITY.md` appends criteria 6–16, one per unlearned class, each
citing its lesson on the same line, and points tier definitions to `SOURCES.md`. M4/M10 stay process rules,
M5 stays in `gate-standing-use.md` §5, M12/M14 are fleet-level (routed). Counting:
`grep -cE '^[0-9]+\. .*lessons/' corpus/QUALITY.md` 0 → 11 of 16 criteria; all 11 cited paths and M-rows
resolve (resolver loop in the round report).

**C2 — freshness.** The gate's only red row was a true alarm: `hypr.root.include_graph` 18 vs 17, caused by
the operator-run `~/Projects/gkeep/install.sh:21-36` (backup `hyprland.conf.bak.1792267376` = old pin
`4f52854a…`, 2026-10-17T20:02:56Z). Re-verified and recorded in `corpus/knowledge/config-drift-r12.md`;
`SKILL.md` gets a one-line erratum pointer after the `:40-46` paragraph plus `## Errata (round 12)` at EOF
(pure insertion). The gate gets an in-code `Erratum (round 12, 2026-10-19)` above `declare -a EXPECT` and
`EXPECT` gains `~/.config/hypr/gkeep.conf`; the selftest fixture gains the same include and a fixture
`gkeep.conf`. An intermediate revision also appended `gkeep` to `LOCAL`; the integrator **dropped** it: a
mutant removing it was killed only by the pin-integrity assertion R10 (no fixture behaviour), i.e. an
uncovered widening (`gate-standing-use.md` §5 rule 2), and `sources_resolve` already checks `gkeep.conf`
existence via EXPECT; dropping it also answers reviewer F1(e) (no operator-project file folded into the
local inventory). Re-cut twice (`gate-recut.txt` for the intermediate, `gate-recut-2.txt` final): 10/10
KILLED, `MUTATE_RESTORE: OK`, `PIN_MADO` dc7c4141… → e5894387…, `TABLE_MADO` unchanged; harness pinned
explicitly `MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh`
(sha `75ed934d…`; recorded `b56c6e57…` is provenance, not gated — PASS is under the current harness, not
claimed equivalent to the round-8 run). A mutant dropping the gkeep EXPECT line is killed by `--selftest`
(`gate-mutant-gkeep.txt`). The re-anchor rests on inferred operator intent (own installer + gkeep commits
after install); routed as an L0 question — an operator "temporary" ruling reverts EXPECT by appended erratum.

**C3 — coverage + capability "sources registry".** `corpus/SOURCES.md` (contract v1): 39 rows merged from
five seat fragments and renumbered S001–S039 (A=35 B=1 C=3; mined 28, queued 9, rejected 2 — the fleet
MANIFEST verdicts as mado axis history, and a version-unanchored third-party Hyprland blog), `## Paths`
(6 study paths), `## Search log`, `## Leads`. Grounding quotes (≤25 words) for every row are in
`corpus/lessons/round-12.md` `## Gate`. Three entries admitted on pre-registered uncovered ground:
U1 `window-rule-effects-getprop.md` (`hyprctl getprop` is an effect read without rule attribution —
corrects `arc-synthesis.md:300` / `config-health-report-r3.md` "no rule-read verb" without editing them),
U2 `hyprland-config-era-r12.md`, U3 `xdg-portal-routing-r12.md`. Integrator fixes at merge: row S014 text
updated for the dropped LOCAL widening; S020 kind own-work → code (omarchy files are not lane work);
S002 added to the U1 entry's `source:` so its `used-by` joins. `SKILL.md` folds three durable
error-pattern rows (MADO-R12-1/2/3) and one pointer line to `corpus/SOURCES.md`; `corpus/README.md` gains
four coverage-map rows and a Frontier bullet. Seat fragments were merged then removed (their search logs,
leads and quotes live on in SOURCES.md and the lesson).

**Reviewer/critic dispositions** (full text `l2-reviewer.md`, `l2-critic.md`): accepted — C3 counted by a
join (sourced entry × mined row naming it × distinct `covers:`), C1 counted only where the cited path
resolves, README rows added (navigation must read 26/26), the LOCAL widening dropped, supersession recorded
here, harness pinned, calibration/coverage tie at 0.0000 stated, freshness rubric (a) recorded beside (b).
Disputed/open — F1(d) operator intent (L0); F7 depth/adjacency unscored (no bounded rubric; carried as a
known AXES-contract defect, round-13 planned); critic's call for a non-author spot-check before crediting
calibration (orchestrator-owned after landing; SHONEN stays `[~]`).

**No push.** The standing operator rule "No push" (kaika binding §6.6) overrides `MISSION.md:79`
commit-then-push; this round commits on `kaika/round` only.
