# Mado round 16 — CustomSource report

Seat: `MadoR16.CustomSource` (scout, leaf; no subagent dispatch). Date: 2026-10-20.
Question: tagged `custom.cpp` — the update path from the producer buffer to the GTK
label, with exact branch anchors. Source reading only; nothing was executed.

## 1. Source identity (verified)

| Item | Value |
|---|---|
| Reserved id | S054 (`code`), Waybar 0.15.0 |
| URL | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp |
| Bytes / SHA-256 | 8746 / `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` |
| Verification | Re-fetched the tagged raw URL on 2026-10-20; `cmp` against `/tmp/waybar-r16/custom.cpp` is byte-identical, digest matches the round draft |
| Anchors | All `custom.cpp:NN` below are 1-based lines of that exact blob |

The scratch copy is `/tmp/waybar-r16/custom.cpp` (outside the lane). No host Waybar
binary, package database or configuration was queried.

### Auxiliary tagged 0.15.0 files (type/cadence resolution only)

These are the same upstream tag but are **not** the reserved S054 row. L1 should not
credit them as separate sources unless it registers them independently.

| Path at tag 0.15.0 | SHA-256 | Used for |
|---|---|---|
| `include/modules/custom.hpp` | `c31fa6ae1be35033f4e90d1eda7d0587dc33e94515c5b6b1a3d65478b073b0f8` | `util::command::res output_`; `std::string alt_` (hides ALabel's bool); `util::JsonParser parser_` |
| `include/ALabel.hpp` | `b4a9d76bc9cfc8bfd1917f2ffea54d1a1678af0dc0fcbdf9723f74c295f085db` | `Gtk::Label label_`; default `interval = 0`, `ellipsize = false`; `format_`; bool `alt_` |
| `src/ALabel.cpp` | `7000f686548fa8572aecef8073ee0e05fd30f851f9b6778e706791280d286a48` | `format_` default; `max-length`/`min-length`; `update()`; `getIcon()`; click toggle |
| `include/AModule.hpp` | `53d19c7ea3391b00b9403288cdbb7ca5f003c8dcdba5065afbf32d4c97b94f31` | `Glib::Dispatcher dp` comment: emitting triggers `update()`; `tooltipEnabled()` |
| `src/AModule.cpp` | `57d3a1cd5fe03d11bec68f0b7d9e3e5e3fc03fa7f3a492964e4f60b588fe2650` | `update()` = `on-update` child only; tooltip default true |
| `include/util/command.hpp` | `7d876c1bc1889bbd55afdc631c910f36749a936df1ea257d30b71597c4201f5d` | `res` fields; `open`/`exec`/`execNoRead`; `/bin/sh -c` |
| `include/util/sleeper_thread.hpp` | `abbabe116dd5d488fb01f75b78549cfb4849a8fdc384cb73a380bdaafcd3897a` | worker function is invoked repeatedly |
| `include/util/json.hpp` | `22a1a3cb6337ddc099d520c453bcaa1cc226a3c814472370d6c73d0c47b5f5fb` | parse throws `std::runtime_error`; `\x`→`\u00` preprocessing |

## 2. Observed update path (buffer → GTK label)

1. **Construction.** `custom.cpp:7-29`. Base `ALabel(config, "custom-"+name, id, "{}")`
   (`:9`) makes `format_` the configured `format` string if present, else `"{}"`
   (`ALabel.cpp:19`). `dp.emit()` at `:20` requests an update before any producer read.
   Mode selection at `:21-28`: signal without interval/restart → `waitingWorker`;
   `interval_ > 0` → `delayWorker`; otherwise an `exec` string → `continuousWorker`.
2. **Producer open.** `custom.cpp:66-72` calls `util::command::open`. That helper
   (`command.hpp:69-122`) forks `/bin/sh -c <cmd>` (`:115`), pipes the child's stdout
   (`:76`, `:109-121`), sets `WAYBAR_OUTPUT_NAME` when non-empty (`:112-114`), sets
   `PR_SET_PDEATHSIG` (`:100`) and its own process group (`:111`). Stdin is not
   redirected, so the child inherits Waybar's stdin; there is no timeout.
3. **One producer line per invocation.** `SleeperThread::operator=` loops
   `while (do_run_) { signal_ = false; func(); }` (`sleeper_thread.hpp:44-50`). Each
   pass of the `continuousWorker` lambda allocates `buff` (`custom.cpp:74`), frees it
   through `ScopeGuard` (`:75-79`), and performs one `getline` (`:80-81`). This is the
   source of "one line per update" for endless scripts; the loop is in the thread
   wrapper, not in `custom.cpp`.
4. **Success branch.** `custom.cpp:105-114`. `std::string output = buff` (`:106`) is a
   C-string copy: bytes after an embedded NUL are dropped even though `getline` read
   them. Only one trailing `'\n'` is removed (`:109-111`); `'\r'` survives. Then
   `output_ = {0, output}` (`:112`) and `dp.emit()` (`:113`).
5. **End/error branch.** `custom.cpp:81-104`. `getline == -1`: `exit_code` starts at 1;
   if `fp_` is open, `exit_code = WEXITSTATUS(util::command::close(fp_, pid_))` (`:84`).
   Non-zero: `output_ = {exit_code, ""}`, `dp.emit()`, error log (`:87-90`). Numeric
   `restart-interval`: sleep `max(1 ms, s*1000)` and reopen (`:92-100`); otherwise
   `thread_.stop(); return;` (`:101-104`). A clean EOF (exit 0) **does not assign
   `output_` and does not emit**; with `restart-interval` it still reopens, without it
   the worker stops.
6. **Timed producers.** `delayWorker` `custom.cpp:39-64`; `waitingWorker` `:118-136`.
   `exec-if` runs through `execNoRead` (`:50`, `:122`), which discards stdout and
   returns `{-1, ""}` on open failure or `{WEXITSTATUS(stat), ""}` otherwise
   (`command.hpp:133-139`). Non-zero suppresses the `exec`
   call and emits (`:51-54`, `:123-126`). Otherwise `exec` runs through
   `util::command::exec` (`:58`, `:130`), which reads the whole stdout via
   `command::read` 128-byte chunks and strips one trailing newline
   (`command.hpp:28-42`, `:124-131`). Sleep is `sleep_for(interval_)` (`:62`) or
   `sleep()` (`:134`). Wake paths: matching `SIGRTMIN+signal` (`:138-142`); scroll and
   toggle (`:150-160`) through `handleEvent` (`:144-148`).
7. **Cross-thread handoff.** `dp.emit()` is the only handoff; `AModule.hpp:23-24`
   documents that emitting triggers `update()`. `custom.cpp` contains no lock or copy
   around `output_` (plain member in `custom.hpp`), so a concurrent read/write is not
   excluded by this source. Dispatcher ordering/coalescing is not established here
   [INFERENCE].
8. **`update()`.** `custom.cpp:162-219`: hide gate `:164-166`; raw/JSON select `:168-172`;
   `fmt::format` `:175-177`; hide gate `:178-179`; `label_.set_markup(str)` `:181`;
   tooltip setters `:182-194`; style-class churn `:195-206`; `event_box_.show()` `:207`;
   `fmt` error handling `:209-216`; `ALabel::update()` `:219`.
9. **Raw parser.** `custom.cpp:222-255`: per-line Glib UTF-8 validation/fix `:227-230`;
   line 0 = text (and tooltip) `:232-241`; line 1 = tooltip `:242-247`; line 2 = class
   `:248-249`; more lines break `:250-251`.
10. **JSON parser.** `custom.cpp:257-292`: class clear `:260`; per-line parse `:262`;
    `text` `:263-267`; `alt` `:268-272`; `tooltip` `:273-277`; class string/array
    `:278-284`; percentage `:285-289`; unconditional `break` `:290`.
11. **Terminal in-file assignment.** `label_.set_markup(str)` at `custom.cpp:181` is
    the only label-text setter in the file; `grep` confirms no `set_text` and no other
    `set_markup`. Tooltip setters `:188/190/192` are separate.

## 3. Exact branch anchors

### Producer / buffer

| Anchor | Condition | Effect |
|---|---|---|
| `custom.cpp:21-28` | signal without interval/restart; else `interval_ > 0`; else `exec` string | chooses `waitingWorker` / `delayWorker` / `continuousWorker`; none if no match |
| `custom.cpp:81` | `getline(&buff,&len,fp_) == -1` | EOF/error path; otherwise success path |
| `custom.cpp:83-86` | `fp_` non-null | `close(fp_,pid_)`, `fp_=nullptr`; raw wait status returned |
| `custom.cpp:87-91` | `exit_code != 0` | `output_={exit_code,""}`, `dp.emit()`, module-name-only error log |
| `custom.cpp:92-100` | `restart-interval` numeric | sleep then reopen; `pid_=-1` first |
| `custom.cpp:101-104` | no numeric restart | `thread_.stop(); return;` |
| `custom.cpp:105-113` | `getline != -1` | C-string copy, one `\n` strip, `output_={0,output}`, emit |
| `custom.cpp:109-111` | last char is `\n` | erase exactly one trailing newline; `\r` retained |
| `custom.cpp:49-55`, `:121-127` | `exec-if` is a string | run it; non-zero → `can_update=false` + emit |
| `custom.cpp:56-61`, `:128-133` | `exec` is a string and `can_update` | full-output read into `output_`, then emit |

### Renderer / label

| Anchor | Condition | Effect |
|---|---|---|
| `custom.cpp:164-166` | (`exec` or `exec-if` configured) **and** (`output_.out.empty()` or `exit_code != 0`) | `event_box_.hide()`; no parse, no `set_markup` |
| `custom.cpp:168-172` | `return-type` exactly `"json"` | `parseOutputJson()`; any other value → `parseOutputRaw()` |
| `custom.cpp:175-177` | always in the else branch | `str = fmt(format_, text_, alt_, icon(percentage_,alt_), percentage_)` |
| `custom.cpp:178-179` | (`hide-empty-text` && `text_` empty) or `str` empty | hide; no `set_markup` |
| `custom.cpp:181` | both gates pass | **`label_.set_markup(str)`** — the GTK handoff point |
| `custom.cpp:182-194` | `tooltipEnabled()` | tooltip markup only: `tooltip-format` → `str` when `text_==tooltip_` → `tooltip_` |
| `custom.cpp:195-207` | non-hidden branch | remove all label classes except `id_`; add `class_`, `flat`, `text-button`, `module`; show box |
| `custom.cpp:209-216` | caught `fmt::format_error` | only the manual/automatic-indexing error is rewritten; other format errors propagate |
| `custom.cpp:219` | every call, hidden or not | `ALabel::update()` → `AModule::update()` → only runs `on-update` (`AModule.cpp:93-98`); never sets text or re-shows |
| `custom.cpp:227-230` | per raw line | invalid UTF-8 replaced via `validate()`/`make_valid()` |
| `custom.cpp:232-241` | `i == 0` | escape-dependent `text_`; **`:240` unconditionally overwrites `tooltip_` with the unescaped line**; `class_.clear()` only here |
| `custom.cpp:242-247` | `i == 1` | tooltip from second line (escape respected) |
| `custom.cpp:248-251` | `i >= 2` | `i==2` pushes one class; `i>2` breaks |
| `custom.cpp:260` | JSON parse start | `class_.clear()` unconditionally |
| `custom.cpp:262` | per line | `JsonParser::parse`; invalid JSON throws `std::runtime_error` (`json.hpp:36-37`) |
| `custom.cpp:263-277` | per JSON line | text/alt/tooltip; escape applied when configured |
| `custom.cpp:278-284` | `class` string or array | one or many classes; array elements coerced by `asString()` |
| `custom.cpp:285-289` | percentage numeric and `asString()` non-empty | `lround(asFloat)`; otherwise 0 |
| `custom.cpp:290` | after first JSON line | unconditional `break`: only one JSON document is consumed |

## 4. The observation boundary U7 may claim

- **Last in-tag artifact:** the string `str` passed to `label_.set_markup` at
  `custom.cpp:181`. Everything after that — Pango markup parsing, glyph shaping, font,
  CSS, ellipsization, compositor paint, screenshot/OCR — is outside both tagged files.
  A source-level statement can assert "this markup string was assigned", not "this text
  was rendered".
- **`str` is not producer stdout.** It is `fmt::format(format_, text_, alt_, icon,
  percentage)` (`:175-177`). `format_` is the user's format or the code default `"{}"`
  (`custom.cpp:9`, `ALabel.cpp:19`); the man documents `{text}` as the default
  (man line 60). A
  static-only config (man DESCRIPTION line 8) can display text with no producer at all,
  and a format may omit `{text}`. Producer bytes are not recoverable from `str`.
- **Markup vs characters.** With `escape` false (man line 127; `custom.cpp:233-239`,
  `:263-272`) command output enters `str` unescaped, so Pango metacharacters in stdout
  are markup, and the displayed characters can differ from `text_`. With escape true,
  `text_` is escaped, but raw-mode line 0 still overwrites `tooltip_` unescaped at
  `:240` (tooltip facet owned by `CustomTooltip`).
- **Raw vs JSON asymmetry.** Raw mode repairs invalid UTF-8 (`:227-230`); JSON mode does
  not. Invalid JSON throws (`json.hpp:36-37`), and `update()` catches only
  `fmt::format_error` (`:209-216`), so the exception leaves `update()` without a label
  assignment. What the GLib dispatcher does with it is [UNK].
- **Hidden does not mean empty.** The hide branches (`:166`, `:179`) only hide the event
  box; they never clear `label_`. The last `set_markup` string persists in the widget.
  `ALabel::update()` (`ALabel.cpp:130` → `AModule.cpp:93-98`) does not change text or
  visibility.
- **One line per update is structural in continuous mode.** `parseOutputRaw` always
  starts at `i==0`, so each endless-script line becomes both `text_` and `tooltip_` and
  clears `class_`; second/third lines only exist for whole-output timed producers.
  JSON mode consumes exactly one line (`:290`); a multi-line/pretty JSON document will
  fail on its first line unless that line alone is valid JSON.
- **Only one raw class line, none in continuous mode.** The class push is at `:249`
  (`i==2`), unreachable when each update supplies a single line.
- **Rendering knobs are configured, not observed.** `ALabel` may set
  `max-length` → `ELLIPSIZE_END` + single-line (`ALabel.cpp:38-45`), `min-length`
  width (`:47-49`), rotate (`:51-58`), alignment (`:60-67`) and justify (`:118-127`).
  Any of these can make displayed text diverge from `str`; actual output is unmeasured.
- **Interaction can change the format.** `Custom::handleToggle` (`:156-160`) calls
  `ALabel::handleToggle` (`ALabel.cpp:180-190`), which, when `format-alt-click`
  matches the clicked button, swaps `format_` to `format-alt` if configured,
  otherwise back to `default_format_`. Custom's `alt_` is a separate `std::string`
  (`custom.hpp`) that hides ALabel's bool `alt_`; that toggle does not change the
  string. A future `str` therefore depends on click history.

## 5. Corrections/additions for the current U7 candidate note

Not edits to `.ufo/waves/round-16/waybar-draft.txt`; input for `WaybarDraft`/L1.

- **Resolve the `[UNK]` "util::command helpers".** `open` runs `/bin/sh -c`
  (`command.hpp:115`), not a direct script path; `exec` reads the entire stdout and
  strips one trailing newline (`:28-42`, `:124-131`); `execNoRead` discards stdout and
  returns `""` (`:133-139`); no timeout, stdin inherited, `WAYBAR_OUTPUT_NAME` set.
- **Resolve the `[UNK]` "ALabel interval once/tooltipEnabled/getIcon".**
  `interval: "once"` → `milliseconds::max()` (`ALabel.cpp:24-30`); Custom's
  `interval_.count() > 0` then selects `delayWorker`, which runs once and sleeps for
  that maximum (signal wake can re-run). `tooltipEnabled()` is `config.tooltip`, default
  true (`AModule.cpp:17`, `:280`; man line 117). `getIcon` looks up `format-icons`
  by `alt` then percentage and returns `""` when absent (`ALabel.cpp:132-152`).
- **Resolve "continuous one getline per update" as observed, not inference:**
  `sleeper_thread.hpp:44-50` re-invokes the lambda; `custom.cpp:74-81` reads one line
  per pass.
- **Add: default format is `"{}"` in code, `{text}` in the man.** Both bind the first
  `fmt` argument (`text_`); config `format` overrides. [INFERENCE on fmt named-argument
  positional binding; not executed.]
- **Add: signal-killed producer is not reliably non-zero.**
  `custom.cpp:84` and `command.hpp:130` call `WEXITSTATUS` on the raw wait status with
  no `WIFEXITED` guard. On Linux/glibc a signal-killed child evaluates to 0, i.e. looks
  "clean"; the actual restart/hide consequence belongs to `CustomFailure`.
- **Add: `return-type` is case-sensitive `"json"`** (`:168`); an invalid option falls to
  raw (`:171`), matching the man.
- **Add: `on-update` runs on every update**, including hidden ones, via
  `AModule::update` (`AModule.cpp:93-98`). This is an action boundary, not rendering:
  the update path can fork a user command without changing the label.
- **Add: empty-output semantics.** With `exec`/`exec-if` configured, empty stdout hides
  unconditionally at `:165`; `hide-empty-text` only decides the static-format case at
  `:178`. `execNoRead` returning `{0,""}` therefore hides an `exec-if`-only module on
  success [INFERENCE from `command.hpp:133-139` + `:165`].
- **Precision on the escape bug:** the overwrite is a literal statement
  `tooltip_ = validated_line;` at `:240`; `text_` remains escaped. Only the first-line
  tooltip is affected.
- **JSON preprocessing:** `JsonParser::parse` replaces every literal `\x` with `\u00`
  before parsing (`json.hpp:39-42`), so a producer text containing backslash-x is
  altered. Not visible in the draft.

## 6. Confidence and remaining unknowns

**Observed (line-anchored):** every branch, assignment and call path in `custom.cpp`
above; auxiliary helper semantics from the same tag; sole label-text setter at `:181`;
`ALabel::update` behavior; `format_` default; `on-update` execution.

**Inference:** `"{}"` binds `text_` as the first fmt argument; worker/caller thread
roles and dispatcher coalescing; signal-death `WEXITSTATUS` value on this platform;
empty-`exec-if`-only hide behavior.

**Unmeasured / unknown:** host Waybar version and config; whether the installed binary
matches tag 0.15.0; GTK/Pango handling of invalid or partial markup; actual glyphs,
ellipsis, CSS, font, alignment and pixels; Glib dispatcher behavior when `update()`
throws; jsoncpp `asString()` behavior for non-string fields in the installed version;
`Glib::ustring` handling of invalid UTF-8 arriving from JSON mode; accessibility/AT-SPI
text of a hidden label; `output_` data-race consequences.

Cross-seat boundaries: tooltip/class/percentage and escaping → `CustomTooltip`;
non-zero exits and empty-output display → `CustomFailure`; man scheduling options →
`CustomExec`/`CustomMan`. This report does not restate their conclusions.

## 7. Tooling and compliance

- Installed/updated nothing; no pacman, service, compositor, input, screenshot,
  Waybar launch or producer command was run. Only read-only HTTPS GETs of the tagged
  raw files, plus `sha256sum`, `cmp`, `nl`, `grep`, `sed`, `find`, `ls`, and a
  read-only Python parse of `spec.json`/`dispatch.json`.
- No `agent.db*`, credential or auth file was opened, copied or modified. No separate
  omp CLI process was launched. `/home/vgpnk/.omp/agent/RULES.md` was read; no install
  was needed or attempted.
- Paths: this report is
  `.ufo/waves/round-16/w1/reports/CustomSource.md`; scratch sources are under
  `/tmp/waybar-r16/` and are not lane artifacts.
