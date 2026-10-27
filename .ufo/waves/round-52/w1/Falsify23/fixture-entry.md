# Dispatcher execution, second pass: the press-time table, the translator refusal, and the request path

This note records what the pinned Hyprland 0.56.2 source says about the three points where a
dispatcher name is turned into a call: the key-press path, the legacy translator's entry, and the
control-socket request. It does not press a key, does not issue a socket request and does not
observe the running compositor. Every statement below is a reading of the pinned bytes, and each
one is mapped to the row, pin and quote that carries it.

Four propositions are admitted. They are ordered as a press would meet them.

1. A press that matched a bind resolves the handler name it stored through the keybind manager's
   dispatcher table and invokes the mapped closure with the stored argument. The table is a
   string-keyed map of callables, so the lookup is a name comparison and nothing else. The lookup
   expression is in the press loop and reads the stored handler, with the mouse form substituted
   for a mouse bind: `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`
   (Hyprland-KeybindManager.cpp:785). A miss at this point only logs, because the name was already
   checked when the configuration line was read.

2. The legacy translator owns the second lookup and refuses an unknown name before any
   implementation is called. Its `run` entry tests membership in the implementation map and
   returns an error result instead of selecting a function: `Bad dispatcher`
   (Hyprland-legacy-DispatcherTranslator.cpp:32). This refusal is reached only by a caller that
   names the translator directly; a bind cannot reach it, since the parse-time check used the same
   table.

3. The control socket reaches the same dispatcher table through a different front door. The request
   text is cut at its first space, the head becomes the name and the tail becomes the argument, and
   the head is resolved in the press path's map:
   `m_dispatchers.find(DISPATCHSTR)` (Hyprland-HyprCtl.cpp:1149). Because the socket path performs
   no press-state write, a dispatcher that reads that field sees the value the thread defaults to.

4. A named submap switch is accepted only when some bind already carries that name. The setter
   scans the bind list for a bind with the requested submap before assigning the current-submap
   string; when the scan finds nothing the call reports failure and keeps the previous value:
   `Cannot set submap` (Hyprland-ConfigActions.cpp:1681). The reset and empty forms take the
   assignment without that scan.

These four points are the whole of what this entry claims. The surrounding machinery - how a
keysym is matched, how the modifier mask is compared, how a bind line is split - was settled in
earlier lane entries and is not restated here. This entry's purpose is to keep the execution-side
facts in one place and to bind each of them to the line that shows it.

## Propositions

| proposition | row | pin | quote | rationale |
|---|---|---|---|---|
| A press resolves the stored handler through the dispatcher table and calls the mapped closure | S380 | Hyprland-KeybindManager.cpp | `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);` | the lookup and the call in the press loop are the same statement |
| The translator refuses an unknown dispatcher name before calling an implementation | S381 | Hyprland-legacy-DispatcherTranslator.cpp | `Bad dispatcher` | the membership test and its error return precede the call |
| A socket request is cut at its first space and resolved in the same dispatcher table | S382 | Hyprland-HyprCtl.cpp | `m_dispatchers.find(DISPATCHSTR)` | the split is written above the lookup on the same path |
| A named submap switch fails when no bind carries that submap | S383 | Hyprland-ConfigActions.cpp | `Cannot set submap` | the failure text is the branch taken after the scan finds no bind |

## Source rows

source: S380 - Hyprland 0.56.2 press-time dispatcher lookup - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp - code - the find in the press loop and the call that follows it - `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`(Hyprland-KeybindManager.cpp:785)
source: S381 - Hyprland 0.56.2 legacy translator refusal - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp - code - the membership test that rejects a name before any implementation runs - `Bad dispatcher`(Hyprland-legacy-DispatcherTranslator.cpp:32)
source: S382 - Hyprland 0.56.2 hyprctl dispatch request path - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp - code - the first-space split, the lookup in the dispatcher map and the reply - `m_dispatchers.find(DISPATCHSTR)`(Hyprland-HyprCtl.cpp:1149)
source: S383 - Hyprland 0.56.2 submap action failure branch - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp - code - the named-submap scan and the error it produces - `Cannot set submap`(Hyprland-ConfigActions.cpp:1681)

## Pin manifest

All paths relative to `.ufo/waves/round-52/fetch/`; Hyprland pins at commit
`efb50993780079460b0cbed1363e2166a2de1d9f`.

| pin | file | row |
|---|---|---|
| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | S380 |
| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/DispatcherTranslator.cpp | S381 |
| Hyprland-HyprCtl.cpp | src/debug/HyprCtl.cpp | S382 |
| Hyprland-ConfigActions.cpp | src/config/shared/actions/ConfigActions.cpp | S383 |

## Held ground

The bind-line field shape, the comma rule and the parse-time validation are reused from earlier
entries and not re-argued here.

held: corpus/knowledge/bind-table-r25.md:38 keys=DISPATCHER,ARG,numbArgs
held: corpus/knowledge/bind-table-r25.md:52 keys=dispatcher
held: corpus/knowledge/keybind-rule-semantics.md:73 keys=params,comma-separated

## Limits

No key was pressed and no request was sent. The four propositions are readings of the pinned
bytes; they are not observations of the running compositor, and the effect of a dispatcher on the
desktop is out of scope. Dispatchers outside these four lines were counted in earlier entries, not
re-read here.
