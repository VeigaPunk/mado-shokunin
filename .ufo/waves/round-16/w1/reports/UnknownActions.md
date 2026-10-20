# UnknownActions — fail-closed design review (mado round 16, w1)

Seat: `MadoR16.UnknownActions` (reviewer, leaf, read-only). Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: design of unknown/incomplete action-kind and malformed-argv controls for the static action-plan gate
(`tools/mado-action-plan.py`, `.ufo/waves/round-16/safety-policy.json`), owned by `MadoR16.SafetyGate`.

## Status

- **Gate artifact not present at review time.** `tools/` contains only `mado-verify.sh`; `tools/mado-action-plan.py`
  and `.ufo/waves/round-16/safety-policy.json` were both absent on re-check. Every finding below is therefore a
  design/spec finding against the `SafetyGate` prompt text in `.ufo/waves/round-16/w1/spec.json`, not a code finding.
  Re-review is required once `SafetyGate` lands.
- Nothing was executed: no gate, selftest, Python snippet, package, service, compositor or input probe. Stdlib
  behaviour cited below is from knowledge of Python, marked `[INFERENCE]` where not observed in this repo.
- No installs, no commits, no edits outside this report.

## Axes (named before iteration)

| Axis | Question | Read as |
|---|---|---|
| A1 unknown kind | Does any kind string outside the closed set reach an allow path? | fail-closed |
| A2 incomplete action | Missing/extra/duplicate keys, null, wrong container types | fail-closed |
| A3 malformed argv | Non-list, non-string elements, empty, control chars, path-shaped argv[0] | fail-closed |
| A4 executable classification | Can a read-source/repo-write action name a blocked program without matching the denylist? | bypass resistance |
| A5 exit contract | Is every error path a non-zero code, with the 0/1/2 split from SKILL `Gate registry` (SKILL.md:498+) honoured? | determinism |
| A6 no-execution | Does the gate ever exec argv, shell out or inspect the host? | invariant |

Lowest axis: **A4** (the spec fail-closes unknown *kinds* but not unknown *executables* inside an allowed kind).

## Findings (severity order)

### H1 — High: unknown executables inside `read-source` / `repo-write` are allowed (fail-open)

The spec (`SafetyGate` prompt) fail-closes unknown *kind* but for allowed kinds only refuses a fixed 12-name
denylist: `pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env`. Every other argv[0]
passes. Under that rule `["python3","-c","<anything>"]`, `["git","-c","core.pager=…"]`, `["find",".","-exec",…]`
or `["nice","pacman","-Qi"]` are all `plan_safe` (exit 0).

Exact-basename denial misses families actually present in this lane's own corpus:

| Blocked behaviour | Grounded example in corpus | Denylist hit? |
|---|---|---|
| Omarchy restart / theme / service actions | `omarchy-restart-waybar` (corpus `grep -rhoE` count 4), `omarchy-restart-hypridle` (3), `omarchy-theme-set` (8), `omarchy-toggle-idle` (11) | No — `omarchy` only matches the exact name |
| Raw input capture / replay | `libinput-debug-events` (3), `libinput-record` (4), `libinput list-devices` (5) | No — `libinput` only matches exact name |
| Compositor dispatch | `hyprctl dispatch` (7), `hyprctl keyword` (4), `hyprctl reload` (6) | Only via `hyprctl` basename; OK for that exact program |
| Service mutation | `systemctl --user` (42) | Yes, exact basename only |
| Wrappers that re-exec | `nice`, `timeout`, `nohup`, `setsid`, `stdbuf`, `xargs`, `doas`, `su`, `pkexec`, `run0`, `systemd-run`, `flock`, `busybox`, `command`, `exec` | No |
| Interpreters/shells not listed | `python3`, `perl`, `awk`, `dash`, `zsh`, `fish`, `ksh` | No |

Consequence: the `input-capture` and `service-mutate` kinds are enforced only by the **label** the plan author writes.
A plan labelled `read-source` that runs `libinput-debug-events` or `omarchy-restart-waybar` is accepted. The
round-15 lesson's stated limit (M2, `corpus/lessons/round-15.md:15`) is a label-free host event; a label-trusting
classifier does not close that class.

**Recommended control (fail-closed):** for `read-source` and `repo-write`, replace the denylist with an
**allowlist of bare basenames** (e.g. `cat`, `ls`, `stat`, `file`, `wc`, `head`, `tail`, `sha256sum`, `grep`) and
keep the spec's 12-name denylist as defence in depth. Any basename not on the allowlist → exit 1,
`unknown_executable`. Path-shaped argv[0] (contains `/`) → exit 2, `malformed_argv`, so `/usr/bin/x` and `./x`
never reach name matching at all. Argument-level exec flags (`find -exec`, `git -c`, `sort --compress-program`,
`tar --to-command`, `rg --pre`, `git --ext-diff`) should be excluded from the allowlist entirely or refused by flag
name; they are data-execution vectors even for an allowed basename.

