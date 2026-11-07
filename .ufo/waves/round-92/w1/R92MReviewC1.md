# R92MReviewC1 — C1 candidate reviewed against xdg-utils v1.2.1 and bash 5.3 / grep 3.12 / gawk 5.4

Seat: reviewer, round-92 w1. Scope: review only (no edits to the lane). Everything below is either a
command I ran in this session or a line citation. DRAFT means the scoring rule of the wave context: no
receipt written, no measurement claimed.

## 0. Object identity (the target moved during the review)

| file | sha256 | note |
|---|---|---|
| candidate `build/mado-xdgmime.c1.py` | `4121d583d42fd5eead93034d78c8ee0cd86d557b223249bc7424cad1c705a8bd` | bytes I first read; draft run = DRAFT_TARGET_MET |
| candidate `build/mado-xdgmime.c1.py` | `b6497a0a0b395dc94402444a857d0cc8cc6e289f5f664447079ccb96db921fa3` (mtime 23:07:14, 761 lines) | **current**; snapshot reviewed, draft run = DRAFT_TARGET_MISSED |
| `xdg-mime.in` v1.2.1 | `11e7d91eebeeb9ae9f77c4cf66a837d5eba4ce91ef2fce105ff8fda786b95c7e` | matches the pin in the context |
| `xdg-utils-common.in` v1.2.1 | `1f6969b54e012f75fea629eb54fd817ab8795b99ee0a28e2e819ffdaf19cc532` | matches the pin |
| `xdg-open.in` v1.2.1 | `a6b0c7afd27300e633d674243d892978db81c625471b57183cc6f3331280790b` | matches the pin |
| installed `/usr/bin/xdg-mime` | `a587107ff995a5f907ab1b731316a169348c6b0383caf8fd151ff21f89615f3f` | `xdg-utils 1.2.1-2` |

The candidate was edited **during** this review (docstring + a new `TYPE_CHARS` gate, +9 lines). The first
draft run (77 s, exit 3) scored the 4121d583 bytes; every later run scores the b6497a0a snapshot
(`$S/cand-snapshot.py`, same bytes). The L1 must pin the hash it freezes; the two hashes do not have the
same verdict.

`diff` of the eight functions the candidate models, extracted from the *installed* `/usr/bin/xdg-mime` vs
the v1.2.1 sources — `search_desktop_file`, `defapp_fallback`, `check_mimeapps_list`, `defapp_generic`,
`first_word`, `desktop_file_to_binary`, `xdg_realpath`, `detectDE`: all **SAME** (exit 0). Arch's
1.2.1-2 carries no patch in any modeled function, so modelling the source and labelling with the installed
binary are consistent.

## 1. Findings by severity

### F1 (high) — the new RFC 6838 type gate contradicts the frozen L1 and kills the mutant leg

`cand-snapshot.py:67` `TYPE_CHARS = rb"[A-Za-z0-9!#$&^_.+/-]+"` and `:704` `if not TYPE_CHARS.fullmatch(mime):
raise Unsupported(... rc 2)`. `xdg-mime` accepts *any* non-empty `$2` that contains `/` and does not start
with `-` (`xdg-mime.in:592-608`), so four frozen answers now exit 2 with empty stdout:

| frozen case | type | oracle (frozen `expect`) | candidate |
|---|---|---|---|
| `f14-invalid-regex` | `text/[` | `None`, rc 0 | rc 2, stdout empty |
| `f17-star-in-type` | `text/p*lain` | `st.desktop`, rc 0 | rc 2, stdout empty |
| `g05-awk-v-escape` | `text/x\tz` (backslash-t) | `a.desktop`, rc 0 | rc 2, stdout empty |
| `g06-awk-v-escape-defaults` | `text/x\tz` | `t.desktop`, rc 0 | rc 2, stdout empty |

