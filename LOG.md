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
