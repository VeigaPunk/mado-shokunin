# CustomFailure — nonzero exit and empty-output display conditions in tagged custom.cpp

Seat: `MadoR16.CustomFailure` (scout, leaf). Round 16, 2026-10-20.
Question: open tagged `custom.cpp`; state the display conditions for nonzero exits and empty output.
Scope: source reading only. No build, test, run, compositor, service, package or live probe.
Baseline: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` (not re-measured here).

## Sources opened

Official tag `0.15.0` resolves to commit `90b209add8937514d0a987aa842e701bd8f1232e`
(lightweight tag; commit `chore: 0.15.0`, 2026-02-06T20:15:03Z). Tag bytes and
commit-pinned bytes for `custom.cpp` are identical (`cmp` clean).

| Path @ 0.15.0 / commit | Bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `src/modules/custom.cpp` | 8746 | 292 | `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` |
| `include/util/command.hpp` | 4636 | 179 | `7d876c1bc1889bbd55afdc631c910f36749a936df1ea257d30b71597c4201f5d` |
| `include/modules/custom.hpp` | 1094 | 49 | `c31fa6ae1be35033f4e90d1eda7d0587dc33e94515c5b6b1a3d65478b073b0f8` |
| `include/ALabel.hpp` | 1124 | 36 | `b4a9d76bc9cfc8bfd1917f2ffea54d1a1678af0dc0fcbdf9723f74c295f085db` |
| `src/ALabel.cpp` | 7944 | 225 | `7000f686548fa8572aecef8073ee0e05fd30f851f9b6778e706791280d286a48` |
| `include/AModule.hpp` | 3477 | 84 | `53d19c7ea3391b00b9403288cdbb7ca5f003c8dcdba5065afbf32d4c97b94f31` |
| `src/AModule.cpp` | 9552 | 285 | `57d3a1cd5fe03d11bec68f0b7d9e3e5e3fc03fa7f3a492964e4f60b588fe2650` |
| `man/waybar-custom.5.scd` (cross-check only; S053 owned elsewhere) | 6656 | 250 | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` |

Retrieved with `curl -fsSL` from `raw.githubusercontent.com/Alexays/Waybar/<ref>/<path>`;
`git ls-remote https://github.com/Alexays/Waybar refs/tags/0.15.0` returned only
`90b209a…` (no peeled `^{}` ref). `src/util/command.cpp` does not exist at this tag;
`command.hpp` is the complete header-only implementation.

## Observed: the exact visibility predicate

`src/modules/custom.cpp@0.15.0:162-220`, `Custom::update()`:

- Line 163 comment: `// Hide label if output is empty`.
- Lines 164-166 — guard **A**:
  `(config_["exec"].isString() || config_["exec-if"].isString()) &&
   (output_.out.empty() || output_.exit_code != 0)` → `event_box_.hide()`.
- Lines 168-172 parse only when A is false: `return-type` equal to `"json"` →
  `parseOutputJson()` (257-292), otherwise `parseOutputRaw()` (222-255).
- Lines 174-179 — guard **B**:
  `(config_["hide-empty-text"].asBool() && text_.empty()) || str.empty()`
  → `event_box_.hide()`; `str` is `fmt::format(format_, text, alt, icon, percentage)` (175-177).
- Line 180-207: else `label_.set_markup(str)`, class/tooltip handling, then
  `event_box_.show()` (207).
- Line 219: `ALabel::update()` → `AModule::update()` only runs `on-update`
  (`src/AModule.cpp:93-98`); it never changes visibility. Within this module,
  166/179/207 are the only `event_box_` visibility calls (grep over custom.cpp,
  ALabel.*, AModule.*).

So the module is shown iff **not A and not B**. Two independent hide reasons:
raw command result (A), and post-parse formatted text (B).

## Observed: where `output_.exit_code` and `output_.out` come from

`util::command::res` is `{int exit_code; std::string out;}` (`command.hpp:23-26`).
`output_` (`include/modules/custom.hpp:43`) is assigned at six sites in
`custom.cpp` across the three worker paths:

| Anchor | Writer | Result stored |
|---|---|---|
| `custom.cpp:49-54` (`delayWorker`, exec-if fail) | `execNoRead(exec-if)` | `{WEXITSTATUS(stat), ""}`; `can_update=false`; `dp.emit()` |
| `custom.cpp:56-61` (`delayWorker`) | `exec(exec)` | `{WEXITSTATUS(stat), stdout}` |
| `custom.cpp:121-133` (`waitingWorker`) | same two calls | same |
| `custom.cpp:87-91` (continuous EOF, nonzero) | `close(fp_, pid_)` | `{exit_code, ""}`; error log; hide on next update |
| `custom.cpp:105-114` (continuous line) | `getline` | `{0, line-with-one-trailing-LF-removed}` |
| `command.hpp:127`, `:136` (open/fork failure) | `exec`/`execNoRead` | `{-1, ""}` |

