# CritClaimSizing — round 45 (mado), inline w1: attack on claim sizing before any data

Seat: `CritClaimSizing`. Claims attacked: **C1** (`tools/mado-monitors.py`, `PRED-C1-r45`) and **C2**
(`corpus/knowledge/hyprland-monitor-rule-r45.md`, `PRED-C2-r45`).
Frozen inputs, read only: `.ufo/waves/round-45/registration.md` (freeze `22a8dedd02f507689c567777e0f20b5e645c8ce0`,
base `0c89478af821a6424c9ac922eafe02e39630cf4f`), `quality/counters/c1-r45-monitors.py`,
`quality/counters/c2-r45-monitor-entry.py`, `receipts/ctl-c1.txt`, `receipts/ctl-c2.txt`,
`receipts/axis-base.txt`, `receipts/c2-ground-base.txt`, `/home/vgpnk/Projects/shokunin/AXES.md`,
`corpus/README.md` `## Frontier`, `corpus/QUALITY.md`, `SCORECARD.md`.
**No lane file was edited, no counter/control/registration/pin touched, no mutating git/jj in the lane.**
All clones/fixtures/work dirs live under `/fast/scratch/hyaku/mado-r45/CritClaimSizing` (removed at exit);
receipts below are copied from there into this seat dir.

Scoring commands (unchanged, as frozen):

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r45-monitors.py \
  --repo <clone> --rev HEAD --work /fast/scratch/hyaku/mado-r45/CritClaimSizing/w [--seed N]
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r45-monitor-entry.py \
  --repo <clone> --rev HEAD --base 0c89478af821a6424c9ac922eafe02e39630cf4f
```

## Scoreboard — controls built beyond the registered set

Every clone is `git clone -q --shared --no-checkout` of the lane, `git -C <clone> rev-parse --show-toplevel` equals
the clone, detached at the freeze, then one commit by a scratch identity (`seat@scratch.invalid`).

| id | control (what it skips) | commit | frozen-counter line | verdict | receipt |
|---|---|---|---|---|---|
| K16 | freeze copy: `git show 22a8ded:.ufo/waves/round-45/l1-draft/mado-monitors.py > tools/mado-monitors.py` — zero implementation by the round | `bcf1629e3678` | `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET` | **MET** (= registered REF, by design) | `e1-freeze-copy.log` |
| K17 | oracle replay: 71-line tool `exec`s the frozen counter's own prefix, brute-forces the seed from the inputs, prints its expected bytes; no Hyprland semantics | `afb31b7adc4a` | `fixtures=49/49 … TARGET_MET` seed 45 **and** `seed=777` | **MET — attack** | `e2-oracle-seed45.log`, `e2-oracle-seed777.log`, `oracle-replay-tool.py.txt` |
| K18 | draft promotion: `l1-draft/entry.md` copied to `corpus/knowledge/` and nothing else | `8938be2fb94f` | `clauses=a:1 b:1 c:0 d:0 e:0 f:0 g:0 h:0 i:0 j:1 admitted=0/1 MISSED` | MISSED — no reach | `e5-draft-only.log` |
| K19 | citation-only entry: registered P tree with **every** line carrying no `S3xx` id, no pin locator and not the census line replaced by `Lorem ipsum …` | `7d3ae115819d` | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1/1 TARGET_MET` | **MET — attack** | `e6-quote-only.log` |
| K00 | freeze tree, no change (registered before state re-derived) | `22a8dedd02f5` | C1 `fixtures=0/49 tool=absent MISSED`; C2 `admitted=0/1 MISSED` | no reach | `k00-freeze-do-nothing-c1.log`, `k00-freeze-do-nothing-c2.log` |
| P (reproduced) | registered positive control `l1-draft/build-pos.py` on the freeze clone | `1e776f1ed59e` | C2 `admitted=1/1 TARGET_MET`; C1 `fixtures=0/49 tool=absent TARGET_MISSED` | reproduces `ctl-c2.txt` P; C1/C2 separable | `p-tree-c2.log`, `p-tree-c1.log`, `e1-c1only-c2.log` |

The registered set (`receipts/ctl-c1.txt`: REF + K00–K15; `receipts/ctl-c2.txt`: P + 9 rejects) contains no
**oracle-read** and no **citation-only** shape; both reach their targets.

---

## F1 [HIGH] C1's counter runs the tool under test with the judge readable — an oracle-replay tool reaches 49/49 at two seeds

