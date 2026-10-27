# ExecOracleV2 — C1 judge harness for warm-cache cases (round 48 w1)

Seat: `ExecOracleV2` (leaf). Lane `mado-shokunin`, base `579f694b45…` . Everything below is measured on
this host on 2026-10-26; nothing is predicted. Python 3.14.8, bubblewrap 0.13.1, GNU bash 5.3.20.

Deliverables (all under `.ufo/waves/round-48/w1/ExecOracleV2/`):

| file | sha256 | what |
|---|---|---|
| `oracle2.py` (774 lines) | `8158a7bfa4ec8f0ca822ce536f6df7292919687d5b0b74d91470058d4fa5de23` | the harness |
| `fixtures-v2.json` (44 cases, `expect` filled by the pin) | `e8ccd94bbc3f5fad4ef4d86758d082cefd77e63b00ae5d928864ace9dd5f7537` | warm-cache fixture set |
| `make-fixtures.py` | `d51e6c38e03059cc8d204cfc136d6d735e4052af271556b8899571ccf0e4e2b8` | author of the above (no `expect` typed by hand) |
| `receipts/` | see §8 | run output |

The harness resolves its lane by walking up for `tools/mado-terminal.py`, defaults the pin to
`.ufo/waves/round-47/fetch/xdg-terminal-exec` (sha256 checked on load) and the tool to
`tools/mado-terminal.py`, and refuses a `--work` inside the lane. It is a drop-in for
`quality/counters/` if `fixtures-v2.json` is installed beside it.

## 1. What it does per case

Three (or four) fresh trees per case, **one run per tree**:

```
prepare(root):  materialize files+exec stubs → pin mtimes → (prime | install literal cache)
                → read cache_before → apply `after` (files/exec_add/exec_remove) → re-pin mtimes
                → read cache_after
o  clean resolver run  → authoritative rc+stdout
d  same run with XTE_DEBUG=1 → the cache verdict (and must not change rc+stdout)
t  the scored run: `python3 -I /oracle/tool.py print ARGS` (or `explain`), under strace
c  warm-diff cases only: the same tree with the cache file deleted → the COLD answer
```

`print` compares `(rc, stdout)` after replacing each tree's root with `$ROOT`; `explain` compares the
`MADO_TERM:` fields `selected`, `path`, `verdict`, `cache`. The verdict is never inferred by me: it is
read off the resolver's own debug channel (`D: cache is actual` :275, `cache is out-of-date` :287,
`invalid cache data` :291, `no cache data` :295, `reached cache line limit` :240), and `disabled` only
from `XTE_CACHE_ENABLED` through the pin's own `check_bool` True-set (:1172, :1179).

Extra invariants the judge enforces per case: determinism over `--reps`; `XTE_DEBUG` neutrality;
`cache_before` identical in all trees; `hash_differs` across roots; `want_cache` (author-declared)
must equal the resolver's own verdict; a warm-diff case's warm answer must differ from its cold
answer; a warm *hit* must leave the cache byte-identical (pin:1457 is guarded by `XTE__CACHE_USED`);
no strace trips on tool runs.

## 2. The background save: which wait works (measured, `receipts/prime-probe.txt`)

`receipts/prime-probe.txt` — same case, 3 runs per strategy:

```
PRIME plain  run=1..3 present=False terminated=False bytes=0
PRIME wait   run=1..3 present=False terminated=False bytes=0
PRIME poll   run=1..3 present=True  terminated=True  bytes=180
PRIME case=hit-baseline plain=[(False,False)] poll=[(True,True)] wait=[(False,False)]
```

* **plain** `bwrap … /oracle/xdg-terminal-exec --print-cmd` → **no cache**. bwrap is PID 1 of the new
  pid namespace; when the main process exits the namespace dies and the fork is destroyed before it
  writes. A cold run in this sandbox therefore never leaves a cache.
