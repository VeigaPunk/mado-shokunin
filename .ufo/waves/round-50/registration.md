# mado round 50 — registration (frozen after w1, before w2; attempt 2)

Base `8ae47b957034ae21012bbf09173cca2c48be345e`. Claims `.ufo/waves/round-50/claims.md` (`13631f24`, attempt 1, unchanged).
Wave `w1` (54 seats) ran under the run-9 orchestrator and was stopped by the run-9 wrap-up (~04:49 -03) after all 54 seat
reports had landed; `w1-results.json` arrived with null outputs, so w1 was integrated from the committed seat reports.
No seat scored a round-50 frozen counter in w1; this freeze (after w1, before any w2 seat) pins the predicates, counters,
fixtures and do-nothing controls; each control below was scored with the frozen counter bytes. Data commit `906178b6`.

## C1 — coverage (sourced): `corpus/knowledge/hyprland-bind-key-match-r50.md`, `PRED-C1-r50`

- Counter `quality/counters/c1-r50-bind-entry.py` (w1/ExecCounterC1R50 port of `c2-r49-bind-entry.py`, re-pointed to
  round 50; L1/wrap-up hardening per w1/SentScratch S2: TMPDIR refused under `/tmp`, `/var/tmp`, `/dev/shm` and inside the
  scored repository), frozen sha256 `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0`.
  Repairs carried from w1: F1 (clause d numeric-band false positive), F2 (clause f/r receipt pinned to
  `binds-live-r50.txt`), F5 (no-pins short-circuit reports the clause it ran). Clause i GROUND tuple re-based because the
  round-49 closure text itself quotes the round-49 terms (`xkb_state_key_get_one_sym`, `m_xkbSymState`) under `corpus/`.
- Command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && TMPDIR=<scratch> python3 -I quality/counters/c1-r50-bind-entry.py --repo . --rev <rev>`.
- Predicate sentence (the counter docstring, clauses a-r): the entry `corpus/knowledge/hyprland-bind-key-match-r50.md` is
  admitted iff every clause scores 1 — registry rows S352-S363 bind the round-50 pins (c), located quotes (d/e), the pinned
  live receipt answers the entry's host claims and replays byte-equal (f/r), the step/ground/topic structure holds (e/h/i/j),
  and the README index row names the entry (b).
- TARGET_MET iff `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET`.
- At data `906178b607f2071af7c2efec5aad976a8bfa5757`: `PRED-C1-r50: clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET` rc 0 (`receipts/c1-at-data.txt`; the same receipt covers the w1/RevC1Counter two-nonce gap in that clause g's 150 cases are generated and judged at count time inside the single run, and the replay in clause r is byte-compared against the pinned digest `9a47199e2297…`).
- Do-nothing controls, frozen counter (receipts `controls-c1.txt`, fixture clones under `/fast/scratch/hyaku/mado-r50/L1Freeze`, toplevel asserted):
  - `c00-absent` (base `8ae47b95…`): `clauses=a:0 admitted=0/1 verdict=TARGET_MISSED` rc 1.
  - `c13-r49-paste` (the round-49 candidate entry pasted at the round-50 path, rev `6a8693fe…`): `f:0 r:0 admitted=0/1 verdict=TARGET_MISSED` rc 1 — the do-nothing control that skips writing the new entry cannot reach the target.
  - `c12-stub` (head + one sentence, rev `2371fcc8…`): `b:0 e:0 f:0 g:0 h:0 i:0 j:0 r:0 verdict=TARGET_MISSED` rc 1.
- Kill rule: any receipt whose final line is not exactly the TARGET_MET sentence above at rev `906178b6…`, or any control
  that reads MET, kills C1.
- Surface moved: bind key matching, frontier → core (claims.md C1).

## C2 — operability: session-material gate v3, `PRED-C2-r50`

- Counter `quality/counters/c2-r50-session-gate.py` (w1/ExecCounterC2R50), frozen sha256 `1d52a62cd969aba59c2cd1f944212b6f9619212b5fb313c470c4c14ebd62b298`.
  Clauses: `s` gate selftest >=94 with all 69 v2 case names; `r` K nonce-sized red fixture repos each detected with
  findings>=1 at the gate's default scope; `g` K counter-shape repos each clean; `d` a red shape outside `.ufo/` is seen
  by default and blind under `--scope ufo`.
- Command: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r50-session-gate.py --repo . --rev <rev> --work <scratch> --nonce <n>`.
- Predicate: the gate bytes installed at `quality/check-session-material.py` of the scored revision are v3
  (sha256 `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`, w1/ExecGateV3, byte-identical to the
  round-49 draft), selftest 94/94 with the 69 v2 case names kept, detecting every frozen red shape family and no green one.
