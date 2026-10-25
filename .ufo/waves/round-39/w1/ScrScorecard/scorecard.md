# mado-shokunin — Scorecard: round 39 update (draft, w1)

Round intent frozen in `.ufo/waves/round-39/registration.md`: three claims — C1
(re-registration of the repaired round-38 discrimination pair), C2 (config-option
ownership resolver, capability acquisition), C3 (sourced config-option knowledge
admission). This draft is written during wave w1 at the freeze commit
`457d1b125932c1e0d797061a2156b917bcd7edaa` (HEAD, "round-39: freeze registration +
base receipts + inherited r38 seat reports"; tip == freeze commit at write time).
The round-39 data commit has **not landed** at write time: C2/C3 after-cells are
pending measurement, no numbers are invented below.

## Round 39 — claims

| Claim | Axis | Before | After | Counting command / measured commits |
|---|---|---|---|---|
| C1 | calibration | frozen round-38 pair (`receipts/manifest-frozen-r38.json` + the unchanged counters) @ base `08be4eb7fd13358ed29b096e8924005d46ac409c`: `controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1; sole failure `c1-duprow` (expected MISSED, observed MET — append-at-file-end row sits outside the counter's `## Registry` parser) — receipt `receipts/c1-redbefore.txt` | re-frozen manifest `.ufo/waves/round-39/c1/manifest.json` (byte copy of the round-38 landed manifest at base; sha256 `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`, `cmp` exit 0) + the same counters @ freeze commit `457d1b12…` and @ tip (same commit): `controls=19 correct=19/19 verdict=TARGET_MET`, exit 0 — `w1/ExecC1After/after-freeze.txt`, `after-tip.txt` (both 1672 B, identical; all 19 controls `ok=1`) | `python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json --rev <rev>`; before @ base `08be4eb…` (red-before receipt), after @ `457d1b12…` |
| C2 | operability | `tools/mado-options.py` absent at freeze commit (`git ls-tree -r --name-only HEAD` has no match; `ls tools/mado-options.py` → exit 2); no counter `quality/counters/c3-r39-options.py` exists at freeze (registered before: `tool=absent`, exit 1) | tool + counter land at the round-39 data commit; target `fixtures=N/N tool=present verdict=TARGET_MET`, exit 0 — measurement pending data landing | `python3 -I quality/counters/c3-r39-options.py --repo . --rev <rev>` |
| C3 | coverage | no `corpus/knowledge/config-option-table-r39.md` and no S218/S219 rows at freeze commit (`git show HEAD:corpus/SOURCES.md` count of `S218`/`S219` rows = 0; registered before: `admitted=0/1 verdict=TARGET_MISSED`, exit 1) | entry + S218/S219 rows land at the round-39 data commit; target `admitted=1/1 verdict=TARGET_MET`, exit 0 — measurement pending data landing | `python3 -I quality/counters/c4-r39-options-entry.py --repo . --rev <rev>` |

## Capabilities (round 39)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| config-option ownership resolver | static resolver of the config-tree option table (all non-bind/non-animation/non-workspace/non-rule `key = value` settings) through the Hyprland source graph, with last-declarer ownership resolution and an optional `--getoption <json>` live-value merge reproducing the divergence vocabulary (`agreement` / `agreement*` / `live-default` / `mismatch` / `config-only`); strict regular-file policy; no compositor, socket or network; Python stdlib only | `tools/mado-options.py`; `quality/counters/c3-r39-options.py` (row entry pending data landing; tool absent at freeze commit `457d1b12…`) | 39 |

## Saturation, retired, records update

Saturation 9.0 / N=3 **unchanged**; retired: **none** this round.

Records update (round-38 lesson correction): the round-38 sources paragraph's
assimilation refusal count "2 refused" is corrected to **3 refused** — the
round-38 ledger records the three refusals explicitly (r28, r29 journal, r29
socket-client; `corpus/lessons/round-38.md` ## Mistakes: "earlier LOG wording said
'two' and is corrected"; LOG round-38 entry: "three refusals stand"). The
published-axis staleness gate is unchanged: `python3 -I quality/check-axis-scores.py
--repo . --rev master` at freeze commit prints `MADO_AXIS: checked=3 mismatched=0
rev=457d1b125932c1e0d797061a2156b917bcd7edaa` (navigation published=derived=55/55,
calibration 50/50, operability 12/12; MATCH ×3, exit 0) — identical to base
`08be4eb…` (`receipts/axis-base.txt`).

## Sources, harm watch, frontier

Sources: **211** rows at freeze commit (round-38 end state). S218 (Hyprland
0.56.0 Variables page, option-syntax) and S220 (0.56.0 Dispatchers page) receipts
fetched this round (`w1/ExecAssimFetches/S218.bin` sha256 `400d1819…2801`,
`S220.bin` sha256 `f9b51362…6e2`); S219 (own-work row for the options tool) is
**unverifiable at fetch time** — no data commit exists yet, `ls tools/mado-options.py`
exit 2, `git log --all -- tools/mado-options.py` empty; receipt to be re-derived at
the data tip. S218/S219 row landing is C3's deliverable (pending).

Harm watch (measured @ freeze commit `457d1b12…`): navigation `indexed=55/55
missing=0 dangling=0 duplicates=0` (`w1/ExecGateHealth/gate1-check-index.out`);
discrimination control replay `controls=19 correct=19/19` (`gate2-discrimination.out`);
eventq counter `fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET`
(`w1/ExecEventqSnapshot/eventq-after.txt`); selftest base `MADO_SELFTEST: 460/460`
(`receipts/selftest-base.txt`); census before and after both exit 0 with the same
W-warning set (`receipts/census-before.txt`, `w1/ExecCensusAfter/census-after.txt`).
Routed defect #3 handled: eventq live snapshot re-taken census-only
(`w1/ExecEventqSnapshot/eventq-live-census.txt`, tool sha256 `436f550e…`; no
committed full `ss -xpa` table).

## Planned (round 40; intent only)

1. Land the round-39 data commit and re-measure: C1 must stay `correct=19/19
   verdict=TARGET_MET` at the data tip; complete the C2/C3 after-cells (N/N,
   admitted=1/1) at the data tip.
2. Repair the two latent counter defects routed from round 38: `c2-r38-request-ground.py:198`
   crashes with `TypeError(int(list))` when a source line lacks `verified-at`; the eventq
   `why` detail's `agree` regex (`OVERALL:.AGREE`) differs from the scoring regex
   (`OVERALL:\s*AGREE`).
3. Regenerate the eventq live/committed receipts every round the instance directory rolls
   (`/run/user/1000/hypr/<HIS>_<epoch>_<rand>/`) — round-38 finding 1.
4. Keep the M37-5 crib-watch by name (considerthese/2026-10-25.md proposal 3) applied to the
   re-registered C1 pair, and rank the next frontier surface once the options table lands
   (considerthese/2026-10-24.md proposal 4 follow-on: per-key `getoption` cross-check
   autonomy).
