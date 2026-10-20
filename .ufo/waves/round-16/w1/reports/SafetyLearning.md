# SafetyLearning — R15 host harm against the proposed static plan gate

Seat: `MadoR16.SafetyLearning` (connector, leaf; no delegation). Lane: `mado-shokunin`, round 16, C2 operability.
Axes: **operability** (primary, the gate's target), **quality** (learning trend), **discernment** (whether the gate's limits are stated, not implied). Coverage is out of this seat's scope.

Evidence basis: committed round-15 reports, evidence, lessons and the spot-check, plus upstream pacman and ArchWiki source text fetched read-only. No host probe, no `pacman`, no `/var/log` re-read, no `/proc`, no install. Host facts below are last observations from round 15 (2026-10-20, about 04:25–04:40 -0300), not current host state. Labels: **[OBS]** quoted from committed evidence; **[UPS]** upstream text; **[INF]** inference; **[UNV]** not verified on this host.

The gate under review is not landed. `MadoR16.SafetyGate` has produced no output yet, so I assessed the contract in `spec.json` C2 (`pacman -Sp --print-format '%n %v'` plan, complete installed-name comparison, any overlap refuses) and QUALITY 20. If SafetyGate's final design differs, re-run this matrix against it.

## 1. R15 actual host harm (the event the gate must answer)

| Step | Observation | Anchor |
|---|---|---|
| Command | `sudo pacman -S --needed --noconfirm libinput libinput-tools`, run by `MadoR15.LibinputEvents` for static man/help reading | [OBS] `round-15.md` M2; `round-15-verifier-spotcheck.md` §R15-V1 |
| Transaction | `libinput 1.31.3-1 -> 1.32.0-1`; new `libinput-tools 1.32.0-1`, `python-libevdev 0.13.1-1` (dependency), `python-pyudev 0.24.4-1`, `python-yaml 6.0.3-2` | [OBS] `pacman.log:2429-2437`, per `LibinputEvents.md` §1, `InputSafety.md:79` |
| Hook | `35-systemd-udev-reload.hook` ran `udevadm control --reload`, then `udevadm trigger -c change` and `udevadm settle`, because `/etc/systemd/do-not-udevadm-trigger-on-update` is absent. Every device, input devices included, got a change uevent. | [OBS] `InputSafety.md:82`, `AttackNoHarm.md:14`; `pacman.log:2438` |
| Partial state | Last `pacman -Sy` at 2026-10-18 14:11 (`pacman.log:2287-2288`); last full upgrade 2026-10-16 (`:2256`); `pacman -Qu` = **413** pending, including `hyprland 0.56.2-2→-4`, `aquamarine 0.15.0-2→0.15.1-1`, `systemd`, `mesa`, `linux` | [OBS] `AttackNoHarm.md:16`, `SourceTrust.md:20-22`, `AttackSource.md:51` |
| Running process | Hyprland PID 1706 mapped `/usr/lib/libinput.so.10.13.0 (deleted)`, i.e. 1.31.3 code while disk holds 1.32.0 | [OBS] `ReviewDocsEra.md:76`; `EvidenceClassJoin.md:98` |
| Detection failure | A seat's `grep` of `pacman.log` returned no matching lines and could not date the change | [OBS] `ReviewScore.md:39-40, 138-139` |
| Ruling | Orchestrator: forbidden partial upgrade. Closure: "A green unchanged gate does not erase that harm." | [OBS] spot-check §R15-V1; `SCORECARD.md:661-668` |

Two details matter for the gate design:

- **The command's own flag did not protect.** `--needed` means "Do not reinstall the targets that are already up-to-date" [UPS: pacman.8.asciidoc, `--needed`]. It skips same-version packages. libinput's version differed, so it stayed a target and was upgraded. `--needed` is a version-equality filter, not a safety filter.
- **The overlap was the upgrade itself.** The R15 harm is exactly an installed name appearing in the plan. That is the condition the proposed gate tests.

## 2. What the proposed gate catches (if invoked)

**Caught: the R15 transaction class, provided the plan is computed and honored.**

- `-S` installs "all the packages it depends on" [UPS: `-S` description], so the target list includes dependencies. The libinput dependency of libinput-tools would appear by name, and the installed-name comparison would flag it. The gate refuses R15's libinput step. The committed red fixture reproduces this: `exit 1`, `already_installed_in_plan`, `overlap ["libinput"]` [OBS `install-guard-red.txt:10-12`].
- Name-level overlap covers indirect upgrades too. A new package that drags in an installed dependency at a newer version appears in the plan under that dependency's name.
- Pure new-name packages (libinput-tools, python-*) pass. That is correct only for the overlap rule; see §3.

**Limits of the catch, even when it fires:**

- The red/green fixtures are hard-coded. `actual_plan` is copied from the post-hoc `pacman.log` lines, so the fixture is an answer key. `installed_before` holds one name (`{"libinput": ...}`), so it never exercises comparison against a full installed set. QUALITY 20 and the spot-check both disclose this; it is not validation of `pacman -Sp` on this host.

## 3. What the gate cannot prevent

Numbered so SafetyGate can map each to a rule or an explicit residual.

