#!/bin/sh
# MutRoutedR3 driver 1 (v2) — private clone, pristine marker runs, plant controls.
# Authored outputs: bounded by ulimit -f 2048 (<<1 MiB each).
# Exception, disclosed: git index writes (~4 MiB internal .git/index) need a
# lifted limit in the confined gitx() subshell; no artifact of this seat does.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-48/w1/ExecSessionMarker
S=/fast/scratch/hyaku/mado-r48/MutRoutedR3
OUT=$S/out
CLONE=$S/clone
BASE=579f694b45c797a9c39761fdb4f9e0a1b71b3585
FX=.ufo/waves/round-48/w2/MutRoutedR3-fx
ID="-c user.name=MutRoutedR3 -c user.email=mutroutedr3@scratch.invalid"
SENT='[{"address": "0x1", "class": "org.example.fake", "title": "redacted", "pid": 42}]'
REAL='[{"address": "0x1", "class": "org.example.fake", "title": "Example Domain", "pid": 42}]'
ulimit -Sf 2048
export TMPDIR=$S/tmp
mkdir -p "$OUT" "$TMPDIR"
exec >> "$OUT/log1.txt" 2>&1

# gitx: run git with the SOFT file-size limit lifted ONLY for its internal
# index writes (.git/index, >1 MiB for 20k entries). Main shells run
# `ulimit -Sf 2048` (hard limit untouched); every authored artifact stays <=1 MiB.
gitx() { sh -c 'ulimit -Sf unlimited; exec git "$@"' git "$@"; }

log() { printf '\n=== %s\n' "$*"; }
gate() { # gate <outname> <extra-args...>
    outn=$1; shift
    start=$(date +%s)
    python3 -I "$CLONE/quality/check-session-material.py" --repo "$CLONE" --rev HEAD "$@" \
        > "$OUT/$outn.txt" 2>&1
    rc=$?
    printf '%s rc=%d %ss\n' "$outn" "$rc" "$(( $(date +%s) - start ))" | tee -a "$OUT/rcs.txt"
    grep -E '^(SESSION_MATERIAL|WAIVER |WAIVER_REJECTED .*(C00_shipped|MutRoutedR3-fx|session-clients|ExecSessionMarker/check))' \
        "$OUT/$outn.txt" | tail -12
}
commit() { # commit <message>
    TL=$(git -C "$CLONE" rev-parse --show-toplevel)
    [ "$TL" = "$CLONE" ] || { echo "TOPLEVEL GUARD FAILED: $TL" >&2; exit 9; }
    gitx -C "$CLONE" $ID commit -qm "$1" || { echo "COMMIT_FAILED: $1" >&2; exit 8; }
    sha=$(git -C "$CLONE" rev-parse HEAD)
    printf '%s %s\n' "$sha" "$1" >> "$OUT/commits.txt"
    echo "commit $sha $1"
}

log "ulimit-f=$(ulimit -f) git=$(git --version) python=$(python3 --version 2>&1)"
log "clone (no-checkout: gate reads the object DB; no >1MiB worktree writes)"
rm -rf "$CLONE"
git clone -q --shared --no-checkout "$LANE" "$CLONE" || exit 1
TL=$(git -C "$CLONE" rev-parse --show-toplevel)
[ "$TL" = "$CLONE" ] || { echo "TOPLEVEL GUARD FAILED: $TL" >&2; exit 9; }
log "detach HEAD to base via plumbing (gitx: internal index write only)"
gitx -C "$CLONE" update-ref --no-deref HEAD "$BASE"
gitx -C "$CLONE" read-tree "$BASE" || { echo "READ_TREE_FAILED" >&2; exit 1; }
echo "HEAD=$(git -C "$CLONE" rev-parse HEAD) want=$BASE"
ls -l "$CLONE/.git/index"

log "input hashes (pristine)"
sha256sum "$SEAT/check-session-material.py" "$SEAT/session-material-waivers.txt" \
    > "$OUT/pristine-input-hashes.txt"; cat "$OUT/pristine-input-hashes.txt"

log "D00 selftest"
start=$(date +%s)
python3 -I "$SEAT/check-session-material.py" --selftest > "$OUT/D00-selftest.txt" 2>&1
rc=$?
echo "selftest rc=$rc elapsed=$(( $(date +%s) - start ))s"
tail -1 "$OUT/D00-selftest.txt"

log "D01 tracked old gate at base (pristine baseline, receipts/01 equivalent)"
git -C "$CLONE" show "$BASE:quality/check-session-material.py" > "$OUT/old-gate-base.py"
start=$(date +%s)
python3 -I "$OUT/old-gate-base.py" --repo "$CLONE" --rev "$BASE" > "$OUT/D01-base-old-gate.txt" 2>&1
echo "D01 rc=$? elapsed=$(( $(date +%s) - start ))s"
tail -2 "$OUT/D01-base-old-gate.txt"

