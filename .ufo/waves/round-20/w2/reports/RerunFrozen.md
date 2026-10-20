# RerunFrozen — partly falsified: expected frozen verdicts hold, but frozen keys miss evidence-classification drift

## P2 — Frozen comparison does not guard the `evidence` field

Yes: the `(file, line, class, rule)` frozen key hides evidence changes. The current scanner emits `evidence` on every finding (`tools/mado-tripwire.py:2067-2075`) and summarizes observed/lead counts (`tools/mado-tripwire.py:2114-2120`), but frozen comparison constructs keys from only those four fields (`tools/mado-tripwire.py:2438-2446`). Round-19's actual replay has 10 observed findings and one lead; the lead is `inputs/r13-root.jsonl:4`. That distinction is an observable Round-20 precision result, not just provenance metadata.

I verified the blind spot with a controlled copy under `/tmp` only. I copied the Round-19 frozen directory (original `expected.json` SHA-256 `50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435`) and changed the expected evidence value for its first finding (`inputs/r15-libinput-events.jsonl:1`, `host_mutation` / `sudo`) to `"lead"`; the unchanged replay emits that row as `"observed"`. The deliberately contradictory expected file had SHA-256 `2e5426786369b077a8199b44bc6cd451f1b6a5954fe8a78623be50ca7e9c28b4`, yet:

```text
python3 -I /tmp/mado-r20w2-RerunFrozen/tools/mado-tripwire.py --frozen /tmp/mado-r20w2-RerunFrozen/frozen-evidence-probe
MADO_TRIPWIRE_FROZEN: frozen_match
{"exit": 0, ... "tool_sha256": "9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c"}
evidence_probe_exit=0
```

The evidence value is therefore not asserted by frozen baselines: an observed↔lead drift at a pinned key can pass. If evidence labels are part of the claimed contract, frozen specs/comparison need to pin and compare them. This is a coverage gap; the probe does not claim that the unmodified Round-19/18 copies themselves differ in evidence.

## Replay results

- Tool was copied from commit `28c6837` into `/tmp/mado-r20w2-RerunFrozen/tools/mado-tripwire.py`; SHA-256: `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.
- `python3 -I /tmp/mado-r20w2-RerunFrozen/tools/mado-tripwire.py --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen` returned `MADO_TRIPWIRE_FROZEN: frozen_match`, exit 0, with no missing/extra findings; expected JSON SHA-256 `50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435`. All five input pins reported `ok: true`.
- `python3 -I /tmp/mado-r20w2-RerunFrozen/tools/mado-tripwire.py --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen` returned `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`, exit 1, with no missing findings and exactly three extras: `inputs/r13-root.jsonl:4 package_query/pacman:-Q`, `inputs/r14-source-safety.jsonl:2 package_query/pacman:-Q`, and `inputs/r14-source-safety.jsonl:3 package_query/pacman:-Q`. All five input pins reported `ok: true`; expected JSON SHA-256 `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`.
- `--scan` over either frozen `inputs/` directory returned 11 findings: 10 observed, one lead (the lead at `r13-root.jsonl:4`). Both snapshots have the same five pinned input digests, so the round-18 mismatch is the expected additional detections, not input drift.

## Limits

This report covers the requested frozen replays and their evidence-key behavior only. The available tool inventory exposes no `lsp` device, so no LSP status/references/definition/diagnostics calls were available or used; no caller-coverage claim is made. No pacman/device/service/compositor commands were run. The contradictory-evidence experiment changed only an isolated `/tmp` copy, not lane files.

## Installs

none
