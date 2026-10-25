# ConnFrontier — connector, mado round 37 wave 1

Seat: `L1Mado37-2.ConnFrontier`. Lane HEAD read: `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`. Date 2026-10-25.
Read-only everywhere. The only writes are this report and scratch under
`.ufo/waves/round-37/w1/scratch/ConnFrontier/` (the rendered wiki texts, `h2t.py`, `fetch-digests.txt`,
`desc-vs-getoption.py` and its receipt `desc-vs-getoption.txt`) and `/dev/shm/mado37-ConnFrontier/` (raw fetches).
Tools installed: none. Sockets: none connected. The only host verbs were `hyprctl` read verbs on the request
socket (`version`, `getoption`, `descriptions`, `monitors`), `pgrep`, and file reads under `~/.config/hypr` and
`~/.local/share/omarchy`.

Axes named: **coverage** (the C1 corpus ground and how it maps onto the lane's maps) and **operability**
(the C2 census `tools/mado-eventq.py` and its live receipt).

## Bottom line

1. **Frontier: the bullet the registration names is the wrong anchor for half its words.** The quoted bullet
   (`corpus/README.md:98-100`) names *Walker's* socket protocol, which is a different socket from Hyprland's
   socket2. The actual semantic hit is the round-16 bullet's "freshness" clause (`:136`). No gate checks the
   Frontier text: the C1 counter reads only `## Coverage map`.
2. **Arc §6 / U1: not U1 as registered, but U1's parent row.** U1 was cut as "per-window rule effects"
   (`SCORECARD.md:251`). The §6 row it came from is "window-rule effects / exec-once results"
   (`arc-synthesis.md:300`), and no U-id ever took the exec-once half. On this host one socket2 subscriber is
   an exec-once job: `socat` pid 2293, started by `omarchy-hyprland-monitor-watch`.
3. **PROVINCE and SKILL are already stale for round 27, and C2 widens the read surface again.**
   `tools/mado-wsrules.py` is tracked but has no PROVINCE tool-table row. Neither binds, anims nor wsrules has
   a SKILL probe-table row. The new tool reads three things no PROVINCE line names: the kernel unix-socket
   table, the compositor session log (recorded as "not read" in `hyprctl-verification-layer.md:30`), and the
   compositor's user-unit journal.
4. **New finding (needs attention): `hyprctl descriptions` contradicts `getoption` for `debug:disable_logs`.**
   `descriptions` reports `"current": false`, while `getoption` reports `int 1`. Across the 71 options this
   host's config sets, `descriptions` reports the compiled default for 63. Any instrument reading
   `descriptions` would invert C2's `markers_observable`.
5. **Proposed move (one, bounded; details in the section below):** run the C2 live receipt with
   `--expect-client waybar --expect-client socat`, and name both subscribers' consequences in the round's
   frontier text. The frozen v2 counter is indifferent to the extra flag. Operability gains a guard on the
   second known subscriber, and coverage gets the correct frontier anchors. Neither axis is harmed.
6. **Next desktop surface, ranked:** (1) the config-option table, predicted per key and checked against
   `getoption`; (2) monitor rules against `hyprctl monitors`; (3) window and layer rules, which have the most
   host bytes but no list verb in v0.56.2.

## Item 1 — `corpus/README.md` `## Frontier`: which bullet moves — FINDING

Command: `awk 'NR>=94 && NR<=180' corpus/README.md` and
`grep -n -E 'Rendered UI, Waybar module text|…' corpus/README.md`.

The bullet the registration names (`registration.md` "Frontier row moved"), at `corpus/README.md:98-100`:

> - Rendered UI, Waybar module text, Walker socket protocol, dispatcher
>   behavior and per-window rule effects: [arc gap ledger](knowledge/arc-synthesis.md)
>   §6. No screenshot, input injection or socket connection is added here.

- "Walker socket protocol" is Walker's own socket. Arc §6 at `arc-synthesis.md:297` says:
  "| walker socket protocol | never connected (constraint); the r9 note measured shape only — protocol
  semantics UNKNOWN |". This round's subject is Hyprland's `.socket2.sock`, so it does not move that item.
  The ScribeReadme draft (`w1/scratch/ScribeReadme/readme.md`, "(b) Frontier subsection") says "The event-socket
  client half of the first Frontier bullet now has sourced ground". That is right only for "Waybar module text".
- The closer hit is the round-16 bullet at `:133-137`:
  > Actual module text, GTK/widget state, pixels, CSS effects, **freshness** and hardware values stay
  > unmeasured; no capability to read the live bar is claimed.

  A Waybar client that the compositor removes at the 64-event cap stops receiving events. Its module text
  then goes stale, which is the "freshness" item. That is the frontier item this theme actually bears on.
  It remains unmeasured, because no removal was observed.
- No round-32 or round-34 Frontier subsection exists. The socket2 path and framing (`ipc-contract-r25.md` §2)
  and the Waybar client route (`waybar-module-text-route-r25.md`) have coverage-map rows (`README.md:55`, `:58`)
  but no frontier text. A round-37 subsection would be the first frontier text for the event socket.
- Gate gap: `quality/counters/c1-r37-event-ground.py` reads only the `## Coverage map` section
  (`grep -n 'README' …` gives `:119-120`, `section(readme, "## Coverage map")`). Whatever the Frontier
  subsection claims, no counter catches a wrong anchor.

## Item 2 — arc gap ledger §6: U1? — FINDING (no as registered; yes for the parent row's other half)

Commands: `awk` over `arc-synthesis.md:286-403`; `rg -n '^covers:' corpus/knowledge/`; `awk 'NR>=244 && NR<=262' SCORECARD.md`.

- The U-ids were fixed in round 12 (`SCORECARD.md:250-256`): "U1 per-window rule effects (`arc-synthesis.md`
  §6 "no rule-read verb"); … U7 Waybar module text". All seven are covered (`covers: U1` through `U7`;
  U1 is `window-rule-effects-getprop.md:6`, U7 is `waybar-observation-boundaries-r16.md:4`).
