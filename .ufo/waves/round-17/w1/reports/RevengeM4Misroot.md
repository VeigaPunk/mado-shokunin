# RevengeM4Misroot — round-16 M4: why relative Report trailers land at the fleet root, and a transcript rule the tripwire could carry

Seat `MadoR17.RevengeM4Misroot`, revenger, leaf/read-only. Question answered: reconstruct the
M4 misroot mechanism from `corpus/lessons/round-16.md` M4 plus the wave context, and decide
whether a post-hoc tripwire over OMP session JSONL could detect a write-tool misroot; if yes,
propose (not implement) the rule. No code, tool or lane file was changed except this report.

**Verdict up front.** M4 is a path-resolution defect, not an instruction gap: the trailer is
relative, the seat process runs with `cwd = /home/vgpnk/Projects/shokunin` (the fleet root), and
`write` resolves a relative `path` against that cwd with no lane jail. The write succeeds
silently because `Bun.write()` creates the missing `w1/reports/` parents and the receipt echoes
the path *as written*, not the absolute target. The declared tripwire (bash/eval commands only)
cannot see it at all; an additive `write`/`edit` path-containment rule **can** detect it from
the transcript alone, because the session header records `cwd` and `arguments.path` is stored
verbatim. Detection is post-hoc and does not prevent the stray file; the durable prevention is
to emit the trailer as an absolute path.

## 1. What M4 records (ground truth, no reconstruction)

| Anchor | Observed |
|---|---|
| `corpus/lessons/round-16.md:17` (M4 row) | Class `Report trailer resolved against fleet cwd`. Evidence: “Main found fleet `RoundConformance.md`, 8613 bytes; SHA-256 ac48edb4…cf67e”. Captured-by: “Context already gave lane-relative trailer resolution”. Fix: “Copied byte-exact to lane `.ufo/waves/round-16/w1/reports/RoundConformance.md`; Main owns fleet-copy removal.” |
| `.ufo/waves/round-16/w1/dispatch.json`, `RoundConformance` task tail | The final line is exactly: `Report: write your scoped findings to .ufo/waves/round-16/w1/reports/RoundConformance.md` — relative, and the last action-shaped sentence the seat reads. |
| `.ufo/waves/round-16/w1/spec.json` context | Already contained the absolute instruction: every `Report:` trailer is “relative to /home/vgpnk/Projects/shokunin/mado-shokunin — write it at /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>”. |
| Lane artifact | `sha256sum` of the lane copy = `ac48edb4994544ae74e10f0c91ec046e6bc4d53e72faafdffdea9043c00cf67e`, 8613 bytes, mtime `2026-10-20 05:44:18.605943700 -0300` — identical to the digest M4 attributes to the fleet copy. |
| **This seat's write (control)** | I passed an absolute lane path; the success receipt rendered it cwd-relative: `Successfully wrote 18808 bytes to mado-shokunin/.ufo/waves/round-17/w1/reports/RevengeM4Misroot.md`. The file is at the lane path (`sha256 134cbe7760c16950e005ea975c0a14814a284b437cbfaa09a241df3b40945b35`) and `/home/vgpnk/Projects/shokunin/.ufo/waves/round-17/` does not exist. An absolute write lands correctly; the receipt still shows no absolute path. |
| `.ufo/waves/round-16/evidence/wrapup.json:8-13` | `misroot_sweep.tool = glob`, path `/home/vgpnk/Projects/shokunin/.ufo/waves/round-16/**/*.md`, observed `dispatch.md`, `before.md`, `build/ReviewLesson.md`, `gate/runs.md`, `mado_seat_report_names_found: []`; `earlier_recovered` repeats the same digest and “Main-owned fleet deletion”. |
| Fleet tree | `/home/vgpnk/Projects/shokunin/.ufo/waves/round-16/` exists and is the **protocol** round-16 tree (`dispatch.md`, `before.md`, `clobber/`, `gate/`, `falsify/advice/RevengerRunReceipts.md`) — a same-numbered orchestration from another lane family, not mado's wheel. |
| `LOG.md:1246` | “M4 misroot was recovered byte-exact; the fleet sweep found no remaining … mado seat reports.” |