* **`sh -c '<pin> …; wait'`** → **no cache**. `wait` reaps only the wrapper's own children; the writer
  is a child of the *pin's* shell and is reparented to bwrap's init, not to the wrapper.
* **poll** → cache present, terminator intact, 180 bytes, 3/3. `WAIT_CACHE` (oracle2.py:59-67) is
  bash-builtin-only (`[ -s ]`, `while IFS= read -r`), because the sandbox allowlist has no `sleep`,
  `cat` or `test`; it is bounded at 20000 iterations (≈0.14 s worst case, measured), breaks early on a
  non-zero pin status, and exits with the pin's own status.

So the harness never runs a scored case in a tree that had a cold run. That is also why `cache_post`
is only asserted for verdicts where the resolver cannot fork a save at all: for cold runs whether the
write lands before teardown is a race (it flipped between reps in an early version — see §7).

## 3. Two roots: the hash is path-dependent, so each tree is primed at its own root

`gen_hash` hashes `"4\n$XDG_CURRENT_DESKTOP\n"` plus `LANG=C ls -LRl ${XTE__CONFIGS}:${XTE__APPLICATIONS_DIRS}`
(pin:200), whose **headers are absolute paths**. Proof, `receipts/hash-probe.txt` (32 primed cases,
identical content at `/…/a/r` and `/…/bbbbbbbb/deep/r`):

```
PROBE rows=32 bad=0        every row: hashes_differ=True shape_equal=True lines=[12,12]
PROBE ex-hit    ff0c4a86198f173fd7be9d1e1a1e2720 07329e6b4369b8bccdd26282a034eae3
```

i.e. the two caches differ **only** in line 1 (the hash) and are byte-equal once the root is replaced
with `$ROOT` (`cache_shape` elides line 1; that elision is also what makes `expect` root-independent
and stable across runs).

A cache primed at A is therefore useless at B, and rewriting the path inside it does not repair it —
line 1 is a digest of the original listing, not text to substitute. `receipts/transplant-probe.txt`:

```
TRANSPLANT verbatim         cache=stale  rc=0 stdout='foot\n'
TRANSPLANT root-rewritten   cache=stale  rc=0 stdout='foot\n'
TRANSPLANT primed-here      cache=hit    rc=0 stdout='foot\n'
```

**Decision:** prime every tree independently at its own root (no cache rewriting anywhere). The
scored comparison then happens between two trees that each hold a *native* cache, which is exactly
the state a warm resolver is in. 32 of the 44 cases are primed and each is checked against its own
declared `want_cache`: 20 `hit`, 7 `stale`, 3 `disabled`, 2 `absent` after a prime that never wrote
a file (one of them `--print-id` priming, which cannot write). All 32 match.

## 4. Fixture schema v2 (as implemented — the L1 freezes the final form)

Round-47 fields (`id`, `class`, `env` with `$ROOT`, `files`, `exec`, `args`, `expect`) plus:

| field | meaning |
|---|---|
| `mtime` | epoch seconds pinned on every file **and directory** below the root (not `.rw`), deepest first. Makes `ls -lR` dates — and therefore the hash — a function of the fixture. Applied before priming. |
| `prime` | `{"args": [...]}`: a cold run before the scored run, run under `WAIT_CACHE`; the harness waits for the terminator, then reads the result. `prime: {"args": ["--print-id"]}` legitimately produces **no** cache (the run exits at the print bail-out pin:1369-1385, never reaching :1457). |
| `after` | `{"files": {"<path>": "<text>" or null}, "exec_add": [...], "exec_remove": [...], "env": {...}, "mtime": <epoch>}`. Applied after priming, `$ROOT` substituted in keys and values, `null` deletes; then mtimes are re-pinned (`after.mtime`, else `mtime`). `after.env` overlays the scored env (`null` unsets). |
| `cache` | literal cache text (`$ROOT` substituted), no priming — for malformed caches and for the `$HASH`-less states. Mutually exclusive with `prime`. |
| `want_cache` | author-declared expected verdict (`hit`/`stale`/`invalid`/`absent`/`disabled`/`null`); checked against the resolver's debug channel. This is the guard that stops a "warm-diff" case from silently decaying into a cold one. |
| `mode` | `print` (default) or `explain`. |
| `expect` | **always** produced by `oracle2.py --emit-expect` from the pinned script: `{rc, stdout, verdict, cache_before, cache_after}` with roots replaced by `$ROOT` and line 1 replaced by `$HASH`. Never typed. |

