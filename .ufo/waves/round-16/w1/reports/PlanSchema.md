# PlanSchema — JSON action-plan schema ambiguity review (mado-r16-w1)

Seat: reviewer, leaf, `MadoR16.PlanSchema`. Axis: operability (C2 static gate design). Coverage not scored here. No verdict on promotion.
Method: source reading only. No gate, selftest, Python, pacman, or host probe was run. Claims about Python runtime behaviour are marked `[INFERENCE]` because they come from documented semantics, not execution.
Installs: none. Tools installed or updated by this seat: none.

## Status of the target

- `tools/mado-action-plan.py`: ABSENT at review time (`tools/` lists only `mado-verify.sh`).
- `.ufo/waves/round-16/safety-policy.json`: ABSENT at review time.
- The only schema definition is the prose in the SafetyGate task text: `dispatch.json:426` (also `spec.json:10`). It says: "schema plan object actions list of objects containing kind and argv list."
- Every finding below is a gap in that prose. Each one needs a decision before the gate is written, or the implementer will pick a default that the reviewers cannot check.

## Findings by severity

### H1 — `argv` type is unspecified; a string argv fails open (high)

Anchor: `dispatch.json:426` "argv list". Nothing says what happens when `argv` is a string, dict, number, or null.

- If the implementation reads `argv[0]` without a type check, a string such as `"pacman -S libinput"` gives `argv[0] == "p"`. Basename `p` is not on the deny list, so the result is `plan_safe`. That is fail-open.
- `argv` as a dict gives `KeyError`. `argv == ""` gives `IndexError`. These are only safe if they are caught and mapped to exit 2.

Recommendation: `argv` MUST be a JSON array with at least one element, every element a JSON string, else exit 2 `malformed_argv`. Type checks run before any basename logic. Strings are never split (no `shlex`).

### H2 — Unknown keys are not rejected; a second command field can smuggle execution (high)

Anchor: `dispatch.json:426`. The prose does not say whether extra keys in the top-level object or in an action object are allowed.

If extra keys pass, a plan like `{"kind":"read-source","argv":["cat","x"],"command":"pacman -S libinput"}` is classified on `argv` only. A downstream consumer that reads `command` would then run what the gate never saw.

Recommendation: strict schema. Top-level keys: exactly `actions`. Action keys: exactly `kind` and `argv`. Any other key gives exit 2 `unknown_key`. Missing keys give exit 2 `malformed_schema`.

### H3 — Exit-code collision: uncaught exceptions look like "unsafe" (high)

Anchor: `dispatch.json:426` "1 failed stable reason; 2 could-not-evaluate". Only the contract's exit 0/1/2 meanings are fixed.

`[INFERENCE]` An uncaught Python exception exits with status 1. Exit 1 is the "unsafe finding" code. So a crash in a malformed-input path reports as a classified failure, not as "could not evaluate". This is the same class of collision that round 15 found in `mado-verify.sh` (`exit=2` on refusals, `AttackMistake.md` CE4 / round-15 spot-check).

Recommendation: the entry point wraps the whole evaluation in one handler. Any exception not raised deliberately as a finding becomes exit 2 `could_not_evaluate`. Exit 1 is emitted only from the finding path. Selftest must include one fixture that forces an unexpected exception and asserts exit 2, not 1.

### H4 — Basename derivation has an empty-basename bypass (high)

Anchor: `dispatch.json:426` "refuse executable basenames pacman,yay,...". The derivation rule is not stated.

`[INFERENCE]` `posixpath.basename("pacman/")` returns `""`. So `["pacman/", "-S", "libinput"]`, if it reaches the basename check, yields an empty basename that is not on the list. Other shapes to close the same way: NUL or newline inside `argv[0]`, and a trailing or leading space.

Recommendation: `argv[0]` MUST match a fixed pattern: no control characters, no trailing `/`, no NUL. The basename is the last non-empty `/`-separated segment. An empty result gives exit 2 `malformed_argv`. Matching is exact and case-sensitive (Linux paths are case-sensitive; do not casefold, which would only add false positives).

### M1 — Empty `actions` is unspecified (medium)

Anchor: `dispatch.json:426`. `{"actions": []}` could return `plan_safe` (exit 0) or `could_not_evaluate` (exit 2).

Argument for exit 2: a plan with no actions can be a truncated or corrupted export. Recording it as `plan_safe` would let a generator bug look like a clean verdict.
Argument for exit 0: nothing is executed, so nothing is unsafe.

Recommendation: exit 2 `empty_actions`. This is a decision for L1, since it changes the `SafetyCases` expected codes. Whichever is chosen, `SafetyCases` and `ExitMap` must state the same value.

### M2 — Empty or missing argv on read-source/repo-write has no exit code (medium)

Anchor: `dispatch.json:426` "read-source (nonempty argv)". The prose says nonempty is a condition of the allowed kind. It does not say whether violating it is a finding (exit 1) or a malformed plan (exit 2).

