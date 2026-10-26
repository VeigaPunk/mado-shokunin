#!/usr/bin/env bash
# ExecOracleGkeep (round 43 w1): rebuild of the round-26 oracle tinywl (wlroots 0.20.2).
# Adapted copy of .ufo/waves/round-26/harness/build-tinywl.sh with D repointed at round-43 scratch,
# meson named by absolute uv-tool path, and the patch read from this seat dir. Original never edited.
set -eu
D=/fast/scratch/hyaku/mado-r43/oracle
S=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecOracleGkeep
MESON=/home/vgpnk/.local/bin/meson
cd "$D"
test "$(git -C wlroots rev-parse HEAD)" = d783533489e1f75d6886c2ab5c5960090ef268f8
cd wlroots
git apply "$S/tinywl-global-versions.patch" 2>/dev/null || true
timeout 300 "$MESON" setup build -Dbackends= -Dsession=disabled -Dxwayland=disabled -Drenderers=gles2 \
  -Dallocators=gbm -Dexamples=true -Dprefix="$D/wlr-prefix"
timeout 900 ninja -C build
sha256sum build/tinywl/tinywl build/libwlroots-0.20.so