`env` semantics: defaults `HOME=<root>/home`, `PATH=<root>/bin:/oracle/bin`,
`XDG_CACHE_HOME=<root>/.rw/cache`, `LANG=C.UTF-8`; a case value overrides, `null` unsets (that is how
`ct-home-unset` models round-47 D1).

## 5. Determinism — 44 cases × 3 reps, and across invocations

`receipts/pin-control-3reps.txt` (control = the pin itself at the tool tree, so the comparison
machinery is judged alone):

```
ORACLE2-r48: cases=44 pass=44 fail=0 reps=3 control=pin
classes=contract:1/1,disabled:4/4,explain:5/5,hit:7/7,invalidated-desktop:1/1,invalidated-exec0:1/1,
invalidated-mtime:1/1,invalidated-name:3/3,invalidated-noprime:1/1,invalidated-size:1/1,
malformed:8/8,warm-diff:11/11
```

Two *independent* invocations of the whole set produce byte-identical observation JSONs
(`--json`, compared with `json.dumps(..., sort_keys=True)` → `True`), including every cache shape,
every verdict and every cold reference; and the `expect` block written by an earlier invocation is
still satisfied (`expect` drift check), which is the property the frozen counter needs.

## 6. Discrimination — the base tool, 29/44 (`receipts/tool-control.txt`)

The delivered tool models a cold cache only, so it should fail exactly the warm cases and nothing
else. It does, with a real divergence in each:

`receipts/warm-diff-table.txt` (warm answer vs the same tree with the cache removed):

```
wd-exec-same-size        cache=hit warm 'foot\n'                          cold 'kitty\n'
wd-list-same-size        cache=hit warm 'foot\n'                          cold 'fooz\n'
wd-tryexec-stub-gone     cache=hit warm 'foot\n'                          cold 'kitty\n'
wd-dir-arg-name          cache=hit warm '--working-directory=$ROOT/w'     cold '--working-directorx=$ROOT/w'
wd-title-arg-name        cache=hit warm '--title=T'                       cold '--titlx=T'
wd-appid-arg-name        cache=hit warm '--app-id=A'                      cold '--app-ix=A'
wd-execarg-name          cache=hit warm '-x echo hi'                      cold '-y echo hi'
wd-hold-arg-name         cache=hit warm '--hold -e echo'                  cold '--holx -e echo'
wd-mtime-blind-old-date  cache=hit warm 'foot\n'                          cold 'kitty\n'
wd-action-cmd            cache=hit warm 'foot new'                        cold 'foot neq'
wd-two-lists             cache=hit warm 'foot\n'                          cold 'fooz\n'
```

Tool control: `cases=44 pass=29 fail=15` — the 11 warm-diff cases above, `ex-hit`/`ex-stale`/`ex-invalid`
(its `MADO_TERM` says `cache=absent` where the resolver says hit/stale/invalid), and `ct-home-unset`
(tool rc 2 vs pin rc 1, empty stdout on both). The 7 `hit`, 8 `malformed`, 4 `disabled` and the
remaining `invalidated-*` cases pass, so the harness is not failing everything.

## 7. Findings the freeze needs