- At data `906178b6…`, nonces 50117 and 778899: `selftest=94/94 names=69/69 red=42/42 green=44/44 scope=seen verdict=TARGET_MET` and `red=44/44 green=41/41 … TARGET_MET` rc 0 (`receipts/c2-at-data-nonce50117.txt`, `c2-at-data-nonce778899.txt`).
- Do-nothing controls, frozen counter, nonce 602211 (receipts `controls-c2.txt`; w1 scored the same controls with the same
  counter bytes at `ExecCounterC2R50/receipts/` — stub `3c0a46b9…`, v2-scope-all `8e2b8e43…`, v3-ufo-default `3758808c…`, R7/R8/R9 rule-removal mutants each dropping exactly its family):
  - `c00-v2-at-base`: v2 gate at base, `red=0/41 green=0/40 scope=blind verdict=TARGET_MISSED` rc 1.
  - `c12-stub` (over-flagging gate, rev `716dbc4f…`): `selftest=34/94 green=0/40 verdict=TARGET_MISSED` rc 1.
  - `c14-v3-ufo-default` (v3 rules, default scope ufo, rev `482e3e89…`): `selftest=93/94 red=0/41 scope=blind verdict=TARGET_MISSED` rc 1.
- Kill rule: any receipt not exactly the TARGET_MET sentence at `906178b6…` for both nonces, or any control reading MET, kills C2.
- Surface moved: the lane's evidence-privacy gate, `.ufo/`-scoped v2 → repo-wide v3 (claims.md C2; round-48 M48-8, round-49 D7-adjacent).

## Frozen artifacts (data commit `906178b6`)

| artifact | sha256 |
|---|---|
| `corpus/knowledge/hyprland-bind-key-match-r50.md` | `ae8f8d4de6fa8ede452423095942ee9f2182efdbab79c02744271c6fb0016977` |
| `corpus/lessons/round-50.md` | `e7cd29620aeed655f54fa3401b901acba8fe3f47ffdb4b5e9d6f3a62e20be794` |
| `corpus/SOURCES.md` (rows S352-S363 appended in `## Registry`) | `b3a1a041d4a9ce0c2555f028ce415bac5a4b1a0e38bf782e730cbb24ddf52744` |
| `quality/check-session-material.py` (v3) | `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61` |
| `quality/check-wave-done.py` | `10f4359ac0af755a4e7bcb1959233862fcde4d1bc895806409b7ea1b054f818c` |
| `quality/check-state-cite.py`, `quality/check-deliverables.py` | w1/ScrQualityR50 prototypes |
| `tools/mado-hostguard.py` | `fdaa5c2ec297ebfdddc1238d0dfe693ba0ae75ed2310939843cf14b024b7b47e` |
| `.ufo/waves/round-50/receipts/binds-live-r50.txt` | `9f16e5a5ce7fe39fc30cd8a6041fcdf733f7b794f20310796bae09d01ae51590` |
| pins `.ufo/waves/round-50/fetch/` (16 files) | `SHA256SUMS` in dir; 14 upstream pins byte-equal to round-49 |

## Routed items at freeze (from claims.md; closures)

- D1 (round size; the 38 round-49 w2 items): ran inside w1's 54 seats (spec carried them retargeted, `make-w1-spec.py`).
- D2 (final state of the 7 unsettled round-49 seats): all 45 round-49 w1 seats settled; the 7 named seats carry non-null
  outputs in the committed `round-49/w1-results.json` (measured 2026-10-27: 0 nulls of 45); `quality/check-wave-done.py`
  lands this round (criterion 102).
- D3 (the 57,865-pair figure): receipt or correction — w2 item (CritC1Random was cut off mid-work, M50-4).
- D4 (do-nothing control on the frozen round-49 C1 counter): closed by w1/ExecDoNothing (8 controls MISS on the committed
  counters at `13631f24`); round-50 freeze controls above extend it to the round-50 counters.
- D6 (QUALITY criteria for M49-1/M49-3): criteria 100-101 landed with instruments.
- D7 (host guard M48-10 installed, both-ways): `tools/mado-hostguard.py` installed; w1/ExecHostGuardR50 receipts
  (16, `SHA256SUMS` ok, fake home only, selftest 45/45 re-run at the installed path this freeze).
- D8 (lesson gate-count correction): erratum appended to `corpus/lessons/round-49.md` with its counting command (M50-2).

## Residuals (declared)

- C1 clause g samples 150 generated cases per run; it is a bounded adversarial sample, not exhaustive proof (w1/CritC1Args).
- C1 clause f/g/r replay reads the live compositor socket read-only; a host without the socket fails closed (SETUP), which
  is the honest direction.
- C2 fixtures are nonce-generated shape carriers; the gate at the lane is red by design (228 findings at base scope-all,
  all true positives the lane committed) — no claim demands exit 0 on the lane repo (w1/ExecGateV3 §3-4).
- The staged shokuknow package and the absent-defect register stay unadopted (lesson Gate; quarantine hand-check is w2 work).
- w2 (falsify) attacks this freeze; nothing here is attacked yet at freeze time.
