# RevGateScript — review of `quality/check-r38-discrimination.py` (round 38 w1)

Scope: the discrimination gate at lane HEAD `bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5`
(Python 3.14.8). Findings verified by running the gate in read-only mode against the live
lane (clones only) and against scratch probe manifests in `/tmp`; no lane production file
was modified. Counters used: `quality/counters/c1-r38-event-ground.py`
(sha256 `6872e18d3003b5fcbf94adac4b259a4a3651d313e848dda8999572851fe71866`),
`quality/counters/c2-r38-eventq.py`
(sha256 `194a45c68f9e5756752daa8449dda1a7ae190ea016153b8e2e2a09c29f236921`).
Lane working tree was clean for all tracked files during the run.

## 1. Head run with the real manifest

Command (cwd = lane root):

```
python3 -I quality/check-r38-discrimination.py \
  --c1 quality/counters/c1-r38-event-ground.py \
  --c2 quality/counters/c2-r38-eventq.py \
  --manifest .ufo/waves/round-38/controls/manifest.json \
  --rev bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 \
  --sandbox-root /tmp/mado38-RevGateScript/run1 \
  --out /tmp/mado38-RevGateScript/receipt-head.txt
```

Exit 0. Exact summary line:

```
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
```

All 19 controls observed exactly their expected verdicts; no `ERROR`, no `ok=0`
(see receipt at `/tmp/mado38-RevGateScript/receipt-head.txt`, 20 lines).
The freeze commit's claim (`correct=19/19`) reproduces at HEAD.

## 2. Code walk

- Manifest load: `json.load(open(a.manifest))`; `manifest["controls"]` fetched unvalidated.
  No schema check (missing key → raw KeyError traceback, exit 1).
- Writes ops: `literal` (write text), `file` (copy from manifest dir), `append`, `delete`,
  `counter_fixture` (dumps `getattr(mod, attr).encode()` from the in-process-imported
  counter), `tool_run` (runs `tools/mado-eventq.py` from the sandbox clone against scratch
  `ss/log/journal` files), `py` (`exec(step["code"], env)`), else `SystemExit` (see F4).
- Counter loading: `importlib.util.spec_from_file_location` — `load_counter()` executes the
  counter module **in-process, in the gate's own process** (used for `counter_fixture`),
  and the counter is then re-run as a subprocess per control with
  `sys.executable -I <script> --repo <sandbox> --rev HEAD`. The instrument is **not**
  copied into the sandbox; it is executed from the lane working-tree path against the
  sandbox clone. Both counters declare `--repo` required and use it (c1:155-159,
  c2:252-256); no hardcoded lane path appears in the counters (grep). The gate does not
  pin the counter bytes (no digest recorded in receipt/summary).
- Verdict comparison: `observed()` requires the printed verdict **and** a matching exit
  code (MET→0, MISSED→1); anything else is `ERROR`. `ok = obs == ctl["expect"]`.
- Summary: `met = correct == len(controls)`; prints `controls=<n> correct=<c>/<n>`.

## 3. Findings

### F1 — HIGH: the sandbox is never deleted; each run leaks ~4.2 GB

`tempfile.mkdtemp(prefix="mado38-dsc-", dir=a.sandbox_root or None)` creates a root that is
never removed (no `try/finally`, no cleanup at exit). One gate run = 19 clones of the lane
(~226 MB each, .git 57 MB + checkout) ≈ 4.2 GB. Verified: after my successful HEAD run,
`/tmp/mado38-RevGateScript/run1` survived with all 19 control clones (4.2 GB). At 11:05–11:12
six sibling runs had left `mado38-dsc-*` dirs totaling 25.2 GB in `/tmp` (they disappeared
later; `/tmp` momentarily reached 95% of 128 GB). The c2 counter (`c2-r38-eventq.py:264-281`)
uses `/dev/shm` for its own scratch but DOES clean up (`shutil.rmtree` in `finally`) — the
gate is the leak. Disk exhaustion can break every lane agent.

### F2 — HIGH: the `py` op is not a sandbox; full host escape (demonstrated)

`exec(step["code"], env)` with globals `env` lacking `__builtins__` → Python injects the
full builtins (`open`, `__import__`, `eval`, `exec`, …). The env additionally passes `os`
and `subprocess` directly. The "safe" helpers also escape: `os.path.join(sb, rel)` returns
`rel` **unchanged** when `rel` is absolute. Demonstrated with probe manifest `attacks1.json`
(gate exit as expected; escapes verified on disk):

