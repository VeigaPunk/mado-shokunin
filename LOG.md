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

**Post-integration review (round 12, second batched call: reviewer + critic over `5174e15`;
`.ufo/evidence/round-12/l2-postreviewer.md`, `l2-postcritic.md`).** Reproduced: every `after.txt`
count, pure-insertion diffs (SKILL 20/0, QUALITY 16/0), 9 Gate quotes re-opened against source
(S001, S002, S005, S013, S014, S017, S018, S020, S024), U1 host reads (class/address only), no
gate marker/VERSION_STR/--help touched; C3 verifies. Fixed in this round:
- Gate: no selftest scenario removed `gkeep.conf` (critic item 4). Scenario B now deletes it and asserts
  `hypr.root.sources_resolve` FAIL. Red-before/green-after: a mutant flipping that row's FAIL arm to PASS
  survived every behavioural assertion at `5174e15` (killed only by pin check R10) and is killed by the
  new assertion (`gate-mutant-sources-resolve.txt`). Third re-cut 10/10 KILLED (`gate-recut-3.txt`),
  `PIN_MADO` → `538d178b…`, `TABLE_MADO` unchanged; selftest 268 → 269/269; `--no-live` 29/0, live 52/0/8,
  `--regression` PASS (`gate-*-after.txt`).
- C1 provenance: criteria 15–16 rest on external inference traps, not lane incidents, and criterion 8's
  secondary pointer grounds M4 — appended provenance notes to `QUALITY.md` and an errata block to the
  lesson; the score is reported under both readings (11/16 pre-registered, 9/16 strict).
- `after.txt` printed one command that differed from the one run, and three counts without commands;
  the final `after.txt` prints every command verbatim. S003's quote line `:330` → `:331` (lesson errata).
- Separability of C3 from C1 (reviewer item 2): each U entry clears criteria 1–5 on its own — one
  `## Rejected` and one `## Limits` section each, and `[OBS]`/`[INF]`/`[UNK]` tags kept apart
  (`grep -c` per entry: getprop 14/5/2, config-era 8/23/7, portal 9/10/5, drift 5/5/4).
Kept open, with reasons: operator intent behind the gkeep re-anchor (L0); the SKILL EOF errata block
(critic item 6, elegance) stays because `PROTOCOL.md` §Evidence requires corrections to sweep every
mention, and the detail lives in `config-drift-r12.md`; depth/adjacency rubrics (round 13).

Note (same round): the paragraph above was first appended by a shell call without `cwd` to the FLEET
ROOT `LOG.md` (relative path); the orchestrator restored that file to HEAD and saved the text to
`/tmp/kaika/mado-misplaced-log.md`; it is appended here verbatim, after `6e3b75f`, so that commit's
LOG lacks it. The measured content of `6e3b75f` is unaffected (gate, QUALITY, lesson, entry errata).

## 2026-10-17 — README: Devin wiki link

- Operator directive (2026-10-17): insert the Devin wiki link into the README header of every repository with a generated wiki.
- Change: `README.md` created (lane-header convention) with a `**Wiki:**` link to https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/mado-shokunin?branch=master.
- Evidence: the org's Devin wiki index lists this repo's generated wiki; sibling lane READMEs carry the same `**Wiki:**` header.
- Documentation-only change; no round run, no axis moved, no verdict changed.

## 2026-10-20 — round 13: protocol boundaries and named-set census

Steer: fleet `.ufo/prompts/mado-round-13.md`, attempt 1. Baseline
`7dcb785b7b943d03703181b218d7860a7b43007b`; the initial lane tree was
clean and carried no inherited round-13 work. The old arc and interrupted
fleet-round-1 records remain history, not a prohibition on this steer.

**Declared claims:** C1 coverage, sourced ground U1–U3 → U1–U4;
C2 operability, complete named-set diagnostics in four isolated negative
cases. C1 works the previous lowest scored sub-axis. C2's finite new
sub-axis does not retire broader operability. No exploratory claim.
Pre-verification rubric clarification in SCORECARD preserves the baseline's
existing detections: overall runs already failed in 3/4 cases, while the
responsible census rows supplied complete named-set diagnostics in 0/4.
Measured baseline: `.ufo/waves/round-13/evidence/before.txt`, command
`python3 .ufo/waves/round-13/measure.py 7dcb785b7b943d03703181b218d7860a7b43007b`.

**C1:** one admitted author-gate entry,
`corpus/knowledge/wayland-protocol-boundaries-r13.md`, covers U4's phase,
advertisement and unexercised-behavior diagnostic route; README and SKILL
route to it. S005 was reopened/mined; S040–S046 were opened and curated
(S045 rejected correction, not new knowledge). S042 fixes S006's owed
revision without editing immutable cells. S017's used-by gains the lesson;
all mutations/quotes live in `corpus/lessons/round-13.md` § Gate.
The U2 note gets a complete append-only S030→S017 mapping; SOURCES retains
the rejected historical row and supplies its explicit correction S045.
The observer's bindings/detail queries are code-grounded in S046, separate
from the headers retained in the sanitized capture.

**Tool install:** wayland-utils **1.3.0-1**, pacman extra,
`sudo pacman -S --needed --noconfirm wayland-utils`, to obtain the assigned
`wayland-info` diagnostic route; GlobalCapture read RULES.md first.
No partial upgrade or system update. Capture/replay: 72 advertisements,
71 distinct interfaces; digest `9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa`.
Commands/output: `evidence/packages.txt`, `globals-recheck-bound.txt`,
`capture-validation.json` under `.ufo/waves/round-13/`.
The first L1 replay lacked WAYLAND_DISPLAY and correctly returned UNKNOWN;
the corrected replay explicitly supplied the previously correlated socket,
not a guessed instance (`session-prerequisites.json`).

**C2:** `tools/mado-verify.sh` now compares expected/observed root-source
declaration membership and local regular `*.conf` names, reporting
missing/extra members while preserving source order and target existence.
gkeep joins the observed/persisted baseline via `LOCAL+=(gkeep)`; it is
not ownership or an operator-intent endorsement. Empty-source indexing
fails closed; unsupported `# hyprlang` directives are rejected rather than
silently interpreted as plain comments. Root expansion and filename
escaping preserve the read-only fence. This is not a full hyprlang parser
or a pin of every filename expanded by the toggle glob.

Gate proof: `--selftest` **310/310**, `--no-live` **29 PASS / 0 FAIL /
0 UNKNOWN / 8 SKIP / 4 NOTE**, both exit 0. Historical spec stays
byte-preserved at `c7ee75b9…`; real re-cut killed **10/10**, restore OK,
target `538d178b…` → `87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39`.
Separate covering spec killed **8/8**, restore OK, over the derived
executable (not a selftest pin-identity shortcut).
Commands/full observations: `evidence/gate-selftest.txt`,
`gate-file-plane.txt`, `regression-recut.txt`, `covering-mutants.txt` and
both results TSVs under `.ufo/waves/round-13/`.

**Registry and reproducibility:** SKILL is the registry home for the
existing gate modes, the conservative source-merge screen, the measurement
probe and the digest-checking frozen regression companion. The companion
ships `frozen/{gate.sh,harness.sh,expected.json,verify.py}` under that round
directory; it verifies both input digests before execution and observed
`MADO_REGRESSION: PASS`, 10/10 table match, and `frozen_match`, exit 0.
Its self-invocation is **12/12**, exit 0. The live sibling harness remains
read-only and provenance-only; the frozen copy pins
`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.
Standing-use and config-drift notes receive append-only current receipts
and governing-rule corrections.

**Learned outside disagreement:** QUALITY criterion 17 prevents S030-style
active-URL duplicates from escaping as warning-only scope-string differences.
The lane-local screen is deliberately not a semantic source-admission oracle.
Selftest **25/25**, exit 0; actual historical `5174e15` registry is red
(`COLLISION S017 -> S030`, exit 1), current registry green (exit 0), retaining
rejected history and valid S042 supersession. Evidence:
`evidence/collision-{selftest,red-corrected,green-corrected}.txt`.
Initial L1 calls used the wrong positional CLI and returned argparse 2;
the documented `--registry` calls above are the exercised proof.

**In-round defects, not hidden:** Safety found unfiltered Wayland scratch
files (world-readable metadata); their owner deleted both and corrected
the capture report. No raw output is retained or pushed. The first frozen
selftest failed with `UnboundLocalError`; adding `failed` to the nested
function's nonlocal declaration is the sole correction, then the same
self-invocation passed (both observations retained).

**Swarm:** one campaign-validated native batch, 32 seats: 8 executor,
7 scout, 4 connector, 5 reviewer, 4 critic, 2 scribe, 1 sentinel, 1 revenger.
L1 is canonical planner; PlanningWalk is the connector-routed bounded data
walk. No per-seat model override or routing edit. Native ids are recorded
in `.ufo/waves/round-13/w1/reports/swarm-registry.json`; spec and unchanged
validator payload are committed with the wave. All seats finished before
L1 verification. Preliminary draft hypotheses are not final verdicts:
notably early target-count wording and SourceRevision line anchors were
not adopted; final code/knowledge and actual observations govern.

**Boundaries and disposition:** no config/compositor mutation, kernel-input
experiment, output action or sibling edit; the sanctioned diagnostic
package install is explicit above. Broader whole-config hashing, generic
parser behavior, expanded-glob membership, historical theme mutation
coverage, rendered UI and operator intent remain named limits.
Depth/adjacency rubric expansion was not a declared claim. SHONEN stays
four assertions. The parent requires an after-report fresh non-author
admit/reject spot-check and closure; admission remains pending that act.
The content commit and revision-bound after measurements are recorded in
the appended round-13 closure entry below and in SCORECARD, never by
rewriting this entry.

### Round-13 closure — measured content revision

Content commit: **`95cbc41fe5d5db121b89c2ddd1f953728663c5f4`**.
Running the exact counter above at that revision produced
U1–U4 **4/7 (5.7143/10)**, all three U4 facets present and source-joined,
navigation **27/27** with no missing/extra/duplicate, and C2 complete
named-set diagnostics **4/4 (10.0000/10)** with all four overall runs
failing. Baseline was **3/7 (4.2857/10)**, **26/26**, strict **0/4** and
overall **3/4** respectively. Both observation counters exited 0.
Exact commands, rows and exits: `.ufo/waves/round-13/evidence/{before,after}.txt`.
The finite score improvement is not whole-domain saturation.

SOURCES at the measured revision: **46**, versus **39** at baseline;
A/B/C **42/1/3**, versus **35/1/3**; mined/queued/rejected **34/8/4**,
versus **27/9/3**, by that counter's `source_registry` field.
Seven new A rows yielded one new U4 knowledge entry; S045 is a duplicate
correction, not expansion. S005 status/used-by and S017 used-by are the
only existing-row cell changes, logged old→new in the lesson.

Committed bindings (`git show <commit>:<path> | sha256sum`) confirm:
gate `037b05dc…` equals the frozen gate input; capture
`ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949`;
frozen runner `094bf3a4…`; source screen `a3a1559b…`.
Full values and the exact measured commit are retained in
`evidence/committed-bindings.json` under the round directory.

SCORECARD records per-claim deltas, harm watch, demonstrated source-merge
and frozen-regression repertoire, and the next-round intent without
opening that round. Local claims: C1 improved, C2 improved. Other scored
axes unchanged; depth/adjacency unscored and unchanged. Learning trends:
expansion improved (new source-joined U4 ground); quality improved
(measured named-set gate plus revision-bound current receipts);
discernment improved narrowly (outside S030 disagreement becomes
criterion 17 with a demonstrated red historical case). The current
round's independent admit/reject spot-check and admission are still
pending the parent's after-report closure, not self-attested.

## 2026-10-20 — round 14: U5 boundaries and regular source targets

**Motivation:** SCORECARD's round-14 plan; lowest scored non-retired
coverage 5.7143/10; outside `round-13-verifier-spotcheck.md` R13-V1..V3;
ReviewResolver/GateRecon source inspection of the baseline `-e`/any-glob
existence predicate. Baseline revision:
`873ff081b2ac363df771261b0ed950cba50d8988`.

**Declared separable claims:** C1 adds sourced U5's documented
output-management/colour boundary route, targeting sourced U-items
4/7 → 5/7. C2 requires owning-row named non-regular diagnostics for
three isolated directory-shaped source cases, targeting 0/3 → 3/3.
These zero baselines are predictions until the named-revision counter
runs; they are not copied results. Counting command:
`python3 .ufo/waves/round-14/measure.py REV`.

**Knowledge/source work:** `corpus/knowledge/output-colour-boundaries-r14.md`
distinguishes configuration test/apply/outcome, manager support events
and immutable image descriptions from unexercised feature behavior.
Opened S047/S048 are exact primary XMLs; S041 is reopened historical
advertisement, not a new client run. S049 corrects immutable S046's broad
retained-data wording, not its diagnostic behavior evidence. README
indexes the actual new note and narrows remaining U5 feature unknowns.
Source byte commands/output are committed in
`.ufo/waves/round-14/evidence/{output,colour}-source-binding.txt`.

**Learned corrections:** U4 gains an appended R13-V1 erratum:
global records contain interface/version only; sanitized probe/session
metadata is also retained. `gate-standing-use.md` gains an appended
R13-V2/V3 clarification; the original fleet report and old receipt are
not rewritten. In particular, round-13's “byte-identical before/after”
means config boundary bytes unchanged **within that one run**, not
identical outputs across code revisions. Its 29 PASS / 0 FAIL / 0 UNKNOWN
historical result stands. Future standalone evidence carries its
resolved measured commit and raw whole-gate digest in the receipt itself.
QUALITY 18/19 are grounded in lesson M4/M1, respectively; existing
criteria 7/9/13 already govern receipt provenance.

**Gate work:** `tools/mado-verify.sh` owns a strict regular-target policy
on its declared sources, not a claim that Hyprland itself errors on every
directory it may skip. Direct files/file symlinks and every glob member
are checked; non-regular and unresolved classes stay separate. Source
set/order checks stay separate; an order-only fixture preserves existing
behavior and is not counted as improvement. ReviewResolver's direct
case moves from ai-usage to default/hypr/windows.conf before any baseline
run to isolate the resolver. All-directory toggle collateral NOTE is
explicit; mixed-glob diagnostics must not accuse the regular sibling.
The current handler remains line-oriented, not a general hyprlang parser.

**Swarm:** one campaign-validated 32-seat native batch through unchanged
host routing. L1 holds canonical planner; PlanningWalk is a connector
bounded data-walk. Spec, unchanged taskCall and recorded ids live under
`.ufo/waves/round-14/w1/`. Reviews are lane-authoring advice, not outside
promotion authority. The generic arbitrary-command receipt wrapper was
rejected and removed as unnecessary surface; its reports remain rejected
candidate evidence. No wrapper capability or executed selftest claimed.

**Tooling:** OutputSpec installed wlr-protocols r112.a741f0a-1 from
official pacman extra (`sudo pacman -S --needed --noconfirm wlr-protocols`)
for the owning XML. ReviewSourceBar's `pacman -Sw` was cache download
only, not a second install. No full-system upgrade or partial `-Sy`.
Host configs/compositor, sibling repos and source trees stay read-only.
No inherited uncommitted lane work existed at start; the non-author
round-13 spotcheck stays untouched. No new L0 decision is needed.

The separate round-14 committed-measurement entry below records actual
results and delivered revisions; no unrun check is a pass. Parent's
fresh after-report non-author closure supplies the independent admit
and reject spot-check. SHONEN remains four author assertions.

### Round-14 closure — committed measurement and correction record

Measured content **`32118fc1014837b3a385c7a66abbdc59b1560835`**;
baseline **`873ff081b2ac363df771261b0ed950cba50d8988`**.
`python3 .ufo/waves/round-14/measure.py <revision>` actually ran at
both revisions, exit 0: sourced U-items **4/7 → 5/7** (coverage
**5.7143 → 7.1429**), navigation **27/27 → 28/28**, regular-source
diagnostics **0/3 → 3/3** (finite score **0 → 10**), and overall
failing runs **0/3 → 3/3** on the selected default-windows/all-directory/
mixed fixtures. Exact commands, rows, source joins and all seven
unscored controls: `.ufo/waves/round-14/evidence/{before,after}.txt`.
The draft ai-usage placement was changed before measurement; its
unscored control honestly shows pre-existing local-inventory detection.

U5's source/body hand check includes the unexpected static safety
boundary: newly opened S050 at tagged Hyprland `efb5099` returns true
from a test stub and schedules reload in `disable_head` before a later
test/apply. The U5 note and SKILL teach the entire transaction as
mutation-class; they do not claim executed host behavior or
binary/source equivalence. S047 is owning XML, not claimed compiled
Hyprland XML. Parent source-byte/peeled-tag bindings and AttackCoverage's
actual-note agreement are retained under the round directory.

**Observed harm watch:** gate selftest **372/372**, file plane **29 PASS,
0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE**, both exit 0. Historical recut
**10/10 KILLED**, regular-policy covering mutants **4/4 KILLED**,
retained census mutants **8/8 KILLED**, GREEN controls and restore OK.
Frozen companion verifies executable input digests, reproduces historical
table **10/10**, ends `frozen_match`/`MADO_REGRESSION: PASS`, exit 0;
its isolated selftest **12/12**, exit 0. Each exact command/output/exit
and results TSV is committed in `evidence/`, not inferred from a prior
round. The repair fails the same contract audit at baseline (exit 1,
FAIL 0/3), then passes after (exit 0, 3/3).

**R13-V1..V3 disposition:** learned, append-only. U4 erratum plus S049
scope retained-data wording to globals records versus sanitized metadata;
QUALITY 19 cites that outside disagreement. Standing-use and this log
correct the ambiguous report boundary claim without rewriting the filed
round-13 report: unchanged bytes within that run, not cross-revision
output equality. The old selftest receipt remains header-deficient;
the same provenance audit fails it with exit 1 naming missing commit/
digest, and passes the new directly bound selftest receipt with exit 0.
The discarded generic wrapper is not a shipped capability.
QUALITY 18 is grounded in M4 and demonstrated by strict fixture failures
and the new covering mutants.

**Inputs:** raw gate and frozen input both
`fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`;
derived target
`cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`;
historical spec stays
`c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8`.
Re-derive committed full inputs via the command in
`evidence/committed-bindings.json`. Mutants grade only that documented
derived executable; no excised-machinery coverage is implied.

**Sources:** revision counter **46 → 50** rows, A/B/C **42/1/3 → 46/1/3**,
mined/queued/rejected **34/8/4 → 38/8/4**. S047/S048/S050 support one new
U5 entry; S049 is correction, not expansion. S041 used-by is the sole
existing-row field change. Maintained before/after census exits 0 with
W04 S030/S042/S045 retained; source merge screen exit 0, collisions 0.
Quotes, immutable corrections and mutation log are in lesson §Gate.

**Swarm and safety:** unique wave members **32** — 3 executor, 8 scout,
4 connector, 6 reviewer, 4 critic, 2 sentinel, 2 scribe, 2 revenger,
1 mutation-tester (registry/spec provide the counting set). L1 canonical
planner, connector PlanningWalk bounded data-walk. All seats finished
before L1 integrated verification. Safety's jj working-copy-snapshot
incident is disclosed, not rewritten; future read-only jj commands use
`--ignore-working-copy`. Source scratch owners removed exact public
temporary paths. `cleanup.json` records this round's own mutation fixture
cleanup; old/foreign scratch was not swept. Source fetch digests were
also bound with pipefail. The only installed package remains authorized
wlr-protocols r112.a741f0a-1, official pacman extra, for XML inspection.

**Verdicts:** C1 coverage improved; C2 operability improved. Other axes
have no additional scored move and no retained harm observed. Expansion,
quality and discernment improved on the specific evidence above, with
current-round independent admit/reject/admission still pending the
parent's after-report non-author closure. Remaining limits are named in
SCORECARD/lesson, not silently retired. SHONEN remains four author
assertions; no promotion, domain mutation, sibling edit, or next-round
mission was performed. No new L0 question.

## 2026-10-20 — round 15: U6 diagnostic route and an honest safety stop

Motivating evidence: SCORECARD planned bounded U6 study and outside
`corpus/lessons/round-14-verifier-spotcheck.md:169` R14-V1, whose three
ancillary mutation headers were provisional although the derived target
was recoverable. C1 is one coverage move on the lowest current-art rubric:
U1–U5 5/7 → U1–U6 6/7, measured by
`python3 .ufo/waves/round-15/measure.py REV`, not source-row volume.
Baseline is `ea0446fcb4840089f0e541d96350144506fb5d1d`; the actual
baseline receipt is `.ufo/waves/round-15/evidence/before.txt`.

Landed work under this round entry: the U6 source/prove/does-not-prove
ladder in `corpus/knowledge/input-debugging-boundaries-r15.md`, S051/S052
and their reciprocal index route; `corpus/lessons/round-15.md` §Gate
records quotes/source correction decisions. S051 supersedes S007's
composite/mutable source description, while S052's input scope is distinct
from S043 registry semantics. Existing registry rows remain unchanged.
R14-V1 is an unscored append-only standing-use explanation plus exact
per-receipt mapping to committed-derived target bytes. Old receipt headers
are never relabeled as later committed full-gate execution.

**Actual safety violation:** wave scout `MadoR15.LibinputEvents` ran
`sudo pacman -S --needed --noconfirm libinput libinput-tools` at
2026-10-20T04:25:16-0300. `/var/log/pacman.log:2429-2437` records
libinput 1.31.3-1 → 1.32.0-1 and new libinput-tools 1.32.0-1,
python-libevdev 0.13.1-1, python-pyudev 0.24.4-1, python-yaml 6.0.3-2
through official Arch extra. The stated reason was static man/help
inspection, not input capture. The orchestrator ruled this a forbidden
partial upgrade and routed remediation to L0. Udev-reload/system-update
hooks also ran. No device/event read, replay, downgrade or restart is
claimed or authorized; package availability is not input behavior.

Lesson M2, QUALITY 20 and SKILL now require a prospective
`pacman -Sp --print-format '%n %v' <pkgs>` plan containing only
not-already-installed packages; any overlap, including dependencies,
goes to L0. No further pacman operation is allowed this round. The same
in-memory guard is red on the actual transaction names (exit 1,
`already_installed_in_plan`, libinput), green only on a new-only fixture
(exit 0, `new_only_plan`), with full commands/output in
`evidence/install-guard-{red,green}.txt` under the round-15 wave.
The guard does not remediate host state or retroactively admit this round.

One validated 64-seat wave; L1 canonical planner plus PlanningWalk mapping.
All wave advice remains lane-authored; no outside SHONEN clearance.
ReviewLibinput's disclosed `hyprctl version` call violated the wave's
no-live-probe instruction and supplies no fresh claim evidence. No input
event capture/injection or compositor/configuration mutation is performed.
No other lane/fleet-runtime source write is part of this work.

Author verdict: C1 is bounded structural coverage, subject to committed
measurement and outside review. Operability safety is harmed by the
partial upgrade, even though no input regression is established. Thus
no-harm admission is unmet. Finish reachable records and halt progression;
do not open round 16. Tool/transaction and source limits are preserved
in the lesson rather than hidden by a green gate or a successful push.

### Round-15 committed measurements and final author verdict

Content `5f13870491588703ea6c81ef390488c5d2eeb727` was committed and pushed
before the final evidence/report record. The exact revision counter
`python3 .ufo/waves/round-15/measure.py REV` returned coverage U1–U5
5/7, 7.1429/10 at baseline `ea0446fcb4840089f0e541d96350144506fb5d1d`
and U1–U6 6/7, 8.5714/10 at content (+1.4286). Only U6 was added.
Navigation 28/28 → 29/29, no missing/extra/duplicates.
Source rows 50 → 52, A/B/C 46/1/3 → 48/1/3,
mined/queued/rejected 38/8/4 → 40/8/4. Exact stdout/exits are under
`.ufo/waves/round-15/evidence/{before,after}.txt`.

After all 64 seats landed, L1 ran one verification set: selftest 372/372,
exit 0; no-live 29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE, exit 0;
source census exit 0 with historical W04 S030/S042/S045; source-merge
screen rows 52, collisions/errors 0, exit 0. Standalone gate receipts
carry measured content and unchanged raw gate hash `fba82a66…`.
No live desktop-input probe or new mutation/frozen replay was run.

The identical static correction audit fails on baseline (exit 1,
`receipt_mapping_missing`) and passes delivered content (exit 0,
`receipt_mapping_verified`, mapped 3, problems []). Original receipt
bytes remain unchanged; derived target is 117602 bytes, `cd1d73d7…`,
not whole-gate `fba82a66…`. Future binding discipline stays direct,
without a new generic execution wrapper. Lesson §Gate and
`evidence/receipt-correction-{red,green}.txt` record this learned R14-V1.

Final per-axis verdicts: coverage improved narrowly, operability safety
harmed by the forbidden partial upgrade, freshness/calibration/depth/
adjacency unchanged. Trends: expansion improved narrowly, quality harmed,
discernment improved through the grounded outside correction; no current
non-author agreement or promotion claimed. **No-harm admission unmet.**
The orchestrator's L0 HOST PARTIAL UPGRADE question owns remediation;
no duplicate lane question or rollback/restart was performed. No round 16.

## 2026-10-20 — round 16: source-only learning after rejected-harmed closure

Trigger: independent `corpus/lessons/round-15-verifier-spotcheck.md`,
R15-V1/V2, at baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
The explicit round-16 steer authorizes this bounded source-only work, never
host remediation. Historical “No round 16” entries above are retained records
of the prior honest stop, not silently overwritten.

C1 coverage admits `waybar-observation-boundaries-r16.md` from opened tagged
S053/S054, indexed in corpus/README. Producer data, formatting/visibility,
GTK markup and actual rendering are separate; actual text remains unknown.
Source digests and located quotes are in round-16 evidence and lesson §Gate.
C2 operability acquires only a finite declared-action classifier, with a
persisted paused policy and self-invocation/frozen evidence. It never
intercepts tool calls or proves arbitrary argv safe; wrappers, credentials,
write destinations and actual host effects are not analyzed. QUALITY21 and
SKILL carry the current pause; old hard-coded overlap controls are not
relabeled real package validation. R15-V1 stays operator-owned and unresolved.

PlanningWalk exposed the L1's initial lowest-axis mistake: calibration's
active literal same-line lesson criterion fraction was lower than coverage.
The explicit SCORECARD correction adds independent C3 calibration and
QUALITY22, grounded in round-16 lesson M3. The original literal counter is
preserved; multiline semantic citation counts are not substituted.

M4 records RoundConformance's actual fleet-root report write despite the
context's lane-relative instructions. L1 copied its 8613 bytes byte-exact to
the lane; Main removes the fleet copy. Wave2 repeats the exact requested
trailer-resolution sentence. This is a disclosed scope/process defect,
not a claim of flawless compliance.

All wave advice is lane-authored, not fresh outside verification. No package
transaction/query, service/compositor mutation, input collection, producer
execution, screenshot or tool installation is authorized for this round.
SHONEN remains four author assertions; historical SKILL promotion tables
remain dated, not current independent clearance. PROVINCE stays unchanged.
No retirement or next-round mission is declared.

Historical source-header note from AppendOnly: commit `95cbc41` changed
SOURCES header prose and its CORPUS pointer without logging the prose rewrite;
no row cells were lost. This new entry records it without rewriting history.

### Round-16 verification correction — M6

First integrated measurement at `9dcf248993a9622a5b016edec0003187141745d2`
observed C1 6/7→7/7, C3 12/20→14/22, independent cases 32/32 and legacy
selftest 372/372. New classifier selftest was **51/52**, not green:
the frozen denied-match case and committed frozen run rejected valid
`denied_executable:sudo`/1 as unreachable. Exact red receipts are retained
at `evidence/action-selftest.json` and `evidence/action-frozen.json`.
The expected-pair prefix table already ended prefixes with `:`, then
appended a second `:`. L1 replaced this with the exact reachable pair set
from pinned kind/name constants. No expectation changed. This correction
is under the operator wrap-up directive; no new worker or wave was spawned.
Lesson M6 records the failed check and the direct fix; final-code receipts
are separate rather than overwriting the red records.

### Round-16 final evidence and handoff

Corrected measured content `1e31681e76b5e7caadd1c749e18669a3632a1c3b`
passes the same new selftest **52/52** and committed negative frozen
comparison **frozen_match**, both exit0. Final executable
`226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3`.
`evidence/action-{selftest,frozen}-final.json` and `committed-bindings.json`
bind actual outputs, code and input/expected hashes. Original red receipts
are preserved; only failed behavior was re-exercised after the small fix.
Normal classifier32-case evidence remains at initial content, unchanged
by the exact frozen-pair correction. Legacy isolated selftest372/372 and
unchanged gate digest are harm watch, not host-package evidence.

Final revision probe confirms C1 **6/7→7/7** (8.5714→10.0000), C3 literal
**12/20→14/22** (6.0000→6.3636). Separate block citation reading
15/20→17/22 is not the score. Selection audit red1/green0 holds baseline
scores fixed while adding calibration to declared axes. New capabilities
table row is bounded declared-kind/12-name classification, never arbitrary
command safety, interception or host repair. Finite documentary coverage
is now ceiling/harm-watch only; broader coverage is not retired.

Census before/end exits0, historical W04 S030/S042/S045; sources52→55,
navigation29→30 with no gaps/duplicates. Exact commands and counts are
in round16 evidence. Both validated waves returned96 reports (64+32);
all advice remains authoring-lane evidence. Operator wrap-up arrived after
both dispatches; no new worker or next-round mission afterward.

M4 misroot was recovered byte-exact; the fleet sweep found no remaining
mado seat reports. M5's **one prohibited read-only `pacman -Q waybar`**
is excluded from evidence; no no-query/compliance claim is made. Seats also
read static package/log metadata, not credited as host-health clearance.
No installation/update/transaction is evidenced; host remediation remains
operator-owned, R15-V1 unresolved and unobserved. The classifier does not
erase that carried operability harm. No independent admission or promotion
is asserted. SCORECARD/lesson record bounded axis and trend verdicts.

## 2026-10-20 — round 17: receipt labels, P4/P6 sourced routes, transcript tripwire

Trigger: admitted round-16 closure (`corpus/lessons/round-16-verifier-spotcheck.md`,
routed R16-V1/V2) at baseline `27cd06f`; claims pre-registered at `0175f13`.
Host pause carried into both wave contexts with an explicit override of the
appended install directive; no package/service/compositor/input command was
issued by L1. `/var/log/pacman.log` (file read) shows 13 runs 07:45-09:39
before launch (no actor recorded) and 0 from 10:51 to close
(`evidence/pacmanlog-round-window.txt`). R15-V1 remains operator-owned, state
`[UNK]`.

C1 calibration: QUALITY 23 (receipt-label precision) from outside R16-V1,
lesson M1, append-only round-16 erratum, recut tamper receipt (exit 2
`snapshot_tampered`, control exit 0 `frozen_match`), label check with red,
mutant and green claims (`EXPECT_SUMMARY: 7/7`). Literal 14/22 → 15/23.
C2 coverage: new rubric V (PROVINCE surfaces P1-P6), instrument bound at
`f52f43f`/`ab0bc9b` before integration; P6 idle/lock and an Alacritty-only P4
route from rows S056-S071 opened this round; 2/6 → 4/6, documentary only.
C3 operability capability: `tools/mado-tripwire.py` (L1-written after seat
TripwireCore died on an m_swe rate limit) — post-hoc detection of issued
commands in OMP transcripts; suites 9/9, 16/16, 33/33, 26/26; anchor
`MadoR15.LibinputEvents.jsonl:54` `call_38165`; 4/4 pacman.log join by call
start; found undisclosed `sudo -n true` (r15) and a second `pacman -Q waybar`
(r16); round 17's own 149 transcripts: 1 `live_probe` (`ps`, RevSeparability).

Waves: w1 70 seats (1 dead: TripwireCore), w2 78 seats (falsify; 0 dead).
Wave-2 corrections landed at `f71ccbe` and are logged in
`lessons/round-17.md` § Wave-2 corrections. Harm watch at `f71ccbe`: legacy
selftest 372/372, classifier 52/52, U 7/7, navigation 32/32, census exit 0.
Freshness not re-measured (no live/no-live gate run; host moved under the
09:15 `-Syu`). Admission not asserted.

## 2026-10-20 — round 18: producer identity, P3/P5 sourced routes, tripwire frozen replay

Trigger: admitted round-17 closure (`corpus/lessons/round-17-verifier-spotcheck.md`,
routed R17-V1..V5) at baseline `d9a5a18`; jj-migration audits
`.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md` (F10/F14) and `JjTrialMado.md`
(`.ufo/state/` ignore). Pre-registration `d3a0000`; integration `4c103b5`;
receipts `abfbf35`; wave-2 integration `be886a3`. Host pause carried; L1 issued
no package/service/compositor/input command.

C1: QUALITY 24 (producer identity on receipts), 25 (mutant bite), 26 (producer
status through pipes); lesson M1-M8; round-17 erratum. 15/23 → 18/26.
C2: P3 Walker and P5 theme/wallpaper documentary routes, rows S072-S095 with fetch
receipts and committed licensed bodies; rubric V 4/6 → 6/6.
C3: `tools/mado-tripwire.py --frozen` digest-pinned replay over committed incident
lines; registry row `mado-tripwire-frozen` (gate).
Routed fixes: gate F10/F14 (pipefail inside the substitution, stub rc knobs,
OM9/OM10, PIN re-cut, 389/389, regression 10/10); `.gitignore` `.ufo/state/`,
`__pycache__/`. Re-cut real-transcript receipts carry producer headers (identical).

Waves: w1 88 seats (0 dead), w2 73 seats (14 dead without a report: CriticAdmission and
CriticHonestyW2 on an Anthropic 429, 12 more when the L1 session exited on the
same 429; ScribeReportDraft failed on a usage limit after writing its draft;
partial outputs re-verified and kept, none respawned). Harm watch PASS at `be886a3`. Evidence:
`.ufo/waves/round-18/evidence/final/`. Admission not asserted.

## 2026-10-20 — round 19: durable anchors and supersession sweep, walker pin currency, tripwire recall

Trigger: admitted round-18 closure (`corpus/lessons/round-18-verifier-spotcheck.md`,
routed R18-V1..V4) at baseline `9c54c56`; carried frozen F1/F2, `measure-mutants.py
--out`, jj audit F6/F9/F16/F17, three tripwire drafts. Pre-registration `17661e0`;
wave-1 integration `df84807`; tripwire merge and QUALITY/lesson `01b8094`; wave-2
corrections and final receipts in the commits after it (cited in the round report).
Host pause carried; L1 issued no package/service/compositor/input command.

C1 calibration: QUALITY 27 (durable anchors) and 28 (supersession sweep), R18-V2 applied
as criterion 24 (no new number); 18/26 → 20/28, pre-registered ≥21/29 missed.
C2 freshness (sourced, S096 host walker bytes): 13 owned files carry dated pointers;
`fresh-pins.py` 2/13 → 13/13 (5/13 name S096 on the crediting line; 0 walker facts
re-measured on 2.17.2); gate `live.walker.version` pin 2.17.2 with the PASS narrowed.
C3 operability: six patches merged into `tools/mado-tripwire.py` (BashCVar, HelperFn,
Installers `tool_install`, VcsClass `vcs_write`, frozen F1, F2); `tw-recall.py` 3/6 → 6/6
on the drafts' own lines (5/6 without the HelperFn rule-B lead); round-19 frozen re-pin.
Repairs: S097/S098 supersede S094/S084 (rejected); PROVINCE `~/.config/omarchy/**`
path-root line; gate F6 (tip read only with `.jj` and equal trees) and F9; landed-check.sh
(F16 narrowed); measure-mutants `--out`/`--workdir` safety; fetch RETENTION + class ignores.

Waves: w1 86 seats + 1 integration seat (TwMerge-2); 28 w1 seats on m_zfl ended on
`429 Rate limit` without a report; w2 67 seats. Harm watch PASS at `01b8094`
(`.ufo/waves/round-19/evidence/harm/`). Installs: none by L1 or any seat (w2
AtkInstallsRecord; two cache-level package materializations in the window belong to a
non-mado seat or are `[UNK]`). Seat `SentinelGatePath` ran one real `hyprctl probe`
(lesson M12). Admission not asserted.

## 2026-10-20 — round 20: repair — tripwire precision (observed vs lead), fail-closed harnesses, round-19 tallies

Trigger: round 19 closed rejected-harmed (`corpus/lessons/round-19-verifier-spotcheck.md`,
R19-V1..V6): HelperFn rule B made `BLOCK=frozenset([...])` an ordinary finding.
Pre-registration `e629f73`; precision suite `f3da504` (no tool change); tool repair
`28c6837`. Host pause carried; L1 ran no package/service/compositor/input command and no
hyprctl.

C1 operability (sourced, S099–S108/S111): every tripwire row carries `evidence`
(`observed`/`lead`); builtins, pure stdlib callables and visible pure bodies give no row;
cross-cell helpers, spawn aliases, vararg and keyword argv resolve; git/jj help and
dry-run forms are not writes (per segment, before de-dup). `tw-precision.py` 29/175 →
172/175 (target 175/175 missed by 3, reasons in SCORECARD); pre-harm `9c54c56` P 66/66
kept; recall 6/6 = 5 observed + 1 lead; controls 0; 11 suites 247/247 after 8 reasoned
case edits (each adds a finding). C2 calibration: QUALITY 29 (fail-closed isolation,
`isolation-check.sh` red on the round-19 shape) and 30′ (detector precision evidence);
registered 30 withdrawn as a restatement of 10 before measurement; 20/28 → 22/30.
Corrections to round 19 (R19-V2 8/13 any-line, 6/13 first-line; V4 154 files, fail-open,
self-report; V5 nine/eight; V6 25 dead seats) via `tally-check.py` (red 5/5).

Waves: w1 85 seats (0 dead; 85 refused twice by the 100-job cap at 16:36 and 16:39, spawned
on the third try at 16:42). Installs: none by L1; seat reports say none.

### Round 20, attempt 2 — recovery (2026-10-21, L1 MadoR20Recovery)

Trigger: attempt 1 (MadoR20) ended without a report (`.ufo/watchdog.log:548`
`lane-dead-no-report`); it had landed `f8576f7` (helper-recovered, PHASE2 incident 6) and
checkpoints `ed4bf22`, `38d1b36`, with w1 85/85 and w2 76/78 reports
(`SentinelPostWaveScan`, `ConnConsumers` dead, not respawned). Wave 2 falsified C1's
no-harm reading at `28c6837`: 52 out-of-suite recall losses, 13 RecursionError flips, a
~N⁴ helper expansion, 24 pure-stdlib leads, missed `jj -R` writes. Attempt 2 ran no new
64–100 wave (163 of ≤200 seats spent): registration `6a7d9ca`, before-receipts
`107955e`, tool v3 `3610e3e`, v3.1 `a8960de` (lesson M15: the removal-side corpus diff
caught a cluster `-h` from the next command hiding a checkout in an unparsed segment).

C1 at `a8960de`: precision 29/175 → 172/175 (target 175/175 missed by 3, unchanged);
recall 6/6 = 5 observed + 1 lead; controls 0; P at `9c54c56` 66/66; harm-watch PASS;
corpus diff from `9c54c56` 0 lost; a2 guards recall_lost 52 → 0, crash_flip 13 → 0,
pure_rows 24 → 0, vcs_fp 31 → 20, vcs_fn 0. C2: 22/30, criterion 29 re-verified, 30′
scoped by M9. Sources S113–S115 (112 → 115). Wave-2 dispositions
`.ufo/waves/round-20/a2/w2-dispositions.md`; residual review: one ordinary task call of
8 reviewer/critic seats (`a2/review/`), refused three times by the 100-job cap before it
started. Host pause carried: no package, service, compositor, input or hyprctl command
by L1. Installs: none by L1.

Final residual review: all 8/8 reports completed, no dead residual seats (round total
171; two dead attempt-1 seats remain uncredited). SCORECARD's final disposition
supersedes the improved author readings: C1 harmed (recall, false leads, memory and
VCS boundary counterexamples), C2 not independently established. Fixed-population
checks reproduced; live-corpus census cannot be repeated without frozen input.
Documentation review corrections landed; behavioral findings remain unresolved under
the operator's wrap-up instruction. No next round started; no installs.

## 2026-10-21 — round 21 attempt 1: registered residual repair

Trigger: non-author round-20 closure `corpus/lessons/round-20-verifier-spotcheck.md` at `794aaeb22b4bf35b2482a6779733b69343baff5b`, MANIFEST rounds[387], rejected-harmed (C1 recall/precision/memory/VCS failures; C2 coupled counter; in-entry false generalization; wrong-topic SHONEN assessment; mutable corpus and late registration). Prior target 175/175 remains missed by three, not rewritten.

Action before implementation/measurements: declaration `0644c536224847ecbb0b6c530d55d142e24f86c9`, provenance/clarification `0caf5f3ef31a38d4dfc5c4a4b586619b2f6ad452`; two causally separate claims in SCORECARD round 21. Wave 1: validated 65 independent oracle/recon items in one unchanged taskCall, L1 planner; actual private external writer worktrees pinned at `0644c536`, read-only advisers own only reports/proposals. Source census start exit 0, four W04 duplicate-URL warnings retained. No implementation or new tool result yet.

Correction landed with this record: the append-only correction inside `corpus/knowledge/tripwire-precision-r20.md` explicitly qualifies recall/sweep claims, preserves true source facts and historical counts, and names the actual residual defects. It does not claim their behavioral repair. Isolation tooling incident and cleanup limitation are preserved at `.ufo/waves/round-21/isolation-incident.json`; no host recovery or tool installation is inferred. Outcomes and measured revisions will be appended after actual observation, never pre-filled.

### Round 21 — replacement writer, frozen inputs and first implementation

Same held round/attempt, not a new claim: MadoR21-2 inherited the predecessor's committed registration/corpus corrections and uncommitted W1 proposals, sources, resource/assessment fixtures. Inherited artifacts landed `eaec245731926827c72b2fff47cb61afdf5d7c91`; normalized C1 oracle landed `b96d1b888a111971b430dc653f5826dc041b26bd` before production repair. The primary population is 35 delivered independently authored oracle proposals, 17 L1/late-source supplemental proposals and one rejected JjReadIwc proposal; `oracle/assemble.py` records all normalization/rejection reasons and never calls a classifier. Dead seats stay dead/uncredited. The cancelled predecessor oracle-measure implementation was not reused.

Observed red: `python3 -I .ufo/waves/round-21/oracle/measure.py --tool tools/mado-tripwire.py` at `b96d1b8` gives primary 8/35, supplemental 5/17 (`evidence/oracle-before.json`). Frozen 1000/2000/4000-assignment resource measurements at `eaec245` safely hit the 384-MiB allocation bound at 4000, while the CLI's unrelated 512-MiB thread reservation returns exit2 at every size (`evidence/resource-before-{module-main,cli}.json`). The C2 before capability is absent: `git cat-file -e eaec245:tools/mado-assessment.py` exits128, path does not exist. No synthetic permissive baseline is credited.

Implementation motivation is those observed residuals, not a rewritten historical benchmark. `tools/mado-tripwire.py` now retains statement snapshots only for inspected eager calls/references, separates value uses from invoked callbacks, preserves literal globals/closure bindings, resolves invoked partialmethod bodies, recognizes the named process-capable stdlib exceptions and strict VCS writes, and reduces the CLI stack reservation. `tools/mado-assessment.py` is an independent artifact-only integrity gate over frozen C2 expectations; it reads no C1 code/results. Complete frozen-corpus comparator: `.ufo/waves/round-21/corpus/compare.py`. These are implementation candidates until measured; subsequent receipts and any failures supersede intent.

Three ordinary two-seat implementation dispatches were refused with `Background job limit reached (100)`; each spawned zero seats. Main instructed coordinator-direct implementation; no dead oracle seat was replaced. No host config, package, compositor or service action; tool installations none.

### Round 21 — removal-side falsification and source correction

First full frozen-fixture replay at `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17`: `.ufo/waves/round-21/corpus/compare.py --before-tool .ufo/waves/round-21/evidence/tool-before.py --after-tool tools/mado-tripwire.py` retains every manifest path and raw outcomes (`evidence/corpus-comparison.json`). It records 33 removed/relabelled groups, 77 added/relabelled groups and 108 explicit error pairs, including the old bounded allocation failure becoming evaluable; real implicit-protocol/callable losses motivated `f499a8db7171b7476fe9f204ab9edbac5a956fa9`. Reclassification is not assumed harmless without semantic adjudication; malformed/deep/time-limited input rows remain visible.

W2 validated 84 distinct fresh attacks, one unchanged taskCall via the host task tool after one cap refusal; actual identities and role mix live in `w2-assignments.json`, `w2/reports/swarm-registry.json`, `w2-spec.json` and `w2-record.txt`. The production binding advanced from payload-rendered2ac0f9b to f499a8d before dispatch completion; every live seat was explicitly steered to record current SHA. This is disclosed rather than treated as an immutable2ac review. W1=65, W2=84, total149; no dead seat replaced.

Source/knowledge correction: `corpus/knowledge/tripwire-binding-boundaries-r21.md` cites S116–S119 and documents bounded callable/protocol/process/VCS reasoning plus the separate artifact-only assessment. S119 explicitly supersedes S113's false universal module-purity inference; S113's valid scoped os quotation remains. `SOURCES.md` used-by changes for S116/S117/S118 and all opened quotes/decisions are logged in lesson round21. SKILL's registry adds `mado-assessment`; README routes the entry. These are local transcript/integrity instruments, not new live desktop authority or promotion evidence.

### Round 21 — settled falsifiers integrated before final measurement

All84 W2 seats settled:58 delivered reports,26 provider deaths; `.ufo/waves/round-21/outcomes.json` records every failed identity and last error. No replacement, reroute or model override was used. Correction to the earlier “total149”:149 is the validated-wave total; the predecessor's ordinary MapResiduals scout adds one, so total150. The inherited OracleGitAddDry proposal without terminal receipt remains supplemental/uncredited.

Only after W2 finished, the isolated drafts landed into the production paths. The repairs respond to the named W2 findings: actual started-thread captured target/args/kwargs and alias calls, inherited constructor and invoked protocol handling, captured-cell rebinding, partialmethod aliases/returned partials, stored methodcaller and chained callable aliases, precise logging factory sections/keyword config, JSON/iterator/metaclass callbacks, IMAP's shell=True sequence semantics, jj aliases/config mutations and uv's pre-package help/`--` boundary. Git's unique `--dry` prefix is recognized without weakening intent-to-add or commit index-write guards. CLI deep-stack behavior keeps the historical512-MiB reservation when unconstrained and uses64MiB only under the declared low address-space cap.

C2 rejects the exact N/A absence mutant from `w2/reports/GateShonenXWithoutNonauthor.md`; its regenerated bytes match the reported mutated SHA `ca8ad4334416ee29317eff4a3aaab53e089af306aeaceba33228f67adb86799f` at `w2/final-guards/verifier-na.json`, and the old gate snapshot is retained. This is not authentication of a real verifier. Corpus comparator now rejects member substitution/order or attribution mismatch and tool/input digest drift; deliberate arbitrary Python candidate-code forgery remains outside that counter's trust model and is disclosed.

S120 adds the reopened CPython3.14.8 lazy-annotation rule. Two advisory reports corrected their pre-3.14 eager-evaluation premise; forcing annotations remains explicitly unsupported, not silently certified. QUALITY applications are lesson-backed and add no new numbered calibration criterion. `SKILL.md`, README and both tripwire knowledge entries carry the source-scope corrections; `SOURCES.md` mutable-field changes and quotes live in lesson21. Isolated draft files were removed after integration; inherited external worktrees were not destroyed. Final code-bound measurements follow as separate retained receipts, never as a claim that earlier hashes measure later code.

Final pre-measurement static binding guard: an unresolved container index is not equal to an unresolved key merely because both use the same `LITERAL_MISS` sentinel. The resolver now leaves that callee unresolved rather than inventing a concrete selected body (`tools/mado-tripwire.py`, `callable_info`). This follows the same no-invented-observed-binding requirement; no extra claim or changed expectation is introduced.

First stable measurement at `ac16f1025dbb142b9c3fc26c9a3722ba62d90f23` retained primary35/35 and C2 twenty/twenty, with all capped resource sizes clean, but the supplemental positive guard caught CallbackBoundArgs (16/17, unparsed_spawns1). Root cause was representing a captured container as `ast.Constant(list)` rather than a literal List/Dict node. `literal_node` now preserves the actual bound argument in thread and stored-methodcaller replays; this is a code-only repair (lesson M12). The failed revision-bound receipt is retained in `evidence/final/oracle-final.json`, not overwritten to pretend the first integration passed.

C2 causal-separability replay is now executable as `.ufo/waves/round-21/assessment-independence.py`: it copies only the artifact gate and frozen C2 fixture subtree to a fresh external temporary tree, changes the inert C1 file from baseline bytes to changed bytes and then removes it, and runs only the same C2 selftest each time. It compares the complete C2 stdout bytes and return codes. No C1 classifier or fixture payload is executed; temporary scaffolding is removed by the runner. Its result is not assumed until a committed, revision-bound receipt is recorded.

At `a1e1b6083a1a0531ab0660f285792eaa2ea51712`, the repaired primary/supplemental oracle is35/35 +17/17; C2 is20/20 and byte-identical across baseline-C1/changed-C1/absent-C1 intervention states; the exact N/A mutant is rejected with `unnamed_nonauthor_verifier` exit1. The immutable legacy guard population retained recall_lost0/crash_flip0/a2_mismatch0/vcs_fn0/dup_rows0, but its pure24 found two newly introduced `logging.info` data leads (`evidence/final/guards-legacy-a1e1b60.json`). Exact logging message APIs are now classified as literal-data consumers, distinct from `logging.config.dictConfig` factories. The legacy VCS “fp” counter is26 versus20 under its old no-final-state truth; eight added commit/index/intent-to-add detections and two removed abbreviated dry-run flags require effect-boundary adjudication, never expectation edits.

C2's frozen selftest receives an independent code-fault proof through `.ufo/waves/round-21/assessment-mutation.py`: a temporary gate copy loses only its actual population-digest comparison, and the unchanged20-case oracle must reject that mutant. The runner never edits production, expectations or fixture payload code and removes its temporary clone. These observations and remaining constraints are retained rather than calling all legacy screens green.

### Round 21 — final residual rejection and durable handoff

Final residual call:3/4 reviewer reports completed; `FinalAssessmentReview` died on Codex capacity and was not replaced. `FinalBindingReview.md` reproduces silent wrong/missing current-code rows for factory capture lifetime, unresolved capture/global leakage, returned-name rebinding, direct run and synthetic-name hygiene. Parent Main confirmed **C1 harmed**, retain red receipts and finish report/commits only. C2's20/20, exact N/A rejection, killed digest-check mutant and C1-intervention equality remain separately demonstrated, not round admission. No behavior was patched after that disposition.

The new knowledge entry, SKILL, README, SCORECARD and lesson now carry an in-place reading route to the final withdrawal; earlier candidate measurements remain dated. QUALITY32 captures the newly exposed lifetime/scope/identity criterion after falsification without retroactive pass or C2 criterion-count credit. The delivered legacy count166/175 is explicitly recorded;172/175 remains round20 history, not the new result. `FinalRemovalReview.md` found no wrongly excused prior process loss in31 groups; `FinalEvidenceReview.md` retained unparsed-clean, logging source-scope, `--dry` effect-provenance, stale module-docstring, old A2 revision and capped-parser limitations. Dispositions and exact provider errors are in `.ufo/waves/round-21/residual/dispositions.json` and `outcomes.json`.

End source census exit0 and full immutable-revision source accounting115→120 are retained in `evidence/final/sources-{end,count}.json`; the start output was recovered from the same round's predecessor observation, not fabricated by rerunning a start time. Mandatory fleet misroot sweep showed only unrelated `.ufo/state/tabi.report-baseline` and `.ufo/watchdog.log` modifications, no untracked candidate; neither was touched. Launch digest: `2026-10-21T04:49:56-03:00 launch mado round=21 pgid=1089102 driver=hyaku-inline attempt=1`. Same held claim/attempt, replacement writer progressing through commits; no other mado round mission or next round was started.

L0 appended: `mado | round-21 | Post-third-rejection disposition requested` (full question in fleet `.ufo/l0-questions.md`), asking operator hold/unblock before another round. Closure, streak, MANIFEST and driver state are parent/operator work and were not edited. Final trends: expansion unchanged(no new admitted province ground/capability from this rejected round); quality harmed(current binding claim remains false); discernment improved, bounded to learning from the previous outside rejection into grounded criteria31/32 and retaining contradictions—not an outside spot-check by our dispatched seats. No promotion or host recovery; L1 installations none.

## 2026-10-21 — round 22: explicitly authorized recovery registration

Operator authorized attempt1 after the three-rejection block; this is permission to execute this recovery only, not admission or streak erasure. Base master `741122d177ae8ff68a73768777f20484d5bdcbe4`; preregistration landed `a963ce67e303db94201507a93018416e4e44fd23` before implementation or measurements. C1 operability targets the actual r21 F1–F5 static binding/callable/scheduled-run failures, six immutable originals plus independently frozen variants. C2 calibration, lowest measured non-retired axis, targets separate artifact-only evidence-tier/count consistency on independent frozen validity cases and the r19 six-incident evidence disclosure. Full specification: `.ufo/waves/round-22/registration.md`, `audit-contract.json`; no criterion-count credit or global safety claim.

Prior authoritative red receipts stay: `corpus/lessons/round-19-verifier-spotcheck.md` C3 precision harm, round20 outside rejection, round21 `residual/FinalBindingReview.md` and final harmed disposition. The historical six-line recall target was met but did not prove precision or no-harm; a5-observed/1-lead translation is not a new execution receipt for the old markerless tool. No re-admission proposal precedes independent non-author falsification. No r23, host recovery, compositor/config/package/service action or private-session census is authorized.

Wave1 validated and dispatched64 seats as one native taskCall; registry and identities `.ufo/waves/round-22/w1-{spec,run,assignments,record-success}.json`. L1 holds the canonical planner seat. The authoring-only wave freezes truth and bounded harnesses; no detector measurement or production implementation is assigned until seal. Initial census exit0 with six disclosed duplicate-URL warnings: `evidence/sources-start.txt`.

### Round 22 — raw truth seal, write-boundary correction and production implementation

Independent raw expectations/input digests landed `9185f1f9806b823a23ef9f5077a893e40e46e1b9` before production edits (`truth-seal.json`:106 rows). Normalized expected/JSONL fixtures are materialized later, with that chronology disclosed. Source S121/S122 now also cite `corpus/knowledge/tripwire-lifetime-recovery-r22.md`; used-by old→new is recorded in lesson22.

The two new production executor identities RepairBindings and ImplementEvidenceAudit died before delivery, both on Codex capacity `turn_rate_limit_exceeded`, exact errors in lesson22; neither was replaced or resumed. Main acknowledged coordinator-direct reachable implementation. The original living harness authors continue in separate actual sparse Git clones. Earlier concurrent new-harness drafting in the shared checkout violated the worktree rule despite disjoint paths: unfinished drafts are retained in `evidence/{oracle,audit}-assemble-shared-draft.py`, no retroactive isolation or collision-absence claim. Lesson22 M6/M8 records the conformance/provider debt.

L1 implemented C1 creation-time lexical literal/callable overlays with invocation-late globals, post-prefix returned identity, bounded factory resolution, construction-bound partial arguments and keyword overrides, collision-free scheduled target metadata, direct/aliased run/start plus cancellation/repeated-call state, and mutation uncertainty. Statement snapshots retain syntactically reachable dependencies instead of every unrelated module binding, so the new stored-closure resource population can test the actual capture path. The directly related stale Git dry-run docstring was corrected without changing Git classification. Production code: `tools/mado-tripwire.py`; no expected population was edited.

Separate C2 `tools/mado-evidence-audit.py` checks explicit label/count/error assertions and exact bounded input bytes, with fail-closed0/1/2 verdicts and self-invocation over the fixed fixture manifest interface. It imports/reads no classifier, host state or network, and cannot establish semantic truth, identity, chronology, admission or promotion. Actual r19 raw markerless data stays could-not-evaluate; derived consistent/counterfactual cases are not original r19 assertions. No implementation success, score or re-admission is inferred before the following pinned measurements and independent attacks.

### Round 22 — normalized harness integration before first detector measurement

All64 original W1 identities returned; their resumed harness work completed in isolated clones. Two additional production seats remain provider-dead, not replacements or successful deliveries. Final isolated OracleHarness/AuditHarness scripts were integrated by L1. Initial materialization receipts are retained red: `evidence/assemble-oracle.json` refused because addendum any-tier constraints were computed but not assigned; `evidence/assemble-audit.json` raised an uninitialized historical-case-list NameError. L1 corrected only these bookkeeping defects, preserving all raw source/expectation bytes.

Successful same-command retries (`evidence/assemble-{oracle,audit}-retry1.json`) materialized57 C1 cases =50 independent proposals +7 immutable originals, expected SHA `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357`; C2 has46 fixed validity/historical cases, expected SHA `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`. Raw truth remains the prior9185f1f9 seal; normalized materialization is explicitly later than production330de68, not a falsely earlier committed expected.json. `fixture-materialization.json` records chronology and explicitly named large fixtures.

Static integration also corrected the exact-case evaluator's erroneous demand for a lead/error signal alongside observed exact rows: exact truth means full row-multiset equality plus zero errors, while the signal requirement belongs to uncertainty cases. No wanted rows changed. Optional `--group proposal` permits before-measuring only the50 NEW independent variants, rather than rerunning six original user-reported failures merely to confirm them. `oracle/integration-decisions.json` records this before any detector measurement. Source/manifest integrity remains checked over the complete57-case population even for a group or single-case selection.

### Round 22 — first pinned measurements and audit envelope repair

At harness/tree revision `5c7b98312c2a89f8f59ae9d9f1c83895ed6cd065`, the same sealed new-proposal counter gives **13/50 before →50/50 after**; full current-code population **57/57**, including all six original r21 fixtures and the exact r19 pure-data negative. Receipts `evidence/first/oracle-before-new50.json` and `oracle-after-all57.json`; count command `python3 -I .ufo/waves/round-22/oracle/measure.py --tool TOOL --group proposal` (default full57 after). This is finite agreement, not no-harm or admission.

The first C2 runner stays red/could-not-evaluate (`evidence/first/audit-after.json`, exit2). All46 individual check exit codes and finding IDs match their frozen expectations, but the runner requires its exact contract authority string and the auditor's different equivalent wording failed that envelope comparison. Its selftest also refused the manifest's explicit root-directory inventory entry `.`. L1 changed only the authority spelling and recognition of `.` as the manifest root **when kind=directory**; snapshot relative paths still reject dot/traversal/symlinks, all expected cases/bytes remain unchanged. Actual revised-tool evidence follows; the first red receipt is not overwritten or called a green run.

The corrected-authority C2 runner at `a607f3eb3851a8e8f0dd90e41ae2271a5665af6e` now matches all46 per-case assertions but selftest still refuses the fixture inventory (`evidence/first/audit-after-corrected.json`, exit2). Narrow diagnosis found the deliberate POSIX filename `cases/AuditRawPathBackslash/root/sub\snapshot.json`: the snapshot API correctly rejects backslashes, but the fixture inventory must be able to hash that literal filename. Inventory-only parsing now permits literal POSIX backslashes and the pinned root-directory record, without weakening snapshot paths. The independent intervention driver's inventory parser received the same structural distinction before its first run. No fixture or expected verdict changed.

`evidence/first-metadata-correction.json` also names an L1 receipt-wrapper attribution defect: the original outer `selected_tool_sha256` field actually printed the current classifier digest. The unchanged raw stdout already carries the correct selected-tool digest (`tool_sha256_before` for C1, `tool_sha256` for C2); later wrapper receipts use distinct correctly named fields. The original observations are retained, not overwritten.

### Round 22 — settled W2 falsifies v1, then lexical ownership/caller-argument repair

All100 fresh pinned W2 seats completed; no W2 death or replacement. Their57 C1 single-case and39 C2 case checks agree with fixed expected verdicts, but the independently authored `NoHarmBoundary` extra probe falsifies C1's supported-form no-harm: a factory returning a module-level helper injects its unrelated local argv as an observed command. The actual red, truth and immutable input landed `03826903a0800c9334ec1b0aae9cfd90670faffe` before a repair. Initial57/57 is not admission.

Three additional static neighbours were frozen before patch/probe in `residual-truth/expected.json`, without changing the original50/57 population. Counter `residual-truth/measure.py` landed `7536183aaa06e8d5b3b500ec48823777ca069c4d`; its before command with `--new-neighbours-only` gives **0/3** at that revision, each producing an invented observed factory-local command (`evidence/first/ownership-neighbours-before.json`). The original known red was not rerun merely to confirm it.

Only after every W2 reader settled, L1 restricted new factory overlays to helpers lexically defined inside that factory; returning a module helper or forwarding an existing closure no longer attaches a foreign frame. Invocation arguments now bind in the original caller environment, and the captured lexical frame is installed only in the callee body, before parameter bindings. This fixes the actual ownership distinction rather than special-casing the observed argv or suppressing its row. After evidence and fresh residual advice follow; no revised pass is pre-claimed.

W2 also found inherited wrong rationale text on three C2 D1 cases and four duplicate historical case pairs. `audit/rationale-and-duplicates-correction.json` preserves the46-case denominator and original seals, names42 distinct pinned fixture trees and appends correct case-grain prose. All C2 verdicts/inputs remain unchanged. Independent source re-openings S121/S122 matched tags/digests/quotes; these are author-lane advice, not outside admission.

At v2 `8c7420938369103010b2601f2f78b61a94247a2a`, unchanged primary/original truth still gives57/57 and the actual C2 self-invocation passes46/46 (`evidence/first/oracle-after-ownership-all57.json`, `audit-selftest-final.json`). Supplemental ownership replay initially gives only2/4: the required module-global rows are restored, but a callable argument handed to an already-followed visible consumer is redundantly swept, adding a false lead or an extra uncertainty count (`ownership-after-four.json`). This red is retained. L1 now suppresses only that redundant reference sweep when the visible consumer was actually followed without unresolved/opaque body state; true inner unknown/deferred consumers still own their leads, and unresolved outer consumers retain conservative sweeps.

The C2 intervention evidence is explicitly narrowed to substitutions of the active `tools/mado-tripwire.py` path, not disappearance of every historical source snapshot. Before its first run the driver now records a heuristic staged classifier-copy inventory, the actual substituted path and unsubstituted candidates. W2 RecoveryIndependence's static source/provenance review found no classifier read in the delivered auditor, but runtime equality is not promoted to universal filesystem noninterference. No expected fixture, C2 verdict or historical raw label changed.

### Round 22 — replacement coordinator withdrawal and finite guard completion

The predecessor host died before its final withdrawal/landing. The replacement retained the same held round22/attempt1 and restored only the eight-line unsafe consumer-sweep suppression from4d308e5; production classifier bytes now exactly match v2 `8c7420938369103010b2601f2f78b61a94247a2a`, SHA256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`. This supersedes the preceding plan to suppress every already-followed consumer. `residual/ResidualForward.md` explains that container/attribute callback stores can escape a followed consumer and lose their lead; its additional caller-frame leakage finding remains unresolved. No new general interpreter repair or admission is claimed.

Re-verified inherited raw seal:106/106 files match size and SHA256 (`evidence/resume/inherited-inventory.json`). Primary unchanged57/57, old oracle35/35+17/17, eleven legacy selftests247/247, and C2 fixed46/46 are observed on the restored production bytes. Supplemental discovery remains2/4, exit1; strict C1 is unprovable/not admitted. Strict C2's unchanged markerless historical5/1 target remains unprovable/not admitted even though its bounded audit runs. The independent digest-check code mutant is killed:44/46, exit1, with AuditRawDigestTamper and AuditRawTamperMalformed failing. All receipts live in `.ufo/waves/round-22/evidence/resume/`.

Frozen1356-fixture comparison against actual delivered-r21 SHA46c82902 retains1214 groups, adds3, removes5, with107 unchanged error pairs and zero unequal error pairs. All eight changed finding groups and eight reduced unparsed counters have source-grounded author adjudication in `corpus-adjudication.json`; this is not an outside no-harm verdict. An initial wrong-baseline replay is retained as excluded `corpus.json`, never substituted for `corpus-delivered-r21.json`. Initial corpus/oracle probes overlapped despite the one-child-per-seat requirement; that conformance deviation is retained, not concealed. All subsequent scanner/resource/mutation probes were sequential.

The frozen assignment1000/2000/4000 and stored-closure512/1024/2048 populations pass API and CLI separately under384MiB/15s, with zero findings/unparsed errors. Assignment RSS API20268/23364/28708KiB, CLI29296/32800/38916KiB; closure RSS API21312/25156/31736KiB, CLI29412/34540/41220KiB. Resource driver exit0 alone is not the semantic verdict; actual scanner summaries are retained. r19 frozen matches, while unchanged r18 retains its expected historical mismatch.

Round spending is170 inherited seats:64+100 validated waves,2 dead production executors and4 residual advisers.165 reports completed; RepairBindings/ImplementEvidenceAudit died on the recorded Codex capacity error, and ResidualOwner/ResidualCaller/ResidualCallable have empty reports and terminal `Request was aborted`. Partial caller truth/scan evidence is retained without credit as a completed report. Four fresh three-seat residual requests were refused by `Background job limit reached (100)`, spawning zero; none replaces a dead identity. Exact accounting/role mixes are in `seat-accounting.json`.

All inherited round evidence is retained. Four obsolete sparse clones under `.ufo/worktrees/r22-*` were byte-archived as `evidence/resume/inherited-worktrees.tar.gz` with22 source paths/hashes and branch/base/status inventory, then removed; only their Git administration and generated bytecode are excluded. Source census remains exit0,120→122 rows (+2 A/mined); source dates, S121/S122 quotes, immutable fields and original red/v3 receipts stay unchanged. The fleet misroot sweep found no mado-owned file. No tool install, host probe/configuration/package/service action, claim-state write, streak reset or next round occurred. Active-path C2 intervention and revision-bound historical precision are recorded after this landing.

### Round 22 — intervention setup failure retained, stage boundary corrected

Recovery evidence landed `579109a6812f4d0a2dd47572caca241075c6021d`. The first active-path intervention could not evaluate: whole-repository archive extraction correctly refused the unrelated absolute symlink `.ufo/waves/round-17/tripwire/hardening/symlink-target.jsonl` (`evidence/resume/audit-active-path-intervention.json`, exit2). No C2 case ran, so this is not independence evidence.

The existing intervention driver now stages only the tracked auditor, active classifier and exact C2 fixture subtree from the selected commit, retaining safe tar extraction and recording the narrowed path list/copy-inventory scope. Historical classifier copies elsewhere are explicitly outside the staged tree, never falsely claimed absent from the repository. No production, expected fixture, cap, verdict or case changed. This is a reproducibility prerequisite fix, not a detector/admission expansion; the revision-bound retry follows.

The first narrowed-stage retry at `d6de0892a05c65aaea5454ab5017bd29e68be1c3` also remains could-not-evaluate, before any C2 run: Git does not record the deliberately empty `AuditRawPathDotDotInternal/root/sub` directory (`audit-active-path-intervention-retry.json`, exit2). The driver now recreates only missing directory entries named by the committed digest-pinned fixture manifest, after rejecting symlink ancestors, and still verifies the exact full inventory. No file, wanted result or symlink target is synthesized. This fixes clone reproducibility rather than weakening an input-tamper verdict.

### Round 22 — completed bounded intervention and final handoff

At `78b182400b048708a82cfb8b6a7e3bc5459fcc0e`, the corrected active-path intervention passes235 runs =47 commands (46 fixed cases plus the real self-invocation) ×5 classifier states: baseline, changed, absent, read-FIFO, execution-marker. Exit codes and complete outputs match; fixtures/auditor remain unchanged; positive controls distinguish baseline/changed, time out on the FIFO and produce the execution marker (exit83). Exact receipt `evidence/resume/audit-active-path-intervention-final.json`, exit0. This covers only the explicitly staged active classifier path, not every historical source snapshot, stat-only access or deliberate evasion.

Historical precision measured at `579109a6812f4d0a2dd47572caca241075c6021d` is unchanged166/175 (P66/66,S17/17,W21/22,H47/52,L15/18). `precision-comparison.json` compares every case against the delivered-r21 receipt: zero previously passing-case losses, identical175-case names. No target was reset or disagreement hidden. The auditor SHA277eced2 and classifier SHAcd9da20c remain the measured production bytes.

Fresh-clone fixture setup is explicit in `empty-directory-materialization.json` and SKILL.md: Git cannot represent three intentionally empty fixture directories; recreate only those pinned directories before standalone C2 selftest/measure. The intervention driver handles exactly that setup internally and preserves every expected byte/label. Two failed setup receipts remain separate could-not-evaluate records, never converted into passes.

Final author verdicts: strict C1 and C2 unprovable/not admitted; expansion unchanged (no province frontier or admitted recovered capability), quality unchanged (bounded repairs/evidence, unresolved detector defects marked), discernment improved only in the grounded-learning sense (previous outside rejection became criteria/lessons, unsafe candidate withdrawn, contradictions retained). No outside-lane admit/reject spot-check is claimed. L0 disposition is appended in the fleet queue; the rejection hold, closure and any future authorization belong to the parent/operator. Stale-lane: the predecessor was killed; this same held attempt progressed through replacement commits, no other mado mission or r23 was started. No tool installation/update occurred.

## 2026-10-22 — round 23: repair-first recovery (operator ruling D11)

Motivating evidence. MANIFEST rounds[400] (round 21, operability harmed: binding failures F1–F5 and a
precision drop 172/175 → 166/175) and rounds[426] (round 22, C1/C2 unprovable: supplemental 2/4,
caller-frame leak, routed defects on census pasting and on expectation commit order). The operator
lifted the mado block for this one round at 10:43:09Z. Registration
`.ufo/waves/round-23/registration.md` and the frozen 12-case repair set landed at `6b383c46`
before any production edit; counter clarifications landed at `a28e4815` and `4de44647` before any
after-measurement.

C1 (operability, repair). Wave-1 executor ExecFullB produced a scope-provenance candidate; it
landed at `2e592aff` (12/12, all guards green). Wave-2 critics then found real regressions against
base that no registered guard covers: a global-store callback silent miss, 13 of 45 recall shapes,
and frame-reuse and binder regressions. The L1 repaired them at `03227ddf` (allowlist escape gate,
per-call frame tokens, scope-correct `own_names`, unbound own names shadow outer scopes). At
`3732c7a7` the repair set is 12/12 (`evidence/repair-after-3732c7a7.json`), the round-22
supplemental is 4/4, the round-22 primary 57/57, round-21 oracle 35/35 + 17/17, selftests 247/247,
precision 166/175 with the identical passing set, corpus comparator 0 added / 0 removed / 0 error
flips with one reduced unparsed counter (`b14_called_spawner.jsonl`, adjudicated: the call raises
TypeError in Python, nothing runs), and all four resource populations clean
(`evidence/guards-fix5-scratch.json`). The wave-2 attack fixtures report zero regressions at the
repaired tool (`evidence/attacks-fix5.txt`; AttackFrameScopes, AttackRecallRegress addenda). H2
(precision 172/175) is not restored; reason in the registration's second clarification.

C2 (coverage, learning, sourced). New note `corpus/knowledge/terminal-trees-r23.md` with 30 new
SOURCES rows S123–S152 (29 mined, S132 queued): tag-pinned foot 1.28.0, kitty v0.49.2,
ghostty v1.3.1. Counter `c2/count.py` 0/3 → 3/3 at `3732c7a7`. Host fact: none of the three
terminals is installed; each tree is declared bytes with no consumer. SKILL.md gains a three-row
decision table; the corpus README frontier records the move.

C3 (calibration). SHONEN box 4 asserts PROVINCE accuracy; PROVINCE named no row for five tracked
tools. Append-only PROVINCE refinement with a five-row table, then a wave-2 correction of the
`mado-verify.sh` reads, the tripwire redaction scope and the mori/tsukuroi overlaps. Counter
`c3/count.py` v2 5 → 0 at `3732c7a7`.

Swarm: wave 1 36 seats (v1), wave 2 33 seats (v1), total 69; five wave-2 attackers were resumed to
re-run on the repaired tool (no new seats). No tool installs.

### Round 23 — C1 withdrawn (append-only)

Late wave-2 reports (AttackLateCell re-run, ReClosureNeighbour) showed regressions against base that
no registered guard covers. One more fix attempt broke the repair set (11/12) and was discarded.
The production classifier is restored to base bytes `cd9da20c…`; the candidate stays as evidence.
C1 is an honest stop at 6/12. Fourteen still-running wave-2 seats were cancelled at the wrap-up
point (their partial reports, if any, are kept); no seat was replaced.

## 2026-10-23 — round 24: repair-first routing, rule attribution route, capability re-demonstration

Base `8e5d9369` (round-23 closure commit). Dispatched 03:02Z. Anti-loop: no change under `tools/`; the
tripwire streak (rounds 20–23) is not worked. Registration, both frozen counters and twelve control
receipts landed before any data seat (`8efd00af`, `d9fec1d3`, `4f21d995`, `c9b76646`, `464a0245`).

Repairs routed from the round-23 outside spot-check: lesson-23 stale sentence corrected; README
withdrawal pointer; QUALITY criteria 33–35 with two checks shown able to fail on round-23 bytes;
the round-23 wave-2 regression fixtures frozen as `carry/` (28 fixtures, no classifier change).

C1 (coverage, sourced). The README frontier item "rule attribution" moves to
`corpus/knowledge/rule-attribution-r24.md`: no Hyprland 0.56.2 channel maps an applied property back to
the rule that set it; the usable route is a unique `tag` effect read from `hyprctl clients`. SOURCES
S153–S168 (S161 queued). Counter v2 `c1/count.py` 0 → PASS_ROW 23/26 from 14 sources, TARGET_MET at
`cf86f9e0` (re-fetch mode). Wave-1 reviewer and critic showed v2 can also be met by true but
non-attribution rule lines (lesson M24-2); wave 2 judged each row by hand.

C2 (calibration). SCORECARD's twelve capability rows were re-run with frozen commands
(`c2/manifest.json`). Base 1/12 mismatches: `tripwire evidence marker` claims L 17/18 but the current
classifier gives L 15/18 (round-21 harm H2). A round-24 status table records each observed status;
counter `c2/count.py` 1 → 0 at `81955bd5`. Two base runs gave identical rows (no flake).

Mistakes mined: lesson-24 M24-1..M24-4 (v1 counter met by two controls and fixed before data; v2
residual hole; round-23 seat reports rewritten after the tip; a one-character `agent://all` message).

### Round 24 — wave 2 (append-only)

Wave 2 (40 seats) re-opened all 16 new sources (all hold) and re-ran both counters at `39c59630` (C1 TARGET_MET
23/26; C2 0/12). It found the C1 counter met by generic rule lines (12 of 23 passing rows carry attribution
content), five prose errors in the new note (tag latch, enable/disable scope, log label, ordering scope, socket2
count), and that C2's population is 12 of 15 capability rows with one outside row stale. Corrections are appended:
note errata, a SCORECARD scope note, lesson-24 M24-5 and wave-2 dispositions, and README index rows for the three
notes that the navigation counter showed unindexed since rounds 21–23. No predicate, manifest or claim row changed.

## Round 25 — Hyprland oracle counter, bind-table resolver, current-state ledger (2026-10-23)

Three attempts (two died with the orchestrator). Attempt 1 landed registration, counter v1, ten v1 control receipts
and counter v2; attempt 2 landed counter v3; attempt 3 found that v1–v3 took every generated case's expected bind
table from the counter's own line model, so a transcription of the model would meet them whatever Hyprland does.
Counter v4 (`1ed41fa8`) keeps v3's case generator and asks Hyprland v0.56.2 itself: a nested instance per case tree
(exec lines removed), read back with `hyprctl -i <instance> binds -j`; the unperturbed tree must equal the live table.

Before any data seat, ten control shapes were scored under v4 and landed (`459dd17f`): do-nothing, `[]`, junk, server
echo, Hyprland shell-out, encoded table + delta parser, grep of every bind line, easy-grammar parser, label-keyed
detector, no-reader. None met it (best 37/41: the label-keyed detector, which learned the case type from
`/proc/self/mountinfo` — lesson M25-2). Then two data seats wrote independent resolvers; the first returned
(`ExecBindToolA`) landed as `tools/mado-binds.py` at `ef94763c`, and the single measurement gave
`PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET` (seed `ed0d8a943980d2f2`). Sources S169–S172 opened;
S162 and S167 gained the new note in used-by; `corpus/knowledge/bind-table-r25.md` landed.

C2 (exploratory): SCORECARD `## Current state (round 25)` lists the 15 capability identities with a fresh run at
base each (13 work, `:437` and `:1342` fail as stated, four documentation defects), every row re-derived by a second
seat. Routed round-24 repairs: A18 in-row correction, S161 and receipt-chronology corrections, SCORECARD pointers,
QUALITY 36 with a check red on round 24 (its mutant coverage is weak: lesson M25-3); the population-equality part of
routed defect 2 stays open (M25-4).

## Round 26 — isolated Hyprland oracle, animation-table resolver, hyprlang arithmetic in binds (2026-10-23)

Round 25's oracle ran nested Hyprland on the operator's live session (windows on the desktop, ~1330 SIGABRT coredump
records). Hyprland 0.56.2 cannot run headless alone (no allocator without a DRM fd), so each nested instance now gets
a private headless tinywl (wlroots 0.20.2, patched to offer wl_compositor/xdg_wm_base v6) inside bubblewrap: no host
`/run`, cleared env, private runtime dir, only the amdgpu render node, `dispatch exit` to stop. Pilot ISOLATED_OK;
w1 IsolationProbe sampled 288 nested pids during a counter run: all private, live clients unchanged, no coredumps.

C1 (coverage): counter v1 froze first; w1 critic showed its append-only cases could be met by a snapshot cache, so v2
(append/edit/independent trees + Hyprland version guard) froze before data and every control was re-scored (best
9/41). `tools/mado-anims.py` (ExecAnimToolA) landed at `2b3487f7`: 41/41. Note `animation-table-r26.md`, sources
S173–S177. C2 (operability): `tools/mado-binds.py` now evaluates hyprlang's one-operator float `{{…}}` expressions
(ExecArithToolB) at `a496b02a`: 51/51 (round-25 tool 22/51). Repairs: label-free case paths (M25-2), counter
self-test with drift and embed witnesses, QUALITY 37 population equality, Q36 successor with `--counter-sha`,
round-25 R8 correction, ledger rows `:1409`/`:1410` second-derived. Open: tool-sandbox `/proc/1/environ` leak,
surviving gate-check mutants, three coredumps from seat crash probes (lesson M26-5…M26-8).

## Round 27 — workspace-rule table tool, offline gates that fail red (2026-10-23, attempt 2)

Attempt 1 (phase-4 orchestrator, ~09:30-03) froze C1 counters v1→v4 (three pre-data redesigns under the kill rule: v1 append-only, v2 prefix-keyed fixtures, v3 top-of-file definitions — each met by a partial reader, each retired before data), scored 13 C1 control shapes, sealed the held-out set H, landed both C2 suites from first-returned data seats, re-scored C2 controls, then died before C1 data and any measurement; watchdog `lane-dead-no-report mado round=27` (fleet `.ufo/watchdog.log:931`). Attempt 2 inherited all of it (re-verified: counters' sha256 match the registration pins, seal matches H bytes, w3 RevProvenance PROVENANCE_OK), landed the data, measured both claims, and finished the corpus.

C1 (coverage, sourced S178–S182 + S158/S162): the inherited ExecWsToolA bytes (unreturned — seat died mid-flight) were landed byte-exact and piloted: 19/41, all 22 failures carrying ONEMPTY (its `on-created-empty` value slice keeps a leading colon). ExecWsToolC returned an independent implementation (dev-validated 41/41 on four seeds incl. BYTE_IDENTICAL raw capture); its bytes landed unmodified at `20022a65` and the single official measurement gave `PRED-C1-r27-v4 cases_pass=41/41 verdict=TARGET_MET` (seed `4cfdf858277ad362`, coredump delta 0). Note `corpus/knowledge/workspace-rules-r27.md` (measurement-status section), capability row in SCORECARD. W1→w3 attack chain: 13 controls (best 32/41), 3/3 tool mutants killed on the 13-tree oracle probes, critic-prompted v4 shapes.

C2 (operability): measurement 1 at `48b9434a` (suites from ExecSuiteA1/ExecSuiteB2 first-returned bytes): green=17/17, w_killed=15/15, h_killed=12/18 vs h_need=14 — TARGET_MISSED on three named suite-A survivors (extra-disjunction, unstable-conjunction, embed-boundary; all c2-counter subjects). Per the registration repair flow (repair seats never read the sealed H directory), w4 repaired suite A; measurement 2 at `0b53bd86`: green=17/17, w_killed=15/15, h_killed=15/18 vs h_need=14, `verdict=TARGET_MET`, exit 0 (`evidence/c2-after-0b53bd86.txt`). Suite B independently confirmed (MutSuiteB: 3 fresh checker-class mutants killed, 46/46 greens).

Spotcheck debt (r26 §7): items 1/3 (M26-10 PROVINCE + binds docstring) landed at `b6650d5`; item 4 SKILL.md registry rows landed (six rows, r26+r27 gates); item 6 population-run citation fixed in SCORECARD with `evidence/r26-population-after.txt` + hidden-dependency note; item 5 Q36 successor landed (`quality/check-control-receipts.py`, receipts `quality/q36-successor-receipts.txt`; two survivors routed: glob-case, marker-case); item 7 host-safety terms carried through every receipt (delta 0); item 2 seeds-per-control routed with the survivors. QUALITY-37 run on the C1 receipt: exit 2 UNREADABLE (open-ended PRED-C2 totals not parseable — routed extension).
## Round 28 — SKILL citation erratum (2026-10-23)

- 2026-10-23 — round-27 SKILL citation erratum: supersedes `SKILL.md:631-636` with
  `SKILL.md:630-635`; the citation was off by one after a header edit. At the
  round-27 closure commit `767b12db62ceb3ad38d24a13e4c693b4375ceb5a` and
  wave-start tip `4f610066efd90804b055c42ae20c41a7f44404f9`, the registry's
  three round-27 rows are `mado-r27-counter-selftest` at 633,
  `mado-r27-population-suite` at 634, and `mado-r27-control-receipts` at
  635; together with the round-26 rows at 630-632, the registry span is
  630-635. Evidence command:
  `git show REV:SKILL.md | grep -nE 'mado-r(26|27)-' | cut -d'|' -f1-2`
  (run once at each revision) returned 630 r26-counter-selftest, 631
  r26-population, 632 r26-control-receipts, and 633/634/635 the three
  round-27 rows above at both revisions.

## Round 28 (2026-10-24, attempt 1 after stale-claim reset; completing attempt)

Inherited seven dead attempts (watchdog `lane-dead-no-report mado round=28` ×7, last OOM-killed mid-work);
reused committed work through 317ff19 and completed the round. Attempt-1 (2026-10-23) waves ran in-session:
w1 39 seats one batched dispatch (6 reports landed), w1b 32 seats prepared (registry, 0 reports), w2 34 seats
one batched task call (w2-run.json; 11 reports landed). Round total 105 seats; 72 seats died with the attempt
and are recorded name-by-name in the three swarm registries.

Evidence landed this attempt, all measured 2026-10-24 against committed bytes:

- C2 calibration: `python3 -I .ufo/waves/round-28/c2/count.py 77cdda869ec616cb38cda494d992e57153a4a602`
  → nine CHECK lines PASS, `PRED-C2-r28 verdict=TARGET_MET`, exit 0
  (`.ufo/waves/round-28/evidence/c2-after-77cdda86.txt`). Before: 1/9, TARGET_MISSED
  (`.ufo/waves/round-28/controls/K2DoNothing.txt`). Eight unresolved round-27 record conditions repaired,
  D9 retained; the lesson-citation rubric is not re-scored by this claim.
- C1 operability (sourced S183): composite `count.py 77cdda86` → per-leg vector
  `.ufo/waves/round-28/evidence/c1-after-77cdda86.txt` (h2-rotate, refpub-kills 12/12, q36-witness,
  q37-open-ended PASS; h1-rotation and boolword-v5 FAIL inside the composite for two evidenced reasons).
  - h1-rotation after-state: `.ufo/waves/round-28/w2/reports/ReviewerSuiteMonotone.md` — new suite
    `h_killed=18/18 verdict=TARGET_MET`, monotone, three `held-c1v2` survivors KILLED; H1's ephemeral
    dependency was declared in the registration and the directory was cleaned before closure.
  - boolword-v5 after-state: `count-v5.py 77cdda86 --seed 28c1a8c0ffee0001` → 41/41, boolword 2/2,
    exit 0; `--tool-file ref-mutants/exactbool-tool.py` → boolword 0/2, TARGET_MISSED, exit 1. The composite
    guard pins count-v4.py at 3d7d301f… (never matched committed 635ae788…, verified at 5198cc8 and 20022a65)
    — frozen-counter defect reported verbatim; composite prints TARGET_MISSED exit 1.
  - Oracle restored by byte-identical rebuild: `.ufo/waves/round-26/harness/build-tinywl.sh` reproduced
    tinywl `227a74af…` and libwlroots `1f3d7036…` exactly (recipe pinned in `.ufo/waves/27/harness/oracle.py`);
    no package installs; meson 1.12.1 / ninja 1.13.2 / gcc 16.2.1 already present.
  - refpub public reference set authored from the three committed public subjects, 4 mutants + 2 benign rows
    per subject, sealed `c1/refpub-seal.txt`, scored 12/12 by the frozen round-27 counter.
- Sources census: validate exit 0 at start (182 rows, `evidence/census-start.txt`) and end (183 rows,
  `evidence/census-end.txt`; +S183 mined by `corpus/knowledge/mutation-testing-r28.md`; W04 warnings unchanged).
- Lesson `corpus/lessons/round-28.md` gained M28 rows (composite guard pin; ephemeral-input preservation;
  blind mutant authoring) alongside the inherited M27-3 row and the S183 gate.
- Fleet misroot sweep re-run at write time: 0 mado-owned fleet-root files (foreign untracked files untouched).
- Host safety: Hyprland coredumps 1338→1338 on every oracle receipt; no compositor/config mutation.

Lane tip at write: 77cdda869ec616cb38cda494d992e57153a4a602 (push verified by the lane helper). Round-shape,
wave seat-mix, dead seats, trend verdicts and the verbatim composite output are in the round report
`.ufo/reports/round-28/mado.md`.

Correction to the round-28 entry (same round, append-only): the no-in-tree-report seat count is 88, not 72 —
w1 33 (39 declared − 6 reports), w1b 32 (32 − 0), w2 23 (34 − 11), all named in the three committed swarm
registries. "No in-tree report" is not "no work": those seats' outputs are carried by the integration commit
317ff19; the count measures reports, not production.

## Round 29 (2026-10-24, attempt 1)

Registration `.ufo/waves/round-29/registration.md`, frozen at `aeb4f58b`, re-frozen at
`3ae437ca` (the QUALITY-38 freeze smoke caught a cosmetic defect — the repaired composite's
self-print label still read `c1-r28`; fixed, re-frozen, re-smoked; both receipts committed).
Base `f652ca99` (round-28 closure: rejected-honest-stop; r28 records stand untouched).
Two claims: C1 operability (repaired six-leg composite, `PRED-C1-r29`), C2 calibration
(four routed record repairs, `PRED-C2-r29`).

- C1: the round-28 composite's guard pin (count-v4.py `3d7d301f…` vs committed
  `635ae788…`, M28-1) is corrected in the re-frozen `.ufo/waves/round-29/c1/count.py`;
  leg h1 adopts the QUALITY-39 named committed-receipt basis
  (`.ufo/waves/round-28/w2/reports/ReviewerSuiteMonotone.md`, owner mado, named at data
  time in the registration). Freeze smoke at `3ae437ca`: all six legs PASS,
  `PRED-C1-r29 verdict=TARGET_MET` exit 0 (`evidence/c1-freeze-smoke-3ae437ca.txt`);
  first smoke at `aeb4f58b` is kept as `evidence/c1-freeze-smoke-aeb4f58b.txt`.
  Before-state at base: `evidence/c1-before-f652ca99.txt` — h1 FAIL (ephemeral),
  boolword FAIL (`normal=missing mutant=missing`), four legs PASS, `TARGET_MISSED` exit 1.
- Kill-rule controls (committed with the freeze): `controls/C1K1-r28composite.txt`
  (unrepaired r28 composite at base → TARGET_MISSED), `controls/C1K2-pinonly.txt`
  (pin fixed, h1 still ephemeral → h1-rotation FAIL rc=2 no-tally → TARGET_MISSED;
  the same run proves the repaired pin makes the boolword leg print real tallies),
  `controls/C2K1-donothing.txt` (C2 counter at base → `R1..R4 FAIL` exit 1).
- Routed item 3: standalone v5 receipts committed —
  `evidence/v5-standalone-normal.txt` (41/41, boolword 2/2, exit 0) and
  `evidence/v5-standalone-mutant.txt` (boolword 0/2, exit 1), full outputs with
  counter self-print lines; HOST_SAFETY coredumps 1338→1338.
- Routed item 4 (§6.6 tenth record defect): append-only erratum in SCORECARD.md's
  round-27 section (`§6.6 erratum (round 29)`) — the r27 report sentence "the tool's
  docstring and the knowledge entry cite them [S178–S182]" overclaims; the S### citation
  lives in the knowledge entry frontmatter; the docstring cites upstream filenames.
  Shown able to fail: `CHECK R4 FAIL` at the C2 do-nothing control.
- Sources census: before 183 rows (committed base blob receipt
  `evidence/census-before.txt`; matches the r28 census-end receipt) → after 184 rows
  (+S184 Schuler & Zeller "Covering and Uncovering Equivalent Mutants", STVR 2013,
  opened 2026-10-24 at the DOI reader, title-level grounding per the S183 treatment;
  gate in `corpus/lessons/round-29.md`); census validate exit 0 at round end.
- Lesson `corpus/lessons/round-29.md`: M27-4 (the §6.6 reference-drift, fix shown able
  to fail) + the honest sweep row (selftest 460/460 exit 0; controls re-verified; the
  navigation counter reads 41/43 at base AND tip — an inherited r27/r28 index gap,
  routed to round 30, not an r29 regression and not silently repaired).
- Wave-1 spec `.ufo/waves/round-29/w1-spec.json` (33 seats) validated under policy v1
  (`w1-plan.json`, plan exit 0). PREPARED but NOT dispatched: this L1 seat has no
  swarm-dispatch tool on this host surface; the orchestrator dispatches prepared waves
  between rounds. Itemized in the round report.
- Host safety: no compositor/config mutation; oracle pins verified (tinywl
  `227a74af…`, libwlroots `1f3d7036…`); every oracle receipt HOST_SAFETY delta=0.
- L0: the two round-28 questions are answered-by-implementation (receipt-basis adopted;
  pin repair shipped as a NEW r29 claim, r28 record untouched) and remain open for
  operator overrule; a round-29 L0 line notes the adoption.
- Inherited finding (not repaired, claim discipline): navigation counter 41/43 —
  `mutation-testing-r28.md` and `workspace-rules-r27.md` missing from
  `corpus/README.md` index rows at base and tip alike.

Measurements land in the round records; the round report cites the pushed lane hash
at write time. Round shape, seat mix, trend verdicts and the verbatim composite output
are in the round report `.ufo/reports/round-29/mado.md`.

## Round 30 (2026-10-24, attempt 1)

Registration `.ufo/waves/round-30/registration.md`, frozen `451e8b3c`
(with counters `c2/count.py`, gate `quality/check-index.py`, controls
C1/C2/C3 and the before-receipts). Base `8f51071b` (round-29 closure:
admitted; the inherited 41/43 navigation gap routed here per
`corpus/lessons/round-29-verifier-spotcheck.md`). Data commit `446dc396`.
Three claims: C1 coverage (index rows), C2 calibration (lowest axis),
C3 operability capability (sourced: S185).

- C1: `corpus/README.md` gains index rows for `knowledge/workspace-rules-r27.md`
  and `knowledge/mutation-testing-r28.md` (r27/r28 inherited gap). Frozen
  fence: `indexed=41/43` exit 1 at base → `indexed=43/43 missing=0
  dangling=0 duplicates=0` exit 0 at `446dc396`
  (`evidence/c1-{before-8f51071b,after-446dc396}.txt`). Do-nothing control:
  the same fence at base is red — registered K1.
- C2: `corpus/QUALITY.md` grounds every active criterion — rows 41–45
  supersede the citation-less seed 1–5 (ground `MINT.md` + M30-1), 46/47
  move 18/19's citations onto the numbered line, 48 canonicalizes 32's
  `lesson round21` spelling, 49–51 give 38–40 canonical paths, 52 is the
  new record-then-claim criterion (M30-2). Counter
  `python3 -I .ufo/waves/round-30/c2/count.py REV`: base literal 28/40
  resolved-active 31/39 TARGET_MISSED (`controls/C2K1-donothing.txt`) →
  `446dc396` literal 40/52 resolved-active 40/40 TARGET_MET exit 0
  (`evidence/c2-after-446dc396.txt`). Superseded lines leave both
  denominators (criterion 21→20 precedent); literal and resolved metrics
  reported side by side per criterion 22.
- C3 (capability, sourced S185): `quality/check-index.py` implements the
  frozen fence's row-set semantics — red at base (`indexed=41/43` exit 1),
  green at tip (`indexed=43/43` exit 0), `--selftest` 6/6
  (missing/dangling/duplicate/symlink-refused/empty). All three receipts
  in `evidence/c3-after-446dc396.txt`. Capability row enters SCORECARD.
- Freeze smoke (criterion 49): all three counters run at the freeze commit
  `451e8b3c` and print real tallies (`evidence/freeze-smoke-451e8b3c.txt`).
- Sources census: 184 → 185 rows (+S185, own-work; validate exit 0 at the
  archived base tree and at tip; W04 warnings re-checked under criterion 17
  — each pair is supersession or distinct-scope reuse, no action).
- Lesson `corpus/lessons/round-30.md`: M30-1 (ungrounded criteria, fix
  shown able to fail at the base control) + M30-2 (the inherited index
  gap's two-round persistence; the sweep recorded it, no gate caught it).
- Harm watch: `MADO_SELFTEST: 460/460` exit 0; `git diff --stat 8f51071b
  master -- tools/ corpus/knowledge/ SKILL.md PROVINCE.md` empty; no
  compositor/config mutation; misroot sweep clean.
- Wave: `.ufo/waves/round-30/w1-spec.json` (33 seats) validated under
  policy v1 (`w1-plan.json`, plan exit 0). PREPARED, not dispatched — this
  L1 seat has no swarm-dispatch tool; the orchestrator dispatches prepared
  waves between rounds. Itemized in the report.
- L0: none new. The two r28/r29 answered-by-implementation questions stay
  open for operator overrule (fleet `.ufo/l0-questions.md:133-135`).

The round report `.ufo/reports/round-30/mado.md` cites the pushed lane hash
at write time.

## Round 31 (2026-10-24, attempt 2 — attempt 1 died pre-prompt on a Kimi 429)

Registration `.ufo/waves/round-31/registration.md` frozen `6803a999`;
data `f621e3c0`; wave spec `72021ded`. Base `274f7355`. Three claims on
three distinct surfaces, each measured without the others:

- C1 (coverage, row-fidelity surface — the routed C1 blind spot): new
  `quality/check-index-rows.py`. Base `rows=43 errors=1` on the r26 row's
  2-cell defect; tip `errors=0` after the README cell repair; selftest
  10/10. The r30 fence's byte-stream name-match stays the navigation gate;
  this gate checks what a row *carries*.
- C2 (calibration — lowest sub-axis at base, resolved-active 0.9750):
  counter v2 resolves every grounding citation (slugged heading in the
  named file, spell form in bytes, bare path non-empty, `outside`
  corroboration-only, `active≥30` floor vs supersede-all). Base UNRESOLVED
  criterion 35 (`M23-7` cited under `#mistakes`, actually under
  `### Final C1 disposition`); tip resolved-active 41/41 TARGET_MET after
  rows 53–54 + the criterion-35 cite repair. Four negative fixtures
  committed; n2 (non-empty unrelated lesson) still passes — the rubric is
  resolution, not relevance; routed.
- C3 (operability — routed C3 findings): `check-index.py` hardened —
  rev pinned through `rev-parse --verify --end-of-options`, symlinked
  corpus ancestors refused under `--root`, `--repo`+`--root` SETUP_ERROR;
  selftest 9/9 → 12/12; `43/43` unchanged at base and tip.
- Routed queue closed per registration §Routed queue items 1–3; item 4
  (no seat dispatch tool) recorded as expected surface.
- Harm watch: `git diff 274f7355..72021ded` touches only the five claimed
  paths; no compositor/config mutation; misroot sweep clean.
- L0: none new. Residual cheats routed forward: relevance-free lesson
  resolution (n2), Holds semantic accuracy, `outside`-only criteria 19/22/
  23/26/28 warnings.

The round report `.ufo/reports/round-31/mado.md` cites the pushed lane
hash at write time.

## 2026-10-24 — round-32 w1 ReviewEntryDispatch

Reviewed the two scribe drafts (dispatcher-semantics-r25,
dispatcher-surface-and-request-grammar-r26) against QUALITY.md and the
S188/S196 re-open seat reports. Evidence:
`.ufo/waves/round-32/w1/reports/ReviewEntryDispatch.md`; every quote,
count, hash and absence claim mechanically checked against the seat-report
bytes and the sha-matched scratch fetches. Result: r25 landable after
splitting one 28-word quote (S188:69 cell); r26 not landable — claims
"45 distinct names" against its own 47-name enumeration and the seat's 47
(47 — token-set diff of draft enumeration vs ScoutDispatchers0560.md
§vocabulary union, 2026-10-24), plus an unanchored §1 measurement block
(reload_config, signature drift, 404/flags/exec claims — all byte-checked
TRUE against the raw fetches except the 45/46 totals). No duplicated
dispatcher fact between the drafts.

## Round 32 — assimilation of the Hyprland IPC two-socket theme, and a calibration gate for the published axis table (2026-10-24, attempt 1)

Motivation: the round-31 outside spot-check admitted round 31 but recorded that
the lane published an axis table it never republished after its own commits moved
the counters (`SCORECARD.md:2014` still says calibration 39/40 and operability
9/9 while the lane's own instruments at that tip print 41/41 and 12/12), and the
operator's 2026-10-24 directive requires the lane to assimilate the shokuknow
corpus and mine `considerthese/`.

Work: (1) C1 — re-opened five sources myself on 2026-10-24 (fetched bytes
`.ufo/waves/round-32/fetch/S186.bin` 6,539 B sha256 `535bc4c385a06162…`,
`S187.bin` 268,731 B, `S188.bin` 12,879 B sha256 `c830ce0717f92776…`,
`S189.bin` 6,479 B sha256 `eea605dfe5ce09e1…`, `S196.bin` 297,863 B sha256
`f9b51362f2440e02…`) and admitted three entries on the IPC two-socket contract
theme with five normalized registry rows (S186, S187, S188, S189, S196);
evidence `corpus/knowledge/ipc-contract-r25.md`,
`corpus/knowledge/dispatcher-semantics-r25.md`,
`corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`,
`corpus/SOURCES.md:198-202`, `corpus/lessons/round-32.md` §Gate. The id-collision
guard was proven able to fail on an indented `  | S002 |` scratch fixture before
the first append (`collisions` file empty on the real pair: 185 registry ids vs
132 staged ids, 0 collisions). (2) C2 — landed `quality/check-axis-scores.py`
(selftest 17/17): the base revision measures `MADO_AXIS: checked=3 mismatched=2`
exit 1 and the tip measures `mismatched=0` exit 0. (3) Frontier step — the
census ran before and after; the round-32 lesson carries the Gate block (3
admits, 1 reject with reason and flip, the quarantine verdicts) and four
`## Mistakes` rows, two of them about this round's own seat scope violation.

Honest notes: two wave seats wrote outside their declared scope (the lane's
`corpus/README.md` and `LOG.md`); both files were restored from the branch tip
and re-applied under the L1 alone — evidence `.ufo/waves/round-32/w1/reports/`
and the `## Mistakes` rows. A seat's 187 MB scratch clone trees were committed at
`f5910876` and removed at `48f9fe09`; the bytes remain in history. The staged
package's **line** anchors were wrong (byte sizes and digests were right) and
were re-derived; see the lesson's `reference-drift` row.

## Round 33 — the round-32 C1 row was false, and the replacement counter was killed before data (2026-10-24, attempt 1)

Motivation: `corpus/lessons/round-32-verifier-spotcheck.md` rejected round 32.
The SCORECARD round-32 C1 row said target met at `cited_entries=3`. A re-run of
the frozen round-32 counter on `d9ed38166cc3be8ef4c52b41d66ad94010feb047` prints
`cited_entries=7`. The same closure measured the committed wave tree at
`f5910876` as 11.6 MB / 554 blobs, not 187 MB, and named twelve defects.

Work: a new calibration gate (`.ufo/waves/round-33/c2/count.py`) appends the
correction line rather than rewriting the false row. A new coverage counter was
frozen and scored against junk before any corpus append; a seat then showed a
symlink crib meets it. The entries were not appended. The axis-score gate's
locator no longer treats a quoted marker as the publication, and the round-32
before/after (`mismatched=2` at `256222890d935212874a09751ff9b7869943c2d7`,
`mismatched=0` at `d9ed38166cc3be8ef4c52b41d66ad94010feb047`) still holds.
`quality/check-axis-scores.py` is now in the SKILL.md gate registry.

## Round 34 — a counter that rejects the crib, then the data (2026-10-24, attempt 1)

Motivation: `corpus/lessons/round-33-verifier-spotcheck.md` rejected round 33.
The round-33 coverage counter was killed before data — a seat showed that the
frozen counter prints `TARGET_MET` on a symlink crib, so the entries were not
appended and the round closed as an honest stop. The closure also routed
defects: the S189 line number, the literature reject's id, twelve undisclosed
seat scratch trees and seven disclosed leftovers, the round-30 report
citation, and the un-re-executed axis-gate selftest.

Work: a NEW coverage counter, `PRED-C1-r34-v1`, was frozen before any corpus
append at `3420e827bd7b21b1374b23245526554ffd20d096` with its predicate
sentence identical in `c1/count.py`, `c1/frozen.json` and
`registration.md`. Its committed pre-data receipts show the symlink crib, the
symlinked-entry, symlinked-parent and symlinked-sources trees, the hardlink
tree, the entries-only, rows-only and used-by-prefix trees and the do-nothing
control all printing `TARGET_MISSED` exit 1, and only a regular-file golden
tree printing `TARGET_MET` exit 0. The round-33 counters are not amended —
their blob ids are identical at the round-33 freeze, the round-33 tip and this
round's tip. The data landed afterwards at
`fa7ba11346116672352b5d41494141c5c4d738d0`: one admitted entry
`corpus/knowledge/waybar-module-text-route-r25.md` and two normalized
registry rows S201 and S202, both sources re-opened by the lane on 2026-10-24
(fetch digests agree three ways — committed blob, `corpus/SOURCES.md`,
`c1/frozen.json`). The id-collision guard was re-proved able to fail on an
indented `  | S002 |` scratch fixture before the first append
(`controls/indented-guard.txt`), and the real pair produced an empty
`collisions` file (190 registry ids vs 140 staged ids). A NEW calibration
counter, `PRED-C2-r34-v1`, pins the published S189 queue-cap line number
against the pinned fetch: the publication was absent before and matches after
(`published=169 measured=169 mismatch=0` exit 0), while a `line=128` card and
a marker-less card both miss. One wave ran under
`scripts/hyaku/ufo-wave-policy-v2.json`: 64 seats validated by
`ufo-swarm-wave.mjs` (band 64–128, one task call), 25 of them attack roles
(reviewer 10, critic 8, mutation-tester 3, revenger 2, sentinel 2) = 39%; 64
dispatched, 64 finished, 64 reports, 0 dead seats. The frontier step mined
`considerthese/2026-10-24.md` item 4 — grounded by host probes, not by the
proposal text — and restated the literature reject against the opened file's
own ids (S206, S209, S210, S211), not S199.

Honest notes: the round-33 closure routed the S189 line-128 statement as
false; re-verification shows both line numbers are correct for their own
quote — line 128 holds the register's quoted `formatEvent` span and line 169
holds the queue-cap constant — so the repair is an appended disambiguation in
`corpus/lessons/round-33.md`, not a retraction. The wave's own mutation
testing found two clauses of the new counter that are honestly redundant
under its frozen spec: the 1–25 word bound cannot fail once the quote string
matches, and the `S_ISLNK`/`O_NOFOLLOW` pair protects only against a TOCTOU
race that no static tree can kill; both are recorded, neither is hidden. The
coverage claim is a bounded documentary-route increment, not a surface move —
the live bar module text stays open as frontier item U7. The twelve
undisclosed round-33 seat scratch trees and the six round-33 control fixture
trees are committed this round, so every round-33 receipt is re-derivable from
committed bytes;
`.ufo/waves/round-33/scratch/ExecK2Receipts` (495,961,904 bytes, three
throwaway git clones whose outputs are pasted verbatim into the committed
`.ufo/waves/round-33/w1/reports/ExecK2Receipts.md`) was moved out of the lane
tree to `/fast/scratch/mado-r33-k2-receipts/` rather than swept. The
axis-gate selftest is now re-executed with a committed transcript:
`MADO_AXIS_SELFTEST: 18/18 assertions passed` exit 0, live gate
`MADO_AXIS: checked=3 mismatched=0` exit 0
(`.ufo/waves/round-34/controls/axis-selftest.txt`). SHONEN stays `[~]` on all
four boxes; nothing was self-promoted.

## Round 35 — SimplifyCounter seat scratch (2026-10-24, wave-1)

Seat task: propose a minimal form of `.ufo/waves/round-35/c1/count.py` keeping
the nine live clauses and the PRED-C1-r35-v1 predicate. Proposal lives in
`.ufo/waves/round-35/scratch/SimplifyCounter/` (`count-min.py`, 104 lines vs
218, plus `analysis.md`); the committed counter is untouched. Evidence:
differential run over `controls/golden` + ten c1 control trees + `.txt`
root-misses + `--root .` gave 21/21 identical stdout/exit pairs; tampered and
missing `--frozen` both exit 2. Drops split into provably dead weight
(`hashlib`/`digest` computed-but-unread, `import os`, `__future__`, helper
folding, regex alternation) and out-of-scope defence (`MAX_BYTES` cap,
`nlink != 1`, explicit `S_ISLNK` branches subsumed by `lstat`+`S_ISDIR`/`S_ISREG`,
`O_NOFOLLOW` — declared non-load-bearing in `c1/clauses.json`, and the
root-symlink gate). Residual divergences (symlinked root, hardlinks, >8MB
files, merged drift message) are enumerated per drop; none is clause-visible.
Findings: `.ufo/waves/round-35/w1/reports/SimplifyCounter.md`.

## Round 35 — MutC1Drop seat scratch (2026-10-24, wave-1)

Seat task: mutation-test the PRED-C1-r35-v1 counter
(`.ufo/waves/round-35/c1/count.py`) by dropping one clause at a time on
copies under `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` (15 mutants,
`gen_and_run.py`), each run over all 11 frozen control trees. Baseline
reproduced all committed `.txt` receipts. Seven conjuncts are verdict-live
with a 1:1 control each (row-unique, used-by-exact, status-mined,
recheck-valid, digest-match, word-bound, quote-substring). Dead under the
frozen spec: ledger-"live" `row-well-formed` (c1-row-extra-field's shifted
cells are killed by status/used-by first) and `entry-regular`
(c1-entry-symlink's leaf resolves to an entry with no S205 gate-quote);
non-ledger `blob is not None`, `st_nlink != 1`, `entry_closed` seed,
S_ISLNK walk (masked by S_ISREG+O_NOFOLLOW for leaf links), and O_NOFOLLOW
(declared non-load-bearing; confirmed). `quote is not None` is verdict-dead
but counter-live on c1-entry-symlink (8/0 vs 7/1). Committed counter
untouched (sha256 78c25892…d12abad6). Findings:
`.ufo/waves/round-35/w1/reports/MutC1Drop.md`.

## Round 35 — the idle-lock control surface lands; the ledger claim is falsified against itself (2026-10-24/25, attempt 2 of 2)

Motivation: `corpus/lessons/round-34-verifier-spotcheck.md` routed four defects into this
round — the `1-25` word bound in `PRED-C1-r34-v1` was dead code under its own frozen spec, the
`S_ISLNK`/`O_NOFOLLOW` pair was presented as load-bearing while protecting only against a TOCTOU
race no static tree can kill, `RevFrozenBlobs.md` labelled `fa7ba113` the lane tip, and the merge
package's id remap is stale on the campaign side (already filed as L0 `ae2c52b8`). Attempt 1
froze both predicates, dispatched the 64-seat wave 1 and died without a report; attempt 2
inherited every artifact and finished the round.

Work: two NEW predicates were frozen before any corpus append at
`19e4ab3171c1540c40d6b12097745af98053b07d`: `PRED-C1-r35-v1`
(`TARGET_MET iff closed_entries=3 AND closed_rows=8 AND open_cites=0`) over the idle-lock
control surface, and `PRED-C2-r35-v1`
(`TARGET_MET iff uncovered=0 AND retired=1 AND toctou_declared=1 AND ledger_tip_ok=1`) over the
lane's own evidence ledger, with eleven committed control receipts and the re-issued
`ledger/RevFrozenBlobs-r35.md`. The data landed at
`02088b4dff0da153df30ff174611d1257c92d0cd`: three entries
(`corpus/knowledge/idle-lock-never-asked-r12.md`, `idle-lock-chain-armed-r14.md`,
`idle-lock-offered-in-the-bar-r15.md`) and eight registry rows S203–S210, adopted from
`shokuknow/merge/mado/` with ids re-pointed by document (package ids S315/S316/S327/S335/
S336/S337/S340/S342 → S203–S210 — the registration's own list of those ids is wrong and is
recorded as M35-1). Counters at `02088b4`: C1 `closed_entries=3 closed_rows=8 open_cites=0
verdict=TARGET_MET` exit 0; C2 `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1
verdict=TARGET_MET` exit 0; root census exit 0 with the same seven pre-existing `W04`
warnings; index gate 47/47 → 50/50; operability suite `MADO_SELFTEST: 460/460 assertions
passed`. Round shape: two v1 waves, 64 + 40 = 104 seats, one batched `task` call per wave.

Then wave 2 attacked the landed bytes and falsified more than it confirmed, which is the
round's main result:

- The C1 counter is **shape-scored**. `count.py:174` computes the receipt digest and never
  reads it, so a tree whose receipts are fabricated at the frozen paths still prints
  `TARGET_MET` (`w1/reports/CritVacuous.md`, `RevTarget.md`; wave-2 `CritVacuousRecheck`
  rebuilt it on the real tree with 87% of prose and 90% of receipt bytes changed, and
  `RevRowsDigest` reproduced five mutants on the live anchors). The real receipts do hash to
  their frozen values 8/8 — honest bytes, invisible to the counter. A one-line repair
  (`and digest == receipt["sha256"]`, on a scratch copy) keeps the real root and
  `controls/golden` at `TARGET_MET` and turns both committed cribs
  (`controls-content/c1-shape-only`, `controls-content/c1-fabricated-payload`) to
  `TARGET_MISSED`; it is a round-36 claim, because the predicate was frozen before data.
- The **C2 claim's substance is falsified**: `ledger_tip_ok` prints `TARGET_MET` on the very
  round-34 defect it claims to repair (stale `fa7ba113` label; `MutC2Real` M3a/M3c/M3d,
  `RevTipLedger` control C), `uncovered=0` is fail-open if a clause is deleted together with
  its control, covered-receipts are token greps, and the round-34 "real tip" is disputed
  (`dff3941` was master for 17 minutes; the last round-34-labelled commit is `6d754bd`; the
  blob ids verify at both). C2 stays `TARGET_MET` as written and is reported **not admitted**
  for operator ruling.
- Semantic falsifications **applied as append-only errata**, not rewrites: the "operator never
  toggled" inference is withdrawn (the journal shows the daemon's scope consumed at
  `2026-10-23T19:24:38` and restarted at `22:14:11`; zero `omarchy-toggle` lines is a null
  channel), the 150 s step is a screensaver with no lock call, the two start lines are two
  boots' first starts, "built not to remember" is replaced by the process-shaped mechanism
  with `autostart.conf` re-arming the daemon, and "never taken it" is withdrawn. The C1
  counter stayed `TARGET_MET` through every errata append — which is the point.
- Census gaps recorded, not repaired (fleet tool): alphabetic `recheck` prose validates
  clean (`MutCensusRow`, `RevValidate`), a blank `used-by` on a `mined` row is silent, and
  `used-by` is unchecked on non-mined rows. The id-collision guard fires on an indented row
  (spec pipeline `S203`; a seat's variant that dropped the id-extraction stage returned 0 and
  is corrected in the lesson), and the real 8 collisions are a genuine double allocation of
  S203–S210 between the lane and the merge package — campaign-side, unresolved.
- Misroot swept: seat `RevLogEvidence` wrote its report at the fleet root; copied byte-exact
  into the lane, `cmp`-verified, fleet copy deleted, recorded as M35-3.

Honest notes: the axis publication went stale for the ~15 minutes between the data commit and
this row (`mismatched=2`, navigation 47/47 vs 50/50, calibration 41/41 vs 41/43 — the
criterion citation needed its M-ids at section level), and this row republishes
`navigation 50/50; calibration 43/43; operability 12/12`. The pre-data `golden` control's rows
differ from the shipped registry in anchor/teaches cells, so the controls never exercise the
live bytes. `c1/clauses.json` names nine controlled live clauses, one `not-load-bearing`
(`o-nofollow-open`, TOCTOU-only) and one retired (`r34-word-bound-1-25`); wave-1
mutation-testing found `row-well-formed` and `entry-regular` verdict-dead on the frozen
controls, which round 36 must re-cut. SHONEN stays `[~]` on all four boxes; nothing was
self-promoted.

## Round 36 — the two admission counters are repaired and shown to discriminate; the lane's records pass a pointer gate (2026-10-25, attempt 1)

Motivation. Round 35 closed on the non-author spot-check
`corpus/lessons/round-35-verifier-spotcheck.md`: C1 re-measured `improved`, **C2
`unprovable` — "the round demonstrates the instrument is vacuous"**, and ten defects
routed (D1–D10). D3 (the C1 counter computes a receipt digest and never compares it
to the bytes) and D4 (the C2 counter scans its own clause list, greps receipts for a
token and substring-tests a prose document for a hardcoded tip) are the two the
operator's claim-sizing lesson names: *every declared claim must be one a do-nothing
control cannot reach and that your instrument cannot pass fail-open*. This round
takes exactly those two as its claims and closes all ten routed defects.

Claims, both frozen at `dbf8b579aeac0f023aaf595770f1cb0049e4baa2` before any round-36
data (`registration.md` under the round-36 wave directory): **C1 calibration** — the
two round-35 admission counters are repaired as standing tools and shown to
discriminate over a frozen 25-control manifest; **C2 operability** — the lane's own
records pass an evidence-pointer durability gate covering D2, D5, D8 and D10.

Work.

- **C1.** Two instruments: `quality/counters/c1-idle-lock.py` (`PRED-C1-r36-v1`) and
  `quality/counters/c2-ledger.py` (`PRED-C2-r36-v1`). The first binds the declared
  sha256 to the bytes actually read and reproduces the census's E12 `## Registry`
  fence; the second pins the live clause set in its frozen spec, requires each live
  load-bearing clause to name a control whose committed receipt records
  `observed=TARGET_MISSED` **and** names the clause, and parses the blob ledger's own
  table at a tip **computed** from git by one rule (the newest commit whose subject
  names `round-34` → `6d754bd`), with every tip-labelled token required to equal it.
  The falsifier is `quality/check-counter-discrimination.py`: 3 accept controls
  (the lane, a registry-shaped copy, the live ledger) and 22 reject controls (14
  `c1` cribs — the eleven round-35 skip cribs, the two committed content cribs, and
  two new fence cribs — plus 8 `c2` mutation fixtures generated from whichever ledger
  the profile names). Before, on the round-35 counters: **14/25**; after, on the
  repaired ones: **25/25**. Both degenerate instruments are excluded by construction
  (an always-accept fails the 22 rejects, an always-reject fails the 3 accepts).
- **C2.** `quality/check-evidence-pointers.py` (`PRED-PTR-r36-v1`) re-derives five
  observables from committed bytes. Before: `dangling_r35=2`, no correction pair, no
  scratch disposition, no tip transcript, no round-36 sections. After: all five at
  target.
- **D2** (uncommitted round work at round-35 closure) resolved: the eight modified
  seat reports and `scratch-evidence/RevEntryR12/evidence.txt` were rewritten from
  the branch (the round-35 evidence the spot-check examined), and the two untracked
  probe directories under `.ufo/waves/round-35/scratch/` were removed — their
  receipts are the evidence and the probes are regenerable.
- **D5** (dangling evidence pointers) closed by a correction pair, not by rewriting
  the round-35 record — the gate's `record_intact` clause refuses a record edit:
  - `.ufo/waves/round-35/scratch/SimplifyCounter/` -> `.ufo/waves/round-35/scratch-evidence/SimplifyCounter/`
  - `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` -> `.ufo/waves/round-35/scratch-evidence/MutC1Drop/`
- **D8** (the "no scratch tree left" claim against 124 tracked paths) closed by a
  named disposition, counted and re-derived: `corpus/lessons/round-36.md`
  § Scratch disposition, `tracked paths=124`.
- **D10** (no tip-revision axis transcript) closed by committing
  `quality/receipts/axis-a3094c99ab85bec35534de2447552c47dd2b647f.txt`, produced by
  `quality/check-axis-scores.py` at this round's data commit.
- **D9** (provenance-trio convention) recorded as a convention ruling in this
  round's lesson and applied to the round's own artifacts; the committed round-35
  entries are not rewritten (append-only).
- **D3/D4** are the claims; **D1/D6/D7** are report-side errata carried in the
  round-36 report (the round-35 tip hash, the corrected row-correction count and the
  per-revision seat counts).
- Frontier step: one new registry row, **S211** (negative controls in observational
  studies, tier A, opened 2026-10-25, receipt
  `.ufo/waves/round-36/fetch/S211.receipt.txt`), which grounds the reject half of
  the manifest. No knowledge entry and no other row; `Assimilation: none this
  round` as registered. Census 200 → 201 rows, exit 0 before and after with the same
  seven pre-existing `W04` warnings.
- Lesson and criteria: `corpus/lessons/round-36.md` with five mistakes (M36-1…M36-5)
  and the Gate block; `corpus/QUALITY.md` criteria 57–60 (clause attribution,
  document-table parsing with a bytes-bound digest, fixture-environment parity, and
  the domain-versus-meta ratio required in every report). Calibration's resolved
  criteria move 43/43 → 47/47, all four new ones grounded.
- **Domain-versus-meta.** The lane's last 30 commits at this round's start touched a
  domain-facing path (`tools/`, `corpus/knowledge/`, `PROVINCE.md`, `SKILL.md`) in
  **3** cases and records or instruments in **27**; the desktop plane has not moved
  since round 27's `tools/mado-wsrules.py`. Recorded as M36-5 and criterion 60 — this
  round is meta work too, and says so.

Round shape: two v1 waves under the frozen band; wave 1 dispatched 64 seats in one
batched call (reviewer 17, mutation-tester 13, scout 12, executor 5, scribe 5,
critic 5, sentinel 2, connector 2, simplifier 2, revenger 1). Evidence: the spec, the
validator's task-call payload and the 64 rendered seat prompts under the round-36
wave directory, and the seat reports under its `w1/reports/` subdirectory.


## Round 36 — correction (the D10 transcript path)

The D10 bullet in the round-36 entry above names a transcript file under
`quality/receipts/` after the data commit; that name was renamed before landing. The
green tip transcript is
`quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt`, produced at the
records commit (`MADO_AXIS: checked=3 mismatched=0`, `MADO_INDEX: indexed=50/50`), and
the red half — the axis gate at the data commit with the previous publication still in
force, `mismatched=1` — is
`quality/receipts/red-axis-publication-stale-at-data-commit.txt`. Nothing else in the
entry changes.

## Round 36 — the sixth mistake, carried by a wave seat

`corpus/lessons/round-36.md` M36-6 and `corpus/QUALITY.md` criterion 61 record a defect a
wave seat found: a command in the frozen registration could not run as written
(`quality/check-index.py --repo .` exits 2). The seat's verbatim run and the corrected
form are in `.ufo/waves/round-36/w1/reports/RevIndexGate.md`.

## Round 36 — correction (superseded transcript pointer, machine form)

The D10 bullet's transcript path is superseded, not cited; the machine-readable form the
pointer gate reads:

- `quality/receipts/axis-a3094c99ab85bec35534de2447552c47dd2b647f.txt` -> `quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt`

## Round 37 — event-socket delivery: what the compositor does to a stalled client, and why this host cannot see it (2026-10-25, attempt 2)

Motivation. Rounds 28–36 were self-audit: the last-30-commit ratio stood at 3 domain / 27 meta
(criterion 60), and the round-36 scorecard planned "move one domain-facing surface". The shokuknow
package `merge/mado/` held an unadmitted event-delivery entry on ground the lane held only as a
quoted line in lessons (`MAX_QUEUED_EVENTS` appears in no knowledge entry at `b4e47e9`). Attempt 1
(06:05–06:46 -03) left one empty directory and no file; nothing was inherited from it.

Claims (registration frozen v1 `8f0a9e3`, v2 `893a8aa` before any data): **C1 coverage** — two
entries on a new edge class under the held IPC contract; **C2 operability** — a read-only
event-socket subscriber census (capability acquisition).

Work.

- **Freeze discipline.** The L1 scored its own v1 controls with the cheapest-control rule and found
  its golden control was a token stub that met C1, and that C2's live clause trusted a hand-writable
  receipt; both counters were re-frozen as v2 before any seat ran (`receipts/controls-v2.txt`,
  13/13).
- **C1.** `corpus/knowledge/event-delivery-limits-r26.md` (package entry, every sentence re-checked
  against re-fetched bytes, five corrections) and `corpus/knowledge/event-queue-observability-r37.md`
  (lane-authored: on a default v0.56.2 host the core logger that writes both removal markers is off
  after start-up, so log and journal zeros are a null channel). Rows S212–S217. Two package entries
  refused (r28, r29). `admitted=0/2` → `2/2`.
- **C2.** `tools/mado-eventq.py` (wave-1 `ExecEventqA`, chosen over the independent `ExecEventqB`
  after both met 10/10 and an out-of-fixture probe): live, it lists `waybar` pid 935660 and `socat`
  pid 2293 on `.socket2.sock`, zero markers, `markers_observable=no`. `fixtures=0/10` → `10/10
  readonly=1 live=1`.
- **Mined mistake, fixed and shown able to fail (M37-4).** Four lane gates inherited `GIT_*`:
  under `GIT_WORK_TREE=/dev/shm` the round-36 pointer gate read `inherited_dirty=8` instead of 0;
  under `GIT_DIR` the axis gate read `mismatched=2`. Every git subprocess now runs with `GIT_*`
  removed; plain and ambient outputs are byte-identical (`receipts/git-env-green.txt`).
- **QUALITY 62** (a zero count needs a positive probe on the same channel) and **63** (worktree
  observables commit their witness).

### Round-36 errata (spot-check §5, append-only; the round-36 report lives in the fleet repo and is not edited)

- **R1.** `.ufo/waves/round-36/w1/reports/DistillerFindings.md` (19,033 B, a lane-authored seat
  report) was untracked at the round-36 close while the report said "working tree clean"; it is
  committed at `80b83c8`. The clean-tree sentence was false when written.
- **R2.** Round-36 report lines 196, 215, 231 (and 303, found by wave-1 `ScribeErrata`) name the
  after state `64979ef`; the receipts and the scorecard name
  `4d28b193e52f6cc8f04e81fda2664e018d62e209`, and the round closed at `a5aaa09`. The gate blobs are
  identical across `4d28b19..a5aaa09`, so the claim is unaffected.
- **R3.** "six criteria (57–61)" — five: `57.`–`60.` at `a3094c9`, `61.` at `520c631`.
- **R4.** The S211 receipt is 1,756 B at the tip, not 1,037 B (1,037 at `a3094c9`, 1,756 from
  `f77b554`, the identity note).
- **R5.** `inherited_dirty` is a worktree reading; routed to QUALITY criterion 63 (witness beside
  the receipt).

Evidence: `.ufo/waves/round-37/` (registration, receipts, fetch, controls, w1 and res reports),
`corpus/lessons/round-37.md`, SCORECARD `## Round 37`.

### Round 37 — residual-call corrections to the observability entry (after the data measurement)

Residual `CritEntryE2` F1/F3/F4 and `RevAfterC1`'s low finding: "717 lines over four service runs"
→ "717 lines … 4 start-up `Using config` lines" (the run count was not backed by S213); "the two
removal paths" → "the two removal markers" (a third, hangup, removal path logs at DEBUG); "never
writes to the journal" → "reaches the journal only through stdout before that point"; the refusal
pointer → the lesson's `### Assimilation` and M37-2. The C1 counter is re-run at the records tip
(`receipts/after-c1-v2-records.txt`); no OBS line's source or quote changed.

### Round 37 — late seat findings folded into the record (append-only)

- **R2 erratum widened** (wave-1 `RevR1R5`): the round-36 report names a wrong after-revision on
  seven lines — 6, 196, 215, 231, 303, 339, 381 — not the four listed above. No receipt ever named
  `64979ef` (at `64979ef` the receipts named `ea89bde`; from `fe55a90` on, `4d28b19`), and both
  gates changed between `64979ef` and `4d28b19`, so "the claim is unaffected" holds only against
  the `4d28b19` receipts. R5 is also wider: the pointer gate checks ten hard-coded round-35 paths
  (an untracked round-36 seat report still reads clean), and two of them no longer exist, which
  counts as clean.
- **C1 counter limits, additional** (M37-5): clause b is exercised by no control (`MutC1Clauses`,
  force-b survived), and the refused r28 package entry pasted in verbatim meets the target
  (`CritAxisClaim`). Both go to the round-38 v3 counter with the self-receipt crib.
- **r29 flip condition** (`ScoutPkgRefuse`): the journal needs both `debug:disable_logs = false`
  and `debug:enable_stdout_logs = true` (`Logger.cpp:47`); the lesson's assimilation table already
  says so, but the registration's flip names only the first.

## Round 38 — request-socket bound; M37-5 repairs (2026-10-25)

- Freeze `58e55ec`: registration, three v3/v1 counters, 19-control manifest, six opened-source
  receipts and the live eventq triplet committed before any round-38 data.
- Data `245065c`/`efb0ec2`: three adopted shokuknow package entries re-grounded —
  `hyprctl-flags-r28.md` (S221), `request-socket-live-bound-r8.md` (S158/S187/S258/S277),
  `request-limits-upstream-r31.md` (S253); three refusals stand (event-queue-host-measurement-r28, event-queue-journal-measurement-r29 - both null-channel - and socket-client-contract-measurements-r29, the 64 KiB-as-request-cap draft). Registry: 4 new rows, S158/S187 used-by extended.
- Counters MET at `b6c1d31`: C1 v3 admitted=2/2; C2 v3 fixtures=14/14 live=1; domain 3/3.
- Manifest/receipts fix `b6c1d31` (duprow in-table insert, docconn receipt-sha update).
- Wave 1: 35 attack seats dispatched (validated under ufo-wave-policy.json).

- **Errata (round 38, wave-1 `RevCommitChain`, F1–F3)**: the C1 v3 counter was patched
  post-freeze (`859d0cf`, clause-c uniqueness) and the discrimination manifest was
  patched post-data (`b6c1d31`, `c1-duprow` in-table insert). At the frozen pair
  (`58e55ec`) the gate scores 18/19 — `c1-duprow` observed `TARGET_MET` — so the C1
  claim **as frozen** fails its own instrument contract ("a later counter change is
  a new predicate and the claim fails as declared"). The landed pair measures 19/19
  as a *new predicate*; a re-registration ruling is routed to the non-author closure.
  C2's counter itself was not touched post-freeze; the manifest's `c2-docconn`
  control was repaired at the same commit (manifest is the shared instrument, so the
  frozen-manifest verdict is likewise 18/19, not 19/19).

- **Errata refinement (round 38, wave-1 `RevM37Routing`)** — re-running the frozen pair
  at `3f14bd2`/`ff81aaf` shows frozen C1 × frozen manifest = 18/19 (sole failure
  `c1-duprow`), but **frozen C1 × fixed manifest = 19/19**: the `859d0cf` counter
  patch was not load-bearing (clause j already enforced uniqueness at freeze). The
  claim's failure at the frozen pair is the manifest control `c1-duprow`'s
  out-of-table append alone; the re-registration ruling scope narrows to that
  control fix. Also: the v3 E2 lineage floor (2/3) rejects the round-37 honest
  proxies h2/h3 (`lineage=1/2`) — the accept path is calibrated to the landed
  vocabulary (landed entries pass E1 6/4, E2 2/2).

- **Round-38 C1 v3 residual refinement (`RevC1v3`)** — post-freeze, verdict-locked:
  F1 `norm()` lowercases before the uppercase-`S` strip, so the `"1024"` lineage
  phrase remains a one-token crib (dilutes the l-floor below the declared residual);
  F2 body-cited ids (provenance/INF lines) escape the per-id clauses — the honest
  pass depends on the narrow head[:15] mining window; F4 `RECHECK_RE` accepts `0d`.
  Clause fixes are routed to round 39; no further post-freeze counter patch is made
  beyond the declared `859d0cf` (the ruling scope stays as narrowed by `RevM37Routing`).

- **Round-38 freeze-verdict refinement (`RevCensusBefore`)** — direct replay at the
  freeze rev `58e55ec9` shows frozen instruments × frozen manifest = 19/19: the
  claim as frozen was internally coherent (its `c1-duprow` append landed outside
  `## Registry`). HEAD instruments × frozen manifest = 18/19 (duprow fails the
  tightened unique-row clause). The divergence between the two seat measurements is
  a bytes-at-which-rev difference; both are recorded and the re-registration ruling
  covers the manifest control rewrite.

- **Round-38 counter-clause hole (`LabratClockSkew`)** — `DATE_RE` (c1-r38:103,
  domain:100) is glyph-shape only: `2026-13-45`, `0000-00-00`, `2026-02-30` all
  pass, `k=1`, and a phony-date sandbox entry scores `TARGET_MET`; `RECHECK_RE`
  is a bare prefix test (`on-every-release` passes, `0d` passes). The frozen
  19-control manifest constrains the clause from above only. Fix routed to round
  39 with `RevC1v3` F1/F2/F4 (no further post-freeze counter patch).

- **Round-38 C2 control-coverage gaps (`MutC2`)** — six v3 clause mutants SURVIVE
  the frozen 19-control manifest: drop ss_sha256 consistency, drop full_table,
  accept tool_sha256 mismatch, drop the `connect(` test, drop tool-presence, drop
  the four fixture cases (M7/M7b), each scoring 19/19; the M4+M7 compound is
  caught only by `c2-missall`. The `full_table` clause is redundant as coded
  (replay_ok implies it). All routed to round 39 with `RevC2v3` F1/F2 — the
  manifest's reject-control set needs the killing fixtures, not the counter.

- **Round-38 C1 verification-gap (`MutC1`)** — all six single-point v3 clause
  mutants SURVIVE 19/19: the frozen verdict does not depend on c-uniqueness,
  quote-floor, d-pin-matching, a-new-at-base, g-OBS-id, or l-lineage (each
  reject is carried by another clause; verdict-level masking). Full kill table and
  clause diagnostics in `w1/reports/MutC1.md`; counter/manifest/claims untouched.
  Also flagged: the C1 run's /tmp cleanup of `mado38-dsc-*` may have touched a
  concurrent sibling's ephemeral gate scratch (recorded, no loss).

- **Round-38 residual-confirmation (`CritV3Residual`)** — the two declared
  fabrications remain cheapest-path: C1 ≈12 KB (3 copied pinned receipts + hollow
  entries), C2 ≈8.8 KB (behavior-exact stub + forged triplet, proc self-forge
  220 B). Classified as accepted tradeoffs matching the registration's declared
  residual; cheapest narrowing clauses proposed for r39 (located-quote depth;
  proc-holder/ss-users consistency + full-output replay equality).

- **Round-38 C2 residual confirmation (`LabratProcProof`)** — the live clause
  never re-derives /proc: `proc` is read from git (:194), "named" is an inode
  substring (:241), and only digest + inodes + AGREE are checked (:242-244).
  A 112-byte forged proc (honest receipt+snapshot kept) scores `TARGET_MET`; 15
  of 17 committed proc lines are deletable with the verdict unchanged; the
  docstring's three promised properties are unenforced. The committed artifact is
  truthful today — the defect is instrument reachability. Routed with
  `CritV3Residual` to r39 (proc-holder/ss-users consistency + full-output replay
  equality).

- **Round-38 freeze-verdict dispute (`RevFrozenClaims` vs `RevCensusBefore`)** —
  RevFrozenClaims's direct replay of the frozen `58e55ec` counter+manifest gives
  18/19 at BOTH the data rev and the freeze rev (`c1-duprow observed=TARGET_MET
  ok=0`; the frozen control appends outside `## Registry`, so the crib never
  bites), falsifying the recorded "frozen pair 19/19 at freeze rev" (added from
  RevCensusBefore at `3674cf28`). It infers the earlier 19/19 came from a mixed
  pairing. Both records stand; closure adjudicates the ruling basis.

- **Round-38 manifest integrity (`RevManifestIntegrity`)** — frozen 13/19 v2
  receipt reproduces line-identically at freeze rev; freeze-manifest duprow × v3
  = 18/19 independently confirms the errata. Control-design notes routed to r39:
  c1-selfreceipt's kill is placement (Leads/considerthese sections), not the
  anti-crib machinery; c1-r28-verbatim reads an absolute shokuknow path
  (non-hermetic).

- **Round-38 bases entry corrections (`ScoutS221`)** — F3 fixed: the `r` flag
  INF now matches the page's safer wording (reload runs after the reply is built,
  S158 `:2107`/`:2126`). F2/F4 routed to r39: server-side flags `j`/`r`/`a`/`c`
  are in S158 `:2068-2096` (`i` is CLI-only); the domain counter binds only the
  lesson Gate lines, not the SOURCES locator cell's sha/size/stamp.

- **Round-38 counter hygiene (`SimplifyV3`)** — deletions measured at 19/19 are
  NOT applied (frozen counters/manifest; clause names j/b are manifest-referenced;
  C7/C9 rejected: deriving tokens breaks the base precondition, deriving PINS from
  the Gate block admits fabricated ids). Two latent defects recorded for r39:
  `c2-r38-request-ground.py:198` crashes (TypeError int(list)) when a source line
  lacks verified-at; the eventq `why` detail's `agree` regex (`OVERALL:.AGREE`)
  differs from the scoring regex (`OVERALL:\s*AGREE`).

- **Round-38 freeze-pair resolution (`ScoutConsiderThese`)** — cross-pair replays
  settle the dispute: frozen counter × frozen manifest = 18/19; frozen counter ×
  landed manifest = 19/19; landed counter × frozen manifest = 18/19; landed pair =
  19/19. The `859d0cf` counter patch was a verdict no-op (clause j already
  enforced unique rows); the 19/19 belongs to the post-data manifest rewrite
  `b6c1d31` (c1-duprow moved inside `## Registry`). SCORECARD move-row wording
  corrected to say the repaired pair reaches 19/19. Also: the request-ground
  counter has no frozen manifest control (gate maps --c2 to the eventq counter
  only); its M37-5 crib classes reject correctly but have no committed replayable
  control set — routed to r39.

- **Round-38 package-audit (`ScoutPkgAudit`)** — the three refusals hold on
  re-derived grounds; two more gkeep entries repeat the same null-channel defect
  (r13/r14) and are refused by the same principle; the staged register's bulk
  append is refused (schema breaks, census flip); the adoptable
  `dispatcher-surface-and-request-grammar-r26.md` amendment and ~54 deferred rows
  go to round 39. Lesson ledger sentence corrected.

## Round 39 — the option-ownership table; the discrimination pair re-registered (2026-10-25, attempt 2)

- Attempt 1 (L1 `MadoR39`) froze `457d1b1` (registration, C1 manifest, base receipts,
  inherited round-38 seat reports) and dispatched v2 wave `w1` (64 seats), then ended with no
  data commit. Attempt 2 (L1 `MadoR39a2`) inherited the wave and integrated it.
- Motivating evidence: `considerthese/2026-10-24.md` proposal 4 (who owns each key, checked
  against `getoption`); the held ownership proof covered 6 keys
  (`knowledge/hyprctl-verification-layer.md` §5); `config-drift-r12.md` says the live layer does
  not establish all ownership. Seats SctHeldEntries and the L1 found the wave-built tool listed
  9 handler/rule rows as options on the host tree (M39-2).
- Freeze `d9b4e4a` (attempt 2, before data): C2 counter `PRED-C3-r39-v2` (generated trees seeded
  by the revision) and C3 counter `PRED-C4-r39-v1`, with controls; the attempt-1 C2 draft
  preserved as `c2/c3-r39-options.v1-draft.py.txt` (unreachable by construction, M39-1).
- C2 data `4ec582e`: `tools/mado-options.py` (handler/special-category boundary from S162/S173;
  selftest 71/71) → `fixtures=11/11 TARGET_MET`.
- C3 data `3783961` → `admitted=0/1` (clause g, S219 OBS line wrapped) → fix `3628472`
  (entry rewrap only) → `admitted=1/1 TARGET_MET`. Rows S218-S220 added; S018/S162/S173
  used-by extended.
- Assimilation: dispatcher-surface amendment appended to
  `knowledge/dispatcher-surface-and-request-grammar-r26.md` (S018, S196 re-opened,
  byte-identical); S220-as-Dispatchers refused (duplicate of S196).
- C1: re-frozen manifest 19/19 at freeze `457d1b1` and tip `3628472`; red-before 18/19.
- Records: lesson `corpus/lessons/round-39.md` (Gate, M39-1, M39-2), QUALITY criterion 64,
  SCORECARD round-39 section.
- Wave `w1`: 64 seats; 60 reports; no report from ExecAssimAppendBlock, ScrReportFrontier,
  MutC3Row (no output retained: the orchestrator's results file notes a kernel restart
  mid-wave), ScrReportMain left its draft without a report.

## Round 40

- Freeze `5e7e885` (v1 predicates), wave `w1` (64 seats) falsified them; v2 predicates, controls and receipts frozen at `8122293` before data.
- Data: `tools/mado-options.py --live`, entries `hyprctl-getoption-native-forms-r40.md` and `host-bar-producer-census-r40.md`, rows S278-S282, lesson `corpus/lessons/round-40.md`, QUALITY 65-68.
- Host finding: gradient angle inheritance (`ffe68e0d 45deg`); a fifth native form `vec2`; hostile config key `x/--batch` reaches the compositor's batch path unless allowlisted.
- Errata: round-39 lesson's S224 "fabrication class" label is `unverifiable` (rotated volatile value).


## Round 41 - mado-globals and the focus-grab entry (2026-10-25, attempt 1)

- Freeze `60c3914` (v1 registration, counters, controls, source receipts) -> wave `w1` (34 seats) falsified the v1 predicates before any data (C1: 8 of 12 cheats TARGET_MET - live-stub bytes readable without running it, a plaintext journal copy on disk, b2 path/fingerprint escapes, clause-g `getattr`/kwargs, a child interpreter, `\w` names; 13 of 42 extra mutants survived; a FIFO journal hung; C2: 9 of 9 forgeries admitted, 29 of 45 mutants survived) -> v2 predicates, 98 + 67 controls, reference and receipts frozen at `294c667` before data.
- Data `07f2641`: `tools/mado-globals.py`, entry `corpus/knowledge/hyprland-focus-grab-r41.md`, rows S283-S289 (+ S037 used-by), README row, lesson, fetch receipt `xdph-installed-version.txt`. Measured: C1 v2 39/39, C2 v2 1/1 (v1: C1 6/24, C2 1/1).
- Wave `w2` (34 seats, falsify) attacked the data and the v2 predicates: data defects fixed in `6fd2234` (request count six not five/four, README row missing its Sources cell, S286 ten branches, a 63-global session reported as whole, the first session belongs to the previous boot, 20 overstated sentences, a quickshell `add_surface` deferral); predicate defects reported open (SCORECARD Round 41).
- Assimilation (focus theme, `merge/mado/`): id guard reg 219 / staged 147 / collisions 27, proved on an indented row; one admit and two refusals, outside spot-check agreed on all three (`w2/RevAssimGate`); considerthese 2026-10-25 proposal 5 -> QUALITY 76 (the reflection's "eight entries" is nine).
- Records: QUALITY 69-76, SKILL.md probe/decision rows and subsection 'Advertised Wayland globals', PROVINCE.md tool row, lesson M41-1..20.
- Wave facts: the orchestrator's kernel restart dropped the w1 seat outputs from `w1-results.json` (reports are on disk); `ConnSiblingOverlap` left no report.

## Round 42, attempt 1 - honest stop: frozen, wave 1 planned and never dispatched (2026-10-25)

- Freeze `809dc2caef09d9cbf15a496e55a1b208803a3561` (registration, counters `quality/counters/c1-r42-geometry.py` and `c2-r42-gkeep-entry.py`, controls, reference tool, pre-wave receipts) and wave spec/dispatch `17b395658187cb408fa301bb22e6d7bf6ed9a93a` (36 seats; the validator accepted it: executor 13, scribe 7, scout 3, connector 3, reviewer 3, critic 3, mutation-tester 2, simplifier 1, sentinel 1). The orchestrator ended the run before dispatch (dispatcher cap 0), so no seat ran, no data landed: `tools/mado-geometry.py`, `corpus/knowledge/hyprland-gkeep-geometry-r42.md`, rows S290-S299 and `corpus/lessons/round-42.md` do not exist.
- Controls found and closed defects before the freeze: C1 controls first hung 30 min on a stdin-echo control (timeout breaker added), three equivalent mutants (M03, M20, M38; the dead `#` contract clause was deleted) and one missed mutant (M26, now killed by a `badjson0` input); C2 control P first failed on quotes under 3 words, a held-id line without a locator and a mutant editing a directory component (F6). Receipts: `.ufo/waves/round-42/receipts/ctl-c1.txt` (46 controls, 0 reach TARGET_MET besides the reference), `ctl-c2.txt` (74/74).
- Before-measurements at base `62dd798`: C1 `fixtures=0/37 tool=absent TARGET_MISSED`, C2 `admitted=0/1 TARGET_MISSED`; census start and end identical (`mado ok`, exit 0).
- Two untracked round-41 seat scratch files (`.ufo/waves/round-41/w2/ExecDiffFuzzV2/scratch/s-grow`, `s-size`) were deleted at round start (spot-check 41 §6.1).
- Facts opened this round from the pinned v0.56.2 sources (not yet registry rows or entries): the rule match engine is `re2::RE2::FullMatch` (anchored, `negative:` prefix); `static_.size` is an expression consumed in the floating branch; `hyprctl clients -j` `size` is `w->size(GEOMETRIC_GOAL)` - the animation goal, not the current value (`Hyprland-HyprCtl.cpp:394-395,412-413`).

## Round 43, attempt 1 - the gkeep geometry round re-run: C1 operability (tools/mado-geometry.py) and C2 coverage (hyprland-gkeep-geometry-r43.md) (2026-10-26)

- Locator correction for the Round 42 entry above (closure `corpus/lessons/round-42-verifier-spotcheck.md` §6.2; the Round 42 text is left as written): `w->size(GEOMETRIC_GOAL)` is at `Hyprland-HyprCtl.cpp:427-428` (the `clients -j` object) and `:448` (the second formatter), not `:394-395,412-413`; the `negative:` prefix is at `Hyprland-RegexMatchEngine.cpp:7-8` and `RE2::FullMatch` at `:16`, not `:10-16`. Computed with `grep -n 'GEOMETRIC_GOAL' .ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp` and `grep -n 'negative\|FullMatch' .ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp` (the round-43 pins are byte-identical to the round-42 ones, `receipts/fetch-sha256.txt`).
- Freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`: registration `.ufo/waves/round-43/registration.md`; C1 re-registered unchanged (`PRED-C1-r42`, counter frozen at `809dc2c`), C2 with round constants only (`quality/counters/c2-r43-gkeep-entry.py`, `PRED-C2-r43`); pins re-fetched 2026-10-26 (seven Hyprland files byte-identical to round 42; `host-clients-r43.json` re-captured; `gkeep-ui-excerpt.py` regenerated with `sed -n '446,$p'` because the round-42 excerpt's header claimed lines 446-495 of a 488-line file and carried one extra blank line). Controls at the round-43 base: `CTL_C1 controls=46` (REF and BASE-absent are anchors; `0 of 47` non-reference runs reach MET), `CTL_C2 controls=74 correct=74/74`. Before: C1 `fixtures=0/37 tool=absent TARGET_MISSED`, C2 `admitted=0/1 TARGET_MISSED`; census `mado ok` exit 0; axes `MADO_AXIS checked=3 mismatched=0`.
- Wave `w1` spec/dispatch `5add5b45a65ddaa18fad00c6afa9dbfda29ee0b0`: 38 seats (executor 14, scribe 7, critic 4, scout 3, connector 3, reviewer 3, mutation-tester 2, simplifier 1, sentinel 1); the registration's planned 37 became 38 after the spec builder showed the attack share at 9/37 (24 %), so one critic (`CritClaimSizing`) was added before the handoff; the frozen registration text was not edited.
- SHONEN box 2 receipt (closure §6.4): `.ufo/waves/round-43/receipts/live-geometry-host.txt` - the tool on the live host, `verdict=NO_MATCHING_CLIENT`, exit 3, 4 clients, no gkeep window.
- Wave `w1` findings that changed the round before data: `CritClaimSizing` (C2 v1 target met by a 17-line entry citing four of ten pins) and `CritC2Cheat` (16 admitted forgeries, 8 closed by string-local tightenings) -> C2 re-registered as `PRED-C2-r43-v2` at `496340dd53fabd800be42e8fb19090f35e2c235c` before any data (`registration-v2.md`; the 74 controls still 74/74 under v2; the w1 forgery harness re-pointed at v2 rejects B1, B2, C1, C2, E1, F1, F2, G1, G2, X2, X3 and still admits the claim-binding family A1, A2, D1, E2, H1, X1). C1 kept as registered: its w1 cheats that reach MET (source-pin selftest, sandbox detection) all carry the full model, and the verbatim-copy finding is the provenance of the deliverable (the round-42 reference), stated in the report.
- Data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`: `tools/mado-geometry.py` (byte-identical to `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`); `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (ten cited ids: new S290-S297 and held S155/S158, whose receipts are the pinned bytes; the drafts' S291/S296 rows were dropped because the commit-form URLs already belong to S155/S158); lesson `corpus/lessons/round-43.md`; README index row and Frontier bullet; PROVINCE.md tool row; SKILL.md decision row, probe row and subsection; QUALITY 77-81; `quality/check-locators.py` (from seat `ExecLocatorGate`). Measured there: C1 `fixtures=37/37 tool=present verdict=TARGET_MET` exit 0; C2 v2 `admitted=1/1 verdict=TARGET_MET` exit 0 (v1 also 1/1); census `mado ok` exit 0 (same W04 x7 + W01 S277 as at base).
- The isolated-oracle observation (`w1/ExecOracleGkeep/`): a Hyprland 0.56.2 nested in the round-27 bubblewrap oracle reported `"size": [420, 500]`, `"floating": true` for app id `org.omarchy.gkeep` under the host's three rules; controls without the size line (200x200, the client's buffer), with `size 300 300` (300x300) and without `float on` (tiled). Reported in the entry as an oracle fact, not a host-session fact.
- The new locator checker caught the L1's own first draft (single-line locators for four quotes that span two receipt lines; M43-7) and one wrong SKILL.md locator (`Hyprland-WindowRuleApplicator.cpp:426` for `SExpressionVec2`, now `:422,426`); the entry and SKILL.md read `locators=15 miss=0`.
- Wave `w2` (32 seats) dispatched after w1's WAVE-DONE (w1: 38 of 38 seats reported, 0 dead). Corrections from its findings, landed after the data commit: the entry's tiled-path INF was false (`Window.cpp:2402-2408` stores the rule's size as a tiled target's pseudo size; `w2/CritEntryInf.md` F1) and "first map only" was wrong in the once-per-window sense (F2); RE2-dot, `negative:` locator, "geometry read verb", census wording, the `setBox` link (`Hyprland-GeometricMovableAnimated.cpp:45`) and the oracle sentence's scope (adapted harness, shm stand-in client) were tightened; the `gkeep-element-rules-r30.md` refusal was withdrawn because its flip had fired (`apps/system.conf:4`); SKILL.md's TILED row, support ceiling and backtracking guard and PROVINCE.md's `--selftest` sentence were corrected. Registry rows keep their landed cells (CORPUS rule 2); their wording defects are recorded in `corpus/lessons/round-43.md` for supersession. The C2 v2 counter stays `admitted=1/1` on the corrected bytes.

## Round 44 (2026-10-26, hyaku run 9, attempt 1)

- Protocol load; round-43 closure (`corpus/lessons/round-43-verifier-spotcheck.md` §6 D1-D7) routed into `corpus/lessons/round-44.md` (Mistakes M44-1..7, Round-43 errata E1-E4); census before `receipts/census-before.txt` exit 0.
- Freeze v1 `e2289516a9a857f55cda7be635933e89b931c3da`: registration, `PRED-C1-r44` (fullscreen/maximized state verdicts for `tools/mado-geometry.py`, grounded in `fetch-c1/` Hyprland FullscreenController/FullscreenHandler/HyprCtl at efb5099), `PRED-C2-r44` (gkeep size-request entry), pins `fetch/` (Window.cpp, XDGShell.cpp, xdg-shell.xml 1.49, gdktoplevel-wayland.c 4.24.1, gkeep ui.py 133b867), controls (C1 0 of 15 met, C2 0 of 3), assimilation id guard (collisions 42; guard proof fires on an indented row) and quarantine slice (13 rows).
- Wave `w1` (38 seats, spec `ae996fcf5e50d2d882dcf543a4ab2df5604dada2`): independent implementations met C1 (`w1/ExecIndepA.md`, `ExecIndepB.md`); cheats met C1 v1 (`w1/CritC1Cheat.md`: sandbox gate, padded selftest); 9 of 9 forgeries met C2 v1 (`w1/CritC2Cheat.md`), plus a re-pointed r12 (`w1/CritClaimSizing.md` F1) and a hidden census-prefix line (`w1/RevC2Counter.md` F2); the "false report" premise was withdrawn (`w1/CritFsPremise.md`).
- Freeze v2 `03fa5c618b089064a657b3d79d3d4272ae4b6894` before any data: `PRED-C1-r44-v2` (NOT_COMPARED exit 5, b5 state-blind teeth, e environment invariance; controls 0 of 20 met, `receipts/ctl-c1-v2.txt`) and `PRED-C2-r44-v2` (T1-T4, exact census exemption, surface clause j; positive control admitted, 10 of 10 do-nothing/forged rejected, `receipts/ctl-c2-v2.txt`).
- Data: `tools/mado-geometry.py` = `c1/ctl-ref-tool-v2.py.txt` (selftest 94/94); entry `corpus/knowledge/hyprland-gkeep-size-request-r44.md`; rows S298-S301 and S164 used-by; lesson round 44; README index row and Frontier "Round-44 gkeep size-request route"; SKILL.md FULLSCREEN/MAXIMIZED/NOT_COMPARED rows, exit-map note and the D3 TILED correction (appended); PROVINCE tool-row note; QUALITY 82-84; `quality/ratio-domain-meta.py` (considerthese 2026-10-25 proposal 1); live host run `receipts/live-geometry-host-r44.txt` (NO_MATCHING_CLIENT, exit 3).


## Round 45 (2026-10-26, hyaku run 9, attempt 1)

- Protocol load; census before `receipts/census-before.txt` exit 0; base `0c89478a`.
- Freeze v1 `22a8dedd`: PRED-C1-r45 (new tool `tools/mado-monitors.py`, reference `l1-draft/`, 49 seeded fixtures, controls 0 of 16 met), PRED-C2-r45 (entry on the monitor-rule chain, nine pins fetched and opened 2026-10-26, controls P admitted, 9 rejected).
- Wave `w1` (41 seats, spec `ebdba13f`; executor 13, scribe 7, critic 6, reviewer 4, scout 3, connector 3, mutation-tester 2, sentinel 1, simplifier 1, revenger 1; 0 dead, all 41 reports): independent rebuilds met C1 (`w1/ExecIndepA.md`, `ExecIndepB.md`); 11 cheats and 5 do-nothing controls met C1 v1 (`w1/CritC1Cheat.md`, `w1/ExecDoNothingC1.md`); 9 forgeries met C2 v1 (`w1/CritC2Forgery.md`); six contract errors against Hyprland (`w1/CritToolSemantics.md`, `w1/ExecParseOracle.md`, `w1/RevTool.md`, `w1/CritEntryContent.md`); one critic finding refuted (float32 integrality; `w1/ExecScaleOracle.md` 0 divergences).
- Freeze v2 `7c0b0035` before data: PRED-C1-r45-v2 (81 fixtures x 3 environments/seeds, bubblewrap isolation, 150 nonce-generated cases against the pinned v2 reference), PRED-C2-r45-v2 (T1-T5, 14 pins, 24 surfaces); controls `receipts/ctl-c1-v2.txt`, `receipts/ctl-c2-v2.txt`.
- Data `ee6659b9`: tool, entry, rows S302-S315, lesson, README row + Frontier, SKILL/PROVINCE rows, QUALITY 85-86, `quality/check-session-material.py`, round-44 D1 projections. Measured: C1 `fixtures=81/81 generated=150/150 ... TARGET_MET`, C2 `admitted=1/1 TARGET_MET`; census `mado ok` exit 0 (W04 S303, S307 added); live host run DP-1 AGREE, OK.
- Not run: wave `w2` (falsification of the data) - the run's request budget ended the round after w1 (round total 41 seats, below the 64 floor; reported as a conformance defect).

## Round 46 (2026-10-26, hyaku run 9, attempt 1)

- Protocol load; census before `receipts/census-before.txt` exit 0; base `b22ea56b`.
- Freeze v1 `8c5434c6`: PRED-C1-r46 (new tool `tools/mado-devices.py`, reference `l1-draft/`, 90 fixtures, controls 0 of 23), PRED-C2-r46 (input-device entry, ten pins fetched and opened 2026-10-26, controls P admitted, 14 rejected after a harness fix).
- Wave `w1` (one v2 wave, 66 seats, spec `e0be61e4`; executor 18, critic 15, scribe 9, reviewer 6, connector 5, mutation-tester 4, scout 4, sentinel 3, simplifier 1, revenger 1; 66 reports, 0 dead): two independent rebuilds met C1 v1; a hyprlang-library oracle, a strtof oracle and source critics found the v1 contract wrong on seven forms; cheats and a delegator met C1 v1; six forgeries met C2 v1; 11 seats ran the round-45 w2 (round-45 closure D1).
- Freeze v2 `2bcc335f` before data (allowlist sandbox, 110 fixtures, clause k for C2); C2 v2 controls PASS 0 of 22; C1 v2 controls FAIL 2 of 40 (pipe tripwire) -> freeze v3 `7f793280` (socket tripwire), controls PASS 0 of 40 (`receipts/ctl-c1-v3.txt`, commit `fb6a1fee`).
- Data `1001bda0`: tool, entry, rows S316-S325, lesson, README row + Frontier, SKILL section + `mado-session-material` registry row, PROVINCE refinement, QUALITY 87-90, live receipt. Measured: C1 `fixtures=110/110 generated=150/150 ... TARGET_MET`, C2 `admitted=1/1 TARGET_MET`; census exit 0; session-material gate `findings=115` exit 1 (18 in round-46 seat files, all synthetic gate fixtures; marker not yet installed).
- Re-verification (freshness): the ten pins re-fetched byte-identical on 2026-10-26 (`w1/ScoutRecheck.md`); upstream main moved to a Lua config (no `src/config/legacy/`).

## Round 47 (2026-10-26, hyaku run 9, attempt 1)

- Protocol load; census before `receipts/census-before.txt` exit 0; base `60edb66e`. Claims declared `c24adef2`; w1 build wave (41 seats, policy v1) dispatched.
- L1 reference `l1-draft/mado-terminal.py` written from the v0.14.3 script; 3000 + 8000 random cases and 140 w1 fixtures agree with the real script (`receipts/l1-fuzz-8000.txt`). Freeze v1 `d7527d60`: PRED-C1-r47 (real script as judge in bwrap, strace tripwire, 190 fixtures, explain clause), PRED-C2-r47 (w1 ExecCounterC2 draft with clause f decoupled from C1). Controls: C1 PASS 0 of 28 (`receipts/ctl-c1.txt`), C2 PASS (`receipts/ctl-c2/`).
- w2 falsify wave (44 seats, policy v1): contract errors H1 (`-type f` binds to the first application dir only) and H2 (`command -v -p`) found outside the fixtures (`w2/ExecC1Diff.md`); fixed in the landed tool (`receipts/h12-check.txt`), fixture gap routed (M47-10). Counter wording/robustness findings `w2/SentC1Sandbox.md` F1-F4, explain residual `w2/CritC1Explain.md`, undeclared C2 forgeries F4/F7/F8 `w2/CritC2Forgery.md` routed.
- Data `0c699605`: tool, entry, rows S326-S339, lesson, QUALITY 91-95, README row + Frontier, SKILL section, R1 erratum, live receipts. Measured: C1 `fixtures=190/190 explained=190/190 generated=150/150 ... TARGET_MET`, C2 `admitted=1/1 TARGET_MET`.
- Re-verification (freshness): host resolver byte-equal to the v0.14.3 tag; omarchy v3.8.3 list and override byte-equal to the host files; the round-17 `[UNK]` selection half answered by a cold-cache capture (`receipts/live-terminal-host-r47.txt`).
- Routed defects: R2 file removed (`receipts/r2-removed.txt`); R3 and R4b routed again.

## Round 48 (2026-10-26/27, hyaku run 9, attempts 1-4)

- Protocol load; census before `receipts/census-before.txt` exit 0; base `579f694b`. Claims declared `5ff16742`; w1 build wave (41 seats, policy v1).
- Freeze v1 `3e6c848a` (PRED-C1-r48 warm-cache counter, 204 warm fixtures; PRED-C2-r48 XKB entry counter; XKB pins and host receipt). w2 falsify wave (48 seats, policy v1; 47 reports, `CritCounterTiming` hung): a cache write, a fork and six more candidates met C1 v1, a mode-755 pin and a 600-character quote met C2 v1.
- Re-registration v2 `02165600` before data: write/fork tripwire, 24 new warm fixtures (228), `--observed` foreign-root capture, pin mode, quote length, pinned replay judge; 66 C1 control candidates all `TARGET_MISSED` (`receipts/v2/ctl-c1v2.txt`).
- Attempt 3's L1 died in the orchestrator session exit; salvage `cf3deeec`. Attempt 4 re-verified it (frozen bytes unchanged, both predicates v1+v2 `TARGET_MET` on a scratch mirror, `receipts/a4/pre-*.txt`) and corrected two transcribed facts in the lesson (M48-11).
- Data `e5d0130d`: entry, lesson, QUALITY 96/99 instruments. Measured: C1 `warm=228/228 explained=418/418 ... TARGET_MET`, C2 `admitted=1/1 TARGET_MET` (`receipts/c1-after-data.txt`, `c2-after-data.txt`).
- Re-verification (freshness): the operator's resolver cache, overwritten by a w2 mutant at 22:26 (M48-10), was rewritten by a resolver run at 23:59:27 (metadata only read).
- Residual `a4r1` (8 reviewer/critic seats, attempt 4) against the committed data: 4 reports, no blocker (`a4r1/MadoA4RevC1v2Diff.md`, `MadoA4CritEntry.md`, `MadoA4CritSalvage.md`, `MadoA4CritAdmission.md`); one lesson locator fixed; 4 seats lost to the 1 MiB file cap colliding with the clone recipe (M48-13). Harm watch: round-47 counters at `d8e3d600` (C2 MET; C1 MET 3 of 4, one bwrap-noise flake, M48-12); do-nothing controls all miss (`receipts/a4/ctl-do-nothing.txt`).

## Round 49 (2026-10-27, hyaku run 9, attempt 1)

- Protocol load; census before `.ufo/waves/round-49/receipts/census-before.txt` exit 0; base `03e4ae76`; operator-owned digest before `receipts/operator-state-before.txt`. Claims `5f37c1b8`; w1 build wave (45 seats, policy v1).
- Freeze `dd2e827e`: registration, C1/C2 counters (w1 drafts + L1 isolation, generator and clause-j edits), 633 fixtures, w1 evidence, pins, candidates; the 47 round-48 sidecars committed (N1, M48-8).
- C1 data `430d2569`: `tools/mado-keysym.py`. Measured `fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` at nonces 4949 and 31337 (`receipts/c1-after-data*.txt`); base `fixtures=0/633 ... TARGET_MISSED` (`receipts/c1-base.txt`).
- C2: candidate entry does not meet `PRED-C2-r49`; no data commit; rows S352-S363 drafted, not appended (honest stop).
- Re-verification (freshness): operator cache `~/.cache/xdg-terminal-exec` digest unchanged across the round (`receipts/operator-state-after.txt`); census after identical, exit 0.
- Wave w2 not dispatched: the L1's request budget ended the round (M49-4). Lesson `corpus/lessons/round-49.md`.
## Round 50 (2026-10-27, hyaku run 10, attempt 2)

- Attempt 1: claims `13631f24`, w1 54-seat build wave dispatched; run-9 wrap-up interrupted L1 after all 54 seat reports
  landed, with null outputs in `w1-results.json`. Attempt 2 integrated from committed seat reports; no claim/counter changes.
- Freeze `470bfd77`; data `906178b6`; w2 falsify wave 32 seats; final integration `c12b588e`. Round total 86 seats.
- C1/C2 frozen predicates return TARGET_MET on their claimed data, with controls MISS; w2 found C1's recycled candidate
  bypass and omitted held ground facts, and C2's canned selftest/all-rule-tag gate bypass. Both claims are honest stops;
  predicates were not re-frozen.
- Lane lesson M50-1..9. Full w2 results `.ufo/waves/round-50/w2-results.json`; w2 seat evidence in `.ufo/waves/round-50/w2/`.
- `quality/check-wave-done.py --repo . --rev <tip> --round 50` → waves=2 settled=2 verdict=OK; index 66/66, exit 0.
- Operator resolver cache digest changed between before/after reads; hypr config files unchanged (`receipts/operator-state-*.txt`).

## Round 51 (2026-10-27, hyaku run 10, attempt 1)

- Protocol/mission/axes/corpus/learning and lane state loaded; base `6ca8c559`. Start census `.ufo/waves/round-51/receipts/census-before.txt`: 300 registry rows, exit 0 (pre-existing W04 warnings). Removed inherited untracked `.ufo/wakes` (388 B stale index-check scratch note; round-50 spot-check D3); no `lane-dead-no-report mado round=51` line at launch.
- Claims freeze `d2740281`: C1 operability/capability = tracked tool ledger; C2 coverage/sourced = dispatcher-execution entry. W1 policy-v1 build/attack wave: 43 seats; all 43 settled, no dead seats. L1 held the canonical planner role per the validator ruling.
- Freeze/integration commit `56026fcb`: ledger checker + counter, ledger, registration, pins and w1 evidence. C1 base at `6ca8c559`: `ledger=absent population=79 TARGET_MISSED`, exit 1; at `56026fcb`: 82/82 ledger rows, all miss fields 0, selftest 50/50, `TARGET_MET`, exit 0. Current C1 integration receipt later re-runs at `485bdfd`.
- C2 data `a0e34387`: dispatcher entry, rows S364-S369, README index, lesson/QUALITY 103. Base `6ca8c559`: absent / `admitted=0/1 TARGET_MISSED`, exit 1; initial data `a0e34387`: 4/4 `TARGET_MET`, exit 0. W1 counter fit: 66 base knowledge files + 3 candidate files, max shingle overlap 0.1%, six new row/pin bindings, 7/3 held citations.
- W2 policy-v1 falsification wave: 33 seats, role mix reviewer 12 / critic 9 / mutation-tester 7 / sentinel 2 / connector 2 / scout 1; all 33 settled, no dead seats. Round total 76. C1's frozen literal predicate passes, but a ledger-wide self-pointer and repeated generic descriptions reach TARGET_MET; report as a disclosed limit, not meaningful-accountability proof. C2's frozen predicate passes, but generic held token `[the]` is a counterexample to semantic evidence, and the original entry contains source-truth overclaims (`w2/RevC2EntryTruth/entry-truth.md`).
- C2 errata `b742d54c`: append-only correction narrows/withdraws the unsupported bind-tail/comma claim, runtime-vs-config-time error, special-dispatcher count, mouse serialization explanation, unconditional socket marker/submap claims, and running-host manager inference. QUALITY 104 and M51-2 record the source-truth miss. The unchanged C2 counter remains 4/4 `TARGET_MET` at corrected revision `b742d54c` and final data integration `485bdfd`; semantic sufficiency and independent review remain unproven.
- Final integration check at `485bdfd`: C1 and C2 both TARGET_MET; index 67/67, exit 0; `quality/check-wave-done.py --round 51` → waves=2 settled=2 verdict=OK, exit 0 (`receipts/wave-done-final.txt`). End census `receipts/census-after-final.txt`: 306 rows, exit 0; six tier-A rows opened 2026-10-27; no held-row status/recheck/used-by changes. Frontier advances one row: dispatcher execution. Assimilation none; `considerthese/2026-10-26.md` proposal 2 partially informs C1, but last-live-run freshness remains open; 13 absent-defect rows remain unverifiable and unadopted.
- M51-1 mines round-50 D1 (stale one-wave receipt vs later two-wave report claim); QUALITY 103 requires a final integration receipt. M51-2 mines C2 source-truth overreach; QUALITY 104 requires sentence-to-pin scope auditing. Both fixes are recorded; C2 errata passed the frozen counter, but no outside reviewer verified the corrected prose. W2 residuals and exact receipts are under `.ufo/waves/round-51/`.
- `PROVINCE.md` adds the lane-level ledger/checker boundary; `SCORECARD.md` records both bounded moves, commands, deltas, capability and next-round carry. SHONEN remains four historical `[~]` assertions; no outside-lane verifier was performed. Tool installs/upgrades: none.

### Round 51 commit map

- `d2740281` claims freeze + census-before receipt; `.ufo/wakes` removed.
- `3ac31642` w1 spec/dispatch evidence; `56026fcb` w1 results, counter freeze, checker, tool ledger and pin directory.
- `a0e34387` C2 entry, S364-S369 registry rows, README coverage row/frontier, initial lesson and QUALITY 103.
- `6366c314` w2 spec/dispatch; `caf52271` w2 launch marker; `485bdfd4` w2 reports/results, QUALITY 104 and source-truth record.
- `b742d54c` append-only C2 entry errata; `2b1e337a` final C1/C2, index, census and WAVE-DONE receipts.
- `22ab80bc`, `f2a612ae`, `ad578633`, `58f4d4fc`, `ed84051d` carry the staged SCORECARD, claim receipts, lesson measurement, PROVINCE inventory, and final LOG/SCORECARD/lesson/QUALITY records respectively. Final scorecard and lesson cite their measured revisions and all known w2 residuals.

### Round 51 evidence correction (M51-3)

W1's held-token attack claim (`tokens=[the]`) was **not reproduced**: W2 ran the exact syntax and got `no_tokens`; `keys=the` also missed because one cited base line lacks that token (`w2/CritC2HeldTokens/held-token-attack.md:9-15`). The earlier W1 wording in the round summary that called this a counterexample is superseded by this correction. No generic-held-token bypass is demonstrated; QUALITY 105 records the exact-fixture requirement. The broad token-specificity question remains an untested design concern, not a measured defect.

## Round 52 (2026-10-27, hyaku run 10, attempt 1) — honest stop

- Base `85d57a818c3707397e21c840b6498b105ba798aa`; frozen claims `.ufo/waves/round-52/claims-frozen.md`; waves w1 68 + w2 32 = 100 seats, all settled. Role mixes and full results are in `.ufo/waves/round-52/{w1,w2}-results.json`.
- C1 operability: **unprovable / honest stop**. The W1 draft produces green/red receipts, but W2 Attack01 demonstrates its lexical context check accepts forged descriptions (up to 82/82) and Attack02 shows self-pointer laundering spellings. The committed implementation was intentionally not landed; no final-tip C1 counter or claim measurement exists. The r51 counter at base was recorded as 82/82 TARGET_MET but does not address the proposed contextual predicate.
- C2 coverage: **unprovable / honest stop**. W1 source drafts are not an admission measurement. W2 Attack07 confirms the simplified landing counter cannot parse the candidate entry, fabricated quote cells pass its structural binding, and the W1 draft counter also fails against the landed proposition map. No final-tip counter/entry measurement exists; do not claim expansion admission.
- Opened and registered S370-S373 in round 52, with quote/source evidence in the new knowledge entry and `.ufo/waves/round-52/fetch/`; three reused URLs received W04 duplicate-scope warnings, requiring explicit QUALITY 17 distinct-scope review. Census after is `mado ok`, exit 0; rows 306→310. No existing source status/recheck/used-by changes.
- Mined M52-1: source-truth claim map can be mechanically present while propositions exceed quote entailment (W2 Attack07 P16-P18); QUALITY 104 is relevant, and the outside review is recorded in `.ufo/waves/round-52/w2/Attack07.md`. The C1 forged-context attack also shows lexical overlap is not semantic accountability.
- Assimilation: none. `considerthese/2026-10-26.md` proposal 2 remains only partially covered by static inventory; last-live-run freshness is not claimed. No installs.
## Round 53 (2026-10-27, hyaku run 10, attempt 1) — honest stop

- Base `ad4bf2059bcfafe63671d262222908ee1fe8001c`; start census command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, 310 rows, exit 0 (existing W04/W01 warnings). Frozen claims `.ufo/waves/round-53/claims-frozen.md`; no `registration.md`, frozen control manifest, or fixture set existed before wave data (`w1/R53Five41.md:52`).
- One v2 build+attack wave `w1`: 64 seats, all 64 reports/outputs settled, 0 null outputs, 0 dead, 0 replacement; role mix executor 8, connector/critic/mutation-tester/revenger/reviewer/scout/scribe/simplifier 7 each. Planner held by L1; attack roles reviewer+critic+mutation-tester = 21/64. Full dispatch, registry, reports and results in `.ufo/waves/round-53/`.
- **C1 operability: unprovable / honest stop.** Base r51 comparator returned `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok TARGET_MET`, exit 0; `R53One1.md:61-79` reproduced generic-description, self-pointer and combined no-work bypasses. A scratch-only proposed r53 counter/measurement in `R53Five45.md` is not a lane artifact; no `c1-r53-*` counter, registration or frozen forgery set landed. Final C1 counter-file count remains 0 (`find quality/counters -maxdepth 1 -type f -name 'c1-r53-*' | wc -l`).
- **C2 coverage: unprovable / honest stop.** Source review re-derived P16's spliced/conditional quote, P17's wrong enclosing function and P18's post-loop return (`w1/R53Five41.md:81-103`; `R53Five45.md:235-257`). Added `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` and index marks old P16–P18 superseded; no `c2-r53-*` counter, independent non-author source-truth review, or uncovered ground/new domain source row landed. The row-count index moves 68→69, but this repair is not expansion credit. Frozen C2 target therefore has no valid final counter measurement.
- The routed r52 lesson gaps were addressed in `corpus/lessons/round-53.md`: row-level Gate records for S370–S373 and S374; QUALITY 17 distinct-scope verdict retains S370≠S365, S371≠S367, S373≠S364; round-52 stale Changes statement is corrected in this new lesson, not rewritten. S370/S371/S374 `used-by` changes are logged old→new there. S374 is an own-work row opened 2026-10-27; no held `status`/`recheck` changes.
- Sources: 310→311 rows; S374 added, tier A own-work/mined; end census exit 0. `corpus/knowledge/` and README index 68→69. Frontier unchanged (no new uncovered domain surface moved into core). Assimilation: none. `considerthese/2026-10-26.md` proposal 3 mined in the lesson; no package entry adopted. No tools installed/upgraded.
- Mined M53-1..M53-4 in `corpus/lessons/round-53.md`, including the missing pre-data control freeze. Learning trends: expansion unchanged (no new ground); quality improved only as a bounded append-only correction with independent review still pending; discernment unchanged (no round-53 non-author gate sample). No axis score/capability delta; SHONEN remains four historical `[~]` assertions.
- End census output ends `mado ok`, 311 rows, exit 0. Final lane/report commit hashes are recorded in the round-53 report after landing; no predicate or target was changed after seats scored.

## Round 54 (2026-10-27, hyaku run 10, attempt 2) — honest stop

- Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; inherited claims and registration were re-read. Freeze/pins landed `350d30e4ec5531f65ce99a57efeb8216f38e678a`, but w1 dispatched at 14:05:25/ready 14:05:28 and the freeze commit is 14:11:10 (`w1/R54Seat08.md`, `w1/R54Seat31.md`): the frozen inputs were not committed before launch (M54-4). No predicates were edited after scoring.
- Two v1 waves settled: w1 37 seats and w2 32 seats, 69 total, 0 dead. W1 roles executor 10, scribe 7, scout 4, reviewer 7, critic 3, mutation-tester 2, connector 2, sentinel 1, simplifier 1; attack share 12/37. W2 roles reviewer 11, critic 10, mutation-tester 6, scout 3, connector 2; attack share 27/32. Full specs, reports and results are under `.ufo/waves/round-54/`; L1 held planner.
- C1 operability — **unprovable / honest stop**. No counter landed. W1 demonstrated that the frozen quote judge has incompatible literal and whitespace-normalized readings (literal 1/4, whitespace-normalized 4/4); it also found the frozen control contract can be self-reported and that the P19 English proposition is contradicted by the adjacent `else` branch (`R54Seat28.md` F2; pinned `ConfigActions.cpp:1566-1569`). The attempted C1 counter stub was removed; no C1 count/capability is claimed.
- C2 coverage — **unprovable / honest stop**. The candidate entry was withdrawn. W1 found S375's frozen locator truncates its quote, S376's frozen quote omits source markup, S375/S377 are adjacent systemd manager/unit ground, and the host-join summary conflicts with the opened autostart file. The frozen predicate cannot be repaired after scoring. S375/S377 are rejected; S376 is mined only by the round lesson for the narrow transport fact; no knowledge entry or frontier coverage is claimed.
- Re-derived source census: 311→314 rows; three tier-A rows opened; status/used-by changes are in `corpus/lessons/round-54.md`. End census `mado ok`, exit 0, output `.ufo/waves/round-54/receipts/census-after.txt`. Knowledge files/index remain 69/69. The mado selftest remained `MADO_SELFTEST: 460/460 assertions passed`; no new instrument or capability landed.
- M54-1..M54-7 are in `corpus/lessons/round-54.md`, including the pre-data commit ordering defect and P19 overclaim. Expansion unchanged (no admitted new knowledge); quality harmed; discernment unchanged (no non-author closure sample yet). No axis score or capability delta. Three settled seats lack the assigned markdown sidecar (`R54Seat06`, `R54Seat19`, `R54W2Seat06`); their terminal outputs remain in the wave results JSON, not recreated as reports. Assimilation: none; no staged package or `considerthese` proposal was adopted. No tool installation/update.

## Round 55 (2026-10-28, hyaku run 11, attempt 1) — three claims, mechanically verified; content verification partial

- Base `3b55b6e9`; freeze `54dacbd8` (committer 18:46:52-03, before any wave; the helper rewrote it from `59e3763f` two seconds earlier) plus pre-data errata `registration-v2.md` (`5a43d67f`) after wave 1 found frozen-text defects (K16 quote held `||` against a no-pipe rule; K17 source rule unsatisfiable for S052; empty-stack KEY sentence contradicted fixture F10). v1 as literally written could not be met by C1.
- Shape: two v1 waves, w1 40 + w2 37 = 77 seats (w1: executor 12, reviewer 8, scribe 7, scout 6, critic 4, connector 2, sentinel 1; 2 scouts dead on a provider limit, re-issued in w2; w2: reviewer 14, critic 9, mutation-tester 9, scout 4, sentinel 1). L1 held planner. No residual call.
- C1 coverage: `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (K01-K18, H01-H06; rows S378-S382). C2 operability: `tools/mado-kbdopts.py` (capability). C3 freshness: append-only P23 block superseding the false P19. Mistake fix: `quality/check-freeze-order.py` + QUALITY 106.
- Measured at `d3fc9ac14a67` (`receipts/at-final.txt`): all frozen lines TARGET_MET (C1 18/18 7/7; C2 18/18 + 8/8 hold-out, controls 3/3; C3 13/13 6/6); selftest 460/460; index 70/70; census exit 0, 314→319 rows.
- Wave-2 attacks BROKE the verifiers' content power: junk entry, false-proposition entry and false P23 all reach TARGET_MET (declared limits); harness controls are defeated by sniffing/consistent-forgery counters; C2 fixtures kill few mutants (24 survivor-derived extra fixtures pass); the tool diverges from hyprlang on 8 listed constructs (docstring). Audit fixes applied (entry wording, E14 second push route, P23 overload scope, S381/S382 supersession rows, harness hardening). Details: lesson M55-1..M55-12, w2 reports.

## Round 56 (2026-10-28, hyaku run 11, attempt 1) — three claims, mechanically verified; content verification partial

- Base `13f0acbe`; freeze v1 `3423ae28` (committer 21:19:17-03) before any wave; wave 1 `2aa347b1` (43 seats, 0 dead). Wave 1 attacked v1 and found five defect classes, disclosed in `.ufo/waves/round-56/registration-v2.md`: C1 control 8 unsatisfiable as written; the C2 harness put `expected.out` beside the argument paths (a six-line reader scored 18/18 + hold-out; the round-55 M55-4 class again); the C3 target was met by deleting the citing tokens and a mechanical fill would record false reliance for about 21 of 65 pairs; the witness receipt overstated coverage; a declared divergence (`GLOB_TILDE`) was not one. Pre-data re-registration v2 `323a69c9` (before the real entry, counters, tool or hold-out reveal; scored v1 counters had run on the base and freeze trees, disclosed) plus errata E12-E14 `15015e77`.
- Integration `2e39282e`, `0ff41272`, `28fc86ac`; wave 2 (35 seats dispatched, 33 reported; `R56W2MutC3Counter` and `R56W2MutC2Harness` stopped at the operator wrap-up; the 78-seat total is w1 43 + w2 35) attacked the integrated tree and its sentence-to-pin audits corrected 9 K and 7 E propositions and 5 prose claims in the entry (`b70f6a2c`, `371d8234`). C1 `corpus/knowledge/hyprland-config-autoreload-r56.md` (K01-K30, H01-H03, E01-E09; rows S383-S395); C2 `tools/mado-watchplan.py` (capability); C3 `used-by` of 23 registry rows (41 paths) against entry citations.
- Measured at `8a7b734627b0` (`.ufo/waves/round-56/receipts/at-final.txt`): C1 `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 TARGET_MET`, harness 12/12; C2 `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 TARGET_MET`; C3 `entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 TARGET_MET`, harness 9/9; selftest 460/460; index 71/71; census exit 0, 319 -> 332 rows; tool ledger 97/97.
- What the numbers do not prove: C1 `TARGET_MET` is quote identity, registry binding, anchor scope and lexical grounding; a lexical rewrite that negates every proposition still reaches `content=33/33` (`w2/R56W2CritC1Forge.md`). C2's hold-out is spent (revealed before wave 2); an embedded 26-fixture lookup passes under bwrap, and the harness now refuses to run without bwrap (`w2/R56W2CritC2Cheat.md`). C3's 24 exemptions are two readers' judgment; `lost` covers 65 pairs (E12). Observation worth keeping: the running compositor's `/proc/<pid>/fdinfo` inotify table held 40 watches whose inodes and order equal the tool's prediction (`w2/R56W2RevProcFdinfo/comparison.md`); one host, one moment, no reload observed.
- Mined M56-1..M56-10 in `corpus/lessons/round-56.md` (M56-1 anchor does not cover the quoted line: criterion 107 text landed in `corpus/QUALITY.md`, able to fail on the round-55 K14/K17). Considerthese `2026-10-28.md` proposal 2 picked (`w1/R56ScoutConsiderthese.md`). Assimilation: none. Learning trends: expansion improved (a sourced chain on ground the corpus held 0 citations of, a capability), quality improved with a trade disclosed (nine over-stated propositions found and fixed; the counters stay content-blind), discernment unchanged (no non-author admit/reject sample at filing).

## Round 56, attempt 2 (2026-10-30 re-dispatch) — wave w3 settles the round the wrap-up stopped

- The run-11 operator wrap-up (2026-10-28 23:35) stopped attempt 1's wave 2 (33/35 reported;
  `R56W2MutC3Counter`, `R56W2MutC2Harness` killed; no `w2-results.json`); claims released
  without closure; the orchestrator re-dispatched round 56 on 2026-10-30 (watchdog launch
  `pgid=1984547`). Frozen claims (v2, `323a69c9`) ran unchanged.
- Attempt-2 self-verification at the inherited tip `0f3a5436` (`receipts/attempt2-l1.txt`):
  C1 `TARGET_MET rows=30/30 … content=33/33 new_rows=8/8` + controls 12/12; C2 `TARGET_MET
  fixtures=18/18 holdout=8/8 controls=4/4` (bwrap); C3 `TARGET_MET entries=71 rows=332
  missing=0 … exempt=24` + controls 9/9; census `mado ok` exit 0, 332 rows
  (`receipts/census-before-a2.txt`); selftest 460/460; index 71/71; ledger 97/97.
- Wave w3 (one v2 wave, 64 seats, band 64-128, attack share 28/64 = 43.75%): all 64 seats
  settled; 58 seat reports; six seats settled without reports (disclosed; no replacements —
  orchestrator recovery boundary). Re-issued the two stopped wave-2 mutation seats
  (`R56W3MutC2Harness` completed: 41/46 killed, 5 survivors documented; `R56W3MutC3Counter`
  mid-work, unverified). Re-fetched S383-S395 independently: 13/13 MATCH. Fresh
  sentence-to-pin audits: 2 UNSUPPORTED clauses, 17 single-line OVERREACH rows, 4 prose
  findings — 14 rows + 4 prose + 1 how-to line corrected before landing (entry edits above;
  counter `num`-leg bounded the rewrites, M56-12).
- Landed this attempt: registry rows S396-S397 (mined, lesson-cited; census 332 → 334, exit
  0 both ends); `quality/check-anchor-cover.py` (criterion-107 checker; green 39/39, red
  r55 32/25/7, 7/7 mutants, 23/23 vector agreement; ledger row added, population 98/98);
  kill-fixture suites (C1 51/51 distinguished, C2 24 killers, C3 kill-level table); C2
  harness re-verification; freeze-order re-proof + D4 blind-spot receipt; /proc second
  sample (40/40) + three-sample ALL_MATCH; tag-pin chain (v0.56.2 → efb50993, unsigned);
  C3 allowlist third reading (23 name-only + S044 reliance-leaning); census
  discrimination battery (6/6 mutants flagged, fills re-derived 0-defective, 4 new gaps
  named); considerthese proposal 2 receipt at the tip (`files=29471 findings=274`).
- Integrated tree re-measured (scratch preview `4c640a9a`, then the lane commit): all three
  frozen gates TARGET_MET + controls green; index 71/71; ledger 98/98; census 334 exit 0;
  CHECK107 rows=39 covered=39 miss=0.
- Mined M56-11..M56-15 in `corpus/lessons/round-56.md` (attempt-2 section); appended the
  owed round-55 census correction (routed round-55 defect 1). Open L0: rounds 28, 29 and 34
  (three lines) remain outstanding — named in the report (M56-13).
- 2026-10-30 15:21-03 operator ruling (events log): SECURITY HOLD lifted, dispatch with a
  credential-sanitization-first mandate; GH013 stays the remote guard. Sanitized and landed:
  folded the full attempt-2 delta into the working copy (`jj squash --from '0f3a5436..master'
  --into @`), abandoned the secret-bearing {cfc63604, f808ca67}, re-landed the redacted tree
  through `jj-lane.sh` as `441347bc` on base `0f3a5436`; push passed GH013; ls-remote
  verified local=remote=`441347bc`, ahead=0 (M56-18 documents the abandon strip-and-recover).
  Post-push battery all green at `441347bc` (`.ufo/waves/round-56/receipts/attempt2-l1-postpush.txt`);
  census exit 0 (`receipts/census-attempt2-end.txt`); secret-pattern set-compare base→tip:
  0 new matches (11 lookalikes are scanner pattern literals and short lowercase identifiers).
  Still operator-owned: revoke/rotate BOTH captured credential classes (sanitization does
  not invalidate live secrets); residual secret-bearing local objects until GC. Mined M56-18.

## Round 57 (2026-10-31, hyaku run 12) — the host changed: PROVINCE correction, a Windows observer capability, the first sourced Windows entry

- The lane's live host changed after round 56: this round observes Windows 11 Home build 26200 (`HOME=/c/Users/jpvei`, MINGW64_NT-10.0-26200; Python 3.13.15 as `python`, no `python3`). Every omarchy-era surface is absent (11/11 tool binaries, 10/10 config/doc trees; probes in `PROVINCE.md` § Round-57 host-change record). The file-plane gate confirms the drift as an absence record, not a regression: `bash tools/mado-verify.sh --no-live` → `MADO_VERIFY: DIVERGED (17 fail, 7 unknown, 2 pass)`, first fail `hypr.file.root`, `gate.boundary.readonly` PASS (gate bytes untouched this round).
- C1 **freshness** (lowest scored axis, 9.6552): the drift was detected, flagged and recorded — `PROVINCE.md` gains the dated host-change record + surface state register (8 groups: 7 absent with re-derivation probes, 1 observed), `SKILL.md` § Round 57 freezes the omarchy-host claims as host-scoped and carries the safety rules over (read-only plane; env channels asserted, never printed; window titles excluded), and the freshness sub-axis is re-baselined with a declared rubric (`surface-state audit currency` 0/8 → 8/8) while the omarchy-host rubric is marked dormant-host, disposal routed to L0. Counting: register rows `git show 5337d25:PROVINCE.md | grep -cE '^\| .* \| (absent|observed) \(2026-10-31\) \|'` → 0; at landing → 8.
- C2 **operability** (capability): `tools/mado-win-desk.py` — read-only Windows desktop observer (one fixed PowerShell child: CIM OS identity, `Screen.AllScreens`, `AppliedDPI`/`LogPixels` via two in-process registry layers, `dwmapi!DwmIsCompositionEnabled`, `Get-Process` census + `GetForegroundWindow`; `--from-file` snapshot re-derivation; `--selftest` spawns nothing). Selftest 9/9 exit 0; live `MADO_WINDESK: CLEAN (screens=1 dpi=96 dwm=on windows=6)`; cross-check 5/5 stable fields AGREE vs independently executed probes (screens, bounds, DPI×2, DWM flag); malformed snapshot → `MADO_WINDESK: ERROR` exit 2, raw bytes never echoed. It never prints window titles, clipboard, environment values or file contents (M56-17 rule carried). Two pre-landing selftest failures mined (M57-1/M57-2): the round-56-era checker scratch policy and the tool's own Windows temp-file lock. Tool ledger population 98 → 99 (`LEDGER: population=99 … TARGET_MET` at landing).
- C3 **coverage** (sourced): `corpus/knowledge/windows-desktop-plane-r57.md` — 5 host rows (each with its re-derivation command), 7 dated [INF-docs] rows (S398-S401, Microsoft Learn, opened 2026-10-31, ≤25-word verbatim quotes), 4 claim-to-host joins (J01 `agreement*` — the 96-DPI stretch path is unexercised here; J02 `agreement` carrying the manifest caveat), divergence D01 (the refreshed 2018-page DWM-overview sentence "runs as a Windows service … can be enabled and disabled" versus the same doc set's "As of Windows 8, DWM composition is always enabled"; observed TRUE on build 26200), limits section (no rendered pixel, no per-monitor DPI, point-in-time census, D01 open). Index row added; knowledge files 71 → 72; registry 334 → 338.
- Harm watch: census exit 0 both ends (`mado ok`); index 72/72 (navigation counter exit 0 at landing with `python` for `python3` — host rename); ledger 99/99; no existing entry, registry row cell, PROVINCE paragraph or SKILL section byte edited (all appends + new files); no hyprctl-era instrument re-pointed.
- L2 disclosure: MISSION's ≥8-L2 batched-dispatch floor is not met — no AgentSwarm/Kimi dispatch surface is reachable from this lane session on the new host; the round is L1-only, disclosed in SCORECARD, the report and an L0 line. Sources: 334 → 338 rows (S398-S401, tier A, `mined`, opened 2026-10-31, all four opened in full with ms.date/git_commit recorded; no rejected-row event — the sweep was bounded to the four surfaces the round rests on, stated in the search log). Considerthese mined: none adoptable this round (2026-10-28 proposal 2 was addressed in round 56 attempt 2; the "refresh the live plane" proposal is void on the old host — its object is gone; nothing else is in-lane). Assimilation: none — shokuknow unreachable. Mined M57-1..M57-4 in `corpus/lessons/round-57.md`.

## Round 58 (2026-10-31, hyaku run 12) — the per-monitor DPI join, the host-portable checker scratch policy, the r57 receipt gap closed

- Carry-in addressed first, per the r57 non-author closure routing: (1) the C2 malformed-snapshot ERROR sub-claim now carries committed evidence both ways — the selftest tally itself covers the ERROR path (`tools/mado-win-desk.py` `VERSION r58-v1`, 9/9 → 10/10; the 10th assertion runs `--from-file` against a malformed snapshot and pins rc=2, the `ERROR (stage=parse …)` line, and that raw payload bytes are never echoed) and a committed ERROR run exists (`.ufo/waves/round-58/receipts/windesk-error-path.txt`; live re-verified CLEAN after the change). (2) M57-1 stands and is fixed below (C1). (3) The omarchy freshness-rubric disposal stays an open L0 question — routed around, never treated as answered; a second L0 line adds the newly measured gate-selftest host gap.
- C1 **operability** (M57-1 routed fix): `quality/check-tool-ledger.py` and `quality/check-wave-done.py` accept `--scratch-root <dir>` — a caller-declared scratch tree that waives only the home-directory refusal (the shared-scratch prefixes stay refused in every mode, and the prefix compare now resolves prefixes, closing a base-state Windows bypass where `--work C:/tmp/…` slipped past the literal `/tmp` rule). Selftests pin the policy (50 → 54 and 58 → 62 pinned assertions; 4 new each): `LEDGER_SELFTEST: 54/54 passed` and `MADO_WAVE_DONE_SELFTEST: 62/62 passed`, both exit 0 via `--scratch-root` on this host; at base bytes both selftests refuse the contract scratch path (rc=2, committed receipts); default `--work` under home still refuses after the change; mutual `--work`+`--scratch-root` is a usage error. The gate `tools/mado-verify.sh` stays byte-untouched and frozen. Counting: `python quality/check-tool-ledger.py --selftest --work <scratch>` at base → rc=2; `python quality/check-tool-ledger.py --selftest --scratch-root <scratch>` → 54/54 rc=0; same shape for wave-done (62/62). Two pre-landing findings mined (M58-3: the waiver-as-candidate design broke the ledger P-rule — reworked into a waiver scope; M58-4: an exit code read through a pipeline tail — all committed receipts now own their rc).
- C2 **coverage** (sourced): `corpus/knowledge/windows-permonitor-dpi-r58.md` closes the r57 entry's named future ground — the per-monitor DPI join. 3 host rows (H06-H08: `GetDpiForMonitor` types 0/1/2 → effective 96 / angular 91 / raw 92 through one `HMONITOR`, two stable runs, rc=0; foreground window `GetDpiForWindow` → 96, point-in-time; `Screen.AllScreens` topology agreement with r57's H02), 7 dated [INF-docs] rows (K08-K14; S402-S404 opened 2026-10-31, ≤25-word verbatim quotes, ms.date/git_commit recorded; S403's archived previous-versions status carried in the row), 4 joins (J05 `agreement*` — effective 96 at 100% scaling is the r57-J01 vacuous shape, caller PROCESS_DPI_AWARENESS `[UNK]`; J06 — both pages map 0/1/2 identically; J07 — the awareness-branch ambiguity named), divergence D02 (the three documented modes do not collapse; raw/angular are panel facts and must never feed UI scale factors). The probe is a committed receipt artifact (`.ufo/waves/round-58/receipts/dpi-probe.ps1`, read-only). Index row added; knowledge files 72 → 73; registry 338 → 341. Mined M58-2: the probe's first draft ordered the enum values from an unopened search snippet (backwards); the opened pages caught it before any row was written.
- Harm watch / disclosure: `bash tools/mado-verify.sh --selftest` on this host → `MADO_SELFTEST: FAILED — 360 passed, 100 failed`, rc=2 (POSIX symlink fixtures denied by the host) — the operability rubric "existing hermetic suite pass fraction" is not re-derivable here; the score stands as the omarchy-host value, the receipt is committed (`gate-selftest-windows.txt`), SKILL § Round 58 corrects the r57 sentence's scope, and disposal is routed to L0 (the gate itself is untouched — rejected list). Census exit 0 both ends (`mado ok`); navigation counter at the landing revision expected 73/73; ledger population 99/99 (the observer row's assertion count updated 9 → 10 with the round); no existing registry row cell, PROVINCE paragraph, knowledge entry body or SCORECARD row rewritten (r57 entry gets an `## Errata (round 58)` block; everything else is appends + new files).
- L2 disclosure: unchanged from r57 — no dispatch surface on this host; L1-only round. Sources: 338 → 341 rows (S402-S404, tier A, `mined`, opened 2026-10-31, all three opened in full; no rejected-row event — the sweep was bounded to the three surfaces the probe rests on, stated in the search log). Considerthese mined: none adoptable (nothing new since the r57 mining; the directory's nine files re-screened). Assimilation: none — shokuknow unreachable. Mined M58-1..M58-4 in `corpus/lessons/round-58.md`.

## Round 59 (2026-10-31, hyaku run 12) — the DWM service model, the case-folded scratch refusal, the r58 carry-in corrections

- Carry-in addressed first, per the r58 non-author closure routing: (1) the stale `93e43f8f…` gate identity in `corpus/lessons/round-58.md` corrected append-only (`## Corrections (round 59)`: the pin is the round-9-11 arc freeze at 3,231 L; the gate this round declines to rewrite is blob `9113c7c05e586328f44ed6822a3d12ff34c47a36`, sha256 `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`, 4,194 L, byte-unchanged since round 19 / `7b4839d3`; receipt `gate-identity-r59.txt`). (2) The provenance trios the r57 and r58 entries lacked added as pure insertions above the titles (`source:` / `verified-at:` / `recheck:` per the CORPUS.md kaika rule; +4/−0 each). (3) The C:/TMP case-variation residual in the checker prefix rule — hardened below (C2) after a base-bytes bypass was demonstrated. (4) The two open L0 questions (omarchy freshness-rubric disposal; gate-selftest host gap) routed around, never treated as answered.
- C1 **calibration** (carry-in corrections): the lesson correction + the two trios above. No claim predicate, score, or existing row text changed; the corrections are appends and pure insertions; the r57 entry also gains an `## Errata (round 59)` block (the D01 closure pointer + the trio note). Counting: `grep -c '^source:' corpus/knowledge/windows-desktop-plane-r57.md` → 0 → 1 (same shape for the r58 entry); `grep -c '## Corrections (round 59)' corpus/lessons/round-58.md` → 0 → 1; `grep -c '9113c7c05e58' corpus/lessons/round-58.md` → 0 → 1.
- C2 **operability** (the residual hardened): at base bytes both fail-closed checkers ACCEPTED a case-variant spelling of an ABSENT shared-scratch prefix (`C:/DEV/shm/…` — `realpath` cannot case-fold a missing path; receipt `casefold-before.txt`, rc=1, bypasses=2; the carry-in's `C:/TMP` spelling is masked on this host because `C:\tmp` exists and `realpath` true-cases existing prefixes — per-prefix table in the receipt; `C:\tmp`/`C:\var` hold third-party content, untouched). Fix: `os.path.normcase` in the prefix compare of both checkers (identity on POSIX); named pin assertion `refuse-work-casefold` in each selftest (Windows-conditional: the case cannot arise where normcase is the identity; `SELFTEST_CHECKS` host-derived, 54 → 55 and 62 → 63); CLI refusals ×4 receipted (rc=2); default `--work` under home still refuses (rc=2); production mode `TARGET_MET` (population 99/99). Host left clean (probe removes every directory it creates; `C:/DEV` verified absent after). Mined M59-1 (rc=1 indistinguishable from a crash in the first probe draft — the exit-code vocabulary itself must be crash-safe), M59-2 (the masking host state; probe records pre-existence of every directory it might create), M59-3 (`git status` MM noise vs byte-identical `git show HEAD:` — tree state only ever asserted by byte comparison on this host).
- C3 **coverage** (sourced): `corpus/knowledge/windows-dwm-service-model-r59.md` closes the r57 entry's finding D01 (the refreshed DWM overview's Vista/7-era service sentence vs S400's always-enabled note). Sourced model row S405 (Microsoft Learn Compatibility Cookbook, opened 2026-10-31 in full; ms.date 2018-07-11, git_commit 40f2250e0d45a6cdf02bd22408933c9ee4c10d78): Windows-8+ DWM is an always-on core OS component, every Windows-7-era disabling path removed. Host joins (probe committed read-only, two byte-identical runs): `SERVICES 0`; `sc query UxSms` rc 1060; dwm.exe one process point-in-time, `tasklist /svc` services N/A; `DwmIsCompositionEnabled` hr=0 TRUE. 4 H rows + 6 K rows + 4 joins; D01 closed flip-met with the named residue (no Win11-labeled model sentence in the bounded sweep). Used-by cells of S399/S400 extended with the r59 entry + lesson (the exact consistency the used-by contract wants); search-log § Round 59 appended. Registry 341 → 342; knowledge files 73 → 74; index rows 73 → 74.
- Harm watch: census exit 0 both ends (`mado ok`; round-start run quoted in the report — not tee'd, disclosed; end receipt committed); navigation counter at the landing revision expected 74/74 exit 0; ledger population 99/99 (`LEDGER: … TARGET_MET` at base, re-run at landing); used-by counter at base → `missing=2 … TARGET_MISSED` — a pre-existing r58-era defect (the r57 entry's round-58 errata block names S402-S404 without their used-by cells; mined M59-4), repaired this round: the two cells extended with `corpus/knowledge/windows-desktop-plane-r57.md`, counter at the landing → `missing=0 … TARGET_MET` (receipts `usedby-before/after-r59.txt`); `tools/mado-verify.sh` bytes untouched (blob identity re-measured in the C1 receipt); no existing knowledge entry body or registry proposition cell rewritten (used-by cell extensions on S399/S400/S402/S404 are the used-by contract's own consistency moves; everything else appends, insertions, or new files).
- L2 disclosure: unchanged since r57 — no AgentSwarm dispatch surface on this host; L1-only round. Sources: 341 → 342 rows (S405, tier A, `mined`, opened 2026-10-31 in full; S399/S400 re-opened; one bounded sweep, no rejected-row event — the one surfaced candidate was opened and included, and the sweep reports the Win11-labeled-sentence miss honestly). Considerthese mined: none adoptable (nine files re-screened; nothing new since the r58 mining). Assimilation: none — shokuknow unreachable. Mined M59-1..M59-3 in `corpus/lessons/round-59.md`.

## Round 60 (2026-10-31, hyaku run 12) — the DPI-awareness join, the durable DPI observer, the r59 record corrections

- Carry-in addressed first, per the r59 non-author closure routing (three items): (1) the SCORECARD
  round-59 C1 row's parenthetical number-shape drift — the row's counting command is a per-file
  `git diff --stat` but its parenthetical read "(+4/−0, +5/−0)" while the measured per-file insertions
  at the landing are +17/−0 (`corpus/knowledge/windows-desktop-plane-r57.md`: trio +4 + errata +13) and
  +5/−0 (`corpus/knowledge/windows-permonitor-dpi-r58.md`: trio) — corrected append-only as a SCORECARD
  `### Corrections (round 60)` block carrying the re-derivation command (`git diff-tree -r --numstat
  6f2e4115 25294ab3 -- <two entries>`; the load-bearing property the r59 verifier confirmed — insertions
  only, no existing line modified — was and stays true). (2) The LOG round-59 tail bullet said "Mined
  M59-1..M59-3" while the r59 lesson holds four mined mistakes (M59-1..M59-4); the same-class defect in
  SKILL.md § Round 59's ground line ("(M59-1..M59-3)") was found by this round's sweep and corrected in
  the same move — both corrected append-only (this bullet; SKILL § Round 60 rule 3), original bytes
  untouched. (3) The three open L0 questions (omarchy freshness-rubric disposal; gate-selftest host gap;
  calibration resolved-active re-derivability) routed around, never treated as answered; a fourth L0
  line files the screen-capture-scope question the r59 route named as the rendered-pixel precondition.
- C1 **calibration** (carry-in corrections): the corrections above. No claim predicate, score, or
  existing row text changed; the SCORECARD/LOG/SKILL gains are appends (the r57/r58/r59 sections and
  both defect lines keep their original bytes). Counting: `grep -c '^### Corrections (round 60)'
  SCORECARD.md` → 0 → 1; `grep -c '^## Round 60' LOG.md` → 0 → 1; `grep -c '^## Round 60' SKILL.md`
  → 0 → 1; preservation by diff shape: `git diff <base>..<landing> --numstat -- SCORECARD.md LOG.md
  SKILL.md` → 0 deleted lines in each (the corrections live in new appends; checked at commit time —
  worktree-vs-index diff output is host garbage, the M59-3 rule). Receipt `before-state-r60.txt`
  (all base values).
- C2 **coverage** (sourced): `corpus/knowledge/windows-dpi-awareness-metrics-r60.md` closes the r58
  entry's named caller-branch residues in the same launch shape. Sourced rows S406-S411 (Microsoft Learn
  winuser/windef, opened 2026-10-31 in full BEFORE any row was written; ms.date 2018-12-05, git_commit
  fa53641576e3603fa7b66d3a4ad969d3ce49d6f3 for five pages, 9267262487657894a8af112d7165006fed5035a7 for
  the DPI_AWARENESS enumeration; every located quote verbatim) + re-used S404 for the J14 join. Host
  facts (probe committed read-only, two byte-identical runs rc=0): the `powershell.exe` child launch
  shape measures `DPI_AWARENESS_UNAWARE` (0) — H13; `GetSystemMetrics(SM_CXSCREEN/SM_CYSCREEN)` =
  1920x1080 equals `GetSystemMetricsForDpi(…, 96)` — H14 (agreement, vacuous at effective 96, named in
  J13: the getter identifies the branch, never the metrics join); main-window histogram 6 windows all
  `PER_MONITOR_AWARE` — H15 (point-in-time, no titles/names/handles collected); foreground dpi 96 with
  window awareness 2 — H16 (read against S404's return table; the r58 probe's own process context stays
  `[UNK]`, same-shape pin disclosed in J14; the r58 entry bytes untouched). 4 H + 7 K + 4 J rows. Index
  row added; knowledge files 74 → 75; registry 342 → 348; S404 used-by cell extended (the contract's
  consistency move, logged in the lesson).
- C3 **operability** (capability): `tools/mado-win-dpi.py` (`VERSION r60-v1`) — the durable form of the
  probe. Selftest **10/10** exit 0 (named assertions: whitelist drop, thread-awareness INVALID,
  GetSystemMetrics's documented 0-failure return treated as CHECK FAILED never a measurement, metrics
  disagreement at non-96 CLEAN not failed, histogram-sum self-check, from-file roundtrip, malformed
  ERROR with bytes never echoed, static no-titles/no-names/no-handles/no-Set* assertions); live
  `MADO_WINDPI: CLEAN (awareness=unaware metrics=1920x1080 dpi96=1920x1080 windows=6 fg_dpi=96)` twice,
  byte-identical rc=0; `--from-file` re-derives from the committed snapshot (rc=0); malformed snapshot →
  `MADO_WINDPI: ERROR (stage=parse …)` rc=2, raw bytes never echoed; crosscheck **5/5** stable fields
  AGREE against the independently executed probe. Tool ledger population 99 → 100 (ledger row +
  PROVINCE round-60 refinement landed in the same round). Harm watch: both checker selftests stay green
  at current bytes (`LEDGER_SELFTEST: 55/55`, `MADO_WAVE_DONE_SELFTEST: 63/63`, rc 0; receipt
  `harmwatch-selftests-r60.txt`); `tools/mado-verify.sh` bytes untouched this round.
- Harm watch / disclosure: census exit 0 both ends (`mado ok`; start run quoted in the report, end
  receipt `census-after-r60.txt`); navigation counter at the landing revision expected 75/75 exit 0;
  used-by counter at the landing expected missing=0 `TARGET_MET` (the M59-4 rule applied proactively:
  every row this round's appends name — S404, S406-S411 — carries the citing paths in its used-by cell
  in the same landing); no existing knowledge entry body or registry proposition cell changed (the S404
  used-by extension is the used-by contract's own in-place cell move, logged old→new in the lesson;
  everything else appends, insertions, or new files).
- L2 disclosure: unchanged since r57 — no AgentSwarm dispatch surface on this host; L1-only round.
  Sources: 342 → 348 rows (S406-S411, tier A, `mined`, opened 2026-10-31 in full; S404 re-opened for
  the J14 join at its held URL; one bounded sweep, no rejected-row event — the sweep was bounded to the
  six documented getters the probe invokes). Considerthese mined: none adoptable (nine files
  re-screened; nothing new since the r58 mining). Assimilation: none — shokuknow unreachable. Mined
  M60-1..M60-3 in `corpus/lessons/round-60.md`. Correction to this log's round-59 tail bullet, recorded
  here per the append-only rule: that bullet's "Mined M59-1..M59-3" is wrong — the r59 lesson holds
  M59-1..M59-4 (the r59 verifier spot-check § 6 item 2 named it; the same-class SKILL § Round 59 ground
  line was found by this round's sweep).

## Round 61 (2026-11-01, hyaku run 12) — the native display-topology plane, the durable display observer, the r60 carry-in corrections

- Carry-in addressed first, per the r60 non-author closure routing (two routed defects + the standing L0 set):
  (1) pointer-resolution defect — the r60 lesson's Census section named three receipt files that do not exist under
  those names (`navigation-landing-r60.txt`, `usedby-after-r60.txt`, `ledger-landing-r60.txt`); the runs they describe
  live in `.ufo/waves/round-60/receipts/landing-counters-r60.txt` (sections `-- navigation counter --`,
  `-- used-by counter --`, `-- tool ledger production --`), and the base used-by run is `usedby-before-r60.txt` —
  corrected append-only as `## Corrections (round 61)` in the r60 lesson naming the three supersedings (filed bytes
  untouched; this round's own landing counters adopt the named-sections file shape by construction, so the defect
  class cannot recur here). (2) Same-class sweep incompleteness — `corpus/lessons/round-59.md` line 74's
  "(diff shape +4/−0 each, checked at commit time in the report)" is the number-shape drift class round 60 corrected
  in SCORECARD/LOG/SKILL; it was counted by r60's `before-state-r60.txt` but left without a disposition — corrected
  append-only as `## Corrections (round 61)` in the r59 lesson beside the measured per-file +17/−0 and +5/−0
  (re-derivation `git diff-tree -r --numstat 6f2e4115 25294ab3 -- <the two entries>` → `17 0` / `5 0`; the
  corrections-block precedent is the r59→r58-lesson block). Preservation for both: originals byte-exact
  (`git show <base>:… | diff - <(head -n N)` — r59 lesson 217 lines, r60 lesson 181 lines at base; appends only,
  0 deleted lines). (3) The four open L0 questions (omarchy freshness-rubric disposal; gate-selftest host gap;
  calibration resolved-active re-derivability; screen-capture scope) routed around, never treated as answered; no
  new L0 line this round — the fourth is already filed (r60) and nothing new needed an operator decision.
- C1 **calibration** (carry-in corrections): the corrections above. Counting: `grep -c '^## Corrections (round 61)'
  corpus/lessons/round-59.md` → 0 → 1; `grep -c '^## Corrections (round 61)' corpus/lessons/round-60.md` → 0 → 1;
  `grep -c 'landing-counters-r60' corpus/lessons/round-60.md` → 0 → 3 (the superseding names now resolve);
  preservation by ORIGINAL_PRESERVED diff checks (worktree-vs-index diff is host garbage, the M59-3 rule — the
  check is `git show <base>:<file> | diff - <(head -n <base-lines>)`, both empty).
- C2 **coverage** (sourced): `corpus/knowledge/windows-display-topology-r61.md` lands the native display-topology
  plane and the display-mode layer — the one Windows-plane layer no entry held (r57 managed Screen, r58 per-monitor
  DPI, r59 DWM service model, r60 metrics/awareness). Sourced rows S412-S417 (Microsoft Learn winuser/wingdi, opened
  2026-11-01 in full BEFORE any row was written; ms.date 2018-12-05 for five pages — git_commit
  9267262487657894a8af112d7165006fed5035a7 / a9040b7bd365036907a35293e28d8cd449e31b87 /
  fa53641576e3603fa7b66d3a4ad969d3ce49d6f3 — and 2023-06-13 with f014fff5b27fe5eb5115f15dd6762713bc73c697 for
  DEVMODEW; every located quote verbatim). Host facts (probe committed read-only, two byte-identical runs rc=0;
  the tool independently agrees): native enumeration count 1 (H17, equal to the managed count); primary
  MONITORINFOEXW `\\.\DISPLAY1` rcMonitor (0,0,1920,1080) MONITORINFOF_PRIMARY set (H18, field-for-field with the
  managed layer); work area (0,0,1920,1032) — 48 px band, owner `[UNK]`, the taskbar is never read (H19, J17
  directional); current mode 1920x1080 @ 64 Hz, 32 bpp, registry settings identical, mode index series exactly 1
  (H20, D03 — a 1-mode driver list beside the three-way DPI split of r58 D02). 4 H + 10 K + 4 J rows. Index row
  added; knowledge files 75 → 76; registry 348 → 354; the mode layer is documented to ignore the calling context
  (K37), so the DPI entries' caller-awareness `[UNK]` does not arise here (J20).
- C3 **operability** (capability): `tools/mado-win-display.py` (`VERSION r61-v1`) — the durable form. Selftest
  **10/10** exit 0 (named assertions: whitelist drop, two-primaries CHECK FAILED, work-outside-monitor CHECK FAILED,
  the documented 0-failure return classes as CHECK FAILED never measurements, empty mode list CHECK FAILED,
  from-file roundtrip, malformed ERROR with bytes never echoed, static getter-only pins with exact per-site counts);
  live `MADO_WINDISPLAY: CLEAN (monitors=1 primary=\\.\DISPLAY1 mode=1920x1080@64 work=1920x1032)` twice,
  byte-identical rc=0; `--from-file` re-derives from the committed snapshot (rc=0); malformed snapshot →
  `MADO_WINDISPLAY: ERROR (stage=parse …)` rc=2, raw bytes never echoed; crosscheck **5/5** stable fields AGREE
  against the independently executed managed probe (crosscheck script committed beside its receipt). Tool ledger
  population 100 → 101 (ledger row + PROVINCE round-61 refinement landed in the same round). Harm watch: both
  checker selftests stay green at current bytes (`LEDGER_SELFTEST: 55/55`, `MADO_WAVE_DONE_SELFTEST: 63/63`, rc 0;
  receipt `harmwatch-selftests-r61.txt`); `tools/mado-verify.sh` bytes untouched this round.
- Harm watch / disclosure: census exit 0 both ends (`mado ok`; START TEE'D TO A COMMITTED RECEIPT this round —
  `census-start-r61.txt` closes the r59/r60 un-tee'd disclosure; end receipt `census-after-r61.txt`); navigation
  counter at the landing revision expected 76/76 exit 0; used-by counter at the landing expected missing=0
  `TARGET_MET` (the M59-4 rule applied proactively: every row this round's appends name — S412-S417 — carries the
  citing paths in its used-by cell in the same landing); no existing knowledge entry body or registry proposition
  cell changed this round (the six S-rows are new rows with their cells written at insertion; everything else
  appends, insertions, or new files).
- L2 disclosure: unchanged since r57 — no AgentSwarm dispatch surface on this host; L1-only round. Sources: 348 →
  354 rows (S412-S417, tier A, `mined`, opened 2026-11-01 in full; one bounded sweep, no rejected-row event; one
  URL-correction event recorded in the search log and mined M61-2). Considerthese mined: none adoptable (nine files
  re-screened; nothing new since the r58 mining). Assimilation: none — shokuknow unreachable. Mined M61-1..M61-2 in
  `corpus/lessons/round-61.md` (M61-1: the M60-1 class recurring three times in one selftest tally — assertion
  bugs, never tool bugs, each read against the implementation before either was edited; M61-2: a struct-header
  locator guess 404'd inside the sweep, caught by open-before-write).

## Round 62 (2026-11-01, hyaku run 12) — the DWM client-attribute plane, the durable DWM observer, the r61 carry-in corrections

- Carry-in addressed first, per the r61 non-author closure routing (two routed defects + the standing L0 set):
  (1) report-table number drift — the round-61 report's "Landed changes" table rows for `LOG.md` ("+52"),
  `PROVINCE.md` ("+13") and `SKILL.md` ("+50") are wrong per file while the totals ("28 files, +1416/−0")
  are right; measured per-file insertions **+64/−0, +19/−0, +55/−0** (re-derivation `git diff-tree -r
  --numstat cccda4da ad4e8403 -- LOG.md PROVINCE.md SKILL.md` → `64 0` / `19 0` / `55 0`; totals
  `28 files 1416 added 0 deleted`) — corrected append-only as `## Corrections (round 62)` in
  `corpus/lessons/round-61.md` naming the superseded table rows, restated as the erratum in the round-62
  report (the fleet-root report file itself is not lane-edited). (2) Same-correction family nit — the r61
  correction block names the receipt section `-- navigation counter --`; the actual header at base is
  `-- navigation counter (SCORECARD fence, python for python3) --` (re-derivation `git show
  4c5435d8:…landing-counters-r60.txt | grep -n '^--'` → line 2), and LOG's own round-61 carry-in bullet
  above carries the same short form — corrected append-only as `## Corrections (round 62)` in
  `corpus/lessons/round-60.md` plus this bullet naming both sites; defect lines keep their original bytes
  (preservation: `git show <base>:<lesson> | diff - <(head -n N)` — r60 lesson 208 lines, r61 lesson 175
  lines at base, both ORIGINAL_PRESERVED). (3) The four open L0 questions (omarchy freshness-rubric
  disposal; gate-selftest host gap; calibration resolved-active re-derivability; screen-capture scope)
  routed around, never treated as answered; no new L0 line this round — nothing new needed an operator
  decision (the D04 timing failure is recorded as a host finding, not an operator question).
- C1 **calibration** (carry-in corrections): the corrections above. Counting: `grep -c
  '^## Corrections (round 62)' corpus/lessons/round-61.md` → 0 → 1; same grep on
  `corpus/lessons/round-60.md` → 0 → 1; the numstat re-derivation is in the r61 lesson's block and in
  `before-state-r62.txt` (measured at round start, before any edit); preservation ORIGINAL_PRESERVED as
  above. Base values: `before-state-r62.txt` (navigation 76/76, SOURCES 354, ledger 101, entry and tool
  absent at base).
- C2 **coverage** (sourced): `corpus/knowledge/windows-dwm-attributes-r62.md` lands the DWM
  client-attribute plane — the layer between the held layers (r57/r59 composition + service model from
  the outside, r58/r60 DPI, r61 topology): H21 composition TRUE beside r59's pin; H22 the cloaked-window
  census (14 cloaked of 161-170 top-level in five committed executions, reasons 7 app + 7 shell + 0
  inherited in every execution, attr_failed 0; counts only — never handles/titles, never a per-window
  tabulation, J22's cross-layer `[UNK]` named); H23 the frame-bounds join (GetWindowRect beside
  DWMWA_EXTENDED_FRAME_BOUNDS on the probe's own console window: 7 px inset left/right/bottom, 0 top, in
  every execution — J23 separates the two documented causes: the resize-border cause observed, the
  DPI-virtualization cause vacuous at effective 96, the r60 J13 shape); H24/D04 the timing getter fails
  with undocumented `0x88980090` in BOTH documented call shapes (NULL required shape; non-NULL
  E_INVALIDARG promise), cbSize 320 per the documented 39-member layout, deterministic — the
  rateRefresh→r61's-64-Hz join never lands and stays `[INF-docs]`. 6 dated `[INF-docs]` rows K38-K43
  (S418-S423, opened 2026-11-01 in full BEFORE any row was written; one URL-correction event inside the
  sweep — the underscore slug — mined M62-2). Index row added; knowledge files 76 → 77; registry
  354 → 360; entry row count 14 (4 H + 6 K + 4 J; the finding D04 is a Findings bullet).
- C3 **operability** (capability): `tools/mado-win-dwm.py` (`VERSION r62-v1`) — the durable form.
  Selftest **11/11** exit 0 after three red assertion-authoring runs (the M61-1 class again: a generic
  `"wmi"` substring ban colliding with the legitimate `DwmIsCompositionEnabled` P/Invoke; two static
  count assertions written against remembered shapes — `enumwindows` 5 sites not 2, `iswindow(` paren
  form 3 not the bare-substring 5; each read against the implementation, every fixed assertion carries
  its site list); live `MADO_WINDWM: CLEAN (composition=on reasons=app+shell
  timing=unavailable(hr=0x88980090))` twice, **verdict lines byte-identical** rc=0, the JSON lines
  differing only in the named churn field (`windows.top_level` 168→170, receipt
  `windwm-live-churn-diff.txt` — the declared amendment narrowed this receipt shape before the formal
  runs); `--from-file` re-derives from the committed snapshot (rc=0); malformed snapshot →
  `MADO_WINDWM: ERROR (stage=parse …)` rc=2, raw bytes never echoed; crosscheck **5/5** stable fields
  AGREE against the independently executed probe (+ census structure, no equality claim on churn-prone
  counters); no Set*/Move*/Change* verb exists in the tool. Tool ledger population 101 → 102 (ledger
  row + PROVINCE round-62 refinement landed in the same round).
- Harm watch / disclosure: census exit 0 both ends (start tee'd to `census-start-r62.txt` — the r61
  committed-receipt shape kept; end receipt `census-after-r62.txt`); navigation counter at the landing
  revision expected 77/77 exit 0; used-by counter at the landing expected missing=0 `TARGET_MET` (the
  M59-4 rule applied proactively: every row this round's appends name — S418-S423 — carries the citing
  paths in its used-by cell at insertion); `tools/mado-verify.sh` bytes untouched this round (sha256
  prefix `050efc720599345a` re-measured); both fail-closed checkers' selftests stay green at current
  bytes (55/55, 63/63 — receipt `harmwatch-selftests-r62.txt`); no existing knowledge entry body or
  registry proposition cell changed (the six S-rows are new rows with their cells written at insertion;
  everything else appends, insertions, or new files).
- L2 disclosure: unchanged since r57 — no AgentSwarm dispatch surface on this host; L1-only round.
  Sources: 354 → 360 rows (S418-S423, tier A, `mined`, opened 2026-11-01 in full; one bounded sweep, no
  rejected-row event; one URL-correction event recorded in the search log and mined M62-2). Considerthese
  mined: none adoptable (nine files re-screened; nothing new since the r58 mining). Assimilation: none —
  shokuknow unreachable. Mined M62-1..M62-2 in `corpus/lessons/round-62.md` (M62-1: the number-shape
  drift class recurring in the r61 report's own Landed-changes table beside a C1 that corrected the same
  class — every table number now carries its numstat; M62-2: a struct slug written with hyphens where
  the docs keep the type name's underscore — the M61-2 locator rule applied, refinement recorded).

- Amendment to this round's harm-watch bullet above, recorded here per the
  append-only rule before closure: the sentence "no existing knowledge entry
  body or registry proposition cell changed" is incomplete as to the
  used-by layer. Row S400's used-by cell moved in place across the round
  (old suffix `…windows-dwm-service-model-r59.md, corpus/lessons/round-59.md |`
  → new suffix `…corpus/lessons/round-59.md,
  corpus/knowledge/windows-dwm-attributes-r62.md |`; proposition text
  untouched), which is why the final landing range numstat reads
  +1806/−1 with the single −1 being S400's row line (the used-by
  contract's own consistency move, red-amber-green recorded in
  `landing-counters-r62.txt` and the lesson Addendum/Addendum 2;
  S405's mis-aimed extension nets to zero at the final tip). The
  proposition-cell half of the sentence stands as written.

## Round 63 (2026-11-01, hyaku run 12) — the DisplayConfig path/target plane, the durable CCD observer, the r62 carry-in corrections

- Base `cb442f663ca616c0825ed10beccece26bf920b35` (the r62 verifier
  spot-check). Claims declared before the formal receipt runs:
  `.ufo/waves/round-63/claims-declaration-r63.md`. Axis posture unchanged
  (saturation 9.0 / N=3, last capability r62, gap 1 < 3; every published
  scored sub-axis at its finite maximum at base — before-state-r63.txt:
  navigation 77/77, SOURCES 360, ledger 102/102 TARGET_MET); the four
  dormant-rubric L0 questions plus the standing L2-floor line routed
  around again, never treated as answered. L1-only round (no dispatch
  surface on this host; disclosed since r57).
- C1 **calibration** — the r62 carry-in corrections, append-only: ONE
  `## Corrections (round 63)` block in `corpus/lessons/round-62.md`
  dispositioning all six closure-routed drifts (total-range mislabel →
  35 files +1830/−1 at the receipts tip / 34 files +1806/−1 only at
  `bd06d021` / 35 files +1860/−1 final; "wave receipts +441" → 21 files
  +359 receipts-only, 23 files +466 wave total; "18 receipt files" → 20;
  "Four commits" → 5; census endpoint "161-170" → committed all-run range
  160-170 with probe run 2's `top_level` 160; declaration S418-S422 vs
  landed S418-S423 noted), each beside its re-derivation command, plus
  the in-file `## Errata (round 63)` on entry row H22 in
  `corpus/knowledge/windows-dwm-attributes-r62.md` (defect row
  untouched). ORIGINAL_PRESERVED both files (r62 lesson 254 lines, r62
  entry 72 lines at base; show-pipe diff empty). One drift in this
  round's own draft block — "255 lines at base" against base 254 —
  caught and fixed before landing: the class rule applies to itself.
- C2 **coverage** (sourced) — the DisplayConfig (CCD) path/target plane:
  `corpus/knowledge/windows-displayconfig-r63.md` (H25-H28 with
  re-derivation commands, K44-K54 dated `[INF-docs]`, J25-J28, finding
  D05 — the mode table's `pixelRate`/`hSyncFreq`/`vSyncFreq` read the
  undocumented sentinel 0xFFFFFFFE in every committed execution beside a
  sane 1920x1080 `activeSize`, while the path-side `refreshRate` reads
  **64/1**, agreeing with r61's GDI 64 Hz across two documented OS
  planes; the DWM timing side rechecked unchanged this round:
  `MADO_WINDWM: CLEAN (composition=on reasons=app+shell
  timing=unavailable(hr=0x88980090))` — D04 stands). Registry S424-S434
  (tier A, `mined`, opened in full before any row was written; 11
  identified / 11 screened / 11 included / 0 excluded; one locator event
  — the remembered enum order overruled by the opened page — mined
  M63-3; no 404 event). Limits restated: no rendered pixel, no names or
  ids (the documented name getter deliberately not called), enum
  integers only, source-mode union not decoded, no Set*/Change* verb.
- C3 **operability** (capability): `tools/mado-win-displayconfig.py`
  (`VERSION r63-v1`) — the durable form. Selftest **13/13** exit 0 after
  two disclosed red runs (M63-1: the first on-disk write lost the
  embedded script's two-line tail — invocation + closing triple-quote —
  and the tokenizer reported it 190 lines away as an "invalid character"
  inside an ordinary docstring; the odd triple-quote count was the
  diagnosis; M63-2: the M62-3 class's fourth recurrence, a count
  assertion `intptr.zero == 2` written against a remembered comment
  shape, actual sites 1, fixed to the implementation with its site
  list); live `MADO_WINDISPLAYCONFIG: CLEAN (paths=1 refresh=64/1
  vsync=unavailable(0xfffffffe))` twice, **outputs byte-identical** rc=0
  (the CCD topology moves only on a display change — a named, different
  churn class than the r62 census); `--from-file` re-derives from the
  committed snapshot (rc=0); malformed snapshot →
  `MADO_WINDISPLAYCONFIG: ERROR (stage=parse …)` rc=2, raw bytes never
  echoed; crosscheck **5/5** stable fields AGREE against the
  independently executed probe (+ verdict structure); the raw-byte dump
  receipt (`displayconfig-rawdump.txt`) distinguishes layout error from
  host fact for D05 (documented offsets carry `FE-FF-FF-FF` while
  `activeSize` carries 1920/1080); no Set*/Change* verb exists in the
  tool. Tool ledger population 102 → 103 (ledger row + PROVINCE
  round-63 refinement landed in the same round).
- Harm watch / disclosure: census exit 0 both ends (start tee'd to
  `census-start-r63.txt` — the r61/r62 committed-receipt shape kept; end
  receipt `census-after-r63.txt`); navigation counter at the landing
  revision expected 78/78 exit 0; used-by counter at the landing expected
  missing=0 `TARGET_MET` (the M59-4 rule applied proactively: every row
  this round's appends name — S424-S434 — carries the citing paths in
  its used-by cell at insertion); `tools/mado-verify.sh` bytes untouched
  this round (sha256 prefix `050efc720599345a` re-measured); both
  fail-closed checkers' selftests stay green at current bytes (55/55,
  63/63 — receipt `harmwatch-selftests-r63.txt`); the two corrected r62
  records are pure appends; no existing knowledge entry body or registry
  proposition cell changed (the eleven S-rows are new rows with their
  cells written at insertion; everything else appends, insertions, or
  new files). Receipt defect disclosed before commit: the first
  before-state draft ran the harmwatch selftests without the
  caller-declared `--scratch-root` and mis-grepped the live-run JSON
  spacing — both re-derived in the receipt (QUALITY 26).
- L2 disclosure: unchanged since r57 — no AgentSwarm dispatch surface on
  this host; L1-only round. Sources: 360 → 371 rows (S424-S434, tier A,
  `mined`, opened 2026-11-01 in full; one bounded sweep, no rejected-row
  event; one locator event recorded in the search log and mined M63-3).
  Considerthese mined: none adoptable (nine files re-screened 2026-11-01;
  nothing new since the r58 mining). Assimilation: none — shokuknow
  unreachable. Mined M63-1..M63-3 in `corpus/lessons/round-63.md` (M63-1:
  the write-tail truncation the tokenizer reported 190 lines from the
  defect — the selftest is the first reader of every new tool byte;
  M63-2: the static-count-assertion class's fourth recurrence — counts
  are written from the implementation's bytes, never from memory;
  M63-3: an enum's values remembered in the wrong order, caught by the
  open-before-write sweep before any code or row was written — enumerated
  values come from the opened page).

- Amendment to this round's harm-watch bullet above, recorded here per the
  append-only rule before closure: the sentence "used-by counter at the
  landing expected missing=0 `TARGET_MET`" was written as a prediction,
  and the landing's actual used-by run was red — not on a missing cell
  (the M59-4 proactive rule held: all eleven S-rows carried their citing
  paths at insertion) but on the counter's setup gate: S430's `teaches`
  cell carried two unescaped pipes and read as 13 cells. Repaired in-round
  (cell re-keyed on the row id, pipe set replaced with slashes,
  proposition text otherwise untouched); the counters receipt records the
  red run at `c9a70974` and the green run at the repair `cdacf215`
  (`entries=78 rows=371 … TARGET_MET`). Full record: lesson Addendum and
  `landing-counters-r63.txt`.

- Second amendment to this round's record, before closure: the landing
  commit `c9a70974` named `.ufo/waves/round-63/receipts` as a commit path
  and the plumbing helper landed none of the directory's 24 files — the
  post-landing `ls-tree` check on the receipts subtree caught it (the
  commit-side twin of M63-1's write-trusted-from-its-echo; the helper
  accepts a directory argument silently and lands only explicitly named
  files). All 24 receipt files re-landed by explicit path at `49b053e8`,
  bytes as measured; the rule is recorded in lesson Addendum 2 (receipt
  directories are committed file-by-file; every committed artifact is
  verified at its own path). The counters receipts at `c9a70974` /
  `cdacf215` are unaffected (they recorded git-object runs at those shas,
  which exist unchanged).

## Round 64 (2026-11-01, hyaku run 12) — the r63 carry-in repair, the D05 flip-condition probe, the citation checker capability

- Base `7fe65562c15d20e5cfdc1da536f774149ab52b7e` (the r63 closure tip,
  pushed). Claims declared before the formal receipt runs:
  `.ufo/waves/round-64/claims-declaration-r64.md`. Axis posture unchanged
  (saturation 9.0 / N=3, last capability r63, gap 1 < 3; every published
  scored sub-axis at its finite maximum at base — `before-state-r64.txt`,
  every producer's rc captured: navigation 78/78 = 10.0000, used-by
  missing=0 TARGET_MET, ledger population=103 TARGET_MET, registry 371
  rows, mado-verify.sh sha prefix `050efc720599345a`); the four
  dormant-rubric L0 questions plus the standing L2-floor line routed around
  again, never treated as answered. L1-only round (no dispatch surface on
  this host; disclosed since r57).
- C1 **calibration** — the r63 carry-in repair (the closure's routed item
  1): the r63 error-path receipt cited its input fixture
  `.ufo/waves/round-63/receipts/broken-fixture.json`, which never landed.
  The fixture is now committed at the cited path — disclosed everywhere it
  is claimed as the round-64 re-creation (a truncated JSON snapshot; the
  r63 original's bytes were ephemeral and are unrecoverable, and the r63
  receipt remains the record of the r63 run) — and the verdict is
  re-derived against committed bytes: rc=2,
  `MADO_WINDISPLAYCONFIG: ERROR (stage=parse detail=JSONDecodeError in
  snapshot .ufo/waves/round-63/receipts/broken-fixture.json)` — the same
  whitelisted detail line as the r63 receipt, raw bytes never echoed
  (`windisplayconfig-errorpath-r64.txt` + stderr). Before 0 → after 1 by
  the ls-tree count; the citation now resolves.
- C2 **coverage** (sourced) — the D05 flip-condition probe the r63 closure
  named as the r64 candidate: S424 re-opened this round (page unchanged:
  ms.date 2018-12-05, git_commit `39f250c30f4e46de1ef92f2ef07161753ba36e35`,
  updated_at 2026-05-15; the flags table pins QDC_VIRTUAL_MODE_AWARE 0x10
  Windows 10+ and QDC_VIRTUAL_REFRESH_RATE_AWARE 0x40 Windows 11+; the
  page's own example code is the 0x12 shape), then one bounded read-only
  probe (`.ufo/waves/round-64/receipts/qdc-flagmatrix-probe.ps1`; getters
  only; whitelist unchanged — counts, rationals, flags, enum integers; no
  ids, no LUID halves, no names) ran the four documented shapes 0x02 / 0x12
  / 0x42 / 0x52 twice, byte-identical (`qdc-matrix-run1/2.json`). Measured:
  the virtual-refresh shape is the r63 baseline verbatim — same table,
  same 0xFFFFFFFE sentinel (H29); the virtual-mode shapes grow the mode
  table by a DESKTOP_IMAGE entry (infoType 3, the documented K51
  vocabulary), set the documented SUPPORT_VIRTUAL_MODE path flag 0x8
  (K46), and move the path's target `modeInfoIdx` 0 → 2 onto that
  non-TARGET entry, where the decode guard (infoType == 2) emits null —
  the r63 rejected-row discipline kept (H30). Disposition: D05 **narrowed,
  not flipped** — no documented shape returns decoded frequencies, the
  cause stays `[UNK]`, and the remaining residue is the driver-class /
  second-host reading, operator-scoped (H31); D05's original bytes
  untouched. The entry gains the append-only `## Update (round 64)`
  sections (rows H29-H31 + J29; 19 → 23 row sites); the 0x02 leg
  crosschecks 19/19 stable fields AGREE against the r63 committed snapshot
  (`qdc-matrix-crosscheck.py` + receipt); the r63 observer re-run CLEAN at
  r64 (`windisplayconfig-recheck-r64.txt`).
- C3 **operability** (capability acquisition) —
  `tools/mado-receipt-citecheck.py`: the r63 closure's routed defect class
  (a receipt citing a committed-looking path that never landed) mechanized
  as a read-only checker — strict anchored file-path-citation grammar
  (bare-directory, rev-prefixed, absolute and URL forms are not
  citations), one `git ls-tree -r --name-only` child per run, MISSING
  citations named with their citing files, 4 MiB read cap, hermetic
  12-assertion `--selftest` under a caller-declared `--scratch-root` that
  spawns nothing; caller-named scan scope only, never run over r56-era
  material (the security boundary). Red demonstration at the base rev:
  the checker over the r63 receipts at `7fe65562` names exactly the routed
  citation MISSING (`missing=1 … TARGET_MISSED` rc=1,
  `citecheck-red-base-rev.txt`); green at the landing (landing counters).
  Ledger row + PROVINCE round-64 refinement landed the same round;
  ledger population 103 → 104.
- Harm watch / disclosure: census exit 0 both ends (start tee'd to
  `census-start-r64.txt`; end receipt `census-after-r64.txt`); navigation
  78/78 exit 0 at the landing; used-by missing=0 TARGET_MET at the landing
  (registry untouched at 371 — no rows added or edited); ledger 104/104;
  `tools/mado-verify.sh` bytes untouched (sha prefix `050efc720599345a`);
  both fail-closed checkers' selftests green (55/55, 63/63) with the
  caller-declared `--scratch-root`; r62/r63 observers' verdicts re-measured
  unchanged (`dwm-recheck-r64.txt` — D04 stands; displayconfig recheck —
  the D05 baseline); every record edit an append (head-diff prefix checks
  in the landing counters receipt); the two work-window write defects
  (M64-1 quoting, M64-2 truncated long-heredoc — SCORECARD restored
  byte-exact from the base git object) disclosed in
  `corpus/lessons/round-64.md`. Sources: 371 → 371 rows (no new URL entered
  the sweep — the r64 probe's entire documented surface is the r63-opened
  row set; S424 re-opened, recorded in the lesson Gate); no new census W04.
  Considerthese mined: none adoptable (nine files re-screened 2026-11-01;
  directory listing + mtimes unchanged since the r63 screen). Assimilation:
  none — shokuknow unreachable. L2 disclosure: unchanged since r57. Mined
  M64-1..M64-2 in `corpus/lessons/round-64.md`.

- Amendment to this round's harm-watch bullet above, recorded per the
  append-only rule before closure: the ledger-append at the landing
  `688144573a26` glued the new citecheck row onto `quality/tool-ledger.md`'s
  final r63 row (that row carried no trailing newline at base), and the
  ledger counter went RED at the landing
  (`population=104 ledger_rows=102 uncovered=2 dangling=1 …
  verdict=TARGET_MISSED`, rc=1) — the ledger gate caught the write defect
  before closure. The diff-tree numstat's `1 deleted` on the ledger file
  was the second tell (no honest pure-append round contains a deletion).
  Repaired keyed on the row content: glued line split, r63 row bytes
  restored byte-exact (head-prefix cmp against base, R63_ROW_RESTORED_BYTE_EXACT),
  trailing newline added; GREEN at the repair `8c5af6ad`
  (`population=104 ledger_rows=104 uncovered=0 dangling=0 …
  verdict=TARGET_MET`). Both states in `landing-counters-r64.txt` (named
  sections); the repair commit discloses the defect. Lesson Addendum
  records the class rule: an append is read back at its JOIN, not only at
  its new bytes.

## Round 65 (2026-11-03) — returned-host register and standing landing instrument

- Claims frozen at `cb63ab13ccaf85191318701d5db5ace050bd5bd4`: C1 freshness
  (eight-group register re-derived on returned omarchy host); C2 operability
  (one-command landing-counters capability). Content landed at
  `c6b8ec301ac54c2c082ad228cbacabecbd15b48e`.
- C1 base control MISS rc=1 → measured MET rc=0 (8 groups, 4 resolved receipts);
  C2 absent-at-base MISS rc=1 → MET selftest=0 landing=0 rc=0. Exact commands
  and outputs: `.ufo/waves/round-65/measurement-final-r65.txt`. First-run red
  is preserved in `measurement-first-r65.txt`: output inside the receipts scan
  made the tree dirty; relocating the output fixed the observation, not code.
- Wave w1: 12 seats, all settled (WAVE-DONE received); 4 executors, 2 scouts,
  2 reviewers, 1 critic, 1 mutation-tester, 1 scribe, 1 connector; 4/12 attack.
  Planner mapping: L1. Results and seat reports under `.ufo/waves/round-65/`.
- Lesson `corpus/lessons/round-65.md` records the live-host return, forged-cell
  counter limit, critic blockers, fixes, mutation survivors and wrong-column
  premise. Live gate CLEAN 52 pass, selftest 460/460; no desktop writes.
- Source rows 371 unchanged in count; S028/S097 reopened with located quotes,
  opened cells advanced to 2026-11-03, on-release cadence unchanged. Census
  exit 0 both ends. Assimilation none: package reachable, no fitting theme.
  Considerthese unchanged since prior screen. No tools installed.
- Prior-art attribution: kumitate round-gate/cite-check and tsukuroi cited-receipt
  gate share the one-command shape; mado claims capability, not novelty.

## Round 66 (2026-11-03) — record binding and child-status discrimination

- Two claims, declaration `ed980316e330703030d0c17b2a7098e058295b99`:
  C1 calibration (three structural register controls plus genuine case),
  C2 operability (four child-status controls plus selftest and actual landing).
  Motivation: `corpus/lessons/round-65-verifier-spotcheck.md` routed items 1-3.
- New `quality/counters/c1-r66-register.py` and
  `quality/counters/c2-r66-landing-instrument.py`; current
  `quality/landing-counters.sh` cutover requires round scope and distinguishes
  ERROR from RED. Old r65 counter files remain pinned history, not aliases.
- Sources: one new S435, Bash exit-status vocabulary, cited by
  `corpus/lessons/round-66.md`; no existing source cells changed.
  QUALITY 108, SKILL gate rows and PROVINCE inventory document the bounded
  structural guarantee. No new desktop surface or knowledge entry.
- Seat evidence under `.ufo/waves/round-66/w1/`: baseline 1/4 for each
  claim; candidate demonstrations 4/4. Committed-revision results follow
  in a separate measurement entry; draft tests are not substituted for them.
- The lesson retains freeze/control-order violations, marker premise error,
  file-plane-only control ambiguity, state-truth gap and mutation survivors.
  No universal soundness, promotion or novelty claim. Assimilation none.

### Round 66 — committed measurement result

- At `739a01c5191a1b5bb21ef2a5f7792aab6e152328`, both frozen commands
  print correct=4/4 TARGET_MET rc0; each base run at `eafd500f` scores
  correct=1/4 TARGET_MISSED rc1. Full commands and outputs:
  `.ufo/waves/round-66/measurement-c1-before.txt`,
  `measurement-c1-after.txt`, `measurement-c2-before.txt`,
  `measurement-c2-after.txt` in that same wave directory.
- C2 includes extracted driver selftest 58/58 and actual landing GREEN:
  navigation 78/78, used-by missing0, ledger108/108, citations4/4.
  Retained raw driver logs are under
  `.ufo/waves/round-66/measurement-evidence/c2-after/candidate/driver/`.
- WAVE-DONE received: one v1, 12 settled seats, four executors, two scribes,
  scout/connector/reviewer/critic/mutation-tester/sentinel one each;
  attack3/12, planner L1, residual0, dead0. Wave checker OK rc0:
  `.ufo/waves/round-66/wave-done-final-r66.txt`.
- Source census exit0 both ends; exact histograms/commands in
  `.ufo/waves/round-66/sources-shape-r66.txt`. Rows371→372, one new
  A/docs/mined S435; no old source cells changed. No tool installs.
- No attributable misroot found; unrelated fleet `.scratch`, sibling
  reports and unattributed `after` left untouched. Recorded at
  `.ufo/waves/round-66/misroot-disposition-r66.txt`.
- This is local bounded repair, not fleet novelty: connector cites
  kumitate NO_CHILD, tsukuroi could-not-evaluate and tameshi ARM_DEAD.
  Current route-table drift is recorded, not silently overridden.
  Closure owns admission and any trade/no-harm judgment.

### Round 67 — register citation binding and the landing control set

- Claims (frozen at `061dc329`): C1 calibration, the returned-host register must cite the live
  receipt inside a table row's receipt cell (r66 tree-level check accepted an unreferenced live
  object; the r66 counter scores 4/6 on the frozen six cases, the r67 counter 6/6); C2 operability,
  the standing landing instrument's selftest must kill the zero-citation guard clause and a child's
  `GIT_NO_REPLACE_OBJECTS` (candidate harness at the base 0/2, at the cutover 2/2). Pre-freeze
  control baseline committed at `aa7fe5a1` (`control-baseline-r67.txt`); no target is reachable by
  doing nothing.
- Instruments: new `quality/counters/c1-r67-register.py` (git-object reads only, row-local receipt
  resolution, exact committed live line, 16-case hermetic selftest) and
  `quality/counters/c2-r67-landing-controls.py` (extracts the instrument at `--rev`, runs its
  selftest, builds M-Z and M-R in scratch, prints mutant digests; 47-case hermetic selftest). The
  standing `quality/landing-counters.sh` gains one zero-citation selftest case (62/62); the three
  git-reading children (`c3-r56-used-by.py`, `check-tool-ledger.py`, `mado-receipt-citecheck.py`)
  set the replacement-object guard themselves — the r66 parent export never reached the two that
  rebuild env. Cutover `5f9ce459803dc17aceb16a6f8507006b85737c35`; two ledger rows added in the same commit (critic B2).
- Knowledge: `corpus/knowledge/replace-ref-citation-boundaries-r67.md` (blob vs tree/commit
  replacement levels, presence-not-truthiness of `GIT_NO_REPLACE_OBJECTS`, the lane reader census,
  what the R control does not prove), one new source `S436` (git v2.56.0 `git-replace.adoc`,
  tag-pinned, three independent fetches), QUALITY 109, SKILL gate rows and a bold PROVINCE
  refinement paragraph. No desktop surface, no PROVINCE frontier move. Assimilation none: the
  `merge/mado/` package has no fit and its staged ids collide 94/147 with the lane registry
  (connector screen).
- Evidence: one v1 wave, 13 seats (executor 4, scribe 2, scout 2, connector 1, reviewer 2,
  critic 1, mutation-tester 1; attack 4/13; L1 holds the planner seat), settled 13/13
  (`wave-done-r67.txt`). Measured at `caf131d6be04dd2ccc742636625c1ce196610522`, receipts committed at `2447048be5467ca0e35928d80aa99c90523a6739`:
  C1 `controls=6/6 register=accept TARGET_MET` rc 0; C2 `selftest=0 killed=2/2 TARGET_MET` rc 0;
  landing GREEN at the default round-67 scope; gate 460/460; census exit 0 rows 372 -> 373.
- Residuals, stated not smoothed: C1's row-count guard is an equivalent mutant; the M-Z kill is
  overdetermined by two structural assertions beside the behavioural case; a harness self-mutant
  (`mr_killed = True`) survives its selftest; the M-R child is landing-path-protected by
  inheritance and is vulnerable only standalone (critic B1); the citecheck tool invoked alone still
  reports `TARGET_MET` at `citations=0`; replacement refs do not prove authenticity and a repo
  already rewritten is not repaired. The critic's B3 (block-wide unresolved-receipt regression) was
  repaired at integration with 0 frozen-verdict changes; B5/B6/B7/B9 are recorded as wording/label
  disclosures in the lesson.
- Critic closures (`R69CriticClaims`, B1-B11) — dispositions in SCORECARD § Closure corrections:
  B2 fixed (the base leg must apply all three recipes or the counter refuses; selftest 28/28),
  B3 mitigated (two dominance regression cases in the counter's own selftest; the mutant now dies
  39/41), B8/B9/B11 corrections applied to the SCORECARD, B4/B5/B6/B7/B10 disclosed, B1 disclosed
  as the instrument's limit (a substitute harness can score the target; the delivered harness is
  the r68 measurement body plus the paired cases). Receipt `critic-closures-r69.txt`.
- Final measurement at `759c9d7b0d81ed0d6457b0b83e5f7e05b46abe3d` (`measurement-final-r69.txt`):
  C1 `selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0; C2 `population=20
  readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET` rc 0.
- Wave settlement: 12 seats dispatched, 12 settled, no dead seats (`w1-results.json`).
- Tooling: none installed or upgraded; no pacman transaction (host pause respected). The
  considerThese 2026-10-28 proposal 2 was executed once at the pre-r67 tip: gate exit 1,
  `files=33466 findings=280`, `waived 49/47`, the r37/r38 socket tables carry 5 and 715 proc rows —
  routed to L0 as an operator history/redaction decision, not repaired here.


## Round 68 (2026-11-03) — self-credit control and the guarded gate population

- Claims frozen at `e0727cda15621766c35dcf8b70c211b6531aab45` (declaration
  `.ufo/waves/round-68/claims-declaration-r68.md`; base `510100c8`): C1 calibration — the control
  harness must kill its own forged kill credit under three frozen single-point recipes, base 0/3;
  C2 operability — the standing `quality/check-*.py` gate population must read git objects through
  an environment carrying `GIT_NO_REPLACE_OBJECTS`, base 1/13, population 20 and 13 readers frozen
  in the target.
- Instruments: `quality/counters/c1-r68-landing-controls.py` (successor harness; `--selftest`
  drives the real `measure()` body with scripted children, 52/52), `c1-r68-selfmutants.py` (three
  recipes against the candidate and the pinned r67 harness; 26/26 selftest), and
  `c2-r68-reader-guard.py` (AST census over the gate population plus the eleven-case control set;
  25/25 selftest). Twelve gates gained the guard: anchor-cover, axis-scores, control-receipts,
  deliverables, evidence-pointers, freeze-order, index, index-rows, landed-contract,
  round-outcome-first, session-material, wave-done.
- Measured at `379e97f884a6cf7ed3ac96068b0165d63495524f`: C1 `selftest=0 killed=3/3 applied=3/3
  base=0/3 TARGET_MET` rc 0 (base-scored r67 harness survives all three, 47/47); C2
  `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 TARGET_MET` rc 0. Landing GREEN
  (nav 80/80, used-by 374 rows missing=0, ledger 113/113, citations 11/11); gate selftest 460/460;
  CHECK107 rows=8 covered=8. Receipts: `.ufo/waves/round-68/measurement-final-r68.txt`,
  `measurement-selftests-r68.txt`, `control-baseline-r68.txt`.
- Two counter defects were caught by attack seats and repaired before landing, each with a
  red-before receipt: the declared C2 command passed an argument the counter did not accept
  (`c2-command-erratum-r68.txt`, rc 2 → rc 1) and the C2 verdict did not enforce the frozen
  population/reader counts, so a verb-deleted gate scored TARGET_MET (`c2-denominator-erratum-r68.txt`,
  readers=12 TARGET_MET rc 0 → TARGET_MISSED rc 1). Mined as lessons M68-3/M68-4; QUALITY 110 added.
- Knowledge: `corpus/knowledge/gate-git-read-guards-r68.md` (MADO-R68-1; object-read verb family,
  the four accepted and three rejected guard constructions, the population boundary, the
  dominance hazard) with eight S437 evidence rows; one new source S437 (git v2.56.0
  `git-cat-file.adoc`, tag-pinned, three byte-identical fetches) and one in-place cell change:
  S436 `used-by` gains the new entry (logged old→new in the lesson Gate). SKILL r68 gate rows,
  PROVINCE instrument paragraph, QUALITY 110.
- Wave w1: 12 seats (executor 4, scribe 2, scout 1, connector 1, reviewer 2, critic 1,
  mutation-tester 1), 4/12 attack, one batch under policy v1 band 8-16; seat reports under
  `.ufo/waves/round-68/w1/`. The L1 holds the planner seat. No dead seats in the settled set at
  the time of this entry (results in the wave handoff).
- Disclosed, not smoothed: RevC1 survivors (drop the `forged_credit` term, credit `mz_rc is None`,
  remove the hermeticity guard) and multi-edit forgeries; RevC2's value-position over-inclusion
  and the connector's guard-dominance variant (reads forged bytes while classified guarded;
  `aux-dominance-r68.txt`). The guard is presence-tested, does not authenticate objects and does
  not protect an already-rewritten repository. No universal fault-coverage claim.
- Critic closures (`R69CriticClaims`, B1-B11) — dispositions in SCORECARD § Closure corrections:
  B2 fixed (the base leg must apply all three recipes or the counter refuses; selftest 28/28),
  B3 mitigated (two dominance regression cases in the counter's own selftest; the mutant now dies
  39/41), B8/B9/B11 corrections applied to the SCORECARD, B4/B5/B6/B7/B10 disclosed, B1 disclosed
  as the instrument's limit (a substitute harness can score the target; the delivered harness is
  the r68 measurement body plus the paired cases). Receipt `critic-closures-r69.txt`.
- Final measurement at `759c9d7b0d81ed0d6457b0b83e5f7e05b46abe3d` (`measurement-final-r69.txt`):
  C1 `selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0; C2 `population=20
  readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET` rc 0.
- Wave settlement: 12 seats dispatched, 12 settled, no dead seats (`w1-results.json`).
- Tooling: none installed or upgraded; no pacman transaction (host pause respected).

### Round 68 — closure addendum (critic blockers)

- `R68CriticClaims` filed B1-B7 after the wave settled. B1 (frozen `controls=11/11` unenforced by
  the C2 verdict) and B5 (`CONTRACT_RE` never checked on the emitted line) are instrument fixes:
  `verdict_met()` now requires `controls_total == 11` (M68-6), both `measure()` bodies `fullmatch`
  the assembled contract line and fail closed. B4 corrected the C1 docstring token to
  `applicable=no`. B3 renumbered the duplicated `M68-3` row before closure. B2 is an append-only
  erratum (`axis-posture-erratum-r68.txt`: 78/78 -> 79/79, 108/108 -> 110/110, N=3 citation).
  B6 restates the dead-guard limit (the census counts construction, not wiring; one gate carries
  a runtime hazard receipt) and B7 records that the scored harness is the L1's instrument,
  committed 8 s after the dispatch marker. No frozen predicate changed; the claims re-measured
  green after the fixes (C1 selftest 27/27, C2 26/26).

### Round 69 — the paired-recipe control harness and the guard-dominance census (2026-11-03, hyaku run 15)

- Two frozen claims, declared before any candidate data: C1 calibration (the hardened control
  harness kills paired decision+oracle forgeries; three frozen recipes R1 crash-≠-kill, R2
  unparseable-≠-kill, R3 spawn-guard-itself) and C2 operability (the guard census requires the
  key in key position and requires it to reach a git launch by one of three dominance flows).
  Declaration and control set landed at the freeze `789a87f1a667b43dd759222a2f048bf8f75b43ce`;
  base `04093b83f73a841117d3b31dbb2a6063f4f2a454`.
- Pre-freeze do-nothing controls, committed in the freeze: the r68 harness under the same three
  recipes survives 0/3 kills; the r68 classifier scores `7/11` on the frozen eleven cases.
  Receipt `.ufo/waves/round-69/control-baseline-r69.txt` (includes the recipe-L equivalence
  probe: `mz_killed = mz_rc != 0 or mz_rc is None` is an equivalent mutant).
- Wave w1: one v1 wave, 12 seats under `ufo-wave-policy.json` band 8–16 — executor 4, scribe 2,
  scout 1, connector 1, reviewer 2, critic 1, mutation-tester 1; 4/12 attack (33 %); the L1 holds
  the planner seat (the validator rejects a planner role). Spec `.ufo/waves/round-69/w1-spec.json`,
  validated dispatch `.ufo/waves/round-69/w1-dispatch.json` (`spawn=12`), ready
  `98bff016d0ef151aceedf03d75239b81c9f6eeed`. Seat reports under `.ufo/waves/round-69/w1/`.
- Instruments at `5fc29ae7`: `quality/counters/c1-r69-landing-controls.py` (r68 body, paired
  selftest), `quality/counters/c1-r69-paired-recipes.py`, `quality/counters/c2-r69-guard-dominance.py`.
- Attack outcomes, both closed before landing (no predicate changed):
  - `R69RevC2` found six bounded defects against the frozen C2 sentence (dead inline construction,
    producer overwrite/late guard, nested key in value, sibling-scope leakage, one-hop parameter
    mismatch, dead-else false negative). Repaired at `6d21f535492f74dfef538eecb303486a1588c1be`;
    receipt `c2-classifier-repair-r69.txt` (pre-fix 7 violations → post-fix 8/8 cases; frozen
    controls and the 20/13/13 population unchanged; selftest 40/40 with the six cases pinned).
  - `R69RevC1` found S1 (an absent base harness read `base=0/3` and printed TARGET_MET), S2 (no
    compile gate before crediting a kill), S3 (a hung child crashed with no contract line),
    S4 (stale `r68` self-description and scratch-dir names), S5 (`--base-rev` silently defaulted).
    Repaired at `296ed0d75e361387908cf2dd418d3677f49f94c8`: the base harness is required and its
    absence is a setup error; mutants are `py_compile`-checked before a kill is credited; the main
    body catches `OSError`/`SubprocessError` and exits 2 with a reason; the seat's harness draft
    (sha256 `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73`) is adopted, with
    `r69-c1` scratch dirs and the round-69 limits paragraph. Selftest 27/27 (two assertions pin
    the new refusals).
- Mutation battery (`R69MutBattery`): nine C1-counter and six C2-counter single-point mutants; every
  one killed by its counter's own selftest except the base-rev-ignoring C1 mutant (`base_sha = sha`),
  which survived because the scripted `git show` could not tell the two revisions apart. Closed at
  `e0e1831a` by separating the scripted revisions (the mutant now dies with the base-absent refusal);
  the C2 `population_at`/`unguarded` arithmetic findings are disclosed as residuals (the frozen
  verdict requires `population=20`, `readers=13`, `guarded=13`, so neither can forge a pass).
- Measured at `e0e1831a` (`measurement-final-r69.txt`): C1 `selftest=0 killed=3/3 applied=3/3
  base=0/3 verdict=TARGET_MET` rc 0; C2 `population=20 readers=13 guarded=13 unguarded=0
  controls=11/11 base_controls=7/11 verdict=TARGET_MET` rc 0. First measurement at `296ed0d7`
  (`measurement-r69.txt`) reads the same two lines; C1 `selftest=0 killed=3/3 applied=3/3 base=0/3
  verdict=TARGET_MET` rc 0; C2 `population=20 readers=13 guarded=13 unguarded=0 controls=11/11
  base_controls=7/11 verdict=TARGET_MET` rc 0. Before: C1 `selftest=absent … TARGET_MISSED` rc 1;
  C2 the held rule's `7/11`.
- Knowledge: `corpus/knowledge/gate-guard-dominance-r69.md` (MADO-R69-1; key position, the three
  dominance flows, the four rejected shapes, the 20-file population by guard shape, the limits)
  with eight evidence rows S438/S436/S437; one new source **S438** (git v2.56.0 `git.adoc`,
  tag-pinned, fetched three times byte-identically) and the entry's index row + Frontier bullet.
  QUALITY 111 (a frozen recipe must change a printed observable; a guard must be a key that reaches
  the read) and the lesson's M69-1/M69-2/M69-3. SKILL gains the two gate rows; PROVINCE its
  round-69 instrument paragraph; `quality/tool-ledger.md` gains the three rows.
- Harm watch: `MADO_SELFTEST: 460/460` rc 0; axis table 3/3 MATCH at the records; landing counters
  GREEN with explicit citecheck paths (the first run's `rc 2` was a setup default, logged as
  M69-3); r68 counters keep their pinned bytes and selftests (27/27, 52/52, 26/26).
- Critic closures (`R69CriticClaims`, B1-B11) — dispositions in SCORECARD § Closure corrections:
  B2 fixed (the base leg must apply all three recipes or the counter refuses; selftest 28/28),
  B3 mitigated (two dominance regression cases in the counter's own selftest; the mutant now dies
  39/41), B8/B9/B11 corrections applied to the SCORECARD, B4/B5/B6/B7/B10 disclosed, B1 disclosed
  as the instrument's limit (a substitute harness can score the target; the delivered harness is
  the r68 measurement body plus the paired cases). Receipt `critic-closures-r69.txt`.
- Final measurement at `759c9d7b0d81ed0d6457b0b83e5f7e05b46abe3d` (`measurement-final-r69.txt`):
  C1 `selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0; C2 `population=20
  readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET` rc 0.
- Wave settlement: 12 seats dispatched, 12 settled, no dead seats (`w1-results.json`).
- Tooling: none installed or upgraded; no pacman transaction (host pause respected).

### Round 70 — the real-children kill credit and the guard carrier set (2026-11-04, hyaku run 15)

- Claims frozen at `bc18399b` before any candidate data: C1 **calibration** (the landing harness
  credits a kill only on a parsed failed assertion, proven with real children) and C2 **operability**
  (the guard census counts alias, attribute, `**`-splat and constant-key carriers while keeping the
  git-launch negatives). Declaration `.ufo/waves/round-70/claims-declaration-r70.md`; control set
  `.ufo/waves/round-70/controls/c2-controls-r70.json` (17 cases, sha256 `29947b4c…`); pre-freeze
  controls `.ufo/waves/round-70/control-baseline-r70.txt` (held harness `1/3`, held classifier
  `13/17`). Base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`.
- C1 instruments: `quality/counters/c1-r70-landing-controls.py` (successor harness; M-Z credit =
  nonzero exit AND a parsed `MADO_LANDING_COUNTERS_SELFTEST: p/n` with `p < n`) and
  `quality/counters/c1-r70-real-children.py` (three real `bash` children in a scratch git fixture:
  genuine failure / crash with no summary / garbled summary; candidate 3/3, held harness 1/3).
  The first committed counter (`5144a6b5`) died mid-measurement on a missing per-scenario scratch
  directory; repaired pre-data in `9508e878` (M70-1, criterion 110(a)).
- C2 instrument: `quality/counters/c2-r70-carriers.py` (round-69 key position and dominance flows
  plus four carriers; 17-case frozen set with the eleven held cases carried forward byte-identically
  and asserted at `--rev`). Review (`R70RevC2` blockers 1–2) showed attribute carriers bypassing
  dominance and a locally shadowed constant key still counting; repaired against the same frozen
  sentence in `6a25e865` (attribute store-before-use with no intervening replacement; scope-filtered
  constants), red-before → green-after in `c2-classifier-repair-r70.txt`, with the five attack cases
  pinned in the selftest (54/54) and the two disclosed limits (`dict(**GUARD)`, two-hop alias) held
  at `(True, False)`.
- Measured at `3d28f92a` (`measurement-r70.txt`): C1 `cases=3 correct=3 base_correct=1
  verdict=TARGET_MET` rc 0; C2 `population=20 readers=13 guarded=13 unguarded=0 controls=17/17
  base_controls=13/17 verdict=TARGET_MET` rc 0. Before: both counters absent at the base rev, the
  held harness `1/3` and the held classifier `13/17` on the same sets.
- Knowledge: `corpus/knowledge/landing-kill-credit-real-children-r70.md` (MADO-R70-1) and
  `corpus/knowledge/guard-carrier-shapes-r70.md` (MADO-R70-1), three new source rows **S439**
  (expressions.rst, `**` unpacking), **S440** (simple_stmts.rst, subscription assignment) and
  **S441** (rendered subprocess docs, `CompletedProcess.returncode`), plus the S435 `used-by`
  reverse link; index rows and the Round 70 Frontier bullet. QUALITY **112** (append-only record
  order and commit-list completeness, from the round-69 spot-check defects 1–2) and **113** (a kill
  credit rests on a parsed failed assertion, and its real-children leg uses real child processes).
  Lesson `corpus/lessons/round-70.md` with M70-1…M70-5 and the Gate block (three admits, two
  rejects).
- Harm watch (`harm-watch-r70.txt` at `40709300`): gate `MADO_SELFTEST: 460/460` rc 0; the frozen
  round-69 counter `killed=3/3 applied=3/3 base=0/3 TARGET_MET` rc 0 (its harness file is
  byte-identical to the base); landing instrument GREEN with all four legs (`nav=0 usedby=0
  ledger=0 citecheck=0`) on the round's committed record files; axis table `checked=3 mismatched=0`
  (navigation 83/83, calibration 86/86, operability 12/12); ledger 119/119 uncovered=0; every
  instrument selftest green (68/68, 26/26, 54/54, 43/43, 59/59).
- Wave: ONE v1 wave, 14 seats (executor 4, scribe 3, scout 2, reviewer 2, critic 1,
  mutation-tester 1, connector 1; attack share 4/14), all 14 settled, no dead seats; dispatch
  `w1-spec.json`/`w1-dispatch.json`/`w1.ready` committed as evidence, seat reports under
  `.ufo/waves/round-70/w1/`.
- Disclosures (SCORECARD § Closure corrections, errata E1–E6): review blockers R1–R8; declaration
  errata for the stale seat count (14, not 13), the harm-watch command form, the C2 base-leg
  vehicle, C1's substituted source, C2's two-document sentence, and the mislabelled base evidence
  line. Predicates, targets, counters and kill rules unchanged.
- Tooling: none installed or upgraded; no pacman transaction (host pause respected). No desktop,
  compositor, service or session probe this round.
- Final integration `5a7af0fb`: WAVE-DONE and all 14 outputs, corrected the expressions locator
  to 514–517, removed a wrong HTML-line pin for held S435 (its texi locator is not an HTML line),
  and added standing SKILL/PROVINCE guidance. Final anchor checks are 2/2 and 2/2, census exit 0,
  and origin/master matches the pushed hash (`final-record-checks-r70.txt`).
  Fleet-root misroot sweep found only shared/operator changes and unattributed sibling artifacts;
  no mado round-70 misroot was identified or removed.

### Round 71 — the exit-status-disagreement kill credit and the four carrier shapes (2026-11-04, hyaku run 15)

- Claims frozen at `4a91c644` before any candidate data: C1 **calibration** (the landing
  harness credits a kill on the parsed failed assertion whatever the child's exit status) and
  C2 **operability** (the guard census counts the dict-call splat, the splat-through-alias, the
  store-through-alias and the attribute-through-second-object shapes). Declaration
  `.ufo/waves/round-71/claims-declaration-r71.md`; control set
  `.ufo/waves/round-71/controls/c2-controls-r71.json` (23 cases, sha256 `d7814de8…`); pre-freeze
  do-nothing controls `control-baseline-c1-r71.txt` (held harness `3/4`, missing `liar-success`
  only) and `control-baseline-c2-r71.txt` (held classifier `19/23`, missing exactly the four
  carriers). Base `c354f4d410b829d985b31560af9202d98655dad0` — which itself first commits the
  round-70 seat-report leftovers the closure routed (spot-check defect 1, criterion 114).
- C1 instruments: `quality/counters/c1-r71-landing-controls.py` (successor harness;
  `mz_killed = summary_shows_failure(out)` — the exit status no longer gates the credit) and
  `quality/counters/c1-r71-real-children.py` (four real `bash` children: liar-success /
  stderr-genuine / liar-kill / crash-stderr; candidate 4/4, held harness 3/4). Harness selftest
  70/70; counter selftest 27/27. The reviewer verified the sole behavioural delta is the
  dropped conjunct and that the combined-stream reader is the only one scoring 4/4
  (`w1/R71RevC1.md`; its F1–F6 findings are disclosed limits, not blockers).
- C2 instrument: `quality/counters/c2-r71-shapes.py` (held round-70 rule + four carriers,
  23-case frozen set with the seventeen held cases carried byte-identically; selftest 63/63).
  The wave's reviewer falsified the first widening (`w1/R71RevC2.md` F1 HIGH: splat-alias
  rebind before the splat; F2 MEDIUM: object-alias edge bound after the call); repaired
  against the frozen sentence at `3868bc65` with the red-before/green-after receipt
  `.ufo/waves/round-71/c2-dominance-repair-r71.txt`, both repro sources pinned as counter
  regressions, and the frozen 23 scoring identically before and after (re-run receipted in
  `measurement-r71.txt`). No production file is reclassified: the per-file census stays
  20 / 13 / 13 / 0.
- Frozen counting commands run verbatim at `8e78a4ee` (instruments) and re-run at `3868bc65`
  (repair): `MADO_R71_REAL_CHILDREN: cases=4 correct=4 base_correct=3 verdict=TARGET_MET` rc 0
  and `MADO_R71_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=23/23
  base_controls=19/23 verdict=TARGET_MET` rc 0 (`.ufo/waves/round-71/measurement-r71.txt`).
- Curation: SOURCES 378 → 380 rows (S442 supersedes S108 for the run() capture_output scope;
  S443 supersedes S439 for the § Calls `**` scope; both fetched three times byte-identical to
  the held pins, fetch receipts committed; stdtypes.rst screened and rejected). Two knowledge
  entries admitted (`corpus/knowledge/kill-credit-exit-disagreement-r71.md`,
  `corpus/knowledge/guard-carrier-shapes-r71.md`), README index 83 → 85 rows plus the round-71
  frontier bullet, PROVINCE round-71 refinement, tool-ledger 119 → 122 rows, QUALITY criteria
  114–115 registered from M71-1/M71-4 (`corpus/lessons/round-71.md` `## Mistakes`,
  `## Gate`).
- Wave: one v1 wave of 13 seats (executor 3, scribe 3, scout 2, reviewer 2, critic 1,
  mutation-tester 1, connector 1; attack share 4/13 = 30.8%) validated under the band-8–16
  policy and dispatched through the inline spawn handoff; all 13 settled `status: ok`, zero
  dead; **11 seats returned empty outputs and wrote no files** — an evidence gap disclosed
  per QUALITY 115, with the two reviewer reports carrying the round's independent attack
  evidence (M71-4). No counter binds seat votes, so no frozen result depends on the missing
  seats.
- Standing-instrument repair (routed defect 2, M71-2): red-before receipt
  `m71-2-red-before-r71.txt` (the `--round 70` default dies as a setup error) and the repair —
  this round commits its receipts at `.ufo/waves/round-71/receipts/` so the `--round 71`
  default resolves committed bytes; the landing-time GREEN default run is receipted in
  `.ufo/waves/round-71/harm-watch-r71.txt`. Routed defect 3 (r69 deliverable-citation reds)
  stays observed-not-repaired: it belongs to a round-69 correction entry.
- Harm watch at the landing tip: gate `MADO_SELFTEST: 460/460`; the frozen round-70 counters
  stay TARGET_MET (`cases=3 correct=3 base_correct=1`, `controls=17/17 base_controls=13/17`);
  axis table `checked=3 mismatched=0`; navigation 85/85; ledger 122/122; landing GREEN with
  the `--round 71` default path (`.ufo/waves/round-71/harm-watch-r71.txt`,
  `.ufo/waves/round-71/receipts/`). No config tree, compositor, service or sibling repo was
  written; no pacman transaction; no tool installed or upgraded.

### Round 72 — the summary's own detail and the outcome's own report (2026-11-04, hyaku run 15)

- Claims frozen at `5601e526` before any candidate data: C1 **calibration** (the landing kill
  credit requires the run's own failure detail, `n > 0` and `p < n` plus `SELFTEST FAIL` count =
  `n − p`) and C2 **operability** (the contract outcome reads the extracted instrument's last
  parsed summary, not its exit status). Declaration
  `.ufo/waves/round-72/claims-declaration-r72.md`; control sets
  `.ufo/waves/round-72/controls/c1-modes-r72.json` (sha256 `18144745…`) and
  `c2-controls-r72.json` (sha256 `640fb44f…`); pre-freeze do-nothing controls
  `control-baseline-c1-r72.txt` (held 6/8) and `control-baseline-c2-r72.txt` (held 4/8). Base
  `976684a27e99c2508037a60eec415f550f53d70e` (lane clean: `tracked=0 untracked=0`).
- Instruments: `quality/counters/c1-r72-landing-controls.py` (round-71 generation plus the two
  disjoint rule deltas `credit()` and `summary_green()`/`outcome_verdict()`; selftest 83/83),
  `quality/counters/c1-r72-summary-credit.py` (eight real `bash` fixture modes: the four
  round-71 scenarios carried unchanged plus `bare-failing`, `mismatch-detail`, `last-wins-pass`,
  `last-wins-fail`; selftest 33/33) and `quality/counters/c2-r72-outcome.py` (eight frozen
  `(gate_out, gate_rc, killed)` cases; hermetic selftest 24/24). Frozen rounds 68–71 untouched:
  `git rev-parse` shows identical blob ids for `c1-r71-landing-controls.py`,
  `c1-r71-real-children.py`, `c2-r71-shapes.py`, `tools/mado-verify.sh` and
  `quality/landing-counters.sh` at base and tip.
- Frozen counting commands run verbatim at `9bcb4fd5`: `MADO_R72_SUMMARY_CREDIT: cases=8
  correct=8 base_correct=6 verdict=TARGET_MET` rc 0 and `MADO_R72_OUTCOME: cases=8 correct=8
  base_correct=4 verdict=TARGET_MET` rc 0 (`.ufo/waves/round-72/measurement-c{1,2}-r72.txt`).
  The do-nothing controls miss exactly the declared shapes: the held harness credits
  `bare-failing`/`mismatch-detail`, and the held outcome is wrong on four cases in both
  directions.
- Curation: SOURCES 380 → 383 rows — S444 (CPython 3.14.8 `Doc/library/unittest.rst`,
  `wasSuccessful()`), S445 (`Lib/unittest/main.py`, the runner's exit derivation from
  `wasSuccessful()`), both `mined` and cited by `corpus/knowledge/outcome-verdict-gate-summary-r72.md`;
  S446 is the round-71 reject curated as a `rejected` row at its real 3.14 path
  (`Doc/builtins/stdtypes.rst`; the r71 citation `Doc/library/stdtypes.rst` 404s, curl rc 22 ×3).
  Fetches three times byte-identical each (`.ufo/waves/round-72/fetch/`). S442's `used-by` gained
  the round-72 C1 entry (old→new logged in `corpus/lessons/round-72.md` § Gate). Census
  `scripts/sources-census.sh validate` exit 0 at start (380) and end (383).
- Knowledge: two entries admitted (`corpus/knowledge/summary-credit-own-detail-r72.md`,
  `corpus/knowledge/outcome-verdict-gate-summary-r72.md`); README index 85 → 87 rows plus the
  round-72 Frontier bullet; PROVINCE round-72 refinement; QUALITY criteria 116–117 registered
  from `corpus/lessons/round-72.md`; the four r71 routed/conformance defects repaired or
  curated (reject row S446, the 404 anchor, the quote word count, the harm-watch rc wording).
- Registry: `quality/tool-ledger.md` 122 → 125 rows (harness + two counters); the `SKILL.md` Gate
  registry gains four rows — the r71 and r72 counters (the r71 routed defect that neither r71
  counting instrument was registered).
- Wave: one v1 wave of 13 seats (executor 3, scribe 3, scout 2, reviewer 2, critic 1,
  mutation-tester 1, connector 1; attack share 4/13 = 30.8%) validated under the band-8–16 policy
  and dispatched through the inline spawn handoff; seat outcomes are reported per seat in the
  round report (QUALITY 115).
- Harm watch at the landing tip: gate `MADO_SELFTEST: 460/460`; index 87/87; ledger 125/125
  `uncovered=0`; axis table re-derived (navigation 87/87, calibration 86/86, operability 12/12);
  census exit 0; frozen instrument blob ids unchanged (`.ufo/waves/round-72/receipts/harm-watch-r72.txt`).
  No config tree, compositor, service or sibling repo was written; no pacman transaction; no
  tool installed or upgraded.
- Review-driven repair at `4f598cfd` (this entry, appended): the successor harness now
  implements "last parsed summary" literally (a malformed trailing marker cannot suppress the
  last parseable one) and counts only the production fail grammar `SELFTEST FAIL <i>: ` —
  both from the wave's `R72RevC1` F1/F2 and `R72CriticClaims` Counterexample B, with the
  red-before/green-after receipt `.ufo/waves/round-72/receipts/c1-r72-repair.txt` and the
  frozen eight-case sets re-scored identically (`re-measure-r72.txt`: 8/8 vs 6/8 and 8/8 vs
  4/8). The declaration carries an append-only erratum naming the stream-precedence limit and
  the finite-set statements; no predicate, control or target changed.
- Wave settlement (this entry, appended): all 13 seats settled with delivered files — the two
  reviewers (`R72RevC1`, `R72RevC2`), the critic and the mutation battery delivered real
  attacks; their findings drove the `4f598cfd` repair and the declaration erratum. The mutation
  battery's survivors are disclosed, not hidden: GAP-1 (`summary_green()` without the `n > 0`
  guard survives both frozen sets — no zero-denominator case) and GAP-2 (the counters'
  `score()` None-guard is vacuous on these sets — no absent candidate). Both become round-73
  controls under a new frozen denominator, never a widening of this round's.

### Round 73 — the control set as an instrument and two more guard carriers (2026-11-04, hyaku run 15)

- Claims frozen at `87e4c61a` before any candidate data: C1 **calibration** (the frozen outcome
  case set separates four named mutations of the round-72 outcome rule; the held eight-case set
  separates two) and C2 **operability** (the guard census counts the `global`-declared guard and
  the mutated-`os.environ` transport). Declaration `.ufo/waves/round-73/claims-declaration-r73.md`;
  control sets `controls/c1-outcomes-r73.json` (10 cases, sha256 `263b3c5a…`) and
  `controls/c2-cases-r73.json` (28 cases, sha256 `65e94644…`); pre-freeze do-nothing receipts in
  `control-baseline-r73.txt` (held set killed 2/4; held classifier 25/28). Base
  `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce` (lane clean: `tracked=0 untracked=0`).
- Instruments: `quality/counters/c1-r73-summary-mutants.py` (extracts the round-72 harness at
  `--rev`, asserts the r72 eight-case set is carried byte-identically, applies four named literal
  mutations exactly once each — the dropped `n > 0` guard, the pre-repair prefix-match parse, the
  relaxed comparison, the kill-count-only outcome — and scores each on the ten-case and held
  eight-case sets; selftest 25/25) and `quality/counters/c2-r73-shapes.py` (the round-71 classifier
  plus `global_guard` and `environ_transport_guard`, 28 frozen cases, population unchanged;
  selftest 75/75). Frozen rounds 70–72 untouched: identical blob ids at base and at the instrument
  commit.
- Frozen counting commands run at `1459cca11fb5d3956a6e9a128217852dd0c28cb9`:
  `MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET` rc 0 and
  `MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=28/28
  base_controls=25/28 verdict=TARGET_MET` rc 0 (`.ufo/waves/round-73/measurement-c{1,2}-r73.txt`).
- Curation: SOURCES 383 → 386 rows — S447 (CPython 3.14.8 `Doc/reference/simple_stmts.rst`, the
  `global` statement), S448 (`Doc/library/os.rst`, `os.environ`), S449 (`Doc/library/subprocess.rst`,
  the `run` `env` paragraph; S442's document at a separate scope), all `mined` and cited by
  `corpus/knowledge/guard-carrier-global-environ-r73.md`. Fetches three times byte-identical each
  (`.ufo/waves/round-73/fetch/`); the census prints S449's documented W04 duplicate-URL warning
  across scopes.
- Knowledge: two entries admitted (`corpus/knowledge/control-set-mutant-kill-r73.md`,
  `corpus/knowledge/guard-carrier-global-environ-r73.md`); README index 87 → 89 rows plus the
  round-73 Frontier bullet; PROVINCE round-73 refinement; QUALITY criteria 118–119 registered from
  `corpus/lessons/round-73.md` `## Mistakes`.
- Registry: `quality/tool-ledger.md` 125 → 127 rows; the `SKILL.md` Gate registry gains two rows
  (`mado-r73-mutant-kill`, `mado-r73-guard-shapes`).
- Conformance repair: the declaration's §C1 printed command omitted `--controls` (the counter
  exits 2 on it); found by the wave's `R73RevC1` before the report and repaired as append-only
  erratum E1; logged as M73-1 and pinned by QUALITY 118.
- Wave: one v1 wave of 13 seats (executor 3, scribe 3, scout 2, reviewer 2, critic 1,
  mutation-tester 1, connector 1; attack share 4/13 = 30.8%) validated under the band-8–16 policy
  and dispatched through the inline spawn handoff; seat outcomes are reported per seat in the round
  report (QUALITY 115).
- Harm watch at the landing tip: gate `MADO_SELFTEST: 460/460`; index 89/89; ledger 127/127
  `uncovered=0`; axis table re-derived; census exit 0; frozen instrument blob ids unchanged
  (`.ufo/waves/round-73/receipts/harm-watch-r73.txt`). No config tree, compositor, service or
  sibling repo was written; no pacman transaction; no tool installed or upgraded.
- Review-driven repair at `84fc266a` (this entry, appended): C1's `--base-rev` is now resolved and
  refuses a base/candidate harness difference (red-before: the old counter printed the contract line
  for `--base-rev NO_SUCH_BASE_R73`, rc 0; green: exit 2 with the reason, rc 0 with the real base) and
  the usage example names `--controls`; C2 refuses a shadowing launch binding, restricts cancellation
  to module-resolving bindings and treats `del os.environ[KEY]` as a cancellation — the reviewers'
  three fixtures flip as named in `.ufo/waves/round-73/receipts/repair-r73.txt`, three regressions pin
  the repairs, selftests 26/26 and 78/78. Both claims re-measured at the repair commit with identical
  counts (`measurement-c{1,2}-r73.txt`); no predicate, control label, kill rule or target changed.

### Round 74 — the rule's own witness and two more guard carriers (2026-11-04, hyaku run 15)

- Claims (both frozen before any candidate data in `.ufo/waves/round-74/claims-declaration-r74.md`,
  landed with the instruments at `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`, base
  `bd5a971532f37df85a78f6f566dd1e649b79de11`): **C1 calibration** — the landing kill credit
  requires the run's own echo of a caller-generated per-run challenge, closing the round-71/72/73
  declared replay limit on the rule; **C2 operability** — the guard census counts a one-hop object
  alias stored at one dotted spelling and handed at the other, and a one-hop `os.environ` alias
  whose store reaches `env=alias`, `dict(alias)` or `{**alias}`.
- Instruments: `quality/counters/c1-r74-witness-rule.py` (`credit(out, nonce)`, hermetic selftest
  21/21), `quality/counters/c1-r74-replay-witness.py` (twelve real `bash` children, a fresh
  `secrets.token_hex(8)` challenge per run, the held round-72 `credit` as the control; selftest
  21/21) and `quality/counters/c2-r74-shapes.py` (the round-73 classifier plus `twohop_guard` and
  `environ_alias_guard`; selftest 86/86). Frozen control sets:
  `.ufo/waves/round-74/controls/c1-replay-cases-r74.json` (12 cases, sha256 `17c95774…`) and
  `c2-cases-r74.json` (36 cases, sha256 `4db4cc70…`, the round-73 twenty-eight carried
  byte-identically).
- Pre-freeze do-nothing receipt `.ufo/waves/round-74/control-baseline-r74.txt`: the held round-72
  credit scores 8/12 and the held round-73 classifier 32/36 — both below their targets before the
  freeze. Mistake red states: `receipts/m74-1-red.txt` (a fixture lane built without the harness
  mutation scores the held rule 9/12) and `receipts/m74-2-red.txt` (two draft case labels
  disagree with the held classifier).
- Frozen counting commands run at `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`:
  `MADO_R74_REPLAY_WITNESS: cases=12 correct=12 base_correct=8 verdict=TARGET_MET` rc 0 and
  `MADO_R74_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=36/36
  base_controls=32/36 verdict=TARGET_MET` rc 0 (`.ufo/waves/round-74/measurement-c{1,2}-r74.txt`).
- Curation: SOURCES 386 → 389 rows — S450 (CPython 3.14.8 `Doc/library/secrets.rst`, `token_hex`),
  S451 (`Doc/reference/simple_stmts.rst`, the attribute-reference assignment bullet), S452
  (`Doc/library/os.rst`, the environ mapping-modification paragraph) — all `mined` and cited by the
  two new entries; S452 supersedes S448's false digest (round-73 closure D1) with the re-derived
  `2d0f2892…b2ae5` (208,655 B, three byte-identical fetches). Re-opened reject S446 now carries its
  located quote (round-73 D5). Fetches three times byte-identical each
  (`.ufo/waves/round-74/fetch/`); the census prints the documented W04 warnings and exits 0.
- Knowledge: two entries admitted (`corpus/knowledge/replay-witness-credit-r74.md`,
  `corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md`); README index 89 → 91 rows plus the
  round-74 Frontier bullet; QUALITY criteria 118–119 appended to the canonical
  `corpus/QUALITY.md` (round-73 D4) and 120–121 registered from `corpus/lessons/round-74.md`
  `## Mistakes`; the root `QUALITY.md` fragment carries a redirect line.
- Registry: `quality/tool-ledger.md` 127 → 130 rows; the `SKILL.md` Gate registry gains three rows
  (`mado-r74-witness-rule`, `mado-r74-replay-witness`, `mado-r74-guard-shapes`).
- Wave: one v1 wave of 13 seats (executor 3, scribe 2, scout 2, reviewer 2, critic 1,
  mutation-tester 1, connector 1, sentinel 1; attack share 4/13 = 30.8%) validated under the
  band-8–16 policy and dispatched through the inline spawn handoff; seat outcomes are reported per
  seat in the round report (QUALITY 115).
- Harm watch: gate `MADO_SELFTEST: 460/460` (`receipts/gate-selftest-r74.txt`, the L1-run leg; the
  harm seat kept its stricter no-/tmp bound and recorded it as NOT RUN for itself); index 91/91;
  ledger 130/130 `uncovered=0`; axis table re-derived; census exit 0; five frozen instrument blob
  ids unchanged. No config tree, compositor, service or sibling repo was written; no pacman
  transaction; no tool installed or upgraded. Routed defect: `tools/mado-verify.sh:418` hardcodes a
  `/tmp` selftest scratch (scratch rule 4, next round's frozen-counter amendment).

- Review-driven repair at `4cfa5ddc` (this entry, appended): C1's witness grammar widened to the
  frozen "<16 hex>" with a byte-exact comparison and two new rule cases, and the counter now draws
  a fresh challenge per child; C2 refuses a launch whose parameter shadows the alias, counts
  `AnnAssign` bindings, and requires the alias edge to exist before the store; all three
  instruments refuse a scratch path with a symlinked component; the C2 selftest writes its tampered
  file with `O_NOFOLLOW`; the C1 child environment is allowlisted. Both claims re-measured at the
  repair commit with identical counts (`measurement-c{1,2}-r74-final.txt`), and the reviewers'
  fixtures flip as named in `SCORECARD.md` § Review-driven repair. Carried limits: the held
  attribute flow's root-name rebinding, the generic `del` gap, the two copy spellings, and the
  three mutants the frozen sets do not separate (C1-M4, C2-M3, C2-M4).

## Round 75 — the harness's own witness and two next carrier shapes (2026-11-04, hyaku run 15)

Base `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`; frozen declaration and instruments
`def73656c94f0e88bd671cfb4a65124338261722`; final measured content C1 `a3c88663…`, C2
`4527fcae…`. One v1 wave of 13 seats (executor 3, scribe 2, scout 2, reviewer 2, critic 1,
mutation-tester 1, connector 1, sentinel 1; attack share 4/13 = 30.8%; no dead seats).

- **C1 (calibration): witness credit wired into the landing harness.** The held round-72 harness
  credited the M-Z kill on arithmetic alone (6/11 on the frozen fixture modes). The successor
  `c1-r75-landing-controls.py` loads the frozen generation under a sha256 pin, draws one
  `secrets.token_hex(8)` challenge per run, hands it in `MADO_LANDING_NONCE`, and credits the kill
  and the outcome green only on the child's last parsed `MADO_LANDING_WITNESS: <16 hex>` echo;
  `c1-r75-harness-witness.py` scores eleven real `bash` fixture lanes through the actual pipeline:
  `cases=11 correct=11 base_correct=6 verdict=TARGET_MET` (bounded 10.0000 vs held 5.4545).
  `quality/landing-counters.sh` echoes a well-formed challenge (62/62 selftest unchanged).
- **C2 (operability): name-neutral keyed copies and literal-key delete.** `c2-r75-shapes.py` adds
  the two deltas on S453/S454 ground; `population=20 readers=13 guarded=13 unguarded=0
  controls=47/47 base_controls=41/47 verdict=TARGET_MET` (bounded 10.0000 vs held 8.7234).
- **Sources & frontier.** Registry 389 → 391 rows: S453 (`simple_stmts.rst` § del, 13-word quote
  at :468-469) and S454 (`builtins/stdtypes.rst` `dict(mapping, **kwargs)`, 21-word quote at
  :5350-5352), both `mined`, both different-scope W04 repetitions and neither a supersession; the
  S446 reject is re-opened with its quote count corrected 23 → 21 (round-74 D3). Census: round
  start (base mirror) exit 0, round end exit 0 (receipts `census-{start,end}-r75.txt`). Two
  knowledge entries admitted (`harness-witness-credit-r75.md`, `guard-carrier-copy-del-r75.md`);
  index 91 → 93.
- **Both claims measured against the do-nothing controls:** held 6/11 and 41/47, both below the
  targets; receipts `control-baseline-r75.txt` (pre-freeze) and `measurement-c{1,2}-r75-final.txt`.
- **Mistakes mined (7, `corpus/lessons/round-75.md` `## Mistakes`):** the declaration's
  self-contradictory no-harm line (M75-1), the hardening change that made the C1 counter score 0/11
  while its selftest passed (M75-2), the unreachable `del-before-store` fixture (M75-3), the
  probabilistic uppercase oracle (M75-4), the carried 21/21 stale tally (M75-5), the carried
  unlanded selftest receipts (M75-6) and the declaration's stale 12-seat planning line (M75-7).
  Four QUALITY criteria land from them (124–127).
- **Registry and gate bookkeeping.** `quality/tool-ledger.md` 130 → 133 rows; the `SKILL.md` Gate
  registry gains three rows (`mado-r75-harness-witness`, `mado-r75-landing-controls`,
  `mado-r75-guard-shapes`) and the `mado-r74-witness-rule` row is corrected 21/21 → 23/23 and
  reclassed `probe` (round-74 closure D1/D5).
- **No-harm and the one declared amendment.** Gate `MADO_SELFTEST: 460/460` at the amended bytes;
  the amendment honours `MADO_SELFTEST_SCRATCH`/`TMPDIR` (red-before: TMPDIR ignored at 460/460;
  green: refusal for a missing base, 460/460 for a valid one) and `PIN_MADO` is re-cut
  `367ff5ec…` → `49567a0f…`. Index 93/93; ledger 133/133 `uncovered=0`; axis table re-derived;
  census exit 0; `c2-r74-shapes.py` and the round-72/73 instruments keep their base blob ids. No
  config tree, compositor, service or sibling repo was written; no pacman transaction; no tool
  installed or upgraded.
- **Review-driven repair at `e3e29bb4`, `f75afbf6`, `4527fcae`, `b545bea9`, `a3c88663`** (this
  entry, appended): C2 counts `env=` only and skips dead-branch deletes; C1's loader writes into a
  private `O_NOFOLLOW` generation dir and creates the validated scratch root first; the held C2
  generation is pinned before execution and `/` is refused as scratch; the C1 child-env evidence
  redacts the live challenge; the gate scratch honours TMPDIR (pin re-cut); the C1 counter honours
  the absent-candidate contract (`correct=absent`, rc 1). Carried limits: C1-M2 (the counter scores
  `mz=` only), C1-M3 (prefix vs equality unobservable at 16 hex), the probabilistic uppercase
  oracle, the unreachable `del-before-store` fixture, concurrent trust of the scratch parent, and
  the frozen C2 receipt's stale "round-73 rule" label.

## Round 76 — the harness's outcome field and two deletion shapes (2026-11-04, hyaku run 15)

- **Claims.** C1 calibration: `quality/counters/c1-r76-outcome-field.py` scores the landing
  harness's contract **outcome** field (`verdict=`) as well as its kill decision (`mz=`), over
  sixteen frozen fixture modes; four named mutations of the harness's `outcome_green` rule are
  killed 4/4 while the held mz-only rule kills 0/4 (`cases=16 correct=16 mutants=4 killed=4
  base_killed=0`, rc 0, `.ufo/waves/round-76/measurement-c1-r76.txt`). C2 operability:
  `quality/counters/c2-r76-shapes.py` counts an interprocedural `del` (a callee that deletes the
  guard key from the mapping it receives, under the dominance test) and a dynamic-key `del` (a
  same-scope name bound once, earlier, to the guard key or a module constant); fifty-nine frozen
  cases score 59/59 against the held 55/59, population unchanged 20/13/13/0
  (`measurement-c2-r76-final.txt`, rc 0, measured at its instrument's last change `3588a527…`
  with identical counts at `755b339f…`/`cb713254…`; C1 at `3588a527…`). Freeze v1 `755b339f…`, freeze v2 `cb713254…`, base `c3e0bc5f…`.
- **Negative result.** The round-75 planned item "kill the echo-dropping outcome mutation" is
  impossible through `verdict=`: the field is green only when `killed == 2`, and the M-Z kill
  already requires the echo, so that mutation produces an identical field on every reachable case
  (measured 16/16 in the v2 receipt kept beside the final one; the matched control is
  `control-baseline-r76-matched.txt`). The claim moves to the four
  observable outcome-rule mutations (`outcome-summary-only`, `-killed-only`, `-killed-any`,
  `-killed-or`) with `always-red` as the shape that separates a rule ignoring the green conjunct.
  Recorded in `corpus/knowledge/outcome-field-r76.md` §2 and lesson M76-2.
- **Mechanical fixes.** The witness grammar reads 16+ hex so an over-long echo is a parsed
  mismatch (prefix-vs-equality observable), and the per-run challenge is drawn by rejection
  sampling until it contains an `a-f` letter, closing round-75 M75-4's probabilistic uppercase
  oracle; the counter prints `has_letter=yes` per case and the selftest asserts 200 draws.
- **Mistakes.** Four mined (M76-1 label set modelled `verdict=` as summary-green only; M76-2 the
  unobservable separator class; M76-3 a control-leg regex anchored to end-of-line reported four
  mutants as `0/15` without observing a row; M76-4 the fixture template's first colouring of
  `right`/`green-mutant`), each with evidence, captured-by and a fix that can fail. QUALITY
  128–131 land from them and from considerthese 2026-10-28 proposal 5.
- **Registry and gate bookkeeping.** SOURCES 391 → 393 rows (S455 expressions.rst § Calls,
  S456 simple_stmts.rst § The del statement; S446 re-opened and kept rejected); census exit 0
  with the two documented W04 duplicate-URL warnings; `quality/tool-ledger.md` 133 → 136 rows;
  index rows for both new entries.
- **No-harm.** Gate `bash tools/mado-verify.sh --selftest` unchanged at its bytes (the round
  touches no gate line); the round-72/73/74/75 instruments, `quality/landing-counters.sh`,
  `check-tool-ledger.py` and `check-axis-scores.py` keep their base blob ids. No config tree,
  compositor, service or sibling repo was written; no pacman transaction; no tool installed or
  upgraded.

  Correction (round 77, append-only): the round-76 entry above says "Four mined"; the lesson's
  `## Mistakes` table holds five rows (M76-1…M76-5) — `grep -c '^| M76-' corpus/lessons/round-76.md`
  prints `5`. The count defect is dispositioned in `corpus/lessons/round-76.md` `## Corrections
  (round 77)` (round-76 closure D4).

## Round 77 — the bar's footprint and an executable runbook (2026-11-04, hyaku run 15)

- **Claims.** C1 coverage: the bar-footprint chain becomes a measured join —
  `tools/mado-barfoot.py` derives the declared waybar box (position/layer/height/width/margin/
  exclusive) and joins it to the live layer entry in `hyprctl layers -j` and the monitor's
  `reserved` band from `hyprctl monitors -j`; a frozen fifteen-case set scores
  `cases=15 correct=15 mutants=5 killed=5 base_correct=8/15 tool_selftest=18/18 TARGET_MET`
  at freeze `a83e9bee` (base `aeeef067`), with the live-echo control at 8/15
  (`receipts/control-baseline-r77.txt`). C2 operability: the SKILL.md read-only probe table
  executes end-to-end — twelve frozen expectations, each bound to its committed table row,
  `cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12 TARGET_MET` at the same freeze;
  the read-the-table control reports `executed=0`.
- **Host ground (read-only).** DP-1 3440x1440@99.997, waybar at layer level 2, box 0,0,3440,26,
  reserved `[0,26,0,0]`, usable area y=26..1440; the bar declares `layer top`, `position top`,
  `height 26`, no margins, exclusive default. Captures `fetch/live-{layers,monitors}-r77.json`
  (sha256 `46eb2481…` / `e732af34…`); live join `MADO_BARFOOT … verdict=CLEAN`. No config tree,
  compositor state or service was written.
- **Sources.** SOURCES 393 → 401 rows: S457–S462 and S464 new (Hyprland `Renderer.cpp`, `HyprCtl.cpp`,
  `ReservedArea.cpp`, the layer-shell XML at efb5099; `waybar(5)` and Waybar 0.15.0 `bar.cpp`),
  S463 opened and rejected (wayland.app, no revision pin). Census exit 0 with the documented
  W04 duplicate-URL warnings (S458 shares the HyprCtl.cpp URL with earlier rows).
- **Mistakes.** Five mined in `corpus/lessons/round-77.md`: M77-1 the 12-field registry row
  (census E01), M77-2 the counter resolving `--repo .` inside its scratch cwd, M77-3 the carried
  stale-revision class (r76 D2) with the first fix that can fail, M77-4 my own line-anchor drift
  before the grep, M77-5 a frozen fixture with an impossible layer size.
- **Routed defects D1–D8 (round-76 spot-check).** Dispositioned append-only: D1 provenance trios
  in the two r76 entries; D2 SCORECARD revision correction; D3 declaration errata and the r76
  counter's docstring text (parity receipt); D4 the mistake count from the lesson rows; D5 this
  report's Stale-lane line; D6 the three r76 handoff files committed with the freeze; D7/D8 the
  r76 pointer corrections in the lesson.
- **Registry and gate bookkeeping.** `quality/tool-ledger.md` 136 → 140 rows; `SKILL.md`
  canonical Gate registry gains `mado-r77-barfoot` (probe), `mado-r77-barfoot-counter` and
  `mado-r77-runbook` (gates); index 95 → 96 rows; SCORECARD round-77 block with both axis rows and two capability
  rows. The used-by back-references of seven registry rows are repaired in place (12 pairs,
  logged old→new in `corpus/lessons/round-77.md`), and `quality/landing-counters.sh` is GREEN
  (nav/usedby/ledger/citecheck all rc 0).
- **No-harm.** Gate `bash tools/mado-verify.sh --selftest` 460/460 at unchanged bytes; the
  frozen r72–r76 instruments and `quality/landing-counters.sh`, `check-tool-ledger.py`,
  `check-axis-scores.py` keep their base blob ids (the r76 counter takes a docstring-only
  correction with a parity run); axis table re-derived at the landing tip; census exit 0. No
  config tree, compositor, service or sibling repo was written; no pacman transaction; no tool
  installed or upgraded.
- **Wave.** One v1 wave, 12 seats (4 executors, 2 scribes, 1 scout, 1 connector, 1 reviewer,
  1 critic, 1 mutation-tester, 1 revenger; attack share 4/12). Seat outcomes are reported in the
  round report; a dead seat stays dead in the evidence.

## Round 78 — the margined band and a churn-resistant runbook (2026-11-04, hyaku run 15)

- **Claims.** C1 coverage: the margined auto exclusive-zone composition becomes a modelled join —
  `tools/mado-barfoot.py` (`r78-v1`) forms `expected = extent + margins[opposite edge]` from the two
  measured contributors (gtk-layer-shell's client auto zone plus Hyprland's anchored-edge margin);
  the frozen eighteen-case set scores `cases=18 correct=18 mutants=7 killed=7 base_correct=8/18
  tool_selftest=22/22 TARGET_MET` at `d27c5ff4` (freeze `b8508bd9`, pre-wave amendment `44a36b64`,
  base `f597eccb`), with the held r77 model at 8/18
  (`receipts/measurement-c1-r78.txt`, `receipts/control-baseline-c1-r78.txt`). C2 operability: the
  SKILL.md read-only runbook binds twelve of its seventeen rows by shape and validates the two bar
  captures as dump rows — `cases=17 executed=17 matched=17 shapes=12/12 anchors=17/17 control=5/17
  mutants=5 killed=5 TARGET_MET` at the same revision; the held fixed-value rule scores 5/17
  (`receipts/measurement-c2-r78.txt`).
- **Host ground (read-only).** The declared zero-margin bar joins CLEAN (DP-1, level 2, box
  0,0,3440,26, `reserved [0,26,0,0]`); a fixture declaration adding `margin: 4` predicts
  `box=4,4,3432,26` and band 34 against the live 26 and reports DIFFER, where the r77 tool returned
  UNMODELLED. Captures `fetch/live-{layers,monitors}-r78.json` (the monitors reply reduced to the
  fields the join reads), receipt `receipts/live-join-r78.txt`. No config tree, compositor state or
  service was written.
- **Sources.** SOURCES stays 401 rows: the seven rows the claims cite (S457–S462, S464) are
  re-opened with fresh pinned fetches under `.ufo/waves/round-78/fetch/` (six code files
  byte-identical to the round-77 copies; `waybar(5)` re-rendered), S463 re-confirmed rejected, and
  their `used-by` cells gain `corpus/knowledge/bar-footprint-margins-r78.md` (eight rows touched
  old→new, logged in the lesson). Census exit 0 at both ends.
- **Mistakes.** Eight mined in `corpus/lessons/round-78.md`: M78-1 three impossible margined fixture
  boxes, M78-2 an unsorted churn sample, M78-3 a monitor serial quoted into a receipt (privacy gate
  R5), M78-4 the file-wide anchor test the wave connector broke, M78-5 the multi-line ledger row
  that made the freeze commit ledger-red, M78-6 declaration provenance drift, M78-7 stale
  present-tense claims in the registry/index/entry, M78-8 the time-bound r77 citation.
- **Registry and gate bookkeeping.** `quality/tool-ledger.md` 140 → 142 rows (two new counters;
  the `tools/mado-barfoot.py` row now describes r78-v1 and cites the r78 declaration); `SKILL.md`
  canonical Gate registry gains `mado-r78-barfoot-margins` and `mado-r78-runbook`, the r77 probe
  row is corrected to the current tool (22/22, new exit map, both frozen sets), and three
  read-only probe rows are added (active workspace, object counts, the two captures); index
  96 → 97 rows; SCORECARD round-78 block with both axis rows and two capability rows.
- **No-harm.** Gate `bash tools/mado-verify.sh --selftest` 460/460 at unchanged bytes; the frozen
  r72–r77 instruments, `quality/landing-counters.sh`, `check-tool-ledger.py`, `check-axis-scores.py`
  and `check-index.py` keep their base blob ids; `check-session-material.py` 291 findings at both
  base and tip with none on a round-78 path; axis table re-derived at the landing tip; census exit 0.
  No config tree, compositor, service or sibling repo was written; no pacman transaction; no tool
  installed or upgraded.
- **Wave.** One v1 wave, 13 seats (4 executors, 2 scribes, 1 scout, 1 connector, 2 reviewers,
  1 critic, 1 mutation-tester, 1 sentinel; attack share 5/13). Seat outcomes are reported in the
  round report; a dead seat stays dead in the evidence.

## Round 79 — the static reserve under the band and a per-row runbook (2026-11-04, hyaku run 15)

- **Claims.** C1 coverage: the static `monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT`
  reserve composes with the bar's own band — `tools/mado-barfoot.py` (`r79-v1`) reads the rule walk
  behind the reserve (`addreserved` sets the same-selector rule, a positional rule replaces it,
  `transform` copies it, the newest rule wins), arranges the bar inside the static-reduced usable
  box and forms `expected = static[edge] + extent + opposite margin`; the frozen twenty-three-case
  set scores `cases=23 correct=23 mutants=12 killed=12 base_correct=18/23 carried=18/18
  tool_selftest=50/50 TARGET_MET` at `999a4a3f` after repairs R1–R3 (the frozen run at
  `5eb8f20f` printed the same counts on the pre-repair bytes; base `e4b153df`), with the held r78 model at 18/23
  (`receipts/measurement-c1-r79.txt`, `receipts/control-c1-r79-at-base.txt`). C2 operability: the
  SKILL.md runbook executes per-row bindings — 22 cases on 22 distinct rows, four documented model
  refusals over committed fixtures (a `mode` preset, a scaled monitor, the `background` layer, a
  spaced output pattern) and the `omarchy menu keybindings --print` row bound by shape —
  `cases=22 executed=22 matched=22 shapes=17/17 anchors=22/22 rows=22/22 control_new=0/5 mutants=9
  killed=9 tree=bound TARGET_MET` at the same revision; the held r78 instrument exits 2 on the
  successor set (`receipts/measurement-c2-r79.txt`).
- **Host ground (read-only).** The live join with `--rules ~/.config/hypr/monitors.conf` reports
  `STATIC … top=0 right=0 bottom=0 left=0 source=rules` (no `addreserved` line in the host tree),
  box `0,0,3440,26`, `reserved=EQ band=26 expected=26`, `CLEAN` rc 0 — the composition is exercised
  by the frozen fixtures, not by a host mutation. No config tree, compositor state or service was
  written; no `addreserved` line was applied.
- **Sources.** SOURCES 401 → 404 rows: S465 (`src/output/Monitor.cpp`, `setStatic` and
  `logicalBoxMinusReserved`) and S466 (`src/desktop/reserved/ReservedArea.cpp`, `calculate`'s
  static-plus-dynamic sum) admitted, both fetched byte-identically at `efb5099…` and byte-equal to
  earlier pins; S467 (the Hyprland wiki Monitors page) rejected — it documents the line syntax only,
  not the summation, and the live URL 404s. `used-by` gains the new entry on S303, S457, S458 and
  S459 (old → new in the lesson). Census exit 0 at both ends.
- **Mistakes.** Seven mined in `corpus/lessons/round-79.md`: M79-1 the round-78 before-command class
  (closed by the counter's `anchor-absent` path), M79-2 the C2 counter's missing `cwd` and two
  wrong mutation anchors caught by a sandbox dry run, M79-3 the stale instrument self-description
  (`r78-v1` / `22/22` examples), M79-4 an unused `churn` key in the first C2 generator that
  silently did not score a sample, M79-5 the fetch manifest's self-referential last line, M79-6 the
  `addreserved` fall-through model and the four fixtures that encoded it (repair R1), M79-7 five
  more reachable model classes (repair R2: origin, clamp, selector refusal, band overflow,
  transform slot) — the tool gained six assertions (43 → 50) and the case set still scores 23/23
  with twelve mutants.
- **Registry and gate bookkeeping.** `quality/tool-ledger.md` 142 → 144 rows (two new counters; the
  `tools/mado-barfoot.py` row now describes `r79-v1`, `--rules` and the r79 selftest);
  `SKILL.md` gains the `### Executable runbook rows (round 79)` table (22 rows) and two canonical
  registry rows (`mado-r79-barfoot-reserve`, `mado-r79-runbook`), and the r77 probe row is updated
  to the r79 generation; index 97 → 98 rows; SCORECARD round-79 block with both axis rows, two
  capability rows and the round-78 routed-defect closures; `corpus/knowledge/bar-footprint-reserve-r79.md`
  supersedes the r78 static-`addreserved` limit.
- **No-harm.** Gate `bash tools/mado-verify.sh --selftest` 460/460 at unchanged bytes; the frozen
  r72–r78 instruments, `quality/landing-counters.sh`, `check-tool-ledger.py`, `check-axis-scores.py`
  and `check-index.py` keep their base blob ids; `check-session-material.py` at both ends with none
  on a round-79 path; axis table re-derived at the landing tip; census exit 0. No pacman
  transaction; no tool installed or upgraded.
- **Wave.** One v1 wave, 14 seats (2 scouts, 1 connector, 4 executors, 2 scribes, 2 reviewers,
  1 critic, 1 mutation-tester, 1 sentinel; attack share 5/14). Seat outcomes are reported in the
  round report; a dead seat stays dead in the evidence.

## Corrections (round 80, append-only)

- **Round-79 count.** The round-79 entry above says "Seven mined"; `corpus/lessons/round-79.md`
  carries eight `## Mistakes` rows (M79-1…M79-8). The eight stands; the sentence above stays as the
  dated record (round-79 closure D3; the r80 lesson's M80-3).

## Round 80 — the composition under the band, and two matcher classes (2026-11-04, hyaku run 15)

- **Claims.** C1 coverage (capability acquisition): a second exclusive layer surface composes under
  the running usable box — `tools/mado-barfoot.py` (`r80-v1`) gains `--surfaces` and the arrangement
  model (`arrangeLayersForMonitor`'s level order and running bounds, `arrangeLayerArray`'s
  full-box/usable bounds split and empty-box skip, `applyExclusive`'s four-rule first match with the
  `zone + margin > 0` guard, and `CReservedArea{ORIGINAL, usable}`'s area guard), printing
  per-surface `MADO_BARFOOT_ATTR:` beside `gt=`/`attr=` vectors — the frozen thirty-three-case set
  scores `cases=33 correct=33 mutants=22 killed=22 base_correct=23/33 carried=23/23
  tool_selftest=111/111 TARGET_MET` at the repair tip (`receipts/measurement-c1-r80-at-tip.txt`;
  the freeze run at `6c302a53` printed the same counts on the pre-repair bytes), with the held r79
  model at 23/33 (`receipts/control-c1-r80-at-base.txt`) and a parser-stub skip also at 23/33
  (`receipts/control-c1-r80-parser-stub.txt`). C2 operability: the runbook gains two matcher
  classes — a chord grammar over `omarchy-menu-keybindings`' chord column and a word-plus-exit-status
  matcher for `systemctl --user is-active` — `cases=24 executed=24 matched=24 shapes=19/19
  anchors=24/24 rows=24/24 control_new=0/2 mutants=16 killed=16 tree=bound TARGET_MET`
  (`receipts/measurement-c2-r80-at-tip.txt`); its before-state is a structural setup refusal (the
  critic's Q1c), so the claim is a capability acquisition with the capability's absence as its
  before, and the demonstrated `rows=22/24 → 24/24` before→after is round 81's instrument.
- **Host ground (read-only).** `receipts/live-join-r80.txt`: the single-surface join and the
  composition join with `wallpaper` declared (`boxes=MATCH,MATCH … attributed=26 gt=0,26,0,0
  CLEAN`); the host carries exactly two layer surfaces (waybar level 2, wallpaper level 0) and no
  second exclusive consumer, stated as such in the entry's limits. No config tree, compositor state
  or service was written.
- **Sources.** SOURCES 404 → 412 rows: S470 (`src/render/Renderer.cpp`, the arrangement/attribution
  ranges) byte-identical to the round-78 pin, S471 (`src/protocols/LayerShell.cpp`, the zone/edge
  handlers and the alignment error), S472 (`tests/desktop/Reserved.cpp`, the upstream area
  assertions), S473 (the installed `omarchy-menu-keybindings`, own-work) and S474 (the installed
  `systemctl` man page) mined; S475 a rejected row that supersedes S467; S476/S477 mined supersede
  rows for S473/S472 after the wave's source seat caught two wrong anchors. One mutable cell moved
  (S475 `recheck on-change → 180d`). Census exit 0 at both ends.
- **Mistakes.** Six mined in `corpus/lessons/round-80.md`: the five routed defects of the round-79
  closure (M80-1 the stale after-cell, M80-2 S467's reason, M80-3 LOG's "Seven mined", M80-4 the
  unregistered `S468`/`S469` fetch files, M80-5 the r79 partial seat) and M80-6, the round's own
  wrong S473/S472 anchors caught by the wave's source seat and corrected as S476/S477. Two empty
  sweeps recorded (no `TODO/FIXME/XXX` in the three instruments; no dead keys in the new sets).
- **Repairs (append-only, declaration §Repair).** R1 the composition `box=` field's index
  (`boxes[sequence.index(0)]`; wave seat `R80ScribeEntry` F1) and the C1 docstring's stale
  `cases=30`; R2 the chord grammar accepts the formatter's empty-key rendering (found by the L1 on
  live bytes and independently by `R80ReviewerC2` F1); R3 the C2 counter's child environment is an
  allowlist and `TMPDIR` is pinned inside the scratch root (`R80Sentinel` F1/F2); R4 the state
  matcher follows the 0/non-zero contract instead of pinning 3 (`R80ReviewerC2` F3). No case,
  expectation, mutant or target moved; every repair re-measured.
- **Named limits (entry §11, SCORECARD).** Four reachable classes where the frozen set does not
  reach and the model is wrong (negative-tie centring, `auto` on a dynamic band, `auto` on
  corner/parallel anchors, the `exclusive` default), plus the C2 residuals the reviewer named
  (the mask-65-only `code:201` rewrite, the enum's `maintenance`/`refreshing` gap, >35-column
  truncation, synthetic negatives).
- **Registry and gate bookkeeping.** `quality/tool-ledger.md` 144 → 146 rows; `SKILL.md` gains the
  `### Executable runbook rows (round 80)` table (24 rows) and three registry rows
  (`mado-r80-barfoot-composition`, `…-counter`, `mado-r80-runbook`), with the two r80 counter cells
  corrected to their measured selftests (60/60, 80/80); `PROVINCE.md` gains the round-80 refinement
  (one read-only `--surfaces` declaration); the hermetic gate stays 460/460; index 98/98 → 99/99;
  axis table `mismatched=0`; session-material 291 findings with no round-80 path.
- **Wave.** One v1 wave, 14 seats (`w1-spec.json`, `w1-dispatch.json`, `w1.ready.dispatched`); seat
  reports under `.ufo/waves/round-80/w1/` and their findings in the lesson. Dead seats and empties
  are disclosed in the round report, never backfilled (QUALITY 115).

## Round 81 — the overflow rounding and the auto gate, and two matcher classes (2026-11-04, hyaku run 15)

- **Claims.** C1 coverage (capability acquisition): the bar-footprint join models the three reachable
  classes round 80 recorded as `NOT_MODELLED` — hyprutils `CBox::round`'s coupled origin/far-edge
  rounding (a panel one pixel wider than its bounds lands at `x=-1, w=1002`, where the round-80 model's
  floor-divided offset gave `0/1001`), the auto exclusive zone gtk-layer-shell actually sends (gated on
  `horiz XOR vert`, sized from the allocation, plus the unanchored margins — so a corner, a parallel
  pair and an all-four anchor set reserve nothing even with an explicit `exclusiveEdge`, a left dock's
  zone reaches the left rule and the attribution vector, and a dynamic band is a named refusal), and
  the `hyprutils >= 0.14.0` pin that licenses the tag. Frozen set 39 cases (33 carried parsed-equal +
  6 new), 28 mutants, held round-80 tool 33/39 — `cases=39 correct=39 mutants=28 killed=28
  base_correct=33/39 carried=33/33 tool_selftest=121/121 verdict=TARGET_MET` at `0e2ccd2a`
  (`receipts/measurement-c1-r81.txt`). C2 operability: the runbook gains an action-column matcher
  (`omarchy menu keybindings --print | cut -c36-`: the `%-35s` padding pins the separator's column, the
  action must be non-empty, trimmed and carry no second arrow — and no entity rule, because the
  payload escapes markup only on some lines) and a `pgrep -x waybar` matcher that binds the PID list
  with the exit status (a state pair, never a frozen value) — 26 cases / 26 rows / 26 distinct anchors,
  `control_new=0/2`, 23 mutants killed (`receipts/measurement-c2-r81.txt`).
- **Sources.** Three rows opened and pinned this round: **S478** hyprutils `v0.14.0` `src/math/Box.cpp`
  (`CBox::round` `:51-63`, sha256 `2d04de99…`), **S479** Hyprland `CMakeLists.txt` `:150`
  (`set(HYPRUTILS_MINIMUM_VERSION 0.14.0)`, sha256 `97b8028a…`) and **S480** hyprutils `v0.14.2`
  `src/math/Box.cpp` — the installed version, byte-identical to S478 (`pacman -Q hyprutils` →
  `0.14.2-1`, `cmp` empty); `fetch/sha256-r81.txt` verifies 3/3. Census 412 → 415 rows, exit 0 both
  ends (standing W04 warnings). Assimilation: none — the staged
  `/home/vgpnk/Projects/shokuknow/merge/mado/` package collides with the lane's id space on **94** ids
  and touches none of this round's ground (`assimilation/collisions`).
- **Instruments.** `tools/mado-barfoot.py` `r81-v1` (selftest 111 → 121); the two successors
  `quality/counters/c1-r81-overflow-auto.py` (72/72) and `c2-r81-runbook.py` (88/88); the runbook
  heading moves to `### Executable runbook rows (round 81)` with two new rows and the r80 probe rows
  795–797 followed by the r81 registry rows 798–800. Index 99/99 → 100/100; ledger 146 → 148 rows;
  gate 460/460 unchanged; axis table `mismatched=0`.
- **Wave.** One v1 wave, 14 seats (`w1-spec.json`, `w1-dispatch.json`, `w1.ready`,
  `w1.ready.dispatched`). Nine settled with a report and `STATUS: ok`; **five settled empty and
  wrote nothing** — both reviewers, the critic, the mutation-tester and the sentinel — so the
  round's claims have no reviewer/critic attack artifact and the lane's own `check-wave-done` gate
  reads `dispatch-mismatch missing=5`, `verdict=MISSING`, exit 1
  (`receipts/wave-done-r81.txt`). Disclosed, never backfilled (QUALITY 115).
- **Live observation.** The host join is CLEAN on today's capture (`receipts/live-join-r81.txt`):
  DP-1 3440x1440, waybar level 2 at `0,0,3440,26`, `band=26 expected=26 CLEAN`; the monitor's
  `description`/`serial`/`make`/`model` fields were redacted before the capture was kept.
- **Repairs of the round-80 closure.** D1 (appended errata only), D2 (report pointers measured at the
  landing tip), D3 (every pointer carries its `grep -n` line), D4 (the blank line before M80-6
  removed), D5 (every seat named with its artifact count), D6 (attack share stated by the policy
  list, the sentinel named separately), D7 (`receipts/wave-done-r81.txt`).
- **Mistakes.** Four mined into `corpus/lessons/round-81.md`: M81-1 the entity rule imported from the
  payload's escaping code and falsified by a live bare `&`; M81-2 `.strip()` on `pgrep` output
  accepting a padded PID; M81-3 two carried mutant anchors dying `anchor-absent` after the zone moved
  (caught by the anchor-existence check, re-pointed); M81-4 the round-80 `Planned` row's
  `preview_scale` ground — no such symbol exists.

## Round 82 — the client's own band, and the tray plane in the runbook (2026-11-04, hyaku run 15)

- **Claims.** C1 coverage (capability acquisition): the bar-footprint join models the class round 81
  refused — a declared dynamic band (`height = 0` on a horizontal surface, `width = 0` on a vertical
  one) — by taking the client's own allocation as a declared input. The layer-shell protocol says a
  zero size is the client's to pick (S481, `set_size` `:347-348`), gtk-layer-shell sends
  `current_allocation.height`/`.width` as the auto zone plus the unanchored margins (S464 `:276`/`:282`,
  held), and Hyprland's arrange pass spans the bounds for a zero desired size — so the band and the
  arranged box are two different numbers and only the allocation names the first. `tools/mado-barfoot.py`
  `r82-v1` adds `--allocation {namespace: band}` and one resolver (`band_of`: declaration first,
  allocation second, a zero or absent band a model refusal, a negative one a setup refusal, an
  unknown namespace a setup refusal) used by both the single-surface and the composition paths.
  Frozen set 47 cases (39 carried parsed-equal + 8), 34 mutants, held round-81 tool 39/47 —
  `cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39 tool_selftest=133/133
  verdict=TARGET_MET` at `780c30fc` (`receipts/measurement-c1-r82.txt`). C2 operability: the runbook
  gains the tray plane as three shape-bound rows — the `StatusNotifierWatcher`'s bus-name owner
  (`busctl --user list`: a line whose PID column is a decimal in 1..4194304), its interface census
  (`busctl --user introspect … /StatusNotifierWatcher`) and the method table that census prints
  (`| awk '$2=="method"'`: every line `.Name method`, at least two) — 29 cases / 29 rows / 29 distinct
  anchors, `control_new=0/3`, 25 matcher mutants killed (`receipts/measurement-c2-r82.txt`).
- **Sources.** Three rows opened this round: **S481** Hyprland 0.56.2's vendored
  `protocols/wlr-layer-shell-unstable-v1.xml` (`set_size`, sha256 `87e0b9c8…`, 19326 B), **S482**
  kstatusnotifieritem `v6.2.0` `src/org.kde.StatusNotifierWatcher.xml` (sha256 `19df7f18…`, 1151 B),
  and **S483** the freedesktop wiki's watcher page, registered `rejected`: it spells the bus name
  `org.freedesktop.StatusNotifierWatcher`, which the round's rows would contradict (flip recorded).
  Census 415 rows at round start (exit 0) → 418 at the content tip (exit 0); no older cell moved.
- **Instruments.** `tools/mado-barfoot.py` `r81-v1` → `r82-v1` (selftest 121 → 133); the two successors
  `quality/counters/c1-r82-allocation-band.py` (84/84) and `c2-r82-runbook.py` (90/90); the runbook
  heading moves to `### Executable runbook rows (round 82)` with three new rows. Index 100/100 →
  101/101; ledger 148 → 150 rows, uncovered 0; gate 460/460 unchanged; axis table `mismatched=0`.
- **Repairs of the round-81 closure.** R1 (this wave's attack seats write artifacts or the gap is
  reported), R2 (round-82 corrections stay in the round-82 section), R3 (the r82 counter's contract
  line is `MADO_R82_RUNBOOK: cases=29 … mutants=25`, not the r81 text), R4 (`--selftest` transcripts
  land under `receipts/`), R5 (round-80 D1–D3 erratum named in the report), R6 (the wave's seat counts
  carry a `jq` counting command in the report).
- **Mistakes.** Two mined into `corpus/lessons/round-82.md`: M82-1 a resolver branch that both
  callers guarded away (the "declaration wins" rule was dead code; the first mutant survived 47/47);
  M82-2 the freedesktop page naming a different bus name, caught by opening the source before
  writing its row. The anchor-drift candidate was examined by the lesson seat and **not admitted**:
  no lane byte carries the `reason=anchor-absent` event (the only such lines are the base control's),
  and both anchors are present at the freeze.

## Round 83 — second-surface allocation and tray state (2026-11-04)

- C1 coverage: tools/mado-barfoot.py now resolves any declared namespace's allocation before arranging exclusive surfaces. Receipt `.ufo/waves/round-83/receipts/measurement-c1-r83.txt` at dbc09269 reports correct=58/58, kills=39 but declared mutants=38: TARGET_MISSED. The clerical constant is repaired forward; no retroactive admission.
- C2 operability: SKILL.md executable runbook 29→31 rows, including tray items and host-registered boolean; dbc09269 receipt matched=31/31, mutants=27 killed=27, TARGET_MET.
- Instruments, controls and declaration landed in 4e48d8e7, 4208c24a, aeeb5e54 and dbc09269. Pre-wave red measurements drove repairs; amendments are disclosed, not a clean pre-data freeze.
- Sources S484/S485 and mistakes/gate: corpus/lessons/round-83.md. Round82 correction: set_size assignment sentence is 128–129; 347–348 is configure. Round82 seat status count is 7 ok/7 defect; census includes W01 S277.

## Round 84 — namespace discipline and pipeline producer status (2026-11-04)

- Claims: C1 coverage of three ambiguous declaration classes; C2 operability of guarded
  pipeline commands plus two contained failure-propagation rows. Freeze landed at
  `3f9eec3906ddd1492e8bc08325e83064f00111ea`; declaration and do-nothing receipts are
  `.ufo/waves/round-84/claims-declaration-r84.md` and `receipts/control-c{1,2}-r84-*`.
- ONE validated ten-seat v1 wave settled (Main WAVE-DONE; `w1-results.json`, ten nonempty
  outputs). ExecC1 and ReviewerC1 independently re-executed61/61,41/41 kills,held58/61,
  carried58/58,selftest139/139 at the freeze. ReviewerC1 retained three surviving cheats;
  this is finite refusal coverage, not universal identity correctness.
- Frozen C2 executed/matched33/33 but ended setup rc2: final mutation anchor occurred twice.
  The forward repair expands only that anchor to a unique two-line executable block;
  cases, predicate, kill rule and populations remain fixed. Original frozen rc2 is not
  re-described as a pass. Counter docstrings/control citations corrected forward too.
- Sentinel's live-stdout disclosure risk is repaired: C2 durable rows retain only rc and byte
  count, never live values. Absolute handoff paths are protocol-required; census path output is
  retained unfiltered per prompt. No credential issue was observed; no historical rewrite.
- Sources S486/S487 were opened/pinned by L1; two bounded knowledge entries are indexed.
  Gate/Mistakes and the one considerthese adoption (domain-share line) live in
  `corpus/lessons/round-84.md`; QUALITY138/139 derive from producer masking and registry drift.
- R83 routed R1: add four missing home-registry rows plus two current successors; R2:
  population equality preassertions and constant-drift setup refusals; R3: connector delivers
  file:line sibling ownership scan and one interpretation caption, without changing frozen rows.
- Every source/claim result is either re-executed this round or explicitly attributed to
  committed prior evidence. No tool installs, pacman transaction or desktop/service write.
- L1 final re-executions at `6229a0eb8be551660aa2862e52c3991613429532`:
  C1 cases61/correct61/mutants41/killed41/held58/carried58/TARGET_MET;
  C2 repaired successor cases33/executed33/matched33/shapes26/26/killed29/29/TARGET_MET.
  Exact commands/revision/input hashes: `.ufo/waves/round-84/receipts/final-c{1,2}-r84.txt`.
  Frozen C2 remains setup rc2, not retroactively green; **round honest stop, not admitted**.
- Harm watch at that content: `final-index-r84.txt`104/104; `final-ledger-r84.txt`154/154;
  `final-gate-r84.txt`460/460; `final-wave-r84.txt`1/1 with10 settled outputs. Initial
  axis publication failed (102 versus104), retained as `axis-prepublication-r84.txt`; records
  correct only its publication marker. Source census420→422, exits0/0, warning set retained.
- R83 registry R1 red4 missing→green0 in `registry-{before,after}-r84.txt`; per-seat exact IDs,
  expired terminal statuses and unverified actual models are disclosed in `seat-metadata-r84.json`.
  Zero replaced seats; ten substantive outputs, no terminal-success inference. Main's WAVE-DONE
  received before any report. No source tree/sibling edit or package operation.

## Round85 — cause-bound identity witnesses and status classes (2026-11-04)

- Claims: C1 coverage of declaration-identity cause witnesses; C2 operability of the runbook's
  status classes. Motivating evidence: round84 verifier R1–R4, stage-only refusal holes and
  producer-status/prefix survivors. Freeze `3905311c75a39c5710413105865c0a1a7dd0116a`;
  successor rows and binding repairs `d7c40e6d1b9a7476f2ff48254d577799ce9901e4`.
- C1 tool now emits literal cause tokens at identity refusal sites and distinguishes bar,
  same-level-extra and cross-level-extra namespace repeats without casefolding names.
  Frozen controls72 cases=61 carried+11 witnesses; counter51 mutants, held tool62/72.
  Full frozen target72/72,51/51 kills,152/152 selftest is independently re-executed by the
  lane reviewer (`.ufo/waves/round-85/w1/R85ReviewerC1.md`). Case-only cause-flooding and
  wrong-negative-allocation outputs expose limits, not full-gate survivors.
- C2 adds documented contained pipelines with guarded0/7/141 versus unguarded0/0/0.
  Frozen counter fails setup on declared negative supersessions; its frozen SKILL section
  has33 rows rather than36. Forward comparison/row/anchor-region/print fixes execute36 rows
  in sandbox, but four declared mutations survive (33/37). Original claim stays unverified.
  Controls restored byte-identical to freeze after a discarded forward pattern experiment.
- Source curation: S488 POSIX2024 section2.9.2 and S489 maintainer Bash5.3 section3.7.5;
  S490 rejects uniquely inferring signal13 from141 because explicit exit141 is equivalent.
  GNU endpoint timeouts are not quote absence; maintainer copy was opened independently.
  Registry422→425; old cells unchanged. Gate/located quotes live in lesson85.
- Critic and mutation reports retain command-only Markdown binding, special-status bypass,
  broad carried exemptions, clause-deletion monotonicity and exact-identity case holes.
  QUALITY140–142 learn these findings; no population/kill-rule revision admits the freeze.
  Sentinel finds metadata paths and inherited setup/symlink containment limits; mandatory
  path/census receipts remain unfiltered, no credential disclosure was observed.
- Two bounded knowledge notes are indexed; registry-home and ledger rows for both new
  counters repair the observed freeze ledger red156 population/154 registered/uncovered2.
  SOURCES, lesson, README and SCORECARD records land with the integration commit.
  No package install, pacman transaction, service/config mutation or sibling write.
- ONE13-seat v1 wave, five attack seats, one connector; L1 holds planner. Wave completion,
  final measurements and any dead seats are retained in the final receipts/report. No
  promotion or capability admission; outside-lane judgment remains the integrator's.

### Round85 corrections (append-only)

The earlier sentence “old cells unchanged” is superseded: S486/S487 used-by cells each
append the corresponding round85 knowledge note; exact old→new strings are in lesson85
§Registry changes. No pre-existing status, recheck or opened cell changes.
Frozen declaration ancestry “nine removed” is false: only `rc-blind` is removed from the29
r84 C2 mutants;28 retained+9 new=37. Its kill-rule OR differs from executable AND. These are
declared/instrument disagreements, not repaired frozen predicates.
The successor's table labels seven specialized status pairs explicitly and corrects sample
counts, but the counter still authenticates command cells only. Neither Markdown edits nor
the forward docstring/version corrections cure frozen C2. VERSION is now r85-v1; historical
freeze carries r84-v1 and remains byte-resolvable.

Main supplied WAVE-DONE for all13 seats before the report. Raw `w1-results.json` retains
output=null for13 seats after the orchestrator kernel restart;13 substantive seat report
files exist. Do not fill those nulls or infer terminal success/dead counts from report files.
`receipts/settlement-r85.json` records exact names/roles and unavailable answering models.
Configured scout/scribe routes currently use m_mim, contrary to the prompt's m_mim-off note;
operator-owned routing was neither edited nor overridden. This is disclosed conformance
drift, not an inferred change of the seats' captured routes.

Final L1 re-executions at `2b6dd76b65de4dfe701db87db13b7e448b3538ee`, after WAVE-DONE:
C1 target met72/72,51/51 kills; C2 successor36/36 but33/37 kills,target missed.
Frozen C2 remains setup2; **round honest stop, not admitted**. Exact commands and pins:
round85 `receipts/final-c{1,2}-r85.txt`, `final-inputs-r85.json`. Counter selftests119/119,
106/106; index106/106; ledger156/156/uncovered0/bad_pointer0 (repairs freeze red); axis3/0;
standing selftest460/460; wave1/1/OK all exit0. Census422→425, exits0/0 with warnings
unfiltered. Final fleet misroot sweep leaves unassignable `after` and all sibling/operator
files untouched. No owned misroot, installs, replacements or new L0 question.

### Round86 — refusal records, clause observation and a fresh start after three rejections

Round 86 (hyaku run 15, attempt 2) continues attempt 1's frozen declaration unchanged:
base `a722c604`, attempt-1 bytes preserved at `f72bba01`, freeze
`237ecf4e69a4986108f719f3beeafe111adaa033`. Fresh-start reads done first:
`corpus/lessons/round-85-verifier-spotcheck.md` (routed defects R1–R7),
`round-84-verifier-spotcheck.md`, `round-83-verifier-spotcheck.md`, `round-85.md` and the
2026-11-04 `considerthese/` reflection.

- The counters shipped by the dead attempt were run before anything was frozen, and both C2 runs
  before the last repair failed: `ERROR (stage=setup mutant regex-anchor-dropped anchor occurs 0
  times, not once)` (rc 2, never a verdict) and then `matched=34/37 … clauses_observed=34/37`
  because the anchor-observation conjunct contradicted the counter's own `declared` tuple, then
  `matched=37/37 … killed=35` because two mutations had drifted onto the held control. All four
  runs, and the three repairs, are in `.ufo/waves/round-86/receipts/instrument-repair-r86.md`;
  C1 needed no repair.
- C1 at the freeze: `cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72
  tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET` — the all-cause
  flood that the held substring rule scores 75/75 scores 48/75 under the record rule, while the
  unchanged r85 tool scores full marks under both (the increment is the rule).
- C2 at the freeze: `cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37
  clauses_observed=37/37 mutants=37 killed=37 verdict=TARGET_MET`, `held_rule_new_case=0/1`.
  The four r85 survivors (`negatives-skipped`, `samples-skipped`, `regex-anchor-dropped`,
  `line-anchor-prefix`) die on the observation.
- Knowledge: `corpus/knowledge/refusal-records-clause-observations-r86.md` (indexed in
  `corpus/README.md`, frontier bullet added). Lesson: `corpus/lessons/round-86.md` (M86-1..5,
  Gate with S491/S492, census, considerthese). QUALITY 143/144/145 added.
- Registry: S491 (RFC 7493 §2.3, duplicate member names MUST NOT, pin
  `fetch/S491.bin` line 159) and S492 (CPython `re.rst` `fullmatch`, pin `fetch/S492.bin`
  line 957) — 425→427 rows, census exit 0 before and after, standing W04 warnings unfiltered.
- CONSIDERTHESE: `considerthese/2026-11-04.md` proposal 2 (a claim stands beside a red wave-done
  receipt) lands as QUALITY 145; the reflection's figures are relayed, not re-measured.
- Work in flight: ONE v1 wave of 14 seats (executor3, scribe3, scout2, reviewer2, critic1,
  mutation-tester1, sentinel1, connector1; L1 holds the planner seat; 4 attack seats). Wave
  settlement, dead seats, final measurements and the misroot sweep are recorded after WAVE-DONE.
- WAVE ATTACKS (records under `.ufo/waves/round-86/w1/`, all instruments frozen and unfixed):
  ReviewerC1 scores four forgeries 75/75 under the record rule (all-ten-token flood on stderr,
  one-leading-space duplicate record, result-path flood, homoglyph flood) and verifies the ten-cause
  vocabulary complete by AST; Critic shows the negative observation exempts the record's own cause by
  identity not position, both kill rules under-enumerate their rc conjunctions, separability holds one
  way but not both, and dissents from C1's calibration label; ReviewerC2 shows the clause observation
  counts iterations not evaluations (count-preserving stub passes case-level); Sentinel rates an
  ambient `GIT_DIR` overriding C2's `-C repo` as high and lists seven more hygiene findings;
  MutationTester runs 17 counter mutants beyond the declared populations — 5 killed, 12 survived,
  each with an executable input; Connector names the dead constants and the two-convention refusal
  judgement between C1 and C2. Every item is routed in `corpus/lessons/round-86.md`; none changes a
  frozen predicate or a verdict.
- Quote fidelity: the declaration and the first lesson draft quoted S492 as "… return a corresponding
  Match." while the pinned bytes carry the Sphinx role (`:class:`~re.Match``). Both places now quote
  the bytes verbatim; the located spans are S491 bytes 6364–6437 and S492 bytes 39792–39901, and the
  word counts are 11 and 13 (M86-8).
- WAVE SETTLEMENT: ONE v1 wave, 14 seats, roles executor3 / scribe3 / scout2 / reviewer2 / critic1 /
  mutation-tester1 / sentinel1 / connector1; L1 holds the planner seat; four attack seats (28.6%).
  `w1-results.json` records `seats=14`, 14 result rows, every `output` non-empty and 14 substantive
  reports under `.ufo/waves/round-86/w1/`; no dead seat, no residual call, round total 14. One
  report-path defect is my own: the item text still named `R86LabRunbook.md` after the item was
  renamed for the scout role; the file is renamed to `R86ScoutRunbook.md` at integration (content
  untouched) and the class is mined as M86-9.
- FINAL MEASUREMENTS after settlement, at the round tip: C1 `receipts/final-c1-r86.txt` —
  `cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 tool_selftest=152/152
  flooding=48/75 held_flooding=75/75 verdict=TARGET_MET`, rc 0; C2 `receipts/final-c2-r86.txt` —
  `matched=37/37 shapes=27/27 clauses_observed=37/37 mutants=37 killed=37 verdict=TARGET_MET
  tree=bound`, rc 0, plus the freeze-revision clone receipt `final-c2-freezerev-r86.txt`.
  Counter selftests 127/127 and 114/114; standing gate selftest 460/460; index 107/107;
  ledger 158/158 uncovered0; axis 3/0; census 425→427 both exit 0. **Both claims verify.**

### Round 87 — mako effective settings and control-figure fidelity (2026-11-05, hyaku run 15, attempt 1)

- Fresh start after Amendment 27 ("Authorize all"). Declared two frozen claims (`.ufo/waves/round-87/claims-declaration-r87.md`):
  C1 capability, coverage (mako effective settings for one notification); C2 calibration (the r86 held-rule control figure `0/1`).
  Stagnation nudge applied (every axis at 10; no capability row since round 82).
- Wave w1: 12 seats (scout 1, executor 3, scribe 2, connector 1, reviewer 2, critic 1, mutation-tester 1, sentinel 1), attack share
  4/12. All 12 settled; no dead seat; `w1-results.json`; reports under `.ufo/waves/round-87/w1/`.
- Landed: `7563452f9b35af0141c49dc4cc7f791968ca0c90` (tool, two counters, frozen controls, figure file, knowledge entry, S493 row,
  README/PROVINCE/ledger rows, lesson, r86 correction blocks, declaration errata); `00c967214e338d8f0ebb02b78f98fd61a542a515`
  (C1 counter accepts upper-case mutant ids: pre-score setup repair; measured revision).
- Measured at `00c96721`: C1 `TARGET_MISSED` (22/22 cases; controls 7/22, 8/22; mutants 5/10). C2 `TARGET_MET` (before 5.0
  fixture, after 10.0). Harm watch: index 108/108, ledger 161/161 uncovered 0, gate 460/460, file plane CLEAN, census exit 0 (428 rows).
- Named limits: five surviving frozen mutants; containment of symlinked includes; correction-block reasoning; the r86 selftest pin.
  Routed to round 88. Receipts: `.ufo/waves/round-87/receipts/`.

### Round 88 — mako criteria fields, upstream grammar and include containment (2026-11-06, hyaku run 15, attempt 1)

- Fresh start (Amendment 46) after r83–r87 rejected honest stops; the r85–r87 spot-checks read first. Two claims
  (`.ufo/waves/round-88/claims-declaration-r88.md`): C1 capability, coverage (mako criteria fields + upstream boolean/urgency
  grammar); C2 operability (include= containment under declared read roots). Stagnation nudge applied.
- Motivating evidence: the r87 resolver, replayed on the host's own mako chain, refuses `core.ini:15 invisible=true` and
  `:18 invisible=false` ("expects 0 or 1") and so cannot resolve the do-not-disturb state (`.ufo/waves/round-88/w1/receipt-base-host-config-r88.txt`,
  `R88MExecSelftest.md` §5); upstream `types.c parse_boolean` accepts them (S494). r87 R2: a symlinked include escaping HOME is read.
- Wave w1: 12 seats (scout 2, scribe 2, executor 3, connector 1, reviewer 2, critic 1, mutation-tester 1), attack 4/12; all
  settled, no dead seat (`w1-results.json`). Their findings became the declaration's draft revisions before the freeze.
- Landed: freeze `9e36e3a3103349b939982e532feca443f02e660d` (declaration, counters, frozen cases/mutants, pre-freeze control
  receipts, wave evidence); C1 tool `650e18bdf0ae404ec9a80874c4503ecf3237e8e6`; C2 tool `7d3074865a9f5acfa0f1c9c66b460e73d4031331`;
  records (knowledge entry, S494/S495, README row, lesson, QUALITY 146–147, SCORECARD, this entry) in the round's record commit.
- Measured: C1 at `650e18bd` TARGET_MET 62/62, 22/22 killed, controls 14/15/33/43 < 62; C2 at `7d307486` TARGET_MET 26/26, 7/7
  killed, base 11, refuse-all 14 < 26; C1 re-run at `7d307486` TARGET_MET. Census 428 → 430, exit 0.
- Residual r1: 4 attack seats (reviewer 2, critic 1, mutation-tester 1), all settled (`r1-results.json`): C1 VERIFIES, C2
  VERIFIES; critic STANDS on both predicates, FALLS on the declaration's C2 "before" sentence (errata appended), WEAKENED on two
  stale ledger figures and an uncommitted harm receipt (fixed in the final commit). Mutation probe survivors routed to round 89.
  Round total 16 seats (w1 12 + r1 4), 0 dead. Harm watch at `498855cb`: gate 460/460, file plane CLEAN 29, index 109/109,
  ledger 163/163 uncovered 0, tool selftest 52/52, counter selftests 40/40 and 28/28 (`receipts/harm-final-r88.txt`).

### Round 89 — mako summary~/body~ as POSIX ERE (capability) and a runnable survivor gate (2026-11-06, hyaku run 15, attempt 1)

- Inputs: the r88 non-author spot-check (routed R1–R5) and `R88MResidMut` §3–§4; the r88 named limit "summary~/body~ refused";
  `considerthese/2026-11-06.md` proposals 1 and 3. Two claims (`.ufo/waves/round-89/claims-declaration-r89.md`): C1 capability,
  coverage (mako `summary~`/`body~` matched with libc `regcomp(REG_EXTENDED + REG_NOSUB)`/`regexec` in the C locale, behind
  upstream's criteria tokenizer); C2 operability (a runnable survivor gate over round 88's routed survivors). Nudge not claimed.
- Motivating evidence: the host's `core.ini:24-36` carry five `[summary~="…"]` click-action sections, all refused by the r88 tool
  (base decides 4/9 host criteria sections, 5 refusals per run; the candidate 9/9, 0 refusals: `w1/R89MExecHostDiff.md`). mako
  v1.11.0 never calls setlocale (S500), so it matches in the C locale (S498); a bare Python process here starts in `en_US.UTF-8`.
  The r88 tokenizer kept `\` inside quotes and split on any whitespace, unlike `parse_criteria` (M89-2).
- Wave w1: 12 seats (scout 2, scribe 1, executor 4, connector 1, reviewer 2, critic 1, mutation-tester 1), attack 4/12. Findings
  became draft revisions before the freeze: earlier-invalid-occurrence fix (ReviewC1 F1), M33–M37, cases r31/r32/n04/n07,
  45 blind cases (b01–b45), and the critic's wording/axis/provenance/sequencing changes (F2–F11). Fuzz: 12 800 candidate/oracle
  comparisons, 0 disagreements; Python `re` disagrees on 404/3200.
- Landed: freeze `d87361354b4d142287aac05bb973315749ef1fce` (declaration, counters, frozen controls, pre-freeze receipts, w1
  evidence, r88 dispatch markers per R5); C1 tool `099c662dc55521e365cd4126132cdcda4efc54b6` (candidate bytes unchanged,
  sha256 6b4bc409…); records (knowledge entry, S496–S500, S493/S494 used-by, README rows, lesson, QUALITY 148–149, ledger rows,
  SCORECARD, this entry, measured receipts) in the round's records commit.
- Measured: C2 at the freeze `TARGET_MET cases=95 correct=95 counted=7 killed=7 do_nothing_B_only_killed=0` (tool = r88 tool,
  `receipts/c2-measured-F-r89.txt`); C1 at `099c662d` `TARGET_MET cases=141 correct=141 carried=61/61 mutants=37 killed=37`,
  controls naive 34, globals 35, base 78, python-re 127 (`receipts/c1-measured-A-r89.txt`); C2 re-run at `099c662d` TARGET_MET
  (`receipts/c2-harm-at-A-r89.txt`). MODELLED_FIELDS 10 → 12. Census 430 → 435 rows, exit 0.
- Residual r1: 4 attack seats (reviewer 2, critic 1, mutation-tester 1), all settled (`r1-results.json`): C1 VERIFIES (pins hold,
  frozen command reproduces the receipt byte-for-byte, 26 expectations re-derived), C2 VERIFIES (F and A bodies byte-identical,
  B-only 0/7 and selftest 3/7 reproduced, RM6C2 crash-only attack failed). Critic: F1–F3 (harm and end-census receipts cited
  before they were committed) FALL → committed in the final commit; F4 the blind set is 45 (b01–b45), not 44 → corrected here and
  as a declaration erratum; F5 the entry's host-refusal sentence described the `--summary --app-name` run → corrected; F6–F8 locator
  and wording → corrected. Mutation probe: 15 new mutants, 4 killed, survivors RS01 (body~ earlier-invalid), RS05 (quoted bare
  token), RS12 (group-index accepted) routed to round 90 as cases; RS02 crash-only; RS04/RS09 text-only; RS07/RS08/RS11/RS15
  argued equivalent. Round total 16 seats (w1 12 + r1 4), 0 dead. Harm watch at `51bf076f`: gate 460/460, file plane CLEAN 29,
  index 110/110, ledger 165/165 uncovered 0, tool selftest 59/59, counter selftests 27/27, 18/18, 40/40, 28/28
  (`receipts/harm-final-r89.txt`); census end rc 0 (`receipts/census-end-r89.txt`).

### Round 90 — xdg-desktop-portal backend routing (capability) and a receipt-presence gate (2026-11-06, hyaku run 15, attempt 2)

- Inputs: the round-89 non-author spot-check (D1 records cite receipts committed later, D2 registry stops at r86, D3 RS01/
  RS05/RS12 survive); `considerthese/2026-11-06.md` proposal 4 (widen past bar + mako: xdg-desktop-portal); the round-12
  portal table (`corpus/knowledge/xdg-portal-routing-r12.md`, hand-derived, 16 rows, no tool). Two claims
  (`.ufo/waves/round-90/claims-declaration-r90.md`): C1 capability, coverage; C2 operability. Nudge not claimed.
- Motivating evidence: `git show 5041acf9:tools/mado-portals.py` fails (no instrument on the portal plane); the round-12
  table omits Background, Wallpaper, RemoteDesktop, Clipboard and Usb; `--rev 498855cb` and `--rev 51bf076f` of the new
  check print `verdict=MISSING` where `check-deliverables.py` said `OK` (M90-2).
- Attempts: attempt 1 (`MadoR90`) ran wave w1 and wrote the declaration, counters and frozen controls, then ended before
  any commit (watchdog `lane-dead-no-report mado round=90` 20:22:51). Attempt 2 (`MadoR90a2`) inherited every file after
  `sha256sum` matched each pin, re-ran both draft controls (`.ufo/waves/round-90/receipts/c1-controls-prefreeze-r90.txt`,
  `.ufo/waves/round-90/receipts/c2-controls-prefreeze-r90.txt`), then froze. Nothing inherited was discarded.
- Wave w1: 13 seats (scout 2, scribe 1, executor 4, connector 1, reviewer 2, critic 1, mutation-tester 2), attack 5/13; all
  settled; `w1-results.json` records no outputs (orchestrator kernel restart); 11 seats left report files, the two scouts
  did not (M90-4). Findings became the declaration's six draft revisions before the freeze.
- Landed: freeze `1d9bc40414a5d6bddd449cc633a12f2e7e338652`; C1 `7bec239929cdd1d7c796a89ddccefe47d802673a`; C2
  `c09d3465299c53a8158a96b2214c2bcda44bcb41`; D3 `7c28090e99ca99b799e16a92797bf33f63aca372`; records (knowledge entry, S501–S503,
  README rows, QUALITY 150–151, ledger rows, SKILL registry rows, lesson, SCORECARD, this entry) in the records commit,
  gated by the C2 check in `--worktree` mode (`.ufo/waves/round-90/receipts/c2-gate-records-r90.txt`).
- Measured: C1 at `7bec2399` `TARGET_MET cases=229 correct=229 blind=66/66 fresh=120/120 mutants=60 killed=60`, controls
  r12-rule 70, host-table 10, do-nothing 35, base 0 (`.ufo/waves/round-90/receipts/c1-measured-r90.txt`); C2 at `c09d3465`
  `TARGET_MET expectations=83 met=83 defects_detected=4/4 population=38 mutants=28 killed=28`, controls 0/44/46/0
  (`.ufo/waves/round-90/receipts/c2-measured-r90.txt`). Census 435 → 438 rows, rc 0 both ends
  (`.ufo/waves/round-90/receipts/census-start-r90.txt`, `.ufo/waves/round-90/receipts/census-end-r90.txt`).
- Host answer (`.ufo/waves/round-90/receipts/host-run-r90.txt`): gtk serves 11 interfaces, hyprland 4 (Screenshot,
  ScreenCast, GlobalShortcuts, InputCapture), none 6 (Background, Wallpaper, Secret, RemoteDesktop, Clipboard, Usb); Secret
  has no backend because `gnome-keyring.portal`'s `UseIn=gnome` never matches `hyprland` and gtk lacks Secret.
- Harm watch at the records commit `6156d399`: gate selftest 460/460, file plane CLEAN 29, index 111/111, ledger 169/169 uncovered 0, `tools/mado-mako.py` selftest 62/62, `tools/mado-portals.py` selftest 22/22, receipt presence at the records commit OK 31/31, round-89 C1 TARGET_MET 141/141 37/37 and C2 TARGET_MET 7/7 on the D3 tool (`.ufo/waves/round-90/receipts/harm-final-r90.txt`). Final commit gated by the C2 check (`.ufo/waves/round-90/receipts/c2-gate-final-r90.txt`).

### Round 91 — default-application resolution (capability) and a seat-report retention gate (2026-11-06, hyaku run 15, attempt 1)

- Inputs: the round-90 non-author spot-check (routed defects: no gate self-test on `check-receipt-presence.py`; two scout
  reports lost, M90-4; lesson wording); `considerthese/2026-11-06.md` proposal 4 (widen past bar + mako; prefer an
  operator-config gap). Two claims (`.ufo/waves/round-91/claims-declaration-r91.md`): C1 capability, coverage; C2
  operability. Nudge not claimed.
- Motivating evidence: no lane line on MIME/default applications (`grep -n -i -E 'mime|xdg-open|mimeapps|default app'
  PROVINCE.md SKILL.md corpus/README.md` → none at `cc0381db`) while Omarchy writes `~/.config/mimeapps.list` and
  `hyprland-mimeapps.list`; at `cc0381db` 133 of 1732 dispatched seats' `Report:` paths are absent from the tree (R91MExecGate
  labels; round 90's two scouts among them) and no lane check reads the trailers.
- Wave w1: 14 seats (scout 2, scribe 1, executor 5, connector 1, reviewer 2, critic 1, mutation-tester 2), attack 5/14.
  Findings changed the candidate (shell parser and program lookup ported, GKeyFile byte rules, xdgmime's own dirs, libc
  alias replay, readdir order), the counters (fresh leg, sandbox narrowed, opaque tool paths, selftest per mutant,
  generator-truth fresh fixtures for C2) and the sets before the freeze. Residual `r1`: 2 attack seats on the measured bytes.
- Landed: freeze `fa71279fc927f86df2d14a62f1f60230a7cf4ada`; C1 `54a0683ce5c1c746fa02fa9f36b530c44772bfa2` (tool, knowledge
  entry, S504–S507, PROVINCE/SKILL/ledger/index rows, host replay); C2 `0e09349e2c735c9fe1d4ba8d5c4ef79506f2d0bc` (gate and
  its rows); D1 `cbbeb862455d9bc65f6b837083618bd6d69e475a`; records (lesson, QUALITY 152, SCORECARD, this entry, S-row used-by
  updates, census end, the round's own gate runs) in the records commit, gated by `quality/check-receipt-presence.py`
  and `quality/check-seat-reports.py` in `--worktree` mode.
- Measured: C1 at `54a0683c` `TARGET_MET cases=268 correct=268 fresh=120/120 mutants=65 killed=65 oracle_agree=268/268`,
  controls do-nothing 63, naive 62, cache-only 102, base 0 (`.ufo/waves/round-91/receipts/c1-measured-r91.txt`); C2 at
  `0e09349e` `TARGET_MET expectations=59 met=59 fresh=60/60 selftest checks=16 failed=0 mutants=55 killed=55`, controls
  0/5/0/11 (`.ufo/waves/round-91/receipts/c2-measured-r91.txt`). Census 438 → 442 rows, rc 0 both ends
  (`.ufo/waves/round-91/receipts/census-start-r91.txt`, `.ufo/waves/round-91/receipts/census-end-r91.txt`).
- Host answer (`.ufo/waves/round-91/receipts/host-run-r91.txt`): 1211 types named by the host's lists and mime db, tool and
  gio agree on all 1211 (122 with no default); e.g. `text/plain` → nvim, `inode/directory` → Nautilus,
  `x-scheme-handler/https` → chromium, `x-scheme-handler/mailto` → HEY.
- Harm watch at `cbbeb862`: all green (`.ufo/waves/round-91/receipts/harm-final-r91.txt`; SCORECARD round 91).
- Residual r1 (2 seats, measured bytes): C1 and C2 re-measured identically; 18 new C1 fixtures agree with gio; six C2 gate
  defects outside the frozen set routed to round 92 (SCORECARD round-91 errata); all 16 seats left report files
  (`.ufo/waves/round-91/receipts/c2-gate-round91-r91.txt`).

### Round 92 — xdg-open's resolver (capability) and the seat-report gate failing closed (2026-11-06, hyaku run 15, attempt 1)

- Inputs: the round-91 non-author spot-check (routed defects: round-90 GKeyFile statement and portal re-proof; seat-report
  gate F1/F4 and F2/F3/F5/F6; one gate table per lesson); `considerthese/2026-11-06.md` proposal 4 (widen past bar + mako;
  prefer an operator-config gap). Two claims (`.ufo/waves/round-92/claims-declaration-r92.md`): C1 capability, coverage;
  C2 operability. Nudge not claimed.
- Motivating evidence: the lane's round-91 entry, PROVINCE and index said `xdg-open` reduces to GLib; xdg-utils 1.2.1
  `xdg-open` on Hyprland asks `xdg-mime query default` (xdg-open.in:595-596, :664-665, :392-412), and no lane file models
  it (`git grep -l defapp_generic d992ef74 -- tools corpus` empty). On this host the two answers differ for 378 of 1133
  types. The seat-report gate as landed in round 91 skipped a symlinked dispatch in `--rev` with `verdict=OK` and hung on
  a FIFO (R91MResidC2 F1, F4).
- Wave w1: 13 seats (scout 1, scribe 1, executor 5, connector 1, reviewer 2, critic 1, mutation-tester 2), attack 5/13.
  Findings changed the candidate (RFC 6838 type scope, glob escapes and reversed ranges, gawk escapes, `--selftest`,
  directory/gitlink dispatches refused), the counters (bytes clause against shipped interpreters, C2 sandbox and fresh
  leg, pinned round-91 leg with setup-error mapping) and the sets (270 cases from five sources, 81 C1 mutants; 45
  fixtures, 37 C2 mutants) before the freeze. No residual call.
- Landed: freeze `6a0134acb08b26b1cd3c6f0a4b8c63495ca89e3e`; C1 `243326cb884b04bf91c36e6c7565b6f079a8fb7f` (tool, knowledge
  entry, S508–S510, round-91 entry correction, PROVINCE/SKILL/ledger/index rows, host replay); C2
  `297e25153ceb3a4e119eed5b377d7547828d01b6` (gate and its rows); records (lesson, QUALITY 153–154, SCORECARD, this entry,
  round-90 entry correction, S-row used-by updates, measurements, harm watch, census end, w1 evidence) in the records commit.
- Measured: C1 at `243326cb` `TARGET_MET cases=270 correct=270 fresh=120/120 mutants=81 killed=81 oracle_agree=270/270`,
  controls do-nothing 101, naive 78, GLib resolver 139, base 0, bytes clause ok (`.ufo/waves/round-92/receipts/c1-measured-r92.txt`);
  C2 at `297e2515` `TARGET_MET fixtures=45 met=45 fresh=60/60 selftest checks=23 failed=0 mutants=37 killed=37`, controls
  19/7/15, round-91 counter TARGET_MET (`.ufo/waves/round-92/receipts/c2-measured-r92.txt`). Census 442 → 445 rows, rc 0 both ends.
- Host answer (`.ufo/waves/round-92/receipts/host-run-r92.txt`): 1133 types, tool and xdg-mime agree on all; against gio, 375
  types have no `xdg-open` default (282 would open in nvim under gio) and 3 open another application
  (`application/vnd.ms-excel`: xdg-open `chatgpt.desktop`, gio `libreoffice-calc.desktop`).
- Harm watch at `297e2515`: all green (`.ufo/waves/round-92/receipts/harm-final-r92.txt`; SCORECARD round 92).

### Round 93 — portal key-file bytes (edge class) and the selftest-strength gate (2026-11-07, hyaku run 15, attempt 1)

- Inputs: the round-92 non-author spot-check (routed defects: report cross-domain item; land the `tools/mado-portals.py`
  GKeyFile port under its own frozen counter with regenerated round-90 mutants; a weakened passing selftest assertion is
  invisible to the lane's instruments); `considerthese/2026-11-06.md` proposals 4 (operator-config gap) and 1 (survivor
  ledger). Two claims (`.ufo/waves/round-93/claims-declaration-r93.md`): C1 coverage, edge class; C2 operability. Nudge
  not claimed.
- Motivating evidence: the round-90 tool voided a whole `portals.conf` or `.portal` on any invalid UTF-8 byte (comments,
  unread keys, names), stripped VT as whitespace and kept NUL bytes inside values and group lines; GLib 2.90.1 does none
  of these (S511–S514). The base tool answers 32 of the 80 frozen byte-subset cases as the installed xdg-desktop-portal
  does (`.ufo/waves/round-93/receipts/c1-controls-prefreeze-r93.txt`). The round-92 seat-report gate's selftest could be
  weakened (a `want_in` dropped, ids compared as a prefix) with its result line unchanged, and no lane instrument saw it
  (`do_nothing_flagged=0/39`, `.ufo/waves/round-93/receipts/c2-controls-prefreeze-r93.txt`).
- Wave w1: 13 seats (scout 1, scribe 1, executor 5, connector 1, reviewer 2, critic 1, mutation-tester 2), attack 5/13,
  0 dead. Findings changed the candidate (NUL C-string view, continuation bytes after `]`, six selftest checks), the case
  set (229 + 71 byte + 66 review/L1 = 366), the mutants (59 round-90 carried, 9 re-anchored; 16 byte-class), the C2 kill-set
  (20 unique → 32 exact-set kills), the gate (exact-set kills, check-count pin), the C2 counter (rewritten by the L1:
  verdict and exit code, neutral edits, setup panel) and both counters' pins on the frozen bytes — all before the freeze.
- Landed: freeze `65dac61b0a3097d5f4f6f8ccf7444ea60ab27a77`; C1 `0a85e687048ae24f77f043b268794e408d0cc306` (tool, knowledge
  entry `corpus/knowledge/portal-keyfile-bytes-r93.md`, S511–S514, PROVINCE/SKILL/ledger/index rows); C2
  `4fd3b292eb6a96c5c6e471728dbab9ff2a15b99a` (gate, kill-set, SKILL/ledger/PROVINCE rows); records (lesson, QUALITY 155–158,
  SCORECARD, this entry, S-row used-by updates, measurements, harm watch, census end, w1 results) in the records commit.
- Measured: C1 at `0a85e687` `TARGET_MET tool_pin=ok cases=366 correct=366 bytes_cases=80 bytes_correct=80 fresh=120/120
  fresh_bytes=60/60 mutants=75 killed=75`, controls do-nothing 35, r12 74, host-table 10, base 318 / byte subset 32
  (`.ufo/waves/round-93/receipts/c1-measured-r93.txt`); C2 at `4fd3b292` `TARGET_MET positive=OK:0 neutralised_flagged=23/23
  hand_flagged=16/16 neutral_ok=6/6 mutants=22 killed=22`, do-nothing 0/39, always-OK 0/39, always-WEAK fails (i), sha-diff
  0/6 neutrals (`.ufo/waves/round-93/receipts/c2-measured-r93.txt`). Census 445 → 449 rows, rc 0 both ends.
- Harm watch at `4fd3b292` (`.ufo/waves/round-93/receipts/harm-final-r93.txt`): gate selftest 460/460, file plane CLEAN 29,
  index 114/114, ledger 179/179, portals 28/28, mime 17/17, xdgmime 12/12, mako 62/62 (first line a harness defect, corrected
  append-only in the receipt), seat-reports 23/23, receipt-presence 6/6, selftest-strength 11/11 and OK 32/32 on the real
  gate, round-90 C2 83/83 28/28, round-92 C2 45/45 with its round-91 leg; the round-90 C1 counter stops with
  `SETUP_ERROR mutant M03 find occurs 0 times` on the ported tool, as declared (QUALITY 155); unchanged-tool diff empty.

### Round 94 — file name → MIME type (capability) and the selftest-strength gate on two more tools (2026-11-07, hyaku run 15, attempt 1)

- Inputs: the round-93 non-author spot-check (routed defects: an instrument for QUALITY 158; the selftest-strength gate
  wired for one tool only; freeze the portal entry's §8 classes); `considerthese/2026-11-06.md` proposal 4 (one
  operator-config gap over another harness counter). Two claims (`.ufo/waves/round-94/claims-declaration-r94.md`): C1
  coverage, new surface; C2 operability. Nudge not claimed.
- Motivating evidence: no lane tool answered which MIME type GLib gives a file name (`git show
  a3de9972:tools/mado-mimeglob.py` → absent), the step before every gio default-application answer; this host has a user
  `~/.local/share/mime` with both `mime.cache` and `globs2`, so the user's `globs2` is dead text (entry §4). The round-93
  gate could not be pointed at `tools/mado-xdgmime.py` or `tools/mado-mime.py` (no kill-set): the do-nothing instrument
  flags 0 of their 29 single-check neutralisations.
- Wave w1: 14 seats (scout 1, scribe 1, executor 5, connector 1, reviewer 3, critic 1, mutation-tester 2), attack 6/14,
  0 dead. Findings changed the candidate (R94MReviewC1 F1–F7), the case set (235 + 51 + 24 + 55 + 5 L1 = 370), the mutant
  set (57 + 14 L1, 11 excluded with arguments), the C1 predicate (enumerated classes, static no-external-resolver conjunct,
  empty PATH, host database digests), the C2 kill-sets (27 → 46 kills) and panel (12 → 91 hand weakenings) and the C2
  predicate (first-draft control) — all before the freeze.
- Landed: dispatch evidence `5a164538438c2f101e44a79ad9e05aaf3ca910fb`; freeze `bcc5429b68a8b60bc5238fa06f01818686a9d465`;
  C1 `38f77d89310bf9fc752e54e4e98844a9b6ce88cc` (tool, knowledge entry `corpus/knowledge/mime-glob-guess-r94.md`, S515–S518,
  S505 used-by, PROVINCE/SKILL/ledger/index rows); C2 `764d083ad83b8de41bb4331a71f9b8ce237997c1` (two kill-sets,
  SKILL/ledger/PROVINCE rows); records (lesson, QUALITY 159–162, SCORECARD, this entry, used-by updates, measurements, harm
  watch, census end, w1 results) in the records commit.
- Measured: C1 at `38f77d89` `TARGET_MET tool_pin=ok cases=370 correct=370 classes=20/20 static_no_external_resolver=ok
  fresh=120/120 host=9745/9745 mutants=60 killed=60`, do-nothing 43, naive 63, base 0
  (`.ufo/waves/round-94/receipts/c1-measured-r94.txt`); C2 at `764d083a` `TARGET_MET positive=OK:0,OK:0
  neutralised_flagged=29/29 hand_flagged=91/91 neutral_ok=6/6 control_hand_flagged=45/91`, do-nothing 0, always-OK 0,
  sha-diff 0/6 (`.ufo/waves/round-94/receipts/c2-measured-r94.txt`). Census 449 → 453 rows, rc 0 both ends.
- Harm watch at `764d083a` (`.ufo/waves/round-94/receipts/harm-final-r94.txt`): all green as listed in SCORECARD round 94;
  the round-90 C1 counter's declared SETUP_ERROR on the ported portal tool unchanged.

### Round 95 — GLib content-type guess given file bytes (capability) and the selftest-strength gate on two more tools (2026-11-07, hyaku run 15, attempt 3)

- Inputs: the round-94 non-author spot-check (routed defect 3: two of the five unguarded tools — `tools/mado-mimeglob.py`
  and `tools/mado-portals.py` — get kill-sets under the unchanged round-93 gate; defects 1, 2, 4, 5 dispositioned in the
  lesson's Gate block); `considerthese/2026-11-06.md` proposal 4 (a content-sniffing step after the filename guess).
  Two claims (`.ufo/waves/round-95/claims-declaration-r95.md`): C1 coverage, new surface; C2 operability. Nudge not
  claimed.
- Motivating evidence: no lane tool answered which MIME type GLib gives a byte string with a name, cache and text mode —
  the step `g_content_type_guess_for_data` performs before `xdg-open`/gio act on a file; round 94's `mado-mimeglob.py`
  covers the name-only half. The round-94 gate still could not be pointed at the two ported tools (no kill-set): the
  do-nothing instrument flags 0 of their 75 hand weakenings.
- Wave w1: 14 seats (scout 1, scribe 1, executor 5, connector 1, reviewer 3, critic 1, mutation-tester 2), attack 6/14,
  0 dead. Findings changed the candidate (`c1` → `c1b` → `c1c`: VT/isspace table port, 301-stub digest handling, text
  mode), the case set (300 cases / 2863 inputs / 20 classes), the mutant set (94 counted, 5 excluded with arguments), the
  C1 predicate (enumerated classes, `class_kills`, `real_rebuild`, host leg, audit-hook launcher, forgery leg), the C2
  kill-sets (first drafts → c2b: 22 + 42 kills) and panel (75 hand weakenings, 47 single-check neutralisations, 36/47
  singleton labels) and the C2 predicate (first-draft control, ≥2 neutrals per tool) — all before the freeze.
- Landed: freeze `a689d2e3dc968c6909a7dce0575cd392ecc57109`; C1 `9afa39f5342fe19b661513b4de9854324508da84` (tool,
  knowledge entry `corpus/knowledge/mime-magic-sniff-r95.md`, S519–S523, S505 used-by, PROVINCE/SKILL/ledger/index
  rows); C2 `6f6955f9cf6ff9bf8f5e769f6b8d8ff79ac55ce3` (two kill-sets, SKILL/ledger/PROVINCE rows); records (lesson,
  QUALITY 163–165, SCORECARD, this entry, used-by updates, measurements, harm watch, census end, w1 results) in the
  records commit.
- Measured: C1 at `9afa39f5` `TARGET_MET tool_pin=ok cases=300 correct=300 classes=20/20 fresh=120/120 host=9822/9822
  mutants=94 killed=94 class_kills=20/20 real_rebuild=11/11 static_no_external_resolver=ok audit_denials=0`, controls
  do-nothing 17, name-only 57, naive 186, base 0, memoriser_fresh=0/120
  (`.ufo/waves/round-95/receipts/c1-measured-r95.txt`); C1 re-run at tip `6f6955f9` TARGET_MET with memoriser_fresh=1/120
  (`.ufo/waves/round-95/receipts/c1-at-tip-r95.txt`); C2 at `6f6955f9` `TARGET_MET positive=OK:0,OK:0
  neutralised_flagged=47/47 hand_flagged=75/75 neutral_ok=6/6 control_hand_flagged=28/75 singleton_labels=36/47
  tool_pin=ok,ok` (`.ufo/waves/round-95/receipts/c2-at-tip-r95.txt`); C2 at `9afa39f5` `SETUP_ERROR … kill-sets absent`
  rc 2 (`.ufo/waves/round-95/receipts/c2-at-c1-r95.txt`). Census 453 → 458 rows, rc 0 both ends.
- Harm watch at `6f6955f9` (`.ufo/waves/round-95/receipts/harm-final-r95.txt`): all green as listed in SCORECARD round 95;
  the round-90 C1 counter's declared SETUP_ERROR on the ported portal tool unchanged.

## Round 96 — the TEXT MIME database's magic step (capability), the last gate-compatible tool guarded (2026-11-07, hyaku run 15, attempt 1)

Declaration `.ufo/waves/round-96/claims-declaration-r96.md` (freeze `b056290d`, w1 findings folded in before the
freeze and listed there; lesson `corpus/lessons/round-96.md`). C1 measured at `5dd921b3` (`tools/mado-mimetext.py` =
frozen candidate, sha256 `d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd`; counter
`quality/counters/c1-r96-magictext.py` `9d3e1e76…a7f7`); C2 measured at `f54def27`
(`quality/check-receipt-presence.py` = `be716a63…c962`; kill-set `305d735f…a495`; gate unchanged `2d6f1219…a61b`).
Stagnation nudge not claimed (capabilities entered at rounds 88–95); every owned axis at 10, so the lowest-axis duty
is a tie. Sourced claim: C1 (S524, S525, S505, S520, S521, S522, S523 — S524/S525 opened this round). C2 answers the
round-95 spot-check's routed defect 3 for the last gate-compatible tool.

- C1 — coverage, new surface (capability): no lane tool answered the text `mime/magic` database at base (the r95 tool
  refuses text mode); `tools/mado-mimetext.py` now answers 284/284 frozen cases (16/16 classes), 268/268 seeded fresh
  inputs, 9822/9822 host pairs over the round-95 4911-file list against the host's own cache-free text database, and
  84/84 counted mutants (class_kills 16/16); controls: do-nothing 0/259 text-mode, name-only 32/284, naive 101/284,
  memoriser 0/40 fresh, ctypes-libgio forgery rejected (`audit_denials=5`); `checks=50 failed=0`
  (`.ufo/waves/round-96/receipts/c1-measured-r96.txt`). Entry `corpus/knowledge/mime-textdb-magic-r96.md`; index and
  frontier rows; SKILL and PROVINCE rows.
- C2 — operability: `quality/check-receipt-presence.py` gains six distinct selftest labels and its selftest block
  after `main()` (the gate's `non_selftest_prefix` then covers the production path), and
  `quality/selftest-kills/check-receipt-presence.json` guards it under the unchanged round-93 gate: hand weakenings
  flagged 0/31 → 31/31, single-check neutralisations 0/6 → 6/6, singleton labels 6/6, neutral edits OK 6/6, controls
  (do-nothing 0, always-OK 0, always-WEAK WEAK:1, first draft 19/31), round-90 main-path leg TARGET_MET 83/83
  (`.ufo/waves/round-96/receipts/c2-measured-r96.txt`).
- Separability: C1 TARGET_MET at the C2 tip (`receipts/c1-at-c2-r96.txt`); C2 SETUP_ERROR (kill-set absent) at the
  C1 tip (`receipts/c2-at-c1-r96.txt`).
- Frontier: SOURCES 458 → 460 rows (S524 `xdgmimemagic.c`, S525 spec §2.5); used-by appends on S505/S519–S523;
  {C1} = S524/S525; census start/end rc 0. Mistakes: M96-1 (63-hex oracle pin), M96-2 (a `mime.cache` proxy read as
  cache mode, five mislabelled refusal cases) → QUALITY 166; QUALITY 167 (selftest after the production path).
- Assimilation: none (94 staged-id collisions; no staged entry on this plane). considerthese 2026-11-07 proposal 3
  (an exhaustive small-domain sweep; here the oracle-labelled case set) is the mined proposal.

- **Correction (appended, round 96):** the r96 entry's §9 first said the cache version sits "at bytes 4..7"; the
  library reads it at offsets 0..3 (BE u16 major, then minor), which is what the frozen counter's `loadable_cache`
  and the five refusal fixtures use. Corrected by the entry's §10 erratum; no measurement moves.

## Round 97 — the path's content type (capability), the round-96 counters' self-invocation (2026-11-07, hyaku run 15, attempt 1)

Declaration `.ufo/waves/round-97/claims-declaration-r97.md` (freeze `78e9ccdd`; corrected before the freeze on the
wave's measured findings, listed in its `## Freeze` block). C1 measured at `4541d94b` (`tools/mado-filetype.py` =
frozen candidate `da6af7a0…8a44d2d8`; counter `quality/counters/c1-r97-filetype.py` `745a341e…195ba9e0`); C2 measured
at `65ff5591` (the two round-96 counters with `--selftest`: `c1-r96-magictext.py` `4f678384…aaa64d`,
`c2-r96-selftest-kills.py` `54143b8a…002217b`; counter `quality/counters/c2-r97-counter-selftest.py`
`abb17a01…06b879`). Stagnation nudge not claimed (capabilities entered at rounds 88–96); every owned axis at 10, so
the lowest-axis duty is a tie. Sourced claim: C1 (S522, S526, S527, S518, S521, S515, S516, S519, S520, S524, S525;
S526/S527 opened this round).

- C1 — coverage, new surface (capability): no lane tool answered a *path's* content type at base; `tools/mado-filetype.py`
  now answers GIO 2.90.1's `standard::content-type` / `standard::fast-content-type` — the stat branches in order
  (symlink broken/nofollow, directory, chardev, blockdev, FIFO, zero-size regular, socket), the alias rewrite, the
  basename-only guess and its uncertain states, and the sniff of the database's own max extent (clamped to 16384)
  taken only when not `--fast` and uncertain — 157/157 frozen cases (15 classes), 101/101 counted mutants
  (class_kills 15/15), 140/140 fresh paths from a measurement-time seed, 6194/6194 frozen host labels (0 mismatches,
  0 drift), `checks=40 failed=0`; controls name-only 39/157, naive 67/157, memoriser 0/140 fresh, ctypes forgery
  rejected (`audit_denials=0` on the candidate, 3 on the forgery)
  (`.ufo/waves/round-97/receipts/c1-measured-r97.txt`). Entry `corpus/knowledge/gio-content-type-file-r97.md`; index
  and frontier rows; SKILL and PROVINCE rows; SOURCES 460 → 462.
- C2 — operability: the two round-96 counters gain a `--selftest` self-invocation mode (10 checks each, stable `st-*`
  ids, fixtures resolved from the counter's own path so the landed `quality/counters/` layout is green), the C2
  counter scores it (18/18 neutralisations flagged with their declared ids, 6/6 broken modes named, base bytes
  refuse `--selftest` rc 2, the echo stub credited with none of the 18, registry 1 → 3 instrument rows re-derived at
  both revisions, ledger membership 2/2) (`.ufo/waves/round-97/receipts/c2-measured-r97.txt`). SKILL registry rows for
  the two counters and the receipt-presence kill-set named inside the strength row's population; ledger rows for the
  tool and both counters.
- Separability: C1 re-run at the C2 tip (`receipts/c1-at-c2-r97.txt`); C2 at the C1 tip (`receipts/c2-at-c1-r97.txt`).
- Frontier: SOURCES 460 → 462 rows (S526 `gcontenttype-fdo.c` sniff length, S527 `gio(1)` info contract); used-by
  appends on S505/S515/S516/S518/S519/S520/S521/S522/S524/S525; census start/end rc 0. Mistakes M97-1..M97-6;
  QUALITY 168–169.
- Assimilation: none (the staged package has no entry on the content-type caller plane; the id-collision check is
  `.ufo/waves/round-97/assimilation/`). considerthese: no still-unimplemented proposal matched this round's surface;
  the 2026-11-07 proposal 3 (an exhaustive small-domain sweep) was already mined in round 96.
- Round shape: wave w1 (14 seats, 5 attack) plus wave w1b (10 seats, 5 attack) re-dispatched after four seats died on
  a provider 401; round total 24 seats. Dead seats: w1 R97MScoutSources, R97MExecC2, R97MMutC2 (no report; their
  items were covered by w1b), w1 R97MExecCasesC1/R97MExecToolC1/R97MExecC2/R97MExecCounterC2 died on the 401 and
  were replaced in w1b; no dead seats in w1b.

## Round 98 — the launch argv sequence (capability), the registry citation read-back (2026-11-07, hyaku run 15, attempt 1)

Declaration `.ufo/waves/round-98/claims-declaration-r98.md` (frozen at the artifacts commit `06b6bf2a`; its
`## Freeze block` carries every pin and lists the pre-freeze corrections). C1 measured at `a3471631`
(`tools/mado-execargv.py` = `49f7fecd…f713`; counter `quality/counters/c1-r98-execargv.py` `7ed2f8f6…a64c5`;
cases `21cccc3a…e370e`; mutants `32c207b3…53bb`; renderer `182cf06c…e3d4`); C2 measured at `a3471631`
(`quality/check-sources-readback.py` = `f1000bf1…d8f5`; counter `quality/counters/c2-r98-sources-readback.py`
`e944fdac…e6e0a`).

- C1 — coverage, new surface (capability): no lane tool answered a launch argv at base; `tools/mado-execargv.py`
  now answers the **sequence of argv vectors** GIO 2.90.1 builds and spawns from a desktop entry's `Exec` key and a
  file/URI list — the load gate and its five refusal shapes, the byte walk with the selector byte consumed, the
  twelve field codes and `%%`, `force_file_uri` and `X-GIO-NoFuse`, the head-pointer no-substitution `%f` append,
  `g_shell_quote`, the `g_shell_parse_argv` grammar, and the `do { } while (dup_uris != NULL)` loop that spawns
  once per URI for the single-consuming codes — 88/88 frozen cases over 20 classes (20/20), 79/79 counted mutants
  (class_kills 20/20, 0 crashed, 0 survived), 60/60 fresh cases at seed `e2bf4d1b757e2e7b`, controls behind
  (naive 4/88, field-code 47/88, memoriser 0/60 on fresh), `checks=38 failed=0`
  (`.ufo/waves/round-98/receipts/c1-measured-r98.txt`). Entry `corpus/knowledge/gio-exec-argv-r98.md`; index and
  frontier rows; SKILL and PROVINCE rows; SOURCES 462 → 466.
- C2 — operability: `quality/check-sources-readback.py` reads the registry back from every entry's `source:`
  frontmatter (R1 recheck-path, R3 usedby-missing, R4 entry-cites-unacknowledged over `mined` rows, R5
  missing row, R6 duplicate id) and the 21 unacknowledged citations it found are repaired row → entry (21/21,
  `added_paths=21`), with the gate green at 466 rows / 119 entries, planted 5/5, the always-clean stub flagged,
  the fleet census exit 0, gate selftest 21 checks, counter selftest 18 checks
  (`.ufo/waves/round-98/receipts/c2-measured-r98.txt`). The two disowned citations (S030 rejected, S132 queued)
  are recorded in the lesson with their entries' sentences and are not repaired.
- Separability: C1 `SETUP_ERROR … tools/mado-execargv.py absent at 35f3ce80` (`receipts/c1-at-base-r98.txt`);
  C2 `SETUP_ERROR gate-absent-at-rev` (`receipts/c2-at-base-r98.txt`).
- Frontier: SOURCES 462 → 466 rows (S528 gdesktopappinfo.c launch expansion, S529 gshell.c quoting/tokenizer,
  S530 the Desktop Entry Specification's Exec section, S531 the installed `gio(1)` `launch` scope); used-by appends
  on S504, S506, S527 and the 21 repaired cells; census start/end rc 0. Mistakes M98-1..M98-6 in
  `corpus/lessons/round-98.md`.
- Assimilation: none (the staged `merge/mado/` package has no entry on the launch plane; `Assimilation: none` in
  the report's Sources & frontier section). considerthese: no still-unimplemented proposal matched this round's
  surface.
- Round shape: one v1 wave w1 of 11 seats (4 executors, 2 mutation-testers, 1 scout, 1 scribe, 1 connector,
  1 reviewer, 1 critic; attack 4/11 = 36 %); no residual call; no dead seats; round total 11.

## Correction (round 99 — the round-98 entry above)

The round-98 entry's own numbers are corrected here, append-only; the entry's claims and verdicts are not
rewritten. Source: `corpus/lessons/round-98-verifier-spotcheck.md` section 5 (D4, D8) and the receipts it
names.

- **Fresh seed.** The entry says the C1 fresh leg ran at seed `e2bf4d1b757e2e7b`; the receipt
  `.ufo/waves/round-98/receipts/c1-measured-r98.txt` and the report both print
  `fresh_seed=f00d3edcdb285ac0`. The measured value is `f00d3edcdb285ac0`; `e2bf4d1b757e2e7b` is the
  generator's *input* seed line, not the frozen run's seed. Re-derive:
  `grep -o 'fresh_seed=[0-9a-f]*' .ufo/waves/round-98/receipts/c1-measured-r98.txt`.
- **Mistake count.** The entry says "Mistakes M98-1..M98-6"; `corpus/lessons/round-98.md` holds M98-1
  through M98-12. Re-derive: `grep -c '^\*\*M98-' corpus/lessons/round-98.md` -> 12.
- **C2 commit attribution (D8).** The entry's prose attributes the 21-path repair and the
  S504/S506/S527 `used-by` additions to one commit. They are two: the 16-row/21-path repair landed at
  `06b6bf2a` and the entry plus the three `used-by` cells landed at `020af865`. Re-derive:
  `git log --oneline 06b6bf2a..020af865 -- corpus/SOURCES.md corpus/knowledge/gio-exec-argv-r98.md`.
- **Registry numbers (D2).** The entry's "466 rows / 119 entries" is the *records* state (`020af865`+),
  not the gated revision: the gate ran at `a3471631`, which has 462 rows / 118 entries. Round 99 re-runs
  the gate at the records tip and commits the receipt; the numbers are not rewritten here.

## Round 99 — the launch spawn environment (capability), the harm watch as an instrument (2026-11-07, hyaku run 15, attempt 4)

Declaration `.ufo/waves/round-99/claims-declaration-r99.md` (freeze block filled after wave `w1`; the
attempt-3 measurement note records the `--rev HEAD` invocation error and the re-run). Claim text narrowed
before filing under the pre-file falsification rule: `plans/round-99.md` A1 (the base already holds the
`g_find_program_for_path` primitive in `tools/mado-mime.py:467`), A3 (the predicate's `selftest_checks` is
the counter's fixture selftest, not the gate's `--selftest`), A4 (a per-leg setup error aborts the
remainder), A5 (`r97c2_counter_selftest` was already named in `harm-final-r98.txt:41-43` at `fa4445af`;
only `r97c1_filetype` was spot-check-only) and A6 (count/duplicate/round-missing census checks are gate
behaviour, not counter-verified). A2/A7/A8 are errata and named limits. Ledger:
`.ufo/waves/round-99/claim-falsification.tsv` (8 rows, 6 attack seats read).

- C1 — coverage, new surface (capability): no lane tool answered the launch spawn environment at base;
  `tools/mado-launchenv.py` now answers the composite around a launch argv — the load gate (`TryExec`
  then `Exec`, each through `g_find_program_for_path(program, process PATH, Path=)`, and the
  executable-and-not-a-directory test, with the `Unable to load application information` refusal), the
  twelve-row `known_terminals` table in order with its `exec_arg` column and the `Terminal=true` prepend,
  the post-prepend `argv[0]` lookup with its `Program ‘x’ not found in $PATH` refusal, `Path=` as the
  child's cwd (empty inherits, unenterable fails with `cwd-failed`) and as the working directory of the
  four searches, and `GIO_LAUNCHED_DESKTOP_FILE`. Measured at `56a9b299`: 67/67 frozen cases over 31/31
  classes, 69/69 counted mutants killed (class_kills 31/31, 0 crashed, 0 survived), 60/60 fresh cases at
  seed `7d00c2c940ceb88e`, controls behind (naive 1/67, held round-98 argv tool 4/67), tool selftest
  90/90 (`.ufo/waves/round-99/receipts/c1-measured-r99.txt`). Entry
  `corpus/knowledge/gio-launch-env-r99.md`; README index/frontier; SKILL and tool-ledger rows; SOURCES
  466 → 469.
- C2 — operability: `quality/harm-watch.py` replays the frozen 28-leg panel, each leg with a frozen `rc`
  and stdout marker, after a census that fails closed on a leg the panel declares but does not carry (the
  count finding net of the explained delta, plus duplicate, round-missing, unknown and missing ids); each
  leg runs with a timeout under the caller's scratch root. The counting command at `3b69f041`:
  panel_legs 28/28, legs_run 28, **mismatches=2** — `r92_gate_defects` and `r97c1_filetype` both hit the
  panel's frozen 600 s per-leg cap (`rc=124 timeout-after-600s`) under fleet load; the two-leg probe at a
  short scratch root reproduces both (`receipts/c2-probe-r99.txt`). The five planted panels are all
  caught, the marker-blind gate copy is rejected, the always-OK stub is flagged and the counter selftest
  is 17/17, but the frozen `mismatches == 0` conjunct is unmet: **TARGET_MISSED, honest stop** (A9); the
  target is not narrowed after landing and the panel-timeout repair is routed to round 100. The
  attempt-3 `TARGET_MET` line left no receipt; the attempt-4 re-derivation is the reported value. The
  panel restores both round-98 dropped legs (`r97c1_filetype`, `r97c2_counter_selftest`; the latter is a
  base-rev replay by its own pins, named limit A7).
- Separability: C1 `SETUP_ERROR … tools/mado-launchenv.py absent at 2cbaa141`
  (`receipts/c1-at-base-r99.txt`); C2 `SETUP_ERROR … quality/harm-watch.py absent at 2cbaa141`
  (`receipts/c2-at-base-r99.txt`).
- Frontier: SOURCES 466 → 469 rows / 119 → 120 entries (S532 `gio-tool-launch.c`, S533 `gutils.c`, S534
  the Desktop Entry Specification recognised keys; all tier A, opened 2026-11-07); `used-by` appends on
  S504, S506, S528, S529, S531; census start/end rc 0; read-back gate `rows=469 entries=120 findings=0`.
  Mistakes M99-1..M99-3; QUALITY 170–172.
- Assimilation: none (the staged `merge/mado/` package holds no entry on the launch/terminal/`Exec`
  plane; the closest staged entry is the systemd unit fragment plane). considerthese: no
  still-unimplemented proposal matched this round's surface.
- Record repairs (round-98 spot-check D1–D8): S532–S534 rows (D1), readback receipt at the records tip
  (D2), the two r98 SKILL pins (D3), the LOG r98 seed/mistake-count erratum (D4), the panel (D5),
  QUALITY 170 (D6), this report (D7), the C2 two-commit attribution (D8).
- Round shape: one v1 wave `w1` of 12 seats (4 executors, 2 mutation-testers, 2 reviewers, 1 critic,
  1 scout, 1 scribe, 1 connector; attack 6/12 = 50 %); no residual call; no dead seats; round total 12.
  The planner seat is the L1 (validator-frozen role); the bounded planning data-walk rode the scout and
  the records reviewer.
