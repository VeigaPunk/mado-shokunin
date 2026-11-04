# R77Critic — falsification of the round-77 design (verdicts + commands)

Seat: critic, round mado 77, wave w1 · 2026-11-04 · base `aeeef067bd…`, HEAD `8b7ef027…`.
Method: every experiment ran read-only against frozen bytes (hashes re-measured and identical to
the declaration: tool `409e78a4…`, c1 counter `56620959…`, c2 counter `056a9152…`, c1 cases
`7d6e2b1a…`, c2 cases `597b2302…`); fixtures lived under my scratch only (fixture repos verified
`rev-parse --show-toplevel` == fixture dir before commit; throwaway identity inside the fixture
only). No lane byte, config tree, or compositor state was written. Both counting commands were
re-run by this seat into its own scratch; both reproduce TARGET_MET (rc 0): C1 15/15, 5/5 killed,
base 8/15, `tool_sha256=409e78a4…`; C2 12/12 executed/matched at `8b7ef027`.

## Verdict table

| Q | Verdict |
|---|---|
| (a) coverage move or re-score | **Coverage move** — new surface; held surfaces untouched |
| (b) cheaper control meets 15/15? | **No** — best artifact-reading rule without the modeled join scores 8/15; the seat-proposed cheaper rule scores 7/15; target is right |
| (c) executed/matched split | **Split works; anchor half overclaims** — fixture proves anchors bind *mention*, not the row's stated outcome; 2/12 rows' expectations are not "the outcome the row states" (F1) |
| (d) causal separability | **Separable both ways** — zero cross-references; disjoint inputs; each counter re-run green with the other absent |
| (e) harms | **None found**; three watch items (W1–W3) |
| (f) universal / unfalsifiable / uncommitted after-state | **No universal or unfalsifiable clause**; one uncommitted-bytes finding (F3, closed at `3e35d0a9`) and one new provenance finding (F4: counters pin everything but their own bytes — see addendum) |

## (a) C1 is a new surface, not a re-score

Commands showing the surface unmoved at base:

    git grep -n -iE "barfoot|footprint" aeeef067bd -- tools quality corpus SCORECARD.md SKILL.md README.md SOURCES.md PROVINCE.md
      → empty (rc 1)
    git show aeeef067bd:SKILL.md | grep -n -i reserved
      → only the round-44 window-geometry row (line 282, a different plane) and tool-ledger prose;
        the read-only probe table (~line 204) carries no reserved-band sample
    git grep -n -iE "reserved|monitors -j" aeeef067bd -- quality tools
      → only check-session-material.py waiver prose ("reserved synthetic namespace"), no
        monitor-band consumer; no prior counter reads `monitors -j` reserved

The lane's held layer surface is the point-sample read (SKILL.md MADO-R3-1 row) plus module
semantics; neither is re-scored by C1 — the r77 instruments are new files, and the r76 counters
(`c1-r76-outcome-field.py`, `c2-r76-shapes.py`) are untouched and stay green (gate 460/460 at
freeze, receipt `receipts/pre-wave-evidence-r77.txt`). C1 adds: declaration→live-box→reserved-band
derived join with verdicts. Axis check: `python3 -I quality/check-axis-scores.py --rev
aeeef067bd|8b7ef027 --repo .` → `MADO_AXIS: checked=3 mismatched=0` at both (re-run by this seat);
the published axes genuinely sit at maximum and neither claim moves an axis number.

## (b) The live-echo control is the cheapest sufficient rule

Re-implemented the counter's `naive_score` and scored weaker families over the frozen 15 cases
(`scan-out.txt`):

| rule | score |
|---|---|
| frozen live-echo (presence + reserved sign) — parity with receipt | **8/15** |
| constant `(rc=0, MATCH, EQ, CLEAN)` — exhaustive scan of all 288 constants | **5/15** (max) |
| presence + `reserved=EQ` unconditionally (the seat-proposed cheaper rule) | **7/15** |
| config-only (models config, ignores the live layers dump) | **6/15** |

No rule that ignores config semantics or live box coordinates exceeds 8/15, and no constant beats
5/15; 15/15 is reachable only by the modeled join. The target (`base_correct < 15`) therefore
measures the claimed work. The only rule that reaches 15/15 is name-keying the oracle, which the
fixed instrument code excludes by construction.

## (c) The executed/matched split separates running from reading — but the anchor binds mention

