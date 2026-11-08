# mado round 99 — lessons (hyaku run 15, attempt 2)

Lane `mado`, branch `master`, base `2cbaa141f42df9dfeee4d207cae6558a4dd59863`. This file carries the
round's `## Gate` (every source row opened this round: URL, access date, located quote, decision) and
`## Mistakes` (class, evidence pointer, captured-by, fix, shown able to fail).

## Gate

Every row below was fetched with `curl -sSL -o <file> -w '%{http_code} %{url_effective}'` on
2026-11-07 and counts only at HTTP 200; the bytes are committed under
`.ufo/waves/round-99/fetch/` and hashed in `.ufo/waves/round-99/receipts/sources-open-r99.txt`.

| id | row | url | access | located quote (<=25 words) | decision |
|---|---|---|---|---|---|
| S532 | `gio-tool-launch.c` (tier A) | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c | 2026-11-07 | `args = g_list_append (args, g_file_new_for_commandline_arg (argv[i]));` (`:116`) | admit — the caller that builds the launch argument list; the round-98 lesson listed it and the registry never carried it (spot-check D1) |
| S533 | `gutils.c` (tier A) | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c | 2026-11-07 | `Locates the first executable named @program in @path, in the same way that execvp() would locate it.` (`:280-281`) | admit — the program-search function the load gate, the terminal search and the `argv[0]` lookup all call |
| S534 | Desktop Entry Specification, recognised keys (tier A) | https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html | 2026-11-07 | `If entry is of type Application, the working directory to run the program in.` (`:128`) | admit — the spec's `Path` and `Terminal` sentences (`:130` `Whether the program runs in a terminal window.`), the documentary half of the round's surface |

Rejected this round: none (three rows opened, three admitted; the round adds no row it refuses).

## Mistakes

