# TripwireClassifierJoin — tripwire classes vs action-plan deny_executables and safety-policy

Round 17 connector report. Read-only: no gate, tool, scan, test or host operation was executed.
Measured lane state: HEAD `0175f13`; `tools/mado-tripwire.py` does not exist at report time
(checked through drafting). The fixture trees `.ufo/waves/round-17/tripwire/{core,compound}/` and
their `expected.json` landed during drafting and are used below as corroboration of rule tokens and
exit expectations, but the classifier itself is still **declared**: the comparison is against the
binding contract in the round-17 wave context (`gen_w1.py` `CONTEXT` / `w1/spec.json` `context`,
section "Tripwire interface"), which is what TripwireCore was dispatched to implement. If landed
code differs, re-diff §2–§4 against the code; the class names and rule tokens cannot differ without
breaking the fixture seats' `expected.json`.

## 1. The three vocabularies

| Artifact | Subject it classifies | Token set | Input model |
|---|---|---|---|
| `tools/mado-action-plan.py` (v1) | a **declared** action plan: `kind` + `argv` | findings: `plan_safe`, `blocked_action_kind:<kind>`, `denied_executable:<basename>`, `unknown_action_kind`, `empty_argv`, `plan_malformed`, `policy_malformed`, `snapshot_tampered`, `frozen_error`, `frozen_match`, `frozen_verdict_mismatch` (`:81-91`) | strict JSON; argv is data, never parsed or executed; first refusing action only (`_classify`, `:331-368`) |
| `.ufo/waves/round-16/safety-policy.json` | the policy instance for the above | `paused`, `paused_scope` = 4 kinds (`:4-9`), `deny_executables` = 12 exact basenames (`:10-23`), `kinds` = 6 (`:24-45`) | validated to **equal** the code constants `PINNED_PAUSED_SCOPE`/`PINNED_DENY_EXECUTABLES`/`PINNED_KINDS` (`:103-120`, checks `:253-270`); it is a committed copy, not an authoritative source |
| `tools/mado-tripwire.py` (declared) | **issued** bash/eval commands in OMP JSONL | classes: `host_mutation`, `package_query`, `live_probe`; rule = `<argv0>` or `<argv0>:<verb>`; `--permit CLASS` | shlex with `punctuation_chars=True`, segment splitting, wrapper stripping, recursion; all findings across all lines |

Schema names are likewise disjoint: `mado-action-plan-verdict-v1` carries one `finding` plus
`action_index`/`action_kind`/`detail`; `mado-tripwire-verdict-v1` carries `files`, a `findings`
list, `counts`, and `permitted`. They share only the two-line stdout shape (`MADO_PLAN:` /
`MADO_TRIPWIRE:` then one JSON line) and the exit convention `0` clean, `1` refusal/finding,
`2` could-not-evaluate with `2` winning over `1` (action-plan `:93`; context "Exit:").

## 2. Shared vocabulary

Genuinely shared, end to end:

- **Exit convention** `0` clean / `1` refused-or-finding / `2` could-not-evaluate, `2 > 1`.
- **"Clean is bounded"** wording: `plan_safe` "passed finite kind/argv[0] screen; not permission or
  safety" (`:365-366`); the tripwire's docstring is contractually required to state post-hoc,
  toolCall-only limits.
- **The 12 deny basenames** are the largest shared artefact: `pacman yay paru systemctl hyprctl
  omarchy libinput evtest sudo sh bash env`; the tripwire's rule table re-uses these names as
  `argv0` tokens (plus `zsh`, `dash`, `doas`, `pkexec`, `pkill`, `kill`, `killall`, `mkinitcpio`,
  `bootctl`, `grub-mkconfig`, `paccache`, and the live-probe/package-query names).
- **Intent overlap**: `host_mutation` covers the four denied kinds' effects;
  `live_probe` covers the probe-shaped deny names; `package_query` covers the pacman query verbs
  that the policy refuses only by name.