**Exact sentence** (`quality/counters/c1-r45-monitors.py:12`): "the tool is extracted to a fresh directory under --work,
each fixture runs `python3 -I <tool> <args>` with its own fresh working directory, environment exactly
{PATH, LANG=C.UTF-8, HOME=<fresh dir>, HYPRLAND_INSTANCE_SIGNATURE=mado-r45-fixture}" — and the environment is exactly
that (`:311` `env = {"PATH": fakebin + ":/usr/bin:/bin", …}`). Nothing hides the counter's file, its `FIXTURES`
table (`:80`) or anything else on the host filesystem; `-I` isolates module import, not file reads.

**Counterexample.** `oracle-replay-tool.py.txt` (71 lines, committed as `tools/mado-monitors.py` at `afb31b7adc4a`):
it opens the frozen counter at its absolute path, `exec`s the prefix before `def run_fixture` — which yields the
counter's own `names`, `subst` and `FIXTURES` — brute-forces the seed from the config/dump bytes it was given, and
prints the expected lines verbatim. No rule is parsed, no dump joined, no scale correction, no verdict computed.

```
PRED-C1-r45: fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=afb31b7adc4ae84a233b4e542b8402c6297117d5 seed=45
PRED-C1-r45: fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=afb31b7adc4ae84a233b4e542b8402c6297117d5 seed=777
```

Seed independence is the point: round-44 closure D4 (seeded output names) stops a *fixed-text* fake — the round-44
`cheat-a-fixed-bytes` control scored 19/26 — but not a tool that reads the judge's derivation. `selftest=ok` is
free (it prints `MADO_MONITORS_SELFTEST: 33/33 passed` and exits 0); `readonly=ok` is free (it never runs a PATH binary).

**Why it matters.** This is not a declared residual; it is the lane's own admitted bar being violated:

* `corpus/QUALITY.md:379` (criterion 66): "runs it in a boundary that hides the judge (its code, its seeds'
  derivation, its call log and its table)" — the round-45 counter runs unsandboxed, on the same filesystem.
* `corpus/QUALITY.md:393` (criterion 73): "a tool that reaches the verdict by reading the stub's bytes or
  replaying an on-disk copy is not running the program".
* `corpus/QUALITY.md:324` (criterion 36): "the receipts name the shortcut shapes the closures have seen meet a
  counter (do-nothing, all-false/empty, junk, server echo, label- or fixture-keyed, no-reader)" — `ctl-c1.txt`
  names REF, base-absent, a copied other tool, a naive stub and 12 semantic mutants; **no fixture-keyed/oracle-read
  and no no-reader shape**.
