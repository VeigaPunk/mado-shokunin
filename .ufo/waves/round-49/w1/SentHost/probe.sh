#!/bin/bash
# SentHost round-49 w1 — host-safety probes. READ-ONLY on host state: every run gets
# HOME/XDG_* inside $S, the real home is never a target, nothing is written outside $S.
# Deterministic: re-running regenerates every receipt under receipts/.
set -u
ulimit -f 65536                      # 64 MiB/file
S=${S:?S required, under /fast/scratch}
OUT=${OUT:?OUT required (seat receipts dir)}
case "$S" in /fast/scratch/*) ;; *) echo "refuse: S not under /fast/scratch" >&2; exit 2;; esac
mkdir -p "$S/probe" "$OUT"
cd "$S/probe" || exit 2
RB=$OUT
CK=/usr/lib/xkbcommon/xkbcli-compile-keymap
HT=/usr/lib/xkbcommon/xkbcli-how-to-type
XK=/usr/share/xkeyboard-config-2

mkdir -p home/.config home3/.config/xkb/symbols home4 fake-xkb extra/symbols rwdir
printf 'SENTINEL\n' > rwdir/canary.txt
printf 'include "%%L"\n<Multi_key> <a> <b> : "z"\n' > home/.config/XCompose
printf 'default partial alphanumeric_keys\nxkb_symbols "basic" { name[Group1]="EVIL"; key <AD01> { [ z ] }; };\n' > home3/.config/xkb/symbols/br
printf 'default partial alphanumeric_keys\nxkb_symbols "basic" { name[Group1]="EVIL3"; key <AD01> { [ x ] }; };\n' > extra/symbols/br
printf '<Multi_key> <a> <a> : "w"\n' > home4/.XCompose

runck() { env -i PATH=/usr/bin "$@" "$CK" --layout br; }

# ---- R1: compile-keymap filesystem trace, write scan, include-path order
{
  echo "# R1 compile-keymap filesystem access (env -i, HOME/XDG in scratch)"
  echo "# cmd: env -i PATH=/usr/bin HOME=\$S/home XDG_CONFIG_HOME=\$S/home/.config strace -f -e trace=%file $CK --layout br"
  env -i PATH=/usr/bin HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/.config" \
    strace -f -qq -e trace=%file -o trace-ck.txt "$CK" --layout br > /dev/null
  echo "# rc=$?"
  echo "## include-path probes in the order libxkbcommon asks for them:"
  grep -E 'newfstatat\(AT_FDCWD, "[^"]*(xkb|X11)' trace-ck.txt | sed -E 's/^[0-9]+ +//' | grep -vE "xkeyboard-config-2/"
  echo "## total %file lines: $(wc -l < trace-ck.txt)"
  echo "## write-ish opens (O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND|mkdir|rename|unlink|symlink):"
  grep -cE 'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND|mkdir|rename|unlink|symlink' trace-ck.txt
  echo "## keymap written by that run:"
  env -i PATH=/usr/bin HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/.config" "$CK" --layout br | sha256sum
  echo "## every other allowed compile mode is write-free too:"
  for mode in "--test --layout br" "--layout us" "--layout br --options compose:caps"; do
    # shellcheck disable=SC2086
    env -i PATH=/usr/bin strace -f -qq -e trace=%file -o t-mode.txt "$CK" $mode >/dev/null 2>&1
    echo "  compile-keymap $mode -> rc=$? write-opens=$(grep -cE 'O_WRONLY|O_CREAT|O_TRUNC' t-mode.txt)"
  done
} > "$RB/r1-compile-fs.txt" 2>&1

# ---- R2: isolation matrix for the compile inputs
{
  echo "# R2 compile isolation matrix (all: --layout br)"
  for tag in clean hostile inc-clean inc-hostile root extra extra-inc; do
    case $tag in
      clean)      pre="env -i PATH=/usr/bin HOME=$PWD/home XDG_CONFIG_HOME=$PWD/home/.config" ;;
      hostile)    pre="env -i PATH=/usr/bin HOME=$PWD/home3 XDG_CONFIG_HOME=$PWD/home3/.config" ;;
      inc-clean)  pre="env -i PATH=/usr/bin HOME=$PWD/home XDG_CONFIG_HOME=$PWD/home/.config" ;;
      inc-hostile)pre="env -i PATH=/usr/bin HOME=$PWD/home3 XDG_CONFIG_HOME=$PWD/home3/.config" ;;
      root)       pre="env -i PATH=/usr/bin XKB_CONFIG_ROOT=$PWD/fake-xkb" ;;
      extra)      pre="env -i PATH=/usr/bin XKB_CONFIG_EXTRA_PATH=$PWD/extra" ;;
      extra-inc)  pre="env -i PATH=/usr/bin XKB_CONFIG_EXTRA_PATH=$PWD/extra" ;;
    esac
    case $tag in inc-*|extra-inc) inc="--include=$XK" ;; *) inc="" ;; esac
    # shellcheck disable=SC2086
    printf '%-12s %s  evil=%s\n' "$tag" "$($pre "$CK" $inc --layout br 2>/dev/null | sha256sum | cut -d' ' -f1)" \
      "$($pre "$CK" $inc --layout br 2>/dev/null | grep -c 'EVIL')"
  done
  echo "# rows: clean/inc-clean are the reference (the same keymap). hostile, extra are shadowed by a user/extra"
  echo "# symbols/br that names name[Group1]=\"EVIL\". root is a compile that FAILS (see r2-root-err.txt)."
  env -i PATH=/usr/bin XKB_CONFIG_ROOT="$PWD/fake-xkb" "$CK" --layout br 2>&1 | head -6
} > "$RB/r2-include-matrix.txt" 2>&1

# ---- R3: same-work-dir planting exploit (the counter reuses one work dir)
{
  W=$PWD/work1; mkdir -p "$W/home/.config"
  c() { env -i PATH=/usr/bin HOME="$W/home" XDG_CONFIG_HOME="$W/home/.config" "$CK" --layout br; }
  ci() { env -i PATH=/usr/bin HOME="$W/home" XDG_CONFIG_HOME="$W/home/.config" "$CK" --include="$XK" --layout br; }
  echo "# R3 exploit: a directory planted under the counter's own \$XDG_CONFIG_HOME changes the fixture keymap"
  echo "before  default-include  $(c  | sha256sum)"
  mkdir -p "$W/home/.config/xkb/symbols"
  printf 'default partial alphanumeric_keys\nxkb_symbols "basic" { name[Group1]="EVIL2"; key <AD01> { [ q ] }; };\n' > "$W/home/.config/xkb/symbols/br"
  echo "after   default-include  $(c  | sha256sum)   evil=$(c | grep -c EVIL2)"
  echo "before  --include        $(ci | sha256sum)"
  echo "after   --include        $(ci | sha256sum)   evil=$(ci | grep -c EVIL2)"
} > "$RB/r3-workdir-planting.txt" 2>&1

# ---- R4: how-to-type filesystem access with and without --disable-compose
{
  env -i PATH=/usr/bin HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/.config" "$CK" --layout br > br.xkb
  echo "# R4 how-to-type --keymap: compose ON vs --disable-compose"
  env -i PATH=/usr/bin HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/.config" \
    strace -f -qq -e trace=%file -o t-ht-compose.txt "$HT" --keymap=br.xkb --keysym slash > ht-compose.out 2>&1
  env -i PATH=/usr/bin HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/.config" \
    strace -f -qq -e trace=%file -o t-ht-nocompose.txt "$HT" --keymap=br.xkb --disable-compose --keysym slash > ht-nocompose.out 2>&1
  echo "## non-loader paths read WITH compose:"; grep -vE 'ld\.so|libxkbcommon|libc\.so' t-ht-compose.txt | sed -E 's/^[0-9]+ +//'
  echo "## non-loader paths read WITH --disable-compose:"; grep -vE 'ld\.so|libxkbcommon|libc\.so' t-ht-nocompose.txt | sed -E 's/^[0-9]+ +//'
  echo "## write-ish opens, both runs:"; grep -cE 'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC' t-ht-compose.txt t-ht-nocompose.txt
  echo "## stdout diff (compose-on minus compose-off):"; diff ht-nocompose.out ht-compose.out || true
  echo "## \$XCOMPOSEFILE is honoured ahead of the XDG/default compose files:"
  printf '<Multi_key> <x> <y> : "q"\n' > xcf.txt
  env -i PATH=/usr/bin HOME="$PWD/home" XCOMPOSEFILE="$PWD/xcf.txt" \
    strace -f -qq -e trace=%file -o t-ht-xcf.txt "$HT" --keymap=br.xkb --keysym slash >/dev/null 2>&1
  grep -E 'xcf\.txt|XCompose' t-ht-xcf.txt | sed -E 's/^[0-9]+ +//' | sed "s#$PWD#<scratch>#"
  echo "## \$HOME/.XCompose is probed when the XDG compose file is absent:"
  mkdir -p home5; printf '<Multi_key> <a> <a> : "w"\n' > home5/.XCompose
  env -i PATH=/usr/bin HOME="$PWD/home5" \
    strace -f -qq -e trace=%file -o t-ht-h5.txt "$HT" --keymap=br.xkb --keysym slash >/dev/null 2>&1
  grep -iE 'compose' t-ht-h5.txt | sed -E 's/^[0-9]+ +//' | sed "s#$PWD#<scratch>#"
} > "$RB/r4-howtotype-fs.txt" 2>&1

# ---- R5: judge contract facts the counter compares against
{
  J() { env -i PATH=/usr/bin "$HT" "$@"; }
  echo "# R5 judge (pinned how-to-type) exit codes and stdout shape"
  for a in slash Return nosuchsym; do
    J --keymap=br.xkb --disable-compose --keysym "$a" > o.txt 2> e.txt; rc=$?
    echo "--keysym $a -> rc=$rc stdout_lines=$(wc -l < o.txt) stderr_first=$(head -1 e.txt)"
  done
  for a in 0x0060 96 0x1008FF1B; do
    J --keymap=br.xkb --disable-compose --keysym "$a" > o.txt 2>&1
    echo "--keysym $a -> rc=$? first_line=$(head -1 o.txt)"
  done
  echo "## XKB_CONFIG_ROOT has no effect once --keymap is given:"
  env -i PATH=/usr/bin XKB_CONFIG_ROOT="$PWD/fake-xkb" "$HT" --keymap=br.xkb --disable-compose --keysym slash > k.out 2>&1
  cmp -s k.out ht-nocompose.out && echo "identical to the clean-env run"
  echo "## RMLVO mode (no --keymap) DOES read the host tree:"
  env -i PATH=/usr/bin HOME="$PWD/home" strace -f -qq -e trace=%file -o t-rmlvo.txt "$HT" \
    --rules evdev --layout br --disable-compose --keysym slash > rmlvo-clean.out 2>&1
  echo "host-tree opens: $(grep -c 'xkeyboard-config-2' t-rmlvo.txt)"
  env -i PATH=/usr/bin HOME="$PWD/home3" XDG_CONFIG_HOME="$PWD/home3/.config" "$HT" \
    --rules evdev --layout br --disable-compose --keysym slash > rmlvo-hostile.out 2>&1
  echo "clean rows=$(grep -c '^[0-9]' rmlvo-clean.out) hostile-rows=$(grep -c '^[0-9]' rmlvo-hostile.out)"
} > "$RB/r5-judge-contract.txt" 2>&1

# ---- R6: bwrap sandbox recipe (judge + tool) and visibility
{
  echo "# R6 bwrap recipe that runs the judge with no host home in view"
  bwrap --unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-net --die-with-parent --new-session \
    --ro-bind "$HT" /judge --ro-bind /usr/lib/libxkbcommon.so.0 /usr/lib/libxkbcommon.so.0 \
    --ro-bind /usr/lib/libc.so.6 /usr/lib/libc.so.6 --ro-bind /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2 \
    --ro-bind /etc/ld.so.cache /etc/ld.so.cache --bind "$PWD/br.xkb" /k.xkb --dev /dev --proc /proc --tmpfs /tmp \
    --clearenv /judge --keymap=/k.xkb --disable-compose --keysym slash
  echo "# rc=$?"
  echo "## why the loader bind path matters: /lib -> usr/lib, /lib64 is real"
  ls -l /lib | sed 's/  */ /g'; ls -l /lib64/ld-linux-x86-64.so.2 | sed 's/  */ /g'
  readelf -l "$HT" | grep 'interpreter'
  echo "## the loader must be bound at its interpreter path (/lib64/...), not /usr/lib/ld-linux-x86-64.so.2:"
  bwrap --unshare-user --ro-bind "$HT" /judge --ro-bind /usr/lib/libxkbcommon.so.0 /usr/lib/libxkbcommon.so.0 \
    --ro-bind /usr/lib/libc.so.6 /usr/lib/libc.so.6 --ro-bind /usr/lib/ld-linux-x86-64.so.2 /usr/lib/ld-linux-x86-64.so.2 \
    --bind "$PWD/br.xkb" /k.xkb --dev /dev /judge --keymap=/k.xkb --disable-compose --keysym slash 2>&1 | head -2
  echo "## visibility inside (no /home, no /run/user, no /etc/xkb, no net):"
  bwrap --unshare-user --unshare-pid --unshare-net --die-with-parent --clearenv \
    --ro-bind /usr /usr --ro-bind /lib64 /lib64 --ro-bind /etc/ld.so.cache /etc/ld.so.cache \
    --bind "$PWD/br.xkb" /k.xkb --dev /dev --proc /proc --tmpfs /tmp \
    /usr/bin/sh -c 'ls -A /; ls -d /home /root /run/user /etc/xkb 2>&1; ls /sys/class/net 2>&1 | head -2' 2>&1
  echo "## canary unchanged after a judge run:"
  sha256sum rwdir/canary.txt
  echo "## --clearenv matters: variable NAMES visible inside the sandbox (values are not printed)"
  pre() { bwrap --unshare-user --die-with-parent --ro-bind /usr /usr --ro-bind /lib64 /lib64 \
            --bind "$PWD/br.xkb" /k.xkb "$@"; }
  echo "without --clearenv: $(pre /usr/bin/env 2>/dev/null | wc -l) vars; sample: $(pre /usr/bin/env 2>/dev/null | cut -d= -f1 | grep -E 'WINDOWID|XDG_CONFIG_DIRS|HYPRLAND|XAUTHORITY' | sort | tr '\n' ' ')"
  echo "with    --clearenv: $(pre --clearenv /usr/bin/env 2>/dev/null | wc -l) vars"
} > "$RB/r6-bwrap.txt" 2>&1

