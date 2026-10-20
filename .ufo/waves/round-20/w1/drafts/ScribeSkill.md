# ScribeSkill draft — SKILL.md tripwire section and isolation-harness subsection (round 20)

Status: DRAFT, NOT APPLIED. Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md`.
Line numbers were read from the working tree, which matches master `e629f73`
(`git status` shows SKILL.md unmodified; the tripwire heading is at 525 and the
registry row at 563 at both). Line 600 was read from the working tree only.

Gate on application: the evidence-marker, binding-guard and carve-out text below
describes the round-20 TARGET contract (pre-registration E1-E4). Tool `e629f73`
(= `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`) does NOT
implement it yet. Apply these blocks only after C1 lands and
`tw-precision.py` reports N/N with the guards in the pre-registration. Until then
the SKILL text must not claim these behaviours.

Blocks, in file order:

| block | action on the original SKILL.md | lines |
|---|---|---|
| A | REPLACE | original 525-540 inclusive |
| B | APPEND (insert directly after block A's text, before the blank line preceding `## Gate registry`) | after original 540, replaces nothing |
| C | APPEND | after original 600 (`` `clean` is not `plan_safe`. ``) |
| D | REPLACE one phrase inside the registry row | original 563, the substring `1 at least one unpermitted host_mutation/package_query/live_probe finding (\`findings\`)` |

---

## BLOCK A — REPLACE original lines 525-540

### Post-hoc transcript tripwire (round 17; evidence markers round 20)

After every wave and before writing anything about seat conduct, run
`python3 -I tools/mado-tripwire.py --scan <session-dir>/<Lane>R<N>` over the
round's seat transcripts (no `--permit` while the host pause holds) and quote its
first line, `counts`, `unparsed_spawns` and, from round 20, `observed_findings` and
`lead_findings`. A finding is an issued command to disclose in the lesson, not a
host-state fact: confirm package transactions against `/var/log/pacman.log` by
timestamp (UTC in transcripts, -0300 in the log) using the call's
`custom/tool_execution_start` time — a record's own timestamp can be minutes late for
provider-history records holding many calls. Round 17 found, in rounds 13-16, every
disclosed package transaction plus undisclosed elevated/query calls (lesson
`round-17.md` M2); breaches outside its classes (jj, /proc reads, file misroots) are
not findings. Its `--scan` entry stays a probe: it reads mutable transcripts. Round 18
adds the gate entry `--frozen` (registry row `mado-tripwire-frozen`): a digest-pinned
replay of committed incident lines.

**Evidence markers (round 20 target).** Every finding row carries `"evidence"`:

- `observed`: the transcript states the command AND the path that runs it: a bash
  `command`, a `!` or `%%bash` line, a literal spawn (subprocess, os, asyncio,
  `tool.bash`, including a spawn alias bound in the same text), or a call with literal
  argv to a helper (def, async def or lambda, decorated or not) whose body is visible
  in the transcript and reaches a spawn with that argv. A helper body counts only when
  it sits in the same cell or an earlier py eval cell of the same file with no `reset`
  cell between.
- `lead`: a literal positional `['prog', ...]` argv that classifies as a host command,
  handed to a callee whose body is NOT visible (an unbound bare name, or a name
  imported from a module outside the known-pure stdlib set). A lead records that the
  argv is stated outright. It does not record that the callee ran it: a helper that
  only formats or logs the argv produces a lead too.
- A row with no `evidence` key is an unmarked row. Tool output before round 20
  (including `367be947`) has none. The comparator reads an unmarked row as observed;
  a report must not read it as proof that a callee executed anything beyond the
  command text it quotes.

The verdict keeps lead rows in `findings` (exit 1, label `findings`). Read
`observed_findings` and `lead_findings` separately. Never report a lead as an executed
command.

**Binding guard (round 20 target).** A builtin or known-pure callable (`frozenset`,
`print`, `json.dumps`, `shlex.join`, `collections.*`, `functools.*` other than
`partial`/`wraps` over a spawn, ...) keeps its exemption from helper-argv leads only
while the text does not rebind it. A def, lambda, assignment or import of the same
name removes the exemption, and the binding in effect at the call decides: the latest
preceding binding, across earlier py eval cells of the same file. `del name` or a
`reset` cell unbinds the name; a literal-argv call to it is then a lead. A class,
dataclass, NamedTuple, lambda or def visible in the transcript counts as pure when its
body has no spawn and no call that would itself be observed or a lead (transitively,
depth <= 4).

The guard exists because of the round-19 harm. At `367be947` the data-only cell
`BLOCK=frozenset(['pacman','-Q','hyprland'])` yields `package_query / pacman:-Q`
with no evidence key (checked 2026-10-20 on a /tmp fixture that was scanned, never
executed). It is not a spawn and not a call.

Limits of the guard (stated, not hidden):

- Text only, read in textual order. It does not model execution order: a binding
  inside a function body that runs later, or inside a loop or conditional, is judged
  by where it appears. [INFERENCE: the target says "latest preceding binding"; nested
  control-flow behaviour is not verified.]
- A binding the text does not show is invisible: a name bound in a cell that is not in
  the transcript, `exec`, `globals()`/`setattr`, `importlib`, `from m import *`,
  `builtins.<name> = ...`, or a binding in another file. A name the guard treats as
  pure can be rebound at runtime.
- A call through an invisible path to a spawn is outside the classes. It becomes a
  lead only when handed a literal argv and the callee is unbound or imported from an
  unknown module.
