# ScrMistakes — round-46 w1 (2026-10-26) — mistakes mined for `corpus/lessons/round-46.md ## Mistakes`

Seat: `ScrMistakes` (scribe, leaf; no dispatch, no background jobs). Lane `mado-shokunin`, base
`b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`.
Deliverable: `.ufo/waves/round-46/w1/ScrMistakes/mistakes.md` — **14 rows** (M46-1 … M46-14), **3 proposed
QUALITY criteria (87, 88, 89)** with checks, **2 candidates not proposed**, **2 conflicts recorded verbatim**, and
the routed items D1/D3/D6 that are not rows.

## Behavior

Mined from the round-45 closure §6 (D1–D6), this round's freeze, and the w1 attack seats' committed receipts;
every count was re-derived from the lane's own bytes rather than transcribed:

- **Five cross-scope URL repeats, not two** — built the positive-control tree in scratch (clone of the freeze +
  `l1-draft/build-pos.py`, commit `b82517c`), ran the fleet census over its registry: 14 W04 lines against 9 at
  base, five new (S317, S318, S320, S321, S324); exact-URL row counts per family
  (`receipts/census-pos.txt`, `receipts/url-exact-pos.txt`). Two seats independently reached five
  (`CritRegistration.md:16`, `CritPremise.md:20`).
- **The C2 control battery's abort reproduced as a measurement** — the first cut asserted global uniqueness of a
  URL the corpus holds twice (S182 and S321 share `MiscFunctions.cpp`): `count=2` raises at
  `run-c2-controls.py:126`, while the protocols URL now used (`count=1`) holds
  (`receipts/harness-assert-demo.txt`).
- **The pre-freeze V03 survivor** — post-freeze line `ctl-c1.txt:7` (`fixtures=89/90 … TARGET_MISSED`) and the
  separating fixture (index 22, `case-exact-dump-name`, sha256 `027ed508…` = the counter's pin,
  `receipts/fixtures-pin.txt`). The pre-freeze run has no committed receipt; the row says so.
- **The round-45 w2's product** — the tool holds (5 nonces, 22/22 adversarial), the entry has six non-supported
  sentence units (two mis-located, one wrong, three unpinned), the privacy gate catches 0/22 attack shapes while
  its selftest reads 22/22, and the C2 counter admits 10 of 12 forgeries with six undeclared.
- **The C1 harness's clause r and its sandbox** — after `SentTool-3`'s IRC report I verified the code facts and
  receipts: clause r is a PATH marker two committed bypass tools walked through at `verdict=TARGET_MET`, the
  counter writes a `.pyc` into the frozen lane against its own docstring, and the sandbox leaves the live
  compositor socket, `$HOME` and 25 sibling scratch dirs reachable (`receipts/senttool-verify.txt`). Rows M46-12,
  M46-13, M46-14.
- **The in-flight v2** — after `ConnCrossClaim-3`'s broadcast I read (not scored) the untracked
  `quality/counters/c1-r46-devices-v2.py`: the selftest env now carries the fake bin and the pipe tripwire replaces
  the file marker (clause r's second shape closed), and the allowlist root drops `/home`, `/run`, `/fast` (M46-14's
  fix in source form), but `/usr` is still bound with the stub only on PATH, so M46-12's absolute-path shape stays
  open as written (`receipts/c1-v2-carryover.txt`).
- **D2/D4/D5 re-measured** — the serial in 24 tracked files (3 held entries, 21 wave copies; token compared to a
  live serial field in-process, value never written); `results.json` gone but the 282 B digest untracked;
  `w1-results.json` 41/41 `output: null`.

## Gates and instruments (what I actually ran)

| instrument | run | result |
|---|---|---|
| `w1/ScrMistakes/verify-quotes.py` | every quote in the draft, against its source line and the draft | `claims=42 found=42 not_found=0 over_25_words=0 draft_missing=0`, exit 0 (`receipts/verify-quotes.txt`) |
| `w1/ScrMistakes/check87.py` (proposed criterion 87) | committed `ctl-c2.txt` (15 controls) and two red shapes | `PASS`; red `scored=7 want=15 verdict_line=absent` and red `verdict_line=absent` (`receipts/check87-run.txt`) |
| `w1/ScrMistakes/check88.py` (proposed criterion 88) | `CritC2Forgery/forge.out` + `tighten.out`, declared F1,F2,F3,F9, plus two red shapes | `PASS`; red `admitted_uncovered=F10,F4,F5d,F6,F7,F8`; red `admitted_passing=F1,F2,F3,F9` (`receipts/check88-run.txt`) |
| fleet `scripts/sources-census.sh validate --file <pos>/corpus/SOURCES.md` | read-only over the scratch tree | 14 W04 lines, `ok`, exit 0 (`receipts/census-pos.txt`) |
| read-only lane git | `git show`/`git grep`/`git ls-files`, `GIT_OPTIONAL_LOCKS=0 git status --porcelain` | no index refresh, no mutation |

Criterion 89 has **no runnable check yet** (the green requires the next counter); its red state is `SentTool`'s two
bypass receipts, which I verified line by line but did not re-run. I did **not** run the C1/C2 claim counters, the
round-45 w2 counters, or any lane gate.

## Touched surfaces

- Written: `.ufo/waves/round-46/w1/ScrMistakes.md` (this report) and
  `.ufo/waves/round-46/w1/ScrMistakes/` (`mistakes.md`, `check87.py`, `check88.py`, `verify-quotes.py`,
  `receipts/` 14 files). Nothing else in the lane.