1. **`cache=disabled` cannot come from a `/disable_cache` directive on a readable cache.** The read
   happens at pin:1179, the directive is parsed from pin:1198 onward (`read_config_paths`), so a valid cache is applied
   before the directive is ever seen. `receipts/pin-control-3reps.txt` case `dis-directive-inert`
   (list edited from `#/disable_cach` to `/disable_cache`, same size, same mtime) → `cache=hit`.
   `dis-directive-cold` (no cache at all) → `cache=absent`. The only observable `disabled` is
   `XTE_CACHE_ENABLED` false in the environment, which short-circuits the read. The draft contract
   in `claims.md` ("disabled via XTE_CACHE_ENABLED **or** /disable_cache") should be narrowed to
   match: the directive suppresses the *save*, it does not disable the *read*.
2. **The hash covers metadata only, never content.** Same size and same displayed date ⇒ same hash:
   five fixtures edit `Exec=`, the preference list, `X-TerminalArgDir/Title/AppId/Exec/Hold` and a
   `[Desktop Action]` `Exec=` in place and keep `cache=hit`.
3. **Old-dated entries blind the date check.** For a file older than six months `ls -l` prints the
   year, so an mtime shift inside that year is invisible: `wd-mtime-blind-old-date` changes the mtime
   by one hour *and* the Exec, and the cache still hits. Only the year-level change
   (`inv-mtime-year`) invalidates. A counter that expects an mtime edit to invalidate must pin the
   date inside the `Mon dd HH:MM` window, which is clock-dependent and therefore expiring — my
   fixtures stay in the year regime on purpose and none of them expires.
4. **A cold run's background save is a race inside the sandbox** (it flipped `cache_after`/verdict
   between reps until I gave every run its own tree). Any counter that runs a case twice in one tree
   inherits that nondeterminism.
5. **Cache line limit is 50** (pin:223, :228). 49 payload lines + terminator = 50 → `invalid`
   (`mf-line-limit`). A terminator without a trailing newline is also `invalid` (the `while read`
   loop drops the unterminated last line, pin:228-254) — `mf-terminator-no-newline`. `\r` after the
   terminator → `invalid` too. All three are distinguished from `stale` only by the debug line,
   which is why the harness reads the verdict there instead of re-deriving it.
6. **HOME unset** (`ct-home-unset`, `XDG_CACHE_HOME` unset as well): pin rc 1, empty stdout; the
   delivered tool answers rc 2. Round-47 D1 is now an executed predicate, not a note.

## 8. Receipts and the exact sandbox argv

All under `.ufo/waves/round-48/w1/ExecOracleV2/receipts/`:

| file | sha256 |
|---|---|
| `prime-probe.txt` | `3777705888bbee28b3d544c33e859a779cde54401fcd1632c0f3313a52d25ddd` |
| `hash-probe.txt` | `7065b8aedbb4c95675e6bb8bb844e7807adec264b8416930d999f4a9b74d42c1` |
| `transplant-probe.txt` | `18de54b0e03acf429531a276cf12538c5c5a87c3de9cee59a7c54cc0a85ab840` |
| `pin-control-3reps.txt` | `8ddab15a160c835039d36f40b2facaa8fa8e7127e50b19e3f40ace9c0931d949` |
| `pin-observations.json` | `3656687686effbe9700e4e88656f374f74f0a89b3ecd9f208bd10d1eaa15eb60` |
| `tool-control.txt` | `1eb431caae5e7f89f7ff0002d8c3e184b551e4c3bd13d9a24b69ad6cdf52dd36` |
| `tool-observations.json` | `a11a4dd4c44945229ff27741f4679394932c57d6d3007ddcd11ebd10a7919038` |
| `warm-diff-table.txt` | `5d10d61525cc3faec159fe7abcd6699d8e0c69f3d596a3f0bc06144e208b4013` |
| `argv.txt` | `a203956253e96880261dd47df2eb56541eec381d550d1a213978f09d9e2a6740` |
| `cross-invocation.txt` | `46a3c3fc9d4ffe76615c4f04eb46c8f6f184445ee5ae275fc25feb3217d382cb` |

Reproduced with (work dir outside the lane; every receipt is this exact command):

