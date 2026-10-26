#!/bin/sh
# verify-quotes.sh - every quote printed in report.md is <= 25 words, is found verbatim at the
# cited line of the cited frozen file, and is present verbatim in report.md itself.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-43/w1/LabRe2Fuzz
rc=0

check() {
  file=$1
  line=$2
  text=$3
  got=$(sed -n "${line}p" "$LANE/$file")
  words=$(printf '%s' "$text" | wc -w)
  case "$got" in
    *"$text"*)
      echo "OK   $file:$line  (${words} words) found: $text" ;;
    *)
      echo "FAIL $file:$line  (${words} words) missing: $text"
      echo "     line is: $got"
      rc=1 ;;
  esac
  if grep -Fq "$text" "$SEAT/report.md"; then
    echo "     present verbatim in report.md"
  else
    echo "     NOT present verbatim in report.md"
    rc=1
  fi
  if [ "$words" -gt 25 ]; then
    echo "     quote longer than 25 words"
    rc=1
  fi
}

check ".ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp" 16 \
  'return re2::RE2::FullMatch(other, *m_regex) != m_negative;'
check ".ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp" 12 \
  'm_regex = makeUnique<re2::RE2>(regex);'
check "quality/counters/c1-r42-geometry.py" 89 \
  'the REGEX alphabet is restricted so the two agree on it, and a regex outside it is `unsupported`'
check ".ufo/waves/round-42/c1/ctl-ref-tool.py.txt" 34 \
  'REGEX is 1-200 characters of `[A-Za-z0-9_.^$()|*+?-]` and the escapes'
check ".ufo/waves/round-42/c1/ctl-ref-tool.py.txt" 40 \
  '`re.fullmatch(REGEX, class)` succeeds (Hyprland: `RE2::FullMatch`).'

if [ "$rc" -eq 0 ]; then echo "QUOTES VERDICT: PASS"; else echo "QUOTES VERDICT: FAIL"; fi
exit "$rc"
