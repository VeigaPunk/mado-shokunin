# RevSelftest — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Run the lane's standing suite read-only and record it exactly: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && bash tools/mado-verify.sh --selftest`, plus `sha256sum tools/mado-verify.sh` and `wc -l tools/mado-verify.sh`. Report the final `MADO_SELFTEST:` line, the exit code, and whether the tool bytes are unchanged from the round-35 tip (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse 7a068cb:tools/mado-verify.sh`).
