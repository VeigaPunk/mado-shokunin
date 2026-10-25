# ExecFetchK2Sources — K2 receipts (omarchy v3.8.4 Waybar indicator scripts)

Seat: ExecFetchK2Sources, mado round 40 / w1. Scope: receipts for assimilation candidate K2
(`merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md`, sources S237/S238 — the
`screen-recording.sh` / `notification-silencing.sh` Waybar indicator producers).

## Files written (all inside the lane)

| path (relative to `mado-shokunin/`) | what |
|---|---|
| `.ufo/waves/round-40/fetch/omarchy-v3.8.4-screen-recording.bin` | upstream bytes, 169 B, sha256 `28491cd3…a199bc63c` |
| `.ufo/waves/round-40/fetch/omarchy-v3.8.4-screen-recording.bin.http.txt` | HTTP 200, `DATE_UTC=2026-10-25T20:49:07Z`, SIZE, SHA256, effective URL, curl exit 0 |
| `.ufo/waves/round-40/fetch/omarchy-v3.8.4-notification-silencing.bin` | upstream bytes, 174 B, sha256 `312900d1…9d6de69` |
| `.ufo/waves/round-40/fetch/omarchy-v3.8.4-notification-silencing.bin.http.txt` | same fields |
| `.ufo/waves/round-40/fetch/host-indicator-screen-recording.bin` | host copy, 169 B, mode 755 |
| `.ufo/waves/round-40/fetch/host-indicator-notification-silencing.bin` | host copy, 174 B, mode 755 |
| `.ufo/waves/round-40/w1/ExecFetchK2Sources/quotes.md` | located quotes, candidate carry marking, host-vs-upstream comparison |
| `.ufo/waves/round-40/w1/ExecFetchK2Sources/v3.8.3-{screen-recording,notification-silencing}.bin` | tag-stability evidence (see finding 3) |
| `.ufo/waves/round-40/w1/ExecFetchK2Sources.md` | this report |

No tracked file edited; nothing written outside `.ufo/waves/round-40/`. shokuknow (candidate repo) was
read only. `/tmp` header scratch removed.

## Behavior / result

Both upstream scripts fetched with `curl -sS -L` from
`https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/{screen-recording,notification-silencing}.sh`
— HTTP **200**, curl exit **0**, no redirect (`%{url_effective}` equals the request URL), server `Date`
`Sun, 25 Oct 2026 20:49:07 GMT`, sizes 169 / 174 B, 7 lines each, trailing newline `0a`, no CRLF.

Host files `~/.local/share/omarchy/default/waybar/indicators/{screen-recording,notification-silencing}.sh`
copied byte-exact. **`cmp` in both directions returns 0 for both files — the host scripts are
byte-identical to upstream v3.8.4** (same sha256, same size). This is not the case the registration
already holds for the *config* (6354 B host vs 5114 B upstream); for these two indicator scripts there
is no host-vs-upstream difference to explain.

## Located quotes (each `grep -F` verified, `rc=0`)

`screen-recording.sh` — probes a **process**, `pgrep -f "^gpu-screen-recorder"`:

- `:3` (6 words) `if pgrep -f "^gpu-screen-recorder" >/dev/null; then`
- `:4` (8 words) `echo '{"text": "󰻂", "tooltip": "Stop recording", "class": "active"}'` (glyph U+F0EC2)
- `:6` (3 words) `echo '{"text": ""}'`

`notification-silencing.sh` — probes a **query**, `makoctl mode | grep -q 'do-not-disturb'`:

- `:3` (8 words) `if makoctl mode | grep -q 'do-not-disturb'; then`
- `:4` (8 words) `echo '{"text": "󰂛", "tooltip": "Notifications silenced", "class": "active"}'` (U+F009B)
- `:6` (3 words) `echo '{"text": ""}'`

S238's probe is a substring test (`grep -q`), not an equality test on the mode name; S237's anchor is
`^gpu-screen-recorder` on the full command line, so argv[0] must *begin* with that name. Neither script
writes, sets, dispatches or reloads anything; both are 7-line, structurally identical skeletons.

## Candidate carry check (`host-producer-outputs-r29.md`)

Rule: REPRODUCED = quoted text occurs verbatim at the named location; DIFFERENT = same construct, changed
bytes/values; ABSENT = not found. The candidate escapes inner `"` as `\"` inside `> "…"` blocks, so
marking is done on unescaped content.

