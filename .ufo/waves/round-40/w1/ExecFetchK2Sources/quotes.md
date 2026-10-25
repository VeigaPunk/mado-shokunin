# ExecFetchK2Sources — located quotes for K2 (`host-producer-outputs-r29`)

Seat: ExecFetchK2Sources, round 40 / w1. Target: assimilation candidate K2 =
`merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md` (source repo shokuknow, read-only,
never written). K2's own subject: the omarchy v3.8.4 Waybar indicator scripts S237 / S238.

All paths absolute. Every quote below is `grep -F` verified against the fetched bytes; `rc=0` and the
line number are printed by `grep -Fn`. Fetch date 2026-10-25.

## 1. Fetch receipt (exact bytes, upstream)

| S-id | destination | HTTP | Date header | SIZE | sha256 | curl exit |
|---|---|---|---|---|---|---|
| S237 | `.ufo/waves/round-40/fetch/omarchy-v3.8.4-screen-recording.bin` | 200 | Sun, 25 Oct 2026 20:49:07 GMT | 169 | `28491cd3fdaaea78143432d6e2d5b609f06f90e420874d8bdd83a25a199bc63c` | 0 |
| S238 | `.ufo/waves/round-40/fetch/omarchy-v3.8.4-notification-silencing.bin` | 200 | Sun, 25 Oct 2026 20:49:07 GMT | 174 | `312900d1a9ca772e944e626d86cb54af6dec4dd5619510ecb262562da9d6de69` | 0 |

Effective URLs (no redirect):
`https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/screen-recording.sh`,
`.../notification-silencing.sh`. Per-file header receipts sit beside each `.bin` as `*.bin.http.txt`
(`DATE_UTC` = ISO-8601 form of the response `Date` header, `DATE_RAW` = that header verbatim,
`HTTP_STATUS`, `SIZE`, `SHA256`, `EFFECTIVE_URL`, `CURL_EXIT`).

Shape: both files are `Bourne-Again shell script, Unicode text, UTF-8 text executable`, 7 lines, last
three bytes `66 69 0a` (trailing newline present, no CRLF).

## 2. Host copies and host-vs-upstream comparison

Host tree `/home/vgpnk/.local/share/omarchy/default/waybar/indicators/` (read-only; bytes copied, tree
never written):

| host file | copy | sha256 | mode |
|---|---|---|---|
| `screen-recording.sh` | `.ufo/waves/round-40/fetch/host-indicator-screen-recording.bin` | `28491cd3…a199bc63c` | 755 |
| `notification-silencing.sh` | `.ufo/waves/round-40/fetch/host-indicator-notification-silencing.bin` | `312900d1…9d6de69` | 755 |

`cmp` results, all rc=0 (four comparisons, two directions):

```
cmp upstream-screen-recording       host-indicator-screen-recording      -> SCREEN_RECORDING_IDENTICAL
cmp upstream-notification-silencing host-indicator-notification-silencing -> NOTIFICATION_SILENCING_IDENTICAL
cmp $HOME/.local/share/omarchy/.../screen-recording.sh       upstream-screen-recording        -> HOSTDIR_SCREEN_IDENTICAL
cmp $HOME/.local/share/omarchy/.../notification-silencing.sh upstream-notification-silencing  -> HOSTDIR_NOTIF_IDENTICAL
```

**Host == upstream byte-for-byte for both scripts** (169 B / 174 B, identical sha256). This is the
difference from the *config* byte gap the registration already holds (6354 B host vs 5114 B upstream):
the indicator scripts carry no host-vs-upstream difference at all.

Tag-sensitivity check (fetched for this receipt into the seat dir, `v3.8.3-*.bin`): upstream **v3.8.3**
serves the *same* sha256 for both files, so the identity is not an artifact of the tag choice.

Host git state (read-only): `HEAD = 8fcc9d6048af4cb0e3af8512c78049857a3b53dd`,
`describe --tags = v3.8.4`, `git status --porcelain -- default/waybar/indicators` empty,
`git show v3.8.4:<path> | sha256sum` reproduces both hashes above. Caveat: the host tree's `version`
file still reads `3.8.3` while the checkout is at tag `v3.8.4` — the `version` file lags the tag; it is
not a disagreement with the S237/S238 `tag v3.8.4` locator.

## 3. Located quotes (3–25 words, verbatim, line numbers)

Convention: an indented source line is quoted without its two leading spaces (insignificant shell
indentation); each quote is verified as an exact `grep -F` substring of the numbered line (`rc=0`). The
two probe lines carry no indentation and therefore match the line byte-for-byte.

### S237 — `screen-recording.sh` (probes a **process**: `pgrep -f "^gpu-screen-recorder"`)

- line 3 — 6 words — `if pgrep -f "^gpu-screen-recorder" >/dev/null; then` — the whole probe: a
  `pgrep -f` on the full command line, anchored at start-of-line, so a recorder is detected only when
  argv[0] begins with `gpu-screen-recorder`. Read-only; the script runs nothing but `pgrep`.
- line 4 — 8 words — `echo '{"text": "󰻂", "tooltip": "Stop recording", "class": "active"}'` — the
  positive branch: one Waybar JSON object, single non-ASCII glyph U+F0EC2 as `text`, class `active`
  (line 4 is 70 chars).
- line 6 — 3 words — `echo '{"text": ""}'` — the negative branch: empty `text`, no tooltip, no class.

