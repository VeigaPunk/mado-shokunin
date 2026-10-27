#!/bin/sh
# mkrev.sh TAG FILE : commit FILE as tools/mado-terminal.py on top of the freeze rev, tag tool-TAG
set -eu
S=/fast/scratch/hyaku/mado-r48/MutC1Counter
TAG=$1; FILE=$2
blob=$(git -C "$S/tree/lane" hash-object -w --path=tools/mado-terminal.py "$FILE")
git -C "$S/tree/lane" update-index --add --cacheinfo 100755,"$blob",tools/mado-terminal.py
tree=$(git -C "$S/tree/lane" write-tree)
commit=$(GIT_AUTHOR_NAME=mut GIT_AUTHOR_EMAIL=mut@seat GIT_COMMITTER_NAME=mut GIT_COMMITTER_EMAIL=mut@seat \
  git -C "$S/tree/lane" commit-tree "$tree" -p 3e6c848a -m "tool $TAG")
git -C "$S/tree/lane" tag -f "tool-$TAG" "$commit" >/dev/null
printf '%s %s %s\n' "$TAG" "$commit" "$(sha256sum "$FILE" | cut -d' ' -f1)"
