# CustomExec — round 16 / w1 — report

Seat: `MadoR16.CustomExec` (scout, leaf; no delegation, no background jobs).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Axis: **coverage** (U7 Waybar module text observation boundary). No axis verdict is issued.
Scope: tagged S053 `waybar-custom(5)` manual only; `exec`/`exec-if`/`exec-on-event`/
`interval`/`restart-interval`/`signal` scheduling semantics. No commands, no producer
execution, no package/service/live probe.

---

## Outcome

- Opened the **tagged** Waybar 0.15.0 custom-module manual, not the mutable latest page.
  `[OBS-source]` `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd`,
  accessed 2026-10-20: **6656 bytes**, **250 lines**, SHA-256
  `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82`.
- Pinned the tag: `git ls-remote` resolves `refs/tags/0.15.0` to commit
  **`90b209add8937514d0a987aa842e701bd8f1232e`** (one line, no peeled tag object).
  The commit-pinned URL returns **byte-identical** bytes (`cmp` clean, same SHA-256).
- Confirmed the wave's existing binding:
  `.ufo/waves/round-16/evidence/source-bindings.json` records the same S053 URL,
  `bytes: 6656`, and the same SHA-256. This report adds exact line anchors; it does
  not create a second provenance chain.
- Extracted the documented scheduling contract: a gated producer (`exec-if` exit 0),
  four update regimes (numeric `interval`, `once`, self-looping, signal-only), a
  restart policy (`restart-interval`), and an event re-execution trigger
  (`exec-on-event`, default true).
- Found the manual **does not resolve** numeric-`interval` + `signal` precedence, and
  **does not document** process invocation (shell/argv/env/cwd), timeout, buffering,
  stdin/stdout/stderr handling, concurrency, or any module-text readback surface. These
  are the load-bearing limits for U7.
- The current U7 note's Producer-contract paragraph is directionally correct but
  under-specified (below, §5). No sibling file was edited.
- Zero tools installed or updated; no package transaction, signal, service, compositor,
  screenshot, producer, or UI action was performed.

---

## 1. Source identity and exact anchors

`[OBS-source]` S053 tag **0.15.0** → commit **`90b209add8937514d0a987aa842e701bd8f1232e`**;
file `man/waybar-custom.5.scd`; **6656 bytes**, **250 lines**; SHA-256
`efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82`.
Anchor numbering below is the line number in that exact file. The scd file carries no
internal version/date header (line 1 is only `waybar-custom(5)`); tag identity comes from
the URL/commit pin, not from document metadata.

Scheduling fields occupy the `CONFIGURATION` block:

| Field | Line span | Declared type / default |
|---|---|---|
| `exec` | 15–17 | string |
| `exec-if` | 19–22 | string |
| `hide-empty-text` | 24–26 | bool (display gate; adjacent, not scheduled here) |
| `exec-on-event` | 28–31 | bool, default **true** |
| `return-type` | 33–35 | string (CustomMan lane) |
| `interval` | 37–43 | integer or float; also the undocumented-for-type string `once` |
| `restart-interval` | 45–50 | integer or float |
| `signal` | 52–56 | integer |
| `on-update` | 99–101 | string (update-triggered action; adjacent) |
| `format` / `{text}` | 58–61, 168–170 | display mapping (CustomMan lane) |

### 1.1 Local installed-man cross-check

`[OBS-local-doc]` `/usr/share/man/man5/waybar-custom.5.gz` (decompressed 7744 bytes,
SHA-256 `915dcb4c9118f0df53cfefc888b3b457a44127b5926619683ea27e9c6abed88e`; scdoc
1.11.5; `.TH … "2026-08-31"`) contains **all 16 scheduling quotes below verbatim**
after roff unescaping and whitespace normalization. This shows the local document is not
a divergent edition of these paragraphs.

Limit: the installed man is a rendered local artifact, not the tag binding; its `.TH`
date is build metadata; the cross-check does **not** establish installed-binary/source
equivalence, package health, or running behavior. It is not used as source authority.

---

## 2. Documented scheduling contract (facts and direct reading)

All quotes are exact scdoc text; `*…*` is scdoc emphasis markup. Every quote is **≤25
words** (count in parentheses) and was checked as an exact line match after removing the
` ++` continuation marker.

### 2.1 Producer and gate

- `S053:15-17` — “The path to the script, which should be executed.” (9 words)
  `[OBS-source]` `exec` names the producer script; the manual calls the value a path.
- `S053:19-22` — “*exec* will be executed if the exit code of *exec-if* equals 0.”
  (12 words) `[OBS-source]` The producer is gated by a second script: exit 0 permits
  `exec`; any other exit does not. The manual does not state what is displayed on a
  non-zero gate (that is S054/failure-lane territory).
