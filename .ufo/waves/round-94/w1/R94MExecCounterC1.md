# R94MExecCounterC1 — C1 counter (`quality/counters/c1-r94-mimeglob.py`), PRED-C1-r94-v1

Seat: R94MExecCounterC1 (executor, leaf). Round 94 / hyaku run 15 / attempt 1, wave w1. Base `a3de9972`.
Files written: `quality/counters/c1-r94-mimeglob.py` (new, mode 755) and this report. Nothing else.
Every run below is **DRAFT** (`--draft-tool` = candidate bytes; the frozen inputs are not yet frozen). Nothing was
written under `.ufo/waves/round-94/receipts/`. No installs, no upgrades (`pacman -Q` read-only only).

## 1. What the counter does (PRED-C1-r94-v1)

| clause | implementation |
|---|---|
| tool identity | `git -C <repo> show <rev>:tools/mado-mimeglob.py` (or `--draft-tool`); sha256 vs `--expect-tool-sha256` → `tool_pin=ok|FAIL` (FAIL is a miss) |
| frozen inputs | `--cases --mutants --oracle-src --fresh-gen --host-names` each sha256-pinned; mismatch → `SETUP_ERROR` rc 2. The case file's `oracle_src_sha256` must equal the pinned oracle source |
| oracle | `gcc -O1 -o <scratch>/oracle <oracle-src> $(pkg-config --cflags --libs gio-2.0)`; prints the binary sha256 and `pacman -Q glib2 shared-mime-info` |
| (i) frozen cases | each case materialised under a fresh dir in `--scratch-root` (`{root}` substituted, base64 bytes; a key ending in `/` is a directory); oracle run as `env -i LC_ALL=C` + case env (null = unset); live labels must equal the recorded labels, else `SETUP_ERROR oracle_drift=<ids>`; tool run with env→flags (`--data-home[-unset]`, `--data-dirs[-unset]`, `--home`, then `--` and the names); correct iff every name's (type, uncertain) equals the label. Nonzero exit (incl. exit 3), no JSON, or a malformed result → `crash`: counted as not answered and as wrong |
| (ii) fresh | `--fresh-gen --seed S --n N --out F --scratch-root D` run with `-I`; cases labelled by the live oracle; `--fresh-seed` fixes S, default random (printed) |
| (iii) host | `--host-names`: `#` lines are the header; every other non-empty line is one name whose `\xHH` escapes are unescaped to bytes; run under the counter's own `HOME`, `XDG_DATA_HOME`, `XDG_DATA_DIRS` (printed; unset stays unset) against the live oracle, in chunks of 2000 names |
| (iv) mutants | each `find` must occur exactly once in the tool bytes (else `SETUP_ERROR`); killed iff ≥1 frozen case gives a well-formed JSON answer differing from the label; see 2.4 for the crash rule |
| (v) controls | do-nothing = `application/octet-stream`, uncertain 1 on every name; naive map = last `.ext` → highest-weight `*.ext` globs2 entry, uncertain 0 (both case readings, see 2.1); base = `git show <base-rev>:tools/mado-mimeglob.py`, absent → `base_correct=0` |
| verdict | `MADO_MIMEGLOB_COUNT: TARGET_MET|TARGET_MISSED|SETUP_ERROR`, with `DRAFT_` prefix under `--draft-tool`; rc 0/1/2, 3 for DRAFT |

Conjuncts as coded: `tool_pin ok`, `correct == cases`, `answered == cases`, `fresh == fresh_n`, `host == host_n`,
`killed == mutants`, `do_nothing < cases`, `naive < cases`, `base < cases`.

## 2. Judgement calls (the declaration is silent or ambiguous; the L1 should freeze these before data)

1. **Naive control folding.** The declaration does not say whether the extension is ASCII-folded. The counter scores
   both readings and gates on the stronger one (`naive_correct = max(exact, folded)`), printing both. A weaker
   reading would let (v) pass by construction.
2. **Do-nothing control** is computed in-process (a constant answer), not a committed file (critic C1-F4 wants control
   files pinned by sha256; not done here).
