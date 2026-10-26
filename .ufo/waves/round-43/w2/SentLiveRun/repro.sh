#!/usr/bin/env bash
# Regenerate every trace of this seat from the tool at the data commit.
# Writes only into this seat directory; scratch is removed by the caller.
set -u
D=$(cd "$(dirname "$0")" && pwd)
S=$(mktemp -d -p /fast/scratch/hyaku/mado-r43) || exit 1
trap 'rm -rf -- "$S"' EXIT
T=$S/mado-geometry.py
R=$HOME/.config/hypr/gkeep.conf
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show \
  1959770657f1f8665097c1aed4be6c1cbb07139f:tools/mado-geometry.py > "$T"
hyprctl clients -j > "$S/dump-now.json"

strace -f -e trace=process,network,file -o "$D/tr-selftest.log" -s 300 \
  python3 -I "$T" --selftest > "$D/out-selftest.txt" 2> "$D/err-selftest.txt"
hyprctl clients -j | strace -f -e trace=process,network,file -o "$D/tr-hostpipe.log" -s 300 \
  python3 -I "$T" --clients - --rules "$R" > "$D/out-hostpipe.txt" 2> "$D/err-hostpipe.txt"
mkfifo "$S/fifo"
timeout 10 strace -f -e trace=process,network,file -o "$D/tr-fifo-clients.log" -s 300 \
  python3 -I "$T" --clients "$S/fifo" --rules "$R" > "$D/out-fifo-clients.txt" 2> "$D/err-fifo-clients.txt"
timeout 10 strace -f -e trace=process,network,file -o "$D/tr-fifo-rules.log" -s 300 \
  python3 -I "$T" --clients "$S/dump-now.json" --rules "$S/fifo" > "$D/out-fifo-rules.txt" 2> "$D/err-fifo-rules.txt"
timeout 10 strace -f -e trace=process,network,file -o "$D/tr-stdin-closed3.log" -s 200 \
  bash -c 'exec 0<&-; exec python3 -I "$1" --clients - --rules "$2"' _ "$T" "$R" \
  > "$D/out-stdin-closed3.txt" 2> "$D/err-stdin-closed3.txt"
timeout 10 strace -f -e trace=process,network,file -o "$D/tr-ptmx.log" -s 300 \
  python3 -I "$T" --clients "$S/dump-now.json" --rules /dev/ptmx > "$D/out-ptmx.txt" 2> "$D/err-ptmx.txt"
strace -f -e trace=write,openat,ftruncate -o "$D/tr-write-host.log" -s 120 \
  python3 -I "$T" --clients "$S/dump-now.json" --rules "$R" > "$D/out-write-host.txt" 2>&1
strace -f -e trace=write,openat,ftruncate -o "$D/tr-write-selftest.log" -s 100 \
  python3 -I "$T" --selftest > "$D/out-st3.txt" 2>&1
strace -f -e trace=openat,fstat,newfstatat,read,close -o "$D/tr-fifo-fd.log" -s 60 \
  python3 -I "$T" --clients "$S/fifo" --rules "$R" > "$D/out-fifo-fd.txt" 2> "$D/err-fifo-fd.txt"
strace -f -e trace=openat,fstat,read,close -o "$D/tr-ptmx-fd.log" -s 60 \
  python3 -I "$T" --clients "$S/dump-now.json" --rules /dev/ptmx > "$D/out-ptmx-fd.txt" 2>&1
strace -f -e trace=openat,fstat,read,close -o "$D/tr-devnull-fd.log" -s 60 \
  python3 -I "$T" --selftest > "$D/out-devnull-fd.txt" 2>&1
strace -f -e trace=openat,fstat,read,close -o "$D/tr-host-fd.log" -s 40 \
  python3 -I "$T" --clients "$S/dump-now.json" --rules "$R" > "$D/out-host-fd.txt" 2>&1
python3 "$D/summarize.py" > "$D/summary.txt"
(cd "$D" && sha256sum $(ls | grep -v '^hashes.txt$') > hashes.txt)
