# R55W2MutC1CounterA — mutation test of the C1 counter `quality/counters/c1-r55-kbd-entry.py`

Seat: R55W2MutC1CounterA (wave w2, falsify round). Scored revision: `57584ed67716340b3d466fa04333ac0bab3fb79e`.
Instrument sha256 (exported at that revision): `30b0513f8080b8794aa40702385eda8266e0bc5931bad2e2861f4cbe905b3b46`.
Verdict vocabulary per target is in the seat report `.ufo/waves/round-55/w2/R55W2MutC1CounterA.md`.

## Method and bounds

- **Lane untouched.** The counter, the harness (`quality/check-r55-controls.py`, `quality/r55_ctl_c{1,2,3}.py`) and every
  input they read were exported read-only: `git -C <lane> archive 57584ed… quality/… corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md corpus/README.md corpus/SOURCES.md .ufo/waves/round-55/frozen-tables-v2.json .ufo/waves/round-55/fetch | tar -x -C <scratch>/export`.
  Those files were committed in a scratch repo (`git init`, `rev-parse --show-toplevel` asserted equal to the repo dir before the first commit; `-c user.name=ctl -c user.email=ctl@ctl`). Scratch commit: `fa1d6c7037810935ca566e86d1d99547efdbb664`, which carries the scored-revision bytes of those paths.
  No command ran against the lane or fleet repo except read-only `git show`/`git archive`/`git ls-tree`. No lane file was edited, restored or committed. The mutants are copies in `mutants/`; they were copied again into scratch (`run/<id>/counter.py`) and only the scratch copies were executed.
- **Mutants.** 32 one-edit copies, produced by `receipts/gen.py` from the exported source. Each applies exactly one `str.replace` whose old text occurs exactly once (asserted); each changes exactly 2 lines (one removed, one added). The eleven leg-drop mutants are required by the task (`entry_absent` … `tables_sha`); the others flip one comparison or remove one clause of a leg. Hash of each file: `receipts/manifest.json`.
- **Runs.** Per mutant, `receipts/one.sh` runs, with `python3 -I` and a per-mutant `--work` in scratch:
  - selftest: `python3 -I run/<id>/counter.py --selftest --repo <D> --rev HEAD --work run/<id>/st`
  - independent harness: `python3 -I quality/check-r55-controls.py --claim c1 --repo <D> --rev HEAD --work run/<id>/h --counter run/<id>/counter.py`
  where `<D>` is the scratch repo above. Outputs: `receipts/selftest/<id>.out`, `receipts/harness/<id>.out|.err`.
- **Baseline (unmutated, same scratch repo).** Counter: `MADO_KBD_ENTRY: rev=HEAD rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`, rc 0. Selftest: `MADO_KBD_ENTRY_SELFTEST: 50/50 passed`. Harness: `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`. Receipts: `receipts/baseline/`.
- **Nothing installed.** No tool was installed or upgraded for this probe; `hyprctl` was not invoked. Scratch lives under `/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterA/` and is removed before yield.
- **Selftest independence.** The counter's own selftest is written by the counter's author and is synthetic: its "good tree" is a generated entry and registry (`syn_entry`, `syn_registry`), not the real entry. It is an instrument check, not an independent one. Only the harness judges the real entry, and only through its good tree and seven controls.

## Results at a glance

- 32 mutants. **23 killed**: 11 by the independent harness (harness good-tree or control), 12 by the counter's selftest only. **9 survive every check** (no selftest case, no harness control, good tree still green): `m16 m19 m20 m21 m22 m24 m25 m26 m32`.
- Of the 9, **5 change the verdict** of a tree the unchanged counter marks TARGET_MISSED (m16, m19, m20, m21, m22; demonstrations A–E). Three change only the leg name while the verdict stays MISSED (m24, m26, m32; demonstrations F, G, H). One is stricter, not admissive (m25; unit probe).
- The eleven required leg-drop mutants: all eleven are killed. Harness controls exercise only 7 of the 11 legs (table below); `provenance`, `index`, `new_rows` have no harness control and `tables_sha` has no *required* one.

## Mutant table

Columns: `harness (good / controls)` is the harness's own summary line; `killed by` lists the failing harness controls (`C1-CTL-n` in `r55_ctl_c1.py` order, `good` = good-tree check) and the failing selftest cases; `survivor risk` says which behaviour is unguarded.

