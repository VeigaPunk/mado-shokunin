source: S493 (mako(5) of the installed mako 1.11.0-1), S494 (upstream mako v1.11.0 criteria.c, https://raw.githubusercontent.com/emersion/mako/v1.11.0/criteria.c sha256 22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c: lines 46-59, 115-132, 162-262, 332-351, 542-550), S496 (regex(3) on this host, man-pages 6.19-1: /usr/share/man/man3/regex.3.gz container sha256 f79f05fd7ecd85fb292110e53d3709e956fddefbcce8f0e156c88ca0624be6ff; regcomp.3.gz is a `.so man3/regex.3` stub, sha256 bdeb1289a9739e2a01374fb45979ae3c60642800b58ee87e32b8f24a20db7977), S497 (regex(7) on this host: /usr/share/man/man7/regex.7.gz container sha256 7d3f3e609b015ffa8906c3d06c4f79b8f5f93495b87471ca776b133e1de94373), S498 (setlocale(3) on this host: /usr/share/man/man3/setlocale.3.gz container sha256 253d8b37dc72ff3fbe3e34c3968e3268d88ec1a3833cd5606790450709f56111, decompressed lines 135-137), S499 (glibc /usr/include/regex.h on this host, sha256 ae656ea6032f59d670c8c1055e1eebcb93ddbc482fd26b333ed529d6a4784b97: `REG_EXTENDED 1` at :310, `REG_NOSUB (1 << 3)` at :323), S500 (upstream mako v1.11.0 tag tarball https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0 sha256 72d11d3fca20a3dfbca0107ff875eace479751be0cf2ddd1dd5bafa131ac7282: no setlocale call anywhere in the tree; include/enum.h sha256 1367d5c39ca619bd8ddd25c6613ca5667de8f4b13ab5803b3a27e358a8127351 lines 7-11); host `~/.local/share/omarchy/default/mako/core.ini` lines 24-38
covers: what mako 1.11.0 does with the `summary~` and `body~` criteria fields — the `regcomp` flags, the unanchored `regexec` search, the C locale because the tree never calls `setlocale`, an invalid pattern rejecting the whole criteria, the `summary`/`summary~` conflict, and the criteria tokenizer's escape and separator rules; a feature-by-feature comparison of glibc ERE against Python `re`; the host's five `summary~` sections and what each one applies
verified-at: 2026-11-06 at 099c662dc55521e365cd4126132cdcda4efc54b6 (C1 measured revision; the candidate bytes landed unchanged from the freeze d87361354b4d142287aac05bb973315749ef1fce). Runs cited below as DRAFT were made on those same bytes before the freeze; the measured receipt is `.ufo/waves/round-89/receipts/c1-measured-A-r89.txt`; host replay `.ufo/waves/round-89/w1/R89MExecHostDiff.md` (base decides 4/9 host criteria sections, the candidate 9/9).
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
   `r11-invalid-inline-flag` pins it). Every occurrence counts: `apply_criteria_field` runs once per token, in
   order (criteria.c 207-212, 243), so in `[summary~=a(b summary~=x]` the first `regcomp` fails and the criteria
   is rejected even though the last occurrence — the one a repeated field keeps — is valid. The tool compiles
   every occurrence in order for this reason (case `r32-earlier-invalid-occurrence`, mutant M37; found by
   R89MReviewC1 F1 before the freeze). In mako an invalid criteria makes `load_config_file` fail (config.c
   844-849); the tool refuses that one section and keeps resolving the rest (lane stance, as for every refusal).
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
