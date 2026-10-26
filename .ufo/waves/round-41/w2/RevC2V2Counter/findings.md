# RevC2V2Counter — Attack on `PRED-C2-r41-v2` (`quality/counters/c2-r41-focus-entry-v2.py`) and `run-c2-v2-controls.py`

Reviewed `quality/counters/c2-r41-focus-entry-v2.py` (frozen at `294c667901a8c7b7165ba849d03cba9a24c14fa4`) line-by-line against its docstring (lines 2–88) and `.ufo/waves/round-41/ctl/run-c2-v2-controls.py` (67 controls: `P-real`, `P-patched`, and 65 mutants; receipt `.ufo/waves/round-41/receipts/ctl-c2-v2.txt`). Also scored the data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1` (`admitted=1/1 verdict=TARGET_MET`).

All PoC fixtures were built using the control runner's own recipe (`D=$(mktemp -d)`, `git -C "$D" init -q`, `rev-parse --show-toplevel` verified equal to `$D` before the first commit, throwaway identity via `-c`, cleaned up in `finally`). Harness: `.ufo/waves/round-41/w2/RevC2V2Counter/poc_c2_v2.py`; output receipt: `.ufo/waves/round-41/w2/RevC2V2Counter/poc-results.txt`.

---

## Findings by Severity

### HIGH-1 — `run-c2-v2-controls.py:327-336` (`patched_counter`) has a Python dict-key shadowing bug that leaves 11 receipt-mutating controls pinned to the original hashes; `W16-quote-across-html-blocks` is NOT fixed in `c2-r41-focus-entry-v2.py` and passes (`admitted=1/1`) on both the fixed patched counter and the frozen real counter (`POC01`)
- **Target:** `.ufo/waves/round-41/ctl/run-c2-v2-controls.py:327-336` and `quality/counters/c2-r41-focus-entry-v2.py:9-13, 264-280`.
- **Mechanism:**
  1. `run-c2-v2-controls.py:10-12` states: *"patched: a copy of the counter whose PINS also hold the fixture's own receipts - so a clause mutant is killed by ITS clause, not by the pin."*
  2. `patched_counter()` (`run-c2-v2-controls.py:333`) executes `src = src.replace("PINS = {\n", "PINS = {\n" + extra, 1)`. Because `extra` is inserted at the **top** of the `PINS = { ... }` dict literal, the original 9 keys in `PINS` (`c2-r41-focus-entry-v2.py:125-135`) appear **after** `extra` in the dict literal and overwrite `extra` when Python constructs the dict.
  3. Consequently, for all 11 `"patched"` controls that mutate a receipt whose filename is in `PINS` (`J02`, `J03`, `J11`, `J16`, `J17`, `N04`, `N05`, `W14`, `W15`, `W16`, `W17`), `PINS.get(os.path.basename(path))` still returns the **unmodified pre-wave SHA-256**, so `pin_ok` is `False` in clause `d` (`receipts/ctl-c2-v2.txt:21-22,27-29,33-34,57-60`).
  4. For `W16-quote-across-html-blocks` (`run-c2-v2-controls.py:242-243`, which tests `c2-r41-focus-entry-v2.py:12` *"a quote assembled across HTML blocks"*), `issue-565.html` starts with `<html><p>New windows in inactive</p><p>workspaces stealing focus</p>...`. In `c2-r41-focus-entry-v2.py:264-280`, `looks_html(blob)` returns `True`, and `norm(text)` replaces every `<[^>]+>` with `" "` and collapses whitespace (`re.sub(r"<[^>]+>", " ", text)`). The two `<p>` blocks are still joined into `"New windows in inactive workspaces stealing focus"`. `W16` only scored `0/1` in `ctl-c2-v2.txt:59` because `patched_counter()` failed to override `PINS["issue-565.html"]`.
  5. Even on the **unmodified frozen real counter** (`COUNTER`), the pinned `.ufo/waves/round-41/fetch/issue-565.html` allows a quote assembled across separate HTML block elements (e.g. `"GitHub Skip to content Navigation Menu"`, spanning `<title>`, `<a>`, `<header>`) that never occurs as contiguous text in `issue-565.html`.
- **Reproduction (`poc_c2_v2.py` / `poc-results.txt`):**
  - `control=W16-quote-across-html-blocks broken_patched=(1, admitted=0/1 verdict=TARGET_MISSED, a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1) | fixed_patched=(0, admitted=1/1 verdict=TARGET_MET, a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1)`
  - `poc=POC01-real-html-quote-across-blocks scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`

### HIGH-2 — PINS bypasses (`c2-r41-focus-entry-v2.py:125-135, 368-370`): `PINS` is an unindexed `filename -> sha256` map of 9 files (2 uncited by the entry) that never binds which ID may cite which receipt, and exempts held IDs from `PINS` even when overwriting a pinned filename (`POC02`–`POC05`)
- **Target:** `quality/counters/c2-r41-focus-entry-v2.py:42-43, 125-135, 367-370`.
- **Mechanism:**
  1. **Reuse of the 2 unused pinned `.xml` and `.hpp` receipts (`POC02`):** `PINS` (`:125-135`) pins 9 files, whereas the genuine entry cites 7 new IDs (`S283`–`S289`). Both `"Hyprland-FocusGrab.hpp"` (`:127`) and `"input-capture-v1.xml"` (`:129`, for the sibling `hyprland_input_capture_v1` protocol, which `corpus/lessons/round-41.md:45` notes *"is not cited by the entry and has no row"*) are in `PINS`. Any new ID can cite `input-capture-v1.xml` or `Hyprland-FocusGrab.hpp` in place of `focus-grab-v1.xml` or `Hyprland-FocusGrab.cpp` and pass `pin_ok`.
  2. **Pinned file cited for a different ID / full permutation (`POC03`):** `pin_ok` (`:369-370`) checks only `PINS.get(os.path.basename(path)) == digest and path == FETCH + os.path.basename(path)`. It does not bind `i` (the source ID) or row metadata to the receipt. Permuting the 6 non-journal pinned receipts across `S283`–`S288` (while keeping `S283`–`S288`'s original rows and locations in `corpus/SOURCES.md`) fails clause `e` if locations are unchanged, or passes all clauses `a`–`i` (`admitted=1/1`) when paired with the location-binding bypass below or when `S283`–`S288`'s rows swap receipts/locations across IDs.
  3. **Swapping `own-work` and `docs` IDs (`POC04`):** `S283` can be marked `own-work` citing `xdph-journal.txt` while `S289` is marked `docs` citing `focus-grab-v1.xml`; the real counter admits it (`admitted=1/1`).
  4. **Held-ID overwrite of a pinned file in `fetch/` (`POC05`):** Clause `d` (`:367-368`) checks `if i in new_ids: pin_ok = ...`. If a held ID (e.g. `S050` or `S037`, where `i not in new_ids`) cites `.ufo/waves/round-41/fetch/protocols-README.md` (one of the 9 filenames in `PINS`) and overwrites that file in git with 512+ bytes of forged text (while no new ID cites `protocols-README.md`), `pin_ok` remains `True` and the real counter scores `admitted=1/1`.
  5. **Rename check:** Renaming a receipt file for a **new** ID (e.g. `other-name.txt` with a pinned file's SHA-256) is blocked by `PINS.get(os.path.basename(path)) == digest` (tested by `F5-receipt-renamed`). Renaming is only possible for a **held** ID (`i not in new_ids`).
- **Reproduction (`poc_c2_v2.py` / `poc-results.txt`, all on the unmodified real counter):**
  - `poc=POC02-pins-reuse-unused-xml-hpp scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`
  - `poc=POC03-pins-full-id-permutation scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`
  - `poc=POC04-pins-swap-docs-and-ownwork scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`
  - `poc=POC05-held-id-overwrites-pinned-file scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`

### HIGH-3 — Clause `e` location/receipt-name binding and location-uniqueness bypasses (`c2-r41-focus-entry-v2.py:48-51, 338-339, 399-420`): 1-character `.` path component, superstring component, and `?query` location duplication (`POC06`, `POC07`)
- **Target:** `quality/counters/c2-r41-focus-entry-v2.py:48-51, 338-339, 399-420`.
- **Mechanism:**
  1. **1-character `.` or `.ext` path component (`comp in rb`, `POC06`):** Clause `e` (`:406-409`) computes `comp = re.split(r"[?#]", cells_[1].split()[-1])[0].rstrip("/").rsplit("/", 1)[-1].lower()` and checks `bool(comp) and (comp in rb or rb in comp)`. Because every receipt filename `rb` in `PINS` contains `.` (`.xml`, `.cpp`, `.html`, `.md`, `.txt`), a location whose last path component is `"."` (e.g. `https://unrelated-0.invalid/.`) or `".xml"` / `".cpp"` satisfies `"/" in loc and "." in loc` (clause `c`, `:339`) and `comp in rb` (clause `e`, `:409`) for **every** receipt without naming any file.
  2. **Superstring path component (`rb in comp`, `POC07`):** Because clause `e` is a two-way substring check (`comp in rb or rb in comp`), a path component concatenating all 6 receipt basenames (`focus-grab-v1.xml-Hyprland-FocusGrab.cpp-quickshell-grab.cpp-xdph-PortalManager.cpp-issue-565.html-protocols-README.md`) satisfies `rb in comp` for **every** new ID simultaneously.
  3. **Query-string duplicate locations (`POC07`):** Clause `e` strips `[?#]` when computing `comp` (`:406`), but only strips `#` when checking location uniqueness (`key = loc.split("#")[0]`, `:415`). Thus all 6 new IDs (`S283`–`S288`) can point to the exact same URL path `https://single-url.invalid/<mega_comp>?dup=0` .. `?dup=5` and pass both `rb in comp` and `same == [i]`.
