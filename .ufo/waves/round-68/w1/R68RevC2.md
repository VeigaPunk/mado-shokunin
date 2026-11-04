# R68RevC2 — C2 adversarial review

Axes: calibration C1; operability C2 (review scope). Recommendation: **C2 predicate unsound as bounded**. The twelve actual gate repairs pass the source census and the sampled replacement hazard; the census executable does not enforce the frozen contract.

## Findings, severity order

1. **High — denominator deletion still earns TARGET_MET.** `quality/counters/c2-r68-reader-guard.py:168-174` checks only readers>0, unguarded=0 and all supplied controls correct. It never requires population=20, readers=13, or controls=11. Deleting every quoted object-read verb from the repaired axis gate gives `reader=no guard=no`, then `population=20 readers=12 guarded=12 unguarded=0 controls=11/11 verdict=TARGET_MET`, rc=0. This violates the declaration's explicitly frozen denominator. The printed line is not the exact frozen success line, so an independent consumer comparing the *entire* frozen line could reject it; the executable's own verdict and rc falsely accept it. Do not describe reader deletion as prevented by this counter.

2. **High — the exact frozen command cannot run.** The declaration includes `--scratch-root DIR`; parser lines 323-329 accept only repo/rev/controls/selftest. Exact baseline command exits 2: `error: unrecognized arguments: --scratch-root /fast/scratch/hyaku/mado-r68/R68RevC2`. All successful measurements below explicitly omit that unsupported option; they are not claimed as successful execution of the exact frozen command.

3. **Medium — guard detection accepts string values rather than guard keys.** Lines 100-112 accept any descendant constant equal to the key. `env={"LABEL":"GIT_NO_REPLACE_OBJECTS"}` followed by an unguarded git show is reader=yes guard=yes. This is beyond the declared branch/dataflow limitation: it constructs no guard key at all. Source-presence score can be inflated without a guard.

4. **Medium — a declared update-keyword construction is missed.** `env={}; env.update(GIT_NO_REPLACE_OBJECTS="1")` followed by git show with env=env is reader=yes guard=no. Lines 118-121 only inspect call keywords named env, so update's guard keyword is ignored. The declaration explicitly includes `dict()/update()` keyword construction. Annotated literal binding `env: dict={"GIT_NO_REPLACE_OBJECTS":"1"}` is also missed (AnnAssign unhandled). Computed constant concatenation is missed too; that last case is a syntax-coverage limitation rather than a separately declared guarantee.

## Executed commands and evidence

All commands, cwd, stdout, stderr and exit codes are in `R68RevC2/receipts.json`; full paired gate outputs in `R68RevC2/behavior.json`; exact attack sources in `R68RevC2/attacks.json`; reviewed draft hashes in `R68RevC2/draft-sha256.json`. Paths in this paragraph are relative to this report's directory.

Counter SHA256: `0e853b1b11b3f327bc2c0e6a4aa6ce32a5fc5561d9575b0bf1bc548c7f4dfea8`.
Frozen controls SHA256: `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91`.

Let L=/home/vgpnk/Projects/shokunin/mado-shokunin, C=$L/quality/counters/c2-r68-reader-guard.py, K=$L/.ufo/waves/round-68/controls/c2-controls.json, S=/fast/scratch/hyaku/mado-r68/R68RevC2.

