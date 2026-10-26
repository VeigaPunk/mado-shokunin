# ExecIndepA — C1 differential implementation, round 44 w1

Seat: `ExecIndepA` (leaf). Assignment: implement C1's contract extension **differentially** — from the
frozen counter text alone — and score it. Independent means: I did **not** open
`.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` at any point, and nothing in this report depends on it.

## Files written (all inside the lane, my seat only)

| path | what |
|---|---|
| `.ufo/waves/round-44/w1/ExecIndepA/mado-geometry.py` | the round-43 tool (`tools/mado-geometry.py`, sha256 `e3c2e471…`) plus the state extension; sha256 `b7db9b4a7ff8ebe7f1970cb6126bbdba29c05a528524cdcd5612e6327677b3d8` |
| `.ufo/waves/round-44/w1/ExecIndepA/score-receipt.txt` | the scoring transcript (4 runs of my tool: 1 random nonce + 3 fixed nonces `0000000000000001`, `aaaaaaaaaaaaaaaa`, `ffffffffffffffff`, plus the round-43 control at the pinned nonce) |
| this report | |

No tracked file, counter, control, registration, reference or pin was edited. `tools/mado-geometry.py`
is untouched (still sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`) — the L1 is
the integrator.

## Result

**`PRED-C1-r44: fixtures=26/26 tool=present verdict=TARGET_MET rev=e2289516a9a857f55cda7be635933e89b931c3da`, exit 0,
clauses `a:1 b:1 b4:1 g:1 r:1`** — reproduced on the 4 nonces recorded in the receipt, no failing fixture on any of them
(`score-receipt.txt`, lines for `nonce=0000000000000001`, `…aaaaaaaaaaaaaaaa`, `…ffffffffffffffff` and two
random nonces).

Clause r (the no-harm clause) passes on the same bytes: `PRED-C1-r42: fixtures=37/37 tool=present
verdict=TARGET_MET` — the round-43 contract still holds byte-exactly, i.e. the extension added the state
words without touching any state-free output byte.

`b`: `MADO_GEOMETRY_SELFTEST: 112/112 passed` (round-43 tool had 73; I added 39 state cases).

## What the extension is (file:line in my copy)

- `fsmode_of(c)` (`:191-204`): `type(f) is not int → 0`, then `f == 1 → 1`, `f == 2 → 2`, else `0`. So
  `true`, `2.0`, `"2"`, `3`, `-1`, `null`, `[2]`, `{"internal": 2}` and absent are all 0.
- `verdict_of(size, want, floating, mode)` (`:207-219`): `BADSIZE` (size none) → `FULLSCREEN` (mode 2) →
  `MAXIMIZED` (mode 1) → `TILED` (not floating) → `AGREE` (size == want) → `DIFFER`.
- `evaluate` (`:228-256`) increments only the chosen verdict's tally key (`tally[verdict.lower()]`), so a
  BADSIZE client with fsmode 1/2 contributes to `badsize` alone; `matched` is incremented before the
  verdict, as in round 43.
- `states_of(t)` (`:284-288`) returns ` maximized=<n> fullscreen=<n>` iff their sum > 0, else `""`;
  `report` (`:276-280`) splices it between `badsize=<n>` and ` verdict=`.
- Docstring: the "Client state." paragraph (`:51-58`), the bracketed summary token (`:63`), the
  conditional sentence (`:66-68`). The TILED sentence is narrowed for pseudo-tiled clients (`:56-57`),
  matching closure D3 — a pseudo-tiled client is non-floating and reports TILED.

## Failures

No counter fixture or clause failed. One failure occurred and it was **my file, not the contract**:

```
SELFTEST FAIL fs-client-line: got 'MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$' want 'MADO_GEOM_CLIENT: addr="0x1" class="org.omarchy.gkeep" floating=true size=2560x1440 want=420x500 float_rule=on verdict=FULLSCREEN'
```

My case indexed `lines[1]` as the client line, but the `gk` config holds **two** supported rules (float on,
size 420 500), so `lines[2]` is the first client line — the contract ("per supported rule … per matched
client … last") is unambiguous here. Fixed by indexing `lines[2]`; the case now pins the whole FULLSCREEN
client line byte-exactly.

## The delta is the state logic (measurement, not assumption)

Same revision, same pinned nonce `0000000000000001`, `--tool tools/mado-geometry.py` (round-43, unmodified):
`fixtures=14/26 verdict=TARGET_MISSED`, `b:0 b4:0`. The 12 fixtures it fails are exactly the state ones,
and each failure is the false report the claim cites — the old tool returns rc 1 (DIFFER) where the target
returns 0, e.g. `fixture=fs0 ok=0 rc=1 want=0`, `fixture=maxfloat0 ok=0 rc=1 want=0`,
`fixture=fsagree0 ok=0 stdout line 3 got='MADO_GEOM_CLIENT: … size=420x…`. (The lattice count is
nonce-dependent — 12 here, 13 in `receipts/ctl-c1.txt`, 12–13 at base per the registration; the verdict is
not.)

`b4` teeth, all 12 sites flipped and **all 12 killed** (`need=9`), so the state logic is load-bearing in
the selftest and not just in the fixtures:

