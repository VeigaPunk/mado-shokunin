#!/bin/bash
# Seat ExecDoNothingC1: build one scratch clone per control, commit the control at tools/mado-devices.py, score it
# with the frozen C1 counter, and keep the counter's stdout. Never touches the lane.
#
# This is the recipe for every row of controls.md; the receipts under receipts/ were produced by the same commands
# (the A/B/E/E2/C half ran once as an intermediate split script before this merge).
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
C=$LANE/.ufo/waves/round-46/w1/ExecDoNothingC1
S=/fast/scratch/hyaku/mado-r46/ExecDoNothingC1
BASE=b22ea56bff2faec39ce9ff75d2107eaf4612ecbe
CTR=$LANE/quality/counters/c1-r46-devices.py

score() {  # name rev nonce
    local n=$1 rev=$2 nonce=$3
    mkdir -p "$S/w/$n"
    python3 -I "$CTR" --repo "$S/$rev" --rev HEAD --work "$S/w/$n" --nonce "$nonce" > "$S/out-$n.txt" 2>"$S/err-$n.txt"
    echo "CTL $n exit=$? $(grep -h ': fixtures=' "$S/out-$n.txt")" >> "$S/results.txt"
}

clone() {  # dest
    rm -rf "$S/$1"
    git clone -q --shared --no-checkout "$LANE" "$S/$1" || return 1
    test "$(git -C "$S/$1" rev-parse --show-toplevel)" = "$S/$1" || { echo "BAD TOPLEVEL $1"; return 1; }
    git -C "$S/$1" checkout -q --detach "$BASE" || return 1
    mkdir -p "$S/$1/tools"
}

commit() {  # dest msg
    git -C "$S/$1" add -A
    git -C "$S/$1" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m "$2"
}

mkdir -p "$S/w" "$S/tools-a"
: > "$S/results.txt"

# REF-COPY: the frozen reference verbatim at tools/mado-devices.py
clone ref && cp "$LANE/.ufo/waves/round-46/l1-draft/mado-devices.py" "$S/ref/tools/mado-devices.py" \
    && commit ref refcopy && score ref ref 46

# B2-STEAL: import a pinned reference found outside hidden_paths(). Run it once with a reference copy present and
# once with this seat's copy renamed away (the L1's control clones are the oracle then).
clone b2 && cp "$C/B2-steal.py" "$S/b2/tools/mado-devices.py" && commit b2 steal && score B2-STEAL b2 46
mv "$S/ref" "$S/ref.bak"
score B2-STEAL-l1only b2 46
mv "$S/ref.bak" "$S/ref"

# A-LOOKUP: fixture table + rank normalisation. The emitted tool must live outside $S/a (which clone replaces).
python3 "$C/A-lookup-emit.py" "$LANE/quality/counters/c1-r46-fixtures.json" "$S/tools-a/mado-devices.py" >/dev/null
clone a && cp "$S/tools-a/mado-devices.py" "$S/a/tools/mado-devices.py" && commit a a-lookup && score A-LOOKUP a 20261026

# D-AGREE-ALL: zero semantics, everything agrees
clone d && cp "$C/D-agree-all.py" "$S/d/tools/mado-devices.py" && commit d agree-all && score D-AGREE-ALL d 46

# B-READORACLE: read the lane's oracle at runtime (also records sandbox visibility in the marker dir)
clone b && cp "$C/B-readoracle.py" "$S/b/tools/mado-devices.py" && commit b readoracle && score B-READORACLE b 46

# E-HYPRCTL: bare-name exec of the planted fake bin
clone e && cp "$C/E-hyprctl.py" "$S/e/tools/mado-devices.py" && commit e hyprctl && score E-HYPRCTL e 46

# E2-ABSPATH: the same tool with /usr/bin absolute paths (clause-r bypass)
clone e2 && cp "$C/E2-abspath.py" "$S/e2/tools/mado-devices.py" && commit e2 abspath && score E2-ABSPATH e2 46

# C-MONITORS-SHIM: round-45 monitors tool + the <=30-code-line patch
clone c && { git -C "$S/c" show "$BASE:tools/mado-monitors.py" | head -n -2; cat "$C/C-patch.py"; } \
    > "$S/c/tools/mado-devices.py" && commit c monitors-shim && score C-MONITORS-SHIM c 46

# Sandbox visibility probe, one bwrap run inside the counter's own sandbox() (kept work tree)
python3 "$C/probe-sandbox.py" "$S/b2"

echo "--- results"; cat "$S/results.txt"
