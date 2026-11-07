# R92MMutC1 — mutation probe of the C1 candidate (mado round 92, wave w1)

Role: UFO-FSD mutation tester. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision
`d992ef7494b054591ee9104df1da49264678df5d`. Assignment: mutation-test the C1 candidate
`.ufo/waves/round-92/build/mado-xdgmime.c1.py` against the labelled L1 cases
`.ufo/waves/round-92/controls/xdgmime-cases-r92-l1.json`.

**Object probed (pin).** The candidate was being edited by its owner during this probe (752 lines at first
read → 761 → 834 lines). My mutants, scoring and counter draft runs are pinned to the byte snapshot
`084bce8ce45b7637b0f3bf39c3b6208e04093032f5db19441bff744557c6cfec` (834 lines), captured in scratch and
identical to the live file at the end of the probe. The candidate was **never written by this seat**: all
mutations are find/replace copies, and the live file's hash history is the owner's.

## Deliverables (owned)

| file | sha256 |
|---|---|
| `.ufo/waves/round-92/controls/xdgmime-mutants-r92-mc.json` | `0c0e0905eea9732fa829c3ddbf81c85e60f18249667e7d3efb492186fb5d8807` |
| `.ufo/waves/round-92/controls/xdgmime-cases-r92-mc-unlabelled.json` | `a068080851a46ca56f75327342d2fb3b65a1f106559dd9de36ca3950a241f605` |
| this report | — |

## Method / detector

- Detector: the frozen predicate PRED-C1-r92-v1, executed by
  `quality/counters/c1-r92-xdgmime-default.py` in **DRAFT** mode (`--draft-tool`; exit 3). Case correctness is
  `run_tool` equality of `{type: {default, rc}}` against the stored `xdg-mime` labels; a mutant is killed only
  when it returns a well-formed wrong answer (`wrong`), never by a crash alone (QUALITY 148).
- For per-case detail (which case kills which mutant; L1 fragility) I reused the counter's own
  `run_tool`/`correct`/`sandbox_argv` through an import harness in scratch (`harness.py`), so every score below
  was produced under the same bwrap sandbox (xdg-utils, shells and the lane hidden) as the counter.
- Mutants: 43 new, each a single find/replace whose `find` occurs exactly once in the pinned candidate and whose
  mutant compiles (`gen-mutants.py` assertion run: `mutants 43 bad []`, rc 0). Each flips one modelled rule that
  no L1 mutant (M01–M40) flips.
- Cases: 14 new killing cases in the oracle schema (unlabelled in the owned file; labelled copies in scratch with
  `xdgmime-oracle-r92.py`; `mc` group). All 14 labels were produced by the installed `/usr/bin/xdg-mime`; the
  counter's oracle re-labelled them at run time (`oracle_agree = 142/142`). The supplied draft argv fixes `--fresh 60` (the predicate proper uses 120); every run here is a DRAFT run, not a measurement.

## Result — 43 mutants against the frozen L1 cases (128)

`killed 30`, `survived 13` (the draft counter reports the 13 as `crashed-not-killed` only because the
**candidate itself** exits 2 on four L1 cases — a shared baseline failure, not 13 real crashes; see F1/F3).
No mutant is killed only by a case the candidate itself fails (checked by subtracting
`f14,f17,g05,g06` from every `wrong_ids`: the result was empty).

Counter summary, draft run 1 (verbatim):
```
MADO_XDGMIME_DEFAULT: DRAFT_TARGET_MISSED pred=PRED-C1-r92-v1 rev=draft:/fast/scratch/hyaku/mado-r92/R92MMutC1/candidate-live-084bce8c.py base_rev=d992ef7494b054591ee9104df1da49264678df5d cases=128 correct=124 b=16/16 d=39/39 f=19/21 g=4/6 m=36/36 s=10/10 answered=124/128 fresh=60/60 fresh_seed=139185804 mutants=43 killed=30 crashed_not_killed=13 oracle_agree=128/128 do_nothing_correct=33 naive_mimeapps_correct=44 glib_resolver_correct=59 base_tool_correct=0 base_tool=absent tool_sha256=084bce8ce45b7637b0f3bf39c3b6208e04093032f5db19441bff744557c6cfec
```

