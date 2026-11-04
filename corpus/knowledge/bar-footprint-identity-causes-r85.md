source: S486 — https://www.rfc-editor.org/rfc/rfc8259.txt section 4 (pinned `.ufo/waves/round-84/fetch/rfc8259.txt:322`, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`); the lane's own frozen controls `.ufo/waves/round-85/controls/c1-cases-r85.json` (sha256 `bacae37d29d06e4f9d623262c05f2975bcba338e650dbd38cbbd4039ca6216a1`, 72 cases) and `.ufo/waves/round-84/controls/c1-cases-r84.json` (sha256 `5c9ce3891e1ec4be1820d229bbcfddfa5b61cfbd0d02cc93252ac38c6dd9e883`, 61 carried); the declaration `.ufo/waves/round-85/claims-declaration-r85.md` (sha256 `71d3bfa8d92277002c609437fd57531f75c661637266492662e49ce242bc8d54`); the instrument `tools/mado-barfoot.py` and `quality/counters/c1-r85-identity-causes.py` (sha256 `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`)
verified-at: 2026-11-04; instrument freeze `3905311c75a39c5710413105865c0a1a7dd0116a`; tool bytes `tools/mado-barfoot.py` sha256 `d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12` (88,106 B) at that revision
recheck: python3 -I quality/counters/c1-r85-identity-causes.py --repo . --rev REV --base-rev 5f174ca48d4f9cf94abf1a8c58b7d6f88733aced --controls .ufo/waves/round-85/controls/c1-cases-r85.json --carried .ufo/waves/round-84/controls/c1-cases-r84.json --scratch-root DIR

# Ten declaration-identity refusal causes, each naming the defect it found

A refusal that names its own cause is a different artifact from a refusal that only says
"refused". At the freeze revision `tools/mado-barfoot.py` prints every identity refusal as
`MADO_BARFOOT: ERROR (stage=setup cause=<token> …)` or `(stage=model cause=<token> …)`: the
token is attached to the exception (`tools/mado-barfoot.py:144-160`), rendered by `cause_tag`
(`:1667-1670`), and printed at the two handlers (`:1719` model, `:1722` setup). A site that
declares no cause prints no token (`cause_tag` returns the empty string for it), so the token
vocabulary below is exactly the set of identity defects the tool names.

Round 84 bound only the refusal *stage*, so a tool that refused the right stage for the wrong
reason scored. Round 85 binds the cause token too. Ten tokens, one per declaration defect
class:

| cause | stage | raised at (freeze rev) | what the refusal prevents | frozen witness |
|---|---|---|---|---|
| `alloc-duplicate-key` | setup | `:456-457` (in `allocation_pairs`, `:450-459`; the pairs hook reaches JSON decoding through `:236` and `:467`) | a repeated allocation key silently selecting one of two declared bands for the same namespace | `alloc-dup-key-equal` (`:3955`), `alloc-dup-key-interleaved` (`:4018`) |
| `alloc-not-object` | setup | `:469-470` | reading a band out of a declaration that is not a namespace→band map | `alloc-not-object` (`:4081`) |
| `alloc-empty-namespace` | setup | `:474-475` | a band keyed to `""`, which no surface can own | `alloc-empty-namespace` (`:4187`) |
| `alloc-non-integer` | setup | `:477-478` | a band that is not an integer (a JSON boolean is refused too) | `alloc-non-integer` (`:4133`) |
| `alloc-negative` | setup | `:480` | a negative band, which has no extent | `alloc-negative-refused` (carried; stage only) |
| `alloc-unknown-namespace` | setup | `:823-825` (composition path) and `:1021-1023` (single-surface path) — two sites, one token, different messages | an allocation entry that names no declared surface, silently unused | `alloc-unknown-case-variant` (`:4239`) |
| `namespace-duplicate-bar` | setup | `:807-808` | an extra surface taking the bar's own name, so one name would carry the bar's band and a second surface's | `ns-dup-bar` (`:4293`) |
| `namespace-duplicate-surface` | setup | `:814-816` | two extras at one level sharing a name | `ns-dup-surface` (`:4351`) |
| `namespace-duplicate-cross-level` | setup | `:810-813` | two extras at different levels sharing a name | `ns-dup-cross-level` (`:4425`) |
| `live-duplicate-surface` | model | `:1007-1008` (in `find_layer`, `:998-1009`) | picking one of two live boxes that carry the declared namespace at the declared level | `live-dup-surface` (`:4572`) |

Witness line numbers are in `.ufo/waves/round-85/controls/c1-cases-r85.json` at the freeze
revision. Cause-bearing expectations require token presence somewhere in stdout alongside the
stage and status; they do not bind a unique cause on its own error record (`:306-317`).

