#!/bin/bash
# verify every quoted sentence against its located source line
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/registration.md
C=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r46-devices.py
A=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py
P=/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-46.md
chk() { grep -nF -- "$2" "$1" | head -1 | sed "s|^|OK $1:|"; }
chk "$R" "every published axis ties at its maximum at base"
chk "$R" "so each is a lowest axis"
chk "$R" "at the data commit and the round tip, under any nonce"
chk "$R" "may re-register as v2 with a new freeze"
chk "$R" "a tool holding a model of the contract is an implementation of it"
chk "$R" "new rows S316-S325"
chk "$R" "A tool-only tree meets C1 and misses C2"
chk "$R" "control, not the data"
chk "$C" "The model is invisible to the tool (clause i)."
chk "$C" "the read-only clause catches PATH lookups only"
chk "$A" "the lane's published axis table must not be stale"
chk "$P" "A target must be one a do-nothing control cannot reach"
chk "$P" "score it with the frozen counter, and commit that receipt"
chk "$P" "is not the claim's rule"
chk "$P" "Use no universal clauses"
chk "$P" "Declare each after-state as one concrete value"
