# R99MScribe - round 99 w1 scribe report

Seat: `R99MScribe` (scribe). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`,
base revision `2cbaa141f42df9dfeee4d207cae6558a4dd59863`. No commit, no push, no mutating git/jj
command, no subagent, no tool install. Scratch `/fast/scratch/hyaku/mado-r99/R99MScribe` deleted
before this report was filed.

## 1. What was produced

| artifact | path | lines | state |
|---|---|---|---|
| the entry draft | `.ufo/waves/round-99/w1/drafts/gio-launch-env-r99.md` | 427 | complete draft; the L1 lands it at `corpus/knowledge/gio-launch-env-r99.md` |
| the row drafts + gate table | `.ufo/waves/round-99/w1/drafts/sources-rows-r99.md` | 66 | S532, S533, S534 in the 11-column schema; held-row `used-by` additions; `## Gate` table |
| the probe transcript | `.ufo/waves/round-99/w1/R99MScribe-probes.txt` | 156 | 24 cases, 24/24 agreeing |
| the probe harness | `.ufo/waves/round-99/w1/R99MScribe-probe.py` | 280 | the instrument that produced the transcript |
| this seat's spec fetch | `.ufo/waves/round-99/fetch/spec-terminal-path.html` | - | HTTP 200, 24174 B, sha256 `7bc0b640...5c03d9` |

Both drafts are ASCII-only (`LC_ALL=C grep -cP '[^\x00-\x7F]'` = 0 on each).

The entry's structure follows the seat item: scope and provenance (section 1), the load gate (2),
the twelve-row known-terminals table with order and `exec_arg` (3), `g_find_program_for_path`'s
decision tree as a table (4), the prepend (5), the post-prepend `argv[0]` lookup (6), `Path=` as cwd
and as the searches' working dir (7), the empty-`Path=` inheritance (8),
`GIO_LAUNCHED_DESKTOP_FILE` (9), the two refusal shapes with their exact messages (10), the
spec-vs-implementation deltas (11), named limits (12), and the probe rows (13).

## 2. Provenance and commands actually run

- **Sources.** `gdesktopappinfo.c` and `gshell.c` are not in `.ufo/waves/round-99/fetch/`; they were
  read from `.ufo/waves/round-98/fetch/` and hashed:
  `sha256sum` -> `8e9ce1a8...5b0d` and `640a0d0f...0442`, equal to the L1's round-99 receipt rows.
  `gutils.c` (`65086c29...3771`) and `gio-tool-launch.c` (`16b4c868...6595a`) were read from the round-99
  fetch dir and match the receipt. **This is the one place the seat item's premise does not match
  the tree**: the item says the two round-98 files are "carried" into the round-99 fetch dir, and
  they are not there yet. No bytes were moved; the entry cites the receipt's digests.
- **The spec page.** Fetched by this seat:
  `curl -sSL -o .ufo/waves/round-99/fetch/spec-terminal-path.html -w '%{http_code} %{url_effective}' https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html`
  -> `200 https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html`, rc 0.
  sha256 `7bc0b6401cda9c019d5b89a2fab053d216eb937c83602df838a6c0a1175c03d9`, 24174 B - byte-identical
  to the L1's `spec-recognized-keys.html`, so S534's digest is confirmed by two independent fetches.
- **The probes.** 24 cases, each a case root under the scratch dir, each `gio launch` call under
  `env -i LC_ALL=C HOME=<root>/h PROBE_OUT=<root>/out PATH=<the case's own bin dirs only>`, cwd =
  the case root, 10 s timeout, then a quiet wait (poll to a stable size, 0.3 s of no growth, 8 s
  cap). The probe child appends one record per spawn with one `printf` per line. No host
  application was started; no host PATH was ever passed to `gio`.

## 3. Findings the L1 must rule on before the freeze

**F1 - `program-not-found` is reachable only through an empty `Exec`.** The load gate skips its
check when `Exec` is empty (`gdesktopappinfo.c:1974`), so `Exec=` plus one non-executable argument
reaches the post-prepend lookup and refuses with `Program '<arg>' not found in $PATH`, exit 1 (P23).
A case family built only from non-empty `Exec` lines can never label the contract's
`program-not-found` cause. The frozen case file needs the empty-`Exec` shape (or the cause stays
unprobed).

**F2 - with `Terminal=true` the `Exec` program name is never resolved.** The prepend runs at
`:3027-3029` and the post-prepend lookup rewrites `argv[0]` only (`:3066-3086`), so the terminal
receives the literal `Exec` name at index 1 (P19 `TA1=probe.sh`). When that name is findable only
through `Path=` and not through `PATH`, the terminal's own `exec` fails, no probe record is written,
and `gio launch` still exits **0** (P22). Two consequences for the oracle: a model that resolves
index 1 is wrong, and "no record" must not be read as a refusal.

**F3 - a successful spawn exits 0 even when the child fails** (P22). The oracle's `expect` must
derive the cause from `gio`'s stderr and exit status only, never from a missing child record.

**F4 - the CLI contract's cause list omits `cwd-failed`.** Declaration R4 names "the refusal cause
`cwd-failed` (measured this round)" and this seat measured it (P08:
`Unable to launch application '<desktop>': Failed to change to directory "<path>" (No such file or
directory)`, exit 1), but shared contract 1's exit-2 cause list is `load`, `no-terminal`,
`program-not-found`, `no-exec`, `desktop-file`, `exec-parse` - no `cwd-failed`. A candidate that
refuses with `cwd-failed` prints a cause outside the frozen list. The L1 should either add the cause
to the CLI contract or drop R4's cause name; the entry records the refusal shape either way
(section 10).

**F5 - the terminal search uses `Path=` as its working directory** (P19), which the declaration's R2
already states (`g_find_program_for_path(name, PATH, Path=)`); no conflict, recorded as measured.

