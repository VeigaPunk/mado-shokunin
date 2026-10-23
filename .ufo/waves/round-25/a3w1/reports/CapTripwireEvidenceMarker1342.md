# CapTripwireEvidenceMarker1342 — C2 row re-run at 41cc04c8

## Ledger line

| SCORECARD.md:1342 | tripwire evidence marker | Tell an observed command from a lead on every finding row; drop provably pure data | fails at 41cc04c8: the row's literal command (REV 28c6837) exits 0 with P 66/66, L 17/18 (172/175) — a pinned historical reproduction; the same counter at 41cc04c8 exits 0 with P 66/66, L 15/18 (166/175, score 9.4857), three L lead cases return exit 0 with no findings | `cd <clone> && timeout 600 prlimit --as=4000000000 python3 -I .ufo/waves/round-20/tw-precision.py 28c6837` and `... python3 -I .ufo/waves/round-20/tw-precision.py 41cc04c8` | SCORECARD.md:1582 (round-24 status table: fails, L 15/18 at `8e5d9369`, round-21 harm H2 unrepaired); SCORECARD.md:1458 (L 15/18 at `a6cef89`) |

## Row under test

- Base revision `41cc04c8d593837a0d5078bffaacdaa163d12897`; `SCORECARD.md` is 1,618 lines at that revision, sha256:`6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08` (`git show 41cc04c8:SCORECARD.md | sha256sum`).
- The row sits in `### Capabilities (round 20)` (line 1338), inside `## Round 20 — committed results and bounded author verdicts` (line 1318).
- Row text, verbatim:

  `| tripwire evidence marker | Tell an observed command from a lead (argv stated, executing body not visible) on every finding row, and drop provably pure data | `python3 -I .ufo/waves/round-20/tw-precision.py 28c6837` (P 66/66, L 17/18); `tw-recall-split.py 28c6837` (5 observed + 1 lead) | 20 |`

