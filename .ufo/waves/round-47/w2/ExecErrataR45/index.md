# ExecErrataR45 — seat index (round-47 w2, R4b)

Full findings: `.ufo/waves/round-47/w2/ExecErrataR45.md` (the Report). This file is the seat-dir index.

## Verdicts (6/6 subjects confirmed, 0 refuted)

| # | unit | verdict |
|---|---|---|
| E1 | `entry:84` mis-located monitor-added veto | CONFIRMED — `Hyprland-Monitor.cpp:275-287` + `:389` (with `:302`) is exact |
| E2 | `entry:96` wrong provenance | CONFIRMED — `live-monitors-host-r45.txt` is the landed tool's run, committed at the freeze |
| E3 | `entry:98` "not proof of which branch ran" | CONFIRMED — branch closed: all three `DELTALESSTHAN` negations false, push at `:838` cannot run |
| E4 | `entry:18` a9902ea pin | CONFIRMED, one sub-claim WRONG in the prose: `CONFIG_LEGACY` enumerator is removed from `ConfigManager.hpp`, only its `case` from the `.cpp`; the appended block's wording is already right |
| E5 | `entry:106` non-DRM descriptions | CONFIRMED, stronger — whole v0.15.1 tag has 3 `description` occurrences, one assignment (`DRM.cpp:2101`) |
| E6 | `entry:107` line form removed, rules survive | CONFIRMED — but its wording breaks the frozen counter (below) |

## Blocker the L1 must apply before appending

`block-as-drafted.md` names `S303` in the E6 bullet. `quality/counters/c2-r45-monitor-entry.py` clause g
(`all_body_lines_bound`) requires every unfenced entry line naming a cited id to carry that id's Gate quote and
locator, so appending the block verbatim scores `admitted=0/1 TARGET_MISSED` (both the r45 counter and its v2)
against `admitted=1/1 TARGET_MET` at baseline. `block-fixed.md` — same block, blank line prepended, the id
replaced by "(the handler row the entry's source list cites)" — scores `admitted=1/1 TARGET_MET` on both.
Evidence: `receipts/counter-append-test.txt`, `receipts/block-diff.txt`.

## Artifacts

| file | what it is |
|---|---|
| `verify-r45-errata.py` | offline re-derivation of every erratum + shape check; run it with `python3 -I` |
| `receipts/verify-r45-errata.txt` | its output, `RESULT: mismatches=0` (102 lines) |
| `counter-append-test.sh` | the clone-and-append experiment; args: `<work> <as-drafted> <fixed>` |
| `receipts/counter-append-test.txt` | baseline MET, verbatim MISSED (g:0), fixed MET |
| `block-as-drafted.md` | the fenced block of `w1/ScrErrataR45/errata.md`, verbatim (37 lines) |
| `block-fixed.md` | the appendable block: leading blank line + id token removed (38 lines) |
| `receipts/block-diff.txt` | the two-line diff between them |
| `receipts/host-shape.txt` | read-only `hyprctl -j monitors all` shape check (lengths only; no names/serials) |
| `receipts/90d-probe.txt` | `90d` re-probe: REST `http_code=422` with `http_code_full=200`, HTML `404` vs control `200` |
| `receipts/w1-verify-rerun.txt` | the w1 seat's own verifier re-run, `mismatches=0` |
| `pins/` + `pins/PINS.md` | four pins with URL + sha256 (aquamarine v0.15.1 tarball, Null.cpp, Backend.cpp, ConfigManager.hpp at a9902ea) |
