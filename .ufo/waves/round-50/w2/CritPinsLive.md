# CritPinsLive — w2 FALSIFY attack on PRED-C1-r50 clause f/r (pin/receipt freshness + receipt name pin)

Seat: CritPinsLive (leaf). Attack rev: `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip).
Data commit: `906178b607f2071af7c2efec5aad976a8bfa5757`. Round-49 base: `8ae47b957034ae21012bbf09173cca2c48be345e`.
Method: read-only `git cat-file`/`git show` in the lane; all counter runs against a `git clone -q --shared` of the lane in
`/fast/scratch/hyaku/mado-r50/CritPinsLive/clone` with `TMPDIR` there. No tracked file edited, no lane/fleet mutation, no
host-state write; live compositor read-only (`hyprctl binds -j`, `hyprctl devices -j`, `hyprctl getoption`).

## Verdict

**No defect that the frozen counter can be scored against; one latent cosmetic defect in the fetch manifest (self-line).**
All five assigned checks (a-e) pass except the manifest self-referential line, which is unverifiable by construction and
does not feed PRED-C1-r50.

## (a) fetch/SHA256SUMS vs recomputed tree hashes — 15/15 substantive entries exact; self-line FAILED

`git cat-file blob b4a79843:.ufo/waves/round-50/fetch/SHA256SUMS` lists 16 entries. Recomputing sha256 over each blob in
the tree at the attack rev and diffing (self-line excluded) is clean: all 15 substantive entries match exactly
(`receipts/fetch-SHA256SUMS-at-b4a79843.txt` vs `receipts/fetch-SHA256SUMS-recomputed.txt`), including
`9f16e5a5…1590  binds-live-r50.txt` which equals the registration table value. The 16th entry
(`bb21f728…4d07  SHA256SUMS`) is the manifest hashing itself; it verifies under no convention tested (naive recompute
`e2b91106…`, minus-self-line `fa76b493…`, zeroed-hash `bb1e0a58…`, empty-hash, self-line-first, CRLF — none match), and
`sha256sum -c SHA256SUMS` on an extracted copy reports `SHA256SUMS: FAILED`, 15 OK, rc=1
(`receipts/sha256sum-c-manifest.txt`). The blob is byte-identical at 906178b6, 470bfd77 and b4a79843, so the value is
stable, not drifted. **Impact on the frozen instrument: none** — PRED-C1-r50 never reads the manifest; its trust root is
registry-row digests over `git cat-file` bytes (counter docstring lines 10-20; clause c pins bound by row-recorded
digests), and registration describes the manifest only as "SHA256SUMS in dir; 14 upstream pins byte-equal to round-49".
**Smallest safe correction:** regenerate the manifest without the self-referential line (15 entries) so `sha256sum -c` is
fully green; a fixed-point self-hash is not attainable otherwise.

## (b) 14 upstream pins byte-equal round-49 — PASS

Pairwise sha256 of the 14 upstream files at `8ae47b95:.ufo/waves/round-49/fetch/` vs
`b4a79843:.ufo/waves/round-50/fetch/`: all 14 SAME (`receipts/upstream-pins-r49-vs-r50.txt`). No byte drift across the
round boundary; the re-fetch produced identical ground.

## (c) receipts/binds-live-r50.txt byte-equal fetch pin copy — PASS

`git cat-file` of `.ufo/waves/round-50/receipts/binds-live-r50.txt` vs `.ufo/waves/round-50/fetch/binds-live-r50.txt` at
b4a79843: `cmp` byte-equal, both sha256 `9f16e5a5ce7fe39fc30cd8a6041fcdf733f7b794f20310796bae09d01ae51590` (1768 B), stable
across 906178b6 / 470bfd77 / 8dbbf61a / b4a79843. Matches the registration frozen-artifact table.

## (d) clause r live-capture path — cannot be satisfied by pinned bytes alone; one-digit tamper fails

Code read (`quality/counters/c1-r50-bind-entry.py`): `RECEIPT_NAME = ^binds-live-r50\.txt$` (line 203) pins the receipt
name in clause f and clause r. `clause_r` (line 1123) calls `live_binds()` (line 1068), which executes
`/usr/bin/hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j` in a sandbox (HOME/XDG_* under TMPDIR,
`XDG_RUNTIME_DIR` + `HYPRLAND_INSTANCE_SIGNATURE` required from the live environment) and recomputes the raw-JSON digest,
total, form counts and resolve value from the socket. The receipt's stated values are only the EXPECTED side of the
comparison — no code path feeds receipt bytes into the live digest, so pinned bytes alone cannot satisfy clause r.

Empirical (clone of the lane in scratch; baseline at b4a79843 → TARGET_MET rc=0, clause r `replay=ok sha=9a47199e2297
binds=192 resolve=0`):
- receipt sha256 digit `…99e2…`→`…99f2…` (rev 34323ff4…): `clause=f entry_disagrees sha=0`, `clause=r replay_mismatch
  sha=9a47199e2297/9a47199f2297` → `f:0 r:0 TARGET_MISSED` rc=1
  (`receipts/tamper-digest-digit.txt`).
- receipt total `binds=192`→`193` (rev 277a7566…): `clause=f receipt_forms_sum …!=193`, `clause=r replay_mismatch
  total=192/193` → `f:0 r:0 TARGET_MISSED` rc=1 (`receipts/tamper-total-digit.txt`).

Freshness (clause f `receipt_present_at_base` guard): the receipt does not exist at base 8ae47b95 (`git cat-file -e`
rc=128), so the receipt must be new this round.

## (e) binds-live-r50.txt hygiene — PASS

Shape-only receipt: no home path or account literal (grep `/home/`, `/root/`, account name — zero hits); no raw JSON
(`"modmask"`/`"dispatcher"`/`"keycode"` — zero hits); absolute-path scan hits only repo-relative mentions
(`.ufo/waves/round-50/w1/ExecLiveR50/make-receipt.py` generator note, `code:/mouse/switch:` key-form prose); `efb50993…` is
the Hyprland **source** commit (the registry-pinned ref), not the live instance signature (which carries the
`_1793027319_436109330` suffix — absent from the file); all 28 device names/addresses from read-only `hyprctl devices -j`
cross-checked against the receipt — zero hits; no title-like fields. The file's own attestation line ("no device name,
window title, dispatcher argument, bind description or home path appears in this file") holds under these checks.

## Deliverables

- Report: `.ufo/waves/round-50/w2/CritPinsLive.md` (this file).
- `receipts/fetch-SHA256SUMS-at-b4a79843.txt` — manifest bytes at the attack rev.
- `receipts/fetch-SHA256SUMS-recomputed.txt` — sha256 of every fetch blob recomputed from the tree at b4a79843.
- `receipts/sha256sum-c-manifest.txt` — `sha256sum -c` result: 15 OK + self-line FAILED rc=1.
- `receipts/upstream-pins-r49-vs-r50.txt` — 14/14 SAME pairwise hash comparison.
- `receipts/binds-live-r50-at-b4a79843.txt` — receipt bytes at the attack rev (sha256 9f16e5a5…1590).
- `receipts/tamper-digest-digit.txt`, `receipts/tamper-total-digit.txt` — one-digit tamper counter runs (both TARGET_MISSED).

No tool installed. Scratch dir `/fast/scratch/hyaku/mado-r50/CritPinsLive` deleted after receipts were copied here.