### S238 — `notification-silencing.sh` (probes a **query**: `makoctl mode`)

- line 3 — 8 words — `if makoctl mode | grep -q 'do-not-disturb'; then` — the whole probe: one
  `makoctl mode` read piped into `grep -q` for the substring `do-not-disturb`; a substring test, not an
  equality test on the mode name.
- line 4 — 8 words — `echo '{"text": "󰂛", "tooltip": "Notifications silenced", "class": "active"}'` —
  positive branch, single non-ASCII glyph U+F009B as `text`, class `active` (line 4 is 78 chars).
- line 6 — 3 words — `echo '{"text": ""}'` — negative branch, byte-identical to S237 line 6.

Both scripts are 7 lines and share the identical skeleton: shebang, blank, one probe, positive JSON,
`else`, empty JSON, `fi`. Neither script writes, sets, or dispatches anything: S237's only external
program is `pgrep`; S238's are `makoctl mode` (read) and `grep -q`.

## 4. Candidate carry check (`host-producer-outputs-r29.md`)

Marking rule used: **REPRODUCED** = the quoted text occurs verbatim at the named location;
**DIFFERENT** = the location exists and the same construct occurs with changed bytes/values;
**ABSENT** = not found. The candidate wraps every quote in a `> "…"` blockquote and escapes inner
double quotes as `\"`, so a literal byte match is impossible by construction; marking is done on the
unescaped quote content.

| cand. line | S-id | quote (unescaped) | words | verdict | located at |
|---|---|---|---|---|---|
| 21 | S237 | `if pgrep -f "^gpu-screen-recorder" >/dev/null; then` | 6 | **REPRODUCED** | `screen-recording.bin:3`, `grep -F` rc=0 |
| 25 | S238 | `if makoctl mode \| grep -q 'do-not-disturb'; then` | 8 | **REPRODUCED** | `notification-silencing.bin:3`, `grep -F` rc=0 |
| 29 | S240 | `"""Cache AI CLI usage windows and render a Waybar chip. waybar reads cache only."""` | 14 | **REPRODUCED** | `~/.local/bin/ai-usage:2` (symlink → `Projects/omarchy-usage-tray/bin/ai-usage`), rc=0 |
| 35 | S241 | `"updated_at": "2026-10-23T22:52:44Z",` | 2 | **DIFFERENT** | `~/.cache/ai-usage/status.json:3` now reads `"updated_at": "2026-10-25T20:47:13Z",` |
| 50 | S239 | `from gkeep.cli import main` | 4 | **REPRODUCED** | `~/.local/bin/gkeep:9` (symlink → `Projects/gkeep/bin/gkeep`, 252 B), rc=0 |
| 55 | S240 | `return Path(os.environ.get("AI_USAGE_CACHE", Path.home() / ".cache/ai-usage/status.json"))` | 5 | **REPRODUCED** | `~/.local/bin/ai-usage:64`, rc=0 |

The two K2-scope quotes (lines 21, 25) are **REPRODUCED verbatim**. Lines 29/50/55 (S239/S240) are
adjacent to K2 but re-checked here because the candidate carries them; they reproduce too.

### Three candidate claims that do not reproduce as stated

- **S241 timestamp (candidate line 35) is a rotated volatile value.** The construct reproduces, the
  value does not: `2026-10-23T22:52:44Z` vs the current `2026-10-25T20:47:13Z`. This is the same
  fabrication-class false positive the round-39 lesson corrected (a rotated volatile timestamp), and a
  quote of this field cannot be stable across rounds — the candidate's `recheck: 90d` cannot hold for it.
- **That same quote is only 2 words**, below the 3-word floor of the 3–25 word quote rule, so it is
  under-specified even where it does match. The two K2 quotes are 6 and 8 words and sit inside the band.
- **S240 file size drifted.** Candidate §2 states the `ai-usage` program is `134 777 B`; the resolved
  target today is `114 246 B` (`stat -L`). The quote still reproduces; the size claim does not.

### Candidate's measured host facts, re-derived only where allowed

- `pgrep -f "^gpu-screen-recorder"` → rc=1 (no match) on `/usr/bin/pgrep` from procps-ng 4.0.7, and
  `pgrep -af gpu-screen-recorder` → rc=1. The binary `/usr/bin/gpu-screen-recorder` *is* installed, so
  the chip's negative branch is what renders now — consistent with candidate §1. This is a live
  process probe, so it is time-varying, not a durable fact.
- `makoctl mode` was **not** run: it opens the mako daemon socket, and this seat is barred from socket
  connects of its own. The candidate's "`makoctl mode` reports `default`" is therefore **not
  re-derived here** (declared gap, not a contradiction).
- Harness note: in this seat's shell `pgrep` resolves to a shell builtin (`type -a pgrep`), while the
  script runs under `#!/bin/bash` and resolves `/usr/bin/pgrep`. Only the `/usr/bin/pgrep` result above
  is evidence about the script's behaviour.

## 5. Scope of this receipt

Written only under `.ufo/waves/round-40/` (the two named `.bin` + `.http.txt` pairs in `fetch/`, the two
`host-indicator-*.bin` copies, and this seat dir). No config tree, compositor verb, package
transaction, git mutation or shokuknow write. Compositor verbs used: none. Read-only git used:
`rev-parse`, `describe`, `status --porcelain`, `show` on `~/.local/share/omarchy`.
