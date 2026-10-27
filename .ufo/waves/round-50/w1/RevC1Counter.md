# RevC1Counter — counter review

## Result

The lane-tip clone run at `13631f24050f22db92bf5bd33e0f4d014192992e` passed: `fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`. Clause outputs included `t tool=present`, `s selftest rc=0 last='MADO_KEYSYM_SELFTEST: 38/38 passed' ok`, `s refusals=ok`, `f fixtures=633/633`, `g generated=150/150`, and `r trips=0`. The clone was created and top-level checked under `/fast/scratch/hyaku/mado-r50/RevC1Counter`; however, the work directory initially under that clone was rejected by the counter because it is inside the lane root. I moved counter work to sibling scratch `/fast/scratch/hyaku/mado-r50/work`, which meets the counter's explicit requirement (outside repo, lane and its parent, and /tmp,/var/tmp). This successful run used nonce 501. A second run was attempted asynchronously but cancelled after the invocation was misconfigured; therefore the required two-nonce evidence is incomplete and no second verdict is claimed.

## Clause review: docstring vs registration

- `t` matches: docstring requires the revision-addressed tool blob to be regular mode 100644/100755; registration's `tool=present` predicate is consistent.
- `s` matches: selftest threshold and exact last nonempty line plus the two refusal cases are explicit, and registration uses the same passing predicate.
- `f` matches: pinned fixture file/fallback, clean compile, default-path byte comparison, pinned judge/record drift check and stdout+exit comparison are the stated contract; registration documents 633 fixtures.
- `g` matches the frozen generator specification: 150 nonce-seeded cases; layout/variant combination and ARG pool described; each judged at count time. It is non-vacuous by construction because it selects among full header names and U names in addition to the frozen pools. [INFERENCE] A deterministic proof that these particular nonces actually sampled a novel argument/layout combination was not captured in the first run output.
- `r` matches docstring's traced tool-run restriction and exception limited to selftest writes under /tmp. Successful run reported zero trips.
- `i` matches the explicit bwrap mount allowlist and absence of network/judge library from the tool sandbox. Run emitted `python=python3.14 ... libs=42 site_packages=hidden net=none`.

Registration lines 10-17 summarize the same counter clauses/predicate; line 22's claimed 57,865 reference comparisons is explicitly not counter evidence and remains an outside-scope known routed defect (D3). No actionable defect found in clauses t/s/f/g/r/i from this run. Two-nonce requirement remains a verification gap, not a pass.
