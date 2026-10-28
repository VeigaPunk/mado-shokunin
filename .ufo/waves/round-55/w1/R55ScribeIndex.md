# R55ScribeIndex — round 55, wave w1, integration drafts

Seat: `R55ScribeIndex` (leaf scribe; no subagent dispatch). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD `dbc2eefe` (freeze `54dacbd8` is an ancestor). Drafts only: no tracked file in the lane was edited, no git/jj mutation was run, nothing was committed, no host read was made, and no tool was installed.

## 1. What I did

1. Read the frozen contract `claims-frozen.md` and `registration.md` in full, and `corpus/README.md`, `PROVINCE.md` and `quality/tool-ledger.md` for style.
2. Counted index rows (69) and notes on disk (69).
3. Checked the frozen C3 pin (`.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`) against the errata's P19 claim by line (read only).
4. Read peer drafts only to align wording (`R55ScribeEntryA/entry.md` header and scope, `R55ScribeP19a/after.md` P23 block, `R55ScribeEntryA/verify.txt`). Nothing of theirs was edited or copied wholesale.
5. Wrote six draft files and a checker; applied the drafts to a scratch copy of the lane's HEAD tree (via `git archive`, read-only on the lane) and checked them.

## 2. Deliverables (drafts for the L1; not applied)

Directory: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScribeIndex/`

| file | item | what it is |
|---|---|---|
| `01-coverage-row.md` | (1) coverage-map row | one table row for `knowledge/hyprland-keyboard-repeat-numlock-r55.md`, to go after the r52-errata row |
| `02-frontier-bullets.md` | (1) Frontier bullets | "Round 55 moves …" bullet naming what stays open, plus a correction bullet; first under `## Frontier` (newest-first, as r47–r51 are) |
| `03-errata-row.md` | (2) correction line | replaces README line 81 in place; contains `hyprland-synthetic-dispatch-r52-errata-r53.md`, `P23`, `supersedes P19`. Not a second row (check-index requires one row per note) |
| `05-province-round55.md` | (3) PROVINCE | "Round-55 refinement" paragraph in the round-45/46 style; `tools/mado-kbdopts.py` as read-only (reads only `--config`/`--getoption` files, starts no process, writes nothing); four record instruments |
| `06-ledger-rows.md` | (4) ledger | five rows in the `quality/tool-ledger.md` grammar: `tools/mado-kbdopts.py`, `quality/check-freeze-order.py`, `quality/check-r55-controls.py`, `quality/counters/c1-r55-kbd-entry.py`, `quality/counters/c3-r55-p19.py` |
| `verify-drafts.py` | checker | applies the drafts to a copy of HEAD under `--work` and checks them |
| `verify-drafts.txt` | receipt | output of the checker run (below) |
| `receipts.txt` | receipt | counts, ancestry, status, pin lines, checker output |

