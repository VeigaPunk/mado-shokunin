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
