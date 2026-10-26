# Seat ScrSkillFinal — round 41 w2 report

## Status
- Target: final SKILL.md / PROVINCE.md insertion text for the delivered `tools/mado-globals.py`.
- Deliverable: `.ufo/waves/round-41/w2/ScrSkillFinal/insert.md` (written; see below).
- Verification runs: delivered tool executed on
  `.ufo/waves/round-41/fetch/xdph-journal.txt` (sha256 `bf8fa91a…`) this seat, 2026-10-25.
- No tool installed (python3 already present; no channel action). No host-service/compositor
  mutation; no `--live` run (not needed; journal-file runs used); no pacman.

## What was attacked
1. DATA commit `07f2641` deliverable `tools/mado-globals.py` — operability/C1 side
   (fixtures 39/39 claimed). Ran real workloads; see receipt list below.
2. The w1 drafts (`ScrSkillProvince/skill-rows.md`, `province-row.md`) — sample lines were
   pasted from the v1 reference control, not the deliverable; re-derived against the real tool.
3. Anchor line numbers claimed in w1 — re-verified at the DATA commit.
4. PROVINCE.md inventory-table completeness (w1 finding) — re-measured at HEAD.

## Deliverable validation
- `insert.md` subsection 'Advertised Wayland globals': 17 non-blank lines (< 25).
- Every sample line in `insert.md` verified verbatim against the run receipts (`/tmp/globals-run1.txt`,
  `/tmp/globals-expect2.txt`) — PASS; the exact command string is present.
- Portal provenance re-verified this seat: `xdph-PortalManager.cpp:85` `CPortalManager::onGlobal`,
  log at `:88` (`Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);`).

| Check | Command (lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`) | Result |
|---|---|---|
| Deliverable == v2 reference | `sha256sum tools/mado-globals.py` vs `git show 07f2641:tools/mado-globals.py` vs `.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt` | all `286c051f…` (byte-identical) |
| Journal identity | `sha256sum .ufo/waves/round-41/fetch/xdph-journal.txt`; `git show 07f2641:…xdph-journal.txt` | `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7` both |
| Main run | `python3 tools/mado-globals.py --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt` | rc 0, 66 stdout lines, stderr empty; final line `… expected_missing=- ignored=0 verdict=OK` |
| Diff run | same + `--diff` | rc 0, 67 lines; DIFF line 1902 bytes: added 63 names (first `ext_background_effect_manager_v1`, last `zxdg_output_manager_v1`), removed 8, `ver_changed=-` |
| Expect present | `--expect hyprland_focus_grab_manager_v1` | rc 0, `expected_missing=- verdict=OK` |
| Expect absent | `--expect zwlr_screencopy_manager_v2` | rc 1, `expected_missing=zwlr_screencopy_manager_v2 verdict=MISSING_EXPECTED` |
| Selftest | `python3 tools/mado-globals.py --selftest` | rc 0, `MADO_GLOBALS_SELFTEST: 63/63 passed` |
| Exit 2 (usage/unreadable/too_large/bad_expect) | synthetic /tmp inputs | all `MADO_GLOBALS: SETUP …`, rc 2 |
| Exit 3 | empty journal | `sessions=0 … verdict=NO_SESSIONS`, rc 3 |
| Exit 4 | all-adverts-ignored input | `sessions=0 … ignored=1 verdict=UNRECOGNIZED_FORMAT`, rc 4; one-ignored-of-two → rc 0 `ignored=1` |
| Exit 5 | not run (would need a live journalctl failure); grounded in docstring lines 13-24 and `read_live`/`resolve_program` code only | unobserved |

## Findings
- **No defect found on the DATA deliverable (C1 surface).** Runs match the stated contract; exit
  map 0/1/2/3/4/5 confirmed except 5 (unobserved, code-ground only).
- **Not a defect — w1 sample lines are now stale, which is why this insert exists:** the w1
  receipts (`ref-run-journal.txt`/`ref-run-diff.txt`) matched the v1 reference, whose
  `MADO_GLOBALS:` line lacks `ignored=0` (the v2 deliverable adds it) and whose selftest was
  47/47 vs the deliverable's 63/63. The w1 draft's rows and this insert must therefore use the
  deliverable's real bytes; sample lines in `insert.md` are pasted from the runs above.
- **Anchors hold at the DATA commit:** SKILL.md (2006 lines) probe table header at 202, last row
  221; decision table last row 156; PROVINCE.md (95 lines) inventory last row 30. Verified by
  `grep -n`/`read` on `git show 07f2641:…`.
- **PROVINCE.md inventory is stale (w1 finding corroborated):** `git ls-tree --name-only HEAD tools/`
  = 11 files; table rows (lines 24-30) list 7. After inserting the `mado-globals.py` row,
  `mado-eventq.py`, `mado-options.py`, `mado-wsrules.py` remain unlisted despite the round-23
  "every tracked file" clause. Reported; not repaired (frozen file).

## Checks not run (not claimed)
- `--live` leg (a live `journalctl` subprocess) — allowed verb but not needed for the deliverable.
- Exit 5 live-failure paths — would need a broken/non-executable journalctl on this host.
- No counter/control re-runs; C2 scoring is the L1's/main agent's.

## Artifacts
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/ScrSkillFinal/insert.md`
- /tmp receipts: `globals-run1.txt`, `globals-run2.txt`, `globals-expect{1,2,3}.txt`,
  `globals-selftest.txt` (ephemeral).
