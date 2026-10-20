# CredentialFence — round 16 w1 sentinel report

Seat: `MadoR16.CredentialFence` (sentinel; leaf, read-only, no remediation scope).
Surface: privacy and probe boundaries for the source-only Waybar U7 work. Credential paths and window titles must never be collected. Date 2026-10-20.

## Axes

- **A1 no collection:** credential paths, secret content, window titles and producer or module text are never collected.
- **A2 no live probe:** no producer, signal, screenshot, compositor or service probe.
- **A3 honest boundary text:** the note, SKILL and gate do not claim more privacy or safety than they show.

## What this seat did (exact)

- Read `corpus/lessons/round-15-verifier-spotcheck.md` (required) and `~/.omp/agent/RULES.md`. Nothing was installed or updated: the contract forbids installs this round and no tool was missing.
- Read the round-16 `spec.json`, the current `.ufo/waves/round-16/waybar-draft.txt`, and the sibling reports `FrontierDraft.md` and `SiblingBoundary.md` (grep only).
- Grepped the corpus and SKILL for title, secret and Waybar anchors. Read `.ufo/evidence/round-12/drift-waybar.txt` through grep.
- Fetched public tagged sources from `raw.githubusercontent.com/Alexays/Waybar/0.15.0/`:

| File | SHA-256 | Bytes |
|---|---|---|
| `man/waybar-custom.5.scd` | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` | 6656 |
| `src/modules/custom.cpp` | `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` | 8746 |
| `include/util/command.hpp` | `7d876c1bc1889bbd55afdc631c910f36749a936df1ea257d30b71597c4201f5d` | 4636 |
| `src/AModule.cpp` | `57d3a1cd5fe03d11bec68f0b7d9e3e5e3fc03fa7f3a492964e4f60b588fe2650` | 9552 |

  - The man and custom.cpp digests match `waybar-draft.txt:1`.
  - Disclosure: my first digest attempt piped through `tee >(wc -c) | sha256sum`. That mixed the `wc` output into the hashed stream, so those hashes were wrong and were thrown away. The values above come from a clean re-download into a `/tmp` file, which was then removed.
- **Not done:**
  - No read of `~/.config/waybar/*`, `~/.config/ai-usage/*`, `~/.cache/ai-usage/*`, any producer script, a journal or log, `/proc`, `hyprctl`, `pgrep`, a screenshot, or any package or service command.
  - No access to `~/.omp/agent/agent.db*`. No omp CLI launched.
  - Host module names cited below come from earlier corpus records ([OBS-record]), not fresh host reads.

## Findings

### F1 — HIGH — standing SKILL route still sends the U7 question to producer execution

**Evidence:**
- `SKILL.md:358` answers "What is the bar showing right now?" with "pure-read producer payloads (`RUN`), e.g. the indicator scripts".
- `SKILL.md:233-236` allows a producer run when its source "proves it pure-read".
- The historical run happened: `corpus/knowledge/waybar-walker-semantics.md:435-436` executed the three indicator scripts, `omarchy-voxtype-status` and `ai-usage waybar`.
- `waybar-walker-semantics.md:149` records the `ai-usage` RUN payload `alt` = `kimi` (a provider/account identity) and "tooltip 9 lines". The same row puts this producer next to a 0600 cache (`~/.cache/ai-usage/status.json`) and the 0600 `~/.config/ai-usage/env` ("shape only, never read"). Its meters come from `omp usage --json` (`ai-usage:406-408`).
- `waybar-walker-semantics.md:377` (§9 item 1) and `:436` record that the voxtype producer killed its caller (exit 143).

**Exploit path:** a round-16 seat or the L1 integrator uses the existing U7 recipe "observe module text" and follows `SKILL.md:358`. "Source proves pure-read" then lets it run `~/.local/bin/ai-usage waybar` or an indicator script.
- That breaks the round contract: no command producer probes, source reading only.
- It collects account or provider identity and usage content.
- It runs code next to a credential file and an `omp` CLI path, which this round forbids launching.

The "pure-read" test checks for side effects, not for privacy. A producer with no side effects still emits personal content: the man page's own cmus example prints `'%a - %t'` "artist - title" (man line 212).

**Impact:**
- Live-probe breach of the same kind as R15-V2 (`hyprctl version`).
- Credential-adjacent collection.
- The U7 claim would pick up host-run evidence that this round does not admit.

**Smallest remediation (L1-owned SKILL text; SkillSafety drafts the pause wording):**
- Add an append-only round-16 supersession: "While the host pause holds and in every source-only round, producer execution is suspended, including 'pure-read' producers. The `SKILL.md:233-236` license and the `:358` RUN route do not apply."
- Extend safety rule 4 (`SKILL.md:240-242`): producer stdout, `text`, `tooltip`, `alt`, `class` and module labels are session material. If ever live they are shape-only (byte length and class token presence). They are never quoted.
- Historical RUN rows stay as history, but are not standing authorization.

### F2 — HIGH — planned action-plan gate cannot fence credential paths or Waybar or desktop probes

**Evidence:**
- The SafetyGate spec (`spec.json`, item SafetyGate) refuses read-source and repo-write only by executable basename. The list is `pacman, yay, paru, systemctl, hyprctl, omarchy, libinput, evtest, sudo, sh, bash, env`, plus blocked kinds.
- The argument vector is never examined.
- `tools/mado-action-plan.py` does not exist yet at this reading, so this is a design review.

**Exploit path:** each of these plans would pass as `plan_safe` (exit 0) under the specified design:

| `read-source` argv | Boundary broken |
|---|---|
| `cat ~/.config/ai-usage/env` | secret content |
| `cat ~/.omp/agent/agent.db` | contract-forbidden file |
| `cat /proc/<pid>/environ` | session material, SKILL rule 4 |
| `~/.local/bin/ai-usage waybar` | producer execution (F1) |
| `waybar` | launches every configured producer |
| `pkill -RTMIN+8 waybar` | live signal. It is the man page's documented refresh (line 244) and its on-click example (line 239) |
| `grim -` | screenshot |
| `wl-paste` | clipboard content |
| `journalctl --user -u waybar` | log content. See F4: tagged `command.hpp:84,147` logs the full command string on fork failure |
| `python3 -c …` | interpreter. Not covered because only `sh`/`bash`/`env` are denied |

**Impact:** if the receipt, SKILL gate-registry row or SCORECARD wording reads `plan_safe` as "safe desktop plan", it makes a false safety claim on exactly this round's privacy and probe surface. C2 would be over-credited.

**Smallest remediation (pick one; L1 decides; no enforcement claim either way):**
- (a) **Wording only, preferred given scope.** The gate registry row, receipt and SCORECARD say: "`plan_safe` = no blocked kind and no listed basename. It does not establish credential, privacy, probe or arbitrary-command safety. Arguments are not inspected." Add one green-with-limit control (`read-source ["cat","~/.config/ai-usage/env"]` → exit 0) to the safety-cases notes as a documented known pass, not a red.
- (b) **Bounded extension.** The persisted policy adds basenames `waybar, pkill, kill, killall, grim, wl-paste, journalctl, python, python3, perl` and a credential-path prefix list checked against every argv element:
  - `~/.ssh`, `~/.gnupg`, `~/.local/share/keyrings`, `~/.omp/agent/agent.db`
  - `~/.config/ai-usage`, `~/.cache/ai-usage`
  - `/proc/*/environ`, `hyprland.log`

  Expand `~` and `$HOME` literally only, with no shell evaluation. The red controls are the matching rows above.

  This is still a finite list, not privacy enforcement. It overlaps PolicyScope/ExecBasename ownership of the name list. The new axis here is argv paths, not basenames.

### F3 — MEDIUM — draft privacy wording: "neither file contains a network call" is code-true but example-false

**Evidence:**
- `waybar-draft.txt:36` is true for `custom.cpp`.
- The man page's examples, however, include:
  - a network or package command: `"exec": "checkupdates | wc -l"` (line 237)
  - a full system upgrade: `"on-click": "termite -e 'sudo pacman -Syu'; pkill -SIGRTMIN+8 waybar"` (line 239). This is the exact transaction class the host pause forbids.
  - process probes in `exec-if: pgrep spotify|mpd|cmus` (lines 186, 199, 213)
  - an artist/title producer (line 212)

**Impact:** a reader could take the man page as a privacy- and network-neutral source, or treat its examples as recipes. The contract says source commands are data, never permission.

**Smallest remediation (WaybarDraft/L1 note text, one bullet under `## Safe observation`):** "custom.cpp contains no network call. The man page's examples (lines 185-244) include network, package-upgrade, process-probe and live-signal commands, and an artist/title producer. They are documentation data: none was run, and none is authorization."