Nothing else is shared. No token is identical across the class and kind sets: the policy says
`package-install`, the tripwire says `host_mutation`; the policy says `input-capture`, the tripwire
has no such class. A script cannot join the two verdicts mechanically; a human needs the crosswalk
below. The word *mutation* appears in both (`host_mutation` vs `service-mutate` etc.), which invites
a false equivalence but is not one.

### Crosswalk a reader must apply by hand

| Policy token | Tripwire token | Notes |
|---|---|---|
| `blocked_action_kind:package-install` | `host_mutation`, rule `pacman:-S` (fixture-specified) and the analogous yay/paru mutating forms (`-Sy -Su -Sw -U -R -D`) | policy reads a declared kind; tripwire must parse the verb |
| `blocked_action_kind:service-mutate` | `host_mutation`, rule `systemctl:<verb>` | tripwire also splits read-only verbs out |
| `blocked_action_kind:compositor-mutate` | `host_mutation`, `hyprctl:<verb>`, `hyprpaper`, `hyprsunset` | |
| `blocked_action_kind:input-capture` | **`live_probe`**, rules `libinput`, `evtest` | class **differs**; see §3.3 |
| `denied_executable:sudo` | `host_mutation`, rule `sudo`, and the wrapped command classified too | tripwire recurses; action-plan does not |
| `denied_executable:pacman` (any argv) | `host_mutation` **or** `package_query` | same default exit 1, different token |
| `denied_executable:sh` / `bash` / `env` | **no finding for the wrapper** — recursed or stripped | opposite direction; see §3.1 |
| `read-source` / `repo-write` | no analogue | transcript commands are processes, not OMP tool calls |

## 3. Inconsistent names and semantics (evidence, then consequence)

### 3.1 `bash` / `sh` / `env`: denied by the plan gate, recursed-into by the tripwire

- Action-plan: any allowed-kind action whose `argv[0]` basename is `bash`, `sh`, or `env` returns
  `denied_executable:<name>` exit 1 (`:358-361`). Pinned cases: `read_source_bash_shell`
  (`safety-cases.json:174`, `bash -c "cat corpus/SOURCES.md | grep S051"` → `denied_executable:bash`),
  `read_source_sh_shell` (`:187`), `read_source_env_wrapper` (`:200`).
- Tripwire: `bash|sh|zsh|dash -c STR` and `eval STR` are **recursed into**; `env [-opts]
  [VAR=val...]` is stripped. `bash -c 'cat corpus/SOURCES.md'` therefore yields no finding.
- Consequence: the same shell text gets opposite verdicts — `denied_executable:bash` / exit 1
  versus `MADO_TRIPWIRE: clean` / exit 0. This is not a bug in either tool: the plan gate screens a
  *declaration* and cannot inspect a payload, so it treats uninspectable wrappers as refused; the
  tripwire inspects what ran and reports the payload. But the two results must never be presented as
  the same judgement: **`clean` is not `plan_safe`**, and `plan_safe` is not evidence a command ran.
- The wrapper sets are also unequal in the other direction: `zsh`, `dash`, `doas`, and `pkexec` are
  absent from `PINNED_DENY_EXECUTABLES` (`:109-112`), so a declared `read-source` plan
  `["zsh","-c","pacman -S x"]`, `["doas","pacman","-S","x"]`, or `["pkexec", ...]` is `plan_safe`
  by the code path at `:331-366` (basename not in the set), while the tripwire classifies the zsh
  payload, and `doas`/`pkexec` themselves, as `host_mutation`. This is a finite-screen limit, not a
  hidden control: the policy's own `scope_limit` (`safety-cases.json:17`) says the gate is only a
  12-basename screen, and `:9-13` says "not arbitrary shell analysis".

### 3.2 `omarchy` (exact) vs `omarchy-*` (glob) — a pinned contradiction

- Policy: the literal basename `omarchy` (`safety-policy.json:16`); action-plan matches exact
  basenames only (`:358`). `omarchy-pkg-add` is explicitly pinned **allowed**:
  `residual_control_omarchy_pkg_add_unscreened`, `safety-cases.json:494` → `plan_safe` exit 0.
