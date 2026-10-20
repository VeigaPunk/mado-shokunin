# mado — round 19 (hyaku phase 2, attempt ⟨attempt⟩)

Lane `mado-shokunin`, branch `master`. Baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`
(round-18 closure). Pre-registration `17661e0⟨full hash⟩` (`SCORECARD.md` "Round 19 — declared
claims"). Lane tip ⟨lane tip hash⟩ (landed via `scripts/hyaku/jj-lane.sh`; `state` output
⟨state line⟩).

## Work performed

Declared claims (pre-registered at `17661e0`, `SCORECARD.md` "Round 19 — declared claims"):
**C1 calibration** (lowest axis, literal lesson-citation fraction, `python3 .ufo/waves/round-17/measure.py REV`, key c1),
**C2 freshness, sourced** (walker version-pin currency, `python3 -I .ufo/waves/round-19/fresh-pins.py REV`),
**C3 operability: tripwire recall** (`python3 -I .ufo/waves/round-19/tw-recall.py REV`, frozen real-incident lines).
No exploratory claim.

- Outside spot-check R18-V1 (S094 anchor cites per-fetch GitHub HTML digests): ⟨disposition and evidence pointer⟩.
- Outside spot-check R18-V2 (QUALITY criterion 26 red-before rests on a headerless receipt): ⟨disposition and evidence pointer⟩.
- Outside spot-check R18-V3 (eleven owned files keep the walker 2.17.0 pin, host at 2.17.2 per `/var/log/pacman.log:2929`): ⟨disposition and evidence pointer⟩.
- Outside spot-check R18-V4 (S084 cites the unpinned docs.rs `latest` alias): ⟨disposition and evidence pointer⟩.
- Carried frozen F1/F2: ⟨disposition and evidence pointer⟩.
- Carried `measure-mutants.py` default `--out`: ⟨disposition and evidence pointer⟩.
- Carried jj audit F6 / F9 / F16 / F17 (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md`): ⟨fixed or not-fixed, with reason and pointer per item⟩.
- Carried tripwire drafts `TwMissBashCVar.patch`, `TwMissHelperFn.patch`, `TwInstallerChannels.patch` (fixtures `.ufo/waves/round-18/drafts/tripwire/r18-*`): ⟨applied or rejected, with reason, rebased sha256 ⟨…⟩ and suite result⟩.
- C1 work item (lesson-cited QUALITY criteria 27+, each with a runnable check red on a real `9c54c56` artifact): ⟨criteria added, red-before receipt path⟩.
- C2 work item (13 owned files holding `2.17.0` gain a `2.17.2` line plus an `S###` row token; gate `live.walker.version` pin and selftest move): ⟨files changed, pin move evidence⟩.
- C3 work item (tripwire drafts applied or rejected; round-19 frozen baseline re-pinned at the landed classifier): ⟨evidence pointer⟩.
- Frontier step (S094 superseding row S097, S084 re-point to S098, PROVINCE path-root line for `~/.config/omarchy/**`): ⟨evidence pointer⟩.
- Mistakes routed to `lessons/round-19.md` `## Mistakes`: ⟨rows M⟨n⟩–M⟨n⟩⟩.

## Landed changes

LOG entry `## ⟨date⟩ — round 19: ⟨LOG heading⟩`.

| commit | content |
|---|---|
| ⟨hash⟩ | ⟨pre-registration / start census⟩ |
| ⟨hash⟩ | ⟨wave-1 integration⟩ |
| ⟨hash⟩ | ⟨receipts at ⟨hash⟩: measure before/after, harm watch⟩ |
| ⟨hash⟩ | ⟨wave-2 integration⟩ |
| ⟨hash⟩ | ⟨final receipts bound to tip⟩ |

Inherited state: ⟨`lane-dead-no-report mado round=19` line present or absent; attempt number⟩.
⟨Interrupted or resumed sessions, and how their uncommitted work was kept or discarded.⟩

## Before → after measurements

Each row: claim, counting command, commit measured against. Declared pre-registration values are
shown only as the declared baseline; the before and after cells are measured values.

| claim | command | before @ `9c54c56` (declared) | after @ ⟨hash⟩ |
|---|---|---|---|
| C1 calibration | `python3 .ufo/waves/round-17/measure.py REV` (c1) | ⟨measured⟩ (declared 18/26 = 6.9231) | ⟨measured⟩ (target ≥ 21/29) |
| C2 freshness | `python3 -I .ufo/waves/round-19/fresh-pins.py REV` | ⟨measured⟩ (declared 2/13 = 1.5385) | ⟨measured⟩ (target 13/13) |
| C3 operability | `python3 -I .ufo/waves/round-19/tw-recall.py REV` | ⟨measured⟩ (declared 3/6 = 5.0000) | ⟨measured⟩ (target 6/6) |

