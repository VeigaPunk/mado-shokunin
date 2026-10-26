# SentHost — host-mutation and privacy risk of w1 (round 47)

Seat: SentHost · wave: w1 (BUILD) · date 2026-10-26 · lane tip at round start `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`
Scope: what this wave asks seats to do to the host, and what `tools/mado-terminal.py` must guarantee so that
`explain` on the host is safe. Every experiment ran on scratch fixtures under
`/fast/scratch/hyaku/mado-r47/SentHost/`; `~/.config`, `~/.local/share` and the compositor were only read.

**One inadvertent host write happened, by this seat.** The agent shell exports
`XDG_CACHE_HOME=/home/vgpnk/.cache`, so setting `HOME=<scratch>` did not redirect the resolver cache: in one
traced pass my harness opened `~/.cache/xdg-terminal-exec` four times for reading and **once for writing**, and
left a fixture entry in it (F2b; three such passes ran). I detected it by re-stat'ing
the file, reconstructed the original 190 bytes from a captured read, and wrote them back with the original
mtime; `sha256 f497ed05…`, size 190 and `mtime 17:42:25.200770484 -0300` are restored
(`receipts/host-cache-observed.txt`, `receipts/cache-restored.txt`). Nothing else outside scratch was written.

---

## 0. Verdict

1. The wave's own guard (`w1-spec.json:3`: "never launch a terminal or any GUI program") is **not carried into
   three seat prompts** — `ExecFixtures` (:24), `ExecControls` (:39) and `ExecCache` (:49) run the real
   resolver without a printed requirement that the argv contain a print mode. (`ExecRefCompare` :84 does say
   "print modes, XDG_CACHE_HOME empty, restricted PATH"; it is compliant.)
2. **The resolver cache is the one way this wave can write outside scratch — and the trap is live.**
   It happens when a run includes `--print-cmd` *and* `XDG_CACHE_HOME` is unset or empty (both mean
   `$HOME/.cache`, `/usr/bin/xdg-terminal-exec:172`). Worse, the agent shell already exports
   `XDG_CACHE_HOME=/home/vgpnk/.cache`, so `HOME=<scratch>` redirects nothing (F2b — this seat hit it and
   restored the file). `ExecFixtures` (:24) states neither. `ScrSkill` (:154) documents a `mktemp -d` capture
   that is never removed.
3. **A FIFO named `*.desktop` in the user applications dir hangs the resolver forever** (proven:
   `openat(... Fifo.desktop, O_RDONLY) = ? ERESTARTSYS`). That is a live DoS on SUPER+RETURN, on every
   `--print-*` run in this wave, and on the C1 judge if a fixture ever materializes one. The planned tool must
   therefore refuse non-regular files — which is a *frozen, documented divergence* from the script, not a bug.

---

## 1. Method and what was actually run

| probe | result | receipt |
|---|---|---|
| `bwrap --unshare-all … /usr/bin/true` on this host | rc=0; `kernel.unprivileged_userns_clone=1` | this report §1 |
| `strace -f -e trace=execve,socket,connect python3 -I pure.py` | execve=1 socket=0 connect=0 | `receipts/exec-argv.txt` |
| `strace` of a full print run (`--print-id --print-path --print-cmd`) | spawns `awk find ls md5sum tr`; writes only the cache file and `/dev/null` | `receipts/exec-argv.txt` |
| cache target under three `XDG_CACHE_HOME` states | `--print-id` writes nothing; `--print-cmd` writes; unset **and empty value** both fall back to `$HOME/.cache` | `receipts/cache-write.txt` |
| same, with `HOME=<scratch>` but `XDG_CACHE_HOME` left inherited | the real `~/.cache` is opened (the ambient value wins over `HOME`) | `receipts/ambient-cache-env.txt` |
| warm vs cold cache over an edited entry | warm prints `fake-term`, cold prints `fake-trmX` | `receipts/stale-cache.txt` |
| hostile applications dir (FIFO, loop, `/proc` link, dangling, 50 MB file) | FIFO hangs the resolver | `receipts/hostile-files.txt`, `receipts/fifo-hang.txt` |
| `Exec=cd` / `Exec=foo; touch …` / `Exec=$(touch …)` | builtin accepted; metacharacters never executed (0 canaries) | `receipts/builtin-exec.txt` |
| host applications dirs, shape only | user 71 entries / `/usr/share` 121 / 0 non-regular / 0 symlinks / 1 subdir | this report §6 |