The split itself works: the counter's own base rule prints `MADO_R77_BASE: executed=0
matched_by_read=12/12`, and the target requires `executed==12 && matched==12`; a read-only
"checklist" cannot reach it. `matched()` compares observed stdout/rc against the frozen case value.

Attack that landed — do the anchors bind the row's *stated outcome*? Fixture experiment
(`anchor-out.txt`), sanctioned fixture repos under scratch:

  * Run A: SKILL.md copy with the stated samples doctored (Matte Black→Foam Gray, 192→7,
    `str: br`→`str: us`, DP-1 resolution changed), backticked commands kept, committed →
    `MADO_R77_RUNBOOK: cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12
    verdict=TARGET_MET` at the fixture rev `7727d49e`.
  * Run B: the `hyprctl layers -j` row deleted → `ERROR (stage=setup anchor … not in SKILL.md)`.

So the anchor check is presence-only: it detects row *removal*, never row-outcome *drift*. The
declaration's predicate sentence — "the observed outcome equals the expectation the bound SKILL.md
row states" — is not what the instrument implements. Two concrete rows break the sentence:
`monitors-reserved` (the bound row states no reserved outcome at all; the expectation is the frozen
case value, disclosed only in the case JSON note) and `waybar-process` (the row states `waybar
1707…`; live pid 1720 passes via the `^[0-9]+$` shape — this one *is* disclosed in the declaration's
named limits).

**F1 (finding, wording/calibration, not instrument):** the C2 predicate overclaims for 2/12 rows,
and `monitors-reserved`'s deviation is disclosed only in the case note, not the declaration.
Smallest safe correction (L1, errata append — never rewrite a scored predicate): append to the C2
named limits, e.g. "the monitors-reserved expectation is the frozen case value; the bound row's
sample does not state the band". No byte change to the frozen counter or case set is needed; the
instrument is falsifiable and separates execution from mention.

## (d) C1 and C2 are causally separable

* Zero cross-references: `grep -n -iE "barfoot|footprint|reserved|c1-" c2-r77-runbook.py` → empty;
  `grep -n -iE "runbook|SKILL|probe|c2-" c1-r77-barfoot.py` → empty.
* Disjoint inputs: C1 consumes `tools/mado-barfoot.py@rev` + c1 cases + a scratch root, never the
  host; C2 consumes `SKILL.md@rev` + c2 cases + host read verbs, never the tool. Each target is
  computable with the other's artifacts absent — demonstrated by this seat's re-runs, each invoked
  with only its own inputs.

## (e) Harms: none found

* Operability/adjacency: all twelve frozen C2 argv are sanctioned read verbs (`hyprctl
  version|configerrors|monitors -j|getoption|binds -j|layers -j`, `pgrep -x`, `makoctl mode`,
  `omarchy theme current|version`); no forbidden verb, no socket, no write; the counter prints only
  probe stdout (no instance signature, no window titles). C1 never touches the host (git show +
  fixture files; scratch-root guarded against `/` and symlinks).
* Calibration: no published axis moves (verified at base and HEAD, `mismatched=0`); the operability
  fraction derives from `check-index.py --selftest`, not from the probe table, so landing r77
  cannot silently shift it.
* Freshness: C1 is fixture-bound (no host dependency, so no drift); C2 is declared point-in-time.
* Watch items: **W1** `binds-count` (exact 192) and `monitors-size` (exact string) are host-volatile
  to operator action; after any operator change the round must be re-measured, not re-asserted.
  **W2** cosmetic: the `MADO_R77_PROBE row=` field prints `skill_anchor`, so the `omarchy-version`
  line shows the theme anchor (`row=\`omarchy theme current\``) — receipt readers may misbind the
  probe; a note suffices, no byte change.
  **W3** see F2 below.

## (f) Universal clauses / unfalsifiable targets / uncommitted after-state

* No universal clause found: both targets are numeric with rc maps (C1 `correct==15 ∧ killed==5 ∧
  base<15 ∧ selftest`, rc 0/1/2; C2 `executed==12 ∧ matched==12 ∧ anchors==12`, rc 0/1/2); both
  receipt labels are re-derivable from committed bytes (C1) or the returned host (C2).
* Freeze order holds: declaration+instruments `e4717a1c` → counter fix `a83e9bee` → pre-wave
  receipts `94b5afb1` → wave spec `8b7ef027`; the two live captures cited by the freeze ARE in
  `e4717a1c` (verified `git ls-tree`).
* **F3 (finding, landing obligation):** C1's "Sourced ground" cites S457–S462, whose fetch bins
  (`fetch/S457.bin` … `S463.bin`) and the `corpus/SOURCES.md` rows are currently *untracked /
  modified-uncommitted* at HEAD `8b7ef027`. The committed declaration's provenance chain dangles
  until L1 commits them with the round evidence. Same class: `corpus/knowledge/bar-footprint-r77.md`
  untracked (expected wave mechanics), and the r76 D6 handoff files (`w1.ready*`) still untracked —
  the declaration commits to landing them this round; verify at integration. Status at review
  close: closed by `3e35d0a9` for S457–S463 and the knowledge entry; `S464.bin` and `w1.ready*`
  remain untracked (see addendum).
