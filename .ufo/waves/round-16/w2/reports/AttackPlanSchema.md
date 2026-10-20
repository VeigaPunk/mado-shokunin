# MadoR16.AttackPlanSchema — falsification of tools/mado-action-plan.py JSON schema surface

Seat: MadoR16.AttackPlanSchema (leaf reviewer, read-only).
Scope: top-level plan object, `actions` list, action object, `kind`, `argv` exact types; frozen-mode replay of the same schema; coverage of the schema in pinned fixtures.
Anchors are to the integrated artifacts as they stand at review time (`tools/mado-action-plan.py` 752 lines, `.ufo/waves/round-16/safety-policy.json`, `.ufo/waves/round-16/safety-cases.json`, `.ufo/waves/round-16/frozen/`).

## Execution and provenance

- Gate, selftest, frozen replay, measure.py: **not executed** (contract: source reading only; L1 alone verifies).
- Read-only commands run: `sha256sum` on `frozen/plan.json`, `frozen/policy.json`, `safety-policy.json` (checksum fact only); `cmp` of frozen policy vs committed policy; `git status --porcelain` on `tools` and `.ufo/waves/round-16`; `ls`/`grep` on lane files.
- Installs or updates: none.
- Pins: `frozen/expected.json` `plan_sha256` = `82bc7652…febc3`, `policy_sha256` = `fb134d8f…18b7fc`. Both match the bytes on disk (checksum observed). The committed policy is byte-identical to the frozen copy.

## Verdict on the requested attack

**Attack did not reproduce at the source level: a malformed later action cannot return clean or denied early.** The whole action list is type-checked before any classification:

- `_evaluate` (tools/mado-action-plan.py:354-372) runs policy load → policy validation → plan load → `_validate_plan` → `_classify`. Classification only starts after `_validate_plan` returns `(actions, None)`.
- `_validate_plan` (lines 284-308) iterates **every** element of `actions` (`for i, action in enumerate(actions)`, line 296) and returns `plan_malformed` on the first bad one, before `_classify` sees any action. An earlier `package-install` or `read-source`+`sudo` refusal cannot short-circuit this loop.
- Result by source: `[read-source cat x] + [package-install pacman …] + [read-source argv:null]` → `plan_malformed`, exit 2, not `blocked_action_kind:package-install`, not `plan_safe`. Consistent with the documented rule in `safety-cases.json` assumptions (`finding_priority`, line 15) and SKILL.md's exit-2 row.

## Exact-type surface, checked

| Position | Check (anchor) | Result |
|---|---|---|
| top-level | must be `dict` (286-287); unknown keys rejected (288-290); `schema` if present must equal `mado-action-plan-v1` (291-292) | closed |
| `actions` | must be `list` (293-295); absent/`null`/object/string → plan_malformed | closed |
| action | must be `dict` (297-298); unknown keys rejected (299-301) | closed |
| `kind` | `action.get` then `isinstance(str)` (302-304); absence → None → rejected | closed |
| `argv` | `_is_str_list`: `isinstance(list)` and every element `isinstance(str)` (218-219, 305-307); `bool`/`int`/`null`/nested list rejected | closed |
| JSON | strict pairs (181-187), NaN/±Infinity (190-191, parse_constant), BOM and invalid UTF-8 (200), non-object root | closed; all raise into `except Exception` → plan_malformed |
| `kinds.get(kind)` (328) | arbitrary kind strings never reach the finding line; unknown string → exit 1 `unknown_action_kind`, non-string → exit 2 | closed |
| stdout | findings interpolate only pinned names (`blocked_action_kind:<pinned>`, `denied_executable:<exe ∈ pinned deny set>`); detail uses `!r` and `json.dumps` (ensure_ascii) | no injection path found |

Type-confusion checks that held: `paused` must be `is True` (234); `argv_nonempty` must be `bool` (270); frozen `expected_exit` must be `type(...) is int` (411), so `true` is rejected; frozen pin comparison is `.lower()` on both sides (420).

## Findings

### F1 — MEDIUM — frozen mode digest-verifies one read and replays a second read (TOCTOU, integrity claim not fully realised)