- `python3 -I "$C" --repo "$L" --rev 510100c8 --controls "$K" --scratch-root "$S"`: rc=2 (unsupported option).
- Same command without `--scratch-root "$S"`: rc=1, final line `MADO_R68_READER_GUARD: population=20 readers=13 guarded=1 unguarded=12 controls=11/11 verdict=TARGET_MISSED rev=510100c81e6cf63fec6be380c2f2f9c670f32cbc`.
- Fixture: created with `tempfile.mkdtemp(prefix="fixture.",dir=S)`; `git -C D init -q`; asserted `git -C D rev-parse --show-toplevel == D` before commits. Copied all twenty lane quality/check-*.py files, then overlaid all twelve sibling draft files (paths/hashes recorded). Added quality and committed with fixture-local user identity. Every git call names `-C D`; no lane git mutation.
- `python3 -I "$C" --repo D --rev f17140c107e7e7410cbe83a335c03c1e9659f754 --controls "$K"`: rc=0, final line `MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 verdict=TARGET_MET rev=f17140c107e7e7410cbe83a335c03c1e9659f754`.
- Reader deletion reproduction: replace every match of counter.VERB_RE in repaired check-axis-scores.py by its two quotes with empty contents; commit fixture. `python3 -I "$C" --repo D --rev 6ae3e0f733f3f8cb046356eca028c34e7154d727 --controls "$K"`: rc=0, final line `MADO_R68_READER_GUARD: population=20 readers=12 guarded=12 unguarded=0 controls=11/11 verdict=TARGET_MET rev=6ae3e0f733f3f8cb046356eca028c34e7154d727`. Earlier renamed-verb variant also produced 12/12 TARGET_MET, rc=0 (receipt retained).
- Replaced fixture's worktree-only check-wave-done.py by `print("worktree only")`; reran at the committed SHA: still reader=yes guard=yes for that file, same committed totals, rc=0. Object enumeration correctly ignores worktree edits.

## Census attacks

Every case includes a git show subprocess invocation; exact sources are preserved in attacks.json. Standalone reproduction (rc=0):

```sh
python3 -I -c 'import runpy,json,sys; m=runpy.run_path(sys.argv[1]); cases=json.load(open(sys.argv[2])); [print(k,m["classify"](v["source"])) for k,v in cases.items()]' "$C" "$L/.ufo/waves/round-68/w1/R68RevC2/attacks.json"
```

| Case | reader | guard | Interpretation |
|---|---|---|---|
| comment only | yes | no | correctly rejected |
| docstring only | yes | no | correctly rejected |
| unrelated labels dict passed as env=labels | yes | no | frozen rule rejects it; note actual env dictionary would set the key if executed |
| dead if False branch | yes | yes | runtime false positive, explicitly admitted by declaration |
| uncalled helper builds guard | yes | yes | runtime false positive, admitted no-dataflow limit |
| env overwritten with {} | yes | yes | runtime false positive, admitted no-dataflow limit |
| key string occurs only as LABEL value | yes | yes | false positive; finding 3 |
| guard key has empty value | yes | yes | runtime false positive, admitted value-not-interpreted limit |
| computed real guard key | yes | no | runtime false negative; constant expression not evaluated |
| annotated real guard literal | yes | no | false negative; AnnAssign ignored |
| env.update guard keyword | yes | no | false negative; finding 4 |
| shell-string git show | no | no | runtime reader false negative, consistent with frozen quoted-verb rule |

## Behavior comparisons, all twelve repaired gates

Committed comparator bytes were extracted with `git -C "$L" show e0727cda:quality/NAME` into owned scratch. Both variants ran `python3 -I FILE ARGS` with cwd=S and explicit TMPDIR/TMP/TEMP=S; every real invocation read the lane at freeze `e0727cda15621766c35dcf8b70c211b6531aab45` (F below). Commands/outputs are verbatim in receipts.json. No desktop/host-serial option used.

| Gate | real arguments (repo=L) | base/repaired rc | selftest base/repaired |
|---|---|---|---|
| anchor-cover | --repo L --rev F --entry corpus/knowledge/replace-ref-citation-boundaries-r67.md --work S/anchor | 0/0 | unsupported |
| axis-scores | --repo L --rev F | 1/1 (stale navigation 71/71 vs 79/79) | 0/0, 18/18 |
| control-receipts | --repo L --tip F --round 67 --data-registry DATA.md | 1/1 (no receipts) | unsupported |
| deliverables | --repo L --rev F --file L/quality/check-axis-scores.py | 0/0 | unsupported |
| evidence-pointers | --repo L --rev F --branch F | 0/0 | unsupported |
| freeze-order | --repo L --rev F --round 67 --wave w1 --work S | 1/1 (no_freeze) | 0/0, OK |
| index-rows | --repo L --rev F | 0/0, rows=79 errors=0 warns=3 | 0/0, 10/10 |
| index | --repo L --rev F | 0/0, indexed=79/79 | 0/0, 12/12 |
| landed-contract | --repo L --frozen-rev F --frozen tools/mado-terminal.py --landed L/tools/mado-terminal.py | 0/0, frozen=9 landed=9 | unsupported |
| round-outcome-first | --repo L --rev F --round 67 | 1/1 (no-surface) | 0/0, cases=5 |
| session-material | --repo L --rev F | 1/1, files=33540 findings=280 | 0/0, 94/94 |
| wave-done | --repo L --rev F --round 67 | 0/0, settled=1 | 0/0, 62/62 |

