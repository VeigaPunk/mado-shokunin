# R79RevC1 — adversarial review of C1 (static `addreserved` composition), round 79

Seat: reviewer, leaf member (no subagents). Scope: C1 only — re-derive, do not trust the receipt.
Pins used: freeze `5eb8f20fe291603c74973fa94cc55723ac8089a4`, base `e4b153dfa4a67ca56f7ec65cb6639082451626a7`,
frozen tool sha256 `c9aa1391…bed86de`, frozen controls sha256 `5f7ebb3c…252eb7`, counter blob `48ebfab6…a96a26cb0`.
Method: all measured bytes extracted via `git show <rev>:<path>` (read-only git); attack trials ran against a
scratch fixture repo (`/fast/scratch/hyaku/mado-r79/R79RevC1/fx`, toplevel asserted before every commit).
No repo edits, no host writes, no pacman, no tools installed.

## §1 Re-derivation of the frozen claim (assignment item 1)

| check | result |
|---|---|
| `git show 5eb8f20f:tools/mado-barfoot.py` sha256 | `c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de` = pinned value; worktree matched at review start |
| `git show e4b153df:tools/mado-barfoot.py` sha256 | `1bceb514…7504b5b05` = value in both receipts |
| Counter re-run at freeze (`--rev 5eb8f20f`, clean scratch, declared command) | **byte-identical to `receipts/measurement-c1-r79.txt`**, rc 0: `cases=23 correct=23 mutants=12 killed=12 base_correct=18/23 carried=18/18 tool_selftest=43/43 verdict=TARGET_MET` |
| Counter re-run at base (`--rev e4b153df`) | **byte-identical to `receipts/control-c1-r79-at-base.txt`**, rc 1: `correct=18 killed=4 … verdict=TARGET_MISSED` |
| Fetch pins | all 9 content lines of `fetch/sha256-r79.txt` verify OK |
| Carried prefix | `cases[:18] == r78 cases` (counter assertion) and independently canonical-JSON byte-equal with equal key order for all 18 |
| Controls in git vs worktree | freeze blob = worktree at measurement time (`5f7ebb3c`), r78 file unchanged (`99f1d82f…` at both freeze and worktree) |
| 12 mutation anchors | each occurs exactly once in the freeze tool, none vacuous; the 4 anchors also present in the base tool are exactly the 4 the base control killed (17/23 each) — internally coherent |
| Anchor liveness | anchors sit on executed lines: `OPPOSITE_EDGE` (:92), selector gate (:365), `STATIC_SIDES` zip (:374), transform/keep (:376), composition `expected = static[edge] + contribution` (:555), box offset, extent; the tool's own selftest re-tests the static semantics 8× (:729-755) |

Hand re-derivation of the five new cases from case inputs + sources (freeze set): static-composed
26+((4+26)+4)=60 ✓; static-other-edge 0+26=26 with box x=40 ✓; static-exclusive-false band=26,
would-be expected=52 ✓; static-last-wins 26+26=52 with only M1's selector ✓; capture values in every
new case agree with the same arithmetic (no circularity inside the *data*).

## §2 Attacking the counter (assignment item 2)

Trials ran the **freeze counter blob** against **fixture commits** in scratch (base tool commit + variant commits):

1. **Capture-echo tool** (`expected = band` — the tool derives its prediction from the runtime capture instead
   of `--rules`): `TARGET_MISSED`, rc 1, correct=20/23. Killed by exactly `second-consumer` (pinned expected=34
   vs echo 60), `reserved-differ` (34 vs 26), `static-exclusive-false` (52 vs 26). The frozen set has real
   anti-lookahead teeth.
2. **Hardcoded/refusal-all do-nothing tools**: any tool lacking the 12 anchor literals dies at `killed=0`
   (`anchor-absent` path, counter `apply_mutation` → `MADO_R79_MUTANT … reason=anchor-absent`); a refusal-all
   tool caps at 19/23. TARGET_MET requires 23/23 outputs *and* 12 live anchors whose mutation changes scores —
   a pure lookup table cannot pass.
3. **Semantically equivalent refactor** (`expected = contribution + static[edge]`): correct=23/23 but
   `static-dropped` anchor-absent → killed=11 → `TARGET_MISSED`, rc 1. See F3: the kill rule binds anchor
   *text*, not semantics — correct for a pinned artifact, but it means `killed=12` certifies "these 12 anchors
   are live in these bytes", not implementation-independence.
