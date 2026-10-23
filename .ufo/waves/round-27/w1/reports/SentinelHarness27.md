# SentinelHarness27 — round 27, w1

## Scope and method

Read-only security/host-safety review of the round-26 → round-27 `harness/oracle.py` diff and the relevant C1 call path. I ran only:

```text
diff -u /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/harness/oracle.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/harness/oracle.py
```

The diff reports 1 file changed, 6 insertions(+), 4 deletions(-): a new round-27 slot directory, the snapshot symlink filter, and `env -i PATH=/usr/bin` around both bwrap launch commands (plus the runtime-dir prefix change). I did not run Hyprland, a counter, or a probe; no host coredump delta was collected because no Hyprland process was started. No source files were changed.

## Verdict

The `env -i` change closes the observed M26-5 `/proc/1/environ` inheritance leak at both bwrap launches, assuming the expected trusted executable lookup. The new snapshot check blocks a file symlink whose resolved target is outside canonical HOME, but it does not establish containment in the approved config roots: a symlinked root bypasses it, and links within HOME can still escape the selected root. A TOCTOU race remains. Static review found no direct case-tree path to the live compositor/runtime; copied host files can nevertheless cross into the tool sandbox through the snapshot bypasses.

## M26-5 environment leak — fixed at both bwrap launches

**Evidence:** In round 27, `oracle.py:148-162` starts the oracle path as `env -i PATH=/usr/bin prlimit ... bwrap ...`; `oracle.py:234-239` starts `run_tool` as `env -i PATH=/usr/bin timeout ... bwrap ...`. Each bwrap also applies `--clearenv` before setting its sandbox environment. The prior M26 observation was that the tool could read the launching environment from bwrap PID 1's `/proc/1/environ` (`round-26/w2/reports/ReviewIsolation.md:56`). The diff now strips that launch environment before bwrap exists, in both paths; PID 1 should therefore have only `PATH=/usr/bin`, rather than inherited credentials/session-variable names. The oracle child then gets only its explicitly listed variables (`:156-161`); the tool child gets its explicit `PATH` and `HOME` (`:237-239`).

**Caveat:** both argv arrays name the outer executable as bare `env`, so the host `subprocess` resolves it using the caller's inherited `PATH` before `env -i` takes effect. The prescribed counter invocations set `PATH=/usr/bin`, but direct callers with an attacker-controlled `PATH` could run a different `env` first. Use `/usr/bin/env` if the harness itself must guarantee the scrub under arbitrary caller environments.

## MEDIUM — snapshot root symlinks bypass the new filter; in-HOME links escape the selected root

**Exploit path:** Arrange for a configured root (or an ancestor such as `.config`) to be a symlink to another readable directory. `snapshot()` calls `realpath(src)` before `os.walk` (`round-27/harness/oracle.py:70-75`), so files reached through that root have canonical, non-symlink `p` paths when the new `islink(p)` check runs (`:77-80`). They are copied if regular and no larger than 1 MiB (`:80-87`), even when the resolved root is outside HOME. For a normal symlinked Omarchy theme root, the same canonicalization loses the root link; additionally, a file symlink inside the resolved theme tree to another location anywhere below canonical HOME passes the check because it tests HOME, not the theme/config root. Relative file links are resolved by `realpath`: links resolving outside HOME are skipped, while links resolving to another in-HOME location (for example a private file elsewhere under HOME) pass. Nested symlink directories below an ordinary walked root are not traversed by default `os.walk`; the root/ancestor symlink case is the bypass.

**Evidence:** `oracle.py:73-80` resolves each root first, then only checks individual `fn` entries. The containment prefix is `realpath(home_src) + os.sep`, not a validated resolved root. The copied tree is mounted read-only at `/snap/home` for the untrusted tool (`:234-239`). The historical round-26 review dynamically confirmed the root-symlink escape before this change (`round-26/w2/reports/ReviewIsolation.md:51`); round 27 leaves the root canonicalization in place and adds only the per-file check.

**Impact:** user-readable non-config files can be copied into the tool's input tree. This is a host-file disclosure boundary from the snapshotter to the tool, conditional on attacker-controlled or misconfigured config roots/links; the 1 MiB per-file limit does not make the copied data trusted.

**Smallest remediation:** validate each resolved source root against an explicit allowlist of intended canonical roots, with the Omarchy theme symlink constrained to its approved themes subtree; validate each copied file target beneath that approved root, not merely beneath HOME. Do not silently accept an arbitrary canonical target merely because it lies in HOME.

## LOW — containment check and file read are not atomic

**Exploit path:** A process able to mutate the source tree concurrently can replace a checked file/link or a path component after `islink`/`realpath` and before `isfile`/`getsize`/`open`, making the copy read a different target than the one checked.

**Evidence:** `oracle.py:78-85` performs containment, type/size checks, and `open(p, "rb")` as separate path-based operations. No file descriptor is held across the check and read.

**Impact:** under concurrent same-user mutation, a link that originally passes containment can be swapped to an external readable file before the bytes are read. This is a race, not an observed event in this review.

**Smallest remediation:** open relative to a descriptor for the validated root with beneath/no-magic-link resolution, then use `fstat` and read from that same descriptor. Keep the canonical-root allowlist above; an atomic open alone does not fix root misclassification.

## Live-session reachability

**Finding:** No direct live-session socket or compositor-control path is apparent in the intended case execution. `run_tool` unshares namespaces, clears the child environment, mounts the case only at `/snap/home`, uses private `/tmp`, and does not mount the host `/run` or the host home (`oracle.py:234-239`). The oracle path unshares all and uses a private XDG runtime directory plus tmpfs `/run`; it mounts the copied case home, read-only `/usr`, `/etc`, the WLR build and selected `/sys` paths, while its fresh `/dev` gets only the named render node (`:146-162`). Its host-side `hyprctl` calls get only `PATH` and the private `XDG_RUNTIME_DIR` (`:130-133`), with no inherited `HYPRLAND_INSTANCE_SIGNATURE`; the exit dispatch targets the signature found through that private runtime (`:173-205`).

The snapshot symlink issue is still a data-copy escape, not a live-session connection: a root/link can cause host-readable regular-file bytes to be copied into the case tree, but the live runtime/socket is not mounted into either sandbox, and Unix sockets are not copied by the regular-file check. A tool may read the copied bytes; it does not thereby gain a live compositor socket or a dispatch route. This conclusion is static and limited to the reviewed paths; no live-session probe was run.