- Stated capability: mark every finding row `observed` vs `lead` (argv stated, executing body not visible) and drop provably pure data.
- Demonstration commands: (1) `python3 -I .ufo/waves/round-20/tw-precision.py 28c6837`, stated result P 66/66, L 17/18; (2) `tw-recall-split.py 28c6837`, stated result 5 observed + 1 lead. The `tw-recall-split.py` form means `python3 -I .ufo/waves/round-20/tw-recall-split.py 28c6837` from the clone root (the script's own usage line: `usage: tw-recall-split.py REV`).
- Evidence pointer: inline numbers, no separate receipt path.

## Sandbox re-run

Clone preparation (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireEvidenceMarker1342
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireEvidenceMarker1342 checkout -q --detach 41cc04c8
```

Observed: `HEAD=41cc04c8d593837a0d5078bffaacdaa163d12897`, `git status --porcelain` line count 0. All runs below were made in this clone, never in the lane.

Bytes exercised (from the clone's git objects):

```text
bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7  .ufo/waves/round-20/tw-precision.py  (at 28c6837 and at 41cc04c8: identical)
5c8f1424833de506f8f839164ff284614ed5080b6015cf615b61b31e30bc7956  .ufo/waves/round-20/tw-recall-split.py
9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c  tools/mado-tripwire.py at 28c6837
cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84  tools/mado-tripwire.py at 41cc04c8 (round-23 restoration; matches the `cd9da20c…` restore named in SCORECARD round 23)
```

The counter's suite pin is `f3da50488661509ce5d144c90f7780f8088e0903` in both runs; the suite lives at `.ufo/waves/round-20/precision` at base.

Run A — the row's command as written (pinned to `28c6837`):

```sh
cd /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireEvidenceMarker1342
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 python3 -I .ufo/waves/round-20/tw-precision.py 28c6837
```

Result: `exit=0`, 172/175, score `9.8286`, families `H 51/52`, `L 17/18`, `P 66/66`, `S 17/17`, `W 21/22`; failing names `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` — the same three the round-20 row at `SCORECARD.md:1329` names. The row's P 66/66 and L 17/18 reproduce exactly. Because the argv pins `28c6837`, this is a reproduction of the 2026-10-21 measurement, not a statement about the base tree's tool bytes.

Run B — current-state form at the base revision. `SCORECARD.md:1329` and `:1390` document the generic form `python3 -I .ufo/waves/round-20/tw-precision.py REV` (suite pin `f3da504`); the counter itself is unchanged between `28c6837` and base (hash above), so only `REV` moves:

```sh
cd /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireEvidenceMarker1342
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 python3 -I .ufo/waves/round-20/tw-precision.py 41cc04c8
```

Result: `exit=0`, 166/175, score `9.4857`, families `H 47/52`, `L 15/18`, `P 66/66`, `S 17/17`, `W 21/22`. The L family is the marker's own family: three cases want a `lead` row and get `exit 0` with `"findings": []`:

```json
{"family": "L", "got": {"exit": 0, "findings": []}, "name": "L-CasePureCrossCell-reset-clears-helper", "pass": false, "want": {"exit": 1, "findings": [{"class": "package_query", "evidence": "lead", "line": 3, "rule": "pacman:-Q"}]}
{"family": "L", "got": {"exit": 0, "findings": []}, "name": "L-CaseLeadsInvisible-reset-cleared-helper", "pass": false, "want": {"exit": 1, "findings": [{"class": "package_query", "evidence": "lead", "line": 2, "rule": "pacman:-Q"}]}
{"family": "L", "got": {"exit": 0, "findings": []}, "name": "L-AdoptW2-AdvHelperFn-b14", "pass": false, "want": {"exit": 1, "findings": [{"class": "package_query", "evidence": "lead", "line": 1, "rule": "pacman:-Q"}]}
```

So the row's two halves split at base: `drop provably pure data` holds (P 66/66), `Tell an observed command from a lead … on every finding row` does not (L 15/18). The three failures are all missing-`lead` (silent) failures, not mislabels.

Run C — the row's second pointer, at both revisions:

```sh
cd /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireEvidenceMarker1342
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 python3 -I .ufo/waves/round-20/tw-recall-split.py 28c6837   # exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 python3 -I .ufo/waves/round-20/tw-recall-split.py 41cc04c8   # exit=0
```

Both runs: `incident_lines: 6`, `totals {"detected_observed": 5, "detected_lead": 1, "detected_unmarked": 0, "undetected": 0}`, `finding_totals {"observed": 10, "lead": 1, "unmarked": 0}`, `control_lines: 20`, `control_findings: 0`. The second pointer's stated "5 observed + 1 lead" still holds at base with the restored tool; it does not test the three L precision cases that fail.

## Verbatim command output (trimmed)

Raw stdout of each counter run is a single JSON line (39,141 bytes for `28c6837`, 39,308 bytes for `41cc04c8`); `stderr` was empty in both. The raw receipts are retained outside the lane (the clone was deleted):

```text
/fast/scratch/hyaku/mado-r25a3/c2/receipts-CapTripwireEvidenceMarker1342/twp-28c6837.json   sha256:08508e040468011c8f073d35a9152a5cb4d55a35dccadb7ac99ca08c963938d8
/fast/scratch/hyaku/mado-r25a3/c2/receipts-CapTripwireEvidenceMarker1342/twp-41cc04c8.json  sha256:8f383963d9072b7c1769894eaac13ca5ddf3e91205c458ec5ec7bb654fa4256f
/fast/scratch/hyaku/mado-r25a3/c2/receipts-CapTripwireEvidenceMarker1342/split-41cc04c8.json sha256:ce5bf5de8be824d755bac054f372dc47210ec4796557436afd581df37254cbe2
```

Verbatim field substrings, copied from `twp-28c6837.json` (run A, `28c6837`):

```json
"commit": "28c68378eccbd5f227cdc28a62406ff390e3540a"
"families": {"H": {"passed": 51, "total": 52}, "L": {"passed": 17, "total": 18}, "P": {"passed": 66, "total": 66}, "S": {"passed": 17, "total": 17}, "W": {"passed": 21, "total": 22}}
"rev": "28c6837"
"score": 9.8286
"tool_sha256": "9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c"
```

Verbatim field substrings, copied from `twp-41cc04c8.json` (run B, `41cc04c8`):

```json
"commit": "41cc04c8d593837a0d5078bffaacdaa163d12897"
"families": {"H": {"passed": 47, "total": 52}, "L": {"passed": 15, "total": 18}, "P": {"passed": 66, "total": 66}, "S": {"passed": 17, "total": 17}, "W": {"passed": 21, "total": 22}}
"rev": "41cc04c8"
"score": 9.4857
"tool_sha256": "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84"
```

`git show 41cc04c8:SCORECARD.md` size/sha (row context):

```text
1618 lines, sha256 6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08
```

Verbatim `tw-recall-split.py 41cc04c8` header (stdout, exit 0):

```json
{
 "schema": "mado-tw-recall-split-r20-v1",
 "rev": "41cc04c8",
 "commit": "41cc04c8d593837a0d5078bffaacdaa163d12897",
 "tool_sha256": "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84",
 "pin_rev": "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d",
 "incident_lines": 6,
 "totals": {
  "detected_observed": 5,
  "detected_lead": 1,
  "detected_unmarked": 0,
  "undetected": 0
 },
 "finding_totals": {
  "observed": 10,
  "lead": 1,
  "unmarked": 0
 },
 "control_lines": 20,
 "control_findings": 0,
```

## Supersede / contradiction scan of SCORECARD.md at 41cc04c8

Search commands: `git show 41cc04c8:SCORECARD.md | grep -n -i -E "tripwire evidence marker|tw-precision|tw-recall-split|evidence marker"`, `… | grep -n -E "L 17/18|L 15/18|17/18"`, and a full scan for `1342`/pointer text.

- `:1338` `### Capabilities (round 20)` — the row's section; no pointer line exists at the end of it at base (`grep -n 1342` finds no hit anywhere in the file, so the R6 in-row pointer named in round-25 registration had not landed at this revision).
- `:1329`, `:1390` (axis rows) and `:1342` (this row) all cite P 66/66, L 17/18 at `28c6837`/`a8960de`. These are dated measurements, not present-tense claims.
- `:1458` (round 21, "Legacy screens") is the first contradicting observation: `tw-precision.py a6cef8984…` … `(P66/66,S17/17,W21/22,H47/52,L15/18)` … "Never call this 175/175 or retroactively admit round20." It reports L 15/18 under the same historic wants but does not mark this row.
- `:1566` `### Capability status (round 24 re-demonstration)`; its preamble (`:1568-1571`) states "Status is what the command did, not what the original row asserted. This table supersedes the implied `works` of every earlier row; the earlier rows stay as written."
- `:1582` is the explicit superseding row: `| tripwire evidence marker | fails | tw-precision.py <rev>: L 15/18 (P 66/66) at 8e5d9369, not the row's L 17/18 (that was 28c6837). Two reset-cleared helper leads (…) pass at 28c6837 and fail now: round-21 harm H2, still unrepaired (.ufo/waves/round-24/w1/reports/ScribeC2Evidence.md) |`
- The round-24 scope note (`:1588-1598`) confirms this capability is inside the 12 counted `Capabilities` rows, not one of the three out-of-population repertoire rows.
- No later row retires or repairs the capability. My base re-run agrees with `:1582` exactly (`L 15/18`, `P 66/66`) and adds the third L failure (`L-AdoptW2-AdvHelperFn-b14`), which also failed at `28c6837` and is named in `:1329`.

## Verdict and limits

- Observed at `41cc04c8`: **fails** as a present-tense capability. The row's literal command still passes because it pins `28c6837`; the capability it describes is not present in the base tool bytes (L 15/18, three lead-want cases silent, `exit 0`, 166/175).
- The row mixes a historical demonstration (literal argv) with a present-tense claim; a reader who re-runs it as written gets the stated 17/18 and a false impression of the current tool. That is a stale-row defect of exactly the kind round-24 §2.2 named, and `:1582` already corrects it.
- Not claimed: any verdict on the counter's *wants* (whether the three cases are right) — that is a mutation-review question outside this C2 row re-run. The three L cases at base all expect `lead` on `pacman:-Q` in cases whose names reference a helper; the tool emits nothing.

## Safety and cleanup

- No lane file was modified except this report. No git/jj write ran in the lane or fleet repo; sandbox git ran only in the clone with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset. No packages, services, `~/.config`, or live compositor state touched; no `hyprctl`, no nested Hyprland, no network.
- The counter and suite were executed unmodified from committed bytes; no file under `.ufo/waves/round-20/` was edited.
- Clone deleted (`rm -rf /fast/scratch/hyaku/mado-r25a3/c2/CapTripwireEvidenceMarker1342`); no surviving `tw-precision`/`tw-recall-split` processes (`pgrep -af` count 0). Receipts kept under `/fast/scratch/hyaku/mado-r25a3/c2/receipts-CapTripwireEvidenceMarker1342/` (≈80 KB total); `/fast` had 221 GB free.