If the operator instead keeps a denylist, it must at minimum add: exact-prefix families `omarchy-`, `libinput`,
`hypr`, `systemd`, `pacman`, `yay`, `paru`; the wrapper set above; interpreters `python`, `python3`, `perl`, `ruby`,
`node`, `awk`, `dash`, `zsh`, `fish`, `ksh`; and case-folded comparison. This is still open-ended by construction,
and the report must say so.

### H2 — High: `kind` strictness is undefined; an implementation can fail open here

The spec does not say whether `kind` matching is exact. Required, stated explicitly in the spec or the gate:

- `kind` must be a JSON **string**, compared by **exact** equality to the closed set
  `{read-source, repo-write, package-install, service-mutate, compositor-mutate, input-capture}`.
- No `strip()`, no case folding, no `_`/`-` normalization, no prefix or substring tests (`"package" in kind`).
- The classifier must dispatch on **allow-set membership**, never on **block-set membership with an else-allow**.
  `if kind in BLOCKED: … else: allow` fails open for any new or misspelt kind. Required form:
  `if kind == "read-source": … elif kind == "repo-write": … elif kind in BLOCKED: … else: refuse(unknown_kind)`.
- `kind` values that are not hashable (list/dict) must be rejected by the type check before any `set`/`dict`
  lookup; otherwise a `TypeError` escapes (see H5).

### H3 — Medium: malformed argv has no type rules in the spec

Spec says only "read-source (nonempty argv)". Required rules, all → exit 2 `malformed_argv`:

| Input | Required result | Why |
|---|---|---|
| `argv` absent, `null`, string, object, number | 2 | string argv must never be shlex-split |
| `argv: []` for **any** kind | 2 | argv required and nonempty for every kind, so a blocked kind never gets an ambiguous "blocked with no argv" result |
| element not `type(x) is str` (int, bool, null, list, object) | 2 | `bool` is an `int` subclass `[INFERENCE]`; use `type() is str`, not `isinstance` |
| element containing U+0000–U+001F or U+007F | 2 | NUL and newline make allowlist/executor disagreement possible |
| `argv[0]` == `""`, ends with `/`, or has no basename | 2 | `os.path.basename("pacman/") == ""` `[INFERENCE]`; an empty basename must never be "allowed" |
| `argv[0]` with whitespace, or non-ASCII outside `[A-Za-z0-9._+-]` | 2 | Avoids normalisation mismatch (`"pacman "`, Unicode lookalikes) with any executor that strips or NFKC-folds |
| `argv[0]` containing `/` | 2 (or 1 `path_executable` for read-source) | path-shaped names are out of the classifier's competence |
| extra argv elements | not a schema error | arguments are data; argument-level policy is out of scope and must be stated as such |

### H4 — Medium: action-object schema is open unless closed explicitly

- Exactly `{kind, argv}` per action; any other key → exit 2 `unknown_field`. Otherwise
  `{"kind":"read-source","argv":["cat","x"],"shell":true}` or a `cwd`/`env` field passes unnoticed and a later executor
  may honour it.
- Top-level: exactly `{actions}`; `actions` must be a JSON array (not object, string or null; iterating a dict
  yields keys, and iterating a string yields characters, which is a silent-pass path). Non-object elements → 2.
- **Empty `actions: []` must not return `plan_safe`.** A vacuous pass is readable as permission. Recommend exit 2
  `empty_plan`. Decision for the operator, but the default must be non-zero.
- Missing `kind` or missing `argv` in any action → exit 2 `malformed_action`, including for blocked kinds
  (incomplete ≠ blocked).

### H5 — Medium: exit-code contract has an escape to code 1

- Python's uncaught exception exits **1** `[INFERENCE]`. Code 1 is the spec's "failed stable reason" (refusal).
  So an internal crash (RecursionError on deeply nested JSON, `TypeError` from an unhandled non-string) reads as a
  policy refusal, not as could-not-evaluate. Required: a top-level `try/except` mapping every unexpected exception to
  exit 2 `internal_error`, and an explicit `exit 0` only after the whole plan validated and every action classified.
  No bare `except: pass` on the success path.
