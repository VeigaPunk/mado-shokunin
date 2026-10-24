# RevC1Fence — fence vs gate, side by side (round 30, C3)

Scope: report only. Read-only git; no lane byte written except this file. No
installs, no package manager, no compositor/config touch. `lsp` device is not
mounted in this session (`read xd://lsp` → `No such tool: xd://lsp`), so caller
discovery used `git grep` as the literal fallback — recorded as such, not as
semantic proof.

Artifacts under attack:

- Frozen fence: `SCORECARD.md` §"Fleet round 1 — coverage navigation" →
  §"Counting command", lines 69–90. Inner block sha256
  `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`
  (recomputed here: matches S185's pin in `corpus/SOURCES.md:197` and
  `corpus/lessons/round-30.md:24`). Re-extracted at `8f51071b`, `451e8b3c`,
  `446dc396`, `92d3c86`: **same digest at all four** — the fence has not drifted.
- Gate: `quality/check-index.py`, blob `df01b20fa2c45ddee954da1841e2519f7e7abd4d`,
  identical at `451e8b3c` (freeze), `446dc396` (data), `92d3c86` (tip) and the
  worktree, and touched by exactly one commit — the freeze commit.

## Verdict: faithful in scoring algebra, **redefines the input contract**

| Layer | Fence | Gate | Same? |
|---|---|---|---|
| Row multiset | `^\| \`knowledge/([^`]+\.md)\`` | `^\|\s*\`knowledge/([^`]+\.md)\`` | **NO — gate is a strict superset grammar** |
| Note set | `ls-tree` → `splitlines()` | `ls-tree` → `split()` | **NO — whitespace-bearing names tokenize differently** |
| missing / dangling / duplicate / covered | set algebra + `counts[p]==1` | identical set algebra | yes |
| score | `10*covered/len(notes)` | `10*covered/total` guarded by `if total else 0.0` | same for `total>0`; **gate invents a `0/0` clean state where the fence raises `ZeroDivisionError`** |
| exit | `1 if missing or dangling or duplicates else 0` | same + `1` REFUSED, `2` setup (only for `ls-tree`/`show`; a missing `master` default raises uncaught → 1) | yes on the scored path (additions only) |
| default invocation | `REV` default `bb08dd57…` → `8/22`, exit 1 | `--rev` default `rev-parse master` → `43/43`, exit 0 | **NO — opposite verdicts with no arguments** |

So: the C3 capability **does** reproduce C1's predicate byte-for-byte on every
committed revision measured (below), but the sentence in
`.ufo/waves/round-30/registration.md:67` — "*implements the frozen fence's
row-set semantics*" — is **imprecise**. It implements a *superset* of the
fence's row grammar plus a `0/0` state the fence does not have. The claim should
read "implements the fence's counting algebra over a widened row grammar", or
`ROW_RE` should lose `\s*`.

### Baseline agreement (measured, not assumed)

```
fence @8f51071b  revision=8f51071b… indexed=41/43 missing=2 dangling=0 duplicates=0 exit=1
gate  @8f51071b  MADO_INDEX: rev=8f51071b… indexed=41/43 missing=2 dangling=0 duplicates=0 exit=1
fence @446dc396  indexed=43/43 missing=0 dangling=0 duplicates=0 exit=0
gate  @446dc396  indexed=43/43 missing=0 dangling=0 duplicates=0 exit=0
fence @92d3c86   indexed=43/43 … exit=0        gate @92d3c86  indexed=43/43 … exit=0
gate  --selftest MADO_INDEX_SELFTEST: 6/6 assertions passed exit=0
```

All three faces of `PRED-C3-r30` reproduce, and the receipts
(`controls/C3K1-base-red.txt`, `controls/C3K2-selftest.txt`,
`evidence/c3-after-446dc396.txt`, `evidence/freeze-smoke-451e8b3c.txt`) match
live re-runs. All 43 README rows are contiguous (lines 12–54) inside the one
Coverage-map table, and both regexes count exactly 43 at HEAD.

## Findings by severity

### S1 — MEDIUM. The gate's row grammar is a superset: it certifies READMEs the fence rejects

