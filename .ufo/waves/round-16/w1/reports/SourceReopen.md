# SourceReopen — S051 safety quotes only, docs are data not permission

Seat: `MadoR16.SourceReopen` (scout, leaf; no delegation). Date: 2026-10-20.
Scope: reopen the admitted S051 libinput helper documentation and report only the
safety-bearing quotes, their exact anchors, and the "static documentation is not
permission" boundary. Read-only.

**Nothing was executed from the documented tools.** No `libinput` subcommand, no
`sudo`, `evtest`, replay/uinput, compositor/service/package command, no device-node
access and no live probe. No install or upgrade was made (`pacman` transactions were
not attempted; the host pause is respected). The only operations were read-only
HTTPS GETs of the pinned raw file, a local `wc -c`/`sha256sum`, and text reads of repo
bytes. Context read first: `corpus/lessons/round-15-verifier-spotcheck.md`.

## 1. Reopened identity (observed)

| Field | Observed value |
|---|---|
| URL | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` |
| Revision | tag `1.32.0` in the URL (tag-object → commit mapping from committed round-15 evidence: `c7e6fe66…` → `5cf833b5…`; not re-resolved here) |
| Bytes | **16990** (`wc -c`) |
| SHA-256 | **`53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`** |
| Comparison | matches `corpus/SOURCES.md:63`, the U6 note head line 1, and the round-15 closure quote check |

No source drift. The line numbering below is the line numbering of those exact
16990 bytes.

## 2. Safety quotes (only safety-bearing spans)

Word counts are whitespace-delimited after stripping RST markup; each is ≤25.

| Anchor | Verbatim span | Words | What it establishes | What it does not establish |
|---|---|---|---|---|
| `:31-32` | "Most of the tools must be run as root to have access to the kernel's `/dev/input/event*` device files." | 18 | A documented **precondition**: most helpers reach kernel event nodes, and the page says root is needed for that access | That root is the only barrier, that this host enforces it, that the user may run anything because it says "must", or any device/seat fact |
| `:45-46` | "This tool does **not** show your desktop's configuration, just the libinput built-in defaults." | 13 | `list-devices` output is libinput defaults, not the compositor's applied settings | Hyprland's actual option values or any client delivery |
| `:141-143` | "To reproduce the event sequence as your desktop session sees it, ensure that all options are turned on or off as required." | 22 | The debug-events run is only representative if options are passed explicitly; it does not infer the session | That any run was performed, or that defaults equal this host's settings |
| `:220-221` | "The recorded events are **kernel events** and independent of the libinput context." | 12 | `record` captures kernel-layer events independent of libinput/compositor context | Any compositor forwarding, focus, or application effect; capture itself remains input-capture class |
| `:262-263` | "For data protection, ``libinput record`` obscures key codes by default, any alphanumeric key shows up as letter \"a\"." | 18 | Default alphanumeric redaction only; the page itself limits the claim to alphanumeric keys | Blanket anonymity, safety to retain, or coverage of non-alphanumeric/HID material |
| `:276-277` | "``libinput replay`` creates a new virtual device based on the description in the log file." | 15 | Replay is **injection/mutation** by the page's own description (a new virtual device) | That a replay is a harmless read, or which events it would inject here |
| `:281-282` | "Users are advised to always replay a recorded event sequence to ensure they have captured the bug." | 17 | The page carries an **upstream bug-report workflow recommendation** to replay | Any authorization for this lane; an "advised" workflow sentence is not a permission grant |
| `:286-287` | "``libinput record --no-events`` to print the device description and exit immediately without waiting for any events" | 16 | `--no-events` suppresses event capture, not the device access implied by the command's node argument | That `--no-events` is a read-safe probe here; the flag is not an authorization token |
| `:307` | "The tool will wait for device activity before creating an output file." | 12 | With `--autorestart`, the file appears only after device activity — metadata is still produced from a live device | That an idle device is unobserved, or that metadata-only recording is identity-free |

The variant rows (`:276-277`, `:286-287`, `:307`) are the ones most likely to be
misread as "safe variants".
They are quoted so the boundary is explicit: `--no-events` still opens a device
node (the command takes `/dev/input/eventN`), replay builds a virtual device, and
autorestart is still an active `record` run. The page nowhere says any of these
are non-sensitive or permission-free.

## 3. "Static docs, not permission" — reinforcement

1. **Precondition ≠ authorization.** `:31-32` states what the tools require to
   *have access*; it never says who may run them, under what policy, or that a
   quoted page grants any right. The authority boundary remains `PROVINCE.md` /
   `SKILL.md` and the round contract, not upstream prose.
2. **`sudo` in examples is syntax, not a grant.** The examples at `:50`, `:138`,
   `:151`, `:196`, `:228`, `:271`, `:289`, `:344`, `:349` render
   `$ sudo libinput …`. They show
   invocation form for upstream bug reporters. The page does not assess this host,
   this user, or this lane.
3. **Recommendations are upstream audience advice.** `:281-282` ("Users are
   advised to always replay…") and the reporting workflow (`:261`, `:269-279`)
   address people reproducing libinput bugs. They are **source data, not
   instructions to this lane** — the same wording the committed U6 note already
   uses (`corpus/knowledge/input-debugging-boundaries-r15.md:80-81`).
4. **Redaction defaults are not classification.** `:262-263` redacts only
   alphanumeric keys by default; the page does not claim completeness. Nothing in
   S051 makes a recording or a metadata dump retainable or non-authentication-bearing.
5. **For the C2 gate.** Documentation of a command must never be an input to the
   classifier as an allow-signal. For `read-source`/`repo-write` labels, argv whose
   basename is `libinput` or `sudo` must fail closed — including
   `libinput record --no-events` and `libinput list-devices`; for the
   `input-capture` kind, the kind itself blocks regardless of argv. Neither branch
   may take a quoted sentence from S051 as an allow-signal. The gate's
   static refusal list (`pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env`)
   and the `input-capture` kind are consistent with this page's own classification
   of record/replay as device-level operations.

## 4. Cross-artifact consistency (observed)

| Artifact | Anchor | Observation |
|---|---|---|
| `corpus/SOURCES.md:63` | S051 row | URL, tag, sha256, `supersedes S007 —`, `mined`, `used-by` the U6 note all match this reopen; scope says "not host input behavior" |
| `corpus/knowledge/input-debugging-boundaries-r15.md:1-4` | head | Same pinned URL and digest; `verified-at` says static inspection, not delivery |
| same note `:66-84` | `## Safe boundary` | Lists list-devices/list-kernel-devices/quirks, debug-events/evtest/keymap logging, record (incl. `--no-events`), replay as not executed; says "source data, not instructions to this lane"; says the flag "is not authorization" |
| same note `:74` | route table | Says most helpers require input-device access — does **not** repeat "root" as the barrier |
| `corpus/README.md:40`, `SCORECARD.md:606-610` | U6 admission | Consistent with the bounded route and the S051/S052 joins; no claim of executed helpers |