**M99-1 — a registry row's pins were copied from a pre-freeze draft, and no lane instrument reads a
row's pins back.**
Class: a claim about bytes that no checker re-derives (the round-98 spot-check's D3).
Evidence: `SKILL.md`'s `mado-r98-execargv` row carried `--expect-tool-sha256 acfcc4f7…` and
`--expect-mutants-sha256 5f074f70…`; the committed `tools/mado-execargv.py` at the tip hashes
`49f7fecdc3bef99a077fe73ac12f5fe211d7ae8c41df5ddc949daf685405f713` and the mutants file
`32c207b32d8aa6126ee949383e7ab992f53c76369310a3e7d88c2b6240ce53bb`, the values the round-98 freeze
block names. A reader running the row's own command hit `SETUP_ERROR tool_pin`.
Captured-by: the round-98 outside spot-check (D3), not any lane instrument — the round-98 counter
checks its pins against the *file it materialises*, so it can never see a row's stale copy.
Fix: the two pins corrected to the freeze block's values, and `corpus/QUALITY.md` criterion 171 added
(a row's pins are re-derived from the artifact they name at the row's declared revision).
Shown able to fail: `git show master:tools/mado-execargv.py | sha256sum` prints `49f7fecd…` while the
pre-fix row printed `acfcc4f7…`; the r98 counter with `--expect-tool-sha256 acfcc4f7…` exits
`SETUP_ERROR … tool_pin` and with `49f7fecd…` runs the case leg.

**M99-2 — two source locators were written from the function's range, not from the line the quote sits
on.**
Class: a citation whose locator is inferred from the block it belongs to (the round-97 lesson's
criterion-168 family, applied to line numbers).
Evidence: the S533 Gate row said `:274-276` for `Locates the first executable named @program in @path…`
and the fetch receipt said `:345-347` for `Use the working dir as program path if provided`; the bytes
put them at `:280-281` and `:322` (the second string also recurs at `:479`).
Captured-by: the round-99 records reviewer (R99MReviewRecords, `receipts/review-records-r99.txt`),
which re-grepped both strings; no lane gate reads a lesson's locator.
Fix: both locators corrected to the grepped lines; the rule applied from now on is that every
locator is produced by `grep -n` on the fetched bytes, never by reading a function's range.
Shown able to fail: `grep -n 'Locates the first executable named' .ufo/waves/round-99/fetch/gutils.c`
prints `280:`, and `grep -n 'Use the working dir as program path'` prints `322:` and `479:` — neither
is `274` or `345`.

**M99-3 — a frozen claim sentence was wider than the property its counter enforces, and only the wave's
own attack seats found it.**
Class: a before-state or control sentence that a reader would re-derive differently from the instrument
(the Amendment-59 / addendum-§8 class; five lanes lost 26 of 26 claims to it).
Evidence: C1's before-state named "the post-prepend `argv[0]` program lookup" as a surface no lane tool
answered, while `tools/mado-mime.py` already models `g_find_program_for_path` at the base
(`git show 2cbaa141:tools/mado-mime.py`, `find_program` at `:467`); C2 said "the two dropped legs were
noticed only by the outside spot-check", while `.ufo/waves/round-98/receipts/harm-final-r98.txt:41-43`
(committed `fa4445af`, before the spot-check) already names the `r97c2_counter_selftest` omission; and
C2's `selftest_checks >= 12` is the counter's fixture selftest, not the gate's `--selftest`.
Captured-by: the round's attack seats — `w1/R99MReviewRecords.md` §8 and §9.11,
`w1/R99MCriticC2.md` F3/F9, `w1/R99MMutC2.md` F3/F4 — not any lane gate; the pre-file ledger
(`.ufo/waves/round-99/claim-falsification.tsv`) is the first instrument that binds them.
Fix: the claims were amended down to the enforceable sentences before filing (`plans/round-99.md`
A1/A3/A4/A5/A6), the ledger reconciles every attack seat's artifact, and QUALITY criterion 172 makes
the pre-file read permanent.
Shown able to fail: `git show 2cbaa141:tools/mado-mime.py | grep -n 'def find_program'` prints `:467`
(the primitive existed, so the original C1 sentence is false at the base), while the narrowed composite
sentence has no counterexample in the wave; the pre-file gate run over a ledger with one attack-seat row
removed prints `FINDING attack-seat-unread …` (control receipt
`.ufo/waves/round-99/receipts/prefile-control-r99.txt`), and the frozen ledger exits 0.

**M99-4 — a frozen per-leg timeout with no headroom converts host load into a red panel, and the
round's claim number is judged on it.**
Class: an instrument limit (a wall-clock cap) that is an undeclared input to the predicate; the
round-98/99 panel chose 600 s at `e39cd5e0`, below the worst leg's loaded duration.
Evidence: the attempt-4 re-derivation of the frozen C2 command scored `mismatches=2` —
`r92_gate_defects` and `r97c1_filetype` both `rc=124 timeout-after-600s` at the cap under fleet load
(load average 327 on 32 cores); the two-leg probe at a short scratch root reproduces both
(`.ufo/waves/round-99/receipts/c2-measured-r99.txt`, `c2-probe-r99.txt`). The mutation seat had
predicted the class before the freeze (`w1/R99MMutC2.md` F5: a lowered cap voids a slow leg's
discrimination); the cap was nonetheless re-frozen to 600 s.
Captured-by: the round's own re-derivation, not a wave seat (the wave flagged the class, the
pre-file ledger read the wording, but no instrument watched the cap).
Fix: the C2 claim files as an honest stop (`plans/round-99.md` A9); the repair routed to round 100
is a re-frozen panel whose per-leg cap is above the measured worst leg plus headroom (or a
per-leg declared expectation), never a post-data target move.
Shown able to fail: the two-leg probe exits 1 with `LEG … rc=124 … timeout-after-600s` twice at the
frozen cap; the panel's own `timeout_s` is 600 and the counter passes no `--timeout`, so a leg
needing >600 s is scored as a mismatch.

## Errata (round 100 — the outside spot-check's routed defect 1, corrected append-only)

- The pointer in M99-3 and in `QUALITY.md` criterion 172 reads `find_program` "at `:467`". Measured at
  round 100: `git show 2cbaa141:tools/mado-mime.py | grep -n 'def find_program'` prints
  `466:def find_program(program: str, path_env: str | None, workdir: str | None) -> bool:`. `:467` is
  the first docstring line (it names `g_find_program_for_path`, which is why the pointer read as
  plausible). The corrected pointer is `:466` (the `def` the command prints); the docstring line
  `:467` is cited by name where the GLib sentence it paraphrases matters.
- M99-4's "no instrument watched the cap" stands; the cap's repair lands in round 100 (C2).