Reproduce: `f17` fixture is `share/applications/mimeinfo.cache` = `[MIME Cache]\ntext/plain=st.desktop;\n`
with `PATH={ROOT}/bin:/usr/bin`, `XDG_CURRENT_DESKTOP=Hyprland`; `xdg-mime query default 'text/p*lain'`
prints `st.desktop` because the BRE `p*` matches `p` (`g05`/`g06` are the gawk `-v` `\t` → TAB and the grep
`\t` → `t` cases).

DRAFT counter on the snapshot (`--draft-tool`, exit **3**, `MADO_XDGMIME_DEFAULT` line quoted in §3):
`correct=124/128` (f=19/21, g=4/6), `answered=124/128`, and **`killed=38/39` with `M36
crashed-not-killed wrong=0 crashed=4`**. M36 rewrites `pre = awk_v(mime) + b"="` → `pre = mime + b"="`; on
every type the gate admits there is no backslash, so `awk_v` is the identity and the mutant can never be
killed. The gate therefore *structurally* guarantees at least one survivor.

Same hash, `--draft-tool`, one 47 s run; the 4121d583 bytes had scored `correct=128/128`, `killed=39/39`.

Consequences the L1 must settle before the freeze:
1. remove the gate and model the remaining grep/gawk corners, or
2. regenerate the frozen case file without those types — which deletes exactly the BRE/gawk coverage that
   `f14/f17/g05/g06` exist to test and makes the docstring's "GNU grep BRE, gawk `-v` escapes" vacuous,
   and *still* leaves M36 unkillable (rewrite the mutant file too), or
3. amend the declaration's predicate and Count — it currently says "for every asked type" (§2) and
   "MIME types a lane tool answers …: 0 → **every type**".

Also note the whole-case effect: `main` catches `Unsupported` outside the type loop (`:748-751`), so one
refused type discards the answers already computed for its sibling types in the same argv.

### F2 (medium) — `pathexp` mis-models a backslash before a glob metacharacter in an expansion result

`cand-snapshot.py:195` `lit = re.sub(rb"\\(.)", rb"\1", comp)` strips the backslash from a component that
`glob_rx` marked non-special. bash keeps that backslash (quote removal already happened) and only *quotes*
the following character, so the word is returned verbatim.

Fixture `rv-glob-backslash-star` (in `w1/R92MReviewC1-fixtures.json`): `XDG_CONFIG_HOME={ROOT}/c\*` with a
directory literally named `c*` holding `mimeapps.list` = `[Default Applications]\ntext/plain=a.desktop\n`,
`XDG_DATA_HOME={ROOT}/data` with `applications/a.desktop` (`Exec=a %U`) and `bin/a`.

- oracle (`/usr/bin/xdg-mime`, labelled in `$S`): `None`, rc 0 — bash expands the word to `{ROOT}/c\*`
  (the star is quoted by the backslash), no such directory, phase skipped.
- candidate: `a.desktop`, rc 0 — it un-escapes to `c*`, finds the directory, reads the list.

Not reached by the frozen set (0/128) or by the frozen fuzz generator (`TYPES`/`DIRS_*` contain no
backslash), so it is latent. Same class in `glob_rx` (`:150-152`): a backslash is *dropped* while the next
char is escaped, whereas bash keeps it. Both happen only in unquoted expansions (`$XDG_*`, the desktop
list, app ids, `$(search_desktop_file …)`), never in quoted positions.

### F3 (low) — a `--help` / `--manual` *type* is refused, while xdg-mime answers it

`cand-snapshot.py:696-697`. `check_common_commands "$@"` (`xdg-utils-common.in:235-262`) scans every
argv element, so `xdg-mime query default --help` prints the usage text and exits 0, and `--manual` prints
the manual page and exits 0 (oracle-labelled: `rv-type-help` default = the usage text, rc 0; `rv-type-manual`
= the manual, rc 0). The candidate exits 2 with empty stdout. Undeclared: the docstring's scope list
(`:23-25`) does not contain it. Reachable — the counter passes `--` before the types.

### F4 (low) — `PATH` unset is refused, while xdg-mime answers

