# Mado round 16 — WaybarDraft report (U7 candidate)

Seat: `MadoR16.WaybarDraft`, leaf member, no subagent dispatch. Date: 2026-10-20.

## Behavior

Wrote one candidate note: `.ufo/waves/round-16/waybar-draft.txt`, with the provenance trio (`source:`, `verified-at:`, `recheck:`), `covers: U7`, and four level-2 sections: `Producer contract`, `Renderer boundary`, `Safe observation`, `Unexercised rendering ([UNK])`. The note describes the Waybar `custom/<name>` exec producer's stdout parse path (text, tooltip, class, percentage, restart and signal conditions) and where the 0.15.0 source hands that text to GTK. It states the boundary: static reading only, with no rendered-bar claim.

Reserved source ids for L1 to register in `corpus/SOURCES.md`: **S053** (Waybar custom module man page) and **S054** (`src/modules/custom.cpp`). I did not edit SOURCES.md.

## Sources and digests

Fetched with `curl` (read-only HTTPS GET) on 2026-10-20 at 08:38:41Z:

| Id | URL | Bytes | SHA-256 |
|---|---|---|---|
| S053 | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd | 6656 | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` |
| S054 | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp | 8746 | `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` |

Local copies are in `/tmp/waybar-r16/` (outside the lane, scratch only). Digests are of the curl bytes, which are the tagged raw bytes.

## Findings from source reading (not execution)

- **Raw mode reads three lines, and continuous mode sees one.** `parseOutputRaw` (custom.cpp 222-250) takes line 0 as text, 1 as tooltip and 2 as class. `continuousWorker` (81-112) delivers one `getline` per update, so tooltip and class lines do not assemble in continuous mode. [INFERENCE from code; not exercised.]
- **Escape bug in raw tooltip (inference).** With `escape` set, line 235 escapes the first-line tooltip, but line 240 reassigns `tooltip_ = validated_line` unconditionally. The first-line tooltip is therefore unescaped unless a second line supplies one (243-246). [INFERENCE from code; not exercised.]
- **Unescaped script text is Pango markup.** `label_.set_markup(str)` (line 181) receives the formatted string; `escape` defaults to false per the man page. Whether invalid markup is rejected or shown raw is [UNK].
- **JSON percentage.** `percentage` counts only when numeric (285-288); a JSON string yields 0. [source observation]
- **Restart and clean exit.** With `restart-interval`, a clean (exit 0) end of stream keeps the previous `output_` because the branch does not reset it (88-96). A non-zero exit sets `output_` to empty, which hides the module (165). [source observation]
- **Hide conditions.** The module hides on empty output or non-zero exit when `exec` or `exec-if` is set (165), and on empty text with `hide-empty-text` (178-179).
- **Signal.** `refresh(sig)` wakes the worker only on `SIGRTMIN + signal` (138-142).

## Tooling and host record

- Installed nothing and updated nothing. Pacman transactions are paused host-wide, and the assignment forbids installs this round.
- Ran no `pacman`, `waybar`, service, compositor, input, screenshot or exec/on-click command. Only `curl` against raw.githubusercontent.com (source reads), `sha256sum`, `grep`, `find`, `ls`, `head`, plus `date -u`.
- Did not open or modify `~/.omp/agent/agent.db*` or credential files. Read `/home/vgpnk/.omp/agent/RULES.md` (no change to it).

## Missing prerequisite and overlap

- The assignment's `Read round-15-verifier-spotcheck.md` target path `.ufo/waves/round-15/...` does not exist in this lane. The file is at `corpus/lessons/round-15-verifier-spotcheck.md`. I read it there. It confirms the U7 absence (no credited note as of round 15) and the 5/7 → 6/7 coverage state.
- `corpus/knowledge/waybar-walker-semantics.md` and `waybar-walker-plane.md` already document omarchy's Waybar custom modules with RUN rows and static evidence. They carry no `covers:` marker, so they do not credit U7. This draft does not duplicate their omarchy-specific host observations. L1 should decide whether they link to S053/S054. I did not edit them.

## Limits

- Tagged 0.15.0 source only. Host version, user config and the `util::command` helpers (shell or direct exec, environment, stdin, timeout) were not read; ALabel base behaviour for `interval: "once"`, `tooltipEnabled()` and `getIcon()` was not read. All are listed `[UNK]` in the note.
- Privacy and network: neither file makes a network call. Any egress comes from the configured command, which is not established here.
- The draft asserts no rendered output, no CSS effect and no script behaviour.

## Checks for the L1 integration run (not run by this seat)

- `covers:` line regex `^covers: (U[1-7])$` on `waybar-draft.txt` (expect `covers: U7`).
- The four level-2 headings exactly as listed above.
- Register S053 and S054 in `corpus/SOURCES.md` with the digests above.

## Artifact paths

- Candidate note: `.ufo/waves/round-16/waybar-draft.txt`
- This report: `.ufo/waves/round-16/w1/reports/WaybarDraft.md`
- Scratch copies (outside lane): `/tmp/waybar-r16/waybar-custom.5.scd`, `/tmp/waybar-r16/custom.cpp`