One token of the ten, `alloc-negative`, has no cause-bound witness in the 72-case frozen set:
the carried case `alloc-negative-refused` (`.ufo/waves/round-85/controls/c1-cases-r85.json:2744-2757`)
pins only the stage and the exit code, and the ten identity witnesses cover the other nine
tokens (`alloc-duplicate-key` twice). The token is nonetheless emitted by the tool and asserted
by the tool's own selftest (`tools/mado-barfoot.py:1635-1636`, part of the measured 152/152), so
the token exists in the frozen vocabulary; only the frozen population's cause clause does not
bind it. Measured consequence (`.ufo/waves/round-85/w1/R85ReviewerC1.md`): a tool that refuses
the negative band with `cause=alloc-not-object` instead of `cause=alloc-negative` scores
**72/72** on the frozen cases. That is a case score, not a full-gate pass — the change breaks
the negative-allocation mutant's literal anchor and the tool's own cause selftest, so the
declared 51-mutant clause still rejects it. The 72/72 case score alone therefore does not
certify all ten tokens.

## What each refusal keeps out of the join

The join is a keyed one: a declared surface is identified by its namespace, its band comes from
the allocation map under that same namespace, and the live box is looked up by namespace at a
level. Three places key on the namespace alone, so one name carrying two surfaces collapses
them rather than naming two things:

- the band lookup `allocation.get(spec["namespace"])` (`tools/mado-barfoot.py:492`) — one
  allocation entry would serve both surfaces;
- the attribution map `attribution[(spec["namespace"], edge)]` (`:919-920`) — the key carries
  no level, so two surfaces with one name sum into one attribution entry and one printed
  total;
- the live lookup `e.get("namespace") == namespace` (`:1005`) — one of two live boxes would be
  chosen without a reason.

`namespace-duplicate-surface`, `namespace-duplicate-cross-level` and `namespace-duplicate-bar`
are the three shapes of that collapse, told apart by the level test at `:809` and the bar
special case at `:806`. The allocation-side refusals remove the other half: a repeated
allocation key, an allocation that is not a map, an ownerless or non-integer or negative band,
and an entry naming no surface. RFC 8259 section 4 says object names SHOULD be unique and
describes what receivers do when they are not — "Many implementations report the last
name/value pair only" (`.ufo/waves/round-84/fetch/rfc8259.txt:333-334`). S486 licenses the
refusal; it does not require one, and it is not a layer-shell namespace requirement
(`corpus/SOURCES.md:438`).

## Four separations the round-84 population could not see

- **Equal-valued versus interleaved.** `{"waybar":26,"waybar":26}` and
  `{"waybar":26,"panel":40,"waybar":40}` both carry `alloc-duplicate-key`. The refusal does
  not depend on the repeated value being equal and does not depend on the two keys being
  adjacent: the pairs hook sees every key of the object, so the equal-valued repeat is
  refused on the same terms as the interleaved one.
- **One level versus cross-level.** Two extras sharing a name at one level carry
  `namespace-duplicate-surface`; the same two extras at levels 3 and 2 carry
  `namespace-duplicate-cross-level`. The tokens differ because the defects differ: the
  cross-level pair is still one name for two surfaces, but the level comparison at `:809` is
  what separates the two causes.
- **Case-distinct names versus a case-variant key.** A declared surface named `Waybar` beside
  the bar named `waybar` is accepted as two surfaces (`ns-case-distinct-accepted`, `:4499`;
  measured `verdict=CLEAN`, band 66, attributed 66). An allocation key `Waybar` against a
  surface named `waybar` is refused `alloc-unknown-namespace`
  (`alloc-unknown-case-variant`, `:4239`). The join compares namespaces as exact strings in
  both directions — the duplicate test is a dict membership test on the raw name (`:804`) and
  the live lookup is `==` on the raw name (`:1005`) — so a case variant is a different name,
  never a resolution of another. The round-84 population could not see this because its
  reviewer admitted a casefold over-refusal and a level-qualified extra identity
  (`.ufo/waves/round-85/claims-declaration-r85.md`, C1 "Surface named, not the number").
- **The bar's name versus two extras.** An extra reusing the bar's namespace carries
  `namespace-duplicate-bar`, not `namespace-duplicate-surface`: the bar's band is resolved
  under its own name, so this is the one shape where the name belongs to a surface the caller
  did not declare as an extra.

## Measured at the freeze revision

Run at `3905311c75a39c5710413105865c0a1a7dd0116a` with the command in the `recheck:` line,
exit 0:

```
MADO_R85_IDENTITY: cases=72 correct=72 mutants=51 killed=51 base_correct=62/72
                   carried=61/61 tool_selftest=152/152 verdict=TARGET_MET
```

