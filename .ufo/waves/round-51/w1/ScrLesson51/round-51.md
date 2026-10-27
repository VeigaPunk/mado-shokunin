# Round 51 lesson — the lane-level tool ledger and the dispatcher dispatch (2026-10-27, hyaku run 10)

Base `6ca8c559a4a3d6d361101592116eea2bc7452437` (the round-50 verifier spot-check commit; round-50 data tip
`74782d39e7697608917b5e909f0e8580aaa3e15c`); claims `.ufo/waves/round-51/claims.md`
(`d274028163033244bd78938ad152dc250cc50480`). Wave `w1` (43 seats, `.ufo/waves/round-51/w1-spec.json`) ran BUILD +
first attack under policy v1; TODO-L1: the freeze revision, the `w2` seat set, the round total and the WAVE-DONE verdict.

C1 is the operability move (capability acquisition): the tracked lane-level tool ledger the claim declares —
`quality/tool-ledger.md`, `quality/check-tool-ledger.py`, `quality/counters/c1-r51-ledger.py` (`PRED-C1-r51`; all three
absent at base) — answering round 50's
`w2/RevLedgerR50` miss (the wave-seat ledger covered neither `tools/mado-hostguard.py` nor `tools/mado-keysym.py`, and no
lane-level ledger existed) and `considerthese/2026-10-26.md` proposal 2. C2 is the coverage move (sourced):
`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, new rows `S364` onward (claim band `S364`–`S379`), `PRED-C2-r51`,
whose novelty clause counts `.ufo/waves/round-*/candidate/**` in its baseline — round 50's candidate-inclusive carry
(M50-6). Round-50 closure defects routed here: D1 (the final WAVE-DONE receipt must be committed at the integration tip —
M51-1 below), D4/M50-9 (the fetch-checksum manifest's unverifiable self-row, cleaned receipt-side only, never by editing
round-50 bytes), and the 13-row absent-defect quarantine hand-check (`## Gate` → `### Assimilation`).

## Gate

Sources opened 2026-10-27 by w1 seats (TODO-L1: name the fetch/verify seats and the pins they landed — candidates from the
dispatch are `w1/ScoutDispatchMap`, `w1/ExecFetchDispatch`, `w1/ScrRowsDispatch`, `w1/ScrDispatchEntry`, `w1/RevNovelty`,
`w1/CritHeldFacts`, `w1/RevRowsTruth`). Pins under `.ufo/waves/round-51/fetch/` (TODO-L1: pin count, the entry's pin
manifest path, `SHA256SUMS`, and the sender/pin-binding receipt — the round-50 house line is "every digest in the rows
binds a pin, `mismatches: []`"). Census: before at `receipts/census-before.txt` (claims commit, 22 lines: 19 `W04`,
1 `W01`, `mado ok`, `EXIT=0`); after TODO-L1 (`sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`, exit 0
required). The claim's own history: round 50's C1 novelty was falsified at 81.7% shingle coverage by the round-49 candidate,
so this round's Gate must state the overlap numbers clause (c) measured, per compared file, not summarise them.

Admit lines (one per new registry row; URL, access date `2026-10-27`, the located quote with its pin and line. Quotes
≤25 words. TODO-L1: replace the template with one line per row and re-verify every quote against its pin):

```
- **S<id> admit**, tier <A|B|C>, <code|docs|own-work>. URL: <url>; opened 2026-10-27; pin `.ufo/waves/round-51/fetch/<file>:<line>`; quote »<quote>« (<n> words). <Which symbol the claim depends on and why this line SETS it rather than reads it (criterion 100)>. TODO-L1
```

Row shape constraints the L1 must keep (claim clause (b), row cells per `corpus/SOURCES.md`): status `mined`, opened
`2026-10-27`, tier `A`, used-by `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`; cite ≥2 rows in `S364`–`S379`
from the entry's `source:` block. Counts in this section are computed, not typed:

```
A=$(sed -n '/^## Gate/,/^## Mistakes/p' corpus/lessons/round-51.md | grep -cE '^- \*\*S[0-9]+ admit\*\*')
R=$(sed -n '/^## Gate/,/^## Mistakes/p' corpus/lessons/round-51.md | grep -cE '^- \*\*REJECT ')
```

Control and skeleton, measured 2026-10-27: the same pipeline on `corpus/lessons/round-50.md` reads `A=12`, `R=5` (its own
admit and reject lines); on this skeleton it reads `A=0`, `R=0`, because the templates are written `S<id>` and
`**REJECT**` — a template that scored would be a false decision.

### Rejected after opening

TODO-L1: one line per rejection, with the measurement that killed it and its flip condition. At least one reject line, or
a single `none opened — <reason>` line. The classes this round must test against the dispatcher surface (each is measured
at the cited point, never assumed):
(1) a rendered wiki archive page with no commit anchor; (2) a wiki URL that moves with every commit (flip: the
commit-pinned raw URL); (3) a page that states no 0.56.2 dispatcher behaviour (`0.56.2` ×0, dispatcher symbols ×0);
(4) re-registering a URL already held — the dispatcher path reaches `src/debug/HyprCtl.cpp` (held `S307`, `S320`),
`src/config/legacy/ConfigManager.cpp` (held `S303`, `S317`) and `src/devices/IKeyboard.cpp` (held `S319`), so a hyprctl- or
config-side row must widen a held `teaches`/anchor instead of duplicating the URL.

```
- **REJECT** `<url>` — <class from (1)-(4)>; <measurement: token counts, zero forty-hex anchors, duplicate of held S###>; flip: <the condition that would admit it>. TODO-L1
```

Status/recheck/used-by changes this round (old → new; every `old` cell read at the base revision, not retyped):

| row | old at `6ca8c559` | new |
|---|---|---|
| `S364`–`S<top>` | absent | present; tier `A`, status `mined`, opened `2026-10-27`, used-by `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` |
| `S319` (worked row — keep only if the entry cites it) | tier `A`, status `mined`, opened `2026-10-26`, recheck `90d`, used-by `corpus/knowledge/hyprland-input-devices-r46.md` (row parsed at `6ca8c559`) | used-by gains `, corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`; tier/status/opened unchanged |
| TODO-L1 | one further row per held row the entry cites (`S303`/`S307`/`S317`/`S318`/`S320`/`S321` are the measured candidates; `git show 6ca8c559:corpus/SOURCES.md \| grep -E '^\| *S3(03\|07\|17\|18\|20\|21) *\|'` reads their old cells) | |

No held row changes status or tier this round unless the L1 records the change here. Renumber map: TODO-L1 — `none` while
the claim registers only new ids and no staged row is adopted; any staged adoption is renumbered by source/document, never
arithmetically (round-48/50 id guard). Lane top at base: `S363` over 300 rows.

### Assimilation (shokuknow `merge/mado/` + absent-defect register + `considerthese/`)

Shape required: ≥1 **Admit** line with its grounding, and ≥1 **Reject** line with its flip condition; for any table that
yields nothing adoptable, one `none — <reason>` line stands in for that side. TODO-L1: the verdicts, from
`w1/ScoutAssim` and `w1/ScoutConsiderthese`.

```
- **Admit: <considerthese/<date>.md proposal n | staged entry>** — <what it proposes>; grounded this round by <C1|C2 artifact> at <path:line>. TODO-L1
- **Reject: <merge/mado/ staged package | considerthese proposal n>** — <measurement: e.g. `MERGE-REPORT.md` names no dispatcher/tool-ledger entry and the keyword scan hit 0 staged files>; flip: <condition>. TODO-L1
```

Id-collision guard proven before any append (a non-empty `collisions` fixture from an indented `  | S002 |` row, never
arithmetic): lane ids at base `300` (`S001`–`S363`); staged ids and intersection TODO-L1 (`w1/ScoutAssim`), renumbering by
source/document only.

Quarantine verdict summary (absent-defect register, lane slice = 13 rows — 6 payload-absent `S189`, `S195`, `S201`,
`S205`, `S224`, `S228`; 7 unchecked prose classes `S199`, `S200`, `S209`, `S222`, `S223`, `S225`, `S235`; register at
shokuknow `.ufo/waves/corpus-expansion-1/absent-defect-register.md`, READ-ONLY). Per-row hand-checks are `w1/ScoutQuarantine`'s
work; TODO-L1 fills the counts from that report:

```
quarantine: rows=13 payload_absent=6 unchecked_prose=7 present=<n> absent=<n> unverifiable=<n> adopted=0 verdict=<...>
```

A row classified `unverifiable` is not a presence claim and keeps adoption from, or into, the register closed for that row;
a row classified `present` still needs its locator before any adoption. Round 50 left the same slice open with adoption
closed; if this round also adopts nothing, the reason is this summary's counts, not silence.

## Mistakes

**M51-1** · class `closure evidence` (a final verdict asserted in prose with no receipt at the revision it is attributed to)
· evidence: the round-50 report (fleet `.ufo/reports/round-50/mado.md:3`) writes
`quality/check-wave-done.py --repo . --rev 74782d39e7697608917b5e909f0e8580aaa3e15c --round 50` → `waves=2 settled=2
verdict=OK, exit 0`, and `LOG.md:2560` (read at tip `74782d39`) writes the same verdict with a placeholder revision
(`--rev <tip>`); the only committed closure receipt is `.ufo/waves/round-50/receipts/wave-done-r50.txt` (commit
`b4a79843cc2545bbe800db9322e58f6e00436629`), whose header reads `--rev 8dbbf61a1a1425d7c0c07354163bae6be49d09d0` and whose
body reads `waves=1 settled=1` — measured at the w1-only state, before `w2-results.json` landed (`c12b588e`). At
`74782d39` both `w1-results.json` and `w2-results.json` are present, so the two-wave run was derivable, yet no committed
receipt records it; the only `waves=2` strings under `.ufo/waves/round-50/` are the w1 seat's own gate source and probes
(`w1/ExecWaveDone/check-wave-done.py`, `w1/ExecWaveDone/receipts/history-base.txt` for rounds 41/43/44/47, and the
`w1/ExecWaveDone/receipts/selftest.txt` fixture `round=49 waves=2 settled=1 verdict=MISSING`), none of them round 50's
closure — `corpus/lessons/round-50-verifier-spotcheck.md` §2 D1 and §6 item 1.
· captured-by: none pre-round-51 as a closure event — and the nearest instrument is measurably live: criterion 69's
`check69.py` reads `rev <hex>` tokens, and pointed at that report with the round's own receipts dir at `74782d39` it prints
`MISSING 74782d39… cited at 74782d39…: no committed receipt under .ufo/waves/round-50/receipts names it` /
`FAIL 1/1 cited revisions lack a committed receipt`, exit 1. No closure step pointed it at the report: the report is a
fleet-repo file, the lane's gate family reads lane paths, and `LOG.md`'s placeholder `--rev <tip>` yields no token at all.
· fix: criterion 103 (drafted this round by `w1/RevQuality103/criterion-103.md`; landed at integration) plus the
integration-time receipt procedure — after the last integration edit, the L1 re-runs the wave-done gate at its own
integration revision, commits the complete output and exit status under `.ufo/waves/round-51/receipts/`, cites that receipt
in the report and `LOG.md` with the receipt's own revision token, and runs criterion 69's instrument on both texts before
filing.
· fix shown able to fail: TODO-L1 (arm shape for the L1 to capture: red = round 50's `receipts/wave-done-r50.txt` offered
as the final two-wave verdict, `waves=1` against a `waves=2` claim; green = a fresh `--rev <round-51 integration tip>
--round 51` receipt whose summary line matches the report. The red/green numbers are the L1's to capture, not this seat's.)
