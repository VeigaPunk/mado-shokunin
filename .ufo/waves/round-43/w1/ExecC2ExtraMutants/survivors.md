# C2 survivors - controls the counter ADMITS

Every row was built on the registered genuine fixture (`run-c2-controls.py::admitted()`)
and scored with that module's `score()` under the three scorers in `harness.py`
(`real` = the frozen counter, `patched` = the registered pin-patched copy, `pinfree` =
supplementary copy whose whole PINS literal is rebuilt so a defect inside a pinned
receipt is reached by its own clause). A survivor is a control whose defect survives:
the counter reports `admitted=1/1` under its primary scorer.

Classification key:
- **RESIDUAL (declared)** - the predicate's docstring already declares this hole;
  binding the claim to the quote is the non-author closure's job, not the counter's.
- **HOLE** - not declared in the docstring; the clause that should kill the control
  does not. Severity is judged by what the hole lets land.
- **LEGITIMATE** - no clause should kill it; the control satisfies the contract.

Evidence column: a source quote is `receipt:line`, re-verified by this harness with the
counter's own `quote_at()` against the pinned `fetch/` bytes; `fixture line` marks a
generated fixture line, `fixture-local` a receipt the fixture invents (held id).

| control | scorer | clause vector | clause that should kill it | claim-to-quote binding is a non-author job? | classification | verified evidence |
|---|---|---|---|---|---|---|
| CL23-gate-outside-section | patched | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | d | no - the failing check is the counter's own | HOLE (low): the outside-section scan drops any line whose TEXT equals an in-section line (`line not in in_gate`), so a byte-identical GATE line under another heading is invisible to d. Only a differing outside line is counted. | Hyprland-Target.cpp:11 |
| CL39-refuse-foreign-path | patched | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | i | no - the failing check is the counter's own | HOLE (low): clause i tests os.path.basename() only, so a foreign path with a staged basename is accepted; the docstring's residual list does not declare it. | lesson (fixture line) |
| CL40-admit-foreign-path | patched | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | i | no - the failing check is the counter's own | HOLE (low): same basename-only test on the ADMIT target; a file outside the package is accepted as the admitted staged file. | lesson (fixture line) |
| CL55-quote-truncated-at-punctuation | patched | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | d | not applicable | LEGITIMATE (no clause should kill it): d's rule is a word-boundary rule; the quote ends with a word char followed by `;`, so 3-25 words and word-bounded. The semantic residue is claim binding (declared residual). | Hyprland-Target.cpp:11 |
| CL62-two-digit-id-invisible | patched | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | b | no - the failing check is the counter's own | HOLE (low): SRC_RE, the ghost scan, ROW_RE and GATE_RE all require 3+ digits, so an S99 citation and its source line are neither counted nor rejected; the entry is admitted carrying an unregistered citation. | entry (fixture line) |
| R01-real-quote-unsupported-size-claim | real | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | g | yes - declared residual | RESIDUAL (declared): the docstring's last paragraph declares that a real receipt can be cited for a claim it does not support; binding claim to quote is the non-author closure's job. | Hyprland-HyprCtl.cpp:395 |
| R05-real-quote-exclusivity-claim | real | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | g | yes - declared residual | RESIDUAL (declared): same claim-to-quote hole; the census line itself stays honest, only the prose claim is unsupported. | host-clients-r43.json:49 |
| R06-real-quote-current-value-claim | real | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | g | yes - declared residual | RESIDUAL (declared): the quote shows the assignment into the animated variable, not that hyprctl reads the current value. | Hyprland-GeometricMovableAnimated.cpp:45 |
| R08-held-id-invented-receipt | real | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1` | d | yes - declared residual | RESIDUAL (declared): the docstring declares 'a held id's receipt is not pinned'; any held-id receipt bytes pass d. | S050.txt (fixture-local, not a pinned receipt) |

