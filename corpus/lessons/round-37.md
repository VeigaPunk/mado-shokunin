# Round 37 — event-socket delivery: what the compositor does to a stalled client, and why this host cannot see it

Lane: mado-shokunin. Date: 2026-10-25 (attempt 2; attempt 1 left one empty directory and no file).
Registration: `.ufo/waves/round-37/registration.md` (frozen v1 at `8f0a9e3`, re-frozen v2 at
`893a8aa` before any data — Amendment 1).

## Claims

- **C1 coverage** (assimilation + sourced) — `PRED-C1-r37-v2`
  (`quality/counters/c1-r37-event-ground.py`): two entries land on ground the lane did not hold —
  `knowledge/event-delivery-limits-r26.md` (package entry, re-grounded) and
  `knowledge/event-queue-observability-r37.md` (lane-authored). Before 0/2, target 2/2.
- **C2 operability** (capability acquisition) — `PRED-C2-r37-v2`
  (`quality/counters/c2-r37-eventq.py`): `tools/mado-eventq.py`, a read-only census of the
  compositor's event-socket subscribers and their unread bytes. Before 0/10, target 10/10 with
  `readonly=1 live=1`.

## Gate

Census before (`receipts/census-before.txt` under the round-37 wave directory):
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
→ seven pre-existing `W04` (S030, S042, S045, S097, S119, S120, S121), `mado ok`, exit 0; 201 rows.
Census after: see `## Census after` below.

Source lines — every source an admitted entry cites was opened by the L1 this round (access date
2026-10-25 for all; the receipt digests below bind the bytes; quotes are ≤25 words and located):

GATE S189 receipt=.ufo/waves/round-37/fetch/S189.bin sha256=eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d quote="const size_t MAX_QUEUED_EVENTS = 64;"
GATE S189 receipt=.ufo/waves/round-37/fetch/S189.bin sha256=eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d quote="Socket2 fd {} overflowed event queue, removing"
GATE S201 receipt=.ufo/waves/round-37/fetch/S201.bin sha256=799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e quote="std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes"
GATE S212 receipt=.ufo/waves/round-37/fetch/S212.bin sha256=1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9 quote="m_ipc.registerForIPC("workspacev2", this);"
GATE S213 receipt=.ufo/waves/round-37/fetch/S213.receipt.txt sha256=1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58 quote="debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}"
GATE S214 receipt=.ufo/waves/round-37/fetch/S214.bin sha256=d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868 quote="m_logsEnabled = !*PDISABLELOGS;"
GATE S215 receipt=.ufo/waves/round-37/fetch/S215.bin sha256=a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754 quote="MS<Bool>("debug:disable_logs", "disable logging to a file", true),"
GATE S216 receipt=.ufo/waves/round-37/fetch/S216.bin sha256=74833ecbf0e2b6f8ad84345ac0716a3295a0e347420a188be0ab4f6a684af7c0 quote="conn->setName("aquamarine");"
GATE S217 receipt=.ufo/waves/round-37/fetch/S217.bin sha256=aeb07ba1ba1fd5cfdb75aaf7434910c887096c24952f1a6788f71a4d7dbe78fe quote="if (!m_logsEnabled)"
GATE S217 receipt=.ufo/waves/round-37/fetch/S217.bin sha256=aeb07ba1ba1fd5cfdb75aaf7434910c887096c24952f1a6788f71a4d7dbe78fe quote="bool                    m_logsEnabled = true;"

| id | URL / artefact | located at |
|---|---|---|
| S189 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp | `:169` (cap), `:175` (overflow marker); byte-identical to the round-32 fetch |
| S201 | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp | `:115`; byte-identical to the round-34 fetch |
| S212 | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp | `:804` |
| S213 | host: session `hyprland.log`, `journalctl --user -u wayland-wm@hyprland.desktop.service`, `hyprctl getoption debug:*` | receipt § live options |
| S214 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/log/Logger.cpp | `:48` |
| S215 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp | `:629` |
| S216 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/Compositor.cpp | `:306` |
| S217 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/log/Logger.hpp | `:23` |

Rows added: S212–S217 (six; tier A; kinds code ×5, own-work ×1), all `mined`, opened 2026-10-25.
In-place changes (CORPUS.md rule 2), old → new:

- S189 `used-by`: `corpus/knowledge/ipc-contract-r25.md` → `corpus/knowledge/ipc-contract-r25.md, corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md`
- S201 `used-by`: `corpus/knowledge/waybar-module-text-route-r25.md` → `corpus/knowledge/waybar-module-text-route-r25.md, corpus/knowledge/event-delivery-limits-r26.md`

No row's `status` or `recheck` changed.

### Assimilation (shokuknow `corpus-expansion-1`, package `merge/mado/`, read-only)

One theme: event-socket delivery. Three package entries considered.

