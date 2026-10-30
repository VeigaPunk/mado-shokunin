# R56W3ExecHoldoutReseal

## Attack / implementation

Attack: C2 hold-out integrity and the w2 revealed-table lookup route. Added round-57 candidate `quality/r56_ctl_c2_reseal.py` only under this seat's deliverable directory. It accepts the caller's sealed hold-out directory and build-time digest, checks the digest before execution, exports the supplied tool into its isolated work directory, stores fixture expectations in process memory, and runs each fixture with only its copied `tree/`, an empty working directory, and the exported tool. Output is marked `MADO_R56_C2_RESEAL`.

The commitment implementation follows the frozen harness precisely: sorted relative paths encoded as bytes, NUL, `f`/`l`, NUL, SHA-256 of file bytes/link text, newline. The type marker is part of frozen `quality/r56_ctl_c2.py:85-108` and required to reproduce the frozen tables value; it is not omitted despite the abbreviated formula in the seat description.

## Evidence

Exact command outcomes are retained in `reseal-a2.txt`. Commands were run with `python3 -I`; the baseline harness was run with `--no-sandbox` because this prototype does not itself sandbox the underlying fixture process. The existing harness reported sandbox=bwrap in stderr for baseline, while its invocation included `--no-sandbox` for these local runs (no claim is made here about adversarial sandbox isolation).

- Frozen harness at revision `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` with the revealed hold-out: `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`.
- Candidate on good tool, with frozen sealed digest `65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183`: `fixtures=18/18 holdout=8/8 holdout_commit=ok verdict=TARGET_MET`.
Exact invocation forms (paths are the scratch variables used at execution):
```sh
python3 -I "$D/quality/r56_ctl_c2.py" --repo "$R" --rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --work "$S/frozen-work" --holdout "$S/holdout" --no-sandbox
python3 -I "$A" --tool "$D/tools/mado-watchplan.py" --committed "$D/.ufo/waves/round-56/fixtures/c2" --holdout "$S/holdout" --sealed-sha256 65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183 --work "$S/reseal-good"
python3 -I "$A" --tool "$S/mutant.py" --committed "$D/.ufo/waves/round-56/fixtures/c2" --holdout "$S/holdout" --sealed-sha256 65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183 --work "$S/reseal-mutant"
python3 -I "$A" --tool "$A_TOOL" --committed "$D/.ufo/waves/round-56/fixtures/c2" --holdout "$S/tampered" --sealed-sha256 65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183 --work "$S/reseal-tampered"
python3 -I "$D/quality/r56_ctl_c2.py" --repo "$D" --rev HEAD --work "$S/frozen-mut-work" --holdout "$S/holdout" --no-sandbox
```
`$A_TOOL` is the unmodified archived tool at `$D/tools/mado-watchplan.py`. The four fixture-scoring calls returned the decisive lines shown in the receipt. bwrap was present; `--no-sandbox` only makes the old harness tolerate absence of bwrap, and stderr identified its actual mode as `sandbox=bwrap`.

Exact evidence text: `reseal-a2.txt`. The frozen baseline stderr also recorded `control_scores={'const-host': (1, 0), 'empty': (0, 0), 'sibling-reader': (0, 0), 'lookup-committed': (18, 0)}`.

- `.ufo/waves/round-56/w3/R56W3ExecHoldoutReseal/quality/r56_ctl_c2_reseal.py`
- `.ufo/waves/round-56/w3/R56W3ExecHoldoutReseal/reseal-a2.txt`

## Defects / severity

No defect demonstrated in the candidate by these runs. Evidence shows the selected mutation is detected and scored identically to the frozen harness, and a hold-out byte change is rejected. This prototype does not implement the frozen harness's four independent control programs; it is a scorer/seal prototype, so it does not establish control coverage. That is a limitation of the candidate evidence, not a claim failure.

## Not verified / risks

- Not run inside bwrap by this prototype; the frozen harness baseline was run as explicitly recorded with `--no-sandbox`. No claim of containment against absolute-path reads is made.
- Only the named single operator swap was compared; no broader mutation set was attempted.
- No tests, lint, build, or formatter were run, as required for this wave.
- No tooling was installed or updated.