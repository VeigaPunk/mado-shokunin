#!/usr/bin/env bash
# Rebuild the round-26 oracle parent compositor (tinywl, wlroots 0.20.2) exactly as pinned in oracle.py.
# Needs meson (installed this round: `uv tool install meson` -> 1.12.1), ninja, gcc and the wlroots deps
# already on the host (wayland 1.26.0, wayland-protocols 1.49, libdrm 2.4.134, mesa gbm/egl/glesv2,
# xkbcommon 1.13.2, pixman 0.46.4). Writes only under /fast/scratch/hyaku/mado-r26/wlroots.
set -eu
D=/fast/scratch/hyaku/mado-r26
cd "$D"
timeout 200 git clone -q --depth 1 --branch 0.20.2 https://gitlab.freedesktop.org/wlroots/wlroots.git wlroots
cd wlroots
test "$(git rev-parse HEAD)" = d783533489e1f75d6886c2ab5c5960090ef268f8
git apply "$(dirname "$(readlink -f "$0")")/tinywl-global-versions.patch"
timeout 300 meson setup build -Dbackends= -Dsession=disabled -Dxwayland=disabled -Drenderers=gles2 \
  -Dallocators=gbm -Dexamples=true -Dprefix="$D/wlr-prefix"
timeout 600 ninja -C build
sha256sum build/tinywl/tinywl build/libwlroots-0.20.so
