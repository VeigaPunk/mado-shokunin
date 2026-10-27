# ExecCounterC1 — C1 counter draft `quality/counters/c1-r49-keysym.py`

Status: **complete** (draft delivered at the seat dir; the L1 installs it; nothing tracked was edited).
Seat dir: `.ufo/waves/round-49/w1/ExecCounterC1/`. Scratch `/fast/scratch/hyaku/mado-r49/ExecCounterC1` removed at exit.

Deliverables in the seat dir:

| file | sha256 | role |
|---|---|---|
| `c1-r49-keysym.py` | `1a7fcc21b7508db46f6a22325de84f6ed115fd81b63607a364c1c4addd27b4fe` (732 lines) | the counter (PRED-C1-r49) |
| `c1-r49-fixtures.json` | `81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393` | the pinned fixture file, adopted from w1/ExecFixtures `fixtures-counter.json` (byte-identical) |
| `counter-selftest.py` | `5e4c247226ed305d2042d3436834f995ce77cdd5289691a893759166d8d14c80` | scratch-only positive-path harness (judge-as-tool) proving the declaration arithmetic |
| `scratch-refB-tool.py` | `81cd3b19e2d1bcce826a43b56b025af4b84c34eee1d9cb7f2fb357a775f62fff` | the exact tool blob scored in §4.5: ExecRefKeysymB's `keysym_ref.py` (bytes with sha256 `37f25259…`, as of 01:52) plus a 90-line contract CLI/selftest wrapper. **Not a deliverable, never install it.** |
| `receipts-*.txt` | — | every run quoted below |

## 1. What the counter scores

`TARGET_MET` iff all clauses hold on committed revision REV of `--repo`:

- **t** `tools/mado-keysym.py` is a regular blob (100644/100755) at REV; read with `git show REV:TOOL`, never the
  working tree (proved in §4.6).
- **s** tool self-checks at REV, inside the sandbox: `--selftest` exits 0 with last non-empty stdout line
  `MADO_KEYSYM_SELFTEST: N/N passed`, N ≥ 25 and N == N; and the two documented refusals exit 2 without a
  `=== Direct access ===` table — `how-to-type --keymap FILE --keysym ARG` (no `--disable-compose`) and
  `how-to-type --keymap FILE --disable-compose` (no `--keysym`).
- **f** every fixture: the counter compiles its keymap with the pinned `xkbcli-compile-keymap` in a clean env
  (`env -i` equivalent: `PATH=/usr/bin`, `HOME`/`XDG_CONFIG_HOME` under `--work`, `LC_ALL=C`), runs the pinned
  `how-to-type --keymap=FILE --disable-compose --keysym ARG`, and requires the tool's exit status **and stdout
  bytes** to equal the judge's. A fixture whose judge result no longer matches its recorded `(rc, sha256(stdout))`
  is a SETUP error (drift), not a tool failure. stderr is never compared.
- **g** `GEN = 60` nonce cases: RMLVO drawn from a frozen, pre-validated pool (61 layout/variant pairs and 15 option
  strings, all compiled successfully when the counter was written) × ARG drawn from a pool of names, numeric
  forms, absent-but-valid names and invalid names. Same equality as f, judge computed at count time.
- **r** every traced tool run (selftest, refusals, fixtures, generated): after the sandboxed `python3` execve, any
  further `execve/execveat/socket/socketpair/connect/fork/vfork/clone/clone3`, or any write attempt
  (`open*` with `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND`, or `creat/mkdir(at)/rmdir/unlink(at)/rename(at/at2)/
  link(at)/symlink(at)/truncate/ftruncate/mknod(at)`), is a trip. The single exception is clause s's `--selftest`:
  writes whose every absolute quoted path is under `/tmp` are excused (the tool's documented `$TMPDIR` case
  scratch); a write anywhere else still trips. Both directions measured (§4.2, §4.3).
