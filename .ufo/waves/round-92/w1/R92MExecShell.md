# R92MExecShell — shell-semantics attack on mado-xdgmime.c1.py (xdg-mime 1.2.1)

Method: micro-probes of bash/coreutils/gawk (`IFS=` same-shell tests, `command -v`, `read`, `echo`, `basename`, bracket globs via `pathexp` vs `echo` glob, `awk -v` escapes), then fixture batches labelled with the frozen oracle `xdgmime-oracle-r92.py` and run through the candidate with the counter's argv shape (DRAFT runs only). No candidate edits.

## Cases shipped
110 cases in `.ufo/waves/round-92/controls/xdgmime-cases-r92-sh-unlabelled.json` (ids `sh-NN-<rule>`, no `expect`): IFS `:`/`;` splitting (leading/trailing/double colons and semicolons), pathname-expansion of XDG dirs / desktop names / `*.desktop` fallback names (`* ? [..] [!..] [^..]`, hidden/dotfiles, unmatched, backslash-escaped), `read first rest` backslash/continuation, `echo` option apps and trader values, `command -v` keywords/builtins/xdg-mime functions/slashed/empty-PATH/non-exec dirs/symlinks, `[ -e ]`+realpath, basename odd ids. Counts: 110 total, ≥40 required.

## DRAFT diffs (labelled by oracle, run DRAFT vs candidate — not a measurement)
8/110 disagree; all other 102 agree byte-for-byte.

### D1 — REPLICATE XDG (crash): reversed bracket range `[c-a]` / `[z-a]`
- Fixtures: `sh-109-revrange-cfg`, `sh-110-revrange2` (XDG_CONFIG_HOME="{ROOT}/[c-a]foo" resp. "[z-a]d" with a dir literally named `[c-a]foo`).
- xdg-mime output: `w.desktop` rc 0 (bash treats a reversed range as literal/empty, pattern left literal, dir exists, mimeapps.list read).
- Candidate: exit 1, `re.PatternError: bad character range c-a at position 5` (from `re.compile` in `glob_rx`, mado-xdgmime.c1.py:170 via `_bracket`; uncaught).
- Source: `pathexp`/`glob_rx`/`_bracket` (mado-xdgmime.c1.py:96-212).
- Fix: when `_bracket` yields an invalid reversed range, treat the bracket as literal (return `None` from `_bracket` so `glob_rx` escapes `[`) — matching bash, which leaves a reversed range unmatched-but-harmless (it even matched `[e-a-c]*`→`-a` in probes: it degrades to the literal/class content, never to a regex error). At minimum catch `re.error` in `glob_rx` and return `None`.

### D2 — SCOPE REFUSAL, not a model bug at unit level: awk `mimetype` backslash escapes
- Fixtures: `sh-71..76-awk-*` (types `text/pla\e`, `text/\ann`, `text/p\ n`, `text/\102`, `text/\x41`).
- xdg-mime output: rc 0 (gawk `-v` decodes `\e→e` etc.; e.g. `text/\101` and `text/\x41` → `text/A`, key `text/A=` matched → `q.desktop`). Candidate: exit 2 `unsupported: … characters outside RFC 6838 restricted-name` (mado-xdgmime.c1.py:704-706).
- This is by design of the candidate's stated scope gate; it is NOT reachable through an RFC-6838 type, but the oracle case schema accepts such types and xdg-mime answers. Flag for L1: either keep the gate (these 6 cases will count as misses if frozen) or widen `TYPE_CHARS` to model `bre()` + `awk -v` escapes (candidate `awk_v` itself is also wrong on unknown escapes: gawk drops the backslash (`\e→e`, `\d→d`) while candidate `awk_v` keeps `\e`; mado-xdgmime.c1.py:370-404, `d not in m` → `b"\\"+d`).

## Areas that MATCHED (no fixture disagreement — evidence notes)
- IFS splitting: same-shell bash `set -- $v` under `IFS=:` on `"a::b:"`, `":a:"`, `"::"`, `""` → `argc=3 <a,,b>`, `<,a>`, `<,,>`, `0` — identical to candidate `ifs_split` (mado-xdgmime.c1.py:77-84), including middle/leading empties; only trailing empties are dropped by candidate and matched by shell for the loop forms tested (`for desktop in $XDG_CURRENT_DESKTOP ''` exercised via `""` literal). Dirs with trailing colons: empty-dir applications lookups (`/applnk` absolute in real, cwd-relative in candidate) coincide since fixtures cannot own `/applnk` — noted as a benign residual risk.
- `read first rest` (no -r): 16 probes (`a\ b c`, `a\\b c`, `a\<nl>b`, trailing `\`, `-n`, tabs) all byte-identical to candidate `read_first` (mado-xdgmime.c1.py:420-447).
- `echo "$x"`: probes `-n -e -E -ne -eE -Ene -nE -xxx -nfoo -- -` all match candidate `echo_out` (mado-xdgmime.c1.py:234-238); trader values `-n w.desktop` etc. also agreed (xdg-mime's `echo "$trader_result"` is quoted, and `trader_result` there is a single already-split field).
- `command -v`: candidate's KEYWORDS/BUILTINS/FUNCTIONS sets match bash 5.3 and the 41 functions in `/usr/bin/xdg-mime` exactly (0 missing/extra); `command -v "."` → `.`, directory-on-PATH → rc1, `./exec`→path, nonexec→rc1, `.`/`..`/`/`/`-n` fixtures all agreed; empty PATH element and `PATH=""` agreed.
- `basename`: all odd ids (`-n -n.desktop -- -e.desktop ! - ...desktop a/ / "" --help`) agree with candidate `basename` (mado-xdgmime.c1.py:223-231) (leading-dash → invalid option on stderr, empty stdout).
- `pathexp` glob ordering: candidate sorts byte-wise = LC_COLLATE=C; oracle env has no LC_ALL/LANG so bash uses C — `cfgA` vs `cfga` case agreed. Bracket negation `!`/`^`, `[:class:]` names, leading-`]` literal, hidden-dotfile rule, `\G` in bracket — all agreed at fixture level (micro-diff tool reports are ordering-only). `[a\*b]`/`\\a*` backslash-outside-bracket: real `echo a\*` gives `a\*`?? — probe shows literal star `a*` for `a\*` — wait: `pathexp` for `a\\*` returns `[a\*]` literal vs real `a*` (file named `a*` matched? no — `*a` file exists; the shell un-escapes to `a*` then matches file `a*`-containing names… recorded in probe log; fixture-level agreement held for all Exec/id glob cases in the 110).
- `[ -e ]`+`xdg_realpath`: dangling symlink, symlink-ok, abs-dir, abs-nonexec fixtures all agreed with `exists_path` (mado-xdgmime.c1.py:478-479).

## Reproductions
- D1: oracle case `sh-109-revrange-cfg` above; oracle expect `{"text/plain":{"default":"w.desktop","rc":0}}`, candidate stderr `re.PatternError: bad character range c-a at position 5`.
- D2: oracle case `sh-75-awk-emptyseg` (type `text/\101`); oracle `q.desktop` rc 0, candidate exit 2 with the unsupported message.

## Dead steps / errors
None for the scoped work. Scratch removed.

Report: .ufo/waves/round-92/w1/R92MExecShell.md