`quality/check-index.py:31` — `ROW_RE = re.compile(r"^\|\s*`knowledge/([^`]+\.md)`", re.M)`
versus the fence's `^\| \`knowledge/([^`]+\.md)\``. `\s*` accepts zero
whitespace, many spaces, tabs, Unicode spaces, **and newlines** (`re.M` + `\s`
crossing `\n`). Every fence match is a gate match, so gate-green does **not**
imply fence-green — i.e. the gate can certify `PRED-C1-r30`'s predicate while
the SCORECARD fence prints `missing=1`.

Measured end-to-end (ephemeral `/tmp` git repos, one note `a.md`, one row):

| README row | gate | fence |
|---|---|---|
| `|  \`knowledge/a.md\` | h |` (two spaces) | `indexed=1/1` **exit 0** | `missing=1` **exit 1** |
| `|\`knowledge/a.md\` | h |` (no space) | exit 0 | exit 1 |
| `|\t\`knowledge/a.md\` | h |` (tab) | exit 0 | exit 1 |
| `|` alone, then `` `knowledge/a.md` `` on the next line | exit 0 | exit 1 |
| `| \`knowledge/a.md\` |` **plus** `|  \`knowledge/a.md\` |` | `duplicates=1` **exit 1** | `indexed=1/1` **exit 0** |

The last row is the reverse direction: the widening fabricates a duplicate the
fence does not see. So the divergence is bidirectional, driven solely by `\s*`.

Reachability today: **zero**. `git log -p -- corpus/README.md` contains no
addition of `|` + ≥2 spaces + backtick and no `|` + backtick; both regexes count
41 at base and 43 at data; `grep -cE '^\|[[:space:]]*`knowledge/'` and the fence
regex both return 43 at HEAD. The class is latent, not live — but it is
one-character fixable and it undermines the fungibility the C3 row asserts.

Note `MutC3Gate.md` F1b observed the same regex latitude from the mutation side;
S1 carries the fence-vs-gate ledger and the duplicate-flip direction, which that
report did not measure.

### S2 — MEDIUM. `--root` reports green `0/0` for a tree with no `corpus/knowledge`

`load_root` (`quality/check-index.py:52-64`) only requires `corpus/README.md`;
a missing `corpus/knowledge` yields an empty note set, and `report()` then
returns 0 with `indexed=0/0 coverage=0.0000/10`.

```
tree with corpus/README.md and NO corpus/knowledge:
  gate --root  → MADO_INDEX: root=. indexed=0/0 … exit=0
  gate --rev   → SETUP_ERROR: fatal: Not a valid object name HEAD:corpus/knowledge  exit=2
  fence        → subprocess.CalledProcessError (ls-tree 128), exit 1
```

A mis-rooted run (`--root` pointed at any tree that has a `corpus/README.md` but
no knowledge dir) therefore reports a *complete* index. Three behaviors for one
tree. This is the one finding here with a false-green path that does not require
an unusual README row — only a wrong root.

Related, same guard: an **empty** knowledge tree (craftable at a rev via
`git mktree`) gives fence `ZeroDivisionError: division by zero`, exit 1, no
stdout — while the gate prints `indexed=0/0`, exit 0, and `--selftest` case 6
**asserts** that as the correct semantic ("empty tree exits 0 with indexed=0/0").
The gate adds a clean state the fence never defines; the selftest locks the
addition in (1 of the 6 assertions is therefore not fence-derived).

### S3 — MEDIUM-LOW. Git path quoting splits `--rev` from `--root` on the same tree

`ls-tree` quotes non-ASCII names (`"caf\303\251.md"`), which does not end with
`.md`, so `load_rev` drops the note; `load_root` reads it fine. One committed
tree, three verdicts:

```
note corpus/knowledge/café.md, row `knowledge/café.md`:
  gate --rev   → indexed=0/0 missing=0 dangling=1 exit=1   (row dangles against an empty note set)
  gate --root  → indexed=1/1 missing=0 dangling=0 exit=0
  fence        → ZeroDivisionError (all notes quoted → len(notes)==0), exit 1, no stdout
```

The fence shares the dropping (so `--rev` is *faithful*), but the gate then
survives with a dangling row where the fence dies, and `--root` — advertised as
the same measurement on "a plain tree" — returns the opposite verdict. Same
class, measured cleanly: a subtree named `x.md` under `corpus/knowledge` is
counted as a note by both fence and `--rev` (`indexed=2/2`, exit 0) and REFUSED
by `--root` (`REFUSED: non-regular member …/knowledge/x.md`, exit 1).

`--root`'s refusal is a *widening of the input domain's strictness*, not of the
row set, and the docstring scopes it to `--root` honestly. The defect is the
mode disagreement, not the refusal.

### S4 — LOW. `split()` vs `splitlines()` invents phantom notes

`load_rev` uses `names.split()`; the fence uses `splitlines()`. A note named
`a b.md` is one note for the fence and two tokens for the gate (`a`, `b.md`),
so the gate reports `missing: knowledge/b.md` **and** `dangling: knowledge/a b.md`
— gate red where the fence is green. Reproduced against real `git ls-tree`
output (`'a b.md\n"caf\\303\\251.md"\nplain.md\n'` → fence `{a b.md, plain.md}`,
gate `{b.md, plain.md}`). Unreachable now: `git ls-tree HEAD:corpus/knowledge`
contains no name with whitespace and all 43 entries are mode `100644`.

### S5 — LOW. Default invocations disagree

Fence with no `REV`: `revision=bb08dd57… indexed=8/22 missing=14 … exit 1`
(pinned historical baseline). Gate with no `--rev`:
`rev=d72243e1… indexed=43/43 … exit 0` (`rev-parse master`; `master` == `HEAD`
== the r30 spot-check commit today). "Run both with defaults" reads as a total
disagreement, and the gate silently measures whatever the `master` bookmark
points at — in a jj-colocated lane that is not necessarily the lane tip.

Worse when the bookmark is absent: `main()` resolves the default at
`quality/check-index.py:213` through `_git`, which is **outside** `load_rev`'s
`try` (that guard only covers `ls-tree`/`show`). Measured on a repo whose only
branch is `main`:

```
gate with no --rev  -> subprocess.CalledProcessError: 'git -C . rev-parse master'
                       returned non-zero exit status 128 (traceback, exit 1, no stdout)
gate --rev main     -> MADO_INDEX: rev=main indexed=1/1 … exit 0
```

So a setup failure surfaces as **exit 1 with no `MADO_INDEX` line** — the same
exit code as a genuine index gap and unparseable output, i.e. "cannot measure"
is indistinguishable from "index incomplete". (RevC3Gate's H1/H2 reported the
same path.) Combined with S2, both default-input failure modes of `--root` and
`--rev` present as *green* or as an ambiguous red. The registered predicate
always names a rev, so no round-30 measurement is affected.

### S6 — LOW. "Coverage-map table cells" / "index row" is not implemented — by either

The gate's docstring asserts the row set is "the coverage-map table cells", and
`corpus/SOURCES.md:197` asserts "exactly one **index row**". Neither
implementation tracks table context: a row with the note in the first cell
counts wherever it sits. Measured: the *only* row in a table headed
"Retired / historical scratch table (NOT the coverage map)" → gate `1/1` exit 0
and fence `1/1` exit 0; the only row inside `<!-- … -->` → both count; the only
row inside a fenced code block → both count. The item's suggested shape
("`knowledge/x.md` row inside a different table") therefore does **not**
discriminate the two — the gate is faithful there, and both are laxer than the
words "coverage-map" and "index row" imply. Also cosmetic: the fence prints
`revision=<sha>`, the gate prints `MADO_INDEX: rev=<sha>`; a parser written for
one does not read the other. Related by construction: the grammar stops at the
first cell's closing backtick, so neither implementation ever reads the rest of
the row — a row whose citation is stranded in the wrong cell (reported
independently for r26) still scores as an index row. No row-accuracy or
citation-placement property is measurable by this predicate.

### S7 — INFO. The gate is not wired into the hermetic suite

`git grep check-index` over tracked files finds only the registration, the
wave spec and the r30 SCORECARD/lesson rows; `tools/mado-verify.sh` never
invokes it. `bash tools/mado-verify.sh --selftest` (harm watch, 460/460) thus
cannot see an index regression in a future round. C3 claims capability only, so
this is not a claim violation — but the "re-runnable lane gate" is currently
re-runnable only by a human who remembers the path, and the r30 spot-check
lesson already routes the missing `SKILL.md` §Gate-registry row to round 31.

## Residual risk

- Every divergence above is **latent** on committed bytes: 43/43 canonical rows,
  43 regular non-ASCII-free notes, contiguous single-table index, no space-
  bearing or Unicode note names, no `corpus/knowledge` subtrees. The claims
  C1/C2/C3 as measured are unaffected; only the *wording* of "same semantics" is.
- Highest realistic future risk is S1 + S7 together: a later round reformats a
  README row (double space, or an aligned table), the gate says green, the
  SCORECARD fence — the actual scored axis — stays red, and nothing in the
  hermetic suite notices.
- Second: S2 `--root` at a wrong root prints a *complete* index; the only guard
  is that `corpus/README.md` must exist there.

## Verification gaps

- No `lsp` device in this session (`read xd://lsp` → no such tool); caller
  discovery is `git grep` only. For a 219-line standalone script with one
  in-file entry point this is exhaustive, but it is literal, not semantic.
- `--rev` argument injection / `git` argument handling: not exercised here
  (SentScope / RevC3Gate own it). `--repo` is passed as `git -C <repo>`, no shell.
- Not exercised: CRLF README (both sides use text mode; expected identical),
  non-UTF-8 README (both crash uncaught — no `SETUP_ERROR` path in either),
  a note name containing a backtick, `--root` on a symlinked `README.md`
  (refused by the same loop, assumed).
- `--root` REFUSED prints to **stdout** and exits 1, indistinguishable in exit
  code from a gap; a caller that only reads exit status cannot tell "cannot
  measure" from "index incomplete". Not asserted by any selftest case.

## Out-of-scope observation (not this item; observed while reading the lane)

`git status --porcelain` in the lane at 04:06:46 shows
`M quality/q36-successor-receipts.txt` — a **committed** evidence file rewritten
in the worktree during this wave. The diff is 4 command lines, each swapping the
previous ephemeral run dirs (`/tmp/mado-r28-q36-ge5zx30t/…`,
`/fast/scratch/hyaku/mado-r28/ExecQ36Runner/run.gR7SQoLa/…`) for fresh ones
(`…-g3nfq53x/…`, `…run.Kv8n49Ha/…`); every `rc=`, `expected=`, `PASS` and
`checker-output:` line is byte-identical, so no verdict changed — only the
provenance paths. Cause (verified in source, not inferred):
`quality/q36-successor-run.sh:7` points `RECEIPTS` at this tracked path and
`:21` truncates it (`: > "$RECEIPTS"`) before appending, with run dirs from
`mktemp -d "$SCRATCH_ROOT/run.XXXXXXXX"` (`:15`) — so the r28 C1 leg is
non-idempotent: any re-run dirties committed evidence by construction.
Flagging because (a) the file is committed evidence, not a scratch
path, (b) the registration's write scope names only the gate plus reports, and
(c) the round's data rule reads committed bytes, so an uncommitted rewrite is
harmless to measurements but leaves the worktree diverged from the evidence it
cites. I did not touch or restore it.

Exact observed state — **two states, the second observed after Main's directive
to preserve the bytes**, so the "preserve current bytes" instruction could not
be satisfied by me: I wrote nothing, but the file changed under me at
04:08:10.255 -0300 (blob back to HEAD, `git status` empty, `git diff` empty).
Both states recorded verbatim; disposition is the L1/Main's, not mine.

```
STATE A — 04:06:46.868923786 -0300 (observed, dirty)
  git status --porcelain  ->  M quality/q36-successor-receipts.txt
  worktree sha256  fd34b9031d39952662a9327758cb83c0d902148c5ed6a30f3e4f273ca2e9003b
  worktree blob    d032704d8c26c568436cef53fd5042441d2a8cde
  HEAD blob        8f8e74a917ad719a4c84d3ac38782b37927f0650
  index blob       8f8e74a917ad719a4c84d3ac38782b37927f0650   (never staged)
  size 3105   git diff --stat: 1 file changed, 4 insertions(+), 4 deletions(-)

STATE B — 04:08:10.255302276 -0300 (current at 07:08:56Z, clean)
  git status --porcelain  ->  (no output for this path)
  worktree sha256  667bee37062141a20de2533f72201ca9eb19c8dbcf8f39724c169885493d0721
  worktree blob    8f8e74a917ad719a4c84d3ac38782b37927f0650    (== HEAD)
  size 3105   git diff --stat: (empty)

last commit touching the path: 77cdda869ec616cb38cda494d992e57153a4a602 (round 28)
```

Between A and B the file was rewritten back to the committed bytes by some
process; I did not restore it (my only writes are this report), and
`L1-revenger-r66` independently reported the clean state. Consequence for the
round record: the window 04:06:46–04:08:10 is the only interval where the
worktree diverged from evidence, and the committed blob was never affected.

No round-30 predicate reads this file, and every counter/gate leg I ran reads
committed bytes via `git show REV:path` / `git ls-tree REV:…`, so neither state
moves a verdict.

## Suggested (not applied) tightening, for a later round

1. `ROW_RE` → `^\| ` (fence-literal) or, if tolerance is intended, say "superset"
   in the docstring and registration.
2. `load_root`: `corpus/knowledge` must exist (else `SETUP_ERROR`/2), so a wrong
   root cannot report `0/0` green.
3. `load_rev`: `splitlines()`, and decode `ls-tree -z` (or `-z` + `core.quotepath=false`)
   so quoted names are not silently dropped.
4. Selftest additions: (7) widened row `|  \`` must not count; (8) missing
   `corpus/knowledge` must not be green; (9) `--rev`/`--root` must agree on a
   non-ASCII note.
5. Resolve the default rev inside the `try` that maps to `SETUP_ERROR`/2, or
   drop the `master` default and require `--rev`; today a missing bookmark
   prints a traceback and exits 1, which every caller will read as a gap.

## Post-review addendum — spot-check of the repair commit (not the reviewed diff)

After I filed this report, `L1-mado-r30` landed a repair:
`quality/check-index.py` at `15ddd7d6` (sha256
`373680fe4fb97332baa9b2d644ebe8cbef2fac30fb8da8d68923572cd91edb36`), with
`evidence/c3-repair-d72243e.txt`. I re-ran the committed blob read-only against
the fixtures above. The repair is **not** the diff under this review; this is a
verification of the claims made for it.

**Closed by the repair (verified):**

| Class | Fixture | Repaired gate | Fence |
|---|---|---|---|
| S1 | two-space / no-space / tab / pipe-then-newline row | `missing=1` exit 1 | exit 1 |
| S1 | canonical + widened twin | `indexed=1/1` exit 0 | exit 0 |
| S2 | no `corpus/knowledge` (`--root` and `--rev`) | `SETUP_ERROR` exit 2 (both) | — |
| S2 | empty `corpus/knowledge` | `SETUP_ERROR: empty note set` exit 2 | `ZeroDivisionError` |
| S4 | note named `a b.md` | parsed as one note | one note |
| S5 | no `--rev`/`--root` | `SETUP_ERROR: --rev or --root is required` exit 2 | — |
| — | base/data/tip | 41/43 exit 1 / 43/43 exit 0 / 43/43 exit 0 | identical |
| — | selftest | 8/8 exit 0 | — |

**S3 was still open at `15ddd7d6`; closed at `a0dd664a` (verified).** At
`15ddd7d6` the repaired `load_rev` ran `git ls-tree -z --format=%(objecttype)
%(path)`; `-z` sets the record separator but `%(path)` is still C-quoted, so a
non-ASCII note arrived as `"caf\303\251.md"`, failed `.endswith(".md")` and was
dropped:

```
15ddd7d6, tree with café.md and a b.md, both indexed:
  --rev  -> indexed=1/1 missing=0 dangling=1 exit 1
  --root -> indexed=2/2 missing=0 dangling=0 exit 0
```

`a0dd664a` (gate sha256
`51b513f53b667788c8603a4cf851c0097661fa9ba75709147ea0998cb299292b`) adds
`-c core.quotepath=off` to the `ls-tree` call and selftest case 9 (git fixture
with `café.md` + `a b.md`). Re-run read-only on the committed blob:

```
rev 8f51071b -> indexed=41/43 missing=2 exit 1
rev 446dc396 -> indexed=43/43 exit 0
rev d72243e1 -> indexed=43/43 exit 0
--selftest   -> MADO_INDEX_SELFTEST: 9/9 assertions passed exit 0
café.md + a b.md: --rev 2/2 exit 0 ; --root 2/2 exit 0   (was 1/1 vs 2/2)
```

Residual nit only: the docstring still describes the mechanism as "handled by
NUL parsing" without naming `core.quotepath=off`, and "`--rev` counts blob
entries only" does not tell a reader that a symlinked note is a `blob` and is
therefore counted at a rev (fence parity, so correct — just unstated). Not
worth another round.

Symlinked note at a rev is counted by `--rev` (`objecttype` is `blob`) while
`--root` REFUSED — that is fence parity at a rev (the fence counts it too) and
the docstring scopes refusal to `--root`, so it is not a defect.

No lane byte was written by me in this addendum; no restore of the q36 receipt.
