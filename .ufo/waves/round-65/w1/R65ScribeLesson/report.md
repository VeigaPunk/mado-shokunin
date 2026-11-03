# R65ScribeLesson — report

Seat: mado round 65, wave w1, scribe (lesson draft). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`524fa1f90b1f2de44b3019bacf833d54e0af13a0`, frozen declaration head
`cb63ab13ccaf85191318701d5db5ace050bd5bd4`. Date 2026-11-03. Host: omarchy
Linux, live Hyprland 0.56.2 (read-only). Leaf seat: no agents spawned, no
installs, no pacman, no mutating git, no config/session writes, no r56-era
material opened, no credential-shaped capture.

## Deliverable

`.ufo/waves/round-65/w1/R65ScribeLesson/round-65.md` — draft lesson: header +
`## Mistakes` (2 mined, 2 examined-and-dropped with reasons) + `## Gate`
(S028/S097 re-open blocks, quotes marked FILL-FROM-SCOUT) + `## Assimilation`
and `## Considerthese` as FILL-BY-L1 placeholders. Nothing written to
`corpus/**`.

Also in the seat dir: `scribe-evidence.txt` (this seat's receipt, every
producer's own rc) and `evidence.sh` (the script that produced it, so the
receipt is re-runnable).

## What I ran (all read-only; full output + rc in `scribe-evidence.txt`)

| Command | Output | rc |
|---|---|---|
| `git diff-tree -r --numstat 7fe65562 66b8994b \| awk …` | `files=31 added=1193 deleted=1` | 0 |
| `git ls-tree -r --name-only 688144573a26 -- .ufo/waves/round-64/receipts/ \| wc -l` | `19` | 0 |
| `git diff-tree -r --name-only 7fe65562 66b8994b -- .ufo/waves/round-64/receipts/ \| wc -l` | `21` | 0 |
| `grep -n '18 round-64 receipt files\|30 files, +1192' /fleet/.ufo/reports/round-64/mado.md` | lines 87 and 93 carry the drifts | 0 |
| `python3 quality/check-tool-ledger.py --selftest --scratch-root <S>/st-ledger` | `LEDGER_SELFTEST: 54/54 passed` | 0 |
| `python3 quality/check-wave-done.py --selftest --scratch-root <S>/st-wave` | `MADO_WAVE_DONE_SELFTEST: 62/62 passed` | 0 |
| `grep -n SELFTEST_CHECKS quality/check-tool-ledger.py` / `check-wave-done.py` | `55 if os.name == "nt" else 54` (:76) / `63 … else 62` (:167) | 0 |
| `grep -cE '^\| .* \| (absent\|observed) \(2026-10-31\) \|' PROVINCE.md` | `8` register rows | 0 |
| `grep -c 'absent (2026-10-31)' PROVINCE.md` | `7` | 0 |
| `hyprctl version` | `Hyprland 0.56.2 … commit efb50993…` | 0 |
| `walker --version` | `2.17.2` | 0 |
| `omarchy version` | `3.8.3` | 0 |
| `omarchy --version` | `Unknown Omarchy command: omarchy --version` | **127** |
| `command -v pwsh` / `powershell.exe` / `powershell` | nothing | 1 / 1 / 1 |
| `python3 tools/mado-win-desk.py` | `MADO_WINDESK: ERROR (stage=spawn detail=interpreter not found: powershell.exe)` | **2** |
| `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | `371` | 0 |
| `grep -E '^\| *S097 *\|' corpus/SOURCES.md \| awk -F'\|' '{print $9" \| "$10}'` | `mined | 2026-10-20` | 0 |
| `grep -c W04` / `grep -c W01` on `census-start-r65.txt` | `36` / `1` (same set as r64) | 0 |

### In-flight defect I caught in my own measurement (disclosed, not committed anywhere)

`omarchy --version | head -3` and `python3 tools/mado-win-desk.py | head -5`
both **printed `rc=0`** when I read `$?` after the pipe — the tail's rc, not
the producer's. Re-run as `out=$(cmd); rc=$?` the true rcs are **127** and
**2**. Nothing wrong reached any committed byte: the first reading was
corrected before it was written down, and the corrected values are what the
draft cites. It is recorded here because it is a live demonstration of the
class M65-2 mines, and because the r64 Addendum disclosed the same mechanism
in a landing receipt (`LEDGER_LANDING_RC=0` was `tail`'s rc).

## What I mined and why

- **M65-1 — r64's two report-prose number drifts, mined as the recurrence of
  the M62-1 number-shape class at the report layer.** Real: measured 31
  files/+1193/−1 vs prose 30/+1192, and 19 receipt files at the r64 landing vs
  prose 18. Not already mined: `round-64.md`'s `## Mistakes` (M64-1, M64-2)
  and Addendum cover the write defects and the ledger glue only, and a grep of
  the lesson for those figures returns nothing. The new element named in the
  draft is the detection channel — the report is the one record no counter
  reads — plus the rev-under-determination (`21` across the range, `19` at the
  landing).
