# SkillRegistryDraft — six probe rows and one append-only note drafted; four named scripts not yet landed

Draft: `.ufo/waves/round-19/drafts/SkillRegistryDraft.md` (sections A–D). Only that file was written, plus this report. No lane file, no `SKILL.md` edit.

## Findings

1. **Column shape confirmed.** `SKILL.md:549` header is eight columns (`name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner`); rows run `:551`–`:571`; `:571` (`mado-measure-mutants`) is the last row; `:572` blank. Insertion after `:571` (section A). The round-18 precedent draft (`.ufo/waves/round-18/drafts/SkillRegistryDraft.md`) uses the same shape.

2. **Four named scripts are absent.** `ls` of `.ufo/waves/round-19/` shows no `anchor-durability.py`, `supersede-sweep.py`, `supersessions.json` or `frozen-repin.py`. Their rows are transcribed from the item contracts in `.ufo/waves/round-19/w1/spec.json` (items `AnchorDurability`, `SupersedeSweep`, `FrozenRepinScript`) and carry `contract control, unobserved` in the self-test cell. I did not run them.

3. **`landed-check.sh` landed** (present at drafting). Its header states the exit map used in the draft: `0` all LANDED; `1` any LOCAL_ONLY or MISSING; `2` usage or could-not-evaluate. Its only network call is `git ls-remote origin refs/heads/master`; it never fetches or writes git state or invokes jj. Not executed by me.

4. **Counters run read-only at `9c54c56`** (both exit 0; both usage errors exit 2 — `fresh-pins.py nosuchrev` → `could_not_evaluate: rev nosuchrev`; `tw-recall.py` with no argument → usage, rc 2):
   - `fresh-pins.py`: commit `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, denominator 13, current 2, score 1.5385. Current: `corpus/README.md:44` and `corpus/knowledge/walker-route-r18.md:1`. The other 11 are not current. Output saved at `/tmp/r19-reg-fresh.json` (scratch).
   - `tw-recall.py`: tool sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` (matches the spec's pin), incident lines 6, detected 3, score 5.0. Detected: `inputs/r13-global-capture.jsonl:1`, `inputs/r14-review-source-bar.jsonl:1`, `inputs/r15-libinput-events.jsonl:1`. Missed: `inputs/r13-root.jsonl:4`, `inputs/r14-source-safety.jsonl:2`, `inputs/r14-source-safety.jsonl:3`. Output saved at `/tmp/r19-reg-recall.json` (scratch).
   - Script sha256: `fresh-pins.py` `a094be01…d789`; `tw-recall.py` `22090298…cd28`; `SKILL.md` `9a2088a4…3e41`.

5. **Tripwire class spelling conflict.** The round-18 draft `TwInstallerChannels.patch` adds class `tool_install` (`CLASSES` at patch line 22; `classify_installer` returns `tool_install` at lines 113–152). The round-19 spec calls the class `installer`. No draft token exists for `vcs_write` in `.ufo/waves/round-18` or `.ufo/waves/round-19` (only in `w1/spec.json` and `w1/dispatch.json`). The draft therefore names both as PENDING L1 DECISION and does not pick a spelling.

6. **The `mado-tripwire` verdict map enumerates classes.** `SKILL.md:563` lists `host_mutation/package_query/live_probe`. If a class lands without a verdict-map update, its findings sit outside the stated verdict. Section B is an append-only note; the existing row is not edited.

7. **Kind vocabulary gap.** `mado-frozen-repin` writes a caller-selected DIR. The registry knows only `gate` and `probe`. The draft uses `probe` as instructed and records the choice as D1 for L1.

8. **Counter limits.** `fresh-pins` passes any line holding `2.17.2` and any `S###`, so it does not check row validity. `tw-recall` credits any finding class on an incident line and has no precision guard. Section C states both limits for the registry.

## Evidence pointers

- Worktree reads: `SKILL.md:549-572`, `SKILL.md:563`, `SKILL.md:566`, `SKILL.md:584-594`.
- `tools/mado-tripwire.py:61` (`CLASSES`) at both worktree and `9c54c56` (same line).
- `.ufo/waves/round-19/fresh-pins.py` (sha `a094be01…`), `.ufo/waves/round-19/tw-recall.py` (sha `22090298…`).
- `.ufo/waves/round-19/w1/spec.json` items `AnchorDurability`, `SupersedeSweep`, `FrozenRepinScript`, `LandedCheck`.

## Limits

- Did not run `anchor-durability.py`, `supersede-sweep.py` or `frozen-repin.py`; they do not exist.
- Did not verify any `python3 -I` invocation against a landed header or `--help`.
- Read `SKILL.md` from the worktree, not `9c54c56`. Line numbers are the worktree's at drafting time.
- Did not run `landed-check.sh`; its header was read only.
- Did not check the round-18 frozen replays or `mado-tripwire --frozen`; those rows are unchanged.
- The `--ledger` default for `supersede-sweep` is unknown until the script lands ([UNK]).
- The `frozen-repin` DIR-exists rule is unknown until the script lands ([UNK]).

## Installs

none
