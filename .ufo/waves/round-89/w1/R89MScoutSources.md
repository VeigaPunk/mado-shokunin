# R89MScoutSources — source opening and drafted SOURCES.md rows (round 89, wave w1)

Seat: `R89MScoutSources` (scout). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Access date for every row below:
**2026-11-06**. Host versions (`pacman -Q man-pages glibc mako`, exit 0): `man-pages 6.19-1`, `glibc 2.44+r50+g1848099f063e-1`,
`mako 1.11.0-1`.

I did **not** edit `corpus/SOURCES.md` (the L1 appends). Rows below are drafts in the exact 11-column order of the frozen
contract (`CORPUS.md` § "SOURCES.md — where a shokunin learns"): `id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by`. Next free id is **S496**; S491–S495 are the last rows present.

**DRAFT — these are drafted rows, not a measurement.** No counter was run by this seat; nothing here is a verdict.

---

## 1. Findings that change the claim's shape (read before the rows)

1. **The REG_EXTENDED ↔ ERE sentence is not in POSIX chapter 9.** `https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html`
   contains **zero** occurrences of `REG_EXTENDED` (`grep -c "REG_EXTENDED" posix-ch09.html` → `0`). Chapter 9 gives the ERE
   *grammar* (section 9.4) and, at HTML lines 38-40, the *interface* sentence ("Both BREs and EREs are supported by the Regular
   Expression Matching interface … under `regcomp()`, `regexec()`"). The normative flag-to-syntax binding
   ("The application can specify Extended Regular Expressions using the `REG_EXTENDED` cflags flag.") lives on the separate
   **functions/regcomp.html** page (HTML lines 135-136). I therefore drafted **two** POSIX rows (S499 chapter 9, S500 regcomp()
   function page) instead of one; folding them into a single row would have forced the SOURCES `teaches` cell to cite a sentence
   the chapter-9 bytes do not contain.
2. **The "no setlocale" fact is a negative over the whole tree, not a main.c fact.** `main.c` alone cannot support "mako never
   calls `setlocale`". The supporting evidence is `grep -rn setlocale` over the **extracted tag tarball** (59 files) → no output,
   exit 1. Drafted as S501 anchored on the tarball, not on main.c.
3. **The criteria-tokenizer rules are *not* inside S494's anchor.** S494 anchors `criteria.c:75-76,80-81,100-101,105-106,110-111,
   122-123,85-86,90-91,267-290` plus `types.c`/`config.c`. Upstream `parse_criteria` (the tokenizer C1 leans on: backslash escapes
   inside quotes, space-only token split) is `criteria.c:162-258`, and the `REG_EXTENDED|REG_NOSUB` compile sites are
   `criteria.c:332-351` — neither is in S494's anchor. S501 covers them at the tarball URL, so the L1 need not open a fourth
   upstream URL. This is a **scope addition, not a correction**: S494 stays as it is (no `supersedes` needed, no `teaches` change).
4. **Two reads are needed to reproduce the man quotes.** The `.gz` container decompresses to nroff source (`nl -ba` on the
   decompressed text gives the line numbers used in the anchors); `man -P cat | col -bx` gives the flowed text (rendered line
   numbers are given alongside). Both were produced; the anchors below cite the decompressed-text lines (the re-checkable
   `zcat … | nl -ba` form) plus the rendered line.
5. **`regex.h` is the host's glibc header** (`pacman -Qo /usr/include/regex.h` → "owned by glibc 2.44+r50+g1848099f063e-1",
   exit 0), so the numeric flag values are a host fact, not a portability claim.
6. **Every fetch was fetched twice and compared byte-for-byte** (`cmp` exit 0 for all three network fetches: chapter 9, the
   regcomp() function page, the tag tarball).

---

## 2. Drafted registry rows (S496–S502)

### S496 — regcomp(3) on this host (man-pages 6.19-1)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S496 | regcomp(3)/regex(3) manual on this host, man-pages 6.19-1 installed — file:///usr/share/man/man3/regex.3.gz (container sha256 f79f05fd7ecd85fb292110e53d3709e956fddefbcce8f0e156c88ca0624be6ff; decompressed text sha256 1e2204595870b1eb85b9d2a559f39bcdbab1d8cc0f070406e4fa4a2f3568fda5, 403 lines / 8501 B) | docs | A | libc regcomp/regexec flags and return codes as documented on this host: REG_EXTENDED, REG_NOSUB, REG_NOMATCH | decompressed text lines 77-84 (REG_EXTENDED: "Use POSIX Extended Regular Expression syntax when interpreting regex"), lines 92-100 (REG_NOSUB: "Report only overall success"), lines 246-249 (REG_NOMATCH: "regexec() returns zero for a successful match or REG_NOMATCH for failure"); rendered lines 49-51, 57-59, 123; `.TH regex 3 2026-02-08 "Linux man-pages 6.19"`; opened 2026-11-06 | Tier A because this is the installed man page of the very libc the C1 matcher calls: REG_EXTENDED selects POSIX ERE syntax and REG_NOSUB reports success/failure only, so regexec's return of 0 versus REG_NOMATCH is the whole match verdict a criterion needs | mined | 2026-11-06 | 180d | corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md |

Gate quote block (S496) — URL/path: `file:///usr/share/man/man3/regex.3.gz` · access date: 2026-11-06 · primary quote (9 words):
> "Use POSIX Extended Regular Expression syntax when interpreting regex."

located at decompressed-text line 78-81 (rendered line 50; flag name at line 77).

Additional located quotes from the same source (each ≤25 words):
- line 92-93: `REG_NOSUB` → "Report only overall success." (rendered 57-58).
- line 246-249: `regexec()` → "returns zero for a successful match or REG_NOMATCH for failure." (rendered 123).

### S497 — setlocale(3) on this host (man-pages 6.19-1)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S497 | setlocale(3) manual on this host, man-pages 6.19-1 installed — file:///usr/share/man/man3/setlocale.3.gz (container sha256 253d8b37dc72ff3fbe3e34c3968e3268d88ec1a3833cd5606790450709f56111; decompressed text sha256 1a31b48c96ff1a4334cb2a6caa2d6228134ed056106304a155cb7015de44f1bf, 244 lines / 4924 B) | docs | A | the locale a process runs in before it calls setlocale(): the startup "C" locale | decompressed text lines 135-137 ("On startup of the main program, the portable \"C\" locale is selected as default"), lines 138-143 (portability requires an explicit setlocale(LC_ALL, "") after program initialization); rendered line 58; `.TH setlocale 3 2026-02-08 "Linux man-pages 6.19"`; opened 2026-11-06 | Tier A because it is the installed man page of this host's libc: a program that never calls setlocale stays in the portable "C" locale, which is exactly the premise under which a libc regcomp/regexec criterion is locale-invariant | mined | 2026-11-06 | 180d | corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md |

Gate quote block (S497) — URL/path: `file:///usr/share/man/man3/setlocale.3.gz` · access date: 2026-11-06 · primary quote
(15 words):
> "On startup of the main program, the portable \"C\" locale is selected as default."

located at decompressed-text lines 135-137 (rendered line 58).

### S498 — regex(7) on this host (man-pages 6.19-1)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S498 | regex(7) manual on this host, man-pages 6.19-1 installed — file:///usr/share/man/man7/regex.7.gz (container sha256 7d3f3e609b015ffa8906c3d06c4f79b8f5f93495b87471ca776b133e1de94373; decompressed text sha256 b81f25c555e2d7fe56349d7cf865bdf6ed36dc8ebb65f31f705b09ca55d33935, 375 lines / 12424 B) | docs | A | POSIX.2 regular-expression forms as documented on this host: which form is "extended", bracket expressions and character classes, and locale dependence of ranges and classes | decompressed text lines 33-40 (POSIX.2 "extended" REs are the modern form), lines 129-133 and 206-213 (bracket expression; character class "[:" ":]" stands for all characters of that class), lines 226-228 (classes stand for the wctype(3) classes; "A locale may provide others"), lines 150-151 (ranges are collating-sequence-dependent); rendered lines 7-8, 74-75, 82, 48; `.TH regex 7 2026-02-08 "Linux man-pages 6.19"`; opened 2026-11-06 | Tier A because it is the installed man page for this host's regex syntax: it fixes which of the two POSIX.2 forms a POSIX ERE criterion uses and shows that bracket ranges and character classes are the locale-sensitive parts, so a locale-free matcher has to keep its patterns inside what the "C" locale makes stable | mined | 2026-11-06 | 180d | corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md |

Gate quote block (S498) — URL/path: `file:///usr/share/man/man7/regex.7.gz` · access date: 2026-11-06 · primary quote (22 words):
> "Regular expressions (\"RE\"s), as defined in POSIX.2, come in two forms: modern REs (roughly those of egrep(1); POSIX.2 calls these \"extended\" REs)"

located at decompressed-text lines 33-37 (rendered lines 7-8).

Additional located quotes (each ≤25 words):
- lines 206-213: "the name of a character class enclosed in \":\" and \":]\" stands for the list of all characters belonging to that class." (rendered 74-75).
- lines 226-228: "These stand for the character classes defined in wctype(3). A locale may provide others." (rendered 82).
- lines 150-151: "Ranges are very collating-sequence-dependent, and portable programs should avoid relying on them." (rendered 48).

### S499 — POSIX.1-2024 (Issue 8) Chapter 9, Regular Expressions

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S499 | The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024, Chapter 9 "Regular Expressions" — https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html (fetched sha256 2f5f60e9fe2954fe09dc0991f5c03b7c1de771b0ae2104e4a8a5745187c64e24, 60438 B; tag-free, opened 2026-11-06) | spec | A | the normative POSIX ERE grammar (section 9.4) and the locale statement that governs how a POSIX ERE is interpreted | section 9.4 "Extended Regular Expressions" heading + body at HTML lines 482-485; HTML lines 38-40 (BREs and EREs are the two forms the regcomp()/regexec() interface supports); HTML lines 32-34 (character sets are interpreted according to the current locale, but character class expressions give contextual invariance across locales); HTML line 541 (9.4.5 ERE bracket expressions follow the BRE bracket rules); two fetches byte-identical; opened 2026-11-06 | Tier A because it is the specification itself: it fixes the ERE grammar a POSIX ERE criterion is written against and it states that character class expressions are locale-invariant while the surrounding character sets are locale-interpreted, which is why the "C" locale is a sufficient ground for a portable pattern | mined | 2026-11-06 | 180d | corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md |

Gate quote block (S499) — URL: `https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html` · access date: 2026-11-06 ·
primary quote (25 words):
> "Both BREs and EREs are supported by the Regular Expression Matching interface in the System Interfaces volume of POSIX.1-2024 under regcomp(), regexec()"

located at HTML lines 38-40.

Additional located quotes (each ≤25 words):
- HTML lines 483-485 (section 9.4 body): "The extended regular expression (ERE) notation and construction rules shall apply to utilities defined as using extended regular expressions".
- HTML lines 33-34: "many features, such as character class expressions, provide for contextual invariance across locales".
- HTML line 541 (9.4.5): "The rules for ERE Bracket Expressions are the same as for Basic Regular Expressions".

### S500 — POSIX.1-2024 (Issue 8) regcomp() function page

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S500 | The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024, `regcomp()` — https://pubs.opengroup.org/onlinepubs/9799919799/functions/regcomp.html (fetched sha256 544ff826004bbfa6436bb8b18d9ee38a4a12cd3473290ed530887648eab94874, opened 2026-11-06) | spec | A | the normative binding between the regcomp() cflags and POSIX ERE syntax: REG_EXTENDED, REG_NOSUB, REG_NOMATCH | HTML lines 121-122 (REG_EXTENDED: "Use Extended Regular Expressions"), lines 130-131 (REG_NOSUB: "Report only success/fail in regexec()"), lines 135-136 (the application selects EREs with the REG_EXTENDED cflags flag), lines 149-150 (REG_NOMATCH: "regexec() failed to match"), lines 237-238; the spec's own example at HTML line 196 compiles with REG_EXTENDED together with REG_NOSUB; two fetches byte-identical; opened 2026-11-06 | Tier A because it is the specification of the function the C1 matcher calls: it is the place that says REG_EXTENDED is what makes a pattern an ERE and that with REG_NOSUB a successful regexec is reported as success/failure only | mined | 2026-11-06 | 180d | corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md |

Gate quote block (S500) — URL: `https://pubs.opengroup.org/onlinepubs/9799919799/functions/regcomp.html` · access date: 2026-11-06 ·
primary quote (13 words):
> "The application can specify Extended Regular Expressions using the REG_EXTENDED cflags flag."

located at HTML lines 135-136.

Additional located quotes (each ≤25 words):
- HTML line 122: `REG_EXTENDED` → "Use Extended Regular Expressions."
- HTML line 131: `REG_NOSUB` → "Report only success/fail in regexec()."
- HTML lines 237-238: `REG_NOMATCH` → "regexec() failed to match."
- HTML line 196 (spec example): `regcomp(&re, pattern, REG_EXTENDED|REG_NOSUB)`.

### S501 — upstream mako v1.11.0 tag tarball (whole tree)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S501 | upstream mako v1.11.0 source tree — tag tarball https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0 (sha256 72d11d3fca20a3dfbca0107ff875eace479751be0cf2ddd1dd5bafa131ac7282, 67907 B; tag object 274aa303f69f7a5ecbc56c6db8746cb2fbbd487c, peeled commit 91c6b799855762ad1eb8b4498967c270a339be0c; two fetches byte-identical) — also main.c at https://raw.githubusercontent.com/emersion/mako/v1.11.0/main.c (sha256 2a09f5711e2c9fd09f47c3160e6397ee972783402189aca687c7830ab63e230c, identical to the tarball's main.c) | code | A | the upstream implementation of the mako release the host runs (mako 1.11.0-1): the criteria tokenizer, the regex compile flags, the match call, and the absence of any setlocale call in the whole tree | `grep -rn setlocale` over the extracted 59-file tree → no output, exit 1; `grep -rn locale` → no output, exit 1; main.c sha256 2a09f5711e2c9fd09f47c3160e6397ee972783402189aca687c7830ab63e230c (143 lines); criteria.c sha256 22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c — criteria.c:162-258 (parse_criteria tokenizer: quote state 184-197, backslash escape 177-182 and 201-203, space-only token split 207-215), criteria.c:332-351 (regcomp with REG_EXTENDED together with REG_NOSUB for summary~ and body~), criteria.c:47-58 (match_regex_criteria: regexec, REG_NOMATCH is the no-match verdict), criteria.c:542-550 ("Cannot set both `summary` and `summary~`" / "`body` and `body~`"); opened 2026-11-06 | Tier A because this is the pinned upstream implementation of the release the host runs, and it is the only place that shows both halves of the C1 premise: mako compiles the criterion with REG_EXTENDED together with REG_NOSUB and matches with regexec, and no file in the tree calls setlocale, so those libc calls run in the startup "C" locale | mined | 2026-11-06 | 180d | corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md |

Gate quote block (S501) — URL: `https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0` (tree) and
`https://raw.githubusercontent.com/emersion/mako/v1.11.0/main.c` (main.c) · access date: 2026-11-06 · primary quote (7 whitespace-separated tokens, two source lines 333-334 joined at the line break):
> "if (regcomp(&criteria->summary_pattern, value, REG_EXTENDED | REG_NOSUB)) {"

Additional located quotes (each ≤25 words):
- `criteria.c:345-346`: "if (regcomp(&criteria->body_pattern, value, REG_EXTENDED | REG_NOSUB)) {".
- `criteria.c:50` (match_regex_criteria): "if (ret != REG_NOMATCH) {".
- `criteria.c:543`: "Cannot set both `summary` and `summary~`" (and `:548` the `body`/`body~` twin).
- `criteria.c:186-187` (quote state, two source lines): line 186 `case '\\':` and line 187 `state = MAKO_PARSE_STATE_QUOTE_ESCAPE;` — the backslash escape inside quotes.
- `criteria.c:207-208` (normal state): "case ' ':" / "New token, apply the old one and reset our state." — the space-only split.

Negative evidence, reproducible (no quote; command + exit code): `grep -rn setlocale tree/mako-1.11.0/` → no output, grep exit 1;
`grep -rn locale tree/mako-1.11.0/` → no output, grep exit 1. "no file calls setlocale" is therefore a whole-tree fact, not a
main.c fact; main.c is recorded separately (sha256 above) only because the claim names it.

### S502 — glibc `<regex.h>` on this host

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S502 | glibc `<regex.h>` on this host, glibc 2.44+r50+g1848099f063e-1 installed (pacman -Qo /usr/include/regex.h → owned by glibc) — file:///usr/include/regex.h (sha256 ae656ea6032f59d670c8c1055e1eebcb93ddbc482fd26b333ed529d6a4784b97) | code | A | the numeric cflags this host's libc uses for REG_EXTENDED and REG_NOSUB, and the identity of REG_NOMATCH | line 310 `#define REG_EXTENDED 1`, line 323 `#define REG_NOSUB (1 << 3)`, line 377 `#define REG_NOMATCH _REG_NOMATCH` (enum at line 350); opened 2026-11-06 | Tier A because the header is the host's own glibc artifact: it fixes the exact integers a ctypes regcomp() call must pass for REG_EXTENDED and REG_NOSUB, and names REG_NOMATCH as the libc-side no-match constant | mined | 2026-11-06 | 180d | corpus/knowledge/mako-regex-criteria-r89.md,corpus/lessons/round-89.md |

Gate quote block (S502) — URL/path: `file:///usr/include/regex.h` · access date: 2026-11-06 · primary quote (3 tokens):
> "#define REG_EXTENDED 1"

located at line 310 (and `#define REG_NOSUB (1 << 3)` at line 323).

---

## 3. Rejected / not drafted

No source in the claim's list was rejected: all five listed sources (a)–(e) were opened and are drafted above (plus two
supporting rows, S499/S500 split and S502 header). One boundary is recorded instead of a row:

