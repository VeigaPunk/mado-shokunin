# R88MScoutSources — round-88 source opening: upstream mako v1.11.0 code and path_resolution(7)

Seat: R88MScoutSources (scout), round 88 (hyaku run 15, attempt 1), wave w1.
Task: open the round's two new sources, pin the facts C1 and C2 rest on, draft the two registry
rows. No candidate tool was read, run or scored; no tool bytes, case file, counter or mutant file
was opened. This seat read only: the two named upstream source files, the two named man pages, the
SOURCES registry, and the claims declaration.

Scratch: `$HYAKU_SCRATCH/mado-r88/R88MScoutSources` (default `/fast/scratch/hyaku`), created with
`mkdir -p`, and deleted at the end of the seat (`rm -rf -- "$S"`, verified absent afterwards —
the directory no longer exists). No clone, no work tree, no fixture
repository was needed: every upstream byte was fetched over HTTPS with `curl -fsSL` into the
scratch directory. **No git or jj mutation was run anywhere.** The only git call is read-only
`git ls-remote` (no repository was created, no commit was made).

---

## 1. Source pinning

### 1.1 Upstream mako v1.11.0 (S494)

Tag existence — `git ls-remote https://github.com/emersion/mako refs/tags/v1.11.0` (read-only, exit 0):

| object | sha1 |
|---|---|
| `refs/tags/v1.11.0` (annotated tag object) | `274aa303f69f7a5ecbc56c6db8746cb2fbbd487c` |
| `refs/tags/v1.11.0^{}` (peeled commit) | `91c6b799855762ad1eb8b4498967c270a339be0c` |

Fetches — `curl -fsSL https://raw.githubusercontent.com/emersion/mako/v1.11.0/<file>`:

| file | HTTP | bytes | lines (`nl -ba`) | sha256 |
|---|---|---|---|---|
| `criteria.c` | 200 | 16018 | 573 | `22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c` |
| `types.c` | 200 | 8770 | 362 | `c2f3398d45877c10ae94a61634629c22b1c4c472b526a4963d45f7981c4734de` |
| `config.c` | 200 | 31263 | 1020 | `94c3a4e7b0bc7304dd9011c1e44d91cfffe417fe03aa3fa864205204f968ca12` |

Reproducibility: each file was fetched three times; all three copies are byte-identical
(`cmp` exit 0 per file). Each file was additionally re-fetched from the **peeled commit** URL
(`.../mako/91c6b799855762ad1eb8b4498967c270a339be0c/<file>`) and is byte-identical to the tag-URL
copy — the tag URL therefore resolves to the pinned commit, not to a moving branch.

All three files end with a newline; `wc -l` and the last `nl -ba` line number agree (573 / 362 /
1020), so the cited line numbers are the real file line numbers.

### 1.2 path_resolution(7) on this host (S495)

| item | value |
|---|---|
| file | `/usr/share/man/man7/path_resolution.7.gz` |
| container sha256 (`sha256sum`) | `2a21ab674e6f2c51f74c15b3709e2155873734cf867f8ffd2d1b3dec14d41077` |
| decompressed text sha256 (`zcat ... \| sha256sum`) | `2072681115cb012523b968eb243c5ba306ac68fca7f92d9e378949108921dc12` |
| decompressed size / lines | 9706 bytes / 266 lines (`zcat ... \| nl -ba`) |
| package version | `man-pages 6.19-1`; the page's own `.TH` line reads `path_resolution 7 2026-02-08 "Linux man-pages 6.19"` |

### 1.3 Host package versions — `pacman -Q mako man-pages` (read-only query, exit 0)

```
mako 1.11.0-1
man-pages 6.19-1
```

The host's installed mako is `1.11.0-1`, i.e. the same upstream release as the tag opened above:
the upstream code pinned in S494 is the code that defines the behaviour of the mako the host runs.

---

## 2. Located quotes (each ≤ 25 words, verbatim from the fetched bytes at the cited line)

Every quote below was re-checked programmatically against the fetched file at the cited line
(membership test on the exact line string); zero mismatches. C-source quotes are the trimmed
line contents; man-page quotes are the raw roff-source lines (the `.BR`/`.IP` markup lines are
cited, not a rendered view).

