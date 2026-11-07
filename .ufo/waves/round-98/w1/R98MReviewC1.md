# R98MReviewC1 - C1 review (round 98, wave w1)

Reviewer seat. Scope: attack C1 without editing the candidate. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; base `35f3ce808788b11c063309b1b5ad0192754795ea`.

## Artifacts measured (sha256 at the final read)

| artifact | sha256 | state |
|---|---|---|
| `controls/execargv-cases-r98.json` | `9b39299ad558dec0a70768a1c70eec0e3e2722fc8d567d58106aff53d6aad02f` | 64 cases, 16 classes (the 20-class re-freeze had not landed) |
| `controls/execargv-probe-r98.py` (oracle renderer) | `48c9a1694316d3ebbfcc92567dae15933e400cb1946d0643b410cbfb2d72d358` | per-spawn file + lock sequence |
| `controls/execargv-fresh-r98.py` (fresh generator) | `f9a0df2766143cc15adf512ddc47e916123460867189a1af5043d2283ced38c6` | |
| `controls/execargv-mutants-r98.json` | `1794064b253f5c6fcb913fb7b366bcca7657caf496003d38eb17b86feb595fbf` | 78 mutants, 19 classes, pins candidate `31aca8d8` |
| `build/mado-execargv.py` (candidate) | `630faeee44af175760917295c9e3c712fbf6ee0dab43e95d4e473db71967829e` | |
| `build/c1-r98-execargv.py` (counter) | `79045e9742393d3ccada0ae145294a8263902c24e35331fb4df88f1176649ddd` | 20 classes, MIN_CASES 70 |
| `/usr/bin/gio` | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` | glib2 2.90.1-1 |

The lane moved while this review ran; every number names the bytes it was measured on. No tool was
installed or upgraded.

## Verdict

The candidate answers the frozen 16-class set 64/64, and the amended rules I could exercise all
match the oracle (`%f %f` + 3 -> 2 launches, `%f %F` + 3 -> 1, non-local `%F`/`%D`/`%N` with the
separator rule, `%d`/`%n` on a non-local URI, `%i` empty Icon, `Name[de]`/`Name[C]` under
`LC_ALL=C`, `% `, `%1`, `%%` attached, a `#` comment line, `Hidden=true`, `X-GIO-NoFuse=true` for
`%u`/`%U`, and `%k` with a relative DESKTOP argument). Two source-level rules remain wrong in the
candidate and no case exercises either (O1, O2). The artifacts are mid-re-freeze: the case file is
still 16 classes, the mutant file still pins an older candidate and four of its anchors no longer
occur once, and the case file's renderer pin no longer matches the renderer bytes (O3). Those three
are mechanical and must be re-cut before measurement; none of them is a model defect.

## Open findings

### O1 (medium) - the candidate strips an icon extension from an absolute Icon path

Source: the `.png`/`.xpm`/`.svg` strip is the `else` branch of `g_path_is_absolute`
(`gdesktopappinfo.c:2036-2055`). Measured: `Icon=/tmp/ic.png`, `Exec={probe} %i` -> oracle
`["{probe}", "--icon", "/tmp/ic.png"]`, candidate `["{probe}", "--icon", "/tmp/ic"]`. The frozen `i`
class uses only `ic.png`, `my icon` and null; the fresh `ICONS` pool is `[None, "ic.png",
"my icon"]`. No case exercises the guard. Fix: skip the strip when the name is absolute
(`build/mado-execargv.py`, `strip_icon_ext`).

### O2 (medium) - the candidate's `%` walk is character-wise; the source walks bytes

`expand_application_parameters` advances a `const char *p` (`gdesktopappinfo.c:2721-2725`), so `%`
consumes exactly one byte. Measured: `Exec={probe} %<U+00E9>x` -> oracle `["{probe}", "\udca9x"]`
(the `%` ate 0xC3, leaving 0xA9 and `x`), candidate `["{probe}", "x"]`. No frozen or fresh case
carries a non-ASCII byte after `%`. Fix: walk the UTF-8/surrogateescape bytes.

### O3 (blocker until re-cut) - the artifacts are mid-re-freeze

At the final read the counter's own setup checks fail on the committed artifacts:

- `setup-envelope-classes`: the case file has 16 classes, the counter requires the 20
  (`build/c1-r98-execargv.py:119-122`);
- `setup-renderer-sha256`: the case file's `renderer_sha256` is `60ea7734`, the renderer file now
  hashes `48c9a169` (the counter verifies the file beside the cases, `:982-990`);
- mutant validation: the mutant file pins candidate `31aca8d8` while the candidate is `630faeee`,
  and four anchors no longer occur exactly once in the non-selftest bytes
  (`f-01-one-arg-consumes-all`, `U-mixed-01-uri-branch`, `U-mixed-02-list-consumes-one`,
  `d-03-consumed-false`).

