# Falsify28 — C1 counter isolation/scratch behavior

## Deliverables
- Seat-local fixture battery (scratch git repo + predicate-satisfying naive counter) demonstrating a non-isolated C1-style counter that still satisfies the frozen green/red receipts; receipt copies under `.ufo/waves/round-52/w1/Falsify28/receipts/`.
- Source-level analysis of the isolation machinery in the base counter/checker and the advisory-only `REFUSED_ROOTS` scratch guard in the r51 template.
- No tracked lane edits; no claim or predicate edits; no installs.

## Evidence and attack

Attacked item/predicate: frozen C1 operability predicate (`.ufo/waves/round-52/registration.md:7`):
"a new counter for the tracked instrument ledger runs at a requested pinned revision, and validates population row uniqueness, resolvable evidence pointer, non-self pointer, and a description containing instrument-specific functional context. It must pass on the existing production ledger at the base revision and fail on `controls/c1-do-nothing.md` specifically for self-pointer/context defects."

Attacked clause, specifically: **"runs at a requested pinned revision" + "resolvable evidence pointer."** The predicate never requires that the counter read ledger bytes or resolve evidence targets from the *pinned revision's tree*. It only requires that a `--rev`-shaped argument exist and that the two named receipts (production pass at base, control fail) hold. I demonstrate that a counter implementing all four named checks, and passing both receipts, can still resolve evidence against (a) the repository *working tree* and (b) the *invocation cwd* — so its verdict tracks ambient filesystem state instead of the pinned revision.

Why this matters to the claim: the claim's "Before" text says the r51 counter's weakness is basename-substring evidence. The base instruments actually isolate reads well — `c1-r51-ledger.py` clones at the rev (`make_clone`, `quality/counters/c1-r51-ledger.py:106-131`) and reads content via `git show rev:path` (`show`, `:151-152`; `pointer_resolves` requires the token to be in the `ls-tree` listing, `:196-208`), and `quality/check-tool-ledger.py` resolves population and blobs through `tree()`/`blob()` (`:135-156`). So a faithful round-52 builder will probably inherit isolation — but the frozen predicate does not *require* it, and the specified acceptance evidence (green production receipt at base + red control receipt) is **incapable of distinguishing an isolated counter from a non-isolated one**, because at the base revision the working tree equals the pinned tree. The accountability property is therefore unverified exactly in the situations the pinned revision exists for: dirty trees, older revs checked after later commits, and invocation from scratch directories.

## Reproducible setup and results

Setup (all under scratch `/fast/scratch/hyaku/mado-r52/Falsify28/`, removed after receipt copy; disk guard checked, 599G free):
1. `iso-fixture/repo`: git repo, one commit (`e5b3e82b874d5472892a8856cd0df14013924432`, "base") containing `tools/demo-tool.sh` (evidence naming `demo-tool.sh`) and `quality/tool-ledger.md` with one good row: pointer `` `tools/demo-tool.sh` ``, description `` `demo-tool.sh` verifies demo dispatch routing end to end ``.
2. `iso-fixture/naive_counter.py` (copied to `receipts/naive_counter.py`): implements the four frozen checks — population row uniqueness, resolvable evidence pointer, non-self pointer, instrument-specific context — with population read from the pinned rev (`git ls-tree -r --name-only <rev>`, isolated, mirroring the base counter) but evidence resolution via filesystem `os.path.isfile(os.path.join(repo, token))` with a cwd-relative fallback `os.path.isfile(token)`. Ledger text is likewise read from the working tree. This is the natural implementation a builder writes when the predicate says "resolvable evidence pointer" without an isolation requirement.
3. `iso-fixture/ctrlrepo`: scratch repo staging the frozen control bytes (`.ufo/waves/round-52/controls/c1-do-nothing.md`) as `quality/tool-ledger.md` plus `tools/mado-verify.sh`.

