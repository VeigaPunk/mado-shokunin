# R87ExecMako — report (round 87, wave w1)

Seat: R87ExecMako (executor). Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin.
Scratch: /fast/scratch/hyaku/mado-r87/R87ExecMako (removed at exit; verified absent).
Did not open `controls/mako-cases-r87.json` and did not read any R87Scout report.

## Files written

- `tools/mado-mako.py` (NEW, 25148 bytes, mode 0755 via the write tool). Python 3 stdlib only; no subprocess, network, makoctl, hyprctl or D-Bus. The manual line map is in the comment block at the top of the file.
- `.ufo/waves/round-87/controls/mako-mutants-r87.json` (NEW, schema `mako-mutants-r87-v1`, exactly 10 mutants).
- `.ufo/waves/round-87/w1/R87ExecMako.md` (this report).

## Tool contract as built

- Arguments: `--config PATH` (required; `realpath` once, must be a regular file and readable, else exit 2), `--home DIR` (default `os.path.expanduser("~")`), `--app-name NAME`, `--urgency {low,normal,critical}`, `--mode NAME` (repeatable), `--selftest` with `--scratch-root DIR` (required; must be an existing directory; the selftest creates one private child via mkdtemp and removes it).
- Stdout: exactly one JSON object with keys `effective`, `applied`, `refusals` (sorted keys).
- Stderr: `MADO_MAKO: resolved=<len(effective)> refusals=<m>`.
- Exit 0 when resolution ran; 2 on setup error (argparse errors also exit 2).

## Semantics (each traced to a manual line; manual numbering = `nl -ba` of the decompressed roff)

- Defaults form the base (L519-522); global section overrides (L519-522, L581 allows `key = value`); matching criteria override in file order, last wins (L435-437).
- Criteria fields modelled: `app-name` (plain string, equality; L443-444, regex only via `~` suffix L450), `urgency` (L459), `mode` (L469-471). Any other field (summary, body, category, desktop-entry, app-icon, actionable, expiring, grouped, group-index, hidden, output, anchor, bare booleans) is refused and the section is not applied (L447-495, L510-516).
- A criteria needing `--app-name` or `--urgency` that was not supplied is refused, not guessed (section not applied).
- Criteria quoting and backslash escapes per L497-508; spaces around `=` in a criteria header are refused (L506-507).
- `include=` in the global section only (L45); must be absolute or start with `~/` (L47-48); `~/` expands via `--home`; target must be a regular file (checked with `os.stat`, following symlinks); missing, non-regular, and cyclic includes are refused. Included content is read at the directive's position and returns to the global section.
- Modes: enabled set = {"default"} (L620-621) plus every `--mode` value (L633-634 `makoctl mode -a` adds).
- Unknown options, global-only keys in criteria (max-history L28, sort L37), criteria-only `invisible` in global (L540-545), and invalid values for enumerated, boolean (0|1), integer, directional (1-4 ints, L569-573), colour (L557), progress-color, and action options are refused per line; the rest of the file still applies.

## Judgment calls the L1 should see (not in the manual verbatim)

1. The sha256 in the frozen declaration (`f717848f…`) is the sha of the DECOMPRESSED roff text, not of `/usr/share/man/man5/mako.5.gz` (which is `17ffc88c…`). Checked in this seat: `sha256sum mako.5` (decompressed) = `f717848f47cc7739d4bd…`; `sha256sum mako.5.gz` = `17ffc88c9950ba83a60a…`. The declaration's wording should say which one is pinned.
2. Include placement: the manual says "Includes a config at the specified path" (L45) and is silent on ordering; the tool treats it as inline at the directive.
3. `app-name` equality: L443 names the type "string" without "exact"; L447/L453 state "exact" for summary/body. The tool treats app-name as literal equality.
4. Effective includes defaults for every option, and the global-only keys `max-history` and `sort` (L519-522 "contains the defaults for all style options").
5. Including "default" in the enabled set even when `--mode` is given follows L620-621 and L633-634; a caller that intends `--mode` to replace the list will get different results.

