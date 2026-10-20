#!/usr/bin/env bash
# run_git.sh NAME -- CMD...  : build a fresh repo, snapshot, run CMD, report.
# Usage: run_git.sh <name> <mode> -- <argv...>
#   mode: add | commit | push | free   (free: argv run verbatim in repo)
set -u
export HOME=/tmp/mado-r20w2-vcs/git-home
export GIT_CONFIG_NOSYSTEM=1
export XDG_CONFIG_HOME=/tmp/mado-r20w2-vcs/git-home/xdg
name="$1"; mode="$2"; shift 2
[ "$1" = "--" ] && shift
base=/tmp/mado-r20w2-vcs/git-cases/$name
rm -rf "$base"; mkdir -p "$base"
snap() {  # hash all of .git plus tracked content mtimes-independent
  (cd "$1" && find .git -type f -exec sha256sum {} + 2>/dev/null | sort | sha256sum | cut -d' ' -f1)
}
repo="$base/work"; mkdir -p "$repo"
git -C "$repo" init -q
echo seed > "$repo/seed.txt"; git -C "$repo" add seed.txt
git -C "$repo" commit -qm seed
echo changed > "$repo/seed.txt"          # tracked modification for add/commit -a
git -C "$repo" add seed.txt            # staged copy so plain `commit` can write
echo new > "$repo/new.txt"               # untracked
bare="$base/remote.git"
git init -q --bare "$bare"
git -C "$repo" remote add origin "file://$bare"
git -C "$repo" push -q -u origin main 2>/dev/null
# a local commit ahead of the remote so pushes can move the ref
git -C "$repo" commit -qam ahead
# fresh work for commit/add verbs: a staged tracked change + unstaged + untracked
echo staged > "$repo/seed.txt"; git -C "$repo" add seed.txt
echo unstaged > "$repo/seed.txt"
# pre-push canary hook proves hook ran even on dry-run
mkdir -p "$repo/.git/hooks"
printf '#!/bin/sh\ntouch %s\n' "$base/canary" > "$repo/.git/hooks/pre-push"
chmod +x "$repo/.git/hooks/pre-push"
before_repo=$(snap "$repo"); before_remote=$(snap "$bare")
before_head=$(git -C "$repo" rev-parse HEAD)
before_rhead=$(git -C "$bare" rev-parse HEAD)
before_refs=$(git -C "$bare" for-each-ref 2>/dev/null | sha256sum | cut -d' ' -f1)
before_idx=$(git -C "$repo" ls-files -s 2>/dev/null | sha256sum | cut -d' ' -f1)
out=$(cd "$repo" && "$@" 2>&1); rc=$?
after_head=$(git -C "$repo" rev-parse HEAD 2>/dev/null || echo lost)
after_rhead=$(git -C "$bare" rev-parse HEAD 2>/dev/null || echo lost)
after_refs=$(git -C "$bare" for-each-ref 2>/dev/null | sha256sum | cut -d' ' -f1)
after_idx=$(git -C "$repo" ls-files -s 2>/dev/null | sha256sum | cut -d' ' -f1)
after_repo=$(snap "$repo"); after_remote=$(snap "$bare")
canary=no; [ -e "$base/canary" ] && canary=yes
mut=no
# a real write moves HEAD, a remote ref, or the index — not just COMMIT_EDITMSG
[ "$before_head" != "$after_head" ] && mut=yes
[ "$before_refs" != "$after_refs" ] && mut=yes
[ "$before_idx" != "$after_idx" ] && mut=yes
filesmut=no
[ "$before_repo" != "$after_repo" ] && filesmut=yes
[ "$before_remote" != "$after_remote" ] && filesmut=yes
printf '## %s | rc=%s mut=%s filesmut=%s canary=%s\n' "$name" "$rc" "$mut" "$filesmut" "$canary"
printf '   head %s -> %s ; remote %s -> %s\n' \
  "${before_head:0:8}" "${after_head:0:8}" "${before_rhead:0:8}" "${after_rhead:0:8}"
printf '   out: %s\n' "$(echo "$out" | head -3 | tr '\n' '~')"
