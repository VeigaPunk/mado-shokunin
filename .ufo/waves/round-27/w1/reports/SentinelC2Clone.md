# SentinelC2Clone — C2 counter host/lane safety

## Finding

**Severity: HIGH** — running an untrusted suite from `REV` is arbitrary code execution as the invoking user, not a sandboxed test. The counter can expose lane repository integrity and user-readable files/secrets, and it does not constrain network access. This is a static review; no hostile suite was executed.

### Exploit path and impact

- `c2/count.py:54-67` runs `git clone --shared --no-checkout LANE <scratch>` and checks out `REV` in the resulting clone. Those Git operations target the clone's worktree and `.git`; the helper's `GIT_OPTIONAL_LOCKS=0` also applies to its `git -C LANE` reads. **[INFERENCE]** The clone operation itself is not intended to write source `.git` state. `--shared`, however, makes the clone depend on the source object store rather than giving the suite an isolated copy of those objects.
- At `:70-95`, the counter starts the suite with `python3 -I <clone>/<rel>`, cwd set to the clone, and only `PATH` and a temporary `HOME` in its environment. `-I`/`env -i`, `timeout 300`, and `prlimit --as=4000000000` do not restrict filesystem or network syscalls. The suite runs with the caller's UID and can use ordinary Python/OS APIs. **[INFERENCE]** It can discover the source path from clone metadata/alternates or the known lane path, then write accessible lane `.git` files (objects, index, refs, config) and colocated `.jj` state; it can also read/write other user-accessible files and attempt network connections. The shared object store gives a particularly direct route to corrupt source objects. `HOME=<scratch>` hides the normal home as a default, not as a filesystem path.
- There is also an input-path escape before execution: `:131-134,153-160,70-81` accepts `--suite-*-rel`, then passes it to `os.path.join(m, rel)` without checking containment. An absolute `rel` or `..` traversal escapes the clone; when an override file is supplied, the counter itself writes its bytes to that path. A suite path committed as a symlink can also make `isfile()` and Python follow a target outside the clone.
- The memory limit is per process, not an aggregate/job or disk quota; default `jobs=6` can run multiple suites concurrently. The code has no explicit cgroup/subreaper cleanup for descendants that deliberately detach from the `timeout`-managed command.

**Smallest effective remediation before closure runs a data-bearing/untrusted revision:** do not execute its suite on the host. Run each suite in an OS sandbox (e.g. bubblewrap/container) with network and host home/lane mounts absent, a private writable scratch mount only, and bounded process/memory/disk resources plus teardown of the whole process group/cgroup. Feed it a non-shared private clone/snapshot so the suite cannot reach the lane object store through alternates. Also reject absolute/traversing suite relpaths, require a regular non-symlink file, and verify the resolved destination remains beneath the clone. Replacing `--shared` alone is not sufficient: same-UID suite code could still open the lane by absolute path.

## Evidence and authorized base run

Reviewed `c2/count.py` lines 54-95, 127-160, and 183-190. The suite-launch command is constructed at `:88-90`; there is no filesystem, network, PID, or mount namespace there. The base revision did not contain either suite: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree 5ddc5885 quality/ && git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e 5ddc5885:quality/counter-selftest.py` ended with `fatal: path 'quality/counter-selftest.py' does not exist in '5ddc5885'`.

I used the one authorized no-override base run:

```text
timeout 900 prlimit --core=0 -- env -i PATH=/usr/bin HOME=/home/vgpnk python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885
```

It completed in 13.26 seconds with exit 1. Output included:

```text
SUITE A quality/counter-selftest.py MISSING at REV
SUITE B quality/population-suite.py MISSING at REV
PRED-C2-r27 green=0/8 w_killed=0/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED
exit=1
```

Thus the run exercised clone/checkout only; every case returned `rc=None` for a missing suite, so **no suite Python was run**. This is not evidence that execution of a present or hostile suite is safe.

Before/after `git status --porcelain` was:

```text
before: ?? controls/; ?? evidence/c1-before-543f0445-run2.txt; ?? evidence/c2-before-543f0445-run2.txt; ?? fetch/; ?? w1/
after:  same, plus ?? evidence/r26-population-after.txt
```

The new untracked evidence file appeared during this run window in the shared lane; attribution is unknown. `.git` directory mtime changed from `2026-10-23 07:32:51.175968103 -0300` to `07:33:42.732208470 -0300`; in the `ls -la --full-time .git` snapshots, the listed direct entries (including `config`, `HEAD`, `index`, `objects`, `refs`) retained their prior mtimes. Because the root directory mtime changed and concurrent lane activity is visible, this is not a clean causal before/after proof of no `.git` mutation. The counter code's writes are directed to its scratch clone, but the hostile-suite risk above remains.

`coredumpctl list --no-pager --no-legend` count for `/usr/bin/Hyprland`: **1338 before, 1338 after (delta 0)**. This counter run did not launch Hyprland.
