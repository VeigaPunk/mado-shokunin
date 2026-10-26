# ScrToolLedger — round 47 / w1 — the lane's live-state tool ledger

**Seat outcome:** delivered. The ledger of the lane's `tools/` instruments (question, inputs, last
live run with receipt + round + commit, verdict there, byte-binding, invocation) is written, with
counts re-derived from committed evidence, a ready-to-paste `corpus/README.md` section, one proposed
QUALITY criterion (91) and a checker shown to fail three ways.

Base: `c24adef2632672325a4eef3e3492f6716ccb6d14`. Every count was produced at that commit; the raw
output is in `w1/ScrToolLedger/receipts/`.

## Artifacts (all under `.ufo/waves/round-47/w1/ScrToolLedger/`)

| path | holds |
|---|---|
| `ledger.md` | the deliverable: §1 live-run definition + lookup rule, §2 the tables (2a host-facing 9, 2b nested-scored 2, 2c artifact gates 3), §3 counts, §4 findings F1–F5, §5 draft README section, §6 proposed criterion 91, §7 limits, §8 machine-readable rows, §9 checker demonstration |
| `check-ledger.py` | the criterion's checker (stdlib, `--repo/--rev/--ledger`, reads `git show` only, writes nothing) |
| `receipts/tools-inventory.txt` | 14 instruments: sha256, line count, mtime, last commit |
| `receipts/live-receipts.txt` | per tool: receipt path, round, `git log -1 --format=%H`, current sha, verdict locators |
| `receipts/absence.txt` | the absence proofs (globals, verify-live, binds/anims/wsrules oracle lines, tripwire scans), receipt-file denominators |
| `receipts/live-receipt-paths.txt` | the 10 live receipts tagged RECEIPTS/ELSEWHERE; subprocess-site counts per tool; nested-harness scratch paths |
| `receipts/locators.txt` | PROVINCE.md input rows + each tool's own usage/argument lines |
| `receipts/verify-quotes.txt` | 20 quoted fragments re-grepped at their source lines: `QUOTES total=20 missing=0` |
| `receipts/check-ledger.txt` | checker on pristine ledger (exit 0) and on three doctored copies (exit 1 each), plus the `--rev` read |

Final deliverable digest: `ledger.md` sha256 `91ec6bcb9119925bfa80b241b3fdeb4972c1b421a818be928f1579614d0376b6`
(298 lines) at the time `receipts/check-ledger.txt` was produced.

## Behaviour (what was done)

1. Read the 14 docstrings (`tools/mado-*.py`, `tools/mado-verify.sh`) and the `PROVINCE.md:20-32`
   input rows for question + inputs + invocation.
2. Searched **all** committed lane evidence for a live execution of each tool, not only
   `.ufo/waves/*/receipts`: verdict tokens, `live=`, `tool=… sha256:`, `*/receipts/live-*`, plus a
   per-tool `grep -rn` over `.ufo/waves`, `.ufo/evidence`, `corpus/`.
3. Bound each receipt with `git log -1 --format=%H -- <receipt>` and compared the receipt's recorded
   tool sha256 with `sha256sum tools/<tool>` — the column the lane's `PROVINCE.md` and `SKILL.md`
   both lack.
4. Wrote the ledger, the README section, criterion 91 and `check-ledger.py`; demonstrated the
   checker on three doctored copies (declared-status lie, deleted row, wrong receipt).

## Counts (the answer the brief asked for)

- 14 tracked instruments: 13 `mado-*.py` + `mado-verify.sh`.
- 9 read host state; **8 have a committed live receipt**, **1 (`mado-globals.py`) has none**.
- **3 live receipts predate the current bytes**: `mado-verify.sh` (live r12, `ea798ad0…` → now
  `050efc72…`), `mado-tripwire.py` (live r19, `367be947…` → `cd9da20c…`), `mado-binds.py` (live r25,
  `9efa1136…` → `0cda0e6f…`).
- 5 host-facing receipts are bound to the current bytes: eventq r38, options r40, geometry r44,
  monitors r45, devices r46.
- 2 config resolvers were scored only by a nested Hyprland (`anims` r26, `wsrules` r27), whose harness
  scratch no longer exists.
- 3 are artifact gates with no host input by design (`action-plan`, `assessment`, `evidence-audit`).

## Findings

- **F1** `mado-globals.py` has no receipted live run; its entry rests on a captured journal
  (`.ufo/waves/round-41/fetch/xdph-journal.txt`, `bf8fa91a…`). Cheapest closure is one hermetic
  `--journal-file` run over that committed capture, receipted with the tool hash.
- **F2** the brief's lookup rule (`git grep` over `.ufo/waves/*/receipts`) finds **4 of 10** live
  receipts; the other 6 sit in `evidence/`, `fetch/`, `.ufo/evidence/`.
- **F3** three live receipts no longer describe the bytes on disk; `mado-verify.sh` is the worst
  (the lane's standing gate, last live verdict 35 rounds old, while its `CLEAN` line claims
  "file + live planes").
- **F4** the nested-compositor harness named by the r25/r26/r27 counters
  (`/fast/scratch/hyaku/mado-r26/wlroots/build`, `…/mado-r2*-oracle-slots`) is absent, so
  `knowledge/workspace-rules-r27.md`'s offered recheck command cannot run before it measures.
- **F5** positive: no instrument reads beyond its `PROVINCE.md` row; spawn sites counted and read
  (eventq 8, globals 6, options 7, tripwire 20 all in selftest child path, the three joins 0).

## Gates and safety

- No host probe, no compositor read, no process launched beyond `grep/git/find/sha256sum/python3`
  over lane files. `hyprctl`, `xdg-terminal-exec`, `ss`, `journalctl` were **not** run.
- No pacman, no package transaction, no tool install — nothing to record under the tooling directive.
- Write scope respected: only `.ufo/waves/round-47/w1/ScrToolLedger/` (deliverables) and this report.
  `corpus/README.md`, `corpus/QUALITY.md`, `PROVINCE.md`, `SKILL.md` are **not** edited; the README
  section and criterion 91 are drafts for the L1 integrator. No git/jj mutation.
- Session material kept shape-only: device **names** from the devices receipt are not reproduced;
  only its verdict line is. No window titles, serials, process tables or home listings.
- Scratch `/fast/scratch/hyaku/mado-r47/ScrToolLedger/` (three doctored ledger copies) deleted.

## Out of scope (named, not done)

- Landing the README section and criterion 91 in `corpus/README.md` / `corpus/QUALITY.md` (L1 only).
- Producing the missing live receipts (globals over the captured journal; a live `mado-verify.sh`;
  a current-byte tripwire session scan; a binds re-score) — these are re-run tasks the ledger names,
  and a live `verify` run would be a host probe this seat is not cleared to make.
- Rebuilding the nested-Hyprland harness to re-score `anims`/`wsrules`/`binds`.

## Known limits of the deliverable

- "Live" is judged from receipt text plus tool hash; a receipt that misstated its own mode would be
  recorded as live. Nothing was re-run to check.
- The receipt-file denominators (1515 files / 89 `receipts/` dirs at 2026-10-26T18:48-03:00) move
  during the wave; the set of named live receipts is stable, the denominators are dated.
- `check-ledger.py` proves the ledger is consistent with the receipts, not that the receipts are
  true (criterion 25's boundary); it is a seat instrument, not credit.
