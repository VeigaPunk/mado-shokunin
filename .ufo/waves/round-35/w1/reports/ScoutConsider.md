# ScoutConsider — considerthese/ sweep (round 35, w1)

Scope: read-only scan of `considerthese/`. Files present: `2026-10-19.md` through `2026-10-24.md` (one per day, 6 files).

## Latest file

`considerthese/2026-10-24.md` (dated 2026-10-24, written ~3h before this scan).

Window covered: 2026-10-21 09:52 → 2026-10-24 09:52 BRT; rest of round 27 and rounds 28–31 (commits after `0a9ea77` up to tip `9186234`).

## Proposals carried

The file's final section is titled **"Self-improvement suggestions (proposals only; not acted on)"** — six numbered items:

1. Track a domain-versus-meta ratio per window; flag ≥2 rounds without a desktop-facing change.
2. Report run reliability (dead attempts, OOM kills, provider 429s) as its own line, counted from LOG and watchdog lines.
3. Follow up routed items across reflections — keep a short carried list (n2 relevance cheat, Holds semantics, undispatched waves), check each off by commit.
4. Suggest the next desktop table explicitly — read `PROVINCE.md`, propose the next Hyprland surface (window rules, monitors, layer rules) with grounding sources.
5. Verify one cited fact first-hand per day, read-only (e.g., re-open one of S178–S182 and confirm the quoted line).
6. Note the window's time-of-day pattern — report when rounds ran so the operator can correlate host load / coredumps with lane activity.

## Implementation status

**All six are marked not implemented.** The section header declares them "proposals only; not acted on," and no item carries a landed-at commit. One nuance for proposal 3: the file itself performs the follow-up once (confirms yesterday's flagged M26-10 landed at `b6650d5`), but the proposal — a persistent carried list checked across files — is still unimplemented.

## Surface each unimplemented proposal points at

| # | Surface |
|---|---|
| 1 | `tools/`, `corpus/knowledge/`, `PROVINCE.md` (domain side) vs `quality/`, records, `SCORECARD.md` (meta side); emitted into the `considerthese/` daily files |
| 2 | `LOG.md` attempt/death entries + fleet-side watchdog output (`scripts/shokunin-watchdog.sh`, `.ufo/watchdog.log` at fleet root); reported to operator |
| 3 | Prior routed items: n2 relevance cheat (`quality/` citation counter fixtures), Holds↔note overlap (`SKILL.md`/contract Holds semantics), undispatched wave specs (`.ufo/waves/`); tracked via `considerthese/` files |
| 4 | `PROVINCE.md` (lane scope), `corpus/SOURCES.md` (grounding sources); domain target = Hyprland **window rules, monitors, layer rules** — would land as new `tools/` resolver + `corpus/knowledge/` note, same shape as `tools/mado-wsrules.py` |
| 5 | `corpus/SOURCES.md` source registry — specifically S178–S182 (Hyprland workspace-rule sources); any future day's cited source |
| 6 | `LOG.md`/commit timestamps vs host receipts (coredump counts in oracle lines); operator-facing timing note in `considerthese/` |

## Note for L1

Only proposal 4 is desktop-facing; the other five are lane-meta (reflection format, follow-up bookkeeping, fact re-checks). Context the file also carries: `tools/`/`corpus/knowledge/`/`SKILL.md`/`PROVINCE.md` untouched since round 27; PR #1 (draft README) still open since 2026-10-17; negative fixture n2 (irrelevant-but-resolving citation passes the QUALITY rubric) is a named residual cheat.
