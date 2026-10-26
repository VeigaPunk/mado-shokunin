# CritClaimSizing — cheap-pass survey of the C1/C2 predicates (round-47 w1)

Seat: CritClaimSizing (leaf; no subagent dispatch). Purpose: attack the declared C1/C2
predicate designs for cheap passes, before the L1 freezes the instruments in `registration.md`
after this wave. Inputs: `round-47/claims.md` (declared claims, lines 10-17) and the draft
contract/judge text in `w1-spec.json:3`. Every quoted clause fragment below is from those two
files, located inline.

Axes named (godspeed): (A) C1 judge fidelity — the judge must actually discriminate a faithful
implementation from a cheap one; (B) C2 sourcedness — the entry must be earned, not quoted;
(C) freeze robustness — every recommendation lands as a registrable clause, not prose.

---

## 1. C1 — cheapest tools that meet the contract without the capability

The contract's integrity clauses are: "re-implements, in Python 3 stdlib only and WITHOUT
starting any process or opening any socket, the selection" (w1-spec.json:3); judge = real pinned
script, side-by-side in a bubblewrap sandbox, ">= 100 pinned fixtures plus >= 150 nonce-generated
cases", "identical stdout + exit status", tripwire "strace -f execve count, and fake binaries
bound over /usr/bin/xdg-terminal-exec and the shells" (w1-spec.json:3).

### 1.1 Exec-through (wrap the real binary)
Cheapest: `mado-terminal.py` execs `/usr/bin/xdg-terminal-exec` (or invokes a bundled copy via
`sh`), passing args through. Byte-identical everything by construction.
Stopped by: "WITHOUT starting any process or opening any socket" (w1-spec.json:3) + tripwire
(execve count; fake binaries over the real script and the shells) (w1-spec.json:3). **Stopped.**
Only wording suggestion: "starting any process, by any API (subprocess, os.exec*, posix_spawn,
ctypes/libc calls)" so dynamic loading cannot route around the strace tripwire.

### 1.2 Vendored script + tiny POSIX-sh interpreter in pure Python
Cheapest *correct* tool: embed the byte-equal pinned script and execute it with a small shell
interpreter written in Python 3 stdlib (the script uses arrays, parameter expansion, `case`,
external `tr`/`find -L`/`awk` semantics — reimplement those three in stdlib too, or use
`posix` calls; all in-process). No process, no socket, stdlib-only => satisfies every letter of
the contract, and because it runs the pinned program it is byte-identical on every fixture and
every nonce, forever. To the question "is that an implementation?": yes — it is the *strongest*
implementation (it holds the full selection algorithm), which is exactly why it is not cheap in
effort but is instant in correctness and makes the whole oracle pointless.
Which clause stops it: **none**. "Re-implements ... the selection" is satisfied by vendoring;
the anti-wrapper clauses don't reach in-process interpretation.
Proposed clause (if independent authorship is wanted): "the tool must not contain the pinned
script or a byte-level transcription of it (verbatim source, token stream, or contiguous runs of
its text longer than 40 chars, excluding standard XDG variable/option names); the selection logic
must be authored in Python for this round." Enforceable statically (longest-common-substring vs
the pin). Alternative: declare it a permitted residual explicitly. Either way, decide at freeze;
silence leaves a loophole whose exploit costs nothing at judging time.

### 1.3 Lookup table keyed by a hash of the case
Cheapest: hash (env + file tree + argv) -> embedded table -> output.
Stopped by: the corpus includes ">= 150 nonce-generated cases" (w1-spec.json:3) — if nonces are
genuinely fresh and unpredictable, precomputation cannot cover them. But the text does not say
they are fresh, secret, or wide: a deterministic seeded generator described in the counter is
precomputable by a submitter who learns it (and the counter lives in-repo). **Not fully stopped.**
Proposed clause: "nonce cases are generated at judge time with a fresh CSPRNG seed not published
before the run; file names, ids, paths, env values and argv are drawn from ranges too wide to
enumerate; the counter must not reuse a seeded corpus between judging runs." Belt: static
inspection banning embedded case→output or hash→output maps.