3. **Class list (critic C1-F1).** PRED (i) reads "every class named in the case file", which no data can falsify.
   The counter does not enforce a class list; it prints `classes=K`. The schema lists **20** classes (the critic's
   "21" is off by one); the frozen file has all 20, each with ≥9 cases. Freezing the enumerated list is the L1's call.
4. **Crash rule for mutants.** A first version counted every not-killed mutant that crashed *anywhere* as
   `crashed_not_killed`; that charged the candidate's own two refusals (2.5) to every mutant (22 false
   `crashed_not_killed`). Final rule: a survivor is `crashed_not_killed` only if it crashes on a case where the
   candidate does not; otherwise `survived`. The verdict prints `survived=`.
5. **Fresh seed** defaults to 4 random bytes (printed as `fresh_seed=`); `--fresh-seed` fixes it. `--fresh` defaults to 40.
6. **Verdict line** keeps the frozen field order and appends `classes`, `naive_exact_correct`, `naive_folded_correct`,
   `survived`, `oracle_sha256`, `tool_sha256`.
7. **Frozen file moved during the run.** `controls/mimeglob-cases-r94.json` changed at 03:46 (sha
   `76215052…` → `2df52ec2…`) while I was running; my earlier DRAFT used the old bytes. All numbers below are from
   the current bytes (pinned in the run).

## 3. Measured-shape DRAFT on the frozen inputs (DRAFT; candidate bytes; current case bytes)

Inputs (sha256 pins as passed): cases `2df52ec2…3e92`, mutants `f6784…` (57), fresh gen `ab76b97e…`, host names
`4b6d6a6c…`, oracle source `9c4337b3…6b11`, candidate `0700915a…d63e`. Base `a3de9972` has no tool.
`--fresh 40 --fresh-seed 94 --workers 8`, wall 72 s, rc 3 (verbatim from the run's stdout):

```
oracle_binary_sha256=38cea1b00dd65bb2531921aeaf7f586f3524a62fa6823b4f2c49c910724239e2
pacman -Q glib2 shared-mime-info:  glib2 2.90.1-1 / shared-mime-info 2.5.1-2
host env HOME='/home/vgpnk' XDG_DATA_HOME='/home/vgpnk/.local/share' XDG_DATA_DIRS='/usr/local/share:/usr/share' names=9745
base: tool absent at base-rev (answered=0)
MADO_MIMEGLOB_COUNT: DRAFT_TARGET_MISSED pred=PRED-C1-r94-v1 rev=draft:…/mado-mimeglob.c1.py tool_pin=ok cases=235 correct=233 answered=233 text=127/129 cache=83/83 mixed=23/23 classes=20 fresh=40/40 fresh_seed=94 host=9745/9745 mutants=57 killed=35 crashed_not_killed=0 survived=22 do_nothing_correct=30 naive_correct=40 naive_exact_correct=38 naive_folded_correct=40 base_correct=0 oracle_sha256=38cea1b0…239e2 tool_sha256=0700915a…d63e
```

Per clause (DRAFT):

- (i) **fails**: 233/235. Misses are `bytes-04-invalid-utf8-in-pattern` and `bytes-05-invalid-utf8-literal` (both
  CRASH). See 3.1.
- (ii) fresh 40/40 ✓. (iii) host 9745/9745 ✓. tool_pin ok ✓.
- (iv) **fails**: 35/57 killed, 22 survived (listed in 3.2).
- (v) controls all miss: do-nothing 30/235, naive 40/235 (folded reading; exact 38), base 0/235 ✓.

### 3.1 Candidate refusal on invalid UTF-8 (the two (i) misses)

Reproduced (Python driver, escaped output; the shell tool cannot echo raw bytes):
glob file `dh/mime/globs2` = `50:app/x-hi:*.hi\xff\n`, name `f.hi\xff`.

- candidate: `python3 -I tools/mado-mimeglob.py --json --data-home <dh> --data-dirs "" --home <h> -- f.hi\xff` →
  rc 3, stdout `MADO_MIMEGLOB: UNSUPPORTED <dh>/mime//globs2: line is not valid UTF-8`
  (candidate `TextDB.read`, the `except UnicodeDecodeError: raise Unsupported` arm).
- oracle: `LC_ALL=C XDG_DATA_HOME=<dh> XDG_DATA_DIRS= oracle f.hi\xff` → rc 0, `app/x-hi	0`.

The declaration's PRED counts a refusal as not answered (wrong). So this is a real candidate defect against the
frozen labels, not a counter fault. `bytes-05` is the same arm (a `\xff\xfe` literal line). The candidate's own
docstring states the refusal, so this is a design choice the frozen set contradicts; the L1 must decide whether the
candidate answers these lines (GLib does) or the claim's bytes class is narrowed. Not fixed here (scope: counter only).

### 3.2 Surviving mutants on the frozen set (22; each is a find/replace the frozen cases do not distinguish)

`dirs-03-empty-element`, `dirs-04-data-home-empty`, `mode-05-cache-continue`, `fgets-01-chunk-find`,
`fgets-04-nul-skip`, `atoi-01-sign`, `atoi-02-whitespace`, `v1-01-weight-50`, `cs-01-prefix`, `glob-04-backslash`,
`glob-05-first-k`, `literal-02-fold-first`, `literal-03-fold-cs`, `trie-02-extra-order`, `pass-05-full-unfolded`,
`cache-01-fnmatch-threshold`, `cache-05-cs-bit-fnmatch`, `cache-07-fnmatch-unfolded`, `cache-08-literal-order`,
`dupe-01-max-weight`, `dupe-02-swap-from-end`, `guess-06-empty-name`.

Some are probably equivalent on the frozen set (e.g. `dirs-03` only changes a lookup of an absolute `/mime/` that no
case creates). The mutation seat (R94MMutC1) and the case seat own the split between "equivalent" and "test gap";
this counter reports them as survivors, which is what (iv) requires.

## 4. Verification run (DRAFT; my scratch `/fast/scratch/hyaku/mado-r94/R94MExecCounterC1`)

Commands and exit codes:

- Oracle compile: `gcc -O1 -o $S/oracle <oracle.c> $(pkg-config --cflags --libs gio-2.0)` rc 0; binary sha256 above.
- Candidate `--selftest`: rc 0, `MADO_MIMEGLOB_SELFTEST: checks=15 failed=0`.
- Counter with a wrong pin: rc 2, `SETUP_ERROR … cases sha256 … != pinned deadbeef`.
- Counter, the case file's fixture path was wrong during development: rc 2, `SETUP_ERROR oracle_drift=…` (the drift
  check fired as designed); fixed, rerun rc 3.
