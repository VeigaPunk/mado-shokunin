# mado round 71 — lesson

author: mado L1 (the scored instruments are the L1's own; the one w1 wave's seats attack them).
date: 2026-11-04 (America/Sao_Paulo)
base: `c354f4d410b829d985b31560af9202d98655dad0`
frozen declaration: `.ufo/waves/round-71/claims-declaration-r71.md`, `4a91c644289437b588881a7254481157decfa450`
control set: `.ufo/waves/round-71/controls/c2-controls-r71.json`, sha256
`d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df` (23 cases)
pre-freeze baselines: `.ufo/waves/round-71/control-baseline-c1-r71.txt` and
`.ufo/waves/round-71/control-baseline-c2-r71.txt`
measured content: `3868bc659621fd1ffeb46d8a2040b1f327ae3444` (C2 carries the reviewer-driven
dominance repair; the frozen 23 score identically at `8e78a4ee` and at the repair commit;
measurement `.ufo/waves/round-71/measurement-r71.txt` records both runs)

## Outcome and boundaries

Two bounded claims, both frozen before any candidate data.

- **C1 calibration — the landing harness credits a kill on the parsed failed assertion even
  when the child's exit status disagrees.** At the measured revision the frozen counter
  `quality/counters/c1-r71-real-children.py` builds a scratch git fixture whose lane decides
  its behaviour from the frozen clause's own effect, runs four real `bash` children
  (`liar-success`: a genuine `1/2` summary with exit 0; `stderr-genuine`: the genuine summary
  on stderr only; `liar-kill`: a passing `2/2` summary with exit 1; `crash-stderr`: exit 2 with
  no summary) against the round-71 harness (`c1-r71-landing-controls.py`, whose M-Z credit is
  `summary_shows_failure(out)` alone) and the byte-frozen round-70 harness, and requires
  `correct=4 base_correct=3`. Measured exactly that, rc 0. The held harness misses
  `liar-success` and only it — the do-nothing control. The reviewer confirmed the sole
  behavioural delta is the dropped `mz_rc != 0` conjunct and that a combined
  stdout-then-stderr read is the only reader scoring 4/4 (`w1/R71RevC1.md`).
- **C2 operability — the guard census counts four more carrier shapes.** At the measured
  revision `quality/counters/c2-r71-shapes.py` applies the held round-70 rule plus (a) the
  dict-call `**` splat of a module mapping carrying the key, (b) the splat through a one-hop
  alias of that mapping, (c) a key store through a one-hop alias of the mapping handed to the
  launch (rebinding dominance over both names, whatever their spelling), and (d) an attribute
  store bridged to a dotted use by one object-alias edge (`cfg.runner = runner`, with
  store-before-use, edge-resolved replacement dominance, and the edge bound strictly before
  the call). The frozen 23-case set carries the round-70 seventeen cases byte-identically and
  adds four carriers and two negatives. Measured `population=20 readers=13 guarded=13
  unguarded=0 controls=23/23 base_controls=19/23 verdict=TARGET_MET` rc 0; the held round-70
  classifier scores 19/23, missing exactly the four carriers.