* Round 44 already paid for this class: `.ufo/waves/round-44/w1/CritC1Cheat.md` §1 records the round-42 counter's
  bubblewrap profile (`c1-r42-geometry.py:153-168` `sandbox_cmd`, `HOME=/nonexistent`) and a cheat that flipped
  behaviour on the sandbox fingerprint. Round 45's counter has no sandbox at all: `grep -c sandbox
  quality/counters/c1-r45-monitors.py` → `0`.

**Impacted axes.** operability (the claimed capability is reachable without it: the target is a byte equality, not
the join), calibration (the control receipt's "0 of 16 MET" is true of 16 controls and false of the class the
lane's own criterion names).

**Smallest safe correction.** Keep the contract and the fixtures; change only how the tool is run: wrap the fixture
call in the round-42 `bwrap` profile (`--ro-bind /usr /usr --ro-bind /bin /bin --bind <fixture dir> <fixture dir>
--tmpfs /home/vgpnk/Projects`), so the counter's file and table are not reachable, and record the tool's `openat`
attempts judge-side (criterion 66's "records requests on the judge's side"). Then add K17 (oracle replay) to
`ctl/run-c1-controls.py` with expected `TARGET_MISSED` (prediction, **not run here**: under that profile the
reference's 49/49 does not change and the oracle cannot open its source, so K17 falls to 0/49). If no sandbox can be used on this host, the counter must be declared to measure "agreement with the
counter's own model" and the claim cannot be a capability acquisition.

---

## F2 [MEDIUM] The cheapest route to C1's target is a one-command install of the pre-frozen reference; the control receipt does not carry it

**Exact sentence** (`registration.md:18-19`): "Prior art at base, disclosed: `tools/mado-verify.sh:3518-3530` checks one hardcoded output"
(`:18`) "(DP-1 3440x1440 within 0.5 Hz of 100) without reading any rule" (`:19`) — accurate (see F5) — but the
prior-art paragraph omits the answer key committed in the same freeze.

**Counterexample.** K16: one `git show 22a8dedd…:.ufo/waves/round-45/l1-draft/mado-monitors.py > tools/mado-monitors.py`
plus a commit is `fixtures=49/49 … TARGET_MET` (`e1-freeze-copy.log`, rev `bcf1629e3678`). This is the same fact as
round 44's `w1/CritClaimSizing/findings.md` F6 ("C1's target is reachable by a 30-line local patch (and by copying
the committed reference)"). It is registered as REF (must be MET), so it is disclosed by design — the sizing
consequence is what the registration does not say: C1's "capability acquisition" lands by *installation*, and the
round's own marginal work is verification. `ctl-c1.txt` counts 16 controls and none of them is "the reference
installed by copy", so a closure reading that line cannot tell an install from a build.

**Impacted axes.** operability (the before→after measures a tool's presence, not the round's construction of it),
calibration (the receipt's control tally does not include the cheapest reaching route).

**Smallest safe correction.** One added control line in `ctl-c1.txt` — `K16-REF-INSTALL (the freeze reference copied
as the tool): TARGET_MET`, labeled as expected-MET — and one clause in the registration's C1 paragraph: "the data
commit may install the frozen reference; the claim measures the installed tool's behaviour, not its authorship".

---

## F3 [MEDIUM] C2 admits a citation-only entry: every non-citation line can be `Lorem ipsum`, including the host observation and `Limits`

**Exact sentence** (`registration.md:54-55`): "clause j binds a locator and a keyword" (`:54`) "per surface, not the truth of the sentence"
(`:55`) — the declared residual is about a sentence's truth, not about the entry being able to contain no prose.

**Counterexample.** K19: the registered P tree with every line that carries no `S3xx` id and no pin locator (and is
not the census line) replaced by `Lorem ipsum dolor sit amet, consectetur adipiscing elit.`, committed at
`7d3ae115819d`, scores `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1/1 TARGET_MET`
(`e6-quote-only.log`). The lines this deletes include the entire `## §6 On this host` observation (the only live
fact), its `**UNK**` honesty line, all three `## Limits` bullets and every section heading. The kept bytes are the
citation-bearing fact lines, the 20-line header and the census line — i.e. the counter admits a quote salad.

This is the route round 44's `findings.md` F1 found ("18-line quote-only entry: C2 TARGET_MET") surviving the
round-44 v2 counter and its new clause j width bound: the width bound constrains locators, not prose. The control
set (`ctl-c2.txt`) has SHELL, WIDE-RANGE, HIDDEN-LINE, FORGED-PIN, FALSE-URL, PROSE-CENSUS, ANCHOR-PAST-EOF and
R14-COPY — none of them the citation-only shape.

**Impacted axes.** coverage (the claim's own artifact is the surface; the counter measures citation scaffolding, so
an admitted entry can have no synthesis, no limits and no host section), calibration (the after-state `admitted=1/1`
is read as "the entry exists and is sourced" when it means "the citation lines are well-formed").

**Smallest safe correction.** One clause (k): the entry must carry the host receipt line and the `Limits` bullets
bound to their locators — e.g. `>= 2` unfenced `- ` bullets outside the first 20 lines whose locator resolves into
`.ufo/waves/round-45/receipts/`, and no unfenced line outside the first 20 may be identical to another (placeholder
detector). Cheaper alternative, if the wider residual is intended: say in the registration that non-citation prose
is unmeasured, and register K19 (citation-only) in `ctl-c2.txt` with its expected verdict made explicit.

---

## F4 [MEDIUM] The lowest-axis argument rests on a staleness check over three axes, has no coverage row, and both after-states are counter verdicts, not scores

**Exact sentence** (`registration.md:9-10`): "`MADO_AXIS: checked=3 mismatched=0` (navigation 61/61, calibration 71/71,
operability 12/12): every published axis" (`:9`) "ties at its maximum, so each is a lowest axis and the claims'
after-states are their counters' lines" (`:10`).

**Counterexample.**

* `quality/check-axis-scores.py:32` `AXES = ("navigation", "calibration", "operability")`; its docstring says "Axes
  the gate cannot re-derive are not checked and are not claimed". `receipts/axis-base.txt` prints exactly those
  three rows — **no coverage row**, so it cannot support C2's coverage claim at all, and it says nothing about
  ranking (§9: "Name the axis by the surface the round changes, not by the number it produces").
