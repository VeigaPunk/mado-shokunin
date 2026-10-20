# MadoR16.NoLiveBreach — critic: fresh live commands in a source-only round

Seat: `MadoR16.NoLiveBreach` (critic, leaf; no dispatch). Date 2026-10-20.
Read first: `corpus/lessons/round-15-verifier-spotcheck.md` (R15-V1/V2), `~/.omp/agent/RULES.md`.
Read-only review; this seat edits no lane file except this report.

Axes: (A) no fresh live probe by L1 verification; (B) the C2 gate is not over-credited as a
no-live guard; (C) the round-15 breach is fully recorded; (D) standing SKILL text does not
re-authorize old live routes.

## Counterexamples (strongest first)

### CE1 — L1's "verify once" can fire every forbidden probe class through the lane's own gate (axis A, D)

- `tools/mado-verify.sh` **defaults to live**: usage `:16`, `:97` ("(default) live read-only run against
  $HOME"); `LIVE_REQ=auto` `:87`; `auto` → `LIVE=1` when `ROOT == $HOME` `:3661`.
- A bare run executes: `hyprctl version`, `-j instances`, `configerrors`, 7× `-j getoption`, `-j binds`,
  `-j monitors`, `-j layers` (`:2976-3169`); `waybar --version` `:3150`; `pgrep -x waybar` `:3161`;
  `busctl --user get-property fr.arouillard.waybar …` `:3198`; `walker --version` `:3211`;
  `systemctl --user is-active` ×2 `:3222-3223`; `omarchy theme current` `:3236`, `:3462`;
  `omarchy version` `:3361`; `git -C <omarchy checkout>` `:3382-3406`; `omarchy commands --json --all` `:3422`.
  These are compositor, service and command-producer probes, which the contract forbids.
- `--no-live` does not run those commands. It still reads host config planes under `$HOME`. The round-15 receipt
  `.ufo/waves/round-15/evidence/gate-file-plane.txt:1,7` shows `command: bash tools/mado-verify.sh --no-live` and
  `root: /home/vgpnk`. That reads host config, not sources, and neither C1, C2 nor C3 needs it.
- Fresh round-16 recommendations that lead there:
  - `w1/reports/PlanningWalk.md:95` says "`bash tools/mado-verify.sh --no-live` and `--selftest` (harm watch only)".
  - `w1/reports/SkillSafety.md:70` says "run the lane's own gate once". That phrase is ambiguous, and the bare form is live.
  - Standing text points the same way. `SKILL.md:507` (registry: "default live"), `:1597` ("standing verdict is
    `bash tools/mado-verify.sh` (live, read-only)") and `SCORECARD.md:533,653` (earlier rounds' `--no-live` recipe) are
    old recommendations, not authorization.
- **Smallest safe correction:** the only old-gate check this round is
  `bash tools/mado-verify.sh --selftest` plus digest equality. The digest is `fba82a66…`, already recorded by
  `SafetyReceipt.md:39`. Do not do a bare run or a `--no-live` run against `$HOME`.
  - `[INFERENCE]` from grep of every `"$0"` re-invocation: `--selftest` child runs all pass `--root <tmp>`, so
    `auto` resolves to non-live. Live children run only under stub or sandbox `PATH` (`:685-794` OMB stubs;
    `:994`, `:1433` SANDBOX, which contains no `hyprctl`).
  - Name this in the round-16 SKILL instruction, e.g. "source-only rounds run the mado-verify gate in `--selftest`
    mode only; its default mode is live."

### CE2 — the new C2 gate returns `plan_safe` for live probes (axis B)

I derived these statically from `tools/mado-action-plan.py` `_classify` `:219-250`. It checks only the `kind`,
non-empty argv and the `argv[0]` basename against `safety-policy.json` `deny_executables`. I did not execute it.
Each of these single `read-source` actions should reach `plan_safe`, exit 0 `[INFERENCE until L1 runs it]`:

| argv | Live effect if executed | Anchor |
|---|---|---|
| `["tools/mado-verify.sh"]` | the full live layer in CE1 (basename `mado-verify.sh` is not denied) | gate `:3661` |
| `["cat","/proc/1706/maps"]` | process probe; this exact read was the unflagged round-15 breach (CE3) | r15 `ReviewDocsEra.md:20` |
| `["pgrep","-x","Hyprland"]` | process probe (round 15) | r15 `ReviewDocsEra.md:76` |
| `["pkill","-RTMIN+8","waybar"]` | signals the bar; `refresh` wakes the worker (S054 `custom.cpp:138-140`), which re-runs `exec` through `/bin/sh -c` (tagged `include/util/command.hpp:115,163`). The tagged man page recommends it (S053 `:244`). | S053/S054 |
| `["grim","-"]` | screenshot. Old `SKILL.md:212` lists it as a "read-only probe". | SKILL |
| `["waybar","--version"]`, `["makoctl","mode"]` | runs a package binary or queries a service | gate `:3150`; SKILL `:209` |

- The `pkill`, `grim` and `waybar` basenames are already proposed in `CredentialFence.md:87`. Wrappers and
  interpreters are already covered by `ExecBasename.md` and `UnknownActions.md`. I do not repeat those findings here.
- What is new: liveness is in the **operand** (`/proc`, `/sys`, `/dev`, `/run`, `$XDG_RUNTIME_DIR`, `$HOME`
  config), or in an executable's **default mode** (the lane's own gate). That means even the argv0 allowlist in
  `SafetySimplify.md:41-44` (`cat`, `stat`, `ls`, `readlink`) would pass row 2.
- **Smallest safe correction:** wording, not code. Put this sentence in the SCORECARD C2 text, the lesson Boundaries
  section (`round-16.md:66-69`) and the future `mado-action-plan` registry row:
  "`plan_safe` is not a no-live-probe verdict. Operands are not analysed (`cat /proc/<pid>/maps` passes), and
  unlisted executables pass, including `tools/mado-verify.sh`, whose default mode is live."
- Optional code change, L1's decision: refuse `read-source` operands with prefixes `/proc/`, `/sys/`, `/dev/` or
  `/run/`, with a matching red case. A known false negative must never be added as a green (exit 0) fixture.

### CE3 — the round-15 no-live breach is under-counted (axis C)

- The round-16 lesson M2 (`corpus/lessons/round-16.md:15`) cites only ReviewLibinput's `hyprctl version`. This
  repeats the closure's carry-forward (`round-15-verifier-spotcheck.md:274-277`).
- The same round also performed live process reads that were not self-flagged:
  - `.ufo/waves/round-15/w1/reports/ReviewDocsEra.md:20`: `/proc/1706/maps` read.
  - `.ufo/waves/round-15/w1/reports/ReviewDocsEra.md:76`: `/proc/1706/maps` and `pgrep -x Hyprland → 1706 …`.
  - `LibinputList.md:122` reuses the `/proc/1706/exe` mapping.
  - `MistakeDraft.md:23` (R15-b) surfaced this, and `ClosureDebt.md:185-187` repeated it. The integrated M2 dropped it.
- Round-16 drafts still re-use that result as fresh `[OBS]`: `SafetyLearning.md:18,46` ("Hyprland PID 1706 mapped …
  (deleted)"). I grepped the canonical lesson, QUALITY, U7 note and SOURCES for `/proc|(deleted)|1706|pgrep` and found
  0 hits, so it has not been imported yet.
- **Smallest safe correction:** append to the M2 Evidence cell: "plus ReviewDocsEra `/proc/1706/maps` read and
  `pgrep -x Hyprland` (`ReviewDocsEra.md:20,76`), not self-flagged. These are process debt, not admissible fresh
  evidence." This is append-only in the new round-16 lesson. The closure file stays untouched. Do not import the
  deleted-library observation as `[OBS]`.

### CE4 — the integrated bans read as mutation-only, while R15-V2 was a read-only probe (axis D)

- The ban text in four places frames the prohibition around mutation:
  - SKILL bullet header `SKILL.md:39-40`: "no package transactions or service/compositor mutations".
  - `SCORECARD.md` (round-16 text): "no package query/transaction, service operation, live compositor or input probe".
    This omits **screenshot** and **command-producer/signal** probes.
  - Lesson `round-16.md:66-67`: "service/compositor mutation, input capture, producer execution or screenshot". This
    omits read-only compositor/process probes.
  - Old SKILL calls `hyprctl`/`pgrep`/`busctl`/`makoctl`/`grim` "Read-only probes" (`SKILL.md:193-212`) inside a
    "mutation-free fence".
- A reader can therefore satisfy "no mutation" and still repeat `hyprctl version`, which is exactly R15-V2.
- `SKILL.md:43` ("No live probe is authorized by an old command example") and `:489` ("Old live command tables
  describe dated routes") help. They do not name the tables.
- **Smallest safe correction:** align all three enumerations to the contract: "no live compositor, process, service,
  input-device, screenshot, signal or command-producer probe, read-only included". In SKILL `:489`, name the
  suspended routes: §Read-only probes `:193-212`, claim-first live rows `:138-147`, `:358`, the RUN licence
  `:131`, `:233-235`, and the `mado-verify` registry default mode `:507`.

### CE5 — the U7 note does not name interaction as a producer trigger (axis D; optional, harms nothing)

- `corpus/knowledge/waybar-observation-boundaries-r16.md:52-57` forbids executing `exec`, `exec-if` and event
  commands, and treats the man example (`sudo pacman -Syu`; `pkill`) as data. Good.
- It does not state that **clicking or scrolling** a module runs `on-click` (S053 `:87-89`). With the default
  `exec-on-event: true` (S053 `:28-31`, default at `:30`), that interaction also re-runs `exec` (S054 `handleEvent`
  `:144-146`).
- Suggested clause: "Interacting with a module (click or scroll) executes its event command and, by default, its
  producer." The measured headings and `covers:` line are unchanged.
- Shell semantics stay `[UNK]` in the note. Tagged `include/util/command.hpp:115,163` uses
  `execlp/execl("/bin/sh","sh","-c",cmd)` (raw sha256 `7d876c1b…`, 4636 B). Citing it would need a new source id,
  which is not reserved this round, so this is left to L1.

## Not a breach (checked)

- **The new gate is live-clean.** Its only `subprocess.run` calls are
  `[sys.executable, script, --plan/--policy | --frozen]` (`mado-action-plan.py:430-433`, `:492-494`). Supplied argv
  is never executed. There are no `/proc`, `/dev` or environment reads.
- **measure.py** hashes `tools/mado-verify.sh` with `gate_executed: False` (`measure.py:316-318`, `:342-344`).
- **waybar-draft and WaybarDraft** fetched the tagged raw source with curl only.
- **Other seats' fresh actions:** no seat disclosed a live compositor, service, input, screenshot or producer
  command. The following are host or doc file reads, not probes:
  - `MistakeDraft` and `NoInstalls` read `/var/log/pacman.log` as text. ClosureDebt correctly labels this a read.
  - `SafetyService` read static files under `~/.local/share/omarchy/bin` and installed man sources.
  - `SafetyReceipt` ran `python3 --version`.
- **Incidental, not this axis:** `safety-cases.json` expected findings do not match what the gate emits. For example,
  the cases expect `blocked_action_kind:package-install`, `unknown_action_kind`, `empty_argv` and
  `denied_executable:pacman`. The gate emits the bare constants `denied_kind`, `denied_unknown_kind`,
  `denied_empty_argv` and `denied_executable` (`:75-85`, `_emit :110-120`). L1 needs to reconcile these before any
  case run.

## Impacted axes and judgement

- **Operability:** a fixable defect if L1 verifies with a bare or `--no-live` gate run. It turns into a contract
  breach the canonical judge must reject if such a run actually happens.
- **Calibration and quality:** CE2 and CE4 are fixable wording defects that over-credit C2 as a no-live guard.
- **Discernment:** CE3 is a fixable provenance under-count.
- **Coverage (C1):** unaffected. CE5 is optional hardening only.

## Own actions and tooling

- Ran read-only `git status/diff/rev-parse` in the lane, plus `ls`, `grep`, `sed -n` and `wc` on lane and round-15 files.
- Parsed the wave JSON in Python.
- Ran `curl` GETs of three tagged Waybar 0.15.0 raw files:
  - `waybar-custom.5.scd`: `efb6a63a…`, 6656 B
  - `custom.cpp`: `2232f7f7…`, 8746 B
  - `command.hpp`: `7d876c1b…`, 4636 B
  The first two digests match the WaybarDraft values. The scratch copies in `/tmp/nolivebreach-r16` were removed.
- Did not execute any gate, selftest, measure, producer, `hyprctl`, `pgrep`, `/proc` read, signal, screenshot,
  package or service command.
- Did not open `agent.db*` or credentials.
- Sent one coordination message to `MadoR16`.
- Installs and updates: none. RULES.md was read, and this round's contract forbids installs, which takes precedence.
  No prerequisite was missing.
