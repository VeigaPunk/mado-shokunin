# RevChronology — round 25, attempt 3 chronology audit (read-only)

Seat: `MadoR25A3.RevChronology` (reviewer, wave a3w2). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `fa466833`. All times converted to UTC (committer timestamps were `-03:00`).

## Commands run

- `git -C …/mado-shokunin log --format='%H %cI %s' 41cc04c8..master`
- `git -C …/mado-shokunin log --format='%H %cI %s' -- .ufo/waves/round-25/c1/`
- `git show --stat 1ed41fa8` ; `git status --porcelain -- .ufo/waves/round-25/c1/` ; `sha256sum .ufo/waves/round-25/c1/count*.py`
- `git log -- .ufo/waves/round-25/a3w1/reports/swarm-registry.json` ; `git status --porcelain -- .ufo/waves/round-25/a3w2/` ; `git log -- .ufo/waves/round-25/a3w2/`
- `find .ufo/waves/round-25 -name 'swarm-registry.json' -o -name '*registry*'` (only two registries exist: a3w1, a3w2)
- Read: both `swarm-registry.json` files (member entries carry no per-seat timestamps; wave `createdAt` is the earliest witness), `registration.md` §"Attempt 3" (lines 169–235).

## Timeline (UTC)

| When (UTC) | Commit / event | Content |
|---|---|---|
| 2026-10-23 01:58:29 | `04051723` | attempt 1 — registration, frozen C1 counter (v1) |
| 2026-10-23 02:23:06 | `7228299d` | attempt 1 — v1 control receipts + C1 counter v2 (pre-data amendment) |
| 2026-10-23 02:37:00 | `a258c6ae` | attempt 2 — C1 counter v3 (HARD cases, model check) |
| 2026-10-23 06:50:06 | `1ed41fa8` | attempt 3 — **counter v4 + registration** (c1/count.py, c1/count-v3.py, registration.md §Attempt 3, evidence) |
| 2026-10-23 06:52:29.830 | a3w1 `createdAt` | v4-scoring wave registry created (+143.8 s after `1ed41fa8`) |
| 2026-10-23 06:55:21 | `2896dc4a` | routed repairs R1–R6 + wave a3w1 spec (no `c1/` change) |
| 2026-10-23 07:29:16 | `459dd17f` | **pre-data control receipts** under v4 (controls/v4/*.md) + a3w1 reports (incl. tracked a3w1 registry) |
| 2026-10-23 07:31:13 | `fa466833` | SOURCES S169–S172 + wave a3w2 spec (HEAD) |
| 2026-10-23 07:31:20.779 | a3w2 `createdAt` | data-wave registry created (+124.8 s after `459dd17f`); still untracked (`?? .ufo/waves/round-25/a3w2/`) |

## Findings

1. **Counter v4 + registration before any v4-scoring seat — OK.** `1ed41fa8` (06:50:06Z) is the commit that both rewrote `c1/count.py` to v4 (with `count-v3.py` pinned) and added registration.md §Attempt 3. The first attempt-3 scoring wave, a3w1, has `createdAt` 06:52:29.830Z — after the counter commit. Only two registries exist under `.ufo/waves/round-25/`; no earlier attempt-3 registry.
2. **Control receipts before the data wave — OK.** `459dd17f` (07:29:16Z, "pre-data control receipts under counter v4 (10 shapes, none met)") precedes a3w2 `createdAt` 07:31:20.779Z, and also precedes the a3w2 spec commit `fa466833` (07:31:13Z).
3. **No counter/predicate byte change after `1ed41fa8` — OK.** `git log -- .ufo/waves/round-25/c1/` lists `1ed41fa8` as newest; the only later commits (`2896dc4a`, `459dd17f`, `fa466833`) never touch `c1/`. `git status --porcelain` on `c1/` is empty (no uncommitted edits). On-disk `count.py` sha256 = `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`, matching the registration's pinned v4 hash; `count-v3.py` sha256 = `8532d3e9…8375`, matching the pinned generator hash.
4. **Attempt 1 and 2 commits in range — listed above.** `04051723`, `7228299d` (attempt 1), `a258c6ae` (attempt 2). Each has committer time strictly before `1ed41fa8`; the `c1/`-filtered log independently confirms no `count.py` change after `1ed41fa8`.

## Notes (non-violations)

- registration.md line 169 records orchestrator `MadoR25A3` "dispatched 06:40Z" — 10 min before `1ed41fa8`. The orchestrator is not a scoring seat; the audited invariant is counter-before-scoring-seat, and the first scoring wave's registry (06:52:29Z) postdates the counter (06:50:06Z).
- a3w1's `createdAt` (06:52:29Z) precedes its spec commit `2896dc4a` (06:55:21Z); the registry file itself was committed later at `459dd17f`. Both events remain after `1ed41fa8`, so the audited order holds.
- a3w2's registry is untracked, as expected for a live wave.
- No tools installed or upgraded (audit needed only git/coreutils already present).

CHRONOLOGY: ordered