**F6 - the empty-`Path=` inheritance is a measurement, not a located line.** P07/P14/P15 measure it;
the empty-vs-NULL decision is in `gspawn.c`, which this round did not open. The entry says so in
sections 8 and 12. The declaration's "(measured)" wording is consistent; a source citation for it
would need `gspawn.c` in the fetch list.

**F7 - `S532` is the id the round-98 lesson already used for `gio-tool-launch.c`** (spot-check
defect D1). The drafted row uses that id, the lesson's line (`:116`) and the lesson's sha256
(`16b4c868...6595a`), so landing it closes D1's row half. `S533` duplicates S506's URL (one expected
W04); `S534`'s URL is new to the registry (`grep -c 'recognized-keys' corpus/SOURCES.md` = 0), as is
S532's (`grep -c 'gio-tool-launch'` = 0).

## 4. Harness corrections made during the work (disclosed, not hidden)

- Run 1 had three of my own expectation errors, not oracle disagreements: P01/P02 expected the probe
  to see the terminal's arguments (it sees only the ones after them), and P11 put `probe.sh` in a
  directory that was on `PATH`, so the case could not test the missing-`Path=` refusal. Fixed the
  expectations and moved the program off `PATH`; run 2 was 20/22 with one expectation error (P19's
  `TA1`, which is the finding F2) and one sentinel the checker did not understand (`<absent>`).
- Run 3 added P21/P22 (the `argv[0]`-only rewrite) and P23/P24 (the empty-`Exec` shape). P23's first
  fixture was mode 0755 because the builder chmods every file, so the "non-executable" argument was
  executable and the case launched; the builder now writes `.txt` files 0644 and P23 refuses as
  expected.
- Run 4 (the filed transcript) is 24/24. `DSI=<unset>` and `XAT=<unset>` in all 16 rows that
  produced a record.

## 5. Gates

None run, none claimed. This seat's assignment is the entry and the rows; the C1 counter, the case
file, the oracle and the harm watch are other seats' artifacts and did not exist in the wave dir
when this report was written (`.ufo/waves/round-99/controls/` and `build/` are absent). The drafts
are therefore **unverified by any lane instrument**; the L1's freeze and the C1 counter are the
first verification they will see. The probe transcript is evidence about `/usr/bin/gio`, not about
the candidate.

## 6. Touched surfaces

- Written: `.ufo/waves/round-99/w1/drafts/gio-launch-env-r99.md`,
  `.ufo/waves/round-99/w1/drafts/sources-rows-r99.md`, `.ufo/waves/round-99/w1/R99MScribe-probes.txt`,
  `.ufo/waves/round-99/w1/R99MScribe-probe.py`, `.ufo/waves/round-99/w1/R99MScribe.md`,
  `.ufo/waves/round-99/fetch/spec-terminal-path.html`.
- Read only: the round-99 wave dir (declaration, receipt, fetch, probe), `.ufo/waves/round-98/fetch/`,
  `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-98.md`,
  `corpus/lessons/round-98-verifier-spotcheck.md`, `corpus/knowledge/gio-exec-argv-r98.md`, `SKILL.md`,
  `/usr/share/man/man1/gio.1.gz`.
- Not touched: `tools/`, `quality/`, `corpus/`, the git index, jj state, the fleet repo, any sibling
  lane, `~/.config`, `~/.local/bin`, any credential material.

## 7. Out of scope / not done

- The C1 candidate (`tools/mado-launchenv.py`), the oracle, the case file, the fresh generator, the
  mutants, the C2 harm watch and panel, the record repairs D2/D3/D4/D6/D8, and the `SKILL.md`
  registry row for `mado-launchenv` are other seats' or the L1's. The entry names the tool only as
  the surface the claim is about; it does not describe its CLI.
- No install or upgrade was made, so there is no tool/version/channel entry to record.
- The entry does not model spawn order, `DBusActivatable`, the `gio-launch-desktop` wrapper, the
  portal path, or whether the process survives (section 12 of the entry).

## 8. Conflicts, verbatim

1. **Round-99 fetch dir vs the seat item.** The item says "the fetched bytes are in
   `.ufo/waves/round-99/fetch/` (gdesktopappinfo.c and gshell.c carried from round 98, ...)"; the
   directory holds only `gio-tool-launch.c`, `gutils.c` and `spec-recognized-keys.html`. The two
   round-98 files exist only under `.ufo/waves/round-98/fetch/` and hash to the receipt's digests.
2. **`cwd-failed` (F4).** Declaration R4: "the refusal cause `cwd-failed` (measured this round)";
   shared contract 1's cause list: "`load` ...; `no-terminal`; `program-not-found`; and the round-98
   causes `no-exec`, `desktop-file`, `exec-parse` passed through". The two lists disagree.
3. **The declaration's R3 wording vs its observable.** R3 says the lookup replaces `argv[0]`; the
   declaration does not say that with `Terminal=true` this leaves the `Exec` program unresolved
   (F2). The rule is right; the consequence is missing from the declaration and is in the entry
   (section 6).

## 9. Named limits of this report

- 24 probe rows over one host, one `gio` build, one day. They label the shapes the entry states;
  they do not prove the twelve-row table's other eight rows (only rows 1, 2, 3 and 12 were exercised
  for order/`exec_arg`).
- The terminal fixtures are stand-ins (`#!/bin/sh` scripts that record and `exec`); the real
  `xdg-terminal-exec` on this host has its own configuration and was never started.
- The entry's quotes are <= 25 words and whitespace-collapsed, but three of them are doc-comment
  sentences (`gutils.c:274-276`, `:383-384`, `gdesktopappinfo.c:1992`) rather than code; the row
  quotes in the sources draft are code lines.
