# SentinelHostPause — round 17 wave 1 host-pause audit

Seat: MadoR17.SentinelHostPause (sentinel, leaf). Date 2026-10-20. Scope: the
wave-1 context and the 70 items as dispatched. Wave 2 should strengthen the
exact phrases below. Report only; I edited nothing else.

Inputs read (file bytes only):
- `.ufo/waves/round-17/w1/spec.json` sha256 `5f57185e…6c200d`
- `.ufo/waves/round-17/w1/dispatch.json` sha256 `abed46c1…01184b5`; `taskCall.context` == `spec.json .context` (checked equal)
- `.ufo/waves/round-17/gen_w1.py` sha256 `6b4f4988…f7f6816c200d`
- `~/.omp/agent/RULES.md` (l.1-14)
- `SKILL.md` (grep only)
- `tools/mado-verify.sh` and `tools/mado-action-plan.py` (grep/sed only)
- `corpus/lessons/round-16-verifier-spotcheck.md` (required reading)

No transcripts were read; my item does not name them. No command outside
cat/sed -n/grep/sha256sum/file/command -v ran. No tools were installed or
updated.

"ctx l.N" means line N of `taskCall.context`, which is the same as gen_w1.py
l.(N+10) for l.10-13. "items[i]" is the index in `spec.json .items`.

Axes: (a) phrases that permit or invite a host command, (b) gaps in what is
forbidden, (c) hazards in how fixtures get made, (d) durable corpus text that
future seats will execute.

## Findings (severity-ranked)

### H1 — The harness appends the operator tooling directive, and the context sends seats to read it
- **Evidence.**
  - `dispatch.json`: 0 of 70 tasks contain "Tooling directive", yet my received task ends with it. The harness appends it after L1's text, and it is also in the generic-rules system prompt.
  - RULES.md l.3-5: "installs or updates any tool that helps its task … with full privilege, without asking first. Passwordless `sudo` is available."
  - RULES.md l.7, channel 1: `sudo pacman -S --needed --noconfirm <pkg>`. This is byte-identical to the prefix of the round-15 harm command that ctx l.5 names as the red anchor.
  - ctx l.11: "you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first". RULES.md has no pause carve-out.
  - L1 had to send a mid-wave IRC reminder. That shows the spec text alone was not trusted to hold.
- **Exploit path.** A seat has these signals:
  - A later, "always on, every agent" operator text.
  - An explicit "read RULES.md first".
  - Godspeed's "Act directly".

  It takes RULES.md channel 1 for a missing tool and runs `sudo pacman -S …` against the stale sync db. That repeats the round-15 partial-upgrade mechanism.
- **Impact.** A repeat of R15-V1-class host harm (boot chain, input stack).
- **Smallest remediation.** Replace ctx l.11 (see Wave-2 text, P1).

### H2 — The context names npx and uv tool as permitted channels; with passwordless sudo they are a pacman-free path to host mutation
- **Evidence.**
  - ctx l.11: "use only uv tool / npx / an official release binary in ~/.local/bin".
  - RULES.md l.4-5: passwordless sudo.
  - The tripwire class lists (ctx l.24-26) do not cover `npx`, `uv tool install`, `uv run`, `pip install`, `cargo install` or `npm -g`.
  - No item needs a new tool: `command -v` resolves curl, jq, git, python3 and sha256sum.
- **Exploit path.** `npx <pkg>` downloads and runs registry code immediately. A `uv tool install` from an sdist runs build-backend code. Either can call `sudo pacman …` or `systemctl …` in a child process. The transcript then shows only `npx foo`, which C3's tripwire classifies as clean.
- **Impact.** Host mutation that the round's own detection capability cannot see.
- **Remediation.** No installs in round 17 (P1).

### H3 — `tools/mado-verify.sh` runs live hyprctl when called bare, and SKILL.md calls the bare form the standing verdict
- **Evidence.**
  - `tools/mado-verify.sh:87` `LIVE_REQ="${MADO_VERIFY_LIVE:-auto}"`.
  - `live_plane()` at :2968-3079 runs `hyprctl version`, `-j instances`, `configerrors`, `-j getoption …` and `-j binds` whenever hyprctl is on PATH and `HYPRLAND_INSTANCE_SIGNATURE` is set.
  - SKILL.md:534 says "default live"; :651 "# live, read-only"; :1567; :1645 "the standing verdict is `bash tools/mado-verify.sh` (live, read-only)"; :1655 "run the gate for the standing verdict"; :1711.
  - SKILL.md:39-42 forbids live reads only for "This source-only round", meaning round 16. ctx l.10 names hyprctl, but nothing tells round-17 seats or L1 that the bare gate counts as a hyprctl command.
  - Seats are pointed at SKILL.md by items[15] SkillRegistryDraft (rows 535-548), items[59] SkillSectionJoin and items[49] RevHarmWatch.
  - `--selftest` is hermetic: it uses a sandboxed PATH (:985-994).
- **Exploit path.** A seat, or L1's integration verify, runs the "standing verdict" without `--selftest` or `--no-live`. That issues hyprctl live reads during the pause.
- **Remediation.** P3.