### 1.4 Read the expected answer at run time (exfiltration)
Cheapest: fixtures carry `expect` (rc + stdout) in the manifest; the oracle runs side-by-side in
the same sandbox. The tool can (a) locate and read the fixture manifest (it is in the repo, and
the repo may be visible), (b) read the oracle's redirected stdout, (c) read the oracle's cache
under XDG_CACHE_HOME after it ran, (d) read sibling `/proc/<pid>/fd/*` — and echo `expect.stdout`
with the right rc. This yields identical stdout + exit status on 100% of cases with zero selection
logic. It can even do it lazily/robustly: try the manifest first, fall back to a real
implementation if hidden.
Which clause stops it: **none**. "Read-only" permits reads; "no socket" bans sockets only; the
judge description specifies no visibility or ordering. **This is the single largest hole in the
freeze.**
Proposed clause (three-pronged):
1. Ordering: "the counter runs the tool before the oracle on every case; expect records are
   produced after the tool's run and are never readable by the tool."
2. Visibility: "the tool's sandbox exposes only the materialized case ($ROOT tree, stub
   executables, environment) and the Python stdlib; the lane repo, the counter, the manifest,
   the oracle process and its outputs, and any other case are invisible."
3. Reads: "the tool must open no file outside the set the pinned script itself opens for the
   same case (openat-audited like the execve tripwire), and must treat XDG_CACHE_HOME as a
   private empty dir — never the oracle's cache."

### 1.5 Hardcode the host answer
Cheapest: always print `Alacritty.desktop` / `alacritty` / the host override path (host facts,
L1, 2026-10-26).
Stopped by: equality is "in the same environment" (w1-spec.json:3), and fixtures parameterize env
— any non-host env mismatches. Stopped *only insofar as* the suite actually varies env and
expects non-host answers. Add explicitly: "the fixture suite must include at least one case
resolving to a system (non-user) entry, at least one NO_TERMINAL case, and cases under at least
two different XDG_CURRENT_DESKTOP values including unset; nonces must vary XDG_CONFIG_DIRS /
XDG_DATA_DIRS ordering."

### 1.6 Shallow approximation (dominant-path algorithm)
Cheapest approximator: "first TerminalEmulator in the first data dir whose TryExec is on PATH",
or a hand-rolled partial emulation. It passes every case the corpus does not probe.
Stopped by: nothing structural — the judge only samples; I/O equality on the corpus blocks it
only if the corpus touches every divergent branch. The schema has a `class` field (w1-spec.json:3)
but the spec never demands coverage of the documented edge classes.
Proposed clause: "the pinned fixtures and nonce generator must together exercise every branch of
the pinned script that changes output: per-DESKTOP list-file order and fallback, per-data-dir ID
precedence, Hidden, NoDisplay, OnlyShowIn/NotShowIn, Type≠Application, absent/off-PATH TryExec,
empty Exec, Actions, X-TerminalArg* keys, %-argument composition, --print-cmd[=seq],
--print-delimiter=seq, --dir/--title/--app-id/--hold, nonexistent --app-id, duplicate IDs,
unset XDG vars, PATH without candidates, and argv quoting." (Material for the matrix is already in
the lane: upstream script and README under `ScoutSpecs/pins/` and `ScoutScriptMap/`.)

### 1.7 Explain: the "why" is unverifiable
Explain has no oracle counterpart; the judge never reads traces. Cheapest: a canned plausible
rejection narrative plus a self-declared `MADO_TERM` line; exits 0/2/3 are trivially
reproducible. Without `--observed` nothing distinguishes it from a real trace; with `--observed`,
only the verdict line is compared, and a tool can always read the observed capture and echo AGREE.
Which clause stops it: none (the verdict is self-reported; `--observed` defines AGREE as "equal",
not as "computed honestly").
Proposed clauses:
1. Consistency: "on the same environment, explain (without --observed) must report the same
   selected id and path as print; both must be deterministic across runs."
2. Oracle-checked explain: "the counter runs `explain --observed <capture>` on every fixture and
   nonce and requires verdict=AGREE and exit 0."
3. Trace playback: "every list-file:line cited in a trace must exist in the corresponding list
   file for that case and must contain the cited entry; every rejection reason must be compatible
   with that entry's attributes."

### 1.8 Selftest padding
Cheapest: 30 trivial hermetic cases (empty env ⇒ NO_TERMINAL) or duplicated cases print "30/30
passed".
Which clause stops it: none — ">= 30 hermetic cases built under $TMPDIR" (w1-spec.json:3) counts
lines, not behavior (round-46 already declared its selftest clause a printed line,
round-46/registration.md:38-39).
Proposed clause: "selftest cases must cover the same behavior matrix as the fixtures (≥1 per
class), must include at least one knowingly-failing assertion (the suite must be able to fail),
and N must equal the number of distinct case ids."