- Tripwire: `omarchy-*` is split by name substring — `restart|refresh|install|update|remove|
  theme-set|toggle|launch` → `host_mutation`; all other `omarchy-*` → `live_probe`. `omarchy-pkg-add`
  contains none of those substrings, so it is a `live_probe` **finding** (exit 1 by default).
- Consequence: a command one artefact pins as clean, the other reports as a finding, and the name
  shapes do not even intersect (`omarchy` is not `omarchy-*` and vice versa). For the round's
  purpose (detect R15-shaped harm) the tripwire being stricter is defensible — `omarchy-pkg-add
  libinput` is exactly the install-adjacent helper the policy's residual case leaves open — but it
  means the tripwire is **not** "the policy applied to transcripts", and its `omarchy` handling
  should be described as a deliberate widening, not as policy alignment. `omarchy-launch-screensaver`
  is `host_mutation` by the tripwire and `plan_safe` by the policy, the sharpest divergence.

### 3.3 `libinput` / `evtest`: `input-capture` in the policy, `live_probe` in the tripwire

Both names are in `deny_executables` (`:17-18`) and are the canonical `input-capture` denied kind
(`:42-44`). The tripwire puts them in `live_probe`, not `host_mutation`. Default exit is 1 either
way, but the class token is what `--permit` acts on: `--permit live_probe` would waive a
`libinput debug-events` finding, and the same permit also waives `grim`, `slurp`, `hyprpicker`,
`waybar`, `hyprlock` and `hypridle`. The policy treats input capture as a denied *kind*; the tripwire
has no class of that granularity. This is the highest second-order hazard in the comparison: a
permit chosen for benign `hyprctl version`-class probes silently covers input capture and
screenshots. Fixtures may pin this; the limit paragraph should state it, because "permit live_probe"
reads narrower than it is. Whether a permitted finding stays visible in `findings` is itself
unresolved — see §3.7.

### 3.4 `pacman -Q` / `-Sp`: `package_query` vs `denied_executable:pacman`

The policy refuses pacman wholesale by name, including pure queries; round-16 M5 records that even a
read-only `pacman -Q waybar` was a pause breach (`corpus/lessons/round-16.md:18`). The action-plan
therefore returns `denied_executable:pacman` for `pacman -Sp ...`
(`read_source_disguised_pacman_plan_mode`, `safety-cases.json:148`). The tripwire returns
`package_query`. Both exit 1 with no permit, so the default verdicts agree; the tokens do not.
The tripwire additionally *can* express `--permit package_query` → exit 0, a state the paused policy
cannot express at all. **During the host pause, `--permit package_query` should not be used in any
evidence invocation**: it would green-light the exact round-16 M5 breach class. Permits belong in
fixture cases that test permit semantics, not in the real-transcript receipts.

### 3.5 Wider-than-policy tripwire rules (intended strictness, not drift)

`systemctl status|show|...`, other `hyprctl` verbs, `journalctl`, `loginctl`, `waybar`, `walker`,
`hypridle`, `hyprlock`, `alacritty`, `wev`, `wlr-randr`, `grim`, `slurp`, `hyprpicker`, `busctl`,
`dbus-send`, `gdbus`, `notify-send`, `makoctl`, plus `expac`, `pactree`, `checkupdates`, and
`pkill|killall|kill`, `mkinitcpio`, `bootctl`, `grub-mkconfig`, `paccache` are tripwire-only. Under
a `read-source` declaration most of these are `plan_safe` because their basenames are outside the 12
(`:109-112`). The tripwire is stricter here, which serves C3; the registry/lesson must not present
the two lists as one list.

### 3.6 Finding multiplicity and ordering are not comparable

