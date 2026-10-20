# SrcUnshare — v2.42.4 sources confirm "no root mapping → mount EPERM", but the cause is the exec-time capability drop, not libmount's fstab gate; 1 primary + 1 supporting row drafted

Seat: SrcUnshare (MadoR20.SrcUnshare-3). Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`
(HEAD `e629f731172b8238caffe50f152217ce56535fb4`). Written: this file, `fetch/SrcUnshare/`
(7 bodies + `receipts.jsonl`), and inert `/tmp` scratch (a discarded 404 probe body). No lane source, tool,
corpus or fleet file was touched.

## Answer to the assigned question

*Why does `mount` fail without a root mapping?* Three sourced layers at the pinned tag, in order of the
actual control flow:

1. **The uid mapping decides whether the exec'd payload is "root" inside the namespace.**
   `unshare.1.adoc:131-135`: `-r/--map-root-user` maps the caller's effective uid/gid "to the superuser UID
   and GID in the newly created user namespace"; `-c/--map-current-user` maps them "to the same UID and GID".
   The same paragraph states the purpose verbatim: `--map-root-user` "makes it possible to conveniently gain
   capabilities needed to manage various aspects of the newly created namespaces (such as … mounting
   filesystems in the mount namespace) even when run unprivileged" (`:132`).
2. **Executing the payload clears its capabilities when the namespace uid is nonzero.**
   `capabilities.7:1234-1242` (man-pages-6.16): "if a process with nonzero user IDs performs an execve(2)
   then any capabilities that are present in its permitted and effective sets will be cleared."
   Conversely `capabilities.7:1296-1299`: "If the real or effective user ID of the process is 0 (root), then
   the file inheritable and permitted sets are ignored" — the kernel then hands root-in-ns the full set
   (`:1320-1326`). `user_namespaces.7:133-137` grants the creator "a full set of capabilities in that
   namespace", which is why the *creating* unshare process may hold CAP_SYS_ADMIN while the exec'd child
   does not.
3. **mount(2) needs CAP_SYS_ADMIN in the user namespace that owns the mount namespace.**
   `user_namespaces.7:274-282`: "Holding CAP_SYS_ADMIN within the user namespace that owns a process's mount
   namespace allows that process to create bind mounts and mount the following types of filesystems" —
   the list includes `tmpfs (5) (since Linux 3.9)` (`:295-298`). With a nonzero mapping the exec'd child has
   no capabilities, so mount(2) returns EPERM.

**Which code path prints the message.** `mount.8.adoc:169`: "Normally, only the superuser can mount
filesystems."; `:72`: "The root permissions are necessary to mount a filesystem by default."; `:185`: "Since
util-linux 2.35, mount does not exit when user permissions are inadequate according to libmount's internal
security rules. Instead, it drops suid permissions and continues as regular non-root user."

The code that implements that sentence matters for the row, because it routes the failure to the *kernel*:

* `sys-utils/mount.c:46-58` (`suid_drop`) drops permissions and then calls `mnt_context_force_unrestricted(cxt)`
  unconditionally; block D `mount <source> <target>` calls it for every restricted caller
  (`:1105-1114`), and `-t <type>` triggers the same (`:1041-1042`).
* So `mount --bind A B` (and `mount -t tmpfs tmpfs D`) from a non-root caller is evaluated on the
  **unrestricted** libmount path and reaches the `mount(2)` syscall; the restricted fstab gate
  (`libmount/src/context_mount.c:245-246`, `return -EPERM` when `!mnt_context_tab_applied`) is *not* what
  refuses. That gate would print a different string: `"operation permitted for root only"`
  (`context_mount.c:1622-1624`, reached only under `!mnt_context_syscall_called(cxt)`, `:1610`).
* The string `"must be superuser to use mount"` exists exactly once, at `context_mount.c:1790`, inside the
  `syserr == EPERM` branch that requires `syserr = mnt_context_get_syscall_errno(cxt)` (`:1755`), i.e. a real
  failed mount(2), and it selects that wording only when `geteuid() != 0` (`:1781-1790`).
  **Therefore the message a harness will see is proof that the syscall ran and the kernel refused** — not
  proof of an fstab policy miss.

This agrees byte-for-byte with the independently observed probe in `w1/reports/ScoutUnshareHost.md`
(§ Answer, item 2): inner `uid=1000`, `CapEff: 0000000000000000`, `mount --bind` → `mount: …/b: must be
superuser to use mount.`, mount rc 32. Under `--map-root-user` the same report observes `inner_uid=0`,
`CapEff: 000001ffffffffff`, mount rc 0. So the round-19 failure mode is not a util-linux quirk to be worked
around; it is the documented consequence of mapping a nonzero uid and then exec'ing.

## Observed facts (commands and bytes)

| Fact | Evidence |
|---|---|
| Tag resolves (annotated): `a1d2b6980b84f38b389a6d6dda4a9623f47d13be` → peeled `d76cbf8f13e65ff657344f7f6a90042cf755ba59` | `git ls-remote https://github.com/util-linux/util-linux refs/tags/v2.42.4 'refs/tags/v2.42.4^{}'` |
| man-pages tag (annotated): `5d300a0fcb7df33de34f4e81d1c2d27ef94a850b` → peeled `29e0874dde8dd3e1ba555ca377b32ff18274a8e2` | `git ls-remote https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git 'refs/tags/man-pages-6.1*'` |
| Bodies fetched 200, sizes and digests below; receipts in `fetch/SrcUnshare/receipts.jsonl` | `curl -sSL --max-time 60 -o … -w '%{http_code} %{url_effective}'` |
| Host util-linux is 2.42.4-1 | `/var/lib/pacman/local/util-linux-2.42.4-1/desc` (%VERSION% `2.42.4-1`), read as bytes |
| `/usr/bin/unshare` sha256 `e4e385ae4accf4af5302c4bb32859355b1c640315bef56ce73d31b8b1f97fdc0`, 43,408 B, mtime 2026-09-21 08:54:30 -0300; `/usr/bin/mount` sha256 `ca6c26aa2b11a8431481d39ee562bc07a88984f3294f34846d3257ec28ae9c91`, 43,168 B | `sha256sum /usr/bin/{unshare,mount}` (file bytes only; no mount was executed) |
| `unshare --user --map-current-user /usr/bin/id -u` → `1000`, rc 0; `unshare --user --map-root-user /usr/bin/id -u` → `0`, rc 0; `unshare --version` → `unshare from util-linux 2.42.4` | run by me; payload is `/usr/bin/id -u` only — no mount, no write, no device |

