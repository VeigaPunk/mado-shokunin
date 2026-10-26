# ExecIndepA — independent `mado-geometry.py` from the PRED-C1-r42 contract (round 43, w1)

Deliverable (single file, stdlib only, 92-check selftest):
`.ufo/waves/round-43/w1/ExecIndepA/mado-geometry.py`
sha256 `8ec6b9504349b35f08bef639e10e02c5d37dae85f8f5aa06754fa2928ecf6381`, 22273 bytes (recomputed after
every edit; this is the file the receipts below were produced with).

Method constraint honoured: the contract was taken from the **docstring only** of
`quality/counters/c1-r42-geometry.py` (extracted with `ast.get_docstring`), and
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` was never opened, read, grepped or hashed by this seat.
The judge was used only as a black box: `importlib` load of the counter module, calls to
`gen_texts(rng)`, `gen_clients(rng, wants)`, `model_rules(text)`, `model_out(clients_raw, texts)`;
`main` was never executed, and no counter body was read (the only counter bytes read are the
docstring and the `--help` output).

## Result

- **Scored `TARGET_MET`, 37/37 fixtures, all five clauses.**
  Command (as assigned):
  `cd /home/vgpnk/Projects/shokunin/mado-shokunin && C1R42_TMP=/fast/scratch/hyaku/mado-r43/ExecIndepA python3 -I quality/counters/c1-r42-geometry.py --repo . --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 --tool <seat>/mado-geometry.py`
  Verbatim tail (`score-c1.txt`):
  `PRED-C1-r42 clause=b rc=0 selftest=92/92`
  `PRED-C1-r42 clause=b2 sites=46 killed=6/6 forced_dead=1`
  `PRED-C1-r42 clauses=a:1 b:1 b2:1 b3:1 g:1`
  `PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=8eb164ce220aa2f6`
  exit 0. The six b2 mutants chosen by that nonce all died (`mutant=0 site=summary_line:331 killed=1 forced`
  through `mutant=5 site=parse_args:52 killed=1`); the forced site is in the function that carries
  `MADO_GEOMETRY: rules=`.
- **No failing fixture line exists**: all 37 fixture lines print `ok=1 ok` (`gen0`..`gen9`, the 27 fixed
  classes and `empty0`). Nothing to report verbatim as a failing fixture.
- **Selftest**: `python3 -I mado-geometry.py --selftest` → `MADO_GEOMETRY_SELFTEST: 92/92 passed`, exit 0
  (`selftest.txt`, `teeth.txt`). 92 checks; the counter's b2 sample (the forced summary site plus five
  nonce-chosen sites) was killed 6/6, and the two hand-flipped parser comparisons below are killed too.
- **Teeth, demonstrated two ways** (`teeth.txt`, `score-mutant-flip.txt`):
  1. one flipped parser comparison, `SIZE_TOKEN.fullmatch(token) is None` → `is not None`
     (`mut-flip-digitcheck.py`, kept as an artifact) → `MADO_GEOMETRY_SELFTEST: 82/92 passed`, exit 1;
  2. `len(args) != 2` → `== 2` (`mut-flip-argcount.py`) → selftest crashes inside `supported_size`
     (`IndexError`), exit 1.
  The counter kills the first mutant too: `fixtures=7/37 tool=present verdict=TARGET_MISSED …
  nonce=34464ec202de871e` (failing lines e.g. `fixture=size0 ok=0 size '0 0': rc=4 want=1`,
  `fixture=regex0 ok=0 rc=4 want=1`, `fixture=empty0 ok=0 case 3: rc=4 want=3`).

## Differential against the judge's model — 1000 random cases, 0 disagreements

Required set: 300. Run: three seed bases, 300 + 300 + 400 cases (`diffany.py`, logs `diff-a.txt`,
`diff-b.txt`, `diff-c.txt`), protocol: `gen_texts(rng)` → `(rule_lines, wants)`, the lines split into
**1-3 consecutive rule files**, `json.dumps(gen_clients(rng, wants))` as the clients document, clients
delivered alternately through a file and through stdin (`--clients -`), stdout compared byte-exactly and
rc compared, stderr required empty. Every case: `model_out(clients_bytes, [file_text…])`.
Result lines: `cases=300 agree=300 disagree=0 base=90210`, `… base=555000`, `cases=400 agree=400
disagree=0 base=987654`.

### The one disagreement this seat found (in my file, now fixed)

First run of the directed probes disagreed on exactly one case (`esc150`), and it was **my file that was
wrong**, not the contract or the counter:

- contract sentence, `quality/counters/c1-r42-geometry.py:34`: "REGEX fully matches 1-200 characters of
  `[A-Za-z0-9_.^$()|*+?-]` and the escapes" (`quotes.txt` Q1, line 34, 6 words) — the bound counts
  **items** of that grammar (a `\.` escape is one item), not source characters;
- I had added a redundant source-length guard (`len(pattern) > 200`), so a 300-character regex of 200
  items was `unsupported` in my tool while the model supports it
  (`esc150`: model `MADO_GEOM_RULE: n=1 … class=a\.a\.…`, my then-output
  `MADO_GEOMETRY: rules=0 … unsupported=1 … verdict=NO_SIZE_RULES`);
- after deleting the guard, boundary probe `probes-regex-bound.txt` agrees at every point:
  `200_plain chars=200 units=200 model_rc=3 mine_rc=3 agree=True`, `201_plain chars=201 units=201
  model_rc=4 mine_rc=4 agree=True`, `200_escapes chars=300 units=200 model_rc=3 mine_rc=3 agree=True`,
  `201_escapes chars=301 units=201 model_rc=4 mine_rc=4 agree=True`, `260_escapes_units chars=320
  units=260 model_rc=4 mine_rc=4 agree=True`, `199_escapes chars=298 units=199 model_rc=3 mine_rc=3
  agree=True`. The selftest now pins the boundary (200 items of escapes accepted at 300 source
  characters; 201 items and 260 items rejected).

After the fix the directed probe set is 18/18 plus a cwd-relative rules path named `-`
(`probes.txt`, `== dash-rules-path agree=True`).

## Contract-text findings (attack the predicate text, not my file)

F1 **`float` field-0 grammar is written asymmetrically, and the literal reading is wrong.**
`quality/counters/c1-r42-geometry.py:32-33`: "field 0 has exactly two argument tokens fully matching
`[0-9]{1,5}` (ASCII digits; size) or exactly one token equal to `on` or `off` (float)" (`quotes.txt`
Q2 line 32, Q3 line 33). The size branch says *argument* tokens; the float branch says "exactly one
token", which read literally makes every real float rule (`float on`) unsupported, because field 0 has
two tokens (`float`, `on`). The judge reads it as one **argument** token: probe `float1`
(`windowrule = float on, match:class x`) → model `MADO_GEOM_RULE: n=1 file=1 effect=float arg=on
class=x`, `float_rules=1`, exit 4; my tool agrees. A w2 seat can quote the literal sentence and argue
the counter's model contradicts its own contract, so the sentence should say "one argument token" —
but the round-43 freeze makes this a *reported* residual, not an edit (the counter is frozen; the model
and the fixtures are what `PRED-C1-r42` scores).

F2 **`TILED` is decided by the client's own `floating`, never by a matched `float` rule.**
`…:43` "floating is true only for JSON true" (Q5) and `…:47` "TILED (not floating)" (Q4) never say which
floating; `…:45` "the last matching `size` rule gives want" (Q6) gives `float_rule` its own output field
but no verdict role. Probe `float2`: rules `size 1 2` + `float on` for class `x`, client
`floating:false, size:[1,2]` → model prints `verdict=TILED` with `float_rule=on`, and my tool agrees
byte-exactly. So the cross-reference reading (`floating` = the client's JSON field) is the scored one;
the contract never states it in one sentence.

F3 **Regex bound wording** (same sentence as my fixed defect): "1-200 characters of [class] and the
escapes" reads naturally as 200 source characters to at least one implementer (me), while the scored
model counts 200 grammar items. Evidence above (`200_escapes` 300 source characters accepted). The
sentence is decidable only from the model, not from the text.

No other disagreement was found: 1000 random cases and 19 directed probes (duplicate JSON keys,
`mapped` 0/null/"false", `floating` 1 vs true, `size` floats/booleans/3-element, tab separators,
`windowrule=` without a space, `float off`-only rule files, leading zeros in `size` args, control
characters in the class, escaped backslash, stdin-vs-file, 1-3 rules files) agree with the judge.

## Operability check on the real receipts (read-only, not scored)

`host-receipts-run.txt` — my tool on the frozen round-43 receipts `fetch/host-gkeep.conf` and
`fetch/host-clients-r43.json`, both invocation forms (file, and `--clients -` from the receipt); the two
forms print identically, verbatim:
```
MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$
MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$
MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT
```
exit 3. The third rule line of the host file, `center on`, lands in `other=1`; no gkeep client is open
in the receipt, so nothing matches. No compositor verb was run: the receipt was read from disk.

## Behaviour implemented (summary)

CLI `--selftest`, or `--clients V` once + `--rules V` one-or-more (two-token, any order); setup
failures print one `MADO_GEOMETRY: SETUP <usage|unreadable|too_large|bad_json>` line and exit 2 in the
contract's order (usage → clients unreadable/too_large/bad_json → rules files in argument order, size
cap 1048576 bytes, stdin read capped at 1048577, FIFOs/directories/missing paths rejected by `stat`
before any open so nothing blocks). Rules: `windowrule[ \t]*=(.*)` full-match, per-field strip, effect
= first token, size/float support grammar as above, 1-based rule numbering across files, file index
per rule. Clients: `mapped is false` skip, class string-or-empty, `floating is true` only, size a
2-element list of non-bool ints ≥ 0, address string-or-`-`, duplicate keys last-wins, control chars
below U+0020 in the class block a match. Last matching size rule gives `want`, last matching float rule
gives `float_rule`; verdict order BADSIZE → TILED → AGREE/DIFFER; summary verdict order
NO_SIZE_RULES(4) → DIFFER(1) → NO_MATCHING_CLIENT(3) → OK(0). Output: rule lines, matched-client lines
in input order, summary; nothing else; stderr empty.

## Evidence retained (all in `.ufo/waves/round-43/w1/ExecIndepA/`)

| file | what it shows |
|---|---|
| `mado-geometry.py` | the deliverable (sha256 above) |
| `score-c1.txt` | full `--tool` scoring run: 37/37, clauses a/b/b2/b3/g, nonce `8eb164ce220aa2f6` |
| `score-mutant-flip.txt` | the same counter on a one-comparison mutant: 7/37 `TARGET_MISSED` |
| `selftest.txt`, `teeth.txt` | 92/92 in the tool; 82/92 and an `IndexError` under two parser flips |
| `diff-a.txt`, `diff-b.txt`, `diff-c.txt`, `diffany.py` | 1000 model-vs-tool cases, 0 disagreements |
| `probes.txt`, `probes.py` | 19 directed probes, all agreeing after the fix |
| `probes-regex-bound.txt` | chars-vs-items boundary table against the model |
| `quotes.txt` | each quoted contract span with its 1-based line in `quality/counters/c1-r42-geometry.py` |
| `host-receipts-run.txt` | the tool over `fetch/host-gkeep.conf` + `fetch/host-clients-r43.json` |
| `mut-flip-digitcheck.py`, `mut-flip-argcount.py` | the two flipped copies (artifacts, **not** deliverables) |

## Risks / residuals (mine, for w2 to attack)

1. My selftest builds its fixtures in the fixed directory `/tmp/mado-geometry-selftest`; two concurrent
   host runs of `--selftest` could race. Inside the counter's sandbox (fresh tmpfs per run) it is
   isolated, and the scored runs above are clean; a host-level parallel run is the only exposure.
2. The tool matches with Python `re`, not RE2 (inherited residual); the REGEX alphabet is restricted to
   the contract's allowed set, but a regex where the two engines differ (`a|b` with anchors, empty
   alternation) is *supported* under both readings only because the alphabet check precedes
   `re.compile`. My selftest pins `^(org.arch.gkeep)$`, `^a$(`, `a(?i)b`, `a*+`, `(`, `a\.b`, `a b`.
3. Clause g is a name heuristic: my file imports only `json os re stat sys`, calls `re.compile`,
   `os.stat`, `os.mkfifo` (selftest), `os.makedirs`, and uses no `**` unpacking, no `getattr`, no
   `__file__`/`sys.argv[0]`/`sys.executable`/`sys.modules`; scored `g:1`. A heuristic can still be
   gamed by a tool that *models* the contract — declared residual of the predicate.
4. `mapped is False` uses Python identity, so `0`, `null`, `"false"` are mapped (contract: "0, null and
   "false" are not false"): probe `map0`/`mapnull`/`mapstr` agree.
5. Integration note for the L1: the counter reads `tools/mado-geometry.py` at the data commit (clause a),
   so this file must be copied to that path in the data commit; the seat dir copy alone scores nothing
   at a revision. I did not touch `tools/`, the registry, the counters or the controls.

## Tooling / host hygiene

No install or update was needed (stdlib only; `python3` and the counter's `bwrap` already present);
`pacman` was not invoked (host-wide pause). No compositor verb, no Wayland connection, no host-service
change: the only host reads were the two frozen receipts. Scratch lived in
`/fast/scratch/hyaku/mado-r43/ExecIndepA/` and was deleted after the receipts above were copied.
No tracked file was written by this seat (`git status` shows my seat files as untracked; the `M LOG.md`
entry there is not mine — nothing in this seat wrote `LOG.md`).
