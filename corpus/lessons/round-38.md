# Lessons — mado, round 38

Round intent (frozen in `.ufo/waves/round-38/registration.md`): three claims —
**C1** (v3 re-grounding counter discriminating the round-37 v2 cribs), **C2**
(request-socket admission across three adopted package entries), **C3**
(the live triplet closing the v3 `live` clause). The 19-control frozen
manifest `.ufo/waves/round-38/controls/manifest.json` is applied and replayed
by `quality/check-r38-discrimination.py`.

## Gate

GATE S158 receipt=.ufo/waves/round-38/fetch/S158.bin sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote="int ret = poll(pollfds, 1, 5000);"
GATE S187 receipt=.ufo/waves/round-38/fetch/S187.bin sha256=136e5511fba5524a5cb1685668429ee28f7a2710c70104441eeb2b674f6a37a4 quote="evaluates connections to this socket completely synchronously"
GATE S221 receipt=.ufo/waves/round-38/fetch/S221.bin sha256=35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a quote="select instance (id or index in hyprctl instances)"
GATE S253 receipt=.ufo/waves/round-38/fetch/S253.bin sha256=3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf quote="static constexpr size_t REQUEST_LIMIT      = 1024 * 1024;"
GATE S258 receipt=.ufo/waves/round-38/fetch/stat-sockets.txt sha256=fcc608203f66879f469b61761619e555e04b67127f215d495bd35b9b27421928 quote="directory /run/user/1000/hypr/"
GATE S277 receipt=.ufo/waves/round-38/fetch/S277.bin sha256=ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6 quote="There is no length prefix or newline."

Every quote is verbatim in its receipt bytes and in the citing entry body.
S158's quote is its v0.56.2 accept loop's timeout (the live bound);
S187's is the synchronous-evaluation sentence; S221's is the `i` flag
description inside `flag list:` (the `>` arrow is `&gt;` in the HTML);
S253's is the request ceiling constant; S258's names the measured object;
S277's is the third-party grammar corroboration.

## Assimilation ledger — shokuknow, `merge/mado/`

Staged table: 5 knowledge entries + register + 147-row `SOURCES.append`.
This round adopted the three usable knowledge entries and refuses the other
three (r30 included), per the frozen registration:

| Staged id | Package source | Decision | Lane row / entry |
| --- | --- | --- | --- |
| S221 → S221 | 0.56.0 hyprctl page | adopt — verbatim re-fetched | S221, `hyprctl-flags-r28.md` |
| S272 → S158 | HyprCtl.cpp at tag v0.56.2 | adopt — byte-identical to held S158 at the same commit | S158 (used-by + r8) |
| S276 → S187 | 0.56.0 IPC page | adopt — byte-identical to held S187 | S187 (used-by + r8) |
| S277 → S277 | chonkstep docs | adopt — community tier C | S277, `request-socket-live-bound-r8.md` §2 |
| S253 → S253 | upstream `ipc/s1/Unix.cpp` | adopt — first-party code at a later revision | S253, `request-limits-upstream-r31.md` |
| (package own-work stat receipt) → S258 | own-work stat receipt | adopt — host measurement re-taken this round | S258, `request-socket-live-bound-r8.md` §2 |
| (new) | event-queue-host-measurement-r28.md | **refuse** — "never overflowed" leans on a null channel (debug:disable_logs=1); corrected by round-37's event-queue-observability-r37.md | none |
| (new) | event-queue-journal-measurement-r29.md | **refuse** — same null channel; its journal reading (21 core-logger lines, zero markers) is observability-r37.md's measurement | none |
| (new) | socket-client-contract-measurements-r29.md | **refuse** — "requests capped at 64 KiB" is chonkstep's own request cap (S277 `:61`), not upstream's follow-queue bound; its socket census is superseded by S258's stat and round-37's live census | none |
| (new) | socket-modes-and-request-read-r30.md | **refuse** — frozen registration declines the package's successor chain; the request-socket facts are covered by the adopted S158/S187/S253 entries | none |

Id collisions: 15 of 147 staged ids (S203–S217) conflicted with held rows
(their entries span ipc-contract/dispatcher/waybar and two literature amendments,
not only the refused register block). A 16th id clash is unrecorded yet:
staged S258 is the English ArchWiki drift document (unadopted); the lane's
S258 is this round's host stat receipt — same id, disjoint documents. The four
adopted new lane ids (S221, S253, S258, S277) were free against held rows. The staged register is left unassimilated (its rows
covered only the refused entries).

## Findings — open items for round 39+

1. **The two counters still read committed bytes only.** Both v3 counters
   score a repository revision; a crib committed at `rev` cannot pretend the
   current entry `lineage=... ok` numbers away. That is by design — but the
   live clause's triplet is also committed bytes, so the counters' own
   receipts must be regenerated every round the instance dir rolls
   (`/run/user/1000/hypr/<HIS>_<epoch>_<rand>/`). `before-c2.txt` was taken
   at the freeze commit; the round's own `live` clause replays the committed
   receipts.
2. **`hyprctl i` on this host.** The documented `i` flag exists; whether the
   host's own scripts (waybar idle-indicator, omarchy menus) ever issue a
   flagged request was not inspected — an explicit UNK in
   `hyprctl-flags-r28.md` §3.
3. **S218–S220 remain unclaimed.** The register skips S218–S220 entirely
   (held rows jump S217 → S221); a future round whose sources need them may
   take them.
4. **`hyprctl --help` flagged-request sweep** (quarantine item, register
   §Refused): the package's shell-history census claimed `hyprctl` requests
   with `j/` prefixes exist in `~/.zsh_history`; that file was not opened —
   it is outside this lane's own-work boundary this round.
5. **The `has-tool` discipline is per-path, not per-binary.** C2's
   `tool_present` clause checks `tools/mado-eventq.py` exists at `rev`; a
   rename or a sibling tool would need the clause re-pinned.

## Mistakes

- Freeze-discipline failure (RevCommitChain F1-F3): the C1 counter (859d0cf)
  and the discrimination manifest (b6c1d31) were patched after the freeze. The
  claim as frozen fails its own instrument contract; the landed pair is a new
  predicate routed for a re-registration ruling. Refined by the wave's replays:
  frozen instruments x frozen manifest = 19/19 at the freeze rev (the c1-duprow
  control's `append` landed outside `## Registry`), 18/19 under HEAD instruments x
  frozen manifest, 19/19 under the repaired pair.
- The frozen registration refused `socket-modes-and-request-read-r30.md`'s
  successor chain as a package entry; the ledger above records the three refusals
  explicitly (r28, r29 journal, r29 socket-client) - earlier LOG wording said
  "two" and is corrected.
- S258 was cited in r8's body but omitted from its `source:` header at data time;
  the counter's per-id clauses therefore did not enforce it (RevDomCounter). Fixed
  at `b8400aa7` after the counter admitted 3/3 with the hole open.
