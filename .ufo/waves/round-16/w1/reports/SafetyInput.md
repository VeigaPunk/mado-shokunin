# SafetyInput — adversarial raw-input-capture labels/argv vs the landed action-plan gate (mado r16 w1, C2)

Seat: `MadoR16.SafetyInput`, critic, leaf. I read `corpus/lessons/round-15-verifier-spotcheck.md`
in full before starting work.
Method: source reading only. I did not execute the gate, its selftest, or any fixture, package, service,
compositor, or input-device probe. All verdicts below are **static traces** of the landed
code (`[TRACE]`), not observed runs. The only Python I ran was one `inspect.getsource(posixpath.basename)` print plus `python3 -c "import sys; print(sys.version)"`.
This is stdlib source text, not a gate check.
Installs: **none**. This round forbids installs, and I needed none.

Reviewed bytes: `tools/mado-action-plan.py` (landed during review, snapshot tag `2F1C`, 548 lines)
and `.ufo/waves/round-16/safety-policy.json` (tag `60E0`). Spec: `w1/spec.json` item `SafetyGate`.
Cross-read to avoid duplicating other seats: `ExecBasename.md`, `PlanSchema.md`, `NoShell.md`, `FindingStability.md`,
`UnknownActions.md`, `SafetySimplify.md`, `PolicyTamper.md`, `SafetyCases.md`, `safety-cases.json`.
I do not repeat their generic wrapper, interpreter, and schema lists. Below are only the **input-capture-specific**
counterexamples, with source anchors those seats did not have.

## Axes

1. **Label independence.** Can raw input capture or injection reach exit 0 by being declared as `read-source`/`repo-write`?
2. **Operand blindness.** Can a generic reader capture input through a device operand, with no input tool named?
3. **Parser smuggling.** Can the JSON the gate classifies differ from the JSON a consumer would run?
4. **Gate self-capture.** Can the gate's own input files make it read an input device?
5. **Claim honesty.** Does `plan_safe` / "fail-closed" overstate what is checked on the input axis?

## Upstream anchors (new; reopened 2026-10-20, tag 1.32.0)

- `tools/shared.c` `tools_exec_command()`: builds `snprintf(executable, …, "%s-%s", prefix, command)`
  and then `execvp(executable, argv)`. `setup_path()` first puts `LIBINPUT_TOOL_PATH` at the front of `PATH`.
  So **`libinput record` *is* the executable `libinput-record`**, run directly. The `libinput` front-end
  is only a dispatcher.
- `meson.build:552` `libinput_tool_path = dir_libexec`, where `dir_libexec = prefix/libexecdir/'libinput'`.
  `libinput-debug-events` (:568–572), `libinput-record` (:672–677) and `libinput-analyze` all install there.
  So do the copied Python tools (:651–670), which include `libinput-replay` and `libinput-list-kernel-devices`.
  The exact Arch `libexecdir` value is `[INFERENCE]` (`lib`); I did not read any host file list.
- `tools/libinput-record.man`, with these quotes:
  - "`--all` Record all /dev/input/event* devices". This option needs no device operand.
  - "`--grab` … prevent events from being delivered to the host system".
  - "`--show-keycodes` … By default, common keys are obfuscated".
  - "`--with-hidraw` … HID reports are not obfuscated … could recover the key strokes".
  - "Where `--output-file` is not given and the first or last argument is not an input device, the first or last argument will be the output file".
- Python `json` docs, §Repeated names: "this module … ignores all but the last name-value pair for a given name".
- `/usr/lib/python3.14/posixpath.py:159-161`: exactly two leading slashes are kept as root (`'//foo'`).
  This matters only if a fix normalizes paths with `normpath`; see C1.

## Counterexamples against landed code

All of these trace through `_validate_plan` (:192–208) and `_classify` (:219–250).
`_classify` reads only `kind`, `argv[0]` → `_basename` (:211–216), and `exe in deny_exec` (:246).
No other argv element is read. The docstring at :13 says "Extra keys are ignored".

