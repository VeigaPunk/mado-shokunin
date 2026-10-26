#!/bin/sh
# Re-derive every locator quoted in digest.md from the live files (no typed line numbers).
# run: sh verify-locators.sh <lane-root>   (default /home/vgpnk/Projects/shokunin/mado-shokunin)
set -eu
L=${1:-/home/vgpnk/Projects/shokunin/mado-shokunin}
D=$L/.ufo/waves/round-46/w1/ExecStofOracle/diff.py
T=$L/.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv
J=$L/.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json
fail=0
chk() { # chk <label> <expected-substring> <file> <line>
  got=$(sed -n "${4}p" "$3")
  case $got in
    *"$2"*) printf 'ok   %-22s %s:%s\n' "$1" "$(basename "$3")" "$4" ;;
    *) printf 'FAIL %-22s %s:%s got=%s\n' "$1" "$(basename "$3")" "$4" "$got"; fail=1 ;;
  esac
}
# locators computed by: grep -n 'rows.append\|with open(out_path\|fh.write("cat' "$D"
chk rows-append        'rows.append({'                    "$D" "$(grep -n 'rows.append({' "$D" | cut -d: -f1)"
chk write-outjson      'with open(out_path, "w"'            "$D" "$(grep -n 'with open(out_path, "w"' "$D" | cut -d: -f1)"
chk write-rows-tsv     'with open(out_path + ".rows.tsv"'   "$D" "$(grep -n 'with open(out_path + ".rows.tsv"' "$D" | cut -d: -f1)"
chk write-header       'cat\tcls\tref_line'                 "$D" "$(grep -n 'fh.write("cat' "$D" | cut -d: -f1)"
chk write-row          'r["cat"], r["cls"], r["ref_line"]' "$D" "$(grep -n 'r\["cat"\], r\["cls"\], r\["ref_line"\]' "$D" | cut -d: -f1)"
chk tsv-header         'cat	cls	ref_line	truth_line	ref_printed	truth_printed	text' "$T" 1
# out.json top-level key list, in file order
printf 'ok   out.json keys        %s\n' "$(python3 -I -c 'import json,sys;print(",".join(json.load(open(sys.argv[1]))))' "$J")"
exit $fail
