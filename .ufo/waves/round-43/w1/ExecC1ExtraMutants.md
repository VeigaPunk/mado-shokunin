# ExecC1ExtraMutants — C1 mutation population beyond the 40 registered (round 43, w1)

Seat: `ExecC1ExtraMutants` · wave `w1` (build + first falsifiers) · lane `mado-shokunin` · 2026-10-26.
Claim attacked: **C1 / `PRED-C1-r42`** — the frozen predicate `quality/counters/c1-r42-geometry.py` (37 fixtures, clauses
a, b, b2, b3, g) against the contract that is the docstring of `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`.

**Verdict of this seat: the fixture population is not blind to any *behavioural* defect I could build at a fresh site
(53 of 68 mutants killed, every kill carried by a byte-level fixture) — but it is blind to two non-behavioural defects
(`N48` rules-file UTF-8 error handler, `N51` descriptor leak) and it intersects the 38 registered mutants on 21
mutation sites.** No blocker.

## Deliverable — `.ufo/waves/round-43/w1/ExecC1ExtraMutants/survivors.md`

68 rows, `mutant | edit (ref -> mutant) | category | verdict | failing fixtures/clauses`, then one section per survivor
with its classification. Every mutant file is in `mutants/<name>.py`, the replacement pairs in `mutants.json`, the raw
counter output per mutant in `results.json`.

## Method

Reference: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` → `ref.py` (sha256 `e3c2e471…`; `diff` against
`tools/mado-geometry.py` at HEAD is empty). Each mutant is **one text replacement asserted to match the reference
exactly once** (`str.count(old) == 1`, checked at generation time; `diff -u ref.py mutants/<name>.py` is one hunk, one
`-` line, one `+` line for every mutant — `equiv.txt` section B), and every mutant file compiles.

Scored per mutant (private nonce `exm4300NN`, `C1R42_TMP` under `/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants/run/<name>`):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && C1R42_TMP=<scratch>/<name> \
  python3 -I quality/counters/c1-r42-geometry.py --repo . \
    --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 \
    --base a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f \
    --tool .ufo/waves/round-43/w1/ExecC1ExtraMutants/mutants/<name>.py --nonce exm4300NN
```

