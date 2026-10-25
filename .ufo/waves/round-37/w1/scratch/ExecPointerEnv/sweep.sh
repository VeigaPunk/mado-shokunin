#!/usr/bin/env bash
# ExecPointerEnv sweep: does an ambient GIT_DIR (or another GIT_* variable) change the
# output of each git-calling gate under LANE/quality/*.py, LANE/tools/*.py, mado-verify.sh?
# Read-only: GIT_OPTIONAL_LOCKS=0 on every run, scratch only under /dev/shm.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
FLEET_GIT=/home/vgpnk/Projects/shokunin/.git
W=/dev/shm/mado37-ExecPointerEnv/sweep
rm -rf "$W"; mkdir -p "$W/tmp" "$W/selftest"
cd "$LANE" || exit 2
export GIT_OPTIONAL_LOCKS=0 TMPDIR=$W/tmp

# $1 tag, $2 env assignment ("" = plain), rest = command
run() {
  local tag=$1 envset=$2; shift 2
  local out="$W/$tag.out"
  if [ -n "$envset" ]; then env "$envset" "$@" >"$out" 2>&1; else "$@" >"$out" 2>&1; fi
  local rc=$?
  printf '%s rc=%s sha=%s lines=%s\n' "$tag" "$rc" "$(sha256sum <"$out" | cut -c1-16)" "$(wc -l <"$out")"
}
verdict() { grep -E "$2" "$W/$1.out" | head -${3:-3} | sed "s/^/  [$1] /"; }
same() { if cmp -s "$W/$1.out" "$W/$2.out"; then echo "  => $1 vs $2: IDENTICAL"; else echo "  => $1 vs $2: DIFFERENT"; fi; }

echo "date=$(date -u +%FT%TZ) lane_head=$(git rev-parse HEAD) git=$(git --version)"
echo "--- index sha256 before"; sha256sum .git/index "$FLEET_GIT/index"

echo; echo "### quality/check-axis-scores.py --repo . --rev master"
run axis.plain "" python3 -I quality/check-axis-scores.py --repo . --rev master
run axis.gitdir "GIT_DIR=$FLEET_GIT" python3 -I quality/check-axis-scores.py --repo . --rev master
verdict axis.plain 'MADO_AXIS' 1; verdict axis.gitdir 'MADO_AXIS|error|Error' 2; same axis.plain axis.gitdir

echo; echo "### quality/check-index.py --rev master --repo ."
run index.plain "" python3 -I quality/check-index.py --rev master --repo .
run index.gitdir "GIT_DIR=$FLEET_GIT" python3 -I quality/check-index.py --rev master --repo .
verdict index.plain 'indexed=|ERROR|error' 2; verdict index.gitdir 'indexed=|ERROR|error' 2; same index.plain index.gitdir

echo; echo "### quality/check-index-rows.py --rev master --repo ."
run rows.plain "" python3 -I quality/check-index-rows.py --rev master --repo .
run rows.gitdir "GIT_DIR=$FLEET_GIT" python3 -I quality/check-index-rows.py --rev master --repo .
verdict rows.plain '.' 2; verdict rows.gitdir '.' 2; same rows.plain rows.gitdir

echo; echo "### quality/check-control-receipts.py (round-27 committed invocation)"
CCR=(python3 -I quality/check-control-receipts.py --round 27 --data-registry .ufo/waves/round-27/w2/reports/swarm-registry.json --tip 2fdca5ca --receipt-glob 'v2/*.txt' --seeds 2 --shapes DoNothing,Junk,Echo,LabelKeyed,StaticBase,NaiveGrep,RootOnly,NoMerge,NoVariables,FlatScan)
run ccr.plain "" "${CCR[@]}"
run ccr.gitdir "GIT_DIR=$FLEET_GIT" "${CCR[@]}"
run ccr.commondir "GIT_COMMON_DIR=$FLEET_GIT" "${CCR[@]}"
run ccr.objdir "GIT_OBJECT_DIRECTORY=$FLEET_GIT/objects" "${CCR[@]}"
verdict ccr.plain '.' 2; verdict ccr.gitdir '.' 2; verdict ccr.commondir '.' 2; verdict ccr.objdir '.' 2
same ccr.plain ccr.gitdir; same ccr.plain ccr.commondir; same ccr.plain ccr.objdir

echo; echo "### quality/check-counter-discrimination.py --profile r36 --no-receipts"
CCD=(python3 -I quality/check-counter-discrimination.py --profile r36 --manifest .ufo/waves/round-36/controls/manifest.json --repo . --no-receipts)
run ccd.plain "" "${CCD[@]}"
run ccd.gitdir "GIT_DIR=$FLEET_GIT" "${CCD[@]}"
run ccd.commondir "GIT_COMMON_DIR=$FLEET_GIT" "${CCD[@]}"
verdict ccd.plain 'DISCRIM|discriminat|total|verdict' 2; verdict ccd.gitdir 'DISCRIM|discriminat|total|verdict' 2
same ccd.plain ccd.gitdir; same ccd.plain ccd.commondir

echo; echo "### quality/counter-selftest.py (round-26 counters, offline)"
CST=(python3 -I quality/counter-selftest.py --c1 .ufo/waves/round-26/c1/count-v2.py --c2 .ufo/waves/round-26/c2/count.py --rev 05319e0f --scratch "$W/selftest")
run cst.plain "" "${CST[@]}"
run cst.gitdir "GIT_DIR=$FLEET_GIT" "${CST[@]}"
verdict cst.plain 'SELFTEST' 1; verdict cst.gitdir 'SELFTEST' 1; same cst.plain cst.gitdir

echo; echo "### tools/mado-verify.sh live omarchy git rows (real \$HOME root, sandbox PATH)"
SB=$W/bin; mkdir -p "$SB"
for f in /usr/bin/*; do
  b=${f##*/}
  case "$b" in
    hypr*|Hyprland|omarchy*|busctl|systemctl|loginctl|walker|waybar|socat|nc|ncat|netcat|dbus-*|gdbus|notify-send|makoctl|swayosd*|uwsm*) continue ;;
  esac
  ln -s "$f" "$SB/$b"
done
echo "sandbox PATH entries=$(ls "$SB" | wc -l); hyprctl=$(PATH=$SB command -v hyprctl || echo absent) omarchy=$(PATH=$SB command -v omarchy || echo absent)"
MV=(env -u HYPRLAND_INSTANCE_SIGNATURE PATH="$SB" MADO_VERIFY_LIVE=yes bash tools/mado-verify.sh --live)
run verify.plain "" "${MV[@]}"
run verify.gitdir "GIT_DIR=$FLEET_GIT" "${MV[@]}"
run verify.worktree "GIT_WORK_TREE=/dev/shm" "${MV[@]}"
for t in verify.plain verify.gitdir verify.worktree; do verdict "$t" 'omarchy\.(git\.(tag|head)|skill\.vs_head)' 3; done
same verify.plain verify.gitdir; same verify.plain verify.worktree
echo "  non-omarchy-git line diff plain vs gitdir: $(diff <(grep -vE 'omarchy\.(git|skill\.vs_head)' "$W/verify.plain.out") <(grep -vE 'omarchy\.(git|skill\.vs_head)' "$W/verify.gitdir.out") | grep -c '^[<>]')"

echo; echo "--- index sha256 after"; sha256sum .git/index "$FLEET_GIT/index"