| id | file (mutants/) | what the edit removes or flips | edit (exact, one `str.replace`) | harness (good / controls) | killed by | survivor risk |
|---|---|---|---|---|---|---|
| m01 | `m01-entry_absent.py` | entry_absent never reported | `missed["entry_absent"].append("entry_absent")` -> `pass` | good=ok, controls=6/7 | harness: C1-CTL-1; selftest: 3/50 fail (CTL1-absent, symlink-entry-file, tree-without-any-r55-file) | LOW. Killed by the harness (CTL-1) and selftest. |
| m02 | `m02-provenance.py` | provenance trio never reported | `missed["provenance"].append("provenance")` -> `pass` | good=ok, controls=7/7 | selftest: 4/50 fail (provenance-no-recheck, provenance-no-S-id-in-source, provenance-wrong-date, ...) | MEDIUM. Provenance trio has no harness control; selftest only (4 cases). A stale or missing `verified-at`/`recheck`/`source:` line passes the harness. |
| m03 | `m03-index.py` | README index leg never reported | `missed["index"].append("index")` -> `pass` | good=ok, controls=7/7 | selftest: 3/50 fail (index-row-missing, index-row-duplicated, tree-without-any-r55-file) | MEDIUM. README index leg has no harness control; selftest only (index-row-missing, index-row-duplicated). |
| m04 | `m04-row.py` | row:<id> never reported | `missed["row"].append("row:" + rid)` -> `pass` | good=ok, controls=6/7 | harness: C1-CTL-5; selftest: 14/50 fail (CTL5-dropped-row-K17, host-row-src-cell-not-host-H03, short-proposition-K02, ...) | LOW for K17 only. Harness exercises row:K17 alone; the other 31 row-grammar failures rest on selftest (14 cases). |
| m05 | `m05-anchor.py` | anchor:<id> never reported | `missed["anchor"].append("anchor:" + rid)` -> `pass` | good=ok, controls=6/7 | harness: C1-CTL-3; selftest: 2/50 fail (CTL3-shifted-anchor-K01, anchor-wrong-pin-file-K08) | LOW for K01 only. Harness exercises anchor:K01 alone (K08 via selftest). |
| m06 | `m06-quote.py` | quote:<id> never reported | `missed["quote"].append("quote:" + rid)` -> `pass` | good=ok, controls=6/7 | harness: C1-CTL-2; selftest: 7/50 fail (CTL2-spliced-quote-K04, CTL6-host-forged-H02, backtick-style-double-K05, ...) | LOW. Quote leg exercised by CTL-2 (K04) and CTL-6 (H02 collateral). |
| m07 | `m07-pin_hash.py` | pin_hash never reported | `missed["pin_hash"].append("pin_hash")` -> `pass` | good=ok, controls=6/7 | harness: C1-CTL-7; selftest: 4/50 fail (CTL7-pin-tamper-tables-and-pin, pin-bytes-only-appended-space, symlink-pin-file-SeatManager, ...) | LOW. CTL-7 requires pin_hash. |
| m08 | `m08-source_cell.py` | source_cell:<id> never reported | `missed["source_cell"].append("source_cell:" + rid)` -> `pass` | good=ok, controls=6/7 | harness: C1-CTL-4; selftest: 4/50 fail (CTL4-wrong-source-K10, source-candidate-status-S380, source-cell-not-an-S-id-K02, ...) | LOW-MEDIUM. Harness exercises K10 wrong S-id only; the status leg rests on selftest, and the commit clause is unguarded (m16). |
| m09 | `m09-new_rows.py` | new_rows never reported | `missed["new_rows"].append("new_rows")` -> `pass` | good=ok, controls=7/7 | selftest: 3/50 fail (new-rows-usedby-missing-entry-S379, source-candidate-status-S380, symlink-sources-file) | HIGH. new_rows has NO harness control: the 7 frozen controls leave the registry rows that count toward new_rows untouched (CTL-4 changes a K10 cell, not a registry row). Selftest only (3 cases). |
| m10 | `m10-host.py` | host:<id> never reported | `missed["host"].append("host:" + rid)` -> `pass` | good=ok, controls=6/7 | harness: C1-CTL-6; selftest: 2/50 fail (CTL6-host-forged-H02, symlink-pin-directory) | LOW. CTL-6 requires host:H02 (H01-H06 otherwise unexercised). |
| m11 | `m11-tables_sha.py` | tables_sha never reported | `missed["tables_sha"].append("tables_sha")` -> `pass` | good=ok, controls=7/7 | selftest: 5/50 fail (CTL7-pin-tamper-tables-and-pin, tables-trailing-newline, tables-absent, ...) | MEDIUM. tables_sha is emitted as collateral by CTL-7 but no control requires it; harness 7/7 with the leg deleted. Selftest only (5 cases). |
| m12 | `m12-anchor-flip.py` | anchor comparison inverted | `if cells[3] != "%s:%d"` -> `if cells[3] == "%s:%d"` | good=bad, controls=1/7 | harness: C1-CTL-2, C1-CTL-3, C1-CTL-4, C1-CTL-5, C1-CTL-6, C1-CTL-7, good; selftest: 40/50 fail (good-tree, good-alt-source-S215-for-K15, CTL2-spliced-quote-K04, ...) | LOW. Good-tree check and all controls fail. |
| m13 | `m13-new_rows-threshold.py` | new_rows threshold off by one (accepts 2/3) | `if new_rows < new_min:` -> `if new_rows < new_min - 1:` | good=ok, controls=7/7 | selftest: 2/50 fail (new-rows-usedby-missing-entry-S379, source-candidate-status-S380) | MEDIUM. Threshold off-by-one (accepts 2/3) is only seen by selftest (new-rows-usedby-missing-entry-S379 expects new_rows=2/3). |
| m14 | `m14-exit-code-flip.py` | exit status inverted | `(0 if verdict == "TARGET_MET" else 1)` -> `(1 if verdict == "TARGET_MET" else 0)` | good=bad, controls=0/7 | harness: C1-CTL-1, C1-CTL-2, C1-CTL-3, C1-CTL-4, C1-CTL-5, C1-CTL-6, C1-CTL-7, good; selftest: 46/50 fail (good-tree, good-alt-source-S215-for-K15, CTL1-absent, ...) | LOW. Good-tree exit-status check fails. |
| m15 | `m15-tables-sha-flip.py` | tables_sha leg fires on the match, not the mismatch | `if not sha_ok:` -> `if sha_ok:` | good=bad, controls=7/7 | harness: good; selftest: 46/50 fail (good-tree, good-alt-source-S215-for-K15, CTL1-absent, ...) | LOW. Good-tree check fails. |
| m16 | `m16-source-commit-dropped.py` | source_ok no longer requires the frozen commit in the URL | `if pin.startswith("Hyprland-") and c["commit"] not in url:` -> `if False and c["commit"] not in url:` | good=ok, controls=7/7 | NOTHING | HIGH. Commit clause of source_ok unguarded by selftest and harness. Verdict-level: TARGET_MET on a tree whose three K13-K15 sources cite a Hyprland URL at another commit (demo A). |
| m17 | `m17-source-status-dropped.py` | source_ok no longer requires status mined | `if cells[7] != "mined" or not url.endswith("/" + c["source_suffix"][pin]):` -> `if not url.endswith("/" + c["source_suffix"][pin]):` | good=ok, controls=7/7 | selftest: 1/50 fail (source-candidate-status-S380) | MEDIUM. status clause guarded only by selftest (source-candidate-status-S380). |
| m18 | `m18-source-suffix-dropped.py` | source_ok no longer requires URL suffix = pin source_suffix | `not url.endswith("/" + c["source_suffix"][pin])` -> `not url` | good=ok, controls=6/7 | harness: C1-CTL-4; selftest: 1/50 fail (CTL4-wrong-source-K10) | LOW. Suffix clause exercised by CTL-4 and selftest. |
| m19 | `m19-prop-strip-dropped.py` | proposition leading/trailing whitespace accepted | `or prop != prop.strip() ` -> `` | good=ok, controls=7/7 | NOTHING | HIGH. Proposition whitespace rule unguarded. Verdict-level: TARGET_MET where the original reports row:K01 (demo B). |
| m20 | `m20-id-cell-check-dropped.py` | id cell compared to rid no longer checked | `if (cells[0] != rid or not prop` -> `if (not prop` | good=ok, controls=7/7 | NOTHING | HIGH. Id-cell check unguarded. Verdict-level: TARGET_MET where the original reports row:K07 (demo C). |
| m21 | `m21-new-row-opened-dropped.py` | new_rows ignores the opened date | `cells[8] != c["opened"] or ` -> `` | good=ok, controls=7/7 | NOTHING | HIGH. `opened` date of new rows unguarded. Verdict-level: TARGET_MET where the original reports new_rows=2/3 (demo D). |
| m22 | `m22-new-row-tier-dropped.py` | new_rows accepts any tier | `cells[3] != "A" or ` -> `` | good=ok, controls=7/7 | NOTHING | HIGH. Tier-A rule of new rows unguarded. Verdict-level: TARGET_MET where the original reports new_rows=2/3 (demo E). |
| m23 | `m23-new-row-usedby-dropped.py` | new_rows ignores used-by naming the entry | `if c["entry"] not in cells[10]:` -> `if False:` | good=ok, controls=7/7 | selftest: 1/50 fail (new-rows-usedby-missing-entry-S379) | MEDIUM. used-by naming the entry is guarded only by selftest (new-rows-usedby-missing-entry-S379). |
| m24 | `m24-pipe-check-cells3.py` | a pipe inside the anchor cell is no longer a row-grammar failure | `for x in cells[:4]` -> `for x in cells[:3]` | good=ok, controls=7/7 | NOTHING | LOW-MEDIUM. Leg identity only: a `\|` inside the anchor cell gives anchor:K01 instead of row:K01 (demo F); verdict unchanged. |
| m25 | `m25-pin-line-bound.py` | pin_line: last line of a pin unreachable | `return lines[n - 1] if n <= len(lines) else None` -> `return lines[n - 1] if n < len(lines) else None` | good=ok, controls=7/7 | NOTHING | LOW. Mutant is stricter, not admissive: a quote on the final line of a pin (no trailing LF) is reported missed. No frozen row points at the last line, so the current verdict is unaffected (unit probe). |
| m26 | `m26-quote-substring-dropped.py` | quote:<id> ignores the frozen quote's presence in the pin line | `or pl is None or fr["quote"] not in pl:` -> `or pl is None:` | good=ok, controls=7/7 | NOTHING | MEDIUM. Leg identity: the substring clause of quote:<id> is unguarded. With a pin line edited, the mutant drops quote:K01 and keeps pin_hash (demo G); verdict unchanged. |
| m27 | `m27-html-comment-ignored.py` | rows inside HTML comments are visible | `if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:` -> `if False:` | good=ok, controls=7/7 | selftest: 1/50 fail (row-only-inside-html-comment-K13) | MEDIUM. HTML-comment exclusion guarded only by selftest. |
| m28 | `m28-fence-ignored.py` | rows inside fenced code are visible | `fence = m.group(1)` -> `pass` | good=ok, controls=7/7 | selftest: 1/50 fail (row-only-inside-code-fence-K12) | MEDIUM. Fence exclusion guarded only by selftest. |
| m29 | `m29-verified-at-prefix.py` | provenance accepts any verified-at date | `ver = any(ln == "verified-at: 2026-10-28" for ln in head)` -> `ver = any(ln.startswith("verified-at:") for ln in head)` | good=ok, controls=7/7 | selftest: 2/50 fail (provenance-wrong-date, CRLF-whole-entry) | MEDIUM-LOW. verified-at date guarded only by selftest (provenance-wrong-date). |
| m30 | `m30-source-sid-in-line.py` | provenance source line need not cite an S-id | `src = any(ln.startswith("source:") and S_IN_LINE.search(ln) for ln in head)` -> `src = any(ln.startswith("source:") for ln in head)` | good=ok, controls=7/7 | selftest: 1/50 fail (provenance-no-S-id-in-source) | LOW-MEDIUM. source-line S-id requirement guarded only by selftest. |
| m31 | `m31-index-lt1.py` | duplicate README index rows accepted | `if n_idx != 1:` -> `if n_idx < 1:` | good=ok, controls=7/7 | selftest: 1/50 fail (index-row-duplicated) | LOW-MEDIUM. Duplicate README index row guarded only by selftest. |
| m32 | `m32-backslash-pipe-check-dropped.py` | a backslash-escaped pipe no longer makes the row malformed (equivalent under the other checks, run for completeness) | `if "\\\|" in line:` -> `if False:` | good=ok, controls=7/7 | NOTHING | LOW. Leg identity only (inference from the code, confirmed by demo H): `\\|` in the quote cell gives quote:K05 instead of row:K05; verdict unchanged. Selftest and harness pass. |

