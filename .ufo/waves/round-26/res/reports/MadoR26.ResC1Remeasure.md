# Residual — C1 re-measure, independent re-derivation (MadoR26.ResC1Remeasure)

Date: 2026-10-23. Lane: /home/vgpnk/Projects/shokunin/mado-shokunin, lane clean at start (`git status --porcelain` empty), no lane or fleet writes except this report.

## Verdict

**C1 RE-MEASURE agree** — the landed 41/41 TARGET_MET at 2b3487f7 reproduces independently: shas re-derived, two fresh-seed counter-v2 runs both TARGET_MET with all guards green, and the tool bytes contain none of the snapshot-derived content the predicate forbids in spirit.

## 1. Hash re-derivation

| Object | sha256 (recomputed) | Expected | Match |
|---|---|---|---|
| `git show 2b3487f7:tools/mado-anims.py` | `2beda3f7b1a5a7901f6a2cfc7e5b314b68ea9be8d0da27d3a92879946d9cab7d` | `2beda3f7…cab7d` | yes |
| counter `c1/count-v2.py` (committed bytes at 2b3487f7) | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` | `4ed70b54…6428` (registration pin) | yes |
| working-tree `tools/mado-anims.py` | `2beda3f7…cab7d` (identical to committed bytes) | — | yes |

`2b3487f7` resolves to `2b3487f75a09ac03f15666810b0145da2538565f`; the counter printed the same rev and oracle pin `680798ed…e441` in every run. Landing commit message records the tool sha.

## 2. Fresh-seed runs (both TARGET_MET)

Invoked exactly as the residual call prescribes: `cd <lane> && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 python3 -I .ufo/waves/round-26/c1/count-v2.py 2b3487f7 --jobs 4 --seed <seed>`; seeds freshly drawn from /dev/urandom, both distinct from the landed run's seed `4408656415ee7578`.

| Run | seed | result | guards | HOST_SAFETY |
|---|---|---|---|---|
| landed (comparison) | `4408656415ee7578` | 41/41 TARGET_MET, exit 0 | ORACLE_VERSION `efb50993…`, base_twice equal 35/6 | delta 0 (1338→1338) |
| re-run 1 | `b74f4955157288e1` | 41/41 TARGET_MET, exit 0 | same, all green | delta 0 (1338→1338) |
| re-run 2 | `f372c53d3f5c8f6f` | 41/41 TARGET_MET, exit 0 | same, all green | delta 0 (1338→1338) |

Both re-runs: snapshot 79 files, digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727` (identical to the landed run); every case PASS with missing=extra=0 on both node and bezier fields; 79 of 80 generated cases `changed=yes` (run 2 C06 `changed=no` — diagnostic only). Family mix per case (APPEND/EDIT/SYNTH with op lists) is seed-dependent and differs across all three receipts, so the agreement is not a replay of one case set.

Counter discrimination cross-check: under the same frozen counter, the snapshot-cache control scores 4/41 TARGET_MISSED (`.ufo/waves/round-26/controls/v2/K1SnapshotCache.txt`, seed `72d13a4e7200c4dd`), with the 10 SYNTH trees missing 17–22 nodes each — a 41/41 pass therefore requires reading the case tree's actual bytes.

## 3. Spirit audit of the tool bytes (2beda3f7…)

Read in full (503 lines); greps run against the working tree, which is byte-identical to the committed bytes.

