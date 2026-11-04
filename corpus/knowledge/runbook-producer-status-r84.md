source: S487 — https://www.gnu.org/software/bash/manual/html_node/Pipelines.html section 3.2.3; .ufo/waves/round-84/controls/c2-runbook-cases-r84.json
verified-at: 2026-11-04; instrument freeze 3f9eec3906ddd1492e8bc08325e83064f00111ea
recheck: python3 -I quality/counters/c2-r84-runbook.py --repo . --rev REV --controls .ufo/waves/round-84/controls/c2-runbook-cases-r84.json --carried .ufo/waves/round-83/controls/c2-runbook-cases-r83.json --scratch-root DIR

# Producer status is part of an honest desktop probe

A pipeline's final stage can print plausible output and exit0 while its producer failed. A text-shape matcher cannot reconstruct the erased status. S487 documents the default last-command status and pipefail's rightmost nonzero status. The runbook therefore declares `set -o pipefail;` in its pipeline commands, rather than pretending ordinary `sh -c` already supplies that behavior.

The frozen set supersedes only argv/skill_anchor on fifteen existing pipeline cases, leaving their expected shapes, samples and negatives intact. Two new contained fixture rows exercise the execution boundary: the comparison prints unguarded=0/guarded=7, and a guarded producer prints plausible `b true` but exits7. Its dedicated matcher requires both rc7 and that text; rc0 with identical text is a negative. These fixtures read no desktop state and write no files. They demonstrate status propagation, not successful live D-Bus calls.

Before-control `.ufo/waves/round-84/receipts/control-c2-r84-unguarded.txt` is re-executed this round: producer exits7, unguarded tail returns0, expected failure pair does not match. This is the substantive no-work control; a predecessor counter refusing a changed section heading would not prove the semantic improvement.

The full recheck binds SKILL/tool/fixture bytes to REV and executes the actual read-only desktop rows. Successful shape matching is still not rendering, producer honesty, tray health, or attribution. A nonzero producer propagated by pipefail fails an ordinary row even when stdout looks right. A head/tail consumer can cause SIGPIPE on large output; that is an honest nonzero outcome, not permission to suppress the producer failure. Host support for pipefail is established by the contained fixture, not inferred merely from the word `sh`.

Frozen finite population: 33 rows and 29 mutations; re-derive with the recheck command. Mutation population is asserted before scoring; diagnostic --no-mutants does not claim TARGET_MET. The strip-guard execution mutant tests actual command execution, not only a mocked rc/out pair.
