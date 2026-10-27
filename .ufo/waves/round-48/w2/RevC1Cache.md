# w2 / RevC1Cache — C1 cache-contract falsification against the v0.14.3 pin

Seat: `RevC1Cache` (leaf). Lane `mado-shokunin`, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Attacked: `PRED-C1-r48` (`quality/counters/c1-r48-terminal-cache.py`), its 204 warm fixtures, and the
candidate tool `tools/mado-terminal.py` (`.ufo/waves/round-48/l1-draft/mado-terminal.py`).
Pin: `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256 `89f2be9a…3127ac` = `/usr/bin/xdg-terminal-exec`
(both hashed this session). Judge is the pin; nothing here was judged by an L1 reference.

## Verdict

* **No live miss in the frozen tool on the cache path.** The frozen tool agrees with the pin on every case I
  built (24 host cases) and on **204/204** fixtures in an independent bwrap-free replay of clause `w`
  (stdout/rc), its recorded `state` (204/204), its recorded `cold` twin (204/204), its class premise
  (204/204), its `expect` (204/204) and clause `x`'s explain fields (204/204). Its hermetic selftest is 69/69.
* **Two coverage holes in the frozen instrument** (a wrong tool would still score `TARGET_MET`):
  1. `F1` — no fixture, no nonce warm case and no selftest case ever reads a **hash-valid cache whose command
     section spans more than one line**, so the LF reconstruction at `x:248` is unscored; the pin reaches it
     from an ordinary desktop entry. Mutant `joinless` (drops the LF join) passes selftest 69/69 and every
     clause-`w`/`x` check on the frozen set (204/204), yet mispredicts the resolver.
  2. `F2` — no fixture makes the cache file **unreadable**, so the pin's `x:217`/`x:258` redirect-failure path
     (`invalid cache data`, cold answer, rc 0) is unscored; mutant `unreadable_absent` (state `absent`
     instead of `invalid`) passes selftest 69/69 and 204/204 on the frozen set.
* **One corner that is untested but unobservable** (`F3`): `XTE_CACHE_ENABLED=""` (empty string). It differs
  from a bad value only in the *filesystem* side effect at the end of the run, never in stdout/rc/state, so
  no fixture can score it; no action required, recorded for completeness.
* **Controls that do bite** (measured, so the L1 can see which classes are genuinely pinned): the 50-line
  boundary (`line50_accept` mutant), the default cache path (`cache_home_only` mutant), the missing trailing
  newline, the early/junk terminator, empty fields, the cached action and the printer modes.

Per the wave rule nothing below narrows the predicate. `F1`/`F2` are pre-data holes — `registration.md`:
*"W2 may find a pre-data hole; only before data may L1 re-register as a new version and re-run the complete
control set."* The tool is right; the freeze cannot tell a wrong one from it. Fix them by **adding fixtures
before the data commit**, not by changing any expectation.

## Method and independence

1. Re-read the pin by hand: `gen_hash` `x:179-215`, `read_cache` `x:217-298` (line limit `x:239-242`,
   terminator `x:249-255`, `done <` `x:258`, hash + `command -v` gate `x:273-275`), `save_cache` `x:300-340`
   (newline guard `x:312-318`, write `x:332`), gate `x:1172-1200`, call `x:1455-1458`, `set -euf` `x:23`.
2. `host.py` (retained) builds one tree under my scratch (`$ROOT/bin/foot`, list, entry, `.rw/cache`), primes
   the cache with the pin itself (`--print-cmd`, poll for `\x1eEND_OF_EXEC_USEP`), then for each case writes
   the cache bytes, runs the **pin** (`/bin/sh <pin>`, `XTE_DEBUG=1`, host `/bin/sh` = bash 5.3.20) and the
   **tool** (`python3 -I <tool> print | explain`), each against the cache bytes the case specifies. The pin
   rewrites the cache when it misses, so the tool is always run **first** and the cache is restored before the
   pin runs; `cache_after` records the state the pin's background save left.
3. `replay.py` / `replay2.py` (retained) re-run the whole frozen fixture file with the counter's clause-`w`
   preparation semantics (files in `meta.files_order`, exec stubs, mtime pinning, literal cache or pin prime
   with waiter, `after` mutations incl. `cache_lines`/`cache_sub`/`cache_append`/`modes`), variant A only,
   comparing (rc, `$ROOT`-normalised stdout), the derived state (`cache is actual`/`out-of-date`/`invalid
   cache data`/`reached cache line limit`/`no cache data`/`paths:`), the cold twin, the class premise and
   clause `x`'s selected/path/cache/verdict. Difference from the counter: no bwrap, and `PATH=$ROOT/bin:
   /usr/bin:/bin` instead of `/oracle/bin` (the seven externals resolve identically; recorded as a residual).
4. Mutants are byte-identical copies of the frozen tool with one edit each (`mut/`), so a survivor isolates
   exactly one rule.

Instrument integrity checked: the draft fixture file equals the frozen one (both sha256
`4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa` = `SHA256_WARM`), the draft counter is
byte-identical to `quality/counters/c1-r48-terminal-cache.py`, and the candidate tool
(`sha256 1dfde36c…753a92`) equals `tools/mado-terminal.py` in the lane working tree at attack time.

## Required case classes: pin behaviour vs the frozen tool vs the freeze

`pin state` is derived from the pin's own `XTE_DEBUG` stderr with the counter's mapping. Full bytes:
`w2/RevC1Cache/ev/host-cases.json`.

| # | case | pin rc / state | pin stdout | frozen tool | freeze coverage | verdict |
|---|---|---|---|---|---|---|
| 1 | unreadable cache file (mode 000) | 0 / `invalid` | `foot\n` | rc 0, `cache=invalid` | **none** | agree; `F2` hole |
| 2 | cache path is a directory | 0 / `absent` | `foot\n` | rc 0, `cache=absent` | **none** | agree; `F2` class |
| 3 | unreadable cache dir (mode 000) | 0 / `absent` | `foot\n` | rc 0, `cache=absent` | **none** | agree |
| 4 | no trailing newline on the terminator line | 0 / `invalid` | `foot\n` | rc 0, `cache=invalid` | `M-18`, `v2-mf-12` | agree; pinned |
| 5 | terminator line 49 (hash **valid**) | 0 / `hit` | 39 `x` lines joined by LF | rc 0, identical bytes, `cache=hit` | `M-16` (zero hash → `stale` only) | agree; hit side of the boundary unscored (`F1`) |
| 6 | terminator line 50 (hash valid) | 0 / `invalid` | `foot\n` | rc 0, `cache=invalid` | `M-17` (terminator on 50), `v2-mf-11` (terminator on 51), `M-09` (60 lines) | agree; pinned (mutant caught) |
| 7 | multiline cached args (2 lines, `--print-cmd`/`--test`/id+path) | 0 / `hit` | `foot\n--a\ntail\n`, `  >--a\ntail<` | identical | **none** | agree; `F1` hole |
| 8 | multiline with an empty middle line | 0 / `hit` | `foot\n--a\n\nzx\n` | identical | **none** | agree; `F1` hole |
| 9 | cached action (line 5 = `srv`) | 0 / `hit` | `foot.desktop:srv` / `path:srv` | identical | `v2-mf-24`, `L1-05` | agree; pinned |
| 10 | empty fields: line 2 / line 1 / line 3 / line 4 / lines 3-10 | `stale` / `stale` / `hit` / `hit` / `hit` | `foot\n`, `""`, `""`, `foot.desktop`, `""` | identical in all five | `v2-wi-26..30`, `v2-mf-06/09/23` | agree; pinned (`--print-content` on an empty path: rc 1, `x:1362` redirect) |
| 11 | cache path default (`XDG_CACHE_HOME` unset) and `XDG_CACHE_HOME=""` | 0 / `hit` both | `foot\n` | identical, `cache=hit` | `W-02`, `W-14`, `v2-wd-38` (the only `default_cache` fixtures) | agree; pinned by `state` (`W-02`) and by stdout (`W-14`) |
| 12 | `XTE_CACHE_ENABLED=""` with a valid cache (+ `/enable_cache`, `/disable_cache`, none) | 0 / `disabled` | `foot\n` | rc 0, `cache=disabled` | **none** (only `0/no/banana/1/true`) | agree; `F3` unobservable |
| 13 | exec word-split corners: terminator on line 11; trailing `\x1f`; leading `\x1f` | 0 / `hit` | `\n`, `foot\n--a\n`, `\nfoot\n` | identical | `v2-mf-30`, `v2-mf-03` | agree; pinned |
| 14 | NUL byte inside a cached field | 0 / `stale` | cold path | identical | none | agree |

Empty-string `XDG_CACHE_HOME` (`":-"` ⇒ `$HOME/.cache`, `x:172`) and `XDG_CACHE_HOME` unset behave the same
in the pin and in the tool (`A13`/`A14`).

## Frozen-set verification (my replay, variant A, host)

`mado-terminal.py fixtures=204 tool_agrees=204 state_ok=204 cold_ok=204 premise_ok=204 expect_ok=204
explain_ok=204` and `MADO_TERMINAL_SELFTEST: 69/69 passed`.
No fixture's recorded `state`, `cold`, `expect` or class premise drifted on this host.

## Mutant matrix (measured; `mut/*.py`, `ev/replayx*.json`)

| mutant (one edit) | selftest | clause w (rc/stdout) | state/cold/premise | clause x | survives freeze? |
|---|---|---|---|---|---|
| `joinless` — `usep + line` instead of `usep + LF + line` (`x:248`) | 69/69 | 204/204 | 204/204 | 204/204 | **YES — hole `F1`** |
| `unreadable_absent` — unreadable cache ⇒ `absent` | 69/69 | 204/204 | 204/204 | 204/204 | **YES — hole `F2`** |
| `cache_home_only` — never look in `$HOME/.cache` | 69/69 | 203/204 (`W-14`) | 204/204 | fails (`W-02`: `cache=absent` vs `hit`) | no — default path is pinned |
| `line50_accept` — the limit fires at `n > 50` instead of `n == 50` | **68/69** | 204/204 | 204/204 | fails on `M-17` (`cache=stale` vs `invalid`; 202/204) | no — the boundary at 50 is pinned |

The two survivors are not merely passing: their per-fixture tool output **and** explain fields are
byte-identical to the frozen tool's on all 204 fixtures (`ev/replayxx4-{joinless,unreadable_absent}.json`,
zero differences against `ev/replayxx3-mado-terminal.json`).

### F1 — the LF reconstruction of a multi-line cache is unscored (pre-data hole, must be fixed before data)

The pin documents the feature it implements: *"Command is stored as raw expanded and tokenized
`$XTE__USEP`-separated command, technically it can contain newline characters. Reconstruct newlines"*
(`x:245-247`), implemented at `x:248`. Its `save_cache` newline guard (`x:312-318`) compares the **whole
concatenation** with a bare newline (pattern `"$XTE__LF"`), so it can only fire when every field is empty —
for a real newline-bearing argument the cache is **written**, not removed.

Measured, pin-reachable, on `$ROOT/usr/share/applications/foot.desktop` =
`[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot "a\nb"\n` (a two-character `\n`
escape inside quotes, which the pin's expander turns into a newline):

```
cold  pin --print-cmd   rc=0  'foot\na\nb\n'
      pin writes        12 physical lines:
       '5cac47f4…\nfoot\n<root>/usr/share/applications/./foot.desktop\nfoot.desktop\n\n-e\n\n\n\n\nfoot\x1fa\nb\x1eEND_OF_EXEC_USEP\n'
warm  pin --print-cmd   rc=0  'foot\na\nb\n'          (hit)
warm  pin --test        rc=0  'Command and arguments:\n  >foot<\n  >a\nb<\n'
      frozen tool       identical on all three, explain cache=hit
      joinless mutant    'foot\nab\n'  /  '  >foot<\n  >ab<\n'      ← mispredicts
```

Why the freeze cannot see it: every `state=hit` fixture (90/90) gets its cache from `prime`, i.e. from the
pin's own `save_cache`, and **no frozen entry text contains a backslash** (checked over all 204 `files`
maps), so no primed cache can be multi-line; no literal-cache fixture carries a real md5 (all `000…`,
empty, short, long or non-hex), so the hit path is never entered from a literal cache; no `cache_lines` /
`cache_sub` value injects a newline into lines 11+ (the only `\n→\r\n` rewrites make the cache *invalid*);
`gen_warm_case` hits are all prime-based and `corrupt_cache` never emits a valid multi-line cache (checked
over 240 generated instances, three nonces); `--selftest` has no such case (the mutant scores 69/69).

Recommended repair (before the data commit, no expectation changes): one `WARM-SAME` fixture with the
`Exec=foot "a\nb"` entry above, `prime` = `["--print-cmd"]`, `expect` `{rc:0, stdout:"foot\na\nb\n"}`,
`state:"hit"`, `cold` `{rc:0, stdout:"foot\na\nb\n"}` — and the `joinless` mutant added to the w1 control
directory, because it is the only control that distinguishes the rule. Optionally a second fixture with
`["--test"]` (`  >a\nb<`). `cmd=` in the explain record stays `foot` (the first word), so clause `x`'s
one-physical-line parser (`TERM_RE`) is not affected by this fixture; a fixture whose **first** command word
contains a newline would be unparseable to `TERM_RE` and must not be added without extending the parser.

### F2 — an unreadable cache is unscored (pre-data hole, must be fixed before data)

Measured (`A1`): file mode 000, valid content. `[ -f ]` (`x:221`) is true, so the pin opens it and the
`done < "${XTE__CACHE_FILE}"` redirect (`x:258`, reported by bash as `line 217`) fails:

```
<pin>: line 217: <root>/.rw/cache/xdg-terminal-exec: Permission denied
D: invalid cache data
```

`xte__finished` stays 0 ⇒ `invalid cache data` ⇒ cold answer, rc 0, stdout `foot\n`; the background
`save_cache` then fails on the same path too (`<pin>: line 321: <root>/.rw/cache/xdg-terminal-exec:
Permission denied`, harmless: it runs in the forked subshell of `x:1457`). The counter's mapping turns the
run into `invalid` (correct), and the frozen tool predicts `invalid`/cold (correct). Contrast: a mode-000
*directory* (or the cache path being a directory) makes `-f` false ⇒ `no cache data` ⇒ `absent`.

Why the freeze cannot see it: no fixture uses `after.modes` on the cache path (the only `modes` fixture,
`v2-wi-21`, chmods a desktop entry), so the branch is never taken and `unreadable_absent` survives everything.
Recommended repair: one `MALFORMED` fixture — `prime: {"args":["--print-cmd"]}`,
`after: {"modes": {".rw/cache/xdg-terminal-exec": 0}}`, `args:["--print-cmd"]`, `state:"invalid"`,
`expect:{rc:0, stdout:"<the cold answer>"}` — plus `unreadable_absent` as a control. Note the class is the
*full* assertion here: stdout alone cannot separate `invalid` from `absent`, only `state`/`explain cache=`
can, which is exactly why the recorded `state` matters.

### F3 — `XTE_CACHE_ENABLED=""` (empty) is untested and unobservable

`check_bool ""` prints `Assuming '' means no` and returns 1 (`x:50-59`), so the cache is never read; but
`XTE__CACHE_CONFIGURED=${XTE_CACHE_ENABLED-}` is empty, so a `/enable_cache` directive in a list file still
wins and `save_cache` **writes** the cache, while with a non-empty bad value the directive is ignored and the
cache is **removed**. Measured (`A15`/`A16`/`A16b`/`A17`/`A17b`): stdout `foot\n`, rc 0 and derived
`disabled` in all five; the cache file ends `absent` without a directive, `present` (rewritten) with
`/enable_cache`, `absent` with `/disable_cache`. Because no scored channel reads the cache file after a run,
a fixture cannot distinguish these; the tool models `cache_configured` correctly (`A16` agrees). No repair
required; recorded so a future wave does not mistake this for a gap.

## Recorded pin facts that a future round should not re-derive

* `set -euf` (`x:23`) does **not** abort on the unreadable-cache redirect, because `read_cache` is invoked in
  an `if check_bool … && read_cache` list (bash suppresses errexit inside a function called from a condition).
  Reasoning from `set -e` alone predicts exit 1/empty stdout — the pin does not do that.
* The line limit is checked **before** the terminator check (`x:239` precedes `x:245-255`): a terminator on
  line 50 is `invalid`; on line 49 it is a hit.
* An unterminated last line is invisible to `while IFS= read -r` (bash returns 1 with the partial value and
  the body never runs): `M-18` is `invalid`, not a hit, and a terminated cache followed by an unterminated
  junk line is still a hit (`A4`).
* The terminator must end its line: a `\r` after it (CRLF) defeats the match, which is why `v2-wi-31` is
  `invalid` rather than `stale`.
* `command -v <line 2>` is the only command gate: script function names (`gen_hash`, `read_cache`, …), bash
  builtins/keywords, `--`/`-p`/`-v`/`-V` clusters and resolvable paths pass; `""` and other `-…` fail.
* `save_cache` is forked (`x:1457`) and skipped entirely when the cache was used (`x:1455`), and
  `--print-content` exits before it — so a cold `--print-content` run never writes a cache.

## Risks / residuals of this seat

* My replay is host-side, not bwrap-side: `PATH` is `$ROOT/bin:/usr/bin:/bin` (the counter uses `/oracle/bin`
  with copies of the seven externals) and stderr isolation is not reproduced. stdout/rc/state/premise/explain
  are the compared channels, so this does not change any verdict I report; the counter's sandbox remains the
  authority for the final score.
* Clause `x`'s `cmd=` was not re-derived from the pin's `--print-cmd=\036` run in my replay; my explain
  comparison covers selected/path/cache/verdict (none of the mutants touches the command). The frozen set's
  own recorded expectations are unchanged, so this cannot mask an expectation drift.
* The 10 `HOME-UNSET` fixtures were replayed and passed (part of the 204/204), but their `set -u` reasoning
  (round-47 D1) is out of this seat's scope and was not re-derived.
* Not attacked here (other seats' scope): C2, the registry/README rows, the D1-D4 installation, and anything
  that is not the C1 cache contract.

## Reproduce

The harness and mutants are retained under `w2/RevC1Cache/`; copy them into a fresh scratch seat directory
and run from there (they build `tree*/`, `rp*/` and read/write only under the script's `S` constant):

```
S=/fast/scratch/hyaku/mado-r48/RevC1Cache            # recreate, adjust S in the copies if it differs
python3 host.py                                       # pin vs frozen tool vs mutants, 24 cases, ~3 s
REPLAY_TAG=x4 python3 replay2.py /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-terminal.py
REPLAY_TAG=x4 python3 replay2.py mut/joinless.py      # ~60 s per tool, 204 fixtures, clause w + x
python3 -I <tool> --selftest                          # frozen 69/69, joinless 69/69, line50_accept 68/69
```
Retained: `w2/RevC1Cache/{host.py,replay.py,replay2.py}`, `w2/RevC1Cache/mut/*.py`,
`w2/RevC1Cache/ev/{host-cases.json,pin-functions.txt,replay-*.json,replayx*.json}`.
No lane file was modified. Shell writers ran under `ulimit -f 2048`; the largest retained output file is
105,971 bytes (`ev/replayxx4-joinless.json` / `…-unreadable_absent.json`) and the scratch total was 1.7 MB
before removal (the only larger file ever touched was a failed 1 MiB-truncated host-binary copy from an
abandoned counter-`Box` attempt, since deleted).