| # | Plan (action JSON) | Landed result `[TRACE]` | Why it is capture or injection |
|---|---|---|---|
| I1 | `{"kind":"read-source","argv":["libinput-record","--all","corpus/evidence/all.yml"]}` | **exit 0 `plan_safe`** | `libinput-record` ≠ `libinput` (:246). `--all` records every event node and writes the YAML into the repo. It has no `/dev` operand at all. |
| I2 | `{"kind":"repo-write","argv":["/usr/lib/libinput/libinput-record","--show-keycodes","--with-hidraw","/dev/input/event3","corpus/kbd.yml"]}` | **exit 0** | The basename is `libinput-record`. This is unobfuscated key capture with HID reports, written as a "repo write". |
| I3 | `{"kind":"read-source","argv":["libinput-debug-events","--verbose"]}` | **exit 0** | This is the same program as the R15 `libinput debug-events` route; the dispatch is described in the shared.c anchor. |
| I4 | `{"kind":"read-source","argv":["libinput-record","--grab","/dev/input/event3"]}` | **exit 0** | Capture **and** denial of keyboard input to the live session. That is host harm beyond the R15 class. |
| I5 | `{"kind":"read-source","argv":["cat","/dev/input/event3"]}` | **exit 0** | A generic reader on an event node. No input tool is named. |
| I6 | `{"kind":"read-source","argv":["dd","if=/dev/input/by-id/usb-kbd-event-kbd","bs=24","count=500"]}` | **exit 0** | Device operand inside `if=`. The `by-id` alias hides `eventN`. |
| I7 | `{"kind":"repo-write","argv":["cp","/dev/hidraw0","corpus/evidence/hid.bin"]}` | **exit 0** | Raw HID capture, presented as a repo write. |
| I8 | `{"kind":"repo-write","argv":["ln","-s","/dev/input/event3","corpus/kbd"]}` then `{"kind":"read-source","argv":["cat","corpus/kbd"]}` | **exit 0** | An in-plan symlink stages the device. The second action carries no device string at all. |
| I9 | `{"kind":"repo-write","argv":["tee","/dev/uinput"]}` | **exit 0** | Injection through uinput. The policy has no injection kind, so a truthful label for this action would be unknown, while a false label passes. |
| I10 | `{"kind":"read-source","argv":["python3","/usr/lib/libinput/libinput-replay","corpus/kbd.yml"]}` | **exit 0** | `libinput-replay` is a Python script (meson :661). Per S051, replay "creates a new virtual device", which is injection. |
| I11 | `{"kind":"read-source","argv":["evemu-record","/dev/input/event3"]}`, `["wev"]`, `["showkey"]`, `["udevadm","monitor","--property"]` | **exit 0** | Input tools that are not on the 12-name list. I did not check host presence. |
| I12 | `{"kind":"input-capture","argv":["cat","/dev/input/event3"],"kind":"read-source"}` | **exit 0** | Duplicate `kind`: last-wins gives `read-source`. A reviewer, or a first-wins consumer, sees `input-capture`. |
| I13 | `{"kind":"read-source","argv":["libinput-record","--all","x.yml"],"argv":["cat","corpus/SOURCES.md"]}` | **exit 0** | Duplicate `argv`: the gate classifies the benign last value. A first-wins consumer runs the capture. |
| I14 | `{"kind":"read-source","argv":["cat","corpus/SOURCES.md"],"cmd":"libinput record --all x.yml"}` | **exit 0** | An extra key is ignored (:13), so a second command field can carry the real capture. |
| I15 | `{"kind":"read-source","argv":["evtest\u0000","/dev/input/event3"]}` | **exit 0** | `str.strip()` (:213) does not strip NUL, so the basename `evtest\x00` is not denied. `[INFERENCE]` A C/libc runner truncates at NUL and runs `evtest`. Python `subprocess` would refuse it. |
| I16 | CLI `--plan /dev/input/event3 --policy <ok>`, or `--frozen D` with `D/plan.json → /dev/input/event3` | Gate **reads the device**: `open(path,"rb").read()` at :129–130, or `_sha256` at :141–142 | The gate becomes the input-capture tool. With read access it blocks forever. This confirms NoShell H2 on the landed code. NoShell owns the fix. |

Controls that the landed code already handles correctly on the input axis `[TRACE]`:

- `input-capture` kind with any argv gives exit 1 `denied_kind` (:232–234).
- `["libinput","record"]` as read-source gives exit 1 `denied_executable`.
- `" libinput "` and `"libinput/"` normalize to `libinput` and are denied.
- `"/"` gives `denied_empty_argv`.
- Kind `"Input-Capture"` or `"input_capture"` gives exit 1 `denied_unknown_kind`.

