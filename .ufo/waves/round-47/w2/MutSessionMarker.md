# MutSessionMarker — round-47 w2 R3: mutation-probing the session-material marker gate

Seat: `MutSessionMarker` (leaf, no subagents, no background jobs). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Measured on scratch clones of the lane at base **`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`** (the R3 draft's own
measured frame; w1 receipt 02 parity re-checked, below). Nothing in the lane was written outside
`.ufo/waves/round-47/w2/MutSessionMarker/` and this report; all clones and work trees lived under
`/fast/scratch/hyaku/mado-r47/MutSessionMarker/` and were deleted before this seat finished.

Target: the drafted R3 gate `.ufo/waves/round-47/w1/ExecSessionMarker/check-session-material.py` (sha256
`a4a0a084e745f511048d5be445bed4959a18b5d64798a55da06c74cc0d08e9c9` — matches the w1 report §1). The probe:
install a planted battery of real-shaped session material and run the same bounded detector on pristine, mutated
and restored bytes.

## 1. Method

- `probe/build-clone.sh` clones the lane (`git clone -q --shared --no-checkout`, toplevel guard `git rev-parse
  --show-toplevel` = clone dir, scratch identity commits only) and commits five states:
  | state | commit contents |
  |---|---|
  | S0 | base `60edb66`, gate only, no markers (cross-check anchor) |
  | S1 | three unmarked planted files: client dump, proc table, monitor dump |
  | S2a | + sidecar + registry row for the round-45 `C00_shipped/mons.json` fixture (clean waiver) |
  | S2b | + a fabricated monitor object appended inside that registered fixture (tamper) |
  | S34 | + `fixtures/real-content.json` (real-shaped client+proc+monitor, valid sidecar + registry row, kind=fixture) and `fixtures/not-a-gate-copy.json` (client dump marked kind=gate-copy) |
  | S5 | + `fixtures/prose-serial.md` (serial-shaped token, valid sidecar that cannot name R5) |
  Every identity value is FABRICATED for this probe (no hyprctl, no host data); values are assembled from
  concatenated parts in `probe/make-plants.py` so the generator's own bytes never carry a matchable token.
- `probe/detector.py` runs `python3 -I <gate> --repo <clone> --rev <state>` per state and asserts: exit 1,
  the planted FINDING lines, and the exact named WAIVER_REJECTED reasons. The gate's own selftest runs first.

## 2. Pristine battery (the claim holds)

Selftest: **`SELFTEST: passed=63/63 failed=0`** (receipt `01-selftest.txt`), exit 0.

| state | result | key lines (receipt `raw/<state>.txt`) |
|---|---|---|
| S0 | PASS | `SESSION_MATERIAL: files=18371 findings=136`, `R1_CLIENT_DUMP=29 R2_PROC_TABLE=31 R3_MONITOR_IDENT=53 R4_HOME_LISTING=2 R5_SERIAL_PROSE=21` — equals w1 receipt 02's frame |
| S1 | PASS | planted client dump R1 count=2, proc table R2 count=2, monitor dump R3 count=1 all kept; `files=18374 findings=139`; no waiver lines |
| S2a | PASS | `WAIVER file=…/C00_shipped/mons.json rule=R3_MONITOR_IDENT kind=fixture`, `SESSION_MATERIAL_WAIVED: findings=1 files=1`, `files=18375 findings=138` |
| S2b | PASS | `WAIVER_REJECTED … rule=R3_MONITOR_IDENT reason=sha-mismatch`, tampered R3 finding returns count=2, `files=18375 findings=139` |
| S34 | PASS | three `value-not-synthetic:title-not-synthetic` / `program-not-synthetic` / `serial-not-synthetic` rejections on real-content.json, `gate-source-mismatch` on the non-gate file, all four findings kept, `files=18379 findings=143` |
| S5 | PASS | `WAIVER_REJECTED … rule=R5_SERIAL_PROSE reason=serial-rule-not-waivable`, R5 finding kept count=1, `files=18381 findings=144` |

So the four named cases each exit 1 with the real material kept: unmarked (S1), marked/tampered (S2b),
registry-named file with real content (S34, valid sidecar + row), and a marked non-synthetic file (S34,
kind=gate-copy). The gate's "fails both ways" property reproduces on this tree.

