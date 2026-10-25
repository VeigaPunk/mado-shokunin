# RevC1RedBefore — C1 red-before re-derivation (round-39 w1)

Scope: independently re-derive the C1 red-before in a sandbox (no lane mutations):
extract the round-38 frozen manifest via `git show`, run the discrimination checker
with the current counters, confirm `controls=19 correct=18/19 verdict=TARGET_MISSED`
exit 1 with sole failing control `c1-duprow` (ok=0).

## Method (all scratch outside the lane, in /tmp/c1-redbefore-sandbox)

1. Manifest extraction (read-only git, sandbox target):
   `cd /home/vgpnk/Projects/shokunin/mado-shokunin`
   `git show 58e55ec:.ufo/waves/round-38/controls/manifest.json > /tmp/c1-redbefore-sandbox/manifest-frozen-r38.json`
   → `show_exit=0`; JSON parse ok, `controls=19`.
   sha256 = `14c49d9fec35dc9bc307fbdd5c732e2ce80fabeaadfe3327b9121f50b9553edb`
   — byte-identical to `.ufo/waves/round-39/receipts/manifest-frozen-r38.json` (same sha).
2. State checks:
   - Lane tip: `git rev-parse HEAD` = `457d1b125932c1e0d797061a2156b917bcd7edaa`
     (registration base `08be4eb7fd13358ed29b096e8924005d46ac409c` is an ancestor:
     `git merge-base --is-ancestor` exit 0).
   - Counters `quality/counters/c1-r38-event-ground.py`,
     `quality/counters/c2-r38-eventq.py`: `git diff --stat` empty between base↔HEAD
     and worktree↔HEAD → unchanged at base, tip, and worktree. "Current counters"
     ≡ frozen counters.
3. Checker run (exactly the registered command; `--rev` = named base commit
   08be4eb7…; counters from worktree):
   `python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest /tmp/c1-redbefore-sandbox/manifest-frozen-r38.json --rev 08be4eb7fd13358ed29b096e8924005d46ac409c --out /tmp/c1-redbefore-sandbox/c1-redbefore-my-run.txt --sandbox-root /tmp/c1-redbefore-sandbox`
   → `checker_exit=1`.

## Output (verbatim, `c1-redbefore-my-run.txt`)

```
control=c1-live instrument=c1 expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-donothing instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-selfreceipt instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-quotefloor instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-nolineage instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-r28-verbatim instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-token-stub instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-clause-b instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-live instrument=c2 expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-donothing instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-forged instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-impsock instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-lagconst instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-missall instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-onepass instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-docconn instrument=c2 expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-stub-clean instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-proc-mismatch instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED
```

## Result

- `controls=19 correct=18/19 verdict=TARGET_MISSED`, `checker_exit=1` ✓ (target met).
- Sole failing control: `c1-duprow` (expected MISSED, observed MET, ok=0); append-at-file-end
  row is outside the counter's `## Registry` parser (consistent with the round-38 errata).
- Independent run `diff`-identical to the registered receipt
  `.ufo/waves/round-39/receipts/c1-redbefore.txt`.
- No lane file written/touched by this leaf; all scratch in `/tmp/c1-redbefore-sandbox`.
  No tools installed (stdlib-only checker; no installs to record).

## Final answer

1. Red-before re-derived independently: frozen round-38 manifest (git show 58e55ec:…, sha256 14c49d9f…) × unchanged counters at 08be4eb7 → controls=19 correct=18/19 verdict=TARGET_MISSED, exit 1.
2. Sole failing control c1-duprow (expected MISSED, observed MET, ok=0).
3. Output byte-identical to registered receipt .ufo/waves/round-39/receipts/c1-redbefore.txt.
4. Lane tip is now 457d1b1 (base is ancestor); counters verified unchanged base↔HEAD↔worktree.
5. No lane mutations, no installs; scratch only in /tmp/c1-redbefore-sandbox.