### (a) `match_criteria` compares the six string fields with `strcmp` — `criteria.c`

| file:line | quote | claim fact it grounds |
|---|---|---|
| `criteria.c:75-76` | `if (spec.app_name &&` / `strcmp(criteria->app_name, notif->app_name) != 0) {` | C1: app-name is exact string equality (baseline field) |
| `criteria.c:80-81` | `if (spec.app_icon &&` / `strcmp(criteria->app_icon, notif->app_icon) != 0) {` | C1: app-icon is exact string equality — one of the five added fields |
| `criteria.c:100-101` | `if (spec.category &&` / `strcmp(criteria->category, notif->category) != 0) {` | C1: category is exact string equality |
| `criteria.c:105-106` | `if (spec.desktop_entry &&` / `strcmp(criteria->desktop_entry, notif->desktop_entry) != 0) {` | C1: desktop-entry is exact string equality |
| `criteria.c:110-111` | `if (spec.summary &&` / `strcmp(criteria->summary, notif->summary) != 0) {` | C1: summary is exact string equality (not a prefix/substring rule) |
| `criteria.c:122-123` | `if (spec.body &&` / `strcmp(criteria->body, notif->body) != 0) {` | C1: body is exact string equality |

Each string field is gated by its own `spec.<field>` flag and compared with `strcmp(...) != 0`;
there is no case folding, no substring match and no regex on these six fields. `summary~`/`body~`
are separate regex fields (`criteria.c:332-351`, `regcomp(..., REG_EXTENDED | REG_NOSUB)`), which
is why the declaration can keep them as named limits.

### (b) `actionable` / `expiring` comparison lines — `criteria.c`

| file:line | quote | claim fact it grounds |
|---|---|---|
| `criteria.c:85-86` | `if (spec.actionable &&` / `criteria->actionable == wl_list_empty(&notif->actions)) {` | C1: actionable is a boolean comparison (true means "has actions"), not a string match |
| `criteria.c:90-91` | `if (spec.expiring &&` / `criteria->expiring != (notif->requested_timeout != 0)) {` | C1: expiring is a boolean comparison (true means "has a non-zero requested timeout") |

The upstream semantic of `actionable=true` is "the notification has at least one action"; the
upstream semantic of `expiring=true` is "the notification carries a non-zero requested timeout".
The resolver's boolean inputs must carry the same polarity, and the field names are exactly
`actionable` and `expiring` (`criteria.c:369`, `criteria.c:377`).

### (c) `apply_criteria_field` bare-key and `!` negation handling — `criteria.c`

| file:line | quote | claim fact it grounds |
|---|---|---|
| `criteria.c:267` | `bool apply_criteria_field(struct mako_criteria *criteria, char *token) {` | C1: the criteria field parser is `apply_criteria_field` |
| `criteria.c:269` | `char *value = strstr(key, "=");` | C1: the presence of `=` is what distinguishes a valued field from a bare key |
| `criteria.c:270` | `bool bare_key = !value;` | C1: a token with no `=` is a bare (boolean) key |
| `criteria.c:283` | `if (*key == '!') {` | C1: `!` is the negation marker on a bare key |
| `criteria.c:286` | `value = "false";` | C1: `!field` means false |
| `criteria.c:288` | `value = "true";` | C1: a bare field means true |

The negation is only reachable on the bare-key branch: a token containing `=` is split at the first
`=` and the value is taken verbatim, so `actionable=!true` is *not* a negation upstream. The
bare-key branch then falls through to the boolean fields at `criteria.c:369-408`, where an
unrecognised bare key is an error (`criteria.c:402-403`).

### (d) `types.c` `parse_boolean` — the upstream boolean grammar

| file:line | quote | claim fact it grounds |
|---|---|---|
| `types.c:19` | `bool parse_boolean(const char *string, bool *out) {` | C1: the single boolean entry point |
| `types.c:20` | `if (strcasecmp(string, "true") == 0 \|\| strcmp(string, "1") == 0) {` | C1: `true` is case-insensitive; `1` is exact — the manual's `0\|1` wording is narrower than upstream |
| `types.c:23` | `} else if (strcasecmp(string, "false") == 0 \|\| strcmp(string, "0") == 0) {` | C1: `false` is case-insensitive; `0` is exact |
| `types.c:28` | `return false;` | C1: anything else is refused, not guessed |