| probe | py code | result |
|---|---|---|
| helper write, abs path | `write('/tmp/…/esc-helper.txt','x')` | file created outside sandbox |
| builtin `open` | `open('/tmp/…/esc-builtin.txt','w')` | file created outside sandbox |
| `os.system` | `os.system('touch /tmp/…/esc-os.txt')` | file created outside sandbox |
| `subprocess.run` | `subprocess.run(['touch','/tmp/…/esc-sub.txt'])` | file created outside sandbox |
| helper delete, abs path | `delete('/tmp/…/canary.txt')` | canary deleted outside sandbox |
| helper read, abs path | `write('ESCAPED-READ.txt', read('/etc/hostname'))` | sandbox file contains hostname `plazir27` |


All probe controls observed `TARGET_MET` because they leave the real corpus intact at HEAD —
the genuine accept path still passes. The verdicts are irrelevant to the escape evidence,
which is the files created/deleted outside the sandbox.
The **frozen manifest already crosses the boundary by design**: `c1-r28-verbatim`
(manifest line 91) does `open('/home/vgpnk/Projects/shokuknow/merge/mado/…')` (a declared
read-only host read). So the name "sandbox" is false advertising; the isolation claim does
not hold. Practical risk is contained only because the manifest is frozen and lane-authored —
but any future manifest/control change (re-freeze, buggy or malicious control) can read or
destroy anything the gate user can (`rm -rf …` via `os`). No dangerous capability is
missing; the environment is over-permissive.

### F3 — HIGH: cross-control state poisoning via shared `ctx` (demonstrated)

`ctx` (and the live counter modules in `ctx["counters"]`) are shared across controls. Probe:
control `ctx-poison-A` ran `ctx['poisoned']='CTX-POISONED-BY-CONTROL-A'`; control
`ctx-poison-B` wrote `ctx.get('poisoned','clean')` into the sandbox — the leftover clone
contained `POISON-MARKER.txt => CTX-POISONED-BY-CONTROL-A`. A control can therefore alter
the behavior of later controls (e.g. mutate `ctx["scratch"]`, `ctx["controls_dir"]`, or
monkeypatch counter module attributes for `counter_fixture`), so controls are not
independent experiments.

### F4 — MEDIUM: setup failures exit 1 (and erase all results), not 2 as documented

Docstring promises "Exit 0/1; setup 2" ("setup" = usage/setup errors). In
code, `apply_writes` raises `SystemExit(str)` for unknown ops; `SystemExit` is a
`BaseException`, not caught by `except Exception`, so it kills the whole run, prints
nothing, and exits **1** — indistinguishable from a missed verdict by exit code alone.
Verified: probe `attacks2.json` (op `bogus_op`) → stderr
`MADO_R38_DISCRIMINATION SETUP unknown op bogus_op`, exit 1, **stdout empty** (all prior
controls' lines lost). Also `--sandbox-root` must pre-exist (`tempfile.mkdtemp` does not
create parents): a missing dir → raw `FileNotFoundError` traceback, exit 1 (hit twice
during this review). `json.load`/missing-key failures also exit 1 via traceback.

### F5 — MEDIUM: `instrument` field unvalidated — silent fallback to c2

`script = a.c1 if inst == "c1" else a.c2` — any value other than the exact string `"c1"`
(typo `"C1"`, `"c3"`, missing) silently runs the c2 counter, and the control is scored
against c2's verdict. Verified: probe `instrument-typo` (instrument `"cX"`, no writes,
expect `TARGET_MET`) → `control=instrument-typo instrument=cX expected=TARGET_MET
observed=TARGET_MET ok=1`. A c1 control could pass/fail under the wrong instrument without
notice. `ctl["expect"]` and `ctl["id"]` are likewise unvalidated.

### F6 — MEDIUM: `git add`/`git commit` return codes unchecked

`sb` `git add -A` and `git commit --allow-empty` return codes are ignored. If a commit
fails (ambient global config, hooks, disk), the counter then runs against the committed
pre-write tree while the writes sit uncommitted — the control is scored on the wrong tree
silently. Host config currently benign (no `commit.gpgsign`, no `core.hooksPath`), so this
is latent; the gate should fail loudly on nonzero add/commit.