### F4 — MEDIUM — scope the draft's logging claim to custom.cpp; the command helper logs command strings

**Evidence:**
- `waybar-draft.txt:36` says logging "in these files" names the module only. That holds for `custom.cpp:19,90`.
- Tagged `include/util/command.hpp:84` and `:147` log `"Unable to exec cmd {}, error {}"` with the full `exec`/`on-click` string.
- Producers start via `execlp("/bin/sh", "sh", "-c", cmd…)` (`:115`) or `execl(...)` (`:163`). Their only environment change is `setenv("WAYBAR_OUTPUT_NAME", …)` (`:113,161`) [INF from code: the rest of Waybar's environment is inherited unchanged]. `AModule.cpp:96,189,274` run `on-update` and click/scroll commands through `forkExec`.

**Impact:**
- An `exec` string that embeds a token can reach Waybar's log or journal. Log reading is therefore not credential-safe.
- The draft's `[UNK]` at `waybar-draft.txt:44` ("shell or direct-exec semantics, environment") can be settled from source if L1 wants it. It is outside the reserved S054 scope (custom.cpp only).

**Smallest remediation:** keep the scoped words "in these files". Add one limit: "Waybar's command helper (not admitted here) is the logging and exec path. Waybar logs and the journal are not read." Do not generalize to "Waybar does not log commands." Optionally cite `command.hpp` under a separate reserved id. It must not be folded into S054.

### F5 — LOW — window-title fence holds; carry it explicitly into U7

**Evidence (all OBS-record):**
- The standing rule is `SKILL.md:33-34,240-242,354,360`.
- Lane practice follows it: `config-health-report-r3.md:21,607`, `hyprctl-verification-layer.md:19-21`, `remaining-planes-census.md:25-26`, `province-accuracy-selfaudit.md:29,142-145`.
- No title, secret or producer content appears in the round-16 draft, `FrontierDraft.md` or `SiblingBoundary.md`.
- The round-12 Waybar evidence holds module names and digests only (`drift-waybar.txt:30-34`), with no exec strings.

**Gap:** U7 is "module text". Module text can carry titles directly: a producer that prints the active window, the man's artist/title example, or a network tooltip `{essid}` (`waybar-walker-semantics.md:151`).

**Smallest remediation:** the U7 note's `## Safe observation` states that module text, tooltips and the producer stream are session material. The admitted route is the documented parse path only.

### F6 — LOW — host credential-adjacent modules named for the fence (record only)

**Evidence (OBS-record):**
- `custom/ai-usage` (`waybar-walker-plane.md:57`; `waybar-walker-semantics.md:149`). The adjacent `~/.config/ai-usage/{env,providers,providers.bak.alibaba}` files are mode 0600 and were never read (`province-accuracy-selfaudit.md:146-149`; routed to kagi at `:247-248`).
- `custom/gkeep`, the operator's project module (`drift-waybar.txt:34`; `config-drift-r12.md:35`).
- Whether gkeep's producer uses credentials or the network is `[UNK]`. It was not read and should not be read this round.

**Remediation:** none beyond F1 and F2. Listed so that L1 does not cite these modules as U7 examples, and so that any later live round treats them as kagi-adjacent.

## Ownership and limits

- No edits outside this report. No commits. No build, test or gate execution. Nothing installed or updated.
- F1 (SKILL), F2 (gate/policy/registry wording) and F3–F5 (note text) are integration decisions for L1 and the owning seats.
- This seat confirms only static source and corpus facts. It does not establish privacy safety of any host producer, of the planned gate, or of Waybar at large.
- Message sent only to `MadoR16`: the F1/F2 summary.
