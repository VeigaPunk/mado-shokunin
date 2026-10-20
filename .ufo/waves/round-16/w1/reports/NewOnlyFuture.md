# NewOnlyFuture — future when-pause-lifted install plan wording

Seat: `MadoR16.NewOnlyFuture` (scribe, leaf). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Status: **drafted wording only.** Nothing below is executed, authorized, or in effect. No present dry run was performed. No pacman, sync, `pacman -Qq`, `-Sp`, service, compositor, or package operation was run by this seat. No installs or updates were made, so the tooling record is empty.

## Scope and sources read (source only)

| source | anchor | use |
|---|---|---|
| `corpus/lessons/round-15-verifier-spotcheck.md` | `#32EF` lines 254–277 (R15-V1, R15-V2) | pause-period rule; future real plan plus complete installed-name comparison; refuse every overlap; fixtures do not prove the step ran |
| `corpus/lessons/round-15.md` | `#7C00` M2 row (line 15) and lines 18–23 | the guard text: `pacman -Sp --print-format '%n %v'`; overlap includes dependencies; overlap goes to L0; guard does not remediate host state |
| `LOG.md` | `#950B` lines 1092–1111 | M2 lesson entry; in-memory guard red/green only; not a retroactive admission |
| `SKILL.md` | `#E381` lines 469–475 | pre-install plan rule; overlap goes to L0; no further pacman operations |
| `corpus/QUALITY.md` | `#1C02` item 20, lines 72–78 | pre-install plan rule and "helpful-tool authorization does not permit a partial upgrade" |
| `.ufo/waves/round-15/evidence/install-guard-red.txt` | `#943C` | fixture-only control, exit 1, `already_installed_in_plan`, overlap libinput; `fixture_only: true` |
| `.ufo/waves/round-15/evidence/install-guard-green.txt` | `#6BED` | fixture-only control, exit 0, `new_only_plan`; `fixture_only: true` |
| `.ufo/waves/round-16/w1/spec.json` | `#8535` | round-16 directive: no pacman during pause; future real plan only after operator authorization |
| `.ufo/waves/round-16/w1/dispatch.json` | `#85E2` lines 421, 426, 741 | SafetyGate policy: `paused=true`, `package-install` blocked; my assignment text |
| `~/.omp/agent/RULES.md` | `#6A50` | tooling channel order; no partial upgrade (`-Sy`/`-Syu`/`-Sy <pkg>`); record every install or update |

Not opened: `~/.omp/agent/agent.db*`, any credential or auth file, any sibling-seat output beyond the listed anchors.

## Facts the future wording must respect (grounded)

1. **Pause holds.** All pacman transactions are paused host-wide until an operator recovery decision (round-16 spec, dispatch). The routed defect R15-V1 is unresolved; the operator decision channel is the L0 line beginning "HOST PARTIAL UPGRADE during mado r15" (spotcheck `#32EF`).
2. **Prior violation.** Round-15 `pacman.log:2429-2437` records `libinput 1.31.3-1 → 1.32.0-1`, plus new `libinput-tools`, `python-libevdev`, `python-pyudev`, `python-yaml`. The orchestrator ruled this a partial upgrade. The round-15 guard does not repair it.
3. **Sync-database state.** Round-15 `AttackNoHarm.md#FAC8` and `SourceTrust.md#11CC` record the last `pacman -Sy` on 2026-10-18 14:11 and 413 pending updates. The sync DB is therefore ahead of the installed system. This is a stated observation from another seat's report, not re-verified here.
4. **Existing guard is fixture-only.** The round-15 red/green evidence hard-codes `installed_before` and `actual_plan` values (`fixture_only: true`). The spotcheck says these "do not prove that operational step ran" and that a future install must use the **real** plan.

## Drafted future wording (not in effect; activates only on the conditions in step 0)

**Step 0 — gate to enter.** The procedure may begin only when all of the following hold, each recorded in the L0 ledger by the operator:
- (a) an explicit operator recovery decision that lifts the pacman pause;
- (b) the exact package names, the requested channel (official Arch `extra`/`core`), and the reason for the install;
- (c) an operator statement on the sync-database state (whether it is current with the installed system), since `-Sp` does not refresh it;
- (d) an operator-written policy change that lifts `package-install` in `safety-policy.json`. Plan authors cannot self-allow it.
If any condition is missing, the install is refused and the request goes to L0. No `-Sy`, `-Syu`, `-Sy <pkg>`, `-U`, `-R`, downgrade, or service/compositor restart is part of this procedure.