`cand-snapshot.py:700-701`. With `PATH` absent bash uses its compiled-in default path, so xdg-mime still
finds `grep`/`awk`/`realpath` and resolves normally: `rv-path-unset` oracle = `a.desktop`, rc 0; candidate
rc 2. Undeclared in the docstring scope list (the only mentioned PATH item is the "assumed" reaches-utilities
line). The oracle schema says "PATH must be present", so the frozen and fresh legs never hit it.

### F5 (low) — declaration premise numbers are not reproducible from the frozen artifacts; the scope list is docstring-only

- §2 "the GLib resolver at the base revision scores **56/123** of the draft cases (`glib_resolver_correct=56`)".
  Re-run on the frozen file (128 cases, 131 answers): `glib_resolver_correct=59` in both independent draft
  runs, alongside `do_nothing_correct=33` and `naive_mimeapps_correct=44`. So 56/123 describes an earlier
  draft case file, not the frozen one; the direction of the premise ("the two resolvers disagree") holds
  (59/128 is far below 128), but the number should cite the frozen file or the file it was measured on.
- The declaration confers no type restriction and its Count says "every type"; the candidate refuses types
  outside RFC 6838. The declaration must inherit the scope list or drop the refusal (F1).
- `XDG_UTILS_DEBUG_LEVEL set` is refused (`:744-747`) though xdg-mime's answer does not depend on it: with
  `XDG_UTILS_DEBUG_LEVEL=1` the oracle still prints `app2.desktop` rc 0 for the same fixture (`rv-debug-level`,
  labelled). It is declared in the docstring, so this is a declared conservative refusal, not a divergence —
  but it is another place where "answers every type" is not what the tool does. Same for a *non-empty*
  `XDG_UTILS_REALPATH_BACKEND` (declared; the only observable is existence, so the refusal is conservative).

Verified premises: `git grep -l defapp_generic d992ef74 -- tools corpus` empty (rc 1); `git cat-file -e
d992ef74:tools/mado-xdgmime.py` rc 128 (tool absent) → `base_tool=absent, base_tool_correct=0`;
`tools/mado-mime.py` present at base; `open_generic_xdg_mime` (`xdg-open.in:391-397`) really runs
`xdg-mime query default "$filetype"`, and `open_generic` reaches it for an unknown DE with a display
(`:478-500`).

## 2. Function-by-function audit

Every row names the upstream lines and the evidence. "Matches" = no divergence found by the cases,
fixtures, differential probes or reading listed in §4.

