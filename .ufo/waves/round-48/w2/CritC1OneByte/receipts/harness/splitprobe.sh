set -u
IFS=$'\x1f'
v=$1
set -- $v
printf 'n=%d' "$#"
for a in "$@"; do printf '|%s' "$a"; done
printf '\n'
