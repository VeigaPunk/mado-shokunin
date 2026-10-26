# mado round 44 — registration v2 (frozen BEFORE any round-44 data commit)

Supersedes both predicates of `registration.md` (freeze `e2289516a9a857f55cda7be635933e89b931c3da`), as that file allows ("a hole
`w1` finds before any data commit re-registers as v2 with a new freeze"). No data commit exists: the lane branch carries only the
freeze `e2289516` and the w1 spec `ae996fcf` above the base `6a1a905`; `tools/mado-geometry.py` is still the round-43 tool
(sha256 `e3c2e471…`) and `corpus/knowledge/hyprland-gkeep-size-request-r44.md` is absent. Wave `w1` ran 38 seats (all reported;
`w1-results.json`).

## Wording withdrawn (w1/CritFsPremise finding 1, w1/CritClaimSizing F5)

`registration.md` called the round-43 tool's DIFFER for a fullscreen window "a false report". It was not: the tool documents DIFFER
as "a report, not a fault", and the box really differs. The correct statement: for a maximized or fullscreen client the dump shows
the state's box, and the round-43 tool could not say that the rule no longer governs it (true about the box, silent about the cause).
C1 is a **contract extension of the round-43 capability** (operability surface: the tool's verdict vocabulary and exit map), not a
bug fix, and it is booked once — as C1, not also as a mined mistake.

## C1 — `PRED-C1-r44-v2` (replaces `PRED-C1-r44`)

- **Why.** `w1/CritC1Cheat`: cheat E (state logic enabled only when `HOME=/nonexistent`, i.e. inside the counter's sandbox) and
  cheats C/F (a selftest with no state assertion) reached TARGET_MET under v1. `w1/CritFsPremise` S1: a dump whose matched clients
  are all fullscreen printed `verdict=OK` exit 0 though nothing was compared. `w1/RevC1Counter` LOW-1..3 (crash paths, docstring final
  line, unguarded regress timeout).
- **Predicate:** the docstring of `quality/counters/c1-r44-geometry-states-v2.py`: v1 plus the top verdict **NOT_COMPARED** (exit 5,
  agree = 0 and maximized + fullscreen > 0; a TILED-only dump stays OK as in round 43, so clause r still holds), clause **b5**
  (state-blind teeth: a copy whose `json.loads` renames the `fullscreen` key must fail its own selftest), clause **e** (environment
  invariance: five state inputs run inside and outside the sandbox give identical stdout and exit), the setup fixes.
  `receipts/c1-v1-to-v2.diff` is the whole change. Reference: `c1/ctl-ref-tool-v2.py.txt` (selftest 94/94).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo . --rev <rev> --work <scratch>`
- **Before** (base `6a1a905`): `fixtures=11/26 tool=present verdict=TARGET_MISSED`, clauses `a:1 b:0 b4:0 b5:0 e:1 g:1 r:1`, exit 1
  (`receipts/c1-v2-before-base.txt`; the lattice share varies with the nonce, the verdict does not). **Target:** `fixtures=26/26 …
  verdict=TARGET_MET`, exit 0, at the data commit and at the tip. **Kill rule:** anything else at the data tip is a miss, reported as an
  honest stop; no narrowing, no re-registration after data. The countable after-state is this counter's line, not a published axis
  number (w1/CritClaimSizing F6, F9: the lane's published operability fraction is `check-index.py --selftest` 12/12 and C1 does not move it).
- **Controls:** `receipts/ctl-c1-v2.txt` (`ctl/run-c1-controls-v2.py`): REF met; BASE-tool, ABSENT and 18 variants (the 13 v1 variants
  ported, K14 no NOT_COMPARED, K15 NOT_COMPARED on TILED-only, K16 NOT_COMPARED with exit 0, X1 sandbox gate = cheat E ported — caught
  by **e** only, X2 padded selftest = cheat C ported — caught by **b5** only) all missed: `CTL_C1v2 VERDICT: PASS (controls scoring
  TARGET_MET: 0 of 20; reference met: 1)`.
- **Residuals (declared):** a tool holding a model of the contract is an implementation; b4 is a naming heuristic (b5 carries the teeth);
  b5 binds the `json.loads` path only; e compares one second environment; the SKILL/PROVINCE rows are documentation riding with C1 and
  are not scored (w1/CritClaimSizing F7); live maximized/fullscreen geometry is the pinned sources' fact.

## C2 — `PRED-C2-r44-v2` (replaces `PRED-C2-r44`)

- **Why.** `w1/CritC2Cheat`: 9 of 9 forgeries admitted, including a forged receipt for held S164 that inverts the census (also
  `w1/RevC2Counter` F1), pinned bytes under false URLs (also RevC2Counter F3), prose contradicting the census, an anchor past EOF;
  `w1/RevC2Counter` F2 / `w1/SimpContract` D8: claim lines hidden behind the census prefixes; `w1/CritClaimSizing` F1: the staged r12
  re-pointed to lane ids, and an 18-line quote-only entry, admitted while holding none of the claimed surfaces; F4: the v1 docstring
  contradicted its code (ten pins, the round-43 host census).
- **Predicate:** the docstring of `quality/counters/c2-r44-gkeep-size-request-v2.py` — a complete standalone text (no inherited prefix):
  CritC2Cheat's T1-T4 (every PINS receipt pinned by digest, held ids included; every PINS receipt cited under its pin URL; census numbers
  not contradicted by prose; new-row anchors inside their receipt), the census-prefix exemption removed (only the two exact census lines
  are exempt), and clause **j** — twelve named surfaces (report size, sendWindowSize, the X11 configure branch, onAck; setSize and the
  deferred sendConfigure; the zero-size sentence and ack_configure; GTK's configured-size store, minimum-size constraint and 0x0 case;
  gkeep's application_id line), each cited by a locator whose range covers the counter-computed anchor line, on a line with the
  surface's keyword. `receipts/c2-v1-to-v2.diff` is the whole change.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r44-gkeep-size-request-v2.py --repo . --rev <rev>`
- **Before** (base): `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-v2-before-base.txt`). **Target:** `admitted=1/1
  verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** as C1.
- **Controls:** `receipts/ctl-c2-v2.txt` (`ctl/run-c2-controls-v2.py`): positive control P (the L1 draft `l1-draft/`, built by
  `l1-draft/build-pos.py` at the freeze) admitted; C2-BASE, STAGED-COPY, SHELL, R12-REPOINT and MINIMAL-QUOTES (CritClaimSizing's two
  admitted controls), HIDDEN-LINE, FORGED-PIN, FALSE-URL, PROSE-SIZE-REQUEST, ANCHOR-PAST-EOF all rejected: `CTL_C2v2 VERDICT: PASS
  (wrong=0 of 11; positive admitted=1)`. P is a control, not the data: the data commit is integrated from P and the w1 drafts and
  re-scored.
- **Residuals (declared):** claim-to-quote binding (CritC2Cheat F1, F6) and registry prose cells (F8) are the non-author reading; clause j
  binds a locator and a keyword per surface, not the truth of the sentence; the census lines are bookkeeping of pinned bytes.

## Separability (unchanged)

C1's counter reads only the tool and the round-42 counter; C2's reads only entry, registry, lesson, README and pins (w1/ConnCrossClaim,
w1/CritClaimSizing F10 PASS).
