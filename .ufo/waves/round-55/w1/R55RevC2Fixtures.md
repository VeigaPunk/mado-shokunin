# R55RevC2Fixtures — wave w1 report (round 55, C2 fixture audit)

Deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC2Fixtures/fixture-audit.md`
(receipts: `…/w1/R55RevC2Fixtures/receipts/{interp.py,drive.py,drive-output.txt,ablation-literal-empty-stack.txt}`).

## Verdict

- **Freeze defects (committed expectation disagrees with §C2 text): none.** 18/18 hand-derived stdout byte-equal to
  `expected.out`; 18/18 derived rc equal `expected.rc`.
- **Contract ambiguity A1 (decides F10):** §C2 "KEY is the stack joined with `:` then `:` then LHS" read literally for an
  empty stack gives `:<LHS>`, which drops the top-level `device[kbd-a]:repeat_rate` line and yields F10 `unsupported=3`
  (committed 4). Intended reading (empty stack → KEY = LHS) gives 4. Reported for the L1; frozen text not edited.
- **Source-citation gap A2 (decides F18):** §C2 cites `ConfigValues.cpp:277-280` for `numlock_by_default` 0..1. Pin line 277
  is `MS<Bool>("input:numlock_by_default", …, false, …)` with no min/max; the 0..1 range is not in the cited source.
  Lines 279–280 (`repeat_rate` 0..200 with min 0/max 200; `repeat_delay` max 2000) do match the contract.
- **F02 args vs committed host pins:** consistent with the host, but the keyboard name is not verifiable (O1, below).

## What I did (commands and decisive output)

1. Read `registration.md`, `claims-frozen.md` (contract text; `fetch/`, `frozen-tables.json` c2 keys read; nothing edited).
2. Read all 73 files under `fixtures/c2/F01..F18` (`cat -A`). Read `fetch/host-input.conf`, `fetch/host-getoption.json`,
   `fetch/SHA256SUMS.txt`. I did not read any other seat's output, any tool source, or any hold-out path. The hold-out
   directory was not looked for; the `fixtures/c2` listing shows only F01–F18.
3. Host reads (read-only, allowed): `cmp fetch/host-input.conf ~/.config/hypr/input.conf` → identical, 1584 bytes;
   `hyprctl getoption input:repeat_rate -j` → `40`; `input:repeat_delay -j` → `250`; `input:numlock_by_default -j` → `1`;
   `hyprctl devices -j` → keyboard names listed (no `at-translated-set-2-keyboard`); `hyprctl version` →
   `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`. No keyword, dispatch, reload or write.
4. `sha256sum -c fetch/SHA256SUMS.txt` → all 10 `OK`, including `host-input.conf` and `host-getoption.json`.
5. Wrote an independent interpreter from §C2 text in scratch (`interp.py`) and a driver (`drive.py`) that runs it with
   cwd = lane root on each `args.json`, diffs bytes and rc, and checks committed bytes against
   `frozen-tables.json` `c2.fixture_file_sha256`. Output (`receipts/drive-output.txt`, tail):
   `FAILS: none`, 18 lines `out_match=True rc_match=True frozen=ok`.
6. Ablation with the literal empty-stack KEY reading (`receipts/ablation-literal-empty-stack.txt`): `FAILS: ['F10']`
   (only F10; the other 17 still match).

## Per-fixture result (hand-derived from §C2 text; full table in fixture-audit.md)

F01 `*`, 25/600/0 `-/-/-`, unsupported 0 — match. F02 `G/G/G` 40/250/1, LIVE AGREE ×3 — match.
F03 rate 30 `G` — match. F04 kbd-a `50 300 0 D/G/-`, kbd-b `30 300 0 G/G/-` — match.
F05 kbd-a numlock 1 `-/-/D`, kbd-b numlock 0 `-/-/G` — match. F06 device with no keys falls back to global — match.
F07 `nope` → prefix `no` → 0 (not unsupported) — match. F08 `online` → prefix `on` → 1 — match.
F09 device block merge: rate 50 D, delay 100 D, unsupported 0 — match.
F10 unsupported 4 (`$r`, 9999 out of range, two `device[` forms) — match under intended reading; **mismatch (3) under literal reading — A1**.
F11 two configs, globals persist: rate 45 `G`, numlock 1 `G` — match.
F12 `33 # fast` → 33; `4##0` → unsupported; unsupported 1 — match.
F13 LIVE DIFFER ×3 (config 30/600/0 vs live 40/250/1), DONE DIFFER — match.
F14 rate AGREE, delay/numlock UNKNOWN, DONE UNKNOWN — match.
F15 missing path → `SETUP unreadable`, rc 2 — match. F16 `{not json` → `SETUP bad_json`, rc 2 — match.
F17 no args → `SETUP usage`, rc 2 — match.
F18 numlock 2 → unsupported (range 0..1, **A2 source gap**), delay 2000 and rate 200 inclusive → from `G/G/-`, unsupported 1 — match.

## Other observations

- **O1 — F02 keyboard name:** `at-translated-set-2-keyboard` is not in any committed pin (`SHA256SUMS.txt` has no device
  list) and not in `hyprctl devices -j` on this host (10 keyboards, e.g. `hp--inc-hyperx-alloy-origins-core`,
  `hl-virtual-keyboard-fcitx5`). The expected output does not depend on the name (the host config has no device block),
  so the expectation is correct. But F02 does not exercise a per-device join against a real device.
- **O2 — unspecified cases (no fixture uses them):** precedence when a config is unreadable and getoption is bad JSON;
  whether a whitespace-only `--getoption` line counts as "non-empty".

## Deviations and limits

- I did not run `tools/mado-kbdopts.py`, `quality/check-r55-controls.py` or any counter; this is a text/hand check only.
- I did not re-audit the source semantics beyond the three pin lines cited above (ConfigValues 277–280, legacy ConfigManager
  1113–1124 `getConfigValueSafeDevice` read, InputManager 1282–1283 read).
- The hold-out was not looked for or used.
- No tools installed or updated. No pacman, no package manager.
- Lane writes: only `.ufo/waves/round-55/w1/R55RevC2Fixtures.md` and `.ufo/waves/round-55/w1/R55RevC2Fixtures/`. No tracked
  file, no git or jj mutation, no commit, no task or background job.
- Scratch: `/fast/scratch/hyaku/mado-r55/R55RevC2Fixtures/` (interp.py, drive.py), removed before yield after receipts were
  copied into the deliverable directory.