| modeled function | verdict | evidence |
|---|---|---|
| `query` arg checks (`xdg-mime.in:569-608`) | matches for `""`, `-x/y`, `--version`; **diverges** for `--help`/`--manual` (F3) and `PATH` unset (F4) | frozen `s06`,`s08`, `rv-empty-type` = oracle; `rv-type-help`, `rv-type-manual`, `rv-path-unset` ≠ oracle |
| `detectDE` dispatch (`xdg-utils-common.in:278-355`; `xdg-mime.in:703-733`) | matches for generic/xfce/gnome/kde-without-trader/lxqt-without-`qtxdg-mat`/flatpak override; out of declared scope for KDE with a trader and LXQt with `qtxdg-mat`; `uname`/Cygwin/Darwin and the `gnome3` rename are not modelled but cannot change the defapp route on Linux | frozen `s01` (rc 3), `s02`, `s03`, `s04` (flatpak beats LXQt), `s09` all ok; no case carries `DISPLAY`/`DBUS_SESSION_BUS_ADDRESS`, so the declared dbus-send/xprop assumption holds under `env -i` |
| `defapp_generic` (`xdg-mime.in:459-505`) | matches | frozen `m` 36/36; `$XDG_CONFIG_HOME`/`$XDG_CONFIG_DIRS`/data-dir order and default values read line by line; `expand(ifs_split(...))` equals bash `IFS=:` splitting — probed `"a:"`→1, `":"`→1 empty, `"::"`→2 empty, `"a::b"`→3 (candidate `ifs_split` identical) |
| `check_mimeapps_list` (`xdg-mime.in:406-457`) | matches | frozen `m` cases; `rv-app-id-glob` (`text/plain=*.desktop` globs in cwd) = oracle `q.desktop`; header/`[`-reset/`startswith(TYPE=)`/`awk -F= $2` semantics read line by line |
| `desktop_file_to_binary` (`xdg-utils-common.in:55-97`) | matches | frozen `d` 39/39; vendor-dash split = `${desktop%-*}`/`${desktop#*-}` (`rfind`/`find`), `-r` checks, `applications/` + `applications/*/` + `applnk/` + `applnk/*/` order, `file_path` reuse *within* a call. The `file_path` global does **not** leak between apps: the caller is `exists=$(desktop_file_to_binary "$app")`, a subshell — `rv-stale-file-path-second-app`/`-empty-app` both give the oracle's `app2.desktop`, so the candidate's per-call `file_path = b""` is correct, not a bug |
| `first_word` (`xdg-utils-common.in:16-20`) | matches | differential vs `bash -c 'read first rest; echo "$first"'` on 13 inputs (leading ws, `x\ y`, `ab\<newline>cd`, `-n`, `-e`, tabs, empty/blank lines): 0 differences |
| `xdg_realpath` (`xdg-utils-common.in:427-463`) | matches on its only observable (existence; `check_mimeapps_list` only tests `-n`) | `exists_path` ≡ `[ -e ]`; empty command → False; declared refusal when `XDG_UTILS_REALPATH_BACKEND` is set |
| `defapp_fallback` (`xdg-mime.in:372-404`) | matches | frozen `f` 21/21 minus the gate (F1); `rv-initialpref-multiline` (two `InitialPreference=` lines → `"05\n3"` invalid → skipped) = oracle `y.desktop`; `rv-fallback-space-name` = oracle `my` (the unquoted `$(...)` splits the name); absent `InitialPreference` → `pref="0"` beats `-1` (read, and covered) |
| `search_desktop_file` (`xdg-mime.in:359-370`) | matches | grep `-l` on `"$dir/"*.desktop`, then recursion into `"$dir/"*/` (hidden excluded, sorted, unmatched literal); `grep_lines` on a directory/symlink = no output |
| shell helpers (`ifs_split`, `ws_split`, `pathexp`/`glob_rx`, `basename`, `echo_out`, `read_first`, `awk_v`, `bash_int`, `bre`, `command_v`) | matches except `pathexp`/`glob_rx` backslash (F2) and `awk_v` unknown escapes (now declared out of scope) | `pathexp` vs bash under `LC_ALL=C` on 18 patterns (`*`,`?`,`[a-c]`,`[!a]`,`[]]`,`[[:alpha:]]`,`*/`,`sub/`): 0 differences; `basename` vs coreutils 9.12 incl. `-x`/`--`/`a//b`/`/`: 0; `echo_out` 12 inputs: 0; `bash_int` vs `test -lt` 20 values (spaces, `+`, `04`, int64 bounds, embedded newline): 0; `command_v` vs bash for `detectDE`/`true`/`time`/`echo`/`[`/`cd`/`if`/`printf`/`./x`/`/tmp`/`/dev/null`/`..`: 0; the `FUNCTIONS` set equals the 37 functions defined in the installed `/usr/bin/xdg-mime` exactly (both set differences empty) |
| `awk_v` escapes | **out of declared scope** after the gate (F1), but the model was wrong before it: gawk turns an unknown escape into the bare character (`a\qb`→`aqb`, `a\ b`→`a b`) while `awk_v:376-411` keeps the backslash (2/15 probes) | `rv-awk-unknown-escape` oracle `a.desktop` vs candidate rc 2. If the gate is dropped, this must be fixed or re-scoped |

## 3. Commands run (all in `$S`, nothing written under the lane's `receipts/`)

