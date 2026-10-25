#!/usr/bin/env bash
# Quote verification for ExecJournalHistory/finding.md (round 41, w1).
# For each quote: it must appear verbatim (a) in the receipt finding.md and (b) in the named source.
# Read-only: only journalctl reads, file reads and strings.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FINDING="$HERE/finding.md"
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
FETCH=$LANE/.ufo/waves/round-41/fetch
COUNTER=$LANE/quality/counters/c1-r41-globals.py
BIN=/usr/lib/xdg-desktop-portal-hyprland
HYPRLOG=$(ls /run/user/1000/hypr/*/hyprland.log 2>/dev/null | sed -n '1p')
fails=0

check() { # check <label> <quote> <source-cmd...>
  local label="$1" quote="$2"; shift 2
  local in_receipt=0 in_source=0
  grep -Fq -- "$quote" "$FINDING" && in_receipt=1
  if "$@" 2>/dev/null | grep -Fq -- "$quote"; then in_source=1; fi
  if [ "$in_receipt" = 1 ] && [ "$in_source" = 1 ]; then
    printf 'MATCH    %-34s words=%-3s %s\n' "$label" "$(printf '%s' "$quote" | wc -w)" "$quote"
  else
    printf 'MISS     %-34s receipt=%s source=%s  %s\n' "$label" "$in_receipt" "$in_source" "$quote"
    fails=$((fails+1))
  fi
}

check "journald accounting" \
  "Consumed 43.752s CPU time over 1d 15h 21min 17.607s wall clock time" \
  journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o cat

check "counter session model" \
  "or its PID differs from the open session's PID" \
  sed -n '33,35p' "$COUNTER"

check "counter diff line" \
  "MADO_GLOBALS_DIFF: from=<k-1> to=<k> added=<csv|-> removed=<csv|->" \
  sed -n '43p' "$COUNTER"

check "init-phase toplevel line" \
  "[toplevel] Activated, bound to 55cc6bdd08d0, toplevels: 0" \
  journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o cat

check "banner head (binary)" \
  "Gathering exported interfaces" \
  strings -a "$BIN"

check "banner head 1 (binary)" \
  "Initializing xdph..." \
  strings -a "$BIN"

check "advert format (binary)" \
  "| Got interface: {} (ver {})" \
  strings -a "$BIN"

check "truncated tail" \
  "[core] dmabufFeedbackMa" \
  journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o cat

check "session-2 last advert" \
  "Got interface: ext_output_image_capture_source_manager_v1 (ver 1)" \
  journalctl --user -u xdg-desktop-portal-hyprland -b 0 --no-pager -o cat

check "vacuum audit line" \
  "COMMAND=/usr/bin/journalctl --vacuum-size=50M" \
  journalctl --no-pager -o cat

check "boot-0 output present" \
  "drm: Connecting connector DP-1, CRTC ID 205" \
  cat "$HYPRLOG"

check "session-1 dmabuf advert" \
  "Got interface: zwp_linux_dmabuf_v1 (ver 5)" \
  journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o cat

echo "---"
echo "quotes verified: 12, failures: $fails"
exit $((fails > 0))
