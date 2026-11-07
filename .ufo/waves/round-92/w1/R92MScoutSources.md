# R92MScoutSources — upstream sources for C1 (xdg-utils 1.2.1 resolver) and the Bash/Grep rules it replays

Seat `R92MScoutSources`, mado round 92, wave w1, base revision `d992ef7494b054591ee9104df1da49264678df5d`.
Scratch `S=$HYAKU_SCRATCH/mado-r92/R92MScoutSources` (= `/fast/scratch/hyaku/mado-r92/R92MScoutSources`), deleted on exit.
No measurement was run here: every digest below is a byte digest of a fetched file or an awk-extracted
function body. No candidate, control, counter or declaration was modified.

Deliverable: this report. Cited artifacts copied to
`.ufo/waves/round-92/w1/R92MScoutSources-fetch/` (upstream sources only, digests below):
`xdg-mime.in` (11e7d91e…), `xdg-utils-common.in` (1f6969b5…), `xdg-open.in` (a6b0c7af…),
`bashref.texi` (f3d37d57…), `grep.texi` (ea3c821a…).

---

## 1. Upstream xdg-utils v1.2.1 — fetch, digest, and installed/upstream function equality

### 1.1 Fetches (each URL fetched twice; both fetches byte-identical)

| file | URL | sha256 (both fetches) | rc |
|---|---|---|---|
| `scripts/xdg-mime.in` | `https://gitlab.freedesktop.org/xdg/xdg-utils/-/raw/v1.2.1/scripts/xdg-mime.in` | `11e7d91eebeeb9ae9f77c4cf66a837d5eba4ce91ef2fce105ff8fda786b95c7e` | 0 |
| `scripts/xdg-utils-common.in` | `…/raw/v1.2.1/scripts/xdg-utils-common.in` | `1f6969b54e012f75fea629eb54fd817ab8795b99ee0a28e2e819ffdaf19cc532` | 0 |
| `scripts/xdg-open.in` | `…/raw/v1.2.1/scripts/xdg-open.in` | `a6b0c7afd27300e633d674243d892978db81c625471b57183cc6f3331280790b` | 0 |
| tag archive | `https://gitlab.freedesktop.org/xdg/xdg-utils/-/archive/v1.2.1/xdg-utils-v1.2.1.tar.gz` | `f6b648c064464c2636884c05746e80428110a576f8daacf46ef2e554dcfdae75` | 0 |

All three digests equal the values named in the round-92 context; both fetches of each URL compared
equal (`cmp`, rc 0). The three scripts inside the tag archive are byte-identical to the three raw-file
fetches (`cmp`, rc 0) — the archive and the raw endpoint agree.

### 1.2 The installed script is upstream v1.2.1 plus its man page and the expanded common block

Whole-file `diff` of upstream `.in` against the installed script shows **insertions only, zero deletions**:

- `xdg-mime.in` (1079 L) vs `/usr/bin/xdg-mime` (1794 L, sha256 `a587107ff995a5f907ab1b731316a169348c6b0383caf8fd151ff21f89615f3f`):
  hunks `16a17,34`, `21a40,258`, `27a265,279`, `31a284,746` — the licence text, the rendered manual page,
  the rendered usage text, and the inlined common block; `grep -cE '^[0-9]+(,[0-9]+)?d'` = 0.
- `xdg-open.in` (671 L) vs `/usr/bin/xdg-open` (1267 L, sha256 `7d759d54f0d4ce1beeb34ee62c587985b5042374e8de237b0dcb8cd47aa698cf`):
  hunks `15a16,33`, `20a39,144`, `26a151,159`, `30a164,626`; deletions 0.
- The inlined common block is upstream `xdg-utils-common.in` with `@NAME@` substituted
  (`@NAME@` occurrences: 12, all in the `exit_failure_*`/`check_*` messages): installed
  `/usr/bin/xdg-mime:284-746` vs `sed 's/@NAME@/xdg-mime/g'` upstream → `diff` 0 lines over 463 lines;
  installed `/usr/bin/xdg-open:164-626` vs `sed 's/@NAME@/xdg-open/g'` → `diff` 0 lines over 463 lines.

