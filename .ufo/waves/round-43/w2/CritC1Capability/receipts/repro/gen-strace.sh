#!/bin/bash
set -u
S=/fast/scratch/hyaku/mado-r43/CritC1Capability
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w2/CritC1Capability
cd "$S" || exit 1
OUT="$W/receipts/strace.txt"
{
  echo "# strace of --selftest and of a real run (tool copy sha256 e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99)"
  echo
  echo '## selftest: strace -f -e trace=openat,write,clone,clone3,fork,vfork,execve,socket,connect python3 -I mado-geometry.py --selftest'
  strace -f -o st-self.log -e trace=openat,write,clone,clone3,fork,vfork,execve,socket,connect \
    python3 -I mado-geometry.py --selftest > st-self.out 2>&1
  echo "stdout: $(cat st-self.out)"
  echo
  echo '$ openat of the three selftest fixture paths:'
  grep -E 'openat\(AT_FDCWD, "(/|/dev/null|/nonexistent/none)"' st-self.log
  echo
  echo '$ write() targets seen:'
  grep -oE 'write\([0-9]+' st-self.log | sort -u
  echo
  echo '$ count of O_WRONLY or O_CREAT anywhere:'
  grep -cE 'O_WRONLY|O_CREAT' st-self.log
  echo '$ count of socket(/connect(/clone/fork:'
  grep -cE 'socket\(|connect\(|clone|fork' st-self.log
  echo '$ count of execve(:'
  grep -c 'execve(' st-self.log
  echo
  echo '## source lines holding the reads that selftest performs'
  grep -n 'read_regular(' mado-geometry.py
  echo
  echo
  echo '## real run: strace -f -e trace=openat,write,clone,clone3,fork,vfork,execve,socket,connect python3 -I mado-geometry.py --clients clients.json --rules ~/.config/hypr/gkeep.conf'
  strace -f -o st-run.log -e trace=openat,write,clone,clone3,fork,vfork,execve,socket,connect \
    python3 -I mado-geometry.py --clients clients.json --rules /home/vgpnk/.config/hypr/gkeep.conf > st-run.out 2>&1
  rc=$?
  echo "exit=$rc"
  echo 'stdout:'
  cat st-run.out
  echo
  echo '$ openat of the caller-supplied paths (and any other /home path that is not python runtime):'
  grep 'openat' st-run.log | grep -E 'clients\.json|/home/vgpnk/\.config'
  echo
  echo '$ every openat outside the python runtime/libc/locale:'
  grep 'openat' st-run.log | grep -vE '\.py|\.pyc|/usr/lib/python|site-packages|/etc/ld|/proc/self|/etc/localtime|pyvenv|_pth|pybuilddir'
  echo
  echo '$ count of socket(/connect(/clone/fork:'
  grep -cE 'socket\(|connect\(|clone|fork' st-run.log
  echo '$ execve line (the caller-started interpreter itself):'
  grep 'execve(' st-run.log | cut -c1-170
} > "$OUT" 2>&1
cat "$OUT"
