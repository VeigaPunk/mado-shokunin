# Round 64 — mado lesson (hyaku run 12)

Base `7fe65562c15d20e5cfdc1da536f774149ab52b7e` (the r63 closure tip,
pushed). Host: Windows 11 Home, build 26200, as in rounds 57-63. Three
claims: **C1 calibration** (the r63 carry-in repair — the closure's routed
item 1: the error-path receipt's cited fixture `broken-fixture.json` never
landed; the lane committed the fixture at the cited path as a disclosed
round-64 re-creation and re-derived the rc=2 error verdict against the
committed bytes), **C2 coverage** (sourced — the D05 flip-condition probe:
S424 re-opened, one bounded read-only probe running the QDC flag matrix
0x02/0x12/0x42/0x52 twice byte-identical; D05 narrowed, not flipped, with
three new measured rows and one join in the entry's append-only Update
section), **C3 operability** (capability acquisition
`tools/mado-receipt-citecheck.py` — the routed defect class mechanized:
red `TARGET_MISSED` at the base rev naming exactly the routed citation,
green at the landing; ledger 103 → 104). L1-only round again: the MISSION
≥8-L2 dispatch floor has no surface on this host (disclosed since r57, L0
open; unchanged). The security boundary held throughout: no r56-era
credential material was opened or surfaced; the citecheck's scan scope is
caller-named paths only and never touches r56-era material.

## Gate

### Admitted

- **S424 re-opened (2026-11-01)** —
  `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-querydisplayconfig`
  (the r63 row, unchanged upstream: ms.date 2018-12-05, git_commit
  `39f250c30f4e46de1ef92f2ef07161753ba36e35`, updated_at 2026-05-15).
  Located quote (verbatim, § Parameters, the flags OR-table):
  "This flag should be bitwise OR'ed with other flags to indicate that the
  caller is aware of virtual refresh rate support." (QDC_VIRTUAL_REFRESH_RATE_AWARE
  0x00000040, "Supported starting in Windows 11"); the companion row
  QDC_VIRTUAL_MODE_AWARE 0x00000010 "Supported starting in Windows 10"; and
  the page's own example code declaring
  `UINT32 flags = QDC_ONLY_ACTIVE_PATHS | QDC_VIRTUAL_MODE_AWARE;` — the
  documented virtual-aware call shape this round's probe pins. The K44
  r63 transcription was checked against the live page before any probe was
  written (the M63-3 discipline) and agrees. No new registry row: the r64
  probe's entire documented surface is the eleven rows the r63 sweep opened
  (S424-S434); no new URL entered the sweep, no rejected-row event, no
  reused-row fabrication. Registry row count 371 → 371; the re-open is
  recorded here and in the entry's Update header, not by cell edits (CORPUS
  rule 2 — only status/recheck/used-by change in place, and none changed).

- **Entry Update** `knowledge/windows-displayconfig-r63.md` — the
  append-only `## Update (round 64)` sections: rows H29 (the 0x42
  virtual-refresh shape returns the r63 baseline verbatim, sentinel
  included), H30 (the 0x12/0x52 virtual-mode shapes grow the mode table by
  a DESKTOP_IMAGE entry — infoType 3, the documented K51 vocabulary — set
  the documented SUPPORT_VIRTUAL_MODE path flag 0x8 (K46/S426), and move
  the path's target `modeInfoIdx` 0 → 2 onto that non-TARGET entry; the
  decode guard emits null, the rejected-row discipline kept), H31 (D05
  narrowed, not flipped: no documented shape returns decoded frequencies;
  cause stays `[UNK]`; remaining residue driver-class / second-host,
  operator-scoped), J29 (the two flags answer D05's two residue branches
  distinctly). Entry row sites 19 → 23; the entry's original 105 lines are
  a byte-preserved prefix (head-diff in the landing counters receipt).

- **Capability (C3)**: `tools/mado-receipt-citecheck.py`
  (`VERSION r64-v1`): selftest 12/12 rc=0; red demonstration at the base
  rev — the checker over `.ufo/waves/round-63/receipts` at `7fe65562`
  reports `citations=9 resolved=8 missing=1 … verdict=TARGET_MISSED` rc=1,
  the missing citation exactly `.ufo/waves/round-63/receipts/broken-fixture.json`
  from `windisplayconfig-error-path.txt` (the r63 closure's routed item,
  caught by instrument); green at the landing (landing counters receipt).
  Ledger population 103 → 104; PROVINCE round-64 refinement in the same
  landing.

