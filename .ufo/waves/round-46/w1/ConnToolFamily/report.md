# ConnToolFamily — mado round 46 w1 — live-state tool family consistency + ledger

Seat: ConnToolFamily (connector, leaf). Scope: compare the round-46 reference
`.ufo/waves/round-46/l1-draft/mado-devices.py` (C1, frozen contract) against the
committed live-state tool family on five interface axes; list the inconsistencies
the new tool introduces with fix proposals; draft the proposal-2 ledger from
committed receipts only. No lane files edited; no counters/fixtures touched.

## Axes

- **A1 interface consistency** — do the new tool's argument forms, setup lines,
  exit maps, output prefixes and read-only boundaries match the family?
- **A2 ledger utility** — can a reader see, per tool, the question it answers,
  its last committed live-run receipt and the verdict?
- **A3 evidence discipline** — every claim tied to a committed path:line or a
  committed receipt; nothing fabricated.

Verdict up front: A1 mostly holds (the reference clones the mado-monitors.py
template); three real inconsistencies are introduced (I1–I3 below), two minor
notes (I4–I5). A2 delivered as the table in §4. No fix touches frozen artifacts;
all fixes are proposals for the tool's own docs/behaviour when it lands.

## 1. Family profile across the five axes

Two sub-families exist. **Dump-joiners** take one live dump on stdin (or a file)
plus config files, and join them offline. **Live-probers** run read verbs
themselves. The new tool is a dump-joiner and is compared against
mado-monitors.py and mado-geometry.py, its two siblings.

| tool | argument form | setup-error line (exit) | exit map (priority order) | output line prefixes | read-only boundary |
|---|---|---|---|---|---|
| mado-monitors.py | two-token: `--selftest` alone, or `--monitors V` once + `--config V` 1+ (any order) | `MADO_MONITORS: SETUP <reason>` exit 2; reasons usage\|unreadable\|too_large\|bad_json | NO_RULES(4) → NOT_COMPARED(5) → DIFFER(1) → NO_MATCHING_MONITOR(3) → OK(0) | MADO_MON_RULE, MADO_MON_OUTPUT, summary MADO_MONITORS | files+stdin only, no process/socket; 1 MiB cap (tools/mado-monitors.py:26,28,100-102,464-470) |
| mado-geometry.py | two-token: `--selftest` alone, or `--clients V` once + `--rules V` 1+ | `MADO_GEOMETRY: SETUP <reason>` exit 2; same 4 reasons | NO_SIZE_RULES(4) → DIFFER(1) → NO_MATCHING_CLIENT(3) → NOT_COMPARED(5) → OK(0) | MADO_GEOM_RULE, MADO_GEOM_CLIENT, summary MADO_GEOMETRY | files+stdin only; same cap (tools/mado-geometry.py:19-26,65-73,262-270) |
| **mado-devices.py (new ref)** | two-token: `--selftest` alone, or `--devices V` once + `--config V` 1+ | `MADO_DEVICES: SETUP <reason>` exit 2; same 4 reasons | NOT_COMPARED(5) → DIFFER(1) → NO_KEYBOARDS(3) → STALE_BLOCK(4) → OK(0) | MADO_DEV_KEYBOARD, MADO_DEV_MOUSE, MADO_DEV_BLOCK, summary MADO_DEVICES | files+stdin only; same 1 MiB cap (.ufo/waves/round-46/l1-draft/mado-devices.py:28,80-89,99,410-419) |
| mado-globals.py | argparse: `--journal-file PATH [--expect N]... [--diff]` or `--live [--journalctl P]` | `MADO_GLOBALS: SETUP <reason>` exit 2 (usage/input); exit 5 live journal failure | OK(0) / MISSING_EXPECTED(1) / NO_SESSIONS(3) / UNRECOGNIZED_FORMAT(4) | MADO_GLOBALS_SESSION, MADO_GLOBAL, MADO_GLOBALS_DIFF, summary MADO_GLOBALS | `--live` runs journalctl subprocess; 8 MiB cap (tools/mado-globals.py:24,28,45) |
| mado-eventq.py | argparse flags, live defaults (`--ss-file`, `--log`, `--journal-file`, `--disable-logs`, `--snapshot-out`, `--expect-client`) | `MADO_EVENTQ: SETUP <reason>` exit 2, ten named reasons | CLEAN(0) / MARKERS\|MISSING_CLIENT(1) | MADO_EVENTQ_CLIENT, MADO_EVENTQ_MARKERS, summary MADO_EVENTQ | runs ss/journalctl/hyprctl-getoption; writes --snapshot-out (tools/mado-eventq.py:60-62,78-79) |
| mado-options.py | argparse: `--home DIR [--getoption FILE \| --live [--hyprctl P] [--probe K]...]` | named failures on **stderr**, exit 3/4/5; exit 2 usage | OK(0) / selftest-fail(1) / usage(2) / read-fail(3) / getoption-malformed(4) / live-fail(5) | **none** — one JSON array | static path no subprocess; `--live` runs hyprctl getoption per key (tools/mado-options.py:61-65,80) |

