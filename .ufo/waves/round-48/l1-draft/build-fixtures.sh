#!/usr/bin/env bash
# L1: rebuild quality/counters/c1-r48-fixtures.json candidates: merge the two w1 seat sets, then add the L1 cases
# (measured from the pin), then pin the file's sha256 in the counter. Usage: build-fixtures.sh WORK
set -eu
cd "$(dirname "$0")"
python3 merge-fixtures.py c1-r48-fixtures.json
python3 -I add-fixtures.py "$1"
H=$(sha256sum c1-r48-fixtures.json | cut -d' ' -f1)
sed -i "s/^SHA256_WARM = .*/SHA256_WARM = \"$H\"/" c1-r48-terminal-cache.py
echo "SHA256_WARM=$H"