- **Forbidden environment/proc reads: none.** Imports are exactly `glob, json, os, stat, struct, sys`. No `os.environ`/`getenv`, no `/proc`, no `subprocess`, `socket`, `urllib`, `time`, `hashlib`, no network or state files. Sole file access is `open(path, "rb")` on config files resolved from `--home`; only stdout is written.
- **No keying on paths/mtimes.** `os.stat` appears once, as an `S_ISREG` regular-file gate in `handle_source`; no mtime/ctime/atime reads, no path-name conditionals, no caching between runs (single process, state in memory only). Random case directories and shuffled order cannot influence it.
- **Embedded tables are upstream shape, not snapshot content.** `NODE_TABLE` (35 nodes + parents), `NODE_DEFAULTS` (5 entries), `DEFAULT_BEZIER`, `LINEAR_BEZIER` are transcriptions of Hyprland `efb50993` AnimationTree.cpp `reset()` / hyprutils v0.14.2 AnimationConfig.cpp:13, with upstream line citations in comments. The snapshot's own directive content is absent — greps for its bezier names (`easeOutQuint`, `easeInOutCubic`, `almostLinear`, `quick`, bare `ease`), its speeds (5.39, 3.79, 1.49, 1.73, 1.46, 3.03, 3.81, 1.79, 1.39), its styles (`popin`, `slidevert`, `gnomed`, `slidefade`), its bezier coordinates, and any host string (`vgpnk`, `omarchy`, `/home/`) return no matches in the tool (the only near-hits are upstream-cited `DEFAULT_BEZIER = (0.0, 0.75, 0.15, 1.0)` and the docstring's "no socket, no network").
- **Behavioral confirmation.** The tool passed 20 SYNTH trees containing none of the snapshot's files and 20 EDIT cases rewriting/deleting the snapshot's own lines, at fresh random directory names — the shapes that break a snapshot cache or label-keyed tool (which stall at 4/41 and 17–22 node misses per SYNTH case under the same counter).

## 4. Both PRED lines

**PRED-C1-r26 (v1, superseded for judgment by the v2 redesign; kept with its receipts):** "At REV, the committed bytes of tools/mado-anims.py, run in the tool sandbox (no network, no /run, cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for the unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases the same animation-node set (name, overridden, bezier, enabled, speed, style) and the same bezier set (name, X0, Y0, X1, Y1) that Hyprland v0.56.2 itself reports with `hyprctl animations -j` for the same tree (a nested, headless, session-isolated instance run by the counter on a copy with exec lines removed); target: cases_pass=41/41."

**PRED-C1-r26-v2 (governing; registration.md redesign section = `c1/count-v2.py:12-24` docstring = my receipts' label, verified identical):** "At REV, the committed bytes of tools/mado-anims.py, run in the tool sandbox (no network, no /run, cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for the unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases (20 that append directives to the snapshot, 10 that edit or delete the snapshot's own directives, 10 independent trees that contain none of the snapshot's files) the same animation-node set (name, overridden, bezier, enabled, speed, style) and the same bezier set (name, X0, Y0, X1, Y1) that Hyprland v0.56.2 itself reports with `hyprctl animations -j` for the same tree (a nested, headless, session-isolated instance run by the counter on a copy with exec lines removed); target: cases_pass=41/41."

Both re-runs print `PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET`.

## Host safety

Nothing started outside the sanctioned counter runs; both re-runs report `hyprland_coredumps_before=1338 after=1338 delta=0`. All processes exited (counter exits, workspace tmp cleaned by the counter).

## Tooling directive record

No tool installed or upgraded; nothing needed beyond the lane's pinned harness.

## Residual risk / verification gaps

- No LSP server answered for a standalone lane script in this seat, so semantic checks (references/definition/diagnostics) were unavailable; the literal-token greps above are text evidence, with the counter's behavioral discrimination (control 4/41 vs tool 41/41 ×2) carrying the semantic weight.
- The tool resolves absolute/`~`-escaping `source =` paths per hyprlang semantics, so it can read outside `--home` when a config says so; under the counter sandbox such paths see only sandbox bytes, and this is the stated reads-outside-`--home` limit class (R7), not a snapshot shortcut.
- `float32()` emulates `std::stof` via struct pack/unpack on x86-64; exercised on all 80 generated cases including decimal speeds (e.g. 5.39, 1.73) without mismatch, but exotic out-of-range literals beyond the generator's space are untested.
- v1 (`c1/count.py`) was not re-run: v2 governs per the registration redesign note, v1 and its receipts stand unchanged.
