# ConnGateReuse — connector report (mado round 36, wave 1)

Seat: `L1Mado36.ConnGateReuse`. Assignment: assess whether
`quality/check-counter-discrimination.py` is reusable by sibling lanes as a
pattern; split lane-specific from generic parts; give the smallest
generalization and the interface a sibling would implement. Report only —
no edits. Lane HEAD `dbf8b57` (the freeze commit). All work read-only;
mutants were generated under `/tmp` (allowed scratch), gate run with
`--no-receipts` so the receipts dir was untouched.

## 0. Grounding run (evidence the gate behaves as its docstring claims)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
  python3 -I quality/check-counter-discrimination.py --profile r35 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --no-receipts --mutants /tmp/mado-r36-mutants-conngatereuse2
EXIT=1
MADO_DISCRIMINATION: profile=r35 instruments=c1,c2 controls=25 correct=14/25 \
  label='round-35 frozen counters (unmodified)' verdict=TARGET_MISSED
```

Byte-for-byte the same classification as the frozen before receipt
(`.ufo/waves/round-36/receipts/before-discrimination.txt`: `correct=14/25`,
same per-control `ok=` pattern). Exit 1 = TARGET_MISSED as documented
(`check-counter-discrimination.py:21`). The lazy generator produced all 8
mutant trees under `/tmp` before the first `c2` mutant control ran.

## 1. What the gate actually is

A 201-line orchestrator, not a checker: it holds **zero** predicate logic.
Everything it asserts is delegated to two *instruments* (the counters) whose
only observable is one token: `verdict=(TARGET_MET|TARGET_MISSED)`
(`VERDICT` regex, line 50). The gate contributes the *discipline*: a frozen
control manifest, expected-vs-observed classification, fail-closed ERROR
handling, per-control receipts, and a clause-attribution table. That is
precisely the reusable part — and it is small.

## 2. Lane-specific parts (must be replaced or parameterized)

| Element | Location | Why lane-specific |
|---|---|---|
| `PROFILES` dict | `check-counter-discrimination.py:33-47` | Hardcodes instruments `c1`,`c2`, their script paths (`quality/counters/*.py`, `.ufo/waves/round-35/c*/count.py`) and frozen-spec paths per profile name `r35`/`r36`. |
| Instrument dispatch | lines 132-158 | The loop special-cases `inst == "c1"` (argv `--root <tree> --frozen <spec>`) vs `else`/`c2` (argv `--repo <tree> --frozen <spec>`). A third instrument cannot be added without editing the dispatch; a sibling's instruments get mado's flag names. |
| `GENERATOR` path | line 49 | `.ufo/waves/round-36/c2/gen-mutants.py` — mado's clause-ledger/blob mutator, itself keyed to mado's `clauses.json`/`RevFrozenBlobs-*.md` ledgers (`gen-mutants.py:30-39`, builds at 75-144). |
| `--receipts` default | line 80 | `.ufo/waves/round-36/controls/receipts` — mado round-36 path baked into a default. |
| `GIT_DIR` pinning | line 96 | `env["GIT_DIR"] = repo/.git` unconditionally — assumes every lane is a git worktree. Harmless for git siblings, wrong for a non-git lane. |
| Manifest control kinds | manifest.json | `kind:"tree"` + `root`, `kind:"mutant"` + `mutation` are mado's fixture vocabulary; the gate hard-codes `control["root"]` (tree) and `control["id"]→mutants` lookup. |
| `mutation.txt` receipt annex | lines 186-189 | Appends the fixture's `mutation.txt` when present — mado's generator convention. |
| Banner/label | lines 54-56, 193-196 | `MADO_DISCRIMINATION`, profile `label` strings. Cosmetic but hardcoded. |
| Receipt header | line 179 | Requires `manifest["id"]` (crashes `KeyError` on a manifest without `id` — unchecked field). |

## 3. Generic parts (carry verbatim)

| Element | Location | Reuse value |
|---|---|---|
| Manifest schema | `manifest.json` | `{id, frozen_at, note, controls:[{id, instrument, kind, expect, clause?}]}` — instrument name is already a free-form key; the schema itself is lane-agnostic. |
| Accept/reject classification loop | lines 125-169 | `ok = obs == expected`; count `correct`; TARGET_MET iff `correct == total`. The deliberate asymmetry (accept controls kill always-reject instruments, reject controls kill always-accept) is documented at lines 12-16 and is the *point* of the pattern. |
| Fail-closed `observed_of` | lines 68-72 | rc==2 → `ERROR`; missing verdict token → `ERROR`. `ERROR` can never equal an `expect` value (manifest only uses `TARGET_MET`/`TARGET_MISSED`), so crashes/timeouts/missing instruments always score `ok=0`. `run()` maps timeout to rc 124 → `ERROR` (lines 59-65). |
| Exit-code contract | lines 20-21, 197 | 0/1/2 = MET/MISSED/setup-error — the same convention every mado gate uses (`check-evidence-pointers.py:34` identical). |
| Per-control receipt format | lines 170-189 | `<control>.txt`: manifest id + profile header, expected/observed, the exact argv, full instrument output, exit code. Receipts are self-contained reproductions — directly reusable. |
| Clause-attribution table | lines 171-191 | `clause=<name> controls=N missed=M` — binds each load-bearing predicate clause to the controls that exercise it; generic over any `clause` string. |
| Profile indirection | lines 77, 33-47 | The *idea* (a profile names the instrument revision under test, so the gate scores instruments not claims) is generic; only its dict literal is lane-bound. |
| Env hygiene | lines 95-97 | `PYTHONDONTWRITEBYTECODE=1`, `sys.executable -I` isolation — portable to any Python instrument. |
| Lazy fixture generation | lines 106-123 | `ensure_mutants()` runs the generator once, on first need, and parses `mutant=<id> dir=<dir>` lines — a clean producer contract a sibling generator can satisfy. |

## 4. Smallest generalization

The gate is one indirection away from being lane-generic. **Replace the
`PROFILES` literal and the two-arm dispatch with a profile file**: a JSON
document (sit it next to the manifest, or embed as `manifest["instruments"]`)
mapping instrument name → invocation template:

```json
"profiles": {
  "r36": {
    "label": "round-36 repaired counters",
    "instruments": {
      "c1": {"argv": ["{py}", "-I", "{script}", "--root", "{target}", "--frozen", "{frozen}"],
             "script": "quality/counters/c1-idle-lock.py",
             "frozen": ".ufo/waves/round-36/c1/frozen.json"},
      "c2": {"argv": ["{py}", "-I", "{script}", "--repo",  "{target}", "--frozen", "{frozen}"],
             "script": "quality/counters/c2-ledger.py",
             "frozen": ".ufo/waves/round-36/c2/frozen.json"}
    }
  }
}
```

- `{target}` = the control's tree root (manifest `root`) or the generated
  mutant dir; `{frozen}`/`{script}` resolved against `--repo`; `{py}` =
  `sys.executable`. This removes the `if inst == "c1"` arm entirely and makes
  the instrument set open-ended — a sibling with **one** instrument works with
  a one-entry map.
- `GENERATOR` becomes an optional per-manifest key
  (`"fixture_generator": {"argv": [...], "emits": "mutant=<id> dir=<dir>"}`);
  a lane whose controls are all `kind:"tree"` never needs one.
- `GIT_DIR` pinning moves into the instrument env config or becomes
  conditional on `repo/.git` existing.
- Estimated delta: ~30 lines removed (PROFILES + both dispatch arms), ~25
  added (template expansion). Everything in §3 survives untouched.

Cheaper still (and acceptable): the file is 201 lines and the load-bearing
value is the **contract**, not the bytes — a sibling can copy the file and
edit PROFILES + the two argv lists (~15 edited lines). Recommend the JSON
profile anyway: it keeps `instrument` a manifest-declared name rather than a
code literal, which is what makes the manifest portable.

## 5. The interface a sibling lane implements

Per instrument:

1. An executable invoked as `<argv template>` against a target tree and a
   frozen spec file.
2. Output contract: exactly one line containing `verdict=TARGET_MET` or
   `verdict=TARGET_MISSED` (stdout or stderr; gate merges both).
3. Exit discipline: 0=MET, 1=MISSED, **2=setup error** — rc 2 is the
   ERROR path; an instrument that dies on a control must exit 2, not 1, or
   it scores a false MISSED.
4. A frozen spec JSON the instrument pins itself against (mado's
   `PRED-C1-r36-v1`/`PRED-C2-r36-v1` pattern — predicate text frozen before
   data).

Per lane:

5. A control manifest: ≥1 `expect:TARGET_MET` control and ≥1
   `expect:TARGET_MISSED` control per instrument, each reject differing from
   an accept in exactly one committed input; `clause` tags binding rejects
   to the frozen predicate's clauses.
6. Tree controls supply `root` (live repo = `"."`); optional fixture controls
   need a generator emitting `mutant=<id> dir=<dir>` lines — nothing else in
   the gate cares how mutants are built.
7. Optional: receipt annex convention `mutation.txt` inside the fixture dir.

## 6. Affected axes

- **C1 calibration (primary):** the manifest+profile machinery is *the*
  discrimination instrument — 3 accept / 22 reject, one-input mutants, ERROR
  never `ok`. Reuse preserves the axis: a sibling inherits a falsifier that
  cannot be passed by an always-accept, always-reject, or crashing counter.
- **C2 operability:** per-control receipts (argv + output + exit + fixture
  annex) are the evidence-pointer-friendly artifact shape; the clause table
  gives the audit surface.
- **No harm:** the proposal changes no committed bytes anywhere; it is a
  synthesis (generalize-by-config) that keeps every existing behavior —
  verified: the r35 run reproduced the frozen receipt exactly.

## 7. Risks / contradictions (stated, not smoothed)

- **Ordering hazard (real):** `ensure_mutants()` fires lazily at the first
  `kind:"mutant"` control, and mado's generator copies *this gate's own
  receipts* into fixtures (`gen-mutants.py` docstring at
  `check-counter-discrimination.py:107-110`: "a fixture copies the receipts
  its ledger names, and those receipts are this gate's own output"). The
  manifest happens to order all `c1` accept controls before `c2` mutants; a
  sibling that reorders controls — or generates eagerly — changes semantics
  silently. A generalization SHOULD document "mutant fixtures may depend on
  earlier controls' receipts; manifest order is load-bearing," or emit a
  warning when a mutant control precedes the controls its fixture copies.
- **`manifest["id"]` unchecked** (line 179): a manifest without `id` passes
  the `controls` check then dies `KeyError` mid-loop — partial receipts
  written, no verdict line. Minor; a generalized gate should validate the
  manifest schema up front (currently only `controls` non-empty is checked).
- **Regex contract is brittle by design**: any instrument output containing
  `verdict=` earlier than the real verdict line is parsed as the verdict
  (`re.search`, first match). Mado's instruments emit it once at the end; a
  sibling instrument that echoes its spec (which contains the word
  `verdict`) misclassifies. Contract should specify "verdict line must be
  the *last* verdict= token" or gate should use `findall()[-1]`.
- **Merge of stdout+stderr** (line 65): convenient, but means an instrument
  that logs `verdict=TARGET_MET` to stderr during a crash (rc≠0,≠2) still
  scores MET — the current `observed_of` only special-cases rc==2; rc 1 or
  124-with-output still reads the token. For mado's counters (which print
  verdict then `raise SystemExit(0|1)`) rc==1+MET cannot occur, but the gate
  does not *enforce* verdict/exit coherence (rc 0 + `TARGET_MISSED` scores
  MISSED — arguably correct; rc 1 + `TARGET_MET` also scores MET — a
  lie-positive). Worth one line in the contract: "verdict token and exit
  code must agree; gate MAY treat disagreement as ERROR."
- **Two verbatim labels** (`MADO_DISCRIMINATION`, `GEN-MUTANTS`) leak lane
  identity into a would-be shared tool — cosmetic.

## 8. Verdict

**Reusable as a pattern; reusable as code after one small lift.** The core
(manifest schema, expected-vs-observed classification, fail-closed ERROR,
receipts, clause table, exit contract) is already lane-agnostic — roughly
140 of 201 lines. The lane-bound residue is one config literal (`PROFILES`),
one generator path, one receipts default, and a two-arm dispatch that a
`{target}`/`{frozen}` argv template collapses. Smallest correct move:
profile JSON + argv templates + conditional `GIT_DIR`; a sibling then ships
only instruments, frozen specs, and a manifest — no gate code at all.

No tools installed this seat (python3 host binary sufficient; pacman
untouched per the pause). No writes outside this report and
`/tmp/mado-r36-mutants-conngatereuse{,2}`.
