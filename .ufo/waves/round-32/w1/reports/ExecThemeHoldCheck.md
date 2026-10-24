# ExecThemeHoldCheck — C1 do-nothing control (round 32, w1)

Seat: ExecThemeHoldCheck (leaf member; no subagent dispatch used).
Question: is the C1 theme — the Hyprland IPC two-socket REQUEST/EVENT
contract + dispatcher surface — already held by the lane, and can a
one-sided ("do-nothing") commit reach the frozen C1 counter?

Verdict: **theme not held**; **both one-sided controls fail the counter.**

- Lane state: jj working copy `@` = `ade66d563381adce82bcab0f5d238ee0158d2d4c`
  (git HEAD `50e6a8f32bfaf0487b2762eb3b5c9f51ed54b75c`); registration base
  `256222890d935212874a09751ff9b7869943c2d7`.
- Frozen counter verbatim on the live lane:
  `entries=0 rows=0 cited_entries=0` — target `entries=3 rows=5 cited_entries=3`.
- `corpus/knowledge/` holds **43** notes; none of the three C1 entry files
  exists (`ipc-contract-r25.md`, `dispatcher-semantics-r25.md`,
  `dispatcher-surface-and-request-grammar-r26.md` all absent); registry
  carries **0** rows for S186/S187/S188/S189/S196.

The four claims checked per note (from the registered C1 entry
`ipc-contract-r25.md`): **(a)** request socket path, **(b)** event socket
path, **(c)** request grammar, **(d)** event framing.

## 1. Knowledge sweep — prescribed grep, 11 hits

Command run exactly as prescribed:

```sh
grep -rilE 'socket2|\.socket\.sock|dispatcher' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/
```

Hits (11 of 43): `hyprctl-verification-layer.md`, `keybind-rule-semantics.md`,
`config-health-report-r3.md`, `remaining-planes-census.md`,
`omarchy-drift-watch.md`, `gate-standing-use.md`, `arc-synthesis.md`,
`closeout-r11.md`, `hyprland-config-era-r12.md`, `rule-attribution-r24.md`,
`bind-table-r25.md`.

Per-note quoted context and claim matrix below. `YES` = the note asserts the
claim; `PRTL` = the path/name is present but the requested role/framing is
not asserted; `NO` = absent; `—` = word match is a different sense
(Hyprland *bind dispatchers* or Omarchy `bin/omarchy` router, not IPC).

### `hyprctl-verification-layer.md` — (a) PRTL (b) PRTL (c) NO (d) NO

```text
29:| instance | `HYPRLAND_INSTANCE_SIGNATURE` set, shape `<commit>_<epoch>_<pid>` (shape only); one socket dir `/run/user/1000/hypr/<sig>/` |
30:| IPC surface | that dir contains `.socket.sock`, `.socket2.sock` (both `srwx`), `hyprland.lock`, `hyprland.log` (967,994 B, not read) |
31:| instances | `hyprctl -j instances` → one entry; its `wlSocket` field is `null` `[UNK]` why |
…
233:with `.socket.sock`; `hyprctl` cannot connect; more than one instance and the
234:target is ambiguous (do not guess with `--instance`; resolve via the running
235:session's own signature).
```

Both filenames are inventoried under "IPC surface" and `.socket.sock` is the
socket hyprctl connects to — so the paths exist on record, but the note
never assigns REQUEST vs EVENT roles, never states the request grammar
(`/j` prefix, `[[BATCH]]`, command+args), and never states the event framing
(`name>>data` lines). This is a live-probe inventory, not the contract.

### `config-health-report-r3.md` — (a) PRTL (b) PRTL (c) NO (d) NO

```text
165:- instances: 1; `wl_socket` present as `wayland-1` in `-j` (F8); socket dir
166:  `/run/user/1000/hypr/<sig>/` holds `.socket.sock`, `.socket2.sock` (both
167:  `srwx`) and `hyprland.lock` — R2-1 §1 surface claim re-verified; signature
168:  shape `<commit>_<epoch>_<pid>` only.
169:- `configerrors` empty, rc=0; `version` 0.56.2, commit `efb5099…` (equal).
```

Same inventory-style re-verification; no roles, grammar or framing. Other
hits in this file (`dispatchers n=24`, line 130 histogram) are bind
dispatchers, a different sense.

### `bind-table-r25.md` — (a) YES (b) NO (c) NO (d) NO

