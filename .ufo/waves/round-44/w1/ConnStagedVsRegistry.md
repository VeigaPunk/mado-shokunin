# ConnStagedVsRegistry — staged rows vs lane registry for the gkeep residue (round 44 w1)

Status: COMPLETE. Matrix: `.ufo/waves/round-44/w1/ConnStagedVsRegistry/matrix.md`.

## Verdicts (all locators computed by grep -n; full outputs in matrix.md)

1. **URLs the lane holds.** Lane registry (234 rows, tops S297) holds Window.cpp
   ONLY as S164 (`corpus/SOURCES.md:176`), at the commit-hash form
   `…/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp`,
   sha256 `d735d454…` — byte-identical to the round-44 pin `fetch/Hyprland-Window.cpp`
   (`receipts/fetch-sha256.txt:2`). Lane holds gkeep `ui.py` ONLY as the S297
   excerpt row (`corpus/SOURCES.md:246`, own-work, `.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py`,
   lines 446–488, records full-file sha256 `07a3c4a5…` = the pin's hash). The full
   raw URL `raw.githubusercontent.com/VeigaPunk/gkeep/133b867…/gkeep/ui.py` appears
   in 0 lane rows → the provisional new row S301 adds no held URL.

2. **Anchor/tag forms.** Lane convention: Hyprland code at commit-hash URLs (35 rows
   at efb5099; 0 rows at `/v0.56.2/`); staged residue cites Window.cpp etc. at the
   `/v0.56.2/` tag form 7+ times. Tag v0.56.2 == commit efb5099 (registration; host
   `hyprctl version`), same bytes (hash match above). Exact-string URL dedup would
   miss every one of these aliases. Lane-internal precedent: S018
   (`blob/v0.56.2/…/debug/HyprCtl.cpp`) and S158 (`raw/efb5099…/debug/HyprCtl.cpp`)
   are the same document/commit under two forms, both active — the lane's
   URL-equality screen (QUALITY.md:34; S030 rejected-dup precedent) is string-based
   and tolerates the alias pair.

3. **Tier C/community.** None. All 26 staged ids cited by the 10 residue files are
   tier A code/docs/dataset/own-work (14 code, 2 docs, 1 dataset, 9 own-work);
   staged tier-C rows (S210, S211, S216, S217, S230, S244, S348) are cited by other
   entries, not the gkeep residue.

4. **Private receipts.** Lane-side: S297 is a lane-private excerpt receipt. Staged-side:
   8 of the 26 cited rows are package-private `lanes/mado/roundN/fetch/*.txt`
   receipts (S275, S292, S293, S299, S310, S320, S326, S339) plus one host-file row
   (S251, ~/.config/hypr/gkeep.conf). The C2 entry should cite the public fetch/
   pins, not these.

5. **Duplicate-URL warnings the new rows add.** None. XDGShell.cpp @ efb5099,
   xdg-shell.xml @ 1.49 stable, gdktoplevel-wayland.c @ 4.24.1, gkeep-ui.py @
   133b867: 0 lane rows each (nearest neighbour S048 colour-management-v1.xml,
   different path). Window.cpp is held (S164) and correctly not re-opened.

6. **renumber-map.tsv: every mapping is by document — YES.** Both rows
   (S311→S164 hash-verified d735d454; S312→S301 hash-verified 07a3c4a5), neither
   by id. Map covers only the C2 predecessor's citations; sufficient for C2 scope.

## Hazards for the record

- **H1 (number collision):** 7 staged ids cited by the residue collide numerically
  with lane rows holding DIFFERENT documents: S284, S285, S286, S287, S292, S293,
  S297 (e.g. staged S297 = WindowRuleApplicator.cpp vs lane S297 = ui.py excerpt;
  lane S284 = FocusGrab.cpp vs staged S284 = Window.cpp). Anyone resolving staged
  citations by number alone lands on the wrong document. The 42-id collision file
  (`assimilation/collisions`) spans S203–S221, S253, S258, S277–S297.
- **H2 (string-dedup blind spot):** QUALITY.md:34's repeated-URL screen is
  string-equality; tag/commit aliases of one document pass it (S018/S158 live).
  Document-aware screening is what the renumber map applies for S311.
- **H3:** the r9 citation staged S287 (wiki.hypr.land 0.56.0 Window-Rules page)
  has no lane row; if r9's citations are ever assimilated, that row is genuinely new.

Tools: none installed (read-only grep analysis; no installs needed).
Scratch: none created (no fixtures built; all reads in-place).
