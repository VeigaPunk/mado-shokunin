#!/usr/bin/env bash
# Computed locator check for the S302-S308 draft cells (ScrSupersedeRows, round 44 w1).
# Every line number and count asserted by a draft cell is recomputed here from the pinned bytes.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
F43=$LANE/.ufo/waves/round-43/fetch
F44=$LANE/.ufo/waves/round-44/fetch
pass=0; fail=0
chk() { # chk <label> <file> <line> <grep -E pattern>
  local label=$1 file=$2 line=$3 pat=$4 got
  got=$(sed -n "${line}p" "$file")
  if printf '%s' "$got" | grep -Eq -- "$pat"; then pass=$((pass+1)); printf 'ok\t%s\t%s:%s\n' "$label" "$(basename "$file")" "$line"
  else fail=$((fail+1)); printf 'FAIL\t%s\t%s:%s\tgot=%s\n' "$label" "$(basename "$file")" "$line" "$got"; fi
}
cnt() { # cnt <label> <file> <pattern> <expected>
  local label=$1 file=$2 pat=$3 want=$4 got
  got=$(grep -cE -- "$pat" "$file")
  if [ "$got" = "$want" ]; then pass=$((pass+1)); printf 'ok\t%s\tcount=%s\n' "$label" "$got"
  else fail=$((fail+1)); printf 'FAIL\t%s\tcount=%s want=%s\n' "$label" "$got" "$want"; fi
}

# --- S302 RegexMatchEngine.cpp (470 B, sha 8ca65533)
chk S302-ctor-open  "$F43/Hyprland-RegexMatchEngine.cpp" 6  '^CRegexMatchEngine::CRegexMatchEngine\(const std::string& regex\) \{'
chk S302-ctor-close "$F43/Hyprland-RegexMatchEngine.cpp" 13 '^\}'
chk S302-match-open "$F43/Hyprland-RegexMatchEngine.cpp" 15 '^bool CRegexMatchEngine::match\(const std::string& other\) \{'
chk S302-match-close "$F43/Hyprland-RegexMatchEngine.cpp" 17 '^\}'
chk S302-neg-strip  "$F43/Hyprland-RegexMatchEngine.cpp" 7  'starts_with\("negative:"\)'
chk S302-substr9    "$F43/Hyprland-RegexMatchEngine.cpp" 9  'substr\(9\)'
chk S302-fullmatch  "$F43/Hyprland-RegexMatchEngine.cpp" 16 're2::RE2::FullMatch\(other, \*m_regex\) != m_negative'
cnt S302-lines      "$F43/Hyprland-RegexMatchEngine.cpp" '' 17

# --- S303 DefaultFloatingAlgorithm.cpp (10359 B, sha f05f2561)
chk S303-const      "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 16 'DEFAULT_SIZE = \{640, 400\}'
chk S303-firstmap   "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 49 'if \(target->window\(\) && target->window\(\)->m_firstMap\) \{'
chk S303-sizetest   "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 55 'if \(WINDOW->m_ruleApplicator->static_.size\) \{'
chk S303-computed   "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 56 'const auto COMPUTED = WINDOW->calculateExpression'
chk S303-overwrite  "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 60 'windowGeometry\.w = COMPUTED->x;'
chk S303-overwrite2 "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 61 'windowGeometry\.h = COMPUTED->y;'
chk S303-poswarp    "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 64 'positionAnimation\(\)->setValueAndWarp\(\*COMPUTED\)'
chk S303-center     "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 79 'static_.center.value_or\(false\)'
chk S303-recenter-i "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 90 'if \(!posOverridden && \(!DESIRED_GEOM \|\| !DESIRED_GEOM->pos\)\)'
chk S303-place-if   "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 93 'if \(posOverridden'
chk S303-place-call "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 96 'target->setPositionGlobal\(windowGeometry\);'
chk S303-place-else "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 102 'target->setPositionGlobal\(windowGeometry\);'
cnt S303-tiled-2402 "$F44/Hyprland-Window.cpp" '^        if \(m_ruleApplicator->static_\.size\) \{' 1
chk S303-tiled-a    "$F44/Hyprland-Window.cpp" 2402 'if \(m_ruleApplicator->static_.size\) \{'
chk S303-tiled-b    "$F44/Hyprland-Window.cpp" 2403 'calculateExpression\(\*m_ruleApplicator->static_.size\)'
chk S303-tiled-c    "$F44/Hyprland-Window.cpp" 2408 'setPseudoSize\(\*COMPUTED\)'