Re-cut the case file (20 classes, >=70 cases, current renderer pin), re-cut the mutants against the
final candidate bytes, and re-run the candidate. The `nofuse` class needs a case shape: the
candidate now reads `X-GIO-NoFuse` and matches the oracle (measured: `%u` + file ->
`file://<root>/a.txt`; `%U` + file + http -> `[file URI, http URI]`; `false` -> the path), but
`DESKTOP_KEYS` (`:132`) does not carry the key, so the cases must use `desktop_raw` or the schema
must add it.

### O4 (medium) - the case schema admits shapes the model declares out of scope

`validate_case` accepts `Terminal: true` and any `Path` string, while the candidate's named limits
exclude both. Measured: `Terminal=true` -> gio exits 0 with no record (xdg-terminal-exec fails
without a display) and the renderer's structural cause prints `exec-parse`; `Path=nope` -> gio rc 1
`Failed to change to directory "nope"`, also labelled `exec-parse` although the declaration's cause
vocabulary has no name for it. The frozen file has neither and the fresh generator sets both null.
Fix: `validate_case` rejects `Terminal: true` and a non-null `Path` (or the declaration names the
causes).

### O5 (low) - the cause for an Exec that fails `g_shell_parse_argv` at load is pinned by the cases, not by the declaration

`quote-04-unterminated-dq` and `quote-05-unterminated-sq` freeze `{"error": "exec-parse"}` while gio
reports the load failure (`Unable to load application information`), the surface rule 1 maps to
`desktop-file`. The candidate prints `exec-parse` and matches. Rule 1 should say it.

### O6 (low) - an argv value containing a newline is mislabelled as a refusal

The probe is line-oriented. With a file named `a\nb` the record file holds two lines where one
sealed record is required, so `read_probe_out` finds no sealed record and `case_expect` returns
`{"error": "exec-parse"}` (measured; the old append-file renderer froze a truncated value instead).
gio launches the case correctly. Fix: encode values in the probe, or refuse to freeze a case whose
measured argv contains a newline.

### O7 (low) - the candidate's named limits contradict its code

`build/mado-execargv.py:22` still says "X-GIO-NoFuse is not read", while `run()` reads it and
`build_launches` takes `no_fuse`. The same class as round-97's M97-1 (a stated rule contradicted by
the round's own bytes). Fix the docstring before the freeze.

### O8 (low) - the committed control receipt's two models are the same function

`controls/control-naive-r98.py:134-138`: `naive` and `noexp` both return `Exec.split()`, so the
receipt's `noexp_correct=2` is the naive model's score. The counter's embedded `NOEXP_SRC` is
distinct (tokeniser, no field codes), so the counter's control leg is sound. My own score over the
frozen 64: naive 3/64, no-expansion (strip codes, then split) 10/64 - both strictly fewer than 64.

### O9 (low) - predicate (iv) is not checkable as written

"every frozen label was produced by this binary at the freeze" cannot be verified from the
artifacts: the counter checks the installed `gio` sha256 and the renderer sha256 and never re-runs
gio on a frozen case. The checkable form is "the case file's `gio_sha256` equals the installed
binary's and `renderer_sha256` equals the renderer bytes".

### O10 (low) - kill accounting counts a case the original candidate also fails

`build/c1-r98-execargv.py:1111-1117`: `wrong_ids` is computed from the mutant's results alone, so a
mutant wrong on a case the original is also wrong on counts as killed by that case. The kill should
be measured on the cases the original answers correctly (`oc` is already available for the crash
comparison). The crash rule itself is sound: a new crash is `crashed_not_killed`, never a kill, and
the selftest asserts it.

### O11 (low) - the fresh generator labels every case `exec-parse` for a relative `--dir`

`build_root` joins the relative parent and `case_expect` runs gio with `cwd=root` while passing the
relative desktop path, so the path resolves twice. Measured: `--dir fg1/roots` ->
`FRESH_GEN: cases=60 ok=0 refused=60`, all `refusal:exec-parse`; the same seed with an absolute
`--dir` -> `ok=52 refused=8`. The counter passes an absolute `gen_dir`, so it is unaffected.

## Resolved during the wave (recorded so the L1 can confirm the final pins)

- **R1 - the settle race.** At the append-file renderer (`c5c69445`) the oracle reproduced its own
  `%f`-with-3-files label 28/40 times (5/40 one-launch labels, 6/40 permuted). At the per-spawn-file
  renderer (`60ea7734`) I measured 120 runs over `%f` x 3, `%f` x 6 and the rule-4 shape: **no lost
  record**; the only variance is the order, which rule 7 excludes from the surface. Residual: the
  200 ms quiet window has no positive completion signal, so a straggler child delayed past it would
  still be missed (not observed in 120 runs).
