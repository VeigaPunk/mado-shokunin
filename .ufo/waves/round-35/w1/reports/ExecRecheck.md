# ExecRecheck — round-35 fetch-receipt drift sweep (re-run 2026-10-24 ~23:28 -0300)

## Verdict

**No receipt has drifted.** All eight committed receipts reproduce byte-for-byte
when every constituent command is re-run against the live host today.

Baseline: `.ufo/waves/round-35/fetch/S203–S210.receipt.txt` are git-tracked,
committed in `19e4ab31` ("round-35: freeze C1 and C2 predicates, the clause
ledger, the control receipts and the re-issued blob ledger"). `git status` and
`git diff HEAD` over `fetch/` are empty — worktree bytes == committed bytes.

Method: each receipt was rebuilt into `/tmp/rr35/fresh/` by re-executing the
same probes that produced it (hashes, sizes, `cat -n` bodies, `journalctl
--user`, `pgrep`, `systemctl --user`, `ls`, `stat`, `grep` counts), then
`diff -u` committed-vs-fresh. All eight diffs came back clean; the rebuild
script is `/tmp/rr35/recheck.sh` (read-only; no receipt or host file touched).

## Differing lines

None. `diff -u` output per receipt: `(byte-identical)` ×8.

## Commands re-run per receipt (all outputs confirmed live)

| Receipt | Probes re-run | Result |
|---|---|---|
| S203 | `sha256sum` + `wc -c` + `cat -n` of `~/.local/share/omarchy/bin/omarchy-first-run` (hash `20508471…`, 1089 B, 28 lines); `find install/first-run -name '*.sh' \| wc -l` → 12; `ls install/first-run` → 13 entries | identical |
| S204 | `journalctl --user --no-pager \| grep -c 'omarchy-toggle'` → 0; journal first-5 grep → empty | identical |
| S205 | `pgrep -a -x hypridle` → `1667 /usr/bin/hypridle`; `pgrep -a -x hyprlock` → none; `systemctl --user is-active hypridle` → `inactive`; `journalctl --user … \| grep 'Started hypridle'` → the same two Oct-23 lines; `grep -n 'timeout'` and `sha256sum` on `hypridle.conf` (`e7d3b8dd…`) | identical |
| S206 | `sha256sum` + `wc -c` + `grep -n -A6 'custom/idle-indicator'` + `grep -c 'omarchy-toggle-idle'` on `~/.config/waybar/config.jsonc` (`a408a33d…`, 6354 B) | identical |
| S207 | `sha256sum` + `wc -c` + `cat -n` + `grep -c 'Idle lock disabled'` on `idle.sh` (`6d8d2c11…`, 159 B) | identical |
| S208 | `sha256sum` + `wc -c` + `grep -n 'Idle'` + `grep -c 'omarchy-toggle-idle'` on `omarchy-menu` (`d196b086…`, 33017 B) | identical |
| S209 | `ls`, per-copy `stat` mtime + `grep -c 'omarchy-toggle-idle'` over `config.jsonc.bak*` → 4 copies, all handler=1, oldest mtime `2026-10-03 17:44:32` (`.bak.1791314470`) | identical |
| S210 | `ls` + `grep -il 'idle'` on `~/.local/state/omarchy/toggles/hypr` → 2 files (`flags.conf`, `window-no-gaps.conf`), 0 idle | identical |

## Stability notes (pre-existing receipt quirks, re-observed — not drift)

- **S205**: process probe vs unit probe still disagree — `hypridle` runs as pid
  1667 while `systemctl --user is-active hypridle` prints `inactive` (it is not
  managed as a user unit; the receipt's "started in this session" claim rests on
  the journal lines alone). Both probes reproduce exactly as committed.
- **S203**: `install/first-run/` lists 13 entries; the `.sh`-only count is 12 —
  `install-voxtype.hook` is the 13th entry, installed via `omarchy-hook-install`
  rather than `bash`. Consistent with the committed receipt.
- **S209**: the receipt's "oldest dated copy" path line shows
  `config.jsonc.bak` (alphabetically first) while its `stat` line correctly
  shows `…bak.1791314470` @ `2026-10-03 17:44:32.097653608 -0300` — this
  resolves the round's 2026-10-03 vs 2026-10-06 question in favor of
  **2026-10-03** per live `stat`. Re-observed unchanged today.
