# R54W2Seat05 — C1 duplicate-P19 row order

## Finding — High: prior prototype admits forged duplicate before good row

The frozen C1 contract requires **each** corrected proposition P19–P22 to verify at the scored revision (claims-frozen.md:19–30). P19 is tied to `ConfigActions.cpp:1554-1558` (claims-frozen.md:25–26); the frozen proposition table specifies that pin, anchor, and quote (registration.md, C1 fixture inventory / proposition table). The actual pinned span has the modifier call at line 1554, the pressed-state condition at 1556, the non-mouse branch at 1557, and the key call at 1558 (round-52 `Hyprland-ConfigActions.cpp`:1554–1558). Thus a duplicate P19 row cannot stand in for another required proposition, nor should a forged duplicate become harmless merely because a valid row occurs later.

Relevant prior measurement: w1 `R54Seat02.md`:266–277 records its isolated prototype's `parse_entry` keyed by ID and keeping the last row. It reports:

```
good P19 row first, forged P19 row second -> prop=3 quote=4 anch=3 pin=4   (caught)
forged P19 row first, good P19 row second -> prop=4 quote=4 anch=4 pin=4   (ADMITTED)
```

The second ordering is a row-order false-green: the good row overwrites the forged one, allowing the entry's duplicate-row ambiguity to pass. W1 therefore recommends requiring exactly one row per frozen ID (and rejecting duplicates). This is evidence from the w1 report, not a fresh execution by this seat.

## W2 check and limit

The frozen pinned command names `quality/counters/c1-r54-errata-truth.py` (claims-frozen.md:19–21), but that file is absent in the lane at this check. Accordingly the duplicate-before/after-good-row mutation was **NOT RUN** against a current counter; no final scored implementation behavior can be confirmed here. No predicate or registration was changed. The prior prototype's reported false-green remains an actionable risk until an available counter rejects both row orders.

Exact absence check:

```
$ if test -e /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py; then printf 'counter-present\n'; else printf 'counter-absent\n'; fi; rc=$?; printf 'EXIT=%d\n' "$rc"
counter-absent
EXIT=0
```

Axes: operability (duplicate rows must not falsify the P19–P22 record); harm watch (no source, registration, or predicate edits).

## Trailer

- Finding attacked: item 5, duplicate P19 before and after a good row; w1 prototype reported the forged-before-good ordering as admitted.
- Evidence: frozen contract `claims-frozen.md:19–30`; P19 anchor `claims-frozen.md:25–26`; exact pin span `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp:1554–1558`; relevant prior measurement `.ufo/waves/round-54/w1/R54Seat02.md:266–277`.
- Exact command/output/exit: absence check above; `counter-absent`, exit 0. Counter invocation and row-order fixture: NOT RUN/absent.
- Files changed by this seat: `.ufo/waves/round-54/w2/R54W2Seat05.md` only. No other source or lane files changed.
- Scratch: `/fast/scratch/hyaku/mado-r54/R54W2Seat05`; cleaned before yield.
