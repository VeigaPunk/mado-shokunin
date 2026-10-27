# R54W2Seat12 — C1 uncited pin integrity falsification

## Axes
- **Claim integrity:** whether each frozen real input is actually covered by the counter's success predicate.
- **Adversarial resistance:** whether an in-scope pin mutation can leave all reported pin checks at 4/4.

## Counterexample and evidence
**Counterexample:** mutate only an uncited frozen pin, `Hyprland-ConfigActions.hpp`, leaving all pin files named by P19–P22, the errata entry, and the checksum manifest unchanged. If the stated pin count is citation-derived, all four cited pins still pass and the frozen `pins=4/4` can remain green despite one of the four enumerated pins being corrupted. Thus `pins=4/4` does not establish integrity of *all* frozen pins unless the counter also checks each frozen inventory pin against its recorded digest, including the header that no proposition cites.

Evidence: the frozen C1 predicate says “each of the four pins' bytes hash to the round-52 recorded sha256” (claims-frozen.md:28-30). Registration lists four pins and hashes: `Hyprland-ConfigActions.cpp` `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637` (registration.md:16), `Hyprland-ConfigActions.hpp` `746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073` (line 17), `Hyprland-KeybindManager.cpp` `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40` (line 18), and `Hyprland-legacy-DispatcherTranslator.cpp` `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771` (line 19). The four proposition rows cite only ConfigActions.cpp (P19/P20) and legacy-DispatcherTranslator.cpp (P21/P22), registration.md:25-30. KeybindManager.cpp is only mentioned as the swapped-to negative-control target (line 47); the header is not cited in the proposition table or controls. Therefore an implementation checking only proposition-referenced pins could count 4/4 while missing header integrity.

This is a **conditional vulnerability of a natural implementation**, not a demonstrated counter failure: the round-54 counter is absent in the inspected lane tree (quality/counters listing contains no `c1-r54-errata-truth.py`; frozen claims.md:32 itself records its absence at base), so no implementation could be probed. I did not alter any pin or run a synthetic counter experiment. Frozen C1 control C1-CTL-3 tampers with one recorded SHA256 (registration.md:44), but the cited-control design does not explicitly assert a test that mutates an uncited pin's bytes while preserving its manifest.

## Impact and smallest safe correction
Impacts **claim integrity** and **adversarial resistance**: the predicate language covers all four pins, but a citation-scoped implementation/control suite could under-test it. Smallest correction is implementation/test-side only: hash all four filenames in the frozen pin inventory against their independently frozen expected digest on every run; add a control that corrupts `Hyprland-ConfigActions.hpp` bytes while leaving SHA256SUMS unchanged and requires `pins≤3/4` / `TARGET_MISSED`. Do not alter frozen predicates or registration.

## Existing command availability
Frozen command: `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` (claims-frozen.md:20). **NOT RUN / absent:** `quality/counters/c1-r54-errata-truth.py` is absent in the inspected counter directory; wave-1 registration says implementer owns it and wave 1 is build work, not a landed counter. No substitute command or output invented. No fixtures needed for this source-level counterexample.

## Commands and outputs
- `read skill://godspeed` — returned Godspeed instructions.
- `read /home/vgpnk/.omp/agent/RULES.md` — returned install policy; no installs/updates performed.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/claims-frozen.md:13-44` — returned C1 predicate, pin scope, kill rule and base absence statement.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/registration.md:8-53` — returned four digest entries, proposition pin spans, and controls.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/SHA256SUMS` — returned manifest with all four pins and hashes (also README hash).
- `glob /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters` — listed counters; no round-54 C1 counter present.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/w1/R54Seat12.md` — prior report is C2 frontier reconnaissance, not C1 evidence.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/w1-results.json:55-78` — item 12's W1 output is C2 reconnaissance; no C1 counter finding there.
- `mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat12` — exit 0; created mandated scratch directory.
- `df -h /fast/scratch/hyaku/mado-r54/R54W2Seat12` — exit 0; 804G total, 224G used, 580G available; no ENOSPC.
- `find /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/w2 -maxdepth 1 -type f -printf '%f\\n'` — exit 0; listed only `swarm-registry.json` before this report.

## Report trailer
Lane-relative report: `.ufo/waves/round-54/w2/R54W2Seat12.md`. Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat12` was removed before yield. No fixture/git/jj mutation, producer execution, host/config/service/compositor mutation, package query, tool install, or source/predicate/registration edit.