# CriticC1Predicate — falsification of C1's frozen predicate/counter (round 32)

Seat: critic (report only). Scope: C1 only (`registration.md:16-65`). The sibling
seat report `w1/reports/ExecThemeHoldCheck.md` did **not exist** at attack time —
its log read "Working..." — so the theme-not-held question is re-derived here
from the live corpus, not inherited.

Method: four scratch trees under
`.ufo/waves/round-32/c2/controls/c1-predicate-attack/` (the path named in this
seat's prompt; a subdir is used so K2's own `c2/controls/` receipt seat is not
collided with). Each tree is a minimal lane-root replica — `corpus/SOURCES.md`
plus the three `corpus/knowledge/` entry paths — and the frozen counter body
runs verbatim, `cd`-ed into the scratch root (the counter is pure relative
paths, so `cd` is the only substitution). Lane tree untouched.

**Frozen counter** (registration.md:47-55), as executed:

```sh
e = number of A,B,C that are regular files        # [ -f ]
r = grep -cE '^\|[[:space:]]*S(186|187|188|189|196)[[:space:]]*\|' corpus/SOURCES.md
c = grep -cE '^source:.*S(186|187|188|189|196)' A B C | awk sum of 2nd colon-field
```

**Baseline — counter is live at base** (none of the claimed files/rows exist at
HEAD `9186234`):

```
$ cd <lane root> && <verbatim counter>
entries=0 rows=0 cited_entries=0
```

## Attack 1 — do-nothing can't, junk CAN: the target is reachable while the lane holds nothing real

Four trees, all scored by the verbatim counter:

| Variant | Construction | Counter output |
|---|---|---|
| v1-shape-junk | Five 11-col stub rows `S186…S196`, payload cells `junk/nothing/nowhere`, `used-by` → `corpus/knowledge/does-not-exist.md` (absent, verified); three entries = one line `source: S<n>`, **13 bytes each, zero knowledge** | `entries=3 rows=5 cited_entries=3` — **TARGET MET** |
| v2-degenerate | `SOURCES.md` = five copies of `| S186 \|` (1-cell lines, one id duplicated ×5, four ids absent); A = three `source: S186` lines, B and C **empty** | `entries=3 rows=5 cited_entries=3` — **TARGET MET** |
| v3-extra-ids | Correct five rows + entries citing extra unregistered ids `S998`, `S999` | `entries=3 rows=5 cited_entries=3` — **TARGET MET** |
| v4-realistic-overcount | Realistic entries, all five ids cited per the claim's mapping — but A splits provenance across **two** `source:` lines | `entries=3 rows=5 cited_entries=4` — **FALSE NEGATIVE** |

