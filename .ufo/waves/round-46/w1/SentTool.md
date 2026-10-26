# w1 / SentTool — safety review: C1 reference, both round-46 counters, host reads

Seat `SentTool` (safety-review attack role, leaf), round 46 w1, 2026-10-26. Full detail:
`.ufo/waves/round-46/w1/SentTool/findings.md`; receipts: `.ufo/waves/round-46/w1/SentTool/evidence/` (16 files,
each a command + its real output). Scratch `/fast/scratch/hyaku/mado-r46/SentTool` removed at hand-off; no frozen
file in the lane was edited by this seat (`git status` over `quality/ .ufo/waves/round-46/l1-draft/ tools/ corpus/`
shows only two untracked sibling files, `c1-r46-devices-v2.py` and `c1-r46-fixtures-v2.json`, which are not mine).

## Verdict

**The reference tool is sound. The scoring harness is not.** `l1-draft/mado-devices.py`
(sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b`) starts no process, opens no socket and
writes nothing — verified under strace, not just by reading its docstring. But C1 scores *arbitrary committed code*
at `tools/mado-devices.py` inside a sandbox that leaves the live Hyprland IPC socket, `$HOME` and 25 sibling seat
scratch dirs reachable, and its clause `r` ("no hyprctl/libinput/journalctl/udevadm run") is defeated by three
different tools that I built and scored — all at `verdict=TARGET_MET`.

| # | Sev | Where | Finding | Receipt |
|---|-----|-------|---------|---------|
| F1 | HIGH | `c1-r46-devices.py:243,251-257,269` | scored tool can reach the live compositor socket (`$XDG_RUNTIME_DIR/hypr/<sig>/.hyprland.sock`), `~/.config`, `$HOME`, the wave scratch root; env B *hands* it `/run/user/<uid>`; `--ro-bind / /` does not stop `connect()` | `evidence/sandbox-reachability.txt`, `evidence/socket-ro-bind.txt` |
| F2 | HIGH | `c1-r46-devices.py:29-31,375,400,256` | clause `r` is a PATH marker and the marker is erasable: 3 bypasses scored `TARGET_MET`, `clause=r marker=absent` | `evidence/clause-r-bypass-{absolute-path,selftest-path,marker-erase}.txt`, patches in `evidence/bypass-commits.txt` |
| F3 | MEDIUM | `c1-r46-devices.py:9-10,97-101` | `load_model()` writes `__pycache__/*.pyc` inside the frozen lane; "nothing in the lane is written" is false | `evidence/lane-bytecode-write.txt` |
| F4 | MEDIUM | `c1-r46-devices.py:256,400` | only writable real path in the sandbox is unbounded, discoverable from `/proc/mounts`; it is also the trip F2 erases | `evidence/sandbox-writable-surface.txt` |
| F5 | LOW | `c1-r46-devices.py:417-425` | `--work` accepts any existing dir outside 3 paths (`~`, `/tmp`, `/` legal); positive: all `mkdtemp` pass `dir=`, `rmtree` bounded and symlink-safe | `evidence/work-dir-validation.txt` |
| F6 | LOW | `c1-r46-devices.py:146` | marker path interpolated unquoted into the fake `#!/bin/sh` binaries | `evidence/fakebin-quoting.txt` |
| F7 | LOW | `mado-devices.py:196-203` | `cut_comment` is O(n²): one 1 MiB line of `##` pairs = 8.86 s CPU (cap-exact) | `evidence/tool-dos-timings.txt` |
| F8 | LOW (reading only) | `c2-r46-input-device-entry.py:28 vs :532-534,:668` | docstring says a new id's Gate receipt must be a PINS receipt; code accepts a candidate-authored file under `fetch/` | code reading; no run claimed |

### The three executed clause-`r` bypasses (same frozen counter, nonce 46)

Each is the reference with ~6 lines added at import, committed on a scratch clone at freeze `8c5434c`, and scored
with `python3 -I quality/counters/c1-r46-devices.py --repo <clone> --rev <rev> --work <scratch> --nonce 46`:
all three print `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0.

1. `3d96dcd36d166585619df68a8ffc2dabdfad00e4` — `subprocess.run(["/usr/bin/hyprctl", "version"], …)`: a real
   `hyprctl` run on every invocation; absolute path ignores PATH, the binary survives `--ro-bind / /`.
2. `ef072a720cc7c157a58084cd33d51defff280775` — bare-name `hyprctl`, executed only under `--selftest`: that run's
   env is `{"PATH": "/usr/bin:/bin", …}` (`:375`) and never sees the fake bin, so no marker exists at `:400`.
3. `3d9ce68cc4258eb7556a7c4ac7f0ca19d471ad46` — bare-name fake `hyprctl` on every run, then
   `unlink("../mk-*/marker")`: the marker dir is the sandbox's only writable bind and a sibling of every working
   directory, so the trip is deleted before it is read. Clause `r` observes a file the scored run controls —
   vacuous in its own terms, not merely PATH-limited.

## Verified holds (attacks that failed)

- **Reference has no process/socket/write path.** `evidence/ref-syscalls.txt`: 1 `execve` (the interpreter itself),
  0 socket/connect/bind/sendto, 0 write-mode opens, 0 creat/unlink/rename/mkdir. Docstring `:26` holds under trace.
- **Output injection holds.** `evidence/output-injection.txt`: a device name carrying `\nMADO_DEVICES: …verdict=OK`
  stays inside one `name="…"` field and the real summary still counts `keyboards=1`; quotes, `=`, `%s`, `{}`,
  `\x1b[2J`, tab all escaped; `10**60` scrollFactor prints on its own line. Names/values go through
  `json.dumps` (`:386,:401,:409`); the `SETUP` reason is a literal.
- **Path handling holds.** `evidence/path-handling.txt`: FIFO, `/dev/zero`, directory, broken symlink,
  `/proc/self/mem`, `/proc/kcore`, `/dev/stdin`-over-pipe → `SETUP unreadable` in ≤0.02 s (no block:
  `O_NONBLOCK`+`fstat`+`S_ISREG` before any read, `:126,:130`); symlink→regular accepted by design;
  `/proc/self/environ` is procfs-regular and accepted, but only `input:kb_*`/`device*` keys reach the output, so
  it cannot dump its contents. Size cap exact: 1 048 576 accepted, 1 048 577 → `too_large`.
- **The live receipt is truthful and shape-only.** `evidence/live-receipt-verify.txt`: config sha256 matches the
  receipt's pin `3769c92a…7bf4`; lines 5-19 are byte-identical to my fresh
  `hyprctl devices -j | mado-devices.py` run (15 lines, same summary, `exit=0`); no `address`, `0x…`, `serial`,
  `description` or `title` anywhere; residual is HID vendor/model inventory names, which the claim requires.
- **C2 counter has no scratch and no exec surface.** One `subprocess` call (`git -C repo …`, `GIT_*` stripped,
  `:137`), no `tempfile`, no write-mode `open`, no `eval`/`exec`/`compile`/`importlib`/`pickle`; the controls clone
  only under their caller's scratch, assert `rev-parse --show-toplevel` equals the clone, and rmtree only clones.

## What I did not do

No contact with the live compositor beyond the allowed reads (`hyprctl devices -j`, one `--devices` dump re-read);
no `dispatch`/`keyword`/`reload`/`setprop`/`switchxkblayout`/`--batch`/`output`/`plugin`/`kill`; no Wayland client of
my own; the `hyprctl` executions in F2 ran with the fixture's fake instance signature (exit 4, nothing found) and
the socket test used **my own** listener, never the compositor's. No pacman or package transaction. No subagents.
No counter, fixture, control, registration, reference or pin edited — every counter run used a clone in my scratch.
Tool installations: none needed (bwrap and strace already present on the host).

## Handoff

`MadoR46` (lane L1) replied that v2 takes: a `/usr,/etc`-only root allowlist, the fake-bin PATH for the selftest,
`--ro-bind` of the four fakes over `/usr/bin/{hyprctl,libinput,journalctl,udevadm}`, and a pipe-based trip instead
of a deletable marker. Still open from my side on that plan: (a) the AF_UNIX escape is closed by hiding
`$HOME` + `/run/user/<uid>` (the allowlist alone is not load-bearing — `--ro-bind` does not stop `connect()`);
(b) `sys.dont_write_bytecode = True` (F3); (c) `shlex.quote(marker)` (F6); (d) `RLIMIT_FSIZE` or per-run marker
cleanup (F4); (e) C2's `pin_ok`/`new_ids` (F8) if that counter is re-cut too. A regression test for F2 costs one
full C1 score (~10 s on this host) per bypass shape.

Snapshot check of the v2 under construction (advisory, not a review; `quality/counters/c1-r46-devices-v2.py` sha256 `19d00e66…d1e2a`, 21:03 UTC): its allowlist-root sandbox, fake-bin selftest PATH and pipe trip close F1, F2 bypasses 2/3 and F6. Still open at that hash: F2 bypass 1 (`/usr/bin/hyprctl` is bound from the real `/usr`, no fake over it — harmless now that `/run` is unbound, but the clause still measures PATH only), F3 (`load_model()` still imports the pinned reference, so the lane `__pycache__` write remains), and a new F4 analogue (`--bind cwd cwd` makes each run dir writable).