So the accepted upstream boolean literals are exactly: `true`/`TRUE`/`True`… , `1`, `false`/`FALSE`… ,
`0`. `strcasecmp` for the words, plain `strcmp` for the digits — so `01`, `yes`, `on` are refused.

### (e) `config.c` style boolean options go through `parse_boolean`

| file:line | quote | claim fact it grounds |
|---|---|---|
| `config.c:621` | `return spec->markup = parse_boolean(value, &style->markup);` | C1: the style-option booleans use the same `parse_boolean` as criteria booleans |
| `config.c:649` | `return spec->invisible = parse_boolean(value, &style->invisible);` | C1: `invisible=true` / `invisible=false` are upstream-valid — the host's DND config is upstream-valid, so refusing it is a lane rule, not a mako rule |
| `config.c:592-593` | `return spec->icons =` / `parse_boolean(value, &style->icons);` | C1: `icons` takes the same grammar (guarded by `HAVE_ICONS`) |
| `config.c:644` | `parse_boolean(value, &style->ignore_timeout);` | C1: `ignore-timeout` too |
| `config.c:651` | `return spec->history = parse_boolean(value, &style->history);` | C1: `history` too |

The full set of `parse_boolean` call sites in `config.c` is lines 593, 621, 623, 644, 649, 651 —
`icons`, `markup`, `actions`, `ignore-timeout`, `invisible`, `history`. This is the fact that makes
the C1 host-config case decidable: the manual documents `invisible=0|1` (manual line 545), but
upstream accepts `true`/`false` for the same option, and the host's own mako config writes
`invisible=true`.

### (f) `config.c` include handling — expansion, open, and the absence of any containment

| file:line | quote | claim fact it grounds |
|---|---|---|
| `config.c:505` | `static char *expand_config_path(const char *path) {` | C2: the only path transformation applied to an include target |
| `config.c:506` | `if (strncmp(path, "/", 1) == 0) {` | C2: an absolute include path is taken unchanged |
| `config.c:507` | `return strdup(path);` | C2: absolute paths are not rewritten at all |
| `config.c:510` | `if (strncmp(path, "~/", 2) != 0) {` | C2: the only syntactic restriction is that a non-absolute path must start with `~/` |
| `config.c:511` | `fprintf(stderr, "Config path must start with / or ~/\n");` | C2: the refusal message confirms the restriction is *syntactic form*, not location |
| `config.c:515` | `const char *home = getenv("HOME");` | C2: `~/` is expanded against `$HOME` textually |
| `config.c:521` | `return mako_asprintf("%s/%s", home, path + 2);` | C2: the expansion is a plain string concatenation — no `realpath`, no `..` folding, no symlink read |
| `config.c:545` | `} else if (strcmp(name, "include") == 0) {` | C2: `include` is a config option, handled here |
| `config.c:546` | `char *path = expand_config_path(value);` | C2: the include target goes through `expand_config_path` and nothing else |
| `config.c:547` | `return path && load_config_file(config, path) == 0;` | C2: the expanded path is handed straight to the loader |
| `config.c:781` | `FILE *f = fopen(path, "r");` | C2: the file is opened by that path — the kernel resolves whatever it points at |

**Plain statement of (f): upstream mako contains no containment, no symlink restriction and no
prefix restriction on `include=`.** Verified by exhaustion over the three fetched files: the
identifiers `realpath`, `canonicalize`, `readlink`, `lstat`, `S_ISLNK` and `O_NOFOLLOW` occur
**nowhere** in `criteria.c`, `types.c` or `config.c` (`grep` exit 1, no matches). The only
`has_prefix` helper in `config.c` (`config.c:553`) is used for `on-` style-option names
(`config.c:682`) and for `invoke-action ` / `exec ` binding values (`config.c:697`, `config.c:700`)
— it never touches a path. `config.c:6` includes `<wordexp.h>` but the file never calls
`wordexp`/`wexp` (the only occurrence of the identifier is the `#include` line itself), so no
shell-style expansion or globbing happens either.

