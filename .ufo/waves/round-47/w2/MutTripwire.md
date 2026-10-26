# MutTripwire — round-47 w2 falsify seat — clause r (process/socket tripwire)

Status: DONE. 12 single-behaviour rare-path mutants of the frozen L1 reference, all scored with the untouched
frozen C1 counter at the freeze commit d7527d608ad2b2e3cc398fdde34db7947b254a1a (nonce 47; one nonce-variation
rerun). **4 survivors = a live clause-r hole; re-registration as v2 before any data commit can close it.**

## The hole

Clause r declares "strace around bwrap: no process and no socket after the sandboxed python3's execve"
(registration.md:36-37) and implements it as one strace expression over every tool run
(quality/counters/c1-r47-terminal.py:82 `TRACE_SET = "trace=execve,execveat,socket,socketpair,connect"`,
attached at :164, every post-execve line a trip at :174-196, `readonly` from trips at :456). **The trace set has
no fork-family syscall** (`clone`, `clone3`, `fork`, `vfork`). A tool can therefore create a real process inside
the sandbox — `os.fork()` or `multiprocessing.get_context("fork").Process(...)` — with no `execve`, no
`socket`: clause r prints `trips=0`, and if the child is silent the mutant is indistinguishable from the
reference on every clause. Verified in-sandbox, not inferred: replicating the counter's own Box.argv (same bwrap
flags and binds) with only the strace expression widened shows the M09 selftest run ending `43/43 passed`, rc=0,
with exactly one post-execve event — `clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|...|SIGCHLD, ...)` —
and 0 counter-visible events (receipts/diag-insandbox-M09.txt).

Declared w1 controls (registration.md "Controls") cover only exec/socket shapes (DELEGATE-SH, SUBPROC-EMBED,
EMBED-EXECV, CTYPES-EXECVE, SOCKET-AND-REF); there is no pure-fork control, which is why this survived the
control wave. Minimal detector closure: add `clone,clone3,fork,vfork` to TRACE_SET (one string,
c1-r47-terminal.py:82). Coverage finding, not a contract change — the contract already forbids process creation.

## Verdict matrix (counter verdict | clause-r trips | receipt)

| id | behaviour | rare path | verdict | trips |
|----|-----------|-----------|---------|-------|
| R0 | (pristine reference, harness sanity, nonce 47) | — | TARGET_MET | 0 |
| M01 | os.system(":") | --selftest | TARGET_MISSED (killed) | 1 `execve("/bin/sh",["sh","-c","--",":"])` |
| M02 | os.system(":") | plain `explain` | TARGET_MISSED (killed) | 190 |
| M03 | subprocess.run(["/bin/sh","-c","exit 0"]) | `print --print-cmd` | TARGET_MISSED (killed) | 645 |
| M04 | subprocess.Popen(same) | `explain --observed` | TARGET_MISSED (killed) | 330 |
| M05 | socket()+connect(127.0.0.1:1) | `print --print-cmd` | TARGET_MISSED (killed) | 1290 |
| M06 | socket()+connect | first accepted `[Desktop Action]` group | TARGET_MISSED (killed) | 46 |
| M07 | os.fork + os.execv(/bin/sh) | --selftest | TARGET_MISSED (killed) | 1 (the exec, not the fork) |
| M08 | os.fork + os.execv(/bin/sh) | plain `explain` | TARGET_MISSED (killed) | 190 |
| **M09** | **os.fork, child os._exit(0), no exec** | **--selftest** | **TARGET_MET (SURVIVED)** | **0** |
| **M10** | **os.fork, no exec** | **`print --print-cmd`** | **TARGET_MET (SURVIVED)** | **0** |
| **M11** | **multiprocessing fork-context Process** | **plain `explain`** | **TARGET_MET (SURVIVED)** | **0** |
| **M12** | **multiprocessing fork-context** | **100th in-process case run of --selftest** | **TARGET_MET (SURVIVED)** | **0** |
| R1 | = M10, nonce 90210 | `print --print-cmd` | TARGET_MET (SURVIVED) | 0 |

Reading: every exec-bearing and socket-bearing mutant is killed by clause r in every tested rare path — the
tripwire works for what its trace set names. Process creation without exec is invisible in every path; the
survivors include the plain `--selftest` path and the hottest path (`--print-cmd` parsing), so this is not a
corner-case coverage gap but a blind spot of the detector itself. The surviving mutants pass selftest 43/43,
fixtures 190/190, explained 190/190, generated 150/150, `trips=0`, exit 0.