# --- S304 Target.cpp (3064 B, sha 49323833)
chk S304-store      "$F43/Hyprland-Target.cpp" 10 'void ITarget::setPositionGlobal\(const STargetBox& box, uint8_t\) \{'
chk S304-assign     "$F43/Hyprland-Target.cpp" 11 'm_box = box;'
chk S304-roundL     "$F43/Hyprland-Target.cpp" 12 'm_box.logicalBox.round\(\);'
chk S304-roundV     "$F43/Hyprland-Target.cpp" 13 'm_box.visualBox.round\(\);'
chk S304-overload   "$F43/Hyprland-Target.cpp" 16 'void ITarget::setPositionGlobal\(const CBox& box, uint8_t flags\) \{'
chk S304-position   "$F43/Hyprland-Target.cpp" 64 'CBox ITarget::position\(\) const \{'
chk S304-logical    "$F43/Hyprland-Target.cpp" 65 'return m_box.logicalBox;'
chk S304-remember   "$F43/Hyprland-Target.cpp" 68 'void ITarget::rememberFloatingSize'
chk S304-lastfloat  "$F43/Hyprland-Target.cpp" 72 'Vector2D ITarget::lastFloatingSize\(\) const \{'

# --- S305 WindowTarget.cpp (16614 B, sha 8bcaf370)
chk S305-setpos     "$F43/Hyprland-WindowTarget.cpp" 36 'void CWindowTarget::setPositionGlobal\(const STargetBox& box, uint8_t flags\) \{'
chk S305-updatepos  "$F43/Hyprland-WindowTarget.cpp" 39 'updatePos\(flags\);'
chk S305-float-if   "$F43/Hyprland-WindowTarget.cpp" 70 'if \(floating\(\) && m_window && !Fullscreen::controller\(\)->isFullscreen'
chk S305-setbox     "$F43/Hyprland-WindowTarget.cpp" 71 'm_window->setBox\(m_box.logicalBox\);'
chk S305-sendwin    "$F43/Hyprland-WindowTarget.cpp" 74 'm_window->sendWindowSize\(\);'
chk S305-sendgate   "$F43/Hyprland-WindowTarget.cpp" 73 'if \(CONFIGURECLIENT\)'
chk S305-clampfn    "$F43/Hyprland-WindowTarget.cpp" 297 'Vector2D CWindowTarget::clampSizeForDesired'
chk S305-clampmin   "$F43/Hyprland-WindowTarget.cpp" 300 'newSize = newSize.clamp\(\*m\);'
chk S305-clampmax   "$F43/Hyprland-WindowTarget.cpp" 302 'newSize = newSize.clamp\(Vector2D\{MIN_WINDOW_SIZE'
chk S305-desired    "$F43/Hyprland-WindowTarget.cpp" 306 'desiredGeometry\(\) \{'
chk S305-clientg    "$F43/Hyprland-WindowTarget.cpp" 310 'DESIRED_GEOM = g_pXWaylandManager->getGeometryForWindow'
chk S305-clampdes   "$F43/Hyprland-WindowTarget.cpp" 313 'requested.size = clampSizeForDesired\(DESIRED_GEOM.size\(\)\);'
chk S305-stored     "$F43/Hyprland-WindowTarget.cpp" 323 'const auto STOREDSIZE = .*persistentSize\(\)'
chk S305-storeduse  "$F43/Hyprland-WindowTarget.cpp" 326 'requested.size = clampSizeForDesired\(\*STOREDSIZE\);'
chk S305-small      "$F43/Hyprland-WindowTarget.cpp" 339 'if \(DESIRED_GEOM.width <= 2 \|\| DESIRED_GEOM.height <= 2\) \{'
chk S305-surf5      "$F43/Hyprland-WindowTarget.cpp" 342 'if \(SURFACE->m_current.size.x > 5 && SURFACE->m_current.size.y > 5\) \{'
chk S305-surfpos    "$F43/Hyprland-WindowTarget.cpp" 344 'requested.pos.reset\(\);'
chk S305-surfsize   "$F43/Hyprland-WindowTarget.cpp" 345 'requested.size = clampSizeForDesired\(SURFACE->m_current.size\);'
chk S305-x11or      "$F43/Hyprland-WindowTarget.cpp" 350 'if \(m_window->m_isX11 && m_window->isX11OverrideRedirect\(\)\) \{'
chk S305-600x400    "$F43/Hyprland-WindowTarget.cpp" 354 'Vector2D\{600, 400\}'
chk S305-orpos      "$F43/Hyprland-WindowTarget.cpp" 358 'requested.pos  = g_pXWaylandManager->xwaylandToWaylandCoords'
chk S305-nodesired  "$F43/Hyprland-WindowTarget.cpp" 364 'return std::unexpected\(m_window->m_isX11 && m_window->isX11OverrideRedirect\(\) \? GEOMETRY_INVALID_DESIRED : GEOMETRY_NO_DESIRED\);'
chk S305-close      "$F43/Hyprland-WindowTarget.cpp" 396 '^\}'