- Counter, a one-mutant file (`UNKNOWN` `application/octet-stream` → `text/plain`): rc 3, `mutant m1-unknown killed`.
- Counter, a comment-only mutant (`import os` → `import os  # x`): rc 3, `survived`, `killed=0`.
- Counter, a tool that always exits 3: rc 3, both dev cases `CRASH`, `answered=0 correct=0`.
- Counter, tool absent at `HEAD`: rc 2, `SETUP_ERROR … absent at HEAD`.
- Frozen-set DRAFT crash on a directory-marker key (`s1/mime/mime.cache/`): rc 1 with a traceback in the oracle
  leg; fixed by materialising keys ending in `/` as directories; the rerun is 3.1 above (rc 3).
- Counter with the final code and the current bytes: rc 3, the verdict in section 3.

## 5. Open items for the L1 (not closed by this seat)

- Candidate defect 3.1: the candidate refuses invalid-UTF-8 glob lines; the frozen labels answer them. The C1
  claim cannot reach TARGET_MET with this candidate and these labels (either the candidate or the claim changes).
- Survivors 3.2: the frozen mutant/case set kills 35 of 57 on this candidate; (iv) needs all 57 to be killed or the
  survivors declared equivalent (the counter has no equivalence list; the mutant file carries
  `equivalent_not_counted`, 4 entries, which the counter does not read).
- The class conjunct (2.3) and control files (2.2) are weaker than the critic's C1-F1/C1-F4 repairs.
- A frozen cases file may still move before freeze (2.7); pin at freeze.
