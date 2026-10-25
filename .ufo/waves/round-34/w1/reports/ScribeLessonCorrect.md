# ScribeLessonCorrect — draft erratum for the S189 queue-cap line

Scope: draft an append-only, dated correction to `corpus/lessons/round-32.md`
(the lane's own lesson) naming the correct S189 queue-cap line. The L1
appends; this seat wrote no lane record.

## Deliverable

- `.ufo/waves/round-34/scratch/ScribeLessonCorrect/correction.md` — the
  erratum text, in the lane's house style (`## Erratum (round 34,
  append-only, 2026-10-24) — S189 queue-cap line`, modeled on the round-16
  §"Erratum (round 17, append-only) — R16-V1" form: superseded text named,
  measured replacement, evidence pointer, status note).

## Verified facts (re-derived this session, not copied)

- `corpus/lessons/round-32.md:73` — inside the **anchor** bullet: S189's
  re-derived anchors are published as
  `:14`/`:21`/`:35`/`:126`/`:128`/`:129`.
- `.ufo/waves/round-32/fetch/S189.bin:169` reads
  `    const size_t MAX_QUEUED_EVENTS = 64;` — the queue cap.
- `.ufo/waves/round-32/fetch/S189.bin:128` reads
  `    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`
  — `formatEvent`'s assignment, a different statement.
- Fetch integrity confirmed by `w1/reports/ScoutS189.md` and
  `w1/reports/RevC2Truth.md`: sha256
  `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`,
  6,479 B, 192 lines.
- `SCORECARD.md:2108` publishes `r34-s189-line: line=169` (sole match);
  PRED-C2-r34-v1 is frozen in `.ufo/waves/round-34/c2/frozen.json` and
  `registration.md:41`; a `line=128` card prints TARGET_MISSED.

## Precision note carried into the draft

The six line-73 anchors are each individually correct for the S189 registry
row's own claims (`corpus/SOURCES.md:201`: `:126` formatEvent, `:128`
1024-character truncation, `:129` newline sanitisation). No admitted lane
entry cites `S189:128` for the queue cap — grep of `corpus/knowledge/`
finds the queue-cap claim only in the still-unappended staged entry
`event-delivery-limits-r26.md`, which round-33 (`corpus/lessons/round-33.md`
Gate) already located at `S189 line 169`. The draft therefore states the
falsehood narrowly: the queue-cap reading of line 128 is wrong; the queue
cap is `:169`. The six anchors and the registry row are kept status-neutral
rather than rewritten.

## Bounds observed

- `corpus/lessons/round-32.md` not edited — lessons are append-only and the
  L1 owns the append.
- No other lane record touched; leaf member, no subagents dispatched.