Ground truth vs. counter (the trees' actual contents):

```
v1: distinct registry ids: S186 S187 S188 S189 S196; cited ids: S186 S188 S196; used-by target: ABSENT
v2: distinct registry ids: S186;                     cited ids: S186        ← 1 real id total
v3: cited ids: S186 S187 S188 S189 S196 S998 S999                            ← extras invisible
v4: cited ids: all five, correctly mapped — fails on provenance line count
```

Answers to the seat's probes: **an empty/stub entry whose `source:` line merely
names an id counts** (v1: `source: S186` is the entire file). **Rows whose
`used-by` names a nonexistent file count** (v1: `ls does-not-exist.md` → No such
file or directory). **Even non-rows count** (v2: `| S186 |` repeated five times
satisfies `rows=5` with one id).

Sharpened micro-flaws, measured:

- `grep -c` counts **matching lines, not distinct ids and not files**: the claim's
  per-entry citation mapping (`A→{S186,S187,S189}`, `B→S188`, `C→S196`) is
  unenforced (v2/v3); a 2-line provenance header **over**counts (v4, honest work
  rejected on formatting).
- Row regex requires only `| <id> |` at line start: `| S186 |` is a match; cell
  count, `status`, `recheck`, `used-by` are never read.
- `source:` regex has no id boundary: `source: S1866 S1960` → `1` (verified),
  so a citation of unregistered `S1866` scores toward `cited_entries`.
- `^source:` matches inside fenced code blocks: ` ```\nsource: S186\n``` ` → `1`
  (verified); quoted text counts as a citation.
- `[ -f ]` accepts any regular file, including empty (v2's B, C are 0 bytes).

**The K1 "do-nothing controls" claimed in registration.md:61-65 answer a
different question.** They prove no *one-sided* commit reaches the target. They
do not test a *two-sided junk* commit — which reaches it in ~10 lines, shown
above. The advertised controls are satisfied by the attack they were meant to
exclude.

## Attack 2 — one theme or two? TWO topics under an IPC title

Fetched payload identities (`.ufo/waves/round-32/fetch/`, opened this round):

```
S186.bin  Hyprland wiki "IPC"        — two UNIX sockets (.socket.sock/.socket2.sock), HIS
S187.bin  wiki IPC page @0.56.0 (HTML)                                    [same surface, pinned]
S188.bin  Hyprland Lua docs "Dispatchers" — "Dispatchers return tables that describe an
          action… Their purpose is to be fed into hl.bind() or hl.dispatch()… Simply writing
          hl.dsp.whatever() on its own will do nothing."
S189.bin  EventManager.cpp (C source) — socket2 event pump
S196.bin  wiki "Dispatchers" @0.56.0 (HTML) — the dispatcher COMMAND surface
```

Claim title: "the Hyprland IPC **two-socket contract**". Subjects: A+S186/187/189
= IPC transport (sockets, grammar, framing); C+S196 = dispatcher command
surface over that socket — arguably the same machine-facing plane. **B+S188 is a
different subject**: the *Lua* `hl.dsp.*` deferred-action API ("describe, they do
not act") — a scripting-layer semantic sharing only the word "dispatcher". Two
topics (IPC/socket layer; dispatcher APIs) are fused under a socket-contract
title. Worse, the claim's framing makes it cheap to confuse `hl.dispatch()`
(Lua) with `hyprctl dispatch` (IPC) — the exact ambiguity the corpus needs
disambiguated.

The counter is indifferent — `[ -f ]` never reads contents — so this defect is
purely in the claim's text, not caught by the predicate. Note `keybind-rule-semantics.md`
already holds a 24-dispatcher inventory (`§3`, `[INF-docs]`, "no dispatcher was
fired") — the dispatcher side of this bundle is NOT as uncovered as the title
implies; the genuinely unheld half is the wire contract (socket paths appear in
`hyprctl-verification-layer.md:30` only as a directory listing).

## Attack 3 — the five ids are NOT enumerated as a set

The counter never computes the cited-id set:

- **Completeness unchecked**: nothing forces all five ids to be cited. v2 cites
  only `S186`; `cited_entries=3` anyway.
- **Exclusivity unchecked**: extra cited ids are invisible (v3: `S998`, `S999`
  ride free). The regex has no complement test and no word boundary (`S1866`
  matches).
- **Row completeness unchecked**: `rows` counts lines, not distinct ids (v2: 5
  copies of `| S186 |`).
- **Reciprocity unchecked**: `used-by` is never inspected — dangling `used-by`
  passes (v1), and a `source:` line in a code fence counts.

So the counter does not enumerate the claimed set in either direction: cited ⊆
claimed and claimed ⊆ cited are both unmeasured.

## Attack 4 — reachable without the claimed work? YES, and the lane's own census knows it

v1b: real `corpus/SOURCES.md` + five appended 11-col stub rows + the three stub
entries → counter `entries=3 rows=5 cited_entries=3`. Same file under the lane's
census validator:

```
$ bash scripts/sources-census.sh validate --file v1b/.../SOURCES.md; echo exit=$?
file E12 S186 row outside Registry section … exit=1   (appended below section end)
$ bash scripts/sources-census.sh validate --file v2b/.../SOURCES.md; echo exit=$?
file E01 S186 fields=1 … exit=1                        (1-cell "rows")
```

The frozen counter accepts what the committed schema validator rejects: the
predicate operates **below the schema floor** the claim text itself invokes
("normalized to the census 11-column schema"). Only the registration's process
gates (item 4: validate-before-append) stand between junk and the registry —
i.e. honesty, not the kill rule. And the validator's `used-by` handling never
checks target existence (dangling `used-by` unflagged even at E-level; verified:
`does-not-exist` absent from all validator output).

## Verdict: **CLAIM DEAD** (predicate dead, not necessarily the data)

The frozen counter certifies *line-shape*: three existing paths, five matching
lines, three matching lines. Every semantic the claim text asserts — real
entries, five *distinct* registry rows, the per-entry citation map, `used-by`
reciprocity, the 11-column schema, "re-grounded this round" — is carried by
prose and process gates, zero predicate weight. Under the stated kill rule
("met iff the counter prints exactly that triple"), a ~25-line junk commit is a
pass. The round-30 precedent (CritPredicates: all three predicates cheatable;
claims stood on data + review) says this is survivable *if* the wave's
non-author review re-derives the data — but the frozen instrument itself is
falsified.

**Minimal predicate repairs that would have held at freeze time** (informational
only — the target may NOT be narrowed after data):

1. `rows` → count **distinct** ids, e.g. extract field-1 of 11-field rows in the
   `## Registry` section, `sort -u`, intersect with `{S186,S187,S188,S189,S196}`,
   require size 5. Kills v1b/v2.
2. `cited_entries` → per-file existence: `grep -qE '^source:.*\bS(…)\b' file` per
   file (or require each file's own claimed id set); word-boundary the ids.
   Kills v2 (all-in-one-file), v4's false negative, and `S1866`.
3. Cited-set equality: `grep -hoE 'S[0-9]+' A B C | sort -u` must equal the
   frozen five — kills extra ids (v3) and missing ids (v2) in one check.
4. `used-by` reciprocity: for each of the five rows, `used-by` cell must name a
   path in `{A,B,C}` that exists. Cheap field-11 grep.
5. Substance floor: each entry ≥ N bytes and containing `[OBS]`/`[INF]` markers
   the QUALITY bar already requires; excludes empty files and code-fence-only
   `source:` lines.

Even all five leave "re-grounded by opening the source" unverifiable by shape —
a row-anchor/quote-match against the pinned fetch bytes (`.ufo/waves/round-32/fetch/S<n>.bin`)
would close that, but that is a different instrument class than a grep counter.

Environment: stock bash 5.3 + GNU grep/awk; no installs. Scratch receipts:
`.ufo/waves/round-32/c2/controls/c1-predicate-attack/{v1,v2,v3,v4,v1b,v2b}*`.
Lane mutations: this report + the scratch dir only.
