# Attack — Version binding bullets (P4 terminal route, P6 idle/lock route)

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD `988b858`.
Targets: `corpus/knowledge/terminal-route-r17.md:113-118` (HEAD `a9998d1`;
the identical bullet text sits at worktree lines 114-119 under a concurrent,
uncommitted peer edit that does not touch it — `git diff -U0 | grep
'Version binding\|pacman.log'` is empty, and a `diff` of HEAD 113-118 against
worktree 114-119 prints `IDENTICAL`) and
`corpus/knowledge/idle-lock-route-r17.md:109` (worktree = HEAD, no diff).

**Verdict: attack failed. Every clause of both bullets verifies against
`/var/log/pacman.log` by file read. No line-number, version, date, or
"no later line" mismatch exists.** The upstream-tag half of each bullet also
verifies (tags live, raw bytes hash to the SOURCES values). Remaining items are
wording/attribution nuances, not factual defects.

Method: file bytes only — `grep -n`, `sed -n`, `sha256sum`, `wc`, `stat`, and
`curl` for tag-pinned raw bytes. No pacman/yay/paru, no sudo, no service,
compositor, input or package query. Installs: **none**. Log read is
`/var/log/pacman.log`, 3160 lines, sha-relevant extent only.

## Receipts

Log state at read: 3160 lines, `mtime=2026-10-20 09:39:21.639895809 -0300`,
last line `[2026-10-20T09:39:21-0300] … running 'gdk-pixbuf-query-loaders.hook'`.
No rotated `pacman.log.*` exists. An absolute grep for the four package names
returns exactly nine lines: `484` (the `-S` command list), `639`, `823`, `853`,
`1214`, `1792`, `1798`, `1946`, `2935` — so "no later line" claims are
exhaustive over the whole file.

### P4 clause 1 — alacritty

Claim: `installed alacritty (0.17.0-1)` (pacman.log:639, 2026-10-03), no later
alacritty line.

```
639:[2026-10-03T17:44:19-0300] [ALPM] installed alacritty (0.17.0-1)
```

- Line number 639 — exact.
- Version string `0.17.0-1` — exact.
- Date 2026-10-03 — exact (local `-0300`; 17:44:19).
- "No later alacritty line" — true; the only other mention is line 484, the
  preceding `pacman -S --noconfirm --needed … alacritty …` command
  (2026-10-03T17:42:38-0300). No `upgraded`, `reinstalled`, `downgraded` or
  `removed` alacritty event exists anywhere in the file.
- pkgver 0.17.0 matches the pinned tag `v0.17.0` (`releases/tag/v0.17.0` → 200;
  `extra/man/alacritty.5.scd` at that tag = 28787 bytes,
  sha256 `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107`,
  identical to SOURCES S058).

**Match.**

### P4 clause 2 — xdg-terminal-exec

Claim: `upgraded xdg-terminal-exec (0.14.3-1 -> 0.14.3-2)` (pacman.log:2935,
2026-10-20 09:16, a non-lane `-Syu`).

```
2935:[2026-10-20T09:16:46-0300] [ALPM] upgraded xdg-terminal-exec (0.14.3-1 -> 0.14.3-2)
```

- Line number 2935 — exact.
- Version transition `0.14.3-1 -> 0.14.3-2` — exact.
- Timestamp 09:16 — exact (`09:16:46-0300`).
- `-Syu` — verified by transaction membership: command header
  `2462:[2026-10-20T09:15:30-0300] [PACMAN] Running 'pacman -Syu --needed
  --noconfirm nvme-cli smartmontools fio xfsprogs pacman-contrib earlyoom
  iotop-c sysstat stress-ng btrbk linux-lts linux-lts-headers'`;
  `transaction started` at `2479:[2026-10-20T09:16:27-0300]`; next command
  header is line 3064. Line 2935 lies inside that transaction.
- Prior upgrade `1946:[2026-10-11T16:14:39-0300] upgraded xdg-terminal-exec
  (0.14.0-1 -> 0.14.3-1)` exists but does not disturb the claim: 0.14.3 is
  still the last logged pkgver.
- "non-lane": not a pacman.log field (the log records no actor). Consistent
  with the round's own record: the transaction predates round-17 launch
  (`0175f13` committed 2026-10-20T10:56:28-03:00) and `SCORECARD.md:893-894`
  states `/var/log/pacman.log:2440-3152` shows "13 non-lane runs on 2026-10-20
  07:45-09:39 (including `pacman -Syu`), none after round launch". The
  attribution is an inference from timing, not a log fact (see Residual risk).