Resolver hashed: `/usr/bin/xdg-terminal-exec` sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (matches the wave's pin).

---

## 2. Every host command the wave names, seat by seat

Locators are `w1-spec.json` prompt lines (computed: `receipts/seat-lines.txt`, `receipts/locators.txt`).
"launch" = can start a non-read-only program; "write" = can write outside the seat scratch.

| seat (spec line) | host command(s) in the prompt | launch | write | verdict |
|---|---|---|---|---|
| ExecRefA (:9) | real script in `bwrap` *or* "scratch env: every XDG_* var set into a case root, HOME=<root>/home, XDG_CACHE_HOME=<empty>, PATH=<root>/bin:…" | no (print) | case root only | SAFE **because** this prompt names `XDG_CACHE_HOME`; `HOME` alone would not suffice (**F2b**); `PATH` needs `ls`+`md5sum` too, not just `tr/find/awk` (`:200-201`) |
| ExecRefB (:14) | same | no | same | SAFE, same caveat |
| ExecOracle (:19) | `bwrap --unshare-all`, copy of the script, `strace -f -e trace=execve`; hides `/usr/bin /home /fast /etc/xdg /usr/share/applications` | no | `--work DIR` | SAFE (bwrap verified); must also bind `/usr/lib` + loader |
| ExecFixtures (:24) | "run the REAL script (use your own minimal sandbox: bwrap … **or document how you isolated host terminals**)" + `--nonce N` | **YES** if any case's `args` lacks a print mode | the real `~/.cache` — the schema's env map omits `XDG_CACHE_HOME`, which is ambient (**F2b**) | **F4**, **F2b** |
| ExecCounterC1 (:29) | checkout tool at rev in a scratch clone; `bwrap`; `strace -f -qq -e trace=execve,socket,connect`; fake binaries over `/usr/bin/…` | no | work dir | SAFE; needs cache-per-run (**F3**) and a `git -C "$D"` guard |
| ExecCounterC2 (:34) | reads committed pins only ("fetches nothing") | no | none | SAFE |
| ExecControls (:39) | executes DELEGATE (`os.execv /usr/bin/xdg-terminal-exec`), SUBPROC, EMBED-SH, CTYPES-EXEC variants; runner commits into a scratch clone | **YES** if argv lacks a print mode | scratch clone | **F5** |
| ExecLive (:44) | `XDG_CACHE_HOME=<scratch> xdg-terminal-exec --print-id --print-path --print-cmd`; same with `--dir=/tmp`; same with `-- htop`; `sha256sum`/`stat` over `~/.config/xdg-terminals.list`, `*-xdg-terminals.list`, both `Alacritty.desktop`, `~/.cache/xdg-terminal-exec` | no | scratch cache (only because `--print-cmd` is present) | SAFE as written; the cache must **exist** as a dir or the script `mkdir -p`s it (`:303`) |
| ExecCache (:49) | "scratch runs (XDG_CACHE_HOME in your scratch)"; valid/stale/corrupt cache cases | **unstated** | scratch | **F2c**: must still pass a print mode; the cache is read regardless of print mode, so `--print-id` suffices |
| ExecStraceTrip (:54) | `strace` inside bwrap; `execv/posix_spawn/ctypes/socket(AF_UNIX)/socket(AF_INET)` | test constructs | scratch | SAFE if the `AF_INET` socket is never `connect`ed to a real address, and `--unshare-net` is on |
| ExecSessionMarker (:59) | gate on scratch clones; "Never print the serial value" | no | scratch clones | SAFE |
| ExecSupersede (:64) | re-fetch pins (network); copy `corpus/` to scratch; `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` | no | stdout only | SAFE — verified: `--file` is distinct from `--out` (`sources-census.sh:69,78`), and the header promises "writes only stdout or --out" (`:7`); set `TMPDIR` for its `mktemp` (`:164`) |
| ExecR2Digest (:69) | `sha256sum`, `wc` over a 3.3 MB untracked TSV | no | none | SAFE; commit the digest line only, never rows |
| ExecIdGuard (:74) | `grep`/`awk` over lane `corpus/SOURCES.md`, shokuknow staged file, absent-defect register | no | **`.ufo/waves/round-47/assimilation/`** | **F9** (write-scope contradiction) |
| ExecAxisBase (:79) | `python3 -I quality/check-axis-scores.py …` (spawns committed scripts with the inherited env), `check-session-material.py …` (`git cat-file --batch`, `NamedTemporaryFile`), `for t in tools/mado-*.py; do python3 -I $t --selftest; done`, `bash tools/mado-verify.sh --selftest` | no | `TMPDIR`; **`mado-verify.sh` writes `/tmp/w5-mado-m52-*`** | SAFE, **F11** (litter; set `TMPDIR`) |
| ExecRefCompare (:84) | 500+ real-script runs, "print modes, XDG_CACHE_HOME empty, restricted PATH" | no | scratch | SAFE (**F3** still applies to the three-run reuse) |
| ScoutScriptMap (:89) / ScoutSpecs (:94) / ScrEntry (:114) / ScrRows (:119) / ScrErrataR45 (:139) | HTTPS GET of pinned URLs (github / gitlab.freedesktop.org) | no | seat dir | SAFE (pins to seat dir + sha256, as the wave requires) |
| ScoutOmarchy (:99) | reads `~/.config/xdg-terminals.list`, `~/.local/share/applications/Alacritty.desktop`; **`pacman -Qo`** | no | none | **F6** (pacman is paused host-wide) |
| ScoutShokuknow (:104) / ScoutHeld (:109) / ScrToolLedger (:149) | read shokuknow; `git grep` at base; `git log --format=%H -- <receipt>` | no | none | SAFE (read-only git) |
| ScrSkill (:154) | documents `XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-path --print-cmd` | no | **leaves a dir under `$TMPDIR`** | **F8** |
| SentPrivacy (:199) | gate on a scratch clone with a sample receipt from a read-only host run | no | scratch | SAFE; the sample must be redacted before it is cited |
| RevR46 (:204) | `c1-r46… --work <scratch>`, `c2-r46…`, tool selftests | no | scratch | SAFE |
| RevengerUwsm (:209) | reads `/usr/bin/uwsm-app`; **`systemctl --user show-environment`** | no | none | **F7** (env dump) |
| Crit*/Conn*/Scr* (rest) | reads of lane/sibling files, `git grep`, `git log` | no | none | SAFE |

No seat is told to *run* `hyprctl`: the two mentions are descriptive (the context's allowed-read list at `:3`,
and `ScrToolLedger`'s "inputs" column at `:149`). Nor is there any service restart, any package transaction, or
any `git`/`jj` write in the lane or fleet. `git` writes appear only in scratch clones — those seats must still
assert `git -C "$D" rev-parse --show-toplevel` = `$D` before the first commit (context rule, unchanged).

---

## 3. Findings

### F1 (critical — resolver DoS, reachable from the hotkey) — FIFO in the last applications dir

**Exploit path.** Any process running as the user — an installer, a dotfiles sync, a PKGBUILD that writes into
`~/.local/share/applications` — creates `~/.local/share/applications/x.desktop` as a FIFO. The next
SUPER+RETURN (`w1-spec.json:3` quotes `bindings.conf:2`) blocks forever: `uwsm-app` waits, no terminal opens.

**Why.** The resolver builds one `find` expression for all applications dirs, but only the first group is
ANDed with `-type f`; later groups are `-o`-ed in without it. Captured argv:

```
find -L <dir1>/. <dir2>/. -type f ( -path <dir1>/./[a-zA-Z0-9_]*.desktop ! -path <dir1>/./*[^a-zA-Z0-9_./-]* )
                                 -o ( -path <dir2>/./[a-zA-Z0-9_]*.desktop ! -path <dir2>/./*[^a-zA-Z0-9_./-]* )
```
i.e. `(-type f AND group1) OR group2` — the script appends `set -- "$@" -type f` once (`:766`), then joins each
further applications dir with `xte__or_arg='-o'` (`:774`). `XTE__APPLICATIONS_DIRS` is filled by *prefixing*, so
the `XDG_DATA_HOME` dir is **last** and is the unconstrained group. `ExecOracle` reproduced this vector
independently (its own receipt: rc=124, 3003 ms, reader-less FIFO), so it does not rest on my harness alone. Verbatim run of that expression lists the FIFO
only when its dir is second (`receipts/fifo-hang.txt` §2 vs §3); the resolver then blocks on
`openat(…, Fifo.desktop, O_RDONLY) = ? ERESTARTSYS` (3 s strace, rc=124).

**Measured.** `--print-id` with a valid entry present: rc=124 at 3 s (A), rc=124 at 3 s (C), rc=0 (B, FIFO in
the non-last dir). A directory named `Dir.desktop` does **not** hang (rc=0; `open` on a directory fails, not blocks). A 50 MB single-line
entry does not hang but costs ~1.6 s per scan (`receipts/hostile-files.txt`).

**Impact.** (a) live DoS on the terminal hotkey; (b) every `--print-*` command this wave runs can hang;
(c) the C1 judge cannot produce `expect` for such a case — a fixture generator that materializes a FIFO will
hang the counter itself.

**Smallest remediation (this wave).**
1. Wave prose: no fixture may materialize a FIFO/socket/device; the fixture schema's `files` map creates
   regular files only (state it explicitly in the frozen schema doc).
2. C1 counter: per-case wall-clock timeout on *both* sides; a script timeout is a setup error, never a verdict.
3. Tool: reject non-regular files **before** opening (§4 R2) and trace `rejected: non-regular`. Freeze this as
   a declared divergence: the script hangs, the tool must not.

### F2 (high — write outside scratch) — the cache write is narrower than the wave says, and one spelling hits `~` 

Three empirical facts (`receipts/cache-write.txt`):

| invocation | writes |
|---|---|
| `--print-id` only | **nothing** — the early bail-out at `xdg-terminal-exec:1368-1386` exits (`:1383`) before `save_cache` (`:1457`) |
| `--print-id --print-path --print-cmd` | `$XDG_CACHE_HOME/xdg-terminal-exec` |
| `--print-cmd`, `XDG_CACHE_HOME` unset | `$HOME/.cache/xdg-terminal-exec` |
| `--print-cmd`, `XDG_CACHE_HOME=` (empty value) | `$HOME/.cache/xdg-terminal-exec` |

Cause of the last row: `:172` uses `:-`, so an empty value is treated as unset. The wave says
"`XDG_CACHE_HOME=<empty dir>`" (`:3`), which a seat can read as "set it to empty".
Also `mkdir -p "${XDG_CACHE_HOME}"` (`:303`) means a non-existent path is created, so a typo'd path is
materialised rather than failing.

**Remediation.** Freeze the wording: *an existing, empty directory under `/fast/scratch/hyaku/mado-r47/<Seat>/`*;
add the precondition `[ -d "$XDG_CACHE_HOME" ] && [ -z "$(ls -A "$XDG_CACHE_HOME")" ]` before any run, and
`test "${XDG_CACHE_HOME:-x}" != ""` (rejects the empty-value spelling).

### F2b (critical — and this seat hit it) — `XDG_CACHE_HOME` is ambient, so `HOME=<scratch>` redirects nothing

The agent shell exports `XDG_CACHE_HOME=/home/vgpnk/.cache` (`receipts/ambient-cache-env.txt`). The frozen
fixture schema's `env` map names only `XDG_CURRENT_DESKTOP`, `XDG_CONFIG_HOME`, `XDG_CONFIG_DIRS`,
`XDG_DATA_HOME`, `XDG_DATA_DIRS` — **not** `XDG_CACHE_HOME`. A harness that sets exactly those five plus `HOME`
therefore still inherits the real cache path, and the first `--print-cmd` writes the real `~/.cache`.

Proof that does not write: with `HOME=<scratch>` and the variable inherited, `--print-id` opens
`/home/vgpnk/.cache/xdg-terminal-exec` `O_RDONLY`; with the variable redirected it opens no cache at all
(`receipts/ambient-cache-env.txt`).

**This seat made the mistake.** In one traced pass of my receipt generator the real
`~/.cache/xdg-terminal-exec` was opened four times `O_RDONLY` and once `O_WRONLY|O_CREAT|O_TRUNC`, and the
fixture's entry (`…/bu/…/OnlyCD.desktop`) ended up in it; three passes ran (mtime moved 17:42:25 → 18:50:55). It was found by
re-stat'ing the file, and attributed by tracing the generator: the `O_WRONLY` open belongs to my own bash
process, and the cached entry is my `bu` fixture. Restored byte-identically
(`receipts/host-cache-observed.txt`, `receipts/cache-restored.txt`). What wrote the *pre-existing* 190-byte
content at 17:42:25 — a normal terminal launch or an earlier seat with the same bug — is not knowable from the
file; the mechanism above makes the latter plausible for any seat in this wave.

Corroboration from the comparison seats (their receipts, not mine): `ExecRefA`, `ExecRefB` and `ExecRefCompare`
(809 runs) build complete child environments with an explicit per-case `XDG_CACHE_HOME` and report no host
writes; `ExecRefCompare` stat'ed `~/.cache/xdg-terminal-exec` at 190 B / `17:42:25`, matching the state I
restored.

**Remediation (freeze clause, cheap and decisive).** Every invocation of the resolver sets `XDG_CACHE_HOME`
explicitly — never `HOME` alone — and the counter asserts the resolver's file opens include **no path under
`$HOME`**. Add `XDG_CACHE_HOME` to the schema documentation as a harness-owned variable that a case may
override but never inherit.

### F3 (high — judge soundness) — a warm cache can flip the verdict

The cache key is an md5 over `ls -LRl` of the config+data paths (`:200-201`), i.e. names, sizes and mtimes —
not contents. Editing a desktop file while preserving size and mtime keeps the hash, so `read_cache` (`:274`)
applies the old answer. Measured: same tree, entry changed `fake-term`→`fake-trmX` (94→94 bytes, identical
mtime): **warm cache prints `fake-term`, cold cache prints `fake-trmX`** (`receipts/stale-cache.txt`).

Consequence for C1: the contract says the tool "models a cold cache" — but if the *judge* reuses a cache dir
across the three runs of clause f (two case-root seeds + one env variant), the judge is not cold and a correct
tool is scored DIFFER. Conversely a CACHE-READ control could pass if the counter's cache is warm.

**Peer corroboration (their receipts, not mine).** `ExecCache` independently measured the same divergence and
two more variants: a PATH-only change (an earlier-prefix binary, hashed listing unchanged) and a *forged* cache
(keep line 1, edit the cmd/path/id lines) which prints a different entry and logs "cache is actual". It also
measured the write as asynchronous — the cache file was present in 0/30 checks immediately after the process
exit and 30/30 at +50 ms. `ExecFixtures` independently confirmed the `find` precedence (a directory named
`*.desktop` is listed by the unconstrained group but fails immediately instead of blocking) and reported no
host writes (its runner is `env -i` inside bwrap with an explicit per-case cache).

Consequences beyond the stale-flip: (i) whoever can write `~/.cache/xdg-terminal-exec` chooses the terminal
without touching a single desktop file — same-user only, so it is not a privilege boundary, but it means the
cache is *selectable input* and the tool must never read it; (ii) "the cache file is missing right after the
process exited" does **not** prove nothing was written — `save_cache "$1" &` (`:1457`) may still be in flight.

**Remediation (freeze clause).** Each resolver invocation in clause f, g and the nonce batch gets a fresh
empty `XDG_CACHE_HOME` created immediately before it and discarded after it (never reused across the three
seeds), and the counter must not infer "no write" from an immediately-following `ls`. Add two negative
controls: the counter plants a poisoned cache (an entry naming a different desktop file) and requires the
tool's output to be unchanged and its open list to exclude the cache path, and it requires `explain` to state
that the cache is ignored.

### F4 (high — launch risk) — `ExecFixtures` has no print-mode or HOME mandate

`:24` says "run the REAL script (use your own minimal sandbox … **or document how you isolated host
terminals**)". The frozen schema fixes `HOME=$ROOT/home`, but nothing in that sentence says it, and nothing
says every case must carry a print mode. A generator that materializes `args: []` (legal per the schema's `…`)
and runs the script on the host **launches alacritty** — the exact thing `:3` forbids.

**Remediation.** Generator assertion: refuse any case whose `args` contains no `--print-*`/`--test`; refuse to
run unless `HOME == <case root>/home`; materialize `XDG_CACHE_HOME` inside the case root when the schema
leaves it unset. Note `--test` is launch-free (`xdg-terminal-exec:1460-1464` exits before `exec "$@"` at `:1499`); it does write the
cache, so it needs the same `XDG_CACHE_HOME` redirect — a safe alternative for argv observation.

### F5 (high — launch risk) — control variants that execute the resolver

`ExecControls` (:39) writes `DELEGATE (os.execv /usr/bin/xdg-terminal-exec)`, `SUBPROC`, `EMBED-SH`,
`CTYPES-EXEC`. These are the *instrument* the counter must reject; they are safe only if every invocation
carries a print mode. A runner that feeds a fixture case with `args: ["--dir=/tmp"]` would start a terminal on
the host.

**Remediation.** `run-controls.py` refuses any argv without a print mode (same assertion as F4) and runs each
variant inside `bwrap`. Note `--` is not special to the resolver (unknown options are discarded, `:1317-1319`),
so `-- htop` in ExecLive is safe *only* because `--print-cmd` is also present — do not "simplify" it away.

### F6 (medium — guard conflict) — `pacman -Qo` vs "pacman is PAUSED host-wide"

`:99` says "`pacman -Qo` is allowed: it is a query, not a transaction"; the orchestrator guard says never run
pacman. Both are defensible, but the stricter one should win. Verified pacman-free substitute:

```
grep -rl 'usr/share/applications/Alacritty.desktop' /var/lib/pacman/local/*/files
→ /var/lib/pacman/local/alacritty-0.17.0-1/files
```
(read-only, no DB lock, no transaction). Recommend the wave state this substitute.

### F7 (medium — privacy) — `systemctl --user show-environment` dumps the manager environment

`:209` already says "print ONLY the XDG_* and PATH keys", but the risk is the *pipe*, not the intent: a seat
that captures the command's stdout into a receipt stores whatever the user manager holds (agent sockets,
tokens). **Remediation:** the prompt must give the literal filter
`systemctl --user show-environment | grep -E '^(XDG_[A-Z_]*|PATH)='` and forbid storing raw output; the receipt
must contain only those keys.

### F8 (medium — litter and a bad precedent) — the documented capture command leaks a temp dir

`:154` (ScrSkill) documents `XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-path --print-cmd`
as the operator-facing recipe. `mktemp -d` honours `TMPDIR` (default `/tmp`) and nothing removes it; it also
relies on the inherited `TMPDIR`, which the wave forbids. This text is destined for `SKILL.md`, so it will be
copied for years. **Replacement (paste-ready):**

```
d=$(mktemp -d) && XDG_CACHE_HOME=$d xdg-terminal-exec --print-id --print-path --print-cmd; rc=$?; rm -rf "$d"; exit $rc
```

### F9 (medium — write-scope contradiction) — `assimilation/` is outside the seat directory

`:74` (ExecIdGuard) writes into `.ufo/waves/round-47/assimilation/`, while `:3` says each seat writes only its
own seat dir. Both are in the same frozen file. **Remediation:** L1 states which wins (recommended: name
`assimilation/` as a shared path in the context, or have the seat write into its own dir and let the L1 copy).

### F10 (medium — host bypass of the print-only rule) — `--print-content` prints arbitrary file bytes

The resolver supports `--print-content` (`:119`, `:1356-1376`) which emits the selected file's bytes. With
a symlink in the applications dir the "selected file" can be **any readable file**: proven with
`Escape.desktop → <outside>/Evil.desktop` — `--print-id --print-path --print-content` printed the outside
file's content (`receipts/hostile-files.txt`, last block). No seat is told to use it today, but ExecLive's
sibling commands (`--print-id/--print-path/--print-cmd`) make it a one-token edit away.
**Remediation:** wave prose bans `--print-content` on the host outright, and the tool contract stays limited
to id/path/cmd.

### F11 (low — `/tmp` dependence) — `mado-verify.sh --selftest` hardcodes `/tmp`

`tools/mado-verify.sh:24,123,271` state fixtures live under `/tmp/w5-mado-m52-*`. ExecAxisBase runs it (`:79`).
It is pre-existing committed code (so it is not a w1 violation), and the files are small, but the wave's rule is
"never rely on an inherited TMPDIR". **Remediation:** ExecAxisBase runs it as `TMPDIR=<scratch> bash …` and the
L1 notes the hardcoding for round 48 (`sources-census.sh:164` has the same `${TMPDIR:-/tmp}` shape).

### F12 (low — privacy of our own receipts) — `explain`'s trace can be a home-directory listing

The host user applications dir holds 71 entries (shape-only count). An `explain` that prints every rejected
candidate's path emits ~71 distinct `/home/...` lines — over the R4 home-listing threshold (default 10,
`quality/check-session-material.py:70,178`). **Remediation:** the trace prints rejected candidates as `id`
plus a short reason, and prints a path **only for the selected entry**; add `--redact-home` (default on for
`explain`, off for `print` so byte-equality is preserved). Any receipt that must quote a path substitutes
`$HOME` manually.

