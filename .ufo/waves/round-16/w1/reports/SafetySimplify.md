# Round 16 · SafetySimplify — scope review of the static action-plan gate

Lane: `mado-shokunin` · baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` · seat: simplifier (leaf, source reading only).
No install, no package/service operation, no live compositor/input/command probe, no edits outside this report.

## Verdict

The dispatched gate (`SafetyGate`, `.ufo/waves/round-16/w1/dispatch.json`) is
buildable, but its scope is larger than the safety claim it can honestly make.
The minimal bounded version is a **schema check plus one exact-match allowlist over
`argv[0]`**. It needs no shell parsing, no basename logic, no `paused` flag, no
`repo-write` kind, and no `--frozen` mode this round. Every removal below is
justified by a source anchor or by a concrete bypass.

## Sources read (anchors)

- Dispatch brief, task `SafetyGate` and `SafetySimplify` in `.ufo/waves/round-16/w1/dispatch.json` (the `taskCall.tasks[]` block) and `spec.json` items `SafetyGate` and `SafetySimplify`.
- `corpus/lessons/round-15-verifier-spotcheck.md:254-277` (R15-V1 host partial upgrade; R15-V2 procedural: plan must be real `pacman -Sp`, hard-coded fixtures are not validation).
- `corpus/lessons/round-15.md:15` (M2: `pacman -Sp --print-format '%n %v'` new-only rule) and `:51-73` (Gate candidate decisions).
- `SKILL.md:31` (read-only substrates), `SKILL.md:57-60` ("mado writes none of them"), `SKILL.md:105` (hyprctl read verbs), `SKILL.md:66` (`omarchy menu keybindings --print`), `SKILL.md:125,141` (`systemctl`, `pgrep`, `busctl`, `hyprctl -j layers` as read probes).
- `SKILL.md:507-515` gate registry: the frozen-regression rows pin the **executables** (`gate.sh`, `harness.sh`, `verify.py` digests in `expected.json`), not inputs. Existing gate convention: `--selftest` with in-process/subprocess fixtures and exit 0/1/2.
- `corpus/knowledge/gate-standing-use.md:24-40` (single writer; read-only on every substrate; exit map).
- `tools/` contains only `mado-verify.sh`; `tools/mado-action-plan.py` does not exist yet.

## Finding 1 — No shell parsing is needed; the input must be argv only

The plan schema already carries `argv` as a JSON list. Shell strings are then not a
gate concern at all: a string-form `command`/`cmd`/`shell`/`script` key is a schema
error (exit 2), and any shell wrapper such as `["sh","-c","…"]` is refused by the
argv[0] allowlist (Finding 3). **Remove** every quoting, `;`, `&&`, `|`, redirection,
`$()`, and `-c` analysis from the design. The gate states plainly that it classifies
declared argv vectors, not shell text.

## Finding 2 — The named denylist is a bypass, so drop it in favour of an allowlist

The `SafetyGate` brief refuses basenames `pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env` for `read-source`/`repo-write`. A denylist of wrappers is never complete. Concrete passes under that denylist:

- `["xargs","pacman","-S","libinput"]` — `xargs` not listed.
- `["nice","-n","0","pacman",…]`, `["timeout","60","pacman",…]`, `["nohup",…]`, `["setsid",…]`, `["stdbuf",…]`, `["busybox","pacman",…]`, `["doas",…]`, `["pkexec",…]`, `["su","-c",…]`, `["python3","-c",…]`, `["perl","-e",…]`, `["find",…,"-exec",…]`, `["command","pacman",…]`, `["exec","pacman",…]`.

The exact R15 transaction (`sudo pacman -S --needed --noconfirm libinput libinput-tools`) is caught only because `sudo` and `pacman` are named. A new wrapper name defeats the check silently. **Replace with an exact allowlist:** `argv[0]` must equal an allowlisted name exactly (no path component). Anything else under `read-source` is refused. This is fail-closed by default and needs no basename function, no path normalization, and no wrapper inventory.

Proposed starting allowlist (read-only utilities; `find` excluded for `-exec`/`-delete`):
`cat, head, tail, wc, stat, ls, file, readlink, sha256sum, grep, diff`.
The parent may trim or extend it; each addition needs a stated read-only justification. Do not add `sh`, `bash`, `env`, `xargs`, `find`, or any launcher.

## Finding 3 — Denylist and allowlist differ on the lane's own read routes; say so, do not hide it

`hyprctl`, `systemctl`, `omarchy`, and `libinput` are read routes the lane is permitted to use (`SKILL.md:66,105,125,141`). The gate cannot separate `hyprctl -j binds` from `hyprctl reload` by executable name, and this round does not add argv-verb semantics. Under the allowlist they are **refused as `exec_not_allowlisted`**. That is intentional over-refusal, fail-closed. Consequence to record in the SKILL row and report: **a plan is not the route for these reads**; the lane's ordinary read path remains the way to run them, and the gate does not authorize them. No `read-source` plan containing those executables can be marked `plan_safe`.

## Finding 4 — `paused=true` is an unreadable predicate; remove it from the policy

A static classifier cannot enforce a host-wide pacman pause, and the spec does not say what `paused=true` does to classification. The only consistent semantics is "refuse every plan", which makes `plan_safe` unreachable under the persisted policy and makes the selftest's green path depend on a different policy. **Drop the field.** The pause is recorded in `LOG.md`/`round-15-verifier-spotcheck.md`; it is not a gate input. Tradeoff: a reader of the policy file will not see the pause; mitigate by stating it in the SKILL row and the report, not in dead JSON.

## Finding 5 — `repo-write` has no consumer; remove the kind

`SKILL.md:57-60` states mado writes none of its substrates. `PROVINCE.md` makes the lane read-only. Nothing in round 16 emits a `repo-write` action, and the lane's report writes happen through its own tools, not through an action plan. **Remove** `repo-write`. Tradeoff: if a future round genuinely needs a write-class plan, it adds a kind with its own allowlist and selftest, not a pre-declared empty branch.

## Finding 6 — `--frozen DIR` pins the wrong object; cut it this round

The brief's `--frozen` verifies digests of `plan.json` and `policy.json`. Those are the **inputs**. The registry's frozen convention (`SKILL.md:510,515`) pins the **executables** (`gate.sh`/`harness.sh`/`verify.py`) so that a changed classifier cannot pass an old expectation. A frozen mode that hashes only inputs proves nothing about the classifier and adds a second code path with its own failure modes. **Cut it.** If the parent wants a frozen row, pin the gate's own sha256 in the selftest's expected constants and register the frozen row later with `expected.json` that pins `tools/mado-action-plan.py` itself. Tradeoff: no tamper detection this round; the honest claim is "selftest-green at a stated sha", not "frozen".

## Finding 7 — Minimal decision rules (ordered; schema errors dominate)

Validate the whole plan before classifying any action, so a malformed later action can never be hidden by an earlier refusal:

1. **Exit 2 (could not evaluate)**, checked first, in this order:
   - plan or policy missing, unreadable, or not valid JSON (use `object_pairs_hook` to refuse duplicate keys — a silent last-key-wins is a bypass);
   - top level not an object, or keys ≠ `{"actions"}`;
   - `actions` not a non-empty list;
   - each action not an object with keys exactly `{"kind","argv"}`;
   - `kind` not a string in `{read-source, package-install, service-mutate, compositor-mutate, input-capture}`;
   - `argv` not a non-empty list; any element not a non-empty `str` without NUL.
   - Any string-form command key anywhere → schema error (covered by the exact-key rule).
2. **Exit 1 (refused, stable reason)**, first failing action in array order:
   - `kind != read-source` → reason = the kind name (`package-install`, `service-mutate`, `compositor-mutate`, `input-capture`);
   - `kind == read-source` and `argv[0]` not in the policy allowlist → reason `exec_not_allowlisted`.
3. **Exit 0** `plan_safe` otherwise.

Reason mapping (`pacman`→`package-install` etc.) is **not** added: one reason for disguised read-source executables keeps the code small. Tradeoff: a reviewer sees `exec_not_allowlisted` rather than "this is pacman"; the report text may name the executable, not the code.

The policy file contains only `allowed_exec` (the Finding 2 list) and `allowed_kinds: ["read-source"]`. Policy failures (not a list, empty, non-string, contains `sh`/`bash`/`env`/`xargs`/launchers) are exit 2.

## Finding 8 — What the gate cannot do (state in the registry row)

- It never executes argv and never inspects the host. Enforcement is the executor's responsibility; the gate is a pre-check on a declared plan, same limit as the round-15 `measure.py` rules.
- It does not catch an agent that runs `sudo pacman …` directly from its own shell. That is the exact R15-V1 event. The gate reduces the risk only for work that routes through a plan; it does not close R15-V1.
- Allowlist membership is a downstream claim about what the executor will run. A read-only utility can still be pointed at a writable path by its own flags; the gate does not inspect flags.
- Selftest-green proves the classifier's stated predicate on its fixtures, not a production guard.

## Minimal selftest set (subprocess, exit + stable finding)

1. valid read-source `["cat","x"]` → 0 `plan_safe`
2. kind `package-install` (argv `["pacman","-S","libinput"]`) → 1 `package-install`
3. kind `service-mutate` → 1; kind `compositor-mutate` → 1; kind `input-capture` → 1
4. read-source `["sudo","pacman",…]` → 1 `exec_not_allowlisted`
5. read-source `["xargs","pacman",…]` (wrapper bypass case) → 1 `exec_not_allowlisted`
6. read-source `["/usr/bin/cat",…]` (path form) → 1 `exec_not_allowlisted`
7. read-source `["hyprctl","-j","binds"]` (over-refusal case, Finding 3) → 1 `exec_not_allowlisted`
8. unknown kind `"repo-write"` → 2 (unknown kind is malformed)
9. `argv` string not list; empty `argv`; non-string element; NUL in element → 2
10. top-level extra key; `actions` empty; action extra key → 2
11. duplicate JSON key in plan → 2
12. missing plan file; invalid policy JSON; policy with `sh` in `allowed_exec` → 2
13. first-action refusal does not hide a later malformed action → 2 (validates whole plan first)

Pin the expected exit codes and finding strings as literal constants in the test table, independent of the classifier's own output format.

## Decisions requested from the parent (no action taken)

- Accept the allowlist (Finding 2) in place of the named denylist.
- Accept over-refusal of `hyprctl`/`systemctl`/`omarchy`/`libinput` reads (Finding 3).
- Accept removal of `paused`, `repo-write`, and `--frozen` (Findings 4–6).

If any of these is declined, the matching tradeoff above is the cost.

## Checks for L1 (not run by this seat)

- `python3 tools/mado-action-plan.py --selftest` → expect 13/13 fixtures, exit 0.
- Re-hash the file and record the sha256 in the report; the registry row cites it.
- Confirm the gate contains no `subprocess`, `os.system`, `shlex`, or `exec` call (static grep is sufficient; it is not execution).

No tools were installed or updated by this seat. No host or package state was read or changed.
