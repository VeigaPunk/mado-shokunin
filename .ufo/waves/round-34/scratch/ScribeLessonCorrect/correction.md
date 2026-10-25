Draft for the L1: append to `corpus/lessons/round-32.md`. Append-only — no
existing line is edited. Dated entry in the lane's erratum style (house form:
`corpus/lessons/round-16.md` §"Erratum (round 17, append-only) — R16-V1").

## Erratum (round 34, append-only, 2026-10-24) — S189 queue-cap line

Superseded statement, line 73 (the S189 anchor set inside the **anchor**
bullet, written at `f5910876`): the re-derived staged anchors were published
as `:14`/`:21`/`:35`/`:126`/`:128`/`:129`. Read as the locator for the
client-queue cap, the line-128 anchor is false. `:128` is `formatEvent`'s
`eventString` assignment —

    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));

— not the queue cap. The queue-cap statement is at **line 169** of
`.ufo/waves/round-32/fetch/S189.bin` (sha256
`eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`, 6,479 B —
both re-derived 2026-10-24):

    const size_t MAX_QUEUED_EVENTS = 64;

The six anchors stay correct for the S189 registry row's own claims
(`corpus/SOURCES.md`, S189 row: `:126` `formatEvent`, `:128` the
1024-character truncation, `:129` the newline sanitisation); that row never
claimed the queue cap, and no admitted lane entry cites `S189:128` for it.
What is false is only the queue-cap reading of line 128. Evidence pointer:
the frozen round-34 calibration predicate PRED-C2-r34-v1
(`.ufo/waves/round-34/c2/frozen.json`, `.ufo/waves/round-34/registration.md`)
requires the last `r34-s189-line:` line to publish `line=169` and a card
tailing `line=128` prints TARGET_MISSED; the lane publishes
`r34-s189-line: line=169` at `SCORECARD.md:2108`. Line verification:
`.ufo/waves/round-34/w1/reports/ScoutS189.md` (seat) and
`.ufo/waves/round-34/w1/reports/RevC2Truth.md` (non-author re-check, sha and
both lines confirmed). Round-33's own admission location for the pending
queue-cap entry already read `S189 line 169` (`corpus/lessons/round-33.md`
Gate). Status-neutral for the round-32 anchors and the registry row.