```
evaluate:233,241,245,249   fsmode_of:198,200,202   states_of:286
verdict_of:209,211,213,217
clause=b4 sites=12 killed=12 need=9
```

(evaluate's four sites count because its tally literal holds the string `"fullscreen"` — clause b4 is a
name-based heuristic, as its residual says.)

## Contract sentences I needed to read twice

1. "fsmode is the `fullscreen` value when it is a JSON integer (not a boolean, not a float) equal to 1 or 2,
   else 0" (counter docstring `:17-19`).
   - Reading A: type test — `type(v) is int` (so `true` and `2.0` are 0, because Python's `True == 1`).
   - Reading B: value test — `v == 1 or v == 2` on any JSON number, which would admit `true` and `2.0`.
   - **Decided by `fsvals0`** (`FIXED`, counter `:243`): `True`, `2.0`, `"2"`, `3`, `-1`, `None`, `[2]`,
     `{"internal": 2}`, `0` must all be `differ=1` with no state segment. Reading A. Not a hole. My
     `fsmode_of` is A and `fsvals0` passes.

2. "The summary line carries ` maximized=<n> fullscreen=<n>` … exactly when maximized + fullscreen > 0"
   (counter `:21-23`) — **whether the two counters are per-verdict or per-fsmode.**
   - Reading A: `maximized`/`fullscreen` count clients whose *verdict word* was MAXIMIZED/FULLSCREEN.
   - Reading B: they count every matched client whose fsmode is 1/2, whatever verdict the order produced —
     so a BADSIZE client with fsmode 1 would set `maximized=1` and switch the segment on.
   - These differ exactly on `[G(None, 1)]` and `[G([420.0, 500], 2)]`. **Decided by `fsbad0`**
     (counter `:241`): the expected summary there is `badsize=1` with **no** state segment, so Reading A.
     I first read B; only `fsbad0` and the counter's `t[v] += 1` disambiguate — the prose alone does not
     say "per verdict". Narrow docstring weakness, not a hole (a fixture decides it).

3. "FULLSCREEN and MAXIMIZED clients count as matched and never as differ" (counter `:23-25`).
   - Reading A: they increment `matched` only.
   - Reading B: "matched" could also mean "counted as agree" (both are non-differ outcomes).
   - **Decided by `fsagree0`** (counter `:238`): `[420, 500]` with fsmode 2 must print `agree=0
     fullscreen=1 verdict=OK`, i.e. FULLSCREEN beats AGREE and adds nothing to `agree`. Reading A. Not a
     hole.

4. Clause b4: "the comparison sites of every function (selftest, main, usage and functions nested in
   selftest excluded) whose body holds a string constant containing `fullscreen` (any case) number >= 6;
   each is flipped … must fail for >= 75 % of them (rounded up)" (counter `:37-41`).
   - Reading A: "number >= 6" is the count of *sites*; every site is flipped; need = ceil(0.75 · N).
   - Reading B: "number >= 6" attaches to the string constants; "them" refers to functions, not sites.
   - **Decided by the counter's own line** `clause=b4 sites=12 killed=12 need=9`. Reading A. Not a hole.
     The trap is real though: a formatting helper (`states_of`) becomes a site merely because its docstring
     says `fullscreen`, so its `> 0` comparison is mutated and must be killed — which is why I assert the
     **exact** state-free summary line in `--selftest`, not just a substring.

### One fixed-fixture gap (hole, narrow)

**FULLSCREEN before TILED is not pinned by any fixed fixture.** In `FIXED` (counter `:236-261`) every
client carrying `fullscreen` 1/2 is floating except `max0`/`maxfloat0`, which use mode 1:
`fs0`, `fsagree0`, `fsmix0`'s state clients and `fsstdin0` all use the default `floating=true`. So
MAXIMIZED-before-TILED is decided (`max0` `:239`, `fl=False` + mode 1 must print MAXIMIZED), but a tool
that put TILED before FULLSCREEN would pass every fixed fixture and be caught only when the nonce lattice
(`gen_state_clients` draws `floating` and `fullscreen` independently) happens to draw mode 2 with
`floating=false`. I implemented the sentence's order and it passes `fsmany0`/`sgen*` on all four recorded nonces,
but the fixed set should gain `G([2560, 1440], 2, fl=False)` (and ideally `G(None, 2)` for
BADSIZE-before-FULLSCREEN with a missing size rather than a bad one) if this predicate is ever revised.

## Risks / residuals

- My tool is a model of the contract (the counter's declared residual 1): it is an implementation, and
  passing proves conformance to the model, not to a live Hyprland.
- Nothing here was checked against real compositor state: no `hyprctl clients -j` dump with a stateful
  gkeep window exists unattended, and the registration says the fact is the pinned source's.
- `b4`'s teeth are name-based: moving state logic into a helper without the word `fullscreen` in its body
  would escape it (counter residual, not a defect I introduced).
- No tool was installed, upgraded or removed (python3 3.14.8, `/usr/bin/bwrap`, `/usr/bin/prlimit` were
  already present); no package transaction, no compositor mutation, no git/jj mutation.
- Scratch `/fast/scratch/hyaku/mado-r44/ExecIndepA/` deleted after the receipts were copied into the seat
  directory; every citation above names a file under
  `.ufo/waves/round-44/w1/ExecIndepA/` (or a frozen counter line).