**Step 1 — capture installed names (before planning).** Record the exact command and full stdout of `pacman -Qq` (names only) with a timestamp. Store it as the installed-name set `I`. A non-zero exit refuses.

**Step 2 — obtain the real plan (no fixture).** Run exactly:
`pacman -Sp --print-format '%n %v' <operator-named packages>`
Record the argv, stdout, stderr, exit code, and timestamp. A non-zero exit refuses. Parse each stdout line as exactly two fields, `name version`. A malformed line, an empty plan, or a parse error refuses (fail closed). The plan set `P` is the full list of names printed, **including dependencies**, not only the operator-named targets.

**Step 3 — complete installed-name comparison.** Compute `overlap = P ∩ I`.
- Any non-empty overlap refuses. The install is not run. The overlap names and the plan artifact go to L0 for operator decision. This applies to every planned name, including dependencies and packages that would be upgraded in place.
- An empty overlap is required before Step 4. The result is recorded as `new_only_plan` with its evidence.

**Step 4 — re-check at transaction time.** Immediately before the install, repeat Step 1 to get `I'`. If `I' ≠ I`, or any name in `P` now appears in `I'`, discard the plan and return to Step 2. Do not reuse a stale plan.

**Step 5 — install only the planned set.** Use only the operator-named argv with the same package list used in Step 2, and no other flags that refresh or upgrade:
`sudo pacman -S --needed --noconfirm <exact operator-named packages>`
The package list must be byte-identical to the Step 2 argv. Any difference restarts from Step 2. The `--needed` flag does not make the install safe; the overlap check in Step 3 is the guard.

**Step 6 — evidence and record.** Write one artifact containing: the Step 1 set `I` and `I'`, the Step 2 argv and output, `P`, the overlap result, the Step 5 argv, the exit code, and the post-install `pacman -Qq` names. Add the tooling record required by RULES.md: tool, version, channel, and reason. Any verdict that says "install success" must cite these exact artifacts. The artifact must say whether the install ran or was refused.

## Limits the future wording must state (not solved by this draft)

- **Names only.** The overlap check compares names printed by `%n`. It does not check `provides`, `conflicts`, `replaces`, or ABI compatibility. A replacement or soname change can pass as "new-only" and still break a running system.
- **Sync DB.** `-Sp` uses the existing sync database and does not refresh it. If the DB is ahead of the installed system (the 2026-10-18 `-Sy` state), a "new-only" plan can still be a partial upgrade in Arch terms. Step 0(c) puts that decision with the operator; this draft does not decide it.
- **Hooks.** The plan does not show hooks (for example udev reload or system-update hooks). Round-15 M2 included them. Operator review of hooks is required before Step 5; this draft does not automate it.
- **No proof of past runs.** Red/green fixtures prove only the in-memory comparison logic. They do not prove a real plan was taken or that any install was safe.
- **Post-install state is not verified here.** Step 6 records the post-install names. It does not check that the running compositor or services are unaffected, and it does not repair the existing libinput state.

## Findings for the planner and L0

1. The round-16 wording already requires a real `-Sp` plan and complete installed-name comparison in future. The drafted steps above make that concrete (argv, parse rule, overlap rule, re-check, binding of the install argv to the plan).
2. **Gap:** existing guard text (QUALITY 20, SKILL, LOG) does not require re-checking installed names at transaction time (Step 4), nor binding the install argv to the planned list (Step 5). Future lesson text should add both. This is a proposal, not an edit; this seat does not edit corpus files.
3. **Gap:** no existing rule forbids a stale sync DB from being used for a new-only install. Step 0(c) proposes that the operator state it. This is a decision for the operator, not for mado seats.
4. The red/green evidence files are labeled `fixture_only`. Future reports should not cite them as install-plan validation.

## Out of scope

- No present dry run, no `-Sp`, no `-Qq`, no sync or install.
- No edits to corpus, SKILL, LOG, QUALITY, SCORECARD, or any sibling seat's files.
- No host, service, compositor, input, or screenshot probe.
- No commits.

## Tooling record

None. No tool was installed or updated. Missing prerequisites for any future install: operator recovery decision, operator-named package list, sync-DB state statement, and the `package-install` policy change (Step 0).
