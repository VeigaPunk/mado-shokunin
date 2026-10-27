# SentHostState50 — can a frozen round-50 instrument write host state? (w2, round 50)

author: seat `SentHostState50` (leaf, no dispatch), mado round 50 w2, 2026-10-27.
attack revision: `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip), cloned with `git clone -q --shared` into my scratch;
every counter/instrument run below ran against that clone, never in the lane tree.
target: **no committed round-50 instrument can write host state; the outer-tracer false-miss trap (R-SHS-3)**.
receipts beside this file under `receipts/`; every locator is `grep -n`/`sed -n` computed; `~` is the home directory.

## Verdict

**SUPPORTED for the clean paths of all seven instruments; three residuals, two of them writes outside any refusal set
(low severity, none reaches a ledgered operator path on the frozen commands).**

- The seven landed instruments carry **9 write surfaces and 6 exec surfaces, and zero `socket()`/`connect()` calls**
  (`receipts/containment-table.txt`, one row per surface with its locator; a repo-wide grep for `socket.|connect(|urllib|http.client|requests`
  over all seven files returns nothing).
- Six of the seven write **only** under a caller-supplied root that is refusal-checked at admission. The one exception is the
  gate's `cat-file` request list, which uses the ambient temp dir with no refusal (`quality/check-session-material.py:975`).
- **R-SHS-3 cannot recur in the two counters**: neither `PRED-C1-r50` nor `PRED-C2-r50` starts a tracer or a bwrap namespace
  (`receipts/tracer-nesting.txt`: `strace|bwrap|TracerPid|ptrace` → no match in either file), so an outer tracer is never
  nested. The round-49 mechanism (a counter that ran `strace … bwrap …` itself) is gone from the round-50 code, not merely
  worked around.
- The one documented ambient read is real and read-only: `PRED-C1-r50` clause r replayed the pinned capture at the attack
  rev — `clause=r replay=ok sha=9a47199e2297 binds=192 … resolve=0` — and the live control `hyprctl version` answered
  (`receipts/c1-live-clause-r-and-control.txt`). The child's `HOME`/`XDG_*` are a fresh scratch dir
  (`quality/counters/c1-r50-bind-entry.py:1075-1080`); only `XDG_RUNTIME_DIR` and `HYPRLAND_INSTANCE_SIGNATURE` are inherited
  (`:1071-1074`), which is what the Unix socket needs.

## Verdicts by instrument

| instrument (bytes at `b4a79843`) | writes | exec | socket | confinement verdict |
|---|---|---|---|---|
| `quality/counters/c1-r50-bind-entry.py` `e162d671…a84c0` | `mkdtemp(prefix="c2r-", dir=tmp_root())` `:1075`, five `HOME`/`XDG_*` dirs under it `:1077-1080`, `rmtree` in `finally` `:1120` | `/usr/bin/hyprctl binds -j` `:1081`, `getoption` `:1107` (absolute path, no PATH lookup `:1126`); `git show|rev-parse|ls-tree|grep` `:214-236,384,950,1017-1030` | none opened; hyprctl is the consumer | **confined to TMPDIR**, scratch `HOME` for the child; refuses `TMPDIR` under `/tmp`,`/var/tmp`,`/dev/shm`, inside the repo, and an absent `TMPDIR` (`:1054-1073`, measured); **no home rule** → F1 |
| `quality/counters/c2-r50-session-gate.py` `1d52a62c…b298` | `--work` mkdir `:435`, gate copy `:444`, fixture repo `open(...,'w')` `:318`, `rmtree` `:479,:561` | `python -I <gate>` `:253`, `git` `:223` — every child gets `child_env(work)` `:197-212` | none | **confined to `--work`**; `--work` and inherited `TMPDIR` refused under the `/tmp`,`/var/tmp`,`/dev/shm` family and under the invoking home (`:419-433`, measured) |
| `quality/check-session-material.py` (v3) `ffdc9d62…b61` | `NamedTemporaryFile("wb", delete=False)` **with no `dir=`** `:975` → unlinked `:1008`; selftest `mkdtemp(TMPDIR or None)` `:2078`; selftest fixture repos `:1517-1528` | `git cat-file --batch` `:980`, `git` `:924` (read-only verbs), `hyprctl monitors all -j` only under `--serial-from-host` `:631,:2106` | none opened; hyprctl is the consumer | **read-only scan; one write per scan into the ambient temp dir, no refusal set → F2** |
| `quality/check-wave-done.py` `10f4359a…18c` | `mkdtemp(prefix="wave-done-selftest.", dir=real)` `:542`, fixture tree `:551-582` | `git rev-parse|show|ls-tree` `:187-226`, self re-invocation `:923-933` with `HOME=<work>/child-home` `:615-616` | none | **confined to `--work`**; refuses the `/tmp`,`/var/tmp`,`/dev/shm` family, `$HOME` **and** the passwd home, absent `HOME` is an error (`:504-539`, measured) |
| `tools/mado-hostguard.py` `fdaa5c2e…b47e` | `--work` + `home`/`XDG_*` dirs 0700 `:303-309`, selftest root `:1124` | `Popen(..., start_new_session=True)` `:386`, `killpg(SIGKILL)` on timeout `:396-403`, `bwrap` only with `--sandbox bwrap` `:315-378` | none | **confined to `--work`**; refuses the `/tmp`,`/var/tmp`,`/dev/shm` family, operator home (passwd), its own repo (`:151-168`); `--env-keep`/`--env-set` on a managed name refused (`:286-295`) |
| `quality/check-state-cite.py` `822912fc…8c` | **none** — `open(...,"r")` only `:72,:94,:121`, `glob` | none | none | read-only |
| `quality/check-deliverables.py` `6fe0a4b4…88f` | **none** — `open(...,"r")` only `:125` | `git show`, `git cat-file -e` `:94,:113` | none | read-only |

All seven digests recomputed at the attack rev equal the freeze table (`receipts/instrument-pins.txt`).

## Live probes (no tracer — R-SHS-3 says a wrapped counter reports a false miss, so I did not wrap any)

1. **Full `PRED-C1-r50` run** at the attack rev, `TMPDIR=<scratch>/tmp-c1`:
   `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET`, rc 0, 0.8 s; **0 entries** left in
   the scratch afterwards. Clause r is the ambient-read surface and it replayed byte-equal.
2. **Positive proof the c1 scratch is created inside `TMPDIR`** (not adjacent to it): with `TMPDIR` at mode 500 the run fails
   in `mkdtemp` with `PermissionError: … <scratch>/ro-c1/c2r-k83yb5sb`. So the `c2r-*` tree, its five `HOME`/`XDG_*` children
   and every file the child sees are under `TMPDIR`.
3. **Gate scan on the clone** with a writable `TMPDIR`: `SESSION_MATERIAL: files=23920 findings=235 rev=b4a79843…`, and the
   clone is still clean (`git -C <clone> status --porcelain` → 0 lines). The gate writes nothing into the scored repo.
4. **Live control, the only allowed host read**: `hyprctl version` → `Hyprland 0.56.2 … commit efb50993…` (one read-only verb;
   no dispatch/keyword/reload/setprop/output/batch was issued in this seat).

## Findings

### F1 (low, open) — `PRED-C1-r50` accepts a `TMPDIR` under a home: R-SHS-2 is only half-remediated

- **What it attacks**: `quality/counters/c1-r50-bind-entry.py:1054-1073` (`tmp_root()`). Its refusal set is `/tmp`,
  `/var/tmp`, `/dev/shm`, an absent `TMPDIR`, a non-directory, and a `TMPDIR` inside the scored repo. There is **no home
  rule**, although the docstring `:123-127` claims "a scratch HOME/XDG_* set (never the operator's)".
- **Measured**: `TMPDIR=<fakehome>` → `verdict=TARGET_MET` rc 0, i.e. the counter created `c2r-*` (and `home`, `xdg_*`
  inside it) under that home and removed them on the clean path (`receipts/home-admission.txt`). A 0.55-0.755 s SIGKILL sweep
  (10 ms then 1 ms steps) bracketed the scratch's lifetime to **<1 ms** — killed at 0.731 s it left 0 entries, at 0.732 s the
  run had exited — so residue was not capturable on this host; the residue claim is structural: `finally: shutil.rmtree(S)`
  at `:1120` cannot run after a kill. The round-49 counter of the same shape left 9 entries under a home when killed
  (`w1/SentHostState.md` §3.1, `receipts/workroot-under-home.txt`).
- **Exploit path**: operator or tooling has `TMPDIR=$HOME/tmp` (a common shell setting) and runs the frozen command without an
  explicit `TMPDIR`; the instrument writes and then removes `c2r-*` under home. A timeout/SIGKILL/OOM at the wrong moment
  leaves that tree in home state — the shape M48-10 exists to prevent.
- **Impact**: bounded transient home writes, residue only on abnormal termination; not reachable from the frozen scoring
  command, which passes `TMPDIR=<scratch>` (`registration.md`, C1 command line). No ledgered path is touched.
- **Smallest remediation**: copy the four-line home refusal that `c2-r50` already carries (`c2-r50-session-gate.py:421-427`)
  into `tmp_root()`, comparing against `os.path.realpath(os.path.expanduser("~"))` and the passwd home; `Setup` (rc 2),
  as the siblings do. Two clauses, no behaviour change on a scratch dir.

### F2 (low, open) — gate v3 writes its `cat-file` request list into the ambient temp dir with no refusal (R-SHS-4 still open)

- **What it attacks**: `quality/check-session-material.py:975` — `tempfile.NamedTemporaryFile("wb", delete=False)` with no
  `dir=`, in the scan path of every non-selftest run; the selftest scratch at `:2078` has the same shape
  (`dir=os.environ.get("TMPDIR") or None`). The gate has **no `--work`** and **no scratch-root rule**, unlike both counters and
  the wave-done gate.
- **Measured**: with `TMPDIR` at mode 500 the scan still completed (`files=23920 findings=235`, rc 1) because
  `tempfile.gettempdir()` silently fell back: `TMPDIR=<unwritable>` → `/tmp`, `TMPDIR` unset → `/tmp`
  (`receipts/gate-tmpdir.txt`). So the sha-list request file is written to a temp dir chosen by ambient state, never
  refusal-checked, `0600`, unlinked at `:1008`.
- **Exploit path**: `TMPDIR=$HOME/tmp python3 -I quality/check-session-material.py --repo .` (or `--selftest`) writes the
  request list — and, in selftest mode, whole fixture git repositories with commits (`:1517-1528`) — under home. A kill leaves
  them there. The last entry of the fallback chain is `os.getcwd()`, so with every temp candidate unwritable the write lands in
  the lane/repo checkout instead.
- **Impact**: content is a list of blob SHAs (plus, in selftest mode, synthetic fixtures); no operator secret, no tracked file
  modified. It is still the round's frozen C2 instrument writing outside any declared root.
- **Smallest remediation**: mirror the counters — require `TMPDIR` outside the `/tmp`,`/var/tmp`,`/dev/shm` family and outside `$HOME`/passwd home, raise
  `GateError` otherwise (the gate already has `GateError` → exit 2), and pass `dir=` explicitly to both the request file and the
  selftest scratch.

### F3 (informational) — `PRED-C1-r50`'s git calls inherit the operator's `HOME`, so they read `~/.gitconfig`

- **What it supports**: `quality/counters/c1-r50-bind-entry.py:185` builds the git env as "ambient minus `GIT_*`", which keeps
  `HOME`. Every `git -C repo show|rev-parse|ls-tree|grep` (`:214-236`) therefore reads the operator's global config; the
  siblings neutralize this (`c2-r50-session-gate.py:197-212` sets `HOME=<work>/home` and `GIT_CONFIG_NOSYSTEM=1`;
  `check-wave-done.py:172-181` sets `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM=/dev/null` and `GIT_OPTIONAL_LOCKS=0`).
- **Measured**: an invalid `~/.gitconfig` in a fake home makes the counter stop at `SETUP unresolved revision …` rc 2
  (`receipts/c1-ambient-config.txt`) — the read is real, and it fails **honestly** (setup, never a verdict), which is the safe
  direction.
- **Impact**: no write surface (these verbs do not lock or refresh an index); a hostile or broken user config can only force a
  SETUP. Worth stating because the counter's docstring presents clause r as the *only* ambient read.
- **Smallest remediation (optional)**: pin `HOME`/`GIT_CONFIG_GLOBAL=/dev/null`/`GIT_OPTIONAL_LOCKS=0` in `ENV` at `:185`, as
  `check-wave-done.py:172-181` does, so the counter's read set matches its docstring.

### F4 (supporting, closes R-SHS-3 by construction) — no round-50 counter nests a tracer

- `receipts/tracer-nesting.txt`: `strace|bwrap|TracerPid|ptrace` has no match in `c1-r50-bind-entry.py` or
  `c2-r50-session-gate.py`, and none in the gate or the wave-done gate. Only `mado-hostguard.py` mentions `bwrap`, as an
  optional `--sandbox` (`:315-378`), and it starts no tracer itself (w1/ExecHostGuardR50 measured an outer `strace` leaving
  `exit=0`, digest before = after). The R-SHS-3 artifact is therefore unreachable: the counter that ran its own
  `strace … bwrap …` was the round-49 keysym counter (`w1/SentHostState.md:183`), and `PRED-C1-r50` replaced it with a direct
  `/usr/bin/hyprctl` read.
- Consistent with the freeze: the C1 counter's only live dependency is the compositor socket, which is a `connect()` inside
  `hyprctl` (`:1081,:1107`), and the freeze records "a host without the socket fails closed (SETUP)".

### F5 (supporting) — three of the four work-root instruments refuse the operator home at admission; nothing is created

Measured, each rc 2 with `test -e` → `NO` (`receipts/home-admission.txt`):
`c2-r50 --work <home>/…` → `--work is under the invoking home (~)`; `check-wave-done.py --selftest --work <home>/…` →
`refusing work dir inside the home directory (got ~/…)` (both `$HOME` and the passwd home, `:504-523`); `mado-hostguard.py
--selftest --work <home>/…` → `refused: … resolves inside the operator home`, `MADO_HOSTGUARD_SELFTEST: 0/45 passed`.
This is the round-48 M48-10 admission shape, implemented three times independently. The c1 counter (F1) is the gap.

## Limits of this seat (declared)

- Static containment is by locator, not by syscall tracing: R-SHS-3 says an outer tracer makes a counter report a false miss, so
  no counter was wrapped. The dynamic support is (i) a real full run with a clean scratch, (ii) the mode-500 `TMPDIR` probe
  which localizes the c1 scratch, (iii) the three admission refusals, (iv) the gate's temp-dir fallback.
- The SIGKILL residue for `PRED-C1-r50` is **not** measured on this host (sub-millisecond window); it is inferred from the
  `finally`-only cleanup at `:1120` plus the round-49 measurement of the same code shape. `[INFERENCE]` for residue; the
  acceptance of a home-rooted `TMPDIR` is measured.
- Only the seven named instruments were read. `quality/counters/*` from earlier rounds, `tools/mado-*.py` probes and
  `quality/check-*.py` outside the freeze were not audited here.
- No host mutation, no compositor verb beyond the four allowed reads, no GUI launch, no pacman transaction; all scratch under
  `/fast/scratch/hyaku/mado-r50/SentHostState50` (deleted before this seat finished).

## Deliverables

- `.ufo/waves/round-50/w2/SentHostState50.md` (this report)
- `.ufo/waves/round-50/w2/SentHostState50/receipts/containment-table.txt`
- `.ufo/waves/round-50/w2/SentHostState50/receipts/c1-live-clause-r-and-control.txt`
- `.ufo/waves/round-50/w2/SentHostState50/receipts/home-admission.txt`
- `.ufo/waves/round-50/w2/SentHostState50/receipts/gate-tmpdir.txt`
- `.ufo/waves/round-50/w2/SentHostState50/receipts/tracer-nesting.txt`
- `.ufo/waves/round-50/w2/SentHostState50/receipts/c1-ambient-config.txt`
- `.ufo/waves/round-50/w2/SentHostState50/receipts/instrument-pins.txt`

Report: .ufo/waves/round-50/w2/SentHostState50.md
