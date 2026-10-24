# ScribeEntryDispatchers — re-grounded draft for `dispatcher-semantics-r25.md`

Leaf scribe; no subagents dispatched. Read-only inputs: the staged package
entry and the `ScoutDispatchersWiki` seat report (S188 re-open). Writes: this
report + the scratch draft only. `corpus/` untouched.

## Deliverable

Draft written to
`.ufo/waves/round-32/scratch/ScribeEntryDispatchers/dispatcher-semantics-r25.md`
— as it should land in `corpus/knowledge/dispatcher-semantics-r25.md` (landing
is the L1's job, not this seat's).

Contract shape: provenance trio first (`source:` S188 with URL + `# Dispatchers`
anchor + wiki commit; `verified-at:` 2026-10-24; `recheck:` 90d + sha256
prefix, re-run at write time), every claim carries its S-id, `## Gate` block
with URL + access date 2026-10-24 + 18-word located quote (S188:9), explicit
unknowns kept.

## Write-time verification (re-run, not copied)

Against `.ufo/waves/round-32/scratch/ScoutDispatchersWiki/dispatchers.md`:

- `sha256sum` → `c830ce0717f92776f03a977506141c549705aebe4e738ce801faddaa7b2d7d14`;
  prefix matches the staged entry's recheck expectation `c830ce0717f92776`. 12879 bytes.
- Line anchors all confirmed by `grep -n` on the bytes: instability quote → L9;
  `hl.dispatch()` wrapper sentence → L14; "Simply writing `hl.dsp.whatever()` …
  will do nothing" → L15; `event( string ) | Send an event to socket2` → L59;
  `force_idle( int )` full cell → L69; DPMS/force_idle keybind warning → L82.
- §4 recheck re-run: `grep -c 'hl.dispatch'` → `7` (expectation "1 or more" met).

## Deltas vs the staged entry (all from the scout's flags)

1. `force_idle` quote completed: staged quoted only the first sentence of the
   L69 cell; the draft quotes the full cell including "Timers return to normal
   behavior upon the next activity. Do not use with a keybind directly!" — the
   clauses the scout flagged as load-bearing for the §2 INF. The INF now cites
   the full cell (next-activity termination added).
2. Added one OBS (S188:15, bare call does nothing) — located by the scout as
   the supporting line for item (1); verified in the bytes.
3. `dpms` row located (S188:58) for its inline "Do not use with a keybind
   directly!" clause, which the warning at S188:82 repeats.
4. UNK re-scoped to what S188 supports: the bytes pin a wiki commit, no 0.56.x
   marker, so the shipped-v0.56.2 dispatcher surface stays unverified; the
   "0.56.0 page not fetched" meta-claim is replaced by "outside this entry's
   source set" (a sibling seat's 0.56.0 fetch exists in wave scratch but is not
   an input to this draft). Unknown preserved, `CANNOT-ANSWER.md` pointer kept.
5. Recheck/verified dates advanced to 2026-10-24 with the observed values;
   instability scope (dispatcher contents, not the wiki page) stated explicitly.

No staged claim was contradicted by the re-opened bytes; no claim in the draft
goes beyond them (INFs are marked INF with byte basis; UNKs marked UNK).

## Theme verdict: different surface, one bridge row

The round's ONE theme (registration, C1) is the Hyprland IPC two-socket
contract. **This entry's subject is a different surface.** Reasoning from the
two files:

1. Every claim in the staged entry — and everything the scout located for it —
   is about the Lua dispatcher API: describe-vs-execute semantics (S188:9,
   S188:14, S188:15), per-dispatcher behavior (`event` S188:59, `force_idle`
   S188:69, `dpms` S188:58, keybind warning S188:82), and contents instability
   (S188:9). None of it is socket-level: no request grammar, no `EVENT>>DATA`
   framing, no event catalogue, no truncation/sanitisation rule appears in the
   S188 claims or in the re-opened bytes.
2. The single touchpoint is one table row: `event( string )` — "Send an event
   to socket2" (S188:59). It names socket2 as a destination for a Lua-level
   dispatcher, but carries no wire semantics. The two-socket contract (socket1
   request grammar, socket2 event framing) is the subject of the sibling
   `ipc-contract-r25.md` entry, not of this one.
3. So: adjacent, not identical — the dispatcher API is the config-layer action
   surface with exactly one documented bridge row into socket2, while the IPC
   two-socket contract is the protocol surface itself. Both sit inside the C1
   theme package (this entry is one of the 3 assimilated knowledge entries),
   which is why it rides the theme wave; the surfaces it documents are not the
   same surface.

## Blockers

None. If the L1 wants the 0.56-versioned dispatcher surface grounded, the
`ScoutDispatchers0560` seat's output is the input to request — outside this
entry's S188 re-open.
