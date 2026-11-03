# mado round 65 — lesson

Date 2026-11-03. Base `524fa1f90b1f2de44b3019bacf833d54e0af13a0` (the r64
verifier spot-check tip). Host: the omarchy Linux host returned after rounds
57-64 ran on Windows 11 Home build 26200 — a live Hyprland 0.56.2 session
(instance `efb50993…_1793632040_1005787507`) is observable read-only, and the
2026-10-31 host-change register is the record most factually wrong right now
(7 rows dated 2026-10-31 say the omarchy surfaces are ABSENT; all 7 are
PRESENT). Two claims, as frozen in `claims-declaration-r65.md`: **C1
freshness** (the surface-state register re-derived on the returned host) and
**C2 operability** (the landing-counters standing instrument). Claim outcomes
are the L1's to record; this draft mines only mistakes and sources.
author: mado L1 lane (wave w1 scribe draft, L1-integrated).

## Mistakes

- **M65-1 — the r64 report's two summary numbers were published without their
  counting command, and no counter in the round could see them.** This is the
  M62-1 number-shape class (`corpus/lessons/round-62.md`) arriving in the
  **report prose**, which is the one record no gate reads: navigation, used-by,
  ledger and citecheck all read the lane repo; the fleet-root report is outside
  every one of their scopes. Evidence (fleet root
  `.ufo/reports/round-64/mado.md`, read-only): line 93 says “Range numstat
  `7fe65562..66b8994b`: 30 files, +1192/−1”; measured
  `git diff-tree -r --numstat 7fe65562c15d 66b8994b | awk …` → **files=31
  added=1193 deleted=1**, rc=0. Line 87 says `18 round-64 receipt files`;
  `git ls-tree -r --name-only 688144573a26 -- .ufo/waves/round-64/receipts/ |
  wc -l` → **19**, rc=0. Both drifts are status-neutral (no claim, axis or
  pointer moves) and both were left unmined in `round-64.md`, whose `##
  Mistakes` covers only the two write defects and whose Addendum covers the
  ledger glue. Captured-by: the r64 non-author spot-check §8 items 1-2 — i.e.
  by a human-scheduled reviewer, never by an in-round counter. Class
  `measurement` (number-shape); recurrence history: the r61 report's Landed
  changes table (corrected in the round-62 lesson's `## Corrections`), the r62
  round's six drifts (r63's C1), and these two — three sourced rounds in a row
  where an asserted number was not produced by its counting command. Fix
  shape: the report's summary numbers are computed at the landing rev and
  pasted with the command that produced them, and **a count over a directory
  names its rev** — the same r64 receipt directory holds 21 files across
  `base..HEAD` but 19 at the landing commit, so `receipt files` without a rev
  is under-determined as well as mis-counted. Evidence this seat: `scribe-evidence.txt` §m1.

