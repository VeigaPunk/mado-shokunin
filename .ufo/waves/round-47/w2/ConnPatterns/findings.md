# ConnPatterns — round 47 w2 findings: round-46 break classes vs round-47 freeze

Seat: ConnPatterns (w2, FALSIFY). Lane: mado-shokunin. Freeze `d7527d608ad2b2e3cc398fdde34db7947b254a1a`
(base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`). Source of the break classes: round-46 `registration-v2.md` /
`registration-v3.md` and their w1 reports (`CritC1Cheat.md`, `SentTool.md`, `CritC2Forgery.md`).

Every `file:line` below was computed with `grep -n` (never typed); every quoted fragment is <= 25 words and
present verbatim in the cited file. All scores were re-run on this host by this seat (receipts in `receipts/`).

---

## Verdict at a glance

| round-46 break class | round-47 analogue | closed? |
|---|---|---|
| C1 ambient reference copy (CritC1Cheat A/C) | delegator/embed controls DELEGATE-SH, SUBPROC-EMBED, EMBED-EXECV, CTYPES-EXECVE | **yes** (minimal bwrap root; pin mounted only in oracle runs; embedded-in-process copy is the declared-section, not a cheat) |
| C1 deletable marker (CritC1Cheat B) | none — clause r has no marker file; strace trace lives outside the sandbox | **yes** (mechanism removed; fail-closed keys exist) |
| C1 absolute-path binaries (CritC1Cheat B, SentTool F2) | `/usr/bin` is not mounted at all; selftest shares the sandbox PATH | **yes** (stronger than v2: no `/usr/bin` exists inside) |
| C1 inherited pipe (v3: TRIP-ABSOLUTE-PATH / TRIP-SELFTEST-ONLY met) | none — no in-band tripwire channel; clause r is external strace | **yes** (mechanism removed) |
| C2 self-receipt (F7) | clause f receipts must be **absent at base** → authored with the data revision | **partly** — open inside the predicate; closed only by the declared non-author closure |
| C2 uncited pinned rows (F5d) | HELD S056-S060 byte-equal; but new uncited rows are invisible | **no** — demonstrated (admitted=1/1 with falsified uncited S339) |
| C2 indented code (F8) | no check for unquoted code blocks | **no** — demonstrated (admitted=1/1 with invented indented code) |

---

## C1 — operability (tools/mado-terminal.py)

### 1. Ambient reference copy — CLOSED
Round-46: a 12-line delegator execs a copy of the reference found under `/fast/scratch`; the sandbox exposed `/fast`
(`CritC1Cheat.md:11-16`). Round-47: the bwrap root is minimal — only `/usr/lib`, bash at `/bin/sh`+`/bin/bash`,
`/oracle/bin`, `/dev`, `/proc`, tmpfs `/tmp`, the fixture root and its `.rw` (`c1-r47-terminal.py:139-148`). The
scratch, the lane and `/fast` are not mounted; env is cleared (`--clearenv`). The oracle pin is bound **only** on
oracle runs (`c1-r47-terminal.py:148`), never on tool runs (`:146`). Controls DELEGATE-SH / SUBPROC-EMBED /
EMBED-EXECV / CTYPES-EXECVE (all embed or exec the reference) all MISSED, `readonly=fail`
(`receipts/ctl-c1.txt:5-10`). Closed.

Nuance: an **in-process** interpreter of an embedded copy is unstoppable by clause r — and is declared legitimate:
registration.md:52-53 "a tool carrying a model of the resolver (an emulator, or a Python interpreter for an embedded
copy of the script) is an implementation of it". I verified the boundary: a tool that `os.fork()`s a child (which
`_exit(0)`s) and then runs an embedded copy of the reference via `runpy.run_path` scores `TARGET_MET`,
`readonly=ok`, `trips=0` (`receipts/c1-fork-runpy.txt`). That is expected under the residual; it is reported here
because it doubles as evidence for the clause-r gap in class 4 below.

### 2. Deletable marker — CLOSED
Round-46: the `r` tripwire was a marker file inside the tool's writable bind; the tool unlinked it
(`CritC1Cheat.md:19-20`). Round-47: there is no marker file. Clause r = strace syscall trace written to a file in
the counter's work dir (outside the sandbox, not mounted); strace owns the fd. There is no in-sandbox artifact to
delete. Fail-closed keys exist: `trace-missing` (`c1-r47-terminal.py:178`) and `python-execve-not-seen` (`:194`).
Closed.

### 3. Absolute-path binaries — CLOSED
Round-46: `/usr/bin/hyprctl` by absolute path reached the real binary (SentTool F2). Round-47: `/usr/bin` is not
mounted at all (only `/usr/lib`; `c1-r47-terminal.py:140`), so `/usr/bin/<name>` is ENOENT. The selftest also runs
in the same sandbox with `PATH=/oracle/bin` (`c1-r47-terminal.py:392-396`), not on a host PATH — the
round-46 "bare hyprctl during --selftest" route has no target here. Closed (harder than v2, which still bound
`/usr`).

### 4. Inherited pipe — CLOSED, with a fork-shaped caveat
Round-46 v3: the tripwire was an inherited pipe; the tool's `subprocess.run` closed inherited fds, so the fake binary
could not report (`registration-v3.md:5-6`). Round-47: no pipe, no fake binary, no first-band channel — clause r is
external `strace -f` around the whole sandboxed tool. Nothing the tool closes can mute it. Closed.

Caveat: the trace set is `trace=execve,execveat,socket,socketpair,connect` (`c1-r47-terminal.py:82`). It does not
count `clone/clone3/fork/vfork`, so a pure-Python child process (fork, no execve) is invisible to `r`. ExecStraceTrip
measured exactly this and recommended counting process clones (`w1/ExecStraceTrip.md:21-23`, `:95`); the frozen counter
dropped that part. Demonstrated by my fork+runpy run: `readonly=ok` with a real fork (`receipts/c1-fork-runpy.txt`).
Scoring consequence today: none, because embedding is already declared legitimate (class 1 nuance). It is still a
wording gap: the docstring claims "no process after the sandboxed python3's execve" (`c1-r47-terminal.py:36`), which
the trace does not enforce. If the next round wants "no process" to be true, add clone/fork without `CLONE_THREAD`
(as ExecStraceTrip's P2).

---

## C2 — coverage (corpus/knowledge/xdg-terminal-selection-r47.md)

### 5. Self-receipt (F7) — analogue present; closed only by the declared non-author closure
Round-46 F7: the scored revision wrote its own live receipt under `receipts/` and cited it; the counter read cited
receipts "at REV" (`CritC2Forgery.md:16-18`). Round-46 v2 closed it mechanically with clause k: cited receipts
byte-equal at the freeze commit (`registration-v2.md:67-69`).

Round-47 clause f takes the opposite design: the receipt must be **absent at base** (`c2-r47-terminal-entry.py:577-579`
`receipt_present_at_base` fails) — i.e. it is authored with the data revision. The counter checks form only:
`resolver_sha256=` (the v0.14.3 digest), `observed=` path, >= 3 `XDG_*` lines, first observed line `.desktop`,
second absolute path, and the entry line stating id+path (`:584-608`). Nothing checks who produced the capture or
that it predates the data commit. Closure is the declared residual: registration.md:76-78 "a capture can be typed
rather than produced by the resolver (the counter checks its form and digest line; the non-author closure re-runs the
print command)". The positive control itself demonstrates the mechanism: build-control.py writes the receipt in the
same commit as the entry (`ctl/c2/build-control.py:302-324`, `:339-341`) and the counter admits it
(`receipts/pos-score.txt`). So: analogue present, open inside the predicate, closed only by the external reading —
exactly the boundary the registration declares. Not a hole, but it is a *weaker* mechanical posture than v2's
freeze-bytes check.

### 6. Uncited pinned rows (F5d) — OPEN (demonstrated)
Round-46 F5d: a falsified *uncited* row on a pinned URL was admitted because clauses walked only cited ids
(`CritC2Forgery.md:71-82`). Round-46 v2 closed it with fix E ("a registry row the entry never cites is byte-identical
to its base row") and F ("every registry row born at REV is cited") (`CritC2Forgery.md:135-136`).

Round-47: clause h protects the five pre-existing pinned rows — S056-S060 byte-equal at base and REV
(`c2-r47-terminal-entry.py:646-654`; at base only S056/S057 carry the vladimir-csp URL — computed `grep`). But:
- clause b walks only the provenance-head ids (`c2-r47-terminal-entry.py:696-699`, `:710-711` `ghosts = cited - set(reg_rev)` — one-directional: cited must exist, new-uncited never checked);
- there is no "every row born at REV is cited" check (round-46 fix F is absent);
- no clause inspects the anchor/scope of an uncited row.

Demonstration: on top of the admitted POS control I appended an uncited falsified row S339 using the **same pinned
README URL** as S327/S056, with a scope sentence contradicting S327 and an anchor range beyond the pin's line count
(`README.md:1-99999`). The counter still reports `admitted=1/1 TARGET_MET`
(`receipts/uncited-row-s339.txt`, rev `9924b239...`). Reproduce: build the POS control, append that row after S330,
commit, score.

Concrete draft surface: the w1 rows draft registers S326-S338 (`w1/ScrRows/rows.md`), while the entry draft head
cites only S326/S327 (`w1/ScrEntry/entry.md:3-4`). Unless the landed entry cites all rows it registers, 11 rows
(S328-S338) would land uncited and unchecked.

### 7. Indented code (F8) — OPEN (demonstrated)
Round-46 F8: two 4-space-indented invented C++ lines in no pin were admitted (`CritC2Forgery.md:100-113`); v2
closed it with fix D ("a 4-space-indented code run must occur verbatim in a pin").

Round-47: clause d sees only quoted spans carrying an adjacent locator (`QUOTE_RE`, `c2-r47-terminal-entry.py:142-144`,
scan at `:486-514`). Unquoted indented lines are matched by nothing — no clause, no residual statement (registration.md:76-78
names quotes, not code). Demonstration: I appended two invented 4-space-indented C++ lines to the admitted POS entry;
the counter still reports `admitted=1/1 TARGET_MET` (`receipts/indented-code-f8.txt`, rev `5143ff6e...`). The
current entry draft contains no such block, so the hole is latent — it becomes real the moment the landed data carries
any unquoted code/command sample (e.g. a shell snippet in the live section).

---

## What is NOT broken (checked, not assumed)

- C1 CLI controls: 28/28 MISSED + REF MET (`receipts/ctl-c1.txt:30`), including the round-46 cheat shapes
  (DELEGATE-SH, SOCKET-AND-REF, CTYPES-EXECVE).
- C2 control set: POS admitted; N-BASE/QUOTE/BRANCH/HELD/RECEIPT/NOSTEPS/OBS/NOSHA/RANGE/PIN all reject on their
  intended clauses (`receipts/ctl-c2/ctl-summary.txt`).
- Clause h holds: moving S056 is rejected (N-HELD) — the pre-existing pinned-rows subset is protected.
- C1 sandbox exposes no `/home`, `/fast`, lane, scratch, or `/run`; no live compositor socket is reachable
  (no `/run/user` mount), so the round-46 F1 AF_UNIX socket reachability has no analogue.

## Reproducible commands

C2 demonstrations (needs `C2R47_WORK` = scratch holding `pins/xdg-terminal-exec-0.14.3/` = the tag tarball
`https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3`, sha256
`82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe`):

```
export C2R47_WORK=<scratch>
python3 -I <lane>/.ufo/waves/round-47/ctl/c2/build-control.py
python3 -I <lane>/quality/counters/c2-r47-terminal-entry.py --repo $C2R47_WORK/ctl --rev HEAD      # POS, 0
# then append the S339 row (receipts/uncited-row-s339.txt) or the indented block (receipts/indented-code-f8.txt),
# git add -A && git commit, and score again — still 0.
```

C1 fork demonstration (one count, ~60 s, nonce 1):

```
D=$(mktemp -d -p <scratch>); git clone -q --shared --no-checkout <lane> "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
# cp wrapper (os.fork()/_exit(0) + embedded ref via runpy.run_path) to "$D/tools/mado-terminal.py"
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand
python3 -I <lane>/quality/counters/c1-r47-terminal.py --repo "$D" --rev HEAD --work <scratch>/w --nonce 1
```

## Safety compliance
All clones in `/fast/scratch/hyaku/mado-r47/ConnPatterns/` (deleted at finish); no lane file modified; no mutating
git in the lane; no host service/compositor contact; no pacman; xdg-terminal-exec never run without `--print-*` and
never with a host cache (`XDG_CACHE_HOME` inside scratch). Tools installed: none (curl/git/bwrap/strace already on
host).
