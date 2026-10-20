# ExecBasename — static basename denial review (Mado round 16, C2)

Reviewer seat: `MadoR16.ExecBasename` (leaf reviewer, read-only, no subagent dispatch).
Scope: review the basename denial design specified for the static action-plan gate, and
explain which wrappers and sibling executables it does not cover. No broader enforcement
claim is made or implied.

## Status of the reviewed artifact

- The design source is the `SafetyGate` prompt in `.ufo/waves/round-16/w1/spec.json`
  (item `SafetyGate`), which reads: "For read-source/repo-write refuse executable basenames
  pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env (no shell
  execution or command evaluation). This is a bounded declared-plan classifier not arbitrary
  shell analysis or enforcement."
- `tools/mado-action-plan.py` and `.ufo/waves/round-16/safety-policy.json` do **not exist yet**
  in the lane at review time (`tools/` holds only `mado-verify.sh` and `swarm-registry.json`).
  `agent://MadoR16.SafetyGate` reports "Nothing produced yet". Every finding below is therefore
  about the specified design text, not about implemented code. Re-check each finding against the
  implementation once it lands.
- The basename list above is the only content-based denial specified for read-source and
  repo-write. The other controls (`kind` = package-install / service-mutate / compositor-mutate /
  input-capture blocked) trust the plan's own `kind` label.

## Axes

1. **Denial coverage** — does the 12-name list cover the executables the R15 harm and the
   stated scope actually need?
2. **Wrapper coverage** — are exec-wrappers that re-dispatch argv[0] to a denied name caught?
3. **Sibling-family coverage** — do hyphenated or renamed siblings of denied names get caught?
4. **Fail mode** — is an unlisted executable allowed or refused?
5. **Claim honesty** — does the design's wording overstate what the check does?

## Mechanism as specified (what the check sees)

- The check inspects `argv[0]` of each `read-source` / `repo-write` action only (the spec gives
  no rule for `argv[1..]`; see F7).
- Basename is matched by exact string equality against the 12 names. Absolute paths reduce to
  their basename, so `/usr/bin/pacman` is denied; `./pacman` is denied.
- The gate must not execute argv or inspect the host (spec). So it cannot resolve symlinks,
  PATH lookups, or what a wrapper will dispatch to.

## Findings (ordered by severity)

### F1 — High: exec-wrappers in argv[0] position pass unchecked

Plan `read-source`, `argv = ["nice","-n","0","pacman","-S","--needed","libinput"]` →
argv[0] = `nice`, not on the list → clean. The same holds for any wrapper that re-dispatches
its arguments to another program. Not covered:

`nice nohup timeout stdbuf setsid ionice chrt taskset time command builtin exec xargs flock
watch strace ltrace script unbuffer busybox doas su runuser pkexec nsenter unshare chroot
bwrap firejail systemd-run ssh dash zsh ksh fish csh ash rbash`

Covered wrappers are only `sudo`, `env`, `sh`, `bash`. The list therefore is a judgment about
which wrappers to name, not a closed set. The design has no unwrapping step.

Note the R15 shape is only caught when it is written literally: `sudo pacman -S ...` in a
read-source action is refused at `sudo`. The same operation written as `nice`, `timeout`,
`doas`, `busybox`, or `dash -c` is not refused.

### F2 — High: sibling and hyphenated families are not covered by exact-match names

Exact equality misses binaries that share a family name. Examples, with anchors:

- **libinput-tools (highest concern).** The list names `libinput`. The helper binaries are
  `libinput-list-devices`, `libinput-debug-events`, `libinput-record`, `libinput-replay`, and
  siblings such as `libinput-measure`, `libinput-analyze`, `libinput-debug-gui` (named in
  `corpus/knowledge` S051 `tools.rst` and in `corpus/lessons/round-15.md:16,89`). None of
  these basenames equals `libinput`. So `read-source ["libinput-record","/dev/input/event3"]`
  is clean. That is raw input capture labelled as read-source, which the `input-capture`
  block never sees because it depends on the self-declared `kind`. The R15 install that
  pulled `libinput-tools` (`corpus/lessons/round-15-verifier-spotcheck.md:256-258`) is also a
  package the name list does not model.