- Anchor: `run_frozen`, tools/mado-action-plan.py:414-422 computes `_sha256(path)` (a `_read_regular` open/read) for plan.json and policy.json; then line 424 calls `_evaluate(plan_path, policy_path)`, which calls `_load_json` (lines 356, 364) that opens and reads the files again via `_read_regular` (lines 196, 150-178).
- The verdict is therefore computed over bytes that were never hashed. The digest pin proves the bytes at time T1; the verdict is over the bytes at T2.
- Bounded counterexample (source trace, not executed): a writer with access to the snapshot directory replaces `plan.json` between T1 and T2 with a plan whose verdict is `plan_safe`. The pin check passes against the original bytes at T1 and the replay returns `frozen_match` (if expected were `plan_safe`/0) with exit 0 for a plan whose bytes were never pinned.
- The frozen-mode promise (docstring line 381 "Verify both pinned input digests, then replay"; SKILL row mado-action-plan-frozen; SCORECARD C2 row "digest-bound frozen run") implies the replayed bytes are the verified bytes. They are not.
- Selftest does not catch it: the tamper fixture (`frozen-tampered-plan`, selftest lines 687-691) tampers *before* the child process starts, never between reads.
- Fix shape for L1 to decide: evaluate from the bytes already hashed (parse `raw` returned by `_read_regular` once, pass the parsed objects into `_evaluate`), so one read is both verified and evaluated.

### F2 — MEDIUM — frozen_match exits 0 for a refused plan (documented, but a consumer hazard)

