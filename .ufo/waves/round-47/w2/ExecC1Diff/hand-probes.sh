#!/bin/sh
# hand-probes.sh - the four ExecC1Diff holes, reproduced one by one outside the fuzz driver.
# Every tree lives under $S (scratch); XDG_CACHE_HOME points inside it; the resolver is only ever called with a
# --print-* option. Receipt: hand-receipts.txt beside this script.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
PIN_SRC=$LANE/.ufo/waves/round-47/fetch/xdg-terminal-exec
REF=$LANE/.ufo/waves/round-47/l1-draft/mado-terminal.py
OUT=$(dirname "$0")/hand-receipts.txt
S=${S:-$(mktemp -d)}
trap 'rm -rf -- "$S"' EXIT
rm -rf "$S"; mkdir -p "$S"
cp "$PIN_SRC" "$S/xte"; chmod 755 "$S/xte"
: > "$OUT"

say() { printf '%s\n' "$@" >> "$OUT"; }
run_pair() { # $1=tree $2=label ; rest = args
	t=$1; lbl=$2; shift 2
	E="env -i HOME=$t/home PATH=$t/bin:/usr/bin XDG_CONFIG_HOME=$t/home/.config XDG_CONFIG_DIRS=$t/etc/xdg \
XDG_DATA_HOME=$t/home/.local/share XDG_DATA_DIRS=$t/usr/share XDG_CURRENT_DESKTOP=Hyprland \
XDG_CACHE_HOME=$t/cache LANG=C.UTF-8"
	say "--- $lbl"
	( cd "$t" && timeout 10 $E "$S/xte" "$@" ) > "$S/o.out" 2> "$S/o.err"; orc=$?
	( cd "$t" && timeout 10 $E python3 -I "$REF" print "$@" ) > "$S/t.out" 2> "$S/t.err"; trc=$?
	say "pin  rc=$orc stdout=$(od -An -c "$S/o.out" | tr -s ' ' | tr '\n' ' ')"
	say "tool rc=$trc stdout=$(od -An -c "$S/t.out" | tr -s ' ' | tr '\n' ' ')"
	say "pin  stderr=$(head -c 200 "$S/o.err" | tr '\n' '|')"
	say "tool stderr=$(head -c 200 "$S/t.err" | tr '\n' '|')"
}
mk() { # $1 tree
	mkdir -p "$1/usr/share/applications" "$1/home/.local/share/applications" "$1/bin" "$1/cache" \
		"$1/home/.config" "$1/etc/xdg"
	printf '#!/bin/sh\nexit 1\n' > "$1/bin/foot"; chmod 755 "$1/bin/foot"
}
ENTRY='[Desktop Entry]
Type=Application
Name=foot
Exec=foot
Categories=System;TerminalEmulator;
'

say "== ExecC1Diff hand probes ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
say "pin sha256=$(sha256sum "$PIN_SRC" | cut -d' ' -f1)"
say "ref sha256=$(sha256sum "$REF" | cut -d' ' -f1)"
say ""

# H1: a directory named *.desktop in the highest-preference applications dir shadows the real entry
t=$S/h1; mk "$t"; printf '%s' "$ENTRY" > "$t/usr/share/applications/foot.desktop"
mkdir -p "$t/home/.local/share/applications/foot.desktop"
run_pair "$t" "H1 directory foot.desktop in home/.local/share/applications" --print-path
say "pin find line: $(grep -n 'set -- "\$@" -type f' "$PIN_SRC" | cut -d: -f1)"
say ""

# H1b: the same with a symlink to /dev/null (any non-regular path type is registered for dirs 2+)
t=$S/h1b; mk "$t"; printf '%s' "$ENTRY" > "$t/usr/share/applications/foot.desktop"
ln -s /dev/null "$t/home/.local/share/applications/foot.desktop"
run_pair "$t" "H1b symlink to /dev/null named foot.desktop" --print-path
say ""

# H1c: a FIFO named *.desktop makes the resolver block on the read
t=$S/h1c; mk "$t"; printf '%s' "$ENTRY" > "$t/usr/share/applications/foot.desktop"
mkfifo "$t/home/.local/share/applications/foot.desktop"
run_pair "$t" "H1c FIFO named foot.desktop (pin blocks: rc 124 = timeout)" --print-path
rm -f "$t/home/.local/share/applications/foot.desktop"
say ""

# H2: Exec[0] / TryExec that bash's `command` builtin parses as its own option
for spec in "Exec=-p" "Exec=--" "TryExec=-p" "TryExec=--"; do
	t=$S/h2-$(echo "$spec" | tr '=-' 'ab'); mk "$t"
	case "$spec" in
	Exec=*) body="$spec" ;;
	*) body="Exec=p
$spec" ;;
	esac
	printf '[Desktop Entry]\nType=Application\nName=p\n%s\nCategories=System;TerminalEmulator;\n' "$body" \
		> "$t/usr/share/applications/p.desktop"
	printf '#!/bin/sh\nexit 1\n' > "$t/bin/p"; chmod 755 "$t/bin/p"
	run_pair "$t" "H2 $spec" --print-id
done
say ""

# H3: HOME unset
t=$S/h3; mk "$t"; printf '%s' "$ENTRY" > "$t/usr/share/applications/foot.desktop"
say "--- H3 HOME unset (XDG_CONFIG_HOME and XDG_DATA_HOME unset too)"
( cd "$t" && timeout 10 env -i PATH="$t/bin:/usr/bin" XDG_CONFIG_DIRS="$t/etc/xdg" XDG_DATA_DIRS="$t/usr/share" \
	XDG_CURRENT_DESKTOP=Hyprland XDG_CACHE_HOME="$t/cache" LANG=C.UTF-8 "$S/xte" --print-id ) > "$S/o.out" 2> "$S/o.err"
orc=$?
( cd "$t" && timeout 10 env -i PATH="$t/bin:/usr/bin" XDG_CONFIG_DIRS="$t/etc/xdg" XDG_DATA_DIRS="$t/usr/share" \
	XDG_CURRENT_DESKTOP=Hyprland XDG_CACHE_HOME="$t/cache" LANG=C.UTF-8 python3 -I "$REF" print --print-id ) \
	> "$S/t.out" 2> "$S/t.err"
trc=$?
say "pin  rc=$orc stdout=$(od -An -c "$S/o.out" | tr -s ' ' | tr '\n' ' ')"
say "tool rc=$trc stdout=$(od -An -c "$S/t.out" | tr -s ' ' | tr '\n' ' ')"
say "pin  stderr=$(head -c 200 "$S/o.err" | tr '\n' '|')"
say "tool stderr=$(head -c 200 "$S/t.err" | tr '\n' '|')"
say ""

# the exact command -v check the resolver makes (x:936, x:964)
say "--- command -v table (the check at x:936 / x:964)"
for n in -p -v -V -- -pv -pV -vp -x -q --foo - -e -c -a; do
	bash -c 'command -v "$1" >/dev/null 2>&1; printf "%s -> rc=%d\n" "$1" "$?"' _ "$n" >> "$OUT"
done
say ""
say "END"
cat "$OUT"