## 2. What the new tool keeps consistent (no action needed)

- Two-token argument grammar is byte-for-byte the monitors template
  (mado-devices.py:28 vs tools/mado-monitors.py:28), including "anything else is
  usage" and "in any order".
- Same setup contract: single stdout line `MADO_DEVICES: SETUP <reason>`, exit 2,
  same closed reason set usage|unreadable|too_large|bad_json
  (mado-devices.py:29-33,546-557).
- Same size policy: MAX_BYTES = 1048576, stdin read capped at 1048577
  (mado-devices.py:99; monitors matches).
- Same read-only boundary sentence: "It reads files and standard input only; it
  starts no process and opens no socket" (mado-devices.py:34; monitors:26).
- Same field encoding `<json>` = json.dumps ensure_ascii; same
  `MADO_<TOOL>_SELFTEST: n/n passed` shape (mado-devices.py:542).
- Exit codes stay on the family ladder (5/1/3/4/0 with 2 reserved for setup);
  verdict vocabulary reuses AGREE/DIFFER/NOT_COMPARED/OK.

## 3. Inconsistencies the new tool introduces (fix proposals)

**I1 — `verdict=DIFFER` no longer implies `differ>0` on the summary line.**
The exit-1 test is `differ + fallback + mice_differ > 0` (mado-devices.py:412),
but the summary's `differ=` counter counts keyboard DIFFERs only
(mado-devices.py:420-422). A run with one FALLBACK keyboard and everything else
agreeing prints `differ=0 ... verdict=DIFFER` (exit 1); same for one differing
mouse (`mice_differ=1`, `differ=0`). In monitors, `verdict=DIFFER` ⇔ `differ>0`
(tools/mado-monitors.py:468); geometry likewise (tools/mado-geometry.py:265).
Any family wrapper that gates on `differ=0` before trusting `verdict=DIFFER`
mis-reads the new tool.
Fix proposals (cheapest first): (c) document the trio invariant in the docstring
next to the output spec (mado-devices.py:84-89); (a) fold fallback+mice_differ
into the printed `differ=` count; (b) keep counters and add a
`verdict_driver=` field. Recommend (c) for this round — the counter and 150
generated cases pin the current line, so a print change is a contract change.

**I2 — internal asymmetry: the mouse line shows expected AND reported, the
keyboard line shows expected only.**
`MADO_DEV_MOUSE` prints `scroll_factor=<expected> reported=<actual>`
(mado-devices.py:82,400-402), but `MADO_DEV_KEYBOARD` prints only the expected
XKB names (mado-devices.py:81,385-388); the reported names exist only inside
`differ=<names>`. Geometry prints both sides (`size=` live, `want=` declared,
tools/mado-geometry.py:67); monitors prints declared values plus differ fields.
The new tool mixes the geometry style (mouse) with the monitors style (keyboard)
inside one tool, and the FALLBACK verdict — defined as "reported is exactly
us/empty" — cannot be eyeballed against the printed names.
Fix proposal: add the five reported names to the keyboard line (or a compact
`reported=` blob), or drop `reported=` from the mouse line. Recommend adding:
it makes FALLBACK self-explanatory and helps CI greps. Contract-pinned, so land
as a doc fix + a follow-up proposal, not a silent change.

