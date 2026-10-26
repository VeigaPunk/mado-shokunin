# ExecCounterC1 — round-47 w1 BUILD: the C1 counter draft

Status: instrument complete and measured; the L1 froze `quality/counters/c1-r47-terminal.py` at `d7527d60` while
this seat was still measuring, so this draft is input to that freeze, not the frozen artifact
(`xdg-terminal-exec`/fixtures/`--work` layout differ; see the comparison at the end). Numbers below name their
receipt; three final-version measurements (guards, the reference's TARGET_MET, the cache mutant) were cut by the freeze
and stand only in the session transcript - their commands are `run-final-battery.sh <scratch>`, one pass each.

Deliverable: `.ufo/waves/round-47/w1/ExecCounterC1/c1-r47-terminal.py` (draft; this seat never wrote the tracked
`quality/counters/c1-r47-terminal.py`, which the L1 froze at `d7527d60` from its own material).
sha256 `7b1572056db0fe65a14ceb7e3b27b730f29363fc68d36427c84212dae94bc10a`.

Companion files in this seat (all needed to re-run or audit the counter):

| file | what it is |
|---|---|
| `c1-r47-terminal.py` | the counter: `--repo R --rev X --work DIR [--nonce N] [--fixtures F]` |
| `xdg-terminal-exec-v0.14.3` | the pinned judge, byte-equal to upstream tag v0.14.3 and to `/usr/bin/xdg-terminal-exec` (`receipts/pin-script.txt`) |
| `fixtures-placeholder.json` | 128 hand-written placeholder cases, `expect` produced by the pinned script (self-test only, NOT the round's fixture set) |
| `make-placeholder-fixtures.py` | builds that file from 16 templates × 8 argument variants |
| `controls/*.py` | stub, lietest, delegator, subproc, embed control tools |
| `run-controls.py` | commits each control into a throwaway repo and scores it |
| `check-counter-guards.py` | guard/non-vacuity checks (14) |
| `check-oracle-determinism.py` | the script must answer the same generated case identically in two case roots |
| `make-cacheread-mutant.py` | mutation test for the forged-cache clause |
| `run-final-battery.sh` | one pass of all of the above, receipts into `receipts/` |

## What the counter does

The judge is the real script, pinned by sha256 and resolved from
`<counter dir>/xdg-terminal-exec` → `<counter dir>/xdg-terminal-exec-v0.14.3` → `quality/counters/…` →
`.ufo/waves/round-47/w1/ScoutScriptMap/upstream-xdg-terminal-exec` → `/usr/bin/xdg-terminal-exec`. The first
candidate that exists decides, and a byte difference is a setup error (a present-but-different copy is a revocation of
the pin, not something to paper over). Clauses:

- **a** `tools/mado-terminal.py` is a blob (100644/100755) at REV; absent → `tool=absent`, `TARGET_MISSED`, exit 1.
- **s** `python3 -I TOOL --selftest` in the sandbox: exit 0, last non-empty stdout line exactly
  `MADO_TERMINAL_SELFTEST: N/N passed`, N from ASCII digits, N ≥ 30.
- **f** four runs per fixture: (i) seed-47 case root, fixture env; (ii) seed-nonce case root, fixture env;
  (iii) nonce case root, env variant (`TMPDIR`, `XDG_RUNTIME_DIR`, `TERM`, `PYTHONHASHSEED`, `LANG`); (iv) forged
  cache. Each of (i)-(iii) runs the script and the tool in **separate freshly materialized roots** and requires
  tool stdout+rc == script stdout+rc (normalized: that run's case root → `$ROOT`) **and** script stdout+rc == the
  fixture's recorded `expect` (the expect is checked first, so drift is reported as `oracle-vs-expect`, not as a tool
  defect). Run (iv) runs the script once (through a wrapper that lets its backgrounded `save_cache` finish, relaying
  stdout and rc unchanged), forges its cache (entry path, id, action and exec array replaced; hash and command lines
  kept, so the script treats it as actual), and requires the tool to still print the cold answer for that root.
  `forge_live` proves the forged cache actually changes the script's own answer. stderr is unconstrained (the script
  writes diagnostics there; the contract is stdout and exit status).
- **i** every run is bubblewrap with `/usr`,`/etc` read-only, host `/bin`,`/sbin`,`/lib`,`/lib64` symlinks,
  `--dev /dev --proc /proc --tmpfs /tmp --unshare-pid --unshare-net --die-with-parent`, plus read-only binds of the
  tool dir, the script dir and the tool-bin dir and a writable bind of the case dir only; no host `/home`, `/run`,
  `/var`, `/srv`, `/opt`, `/mnt`, and the case dir is the only `/fast` path. The counter also traces the script's own
  `openat`/`open` on the probe case and refuses to score if the resolver opens anything under the operator's home.
- **r** two independent tripwires, both proven live at count time before any tool run: (1) PATH is
  `$ROOT/bin:<toolbin>` where toolbin symlinks all of `/usr/bin` except executable fakes named
  `xdg-terminal-exec`, `sh`, `bash`, `dash`, `busybox` and every `python*` other than the interpreter, each connecting
  to a counter-owned unix socket (bound read-only at `/trip`) and also mounted read-only over the corresponding
  `/usr/bin` realpath during tool runs (a name is covered at its realpath because `/usr/bin/sh` is a symlink and
  bubblewrap cannot mount on a symlink destination); (2) `strace -f -qq -e trace=execve,socket,connect` on a resolving
  probe case (all five print modes, `--dir/--title/--app-id/--hold`, an entry with `TerminalArg*`) must show exactly
  one successful execve (the interpreter) and no socket/connect line.
- **g** 150 nonce-driven cases from `gen_case()` (config list files desktop-prefixed and plain across config and
  data-dir stores, the `/enable_cache` `/disable_cache` `/execarg_compat` `/execarg_strict` `/execarg_default`
  directives, `+`/`-` markers, actions; entries with duplicates/overrides, Hidden, TryExec, Type, Categories,
  OnlyShowIn/NotShowIn, Actions, `X-TerminalArg*`, quoting and % fields, missing executables, invalid IDs; print modes
  mixed, repeated, with `--print-cmd=<seq>`/`--print-delimiter=<seq>`, `--dir/--title/--app-id/--hold`, trailing
  command words, unknown options), each judged by the real script in the sandbox.

Summary line and exit codes exactly as assigned: `fixtures=a/b generated=c/150 selftest=ok|fail readonly=ok|fail
tool=present|absent verdict=TARGET_MET|TARGET_MISSED rev=<full> seeds=47,<nonce>`; 0 met, 1 missed, 2 setup (fewer than
100 fixtures, duplicate id, path escape, cache file in a fixture, fixture pinning HOME/PATH/XDG_CACHE_HOME or pointing
into the operator's home, an argument list without a print mode before the option scanner's break, script sha
mismatch, `bwrap`/`strace` missing, a script-side timeout).

## Measured (receipts)

- **The counter is satisfiable.** `ExecRefB/mado-terminal.py` reaches `verdict=TARGET_MET` with
  `fixtures=128/128 generated=150/150 selftest=ok readonly=ok` (measured in the session at the draft's final sha; the
  same reference at its earlier sha is the `good` control in `receipts/ctl-c1-good.txt`, `fixtures=128/128`).
- **Controls all MISS**, `CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 5; reference met: 0)`
  (`receipts/controls-run.txt`, `receipts/ctl-c1-*.txt`):
  stub → s/f/g fail; lietest (`40/40` printed, nothing implemented) → s passes, f/g fail; delegator (`os.execv`
  `/usr/bin/xdg-terminal-exec`) and subproc → `readonly=fail`, trace shows two execve plus
  `connect(… sun_path="/trip/s.sock")`, 535 tripwire hits; embed (script text written out and piped to `/bin/sh`) →
  `execve=['/usr/bin/python3', '/bin/sh']`, tripped `sh`.
- **Guards 14/14** (the same 14 checks passed on the draft before the forged-cache addition; the final-sha re-run was
  cut by the freeze): tool-absent, bad-rev, fewer-than-100, no-print-mode, path-escape,
  duplicate-id, work-inside-lane, work-inside-repo, `oracle-vs-expect` live (a mutated expect is reported as fixture
  drift), four selftest formats (29/29 fails, 30/30 passes — the boundary, 31/30 fails, Arabic-Indic digits fail) and
  nonce dependence.
- **The forged-cache clause bites** (measured in the session; `make-cacheread-mutant.py` reproduces the mutant): the
  reference plus one hook that reads the resolver cache is `fixtures=53/128` with exactly 75 `cacheD:` failures (the 75
  fixtures where a cache was forged), `generated=150/150 selftest=ok readonly=ok` → `TARGET_MISSED`.
- **The script is deterministic on the generated cases** (`receipts/oracle-determinism.txt`): 150/150 identical
  across two case roots.
- **Pin** (`receipts/pin-script.txt`): upstream tag v0.14.3, the host binary, the lane's two Scout pins and this seat's
  copy are all `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`.

## Host safety

No terminal was launched and no process was started outside `bwrap`/`strace`/`git`/`python3`: every script invocation
carried a `--print-*` mode (and the counter refuses an argument list whose print mode comes after the scanner's break),
every script and tool run took `XDG_CACHE_HOME=<case root>/.cache` with the root materialized empty, and the script was
run 300+ times without ever reaching `exec "$@"`. Compositor untouched, no package transaction, host config trees read
only, session material never collected.

## Risks and residuals (also declared in the counter docstring)

1. A `--print-content`/`--test`-shaped fixture is outside the draft contract; such a fixture would fail the tool
   legitimately, but the L1 should decide whether the fixture set may contain it.
2. Run (iv) cannot forge when the script wrote no cache (id/path-only print modes exit before `save_cache`; 75 of 128
   placeholder fixtures take the cmd path). A tool that reads an absent cache and one that ignores the cache are
   indistinguishable there; run (iv) carries the cache claim where a cache can exist.
3. `save_cache` is backgrounded (`xdg-terminal-exec:1457`), so the forged cache can in principle be overwritten by the
   tail of that write, which can only turn a cache-reading tool's failure into a pass for that fixture; the counter
   uses a wrapper that waits 0.15 s for the write and then forges.
4. `find -L` is unsorted (`xdg-terminal-exec:795`): a fixture that leaves two co-equal terminal entries in one
   applications directory depends on directory order. Within one run both roots are materialized in JSON key order, so
   the counter pins that order; a fixture whose answer depends on readdir order is a fixture defect. The generated
   clause is not affected on this filesystem (150/150 deterministic, receipt above).
5. Clause r proves "no process, no socket" on one traced case plus the tripwire over all runs; a tool that branches on
   its arguments and spawns only where nothing is traced is not excluded by strace alone (the tripwire would still
   catch the named binaries).
6. Whether the real script matches the host's launch path (`uwsm-app -- xdg-terminal-exec --dir=...`) beyond the script
   is the non-author reading; the counter is silent on it.
7. Fixtures are the L1's; this seat's `fixtures-placeholder.json` is a self-test instrument and must not be frozen as
   the round's fixture set (the round's set is ExecFixtures' ≥120 cases).

## For the L1 (freeze notes)

- Land the counter together with the pinned script copy (or keep the `ScoutScriptMap` pin): the counter only needs one
  of the candidate paths to hold a byte-equal copy.
- `--fixtures` has no useful default until the round's fixture file is placed beside the counter as
  `c1-r47-fixtures.json`; the run-time fixture sha256 is printed on the `clause=i` line for the freeze to record.
- Decide on run (iv) (forged cache). It is an addition to the three runs named in the seat brief, justified by
  SentHost-3/ExecCache (a forged cache makes the script answer differently, so a tool that reads a cache must not
  pass); dropping it restores the three-run shape, keeping the empty-cache-per-root enforcement either way.
- Runtime on this host: about 45 s per scored revision with 128 fixtures, measured with `ExecRefB`.

## Against the frozen counter (`d7527d60`, `quality/counters/c1-r47-terminal.py`)

Read at the freeze; compared clause by clause with this draft. The frozen counter is stricter in three places and
already covers one thing this draft does not; three things this draft carries are absent there.

**Stricter in the frozen counter (accepted, no action from this seat).**
- Isolation is a constructed root (`--unshare-all --clearenv`, `/usr/lib` only, bash + the resolver's seven external
  commands, `/usr/bin/python3` for the tool) instead of this draft's `/usr` + `/etc` binds; much smaller surface.
- Clause `r` runs *every* tool run under `strace` and traces `execve,execveat,socket,socketpair,connect`, so a socket
  made by anything the tool forks is a trip; this draft's strace covers only the probe case and leans on the tripwire
  fakes for the rest.
- Clause `x` (explain + `--observed` AGREE/DIFFER) exists there and not here: this draft scores `print` only, so a tool
  could reach TARGET_MET with a broken `explain` contract. That is the largest coverage item this draft lacks.

**This draft has, the frozen counter lacks.**
1. **A cache-reading tool is undetectable.** The frozen counter's contract calls the warm cache out of scope and
   never presents one: `XDG_CACHE_HOME=<root>/.rw/cache` is created empty, and the oracle's tree is a different tree,
   so every tool run sees no cache. Measured consequence here: the reference plus one hook that prints the resolver's
   cached fields when a cache exists (`make-cacheread-mutant.py`) scores `fixtures=53/128` with exactly 75 `cacheD:`
   failures under this draft's forged-cache run and would score the frozen counter's `f` clause unchanged, because no
   run ever hands it a cache. Whether that matters is a freeze decision: a tool that models a cold cache is required by
   the contract, and the frozen sandbox makes the mistake unobservable rather than impossible.
2. **A script-side timeout becomes a verdict, not a setup error.** The frozen `run()` maps `TimeoutExpired` to
   `(124, "")` and then compares the tool against that value. A fixture that blocks the judge (a FIFO named `*.desktop`
   in the last applications dir does: ExecStraceTrip/SentHost evidence) therefore reads as "the tool must print
   nothing and exit 124", i.e. the instrument scores its own hang. This draft raises a setup error instead, so a
   blocking case can never be mistaken for a tool defect.
3. **No oracle-determinism guard on the generated clause.** `g` there compares the tool with one oracle run per case;
   if the judge were nondeterministic on a case, a correct tool would fail. Measured here (`receipts/oracle-determinism.txt`)
   the judge is 150/150 identical across two case roots for this draft's generator, which is evidence that the frozen
   `g` clause is safe on this host and filesystem — but it is evidence, not a check inside the frozen counter.
4. **Smaller, both host-safety belts:** this draft refuses a fixture whose argument list reaches the option scanner's
   break before consuming a print mode (without a print mode the resolver `exec`s a terminal; the frozen sandbox has no
   terminal binary, so it is harmless there), and it traces the resolver's own `openat` to refuse a run that reads
   anything under the operator's home. The frozen counter achieves the second property structurally by `--clearenv`
   and a minimal root.

**Fixture scope note for the freeze.** The frozen `g` argument vectors include `--test -e ls`, `--print-content` and
`--print-content --print-cmd`. The seat brief's draft contract names `--print-id/--print-path/--print-cmd[=seq]/
--print-delimiter=seq`; this draft's generator stayed inside those. If the frozen `g` clause keeps `--test` and
`--print-content`, the tool contract must be widened to cover them explicitly, or a compliant tool fails `g` on a mode
the contract never asked for.