## 3. Mutations (both killed)

Both mutations applied to isolated scratch copies of the gate only (`probe/gates/gate-m1.py`, `gate-m2.py`),
then restored byte-exactly.

- **M1 — accept any marked file** (waive any finding whose path has a sidecar, before any verification; 2
  lines inserted in `apply_waivers()`). Detector on the planted battery (receipt `03-mutant-M1.txt`):
  **DETECTOR FAIL passed=1 failed=3** — S2b fails (tampered wafer waived), S34 fails (real content waived),
  S5 fails (the prose serial is waived — the serial band is gone). Only S2a (clean waiver) still passes, as it
  must. Killed.
- **M2 — skip R3 in marked files** (don't emit R3 findings for paths that have a sidecar; 3 lines in `run()`).
  Detector (receipt `04-mutant-M2.txt`): **DETECTOR FAIL passed=1 failed=4** — S2a fails (nothing left to
  waive), S2b fails (no rejection, no finding), S34 fails (R3 rejection+finding gone), S5 fails (summary drops
  by the two marked R3 findings). S1 (unmarked R3) still passes. Killed.

No mutant survived: the planted battery has teeth for both named marker-logic weakenings. Before/after hashes:
pristine `a4a0a084…` (sha256) / `7f9dec84…` (md5) equal on the restored files (receipt `00-gate-pristine-sha.txt`
records the hash before and after); re-running the detector on the restored bytes reproduces the pristine output
byte-for-byte (receipt `05-restored-parity.txt` + `raw/restored-*` vs `raw/S2b-*`/`raw/S34-*`, identical).

## 4. Verdict

No hole found in the R3 draft within this battery: the four real-material plants are all kept with named
reasons, and the two targeted mutations are both caught. This is the receipt the routed R3 item asks w2 to
produce — the marker gate stands the falsify probe on the planted states.

Pinned (not re-probed): the declared w1 residuals — a retitled `redacted` title escape for R1 (W4b's namespace
is the title), and R5/R6's shape-only class — are outside the marker logic's waiver surface by design and were
not challenged here beyond S5 (which re-confirms the serial band refuses a marked file).

## 5. Tooling and hygiene

No installs, no pacman (host-wide pause respected), no compositor access, no terminal, no xdg-terminal-exec, no
host cache writes. Python 3.14.8 stdlib + git only. All receipts are the gate's own stdout (`probe/verify-claims.py`
asserts every number above against them: `CLAIMS_CHECK passed`, receipt `06-claims-check.txt`). Scratch deleted;
no receipt cites a scratch or `/tmp` path as evidence.

## 6. Repro

```sh
SEAT=…/mado-shokunin/.ufo/waves/round-47/w2/MutSessionMarker
S=/fast/scratch/hyaku/mado-r47/MutSessionMarker        # (deleted after runs)
bash "$SEAT/probe/build-clone.sh"                       # clone at 60edb66 + 5 state commits
python3 -I "$SEAT/probe/detector.py" --gate "$S/gate-pristine.py" --clone "$S/clone" \
  --manifest "$S/manifest.json" --out-dir "$S/out"
python3 -I "$SEAT/probe/detector.py" --gate "$SEAT/probe/gates/gate-m1.py" --clone "$S/clone" \
  --manifest "$S/manifest.json" --out-dir "$S/out-m1" --states S2a-cleanwaive,S2b-tampered,S34-realcontent,S5-proseserial
python3 -I "$SEAT/probe/detector.py" --gate "$SEAT/probe/gates/gate-m2.py" --clone "$S/clone" \
  --manifest "$S/manifest.json" --out-dir "$S/out-m2" --states S1-unmarked,S2a-cleanwaive,S2b-tampered,S34-realcontent,S5-proseserial
cp "$S/gate-pristine.py" "$SEAT/probe/gates/gate-m1.py"; cp "$S/gate-pristine.py" "$SEAT/probe/gates/gate-m2.py"
sha256sum "$SEAT/probe/gates/gate-*"                    # all three equal a4a0a084…
python3 -I "$SEAT/probe/verify-claims.py" "$SEAT"
```