### 1.3 The ten named functions are byte-identical (awk-extract both, diff)

`awk` extractor (`/^[A-Za-z_][A-Za-z0-9_]*\(\)[ \t]*$/` opens, a line `}` closes) applied to upstream and to
the installed script, then per-function `cmp`:

| function | upstream lines | installed lines | extracted body sha256 | identical |
|---|---|---|---|---|
| `defapp_generic` | `xdg-mime.in` 459-505 | `/usr/bin/xdg-mime` 1174-1220 | `9d5acb8b9f92f6f7b0d835d3d6f6220973c8f723d0b05f5b11a130977e1f99bb` | yes |
| `check_mimeapps_list` | `xdg-mime.in` 406-430 | `/usr/bin/xdg-mime` 1121-1145 | `c50ef763d8156b7ab2f5ef7abb9f76fb9c86d8eda679e1453b0f88ef5cacc70e` | yes |
| `defapp_fallback` | `xdg-mime.in` 372-404 | `/usr/bin/xdg-mime` 1087-1119 | `8fc7213ab9fabe7405431aa3982bfd37bb9b7ebeba69a561d83f9bb8113c30b6` | yes |
| `search_desktop_file` (mime) | `xdg-mime.in` 359-370 | `/usr/bin/xdg-mime` 1074-1085 | `ef7a3b65626ef8a3af753fafe6e4473ee03bac40efc943104d25df27fd9609be` | yes |
| `desktop_file_to_binary` | `xdg-utils-common.in` 55-90 | `/usr/bin/xdg-mime` 338-373 | `e63cf6ee7d650fd48170140dd8a85c716378b55e96a913f040cb805229b5fcfe` | yes |
| `xdg_realpath` | `xdg-utils-common.in` 427-463 | `/usr/bin/xdg-mime` 710-746 | `55f8fb5b1054d558c648d6ff6154dd909a3e6f0daa75272562cc0075101517b2` | yes |
| `detectDE` | `xdg-utils-common.in` 278-378 | `/usr/bin/xdg-mime` 561-661 | `9c670cc1bbf1582a0a9877ad0b2206bc033d218cb5d90c9a03fc3cfabc905787` | yes |
| `first_word` | `xdg-utils-common.in` 16-21 | `/usr/bin/xdg-mime` 299-304 | `d04eb4f85bc36969ad673a4ce4d322070f57f06cdd559040f5f0b10bfb0a9f86` | yes |
| `search_desktop_file` (open) | `xdg-open.in` 312-389 | `/usr/bin/xdg-open` 908-985 | `082305c72663b610f02413f820f768cb63b3553176d3e6ddb7742f82162e316f` | yes |
| `open_generic_xdg_mime` | `xdg-open.in` 392-412 | `/usr/bin/xdg-open` 988-1008 | `727561b3a582e76436f3b188886dcab43015a1c5407987f84a08106b70978c87` | yes |

(The body digest is of my extraction, not an upstream-published digest; it is reproducible from the two
fetched files with the awk extractor above.) This is the byte-level evidence behind S508's anchor clause
"the installed script's eight modelled functions are byte-identical to the tag".

### 1.4 Line ranges for the surfaces the declaration names (upstream `.in` line numbers)

`xdg-mime.in` (v1.2.1):

| surface | lines |
|---|---|
| query-default argument checks | 569-618 for the whole `query)` case; the `default)` branch is **593-612**, of which the mimetype argument check is **599-611** (`-*)` → "unexpected option", `*/*)` → ok, else "mimetype '$mimetype' is not in the form 'minor/major'"), and "mimetype argument missing" is 596-598; `unknown query type` is 614-616 |
| defapp dispatch | **712-729** — `detectDE` 713, the KDE-session-4/5 branch 715-717, `case "$DE"` 719-727 with `lxqt) defapp_lxqt` 720-722 and `*) defapp_generic` 724-726 |
| `check_mimeapps_list` | 406-430 (the `[Default Applications]` awk reader 425-441 is inside it; the `IFS=:` desktop loop 413-414, the `IFS=";"` app loop 442-450) |
| `defapp_generic` | 459-505 — config dirs 470-485, the `defaults.list`/`mimeinfo.cache` **grep at 493** (`grep "$MIME=" … \| head -n 1 \| cut -d '=' -f 2 \| cut -d ';' -f 1`), the fallback call 503 |
| `defapp_fallback` | 372-404 — the recursive `search_desktop_file` loop 388, the `InitialPreference` awk 389, the `-gt` comparison 392, `basename` 401 |
| `search_desktop_file` | 359-370 (`grep -l "$MIME;" "$dir/"*.desktop` at 365) |
| the `DE=""` → `generic` assignment that exists **only** in the `info` (filetype) branch | 684-688 — note it is *not* in the defapp branch, so an empty DE falls through the `*)` arm to `defapp_generic` |

