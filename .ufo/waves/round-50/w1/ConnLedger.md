# ConnLedger findings

## Verdict
No missing tools or wrong rows found in the r49 draft ledger at its declared base, but its frozen scope is stale for the round-50/base retarget.

## Evidence
- `check-ledger.py --repo <lane> --rev 03e4ae76... --ledger <draft>/ledger.md` → `LEDGER rows=12 excluded=3 receipts=12 verdicts=12 current=7 stale=3 uncommitted=1 none=1`; `LEDGER-MATCH`.
- At round-50 base `8ae47b957034ae21012bbf09173cca2c48be345e`, `git ls-tree -r --name-only <base> -- tools/` lists 16 blobs, adding `tools/mado-keysym.py` to the 15-tool r49 base. The r49 checker pins `BASE=03e4ae76...` (`check-ledger.py:49`) and its row/exclusion declarations contain no keysym (`:59-146`); therefore it is not a valid completeness check at r50 base.
- `mado-keysym.py` is a capability tool that reads a caller-supplied compiled keymap and keysym, not live state (docstring lines 2-5, 14-21). It should not be added to a ledger specifically scoped to live-state tools; instead explicitly exclude it as non-live-state with a cited reason, to preserve completeness while making the scope auditable.
- Three sampled receipt checks at the r49 ledger’s revision: eventq receipt `.ufo/waves/round-38/receipts/eventq-live.txt` exists and its line 8 is quoted verbatim by ledger lines 57-60; geometry receipt `.ufo/waves/round-44/w2/SentLiveRun/live-run.txt` exists and line 7 matches ledger lines 90-93; monitors receipt `.ufo/waves/round-46/w1/ExecW2Monitors/live-runs.txt` exists and line 35 matches ledger lines 101-104. Each path and contents were read from committed worktree files; checker independently derives from git objects.
- Round-49 receipt `.ufo/waves/round-49/receipts/c1-after-data.txt:643` says `fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`; this does not change live-state ledger scope.

## One bounded proposal: retarget scope without misclassification
For the round-50 ledger refresh, keep live-state entries restricted to actual live probes/joins/session records/config-scored tools, but change the checker’s instrument-set rule to explicitly partition all `tools/` blobs into (a) live-state rows and (b) non-live-state exclusions. Add `mado-keysym.py` to exclusions with its docstring’s read-only, caller-provided-input rationale; point the checker at round-50 base and re-derive candidate receipts there. Preserve a generated complete tool inventory so a new tool cannot silently fall outside both partitions.

## Axes, contradictions, risks, verification
- Axes: improves coverage (inventory completeness) and operability (ledger remains usable as a current snapshot); no axis harm intended.
- Contradiction: “live-state tool ledger” does not mean every tool under `tools/` is a live-state tool. The current checker’s all-tools-must-be-row-or-exclusion rule enforces inventory completeness, but the r50 base adds a tool with no live-state interaction; classifying it as live would mislead.
- Risk: simply retargeting the old checker and calling keysym a live row would produce a false claim; excluding it without a cited class reason would be a silent gap. Round-50 receipts must be checked against the exact r50 base, not today’s worktree.
- Verification: rerun the ported checker against base `8ae47b95...`; assert every `tools/` blob occurs exactly once in live rows or explicit exclusions, then independently check three receipt paths, verdict-line bytes and receipt revisions via `git show` at that base.