- `pacman` misses `pacman-key`, `pacman-db-upgrade`, `paccache`. `makepkg` (builds and can
  install with `-i`), `pamac`, `trizen`, `aura` are not `pacman`/`yay`/`paru` and are not listed.
- `systemctl` misses `systemd-run`, `busctl`, `loginctl`, `machinectl`, `udevadm`, `reboot`,
  `shutdown`, `telinit`, `init`.
- `hyprctl` misses `hyprpm` and other Hyprland control binaries.
- `omarchy` misses every `omarchy-*` helper. Anchors in the lane:
  `corpus/knowledge/walker-deep.md:493` (`omarchy-theme-set`),
  `corpus/knowledge/waybar-walker-semantics.md:119,150,151,154` (`omarchy-menu`,
  `omarchy-launch-bluetooth`, `omarchy-launch-wifi`), `tools/mado-verify.sh:3596`
  (`omarchy-theme-set`).
- `evtest` misses `evemu-record`, `evemu-event`, `evemu-describe` (raw device capture).
- `sudo` misses `doas`, `pkexec`, `su`, `sudoedit`.

### F3 — High: interpreters and build tools can run any command; the denylist cannot cover them

Any allowed interpreter or build driver can launch `pacman` or `systemctl` without naming it
in argv[0]. None of these are denied, and each can carry arbitrary argv:

- `python3`, `python`, `perl`, `ruby`, `node`: e.g. `["python3","-c","import os; os.system('pacman -S libinput')"]`.
- `awk`/`gawk`/`mawk`: `awk 'BEGIN{system("pacman -S x")}'`.
- `find -exec`, `make` recipes, `xargs` (already F1), `git -c` / hooks / aliases.
- `cargo` (build.rs), `npm`/`npx` (postinstall), `uv run`.
- `tar --to-command`, `rsync -e`, `ssh`/`scp`; pagers or editors with shell escape (`less`, `vim`).

`mado-verify.sh` itself uses `python3`, so an allowlist that includes it has the same hole.
This is a structural limit of a declared-argv denylist. The gate's own "not arbitrary shell
analysis" wording is the honest scope; the denylist must not be presented as stopping
arbitrary command execution.

### F4 — Medium: raw-input capture by device path is not denied

`read-source ["cat","/dev/input/event3"]`, `["dd","if=/dev/input/event3","count=1"]`,
`["head","-c","64","/dev/input/by-id/..."]` and `/dev/uinput` writes pass, because no path
argument is inspected. Input capture is only blocked by the self-declared `kind`. A bounded,
static string check on read-source arguments naming `/dev/input/` and `/dev/uinput` would
close this without shell parsing.

### F5 — Medium: repo-write carries no destination constraint

`repo-write` requires only a nonempty argv. `["cp","x","/usr/lib/systemd/system/x.service"]`,
`["tee","/etc/sudoers.d/x"]`, `["ln","-sf","/usr/bin/y","/home/u/.local/bin/z"]` and
`dd of=` all pass if `argv[0]` is an unlisted name. The basename design does not address
writes outside the repo, and the spec's "repo-write" label is not a path check. This is a
residual to state, not a finding to close with this list.

### F6 — Medium: the denylist sits in code, outside the frozen-input digest

The spec's `--frozen DIR` verifies digests of `plan.json` and `policy.json` only. If the 12-name
list is hard-coded in `tools/mado-action-plan.py`, editing that list changes the gate's
behaviour without changing any digest the frozen check binds. Putting the list (and any
wrapper or family list) in `safety-policy.json` makes it snapshot-bound. This is a
design-placement point, not a runtime exploit.

### F7 — Medium: basename extraction edge cases are unspecified

- `argv[0]` ending in `/` (`"pacman/"`) yields an empty basename and passes. Reject empty or
  trailing-slash `argv[0]` as malformed (fail closed).
- Prefix assignments (`"PATH=/x"` as `argv[0]`) are not commands under execve but would be
  under any later shell consumer. Reject `=` in `argv[0]` or state it is not a command.
