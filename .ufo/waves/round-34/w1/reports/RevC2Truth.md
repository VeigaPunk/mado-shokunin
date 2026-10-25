# RevC2Truth — round-34 calibration claim ground-truth verification

Scope: verify the `r34-s189-line` claim's ground truth against
`.ufo/waves/round-32/fetch/S189.bin` and confirm the scorecard publication.

## Verdict: claim CONFIRMED (sha + line=169 both check out)

## 1. Hash

    $ sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/fetch/S189.bin
    eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/fetch/S189.bin

Matches claimed `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`. CONFIRMED.

## 2. Line contents (verbatim, `sed -n '128p;169p'`)

    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));
    const size_t MAX_QUEUED_EVENTS = 64;

- Line 169 strip-equals `const size_t MAX_QUEUED_EVENTS = 64;` — CONFIRMED
  (source line is `    const size_t MAX_QUEUED_EVENTS = 64;`; stripped of leading
  whitespace it equals the claimed literal).
- Line 128 does NOT strip-equal it — CONFIRMED (it is the `std::format` line above).
- Line-169 context (read range 164–171): the constant sits inside the event-dispatch
  block after the `m_isShuttingDown` guard, immediately before
  `makeShared<std::string>(formatEvent(event))` and the `m_clients` loop.

## 3. Scorecard publication

    $ grep -n 'r34-s189-line' /home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md
    2108:r34-s189-line: line=169

- Exactly one matching line (count=1): `SCORECARD.md:2108`.
- The LAST (and only) such line publishes `line=169` — YES.
- Caveat, stated at claim: this key does not exist in the fleet-root
  `/home/vgpnk/Projects/shokunin/SCORECARD.md` (grep -c = 0 there). The publication
  is lane-local only, in `mado-shokunin/SCORECARD.md`. The claim is accurate as long
  as it is read against the lane scorecard.

## Summary

| Check | Result |
|---|---|
| sha256 of S189.bin | CONFIRMED `eea605df…9540d` |
| line 169 == literal | CONFIRMED |
| line 128 != literal | CONFIRMED |
| last `r34-s189-line` publishes line=169 | CONFIRMED (`SCORECARD.md:2108`, sole match, lane-local) |