- **i** the tool runs in `bwrap --unshare-all --die-with-parent --new-session --clearenv` with a fresh root whose
  mounts are exactly: a fresh `/`, `/usr`, `/usr/lib` tmpfs; the stdlib tree read-only; an empty tmpfs over its
  `site-packages`; the interpreter (`ldd python3`'s realpath) at `/usr/bin/python3`; the shared-library closure
  (`ldd` over the interpreter and every `lib-dynload/*.so`, 42 files here: libz, libssl, libcrypto, libffi,
  libsqlite3, liblzma, …), each bound at the SONAME path ldd printed and at its realpath; `/lib`, `/lib64` →
  `usr/lib`; the pinned header
  `/usr/include/xkbcommon/xkbcommon-keysyms.h` read-only (`HEADER_SHA256`); the case keymap at
  `/fixture/keymap.xkb` read-only; the tool blob at `/oracle/tool.py` read-only; `/dev`; a fresh `/proc`; a fresh
  `/tmp` tmpfs. No host `/usr/lib` beyond that closure → **libxkbcommon and the xkbcli binaries are not present in
  the sandbox**, so a tool cannot ctypes-load or exec the judge. Env inside: `PATH=/usr/bin LC_ALL=C
  HOME=/nonexistent TMPDIR=/tmp`. No network (`--unshare-all`).

Final line, exactly as frozen in the counter: `PRED-C1-r49: fixtures=K/F generated=G/N selftest=<ok|fail>
readonly=<ok|fail> tool=<present|absent> verdict=TARGET_MET|TARGET_MISSED`; exit 0 met, 1 missed, 2 setup.
CLI: `--repo --rev --work --nonce` (nonce default random and printed).

SentScratch is enforced before anything runs: `--work` under `/tmp` or `/var/tmp`, a `TMPDIR` under `/tmp`, or a
`--work` inside the repo/lane/lane-parent is a SETUP error, exit 2 (`receipts-setup-refusals.txt`).

## 2. Fixtures and generator

- **Installed fixture file** (authoritative, pinned): 633 cases, 17 classes (`ABSENT BIND CASE DEAD DIGITS
  FUNCTION HOST INVALID KEYPAD LETTERS MODIFIER MULTI NUMERIC OPTIONS PUNCT VARIANT XF86`), 27 distinct RMLVO
  keymaps, 581 rc-0 / 52 rc-2 (invalid/case-negative) cases, 633 unique ids. Schema is exactly the counter's
  six keys `{id,class,rmlvo,arg,rc,sha256}`; `check_fixture()` accepts all 633.
- My own embedded set (57 cases) remains as the fallback when `SHA256_FIXTURES` is emptied; its 8 overlapping
  cases agree byte-for-byte with ExecFixtures' digests (slash `3d895204…`, Return `9697ab0c…`, dead_acute
  `db686887…`, ISO_Level3_Shift `b181628d…`, `0x2f`/`47` `3d895204…`, XF86AudioMute `a815c2db…`, Escape
  `d0cf7e53…`).
- **Drift check at count time**: all 633 recorded `(rc, sha256)` were re-derived from the pinned judge on this host
  with no drift (`receipts-selftest-sim.txt`, 633/633; independent manual spot checks of `r49-c1-0001/0200/0400/
  0600` agree).
- The generator pools are frozen literals in the counter; a generated RMLVO that stops compiling (an
  xkeyboard-config change would be the cause) is a SETUP error, not a silent skip.

## 3. Judge and sandbox, exactly

Judge argv (counter side, outside the sandbox):

```
/usr/lib/xkbcommon/xkbcli-compile-keymap --rules evdev --model pc105 \
    [--layout L] [--variant V] [--options O]           # flags only for non-None RMLVO fields
/usr/lib/xkbcommon/xkbcli-how-to-type --keymap=<compiled file> --disable-compose --keysym <ARG>
```

with `PATH=/usr/bin HOME=<work>/judge-home XDG_CONFIG_HOME=<work>/judge-cfg LC_ALL=C`, `cwd=<work>`, no inherited
environment, both binaries' sha256 verified first (`f6c0b122…` how-to-type, `43b924f6…` compile-keymap,
`13023369…` header). Tool argv (inside the sandbox):

```
/usr/bin/python3 -I /oracle/tool.py how-to-type --keymap /fixture/keymap.xkb --disable-compose --keysym <ARG>
```