**I3 — the exit-4 domain verdict moved from first to last in the priority
ladder.**
Monitors tests NO_RULES(4) first, before NOT_COMPARED(5)
(tools/mado-monitors.py:464-466); geometry tests NO_SIZE_RULES(4) first too
(tools/mado-geometry.py:262-264). The new tool tests its exit-4 STALE_BLOCK
last, after NOT_COMPARED, DIFFER and NO_KEYBOARDS (mado-devices.py:410-419).
On a run with both `unsupported>0` and `stale>0`, family readers get
NOT_COMPARED from the new tool where the sibling tools would surface the
domain verdict. The device's choice is defensible (an unmodelled line could
create the very device a stale block names, so NOT_COMPARED is the safe
answer), but the position is a divergence.
Fix proposal: cheapest is one docstring sentence at mado-devices.py:87-89
giving the rationale; behavioural alignment (move STALE_BLOCK ahead of
NOT_COMPARED) is a contract change and should not be done this round.

**I4 — NO_KEYBOARDS(3) masks an all-agreeing mouse population (minor).**
With zero keyboards the verdict is NO_KEYBOARDS/3 even when every mouse AGREEs
and no stale block exists (mado-devices.py:414-415); the per-line
MADO_DEV_MOUSE lines still carry the answer. Monitors' analog NO_MATCHING_MONITOR(3)
has no second population to mask, so this is a new shape, not a violation.
Fix proposal: document, not change — keyboards==0 is a genuine "nothing to
compare on the primary plane" signal, and the frozen fixtures pin this map.

**I5 — `bad_json` now denotes three different schemas (minor, family-wide).**
Monitors/geometry: top-level list of objects; devices: object whose
`keyboards`/`mice` are lists of objects each with a string `name`
(mado-devices.py:30-33). Same reason word, three validations — fixture writers
must read each docstring. Noted for the ledger; no fix.

**Not new, for completeness:** geometry's config flag is `--rules` while
monitors/devices use `--config` (tools/mado-geometry.py:19-26) — pre-existing;
the new tool sides with the majority. And devices' `kb_file=<set|->` reports a
config-side fact the dump never carries, mirroring monitors' seen-but-not-compared
counters (v2=) — consistent, no action.

## 4. Ledger — considerthese 2026-10-26 proposal 2 (committed receipts only)

Every receipt below is a committed lane file (verified via `git ls-files` /
`git grep` at tip e0be61e4); no /tmp or scratch path is cited.

| tool | question it answers | last live run receipt | verdict |
|---|---|---|---|
| tools/mado-monitors.py | does each connected output run the mode/position/scale/transform its monitor rule declares? | .ufo/waves/round-45/receipts/live-monitors-host-r45.txt (2026-10-26T16:46:59-03:00) | OK, exit=0 — 1 output AGREE; selftest 48/48 |
| tools/mado-geometry.py | does the size a window rule asks for match the size the compositor reports? | .ufo/waves/round-44/receipts/live-geometry-host-r44.txt (2026-10-26T14:30:05-03:00) | NO_MATCHING_CLIENT, exit=3 (gkeep client not mapped at read time) |
| tools/mado-globals.py | which Wayland globals did the compositor advertise to its portal, per session/class? | .ufo/waves/round-41/w1/ExecLiveHost/live-census.txt (host 2026-10-25T20:02:07-03:00) | stable: live-diff rc=0 across 3 runs; --expect rc=1 by design (MISSING_EXPECTED probe) |
| tools/mado-eventq.py | who is subscribed to socket2, is anyone lagging, did the compositor drop anyone? | .ufo/waves/round-38/receipts/eventq-live.txt (taken 2026-10-25T11:00-03:00) | CLEAN, exit=0 — subscribers=2, overflow=0, write_fail=0, lagging=0 |
| tools/mado-options.py | does each declared config-tree option match the compositor's live value? | .ufo/waves/round-40/w1/ExecToolLive/live-host-census.txt (r40) | exit=0 — 70 rows: agreement=62, agreement*=8, mismatch=0 |
| l1-draft/mado-devices.py (r46 reference; lands as tools/mado-devices.py) | does each keyboard run the XKB names its config declares, and does each mouse report the scroll factor its device block sets? | .ufo/waves/round-46/receipts/live-devices-host-l1.txt (2026-10-26) | OK, exit=0 — keyboards 9 AGREE + 1 VIRTUAL (hl-virtual-keyboard-fcitx5); mice 4 AGREE |

