source: S438 — git v2.56.0 `Documentation/git.adoc` (tag v2.56.0, fetched 2026-11-03, sha256 050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79, 47005 bytes; quotes at `git.adoc:180-181,928-929`) — the documented `--no-replace-objects` option and `GIT_NO_REPLACE_OBJECTS` environment entry that make "constructed" and "in effect" two different facts
verified-at: 2026-11-03
recheck: 90d — re-fetch the tag's `Documentation/git.adoc` and re-hash it; also when the host git leaves 2.56.0, when the r69 controls, the census population regex or the guard key change, or when `quality/counters/c2-r69-guard-dominance.py` is superseded

# Lane gate git reads: key position, dominance, and the census that stopped counting mentions (MADO-R69-1)

## Scope

Lane-tooling scope only. This entry explains the mechanics behind round-69 claim C2
(`.ufo/waves/round-69/claims-declaration-r69.md:89-159`): why the round-68 reader census
scored a *mention* as a guard, what the round-69 rule requires instead — the key must sit in
**key position** of an environment mapping, and that mapping must **dominate** a `git` process
launch — which eleven frozen cases pin the two rules, where the counted population begins and
ends, and what the resulting `guarded=13 unguarded=0` line still does not establish. It is not
a desktop claim, not a state-cell truth claim and not an authenticity claim about repository
objects: the replacement mechanism and its fixture measurements stay in the held row S436
(`git-replace.adoc:34`, `corpus/knowledge/replace-ref-citation-boundaries-r67.md`) and in the
round-68 entry (`corpus/knowledge/gate-git-read-guards-r68.md`). This entry opens S438
(`git.adoc:180`, `git.adoc:928`) for the documented switch the dominance rule is about.

Host git measured for the fetch: `git version 2.56.0`.

## 1. What the round-68 census accepted without a guard

