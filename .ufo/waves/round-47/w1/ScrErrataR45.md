# ScrErrataR45 — R4b: errata for the round-45 entry's six non-supported sentence units

Seat: ScrErrataR45, round-47 w1 (lane `mado-shokunin`, base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`).
Target: `corpus/knowledge/hyprland-monitor-rule-r45.md` as landed at `4d22eeb`
(`sha256 128df1bd1055fcbb09f611c48286cd013e9d8bade992f4c17e81ba0615bb9c7b`, still the lane's version).
Input: `.ufo/waves/round-46/w1/CritW2Entry.md` (F1-F4 = six sentence units at lines 18, 84, 96, 98, 106, 107).

## Verdict over the six units

| unit | CritW2Entry finding | verdict | what the pins decide |
|---|---|---|---|
| `entry:84` | F1 mis-located veto | CONFIRMED, citation corrected | `:264` is the already-enabled path that returns at `:271` before the emit; the veto is `:275-287`, the emit `:389` reached via `m_enabled = true;` (`:302`), default `m_enabled = false` (`Monitor.hpp:357` @ efb5099) |
| `entry:96` | F2 false provenance | CONFIRMED, citation replaced | cited `live-monitors-host-l1.txt` is a run of `l1-draft/mado-monitors.py` (`# tool sha256 c6ac5fc2…`); the landed tool at `4d22eeb` is `2f007417…` and `live-monitors-host-r45.txt` prints the same AGREE/OK/exit 0 |
| `entry:98` | F3 wrong (INF) | CONFIRMED, claim corrected | 3440/1440 exact + \|99.997-100.000\| = 0.003 < 1 Hz: all three negated `DELTALESSTHAN` bounds at `:836-837` pass, so the custom-mode push at `:838-839` cannot execute; branch is determined |
| `entry:18` | F4 unpinned | CONFIRMED, pin supplied | commit `a9902ea65f461…` dated 2026-07-22T16:35:10Z, "config: remove legacy config support (#15539)", removes `src/config/legacy/ConfigManager.cpp` (2184 deletions) and the `Legacy`/`CONFIG_LEGACY` selection; raw file 404s |
| `entry:106` | F4 unpinned | CONFIRMED **and stronger**: the wording is false at aquamarine v0.15.1 | Wayland.cpp / Headless.cpp / Output.cpp contain 0 occurrences of `description`; `name, description, make, model, serial` are default-empty (`Output.hpp:258`); only `DRM.cpp:2101` sets one — non-DRM outputs get an empty description, not a different one |
| `entry:107` | F4 unpinned | CONFIRMED, pin + scope | same commit removes the file holding the `monitor` keyword handler; monitor rules survive as Lua fields (`LuaBindingsConfigRules.cpp:80`, `MONITOR_FIELDS[]`) driven at `ConfigManager.cpp:809-810` |

No finding was REFUTED; none had to be.

## Work performed (commands and outcomes)

1. Read `CritW2Entry.md` and the entry; located all six units with `grep -n` (verify.py asserts the line numbers).
2. Compared the two round-45 receipts and their tool hashes; hashed the landed tool at `4d22eeb`, at base
   `60edb66e`, and on disk -> all `2f007417…`; hashed `.ufo/waves/round-45/l1-draft/mado-monitors.py` ->
   `c6ac5fc2…` (matches the l1 receipt's `# tool sha256`).
3. Cross-checked the fourteen round-45 pins against `.ufo/waves/round-45/receipts/fetch-sha256.txt` ->
   14/14 OK (`receipts/pin-manifest-check.txt`).
4. Fetched and pins into the seat dir: Hyprland commit `a9902ea` JSON + `src/config/ConfigManager.cpp` +
   `src/config/lua/ConfigManager.cpp` + `src/config/lua/bindings/LuaBindingsConfigRules.cpp` +
   `src/output/Monitor.hpp` @ `efb5099`; aquamarine v0.15.1 `src/backend/{Wayland,Headless}.cpp`,
   `src/backend/drm/DRM.cpp`, `src/output/Output.cpp`, `include/aquamarine/output/Output.hpp`, tree listing
   (`receipts/PINS.md` records URL + sha256). The re-fetched `DRM.cpp` is byte-identical to the round-45 pin
   (`ff9b19d8…`), which is the provenance check on the non-DRM files' sibling.
5. Probed the `recheck:` line's `90d` shorthand: `GET /repos/hyprwm/Hyprland/commits/90d` -> 422
   "No commit found for SHA: 90d"; a full sha -> 200 (`receipts/90d-probe.txt`).
6. Re-verified every locator in the draft errata with `verify.py` -> `RESULT: mismatches=0`
   (`receipts/verify-locators.txt`), including negative assertions (no `description` in the two non-DRM
   backends, no `Legacy` in main's ConfigManager.cpp).

## Gates and safety

- No tracked file touched: `git status --porcelain` on the entry, `tools/mado-monitors.py` and
  `.ufo/waves/round-45/` is empty. The errata are drafted, not applied — the L1 integrates.
- No package manager, no installs, no host-service change, no compositor command of any kind (no `hyprctl`
  call was needed), no terminal/GUI launch, no `xdg-terminal-exec` invocation.
- Network use: read-only GitHub raw/API fetches for the pins above; nothing published.
- Scratch `/fast/scratch/hyaku/mado-r47/ScrErrataR45/` held the fetch staging and was deleted after the pins
  were copied into the seat dir; the only `/tmp` file (`seat90d.txt`, ~100 bytes) was removed in the same
  command that created it.
- Session material: none captured; the only quoted paths are repo-relative.

## Touched surfaces

- `.ufo/waves/round-47/w1/ScrErrataR45/` (this seat): `errata.md`, `verify.py`, `pins/` (16 files),
  `receipts/{verify-locators.txt,pin-manifest-check.txt,PINS.md,90d-probe.txt}`.
- `.ufo/waves/round-47/w1/ScrErrataR45.md` (this report).
- Nothing else in the lane; nothing outside the lane.

## Out of scope / handed back

- Integrating the append blocks into `corpus/knowledge/hyprland-monitor-rule-r45.md` and assigning the SOURCES
  row owed for E4/E6 (C2 of this wave opens S326.. for a different subject — the L1 picks the number).
- The other round-46 closure items R1-R4a (other seats).

## Extra observations (beyond F1-F4)

- **S1** `entry:18`'s `(or 90d at the latest)` is not a resolvable revision and cannot be acted on as written.
- **S2** F4's third unit is a stronger defect than "unpinned": the words are false at the pinned aquamarine
  version, so the fix is a replacement, not a citation.
- **S3** The entry is unchanged since `4d22eeb`, so the errata apply to the landed text.

## Limits

- Source reading only, at Hyprland `efb5099`/`a9902ea` and aquamarine/hyprutils `v0.15.1`/`v0.14.2`; no Hyprland
  build, no config change, no compositor experiment (a Wayland- or headless-backed output was never observed on
  this host — the E5 correction rests on the backend sources and the shared field declaration).
- The `monitor.added` emit count is over the fourteen round-45 pins plus the files pinned here, not over the whole
  upstream tree.
- E3's counterfactual (a pushed custom mode would set 100.000) is read from `:903`; it was not exercised.

## Artifact paths (relative to `mado-shokunin/`)

- Errata (the deliverable): `.ufo/waves/round-47/w1/ScrErrataR45/errata.md`
- Locator receipt: `.ufo/waves/round-47/w1/ScrErrataR45/receipts/verify-locators.txt`
- Pin manifest check: `.ufo/waves/round-47/w1/ScrErrataR45/receipts/pin-manifest-check.txt`
- Pin provenance (URL + sha256): `.ufo/waves/round-47/w1/ScrErrataR45/receipts/PINS.md`
- `90d` probe: `.ufo/waves/round-47/w1/ScrErrataR45/receipts/90d-probe.txt`
- Verification script: `.ufo/waves/round-47/w1/ScrErrataR45/verify.py`
- Pins: `.ufo/waves/round-47/w1/ScrErrataR45/pins/`