All runs are DRAFT.

```
sha256sum <sources> /usr/bin/{xdg-mime,bash,grep,gawk,realpath,basename}                     exit 0
diff inst.<fn> src.<fn> for the 8 functions                                                  exit 0 (all SAME)
python3 -I build/mado-xdgmime.c1.py --selftest                                               exit 2 (no such flag; C1 has none)
drive.py xdgmime-cases-r92-l1.json    (4121d583 bytes)                                       131 answers, 0 mismatches
drive.py xdgmime-cases-r92-l1.json    (b6497a0a snapshot)                                    131 answers, 4 mismatches (F1)
drive.py rv-labelled.json  / rv2-labelled.json (b6497a0a snapshot)                            13 answers, 6 mismatches (F1-F4)
c1 counter --draft-tool 4121d583                                                             exit 3
c1 counter --draft-tool $S/cand-snapshot.py (b6497a0a)                                       exit 3
```

Counter summary line (4121d583): `DRAFT_TARGET_MET … cases=128 correct=128 b=16/16 d=39/39 f=21/21 g=6/6
m=36/36 s=10/10 answered=128/128 fresh=120/120 fresh_seed=1092736387 mutants=39 killed=39
crashed_not_killed=0 oracle_agree=128/128 do_nothing_correct=33 naive_mimeapps_correct=44
glib_resolver_correct=59 base_tool_correct=0 base_tool=absent`.

Counter summary line (b6497a0a): `DRAFT_TARGET_MISSED … cases=128 correct=124 b=16/16 d=39/39 f=19/21
g=4/6 m=36/36 s=10/10 answered=124/128 fresh=120/120 fresh_seed=3058268682 mutants=39 killed=38
crashed_not_killed=1 oracle_agree=128/128 do_nothing_correct=33 naive_mimeapps_correct=44
glib_resolver_correct=59 base_tool_correct=0 base_tool=absent tool_sha256=b6497a0a…`.

The fresh leg passes on both hashes because the frozen fuzz generator's `TYPES` are all inside the gate's
alphabet — the gate is invisible to it, which is why only the hand set catches F1.

## 4. Residual risk and verification gaps

- F1 is the only finding that changes a verdict today. If the L1 regenerates `xdg-mime-cases-r92-l1.json`
  away from those four answers, the frozen set loses its only grep-BRE (`p*`, `[`) and gawk-escape (`\t`)
  coverage; the mutant file also needs a rewrite (M36 becomes undetectable), and the declaration's
  "every type" wording must change. Silently dropping the cases while keeping the docstring's "GNU grep BRE,
  gawk `-v` escapes" claim would leave an unmeasurable claim in place.
- F2 is a model gap in a class the frozen set and the frozen fuzz generator never reach (backslash before a
  metacharacter inside an *unquoted expansion*). A future fuzz generator that puts `\` in `XDG_*`/app ids
  would turn it into a fresh-leg failure.
- Not modelled and not verified: `uname`/Cygwin/Darwin, `gnome-default-applications-properties` (GNOME 2),
  `KDE_SESSION_VERSION` values that bash `test` parses but `defapp_kde` ignores (`-4`, `+5` — read, not
  fixture-tested), a file that is a FIFO (schema cannot express it; both sides would block), and the
  sandbox's masking of `/usr/bin/bash` (no frozen or fresh case names a masked binary in `Exec`, checked).
- The docstring's "Read-only … runs no program" is true: no `subprocess`/`os.system`/`popen` in the file
  (grep, rc 1).
- Reviewed bytes are still being edited by the author seat; the L1 should freeze a hash, not "the candidate".

## 5. Scratch

`$S = /fast/scratch/hyaku/mado-r92/R92MReviewC1` is deleted on exit. Cited artifacts copied to
`w1/R92MReviewC1-fixtures.json` (13 cases with oracle `expect` + the candidate's answer per case) and
`w1/R92MReviewC1-drive.py` (the runner used above).