- **Not a row: "mako never calls setlocale" as a standalone upstream row.** It is a negative over a tree, not a quotable
  statement, so it rides inside S501's anchor with its reproducing command and exit code. If the L1 prefers it standalone it
  would need a `teaches` cell that quotes a command rather than a sentence, which the contract does not admit.
- **Not drafted: the mako(5) manual for round 89.** It is already S493 (`mako(5) manual text, mako 1.11.0-1 installed`) and
  round 87's knowledge entry cites it; re-opening it here would duplicate an existing mined row's URL and scope.

---

## 4. Commands run, with exit codes

Run from the seat scratch `S=/fast/scratch/hyaku/mado-r89/R89MScoutSources` (created with `mkdir -p`, `$HYAKU_SCRATCH`
defaulted to `/fast/scratch/hyaku`); scratch removed on exit. Every path is absolute.

| # | command | exit | result |
|---|---|---|---|
| 1 | `mkdir -p "$S"` | 0 | scratch created |
| 2 | `pacman -Q man-pages glibc mako` | 0 | man-pages 6.19-1 / glibc 2.44+r50+g1848099f063e-1 / mako 1.11.0-1 |
| 3 | `pacman -Qo /usr/include/regex.h` | 0 | owned by glibc 2.44+r50+g1848099f063e-1 |
| 4 | `pacman -Ql glibc \| grep include/regex.h` | 0 | `glibc /usr/include/regex.h` |
| 5 | `man -w regcomp` | 0 | `/usr/share/man/man3/regex.3.gz` |
| 6 | `man -w setlocale` | 0 | `/usr/share/man/man3/setlocale.3.gz` |
| 7 | `man -w regex` | 0 | `/usr/share/man/man3/regex.3.gz` (section 3 wins over section 7) |
| 8 | `man -w -s 7 regex` | 0 | `/usr/share/man/man7/regex.7.gz` |
| 9 | `zcat` each of the three man files → `.txt` | 0 | 403 / 244 / 375 lines; sha256 of texts recorded above |
| 10 | `sha256sum` man containers + `/usr/include/regex.h` | 0 | digests in the rows |
| 11 | `zcat … \| nl -ba \| sed -n …` on all three man pages | 0 | quoted line numbers |
| 12 | `MANWIDTH=100 man -P cat … \| col -bx` on all three man pages | 0 | rendered line numbers (248 / 127 / 149 lines) |
| 13 | `curl -sSL -o mako-v1.11.0.tar.gz https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0` | 0 | 67907 B, sha256 72d11d3f… |
| 14 | `tar -xzf mako-v1.11.0.tar.gz -C tree` | 0 | `tree/mako-1.11.0`, 59 files |
| 15 | `grep -rn setlocale tree/mako-1.11.0/` | **1** | no output — **no file calls setlocale** |
| 16 | `grep -rn locale tree/mako-1.11.0/` | **1** | no output — the string "locale" occurs nowhere in the tree |
| 17 | `grep -n setlocale main.c.v1110` (raw fetch) | **1** | no output in main.c (143 lines) |
| 18 | `curl -sSL -o main.c.v1110 https://raw.githubusercontent.com/emersion/mako/v1.11.0/main.c` | 0 | sha256 2a09f571…, identical to the tarball copy |
| 19 | `sha256sum` tarball, main.c (both copies), criteria.c | 0 | digests in S501 |
| 20 | `grep -n "regcomp\|regexec\|REG_" tree/mako-1.11.0/criteria.c` | 0 | 48, 50, 333-334, 345-346 |
| 21 | `grep -n REG_EXTENDED\|REG_NOSUB\|REG_NOMATCH /usr/include/regex.h` | 0 | 310, 323, 350, 377 |
| 22 | `curl -sSL -o posix-ch09.html https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html` | 0 | sha256 2f5f60e9…, 60438 B |
| 23 | `grep -c "REG_EXTENDED" posix-ch09.html` | 0 | **0** — chapter 9 names no flag (drives the S499/S500 split) |
| 24 | `grep -o "Extended Regular Expression\|REG_EXTENDED\|grep" posix-ch09.html \| sort \| uniq -c` | 0 | 4 / 0 / 2 |
| 25 | `curl -sSL -o posix-regcomp.html https://pubs.opengroup.org/onlinepubs/9799919799/functions/regcomp.html` | 0 | sha256 544ff826… |
| 26 | `nl -ba posix-ch09.html \| sed -n "30,40p;482,485p"` and `\| sed -n "372,416p"` | 0 | quoted HTML lines |
| 27 | `nl -ba posix-regcomp.html \| sed -n "121,122p;130,131p;135,136p;237,238p"` | 0 | quoted HTML lines |
| 28 | `curl` ×2 of each of the three network sources, then `cmp` the pairs | 0 (cmp) | all three byte-identical across two fetches |
| 29 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 0 | 430 rows; max id S495 → next free **S496** |
| 30 | `awk -F'|' … NF!=13` style column check on the drafted rows (written into this report, 11 cells, no `\|` inside a cell) | 0 | 11-column shape held |
| 31 | `curl -sSL https://api.github.com/repos/emersion/mako/git/ref/tags/v1.11.0` and `…/git/tags/274aa303…` | 0 | tag object 274aa303f69f7a5ecbc56c6db8746cb2fbbd487c → peeled commit 91c6b799855762ad1eb8b4498967c270a339be0c (same values S494 records) |
| 32 | `grep -n "codeload\|main\.c\|man7/regex\|V1_chap09\|functions/regcomp" corpus/SOURCES.md` | 0 | no existing row shares the drafted URLs (only S079 uses a codeload URL, for a different project); S494 stays valid, S501 adds scope at a different URL |

