# SrcXdgTerminalExec — upstream xdg-terminal-exec (round 17, w1 scout)

Date: 2026-10-20. Scope: identify the latest upstream tag, fetch `README.md`
at that tag, record SHA-256 plus ≤25-word quotes on `xdg-terminals.list`
lookup paths/order, desktop-entry selection and fallback, and locate the
freedesktop proposed default-terminal spec it implements. Report only; no
lane file outside this report was written. No host mutation, no package
query, no live probe, no execution of any terminal tool.

Method: `git ls-remote --tags` (git protocol) and `git clone --depth 1
--filter=blob:none --branch v0.14.3` into `/tmp`, plus `curl` of
`raw.githubusercontent.com`. The GitHub REST API was attempted first and
returned HTTP 403 (`x-ratelimit-remaining: 0`), so no API metadata is used;
all identity claims below come from git refs and raw bytes.

## 1. Latest upstream tag

Repository: <https://github.com/Vladimir-csp/xdg-terminal-exec>
(default branch `master`; documented GitLab mirror
<https://gitlab.freedesktop.org/Vladimir-csp/xdg-terminal-exec>).

| Fact | Observed value |
|---|---|
| Tags enumerated (`git ls-remote --tags --refs`) | 21, range `v0.9.0` … `v0.14.3` |
| Latest tag (highest semver) | **`v0.14.3`** |
| Tagged commit | `065925df9f419008159258ae169018bfd23df71b` |
| Tag object type | `commit` (`git cat-file -t`), i.e. lightweight tag |
| Commit date | `2026-07-29T22:51:12+03:00` |
| Commit subject | `style: normalize function comments to be inside` |
| Remote `HEAD` (`git ls-remote --symref`) | `refs/heads/master` → `065925df…` — the tag commit, so no newer untagged commit |

Tag list (verbatim names, all lightweight per `--refs` output):
`v0.9.0 v0.9.1 v0.9.2 v0.9.3 v0.10.0 v0.10.1 v0.11.0 v0.11.1 v0.12.0
v0.12.1 v0.12.2 v0.12.3 v0.12.4 v0.13.0 v0.13.1 v0.13.2 v0.13.3 v0.14.0
v0.14.1 v0.14.2 v0.14.3`.

## 2. README fetched at the tag

- URL: <https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md>
- Access date: 2026-10-20. HTTP 200. 14,762 bytes / 337 lines.
- **SHA-256 `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40`**
  (of the raw bytes exactly as served).
- Cross-check: `git show v0.14.3:README.md` piped through `cmp` is byte-identical;
  git blob id `4f939aa405979be8568f79be85530f38e32b9263`. So the fetched raw
  document equals the tagged tree content, not a moving branch.

Supporting tag artifacts fetched from the same commit for the order detail:

| File at `v0.14.3` | Bytes / lines | SHA-256 |
|---|---|---|
| `xdg-terminal-exec.1.scd` (man page) | 186 lines | `3dba162f5502a3553bad9b2398ace10f7bc2456900c7c9ff62a436935876ec59` |
| `xdg-terminals.list` (low-priority default) | 1,053 B | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` |
| `xdg-terminal-exec` (POSIX shell implementation) | 1,499 lines / 44,020 B | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |

## 3. Verbatim quotes (each ≤25 words)

All anchors are line numbers in the raw `README.md` at `v0.14.3` unless
marked `MAN` (the `.1.scd` file). Quoted words are contiguous in the file;
backticks are part of the source.

| # | Topic | Quote | Anchor | Words |
|---|---|---|---|---|
| Q1 | What it is / spec reference | "Proposal for XDG Default Terminal Execution Specification and reference shell-based implementation." | README:3-4 | 11 |
| Q2 | Prose warning status | "backwards compatibility is maintained as best effort and is not guaranteed" | README:8-9 | 11 |
| Q3 | Config file names | "Configuration files are named `${desktop}-xdg-terminals.list` or `xdg-terminals.list` and placed in XDG config hierarchy." | README:100-101 | 13 |
| Q4 | `${desktop}` resolution | "`${desktop}` here is a lowercased string that can be matched (case-insensitively) against items of `$XDG_CURRENT_DESKTOP`" | README:103-105 | 15 |
| Q5 | Lookup order (prose) | "Default paths for configuration and data are resolved into (in order of decreasing priority):" | README:110-111 | 14 |
| Q6 | Priority composition | "A list of explicitly preferred entry IDs and fallback exclusions is composed by taking previously unseen IDs" | README:155-156 | 17 |
| Q7 | Per-dir order (man) | "In each directory, prefixed files are parsed first, in the order listed in _${XDG_CURRENT_DESKTOP}_." | MAN:87-88 | 14 |
| Q8 | Entry eligibility | "Entry eligible for selection should have `TerminalEmulator` Category and `X-TerminalArgExec=` key" | README:63-65 | 11 |
| Q9 | Applicability check | "presense of `TerminalEmulator` category" (spelling as in source) | README:167 | 5 |
| Q10 | Discard rule | "entry is discarded if it does not pass the checks" | README:170 | 10 |
| Q11 | Selection rule | "the first applicable entry is used" | README:171 and :178 | 6 |
| Q12 | Fallback trigger | "If no applicable entry is found, fallback selection is performed from entries in XDG data hierarchy" | README:172-173 | 16 |
| Q13 | Fallback disclosure | "the order in which found entries under the same base directory are checked in is undefined" | README:179-180 | 16 |
| Q14 | Terminal failure | "If no applicable entry is found, an error is returned." | README:181 | 10 |
| Q15 | Fallback exclusion | "`-terminal.desktop` excludes entry from fallback selection." | README:141 | 6 |
| Q16 | Exclusion protection | "`+terminal.desktop` protects entry from fallback exclusion." | README:143 | 6 |
| Q17 | Man: explicit pick | "The first listed, found, and valid Desktop Entry is used." | MAN:90 | 11 |
| Q18 | Man: fallback | "Otherwise fallback to the first found and valid Desktop Entry is performed." | MAN:92 | 12 |

Format lines for the config file (README:137-145), not quoted as prose:
`terminal.desktop` / `terminal.desktop:action` mark an explicit pick;
`-terminal.desktop` excludes from fallback; `+terminal.desktop` protects
against later exclusion.

## 4. Lookup paths, in documented decreasing priority

Verbatim list entries from README:112-123 (config) and :125-128 (entries;
continuation after the quote in Q5):

1. `${HOME}/.config/${desktop}-xdg-terminals.list`
2. `${HOME}/.config/xdg-terminals.list`
3. `/etc/xdg/${desktop}-xdg-terminals.list`
4. `/etc/xdg/xdg-terminals.list`
5. `/usr/local/share/xdg-terminal-exec/${desktop}-xdg-terminals.list`
6. `/usr/local/share/xdg-terminal-exec/xdg-terminals.list`
7. `/usr/share/xdg-terminal-exec/${desktop}-xdg-terminals.list`
8. `/usr/share/xdg-terminal-exec/xdg-terminals.list`
9. Desktop entries: `${HOME}/.local/share/applications/`,
   `/usr/local/share/applications/`, `/usr/share/applications/`.

Per the man page, inside each config directory prefixed
`${desktop}-…` files are parsed before the unprefixed `xdg-terminals.list`
(MAN:86-89). Directives begin with `/` and are not entry IDs
(README:147-150); `[+-]entry.desktop` only affects fallback.

Algorithm in one sentence (direct restatement of Q6-Q14): compose a
first-seen-wins explicit list from config dirs (per-desktop files in
`$XDG_CURRENT_DESKTOP` order, then plain `xdg-terminals.list`) and from
data-dir `xdg-terminal-exec/` fallbacks; take the first applicable entry
that passes Category plus desktop-entry validation (without `*ShowIn`);
otherwise fall back to data-hierarchy entries with `*ShowIn` honored, first
applicable wins, same-directory order undefined; else error.

## 5. Freedesktop proposed spec it implements

The README points at it directly (README:3-7):

> Proposal for XDG Default Terminal Execution Specification and reference
> shell-based implementation. The proposal PR can be found
> [here](https://gitlab.freedesktop.org/terminal-wg/specifications/-/merge_requests/3/diffs).

Located proposal (GitLab API, 2026-10-20):

| Fact | Observed value |
|---|---|
| Project | `terminal-wg/specifications` — "Terminals Working Group Specifications" (<https://gitlab.freedesktop.org/terminal-wg/specifications>), created 2019-01-03, last activity 2026-07-31 |
| Merge request | **!3 "Add xdg-terminal-exec"**, author `Vladimir-csp` |
| State | `opened` — **not merged** (`merged_at: null`); `detailed_merge_status: mergeable`; `blocking_discussions_resolved: true`; 81 notes |
| Dates | created `2019-01-29T17:56:18Z`, updated `2026-07-31T07:46:04Z` |
| Change | one new file `proposals/xdg-terminal-exec.md` (247 lines, `changes_count: 1`) |
| Head SHA | `64c429dfaf442d4a7ca9a656baf91a1b2d9c1a4d` (base/start `ba3a5e278f781aa5917b0f3878bb93b0fb3b51bb`) |
| Raw fetch | HTTP 200, 10,498 bytes, 247 lines, **SHA-256 `c16a717a0232d08402d53d8847c25c3de6ddf443760ec1ecdf6a3ee76ca8375a`** |
| On master? | HTTP 404 for `proposals/xdg-terminal-exec.md`; master `proposals/` holds only `template.md`, `accepted/` only `README.md` |

Proposal header bytes:
`* Name: xdg-terminal-exec` / `* Start Date: 2019-01-29` (spec:1-2).
Its "Default Terminal Execution Specification" section carries the same
three-part structure and the same priority algorithm as the README: a
byte-level `diff` of README:100-181 against spec:92-172 shows no textual
difference in that range other than the compared range's final line. Status
is therefore **proposal, never standard**; the README's own warning (Q2)
applies, and the MR has been open for over seven years.

## 6. Host cross-check (documentary file bytes only, for the P4 route)

Read as file bytes (`ls`, `cat`, `grep`, `sha256sum`); nothing was executed,
launched, or queried through a package manager. These are inputs to a
documentary route, not observed behaviour.

| Host path | Bytes / mtime | SHA-256 | Relation |
|---|---|---|---|
| `~/.config/xdg-terminals.list` | 127 B, 2026-10-03 17:44 | `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b` | Names `Alacritty.desktop`; comment: "The first found and valid terminal will be used" |
| `/usr/share/xdg-terminal-exec/xdg-terminals.list` | 1,053 B, root | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` | Byte-identical to tag default list (fallback exclusions + `/execarg_default:` directives) |
| `/usr/bin/xdg-terminal-exec` | 44,020 B / 1,499 lines, root, 2026-09-18 | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` | Byte-identical to `v0.14.3:xdg-terminal-exec` (`cmp`); parses `X-TerminalArgExec` at script:885 and legacy `X-ExecArg` at :893 |
| `~/.local/share/applications/Alacritty.desktop` | 452 B, user | — | `Categories=System;TerminalEmulator;`, `X-TerminalArgExec=-e`, `X-TerminalArgAppId=--class=`, `X-TerminalArgTitle=--title=`, `X-TerminalArgDir=--working-directory=` |
| `/usr/share/applications/Alacritty.desktop` | 374 B, root | — | `Categories=System;TerminalEmulator;`, `Exec=alacritty`; **no** `X-TerminalArgExec=` line |

Absent on host: `/etc/xdg/xdg-terminals.list`,
`/usr/local/share/xdg-terminal-exec/`, `/usr/local/bin/xdg-terminal-exec`.

Bounded consequence for the P4 route: the documented algorithm reads
`~/.config/xdg-terminals.list` first (position 2, above `/etc/xdg` and all
data-dir fallbacks), finds `Alacritty.desktop`, and resolves that entry ID in
`${XDG_DATA_HOME}` before `/usr/share`; the user entry there carries both the
`TerminalEmulator` category and `X-TerminalArgExec=-e`, satisfying the
README's eligibility clause (Q8). Label: **[INFERENCE]** from documented
order and file bytes — no launch was performed, so this is not an observation
that Alacritty starts. If the user entry were absent, the system entry lacks
`X-TerminalArgExec=` and would fail a strict eligibility read; the
implementation's compat mode (default, README:291-293) can still supply the
legacy `-e` default, so absence of the key alone cannot be claimed fatal.

## 7. Proposed SOURCES rows for L1 (id S0xx-pending)

Column layout copied from `corpus/SOURCES.md` header (11 columns).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx-pending | xdg-terminal-exec README — https://github.com/Vladimir-csp/xdg-terminal-exec (raw: https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md) | docs | A | XDG default-terminal selection: config lookup order, desktop-entry eligibility, fallback algorithm (ground for P4 terminal surface) | README.md @ v0.14.3 (commit 065925df…, 337 lines, sha256 c7a1a8bb…) :100-123, :137-181; man page :86-92 (sha256 3dba162f…) | Config order runs from `~/.config/${desktop}-xdg-terminals.list` through data-dir `xdg-terminal-exec` fallbacks; entries need `TerminalEmulator` plus `X-TerminalArgExec=`; explicit list is tried first, then data-hierarchy fallback, then error | mined | 2026-10-20 | 180d | corpus/knowledge/terminal-emulator-surface-p4.md (proposed) |
| S0xx-pending | freedesktop terminal-wg proposal — proposals/xdg-terminal-exec.md, MR !3 — https://gitlab.freedesktop.org/terminal-wg/specifications/-/merge_requests/3 | spec | A | proposal status and normative text this implementation follows | proposals/xdg-terminal-exec.md @ 64c429df… (247 lines, sha256 c16a717a…); MR opened 2019-01-29, updated 2026-07-31, not merged; absent on master (404) | The spec is still an unmerged proposal after seven years; its priority text is byte-equivalent to the README's, so neither can be cited as an accepted standard | mined | 2026-10-20 | on-merge | corpus/knowledge/terminal-emulator-surface-p4.md (proposed) |
| S0xx-pending | Host terminal resolver bytes — /usr/bin/xdg-terminal-exec and ~/.config/xdg-terminals.list | code | A | P4 terminal surface documentary route: which resolver and preference list the host carries | /usr/bin/xdg-terminal-exec (44,020 B, sha256 89f2be9a…), byte-identical to upstream v0.14.3; ~/.config/xdg-terminals.list (127 B, sha256 d035da57…) names `Alacritty.desktop`; ~/.local/share/applications/Alacritty.desktop carries `X-TerminalArgExec=-e` | Host resolver bytes equal upstream v0.14.3 and the user list names an entry whose user desktop file carries the required keys — documentary only, no launch observed | mined | 2026-10-20 | on-change | corpus/knowledge/terminal-emulator-surface-p4.md (proposed) |

## 8. Confidence

- Upstream latest tag, commit, digest, and README content: **high** — refs via
  git protocol, raw bytes hashed, raw compared byte-for-byte with the tag blob.
- Lookup/selection/fallback wording: **high** — contiguous quoted lines above,
  anchored.
- Freedesktop proposal identity/status: **high** — GitLab API fields plus raw
  head-SHA fetch and a 404 check on master.
- Host file identities and byte-equality with the tag: **high**.
- "The host would select Alacritty": **medium**, inference from the documented
  algorithm; runtime not observed.

## 9. Remaining unknowns

- Package identity/provenance of the installed `/usr/bin/xdg-terminal-exec`
  (which package or installer placed it, its package version): **[UNK]** — the
  host pause forbids any pacman query. Only its bytes are known.
- Whether any launcher, keybinding or DE integration actually invokes
  `xdg-terminal-exec` on this host, and with which `--dir`/`--hold` options:
  **[UNK]** — would require a live probe, out of scope.
- Whether the proposal MR will be merged; archived state as of 2026-10-20 is
  open/mergeable, not accepted.
- GitHub release notes / star metadata: not retrieved (REST API rate-limited);
  not needed for the tag/README claims.

## 10. Process compliance

- No `sudo`, `pacman`/`yay`/`paru` (not even `-Q`), `systemctl`, `hyprctl`,
  `libinput`, `evtest`, `wayland-info`, `hypridle`, `hyprlock`, `alacritty`,
  `waybar`, `walker`, `omarchy-*`, `notify-send`, screenshots or any live
  probe was run. `xdg-terminal-exec` was never executed.
- Host reads were `ls`/`cat`/`grep`/`sha256sum` on the two config/list paths
  and the two desktop entries; no credential or agent database was opened.
- Nothing installed or updated, so no tooling record is due.
- Network writes: none; the only clone is a throwaway shallow repository in
  `/tmp`. The sole lane write is this report.