Recommendation: exit 2 `malformed_argv` for `argv: []` or a missing `argv`, since the plan cannot be evaluated. `SafetyCases` already lists "missing argv"; its `expected_code` must be 2.

### M3 — `kind` values: type, case, and unknown kinds (medium)

Anchor: `dispatch.json:426`. The allowed and blocked kinds are listed. Not stated: whether `kind` must be a string, whether matching is case-sensitive, and what an unknown kind returns.

Recommendation:
- `kind` not a string, or not one of the known kinds exactly (case-sensitive): exit 2 `unknown_kind`. "Unknown or malformed fails closed" (`dispatch.json:426`) maps to exit 2, not exit 1.
- Known blocked kinds (`package-install`, `service-mutate`, `compositor-mutate`, `input-capture`): exit 1 with a stable reason per kind. The argv is not used to decide these, but its schema is still validated first (see M4).

### M4 — Precedence between schema errors and findings is unspecified (medium)

Anchor: `dispatch.json:426`, "Exit 0 clean finding plan_safe; 1 failed stable reason; 2 could-not-evaluate". With two or more problems in one plan, the contract does not say which code wins.

Recommendation (for FindingStability / ExitMap to confirm):
1. Parse and validate the whole plan (types, keys, kinds, argv shape) before any classification. Any schema error anywhere gives exit 2, even if an earlier action would have been a finding.
2. Only if the schema is valid, classify each action in list order. Any finding gives exit 1, and the output names the first finding by index.
3. No findings and a valid schema gives exit 0 `plan_safe`.

This keeps "malformed" from being masked by an earlier unsafe-looking action, and keeps the output deterministic.

### M5 — Duplicate keys, NaN, and Infinity (medium)

`[INFERENCE]` Python's `json` module accepts duplicate object keys silently (the last value wins), and accepts `NaN`, `Infinity`, and `-Infinity` by default. A plan with two `kind` keys could be read differently by a reviewer and a consumer that take the first.

Recommendation: `object_pairs_hook` rejects duplicate keys; `parse_constant` rejects the three non-finite literals. Both give exit 2.

### M6 — File decoding, BOM, size, and nesting (medium)

`[INFERENCE]` `json.loads` on text with a leading UTF-8 BOM raises. Non-UTF-8 bytes raise `UnicodeDecodeError` if decoding is not strict. Very deep nesting raises `RecursionError`. A very large file has no defined bound.

Recommendation: read bytes; decode strictly as UTF-8; reject a BOM; enforce a fixed size cap (value to be chosen by ExitMap); all failures exit 2. The same rules apply to `--policy`.

### M7 — Argv element types and control characters (medium)

Anchor: `dispatch.json:426` "argv list" with no element type.

Recommendation: every element must be a JSON string. Non-strings (number, bool, null, array, object) give exit 2 `malformed_argv`. Elements containing NUL or a newline give exit 2, because a downstream consumer may truncate or split on them. The gate never executes argv (`dispatch.json:426`), so element contents only matter for classification and for what a consumer might later do.

### M8 — Policy as source of truth is ambiguous (medium)

Anchor: `dispatch.json:426` "Persist policy paused=true, allowed kinds ...". If the policy file carries the allowed kinds and denied basenames, a tampered policy can allow `package-install` or remove `pacman` from the deny list. The gate would then be policy-driven, not pinned.

Recommendation:
- The deny lists (kinds and basenames) are constants in `mado-action-plan.py`. The policy can carry `paused` and identity fields only. The policy cannot widen allowed kinds or remove denies.
- `paused` MUST be the JSON boolean `true`. The string `"true"`, the number `1`, or any other value gives exit 2 `policy_not_paused` or `malformed_policy`. (`PolicyTamper` owns the exit-code choice; this seat recommends exit 2, matching the "2 could-not-evaluate ... policy" line at `dispatch.json:426`.)
- Unknown policy keys give exit 2.

### M9 — `--plan`/`--policy` versus `--frozen DIR` (medium)

Anchor: `dispatch.json:426`. The prose lists `--plan PATH --policy PATH` and separately `--frozen DIR`. It does not say whether they combine.

Recommendation: `--frozen` is mutually exclusive with `--plan`/`--policy`; combining them gives exit 2 at argument parsing. `FrozenDesign` should confirm this.

### L1 — Basename deny list is a closed list; coverage limits must be stated (low, scope)

Anchor: `dispatch.json:426` lists `pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env`. This is a fixed deny list. It does not cover wrappers, alternate shells, or other package and host tools. These are not named in the list and are not blocked by it:

- Shells and wrappers: `dash`, `zsh`, `fish`, `busybox`, `xargs`, `nice`, `nohup`, `timeout`, `stdbuf`, `setsid`, `chroot`, `su`, `doas`, `pkexec`, `run0`, `systemd-run`.
- Interpreters that can spawn commands: `python`, `python3`, `perl`, `ruby`, `node`.
- Package tools: `makepkg`, `pacman-key`, `pacstrap`, `arch-chroot`, `pamac`.
- Input and compositor helpers: `ydotool`, `ydotoold`, `wtype`, `xdotool`, `wlrctl`, `swaymsg`, `input-remapper`.

