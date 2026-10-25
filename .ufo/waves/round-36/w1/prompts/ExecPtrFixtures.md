# ExecPtrFixtures — executor seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: executor

Build the negative fixtures for the tip transcript requirement in /tmp: a receipt named for a non-ancestor commit, one whose `MADO_AXIS:` line says `mismatched=1`, one whose line says `rev=` a different hash than the filename, and one correct one (produce it honestly by running `python3 -I quality/check-axis-scores.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev <a real commit>` if that gate supports it; otherwise copy a real transcript and correct its rev). Run LANE/quality/check-evidence-pointers.py against copies of the lane that differ only in `quality/receipts/`. Report each verdict. Do not write into LANE.
