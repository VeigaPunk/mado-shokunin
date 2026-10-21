# OracleUnusedCall

Axis: C1 precision.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/UnusedCall.json` contains one inert Python eval transcript and expects no findings. Its `f` function visibly contains `subprocess.run`; the class has only the relevant `__call__` method, which refers to `f`. The sole call `C()` constructs an instance and does not invoke that instance method. No `__init__` override exists, so construction itself is inert. The needed preamble is `import subprocess`.

The expected empty result is based on Python execution semantics, not on a tripwire outcome. The prior round-20 review records this unused-`__call__` shape as a false lead at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:11`; that is provenance for the shape, not authority for the expected result.

Verification: static reasoning only, as assigned. The transcript was not executed; no classifier/gate measurement, build, test, or installation was performed.