Freshness note for the ledger if adopted: eventq and globals receipts are the
oldest (round-38 / round-41-era, >1 day); monitors, geometry and devices are
2026-10-26. Recording receipt age alongside the verdict (synergy with
proposal 3's age count) lets a reader see at a glance which tool is stale.

## 5 Verification-surface cross-check (seat SentTool, F1/F2)

Seat SentTool's safety review (findings.md:19-20, evidence
evidence/clause-r-bypass-*.txt) — confirmed by connector seat ConnCrossClaim
(harnessFindings.sentToolF1/F2, .ufo/waves/round-46/w1/ConnCrossClaim/report.md) —
shows the §1 "read-only boundary" column is a
**tool-side declaration** whose binding enforcement lives in the C1 counter's
sandbox(), not in the tool: clause r's no-hyprctl check is PATH-only (two
bypass tools scored TARGET_MET at nonce 46), and `--ro-bind / /` leaves the
live $XDG_RUNTIME_DIR Hyprland IPC socket reachable. Consequence for the
ledger: record the enforcement layer per tool so a reader does not conflate
"the tool starts no process" (mado-devices.py:34) with "the counter proved no
process ran". No change to the §3 inconsistencies — those are output-contract
level, independent of sandbox enforcement.

## 6. The one bounded move

Adopt proposal 2 as one committed artifact — e.g.
`corpus/knowledge/live-state-tool-ledger.md` — holding the §4 table plus two
lines of family invariants distilled from §3: (1) on a summary line, name the
exact counters that drive `verdict=DIFFER`; (2) state where the domain-empty
verdict sits in each tool's exit ladder. This improves operability (João can see
which read-only tool to run and what its last verdict was) and coverage (the
input-device plane gains its tool row) without touching the frozen C1/C2
counters — the ledger is routed non-claim work. Risks: none to scoring; the
only hazard is staleness, mitigated by the age note. Verification: all six
receipt paths re-checked as committed above; the two invariants are quoted from
the cited line numbers.

## Evidence index

- Reference contract: .ufo/waves/round-46/l1-draft/mado-devices.py:28-34,80-89,99,385-388,400-402,410-419,542,546-557
- Siblings: tools/mado-monitors.py:26,28,100-102,464-470; tools/mado-geometry.py:19-26,65-73,262-270
- Live-probers: tools/mado-globals.py:24,28,45; tools/mado-eventq.py:60-62,78-79; tools/mado-options.py:61-65,80
- Receipts: .ufo/waves/round-45/receipts/live-monitors-host-r45.txt; .ufo/waves/round-44/receipts/live-geometry-host-r44.txt; .ufo/waves/round-41/w1/ExecLiveHost/live-census.txt; .ufo/waves/round-38/receipts/eventq-live.txt; .ufo/waves/round-40/w1/ExecToolLive/live-host-census.txt; .ufo/waves/round-46/receipts/live-devices-host-l1.txt
- Proposal: considerthese/2026-10-26.md:48 (proposal 2)
- No tools installed; no packages touched; no git/jj mutation in the lane.
