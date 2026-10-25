# ConnSiblingOverlap — sibling-lane overlap scan (round 40, w1)

Seat: ConnSiblingOverlap-2. Read-only. Reports overlap of sibling lanes with mado's
`--live`/getoption option-table surface (C1) and the K1/K2 (claims C1/C2)
assimilation scope (host bar producers, round-40 registration.md:100-110).

## Evidence read

- Fleet: `MISSION.md` (lanes/axes contract), `AXES.md` (depth/coverage/operability/
  freshnessnesscalibration/adjacency; adjacency = report, never absorb).
- Lane provinces: tsukuroi, mori, kama, tameshi, kake, souji, kumitate, chousa,
  kotodama, kasegi, kagi, kengaku, kotoba, kaidoku, tabi, revenger, lore, audio,
  game-dev-2d, game-dev-3d, mado (all 21 siblings).
- Held mado entry: `corpus/knowledge/waybar-walker-semantics.md` (MADO-R3-1; maps
  the 19 waybar modules and names the producer scripts).
- Greps over every sibling's `corpus/ tools/ scripts/ SKILL.md PROVINCE.md
  SCORECARD.md` (non-wave) for `hyprctl|getoption|hyprlang|waybar|active_border|
  omarchy|ai-usage`: only the hits cited below exist; all other lanes returned zero.

## 1. The getoption / option-table surface — mado-exclusive

No sibling lane claims the compositor option table or runs `hyprctl getoption`.
Evidence of mado ownership and of sibling boundaries that keep it mado's:

- mado `PROVINCE.md:3-16` owns `~/.config/hypr/`, `~/.config/waybar/`,
  `~/.config/walker/`, terminal/themes/idle; config trees read-only.
- mado `SKILL.md:8` ("desktop & compositor craft playbook — the Hyprland/waybar/
  walker/terminal config plane"), `:156`, `:211` (`hyprctl layers -j`),
  `:359` (`hyprctl getoption <key>` value+set used for shadowing checks).
- mado `tools/mado-options.py` exists at base (round-40 registration recount:
  base `n=71`, selftest); option-table knowledge entry
  `corpus/knowledge/config-option-table-r39.md:1-14` (round-39 C3) resolves
  key ownership via S218/S220/S162/S173.
- tsukuroi routes configuration-level desktop diagnosis **to mado**:
  `PROVINCE.md:48` (ADJ-03: "Desktop rendering, bindings, menu or idle behavior
  needs configuration-level diagnosis … → mado"); `PROVINCE.md:124` (OUT-004
  quote: "Mado owns the Hyprland, waybar, walker and terminal configuration
  plane"). Tsukuroi's core is package/systemd/driver/boot, not compositor options.
- mori `PROVINCE.md:12-16` refuses OS/compositor state (observability only).
- kama `PROVINCE.md:3-15` owns endpoint health; mado `.ufo/evidence/round-12/
  l2-connector.md:10` records the explicit split: "Mado owns desktop display
  (waybar `custom/ai-usage`, hypr float rules); kama owns endpoint process and
  port health."
- tameshi `PROVINCE.md:14-17` owns the *verification method* and refuses product
  domains ("every lane's gate remains its own"); its `mutation-case-mado-verify.md`
  treats mado's `tools/mado-verify.sh` as a read-only mutation surface (including
  `hyprctl` PATH-starvation scenarios) — method adjacency, not option-table
  ownership.
- kaidoku `corpus/knowledge/2026-10-13-crash-evidence.md:15-26,50-54` RE'd waybar
  **coredumps** (crash artifacts); touches the waybar binary crashes, no config/
  option surface.
- tabi `corpus/evidence/round-19/validation/decisions.json:339` `GetOptionList()`
  is a browser select-option DOM/schema token (S077 form_mcp_schema.cc), unrelated
  to `hyprctl getoption`.
- audio: waybar appears only as a PipeWire **client** in `corpus/live/…/
  pw-dump.json` (`application.name: waybar`) and `pactl-clients.txt` — stream
  observation, not config ownership.

→ Verdict: no overlap. C1's `--live` verb stays inside mado's sole surface; no
sibling needs coordination at the option-table level.

## 2. Waybar producers (assimilation scope) — complementary touchpoints

Producer inventory from the held entry (`waybar-walker-semantics.md`):
`weather.sh` (`:135`), `omarchy-update-available` (`:136`),
`indicators/screen-recording.sh` (`:138`), `indicators/idle.sh` (`:139`),
`indicators/notification-silencing.sh` (`:140`), `omarchy-voxtype-status`
(`:137`), `ai-usage` CLI + `ai-usage.timer` (`:149`), signal bus `:178-194`.
The producer scripts live under the omarchy skill tree (mado
`PROVINCE.md:10-12`: omarchy = documentation surface, read-only); the consumers
are in `~/.config/waybar/config.jsonc` (mado-owned).

No sibling owns these producers. Two siblings have genuine, complementary
touchpoints on the **ai-usage** producer:

1. **tsukuroi — systemd timer census (timer half of the producer).**
   `SKILL.md:47` (user systemd units & timers row: "only `ai-usage.timer`
   active (≈5-min cadence; last run 09:52:56, Result=success)");
   `SKILL.md:643` (enabled user timers = exactly `ai-usage.timer`);
   `tools/tsukuroi-census.sh:1950` / `:2279` (fixture + drift check on
   `ai-usage.timer`). Tsukuroi tracks the timer's arm/result state; it does not
   read the producer's cache or the bar chip. mado's assimilation scope ("gkeep/
   ai-usage producers' current-output decidability") is the chip/cache side.
   Both lanes observe the same timer without conflict.
2. **kake — cache consumption.** `corpus/knowledge/keeper-timer-inert.md:40,182`
   list `ai-usage.timer` among `systemctl --user list-timers`; `corpus/knowledge/
   speedrun-pipeline.md:22` degrades to `null`, "never fatal (ai-usage cache,
   `omp usage --json` 30s cache…)", `:80` cannot attribute the 5-min poller to
   `ai-usage.timer`. kake is a **consumer** of the ai-usage cache (web-speedrun
   data source), not an owner; a future change to the producer's cache shape/
   decidability would be visible to kake too.
3. **kumitate — recorded neutrality.** `corpus/lessons/round-11.md:64-68`
   records `ai-usage.timer` (with webzites-probe/charter-scribe) as "owned by
   other identities' lanes" and the fleet rule that lanes do not toggle host
   state — consistent with the producer being operator/external-owned.

## 3. K1/K2 disambiguation

The frozen registration (registration.md:29-98) names this round's claims **C1**
(operability) and **C2** (coverage); there is no K1/K2 claim in it. In mado's
history, "K1/K2" are defect-case labels for the verify.sh include-graph surface
(`.ufo/waves/round-13/w1/AttackSets.md:26-27,45-92`: K1 = hyprlang `#`
conditional source block; K2 = empty `source =` value) — unrelated to the option
table. This scan therefore covers the C1 (`--live`/getoption) and C2
(host-bar-producers assimilation) scopes above.

