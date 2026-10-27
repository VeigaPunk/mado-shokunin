#!/bin/bash
# SentHost probe (round 48 w1) - host-safety review of the round's probes.
# Read-only against the host: the only host file read is the xdg-terminal-exec cache's
# metadata and sha256 (never written, never deleted, never printed). Every run of the
# resolver/pin gets XDG_CACHE_HOME inside the scratch tree. No compositor verb except
# `hyprctl devices -j` piped into a filter that prints counts and key names only.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
R_OUT=$HERE/receipts
mkdir -p "$R_OUT"
S=$(mktemp -d -p /fast/scratch/hyaku/mado-r48/SentHost 2>/dev/null || { mkdir -p /fast/scratch/hyaku/mado-r48/SentHost; mktemp -d -p /fast/scratch/hyaku/mado-r48/SentHost; })
trap 'rm -rf -- "$S"' EXIT
PIN=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec
HOSTCACHE=/home/vgpnk/.cache/xdg-terminal-exec
now(){ date -u +%Y-%m-%dT%H:%M:%SZ; }
cache_sig(){ stat -c 'size=%s mode=%a mtime=%Y inode=%i' "$HOSTCACHE" 2>/dev/null || echo absent; sha256sum "$HOSTCACHE" 2>/dev/null | cut -d' ' -f1; }

# ---------- 1. host cache baseline (metadata + hash only) --------------------
{
  echo "# host cache signature BEFORE the probes ($(now))"
  echo "path: $HOSTCACHE"
  cache_sig
  echo "# round-47 record, for comparison (ScoutHeld H-h / round-47 RevengerCache): sha256 f497ed05... 190 B"
} > "$R_OUT/01-host-cache-before.txt"
before=$(cache_sig)

# ---------- 2. fixture (scratch only) ---------------------------------------
R=$S/case
mkdir -p "$R/home/.config" "$R/data/applications" "$R/rw" "$R/bin"
printf 'foo.desktop\n' > "$R/home/.config/xdg-terminals.list"
printf '[Desktop Entry]\nType=Application\nName=Foo\nExec=foo\nCategories=TerminalEmulator;\n' > "$R/data/applications/foo.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foo"; chmod +x "$R/bin/foo"
chmod -R a+rX "$R"; chmod 777 "$R/rw"
E=(env -i PATH="$R/bin:/usr/bin:/bin" HOME="$R/home" XDG_CACHE_HOME="$R/rw"
   XDG_CONFIG_HOME="$R/home/.config" XDG_DATA_HOME="$R/data" LC_ALL=C)
settle(){ local i=0; while [ ! -s "$R/rw/xdg-terminal-exec" ] && [ $i -lt 300 ]; do sleep 0.01; i=$((i+1)); done; }
show(){ if [ -e "$R/rw/xdg-terminal-exec" ]; then echo "  cache: present $(stat -c %s "$R/rw/xdg-terminal-exec") B mode $(stat -c %a "$R/rw/xdg-terminal-exec")"; else echo "  cache: ABSENT"; fi; }