- **M65-2 — this round's own register-probe receipt records two version values
  with no producer, in a shape that is not re-derivable.** Real: the receipt's
  `== versions` block prints bare `2.17.2` and `3.8.3` with no `cmd:`/rc
  (attributable only by guessing: `walker --version`, `omarchy version`), and
  the guess space includes an invocation (`omarchy --version`) that fails with
  a diagnostic but whose piped rc reads 0. Class `measurement`; fix shape in
  the draft (producer rc captured off a pipeline; `cmd:` on every value line).

## What I left (and why)

- **m2 (substrate whiplash) — dropped, not mined.** The r57 register did carry
  the re-derive-on-return probe column, a dated state cell on all 8 rows, and
  the explicit "nothing in it is claimed about this host" scope sentence; the
  round's own probe receipt re-ran those shapes (7/8 flipped PRESENT) and the
  8th is unobservable here, which C1's kill rule anticipates. Mining it would
  have invented a mistake. I kept one *watch item* (not a defect): the landing
  block's eighth row needs the `mado-win-desk.py` probe line beside its state
  cell, because the committed probe receipt stops after the 7 Linux groups.
- **m3 (selftest 54/54 + 62/62 vs r64's 55/55 + 63/63) — dropped, not mined.**
  Both checkers pin a host-conditional total (`55 if os.name == "nt" else 54`;
  `63 … else 62`) for the r59 case-variation pin, which exists only where
  `os.path.normcase` folds. Both bundles are green on their own host; not a
  drift and not cross-comparable. Stated precisely in the draft so the next
  scribe does not re-investigate.
- **Gate quotes — left as `FILL-FROM-SCOUT`** per the seat spec; I did not
  fetch, so no quote is invented. I supplied the *host-side* anchors I did
  measure (Hyprland build == tag commit prefix; omarchy `version` 3.8.3 vs
  checkout HEAD == v3.8.4 tag, the split S097 already records) so the L1 can
  land the re-open without re-deriving the host facts.
- **Assimilation and Considerthese — placeholders**, FILL-BY-L1.
- **Claim outcomes, census end, landing numbers — not mine**, not written.

## Findings for the L1

1. The currency rubric's formula counts *dated* rows, not host-true rows
   (`SCORECARD.md:2962`), so the seven stale ABSENT rows still satisfy its
   letter. C1's block repays host-truth; the arithmetic never moved. Worth one
   sentence in the integrated lesson so the rubric re-derivation is not read as
   a score change caused by the register.
2. `corpus/lessons/round-65.md` does not exist yet; the draft is in the seat
   dir only, as required.
3. The Report trailer path (`.ufo/waves/round-65/w1/R65ScribeLesson.md`) is
   outside the seat dir; written as an identical copy of this report because
   the seat spec names that path explicitly. No other file outside the seat dir
   was written.
4. `S028`'s recheck cell is `2026-10-19` and `S097`'s is `2026-10-20` (measured
   from `corpus/SOURCES.md`), matching the old→new lines in the draft.
5. Registry row count 371 at base; no row appended, two re-opens only, as the
   draft's explicit zero-row line says.

## Scratch

`/fast/scratch/hyaku/mado-r65/w1/R65ScribeLesson/` — removed before yield
(evidence copied to the seat dir first).