# --- S306 GeometricMovableAnimated.cpp (1576 B, sha 649f1a8d)
chk S306-goal       "$F43/Hyprland-GeometricMovableAnimated.cpp" 19 'GEOMETRIC_GOAL: return m_realSize->goal\(\);'
chk S306-current    "$F43/Hyprland-GeometricMovableAnimated.cpp" 20 'GEOMETRIC_CURRENT: return m_realSize->value\(\);'
chk S306-posopen    "$F43/Hyprland-GeometricMovableAnimated.cpp" 8 'CGeometricMovableAnimated::position'
chk S306-sizeopen   "$F43/Hyprland-GeometricMovableAnimated.cpp" 17 'CGeometricMovableAnimated::size'
chk S306-boxopen    "$F43/Hyprland-GeometricMovableAnimated.cpp" 26 'CGeometricMovableAnimated::geometricBox'
chk S306-resize     "$F43/Hyprland-GeometricMovableAnimated.cpp" 39 'void CGeometricMovableAnimated::resize'
chk S306-animpos    "$F43/Hyprland-GeometricMovableAnimated.cpp" 53 'positionAnimation\(\) \{'
chk S306-animsize   "$F43/Hyprland-GeometricMovableAnimated.cpp" 57 'sizeAnimation\(\) \{'
cnt S306-lines      "$F43/Hyprland-GeometricMovableAnimated.cpp" '' 59

# --- S307 host-clients-r43.json (711 B, sha 21db902e)
for L in 2 17 32 47; do
  if sed -n "${L}p" "$F43/host-clients-r43.json" | grep -Fxq ' {'; then
    pass=$((pass+1)); printf 'ok\tS307-object-%s\thost-clients-r43.json:%s\n' "$L" "$L"
  else
    fail=$((fail+1)); printf 'FAIL\tS307-object-%s\thost-clients-r43.json:%s\n' "$L" "$L"
  fi
done
for L in 4 19 34 49; do chk "S307-mapped-$L" "$F43/host-clients-r43.json" "$L" '"mapped": true,'; done
for L in 6 21 36 51; do chk "S307-floating-$L" "$F43/host-clients-r43.json" "$L" '"floating": false,'; done
chk S307-class-chromium "$F43/host-clients-r43.json" 50 '"class": "chromium",'
cnt S307-fullscreen "$F43/host-clients-r43.json" 'fullscreen' 0
cnt S307-gkeep      "$F43/host-clients-r43.json" 'gkeep' 0
cnt S307-lines      "$F43/host-clients-r43.json" '' 62
cnt S307-size-1720  "$F43/host-clients-r43.json" '"floating": false' 4