### 1.9 Shared-cache contamination
If tool and oracle share XDG_CACHE_HOME, the oracle warms the cache the tool must model cold, and
the tool can read it (1.4). Conversely the tool's own cache write could warm the oracle's later
run. Proposed clause: "tool and oracle receive distinct, initially-empty XDG_CACHE_HOME
directories; neither may observe the other's cache; cache contents are out of contract in both
directions."

---

## 2. C2 — cheapest entries that "close" the claim

### 2.1 Quote the pins, state no chain
Cheapest entry: rows citing the pinned script tag, README and host facts; "the chain" described at
documentary level (list files consulted in order, override precedes system entry); the r17 [UNK]
(terminal-route-r17.md:144-145) declared closed by that precedence; nothing executed.
Which clause stops it: partially. "rows S326.. opened this round" (claims.md:16) / "SOURCES rows
S326.. opened this round" (w1-spec.json:3) bind rows; "closing ... with a live, read-only host
observation" (w1-spec.json:3) demands an observation — but the L1-provided host fact is already a
recorded print-mode run, and the entry could cite that fact as "the observation" without performing
it. **Not fully stopped.**
Proposed clause: "the observation must be reproduced in this round by the entry's author: the
entry must show the exact command line (with XDG_CACHE_HOME redirected), the environment, the
sha256 of a saved receipt, and the quoted output; the counter must replay the command and compare
bytes. A reused or second-hand observation does not close the [UNK]." Scope note: launch is banned
(host safety), so the closure must be worded "selection-time (print mode), not terminal spawn" and
must quote the UNK sentence and state that scope.

### 2.2 Fabricated or unevaluated chain detail
Cheapest: assert per-DESKTOP list order, data-dir precedence, validation keys, actions, exec-arg
composition, print modes and cache behavior from the README/manpage or intuition, with loosely
chosen script-line citations.
Which clause stops it: none stated; round-46's residual only bound a locator and a keyword per
surface, "not the truth of the sentence" (round-46/registration.md:57).
Proposed clause: (a) anchor every asserted behavior to a source that actually contains it (`script:NN`
line, manpage page, or observation receipt); (b) cross-check the entry's chain claims against the
C1 fixture oracle: for the env families the fixtures cover, the entry's stated selection order must
agree with the script's observed selection on the matching cases. (b) reuses C1's machinery at
zero marginal oracle cost.

### 2.3 Re-claim held ground
Duplicate or restate `terminal-route-r17.md` (documentary route, S056-S060), `terminal-trees-r23.md`
or `terminals-and-omarchy.md` content.
Which clause stops it: the claims text lists the held ground (w1-spec.json:3) but provides no
mechanic. Proposed clause: "the counter rejects sentences that substantially repeat
terminal-route-r17.md / terminal-trees-r23.md / terminals-and-omarchy.md (locator overlap or
phrase near-duplication)," mirroring the round-46 R4 supersession checks.

---

## 3. Residuals the freeze should declare
- Carry-over: sandbox-detection — a tool may detect it is sandboxed by means the judge does not
  vary, and the round-46 freeze accepted that residual (round-46/registration.md:36-37). If the L1
  wants it closed here, vary the sandbox between runs (mount layout, pid namespace, visible paths);
  else declare it again.
- New: the oracle is the real pinned script, so the round-46 "contract error shared by reference
  and tool" residual disappears (there is no reference of ours). A *new* residual appears instead:
  the judge sees only I/O, never method, so clauses 1.3/1.6/1.7 must be frozen as hard requirements,
  not good intentions.
- New: "no process / no socket" and "Python 3 stdlib only" are anti-wrapper clauses, not
  pro-fidelity clauses; they do not by themselves make a faithful implementation.

## 4. Priority for the freeze
1. 1.4 exfiltration (ordering + visibility + openat audit) — the only attack that is both
    zero-effort and 100% effective today.
2. 1.2 vendoring decision (clause or declared residual).
3. 1.3 nonce freshness + anti-table static check.
4. 1.6 behavior-matrix fixture/nonce mandate.
5. 1.7 explain checks (consistency + oracle-checked + playback).
6. 2.1 observation reproduction (this-round receipt, replay).
7. 1.8 selftest substance; 1.9 cache separation; 2.2 anchoring/cross-check; 2.3 hold-ground reject
    mechanic.

No tools installed; no scratch used; no host process run; nothing outside this seat's report files
was written.