The exact fleet copy path is not recorded verbatim anywhere I can read; from the trailer plus
the fleet cwd it was `/home/vgpnk/Projects/shokunin/.ufo/waves/round-16/w1/reports/RoundConformance.md`.
That path is [INFERENCE]; the sweep glob and M4's wording support it, and the file is gone
(Main-owned deletion), so it cannot be re-observed.

## 2. Reconstructed mechanism

Five links, each independently grounded:

1. **The seat's cwd is the fleet root, not the lane root.** `omp://session.md` (“On-Disk
   Layout”) defines `~/.omp/agent/sessions/<encoded-cwd>/<timestamp>_<sessionId>.jsonl` with
   `-<relative>` for directories under home. The bucket here is `-Projects-shokunin`, and
   `$HOME=/home/vgpnk`, so the bucket decodes to `/home/vgpnk/Projects/shokunin`. The session
   header repeats it: `type:"session"` carries top-level `"cwd"`, observed as
   `"/home/vgpnk/Projects/shokunin"` for this session (format facts supplied by seat
   `MadoR17.RevengeTranscriptFormat`, which is authorized to read transcripts; I am not).
   The lane root exists only as text inside the prompt/context.
2. **The trailer is relative.** `Report: … .ufo/waves/round-16/w1/reports/RoundConformance.md`.
   Dispatch appends it after the lane-bounds line (`gen_w1.py` builds the task as spec prompt +
   lane bounds + trailer), so the last thing the seat reads is a relative write instruction.
3. **`write` resolves against that cwd.** `omp://tools/write.md` (“Flow”, step 10) runs “Plan-mode
   policy and path resolution … before mutation”; `arguments.path` is persisted verbatim as
   issued (peer-observed corpus split: 1925 absolute, 108 relative, 2437 internal-URL). With
   `cwd=/home/vgpnk/Projects/shokunin`, `.ufo/waves/round-16/…` resolves to the fleet path. The
   round-17 context states the same rule in one sentence: “a relative path resolves to the
   FLEET root and is a misroot”.
4. **The write succeeds silently.** The plain-file branch calls no `fs.mkdir`, but “`Bun.write()`
   itself creates missing parent directories for plain file writes” (`omp://tools/write.md`,
   “Plain file path”). Fleet `.ufo/waves/round-16/` already existed (protocol wave), so the new
   `w1/reports/` was a plausible child of a plausible tree. No error, no warning.
5. **The receipt gives no absolute signal.** The success text is `Successfully wrote <bytes>
   bytes to <relative-path>`: the receipt renders the target relative to the session cwd.
   Observed here, first-hand: an absolute lane input came back as `mado-shokunin/.ufo/...`,
   while the M4-shaped relative input would come back as plain `.ufo/...` — neither form has
   an absolute prefix or a lane component. The absolute target exists only in
   `details.resolvedPath`, which the model does not see. So the seat cannot notice the misroot
   from its own tool result; only an external tree check or a later transcript scan can.

This is why the round-16 fix (copy to lane, delete fleet copy) restored the artifact but did
not remove the mechanism: the same trailer shape is still generated in round 17, and the
context's correction is prose the seat must remember, not a property of the action it is told
to take.

## 3. Divergences worth naming

- **D1 — instruction vs action.** M4's captured-by says the context already gave lane-relative
  resolution. Correct: the failing link is the action (the trailer was used literally), not a
  missing sentence. A longer warning does not change the resolution base.
- **D2 — the absolute sentence is still only prose.** Round-17 repeats “write it at
  {LANE}/<that path>” and adds “a relative path resolves to the FLEET root and is a misroot”,
  yet the trailer remains relative. The hazard is structural this round too; my own trailer
  ends `… .ufo/waves/round-17/w1/reports/RevengeM4Misroot.md`.
