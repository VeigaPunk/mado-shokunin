# R55ScribeSources — round 55 wave w1 (draft; L1 integrates)

Scope: draft the registry rows S378, S379, S380 for the C1 keyboard repeat/numlock entry; write the lesson Gate block; write the row-check script and receipts; write a search-log note; check the three URLs against the registry. Pins were re-opened from `.ufo/waves/round-55/fetch/`; the contract was read from `claims-frozen.md`, `registration.md` and `frozen-tables.json`, and nothing was reinterpreted.

## Result

- Rows drafted, 11 columns (NF=13 under awk -F'|'): S378 `src/managers/SeatManager.cpp`, S379 `src/protocols/core/Seat.cpp`, S380 `src/devices/IKeyboard.hpp`. All tier A, kind code, status mined, opened 2026-10-28, recheck on-release, used-by `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`.
- Gate block: one entry per row (URL, access date 2026-10-28, quote ≤25 words with `file:line`, teaches sentence). Every quote is a byte substring of its pin line; every teaches sentence equals its row's teaches cell.
- Frozen C1 quotes K10, K11, K12 and K18 are byte-identical substrings of their pin lines and fall inside the new rows' anchor ranges.
- Verifier: `VERDICT OK`, exit 0. A one-space mutation of the S380 gate quote is caught (`FAIL(1)`, exit 1).
- Registry check: two of the three URLs are absent. **S380's URL already exists** as S363 (duplicate-URL W04 warning; see defects).
- No tracked file was edited; no git or jj mutation; no host read beyond the committed pins; no hyprctl call; no subagent, no installs.

## Deliverables

- `.ufo/waves/round-55/w1/R55ScribeSources/rows.md` — the three draft rows (paste-ready for `corpus/SOURCES.md` after S377, L1 to integrate).
- `.ufo/waves/round-55/w1/R55ScribeSources/gate.md` — Gate block text for S378–S380.
- `.ufo/waves/round-55/w1/R55ScribeSources/search-log.md` — round 55 search-log note (question, where searched, identified/screened/included/excluded, stop rationale).
- `.ufo/waves/round-55/w1/R55ScribeSources/verify-r55-seat-sources.py` — row/quote verifier (`python3 -I`; writes nothing; `--work` accepted but unused because no temp file is created).
- `.ufo/waves/round-55/w1/R55ScribeSources/receipts/verify-rows-gate.txt`, `verify-mutant-gate.txt`, `validate-baseline.tsv`, `validate-candidate.tsv`, `SOURCES.candidate-rows-inserted.md`.
- This report: `.ufo/waves/round-55/w1/R55ScribeSources.md`.

## Commands and decisive output

1. Pin hashes, from the fetch dir (`sha256sum -c SHA256SUMS.txt`):
   - `Hyprland-SeatManager.cpp: OK`, `Hyprland-protocols-core-Seat.cpp: OK`, `Hyprland-IKeyboard.hpp: OK` (all 10 pins OK).
   - Read-only `git show 54dacbd…:.ufo/waves/round-55/fetch/<pin> | sha256sum` gives the same digests as the working-tree pins for the three seat pins (`bd7485…8`, `cc23bb…8`, `82e0bc…f05`).
2. Anchor lines, from the pins:
   - `Hyprland-SeatManager.cpp` 175 `void CSeatManager::updateActiveKeyboardData() {`, 176 `if (m_keyboard)`, 177 `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);`, 178 `PROTO::seat->updateKeymap();`.
   - `Hyprland-protocols-core-Seat.cpp` 441 `void CWLKeyboardResource::repeatInfo(uint32_t rate, uint32_t delayMs) {`, 442 `if (!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs))`, 447 `m_resource->sendRepeatInfo(rate, delayMs);`, 603 `void CWLSeatProtocol::updateRepeatInfo(...)`, 604 keyboard-capability gate, 608 `k->repeatInfo(rate, delayMs);`.
   - `Hyprland-IKeyboard.hpp` 121 `int m_repeatRate = 0;`, 122 `int m_repeatDelay = 0;`, 123 `int m_numlockOn = -1;`.