Harm watch at ⟨hash⟩: ⟨`HARM_WATCH: PASS|FAIL` with receipt pointer⟩. Gate selftest ⟨N/N⟩,
regression ⟨N/N⟩, classifier ⟨N/N⟩, tripwire suites ⟨N/N⟩, frozen r18 suite ⟨N/N⟩, U ⟨N/N⟩,
rubric V ⟨N/N⟩, navigation ⟨N/N⟩, census exit ⟨code⟩.

Tool shas, labelled: tripwire `⟨sha256 prefix⟩…` (`9c54c56`), `⟨…⟩` (`⟨hash⟩`, final).
Gate `⟨…⟩` → `⟨…⟩`. Receipts: `.ufo/waves/round-19/evidence/*`.

## Sources & frontier

Census command: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.
- Start (`⟨evidence path⟩`): exit ⟨code⟩, with ⟨historical W04 rows, if any⟩.
- End (`⟨evidence path⟩`): exit ⟨code⟩.

Rows changed ⟨old⟩ → ⟨new⟩. Rows added by tier: ⟨tier histogram⟩.
Rows touched old→new: ⟨S### `old` → `new`⟩.
Reserved ids: S096 host walker bytes ⟨status⟩; S097 superseding row for S094 (no HTML digests) ⟨status⟩;
S098 xdg crate tarball row replacing S084 as support ⟨status⟩; S099–S105 L1-assigned ⟨status⟩.
Frontier rows advanced: ⟨list⟩.

## Trend verdicts

- **expansion: ⟨improved|harmed|unchanged|unprovable-but-better⟩.** ⟨evidence pointer⟩.
- **quality: ⟨improved|harmed|unchanged|unprovable-but-better⟩.** ⟨evidence pointer⟩.
- **discernment: ⟨improved|harmed|unchanged|unprovable-but-better⟩.** ⟨evidence pointer; outside non-author verification status⟩.

## SHONEN

One line per box of `SHONEN.md`. `[x]` only with a named non-author verifier; `[~]` with a resolvable
evidence pointer; `[ ]` if untouched.

- ⟨[x]|[~]|[ ]⟩ SKILL.md contains real decision tables, error patterns, checklists, cited sources — ⟨evidence pointer or verifier name⟩.
- ⟨[x]|[~]|[ ]⟩ At least one end-to-end domain task executed and logged in LOG.md — ⟨evidence pointer or verifier name⟩.
- ⟨[x]|[~]|[ ]⟩ Instructions executable by an agent without oral context — ⟨evidence pointer or verifier name⟩.
- ⟨[x]|[~]|[ ]⟩ No cross-domain bleed (PROVINCE.md still accurate) — ⟨evidence pointer or verifier name⟩.

## Other required lines

- **Stale-lane:** ⟨stale-lane statement; any open mission of this lane⟩.
- **Installs:** ⟨tool, version, channel, reason per install or update; or `none`⟩.
- **Open L0 questions:** ⟨question lines appended to `.ufo/l0-questions.md`, or `none filed`⟩.
- **Host:** the host pause holds (no package query or transaction, service, compositor, input or
  screenshot operation; host files read as bytes only). ⟨any observed host mutation, with
  `/var/log/pacman.log` line pointer and actor status⟩. R15-V1 stays operator-owned.
- **Fence slips and misroot sweep:** ⟨seat fence slips disclosed; fleet `git status --porcelain` result; files moved out of the fleet root⟩.

## Waves, seats, routing

| wave | seats | role mix | dead seats |
|---|---|---|---|
| Wave 1 (`.ufo/waves/round-19/w1/{spec,dispatch,record}.json`) | ⟨n⟩ | ⟨role counts⟩ | ⟨n and names, or 0⟩ |
| Wave 2 (⟨name⟩) | ⟨n⟩ | ⟨role counts⟩ | ⟨n and names, or 0⟩ |
| Residual (⟨name⟩) | ⟨n⟩ | ⟨role counts⟩ | ⟨n and names, or 0⟩ |

- **Round total:** ⟨n⟩ seats (cap ≤200 per round; validator cap 100 per wave).
- **Planner seat:** held by L1 (the canonical §3 planner seat). The validator rejects `planner`, a
  frozen-topology seat and never a swarm role. The bounded planning data-walk rode
  ⟨scout/connector/revenger item names⟩.
- **Routing** (by role, no model parameter): ⟨route mapping observed, or the lane-addendum routing
  table; note any seats that kept their original routes⟩.
- **Seats that ended without a report:** ⟨names and cause, or none⟩. None was respawned unless
  stated here: ⟨…⟩.

## Acceptance placeholders (not claims)

Admission is not asserted. Non-author closure is required: ⟨verifier name or `pending`⟩.
