RECEIPT tool=/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py tool_sha256=367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d utc=2026-10-20T18:01:27Z argv=/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --scan inputs/r15-libinput-events.jsonl inputs/r13-global-capture.jsonl inputs/r14-review-source-bar.jsonl inputs/r14-source-safety.jsonl inputs/r13-root.jsonl

# Frozen tripwire replay (re-pinned)

Re-pinned from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen` (source expected.json sha256 `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`) by the
round-19 regenerator `.ufo/waves/round-19/frozen-repin.py`. The scan on the
RECEIPT line ran over the relative `inputs/...` paths with cwd = this
directory's staged copy (byte-identical; published by one rename after the
replay below). `expected_findings` is the tool's own output on these bytes.

A frozen baseline proves these bytes still draw this verdict *from this tool
digest*. It does not prove the tool classifies the original incident
correctly: the source pin carried the committed receipts' claim, and this
re-pin keeps that claim only as its refusal rule - no source expected finding
may disappear, and no finding may land on a line that was neither expected
nor a known miss (unless it was regenerated with `--allow-new-findings`).

Replay during re-pin (staged copy, same tool):

    MADO_TRIPWIRE_FROZEN: frozen_match

Verify this directory: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen`
Re-pin: `python3 -I .ufo/waves/round-19/frozen-repin.py --from /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen --to /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`

## Inputs (byte-exact copies, digest-verified against the source pin)

| path | bytes | lines | sha256 |
|---|---|---|---|
| `inputs/r15-libinput-events.jsonl` | 11475 | 5 | `7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90` |
| `inputs/r13-global-capture.jsonl` | 14953 | 5 | `265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9` |
| `inputs/r14-review-source-bar.jsonl` | 34025 | 5 | `4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232` |
| `inputs/r14-source-safety.jsonl` | 28572 | 6 | `8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1` |
| `inputs/r13-root.jsonl` | 47931 | 5 | `24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11` |

## Verdict

- scan: `findings`, exit 1, unpermitted 11
- findings: 11 {"host_mutation": 6, "live_probe": 1, "package_query": 4}
- expected_findings: 11
- known_misses kept: 0; dropped as now-detected: inputs/r14-source-safety.jsonl:2, inputs/r14-source-safety.jsonl:3, inputs/r13-root.jsonl:4
- findings on lines that were neither expected nor a known miss: 0

## Provenance

`provenance.json` is the source object with a `repinned_from` note appended
(an existing note is kept and becomes a list). Any `tool_receipt_sha256`
already present still names the receipt the *original* findings came from;
the tool digest that produced this baseline is on the RECEIPT line above.