Therefore: **the C2 containment stance is a lane stance, not an upstream mako rule** — exactly as
the declaration states. Upstream will open any absolute path, and will follow any symlink the
kernel resolves; a lane-side containment test is a stricter rule the tool adds, and its
justification must come from the lane's own trust boundary (and mado's credential-material rule),
not from mako.

Two further upstream facts that the C2 case file needs, both read from the fetched bytes:

- **Include is a top-level option only.** `config.c:863-869`: a line is first offered to
  `apply_style_option`; `apply_config_option` (which owns `include`) is consulted only
  `if (!valid_option && section == NULL)`. An `include=` inside a criteria section is therefore
  not an include — it is an unparsable option (`config.c:871-877`).
- **Include chains are unbounded upstream.** `load_config_file` calls `apply_config_option`, which
  calls `load_config_file` again (`config.c:547`), and `config.c` contains no depth, nesting or
  recursion guard (`grep` for `depth|recursi|nest` → exit 1, no matches). A chained include whose
  second hop escapes is reachable upstream; the lane must decide what to do with it.

### (g) Is the `summary` / `summary~` conflict enforced in code? — yes

| file:line | quote | claim fact it grounds |
|---|---|---|
| `criteria.c:542` | `if (criteria->spec.summary && criteria->spec.summary_pattern) {` | C1: the conflict is checked in code, not only in the manual |
| `criteria.c:543` | `fprintf(stderr, "Cannot set both \`summary\` and \`summary~\`\n");` | C1: setting both is an error, not a last-wins |
| `criteria.c:547` | `if (criteria->spec.body && criteria->spec.body_pattern) {` | C1: same for body |
| `criteria.c:548` | `fprintf(stderr, "Cannot set both \`body\` and \`body~\`\n");` | C1: same for body |

The check lives in `validate_criteria` (`criteria.c:498`), which `config.c` calls when a section
closes (`config.c:834`) and once more at end of file (`config.c:882`), and it returns `false`
(`criteria.c:544`, `criteria.c:549`) — so the conflicting configuration is rejected, not resolved
by a precedence rule. The manual states the same conflict in prose (manual lines 447-451,
453-457).

### (h) `path_resolution(7)` quotes (S495)

| file:line | quote | claim fact it grounds |
|---|---|---|
| `path_resolution.7.gz:77-80` (text lines 77-80) | `If the component is found and is a symbolic link,` / `we first resolve this symbolic link` / `(with the current lookup directory` / `as starting lookup directory).` | C2: every non-final path component that is a symlink is resolved before the walk continues — a symlinked *directory* component changes where the rest of the path is looked up |
| `path_resolution.7.gz:137-139` (text lines 137-139) | `By convention, every directory has the entries "." and "..",` / `which refer to the directory itself and to its parent directory,` / `respectively.` | C2: `..` is a directory-parent operation, evaluated at resolution time |
| `path_resolution.7.gz:141-143` (text lines 141-143) | `The path resolution process will assume that these entries have` / `their conventional meanings, regardless of whether they are` / `actually present in the physical filesystem.` | C2: `..` is folded even where no `..` entry exists on disk — a containment test cannot be satisfied by a lexical check on the written path |
| `path_resolution.7.gz:145` (text line 145) | `One cannot walk up past the root: "/.." is the same as "/".` | C2: `..` at the root is clamped, so `~/..` is a real parent path, not an error |
| `path_resolution.7.gz:170-172` (text lines 170-172) | `If the last component of a pathname is a symbolic link, then it` / `depends on the system call whether the file referred to will be` / `the symbolic link or the result of path resolution on its contents.` | C2: the final component is followed by `open` but not by `lstat` — the containment decision must be made on the *resolved* path, not on the link |
| `path_resolution.7.gz:175-178` (text lines 175-178) | `will operate on the symbolic link,` / `while` / `operates on the file pointed to by the symbolic link.` | C2: the `lstat`/`stat` contrast that shows the final-link case is call-dependent |

(Line numbers are those of `zcat /usr/share/man/man7/path_resolution.7.gz | nl -ba`, i.e. of the
roff source. The two mismatch lines caught while checking were 176-177, whose raw text is
`while` / `.BR stat (2)`; the quote above is reproduced across the 175-178 span without
misreporting a line number.)

