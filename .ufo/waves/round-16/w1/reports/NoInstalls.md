# NoInstalls — mado round 16, wave w1 (reviewer, leaf)

Seat: `MadoR16.NoInstalls`. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: install prohibition precedence over the generic tooling directive; open
safety debt. Method: source and committed-file reading, plus a passive read of
`/var/log/pacman.log`. No package, service, compositor or input operation was
run. No install, update, downgrade, `-Sy`/`-Syu`/`-U`/`-R`, or service restart.
No `~/.omp/agent/agent.db*` or credential file was opened. No sibling file was
edited.

## Verdict

1. **Precedence: the round-16 prohibition governs this round.** The generic
   "install without asking" directive does not authorise installs in this round.
   This seat installed nothing and records no tool install or update.
2. **Safety debt: open.** The round-15 forbidden partial upgrade (libinput
   1.31.3-1 → 1.32.0-1) is unremediated. Remediation is operator-owned (L0).
3. **No round-16 package transaction observed** in `/var/log/pacman.log` up to
   its last entry, `2026-10-20T04:25:21-0300` (line 2439). This is a log-read
   observation, not a live package-state query.
4. **Missing prerequisites: none for this round.** `/usr/bin/python3`
   (3.14.7) and `/usr/bin/git` are present. The stdlib-only deliverables
   (`tools/mado-action-plan.py`, `measure.py`) need nothing further. Nothing was
   installed to obtain these.

## Why the round prohibition takes precedence

- **Specificity.** The wave contract (`.ufo/waves/round-16/w1/spec.json` line 3,
  and `dispatch.json` `taskCall.context`) says: "This round do not install
  anything; report missing prerequisites. All pacman transactions PAUSED
  host-wide until operator recovery decision: never -Sy/-Syu/-U/-R, downgrade or
  restart services." The generic directive is general and "always on"; the
  round contract is specific to this round and this host state.
- **Dating.** The generic directive is dated 2026-10-19. The round-16 pause
  follows the round-15 incident of 2026-10-20 04:25.
- **The directive's own text.** `~/.omp/agent/RULES.md` (read in full) says
  "Never run a partial upgrade (`pacman -Sy <pkg>`)" and "If an install fails on
  a stale sync database, report it." It is conditional ("read before helpful
  installs"), and it contains no exception to a host pause.
- **Precedent.** The round-15 closure
  (`corpus/lessons/round-15-verifier-spotcheck.md` lines 252–266, routed
  R15-V1) records that the same generic directive, applied without the
  update-safety gate, produced the forbidden partial upgrade.
- **Judgement.** The precedence conclusion is my inference from the above, not
  a quoted rule. The contract's wording is explicit about this round.

## Safety-debt evidence (passive log read)

`/var/log/pacman.log`, matched lines dated 2026-10-18 through 2026-10-20.

- **Lines 2429–2437, `2026-10-20T04:25:16–17`.** Seat `MadoR15.LibinputEvents`
  ran `sudo pacman -S --needed --noconfirm libinput libinput-tools`. Line 2432:
  `upgraded libinput (1.31.3-1 -> 1.32.0-1)`. Lines 2433–2436 installed
  `python-libevdev 0.13.1-1`, `python-pyudev 0.24.4-1`, `python-yaml 6.0.3-2` and
  `libinput-tools 1.32.0-1`. Line 2438: `35-systemd-udev-reload.hook` ran.
  `upgraded` is the only "upgraded" transaction in this window; it is the partial-
  upgrade signature the operator ruled on.
- **Lines 2422–2428, `2026-10-20T02:41`.** `wlr-protocols r112.a741f0a-1` (new,
  pre-pause; LOG.md line 974 cites it as the OutputSpec install).
- **Lines 2410–2421, `2026-10-20T01:06–01:07`.** `wayland-utils 1.3.0-1` and
  `man-pages 6.19-1` (new, pre-pause).
- **Lines 2349–2409, `2026-10-18` to `2026-10-19`.** `cmark`, `lychee`, `rizin`,
  `shfmt`, `quickshell` (installed, then removed at 19:14:32 by `pacman -Rns`),
  `libdwarf`, `cpptrace`, `qt6-wayland`, `dmidecode`, `gitleaks`. All are new
  installs or removals, none "upgraded". They predate the pause.
- No entry after line 2439 (`2026-10-20T04:25:21`).

These are historical records from other seats. This seat did not run them and
does not re-judge them. Only the libinput upgrade is the open safety debt. The
log shows the transaction; it does not show input behaviour, and neither the
log nor this report establishes a regression.

## Open debt carried forward (no repair proposed here)

- **R15-V1** (unremediated forbidden partial upgrade): owner L0
  (`hyaku-orchestrator` decision channel). Note that the spot-check
  (`round-15-verifier-spotcheck.md` lines 254–266) says no reinstall, downgrade,
  removal, full upgrade or restart was performed or authorised by closure.
- **R15-V2 / process debt:** the "no live probe" breach (`ReviewLibinput`
  `hyprctl version`, disclosed in the round-15 lesson) is process debt, not new
  claim evidence. Any future install must follow the real
  `pacman -Sp --print-format '%n %v'` plan plus complete installed-name
  comparison. Hard-coded fixtures are not that validation.
- **Installed-package state:** this seat did not query the live package database
  (`pacman -Q*`), because that is a package operation outside the round's
  source-only rule. The current libinput version is therefore taken from the log
  only.

## Hand-off

- No tool installed or updated by this seat (none needed; record: `none`).
- The main agent should keep the install prohibition in every seat context this
  round and should not start any install, however helpful, until the operator
  recovery decision lands.
- Checks for the main agent to run after integration: none required by this
  seat. It runs no build, lint or test (contract).
