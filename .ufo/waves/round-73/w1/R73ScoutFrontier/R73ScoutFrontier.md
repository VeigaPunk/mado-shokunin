# R73ScoutFrontier — round-73 frontier-step reconnaissance

seat: R73ScoutFrontier (leaf; read-only, no dispatch)
date: 2026-11-04 (America/Sao_Paulo)
repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`
base `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce` · freeze `87e4c61ac90e9ac587c9f65ac7844ded268d9046` ·
instruments `1459cca11fb5d3956a6e9a128217852dd0c28cb9` (= HEAD at read time).
Ancestry verified read-only: `merge-base --is-ancestor` passes base→freeze and freeze→instruments.
Nothing was written outside this directory; no git/jj mutation.

## 1. Frozen census

Command run verbatim:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

- **Exit code: 0.**
- stdout is 40 lines: **39 findings + 1 final `mado<TAB>ok<TAB>…/corpus/SOURCES.md` line**.
  Finding codes: **38 × W04** (same URL across scopes) and **1 × W01** (tier-C mined with a
  non-`—` used-by: `S277` → `corpus/knowledge/request-socket-live-bound-r8.md,
  corpus/knowledge/request-limits-upstream-r31.md`). **No E codes**, so no malformed row,
  duplicate id, duplicate URL+scope, enum, date or used-by-path defect.
- `validate` prints findings only; it does not print a row count. The registry count comes from
  the `census` mode of the same script at the same root:

```
mado  rows 383
mado  tier.A 369   tier.B 7   tier.C 7
mado  status.mined 361   status.queued 10   status.rejected 12
FLEET rows 383  tier.invalid 0  status.invalid 0  missing 0
(mode exit 0)
```

**Row count: 383**, matching the stated round-start 383; `missing 0`. Independent check:
`grep -c '^| *S[0-9]' corpus/SOURCES.md` → 383.

W04 is a warning class only (script header: "W-codes … never change status"), so the 38 existing
same-URL findings do not threaten exit 0; §4 explains why the three planned appends add to that
set rather than failing E04.

## 2. `corpus/README.md` `## Frontier` — round-72 items and round-73 movement

The Frontier section starts at line 131. **Round 72 contributes exactly one bullet** (line 133,
`grep -c '^- Round 72'` = 1). Its two landed items and three open items, quoted:

- landed: "the kill credit now requires the run's own failure detail — the last parsed `p/n`
  summary must report a shortfall and the run's own `SELFTEST FAIL` lines must number exactly
  that shortfall — so a bare or replayed summary line no longer earns a kill (eight real `bash`
  fixture modes: 8/8 against the held 6/8 …)";
- landed: "the contract verdict now reads the subject's last parsed summary instead of its exit
  status, so a failing summary at exit 0 is red and a green summary at exit 2 is green";
- open: **"a summary replayed with matching detail is not authenticated"**;
- open: **"the eight cases are a finite grammar sample"**;
- open: **"the r71 guard-census widening (plan item 2) is deferred to a later round"**.

| round-72 open item | round-73 claim | movement | status after round 73 |
|---|---|---|---|
| a summary replayed with matching detail is not authenticated | neither C1 nor C2 | none — C1 scores the committed rule's decision functions against four mutations; `valid-then-garbled` and `zero-denominator` test parsing, not provenance. C1's own target surface repeats the gap | **stays open, untouched** |
| the eight cases are a finite grammar sample | C1 | **moved.** The held eight cases are carried byte-identically (receipt: `cases=8 sha256=640fb44f… carried=yes`) and scored beside a ten-case set that adds `zero-denominator` and `valid-then-garbled`; the ten-case set separates all four named mutations (`killed=4/4`) where the held set separates two (`base_killed=2/4`), pristine 10/10 | **widened, not closed** — still a finite sample by C1's own declared limit ("a mutation that changes behaviour only outside these ten cases is not counted") |
| the r71 guard-census widening (plan item 2) is deferred to a later round | C2 | **moved and discharged.** Round 73 is the later round: `global`-declared guard and mutated-`os.environ` transport are counted, 28 controls at 28/28 with the held classifier at 25/28 missing exactly the three named cases; population 20, readers 13, guarded 13, unguarded 0 | **closed as a deferral**; bounded residual stays open by declared limits (one `global` declaration, line-order dominance, one `os.environ` store + two copy spellings, no cross-module producer, no two-hop alias) |