# ---------- 3. priming race ------------------------------------------------
{
  echo "# priming a cache: four shapers, and the three-repeat poll"
  echo "# sandbox = the round-47 counter's shaper (--unshare-all --die-with-parent --new-session --clearenv,"
  echo "#   ro-bind /usr, loader symlinks, --proc --dev --tmpfs /tmp, case root ro, <root>/rw rw)"
  B=(/usr/bin/bwrap --unshare-all --die-with-parent --new-session --clearenv
     --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin
     --proc /proc --dev /dev --tmpfs /tmp --ro-bind "$R" "$R" --bind "$R/rw" "$R/rw")
  SE=(--setenv PATH "$R/bin:/usr/bin:/bin" --setenv HOME "$R/home" --setenv XDG_CACHE_HOME "$R/rw"
      --setenv XDG_CONFIG_HOME "$R/home/.config" --setenv XDG_DATA_HOME "$R/data" --setenv LC_ALL C)
  run_variant(){ local name=$1; shift; rm -f "$R/rw/xdg-terminal-exec"
    "${B[@]}" "${SE[@]}" /bin/sh -c "$*" >/dev/null 2>&1
    printf '%-58s' "$name"; show; }
  echo "A: sandbox exits when the pin returns, no wait at all"
  run_variant "sh -c 'pin --print-cmd'"            'xdg-terminal-exec --print-cmd'
  echo "B: --as-pid-1 (sh is pid 1) + wait"
  rm -f "$R/rw/xdg-terminal-exec"
  "${B[@]}" --as-pid-1 "${SE[@]}" /bin/sh -c 'xdg-terminal-exec --print-cmd; wait' >/dev/null 2>&1
  printf '%-58s' "--as-pid-1 sh -c 'pin; wait'"; show
  echo "C: default init, busy poll without a sleep (300 shell iterations, ~1 ms)"
  run_variant "sh -c 'pin; while [ ! -s cache ]; do :; done' x300" \
    'xdg-terminal-exec --print-cmd; i=0; while [ ! -s "$XDG_CACHE_HOME/xdg-terminal-exec" ] && [ $i -lt 300 ]; do i=$((i+1)); done'
  echo "D: default init, keep the sandbox alive with a bounded sleep poll (the guard)"
  for k in 1 2 3; do
    rm -f "$R/rw/xdg-terminal-exec"; t0=$(date +%s%N)
    "${B[@]}" "${SE[@]}" /bin/sh -c 'xdg-terminal-exec --print-cmd; i=0; while [ ! -s "$XDG_CACHE_HOME/xdg-terminal-exec" ] && [ $i -lt 500 ]; do sleep 0.01; i=$((i+1)); done; [ -s "$XDG_CACHE_HOME/xdg-terminal-exec" ]' >/dev/null 2>&1
    rc=$?; t1=$(date +%s%N); printf '  poll+sleep run %s: wrapper_rc=%s latency=%s ms size=%s B\n' "$k" "$rc" "$(( (t1-t0)/1000000 ))" "$(stat -c %s "$R/rw/xdg-terminal-exec" 2>/dev/null || echo 0)"
  done
  echo "E: outside bwrap, the same race: 5 cold runs, time until the cache file settles"
  for k in 1 2 3 4 5; do rm -f "$R/rw/xdg-terminal-exec"; t0=$(date +%s%N)
    "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; settle; t1=$(date +%s%N)
    printf '  run %s: %s ms size=%s\n' "$k" "$(( (t1-t0)/1000000 ))" "$(stat -c %s "$R/rw/xdg-terminal-exec" 2>/dev/null || echo 0)"; done
  echo "# the pin writes the cache in a background child (pin :1457 'save_cache \"\$1\" &'); when the"
  echo "# sandbox exits with the pin, the pid-namespace init takes the child with it (variants A-C)."
} > "$R_OUT/02-prime-race.txt"

