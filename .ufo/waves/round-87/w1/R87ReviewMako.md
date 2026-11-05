# R87ReviewMako — attack review of tools/mado-mako.py (C1, round mado 87 w1)

Date: 2026-11-05. Seat: R87ReviewMako (reviewer, attack seat, leaf — no dispatch).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-mako.py` at the wave content revision.
Basis: mako 1.11.0 manual, decompressed to scratch with `zcat /usr/share/man/man5/mako.5.gz`;
sha256 of the decompressed text `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` —
matches the sha pinned in `claims-declaration-r87.md`. Line numbers below = `nl -ba` on that file.

Method (independence order kept): manual read first → my own expectations written to scratch
(`expectations.md`, 21 planned probes) → only then the frozen cases file consulted for comparison.
The cases file was NOT on disk when my expectations were fixed.

## Execution summary

- Tool appeared at poll check 3 (05:55:07); cases file absent for 30 checks (05:53–06:38), landed
  ~06:39 in poll window 2; comparison completed against it (§Comparison).
- 58 direct tool invocations over my 44 adversarial fixture files (batteries F01–F21, P01–P26),
  all `python3 -I`, `TMPDIR` pointed at my scratch, every fixture under
  `$HYAKU_SCRATCH/mado-r87/R87ReviewMako`; plus 24 exact replays of the 23 frozen cases
  (23 as-frozen + 1 with the C13 typo corrected) through my scratch replay driver.
- Exit codes observed: 0 for every resolution run (refusals in-band), 2 for setup errors
  (bad `--urgency` value → argparse, missing `--config` → "cannot stat", directory `--config` →
  "not a regular file (after symlink resolution)"). No hangs; the FIFO include target returns
  instantly with a refusal (stat-based check, no open).
- Scratch will be deleted on exit; no lane file written except this report.

## Defects

### D1 — MEDIUM (missing refusal): `~/` include resolved from `$HOME` when `--home` is absent

The tool reads a file its caller never named. Frozen declaration, Tool paragraph: "reads only the
regular files its caller names (`--config`, `--home` for `~`)". With no `--home`, line 522 of the
tool (`home = args.home or os.path.expanduser("~")`) guesses `~` from the process environment and
silently resolves includes against it — environment-dependent output on a `~/` include chain
(the real lane surface: `~/.config/mako/config` is a symlink whose file uses omarchy includes).

Reproduction (run 06:10, scratch `$S=/fast/scratch/hyaku/mado-r87/R87ReviewMako`):
```
# $S/f15/main.ini:      include=~/decoy.ini
# $S/f15/home1/decoy.ini: font=Home1Font
# $S/f15/home2/decoy.ini: font=DecoyFont
HOME=$S/f15/home2 TMPDIR=$S/tmp python3 -I tools/mado-mako.py \
  --config $S/f15/main.ini --app-name x --urgency normal     # no --home
→ exit 0; refusals: []; applied: [... "include:$S/f15/home2/decoy.ini"];
  effective font = "DecoyFont"
```
With `--home $S/f15/home1` the same config yields `font=Home1Font` (correct), proving `--home`
works when given; the defect is only the silent fallback. Deciding authority: the declaration's
"refuses, never guesses" contract + manual L45–49 (`include` path "must be absolute or otherwise
start with ~/"; without `--home` the tool cannot know the caller's home and must refuse the `~/`
include instead of expanding from `$HOME`). Correct behavior: refusal entry, no read.

### D2 — MEDIUM (missing refusal): bare actions accept trailing words

`check_value`'s binding branch (tools/mado-mako.py, BINDING_KEYS case) rejects trailing words only
for `dismiss`. Every other bare action accepts arbitrary trailing text and stores it as the
effective value with zero refusals. Manual grammar: L96 `none`, L134–136 `invoke-default-action`
("Invoke the default action on the notification."), L107/L112 `dismiss-all`/`dismiss-group` — all
bare; only L101 `dismiss [--no-history]`, L117–119 `invoke-action <action>` and L139
`exec <command>` take anything after the verb.

Reproduction (both run 06:10–06:12):
```
# $S/f41/main.ini:       on-button-left=invoke-default-action extra
python3 -I tools/mado-mako.py --config $S/f41/main.ini --app-name x --urgency normal
→ exit 0; refusals: []; effective on-button-left = "invoke-default-action extra"

