# R56W3ExecTagPin — tag and pin verification

## Finding
- **Attacked:** the C1 upstream revision identity and S383 `ConfigWatcher.cpp` source pin bytes; additionally recorded the requested kernel and man-pages versions.
- **Result:** the GitHub tag ref `v0.56.2` directly identifies commit `efb50993780079460b0cbed1363e2166a2de1d9f` (`object.type=commit`). The raw file served at the tag hashes to `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c`, matching the S383 pin cell exactly. No blocking mismatch.
- **Additional evidence:** kernel `7.2.11-arch1-1`; the two retrieved inotify manual pages identify Linux man-pages 6.19 (`inotify(7)` 2026-02-14; `inotify_add_watch(2)` 2026-02-08).

## Commands and decisive output
Exact commands and outputs are preserved in `R56W3ExecTagPin/receipts/tag-pin-a2.txt`. In brief:
- `curl -fsSL https://api.github.com/repos/hyprwm/Hyprland/git/ref/tags/v0.56.2` → `ref=refs/tags/v0.56.2`, object SHA `efb50993780079460b0cbed1363e2166a2de1d9f`, type `commit`.
- `curl -fsSL https://api.github.com/repos/hyprwm/Hyprland/git/commits/efb50993780079460b0cbed1363e2166a2de1d9f` → same commit SHA; API reports `verification.verified=false`, reason `unsigned`.
- `curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/config/shared/inotify/ConfigWatcher.cpp | sha256sum` → `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c`.
- `uname -r` → `7.2.11-arch1-1`.

The attempted `/git/tags/<sha>` peel request returned HTTP 404 because the tag ref object is directly a commit, not an annotated-tag object; the commit endpoint then succeeded. No data discrepancy indicated.

## Defects and limits
- **Blocking the claim:** none observed.
- **Weakens the claim:** GitHub API marks the commit unsigned (`verified=false`, `reason=unsigned`); this verifies tag/ref and content identity, not a signed-commit authenticity claim.
- **Could not verify:** the grep output captured for `man7-proc_pid_fdinfo.5.html` was truncated before its decisive footer line; exact release evidence was obtained for both requested inotify pages, and the named proc-fdinfo page was searched but its version footer was not independently captured in the receipt. The host kernel version is current command output, not a historical kernel measurement.
- **Checks not run:** no build, lint, or tests (not applicable to this evidence-only assignment).

## Deliverables
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ExecTagPin/receipts/tag-pin-a2.txt`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ExecTagPin.md`
