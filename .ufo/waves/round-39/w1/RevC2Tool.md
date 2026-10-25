# RevC2Tool — C2 tool review: `tools/mado-options.py` vs its claim (round 39, w1)

Reviewed at lane tip `457d1b125932c1e0d797061a2156b917bcd7edaa` (freeze commit).
Claim: C2 (registration.md) — static config-option resolver, strict regular-file policy,
last-declarer ownership, `--getoption` merge with the five-word divergence vocabulary.
Predicate: `PRED-C3-r39-v1` (docstring of `quality/counters/c3-r39-options.py`).
State note: `tools/mado-options.py`, `quality/counters/c3-r39-options.py`, and
`.ufo/waves/round-39/w1/` are all untracked at review time (pre-data-commit; expected).

## Verdict summary

The **tool itself satisfies every enumerated claim surface** (selftest 69/69, fixtures 4/4,
strict refusals named, correct last-declarer resolution on tricky orderings, correct row
shape, all five agreement values). However the **claim's counting pipeline cannot emit
TARGET_MET today**: three structural defects, two in the counter and one in the fixture
script's coupling to it. All three are fixable before the data commit (counter and fixture
script are not yet frozen/committed). One low-severity tool defect (conditional-comment
nesting) plus one vocabulary nuance.

## Tool-level verification (all exercised, not read-only claims)

- **No compositor/socket/network**: read path is `os`/`glob`/`json`/`argparse`/`stat` only
  (`read_bytes` tools/mado-options.py:200, `handle_source` :315, `merge_rows` :468).
  `subprocess` (import :72, use :554) is reached **only** from `--selftest` (:568), running a
  copy of itself in a tempdir. No socket/urllib/http imports; `--getoption` reads a JSON
  file, never hyprctl. Import set matches the counter's clause-g stdlib allowlist.
- **Strict regular-file policy, named refusals** (`read_bytes` :200: `os.stat` + `S_ISREG`,
  path in every message):
  - FIFO as source target → exit 3, name in stderr (counter sandbox clause e=1; fixture 3).
  - Dangling symlink source → exit 3 named (fixture 4).
  - Directory as source / directory glob match / missing root / unresolved glob → exit 3
    named (selftest asserts each).
  - Symlink→regular file root works (selftest); recursive `source=` refused named, exit 3
    (my probe: `mado-options.py: recursive source: /tmp/.../hyprland.conf`).