### F7 — MEDIUM: empty manifest is a vacuous green

`met = correct == len(controls)` → `0 == 0` → exit 0, `verdict=TARGET_MET`. Verified:
probe `attacks3.json` (zero controls) → `MADO_R38_DISCRIMINATION: controls=0 correct=0/0
verdict=TARGET_MET` with exit 0. An emptied/truncated manifest passes the gate; it should
reject `len(controls) == 0`.

### F8 — LOW: `tool_run` subprocess inherits ambient `GIT_*`

Docstring claims "Git runs with every ambient GIT_* variable removed", and the git
subprocesses do pass `env=ENV` (the M37-4 repair, LOG.md:2248). But the `tool_run`
subprocess `subprocess.run([sys.executable, "-I", toolp, …])` passes **no env**, so it
inherits ambient `GIT_*` (the tool runs no git today, but the stated guarantee is absolute;
the gate strips GIT_* inconsistently).

### F9 — LOW: `file` op reads outside the controls dir

`open(os.path.join(ctx["controls_dir"], step["src"]))` — an absolute or `../` `src` reads
any host file. Unused by the frozen manifest (ops in use: 12 `py`, 4 `literal`, 1 `append`,
1 `counter_fixture`, 1 `tool_run`); capability exists.

### F10 — LOW: dead code and doc/code drift

- `BASE` (line 37) is defined and never used.
- `if a.out: pass` inside the control loop (line ~166) is dead; `--out` is written after
  the loop.
- The docstring says "scratch root (default /dev/shm)" but the code has
  `default=None` → `tempfile.gettempdir()` → `/tmp` (TMPDIR unset). Checked all history:
  the file was born (freeze 58e55ec, and three duplicate non-ancestor pre-freeze commits
  2dca0e6/a3b2d8b/ca7db0c) with the same docstring/code mismatch — the default never was
  `/dev/shm`; only the c2 counter still prefers `/dev/shm` for its own (cleaned-up) scratch.
  So "the sandbox root moved to /tmp" is a docstring bug, not a code change. (Motive is
  plausible: one run ≈ 4.2 GB would fill the 8 GB tmpfs with two concurrent runs — F1.)
- `sh()`'s `env or ENV` treats an empty dict as ENV (moot).

### F11 — INFO: verdict detection is first-match on concatenated stdout+stderr

`VERDICT.search(p.stdout + p.stderr)` takes the first `verdict=…` occurrence; a counter
printing a verdict-shaped string in a diagnostic could be misread. Exit-code agreement is
checked, which limits the blast.

### F12 — INFO: hardcoded `LANE` clone source

The gate always clones `/home/vgpnk/Projects/shokunin/mado-shokunin` and checks out `--rev`
from it; it cannot be pointed at a different checkout, and (with F2/F5) is tightly coupled
to the live lane.

## 4. What is sound

- `GIT_*` stripping on all git subprocesses (M37-4 repair honored) with sandbox identity
  `sandbox <sandbox@invalid>` and `--no-local` clones; the lane's git state/index are never
  touched (verified: lane `git status` unchanged; only untracked `w1/` wave files).
- Per-control handling of clone/checkout/write failures (non-SystemExit): recorded as
  `observed=ERROR` lines and the run continues.
- `observed()` requires verdict **and** matching exit code — a counter that prints MET but
  exits 1 scores ERROR, not MET.
- The counters clean their own scratch (`c2` `rmtree`; c1 has no scratch), and honor
  `--repo` over any hardcoded path.
- The frozen manifest itself contains no `write`/`delete`/`read` calls outside the sandbox —
  the only host path is the declared read-only `shokuknow` read in `c1-r28-verbatim`.

## 5. Summary

Head run verified: 19/19 TARGET_MET, exit 0 (quoted above), so the round's discrimination
claim reproduces. The gate's model is sound for verdict scoring, but its "sandbox" is a
convenience namespace with full host access (F2), its per-control isolation is leaky (F3),
it leaks ~4.2 GB/run (F1), and its failure semantics contradict their documentation (F4).
Priority: F1 (disk), F2/F3 (isolation claims), F4/F7 (failure/vacuous semantics), F5/F6
(silent mis-scoring).
