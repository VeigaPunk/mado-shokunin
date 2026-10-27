# R54W2Seat13 — C1 manifest filename and resolution falsification

## Axes

Operability (honest-tree acceptance in a clone); coverage (the checker reads only the frozen C1 evidence, not a neighboring round's manifest).

## Attack and result

**Attack:** confuse the filename promised for the round-52 digest manifest, or use a broad glob that can select the round-54 manifest. The exact C1 contract requires the four round-52 pins and round-52 recorded digests (`claims-frozen.md:22-30`); the `--repo/--rev` contract says all inputs come from those git objects (`registration.md:36-38`). The exact frozen inventory is `registration.md:10-19`, especially the purported source filename at `:11-12` and the four literal pin basenames at `:14-19`.

The round-52 manifest is named `SHA256SUMS`, not `SHA256SUMS.txt`. The relevant wave-1 evidence, **R54Seat14.md:60-63**, reports that discrepancy and the concrete glob risk: a wildcard across rounds can pick `.ufo/waves/round-54/fetch/SHA256SUMS.txt`, which is not C1 evidence. Independently, **R54Seat01.md:287-296** records that the `SHA256SUMS` naming discrepancy is round-specific and recommends basenames because round-52 manifest entries are absolute lane paths; **R54Seat03.md:264-285** records the exact committed path and states that a literal `.txt` lookup has no object at base. Those are w1 report claims, not results freshly executed by this seat.

The smallest safe resolution is to read the exact path `.ufo/waves/round-52/fetch/SHA256SUMS` at the scored revision and select records by the four exact frozen basenames, while comparing the recorded value to the frozen digest literals and hashing pin bytes from the scored revision. Do not glob over `SHA256SUMS*` or both round directories. This avoids a false miss from the bad suffix in registration and avoids cross-round substitution. A basename-keyed parse alone is not sufficient if duplicate rows with the same basename are silently overwritten; require an unambiguous expected record (or reject duplicate expected basenames) so the manifest cannot choose between conflicting identities.

**Counter verification: NOT RUN / absent.** The current counter directory listing did not show `c1-r54-errata-truth.py`; frozen baseline absence is also recorded at `claims-frozen.md:32-33`. No runnable pinned command for the counter was available, so no counter output or exit status is claimed. No isolated fixture was needed to establish the filename collision; no claim is made about a landed implementation's behavior.

## Evidence / exact tool calls

- `read skill://godspeed` → skill instructions; no exit code is exposed by the read tool.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/claims-frozen.md` → lines 1-97, including C1 predicate `:19-44`; no exit code is exposed.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/registration.md` → lines 1-117, including C1 pins/controls `:8-53`; no exit code is exposed.
- `read .../.ufo/waves/round-54/w1/R54Seat14.md` and `read .../w1/R54Seat01.md`, `read .../w1/R54Seat03.md` via the w1 search results → filename/glob and absolute-path observations cited above; no exit code is exposed.
- `read .../quality/counters/` → listing did not include a C1 r54 counter; no exit code is exposed.
- `mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat13 && test -d /fast/scratch/hyaku/mado-r54/R54W2Seat13` → exit 0.

No pinned counter command run. No repo fixture, git/jj mutation, host read, or tool install.

**Trailer:** `.ufo/waves/round-54/w2/R54W2Seat13.md` relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat13` removed before yield; no scratch remains.