## Survivors: the unguarded behaviour and the smallest kill test (text only)

Each proposal is a single-edit tree (or unit call) that the unchanged counter answers as shown in the demonstration named; a frozen control of this shape would kill the mutant.

- **m16 `source-commit-dropped`** — `source_ok` no longer requires the frozen commit in a Hyprland-pin URL. Unguarded: "registry URL … contains the frozen commit" (registration §C1, v2 E2). Test: in the good tree change only the URL token of the S318 registry row from `efb50993…` to `0000…`; expect `missed=source_cell:K13,source_cell:K14,source_cell:K15` (demo A). Selftest variant (not run): wrong commit for S316 → `source_cell:K01`…`K07`.
- **m19 `prop-strip-dropped`** — proposition cell with a leading space accepted. Test: K01 row `| K01 | applyConfig…` → `| K01 |  applyConfig…`; expect `missed=row:K01` (demo B).
- **m20 `id-cell-check-dropped`** — id cell `" K07"` (double space after the first pipe) accepted. Test: K07 row `| K07 |` → `|  K07 |`; expect `missed=row:K07` (demo C).
- **m21 `new-row-opened-dropped`** — registry rows with an `opened` date other than 2026-10-28 counted. Test: S379 row `opened` 2026-10-28 → 2026-10-26; expect `new_rows=2/3 missed=new_rows` (demo D).
- **m22 `new-row-tier-dropped`** — tier-B rows counted. Test: S379 row tier `A` → `B`; expect `new_rows=2/3 missed=new_rows` (demo E).
- **m24 `pipe-check-cells3`** — a `|` inside the anchor cell no longer makes the row malformed, so the leg becomes `anchor:K01` instead of `row:K01`. Test: K01 anchor `Hyprland-InputManager.cpp:1220` → `Hyprland-InputManager.cpp:1220|x`; expect `missed=row:K01` (demo F).
- **m25 `pin-line-bound`** — `pin_line` makes the final line of a pin unreachable (`n < len(lines)`). The mutant only rejects, never admits; no frozen row sits on a last line. Unit test: `pin_line(b"line one\nline two", 2) == "line two"` (run in scratch with `importlib`, the counter's `__main__` guard keeps import side-effect free; the shipped `pin_line` returns `line two`, the mutant returns `None`; this unit output is not in `receipts/`, the probe is reproducible from the mutant file alone).
- **m26 `quote-substring-dropped`** — the `quote:<id>` clause "frozen quote is a substring of that pin line" is unguarded because CTL-7 changes the pin by appending a space, not by editing a quoted line. Test (C1-CTL-7b): in the pin `Hyprland-InputManager.cpp` change one character of line 1220 inside the K01 quote (`repeat_rate` → `repeat_rat3`) and leave `frozen-tables-v2.json` as is; expect `missed=pin_hash,quote:K01` (demo G).
- **m32 `backslash-pipe-check-dropped`** — the escape check of `split_row` is not needed to reject a `\|` in cells 0–3, but a `\|` inside the quote cell gives `quote:<id>` instead of `row:<id>`. Test: K05 quote `` `std::max(0, REPEATDELAY);` `` → `` `std::max(0, REPEATDELAY)\|;` ``; expect `missed=row:K05` (demo H).

## Legs with and without frozen harness controls

Source: `r55_ctl_c1.py` CONTROLS (C1-CTL-1…7) and the controls' own mutations; `m<nn>` columns are the mutants that show the leg is or is not guarded.

| leg | harness control(s) that require it | not covered by any harness control | selftest cases that fail when this leg is dropped (mutant) |
|---|---|---|---|
| `entry_absent` | C1-CTL-1 | — | 3 (m01) |
| `provenance` | **none** | all three trio clauses (recheck, source S-id, verified-at) | 4 (m02) |
| `index` | **none** | README row count (missing, duplicated) | 3 (m03) |
| `row:<id>` | C1-CTL-5 (K17 only) | H rows, cell grammar, duplicate ids, fences, comments, CRLF, trailing spaces; m19/m20/m24/m32 | 14 (m04) |
| `anchor:<id>` | C1-CTL-3 (K01 only) | any other row (K08 selftest only) | 2 (m05) |
| `quote:<id>` | C1-CTL-2 (K04), C1-CTL-6 (H02, collateral) | substring clause (m26), backtick style outside K05/H06, K-rows other than K04/K18 | 7 |
| `pin_hash` | C1-CTL-7 | other pins (selftest appends one space in other files) | 4 (m07) |
| `source_cell:<id>` | C1-CTL-4 (K10 S-id) | commit clause (m16), status only via selftest (m17), duplicate registry rows (`len(rows) != 1` unexercised) | 4 (m08) |
| `new_rows` | **none** — none of the 7 controls changes a registry row that counts toward new_rows | tier, opened, commit, used-by (selftest only), threshold (m13, selftest only) | 3 (m09) |
| `host:<id>` | C1-CTL-6 (H02 only) | H01, H03–H06 | 2 (m10) |
| `tables_sha` | **none required** — C1-CTL-7 emits it as collateral but the harness does not require it; harness 7/7 with the leg deleted (m11) | — | 5 (m11) |

The harness requires the named leg to appear; it does not require the set to be exact. Over-reporting is rejected only by the good-tree check (`missed=none`) and by the `owned` rule (a control may not name a row its mutation did not touch, and `entry_absent` must not appear on an existing entry).

## Demonstrations on the real tree (unchanged counter as the parser-compatible control)

Each row: the scored tree with one edit, committed in the scratch repo (`receipts/demo/index.json`, repos removed before yield). "orig" = the shipped counter, "mutant" = the named mutant. Raw output: `receipts/demo/results.txt`.

| demo | edit to the scored tree | orig (shipped counter), rc | mutant, rc |
|---|---|---|---|
| A (m16) | SOURCES S318 row, URL token `efb50993…/src/config/values/ConfigValues.cpp` → `0000…/…` | `sources=15/18 … verdict=TARGET_MISSED missed=source_cell:K13,source_cell:K14,source_cell:K15`, 1 | `sources=18/18 … verdict=TARGET_MET missed=none`, 0 |
| B (m19) | K01 row `\| K01 \| applyConfig…` → `\| K01 \|  applyConfig…` | `rows=17/18 … missed=row:K01`, 1 | `rows=18/18 … TARGET_MET missed=none`, 0 |
| C (m20) | K07 row `\| K07 \|` → `\|  K07 \|` | `rows=17/18 … missed=row:K07`, 1 | `rows=18/18 … TARGET_MET missed=none`, 0 |
| D (m21) | SOURCES S379 row `opened` 2026-10-28 → 2026-10-26 | `new_rows=2/3 … missed=new_rows`, 1 | `new_rows=3/3 … TARGET_MET missed=none`, 0 |
| E (m22) | SOURCES S379 row tier `A` → `B` | `new_rows=2/3 … missed=new_rows`, 1 | `new_rows=3/3 … TARGET_MET missed=none`, 0 |
| F (m24) | K01 anchor `Hyprland-InputManager.cpp:1220` → `…:1220\|x` | `rows=17/18 … missed=row:K01`, 1 | `rows=17/18 … missed=anchor:K01`, 1 |
| G (m26) | pin `Hyprland-InputManager.cpp` line 1220: `"repeat_rate"` → `"repeat_rat3"` (pin only) | `missed=quote:K01,pin_hash`, 1 | `missed=pin_hash`, 1 |
| H (m32) | K05 quote `` `std::max(0, REPEATDELAY);` `` → `` `std::max(0, REPEATDELAY)\|;` `` | `rows=17/18 … missed=row:K05`, 1 | `rows=17/18 … missed=quote:K05`, 1 |
| unit (m25) | `pin_line(b"line one\nline two", 2)` | `'line two'` | `None` |

Demonstrations B, C, F and H are inputs the frozen grammar rejects; the shipped counter rejects them with `row:<id>`, which is the expected answer. They falsify the *mutants*, not the shipped instrument. Demonstrations A, D and E are semantic defects (foreign commit, out-of-window `opened`, tier B); the shipped counter flags them and the mutants do not. None of these demonstrations shows a defect in the shipped counter.

## Limits (declared)

- 32 one-edit mutants, not an exhaustive set. Not mutated: `valid_shape`, the `count_new_rows` loop, `FENCE`, `PROV_WINDOW`, the harness and its 7 controls (out of scope for this seat).
- The mutation is on the counter only. Every mutant was run against the same unmodified harness controls and the same frozen tables.
- The "killed by selftest" column relies on the counter's synthetic selftest; a survivor of the harness alone is not a survivor of the instrument's own checks, and conversely a selftest kill is not independent evidence.
- Demonstrations A–H use scratch commits built from the scored bytes plus one edit; no change was written to the lane.
- Not verified: whether any of the proposed kill tests are worth adding to the frozen harness. That is a decision for the L1; this seat only reports the gap.
