# OracleSaveFunction — scoped advisory finding

## Axis and finding

- **Axis:** C1 precision (operability residual repair).
- **Severity:** No actionable finding; the requested negative expectation is semantically sound.

The proposal at `.ufo/waves/round-21/w1/oracles/SaveFunction.json` contains one inert eval transcript, `saved = f`, where `f` visibly wraps `subprocess.run(["pacman", "-Q", "hyprland"])`, and expects no findings. Static semantics: `def f` creates a function object without executing its body; `saved = f` is a plain name load and store — it neither invokes `f` nor hands it to an invocation-capable sink or callback. The `subprocess.run` statement stays deferred and unreachable during module execution, so the transcript is a pure-data negative that must stay clean. The only preamble required is `import subprocess`, which keeps the potential spawning call visible.

Provenance is exact, not merely analogous: the independent round-20 precision review lists `saved = f` by name as fixture line 8 of its 18 value-only-reference false leads at `a8960de` — `lead` rows emitted while `28c6837` was clean and the function body was never called (`CriticPrecisionV3.md:5-13`, "Treat metadata/value-only uses ... as non-sinks"). The same review's pure-builtin analysis records that passing a function to a non-callback builtin must not sweep its body (`ReviewV3Diff.md:46-57`); a bare assignment is the weaker, store-only member of that same non-sink family.

The requested `C` is unnecessary for this exact `saved = f` case; no class is defined, hence no unused methods beyond the case and no constructor that could itself spawn — the constraint is satisfied vacuously, and introducing `C` would add an unrelated construction path. This negative is adjacent to but distinct from `NeverReferenced.json`: that fixture leaves `f` with zero references, while this one gives `f` exactly one reference that is a store. Together they separate "never referenced" from "referenced but never invoked", which is the precision boundary round-20 falsified. The negative was checked against Python semantics and found correct, so it is proposed rather than rejected.

## Residual risk and verification gaps

This judgment is static only, as required. The transcript and the tripwire were not executed; no scanner outcome, measurement, or lead classification is claimed. The rationale covers this exact ordinary-function store; an environment where module execution could invoke `f` implicitly (none exists in this snippet) is out of scope. `import subprocess` is treated as inert preamble, consistent with every sibling fixture in this wave.

No tools were installed or updated.