Commands and actual results (verbatim receipts in `receipts/run1-green.txt` … `run5-restored.txt`):
- `python3 naive_counter.py --repo iso-fixture/repo --rev e5b3e82…` → `NAIVE_C1: population=1 ledger_rows=1 dup=0 bad_pointer=0 self_pointer=0 context=0 verdict=TARGET_MET rev=e5b3e82…`, exit=0. Green receipt satisfied.
- `python3 naive_counter.py --repo iso-fixture/ctrlrepo --rev fae91d9b…` → `detail: bad_pointer path=tools/mado-verify.sh`, `detail: context path=tools/mado-verify.sh`, `detail: dup path=tools/mado-verify.sh`, `verdict=TARGET_MISSED`, exit=1. Red receipt satisfied.
- Isolation break 1: `mv repo/tools/demo-tool.sh repo/tools/demo-tool.sh.hold` (no commit; `git status` shows `D tools/demo-tool.sh`), same `--rev e5b3e82…`; ground truth `git cat-file -e e5b3e82…:tools/demo-tool.sh` succeeds (pinned blob intact). Naive counter → `bad_pointer=1 verdict=TARGET_MISSED`, exit=1. **Verdict flipped at an unchanged pinned revision purely because of working-tree state.**
- Isolation break 2: working tree still missing the evidence; a decoy `tools/demo-tool.sh` exists only in a scratch cwd (`iso-fixture/decoy/`). Running `cd iso-fixture/decoy && python3 ../naive_counter.py --repo ../repo --rev e5b3e82…` → `verdict=TARGET_MET`, exit=0. **Verdict flipped back by invocation cwd — scratch contamination of evidence resolution.**
- Restore `tools/demo-tool.sh` → `verdict=TARGET_MET` again (run5), confirming the flips are state-dependent, not sticky.

Reproduced: **yes** — both failure modes reproduced with the exact frozen check set green/red receipts satisfied.

Secondary source findings (not separately executed):
- Advisory-only scratch guard: `REFUSED_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")` (`quality/counters/c1-r51-ledger.py:68`) is used solely to print a hint after a selftest failure (`:405-407`); `resolve_work` (`:331-349`) never refuses those roots, so the r51 counter will clone and run checkers under `/tmp` whenever `TMPDIR` says so — contrary to this round's "never /tmp for evidence" rule. A round-52 counter inheriting this template inherits the same scratch-policy hole.
- Control-grammar observation (corroborating, scoped): the frozen control is a 4-column table (`Tool | Reads | Writes | Owner`); under the production 3-column row grammar (`parse_rows` treats cells[1] as description and cells[2:] as pointer), the control's self-referencing token `quality/tool-ledger.md` lands in the description column, so a pointer-cell-only self-pointer check fires `bad_pointer`/`context`/`dup` but not a `self_pointer` class (see run2). If the new counter must fail the control "specifically for self-pointer/context defects" (`registration.md:7`), its self-pointer detector must scan beyond the pointer column; this is a control-shape risk adjacent to, but distinct from, this seat's isolation item.

## Axes, proposed bounded move, risks, verification

Affected axis: operability only. No coverage harm; no axis admits harm from this finding.

Proposed bounded move (recommendation, not an edit): the C1 selftest should add one receipt that pins the isolation property — e.g., stage the production ledger in a fixture repo, run the counter at rev R with the evidence file deleted from the working tree (and again from a cwd containing a decoy), and require the verdict to be unchanged versus the clean-tree run. That single control closes the demonstrated gap and is cheap because it reuses the existing fixture harness. Keep the existing green/red receipts as-is.

Risks/contradictions: this attacks the sufficiency of the frozen acceptance evidence, not any round-52 counter's actual code — no round-52 counter existed in the tree at investigation time (`quality/counters/` contains no r52 ledger counter; `git status` shows only the untracked `.ufo/` wave). The naive counter is a deliberate stand-in for the failure class; it is not evidence that the builder's counter is non-isolated. The base instruments' isolation is good, which cuts both ways: likely inherited, but unverifiable from the named receipts.

Verification: this report exercised only seat-local scratch fixtures (git init/commit/mv, python3 counter runs, git cat-file/ls-tree ground truth) and read-only source inspection of committed files at base `85d57a818c3707397e21c840b6498b105ba798aa`. No package queries, live reads, process/compositor probes, input capture, screenshots, producer execution, host mutation, or tracked/source-tree writes. No installs were needed (none performed). Scratch `/fast/scratch/hyaku/mado-r52/Falsify28/` was removed after receipt copies were written to the seat directory.

## Deliverables
- `.ufo/waves/round-52/w1/Falsify28.md`
- `.ufo/waves/round-52/w1/Falsify28/receipts/run1-green.txt`
- `.ufo/waves/round-52/w1/Falsify28/receipts/run2-control.txt`
- `.ufo/waves/round-52/w1/Falsify28/receipts/run3-wt-tamper.txt`
- `.ufo/waves/round-52/w1/Falsify28/receipts/run4-cwd-decoy.txt`
- `.ufo/waves/round-52/w1/Falsify28/receipts/run5-restored.txt`
- `.ufo/waves/round-52/w1/Falsify28/receipts/fixture-base-rev.txt`
- `.ufo/waves/round-52/w1/Falsify28/receipts/naive_counter.py`

Report: `.ufo/waves/round-52/w1/Falsify28.md`