3. Verifier, `python3 -I verify-r55-seat-sources.py --lane … --seat-dir … --work …`:
   ```
   ok pin_sha Hyprland-SeatManager.cpp bd7485…
   awk rows (NR NF): 1 13 ; 2 13 ; 3 13
   ok quote S378 Hyprland-SeatManager.cpp:177 words=2 len=83
   ok quote S379 Hyprland-protocols-core-Seat.cpp:442 words=14 len=94
   ok quote S380 Hyprland-IKeyboard.hpp:121 words=3 len=24
   ok frozen K10 … / K11 … / K12 … / K18 …
   VERDICT OK   (rc=0)
   ```
   Mutant (`m_repeatRate        = 0;` → 7 spaces in gate.md): `VERDICT FAIL(1)`, rc=1.
   An earlier run failed `gate teaches != row teaches cell` for all three rows (teaches wording and a trailing period differed). Fixed by making gate.md teaches sentences equal the row cells; the receipt is the post-fix run.
4. Registry (`corpus/SOURCES.md`) URL grep, exact URL suffix with the frozen commit:
   ```
   src/managers/SeatManager.cpp 0
   src/protocols/core/Seat.cpp 0
   src/devices/IKeyboard.hpp 1
   312:| S363 | Hyprland 0.56.2 keyboard modifier bits and bind states - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.hpp | code | A | …
   ```
5. Census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <lane> --file <registry> mado`):
   - Baseline (unmodified registry): rc=0, 25 W04 warnings, no E-codes.
   - Candidate (rows inserted after S377 in a scratch copy, scratch corpus mirror): rc=1; W04 count 26 (new: S380 duplicate URL with S363 across scopes); E11 entries for S378, S379, S380 (used-by knowledge entry not yet on disk) and for other rows only because the scratch mirror holds just `corpus/knowledge` and `corpus/lessons`. The E11 mirror artifacts are my test setup, not a registry defect; the rows' own E11 is expected until the entry is written.

## Defects, ambiguities and inputs that show them

- **W04 duplicate URL (S380 vs S363).** `src/devices/IKeyboard.hpp` at `efb50993…` is already S363's URL (scope: modifier bits and bind states). The registration names S380 with this URL; the census flags it only as W04 (warning, does not change status) because the scope differs. L1 should confirm that a second row on the same URL is intended, or cite S363 instead.
- **Shape source.** `corpus/CORPUS.md` is at the fleet root, not in the lane (`mado-shokunin/corpus/` has SOURCES.md only). The 11-column header is identical in `/home/vgpnk/Projects/shokunin/CORPUS.md:86` and the lane `corpus/SOURCES.md:11`, so I used that shape.
- **`teaches` wording.** S378's teaches cell ends with "no host event asserted", a disclaimer rather than a learner benefit (CORPUS rule: one grounded benefit). Kept because the frozen contract's scope note needs it; L1 may trim it, which requires changing gate.md to match.
- **Registration §C1 "pins fetched … from the tag-pinned commit"** versus the pins' file names (`Hyprland-<path with dashes>`): mapping used `frozen-tables.json` `source_suffix`; no inconsistency found.
- **Verifier limit (declared).** It proves quote identity at an exact pin line and that teaches equals the row; it does not prove entailment of the teaches sentence by its quote. That is the sentence-to-pin audit, not this seat's claim.
- **Census harm watch.** `scripts/sources-census.sh validate` will return exit 1 at integration until `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` exists (E11 for S378–S380). The frozen harm-watch line ("stays exit 0") is therefore a post-integration check, not something this draft can satisfy.
- **Lane HEAD.** `git rev-parse HEAD` in the lane printed `dbc2eefe…`, not the freeze commit `54dacbd…`. I did not investigate the lineage; the pin hashes were checked at `54dacbd…` directly.

## Not verified / not run

- Gate quotes were checked against the pins, not re-opened from the live URL (the seat had no network fetch step; the pins are the frozen source the registration names).
- No entailment check of the teaches sentences beyond the quote lines (see verifier limit).
- The C1 entry, counter `c1-r55-kbd-entry.py` and the harness were not run (not in this seat's scope).
- No hold-out path was touched or looked for.

## Tooling

No tool was installed, upgraded or removed. `~/.local/bin` and PATH were not touched. `/home/vgpnk/.omp/agent/RULES.md` was not read because no install was needed.

## Scratch

`/fast/scratch/hyaku/mado-r55/R55ScribeSources/` was removed on exit (trap); receipts were copied into the deliverable directory first.