4. **Carried-prefix objects**: compared are whole case dicts (`cases[:CARRIED] == carried`, structural
   equality over every field) — the right objects; I verified the stronger canonical-bytes equality holds.
5. **`base_correct == 18`**: the base revision is pinned, so 18 is a fixed fact of that blob, and the counter
   enforces `base_correct == BASE_EXPECT` exactly. A hypothetical do-nothing that *accepted* `--rules` but
   ignored it would score 19 (it passes `static-other-edge`, static top=0) — so 18 pins "the held r78 model",
   not "any do-nothing". Nothing without the static term reaches 23 (ignore-rules ≤ 19, echo ≤ 20, refusal-all
   ≤ 19). The control is real.
6. **Counter selftest clause**: `selftest_ok = rc == 0 and m.group(1) == m.group(2)` accepts a vacuous
   `0/0` tool selftest (see F4). Nil impact today — cases and mutants carry the weight.

## §3 Attacking the claim (assignment item 3)

- **Is `coverage` the right axis?** Yes with one caveat. The composition is a host-independent, frozen-input
  behavior; coverage over a frozen case set is the falsifiable form of the claim, and the mutants make the
  instrument attack itself. The caveat is expectation provenance — a coverage axis is only as good as the
  independence of its expectations, and F1 below shows that risk was real at the freeze.
- **Does the composition need `--rules`, or could the tool derive it from the two captures?** It needs
  `--rules`, proven both ways. Empirically: the echo trial (§2.1) is exactly the capture-derived model and it
  fails 3/23. Theoretically: captures carry the *composed* total (static+dynamic); subtracting the bar's own
  contribution makes `expected ≡ band`, so `EQ` is unconditional and the GT/DIFFER detections
  (`second-consumer`, `reserved-differ`) become impossible. The model must be grounded in the config tree to
  have a verdict worth printing.
- **Is any case expectation derived from the tool rather than from the sources?** At the freeze, yes — for one
  input class. See F1.

## §4 Findings by severity

**F1 — HIGH (confirmed real; already found and repaired by the round post-freeze).** The frozen tool credited a
bare `addreserved` (no prior same-selector rule) with its area; the source drops it.
`Hyprland-legacy-ConfigManager.cpp` (r45 receipt, sha `9db68cf4…` = S303 pin): `:1330-1331` writes the area into
the *existing* selector rule and returns; with none, `// fall` (`:1334`) reaches
`monitorRuleMgr()->add(std::move(parser.rule()))` (`:1340`) — a default rule that never received the area.
Consequences at the freeze: the frozen tool on a bare-addreserved config predicted expected=52 vs live band=26
(`receipts/repair-r79-c1-fallthrough.txt`, first block: `box=DIFFER … expected=52 … exit=1`), and the freeze-time
new cases encoded that model: `static-composed`/`static-other-edge`/`static-exclusive-false`/`static-last-wins`
carried bare `addreserved` rules (verified by diffing freeze vs repaired controls), and `static-last-wins`' M2
capture showed reserved-left=5 for M2's bare rule. So for those shapes the expectations matched the tool, not
the sources — the exact failure mode assignment question 3 probes. The wave's own re-derivation caught it
(R79ScribeEntry F1 → LOG M79-6); repair R1 (`d6be05ef`) fixed tool (now `673ac44d…`, adds the drop rule + a
44th selftest "an addreserved with no prior selector rule drops its area"), counter (anchors moved to the
repaired lines, `4af4b1a8…`), and cases (positional rules prepended; M2 capture 5→0). I re-ran the repaired
generation at HEAD bytes: `cases=23 correct=23 mutants=12 killed=12 base_correct=18/23 carried=18/18
tool_selftest=44/44 verdict=TARGET_MET` (tool `673ac44d`, controls `108bde32`) — matching
`receipts/measurement-c1-r79-repair.txt` (measured at `d6be05ef`, same tree contents). The repaired state is
source-aligned and green; the freeze-state claim remains true *as measured* but its "every expectation derived
from the sources" premise had this one counterexample class.

