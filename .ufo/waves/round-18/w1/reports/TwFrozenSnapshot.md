# TwFrozenSnapshot — round-18 frozen tripwire snapshot

## Artifacts written (only these)

Root: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen-tripwire/`

| path | bytes | sha256 |
|---|---:|---|
| `inputs/r15-libinput-events.jsonl` | 11475 | `7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90` |
| `inputs/r13-global-capture.jsonl` | 14953 | `265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9` |
| `inputs/r14-review-source-bar.jsonl` | 34025 | `4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232` |
| `inputs/r14-source-safety.jsonl` | 28572 | `8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1` |
| `inputs/r13-root.jsonl` | 47931 | `24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11` |
| `expected.json` | 3011 | `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9` |
| `provenance.json` | 4766 | `4fb06b6e42b52d5cb04e6ef8a19b36c2a8851a7bbd47e28e1c846f8941ff6310` |
| `README.md` (20 lines) | 1646 | `32bce204f9aa1f2dadcd535c7b58f8b4f65650bc7ab8a4b0810d8d8255f59e21` |

Input total 136,956 bytes (< 900 KiB). No other file was created or modified in the lane; no git/jj write was performed.

## Selection (source line → snapshot line, 1-based)

Sources under `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/`.

- `MadoR15/MadoR15.LibinputEvents.jsonl`: 54→1 (finding, R15-V1 anchor `call_38165`), 83→2, 86→3, 123→4, 158→5 (clean bash controls).
- `MadoR13/MadoR13.GlobalCapture.jsonl`: 19→1 (finding), 75→2, 78→3, 86→4, 107→5 (clean controls).
- `MadoR14/MadoR14.ReviewSourceBar.jsonl`: 41→1 (finding), 46→2, 54→3, 67→4, 95→5 (clean controls).
- `MadoR14/MadoR14.SourceSafety.jsonl`: 130→1, 158→4, 170→5, 186→6 (clean controls); 152→2, 155→3 (known misses).
- `MadoR13.jsonl`: 35→1, 94→2, 98→3, 506→5 (clean controls); 470→4 (known miss).

Every selected line is an assistant `message` record with at least one `toolCall`; every line is byte-exact including its newline, in source order. Each input is pinned to exactly one receipt scan (anchor receipt for R15; whole-round r13/r14 receipts otherwise), avoiding double counting.

## expected.json

`schema mado-tripwire-frozen-v1`, `permit: []`, `expected_exit: 1`, `expected_label: "findings"`; only the contract keys are present.

8 expected findings, all transcribed from the committed receipts:

- `inputs/r15-libinput-events.jsonl` line 1: `host_mutation sudo`, `host_mutation pacman:-S` — `tripwire-anchor-r15.txt`.
- `inputs/r13-global-capture.jsonl` line 1: `host_mutation sudo`, `host_mutation pacman:-S`, `live_probe wayland-info`, `package_query pacman:-Q` — `tripwire-r13.txt`.
- `inputs/r14-review-source-bar.jsonl` line 1: `host_mutation sudo`, `host_mutation pacman:-Sw` — `tripwire-r14.txt`.

Receipts were produced by tool `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072` (`tripwire-vs-oracles.json:tool_sha256`). The whole-round and anchor R15 receipts agree exactly on line 54.

3 known misses (asserted to yield no finding; a finding forces a re-pin):

- `inputs/r14-source-safety.jsonl` line 2 (source 152): variable `recipe` holds `pacman -Q hyprland ...` and is executed via `subprocess.run(['bash','-c',recipe])`; variable-held command text is not classified.
- `inputs/r14-source-safety.jsonl` line 3 (source 155): `recipe2 = recipe.replace(...)` re-executes the same variable recipe; no top-level literal pacman command exists.
- `inputs/r13-root.jsonl` line 4 (source 470): helper `run_record('packages',['pacman','-Q',...],0)` wraps the query; helper/argv calls outside `subprocess.*` are not classified.

Cross-check: `oracle-r13-r14.json` records no hit on SourceSafety 152/155 or MadoR13 470, and a `host_mutation` hit on GlobalCapture 19 / ReviewSourceBar 41; `oracle-r15.json:red_anchor` confirms LibinputEvents 54. The oracles undercount same-line concurrent calls: `tripwire-vs-oracles.json` lists GlobalCapture 19 `live_probe` and `package_query` as `tripwire_only`, so the expected multiset follows the receipt (the contract's authority), not the oracle.

## Skipped source (stated per item)

`MadoR14/MadoR14.OutputSpec.jsonl:65` is 792,861 bytes, exceeding the 256 KiB per-line copy limit; a byte-exact copy was impossible, so the OutputSpec anchor is absent and recorded under `provenance.json.skipped`. The wlr-protocols install remains covered by the R14 input (`pacman:-Sw`); `tripwire-pacmanlog-join.txt` also records that line as the cursor provider-history record whose call time, not record time, is the join key.

## Verification performed

- `sha256sum` of all six sources first, compared to `round-17/evidence/session-index.json`: all equal.
- Re-read every snapshot line against its mapped source line byte-for-byte (newline included), and re-hashed each input against both `expected.json` and `provenance.json`.
- Re-parsed every snapshot line as an assistant toolCall record; checked that findings, controls and misses are disjoint and that controls have no receipt or non-clean oracle hit.
- Sensitive-token scan (password/passwd/secret/token/api key/oauth/bearer/private key) over all snapshot bytes: no match. Operator home paths remain, as the lane already contains them and byte-exactness forbids redaction; the SentinelFrozenPrivacy seat has an advisory review pending.
- JSON validity of both metadata files; README line count 20.
- Independent check by MadoR18.FrozenProvenanceCheck against this exact tree: `MADO_FROZEN_PROVENANCE: match`, exit 0, 26 pairs across the five inputs, all five source sha256 equal to the round-17 index (index sha `06c259bc...`), 11/11 expected-finding and known-miss lines carried by a provenance pair, no unclaimed input; provenance sha256 `4fb06b6e42b52d5cb04e6ef8a19b36c2a8851a7bbd47e28e1c846f8941ff6310` recorded as the verified state. Falsification controls on a /tmp copy: one-byte flip → exit 1 `line_bytes_differ`; missing source → exit 2. `provenance.json` will not be rewritten unless a re-pin is required.

- End-to-end replay by MadoR18.TwFrozenMode against the landed `--frozen`: `MADO_TRIPWIRE_FROZEN: frozen_match`, exit 0, all 5 inputs `ok`, `missing_findings []` and `extra_findings []` (the 3 `known_misses` stay quiet), `scan_exit 1` / `scan_label findings`; `expected_sha256 4f3534ae...`, tool_sha256 `c87a31ef...` (the `--frozen` build; classification unchanged, as the receipt-derived multiset matched).

I did not run `--frozen` to derive or adjust any expected value; the mode owner's independent replay above is the end-to-end check. No lane gate, build, or formatter was executed by this seat.

## Risks / notes for L1

- If the TwMissBashCVar / TwMissHelperFn rule drafts are accepted into the tool, the three `known_misses` lines will start producing findings; `frozen_verdict_mismatch` is the intended signal and the snapshot must then be re-pinned (remove the fixed miss, update digests).
- `provenance.json` uses the canonical shape agreed with FrozenProvenanceCheck: `inputs[].path/sha256` + `sources[].{path,sha256,pairs}`; extra top-level `index`, `tool_receipt_sha256`, `skipped` are ignored by that checker.
- No tools were installed or upgraded; no package-manager, compositor, service, or transcript write was performed.