- The theme does not map onto U1 as registered. Its nearest U-id is U7: the Waybar client half, via the
  freshness clause above. The two new entries should carry **no** `covers:` line. U7 is already covered, so
  `covers: U7` would double-count without moving the 7/7 set.
- The non-obvious hit is that §6's row at `arc-synthesis.md:300` reads
  "| window-rule effects / exec-once results | no rule-read verb in Hyprland 0.56 (r2/R3-2) |". U1 took only
  the window-rule half; **"exec-once results" has never had a U-id**. Host bytes show that one socket2
  subscriber is an exec-once result:
  - `grep -rn 'monitor-watch' ~/.local/share/omarchy/default/hypr/ ~/.config/hypr/` gives
    `autostart.conf:9:exec-once = uwsm-app -- omarchy-hyprland-monitor-watch`.
  - `~/.local/share/omarchy/bin/omarchy-hyprland-monitor-watch` (14 lines, sha256 `256f333c845d8756…`),
    line 7: `socat -U - "UNIX-CONNECT:$SOCKET" | while read -r event; do`. Lines 9-11 run
    `omarchy-hyprland-monitor-internal recover` and `…-mirror recover` on `monitorremoved>>`/`monitorremovedv2>>`.
  - `pgrep -a socat | awk '{print $1,$2}'` gives `2293 socat`; `pgrep -x -c socat` gives `1`. This matches
    peer seats: ExecEventqA prints `MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 …`, and ExecProcCrosscheck
    found "socat 2293's parent is pid 1689 (`omarchy-hyprlan…`, child of Hyprland)".
  - **[INFERENCE]** If Hyprland removes this client at the cap, socat reads EOF and exits, the `while` loop
    ends, and the script exits. `exec-once` does not respawn it. Monitor-toggle recovery would then stop
    silently until the next login. None of this was exercised.

## Item 3 — PROVINCE.md surfaces — FINDING

Commands: read `PROVINCE.md` (81 lines); `ls tools`; `rg -n 'mado-binds|mado-anims|mado-wsrules|ss -x' SKILL.md PROVINCE.md corpus/README.md`.

- Owned surfaces (`PROVINCE.md:6-9`): `~/.config/hypr/`, `~/.config/waybar/`, `~/.config/walker/`, the terminal
  trees, themes and wallpapers, screen and idle. The runtime directory `$XDG_RUNTIME_DIR/hypr/<HIS>/` is not
  named, and neither is the user journal.