**Dead steps:** none. The one near-miss was `man -w regex`, which resolves to the section-3 `regex.3.gz`; the section-7 page was
reached explicitly with `man -w -s 7 regex` (exit 0).

---

## 5. Handoff notes for the L1

- Rows S496–S502 are drafted above in the contract's column order; `status` is `mined` for each, `opened` 2026-11-06.
- **`used-by` paths must exist when the rows are appended** (the frozen census checks mined rows' `used-by` paths). Two paths are
  proposed and do not exist yet: `corpus/knowledge/mako-regex-criteria-r89.md` and `corpus/lessons/round-89.md`. The L1 must
  create them under those names, or rename the cells to the names it actually writes — otherwise the census prints
  `missing: <path>`.
- If the L1 prefers fewer rows, S499 and S500 can merge into one row whose `teaches` cites the regcomp() page for the
  REG_EXTENDED↔ERE binding (the chapter-9 bytes cannot be quoted for it), and S502 can be dropped without losing a claim — but
  S501 should stay, because it is the only row carrying "no file calls setlocale".
- S494 is **not** superseded by S501: S494 keeps criteria/config semantics at the raw-file URLs, S501 adds the tokenizer and
  regex-compile scope plus the whole-tree locale fact at the tarball URL. No `teaches` cell changes, so no rule-2 correction row
  is needed.
- No counter was executed by this seat, so nothing here supports or weakens a TARGET_MET verdict.