- **C1's fixture + re-derivation**: `.ufo/waves/round-63/receipts/broken-fixture.json`
  committed (the round-64 re-creation — disclosed at every claim site);
  `windisplayconfig-errorpath-r64.txt` records the re-derived verdict rc=2,
  the same whitelisted detail line as the r63 receipt, raw bytes never
  echoed.

### Rejected (reasons stay; flip conditions named)

- **Building a screen-capture probe this round** (still): the
  screen-capture-scope L0 question (filed r60) has no ruling. **Flip:**
  unchanged — the operator rules the capture scope; then the probe is
  claimable like any other.
- **Decoding the DESKTOP_IMAGE union member** (the natural follow-on the
  probe's own finding suggests): the H30 finding names the third entry's
  class from the documented S431 vocabulary; decoding its storage would
  need the DESKTOP_IMAGE-mode structure page opened and marshaled, and no
  claim this round needs its contents — the entry's limit is restated in
  the Update section. **Flip:** a claim that joins the desktop-image mode's
  fields (and the opened page for them) brings it in with its own rows.
- **Evolving `tools/mado-win-displayconfig.py` with a virtual-flags
  option** (making the matrix durable in the r63 tool): the r63 receipts
  and capability row pin `VERSION r63-v1` behavior and bytes; the flag
  matrix answered D05's flip condition at the probe layer, so a tool
  evolution this round buys no claim value while invalidating committed
  crosscheck byte-matches. **Flip:** an operator need for the
  virtual-aware observation as a standing surface (a ruling, or a claim
  that needs it), landing as a disclosed new version.
- **Treating the five dormant L0/rubric questions as answerable by
  measurement this round** (omarchy freshness disposal; gate-selftest
  host gap; calibration resolved-active re-derivability; screen-capture
  scope; the L2 floor): all disposals are the operator's (filed
  r57/r58/r59/r60 + the standing L2 line); re-scoring them lane-side
  would presume the ruling. **Flip:** an operator ruling on any of them.

## Mistakes