- C2's live defaults (`registration.md` C2 "Deliverable") read:
  - `ss -xpa`, the kernel unix-socket table for **every** process of the user. The tool filters to socket2,
    but the read is host-wide.
  - `$XDG_RUNTIME_DIR/hypr/<instance>/hyprland.log`. The lane previously recorded it as
    "`hyprland.log` (967,994 B, not read)" (`hyprctl-verification-layer.md:30`).
  - `journalctl --user -u wayland-wm@hyprland.desktop.service`. Unit-health ground is tsukuroi's
    (`PROVINCE.md:33`: "its unit-state rows sit next to tsukuroi's unit-health ground, which stays tsukuroi's").
  - `hyprctl getoption debug:disable_logs -j`, which is inside the existing read-verb set.
- Existing drift: the round-23 table (`PROVINCE.md:22-30`) claims to cover "every tracked file under `tools/`"
  (`:33`). `ls tools` lists `mado-wsrules.py`, which has **no row** and has been missing since round 27.
  `mado-eventq.py` would be the second unlisted tool. The round-36 refinement (`:50-64`) set the precedent of
  naming new instruments in an append-only refinement.
- Verdict: C2 needs an append-only PROVINCE refinement in the round-36 style. It should name `mado-eventq.py`'s
  three new reads (kernel socket table, session log, unit journal), its write scope (none), and the adjacency
  (tsukuroi for unit health; kagi if log lines carry secret shapes, since the tool emits counts only). It should
  also add the overdue `mado-wsrules.py` row. Neither change is scored, so neither harms an axis.

## Item 4 — SKILL.md: does the new tool get a probe-table row — FINDING (yes)

Command: `rg -n '^#|^\| *(Probe|…)' SKILL.md`; `awk 'NR>=191 && NR<=232' SKILL.md`.

Header and nearest rows (`SKILL.md:204`, `:211`, `:216-217`):

```204:217:/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md
| Probe | Answers | Sample |
// ...
| `hyprctl layers -j` | compositor-side view of bar/launcher layer surfaces | DP-1 levels `2` → `waybar` pid 1707 `3440x26`; level `0` → `wallpaper` (MADO-R3-1 §1; read-only whitelist extension, MADO-R3-2 method) |
// ...
| `pgrep -a` / `ps` | what actually runs | waybar 1707, mako 1706, walker 1808, swayosd 1815, 3x alacritty; hypridle/hyprlock absent |
| `systemctl --user is-active <unit>` | service state | hypridle → `inactive` |
```

- No existing row reads the kernel socket table or the session log. The table's precedent for a lane-internal
  read extension is the `hyprctl layers -j` row ("read-only whitelist extension"). The new row belongs
  directly after it, because it is the compositor-side view of who is listening:
  `| python3 -I tools/mado-eventq.py (reads ss -xpa, never connects) | who is subscribed to .socket2.sock, each
  subscriber's unread backlog, and whether the removal markers can be logged at all | <from the committed live
  receipt> |`.
- The Gate registry (`SKILL.md:593+`, header `| name | gate/probe | entry command | verdict map | … |`) has no
  row for `mado-binds`, `mado-anims` or `mado-wsrules` either. `mado-eventq` has a verdict map (0, 1, 2), so it
  qualifies as a registry `probe` row. Adding it alone would extend an existing omission, not fix it.
- Safety-fence note for the same section (`SKILL.md:223+`, "Mutating commands"): the host's own
  monitor-watch *does* hold a socket2 connection through `socat`. The lane's "never connect" rule applies to
  the lane, not to the host. The probe row should say that the census observes the host's connections and
  never makes one.

## Item 5 — new: `hyprctl descriptions` is a second, contradicting `disable_logs` channel — FINDING

Commands: `hyprctl -j descriptions | python3 …` (shape and counts), then
`python3 -I .ufo/waves/round-37/w1/scratch/ConnFrontier/desc-vs-getoption.py`. Receipt:
`scratch/ConnFrontier/desc-vs-getoption.txt`.

```
descriptions_keys=353 getoption_set_true=71 set_true_with_descriptions_current_equal_default=63
general:gaps_out: descriptions.current="20 20 20 20" descriptions.default="20 20 20 20" getoption={"option": "general:gaps_out", "custom": "0 0 0 0", "set": true}
input:kb_layout: descriptions.current="us" descriptions.default="us" getoption={"option": "input:kb_layout", "str": "br", "set": true}
debug:disable_logs: descriptions.current=false descriptions.default=true getoption={"option": "debug:disable_logs", "int": 1, "set": false}
```