The round-68 classifier (`quality/counters/c2-r68-reader-guard.py`) asked one question of an
accepted environment expression: does the key string `GIT_NO_REPLACE_OBJECTS` occur anywhere
in it (`carries_key`, `:106-112`)? Presence, not position; construction, not delivery. Re-run
against the round-69 frozen control set at the base revision
`04093b83f73a841117d3b31dbb2a6063f4f2a454`, it scores **7/11** (rc 1):

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=7/11 verdict=TARGET_MISSED rev=04093b83f73a841117d3b31dbb2a6063f4f2a454
```

The pre-freeze receipt records the same number and names the four cases the r68 rule gets
wrong — exactly the four it accepts as guarded
(`.ufo/waves/round-69/control-baseline-r69.txt:33-46`, `MADO_R69_C2_BASE: controls=7/11
verdict=TARGET_MISSED`):

| rejected by r69 | construction the r68 rule scored as a guard | why no child receives the guard |
|---|---|---|
| `value-position-only` | `env = {"PATH": "/usr/bin", "LABEL": "GIT_NO_REPLACE_OBJECTS"}` | the key string is a *value*; no variable of that name is set in the child environment |
| `dead-branch-only` | `if False:` then `env["GIT_NO_REPLACE_OBJECTS"] = "1"` | the store never executes; the mapping handed to the call carries no key |
| `uncalled-helper` | a `guarded_env()` helper defined but never called | the call site uses a plain mapping; the guard reaches no launch |
| `overwritten-env` | guarded literal, then `env = {"PATH": "/usr/bin"}` before the call | the name is rebound; the call receives the second mapping |

The count does not move this round. At `04093b83` the round-68 repair already reads
`population=20 readers=13 guarded=13 unguarded=0`, so C2's bounded score stays `10 × 13/13`
and the claim moves **discrimination** on the frozen cases (`7/11` → `11/11`), not the guarded
count. The four wrong verdicts are the whole delta; the seven correct ones (`guarded-inline`,
`update-guard`, `subscript-guard`, `module-constant`, `producer-helper`, `argv-name-flow`,
`mention-only`) stay correct under both rules.

## 2. Key position (rule 1)

The guard key counts only where it is a **key** of an environment mapping — a mapping the
child could receive as `env`. Four constructions qualify, and one near-miss does not:

| # | key-position construction | shape | frozen case |
|---|---|---|---|
| 1 | dict-literal key | `env = {"PATH": ..., "GIT_NO_REPLACE_OBJECTS": "1"}` | `overwritten-env` (first binding only; that case is negative for its rebinding) |
| 2 | subscript store on an env-named mapping | `env["GIT_NO_REPLACE_OBJECTS"] = "1"` | `subscript-guard`, `module-constant`, `producer-helper`, `argv-name-flow` |
| 3 | `update`/`setdefault` keyword on an env-named mapping | `env.update(GIT_NO_REPLACE_OBJECTS="1")` | `update-guard` |
| 4 | `dict(KEY=…)` keyword | `dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` | `guarded-inline` |
| — | **value position** (rejected) | `{"PATH": "/usr/bin", "LABEL": "GIT_NO_REPLACE_OBJECTS"}` | `value-position-only` |

No *positive* frozen case isolates construction 1: the only dict literal carrying the key in
key position is `overwritten-env`'s first binding, and that case is expected unguarded because
of the later rebinding. The construction is therefore exercised, but its own verdict is not
scored anywhere in the set.

The env-named anchor is carried over from round 68: a local name tests as env-named when its
lower-cased text contains `env` (`env`, `GIT_ENV`, `git_env`), and an `env=` keyword is
accepted on any call. What changed is what may sit inside that anchor: a matching constant in
value position, which round 68 accepted, now reads as unguarded (`value-position-only`).

Key position is rule 1's whole content; the assigned value is not interpreted. That matches
the document for this key — S438 states the option is equivalent to exporting the variable
"with any value" (`git.adoc:180-181`) — and the round-67 fixture measured `1`, `0`, empty,
`true` and `false` all suppressing replacement (`corpus/knowledge/replace-ref-citation-boundaries-r67.md:51`).

## 3. Dominance (rule 2): the guarded mapping must reach the launch

Key position alone would accept a construction no call ever receives, so the round-69 rule
adds delivery: the guarded environment must reach a process launch of `git` — a call whose
argv literal, or a name bound to an argv literal, contains `git`. Three flows are accepted,
all confined to one module:

| flow | shape | frozen case |
|---|---|---|
| (a) inline | the mapping is written at the git call: `subprocess.run(["git", ... "show" ...], env=<guarded mapping>)`, including a call to a local producer in `env=` | `guarded-inline`, `argv-name-flow` |
| (b) named binding / producer | an env-named name bound to a key-position mapping, or to a call to a local function that returns one, then used as `env=` or as an argument at the git call, with no intervening rebinding of the name to a mapping without the key | `module-constant`, `update-guard`, `producer-helper`, `subscript-guard` |
| (c) one hop | the guarded name is passed as an argument to a locally defined function whose env-named parameter is passed as `env=` at the git call inside it | none (see §4) |

Two exclusions complete the rule:

- **Literal-false branches.** An `if False:` / `while False:` body does not execute, so a
  construction inside one is not a guard (`dead-branch-only`).
- **Prose.** Comments and docstrings are not expressions; a file that only names the key is not
  guarded (`mention-only`, unchanged from round 68).

Delivery is the documented point of the key, not an extra lane convention. S438 states that
`--no-replace-objects` "is equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment
variable" (`git.adoc:180-181`), and that the variable acts on "setting and exporting this
environment variable" (`git.adoc:928-929`) — the environment the child receives, not a string
built anywhere in the parent. The round-68 limit that a guard can be built and then filtered
away is the same fact from the other side
(`corpus/knowledge/gate-git-read-guards-r68.md`, §5).

## 4. The eleven frozen cases

All eleven cases carry the `git` token and a quoted object-read verb, so every one is a
reader: the frozen set discriminates only the guard predicate. `expect_guard` is the scored
half.

| case | reader | guard | what it pins |
|---|---|---|---|
| `guarded-inline` | yes | **yes** | flow (a): `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` written at a `git show` call |
| `value-position-only` | yes | no | rule 1: the key string in value position sets no variable |
| `dead-branch-only` | yes | no | the literal-false exclusion: the store at `if False:` never runs |
| `uncalled-helper` | yes | no | dominance: a producer defined but never called reaches no launch |
| `overwritten-env` | yes | no | flow (b)'s no-intervening-rebinding clause |
| `update-guard` | yes | **yes** | construction 3, then `env=` at a `git ls-tree` call |
| `subscript-guard` | yes | **yes** | construction 2 inside a helper: purge, store, then `env=` at the helper's own call |
| `module-constant` | yes | **yes** | flow (b) at module scope: binding and store outside any function |
| `producer-helper` | yes | **yes** | flow (b) through a producer: `env = git_env(work)` then `env=` |
| `argv-name-flow` | yes | **yes** | argv need not be a literal at the call (`cmd` holds it) and a producer call in `env=` counts |
| `mention-only` | yes | no | prose is not a construction (docstring + comment, `env=dict(os.environ)`) |

Coverage gaps in the frozen set, stated so the counts are not read as more than they are:

- No case isolates flow (c). The committed prototype accepts a one-hop snippet the frozen set
  does not contain — `def run_git(repo, env): subprocess.run(["git", ...], env=env)` called as
  `run_git(repo, env)` with a guarded `env` classifies `(reader=True, guard=True)` — but that
  is a prototype probe, not a frozen case.
- No positive case isolates the plain dict-literal key (§2 construction 1); its only
  appearance is inside a case whose verdict is driven by a rebinding.
- No case is a non-reader. `expect_reader` is true for all eleven, so a change to the reader
  vocabulary is not scored by this control set.
- The positive cases are all delivery shapes for one key; the set says nothing about a second
  guard key, a second object-read verb family, or a non-`subprocess` launcher.

## 5. Population boundary

The denominator is defined by path and read from git objects, unchanged from round 68:

- pattern `^quality/check-[^/]+\.py$` — the lane's standing gate files only, no subdirectory;
- enumerated with `git ls-tree -r --name-only <rev> -- quality` and read with
  `git show <rev>:<path>`, never from a worktree;
- at the base revision `04093b83f73a841117d3b31dbb2a6063f4f2a454`: **population 20, readers 13,
  guarded 13, unguarded 0** — measured with the committed prototype
  (`.ufo/waves/round-69/proto/c2-classify.proto.py`: `SUMMARY population=20 readers=13
  guarded=13 unguarded=0`, rc 0) and reproduced by the round-68 counter at the same revision
  (`population=20 readers=13 guarded=13 unguarded=0`). The receipt pins the denominator alone
  (`.ufo/waves/round-69/control-baseline-r69.txt:48-50`, `population_at_base=20`).

The seven non-readers — no `git` token paired with a quoted object-read verb in the blob — are
`check-counter-discrimination`, `check-locators`, `check-population`, `check-r38-discrimination`,
`check-r55-controls`, `check-r56-controls` and `check-state-cite` (all `.py` under
`quality/`). The thirteen readers are `check-anchor-cover`, `check-axis-scores`,
`check-control-receipts`, `check-deliverables`, `check-evidence-pointers`, `check-freeze-order`,
`check-index`, `check-index-rows`, `check-landed-contract`, `check-round-outcome-first`,
`check-session-material`, `check-tool-ledger` and `check-wave-done`. Every one of the thirteen
carries the key in key position and delivers it to its git calls at the base revision; the
round-68 repair is what moved `guarded=1` to `guarded=13` there.

Outside the denominator:

- `quality/counters/*` — the per-round instruments and their pinned history; a counter may not
  be counted as a repaired reader, and the population regex excludes the subdirectory;
- `tools/*` and the shell instruments (`quality/landing-counters.sh`) — not
  `quality/check-*.py`, and shell has no AST for this rule;
- round 67's wider lexical set — 82 files under `quality/` and `tools/` mentioning a git
  command token, 79 of them containing `show`/`cat-file`, 3 children guarded at `061dc329`
  (`corpus/knowledge/replace-ref-citation-boundaries-r67.md:78-86,168-169`); that is a grep
  census, not this population, and its 76 unguarded files stay a declared residual;
- seat drafts and `.ufo/` receipts — evidence, never counted.

## 6. What the rule does not prove (Limits)

- **Single module, one hop.** Flow (c) stops at the first locally defined function; there is no
  import graph, no cross-module producer and no two-hop parameter chain. A guard produced in
  one module and consumed in another is invisible to the consumer.
- **No alias, attribute or container flow.** `self.env`, `cfg["env"]`, a list of mappings,
  `functools.partial(subprocess.run, env=env)` and a mapping stored in a dict are not followed;
  only a bare local name carries the guard.
- **No path sensitivity beyond literal-false.** `if os.environ.get(...)`, `if sys.platform ==
  "win32"`, `try`/`except` fallthrough and an early `return` are never evaluated. A store
  inside `if True:` counts; a store that a preceding `return` makes unreachable still counts.
- **Ordering is existential per file, not per call.** The prototype accepts the first guarded
  use after the construction: a guarded use followed by an unguarded rebinding and a second
  git call still reads guarded (measured on a probe: `(True, True)`). Conversely a key stored
  after the use is not counted (probe: `(True, False)`). One dominant use is enough; the rule
  does not prove that *every* launch in the blob is guarded.
- **Delivery is a call-shape test, not execution.** The prototype treats any call whose
  arguments contain a literal argv naming `git`, or a name bound to one anywhere in the module,
  as the launch, so a wrapper that receives the argv literal counts even if it launches nothing
  (probe: `(True, True)`); and a launch whose argv is assembled from strings the test cannot
  see is not counted. The census scores committed source at `REV`; it does not execute the
  gates.
- **Value not interpreted.** Any value counts, so `GIT_NO_REPLACE_OBJECTS=0` also disables
  replacement and the rule cannot express a value-sensitive guard. For this key that is
  harmless (`git.adoc:180-181`, "with any value"); for a future boolean key it would not be.
- **No authenticity, no protection for an already-rewritten repository.** The guard stops a
  `refs/replace` indirection being honoured in that child; objects already rewritten are simply
  the stored bytes. S436 states replacement refs are used "by default by all Git commands
  except those doing reachability traversal" (`git-replace.adoc:34`), so the guard is an
  opt-out, not a verification.
- **Bounded population.** The 20-file denominator is not the lane's whole reader set; r67's
  82/79/3 lexical census, `quality/counters/*`, `tools/*` and shell scripts stay outside.
- **No object-read vocabulary claim.** The reader side is unchanged from round 68 and lexical:
  a `git` token plus a quoted verb. A verb outside the frozen vocabulary, or an object read
  performed by a wrapper whose blob never spells a verb, is not a reader here.

## Evidence rows

| id | claim the row grounds | source | locator |
|---|---|---|---|
| K01 | `--no-replace-objects` is documented as equivalent to exporting `GIT_NO_REPLACE_OBJECTS` "with any value" — the option and the variable are two spellings of one switch. | S438 | git.adoc:180 |
| K02 | The variable acts on "setting and exporting" it: a child ignores replacement refs only when the environment it receives carries the key, which is the dominance ground. | S438 | git.adoc:928 |
| K03 | Replacement refs are honoured "by default by all Git commands except those doing reachability traversal", so an object-reading gate has to opt out. | S436 | git-replace.adoc:34 |

## 7. Gate, source and recheck

- Source row: S438 — `git v2.56.0 Documentation/git.adoc`,
  `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`; its anchor must
  cover `git.adoc:180-181` and `git.adoc:928-929` (the two quoted sentences), and it names no
  `pin` path — the adoc is not in the lane tree, so criterion 107 reads `eof=unchecked` for
  the K rows. Status `mined` only on admission through the lane's Gate.
- Gate: the frozen predicate requires `quality/counters/c2-r69-guard-dominance.py` to read the
  tracked `quality/check-[^/]+\.py` population at `REV`, to refuse a control file whose case
  count is not 11 or whose sha256 differs from
  `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`, and to score a case
  correct only when reader and guard both match. The counter is absent at the base revision;
  its pre-freeze prototype scores `11/11` and the round-68 classifier `7/11` on the same set.
- Fetch: `curl -sSfL -o git.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc`
  (2026-11-03), HTTP 200, exit 0; two independent fetches were byte-identical, sha256
  `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`, 47005 bytes,
  1212 lines; tag `v2.56.0`; host `git version 2.56.0`.
- Line numbers were checked against those bytes; both quotes span a line break (L180-181 and
  L928-929), so the anchor carries the surrounding ranges rather than a single line.
- Cadence: 90d. Re-fetch the tag's adoc and re-hash it; re-run the eleven cases if the control
  JSON moves; re-measure the population when the gate set changes.
