# R89MScribeEntry — round 89, wave w1 (scribe entry)

Seat: R89MScribeEntry (scribe). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Base revision: `af998dcc41d48618ffe7afe0efc9354755a9244e` (master). Hyaku run 15, round 89, attempt 1, wave w1.
Assignment: two drafts in this file — (1) a knowledge entry for `corpus/knowledge/mako-regex-criteria-r89.md` and
(2) the `## Mistakes` and `## Gate` sections for `corpus/lessons/round-89.md`. The L1 integrates; nothing under
`corpus/` was written by this seat.

## Files written

- `.ufo/waves/round-89/w1/R89MScribeEntry.md` — this report, containing both drafts.

No other file was created or modified. Scratch lived at `/fast/scratch/hyaku/mado-r89/R89MScribeEntry/` and is
deleted on exit (see § Scratch).

## Behaviour

1. Read the round-89 declaration, the round-88 knowledge entry (`corpus/knowledge/mako-fields-containment-r88.md`)
   for front matter and decision-table form, `corpus/QUALITY.md` (last fifteen criteria, i.e. 138-147),
   `corpus/lessons/round-88.md`, `corpus/SOURCES.md` rows S490-S495.
2. Fetched upstream mako v1.11.0 `criteria.c` and the tag tarball, and read the state-machine enum in
   `include/enum.h` — the first replica attempt used the wrong enum value for `QUOTE_ESCAPE` and printed
   `CONFUSED`; the fix is recorded under Gates #6. Read `criteria.c` lines 46-59, 108-136, 162-262, 326-352,
   538-550 with `nl -ba`.
3. Built the lane's oracle `controls/posix-ere-oracle.c` and ran twelve pattern/text rows through it and through
   `python3 -c 're.search(...)'`; also built a verbatim replica of `parse_criteria`'s state machine to compare
   against (a) the round-88 `tokenize` from git bytes and (b) the round-89 candidate's tokenizer.
4. Ran the C1 candidate (DRAFT bytes) over the host's own mako config chain once per host `summary~` pattern.
   **Every candidate run in this report is DRAFT**: no counter was measured, no receipt was written under
   `.ufo/waves/round-89/receipts/`, and no number here is a round measurement.
5. Left the C1/C2 measured figures and the census as `<L1: …>` placeholders; no number in the drafts is invented.

## Gates (command, exit code)

