# R56RevC2Spec — hostile-reader review of registration §C2 (`tools/mado-watchplan.py`)

Seat: R56RevC2Spec (scribe-reviewer role, leaf, no subagents). Wave w1, round 56. Read-only: no lane edit, no git/jj mutation, no tool written, no harness run. Deliverables: this file and `w1/R56RevC2Spec/{probe.py,probe-output.txt}`. Scratch `/fast/scratch/hyaku/mado-r56/R56RevC2Spec/` is removed before yield.

## 0. What I read and checked

- Contract: `registration.md` §C2 read in full (plus §C1/§C3 for seat boundaries). `claims-frozen.md` C2 and Harm watch read. `frozen-tables.json` sha256 = `d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af` (matches the brief). I read only the `c2` commitment strings from that file. **I did not open, list, or search for any hold-out path or file.**
- Fixtures F01–F18 read in full (args, expected.out, expected.rc, note.txt, tree). Modes and symlink targets via `git -C <lane> ls-tree` / `cat-file` at `3423ae285676c2a10273000f4519163472b443db` (read-only): symlinks at `F05/tree/linked.conf -> real/theme.conf`, `F06/tree/hyprland.conf -> real/main.conf`, `F10/tree/mix/b.conf -> missing-target.conf`; every other fixture blob is 100644.
- Hyprland pins read where they decide a reading: `fetch/Hyprland-legacy-ConfigManager.cpp:1802-1853` (handleSource), `fetch/Hyprland-MiscFunctions.cpp:61-83` (absolutePath), `:829-844` (truthy), `fetch/Hyprland-ConfigWatcher.cpp:32-76`, `fetch/Hyprland-ConfigValues.cpp:492` (option type).
- Host, read-only: `hyprctl getoption misc:disable_autoreload -j` printed the single line `{"option": "misc:disable_autoreload", "int": 0, "set": false }` (matches `fetch/host-getoption.json`). `hyprctl version -j` printed `version 0.56.2`, commit `efb50993…` (matches pin). `stat ~/.config/hypr/hyprland.conf` → regular file, 1329 bytes. No hyprctl keyword/dispatch/reload.
- Python probes under `python3 -I` (Python 3.14.8), in a private scratch tree: outputs verbatim in `w1/R56RevC2Spec/probe-output.txt`.
- Not run: the tool (does not exist yet), `quality/check-r56-controls.py`, any counter.

## 1. Verdict in brief

1. **Predicate-level agreement:** `claims-frozen.md` C2 and `registration.md` §C2 agree on fixture count (18 + 8 = 26), hold-out count, the three controls (`const-host`, `empty`, `lookup-committed`), the five declared divergences, the two-token argument form and the SETUP reasons. No disagreement found at predicate level. One disagreement between the registration's *declared divergences* and the cited Hyprland code (DEF-2) and one fixture-note defect (DEF-1) are reported below.
2. **Ambiguity count:** 40 numbered items (AMB-01..AMB-42; numbers 05 and 12 are unused; AMB-41a is a predicate trap), grouped by the spec's own sections. Almost all have two or more defensible readings that produce different bytes. Only the items marked "= code" in §3 are settled by a Hyprland pin; the rest are settled only by a choice this report recommends. No committed fixture pins any reading that §4 does not list.
3. **Highest-impact unpinned items:** AMB-01 (`} # end`), AMB-02 (unclassified brace lines silently ignored), AMB-03 (category stack after a sourced file returns), AMB-04 (trailing comment containing `$`), AMB-27 (display root matched both as string and realpath), AMB-34 (SETUP precedence), AMB-36/37 (getoption JSON `trailing text` and `NaN`).
4. **Structural gap:** the category / comment / brace grammar (`§C2 Model` bullets 1–3 and the `misc:disable_autoreload` value rules) cites `configStringToInt`, which has **no hit anywhere in `fetch/`** (the other terms, `handleSource`, `GLOB_TILDE`, `parseFile`, hit only the legacy ConfigManager, MiscFunctions, ConfigWatcher and the option table). The hyprlang 0.6.8 parser that decides these readings is not pinned. Everything in §3.1 and AMB-07 is therefore decided by the frozen text alone, not by a source pin.

## 2. Defects found

**DEF-1 — F12 note contradicts its expected output.** `fixtures/c2/F12/note.txt` = `UNKNOWN: no record; non-object lines are bad_json`. `F12/expected.out` = `MADO_WATCH: SETUP bad_json` and `expected.rc` = `2`. The second line of `F12/tree/go.json` is `[1,2]`, which aborts the whole run; no `UNKNOWN` is printed. The note describes a different behaviour (the UNKNOWN case, which is `live=?` with exit 0). Fix the note; the expected bytes are consistent with the frozen rule ("a non-empty `--getoption` line … that is not a JSON object" → SETUP `bad_json`).

**DEF-2 — declared divergence "GLOB_TILDE `~user` forms" is not a divergence.** Hyprland's `absolutePath` (`Hyprland-MiscFunctions.cpp:64-66`) replaces only the first character `~` with `$HOME` *before* `glob(…, GLOB_TILDE)` is called (`Hyprland-legacy-ConfigManager.cpp:1816`). So `~user/x` becomes `$HOME` + `user/x` in Hyprland, exactly as the frozen model's `--home` + `RAW[1:]` rule does. The declared divergence should be removed (or reworded to "`--home` replaces `$HOME`"). Conversely, the frozen model's **Python `len`** (AMB-14) is a real divergence that is not declared.