```
python3 oracle2.py --work $W --control pin  --reps 3 --fixtures fixtures-v2.json --json $W/pin.json  > receipts/pin-control-3reps.txt
python3 oracle2.py --work $W --control tool --reps 2 --fixtures fixtures-v2.json --json $W/tool.json > receipts/tool-control.txt
python3 oracle2.py --work $W --prime-probe       --fixtures fixtures-v2.json > receipts/prime-probe.txt
python3 oracle2.py --work $W --hash-probe        --fixtures fixtures-v2.json > receipts/hash-probe.txt
python3 oracle2.py --work $W --transplant-probe  --fixtures fixtures-v2.json > receipts/transplant-probe.txt
python3 oracle2.py --work $W --show-argv hit-baseline --fixtures fixtures-v2.json > receipts/argv.txt
python3 oracle2.py --work $W --control pin --emit-expect fixtures-v2.json      # rewrites expect
```

`receipts/argv.txt` (`oracle2.py --show-argv hit-baseline`) is the literal argv, unchanged from the
round-47 clause-i allowlist except the wrapper prefix:

```
bwrap --unshare-all --die-with-parent --new-session --clearenv
  --ro-bind /usr/lib /usr/lib --symlink usr/lib /lib --symlink usr/lib /lib64
  --ro-bind /usr/bin/bash /bin/sh --ro-bind /usr/bin/bash /bin/bash
  --ro-bind <work>/bin-XXXX /oracle/bin
  --dev /dev --proc /proc --tmpfs /tmp
  --ro-bind <root> <root> --bind <root>/.rw <root>/.rw
  [tool: --ro-bind /usr/bin/python3.14 /usr/bin/python3
         --ro-bind <lane>/tools/mado-terminal.py /oracle/tool.py]
  [pin:  --ro-bind <work>/pin-XXXX/xdg-terminal-exec /oracle/xdg-terminal-exec]
  --chdir <root>
  --setenv … (sorted env: HOME, LANG, PATH, XDG_*, …)
  tool: /usr/bin/python3 -I /oracle/tool.py print …
  prime: /bin/sh -c '<WAIT_CACHE>' prime /oracle/xdg-terminal-exec …
  scored pin: /oracle/xdg-terminal-exec …
```

Tool runs are additionally wrapped in
`strace -f -qq -e trace=execve,execveat,socket,socketpair,connect -e signal=none -o <outside the sandbox>`
and any event after the sandboxed python3 execve fails the case (0 trips in every run here).

## 9. Risks / open items (for the L1, not acted on)

* `cache=` semantics: I chose "the state at the read"; a `/disable_cache` case must therefore be
  scored with `cache=absent|stale|invalid|hit`, never `disabled` (§7.1). If the freeze wants
  `/disable_cache` to read as `disabled`, the harness must change, not the fixture.
* `explain --observed` (round-47 clause x's second half) is not exercised on warm trees here; only
  the primary `explain` fields are. Adding it is a small change but is outside the assigned target.
* The `hit-*` fixtures pin `mtime=1700000000` / `1735000000`, both in the `ls` year regime, so no
  fixture expires; a counter that wants the `HH:MM` regime must accept a clock-dependent hash.
* `fixtures-v2.json` is authored by `make-fixtures.py`; if the L1 freezes the JSON, keep the author
  beside it, or the intent of `want_cache` is lost on the next edit.

## 10. Cleanliness

Writes are confined to `.ufo/waves/round-48/w1/ExecOracleV2/` and this report; no tracked file was
edited, no git/jj mutation, no compositor/pacman action, no terminal launched, the host's
`~/.cache/xdg-terminal-exec` untouched (every run had `XDG_CACHE_HOME` inside the seat scratch).
Scratch `/fast/scratch/hyaku/mado-r48/ExecOracleV2/` (fixture trees only, well under 2 GB) is deleted
at the end of the wave; nothing citable lives there. No tool was installed or upgraded.