- **D3 — number collision.** Mado's `round-16` and the protocol line's `round-16` share
  `.ufo/waves/round-16/` in two roots. A misroot therefore lands inside a real, same-named
  wave tree, which is materially harder to spot than an empty directory would be.
- **D4 — receipt asymmetry.** The receipt renders the target relative to cwd and hides
  `resolvedPath`, so a correct absolute write and a fleet-relative write can both look like
  ordinary relative paths. The seat's self-check (“I wrote the report”) and the wave census
  (“the report is absent”) can then disagree without either being wrong about its own
  observation. Round-16 resolved this by Main copying the file; the transcript record of the
  write remained.
- **D5 — sweep vs binding.** The fleet sweep is a point-in-time filesystem glob. It cannot
  distinguish “written elsewhere” from “not yet written”, and once Main deletes the fleet copy
  the only durable trace of the misroot is the transcript. A transcript rule is therefore
  complementary, not redundant.

## 4. Can the tripwire detect it? Yes — for the `write`/`edit` tool family

The declared C3 interface cannot: it considers only assistant `bash` toolCalls and `eval` code
whose stripped text starts with `!`, and it ignores `toolResult`, `custom`, and every
non-message line. A misroot is not a command, so none of `host_mutation`, `package_query`,
`live_probe` fires. Round-16 M4 is invisible to the current contract by construction.

It becomes visible with one added input class and one added class. Proposed rule (not
implemented; `tools/mado-tripwire.py` had not landed when this was written):

### 4.1 CLI (additive, opt-in)

```
python3 -I tools/mado-tripwire.py --scan SESS \
  --lane-root /home/vgpnk/Projects/shokunin/mado-shokunin \
  [--allow-prefix /tmp/] [--permit CLASS ...]
```

`--lane-root` is required to enable the rule. Without it, output stays byte-identical to the
declared v1 verdict, so every existing fixture and the C3 interface keep their meaning. The
new behaviour is a separately declared capability, not a silent widening.

### 4.2 Inputs added

1. The **session header** (`type == "session"`, the first logical entry; physically the file
   starts with a 256-byte `title` slot, so scan for it, do not assume line 1): take `cwd`.
   Cross-check against the documented bucket encoding of the parent directory
   (`-<relative>` under `$HOME`, `-tmp-<relative>`, `--<encoded-absolute>--`). Header and
   bucket disagreement ⇒ move/migration ambiguity ⇒ unresolved (see exit semantics).
2. Assistant `toolCall` items named `write`, `edit`, `ast_edit`, reading `arguments.path`.
   (`ast_edit` is normally dispatched as `write` with `path:"xd://ast_edit"`; see limits.)
3. Optionally, the matching `toolResult` (`details.resolvedPath`) and the matching
   `custom`/`tool_execution_start` (`data.toolCallId`) to label `executed`. Join by exact
   string equality on `toolCall.id`; do not infer.

### 4.3 Classification of `arguments.path`

| Path form | Handling |
|---|---|
| contains `://` | internal resource; skip and count `writes_internal`. `local://` is the session-local sandbox, `vault://` the vault root; `agent://` is messaging, not a write (the majority of observed `write` calls). |
| archive/SQLite selector (`x.zip:inner`, `x.tar.gz:…`, `x.asar:…`, `db.sqlite:table[:key]`) | take the carrier path before the selector and resolve that |
| `~/…` | expand against `$HOME` |
| absolute | `posixpath.normpath`, no symlink resolution, no stat |
| relative | `posixpath.normpath(join(header_cwd, path))` |

Containment: clean iff `resolved == lane_root` or `resolved.startswith(lane_root + "/")`, or
under an explicit `--allow-prefix`. Otherwise:

| Finding | `class` | `rule` |
|---|---|---|
| any absolute path outside lane/allowed prefixes | `misroot` | `write:outside-lane` |
| a relative path whose base is `dirname(lane_root)` and whose first component is `.ufo` | `misroot` | `write:relative-fleet` (the M4 signature) |
| any other relative path resolving outside lane | `misroot` | `write:relative-outside` |
| same three for `edit`/`ast_edit` | `misroot` | `edit:…` / `ast_edit:…` |