Rare-path notes: fixtures whose args use `--print-cmd`: 154/190; fixtures holding a `[Desktop Action ...]`
group: 10/190 (receipts/fixtures-evidence.txt) — so the print-cmd and action triggers demonstrably fire inside
counter runs (M03/M05/M06/M10 trip counts are those firings). The 100th-run flavour is implemented as the 100th
in-process case run (M12): cross-invocation state is impossible in this counter because every tool run gets a
fresh tmpfs /tmp and a per-case `--bind` root, so no 100th-invocation mutant can be built that still fires in
the sandbox.

## Mutant construction (smallest behaviour-bearing point)

Each mutant = one module-level `_mut()` helper (the single forbidden behaviour, every exception swallowed) plus
one call at one trigger site; nothing else changes (per-mutant diffs in receipts/Mxx.diff, 7-15 added lines;
regenerate deterministically with `python3 -I .ufo/waves/round-47/w2/MutTripwire/make_mutants.py`; sha256 per
mutant in receipts/manifest.json). Firing + behaviour preservation were verified per mutant before scoring
(receipts/probes.json): each mutant FIRES its syscall at its trigger (host strace with
execve,execveat,clone,clone3,fork,vfork,socket,socketpair,connect) and its stdout+rc are byte-identical to the
reference on the same input (root-normalized). Key sites: M09 fires at mutants/M09-fork-only-selftest-start.py:992
(fork at :1021, helper :1019); M11 guard at mutants/M11-multiprocessing-explain-plain.py:849, Process at :1023;
M12 threshold at mutants/M12-multiprocessing-selftest-100th.py:1000.

## Reproduction (one survivor, end to end)

```
S=/fast/scratch/hyaku/mado-r47/MutTripwire   # honour the scratch directive
D=$(mktemp -d -p "$S"); mkdir -p "$S/w"
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
cp .ufo/waves/round-47/w2/MutTripwire/mutants/M09-fork-only-selftest-start.py "$D/tools/mado-terminal.py"
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand
python3 -I quality/counters/c1-r47-terminal.py --repo "$D" --rev HEAD --work "$S/w" --nonce 47
# -> ... clause=r trips=0 ... fixtures=190/190 explained=190/190 generated=150/150 selftest=ok
#    readonly=ok tool=present verdict=TARGET_MET ... exit 0
```

## Restoration evidence

- Reference bytes before the first run and after the last run:
  sha256 762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08 both times (verified again post-run);
  the reference was never a mutation target — mutants were built from copies in .ufo/waves/round-47/w2/MutTripwire/mutants/.
- No tracked lane file touched (`git status --porcelain` shows only the untracked seat dir + this report);
  all scoring clones lived under /fast/scratch/hyaku/mado-r47/MutTripwire and were removed per run
  (`trap 'rm -rf -- "$D"' EXIT`); scratch dir deleted at seat close.

## Bounds respected

- No pacman transaction, no host service/compositor mutation, no GUI/terminal launch; the pinned resolver was
  never run by this seat (the counter runs it in bwrap; my probes run only our tool).
- xdg-terminal-exec: not invoked directly at all; XDG_CACHE_HOME in probes pointed into the scratch tree.
- Empty argv elements never passed to anything; all scratch writes bounded (probe trees are KBs; no `find ~`,
  no host config reads beyond the counter's own).
- Seat is a leaf: no subagents, no spawned background jobs (two bash calls were auto-backgrounded by the
  runtime at their deadline; both completed serially, ≤2 counts in flight).
- Tooling installs: none (bwrap/strace/git/python3 already present; no tool recorded per the RULES.md ledger).
- Scratch /fast/scratch/hyaku/mado-r47/MutTripwire deleted on seat close; nothing citable lives there — all
  evidence is in this seat dir.

## Artifacts

- Receipts (counter stdout + exit per scored run): receipts/R0-pristine.txt, M01..M12 receipts, R1-M10-nonce90210.txt
- Mutants + provenance: mutants/ (12 files), receipts/manifest.json (sha256, trigger sites), receipts/Mxx.diff
- Probe evidence: receipts/probes.json (firing + stdout equality + counter-visibility per mutant)
- In-sandbox diagnostic: diag_insandbox.py, receipts/diag-insandbox-M09.txt
- Harnesses: make_mutants.py, probe_mutants.py (deterministic; re-run to reproduce everything above)
