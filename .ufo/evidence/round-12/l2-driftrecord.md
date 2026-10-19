# L2 seat R12DriftRecord-3 — final output (verbatim, 2026-10-19)

**Files written** — line counts and SHA-256 prefixes:
- `SKILL.md` — 1,595 lines — `ec3c80b23eae`
- `corpus/knowledge/config-drift-r12.md` — 143 lines — `c3a8d5537f79`
- `.ufo/evidence/round-12/drift-hypr.txt` — 64 lines — `51162d2cecf8`
- `.ufo/evidence/round-12/drift-waybar.txt` — 62 lines — `c5865eded7be`
- `.ufo/evidence/round-12/drift-precedence.txt` — 18 lines — `77bd8e3e1113`
- `.ufo/round-12/sources/drift.md` — 18 lines — `262edc425234`

**Measured:** Hypr root is 29→32 lines, 1,273→1,329 bytes, 17→18 sources; the current SHA is `ce7483f3…`, and the backup matches the old `4f52854a…` pin. `diff -u` shows only lines 30–32 added. Active local `.conf` count is 13; the old 12 is preserved from the MADO-1 inventory.

Waybar config is 249→260 lines and 6,068→6,354 bytes; its top-level module count is 17→18, or 19→20 under MADO-R3-1’s expanded-group convention. Style is 136→155 lines and 1,887→2,256 bytes; the `style.css.pre-ai-readability` intermediate is 150 lines / 2,118 bytes. Backup epochs were converted with `date -u -d`.

`install.sh` at gkeep HEAD `133b867` has a SHA matching its HEAD blob. The live `hyprctl getoption` checks returned `general:gaps_out = 0 0 0 0` and `input:kb_layout = br`; `hyprctl configerrors` was empty (exit 0).

The gate’s round-12 EXPECT/LOCAL erratum is present. It still does not census unlisted local files or pin the Waybar module set. **Not run:** gate, selftest, or regression; the post-integration `--no-live` result remains unverified for the parent’s gate run. The old local-file count’s original listing command was not retained.