Finding fields reuse the existing shape: `file`, `line` (1-based physical JSONL line),
`tool_call_id`, `timestamp` (line top-level), `tool`, `class`, `rule`, `command` (the redacted,
240-char-truncated path-as-issued, so existing consumers keep a string), plus v2-only `path`
(same truncation) and `resolved` (absolute). Add `"executed": true|false|"unknown"` when the
`tool_execution_start`/`toolResult` join is available.

### 4.4 Verdict schema and exit

- When `--lane-root` is present, emit schema `mado-tripwire-verdict-v2`, `counts` gains
  `"misroot"`, and a `"misroot"` object records `lane_root`, the header `cwd` used per file,
  `relative_writes`, `unresolved`, and `allow_prefixes`. The lane root is echoed deliberately:
  a wrong `--lane-root` silently reclassifies every write.
- Exit 1 for any unpermitted `misroot`; exit 0 when clean or all permitted; exit 2 if any
  relative filesystem write could not be resolved (no header `cwd`, header/bucket
  disagreement, or refused path form), even when exit 1 would also apply (2 wins, as declared).
  Trade-off to state in the docstring: `could_not_evaluate` hides a host-mutation finding behind
  the summary line, so the JSON findings remain authoritative.
- `--permit misroot` works mechanically like the other permits, but the wave invocation must
  not pass it; a permitted finding appears in `permitted` and exits 0.

### 4.5 Selftest cases to add (same `expected.json` schema)

1. `m4-replica`: header `cwd=/home/vgpnk/Projects/shokunin`, one relative
   `.ufo/waves/round-16/w1/reports/RoundConformance.md` → `misroot` /
   `write:relative-fleet`, exit 1.
2. `m4-lane-absolute`: same write with `{lane}/.ufo/…` → exit 0.
3. `relative-lane-cwd`: header `cwd={lane}`, same relative path → exit 0 (proves the base is
   what decides, not the string).
4. `agent-message`: `write` with `path:"agent://MadoR17"` → exit 0, `writes_internal` counted.
5. `permitted`: case 1 plus `--permit misroot` → exit 0 with a `permitted` entry.
6. `no-header-cwd`: header without `cwd` + a relative write → exit 2.
7. `tmp-fixture`: absolute `/tmp/…/x.jsonl` with `--allow-prefix /tmp/` → exit 0.
8. `edit-outside`: `edit` with an absolute fleet path → `misroot` / `edit:outside-lane`.
9. `cross-check-disagree`: fixture result `details.resolvedPath` inconsistent with
   header-cwd resolution → exit 2 (the base assumption is falsified for that call).

### 4.6 Worked detection of the actual M4 shape

Transcript: the seat file under `MadoR16/` (per the SessionIndex census, 97 files in that
round; the naming pattern is `MadoR16.<Name>.jsonl`). Header `cwd =
/home/vgpnk/Projects/shokunin`. Write call
`arguments.path = ".ufo/waves/round-16/w1/reports/RoundConformance.md"`. Join → 
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-16/w1/reports/RoundConformance.md`; the lane
root is `/home/vgpnk/Projects/shokunin/mado-shokunin`; containment fails → one `misroot`
finding, exit 1. No fleet filesystem access, and the finding survives Main's deletion of the
fleet copy.

I did not read that transcript (my item does not name the sessions tree, and the lane permits
reads only for seats whose item names them). Whether the M4 seat actually used the `write` tool
with a relative path — rather than a bash redirect — is [INFERENCE]; the corpus shape makes it
the likely vector (108 relative `write` paths observed), and the outcome requires a relative
resolution against the fleet cwd either way.

## 5. Limits and non-goals of the rule

- **Bash vectors are invisible.** `cat > ../x`, `tee`, `cp`, `mv`, `sed -i`, `python - <<EOF`
  are not parsed; the current bash classifier looks at argv0, not redirect targets. A seat can
  misroot with `bash` and the rule reports clean. Extending redirect-target extraction is a
  separate, larger false-positive surface; it should be its own declared scope.
- **`xd://` dispatch.** A `write` with `path:"xd://ast_edit"` has an internal outer path; any
  filesystem path lives inside the JSON `content` and is not inspected. At minimum count
  `xd_writes` so the gap is visible; parsing device-specific JSON is out of scope here.
