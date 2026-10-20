#!/usr/bin/env bash
# =============================================================================
# landed-check.sh — read-only landedness classifier for one lane checkout
#
# Origin: round-19 lane Mado / jj audit F16 — no lane tool could tell a pushed
# commit from an unpushed one, and `git status` clean does not mean landed
# (audit F17). This tool answers one question per hash: is it on origin/master?
#
# Usage:
#   landed-check.sh LANE_DIR HASH...
#
#   LANE_DIR   a git checkout (a jj-colocated checkout works; only git reads)
#   HASH...    full or abbreviated hex object names
#
# Output (stdout, one line per HASH, input order):
#   LANDED <hash>      object present locally and ancestor of the remote tip
#   LOCAL_ONLY <hash> (reason)
#                      present locally, not landed. Reason is one of:
#                        ancestor of refs/heads/master but not of origin/master
#                        remote tip object absent locally (ancestry untestable)
#                        ancestor of neither refs/heads/master nor origin/master
#                        refs/heads/master absent locally
#                        object present but not a commit
#                        ancestry test against origin/master errored rc=N
#   MISSING <hash>     object absent locally
#
# The remote tip is resolved live, never from a stale remote-tracking ref:
#   git -C LANE ls-remote origin refs/heads/master
# That is a network READ. This tool never fetches, never writes git state
# (no index read, no ref update, no worktree touch) and never invokes jj.
#
# Exit map: 0 all HASHes LANDED · 1 any LOCAL_ONLY or MISSING
#           2 usage error, or could-not-evaluate (not a repo, no origin, no
#             refs/heads/master there, ls-remote failed, ancestry test error)
# =============================================================================

set -u

PROG=${0##*/}

usage() {
  printf 'usage: %s LANE_DIR HASH...\n' "$PROG" >&2
  exit 2
}

die2() {
  printf '%s: %s\n' "$PROG" "$*" >&2
  exit 2
}

[ "$#" -ge 2 ] || usage
LANE=$1
shift
[ -n "$LANE" ] || usage
[ -d "$LANE" ] || die2 "not a directory: $LANE"

for h in "$@"; do
  case $h in
    *[!0-9a-fA-F]*) die2 "not a hex object name: $h" ;;
  esac
  if [ "${#h}" -lt 4 ] || [ "${#h}" -gt 64 ]; then
    die2 "object name length out of range (4..64 hex): $h"
  fi
done

command -v git >/dev/null 2>&1 || die2 "git not found in PATH"

# Read-only posture: no interactive credential prompts, no implicit lazy fetch
# in partial clones, no optional index locks. `ls-remote` is time-bounded so a
# dead remote cannot hang a wave.
GIT_TERMINAL_PROMPT=0
GIT_NO_LAZY_FETCH=1
GIT_OPTIONAL_LOCKS=0
export GIT_TERMINAL_PROMPT GIT_NO_LAZY_FETCH GIT_OPTIONAL_LOCKS

tmo() {
  if command -v timeout >/dev/null 2>&1; then
    timeout 60 "$@"
  else
    "$@"
  fi
}

git -C "$LANE" rev-parse --git-dir >/dev/null 2>&1 \
  || die2 "not a git checkout: $LANE"

lsr=$(tmo git -C "$LANE" ls-remote origin refs/heads/master 2>/dev/null) \
  || die2 "git ls-remote origin refs/heads/master failed in $LANE"

remote_tip=$(printf '%s\n' "$lsr" | awk '$2 == "refs/heads/master" { print $1; exit }')
[ -n "$remote_tip" ] || die2 "origin has no refs/heads/master: $LANE"
case $remote_tip in
  *[!0-9a-f]*) die2 "unexpected ls-remote object id: $remote_tip" ;;
esac
if [ "${#remote_tip}" -ne 40 ] && [ "${#remote_tip}" -ne 64 ]; then
  die2 "unexpected ls-remote object id length: $remote_tip"
fi

# Resolve the remote tip to a local commit object. A lane that has not fetched
# since the remote moved cannot prove ancestry; that is reported per hash, not
# papered over with a fetch.
remote_known=0
resolved_remote=
if resolved_remote=$(git -C "$LANE" rev-parse --verify --quiet "${remote_tip}^{commit}" 2>/dev/null) \
   && [ -n "$resolved_remote" ]; then
  remote_known=1
fi

local_master=
local_master=$(git -C "$LANE" rev-parse --verify --quiet 'refs/heads/master^{commit}' 2>/dev/null) \
  || local_master=

shallow=$(git -C "$LANE" rev-parse --git-path shallow 2>/dev/null) || shallow=
if [ -n "$shallow" ] && [ -f "$shallow" ]; then
  printf '%s: warning: shallow clone — ancestry is bounded by the shallow boundary (false LOCAL_ONLY possible)\n' "$PROG" >&2
fi

if [ "$remote_known" = 1 ]; then
  printf '%s: origin/master = %s (object present locally)\n' "$PROG" "$remote_tip" >&2
else
  printf '%s: origin/master = %s (object ABSENT locally; no fetch performed)\n' "$PROG" "$remote_tip" >&2
fi

landed_all=1
unevaluable=0

for h in "$@"; do
  full=
  full=$(git -C "$LANE" rev-parse --verify --quiet "${h}^{commit}" 2>/dev/null) || full=

  if [ -z "$full" ]; then
    landed_all=0
    if git -C "$LANE" cat-file -e "$h" 2>/dev/null; then
      printf 'LOCAL_ONLY %s (object present but not a commit)\n' "$h"
    else
      printf 'MISSING %s\n' "$h"
    fi
    continue
  fi

  if [ "$remote_known" = 1 ]; then
    git -C "$LANE" merge-base --is-ancestor "$full" "$resolved_remote" 2>/dev/null
    mbrc=$?
    case $mbrc in
      0)
        printf 'LANDED %s\n' "$full"
        continue
        ;;
      1)
        ;;
      *)
        printf 'LOCAL_ONLY %s (ancestry test against origin/master %s errored rc=%s)\n' \
          "$full" "$remote_tip" "$mbrc"
        landed_all=0
        unevaluable=1
        continue
        ;;
    esac

    landed_all=0
    if [ -n "$local_master" ] \
       && git -C "$LANE" merge-base --is-ancestor "$full" "$local_master" 2>/dev/null; then
      printf 'LOCAL_ONLY %s (ancestor of refs/heads/master, not of origin/master %s)\n' \
        "$full" "$remote_tip"
    elif [ -n "$local_master" ]; then
      printf 'LOCAL_ONLY %s (ancestor of neither refs/heads/master nor origin/master %s)\n' \
        "$full" "$remote_tip"
    else
      printf 'LOCAL_ONLY %s (not an ancestor of origin/master %s; refs/heads/master absent locally)\n' \
        "$full" "$remote_tip"
    fi
  else
    landed_all=0
    if [ -n "$local_master" ] \
       && git -C "$LANE" merge-base --is-ancestor "$full" "$local_master" 2>/dev/null; then
      printf 'LOCAL_ONLY %s (ancestor of refs/heads/master; remote tip %s is absent locally, ancestry untestable without a fetch)\n' \
        "$full" "$remote_tip"
    else
      printf 'LOCAL_ONLY %s (remote tip %s is absent locally, ancestry untestable; not an ancestor of refs/heads/master either)\n' \
        "$full" "$remote_tip"
    fi
  fi
done

if [ "$unevaluable" = 1 ]; then
  exit 2
fi
[ "$landed_all" = 1 ] && exit 0
exit 1