The consequence for C2's stance text: "fully resolved path (realpath: every symlink and `..`
resolved)" is exactly what the kernel does at `open` time, per these lines. A test that compares
the *written* include path against a declared root would be defeated by a symlinked directory
component (77-80) and by `..` (141-145); the test has to compare the resolved path.

### Cross-check against the manual (S493, already held — not re-opened as a new row)

Read for cross-checking only, from the already-held manual bytes
(`/usr/share/man/man5/mako.5.gz`, text sha256 `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba`):

- manual lines 443-471 list the twelve first-pass criteria fields: app-name, app-icon, summary,
  summary~, body, body~, urgency, category, desktop-entry, actionable, expiring, mode. The
  upstream `types.c` `parse_criteria_spec` (`types.c:192-219`) knows a wider set (it also lists
  group-index, anchor, output, none) because it serves the second-pass and group-by specs too;
  the twelve-field list in the manual is the first-pass section-header set.
- manual line 545 documents `invisible=0|1`, while upstream `config.c:649` accepts
  `true`/`false` through `parse_boolean`. This is the manual-vs-upstream gap C1 leans on, and it
  is a real gap in the manual's wording, not in upstream's behaviour.
- manual lines 45-48 document `include=` and the same absolute-or-`~/` restriction that
  `config.c:510` enforces; the manual is silent on containment, exactly as upstream is.

---

## 3. Draft registry rows (11-column shape, as in the S493 row)

