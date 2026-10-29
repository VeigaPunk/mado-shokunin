# R56ScribeSourcesA — report (round 56, wave w1, claim C1 source rows)

Scope: draft registry rows S383–S390 for `corpus/SOURCES.md`, the source gate, and a shape check of those rows on a registry copy. No lane file was edited; the rows are NOT yet in the lane registry (integration is the integrator's step).

## Deliverables

- `.ufo/waves/round-56/w1/R56ScribeSourcesA/rows.md` — 8 rows, one per line, 11 cells each (`| S383 | … | S390 |`), status `mined`, opened `2026-10-28`, recheck `on-release` (S390 `90d`), used-by exactly `corpus/knowledge/hyprland-config-autoreload-r56.md`.
- `.ufo/waves/round-56/w1/R56ScribeSourcesA/gate.md` — per row: URL, access date 2026-10-28, located quote (≤25 words) with pin line number.
- Receipts (copied from scratch before cleanup):
  - `validate-real-lane-3423ae28.out` — validate on a full lane-commit tree with the rows inserted (rc 1, see below).
  - `validate-scratch-standin-entry.out` — same tree plus a scratch-only stand-in for the entry (rc 0).
  - `validate-copy-only-root-artifact.out` — validate on a copy containing only `corpus/SOURCES.md` (artifact of the `--file` root rule, see defect D2).
- `.ufo/waves/round-56/w1/R56ScribeSourcesA.md` — this report.

## What was done

1. Read `registration.md` §C1 (row grammar, `source_cell`, `scope`, `new_rows` legs), `frozen-tables.json` (`c1.k`, `c1.h`, `pin_sha256`, `pin_suffix`, `rev_rule`, `rows`), and registry rows S364–S369 (style), and `scripts/sources-census.sh` validate code (`row_pass`, `usedby_findings`).
2. Verified pins against the tables (python3 -I, read-only over `fetch/`): all 8 pin sha256 equal the table; all 30 K quotes are substrings of the frozen line in its pin (`bad 0`); sizes: ConfigWatcher 4046, ConfigValues 59222, PropRefresher 5139, EventLoopManager 9073, legacy ConfigManager 90963, MiscFunctions 29785, HyprCtl 97582, man7 44066 bytes.
3. Computed scope locators per pin from `c1.k` (merged per-row lines):
   - S383 ConfigWatcher.cpp: `33-34,46,54-56,60,67,69,105` (K03–K12)
   - S384 ConfigValues.cpp: `492` (K01–K02)
   - S385 PropRefresher.cpp: `148-149` (K15–K16)
   - S386 EventLoopManager.cpp: `71,128` (K13–K14)
   - S387 legacy ConfigManager.cpp: `776,1070,1079-1080,1816,1835-1836,1844` (K17–K24)
   - S388 MiscFunctions.cpp: `65,68` (K25–K26)
   - S389 HyprCtl.cpp: `1223,1276` (K27–K28)
   - S390 inotify.7.html: `186,262` (K29–K30)
4. Wrote rows; a python check on `rows.md` (outside the registry) confirmed: 11 cells each; no backslash; URL = `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<suffix>` (S390 man7 URL); every K row line covered by a locator; anchor carries the pin byte size and sha256 and `.ufo/waves/round-56/fetch/<pin>`; status/opened/used-by fields as specified. Output: `ALL OK`.
5. Gate: opened each pin's cited lines with `read` and copied quotes into `gate.md`; a script confirmed each quote is a substring of the stated line and ≤25 words (13 quote/line pairs, all OK).
6. Shape check: built a lane-commit tree in scratch (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 3423ae285676c2a10273000f4519163472b443db | tar -x -C <scratch>/tree`, read-only git), inserted the rows after the last Registry table row (S382, line 332) of `corpus/SOURCES.md` (593 → 601 lines), and ran validate.

## Commands and decisive output

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/tree/corpus/SOURCES.md --today 2026-10-29
rc=1
file  E11  S383 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
file  E11  S384 … S390 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md   (8 E11 total, one per new row)
file  W01  S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md        (pre-existing)
file  W04  S384 / S387 / S388 / S389 duplicate url … across scopes                         (new rows; 32 W04 total incl. pre-existing)
```
No E01–E10, E12 finding; no E04 (no URL+scope collision); no E01 (all rows NF=13).

With a scratch-only stand-in file at `corpus/knowledge/hyprland-config-autoreload-r56.md` (so the used-by path resolves; this is NOT the entry):

```
$ … validate --file <scratch>/tree/corpus/SOURCES.md --today 2026-10-29
rc=0      E-count: 0      W04 total: 32      W01: S277 (pre-existing)
```

Census of the same tree: `rows 327, tier.A 315, tier.B 5, tier.C 7, status.mined 306`.

**Result: the registry-shape check exits 1 on the lane's current state, solely because the entry `corpus/knowledge/hyprland-config-autoreload-r56.md` does not yet exist at 3423ae2 (E11 ×8). It exits 0 once the entry exists. The task asked for exit 0; I did not create the entry (it is another seat's output) and I did not fake it in the lane.**

## Findings and defects

- **D1 (blocking for exit 0, not a row defect):** validate E11 requires the used-by path to exist under the registry's root. The entry is absent at the lane's frozen commit. The rows are correct; E11 clears when the entry lands. Integrator must run validate after the entry is written.
- **D2 (census tool, `--file` mode):** `resolve_targets` sets the root to `dirname(FILE)/..`. A registry copy alone (`<scratch>/corpus/SOURCES.md`) produced 365 spurious E11 (every used-by path missing), receipt `validate-copy-only-root-artifact.out`. A full tree is required for a meaningful E11 check. The task's literal command (`--file <scratch copy>`) therefore only means something when the scratch copy sits inside a full tree.
- **D3 (W04 warnings on new rows, not failures):** the new rows reuse URLs already registered under different scopes:
  - S384 ↔ S215, S318 (ConfigValues.cpp)
  - S387 ↔ S162, S303, S317, S353, S368 (legacy ConfigManager.cpp)
  - S388 ↔ S182, S321 (MiscFunctions.cpp)
  - S389 ↔ S158, S307, S320, S366 (HyprCtl.cpp)
  S383, S385, S386, S390 have no prior URL match. Scopes differ, so no E04. Warnings do not affect exit.
- **D4 (access-date discrepancy):** the spec fixes access date and opened to `2026-10-28`. The system clock reads `2026-10-29` (UTC) during this run; the quotes were re-read from the pins on 2026-10-29. I recorded the spec's date as instructed. The integrator should decide whether the registered date should be the read date.
- **D5 (contract ambiguity, no effect on pass/fail as I read it):** `scope` says "a comma-separated list … contains a range that includes the row's line" and the spec said "one range". I used per-row merged locators (e.g. `33-34,46,54-56,60,67,69,105`), not a single covering span (e.g. `33-105`). Both satisfy the stated leg; the choice is in the rows. Anchor shape (`locators @ <rev>; pin …`) matches existing S352/S364 rows.
- **D6 (contract wording, legacy file):** S387's K rows span lines 776–1844 across the whole legacy ConfigManager; the per-row list keeps the scope narrow. Nothing in the registration contradicts this.
- **D7 (counter reading, informational):** `source_cell` takes the LAST `http(s)://` token of the source cell; `validate` (`url_of`) takes the FIRST. Every new source cell contains exactly one URL, so the two readings agree here.
- **D8 (teaches claim, checked):** S389 "the path that is not full-reset ends by calling Config::mgr()->reload()": pin lines 1276 (`Config::mgr()->reload();`) then 1278 (`return "ok";`), 1279 closes the function. The `full-reset` branch returns `"ok"` earlier, so the reload is reached only on the non-reset path.

No text of `registration.md` §C1 disagreed with the frozen tables for the items used (K/H quotes, pins, rev rule, new_row_ids S383–S390). `claims-frozen.md` was not read in full by this seat.

## Not verified / not run

- The counter `MADO_AUTORELOAD_ENTRY` (C1) was NOT run: the entry does not exist, and running the counter or controls is not in this seat's assignment.
- Entailment of the teaches sentences beyond the quoted lines was checked by reading, not by a sentence-to-pin audit (out of scope for this seat).
- I did not verify that the S383–S390 rows are not already present in other lanes' registries (only the mado lane commit was used).
- Nothing was applied to `corpus/SOURCES.md` in the lane.

## Hygiene

- No hold-out fixture, no sealed path, no hyprctl/compositor action, no ~/.config write, no package install. No tool was installed or upgraded.
- Lane: read-only (`git archive` into scratch, plus `read`). No commit/add/stash/checkout/reset. Scratch `git init` was used only as an empty fixture directory and never committed.
- Scratch `/fast/scratch/hyaku/mado-r56/R56ScribeSourcesA/` removed before yield (receipts copied first).
