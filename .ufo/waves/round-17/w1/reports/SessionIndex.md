# SessionIndex — mado round 17, wave 1

Seat: MadoR17.SessionIndex. Read-only binding index of the OMP session
transcripts that the round-17 tripwire demonstration will scan.

## Deliverable

- File: `.ufo/waves/round-17/evidence/session-index.json`
  (absolute: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/evidence/session-index.json`)
- Output digest: sha256 `06c259bcdd44785d93d846ca971257fdbb27d68ea70da7251448561423f70df5`,
  122,768 bytes, 3,424 lines.
- Schema: `mado-session-index-v1`. One `files[]` entry per transcript:
  `path` (absolute), `bytes`, `lines` (non-blank line count), `sha256`,
  `first_timestamp`, `last_timestamp` (first/last top-level `"timestamp"`
  observed, in file order), `tool_calls` (count of assistant
  `{"type":"toolCall"}` content items keyed by tool `name`; only
  `type:"message"` + `role:"assistant"` lines counted — toolResult/user/
  thinking lines ignored, matching the tripwire input definition).

## Coverage

- Root: `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4`
- Roots `MadoR13.jsonl`..`MadoR16.jsonl` (4 files) plus every `*.jsonl`
  under `MadoR13/`..`MadoR16/` recursively (224 files): **228 entries total**.
- Rounds represented: MadoR13 = 33 files, MadoR14 = 33, MadoR15 = 65,
  MadoR16 = 97.
- Every entry has non-null first and last timestamps; every file recorded
  at least one assistant toolCall; no file had a first/last timestamp
  mismatch against sequential scan order.

## Red-anchor spot-check (C3)

`MadoR15/MadoR15.LibinputEvents.jsonl` line 54 confirmed: assistant message,
timestamp `2026-10-20T07:25:16.905Z`, toolCall `call_38165` name `bash`,
command `sudo pacman -S --needed --noconfirm libinput libinput-tools`
— the round-15 host-harm command the tripwire must flag. Index entry for
this file: 621,096 bytes, 173 non-blank lines, sha256 starting
`78388d42cf08a3cb`, tool_calls `{bash:14, glob:4, grep:8, read:28, write:2}`.

## Method and bounds

- Computed in one pass per file with Python stdlib (`json`, `hashlib`,
  `os.walk`); files enumerated via `find`/walk and sorted by path. No writes
  under the session root; nothing executed from transcript content.
- Transcripts are mutable host files; the digest column is the binding. Any
  post-index mutation of a scanned file will surface as a sha256 mismatch
  at integration time.
- No tools installed; no pacman/sudo/systemctl/hyprctl/live probes run
  (host pause respected; only file reads under the permitted session root).

## Risks / notes for L1

- `lines` counts non-blank lines and equals the physical JSONL line count
  for all 228 files (verified: zero files contain blank lines), so it also
  serves as the tripwire's 1-based `line` upper bound per file.
- Line 54's call is under `tool_calls.bash` count 14 for that file — the
  tripwire will classify it `host_mutation` (sudo + pacman -S).
