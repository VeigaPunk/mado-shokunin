# GateRegistry — mado-action-plan SKILL registry row draft (round 16, w1)

Seat: `MadoR16.GateRegistry` (leaf, no dispatch). Scope: draft registry row fields for the
planned static action-plan gate, including frozen-mode and static-not-enforcement limits. Source
reading only. No build, lint, test, selftest, gate or frozen run; no package, service, compositor,
input-device or host probe; no installs (none needed for this draft). No shared file edited;
`SKILL.md` is L1-owned, so the rows below are for L1 to insert.

## 0. Landed state at draft time (binding caveat)

- `tools/mado-action-plan.py` does **not** exist yet. `tools/` contains only `mado-verify.sh`
  and `swarm-registry.json`.
- `.ufo/waves/round-16/safety-policy.json` does **not** exist yet.
- `.ufo/waves/round-16/safety-cases.json` does **not** exist yet.
- `.ufo/waves/round-16/` is untracked (`git status`: `?? .ufo/waves/round-16/`); HEAD `32c4fda`.
- Therefore every entry below is derived from the **spec**, not from landed code. Items marked
  **[BIND]** must be re-derived from the landed file and committed policy before the row is
  inserted. A row that disagrees with landed source is a conformance defect, not a rounding choice.

## 1. Sources read (exact anchors)

| Source | Anchor | Used for |
|---|---|---|
| `mado-shokunin/.ufo/waves/round-16/w1/spec.json` | item `SafetyGate` prompt (`items[]`, `name=="SafetyGate"`) | the gate's contract: `--plan PATH --policy PATH`, exit 0/1/2, `--selftest`, `--frozen DIR`, denylist, policy keys, "never executes argv" |
| same | item `SafetyCases` prompt | case set the gate must be tested against (libinput sudo pacman, service restart, compositor change, raw input, unknown kind, missing argv, read-source disguised pacman/sudo/shell, allowed read/write) |
| same | `context` (`# Contract`) | no live probes, PAUSED pacman, `-Sp` plan rule, hard-coded fixture is not package validation, source commands are data |
| `shokunin/PROTOCOL.md` | `## Gate standard` (`:375-423`; read 370-430) | verdict vocabulary, self-test clause, two-evidences/frozen clause, registry row fields, "verdict names revision", `snapshot_tampered` = could-not-evaluate |
| `mado-shokunin/SKILL.md` | `## Gate registry` (`:482-513`) | the landed 8-column table shape and the mode-sensitive-exit and frozen-row precedent |
| `mado-shokunin/.ufo/waves/round-13/w1/reports/ReviewRegistry.md` | §3 mode classification; F4 | code 2 is mode-sensitive → separate gate row per mode |
| `mado-shokunin/.ufo/waves/round-13/frozen/verify.py` | module docstring, `FILES`, `expect` map (exit 0 `frozen_match`, 1 `frozen_verdict_mismatch`, 2 `snapshot_tampered`/`frozen_error`) | template for frozen-mode row semantics |
| `mado-shokunin/corpus/lessons/round-15-verifier-spotcheck.md` | §Routed defects: R15-V1 (`:254`), R15-V2 (following block); §Gate and correction evidence | actual host harm; hard-coded predicate controls are not operational validation; the static-guard limits |
| `mado-shokunin/corpus/knowledge/gate-standing-use.md` | `:1`, `:11-12`, `:22-26` | revision-bearing verdict discipline; single-writer rule |

## 2. Primary row — `mado-action-plan` (gate)

Fits the landed 8-column table at `SKILL.md:489`. Mode-sensitive exit codes → the frozen mode
is a **separate** row (§3), matching the `mado-regression` / `mado-frozen-regression` precedent.

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-action-plan | gate | `python3 tools/mado-action-plan.py --plan PATH --policy PATH` (run from lane root; PATH may be lane-relative or absolute; read-only) | 0 clean (`plan_safe`); 1 failed (declared plan refused, one stable reason id per finding — expected set **[BIND]**: `package-install`, `service-mutate`, `compositor-mutate`, `input-capture`, `unknown-kind`, `missing-argv`, `denylisted-executable`); 2 could-not-evaluate (usage, unreadable or malformed plan, malformed policy, policy absent); other exit codes could-not-evaluate | `python3 tools/mado-action-plan.py --selftest`; `--selftest` spelling is the single token (no internal hyphen); 0 clean, 2 failed (assertion failure), other could-not-evaluate; subprocess fixtures assert exit code and stable finding id | `tools/mado-action-plan.py` self-test expectation constants (independent of the classifier code path) **[BIND]**; `.ufo/waves/round-16/safety-policy.json` (persisted policy: `paused=true`, allowed kinds `read-source` and `repo-write` with nonempty argv, denied kinds `package-install`, `service-mutate`, `compositor-mutate`, `input-capture` blocked, denied basenames list) | reads only the caller-named `--plan` and `--policy` files; writes nothing in the repo; `--selftest` uses temporary fixture trees removed after the run; never executes supplied argv; never inspects host state; no network | mado |