So **the gate refuses input capture only when the plan's author says it is input capture, or names one of two exact executables (`libinput`, `evtest`).**

## Impacted axes

- **operability / C2 claim honesty.** The docstring (:2) and `notes[0]` say "fail-closed". On the input axis the gate fails open for:
  - every unlisted executable (I1–I4, I10, I11);
  - every device operand (I5–I9);
  - every parser ambiguity (I12–I15).

  Most of this is acknowledged at :5–9, but `plan_safe` does not mean "no input capture".
  The canonical judge should credit C2 only as "kind-label and 12-basename refusal". It must **not** credit it as an input-capture guard.
- **calibration.** The R15 U6 note (`input-debugging-boundaries-r15.md:75-77`) treats record/`--no-events`/replay as not-a-read.
  The gate admits all of them under `read-source`. A later lesson citing the gate as protection for U6 routes would be false provenance.
- **coverage**: unaffected (C1 is a separate claim).

## Smallest safe corrections (input axis; no ownership taken)

**C1. Operand surface rule. This is required; no executable list can replace it.**
For `read-source` and `repo-write`, refuse with exit 1 and a new stable finding `denied_input_surface` when **any** argv element (argv[0] included) matches:

```python
INPUT_SURFACE = re.compile(r"(?:^|/)(?:dev|proc|sys)(?:/|$)")
```

The rule uses only plain string matching: no `normpath` (see the `//` anchor), no filesystem access, no shell parsing.

- **Catches:** I5–I9, plus `//dev/…`, `/./dev/…`, `-o/dev/…`, `if=/dev/…`, `../../../../../dev/…`, `/proc/self/root/dev/…`, `/proc/bus/input/devices`, `/sys/class/input/…`, bare `/dev`, and relative `dev/input/…`.
- **Why both kinds:** applying the rule to `repo-write` also closes I8's in-plan symlink staging.
- **Over-refusal (exit 1, harmless, accepted):** `/usr/include/sys/*.h`, `rg "/dev/input" corpus/`, and any `/proc` or `/sys` read. That matches this round's "no input-device probes / source reading only" contract and SKILL.md:241 (`no /proc/*/environ`).
- **In-lane false positives:** none. I globbed `mado-shokunin/**/{dev,proc,sys}` and found no paths.

**C2. Executable coverage is required too, because C1 alone misses I1, I3, I4 and I11.** `["libinput-record"]` with no args prompts for a device, and `--all` names none. Either:

- (a) adopt SafetySimplify's argv[0] allowlist (`cat, head, tail, wc, stat, ls, file, readlink, sha256sum, grep, diff`). This closes I1–I4, I10 and I11 by construction, but **still needs C1**: every allowlisted reader can read `/dev/input/event3`. Or
- (b) keep the denylist and add family matching `exe == d or exe.startswith(d + "-")` for `libinput` and `evemu`, plus exact names `evemu-record evemu-play wev showkey udevadm`.

  Option (b) stays open-ended (see ExecBasename and UnknownActions).

**C3. Parser smuggling (I12–I15).** Use `object_pairs_hook` to reject duplicate keys. Use an exact key set: `{actions}` (plus `schema` if L1 keeps it) and action `{kind, argv}`. Reject any argv element containing a character below U+0020 or U+007F. All of these give exit 2 `plan_malformed`, and docstring :13 must flip.

PlanSchema H2/M5/M7 and FindingStability own the rule. I14 and I12–I13 show it is an exit-0 bypass, not a cosmetic issue.

**C4. Gate self-capture (I16).** NoShell H2 owns this: `lstat`, regular file only, `O_NOFOLLOW|O_NONBLOCK`, and a size cap. It applies to `_load_json` and to `_sha256`.

**C5. Selftest.** Today there is exactly one input fixture (:369–371, `input-capture ["evtest"]`), and it passes by label only. Add the reds below so the corrections are pinned. Use plan strings only: the gate never opens them. Never pass a real `/dev/input` path as `--plan`.

## Proposed fixtures (data for L1 / SafetyCases / selftest; findings assume C1–C3)

