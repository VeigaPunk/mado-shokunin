# w1 / SentTool — safety review: round-46 C1 reference, both counters, host reads

Seat: `SentTool` (safety-review attack role, leaf). Round 46 w1, 2026-10-26.
Reviewed (read-only, frozen): `.ufo/waves/round-46/l1-draft/mado-devices.py` (sha256 `b229efd0…a33b`),
`quality/counters/c1-r46-devices.py`, `quality/counters/c2-r46-input-device-entry.py`,
`.ufo/waves/round-46/receipts/live-devices-host-l1.txt`, `.ufo/waves/round-46/ctl/run-c{1,2}-controls.py`.
Scratch: `/fast/scratch/hyaku/mado-r46/SentTool` (deleted at hand-off). Evidence: `evidence/` beside this file;
every claim below names the artifact it rests on.

**Bottom line.** The reference tool is sound: strace shows one `execve` (itself), zero socket-family calls, zero
write-mode opens, and its output framing survives every injection I could build. What is *not* sound is the
**scoring harness**: a tool committed at `tools/mado-devices.py` is arbitrary code, and the C1 sandbox leaves the
live compositor's unix socket, the user's home and peers' scratch reachable, while clause `r` ("no hyprctl run")
is a PATH marker that three scored bypasses walked straight through at `verdict=TARGET_MET`. The C1 claim can be
true and the counter's evidence for it still be weaker than the registration states.

| # | Sev | Surface | One line |
|---|-----|---------|----------|
| F1 | HIGH | counter `sandbox()` / `hidden_paths()` | scored tool can reach the live Hyprland IPC socket, `~`, and sibling scratch dirs |
| F2 | HIGH | counter clause `r` | the "no hyprctl run" check is PATH-only and erasable; three tools passed `TARGET_MET` while running hyprctl |
| F3 | MEDIUM | counter `load_model()` | scoring writes `__pycache__/*.pyc` into the frozen lane ("nothing in the lane is written" is false) |
| F4 | MEDIUM | counter marker dir | only writable real path in the sandbox is unbounded (disk fill) and is discoverable from `/proc/mounts` |
| F5 | LOW | counter `--work` | accepts any existing dir outside 3 paths (own home, `/tmp`, `/`); seat scratch rule not enforced |
| F6 | LOW | counter `make_fakebin()` | marker path interpolated unquoted into `#!/bin/sh` (command execution on a `--work` with `'`) |
| F7 | LOW | reference `cut_comment()` | O(n²) string copies: one 1 MiB line of `##` pairs costs 8.9 s CPU |
| F8 | LOW (provenance, code-reading only) | C2 counter clause `d` | docstring says a new id must gate on a PINS receipt; the code accepts a candidate-authored file |
| P1–P6 | — | reference / receipts / C2 counter | verified holds (no process, no socket, no write; injection, path classes, size cap, live receipt) |

---

## F1 HIGH — the scored tool runs with live reach to the compositor, the home tree and sibling scratch