* Premature saturation: no — the axes are saturated by *numbers* but the round moves *surfaces*
  (a measured join; an executable runbook), and says so explicitly.

## F2 — the named mutation `reserved-wrong-edge` is crash-flavored (cosmetic; discrimination survives)

The frozen replacement `RESERVED_INDEX = {…},` carries a trailing comma, making the name a 1-tuple
→ the mutant tool dies on first reserved lookup (this seat reproduced: selftest fails,
`correct=4/15`). The "kill" is thus primarily a crash, not an oracle verdict. However, clean
semantic wrong-edge variants are *also* killed by the frozen case set (reproduced with the
counter's own `run_cases`): top↔bottom swap 10/15, rotate+1 9/15, left↔right 14/15 (killed by
`left-vertical`). So the claim "five named mutations each killed" survives a stronger adversary,
but the named mutant's kill evidence is weaker than the receipt implies. Smallest safe correction:
none this round (the instrument is frozen and scored); a later round may replace the anchor's
replacement with the valid dict so the kill is oracle-based. Do not edit the frozen counter now.

## Bottom line

Round design stands: C1 is a genuine coverage move with a discriminating control; C2 genuinely
separates execution from mention. Two wording-grade findings (F1 predicate overclaim +
monitors-reserved disclosure gap; F2 crash-flavored named mutant) and one landing obligation (F3
uncommitted source provenance). All corrections are L1-owned errata/appends; no frozen byte should
change post-score.

Evidence archived by this seat under `.ufo/waves/round-77/w1/R77Critic/evidence/`:
`c1-rerun.txt`, `c2-rerun.txt`, `scan-out.txt`, `semantic-out.txt`, `anchor-out.txt`,
copies of `receipts/control-baseline-r77.txt` and `receipts/pre-wave-evidence-r77.txt`.
Scratch (drivers, fixture repos, temp) deleted after archiving.

## Addendum — post-freeze dispositions audited (HEAD advanced to `2df46e29` during this review)

The wave dispositioned F1 and F2 in `de627316` while this seat was measuring; F3 landed in
`3e35d0a9`. This seat re-measured both counters at the new tip before accepting any of it:

* **F1 closed** — the declaration gained an append-only errata block naming the C2 predicate
  overclaim and `monitors-reserved`/`waybar-process`, exactly as F1 states. Verified: the block is
  appended (9 lines), no scored predicate text was rewritten elsewhere.
* **F2 closed** — `de627316` removed the trailing comma from the `reserved-wrong-edge` replacement;
  the mutant is now a valid-dict semantic swap. Re-measured at `2df46e29`: `correct=10/15 killed=yes`,
  identical to this seat's independent top-bottom semantic variant (10/15) — the kill is now
  oracle-based, not crash-based.
* **F3 closed** — `3e35d0a9` committed the S457–S463 fetch bins, `sha256-r77.txt` and the seven
  SOURCES rows; HEAD's tree carries them (verified `git ls-tree`). `S464.bin` is untracked (new
  source arriving mid-wave) — a landing obligation of the same class, small.
* **New F4 (open): the counters pin everything but themselves.** At `2df46e29` the instrument
  hashes are `tools/mado-barfoot.py` `446d197f…` (was `409e78a4…` at freeze), c1 counter `a5f4ad97…`
  (was `56620959…`), c2 counter `ac2b0f85…` (was `056a9152…`) — three post-freeze instrument edits
  (`0fa69f41`, `bbca7469`, `2df46e29` tool hardening; `4a17b31f`, `de627316` counters), each with
  red/green receipts. Neither counter prints its own sha256 (verified: no self-hash line in either
  source), and both are executed from the working tree, not extracted at `--rev`. The receipt's
  `rev=`/`tool_sha256=` therefore cannot prove which counter bytes produced a verdict. The
  declaration errata's sentence "The instrument, predicate, target and case set are unchanged" is
  contradicted by `4a17b31f` (c2 counter, 42 lines) which precedes it. C1 at the new tip still
  meets the predicate (15/15, 5/5, base 8/15, selftest 18/18 — `evidence/c1-at-head.txt`); C2 still
  `12/12 executed/matched/anchors` (`evidence/c2-at-head.txt`). Smallest safe correction (L1,
  additive, no target change): print `counter_sha256=<sha256 of __file__>` in each counter's receipt
  line, or append an errata naming `4a17b31f`/`de627316`/`0fa69f41` as post-freeze instrument edits
  with their red/green receipts. The ledger row `mado-r77-barfoot-counter` citing "freeze
  `a83e9bee`" should then say which rev the *counter* came from.

