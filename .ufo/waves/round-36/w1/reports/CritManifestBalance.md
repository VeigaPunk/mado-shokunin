# CritManifestBalance — critic report (mado round 36, wave 1)

Seat: `L1Mado36.CritManifestBalance`. Assignment: falsify the C1 control set. Scope stayed read-only for production; all mutant outputs and manifest variants were under `/tmp/mado-critmanifestbalance/` (the gate was always run with `--no-receipts`). No tools installed.

## Finding — the gate does not authenticate the frozen manifest (FAIL)

The checker trusts the `--manifest` path and its mutable `controls`/`expect` fields. It does not verify manifest ID, byte identity, expected count, or expected control IDs against the freeze. Therefore the assertion `correct == controls` can be made true by editing only the manifest copy; no counter repair is needed.

### Reproduction A: change expected outcomes

Copied the frozen manifest to `/tmp/mado-critmanifestbalance/manifest-expectflip-targeted.json` and changed `expect` to the *observed* r35 verdict on each of its 11 failing controls (`c1-shape-only`, `c1-fabricated-payload`, `c1-no-registry-heading`, `c1-row-moved-out`, and `c2-tip-stale`, `c2-tip-one-copy`, `c2-blob-corrupt`, `c2-blob-row-deleted`, `c2-clause-deleted`, `c2-receipt-token`, `c2-receipt-unbound`). All other fields and IDs were retained.

Exact command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/check-counter-discrimination.py --profile r35 \
  --manifest /tmp/mado-critmanifestbalance/manifest-expectflip-targeted.json \
  --no-receipts --mutants /tmp/mado-critmanifestbalance/mut-expectflip-targeted
```

Quoted output:

```text
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=25/25 label='round-35 frozen counters (unmodified)' verdict=TARGET_MET
EXIT=0
```

Verdict: **25/25 reached without repairing either counter.** This is a successful falsifier of the gate/manifest provenance, not evidence that the frozen control set itself is invalid. The exact 11 changed expectations are listed above.

### Reproduction B: shrink the control set

A copy retaining only `c1-live`, with the manifest ID unchanged:

```sh
python3 -I quality/check-counter-discrimination.py --profile r35 \
  --manifest /tmp/mado-critmanifestbalance/manifest-shrink.json \
  --no-receipts --mutants /tmp/mado-critmanifestbalance/mut-shrink
```

Output:

```text
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=1 correct=1/1 label='round-35 frozen counters (unmodified)' verdict=TARGET_MET
EXIT=0
```

A two-control copy retaining `c1-live` and `c2-live` also returned `controls=2 correct=2/2 verdict=TARGET_MET`, exit 0. Verdict: **both reached 100%; the one-control case proves the count is self-referential.**

### Frozen baseline (comparison)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/check-counter-discrimination.py --profile r35 \
  --manifest .ufo/waves/round-36/controls/manifest.json --no-receipts \
  --mutants /tmp/mado-critmanifestbalance/mut-baseline
```

Output:

```text
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=14/25 label='round-35 frozen counters (unmodified)' verdict=TARGET_MISSED
EXIT=1
```

This matches the frozen before receipt (`.ufo/waves/round-36/receipts/before-discrimination.txt:36`, `correct=14/25`). Verdict: **not 25/25**.

## Inverse instruments — kill rule (PASS)

Constructed `always-reject`, `always-accept`, and `always-crash` scripts in `/tmp/mado-critmanifestbalance/deg/`, installed them only in the fake repo `/tmp/mado-critmanifestbalance/fakerepo/.ufo/waves/round-35/{c1,c2}/count.py`, and ran the unchanged 25-control manifest through `--repo /tmp/mado-critmanifestbalance/fakerepo`. The fake repo is a symlink mirror; no production files were replaced.

Commands used:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-counter-discrimination.py \
  --repo /tmp/mado-critmanifestbalance/fakerepo --profile r35 \
  --manifest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-36/controls/manifest.json \
  --no-receipts --mutants /tmp/mado-critmanifestbalance/mut-deg-reject
```

Repeated with `--mutants .../mut-deg-accept` and `.../mut-deg-crash`, replacing both fake-repo counter scripts with the named behavior. Exact quoted result lines:

```text
# always-reject
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MISSED ok=0
control=c1-golden-r36 instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MISSED ok=0
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=TARGET_MISSED ok=0
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=22/25 ... verdict=TARGET_MISSED
EXIT=1

# always-accept
control=c1-donothing instrument=c1 clause=- expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-tip-stale instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MET ok=0
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=3/25 ... verdict=TARGET_MISSED
EXIT=1

# always-crash (exit 2, no verdict)
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=ERROR ok=0
control=c1-donothing instrument=c1 clause=- expected=TARGET_MISSED observed=ERROR ok=0
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=ERROR ok=0
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=0/25 ... verdict=TARGET_MISSED
EXIT=1
```

The exact controls killing each degenerate behavior are: always-reject — all three accepts (`c1-live`, `c1-golden-r36`, `c2-live`); always-accept — all 22 reject controls; crash — all 25 (observed `ERROR`). Verdict: **kill rule passes** for the frozen 25-control manifest.

## Additional attempted path: verdict-token prefix (FAIL to reach target)

Placed a fake script in each fake-repo instrument path that prints `verdict=TARGET_MET` then `verdict=TARGET_MISSED` and exits 0. A one-control direct launch confirmed both lines are emitted; the gate's regex selects the first occurrence (`observed=TARGET_MET`). But because this one behavior falsely returns MET for reject controls, the full set produced `0/25`, exit 1. Verdict: **first-token parser weakness observed, but this attack did not reach 25/25** and is not needed for the primary counterexample.

## Affected axis and smallest safe correction

- **Calibration (C1):** the 25-control discrimination gate can report `TARGET_MET` for the unmodified r35 counters if the manifest is changed. The design of the frozen controls does distinguish the two degenerate instruments (inverse checks above), but the checker does not enforce that it is scoring that frozen set.
- **Smallest correction:** pin/verify the manifest bytes against a digest (or frozen commit blob ID) before reading controls, and reject unexpected total/control-ID/expectation sets. Keep `--manifest` only if its resolved bytes are verified against that frozen identity. This preserves the existing controls and makes the check fail closed under edited copies.

Evidence paths: the frozen manifest is `.ufo/waves/round-36/controls/manifest.json`; the before receipt is `.ufo/waves/round-36/receipts/before-discrimination.txt`; checker argument resolution and count comparison are in `quality/check-counter-discrimination.py` (manifest load and `correct == total`). No production file changed.