The two landed round-72 rules themselves are not re-decided this round: the no-harm clause keeps
the frozen round-72 harness and the round-71/70 classifiers byte-identical, and the C1 receipt
confirms the candidate harness sha `b6108c86…` with pristine 10/10 before mutation.

No other Frontier bullet names a round-72 item; the remaining bullets are older rounds and are
not moved by C1/C2.

## 3. `considerthese/` — inventory and the one still-unimplemented proposal

Files present (9): `2026-10-19.md`, `2026-10-20.md`, `2026-10-21.md`, `2026-10-22.md`,
`2026-10-23.md`, `2026-10-24.md`, `2026-10-25.md`, `2026-10-26.md`, `2026-10-28.md`
(2026-10-27 absent — the 2026-10-28 file records that run failing without writing).

**Proposal selected (one): `considerthese/2026-10-28.md` proposal 4** (which restates the
still-unbuilt half of `2026-10-26.md` proposal 2). Quoted:

> **Keep a live-tool table.** There are now 8 live-state tools. One row each (question answered,
> last live run, verdict, who ran it) would show which ones João can run himself today. This is
> the half of the 2026-10-26 proposal 2 the lane has not built.

Verified still unimplemented at the instruments revision (not merely relayed):

- `quality/tool-ledger.md` is the round-51 inventory/accountability ledger. Its header fixes a
  **three-cell row grammar** (`| path | description | pointer |`) and its table has no live-run,
  verdict-freshness or operator column; `grep -i 'last.live\|live run\|last run'` over the ledger
  and its checker returns nothing.
- `quality/check-tool-ledger.py` docstring and code enforce it: findings include
  "a malformed row (not exactly three cells)" and the parser rejects `len(cells) != 3`
  (`quality/check-tool-ledger.py:250-263`). There is no freshness predicate.
