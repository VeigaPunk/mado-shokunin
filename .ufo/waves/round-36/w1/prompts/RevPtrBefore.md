# RevPtrBefore — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Re-run the C2 before measurement and audit it: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-evidence-pointers.py --rev master`. Confirm the four before-defects the registration names (dangling_r35=2 with the exact two paths, inherited_dirty=10 with the paths, scratch_disposition_ok=0, tip_axis_transcript=0) and the `setup=missing-r36-sections` line. Check the pointer extractor's output by hand: list every backticked lane path in the round-35 LOG/SCORECARD sections and say which the extractor missed or over-counted.