- **Reproduction (`poc_c2_v2.py` / `poc-results.txt`, on the unmodified real counter):**
  - `poc=POC06-loc-1char-dot-substring scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`
  - `poc=POC07-loc-query-dup-and-superstring scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`

### HIGH-4 — Which docstring sentences have no control in `run-c2-v2-controls.py` (67 controls)?
- **Target:** `quality/counters/c2-r41-focus-entry-v2.py:21-79` vs `.ufo/waves/round-41/ctl/run-c2-v2-controls.py:145-267`.
- **Mechanism & Complete Inventory:** By ablating each sub-condition of `c2-r41-focus-entry-v2.py` and by inspecting multi-clause kills across the 65 mutant controls (verified in `poc_c2_v2.py` and ablation runs), **23 docstring requirements have zero dedicated/isolating control** in the 67-control suite (their enforcing code can be deleted from `c2-r41-focus-entry-v2.py` without changing a single control's `admitted` verdict):
  1. **Clause `a` (`:21-22`) — *"is absent at BASE (present at BASE is a setup error, exit 2)"*:** Enforced at `:485-487`, **0 controls** in `run-c2-v2-controls.py` put the entry in `base`.
  2. **Clause `b` (`:23-24`) — *">= 4 distinct `source: S###` lines"*:** Enforced at `:305, 315`, **0 controls** reduce the entry's header `source:` count below 4 or duplicate a `source: S###` line (`N07` only deletes rows from `SOURCES.md`, leaving 8 `source:` lines in the entry).
  3. **Clause `b` (`:24-25`) — *"exactly one `verified-at: 2026-10-25` and exactly one `recheck:` (an ISO calendar date, `NNd` or `on-*`)"*:** Enforced at `:313, 315` (`len(vals) == 1` and `recheck_ok(rc)`), **0 controls** test `recheck:` in the entry header (`W07`/`W08` only mutate `SOURCES.md` cell 9) or duplicate `verified-at:`/`recheck:` inside the first 20 unfenced lines.
  4. **Clause `b` (`:25-26`) — *"no `source:`, `verified-at:` or `recheck:` line outside that window (outside fences)"*:** `W04` tests `source:` past line 20; **0 controls** test `verified-at:` or `recheck:` outside the 20-line window (`W01` moves `verified-at:`/`recheck:` past line 20, which already fails `va == OPENED` and `recheck_ok(rc)` inside the window even if `window == 0` is deleted).
  5. **Clause `b` (`:27`) — lowercase `s###` in *"no `S###`/`s###` token anywhere in the entry"*:** `W02` changes `source: S288` to `source: s288`, which drops `S288` from `ids` while `**OBS** S288` remains in the body; thus `ghosts` already catches uppercase `S288` even if `[Ss]` is weakened to `S`. **0 controls** isolate a lowercase `s999` body token.
  6. **Clause `c` (`:29-30`) — *"every cited id has exactly one `## Registry` row (0-3 leading spaces), 11 cells"*:** **0 controls** test duplicate registry rows (`len(rows) == 2`), >3 leading spaces on a row, or != 11 cells (`N02` and `N07` test `len(rows) == 0`).
  7. **Clause `c` (`:31-32`) — *"ids absent from the BASE registry (at least 3)"*:** `N07-two-new-ids-left` (`run-c2-v2-controls.py:165-171`) deletes the registry rows for `S283`–`S287` from `SOURCES.md` **without** removing `S283`–`S287` from the entry's `source:` header! Thus `N07` fails `rows_ok` (`len(rows) == 0` for `S283`–`S287`) before `len(new_ids) >= 3` (`:343`) is ever reached; deleting `and len(new_ids) >= 3` does not flip `N07`.
  8. **Clause `c` (`:32-33`) — *"location (last whitespace token of cell 1) holding a `/` and a `.`"*:** `W09-row-without-location` replaces the URL with `"surfaces"`, which lacks both `/` and `.` AND simultaneously fails clause `e` (`"surfaces" not in "focus-grab-v1.xml"`). Neither `"/" in loc` nor `"." in loc` is isolated.
  9. **Clause `d` (`:38-39`) — *"no `GATE S###` line sits outside that section"*:** **0 controls** place a `GATE S###` line outside `## Gate`.
  10. **Clause `d` (`:37`) — *"starting in column 0"* (`not gates.get("<indented>")`):** `X11-gate-lines-indented` indents all `GATE` lines, which already causes `GATE_RE` (`^GATE ...`) to match 0 lines (`len(gl) == 0`), so `gates["<indented>"]` (`:351-352, 397`) is dead/redundant on all controls.
  11. **Clause `d` (`:39-40`) — *"committed at REV under .ufo/waves/round-41/fetch/ ... >= 512 bytes"*:** **0 controls** test a receipt path outside `fetch/`, a subdirectory under `fetch/`, or `< 512` bytes.
  12. **Clause `d` (`:40`) — *"with exactly that sha256"* (`hashlib.sha256(blob).hexdigest() == digest`):** `N03-gate-sha-wrong` mutates `S283` (a new ID), which is already caught by `PINS.get(...) == digest` (`pin_ok`); **0 controls** mutate the SHA-256 of the held ID `S050` (the only ID where `sha256(blob) == digest` is not redundant with `pin_ok`).
  13. **Clause `d` (`:41`) — *"no two ids share a path, a sha256"* (`path not in seen_paths and digest not in seen_sha`):** **0 controls** share a receipt path or SHA-256 between two IDs.
  14. **Clause `d` (`:41-42, 44-47`) — *"or a whitespace-normalized quote"* (`nq not in seen_quote`) AND *"and in no OTHER cited receipt"* (`:390-396`):**
      - In `W12-quote-whitespace-distinct` (`run-c2-v2-controls.py:229-232`), `S288` is given `"Wayland  protocol extensions..."` (double space), which is normalized to single space in `seen_quote`, and `S283` (`focus-grab-v1.xml`) is given `"Wayland protocol extensions for Hyprland."`. Because `S283` is evaluated **before** `S288` (`ids` order) and `"Wayland protocol extensions for Hyprland."` does **not** occur in `focus-grab-v1.xml`, `S283` fails `nq in norm_receipt(blob)` first (`clause=d id=S283 gates=1 bound=0`), and is never added to `seen_quote`!
      - In `W15-quote-in-two-receipts` (`run-c2-v2-controls.py:239-241`), `S288` is given the **exact same quote string** as `S283`, so `S288` fails `nq not in seen_quote` at `:377` and is never added to `receipts`; thus the cross-receipt loop at `:390-396` (`quote of %s also in receipt of %s`) **never fires on any of the 67 controls**!
  15. **Clause `d` (`:44`) — *"the quote is 3-25 words"* (lower bound `3 <=`):** `N05` tests 26 words; **0 controls** test `< 3` words.
  16. **Clause `d` (`:45-46`) — *"scripts and styles dropped"* in HTML receipts (`:277-278`):** **0 controls** put a quote inside `<script>` or `<style>`.
  17. **Clause `e` (`:48-49`) — *"each new id's location, without its `#fragment`, occurs in no other registry row"* (`same == [i]` and `.split("#")[0]`):** In both `N09-duplicate-location` and `W13-location-fragment-duplicate`, `S284` or `S288` is given `S283`'s URL (`.../hyprland-focus-grab-v1.xml[#frag]`), which already fails `comp in rb or rb in comp` against `Hyprland-FocusGrab.cpp` / `protocols-README.md` (`:409`). Deleting `same == [i]` and `.split("#")[0]` changes 0 control verdicts.
  18. **Clause `f` (`:52-53`) — *"exactly one column-zero index row"* (upper bound `== 1` vs `>= 1`):** `N06` and `X07` test 0 rows; **0 controls** test 2 rows.
  19. **Clause `g` (`:56`) — *"and that line is not the census line of h"* (`:436-437`):** **0 controls** test this (and no valid `journal sessions=...` line can match `\bS\d{3,}\b` anyway).
  20. **Clause `h` (`:57`) — *"exactly one new cited row has kind own-work"* (upper bound `len(own) == 1` vs `>= 1`):** `N15` tests 0 `own-work` rows; **0 controls** test 2 `own-work` rows.
  21. **Clause `h` (`:58-59`) — *"not a tool's report"*:** Unenforced in code (`POC14` passes with `"MADO_GLOBALS_TOOL_REPORT v1"` header) and **0 controls** test it.
  22. **Clause `h` (`:64-66`) — individual floors `S >= 2`, `A >= 40`, `D >= 20`, `F >= 1`, and `firsts == sorted(firsts)`:**
      - `D >= 20` (`jc[2] >= 20`) is **never violated** by any control (`J02` has `D=31`, `J17` has `D=30`).
      - `J02-single-session` violates `S >= 2`, `A >= 40`, and `boots > 0` simultaneously (and also `pin_ok` under the broken `patched_counter`).
      - `J03-no-focus-grab-advert` replaces `hyprland_focus_grab_manager_v1` in `xdph-journal.txt` without updating `S289`'s quote, so `S289` fails clause `d` (`quote not in norm_receipt`) and `receipts_raw` has no `S289`!
      - `J17-sessions-replayed` appends lines `117:` (which omits line 116 where `hyprland_focus_grab_manager_v1` sits!), so `J17` has `F=0` (`jc[3] == 0`) in addition to `jc[5] == False`. Thus `jc[5]` (distinct ascending session timestamps) and `pid != cur[0]` are never isolated.
  23. **Clause `i` (`:75-78`) — `BAD_LOC` check (`not bad`):** Both `A05-localized-channel-source` (`https://amgsk.dev/posts/hyprland-rules/`) and `F4-localized-redirect` (`https://t.co/9xQ2fG`) replace `S288`'s location with a URL whose last component (`hyprland-rules` / `9xq2fg`) fails **clause `e`** (`comp in rb or rb in comp` against `protocols-README.md`)! Deleting `and not bad` from clause `i` leaves both `A05` and `F4` at `admitted=0/1` (`e:0`).

---

### MEDIUM-1 — STAGED allowlist and ADMIT/REFUSE bypasses (`c2-r41-focus-entry-v2.py:72-75, 119-120, 137-151, 455-461`): `os.path.basename` ignores directory path, `./` prefix allows ADMITting and REFUSEing the same file, punctuation-stuffed 1-word reason passes, and invalid extra ADMIT/REFUSE lines are ignored (`POC08`)
- **Target:** `quality/counters/c2-r41-focus-entry-v2.py:72-75, 119-120, 137-151, 455-461`.
- **Mechanism:**
  1. `staged_ok = lambda p: os.path.basename(p) in STAGED` (`:457`) strips all leading path components. `ADMIT /evil/nonexistent/../../focus-control-surfaces-r28.md as corpus/knowledge/hyprland-focus-grab-r41.md` passes `staged_ok`.
  2. Docstring (`:75`) requires *"the REFUSE target differs from every ADMIT target"*, but `:461` checks `all(m.group(1) != a.group(1) for a in adm)` on the raw regex group `m.group(1)` while `staged_ok` checks `os.path.basename`. Thus `ADMIT merge/mado/.../focus-control-surfaces-r28.md` and `REFUSE ./focus-control-surfaces-r28.md` name the **exact same staged file** and pass (`m.group(1) != a.group(1)` is `True`).
  3. Docstring (`:73-74`) requires `reason=<text of >= 4 distinct words>`, implemented as `len(set(m.group(2).lower().split())) >= 4` (`:460`) with `REFUSE_RE` `(.{20,})$` (`:120`). Because `.split()` does not strip punctuation, `reason=a. a, a; a! a? a: a- a_ a/ a` has 10 "distinct" whitespace tokens and passes.
  4. Because `cl["i"]` checks `bool(adm) and bool(ref)` (`:468`), any number of additional `ADMIT`/`REFUSE` lines naming nonexistent files, self-refusing the admitted file, or carrying 1-word reasons are silently ignored as long as one valid `ADMIT` and one valid `REFUSE` exist.
- **Reproduction (`poc_c2_v2.py` / `poc-results.txt`, on the unmodified real counter):**
  - `poc=POC08-staged-prefix-selfrefuse-punct scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`

### MEDIUM-2 — `BAD_LOC` false positives on genuine English sources and trivial localized-channel bypasses (`c2-r41-focus-entry-v2.py:76-78, 121-122, 462-467`) (`POC09`, `POC10`)
- **Target:** `quality/counters/c2-r41-focus-entry-v2.py:76-78, 121-122, 462-467`.
- **Mechanism:**
  1. **Genuine set check:** On the committed round-41 data (`07f2641696b5ac73de1404ea737a9f27e9819aa1`, 226 rows in `corpus/SOURCES.md`) and control `G`, `BAD_LOC` has **0 hits** on `SOURCES.md` rows. However, the genuine pinned receipt `.ufo/waves/round-41/fetch/issue-565.html` itself contains `"/ja"` (`https://github.githubassets.com/assets/ja9-b94de714266ba389.js`), and because `row_text = " ".join(rows[0]).lower()` (`:466`) concatenates **all 11 cells** of every cited row (including `scope`, `anchor`, `teaches`), any English row whose `scope`/`teaches` cell mentions excluding `/ja` or `/zh` channels (as `corpus/knowledge/hyprland-focus-grab-r41.md:14` and `corpus/lessons/round-41.md:53` do!), or whose URL/path/commit-hash contains `/ja` (`/java`, `/javascript`, `/ja9b94de`) or `/zh` (`/zhang`), is falsely rejected (`i:0`, `POC09`).
  2. **Trivial bypasses (`POC10`):** `BAD_LOC` (`:121-122`) checks `("/zh", "/ja", "/jp/", "/cn/", ...)` with leading slashes and no URL decoding. Country-code TLDs (`.jp/`, `.cn/` — preceded by `.` rather than `/`), major localized hosts (`juejin.cn`, `csdn.net`, `note.com`, `hatenablog.com`, `bilibili.com`), and URL percent-encoding (`%7ah` for `zh`, `%6aa` for `ja`) completely evade `BAD_LOC`.
- **Reproduction (`poc_c2_v2.py` / `poc-results.txt`, on the unmodified real counter):**
  - `poc=POC09-badloc-false-positive-english-row scorer=real rc=1 admitted=0/1 verdict=TARGET_MISSED clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0`
  - `poc=POC10-badloc-bypass-tld-percent-encode scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`

### MEDIUM-3 — Header window (`c2-r41-focus-entry-v2.py:23-28, 111-112, 249-254, 292-316`) and `## Gate` section rules (`:36-39, 345-357`) allow indented `source:`/`verified-at:`/`recheck:` lines past line 20, unvalidated `source: <url>` lines inside line 20, trailing garbage in `recheck:`, and duplicate/uncited `GATE S###` lines outside and inside `## Gate` (`POC11`, `POC12`)
- **Target:** `quality/counters/c2-r41-focus-entry-v2.py:109-112, 249-254, 292-316, 345-357`.
- **Mechanism:**
  1. **Header window (`POC11`):**
     - Line 300 checks `elif re.match(r"^(source|verified-at|recheck):", l): window += 1` (column-0 anchored). Any `  source: S283`, `  verified-at: 1999-01-01`, or `  recheck: bad` indented by >= 1 space past line 20 is ignored (`window == 0`).
     - Inside the first 20 lines, `SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")` (`:112, 304`) silently ignores any `source:` line that does not start with `S\d{3,}` (e.g. `source: https://amgsk.dev/ja/untracked-source` has no `S###` token, so `ghosts` is empty and clause `i` never sees it).
     - `RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")` (`:111`) accepts `0d`, `on---`, and arbitrary trailing text after the first whitespace token (`recheck: 0d UNVALIDATED_TRAILER 2026-99-99`).
  2. **Clause `d` `GATE S###` rules (`POC12`):**
     - Lines 354–357 check `in_gate = set(glines)` and `if re.match(r"^GATE S\d", line) and line not in in_gate: outside += 1`. Because `in_gate` is a set of line strings, repeating any valid `GATE S### ...` line **outside** `## Gate` satisfies `line in in_gate`, so `outside` remains `0` directly contradicting *"no `GATE S###` line sits outside that section"* (`:38-39`).
     - Inside `## Gate`, `for i in ids: gl = gates.get(i, [])` (`:361-363`) ignores `GATE S999 ...` for any uncited ID and ignores any malformed `GATE S283 ...` line that fails `GATE_RE`.
- **Reproduction (`poc_c2_v2.py` / `poc-results.txt`, on the unmodified real counter):**
  - `poc=POC11-header-indented-outside-and-trailer scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`
  - `poc=POC12-gate-outside-section-and-uncited scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`

### MEDIUM-4 — Clause `h` provenance floor bypasses (`c2-r41-focus-entry-v2.py:57-71, 114-118, 209-236, 422-433`): held `own-work` rows bypass `len(own) == 1`, and `journal_counts()` accepts tool-report wrappers, invalid calendar timestamps (`9999-99-99`), UTC-reversed session timestamps across timezones, non-monotonic intra-session timestamps, and a single trailing `-- Boot` line (`POC13`, `POC14`)
- **Target:** `quality/counters/c2-r41-focus-entry-v2.py:57-71, 114-118, 209-236, 422-433`.
- **Mechanism:**
  1. **Second cited `own-work` row via held ID (`POC13`, on the real counter):** Line 422 filters `own = [i for i in new_ids if reg_rev[i][0][2] == "own-work"]`. The lane's `corpus/SOURCES.md` at `BASE` (`ab2bfaab66...`) already has 23 held rows with `kind == "own-work"` (e.g. `S001`, `S002`, `S055`). Citing one of those held `own-work` rows alongside `S289` gives two cited `own-work` rows (and the held `own-work` row can use a forged non-journal receipt in `fetch/`), yet `len(own) == 1` still holds (`admitted=1/1`).
  2. **Provenance floor weaknesses in `journal_counts()` (`POC14`, on the fixed patched counter):**
     - **Tool report wrapper:** `journal_counts()` (`:218-220`) skips any line not matching `BOOT_RE` or `ADV_RE`, so a tool dump starting with `MADO_GLOBALS_TOOL_REPORT v1` is accepted against `:59` (*"not a tool's report"*).
     - **Unvalidated timestamps & timezone sort inversion:** `ADV_RE` (`:115`) matches digits `[0-9]{4}-[0-9]{2}-[0-9]{2}T...` without `valid_date()`, admitting `9999-99-99T12:00:00+00:00`. And `firsts == sorted(firsts)` (`:235`) sorts raw strings lexicographically (`"+00:00" < "+05:00"`), admitting a second session at `12:00:00+05:00` (07:00 UTC) that occurred **5 hours before** the first session at `12:00:00+00:00` (12:00 UTC). Intra-session timestamps after the first advert of a session are never checked at all (`12:00:00` followed by `00:00:00`).
     - **Decoupled `boots > 0`:** A single `-- Boot 00...00 --` line at the very end of the file (after all adverts, separating zero sessions while sessions split only by PID) satisfies `boots > 0` (`:216, 234`).
- **Reproduction (`poc_c2_v2.py` / `poc-results.txt`):**
  - `poc=POC13-second-ownwork-held-row scorer=real rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`
  - `poc=POC14-journal-provenance-floor-bypass scorer=fixed-patched rc=0 admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`

---

## Verification of Committed Round-41 Data (`07f2641696b5ac73de1404ea737a9f27e9819aa1`)

- Ran `python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 --base ab2bfaab661c846d1de9d58c01651cd156a13949` → `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET rev=07f2641696b5ac73de1404ea737a9f27e9819aa1` (exit 0; all clauses `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`).
- Checked the landed data (`corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/SOURCES.md` rows `S283`–`S289` and `S037`, `corpus/lessons/round-41.md`, `corpus/README.md`, `.ufo/waves/round-41/fetch/xdph-installed-version.txt`): none of the predicate bypasses above are exploited by the landed round-41 data. Allfindings above are open defects of the v2 predicate (`c2-r41-focus-entry-v2.py`) and its control runner (`run-c2-v2-controls.py`).

## Tooling & Safety

- No tools installed or updated (Python 3.14 stdlib only).
- All git fixture repositories created via `tempfile.mkdtemp()` in `/tmp`, verified `rev-parse --show-toplevel`, committed with `-c user.name=ctl -c user.email=ctl@ctl.invalid`, and removed in `finally`.
- No tracked lane files or git state modified.
