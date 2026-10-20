# AtkCasesH3 — partly falsified: 1 of 42 AdoptW2 expectations is wrong against the registered contract and inverts the suite's scoring gradient; 41 wants hold, but 2 of those rest on falsified measurements and 1 on a misleading rationale.

Leaf scout, slice = the 42 `CaseAdoptW2--` cases in `.ufo/waves/round-20/precision/`
(H-family focus: the 9 H cases), their `expected.json` rows (`want_exit`,
`want_findings[].evidence`, `before`, `why`) and their `why` justifications. Lane tip
`a4046a8`; tool bytes and case bytes read from git into a /tmp clone
(`/tmp/mado-r20w2-AtkCasesH3`); all git/jj experiments in fresh `/tmp` repos with
`HOME`/`XDG_CONFIG_HOME`/`GIT_CONFIG_NOSYSTEM` redirected. I wrote no tracked lane file
and ran no host probe. Every command below was run; receipts:
`.ufo/waves/round-20/w2/AtkCasesH3/receipts.txt`, matrix
`…/atkcasesh3-matrix.json` (my scan of the 42 cases under the counter's rule), full
committed-counter outputs `…/counter-<rev>.json`.

## Reproduced claims (hold)

- Tool sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` at
  `28c6837`, `367be94773d8…` at `1f7f995`, `c1ae45a7573e…` at `9c54c56` — match the
  SCORECARD.
- Committed counter run from the clone (`python3 -I .ufo/waves/round-20/tw-precision.py REV`):
  `28c6837` **172/175** = 9.8286 (P 66/66 S 17/17 W 21/22 H 51/52 L 17/18);
  `1f7f995` **29/175**; `9c54c56` **110/175**. Score, families and the 3 fails
  (`W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`,
  `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`) reproduce exactly. My 42-case slice:
  40/42 at `28c6837`, 2/42 at `1f7f995`, 29/42 at `9c54c56`.
- `expected.json` blob `c456ab0de54d15f5…` at both `f3da504` and `a4046a8`;
  `git diff --stat f3da504 a4046a8 -- precision precision-heldout` is empty. The suite was
  not edited after the tool change. All 42 per-case `sha256` fields match committed bytes.
- All 42×2 `before` readings match my re-measurement (0 mismatches).

## F1 — wrong expectation (H): `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`

Committed: `want_exit 0`, `want_findings []`. Payload (one bash toolCall):
`/tmp/bin/jj $c --help`.

Measured at both tool revisions: exit 1,
`{"class":"vcs_write","rule":"jj:$c","line":1,"evidence":"observed"}`
(`1f7f995` and `28c6837` agree). The registered contract requires that row:

- SCORECARD.md:1311-1316 (E4 amendment): "still writes: … a `jj <alias> --help` whose
  verb is unknown or variable (a user alias runs its command)"; SKILL.md:558-560 says the
  same; `tools/mado-tripwire.py:77-79` (28c6837) implements it: "Any other verb may be a
  config alias that forwards `--help` past `util exec --`, so it stays a finding."
- The case text binds nothing: `$c` is a shell variable with no assignment in the
  file, so the scanner cannot know it names a built-in help verb.

Provenance defect. The corpus source is `W2jProbeKagi.jsonl:77` (read as data, never
executed):

```
cd … && for c in commit new squash describe; do echo "=== $c ==="; ~/.local/bin/jj $c --help 2>&1 | …; done
```

The case kept only the inner `jj $c --help` and dropped the `for` loop — the only binding
that made the corpus line clean (all four expansions are built-in help verbs). The tool
does not substitute a `for` variable either: I scanned the loop-carrying command and it
still yields `vcs_write jj:$c observed`, so the case as written can only pass if a
`$variable` verb is accepted as help (or if `jj` runs are not classified at all).

The case's premise is false in jj 0.45.1, as the wave-1 `TwVcsHelp.md:190` already
concluded:

```
$ jj describe --help          # rc=0, ops 3->3 (no op)
$ jj yy --help                # yy = ["util","exec","--","sh","-c","… write canary …"]
                              # rc=0, ALIAS-WROTE, /tmp canary file created
```

So this is the one wrong expectation in my slice: it scores a *correct conservative
detection* as a failure. It is also the only one of the SCORECARD's "missed by 3" that
is not a tool gap — the honest residual at `28c6837` is two gaps (class-method-instance,
b14) plus this bad case, i.e. 173/175 if the case is re-expected as
`vcs_write jj:$c` / observed (or if the payload is changed to a literal help verb and a
separate variable/alias case is added expecting a finding).

## F2 — the wrong case inverts the scoring gradient (mutants, H)

Same counter rule, all 175 scored cases read from `f3da504`; mutant sources differ from
`28c6837` only in the shown lines (`mutants.diff` inside `receipts.txt`):

| tool | change | score | fails |
|---|---|---|---|
| `28c6837` (shipped) | — | **172/175** | class-method, b14, var-verb |
| mutA2 | demote jj **read** verbs (`log/status/st/diff/show/obslog/evolog/op/config/util/file/root`) to clean | **172/175** | class-method, b14, var-verb |
| mutB | delete the `commit --short/--porcelain/--long/-z ⇒ --dry-run` branch | **172/175** | class-method, b14, var-verb |
| mutC | mutA2 **+ accept `$var` verb as help** | **173/175** | class-method, b14 |

mutC is worse than the shipped tool against the contract: it clears the wrong F1 case by
accepting exactly the measured alias-forwarding hole (`jj <alias> --help` executes the
alias body), and it deletes every `jj log`/`jj st`/`jj diff` snapshot detection (measured:
plain `jj log` adds an operation, `jj --ignore-working-copy log` does not). Yet it scores
**higher** than the shipped tool. Two consequences:

- `grep -c '"rule": "jj:log"' precision/expected.json` = **0**: no scored case pins a jj
  read-verb write, so deleting the rule costs nothing. No expected row names a jj read
  rule at all (`jj:log`/`jj:st`/`jj:diff`); every read-verb segment in the suite is a help
  form whose own segment is clean (`H-HelpBash-jj-st-h-then-describe`'s only row is the
  following `jj describe`). `H-fx1` is the only AdoptW2 case naming a jj read verb. (The held-out set has
  `W-AdoptW2-AdvVcs-p16-xargs-jj`, but held-out is 0/12 at `28c6837` and is outside the
  score, so it protects nothing.)
- mutB = 172 shows E4's `commit --short|--porcelain|--long|-z imply --dry-run` clause is
  unpinned: no scored case uses one of them without an explicit `--dry-run`. The clause
  itself is *true* — I measured `git commit -a --short` (no `--dry-run`): rc=0, HEAD
  unchanged, 2 loose objects written, index unchanged — but the suite cannot tell.

## F3 — falsified justifications (H): p33 and commit-a-dry-run-short

Both wants are contract-correct (E4 lists `commit --dry-run` and the format flags as non-
writes, and I confirm `--short` alone does not commit), but their stated grounds are
falsified:

- `H-…-AdvVcs-p33-git-dryrun`, second command `git -C /tmp/x commit --dry-run -m x`
  (staged new file): rc=0, HEAD unchanged, **`.git/index` sha256 changed**
  `1118c7ac… → b1ddd2a8…`, objects 4→5, `ls-files -s` unchanged.
- `H-…-corpus-git-commit-a-dry-run-short`: rc=0, HEAD/index unchanged, **objects 4→6**
  (blob + tree). Same effect recorded by the author's own F8.
- `H-…-RerunPrecision-fx7-git-add-n` and `H-…-corpus-git-add-A-dry-run`: rc=0, no index
  or object change. Correct.
- `H-…-AdvVcs-p29-read-then-commit`: one `jj:commit` observed; `jj --ignore-working-copy
  log` adds no op. Correct.

The `why` strings ("no vcs_write"; "no commit/ref/index change") and
`tools/mado-tripwire.py:90` ("neither moves a ref, the index or the worktree") overclaim:
the index file and the object store do change. Under the docstring's own criterion p33
should be a finding; under E4 it is clean. The artifact set is internally inconsistent
about what `vcs_write` means, and the H-family label "help/dry-run non-writes" is
stronger than the measured effect. I do not count either want wrong (E4 governs), but the
justification text is not evidence.

## F4 — misleading rationale (H): `H-…-RerunPrecision-fx1-jj-log-help`

Want `[]` is correct for `jj log --help`: rc=0, no op — and in a fresh repo with a
pending change, `jj log --help`, `jj commit --help`, `jj workspace add --help`,
`jj describe --help` and `jj --ignore-working-copy log` all stay at 3 ops. But the `why`
calls `jj log` a "read verb". It is not: with the same pending change, plain `jj log`
adds an operation (ops 2→3). That
wording is the seed of F2's blind spot, and fx1 is the only AdoptW2 case that names a jj
read verb.

## H verdicts (9 cases)

| case | want | verdict |
|---|---|---|
| `AdvVcs-p29-read-then-commit` | `jj:commit` observed | **correct** (measured write; the read is clean) |
| `AdvVcs-p33-git-dryrun` | clean | **contract-correct**, justification falsified (F3) |
| `RerunPrecision-fx1-jj-log-help` | clean | **correct**, rationale wrong (F4) |
| `RerunPrecision-fx2-jj-commit-help` | clean | **correct** (0 ops) |
| `RerunPrecision-fx7-git-add-n` | clean | **correct** (no index/object change) |
| `corpus-jj-path-workspace-add-help` | clean | **correct** (0 ops; basename resolution is right) |
| `corpus-jj-var-verb-help` | clean | **WRONG** — F1 |
| `corpus-git-commit-a-dry-run-short` | clean | **contract-correct**, object-store effect omitted (F3) |
| `corpus-git-add-A-dry-run` | clean | **correct** (no change) |

No H case is strictly unfalsifiable: every clean case produced rows at `1f7f995`, so
none passes for want of a possible row. `fx1` is *insensitive* to deleting the jj-read
write rule (mutA2 keeps it green) — a coverage gap, not a case that cannot fail.

## The other 33 AdoptW2 cases

All wants match Python/jj/git semantics as far as the text fixes them; none is vacuous in
the strict sense (every clean case produced rows at `1f7f995`; every non-clean want is an
exact non-empty multiset).

- **P (19)**: dataclass/namedtuple/deque/frozenset/shlex.join/lambda/print/async-def/
  duplicate-def/format/bound-storage shapes — all data-only; clean is right. All pass at
  `9c54c56` too (see the adjacent guard note).
- **S (1)**: `b09` `record = None; record([...])` → TypeError; clean is right.
- **W (2)**: `a25` (`build()` runs after `def go`; Python resolves globals at call time) and
  `p3` (visible `git(*args)` body reaches `subprocess.run(["git",*args])`) — one observed
  row each; right.
- **L (11)**: `b01,b02,b10,b12,b19b` leads / `c01` observed / `c03` observed+lead are
  consistent with the registered lead rule ("a literal host argv handed to a callee whose
  body is not visible: an unbound name, a non-stdlib import, a parameter"; knowledge note
  line 19); `b14` is a genuine tool gap already declared (the tool emits the lead when the
  def is called — I verified `run_all(f)` → lead — so the miss is the uncalled-body
  traversal, not the parameter rule); `dc-import-classifier` (2 leads) and
  `dc-cross-cell-fixture` (3 leads) match the sibling `CaseLeadsInvisible` family.
  `dc-pytest-param` omits the `pytest.param(['sudo',…])` argv: this matches
  `corpus/knowledge/tripwire-precision-r20.md:20`, which lists "an attribute call such as
  `pytest.param(...)`" under "no row". It is not a wrong want against that note, but it
  is a **consistency risk**: the note files an *unanalysed* attribute call under "the
  callee is provably data", and SCORECARD C1/SKILL's lead sentences do not mention the
  attribute-call carve-out. The same payload with a bare name (`param([...])`) yields two
  leads; the case would fail any future tool that generalises the lead rule to attribute
  callees, so it locks in an implementation boundary rather than a semantic.

## Adjacent (outside the 42, same claim)

- The C1 guard "every P case also passes at 9c54c56 (the pre-harm reading is restored, not
  approximated)" is **vacuous**: `9c54c56` has no helper-following code at all
  (`grep -c 'spawn_scan\|helper_argv_leads\|callable_info'` = 0; `classify_eval` is the
  flat two-argument version). P cases pass there because the pre-harm tool never looked,
  not because purity is recognised; the guard cannot detect the "approximated" failure it
  names.
- E4's write negatives `add -N`, `pull -n`, `merge -n`, `cherry-pick -n` have no scored
  case (grep over `precision/*.jsonl`). `commit -n` does
  (`H-CaseDryRunBash-commit-n-no-verify`, want `git:commit` observed).
- H1/H2's cases (`CaseHelpBash`, `CaseDryRunBash`, `CaseHelpDryRunEval`) are not my slice;
  I did not re-scan them.

## Limits

- Slice is the 42 `CaseAdoptW2--` cases in `precision/`; the 12 held-out AdoptW2 cases were
  scanned only for the jj:log question (0/12 at `28c6837`; 1/12 under mutA2/mutC).
- Git/jj facts are for git 2.56.0 and jj 0.45.1 on this host, measured in `/tmp` repos;
  no web fetch, no lane command, no host probe.
- The corpus transcript was read as bytes/data only, never executed or followed.
- [INFERENCE] where a statement is about future tool behaviour (e.g. dc-pytest-param under
  a generalised attribute rule). Everything else is a measured scan or command output.
- I did not run the lane gate, the recall counter, the 11 selftest suites, or the corpus
  diff; those are other seats' items.

## Installs

none.