wrapped by `strace -f -qq -e trace=<TRACE_SET> -e signal=none -o <work>/trace-*`.

## 4. Evidence (every line from a run; receipts in the seat dir)

### 4.1 Base `03e4ae76…` must MISS

`receipts-base.txt`:

```
PRED-C1-r49 clause=meta rev=03e4ae76aff7a4be59cb69970dd553baa319695a nonce=49 … fixtures=633
PRED-C1-r49 clause=t tool=absent
PRED-C1-r49: fixtures=0/633 generated=0/60 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED
rc=1
```

### 4.2 Read-only tripwires (stub revisions in a scratch clone, fixture identity)

`receipts-trip-write.txt` — tool writes `/tmp/probe`:
`clause=r trips=695 write:openat(AT_FDCWD, "/tmp/probe", O_WRONLY|O_CREAT|O_TRUNC|O_CL…)`, verdict MISSED.
`receipts-trip-exec.txt` — tool calls `subprocess.run(["/usr/bin/true"])`: `trips=1392` led by
`clone3({flags=CLONE_VM|CLONE_VFORK|…` and `execve("/usr/bin/true", …)`.
`receipts-trip-socket.txt` — `socket(AF_INET, SOCK_STREAM…)`: `trips=696`.
`receipts-trip-self.txt` — a tool that prints only the selftest line: `clause=s … ok`, refusals ok, `trips=0`,
fixtures 0/633, MISSED (clause s alone cannot pass).

### 4.3 The selftest write rule, both ways

`receipts-trip-tmp2.txt` — selftest-only write under `/tmp` (`tempfile.mkdtemp(dir="/tmp")`): `clause=s selftest=…
ok`, `clause=r trips=0` (excused).
`receipts-trip-etc2.txt` — selftest-only write to `/etc/keysym-probe` (EROFS): `trips=1 write:openat(AT_FDCWD,
"/etc/keysym-probe", O_WRONLY|O_CREAT|O_TR…)`, `readonly=fail`.

### 4.4 Do-nothing baseline

`receipts-stub-always2.txt` — a tool that exits 2 always but has an honest selftest line: `fixtures=52/633
generated=7/60 selftest=ok readonly=ok tool=present verdict=TARGET_MISSED`. The 52 are exactly the rc-2 fixtures
and the 7 are the generated invalid-arg cases: a stub collects only the error-path cases.

### 4.5 Positive path

Two independent positive checks:

