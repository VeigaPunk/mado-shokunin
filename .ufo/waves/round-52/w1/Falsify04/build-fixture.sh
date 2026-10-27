#!/usr/bin/env bash
# Build the tiny green fixture repo used by the Falsify04 --work==--repo attack.
# Usage: build-fixture.sh <dest-dir>
set -euo pipefail
DEST="${1:?dest dir}"
rm -rf "$DEST"
mkdir -p "$DEST/tools" "$DEST/quality"
printf 'x.py reads config bytes and prints one stable status line for inventory\n' > "$DEST/tools/x.py"
printf 'x.py\n' > "$DEST/quality/notes.md"
cat > "$DEST/quality/tool-ledger.md" <<'EOF'
# fixture ledger
| Path | Description | Accountability pointer |
| --- | --- | --- |
| `tools/x.py` | x.py reads config bytes prints stable status line inventory check | `quality/notes.md` |
EOF
git -C "$DEST" init -q
git -C "$DEST" config user.name falsify04
git -C "$DEST" config user.email falsify04@example.invalid
git -C "$DEST" config commit.gpgsign false
git -C "$DEST" add -A
git -C "$DEST" commit -q -m 'green fixture'
git -C "$DEST" rev-parse HEAD