* The coverage axis C2 names has no live rubric to tie at a maximum: `sourced-art` is retired —
  `SCORECARD.md:2298` "`sourced-art` was published at 1.0 in round 32 as `10 × covered U-items / 7`, was dropped".
* The nudge is not waived: `SCORECARD.md:601` "Saturation remains 9.0, stagnation window N=3; retired axes: none."
  and a capability entered in round 44 (`SCORECARD.md:2579` "state-aware rule size versus reported size join …
  | 44 |"), inside the three-round window, so the nudge is not waived and the lowest-axis obligation stands — it
  must then be met by a *numbered* sub-axis, which is what round 44's F9 already asked for and round 45 did not
  add. (The tie reading itself — all three published fractions are 1.0, so each is tied-lowest — is formally
  defensible; the defect is the missing per-axis number, not the reading.)
* Consequence for the claims: C1's after-state is `fixtures=49/49 … TARGET_MET`, C2's is `admitted=1/1`; neither
  moves a published number (operability's published fraction is `quality/check-index.py --selftest` 12/12, which
  reads neither the tool nor the entry).

**Impacted axes.** calibration (compliance is asserted from a receipt that measures staleness, not ranking or
coverage).

**Smallest safe correction.** Two sentences in the registration's "Lowest axis" block: (a) state the nudge status
("saturation 9.0 / N=3; a capability entered in round 44, so no waiver") and (b) name each claim's new bounded
sub-axis with a 0–10 before→after and its counting command — e.g. "monitor-rule join verdicts: 0/6 → 6/6 on the
declared contract classes (AGREE/DIFFER/DISABLED/UNRULED/NOT_COMPARED/NO_RULES)". Or add the coverage row to
`quality/check-axis-scores.py`'s derivation and re-run it.

---

## F5 [PASS] C1's surface is genuinely unheld — prior art is only the hardcoded DP-1 row

**Exact sentence** (`registration.md:18`): "`tools/mado-verify.sh:3518-3530` checks one hardcoded output (DP-1
3440x1440 within 0.5 Hz of 100) without reading any rule".

**Check.** `tools/mado-verify.sh:3526` is
`ok = (x.get('width') == 3440 and x.get('height') == 1440 and abs(float(x.get('refreshRate', 0)) - 100) < 0.5)` —
a single name filter (`x.get('name') == 'DP-1'`), no config read, no rule list, no per-output verdict, no
transform/mirror/scale comparison. The other two tools that mention a monitor are not prior art:
`tools/mado-options.py:1229` is a *directive-verb fixture* (`monitor = DP-1, …` sits in the sample config whose
verbs must never enter the option table), and `tools/mado-wsrules.py:632` reads a `monitor:` field *inside a
workspace rule* (`rule.monitor = field[delim + 8:]`), not the monitor rule plane. So the rule→dump join is new and
C1 is an operability surface move — on an unpublished sub-axis (F4), which is the sizing defect, not the axis.

---

## F6 [PASS] Separability holds in both directions

**Check.** C1's counter reads only `tools/mado-monitors.py` at REV (clause a `git ls-tree`, blob via `git show`);
C2's reads `corpus/knowledge/hyprland-monitor-rule-r45.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md`,
`corpus/README.md` and `fetch/` — no tool. Exercised on my trees:

* C1-only tree (K16, `bcf1629e3678`): C1 `TARGET_MET`; C2 `admitted=0/1 TARGET_MISSED` (`e1-freeze-copy.log`,
  `e1-c1only-c2.log`).
* C2-only tree (P, `1e776f1ed59e`): C2 `admitted=1/1`; C1 `fixtures=0/49 tool=absent TARGET_MISSED`
  (`p-tree-c2.log`, `p-tree-c1.log`).

No coupling found. Caveat, not a coupling: because the C1 counter is reachable by an install (F2) and by oracle
replay (F1), a partial C1 that lands "any readable tool" passes — fix F1/F2 rather than changing this statement.

---

## F7 [LOW] C2's ground receipt omits the round-14 entry the claim says it moves

**Exact sentence** (`registration.md:42-44`): "U5 output management, the "runtime state agreement" the round-14
entry left UNK (`corpus/knowledge/output-colour-boundaries-r14.md`)".

