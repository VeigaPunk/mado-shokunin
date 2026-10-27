#!/bin/bash
# Verify every quoted fragment used in findings.md against its source (read-only grep).
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
F=/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/mado.md
ok=0; fail=0
chk() { # chk <file> <fragment>
  local f="$1"; shift
  local frag="$1"; shift
  local lines=$(grep -nF -- "$frag" "$f" | cut -d: -f1 | tr '\n' ' ')
  if [ -n "$lines" ]; then
    echo "OK   [$frag] -> lines $lines ($f)"
    ok=$((ok+1))
  else
    echo "FAIL [$frag] NOT FOUND in $f"
    fail=$((fail+1))
  fi
}
chk "$L/.ufo/waves/round-47/w2/ExecC1Determinism.md" "clause f/x are blind to the readdir axis"
chk "$L/.ufo/waves/round-47/w2/ExecC1Determinism.md" "passes all 190 fixtures and all 190 explain checks"
chk "$L/tools/mado-terminal.py" "Also out of contract: -h/--help, HOME unset, a FIFO named like a desktop file in a"
chk "$F" "the session-material gate reads \`findings=128\` at the tip (115 at base)"
chk "$L/SKILL.md" "no synthetic marker yet, so a red exit is expected until it lands"
chk "$L/.ufo/waves/round-47/registration.md" "bwrap allowlist root without /usr/bin, /usr/share, /etc, /home, /fast"
chk "$L/.ufo/waves/round-47/w2/SentC1Sandbox.md" "F1 — clause text falsified: \`/fast\` IS in the root, writable, and host paths are readable"
chk "$L/.ufo/waves/round-47/w2/CritC1Explain.md" "a capture differing only in the command-line (third printed item) can be reported AGREE"
chk "$L/corpus/knowledge/xdg-terminal-selection-r47.md" "terminal-route-r17.md:150-151"
chk "$L/corpus/knowledge/terminal-route-r17.md" "[UNK] Whether the \`--dir=\` value from \`omarchy-cmd-terminal-cwd\` is valid at"
echo "---"; echo "verify: ok=$ok fail=$fail"
test "$fail" -eq 0