Action-plan returns the **first** refusing action (`:331-368`); the tripwire reports every finding
across every segment and line. The R15 red anchor is specified to produce **two** `host_mutation`
findings — rule `sudo` and rule `pacman:-S` (wave context fixture item; confirmed by
`core/expected.json:5-11`) — while
the plan-side analogue is a single `blocked_action_kind:package-install` if declared, or a single
`denied_executable:sudo` if mislabelled. The tripwire's `counts` therefore cannot be compared with
action-plan's single-finding verdicts, and neither tool's count is a call count (`files[].bash_calls`
/ `eval_calls` are the call counts).

### 3.7 Permit membership is contradictory between the two fixture suites

The interface says only "Exit: 0 no unpermitted finding; 1 at least one unpermitted finding" and the
schema carries both `findings` and `permitted`; it never says whether a permitted finding remains in
`findings`. The two landed `expected.json` files answer that differently:

- `core/expected.json:34-39` `live-probe-permitted`: `"permit": ["live_probe"]`, `want_exit: 0`,
  `want_findings: []` — permits are expected to **remove** the finding rows.
- `compound/expected.json:39-46` `var-assign-pacman-query-permitted`, `:120-128`
  `omarchy-permitted`, `:130-152` `dir-scan-all-permitted`: permit the same classes, expect exit 0
  but keep **every** permitted finding in `want_findings`.

The selftest contract compares "the exact multiset of (class, rule, line, basename(file))" against
`want_findings` (wave context, "Selftest:"), so under any single implementation one suite fails.
That blocks C3's "hermetic selftest N/N exit 0" claim until the interface sentence is fixed.
Recommendation: `findings` always lists every finding; `permitted` lists waived classes; exit 0 iff
`findings` minus permitted is empty. Then `core`'s `live-probe-permitted` must list its two
`live_probe` rows and `compound` stays as written. The alternative (filter permits out of
`findings`) makes the receipt lossy and makes a `--permit live_probe` scan of `libinput`/`evtest`
indistinguishable from clean — exactly the hazard in §3.3.

## 4. Should the tripwire load `.ufo/waves/round-16/safety-policy.json`? No.

1. **It breaks the stated trust boundary.** The interface opens with "never executes or inspects
   anything but the given JSONL files." A policy read is outside that boundary and makes scan
   availability depend on an unrelated path; a missing/moved policy would turn evidence into exit 2.
2. **There is no shared subject to apply.** The policy classifies declared `kind`s; the transcript
   has only shell text. Applying `blocked_action_kind` requires inferring a declaration from text —
   trusting the very declaration the tripwire is meant to verify — while `package_query` (the M5
   class) has no policy kind and `read-source`/`repo-write` have no transcript analogue.
3. **The verdict could not be bound.** `mado-tripwire-verdict-v1` has no `policy_sha256` field. A
   committed receipt would not identify which policy produced it, and the tripwire has no frozen
   mode. Round 16's `--frozen` is the correct precedent for a policy-sensitive tool: pin bytes,
   record the digest, replay. That is not in C3's scope.
4. **It would create retroactive verdicts.** The policy lives under a round-16 path
   (`.ufo/waves/round-16/safety-policy.json`, cited by `SKILL.md:543`); a later round may move or
   retire it. Historic scans would then fail or silently change. The tripwire's class table is
   code-pinned like `PINNED_*`; that is the stable thing.
5. **Literal application would contradict the tripwire's own rules.** `deny_executables` contains
   `bash`, `sh`, `env`; applying it would make `bash -c 'cat x'` and `env FOO=1 true` findings,
   against the interface's recursion/strip rules, and would produce false positives on ordinary
   clean reads the recursion rule is designed to classify cleanly. (This seat did not read the
   round 13–16 transcripts; the fixture/oracle seats measure those.)