Worker selection (`custom.cpp:21-28`): `signal` set with no `interval`/
`restart-interval` → `waitingWorker`; else `interval_ > 0` → `delayWorker`;
else `exec` is a string → `continuousWorker`. `interval: "once"` becomes
`milliseconds::max()` (`src/ALabel.cpp:24-30`), so it takes `delayWorker` and
effectively runs once. `exec` and exec-if are launched as `/bin/sh -c`
(`command.hpp:115`); `exec` also exports `WAYBAR_OUTPUT_NAME`
(`command.hpp:112-114`), `execNoRead` passes an empty output name.

`command::read` (`command.hpp:28-42`) accumulates all stdout and removes
**exactly one** trailing `\n`; it does not trim spaces, `\r`, or other newlines.
`exec` (`command.hpp:124-131`) returns `WEXITSTATUS(waitpid status)`, not the raw
status. `command::close` (`command.hpp:44-67`) loops until `WIFEXITED` or
`WIFSIGNALED`.

## Findings — nonzero exits

1. **A nonzero exit hides only when `exec` or `exec-if` is a configured string.**
   The exit code is in guard A's OR. A module with neither key (pure static
   `format:`) can never hit A, regardless of any stale `output_`.
2. **A nonzero `exec` exit hides even when stdout is nonempty.** Guard A is
   checked before parsing, so text/format/classes are not applied in that update;
   the widget hides with its previous markup still set internally.
3. **A failing `exec-if` hides and suppresses `exec`.** `execNoRead` stores
   `{nonzero, ""}` and `can_update=false`; the update runs with empty output and
   nonzero status → A. The prior output is overwritten by the empty result, so a
   transient `exec-if` failure blanks the module rather than retaining the last
   good text.
4. **`exec-if` without `exec` is always hidden after the first update.**
   `execNoRead` always returns `out == ""` (command.hpp:138). On success A sees
   `(exec-if is string) && out.empty()` → hide; on failure A also hides. The
   initial `dp.emit()` (`custom.cpp:20`) already runs with an empty `out`, so a
   configuration with `exec-if` and only static `format` never displays, even
   when `exec-if` exits 0 and even if no worker was started. (Static consequence
   of source; not executed.)
5. **Continuous script at EOF, nonzero status → hide.** Lines 81-91 set
   `{exit_code, ""}`, emit, log “stopped unexpectedly, is it endless?”; if
   `restart-interval` is numeric it re-executes after the delay, otherwise the
   thread stops. The first line from the new process sets `{0, line}` and can
   show again.
6. **Signal termination does not count as a nonzero exit here.** `exec` returns
   `WEXITSTATUS(stat)`; for a `WIFSIGNALED` child the high byte is 0, so a
   SIGTERM/SIGKILL-killed script is recorded as exit code 0 (and the
   “stopped unexpectedly” log is not taken in the continuous path). “Nonzero”
   in guard A means nonzero normal exit status, or the synthetic `-1` from
   pipe/fork failure. Signal death with nonempty stdout therefore shows; signal
   death with empty stdout still hides via the separate `out.empty()` arm. For a
   continuous script, a signal-killed child at EOF leaves `output_` unchanged,
   so the last line can persist just as in finding 7. [High confidence from
   POSIX `WEXITSTATUS` macro semantics; static reading, not executed.]
7. **A continuous script that exits 0 at EOF neither hides nor updates.**
   Lines 81-104: when `exit_code == 0`, `output_` is left untouched and no
   `dp.emit()` occurs; only restart/stop handling runs. The last shown line
   therefore persists (or a never-updated module stays in its previous
   visibility) even though the producer has ended. This is the mirror image of
   finding 5 and is easy to state wrongly.

## Findings — empty output

Guard A's “empty” is literal `output_.out.empty()` after `command::read`'s single
trailing-newline strip:

- exec exits 0 with **zero bytes** of stdout → hidden.
- exec stdout is exactly `"\n"` → `read` strips it → empty → hidden.
- exec stdout `"\n\n"` → `read` leaves `"\n"`, so A is false; parsing yields
  `text_ == ""`, then default format `"{}"` produces empty `str` → hidden by B.
  With a static-content format and `hide-empty-text` false, the module shows.
- Whitespace-only output (`" "`) is non-empty → A false; default format shows a
  space.