Both rows parse as 11 columns (13 pipe-delimited fields including the leading and trailing
empty fields — the census's `NF==13` check). No cell contains a literal `|`. Checked with
`awk -F'|' '{print NF}'` on the drafted lines: 13 for both. No duplicate URL: `grep -n
'emersion/mako\|path_resolution' corpus/SOURCES.md` exits 1 (no match), so neither the upstream
repository nor `path_resolution` appears anywhere in the registry yet, and no `W04` duplicate-URL
warning is expected.

**S494** (kind `code`; tier **A**):

```
| S494 | upstream mako v1.11.0 source — criteria.c, types.c, config.c at tag v1.11.0 (tag object 274aa303f69f7a5ecbc56c6db8746cb2fbbd487c, peeled commit 91c6b799855762ad1eb8b4498967c270a339be0c) — https://raw.githubusercontent.com/emersion/mako/v1.11.0/criteria.c (also types.c, config.c) | code | A | upstream implementation of the mako release the host runs (mako 1.11.0-1): criteria field semantics, boolean grammar, and config include handling | criteria.c:75-76,80-81,100-101,105-106,110-111,122-123 (six string fields compared with strcmp), criteria.c:85-86,90-91 (actionable and expiring compared as booleans), criteria.c:267-290 (bare key and ! negation), types.c:19-28 (parse_boolean), config.c:621,649,592-593 (style booleans use parse_boolean), config.c:505-521,545-547,780-781 (include expansion and open), criteria.c:542-548 (summary and summary~ conflict is an error); sha256 criteria.c 22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c, types.c c2f3398d45877c10ae94a61634629c22b1c4c472b526a4963d45f7981c4734de, config.c 94c3a4e7b0bc7304dd9011c1e44d91cfffe417fe03aa3fa864205204f968ca12; opened 2026-11-06 | Tier A because the pinned upstream implementation is the code that defines the behaviour of the mako version the host runs, so it is the authority for the exact-match and boolean facts C1 rests on. match_criteria compares app-name, app-icon, category, desktop-entry, summary and body with strcmp and actionable and expiring as booleans; parse_boolean accepts true and false case-insensitively and 1 and 0 exactly and refuses everything else, and a bare key means true while a leading ! means false; include= expands only absolute and ~/ paths, is opened with fopen, and carries no containment, symlink or prefix restriction upstream | mined | 2026-11-06 | 180d | corpus/knowledge/mako-fields-containment-r88.md,corpus/lessons/round-88.md |
```

**S495** (kind `docs`; tier **A**):

```
| S495 | path_resolution(7) on this host, man-pages 6.19-1 installed — file:///usr/share/man/man7/path_resolution.7.gz (container sha256 2a21ab674e6f2c51f74c15b3709e2155873734cf867f8ffd2d1b3dec14d41077; text sha256 2072681115cb012523b968eb243c5ba306ac68fca7f92d9e378949108921dc12) | docs | A | kernel pathname resolution on this host: symlink resolution of path components, dot-dot handling, and the final component as a symlink | lines 77-80 (a symlinked non-final component is resolved before the walk continues), lines 137-143 (dot and dot-dot have conventional meanings and are assumed even when absent on disk), line 145 (cannot walk up past the root), lines 170-178 (a final symbolic link is followed by stat and open but not by lstat); decompressed text 9706 bytes and 266 lines; opened 2026-11-06 | Tier A because the kernel's own documented path-resolution semantics are the normative rule for what a resolved include path is, and C2's stance states its containment test in exactly those terms. Every symlinked component is resolved during the walk and .. is folded at resolution time, so a containment test must compare the resolved path rather than the written one; the final component is followed by the open that mako performs, which is why a symlinked include escapes a lexical prefix check | mined | 2026-11-06 | 180d | corpus/knowledge/mako-fields-containment-r88.md,corpus/lessons/round-88.md |
```

Note on the S495 URL: the source cell uses the `file://` form, as S493 does for the mako manual.
`url_of()` in `scripts/sources-census.sh` matches only `https?://`, so this row contributes no URL
and raises no duplicate-URL finding; the upstream mako URL in S494 is the only new URL and is
unique in the registry.

**Census validation of the two drafted rows.** The two drafted lines were extracted from this
report, inserted into a scratch copy of `corpus/SOURCES.md` immediately after the S493 row (inside
the `## Registry` section, which the census requires — appending them at the end of the file
produces `E12 row outside Registry section`), and the census was run against that scratch copy:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file "$S/censustest/corpus/SOURCES.md" --today 2026-11-06
```

Result: **zero findings name S494 or S495** (`grep -c 'S494\|S495'` → 0 over the 657-line finding
output) — no `E01` field count, no `E02`/`E03` id, no `E05` kind, `E06` tier, `E07` status, `E08`
opened, `E09` recheck, no `E04`/`W04` duplicate URL, and no `W03` mined-but-unused. The census
exited 1, but every finding in that output is a pre-existing `E11 missing used-by` (or a standing
`W04`/`W01`) against other rows of the scratch copy — the sandbox holds only two stub used-by
files, so it is not a valid run of the real registry.

**Dependency for the L1 (E11).** The census's `E11` check requires every `used-by` path of a
`mined` row to exist. Neither `corpus/knowledge/mako-fields-containment-r88.md` nor
`corpus/lessons/round-88.md` exists yet on this lane (checked: both absent). Until the L1 authors
those two files, S494 and S495 will each raise one `E11 missing used-by` in the real registry.
That is an ordering fact for the integrator, not a defect in the rows: the used-by values are
fixed by the declaration, and the rows must not be admitted before the two target files exist.

---

## 4. Gate blocks

### Gate — S494 (upstream mako v1.11.0 source)

- URL: `https://raw.githubusercontent.com/emersion/mako/v1.11.0/criteria.c`
  (companions at the same tag: `.../types.c`, `.../config.c`; commit-pinned equivalents at
  `https://raw.githubusercontent.com/emersion/mako/91c6b799855762ad1eb8b4498967c270a339be0c/<file>`,
  byte-identical)
- Tag existence: `git ls-remote https://github.com/emersion/mako refs/tags/v1.11.0` →
  `274aa303f69f7a5ecbc56c6db8746cb2fbbd487c`, peeled `91c6b799855762ad1eb8b4498967c270a339be0c`
  (exit 0)
- Access date: 2026-11-06. HTTP 200 for each of the three files; sha256 and byte sizes in §1.1;
  three fetches byte-identical.
- Located quote (`criteria.c:110-111`, 13 words):
  `"if (spec.summary && strcmp(criteria->summary, notif->summary) != 0) {"`
- Located quote (`types.c:20`, 13 words):
  `"if (strcasecmp(string, \"true\") == 0 || strcmp(string, \"1\") == 0) {"`
- Located quote (`config.c:781`, 6 words): `"FILE *f = fopen(path, \"r\");"`
- Negative finding (quote-worthy for C2): the identifiers `realpath`, `canonicalize`, `readlink`,
  `lstat`, `S_ISLNK`, `O_NOFOLLOW` occur nowhere in the three fetched files — upstream has no
  containment for `include=`.

### Gate — S495 (path_resolution(7) on this host)

- URL / locator: `file:///usr/share/man/man7/path_resolution.7.gz` (installed man page; upstream
  man-pages project, version `man-pages 6.19-1`, page `.TH` line
  `path_resolution 7 2026-02-08 "Linux man-pages 6.19"`)
- Access date: 2026-11-06. Container sha256 `2a21ab674e6f2c51f74c15b3709e2155873734cf867f8ffd2d1b3dec14d41077`;
  decompressed text sha256 `2072681115cb012523b968eb243c5ba306ac68fca7f92d9e378949108921dc12`
  (9706 bytes, 266 lines).
- Located quote (text lines 77-80, 19 words):
  `"If the component is found and is a symbolic link, we first resolve this symbolic link (with the current lookup directory as starting lookup directory)."`
- Located quote (text line 145, 11 words): `"One cannot walk up past the root: \"/..\" is the same as \"/\"."`
- Located quote (text lines 170-172, 24 words):
  `"If the last component of a pathname is a symbolic link, then it depends on the system call whether the file referred to will be the symbolic link or the result of path resolution on its contents."`

---

## 5. Facts pinned for the claims (one line each)

- **C1 field semantics.** Upstream `match_criteria` compares app-name, app-icon, category,
  desktop-entry, summary and body by `strcmp` exact equality, and compares actionable and expiring
  as booleans — `criteria.c:75-123`.
- **C1 boolean grammar.** `parse_boolean` (`types.c:19-28`) accepts `true`/`false`
  case-insensitively and `1`/`0` exactly; every style boolean option in `config.c` (icons, markup,
  actions, ignore-timeout, invisible, history) goes through it — `config.c:593,621,623,644,649,651`.
  The manual's `invisible=0|1` (manual line 545) is narrower than upstream, so `invisible=true`
  from the host's own mako config is upstream-valid.
- **C1 bare key and `!`.** `apply_criteria_field` treats a token without `=` as a boolean field:
  a leading `!` yields `"false"`, otherwise `"true"` — `criteria.c:267-290`; negation is
  unreachable on a token that contains `=`.
- **C1 named limits.** `summary~`/`body~` are POSIX extended regexes (`criteria.c:332-351`) and
  upstream *errors* on setting `summary` together with `summary~` (and `body` with `body~`) —
  `criteria.c:542-549`.
- **C2 stance origin.** Upstream `include=` expands only `/`-absolute and `~/` paths
  (`config.c:505-521`) and opens the result with `fopen` (`config.c:781`) with **no** containment,
  symlink or prefix restriction anywhere upstream. Containment is therefore a lane stance, and its
  authority is S495, not mako.
- **C2 resolution semantics.** The kernel resolves symlinked components and folds `..` during the
  walk (`path_resolution(7)` text lines 77-80, 137-145) and follows the final component for
  `open`/`stat` but not `lstat` (text lines 170-178) — the containment test must compare the
  resolved path.
- **C2 upstream reach.** `include` is honoured only at top level (`config.c:866-869`) and include
  chains are unbounded upstream (`config.c:547` recurses; no depth guard in the file).

## 6. Dead steps and deviations

- No dead step: every command in this seat's item ran and returned the expected result. Exit
  codes: `pacman -Q` 0; `git ls-remote` 0; all `curl -fsSL` 0 with HTTP 200; `zcat`/`sha256sum` 0.
- Deviation from the item's wording, recorded for the L1: the item asks for "the `!` negation
  handling" under `apply_criteria_field` — upstream implements that negation in `criteria.c`
  (the criteria-field parser), **not** in `config.c`; `config.c` has no `!` handling at all. The
  two quotes above are therefore cited from `criteria.c:283-288`, not from `config.c`.
- No tool was installed or upgraded by this seat; no pacman transaction was run (only the
  read-only query `pacman -Q mako man-pages`).
- No credential material was read: the only host paths touched are the two named man pages. The
  host's mako config chain was not read by this seat.