Notes that belong with the row (in the text block under the table, not in cells):

- **Denied basenames (spec):** `pacman, yay, paru, systemctl, hyprctl, omarchy, libinput, evtest,
  sudo, sh, bash, env`, refused under `read-source` and `repo-write`. Matching is on basename of
  argv[0]. **[BIND]** whether path-qualified argv[0] (`/usr/bin/pacman`) is basename-normalized.
- **Fail-closed:** unknown kind, malformed plan, missing or empty argv, and any kind not in the
  policy allow/deny sets. **[BIND]** that these map to 1 (plan-level refusal) or 2 (malformed input)
  exactly as the landed code does; the spec does not fix the split.
- **`paused=true`:** the spec says "persist policy paused=true" but does not say what the gate
  does with it. **[BIND]** If the landed gate ignores `paused`, the row must say the pause is
  documentary only. The row must not claim the gate enforces a pause.

## 3. Frozen row — `mado-action-plan-frozen` (gate, mode-sensitive)

Needed because PROTOCOL §Gate standard ("Two evidences") requires a frozen run for a gate whose
verdict depends on a mutable artifact. The plan and policy are mutable inputs, so the frozen
run is required, not optional. The row is a separate row because `1` here means verdict
mismatch, not plan refusal (ReviewRegistry F4 pattern).

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-action-plan-frozen | gate | `python3 tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` | 0 clean (`frozen_match`); 1 failed (`frozen_verdict_mismatch`: the recomputed verdict or code differs from `expected.json`); 2 could-not-evaluate (`snapshot_tampered` when a pinned input is missing, changed or unsafe, checked **before** any verdict comparison; `frozen_error` when `expected.json` is malformed); other exit codes could-not-evaluate | `python3 tools/mado-action-plan.py --selftest` (frozen fixtures included **[BIND]**: confirm the landed self-test covers `--frozen` tamper cases); same token spelling as the plan row | `.ufo/waves/round-16/frozen/expected.json` pins sha256 of `plan.json` and `policy.json` plus expected exit code and finding id **[BIND]**; `plan.json` and `policy.json` sit beside it in the same DIR **[INFERENCE from spec]**; the integrator commits `expected.json` from a reviewed run, the runner never derives it | reads the frozen DIR only; writes nothing; never executes supplied argv | mado |

Frozen-mode rules (for the text block):

- Digests are verified **before** the verdict is recomputed. A tampered input is
  `snapshot_tampered` (could-not-evaluate), never a compared verdict. This is PROTOCOL's rule
  ("an edited snapshot is `snapshot_tampered` (could-not-evaluate), not a compared verdict").
- A frozen `0` proves only that the committed plan and policy bytes still produce the committed
  verdict under the **current** gate code. It does not prove classification completeness, host
  safety, or that the plan was executed.
- The gate script itself is not a pinned input in the spec. See limit L5 below.

## 4. Static-not-enforcement limits (for the row's text block; not exhaustive)

These are the limits a reader must see beside any green result. They are in the row text, not
the verdict cells.

- **L1 — Declared-plan classifier only.** The gate reads a JSON plan of `{kind, argv}` objects.
  It does not parse shell, does not evaluate what a binary does with its arguments, and does not
  model environment, PATH, aliases, or runtime resolution. `python3 -c "..."`, `perl`, `xargs`,
  `timeout`, `nice`, `nohup`, `setsid`, and similar wrappers are outside the denylist unless the
  landed list names them **[BIND]**.
- **L2 — Basename denylist is bypassable by naming, not only by wrapping.** Matching is exact
  basename. `omarchy-*` helper scripts, `libinput-debug-events`-style legacy names, `pacman-key`,
  `pacman-mirrors`, `makepkg`, `pamac`, `pacstrap`, `doas`, `pkexec`, `su`, `busybox`, `systemd-run`,
  `waybar`, `kill`, `reboot`, and `udevadm` are not in the spec list **[BIND]**. Non-pacman
  installers (`uv tool install`, `cargo install`, `npm -g`, `pip install`) are not covered by the
  kinds at all **[BIND]**. These are candidate bypasses for SafetyCases / SafetyControlRed to test.
  They are listed here as limits, not as demonstrated bypasses.