`xdg-utils-common.in` (v1.2.1):

| surface | lines |
|---|---|
| `detectDE` | **278-378** — `XDG_CURRENT_DESKTOP` case 283-320 (Cinnamon, Enlightenment, GNOME\*, KDE, DEEPIN, LXDE, LXQt, MATE, XFCE, X-Generic; **no Hyprland**: `grep -ci hyprland` = 0), classic fallbacks 322-333 (incl. the D-Bus `org.gnome.SessionManager` probe 329-330), `$DESKTOP_SESSION` 335-351, `uname` 353-370, `DE="gnome3"` 371-373, flatpak 374-376 |
| `desktop_file_to_binary` | 55-90 — vendor-dash split 64-77, `Exec` grep + `first_word` **84**, `command -v` **85**, `xdg_realpath` **86** |
| `xdg_realpath` | 427-463 |
| `first_word` | 16-21 — `read first rest` (no `-r`) 19, `echo "$first"` 20; the comment at 18 says "No -r is intended here" |

`xdg-open.in` (v1.2.1):

| surface | lines |
|---|---|
| `open_generic_xdg_mime` (the xdg-open call site) | **392-412** — `default="$(xdg-mime query default "$filetype")"` at **395** |
| DE dispatch to it | `detectDE` **593**, `DE=""` → `generic` **595-596**, `case "$DE"` **611-670**, `generic) open_generic "$url"` **664-665** |
| `open_generic` | 477-527 — `filetype="$(xdg-mime query filetype "$file" | sed "s/;.*//")"` **486**, `open_generic_xdg_mime "$file" "$filetype" "$1"` **489** |
| `search_desktop_file` (open) | 312-389 |

**The declaration's premise, at source level.** On a session whose `XDG_CURRENT_DESKTOP` xdg-utils does not
know (Hyprland here: `XDG_CURRENT_DESKTOP=Hyprland`), `detectDE` leaves `DE` empty (no Hyprland arm), so
`xdg-open.in:595-596` sets `DE=generic` and `:664-665` calls `open_generic`, which asks
`xdg-mime query filetype` (486) and then `xdg-mime query default` (395). Inside xdg-mime the defapp branch
(`xdg-mime.in:712-729`) runs `detectDE` (713) and, with `DE` empty, takes the `*)` arm → `defapp_generic`
(725). `xdg-mime.in:686-688` would set `DE=generic`, but only in the `info` branch — it does not run for
`query default`. This is the exact dispatch C1 claims, now anchored to lines rather than to prose.

---

## 2. The Bash and Grep manuals

### 2.1 The named GNU endpoints were unreachable; what I opened instead

`https://www.gnu.org/software/bash/manual/bash.html` and `…/grep/manual/grep.html` (and the
`html_node/…` pages) **timed out from this host**: every attempt returned `curl: (28) Failed to connect to
www.gnu.org:443 after 133159 ms … Could not connect to server` (14 distinct attempts logged across three
runs: 65 s, 90 s, 135 s and 500 s connect windows; `curl` rc 28). `git.savannah.gnu.org` was likewise
unreachable (`curl: (28) Operation timed out after 110482 ms with 0 bytes received`, rc 28).

Three reachable routes to the *same* manual text were opened instead, all on **2026-11-06**:

