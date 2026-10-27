#!/bin/sh
# Run the ls differential harness inside the counter-shaped sandbox: no /etc, no /usr/bin of the host,
# only /usr/lib + python3 + bash + a bin dir with ls, the module dir read-only, and a rw /work.
# usage: run_sandbox.sh <seed> <trees>
set -eu
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/ExecRefCacheB
S=${SANDBOX_ROOT:-/fast/scratch/hyaku/mado-r48/ExecRefCacheB}
mkdir -p "$S/lsbin" "$S/work"
cp -f "$(realpath /usr/bin/ls)" "$S/lsbin/ls"
exec bwrap --unshare-all --die-with-parent --new-session --clearenv \
	--ro-bind /usr/lib /usr/lib --symlink usr/lib /lib --symlink usr/lib /lib64 \
	--ro-bind "$(realpath /usr/bin/bash)" /bin/bash \
	--symlink bash /bin/sh \
	--ro-bind "$S/lsbin" /lsbin \
	--ro-bind "$(realpath /usr/bin/python3)" /usr/bin/python3 \
	--ro-bind "$SEAT" /mod \
	--bind "$S/work" /work \
	--dev /dev --proc /proc --tmpfs /tmp \
	--chdir /work \
	--setenv PATH /lsbin --setenv LANG C --setenv LC_ALL C --setenv HOME /nonexistent \
	/usr/bin/python3 /mod/harness_ls.py /work "$1" "$2"