- **L3 — Not enforcement.** A `0` is not permission to run, and nothing in the pipeline is
  wired to call this gate before execution. Wiring the gate in front of any executor is
  operator-owned and absent. A `1` does not stop a human or another tool from running the same
  command.
- **L4 — No host inspection; no real package validation.** The gate does not query pacman, the
  installed-package set, service state, compositor state, or input devices. Install predicate
  controls are hard-coded fixtures. Per the wave contract, a hard-coded fixture is not actual
  package validation. The real operator-authorized step is `pacman -Sp --print-format '%n %v'`
  plus a complete installed-name comparison, and that step is **not run** and **not authorized**
  by this round. pacman transactions are PAUSED host-wide.
- **L5 — Frozen run pins inputs, not the gate code.** `expected.json` pins plan and policy
  digests only. A gate edit that keeps the same verdict on the frozen inputs produces
  `frozen_match`. The verdict therefore does not name the gate revision unless L1 adds the gate
  sha. **Recommendation (L1 decision, not invented here):** record `tools/mado-action-plan.py`
  sha256 as provenance in `expected.json` at minimum, as the `mado-regression` row does. Pinning it
  as an enforced input would make a gate edit `snapshot_tampered`. Either choice must be stated in
  the row.
- **L6 — Policy pause is not proven to be enforced.** See §2 note. Until the landed code is read,
  `paused=true` is a persisted value, not a demonstrated refusal.
- **L7 — Remediation is not done.** R15-V1 (the forbidden partial upgrade: libinput 1.31.3-1 →
  1.32.0-1, plus libinput-tools, python-libevdev, python-pyudev, python-yaml; udev-reload and
  system-update hooks) remains an unresolved operator-owned host harm (`round-15-verifier-spotcheck.md`
  §Routed defects). The gate neither reinstalls, downgrades, restarts, nor repairs anything. A
  green run does not erase the R15 harm; the lesson states "a green unchanged gate is a different
  observable".
- **L8 — Fixtures are not operational guards.** The round-15 lesson declined to credit a
  fixture-only control as an operational guard (QUALITY 20). This row carries the same caveat:
  self-test green is capability evidence (PROTOCOL "Two evidences"), not a measurement and not
  a guard against the actual libinput or pacman transaction.
- **L9 — Scope of the axes.** This row does not credit coverage (C1), freshness, calibration,
  depth or adjacency. It bears only on operability (C2) as a static classifier, and its verdict
  is lane-local evidence (PROTOCOL §Scope; never stands in for the native judge).

## 5. Required binding checks for L1 at integration (not run by this seat)

These are for the single post-integration verification pass. This seat did not run them.

1. Confirm the landed `tools/mado-action-plan.py` exists and read its finding-id set, exit
   mapping, `paused` handling, basename normalization, and the `--frozen` digest order. Replace
   every **[BIND]** above with the landed value or delete the claim.
2. Confirm the self-test expectation constants are committed in the script and are not computed
   by the same code path they assert (PROTOCOL "independent of the recomputation").
3. Confirm the frozen DIR convention and that `expected.json` is committed from a reviewed run,
   not written by the runner.
4. Confirm the gate never calls `subprocess`, `os.exec*`, `os.system`, `eval`, or `shell=True` on
   supplied argv (a static grep of the landed file is sufficient for the row's "never executes
   argv" claim).
5. Confirm the policy file contents match the spec keys exactly. Record the sha256 of
   `safety-policy.json` in the round notes (not in the registry; the registry names the path only).
6. Insert the two rows into `SKILL.md` `## Gate registry` (`:489` table) and the text blocks
   beneath it. Add the matching entries to `SCORECARD.md` only if L1 decides so. Do not edit the
   historical `## Round-N` sections.
7. Note in the round record that the R15-V1 host harm is **unremediated** and that the operator
   pacman pause is still in force.

## 6. Tooling

None installed or updated by this seat. The host has `python3` 3.14.7 (observed with
`python3 --version`); the gate's stdlib-only design needs no additional package. No pacman, sudo,
or package-manager command was run.

## 7. Open items and disagreements

- The §2 denylist and §4 L2 bypass candidates are unverified against landed code and are
  routed to SafetyCases / SafetyControlRed as test targets, not as established bypasses.
- The §3 "frozen DIR contents" and the L5 gate-sha recommendation are judgments for L1. This
  seat did not decide them for the lane.
- No other seat was messaged. No file outside this report was written.