# $S/f41/none_extra.ini: on-notify=none extra
python3 -I tools/mado-mako.py --config $S/f41/none_extra.ini --app-name x --urgency normal
→ exit 0; refusals: []; effective on-notify = "none extra"
```
An invalid action line silently enters `effective` — a value mako itself would reject at load.

### D3 — LOW (wording): refusal text mis blames valid boolean syntax

`[grouped]` and `[actionable]` are refused with
`criteria token 'grouped' has no '=value' (bare booleans and spaces around '=' are refused)`.
The refusal itself is correct (grouped is a second-pass field, L479–483; actionable is outside the
model), but the message asserts that bare booleans are invalid syntax — manual L510–516 explicitly
documents `[actionable]` / `[!actionable]` as valid, and `[grouped]` is one of the always-present
criteria (L493–495). A config author following the message would "fix" valid syntax. The reason
should say the field is outside the model, not that the grammar is refused.

Reproduction:
```
# $S/f19/main.ini: [grouped] / format=GroupedFormat
# $S/f20/main.ini: [actionable] / font=ActFont
python3 -I tools/mado-mako.py --config $S/f19/main.ini --app-name x --urgency normal
→ exit 0; refusal: "...f19/main.ini:1: criteria token 'grouped' has no '=value' (bare booleans
  and spaces around '=' are refused)"; GroupedFormat not applied (correct outcome, wrong reason).
```

## Contract checks (declaration Tool paragraph)

| Check | Result | Evidence |
|---|---|---|
| stdlib-only | PASS | imports at tool lines 51–58: argparse, json, os, re, shutil, stat, sys, tempfile; import-spy under `python3 -I` loaded no non-stdlib module |
| writes nothing outside --scratch-root | PASS | only write site is `_write` (line 390), called only from `selftest` under `tempfile.mkdtemp(dir=scratch_root)` (line 397); resolution path writes nothing (58 runs, scratch contained only my own files) |
| hardcodes no /tmp | PASS | no `/tmp` literal, no `gettempdir`; the only tempfile call pins `dir=scratch_root` |
| refuses unknown constructs | PASS with D2 exception | refused: unknown global/criteria keys, unmodeled fields (summary, app-name~, grouped, actionable bare forms), out-of-domain values (urgency, colors, enums, ints, bools, directionals, actions, progress-color), malformed headers (unclosed, unterminated quote, dangling backslash, trailing token, repeated field), include forms (relative, `~user`, empty, missing, non-regular, cycle), keys in wrong scope (global-only in criteria, include in criteria, invisible in globals), criteria needing undecided input ("criteria needs --app-name to decide") |
| never invokes makoctl | PASS | no subprocess/os.system/popen/socket/dbus anywhere; the single "makoctl" occurrence is a doc comment (line 36) |

## Behaviors verified correct (no defect)

- Last-occurrence-wins: duplicate global keys (F04 → `Serif 12`), later matching section wins
  (F14 → `BFont`), both-mode sections in order (F07a → `PlayFont`). Manual L435–437.
- Top-of-file keys are globals and apply (F05). Manual L493–497.
- Comments: `#` line inside a section does not close it (F06). Manual L24.
- Include chain: absolute (F02 context), `~/` via `--home` (F10), symlinks to regular files read
  through for both `--config` and include targets (P03 — matches the real lane surface where the
  config is a symlink); cycle refused on a realpath stack without hanging (F01); missing target,
  directory target and FIFO target refused (F02/F03); relative, `~user`, empty includes refused
  (F16/P13/P13b, exact L47–49 authority).
