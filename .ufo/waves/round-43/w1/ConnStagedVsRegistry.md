# Seat report — ConnStagedVsRegistry (round-43 w1)

Status: COMPLETE. Full matrix in `w1/ConnStagedVsRegistry/matrix.md`.

- Compared the 25 staged rows cited by the 11 gkeep-theme files (SOURCES.append.md + the files' `source:` lines) against `corpus/SOURCES.md` (226 rows, tops S289).
- Verdicts: 5 reuse-held (S155/S158/S164 cover staged S284/S297/S298/S311/S318/S319), 8 new-rows (S255/S285/S312 gkeep ui.py dedupe → 1; S256; S286; S287; S302-S305 via pinned receipts S292-S295), 8 refuse (private `lanes/mado/roundN/fetch` receipts, unreopenable), 4 S251-extra: S251 → new row via planned S297 pin.
- No cited staged row is tier C/community; staged community/tier-C rows lie outside the theme and partly out-of-province.
- Staged ids S284-S287 collide with lane-held ids S284-S287 → any opened row must take a free id (≥ S290).
- Census W04/E04 for planned S290-S299: new rows S291 and S296 duplicate held URLs S155/S158 → W04 if scope differs (verified verbatim in fixture); E04 fatal if scope shared (verified verbatim). S290, S292-S295, S297-S299 add no URL duplicates. Baseline lane validate: exit 0 (E-free; existing W04 S030/S042/S045/S097/S119/S120/S121, W01 S277).

Tools: `scripts/sources-census.sh` (fleet; bash/coreutils/gawk, no installs). Scratch: `/fast/scratch/hyaku/mado-r43/ConnStagedVsRegistry` (deleted at finish).
