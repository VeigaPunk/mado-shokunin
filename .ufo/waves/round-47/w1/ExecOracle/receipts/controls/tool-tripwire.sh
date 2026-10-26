#!/bin/sh
# HARNESS SELF-TEST CONTROL: runs a case terminal stub, to prove the stub writes
# its marker and exits non-zero (the tripwire the real judge relies on).
"$HOME/../bin/alacritty" --tripwire 2>/dev/null || true
printf 'no-terminal\n'
