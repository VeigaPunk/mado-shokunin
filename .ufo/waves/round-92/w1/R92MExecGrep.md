# R92MExecGrep — GREP/AWK/TEST falsifiers (DRAFT, v1 wave, round 92)

Seat: `R92MExecGrep`. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Owned files: report `.ufo/waves/round-92/w1/R92MExecGrep.md` (this file) and
`.ufo/waves/round-92/controls/xdgmime-cases-r92-gr-unlabelled.json` (49 cases,
`expect` written by the oracle, not by hand).
Supporting evidence copied to the same directory: `R92MExecGrep-cases-labelled.json`
(identical content), `R92MExecGrep-disagreements.json` (machine-readable disagreement list).

All runs below are **DRAFT** (materialised oracle fixtures, `--json` candidate runs, scratch
under `/fast/scratch/hyaku/mado-r92/R92MExecGrep`, deleted after copying evidence into
`.ufo/waves/round-92/w1/`). Nothing was written under `…/round-92/receipts/`.
Candidate not edited; the only lane writes are the two owned files plus the two evidence
copies named above.

## Method (DRAFT)

- Wrote 49 oracle-schema cases (ids `gr-01`…`gr-49`, one `types` entry each, `expect` omitted):
  20 BRE-family (`grep "$MIME="` on `defaults.list`/`mimeinfo.cache`), 5 cut/path/order-family,
  13 InitialPreference/`test -gt` family, 10 `check_mimeapps_list` `gawk -v` family, 1 BRE-vs-AWK
  escape-parity control.
- Labelled with `controls/xdgmime-oracle-r92.py label` (installed `/usr/bin/xdg-mime`,
  `query default` form only; rc=0, "labelled 49 cases").
- Ran the candidate `build/mado-xdgmime.c1.py` on each materialised fixture, mirroring the C1
  counter's shape (`--json`, whole case env via `--env`, root as cwd; root shared with the
  oracle materialisation, so `{ROOT}`-dependent answers are comparable).
- Result (DRAFT): **14 disagreements / 49**, **35 agreements** (which include 18 deliberate
  agree-controls). Everything in §1–§3 is a disagreement; §4 is agreements worth noting
  (controls that pin behaviour, so an L1 fix must not change them).

Source pins (DRAFT, computed this session): cases file sha256
`3aac5688f6016133…`, candidate sha256 `4121d583d42fd5ee…` (first 16 hex only; full hashes
in the receipts/evidence files).

## 1. BRE translation (`bre()`, candidate lines 272–367) — 8 disagreements

Real behaviour was established both by the oracle labels (installed xdg-mime/grep) and by
direct `grep` probes this session (GNU grep 3.12, C locale).

### gr-01 `text/a**`, cache `text/aaa=z.desktop;` — stacked `*`
Oracle: `z.desktop` (rc 0). Candidate: `None` (rc 0).
`bre()` emits `text/a**=`; Python `re` raises "multiple repeat", so `bre()` returns `None`
(candidate 364–367) and the file is skipped. GNU grep applies the second `*` to the
already-quantified atom (`(a*)*`) and matches. Same family, all disagreements:
- **gr-03** `text/a\{2\}\*` + `text/aa=z.desktop;`: oracle `z.desktop`, candidate `None`
  (`a{2}*` = "multiple repeat" in Python).
- **gr-04** `text/a\+\+ab` + `text/aaab=z.desktop;`: oracle `z.desktop`, candidate `None`
  (Python 3.14 compiles `a++` as possessive; possessive cannot backtrack, so `a++ab` does not
  match `aaab=`, whereas GNU `(a+)+` can give back and matches).
- **gr-14-caret-mid / gr-15-dollar-mid / gr-13-star-at-type-start / gr-17-bracket-class /
  gr-18-dot-not-slash / gr-19-star-zero / gr-20-slash-esc** (gr-13…gr-20) all **agree** with
  the oracle, so only stacked quantifiers are broken in this direction.

