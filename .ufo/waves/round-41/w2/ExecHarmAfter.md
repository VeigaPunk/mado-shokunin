# ExecHarmAfter — w2 harm attack at the data commit

Seat `ExecHarmAfter`, round-41 wave w2 (2026-10-25). Attack: "no axis is harmed" at data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`. Full verbatim captures, comparisons and the derived fractions in `<this dir>/after.md`; this file is the short report.

**Finding 1 — DATA defect (fix before the round lands).** `quality/check-index-rows.py --rev 07f2641 --repo .` exits **1** (was 0 at freeze), `rows=59 errors=1 warns=3`:

```
ERROR row-cells: knowledge/hyprland-focus-grab-r41.md at line 70 carries 2 cells (need 3 non-empty)
```

`corpus/README.md:70` — the new coverage-map row for the C2 entry — carries only the Note and Holds cells; the Sources cell is missing (every other row ends with a third `| S### ... |` cell). This is new damage vs the baseline constraint `errors=0` (same 3 WARNs as the freeze). Because the cell-count check fails, the row's S-id/path checks are skipped for that row.

**Finding 2 — open defect (expected): navigation axis publication is stale.** `quality/check-axis-scores.py --repo . --rev 07f2641` exits **1**, `mismatched=1`:

```
MADO_AXIS_ROW: axis=navigation published=58/58 derived=59/59 verdict=STALE
MADO_AXIS_ROW: axis=calibration published=55/55 derived=55/55 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1 rev=07f2641696b5ac73de1404ea737a9f27e9819aa1
```

Derived counts the gate derives now — **navigation indexed/total = 59/59** (published still 58/58 in `SCORECARD.md:2493`; L1 must publish 59/59), **calibration resolved/active = 55/55**, **operability selftest = 12/12** (both still MATCH; not harmed).

**No other deltas:** `MADO_SELFTEST 460/460`, `MADO_OPTIONS_SELFTEST 211/211`, index `59/59 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` (B rose by exactly the one new note; zeroes intact), bare `check-index-rows.py` exit 2 `SETUP_ERROR` (unchanged), `mado-eventq.py --selftest` exit 2 unrecognized (unchanged gap), census `mado ok` exit 0 with the identical 9-line W-set (byte-identical to the w1 baseline capture).

Tools: none installed (no installs needed). Clone `/tmp/tmp.uMwEMvEpVp/lane` (deleted after capture, see after.md).