log "install marker set (commit c1)"
mkdir -p "$CLONE/quality"
sh "$SEAT/install.sh" "$CLONE"
SIDECARS=$(find "$SEAT/sidecars" -type f -name '*.synthetic' | sed "s|^$SEAT/sidecars/||")
# shellcheck disable=SC2086
gitx -C "$CLONE" add -- quality/check-session-material.py quality/session-material-waivers.txt $SIDECARS
echo "staged=$(gitx -C "$CLONE" diff --cached --name-only | wc -l)"
commit "scratch: install round-48 marker set (MutRoutedR3 replay)"
git -C "$CLONE" rev-parse HEAD > "$S/state-c1.txt"
sha256sum "$CLONE/quality/session-material-waivers.txt" "$CLONE/quality/check-session-material.py" \
    >> "$OUT/pristine-input-hashes.txt"

log "D02 install rev, marked (pristine, receipts/11 equivalent)"
gate D02-install-marked
log "D03 install rev, --no-waivers (receipts/05 equivalent)"
gate D03-install-nowaivers --no-waivers

log "P-b unmarked plant (commit c2)"
mkdir -p "$CLONE/$FX"
printf '%s\n' "$SENT" > "$CLONE/$FX/unmarked-clients.json"
gitx -C "$CLONE" add -- "$FX/unmarked-clients.json"
commit "scratch: plant unmarked synthetic client dump"
gate D04-unmarked

log "P-a marked plant (commit c3)"
SHA=$(sha256sum "$CLONE/$FX/unmarked-clients.json" | cut -d' ' -f1)
printf 'SYNTHETIC-MATERIAL v1 kind=fixture rules=R1_CLIENT_DUMP sha256=%s\n' "$SHA" \
    > "$CLONE/$FX/unmarked-clients.json.synthetic"
printf '%s %s R1_CLIENT_DUMP kind=fixture\n' "$FX/unmarked-clients.json" "$SHA" \
    >> "$CLONE/quality/session-material-waivers.txt"
gitx -C "$CLONE" add -- "$FX/unmarked-clients.json.synthetic" quality/session-material-waivers.txt
commit "scratch: mark unmarked plant (sidecar+registry row)"
gate D05-marked

log "P-c planted-real outside waves (commit c4)"
mkdir -p "$CLONE/.ufo/reports"
printf '%s\n' "$REAL" > "$CLONE/.ufo/reports/session-clients.json"
SHA=$(sha256sum "$CLONE/.ufo/reports/session-clients.json" | cut -d' ' -f1)
printf 'SYNTHETIC-MATERIAL v1 kind=fixture rules=R1_CLIENT_DUMP sha256=%s\n' "$SHA" \
    > "$CLONE/.ufo/reports/session-clients.json.synthetic"
printf '%s %s R1_CLIENT_DUMP kind=fixture\n' ".ufo/reports/session-clients.json" "$SHA" \
    >> "$CLONE/quality/session-material-waivers.txt"
gitx -C "$CLONE" add -- .ufo/reports/session-clients.json .ufo/reports/session-clients.json.synthetic \
    quality/session-material-waivers.txt
commit "scratch: plant real-shaped dump with forged marker outside waves"
gate D06-forged-outside

log "P-c2 planted-real inside waves (commit c5)"
printf '%s\n' "$REAL" > "$CLONE/$FX/forged-real.json"
SHA=$(sha256sum "$CLONE/$FX/forged-real.json" | cut -d' ' -f1)
printf 'SYNTHETIC-MATERIAL v1 kind=fixture rules=R1_CLIENT_DUMP sha256=%s\n' "$SHA" \
    > "$CLONE/$FX/forged-real.json.synthetic"
printf '%s %s R1_CLIENT_DUMP kind=fixture\n' "$FX/forged-real.json" "$SHA" \
    >> "$CLONE/quality/session-material-waivers.txt"
gitx -C "$CLONE" add -- "$FX/forged-real.json" "$FX/forged-real.json.synthetic" \
    quality/session-material-waivers.txt
commit "scratch: plant real-shaped dump with forged marker under waves"
gate D07-forged-inside

log "restore plants (commit c6) back to pristine install bytes"
gitx -C "$CLONE" rm -q -- "$FX/unmarked-clients.json" "$FX/unmarked-clients.json.synthetic" \
    "$FX/forged-real.json" "$FX/forged-real.json.synthetic" \
    .ufo/reports/session-clients.json .ufo/reports/session-clients.json.synthetic
gitx -C "$CLONE" checkout "$(cat "$S/state-c1.txt")" -- quality/session-material-waivers.txt
commit "scratch: restore pristine install state"
gate D08-restored-pristine
sha256sum "$CLONE/quality/session-material-waivers.txt" >> "$OUT/pristine-input-hashes.txt"

log "driver1 done"
