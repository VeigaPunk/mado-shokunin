# R55CritHoldout — report (round 55, wave w1, critic, leaf)

Scope: attack the C2 hold-out and its commitment (registration §C2; claims-frozen.md C2). Deliverable: `.ufo/waves/round-55/w1/R55CritHoldout/holdout-attack.md` (full findings, Table A, proposed rules R1–R5, proposed controls).
Receipts and demonstrations: `.ufo/waves/round-55/w1/R55CritHoldout/receipts.txt`, `.ufo/waves/round-55/w1/R55CritHoldout/attack/sibling_tool.py`, `attack/run_fixtures.py`, `attack/sandbox_export.py`.
Base 3b55b6e91e40f455dd56b2985e4ffc087ada92d5; freeze commit 54dacbd843d64ba744cd3f1bdc2ec622e5010039 (18:46:52 -0300).

## What I did

Read-only. Read claims-frozen.md, registration.md §C2 and §Seat boundaries, frozen-tables.json (`c2` field names and values, `c1` pin list), ctl/const-host.py, ctl/empty.py, ctl/lookup-committed.py, freeze-verify.py, all 18 committed fixtures under `fixtures/c2/`, `fetch/host-input.conf`, `fetch/host-getoption.json`, `fetch/SHA256SUMS.txt`, and the dispatcher `quality/check-r55-controls.py`. Ran read-only git (`rev-parse`, `show --name-only`, `ls-files`, `status`) and `sha256sum` on the two host files. Ran Python quirk checks (`python3 -I -c`). Built an exported copy of the committed C2 tree in scratch and ran a grammar-free attack tool over it.

No git or jj mutation, no commits, no host reads beyond the committed copies, no hyprctl, no writes outside my deliverable directory and scratch. Scratch `/fast/scratch/hyaku/mado-r55/R55CritHoldout/` removed before yield.

