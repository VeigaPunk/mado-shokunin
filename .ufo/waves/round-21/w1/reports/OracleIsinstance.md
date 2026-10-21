# Isinstance oracle proposal

Axis: C1 precision.

Proposal: `.ufo/waves/round-21/w1/oracles/Isinstance.json` contains one Python transcript for `isinstance(object(), C)` and expects no findings. It imports `subprocess`; `f` visibly calls `subprocess.run`, and the only reference to `f` is in `C.__instancecheck__`.

Static basis: `isinstance` consults the metaclass of its second argument. Here `C` has the default metaclass `type`, so its ordinary class-body `__instancecheck__` method is not the hook used by `isinstance`. The expression neither instantiates `C` nor invokes that unused method; thus it cannot reach `f` or its deferred subprocess body. No constructor is defined. The empty expectation is semantically sound and is not based on executing the fixture or a detector result.

The round-20 independent precision review records this exact shape among its false leads (`.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:10-13`). Python references are included in the proposal's `source` field. This report is advisory and separate from the one-fixture JSON proposal.

Verification: static reasoning only; no transcript execution, tripwire run, tests, installs, or production changes.
