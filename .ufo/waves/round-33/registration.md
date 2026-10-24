# mado round 33 — registration (FROZEN before any corpus append)

Lane: `mado-shokunin`. Round: 33 (attempt 1). Identity: `Kimi fresh L1`.
Round-start tip: `de8fe248579520ee9af0f6a6f2db9d116bd55aeb` (r32 spot-check on `d9ed38166cc3be8ef4c52b41d66ad94010feb047`).
This file does not rewrite round-32 predicates and does not claim the round-32 result.

Axes at the round-start tip, re-read from the last published table: navigation 46/46 = 1.0,
calibration resolved-active 41/41 = 1.0, sourced-art 1.0, operability selftest 12/12 = 1.0.
Saturation line 9.0, stagnation window N=3, retired: none. A capability entered in round 32,
so the stagnation nudge does not waive the lowest-axis obligation. Every scored axis is tied
at 1.0. C2 works that tied lowest set on the calibration surface (a published claim row that
does not match a re-run). C1 works coverage on a surface the lane does not hold.

Two claims. Each is a new predicate. Round 32's C1 counter stays frozen and rejected.

## C1 — coverage: Waybar as an event-socket client, and the compositor's answer to a stall

Surface moved: the lane holds no entry on the Waybar Hyprland module's socket2 subscription
or on the compositor removing a client whose event queue reaches 64. The round-32 IPC entries
stay landed and are not this claim.

Frozen cite-map:
- `corpus/knowledge/waybar-module-text-route-r25.md` requires S190, S191
- `corpus/knowledge/event-delivery-limits-r26.md` requires S197, S189

PRED-C1-r33-v1: TARGET_MET iff closed_entries=2 AND closed_rows=4 AND open_cites=0, where a frozen cite is closed only when the entry file contains a 1-25 word gate-quote line for that id that is a contiguous substring of the fetch blob and that blob's sha256 equals the digest frozen in c1/frozen.json, and the registry row for that id lists the entry path in used-by.

Counting command:

```sh
python3 -I .ufo/waves/round-33/c1/count.py --root . --frozen .ufo/waves/round-33/c1/frozen.json
```

Kill rule: met iff that command prints `verdict=TARGET_MET`. Anything else is an honest stop.
The target is not narrowed after landing. Extra `source:` lines do not change the count.

Pre-data controls, scored on 2026-10-24 before any corpus append (receipts under
`.ufo/waves/round-33/controls/`):

- do-nothing (lane tree, fetches present, no entries): `closed_entries=0 closed_rows=0 open_cites=4 verdict=TARGET_MISSED` exit 1
- junk stubs + stub rows + fake blobs: `TARGET_MISSED` exit 1
- rows-only: `TARGET_MISSED` exit 1
- entries-only (real quote text, no rows, no fetch): `TARGET_MISSED` exit 1
- hash-mismatch (one flipped fetch byte): `closed_entries=1 open_cites=1 verdict=TARGET_MISSED` exit 1
- golden scratch (real fetches, real quotes, four rows): `closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET` exit 0
- extra `source:` line on the golden tree: still `TARGET_MET` exit 0

Skip-the-work controls do not meet the target. The golden tree is the claimed work, not a control that skips it.

## C2 — calibration: the published r32-C1 verdict must match a re-run

Surface moved: SCORECARD's round-32 C1 row says the target was met at `cited_entries=3`.
The frozen round-32 counter, re-run by this gate on `d9ed38166cc3be8ef4c52b41d66ad94010feb047`,
prints `cited_entries=7`. This claim does not edit that row and does not edit the round-32 counter.

PRED-C2-r33-v1: TARGET_MET iff the last line matching r33-claim-verdict: r32-C1 cited_entries=<N> verdict=<V> rev=<H> has N equal to the frozen r32 counter's cited_entries on rev H, V equal to honest-stop, and H equal to d9ed38166cc3be8ef4c52b41d66ad94010feb047.

Counting command:

```sh
python3 -I .ufo/waves/round-33/c2/count.py --repo . --scorecard SCORECARD.md
```

Kill rule: met iff that command prints `verdict=TARGET_MET`. A missing line, a wrong N, or
any verdict word other than `honest-stop` is an honest stop.

Pre-data controls:

- do-nothing (current SCORECARD, no verdict line): `claim_mismatch=1 reason=absent verdict=TARGET_MISSED` exit 1
- junk line `cited_entries=3 verdict=target-met`: `published=3 measured=7 verdict=TARGET_MISSED` exit 1
- honest line `cited_entries=7 verdict=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047`: `published=7 measured=7 verdict=TARGET_MET` exit 0

The measured 7 is the frozen round-32 counter on the frozen rev. It is not a new claim that round 32 met its target.