| name | plan action(s) | expected after fix | landed today `[TRACE]` |
|---|---|---|---|
| `in_libinput_record_all_as_read` | read-source `["libinput-record","--all","corpus/evidence/all.yml"]` | 1 `denied_executable` | 0 |
| `in_libexec_record_hidraw_as_repo_write` | repo-write `["/usr/lib/libinput/libinput-record","--show-keycodes","--with-hidraw","/dev/input/event3","corpus/kbd.yml"]` | 1 (`denied_executable` or `denied_input_surface`, per precedence) | 0 |
| `in_cat_event_node` | read-source `["cat","/dev/input/event3"]` | 1 `denied_input_surface` | 0 |
| `in_dd_byid_alias` | read-source `["dd","if=/dev/input/by-id/usb-kbd-event-kbd","count=1"]` | 1 `denied_input_surface` | 0 |
| `in_double_slash` | read-source `["head","-c","48","//dev/input/event3"]` | 1 `denied_input_surface` | 0 |
| `in_symlink_stage` | repo-write `["ln","-s","/dev/input/event3","corpus/kbd"]` | 1 `denied_input_surface` | 0 |
| `in_uinput_inject` | repo-write `["tee","/dev/uinput"]` | 1 `denied_input_surface` | 0 |
| `in_dup_kind` | raw text `{"actions":[{"kind":"input-capture","argv":["cat","x"],"kind":"read-source"}]}` | 2 `plan_malformed` | 0 |
| `in_dup_argv` | raw text with `argv` twice (I13) | 2 `plan_malformed` | 0 |
| `in_extra_cmd_key` | I14 | 2 `plan_malformed` | 0 |
| `in_nul_argv0` | read-source `["evtest\u0000","x"]` | 2 `plan_malformed` | 0 |
| `in_second_action_only` | `[read-source ["cat","corpus/SOURCES.md"], read-source ["cat","/dev/input/event3"]]` | 1, `action_index` 1 | 0 |
| **green** `in_read_u6_note` | read-source `["cat","corpus/knowledge/input-debugging-boundaries-r15.md"]` | 0 `plan_safe` | 0 |
| **green** `in_grep_corpus_for_tool_name` | read-source `["grep","-rn","libinput-record","corpus/"]` | 0 `plan_safe` | 0 |
| **accepted over-refusal** `in_grep_corpus_for_dev_string` | read-source `["grep","-rn","/dev/input","corpus/"]` | 1 `denied_input_surface` | 0 |

The two greens are reason-only controls: each uses the same reader as a red, and only the operand differs.

## Residuals, even after C1–C5

- **Pre-existing symlinks and hard links** inside the lane that point at devices. The gate does no host inspection, so it cannot see them.
- **Runner context.** Runner-supplied stdin and the runner's cwd for relative operands. The plan has no `cwd`/`stdin` fields; C3 should keep it that way.
- **Wayland-protocol capture or injection without a device operand** (`wev`, `wtype`, `wl-paste --watch`). Only the executable rule touches these. `[INFERENCE]` I did not open their sources.
- **Label honesty is still unverifiable.** The gate classifies a declared plan. It never observes what runs, and a plan that is not submitted is not checked. The R15 harm needed no plan (see SafetyLearning §3).

## Cross-seat notes (owners, not mine)

- **Vocabulary drift.** `safety-cases.json` expects these findings:
  - `blocked_action_kind:<kind>`
  - `unknown_action_kind`
  - `empty_argv` (exit 1)
  - `denied_executable:<basename>`

  The landed gate emits `denied_kind`, `denied_unknown_kind`, `denied_empty_argv` and bare `denied_executable`.

  SafetyCases' independence clause says code is authoritative, but L1 must reconcile names before any frozen pins.
- **PolicyTamper.** Input capture is blocked only by policy data (`kinds`, `paused_scope`) plus two basenames, and `deny_executables` in the policy replaces the defaults (:180–181). A policy with `paused:false` and `input-capture: allow` turns I1 into exit 0 with the kind literally `input-capture`.

## Limits of this review

- The landed results are static traces of the bytes at tag `2F1C`. None was executed, and L1's single post-integration verify must confirm them.
- I quoted the libinput source at tag 1.32.0 from upstream raw files. I did not read the host's installed files or package file lists, and I did not compare digests.
- Nothing was written outside this report, and no commits were made.