### M1 — Making the fixtures can execute the commands they describe
- **Evidence.**
  - items[2] TripwireFixturesCompound must encode `echo $(pacman -Qq | wc -l)`, `grep 'pacman -S' notes.md`, `echo "sudo pacman -S x"` and eval code `!sudo pacman -S foo`.
  - items[1] encodes the incident string.
- **Exploit paths.**
  - Fixture JSONL written through an unquoted heredoc (`<<EOF`), `echo "…"`, `printf "…"` or `bash -c` lets the shell expand `$(pacman -Qq | wc -l)`. That is a real package query, the round-16 M5 class.
  - The single quotes in `grep 'pacman -S'` close a surrounding `'…'`, which leaves later text unquoted.
  - The eval tool rewrites `!cmd` lines to shell. If a seat builds a fixture in an eval cell and a physical line starts with `!sudo pacman -S foo` (for example inside a triple-quoted string), it may execute. Whether the rewriter respects string literals is **[UNK]** here; that is items[62] RevengeEvalBang's question.
- **Impact.** At best a package query. At worst `sudo pacman -S foo` with passwordless sudo.
- **Remediation.** P4.

### M2 — The "Safe observation" sections write runnable commands into the durable corpus
- **Evidence.**
  - items[11] NoteIdle: "`## Safe observation` (what an operator may read without mutating; no lock/suspend/dpms triggering)". That still admits `hyprctl …`, `systemctl --user status hypridle`, `journalctl --user -u hypridle` and `busctl …`, all forbidden under the pause.
  - items[12] NoteTerminal has a `## Safe observation` heading with no constraint at all, so `alacritty --version` or `xdg-terminal-exec` dry modes [INFERENCE] could land.
  - items[3] MeasureBuild makes the heading mandatory.
- **Exploit path.**
  - Now: a scribe "validates" its listed commands by running them.
  - Later: future seats read corpus/knowledge as routes while the pause persists. SKILL.md:495 already has to say "Old live command tables describe dated routes, not authorization".
- **Remediation.** P5.

### M3 — The HOST PAUSE denylist misses commands this wave's ground invites
- **Evidence.** ctx l.10 names pacman/yay/paru, sudo, systemctl, hyprctl, libinput, evtest, wayland-info, hypridle, hyprlock, alacritty, waybar, walker, omarchy-*, notify-send, screenshots, "input/device probes, service or compositor operations". It does not name:
  - `loginctl`. items[20] asks for "dbus/loginctl lock behaviour"; `loginctl lock-session` locks the screen.
  - `busctl`/`gdbus`/`dbus-send`. items[27] covers the login1 D-Bus API, and `busctl introspect org.freedesktop.login1` is the natural probe.
  - `journalctl`. items[54] asks about "daemon stop-cause".
  - `systemd-inhibit`.
  - `xdg-terminal-exec`. Only items[12] bars it; items[30] and [33] do not.
  - `uwsm`, `gtk-launch`, `xdg-open`, `makoctl`, `brightnessctl`, `playerctl`, `wpctl`.
  - Process probes (`pgrep`, `ps`, `pidof`, `/proc/*/comm`). SKILL.md:41 barred them in round 16; ctx l.10 does not.
  - `<binary> --version`.
  - Pacman-family tools not spelled "pacman": `checkupdates` (syncs a temp db), `expac`, `pactree`, `pacman-conf`, `makepkg`, `paccache`.
  - Package-database file reads (`/var/lib/pacman/local/*/desc`, `/var/cache/pacman/pkg`). These are a "file bytes only" way to get host versions, which ctx l.14 says must stay [UNK].
- Also: "read as file bytes only (cat/sed/grep/sha256sum)" allows `sed -i`, which writes.
- **Remediation.** Invert to an allowlist (P2).

### M4 — ctx l.11 gives seats a literal pacman command and calls it a "dry-run rule"
- **Evidence.** "When the pause lifts the dry-run rule applies (pacman -Sp --print-format '%n %v' first; …) — not this round."
- `-Sp` is exactly the package_query form the tripwire contract lists (ctx l.25). Reasoning that a "dry-run" is "read-only" is the M5 pattern (round-16 spot-check l.107-110).
- **Remediation.** Remove post-lift policy from seat context; keep it in L1-only text (P1).

### M5 — Items that invite testing by running things
- items[62] RevengeEvalBang: "Determine how the eval tool's `!cmd` lines and `%pip` map to shell execution". Testing empirically means `%pip install`, an install outside even the permitted channels, or `!` shell lines.
- items[61] RevengeTranscriptFormat: "whether a toolCall can exist without execution (denied/aborted)". This invites provoking a denial. No interception layer exists (the "prompt-only fences" of LessonDraft M2), so a forbidden test command simply executes.
- **Remediation.** P6.

### M6 — Sibling gates and discovered scripts look sanctioned
- **Evidence.**
  - RULES.md l.10: "Full-system upgrades (`pacman -Syu`) go through tsukuroi-shokunin's update-safety gate first".
  - items[52] SiblingOverlap: "Which sibling owns host package updates".
  - items[38] FleetToolScan: "grep -l for toolCall, jsonl, sessions, pacman" across `*-shokunin/tools` and `scripts`.