## Commands and decisive output

    git -C <lane> show --name-only 54dacbd8…  → freeze files: claims-frozen.md, ctl/*.py, fetch/*, fixtures/c2/*, (freeze-verify.py, registration.md, frozen-tables.json, receipts/*)
    git -C <lane> ls-files --error-unmatch quality/check-r55-controls.py
      → error: pathspec ... did not match any file(s) known to git      (harness untracked; not in the freeze)
    sha256sum fetch/host-input.conf fetch/host-getoption.json
      → 3769c92a… host-input.conf (= frozen pin); 5557e28f… host-getoption.json (= frozen pin)

    python3 -I run_fixtures.py <tree> attack/sibling_tool.py <tree>/fixtures/c2     (R1, harness layout)
      F01:ok F02:FAIL F03:ok … F16:ok F17:ok F18:ok
      fixtures=17/18
    python3 -I sandbox_export.py <tree> <clean>; python3 -I run_fixtures.py <clean> … (R2, argv inputs only)
      F01:FAIL … F16:FAIL F17:ok F18:FAIL
      fixtures=1/18

    python3 -I -c (quirks): re.match('[0-9]+','40abc') matches, fullmatch does not; '²'.isdigit() True;
      int('٣٠')=30; '\xa030'.strip()='30'; 'a\rb'.splitlines()=['a','b']; '\ufeffinput'.strip() keeps BOM;
      json.loads accepts NaN; isinstance(json.loads('{"int":true}')['int'], int) True

## Answers (detail in holdout-attack.md)

1. **18/18 + 8/8 without a grammar: reachable.** Memorising on argv is blocked by `lookup-committed` (0/8 hold-out). Reading the `expected.*` beside `--config` is not blocked by any frozen control: 17/18 committed, and 8/8 hold-out if the hold-out has the committed layout. The export has to be sandboxed (R2: 1/18).
2. **Commitment binds:** every regular file in each hold-out directory, if the walk covers the directory: args.json, expected.out, expected.rc, c*.conf, getoption.json, the names and the directory names through relpath. It does not bind the relpath root (not stated), symlinks/modes/empty dirs, the correctness of expected.*, or the execution contract (cwd, sibling reads, process use).
3. **Inference from the class names:** low to moderate. The classes point at Table A (ambiguous prose points). They do not reveal output. The real problem is that the reference is not the prose: committed F10 contradicts the literal KEY rule for an empty stack (hand trace: literal gives unsupported=3, fixture says 4).
4. **Selection by hold-out score biases the claim.** Proposed R1–R5 (freeze candidates by manifest before reveal, one reveal, pre-declared selector, report N, post-reveal retirement) and a derivability gate (second implementer derives hold-out expectations from prose before reveal; disagreements labelled prose-ambiguous).

## Defects and ambiguities (inputs shown in holdout-attack.md)

- D1 (High) sibling-read attack: 17/18 committed with no grammar; no frozen control detects it. Input: `fixtures/c2/F01/args.json`.
- D2 (High, cheap fix) export is not sandboxed; receipts R2 shows the fix works.
- D3 (High) the harness that computes the hold-out commitment and runs the controls is not frozen: `quality/check-r55-controls.py` untracked; `r55_ctl_c2.py` absent; neither in freeze 54dacbd8.
- D4 (Medium-high) commitment has no frozen root convention and no frozen self-test vector; a root mismatch reads as `holdout_commit=bad` on a correct tool.
- D5 (Medium) reference is not the prose: committed F10 requires the bare-LHS reading for an empty stack, which the literal text does not give (hand trace).
- D6 (Low-medium) the sealed directory path is in committed `frozen-tables.json` (`c2.holdout_dir`), although the seat spec says seats are not told the path. I did not open it.
- D7 (Medium) selection and authorship are not independent: the L1 writes the hold-out and the reference, selects, and integrates.
- D8 (Low) `lookup-committed` demands 0/8 hold-out; a hold-out argv equal to a committed argv (e.g. `[]`, F17) trips it on a correct tool.
- Table A (A1–A10): ambiguous prose points a hold-out can hinge on: the `[0-9]+` fullmatch vs prefix reading; the whole-line `$`/backslash check that includes comments; `str.strip()` vs the stated strip set (NBSP, `\x1c`–`\x1f`); `splitlines()` vs split on `\n` (lone CR); BOM; Unicode digits through `int()`; blank getoption lines; `NaN` in JSON; `bool` as `int`. Each trap reading is one a careful implementer could pick.

## Hold-out disclosure

Hold-out path disclosed in committed `frozen-tables.json` (`c2.holdout_dir`): reported under D6. I did not open, list, or use any hold-out path or file. No hold-out content was seen.

## Could not verify

- Hold-out contents, layout and expected outputs (sealed). Whether the hold-out layout matches the committed one, which decides whether D1 reaches 8/8.
- `quality/r55_ctl_c2.py` and a full run of `check-r55-controls.py --claim c2` (module absent). The sibling demonstration reproduces the fixture loop (argv from args.json, cwd = exported tree, byte compare), not the harness.
- The reference implementation and its behaviour on Table A.
- The D5 literal-reading trace was done by hand, not by running a literal implementation.
- `tools/mado-kbdopts.py` is not in the tree; nothing was run against it.

## Tooling

None installed or updated. Python 3 `-I` only. No pacman, uv or npm action.

## Checks the main agent should run

- `python3 -I quality/check-r55-controls.py --claim c2 --repo . --rev <rev> --work <scratch>` once the harness and tool are committed, after the export is sandboxed (D1/D2).
- Add control `C2-CTL-4 sibling-read` (≤1/26 under the sandboxed export).
- Commit the harness modules, or their sha256, before `.ready`, and have `freeze-verify.py` check them (D3).
- Commit a hold-out manifest (names and hashes, no content) and a commitment self-test vector before reveal (D4, P1/P2).
