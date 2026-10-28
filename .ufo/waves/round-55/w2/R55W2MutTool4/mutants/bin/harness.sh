#!/bin/bash
# usage: harness.sh <ID> <path-to-tool-copy>   -- runs 26 fixtures + selftest in a private dir
ID=$1; T=$2; S=/fast/scratch/hyaku/mado-r55/R55W2MutTool4
R=$S/run/$ID
rm -rf "$R"; mkdir -p "$R/.ufo/waves/round-55" && cp -r "$S/.ufo/waves/round-55/fixtures" "$S/.ufo/waves/round-55/fetch" "$R/.ufo/waves/round-55/" && cp "$T" "$R/tool.py" || exit 9
cd "$R" || exit 9
kill_list=(); surv_list=(); n=0
for d in .ufo/waves/round-55/fixtures/c2/F* .ufo/waves/round-55/fixtures/c2-holdout/H*; do
  name=$(basename "$d"); n=$((n+1))
  mapfile -t args < <(python3 -I -c 'import json,sys; [print(a) for a in json.load(open(sys.argv[1]))]' "$d/args.json")
  timeout 20 python3 -I tool.py "${args[@]}" > "$R/out.$name" 2> "$R/err.$name"; rc=$?
  if cmp -s "$R/out.$name" "$d/expected.out" && [ "$rc" = "$(cat "$d/expected.rc")" ]; then surv_list+=("$name"); else kill_list+=("$name"); fi
done
timeout 60 python3 -I tool.py --selftest > "$R/st.out" 2> "$R/st.err"; strc=$?
st=$(cat "$R/st.out")
if [ $strc -eq 0 ] && [[ "$st" =~ ^MADO_KBDOPT_SELFTEST:\ ([0-9]+)/([0-9]+)\ assertions\ passed$ ]] && [ "${BASH_REMATCH[1]}" = "${BASH_REMATCH[2]}" ]; then stk=survived; else stk=KILLED; fi
echo "$ID fixtures_total=$n killed=${#kill_list[@]} killed_ids=[${kill_list[*]}] passing_all=$([ ${#kill_list[@]} -eq 0 ] && echo YES || echo NO) selftest=$stk selftest_out=\"$st\" selftest_rc=$strc"
