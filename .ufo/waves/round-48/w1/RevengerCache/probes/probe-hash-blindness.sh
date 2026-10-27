#!/bin/sh
# R48 RevengerCache probe 1: which metadata changes the gen_hash stream cannot see.
# Rebuilds gen_hash's exact input stream for a scratch tree and compares md5s.
# Read-only outside $S; writes nothing on the host.
set -eu
S=${1:-/fast/scratch/hyaku/mado-r48/RevengerCache/probe-blind}
rm -rf -- "$S"
mkdir -p "$S/t/applications/sub"
export LC_ALL=C

printf 'Exec=term-a --flag\n' > "$S/t/applications/x.desktop"
printf 'Exec=term-sub --flag\n' > "$S/t/applications/sub/y.desktop"

# exact gen_hash stream: literal version, XDG_CURRENT_DESKTOP, LANG=C ls -LRl of the operands
h() { { printf '4\n'; printf '%s\n' "${XDG_CURRENT_DESKTOP-}"; LANG=C ls -LRl "$S/t/applications" 2>/dev/null; } | md5sum | cut -d' ' -f1; }

cp -a "$S/t/applications/x.desktop" "$S/x.snap"
H1=$(h)

# (a) same-size edit, mtime restored to the same second
printf 'Exec=term-z --flag\n' > "$S/t/applications/x.desktop"
touch -r "$S/x.snap" "$S/t/applications/x.desktop"
H2=$(h)
printf 'a same-size edit, mtime second restored : %s\n' "$([ "$H1" = "$H2" ] && echo IDENTICAL || echo differ)"

# (b) size change, same mtime second
printf 'Exec=term-zz --flag\n' > "$S/t/applications/x.desktop"
touch -r "$S/x.snap" "$S/t/applications/x.desktop"
H3=$(h)
printf 'a size+1, mtime second restored         : %s\n' "$([ "$H1" != "$H3" ] && echo CHANGED || echo identical)"

# (c) same minute, different second (recent file: ls prints Mon dd HH:MM)
printf 'Exec=term-a --flag\n' > "$S/t/applications/x.desktop"
touch -d '2026-10-20 10:00:05' "$S/t/applications/x.desktop"; H4=$(h)
printf 'Exec=term-q --flag\n' > "$S/t/applications/x.desktop"
touch -d '2026-10-20 10:00:55' "$S/t/applications/x.desktop"; H5=$(h)
printf 'c same minute, other second, same size   : %s   (ls shows: %s)\n' \
	"$([ "$H4" = "$H5" ] && echo IDENTICAL || echo differ)" \
	"$(LANG=C ls -l "$S/t/applications/x.desktop" | cut -d' ' -f6-)"

# (d) both mtimes older than six months, same day/year (ls prints Mon dd  YYYY)
touch -d '2024-03-01 08:00:05' "$S/t/applications/x.desktop"; H6=$(h)
printf 'Exec=term-r --flag\n' > "$S/t/applications/x.desktop"
touch -d '2024-03-01 20:00:05' "$S/t/applications/x.desktop"; H7=$(h)
printf 'd old file, same day/year, same size     : %s   (ls shows: %s)\n' \
	"$([ "$H6" = "$H7" ] && echo IDENTICAL || echo differ)" \
	"$(LANG=C ls -l "$S/t/applications/x.desktop" | cut -d' ' -f6-)"

# (e) month change on an old file is caught
touch -d '2024-11-01 08:00:05' "$S/t/applications/x.desktop"; H8=$(h)
printf 'e old file, month changed                : %s\n' "$([ "$H7" != "$H8" ] && echo CHANGED || echo identical)"

printf '\nH1=%s\nH2=%s\nH3=%s\nH4=%s\nH5=%s\nH6=%s\nH7=%s\nH8=%s\n' "$H1" "$H2" "$H3" "$H4" "$H5" "$H6" "$H7" "$H8"