**Check.** `receipts/c2-ground-base.txt` runs the claim grep (`exit=1`) and lists "held neighbours (disclosed, not
the claimed ground)" as the round-3 `99.997` point sample and the workspace-rule selector — but **not** the round-14
entry named in the same sentence. The entry does leave the surface open (`output-colour-boundaries-r14.md:91`):
"Output test/apply, resulting monitor state, persistence across restart, hotplug race behavior, HDR rendering" …
"remain unexercised" — so C2 is new ground for the chain, and `corpus/README.md`'s frontier says the same ("Output
test/apply, runtime state agreement … remain unknown"). The receipt's disclosure set is therefore incomplete, not
wrong.

**Impacted axes.** coverage (the ground receipt is the surface evidence), calibration (a neighbour the claim itself
names is absent from its receipt).

**Smallest safe correction.** Append the r14 line and its `:91` `[UNK]` sentence to the held-neighbours block of
`receipts/c2-ground-base.txt` (the file is frozen, so the L1 should add the line at the next freeze, not edit it
now), or add one registration sentence saying why r14 is not counted as a neighbour.

---

## Asked attacks 1–6 — ledger

1. **Cheapest reaching control.** C1: K17 (oracle replay) **MET** at seed 45 and 777 — beyond the registered 16
   (F1); K16 (freeze copy) **MET** as designed (= REF, F2). C2: K19 (citation-only) **MET** (F3); K18 (draft
   promotion alone) **MISSED** — the rows/lesson clauses do carry work (`c:0 d:0 f:0 …`). So *both* targets are
   reachable by a control that skips the claimed work; for C1 that control is the frozen counter's own table.
2. **C1's axis move.** Surface named: the rule→dump join (`monitor =` grammar, rule store/lookup, closeness bound,
   1/120 scale correction, JSON fields) per output with AGREE/DIFFER/DISABLED/UNRULED/NOT_COMPARED. Prior art
   `mado-verify.sh:3518-3530` is one hardcoded name/mode check and reads no rule — so the surface is new (F5);
   the *published* operability number does not read tools at all, so the move is on an unpublished sub-axis (F4).
3. **C2 ground.** New sub-surface, not a deepening: r14 covers the protocol/document boundary (S047/S048/S050) and
   explicitly leaves runtime agreement `[UNK]` (`output-colour-boundaries-r14.md:91`); r3 holds only the `99.997`
   point sample (`config-health-report-r3.md:380`); the chain (parser → handler → manager → apply → JSON) has no
   corpus hit (`c2-ground-base.txt` claim grep `exit=1`). The one gap is the receipt's neighbour list (F7), and the
   coverage *number* cannot move because `sourced-art` is retired (`SCORECARD.md:2298`) — a calibration point (F4).
4. **Universal clauses.** No unenumerated universal in either predicate: C1 `f`/`s`/`r` quantify over committed
   constants (`FIXTURES` 49, `SELFTEST_MIN` 30, four PATH binaries); C2 `a`–`j` quantify over cited ids, the six
   census fields, `PINS` and the 17 `SURFACES` constants, and `b`'s "no `S###` token … that is not a cited id" is
   a full-file scan. The registration's one universal, "every published axis ties at its maximum"
   (`registration.md:9`), is quantified over the gate's three-axis set — enumerated by
   `check-axis-scores.py:32` — so it passes the letter of §9 while omitting coverage (F4). No "no harm anywhere"
   phrasing appears in the frozen text.
5. **Lowest-axis argument.** `receipts/axis-base.txt` is a published==derived staleness check over 3 axes
   (`navigation 61/61`, `calibration 71/71`, `operability 12/12`), not a ranking and not a coverage measure; both
   claims' after-states are counter lines; saturation is 9.0 with N=3 and capabilities entered in rounds 37–44, so
   the nudge is not waived. The tie reading is formally defensible ("each is a lowest axis") and is the round-44
   F6/F9 practice, but the obligation AXES asks for — a numbered per-axis delta — is still absent (F4).
6. **Separability.** Holds both ways on built trees (F6): `bcf1629e3678` C1-only and `1e776f1ed59e` C2-only.

---

## Quote verification

`verify-quotes.sh` greps each quoted span in its cited file at its computed line; output in `verify-quotes.log`
(all `OK`). Locators were computed with `grep -n`, never typed from memory.

## Receipts in this seat dir

`e1-freeze-copy.log`, `e1-c1only-c2.log`, `e2-oracle-seed45.log`, `e2-oracle-seed777.log`,
`oracle-replay-tool.py.txt`, `e5-draft-only.log`, `e6-quote-only.log`, `p-tree-c1.log`, `p-tree-c2.log`,
`verify-quotes.sh`, `verify-quotes.log`.
