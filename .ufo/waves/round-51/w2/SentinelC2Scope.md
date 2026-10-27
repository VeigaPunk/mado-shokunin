# SentinelC2Scope — safety/provenance audit of the C2 entry and fetch directory

Seat: SentinelC2Scope (sentinel attack), round 51 w2.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round base `6ca8c559a4a3d6d361101592116eea2bc7452437`; freeze `56026fcb9800370ae04bc65952a6567181c398d0`;
C2 data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`.

Scope attacked: `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, the S364–S369 rows,
the README index row, `quality/counters/c2-r51-dispatch-entry.py`, `corpus/lessons/round-51.md`,
and all 21 files under `.ufo/waves/round-51/fetch/`. No frozen predicate, counter, lane file or
gate decision was edited; every write is inside this seat's directory.

## Verdict

- **PRED-C2-r51: PASS** on the scope/provenance surface, as frozen. Data rev reproduces
  `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387…`, exit 0;
  base reproduces `admitted=0/1 verdict=TARGET_MISSED`, exit 1. Receipts
  `SentinelC2Scope/receipts/c2-counter-{data,base}.txt`.
- **Session-material gate: PASS on the C2 surface.** Whole-tree run at the data rev:
  `SESSION_MATERIAL: files=24477 findings=241 rev=a0e34387…`, exit 1; none of the 241 findings
  names any round-51 path (the gate's `grep round-51` is empty). Scoped rerun on a 26-file
  snapshot of exactly the C2 artifacts: `SESSION_MATERIAL: files=26 findings=0`, exit 0.
- **Upstream provenance: PASS.** All 19 pins were independently re-fetched today from their
  commit-pinned `raw.githubusercontent.com` URLs and are byte-identical (sha256) to the
  committed pins; all 19 `git_blob_sha1` values match `git hash-object` over the committed
  bytes; the entry's 15-item digest paragraph has 0 mismatches. `receipts/upstream-verify.txt`,
  `receipts/hash-audit.txt`.
- **Advisory defects: S1 (medium) and S2 (low)**, neither of which defeats a frozen clause.

## Findings

### S1 — MEDIUM: committed `fetch/SHA256SUMS` carries a self-row; `fetch-manifest.json` says it does not

- Evidence: `.ufo/waves/round-51/fetch/SHA256SUMS:17` is
  `ab6c7355…  .ufo/waves/round-51/fetch/SHA256SUMS`, while the blob's actual sha256 at
  `a0e34387` is `700fea66…`. `sha256sum -c` on the materialized data-rev dir prints exactly one
  `FAILED` row (the self-row) plus `WARNING: 1 computed checksum(s) did NOT match`; all 19 pin
  rows are `OK`. `fetch-manifest.json` simultaneously claims
  `"sums_self_row": "none — SHA256SUMS digests pins only (M50-9/D4 rule)"`.
- Impact: the lane's routed D4/M50-9 fix is not present in the committed artifact — the
  integration that re-pathed the checksum manifest at freeze `56026fcb` re-introduced the
  self-row the w1 receipt (`ExecFetchDispatch/receipts/verify.txt` §3, `self_row_lines=0`)
  and the seat generator (`fetch-all.sh` exit 6) were built to prevent. `sha256sum -c` is
  therefore permanently red by one expected row, which destroys its use as a tamper check for
  the pins and makes the manifest's own `integrity`/`sums_self_row` fields false provenance.
- Exploit path: a local reader or future gate runs `sha256sum -c` and learns to ignore the
  single known failure; a later edit to any pin then hides behind the expected red line. No
  privilege is involved; the trust boundary is the lane's own provenance record.
- Smallest remediation (future amendment, not applied here): regenerate the committed
  manifest over the 19 pins only (no `SHA256SUMS`/`fetch-manifest.json` rows), commit the
  `sha256sum -c` exit-0 receipt, and set `sums_self_row` to the truth. Do not change
  PRED-C2-r51: the frozen sentence never promises checksum verification, so this is not a
  claim miss.

### S2 — LOW: host-local scratch path in the lesson (C1 line, not C2)

`corpus/lessons/round-51.md:24` embeds `--work /fast/scratch/hyaku/mado-r51/L1/c1-freeze`.
No account name, session data or secret; the gate does not model `/fast/…` (R4/R7 cover
`/home/<user>/…`), and the C2 entry/fetch/counter carry no `/home/`, `/tmp/`, `/run/user/`
or drive-letter paths at all. Mask to `<scratch>` on the next touch.

### S3 — INFORMATIONAL: fetch dir is a superset of the entry's pin table

The entry's pin table names 15 of the 19 pins; the extra `Hyprland-ConfigManager.hpp`,
`Hyprutils-VarList2.hpp`, `wiki-Binds.md` (held S359 page) plus `SHA256SUMS`/`fetch-manifest.json`
are supporting material. Every pin the entry names exists; nothing cited is missing.

## Negative results (checked, nothing found)

- No session/personal material in the C2 scope: no client dumps, monitor identifiers, serial
  shapes, home listings, account columns or serial prose (whole-tree and scoped gate runs;
  zero round-51 paths among the 241 pre-existing findings).
- No host process tables (`users:((` absent), no credential-shaped values
  (`gh*_`, `github_pat_`, `sk-`, `AKIA`, `xox*`, private-key blocks, bearer/authorization
  values absent), no `/home/<user>` path in the entry, fetch dir, counter or README row.
- No unpinned URL: 19/19 fetch URLs and all 6 entry source URLs are pinned to 40-hex commits.
- Province: Hyprland/hyprutils source and the English upstream wiki are the config-plane /
  compositor documentation ground; no localized-documentation channel, no socket connected,
  no runtime dispatch performed (source read only, per the round-38 addendum).
- No round-51 synthetic-material sidecar or waiver-registry row exists; the gate needed none.

## Deliverables

- `Report: .ufo/waves/round-51/w2/SentinelC2Scope.md` (this report)
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/source-scope.md` (full audit + full verdicts pasted)
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/session-material-all.txt`
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/session-material-c2scope.txt`
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/hash-audit.txt`
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/url-audit.txt`
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/upstream-verify.txt`
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/secret-scan.txt`
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/c2-counter-data.txt`
- `Report: .ufo/waves/round-51/w2/SentinelC2Scope/receipts/c2-counter-base.txt`

## Checks the integrator should run

1. `sha256sum -c .ufo/waves/round-51/fetch/SHA256SUMS` at the data/integration rev — expect the
   single self-row failure until S1 is fixed.
2. `TMPDIR=<scratch> python3 -I quality/check-session-material.py --repo <lane> --rev <tip> --scope all`
   before committing — existing 241 findings are pre-existing; require no new round-51 path.
3. The frozen counter at the integration tip, to confirm the data-rev line still holds there.