Source, re-opened by me: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp
(59,222 B, sha256 `a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754`).
- `:28` `static std::string jsonify(SP<IValue> v) {`. At `:37-39`, `"current": {}` is filled from
  `x->name(), x->description(), x->defaultVal(), x->value());`.
- `:629` `MS<Bool>("debug:disable_logs", "disable logging to a file", true),`.
- `HyprCtl.cpp:1979-1980` (same commit): `getDescriptions` returns `Config::Values::getAsJson();`.
- **[INFERENCE]** Under the host's legacy hyprlang config, the `Config::Values` objects that `descriptions`
  prints are not the store the legacy manager writes, so `current` shows an unpopulated value. For booleans
  that can even be the opposite of the default.

Consequences:
- `getoption` (the registration's chosen channel) is correct. A refactor, seat or future entry that reads
  `descriptions` instead would print `markers_observable=1` on a host where the logger is off.
- This also confirms ScoutLogger's correction from a second angle: `getoption` shows `"set": false`, so the
  value 1 is the shipped default.
- **[INFERENCE]** The entry `event-queue-observability-r37.md` should name `descriptions` as a refused
  channel, so that nobody "re-verifies" the null-channel finding against it.

## Proposed move (one, bounded)

**Synthesis of C2's live receipt with the frontier and province mapping.** Make the host's *two* known
socket2 subscribers explicit everywhere the round maps itself:

1. Record the C2 live receipt with `--expect-client waybar --expect-client socat`. Peer executors used
   `--expect-client waybar` only (ExecEventqA report `:37`).
2. In the round-37 Frontier subsection, anchor on "Waybar module text" plus the round-16 "freshness" clause,
   not "Walker socket protocol". Add one "still open" line: the monitor-watch exec-once subscriber, and what
   its removal would stop.
3. Add the PROVINCE refinement and SKILL probe row from Items 3-4, plus the overdue `mado-wsrules.py` row.

- **Affected axes:**
  - Operability improves: the live census then guards both host consumers. A removed socat would print
    `missing_client=socat verdict=MISSING_CLIENT`, which is the silent monitor-recovery loss.
  - Coverage improves in accuracy: the frontier text points at the item the theme actually bears on.
  - Neither axis is harmed: the edits are counter-neutral (next section).
- **Why counter-neutral (checked against the frozen predicate text):** `PRED-C2-r37-v2`'s live clause
  (`c2-r37-eventq.py:13-21`) requires `tool_sha256`, `subscribers=N` equal to the client-line count, a
  `comm=waybar` client, and a (comm, pid, fd) multiset that matches the `ss` replay. It never reads
  `missing_client` or `verdict`, and it does not constrain the receipt's flags. `socat` is present now
  (pid 2293), so the receipt's verdict stays `CLEAN`. The C1 counter reads no Frontier text.
  Separability holds because no C1 entry cites the tool.
- **Risks:**
  - The `socat` comm is generic. A future unrelated `socat` socket2 client would satisfy the expectation.
    The comm-only interface is frozen, so this is a stated limit, not something to fix this round.
  - If monitor-watch is ever restarted with a new pid between the snapshot and the receipt, the replay is
    unaffected, because both come from one `ss` capture.
  - The exec-once mapping to arc §6 is a frontier note, not a new U-id. Inventing a U8 would be target
    drift and must not happen.
- **Verification (for the L1 or a reviewer):**
  - `pgrep -x socat` still shows one process.
  - `python3 -I tools/mado-eventq.py --expect-client waybar --expect-client socat` exits 0 with
    `missing_client=` empty.
  - The frozen `python3 -I quality/counters/c2-r37-eventq.py --repo . --rev <tip>` gives
    `live=1`, unchanged by the flag.
  - `grep -n 'Walker socket protocol' <round-37 Frontier subsection>` returns nothing.
  - `git grep -n 'mado-wsrules' <tip> -- PROVINCE.md` returns at least one hit.

## Next desktop surface — considerthese/2026-10-24.md proposal 4, as data

Proposal 4 (`considerthese/2026-10-24.md:49`): "read PROVINCE.md and propose which Hyprland surface is next
(window rules, monitors, layer rules) with the sources that would ground it".

Covered static tables today: binds (`mado-binds.py`), animations (`mado-anims.py`) and workspace rules
(`mado-wsrules.py`). Each is checked against a nested headless v0.56.2 instance's tabular `hyprctl` verb
(`.ufo/waves/round-27/c1/count-v4.py:13`: "`hyprctl workspacerules -j` for the same tree (a nested, headless,
session-isolated instance…"). The ranking criterion is that same property: does v0.56.2 expose a whole-table
read verb that a nested instance can answer, and how much of this host's config populates the table?

Host population (file bytes, `grep -c` over `~/.config/hypr/*.conf`, 13 files): `monitor =` 3, `windowrule =` 9,
`layerrule =` 0, `workspace =` 0, `env =` 4. The omarchy defaults (`default/hypr/*.conf` plus `apps/*.conf`) have
71 `windowrule`/`layerrule` lines, 2 of them `layerrule`. Live read verbs: `hyprctl -j monitors` gives `1 ['DP-1']`;
`hyprctl -j descriptions` gives 353 options, 71 of them `set: true` per `getoption`.

The registered command list comes from re-opening
https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp
(97,582 B, sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`). `:2004-2043` registers
`workspacerules` (`:2005`), `descriptions` (`:2022`), `monitors` (`:2027`), `getprop` (`:2032`) and `getoption`
(`:2039`). `grep -c -E '"(windowrules|layerrules)"' HyprCtl.cpp` gives `0`, so there is no window-rule or
layer-rule list verb.

### Rank 1 — the config-option table (who owns each key, machine-predicted)

- **What:** a static predictor of every option's effective value from the config tree, using the same source
  graph and last-declarer-wins logic as the three existing tools. The oracle is a nested instance's
  `getoption` per name from `descriptions`. It must **not** use `descriptions.current` (Item 5).
- **Why first:**
  - It has a whole-table oracle without spawning any client.
  - The host has 71 set options, the largest config-set population of any candidate.
  - It replaces the lane's manual 56-pair `getoption` layer (`hyprctl-verification-layer.md` §3) and backs the
    SKILL "Who-owns-it table" (`SKILL.md:69`) with an instrument.
  - Item 5 proves that the obvious oracle (`descriptions`) is wrong, which is exactly the kind of trap a
    frozen predicate must pin.
- **Sources (opened 2026-10-25):**
  - HyprCtl.cpp (above) `:2039` `registerCommand(SHyprCtlCommand{"getoption", false, dispatchGetOption});`.
  - ConfigValues.cpp (above) `:168` `MS<Int>("general:border_size", "size of the border around windows", 1, {.min = 0, .max = 20, …`:
    the compiled option table, including defaults.
  - https://wiki.hypr.land/0.54.0/Configuring/Using-hyprctl/ (172,023 B, sha256 `3f02dc8e…`; rendered-text
    line 266 via `scratch/ConnFrontier/h2t.py`): "getoption [option] - gets the config option status (values)".
  - https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/config-options.md
    (58,686 B, sha256 `4e21fdba…`) `:6`: "This page documents all Hyprland configuration options except
    layout-specific ones." This page is Lua-era; the hyprlang grammar is in the 0.54.0 archive.
- **Caveat:** typed values (gradients, CSS gaps, vec2) need normalization, and the Lua era is out of scope.

### Rank 2 — monitor rules → `hyprctl monitors [all]`

- **What:** predict which `monitor =` rule each output takes and the resulting mode, position, scale and
  transform.
- **Why second:**
  - There is a tabular verb.
  - It is the direct successor of this round: the host's only non-Waybar socket2 subscriber exists to react
    to `monitorremoved` (Item 2).
  - U5 output management (`output-colour-boundaries-r14.md`) is documentary only.
  - Limit: the oracle is weak for this host's real rules. A headless instance has `HEADLESS-n` outputs, so
    `DP-1`/`desc:` matching and real mode lists cannot be reproduced **[INFERENCE]**. Only name and wildcard
    selection and the layout arithmetic are testable. The population is small (3 user lines, 1 live monitor).
- **Sources (opened 2026-10-25):**
  - HyprCtl.cpp `:2027` `registerCommand(SHyprCtlCommand{"monitors", false, monitorsRequest});`, and `:320`
    `if (vars.size() == 2 && vars[1] == "all")`.
  - https://wiki.hypr.land/0.54.0/Configuring/Monitors/ (174,164 B, sha256 `3456b6db…`; rendered-text line
    128): "monitor = name, resolution, position, scale".
  - https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/monitors/_index.md
    (5,324 B, sha256 `26331840…`) `:12`: "| output | Output name or `desc:...` description prefix | string | [[Required]] |".
  - https://wiki.hypr.land/0.56.0/Configuring/Basics/Monitors/ (sha256 `ad5ea276…`; rendered-text line 248):
    "Since Hyprland 0.55, hyprlang is deprecated in favor of lua." This is the era fence.

### Rank 3 — window rules (and layer rules)

- **What:** predict which rules match a window or layer and the applied effects.
- **Why third:**
  - It has the most host bytes (9 user plus 71 omarchy rule lines) and the highest value.
  - But there is **no list verb** in v0.56.2 (the zero count above). The oracle would have to be
    `getprop` per window (`:2032`) or `clients` tags on live client windows inside the nested instance.
    That means spawning Wayland clients, a new mechanism the three existing counters never needed.
  - Round 24 already found there is no attribution channel (`rule-attribution-r24.md`). Layer rules are thin
    on this host (0 user, 2 omarchy).
- **Sources (opened 2026-10-25):**
  - HyprCtl.cpp `:2032` `registerCommand(SHyprCtlCommand{"getprop", false, dispatchGetProp});`.
  - https://wiki.hypr.land/0.54.0/Configuring/Window-Rules/ (182,142 B, sha256 `e11da0e1…`; rendered-text
    line 144): "windowrule = match:class my-window, border_size 10". Line 547:
    "layerrule = blur on, match:namespace waybar".
  - https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/rules/layer-rules.md
    (2,129 B, sha256 `a513798f…`) `:28`: "| namespace | Namespace of the layer. Check `hyprctl layers` | [RegEx] |".

Not shortlisted: `devices` (a headless instance has no input devices), and `env =` (arc §6: "no query surface
for the compositor's env").

## Contradictions stated, not smoothed

- The registration says the round moves "Walker socket protocol … (the event-socket client half)". The bytes
  show that bullet's socket item is Walker's socket. The theme's real frontier hit is Waybar module text and
  "freshness".
- The C1 counter certifies the Coverage map. The Frontier text is uncounted, so a wrong anchor passes any gate.
- PROVINCE claims to inventory every tracked tool, but `mado-wsrules.py` has had no row since round 27.
- `descriptions.current` and `getoption` disagree on `debug:disable_logs` (false versus 1) and on 63 of 71
  config-set options.

## Exact commands run (beyond file reads)

```
curl -fsSL -o HyprCtl.cpp https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp
curl -fsSL -o ConfigValues.cpp …/src/config/values/ConfigValues.cpp        # plus BoolValue.cpp, IValue.cpp
curl -fsSL "https://api.github.com/repos/hyprwm/hyprland-wiki/git/trees/c04680a2…?recursive=1"  # path discovery
curl -fsSL …/hyprland-wiki/c04680a2…/content/configuring/{core/monitors/_index.md,core/config-options.md,core/rules/window-rules.md,core/rules/layer-rules.md,core/advanced-configuration/using-hyprctl.md,core/environment-variables.md}
curl -sL https://wiki.hypr.land/{0.56.0/Configuring/Basics/{Monitors,Variables,Window-Rules,Layer-Rules},0.54.0/Configuring/{Monitors,Variables,Window-Rules,Using-hyprctl}}/   # 0.56.0 Layer-Rules → 404
python3 h2t.py w-*.html                                  # rendered-text line numbers cited above
hyprctl -j descriptions | python3 …   → descriptions_entries 353; keys [current, default, description, map, max, min, name]
hyprctl -j monitors | python3 …       → monitors 1 ['DP-1']
hyprctl version | head -1             → Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
python3 -I scratch/ConnFrontier/desc-vs-getoption.py     → receipt quoted in Item 5
pgrep -a socat | awk '{print $1,$2}'  → 2293 socat
grep -c -E <rule patterns> ~/.config/hypr/*.conf and omarchy default/hypr  → counts quoted above
```

All fetch digests and sizes are in `scratch/ConnFrontier/fetch-digests.txt`. No journal line, log line or
window title is reproduced here.
