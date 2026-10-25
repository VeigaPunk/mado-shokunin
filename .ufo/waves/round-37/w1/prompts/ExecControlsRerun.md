# ExecControlsRerun — executor seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: executor

Re-run the round's controls exactly: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-37/controls.py --out /dev/shm/mado37-ExecControlsRerun/controls.txt` and diff the control lines (ignore sandbox commit hashes) against /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/receipts/controls-v2.txt. Then add, in your own scratch copy of controls.py (never the lane's), three further controls and report their verdicts with the frozen counters: (a) C1 entries carrying the quotes and OBS lines but the README rows placed outside the `## Coverage map` section; (b) the right rows but `used-by` naming a different path; (c) a Gate line whose receipt path exists but at a different revision's bytes (digest mismatch after editing one byte of the receipt). Each must be TARGET_MISSED; a TARGET_MET is a finding.