# ---------- 4. cache mutation paths ---------------------------------------
{
  echo "# what an unredirected run of the resolver does to the cache file"
  echo "1) cold run (XDG_CACHE_HOME redirected):"
  "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; settle; show
  echo "2) XTE_CACHE_ENABLED=false --print-cmd  (pin :1172-1180 skips read_cache, :336-337 runs rm -f):"
  "${E[@]}" XTE_CACHE_ENABLED=false /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; sleep 0.3; show
  echo "3) recreate, then a '/disable_cache' line in the list file (read first at :1180, directive seen"
  echo "   during the cold pass, save_cache -> rm -f):"
  printf 'foo.desktop\n' > "$R/home/.config/xdg-terminals.list"
  "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; settle; show
  printf '/disable_cache\nfoo.desktop\n' > "$R/home/.config/xdg-terminals.list"
  "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; sleep 0.3; show
  echo "4) recreate, then a warm run (XTE__CACHE_USED=true, :1456 gates the save):"
  printf 'foo.desktop\n' > "$R/home/.config/xdg-terminals.list"
  "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; settle; show
  "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; sleep 0.3; show
  echo "5) the oracle's own verdict (XTE_DEBUG=1, stderr only; stdout unchanged):"
  printf 'foo.desktop\n' > "$R/home/.config/xdg-terminals.list"
  "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null; settle
  "${E[@]}" XTE_DEBUG=1 /usr/bin/xdg-terminal-exec --print-cmd >/dev/null 2>"$S/w.err"; grep -c '^D: cache is actual' "$S/w.err" | sed 's/^/  warm run: lines matching "D: cache is actual" = /'
  rm -f "$R/rw/xdg-terminal-exec"
  "${E[@]}" XTE_DEBUG=1 /usr/bin/xdg-terminal-exec --print-cmd >/dev/null 2>"$S/c.err"; grep -c '^D: no cache data' "$S/c.err" | sed 's/^/  cold run: lines matching "D: no cache data" = /'
  echo "# XTE_DEBUG (or DEBUG) is read at pin :61; debug goes to stderr, so a scored stdout is unchanged."
  echo "6) which modes reach the save site at all (pin :1368-1385 bails out early for id/path/content):"
  sleep 0.3; rm -f "$R/rw/xdg-terminal-exec"; sleep 0.3   # drain any writer left by section 5
  for mode in --print-id --print-path --print-cmd; do
    rm -f "$R/rw/xdg-terminal-exec"; sleep 0.2
    printf 'foo.desktop\n' > "$R/home/.config/xdg-terminals.list"
    "${E[@]}" /usr/bin/xdg-terminal-exec $mode >/dev/null 2>&1; settle
    cold=$(stat -c %s "$R/rw/xdg-terminal-exec" 2>/dev/null || echo 0)
    "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null 2>&1; sleep 0.2
    mk(){ rm -f "$R/rw/xdg-terminal-exec"; "${E[@]}" /usr/bin/xdg-terminal-exec --print-cmd >/dev/null 2>&1; sleep 0.2; }
    mk; b=$(stat -c %s "$R/rw/xdg-terminal-exec" 2>/dev/null || echo 0)
    "${E[@]}" XTE_CACHE_ENABLED=false /usr/bin/xdg-terminal-exec $mode >/dev/null 2>&1; sleep 0.3
    a=$(stat -c %s "$R/rw/xdg-terminal-exec" 2>/dev/null || echo 0)
    printf '  %-12s cold run leaves cache=%s B; with XTE_CACHE_ENABLED=false: before=%s B after=%s B\n' "$mode" "$cold" "$b" "$a"
  done
  echo "# only the modes that continue past :1370 ('cmd' and the empty/launch case) write, overwrite or"
  echo "# delete; id/path/content print, newline, exit 0 and never touch the cache file."
} > "$R_OUT/03-cache-mutation.txt"

