# CritHeldOut — read-only sealed-row review

## Scope and method

Axes: semantic non-equivalence, witness provenance, benign preservation, independence from W, and behavioural detectability without subject pinning.

Read registration first. Reviewed the six sealed JSON files and their adjacent witness records in `/fast/scratch/hyaku/mado-r27/heldout/`; no sealed row, input, mutation text, or individual witness result is reproduced here.

Performed in-memory JSON, SHA-256, replacement-site, compile and AST checks against the three registered subjects at `2fdca5ca`. Compared edited bytes and ASTs against pristine subjects, all 15 W edits, and the other sealed rows. Traced affected branches and operand types rather than treating AST differences as proof of brokenness. Audited recorded phase commands, source hashes, process statuses and contract-bearing output independently of the self-SHA header. For benign evidence, compared full recorded stdout with only the single self-SHA token removed; no path, ordering, whitespace or whole-header normalization was used. Distinguished complete printed outputs from equality attestations.

This was an evidence/static-semantics review, not a fresh execution of any subject, witness runner, gate, counter or compositor. No gate score or canonical admission is asserted. Behavioural duplicate and pinning-only verdicts are review inferences, not exhaustive formal-equivalence proofs.

Pinned-source reads used this exact argv pattern, once for each registered subject:

```text
env -i PATH=/usr/bin HOME=/home/vgpnk GIT_OPTIONAL_LOCKS=0 timeout 30 prlimit --as=4000000000 --core=0 -- git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2fdca5ca:SUBJECT
```

`SUBJECT` was `.ufo/waves/round-26/c1/count-v2.py`, `.ufo/waves/round-26/c2/count.py`, or `.ufo/waves/round-26/quality/check-population.py`. All three reads exited 0 and matched the working-tree bytes. All six sealed-file hashes matched the committed manifest.

Before and after command:

```text
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Captured stdout was counted in memory for `/usr/bin/Hyprland`: before 1338, after 1338, delta 0; command exits 0/0. Every started process finished and was reaped. No input files, lane code, or git/jj state were modified. No tools were installed or updated. The only write is this requested report.

## Counterexample, impact and correction

No falsifying counterexample was sustained. No reviewed row needs a semantic correction on the available evidence. The impacted-axis verdict is unchanged on all five review axes. Finite, recorded witnesses do not establish general fault coverage or predict the fresh gate result; that limitation must not be promoted into a stronger claim.

## Final summary — per-file counts and verdicts only

W duplicates below count replacement-triple, edited-byte, AST, and reviewed behavioural duplicates; all four counts are zero for every file. Beyond-SHA changes concern benign rows only. Evidence counts are audits of existing records, not new executions.

| File | Sound | Unsound | Evidence count / verdict | Beyond-SHA changes | W duplicates | Pinning-only mutants | Verdict |
|---|---:|---:|---|---:|---:|---:|---|
| HeldC1v2.json | 6 | 0 | 6/6 witness triplets show behavioural differences | — | 0 | 0 | SOUND; non-equivalent |
| HeldC2.json | 6 | 0 | 6/6 witness triplets show behavioural differences | — | 0 | 0 | SOUND; non-equivalent |
| HeldChk.json | 6 | 0 | 6/6 witness triplets show behavioural differences | — | 0 | 0 | SOUND; non-equivalent |
| HeldC1v2-benign.json | 3 | 0 | 18/18 full-output comparison pairs agree; 18/18 restorations agree | 0 | 0 | — | SOUND; preserving modulo self-SHA |
| HeldC2-benign.json | 3 | 0 | 18/18 full-output comparison pairs agree; 18/18 restorations agree | 0 | 0 | — | SOUND; preserving modulo self-SHA |
| HeldChk-benign.json | 3 | 0 | 18/18 preservation attestations; 6/6 printed baseline digests match; 3/3 static identities sound | 0 | 0 | — | SOUND; preserving; edited outputs attested, not separately printed |