- Not written: the lesson `corpus/lessons/round-46.md` (does not exist yet; the L1 writes it), `corpus/QUALITY.md`,
  the registration, the counters, the fixtures, the pins, the entry, the reference, `corpus/SOURCES.md`,
  `corpus/README.md`, `SKILL.md`. No git/jj mutation in the lane or the fleet; no package transaction; no
  compositor write. The only host read was `hyprctl monitors all -j` inside one in-process comparison (M46-10),
  whose value is never written.
- Scratch `/fast/scratch/hyaku/mado-r46/ScrMistakes` (one `--shared` clone, three red-shape files) deleted before
  yield; receipts copied into the seat dir first.

## Findings (one line each; full rows in `mistakes.md`)

1. **M46-1 `number-drift`** — registration: two cross-scope URL repeats; census: five.
2. **M46-2 `vacuous`** — a control battery aborted before scoring on a global-uniqueness assertion the corpus
   violates (a URL held by S182 and S321).
3. **M46-3 `survivor`** — V03 (case-insensitive names) met PRED-C1-r46 before the freeze; fixed by the
   `case-exact-dump-name` fixture, now the only clause-f separator for it.
4. **M46-4 `vacuous`** — PRED-C2-r46 admits 10/12 forgeries, six undeclared; seven tightening candidates A–G kill
   each and pass the positive control.
5. **M46-5 `provider`** — the round-45 entry attributes the landed tool's live run to the L1 reference's receipt
   (`c6ac5fc2…` cited, `2f007417…` ran).
6. **M46-6 `attribution`** — the round-45 entry cites the branch that returns before the event; `check-locators`
   cannot see it.
7. **M46-7 `vacuous`** — the privacy gate's selftest 22/22 while 0/22 attack shapes are caught and 5/6 legitimate
   shapes are flagged.
8. **M46-8 `landing`** — D4's remedy left the replacement digest untracked.
9. **M46-9 `provider`** — D5: 41/41 `output: null` seats; the results file is not evidence.
10. **M46-10 `number-drift`** — the serial is in three held entries (24 files), not one.
11. **M46-11 `reference-drift`** — the C2 draft entry's parser/dump model drifts in three places (flat device key
    is a config error; the UNK row is wrong because the dump prints `active_keymap`; the 47-value count is outside
    its cited range) and omits `main`.
12. **M46-12 `vacuous`** — C1 clause r is a PATH marker: an absolute-path `hyprctl` and a bare-name call under
    `--selftest` both score `TARGET_MET`.
13. **M46-13 `landing`** — the counter writes `__pycache__/*.pyc` into the frozen lane against its own docstring.
14. **M46-14 `scope`** — the sandbox hides repo/lane/parent only; the live compositor socket, `$HOME` and 25 peer
    scratch dirs stay reachable (a unix socket on a `--ro-bind` is still connectable).

Proposed criteria: **87** (a control battery's receipt is complete and its mutation is row-addressed), **88** (a
shape counter carries a forgery suite; a candidate passes the positive and fails each undeclared forgery), **89**
(a harness that scores untrusted code contains the host's IPC/home and tests "runs nothing" by execution, not a PATH
marker). Candidates not proposed: the must-flag half of M46-7, and M46-13's before/after tree observable.

## Conflicts recorded verbatim (not adjudicated here)

1. Privacy-gate false positives at the same revision: `CritW2Gate.md:15` "5 of 6 legitimate shapes are flagged"
   vs `ExecSessionTriage.md:47` "False positives: **0**. Every match is a genuine dump-shaped object" — different
   populations (planted documentation examples vs existing findings).
2. Whether F6 (anchor cell, wrong lines) is a declared residual: `CritC2Forgery.md:14` says not declared; the
   counter's docstring names the anchor ranges among the cells it does read
   (`quality/counters/c2-r46-input-device-entry.py:72`).

## Out of scope / not done

- No edit to the lesson, QUALITY, counters, fixtures, entry, registry, README or SKILL; no re-registration; no
  claim scoring; no adjudication of the two conflicts.
- Routed, not mined: **D1** (discharged in substance — the w2 ran; its lesson belongs in the closure section),
  **D3's registry row** (drafted by `ExecSessionTriage`, the L1's to land), **D6** (drafted as S326–S333 by
  `ExecSupersede`, not yet landed).
- `ExecW2Monitors`, `ExecSerialRule`, `ExecSupersede` were still writing when this draft was taken; their numbers
  are seat receipts and must be re-read at the wave tip. The untracked v2 counters were read at 17:57 and may change
  before the L1 freezes them.

## Artifact paths

- `.ufo/waves/round-46/w1/ScrMistakes/mistakes.md` — the deliverable (rows, criteria, conflicts, routes, limits).
- `.ufo/waves/round-46/w1/ScrMistakes/check87.py`, `check88.py`, `verify-quotes.py` — the three instruments above.
- `.ufo/waves/round-46/w1/ScrMistakes/receipts/` — `verify-quotes.txt`, `check87-run.txt`, `check88-run.txt`,
  `census-pos.txt`, `url-exact-pos.txt`, `url-occurrences-pos.txt`, `harness-assert-demo.txt`, `fixtures-pin.txt`,
  `d2-serial-count.txt`, `d4-d5-state.txt`, `c2-counter-sites.txt`, `senttool-verify.txt`, `c1-v2-carryover.txt`, `locators.txt`.