## 4. Verdict

- getoption/option-table surface: **no sibling overlap** (mado sole owner; all
  sibling boundaries route away or refuse).
- Waybar producers: **no ownership overlap**; two complementary dependencies on
  the ai-usage producer (tsukuroi timer census, kake cache consumption) and one
  neutrality record (kumitate). Attribution of the producers themselves is
  operator/omarchy-owned, outside every lane's province.

## 5. Risks / second-order effects

- tsukuroi's timer-drift verdict depends on `ai-usage.timer` being armed and
  succeeding; mado's live probe does not touch timers, so no interference. But an
  entry claiming the ai-usage producer's current output is undecidable must not
  imply the timer/cache is absent (tsukuroi census and kake pipeline both rely on
  its presence).
- kake's speedrun pipeline consumes the ai-usage cache; the C2 entry's
  "current-output decidability" note should name capture time so the two lanes'
  observations stay comparable.
- No risk on the option-table surface: no sibling reads or writes it.

## 6. Proposed move (bounded)

In mado's C2 entry (assimilation scope), add a scope note delimiting the ai-usage
producer as operator/omarchy-owned (out-of-province) and cross-referencing the two
sibling dependencies — tsukuroi `SKILL.md:47,643` (timer arm/result census) and
kake `speedrun-pipeline.md:22` (cache consumption) — so integration never treats
those observations as contested drift. One doc-scope line; harms no axis (C2
coverage gains an explicit boundary; adjacency is recorded, not absorbed).

## Verification

Run: read-only; no checks needed (no code changed). Citations above are
file:line from the current lane trees; the sibling grep set covered all 21 lanes
with zero additional hits.
