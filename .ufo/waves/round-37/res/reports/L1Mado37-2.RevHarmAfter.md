# RevHarmAfter — harm-watch after-side, mado round 37 (residual falsify call)

Seat: reviewer, read-only. Date 2026-10-25. Baseline: `w1/reports/RevHarmBefore.md`. Freeze: `registration.md` (C1 PRED-C1-r37-v2, C2 PRED-C2-r37-v2, amendment 1, erratum 1). Landed data commit compared: `3f424257a1ea69cd2655770259ba00b423293f4f`; base `b4e47e980bfb0cbc8a4e788f59a41db858751fd8`.

## Verdict

**NOT HARMED on all three axes (navigation, calibration, operability). Zero findings.** Every named item ran cleanly at the landed commit and matches the baseline where a match is expected; the only deltas are the round-37 additions themselves (index 50→52 entries, 2 new knowledge entries, 1 new tool, 2 new counters), all of which are additive. No deletion touches an existing knowledge entry or tool — the diff has **zero deleted files** and 9 deleted lines across 5 modified files (2 source-registry row replacements, 7 git-env-sanitization refactor lines).

## Items

| # | Command (cwd = lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`) | Output (quoted) | Exit | Baseline | Verdict |
|---|---|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed` | 0 | 460/460 | PASS (unchanged) |
| 2 | `sha256sum tools/mado-verify.sh` | `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1  /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` | 0 | identical | PASS (unchanged) |
| 3 | `python3 -I quality/check-index.py --rev 3f424257a1ea69cd2655770259ba00b423293f4f --repo .` | `MADO_INDEX: rev=3f424257a1ea69cd2655770259ba00b423293f4f indexed=52/52 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 | indexed=50/50 (at `--rev master`) | PASS; index grew 50→52 with zero gaps |
| 4 | `python3 -I quality/check-index-rows.py --rev 3f424257a1ea69cd2655770259ba00b423293f4f --repo .` | `MADO_INDEX_ROWS: rev=3f424257a1ea69cd2655770259ba00b423293f4f rows=52 errors=0 warns=3` + same 3 warnings as baseline (verbatim): `WARN cited-glob-nomatch: .ufo/evidence/round-12/getprop-*.txt` in `knowledge/window-rule-effects-getprop.md`; `WARN cited-glob-nomatch: .ufo/evidence/round-12/drift-*.txt` in `knowledge/config-drift-r12.md`; `WARN cited-glob-nomatch: .ufo/waves/round-24/fetch/S###.bin` in `knowledge/rule-attribution-r24.md` | 0 | warns=3 (same 3) | PASS (warn count unchanged) |
| 5 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 8 lines: `mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` + 7 `W04` lines (S030, S042, S045, S097, S119, S120, S121 — identical set to baseline) | 0 | 1 ok, 7 W04 | PASS (identical) |
| 6 | `sha256sum ~/.config/hypr/*.conf ~/.config/waybar/config.jsonc ~/.config/waybar/style.css` | 15 files; per-file hashes identical to baseline for all 15 (e.g. `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365  hyprland.conf`, `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829  waybar/config.jsonc`); combined digest `89e214b8c942c705c550b6868569b9943d37cf9d159c2757fc5bdce1f8ac3195  -` | 0 | identical combined digest | PASS (unchanged) |
| 7 | `coredumpctl list --no-pager 2>/dev/null \| grep -ci hyprland` | `0` (grep exit 1, no match) | grep 1 | 0 | PASS (0 Hyprland coredumps) |

## Deletion audit (item: does any deletion touch an existing knowledge entry or tool?)

`git diff --numstat b4e47e980bfb0cbc8a4e788f59a41db858751fd8 3f424257a1ea69cd2655770259ba00b423293f4f` → 91 files, +6810 −9. Only 5 files contain deletions, 9 lines total:

- `corpus/SOURCES.md` (8+2): the deleted lines are the S189 and S201 source-registry rows (re-opened this round per registration; replaced by new rows for the same source ids). These are source receipts, not knowledge entries and not tools.
- `quality/check-axis-scores.py` (4+2), `quality/check-evidence-pointers.py` (9+3), `quality/check-index-rows.py` (2+1), `quality/check-index.py` (2+1): deleted lines are internal git-invocation helper lines; all 7 are replaced by the same call plus `env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")}` (git-env sanitization; check-evidence-pointers.py documents it in a comment). No check logic is removed, and the mado-verify.sh selftest (460/460, unchanged hash) exercises the checker fleet.

`git diff --diff-filter=D --name-only …` → empty: **zero deleted files**. New files are additions only: `corpus/knowledge/event-delivery-limits-r26.md`, `corpus/knowledge/event-queue-observability-r37.md` (new entries), `tools/mado-eventq.py` (new tool), `quality/counters/c1-r37-event-ground.py`, `quality/counters/c2-r37-eventq.py` (new counters). No existing file under `corpus/knowledge/` or `tools/` is deleted or loses content.

**Verdict: no deletion touches an existing knowledge entry or tool.**

## Per-axis verdict

- **Navigation** — NOT HARMED. `check-index.py` at the landed rev: `indexed=52/52 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0. The index grew only by the two new round-37 entries; zero gaps.
- **Calibration** — NOT HARMED. `check-index-rows.py` warns=3 (identical warning set to baseline), errors=0; census identical (`1 ok`, same 7 `W04`). The checker code change is env sanitization only, and mado-verify.sh is byte-identical and selftest-green.
- **Operability** — NOT HARMED. Selftest 460/460 (unchanged). Config set (13 hypr `.conf` + waybar config/style) byte-identical per file and combined digest `89e214b8…` unchanged; 0 Hyprland coredumps.

## Residual risk / verification gaps

- The after-side ran the assignment's literal commands with `--rev 3f424257…` — the baseline's item 3/4 wording risk (missing `--rev`) is moot because the data commit is named.
- Baseline captured checks at `--rev master` (50 rows); this run uses the landed commit (52 rows). The +2 is the round-37 target set; row count comparison is apples-to-apples once the rev is fixed.

## Writes and tooling

- Writes: this report; scratch under `/dev/shm/mado37-L1Mado37-2.RevHarmAfter/` (config-sha.txt capture). No lane production file, git/jj state, config, service or socket touched.
- Tool installs or updates: none.
