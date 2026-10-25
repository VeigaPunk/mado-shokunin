# CritConsider — which unimplemented considerthese proposal can be grounded through the lane's own bar

Seat: CritConsider (round 35, wave 1). Read-only over lane bytes and host read
verbs; this report is the only write. Relies on `considerthese/2026-10-24.md`
(the latest file, dated 2026-10-24) plus the five earlier daily files, and
re-checks each unimplemented proposal against the lane's own admission
machinery: frozen predicate before data, an independent oracle (round 25's
M25-1 rule — a self-model counter does not verify), discharged kill-rule
controls, PROVINCE read-only bounds, and the open L0 register.

Inventory source: `ScoutConsider.md` (this wave) agrees with my own read —
all six proposals in `2026-10-24.md:46-51` are unimplemented; proposals 1, 2,
3, 5, 6 are reflection-side habits, proposal 4 is the only desktop-facing one.
The five earlier files carry older proposals already dispositioned
(`.ufo/waves/round-18/w1/reports/ConnConsiderThese.md` §2–3) or superseded;
their still-open items are listed in the "cannot" table where they bind.

## The lane's own bar, restated as tests

A proposal is groundable this round only if it can be turned into a claim that
passes, today:

- **Oracle test (QUALITY 36, M25-1):** an expected table from an independent
  oracle — live `hyprctl` read verbs or the nested-Hyprland harness
  (`.ufo/waves/round-26/harness/oracle.py`, reused in round 27) — never the
  lane's own model.
- **Kill-rule test (M28-1, round-30 criterion):** a counter frozen before data
  whose controls demonstrably fail; the counter must run once at freeze.
- **Bounds test (PROVINCE.md):** config trees and `hyprctl` read verbs only;
  no mutation, no transaction (QUALITY criterion at `corpus/QUALITY.md:99`,
  host pause still held), secrets shape-only.
- **Authority test:** no operator-gated step (João's OK, merge approval, L0
  overrule, cross-lane seat) may be a dependency.
- **Axis test (AXES/registration rule):** the claim must sit on a lowest
  non-retired axis. Axis table at round-34 tip (`SCORECARD.md:2110`):
  navigation 47/47, calibration 41/41, operability 12/12 — all 1.0.

## Verdict