- Module-level variable resolution keeps its round-17 limits (straight-line,
  literal-only recipes).

**Help and dry-run carve-outs (round 20 target).** A `vcs_write` row is NOT produced
when the invocation only prints help or is a dry run:

- help: `git <sub> -h|--help`, `git --help <sub>`, `git help ...`, `jj ... -h|--help`
  as a flag (not as an option's value), `jj help ...`;
- dry run: `git commit --dry-run`, `git add -n|--dry-run`, `git push -n|--dry-run`,
  `jj git push --dry-run`.

These still produce a row, as writes:

- `git commit -n` (this is `--no-verify`, a real commit);
- a dry run followed by a real write in the same text: each command is judged, and the
  real write keeps its row;
- `-m --help` (the help string is an option's value, so the commit is real).

Verified 2026-10-20 on /tmp fixtures at `367be947` (no fixture executed):
`git commit --dry-run -m x`, `jj git push --dry-run` and `git commit -h` still each
produce one `vcs_write` row, and `git commit -n -m x` correctly does too. The carve-outs
are not in force until C1 lands. Any other form keeps its existing behaviour.

**Written-script blindness (kept explicit).** `--scan` reads the command text of each
call. It does not read the contents of a file one call writes and a later call runs
(`cat > x.sh <<EOF`, `printf ... > x.py`, a `write` tool file followed by
`bash x.sh` or `python3 x.py`). Such a script is clean whatever it runs. Verified
2026-10-20 at `367be947`: a call writing `/usr/bin/pacman -Q hyprland` into `x.sh`,
followed by `bash /tmp/.../x.sh`, gives `MADO_TRIPWIRE: clean`, exit 0. The round-19
SentinelGatePath run of `/usr/bin/hyprctl probe` inside a written-then-executed
`inns.sh` was not detected by this scan; it surfaced by self-report. A `clean` over a
wave in which seats wrote scripts is therefore not evidence that no host command ran.
Record each written script's path and sha256 and read the script directly.

---

## BLOCK B — APPEND after original line 540 (after block A, before the blank line preceding `## Gate registry`)

### Isolation harness (round 20)

A harness that runs code near host surfaces (a stub `PATH`, a bind mount, a namespace)
MUST fail closed, meaning every setup failure exits before any payload runs.

1. Setup before payload, each step checked on its own. Use `set -eu`, and follow every
   mount, bind, copy and `cmp` step with an explicit `|| exit 99`. The chain
   `[ -e PATH ] && mount ... && echo ok` is forbidden: `&&` chains do not trip `set -e`.
   Round 19's SentinelGatePath used that shape; the mount failed ("must be superuser"),
   and `/usr/bin/hyprctl probe` ran against the real binary (rc 0, `unknown request`)
   shortly before 2026-10-20T18:05Z. Its later `inns.sh` exits 99 or 98 unless every
   bind succeeds and `cmp` confirms the bytes; that is the shape to copy.
2. Verify before payload: `cmp` each stub or bind against its expected bytes, confirm
   the host binary is not reachable through the harness `PATH`, and exit 98 on any
   mismatch. The payload line is never reached after a failed check.
3. Payload is a canary write into a fresh `/tmp` directory (for example
   `printf x > "$CANARY"`, then the check that the file exists there). Never a host
   binary, device, socket, compositor or service call.
4. Stub only `/tmp` paths, or bind inside a mount namespace whose setup step 2 verified.
   Unset `HYPRLAND_INSTANCE_SIGNATURE` and `WAYLAND_DISPLAY` in the harness environment;
   a leaked value reaches the real compositor.
5. Under the host pause, no harness and no seat may run the live gate
   (`tools/mado-verify.sh` without `--selftest` or `--regression`), a real `hyprctl`,
   `pacman`/`yay`/`paru`, `systemctl`, or any `omarchy-*` command, even to test the
   harness. Selftests use canaries only.
6. Record the harness path, its sha256 and each run's exit code (99 setup failure,
   98 verify failure, 0 only after the canary exists). Exit 0 without the canary is not
   evidence the payload ran.
7. The tripwire does not read harness scripts (see written-script blindness above).
   Review the harness code by reading it, and cite the sha256 in the report.

---

## BLOCK C — APPEND after original line 600

Round-20 tripwire limit (target; applies once C1 lands): `evidence` separates what a
transcript states from what it hands to an invisible callee; neither marker is proof of
execution. `observed_findings` is not an executed-command count and `lead_findings` is
not a host-command count. The binding guard and the help/dry-run carve-outs narrow false
positives only where the text itself shows the binding or the flag; they add no coverage.
Written scripts, invisible bindings, dynamic lookup and other sessions remain outside the
scan, as the round-17 limit above states.

---

## BLOCK D — REPLACE one phrase in the registry row at original line 563

Find (exact substring):

```
1 at least one unpermitted host_mutation/package_query/live_probe finding (`findings`)
```

Replace with:

```
1 at least one unpermitted finding of any class, lead rows included (`findings`; the verdict adds `observed_findings` and `lead_findings`)
```

Reason: at `367be947`, a `tool_install` fixture (`uv tool install ruff`) and a `vcs_write`
fixture (`git commit --dry-run -m x`) each exit 1 with label `findings`. The original
phrase lists only three classes and omits both. The lead rows also exit 1 under the
target contract, and the phrase must say so.
