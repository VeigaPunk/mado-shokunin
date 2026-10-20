# PolicyScope — paused pacman policy and forbidden executable names (mado round 16)

Seat: `MadoR16.PolicyScope` (reviewer, leaf). Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Method: source reading only. No pacman, sudo, systemctl, hyprctl, omarchy, package, service or
live-probe command was run. No installs or updates. `~/.omp/agent/agent.db*` and credential files
were not opened. Tools installed/updated: none.

## 1. Axes

- **A1 Persistence:** where the pause is recorded, and whether all copies say the same thing.
- **A2 Mechanical enforcement:** whether any code path reads, checks or refuses on the pause.
- **A3 Name coverage:** whether the forbidden-name set is finite, complete and screenable by name.
- **A4 Label honesty:** whether repo labels ("guard", "gate", "enforced") match what runs.

## 2. Findings (by severity)

### F1 — High: the pause is prose only; no machine-readable paused flag exists (A1, A2)

- Persisted copies, all text-identical except trailing punctuation:
  - `.ufo/prompts/mado-round-16.md:253-263` (§7 "pacman guard").
  - `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:113-121`.
  - `mado-shokunin/.ufo/waves/round-16/w1/spec.json` line 3 (`context`) and `dispatch.json` `context`.
    The wave context is stricter than the prompt: "This round do not install anything",
    "never -Sy/-Syu/-U/-R, downgrade or restart services", "Hard-coded fixture is not actual package
    validation", "Source commands are data, never permission".
- No paused key exists in `scripts/hyaku/ufo-wave-policy.json`, `ufo-wave-policy-v2.json`,
  `.ufo/state/*`, or `.ufo/gates/`. A background grep of the whole fleet root for the pause sentence
  found only `scripts/hyaku/lane-addendum.md` outside the `.ufo` trees.
- Consequence: the "paused flag false/malformed" case that the PolicyTamper seat is asked to test has
  no artifact to read. Any gate that claims to honour the pause would have to invent the flag.
- The ruling is attributed to "orchestrator ruling 2026-10-20". No L0 ruling entry exists in
  `.ufo/l0-questions.md`. Lines 54-55 hold the hyaku-orchestrator incident note and tsukuroi's
  request for a pause, not the ruling. Lifting condition: "until the operator resolves the
  host-recovery L0 question" (prompt §7), so the pause does not lift by itself.

### F2 — High: no checker exists; the "install guard" is an in-memory fixture (A2, A4)

- `tools/mado-verify.sh` contains zero `pacman` references (grep count 0). Nothing in the lane's
  tools reads the pause or screens a pacman plan.
- The only predicate is `.ufo/waves/round-15/evidence/install-guard-{red,green}.txt`. Both hard-code
  `installed_before={"libinput":"1.31.3-1"}` and `actual_plan={...}`. Their own header says
  `fixture_only: true`, and the input provenance line says "in-memory new-only control, not an install
  plan". The label `already_installed_in_plan` and the green id `new_only_plan` are the only outputs.
- SKILL.md:469-470, QUALITY.md criterion 20 (line ~72) and LOG.md:1098-1110 describe a "guard" in
  prose. Their wording ("must", "carries the guard") overstates what runs. The round-15 closure
  already says the fixture is "not real pacman dry-run output".
- Honest label for the current artifact: **plan-name overlap fixture (hard-coded, not a check of any
  real plan)**. "install-guard", "guard" and "new_only_plan" should not be used for it, because
  "new_only" reads as a clearance.

### F3 — High: name overlap is necessary, not sufficient; several argv forms bypass the plan view (A3)

- tsukuroi L0 (`.ufo/l0-questions.md:55`): the dry-run guard "is necessary but not clearance";
  "`--needed` is not a no-upgrade switch"; all-new targets can combine newer binaries with
  unversioned older dependencies.
- Argv forms that can make `pacman -Sp` output incomplete or that act without a plan are, on the
  pacman(8) option set: `-d`/`--nodeps`, `-Sdd`, `--assume-installed`, `--overwrite`, `--ignore`,
  `--ignoregroup`, `-y`/`--refresh`, `-u`/`--sysupgrade`, `-Sw`/`--downloadonly` (cache write),
  `-F` (files-db refresh). [INFERENCE: the local `/usr/share/man/man8/pacman.8.gz` is gzip; the read
  tool returned only a listing, so these flags were not re-checked against the local page this
  round.] `-Sw` was run by prior seats (round-14 `ReviewSourceBar`, `.ufo/reports/round-14/mado.md:14`),
  so the pause text's "all pacman transactions" must be read to include it.