- **M65-2 — outputs captured through a pipeline report the pipeline tail's
  exit status, so failure-shaped probes read as success; and this round's
  register-probe receipt records version values with no producer.** Two layers,
  both measured today.
  First, the receipt: `.ufo/waves/round-65/receipts/before-register-probes-r65.txt`
  `== versions` prints four values in two shapes — two self-labelling
  (`Hyprland 0.56.2 built from branch v0.56.2 at commit efb5099…`,
  `Waybar v0.15.0`) and two bare (**`2.17.2`**, **`3.8.3`**) with no `cmd:`
  line and no rc. Re-derived: `walker --version` → `2.17.2`,
  rc=0; `omarchy version` → `3.8.3`, rc=0. The values are right; the receipt
  just does not say which binary produced them, so a reader has to guess.
  Second, the mechanism that makes the guess dangerous: `omarchy --version`
  prints `Unknown Omarchy command: omarchy --version` and exits **127**, and
  `python3 tools/mado-win-desk.py` prints `MADO_WINDESK: ERROR (stage=spawn
  detail=interpreter not found: powershell.exe)` and exits **2** — yet both
  read `rc=0` when captured as `cmd | head -5` (the tail's rc), which is
  exactly how this seat first measured both of them before re-running with
  `out=$(cmd); rc=$?`. That is the r64 Addendum's disclosed in-receipt
  `LEDGER_LANDING_RC=0` (tail's rc) class, now reproduced on a version probe
  and on a probe whose *failure is the load-bearing fact* (the C1 kill rule's
  unobservable row). Class `measurement` (QUALITY 26 one layer up: a
  producer's rc is evidence only if the rc is the producer's). Captured-by:
  this seat's attempt to attribute each receipt version line back to a
  command. Fix shape: receipt lines carry `cmd:` + value + rc, rc is captured
  from the producer itself (`out=$(cmd); rc=$?`, never after a pipe), and any
  probe whose meaning is a failure carries its diagnostic line beside its rc.
  Evidence this seat: `scribe-evidence.txt` §m65-2.

- **Examined and dropped (m2, substrate whiplash): the record held.** The
  candidate — "host-change records should carry a re-derive-on-return probe
  list" — is already satisfied by the r57 record. Its 2026-10-31 register is
  one row per surface group with an explicit read-only probe column
  (`command -v hyprctl` → not found; `test -d ~/.config/hypr` → missing; …;
  `python tools/mado-win-desk.py` → `MADO_WINDESK: CLEAN …`), a dated state
  cell on every row, and the standing sentence "The omarchy-era text above
  stays as the frozen record of that host; nothing in it is claimed about this
  host." This round's `before-register-probes-r65.txt` re-ran the same probe
  shapes on 2026-11-03: 7 of 8 groups flipped ABSENT → PRESENT, and the 8th
  (windows desktop plane) is unobservable here — `command -v pwsh` rc=1,
  `command -v powershell.exe` rc=1, `python3 tools/mado-win-desk.py` →
  `ERROR (stage=spawn …)` **rc=2**, which is precisely the state C1's kill
  rule says a row may record honestly. No mistake: the round's register work
  is re-derivation, not repair. Watch item, not a defect: the landing block's
  eighth row needs that probe line beside its state cell — the committed r65
  probe receipt stops after the 7 Linux groups and does not record an
  attempted `mado-win-desk.py` run (this seat's probes above supply the
  shape).

- **Examined and dropped (m3, selftest totals 54/54 + 62/62 here vs 55/55 +
  63/63 at r64): a host-conditional pin, not a count regression.** Both
  fail-closed checkers pin the exact case count and branch on the host:
  `SELFTEST_CHECKS = 55 if os.name == "nt" else 54`
  (`quality/check-tool-ledger.py:76`) and `63 if os.name == "nt" else 62`
  (`quality/check-wave-done.py:167`); the extra Windows case is the round-59
  case-variation pin, which exists only where `os.path.normcase` folds and is
  "skipped by construction" on POSIX (both source comments say so).
  Re-measured here: `LEDGER_SELFTEST: 54/54 passed` rc=0 and
  `MADO_WAVE_DONE_SELFTEST: 62/62 passed` rc=0; r64's `55/55` / `63/63`
  (`before-state-r64.txt` lines 42 and 45) are the same suites on the Windows
  branch. Both are green at their own host; the two bundles are not
  cross-comparable, and no defect exists on either side. Recorded so the next
  scribe does not mine it twice.

## Gate

Re-open access date **2026-11-03** (the returned host's first sourced round).
Both rows are re-opened, not appended: registry row count at base
**371 → 371** (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
→ `371`, rc=0, `.ufo/waves/round-65/receipts/before-state-r65.txt`).

### Admitted

| row | URL | access date | located quote (≤25 words) |
|---|---|---|---|
| **S028** (re-opened) | `https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2` | 2026-11-03 | FILL-FROM-SCOUT |
| **S097** (re-opened) | `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml` | 2026-11-03 | FILL-FROM-SCOUT |

Host-side re-derivation measured read-only this round, rc captured
(`scribe-evidence.txt` §Gate):

- **S028** — `hyprctl version` → `Hyprland 0.56.2 built from branch v0.56.2
  at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update
  inputs).`, rc=0. The live gate agrees at the same commit prefix:
  `live.hypr.version PASS Hyprland 0.56.2 efb5099… (pin matches)`
  (`gate-live-r65.txt`), and `live.hypr.configerrors PASS empty`. So the
  registry row's 0.56.2 is the *running* build on this host, not merely the
  tag.
- **S097** — the row already separates the two numbers that a careless re-open
  would conflate: `omarchy version` → `3.8.3`, rc=0 (the gate reads the
  on-disk version file as `3.8.3` too: `omarchy.version.file PASS HELD`),
  while the host checkout's
  HEAD is the **v3.8.4** tag — `omarchy.git.tag PASS HELD: v3.8.4 exactly at
  refs/heads/master`, `omarchy.git.head PASS HELD: 8fcc9d60`
  (`gate-live-r65.txt`). The row's own note says to identify the checkout by
  HEAD/describe, "not by `~/.local/share/omarchy/version`, which still reads
  3.8.3"; `theme.name.read PASS theme.name = 'matte-black'` and the 12-file
  payload byte-identity stand. The re-open therefore contradicts no pin:
  nothing to bump, nothing to errata.

Recheck cells, old → new (append-only; the row cells move, no new row):

- **S028** recheck `2026-10-19` → **`2026-11-03`** (cell was `2026-10-19`;
  used-by `corpus/knowledge/hyprland-config-era-r12.md`).
- **S097** recheck `2026-10-20` → **`2026-11-03`** (opened 2026-10-20, mined).

**No new rows appended this round; zero-row curation with two re-opens**
(371 → 371 at base; this lesson adds neither a row nor a URL to the sweep).

Rubric re-derivation behind C1's number, from the committed gate receipts
(both `rc=0`, both `MADO_VERIFY: CLEAN`): file plane `counts: pass=29 fail=0
unknown=0 skip=8 note=4` (`gate-fileplane-r65.txt`) → 29/29 → 10.0000, which
supersedes the 9.6552 frozen at round 56
(`SCORECARD.md:245`, `28/29`, one FAIL `hypr.root.include_graph`); full live
run `counts: pass=52 fail=0 unknown=0 skip=0 note=8` (`gate-live-r65.txt`) →
52/52 → 10.0000.

One discernment note for the L1, measured and not asserted beyond its
evidence: the round-57 currency rubric's formula is `10 × dated PROVINCE
register rows / declared surface groups` (`SCORECARD.md:2962`) — it counts
*dated* rows, so the seven 2026-10-31 ABSENT rows still satisfy its letter
while the host contradicts every one of them (`before-register-probes-r65.txt`:
`hyprctl`, `waybar`, `walker`, `hypridle`/`hyprlock`/`hyprsunset`,
`.config/{hypr,waybar,walker,alacritty,foot,kitty,ghostty,omarchy}` and
`.agents/skills/omarchy` all PRESENT/present). The debt the block repays is
therefore *host-truth of the dated rows*, not the rubric arithmetic; the
arithmetic never moved.

## Assimilation

FILL-BY-L1 (connector seat reports; not filled by this draft).

## Considerthese

FILL-BY-L1 (connector seat reports; not filled by this draft).
