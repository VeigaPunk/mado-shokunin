# SentScope51 — scope & safety sweep, mado round 51 w1

Status: complete (mid/late-wave snapshot, lane HEAD `3ac31642`, round base
`6ca8c559`). All four assigned checks pass; two pin-hygiene items and the
pin-path consolidation are routed to L1.

## Verdict

1. **Write scope — PASS.** Every seat write is under `.ufo/waves/round-51/w1/`;
   the only untracked path outside it is L1's own `w1.ready.dispatched`. No
   tracked file is modified, staged or deleted (checked in seven passes). Registry
   members = seat reports = seat dirs = 43, one-to-one. Config planes
   (`~/.config/{hypr,waybar,walker,omarchy,terminals}`), `~/.local/bin` and the
   shokuknow checkout show no write in the window.
2. **Secret shapes — PASS.** `quality/check-session-material.py` over a snapshot
   of all seat-written files: `files=155 findings=0` and `files=241 findings=0`,
   exit 0 both times. Baseline for
   comparison: the same gate exits 1 with `findings=241 waived=49` at both the
   round base and HEAD, so the 241 are pre-existing and w1 adds none. An
   independent shape scan (tokens, `op://`, key blocks, JWTs, loopback/RFC1918,
   `file://`, `ssh://`, tailnet names) finds 0 hits and 0 private locators.
3. **Scratch rule — PASS.** 0 hardcoded tmp write targets across 20 drafted
   instruments. Three tmpish literals are refusal tables
   (`REFUSED_WORK_PREFIXES`, `TMPISH`) and two `mkdtemp()` calls honour `TMPDIR`
   and take `--scratch`/`--work`. No `bash`-level `/tmp` fixture driver in w1.
4. **Fetch pins — PASS with two routed items.** 19 pins verify by
   `sha256sum -c` **and** by recomputed git blob sha1 bound to the manifest's
   upstream revisions `efb5099…` (Hyprland, 12 files), `a21e87b…` (Hyprutils, 4)
   and `d5f07c6…` (hyprland-wiki, 3); URLs are
   `raw.githubusercontent.com` only; no local/private path appears in any pin
   or manifest; `SHA256SUMS` has no self row (D4/M50-9 honoured). One extra pin
   (`ScrDispatchEntry/fetch/Hyprland-SharedDefs.hpp`) is byte-identical to
   upstream `src/SharedDefs.hpp` but has **no manifest row**, and its filename
   implies a path that 404s.

## Routed to L1

- `PIN_UNMANIFESTED`: add a `SHA256SUMS`/manifest row for
  `Hyprland-SharedDefs.hpp` naming upstream `src/SharedDefs.hpp`
  (`sha256 0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087`).
- Pin path: `.ufo/waves/round-51/fetch/` (claims C2) does not exist yet; pins
  live in `ExecFetchDispatch/fetch/` and `ScrDispatchEntry/fetch/`.
- `ExecFetchDispatch.md` declares `…/ExecFetchDispatch/fetch-manifest.json`
  while the file is at `…/ExecFetchDispatch/fetch/fetch-manifest.json` — one of
  the two has to move before the freeze re-run.
- Declared-but-absent paths fell 12 → 2 across the sweep
  (`ScrDispatchEntry/held-citations.md`, `ScrDispatchEntry/pin-manifest.md`), in
  a seat still running: re-run `check-scope.py` at the freeze tip; absent at
  freeze = ABSENT defect.
- Cosmetic: the `SEAT = "/home/vgpnk/…"` constant in
  `ExecControlsC1/controls-c1/verify-controls.py` makes that verifier
  host-specific.
- Observation, outside round 51: 175 M of `w5-mado-m52-selftest.*` dirs (676) in
  `/tmp` from a prior wave. Disk guard: `/fast/scratch/hyaku` 64 % used,
  289.3 G free.

## Method

Read-only. `check-scope.py` (hermetic `--selftest`, 12/12, honours
`--scratch`/`TMPDIR`) plus the lane's own gate run at `--rev` on a scratch
fixture of the untracked files. All scratch work under
`/fast/scratch/hyaku/mado-r51/SentScope51/` (removed at finish); no git/jj
mutation outside those fixtures; no compositor socket, no service touched, no
tool installed.

## Deliverables

- `.ufo/waves/round-51/w1/SentScope51/scope-sweep.md`
- `.ufo/waves/round-51/w1/SentScope51/check-scope.py`
- `.ufo/waves/round-51/w1/SentScope51/receipts/sweep-final.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/sweep-pass5.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/sweep-pass6.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/selftest.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/write-scope.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/session-gate.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/session-gate-base.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/session-gate-head.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/pins-verify.txt`
- `.ufo/waves/round-51/w1/SentScope51/receipts/pins-verify-scr.txt`

Report: .ufo/waves/round-51/w1/SentScope51.md
