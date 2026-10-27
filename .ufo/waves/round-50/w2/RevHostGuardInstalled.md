# RevHostGuardInstalled — w2 falsify of D7 (host guard M48-10), round 50

## Verdict

**Partial support; actionable residual in unsandboxed `run`.** Installed tool matches the freeze pin and its selftest/demo basics pass. A delayed detached grandchild can modify a declared path after the guard takes its after-snapshot, yet the run reports `status=ok exit=0`. bwrap with `--die-with-parent` contained the corresponding attempt in my probe. The guard’s documented observation window is only before/after the direct child; it does not claim to prove no later write, but consumers treating `run` success as containment must account for this.

Undeclared writes inside the fake home are **not** violations: the contract pins only declared paths. Hardlink, atomic rename, delete/recreate, and dirfd-relative writes to a declared path during the observed run were all detected (exit 3).

## Evidence

All scratch-only runs used a `git clone -q --shared` at `b4a79843cc2545bbe800db9322e58f6e00436629`; clone root was `/fast/scratch/hyaku/mado-r50/RevHostGuardInstalled/lane`. At that revision, `git show ...:tools/mado-hostguard.py | sha256sum` and the installed tool both yielded `fdaa5c2ec297ebfdddc1238d0dfe693ba0ae75ed2310939843cf14b024b7b47e`, matching registration. Selftest output: `MADO_HOSTGUARD_SELFTEST: 45/45 passed`, rc 0.

W1 receipt evidence: `.ufo/waves/round-50/w1/ExecHostGuardR50/receipts/00-case-exits.txt` says `fails=0`; `a-unsandboxed-caught.txt` records the declared cache change as exit 3. The documented contract is in `tools/mado-hostguard.py:2-16,40-50`: digest twice and fail if a **declared** path changed; a tree digest is explicitly out of contract.

My reproducible receipt set is `.ufo/waves/round-50/w2/RevHostGuardInstalled/receipts/`; its `SHA256SUMS` verification completed with every file `OK`:

- `a-direct-caught.txt`: declared direct write -> exit 3; `fields=sha256,size,mtime_ns`.
- `u-undeclared-inside-home.txt`: wrote a new file and appended to an existing undeclared fake-home file; declared file unchanged, `changed=0 status=ok exit=0`.
- `d1-hardlink.txt`: write through hardlink -> exit 3; digest changed.
- `d2-atomic-rename.txt`: tmp + replace -> exit 3; digest changed (including inode).
- `d3-recreate-same-bytes.txt`: unlink/recreate identical bytes and restore mtime -> exit 3; `fields=ino`.
- `d4-dirfd-openat.txt`: dirfd-relative open/write -> exit 3; digest changed.
- `d5-detached-writer.txt`: direct child forks grandchild, exits; guard reports `child_rc=0 ... changed=0 status=ok exit=0`; after the delayed grandchild writes, the declared-file SHA changes from `860e1440…` to `6cf05c62…`.

A timestamped repeat independently pins the window: `forked_at=1793091834.977224350`, guard completed at `1793091834.995595800` with `changed=0 status=ok`, and grandchild wrote at `1793091835.479070425`; SHA at guard completion was the original `860e1440…`, and at +1s was `ac97d7e4…`. Thus this is a post-snapshot write, not a missed in-window digest mutation. The bwrap detached probe reported exit 0 with unchanged declared-file SHA after waiting one second.

The demo script `run-defeat-probes.sh` and all receipts are in the scoped seat directory. The scratch clone/work/fake home were removed before completion. No tools were installed.
