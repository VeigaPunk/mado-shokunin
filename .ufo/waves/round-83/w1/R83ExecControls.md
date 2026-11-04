# R83ExecControls — round 83 / wave 1

STATUS: defect

Axes: carried-control fidelity; mutation-inventory consistency; receipt provenance. This is a scoped evidence report, not an admission vote.

## Method and scope

Read the claims declaration and retained receipts. Parsed JSON control sets and Python assignments using `json.loads`, `ast.parse`, and `ast.literal_eval`; did not import or execute either counter. Immutable inputs were retrieved with read-only `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show dbc09269fe547ab13541e722dd7d2ba33015f348:<path>`. Compared those with working bytes to distinguish the frozen instrument from concurrent L1 changes. No builds, tests, formatters, live host probes, git/jj mutations, installs, or instrument writes. No LSP tool is exposed in this seat; structural parsing required no symbol refactor. No scratch directory was created, so none remains to remove.

## Carried controls

- **C1:** r82 has 47 cases; r83 has 58. The first 47 r83 cases are parsed-equal to the complete r82 `cases` array, in order, with zero changed fields. Frozen r83 SHA-256 is `e4409dabcf74f32307f14b31afb85091bca7d584771076bdb9a3b336bc9512c4`; working bytes matched that snapshot.
- **C2:** r82 has 29 cases; r83 has 31. Among the first 29, precisely index 25, `waybar-pgrep`, differs, and only in `samples` and `negatives`. Every other carried case is fully parsed-equal, including `skill_anchor`; no anchor exemption is needed. The two differing fields are exactly the declared supersession. The sample PID is replaced by fixture PID 4242; the second multi-PID fixture retains its other numeric PID, and refusal/zero/empty cases remain unchanged. No undeclared carried difference was found.
- Frozen C2 r83 SHA-256 is `a0fba389676a87f2ceaf4933535057587b4ba7f1b2e0b63c00de256df3ae3f86`. During inspection, working C2 bytes instead hashed to `22ca4c1c495274f797d1eec8abb804974a02054d55657fd896507d972c05b3bf`: only the new case at index 29, `tray-items`, changed its `negatives` field. The first 29 retain precisely the same declared supersession. This concurrent change is outside the carried prefix; the old receipt does not evidence those changed bytes.

## Mutation inventory versus constants

| Counter | Frozen MUTANTS | Actual MUTATIONS length | Unique names | Working MUTANTS / length |
|---|---:|---:|---:|---:|
| `quality/counters/c1-r83-surface-band.py` | 38 | 39 | 39 | 39 / 39 |
| `quality/counters/c2-r83-runbook.py` | 27 | 27 | 27 | 27 / 27 |
| `quality/counters/c1-r82-allocation-band.py` | 34 | 34 | 34 | 34 / 34 |
| `quality/counters/c2-r82-runbook.py` | 25 | 25 | 25 | 25 / 25 |

The frozen C1 mismatch is the declared clerical defect, not a missing kill: its 39 actual mutation entries all have distinct names. `MUTANTS` is at line 37 and `MUTATIONS` begins at line 40. The target at lines 518–519 requires `killed == MUTANTS`, so 39 kills cannot satisfy the frozen constant 38. The retained measurement correctly reports `TARGET_MISSED`; it must not be described as `TARGET_MET`.

The working C1 assignment already read 39 during this inspection, consistent with the announced L1 correction. Frozen C1 counter SHA-256: `674b3f57f6ee1acf55a925fb4fbd277bb0a72c30db0ab5698a3d13fcf50bd26f`; observed working counter SHA-256: `0d85c11bea2b0313e73caaac86c6bc0ed5614bd5a0f9968bec6a23a93034050f`. The working module contract text still says `mutants=38 killed=38`. No corrected-revision measurement was run here or inferred from the old receipt.

C2 frozen and working counter SHA-256 both: `7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0`.

## Retained control receipts

### `.ufo/waves/round-83/receipts/control-c1-r83-at-base.txt`