Proposed fix (for the L1; candidate untouched): emulate GNU's "quantifier applied to an
already-quantified atom" by wrapping the repeated atom in a non-capturing group when another
quantifier follows (e.g. `(?:a*)*`, `(?:a{2})*`, use greedy `+` rather than Python
possessive `++`), instead of letting Python reject/short-circuit.

### gr-05 / gr-06 / gr-07 — `\{…\}` at an atom position GNU grep treats as literal
- **gr-05** type `\{2}x/y`, line `{2}x/y=w.desktop;`: oracle `w.desktop`, candidate `None`.
- **gr-06** type `^\{2}x/y` (anchor then brace): oracle `w.desktop`, candidate `None`.
- **gr-07** type `\(\{2}x\)/y` (group start then brace): oracle `w.desktop`, candidate `None`.
Direct probe: `grep '\{2\}x='` prints `warning: stray \ before {` and matches the literal
line `{2}x=…` (rc 0). Candidate `bre()` returns `None` on `{…}` whenever `at_start` is true
(candidate 302), i.e. at pattern start, after `^`, and after `\(`, so all three files are
skipped. Note the `\{…\}` immediately after `^` must be literal even though `^` is an anchor.

Proposed fix: emit a literal `\{…\}` (escaped) instead of `None` when `at_start`; keep
invalid content (`\{a\}`, `\{\}`, unterminated) as a grep rejection (`None`), which
gr-11/gr-10 show is already handled consistently (gr-11 agrees; gr-10 below is the reverse).

### gr-10 — empty `\{\}`: candidate matches, GNU grep rejects
Type `text/x\{\}`, line `text/x{}=w.desktop;`. Oracle: `None`. Candidate: `w.desktop`.
Candidate validates `rx` with `re.fullmatch(rb"\d*(,\d*)?", …)` (candidate 302), which
**accepts the empty string**, emits `{}`, and Python `re` treats invalid `{}` literally, so
it matches. GNU grep: `Invalid content of \{\}` (rc 2) — no match anywhere on the path.

Proposed fix: require at least one digit on one side (`\d+(,\d*)?` or `\d*,\d+`), mirroring
GNU's "at least one bound" rule; `\{,\}`/empty then returns `None` like the other
invalid-brace cases (gr-11 agreement then covers both).

### gr-12 — huge bound: candidate crashes with an uncaught traceback
Type `text/a\{999999999999999999999\}`, cache `text/a=z.desktop;`. Oracle: `None`, rc 0
(GNU grep: `Regular expression too big`, no match, function continues).
Candidate: **rc 1, traceback `OverflowError: the repetition number is too large`** at
`bre()` line 365 — `bre()` catches `re.error` but not `OverflowError`, so the tool exits
1 with a traceback instead of answering `None`/rc 0. Exit-code and stdout-contract
violation, not just a wrong answer.

Proposed fix: catch `OverflowError` (or bound the count pre-parse, e.g. `> 2**31` ⇒ `None`)
in `bre()`; cost is trivial.

### gr-08 / gr-09 — collating `[.a.]` / equivalence `[=a=]` are not modelled (candidate inverts)
- **gr-08** type `text/[[.a.]]`, line `text/.=w.desktop;`: oracle `None`, candidate
  `w.desktop` (BRE `[[.a.]]` in GNU grep is the collating element for `a` only; candidate
  `_bracket` has no `[.` path, so it builds the Python class `[\\[\\.a\\.]\\]` which also
  contains `.`, `[`, `]`).
- **gr-09** type `text/[[=a=]]`, line `text/.=w.desktop;`: oracle `None`, candidate
  `w.desktop` (same reason, equivalence class).
Stock probe this session: `grep '[[.a.]]=b'` matches `a=b`; candidate class would also match
`text/.=…`.

Proposed fix: parse `[. … .]` as the single enclosed character and `[= … =]` as the single
enclosed character (C locale), before falling back to literal parsing.