- Case: `Pacman` is not denied. Harmless on case-sensitive Linux filesystems; not on
  case-insensitive mounts. State it.
- Whether `argv[1..]` is checked is not specified. Checking every token would refuse benign
  paths like `ls /usr/bin/pacman` (basename match), so the spec should state argv[0]-only
  explicitly and list the wrapper rule (F1) separately.

### F8 — Process: no fail-closed default for unlisted executables

The spec fails closed on unknown `kind`, missing argv and malformed input, but not on an
unlisted `argv[0]`. Unlisted names therefore pass. This is the largest single gap between the
design's own fail-closed language and its denylist.

## Wrappers and siblings not covered — summary table

| Class | Examples not denied | Covered today? |
|---|---|---|
| exec wrappers (argv[0] re-dispatch) | nice, nohup, timeout, stdbuf, setsid, ionice, chrt, time, command, exec, xargs, flock, watch, strace, script, busybox, doas, su, runuser, pkexec, nsenter, unshare, chroot, systemd-run, ssh, dash, zsh, ksh, fish | No (sudo, env, sh, bash only) |
| pacman family | pacman-key, pacman-db-upgrade, paccache, makepkg, pamac, trizen, aura | No (pacman, yay, paru only) |
| systemd/service family | systemd-run, busctl, loginctl, machinectl, udevadm, reboot, shutdown, telinit, init | No (systemctl only) |
| Hyprland family | hyprpm, other hypr* control binaries | No (hyprctl only) |
| omarchy family | omarchy-theme-set, omarchy-menu, omarchy-launch-*, omarchy-* helpers | No (omarchy only) |
| input family | libinput-list-devices, libinput-debug-events, libinput-record, libinput-replay, libinput-measure, libinput-analyze; evemu-* | No (libinput, evtest only) |
| interpreters / build / escape | python3, perl, ruby, node, awk, find -exec, make, git -c, cargo, npm, uv, tar --to-command, rsync -e, ssh, less, vim | No |
| raw device paths (read-source args) | /dev/input/*, /dev/uinput | No |
| write destinations (repo-write args) | cp/tee/ln/dd to any absolute path | No |

## Recommendations (design level; no code written here)

1. Replace the argv[0] denylist for read-source and repo-write with an argv[0] **allowlist** of
   named read-only binaries. Refuse every other name with a stable reason (fail closed). Exclude
   the interpreters and build drivers in F3 from the allowlist.
2. If a denylist is kept for any reason, add: the wrapper set (F1), the family prefixes
   (`libinput-`, `omarchy-`, `pacman-`, `systemd-`, `hypr`, `evemu-`), and the interpreter set
   (F3) — and state that the list is incomplete by construction.
3. Move every list into `safety-policy.json` so the frozen digest binds it (F6).
4. Add a bounded string check for `/dev/input/` and `/dev/uinput` in read-source arguments (F4).
5. Reject empty, trailing-slash, and `=`-bearing `argv[0]` as malformed (F7).
6. Keep the claim scope as the spec already states: a bounded declared-plan classifier. A clean
   result (`plan_safe`, exit 0) must not be reported as proof that the plan is safe to run.

## Residual risk and verification gaps

- Nothing was executed. Per the round's rules (source reading only, no checks by seats), no
  gate, selftest, or host probe was run. All findings are from the spec text and the lane's
  source anchors.
- `tools/mado-action-plan.py` and `safety-policy.json` were absent at review time. Re-review
  after SafetyGate lands, especially the argv[0]-only rule and where the lists live.
- Binary names for libinput-tools, makepkg-family, and omarchy helpers are taken from the lane's
  corpus and tool docs (S051 `tools.rst`; `corpus/knowledge` omarchy notes). Installed package
  file lists were not read, and no installed-package census was taken. The full helper set may
  be larger than the names cited here.
- The wrapper and interpreter lists are from general knowledge of Unix process launchers and
  interpreters, not from a measured inventory on this host. They are not claimed as host facts.
- Basename behavior (POSIX `basename` on trailing-slash input, empty result) is standard
  behavior, not observed in this run.

## Tooling

No installs, updates, or package operations were performed by this seat. The pacman transaction
pause for round 16 was respected.