- **R2 - root embedding in fresh expects.** At `c5c69445` `canon` rewrote the root only as a prefix,
  so `end%` + `%f` froze `end<generator root>/file` (2/60 at seed 98) and the counter's rebuilt root
  could never match. The current `canon` substitutes anywhere; measured same seed, two different
  `--dir` trees -> 0/60 label differences.
- **R3 - candidate rules fixed during the wave.** `u-anchor-01-file-frag` (fragment kept),
  `u-anchor-03-file-query-frag` (query kept), `%k` with a relative DESKTOP argument (now
  CWD-joined), and `X-GIO-NoFuse=true` for `%u`/`%U` (now read and matching the oracle) all pass at
  the final candidate.
- **R4 - earlier artifact mismatches.** The counter's `ORACLE_NAME` vs the case file's `oracle`
  string, `validate_case` rejecting the null-`Type`/null-`Exec` refusal cases, and the case file
  missing `renderer_sha256` are fixed.

## Step 1 - independent re-derivation (24 cases, all 16 classes, 3 runs each)

My own builder (`rederive.py` in this seat's scratch): case root from the frozen dict, probe with the
contract's `@@@ <argc>`/`P0=`/`A<i>=` records, `env -i LC_ALL=C HOME=<root>/h PATH=/usr/bin:/bin
/usr/bin/gio launch <root>/case.desktop <args...>`, cwd = root, 1.0 s quiet / 12 s cap.

Sample: the first case of each of the 16 classes by file order, plus the multi-launch and refusal
cases, 24 total. Result: 23/24 reproduced exactly; `n-03-two` reproduced in 2/3 runs with one partial
record in the third (the old renderer; the current renderer produced no partial record in 120 runs).
Every frozen multiset matched whenever the oracle produced complete records. `bad-04-no-exec` matched
the refusal cause 3/3.

| id | class | order | multiset | my launch counts |
|---|---|---|---|---|
| plain-01-noargs | plain | 3/3 | 3/3 | 1,1,1 |
| f-01-noargs | f | 3/3 | 3/3 | 1,1,1 |
| F-01-noargs | F | 3/3 | 3/3 | 1,1,1 |
| u-file-01-plain | u-file | 3/3 | 3/3 | 1,1,1 |
| u-uri-01-http | u-uri | 3/3 | 3/3 | 1,1,1 |
| u-anchor-01-file-frag | u-anchor | 3/3 | 3/3 | 1,1,1 |
| U-mixed-01-file-http | U-mixed | 3/3 | 3/3 | 1,1,1 |
| d-01-noargs | d | 3/3 | 3/3 | 1,1,1 |
| n-01-noargs | n | 3/3 | 3/3 | 1,1,1 |
| i-01-with-icon | i | 3/3 | 3/3 | 1,1,1 |
| c-01-quote-name | c | 3/3 | 3/3 | 1,1,1 |
| k-01-alone | k | 3/3 | 3/3 | 1,1,1 |
| pct-01-100pct | pct | 3/3 | 3/3 | 1,1,1 |
| bad-01-z | bad | 3/3 | 3/3 | 1,1,1 |
| quote-01-dquote | quote | 3/3 | 3/3 | 1,1,1 |
| path-01-space-f | path | 3/3 | 3/3 | 1,1,1 |
| plain-02-two-files | plain | 3/3 | 3/3 | 2,2,2 |
| plain-04-three-files | plain | 3/3 | 3/3 | 3,3,3 |
| f-03-two | f | 3/3 | 3/3 | 2,2,2 |
| f-04-three | f | 3/3 | 3/3 | 3,3,3 |
| d-03-two | d | 3/3 | 3/3 | 2,2,2 |
| n-03-two | n | 2/3 | 2/3 | 2,2,2 (one partial record) |
| bad-03-z-two | bad | 3/3 | 3/3 | 2,2,2 |
| bad-04-no-exec | bad | 3/3 | n/a | refusal `no-exec` 3/3 |

## Step 2 - candidate against the oracle

- Current frozen 64 (16 classes), candidate `630faeee`: **64/64**.
- The same 24-case sample: 24/24.
- The 20-class re-freeze had not landed; the counter rejects the current file (O3), so this 64/64 is
  against the 16-class file only.

## Step 3 - the cheapest no-work controls over the frozen 64

| model | score (multiset) |
|---|---|
| naive `Exec.split()`, one launch | 3/64 |
| no-expansion (strip field codes, then split), one launch | 10/64 |

Both strictly fewer than the total, so the declaration's control claim is true on the frozen set.
The L1's own 23-case family (`receipts/control-naive-r98.json`) reports 2/23 and 2/23, but its two
models are the same function (O8).

## Step 4 - attack probes (48 probes; oracle and candidate on the same root)

43 same, 5 differ at the candidate revision `31aca8d8`; at the final candidate `630faeee` the
fragment/query, `%k` and `X-GIO-NoFuse` probes also match, leaving:

| probe | oracle | candidate | class |
|---|---|---|---|
| `Icon=/tmp/ic.png`, `%i` | `--icon /tmp/ic.png` | `--icon /tmp/ic` | O1, real defect |
| `%<U+00E9>x` | `\udca9x` | `x` | O2, real defect |
| `Path=nope` | rc 1, cwd failure | 1 launch | O4, out of scope |
| `Terminal=true` | rc 0, no record | 1 launch | O4, out of scope |
| `Exec={probe} "unterminated` | load failure; renderer label `exec-parse` | `exec-parse` | O5, convention |

The amended-rule probes, all matching: `%f %f` + 3 -> 2 launches (2 then 1 argument); `%f %F` + 3 ->
1 launch; `%F` with http+file and file+http -> the file only; `%D`/`%N` with http+file -> the file's
dirname/basename only; `%d`/`%n` on an http URI -> nothing; `%i` with an empty Icon -> `--icon ''`;
`Name[de]` and `Name[C]` under `LC_ALL=C` -> `Name`; `% ` and `%1` -> nothing; `%%` attached ->
literal `%`; a `#` comment line in the desktop file -> ignored; `#` after a tab in Exec -> a literal
token; `Hidden=true` -> launches; `X-GIO-NoFuse=true`/`false` for `%u`/`%U`; `%k` with a relative
DESKTOP argument.

## Step 5 - the counter's kill rule

- A crashing mutant is **not** a kill: `new_crash` routes to `crashed_not_killed`
  (`build/c1-r98-execargv.py:1114-1118`); `--selftest` at the final pin prints
  `MADO_COUNTER_SELFTEST: checks=16 failed=0`, rc 0, and asserts `st-mutant-crash`.
- My independent sweep at the matching pin (mutants `c5b66f58`, candidate `31aca8d8`, 64 cases,
  multiset, a kill counted only on a case the original answers correctly): **75 mutants, 75 killed,
  0 crashed_not_killed, 0 survived, 16/16 classes kill at least one**. Baseline 64/64. The current
  mutant file (`1794064b`, 78 mutants, 19 classes) pins the older candidate and four anchors no
  longer occur once (O3), so it must be re-cut before its numbers mean anything.
- A nondeterministic case is **not** re-verified at measurement time: the frozen labels are trusted
  and the fresh labels are measured live. At the current renderer the count is stable (R1), so this
  is no longer an active defect; the residual is the window's lack of a positive completion signal.
- Accounting gap: O10.

## Residual risk and verification gaps

- The re-frozen 20-class case file and the re-cut mutant set were not present at my final read; O3
  must be resolved and the candidate re-measured afterwards.
- I did not run the counter end-to-end (it needs the candidate committed at `--rev`; the candidate is
  a draft in `build/`). I exercised `validate_cases`, `--selftest` (16/0), and read the scoring,
  fresh and mutant code, and I reproduced the kill sweep independently.
- Latent, not exercised by any frozen or fresh case: O1 (absolute Icon), O2 (multibyte after `%`),
  O6 (newline in a value).
- `render_desktop` encodes ASCII, so a non-ASCII Name or Exec crashes the renderer instead of a
  clean setup error.

## Exact sentences to change before the freeze

1. Case schema: add `X-GIO-NoFuse` (bool|null) - the `nofuse` class needs it, the candidate now
   reads it, and `DESKTOP_KEYS` does not carry it (cases must otherwise use `desktop_raw`).
2. Rule 3 `%i`: "when Icon is set **and is not an absolute path**" (the strip is the `else` of
   `g_path_is_absolute`, gdesktopappinfo.c:2036-2055).
3. Rule 2: state that the walk is **byte-wise** (a `%` before a multibyte character consumes one
   byte; measured `%<U+00E9>x` -> `\udca9x`).
4. Rule 1: add "an Exec that the load-time `g_shell_parse_argv` rejects refuses with `exec-parse`
   (measured: `quote-04`, `quote-05`)".
5. Oracle section: "a label is frozen only when two consecutive measurements agree; a timeout with
   an incomplete record is SETUP_ERROR, never a label" (the 200 ms quiet window is not a completion
   signal).
6. Predicate (iv): replace "every frozen label was produced by this binary at the freeze" with "the
   case file's `gio_sha256` equals the installed binary's and `renderer_sha256` equals the renderer
   bytes".
7. Predicate (v): require the two control models to be distinct functions (the counter's are; the
   committed control receipt's are not).
