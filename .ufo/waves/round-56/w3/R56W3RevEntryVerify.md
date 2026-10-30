# R56W3RevEntryVerify — attempt 2

## Scope and axes

Attacked: the entry's **How to verify (read-only)** block at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, command by command. Axes: reproducibility, revision/pin identity, expectation fidelity, read-only safety. Frozen claims and registration v2 were read first; original registration supplied unchanged definitions. No predicates or lane source files were changed.

## Findings by severity

### F1 — weakens reproducibility; does not block a frozen claim

`corpus/knowledge/hyprland-config-autoreload-r56.md:160-161`: the live commands cannot obtain their intended observations in this seat's environment, and the version pipeline hides failure.

Exact inputs/output:

```text
$ hyprctl getoption misc:disable_autoreload -j
HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)
exit=1

$ hyprctl version -j | sed -n '3p'
<empty stdout>
exit=0

$ hyprctl version -j | sed -n '3p'; printf 'PIPESTATUS=%s\n' "${PIPESTATUS[*]}"
PIPESTATUS=1 0
```

Expectation versus observation: getoption should emit live option JSON; version should expose the live commit line. Neither happened. The pipeline's zero exit is not evidence of a successful version query. The block does not document its session-signature prerequisite or propagate the upstream error. This is an execution/environment qualification, not evidence that the historical host captures are false or that Hyprland is not running. Recommendation only: document the required compositor-session environment and preserve/report the upstream command's failure. Do not change any frozen predicate.

## Execution evidence and null results

Durable receipt: `.ufo/waves/round-56/w3/R56W3RevEntryVerify/receipts/howto-a2.txt` (absolute: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevEntryVerify/receipts/howto-a2.txt`). It records every exact command, expectation, MATCH/MISMATCH, exit status and complete decisive output.

All 14 non-comment block statements ran: two assignments and twelve command lines. **12 MATCH; 2 MISMATCH**, both live queries above. REV was changed to the assigned tip as the entry permits; `--work` was changed to seat-owned scratch as required. Independent commands ran concurrently with explicit scratch cwd/TMPDIR.

The block's git-show/sha256sum command returned the frozen tables SHA `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2`. The three quote spot-check pipelines found all selected frozen quotes (9 ConfigWatcher, 5 ConfigManager, 2 MiscFunctions anchors); full handleSource/absolutePath body commands worked. Supplemental `git -C <lane> show <tip>:.ufo/waves/round-56/fetch/<pin> | sha256sum` checks matched all 12 frozen C1 source/host hashes; each exact command and hash is in the receipt. Host stat reported a regular config file; source count returned `18`.

The literal counter invocation succeeded; its working-tree executable was byte-identical to the revision blob. A separately extracted exact-revision executable also ran using `python3 -I`, `--rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1` and seat-owned `--work`, exit 0:

```text
MADO_AUTORELOAD_ENTRY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
```

No additional broken command or pin/quote mismatch was found by these commands. This is C1 lexical/pin evidence, not an entailment proof.

## Residual risk and verification gaps

- Live option/version remain unverified because `HYPRLAND_INSTANCE_SIGNATURE` is absent. No compositor/config mutation was attempted.
- No C1 harness command exists in the actual How-to-verify block despite its comment saying “counter and harness”; no harness, C2/C3 controls or unrelated tests were run by this seat.
- LSP unavailable: `read xd://lsp` returned “No such tool”. This Markdown/command review asserts no semantic reference/definition/diagnostic proof.
- This scoped review does not establish runtime reload behavior, resume continuity, same-identity rerouting or saturation; none is observed by this block.
- No tools installed, no clone/archive, no git mutations. All scratch under `/fast/scratch/hyaku/mado-r56/R56W3RevEntryVerify/` was removed after copying receipts. Only assigned deliverable paths were written in the lane.

## Self-evaluation

Accuracy 4/5: exact outputs retained; live values unavailable. Completeness 4/5: every block statement ran, but session-dependent observations failed. Clarity 4/5: receipt separates expectations from observations; full body output is lengthy. Actionability 4/5: F1 identifies the prerequisite/error-propagation issue without claiming a frozen-predicate failure. Conciseness 4/5: report summarizes the longer receipt. Mean 4.0/5. Highest-impact improvement is providing a valid read-only compositor-session environment for the two live observations; that prerequisite was unavailable to these commands. The user should agree with the explicit qualification rather than an all-green claim.
