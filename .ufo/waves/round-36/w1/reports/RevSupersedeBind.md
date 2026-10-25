# RevSupersedeBind — reviewer seat, mado round 36 wave 1

Prompt: `.ufo/waves/round-36/w1/prompts/RevSupersedeBind.md`
> Audit the correction-pair rule by reading the gate. Then, from the round-35
> record, list every pointer the gate finds dangling and say for each what a
> legitimate correction pair must contain (old exact string, new path that
> resolves after the round-36 data lands). Report any dangling pointer a
> correction pair cannot honestly close.

Gate read: `quality/check-evidence-pointers.py` (`PRED-PTR-r36-v1`) at
`master` (`f77b554`). The freeze commit is `dbf8b57`; the base is `4243d03`.

## 1. What the gate's correction-pair rule requires

From the gate docstring (`quality/check-evidence-pointers.py:11-27`) and the
implementation:

- `dangling_r35_closed`: every round-35-cited pointer that does not resolve at
  the checked tree must appear as the `old` side of a round-36 correction pair
  in `LOG.md` whose `new` side resolves; `record_intact` additionally requires
  the round-35 record to still carry the two spot-check dangling pointers
  (rewriting the record is not a repair). `SUPERSEDED_POINTERS` =
  `.ufo/waves/round-35/scratch/SimplifyCounter/` and
  `.ufo/waves/round-35/scratch/MutC1Drop/mutants/`.
- Pair syntax (`PAIR` regex, line 47): a line in the round-36 `LOG.md`
  section
  `^\s*-\s*`([^`]+)`\s*->\s*`([^`]+)`\s*$`,
  i.e. `- \`old\` -> \`new\`` with exactly one backtick pair per side.
- `old` must equal the dangling literal exactly (the parser takes
  `m.group(1).strip()`); trailing slashes are part of the literal.
- `new` must resolve in the checked tree: `resolves()` (lines 107-112)
  accepts a file that exists in `git ls-tree`, a directory prefix ending in
  `/` with at least one tracked child, or a glob with at least one match.

## 2. Dangling pointers found by the gate (before/at freeze)

Frozen before-run `.ufo/waves/round-36/receipts/before-pointers.txt` (verbatim):

```
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 pointers_r36=0 dangling_r36=0 inherited_dirty=10 scratch_tracked=124 scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
```

Both dangling pointers are real, and both are the record's own citations
(`LOG.md` round-35 sections, lines 2003 and 2020 at `master`):

- `` `.ufo/waves/round-35/scratch/SimplifyCounter/` `` — "Proposal lives in
  `.ufo/waves/round-35/scratch/SimplifyCounter/` (`count-min.py`, 104 lines
  vs 218, plus `analysis.md`)".
- `` `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` `` — "copies under
  `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` (15 mutants,
  `gen_and_run.py`), each run over all 11 frozen control trees".

Neither path exists in any commit: `git log --all --oneline -- '.../scratch/SimplifyCounter' '.../scratch/MutC1Drop'` is empty. They were untracked scratch at round-35 closure and were removed (D2 resolution), with the durable content relocated to `.ufo/waves/round-35/scratch-evidence/` by commit `4efaf63` ("checkpoint the 235 seat evidence files and drop the 3.2 GB mutant trees").

## 3. What a legitimate correction pair must contain — per pointer

| Pointer (`old`, exact string, trailing slash part of the literal) | What a legitimate pair must carry as `new` | What `new` must resolve to | Current state at `master` |
|---|---|---|---|
| `.ufo/waves/round-35/scratch/SimplifyCounter/` | A directory path that contains the same two artifacts the round-35 entry cited: `count-min.py` (104 lines) and `analysis.md` | `.ufo/waves/round-35/scratch-evidence/SimplifyCounter/` | Resolves: `git ls-tree -r --name-only master .ufo/waves/round-35/scratch-evidence/SimplifyCounter/` → `analysis.md`, `count-min.py`; `count-min.py` is 104 lines (matches the record). **Honestly closable.** |
| `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` | A path carrying the mutant-run evidence the entry cited: the generator `gen_and_run.py` and the results `results.json`; the raw 15-mutant trees are gone by design (3.2 GB dropped, committed `4efaf63`) | `.ufo/waves/round-35/scratch-evidence/MutC1Drop/` | Resolves: `git ls-tree -r --name-only master .ufo/waves/round-35/scratch-evidence/MutC1Drop/` → `gen_and_run.py`, `results.json`. **Closable honestly, with one premise made explicit:** the generator is deterministic and committed, the results are committed, and the round-35 spot-check's own D5 text prescribes exactly this destination (`.ufo/waves/round-35/scratch-evidence/MutC1Drop/{gen_and_run.py,results.json}`). The original raw mutant *trees* do not exist; a pair can honestly point at the evidence that exists, not at the trees that were deliberately dropped. |