| # | command | rc | result used by the drafts |
|---|---|---|---|
| 1 | `curl -sS -o criteria.c https://raw.githubusercontent.com/emersion/mako/v1.11.0/criteria.c; sha256sum criteria.c` | 0 | `22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c` — equals the S494 pin |
| 2 | `curl -sSL -o mako.tar.gz https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0; sha256sum; tar xzf` | 0 | tarball `72d11d3fca20a3dfbca0107ff875eace479751be0cf2ddd1dd5bafa131ac7282`; `include/enum.h` `1367d5c39ca619bd8ddd25c6613ca5667de8f4b13ab5803b3a27e358a8127351` |
| 3 | `grep -rn 'setlocale' mako-1.11.0/` | **1** (no match) | mako v1.11.0 never calls `setlocale`; the C locale is the startup default |
| 4 | `nl -ba criteria.c \| sed -n '46,59p;108,136p;162,215p;226,245p;326,352p;538,556p'` | 0 | `match_regex_criteria` 47-59; `summary~` 332-339 / `body~` 344-351; tokenizer states 177-215, refusals 228-239; cannot-set-both 542-550; match sites 115-120, 127-132 |
| 5 | `nl -ba mako-1.11.0/include/enum.h` (via grep `MAKO_PARSE_STATE`) | 0 | `:7-11` NORMAL 0, ESCAPE 1, QUOTE 2, QUOTE_ESCAPE 3 (= QUOTE\|ESCAPE), FORMAT 4 |
| 6 | `cc -O0 -o ore .ufo/waves/round-89/controls/posix-ere-oracle.c` then `python3 -I rows.py` | 0 | row driver for Draft 1 §2 (fifteen rows run; twelve selected for the table); the first `tokoracle` build printed `CONFUSED` because the replica used `QUOTE_ESCAPE = 4`; corrected to 3 per evidence row 5, rebuilt (`cc` rc 0), and re-ran |
| 7 | `python3 -I rows2.py` | 0 | confirming rows `\<Wi` (`match`/`nomatch`), `(ab)\1` (`match`/`match`), `a\nb` on `a<LF>b` (`nomatch`/`match`), `\d` on `d` (`match`/`nomatch`), `\d` on `5` (`nomatch`/`match`) |
| 8 | `cc -O0 -o tokoracle tokoracle.c`; `python3 -I tokcmp2.py`; `python3 -I tokcand.py` | 0 | upstream replica vs round-88 `tokenize` vs round-89 candidate `tokenize` on `[summary="a\.b"]`, `[body~="\d+"]`, `[app-name=a<TAB>b]`, `[summary="q\"x"]`, `[summary="q\\x"]`, `[summary=a\.b]`, trailing backslash, bare `"` |
| 9 | `git show 7d3074865a9f5acfa0f1c9c66b460e73d4031331:tools/mado-mako.py > r88tool.py; sha256sum` | 0 | `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237` (the r88 C2 measured tool) |
| 10 | `python3 -I .ufo/waves/round-89/build/mado-mako.c1.py --config ~/.config/mako/config --home "$HOME"` | 0 | DRAFT: `MADO_MAKO: resolved=37 refusals=7`; the seven refusals are `core.ini:11` (needs `--app-name`), `:20` (needs `--urgency`), `:24,:27,:30,:33,:36` (need `--summary`) |
| 11 | same tool, `--summary <S> --app-name foo`, once per host pattern | 0 | DRAFT: each of the five sections applies; `on-button-left` = the section's exec line for `:24,:27,:30,:33`, `max-icon-size` 32 → 80 for `:36`; a summary outside the five applies none |
| 12 | `r88tool.py` and the candidate on a scratch fixture `[summary="a\.b"]` + `[body~="a\.b"]` | 0 | r88 applies the exact section to the literal summary `a\.b` and not to `a.b`; the candidate (and upstream's tokenizer) resolves the value to `a.b`, so `a.b` matches and `a\.b` does not — the M89-2 divergence, made observable |
| 13 | `cc -O0 -o orelocale orelocale.c` (oracle + `setlocale(LC_ALL, "")`); `LC_ALL=C ./orelocale …`, `LC_ALL=en_US.UTF-8 ./orelocale …` | 0 | with the C locale `^.$` on `é` → `nomatch`, `[[:alpha:]]` on `é` → `nomatch`; with `en_US.UTF-8` both → `match` (lab probe showing what the missing `setlocale` call buys) |
| 14 | `python3 -c "import locale; print(locale.setlocale(locale.LC_CTYPE))"` | 0 | `en_US.UTF-8` — a Python process that calls `regcomp` without pinning `LC_ALL` compiles in UTF-8, unlike mako |
| 15 | `zcat /usr/share/man/man3/regex.3.gz \| nl -ba \| sed -n '60,140p'`; `zcat …/man7/regex.7.gz \| nl -ba \| sed -n '60,215p'`; `zcat …/man3/setlocale.3.gz \| nl -ba \| sed -n '55,150p'`; `sha256sum` of each container | 0 | regex(3):77-100 (REG_EXTENDED / REG_NOSUB), :102-125 (REG_NEWLINE is what stops `.` matching a newline); regex(7):29 (`Linux man-pages 6.19`), :114-127 (atoms; `\`+other character = that character), :206-213 (character classes), :43-45 (open decisions are marked); setlocale(3):135-137 ("On startup … the portable C locale is selected as default") |
| 16 | `sha256sum /usr/share/man/man3/regex.3.gz /usr/share/man/man3/regcomp.3.gz /usr/share/man/man7/regex.7.gz /usr/share/man/man3/setlocale.3.gz` | 0 | `f79f05fd…`, `bdeb1289…` (`regcomp.3.gz` is a 37-byte `.so man3/regex.3` stub), `7d3f3e60…`, `253d8b37…` |
| 17 | `grep -n '^| S49[0-9]' corpus/SOURCES.md`; `grep -n '^\*\*148\|^\*\*149' corpus/QUALITY.md` | 0 / **1** | registry ends at S495; QUALITY's highest number is 147, so the drafts propose 148 and 149 |
| 18 | `git rev-parse HEAD` | 0 | `af998dcc41d48618ffe7afe0efc9354755a9244e` (read-only git; no mutating git/jj command was run anywhere) |

`git` was used read-only (`show`, `rev-parse`, `status`). No pacman transaction; **no tool installed or updated**.

=== DRAFT 1: corpus/knowledge/mako-regex-criteria-r89.md — verbatim begin ===

source: S494 (upstream mako v1.11.0 source, tag tarball https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0 sha256 72d11d3fca20a3dfbca0107ff875eace479751be0cf2ddd1dd5bafa131ac7282: criteria.c sha256 22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c, include/enum.h sha256 1367d5c39ca619bd8ddd25c6613ca5667de8f4b13ab5803b3a27e358a8127351), S496 (PLACEHOLDER — regex(3)/regcomp(3) on this host: /usr/share/man/man3/regex.3.gz sha256 f79f05fd7ecd85fb292110e53d3709e956fddefbcce8f0e156c88ca0624be6ff, while /usr/share/man/man3/regcomp.3.gz is a `.so man3/regex.3` stub, sha256 bdeb1289a9739e2a01374fb45979ae3c60642800b58ee87e32b8f24a20db7977), S497 (PLACEHOLDER — regex(7) on this host, Linux man-pages 6.19: /usr/share/man/man7/regex.7.gz sha256 7d3f3e609b015ffa8906c3d06c4f79b8f5f93495b87471ca776b133e1de94373), S498 (PLACEHOLDER — setlocale(3) on this host: /usr/share/man/man3/setlocale.3.gz sha256 253d8b37dc72ff3fbe3e34c3968e3268d88ec1a3833cd5606790450709f56111), S499 (PLACEHOLDER — /usr/include/regex.h on this host: `REG_EXTENDED 1` at :310, `REG_NOSUB (1 << 3)` at :323). The S496-S499 ids are placeholders for the rows R89MScoutSources drafts; the L1 assigns the final ids when those rows are admitted.
covers: what mako 1.11.0 does with the `summary~` and `body~` criteria fields — the `regcomp` flags, the unanchored `regexec` search, the C locale because the tree never calls `setlocale`, an invalid pattern rejecting the whole criteria, the `summary`/`summary~` conflict, and the criteria tokenizer's escape and separator rules; a feature-by-feature comparison of glibc ERE against Python `re`; the host's five `summary~` sections and what each one applies
verified-at: 2026-11-06 at af998dcc41d48618ffe7afe0efc9354755a9244e (base revision). Every run of the C1 candidate `.ufo/waves/round-89/build/mado-mako.c1.py` cited here is DRAFT; the measured revision is set by the round-89 freeze.
recheck: 90d

# mako `summary~` / `body~`: POSIX extended regex in the C locale

Round 88 refused `summary~` and `body~` and named them a limit (`corpus/knowledge/mako-fields-containment-r88.md`
§1). Round 89 models them the way upstream does: the value is compiled with libc `regcomp(REG_EXTENDED | REG_NOSUB)`
and matched with `regexec`, through `ctypes` in the C locale — never with Python `re`, which answers a different
question (§2). The resolver is `tools/mado-mako.py`; the manual calls both fields "a POSIX extended regular
expression match" and says each conflicts with its exact-match sibling (mako(5) L450-451, L456-457, S493).

Scope: read-only resolution of the effective options for one described notification. Not in scope: a live
notification, D-Bus ownership, `makoctl` state, rendering, and mako's runtime behaviour.

## 1. What mako does with the two fields

1. **Compile flags.** `criteria.c` 332-339 (`summary~`) and 344-351 (`body~`) call
   `regcomp(&criteria->summary_pattern, value, REG_EXTENDED | REG_NOSUB)` / `regcomp(&criteria->body_pattern, …)`.
   `REG_EXTENDED = 1` (`/usr/include/regex.h:310`) selects POSIX extended syntax, not basic
   (regex(3) 77-84); `REG_NOSUB = 1 << 3` (`regex.h:323`) means "report only overall success" (regex(3) 91-100).
   No `REG_ICASE` and no `REG_NEWLINE` are passed: matching is case-sensitive and newline-blind (rule 2).
2. **Unanchored search.** `match_criteria` hands the compiled pattern straight to `match_regex_criteria`
   (criteria.c 115-120, 127-132), which calls `regexec(pattern, value, 0, NULL, 0)` (criteria.c:48). There is no
   anchoring wrapper, so a `summary~` value matches any substring of the summary; `^` and `$` are the only
   anchors, and with `REG_NEWLINE` unset they bind the beginning and end of the whole string, not of a line
   (regex(7) 114-116; regex(3) 102-125 says `REG_NEWLINE` is what makes `.` skip a newline and `^`/`$` match at
   newlines). Measured: `./ore 'Wi.Fi' 'Wi<LF>Fi'` → `match`, and `./ore 'Wi-Fi$' 'Wi-Fi<LF>'` → `nomatch`.
3. **A `regexec` error other than `REG_NOMATCH` is a non-match.** criteria.c 47-59: on any nonzero return it
   prints `failed to match regex: <regerror text>` to stderr and returns `false`; only `REG_NOMATCH` is silent.
   The section therefore does not apply, and the criteria is not rejected.
4. **An invalid pattern rejects the whole criteria.** When `regcomp` returns nonzero, upstream prints
   `Invalid summary~ regex '<value>'` (criteria.c 333-337) or `Invalid body~ regex …` (345-349) and returns
   `false` from `parse_criteria`; the section is not created. Measured with the oracle: `./ore '[' 'x'` →
   `invalid`, and `./ore '(?i)x' 'x'` → `invalid` (glibc ERE has no inline flags; the round-89 case set's
   `r11-invalid-inline-flag` pins it).
5. **`summary` and `summary~` cannot both be set** — nor `body` and `body~`. criteria.c 542-550 prints
   ``Cannot set both `summary` and `summary~` `` / ``Cannot set both `body` and `body~` `` and fails the parse.
   The manual states the same conflict at L447-448 and L453-454 (S493).
6. **The tokenizer runs before `regcomp`.** `parse_criteria` (criteria.c 162-262) is a small state machine over
   the header text: `NORMAL` 0, `ESCAPE` 1, `QUOTE` 2, `QUOTE_ESCAPE` 3, `FORMAT` 4 (include/enum.h:7-11;
   `QUOTE_ESCAPE` is `QUOTE | ESCAPE`, which is why `state &= ~MAKO_PARSE_STATE_ESCAPE` at :181 returns to
   quoting). Its two decisions matter to a regex value:
   - **A backslash escapes the next character in either state, and the backslash is dropped.** Outside quotes
     (NORMAL `case '\\'` → ESCAPE, :201-203) and inside quotes (`case '\\'` → QUOTE_ESCAPE, :186-188), the next
     character is appended verbatim (:177-182). Inside quotes this applies to *every* character, not only `"` and
     `\`. So `[summary~="\d+"]` passes `d+` to `regcomp`, and a literal backslash must be written `\\`. A trailing
     backslash or an unterminated quote refuses the header (:228-239). Measured with a verbatim replica of the
     state machine: `summary="a\.b"` → token `summary=a.b`; `body~="\d+"` → token `body~=d+`.
   - **Only a space separates tokens.** In NORMAL only `case ' '` ends a token (:207-212); a tab, newline or
     other whitespace is an ordinary character inside the token (:193-195 in QUOTE, and the NORMAL `default:`).
     Measured: `app-name=a<TAB>b` is one token `app-name=a<TAB>b` upstream.
7. **The C locale.** mako never calls `setlocale`: `grep -rn setlocale` over the v1.11.0 tree returns no match.
   setlocale(3) 135-137: "On startup of the main program, the portable `C` locale is selected as default", so
   `regcomp`/`regexec` run with `LC_CTYPE=C` whatever the environment says. Two consequences, both measured:
   bracket classes are ASCII-only (`./ore '[[:alpha:]]' 'é'` → `nomatch`), and `.` consumes one **byte**, not one
   code point (`./ore '^.$' 'é'` → `nomatch`, while `./ore '.' 'é'` → `match`). This is the opposite of what a
   Python process sees: CPython selects `LC_CTYPE` from the environment at startup (measured
   `en_US.UTF-8` here), so a `ctypes` `regcomp` without an explicit `LC_ALL=C` compiles in UTF-8 — the lab probe
   `orelocale` with `setlocale(LC_ALL, "")` turns `^.$` on `é` from `nomatch` to `match`.

## 2. Decision table: pattern feature → glibc ERE in the C locale → Python `re`

Every verdict below was produced by running the compiled oracle
(`cc -O0 -o ore .ufo/waves/round-89/controls/posix-ere-oracle.c`; `./ore PATTERN TEXT` prints `match`, `nomatch`
or `invalid`) and `python3 -c 'import re; re.search(PATTERN, TEXT)'` on the same strings. Pattern and text are
shown as Python literals; `<LF>` is a newline byte, and a `|` inside a table cell is escaped as `\|` for Markdown
(row 7's pattern is the three characters `a`, `|`, `b`).

| # | feature | pattern | text | glibc ERE (C locale) | Python `re` | verdict relation |
|---|---|---|---|---|---|---|
| 1 | start anchor | `'^Setup'` | `'Setup Wi-Fi'` | match | match | agree — `^` binds the start of the string in both |
| 2 | `.` against a newline | `'Wi.Fi'` | `'Wi<LF>Fi'` | match | nomatch | **diverge** — with no `REG_NEWLINE`, `.` matches a newline (regex(3) 102-103); `re` needs `re.DOTALL` |
| 3 | `$` before a trailing newline | `'Wi-Fi$'` | `'Wi-Fi<LF>'` | nomatch | match | **diverge** — Python's `$` also matches immediately before a final newline |
| 4 | backslash before an ordinary letter | `'\d'` | `'5'` | nomatch | match | **diverge** — glibc reads `\d` as the ordinary character `d` (regex(7) 117-123); Python reads a digit class |
| 5 | POSIX bracket class | `'[[:alpha:]]+'` | `'xyz'` | match | nomatch | **diverge** — Python reads `[[:alpha:]]` as a literal member set and warns "Possible nested set" |
| 6 | GNU word boundary | `'\<Wi'` | `'Wi-Fi'` | match | nomatch | **diverge** — `\<` is a glibc extension; Python reads `\<` as a literal `<` |
| 7 | alternation | `'a\|b'` | `'xb'` | match | match | agree — both are ERE/Python alternation |
| 8 | group plus | `'(ab)+'` | `'abab'` | match | match | agree — ERE grouping is bare `( )`, as in Python |
| 9 | bounded repetition | `'a{2,3}'` | `'aa'` | match | match | agree — a POSIX `bound` (regex(7) 70-103) |
| 10 | rejected pattern | `'['` | `'x'` | invalid | invalid (`re.error: unterminated character set at position 0`) | same verdict, different channel — `regcomp` returns nonzero and mako rejects the criteria; `re` raises |
| 11 | `.` counts bytes or code points | `'^.$'` | `'é'` (U+00E9, two UTF-8 bytes) | nomatch | match | **diverge** — C locale `.` is one byte (§1.7) |
| 12 | escape sequences are not C escapes | `'a\nb'` | `'a<LF>b'` | nomatch | match | **diverge** — `\n` is the letter `n` to glibc (regex(7) 120-123), a newline to Python |

Seven of the twelve rows disagree; four agree (rows 1, 7, 8, 9); one (row 10) agrees on the verdict but not on the
mechanism. Two further
rows agree and are listed only to keep the divergent set honest: `'(ab)\1'` on `'abab'` (both `match` — glibc's
ERE accepts a backreference as an extension) and `'\bWi'` on `'Wi-Fi'` (both `match`, both reading a word
boundary). The `\b` agreement is incidental: `/usr/include/regex.h` defines no flags for it, regex(7) does not
name it, and other libcs need not have it.

Consequence: substituting Python `re` for the libc call would answer a different question on rows 2, 3, 4, 5, 6,
11 and 12, and on row 10 it would raise instead of returning a rejected criteria; `re` also accepts `(?i)` (the
round-89 case `r11-invalid-inline-flag`), which `regcomp` rejects.

## 3. The host's five `summary~` sections, and what each resolves to

`~/.config/mako/config` line 1 is `include=~/.local/share/omarchy/default/mako/core.ini`, so the host's criteria
sections are the included file's. Five of them carry a `summary~` header; every pattern is a plain literal
(no ERE metacharacter — measured: each pattern matches itself, `./ore '<pattern>' '<pattern>'` → `match` for all
five), and the search is unanchored (§1.2), so each matches any notification whose summary *contains* the text.

| core.ini | header | ERE reading | option the section applies | DRAFT resolution |
|---|---|---|---|---|
| :24 | `[summary~="Setup Wi-Fi"]` | literal substring | `on-button-left=exec sh -c 'omarchy-notification-dismiss "Setup Wi-Fi"; omarchy-launch-wifi'` | section applies; that `on-button-left` |
| :27 | `[summary~="Update System"]` | literal substring | `on-button-left=exec sh -c 'omarchy-notification-dismiss "Update System"; omarchy-launch-floating-terminal-with-presentation omarchy-update'` | section applies; that `on-button-left` |
| :30 | `[summary~="Learn Keybindings"]` | literal substring | `on-button-left=exec sh -c 'omarchy-notification-dismiss "Learn Keybindings"; omarchy-menu-keybindings'` | section applies; that `on-button-left` |
| :33 | `[summary~="Install Dictation with Voxtype"]` | literal substring | `on-button-left=exec sh -c 'omarchy-notification-dismiss "Install Dictation with Voxtype"; omarchy-launch-floating-terminal-with-presentation omarchy-voxtype-install'` | section applies; that `on-button-left` |
| :36 | `[summary~="Screenshot copied & saved"]` | literal substring; `&` is ordinary in ERE | `max-icon-size=80` and `format=<b>%s</b>\n%b` (the second line repeats the global default) | section applies; `max-icon-size` 32 → 80, `format` unchanged |

A summary outside the five applies none of them (measured with `--summary Unrelated`). With `--summary` supplied
and no `--urgency`, the only remaining refusal on the whole chain is `core.ini:20` (`[urgency=critical]`, which
needs `--urgency`); `core.ini:11` (`[app-name=Spotify]`) and the five sections all resolve. This is what round 88
could not do: it refused the five sections by construction.

## 4. Named limits

- **No live notification was sent.** The entry reads source and manual; it does not verify that the running mako
  matches its source. The resolver answers "what would mako compute", not "what mako did".
- **glibc-specific rows.** `\<`, `\>` and the `\`+ordinary-character reading (rows 4, 6, 12) are glibc behaviour
  that regex(7) itself marks as an open POSIX decision (`\*(dg` at lines 43-45 and on the `\`+other rule at
  120-123). Row 11 follows from the C locale instead: a libc that read a multibyte summary as characters even
  under `LC_CTYPE=C` would answer `match`.
- **The tokenizer removes one level of escaping.** A user who writes `summary~="\d+"` gets the pattern `d+`, and
  a user who writes `summary~="\."` gets `.` (any character). This is upstream's documented-by-implementation
  behaviour, not a lane choice; the lane models it and does not "fix" it.
- **The C locale is a property of this mako build.** It holds because no `setlocale` call exists in v1.11.0
  (`grep -rn setlocale` → no match). A future mako that calls `setlocale(LC_ALL, "")` would change rows 5 and 11.
- **Byte semantics apply to the raw message string.** A summary carrying combining characters or an invalid UTF-8
  sequence is matched bytewise; the entry says nothing about how such a summary was produced.
- **`regexec` errors are silent non-matches.** criteria.c 50-55 logs to stderr only; a `REG_ESPACE` during a
  match makes the section not apply rather than reporting a failure. A caller sees "did not match", not "could
  not match".
- **The five host sections are resolved, not verified.** Nothing here shows that a notification summary really
  arrives as those exact strings; the click actions are what the config would apply.

## 5. What this entry does not certify

- It does not certify the round-89 counter or the candidate beyond the DRAFT runs named in the front matter.
- It does not claim Python `re` can be configured to imitate glibc: rows 2, 3, 4, 5, 6, 11 and 12 would each need
  a per-row rewrite, and row 4's reading of `\d` has no `re` equivalent without rewriting the pattern text.
- It does not claim the tokenizer is a general parser: `parse_criteria` handles only the criteria header text, and
  a `\` at the very end or an unclosed quote refuses the header.

## 6. Unknowns

- Whether mako ever re-compiles a pattern at runtime: UNSTATED; the pattern is compiled once at config load
  (criteria.c 332-351) and freed by `regfree` in `destroy_criteria` (criteria.c:38, :40).
- Whether a `regexec` `REG_NOMATCH` and a `REG_ESPACE` are distinguishable to the user: they are not, by the
  return path (§4).
- Whether the host's included `core.ini` is the only criteria source: `~/.config/mako/config` line 1 is the only
  `include=` line and the file carries three colour options after it, so on this host it is.
- Whether a second-pass field can carry a regex: UNSTATED for `output` and `anchor`; `apply_criteria_field`
  (criteria.c 300-400) names exactly two `~` keys, `summary~` (:332) and `body~` (:344), and none for the
  second-pass fields.

=== DRAFT 1 end ===

=== DRAFT 2: corpus/lessons/round-89.md — `## Mistakes` and `## Gate` sections, verbatim begin ===

## Mistakes

**M89-1 — a crash was routed as a distinguishing probe, although the same report states that a crash is not a kill.**
Class: evidence-inference — an abnormal termination read as a semantic difference.
Evidence: `.ufo/waves/round-88/r1/R88MResidMut.md:131` routes the missing case `probe-cycle-via-second-lexical-path`
with `mutant `FAIL exit=1` (RecursionError)`, and `:192-195` (§8) lists "cycle detection through a second lexical
path is untested" among the C2 coverage gaps — while `:38` of the same report states the frozen rule: "a mutant that only crashes is reported as
`crashed-not-killed`, per the frozen rule." The rule's implementation is
`quality/counters/c2-r88-include-containment.py:225` (`status = "killed" if hit else ("crashed-not-killed" if crashed else "survived")`),
with the predicate note at `:168` ("a crash is not a kill") and the selftest at `:471-475`; the C1 counter carries
the same rule at `:281`, `:207` and `:563-566`. On that probe the correct tool refuses with `cycle` and the mutant
only recurses, so the probe is a statement about the mutant's termination, not about a wrong answer.
Captured-by: **none in round 88** — the probe ran outside the frozen case set, so no scorer ever assigned the
mutant a status for it. Round 89's C2 declaration
(`.ufo/waves/round-89/claims-declaration-r89.md` §C2, "RM6C2 is declared crash-only before data") re-reads the
probe against the kill rule, excludes RM6C2 from the 7-of-7 target with the argument that no terminating input
separates it, and keeps `s2-cycle-second-lexical-path` in the supplementary set with its crash printed.
Fix: the declaration declares RM6C2 crash-only before data (not after a miss), and QUALITY criterion 148 makes a
probe's scorer-assigned status the evidence a survivor routing needs:
> **148. A survivor is a coverage gap only when a probe makes the mutant return a well-formed wrong answer.** A seat
> that routes a survivor names the probe, the correct tool's result, and the mutant's result *as the scorer assigned
> it* — a `killed`/semantic verdict, not a process exit status. A probe on which the mutant terminates abnormally
> (nonzero exit, traceback, abort, timeout) distinguishes nothing: it is recorded as "no separating input found",
> the crash is kept as evidence, and the mutant is declared crash-only or equivalent. Check: re-score the probe
> through the same predicate the claim uses and quote its status field; no row whose mutant status is
> `crashed-not-killed` may carry the word "distinguishes". Shown able to fail:
> `.ufo/waves/round-88/r1/R88MResidMut.md:131` routes RM6C2 on `mutant FAIL exit=1 (RecursionError)` while `:38`
> states the rule and `quality/counters/c2-r88-include-containment.py:225` assigns `crashed-not-killed`.
> (lesson: lessons/round-89.md#mistakes M89-1)

**M89-2 — the round-88 tokenizer kept a backslash inside quotes before any character other than `"` and `\`, unlike `parse_criteria`'s `QUOTE_ESCAPE` state.**
Class: model-drift — a re-implementation narrowed an upstream state to two characters.
Evidence: `tools/mado-mako.py` at `7d3074865a9f5acfa0f1c9c66b460e73d4031331:222` reads
`if char == "\\" and i + 1 < len(body) and body[i + 1] in ('"', "\\"):`, and a backslash before any other
character falls through to `:228` `word.append(char)`, keeping it. Upstream `criteria.c:186-188` sends **every**
backslash inside quotes to `MAKO_PARSE_STATE_QUOTE_ESCAPE`, and `:177-182` appends the next character and clears
the escape bit; `include/enum.h:7-11` gives `QUOTE_ESCAPE = 3 = QUOTE | ESCAPE`, so the clear returns to `QUOTE`.
The same pass also shows the separator rule: round 88 split on `char.isspace()` (`:242`), upstream splits on
`case ' '` only (`criteria.c:207-212`), so a tab inside a token ends the token in the lane's model and stays in it
upstream. Measured against a verbatim replica of the state machine: `summary="a\.b"` yields `summary=a.b` upstream
and `('summary', 'a\.b')` from the round-88 `tokenize`; `body~="\d+"` yields `body~=d+` upstream and
`('body~', '\d+')`; `app-name=a<TAB>b` yields one token upstream and two (`('app-name','a'), ('b', None)`) from
round 88. Latent since round 88 in exact `summary=`/`body=` values, and made visible by round 89's regex fields:
on the scratch fixture `[summary="a\.b"]`, the round-88 tool at `7d30748` applies the section to a notification
summary that literally contains a backslash and not to `a.b`, which is the opposite of what the tokenizer-fed
exact compare does upstream.
Captured-by: **no round-88 case** — `c16-backslash-escaped-space` is the only backslash case in
`.ufo/waves/round-88/controls/mako-cases-r88.json` and it is outside quotes (`[app-name=Google\ Chrome]`), so no
case carried a quoted backslash. Round 89's C1 build caught it when the same tokenizer had to feed `regcomp`: the
candidate's `tokenize` (`build/mado-mako.c1.py:276-288`) escapes any character inside quotes and splits on `" "`
only (`:299`), and the C1 case set now pins it with `r14-quoted-backslash-escapes-dot`,
`r15-quoted-double-backslash` and `r16-tab-inside-token`.
Fix: the candidate tokenizer matches the state-machine replica on eight probe inputs (quoted single backslash,
quoted double backslash, escaped quote, bare quote, outside-quote backslash, tab, trailing backslash, unterminated
quote); QUALITY criterion 149 requires the model to be checked against the upstream state machine's own states:
> **149. A model of an upstream parser is checked against the upstream state machine's own states, one probe per
> state, and the probe list is frozen with the model.** A re-implementation of a tokenizer or scanner names the
> upstream file and line range of each state it copies and carries one input that enters that state: for mako's
> `parse_criteria` at minimum the quoted state with a backslash before a character other than the quote or a
> backslash, and the normal state with a tab inside a token. Check: compile a replica of the upstream state machine
> from the pinned source lines and require the model's token output to equal the replica's on every probe; a probe
> whose escaped character is only `"` or `\` does not enter the rule being copied. Shown able to fail:
> `tools/mado-mako.py` at `7d3074865a9f5acfa0f1c9c66b460e73d4031331:222` keeps `\` before `.` inside quotes
> (`('summary', 'a\.b')` where `criteria.c:177-182` yields `a.b`) and splits on any whitespace at `:242` where
> `criteria.c:207` splits on a space only. (lesson: lessons/round-89.md#mistakes M89-2)

## Gate

### Registry rows (S494; S496-S499 placeholders for R89MScoutSources) — opened 2026-11-06

- **S494 extended** (same row; the anchor and `used-by` grow). New anchor lines: `criteria.c:46-59`
  (`match_regex_criteria`: `regexec` with no anchoring, a non-`REG_NOMATCH` error printed and returned as false),
  `criteria.c:162-262` (`parse_criteria`: `ESCAPE`/`QUOTE_ESCAPE` append the next character and drop the
  backslash, only `' '` separates tokens, unterminated quote and trailing backslash refuse), `criteria.c:332-351`
  (`regcomp(..., REG_EXTENDED | REG_NOSUB)` for both fields), `criteria.c:542-550` ("Cannot set both"), and
  `include/enum.h:7-11` (`QUOTE_ESCAPE = 3`). Tag tarball
  `https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0` sha256
  `72d11d3fca20a3dfbca0107ff875eace479751be0cf2ddd1dd5bafa131ac7282`; `include/enum.h` sha256
  `1367d5c39ca619bd8ddd25c6613ca5667de8f4b13ab5803b3a27e358a8127351`. `used-by` gains
  `corpus/knowledge/mako-regex-criteria-r89.md`. Tier A, tag-pinned (criterion 27).
- **S496-S499 placeholders** — the rows R89MScoutSources drafts: regex(3)/regcomp(3) on this host (container
  sha256 `f79f05fd7ecd85fb292110e53d3709e956fddefbcce8f0e156c88ca0624be6ff`; `regcomp.3.gz` is a `.so man3/regex.3`
  stub sha256 `bdeb1289a9739e2a01374fb45979ae3c60642800b58ee87e32b8f24a20db7977`), regex(7) (sha256
  `7d3f3e609b015ffa8906c3d06c4f79b8f5f93495b87471ca776b133e1de94373`), setlocale(3) (sha256
  `253d8b37dc72ff3fbe3e34c3968e3268d88ec1a3833cd5606790450709f56111`), and `/usr/include/regex.h`
  (`REG_EXTENDED 1` at :310, `REG_NOSUB (1 << 3)` at :323). The L1 assigns the final ids and the row text when
  those rows are admitted; the entry cites them by these four placeholder ids until then.

### Candidates considered (round 89)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mako-regex-criteria-r89.md` (regex fields, C locale, tokenizer, host sections) | **admit** | every rule cites S494 or a placeholder at a line; the twelve-row comparison is measured on this host; the five host sections resolve under the DRAFT candidate | a source line that contradicts a stated rule |
| modelling the two fields with Python `re` | **reject** | seven of the twelve measured rows disagree (2, 3, 4, 5, 6, 11, 12), including `^.$` on `é` and `\d` on `5`; `re` also accepts `(?i)`, which mako refuses | a `re` configuration that reproduces all twelve verdicts |
| calling `regcomp`/`regexec` from Python without pinning the locale | **reject** | CPython selects `LC_CTYPE` from the environment at startup (`en_US.UTF-8` on this host), so `ctypes` would compile in UTF-8 while mako compiles in C; the `orelocale` probe flips `^.$` on `é` from `nomatch` to `match` under `en_US.UTF-8` | a measured host where the Python process starts in the C locale |
| modelling `summary~` as an anchored literal match | **reject** | the search is unanchored (criteria.c:48; measured `'Wi-Fi'` on `'Setup Wi-Fi now'` → `match`), and rows 5, 6, 9, 10 are not literal matches | a case set in which literal search and ERE agree on every row |

### Spot-check

Pending: the non-author closure is the operator-dispatched verifier (LEARNING.md). This lesson records no
spot-check result.

### Census

- Round start / round end: `<L1: scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
  output at the round-start and round-end revisions>`.
- Measurements: `<L1: the C1 and C2 measured lines with their receipt paths at the freeze revision>`.

=== DRAFT 2 end ===

## Findings

- **F1 (evidence, D1 §2).** Substituting Python `re` for libc is not a style choice: seven of twelve measured
  rows disagree, and two of them (`^.$` on `é`, `\d` on `5`) are the ones a naive port would silently get wrong.
  The round-88 refusal was therefore right, and the round-89 C1 move needs the ctypes path it declares.
- **F2 (evidence, D1 §1.7).** The locale is a live variable in this model: CPython starts in `en_US.UTF-8` on this
  host (`python3 -c 'import locale; print(locale.setlocale(locale.LC_CTYPE))'`), and the `orelocale` probe shows
  `^.$` on `é` flipping `nomatch`↔`match` between the C and UTF-8 locales. A candidate that forgets `LC_ALL=C`
  would pass any case set that does not contain a non-ASCII or newline case.
- **F3 (evidence, M89-2).** The round-88 tokenizer divergence is observable, not just theoretical: on the fixture
  `[summary="a\.b"]`, the r88 tool applies the section to the literal summary `a\.b` and not to `a.b`; the
  candidate resolves the value to `a.b` and does the reverse. The r88 case set has no quoted-backslash case, which
  is why the frozen counters never saw it.
- **F4 (evidence, M89-1).** The round-88 residual report states the crash-is-not-a-kill rule and then routes a
  crash as a distinguishing probe in the same document (`:38` against `:131`). The contradiction is internal, so
  no external instrument was needed to see it — only a reader holding both sentences.
- **F5 (limit, D1 §3).** The five host sections resolve under the DRAFT candidate, but the entry keeps the
  distinction: resolving them is a statement about the config bytes, not about a delivered notification.

## Out of scope / not run

- No counter was run: neither `quality/counters/c1-r89-mako-regex.py` nor `quality/counters/c2-r89-survivor-kills.py`
  was executed, and no receipt was written under `.ufo/waves/round-89/receipts/`. The candidate's own `--selftest`
  was not run either (not needed by this seat's item).
- The oracle and the state-machine replica are scratch-only: `ore`, `orelocale`, `tokoracle` and the two row
  drivers were compiled and run under `/fast/scratch/hyaku/mado-r89/R89MScribeEntry/` and are not committed.
  Their compile commands and outputs are in the Gates table, which is what a later reader can replay.
- `corpus/`, `tools/`, `quality/`, the declaration, `MANIFEST.json`, `.ufo/state/` and every sibling lane file were
  not touched. No mutating git/jj command was run anywhere; no fixture repository was needed.
- Host reads stayed inside the credential-material rule: `~/.config/mako/config` and the one file it includes
  (`~/.local/share/omarchy/default/mako/core.ini`), plus the named man pages and `/usr/include/regex.h`.

## Scratch

`S=/fast/scratch/hyaku/mado-r89/R89MScribeEntry`, created with `mkdir -p`, used for `criteria.c`, the tag tarball
and its unpacked tree, the oracle and replica binaries, the fixture config and the two r88/candidate tokenizer
comparisons. Deleted with `rm -rf -- "$S"` after this report was written; the deletion was verified by
`test -e "$S"` returning nonzero.