No artifact I reopened presents S051 text as permission or as a live-input result.

## 5. Defects and precision notes (none block this seat)

- **D1 (low, registry-owned).** The S051 `anchor` cell (`SOURCES.md:63`) names the
  sections/Notes and the raw sha256 but records no line anchors for any quoted span,
  including `:31-32`, `:45-46`, `:141-143`, `:220-221`, `:262-263`, `:276-277`,
  `:281-282`, `:286-287` and `:307`.
  `SOURCES.md:5-7` permits only `status`, `recheck`, `used-by` to change in place,
  so L1 should **not** rewrite that anchor; record the line anchors in the round
  lesson (or leave them in this report) instead of a superseding row for an
  unchanged source.
- **D2 (low, note wording).** `input-debugging-boundaries-r15.md:76` says
  `--no-events` "still accesses a device". S051 does not say that in so many words;
  it follows from the command taking `/dev/input/eventN` to print the description.
  The statement is true but is `[INF]` from the command contract, not a verbatim
  quote. If L1 touches the note, tag it as inference; otherwise it is harmless and
  conservative.
- **D3 (low, paraphrase).** `SOURCES.md:63` teaches "debug-events requires explicit
  options". The page's exact claim is narrower in purpose: options must be set as
  required **to reproduce the sequence as the desktop sees it** (`:141-143`). The
  paraphrase is accurate as a distinction; it should not be quoted as verbatim.

## 6. Residual unknowns (not claimed, not measured here)

- The device permission model beyond the page's "must be run as root" sentence —
  group/ACL/udev reach, and whether this host actually requires root. Round-15
  `InputSafety.md` F2 recorded group-`input` membership and a udev rule from static
  files; **not re-read or re-verified by this seat**, and no node mode was measured.
- Whether `record` captures non-alphanumeric or HID material: S051 mentions only
  alphanumeric redaction; the man-page `--show-keycodes`/`--with-hidraw` material is
  outside S051 and was not reopened.
- Any host runtime condition: loaded libinput version, compositor mapping, devices,
  focus, delivery, IME, application text. None was observed.
- Whether any future operator policy would authorize any documented helper. That is
  an operator/L1 decision; this source provides no permission and this report grants
  none.

## 7. Handoff

- L1: keep S051 as-is (no in-place anchor edit); if the round lesson records safety
  anchors, use the nine spans in §2 with the digest in §1.
- Gate seats: treat documented commands and `--no-events`/redaction defaults as
  **data**, never as allow-signals; `libinput`/`sudo` argv stays refused and
  `input-capture` stays blocked.
- Verification claimed here: exact URL bytes, byte count and SHA-256; line-anchored
  quote presence in those bytes; consistency with committed repo text. Not claimed:
  tag-to-commit resolution, host permissions, tool behavior, or any execution.