| mutant | rule flipped | verdict on L1 | wrong | killing case(s) (L1) |
|---|---|---|---|---|
| MC01 | echo: only an exact -n argument suppresses the newline (other flag words print) | killed | 1 | f10-echo-dash-e |
| MC02 | command -v: a name containing / is resolved as a path, never through PATH | killed | 2 | d07-exec-absolute, d17-exec-relative-cwd |
| MC03 | command -v: an empty PATH element means the working directory | killed | 1 | d35-path-empty-element |
| MC04 | command -v: xdg-mime's own function names resolve to the bare name | killed | 1 | d25-exec-function-name |
| MC05 | command -v: reserved words resolve to the bare name | killed | 1 | d26-exec-keyword |
| MC06 | command -v: a PATH hit is the path printed, and it is that path that must exist | killed | 51 | m01-user-default-installed, m03, m04 (+48) |
| MC07 | install check: XDG_DATA_HOME defaults to $HOME/.local/share | killed | 1 | d31-data-home-unset |
| MC08 | vendor split: the app part starts after the FIRST dash while the vendor stops before the LAST | killed | 1 | d02-vendor-two-dashes |
| MC09 | a readable vendor-path desktop file suppresses the flat/subdir search | killed | 1 | d32-vendor-and-flat |
| MC10 | applications subdirectories are searched in sorted order | killed | 1 | d05-subdir-order |
| MC11 | the *.desktop scan visits names in sorted order | killed | 1 | b03-tie-first-sorted |
| MC12 | the mimeapps key match includes the trailing = | killed | 53 | m01, m04, m05 (+50) |
| MC13 | check_mimeapps_list echoes the list token, not its basename | killed | 1 | d22-id-with-slash |
| MC14 | desktop-specific mimeapps.list files are tried before the plain one | killed | 1 | m05-desktop-specific-first |
| MC15 | defaults.list is consulted before mimeinfo.cache | killed | 1 | f03-defaults-before-cache |
| MC16 | the defaults/cache search includes the first (user) data dir | killed | 1 | f15-data-home-first |
| MC17 | the MimeType scan searches for the type WITH its trailing semicolon | killed | 1 | b14-type-without-semicolon |
| MC18 | the fallback preference starts below zero, so a zero preference can win | killed | 9 | b01, b03, b04 (+6) |
| MC19 | the fallback preference is read as 0 followed by the InitialPreference text | killed | 9 | b01, b03, b04 (+6) |
| MC20 | the fallback prints the basename of the selected desktop file | killed | 13 | b01, b02, b03 (+10) |
| MC21 | LXQT_SESSION_CONFIG selects the LXQt session | killed | 1 | s03-lxqt-session-config |
| MC22 | --version prints the xdg-utils version string | killed | 1 | s08-version |
| MC23 | a type starting with - is a syntax error with rc 1 | killed | 1 | s06-leading-dash |
| MC24 | read strips leading IFS whitespace before the first word | killed | 1 | d27-exec-leading-ws |
| MC25 | a data dir's mimeapps.list lives under applications/ | killed | 2 | m19, m23 |
| MC26 | a mimeapps value keeps a leading space | killed | 1 | m26-list-space-kept |
| MC27 | the first matching defaults/cache line of the combined grep output is used | killed | 1 | f08-empty-value-moves-on |
| MC28 | the defaults/cache answer is the first ; field | killed | 11 | f01, f02, f05 (+8) |
| MC42 | an absolute word in pathname expansion stays absolute | killed | 1 | g04-config-dirs-glob |
| MC44 | the defaults/cache grep pattern ends with the = of the key | killed | 1 | f21-first-match-wins-line |
| MC29 | basename strips trailing slashes | survived L1; killed by | 0 | **mc-29-basename-trailing-slash** |
| MC30 | the MimeType scan lists a directory's *.desktop files before recursing into subdirectories | survived L1; killed by | 0 | **mc-30-scan-files-before-subdirs** |
| MC31 | config home is consulted before config dirs | survived L1; killed by | 0 | **mc-31-config-home-before-dirs** |
| MC32 | read stops at the first newline of the Exec pipeline | survived L1; killed by | 0 | **mc-32-first-exec-line-empty** |
| MC33 | a bash test integer outside int64 is not a number | survived L1; killed by | 0 | **mc-33-int64-overflow-pref** |
| MC34 | BRE: ^ anchors only at the start of the pattern | survived L1; killed by | 0 | **mc-34-bre-caret-mid** |
| MC35 | BRE: $ anchors only at the end of the pattern | survived L1; killed by | 0 | **mc-35-bre-dollar-mid** |
| MC37 | pathname expansion does not match hidden names unless the pattern starts with a dot | survived L1; killed by | 0 | **mc-37-glob-skips-hidden** |
| MC38 | InitialPreference is awk field 2 (between the first and second =) | survived L1; killed by | 0 | **mc-38-initial-pref-field-two** |
| MC40 | glob bracket: both ! and ^ negate | survived L1; killed by | 0 | **mc-40-glob-bracket-caret-negates** |
| MC41 | the MimeType scan only visits *.desktop names | survived L1; killed by | 0 | **mc-41-scan-only-desktop-suffix** |
| MC43 | pathname expansion yields names in sorted order, so the first matching dir is used | survived L1; killed by | 0 | **mc-43-glob-expansion-order** |
| MC45 | field splitting keeps empty middle fields of a :-list | survived L1; killed by | 0 | **mc-45-empty-middle-desktop** |