```text
66:Hyprland accepts `--config FILE` and hands the validated explicit path to the compositor; hyprctl `-i` selects an instance by signature or index and routes the request through that instance's runtime socket. [S171, pinned `SrcHyprlandMain.bin:120-144,263-264`, quote: "g_pCompositor->m_explicitConfigPath = configPath;"; S169, pinned `S169.bin:427-435,493-520,227-235`, quotes: "ARGS[i] == "--instance" || ARGS[i] == "-i""; "instanceSignature = overrideInstance;"; "getRuntimeDir() + "/" + instanceSignature + "/.socket.sock"]
```

This is the closest existing hold: `.socket.sock` is explicitly the path a
hyprctl request is routed through (claim a held, as a hyprctl-client fact).
But no `.socket2.sock` event socket, no request grammar (the wire format of
what is written to the socket), no event framing. The note is about bind
tables; other `dispatcher` hits in it are the bind field.

### `remaining-planes-census.md` — (a) NO (b) PRTL (c) NO (d) NO

```text
234:- **OSD / display daemons.** `swayosd-server` user unit active (§2);
235:  `omarchy-hyprland-monitor-watch` PID 1203378 plus its pipeline subshell
236:  1203555 (`socat -U - "UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$…/.socket2.sock"
237:  | while read …` — watches `monitorremoved*` events; the two PIDs are one
238:  script + its `while` subshell `[INF]`).
```

An observed **consumer** of `.socket2.sock` that reads events
(`monitorremoved*`) — the event-role of the second socket is implied by this
one daemon's behavior, but the note does not state the contract: no request
socket counterpart, no event name `>>` data framing, no general socket2
event model.

### `rule-attribution-r24.md` — (a) NO (b) PRTL (c) NO (d) NO

```text
64:- **No attribution channel.** Wave-1 seat ScoutAttributionSweep swept the v0.56.2 tree per channel: hyprctl
65:  (`getprop` renders the applicator value, `src/debug/HyprCtl.cpp:1548-1553`; the only rule-listing verb is
66:  `workspacerules`, `:2005`), Lua (`LuaWindowRule.cpp:58-70` exposes only `set_enabled`/`is_enabled`), socket2
67:  (35 event names, none for rules), logs, the window object (`OverridableVar.hpp:153` keeps one optional value per
68:  override priority; `getPriority()` is not exported) and the plugin bus (`updateRules` carries the window only).
…
128:v0.56.2 channel (39 hyprctl commands, Lua window/query/handle APIs, 45 socket2 event names, 69 plugin-bus events,
…
161:   prints `unknown request` on this host when the set is empty; `-j` prints `[]` (AtkEraWiki). The socket2
162:   inventory is 45 distinct names from 76 `postEvent` call sites, not 35 (AtkSocketChannel).
```

socket2 is treated as an **event-name inventory** channel (45 names from 76
`postEvent` sites) swept for rule attribution — event *names*, not event
*framing*; no path, no grammar, no `name>>data` wire format. (`A dispatcher
can add an identical "X*" string` at :141 is the bind-dispatcher sense.)

### `keybind-rule-semantics.md` — (a)–(d) NO (different sense; dispatcher surface partially covered, see note)

```text
15:**Claim boundary.** The lane ran no keystroke injection, no `hyprctl dispatch`, and mutated
17:read-only `hyprctl` queries (`binds`, `clients`, `getoption`), which verify how the host's
18:**parser** interpreted declared binds (fields, modmask, flags) and the live tag state — not
19:what a dispatcher does when fired.
…
134:## 3. Dispatcher inventory — per-dispatcher semantics (24 live) `[OBS]` counts, `[INF-docs]` semantics
…
288:## 6. Unknowns
289:1. **No dispatcher was fired.** All per-dispatcher semantics are `[INF-docs]`; the lane
290:   verified parsing (modmask/flags/args), not behavior.
```

All hits are the **bind-dispatcher** sense: a 24-dispatcher inventory with
doc-derived semantics, explicitly unfired. This is adjacent to C1's
`dispatcher-semantics-r25.md` entry — the lane already holds *declared
forms + counts + `[INF-docs]` semantics + the "never fired" boundary* for
the dispatcher vocabulary, on this host (0.56.2). What it does **not** hold:
any statement tying dispatchers to the IPC contract (`hyprctl dispatch` →
request socket), and none of (a)–(d).

