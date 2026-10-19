# L2 seat R12GateReanchor-3 — final output (verbatim, 2026-10-19)

Implemented the round-12 re-anchor in `tools/mado-verify.sh`; wrote all requested gate receipts under `.ufo/evidence/round-12/`. No config or compositor writes.

**Measured outcomes**
- 18 — `grep -cE '^[[:space:]]*source[[:space:]]*=' ~/.config/hypr/hyprland.conf` (2026-10-19). Backup SHA `4f52854a3c143dcf…` matches the old pin; `diff -u` shows the gkeep lines appended at 30–32. Installer provenance: `~/Projects/gkeep/install.sh:21-36`; backup epoch is `2026-10-17T20:02:56Z`.
- 13 — `hypr.local.inventory` in `bash tools/mado-verify.sh --no-live` (2026-10-19); include graph and resolved targets both PASS at 18/18.
- 0 — FAIL; 0 — UNKNOWN in `bash tools/mado-verify.sh --no-live` (2026-10-19), exit 0.
- 268 — `bash tools/mado-verify.sh --selftest` assertions passed (2026-10-19), exit 0.
- 52 — `bash tools/mado-verify.sh` PASS; 0 FAIL, 0 UNKNOWN; `boundary.readonly` PASS (2026-10-19), exit 0.
- 10 — final re-cut defects KILLED, 0 survived, 0 inconclusive; `--regression` PASS (2026-10-19), exit 0. `PIN_MADO` now matches derived target `d41a884b…`; measured table remained 10/10 KILLED.
- Live-output title check: no title marker in `gate-live-after.txt`; source sweep `grep -nE 'hyprctl.*clients|\.title|\["title"\]' tools/mado-verify.sh` found no title accessor.

**Edited hunks**
- `tools/mado-verify.sh:2191–2197`: added the append-only erratum with old→new counts, provenance, backup epoch, and re-measure commands.
- `:2215–2216`: added `gkeep.conf` after `ai-usage.conf` in `EXPECT`.
- `:2257, :2259`: updated the local-conf comment to 13 and added `LOCAL+=(gkeep)`. The original array literal is retained so the recorded D6 mutation still matches.
- `:261, :265`: added the fixture source and `gkeep.conf` fixture file.
- `:1291`: updated `PIN_MADO` from the measured re-cut. `TABLE_MADO` is unchanged because the measured table matches it.

**Files and retained evidence** — line counts from `wc -l`, SHA-256 prefixes:
- `tools/mado-verify.sh` — 3241 — `wc -l` (2026-10-19); `79c5e64e2b5e`
- `.ufo/evidence/round-12/gate-regression-before.txt` — 15 — `wc -l` (2026-10-19); `a0768c317a31`
- `.ufo/evidence/round-12/gate-selftest-after.txt` — 3 — `wc -l` (2026-10-19); `cb394b6da29f`
- `.ufo/evidence/round-12/gate-no-live-after.txt` — 48 — `wc -l` (2026-10-19); `1c1410c2388f`
- `.ufo/evidence/round-12/gate-live-after.txt` — 67 — `wc -l` (2026-10-19); `406aedac4d66`
- `.ufo/evidence/round-12/gate-regression-setup.txt` — 10 — `wc -l` (2026-10-19); `8171784939e6`
- `.ufo/evidence/round-12/gate-recut.txt` — 69 — `wc -l` (2026-10-19); `4b924eb8696b`
- `.ufo/evidence/round-12/gate-regression-after.txt` — 15 — `wc -l` (2026-10-19); `44978bbd93cc`
- `.ufo/evidence/round-12/gate-shas.txt` — 15 — `wc -l` (2026-10-19); `8a60790a7c65`

**Risks/blockers:** No blockers. The live gate remains CLEAN with 8 existing notes, including the operator-owned hypridle absence and historical round-1 hash pin note. Harness SHA recorded: `75ed934dc86360f5…`.
