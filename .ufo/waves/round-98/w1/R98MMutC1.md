# R98MMutC1 - C1 mutant population (mutation tester)

Round 98, wave w1, seat R98MMutC1. Read-only mutation probe against the C1
candidate, re-cut to the amended 20-class declaration. This report is the seat
output; the mutant population is the lane draft
`controls/execargv-mutants-r98.json` (the L1 lands it).

## Measured objects

- Candidate: `build/mado-execargv.py` sha256 `acfcc4f7d75162d8035ac26e7ecf48ace8b78dcc8255775e8bab347cfa70ab61` (the final re-pin announced by R98MExecTool; re-read and re-hashed at sweep time).
- Frozen cases: `controls/execargv-cases-r98.json` sha256 `bb78dc3fa162f26f00276d3dff5fa516c46abb0a85bc524adee764e2e9c559b8` (86 cases, 20 classes, 7 refusal cases).
- Oracle: `/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`; glib2 2.90.1-1.
- Mutant file: `controls/execargv-mutants-r98.json` sha256 `5f074f70e6c30339ea61daf2e3f7d849c5ffd181f1e94d1adcca3222eee8438e`.
- Candidate selftest (run by this seat, read-only, at this sha): `MADO_EXECARGV_SELFTEST: checks=38 failed=0`, rc 0.

## Detector and kill definition

The candidate is a model, not a process; the detector is an instrument, not a
candidate. Two detectors were used:

