#!/bin/sh
# Run the warm-cache fixture harness: the patched tool against the REAL pinned resolver in the
# counter-shaped sandbox (no /etc, /usr/bin, /usr/share, /home, /var; the externals are copies).
# usage: run_warm.sh
set -eu
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/ExecRefCacheB
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=${SANDBOX_ROOT:-/fast/scratch/hyaku/mado-r48/ExecRefCacheB}
mkdir -p "$S/oraclebin" "$S/xbin" "$S/work" "$S/pin" "$S/tool"
for n in tr find awk ls md5sum mkdir rm sleep cp; do cp -f "$(realpath "/usr/bin/$n")" "$S/oraclebin/$n"; done
cp -f "$LANE/.ufo/waves/round-47/fetch/xdg-terminal-exec" "$S/pin/xdg-terminal-exec"
chmod 755 "$S/pin/xdg-terminal-exec"
test "$(sha256sum "$S/pin/xdg-terminal-exec" | cut -d' ' -f1)" = 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac
cat > "$S/xbin/wrapped-pin" <<'WRAP'
#!/bin/sh
# run the resolver, then stay alive so its background `save_cache "$1" &` can land
rc=0
/oracle/xdg-terminal-exec "$@" || rc=$?
sleep 0.4
exit "$rc"
WRAP
chmod 755 "$S/xbin/wrapped-pin"

cp -f "$SEAT/mado-terminal.py" "$S/tool/mado-terminal.py"
exec bwrap --unshare-all --die-with-parent --new-session --clearenv \
	--ro-bind /usr/lib /usr/lib --symlink usr/lib /lib --symlink usr/lib /lib64 \
	--ro-bind "$(realpath /usr/bin/bash)" /bin/bash \
	--symlink bash /bin/sh \
	--ro-bind "$S/oraclebin" /oracle/bin \
	--ro-bind "$S/xbin" /xbin \
	--ro-bind "$S/pin/xdg-terminal-exec" /oracle/xdg-terminal-exec \
	--ro-bind "$S/tool/mado-terminal.py" /oracle/tool.py \
	--ro-bind "$(realpath /usr/bin/python3)" /usr/bin/python3 \
	--ro-bind "$SEAT" /mod \
	--bind "$S/work" /work \
	--dev /dev --proc /proc --tmpfs /tmp \
	--chdir /work \
	--setenv PATH /xbin:/oracle/bin --setenv LANG C --setenv LC_ALL C --setenv HOME /nonexistent \
	/usr/bin/python3 /mod/harness_warm.py /work