**F2 — MEDIUM (verification hazard, realized during this review).** The lane tree moved mid-review:
`5eb8f20f` (freeze) → `03e76ee9` → `3b8af34c` → `d6be05ef` → `8696c4dd`, changing `tools/mado-barfoot.py`,
`quality/counters/c1-r79-reserve.py` and the control set while I was auditing (controls sha went `5f7ebb3c` →
`108bde32` under a running measurement; I re-pinned from git and re-ran). Any seat that hashes or measures
working-tree bytes rather than pinned blobs gets moving-target results during integration. Related design note:
the counter reads `--controls`/`--carried` from the **working tree**, not from the measured revision, and never
validates their sha — the receipt's `control sha256=…` line is the only guard, and nothing in the counter
enforces it. A future generation should accept an expected controls sha (or extract controls from the
revision) so the command alone is self-pinning.

**F3 — LOW.** `killed=12` is anchor-literal-bound: a byte-different but semantically identical correct tool
fails the predicate (trial §2.3: 23/23, killed=11, TARGET_MISSED). Correct for a pinned artifact and it is
what kills lookup-table tools, but the property certified is "these anchors are live in these bytes" — worth
one sentence in the next generation's docstring so nobody reads `killed=12` as implementation-independence.

**F4 — LOW.** Counter `selftest_ok` accepts `MADO_BARFOOT_SELFTEST: 0/0` (group(1)==group(2), no minimum). A
tool with a no-op selftest satisfies the "green tool selftest" clause. Nil impact today; cheap to harden
(`int(group(1)) > 0`).

**F5 — LOW (already mined as M79-5; independently confirmed).** The fetch ledger's self-referential last line
(`a9806336…`) matches nothing: the file cannot contain its own hash, and the hash of its 9 content lines is
`76d9f0a7…`. All 9 content lines verify; the self-line is decorative.

**F6 — INFO.** Carried case `exclusive-false` leaves `expected` unpinned (its `expect` omits the key; the tool
printed 34 unchecked), asymmetric with new case `static-exclusive-false` which pins it. Frozen set — note only.

**F7 — INFO.** No round-79 pin contains the string `addreserved`; the TOP/BOTTOM/LEFT/RIGHT order and the
newest-rule-wins convention rest on the r45 corpus pins S303/S304 (receipts present on disk; sha256
`9db68cf4…`/`17d46685…` match the SOURCES rows; handler read confirms `CReservedArea(top, right, bottom, left)`
from `ARGS[2],ARGS[5],ARGS[3],ARGS[4]`, `:1321-1322`). The declaration's instrument list is accurate about
which rows it re-opened; the load-bearing convention is corpus-carried, which is by design — naming it here so
the dependency is explicit. Also: `S459.bin` ≡ `S466.bin` byte-identical (ReservedArea.cpp re-pin, declared,
benign).

## §5 Residual risk and verification gaps

- Frozen-set overfit beyond the 12 anchors is inherent to the axis: any input class absent from the 23 cases is
  unconstrained. That risk was *realized* by F1 (the bare-addreserved class) and can recur for other classes
  (e.g. scale≠1 and transform≠0 are refused, not modeled — an honest boundary). Mitigation stays the corpus
  discipline: source-pinned rows + case additions on each discovered class.
- C2 is out of my scope (covered by R79RevC2). Live-host behavior was not probed (read-only posture; the new
  knowledge entry records the host observation: no `addreserved` in `~/.config/hypr/**`, live join CLEAN).
- Three receipt files appeared untracked during review (`census-start-r79.txt`, `census-end-r79.txt`,
  `repair-r79-c1-model-r2.txt`) — integration in flight after my audit window; not audited here.
- The freeze-state reproduction (§1) and the attack trials (§2) are reproducible from my archived logs in
  `w1/R79RevC1/` (`rerun-after.log`, `rerun-before.log`, `trial-echo.log`, `trial-commute2.log`,
  `trial-repaired.log`).

Verdict recommendation: the freeze-state C1 measurement is genuinely reproduced (23/23, 12/12, 18/23, 18/18,
43/43, byte-identical receipts at both ends); the round's post-freeze repair was necessary, source-grounded,
and re-measured green at the repaired tip. Trust the repaired generation (`d6be05ef`/`8696c4dd` bytes,
`measurement-c1-r79-repair.txt`), keep the freeze receipt as the before-state record it is.

Report: .ufo/waves/round-79/w1/R79RevC1.md
