# mado round 71 — frozen claims declaration

author: mado L1 (attempt 2; attempt 1 died at launch 2026-11-04T00:06 -03 before any work —
nothing was inherited from it)
date: 2026-11-04 (America/Sao_Paulo)
base: `c354f4d410b829d985b31560af9202d98655dad0` (round-70 closure tip `e2bf3fc7` plus the
routed round-70 seat-report leftovers committed under this round's entry)
round: mado lane counter 71 (hyaku run 15). One v1 wave of 12 seats; the L1 holds the planner seat.

This file is written **before** any candidate measurement at the scored revision. The
pre-freeze receipts are `.ufo/waves/round-71/control-baseline-c1-r71.txt` (the held
round-70 harness on the four new real-child scenarios), `.ufo/waves/round-71/control-baseline-c2-r71.txt`
(the held round-70 classifier on the six new carrier cases) and `.ufo/waves/round-71/proto/`
(the prototype scripts that produced them; they are not the scored counters). Nothing in this
declaration may change after the first candidate run; a miss is an honest stop.

Two claims, distinct axes, causally separable: C1 touches only
`quality/counters/c1-r71-landing-controls.py` and `quality/counters/c1-r71-real-children.py`;
C2 touches only `quality/counters/c2-r71-shapes.py` and the frozen 23-case control set.
Neither reads the other's artifacts. The routed standing-instrument repair
(`quality/landing-counters.sh` default `--citecheck-paths`) is round work, not a claim, and
touches neither instrument; it carries its own red-before/green-after receipt.

Duplicate-source check (lesson M70-3, run at freeze time): both planned C1/C2 rows cite URLs
already held (S108 `subprocess.rst` `05cd782c…`, S439 `expressions.rst` `e19de4fe…`), so no new
row would double-index a page: the round appends **superseding** rows per CORPUS rule 2
(`teaches` opens `supersedes S1NN —`) with fresh anchors, fetched three times this round,
byte-identical to the held pins (receipts `.ufo/waves/round-71/fetch/`).

## Axis posture

Every published finite sub-axis sits at its measured maximum at the base rev (navigation 83/83,
calibration resolved-active 86/86, operability selftest 12/12, ledger 119/119; gate
`MADO_SELFTEST: 460/460`), so no axis is distinctly lowest (rounds 56–70 posture). The
stagnation nudge does not apply: the last capability row entered in round 70 (window N=3, gap 0).
Both claims therefore take **new finite denominators** rather than re-scoring a held rule on
new inputs.

## C1 — calibration: the landing harness credits a kill on the parsed failed assertion even when the child's exit status disagrees

- **Target surface.** The kill-credit decision of the landing control harness
  (`c1-*-landing-controls.py`): the conjunct `mz_rc != 0 AND summary_shows_failure(out)`.
  Round 70 required both a nonzero exit and a parsed failed summary. That still misses a real
  child class: a lane whose assertions genuinely fail but whose exit status is 0 (broken status
  propagation — the mutant escapes classification as a survivor although the lane's own summary
  reports the failure). The exit status cannot carry the assertion result (held ground S441/S435:
  one exit status, many causes); the parsed summary is the assertion signal.
- **Before.** At the base rev the round-71 counter and harness are absent. The held round-70
  harness on the four new real-child scenarios scores `base_correct=3/4`: it credits
  `stderr-genuine`, `liar-kill` and `crash-stderr` correctly but misses `liar-success`
  (`held_mz=fail` where the truth is a credited kill) — receipt § each mode of
  `control-baseline-c1-r71.txt`.
- **After (frozen sentence).** At `REV`, `python3 -I quality/counters/c1-r71-real-children.py
  --repo . --rev REV --base-rev c354f4d4… --scratch-root DIR` prints, as its last line:

  `MADO_R71_REAL_CHILDREN: cases=4 correct=4 base_correct=3 verdict=TARGET_MET rev=<sha>`

  and exits 0. `quality/counters/c1-r71-landing-controls.py` is the scored harness; the held
  base harness is `quality/counters/c1-r70-landing-controls.py` extracted at `--base-rev`.
- **Counting command.** The command above; bounded score `10 × correct / 4` → 10.0000; before
  `correct=absent` (0.0000) with the held harness at `base_correct=3/4` (7.5000).
- **Kill rule (before data).** Four scenarios, each a **real `bash` child** in a scratch git
  repo the counter builds (`git init`, one commit per mode, explicit identity, `-C` on every
  git call). The fixture lane carries the frozen clause `[ "$citations" -gt 0 ] && ` exactly
  once and decides its behavior from that clause's own effect; in every scenario the harness's
  M-Z leg deletes the clause and runs the mutated lane:
  - `liar-success` — the deletion fails the zero-citation assertion; the mutated lane prints the
    genuine summary `MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed` on stdout and
    **exits 0** → the truth is a credited kill → expected `mz=pass`;
  - `stderr-genuine` — the deletion fails the assertion; the genuine summary `1/2` is printed to
    **stderr only**, exit 1 → expected `mz=pass` (the rule stays stream-agnostic);
  - `liar-kill` — the assertions pass (`2/2` printed) and the lane exits 1 for an unrelated
    trailing failure → no failed assertion → expected `mz=fail`;
  - `crash-stderr` — the lane exits 2 with stderr noise and no summary → expected `mz=fail`.
  A scenario is correct iff the harness's own `mz=` field equals the expectation. TARGET_MET iff
  `correct == 4` AND `base_correct == 3`. A harness that always prints `mz=pass` fails
  `liar-kill` and `crash-stderr`; one that keeps the round-70 rule fails `liar-success`.
- **Rule (frozen).** The successor harness credits `mz_killed = summary_shows_failure(out)`
  (the parsed `MADO_LANDING_COUNTERS_SELFTEST: p/n` summary with `p < n`), whatever the exit
  status; a crash or an unparseable summary is never a kill; both streams are read (stdout then
  stderr, the round-70 concatenation order, unchanged); the receipt keeps the exit status
  visible.
- **Sourced ground.** Superseding row over the held S108 bytes (CPython v3.14.8
  `Doc/library/subprocess.rst`), anchor § `subprocess.run`, *capture_output* paragraphs
  (`subprocess.rst:53-56`): "If *capture_output* is true, stdout and stderr will be captured."
  with "the internal :class:`Popen` object is automatically created with *stdout* and *stderr*
  both set to :data:`~subprocess.PIPE`" — the child's own report arrives on captured streams,
  separate from the exit status the counter also sees, which is what makes the summary the
  assertion signal and the streams the reader's duty. The returncode ground stays held
  (S441 rendered page, S435 vocabulary). Row id assigned at adoption; the lesson's `## Gate`
  records access date, sha256 and located quotes.

## C2 — operability: the guard census counts the dict-call splat, the splat-through-alias, the store-through-alias and the attribute-through-second-object shapes while keeping every negative

- **Target surface.** The guard census's classifier: which constructions of the environment key
  `GIT_NO_REPLACE_OBJECTS` count as a guard that reaches a `git` launch.
- **Before.** At the base rev the round-71 counter is absent. The held round-70 classifier
  scores `19/23` on the new 23-case set: it misses `dict-call-splat`,
  `dict-call-splat-object-alias`, `store-through-alias-two-hop` and `attribute-second-object`
  and correctly rejects `unguarded-dict-splat-negative` and `env-call-no-key-negative`
  (receipt § each case of `control-baseline-c2-r71.txt`). These four are exactly the shapes the
  round-70 review disclosed as declared limits (R4) and named as next-set intent.
- **After (frozen sentence).** At `REV`, `python3 -I quality/counters/c2-r71-shapes.py --repo .
  --rev REV --base-rev c354f4d4… --controls .ufo/waves/round-71/controls/c2-controls-r71.json
  --scratch-root DIR` prints, as its last line:

  `MADO_R71_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=23/23 base_controls=19/23 verdict=TARGET_MET rev=<sha>`

  and exits 0.
- **Counting command.** The command above; bounded discrimination score
  `10 × controls / 23` → 10.0000; before `19/23` = 8.2609 by the held rule.
- **Kill rule (before data).** The 23-case set is frozen at
  `.ufo/waves/round-71/controls/c2-controls-r71.json`, sha256
  `d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df`. Seventeen cases are the
  round-70 set carried forward byte-identically; six are new: four carriers and two negatives
  named above. A case is correct iff reader and guard both match its frozen expectation. The
  population, reader and guarded counts are re-derived at `REV` over the round-70 census list
  and must stay `20 / 13 / 13 / 0` (the round-70 production set; this round's new instruments
  are not in it). TARGET_MET iff all six of `population==20`, `readers==13`, `guarded==13`,
  `unguarded==0`, `controls==23`, `base_controls==19`.
- **Rule (frozen).** Round-69 key position and dominance flows and the four round-70 carriers
  stay in force. Added, each still subject to the dominance test:
  (a) *dict-call splat* — `dict(<args>, **M)` where `M` is a module-level mapping literal
  carrying the key (the call treats the mapping's contents as additional keyword arguments);
  (b) *splat through an alias* — a one-hop alias of that module mapping
  (`m = GUARD; env = {**os.environ, **m}`) counts as the splat carrier;
  (c) *store-through-alias* — the key is stored through an alias binding of an env mapping
  (`staging = e; staging[KEY] = "1"`) and the launch hands the env-named mapping;
  (d) *attribute through a second object* — one object-alias edge
  (`cfg.runner = runner`) bridges a dotted attribute store (`runner.env[KEY] = …`) to a dotted
  use (`env=cfg.runner.env`), with the round-70 store-before-use and no-replacement dominance.
  Negatives: a `**` splat of a mapping without the key, and a key-less `dict(os.environ)`, are
  not guards.
- **Sourced ground.** Superseding row over the held S439 bytes (CPython v3.14.8
  `Doc/reference/expressions.rst`), anchor § Calls (`expressions.rst:1415-1417`): "If the
  syntax `**expression` appears in the function call, `expression` must evaluate to a mapping,
  the contents of which are treated as additional keyword arguments." — a `**` operand in a
  call is a real carrier, not a mention, which is what makes the dict-call splat and its alias
  forms count. The attribute/alias resolution is the lane's bounded doctrine, disclosed with its
  bounds. Row id assigned at adoption; the lesson's `## Gate` records access date, sha256 and
  the located quote.

## Control set provenance (frozen)

| file | sha256 | cases |
|---|---|---|
| `.ufo/waves/round-71/controls/c2-controls-r71.json` | `d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df` | 23 |

The 17 held cases are byte-identical to `.ufo/waves/round-70/controls/c2-controls-r70.json`
(`29947b4c…`). The counter must assert both digests and refuse (rc 2) on a mismatch.

## Not claimed

Universal fault coverage; that four scenarios exhaust the kill-credit hazards; that the fixture
lane represents the lane's real landing instrument; that a summary-only rule is sound against an
adversarial child that forges a failing summary (a forged summary is byte-indistinguishable from
a genuine one — the round-70 agreement-only stand-in limit applies here with the sign flipped);
that the four new carriers are the only remaining Python shapes; that the alias/attribute
resolution is sound for arbitrary Python (one hop, one object-alias edge, exact dotted names, no
container flow, no path-sensitivity beyond a literal-false branch); runtime behaviour of the
extracted instruments; desktop, compositor, session, service or package state (none is probed
this round); any `[x]`, promotion or axis retirement.

## Harm watch

`bash tools/mado-verify.sh --selftest` stays `n/n`; `quality/landing-counters.sh --round 71
--citecheck-paths <committed round receipts>` ends GREEN once the round's artifacts land (the
default-path defect is repaired separately with its own red/green receipt);
`quality/counters/c1-r70-real-children.py --rev REV` stays `cases=3 correct=3 base_correct=1
TARGET_MET` and `quality/counters/c2-r70-carriers.py` stays `controls=17/17 base_controls=13/17
TARGET_MET` at the tip (the frozen round-70 counters must keep passing: the round-70 harness and
classifier files stay byte-identical); `quality/landing-counters.sh --round 69 --citecheck-paths`
stays GREEN on explicit committed paths; `quality/check-axis-scores.py` re-derived;
`quality/check-tool-ledger.py` green with the three new instrument rows; no config tree,
compositor, service or sibling repo is written.