**Attacks.** Registration C1 clause `i` ("bubblewrap isolation; repository, the counter's lane and its parent
hidden") and the round's host-safety rule (no compositor mutation). Also the reference's own promise that a tool
"opens no socket" (`l1-draft/mado-devices.py:26`) — nothing in the harness enforces that for the *scored* tool.

**Exploit path.** A tool committed at `tools/mado-devices.py` (scored as untrusted code) does its normal job and,
before/after, reads `$XDG_RUNTIME_DIR/hypr/` (visible inside the sandbox — one directory entry), connects to
`<signature>/.hyprland.sock`, and writes `dispatch …` / `keyword …` / `plugin …` frames. stdout is unchanged, so
clauses `a s f g` still pass; clause `r` sees no marker (F2). Reaching a *second* payload is unnecessary: the same
run also reads `~/.config/hypr/*`, the LANE's own home-dir configs, and any sibling seat's scratch.

**Evidence.**
- `evidence/sandbox-reachability.txt` — one run inside the exact argv built by `sandbox()`
  (`c1-r46-devices.py:251-257`: `--ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net
  --die-with-parent` plus `--tmpfs` over the three hidden paths): `hyprctl_path=/usr/bin/hyprctl executable=yes`,
  `xdg_runtime_dir=/run/user/1000`, `hypr_sig_dirs=1`, `hypr_sockets=2`, `wayland_sockets=1`,
  `absolute_home_conf_readable=yes`, `absolute_home_ssh_dir_listable=yes`,
  `scratch_root_entries=5`, `absolute_hyprctl_rc=4` (binary executed; only the fake
  `HYPRLAND_INSTANCE_SIGNATURE` stopped it finding an instance) — and `lane_file_readable=no`, i.e. the tmpfs
  shadow of the lane works while nothing else is hidden.
- `evidence/socket-ro-bind.txt` — a unix socket on a **read-only** bind is still connectable:
  `CONNECT_OK` under `--ro-bind`, `CONNECT_OK` under `--bind`. So the blanket `--ro-bind / /` is *not* a control
  on AF_UNIX; read-only only blocks writes to the socket inode's filesystem, which is not what `connect()` needs
  here.
- `c1-r46-devices.py:243` — hidden paths are exactly `{realpath(repo), lane root, dirname(lane root)}`
  (quote verified). `$HOME`, `/run/user/<uid>`, `/tmp` and every other seat's scratch are not in that set.
- `c1-r46-devices.py:269` — environment B does not merely leave the socket reachable, it *hands the tool the
  directory*: `"XDG_RUNTIME_DIR": "/run/user/%d" % os.getuid()`. A tool under env B never has to guess, and
  `--unshare-net` (`:252`) covers IP networking only, never AF_UNIX.
- `evidence/sandbox-writable-surface.txt` — `/tmp` is `EROFS` inside, so the only writable real path is the
  explicit `--bind`; that bounds *writes*, not reads or IPC.

**Impact.** A single scoring run of an untrusted tool can mutate the live compositor (`dispatch`, `kill`, `plugin`,
`keyword` are all read-only for the harness), read the operator's Hyprland config and `~/.ssh` (both listable
inside), and enumerate the wave's scratch root (`/fast/scratch/hyaku/mado-r46`: 5 entries at receipt time, 25
earlier in the wave — freeze clones there carry the pinned reference and fixtures as plain files). This is the
highest-severity surface in the round: the C1 claim is scored by executing arbitrary code with the user's own
credentials and IPC.

**Smallest remediation.** Extend `hidden_paths()` (line 243) with `os.path.expanduser("~")` and
`"/run/user/%d" % os.getuid()`, so `sandbox()` tmpfs-mounts them too; keep `--unshare-net`. Two lines, no contract
change, and it closes the compositor, the home tree and (via `$HOME`) most secret reads in one move. Screening
`$XDG_RUNTIME_DIR` alone is enough to close the IPC path, but `$HOME` is the cheap blanket.

---

## F2 HIGH — clause `r` is a PATH-marker test; two bypasses scored `TARGET_MET`

**Attacks.** Registration C1 clause `r`: "no `hyprctl`/`libinput`/`journalctl`/`udevadm` run", and the counter's
own clause text at `c1-r46-devices.py:29-31` (quote verified at `:29`).

