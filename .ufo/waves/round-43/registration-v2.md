# mado round 43 — registration v2 (frozen BEFORE any round-43 data commit)

Supersedes the C2 predicate of `registration.md` (freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`), as that file allows
("A hole `w1` finds before any data commit re-registers as v2 with a new freeze, and the report names both predicates").
C1 is **not** re-registered (reason below). No data commit exists yet: the lane branch at this freeze carries only the
round-43 freeze `b2e2efd` and the w1 spec `5add5b4` above the base `a35cfdf`; `tools/mado-geometry.py` and
`corpus/knowledge/hyprland-gkeep-geometry-r43.md` are absent at the branch tip.

## C2 — `PRED-C2-r43-v2` (replaces `PRED-C2-r43`)

- **Why.** Wave w1 showed the v1 target is reachable without the claimed coverage:
  `w1/CritClaimSizing.md` (finding 2) — a 17-line entry citing three own-work receipts and one upstream file is
  `admitted=1/1`, so five of the eight links the claim names were optional; `w1/CritC2Cheat.md` — 16 forged sets
  admitted, 8 of them closed by string-local tightenings it verified on scratch copies (`w1/CritC2Cheat/probes/`).
- **Predicate:** the docstring of `quality/counters/c2-r43-gkeep-entry-v2.py` = v1 plus d+ (the Gate quote occurs exactly
  once, word-bounded, and outside comments), e+ (a `Hyprland-*` receipt's row location starts with the raw URL at
  `efb50993780079460b0cbed1363e2166a2de1d9f`), g+ (every unfenced line naming a cited id carries its quote and computed
  locator), i+ (exact package path, a flip word in each REFUSE reason, no BAD_LOC marker in the entry, and **all ten PINS
  cited**). `receipts/c2-v1-to-v2.diff` is the whole change (97 changed lines: the v2 docstring paragraph, three helper
  functions from the probe, seven patch sites, the PRED name).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r43-gkeep-entry-v2.py --repo . --rev <rev>`
- **Before** (base `a35cfdf`): `PRED-C2-r43-v2: admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-v2-before-base.txt`).
  **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** anything else at the
  data tip is a miss, reported as an honest stop; no narrowing.
- **Controls.** `receipts/ctl-c2-v2.txt` — the registered 74 controls re-run under v2 (`ctl/run-c2-controls-v2.py`: the v1
  runner with the v2 counter and the true raw URLs in control P's code rows): `CTL_C2: controls=74 correct=74/74`, exit 0.
  `ctl/v2-forgeries/forge-v2.log` and `more-v2.log` — CritC2Cheat's own forgery harness re-pointed at v2 (only `COUNTER`,
  `CTL`, `WORK` and the output dir changed): P admitted; rejected B1, B2, C1, C2, E1, F1, F2, G1, G2, X2, X3 (X3 is the
  CritClaimSizing family: no Hyprland receipt cited); **still admitted: A1, A2, D1, E2, H1, X1** — claim-binding forgeries
  (a real quote at a true locator under a claim it does not support, a census contradiction in prose, an index-row lie).
- **Residuals (declared, v2):** the claim-to-quote binding (A1/A2/D1/E2/H1/X1) is the non-author closure's reading; a held
  id's receipt is not pinned (`w1/RevC2Counter/findings.md` F1 — the round's entry is expected to cite no held id, which the
  report will check with `grep -c '^source: S0' <entry>`); a byte-identical GATE line outside `## Gate` and ids with fewer
  than three digits are invisible (`w1/ExecC2ExtraMutants.md` F1, F3; low).

## C1 — `PRED-C1-r42` stays as registered (not re-registered)

w1 findings against C1: `w1/CritClaimSizing.md` finding 1 (a verbatim copy of the round-42 reference meets the target),
`w1/CritC1Cheat.md` cheats 4 (a selftest that pins its own source hash) and 6 (a tool that behaves only when sandboxed).
None of them reaches TARGET_MET without the full contract behaviour on all 37 fixtures — the measured capability is
present in every case; the cheats defeat only the selftest-teeth clause or the sandbox scope. The verbatim-copy finding
is a provenance fact, not a hole: the C1 deliverable **is** the reference written at the round-42 freeze (lane-authored,
never installed, never run on the host as a tool of the lane). The report states the capability as "the round-42
reference installed as `tools/mado-geometry.py`, falsified by three independent implementations, mutation and security
seats", and names cheats 4 and 6 as open defects of `PRED-C1-r42`.

## Separability (unchanged)

C1 touches `tools/mado-geometry.py` only; C2 the entry, rows S290-S299, the lesson `## Gate` and the README index. v2 reads
no C1 file.