6. **`paused` and `--permit` invert meaning.** `paused: true` denies kinds; `--permit CLASS` waives
   classes. A mapping would let `--permit live_probe` waive `libinput`/`evtest` (`input-capture`, the
   policy's most sensitive denied kind) and `--permit package_query` waive the M5 breach class. That
   is the opposite of the pause.

**Bounded move instead** (one proposal): do not add a policy input. Add a crosswalk sentence and the
§2 table to the tripwire's module docstring and to the SKILL limit paragraph beside the existing
"Round-16 classifier limit" text (`SKILL.md:547-556`), stating (a) the vocabularies are deliberately
disjoint, (b) `MADO_TRIPWIRE: clean` is **not** `plan_safe` and vice versa, (c) the two pinned
divergences (`bash -c 'cat …'`: policy denies, tripwire clean; `omarchy-pkg-add`: policy pins
plan_safe, tripwire live_probe), and (d) no `--permit` in real-transcript evidence while the host
pause stands. If L1 wants it executable, the fixture seats can add those two cases as documentation
fixtures; that still loads no policy.

## 5. Affected axes, risks, verification

Axes: **quality** improves if the disjointness sentence lands — it prevents an overclaim in
SCORECARD/SKILL that the tripwire is "the policy applied to transcripts". **Operability (C3)** is
unchanged: this is a description of the capability, not a new capability or a host action.
Coverage, calibration, freshness, depth, adjacency: unaffected. No axis is harmed; no scalar score is
asserted.

Risks to the round:

- If a report says the tripwire "shares the gates's vocabulary" or "applies allow/deny semantics",
  a closure can falsify it with two committed pins: `safety-cases.json:174` (bash denied) vs the
  tripwire recursion rule; `:494` (`omarchy-pkg-add` plan_safe) vs the tripwire's `live_probe`
  fallback. Phrase as crosswalk, never equivalence.
- If evidence scans use permits, `clean` stops meaning "no pause-class command": `live_probe` covers
  input capture and screenshots; `package_query` covers the M5 class. Run evidence scans without
  `--permit`.
- `kill -9`/`kill -0` are undifferentiated `host_mutation` in the tripwire while absent from the
  policy; `kill -0` is a pure existence check. That is a known over-classification direction, worth
  one line in the tripwire limit paragraph if the fixture seats did not already pin it.
- The permit-membership contradiction (§3.7) must be reconciled before any C3 "selftest N/N" number
  is cited: under either single implementation, one of the two fixture suites fails as written.
  That is an interface/fixture defect, not a classifier defect, and it is falsifiable without
  running the tool.

Verification (static; L1 alone executes):

1. `sed -n '103,120p;253,270p;331,368p' tools/mado-action-plan.py` — pinned sets, equality check,
   basename-only screen.
2. `cat -n .ufo/waves/round-16/safety-policy.json` — lines 4-9, 10-23, 24-45 as cited.
3. `sed -n '17,18p;148,220p;319,335p;494,520p' .ufo/waves/round-16/safety-cases.json` — scope
   limit, shell/pacman/probe cases, residual controls.
4. `sed -n '543,556p' SKILL.md` — registry rows and the existing classifier limit paragraph.
5. `sed -n '853,860p' SCORECARD.md` — C3 pre-registration wording the registry must stay consistent
   with.
6. When `tools/mado-tripwire.py` lands: `grep -n 'host_mutation\|package_query\|live_probe\|omarchy\|libinput\|bash\|env' tools/mado-tripwire.py`; confirm the rule table matches the interface before citing this report. The four cross-artifact controls to assert, if L1 wants them: `bash -c 'cat corpus/SOURCES.md'` → tripwire clean / plan `denied_executable:bash`; `pacman -Sp a` → `package_query` / `denied_executable:pacman`; `libinput debug-events` → `live_probe` / `denied_executable:libinput`; `omarchy-pkg-add libinput` → `live_probe` / `plan_safe`. Execute only under L1's integration verification; none were run here.
7. `grep -n 'permit\|want_findings' .ufo/waves/round-17/tripwire/core/expected.json .ufo/waves/round-17/tripwire/compound/expected.json` — shows the §3.7 divergence without running the tool: `core`'s `live-probe-permitted` expects `[]`, `compound`'s three permit cases expect the permitted rows.

No tools were installed or updated. No transcript was read or scanned by this seat.