Note: MC01 is a refinement adjacent to L1 M12 (which disables all echo flag handling); it is kept because it
isolates the `-[neE]+` word rule, and it is killed by a different requirement (only an exact `-n` suppresses).

## Killing cases for the 13 survivors (labelled by `/usr/bin/xdg-mime`)

The owned cases file is unlabelled; these labels were produced by the oracle in scratch and re-checked by the
counter's fresh oracle pass (`oracle_agree=142/142`).

| case | oracle label for the asked type | kills |
|---|---|---|
| mc-29-basename-trailing-slash | text/plain → `x.desktop/` (rc 0) | MC29 |
| mc-30-scan-files-before-subdirs | text/plain → `a.desktop` (rc 0) | MC30 |
| mc-31-config-home-before-dirs | text/plain → `a.desktop` (rc 0) | MC31 |
| mc-32-first-exec-line-empty | text/plain → `None` (rc 0) | MC32 |
| mc-33-int64-overflow-pref | text/plain → `b.desktop` (rc 0) | MC33 |
| mc-34-bre-caret-mid | text/^x → `d.desktop` (rc 0) | MC34 |
| mc-35-bre-dollar-mid | text/$x → `d2.desktop` (rc 0) | MC35 |
| mc-37-glob-skips-hidden | text/plain → `None` (rc 0) | MC37 |
| mc-38-initial-pref-field-two | text/plain → `a.desktop` (rc 0) | MC38 |
| mc-40-glob-bracket-caret-negates | text/plain → `cy.desktop` (rc 0) | MC40 |
| mc-41-scan-only-desktop-suffix | text/plain → `a.desktop` (rc 0) | MC41 |
| mc-43-glob-expansion-order | text/plain → `a.desktop` (rc 0) | MC43 |
| mc-44-trader-key-ends-equals | text/plain → `real.desktop` (rc 0) | MC44 (already killed by f21; extra coverage) |
| mc-45-empty-middle-desktop | text/plain → `m.desktop` (rc 0) | MC45 |