# ---------- 5. xkbcli -----------------------------------------------------
{
  X=/usr/bin/xkbcli
  h(){ sha256sum | cut -c1-16; }
  echo "# xkbcli compile-keymap ($($X --version 2>&1 | head -1)): read-only? env-sensitive?"
  echo "1) file writes and sockets, traced (openat/creat/unlink/mkdir + socket/connect):"
  strace -f -qq -e trace=openat,creat,unlink,unlinkat,mkdir,mkdirat,socket,connect,execve,execveat -o "$S/x.tr" $X compile-keymap --layout br >/dev/null 2>&1
  printf '  write-ish ops: %s   socket/connect: %s   execve: %s\n' \
    "$(grep -cE 'O_WRONLY|O_RDWR|O_CREAT|unlink|mkdir|creat\(' "$S/x.tr")" \
    "$(grep -cE 'socket\(|connect\(' "$S/x.tr")" "$(grep -c execve "$S/x.tr")"
  grep execve "$S/x.tr" | sed 's/^/  /'
  echo "2) XKB_DEFAULT_* are inert here (a full keymap hash per run):"
  printf '  no args                           %s\n' "$($X compile-keymap 2>/dev/null | h)"
  printf '  XKB_DEFAULT_LAYOUT=br             %s\n' "$(XKB_DEFAULT_LAYOUT=br $X compile-keymap 2>/dev/null | h)"
  printf '  XKB_DEFAULT_RULES=nope (rc)       %s rc=%s\n' "$(XKB_DEFAULT_RULES=nope $X compile-keymap 2>/dev/null | h)" "$?"
  printf '  XKB_DEFAULT_OPTIONS=compose:caps  %s\n' "$(XKB_DEFAULT_OPTIONS=compose:caps $X compile-keymap 2>/dev/null | h)"
  printf '  --layout br                       %s\n' "$($X compile-keymap --layout br 2>/dev/null | h)"
  printf '  --layout br --options compose:caps %s\n' "$($X compile-keymap --layout br --options compose:caps 2>/dev/null | h)"
  echo "3) include path is env-controlled (each tree poisoned with symbols/zz):"
  mkdir -p "$S/xdg/xkb/symbols" "$S/h2/.xkb/symbols" "$S/extra/symbols"
  for f in "$S/xdg/xkb/symbols/zz" "$S/h2/.xkb/symbols/zz" "$S/extra/symbols/zz"; do
    printf 'default partial alphanumeric_keys\nxkb_symbols "basic" { name[Group1]="POISON"; };\n' > "$f"; done
  printf '  XDG_CONFIG_HOME/xkb hit: %s\n' "$(XDG_CONFIG_HOME="$S/xdg" $X compile-keymap --layout zz 2>/dev/null | grep -c POISON)"
  printf '  HOME/.xkb hit:           %s\n' "$(HOME="$S/h2" $X compile-keymap --layout zz 2>/dev/null | grep -c POISON)"
  printf '  XKB_CONFIG_EXTRA_PATH:   %s\n' "$(XKB_CONFIG_EXTRA_PATH="$S/extra" $X compile-keymap --layout zz 2>/dev/null | grep -c POISON)"
  mkdir -p "$S/emptyroot"
  printf '  XKB_CONFIG_ROOT=<empty dir> searched-root line: %s\n' "$(XKB_CONFIG_ROOT="$S/emptyroot" $X compile-keymap --layout zz 2>&1 >/dev/null | grep -A1 'include paths searched' | tail -1)"
  printf '  XKB_CONFIG_ROOT=/nonexistent searched-root line: %s\n' "$(XKB_CONFIG_ROOT=/nonexistent $X compile-keymap --layout zz 2>&1 >/dev/null | grep -A1 'include paths searched' | tail -1)"
  printf '  unset searched-root line: %s\n' "$($X compile-keymap --layout zz 2>&1 >/dev/null | grep -A1 'include paths searched' | tail -1)"
  echo "4) XKB_LOG_LEVEL decides whether the XKB-595 warning exists at all (rc stays 0 in every row):"
  for lv in UNSET 0 5 10 20 30 critical error warning none bogus; do
    if [ "$lv" = UNSET ]; then e=$($X compile-keymap --layout br --options nope:nope 2>&1 >/dev/null)
    else e=$(env XKB_LOG_LEVEL="$lv" $X compile-keymap --layout br --options nope:nope 2>&1 >/dev/null); fi
    printf '  XKB_LOG_LEVEL=%-8s XKB-595 lines=%s first=[%s]\n' "$lv" \
      "$(printf '%s' "$e" | grep -c XKB-595)" "$(printf '%s' "$e" | head -1 | cut -c1-52)"; done
  echo "5) failing lookups name the root and the defaults actually used:"
  $X compile-keymap --layout zz 2>&1 >/dev/null | sed 's/^/  /'
  echo "  -- and the defaults the host build carries (empty root forces the lookup to state them):"
  XKB_CONFIG_ROOT="$S/emptyroot" $X compile-keymap --layout zz 2>&1 >/dev/null | grep -E "Couldn't look up rules|Cannot load XKB rules" | sed 's/^/  /'
  $X compile-keymap --rules nope --layout br 2>&1 >/dev/null | sed -n '1p' | sed 's/^/  /'
  $X compile-keymap --layout br --variant nope 2>&1 >/dev/null | sed -n '1,2p' | sed 's/^/  /'
} > "$R_OUT/04-xkbcli-env.txt"

# ---------- 6. hyprctl devices: material keys ------------------------------
{
  echo "# hyprctl devices -j, shape only (no name/address value is printed anywhere)"
  hyprctl devices -j 2>/dev/null | python3 -c '
import json,sys
d=json.load(sys.stdin)
KEEP={"layout","variant","options","model","rules","main","capsLock","numLock","active_layout_index","scrollFactor","defaultSpeed"}
MATERIAL={"name","address","active_keymap"}
for k in sorted(d):
    v=d[k]
    if not isinstance(v,list):
        print("%s: %s" % (k,type(v).__name__)); continue
    keys=sorted({x for e in v if isinstance(e,dict) for x in e})
    print("%s: %d entries" % (k,len(v)))
    print("  material keys present: %s" % (",".join(sorted(set(keys)&MATERIAL)) or "none"))
    print("  shape keys present   : %s" % (",".join(sorted(set(keys)&KEEP)) or "none"))
' | sed 's/^/  /'
  echo "# name = kernel product string, address = the device node id; active_keymap = the compiled"
  echo "# layout label. Round-46's receipt committed 14 name= lines (live-devices-host-r46.txt)."
} > "$R_OUT/05-devices-shape.txt"

