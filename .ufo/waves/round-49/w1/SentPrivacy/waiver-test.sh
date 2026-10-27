#!/usr/bin/env bash
# waiver-test.sh - a round-49 seat fixture that uses the real account name cannot
# be waived; the same shape under a reserved user can.  Values are derived at
# runtime or reserved; the script prints gate reason lines only.
set -eu
ulimit -f 65536
S=/fast/scratch/hyaku/mado-r49/SentPrivacy/waiver
rm -rf -- "$S"; mkdir -p "$S"
GATE=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py
REAL=$(id -un)

build() {          # $1 = user, $2 = repo dir
  local user="$1" d="$2" f rel
  mkdir -p "$d/.ufo/waves/round-49/w1/Seat/fixtures" "$d/quality"
  rel=.ufo/waves/round-49/w1/Seat/fixtures/listing.txt
  for i in $(seq 1 12); do printf '/home/%s/dir%02d/file.txt\n' "$user" "$i"; done > "$d/$rel"
  sha=$(python3 -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$d/$rel")
  printf 'SYNTHETIC-MATERIAL v1 kind=fixture rules=R4_HOME_LISTING sha256=%s\n' "$sha" > "$d/$rel.synthetic"
  printf '%s %s R4_HOME_LISTING kind=fixture\n' "$rel" "$sha" > "$d/quality/session-material-waivers.txt"
  git -C "$d" init -q
  GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@example.invalid \
  GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@example.invalid \
    git -C "$d" add -A
  GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@example.invalid \
  GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@example.invalid \
    git -C "$d" commit -qm fixture
  test "$(git -C "$d" rev-parse --show-toplevel)" = "$d"
}

D1=$(mktemp -d -p "$S" reserved.XXXXXX)
D2=$(mktemp -d -p "$S" realacct.XXXXXX)
build example "$D1"
build "$REAL"  "$D2"

for d in "$D1" "$D2"; do
  rev=$(git -C "$d" rev-parse HEAD)
  case "$d" in *reserved.*) tag=reserved-user ;; *) tag=real-account ;; esac
  echo "== $tag"
  python3 "$GATE" --repo "$d" --rev "$rev" --waivers quality/session-material-waivers.txt || echo "rc=$?"
done
rm -rf -- "$S"
