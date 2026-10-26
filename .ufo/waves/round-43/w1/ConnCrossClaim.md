# ConnCrossClaim — round-43 w1 report (final)

Seat: ConnCrossClaim (cross-claim / cross-source). Deliverable: `.ufo/waves/round-43/w1/ConnCrossClaim/cross.md`.

What was done:
- Read frozen registration (b2e2efd) and both counters' contracts, reference tool, control runners, receipts, pins S290-S299, registry, host files.
- Verified pin locators on raw bytes (`verify-quotes.py` → `quotes-verified.txt`): S290:16, S291:426, S292:60, S293:11, S294:70, S295:45, S296:395, S297:4, S298:49, S299:33; all word-bounded, ≤25 words.
- Verified host provenance: pinned S297 byte-identical to live `~/.config/hypr/gkeep.conf` (`cmp`); S299 ≡ `sed -n '446,$p'` of `~/Projects/gkeep/gkeep/ui.py` (488 lines) modulo 2-line synthetic header; ui.py full-file sha256 matches the header claim.
- Verified the only `static_.size` consumer across all seven Hyprland pins is `CDefaultFloatingAlgorithm::newTarget` (S292:55-66); `hyprctl clients -j` size = `GEOMETRIC_GOAL` (S296:426-428/447-448; S295:17-24).
- Separability empirical runs (scratch): C1 with the reference via `--tool` at rev a35cfdf → `fixtures=37/37 tool=present verdict=TARGET_MET` (receipt `c1-ref-run.txt`); C2 control P real → `admitted=1/1 verdict=TARGET_MET` (receipt `c2-control-p-real.txt`). Static confirmation: C1 counter references no C2 surface; C2 counter's only C1 token is its residual sentence (line 86).
- Findings: (1) C1's FullMatch model and its consumed `size` field rest on facts C2 pins (S290:16; S296:427-428) — consistent both directions, one-way dependence; (2) no contradictions among all checked pairs; (3) unpinned sources that would strengthen both: Hyprland ConfigManager.cpp (rule grammar; needs S300+ id + L1 fetch) and an oracle observation (gkeep window open; reserved by registration, unobtainable by seats); (4) separability holds (both empirical runs at target with the other side absent). Risks: quote-binding gap for the GOAL claim (recommend quoting S296 raw line 426 three-token call or S295 lines 17-24); "only-floating" exclusivity is a cross-pin grep fact, not a single-line quote.

Tools: none installed (existing python3/git/bwrap; no pacman, no host/compositor mutation, no git writes). Scratch `/fast/scratch/hyaku/mado-r43/ConnCrossClaim` removed after completion; all cited receipts copied into the seat dir.