| cand. line | S-id | verdict | evidence |
|---|---|---|---|
| 21 | S237 | **REPRODUCED** | `screen-recording.bin:3`, `grep -F` rc=0 |
| 25 | S238 | **REPRODUCED** | `notification-silencing.bin:3`, `grep -F` rc=0 |
| 29 | S240 | **REPRODUCED** | `~/.local/bin/ai-usage:2` (symlink → `Projects/omarchy-usage-tray/bin/ai-usage`), rc=0 |
| 35 | S241 | **DIFFERENT** | `~/.cache/ai-usage/status.json:3` now `"updated_at": "2026-10-25T20:47:13Z",` (candidate: `2026-10-23T22:52:44Z`) |
| 50 | S239 | **REPRODUCED** | `~/.local/bin/gkeep:9` (symlink → `Projects/gkeep/bin/gkeep`, 252 B), rc=0 |
| 55 | S240 | **REPRODUCED** | `~/.local/bin/ai-usage:64`, rc=0 |

The two K2-scope quotes (21, 25) reproduce verbatim, both inside the 3–25 word band.

## Findings that bear on the assimilation gate

1. **Host == upstream for both indicator scripts** (four `cmp` runs rc=0; sha256 equal). Any K2 statement
   that treats these producer scripts as a host-vs-upstream divergence is unsupported; the divergence
   lives in the waybar *config*, not here.
2. **S241's quoted timestamp is a rotated volatile value** — the construct reproduces, the value does
   not (2026-10-23 vs 2026-10-25). Same fabrication-class false positive the round-39 lesson corrected.
   A 90-day recheck cannot hold for a quote of that field.
3. **Tag stability:** upstream **v3.8.3** serves the same sha256 for both scripts, so the identity in
   finding 1 is not an artifact of the v3.8.4 tag. Host checkout is at `HEAD 8fcc9d60…`, `describe
   --tags = v3.8.4`, `git status --porcelain -- default/waybar/indicators` empty, and
   `git show v3.8.4:<path>` reproduces both hashes. Caveat: the host tree's `version` file reads `3.8.3`
   while the checkout is tagged `v3.8.4` — the version file lags the tag; it does not contradict the
   S237/S238 locator.
4. **S240 size drift:** candidate §2 says `ai-usage` is `134 777 B`; resolved target is `114 246 B`
   (`stat -L`). The quote still reproduces; the size claim no longer does.
5. **The S241 quote is only 2 words** — below the 3-word floor of the 3–25 word quote rule.
6. **S237's negative branch is what renders now:** `/usr/bin/pgrep -f "^gpu-screen-recorder"` → rc=1 and
   `pgrep -af gpu-screen-recorder` → rc=1 (procps-ng 4.0.7), while `/usr/bin/gpu-screen-recorder` *is*
   installed. Live process probe ⇒ time-varying, consistent with candidate §1 at this instant.
7. Harness artifact worth recording: in this seat's shell `pgrep` resolves to a shell builtin
   (`type -a pgrep`), while the scripts run `#!/bin/bash` and resolve `/usr/bin/pgrep`. Only the
   `/usr/bin/pgrep` result is evidence about script behaviour.

## Not run (declared gaps, not contradictions)

- `makoctl mode` — it opens the mako daemon socket, and this seat is barred from socket connects of its
  own. The candidate's "`makoctl mode` reports `default`" is therefore not re-derived here.
- No compositor verb, no package transaction, no git/jj mutation, no config-tree write.

## Tool installs

None (no install or update performed; `curl`, `cmp`, `grep`, `sha256sum`, `stat`, `python3` already
present).

## Checks for the main agent

- `sha256sum .ufo/waves/round-40/fetch/omarchy-v3.8.4-*.bin` → `28491cd3…` (169 B) / `312900d1…` (174 B).
- `cmp` each `.bin` against its `host-indicator-*.bin` → rc=0.
- `grep -Fn 'if pgrep -f "^gpu-screen-recorder" >/dev/null; then'` and
  `grep -Fn "if makoctl mode | grep -q 'do-not-disturb'; then"` on the fetched bytes → line 3 each.
- Read `.ufo/waves/round-40/w1/ExecFetchK2Sources/quotes.md` for the full quote table and marking rule.

Note: `.ufo/waves/round-40/fetch/host-k2-reads.txt` (3869 B) in the same directory is **not** mine — it
appeared during my run from another seat; I neither wrote nor modified it.
