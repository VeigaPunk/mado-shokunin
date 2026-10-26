#!/bin/sh
# probe-shell-semantics.sh -- measures the /bin/sh (bash 5.3) semantics that
# mado-terminal.py models but that are not visible in the xdg-terminal-exec
# source itself: field splitting, `read` boundaries, command -v, printf %b,
# find expression precedence.  Read-only; writes only under ${TMPDIR:-.}.
#
# Usage: TMPDIR=<scratch> ./probe-shell-semantics.sh > receipts/probes.txt
set -u
S=${TMPDIR:-.}
W=$S/probe-semantics.$$
mkdir -p "$W" || exit 1

echo "# shell: $(readlink -f /bin/sh) $($SHELL -c 'echo $BASH_VERSION' 2>/dev/null || /bin/sh -c 'echo $BASH_VERSION')"
echo "# date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo
echo "== 1. unquoted split of a variable with IFS=':' (trailing delimiter only) =="
for v in 'a::' 'a:::' '::' '' 'a::b:' ':a:' 'a'; do
	printf 'v=[%s] ->' "$v"
	/bin/sh -c 'v=$1; IFS=:; for x in $v; do printf "<%s>" "$x"; done; echo' _ "$v"
done
echo
echo "== 2. while read EXITS on the last line when it has no terminating newline =="
printf 'a\nb' > "$W/f1"; printf 'a\nb\n' > "$W/f2"
printf 'no-final-newline: '; /bin/sh -c 'n=0; while IFS= read -r l; do n=$((n+1)); done < "$1"; echo "lines=$n"' _ "$W/f1"
printf 'with-final-newline: '; /bin/sh -c 'n=0; while IFS= read -r l; do n=$((n+1)); done < "$1"; echo "lines=$n"' _ "$W/f2"
echo
echo "== 3. read trims space/tab with the default IFS; IFS= read does not =="
printf '  a b  \t\n   \n' > "$W/f3"
printf 'default IFS: '; /bin/sh -c 'while read -r l; do printf "[%s]" "$l"; done < "$1"; echo' _ "$W/f3"
printf 'IFS= read  : '; /bin/sh -c 'while IFS= read -r l; do printf "[%s]" "$l"; done < "$1"; echo' _ "$W/f3"
echo
echo "== 4. function status = status of the last command the body ran =="
printf '[Grp]\n' > "$W/f4"; printf '[Grp]\n\n' > "$W/f5"
printf 'ends on a skipped group header: '; /bin/sh -c 'f() { r=false; while IFS= read -r l; do case $l in "["*) [ "$r" = true ] && break ;; esac; done < "$1"; }; f "$1"; echo "rc=$?"' _ "$W/f4"
printf 'same + trailing blank line   : '; /bin/sh -c 'f() { r=false; while IFS= read -r l; do case $l in "["*) [ "$r" = true ] && break ;; esac; done < "$1"; }; f "$1"; echo "rc=$?"' _ "$W/f5"
echo
echo "== 5. command -v resolves keywords, builtins, aliases, functions; not dirs =="
for name in '' cd printf '[' : true if esac coproc '%' 'a=b'; do
	/bin/sh -c 'command -v "$1" >/dev/null 2>&1; printf "%-12s rc=%d\n" "[$1]" "$?"' _ "$name"
done
mkdir -p "$W/pb/adir"; printf '#!/bin/sh\n' > "$W/pb/nox"; chmod 644 "$W/pb/nox"
printf 'PATH entry that is a directory: '; /bin/sh -c 'PATH=$1 command -v adir >/dev/null; echo rc=$?' _ "$W/pb"
printf 'PATH entry not executable    : '; /bin/sh -c 'PATH=$1 command -v nox >/dev/null; echo rc=$?' _ "$W/pb"
printf 'alias name                   : '; /bin/sh -c 'alias X.desktop="p=q"; command -v X.desktop >/dev/null; echo rc=$?'
printf 'own shell function           : '; /bin/sh -c 'find_entry() { :; }; command -v find_entry >/dev/null; echo rc=$?'
echo
echo "== 6. printf %b =="
/bin/sh -c "printf '%b' 'a\tb' | od -An -c"
/bin/sh -c "printf '%b' 'q\zq' | od -An -c"
/bin/sh -c "printf '%b' '\101\x41' | od -An -c"
/bin/sh -c "printf '%b' 'e\c f' | od -An -c"
echo
echo "== 7. read var1 var2 with IFS='=' : the last variable =="
for v in 'a' 'a=' 'a==' 'a=b=' 'a=b' '=a'; do
	printf '%s\n' "--dir=$v" > "$W/f7"
	/bin/sh -c 'IFS="=" read -r a b < "$1"; printf "in=[%s] a=[%s] b=[%s]\n" "$2" "$a" "$b"' _ "$W/f7" "--dir=$v"
done
printf '%s\n' '--dir=a' 'b' > "$W/f8"
printf 'raw newline value: '; /bin/sh -c 'v="--dir=a
b"; IFS="=" read -r a b <<- EOF
	$v
	EOF
printf "a=[%s] b=[%s]\n" "$a" "$b"'
echo
echo "== 8. find: only the first -o group keeps -type f (implicit -a binds tighter) =="
mkdir -p "$W/d1" "$W/d2/Dir.desktop" "$W/d2/sub"
printf 'x\n' > "$W/d1/A.desktop"; printf 'x\n' > "$W/d1/B.desktop"
printf 'x\n' > "$W/d2/sub/C.desktop"
D1=$W/d1; D2=$W/d2
echo '-- group1 has -type f, group2 does not --'
find -L "$D1/." "$D2/." -type f -o \( -path "$D2/./[a-zA-Z0-9_]*.desktop" \) 2>/dev/null
echo '-- the starting point is printed only if it matches the expression --'
find -L "$D1/." -maxdepth 0 -type f 2>&1; echo "(nothing above = start filtered)"
echo '-- paths are printed as <dir>/./<rel>, pre-order DFS in readdir order --'
find -L "$D1/." "$D2/." -type f 2>/dev/null
echo
echo "== 9. a directory named *.desktop matches -path in a group without -type f =="
find -L "$D2/." -type f -o \( -path "$D2/./[a-zA-Z0-9_]*.desktop" \) 2>/dev/null
echo
echo "== 10. tr '[:upper:]' '[:lower:]' leaves non-ASCII uppercase alone =="
printf 'HYPÉrland -> '; printf '%s' 'HYPÉrland' | tr '[:upper:]' '[:lower:]' | od -An -c
rm -rf "$W"
