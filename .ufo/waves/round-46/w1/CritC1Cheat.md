# w1 / CritC1Cheat — PRED-C1-r46 attack (scoped findings)

Seat `CritC1Cheat`. Attacked: `quality/counters/c1-r46-devices.py` (frozen PRED-C1-r46) at the round-46 freeze
`8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`. Full narrative + reproduction: `.ufo/waves/round-46/w1/CritC1Cheat/report.md`.
Receipts: `.ufo/waves/round-46/w1/CritC1Cheat/receipts/`. No tracked file edited; scratch removed at exit.

## Result

Four cheat tools, each implementing **no** part of the contract. Three reach `TARGET_MET` (`--nonce 4601`):

- **A** — ambient-oracle delegation: `fixtures=90/90 generated=150/150 selftest=ok readonly=ok verdict=TARGET_MET`
  (`receipts/score-A-ambient.txt`).
- **B** — runs `hyprctl`/`libinput`/`journalctl`/`udevadm` and unlinks the harness marker:
  `verdict=TARGET_MET`, `clause=r marker=absent` (`receipts/score-B2.txt`).
- **C** — harness detection (`/proc/1/cmdline` = bwrap) with delegation; inert on the host
  (`receipts/host-parity-C.txt`, `rc=2`): `verdict=TARGET_MET` (`receipts/score-C-ambient.txt`).
- **D** — fixture-shape table over the pinned corpus: `fixtures=90/90 generated=0/150` (`receipts/score-D-ambient.txt`);
  isolates clause `f`'s weight, not a MET.
- **Ctl** — B without the unlink: `readonly=fail marker=present` → `r` works, it is only scrubable
  (`receipts/score-Ctl2.txt`, `receipts/tripwire-proof-{B,Ctl}.txt`).

## Findings and smallest safe corrections (each keeps the reference MET)

1. **`i` — mask names three paths, the oracle is ambient (A).** `--ro-bind / /` (`quality/counters/c1-r46-devices.py:252`)
   plus `hidden_paths` = `{repo, lane, dirname(lane)}` (`:241-243`, applied `:360`) leaves `/fast/scratch/**` open, where
   **67** files hash to the pinned reference/corpus (`receipts/oracle-inventory.txt`; the wave's own recipes render the
   reference into scratch clones). Fix: minimal root (`/usr /lib /lib64 /bin /etc`, `--proc`, `--dev`), `--tmpfs` over
   `/home /fast /tmp /var /run /srv /opt`, then re-bind only the run dir, the tool file and the marker.
2. **`r` — the tripwire is inside the tool's writable bind (B).** `--bind marker_dir` (`:256`) + one `os.path.exists`
   (`:400`): creatable ⇒ deletable. Fix: enforce, don't observe — launcher installs a seccomp filter denying
   `execve`/`execveat` before running the tool in-process (contract `.ufo/waves/round-46/l1-draft/mado-devices.py:26`
   already says it starts no process); cheap fallback: bind the marker *file* rw with a read-only parent and require a
   per-binary token multiset.
3. **No parity clause (C).** A/B are both sandbox-shaped, so a tool may key on the sandbox. Fix: clause `h` — replay a
   fixed subset without bwrap (private dir, host env, PATH without fakebin) and require byte-identical
   stdout/stderr/rc; also vary invocation form.
3b. **`r` is bypassable without the scrub (cross-checked, `SentTool-3` revs `3d96dcd`, `ef072a7`).** The selftest run
   gets `PATH=/usr/bin:/bin` and no fake bin (`c1-r46-devices.py:376`), so `hyprctl` during `--selftest` leaves no
   marker; the fake binaries exist only on `PATH` while `--ro-bind / /` exposes the real ones, so an absolute
   `/usr/bin/hyprctl` is invisible to `r`. With B that is three routes (name resolution, absolute path, deletion).
   Cheap fix: `--ro-bind` the four stubs over their `/usr/bin` paths and give the selftest `env_a`'s `PATH`; the
   seccomp enforcement of finding 2 subsumes both.
3c. **`--unshare-net` does not block AF_UNIX (cross-checked, `SentTool-3` F2).** `/run/user/<uid>` is not masked
   (`hidden_paths` `:241-243`; env B names it at `:269`), so a scored tool can reach the live
   `$XDG_RUNTIME_DIR/hypr/<sig>/.hyprland.sock`; the contract's "opens no socket" is untested. Fix: add `realpath(HOME)`
   and `/run/user/<uid>` to `hidden_paths`, or adopt finding 1's minimal root (`--tmpfs /run --tmpfs /home`).
4. **`f`/`s` carry no evidence against a table (D).** 90/90 ×3 from the public pinned corpus + a forged
   `MADO_DEVICES_SELFTEST: 90/90 passed`. Fix: derive half the fixture set from the nonce (public shapes, nonce names,
   expectation from MODEL) or gate TARGET_MET on a `f-nonce` line; treat the public 90 as regression.
5. **Procedure leak (minor).** Run dirs pile up in `work` (`:283`) inside an unmasked path → run index/variant
   readable by the tool. Subsumed by fix 1, else `--tmpfs work` with only the run dir bound.

## Closed vectors (evidence in `receipts/sandbox-probe.txt`)

`--unshare-pid` gives pids `[1,2]`, PID 1 = bwrap, no counter cmdline → the nonce and parent argv are unreachable;
`--unshare-net` closes remote oracles; cwd is read-only, so the marker dir is the only writable surface (finding 2).

## Process note (recorded so the next reviewer does not repeat it)

My first clause-`r` sabotage never fired — the harness lays `PATH` as `<work>/bin-XXXX/bin`, so
`dirname(PATH[0])/mk-*` matched nothing and B scored MET as a bare reference copy with `readonly=ok`. Every `r=ok`
must be paired with a no-unlink control (`Ctl`) that shows the marker fires; otherwise the clause reads as passed
while nothing was executed.

## Axis impact

Operability (C1): the after-state line is forgeable in three independent ways; the round must tighten `i`, `r`, `f`/`s`
and add parity, or re-register v2 with new controls before any data commit. Coverage (C2) and separability: untouched.