### Control agreements in this family
gr-02 (stacked-star miss), gr-11 (`\{a\}`), gr-13 (`*x/y` literal), gr-14 (`x^y/z`),
gr-15 (`x$y/z`), gr-16 (`text/\1x` invalid backref → no match both), gr-17 (ordinary bracket
class), gr-18 (`.` matches any char incl `/`), gr-19 (`*` can be empty), gr-20 (`\/` stray
backslash = literal `/`), gr-49 (`\q` in the **grep** leg = literal `q` — agrees, and
contrasts with §2). Unescaped `)` is literal in both (probed: `grep 'a)b='` matches) and
`\(...\)`/unbalanced-`\(`, `\8`→"Invalid back reference", `\c`→stray-`\`-literal were all
probed and are already consistent.

## 2. `awk -v` escape processing (`awk_v()`, candidate 370–404) — 6 disagreements

GNU gawk 5.4.1 probe: for an unknown escape it warns and emits the **plain character**
(backslash dropped) — e.g. `-v v='a\qb'` → `aqb`, `\e` → `e`, `\$` → `$`, `\ ` → ` `,
`\/` → `/`, and `\x` with no hex digits → `x` (`warning: no hex digits in \x escape sequence`).
Candidate `awk_v` instead emits `\\` + the character for anything not in its map and not
octal/`\x` (candidate 401–403), so in `check_mimeapps_list` it looks up a key that still
contains a backslash and never finds the installed line. All six are one bug:

- **gr-39** `text/x\qb` ↔ file key `text/xqb` — oracle `a.desktop`, candidate `None`.
- **gr-40** `text/x\$y` ↔ `text/x$y` — oracle `a.desktop`, candidate `None`.
- **gr-41** `text/x\ey` ↔ `text/xey` — oracle `a.desktop`, candidate `None`.
- **gr-42** `text/x\ y` ↔ `text/x y` — oracle `a.desktop`, candidate `None`.
- **gr-44** `text/x\xzy` ↔ `text/xxzy` — oracle `a.desktop`, candidate `None` (candidate
  emits `\x` verbatim when no hex digits follow, candidate 396–397).
- **gr-47** `text/x\zy` ↔ `text/xzy` — oracle `a.desktop`, candidate `None`.

**gr-43** (`text/x\/y` ↔ `text/x/y`) **agrees** because the candidate happens to map `\/`
explicitly (candidate 374) — but gawk treats it as an *unknown* escape (plain `/`), so the
fix below must preserve that observable.

Known-escape agreements (probed and oracle-confirmed): gr-46 (`\t` → real tab), gr-48
(`\\` → single backslash), octal ≥4 digits (`\7777` → `0xff` + `7`, gr-45, oracle `None` /
candidate `None` — the file key was built with `U+00FF` and neither side matches), `\0`
keeps a NUL inside the string in both.

Proposed fix: replace the unknown-escape branch with "emit the character alone (drop the
backslash)" for every byte not in the map, and for `\x` with no hex digits emit plain `x`.
This is one-line in each spot (candidate 396–403) and is pinned byte-for-byte by the
gawk probes above.

## 3. InitialPreference / integer compare (`initial_preference` + `bash_int`) — 0 disagreements, one trap

13 cases, all oracle/candidate **agree**: octal-looking values `010`/`0123` vs `9`/`100`
(gr-26/27/36), leading space / trailing space / tab / `+5` (gr-29/30/31/37), two
`InitialPreference` lines (gr-32), `X-InitialPreference` only (gr-33), `5=0` (gr-38),
int64 boundary `9223372036854775807` vs `9223372036854775808` (gr-34/35), `08` vs `7`
(gr-28). Two traps the L1 must not "fix":
- bash's `[ … -gt … ]` is **decimal** (probed: `[ 0010 -eq 10 ]` and `[ 0123 -eq 123 ]` true),
  so `bash_int`'s decimal parse is already right; an octal "fix" would break all three
  octal cases.
- The `0` prefix in `pref="0$(…)"` (defapp_fallback) makes signs and interior whitespace
  fail the same way in both — and the candidate's fullmatch (candidate 407–417) already
  reproduces every malformed shape this seat produced.

## 4. `cut`/path/order family — 0 disagreements

All five agree, including the ugly paths:
- **gr-21** data dir literally named `share=` (via `XDG_DATA_DIRS={ROOT}/share=`): both
  oracle and candidate return the `cut`-garbage `'/applications/defaults.list:text/plain'`
  (the `=` in the path makes `cut -d= -f2` return filename+type text) — a genuine
  xdg-mime quirk, reproduced faithfully.
- **gr-22** value `a=b;c.desktop;` → both `a` (`cut -d= -f2` = field 2 only).
- **gr-23** first-file-only-then-second: `defaults.list` wins `head -1` order over the cache.
- **gr-24** `XDG_MENU_PREFIX=lxde-`: prefixed file is tried first in its dir (oracle picks
  `m.desktop` from `lxde-defaults.list` over the unprefixed file in the same dir).
- **gr-25** first data dir wins over the second regardless of filename.

Also verified by probe but not turned into cases (no divergence found): `:` in a path is
inert for `cut` (and unreachable for dir names, since `XDG_*_DIRS` splits on `:`), grep
with two operands prints `file:line` exactly as the candidate models, empty `=` values,
and the fact that candidate `bre()`/`grep_lines` treat a `grep` rc=2 (invalid pattern) as
"no hits" just like the shell pipe does.

## 5. Not found / out of scope notes

- `grep -l "$MIME;"` + `awk -F= '/InitialPreference=/ {print($2)}'` + `[ -gt ]` pipeline in
  `defapp_fallback` otherwise agrees (multiple files, `X-InitialPreference`, nested dirs,
  names with spaces are L1-covered b-cases b03–b16 and were not duplicated).
- Binary file / NUL in a `defaults.list`/`mimeinfo.cache`: GNU grep prints
  `Binary file <path> matches` which `cut -d= -f2` passes through whole and becomes the
  printed default; the candidate raises `Unsupported` at `readfile` (candidate 254–255).
  This is a known-conservativeUnsupported in the candidate (not a wrong answer), so no case
  was minted for it — but the L1 should decide whether a NUL-bearing cache file is in the
  "must model" class; if it is, grep's binary-file line is the byte sequence to emit.
- Installs: **none** (pacman was not used; all probes used the preinstalled `/usr/bin/grep`,
  `/usr/bin/gawk`, `/usr/bin/bash`, python3 in this environment; nothing needed installing).

## Checks run (DRAFT, exit codes)

- Generator (`gen-gr.py`, scratch): wrote 49 cases, rc 0.
- Oracle `label` (twice, after one fixture correction gr-17): rc 0, "labelled 49 cases".
- Candidate differential harness (`run-cand.py`, scratch; materialise + oracle `env_of` +
  `--json` candidate run per case): after fixing my first harness's `--env` flag passing
  (rc 2 "PATH unset" on 49/49 — a harness bug, not a candidate result), **14 disagreements /
  49** (rc 0). Machine-readable list: `.ufo/waves/round-92/w1/R92MExecGrep-disagreements.json`.
- Direct probes this session recorded in §§1–3 are `grep`/`gawk`/`bash` one-liners against
  scratch files; the load-bearing ones were also confirmed end-to-end by the oracle labels.

## What the L1 should do with this

Take cases gr-01, gr-03, gr-04, gr-05, gr-06, gr-07, gr-08, gr-09, gr-10, gr-12,
gr-39–gr-42, gr-44, gr-47 as falsifier cases in their own right (they are labelled by the
installed xdg-mime above); the 14 disagreeing cases plus the 35 agreeing controls are all in
the owned JSON file in oracle schema. Suggested candidate fixes, in order of severity
(crash → silently-wrong-hit → silently-missed-hit): gr-12 `OverflowError` catch, gr-10
`\{\}` validity, gr-05/06/07 literal-`\{…\}`-at-start, gr-01/03/04 stacked quantifiers,
gr-08/09 collating/equivalence classes, gr-39–gr-47 unknown-escape dropping in `awk_v`.

Report: .ufo/waves/round-92/w1/R92MExecGrep.md