### `omarchy-drift-watch.md` — (a)–(d) NO (different sense)

```text
130:  binary exists (`ls` → No such file), so direct-route resolution
131:  (`bin/omarchy:349-372`) cannot match, and prefix help only matches when the
132:  input *is a prefix of* a route (`bin/omarchy:1030-1034`) — it is not.
134:  `[INF]` from the command table + dispatcher code; the verb was **not
135:  executed** (§7). Candidate erratum for the skill lane (append-only; not
```

"dispatcher" = Omarchy's `bin/omarchy` subcommand router. Unrelated.

### `gate-standing-use.md` — (a)–(d) NO; explicitly *unheld*

```text
280:- a **stub scenario proves row logic, never live values** — the hermetic
281:  fixtures exercise the code path, not the host;
282:- rendered UI, socket protocol, idle/lock transitions, dispatcher behaviour,
283:  waybar module text, window-rule *effects* have no read surface: they stay
284:  **UNKNOWN by constraint**, never guessed;
```

The lane's own gate note lists "socket protocol" and "dispatcher behaviour"
as surfaces with **no read surface → UNKNOWN by constraint**.

### `arc-synthesis.md` — (a)–(d) NO; gap ledger names both surfaces

```text
296:| rendered UI / screenshots | no landing site in the gate; grim read to stdout was a one-off probe (r1/r2), never a verdict input |
297:| walker socket protocol | never connected (constraint); the r9 note measured shape only — protocol semantics UNKNOWN |
299:| dispatcher behaviour | no keystroke injection allowed — `[INF-docs]` only (r2, 24 dispatchers) |
…
336:**Unknown (12 named):** rendered UI · walker socket protocol · idle
337:transitions · dispatcher behaviour · window-rule effects · exec-once results ·
```

(`walker socket protocol` is the launcher, not Hyprland IPC.) The arc gap
ledger explicitly carries dispatcher behaviour as a named Unknown.

### `closeout-r11.md` — (a)–(d) NO

```text
41:| hypr-live | `configerrors` empty rc 0; 57/57 `getoption` 0 mismatch; 46 agreement + 6 agreement* + 4 live-default; dispatcher behaviour `[INF-docs]`/[UNK] [OBS-record] | hyprctl live read |
43:| walker | 2.17.0; sockets `stat`'d 0 B, never connected; no reload path — restart is the apply path | consumer-side probe |
```

Recorded verdict: dispatcher behaviour `[INF-docs]`/`[UNK]`; the only
sockets stat'd are walker's.

### `hyprland-config-era-r12.md` — (a)–(d) NO

```text
97:| `corpus/README.md:49` — config, binds, rules and display route | Parsed declarations do not prove dispatcher behavior, rule effects, or `exec-once` results. | Keep syntax validation, effective-state reads, and behavior tests distinct; no rule is fired by this entry. |
```

A risk-register row reiterating that dispatcher behavior is unproven.

### Claim matrix (aggregate)

| Note | (a) req path | (b) event path | (c) req grammar | (d) event framing |
|---|---|---|---|---|
| hyprctl-verification-layer | PRTL | PRTL | NO | NO |
| config-health-report-r3 | PRTL | PRTL | NO | NO |
| bind-table-r25 | YES | NO | NO | NO |
| remaining-planes-census | NO | PRTL | NO | NO |
| rule-attribution-r24 | NO | PRTL | NO | NO |
| keybind-rule-semantics | NO | NO | NO | NO |
| omarchy-drift-watch | NO | NO | NO | NO |
| gate-standing-use | NO | NO | NO | NO |
| arc-synthesis | NO | NO | NO | NO |
| closeout-r11 | NO | NO | NO | NO |
| hyprland-config-era-r12 | NO | NO | NO | NO |

**No note holds the two-socket REQUEST/EVENT contract.** (a) is held only in
`bind-table-r25.md` as a hyprctl `-i` routing fact; (b) is implied only by
one observed socat consumer; (c) and (d) are held nowhere — and two notes
(`gate-standing-use`, `arc-synthesis`) affirmatively list this surface as
UNKNOWN. The dispatcher-surface half is held only at the binds-declaration
level (`keybind-rule-semantics` §3, all `[INF-docs]`, none fired), which the
C1 entries supersede, not duplicate.

