# RevC1Tool — round-50 w1 attack on the landed tools/mado-keysym.py

Status: IN PROGRESS (stub; refined in place as work completes).

- Target: `tools/mado-keysym.py` at `13631f24050f22db92bf5bd33e0f4d014192992e` (sha256
  `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265`, byte-equal to the
  round-49 candidate `.ufo/waves/round-49/candidate/mado-keysym.py`; verified 2026-10-27).
- Judge: `/usr/lib/xkbcommon/xkbcli-how-to-type` (libxkbcommon 1.13.2-1), contract =
  stdout bytes + exit code of `how-to-type --keymap FILE --disable-compose --keysym ARG`.
- Scope: constructs of the serialized keymap format the tool does not model or models
  differently; each exercised through `xkbcli-compile-keymap`, compared tool vs judge;
  divergence not caught by `quality/counters/c1-r49-fixtures.json` (633) = finding.
- Pins: `.ufo/waves/round-50/w1/RevC1Tool/pins/` (libxkbcommon tag `xkbcommon-1.13.2`).
- Scratch: `/fast/scratch/hyaku/mado-r50/RevC1Tool/` (removed before finish).
