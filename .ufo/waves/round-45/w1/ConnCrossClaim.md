# ConnCrossClaim — scoped findings (round 45, w1)

Full report: `w1/ConnCrossClaim/report.md`. Evidence: `w1/ConnCrossClaim/{trees.txt,
c1-A.out, c2-A.out, c1-B.out, c2-B.out, c1-D.out, c2-D.out, c1-E.out, c2-E.out}`.

## Separability: confirmed both ways (registration.md:57-60)

| Tree | contents | C1 counter | C2 counter |
|---|---|---|---|
| A (0163904a) | freeze + tool only | **MET** 49/49 rc=0 | MISSED 0/1 rc=1 |
| B (7dc09f54) | freeze + build-pos data only | MISSED 0/49 rc=1 | **MET** 1/1 rc=0 |

Counters read disjoint paths: C1 reads only `tools/mado-monitors.py` + scratch
(c1-r45-monitors.py:325-368); C2 reads entry/registry/lesson/README/fetch only
(c2-r45-monitor-entry.py:411-632). No cross-artifact dependence.

## Shared assumptions (same pin line -> both claims)

60 Hz default (Hyprland-MonitorRule.hpp:46); 1 Hz bound (Monitor.cpp:837); 1/120
step + 89-step search (Monitor.cpp:1001,1010); eight-key grammar/unknown-key drop
(legacy ConfigManager.cpp:1293-1387); erase-on-add/newest-match (MonitorRuleManager.cpp:38,96);
selector name/`desc:` (Monitor.cpp:1201-1206); JSON fields/`all`/5 decimals
(HyprCtl.cpp:242,320); explicit position (MonitorPositionController.cpp:27);
number test (hyprutils String.cpp:50,59); `sdr_eotf` divergence (wiki-Monitors.md:253).
C1 encodes these executably (docstring + fixtures K03-K15), C2 as sourced census +
surfaces; values 60/1/120/89/8/5 appear in both.

## One wrong pin

- Repo-level pin deviation: tampering one byte of fetch/Hyprland-MonitorRule.hpp
  flips C2 MET->MISSED (clause d sha256 for S305, plus e/g/h/i/j; default-60
  anchor gone) while C1 stays MET (tree E) — C2 is the only pin-integrity guard.
- Wrong-against-reality pin: neither counter can detect it (PINS is the frozen
  trust root). It would silently corrupt both claims together — C1 mis-models real
  Hyprland while passing its 49 self-contained fixtures, C2 documents the wrong
  behavior while passing a-j. Only pin-independent evidence is the live host
  receipt (AGREE/OK), which exercises just one output (@100, scale 1, transform 0,
  mirror none) and cannot catch a wrong 60 Hz default / tolerance / correction
  factor / key grammar.

## Handoff

No lane content edited outside this seat dir; no tools installed; scratch cleaned
after copy. Main agent may re-run counters from the receipts (trees under
/fast/scratch/hyaku/mado-r45/ConnCrossClaim, deleted before finish).