100 lines; 58 case rows; 52 `correct=yes`; 39 mutation rows; 36 `killed=yes`. The six failing cases are `extra-dyn-band-top`, `extra-dyn-band-dock`, `extra-dyn-band-explicit`, `extra-dyn-band-bottom`, `extra-dyn-band-zero-alloc`, and `alloc-two-namespaces`. Three mutation rows report `killed=no reason=anchor-absent`: `extra-alloc-ignored`, `bar-band-no-refusal`, and `alloc-resolved-set-bar-only`.

Exact final lines:

```text
MADO_R83_BASE: correct=52/58 rule=held-r82-model(bar-band-only) base_rev=67dd2b667b72f7f72309340d488b355d543841a5 base_sha256=58ef4f6a6887985feee6da223393aef2e91de716d0a340cbdedbed4d91ed1a76
MADO_R83_CONTROL: sha256=e4409dabcf74f32307f14b31afb85091bca7d584771076bdb9a3b336bc9512c4 carried=47/47
MADO_R83_BARFOOT: cases=58 correct=52 mutants=38 killed=36 base_correct=52/58 carried=47/47 tool_selftest=133/133 verdict=TARGET_MISSED rev=67dd2b667b72f7f72309340d488b355d543841a5 tool_sha256=58ef4f6a6887985feee6da223393aef2e91de716d0a340cbdedbed4d91ed1a76
```

Receipt SHA-256: `6ac66189818cf7cbbd924ba567007d328d4c70c7043cf0c6df3fd53957391cc4`.

### `.ufo/waves/round-83/receipts/control-c2-r82-at-r83.txt`

One line, exactly:

```text
MADO_R82_RUNBOOK: ERROR (stage=setup the runbook section carries 0 command rows, frozen target expects 29)
```

Receipt SHA-256: `9c0fdc779d227efafb9eb33a4bf16fc8b91ffe84191b72c754b78aec6cd7efec`. The declaration identifies this as rc 2; the receipt itself does not retain a shell exit status or revision identifier. It evidences the held instrument's section refusal, not successful execution of r83 rows.

## Retained measurement context

- C1 measurement has 100 lines, 58/58 correct cases and 39/39 killed mutation rows. Its exact summary is:

```text
MADO_R83_BARFOOT: cases=58 correct=58 mutants=38 killed=39 base_correct=52/58 carried=47/47 tool_selftest=136/136 verdict=TARGET_MISSED rev=dbc09269fe547ab13541e722dd7d2ba33015f348 tool_sha256=8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207
```

Receipt `.ufo/waves/round-83/receipts/measurement-c1-r83.txt` SHA-256: `5d0b05a5ae6b27582f79672f35d2f4ad6a018690bc02b4325ba40ed6eb1f8f36`.

- C2 measurement has 61 lines and 27 mutation rows, all killed. Its control and summary lines are:

```text
MADO_R83_CONTROL: superseded=waybar-pgrep held-r82-instrument=receipt(control-c2-r82-at-r83.txt; stage=setup rows=0 expected=29)
MADO_R83_RUNBOOK: cases=31 executed=31 matched=31 shapes=26/26 anchors=31/31 rows=31/31 superseded=waybar-pgrep mutants=27 killed=27 verdict=TARGET_MET rev=dbc09269fe547ab13541e722dd7d2ba33015f348 tree=bound
```

Receipt `.ufo/waves/round-83/receipts/measurement-c2-r83.txt` SHA-256: `960a3df8572c0c9d4864cbddeab76b53ebf8a6e6548dd0d482443fc66ded23ec`. These are retained observations, not newly exercised checks.

## Handoff

Only this report was written. No blockers to the assigned comparison. Remaining evidence risk: corrected working constants and changed new-case fixtures are not covered by the frozen-revision receipts. L1 owns declaration/contract reconciliation and post-integration measurement on its selected revision. This seat neither modified instruments nor reran counters.

Report: `.ufo/waves/round-83/w1/R83ExecControls.md`
