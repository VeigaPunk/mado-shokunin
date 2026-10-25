# ScribeEntryStall — re-draft of `event-delivery-limits-r26` with corrected source ids

Seat: scribe (round-33 w1). Lane: mado-shokunin. Worked alone — leaf member,
no subagent dispatch per wave instructions.

## Outcome

Drafted `.ufo/waves/round-33/scratch/ScribeEntryStall/event-delivery-limits-r26.md`
(8,420 B). Sources: **S189** (`src/managers/EventManager.cpp` at `v0.56.2`,
commit `efb50993…`, round-32 fetch blob re-opened) and **S197** (Waybar
`0.15.0` `src/modules/hyprland/workspaces.cpp`, round-33 fetch blob). The
queue cap is cited to **S189**, not campaign S187 — per the wave instruction
and round-32 M32-12/M2 review residue (the old draft's S187/S188 were `+2`
renumbering drift). The bar-backend claims the old draft made on S188/S190
are bounded out as UNK rather than re-attributed, since the round-33
registration requires only S197+S189 for this entry
(`.ufo/waves/round-33/registration.md`).

Contents: producer-side limits (§1: 1024-char truncation, per-client queue of
**64**, disconnect-on-overflow — removal not throttling), consumer-side
registration (§2: `registerIpc` S197:803-829, 14 calls, `workspacev2` first at
:804, shared `IPC::inst()` at :21, destructor unregister :37), UNK ledger
(§3), repeatable-observation block (§4), Gate with both required
`gate-quote:` lines verbatim plus the provenance table.

## Evidence re-run at write time

```sh
$ sha256sum .ufo/waves/round-32/fetch/S189.bin .ufo/waves/round-33/fetch/S197.bin && wc -c ...
eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d  S189.bin   6479 B
1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9  S197.bin  41392 B
```

Both digests **equal** `c1/frozen.json` (S189/S197 entries). S197's digest
also matches ScoutS197's independent fresh fetch.

```sh
$ grep -c 'MAX_QUEUED_EVENTS' S189.bin        # → 2  (def :169, use :174)
$ grep -c 'm_ipc\.registerForIPC' S197.bin    # → 14 (:804-:827; excludes unregisterForIPC :37)
$ grep -n 'm_ipc(IPC::inst())' S197.bin       # → 21
$ git ls-remote https://github.com/hyprwm/Hyprland 'refs/tags/v0.56.2'
efb50993780079460b0cbed1363e2166a2de1d9f  refs/tags/v0.56.2   # lightweight, no ^{} peel line
```

Line anchors pinned by grep this seat: S189 `formatEvent` :126-133
(truncation :128-129), `flushClient` :133-161 (`EAGAIN` keep :149-150,
`writeOffset` :136-145), `postEvent` :163-191 (cap :169, overflow-check :174,
ERR "overflowed event queue, removing" :175, `removeClientByFD` :176,
`push_back` :180, `WRITABLE` arming :187-188).

## Gate-quote verification

- `gate-quote: S197 m_ipc.registerForIPC("workspacev2", this);` — contiguous
  substring of S197.bin at line 804; 3 quoted words (≤25 bound).
- `gate-quote: S189 const size_t MAX_QUEUED_EVENTS = 64;` — contiguous
  substring of S189.bin at line 169; 6 quoted words.
- `grep -F` literal-substring check: both quoted strings found in their
  blobs; both `gate-quote:` lines found verbatim in the draft.

## Kept unknowns (per instruction)

- Whether this host **ever hit the 64-event cap**: unobserved — no socket,
  no logs, no processes inspected. Overflow-removal is mechanism, not
  witnessed occurrence.
- Whether Waybar's IPC backend (campaign S190) readmits a dropped client:
  deferred — S190 is outside this entry's required source set.
- Installed bar version vs pinned `0.15.0` tag: not interrogated this round.

## Bounds kept

- No write under `corpus/` — scratch draft only; adoption/`used-by` appends
  belong to the closure/adoption path, not this seat.
- No LOG.md append — wave-scoped artifact; the round rollup is the L1's
  (precedent: r32 scribe seats logged via `w1/reports/` only).
- Nothing else mutated: `git status` outside `.ufo/waves/round-33/{scratch/ScribeEntryStall,w1/reports}` untouched.

## Residual

The draft is staged, not admitted: it still needs non-author review per the
protocol before any corpus adoption, and the S190 backend question must be
resolved by whichever entry re-grounds that row.