**DEF-3 — dead clauses.** `§C2 (3)` "(all of `cur` if it holds no `/`)" and `§C2 (5)` "relative match M … absolutePath(M, cur)" are unreachable: `--config` is absolute and every VALUE is therefore absolute (`--home` absolute, `curdir` from an absolute `cur`, and `glob` of an absolute pattern returns absolute paths). The `find_last_of` substr in Hyprland (`MiscFunctions.cpp:68`) happens to behave the same, so nothing observable changes. Either delete the clauses or state that they are unreachable, so an implementer does not invent behaviour for a case that cannot occur.

**DEF-4 — `misc:disable_autoreload` is a Bool option in Hyprland, not an integer.** `Hyprland-ConfigValues.cpp:492` registers `MS<Bool>("misc:disable_autoreload", …)`, while `Hyprland-ConfigWatcher.cpp:33` reads it as `CConfigValue<Config::INTEGER>`. The frozen model's `N` (decimal integer, printed in the header) and its live-compare rule (AMB-06, AMB-08) are therefore reached only through a type the option table does not declare. Reachability of `N > 1` in the real host is unknown; this should be stated.

**DEF-5 — `.*` globbing differs from glibc, and this is not declared.** Hyprland calls glibc `glob(3)` (`Hyprland-legacy-ConfigManager.cpp:1816`). glibc returns `.` and `..` for a `.*` pattern (verified with `ctypes` on `libc.so.6`: `['.', '..', '.hidden.conf']`); Python's `glob` returns only `.hidden.conf` (verified). The declared divergence "glob bytewise order versus the C library's locale collation" does not cover this. See AMB-42.

## 3. Ambiguities

Notation: `FX` = the harness token replaced by the fixture dir (args only). Unless stated, args = `--config {FX}/tree/hyprland.conf --display-root {FX}`. Header shorthand: `H(autoreload=…, disable=…, paths=…, unsupported=…, errors=…)`. "Pinned by code" = the cited Hyprland pin resolves it; "unpinned" = nothing in the frozen tree decides it.

### 3.1 Category / brace / comment grammar (sourced by no pin; decided by frozen text)