## 2. Coverage map (`corpus/README.md`) — no row Holds the IPC contract

`grep -nEi 'socket2|\.socket\.sock|dispatcher|ipc' corpus/README.md` →
6 lines (16, 18, 47, 70, 71, 91). The three index rows whose Holds cells
touch the surface (verbatim, wrapped):

- Row 16 (`keybind-rule-semantics.md`), Holds ends: *"24-dispatcher
  inventory §3 (live counts = declared counts; semantics `[INF-docs]` —
  **no dispatcher was fired**) … unknowns §6 (behaviour unexercised —
  parsing verified, not dispatch)"* — holds dispatcher *inventory*, not the
  IPC contract.
- Row 18 (`config-health-report-r3.md`), Holds: verification-pass summary;
  "24 dispatchers … all equal" — no socket/IPC claim.
- Row 47 (`rule-attribution-r24.md`), Holds: *"no upstream channel maps an
  applied property back to its rule (hyprctl, Lua, socket2, logs, window
  object, plugin bus swept)"* — socket2 appears only as a swept channel in a
  negative result.
- Row 70 province-routes Limit: *"Parsed declarations do not prove
  dispatcher behavior, rule effects or exec-once results."*
- Frontier, lines 90–92: *"Index completeness does not retire these
  unresolved surfaces: Rendered UI, Waybar module text, Walker socket
  protocol, dispatcher behavior and per-window rule effects"* — dispatcher
  behavior is a named unresolved surface.

**No `Holds` cell claims the IPC two-socket contract.** Matches the
registration's "Surface moved" paragraph.

## 3. Do-nothing controls — scratch trees, frozen counter

Trees built (read-only copies of lane bytes; lane untouched — `cmp` verified
identical `SOURCES.md` before mutation, and `corpus/knowledge/` copied
whole, 43 files each):

```text
.ufo/waves/round-32/c1/controls/
├── a-rows-only/    corpus/{SOURCES.md (lane copy + 5 stub rows S186,S187,S188,S189,S196 appended inside ## Registry), knowledge/ (43-file copy)}
└── b-entries-only/ corpus/{SOURCES.md (unmodified lane copy), knowledge/ (43-file copy + 3 stub entries carrying the registered source: lines)}
```

The frozen counter was run verbatim in each root, only the `cd` changed:

```sh
A=corpus/knowledge/ipc-contract-r25.md
B=corpus/knowledge/dispatcher-semantics-r25.md
C=corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
e=0; for f in "$A" "$B" "$C"; do [ -f "$f" ] && e=$((e+1)); done
r=$(grep -cE '^\|[[:space:]]*S(186|187|188|189|196)[[:space:]]*\|' corpus/SOURCES.md)
c=$(grep -cE '^source:.*S(186|187|188|189|196)' "$A" "$B" "$C" 2>/dev/null | awk -F: '{s+=$2} END{print s+0}')
echo "entries=$e rows=$r cited_entries=$c"
```

Baseline (live lane, same command, `cd` = lane root):

```text
BASELINE live-lane: entries=0 rows=0 cited_entries=0
```

### Control (a) — rows only

```text
entries=0 rows=5 cited_entries=0
```

**FAIL** to reach `entries=3 rows=5 cited_entries=3` — missing `entries`
and `cited_entries`. Registry rows alone cannot satisfy the counter.

### Control (b) — entries only

```text
entries=3 rows=0 cited_entries=3
```

**FAIL** to reach `entries=3 rows=5 cited_entries=3` — missing `rows`.
(First run of (b) printed `cited_entries=5` because `grep -c` counts
matching *lines* and the stub carried three `source:` lines; collapsed to
one line `source: S186, S187, S189` for the maximal-miss shape. Note for
adoption: `cited_entries` counts lines, not IDs.) Entries with full citation
lines alone cannot satisfy the counter.

## Conclusion

1. The theme is **not already held**: 0 registry rows for
   S186/S187/S188/S189/S196, 0 of the 3 entry files, no knowledge note holds
   the two-socket contract, no coverage-map row claims it, and the lane's
   own gap ledger names this surface UNKNOWN.
2. A do-nothing (one-sided) commit **cannot reach C1's counter**: rows-only
   yields `entries=0`; entries-only yields `rows=0`. The conjunction
   `entries=3 ∧ rows=5 ∧ cited_entries=3` requires both halves landed.
