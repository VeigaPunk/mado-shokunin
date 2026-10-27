#!/bin/sh
# R48 RevengerCache probe 3: what `LANG=C ls -LRl` actually emits, for the C1 byte-exact emulation.
# Everything under $S; nothing on the host is touched.
set -u
S=${1:-/fast/scratch/hyaku/mado-r48/RevengerCache/probe-ls}
rm -rf -- "$S"
mkdir -p "$S/d/sub" "$S/real"
export LC_ALL=C

printf 'x\n' > "$S/real/t.desktop"
printf 'yy\n' > "$S/d/b.desktop"
ln -s "$S/real/t.desktop" "$S/d/link.desktop"
ln -s /nonexistent/nope "$S/d/broken.desktop"
printf 'z\n' > "$S/d/sub/z.desktop"

echo "== ls -LRl (as gen_hash calls it, stderr dropped)"
LANG=C ls -LRl "$S/d" 2> /dev/null || true
echo
echo "== same tree without -L, for contrast"
LANG=C ls -Rl "$S/d" 2> /dev/null || true
echo
echo "== st_blocks (512-byte units) of the same names"
stat -c '%n blocks=%b size=%s mode=%A nlink=%h' "$S"/d/* "$S"/d/sub/* 2> /dev/null || true
echo
echo "== POSIXLY_CORRECT changes the block unit of the 'total' line"
printf '  default        : '; LANG=C ls -l "$S/d" 2> /dev/null | sed -n 1p || true
printf '  POSIXLY_CORRECT: '; POSIXLY_CORRECT=1 LANG=C ls -l "$S/d" 2> /dev/null | sed -n 1p || true
echo
echo "== operand order: files first, then directories, each alphabetically (what gen_hash relies on)"
mkdir -p "$S/o/zz" "$S/o/aa"
printf '1\n' > "$S/o/m.list"; printf '2\n' > "$S/o/a.list"
LANG=C ls -l "$S/o/m.list" "$S/o/zz" "$S/o/a.list" "$S/o/aa" 2> /dev/null || true
echo
echo "== nonexistent operands vanish into 2>/dev/null; their absence is the only signal"
LANG=C ls -l "$S/o/m.list" "$S/o/nope.list" 2> /dev/null || true
echo
echo "== a directory header line contains the operand spelling verbatim (no realpath)"
LANG=C ls -LRl "$S/o/../d" 2> /dev/null | sed -n 1p || true