1. `receipts-selftest-sim.txt` (harness `counter-selftest.py`, scratch-only: replaces the sandbox Box with one
   that returns the judge's own answer, so the declaration arithmetic is exercised): `fixtures=633/633
   generated=60/60 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, rc 0.
2. **A real implementation passes end to end.** `receipts-refB.txt`: ExecRefKeysymB's core module
   (`keysym_ref.py`, sha256 `37f25259b3283425f62f8474276c4ca181b63c521a7697739cbbe6706e19e2fc` when embedded; the
   seat has since edited it to `dc70c000…`) was wrapped in the contract CLI and scored from a scratch clone
   (commit `56050c623dae3a485ab6158d8f67ded6adff5c72`, `git rev-parse --show-toplevel` verified, tool read with
   `git show`):

```
PRED-C1-r49 clause=s selftest rc=0 last='MADO_KEYSYM_SELFTEST: 32/32 passed' ok
PRED-C1-r49 clause=s refusals=ok
PRED-C1-r49 clause=f fixtures=633/633
PRED-C1-r49 clause=g generated=60/60
PRED-C1-r49 clause=r trips=0
PRED-C1-r49: fixtures=633/633 generated=60/60 selftest=ok readonly=ok tool=present verdict=TARGET_MET
rc=0
```

   The exact scored blob is kept at the seat dir as `scratch-refB-tool.py` (sha `81cd3b19…`) so the receipt is
   replayable; the wrapper is mine, the algorithm is B's, and the wrapper must never be installed.
3. **Reference A's frozen draft passes unchanged.** `receipts-refA.txt` — ExecRefKeysymA's `mado-keysym.py`
   (sha256 `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265`, 1999 lines, the seat's frozen
   bytes) committed at `tools/mado-keysym.py` in the scratch clone (commit
   `c28346289aaab49adf759f3fcde557014d1cc233`, toplevel verified, read with `git show`):

```
PRED-C1-r49 clause=s selftest rc=0 last='MADO_KEYSYM_SELFTEST: 38/38 passed' ok
PRED-C1-r49 clause=s refusals=ok
PRED-C1-r49 clause=f fixtures=633/633
PRED-C1-r49 clause=g generated=60/60
PRED-C1-r49 clause=r trips=0
PRED-C1-r49: fixtures=633/633 generated=60/60 selftest=ok readonly=ok tool=present verdict=TARGET_MET
rc=0
```

   A second nonce (`20261027`) is receipted in `receipts-refA-nonce2.txt`.
   Control tools (cheats) are ScExecControlsC1's to score.

### 4.6 The tool is read from REV, never the working tree

`receipts-gitread.txt`: working tree overwritten with a stub printing `MADO_KEYSYM_SELFTEST: 99/99 passed`, counter
run at commit `1eb2becf…` (which carries 25/25): `clause=s selftest rc=0 last='MADO_KEYSYM_SELFTEST: 25/25 passed'
ok` — the committed bytes scored, the working tree ignored. Same receipt: the default-nonce path
(`nonce=1791969749`, printed) with the tool absent exits 1.

### 4.7 SentScratch and hidden-path refusals

`receipts-setup-refusals.txt`: `--work /tmp/…` → `SETUP work dir under /tmp (SentScratch…)` rc 2;
`TMPDIR=/tmp` → `SETUP TMPDIR is under /tmp …` rc 2; `--work` inside the lane → `SETUP work dir inside a hidden
path …` rc 2.

### 4.8 Cost

693 sandboxed runs (633 fixtures + 60 generated) took ~20 s wall with a trivial stub, 98 s with reference B's core
(2,338-line tool blob) and 160 s with reference A's draft (1,999 lines) — full bwrap + strace per run; the
judge-side compile is cached per RMLVO (27 keymaps for 633 fixtures).

### 4.9 Mutation finding (MutCounterC1Draft) — fixed

The first draft bound only `ldd python3`'s libraries, so stdlib extension modules whose shared objects carry
their own dependencies failed inside the sandbox (`base64` → `binascii` → `libz.so.1`; `_ssl` → `libssl/libcrypto`).
A conforming tool that imports `base64` or `zlib` would have been a false MISSED. Fix: the closure is now `ldd`
over the interpreter **and every `lib-dynload/*.so`**, each library bound at the SONAME path ldd printed and at
its realpath (bwrap mounts files, not the symlink target's directory tree). `Box.python_libs()` raises Setup if
that closure ever names libxkbcommon or an xkbcli binary, so the no-judge property is asserted, not assumed.
`receipts-stdlib-imports.txt`: `closure=42 xkbcommon=[]`, a tool importing base64/zlib/ssl/hashlib/json/ctypes/
sqlite3/lzma/bz2/readline/curses/uuid/pyexpat/… prints `imports ok`, rc 0, trips 0. Re-run after the fix:
`receipts-stub-always2.txt` `libs=42 … fixtures=52/633 … readonly=ok verdict=TARGET_MISSED` and the MET
self-test unchanged (`633/633`, `60/60`). Counter sha moved to `1a7fcc21…`; the mutant's cited `3a9e46…` is not
this file.

## 5. What this attacks, and what it deliberately does not

- **Attacks** (each with the clause that sees it): a tool that only knows the first match (f/g multi-row cases —
  e.g. `HOST-slash` has 5 rows on br+compose:caps); a tool that ignores LevelThree/Lock masks (the row text is
  compared byte-for-byte, including `[ Lock Mod5 LevelThree ]`); a tool with case-insensitive keysym lookup
  (`CASE-lower`/`CASE-SLASH` are rc 2); a tool that mishandles numeric values (`0x2f`, `47`, `0xff0d`, `0x1000e9`
  Unicode names); a tool that shells out to xkbcli/how-to-type (r, plus the binaries are not in the sandbox); a
  tool that fakes by writing a cache (r); a tool that special-cases the fixture file (f passes, g does not —
  the 60 nonce cases share no arg/RMLVO with the frozen file by construction of the pools).
- **Does not score**: the tool's usage text / stderr (how-to-type's own usage names argv[0]); `--keysym`
  arguments starting with `-`; repeated/reordered flags; raw XKB sources with includes, `--keymap -` (stdin) and
  `--format 1` (outside the declared contract). Declared residuals also include `/proc/1/cmdline` exposing the
  bwrap argv. The runtime closure is the interpreter's plus every stdlib extension's `ldd` dependency set, so any
  Python 3 stdlib module imports (verified, §4.9); third-party site-packages are shadowed by an empty tmpfs, and
  libxkbcommon/xkbcli are never present (asserted at setup).
- The header is *allowed* read-only, not required: a tool may embed a generated table instead. Whether the header
  alone suffices for canonical names/aliases is ExecKeysymNames' finding; the counter pins the header's bytes so
  either implementation is judged against the same data source.
- The fixture digest file is pinned by sha256; if the L1 installs a different file, the counter is a SETUP error
  until the constant is updated at freeze — deliberately, so a w2 mutant cannot quietly swap fixtures.

## 6. Freeze notes for the L1

1. Install `c1-r49-keysym.py` at `quality/counters/c1-r49-keysym.py` and `c1-r49-fixtures.json` (sha
   `81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393`) at `quality/counters/c1-r49-fixtures.json`;
   `SHA256_FIXTURES` is already set to that digest. To use a different frozen set, replace both the file and the
   constant (the embedded 57-case fallback is only used if the constant is emptied).
2. Frozen numbers: `SELFTEST_MIN=25`, `GEN=60`, the 633 fixture cases, the 61-pair/15-option/95-name generator
   pools. Changing any of them is a freeze edit.
3. Requisites: `bwrap`, `strace`, `ldd`, `git`; the three pinned binaries/headers and the host python3 (3.14.8)
   whose `ldd` closure — interpreter plus every `lib-dynload/*.so` — is derived at run time (42 libraries here).
   A host python upgrade re-derives; a python without shared `libpython` is a setup error, and so is a closure
   that names libxkbcommon/xkbcli.
4. `--work` must be on a scratch filesystem (not `/tmp`), outside the lane; runtime ~20 s for the full count on
   this host.

## 7. Safety

Read-only git only; no index/commit/push in the lane. Nothing written outside the seat dir and
`/fast/scratch/hyaku/mado-r49/ExecCounterC1` (removed). Every sandbox run had `HOME`/`XDG_*` under `--work`; the
judge ran `env -i`-equivalent, so no host xkb include path was consulted. No compositor/input/terminal action, no
package transaction, no host config or cache touched. Session material: none captured (no device names, no
windows, no home listing; receipts contain only keysym names, RMLVO names and `$ROOT`-free judge text).

## 8. Reference drafts

Both C1 reference drafts were scored in scratch clones (`git rev-parse --show-toplevel` verified, tool read with
`git show REV:tools/mado-keysym.py`, pinned judge, nonce 49):

- **ExecRefKeysymA** (frozen `mado-keysym.py`, sha `dcc13cce…`, 1999 lines), clone commit `c2834628…`:
  `fixtures=633/633 generated=60/60 selftest=ok readonly=ok verdict=TARGET_MET`, rc 0
  (`receipts-refA.txt`; second nonce `20261027` in `receipts-refA-nonce2.txt`).
- **ExecRefKeysymB** core (`keysym_ref.py`, embedded bytes sha `37f25259…`) behind the contract CLI:
  `fixtures=633/633 generated=60/60 selftest=ok readonly=ok verdict=TARGET_MET`, rc 0 (`receipts-refB.txt`).

Re-score any tool the same way:

```
python3 quality/counters/c1-r49-keysym.py --repo <clone> --rev <commit> --work <scratch> --nonce 49
```

with the tool committed at `tools/mado-keysym.py` in `<clone>`.
