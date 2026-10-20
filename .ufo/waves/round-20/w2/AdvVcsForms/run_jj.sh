#!/usr/bin/env bash
# run_jj.sh NAME -- CMD... : fresh jj repo, dirty wc, snapshot, run CMD, report.
set -u
export HOME=/tmp/mado-r20w2-vcs/jj-home
export XDG_CONFIG_HOME=/tmp/mado-r20w2-vcs/jj-home/.config
export PAGER=cat
name="$1"; shift
[ "$1" = "--" ] && shift
base=/tmp/mado-r20w2-vcs/jj-cases/$name
rm -rf "$base"; mkdir -p "$base"
snap() {
  (cd "$1" && find .jj -type f -exec sha256sum {} + 2>/dev/null | sort)
}
repo="$base/work"; mkdir -p "$repo"
(cd "$repo" && jj git init --colocate >/dev/null 2>&1 || jj init --git >/dev/null 2>&1)
echo seed > "$repo/seed.txt"
(cd "$repo" && jj describe -qm seed 2>/dev/null; jj new -qm top 2>/dev/null)
bare="$base/remote.git"; git init -q --bare "$bare"
(cd "$repo" && jj git remote add origin "file://$bare" 2>/dev/null)
(cd "$repo" && jj bookmark create main -r @- 2>/dev/null)
# pre-command observations must not snapshot the working copy
ops_before=$(cd "$repo" && jj op log --no-graph -T 'id ++ "\n"' 2>/dev/null | sha256sum)
wc_before=$(cd "$repo" && jj log -r @ --no-graph -T 'commit_id' 2>/dev/null)
# dirty the working copy so a snapshotting command creates an op
echo dirty >> "$repo/seed.txt"
before_repo=$(snap "$repo"; (cd "$bare" && find . -type f -exec sha256sum {} + 2>/dev/null | sort))
out=$(cd "$repo" && "$@" 2>&1); rc=$?
after_repo=$(snap "$repo"; (cd "$bare" && find . -type f -exec sha256sum {} + 2>/dev/null | sort))
ops_after=$(cd "$repo" && jj op log --no-graph -T 'id ++ "\n"' 2>/dev/null | sha256sum)
desc_after=$(cd "$repo" && jj log -r @ --no-graph -T 'description' 2>/dev/null)
wc_after=$(cd "$repo" && jj log -r @ --no-graph -T 'commit_id' 2>/dev/null)
mut=no
[ "$before_repo" != "$after_repo" ] && mut=yes
echo "$before_repo" | sort > "$base/fl_before.txt"; echo "$after_repo" | sort > "$base/fl_after.txt"
printf '## %s | rc=%s mut=%s ops_changed=%s\n' "$name" "$rc" "$mut" "$([ "$ops_before" != "$ops_after" ] && echo yes || echo no)"
printf '   desc_after=%s wc %s->%s\n' "$desc_after" "${wc_before:0:8}" "${wc_after:0:8}"
printf '   out: %s\n' "$(echo "$out" | head -4 | tr '\n' '~')"