- `S053:28-31` — “If an event command is set (e.g. *on-click* or *on-scroll-up*) then
  re-execute the script after executing the event command.” (19 words)
  `[OBS-source]` With `exec-on-event` at its default `true`, a configured event command
  is a third invocation trigger, in addition to interval/signal. “After” is an ordering
  claim only; the manual does not state whether the event command is waited on, whether
  its effect is visible to the re-execution, or whether the re-execution re-runs
  `exec-if`.
- `S053:99-101` — “Command to execute when the module is updated.” (8 words)
  `[OBS-source]` `on-update` is documented as an update-triggered action, not a text
  source. The manual does not define which updates count (startup, poll, signal, event),
  their ordering, or whether `on-update` itself counts as an “event command” under
  `S053:31`. `[UNK]` A re-exec feedback loop through `on-update` is not resolved by S053.

### 2.2 Update regimes

- Poll — `S053:37-40`:
  - “The interval (in seconds) in which the information gets polled.” (10 words)
  - “Minimum value is 0.001 (1ms). Values smaller than 1ms will be set to 1ms.” (14 words)
  `[OBS-source]` A numeric `interval` is a recurring poll in seconds with a 1 ms floor.
  `[INF-docs]` “Polled” implies repeated producer invocation; S053 does not state
  overlap, cancellation, wait-for-exit, or what happens when a run outlives the interval.
- Startup-only — `S053:41`: “Use *once* if you want to execute the module only on
  startup.” (12 words) `[OBS-source]` `once` is a string sentinel accepted by a field
  declared `integer or float`; the type declaration does not cover it.
- Self-looping — `S053:42`: “If no *interval* or *signal* is defined, it is assumed that
  the out script loops itself.” (17 words) `[OBS-source]` The continuous mode applies
  only when **neither** field is set: the script is expected to keep running and produce
  its own updates. The same line also says “You can update it manually with a signal.”
  (8 words), which is the source of the contradiction in §3.1.
- Signal-only — `S053:43`: “If a *signal* is defined then the script will run once on
  startup and will only update with a signal.” (20 words)
  `S053:52-56`: “The signal number used to update the module.” (8 words) and “The number
  is valid between 1 and N, where *SIGRTMIN+N* = *SIGRTMAX*.” (12 words) and “If no
  interval is defined then a signal will be the only way to update the module.”
  (17 words) `[OBS-source]` The config value is an **RT-signal offset**, not an absolute
  signal number: the configured `N` is added to `SIGRTMIN`. The documented range starts
  at 1, so offset 0 (`SIGRTMIN` itself) is outside the stated range. `N` is symbolic
  (platform/libc dependent); S053 gives no numeric bound and no out-of-range behavior.
  `[INF-docs]` The examples imply the bar process is the signal target and that a signal
  causes a refresh of the producer, but S053 does not explicitly say the signal
  re-executes `exec` versus re-rendering already-produced output.

### 2.3 Restart policy

- `S053:45-50`:
  - “The restart interval (in seconds).” (5 words)
  - “Minimum value is 0.001 (1ms). Values smaller than 1ms will be set to 1ms.” (14 words)
  - “Can't be used with the *interval* option, so only with continuous scripts.”
    (12 words)
  - “Once the script exits, it'll be re-executed after the *restart-interval*.” (10 words)
  `[OBS-source]` `restart-interval` is a continuous-mode policy: when the producer exits,
  wait `N` seconds, then execute it again. The manual states incompatibility with
  `interval` but does not state whether that is enforced at configuration parse, which
  field wins, or whether the `once` sentinel counts as the `interval` option. `[UNK]`
  The interaction with `signal` is also unstated.

### 2.4 Regime summary

| Regime / policy | Documented condition | Documented behavior | Anchor |
|---|---|---|---|
| Numeric poll | numeric `interval` | poll every N s, floor 1 ms | 37–40 |
| Startup only | `interval: once` | execute only at startup | 41 |
| Continuous stream | neither `interval` nor `signal` | script loops itself | 42 |
| Signal-only | `signal` set | run once at startup, then update by signal | 43, 52–56 |
| Restart | `restart-interval`, continuous scripts | re-execute after producer exit + N s | 45–50 |
| Event re-exec | event command + `exec-on-event` (default true) | execute event command, then re-execute script | 28–31 |

`[INF-docs]` These are documentation-level regimes, not a state machine proven by
S053. The manual does not say how the four regimes combine (other than the one
incompatibility it names), does not give a startup order relative to bar mapping, and
does not give any freshness guarantee between an invocation and a visible update.