The D5 closure in the round-36 `LOG.md` entry (lines 2156-2157) uses exactly
these `old` strings and `new` paths.

### 3a. The third pair (D10 transcript) — not a dangling round-35 pointer

`Quality/receipts/axis-a3094c99ab85bec35534de2447552c47dd2b647f.txt` is the
`old` side of the D10 correction pair. It never resolved in any commit (the
tip transcript was renamed to `axis-520c631…` before landing). It is **not**
in `dangling35` (it is cited only by the round-36 record), so it is not part
of the D5 closing obligation; the pair legitimately supersedes it. The `new`
side `quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt`
resolves and satisfies the `tip_axis_transcript` content check
(`MADO_AXIS: checked=3 mismatched=0 rev=520c631…`).

## 4. Design finding: the frozen correction-pair rule is unsatisfiable without a gate change

The gate as frozen (and as shipped through commit `2d90524`) computed:

```
dangling36 = [p for p in ptr36 if not resolves(p, files)]
```

where `ptr36` includes **every** backtick pointer token in the round-36
`LOG.md` section. A D5 correction pair lives inside that section (that is the
only place `pairs` is scanned), so the pair's own `old` token —
`.ufo/waves/round-35/scratch/SimplifyCounter/` — is re-extracted by
`pointers()`, is pointerish, does not resolve, and therefore lands in
`dangling36` automatically.

Consequence: every revision that had the D5 pairs **also** had
`dangling_r36 > 0`, so the target `dangling_r35_closed=1 AND dangling_r36=0`
was unreachable for any honest record. Verified along the real history:

| Revision | pairs | `dangling_r36` (as the gate then computed it) |
|---|---|---|
| `4243d03` (freeze) | 0 | 0 (setup=missing-r36-sections) |
| `a3094c9` (data) | 0 | 2 (`RevSourceQuotes.md`, `.ufo/waves/round-36/scratch/`) |
| `520c631` (records) | 2 | 4 (both D5 olds + `axis-a3094c99…` + `RevSourceQuotes.md`) |
| `ebc5437` | 2 | 4 (same) |
| `c5d7773` | 3 | 4 (same) |
| `cf175c7` / `2d90524` | 3 | 3 (both D5 olds + `axis-a3094c99…`) |
| `a5f76c9` | 3 | **0** — supersession exemption added |

The exemption (commit `a5f76c9`, "the pointer gate's supersede exemption")
changes the rule to:

```
superseded_old = {m.group(1).strip() for m in PAIR lines in log36}
dangling36 = [p for p in ptr36 if not resolves(p, files) and p not in superseded_old]
```

and only then did the same command produce `dangling_r36=0` and
`verdict=TARGET_MET` (confirmed: `python3 -I quality/check-evidence-pointers.py --rev f77b554` → `dangling_r35_closed=1 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET`, exit 0). So the *as-written* rule was closed by a rule change, not by a clean record. This is the correct engineering outcome — a superseded pointer is "named, not cited" — but it means:

- the freeze's plain text ("a round-36 correction pair in `LOG.md` must carry
  it as `old`") was not executable as written; the gate needed the exemption
  to be satisfiable, and
- the exemption is broader than the D5 pair set: **any** `old` side of **any**
  pair in the round-36 LOG section is excluded from `dangling_r36`, even if
  it was never a dangling round-35 pointer (e.g. the D10 transcript `old`).
  In the current record this is harmless (the D10 old genuinely never
  resolved), but a future pair with a typo'd `old` that does resolve would be
  silently invisible to the gate's `dangling_r36` count. Residual gap, not a
  false pass today.

## 5. Verdict

- Gate audited: yes. Dangling pointer list reproduced from the freeze receipt
  and from the record: exactly two (`SimplifyCounter/`,
  `MutC1Drop/mutants/`), both closable by the pairs the record now carries.
- Both pairs in the record are **honest** per §3: each `new` path resolves
  and carries the substantive evidence the round-35 entry cited; the
  MutC1Drop raw trees are the one deliberate exception, named as such and
  pinned by the spot-check's own D5 prescription.
- No dangling pointer exists that a correction pair cannot honestly close; the
  only "cannot" is the *as-frozen rule* (pair old-sides re-poison
  `dangling_r36`), which the supersession exemption resolved — recorded here
  as the design finding with the proof history above.

Evidence pointers: `quality/check-evidence-pointers.py` (rule, lines
45-52, 107-112, 145-160); freeze receipt
`.ufo/waves/round-36/receipts/before-pointers.txt`; `LOG.md` round-35
sections (lines 2003, 2020) and round-36 D5 bullets (lines 2156-2157);
commit `4efaf63` (scratch-evidence checkpoint / mutant-tree drop); commit
`a5f76c9` (supersession exemption); after-receipt
`.ufo/waves/round-36/receipts/after-pointers.txt`; tip run quoted in §4.