1. **GNU release tarball `bash-5.3`** — `https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz`, two fetches
   byte-identical, sha256 `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`.
   **This digest equals the release-tarball digest already recorded in lane row S435's anchor**
   (`corpus/SOURCES.md:385`), so S435's pin is re-derived from a second route. Inside it:
   `doc/bashref.texi` (sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`, 11553 L),
   `doc/bashref.info` (`4edb431cb97126281be3f8e5038a5e3377177f97ab1ca3f6ad9809bd555e8654`),
   `doc/bashref.html` (`b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`).
2. **GNU release tarball `grep-3.12`** — `https://ftp.gnu.org/gnu/grep/grep-3.12.tar.gz`, two fetches
   byte-identical, sha256 `badda546dfc4b9d97e992e2c35f3b5c7f20522ffcbe2f01ba1e9cdcbe7644cdc`; inside:
   `doc/grep.texi` (sha256 `ea3c821a2f32284faac83088e3ba1b9aa541e7f8dd70543d3b9d0d79ffa4b725`, 2407 L,
   `doc/version.texi`: "UPDATED 2 January 2025", "EDITION 3.12"), `doc/grep.info`
   (`132fbe47be9b652aa1c1867498cd7d229bdf8b70b4168863551e4144f36e8257`).
3. **The maintainer copy already rowed as S489/S490** — `https://tiswww.case.edu/php/chet/bash/bashref.html`,
   two fetches byte-identical, sha256 `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`
   — **byte-identical to the release tarball's `doc/bashref.html`** (`cmp`, rc 0). So the URL S489/S490
   already hold is the *rendering of the same 5.3 release*, not a divergent text.

The host's own installed manuals agree with the release text word for word on every rule quoted below
(`/usr/share/info/bash.info.gz`, host bash 5.3.20-1; `/usr/share/info/grep.info.gz`, host grep 3.12-2 —
`/usr/bin/grep --version` reports "GNU grep 3.12-modified", sha256 `19280b0e0714dadf0c100cdbc7f4823d254dd8facba64deeff5ec50d39fecf84`; the shell's own `grep` is a builtin wrapper, so `grep(1)`/info digests are the pinned ones).

### 2.2 Located quotes for the rules the candidate models (each ≤ 25 words, verified verbatim in place)

Bash 5.3 (`doc/bashref.texi` of `bash-5.3.tar.gz`; rendered `bashref.info` section numbers in brackets):

| rule the candidate models | location | quote (word count) |
|---|---|---|
| IFS non-whitespace splitting | `bashref.texi:3026-3028` [§3.5.7 Word Splitting] | "any character in the value of @env{IFS} that is not IFS whitespace, along with any adjacent IFS whitespace characters, delimits a field" (22) |
| globbing of unquoted expansions | `bashref.texi:3058-3063` [§3.5.8 Filename Expansion] | "Bash scans each word for the characters @samp{*}, @samp{?}, and @samp{[}." (11) and "If one of these characters appears, and is not quoted, then the word is regarded as a @var{pattern}" (18) |
| `read` without `-r`, backslash handling | `bashref.texi:5568-5569` [§4.2 Bash Builtin Commands → `read`] | "The backslash character @samp{\} removes any special meaning for the next character read and is used for line continuation." (19) |
| `read -r` (the contrast the candidate models) | `bashref.texi:5629-5631` | "If this option is given, backslash does not act as an escape character." (13) |
| `command -v` prints a single word naming the command | `bashref.texi:5092-5094` [§4.2 → `command`] | "The @option{-v} option displays a single word indicating the command or file name used to invoke @var{command}" (17) |
| the builtin/keyword/function name vocabulary `command -v` must print | `bashref.texi:5701-5703` [§4.2 → `type`] | "@code{type} prints a single word which is one of @samp{alias}, @samp{keyword}, @samp{function}, @samp{builtin}, or @samp{file}" (15) |
| `echo` option handling | `bashref.texi:5224-5225` [§4.2 → `echo`] | "If @option{-n} is specified, the trailing newline is not printed." (10) |
| `test` returns 0/1 | `bashref.texi:4608-4609` [§4.1 Bourne Shell Builtins → `test`] | "Evaluate a conditional expression @var{expr} and return a status of 0 (true) or 1 (false)." (15) |
| `test -gt` integer operators | `bashref.texi:8391-8392` [§3.2 Bash Conditional Expressions] | "@code{OP} is one of @samp{-eq}, @samp{-ne}, @samp{-lt}, @samp{-le}, @samp{-gt}, or @samp{-ge}." (11) |

Grep 3.12 (`doc/grep.texi` of `grep-3.12.tar.gz`; rendered `grep.info` section numbers in brackets):

| rule the candidate models | location | quote (word count) |
|---|---|---|
| BRE `.` matches any one character | `grep.texi:1282` [§3.1 Fundamental Structure] | "The period @samp{.} matches any single character." (7) |
| BRE `*` is a repetition operator | `grep.texi:1302` [§3.1] | "The preceding item is matched zero or more times." (9) |
| BRE vs ERE: `? + { } \| ( )` lose their meaning | `grep.texi:1625-1626` [§3.6 Basic vs Extended Regular Expressions] | "The characters @samp{?}, @samp{+}, @samp{@{}, @samp{|}, @samp{(}, and @samp{)} lose their special meaning" (13) |
| BRE: a leading unescaped `*` is an ordinary character | `grep.texi:1645-1647` [§3.6] | "it is treated like an ordinary character and is not a repetition operator" (13) |
| binary files: output suppressed after NUL | `grep.texi:633-637` [§2.1 Command-line Options → `--binary-files`] | "suppresses output after null input binary data is discovered" (9) |
| usage: `.*` spans one line | `grep.texi:1873-1875` [§4 Usage] | "this is because @samp{.*} matches zero or more characters within a line." (12) |

Each quote was checked to occur verbatim at the stated lines (`bashref.texi`/`grep.texi`) by an exact
substring test over the joined lines; each also occurs in the rendered `.info` of the release and in the
host's installed `.info.gz` (verified for all 15). Host `grep(1)` (MANWIDTH=120 rendering) carries the same
sentences at lines 174-188 and 270/328-330 — the anchors S509/S510 already use.

**Not modelled by any quote above (recorded as a limit, not a finding):** `xdg-utils` uses `awk` (gawk 5.4.1-1)
for the `[Default Applications]` reader and the `InitialPreference` value, and coreutils `basename`; the
candidate models `awk -v` escape processing and `basename` too. I did not open the gawk or coreutils manuals
in this seat (out of the assigned scope), so no registry row is proposed for them — flagged below as a
coverage note for L1.

---

## 3. Registry move: re-opening S490

### 3.1 What S490 is, verbatim

`corpus/SOURCES.md:442` — id `S490`, source "Bash maintainer Reference Manual exit builtin —
https://tiswww.case.edu/php/chet/bash/bashref.html#Bourne-Shell-Builtins", kind `docs`, tier `A`,
scope "proposed numeric-status-only proof of producer termination cause", anchor "Edition5.3 section4.1 exit
builtin, exit n", teaches "REJECTED: exit141 alone cannot uniquely prove signal13 because explicit exit141
returns the same number; flip: separately observed termination metadata that distinguishes normal exit and
signal death.", status `rejected`, opened 2026-11-04, recheck `180d`, used-by
`corpus/lessons/round-85.md`.

### 3.2 The rule the item cites, stated exactly

`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118` rule 2 is **"Append-only. Only `status`, `recheck` and
`used-by` change in place, and each change is logged old→new in the round lesson. A correction is a new row
whose `teaches` opens `supersedes S0NN —`."** The "one URL per scope" constraint is not in CORPUS.md; it is
the census rule in `scripts/sources-census.sh`: `E04` (line 649) "duplicate url … within scope" is an
**error**, `W04` (line 645) "duplicate url … across scopes" is a **warning only** ("warnings do not affect
clean lanes", script header line 33). Both are keyed on the pair `url + scope`, not on the URL alone.
The lane's own collision-review rule is `corpus/QUALITY.md:34` (criterion 17) and
`corpus/lessons/round-26.md:55` ("one row, one URL").

### 3.3 The move: **a new row, not a used-by update on S490**

Reasoning, from the row text and the C1 claim:

1. **Different scope.** S490's scope is the *numeric-status-only proof of producer termination cause*; its
   teaches is a **rejection** of that inference, with a named flip condition ("separately observed
   termination metadata"). C1 asserts nothing about exit141 or SIGPIPE. The C1 claim rests on *shell
   semantics* (IFS splitting, pathname expansion, `read` without `-r`, `command -v` naming, `echo` options,
   `test -gt`) and on the *grep BRE* reading. Those are not S490's scope, so S490 is not the row C1 cites.
2. **Rule 1 (a row is a claim) + rule 2 (append-only).** The only in-place moves are `status`, `recheck`,
   `used-by`. A `used-by` append would assert that the C1 knowledge entry cites S490's *rejected* proposition
   about exit141 — false, and it would leave a rejected row pointing at a knowledge entry that never leans on
   it. The declaration and the scribe's draft agree on the substance: S490 "is *not* cited: it is a rejected
   row and this entry makes no exit-status-as-termination-cause claim"
   (`.ufo/waves/round-92/w1/R92MScribeEntry.md:13-14`).
3. **The census consequence.** The C1 shell-semantics scope is a *different scope* from S490's, so a new row
   at the same URL would be W04-only (warning, exit still 0) — not E04 — because E04 needs the same
   url+scope pair twice with a non-rejected row. Today the lane already carries exactly that warning:
   `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (rc 0) prints
   `mado W04 S490 duplicate url tiswww.case.edu/php/chet/bash/bashref.html across scopes` — S489 and S490
   share the maintainer URL at two scopes. 55 W04 lines, 0 E-lines.
4. **So S490 itself stays as it is.** Its verdict is untouched by round 92 (nothing here observes termination
   metadata), so `status` stays `rejected`, `recheck` stays `180d`, and `used-by` stays
   `corpus/lessons/round-85.md`. The *only* rule-2-legal in-place edit that round 92 could make to S490 is a
   `used-by` append naming `corpus/lessons/round-92.md` — **and only if the round-92 lesson records the
   re-open verification**. The C1 knowledge entry must **not** be added to S490's `used-by`.
5. **What the re-open does buy.** Re-reading the maintainer copy in round 92 produced a fact the registry
   does not yet record and which is *about* the S489/S490 URL: the maintainer HTML is **byte-identical**
   (sha256 `b91026ac…`) to the GNU 5.3 release's own `doc/bashref.html`. That makes the maintainer URL
   defensible as the release rendering, and it is the reason a *new* row may carry either URL without
   contradicting S489/S490.

**Recommendation to L1 (decide at integration, I did not edit `corpus/SOURCES.md`):**

- Keep S490 unchanged (`rejected`, `180d`, used-by `corpus/lessons/round-85.md`).
- If the round-92 lesson records "S490 re-opened; source re-read; verdict unchanged", append
  `corpus/lessons/round-92.md` to S490's `used-by` and log the old→new in that lesson (rule 2).
- The C1 shell-semantics ground belongs in **S509** (already committed: bash(1) on this host) and the grep
  ground in **S510** (already committed: grep(1) on this host); the upstream release text I opened is
  supplementary (§4 below), not a replacement.

---

## 4. Draft registry rows (11-column schema; report only — nothing written to `corpus/SOURCES.md`)

Schema: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

**Ids.** The registry's last id is `S510` (`corpus/SOURCES.md`, 445 rows; ids S508/S509/S510 already exist
and were committed in `243326cb`, so the declaration's "rows S508–S509" was overtaken by a third row).
The next unused id is **S511**. Rows below therefore start at S511, and they are *supplementary* to
S509/S510, not replacements.

### S511 (recommended)

| field | value |
|---|---|
| id | `S511` |
| source | GNU Bash 5.3 Reference Manual — upstream release tarball `https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` (sha256 `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`, two fetches byte-identical), `doc/bashref.texi` (sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`, 11553 lines), `doc/bashref.html` (sha256 `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4` — byte-identical to the maintainer copy `https://tiswww.case.edu/php/chet/bash/bashref.html` held by S489/S490) |
| kind | `docs` |
| tier | `A` |
| scope | the upstream wording of the shell rules the xdg-mime resolver's shell text depends on (IFS field splitting, pathname expansion of unquoted words, `read` without `-r`, `command -v` output), as distinct from the installed-man-page anchor S509 carries |
| anchor | `doc/bashref.texi` §3.5.7 Word Splitting 3026-3028; §3.5.8 Filename Expansion 3058-3063; §4.2 Bash Builtin Commands `command` 5092-5094 and `type` 5701-5703, `echo` 5224-5225, `read` 5568-5569 and `-r` 5629-5631; §4.1 Bourne Shell Builtins `test` 4608-4609; §3.2 Bash Conditional Expressions 8391-8392; opened 2026-11-06 because www.gnu.org refused the connection (curl rc 28, 14 attempts) |
| teaches | the upstream sentence for each rule the replay models, so a reader can check `ifs_split`, `pathexp`, `command_v` and `read_first` against the release text rather than only against a distro rendering |
| status | `queued` |
| opened | `2026-11-06` |
| recheck | `on-release` |
| used-by | `—` |

### S512 (recommended)

| field | value |
|---|---|
| id | `S512` |
| source | GNU grep 3.12 Reference Manual — upstream release tarball `https://ftp.gnu.org/gnu/grep/grep-3.12.tar.gz` (sha256 `badda546dfc4b9d97e992e2c35f3b5c7f20522ffcbe2f01ba1e9cdcbe7644cdc`, two fetches byte-identical), `doc/grep.texi` (sha256 `ea3c821a2f32284faac83088e3ba1b9aa541e7f8dd70543d3b9d0d79ffa4b725`, 2407 lines; `doc/version.texi`: EDITION 3.12, UPDATED 2 January 2025), `doc/grep.info` (sha256 `132fbe47be9b652aa1c1867498cd7d229bdf8b70b4168863551e4144f36e8257`) |
| kind | `docs` |
| tier | `A` |
| scope | the upstream BRE reading of the asked MIME type and the binary-file rule that the resolver's `grep` fallback runs under, as distinct from the installed-man-page anchor S510 carries |
| anchor | `doc/grep.texi` §3.1 Fundamental Structure 1282 (`.` matches any single character) and 1302 (`*` zero or more times); §3.6 Basic vs Extended Regular Expressions 1625-1626 and 1645-1647 (an unescaped leading `*` is an ordinary character); §2.1 `--binary-files` 633-637; §4 Usage 1873-1875; opened 2026-11-06 because www.gnu.org refused the connection (curl rc 28) |
| teaches | why an unanchored `TYPE=` still matches a `text/xzy=` cache line, why a leading `*` in a MIME type is literal rather than a repetition operator, and that grep suppresses output once NUL input is seen |
| status | `queued` |
| opened | `2026-11-06` |
| recheck | `on-release` |
| used-by | `—` |

### Why these are `queued`, not `mined`

A row is `mined` only when cited by ≥1 path in `used-by` (`CORPUS.md:112-115`, rule 1's status definition and
the census's E11 check: a `mined` row whose `used-by` path does not exist on disk is an **error**). Neither
S511 nor S512 is cited by any committed file today (the C1 knowledge entry
`corpus/knowledge/xdg-mime-default-resolution-r92.md` cites S508/S509/S510, not these), so `queued` with
`used-by = —` is the honest state. If L1 decides to cite them from the knowledge entry, the move is a
`queued → mined` status change plus the `used-by` path, each logged old→new in `corpus/lessons/round-92.md`
(rule 2). S511/S512 carry URLs not previously in the lane registry (`grep -c "ftp.gnu.org"` = 0), so they
add **no** W04 line; they also do not disturb S489/S490's existing W04.

**Alternative I considered and rejected:** folding the upstream manual anchors into S509/S510 by editing
their `anchor` cells. Rule 2 forbids it — only `status`, `recheck` and `used-by` change in place — so a
separate row is the only in-contract way to add the upstream anchor, and a separate row is also the honest
one: it is a different source document (the release tarball's manual source) with its own digests and its
own recheck cadence.

---

## 5. Coverage note for L1 (not a finding against the candidate)

The candidate's docstring (`.ufo/waves/round-92/build/mado-xdgmime.c1.py:20-21`) also models **gawk `-v`
escape processing** and **coreutils `basename`**, which `defapp_generic`/`defapp_fallback` really do use
(`awk` at `xdg-mime.in:493`, `basename` at `xdg-mime.in:401`). The lane registry currently holds **no row
for the gawk manual and none for coreutils** (`grep -in "gawk\|coreutils" corpus/SOURCES.md` → no rows;
the only `grep`-worded rows are unrelated). Those two rules are therefore not row-backed ground today. I did
not open those manuals (outside this seat's assigned scope), so I propose no row for them; flagging it so the
L1 can decide whether the C1 knowledge entry's shell-semantics section is fully row-covered without them.

---

## 6. Commands run (each with its exit code)

| command | rc |
|---|---|
| `curl -fsSL …/raw/v1.2.1/scripts/xdg-mime.in` (×2) | 0, 0 |
| `curl -fsSL …/raw/v1.2.1/scripts/xdg-utils-common.in` (×2) | 0, 0 |
| `curl -fsSL …/raw/v1.2.1/scripts/xdg-open.in` (×2) | 0, 0 |
| `curl -fsSL …/archive/v1.2.1/xdg-utils-v1.2.1.tar.gz` (×2) | 0, 0 |
| `sha256sum` of all seven fetched files; `cmp` of each fetch pair | 0 |
| `tar xzf` archive; `cmp` of the three archive scripts against the three raw fetches | 0 |
| `diff xdg-mime.in.fetch1 /usr/bin/xdg-mime`; `diff xdg-open.in.fetch1 /usr/bin/xdg-open` | 1 (differences, all insertions) |
| `cmp` of installed common region vs `@NAME@`-substituted upstream common (both scripts) | 0 |
| awk extract + `cmp` per function (10 pairs, §1.3) | 0 for every pair |
| `curl -fsSL https://www.gnu.org/software/bash/manual/bash.html` (14 attempts) | 28 (timeout) — **dead step**, replaced by ftp.gnu.org + maintainer copy |
| `curl -fsSL https://www.gnu.org/software/grep/manual/grep.html` (same attempts) | 28 — **dead step** |
| `curl -fsSL https://git.savannah.gnu.org/cgit/{grep,bash}.git/plain/doc/*.texi` | 28 — **dead step** |
| `curl -fsSL https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` (×2) | 0, 0 |
| `curl -fsSL https://ftp.gnu.org/gnu/grep/grep-3.12.tar.gz` (×2) | 0, 0 |
| `curl -fsSL https://tiswww.case.edu/php/chet/bash/bashref.html` (×2) | 0, 0 |
| `cmp` maintainer copy vs release `doc/bashref.html` | 0 (byte-identical) |
| quote-verbatim script over `bashref.texi`/`grep.texi` (15 quotes) | 0 (all FOUND) |
| `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 (55 W04, 0 E; `W04 S490 duplicate url tiswww.case.edu/php/chet/bash/bashref.html across scopes`) |
| `git log -1 -- corpus/SOURCES.md` | 0 (`243326cb`, contains S508–S510) |

**No tool was installed or upgraded in this seat** (nothing to record; no pacman transaction was attempted
under the round-92 PACMAN GUARD).

**Remaining unknowns.** (a) The `www.gnu.org` HTML manuals remain unopened from this host; the quotes are
located in the *release* manuals (byte-identical for bash to the maintainer copy) instead, and the URLs a
future reader would try first are the ones that time out — that is why S511/S512 are anchored on
`ftp.gnu.org` tarballs. (b) Whether the *installed* `bash(1)`/`grep(1)` man pages on this host differ in any
rule-relevant sentence from the release text was checked sentence-by-sentence for the fifteen quoted rules
only; other sentences were not compared. (c) The gawk and coreutils manuals behind the candidate's remaining
two modelled rules were not opened (see §5).

**Scratch.** `/fast/scratch/hyaku/mado-r92/R92MScoutSources` was deleted after the cited files were copied to
`.ufo/waves/round-92/w1/R92MScoutSources-fetch/`.