# ---- R7: hyprctl read verbs — write scan
{
  echo "# R7 hyprctl read verbs, %file trace, write scan"
  for v in "version" "binds -j" "getoption input:resolve_binds_by_sym -j" "devices -j"; do
    # shellcheck disable=SC2086
    env -i PATH=/usr/bin HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/.config" XDG_RUNTIME_DIR=/run/user/1000 \
      HYPRLAND_INSTANCE_SIGNATURE="$HYPRLAND_INSTANCE_SIGNATURE" \
      strace -f -qq -e trace=%file -o t-hypr.txt hyprctl $v > hypr.out 2>&1
    rc=$?
    echo "hyprctl $v -> rc=$rc bytes=$(wc -c < hypr.out) writes=$(grep -cE 'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC' t-hypr.txt)"
    echo "  distinct path roots touched: $(sed -E 's/^[0-9]+ +//' t-hypr.txt | grep -oE '"[^"]+"' | tr -d '\"' | grep '^/' | sed -E 's#^(/[^/]+/[^/]+)/.*#\1#' | sort -u | tr '\n' ' ')"
    echo "  home-path hits: $(grep -c "$PWD/home" t-hypr.txt)"
  done
  echo "## binds shape (no names committed):"
  env -i PATH=/usr/bin HOME="$PWD/home" HYPRLAND_INSTANCE_SIGNATURE="$HYPRLAND_INSTANCE_SIGNATURE" \
    hyprctl binds -j 2>/dev/null | python3 -c 'import json,sys;d=json.load(sys.stdin);print("binds=%d fields=%s"%(len(d),",".join(sorted(d[0]))))'
  echo "## getoption:"
  env -i PATH=/usr/bin HOME="$PWD/home" HYPRLAND_INSTANCE_SIGNATURE="$HYPRLAND_INSTANCE_SIGNATURE" \
    hyprctl getoption input:resolve_binds_by_sym -j 2>&1
  echo "## the only network syscall is a connect to the compositor socket:"
  env -i PATH=/usr/bin HOME="$PWD/home" XDG_RUNTIME_DIR=/run/user/1000 HYPRLAND_INSTANCE_SIGNATURE="$HYPRLAND_INSTANCE_SIGNATURE" \
    strace -f -qq -e trace=%network -o t-hypr-net.txt hyprctl binds -j >/dev/null 2>&1
  sed -E 's/^[0-9]+ +//' t-hypr-net.txt | grep -vE '^\+\+\+|^---' \
    | sed -E 's#/run/user/[0-9]+/hypr/[^/"]+#/run/user/<uid>/hypr/<sig>#; s#/run/user/[0-9]+#/run/user/<uid>#g' | head -4
  echo "## (the instance signature, a live per-session value, is redacted to <sig>; never commit it)"
  echo "## without the signature var it refuses (so the counter must not rely on ambient env):"
  env -i PATH=/usr/bin HOME="$PWD/home" hyprctl binds -j 2>&1 | head -1
} > "$RB/r7-hyprctl.txt" 2>&1

# ---- R8: keysym header census (what a runtime read would depend on)
{
  H=/usr/include/xkbcommon/xkbcommon-keysyms.h
  echo "# R8 $H"
  sha256sum "$H"
  echo "lines: $(wc -l < "$H")  bytes: $(wc -c < "$H")"
  echo "#define XKB_KEY_ lines: $(grep -c '^#define XKB_KEY_' "$H")"
  echo "occurrences of XKB_KEY_: $(grep -o 'XKB_KEY_' "$H" | wc -l)"
  echo "lines containing XKB_KEY_: $(grep -c 'XKB_KEY_' "$H")"
} > "$RB/r8-header.txt" 2>&1

# ---- R9: operator-owned paths, shape only (~ substitution, no listings)
{
  echo "# R9 operator-owned state, digest only (stat + sha256; directories are not listed)"
  for p in "$HOME/.XCompose" "$HOME/.config/xkb" "$HOME/.xkb" "$HOME/.cache/xdg-terminal-exec" \
           /etc/xkb "$XK" /usr/share/xkeyboard-config-2.d /usr/share/xkeyboard-config.d \
           "$XK/symbols/br" "$XK/rules/evdev"; do
    if [ -e "$p" ]; then
      meta=$(stat -c '%F %s %Y' "$p")
      if [ -f "$p" ]; then h=$(sha256sum "$p" | cut -d' ' -f1); else h=dir; fi
      case $p in "$HOME"/*) label=operator-owned ;; *) label=package-file ;; esac
      echo "present $label ${p//$HOME/\~} | $meta | $h"
    else
      echo "absent  ${p//$HOME/\~}"
    fi
  done
  echo "## package versions (read from the pacman local db, no transaction):"
  for d in /var/lib/pacman/local/xkeyboard-config-* /var/lib/pacman/local/libxkbcommon-[0-9]*; do
    [ -f "$d/desc" ] && printf '%s ' "$(basename "$d")" && sed -n '5p' "$d/desc"
  done
} > "$RB/r9-operator-state.txt" 2>&1

# ---- R11: what the counter's python tool run may and may not do
{
  echo "# R11 tool-run mechanics for a python3 tool inside the sandbox"
  echo "python: $(python3 -VV 2>&1 | head -1)"
  echo "## -I drops the script's directory from sys.path (Python 3.14): a two-file tool cannot import its sibling"
  mkdir -p pyw; cd pyw || return 1
  printf 'VALUE=1\n' > helper.py; printf 'import helper\nprint("ok", helper.VALUE)\n' > main.py
  env -i PATH=/usr/bin /usr/bin/python3 -I main.py 2>&1 | tail -1
  echo "## without -I the same import writes bytecode next to the module (a write inside the sandbox):"
  env -i PATH=/usr/bin /usr/bin/python3 main.py 2>&1 | tail -1
  find . -name '*.pyc' | sed 's#^#  #'
  echo "## -I implies -E, so PYTHONDONTWRITEBYTECODE is ignored; -B must be a command-line flag:"
  rm -rf __pycache__
  env -i PATH=/usr/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I main.py >/dev/null 2>&1
  env -i PATH=/usr/bin /usr/bin/python3 -I -B main.py >/dev/null 2>&1
  echo "  pyc files after -I (with the env var set) + -B: $(find . -name '*.pyc' | wc -l)"
  cd ..
  echo "## /usr/bin/xkbcli is a dispatcher: it execve's the pinned /usr/lib/xkbcommon binary"
  env -i PATH=/usr/bin strace -f -qq -e trace=%process -o t-disp.txt /usr/bin/xkbcli how-to-type \
    --keymap=br.xkb --disable-compose --keysym slash >/dev/null 2>&1
  grep -o 'execve("[^"]*"' t-disp.txt | sed 's/^/  /'
  echo "## xkbcli list write-opens: $(env -i PATH=/usr/bin strace -f -qq -e trace=%file -o t-list.txt /usr/lib/xkbcommon/xkbcli-list >/dev/null 2>&1; grep -cE 'O_WRONLY|O_CREAT|O_TRUNC' t-list.txt)"
  echo "## sandbox tooling present: bwrap $(bwrap --version | awk '{print $2}'), strace $(strace -V 2>&1 | head -1 | awk '{print $NF}')"
} > "$RB/r11-tool-runnasium.txt" 2>&1
mv "$RB/r11-tool-runnasium.txt" "$RB/r11-tool-run.txt" 2>/dev/null

# ---- R10: pins used by this seat
{
  echo "# R10 pins (sha256 of the binaries and file this seat relies on)"
  sha256sum "$CK" "$HT" /usr/include/xkbcommon/xkbcommon-keysyms.h /usr/bin/xkbcli /usr/bin/hyprctl
} > "$RB/r10-pins.txt" 2>&1

echo "wrote receipts to $RB"
ls -l "$RB"