Verification per survivor (mutant run against its case, sandboxed): every survivor returned a wrong answer,
every base candidate returned the labelled answer; asserted `ALL KILLED`. Counter draft run 2 (L1 + the 14 mc
cases) confirms at set level:
```
MADO_XDGMIME_DEFAULT: DRAFT_TARGET_MISSED pred=PRED-C1-r92-v1 rev=draft:/fast/scratch/hyaku/mado-r92/R92MMutC1/candidate-live-084bce8c.py base_rev=d992ef7494b054591ee9104df1da49264678df5d cases=142 correct=138 b=16/16 d=39/39 f=19/21 g=4/6 m=36/36 mc=14/14 s=10/10 answered=138/142 fresh=60/60 fresh_seed=139185804 mutants=43 killed=43 crashed_not_killed=0 oracle_agree=142/142 do_nothing_correct=35 naive_mimeapps_correct=48 glib_resolver_correct=61 base_tool_correct=0 base_tool=absent tool_sha256=084bce8ce45b7637b0f3bf39c3b6208e04093032f5db19441bff744557c6cfec
```
`candidate --selftest` (DRAFT): `MADO_XDGMIME_SELFTEST: checks=12 failed=0`, rc 0.

## L1 mutant fragility (39 L1 mutants × 128 L1 cases, same detector)

22 of 39 L1 mutants are killed by **exactly one** case (single point of failure):

| mutant | only killing case | mutant | only killing case |
|---|---|---|---|
| M03 | m15-second-default-section | M24 | b06-x-initial-preference |
| M04 | m10-header-trailing-text | M26 | s04-flatpak-overrides-lxqt |
| M05 | m09-first-line-only-in-file | M27 | s05-no-slash |
| M06 | m36-leading-space-key-equals-app | M29 | m16-crlf-value |
| M07 | d02-vendor-two-dashes | M30 | d33-hidden-subdir-skipped |
| M08 | d04-subdir-search | M31 | d23-id-leading-dash |
| M13 | d36-exec-relative-not-executable | M33 | b04-subdir-recursion |
| M14 | d37-path-only-nonexec | M34 | b09-hidden-file-ignored |
| M19 | f05-regex-dot | M35 | b10-space-in-name |
| M21 | f08-empty-value-moves-on | M38 | d39-vendor-applnk |
| M23 | b11-cr-pref | M40 | d12-exec-quoted |

Distribution of kill counts: 1→22, 2→8, 3→4, 4→1 (M15), 6→1 (M01), 14→1 (M20), 48→1 (M02), 0→1 (M36).
**M36 is a survivor on the L1 cases** (0 wrong): with the candidate's RFC-6838 type restriction, `awk_v` is the
identity on every legal type, so only the backslash-typed cases g05/g06 could kill it — and those are exactly
the cases the tool refuses (F1). The L1 mutant set currently contains a mutant that the case set cannot kill.

## Findings (file:line + reproducing input)

**F1 — the candidate refuses four frozen L1 cases.** `build/mado-xdgmime.c1.py:71,711` (`TYPE_CHARS`,
`if not TYPE_CHARS.fullmatch(mime)`) exits rc 2 for any type with a character outside `[A-Za-z0-9!#$&^_.+/-]`.
Four L1 cases ask such types and their labels are the real xdg-mime's answer:
- `f14-invalid-regex`, type `text/[`: xdg-mime → `None`, rc 0; tool → rc 2 `unsupported`.
- `f17-star-in-type`, type `text/p*lain`: xdg-mime → `st.desktop`, rc 0; tool → rc 2.
- `g05-awk-v-escape`, type `text/x\tz`: xdg-mime → `a.desktop`, rc 0; tool → rc 2.
- `g06-awk-v-escape-defaults`, same type: xdg-mime → `t.desktop`, rc 0; tool → rc 2.
Consequence: `correct == cases` cannot hold while both the tool scope and these cases stand; the declaration's
predicate will be `TARGET_MISSED` by construction unless the L1 re-scopes the cases (or the tool). Fresh leg is
unaffected (the fuzz generator emits only legal types: `fresh=60/60`).