Index row count (requested): `grep -c '^| \`knowledge/' corpus/README.md` → **69**; `ls corpus/knowledge/*.md | wc -l` → **69**. After integration the count is **70/70** (the claims' "69/69 → 70/70").

## 3. Commands and decisive output

```
$ grep -c '^| `knowledge/' corpus/README.md
69
$ ls corpus/knowledge/*.md | wc -l
69
$ git -C <lane> rev-parse --show-toplevel        -> /home/vgpnk/Projects/shokunin/mado-shokunin
$ git -C <lane> merge-base --is-ancestor 54dacbd8… HEAD && echo ancestor   -> ancestor
$ git -C <lane> status --porcelain -- quality tools corpus PROVINCE.md
?? quality/check-r55-controls.py                 (pre-existing, not written by this seat)
$ sha256sum .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637   (= frozen c3.pin_sha256)
$ sed -n '1558p;1566p;1568p;1569p' …Hyprland-ConfigActions.cpp
  g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);   # 1558, m_passPressed == 1 arm
  } else {                                                                                   # 1566
  g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);   # 1568, else arm
  g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);  # 1569
```
The pin lines confirm the errata defect: P19's "PRESSED only when `m_passPressed == 1`" is false, because the `else` arm (1566–1569) also sends PRESSED at 1568.

Checker (`verify-drafts.py --lane <lane> --work <scratch>/verify`, rc 0), decisive lines:
```
lane HEAD=dbc2eefee5bb1d2c3f42ce56828b99bd9d81c333
fixture toplevel ok=…/fixture
README base index rows=69
README draft index rows=70 (base 69 + entry row)
notes on disk in HEAD tree=69
rows without file in HEAD tree=['knowledge/hyprland-keyboard-repeat-numlock-r55.md']  (expected: the entry lands with the entry)
files without row=[]
duplicate row targets=none
errata line names file+P23+'supersedes P19': True
DEFECT D1 base README: blank line(s) inside coverage table at line(s) [79] …
PROVINCE paragraph names all five instruments: True
PROVINCE paragraph: 'starts no process' for kbdopts: True
ledger <each of 5 paths>: pointer_exists=True basename_in_pointer=True in_HEAD=False (expected until the instrument lands)
ledger draft rows=5 duplicates_inside_draft=none
VERIFY_DRAFTS: done
```
Scratch was removed by a `trap` after the receipts were copied.

## 4. Defects and ambiguities found (input → what shows it)

- **D1 — README coverage table is broken at line 79.** `corpus/README.md` lines 78 (`hyprland-dispatcher-dispatch-r51.md`) and 80–81 (r52 and r52-errata rows) are separated by a blank line (79). In GitHub-flavoured markdown a blank line ends a table, so the r52 and errata rows render outside the Coverage map table, without a header. The checker confirms it (`DEFECT D1 … line(s) [79]`). Draft 01 is inserted after line 81, so the L1 must also delete line 79 for the new row to sit in the table. Recommended, not applied here.
- **D2 — tool ledger: round-51 rows sit outside the table.** `quality/tool-ledger.md` has a blank line at 111 and 116 and a paragraph at 112–115; the rows at 117–119 (`check-tool-ledger.py`, `c1-r51-ledger.py`, `c2-r51-dispatch-entry.py`) are a second, header-less block. Draft 06 appends the five round-55 rows contiguously after line 119 with no blank line, matching that block, but the L1 should decide whether to fold both blocks under the single header. Whether `check-tool-ledger.py` parses the second block is not verified (the checker is not in the lane at HEAD).
- **D3 — the round-55 control harness cannot run as committed.** `quality/check-r55-controls.py` is untracked (`??` in `git status`) and is a dispatcher: its header and code import `r55_ctl_c1`, `r55_ctl_c2`, `r55_ctl_c3` from `quality/`. None of those modules exists (tracked or on disk: `ls quality/ | grep r55_ctl` → nothing). Consequence: `--claim c1|c2|c3` would fail at import; the `MADO_R55_CONTROLS` and `MADO_R55_C2` lines cannot be produced from this tree. Also the dispatcher's `--counter PATH` and `--holdout DIR` options are not in the frozen registration (the registration names `--work` and `--rev` only); the registration should be checked against the dispatcher by the L1. I did not open the hold-out directory.
- **D4 — no counter, tool or freeze gate exists yet.** `tools/mado-kbdopts.py`, `quality/counters/c1-r55-kbd-entry.py`, `quality/counters/c3-r55-p19.py` and `quality/check-freeze-order.py` are absent at HEAD and on disk; `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` is absent too. Every "TARGET_MET" wording in the drafts is therefore conditional, and the drafts say so. Ledger cell 2 is drafted from the frozen text; the L1 must re-read each instrument's own header at integration (the ledger's rule).
- **D5 — pointer class mismatch for three instruments.** `registration.md` does not name `c1-r55-kbd-entry.py`, `c3-r55-p19.py` or `check-freeze-order.py` (grep: 0 hits for `c1-r55|c3-r55|check-freeze` in `registration.md`); only `claims-frozen.md` names them. Draft 06 points those three rows to `.ufo/waves/round-55/claims-frozen.md`, which passes the basename check but is not the `registration.md` class the ledger documents. Either the freeze's registration text should name them or the ledger grammar should accept claims-frozen.
- **D6 — the existing errata README row is now false.** Its Holds cell says "Corrects only three source-level propositions" (P16–P18). After round 55 that is wrong. Draft 03 replaces the row in place rather than adding a second row (check-index requires exactly one row per note). This is an edit to a row, which the L1 must make; the old text is not preserved as history beyond the errata file itself.
- **D7 — `check-freeze-order.py` has no stated input contract.** The frozen claims name it and its target (round-54 `350d30e4` committer 14:11:10 versus registry `createdAt` 14:05:25) but the registration gives no argument list, input source (git objects or working tree) or verdict grammar. The PROVINCE and ledger text therefore states only what the claims state and marks the input contract unverified.
- **D8 — the errata's escaped-pipe risk (self-found, fixed in the draft).** My first draft used `\|` inside a backticked Holds cell; it was replaced before the check, so no escaped pipe remains in the drafts.

Harm-watch items from the frozen contract that this seat could not run: `bash tools/mado-verify.sh --selftest` (460/460), `scripts/sources-census.sh validate` — not run, not in scope for a scribe seat. The sibling-lane and fleet files were not read.

## 5. Not verified / not run

- No counter, harness, tool or the entry file exists in the lane, so no `MADO_KBD_ENTRY`, `MADO_P19_FIX`, `MADO_R55_CONTROLS` or `MADO_R55_C2` line was produced, and none is claimed here.
- The Holds, Frontier and PROVINCE wording describes the frozen design (registration §C1–C3, claims). It was checked against the peer entry draft's scope section and against the pins for P19, not against the final entry bytes.
- The S-ids cited (S052, S162, S215, S316–S319 held; S378–S380 new) were taken from the frozen registration and `R55ScribeEntryA/entry.md`; I did not open `SOURCES.md` rows.
- I did not read `/home/vgpnk/.omp/agent/RULES.md`: I installed no tool and no upgrade, so the tooling gate did not apply to this seat. Nothing was installed, updated or removed on the host.
- Host reads: none. I did not run `hyprctl` or read `~/.config/hypr`.
- The `.ufo/waves/round-55/fixtures/c2/` directory was listed (F01–F18, committed); I did not open any fixture, and I did not look for or use `fixtures/c2-holdout`.
- Lane tracked state: `git status` after my work shows only `?? quality/check-r55-controls.py` among tracked paths (pre-existing, not mine) and my untracked deliverables under `.ufo/waves/round-55/w1/`. No commit, stash, checkout or reset was run.

## 6. Verdict of this seat

Drafts 01–06 are ready for the L1 with the following conditions: apply D1 (delete line 79) and D6 (replace the errata row) together with the Frontier and PROVINCE inserts; apply the ledger rows only after each instrument lands and its header is re-read; do not treat any of the round-55 claims as met until the four counters and the harness print their green lines at the final revision. Blocking issues for the L1 are D3 (harness modules missing) and D4 (instruments absent).
