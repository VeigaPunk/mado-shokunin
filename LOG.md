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