- Ordering: validate the **whole** plan (all actions) before classifying any. Then malformed-anywhere always yields
  2 regardless of position, and "blocked" appears only for well-formed plans. Without this, a plan with
  `[package-install ok, malformed]` could return 1 or 2 depending on iteration order.
- Mixed plan `[read-source ok, unknown kind]` → 1 `unknown_kind`. Mixed `[unknown kind, malformed]` → 2 (malformed dominates).

### M1 — Medium: JSON parsing ambiguities

- **Duplicate keys**: `json.loads` keeps the last value silently `[INFERENCE: stdlib behaviour, not executed]`.
  `{"kind":"read-source","kind":"package-install","argv":["x"]}` would be read one way by the gate and possibly
  another by a human or executor. Required: `object_pairs_hook` that raises on duplicates → 2 `duplicate_key`.
- **NaN / Infinity**: reject via `parse_constant` → 2 `malformed_plan`.
- **BOM and encoding**: read bytes, decode strictly as UTF-8, reject a leading BOM → 2. Unreadable or non-regular
  file (FIFO, directory, device) → 2 `plan_unreadable`. A FIFO `--plan` can hang the gate; check with `fstat`
  before reading and cap size (suggest 1 MiB).
- **Size/count caps**: e.g. 1000 actions, 256 argv elements → 2 `plan_too_large`. Cheap and removes a resource
  vector; optional.

### M2 — Medium: policy tamper surface for the kind set

- `paused` must be the JSON boolean `true`. `"true"` (string), missing, `false`, or extra top-level keys → 2
  `policy_malformed` or `policy_not_paused`. The spec's PolicyTamper wording ("reject invalid or nonpaused policy")
  confirms `paused: true` is a *precondition for evaluation*, not a mode in which the gate refuses everything; the
  SafetyGate prompt should say so, because "paused" is otherwise ambiguous.
- The **kind set is code, not policy.** A policy entry `"unknown-kind": "allow"` or a missing `"input-capture"` entry
  must be a policy error (exit 2), not a new permission. Policy keys must equal the code's closed kind set exactly.
- Frozen mode (`--frozen DIR`): hash the **same bytes** that are then parsed. Reading plan.json twice opens a
  TOCTOU window between digest check and classification. `[INFERENCE: standard TOCTOU reasoning]`.

### L1 — Low: tooling/ordering notes

- Denylist comparisons should be case-folded in any form the operator keeps (`PACMAN` is a different binary on Linux
  but a lowercase-only comparison is an avoidable bypass shape).
- `--selftest` fixtures must pass argv as data; the self-invocation runs only the gate, never the argv. (NoShell seat
  owns this; noted for the same class.)

## Required fail-closed control table (for SafetyGate and SafetyCases)

Exit convention: **0** `plan_safe`; **1** refusal with stable reason; **2** could-not-evaluate (malformed input,
policy, internal error). Matches the convention already used by this lane (SKILL.md gate registry, lines 498+).

