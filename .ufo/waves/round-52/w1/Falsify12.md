# Falsify12 — C1 counter isolation/scratch behavior

## Deliverables

- `.ufo/waves/round-52/w1/Falsify12.md`

## Scope

Axes: operability and coverage. Attacked frozen item C1, specifically the existing C1 counter's revision binding in its checker-result acceptance path. The frozen C1 target requires a counter run at the requested pinned revision and production/control discrimination (`claims-frozen.md:5-7`; `registration.md:7,13-15`). No claim or predicate edits.

## Finding — checker revision field is not bound to requested revision

Source evidence: `quality/counters/c1-r51-ledger.py:302-328` reads the checker's summary and requires a `TARGET_MET` verdict and exit 0; it checks selected numeric fields against the counter's independent measurement. It returns `ok` with `rev=%s` from the checker output at line 328, but does not compare that field with the requested `rev`. In contrast, the independent measurement and clone are pinned by `main` at lines 375-390. Thus checker-reported revision identity is informational, not an enforced binding.

**Attack / concrete failure mode:** a checker invocation can produce a clean `TARGET_MET` summary carrying a revision other than the requested revision while matching numeric fields; this wrapper accepts it as `checker ledger ok`. This is an attribution/isolation weakness in the checker leg, not proof that the base production ledger is mismeasured by the independent half. C1's newly required control-specific context checks may be performed by a new counter and could close it; this source finding alone does not establish that the future counter retains it.

**Reproducible setup/command:** source inspection only: `read quality/counters/c1-r51-ledger.py:302-328` and `:375-410`. Dynamic reproduction would require substituting/faking the checker response or executing the counter/checker, which this assignment's source-only rule forbids. Actual result: **not reproduced dynamically**; static acceptance-path weakness observed in source. No assertion that the round-52 counter has this weakness; it is absent at base per frozen claims.

## Axis effect, risks, and verification

- Operability: revision provenance of the checker leg is not independently enforced in this baseline wrapper.
- Coverage: the independent file-byte measurement remains pinned, so this does not invalidate that measured coverage; it weakens confidence that the checker leg evaluated the same snapshot.
- Risk/limitation: this is a round-51 counter observation, not a result about an unobserved round-52 implementation. The frozen C1 controls may be independently enforced in the new counter.
- Verification for owning lane: at the requested revision, ensure checker output's `rev` equals the resolved requested commit (and reject mismatch); exercise an otherwise-accepted mismatched-revision response in a contained fixture, then run production and the named generic-self-pointer control as frozen. This seat did not run counters.

## Evidence and limitations

- Local source: `quality/counters/c1-r51-ledger.py:302-328,375-410`; current checkout HEAD is the declared base `85d57a818c3707397e21c840b6498b105ba798aa` (read-only fact command).
- Frozen target/control: `.ufo/waves/round-52/claims-frozen.md:5-7`; `.ufo/waves/round-52/registration.md:7,13-15`.
- No external source candidates/URLs. No package queries, live reads, probes, producer execution, or source checkout writes. No installs. Scratch directory created at `/fast/scratch/hyaku/mado-r52/Falsify12/`; no counter clone or worktree was created.

## Report

- `.ufo/waves/round-52/w1/Falsify12.md`