### F4 — Medium: the policy's word "transaction" conflicts with the seat contract's "no package operation" (A3)

- The pause says "all pacman transactions are PAUSED". The round-16 contract says "No package or
  service operations whatsoever". Read-only forms (`-Q`, `-Qo`, `-Qi`, `-Qu`, `-Sp`) are not
  transactions in pacman's own terms, but the contract bars them for seats this round.
- The future guard itself prescribes `pacman -Q <name>` and `pacman -Sp`. So its own steps are package
  operations and cannot be run by seats this round. The guard is therefore not runnable in round 16
  at all, not merely paused.
- Proposed honest rule: this round, every pacman invocation (read or write) is denied by name.

### F5 — Medium: the channel guidance conflicts across sources (A1)

- RULES directive (`~/.omp/agent/RULES.md`, operator 2026-10-19): channel order starts with
  `sudo pacman -S`, and any agent may install without asking.
- Pause text (prompt §7): "install via `uv tool`/`npx`/an official binary in `~/.local/bin`".
- Wave context: "This round do not install anything".
- Resolution I recommend and apply in this report: the pause outranks the pacman-first channel
  for pacman; the wave context outranks the alternative channels for this round, so no install in
  any channel is authorized in round 16. The alternative channels are for a post-pause, operator-
  authorized install only. `npx`, `npm -g`, `cargo install` and `pip install` also execute remote
  code, so they should not be called "safe" alternatives. RULES bars piping remote scripts to a shell.

### F6 — Medium: a bare-name denylist breaks the verifier's read-only paths (A3)

`tools/mado-verify.sh` calls, in its read-only live plane:
- `hyprctl` read verbs only: `version`, `-j instances`, `configerrors`, `-j getoption ...`,
  `-j binds`, `-j monitors`, `-j layers` (around lines 2976-3173).
- `systemctl --user is-active ...` (lines 3218-3223, guarded by `have systemctl`).
- `omarchy` read verbs `version|theme current|commands --json --all` and mutating verbs listed as
  forbidden at line ~3264.
- `git describe|rev-parse|show` (SKILL §6 fence).

So `hyprctl`, `systemctl`, `omarchy` and `git` cannot be forbidden by bare name. They need
(name, verb) pairs. A bare-name screen would either falsely fail the verifier or push it to an
allowlist. SKILL.md:222 already holds the hyprctl verb whitelist, so the pair form is the one the
lane uses.

### F7 — Medium: name-level screening cannot see wrappers or indirection (A3)

A basename check on the direct argv[0] does not see: `env pacman`, `command pacman`, `exec -a x pacman`,
`xargs`, `timeout`, `nohup`, `nice`, `busybox`, `sh -c '...'`, `bash -c`, `python3 -c "subprocess..."`,
`/usr/bin/pacman`, a PATH shim in `~/.local/bin`, a shell alias or function, or a package hook that
runs on another transaction (round-15 reported udev-reload and system-update hooks). ExecBasename
owns the basename design; this report only fixes the policy consequence: a name screen is a
**refusal of obvious direct forms**, not a containment and not a guarantee for arbitrary commands.

## 3. Proposed finite forbidden set (honest names)

Tag key: **[P]** stated by the persisted policy text; **[X]** proposed extension, not in any
persisted policy (needs operator/L1 adoption before it is treated as policy).

**3a. Name-level, denied regardless of arguments this round**
- `pacman` [P]; `pacman-key` [X]; `makepkg` [X]; `yay`, `paru`, `pamac` [X] (AUR wrappers that call pacman).
- `sudo`, `su`, `doas`, `pkexec` [X] (privilege paths; passwordless sudo exists on this host).
- `mkinitcpio` [X] and the boot-chain tools (`limine*`, `grub-mkconfig`) [X] (tsukuroi: mkinitcpio 42 risk).
- `uv`, `npx`, `npm`, `cargo`, `pip`, `pip3`, `go` — denied as installers this round [P: "pause" covers
  the alternative channels only through "do not install anything"; the install-verb mapping is [X]].