**Not claimed.** Universal fault coverage; that four scenarios exhaust the kill-credit
hazards; that a summary-only credit rule is sound against an adversarial child that forges,
stales or echoes a failing summary (byte-indistinguishable from a genuine one — the round-70
agreement-only stand-in limit applies with the sign flipped); that the fixture lane is the
lane's real landing instrument; that the four carriers are the only remaining Python shapes;
that the alias and attribute resolution is sound for arbitrary Python (one hop, one edge,
exact dotted names, no container flow, no path-sensitivity beyond a literal-false branch);
runtime behaviour of the extracted instruments; desktop, compositor, session, service or
package state (none was probed); any `[x]`, promotion or axis retirement.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M71-1: the round-70 closure left four seat-report files uncommitted in the lane working tree (`R70ScribeEntryC1.md`, its draft entry, `R70ScribeEntryC2.md`, `R70ScribeRowLesson.md`); the outside verifier routed them to round 71. | record order across rounds (inherited) | `corpus/lessons/round-70-verifier-spotcheck.md` step-1 defect; the files sat modified across the round boundary; committed under this round's entry at `c354f4d4` | `none` at r70 — the closure's step-1 uncommitted-work check caught it, and no lane criterion required committing a wave's seat reports before WAVE-DONE is answered | This round commits inherited lane-authored files before its freeze (commit `c354f4d4`, first of the round). QUALITY criterion 114 makes the rule checkable: the failure it shows is a wave seat report still modified in the working tree after the round's report lands. |
| M71-2: `quality/landing-counters.sh`'s default `--citecheck-paths` resolves `.ufo/waves/round-<N>/receipts`, a directory no round had committed, so the default invocation always died as a setup error (r70 erratum E2; the verifier's routed defect 2). | instrument default unusable | red-before receipt `.ufo/waves/round-71/m71-2-red-before-r71.txt` (`--round 70` → rc 2, `citecheck path missing`) | `none` — the lane's own r70 cadence seat found it and routed it; no criterion required an instrument's default path to resolve against committed bytes | This round commits its receipts at `.ufo/waves/round-71/receipts/` (the repair option the verifier named): the `--round 71` default invocation resolves committed bytes and runs GREEN at the tip. The failure the fix shows: a `--round N` default whose receipts dir does not exist at `N`. |
| M71-3: the first C2 widening shipped two dominance bypasses inside the declared envelope — `splat_aliases` credited an alias rebound before the splat (F1), and `attribute_flow` accepted an object-alias edge bound after the call (F2). | predicate implementation wider than its own frozen sentence | `w1/R71RevC2.md` F1 (HIGH) and F2 (MEDIUM), each with a repro source whose runtime truth is unguarded while the widening scored `(True, True)`; red-before re-run at the pre-fix blob `8e78a4ee` in `.ufo/waves/round-71/c2-dominance-repair-r71.txt` | the frozen sentence itself ("each still subject to the dominance test") — the declaration's words were right and the implementation was not; no census case caught it because the frozen 23 contain neither shape | Repaired at `3868bc65` against the same sentence: the alias must be bound exactly once and unrebound between binding and splat; the edge must predate the call. Green-after receipt; both repro sources pinned as counter regressions (`r71-splat-alias-rebound-before-splat`, `r71-attribute-edge-after-use`; selftest 63/63). The failure the fix shows: a bypass fixture flipping from credited to refused at the same revision. |
| M71-4: 11 of the wave's 13 seats settled `ok` with empty final outputs and wrote no seat files; only the two reviewer seats delivered reports. | swarm evidence gap (inherited: orchestrator-side capture/seat-side delivery; cause `[UNK]` from the lane's side) | `.ufo/waves/round-71/w1-results.json`: 13 entries, every `status` ok, `output` empty for 11; only `R71RevC1.md` and `R71RevC2.md` exist in `w1/` | `none` — the run-9 lesson pinned counters that bind seat votes to seat-written files, but no counter here binds seat votes; no criterion required per-seat file receipts at wave settlement | The round reports the evidence gap instead of papering over it: the wave's verification value rests on the two delivered reviews plus the L1's own re-runs (both counting commands, harm watch, census). A future wave context should require each seat to end with one line naming its written report path, so a silent seat is visible in `results.json` itself. |

A fix counts only on its named red/green evidence: M71-1's green is the `c354f4d4` commit; M71-2's
red/green pair is `m71-2-red-before-r71.txt` and the landing-time GREEN default run recorded in
the wave dir; M71-3's pair is `c2-dominance-repair-r71.txt` (pre-fix blob credits both bypasses,
repaired counter refuses both); M71-4's "fix" is the disclosure plus the future-wave-context
rule (its failure mode is the empty-output row in the next results file).

## Gate

Admitted, **S442** — CPython v3.14.8 `Doc/library/subprocess.rst`, § `subprocess.run`,
capture_output paragraphs (superseding row over the held S108 bytes).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (`sha256`
  `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`, 61,603 bytes — the
  digest S108 already records); fetch receipts `.ufo/waves/round-71/fetch/`.
