#!/bin/bash
# Reproduce ExecSeparability's round-47 w2 separability runs (C1/C2, both ways, at the frozen rev).
# Everything lands under $S (scratch) and is deleted at the end; only the seat dir keeps receipts.
# Bounded: no unbounded writes, every resolver-free path (no terminal launched anywhere).
set -eu

LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=60edb66e2f1cb90acc6e9442fc93ded0ca42d750
FREEZE=d7527d608ad2b2e3cc398fdde34db7947b254a1a
C1="$LANE/quality/counters/c1-r47-terminal.py"
C2="$LANE/quality/counters/c2-r47-terminal-entry.py"
REF="$LANE/.ufo/waves/round-47/l1-draft/mado-terminal.py"
CTL="$LANE/.ufo/waves/round-47/ctl/c2/build-control.py"
OUT="$LANE/.ufo/waves/round-47/w2/ExecSeparability"
S=${S:-/fast/scratch/hyaku/mado-r47/ExecSeparability-repro}
TARBALL_SHA=82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe

mkdir -p "$S"; cd "$S"
trap 'cd /; rm -rf -- "$S"' EXIT

commit() { git -C "$1" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m "$2"; }
clone_at() {  # $1 dir, $2 rev
  rm -rf "$1"; git clone -q --shared --no-checkout "$LANE" "$1"
  test "$(git -C "$1" rev-parse --show-toplevel)" = "$1"
  git -C "$1" checkout -q --detach "$2"
}

# --- pinned bytes (tag v0.14.3) -------------------------------------------------------------
mkdir -p pins
curl -fsSL --max-time 120 -o xte.tar.gz \
  https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3
test "$(sha256sum xte.tar.gz | cut -d' ' -f1)" = "$TARBALL_SHA"
tar xzf xte.tar.gz -C pins
P="$S/pins/xdg-terminal-exec-0.14.3"
test "$(sha256sum "$P/xdg-terminal-exec" | cut -d' ' -f1)" = 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac

mkdir -p "$S/w"

# --- tree 1: tool-only at the freeze --------------------------------------------------------
clone_at "$S/clone-tool" "$FREEZE"
cp "$REF" "$S/clone-tool/tools/mado-terminal.py"
git -C "$S/clone-tool" add tools/mado-terminal.py && commit "$S/clone-tool" cand
python3 -I "$C1" --repo "$S/clone-tool" --rev HEAD --work "$S/w" | tail -1     # TARGET_MET
python3 -I "$C2" --repo "$S/clone-tool" --rev HEAD | tail -1                   # TARGET_MISSED clause=a

# --- tree 2: the C2 POS control, as built (BASE) and transplanted to the freeze -------------
C2R47_WORK="$S" python3 -I "$CTL" | tail -3
python3 -I "$C2" --repo "$S/ctl" --rev HEAD | tail -1                          # TARGET_MET
git -C "$S/ctl" diff "$BASE" HEAD > "$S/entry-only.patch"
clone_at "$S/clone-entry" "$FREEZE"
git -C "$S/clone-entry" apply --index "$S/entry-only.patch"
commit "$S/clone-entry" entry-only-at-freeze
python3 -I "$C2" --repo "$S/clone-entry" --rev HEAD | tail -2                  # F1: MISSED, clause=e 0/7
E=corpus/knowledge/xdg-terminal-selection-r47.md
clone_at "$S/clone-entry-named" HEAD
sed -i 's/xdgte-xdg-terminal-exec:/xdg-terminal-exec:/g' "$S/clone-entry-named/$E"
commit "$S/clone-entry-named" freeze-pin-name
python3 -I "$C1" --repo "$S/clone-entry-named" --rev HEAD --work "$S/w" | tail -1   # TARGET_MISSED clause=a
python3 -I "$C2" --repo "$S/clone-entry-named" --rev HEAD | tail -1                # TARGET_MET

# --- both claims at the freeze --------------------------------------------------------------
clone_at "$S/clone-both" "$(git -C "$S/clone-entry-named" rev-parse HEAD)"
cp "$REF" "$S/clone-both/tools/mado-terminal.py"
git -C "$S/clone-both" add tools/mado-terminal.py && commit "$S/clone-both" both
python3 -I "$C1" --repo "$S/clone-both" --rev HEAD --work "$S/w" | tail -1     # TARGET_MET
python3 -I "$C2" --repo "$S/clone-both" --rev HEAD | tail -1                   # TARGET_MET

# --- F2: eighth chain step citing the phantom line 1500 ------------------------------------
clone_at "$S/clone-vac1500" "$(git -C "$S/clone-entry-named" rev-parse HEAD)"
python3 -I - "$S/clone-vac1500/$E" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read().split("\n")
i = max(k for k, l in enumerate(t) if l.startswith("7. "))
t.insert(i + 1, "8. Vacuous step: a locator past the last line of the script (xdg-terminal-exec:1500).")
open(p, "w", encoding="utf-8").write("\n".join(t))
PY
commit "$S/clone-vac1500" vac1500
python3 -I "$C2" --repo "$S/clone-vac1500" --rev HEAD | tail -2                # admitted=1/1 (e:1)
