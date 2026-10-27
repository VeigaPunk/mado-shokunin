#!/bin/sh
# Run the gen_hash agreement harness: the REAL pinned resolver is primed inside a counter-shaped sandbox
# (no /etc, no /usr/bin, no /usr/share, no /home, no /var) and line 1 of the cache it saves is compared with
# warmcache.gen_hash() over the resolver's own XTE__CONFIGS / XTE__APPLICATIONS_DIRS.
# usage: run_hash.sh <seed> <trees>
set -eu
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/ExecRefCacheB
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
PIN=$LANE/.ufo/waves/round-47/fetch/xdg-terminal-exec
S=${SANDBOX_ROOT:-/fast/scratch/hyaku/mado-r48/ExecRefCacheB}
mkdir -p "$S/oraclebin" "$S/xbin" "$S/work" "$S/pin"
cp -f "$PIN" "$S/pin/xdg-terminal-exec"
chmod 755 "$S/pin/xdg-terminal-exec"
test "$(sha256sum "$S/pin/xdg-terminal-exec" | cut -d' ' -f1)" = 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac
for n in tr find awk ls md5sum mkdir rm sleep; do cp -f "$(realpath "/usr/bin/$n")" "$S/oraclebin/$n"; done
cat > "$S/xbin/wrapped-pin" <<'EOF'
#!/bin/sh
# run the resolver, then stay alive so its background `save_cache "$1" &` can land (bwrap --die-with-parent
# would otherwise kill it when the resolver exits)
rc=0
/oracle/xdg-terminal-exec "$@" || rc=$?
sleep 0.4
exit "$rc"
EOF
chmod 755 "$S/xbin/wrapped-pin"
exec bwrap --unshare-all --die-with-parent --new-session --clearenv \
	--ro-bind /usr/lib /usr/lib --symlink usr/lib /lib --symlink usr/lib /lib64 \
	--ro-bind "$(realpath /usr/bin/bash)" /bin/bash \
	--symlink bash /bin/sh \
	--ro-bind "$S/oraclebin" /oracle/bin \
	--ro-bind "$S/xbin" /xbin \
	--ro-bind "$S/pin/xdg-terminal-exec" /oracle/xdg-terminal-exec \
	--ro-bind "$(realpath /usr/bin/python3)" /usr/bin/python3 \
	--ro-bind "$SEAT" /mod \
	--bind "$S/work" /work \
	--dev /dev --proc /proc --tmpfs /tmp \
	--chdir /work \
	--setenv PATH /xbin:/oracle/bin --setenv LANG C --setenv LC_ALL C --setenv HOME /nonexistent \
	/usr/bin/python3 /mod/harness_hash.py /work "$1" "$2"