1. **Invocation bypass.** The gate is a process rule. `pacman` remains callable by any seat with sudo. RULES.md channel order begins `sudo pacman -S --needed --noconfirm <pkg>` [OBS `~/.omp/agent/RULES.md:7`], which is the exact R15 command. The operator's own channel example teaches the pattern that caused the harm, and no gate is in that channel. Blocking this needs a host-level control (wrapper, sudoers scope, or pacman hook), which is operator-owned. Within the lane, the gate can only refuse; it cannot stop a call.
2. **Stale-repository drift.** `-Sp` plans against the local sync DB. A plan with no overlap can still leave the host partial when the host is far behind its repo (413 pending here). ArchWiki defines this as the partial-upgrade hazard: `-S package` without a current sync can pull or leave mismatched libraries, and `-Sy` is unsupported [UPS: ArchWiki "Partial upgrades are unsupported"]. The gate needs a non-mutating freshness precondition (pending-update count from a temporary DB, as `checkupdates` does) [UNV: pacman-contrib installed on this host; not checked, no probes]. Refreshing the live DB with `-Sy` is itself forbidden.
3. **Side effects outside the plan.** `pacman -p` prints targets, not transaction effects [UPS: `-p, --print`]. It shows nothing about scriptlets, triggers, or hooks. The udev-reload hook fired in R15 and replayed change uevents on all devices. A new-name-only plan with a udev rule would pass the overlap check and still trigger the same hook. `--noconfirm` also removes the operator's last chance to notice.
4. **Running-process drift.** ArchWiki: "Upgrades are typically not applied to existing processes" [UPS]. The gate checks disk names only. It cannot see that Hyprland still maps the deleted 1.31.3 library (PID 1706 in R15). Detecting that needs a live `/proc` read, which is forbidden this round, so the residual is unbounded by the gate.
5. **Plan/install race (TOCTOU).** The plan is computed separately from the install. Between them the sync DB or installed set can change. Unless the gate runs the install itself or re-verifies the exact plan, the check is advisory. [INF]
6. **Name-only comparison.** `%n` and `%v` do not capture version, epoch, `%R` replaces, or `%H` conflicts. A replaced or conflicting package can be removed by a transaction whose target list shows only new names. `-p` describes printing targets, not transaction removals, so this is a gap unless SafetyGate adds `%R`/`%H` checks. [INF from man text; not observed]
7. **Fail-open on empty or failed output.** An empty plan is a legitimate result under `--needed` ("nothing to do"). A failed or timed-out `-Sp` that prints nothing looks the same. The gate must check exit status and require every requested target to appear in the plan or be satisfied by the installed set, or it fails open. [INF; requirement]
8. **Full-upgrade case.** "Any overlap refuses" refuses every `-Syu`, since all 413 pending names overlap installed names. The gate therefore cannot authorize the operator-owned recovery (completing the upgrade). That path must be separate, and SafetyGate should say so rather than implying the gate governs recovery.
9. **Non-pacman channels.** RULES.md lists `uv tool install`, a release binary into `~/.local/bin`, and `cargo install`/`npm -g` after pacman. A pacman plan gate covers none of them. They do not touch system libraries in the R15 way, but the gate's scope statement must say so.
10. **Log-based detection is not a control.** ReviewScore's log grep missed the R15 lines. A post-hoc `pacman.log` check cannot be the gate's detection method; the gate must refuse before running.

## 4. Net verdict

The proposed gate would have refused the R15 libinput step if it had been run and honored. It does not prevent the R15 harm class in general. Its effect is to refuse one command path, given that a seat runs it first. What it cannot cover: the channel that the operator's own rule names first; hooks and uevent side effects; running processes that keep old mappings; a host behind its repo with no freshness precondition; and the operator's own recovery. Its output should be stated as **refuse / route to L0**, never as "safe" or "repaired" (spot-check: operability harmed, unchanged gate is a different observable).

## 5. Recommendations (bounded; for SafetyGate, L1 and operator; no edits by this seat)

1. **Wire the gate into the channel rule, or record that it is not.** Operator decision: amend RULES.md channel line 7 so the first channel is gated, or drop `sudo pacman -S` from the channel list. Until then, state the bypass as a residual.
2. **Add preconditions before the overlap check:** (a) exit status 0 from `-Sp`, plus target-presence check (fail closed); (b) freshness via a non-mutating pending-update count, refusing when pending updates exist for a targeted install; (c) full installed-name set from `pacman -Qq`, not a hard-coded subset; (d) refuse any `%R`/`%H` hit.
3. **Bind plan to execution.** Either run the install from the same validated target list, or re-plan and refuse on any difference (TOCTOU).
4. **Route hook-bearing packages to L0** (udev, systemd, or any package with scriptlets), even when the overlap check passes.
5. **Keep fixture language.** Describe the fixture as an in-memory control of comparison logic, not as validation of `pacman -Sp` on this host. Real `-Sp` runs are operator-authorized only.
6. **Separate recovery.** Say explicitly that completing the upgrade is operator-owned and outside this gate.

## 6. Limits and tooling record

- Upstream sources read: pacman `doc/pacman.8.asciidoc` (gitlab.archlinux.org raw) and ArchWiki "System maintenance" (web). Other upstream variants 404'd or reset; no claim rests on them.
- Host reads: none in this seat. R15 facts come from committed reports and quotations; I did not re-open `/var/log`, `/proc`, or any device, service, or package state.
- Tools installed or updated by this seat: **none**. RULES.md was read. The round forbids installs; missing prerequisites (pacman-contrib for `checkupdates`) are recorded as [UNV], not installed.
- Not checked: whether SafetyGate's final design uses `%R`/`%H`, freshness checks, or plan binding. Re-run §3 against that design once it publishes.