# ---------- 7. host tooling ----------------------------------------------
{
  echo "# tooling this round depends on"
  printf 'bwrap:  %s (%s)\n' "$(/usr/bin/bwrap --version)" "$(stat -c '%s B %y' /usr/bin/bwrap)"
  printf 'strace: %s\n' "$(/usr/bin/strace -V | head -1)"
  sysctl kernel.unprivileged_userns_clone user.max_user_namespaces 2>&1 | sed 's/^/  /'
  printf 'apparmor_restrict_unprivileged_userns: %s\n' "$(cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns 2>/dev/null || echo 'absent')"
  echo "# bwrap minimal shape that works here (loader symlinks are required):"
  /usr/bin/bwrap --unshare-all --die-with-parent --ro-bind /usr /usr --symlink usr/lib /lib \
     --symlink usr/lib64 /lib64 --symlink usr/bin /bin --proc /proc --dev /dev /usr/bin/true; echo "  rc=$?"
  echo "# without the symlinks: execvp fails (\"No such file or directory\" = missing ld-linux)"
  /usr/bin/bwrap --unshare-all --die-with-parent --ro-bind /usr /usr --proc /proc --dev /dev /usr/bin/true 2>&1 | sed 's/^/  /'
  echo "# no /etc inside: ls prints numeric ids (root-owned file -> 65534, unmapped)"
  /usr/bin/bwrap --unshare-all --die-with-parent --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin --proc /proc --dev /dev /usr/bin/ls -l /usr/bin/xdg-terminal-exec | sed 's/^/  /'
  echo "# inside the r47-shaped sandbox neither /home nor /etc exists, so an 'openat under /home' check"
  echo "# there can never fire (it is vacuous, not a guard):"
  /usr/bin/bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr/lib /usr/lib \
     --symlink usr/lib /lib --symlink usr/lib /lib64 --ro-bind /usr/bin/bash /bin/sh --ro-bind /usr/bin/bash /bin/bash \
     --dev /dev --proc /proc --tmpfs /tmp --setenv HOME /home/vgpnk --setenv PATH /bin \
     /bin/sh -c 'for p in /home /home/vgpnk /etc/xkb; do [ -e "$p" ] && echo "  visible: $p" || echo "  absent:  $p"; done'
  echo "# bwrap creates the missing parents of a bind target as EMPTY stub dirs, one level each;"
  echo "# a '/fast'-prefix path check therefore matches the legitimate case root:"
  ST="$S/stub"; C="$ST/case"; mkdir -p "$C/home" "$C/.rw"
  /usr/bin/bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr/lib /usr/lib \
     --symlink usr/lib /lib --symlink usr/lib /lib64 --ro-bind /usr/bin/bash /bin/sh --ro-bind /usr/bin/bash /bin/bash \
     --dev /dev --proc /proc --tmpfs /tmp --ro-bind "$C" "$C" --bind "$C/.rw" "$C/.rw" --setenv PATH /bin \
     /bin/sh -c 'for d in '"$ST"' '"$ST"'/case; do set -- "$d"/*; if [ -e "$1" ]; then echo "  $d: has [$1]"; else echo "  $d: empty"; fi; done; echo "  sibling seat dir readable: $([ -e '"$(dirname "$ST")"'/ExecXkbLive ] && echo YES || echo no)"'
  echo "# ambient environment of a seat shell (matters to both probes):"
  env | grep -E '^(XDG_CACHE_HOME|XDG_CONFIG_HOME|XDG_DATA_HOME|XDG_CURRENT_DESKTOP|HOME|LANG|LC_ALL|XTE_[A-Z_]+|XKB_[A-Z_]+)=' | sort | sed 's/^/  /'
} > "$R_OUT/06-host-tooling.txt"

