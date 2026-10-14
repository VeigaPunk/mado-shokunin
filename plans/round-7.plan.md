# WWKD plan — mado round 7 (ufo-round-plan-v1)

Design lane: PREP-M7 (2026-10-14; round-6 32-lane wave, width 32; mado
round-6 work in flight). Everything below was read at design time by this
lane — freeze 2026-10-14T17:40Z — not taken from the record; every pin is
re-measured at dispatch. Round-6 clauses (a) mutation proof / (b) omarchy
drift arm / (c) remaining-planes live note are this plan's precondition
set, checked at dispatch, never assumed.

Design-time state (measured, read-only; re-measure at dispatch):
- HEAD `c03c249`, `git status --porcelain` empty; LOG's last entry is
  round 5; `plans/round-6.plan.md` committed (`eead56b`, 3,564 B / 54 L).
  Second read 17:47Z (polls while drafting): round-6 artifacts had landed
  untracked — `corpus/knowledge/omarchy-drift-watch.md` (18,477 B, 17:44Z),
  `corpus/knowledge/remaining-planes-census.md` (20,512 B, 17:43Z; the
  note is *census*, not the round-6 plan's working name
  `remaining-planes-live.md`), `plans/round-6-record-draft.md` (26,186 B) —
  in flight, content not consumed; paths re-resolved at dispatch.
- Gate `tools/mado-verify.sh` sha256
  `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13`,
  1,098 L by `wc -l` — unchanged from
  the round-5 record at this read (round-6 edits had not landed). Modes
  verify/--no-live/--selftest/--root; verdict `MADO_VERIFY:
  CLEAN|DIVERGED`; exit map 0/1/2; selftest 28/28 per the round-5 record
  (27 assertion-helper call sites counted at this read; the selftest was
  not executed — re-measure at dispatch); plane prefixes `hypr|hypr-live|
  waybar|walker|terms|gate`; 106 `row` + 6 `row_from_rc` call sites
  (`grep -cE '^[[:space:]]*row '` / `…row_from_rc `).
- The two measured gaps this move closes: the theme's only live row is
  `live.theme.current NOTE` "operator-owned; not a verdict input"
  (`:1014-1021`); walker live = version pin (`:989-998`) + services
  (`:1000-1011`) — sockets, D-Bus identity, layer state unverified.
- Live anchors (probes 17:39–17:41Z, read verbs only): `omarchy theme
  current` → `Matte Black`; `theme.name` → `matte-black` (12 B);
  `current/background` symlink → `theme/backgrounds/0-ship-at-sea.jpg`;
  swaybg PID 1203358 argv `-i …/current/background -m fill`;
  `hyprctl -j layers` DP-1 level 0 `wallpaper`, level 2 `waybar`, no
  walker surface (closed); walker PID 1203471 `--gapplication-service`,
  elephant PID 1203474, both units `active`; `walker.sock` /
  `elephant.sock` mode `srwxr-xr-x`, 0 B, under `$XDG_RUNTIME_DIR`;
  `dev.benz.walker` owner PID 1203471; consumer declarations
  `hyprland.conf:13`, `hyprlock.conf:1`, `waybar/style.css:1`,
  `alacritty.toml:1`, mako `config` symlink → theme `mako.ini`; running
  consumers swayosd-server 1203475, mako 1203350; installed-consumer
  census recorded (btop, obsidian, chromium, nvim, gum, fastfetch,
  lazygit, starship in; foot/kitty/ghostty/helix/code out).
- Debt carried: `corpus/lessons/` still 0 entries (sixth round);
  `find corpus -name '*.sh'` → 0 (round-1 ceiling retired via `tools/`).

Candidate decision: the three post-watch-arms candidates (gate regression
mode; the theme/wallpaper plane; walker live-surface coverage) are one
move here, not three — each is the same artifact, the gate, closing over
a dimension the round-6 watch arms left open: time (its own proof becomes
re-runnable) and surface (two declared planes it observes only as notes
today). "Regression mode" is resolved to the fleet idiom measured in
tameshi (`tools/mutate-and-run.sh:66-81`): re-run recorded cases over
fresh copies, revision pins, a stated band, exit map 0/1/2 — not a new
stateful run-over-run diff (rejected reading, recorded: the gate's per-pin
rows already name drift against recorded pins; a snapshot diff would add
state without a new falsifiable class).

Axis move: operability + coverage — ONE move, three ordered stages: the
gate's own proof becomes a gate (a); then the gate's declared census
closes over the theme/wallpaper plane (b) and the walker live surface
(c), and both widenings run under (a), so a widened gate cannot quietly
regress the contracts round 6 proved.