Fetched bodies (`fetch/SrcUnshare/`, all sha256 computed over the saved bytes):

| body | bytes | sha256 |
|---|---|---|
| `unshare.1.adoc` | 21,149 | `023e15ba559af1e3ea1e2eb7efdd0903dadc49af58cb433eef7411db937ba4ae` |
| `mount.8.adoc` | 107,386 | `9df748670dde8f98af91c0ca023a364699e4aea16dd1c5b3398f0b4882629e6d` |
| `libmount-src-context.c` | 93,933 | `e8a67883eb37f459f255047ca325ffffc12427708487d3baab9d33ec9cb298e8` |
| `libmount-src-context_mount.c` | 53,656 | `e486b4095f9d88bde837fcd1dad564549496bf1f6ad371f05d911f5ac6fc6363` |
| `sys-utils-mount.c` | 32,599 | `0fead9beac92b208c9e144aaa0aac5e47ce657adff271ddf78838aca1d47afa2` |
| `user_namespaces.7` | 45,324 | `155d07c0186d2e9d52b253795b564f3041d3cd8ccd1474f3e3895896ffc5729a` |
| `capabilities.7` | 53,128 | `40a71b475511625a03336562df0c5e7eded84a878200d2262e0d67a98b1baab5` |

Additional sourced points on the option set named in the assignment: `--mount` creates the mount namespace
and a persistence file "must be located on a mount whose propagation type is not *shared* (or an error
results)" (`unshare.1.adoc:58-59`); propagation defaults to `private` automatically since 2.27 (`:30`) and
`--propagation` "is silently ignored when the mount namespace (*--mount*) is not requested" (`:140-141`);
the note at `:174` records that proc and sysfs mounted as root in a user namespace must be restricted to
bind-mount semantics.

## [INFERENCE] and [UNK]

- [INFERENCE] The observed `CapEff: 0` in `ScoutUnshareHost.md` is the exec-time drop of
  `capabilities.7:1234-1242`; I did not instrument the kernel, I matched the document rule to the reported
  status line. The two facts are independent observations that agree.
- [INFERENCE] `mk_exit_code`/`MNT_EX_USAGE` means the observed `mount` rc 32 is the usage-class exit; I read
  the mapping in `libmount/src/context_mount.c` but did not execute mount to confirm the exit code (the
  probe report observed 32, so this is corroboration, not my measurement).
- [UNK] Forms that *stay* restricted (single positional `mount /dir`, `-o`-only forms) take the libmount gate
  and can print `operation permitted for root only` or `can't find mount point in /etc/fstab`
  (`context_mount.c:1630-1639`); I traced the branches but did not run them. A harness matching on message
  text must pin *which* invocation shape it uses.
- [UNK] Whether `mount(8)` from this tag ever reaches `mount(2)` for a caller with no mount namespace of its
  own (the `-N/--namespace` flag path) is outside the fetched files; not investigated.
- [UNK] Kernel-version dependence: tmpfs has been userns-mountable since Linux 3.9 per `user_namespaces.7`;
  older semantics are not covered. Host is 7.2.11-arch1-1.