---

## 3. Contradictions and documented silences (U7 load-bearing)

### 3.1 Numeric `interval` + `signal` is not resolved

`[OBS-source]` The file contains both:

- `S053:39`: interval = “The interval (in seconds) in which the information gets polled.”
- `S053:42`: “You can update it manually with a signal.”
- `S053:43`: signal defined ⇒ “the script will run once on startup and will only update
  with a signal.”
- `S053:56`: “If no interval is defined then a signal will be the only way to update the
  module.”

Reading `42` and `39` together, numeric polling and manual signal refresh can coexist.
Reading `43` unconditionally, a defined signal suppresses interval updates. Reading `56`
conditionally, signal is exclusive only when no interval exists. S053 gives no
precedence rule. The examples do not resolve it: the Pacman example pairs
`interval: "once"` with `signal: 8` (`S053:223-229`), which is startup-only + signal under
either reading; the alternate Pacman example uses `signal: 8` with no interval
(`S053:235-241`). **No example pairs a numeric interval with a signal.**

`[UNK]` Therefore docs alone cannot say whether a module with both numeric `interval`
and `signal` polls, is signal-only, or does both. Resolution requires S054 (implementation),
not choosing one sentence. The U7 note must not assert a precedence.

### 3.2 `exec`/`exec-if` invocation is under-specified

`[OBS-source]` The fields are declared as “The path to the script” (`S053:17`) and “The
path to a script” (`S053:21`), but the examples use values that are not paths and that
rely on shell-like behavior:

- `S053:185` `exec` expands `$HOME` and redirects `2> /dev/null`;
- `S053:212` `exec` contains quoted arguments;
- `S053:237` `exec` contains a pipeline;
- `S053:186`, `S053:199`, `S053:213` `exec-if` values are command lines with arguments;
- `S053:238` `exec-if` value is the shell builtin `exit 0`.

`[INF-docs]` The examples imply shell-style command strings, while the prose says
“path”. `[UNK]` S053 does not define shell-versus-direct execution, argument splitting,
environment, working directory, `stdin`/`stdout`/`stderr`, timeout, exit-code handling
beyond `exec-if` = 0, output size limits, or concurrency. Reproducing a producer
invocation cannot be justified from S053 alone.

### 3.3 No documented readback or observation surface

`[OBS-source]` The 250-line file contains **zero** occurrences (case-insensitive literal
search) of: `read`, `query`, `ipc`, `cache`, `dbus`, `SIGUSR`, `reload`. Its only update
vocabulary is poll/interval, signal, event and restart. It documents no verb that returns
current module text or producer output.

`[INF-docs]` Therefore S053 supports only a **write/trigger** model: an update is caused
by internal polling, an event command, or an external signal to the bar. There is no
documented pull/query path. Any observation of current text must come from a separately
authorized producer invocation, a later authorized widget/UI observation, or waiting for
the next internal update — none of which S053 supplies. Even then, producer output would
prove only that invocation, not the bar's retained or rendered value.

### 3.4 Signal is an action, not an observation

`[OBS-source]` `S053:52-56` defines the update signal as an RT offset in `1..N`; the two
Pacman examples (`S053:219-244`) are the only places the manual shows an external
process-signaling update, and the second one also contains a package-transaction
example (`S053:239`). Those example bytes are documentation data, **not authorization**
for this source-only round and were not executed. `[INF-docs]` Sending the offset signal
to the bar is a host action; it is not a read, and S053 promises nothing about coalescing,
queueing, delivery during a running producer, or the resulting text.

### 3.5 Documented silences (exact, reproducible)

`[OBS-source]` Case-insensitive literal counts over the exact 6656-byte file:
`shell` 0, `timeout` 0, `buffer` 0, `stderr` 0, `stdout` 0, `environment` 0,
`working directory` 0, `concurrent` 0, `spawn` 0, `fork` 0, `pipe` 0, `stdin` 0,
`read` 0, `query` 0, `ipc` 0, `cache` 0, `SIGUSR` 0, `reload` 0.

`[INF-docs]` This is a scheduling contract at the level of seconds, startup, exit,
events and signals — not a process-execution contract, not a consumption contract, and
not an observation contract. The man can say *when* a producer may be invoked; it cannot
say how its bytes are collected, whether a given invocation succeeded, or what pixels
result.

---

## 4. What this establishes for U7, and what it does not

`[OBS-source]` The manual's own layer is **intended producer scheduling**. It is not the
installed binary, not a configured module, not a producer run, not a parser, and not a
renderer.

