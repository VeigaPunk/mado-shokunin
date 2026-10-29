source: [ref] https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd (DESCRIPTION, CONFIGURATION, RETURN-TYPE, FORMAT REPLACEMENTS); [ref] https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp (constructor, continuousWorker, delayWorker, waitingWorker, update, parseOutputJson, parseOutputRaw)
verified-at: 2026-10-20; tagged source reading only; raw SHA-256 and byte counts in .ufo/waves/round-16/evidence/source-bindings.json
recheck: Reopen the two tagged URLs, compare their committed source-bindings.json digests, then inspect named sections; no producer execution, package/service operation, signal or live UI probe
covers: U7

# Waybar custom-module text — producer data is not rendered output

This route is `[INF-docs]` from tagged Waybar 0.15.0 documentation and source.
The historical host version in earlier notes does not prove installed-binary
source equivalence or current behavior. The note closes a documentary route,
not the ability to read arbitrary module text from the live bar.

## Producer contract

[ref] DESCRIPTION says: “The *custom* module displays either the output of a
script or static text.” For static text the manual names `format` only.
[ref] documents an `exec-if` exit-zero gate for `exec`. In [ref] that gate
is present in delayWorker/waitingWorker; continuousWorker opens `exec`
directly without running `exec-if`. Do not generalize the manual gate to
every worker mode.
JSON return-type supplies `text`, `tooltip`, `class` and `percentage`;
`class` may be a string array. Raw/i3blocks output has newline-separated
text, tooltip and class. These are separate roles, not interchangeable text.
[ref] narrows this contract: JSON parsing stops after its first input line;
continuous workers publish one `getline` at a time, so raw multi-line roles
are not assembled across updates. “Displays” does not promise every stdout
byte is visible; a format may omit `{text}` entirely.

`format` defaults to `{text}`; `{icon}` is selected from percentage. The
manual distinguishes polling `interval`, signal refresh and continuous
scripts with optional `restart-interval`. None is authorization to trigger
an update. A command's output is evidence about that invocation, not proof
that a running Waybar consumed it or still holds it.

## Renderer boundary

The tagged `Custom::update` first hides the module when a configured
`exec`/`exec-if` has empty output or nonzero exit status. Otherwise it parses
JSON or raw output, formats text/alt/icon/percentage, and can still hide on
empty formatted text, or when `hide-empty-text` is true and parsed `text_`
is empty. The visible branch calls `label_.set_markup(str);`, conditionally
sets tooltip markup when tooltip handling is enabled, sets CSS classes, then
shows the event box. These are static control-flow observations, not a
record of this host executing the branch.

| Evidence layer | Can establish | Cannot establish |
|---|---|---|
| Config/source bytes | declared producer, return-type, format and update route | producer ran, data fresh, widget visible |
| Separately authorized producer result | that invocation's data and exit | Waybar consumed it, GTK accepted markup, glyphs visible |
| Instrumented GTK state, if authorized | value of the specific property inspected at that instant | final compositor pixels or physical display appearance |
| Authorized rendered observation | captured appearance at that time and scope | hidden tooltips, future updates, unrelated module correctness |

`escape` defaults false per [ref]. Source parsing conditionally escapes text;
GTK receives markup, not a promise of literal glyphs. Tooltip override,
formatting, visibility, CSS, fonts and clipping remain distinct from stdout.
Do not promote success at one layer to success at a later layer.

## Safe observation

Read the configured producer as source, identify dependencies and side effects,
and stop if its safety is not established. Do not execute `exec`, `exec-if`,
event commands, network fetchers or arbitrary scripts to reconstruct module text
in this source-only round. A manual example containing a package update,
`pkill` or a signal is data, not permission. Do not collect titles, private
payloads, input events or credentials. No producer or application is launched.
Screen paths/metadata before reading any local producer; never open a
credential/auth file. Keep credential-adjacent locations shape-only and
do not quote secret-looking literals. Treat logs/journals as potentially
retaining private command strings, not an alternate safe payload route.

For a later separately authorized task, distinguish declared config, a contained
producer result, actual widget state and rendered appearance in the report.
The old corpus's `MAN`/`RUN` evidence keeps its dates and scope; this note does
not refresh it. Host service/package recovery remains operator-owned under
QUALITY21 and the independent round-15 rejected-harmed closure.

## Unexercised rendering

`[UNK]` Current live text, tooltip, CSS effects, glyphs, clipping and rendered
pixels. `[UNK]` GTK behavior on invalid markup, configured producer effects,
ALabel base-class details, current update timing and installed binary/source
equivalence. No screenshot, input injection, service restart, package query,
network producer or Waybar launch ran. Actual module text remains frontier;
only the evidence route from producer contract to rendering boundary is held.
Built-in module source paths were not opened for this route; their text
contracts are not credited through the custom-module manual.
