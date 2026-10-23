# RcTripwireEvidenceMarker1342 — C2 ledger recheck of CapTripwireEvidenceMarker1342

Independent re-derivation of the ledger line in
`.ufo/waves/round-25/a3w1/reports/CapTripwireEvidenceMarker1342.md`
(SCORECARD row `tripwire evidence marker`, line 1342 at base `41cc04c8`).

## Method

- Row source: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md`
  → 1618 lines, sha256 `6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08`
  (matches the a3w1 report exactly).
- Sandbox: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q
  /home/vgpnk/Projects/shokunin/mado-shokunin
  /fast/scratch/hyaku/mado-r25a3/rc/CapTripwireEvidenceMarker1342`, then
  `git checkout -q --detach 41cc04c8` → `HEAD=41cc04c8d593837a0d5078bffaacdaa163d12897`,
  `git status --porcelain` = 0 lines. Clone deleted after the runs.
- Runs (all `exit=0`, stderr empty): `cd <clone> && timeout 600 prlimit --as=4000000000
  python3 -I .ufo/waves/round-20/tw-precision.py {28c6837,41cc04c8}` and
  `... tw-recall-split.py {28c6837,41cc04c8}` — the same form the a3w1 seat used.

## Results vs. the a3w1 report

Reproduced byte-for-byte (receipt sha256s identical to the report's):

- `twp-28c6837.json` sha256 `08508e040468011c8f073d35a9152a5cb4d55a35dccadb7ac99ca08c963938d8`,
  39,141 B: 172/175, score 9.8286, H 51/52, L 17/18, P 66/66, S 17/17, W 21/22;
  failing names `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`,
  `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` — same three the report and
  `SCORECARD.md:1329` name.
- `twp-41cc04c8.json` sha256 `8f383963d9072b7c1769894eaac13ca5ddf3e91205c458ec5ec7bb654fa4256f`,
  39,308 B: 166/175, score 9.4857, H 47/52, L 15/18, P 66/66, S 17/17, W 21/22.
- The three L failures at base match verbatim:
  `L-CasePureCrossCell-reset-clears-helper`, `L-CaseLeadsInvisible-reset-cleared-helper`,
  `L-AdoptW2-AdvHelperFn-b14` — each `got {"exit": 0, "findings": []}` vs. a `lead`
  want on `pacman:-Q`.
- `tw-recall-split.py` at both revs: `incident_lines 6`, totals
  `{"detected_observed": 5, "detected_lead": 1, "detected_unmarked": 0, "undetected": 0}`,
  `finding_totals {"observed": 10, "lead": 1, "unmarked": 0}`, `control_lines 20`,
  `control_findings 0` — "5 observed + 1 lead" still holds at base.
  (`split-41cc04c8.json` sha256 `ce5bf5de8be824d755bac054f372dc47210ec4796557436afd581df37254cbe2`
  matches the report.)
- Byte hashes re-verified: `tw-precision.py` `bd3bdc23…` (identical at both revs),
  `tw-recall-split.py` `5c8f1424…`, `tools/mado-tripwire.py` `9613f510…` at `28c6837`
  vs. `cd9da20c…` at `41cc04c8` (round-23 restoration).

Superseding pointers checked in `git show 41cc04c8:SCORECARD.md`:

- `:1582` explicit superseding row `| tripwire evidence marker | fails | … L 15/18
  (P 66/66) at 8e5d9369 …` — present, and my base re-run agrees (`L 15/18`, `P 66/66`).
- `:1566–1571` preamble "This table supersedes the implied `works` of every earlier
  row" — present.
- `:1458` first contradicting observation (L 15/18 at `a6cef89…`) — present.
- `grep -n 1342` finds no hit: the R6 in-row pointer had not landed at this revision,
  as the report states.

## Findings

None. No copied-not-run evidence (every claimed receipt hash reproduced from my own
fresh runs), correct base revision, no overclaim (the report's `fails` verdict matches
observed behavior and the superseding `:1582`), and the report neither missed nor
misstated superseding text — it correctly notes the absence of the in-row `1342`
pointer at base. One minor asymmetry only: the ledger line names the three L failures
but not the five extra H failures at base; the full family counts it does state
(H 47/52 etc.) are all accurate, so this is scope, not error.

## Safety and cleanup

- No lane file modified except this report; no git/jj write in lane or fleet repo;
  sandbox git only in the deleted clone with `GIT_*` unset. Clone deleted
  (`rm -rf /fast/scratch/hyaku/mado-r25a3/rc/CapTripwireEvidenceMarker1342`);
  `pgrep -af 'tw-precision|tw-recall-split'` = 0. No packages/services/`~/.config`/
  compositor state touched; no network.
- Receipts kept outside the lane at
  `/fast/scratch/hyaku/mado-r25a3/rc/receipts-CapTripwireEvidenceMarker1342/` (~160 KB);
  `/fast` has 216 G free.
- No tool installs needed or performed (git/python3/sha256sum already present).

## Verdict

RECHECK CapTripwireEvidenceMarker1342: agree — base re-run reproduces L 15/18 (three
silent missing-`lead` cases), P 66/66, score 9.4857, exit 0; receipt hashes identical;
superseding pointers `:1582`/`:1458` accurate; row `1342` fails at `41cc04c8`.