| Claim | Verdict | Basis |
|---|---|---|
| A custom module can be configured with a producer script gated by `exec-if` exit 0 | established as docs | `S053:15-22` |
| The manual documents numeric polling, `once`, continuous-loop, signal-only and restart policies | established as docs | `S053:28-56` |
| Event commands can re-execute the producer by default | established as docs | `S053:28-31` |
| Numeric interval + signal precedence | **not established** | `S053:39/42/43/56` conflict; no example |
| Producer invocation mechanism (shell/timeout/buffering/env) | **not established** | zero-term search; examples vs “path” prose |
| Current module text can be read through a documented surface | **not established** | no read/query/IPC term; push-only vocabulary |
| A signal causes re-execution versus re-render | **not established** | `S053:43` wording; examples imply re-run only |
| Successful producer invocation equals displayed text | **not established** | scheduling is upstream of parsing/format/GTK |
| Rendered glyphs, markup acceptance, clipping, tooltip display | **not established** | renderer/GTK layer, outside S053 |

`[UNK]` Unresolved by S053 and left to other lanes/source: non-zero `exec-if` display,
empty-output display, `restart-interval` enforcement details, `once` + `restart-interval`,
signal + `restart-interval`, event re-execution versus `exec-if`, `on-update` ordering
and feedback, signal out-of-range handling, and installed-binary/tag equivalence.
S054 owns parsing/visibility/label-update mechanics; this report does not assert them.

---

## 5. Direct use in the existing U7 note (Producer contract)

The note `corpus/knowledge/waybar-observation-boundaries-r16.md:26-30` currently says the
manual “distinguishes polling `interval`, signal refresh and continuous scripts with
optional `restart-interval`.” That is true but omits `once`, the 1 ms floor, the
default-on event re-execution, the RT-offset formula, and the unresolved
interval+signal case. Proposed replacement for the middle of that paragraph (the note's
two closing sentences, “None is authorization…” and “A command's output…”, should stay):

> The manual documents four update regimes: numeric `interval` polling with a 1 ms floor;
> `once` at startup; a self-looping script when neither interval nor signal is set; and a
> startup run followed by signal-only updates when `signal` is set (S053:37-43, 52-56).
> `restart-interval` re-runs a continuous script after it exits and is documented as
> incompatible with `interval` (S053:45-50). A configured event command re-runs the
> script after that command by default (S053:28-31). Numeric `interval` plus `signal`
> precedence is not resolved: S053:39 calls interval a poll, S053:42 permits manual
> signal updates, S053:43 says signal-only, and S053:56 conditions signal-only on no
> interval; no example pairs a numeric interval with a signal. S053 also never defines
> shell, timeout, buffering, environment, stdin/stdout/stderr, concurrency or readback.
> `signal` is an RT offset in 1..N with SIGRTMIN+N = SIGRTMAX (S053:52-56), and the
> manual documents no query verb for current text.

Optional anchor refinement for the note's `source:` line (head-15): add
`CONFIGURATION:15-56` and the tag commit
`90b209add8937514d0a987aa842e701bd8f1232e`; the byte/digest values already match
`evidence/source-bindings.json`. This is advice only; the note and SOURCES.md are owned
by other seats.

---

## 6. Confidence, limits, and process

Confidence:
- **High** for source identity, digests, line anchors, quote text, quote word counts, and
  the zero-term search (`[OBS-source]` exact file bytes).
- **Medium-high** for the regime synthesis (`[INF-docs]`, direct reading of one complete
  file).
- **Low / `[UNK]`** for anything about the installed binary, configured modules, current
  text, signal delivery, update timing, parsing, GTK, and rendering.

Process and limits:
- No LSP server applies to a scdoc man page, and no `lsp` device is mounted here
  (`xd://lsp` returns “No such tool”); anchors are literal line numbers in the tagged
  file, not semantic symbol resolution.
- Source fetches were HTTPS GETs of the tagged URL and the commit-pinned URL; tag commit
  was resolved read-only with `git ls-remote`. No producer, script, event command, signal,
  package transaction, service/compositor operation, screenshot, or UI probe was run.
- Scope slip disclosed: one read-only `pacman -Q waybar` query was issued in the first
  scouting batch (returned `0.15.0-3`). It is **not**
  used as evidence, no sync/install/upgrade/remove/downgrade or service operation
  followed, and no further host query was made. The local man cross-check in §1.1 is a
  file read, not a package operation.
- Zero tools installed or updated. No missing prerequisite blocked this lane.
- No lane/fleet files written except this report; source scratch was kept under `/tmp`.
  No commits; no fleet/sibling edits.