| package entry | verdict | reason | flip |
|---|---|---|---|
| `event-delivery-limits-r26.md` | **admit**, re-grounded | every sentence re-checked against re-fetched bytes; five corrections (the entry's `## Assimilation` note) | — |
| `event-queue-host-measurement-r28.md` | **refuse** | reads a zero marker count in the session log as "never overflowed"; with `debug:disable_logs` = 1 (the shipped default, S215 `:629`) the core logger returns before formatting (S217 `:23-24`), so the log is a null channel; its own source (instance `_1792772698_564628331`) no longer exists | a host with `debug:disable_logs = false`, core lines present after the config load, re-counted |
| `event-queue-journal-measurement-r29.md` | **refuse** | the same null channel, plus the unit journal never carries the core logger (S214 `:47`; probe string 7× in the log, 0× in the journal, S213) | as r28, and `debug:enable_stdout_logs = true` |

Staged rows appended: none as-is. Rows the admitted entry cites, re-pointed **by document**: package
S187 → lane S189, S188 → S201, S214 → S212 (`.ufo/waves/round-37/assimilation/renumber-map.md`).
Id collision check (prompt §10 commands, 0–3-space pattern): reg-ids 201, staged-ids 147,
collisions **9** (S203 S204 S205 S206 S207 S208 S209 S210 S211); guard proof: an indented `  | S002 |`
scratch row is caught by the 0–3-space pattern (n=1) and missed by the column-zero one (n=0).
Recheck prose stripped: none needed (all six rows carry a bare cadence).

Quarantine slice (13 mado data rows): register `round1 S189` (EventManager.cpp, `payload-absent`)
hand-checked — **present** at `:128` (`auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`);
the register's escaped form is why it found nothing. The other twelve name documents no admitted
entry cites; unappended and unchecked.

## Census after

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
→ the same seven pre-existing `W04`, `mado ok`, exit 0 (`receipts/census-after.txt`). Rows 201 → 207
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`): tier A +6 (code 5,
own-work 1); two rows touched in place (S189, S201 `used-by`, above).

## Mistakes

class · evidence · captured-by · fix

- **M37-1** vacuous · v1 control `c1-golden` (`receipts/controls.txt`: a token-only stub, `admitted=2/2 TARGET_MET`) · prompt §9 cheapest-control rule · clause **g** (`PRED-C1-r37-v2`); shown able to fail: the same stub is `c1-token-stub` → `TARGET_MISSED` in `receipts/controls-v2.txt`.
- **M37-2** stale-premise · the package's r28/r29 "never overflowed" readings · none (the campaign had no channel probe) · refused; QUALITY criterion 62; able to fail: S213's probe string is counted 7 in the log and 0 in the journal.
- **M37-3** landing · round-36 report "working tree clean" with `DistillerFindings.md` untracked (spot-check R1) and `inherited_dirty` read from the worktree (R5) · QUALITY 52-style landing rules did not cover worktree observables · file committed at `80b83c8`; QUALITY criterion 63.
- **M37-4** survivor · four lane gates inherited `GIT_*` (`w1/scratch/ExecPointerEnv/red-green.txt`: `GIT_WORK_TREE=/dev/shm` turns `inherited_dirty=0` into `8`; `GIT_DIR` errors or flips `mismatched=0` to `2`) · none · every git subprocess runs with `GIT_*` removed; shown able to fail by the red run, green in `receipts/git-env-green.txt` (identical digests plain and under both variables).
- **M37-5** survivor · after the freeze, wave-1 seats reached both frozen targets with cribs: C1 with a 19-line tree whose fabricated row's "receipt" is the entry itself (`w1/reports/CritC1Cheap.md`), C2's live clause with a snapshot built from the counter's own fixture rows (`w1/reports/RevC2Code.md` F1) · none — the cheapest-control rule was applied only to the L1's own controls · not fixable under the frozen rule (kumitate r42); routed: next counter binds each Gate receipt to `fetch/` and to a re-fetch digest, and cross-checks a live snapshot against `/proc/net/unix` server inodes (this round's `receipts/eventq-live-proc-crosscheck.txt` does this by hand).

### M37-2 — a zero count read on a channel that cannot carry the class

The package measured "zero overflow markers" twice and concluded the queue never overflowed. On a
default v0.56.2 host the logger that writes those markers is off after start-up, so the zero is
structural. The lane made the same move in round 35 (the `omarchy-toggle` journal count, withdrawn).

### M37-3 — a worktree reading reported as a revision fact

The round-36 report asserted a clean tree from a moment's `git status`; one seat report landed
after it. A worktree observable needs a committed witness.

## considerthese

`considerthese/2026-10-24.md` proposal 4 (2026-10-24, "Suggest the next desktop table explicitly …
propose which Hyprland surface is next … with the sources that would ground it"), implemented as
data by wave-1 `ConnFrontier` (`.ufo/waves/round-37/w1/reports/ConnFrontier.md`), sources opened
2026-10-25: (1) the config-option table — who owns each key, predicted from the config tree and
checked against `getoption` per name (HyprCtl.cpp `:2039` registers `getoption`; ConfigValues.cpp,
S215, is the compiled option table with defaults); (2) monitor rules against `hyprctl monitors`;
(3) window and layer rules. This round itself took the event socket, the surface the lane's IPC
contract entry already bordered. The reflection is a pointer, not evidence; the ranking rests on the
opened files named in that report.