- Continuous nonzero exit writes `""` explicitly → hidden (finding 5).
- A continuous script line consisting only of `"\n"` is stripped to `""`
  (`custom.cpp:106-112`) → hidden, even though the producer is still running.
- `exec`/`exec-if` pipe or fork failure yields `{-1, ""}` → hidden.
- An empty-string `exec`/`exec-if` is treated as open failure
  (`command.hpp:70` returns nullptr) → `{-1, ""}` → hidden.

Guard B is a different emptiness test and runs only after parsing:

- `hide-empty-text: true` hides when parsed `text_` is empty, even if `format`
  contains static content. `text_` is set from the first raw line
  (`custom.cpp:232-241`) or the JSON `text` field (`custom.cpp:263-267`);
  `output_.out` non-empty does not protect the module when `text_` is empty.
- `str.empty()` hides unconditionally, so `"format": ""`, or a format whose
  substitutions all expand to empty (e.g. `{icon}` with no matching icon),
  hides regardless of text and of `hide-empty-text`.
- Guard B is unreachable on the same update as guard A: when A fires, parsing and
  formatting are skipped.

The `config.isNull()` warning (`custom.cpp:17-19`, “element will be hidden”)
issues no hide call; with the default format `"{}"` and no output the actual
hide comes from guard B's `str.empty()` after parsing empty output. The wording
is descriptive, not a separate mechanism.

## Documented vs source-only (S053 cross-check; not my row)

The tagged man page documents the `exec-if` exit-code-0 gate
(`man/waybar-custom.5.scd:19-22`) and `hide-empty-text` (24-26), but contains no
statement that a nonzero **`exec`** exit hides the module, no statement that
literal empty output hides it, and no statement about a clean continuous exit
leaving the last line displayed. Those behaviors are visible only in
`src/modules/custom.cpp`. A U7 note that generalizes “Waybar hides custom
modules on nonzero exit / empty output” must anchor both halves to S054
(`custom.cpp:164-166`) and keep S053 limited to its actual prose. The man's
`format` default is documented as `{text}` (`:58-61`) while the constructor
passes the literal `"{}"` (`custom.cpp:9`); text-equivalent under automatic fmt
indexing, not byte-identical wording.

## Confidence

| Claim | Confidence |
|---|---|
| Guard A predicate and its inputs (custom.cpp:164-166, 49-61, 87-114, 121-133) | High — direct source |
| `execNoRead` always yields empty `out`; exec-if-only module always hides | High — direct source |
| Single trailing-LF strip; `"\n"` empty, `"\n\n"` nonempty | High — direct source |
| Guard B tests parsed `text_`, not raw output | High — direct source |
| Clean continuous EOF (exit 0) leaves output_/visibility untouched | High — direct source |
| Signal-killed child maps to exit code 0 via WEXITSTATUS | High on macro semantics; not executed |
| `output_.exit_code` indeterminate until first assignment | High for declaration; inference that current guard short-circuit never reads it unset |

## Remaining unknowns and limits

- Static source only. No LSP/clangd server covers the fetched upstream files, so
  symbol tracing here is direct source reading rather than language-server
  semantic proof. `event_box_.hide()`/`show()` is GTK visibility intent, not
  rendered pixels; parent bar, CSS, layer-shell and `show_all` ordering were not
  examined. This is not rendered verification.
- Initial pre-first-update visibility is unmeasured: `AModule::update` does not
  show/hide, but Waybar's bar-level `gtk_widget_show_all` path (`src/bar.cpp`)
  was not opened. Only post-`update()` visibility is described.
- `output_.exit_code` has no default member initializer (`custom.hpp:43`,
  `command.hpp:23-26`); the initial `dp.emit()` (`custom.cpp:20`) can run before
  any worker assignment. Guard A's `out.empty()` short-circuit avoids reading it
  today, but this is inference over all current call paths, not a sanitizer run.
- Signal-death mapping was derived from `WEXITSTATUS` semantics, not executed.
- Only tag 0.15.0 at commit `90b209a` was read; earlier/later tags may differ.
  No signature verification of the tag was performed.
- Adjacent, not exercised here: `parseOutputRaw` re-assigns
  `tooltip_ = validated_line` after the escape branch (`custom.cpp:240`), so
  `escape: true` applies to text but not to the raw first-line tooltip. This
  affects tooltip markup, not the display-text predicate above.

## Tooling / safety

No tools installed or updated. No package or service operations. No live
compositor, input, screenshot or command-producer probes. Network use was limited
to read-only `curl` of official Waybar tag/commit files and the GitHub API commit
metadata. No registry, corpus, SKILL, QUALITY, SCORECARD or LOG file was modified;
only this report was written.