`ExecBasename` owns the list. This seat's point is schema-level: argv[0] is the only element checked (see L2). Any review or report must say that the gate is a bounded declared-plan classifier, not a sandbox.

### L2 — Which argv element is checked is unspecified (low, scope)

Anchor: `dispatch.json:426` "refuse executable basenames". "Executable" suggests `argv[0]` only. Checking every element would flag `cat /etc/hosts` only if `hosts` were listed, which is noise; checking argv[0] alone lets `["python3","-c","..."]` through.

Recommendation: check `argv[0]` only, and say so in the gate docstring and in `SKILL` registry text. Do not claim that arguments are inspected.

### L3 — `repo-write` has no argument constraint (low, scope)

Anchor: `dispatch.json:426`. Beyond the basename check, `repo-write` places no limit on the arguments. `["rm","-rf","/"]` is labeled `repo-write`, has a non-deny basename, and is `plan_safe`. Likewise `git push`, `chmod`, and `dd`.

This may be intended for a bounded classifier. It must be stated as a residual, not implied to be safe. A future operator path that relies on `repo-write` being harmless would be wrong.

### L4 — Operator future dry-run is refused by design (low, note)

Under this schema, `{"kind":"read-source","argv":["pacman","-Sp","--print-format","%n %v",...]}` is refused by the basename rule, because `pacman` is denied for read-source. That matches "no package operations" this round. A later operator-authorized dry-run must not be routed through this gate and then read as a gate pass. The `-Sp` plan belongs to the operator path and is a separate check (`dispatch.json:426` mentions the future complete-name comparison).

## Suggested minimal schema (for SafetyGate and SafetyCases to agree on)

Exit 2 `malformed_schema` / `unknown_key` / `malformed_argv` / `unknown_kind` / `empty_actions` / `policy_not_paused` / `malformed_policy` / `could_not_evaluate` as appropriate; exit 1 only for the classified findings; exit 0 `plan_safe`.

```
plan    := { "actions": [ action, ... ] }        # exactly this key; nonempty (M1)
action  := { "kind": KIND, "argv": [ STR, ... ] } # exactly these keys (H2)
KIND    := read-source | repo-write | package-install | service-mutate | compositor-mutate | input-capture
STR     := JSON string, no NUL/control chars      # M7
argv[0] := nonempty, no trailing "/", basename not in DENY (H4, L1, L2)
policy  := { "paused": true, ... }                # bool true only; no widening keys (M8)
```

## Fixture cases to add (cross-reference SafetyCases; expected codes as recommended here)

| Case | Input | Expected |
|---|---|---|
| empty actions | `{"actions": []}` | 2 `empty_actions` (M1, decision pending) |
| actions as string | `{"actions": "pacman"}` | 2 `malformed_schema` |
| argv as string | `{"actions":[{"kind":"read-source","argv":"pacman -S libinput"}]}` | 2 `malformed_argv` (H1) |
| argv empty | `"argv": []` on read-source | 2 `malformed_argv` (M2) |
| extra key | action with `"command":"..."` | 2 `unknown_key` (H2) |
| non-string element | `"argv":[1]` | 2 `malformed_argv` (M7) |
| empty basename | `"argv":["pacman/","-S"]` | 2 `malformed_argv` (H4) |
| kind case | `"kind":"Read-Source"` | 2 `unknown_kind` (M3) |
| blocked kind | `"kind":"package-install"` + `pacman -S libinput libinput-tools` | 1 `package_install` (SafetyCases) |
| duplicate key | `"kind"` twice | 2 `malformed_schema` (M5) |
| NaN literal | `NaN` anywhere | 2 (M5) |
| BOM | leading U+FEFF | 2 (M6) |
| policy paused string | `"paused":"true"` | 2 `malformed_policy` (M8) |
| policy widening key | `"allowed_kinds":[...]` | 2 `malformed_policy` (M8) |
| uncaught exception | forced via selftest hook | 2, not 1 (H3) |

## Residual risk and verification gaps

- Nothing here is executed. Every `[INFERENCE]` marker needs confirmation by L1's single post-integration verify, or by a selftest case in the gate. This seat did not run Python.
- The deny list (L1) is a fixed set of names; it does not prevent execution through any wrapper not named. This is accepted as a bounded classifier, not enforcement.
- `read-source` does not restrict paths. A read-source `cat` of a credential file passes. `CredentialFence` owns that boundary.
- Exit-code assignments (M1, M2, M4) are proposals. `ExitMap` and `FindingStability` must confirm them; `SafetyCases` must then match.
- No host state was read. Installed-package claims are out of scope and were not checked.

## Changes to other seats' ownership

None made. This report is the only file written by this seat.