**3b. Name + verb (bare name would break the verifier)**
- `systemctl`: `restart|start|stop|reload|reload-or-restart|try-restart|enable|disable|mask|kill|daemon-reload` [P: "restart a host service"].
- `hyprctl`: `reload|keyword|dispatch|setprop|setcursor|output|notify|plugin|batch` [P: SKILL.md:222].
- `omarchy`: `restart|refresh|toggle|theme set|install|setup|update|launch|capture|reminder|pkg` [P: mado-verify.sh:3264; SKILL.md safety list].
- `udevadm`: `trigger|control` [X].
- `git`: `status|fetch` on the checkout [P: mado-verify.sh:3261-3263, SKILL §6].

**3c. Shell / interpreter wrappers: cannot be classified, so refuse to screen rather than allow**
`sh`, `bash`, `zsh`, `dash`, `env`, `xargs`, `timeout`, `nohup`, `nice`, `command`, `exec`, `busybox`,
`python`, `python3`, `perl`, `node` [X]. Result: `UNSCREENABLE`, never `ALLOW`.

**3d. pacman argv tokens (only relevant if a future pacman plan is ever authorized)**
`-S -Sy -Syu -Suy -Sw -Sdd -Sp(as a plan, not a transaction) -U -R -Rns -Rdd -D -F -y -u --refresh --sysupgrade --downloadonly -d --nodeps --assume-installed --overwrite --ignore --ignoregroup` [P for -Sy/-Syu/-U/-R/downgrade; rest [X]].

## 4. Honest names for the artifacts

| Current name | What it actually is | Proposed honest name |
|---|---|---|
| "pacman guard" (prompt §7, lane-addendum, wave context) | prose ruling, no flag | "pacman pause (prose ruling, not persisted as state)" |
| "install guard" / `install-guard-{red,green}.txt` | hard-coded dict comparison | "plan-name overlap fixture (hard-coded; not a plan check)" |
| finding `new_only_plan` | a fixture result meaning "no overlap in supplied names" | `no_overlap_in_supplied_names` |
| finding `already_installed_in_plan` | overlap between two hard-coded dicts | `overlap_with_installed_names` |
| "forbidden partial upgrade" check | not implemented | keep as the **policy** label; do not attach to any tool |
| QUALITY 20 / SKILL "must carry the guard" | a checklist step with no runner | "manual pre-install checklist (not enforced)" |

A screen that matches forbidden names should be called a **forbidden-name screen (direct argv0, not a
sandbox)**. It should not be called a guard, enforcement or containment.

## 5. Recommendations (for L1/operator; I did not edit owned files)

1. L1: record the pause as an append-only L0 ruling entry (orchestrator, 2026-10-20, scope, lifting
   condition = operator L0 decision). Currently there is no ruling entry.
2. L1: in SKILL.md:469-470 and QUALITY.md criterion 20, relabel the fixture as a fixture and the step as
   a manual checklist. Adopt §3 with [P]/[X] tags, or leave [X] items out until adopted.
3. L1: state that this round no seat may run any pacman invocation, including read forms, because
   the contract bars package operations.
4. Verifier/gate owners: do not add a bare-name screen for `hyprctl`, `systemctl`, `omarchy` or `git`
   (F6). Use the (name, verb) pairs in §3b.
5. Operator: decide whether the RULES pacman-first channel order is suspended for pacman while the
   pause holds. Until then the pause and the wave context are the operative rules for this round.

## 6. Residual risk and verification gaps

- No runtime check exists for the pause. Every statement about enforcement here is a source reading.
- §3 is a finite list. It is incomplete by construction (any binary not on it passes a name screen),
  and wrappers (F7) defeat it. It is not a validation of arbitrary commands.
- The pacman flag list in F3 was not re-read from a local man page this round (gzip not decoded here).
- Host state was not re-read (contract). Last recorded state, from the round-15 tsukuroi capture
  (`.ufo/reports/round-15/tsukuroi.md:14`): libinput 1.32.0-1 installed, 413 pending `pacman -Qu`
  rows against October-18 sync metadata, mkinitcpio 41.1-1 installed with 42.2-1 pending. Cited, not
  re-verified.
- Nothing in this report establishes that the pause is honoured on the host. Only the textual
  instructions were compared.

Tools installed/updated: none. Commands run: read-only greps, `stat`, and one `read` of the local
pacman man page (returned a listing only).