- Anchor: `run_frozen` lines 424-426: when `got_finding == want_finding and got_code == want_exit`, it emits `F_FROZEN_MATCH` with `EXIT_OK` (0). The plan's own finding is not a top-level field; the verdict JSON's `finding` is `frozen_match`, and the plan's `denied_executable:sudo` appears only inside free-text `detail`.
- Live committed instance (source trace, not executed): `.ufo/waves/round-16/frozen/` pins `plan.json` = `read-source ["sudo","pacman","-S",…,"libinput"]`, `expected.json` = `expected_finding: "denied_executable:sudo"`, `expected_exit: 1`. Pins match the on-disk bytes (checksum above). The replay derives `denied_executable:sudo`/1, matches, and the process exits **0** with `MADO_PLAN: frozen_match`.
- Documented: SKILL.md registry row `mado-action-plan-frozen` says "0 clean comparison (`frozen_match`, including expected refused plan)"; selftest `frozen-denied-match` pins exit 0 (lines 680-686). So this is a declared contract, not a bug.
- Risk: any caller that treats exit 0 as "plan permitted" (the gate's own `plan_safe`/0 meaning, SKILL row mado-action-plan) will read a refused plan as clean. Two different meanings share exit 0: `plan_safe` (plan admitted) and `frozen_match` (comparison matched, plan may be refused). Recommend L1 decide whether frozen should surface the replayed finding/exit as first-class fields or the operator docs should bold the distinction. Not an implementation error.

### F3 — LOW-MEDIUM — the requested schema property is not pinned by any fixture

- Selftest case list (tools/mado-action-plan.py:491-614) and `safety-cases.json` names (lines 32-437) contain no case where a **malformed later action follows an earlier refusal**. `first-refusal-wins` and `multi_action_green_then_red` have only well-formed later actions. The property is source-true (verdict section above) but a future refactor of `_validate_plan` into a lazy per-action check could regress it silently.
- Also unpinned: `actions` not a list (only "missing" in cases), top-level wrong `schema` value, `action.kind` non-string, `argv: null`, a FIFO/symlink-to-dir plan (only a plain directory is pinned, selftest line 564), and an over-16 MiB input.
- Suggested fixtures for L1 (not run by this seat): (a) `[read-source ["cat","x"]], [read-source argv:[7]]` → plan_malformed/2; (b) `[package-install ["pacman"]], [read-source argv:null]` → plan_malformed/2 (not `blocked_action_kind`); (c) `{"actions":{}}` → plan_malformed/2; (d) `{"schema":"x","actions":[]}` → plan_malformed/2; (e) `[{"kind":7,"argv":[]}]` → plan_malformed/2.

### F4 — LOW — `_read_regular` silently truncates a file that grows during the read

- Anchor: tools/mado-action-plan.py:161-174. The bound is `remaining = st.st_size + 1` (line 164); the loop stops at that count and returns the bytes read, with no check for further data. A file appended after `fstat` is silently cut at `st_size+1` instead of being rejected.
- Impact is narrow: both frozen digest and evaluation see the same truncated buffer within a process, and truncation of valid JSON usually fails to parse. It does break the module's stated fail-closed contract ("malformed bytes… fail closed", docstring 31-33) for growing inputs. Fix: after the bounded read, attempt one more `os.read` and reject if non-empty.

### F5 — LOW — paths are opened before the regular-file check

- Anchor: tools/mado-action-plan.py:154 `os.open(path, O_RDONLY | O_NONBLOCK)` precedes the `S_ISREG` check at 159. The docstring (150-151) says FIFOs/devices/dirs are "rejected", which is true of the result but not of the side effects: a device node or FIFO is opened (non-blocking) before rejection. Directory rejection is pinned (selftest 564); device/FIFO behaviour is not. Low; `O_NONBLOCK` removes the blocking hazard. Optional: `os.stat(path, follow_symlinks=True)` + `S_ISREG` before open, with `O_NOFOLLOW` if symlinks should be refused.

### F6 — LOW — CLI silently ignores `--policy` with `--frozen` or `--selftest`

- Anchor: tools/mado-action-plan.py:739-748. `--policy` is accepted with any mode; `main` returns at 744-745 (`--frozen`) and 742-743 (`--selftest`) without looking at it. Frozen mode always uses `DIR/policy.json`, so this is not a fail-open, but a caller who passes a different policy gets a verdict under the frozen directory's policy without an error. Recommend `parser.error` when `--policy` is combined with `--frozen`/`--selftest`.

### F7 — LOW — hygiene

- `git status` shows `tools/__pycache__/` untracked and `tools/mado-action-plan.py` / `.ufo/waves/round-16/` untracked (lane work in progress; expected). `__pycache__` should not be committed; ignore or remove at integration. No verdict effect.

## Declared-policy limits (distinguished, not defects)

These are stated in the gate docstring (lines 5-13), `safety-cases.json` `scope_limit` (line 17), and SKILL.md's round-16 classifier-limit note (533-536). They are reproduced here only so the operator sees the exact edges:

- **Symlink / hardlink / copy under another name.** `read-source ["/tmp/pm","-S","libinput"]` where `/tmp/pm` → `/usr/bin/pacman` → `plan_safe`. `_basename` is lexical (316); `argv[0]` is never resolved. Declared.
- **Unlisted wrappers and privilege tools.** `doas`, `pkexec`, `run0`, `su`, `nice`, `timeout`, `nohup`, `xargs`, `busybox`, `python3 -c`, `omarchy-pkg-add` all → `plan_safe` (the last two are pinned residual controls in `safety-cases.json` lines 411-436). The deny list is code-pinned (lines 109-112); `sudo` is denied but `doas`/`pkexec`/`run0`/`su` are not, which is an asymmetry worth an operator decision, not a schema defect.
- **Unicode whitespace.** `_basename` uses `str.strip()` (313), so `"sudo\u00a0"` is denied. This is over-denial, the safe direction. `sudo/.` yields basename `.`, which is not exec-equivalent to sudo (ENOTDIR), so it is not a bypass.
- **Kind labels.** Kind matching is exact (`kinds.get`), so `"package-install "` or `"Package-Install"` → `unknown_action_kind` (exit 1). Fail-closed.

## Residual risk and verification gaps

- All findings are source-trace only. F1 and F2 would be confirmed by a controlled race (F1) and by running `--frozen .ufo/waves/round-16/frozen` (F2, expected exit 0). Neither was run; L1 may choose to run F2 as a single verification command.
- F3 fixtures are proposals; they have not been added or executed.
- The round-16 frozen directory (`.ufo/waves/round-16/frozen/`, mtime 05:51) appeared after the initial glob; it was read directly and its pins checked by checksum only.
- No review of `measure.py`'s observation of the gate was performed beyond the SAFETY_ARTIFACTS presence/bytes list (measure.py:362-366), which does not execute the gate.

## Summary for L1

1. The malformed-later-action attack fails at source level: `_validate_plan` covers every action before classification.
2. Exact-type checks at top-level/actions/action/kind/argv are closed; no bypass of the type layer found.
3. Actionable: F1 (frozen read-then-replay TOCTOU, evaluate the hashed bytes) and F3 (add the later-malformed and type fixtures).
4. Decision needed: F2 (frozen exit 0 on refused plans) — documented, but ambiguous for callers.
5. Low: F4, F5, F6, F7.