**Groundable: `considerthese/2026-10-24.md` proposal 4 ("suggest the next
desktop table explicitly") — in its `monitor=` / input-device forms.** This is
the only unimplemented proposal that can reach a full frozen-predicate claim
under the lane's own bar this round, and it also repairs the debt the same
file names ("no `tools/` or `corpus/knowledge/` change since round 27").

**Not groundable: the window-rule and layer-rule forms of proposal 4; the
tripwire repair; every operator-gated proposal; every mutation surface.** See
argument below.

## Groundable — proposal 4, monitors first

What the host offers, verified first-hand 2026-10-24 (this seat ran each
verb once, read-only):

```
hyprctl version       → Hyprland 0.56.2, tag v0.56.2, efb509937…
hyprctl monitors -j   → [DP-1 3440x1440@99.997 at 0x0 scale 1]
hyprctl windowrules   → unknown request          (decisive, see below)
hyprctl layers        → Monitor DP-1 …            (runtime surfaces only)
```

- **Oracle exists and is already whitelisted.** `monitors` is in the PROVINCE
  `mado-verify.sh` read-verb row (`PROVINCE.md:28`) and the corpus read-verb
  ledger (`corpus/knowledge/hyprctl-verification-layer.md:12-14`). Live truth
  today: one DP-1. A static resolver of the `monitor =` declarations
  (`~/.config/hypr/monitors.conf:10` declares `3440x1440@100`, re-read this
  seat) against `hyprctl monitors -j` in the nested oracle is the exact
  shape that was admitted three times running: binds 0/41→41/41 (r25),
  animations 51/51 (r26), workspace rules 41/41 (r27). The harness is
  committed at `.ufo/waves/round-27/harness/oracle.py`; HOST_SAFETY delta=0
  discipline is established (66 receipts, round 26).
- **Sources exist.** The resolver inherits the same `source =` graph and
  hyprlang machinery as `tools/mado-wsrules.py`; monitor-line parsing is in
  the same `ConfigManager` family already mined at S153–S182 (workspace-rule
  and windowrule handlers share that file). New mined rows are the only
  corpus addition required — the known cost.
- **Adequate second choice: `hyprctl devices -j`.** Also a proven read verb
  (8 keyboard nodes, `active_keymap` Portuguese (Brazil) at
  `hyprctl-verification-layer.md:159`); `input.conf` (54 lines, includes two
  `windowrule` scroll lines) resolves statically. Weaker because the
  devices table is hardware-dependent — inside the nested headless oracle
  the device set may be empty, so a first round would measure against the
  live table only; monitor= has the cleaner held-out story.
- **Why not a QUALITY/calibration claim instead.** Proposals 1, 2, 3, 5, 6
  are reflection-side bookkeeping (domain-vs-meta ratio, run-reliability
  line, carried-list follow-up, first-hand fact check, time-of-day note).
  `considerthese` files are operator-identity reflections, not lesson
  artifacts — `ConnConsiderThese.md:36-38` already ruled that a QUALITY row
  citing `considerthese/` is a false grounding — so none of them can carry
  a claim; they are cheap habits the reflection can adopt unilaterally,
  not round work. Proposal 5 deserves one line of honesty: it is
  groundable as practice (this report re-checked `hyprctl` facts
  first-hand) but it is not a claim and cannot score an axis.

## Not groundable this round

| Proposal (file:line) | Why it fails the lane's own bar |
|---|---|
| Window rules inside `2026-10-24.md:49` (proposal 4's own alternative) | **No table oracle.** `hyprctl windowrules` → `unknown request` on 0.56.2 (this seat). The only live surface is per-window `getprop` effects, and `corpus/knowledge/window-rule-effects-getprop.md` already classes it "effect-read, not match-read — the matching-rule identity remains `[UNK]`". A resolver whose expected value cannot be read from the compositor cannot satisfy M25-1/QUALITY 36. Parsing coverage already exists (`keybind-rule-semantics.md` §4, `rule-attribution-r24.md`, S153–S162). Would need a nested oracle plus spawned clients plus an attribution channel that does not exist in 0.56.2 — a different, larger claim, not a table resolver. |
| Layer rules inside `2026-10-24.md:49` | `hyprctl layers -j` reports live layer surfaces (waybar, wallpaper, notifications), not the `layerrule =` config table — same missing-oracle class as window rules. |
| Live-plane refresh / observed-behaviour rubric (`2026-10-19.md:37`, `2026-10-20.md:54`, `2026-10-21.md:56`) | Read-only probes are in-bounds and run daily in r35 w1 — the artifact is producible. But the proposal asks for a *rubric for observed behaviour*; no frozen denominator exists, and "observed behaviour" of the compositor's rule effects is exactly the oracle-free surface above. Documentary-vs-observed honesty (the lane's own `[UNK]` sections) is what keeps the ceiling a ceiling. Operator-cleared mutations remain barred (QUALITY host-pause criterion). |
| Tripwire classifier repair (`2026-10-22.md:43-44`, `2026-10-23.md:41`) | Two hard dependencies the lane cannot discharge: L0 `l0-questions.md:103` (H2 166/175 ruling) is still open, and the routed precondition — freeze the five wave-2 attack fixtures as a registered population *before* any further tripwire change (`2026-10-22.md:22`) — is unmet. Five straight non-admissions were the cost of ignoring exactly this. |
| Machine-readable per-round digest (`2026-10-20.md:56`) | The file itself marks it "a repo change, so it's João's call". A scratch prototype is lane-legal but grounds no axis claim; landing it is operator-gated. |
| "What your config resolves to" note for João (`2026-10-23.md:52`) | The computation exists (r26 ran both resolvers on the operator tree against live `hyprctl` and agreed); delivering it is "with his OK" — the gating is the deliverable, so it cannot be grounded by the lane alone. |
| Undispatched wave specs (`2026-10-24.md:38`) | Not a proposal, but the carried debt behind proposal 3: seats have no swarm-dispatch tool (L0 `l0-questions.md:139` asks whether a Kimi L1 even may); specs 33/33/15-seat were never dispatched and the lane cannot fix the missing tool. |
| Outside-lane spot-check sampling (`2026-10-19.md:38`) | Requires a sibling lane's seat — cross-lane authority the lane does not hold. (Already exceeded by protocol-shokunin/hyaku closures anyway.) |

## Files and dates relied on

- `considerthese/2026-10-24.md` (dated 2026-10-24): the six unimplemented
  proposals at `:46-51`; domain-drift debt at `:37`; undispatched waves at `:38`.
- `considerthese/2026-10-22.md` (2026-10-22): routed defect 6 — freeze the
  wave-2 attack population before further tripwire work (`:22`); H2 debt (`:44`).
- `considerthese/2026-10-23.md` (2026-10-23): proposals at `:47-52`, including
  the operator-OK note (`:52`).
- `considerthese/2026-10-19.md` / `2026-10-20.md` / `2026-10-21.md`: older
  proposals; dispositions partially recorded in
  `.ufo/waves/round-18/w1/reports/ConnConsiderThese.md` §2–3.
- `.ufo/waves/round-35/registration.md` (2026-10-24): this round's frozen
  claims are idle-lock coverage + clause-ledger calibration — the proposal
  mine feeds the *next* claim slot, not C1/C2.
- `PROVINCE.md` (read-only config trees; `mado-verify.sh` read-verb row `:28`).
- `corpus/QUALITY.md:99` (host-pause criterion — transactions stay barred).
- `corpus/knowledge/window-rule-effects-getprop.md` (match-identity `[UNK]`;
  `workspacerules` listed separately from `getprop`).
- `corpus/knowledge/hyprctl-verification-layer.md:12-14,153-159` (monitors and
  devices as established read surfaces; DP-1 declared-vs-live precedent).
- Fleet `.ufo/l0-questions.md:103,133-135,139` (mado-open rulings that gate
  tripwire work and wave dispatch).
- `.ufo/waves/round-27/harness/oracle.py` (committed nested-Hyprland oracle).
- First-hand host facts (this seat, 2026-10-24): `hyprctl version` → 0.56.2
  `efb509937…`; `hyprctl monitors -j` → DP-1 3440x1440@99.997;
  `hyprctl windowrules` → `unknown request`; `~/.config/hypr/monitors.conf:10`
  declares `3440x1440@100`.