## Drafted rows (11-column shape of `corpus/SOURCES.md`)

`S1xx-pending` per L1's reserved S099-S110 allocation. Both rows are `tier: A`; status `queued` since
nothing consumes them yet.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1xx-pending | util-linux v2.42.4 — sys-utils/unshare.1.adoc + sys-utils/mount.8.adoc + libmount/src/context.c + libmount/src/context_mount.c + sys-utils/mount.c (raw.githubusercontent.com, commit-pinned) | code | A | why an unprivileged `mount` is refused inside a user namespace that maps no root uid, and what `--map-root-user`/`--map-current-user`/`--mount`/`--propagation` actually change at this tag | tag v2.42.4 (`a1d2b698…`) → commit `d76cbf8f13e65ff657344f7f6a90042cf755ba59`; unshare.1.adoc 21,149 B sha256 `023e15ba…`, `:30`, `:58-59`, `:131-135`, `:140-141`, `:174`; mount.8.adoc 107,386 B sha256 `9df74867…`, `:72`, `:167-190`; libmount/src/context.c 93,933 B sha256 `e8a67883…`, `:80`; libmount/src/context_mount.c 53,656 B sha256 `e486b409…`, `:245-246`, `:1610`, `:1622-1624`, `:1755`, `:1778-1790`; sys-utils/mount.c 32,599 B sha256 `0fead9be…`, `:46-58`, `:1041-1042`, `:1105-1114` | `--map-root-user` "makes it possible to conveniently gain capabilities needed to manage various aspects of the newly created namespaces (such as … mounting filesystems in the mount namespace)"; `--map-current-user` maps "to the same UID and GID"; mount keys restricted mode on the real uid (`context.c:80`) but its two-positional form drops suid and forces the unrestriced path, so a refusal is the mount(2) EPERM and reads "must be superuser to use mount" only when `geteuid() != 0` — a failed mount, not an fstab policy miss | queued | 2026-10-20 | on-release | — |
| S1xx-pending | Linux man-pages 6.16 — man/man7/user_namespaces.7 + man/man7/capabilities.7 (git.kernel.org cgit plain, tag-pinned) | docs | A | the kernel rules behind a namespace payload's capability state: what creating a user namespace grants, what exec clears, and which mounts CAP_SYS_ADMIN in the owning namespace permits | tag man-pages-6.16 (`5d300a0f…`) → commit `29e0874dde8dd3e1ba555ca377b32ff18274a8e2`; user_namespaces.7 45,324 B sha256 `155d07c0…`, `:75-78`, `:137`, `:257-260`, `:274-282`, `:295-298`, `:351-353`; capabilities.7 53,128 B sha256 `40a71b47…`, `:1171-1173`, `:1234-1242`, `:1282-1306`, `:1320-1326` | creating a user namespace via unshare(2) gives "a full set of capabilities in that namespace", but "if a process with nonzero user IDs performs an execve(2) then any capabilities that are present in its permitted and effective sets will be cleared", while uid 0 in the namespace makes the kernel treat file permitted/inheritable as all ones; CAP_SYS_ADMIN in the namespace owning the mount namespace permits bind mounts and tmpfs — so the uid mapping, not the namespace itself, decides whether an exec'd payload can mount | queued | 2026-10-20 | 180d | — |

## Hand-off notes for L1

- The row pair supports a QUALITY-29-shaped statement without borrowing a host fact: the isolation gate must
  key on the inner mount/cmp exit status, and a `--map-current-user` run is a *forced* failure input, not a
  fallback. Message-text matching is only valid for the two-positional invocation shape (see [UNK] above).
- `ScoutUnshareHost.md` (sibling item) carries the observed probe; these rows carry the *reason* the probe
  behaves as it does, so a lesson can cite one document per claim class (observation vs rule).
- If L1 wants a single row instead of two, keep the util-linux row and fold the two man-pages sentences into
  its `teaches` cell; the `capabilities.7` quote is the load-bearing one.

## Limits

- I did not execute `mount` in any form. The host pause plus the payload rule ("payloads must be canary
  writes into /tmp, never a host binary") make that out of bounds; the observed message is quoted from
  `ScoutUnshareHost.md`, and my contribution is the source path that explains it.
- I did not run `python3`/`git` inside the lane beyond read-only `git ls-remote` and `git log -1`; no lane
  write, no jj.
- Branch tracing stops at the fetched files: `fs_context`/`do_new_mount` kernel code was not fetched, so the
  FS_USERNS_MOUNT mechanism is cited from `user_namespaces.7`, not from kernel source.
- Only the four unshare options named in the assignment were traced; `--map-users`/`--map-groups`,
  subuid persistence, `--fork` signal handling and `-N/--namespace` were not.

## Installs

none (no tool installed or upgraded; only curl, git, sha256sum, python3 and util-linux's own unshare were run,
the last with an inert `id -u` payload).