- **Source graph**: globs (sorted, last match wins — selftest `smart_gaps` z.conf),
  `~` expansion, `./` and `../` relatives, **variables in source paths** (probe:
  `$dir = sub` + `source = ~/.config/hypr/$dir/x.conf` resolved), `##`→`#` escape
  (`shadow:color = #000000`, selftest), trailing comments, `\`-continuations, categories
  with per-file brace scoping (all selftest-asserted).
- **Last-declarer resolution**: fixture checker run in a /tmp mirror → `fixtures=4/4`,
  exit 0 — covers layer ordering (defaults → theme → user → toggles glob → ai-usage),
  depth-first parent-after-source precedence (`misc:deep_value` parent line 7 beats
  child source), glob order. My probes: same-file re-declare → last wins; exact-lhs
  exclusion keeps `binding = keepme` and `binds:binding = cat` as options while all
  directive verbs (bind/unbind/animation/bezier/monitor/env/exec-once/workspace/
  windowrulev2/submap/layerrule) are excluded (selftest exact-key-set assertion).
- **Row shape**: `{key, value, owner, layer, line, set}` (+ `agreement` only when merged);
  superset of counter `FIELDS`. Live-only rows carry `owner/layer/line: null` — present as
  keys, so clause d shape holds.
- **`--getoption` merge vocabulary**: all five values exercised — `agreement`,
  `agreement*` (shadowed declarer, `_decls>1`), `mismatch` (value inequality and
  set=false-despite-declarer), `config-only`, `live-default` (selftest asserts each;
  probe re-confirmed `agreement*` for same-file double declare, truthy normalization
  `true`↔`1`, scalar-vs-tuple `0`↔`0 0 0 0`).
- **`--selftest`**: `MADO_OPTIONS_SELFTEST: 69/69 passed`, exit 0 (assertion count 69,
  >40 as documented; printed at tools/mado-options.py:994).
- **Exit map**: observed 0 / 2 (no `--home`) / 3 (strict failures) / 4 (missing or
  malformed getoption JSON). Exit 1 (selftest-fail) not exercised; statically correct
  (:996-999).

## Deviations from the claim

### D1 — HIGH (claim-blocking; counter, not tool): assertion-count vocabulary mismatch
`quality/counters/c3-r39-options.py:79` extracts assertions with
`re.finditer(r"(\d+)\s*/\s*(\d+)\s+assertions?", ...)` but the tool prints
`MADO_OPTIONS_SELFTEST: 69/69 passed` (:994) — the word "assertions" never appears.
Counter parsed `assertions=0` → clause b=0 despite `selftest_rc=0`. Empirical: sandbox run
of the unmodified counter against a synthetic repo holding the identical tool bytes printed
`clause=b selftest_rc=0 assertions=0 ok=0`. Fix before freeze: either side adopts the
other's vocabulary.

### D2 — HIGH (claim-blocking; counter): clause f makes TARGET_MET unreachable
`quality/counters/c3-r39-options.py:134`: `clauses["f"] = int(not tool_present)` where
`tool_present` is evaluated at `--rev`. With the tool present at the data commit clause
f=0; with it absent, `met` (:153) also fails on `tool_present`. Both branches of `met`
cannot hold → verdict is TARGET_MISSED by construction. The docstring's intent ("the BASE
revision lacks the tool") is already enforced by the Setup guard (`exit 2` if present at
base). Empirical: sandbox run printed `clauses=b:0 c:0 a:1 d:0 e:1 f:0 g:1` →
`verdict=TARGET_MISSED`. Fix: `clauses["f"] = 1` (precondition already guarded) or base on
`show(repo, base, TOOL) is None`.

### D3 — HIGH (claim-blocking; fixture script ↔ counter coupling): `--tool` ignored
`run-fixtures.sh` has no argument parsing: `--tool`/`--repo` (passed by the counter,
quality/counters/c3-r39-options.py:107) are silently discarded; `TOOL` is always
`$HERE/../../../../..` + `/tools/mado-options.py` (lines 9-11, five levels up from the
script). When the counter copies the script into its sandbox and runs it there, that path
does not exist → every fixture FAILs. Empirical: mirror run printed
`FAIL fixture1 tool-missing: /tmp/revc2-fixrun/tools/mado-options.py … fixtures=0/4`;
after placing the tool exactly where the script derives it, the same script scored
`fixtures=4/4` exit 0 — fixture **content** is sound; only the location coupling is broken.
Also: the counter reads the fixture from `rev:FIXTURE` where FIXTURE is hardcoded to
`.ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh` (another seat's untracked
path) — it must be committed at the data commit or clause c is 0 even with D3 fixed.

### D4 — LOW (tool): `# hyprlang if` region nesting is broken and untested
`parse_comment` (:286) evaluates each `if` against the variable table alone;
`parse_line` (:340) skips lines only when the top of `st.ifs` is failed. Probe:
```
# hyprlang if $undefined_var      → push failed=True
# hyprlang if !$undefined_var     → push failed=False (evaluated regardless of outer)
misc { leaked = 1 }               → DECLARED (rc=0), contradicts enclosing failed region
```
Output contained `misc:leaked`. Sibling failed-if regions are likewise un-skipped once a
later `if` pushes False. Contradicts the docstring's "if/endif nesting" promise; the
selftest contains zero `hyprlang if` fixtures, so 69/69 does not cover this surface.
Impact bounded: real omarchy trees rarely nest conditionals; but the claim's "comments"
surface is documented as nesting-capable.

### D5 — INFO (vocabulary nuance): live-only key with `set=true` is labeled `live-default`
The docstring defines live-default as "live row with no declarer; set=false", but
`merge_rows` (:468) labels any live-only row `live-default` regardless of `set` (probe:
`only:live` set=true → `live-default`). The claim's five-word vocabulary is still fully
present; this only loosens one docstring phrase.

## Residual risk / verification gaps

- Counter could not be run against the real lane repo pre-data-commit (tool untracked, and
  I must not commit); the sandbox substitutes a synthetic repo with byte-identical tool
  content — same code path except the blob's origin.
- Exit 1 (selftest-fail) path and a stat/open TOCTOU race untested (out of claim scope).
- Nested `{{ … {{ … }} … }}` expressions would ExprError-skip the line; not probed, likely
  matches hyprlang rejection.
- Installs: none. Host untouched; all probes under /tmp; the only lane write is this file.

## Bottom line

Tool: accept-quality (69/69 selftest, 4/4 fixtures, every claimed surface exercised and
passing). Claim pipeline: NOT ready — D1/D2/D3 each independently force
`verdict=TARGET_MISSED` at any data commit. All three are pre-freeze fixable (counter and
fixture script still untracked): align the assertion banner regex, make clause f reflect
the base precondition, and make run-fixtures.sh honor `--tool` (or commit it at a path
where its derived TOOL resolves inside the counter sandbox). D4 is a small tool fix
(evaluate `if` only when no enclosing region failed) plus a selftest case.