Supported selftests used --selftest; freeze-order and wave-done additionally used --work S/NAME-variant. All completed paired invocations above have byte-identical stdout/stderr and identical rc; no repair behavior drift observed in these samples.

Every earlier command difference is retained: initial deliverables run used a relative --file from scratch and errored rc=1 in both versions; traceback file names and line numbers differed (125 vs 127), a cosmetic source-location difference. Correct absolute-path run above succeeds identically. Initial landed-contract run used check-session-material.py, which has no contract list: both rc=2, identical `NO-LIST frozen=False landed=False`; corrected real list run above succeeds identically. These were invocation/input errors, not hidden green checks.

## End-to-end refs/replace hazard

Used actual base/repaired check-landed-contract.py processes, not a simulated git helper. In fixture D, committed contract.txt with `"""Out of contract: alpha; beta. Where detected"""` and put the same real bytes in S/landed.txt. Forged object bytes: `"""Out of contract: alpha. Where detected"""`.

Commands (all rc=0 except the explicitly failing base gate):

```sh
git -C D add contract.txt
git -C D -c user.name=Review -c user.email=review@example.invalid commit -qm 'hazard real blob'
git -C D rev-parse HEAD:contract.txt                    # BLOB
git -C D hash-object -w S/forged.txt                    # FORGED
git -C D update-ref refs/replace/BLOB FORGED
git -C D show HEAD:contract.txt                        # alpha only (forged)
GIT_NO_REPLACE_OBJECTS=1 git -C D show HEAD:contract.txt # alpha; beta (real)
python3 -I S/base-check-landed-contract.py --repo D --frozen-rev HEAD --frozen contract.txt --landed S/landed.txt
# rc=1; ADDED-UNREGISTERED beta
# CHECK96: frozen=1 landed=2 added=1 removed=0 unregistered=1 verdict=NARROWED
python3 -I L/.ufo/waves/round-68/w1/R68ExecGate3/draft/quality/check-landed-contract.py --repo D --frozen-rev HEAD --frozen contract.txt --landed S/landed.txt
# rc=0; CHECK96: frozen=2 landed=2 added=0 removed=0 unregistered=0 verdict=OK
```

Exact resolved argv, object hashes and outputs are recorded in receipts.json. Both clean lane invocations returned OK as above. The repaired gate demonstrably reads the real blob through the planted replacement.

## Residual risk and verification gaps

- lsp device unavailable (`read xd://lsp`: No such tool). Definition/caller review used actual source/diffs and executed commands, not claimed semantic-reference proof.
- Source census is not execution/dataflow proof; dead branches, unused helpers, overwritten env and values are admitted limitations. The key-as-value and update-keyword results contradict narrower declared syntax claims independently of those limits.
- Nonzero existing lane verdicts are reported, not suppressed or recast as clean gate passes. Seven supported selftest pairs passed; five gates expose no selftest option.
- Canonical runtime identity, rerouting and resume_continuity_v1 are not touched by these twelve environment repairs. No broader saturation or runtime admission claim is made.
- No tools installed, production edits, commits/staging in lane, desktop probes, services, sockets, package-manager operations, or credential reads.
- Reviewed sibling draft SHA256 values are in draft-sha256.json; no production drafts authored by this reviewer.
- Scratch removal: completed before yield (entire owned scratch tree removed in finally).