- pkgver 0.14.3 matches pinned tag `v0.14.3` (`releases/tag/v0.14.3` → 200;
  `README.md` at that tag = 14762 bytes, sha256
  `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40`,
  identical to SOURCES S056). The host's `/usr/share/xdg-terminal-exec/
  xdg-terminals.list` is 1053 bytes, sha256
  `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034`, equal to
  upstream at v0.14.3 and to S060.

**Match.**

### P6 clause — hypridle and hyprlock

Claim: last logged events `upgraded hypridle (0.1.7-10 -> 0.1.8-2)` at
pacman.log:1792 and `upgraded hyprlock (0.9.6-1 -> 0.9.6-3)` at pacman.log:1798,
both 2026-10-11, no later line through 2026-10-20.

```
1792:[2026-10-11T16:14:32-0300] [ALPM] upgraded hypridle (0.1.7-10 -> 0.1.8-2)
1798:[2026-10-11T16:14:32-0300] [ALPM] upgraded hyprlock (0.9.6-1 -> 0.9.6-3)
```

- Line numbers 1792 and 1798 — exact.
- Versions `0.1.7-10 -> 0.1.8-2` and `0.9.6-1 -> 0.9.6-3` — exact.
- Dates both 2026-10-11 — exact (`16:14:32-0300`).
- "No later hypridle/hyprlock line through 2026-10-20" — true: the earlier
  mentions are the installs `823:[2026-10-03T17:44:21-0300] installed hypridle
  (0.1.7-10)` and `853:[2026-10-03T17:44:22-0300] installed hyprlock
  (0.9.6-1)` plus the line-484 command list; nothing after 1792/1798 through
  the file's last line (2026-10-20T09:39:21-0300).
- Last logged pkgver 0.1.8 / 0.9.6 matches tags `v0.1.8` / `v0.9.6`:
  `releases/latest` still redirects 302 → `…/tag/v0.1.8` and `…/tag/v0.9.6`
  (both tag URLs 200). Raw bytes at the tags hash to the SOURCES values:
  hypridle README `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6`
  (2598 B), `Hypridle.cpp` `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`
  (29880 B), `Hypridle.hpp` `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8`
  (3611 B), `main.cpp` `379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38`
  (2587 B), hyprlock README `83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3`
  (1458 B) — S065-S069.

**Match.**

## Mismatches

None. No counterexample found with an exact anchor.

## Wording observations (not factual defects)

1. P6 line 109 calls 1792/1798 "the last logged transactions" (plural). Both are
   package events inside one transaction: `transaction started` at
   `1424:[2026-10-11T16:14:18-0300]`, from the `-Syu` at
   `1414:[2026-10-11T16:13:19-0300]`. Anchors, versions and dates are
   unaffected; only the noun is loose.
2. P6's closing `[UNK]` "Host binary version of hypridle and hyprlock against
   the tags above" overlaps the binding. It is consistent under a strict
   reading (logged pkgver vs. running binary), but a skimming reader can take
   it as retracting the bullet.
3. P4's intro ("It does not establish … the installed Alacritty version")
   is scoped to the documentary route and is reconciled by the bullet's own
   `[UNK] the running binary`; the two sentences sit tensely but do not
   contradict each other.
4. "non-lane" in P4 is a round-window inference, not something `pacman.log`
   records (see Residual risk 1).

## Residual risk and verification gaps

1. Actor attribution. `/var/log/pacman.log` has no user/host field; the
   09:15:30 `-Syu` cannot be tied to an actor from the file. "non-lane" rests on
   the timestamp being before round launch (`0175f13`, 10:56:28-03:00) and on
   `SCORECARD.md:893-894`. If the round window were defined differently, the
   adjective would need re-derivation; the line/version/date facts would not.
2. Running binary. The log establishes the last logged package version only;
   both notes already mark the running binary `[UNK]`. Nothing here upgrades
   that to a runtime fact.
3. Arch packaging. pkgrel `-2`/`-3` can carry patches that diverge from the tag
   trees; both notes already mark this `[UNK]`, so the tag↔package identity is
   documentary, not a byte identity of the shipped binary.
4. Log extent. "No later line" is true for the file as read (last line
   2026-10-20T09:39:21-0300); a later append would age the clause, not falsify
   it as of this read.
5. Transcript check not performed: my item does not name the agent
   transcripts, so I verified the facts the notes cite, not the notes' authors'
   own read commands.
6. Concurrent edit. At read time (2026-10-20 ~11:57) the worktree held an
   uncommitted peer diff on `terminal-route-r17.md` (7 insertions, 6 deletions:
   S071 added to the `source:` line, compliance wording tightened, three host-
   table rows corrected). It does not touch the version-binding bullet: the
   `git diff -U0` grep for `Version binding|pacman.log` is empty and HEAD
   113-118 equals worktree 114-119. All findings here apply to that identical
   text; re-check line offsets after the wave lands.

## Environment

Reads used: `grep -n`, `sed -n`, `sha256sum`, `wc`, `stat`, `curl` (tag-pinned
raw bytes and `releases/latest` redirects), `git show/log/status` read verbs.
No package manager, service, compositor, input or live probe. Installs: none.
