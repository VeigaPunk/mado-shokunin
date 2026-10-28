# R55W2MutC1CounterB — mutation table for the C1 counter

Instrument: `quality/counters/c1-r55-kbd-entry.py` at scored rev `57584ed6` (its tree is identical to lane HEAD `721ba9c1` for every C1 path; `git diff --stat 57584ed6 HEAD -- quality corpus tools .ufo/waves/round-55/…` is empty).

Method. Each mutant is a copy of the instrument with exactly one line changed (`receipts/` and `mutants/mNN.diff` show each diff). Every mutant was run through (a) its own `--selftest` and (b) the independent harness `quality/check-r55-controls.py --claim c1 --counter mutants/mNN.py` against a scratch git repo (`--repo` = commit `937fb030` built from the exported tree, `--rev HEAD`). The unmutated instrument scores selftest 50/50 and harness 7/7 (`receipts/baseline-*`). All mutants were edited and run under `/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterB/`; nothing in the lane was edited.

Verdicts: **killed** = selftest or harness fails; **SURVIVOR** = both pass and the mutant's output differs from the original on an input the instrument's grammar admits (probe output in `receipts/probe-output.txt`); **EQUIVALENT** = no input distinguishes it.

| mutant | one-line edit (instrument line) | killed by (selftest / harness) | survivor risk |
|---|---|---|---|
| m01 | L61 `TABLES_SHA256` last hex `9`→`8` | selftest aborts rc=2 (sha mismatch on frozen-tables.json); harness good=bad, verdict FAIL | killed |
| m02 | L203 commit regex `{40}`→`{7,40}` | nothing (selftest 50/50; harness 7/7 OK) | **SURVIVOR, low–medium**: a 7-hex `commit` in frozen-tables gives `rows=18/18` on the mutant vs `rows=0/18` on the original (P1). Only reachable if the embedded sha is also changed, so the shape branch is effectively unguarded. |
| m03 | L274 `and c["commit"] not in url` → `and False and …` (Hyprland commit rule off) | nothing | **SURVIVOR, HIGH**: non-new pin S316 with registry URL pinned to `0000…` (no frozen commit) gives `TARGET_MET` on the mutant, `source_cell:K01…K07` on the original (P13). The Hyprland commit rule is the only guard for K rows whose pins are not new. |
| m04 | L274 `"Hyprland-"` → `"wayland-"` (prefix rule moved to the wayland pin) | selftest 12/50 (good-tree → `source_cell:K17`); harness good=bad, controls 2/7 | killed |
| m05 | L377 K proposition floor `40`→`39` | nothing | **SURVIVOR, medium**: K02 proposition of 39 chars gives `row:K02` on the original, `TARGET_MET` on the mutant (P3a). The 40-char boundary passes on both (P3b). |
| m06 | L377 H proposition floor `20`→`19` | nothing | **SURVIVOR, medium**: H04 proposition of 19 chars gives `row:H04` on the original, `TARGET_MET` on the mutant (P4a). |
| m07 | L76 `S_IN_LINE` drops `(?![0-9])` | nothing | **SURVIVOR, medium-low**: `source: S3160` (4-digit id) fails provenance on the original, passes on the mutant (P5). |
| m08 | L75 `SRC_ID` `^\| (S###) \|` → `^\|\s*(S###)\s*\|` | nothing | **SURVIVOR, medium**: a registry row written `\|S378\|` is counted, so the mutant reports `missed=none` and the original `source_cell:K10,new_rows` (P6). The original's exact spacing is not stated in the contract, so the test must pin it explicitly. |
| m09 | L166 CRLF tolerated (`text.replace("\r\n","\n")`) | selftest 48/50 (CRLF-single-row-K05, CRLF-whole-entry) | killed |
| m10 | `split_row` strips trailing spaces/tabs first | selftest 48/50 (trailing-spaces-after-row-K09, trailing-tab-after-row-H01) | killed |
| m11 | L145 `ent[0] not in REGULAR_MODES` dropped (symlink blob read as file) | selftest 49/50 (symlink-entry-file) | killed |
| m12 | L172 fenced-code skipping disabled | selftest 49/50 (row-only-inside-code-fence-K12) | killed |
| m13 | L179 HTML-comment skipping disabled | selftest 49/50 (row-only-inside-html-comment-K13) | killed |
| m14 | L380 proposition `prop != prop.strip()` dropped | nothing | **SURVIVOR, medium**: K02 proposition with a leading space gives `row:K02` on the original, `TARGET_MET` on the mutant (P7). |
| m15 | L286 `cells[3] != "A"` (tier A) dropped from `count_new_rows` | nothing | **SURVIVOR, medium**: a new-row registry entry at tier B is admitted (P8): `new_rows=2/3` vs `3/3`. Lets a non-A source satisfy the new-row floor. |
| m16 | L286 `cells[8] != c["opened"]` (opened = 2026-10-28) dropped | nothing | **SURVIVOR, medium**: a new row with opened 2026-10-27 is admitted (P9): `new_rows=2/3` vs `3/3`. |
| m17 | L337 `verified-at:` exact date → prefix match | selftest 48/50 (provenance-wrong-date) | killed |
| m18 | L415 rev echo uses resolved sha `R.sha` instead of argument | selftest 47/50 (good-tree exact line; repo-path-is-a-symlink; dirty-working-tree-ignored) | killed |
| m19 | L391 quote cell compared after stripping backticks (`` `` `` and bare accepted) | selftest 48/50 (backtick-style-double-K05, backtick-style-none-H06) | killed |
| m20 | L72 `ROW_ID` `\s*\|` → `\b` (first cell may be `K03 extra`) | nothing | **SURVIVOR, low (false-reject direction)**: a prose line `\| K03 extra \| … \|` is treated as a second K03 row, `row:K03` on the mutant, `TARGET_MET` on the original (P10). |
| m21 | L381 H-row `cells[2] != "host"` dropped | selftest 49/50 (host-row-src-cell-not-host-H03) | killed |
| m22 | L73 `SID` `^S[0-9]{3}$` → `^S[0-9]{3}` (no `$`) | nothing | **EQUIVALENT**: `source_ok` looks up the exact key in the registry, and every key is exactly `S###`; P11 output identical on both. |
| m23 | L67 `N_K, N_H = 18, 6` → `18, 7` | selftest rc=2 (setup); harness 0/7, empty stdout | killed |
| m24 | L391 quote-in-pin-line leg dropped (`or fr["quote"] not in pl` removed) | nothing | **SURVIVOR, medium (localisation only)**: pin line for K04 altered with hash now mismatched: original `quote:K04,pin_hash`, mutant `pin_hash` alone (P12). Verdict stays red via pin_hash; the row-level localisation is lost. The contract (counter docstring) says `quote:<id>` fires when the quote is not in the pin line. |