- **M64-1 — a double-quoted `echo` containing backticks opened a bash
  command substitution that swallowed two script lines, and bash reported
  the syntax error at the parenthesis of a LATER line than the defect.**
  The before-state receipt script's first draft transcribed the SCORECARD
  index-row regex into a `cmd:` echo line inside double quotes; the
  backticks around `` `knowledge/…` `` started command substitution, and
  the interpreter died two lines later with "syntax error near unexpected
  token `('". Class `measurement` (caught by the script's own non-zero
  exit and the read-back of the receipt file before anything was committed;
  the receipt's truncated tail was the tell). Evidence: the first
  before-state-r64.txt ends mid-script at the INDEX_RC section with the
  bash diagnostic naming line 41, while the backtick is on line 38 — the
  reported location is a symptom, the quoting scan is the diagnosis (the
  M63-1 class one layer down: there a SyntaxError's reported line, here a
  bash parse-error's). Fix: the echo re-written backtick-free (the regex
  transcribed in prose); the rule carried — embedded markup characters are
  quoted for the shell's benefit, never trusted inside double quotes; a
  parse error's reported line is where the confusion ENDED, not where it
  began.
- **M64-2 — a long in-line heredoc append was truncated mid-line by the
  tool-input boundary, and the write's only signal was a delimiter
  warning.** The first attempt to append the round-64 SCORECARD section
  (~13 KB) was issued as one shell heredoc; the input was cut partway
  through the Capabilities table row, bash reported "here-document
  delimited by end-of-file (wanted `EOF`)", and the file gained a section
  ending mid-sentence ("resolves in the") — the terminator, the planned
  block, the harm watch and the trailing echo all lost. Class
  `measurement` (the M63-1 class at the record-write layer: a write
  trusted from its intent instead of being read back at its target).
  Evidence: post-append `wc -l` (3412 vs the expected ~3455),
  `tail` ending mid-word, `grep -c "### Planned (round 65"` → 0.
  Captured-by: the read-back step (the same landing-verification
  discipline that caught the r63 receipts-directory drop). Fix:
  SCORECARD restored byte-exact from the base git object
  (`git show HEAD:SCORECARD.md`, `cmp` against the truncated prefix
  first — PREFIX_IDENTICAL_TO_BASE — then copied back), and the section
  re-landed through a scratch file written whole, length-checked
  (`wc -l` + `tail -1` against the intended last line) and `cat`-appended.
  Rule: long record appends travel as whole files with a checked length,
  never as one giant in-line heredoc; a heredoc warning is a truncation
  until a read-back proves otherwise.

## Census

Start (round start, before any edit): exit 0, `mado ok`, warning set
36 W04 + 1 W01 (identical to r57-r63), 371 rows by the registry grep;
tee'd to `.ufo/waves/round-64/receipts/census-start-r64.txt` (the
r61-r63 committed-receipt shape kept). End:
`.ufo/waves/round-64/census-after-r64.txt` → exit 0 (S424 re-open added no
row, so the warning set is expected unchanged). Before-state receipt
`before-state-r64.txt` (all base values for every counting command, every
producer's rc captured; one script defect caught and fixed in the work
window — M64-1 — the committed receipt is the re-run's output). Tool and
probe receipts committed beside them: qdc-flagmatrix-probe.ps1 +
qdc-matrix-run1/run2.json (byte-identical, rc=0 ×2) + stderr,
qdc-matrix-crosscheck.py + qdc-matrix-crosscheck.txt (19/19 AGREE),
windisplayconfig-errorpath-r64.txt (+ stderr), citecheck-selftest.txt
(+ stderr), citecheck-red-base-rev.txt (+ stderr), dwm-recheck-r64.txt
(+ stderr), windisplayconfig-recheck-r64.txt (+ stderr), the claims
declaration, and the landing counters receipt (navigation/used-by/ledger/
citecheck-green at the landing, named sections).

## Considerthese and assimilation

- Mined all nine `considerthese/` files again this round (directory listing
  + mtimes re-run 2026-11-01 — no new files since the r58 mining, the same
  nine with unchanged mtimes that r63 screened): no adoptable proposal. The
  dispositions of r57-r63 stand.
- Assimilation: none — shokuknow unreachable.

## Route to round 65 (intent only; no commitment)

1. The five L0 rulings (omarchy freshness disposal; gate-selftest host
   gap; calibration resolved-active re-derivability; screen-capture
   scope; the L2 floor) — the SCORECARD tables follow the ruling, never
   precede it.
2. The rendered-pixel observation iff the screen-capture-scope L0
   question is ruled; the candidate shape stays the statistics-only,
   no-persist capture probe.
3. D05's remaining residue: the driver-class / second-host reading only
   if the operator scopes one; the lane-side flag matrix is complete.
4. The citecheck's standing use in the landing counters each round.

## Addendum (the ledger append glued onto the ledger's final line; the ledger gate went red at the landing; repaired before closure)

The landing commit `688144573a26` carried a ledger-append defect the round's
own receipts did not predict: `quality/tool-ledger.md`'s final r63 row had
no trailing newline at base, so the round's `cat >>` append glued the new
citecheck row onto the r63 row's last line (`…| \`PROVINCE.md\` || \`tools/mado-receipt-citecheck.py\`…`
— one physical line, two rows). The landing counters receipt records the
result: the ledger counter failed at the landing
(`population=104 ledger_rows=102 uncovered=2 dangling=1 …
verdict=TARGET_MISSED`, rc=1, at `688144573a26`) — the ledger gate caught
the write defect before closure, the same red-then-disclosed shape as r62's
and r63's used-by gates. Class: the M64-1/M64-2 class one layer down — an
append written against an assumed trailing newline that was never checked
(a write trusted from its intent, caught by the counter at the landing and
by the diff-tree numstat's `1 deleted`, which no honest pure-append round
may contain). Repaired as the ledger contract's own consistency move, keyed
on the row content: the glued line split, the r63 row's bytes restored
byte-exact (verified by a head-prefix `cmp` of the first 32955 bytes
against the base git object — R63_ROW_RESTORED_BYTE_EXACT), the new row on
its own line, and the file now ends with a newline. Green at the repair
`8c5af6ad67007c6c77c3f71c689684e5fd626c2d`:
`population=104 ledger_rows=104 uncovered=0 dangling=0 … verdict=TARGET_MET`
(landing-counters-r64.txt records both states in named sections; the
diff-tree numstat of the repair is the split itself). The M63 Addendum 2
rule is extended here: an append is verified not only at its own new bytes
but at its JOIN — the last line of the target file is read back after every
append.
