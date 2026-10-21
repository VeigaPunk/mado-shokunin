# OracleAnnotation

Axis: C1 precision.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/Annotation.json` contains one variable-annotation eval transcript and expects no findings. Its `f` body visibly calls `subprocess.run`; the module-level `annotation: f` evaluates the function object as an annotation value but does not invoke it. No process-spawning path is reached. `import subprocess` is the only needed preamble. No class `C` is relevant to this exact variable-annotation shape.

The round-20 review identifies this shape as a false lead at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:11` (case 6). That citation supports the counterexample shape, not the expected result; the empty expectation follows from Python semantics.

Verification: static reasoning only. Neither the transcript nor tripwire was executed; no classifier/gate measurement, build, test, or installation was performed.