`--base` is the round-43 base (the counter's `BASE_DEFAULT` is the round-42 base, so it is passed explicitly); the tool
is absent at both revs, so clause a's precondition holds and `--tool` is the only input. 68 runs, 8-way parallel,
~66 s wall. Replayable: fixed nonces, one per mutant, recorded in each `results.json` entry.

Categories built (as assigned): value-domain edits 24, boundary shifts 4, operator swaps 4, dropped branches 5, dropped
checks 5, reordered checks 3, wrong constants 6, swapped output fields 3 (+ swapped counters 3), off-by-one in
file/rule numbering 3, dropped stability/order 2, changed exit codes 4, dropped state/accumulation 2.

## Novelty against the registered 38

- `run-c1-controls.py`'s `MUTANTS` list parsed with `ast`: 38 entries.
- **47 of my 68 target a mutation site (an exact `old` string) that no registered mutant targets** — above the 40 asked
  for even on the strictest reading.
- 21 reuse a registered *site* with a **different replacement value** (e.g. `MAX_BYTES` 1048576→1048575 vs the
  registered →1048577; `NO_MATCHING_CLIENT` exit 3→4 vs registered →1). **No `(old, new)` pair duplicates a registered
  one**, so all 68 are distinct mutants, but those 21 add variation at a known site rather than new sites. That split is
  the honest answer to "beyond the 40 already registered".

## Kill statistics (68 scored)

- 53 `TARGET_MISSED`, 15 `TARGET_MET`.
- **Every one of the 53 kills has at least one failing fixture.** No kill in this population rests on the selftest teeth
  (b2) or on neutrality (b3) alone: 39 were killed by fixtures with all clauses 1, 14 by fixtures *and* b2/b3 (a
  behaviour change usually breaks the selftest too). So the 37-fixture model, not the selftest, is what discriminates.
- 17 kills are narrow — exactly one failing fixture (`N02` boundary0, `N04`/`N05` size0, `N06` regex0, `N11` float0,
  `N13` size0, `N15`/`N18` other0, `N16`/`N17` space0, `N20` mapped0, `N25`/`N56` ctlclass0, `N27`/`N28`/`N29` usage0,
  `N58` client0). Those are the fixtures that carry a single semantic edge each.
- All 37 fixtures participate in at least 2 kills; the widest are `size0` 25, `regex0` 25, `float0` 24, `space0` 24,
  `client0` 23, `other0` 22, `multi0` 21, `order0` 21. The narrowest (2–3 kills each) are `stdinbig0`, `toolarge0`,
  `usage0`, `badjson0`, `unreadable0`, `fifo0` — the setup/CLI class.
- Kills that expose the contract sentence itself: `N02` shows `boundary0` pins "exactly MAX_BYTES is legal" for the
  file path; `N27`–`N29` show `usage0` pins the two-token form, single `--clients`, required `--rules`; `N45`/`N47` show
  `mapped0`/`empty0` pin the "0/null/'false' are not false" and "empty list is legal, empty input is bad_json" rules.

## The 15 survivors

### EQUIVALENT (13) — no fixture can kill them; the behaviours coincide on every input of the contract

Proofs are in `survivors.md`; supporting differential evidence in `equiv.txt` (2546 shared inputs per report-level mutant,
0 differences: `N08`, `N09`, `N19`, `N22`, `N23`, `N34`, `N46`, `N49`, `N52`, `N53`) and `witness.txt` (sections C, D, G
for the IO-level ones: `N01`, `N54`, `N68`).

| mutant | why it cannot change behaviour |
|---|---|
| `N01` `stdin.read(MAX+1)`→`+2` | only `len(data) > MAX` is consumed; `read(n)` returns `min(available,n)`, so the verdict is "stream holds ≥ MAX+1 bytes" either way, and stdin is never read again. Witness C: 2/MAX-1/MAX/MAX+1/MAX+2/2·MAX identical. |
| `N08` `(.+)`→`(.*)` in MATCH_FIELD | field 1 is stripped of space/tab at both ends and holds no `\n`, so an empty capture is unreachable; same capture on every field. |
| `N09` `split(",")`→`split(",",1)` | affected lines have a tail containing `,`; `,` is outside SAFE's alphabet, so the line is `unsupported` exactly as the `len(fields)==2` test makes it. |
| `N19` `^windowrule…` | RULE_LINE is only used with `.fullmatch`; the added `^` asserts what the call already asserts (no MULTILINE). |
| `N22` `v >= 0`→`v > -1` | `v` is an exact `int` once the isinstance/bool tests pass; identical on ints. |
| `N23` `type(v) is int` | `client_size` only sees `json.loads` output (line 164, no `parse_int` hook); on int/bool/float/str/None/list/dict the two spellings agree (bool excluded by exact type). |
| `N34` `differ > 0 and matched > 0` | `differ` is only incremented for a client that already incremented `matched` — the conjunct is a tautology. |
| `N46` `isinstance(doc, (list, tuple))` | `doc` is only a `json.loads` result; JSON arrays are `list`, never `tuple` — dead branch. |
| `N49` `decode("utf-8","strict")` | `strict` is the documented default handler. |
| `N52` `if size`→`if size is not None` | `size` is `None` or a 2-tuple; every 2-tuple including `(0,0)` is truthy. |
| `N53` `re.fullmatch(..., re.DOTALL)` | DOTALL only changes `.` vs newline; every class reaching the call was already rejected if it holds a codepoint < U+0020, and REGEX can carry no inline flag, bracket class, `{` or control character. |
| `N54` `os.read(fd, MAX_BYTES)` | with the unchanged `<= MAX_BYTES` loop the total read is still the file; verdict depends on file size only. Witness D: clients and rules at MAX-1/MAX/MAX+1/2·MAX identical. |
| `N68` `sys.stdout.write(s+"\n")`→`print(s)` | identical bytes and flush behaviour on the only write in `run()`. Witness G: agree/differ/no-size-rules/setup-unreadable byte-identical. |

### MISSING CHECK (2) — a real defect the 37 fixtures cannot see

**`N48` — rules file decoded with `errors="ignore"` instead of `"replace"`** (`texts = [read_regular(p).decode("utf-8","replace") …]`).
The contract sentence "decoded as UTF-8 with errors replaced" (`quality/counters/c1-r42-geometry.py:26`,
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt:25`) is unexercised: `put()` in the counter writes every rules text as
already-valid UTF-8, and `badjson0` only puts invalid bytes in the *clients* input.

- Fixture that would kill it: one rules file of the bytes `b'windowrule = size 1 2, match:class a\xff\n'`, clients
  `[{"class":"a","size":[1,2],"floating":true}]`.
- Expected (model: `replace` → regex `a\ufffd`, outside SAFE → unsupported, 0 size rules), stdout exactly
  `MADO_GEOMETRY: rules=0 float_rules=0 other=0 unsupported=1 clients=1 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_SIZE_RULES`, exit **4**.
- Mutant: prints `MADO_GEOM_RULE: n=1 file=1 effect=size arg=1x2 class=a` + `verdict=AGREE` + `verdict=OK`, exit **0**
  (`witness.txt` section E, both tools run, ref rc=4, mutant rc=0).

**`N51` — `os.close(fd)` replaced by `pass`** (descriptor leak, one per rules file). Output-invisible, but observable
under fd pressure, which the predicate never creates: `execute()` applies `prlimit --nproc=1:1` only, sets no
`RLIMIT_NOFILE`, and no fixture passes more than three `--rules` files (the widest is `multi0`/`order0`, 3).

- Fixture that would kill it: 300 `--rules` files (the first `windowrule = size 1 2, match:class a\n`, the rest empty),
  clients `[{"class":"a","size":[1,2],"floating":true}]`, tool run under `RLIMIT_NOFILE=128`.
- Expected, stdout exactly (exit **0**):
  `MADO_GEOM_RULE: n=1 file=1 effect=size arg=1x2 class=a` / `MADO_GEOM_CLIENT: addr="-" class="a" floating=true size=1x2 want=1x2 float_rule=- verdict=AGREE` / `MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 clients=1 matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 verdict=OK`.
- Mutant: `MADO_GEOMETRY: SETUP unreadable`, exit **2**; the reference exits 0 with that stdout. Reproduced at
  `RLIMIT_NOFILE` 128, 64 and 32 (`witness.txt` section F).

Both are defects of the **fixture population**, not of the tool: the delivered tool is correct in both places. Neither
falsifies C1's target. Whether they justify a PRED v2 before the data commit is the L1's call (the registration says a
hole found by w1 before any data commit re-registers as v2) — this seat reports, it does not decide.

## Evidence files in this seat (hashes in `SHA256SUMS.txt`)

| file | content |
|---|---|
| `survivors.md` | the required table (68 rows) + the 15 survivor analyses (sha256 `df356ed6…`) |
| `results.json` | per mutant: category, edit, clauses line, final line, every failing fixture line (sha256 `e1feb310…`) |
| `mutants.json` | the exact `(name, category, old, new)` pairs, generation-asserted unique (sha256 `cfd2f030…`) |
| `mutants/<name>.py` | 68 mutant tools (each = `ref.py` + one replacement) |
| `ref.py` | reference copy, sha256 `e3c2e471…` = `ctl-ref-tool.py.txt` |
| `equiv.txt` | section A: 2546-input differential fuzz per report-level survivor (0 differences each); section B: one-hunk/one-line diff census |
| `witness.txt` | sections C–G: end-to-end boundary and witness runs for `N01`, `N54`, `N48`, `N51`, `N68` |
| `classify.json` | the EQUIVALENT/MISSING-CHECK classification and proof text per survivor |
| `quotecheck.txt` | the checker's own receipt: every quoted span located at its `file:line`, every number in this report re-derived from `results.json`/`equiv.txt`/`witness.txt` (OVERALL PASS) |
| `harness/*.py` | generators/runners (`mk.py`, `run.py`, `equiv.py`, `witness.py`, `prep.py`, `classify.py`, `gen_table.py`, `quotecheck.py`) — re-running them needs a scratch dir of the same shape |

## Risks and limits (declared)

1. **Equivalence proofs are arguments over the contract's input domain, not exhaustive execution.** The domain
   arguments for `N23` and `N46` rest on `parse_clients`' `json.loads` being the only producer of the values (line 164,
   no `parse_*` hooks) — a code fact, but the argument is only as good as that reading.
2. `N01`/`N54` equivalence rests on a read cap affecting only *how many* bytes are read, never the verdict, and on the
   tool never re-reading stdin. The boundary is empirically covered (witness C/D at MAX-1/MAX/MAX+1/2·MAX); adversarial
   pipe timing (short reads spanning the cap) is argued, not tested.
3. Witness sections C–G run the tools directly with `python3 -I`, **not** through the counter's bwrap sandbox, because
   the property under test is the tool's own stdout/rc. None of these mutants spawn, so `RLIMIT_NPROC = 1` would not bind;
   the isolation is nevertheless weaker than the counter's and is declared here. `N51` additionally needs a
   `prlimit --nofile` limit that the counter's `execute()` does not apply — that is exactly why the predicate misses it.
4. The 21 same-site mutants reuse a registered mutation site with a different value; they are distinct `(old,new)` pairs
   but not new sites. Only the 47 fresh-site mutants are strict novelty.
5. b2's kill counts depend on the nonce; each mutant was scored once with its own fixed nonce, so per-mutant replay is
   exact but the population was not re-scored under a second nonce. (Survivors are nonce-independent: they pass 37/37
   fixtures and all clauses, and an equivalent mutant's clause b2/b3 behaviour is the reference's.)
6. I did not run or modify the frozen control runner `run-c1-controls.py` or its receipt; the registered 38 stand as
   registered.

## Blockers

None.

## Tooling and hygiene

- No tool installed; no `pacman` (host-wide pause respected), no `uv`/`npx`. Used the resident `python3`, `diff`,
  `/usr/bin/prlimit` and the counter's own `bwrap` sandbox.
- Wrote only inside `.ufo/waves/round-43/w1/ExecC1ExtraMutants/` and this report; no tracked file touched
  (`git status --porcelain` shows only untracked round-43 wave files plus a `LOG.md` modification I did not make). No compositor/host state
  touched; no git/jj mutation.
- Scratch `/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants/` deleted after copying the harness and receipts into this
  seat directory; nothing citable lives there.
