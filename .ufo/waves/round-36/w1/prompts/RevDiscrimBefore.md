# RevDiscrimBefore — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Re-run the frozen before measurement and audit every line of it. Command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-counter-discrimination.py --profile r35 --manifest .ufo/waves/round-36/controls/manifest.json --receipts /tmp/w36-rev-discrim`. It must print the same 14/25 the freeze recorded. For each `ok=0` line, name which routed defect it exposes (D3 dead digest clause; the E12 registry-section gap from round-35 `RevC1Tip` F2; D4's self-authored ledger observables) and quote the evidence in LANE/.ufo/waves/round-35/ that shows the class. Confirm no `ok=0` line is a legitimate reject of a legitimate control: check each of the 15 c1 controls and 9 c2 controls individually. Verdict per control.
