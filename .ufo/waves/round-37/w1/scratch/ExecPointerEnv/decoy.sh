#!/usr/bin/env bash
# Does an ambient GIT_DIR redirect the --selftest fixture writes (git init/add/commit) of
# check-index.py / check-index-rows.py into the repository GIT_DIR names? The target is a
# throwaway decoy repo under /dev/shm, never the fleet or the lane.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W=/dev/shm/mado37-ExecPointerEnv/decoy
rm -rf "$W"; mkdir -p "$W/tmp"
export TMPDIR=$W/tmp
cd "$LANE" || exit 2
for tool in check-index check-index-rows; do
  D=$W/$tool
  git init -q "$D"
  git -C "$D" -c user.name=decoy -c user.email=decoy@sandbox commit -q --allow-empty -m decoy-base
  echo "=== $tool --selftest plain"
  python3 -I quality/$tool.py --selftest >"$W/$tool.plain.out" 2>&1; echo "rc=$? last: $(tail -1 "$W/$tool.plain.out")"
  echo "=== $tool --selftest GIT_DIR=<decoy>/.git"
  GIT_DIR=$D/.git python3 -I quality/$tool.py --selftest >"$W/$tool.gitdir.out" 2>&1; echo "rc=$? last: $(tail -1 "$W/$tool.gitdir.out")"
  echo "  decoy commits after: $(git -C "$D" rev-list --count HEAD) (was 1); tip subject: $(git -C "$D" log -1 --format=%s)"
  echo "  decoy index entries after: $(git -C "$D" ls-files | wc -l) (was 0)"
  grep -E 'FAIL|fail' "$W/$tool.gitdir.out" | head -3 | sed 's/^/  /'
done
