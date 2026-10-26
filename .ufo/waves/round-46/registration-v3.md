# mado round 46 — registration v3 for C1 only (frozen BEFORE any round-46 data commit)

`PRED-C1-r46-v2` (freeze `2bcc335f236c950fded185a6e7d00c0cda5d80c7`) was scored against its registered controls at that
freeze and **failed them**: `receipts/ctl-c1-v2.txt` ends `CTL_C1v2 VERDICT: FAIL (controls scoring TARGET_MET: 2 of 40;
reference met: 1)` - TRIP-ABSOLUTE-PATH and TRIP-SELFTEST-ONLY met the predicate. Cause: clause r's tripwire was an
inherited pipe, and the tool's own `subprocess.run` closes inherited fds, so the fake `hyprctl` could not write to it.
No seat scored v2 and no data commit exists (lane above the base: `8c5434c6` v1 freeze, `e0be61e4` w1 spec, `2bcc335f`
v2 freeze).

- **Change:** `quality/counters/c1-r46-devices-v3.py` = the v2 counter with clause r on a unix socket the counter listens
  on outside the sandbox (socket file in a read-only bind; the fake binaries connect and send their name; accepted
  connections cannot be taken back). Fixtures (`c1-r46-fixtures-v2.json`), the v2 reference, clauses a/s/f/i/g, the
  target, kill rule and residuals are v2's, byte for byte; `c1-r46-devices-v2.py` stays as frozen.
- **Pre-freeze probe** (scratch, not a receipt of record): TRIP-ABSOLUTE-PATH and TRIP-SELFTEST-ONLY `readonly=fail
  verdict=TARGET_MISSED`, w1 CritC1Cheat cheatB `TARGET_MISSED`, reference `TARGET_MET`.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r46-devices-v3.py --repo . --rev <rev> --work <scratch outside /home/vgpnk/Projects/shokunin> [--nonce N]`
- **Before** (base): `receipts/c1-v3-before-base.txt`. **Target:** `fixtures=110/110 generated=150/150 selftest=ok
  readonly=ok tool=present verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** as v2; no further
  re-registration after data.
- **Controls:** `ctl/run-c1-controls-v3.py` (the v2 set of 40 + REF) → `receipts/ctl-c1-v3.txt`.

C2 stays `PRED-C2-r46-v2` (controls `receipts/ctl-c2-v2.txt`: PASS, wrong 0 of 22).
