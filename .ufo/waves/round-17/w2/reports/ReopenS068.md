# ReopenS068 — row S068 (hypridle v0.1.8 `src/main.cpp`)

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; HEAD
`988b858bd6049bc709807534fd725c05264f7e60` (verified with `git log -1`).
`git diff` over `corpus/SOURCES.md`, `corpus/lessons/round-17.md` and
`corpus/knowledge/idle-lock-route-r17.md` is empty, so the worktree bytes read
are the HEAD blobs. Registry rows at HEAD: 70 (the gate's 55 → 70 holds).

## Verdict

**PASS — no falsification found.** URL, anchor quote, digest, tier/status, the
row's teaches claim, and the citing note's single S068-derived claim all hold
against independently fetched bytes. Two precision observations below are
anchor-range/wording under-inclusions, not false claims.

## Receipts (independent re-open)

| check | observation |
|---|---|
| fetch | `curl -sSL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp` → HTTP 200, 2587 bytes, 75 lines |
| sha256 | `379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38` — equal to SOURCES cell and gate cell (programmatic string compare, both `True`) |
| tag-pinning | codeload `refs/tags/v0.1.8` tarball `hypridle-0.1.8/src/main.cpp` is `cmp`-identical to the raw fetch, same digest — the tag path is not a moving alias for different bytes |
| tag selection | `https://github.com/hyprwm/hypridle/releases/latest` → 302 `.../releases/tag/v0.1.8`; GitHub REST API returns 403 (rate limit), matching the note's own statement that the API was not used |
| row location | `corpus/SOURCES.md:80` (11 cells); unique S068 row |
| gate location | `corpus/lessons/round-17.md:55`; unique S068 gate row; both identical in `git show HEAD:...` |

## Row verification (`SOURCES.md:80`)

| field | value | result |
|---|---|---|
| source | `hypridle src/main.cpp @ v0.1.8 — https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp` | URL byte-identical to gate URL; 200 |
| kind / tier | `code` / `A` | consistent with gate preamble (tag-pinned upstream source) |
| anchor | `file lines 55-63; sha256 379bf…a38` | digest correct; range contains the quote line (see F1) |
| teaches | "a missing config is a fatal CRIT path, not a silent default" | **true**: `configCurrentPath.empty()` at line 57 → `Debug::log(CRIT, …)` line 61 → `return 1;` line 66, i.e. before `init()` line 69 and `CHypridle` line 71; no default config is installed |
| status | `mined` | used-by note exists and cites the row |
| opened / recheck | `2026-10-20` / `on-change` | matches round date and gate preamble |
| used-by | `corpus/knowledge/idle-lock-route-r17.md` | note line 1 carries S068 as positional token 6; inverse mapping holds |

Gate quote at its stated anchor, verbatim:

```
L61 =             Debug::log(CRIT, "ConfigManager: No hypridle.conf file found in:");
```

`"No hypridle.conf file found in:"` is a verbatim substring at `[HM:61]`, 5
words (≤25). The gate's anchor convention `[HM:n] = file line` is stated at
`idle-lock-route-r17.md:24` and resolves correctly.

## Citing-note claims from S068

`corpus/knowledge/idle-lock-route-r17.md:50` is the only line that draws on
S068:

> `hypridle.conf` lookup: missing file logs "No hypridle.conf file found in:" [HM:61]

- The log-excerpt claim is **true** at line 61 (default lookup branch, no `-c`).
- The adjacent "A config file is required; hypridle won't run without one."
  sentence is attributed to `[HW:7]` (S063 wiki), **not** to S068 — no
  over-attribution.
- "Config path per [HW:6]" is likewise wiki-attributed. The note makes no other
  S068 claim.

## Findings (non-falsifying)

- **F1 — anchor range under-inclusive.** The row's range `file lines 55-63`
  ends at the "Create a config or specify one manually:" line and omits
  `return 1;` (line 66), which is the evidence for the word "fatal" in the
  row's teaches cell. The range still contains the located quote (line 61), and
  the verdict is true at lines 57-67, so this is a range-precision defect, not a
  false claim. If the row is ever touched, `55-67` (or `57-66`) is exact.
- **F2 — scope word "lookup".** `main.cpp` constructs `CConfigManager(configPath)`
  (line 55) and tests `configCurrentPath.empty()` (line 57); the directory search
  itself lives in `ConfigManager.cpp`, not in this file. The row's "config
  lookup" is therefore the startup/failure half of the lookup. Shorthand, not a
  false claim; the note's failure-log statement is exactly what the file shows.
- **F3 — gate quote prefix.** The literal is `"ConfigManager: No hypridle.conf
  file found in:"`; the gate quotes the sentence after the prefix. Verbatim
  excerpt, same pattern as S065/S066/S067 — not a defect.

## Attacks attempted (all failed)

Tag-alias/byte substitution (raw vs tag tarball), digest typo (full 64-hex
compare in both files against computed hash), anchor drift (`[HM:61]` vs actual
line 61), claim overreach by the note (none found), used-by inverse mapping
(S068 ↔ note token 6), and row-count consistency (70 at HEAD). None produced a
counterexample; the row stands as written.

## Constraints

Installs: **none**. No package/sudo/systemctl/compositor/device/version probes;
no git mutation, no jj; no delegation. `/var/log/pacman.log` read as bytes only
(`:1792` hypridle 0.1.8-2, `:1798` hyprlock 0.9.6-3 — corroborates the tag
version binding).
