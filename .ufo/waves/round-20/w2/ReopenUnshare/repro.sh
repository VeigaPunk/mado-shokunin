#!/usr/bin/env bash
# ReopenUnshare (Mado round 20, wave 2) -- reproduce the S109/S112 checks.
# Mount probes run only inside private user+mount namespaces, targets under /tmp.
set -u
FETCH=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/ReopenUnshare/fetch
T=/tmp/mado-r20w2-ReopenUnshare/t
mkdir -p "$T"

echo '=== pinned file digests (expect 023e15ba..., 9df74867..., e8a67883..., e486b409..., 0fead9be..., 155d07c0..., 40a71b47...)'
sha256sum "$FETCH"/unshare.1.adoc "$FETCH"/mount.8.adoc "$FETCH"/context.c \
          "$FETCH"/context_mount.c "$FETCH"/mount.c "$FETCH"/user_namespaces.7 "$FETCH"/capabilities.7

echo '=== tag pins (network; expect a1d2b698 -> d76cbf8f and 5d300a0f -> 29e0874d)'
git ls-remote https://github.com/util-linux/util-linux 'refs/tags/v2.42.4*'
git ls-remote https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git 'refs/tags/man-pages-6.16*'

echo '=== gate quotes'
python3 - "$FETCH" <<'PY'
import re, sys
fetch = sys.argv[1]
line132 = open(fetch + '/unshare.1.adoc').read().split('\n')[131]
frags = ['mapped to the superuser UID and GID', 'mounting filesystems in the mount namespace']
print('S109 :132 fragments present:', [f in line132 for f in frags],
      'words:', len(' '.join(frags).split()))
lines = open(fetch + '/user_namespaces.7').read().split('\n')[276:280]
out = []
for l in lines:
    if l.startswith('.B '):
        out.append(l[3:])
    elif l.startswith('.'):
        continue
    else:
        out.append(l)
r = re.sub(r'\s+', ' ', ' '.join(out)).strip()
q = ("Holding CAP_SYS_ADMIN within the user namespace that owns a process's mount "
     "namespace allows that process to create bind mounts")
print('S112 :277-280 exact:', r == q, 'words:', len(r.split()))
PY

echo '=== --map-current-user: expect uid 1000, empty Current:, mount EPERM rc=32'
unshare --map-current-user --mount --propagation unchanged sh -c \
  'echo uid=$(id -u); cat /proc/self/uid_map; capsh --print | sed -n "1p"; \
   mount -t tmpfs tmpfs '"$T"'; echo tmpfs_rc=$?; mount --bind /tmp '"$T"'; echo bind_rc=$?'

echo '=== --map-root-user: expect uid 0, Current: =ep, TMPFS_OK and BIND_OK'
unshare --map-root-user --mount --propagation unchanged sh -c \
  'echo uid=$(id -u); cat /proc/self/uid_map; capsh --print | sed -n "1p"; \
   mount -t tmpfs tmpfs '"$T"' && echo TMPFS_OK; mount --bind /tmp '"$T"' && echo BIND_OK'

echo '=== --map-current-user --keep-caps: expect HAS_CAP_SYS_ADMIN_P and TMPFS_OK'
unshare --map-current-user --keep-caps --mount --propagation unchanged sh -c \
  'echo uid=$(id -u); capsh --has-p=cap_sys_admin && echo HAS_CAP_SYS_ADMIN_P || echo NO_CAP_SYS_ADMIN_P; \
   mount -t tmpfs tmpfs '"$T"' && echo TMPFS_OK || echo TMPFS_FAIL'

echo '=== --map-current-user --keep-caps with a non-setuid python payload: expect py_mount_rc 0 and CapAmb set'
unshare --map-current-user --keep-caps --mount --propagation unchanged python3 -c '
import ctypes
libc = ctypes.CDLL(None, use_errno=True)
r = libc.mount(b"tmpfs", b"/tmp/mado-r20w2-ReopenUnshare/t", b"tmpfs", 0, None)
print("py_mount_rc", r, "errno", ctypes.get_errno())
for line in open("/proc/self/status"):
    if line.startswith(("CapPrm", "CapEff", "CapAmb")):
        print(line.strip())
'