The no-work control is the held round-84 tool scored with this counter: it refuses the right
stages but prints no cause, and scores 62/72
(`.ufo/waves/round-85/receipts/control-c1-r85-base.txt`; base
`5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`, tool sha256 `72456666a31927dfc46f955f41b3aa57b2215a8fcd8dc736fc302d7b58830c7f`,
selftest 139/139 at base). Ten of the seventy-two cases are the identity witnesses that carry
`expect.cause`; the ten declared identity mutants each die on them
(`quality/counters/c1-r85-identity-causes.py:167-196`). Measured attribution of the failing
witnesses, replayed through the counter's own `run_cases`:

| mutant | score | failing witness(es) |
|---|---|---|
| `dup-key-equal-collapsed` | 71/72 | `alloc-dup-key-equal` |
| `dup-key-interleaved-collapsed` | 69/72 | `duplicate-allocation-keys`, `alloc-dup-key-equal`, `alloc-dup-key-interleaved` |
| `alloc-dup-cause-collapsed` | 70/72 | `alloc-dup-key-equal`, `alloc-dup-key-interleaved` |
| `cause-dropped` | 62/72 | all ten cause-bearing witnesses |
| `ns-dup-cause-collapsed` | 71/72 | `ns-dup-cross-level` |
| `ns-dup-level-blind` | 71/72 | `ns-dup-cross-level` |
| `ns-dup-surface-accepted` | 70/72 | `duplicate-extra-namespaces`, `ns-dup-surface` |
| `ns-case-folded` | 71/72 | `ns-case-distinct-accepted` |
| `alloc-case-folded` | 70/72 | `alloc-unknown-namespace`, `alloc-unknown-case-variant` |
| `live-dup-first` | 71/72 | `live-dup-surface` |

## Limits

- **This is the join's input grammar, not a layer-shell uniqueness law.** The rule is one
  name, one surface *for this instrument's declarations*. Nothing here states that a
  compositor forbids two surfaces from sharing a namespace, and nothing here lets a caller
  distinguish two real surfaces that do. S486 is a JSON member-name specification
  (`corpus/SOURCES.md:438`), not a layer-shell requirement.
- **The cause token is not a protocol error code.** It is this tool's own tag on its own
  error line; no protocol defines it, and nothing downstream should read it as one.
- **A right-stage wrong-cause refusal is caught only by the frozen population.** The cause
  clause is exercised by 10 of the 72 cases. The 61 carried cases declare no `expect.cause`,
  so at the right stage and exit code a refusal with the wrong cause is accepted there:
  measured against the counter's own predicate, all 14 carried error cases accept a synthetic
  refusal line carrying `cause=alloc-duplicate-key` whatever their real defect. A population
  that stopped carrying those ten witnesses would score a wrong-cause tool as correct.
- **The cause comparison is a space-delimited substring test over the whole stdout**, not one
  canonical error record with a unique cause token
  (`quality/counters/c1-r85-identity-causes.py:310-318`; the substring form is
  `(" cause=%s " % cause) not in stdout`). Measured: `cause=alloc-duplicate-key EXTRA` is
  accepted, `cause=alloc-duplicate-keyX` is refused, `cause=alloc-duplicate` is refused. A
  cause token that merely begins with a declared token is therefore not distinguished from
  it, and a refusal line carrying several cause tokens satisfies the check once. Measured
  (`.ufo/waves/round-85/w1/R85ReviewerC1.md`): a tool that floods every cause-bearing error
  line with all nine bound tokens plus `cause=wrong-reason` scores **72/72** cases with
  selftest 152/152 — but only 48 of the 51 declared mutants die, so the full gate still
  rejects it. The case score and the full gate are separate things here.
- **The case score is weaker than the full gate, in both directions.** Three independent
  scorer weakenings survive the 72-case score but are caught by the declared mutant clause
  (`.ufo/waves/round-85/w1/R85MutationTester.md`, measured on a frozen snapshot): a scorer
  matching `cause` as a bare substring, a scorer casefolding the cause comparison, and a
  scorer matching the stage as a prefix each still score 72/72. The same seat shows the
  mirror-image tool hole: a tool that stores the allocation key with its trailing space
  stripped (`out[name.rstrip()] = value`) also scores 72/72 on the frozen population, because
  no frozen witness carries a whitespace-aliased key. Neither result is a claim that the
  frozen predicate is false; both are claims about what the 72 cases do not discriminate.
- The cause vocabulary says nothing about the *live* side beyond
  `live-duplicate-surface`, and nothing about which of two live boxes is the true one.

## Unknown

- **Arbitrary duplicate handling.** RFC 8259 leaves receiver behaviour with duplicate names
  unpredictable (`.ufo/waves/round-84/fetch/rfc8259.txt:331-334`). This instrument chooses
  refusal; what another consumer of the same JSON does with the same bytes is not measured
  here and is not implied by this choice.
- **Protocol-level identity semantics.** Whether two live layer surfaces may legitimately
  share a namespace, and what the compositor then does with the two, is not established by
  any source in this note. The refusals above describe a join's input discipline; they are
  not a claim about the protocol or about any host.