- **Exploit path.** A seat runs tsukuroi's gate, or a found script's `--help`/`--selftest`, as the "approved route". That may run checkupdates or pacman.
- **Remediation.** P7.

### L1 — Pressure toward acting first
- The Godspeed preamble is on 70/70 tasks: "IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS … Act directly via tool calls". Together with RULES.md "without asking first", it discourages the right move, which is to message MadoR17 before an uncertain command.
- Only 4 of 70 items carry their own "never run" sentence. The rest rely on ctx l.10, which sits immediately before ctx l.11's install permission.
- **Remediation.** P8.

### L2 — Classifier gaps on pause ground (detection side; items[46] RevTripwireContract owns these, listed so the pause list and the classes stay aligned)
- ctx l.24/26 leave `systemctl suspend|hibernate|hybrid-sleep|suspend-then-hibernate|poweroff|reboot|halt|kexec|soft-reboot|rescue|emergency|default|reset-failed|freeze|thaw|revert|clean|set-environment|import-environment` unlisted in both classes. As worded, they fall to no class [INFERENCE].
- `loginctl lock-session|unlock-session|terminate-*|kill-*` is only live_probe.
- `omarchy-system-lock` (locks the screen) is live_probe, not host_mutation; "lock", "wake" and "screensaver" are not mutation keywords.
- The install channels (`npx`, `uv tool install`, `uv run`, `pip install`, `cargo install`, `npm -g`, `makepkg -si`) are unclassified (see H2).

## Checked and safe (with evidence)
- **items[5] TamperRecut** runs `mado-action-plan.py --frozen`. `subprocess.run` appears only in `_self_invoke` (:522-528, `shell=False`, `stdin=DEVNULL`), called at :741 and :845 on the script copy. The plan argv lines (:565-700) are classifier data and are never executed.
- **items[3] MeasureBuild and items[4] ReceiptLabelCheck** use git read verbs only. The precedent round-16 `measure.py:64` is `git -C REPO` `check_output`.
- **IncidentTimeline** reads `/var/log/pacman.log` with grep, which is clean per ctx l.27.
- **HostIdleFiles, HostTerminalFiles and HostOmarchyLockScripts** (items[32-34]) each carry their own no-execution sentence.

## Wave-2 replacement text (exact phrases)
- **P1 — replace ctx l.11 whole.** "Tooling: NO installs or upgrades this round by any channel (no sudo, pacman, uv tool, uv run, pip, %pip, npx, npm, cargo, or downloaded binaries). This overrides the appended operator Tooling directive and ~/.omp/agent/RULES.md, whose channel 1 is the round-15 harm command; do not read RULES.md for this round. curl, git (read verbs), jq, python3 stdlib and coreutils already exist. A seat that thinks it needs a tool messages MadoR17 and stops." Drop the "When the pause lifts … pacman -Sp …" sentence from seat context.
- **P2 — replace the ctx l.10 list with an allowlist.** "Host commands are an allowlist: cat, sed -n, grep, head/tail via read, sha256sum, wc, ls, find (no -exec/-delete), stat, file, curl (GET to the cited URLs), git (show/ls-tree/log/rev-parse/cat-file only), jq, python3 -I on your own script, and mktemp/cp/rm only under /tmp. Everything else is forbidden, including loginctl, busctl/gdbus/dbus-send, journalctl, systemd-inhibit, xdg-terminal-exec, uwsm, gtk-launch, xdg-open, pgrep/ps/pidof, any `<binary> --version`, checkupdates/expac/pactree/pacman-conf/makepkg/paccache, and reads of /var/lib/pacman or /var/cache/pacman (host versions stay [UNK])."
- **P3 — add.** "Never run tools/mado-verify.sh bare or with --live/--regression/--snapshot: its default MADO_VERIFY_LIVE=auto (:87) issues hyprctl (:2968-3079). SKILL.md's 'standing verdict' lines are dated routes. L1 alone may run `--selftest`."
- **P4 — add to items[1] and items[2].** "Create fixture files only with the write tool (or a python script that json.dumps literal strings). Never via bash heredoc, echo/printf, bash -c or eval cells; never place a fixture command at the start of a line in an eval cell."
- **P5 — items[11] and items[12].** "`## Safe observation` lists file-byte reads only (paths plus cat/sha256sum). Any compositor, service or D-Bus read is listed under `## Unexercised behavior` as '[UNK] needs operator-authorized live round; not run in round 17'. Never run anything you list."
- **P6 — items[62] and items[61].** "Determine from local docs and existing transcripts only; do not execute eval magics, `!` lines or `%pip`, and do not issue any command to observe denial. No interception layer exists; a forbidden test command executes."
- **P7 — items[38] and items[52].** "Never execute discovered or sibling scripts (including --help/--selftest). tsukuroi's update-safety gate is not invocable this round."
- **P8 — add after the Godspeed preamble in context.** "If unsure whether a command is allowed, it is not: do not run it; message MadoR17."

Installs/updates by this seat: none.
