#!/usr/bin/env bash
# ExecPointerEnv red/green transcript for check-evidence-pointers.py under ambient GIT_*.
# GIT_OPTIONAL_LOCKS=0 keeps `git status` from refreshing an index; the fixed copy strips it
# along with every other GIT_* variable.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$LANE/.ufo/waves/round-37/w1/scratch/ExecPointerEnv
R=a5aaa09ad38bfd90c13d76ccf371e36c45a2697e
FLEET_GIT=/home/vgpnk/Projects/shokunin/.git
cd "$LANE" || exit 2
export GIT_OPTIONAL_LOCKS=0

runset() {  # $1 label, $2 script
  local label=$1 script=$2
  echo "=== $label plain"
  echo "\$ python3 -I $script --rev $R"
  python3 -I "$script" --rev "$R" 2>&1; echo "rc=$?"
  echo "=== $label GIT_DIR=$FLEET_GIT"
  echo "\$ GIT_DIR=$FLEET_GIT python3 -I $script --rev $R"
  GIT_DIR=$FLEET_GIT python3 -I "$script" --rev "$R" 2>&1; echo "rc=$?"
  echo "=== $label GIT_WORK_TREE=/dev/shm"
  echo "\$ GIT_WORK_TREE=/dev/shm python3 -I $script --rev $R"
  GIT_WORK_TREE=/dev/shm python3 -I "$script" --rev "$R" 2>&1; echo "rc=$?"
}

echo "date=$(date -u +%FT%TZ) lane_head=$(git rev-parse HEAD) git=$(git --version)"
echo "ambient GIT_* names: $(env | grep '^GIT_' | cut -d= -f1 | sort | tr '\n' ' ')"
sha256sum quality/check-evidence-pointers.py "$S/check-evidence-pointers.py"
echo "--- index sha256 before"
sha256sum .git/index "$FLEET_GIT/index"
echo "--- delta (original -> fixed)"
diff -u quality/check-evidence-pointers.py "$S/check-evidence-pointers.py"
echo
runset RED quality/check-evidence-pointers.py
echo
runset GREEN "$S/check-evidence-pointers.py"
echo
echo "=== GREEN extra: GIT_DIR and GIT_WORK_TREE together"
GIT_DIR=$FLEET_GIT GIT_WORK_TREE=/dev/shm python3 -I "$S/check-evidence-pointers.py" --rev "$R" 2>&1 | head -1; echo "rc=${PIPESTATUS[0]}"
echo "=== able-to-fail: 4243d03 (round-35 spot-check, before any round-36 section), plain and GIT_DIR"
OLD=$(git rev-parse 4243d03)
for s in quality/check-evidence-pointers.py "$S/check-evidence-pointers.py"; do
  python3 -I "$s" --rev "$OLD" 2>&1 | head -1; echo "rc=${PIPESTATUS[0]} env=plain script=$s"
  GIT_DIR=$FLEET_GIT python3 -I "$s" --rev "$OLD" 2>&1 | head -1; echo "rc=${PIPESTATUS[0]} env=GIT_DIR script=$s"
done
echo "--- index sha256 after"
sha256sum .git/index "$FLEET_GIT/index"
stat -c '%n mtime=%Y' .git/index "$FLEET_GIT/index"
