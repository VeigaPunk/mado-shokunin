# R88MScribeEntry — round 88, wave w1 (scribe entry)

Seat: R88MScribeEntry (scribe). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Base revision: 24ba2a9ddac21c1211579231e6ee1d98963f9988 (master).
Assignment: draft the round's corpus text for the L1 to integrate — one knowledge entry, one lesson, two QUALITY
criteria — writing drafts only (the L1 edits `corpus/`).

## Files written

- `.ufo/waves/round-88/w1/draft-knowledge-mako-fields-containment-r88.md` — target `corpus/knowledge/mako-fields-containment-r88.md`.
- `.ufo/waves/round-88/w1/draft-lesson-round-88.md` — target `corpus/lessons/round-88.md`.
- `.ufo/waves/round-88/w1/draft-quality-criteria-r88.md` — targets `corpus/QUALITY.md` criteria 146 and 147.
- `.ufo/waves/round-88/w1/receipt-base-host-config-r88.txt` — the base-tool host replay receipt the drafts cite.
- `.ufo/waves/round-88/w1/R88MScribeEntry.md` — this report.

No other file was created or modified. No `corpus/`, `tools/`, `quality/`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`,
`LOG.md`, declaration, or sibling-lane file was touched.

## Behaviour

1. Read the declaration, the r87 knowledge entry, the r87 lesson, `corpus/QUALITY.md` (numbering and style), the
   r87 verifier spot-check, and `considerthese/2026-11-04.md`.
2. Opened every manual and upstream line the drafts cite (list under Gates), plus `path_resolution(7)` for the
   containment basis, and pinned all three sources by sha256.
3. Ran the **base** (r87) tool once over the host's mako config chain to capture the refusal that M88-1 describes;
   the receipt is committed in w1. No candidate scoring was performed (freeze rule): neither `c1-r88` nor `c2-r88`
   was run, and `build/*.py` and `tools/mado-mako.py` were not executed.
4. Mined the second mistake from the r83–r87 spot-check routed-defect sections and checked it against
   `corpus/QUALITY.md` before claiming it is uncovered.
5. Left every measured figure the L1 owns as `<L1: …>`; no number in the three drafts is invented.

## Gates (command, exit code)

| # | command | rc | result |
|---|---|---|---|
| 1 | `grep -nE '^[0-9]+\. ' corpus/QUALITY.md \| tail -5` | 0 | plain-form list ends at 99; the bold-form block ends at **145** (`corpus/QUALITY.md:1052`), so the drafts use 146/147 |
| 2 | `zcat /usr/share/man/man5/mako.5.gz \| nl -ba \| sed -n '40,60p;415,475p;495,525p'` | 0 | L45-48 include, L443-469 twelve first-pass fields, L510-516 boolean grammar |
| 3 | `zcat /usr/share/man/man5/mako.5.gz \| nl -ba \| sed -n '536,556p;260,270p'` | 0 | L266 `icons=0\|1`, L545 `invisible=0\|1` |
| 4 | `zcat /usr/share/man/man5/mako.5.gz \| nl -ba \| sed -n '610,640p'` | 0 | L616-618 mode application, L628-629 the manual's own `invisible=1` DND example |
| 5 | `zcat /usr/share/man/man5/mako.5.gz \| sha256sum` | 0 | `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` — matches the S493 pin |
| 6 | `curl -sSfL -o <f> https://raw.githubusercontent.com/emersion/mako/v1.11.0/<f>` for `criteria.c`, `types.c`, `config.c`; `sha256sum` | 0 | `criteria.c 2276774…`, `types.c c2f3398…`, `config.c 94c3a4e…` (full digests in the drafts) |
| 7 | `grep -n 'parse_boolean' -A 25 types.c` | 0 | `types.c:19-29`: `strcasecmp` true/false, exact `1`/`0`, else false |
| 8 | `nl -ba criteria.c \| sed -n '61,140p'` | 0 | `match_criteria` per-field tests at 76, 81, 86, 91, 96, 101, 106, 111, 116, 123, 128; `mode` at 155 |
| 9 | `nl -ba criteria.c \| sed -n '267,300p;362,400p'` | 0 | bare token → `"true"`, `!field` → `"false"` (283-289); `parse_boolean` for actionable/expiring/grouped/hidden (369-400) |
| 10 | `nl -ba config.c \| sed -n '495,522p'`; `grep -n 'include' config.c`; `grep -n 'invisible' config.c` | 0 | `expand_config_path` 505-522 (absolute or `~/`, else refused); `include` at 545-548; `invisible` → `parse_boolean` at 648-649 |
| 11 | `zcat /usr/share/man/man7/path_resolution.7.gz \| nl -ba \| sed -n '1,55p;110,200p'`; `sha256sum` of container and `zcat` stream | 0 | symlink resolution 77-99, 40-link cap 105-117, `..` 136-145, mount points 146-161, final symlink 169-178; container `2a21ab67…`, text `20726811…` |
| 12 | `git -C … show 24ba2a9d…:tools/mado-mako.py \| nl -ba \| sed -n '95,130p'` | 0 | `:113-114` `expects 0 or 1`; `:75` `MODELLED_FIELDS = ("app-name", "urgency", "mode")`; `:271` criteria-field refusal |
| 13 | `python3 -I base/mado-mako-r87.py --config ~/.config/mako/config --home "$HOME" --app-name notify-send --urgency normal --mode do-not-disturb` (base tool, sha256 `67a955a5…`) | 0 | `resolved=37 refusals=7`; refusals include `core.ini:15`/`:18` `invisible='true'\|'false': expects 0 or 1` and five `summary~` sections; effective `invisible="0"` |
| 14 | `python3 -I -c` count of `invisible` tokens in `.ufo/waves/round-87/controls/mako-cases-r87.json` | 0 | 22 cases; `invisible=true` 0, `invisible=false` 0, `invisible` 0 |
| 15 | `grep -niE 'scratch' corpus/QUALITY.md`; `grep -niE 'shared scratch\|probe director' corpus/QUALITY.md` | 0 / 1 | 34 and 98 govern result paths and size, not the scratch root; the second grep returns no line (rc 1 = no match) |
| 16 | `grep -niE 'wave-done\|telemetry\|settled\|population\|registry\|locator\|chronolog' corpus/QUALITY.md` | 0 | 145 covers r85 R4 (null output), 102/103 wave results, 93 gate registry, 77/97 locators — each candidate mistake rejected on a hit |
| 17 | `grep -n 'erratum 6\|erratum 4' corpus/lessons/round-87-verifier-spotcheck.md` | 0 | `:25` and `:26`; R4 at `:117-118` |
| 18 | `sed -n '214,218p' corpus/lessons/round-85-verifier-spotcheck.md` | 0 | R7 text quoted in M88-2 |

`git` was used read-only (`show`). No mutating git/jj command was run anywhere. No pacman transaction; **no tool
installed or updated**.

## Findings

- **F1 (evidence, closes M88-1's capture gap).** The r87 frozen case set never exercises the host's boolean
  spelling: `.ufo/waves/round-87/controls/mako-cases-r87.json` has 22 cases and zero `invisible` tokens. The r87
  resolver's refusal of `core.ini:15`/`:18` was therefore invisible to its own scoring, which is why the defect
  survived to r88.
- **F2 (evidence, base tool).** Replayed on the host chain, the base tool reports 7 refusals and resolves
  `invisible` to `"0"`; two of the refusals are the DND lines and five are `summary~` sections. Receipt:
  `receipt-base-host-config-r88.txt`.
- **F3 (named limit, carried into the knowledge draft).** C1 models `summary`/`body` but still refuses `summary~`/
  `body~`, so the host's five `[summary~="…"]` click-action sections (`core.ini:24,27,30,33,36`) remain
  unresolved after r88. The draft states this in §1 and §5 rather than implying full host coverage.
- **F4 (source detail).** The manual's own do-not-disturb example writes `invisible=1` (L628-629) while the host
  writes `invisible=true` — both accepted upstream (`types.c:19-29`), which is exactly the gap the manual's
  `0|1` shorthand hides. Recorded in the knowledge draft §2.
- **F5 (second mistake, mined and checked).** r85 R7 (scratch created directly under the shared scratch root) is
  not covered by any QUALITY criterion: criteria 34 and 98 govern result paths and the size bound, and no line
  matches `shared scratch`/`probe director`. It becomes M88-2 with a dispatch-level fix, not a new number.

## Out of scope / not run

- No candidate scoring: `c1-r88-mako-fields.py` and `c2-r88-include-containment.py` were not executed, and neither
  `build/mado-mako.c1.py`, `build/mado-mako.c2.py` nor the working-tree `tools/mado-mako.py` was run. The C1/C2
  figures in the drafts are `<L1: …>` placeholders.
- No case authoring: `mako-cases-r88.json` and `containment-cases-r88.json` are other seats' files; I did not read
  or write them.
- The `## Gate` registry rows for S494/S495 carry placeholders for the scout's located quotes; the digests and
  locators are mine and are pinned above.
- The lesson's wave-findings table, census rows, spot-check and domain-share count are `<L1: …>` placeholders.

## Scratch

`S=$HYAKU_SCRATCH/mado-r88/R88MScribeEntry` (`/fast/scratch/hyaku/mado-r88/R88MScribeEntry`): held the extracted
base tool and the three upstream files. The receipt was copied into w1 before deletion; the directory was removed
on exit. No scratch remains.
