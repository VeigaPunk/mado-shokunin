# AttackSafetyLearning — QUALITY21 / SKILL pause propagation and conditional real-plan

Seat: `MadoR16.AttackSafetyLearning` (connector, leaf, no dispatch). Read-only.
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`, integrated artifacts at the
working tree (not the stale w1 absence observations).

Not run by this seat: `tools/mado-action-plan.py` (any mode), `measure.py`, any
gate, selftest, or test; no `pacman`/`pacman -Q`/`-Sp`; no package, service,
compositor, input, screenshot, or producer command; no `~/.omp/agent` access.
Every claim below is from reading source/JSON/markdown with `read` and `grep`.
"Traced" means I followed the code path by reading; nothing was executed.

Tooling: none installed, updated, or queried. Recorded per RULES: no install this round.

## Axes (named before iterating)

- **A1 Propagation** — does the pause reach every instruction a future seat reads
  (SKILL standing rules, QUALITY, wave contexts)?
- **A2 Conditionality** — is any future real `pacman -Sp` / installed-name step stated
  as conditional on an explicit operator lift, and is it never read as clearance?
- **A3 Claim fidelity** — does gate/lesson/QUALITY wording stay within the declared
  scope (declared-JSON classifier, 12-name list)?
- **A4 Harm accounting** — does the round-16 C2 gain avoid netting the unresolved
  round-15 operability harm on the same axis?

## Verdict summary

| Question | Verdict |
|---|---|
| Pause reaches seats (wave contexts) | **Holds.** w1 dispatch.json:421, w2 spec.json:3 and dispatch.json:229 each carry "All pacman transactions PAUSED host-wide … never -Sy/-Syu/-U/-R … After pause only operator-authorized future install may use real pacman -Sp …". |
| Pause reaches SKILL standing rules | **Partial.** Core statement at SKILL.md:39-44 and superseding paragraph at :483-491 are correct. Gaps F1, F2, F3 below. |
| Pause reaches QUALITY | **Holds for install/transactions/service/compositor** (QUALITY.md:82-100). Producer execution and package *queries* are not named there (F1, F2). |
| Future real-plan stated conditional, not clearance | **Holds in prose** (QUALITY.md:92-94; SKILL.md:484-488; lesson M2; LOG.md:1177-1179). **Not wired in the gate** (F4). |
| Gate wording within declared scope | **Mostly holds.** Declared limits appear in SKILL.md:533-539, LOG.md:1174-1177, safety-cases.json:17. Overclaim in QUALITY21 acceptance wording (F5). |
| C2 gain nets round-15 harm | **Not restated.** Round-16 SCORECARD section has no operability harm verdict (F7). |

## Findings

Severity is for the pause/clearance purpose. "Declared" means the limit is written
down somewhere in the lane; the finding is whether the *promise* outruns it.

### F1 — High — SKILL standing producer license was not superseded
- **Anchor:** `SKILL.md:231-236` (safety rule 2): "Running a producer script is allowed
  only when its source proves it pure-read and side-effect-free … and it runs contained."
- **Gap:** The round-16 supersession at `SKILL.md:498-507` is scoped to the Waybar
  `RUN` route for "what is showing now?". Rule 2 itself is untouched. The wave
  contract (`w2/spec.json:3`) forbids "command producer probes", and QUALITY21 says
  to carry "this round's no-live-probe scope into every seat context" (QUALITY.md:86-87).
  A future seat that reads SKILL rule 2 is licensed to run pure-read producers.
- **Prior recommendation not applied:** round-16 w1 seat report
  `.ufo/waves/round-16/w1/reports/CredentialFence.md:56-57` proposed an append: "While the host pause holds and in
  every source-only round, producer execution is suspended, including 'pure-read'
  producers. The SKILL.md:233-236 license … do not apply." Absent from SKILL.md.
- **Fix (L1, append-only):** add the sentence above under rule 2 or the pause bullet.

### F2 — Medium — SKILL pause bullet omits package queries and input capture
- **Anchor:** `SKILL.md:39-40`: "no package transactions or service/compositor
  mutations." Compare `safety-policy.json:4-9` (`paused_scope` includes `input-capture`)
  and `w2/spec.json:3` ("No package or service operations whatsoever").
- **Evidence the gap is real:** lesson `round-16.md:18` (M5) records that
  `CustomExec` ran `pacman -Q waybar` in its first batch. A read-only query is not a
  "transaction", so the SKILL text as written does not forbid it.
- **Overstatement:** `round-16.md:14` (M1) says "SKILL standing instruction propagates
  no package/service/live operations into both wave contexts." SKILL does not say
  "no package/service/live operations"; the wave contexts do. Correct the lesson wording
  or add the words to SKILL.
- **Fix:** extend the SKILL bullet to "no package transactions, package queries
  (`pacman -Q`, `-Sp`), service/compositor mutation, input capture, or producer execution."

### F3 — Medium — pause label is round-scoped; the operator pause is not
- **Anchor:** `SKILL.md:39`: "**Current host pause (round 16; supersedes …)**".
- **Contract:** the operator pause runs "until operator recovery decision"
  (`w2/spec.json:3`; `w1/dispatch.json:421`). QUALITY21 says "while the operator's
  host-wide pause holds" (QUALITY.md:82-83). A round-17 reader can take "(round 16;"
  as expiry at round end.
- **Fix:** replace "(round 16; …)" with "(until operator lift; …)".
- **Pointer:** `SKILL.md:473-481` (prospective install procedure, "Before any future
  install, `pacman -Sp …` must list …") has no inline pointer that it is superseded
  below at :483. `AppendOnly.md:118-126` (F1) already reports this; not re-attacked here.

### F4 — Medium — the conditional future real-plan step is not wired to the gate
- **Anchors:** `tools/mado-action-plan.py:113-120` (pinned kinds; `package-install`
  deny), `:233-235` (`paused` must be `True`), `:254-268` (kinds and dispositions must
  equal the pinned table, "mutation kinds … can never become allowed"),
  `:109-112` (`pacman` on the deny list). `safety-cases.json:148` /
  `:157-158` expects `read-source` `["pacman","-Sp",…]` → `denied_executable:pacman`.
- **Consequence (traced):** after an operator lift, the one step criterion 20 requires
  (`pacman -Sp --print-format '%n %v'`) is refused by the gate as a deny-listed
  executable. Any package-install plan is refused by kind. The only way to make the
  gate accept a post-lift plan is a code change to the pinned table, which
  `_validate_policy` would then reject against the code itself unless the code is
  revised. The gate is therefore **not** a post-lift validator, and no document says so.
- **Why it matters for clearance:** a future seat could read "the gate passes" as the
  real-plan check, or edit `safety-policy.json` to get past a refusal. Both paths are
  fail-closed today (`policy_malformed`), so this is an unwired conditional, not an open
  hole.
- **Fix:** state in QUALITY21 and SKILL.md:486-488: "The current gate does not validate
  a post-lift real plan; it refuses `pacman -Sp` and cannot admit package-install. Any
  post-lift use requires a new reviewed gate revision with re-pinned cases, plus an
  operator lift record; a policy-file edit is not a lift."

### F5 — Medium — "disguised forbidden executable" is defined only by the 12-name list
- **Anchor:** QUALITY.md:88-90: the classifier "must fail on the incident-shaped
  libinput transaction, disguised forbidden executable, unknown kind, and malformed
  action." The cases that exercise "disguised" (`safety-cases.json:148-172`, `:289-300`,
  `:318-330`) all use listed names (`pacman`, `sudo`, `sh`, `bash`, `env`, `libinput`).
- **Scope text:** `safety-cases.json:17` and SKILL.md:536-538: "Unlisted argv[0] is NOT
  screened … arbitrary wrappers pass as plan_safe. This is by design."
- **Inconsistency:** the list screens some wrappers (`sudo`, `env`, `sh`, `bash`,
  `:109-112`) and not others (`xargs`, `nohup`, `timeout`, `doas`, `pkexec`, `su`,
  `nice`, `setsid`). The selection rule is not stated.
- **Fix:** QUALITY21 should define "forbidden executable" as "basename in the pinned
  list (`tools/mado-action-plan.py` `PINNED_DENY_EXECUTABLES`)". Negative cases beyond
  the list would then be residual controls, not acceptance evidence.

### F6 — High consequence, declared — `repo-write` allows any destination (declared limit)
- **Anchors:** `safety-policy.json:29-32` (`repo-write` allow, argv nonempty);
  `tools/mado-action-plan.py:335-347` (only argv[0] basename is checked; no path check).
- **Traced:** `{"kind":"repo-write","argv":["write","/home/vgpnk/.config/hypr/hyprland.conf"]}`
  → `plan_safe`, exit 0. SKILL.md:186-188 says Hyprland applies config saves
  immediately, so a green verdict can precede a live compositor change.
- **Declared:** SKILL.md:533-535 ("not … destination confinement"); LOG.md:1176-1177
  ("write destinations … not analyzed"). The promise is not overstated, but the
  consequence is high. The CLI detail string (`N action(s) allowed`) is precise.
- **Fix (optional, L1):** one sentence in SKILL.md:533-539: "A `repo-write` plan_safe
  does not cover writes under `~/.config`, which become live on save."

### F7 — Medium — round-16 C2 gain has no restated operability harm verdict
- **Anchor:** `SCORECARD.md:703-709` ("absent (0) → demonstrated (1)"). The round-16
  section (`SCORECARD.md:690-735`) contains no "harm" or "no-harm" statement.
- **Contrast:** round-15 `SCORECARD.md:665-668` ("operability safety: harmed") and
  `:679-684` ("no-harm condition unmet").
- **Why:** the contract requires moves that improve an axis and harm none. R15-V1
  (`round-15-verifier-spotcheck.md`, R15-V1) remains unresolved and is on the same
  operability axis. QUALITY21 says "no safety trade is erased" (QUALITY.md:99-100), but
  the scoreboard row does not carry that.
- **Fix:** add a line under C2: "operability: capability +1 (bounded declared-plan
  classifier); R15-V1 host harm unresolved; no-harm condition unmet."

### F8 — Low — the gate opens its input before the regular-file check
- **Anchor:** `tools/mado-action-plan.py:154` (`os.open(path, O_RDONLY|O_NONBLOCK)`),
  checked by `S_ISREG` at `:159`. The docstring says the gate "NEVER inspects host
  state" (`:7-8`).
- **Traced:** `--plan /dev/input/eventN` opens a device node before rejecting it.
  Symlinks are followed (no `O_NOFOLLOW`). Overlaps `AttackRegularFiles`; cross-reference
  only.

### F9 — Low — frozen mode hashes, then re-parses (cross-reference only)
- **Anchor:** `run_frozen` `:414-422` (`_sha256` reads, returns digest) and `:424`
  (`_evaluate` re-reads the file). The hashed bytes are not guaranteed to be the parsed
  bytes. Overlaps `AttackFrozenPins`.

### F10 — Low — wave context gives a bare filename for the required prior read
- **Anchor:** `w2/spec.json:3`: "Read round-15-verifier-spotcheck.md before work."
  The file lives at `corpus/lessons/round-15-verifier-spotcheck.md`; a `.ufo/waves/
  round-15` search finds nothing. Future contexts should use the full lane path.

## Positive controls (held under reading)

- Policy pin holds: `paused` must be exact `True` (`tools/mado-action-plan.py:233-235`);
  `kinds` must equal the pinned table (`:254-268`); `package-install` cannot be allowed.
- Incident-shaped `sudo pacman -S …` under `package-install` → `blocked_action_kind`
  (`safety-cases.json:32-42`); under `read-source` → `denied_executable:sudo`
  (`:289-300`). Both traced to `_classify` `:332-347`.
- Traced all listed negative/malformed cases against `_evaluate`/`_classify`
  (`:354-372`, `:319-349`): no mismatch found in the cases I walked. Not executed.
- Real-plan conditionality is stated in QUALITY.md:92-94, SKILL.md:484-488, lesson M2
  (`round-16.md:15`), LOG.md:1177-1179, and ClosureDebt V2-R3. None claims the step ran
  or was cleared.

## Bounded counterexamples (all traced, none executed)

Every plan below has `kind: "read-source"` unless noted. Exit 0 / `plan_safe` in each
case. The gate never executes argv, so none of these runs a command in practice; they
show what a green verdict does and does not cover.

1. `argv: ["xargs","pacman","-S","--noconfirm","libinput"]` → `plan_safe`. Basename
   `xargs` is not in `PINNED_DENY_EXECUTABLES` (`:109-112`). Declared wrapper limit (F5).
2. `argv: ["pacman-key","--refresh-keys"]` → `plan_safe`. Basename `pacman-key` ≠ `pacman`.
   Declared-list limit (F5).
3. `argv: ["uv","tool","install","x"]` (or `cargo install`, `npm -g`) → `plan_safe`.
   The operator tooling directive names these as install channels; the gate does not
   know them. Declared-list limit (F5). Only `package-install` kind would be refused.
4. `kind: "repo-write"`, `argv: ["write","/home/vgpnk/.config/hypr/hyprland.conf"]` →
   `plan_safe`. No destination check (F6).
5. Control (denied as designed): `argv: ["/usr/bin/pacman","-Q"]` → `denied_executable:
   pacman` (basename, `:311-316`). This is why "pacman -Q" is refused as a *plan*; it is
   not why the process breach in M5 is prevented.

## Proposed move (one bounded append bundle, L1-owned)

Improves A1, A2, A3, A4; changes no gate code, pinned policy, or case expectations;
harms no axis.

1. SKILL.md pause bullet (`:39-44`): round label → "until operator lift"; add package
   queries, input capture, and producer execution to the list (F1, F2, F3).
2. SKILL.md rule 2 (`:231-236`): append "suspended while the host pause holds and in
   every source-only round" (F1).
3. QUALITY.md criterion 21 (`:88-90`): define "forbidden executable" as the pinned list;
   state that the post-lift path needs a new reviewed gate revision (F4, F5).
4. SKILL.md classifier-limit paragraph (`:533-539`): one sentence on `repo-write`
   destinations under `~/.config` (F6).
5. SCORECARD.md round-16 C2 (`:703-709`): append the operability line in F7.
6. lesson `round-16.md:14`: replace "SKILL standing instruction propagates no
   package/service/live operations" with the scope that is actually propagated (F2).

## Risks

- Item 1 lengthens SKILL's pause bullet; keep it one bullet to avoid a second pause text
  that can drift.
- Item 3 narrows "forbidden"; it makes QUALITY21 more accurate but weaker as a promise.
  That is the correct trade under A3.
- No item here clears the R15-V1 host harm or claims host repair.

## Checks for L1 (not run here; L1 alone runs verification)

- `grep -n "producer" SKILL.md` — confirm rule 2 (`:231-236`) is still unsuperseded (F1).
- Run the gate once on fixtures for counterexamples 1–4 to confirm they return
  `plan_safe` (the gate does not execute argv; still L1's call).
- `python3 tools/mado-action-plan.py --selftest` and the frozen mode, as the lane
  already scopes them.
- Confirm no edit to `safety-policy.json` or `safety-cases.json` expectations is needed
  for items 1–6.

## Limits

- Read-only. No runtime behavior was observed; all verdicts are from source tracing.
- Did not reread lessons beyond the cited lines, or the w1 reports beyond the anchors
  cited.
- F8/F9 overlap sibling seats (`AttackRegularFiles`, `AttackFrozenPins`) and are not
  independently scored here.