- Criteria matching: all-fields-must-match (F11 combined app-name+mode with only one true → not
  applied); urgency domain enforced with refusal (F08 `urgency=banana`); exact case-sensitive
  string match (P20 `FOO` ≠ `foo`); `[urgency=low]` positive match (P19); quoting, backslash
  escapes, escaped quotes and `]` inside quotes all parse (F13a/b/c, P04); `=` inside a criteria
  value needs no escape (F12 `[app-name=a=b]`); unescaped spaces in criteria refused (P05/P05b,
  L507); `[]` empty criteria matches all (P09, L493–495 "overridden by simply defining the
  criteria yourself"); spaces around `=` accepted in global lines (P07, L581 example).
- Modes: initial list `{default}` — `[mode=default]` applies with no `--mode` and stays enabled
  when other modes are added (P01/P02; L620–621, L633–634).
- CRLF input handled (P15, clean values). Leading-whitespace `#` lines ignored (P14, lenient
  beyond literal L24 — benign). UTF-8 BOM produces a visible refusal, not a silent skip (P16).
- Value validation battery: all ten invalid values refused with precise reasons (P08a–j).

## Observations (manual-silent; no defect claimed)

- O1 Inline `#` is kept in the value: `font=Serif 12 # note` → effective `"Serif 12 # note"` (F06b).
  Literal L24 reading ("lines that begin with # are ignored"). If the frozen cases strip inline
  comments, the cases deviate from the pinned manual, not the tool.
- O2 Include semantics = inline expansion at the directive position; a diamond include re-applies
  the shared file (F17 applied `c.ini` twice, deterministic across reruns, `font=BFont` last wins);
  no dedup. Manual is silent; the model is self-consistent (F01/F17/F21).
- O3 A refused line never aborts resolution: refusals are per-line/per-include and the rest of the
  file still resolves (F01/F02/F18). Consistent with "refusals list" being in-band.
- O4 `invoke-action` with multiple words is accepted (`len(words) >= 2`); the manual shows a single
  `<action>` (L117). Same family as D2, not separately claimed.

## Comparison with the frozen cases (`.ufo/waves/round-87/controls/mako-cases-r87.json`)

The file landed at ~06:39 (poll check in window 2); my expectations had been frozen in scratch
beforehand, so the comparison below is independent in the same sense the scout's authorship was.

Method: my own 20-line replay driver in scratch (`caserun.py`) materializes each case's
`home_files` under a temp home and invokes the tool exactly as the counter's runner does
(`--config <home>/<case.config> --home <home>` plus the case args; counter lines 207, 244–251:
exit-0 required, refusals mode enforced, `expect.effective` is a subset check). The lane counter
itself was NOT executed at the frozen revision. Result: **22/23 PASS; the single FAIL is a defect
in the frozen cases file, not in the tool.**

### G1 — HIGH (blocks TARGET_MET for any correct tool): C13 config path typo

`mako-cases-r87.json`, case `C13-two-sections-only-first-matches`:
`"config": ".config_mako/config"` (underscore) while its `home_files` defines only
`.config/mako/config`. The counter joins home+config raw (c1-r87-mako-criteria.py:207), so the
case invokes the tool on a file that is never materialized. Reproduction (my replay, 06:44):
```
FAIL C13-two-sections-only-first-matches  exit=2
  (mado-mako: setup error: cannot stat --config: No such file or directory)
```
and with `"config": ".config/mako/config"` substituted (everything else identical): `PASS ok`.
Consequence if counted as frozen: candidate correct = 22/23 → score 9.57 → TARGET_MISSED
spuriously, for every faithful tool including a perfect one. The intended path is unambiguous
from the case's own `home_files` and its structural twin C12. Adjudication: typo; resolution is
the L1's call (frozen-artifact procedure) — flagged here so the counter is not run against a
self-defeating control.

### Disagreements between my expectations and the frozen cases (each adjudicated from its pin)

- None on outcomes for the 22 well-formed cases: every case agrees with the expectation I wrote
  beforehand (mapping: C01–C02↔F05, C03↔F11-negative, C04–C06↔P19/F14, C07–C09↔F07, C10–C11↔F11,
  C12↔F14, C13↔F14-negative, C14↔F10, C15↔F21/O2, C16↔F13a, C17↔F13b, C18↔F12, C19↔F06,
  C20↔F16, C21↔P05-family, C22↔P10-family, C23↔F11-positive). Tool behavior also matches all 22.
- C22 wording nuance, no disagreement: the case pins L448 (summary/summary~ conflict) and expects
  `refusals: present`; the tool refuses because `summary` is outside the model before any conflict
  check. Refusal presence — the only thing the predicate checks — is satisfied; the reason string
  differs from the pin's conflict rationale. Cosmetic only.
- C20/C21/C22 `"effective": {}`: initially read as "no keys may change", which no faithful tool
  could satisfy (width=300 legitimately still applies). Adjudicated against the counter source:
  `expect.effective` is iterated as a subset requirement (`for key, want in ...items()`, line
  248), so `{}` means "no key constraints; refusals present only". Consistent; no disagreement.
- Coverage gaps, no disagreement but material: the frozen predicate cannot see D1 or D2. The
  runner always passes `--home` (line 207), so D1's env-`$HOME` fallback never fires; no case
  uses a bare or trailing-token binding action, so D2 never fires. A tool carrying both defects
  still scores 23/23 (with G1 fixed). The defects stand on the declaration contract and the
  manual regardless of the score.
- My probes the cases do not cover, all already verified correct in my batteries: cycle/missing/
  non-regular includes (F01–F03), duplicate keys (F04), inline `#` (F06b, O1), invalid urgency
  section (F08), empty file (F09), `[]` criteria (P09), `mode=default` initial enablement (P01/
  P02, L620–621), symlinked config/include targets (P03), CRLF (P15), BOM (P16), and the full
  value-validation battery (P08a–j).

## Dead steps

- My own fixture bugs, corrected and rerun: F13 used a nonexistent `font-size` key (the tool
  rightly refused it — `font-size` is not a mako option); F15 originally left `home1/decoy.ini`
  absent so it only proved the missing-include refusal; a shell brace slip created a stray empty
  `f340/`. All three fixed; final evidence comes from the corrected runs (F13*-v2, F15*-v2).
- One pipe-ordering stumble in a display command (`2>&1` merged the stderr banner ahead of the
  JSON) — display only, rerun cleanly; not a tool defect.

## Installs

None. No pacman, no uv, no binaries; read-only tooling sufficed.