Claim:
(a) Regression mode — `tools/mado-verify.sh --regression`: re-runs the
    round-6 mutation case (case artifacts resolved from the round-6
    record/commit at dispatch — planned
    `corpus/knowledge/gate-mutation-proof.md`; if the record leaves no case, (a) refuses
    with SETUP and the round reports, no headline). Contract mirrors
    tameshi's: target pin = the gate revision the sweep measured (a live
    mismatch is a SETUP refusal; the recorded table is revision-tied);
    suite `bash "$MUTANT" --selftest` (the landed selftest re-invokes
    `"$0"`, `:406`); pre-stated band — defects exactly the recorded
    count, |killed − recorded| ≤ 1, ≤ 1 verdict flip, control green,
    `MUTATE_RESTORE: OK` required before any PASS; outside the band is
    FAIL; a case that cannot run is SETUP. Token `MADO_REGRESSION:
    PASS|FAIL|SETUP` (never `MADO_VERIFY:`); exit 0/1/2 aligned by
    meaning; `--target/--defects/--suite` refused (usage). The harness
    is consumed read-only (a needed change is a recommendation to
    tameshi, never a patch); scratch only under
    `/tmp/mado-verify-regression.*`. From round 7 every gate-widening
    claim carries `MADO_REGRESSION: PASS`.
(b) Theme/wallpaper plane — new declared rows. File plane: `theme.name`
    parsed and pinned; `current/background` symlink resolves inside
    `current/theme/backgrounds/` to a non-empty file; consumer
    declarations resolve for installed consumers only (`hyprland.conf:13`,
    `hyprlock.conf:1`, `style.css:1`, `alacritty.toml:1`, mako config
    symlink). Live plane: `omarchy theme current` agrees with `theme.name`
    under the measured normalization rule (`Matte Black` ↔ `matte-black`;
    a pair the rule does not join is recorded, never forced); swaybg argv
    names the background symlink and the level-0 `wallpaper` layer pid ==
    swaybg pid. The theme *choice* stays NOTE (operator-owned); chain
    *integrity* becomes verdict input; every mutating verb (`omarchy
    theme set`; `omarchy-theme-bg-*`) stays fenced. Theme parts whose live
    chain stays unresolved (`walker.css`, `swayosd.css`, `btop.theme`,
    `themed/*.tpl.sample` rendering) get their exact probe recorded,
    never an inferred consumer.
(c) Walker live surface — live rows for runtime identity: sockets exist
    with mode + size (`srwxr-xr-x`, 0 B); `dev.benz.walker` owner pid ==
    the walker pid; layer invariant — if a walker namespace appears in
    `hyprctl -j layers` its pid == walker pid; absence is a NOTE (the
    launcher is closed; the gate never opens it). Version/services rows
    stand. Rendered UI and the socket protocol stay UNKNOWN by constraint
    (never opened, never connected); resolutions append to
    `walker-deep.md` §10/§11 as errata.
Ordering: (b) and (c) are gated on (a) green — they widen the very census
and live plane the mutation spec's clauses guard; (a) is gated on round
6's mutation result. If (a) cannot land, (b)/(c) do not ship and the
round says why.
Anti-claim: a kill-rate outside the band is a FINDING (append-only
errata, not smoothed); any unverifiable surface reads UNKNOWN, never
CLEAN; the gate observes the theme plane and never sets it; absent
consumers stay declared-only rows; the normalization rule is measured on
this host's one theme, not assumed general; no compositor/session
mutation (no launcher open, no socket connect, no `omarchy theme set`);
dependencies read-only — tameshi harness and omarchy payload untouched.
Measure: `MADO_REGRESSION: PASS` + `REGRESSION_TABLE`-shaped lines (case,
expected vs observed, band, flips, restore sha before = after, target
sha) + selftest count before → after (28 → 28+N); gate row census before
→ after by plane prefix (the selftest's prefix awk `:352/:356` extended
for any new plane id — counted); theme chain rows vs the design-time pins
above; walker live rows; SKILL gate section (`:460-495`) gains the mode;
SCORECARD move row + LOG entry carrying the commands.

Open unknowns at draft: whether round 6 lands its three clauses, and
under which gate sha; where the round-6 mutation case lives and its band
(may differ from tameshi's — the recorded band, not this plan's shape,
is authority); whether round 6 added plane ids the census awk must
include; whether the `Matte Black` ↔ `matte-black` normalization rule
generalizes beyond this host's single theme; the live consumer of
`current/theme/walker.css` and `swayosd.css`; `corpus/lessons/` debt
(sixth round, still 0 entries).