- Three independent lane records still name the gap: `SCORECARD.md:2795` ("proposal 2
  last-live-run freshness remains distinct from C1's inventory"), `corpus/lessons/round-51.md:20`
  ("does not record last-live-run or verdict freshness; that part remains open"), and
  `corpus/lessons/round-51-verifier-spotcheck.md:82` ("proposal 2's last-live-run/verdict-freshness
  dimension remains unimplemented").

**Why it fits this round / the lane's next round.** C2 is the operability axis and its no-harm
obligation forces both new round-73 instruments into `quality/tool-ledger.md` with
`check-tool-ledger.py uncovered=0`. The ledger's missing freshness dimension is exactly the
operability debt the round-51 closure named, and it is a finite denominator (8 live-state rows at
tip), the same shape round 73's claims use.

**What opening it would require** (all lane-owned; no host/config/write surface):

1. Decide the shape: a fourth cell on the existing row, or a second table (e.g.
   `| instrument | question | last live run | verdict | who |`). Either way the row grammar in
   `quality/tool-ledger.md`'s header and the parser in `quality/check-tool-ledger.py` must change
   in the same commit — the current checker fails closed on `len(cells) != 3`
   (`check-tool-ledger.py:250-263`) and its selftest fixtures pin the malformed-row case
   (`:672-681`), so both the grammar and its fixtures move together.
2. Populate only from dated receipts already in the tree (r45 monitors AGREE, r46 devices 9/9,
   r47 terminal 190/190 fixtures, r49 keysym 633/633, r50 hostguard), and make "never run live" /
   "fixtures only" an explicit token — never infer a verdict from the tool's name (the r51 wave-2
   attack showed generic descriptions and self-pointers pass the current checker).
3. Define what a "last live run" cell means so it is falsifiable: revision sha + date + verdict
   token + receipt path; a row whose receipt path does not resolve or whose basename is missing
   from it must fail closed, mirroring the existing pointer rule.
4. Sequence against round 73: the two new instruments (C1 counter, C2 counter) must land their
   ledger rows first, or the new grammar must accept both shapes during the transition, otherwise
   `uncovered=0` breaks.
5. Register the changed checker in the same places the current one is registered (`SKILL.md` gate
   registry, `quality/tool-ledger.md` header, the QUALITY criterion that names it), and keep the
   population derivation (files under `tools/` + `quality/*.py` + `quality/counters/*.py`)
   untouched so the denominator stays comparable.

## 4. Duplicate-id and duplicate-URL preconditions for the round's appends

Duplicate id (commands as specified):

```
$ grep -oE '^\| *S[0-9]+' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -V | tail -3
S444
S445
S446
$ grep -c 'S447\|S448\|S449' corpus/SOURCES.md
0        (grep rc 1: no matches)
```

**S447–S449 are unused**; the next three appends take S447, S448, S449 and the registry moves
383 → 386 rows.

Duplicate URL is the sharper precondition, because **all three URLs in the sources plan already
have rows** — the round-73 fetch sets are re-fetches of already-cited files, not new URLs:

| planned row | existing row(s) at this URL | existing scope cell (column 6) | fetched sha256 (3/3 identical) |
|---|---|---|---|
| `Doc/reference/simple_stmts.rst` (`global`) | S440 | "the documented evaluation of a subscription assignment target … (round-70 C2)" | `d43206423b327dcf…` (matches S440's recorded digest) |
| `Doc/library/os.rst` (`os.environ`) | S113 | "which stdlib entry points create processes … tripwire v3 stdlib purity split" | `2d0f2892676e1cf9…` (matches S113's recorded digest) |
| `Doc/library/subprocess.rst` (`env` parameter) | S108, S442 | S108: the `args` command parameter binding; S442: "supersedes S108 for this scope — the `run()` capture_output paragraphs …" | `05cd782c5181481a…` (matches S442/S108's recorded digest) |

Fetched bytes on disk (untracked at HEAD): `.ufo/waves/round-73/fetch/` holds three copies each
of the three files, sizes 41,375 / 208,655 / 61,603 B, with byte-identical digests within each
triple — the "three byte-identical fetches each" clause is satisfied, and each digest equals the
one already recorded in the existing row for that file.

Census rule that follows (`sources-census.sh:645-650`): the E04 key is **URL + scope cell** and is
exempt only when the existing non-rejected row is paired with a new row whose teaches cell
contains `supersedes SNNN`. Therefore:

- A new row at an existing URL with a **different** scope cell → **W04 only** (warning; exit stays
  0). Expect W04 38 → up to 41; the final `ok` line and exit 0 are unaffected.
- A new row that repeats an existing scope cell **verbatim** and omits `supersedes SNNN` →
  **E04**, and `validate` exits 1. That is the failure mode to avoid, not the URL reuse itself.

Suggested distinct scopings (anchors read in the fetched bytes, not guessed):

- `global`: `simple_stmts.rst:971-975` — "The :keyword:`global` statement causes the listed
  identifiers to be interpreted as globals." (distinct from S440's subscription-assignment scope).
- `os.environ`: `os.rst:184-187` (`.. data:: environ` — "A mapping object where keys and values
  are strings that represent the process environment") plus `os.rst:581-584` ("Assignments to
  items in :data:`os.environ` are automatically translated into corresponding calls to
  :func:`putenv`") — distinct from S113's process-creation scope.
- `env=` parameter: `subprocess.rst:88-93` — "If *env* is not ``None``, it must be a mapping that
  defines the environment variables for the new process; these are used instead of the default
  behavior of inheriting the current process' environment … much like :data:`os.environ`", with
  the `Popen` twin at `:648-652` — distinct from S108's `args` scope and S442's capture_output
  scope.

Practical consequence for the C2 entry: the three rows will carry W04 warnings and are
re-openable only as long as the fetch receipts are committed with them; the `fetch/` directory is
currently untracked (`git status` shows `?? .ufo/waves/round-73/fetch/`), so the round must commit
it before the rows' "fetched … three times" anchor cell can point at a tracked receipt.

## 5. Repo state, confidence, remaining unknowns

Observed: HEAD `1459cca1` ("round-73: the mutant-killing outcome set and the extended guard
census"); freeze `87e4c61a`; base `d3f6c9f5`; ancestry base→freeze→instruments holds. Working
tree at read time carried only round-73 additions as untracked (`fetch/`, `make-spec-r73.py`,
`measurement-c1-r73.txt`, `measurement-c2-r73.txt`, `w1-dispatch.json`).

Confidence: **high** on §1 (commands and counts), §2 open-item mapping (quoted bullet + receipt
lines), §4 (ids, URLs, digests, E04 rule read in the script); **medium** on §3's fit judgment
(the unimplemented status is verified, the "best next round" ranking is a judgment).

Remaining unknowns: no validator/renderer was run (out of scope for this seat); whether the
round intends the env/global/environ rows to supersede any held row is a lane decision, not
observable at the base; W04's count after the appends is an upper bound (41) until the actual
scope cells are written.