# --- S308 gkeep excerpt (1625 B, sha 3695b788) and its ui.py mapping
chk S308-hdr        "$F43/gkeep-ui-excerpt.py" 1 'excerpt of /home/vgpnk/Projects/gkeep/gkeep/ui.py lines 446-488'
chk S308-appid      "$F43/gkeep-ui-excerpt.py" 6 'application_id="org.omarchy.gkeep",'
chk S308-default    "$F43/gkeep-ui-excerpt.py" 33 'window.set_default_size\(420, 500\)'
cnt S308-sizereq    "$F43/gkeep-ui-excerpt.py" 'set_size_request' 0
cnt S308-excerpt-ln "$F43/gkeep-ui-excerpt.py" '' 45
chk S308-ui449      "/home/vgpnk/Projects/gkeep/gkeep/ui.py" 449 'application_id="org.omarchy.gkeep",'
chk S308-ui476      "/home/vgpnk/Projects/gkeep/gkeep/ui.py" 476 'window.set_default_size\(420, 500\)'
# excerpt line 6 must equal the first data line of ui.py:446-488 (offset 3)
if cmp -s <(sed -n '3,45p' "$F43/gkeep-ui-excerpt.py") <(sed -n '446,488p' /home/vgpnk/Projects/gkeep/gkeep/ui.py); then
  pass=$((pass+1)); printf 'ok\tS308-excerpt-is-ui446-488\n'
else fail=$((fail+1)); printf 'FAIL\tS308-excerpt-is-ui446-488\n'; fi
# byte sizes and hashes cited by the cells
for spec in "470 Hyprland-RegexMatchEngine.cpp 8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282" \
            "10359 Hyprland-DefaultFloatingAlgorithm.cpp f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91" \
            "3064 Hyprland-Target.cpp 49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06" \
            "16614 Hyprland-WindowTarget.cpp 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d" \
            "1576 Hyprland-GeometricMovableAnimated.cpp 649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d" \
            "711 host-clients-r43.json 21db902e1f1234b9f52411cf7885097a18d67b00b9dd0110f9bbd2b36fb442ad" \
            "1625 gkeep-ui-excerpt.py 3695b788c6d766b8e87c01916a6594158a26c2cf816f991ccf30b72d9c5d1713"; do
  set -- $spec; want=$1; f=$2; sha=$3
  gotb=$(wc -c < "$F43/$f"); gots=$(sha256sum "$F43/$f" | cut -d' ' -f1)
  if [ "$gotb" = "$want" ] && [ "$gots" = "$sha" ]; then pass=$((pass+1)); printf 'ok\tbytes+sha\t%s\t%s\n' "$f" "$want"
  else fail=$((fail+1)); printf 'FAIL\tbytes+sha\t%s\t%s/%s got=%s/%s\n' "$f" "$want" "$sha" "$gotb" "$gots"; fi
done
gots=$(sha256sum "$F44/Hyprland-Window.cpp" | cut -d' ' -f1)
if [ "$gots" = d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded ]; then pass=$((pass+1)); printf 'ok\tbytes+sha\tHyprland-Window.cpp (r44 pin)\n'
else fail=$((fail+1)); printf 'FAIL\tbytes+sha\tHyprland-Window.cpp got=%s\n' "$gots"; fi
gots=$(sha256sum /home/vgpnk/Projects/gkeep/gkeep/ui.py | cut -d' ' -f1)
if [ "$gots" = 07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a ]; then pass=$((pass+1)); printf 'ok\tbytes+sha\tui.py full file\n'
else fail=$((fail+1)); printf 'FAIL\tbytes+sha\tui.py full file got=%s\n' "$gots"; fi

printf '\nLOCATORS: checked=%d failed=%d\n' "$((pass+fail))" "$fail"
[ "$fail" = 0 ]
