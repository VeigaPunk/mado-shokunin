# ScribeReg27D6 — round-27 C2 measurement erratum audit

## Axes
- **D6 accuracy:** preserve the two measurements, their revisions, and the repair path.
- **Non-interference:** leave D2/D3 unchanged.

## Finding
`.ufo/waves/round-27/registration.md:174-182` already contains `## Round-27 measurement erratum (round 28)` and all four D6 literals (`round-27 measurement erratum`, `measurement 1`, `measurement 2`, `repair flow`). This section was present in the worktree before this seat acted. Its claims match the receipts and repair reports below, so I did not append a duplicate or edit the registration.

The section records:

- Measurement 1 at REV `48b9434a0b0619b3896c9d80e8288ec2226c9ed8`: `h_killed=12/18`, `h_need=14`, `verdict=TARGET_MISSED`, exit 1 (`.ufo/waves/round-27/evidence/c2-after-48b9434a.txt:1,64-65`).
- Repair flow: repair seats ExecRepairA1 and ExecRepairA2 produced candidates; RevRepair audited them and recommended A1 with A2 as fallback; the next measured candidate was ExecRepairA2's (`aa0e14d160b8429b945f12329e5673a1d484986d1b617a05920a92e77a1d4898`). Provenance: `.ufo/waves/round-27/w4/reports/ExecRepairA1.md:4-14,117-121`, `ExecRepairA2.md:1-15`, and `RevRepair.md:112-179`.
- Measurement 2 at REV `0b53bd861104cb8319c698ce622d1b81d3fc66e9`: `h_killed=15/18`, `h_need=14`, `verdict=TARGET_MET`, exit 0 (`.ufo/waves/round-27/evidence/c2-after-0b53bd86.txt:1,64-65`).
- What the original text implied instead: the round-27 C2 data rule says the first returned suites receive “one measurement” and does not record a failed measurement or repair/re-measurement (`.ufo/waves/round-27/registration.md:70-73`; erratum explanation at `:182`). Read literally, it implies a single measurement.

Both measurement revisions were verified read-only in git:

```text
git rev-parse --verify 48b9434a0b0619b3896c9d80e8288ec2226c9ed8^{commit} && git rev-parse --verify 0b53bd861104cb8319c698ce622d1b81d3fc66e9^{commit} && git rev-parse --verify HEAD
48b9434a0b0619b3896c9d80e8288ec2226c9ed8
0b53bd861104cb8319c698ce622d1b81d3fc66e9
4f610066efd90804b055c42ae20c41a7f44404f9
```

## Scratch-clone verification
The registration candidate was copied into an isolated clone at `/fast/scratch/hyaku/mado-r28/scribe-reg27d6-check`, then committed only in that clone so the counter's `git show REV:path` reads the copied bytes. The scratch setup command completed successfully:

```text
test ! -e /fast/scratch/hyaku/mado-r28/scribe-reg27d6-check && git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r28/scribe-reg27d6-check && cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/registration.md /fast/scratch/hyaku/mado-r28/scribe-reg27d6-check/.ufo/waves/round-27/registration.md && git -C /fast/scratch/hyaku/mado-r28/scribe-reg27d6-check add -- .ufo/waves/round-27/registration.md && git -C /fast/scratch/hyaku/mado-r28/scribe-reg27d6-check -c user.name='Mado D6 scratch verification' -c user.email='mado-d6-scratch@example.invalid' commit --quiet -m 'Scratch verify round-27 measurement erratum'
```

Counter predicate location: `.ufo/waves/round-28/c2/count.py:161-166`. The exact D6 output on the copied candidate was:

```text
python3 -I .ufo/waves/round-28/c2/count.py HEAD
counter c2-r28 sha256:c0415c9a441b3263adf68129ee4d4eb4c122588c58c11de7802df89901540ba7 rev=5f56a653f9ced4bf4544e9e9ab5634e1696b5886
CHECK D6         PASS | both-measurements=True repair-flow=True
PRED-C2-r28 verdict=TARGET_MISSED
exit=1
```

For non-interference, I ran the same counter at the clone's base revision (`python3 -I .ufo/waves/round-28/c2/count.py HEAD^`, REV `4f610066efd90804b055c42ae20c41a7f44404f9`). Before the copy, D2 and D3 were both `FAIL`; after the copy, they remained `FAIL` with identical details:

```text
CHECK D2         FAIL | erratum=False rows=5/5
CHECK D3         FAIL | red-fixture=False census-sha=3fb7261569f4 red/green=False
```

Thus D2/D3 are unchanged by the registration-only copy. The complete C2 counter still returns `TARGET_MISSED`; this report claims only D6 PASS and D2/D3 non-interference, not a full-counter pass. Both scratch runs were isolated from the live lane.

## Touched surfaces, gates, and limits
- **Lane write:** this report only: `.ufo/waves/round-28/w1/reports/ScribeReg27D6.md`.
- **Registration:** pre-existing section at `.ufo/waves/round-27/registration.md:174-182` verified; no duplicate or further edit made.
- **Out of scope:** no counter or other lane file changed; no held-out directory or seal contents read; no lane commit; no network access; no tools installed or updated.
- **Known limit:** D2/D3 remain failing in the isolated clone at both compared revisions; their inputs were not part of this item's registration-only change.