**AMB-01 — `}` with trailing text.** Input line `} # end`.
- R1 (literal "a line without `=`: exactly `}` pops"): the line is *ignored*, stack not popped, no event, no unsupported.
- R2 (comment-cut first, then pop).
- R3 (model principle "everything outside it is counted unsupported, never guessed"): unsupported +1, stack not popped.
- Pinned by: nothing. Recommend R3 (matches the model's own principle).
- 3-line fixture `tree/hyprland.conf`:
  ```
  misc {
  } # end
  misc:disable_autoreload = 1
  ```
  R1: `H(autoreload=on, disable=unset, paths=1, unsupported=0, errors=0)` (KEY is `misc:misc:disable_autoreload`, ignored). R2: `H(autoreload=off, disable=1, …, unsupported=0)`. R3: `H(autoreload=on, disable=unset, …, unsupported=1)`.

**AMB-02 — unclassified brace lines are silently ignored.** Model: "any other line is ignored", and "unsupported" only for `source` and for the `misc:disable_autoreload` key. So a brace opener or assignment the model cannot classify is dropped with no count. Cases: `misc { disable_autoreload = 1 }` (LHS becomes `misc { disable_autoreload`), `misc { # open` (does not end in `{`), `misc` then `{` on its own line (pushes `""`), `misc = {` (has `=`).
- R1 (literal): silent.
- R3: unsupported +1 per unclassifiable brace line.
- Pinned by: nothing.
- 3-line fixture:
  ```
  misc { disable_autoreload = 1 }
  misc { # open
    disable_autoreload = 1
  ```
  R1: `H(autoreload=on, disable=unset, paths=1, unsupported=0, errors=0)`. R2 (one-liner and comment-aware): `H(autoreload=off, disable=1, …, unsupported=0)`. R3: `H(autoreload=on, …, unsupported=2)`.

**AMB-03 — category stack after a sourced file returns.** "The category stack resets at each file's start" does not say whether the parent's stack is restored. A child that leaves `misc {` open can leak into the parent under a shared-state implementation.
- R1 (per-file stack, the natural reading): after return the parent's stack is empty.
- R2 (shared stack): the child's residue stays.
- Pinned by: `Hyprland-legacy-ConfigManager.cpp:1837-1840` restores `m_configCurrentPath` per file, not the hyprlang category stack (not in `fetch/`). Unpinned.
- 3-line fixture (`tree/hyprland.conf` + `tree/a.conf`):
  ```
  source = a.conf
  misc:disable_autoreload = 1
  ```
  `tree/a.conf` = `misc {`.
  R1: `H(autoreload=off, disable=1, paths=2, unsupported=0, errors=0)`. R2: `H(autoreload=on, disable=unset, paths=2, unsupported=0, errors=0)`.

**AMB-04 — trailing comment on the option line and the line-wide `$`/`{`/`\` check.** The `$`/`{`/backslash rule is on "the line", and the `##` rule on "the RHS", but the RHS cut at `#` happens later. So a comment containing `$` poisons the value.
- R1 (literal, line-wide): unsupported +1, value ignored.
- R2 (cut comment first, then classify): accepted.
- Pinned by: F09 pins `1 ## x` (RHS `##`), not a `$` in a comment. Unpinned.
- 2-line fixture:
  ```
  misc:disable_autoreload = 1 # see $HOME
  # $HOME is only a comment
  ```
  R1: `H(autoreload=on, disable=unset, paths=1, unsupported=1, errors=0)`. R2: `H(autoreload=off, disable=1, paths=1, unsupported=0, errors=0)`.

**AMB-33 — `}` on an empty stack.** Spec silent. R1: no-op. R3: unsupported +1. Fixture: `}` / `misc:disable_autoreload = 1` → R1 `autoreload=off disable=1 unsupported=0`; R3 `unsupported=1`. Output-neutral otherwise; state it.

**AMB-41 — `misc:disable_autoreload` written with an internal space** (`misc: disable_autoreload = 1`) → LHS does not match, silently ignored. Literal reading is silent; state that KEY is the exact stripped LHS.

### 3.2 `misc:disable_autoreload` value and live join

**AMB-06 — live compare: equality versus non-zero.** Frozen: "`AGREE` when the live int equals `config`", with `config` ∈ {0,1}. A live int of 2 (possible only with a fake record; the real option is Bool, see DEF-4) gives `DIFFER` under the literal reading and `AGREE` under "non-zero".
- Fixture: `tree/hyprland.conf` = `misc:disable_autoreload = 2`; `tree/go.json` = `{"option": "misc:disable_autoreload", "int": 2}`.
  R1 (literal): `MADO_WATCH_LIVE: … config=1 live=2 verdict=DIFFER`, `DONE … live=DIFFER`. R2 (non-zero): `AGREE`.
- Pinned by: `Hyprland-ConfigWatcher.cpp:34` uses "non-zero → off" for the watch decision, so R2 matches the watch decision the header reports. Recommend R2 and say so.

**AMB-07 — `configStringToInt` prefix and case.** The frozen text says "starts with `true`, `on` or `yes`" (prefix) and "starts with `false`, `off` or `no`" but says nothing about case.
- R1 (prefix, case-sensitive): `none` → 0 and `onion` → 1 (prefix of `on`); `Yes` → unsupported.
- R2 (case-insensitive prefix): `Yes` → 1. Hyprland's sibling helper `truthy()` (`Hyprland-MiscFunctions.cpp:829-844`) lowercases and prefix-matches `true|yes|on`. Note `truthy()` is not `configStringToInt`; it is evidence of the style, not proof.
- R3 (whole-token): `none`, `onion`, `Yes` → unsupported.
- 3-line fixture:
  ```
  misc:disable_autoreload = none
  misc:disable_autoreload = onion
  misc:disable_autoreload = Yes
  ```
  R1: `H(autoreload=off, disable=1, paths=1, unsupported=1, errors=0)`. R2: `H(autoreload=off, disable=1, …, unsupported=0)`. R3: `H(autoreload=on, disable=unset, …, unsupported=3)`.

**AMB-08 — printing `N`.** `disable_autoreload = 007`: "that decimal integer" → R1 prints `disable_autoreload=7`; R2 prints the text `007`. Big values: `99999999999999999999` → R1 prints the exact integer; a 64-bit implementation overflows. Fixture: one line `misc:disable_autoreload = 007` → R1 `H(autoreload=off, disable=7, …)`; R2 `H(…, disable=007, …)`.

**AMB-09 — getoption `int` that is a JSON float.** `{"option": "misc:disable_autoreload", "int": 1.0}` (also `1e2`): Python parses to `float` (verified). R1 (not an integer → ignored): `live=?`, `UNKNOWN`, exit 0. R2 (integral JSON number accepted): `live=1`. Pinned by: F13 pins `true`, not floats. Fixture: `tree/go.json` = that one line, config unset → R1 `MADO_WATCH_LIVE: … config=0 live=? verdict=UNKNOWN`; R2 `live=1 verdict=DIFFER`.

### 3.3 Source RAW and VALUE

**AMB-10 — RAW of length 2: `~/`, `./`, `..`.** Pinned by code for the `./` and `..` forms: `absolutePath` (`MiscFunctions.cpp:70-79`) gives `curdir + "/"` for `./`, and for `..` (no `/` after it) falls to `curdir + "/" + RAW` = `…/tree/..` (unnormalised). `~/` with `--home`: `$HOME`-style concatenation gives `home + "/"`, a directory → SKIP. Without `--home`: unsupported (rule 2).
- R1 (literal, = code): SKIP lines keep the trailing `/` and the `..`.
- R2 (normalised): `…/home`, `…/tree`, `…`.
- Fixture `tree/hyprland.conf` + `tree/home/h.conf` (git cannot store an empty dir), args `+ --home {FX}/tree/home`:
  ```
  source = ~/
  source = ./
  source = ..
  ```
  R1: `SKIP via=$ROOT/tree/hyprland.conf:1 path=$ROOT/tree/home/ reason=directory`, `…:2 path=$ROOT/tree/ reason=directory`, `…:3 path=$ROOT/tree/.. reason=directory`, then `H(autoreload=on, disable=unset, paths=1, unsupported=0, errors=0)`. R2: the same three SKIP paths without trailing `/` and with `..` removed. Pin R1 (matches code).

**AMB-11 — `..` in the middle of a path.** `source = sub/../rel.conf` (no leading `..`): `curdir + "/" + RAW` → `…/tree/sub/../rel.conf`, unnormalised (code-consistent). R2 normalises to `…/tree/rel.conf`. Fixture: `tree/hyprland.conf` = that line; `tree/sub/s.conf` (any content) and `tree/rel.conf` exist. R1: `n=2 … path=$ROOT/tree/sub/../rel.conf type=file … via=$ROOT/tree/hyprland.conf:1`. R2: `path=$ROOT/tree/rel.conf`. Pin R1 (code).

**AMB-13 — `~` prefix without `/`, and `--home` with trailing `/`.** Code (`absolutePath` line 64-66) replaces the first character only, so `~h.conf` → `$HOME` + `h.conf` = `…/homeh.conf`. A reader who thinks only `~/` is supported gets unsupported.
- Fixture: `tree/hyprland.conf` = `source = ~h.conf`; `tree/homeh.conf` exists; args `+ --home {FX}/tree/home`.
  R1 (= code): `n=2 role=primary path=$ROOT/tree/homeh.conf … via=$ROOT/tree/hyprland.conf:1`. R2 (`~/` only): `unsupported=1`.
- `--home` with a trailing slash gives `home//h.conf` under R1 (concatenation, no normalisation); not in fixtures. Pin R1 and say so.

**AMB-14 — `len(RAW) < 2` counts code points in the frozen text, bytes in Hyprland.** `Hyprland-legacy-ConfigManager.cpp:1803` uses `rawpath.length()` on a `std::string` (UTF-8 bytes). The frozen model is Python `len()` (code points).
- R1 (Python len): a one-code-point, two-byte name such as `é` → `ERROR reason=bogus`.
- R2 (byte length, = code): `é` is accepted.
- Fixture: `tree/hyprland.conf` = `source = é`; `tree/é` (empty file).
  R1: `ERROR via=$ROOT/tree/hyprland.conf:1 source=é reason=bogus`, `errors=1`. R2: `n=2 … path=$ROOT/tree/é`.
- Pin R2 (code). This is a real divergence and should be declared.

**AMB-15 — whitespace set: explicit set versus `str.strip()`.** The frozen text says "stripped of space, tab, CR, LF, VT, FF". Python `str.strip()` also strips U+00A0, U+001C–U+001F, U+0085 and others (verified: `"a.conf\xa0".strip()` → `'a.conf'`; with the explicit set → `'a.conf\xa0'`).
- Fixture: `tree/hyprland.conf` = `source = a.conf` followed by U+00A0 (bytes `C2 A0`); `tree/a.conf` exists.
  R1 (explicit, the text): `ERROR … source=a.conf\xa0 reason=nomatch`, `errors=1`. R2 (`str.strip()`): `n=2 … path=$ROOT/tree/a.conf`.
- Pin R1 (the text is explicit); add a sentence that Python `strip()` must not be used.

**AMB-16 — line splitting: `split("\n")` versus `splitlines()`.** The frozen text says "split on `\n`". `splitlines()` also splits on `\r`, `\x0b`, `\x0c`, `\x1c–\x1e`, `\x85`, `\u2028`, `\u2029` (verified: `"a\x0cb\rc\nd".split("\n")` → 2 items; `splitlines()` → 4).
- Fixture: `tree/hyprland.conf` bytes = `misc:disable_autoreload = 1\rsource = a.conf\n`; `tree/a.conf` exists.
  R1 (split on `\n`): one line; RHS `1\rsource = a.conf` is not an integer → `unsupported=1`, `autoreload=on`. R2 (splitlines): `autoreload=off disable=1`, `n=2 a.conf`.
- Pin R1 (the text). Also changes the `via=…:N` numbering in R2.
- Plain CRLF needs no rule: CR is in the explicit strip set, so `}\r`, `misc {\r` and `source = a.conf\r` parse as their LF forms. Only a lone `\r` inside a line (above) is ambiguous.

**AMB-17 — UTF-8 BOM.** `EF BB BF source = a.conf` on line 1: the BOM is not in the stripped set, so LHS = `\ufeffsource` (verified: `str.strip()` does not remove U+FEFF) and the line is silently ignored.
- Fixture: `tree/hyprland.conf` = BOM + `source = a.conf`; `tree/a.conf` exists. R1 (BOM kept): `paths=1 errors=0 unsupported=0`. R2 (BOM stripped): `paths=2`, `n=2 … a.conf`.
- Unpinned. Recommend stating the BOM rule explicitly.

**AMB-18 — quoted path `source = "a.conf"`.** RAW = `"a.conf"` including quotes. R1 (literal): `glob` finds nothing → `ERROR reason=nomatch source="a.conf"`. R2: unsupported (quoting is outside the model). Code-consistent with R1 (`glob` of the raw string), but hyprlang may strip quotes before the handler is called (not pinned). Fixture: `tree/hyprland.conf` = `source = "a.conf"`; `tree/a.conf` exists. R1: `errors=1`. R2: `unsupported=1`.

**AMB-19 — `$VAR` in a `source` path.** The `$`-rule applies to the `misc` key only. `source = $HOME/a.conf` → R1: `ERROR reason=nomatch`. R2 ("outside the model → unsupported"): `unsupported=1`. Unpinned. Fixture: that one line. R1: `errors=1`. R2: `unsupported=1`.

**AMB-20 — empty and bare `source`.** `source =` and `source = # c` → RAW `""` → `bogus` (code: `rawpath.length() < 2` → "bogus!", `legacy 1803-1805`, R1 pinned). Bare `source` (no `=`) is "any other line → ignored" (literal, silent); hyprlang would report an error. Fixture: `source =` / `source = # only` / `source`. R1: `errors=2` (two `ERROR … source= reason=bogus`), line 3 silently ignored, `unsupported=0`. R2 (bare `source` counted unsupported): `unsupported=1`.

**AMB-21 — glob metacharacters in the directory of the current file.** `glob` interprets `[`, `*`, `?` in the prefix `curdir` and in `--home`. Verified in Python: `glob('…/[x]/a.conf')` → `[]`, `glob(glob.escape(…))` → match. Code: Hyprland passes the un-escaped `absolutePath` to `glob(…, GLOB_TILDE)` (`legacy 1816`), so the C library also interprets brackets. Pinned by code for R1 (un-escaped).
- Fixture: args `--config {FX}/tree/[x]/hyprland.conf --display-root {FX}`; `tree/[x]/hyprland.conf` = `source = a.conf`; `tree/[x]/a.conf` exists.
  R1 (= code): `ERROR via=$ROOT/tree/[x]/hyprland.conf:1 source=a.conf reason=nomatch`, `errors=1`. R2 (escaped): `n=2 … path=$ROOT/tree/[x]/a.conf`.

**AMB-22 — undecodable file names.** A name with byte `\xff` reaches Python as a surrogate-escaped `str` (verified: `'a\\udcff.conf'`). Printing it under a UTF-8 locale raises `UnicodeEncodeError` (verified); under `LANG=C` it prints `a�.conf` (verified). Readings: R1 crash (exit 1, outside the contract's exit set 0/2); R2 print U+FFFD (the printed path no longer names the file); R3 treat as unsupported. Fixture: file bytes `a\xff.conf`; `tree/hyprland.conf` = `source = a?.conf`. Pin one explicitly; the contract currently defines no exit for it.

**AMB-42 — leading-dot glob patterns (`source = .*`).** The frozen text pins Python `glob` semantics ("leading-dot names need a leading-dot pattern"), so `.*` returns dotfiles only (R1). Hyprland calls glibc `glob(3)`, which also returns `.` and `..` (R2, verified in DEF-5). Fixture: `tree/hyprland.conf` = `source = .*`; `tree/.hidden.conf` exists. R1: `paths=2 unsupported=0 errors=0`, `n=2 role=primary path=$ROOT/tree/.hidden.conf type=file mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=$ROOT/tree/hyprland.conf:1`, no SKIP. R2: `SKIP via=$ROOT/tree/hyprland.conf:1 path=$ROOT/tree/. reason=directory`, `SKIP via=$ROOT/tree/hyprland.conf:1 path=$ROOT/tree/.. reason=directory`, then the same `.hidden.conf` watch. Pin R2 (the code) and change the frozen glob text, or declare the divergence. Not settled by any committed fixture (F03 pins `*` only).

**AMB-40 — `--getoption` symlink.** "regular" with `stat` (follows links; consistent with F06's config-symlink behaviour) versus `lstat` (symlink is not regular → unreadable). Fixture: args `--getoption {FX}/tree/go.json` where `go.json` is a symlink to a regular file. R1 (stat): normal output. R2 (lstat): `SETUP unreadable`, rc 2. Pin R1 and say `stat`.

### 3.4 Watch list and canonical watches

**AMB-23 — dangling `--config` symlink.** `os.path.lexists` is true, so the frozen type is `file`; the canonical watch needs `realpath(strict=True)`, which fails → no canonical. R2 ("the path resolves to nothing → missing"): `type=missing`. Code agrees with R1: `ConfigWatcher.cpp:54-57` uses `is_directory` (false) and the file mask on the link itself. Fixture: `tree/hyprland.conf` → symlink to `gone.conf` (absent). R1: `paths=1 … autoreload=on`, `n=1 role=primary path=$ROOT/tree/hyprland.conf type=file mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=main`, `DONE watches=1`. R2: `type=missing`. Pin R1 (code).

**AMB-24 — `--config` symlink to a directory.** The primary is `type=dir` (`isdir` follows links). The canonical is labelled `type=file` by the frozen text. R2 would label it `type=dir`. Code (`ConfigWatcher.cpp:65-71`): the canonical watch is always `IN_CLOSE_WRITE` with no directory check, so the frozen label `type=file` describes the mask actually used. Pin R1. Fixture: `--config {FX}/tree/dlink` where `tree/dlink` → `d` and `tree/d/x.conf` exists. R1: `n=1 role=primary path=$ROOT/tree/dlink type=dir mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM via=main`, `n=2 role=canonical path=$ROOT/tree/d type=file mask=IN_CLOSE_WRITE via=main`, `paths=1`.

**AMB-25 — symlinked intermediate directory.** `os.path.islink(V)` checks only the final component. `source = lnk/a.conf` with `tree/lnk → real`: R1 (= code, `ConfigWatcher.cpp:66` `is_symlink(path)`): no canonical watch. R2 (`realpath` compare): canonical `real/a.conf` added. Fixture: `tree/hyprland.conf` = `source = lnk/a.conf`; `tree/lnk` → `real`; `tree/real/a.conf` exists. R1: `paths=2 … watches=2` (no `role=canonical`). Pin R1 (code).

**AMB-26 — canonical watch placement, and the cur path for a sourced symlink.** Code: the canonical watch is added right after its primary (`ConfigWatcher.cpp:59-71`) and the list entry is appended before parsing (`legacy 1836`). `m_configCurrentPath` is set to the link path (`legacy 1838`), so relative sources of a sourced symlink resolve from the link's directory (matches F06's config-symlink note, which is pinned for the main config only). Fixture: `tree/hyprland.conf` = `source = linked.conf`; `tree/linked.conf` → `real/theme.conf`; `tree/real/theme.conf` = `source = plain.conf`; `tree/plain.conf` exists. R1 (= code): watch order `main`, `linked` primary, `linked` canonical (`real/theme.conf`), `plain` primary, `paths=3`. R2 (cur = realpath): `ERROR … source=plain.conf reason=nomatch` because `real/plain.conf` does not exist. Pin R1 (code).

### 3.5 Display root

**AMB-27 — display root matched both as the given string and as its realpath.** "every printed path equal to DIR or starting with DIR + `/`, where DIR is either the given string … or its `os.path.realpath`" does not say which form wins when both match with different remainders. Concrete: `tree/alias` → `.` (symlink to the tree dir), `--display-root {FX}/tree/alias`, `tree/extra.conf` exists, `tree/hyprland.conf` = `source = alias/extra.conf`.
- R1 (given string first): `n=2 … path=$ROOT/extra.conf`.
- R2 (realpath first): `n=2 … path=$ROOT/alias/extra.conf`.
- Both: `config=$ROOT/hyprland.conf` (only the realpath form matches the config line). A string-only implementation prints the absolute export path → fails the fixture.
- Note: `readlink -f /fast` = `/fast` on this host, so **no committed fixture exercises the realpath branch of DIR**; the F05/F06 `$ROOT/tree/real/…` results do not depend on it. Pin R1 (the frozen text names "the given string" first) and add this fixture.

**AMB-28 — sibling prefix (`/a/b` vs `/a/bc`).** The frozen rule ("DIR + `/`") is unambiguous and a naive `startswith(DIR)` is wrong. But every fixture prints `config=` with an absolute path, and the export root path is scratch-dependent (HYG-1), so a sibling test **cannot be pinned** with the current `{FX}`-in-args-only rule. Constant-path variant: `--display-root /dev/n` with `source = /dev/null`, which still prints `config=` absolute and is therefore not reproducible. Recommend HYG-1's fix.

**AMB-29 — `--display-root /`.** `DIR` becomes `""` after the trailing `/` is removed; `os.path.realpath("")` returns the current working directory (verified: `realpath("")` = cwd). Readings: (a) `"$ROOT" + p[len(DIR):]` → `$ROOT/tree/…`; (b) naive `p[1:]` → `$ROOTtree/…`; (c) the cwd branch maps export-root paths to `$ROOT` too. Every path is under `/`, so every header and SKIP path contains export-root components → not reproducible. Recommend rejecting `--display-root /` (usage) or defining it.

**AMB-30 — prefix replacement once.** "that prefix replaced" = replace the leading occurrence once. No ambiguity in the text; no fixture needed. Stated for completeness because a `str.replace` implementation would rewrite inner occurrences.

### 3.6 Depth cap, counters, output size

**AMB-31 — depth cap: per matching path or per line.** "`unsupported` +1 and V is recorded but not parsed" is per over-cap match, not per line. Fixture: `tree/hyprland.conf` = `source = c.conf`; `tree/c.conf` = `source = c*.conf`; `tree/cc.conf` empty. Each level `d` (1..16) parses `c.conf` and `cc.conf`; the depth-16 `c*.conf` line yields two over-cap matches (`c.conf` and `cc.conf` at depth 17).
- R1 (per match, literal): `paths=34 unsupported=2 errors=0` (1 main + 16 `c` + 15 `cc` + 2 over-cap = 34; 34 watch lines).
- R2 (per line): `unsupported=1`.
- Pinned by: nothing (Hyprland has no cap; declared divergence). Recommend R1 and say "per over-cap match". The 34-line expected file is long but deterministic.

**AMB-32 — no output or work bound on fan-out.** `source = self.conf` plus a second self-line gives 2^16 parses and ~131k watch lines. The frozen text has no budget and the harness has no timeout rule. Not a correctness fixture; state a budget or an explicit "no bound" so a harness timeout is not mistaken for a counter result.

**AMB-34 — SETUP precedence.** The frozen text lists setup reasons but not their order. Fixture: `tree/hyprland.conf` = `source = big.conf`; `tree/big.conf` = 1048577 bytes; `--getoption {FX}/tree/go.json` where `go.json` = `[1]`.
- R1 (closure read before getoption): `MADO_WATCH: SETUP too_large`, rc 2.
- R2 (getoption first): `MADO_WATCH: SETUP bad_json`, rc 2.
- Pin one order. Note: committing a 1 MiB file bloats the lane; generate it at commit time or accept the cost.

**AMB-35 — what counts as "read" for `too_large`.** "any file the tool reads". Not read: canonical targets, depth-capped files (listed only), `source` lines inside a category (unsupported, the line ends). R1 (literal): none of those trigger `too_large`. R2 ("the closure" including listed-only files): would trigger. Also boundary: exactly 1048576 bytes → accepted; 1048577 → `too_large` (the text says "larger than"). Fixture pair: `tree/big.conf` with 1048576 bytes (R1 accepted) and with 1048577 bytes (R1 `too_large`).

### 3.7 getoption file

**AMB-36 — trailing text after a JSON object.** `{"option": "misc:disable_autoreload", "int": 1} x`. R1 (`json.loads` of the stripped line; "not a JSON object" → bad_json): `MADO_WATCH: SETUP bad_json`, rc 2 (verified: `JSONDecodeError`). R2 (`raw_decode` accepting a prefix object): `live=1`. Pinned by: nothing. Recommend R1 (the text says "is a JSON object"). Fixture: the one line; R1 `SETUP bad_json` rc 2.

**AMB-37 — `NaN`/`Infinity`.** Python's `json` accepts `NaN` (verified: `{"int": NaN}` → `nan`). `{"option": "misc:disable_autoreload", "int": NaN}`: R1 (Python json): the record parses, is not an integer, is ignored → `live=?`, `UNKNOWN`, exit 0. R2 (strict RFC 8259): bad_json. Recommend strict parsing (`parse_constant` rejecting). Fixture: the one line.

**AMB-38 — BOM and multi-line JSON.** A BOM before `{` → `json.loads` raises (verified) → bad_json. A pretty-printed multi-line object → the first line `{` is bad_json under the line-by-line rule (R1), while a whole-file parser (R2) accepts it. Host check: `hyprctl getoption misc:disable_autoreload -j` emits one line (verified), so the real tool output works; `hyprctl version -j` is multi-line (verified), so pointing `--getoption` at a different dump gives bad_json. Pin R1 and say "one JSON object per line".

**AMB-39 — duplicate keys.** `{"option":"misc:disable_autoreload","int":1,"int":0}` → Python keeps the last (verified: `{'int': 0}`) → `live=0`. R2 (reject duplicates) → bad_json. Spec silent. Fixture: that one line → R1 `live=0`.

**AMB-41a — getoption `int` with `true` and the Python bool trap.** F13 pins `true` as ignored. Python's `isinstance(True, int)` is `True` (verified), so an implementation that tests `isinstance(v, int)` alone accepts `true` as 1. Not a spec ambiguity but a predicate trap: the rule must exclude `bool` explicitly. Fixture: F13 already pins it; no new fixture.

### 3.8 Harness and fixture hygiene

**HYG-1 — non-`$ROOT` absolute paths cannot be in `expected.out`.** The harness replaces `{FX}` in args only; the export dir is scratch-dependent. Every printed path outside the display root (AMB-27/28/29, and `config=` whenever the config is outside the root) is non-reproducible. F02's `/dev/null` is the only constant outside path. Fix: let the harness also substitute `{FX}` in expected.out (same token, same export path), or require every fixture to print only `$ROOT` and `/dev/null`-style constants.

**HYG-2 — `unreadable` is not fixturable.** git stores only 100644, 100755 and 120000; `chmod` is lost on export, and a root-run harness reads anything. The `unreadable` reason (getoption; and the unreadable-sourced-file rule) can only be pinned by a harness-time `chmod`, which the frozen harness does not do. State "not pinned by any committed fixture".

**HYG-3 — empty directories cannot be committed.** Any fixture needing an empty dir needs a placeholder file; the placeholder changes glob results. The F04/F16 trees avoid this; new fixtures must not rely on empty dirs.

**HYG-4 — SETUP output terminator.** `expected.out` for SETUP ends with `\n` (verified for F12, F17, F18 by `od -c`). The frozen text says "stdout exactly `MADO_WATCH: SETUP <reason>`". Add "followed by `\n`".

**HYG-5 — DIR realpath branch is untested** (see AMB-27): `/fast` is not a symlink on this host and no fixture uses a symlinked display root. Add the alias fixture or drop the realpath clause.

## 4. Already pinned by the committed fixtures (no action)

- F01 single file; F02 `/dev/null` SKIP nonregular, `./`, bare, `sub/` and `../` from nested; F03 glob bytewise order, dotfile exclusion, directory SKIP; F04 `~/`-style with `--home`; F05 symlink primary + canonical; F06 main config is a symlink, relative sources resolve from the link dir (main only, see AMB-26); F07 `true` → off, paths still listed; F08 later line wins (`yes` then `no`); F09 `$` var, `source` in category → unsupported, `## token` → unsupported, four unsupported; F10 `nomatch`, `bogus` (`x`), dangling match aborts the rest of the glob, events before watch lines; F11/F13 `DIFFER`/`AGREE`, bool `int` ignored; F12/F18 bad_json (non-object line; `{bad`); F14 missing main → `type=missing`; F15 duplicate watches, `k=1`, `#` comment cut without spaces; F16 directory source via `conf.d` and `conf.d/`; F17 usage (no `--config`).
- Order of events versus watch lines: F10 (three ERROR lines before `n=1`) and F02 (SKIP before `n=1`) pin events first. The one open point is canonical-before-children (AMB-26).
- Nested-category KEY join: the direct `misc` child form (`misc:disable_autoreload`) is pinned by F07, F08 and F09. `misc:misc:…`, `sub:misc:…` and `misc:sub:…` are literal and silent (AMB-02, AMB-41).

## 5. Suggested fixture set (summary)

| ID | Pins | Body (tree/hyprland.conf unless noted) | Recommended reading |
|---|---|---|---|
| AMB-01 | `}` + text | `misc {` / `} # end` / `misc:disable_autoreload = 1` | R3 (unsupported) |
| AMB-02 | unclassified braces | `misc { disable_autoreload = 1 }` / `misc { # open` / `  disable_autoreload = 1` | R3 |
| AMB-03 | stack leak | `source = a.conf` / `misc:disable_autoreload = 1`; `a.conf` = `misc {` | R1 per-file |
| AMB-04 | `$` in comment | `misc:disable_autoreload = 1 # see $HOME` / `# $HOME…` | R2 (cut first) |
| AMB-06 | live `2` | config `= 2`; go.json `int 2` | R2 non-zero |
| AMB-07 | prefix/case | `none` / `onion` / `Yes` | R1 + state case |
| AMB-10 | RAW len 2 | `~/` / `./` / `..` with `--home` | R1 (= code) |
| AMB-11 | mid `..` | `source = sub/../rel.conf` | R1 (= code) |
| AMB-13 | `~h.conf` | `source = ~h.conf`; `tree/homeh.conf` | R1 (= code) |
| AMB-14 | `é` (2 bytes, 1 char) | `source = é`; `tree/é` | R2 bytes (= code) |
| AMB-15 | NBSP | `source = a.conf<U+00A0>` | R1 (explicit set) |
| AMB-16 | `\r` | `misc:disable_autoreload = 1\rsource = a.conf\n` | R1 split `\n` |
| AMB-17 | BOM | `<BOM>source = a.conf` | state explicitly |
| AMB-18 | quoted | `source = "a.conf"` | R1 nomatch |
| AMB-20 | empty source | `source =` / `source = # only` / `source` | R1 (bogus ×2) |
| AMB-21 | `[x]` dir | `--config …/tree/[x]/hyprland.conf` | R1 (= code) |
| AMB-23 | dangling config | `tree/hyprland.conf` → `gone.conf` | R1 (= code) |
| AMB-24 | config → dir | `--config …/tree/dlink` → `d/` | R1 mask (= code) |
| AMB-25 | `lnk/a.conf` | `source = lnk/a.conf`; `lnk` → `real` | R1 (= code) |
| AMB-26 | sourced symlink | see §3.4 | R1 (= code) |
| AMB-27 | alias root | `--display-root {FX}/tree/alias`; `source = alias/extra.conf` | R1 string first |
| AMB-31 | depth cap | `source = c.conf`; `c.conf` = `source = c*.conf`; `cc.conf` empty | R1 per match (paths=34, unsupported=2) |
| AMB-34 | setup order | `source = big.conf` (1048577 B) + getoption `[1]` | pick one order |
| AMB-36 | JSON trailing text | `{…} x` | R1 bad_json |
| AMB-37 | NaN | `"int": NaN` | strict → bad_json |
| AMB-39 | duplicate key | `"int":1,"int":0` | state |
| AMB-42 | `source = .*` (glibc adds `.`, `..`) | `source = .*`; `tree/.hidden.conf` | R2 (= code), spec change needed |

## 6. Limits and what I could not verify

- The tool and the harness do not exist yet; every "R1/R2 output" above is derived from the frozen text by hand, not by running a reference implementation. Expected headers are given for the decisive lines only.
- Hyprlang 0.6.8 (the category/comment/`}` grammar, `configStringToInt`, `registerHandler` flags) is not in `fetch/`; §3.1 and AMB-07 rest on frozen text plus the `truthy()` sibling only.
- Python behaviours (glob, realpath, json, strip, splitlines, surrogate printing) were verified on Python 3.14.8 only; the harness runs `python3 -I` on that host, so this matches the run environment, but I did not test older interpreters.
- Non-UTF-8 printing (AMB-22) was verified under `LANG=C.UTF-8` and `LANG=C` via `env -i`; a test under other locales was not run.
- Unreadable-file behaviour (HYG-2) was not tested (root bypass, no chmod in scope).
- Hold-out fixtures H01–H08 were not opened; nothing here depends on them.
- No tool was installed or upgraded (no `pacman`, `uv`, `npm` used). No host configuration, compositor or service state was touched.

## 7. Receipts

- `w1/R56RevC2Spec/probe.py` — the Python probe (run with `python3 -I`, scratch dir as argv[1]).
- `w1/R56RevC2Spec/probe-output.txt` — verbatim outputs of the probe, the inline checks, the undecodable-name check, and the fixture-facts (modes, symlink targets, trailing newline, frozen-table sha).
- Commands (read-only): `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r 3423ae285676c2a10273000f4519163472b443db -- .ufo/waves/round-56/fixtures/c2`; `git … cat-file -p <rev>:<symlink path>`; `git … show <rev>:…/frozen-tables.json` (c2 keys only); `hyprctl getoption misc:disable_autoreload -j`; `hyprctl version -j`; `stat -c '%n %F %s' ~/.config/hypr/hyprland.conf`; `readlink -f /fast`.