## Commands and exit codes (all run from the lane root with `python3 -I`)

1. `TMPDIR=$S python3 -I tools/mado-mako.py --selftest --scratch-root $S` → exit 0.
   Transcript (stderr):
   ```
   MADO_MAKO_SELFTEST: checks=29 failed=0
   selftest_exit=0
   ```
   (The selftest covers global overrides, comment handling, app-name and urgency matching, quoting and escapes, last-wins, mode on/off and the initial "default" mode, relative/absolute/`~/` includes, missing, non-regular and cyclic includes, unmodelled fields, missing inputs, invalid urgency, unknown and criteria-only global keys, include inside criteria, spaced `=` in criteria, invalid enum, unterminated quote, and max-history in criteria.)
2. Mutant `old` counts and JSON validation (one-line Python count against `tools/mado-mako.py`): all ten `old` strings count exactly 1; schema check and `ast.parse` passed (exit 0).

   | id | count |
   |---|---|
   | M01-criteria-setdefault | 1 |
   | M02-global-ignored | 1 |
   | M03-relative-include-accepted | 1 |
   | M04-tilde-ignores-home | 1 |
   | M05-no-initial-mode | 1 |
   | M06-no-defaults | 1 |
   | M07-app-name-ignored | 1 |
   | M08-missing-input-matches | 1 |
   | M09-urgency-inverted | 1 |
   | M10-unterminated-quote-accepted | 1 |

3. Fixture run in scratch (hand-built: `home/.config/mako/config` symlink → `theme/mako.ini`, which includes `~/.config/mako/core.ini`; criteria `[mode=do-not-disturb]`, `[app-name=firefox urgency=critical]`, `[app-name=firefox]`), invoked as `python3 -I <tool> --config <symlink> --home <home> --app-name firefox --urgency critical --mode do-not-disturb` → exit 0.
   ```
   stderr: MADO_MAKO: resolved=37 refusals=0
   applied: ["global-section", "include:<home>/.config/mako/core.ini", "section:[app-name=firefox]", "section:[mode=do-not-disturb]", "section:[app-name=firefox urgency=critical]", "section:[app-name=firefox]"]
   effective (selected): width=400, height=120 (global), background-color=#112233FF (include section), text-color=#FF0000FF, invisible=1, max-history=5 (include global), anchor=top-right (default)
   refusals: []
   ```
   The symlink was resolved once; the criteria order and last-wins behaved per L435-437.

4. Mutant effect check (scratch driver, 11 configs × 10 mutants, original versus each mutant copy in scratch; exit 0). Each mutant changes the output on at least one config:
   - M01: fixture, mode-default, criteria-override
   - M02: fixture, relative-include, tilde-include, global
   - M03: relative-include
   - M04: fixture, tilde-include
   - M05: mode-default
   - M06: 11 of 11 configs
   - M07: app-mismatch, missing-app
   - M08: missing-app
   - M09: fixture, urgency-mismatch
   - M10: unterminated
   Baseline exits: all 0.

5. Manual line check: `nl -ba mako.5 | sed -n '45,50p;435,437p;469,471p;619,621p'` → exit 0; the lines quoted above match.

## Dead steps

- A persistent-shell trap (`trap 'rm -rf -- "$S"' EXIT`) set in the selftest command removed the scratch directory (including `mako.5`) when that shell ended. The man page was re-decompressed into the same scratch path before the line check; nothing was lost from the lane. No other command failed.

## Installs

None. Nothing was installed or upgraded. No pacman transaction was run.

## Cleanup

- Scratch `/fast/scratch/hyaku/mado-r87/R87ExecMako` removed; `test -e` returned 1 (absent).
- No `__pycache__` was created under `tools/`.
- No file outside the two named files and this report was written in the lane.

## Checks the L1 should run (not run by this seat)

- `python3 -I tools/mado-mako.py --selftest --scratch-root <dir>` expecting exit 0 and `checks=29 failed=0`.
- The C1 counter's own application of the 10 mutants against this tool; the counts above say each `old` is unique.
