#!/bin/bash
# The pin's read_cache line loop, verbatim structure (x:217-262), over $1; writes: <state>\0<f1..f10 each NUL><usep raw>
set -u
XTE__RSEP=$'\x1e'
XTE__LF=$'
'
xte__line_num=0
xte__line_limit=50
xte__cached_exec_usep=
xte__finished=0
xte__state=eof
f1=; f2=; f3=; f4=; f5=; f6=; f7=; f8=; f9=; f10=
while IFS= read -r xte__line; do
	xte__line_num=$((xte__line_num + 1))
	case "${xte__line_num}" in
	1) f1=$xte__line ;;
	2) f2=$xte__line ;;
	3) f3=$xte__line ;;
	4) f4=$xte__line ;;
	5) f5=$xte__line ;;
	6) f6=$xte__line ;;
	7) f7=$xte__line ;;
	8) f8=$xte__line ;;
	9) f9=$xte__line ;;
	10) f10=$xte__line ;;
	"$xte__line_limit")
		xte__state=limit
		break
		;;
	*)
		xte__cached_exec_usep=${xte__cached_exec_usep}${xte__cached_exec_usep:+$XTE__LF}${xte__line}
		case "${xte__line}" in
		*"${XTE__RSEP}END_OF_EXEC_USEP")
			xte__cached_exec_usep=${xte__cached_exec_usep%"${XTE__RSEP}END_OF_EXEC_USEP"}
			xte__finished=1
			xte__state=finished
			break
			;;
		esac
		;;
	esac
done < "$1"
{
	printf '%s\0' "$xte__state" "$f1" "$f2" "$f3" "$f4" "$f5" "$f6" "$f7" "$f8" "$f9" "$f10"
	printf '%s' "$xte__cached_exec_usep"
} > "$2"