| # | Input | Exit | Reason | Note |
|---|---|---|---|---|
| U1 | `kind` `"Read-Source"` | 1 | `unknown_kind` | no case fold |
| U2 | `kind` `" read-source"` | 1 | `unknown_kind` | no strip |
| U3 | `kind` `"read_source"` / `""` | 1 | `unknown_kind` | |
| U4 | `kind` `null`, `7`, `["read-source"]`, `{}` | 2 | `malformed_action` | type check first |
| U5 | `kind` missing | 2 | `malformed_action` | incomplete |
| U6 | `argv` missing / `null` / string `"cat x"` | 2 | `malformed_argv` | no shlex |
| U7 | `argv: []` on `read-source` | 2 | `malformed_argv` | spec says nonempty |
| U8 | `argv: []` on `package-install` | 2 | `malformed_argv` | argv required for every kind |
| U9 | `argv: ["cat", 1]`, `[null]`, `[["cat"]]`, `[true]` | 2 | `malformed_argv` | `type() is str` |
| U10 | `argv: [""]`, `["cat\u0000x"]`, `["cat\n"]` | 2 | `malformed_argv` | control chars |
| U11 | `argv: ["pacman/"]`, `["/usr/bin/"]` | 2 | `malformed_argv` | empty basename |
| U12 | `argv: ["/usr/bin/cat"]` read-source | 2 | `malformed_argv` | path-shaped argv[0] refused |
| U13 | `argv: ["libinput-debug-events"]` read-source | 1 | `unknown_executable` | allowlist; or `input_capture` under prefix denylist |
| U14 | `argv: ["omarchy-restart-waybar"]` read-source | 1 | `unknown_executable` | prefix family |
| U15 | `argv: ["python3","-c","…"]` read-source | 1 | `unknown_executable` | interpreter |
| U16 | `argv: ["nice","pacman","-Qi"]` read-source | 1 | `denied_executable` | wrapper |
| U17 | `argv: ["cat","file"]` read-source | 0 | `plan_safe` | control: allowed |
| U18 | `{"kind":"read-source","argv":["cat","x"],"shell":true}` | 2 | `unknown_field` | closed object |
| U19 | duplicate `kind` keys | 2 | `duplicate_key` | `object_pairs_hook` |
| U20 | `actions` object / string / null | 2 | `malformed_plan` | iterate array only |
| U21 | `actions: []` | 2 | `empty_plan` | never vacuous `plan_safe` |
| U22 | top-level JSON array | 2 | `malformed_plan` | |
| U23 | `[read-source ok, kind "x"]` | 1 | `unknown_kind` | |
| U24 | `[read-source ok, argv "cat x"]` | 2 | `malformed_argv` | malformed dominates |
| U25 | `[package-install, argv []]` | 2 | `malformed_argv` | incomplete blocked kind |
| U26 | `[package-install, valid argv]` | 1 | `package_install` | blocked by kind |
| U27 | invalid UTF-8 or leading BOM | 2 | `plan_unreadable` / `malformed_plan` | strict decode |
| U28 | `NaN` anywhere | 2 | `malformed_plan` | `parse_constant` |
| U29 | policy `paused: "true"` / missing / `false` | 2 | `policy_malformed` / `policy_not_paused` | |
| U30 | policy with extra kind `"unknown-kind":"allow"` | 2 | `policy_malformed` | kind set is code |
| U31 | `--frozen`: tamper plan or policy bytes | 2 | `snapshot_tampered` | digest the bytes actually parsed |
| U32 | injected unexpected exception (selftest only) | 2 | `internal_error` | not 1 |

U13–U16 depend on the classifier choice in H1; their expected codes are conditional on allowlist vs. denylist and
must be pinned to whichever is implemented, not both. U1–U12, U18–U32 are independent of that choice.

## Residual risk (not closed by any static classifier in this design)

- Argument-level execution (`find -exec`, `git -c`, `sort --compress-program`, `tar --to-command`) for any
  allowlisted basename. Requires argv-semantic rules or dropping those basenames; the spec does not provide them.
- Wrappers and interpreters **not yet enumerated**. Any denylist is open-ended; only an allowlist is fail-closed for
  unknown executables.
- Labels: a plan author who labels a host mutation `read-source` and uses an allowlisted basename is not caught.
  The gate classifies declared plans; it does not observe what runs.
- Symlinks and PATH resolution: the gate reads names, not files. A repo-local file named `cat` is still "allowed" by
  name. Not detectable without filesystem inspection, which the gate must not perform.
- `repo-write` has no path scope in the spec: `["rm","-rf","/home/…"]` as `repo-write` with a clean basename passes.
  Path scoping is a separate control and is unscoped here.
- The gate protects only plans that pass through it. An executor that bypasses the gate is out of scope.
- Hard-coded fixtures prove only the classifier's branches. They are not package validation, host safety, or proof
  that the operational install step ran. The round-15 lesson already states this (corpus/lessons/round-15-verifier-spotcheck.md:160-163).

## Verification gaps

- `tools/mado-action-plan.py` and `.ufo/waves/round-16/safety-policy.json` absent at review; H1–H5, M1–M2 unverified
  against code.
- No selftest or case run (contract forbids seat execution). L1 must run the gate's `--selftest` once after
  integration and check U1–U32 (or the subset whose conditional codes match the implemented classifier).
- Python stdlib behaviours marked `[INFERENCE]` (duplicate-key last-wins, `bool` ⊂ `int`, `basename("x/")==""`,
  uncaught-exception exit 1) need one confirmation by L1 during integration, not by this seat.

## Recommended handoff

1. `SafetyGate`: adopt H1 allowlist (or enumerated denylist with prefix families); schema-first validation; closed
   key sets; exit-2 `internal_error` wrapper; duplicate-key rejection; `paused` strictly `true`; kind set in code.
2. `SafetyCases`: include U1–U32 above, labelled by reason; pin the H1-conditional rows to the implemented classifier.
3. `NoShell` / `PolicyTamper` / `SafetyControlRed`: overlapping rows U29–U31 and the subprocess isolation note are
   theirs; this seat does not duplicate their ownership.
4. Lane docs (SKILL gate registry row, QUALITY criterion) are L1-owned; this report makes no edit to them.
