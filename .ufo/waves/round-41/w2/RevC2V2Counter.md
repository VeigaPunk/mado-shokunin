# RevC2V2Counter — Attack on `PRED-C2-r41-v2` (`quality/counters/c2-r41-focus-entry-v2.py`)

Status: **DONE**. Full severity-ranked findings, line references, and PoC reproductions:
`.ufo/waves/round-41/w2/RevC2V2Counter/findings.md`
PoC harness and output receipt:
- `.ufo/waves/round-41/w2/RevC2V2Counter/poc_c2_v2.py`
- `.ufo/waves/round-41/w2/RevC2V2Counter/poc-results.txt`

## Summary of Findings (Predicate & Control Runner Defects; Data Commit `07f264169` Clean)

1. **HIGH-1 (`run-c2-v2-controls.py:327-336` dict-key shadowing bug & `W16-quote-across-html-blocks` survivor in `c2-r41-focus-entry-v2.py:264-280`):**
   - `patched_counter()` inserts `extra` at the **start** of `PINS = {\n`, so the original 9 keys in `PINS` appear later in the dict literal and overwrite `extra`. All 11 `"patched"` controls that modify a pinned receipt (`J02`, `J03`, `J11`, `J16`, `J17`, `N04`, `N05`, `W14`, `W15`, `W16`, `W17`) fail `pin_ok` (`d:0`) instead of being isolated to their target clause.
   - When `patched_counter()` is fixed so fixture receipts override `PINS`, **`W16-quote-across-html-blocks` scores `admitted=1/1 verdict=TARGET_MET`** (`norm()` at `:279` still replaces `<p>` tags with spaces). Even on the **unmodified frozen real counter**, a quote spanning separate HTML blocks in the pinned `issue-565.html` (`"GitHub Skip to content Navigation Menu"`) scores `admitted=1/1` (`POC01`).
2. **HIGH-2 (PINS bypasses, `c2-r41-focus-entry-v2.py:125-135, 367-370`):**
   - `PINS` includes 2 uncited files (`input-capture-v1.xml` and `Hyprland-FocusGrab.hpp`) that any new ID can cite (`POC02`: `admitted=1/1` on real counter).
   - `PINS` is an unindexed `filename -> sha256` dict that does not bind which ID cites which receipt: permuting all 6 non-journal pinned receipts across `S283`–`S288` (`POC03`) or swapping `S283` (`docs`) and `S289` (`own-work` journal) (`POC04`) both score `admitted=1/1` on the real counter.
   - Held IDs (`i not in new_ids`) skip `pin_ok` (`:368`) and can overwrite a pinned filename (e.g. `protocols-README.md`) in `fetch/` with forged bytes (`POC05`: `admitted=1/1` on real counter).
3. **HIGH-3 (Location/receipt-name binding & uniqueness bypasses, `c2-r41-focus-entry-v2.py:406-420`):**
   - `comp in rb or rb in comp` (`:409`) admits a 1-character `"."` or `".xml"` path component (`comp in rb`) for every new ID (`POC06`: `admitted=1/1` on real counter).
   - Conversely, a superstring path component concatenating all 6 receipt filenames satisfies `rb in comp` for every new ID, and because `:406` strips `[?#]` while `:415` only strips `#`, all 6 new IDs can share the same URL path via `?dup=0`..`?dup=5` (`POC07`: `admitted=1/1` on real counter).
4. **HIGH-4 (23 docstring clauses/sub-sentences with no isolating control in the 67-control suite):**
   - Detailed 23-row ablation inventory in `findings.md` (including `a` base precondition; `b` `>= 4` distinct sources, header `recheck:`, `verified-at:`/`recheck:` outside window; `c` duplicate/malformed rows, `len(new_ids) >= 3` masked by missing rows in `N07`; `d` `GATE` outside `## Gate`, `< 512` B, non-`fetch/` path, held-ID sha256, duplicate path/sha, cross-receipt quote loop at `:390-396` masked in `W12`/`W15`, 3-word floor, `<script>/<style>`; `e` `same == [i]` and `#fragment` strip masked by `comp in rb` in `N09`/`W13`; `f` `> 1` README row; `g` census-line exclusion; `h` `> 1` own-work row, `"not a tool's report"`, `D >= 20`, `firsts == sorted(firsts)`; `i` `BAD_LOC` masked by clause `e` in `A05`/`F4`).
5. **MEDIUM-1 (STAGED allowlist bypasses, `:455-461`):** `os.path.basename(p) in STAGED` ignores arbitrary directory prefixes (`/evil/../../focus-control-surfaces-r28.md`), allows the same file to be both `ADMIT`ted and `REFUSE`d via `./` prefix (`m.group(1) != a.group(1)`), and accepts punctuation-stuffed 1-word `REFUSE` reasons (`reason=a. a, a; a! ...`) (`POC08`: `admitted=1/1` on real counter).
6. **MEDIUM-2 (`BAD_LOC` false positives & bypasses, `:121-122, 462-467`):** Zero hits on the 226 rows of the genuine `corpus/SOURCES.md`, but `issue-565.html` itself contains `"/ja"` (`ja9-b94de714266ba389.js`), and scanning all 11 cells rejects an English row whose `scope`/`teaches` cell disclaims `/ja` or whose URL/commit contains `/ja...` or `/zh...` (`POC09`: `i:0`). Conversely, `.jp`/`.cn` TLDs, `juejin.cn`, `note.com`, and percent-encoded `%7ah`/`%6aa` evade `BAD_LOC` (`POC10`: `admitted=1/1`).
7. **MEDIUM-3 (Header window & `## Gate` rules, `:292-316, 345-357`):** Indented `  source:`/`  verified-at:`/`  recheck:` lines past line 20, `source: <url>` without `S###` in the first 20 lines, `recheck: 0d <arbitrary trailer>` (`POC11`), and repeating an in-`## Gate` `GATE S###` line outside `## Gate` (`line not in in_gate` set bug) plus uncited `GATE S999` lines (`POC12`) all score `admitted=1/1` on the real counter.
8. **MEDIUM-4 (Clause `h` provenance floor, `:209-236, 422-433`):** Citing a held `own-work` row from `BASE` bypasses `len(own) == 1` (`POC13`: `admitted=1/1` on real counter); `journal_counts()` accepts tool-report headers, `9999-99-99` dates, UTC-reversed session starts across timezones (`+00:00` then `+05:00`), non-monotonic intra-session timestamps, and a single trailing `-- Boot` line (`POC14`: `admitted=1/1`).

Report: .ufo/waves/round-41/w2/RevC2V2Counter/findings.md