---

## 4. Tool contract — what `explain` must do so that running it on the host is safe

Threat model: `~/.local/share/applications` (71 entries, 1 subdir, user-writable) and the config list files are
attacker-influenced in the "malicious/compromised local package or synced dotfiles" sense; the operator runs
`explain` in a terminal and may commit its output. Requirements are normative for ExecRefA / ExecRefB / the
L1's landed tool. Each has a test the counter can freeze.

| # | Requirement | Why (evidence) | Frozen test |
|---|---|---|---|
| R1 | **No process, no socket, no write.** No `subprocess`/`os.system`/`exec*`/`spawn*`/`fork`, no `socket`, no `urllib`, no `ctypes`, no `pwd`/`grp` lookups. | Tripwire baseline: `python3 -I` + pure script = 1 execve, 0 socket, 0 connect (`receipts/exec-argv.txt`). Name lookups *do* open sockets: the resolver's `ls` connected to `/run/systemd/userdb/io.systemd.DropIn` and `…DynamicUser` (same receipt). | clause r, invoked as `python3 -I <tool>` (never via shebang, so the count is stable) |
| R2 | **Never open a non-regular file; never block.** `os.lstat` first; `os.open(path, O_RDONLY|O_NONBLOCK)`; then `stat.S_ISREG(os.fstat(fd).st_mode)`; refuse FIFO/socket/dir/device with `rejected: non-regular`. | FIFO hangs the resolver (`openat … ERESTARTSYS`); `receipts/fifo-hang.txt`. Lane precedent: `tools/mado-monitors.py:138-145` (`O_NONBLOCK` then `S_ISREG`), `:113` `MAX_BYTES = 1048576`, and its docstring `:26` "reads files and standard input only; it starts no process and opens no socket". | a case tree with a FIFO: `explain` must return within the case timeout with `rejected: non-regular` |
| R3 | **Symlinks: follow files, never recurse into directory links, bound the walk.** Refuse `S_ISLNK` for directories; keep a visited set of `(st_dev, st_ino)`; cap depth. | a directory symlink (`Loop.desktop -> .`) is skipped by `find -L` and does not hang, but a *file* symlink is selected: `Escape.desktop` (a link to a file outside the data dir) won the selection and printed its target. | a loop + a 3-deep link chain: `explain` terminates and names the rejection |
| R4 | **Refuse special filesystems as entry content.** If `realpath` starts with `/proc`, `/sys`, `/dev` or `/run`, do not read it; record `rejected: special-fs target`. | `/proc/self/environ` is a regular file by `stat`; a link to it would otherwise put the operator's environment into the trace. | a link to `/proc/self/environ` in a fixture; assert no `KEY=` content in stdout |
| R5 | **Hard caps**: per-file bytes (1 MiB, the lane's `MAX_BYTES`), per-line bytes, number of files scanned, total bytes, and list-file lines. Record `truncated` in the trace. | a 50 MB single-line entry costs the resolver ~1.6 s and is read whole (`receipts/hostile-files.txt`). | a 2 MiB entry: `explain` completes, exit 0, trace says `truncated`; `print` may diverge → declare the cap in the contract |
| R6 | **Never execute and never shell-expand.** `Exec`/`TryExec` are strings. `TryExec`/`exec0` lookup = PATH scan with `os.access(X_OK)` in Python; `de_expand_str` (`:501-560`) expands only `\s \n \t \r \\` — replicate that in Python. `command -v` semantics include shell builtins: `Exec=cd` is **accepted** by the real script (`receipts/builtin-exec.txt`), so a pure PATH scan would wrongly reject it. A **malformed** `Exec` must also not fail closed: `de_tokenize_exec` (`:561`) and `de_strip_fields` (`:694`) are called at `:958`/`:960` without `|| return 1`, so `Exec=sh \| cat` still selects the entry and yields argv `sh`, and `Exec=sh %z` keeps `%z` literally (`receipts/malformed-exec.txt`; control `Exec=nonexistent-prog` is discarded at `:964`). Found by ExecRefA's differential run (it reports the call sites at different line numbers). | metacharacters in `Exec` were never executed (0 canaries) — the danger is a tool that "validates" by running. | fixtures `Exec=cd` (select), `Exec=foo; touch <marker>` (select or not, but **no** marker file), `Exec=sh \| cat` (select, argv exactly `sh`), `Exec=sh %z` (select, argv `sh`,`%z`), `Exec=nonexistent-prog` (no selection, rc 1) |
| R7 | **Output hygiene for `explain` only** (not `print`): never emit file *content*; escape C0/C1 and `ESC` in every emitted value (a `Name=` or `Exec=` containing `\x1b]52;…` is a terminal-control injection into the operator's terminal); cap value length; `--redact-home` default-on. | this is the standard OSC/CSI injection class; the resolver happily carries such bytes in an `Exec`. | a fixture entry whose `Name` contains `\x1b]0;pwned\x07`; assert the stdout bytes contain `\\x1b` and no raw `0x1b` |
| R8 | **`--observed FILE`**: regular file, ≤ 1 MiB, read once, compare, never echo. | same class as R2/R5. | pass a FIFO as `--observed`: usage/setup error, no hang |
| R9 | **Mirror `find -L` traversal order, not `sorted()`.** The resolver's duplicate rule is "use last found" (`:780`), i.e. readdir order across data dirs, with `XDG_DATA_HOME` **last**. | adding a valid 50 MB entry next to a valid one flipped the selection to the *later* entry (`receipts/hostile-files.txt` §1). | a two-valid-entry fixture where readdir order decides: `print` must match |
| R10 | **Never read the resolver cache.** Model cold cache unconditionally. | F3: a warm cache changes `--print-cmd`'s answer; the tool must not inherit that, and reading `~/.cache` on the host is an unnecessary privacy read. | poisoned cache in `XDG_CACHE_HOME`: tool output unchanged |
| R11 | **Never write**, including no cache, no temp files, no `mkdir`. If a temp is unavoidable it lives under `TMPDIR` and is removed. | the contract says the resolver cache is out of scope; a tool that writes it would poison the real hotkey. | strace: zero `openat` with `O_CREAT`/`O_WRONLY` outside `/dev/null` |
| R12 | **Bounded, terminating walk** of `applications/` with a file-count cap (the host: 71 + 121 entries) and no dependence on `find`. | host shape measured §6. | a tree with 10 000 entries completes under the case timeout |

**The unresolved tension to freeze explicitly.** R2/R4/R5 make the tool *diverge* from the script on
non-regular files, special-fs links and oversize entries. The script hangs or prints content there; the tool
must not. So the C1 predicate must say: byte-equality is required **on the fixture classes that the script
answers**; the classes `FIFO`, `special-fs link`, `> cap` are judged by `explain`'s safety assertions instead.
Without that sentence, a correct tool fails clause f, and a faithful-but-unsafe tool passes.

---

## 5. What the L1 should freeze (clauses to add before w2 attacks them)

1. **Cold-cache-per-run** in clause f and g and in the nonce batch (F3).
2. **Fixture legality**: `args` must contain `--print-id`/`--print-path`/`--print-cmd[=…]`/`--test`;
   `HOME` = case root **and** `XDG_CACHE_HOME` set explicitly to an empty dir inside the case root (the
   ambient value is the real cache, F2b); no FIFO/socket/device in `files` (F1, F2, F4); the fixture set must
   carry the malformed-`Exec` pair from R6, because a stricter-than-script validator fails there.
3. **Per-case timeout on the script side**; a script timeout is a setup error (exit 2), never DIFFER (F1).
4. **Tripwire invocation form** `python3 -I <tool>` with `execve==1, socket==0, connect==0`, plus the
   poisoned-cache control (R10) and the marker-file control for `Exec=foo; touch <marker>` (R6).
5. **Declared divergences** (§4 last paragraph) listed in the C1 contract text, so clause f is not applied to
   the non-regular/special-fs/oversize classes.
6. **Prose fixes**: `XDG_CACHE_HOME` wording (F2), print-mode mandate for ExecFixtures/ExecCache/
   ExecControls (F4, F5), `--print-content` ban (F10), the `systemctl` filter (F7), the `mktemp` recipe (F8),
   the pacman substitute (F6), and the `assimilation/` ruling (F9).
7. **C2 note** (hand-off, not my claim): the `find` expression precedence (`-type f (A) -o (B)`) is a real,
   documentable property of v0.14.3, and it is *why* the FIFO hang exists. It belongs in the new entry's
   selection-chain step, sourced to the script lines, not in the C1 tool.

---

## 6. Host state observed (read-only, shape only)

- `~/.local/share/applications`: 71 entries, 0 symlinks, 0 non-regular files, 1 subdirectory → **the F1
  condition is not present today**, but the directory is user-writable, so it is one `mkfifo` away.
- `/usr/share/applications`: 121 entries; `/usr/local/share/applications`: absent.
- `~/.cache/xdg-terminal-exec`: 190 bytes, mtime `2026-10-26 17:42:25.200770484 -03:00`, sha256
  `f497ed057f8aaba24bea21ba652b810c6c2ab754b0b8fe9d9b1645e072a10cac` — restored to exactly this after this
  seat's slip (F2b). Its first line is a 32-hex key and it names the user-override `Alacritty.desktop` path.
  It is a *warm cache* and is exactly what F3 is about: no seat may delete or rewrite it, and no seat may let
  a run read it.
- The agent environment exports `XDG_CACHE_HOME=/home/vgpnk/.cache`; `w1-spec.json` mtime 18:42:56, `w1.ready`
  18:43:16 (so the wave started ~18:43; the cache's 17:42:25 mtime predates it, its 18:50:55 rewrite did not).
- `bwrap --unshare-all` rc=0 unprivileged; `kernel.unprivileged_userns_clone=1`; `yama/ptrace_scope=1`
  (children only). `strace -f` runs inside `bwrap` on this host (probe rc=0), and the 1-execve baseline was
  measured outside it — the counter should re-assert the count inside its own sandbox.

## 7. Receipts

| file | content |
|---|---|
| `receipts/cache-write.txt` | which print mode writes the cache; unset vs empty-value vs scratch dir |
| `receipts/stale-cache.txt` | warm vs cold `--print-cmd` over an edited entry (size+mtime preserved) |
| `receipts/fifo-hang.txt` | the captured `find` argv, the verbatim expression with/without a FIFO, rc table A–D |
| `receipts/hostile-files.txt` | loop / dangling / `/proc` link / FIFO / 50 MB tree; symlink escape with `--print-content` |
| `receipts/exec-argv.txt` | strace: spawned commands, write targets, userdb sockets, tripwire baseline |
| `receipts/builtin-exec.txt` | `Exec=cd` accepted; metacharacter `Exec` never executed |
| `receipts/locators.txt` | computed line numbers for every quote in this report |
| `receipts/seat-lines.txt` | seat → spec line map (41 items) |
| `receipts/grep-hits.txt` | token→spec-line locator table used for the inventory |
| `receipts/ambient-cache-env.txt` | `XDG_CACHE_HOME` inherited from the agent shell; proof that `HOME=<scratch>` does not redirect it |
| `receipts/host-cache-observed.txt` | the real cache, read-only, two observations (17:42:25 then an 18:50:55 rewrite) |
| `receipts/cache-restored.txt` | byte-identical restoration (190 B, sha, mtime) |
| `receipts/malformed-exec.txt` | `Exec=sh \| cat` and `Exec=sh %z` still select; `Exec=nonexistent-prog` does not |
| `receipts/gen-receipts.sh`, `receipts/gen-fifo.sh` | the generators, parameterised by a scratch dir argument (`$1`) |

Quotes of the resolver are ≤ 25 words each, located by `grep -n` in `receipts/locators.txt`
(`/usr/bin/xdg-terminal-exec:172, 173, 200, 201, 274, 303, 795, 1457, 1499`; `tools/mado-monitors.py:26, 113,
144`). The wave's own sentences are located at `w1-spec.json:3, 24, 39, 44, 49, 74, 79, 99, 154, 209`.