1. In-process: a scratch harness loads the candidate source, calls its
   `run(desktop, args)` model for every frozen case under `LC_ALL=C` (the
   counter's run environment; the locale cases c-04/c-05 depend on it), and
   compares the result with the frozen `expect`. Each call is guarded by a
   2 s SIGALRM; an exception or timeout is recorded as a crash, never a kill.
   This is the sweep that produced the kill table below.
2. CLI: a scratch harness writes the mutant to a scratch copy, runs it as a
   child with `env -i PATH= LC_ALL=C HOME=<case-root>/h` and parses the
   `MADO_EXECARGV: launches=` / `LAUNCH` / `ARGV` lines. Spot-checks on the
   final bytes: plain-01, u-anchor-01, quote-10, bad-01, all with
   `unparsable=0`.

A kill is a **parsed wrong answer**: a wrong launch count or a wrong argv
vector (the predicate scores the multiset of vectors, rule 7; the harness
sorts both sides). A crash, an unparsable output or a timeout is not a kill.

Baseline: the pristine candidate answers **0/86** frozen cases wrong (all 86
exact, including the 7 refusals and the locale/comment/nofuse/nonlocal/
multilaunch cases); the mutant sweep only scores cases the baseline answered
correctly.

The candidate bytes were never modified: every mutant was applied to a
disposable scratch copy under `S=$HYAKU_SCRATCH/mado-r98/R98MMutC1`; the
candidate sha256 before and after the sweep is `acfcc4f7...`. The scratch tree
was removed before the seat yielded; the lane mutant file and this report are
the surviving writes.

## Mutant population

- 79 counted mutants, each `{"id","find","replace","class","expect":"kill"}`.
- Every `find` occurs exactly once in the non-selftest prefix (the prefix ends
  at the first literal `def selftest(`, line 584 of the candidate).
- `find` strings are unique across the counted list, the `not_observable` list
  and the `equivalents` list.
- 16 `not_observable` entries and 8 `equivalents` entries, each with a written
  argument (below).
- The `classes` list is the amended 20-class envelope in declaration order.

## Kill table

One row per counted mutant: the first frozen case that produced a parsed wrong
answer, and the observed wrong answer. The sweep output is captured in this
table; the lane file is the population.

| mutant | class | first kill case | observed wrong answer |
|---|---|---|---|
| plain-01-drop-argv0 | plain | plain-01-noargs | launches=1; [["plain"]] |
| plain-02-empty-argv0 | plain | plain-01-noargs | launches=1; [["", "plain"]] |
| plain-03-extra-argv0 | plain | plain-01-noargs | launches=1; [["x", "/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-01-noargs/probe.sh", "plain"]] |
| plain-05-stop-after-first | plain | plain-02-two-files | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/fast/scratch/hy |
| plain-06-rule4-all | plain | plain-02-two-files | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/fast/scratch/hy |
| plain-07-rule4-no-space | plain | plain-02-two-files | launches=2; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain/fast/scratch/hyaku/ |
| plain-08-rule4-twice | plain | plain-02-two-files | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/fast/scratch/hy |
| plain-09-exec-ignored | plain | plain-01-noargs | ERROR no-exec |
| f-01-one-arg-consumes-all | f | plain-02-two-files | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/fast/scratch/hy |
| f-02-one-arg-uri | f | plain-02-two-files | launches=2; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "file:///fast/scr |
| f-03-consumed-false | f | f-03-two | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/f-03-two/probe.sh", "/fast/scratch/hyaku/mado-r98/R98MMu |
| f-04-drop-first-arg | f | plain-02-two-files | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/fast/scratch/hy |
| f-05-f-uses-dirname | f | plain-02-two-files | launches=2; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/fast/scratch/hy |
| F-01-list-consumes-one | F | F-03-three | launches=3; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| F-02-list-no-space | F | F-03-three | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| F-03-list-reversed | F | F-03-three | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| F-04-list-dirname | F | plain-02-two-files | launches=2; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/fast/scratch/hy |
| F-05-list-comma | F | F-03-three | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| F-06-list-one-iteration | F | F-03-three | launches=3; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| u-file-01-force-dropped | u-file | plain-02-two-files | launches=2; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain"], ["/fast/scratch/ |
| u-file-02-force-ignored | u-file | u-file-01-plain | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-file-01-plain/probe.sh", "file:///fast/scratch/hyaku/m |
| u-file-03-return-uri | u-file | u-file-01-plain | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-file-01-plain/probe.sh", "file:///fast/scratch/hyaku/m |
| u-uri-01-no-fallback | u-uri | u-uri-01-http | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-uri-01-http/probe.sh"]] |
| u-uri-02-scheme-stripped | u-uri | u-uri-01-http | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-uri-01-http/probe.sh", "//example.com/a"]] |
| u-uri-03-uri-upper | u-uri | u-uri-01-http | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-uri-01-http/probe.sh", "HTTP://EXAMPLE.COM/A"]] |
| u-anchor-01-fragment-kept | u-anchor | u-anchor-01-file-frag | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-anchor-01-file-frag/probe.sh", "/fast/scratch/hyaku/ma |
| u-anchor-02-query-drop | u-anchor | u-anchor-01-file-frag | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-anchor-01-file-frag/probe.sh", "/fast/scratch/hyaku/ma |
| u-anchor-03-file-uri-not-local | u-anchor | u-anchor-01-file-frag | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-anchor-01-file-frag/probe.sh", "file:///fast/scratch/h |
| u-anchor-04-uri-suffix | u-anchor | u-uri-01-http | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-uri-01-http/probe.sh", "http://example.com/ax"]] |
| U-mixed-01-uri-branch | U-mixed | u-file-01-plain | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-file-01-plain/probe.sh", "file:///fast/scratch/hyaku/m |
| U-mixed-02-list-consumes-one | U-mixed | F-03-three | launches=3; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| U-mixed-03-reversed | U-mixed | F-02-one | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-02-one/a.txt/fast/scratch/hyaku/mado-r98/R98MMutC1/fin |
| U-mixed-04-list-no-space | U-mixed | F-03-three | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| d-01-dirname-basename | d | d-02-one | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/d-02-one/probe.sh", "a.txt"]] |
| d-02-full-path | d | d-02-one | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/d-02-one/probe.sh", "/fast/scratch/hyaku/mado-r98/R98MMu |
| d-03-consumed-false | d | f-03-two | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/f-03-two/probe.sh", "/fast/scratch/hyaku/mado-r98/R98MMu |
| n-01-basename-dirname | n | n-02-one | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/n-02-one/probe.sh", "/fast/scratch/hyaku/mado-r98/R98MMu |
| n-02-full-path | n | n-02-one | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/n-02-one/probe.sh", "/fast/scratch/hyaku/mado-r98/R98MMu |
| n-03-consumes-all | n | n-03-two | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/n-03-two/probe.sh", "a.txt"]] |
| i-01-drop-icon-flag | i | i-01-with-icon | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/i-01-with-icon/probe.sh", "ic"]] |
| i-02-icon-no-space | i | i-01-with-icon | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/i-01-with-icon/probe.sh", "--iconic"]] |
| i-03-icon-no-quote | i | i-03-icon-space | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/i-03-icon-space/probe.sh", "--icon", "my", "icon"]] |
| i-04-icon-uses-name | i | i-01-with-icon | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/i-01-with-icon/probe.sh", "--icon", "Probe"]] |
| i-05-no-strip | i | i-01-with-icon | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/i-01-with-icon/probe.sh", "--icon", "ic.png"]] |
| i-06-no-strip-return | i | i-01-with-icon | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/i-01-with-icon/probe.sh", "--icon", "ic.png"]] |
| c-01-no-quote | c | c-01-quote-name | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/c-01-quote-name/probe.sh", "OBriens", "App"]] |
| c-02-name-upper | c | c-01-quote-name | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/c-01-quote-name/probe.sh", "O'BRIEN'S APP"]] |
| c-03-name-reversed | c | c-01-quote-name | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/c-01-quote-name/probe.sh", "ppA s'neirB'O"]] |
| k-01-basename | k | k-01-alone | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/k-01-alone/probe.sh", "case.desktop"]] |
| k-02-uses-name | k | k-01-alone | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/k-01-alone/probe.sh", "Probe"]] |
| k-03-consumes-arg | k | k-02-with-f | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/k-02-with-f/probe.sh", "/fast/scratch/hyaku/mado-r98/R98 |
| pct-01-double-pct-nothing | pct | pct-01-100pct | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/pct-01-100pct/probe.sh", "100", "sure"]] |
| pct-02-double-pct-two | pct | pct-01-100pct | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/pct-01-100pct/probe.sh", "100%%", "sure"]] |
| pct-03-trailing-dropped | pct | pct-03-trailing | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/pct-03-trailing/probe.sh", "hi"]] |
| pct-04-join-spaces | pct | plain-01-noargs | launches=1; [["/", "f", "a", "s", "t", "/", "s", "c", "r", "a", "t", "c", "h", "/", "h", "y", "a", "k", "u", "/", "m", "a" |
| bad-01-unknown-literal | bad | pct-05-percent-space | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/pct-05-percent-space/probe.sh", "%", "x"]] |
| bad-02-unknown-char | bad | pct-06-hundred-done | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/pct-06-hundred-done/probe.sh", "100", "done"]] |
| bad-03-unknown-consumes | bad | bad-01-z | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/bad-01-z/probe.sh"]] |
| bad-04-hidden-refused | bad | bad-05-hidden-true | ERROR desktop-file |
| bad-05-type-accepted | bad | bad-07-no-type | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/bad-07-no-type/probe.sh", "/fast/scratch/hyaku/mado-r98/ |
| bad-06-noexec-accepted | bad | bad-04-no-exec | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/bad-04-no-exec/a.txt"]] |
| bad-07-noexec-cause | bad | bad-04-no-exec | ERROR desktop-file |
| bad-08-type-cause | bad | bad-07-no-type | ERROR no-exec |
| quote-01-escaped-dq-closes | quote | quote-03-backslash | ERROR exec-parse |
| quote-02-space-in-quotes | quote | u-file-02-space | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-file-02-space/probe.sh", "/fast/scratch/hyaku/mado-r98 |
| quote-03-single-double-swap | quote | plain-02-two-files | ERROR exec-parse |
| quote-04-single-upper | quote | plain-02-two-files | launches=2; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain", "/FAST/SCRATCH/HY |
| quote-05-invalid-escape-accepted | quote | quote-07-escape-space | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/quote-07-escape-space/probe.sh", "a", "b"]] |
| quote-08-exec-parse-cause | quote | quote-04-unterminated-dq | ERROR desktop-file |
| path-01-no-quote | path | u-file-02-space | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-file-02-space/probe.sh", "/fast/scratch/hyaku/mado-r98 |
| path-02-quote-escape-wrong | path | u-file-03-quote | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/u-file-03-quote/probe.sh", "/fast/scratch/hyaku/mado-r98 |
| d-04-unimplemented | d | d-02-one | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/d-02-one/probe.sh"]] |
| n-04-unimplemented | n | n-02-one | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/n-02-one/probe.sh"]] |
| plain-10-rule4-dropped | plain | plain-02-two-files | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/plain-02-two-files/probe.sh", "plain"]] |
| quote-10-unterminated-accepted | quote | quote-04-unterminated-dq | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/quote-04-unterminated-dq/probe.sh", "unterminated"]] |
| nonlocal-01-f-uri-appended | nonlocal | nonlocal-01-f-http | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/nonlocal-01-f-http/probe.sh", "http://example.com/a"]] |
| multilaunch-01-list-one-arg | multilaunch | F-03-three | launches=3; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/F-03-three/probe.sh", "/fast/scratch/hyaku/mado-r98/R98M |
| comment-01-parsed | comment | comment-01-before | ERROR desktop-file |
| nofuse-01-ignored | nofuse | nofuse-01-u-file | launches=1; [["/fast/scratch/hyaku/mado-r98/R98MMutC1/final/cases/nofuse-01-u-file/probe.sh", "/fast/scratch/hyaku/mado-r9 |

All 79 counted mutants are killed; none survived and none was recorded as a
crash-only mutant. The one crash on a non-kill case is F-06-list-one-iteration
on F-01-noargs (the kill is the parsed wrong answer on F-03-three; the crash is
not counted).

## Class coverage

| class | counted mutants | killed |
|---|---|---|
| plain | 9 | 9 |
| f | 5 | 5 |
| F | 6 | 6 |
| u-file | 3 | 3 |
| u-uri | 3 | 3 |
| u-anchor | 4 | 4 |
| U-mixed | 4 | 4 |
| d | 4 | 4 |
| n | 4 | 4 |
| i | 6 | 6 |
| c | 3 | 3 |
| k | 3 | 3 |
| pct | 4 | 4 |
| bad | 8 | 8 |
| nonlocal | 1 | 1 |
| nofuse | 1 | 1 |
| multilaunch | 1 | 1 |
| comment | 1 | 1 |
| quote | 7 | 7 |
| path | 2 | 2 |

All 20 classes have at least one counted mutant and at least one kill; the
counter predicate `class_kills == 20/20` is satisfied by this population.

## Non-killers

### not_observable (16)

These mutants cannot be observed through the frozen case surface. Each entry
carries its written argument in the lane JSON; the argument is repeated here.

- `m-code-emits` (bad): no frozen case carries %m; the fresh generator may, but the mutant leg runs only the frozen cases
- `DN-codes-dropped` (d): no frozen case uses %D/%N (the classes are d/n lowercase); the fresh generator may
- `duplicate-key-first` (plain): no frozen case carries a duplicate key
- `early-key-accepted` (plain): no frozen case has a key before the first group
- `empty-exec-accepted` (bad): no frozen case has an empty Exec (bad-04 is a missing key)
- `tab-not-delimiter` (quote): no frozen case carries a tab in Exec
- `newline-not-delimiter` (quote): no frozen case carries a newline in Exec
- `backslash-outside-literal` (quote): no frozen case carries a shell-level backslash outside quotes (the invalid-escape cases refuse at GKeyFile)
- `empty-icon-emitted` (i): no frozen case has Icon='' (i-02 has Icon null)
- `crash-infinite-loop` (plain): dropping rule 4 without consuming leaves args and loops forever; the detector records a timeout/crash, not a kill
- `plain-04-single-launch-crash` (plain): the for-loop falls through and build_launches returns None, so run() raises TypeError; a crash is not a kill. The single-launch direction is counted as plain-05-stop-after-first, which returns a parsed answer
- `quote-06-exec-parse-not-refused` (quote): the static parse in run() refuses before build_launches is called; a single-site mutant at the build parse cannot change the answer, so the exec-parse refusal needs two independent sites to disappear
- `quote-07-exec-parse-result` (quote): the static parse in run() refuses before build_launches is called; a single-site mutant at the result mapping cannot change the answer
- `crash-none-uri` (u-uri): for a non-local URI local is None and shell_quote(None) raises; a crash is not a kill
- `i-07-absolute-icon-stripped` (i): no frozen case carries an absolute Icon (i-01..i-05 use ic.png, my icon, null, empty); the fresh generator may. The rule is measured (Icon=/tmp/ic.png keeps the extension) and the candidate implements the guard.
- `pct-08-bytewise-codepoint` (pct): no frozen case puts a multi-byte UTF-8 character after % (pct-05/06 use a space, pct-07 uses 1); the fresh generator may. The byte-wise rule is measured and the candidate implements the byte walk.

### equivalents (8)

These mutants are behaviourally equivalent to the baseline on the frozen
surface (or are a named limit of the model). Each carries its argument.

- `u-anchor-05-hash-bypass` (u-anchor): the '#' bypass is a named limit: a local file URI is fragment-free after arg_model, and a non-local URI answers the URI on both branches (L1 ruling, measured)
- `hidden-accepted` (bad): the corrected rule reads Hidden and does not refuse it (measured: gio launch of Hidden=true succeeds); this mutant only reads it, so it is behaviourally the baseline
- `k-04-no-quote` (k): the frozen/counter desktop path carries no reserved character, so the parsed argv is identical; k is covered by k-01/k-02
- `one-arg-pop-last` (f): with one-arg codes each launch carries exactly one arg, so consuming from the end only permutes launch order, which rule 7 declares unobservable; no frozen case has two one-arg codes
- `list-trailing-space` (F): a trailing space after the last quoted list arg is discarded by the shell parser; same argv
- `rule4-without-args-guard` (plain): when no args remain macro('f') returns without appending; the extra space is discarded by the parser
- `local-uri-unescaped` (u-file): no frozen case has a '#' or '%' in a file name; the local URI is only consumed by the dead '#' branch (the path is used for %u/%U)
- `d-no-quote` (d): the frozen dirname is the case root, which carries no reserved character; same parsed argv

The required-by-seat directions that are now equivalents are explicit:
`u-anchor-05-hash-bypass` (the `#` bypass is a named limit; the local file URI
is fragment-free after the GFile step and a non-local URI answers the URI on
both branches) and `hidden-accepted` (the corrected rule reads Hidden and does
not refuse it; the killable direction is `bad-04-hidden-refused`, which is
counted and kills the Hidden=true case). The `%d`/`%n` unimplemented direction
is counted as `d-04-unimplemented` and `n-04-unimplemented`; the
unterminated-quote direction is counted as `quote-10-unterminated-accepted`.

## Reference cross-check

A second instrument (an independent scratch model of the declaration) was
validated against `/usr/bin/gio` on 47 self-built cases across the original 16
class shapes plus refusal edges: 47/47 exact (launch count and sorted vectors).
Against the 16-class frozen file as read at 16:50:07 it scored 63/64; the only
miss was `bad-06-not-keyfile`, the oracle inconsistency routed to the L1 and
re-measured by the oracle seat. The final candidate's own baseline against the
20-class file is 0/86.

## Findings routed before the freeze

These were measured by this seat and sent to the L1 / the affected seats; the
declaration or the artifacts changed in response.

1. **u-anchor fragment**: `gio launch` converts each argument with
   `g_file_new_for_commandline_arg` (`gio-tool-launch.c:106`); a local file
   URI's fragment (and query) never reaches `expand_macro_uri`. Measured:
   `%u` + `file:///.../a.txt#frag` -> the path; `%u` + `http://...#y` -> the
   URI. The candidate initially returned the raw URI; fixed in the final
   candidate (`arg_model` returns `(local_uri_of(local), local)`).
2. **`%i` extension strip**: `gdesktopappinfo.c:2044-2055` cuts a trailing
   `.png`/`.xpm`/`.svg` before `%i` for a NON-absolute Icon; frozen i-01/i-04
   expect `ic` for `Icon=ic.png`. Folded into rule 3; the final candidate
   keeps an absolute Icon path intact.
3. **GKeyFile escapes**: `a\ b`, `a\z`, `a\:b`, `"a\"b"` all make
   `gio launch` print `Unable to load application information` (rc 1, no
   record) -> `desktop-file`; frozen quote-07/08. The candidate refuses them.
4. **Hidden=true launches**: `gdesktopappinfo.c:2022` reads Hidden and does not
   branch; the only launch-path hidden check is the desktop-id lookup at
   `:2209`. Measured rc 0 with a probe record. The declaration now reads Hidden
   and does not refuse it; `bad-05-hidden-true` is a success case and
   `bad-04-hidden-refused` is the counted kill.
5. **Probe interleaving**: the shared-append probe merged the concurrent
   spawns' records (raw `@@@ 2` / `P0` / `A` lines interleaved); the oracle
   moved to per-spawn files with a lock-assigned sequence number. The old
   frozen `f-04`/`n-03` order was a race artifact; rule 7 now scores the
   multiset, so order is not part of the surface.
6. **Counter/oracle materialisation mismatch**: the counter's `_desktop_escape`
   doubled backslashes while the oracle writes values literally, and the
   counter used `t.desktop` while the oracle used `case.desktop`. Both were
   routed to R98MExecCounter and fixed before the freeze.
7. **bad-06-not-keyfile**: the 16-class frozen case had a valid desktop block
   but a `desktop-file` expect; the oracle re-measured it with `desktop_raw`.
8. **Indented comment (20-class amendment)**: `comment-03-indented` carries
   `"  # indented comment"`; the candidate's `parse_desktop` checked
   `line[0] == '#'` without stripping leading whitespace, so the line was
   parsed as a key -> grammar -> desktop-file. Measured expect: a launch. The
   final candidate lstrips `KEYFILE_WS` before classification and answers it.
9. **20-class amendments**: the declaration now includes `nonlocal` (`%f`/`%F`
   with a non-local URI -> nothing), `nofuse` (`X-GIO-NoFuse=true` flips
   `%u`/`%U` to the URI form), `multilaunch` (`%f %f`, `%f %F`), `comment`,
   the locale-selected `%c` (`Name[en_US]` under `LC_ALL=en_US.UTF-8`), the
   canonicalized `%k`, the absolute-Icon exception, and the byte-wise `%`
   walk. The final candidate implements them; the baseline is 0/86.

## Limits

- The mutant leg is frozen-case-only. Shapes that only the fresh generator
  can produce (`%m`, `%D`/`%N`, duplicate keys, comments in Exec, empty Exec,
  tabs, newlines, `%f` with a non-local URI, empty Icon, absolute Icon,
  multi-byte `%` selector, crash-only mutants) are listed in `not_observable`
  with their arguments; they are not counted kills.
- The `#` bypass and Hidden acceptance are named limits/equivalents, not
  counted kills; the observable directions (`force_file_uri` dropped, Hidden
  refused) are counted.
- The kill evidence is the sweep table in this report (in-process detector)
  plus the CLI spot-checks; the lane mutant file is the frozen population the
  counter consumes.

## Tooling

No tool was installed or upgraded; no pacman transaction, no sudo, no host
service change. The probes used `/usr/bin/python3` (stdlib only), `/usr/bin/gio`
and the existing shell. Scratch: `S=$HYAKU_SCRATCH/mado-r98/R98MMutC1`; it is
removed before the seat yields (the lane files above are the only writes).

