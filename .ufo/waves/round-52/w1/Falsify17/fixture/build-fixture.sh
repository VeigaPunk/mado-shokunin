#!/bin/sh
# Rebuild the Falsify17 seat-local fixture repo. Nothing here touches the lane repo.
# Usage: build-fixture.sh <scratch dir>   (defaults to /fast/scratch/hyaku/mado-r52/Falsify17/fixture)
set -eu
SELF=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUT=${1:-/fast/scratch/hyaku/mado-r52/Falsify17/fixture}
rm -rf "$OUT"
mkdir -p "$OUT"
cp -R "$SELF/tools" "$SELF/quality" "$SELF/docs" "$OUT/"
cd "$OUT"
git init -q
git -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false add -A
git -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -q -m 'fixture: no-work self-pointer ledger, unique rows'
top=$(git rev-parse --show-toplevel)
test "$(cd "$top" && pwd -P)" = "$(cd "$OUT" && pwd -P)" || { echo "toplevel mismatch: $top" >&2; exit 1; }
echo "fixture_top=$top"
echo "fixture_head=$(git rev-parse HEAD)"
git ls-tree -r --name-only HEAD