# ---------- 7b. where a harness's cache path resolves -------------------
{
  echo '# the pin resolves its cache target as XDG_CACHE_HOME:-$HOME/.cache + /xdg-terminal-exec (pin :172-173)'
  echo '# resolved with the environment of THIS seat shell (nothing is run, nothing is opened):'
  printf '  ambient env                     -> %s\n' "$(sh -c 'XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}; echo "$XDG_CACHE_HOME/xdg-terminal-exec"')"
  printf '  ambient, XDG_CACHE_HOME unset   -> %s\n' "$(env -u XDG_CACHE_HOME sh -c 'XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}; echo "$XDG_CACHE_HOME/xdg-terminal-exec"')"
  printf '  guard env (XDG_CACHE_HOME=<work>)-> %s\n' "$(XDG_CACHE_HOME="$S/cache" sh -c 'XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}; echo "$XDG_CACHE_HOME/xdg-terminal-exec"')"
  printf '  HOME unset and XDG_CACHE_HOME unset -> [%s]\n' "$(env -u HOME -u XDG_CACHE_HOME sh -c 'XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}; echo "$XDG_CACHE_HOME/xdg-terminal-exec"')"
  echo '# the first two land on the host cache; only the third (and the counter sandbox) is outside it.'
} > "$R_OUT/08-cache-path-resolution.txt"

# ---------- 7c. HOME fallback inside the sandbox --------------------------
{
  echo '# a fixture with XDG_CACHE_HOME unset: the cache lands in $HOME/.cache, so HOME must be writable'
  B2=(/usr/bin/bwrap --unshare-all --die-with-parent --new-session --clearenv
      --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin
      --proc /proc --dev /dev --tmpfs /tmp --ro-bind "$R" "$R" --bind "$R/rw" "$R/rw")
  echo 'A) HOME under the READ-ONLY case root (r47 shape), XDG_CACHE_HOME unset:'
  rm -rf "$R/rw/home"
  "${B2[@]}" --setenv PATH "$R/bin:/usr/bin:/bin" --setenv HOME "$R/home" --setenv XDG_CONFIG_HOME "$R/home/.config" \
    --setenv XDG_DATA_HOME "$R/data" --setenv LC_ALL C /bin/sh -c \
    'xdg-terminal-exec --print-cmd; sleep 0.3; ls -d "$HOME/.cache" 2>/dev/null || echo "  no $HOME/.cache (mkdir -p failed on the read-only root)"' 2>&1 | sed 's/^/  /'
  echo 'B) HOME under the writable rw dir, XDG_CACHE_HOME unset:'
  mkdir -p "$R/rw/home/.config" "$R/rw/home/.local/share"; chmod -R 777 "$R/rw/home"
  printf 'foo.desktop\n' > "$R/rw/home/.config/xdg-terminals.list"
  cp "$R/data/applications/foo.desktop" "$R/rw/home/.local/share/." 2>/dev/null || true
  mkdir -p "$R/rw/home/.local/share/applications"; cp "$R/data/applications/foo.desktop" "$R/rw/home/.local/share/applications/"
  "${B2[@]}" --setenv PATH "$R/bin:/usr/bin:/bin" --setenv HOME "$R/rw/home" \
    --setenv XDG_CONFIG_HOME "$R/rw/home/.config" --setenv XDG_DATA_HOME "$R/rw/home/.local/share" --setenv LC_ALL C \
    /bin/sh -c 'xdg-terminal-exec --print-cmd; i=0; while [ ! -s "$HOME/.cache/xdg-terminal-exec" ] && [ $i -lt 500 ]; do sleep 0.01; i=$((i+1)); done; echo "  cache at $HOME/.cache: $(stat -c %s "$HOME/.cache/xdg-terminal-exec" 2>/dev/null || echo 0) B"' 2>&1 | sed 's/^/  /'
} > "$R_OUT/09-home-fallback.txt"

# ---------- 8. host cache after -------------------------------------------
{
  echo "# host cache signature AFTER the probes ($(now))"
  cache_sig
  echo "# BEFORE was:"
  echo "$before"
} > "$R_OUT/07-host-cache-after.txt"
after=$(cache_sig)
if [ "$before" = "$after" ]; then echo "host cache untouched: yes" >> "$R_OUT/07-host-cache-after.txt"
else echo "host cache untouched: NO - STOP AND REPORT" >> "$R_OUT/07-host-cache-after.txt"; fi
echo "receipts written to $R_OUT"
