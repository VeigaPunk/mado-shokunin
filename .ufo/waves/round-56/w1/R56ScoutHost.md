# R56ScoutHost — w1 read-only host recon (2026-10-28)

Seat: confirm the committed round-56 host pins still describe the live host, capture the
process/stat/log-shape facts, and say what the reload count can and cannot show.
All work read-only; no hyprctl keyword/dispatch/reload; no writes outside the seat dir;
scratch `/fast/scratch/hyaku/mado-r56/R56ScoutHost/` used and removed.

## Verdict in one line

ALL FOUR HOST PINS BYTE-EQUAL against the live host; pins at freeze commit `3423ae2` hash-match
the working tree and `frozen-tables.json c1.host_pin_sha256`. The pins are current.

## 1. Pin currency (fresh capture vs committed pin)

Pins live at `.ufo/waves/round-56/fetch/` in the lane. Their sha256 values were first checked
against the frozen tables (all four match `c1.host_pin_sha256` exactly), then each pin was
re-fetched live and byte-compared.

Commands (fresh side; diff side `cmp -s pin fresh`):

```
hyprctl getoption misc:disable_autoreload -j
hyprctl version -j
grep -E '^source' ~/.config/hypr/hyprland.conf
stat -c '%F' <each of the 40 reference-watched paths, pin order>
```

| pin | result | decisive output |
|---|---|---|
| `host-getoption.json` | **BYTE_EQUAL** | `GETOPTION_BYTE_EQUAL` (rc 0, no diff) |
| `host-version.json` | **BYTE_EQUAL** | `VERSION_BYTE_EQUAL` (rc 0, no diff) |
| `host-sources.txt` | **BYTE_EQUAL** | `SOURCES_BYTE_EQUAL` (rc 0, no diff); 18 `source =` lines |
| `host-watched-lstat.txt` | **BYTE_EQUAL** | `WATCHED_LSTAT_BYTE_EQUAL`; all 40 paths `regular file`, same order |

Provenance (read-only git):

```
for p in host-getoption.json host-version.json host-sources.txt host-watched-lstat.txt; do
  git -C <lane> show 3423ae285676c2a10273000f4519163472b443db:.ufo/waves/round-56/fetch/$p | sha256sum
done
```

gives `7aa0fbf9…`, `124716ed…`, `738b5945…`, `23623a92…` — identical to the working-tree pins and
to `c1.host_pin_sha256` in `frozen-tables.json`. Commit `3423ae2` = "round-56: freeze claims,
registration, frozen tables, fixtures, controls, pins, baselines" (2026-10-28 21:19:17 -0300).

Content notes (not defects):
- `host-getoption.json`: `{"option": "misc:disable_autoreload", "int": 0, "set": false }` — value 0
  AND `set:false` (option not present in the config tree; hyprlang default 0). For C1/C2 semantics
  this means autoreload is **on** (`disable_autoreload` unset ⇒ 0 ⇒ non-zero test fails).
- `host-version.json`: commit `efb50993780079460b0cbed1363e2166a2de1d9f`, version/tag `v0.56.2`,
  dirty false, hyprlang 0.6.8 — matches registration §C1's pinned commit.
- The running instance dir under `$XDG_RUNTIME_DIR/hypr/` is
  `efb50993780079460b0cbed1363e2166a2de1d9f_1793027319_436109330` — the running compositor names
  the same commit the pin declares.

## 2. Fresh captures written to the seat dir

Saved under `.ufo/waves/round-56/w1/R56ScoutHost/`:

| file | content | value |
|---|---|---|
| `hyprland-lstart.txt` | `ps -o lstart= -p $(pgrep -o Hyprland)` (pid 1622) | `Mon Oct 26 12:08:38 2026` |
| `hyprland-conf-stat.txt` | `stat -c '%y %F' ~/.config/hypr/hyprland.conf` | `2026-10-17 17:02:56.289181525 -0300 regular file` |
| `hypr-reload-shape.txt` | log shape, script `logshape.py` (count + last timestamp only) | `/run/user/1000/hypr/efb5099…_1793027319_436109330/hyprland.log: reload_lines=0 last_reload_ts=none` |
| `getoption.now.json` | fresh `hyprctl getoption … -j` | byte-equal to pin |
| `version.now.json` | fresh `hyprctl version -j` | byte-equal to pin |
| `sources.now.txt` | fresh `source` lines | byte-equal to pin |
| `watched-lstat.now.txt` | fresh types of the 40 reference-watched paths | byte-equal to pin |

## 3. What the reload count can and cannot show about autoreload

Observed: `grep -c 'modified, reloading'` over the one live `hyprland.log` = **0**; no last-reload
timestamp exists.

- **Can show:** that in THIS compositor instance's lifetime (start `Mon Oct 26 12:08:38 2026`) the
  log marker Hyprland emits when it re-reads a config file after noticing a modification has never
  been printed — i.e. no config reload event was logged so far. This is consistent with the facts:
  `hyprland.conf` mtime is `2026-10-17 17:02` (before the compositor started) and `disable_autoreload`
  is 0, so with no modification there should be no reload.
- **Cannot show:**
  1. **That the watcher is armed.** Zero reloads is also exactly what a broken or never-registered
     inotify watch produces. Absence of reload evidence ≠ presence of watch evidence; proving the
     watch list needs the source-level model (C2's `tools/mado-watchplan.py`), not the log.
  2. **Why nothing reloaded** — unmodified config vs disabled autoreload vs suppressed logging are
     indistinguishable from the count alone. (Here `set:false, int:0` rules out the disabled case,
     but the count alone would not.)
  3. **Anything about previous sessions.** The log lives in a per-instance directory named with the
     commit and a boot-time nonce (`…_1793027319_436109330`); each compositor start starts a fresh
     log, so the counter is per-session, not cumulative.
  4. **A future save triggers a reload.** It is a historical count, not a liveness probe; a real
     probe would need a config write, which this seat is forbidden to perform.
  5. Completeness of the marker itself: the count trusts the literal string `modified, reloading`;
     a log-level/flag change or an upstream wording change would silently zero it.

## 4. Input defects / ambiguities found

None. All four pins are internally consistent (`frozen-tables.json c1.host_pin_sha256` = working
tree = freeze commit) and externally current (live host byte-equal). The only observation worth
carrying: the getoption pin records `"set": false` alongside `int 0`; any consumer that treats
`int==0` as "explicitly disabled" would be wrong — autoreload is on by default here.

## 5. Not verified / limits

- No filesystem event was generated and no reload was triggered (host guard: no config writes, no
  `hyprctl` mutations) — so watch liveness is unproven by design.
- Log read was shape-only by instruction: counts and one timestamp; no other log content was read
  or recorded.
- Hold-out fixtures H01-H08: not looked for, not found, not used. No seal breach observed.
- Tooling: no tools were installed or upgraded (pacman guard respected; nothing was needed).

## Report

.ufo/waves/round-56/w1/R56ScoutHost.md
