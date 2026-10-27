# PRED-C1-r51 predicate attacks

Scope: attacks judged strictly against the frozen sentence in round-51 `claims.md`; these are mock artifacts and arithmetic, not an implementation run. Axes: coverage + operability.

## 1. Pointer basename only in a comment

Mock: every ledger row lists its real population file and a pointer such as `quality/notes.md`; that file contains `<!-- mado-hostguard.py -->` but no accountability statement connecting it to the tool.

Why: predicate requires only an accountability pointer naming an existing repo file that “contains the file's basename”; the kill rule only tests basename presence. A comment satisfies the literal test.

Verdict: PASS — can still reach TARGET_MET.

Closing fix: require pointer content to contain an explicit accountability record for the basename (rather than mere substring occurrence), and assert that structure in the counter.

## 2. Descriptions copied across unrelated tools

Mock: all P ledger rows have a non-empty identical description, e.g. “Runs the lane tool and reports its result,” regardless of each file's behavior.

Why: predicate tests non-empty descriptions only; neither uniqueness nor fidelity to the referenced tool is stated. `empty_desc=0` and exact row count remain possible.

Verdict: PASS — can still reach TARGET_MET.

Closing fix: require each description to be a meaningful, file-specific summary, validated by a review/control rather than a nonempty-string check alone.

## 3. Population enumeration excludes or ambiguously handles files

Mock: an implementation enumerates only `*.py` in `tools/`, while the frozen sentence says “files under `tools/`”; a tracked `tools/example.sh` is omitted. Or it recursively counts `quality/receipts/*.py` / `tools/__pycache__/*.py` inconsistently depending on whether those exist in the checkout.

Why: “files under tools/” has no extension/file-kind exclusion; `quality/*.py` is top-level-only, while `quality/counters/*.py` is explicit. The predicate does not say tracked-only, recursive depth, symlink policy, generated/cache exclusions, nor whether untracked worktree files enter P. Thus a counter and reviewer can disagree on P, and the report format cannot disambiguate that disagreement.

Verdict: PASS — a permissive or mismatched population implementation can count P after silently omitting a tool file and still report equality.

Closing fix: define P by a precise revision-tree pathspec and file policy (e.g. all regular tracked files recursively under tools/, top-level quality/*.py, and quality/counters/*.py; explicitly handle symlinks), and derive it from the requested rev.

## 4. Whitespace-only description

Mock: a ledger row uses `description: "   \t  "`.

Why: “non-empty description” is ambiguous: a raw length check accepts it, while a trimmed-content check rejects it; `empty_desc` is named but not defined in the sentence or kill control beyond “empty description.”

Verdict: PASS — if empty_desc is implemented as raw string nonemptiness, it can report zero.

Closing fix: define empty as `not description.strip()` and include whitespace-only control rows that must MISS.

## 5. Counter reads worktree rather than --rev objects

Mock: invoke `--rev <base>` while the worktree contains the new ledger and checker; the counter scans local paths, prints the requested base hash, and emits TARGET_MET. Alternatively, a candidate ledger staged only in the worktree makes a non-HEAD revision appear complete.

Why: predicate specifies behavior “at <rev>” and base result but does not explicitly require all population, ledger, pointer, and checker inputs to be loaded from that revision's objects. A worktree-reading counter could pass the positive invocation and lie about the base invocation when the relevant files are present locally.

Verdict: PASS — the predicate does not itself exclude this bypass.

Closing fix: require the counter to read every assessed file from the `--rev` tree (using isolated extraction or object reads), never the worktree, and test with worktree/rev disagreement in both directions.