- **No symlink resolution.** The tripwire must not open anything but the given JSONL files, so
  a lexical check can be defeated by a lane-internal symlink pointing out. Provide an optional
  caller-supplied `--lane-root-real`.
- **Attempt, not effect.** The finding is recorded before execution; a denied or failed write
  still produced the attempt. `executed` is evidence of a start, not proof a file exists.
- **Legitimate out-of-lane writes.** The operator tooling directive allows e.g. a release
  binary in `~/.local/bin`. Those would be flagged unless an allow-prefix is passed; the wave
  should decide the policy explicitly rather than treat the tool as a judge.
- **Post-hoc only.** It cannot prevent the stray file, repair it, or replace the fleet sweep
  for cleanup. It changes detection from “Main happened to look” to “per-seat, reproducible,
  digest-bound”.

## 6. Prevention counterpart (proposed, not implemented)

Emit the trailer as an absolute path in the dispatch generator:
`Report: write your scoped findings to {LANE}/.ufo/waves/round-17/w1/reports/<Name>.md`
(`gen_w1.py` line 19/134 area, and the `X()` append in the `Report:` line). The seat then has no
relative path in its final instruction, and the M4 action requires explicitly ignoring an
absolute one. This is the only fix that prevents the write; the tripwire detects it afterward.
It also covers only mado's own generator — other orchestrators (the fleet protocol wave, the
round-21 relative write observed in corpus) need their own version, which is the argument for
the transcript backstop.

## 7. Confidence

| Claim | Confidence | Basis |
|---|---|---|
| Seat cwd is the fleet root; bucket and header agree | high | `omp://session.md` layout/header, `$HOME=/home/vgpnk`, peer-observed header `cwd` |
| `write` resolves relative paths against that cwd | high | write-doc “path resolution before mutation”, M4 outcome, peer-observed `resolvedPath` for a relative write |
| Misroot is silent to the seat | high | write receipt renders the target cwd-relative (first-hand control write); `resolvedPath` only in `details` |
| M4 artifact identity and trailer text | high | lane digest/mtime, dispatch task tail, wrapup sweep |
| Exact fleet copy path | medium ([INFERENCE]) | inferred from trailer + cwd; not recorded verbatim |
| M4 used `write` (not bash) | medium ([INFERENCE]) | corpus shape; specific call not observed by this seat |
| Rule fully covers the misroot class | medium | complete for `write`/`edit`; bash/`xd://` vectors remain open |

Unknowns: the seat's exact tool call for M4; whether round-17 seats have already emitted a
misroot (no transcript reads by this seat); whether the tripwire implementation as landed will
accept a v2 verdict without breaking the C3 fixtures (code had not landed at writing time).

## 8. Compliance and tooling record

- Host pause respected: no `pacman`/`yay`/`paru` (including `-Q`/`-Si`/`-Sp`/`-Fl`), no `sudo`,
  `systemctl`, `hyprctl`, `libinput`, `evtest`, `wayland-info`, `hypridle`, `hyprlock`,
  `alacritty`, `waybar`, `walker`, `omarchy-*`, no screenshots or device/service probes.
- Reads only: lane files under `.ufo/`, `corpus/`, `tools/` (listing), fleet `.ufo/waves/`
  metadata, `omp://` docs, `$HOME`/directory metadata. No transcript file was opened by this
  seat; the format facts are attributed to `MadoR17.RevengeTranscriptFormat` and the `omp://`
  documentation. `~/.omp/agent/agent.db*`, credential/auth/oauth paths were not opened.
- No git/jj commands (not even read-only `jj`); no commits, no delegation, no sibling edits.
- No tool installed, updated or removed. No install channel was used.