- Located quote A, 11 words, subprocess.rst:53: "If capture_output is true, stdout and stderr
  will be captured."
- Located quote B, 15 words, subprocess.rst:54-55: "the internal Popen object is automatically
  created with stdout and stderr both set to PIPE".
- Why it grounds the claim: a child's own report arrives on captured streams, separate from
  the exit status — the summary is the assertion signal and both streams are the reader's
  duty. CORPUS rule 2 mechanics: this is a NEW row whose `teaches` opens `supersedes S108 —`;
  S108's cells do not change (its scope stays the `args` binding).

Admitted, **S443** — CPython v3.14.8 `Doc/reference/expressions.rst`, § Calls (superseding
row over the held S439 bytes).

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst`
- Access date: 2026-11-04, fetched three times, byte-identical (`sha256`
  `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92,034 bytes — the
  digest S439 already records).
- Located quote, 25 words, expressions.rst:1415-1417: "If the syntax `**expression` appears in
  the function call, `expression` must evaluate to a mapping, the contents of which are
  treated as additional keyword arguments."
- Why it grounds the claim: a `**` operand inside a call adds the mapping's contents as
  keyword arguments, so `dict(os.environ, **GUARD)` builds a mapping that carries the key —
  the dict-call splat and its alias forms are real carriers, not mentions. CORPUS rule 2
  mechanics: new row, `teaches` opens `supersedes S439 —`; S439 keeps its dictionary-display
  scope and every cell.

Rejected: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/stdtypes.rst`
as a new row. Reason: the mapping-methods page documents method behaviour (`dict.update`,
`setdefault`), not the call/expression semantics these claims rest on; the language reference
is the tier-A surface for them, and the classifier's `update`/`setdefault` clause is already
held from r69 without a fresh row. Flip condition: a claim whose subject is mapping-method
behaviour (not call syntax) re-opens it then.

Registry cell changes (old → new, logged per CORPUS rule 2): none — both new rows are
appends; S108 and S439 keep every cell (the supersede pointer lives in the new rows'
`teaches`). No `status` or `recheck` cell changed anywhere. The registry diff is +2 rows
(378 → 380).

## Wave findings

The orchestrator sent WAVE-DONE for the one v1 wave: 13 seats dispatched in one batched call,
all 13 settled with `status: ok`, zero dead seats (`.ufo/waves/round-71/w1-results.json`).
Material findings and dispositions:

- **C2's widening had two dominance bypasses** (`w1/R71RevC2.md` F1 HIGH, F2 MEDIUM).
  Repaired against the frozen sentence at `3868bc65`; red-before/green-after in
  `c2-dominance-repair-r71.txt`; both repro sources pinned in the counter's selftest (63/63).
  The frozen 23 score identically before and after; the per-file census over the production
  files is unchanged (13 readers, 13 guarded).
- **C1's predicate is sound as bounded** (`w1/R71RevC1.md` verdict; the sole behavioural delta
  is the dropped rc conjunct, and the four fixture modes behave as the receipt records on
  real bash runs the reviewer executed itself). Its F1–F6 findings are disclosures, not
  blockers: the stale/canned-summary class, the mutation↔summary evidentiary link, the
  verdict-level red→green flip on the selftest leg (which still keys on exit status), the
  last-wins multi-summary rule, and the {0,1,2}-rc indistinguishability are all named in the
  entry and the report.
- **The evidence gap**: 11 seats returned empty outputs and wrote no files (M71-4). The
  reviewer seats carried the round's independent verification; the L1 re-ran everything else
  itself. No counter binds seat votes, so no frozen result depends on the missing seats.
- `check-deliverables.py`'s round-69 red state and the fleet-root `after` stub are
  pre-existing/other-lane artifacts — observed, not repaired, per the r70 closure's routing.

Assimilation: none this round — no `merge/mado/` theme was taken. `considerthese/2026-10-28.md`
proposal 4 (a live-tool table) remains named-not-adopted (it governs live-state instruments on
a probed host; this round probes no host).