Totals: 24 mutants. Killed 12 (harness kills 3: m01, m04, m23). Survivors 11 (harness kills 0 of them: all 7/7 controls on every survivor). Equivalent 1 (m22).

Survivor test proposals (text only; each verified to distinguish on the unchanged instrument by the probe in `receipts/probe.py`):
- m03 (HIGH): registry-row fixture where a non-new Hyprland pin's row (S316, cited by K01–K07) carries a URL with the path suffix correct but without `efb50993…`. Expected `missed` includes `source_cell:K01`.
- m02: frozen-tables fixture with `c1.commit` = 7 hex (`efb5099`), tree otherwise good. Expected `rows=0/18 hosts=0/6 sources=0/18 new_rows=0/3 missed=tables_sha`, rc 1.
- m05 / m06: boundary pair. K02 proposition exactly 39 chars → `row:K02`; exactly 40 → pass. H04 proposition exactly 19 chars → `row:H04`; exactly 20 → pass.
- m07: provenance line `source: S3160` alone → `provenance`.
- m08: registry row `|S378|…` → pin the exact spacing outcome (`source_cell:K10,new_rows`), or document it as intentionally strict.
- m14: K02 proposition with leading space → `row:K02`.
- m15: new registry row at tier `B` → `new_rows=2/3`.
- m16: new registry row with opened `2026-10-27` → `new_rows=2/3`.
- m20: add `| K03 extra | note |` after the K03 row → expected TARGET_MET (no `row:K03`).
- m24: K04 pin line altered (hash now mismatched) → `missed` contains `quote:K04` and `pin_hash`.

Not run by any seat: harness controls for these inputs (the 7 frozen controls are the only harness cases), and the selftest branch "sha matches but shape invalid → rc 2" (only reachable with a two-edit copy, not tested by any shipped test).