**Exploit paths (both built, committed and scored in my scratch clone).**
1. **Absolute path, every run.** `subprocess.run(["/usr/bin/hyprctl", "version"], stdout=DEVNULL, stderr=DEVNULL)`
   injected after `import json`. `PATH` is irrelevant to an absolute path, and the real binary lives inside the
   sandbox (`--ro-bind / /`). Scored at rev `3d96dcd36d166585619df68a8ffc2dabdfad00e4`, nonce 46:
   `clause=r marker=absent`, `readonly=ok`,
   `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0
   (`evidence/clause-r-bypass-absolute-path.txt`, patch in `evidence/bypass-commits.txt`).
2. **Selftest PATH, one run.** The selftest is launched with its own env, `env={"PATH": "/usr/bin:/bin", …}`
   (`c1-r46-devices.py:375`, quote verified) — *no fake bin at all*. A tool that calls `hyprctl` by bare name only
   under `--selftest` never touches the marker. Scored at rev `ef072a720cc7c157a58084cd33d51defff280775`:
   identical `TARGET_MET`, `clause=r marker=absent` (`evidence/clause-r-bypass-selftest-path.txt`).
3. **Run the fake, then erase the trip.** The marker dir is the sandbox's only writable `--bind` (`:256`) and it is
   a *sibling of every working directory*, so a relative glob reaches it. A tool that runs `hyprctl` by bare name
   (landing on the fake, creating the marker) and then unlinks `../mk-*/marker` passes: the marker is read once at
   `:400` and is gone by then. Scored at rev `3d9ce68cc4258eb7556a7c4ac7f0ca19d471ad46`: `TARGET_MET`,
   `clause=r marker=absent` (`evidence/clause-r-bypass-marker-erase.txt`). Clause `r` is therefore vacuous in its
   own terms, not merely PATH-limited: the observed side (a file the scored run can write) is under the scored
   run's control.

**Impact.** The clause the registration relies on to assert the tool "runs nothing" is satisfied by a tool that
runs something. Combined with F1 this is not merely a scoring hole: it removes the *only* mechanical signal that a
scored tool spawned a compositor client at all.

**Smallest remediation.**
- Line 375: give the selftest the same env as environment A (fake bin first) instead of `/usr/bin:/bin`.
- Make the four names un-bypassable: after resolving them with `shutil.which`, add
  `--ro-bind <fake>/hyprctl /usr/bin/hyprctl` (and the other three) to `sandbox()`, so an absolute-path invocation
  also lands on the marker.
- Better, and cheap here: run each invocation under `strace -f -qq -e trace=execve -o <log>` (or
  `bwrap --seccomp`) and fail the clause on any `execve` beyond the tool's own — a PATH shim cannot see
  `execveat`, `posix_spawn`, or an interpreter-level `os.execv`.

---

## F3 MEDIUM — the counter writes into the frozen lane (`__pycache__`), contradicting its own docstring

**Attacks.** `c1-r46-devices.py:9-10` — "nothing in the lane is written; scratch only under --work" (quotes
verified at `:9`, `:10`).

**Exploit path.** `load_model()` calls `importlib.util.spec_from_file_location(...)` + `spec.loader.exec_module(mod)`
(`:101`, quote verified) with no bytecode guard; CPython writes
`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc` (and `quality/counters/__pycache__/…`),
i.e. files inside the tree the round freezes. Nothing filters `PYTHONDONTWRITEBYTECODE` and neither script sets
`sys.dont_write_bytecode` (grep: no match).

**Evidence.** `evidence/lane-bytecode-write.txt` — a mirror at the same relative layout gets exactly those two
`.pyc` files from `load_model()`; the real lane already holds
`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc` (2026-10-26T17:23:34, 40172 bytes, not
written by this seat), and `.gitignore:3:__pycache__/` is why `git status` looks clean.

**Impact.** (a) A frozen-artifact claim is false. (b) A stale/shadowed bytecode next to the sha-pinned reference is
a live hazard for any sibling that imports the module *without* the sha gate (`l1-draft/gen-fixtures.py` does
import it); Python revalidates by mtime+size, so a byte-identical-source swap survives, but a same-size
same-mtime edit does not — the sha check is the only real guard and `__pycache__` weakens "read the pinned bytes".
(c) Every scoring run mutates the tree it claims to leave alone.

**Smallest remediation.** `sys.dont_write_bytecode = True` at the top of the counter, add
`PYTHONDONTWRITEBYTECODE=1` to every env it builds, and (belt) load the model with
`compile(pinned_bytes, MODEL_PATH, "exec")` + `exec` in a fresh dict instead of `importlib`.

---

## F4 MEDIUM — the sandbox's single writable real path is unbounded and discoverable

**Attacks.** Clause `i`'s isolation claim ("a writable bind of the marker directory only").

**Exploit path.** A scored tool greps `/proc/mounts` (visible; `proc` is mounted), finds the one rw mount whose
backing device is a real block device rather than `tmpfs`, and writes there until the host filesystem that hosts
`--work` is full (420 invocations × unbounded bytes). The counter deletes `work/` only after the whole scoring run.

**Evidence.** `evidence/sandbox-writable-surface.txt` — `/tmp` write → `Read-only file system`; the `--bind`
directory → write succeeds; and `grep ' <dir> ' /proc/mounts` inside the sandbox prints the rw mount line
(`/dev/nvme1n1p2 … xfs rw,…`). Note the `--tmpfs` mounts over the hidden paths are *also* rw (memory only) — a tool
can fill RAM too, bounded by tmpfs defaults.

**Impact.** Availability of the scoring host mid-wave (other seats' counters fail with ENOSPC); no confidentiality
or integrity gain beyond dropping files that are later rmtree'd — except that this same writable directory holds
clause `r`'s trip, which F2's bypass 3 deletes.

**Smallest remediation.** Give the child `RLIMIT_FSIZE`/`RLIMIT_NOFILE` via `preexec_fn` in `run_tool()` and
`rmtree` the marker dir's *contents* after each fixture (mkdtemp it fresh per run if cheap). A size-limited tmpfs
for the marker would need root; the rlimit does not.

---

## F5 LOW — `--work` acceptance is minimal (and the seat scratch rule is not enforced here)

**Attacks.** Counter contract ("must lie outside the repository, the counter's lane and that lane's parent") vs.
the round's scratch rule (every work dir under `/fast/scratch/hyaku/mado-r46/<Seat>/`, passed explicitly, never
`/tmp`).

**Evidence.** `evidence/work-dir-validation.txt` — `--work` = the lane, the lane's `.ufo`, and the fleet root all
give `SETUP work dir inside a hidden path …`, exit 2 (good); a missing dir gives `SETUP work dir missing`, exit 2;
`/fast/scratch/...` scores normally, exit 1 on a tool-absent lane. So the overlap test is sound and covers the three
paths it names, but `--work ~/w`, `--work /tmp`, `--work /` would all be accepted, which puts the rw marker bind
(F4) inside the home tree or `/tmp`.

**Also verified good** (same receipt): every `mkdtemp` passes `dir=` explicitly (`:283,329,364,368,370,372,425`), so
`TMPDIR` is never consulted — no accidental `/tmp`; `shutil.rmtree(work, ignore_errors=True)` (`:429`) targets only
the `mkdtemp` child, and `rmtree` does not follow symlinks, so a hostile tool cannot redirect the delete.

**Impact.** Hygiene, plus a hostile tool's write destination moving into `$HOME` when a caller is careless.
**Smallest remediation.** Require `--work` to be under an allowlisted root (refuse `$HOME`, `/tmp`, `/`), or at
minimum refuse a `--work` whose realpath is not on a filesystem the operator named in the contract.

---

## F6 LOW — the fake PATH binaries interpolate an unquoted path into a shell script

**Code.** `c1-r46-devices.py:146`: `f.write("#!/bin/sh\n: > '%s'\nexit 0\n" % marker)` (quote verified).

**Exploit path.** `marker` lives under `--work`, which is caller-supplied. `--work "/fast/scratch/x'; cmd; : '"`
produces a fake `hyprctl` whose body executes `cmd` whenever a scored tool invokes it. Contained: the fake binary
runs *inside* the sandbox, so the payload inherits the sandbox's ro filesystem — this is an annoyance and a
misleading marker, not an escape.

**Evidence.** `evidence/fakebin-quoting.txt` — generated script `: > '/fast/scratch/x'; echo
FAKE_HYPRCTL_SHELL_INJECTION; : ''`, its execution prints the injected string.

**Smallest remediation.** `shlex.quote(marker)`, or write the fake binaries as a small `#!/usr/bin/python3` file
taking the marker as argv[1].

