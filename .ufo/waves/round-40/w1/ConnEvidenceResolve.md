# ConnEvidenceResolve — round 40 evidence-pointer resolution

Seat: `ConnEvidenceResolve` (w1, 64 seats). Task: list every evidence pointer cited by the
round-40 registration and the C1/C2 counter docstrings (paths, commits, line numbers, URLs) and
check each resolves at the freeze commit **5e7e88525cc539563de7746361b2650802e81809**
(`git cat-file -e` for lane blobs, file:line existence for source ranges, HTTP HEAD for URLs).
All checks were read-only; no tools were installed (record: none, channel n/a, reason n/a —
only existing `git` and `curl -I` used).

## Freeze identity
- Freeze commit `5e7e88525cc539563de7746361b2650802e81809` exists (`git cat-file -e` OK); its
  tree has 11934 paths.
- Base commit `9fc511ddce708327377161202f358ce37dc266ba` exists (`git cat-file -e` OK).

## Internal lane pointers @ freeze (all resolve unless noted)
| Pointer (as cited) | Resolves at 5e7e885? |
|---|---|
| `quality/counters/c1-r40-live.py` | YES (blob present; docstring = PRED-C1-r40-v1) |
| `quality/counters/c2-r40-forms-entry.py` | YES (blob present; PRED-C2-r40-v1) |
| `tools/mado-options.py` | YES (blob present; base blob also present, lacks `--live` — grep: 0 matches, so C1 clause-a precondition holds) |
| `quality/check-axis-scores.py` | YES |
| `quality/check-index.py` | YES |
| `tools/mado-verify.sh` | YES |
| `scripts/sources-census.sh` | NO in lane tree; resolves only as fleet file `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (regular, 35466 B) |
| `corpus/SOURCES.md` | YES (S162 row line 174, S173 row line 185 present) |
| `corpus/README.md` | YES |
| `corpus/lessons/round-39.md` | YES |
| `corpus/lessons/round-40.md` | absent at freeze — post-freeze destination (D2 appended note; C2 counter `LESSON` reads it at REV). Expected. |
| `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` | absent at freeze — C2 deliverable (lands after freeze; counter clause a requires it at REV). Expected. |
| `corpus/knowledge/waybar-walker-semantics.md` | YES (this is the real home; the registration cites it under `merge/mado/`, see unresolved list) |
| `merge/mado/host-bar-producers-r28.md` | NO — no `merge/` dir in lane tree OR fleet root (checked both) |
| `merge/mado/host-producer-outputs-r29.md` | NO — same |
| `.ufo/waves/round-40/c1/native-capture.jsonl` | YES (blob present; 70 non-blank lines — matches counter clause k) |
| `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt` | YES (blob present) |
| `.ufo/waves/round-40/ctl/run-c1-controls.py` | YES |
| `.ufo/waves/round-40/ctl/run-c2-controls.py` | YES |
| `.ufo/waves/round-40/receipts/{axis-base,c1-before-base,c2-before-base,ctl-c1,ctl-c2,census-before,selftest-base}.txt` | all YES (7/7 blobs present) |
| `.ufo/waves/round-40/fetch/` | absent at freeze — destination for C2 Gate receipts (counter clause d commits them at REV). Expected. |
| `considerthese/2026-10-25.md` | YES (freeze tree line 11757; `2026-10-24.md` also present) |
| `.ufo/waves/round-40/registration.md` | YES (line 11742) |

Receipt contents match the registration's cited strings (checked via `git show
5e7e885:...`):
- `axis-base.txt`: `navigation published=56/56`, `calibration published=51/51`,
  `operability published=12/12`, `MADO_AXIS: checked=3 mismatched=0 rev=9fc511dd…` ✓
- `c1-before-base.txt`: `fixtures=0/13 tool=present verdict=TARGET_MISSED`, clause b
  `selftest=71/71` (the cited "base: 71"), `exit=1` ✓
- `c2-before-base.txt`: `admitted=0/1 verdict=TARGET_MISSED`, `exit=1` ✓
- `ctl-c1.txt`: `CTL_C1: controls=18 correct=18/18` (BASE + REF + M01–M16) ✓
- `ctl-c2.txt`: `CTL_C2: controls=21 correct=21/21` (P + N01–N20) ✓
- `census-before.txt`: seven W04 (S030,S042,S045,S097,S119,S120,S121) + one W01 (S277),
  `exit=0` ✓
- `selftest-base.txt`: `MADO_SELFTEST: 460/460 assertions passed`, `exit=0` ✓

## External pointers (URL HEAD only)
All resolved HTTP 200; downloaded blobs match the registry's recorded sha256 pins:
| URL | HEAD | sha256 (downloaded) vs pin |
|---|---|---|
| `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` | 200 | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` == S162 row pin |
| `…/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp` | 200 | `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807` |
| `…/hyprwm/Hyprland/v0.56.2/src/config/legacy/ConfigManager.cpp` | 200 | identical bytes to efb509 pin (tag == pinned commit) |
| `…/hyprwm/Hyprland/v0.56.2/src/config/shared/complex/ComplexDataTypes.hpp` | 200 | identical bytes to efb509 pin |
| `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp` | 200 | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` == S173 row pin; pinned commit `3a1c1b25b059dae2c6bbc46991562ba1158d125c` also HEAD 200 |

Cited line ranges verified by reading the downloaded sources:
- hyprlang `src/config.cpp:185-264` contains `configStringToInt` in full (185..274),
  including 0x hex, rgba/rgb ARGB forms, true/on/yes→1, false/off/no→0 — matches the
  counter's model. ✓
- Hyprland `src/config/legacy/ConfigManager.cpp:103-170` contains
  `configHandleGradientSet` (103–161): clears `m_colors`, sets angle only when a `deg`
  token is present — the cited inheritance rule. ✓
- `src/config/shared/complex/ComplexDataTypes.hpp:69-77` = `CGradientValueData::toString`
  (lowercase unpadded hex words + `Ndeg`); `:80-136` = `CCssGapData` (1–4-value CSS
  expansion + toString); `:154-175` = `CFontWeightConfigValueData` (WEIGHTS map
  100..1000, case-insensitive parse). ✓

## Unresolved pointers (report)
1. `merge/mado/host-bar-producers-r28.md` — cited in registration §Frontier step/assimilation
   ("round-3/4 entries"); no `merge/` path exists in the lane freeze tree nor in the fleet root
   (`ls /home/vgpnk/Projects/shokunin/merge` → no such file). UNRESOLVED at 5e7e885.
2. `merge/mado/host-producer-outputs-r29.md` — same. UNRESOLVED at 5e7e885.
3. `scripts/sources-census.sh` — not a lane-tree blob at freeze; resolves only as the fleet
   file (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, exists). Partial.
4. `merge/mado/waybar-walker-semantics.md` — cited package path absent; the file itself
   resolves at `corpus/knowledge/waybar-walker-semantics.md` (freeze tree). Path mismatch.

Expected-absent (deliverables/destinations landing after freeze, not dangling): the C2 entry,
`corpus/lessons/round-40.md`, `.ufo/waves/round-40/fetch/`, and the C1 `--live` delivery in
`tools/mado-options.py`.

## Supporting evidence (named)
- `git cat-file -e 5e7e885^{commit}` / `9fc511dd^{commit}` → OK x2.
- Freeze tree listing `git ls-tree -r --name-only 5e7e885` (11934 paths) saved at
  `.ufo/waves/round-40/w1/ConnEvidenceResolve/freeze_tree.txt`.
- Counter sources read via `git show 5e7e885:quality/counters/{c1-r40-live,c2-r40-forms-entry}.py`.
- External sources saved at `.ufo/waves/round-40/w1/ConnEvidenceResolve/{cm_v056.cpp,cdt_v056.hpp,hl_config.cpp}`.

## Verification for main agent
Re-run any pointer check above with `git cat-file -e 5e7e885:<path>` (lane) or `curl -I`
(URLs); receipts re-derivable via `git show 5e7e885:.ufo/waves/round-40/receipts/<name>.txt`.
No lane files were written outside the seat dir and the named report path.