**F2 — L1 mutant M32 no longer applies to the live candidate.** M32's `find`
`    if not any(ch in word for ch in b"*?["):\n        return [word]` occurs **0** times: the candidate replaced
it with a backslash-aware `if not re.search(rb"(?:^|[^\\])(?:\\\\)*[*?[]", word):` at `:182`. The counter returns
`MADO_XDGMIME_DEFAULT: SETUP_ERROR mutant M32: find occurs 0 times`; the L1 must regenerate M32 (or the file must be reverted) before
freezing. All 43 of my mutants still occur exactly once in the live file.

**F3 — baseline failure contaminates the crash counter.** Because of F1 the base tool exits 2 on the same four
cases for every mutant, so the counter reports `crashed=4` for *every* surviving mutant
(`crashed-not-killed`). The 13 survivors are genuine survives: after excluding `f14,f17,g05,g06` their wrong
counts are all 0. This is an artifact of the pinned case set, not of the mutants.

**F4 — live-edit churn during the probe.** The candidate changed twice under the probe (752 → 761 → 834 lines):
the RFC-6838 scope sentence + guard, an RFC-6838-aware `pathexp` early return, and a `--selftest`. My pin is
`084bce8c…`; the L1 must re-run the counter's find-count check against the final bytes at freeze. (Both my
snapshots scored identical verdicts: the 43 mutant verdicts on the older 761-line snapshot and the 834-line
snapshot are the same.)

## Commands run (all DRAFT; no measurement, no receipt written)

| command | rc |
|---|---|
| `python3 harness.py candidate <L1 cases> candidate-live-084bce8c.py` → `n=128 correct=124 wrong=f14,f17,g05,g06` | 1 |
| `python3 harness.py mutants <L1 cases> xdgmime-mutants-r92-mc.json candidate-live-084bce8c.py` → killed 30/43 | 0 |
| `python3 harness.py candidate <mc labelled 14> candidate-live-084bce8c.py` → `correct=14/14` | 0 |
| per-survivor mutant × its mc case (sandboxed) → `ALL KILLED` | 0 |
| `python3 gen-mutants.py` (43 finds ×1, all compile) → `mutants 43 bad []` | 0 |
| `python3 -I candidate-live-084bce8c.py --selftest` → `checks=12 failed=0` | 0 |
| counter draft run 1 (L1 cases, 43 mutants, `--fresh 60`, `--scratch-root $S/c1c`) → `DRAFT_TARGET_MISSED … killed=30 crashed_not_killed=13` | 3 |
| counter draft run 2 (L1+mc cases, `--fresh 60`, `$S/c1d`) → `… cases=142 correct=138 mc=14/14 mutants=43 killed=43 …` | 3 |

Pins used by both counter runs: cases L1 `d51999…`, mutants `0c0e09…`, oracle `e51603…`, fuzz-gen `891704…`,
bins `a58710…,c14c8f…,19280b…,3ac644…,5f6c63…,a21add…` (xdg-mime, bash, grep, gawk, realpath, basename);
draft tool `b6497a0a…` (run 1/2 on the 761-line snapshot) and then `084bce8c…` (re-runs quoted above).

## Host safety / restoration / cleanup

- `xdg-mime` was only ever invoked as `xdg-mime query default TYPE` by the oracle; no `xdg-mime default`,
  `install`, `update-desktop-database`, `gio`, `xdg-open` or application launch was run. Fixtures are `env -i`
  trees rooted under scratch.
- The candidate, controls, counters, cases and every lane file outside my three owned paths were not written.
  No mutating git/jj command was run. No install was made.
- Scratch `S=/fast/scratch/hyaku/mado-r92/R92MMutC1` is deleted after this report; the snapshots and logs it
  held were excerpts only, and every cited number is quoted above.