---

## F7 LOW — the reference's `cut_comment` is quadratic; one 1 MiB config line costs 8.9 s

**Code.** `l1-draft/mado-devices.py:196-203`, the copy at `:201` `line = line[:pos + 1] + line[pos + 2:]` (quote
verified). Each `##` pair rebuilds the whole (still ~1 MiB) string.

**Exploit path.** A 1 MiB config whose single line is `a` followed by `##` pairs. Under the tool's own
`MAX_BYTES = 1048576` (`:99`) this is legal input; the tool spends ~9 s of CPU on it. Scaling is clean O(n²):
1 000 pairs 0.000 s, 20 000 pairs 0.012 s, 200 000 pairs 1.201 s.

**Evidence.** `evidence/tool-dos-timings.txt` — through the CLI: `exact 1048576 → 0.02 s accepted`,
`1048577 → SETUP too_large`, `1 MiB one line of ## pairs → 8.86 s`, `1 MiB of 349 525 continuations → 1.08 s`.
`FLOAT_RE` shows no super-linear behaviour (1 MiB of digits 0.001 s), so the regex surface is fine.

**Impact.** Bounded (the 1 MiB cap caps it at ~9 s; the counter's 20 s timeout absorbs it), so this is operator
latency, not a harness break. Worth fixing because the tool is meant to be run by hand on config files.
**Smallest remediation.** Replace the in-place rewrite with an index walk appending to a list
(`out.append(line[prev:i])`, single `"".join` at the end), or `re.sub` the `##`→`#` pairs before the single-cut.

---

## F8 LOW (provenance; code-reading only, no run) — C2 clause `d` does not enforce what its docstring says

**Attacks.** `c2-r46-input-device-entry.py:28`: "a new id's receipt must be one of PINS" (quote verified).

**Reading.** `pin_ok` at `:532-534` is
`PINS.get(basename(path)) in (None, digest) and (basename(path) not in PINS or path == FETCH + basename(path))` —
so a path whose basename is **not** in PINS is accepted with any digest, as long as `sha256(blob) == digest` for
the blob read **at REV** (i.e. from the candidate's own commit). Clause `i` at `:668` is
`used = set(basename(gates[i][0][0]) …); bad |= not set(PINS) <= used` — the subset runs the *other way*
(every PINS must be used), so it does not restrict new receipts to PINS. Consequence: a candidate may add
`.ufo/waves/round-46/fetch/<Name-of-its-choosing>` inside its own commit and gate a new row on it, provided the
quote is unique in that file and `quote_in_code` passes. T4 (`:677`, the verdict-token check) has the same shape:
it reads `.ufo/waves/round-46/receipts/<file>` at REV, so a candidate-authored receipt can witness a candidate
claim.

**Why it is only LOW here.** The control set covers the *pinned* names (`FORGED-PIN` doctors
`fetch/Hyprland-ConfigValues.cpp`, which PINS pins), clause `e` requires a `Hyprland-` receipt's location to start
with the efb50993 raw URL, and clause `j`/`h` recompute the census and surfaces from the pins — so a fabricated
receipt buys one row, not the census. It is still a provenance gap between the predicate's words and its code, of
the same class round 45's verifier raised (`RevW2Counters` F1/F2 for the r45 counters, which I did not re-run).

**Explicitly not verified by a run.** I did not build a candidate that exploits it; this entry is a code-vs-docstring
reading, and I mark it as such rather than claim a score.

**Smallest remediation.** In `pin_ok`, require `basename(path) in PINS` for ids not in `reg_base` (the `new_ids`
list is already computed at `:511`), and restrict T4's cited receipt paths to PINS or to files present at `BASE`.

---

## Verified holds (what I could not break)

- **P1 The reference starts no process and opens no socket.** `evidence/ref-syscalls.txt`: strace of a normal run —
  `execve count: 1` (the interpreter itself, `execve("/usr/bin/python3", …)`), socket/connect/bind/sendto count 0,
  write-mode opens 0, creat/unlink/rename/mkdir 0. Docstring claim at `:26` holds under trace, not just by reading.
- **P2 Output injection holds.** `evidence/output-injection.txt`: a device name carrying
  `\nMADO_DEVICES: keyboards=0 agree=9 verdict=OK` stays inside one `name="…\n…"` field and the real summary still
  reports `keyboards=1`; quotes/`=`/`%s`/`{}`/`\x1b[2J`/tab are all `json.dumps`-escaped; a `10**60` `scrollFactor`
  prints on its line. Every name and config value goes through `json.dumps` (`:386`, `:401`, `:409`), the
  `differ=` list is drawn from the fixed `NAMES` tuple, and the `SETUP` reason is a literal — no format-string
  passthrough (`%s` in a config value arrives as data).
- **P3 Path handling holds.** `evidence/path-handling.txt`: FIFO, `/dev/zero`, directory, broken symlink,
  `/proc/self/mem`, `/proc/kcore` and `/dev/stdin`-over-a-pipe all return `SETUP unreadable` in ≤0.02 s (no block:
  `O_NONBLOCK` at `:126`, then `fstat` + `S_ISREG` at `:130` before any read, so symlink races and FIFO stalls are
  out). Symlink→regular is accepted (reads the target, by design). `/proc/self/environ` is accepted because procfs
  synthesises it as a *regular* file (`S_ISREG True`); the echo risk is bounded — only lines whose LHS is
  `input:kb_*` or starts with `device` reach the output, so a proc file does not dump its contents.
- **P4 Size cap is exact.** 1 048 576 bytes accepted, 1 048 577 → `SETUP too_large` (both `--config` and stdin).
- **P5 The live receipt is truthful and shape-only.** `evidence/live-receipt-verify.txt`: `~/.config/hypr/input.conf`
  sha256 matches the receipt's pin `3769c92a…7bf4`; the receipt body (lines 5-19) is **byte-identical** to a fresh
  `hyprctl devices -j | mado-devices.py` run (15 lines, same summary line, `exit=0`); grep for
  `address|0x[0-9a-f]{6,}|serial|description|title` finds nothing. Residual: the receipt carries HID vendor/model
  inventory names (hardware fingerprint) — required by the claim (per-device verdicts), no serial, no address, no
  window title, no process table, no home listing.
- **P6 The C2 counter has no scratch and no exec surface.** `c2-r46-input-device-entry.py`: one `subprocess` call
  (`git -C repo …`, `GIT_*` stripped, `:137`), no `tempfile`, no `os.remove`/`shutil`, no write-mode `open`, no
  `eval`/`exec`/`compile`/`importlib`/`pickle` — nothing to report on the scratch axis, and the registry/pin reads
  are lane-local. Same for the controls: `run-c1-controls.py` / `run-c2-controls.py` clone only under their
  caller-supplied scratch dir, assert `rev-parse --show-toplevel` equals the clone before committing, and rmtree
  only those clones.

## Notes for the L1 (not findings)

- Independent corroboration received after my runs (attributed, not adopted as evidence): `RevC1Counter-3` measured
  the same absolute-path shape and a marker-erase variant on the frozen counter, plus a sibling-scratch leak
  (`/fast/scratch/hyaku/mado-r46/*` freeze clones carry `l1-draft/mado-devices.py` and `c1-r46-fixtures.json` as
  plain files — 25 such directories were visible in my sandbox probe); `CritC1Cheat-3` reports the erase route with
  a no-unlink control at `readonly=fail`; `LabDupNames`, `ConnCalibration-3`, `ScrSkill` and `SentHost-2` re-read
  `:375`, `:241-243`, `:251-257`, `:269` and agree on the code facts. My own receipts are the ones cited above.
- **v2 snapshot, advisory only** (not a review; the file is live and moved on after I read it):
  `quality/counters/c1-r46-devices-v2.py` sha256 `19d00e664a1706cb03668efd8104548327419bc71cd9d2e2c68656d48b5d1e2a`, read at
  2026-10-26 21:03 UTC. Closed there: F1 (minimal allowlist root — only `/usr`, `/etc`, the tool dir and the fake
  bin are bound, so `/run/user`, `~` and `/fast` are simply absent), F2 bypass 2 (`PATH` is
  `fakebin + ":/usr/bin:/bin"` for the selftest too), F2 bypass 3 and F6 (`make_fakebin` writes
  `printf x >&<fd>` on an inherited pipe, no path). Still open at that hash: F2 bypass 1 — `/usr/bin/hyprctl` is
  bound from the real `/usr` and no fake is bound over it (grep "/usr/bin/hyprctl" = 0), so an absolute-path exec
  still leaves the trip untouched (harmless for the compositor, since nothing under `/run` is bound, but the
  clause's statement is still not what it measures); F3 — `load_model()` still `importlib`s the pinned reference
  with no `sys.dont_write_bytecode`; and a new F4 analogue — `--bind cwd cwd` makes each run dir writable where v1
  kept it read-only.
- The three clauses that carry the C1 claim (`s`, `f`, `g`) are all *tool-behaviour* clauses and are fine; the
  harness clauses (`i`, `r`) are where the evidence is thinner than the words. If v2 only changes the tool, F1/F2
  survive the round.
- Cost of the two bypasses: 10–11 s per full C1 score (420 sandboxed runs) on this host — a v2 regression test for
  F2 costs one such run per bypass shape.
