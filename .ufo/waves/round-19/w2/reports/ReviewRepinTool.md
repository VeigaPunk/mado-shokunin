# ReviewRepinTool — partial

Scope: code review of `.ufo/waves/round-19/frozen-repin.py` at `01b80946d92b26370d3012a7da655d00dd135154` against CriticC3's circularity point (`w1/reports/CriticC3.md` §6). Two questions: does it let tool output define expected values for new lines, and what would a closure need to accept a re-pin. All scratch under `/tmp/rr`; the lane was not modified except this report. Line numbers below refer to the file as shown by `git show 01b8094:.ufo/waves/round-19/frozen-repin.py`.

Verdict in one line: the script behaves exactly as its own docstring/README claim (every refusal I attacked fired), and its honesty framing is accurate — but CriticC3's circularity point is **confirmed empirically and extended**: expected values for flipped and new lines are tool-defined through three paths, one of which produces **no disclosure at all**, and one flag-free path can pin a semantically wrong class on a known-miss line. The **landed r19 baseline itself passes a strict closure**; the mechanism does not enforce one.

## 1. What the script does enforce (all verified true)

Protocol-compliant toy tools (implementing `--scan` and `--frozen` per the schema checks in `parse_verdict`/replay) were run against the real script bytes (`sha256 7cc8b2cd…`, staged from the commit) with `--from` a byte-exact copy of the 9c54c56 r18 frozen baseline (expected `4f3534ae…`, 8 rows + 3 known misses).

- Dropping/rebasing a source row is refused: toy emitting `pacman:-Sw`→different rule on `r14-review-source-bar:1` → `refused`, `source_finding_missing` (4-tuple multiset, script:472,483). No DIR created (verified `outD` absent; refusal paths never publish — `os.replace` only on success).
- A finding on a line neither expected nor known-miss is refused without the flag: `finding_on_unexpected_line` on fabricated `r15:5` (`outA1` refused, DIR absent; script:474-476,486).
- Findings cannot be attributed to other bytes: `parse_verdict` requires every listed input in the verdict `files` with `sha256 == pin` (script `if entry.get("sha256") != pins[rel]`), and replay verifies `tool_sha256`/`expected_sha256` equality.
- Refusal detail discloses rows; `target_written: false`; exit codes match docstring.

## 2. Attack results — three tool-defines-truth paths

### P1 — `--allow-new-findings`: fabricated line accepted verbatim (disclosed)
`--allow-new-findings` + toy emitting `inputs/r15-libinput-events.jsonl:5 host_mutation toy-fabricated` → rc=0 `written`; `expected.json` contains the fabricated row verbatim; toy replays it `frozen_match`. Disclosed in emit (`new_findings_accepted`) and README ("accepted by --allow-new-findings"), but class+rule are copied from tool output with zero content check, and the flag is all-or-nothing — no allowlist mechanism.

### P2 — known-miss flip takes any class/rule from the tool, no flag (CriticC3 §6 confirmed)
Toy emitting the 8 source rows plus `inputs/r13-root.jsonl:4 live_probe toy-wrongclass` (the known miss whose note says "wraps a package query") → **rc=0 written, no flag**: `known_misses` drops `r13-root:4` (kept 2), and `expected.json` pins `live_probe/toy-wrongclass` on that line. Code: kept/dropped knowns are keyed on `(file, line)` only (script:478-481); the note is carried verbatim for kept misses but **silently discarded** for dropped ones — never compared to the emitted class. Disclosure is line-level only ("dropped as now-detected: inputs/r13-root.jsonl:4"); no class/rule appears in emit or README.
Consequence: `tw-recall.py` counts **any class** (`hit = {(file,line) …}`, `tw-recall.py:73-74`), so a tool emitting `live_probe` on every miss line scores 6/6 **and one flag-free re-pin makes that state hermetic** (`frozen_match` by the same tool, script:510 `"expected_findings": findings` — tool rows written as truth). This is the laundering step CriticC3 §6 described, now demonstrated end-to-end.

### P3 — row growth on an already-expected line: no flag, **no disclosure anywhere**
Toy emitting the 8 source rows plus an extra row on an already-expected line (`r15:1 host_mutation toy-extra-rule`) → **rc=0 written** with 9 expected rows; `new_findings_accepted: []`; README "findings on lines that were neither expected nor a known miss: 0". The refusal is line-set based (`expected_lines | known_lines`, script:474-476), so extra (class, rule) rows on expected lines pass; emit and README expose only counts (host_mutation 6→7 visible only by comparing counts against the source). The docstring's "expected_findings: every finding the tool reports" documents the behavior, but neither emit nor README flags the growth — a reviewer must row-diff `expected.json` to see it.

### Replay tautology
All three written baselines replay `MADO_TRIPWIRE_FROZEN: frozen_match` with their producing tool. The replay's `tool_sha256` equality check compares the tool against itself by construction (script `frozen.get("tool_sha256") != tool_sha`), so the replay is a change detector with zero correctness content for tool-defined rows — CriticC3 §6's core claim, confirmed.

## 3. The landed r19 artifact vs a strict closure (independent re-run)

- Digest continuity: `sha256(git show 01b8094:tools/mado-tripwire.py) = 367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` == RECEIPT line and `provenance.json:repinned_from.tool_sha256`. `repinned_from.source_expected_sha256 = 4f3534ae…` == sha256 of the 9c54c56 r18 `expected.json`. Recorded argv has **no** `--allow-new-findings` (README "Re-pin:" line, provenance argv).
- Row-level delta r18→r19 (multiset diff of `(file,line,class,rule)`): added = exactly `{r14-source-safety:2 package_query pacman:-Q, r14-source-safety:3 …, r13-root:4 …}`; removed = ∅; `known_misses` ∅; permit/exit/label and inputs byte-identical. This is exactly the pre-declared C3 flip set.
- Non-circular oracle: landed tool `--frozen` on the 9c54c56 r18 baseline → `frozen_verdict_mismatch`, `extra_findings` = exactly those 3 rows, `missing_findings` = [] (`expected_sha256 4f3534ae…`). Symmetrically, base tool `c1ae45a7…` `--frozen` on the r19 baseline → mismatch, `missing` = exactly those 3 rows, extra = []. The round-18 baseline's expectations are receipt-sourced (its README: derived from committed receipts, not by running the tool), so this direction is independent of the re-pin — this is "the change made visible" the SCORECARD pre-registered, and it holds.
- Note-consistency of flipped classes: the r18 known-miss notes quote `pacman -Q hyprland wayland-protocols wayland-utils` (×2) and "wraps a package query in a local helper" → `package_query/pacman:-Q` consistent. The landed flips did not exercise P2's laxness.

## 4. What a closure needs to accept a re-pin

The script enforces only line-level refusals; everything stricter is procedural. A closure should require all of:

1. **No `--allow-new-findings`** (or `new_findings_accepted` equal to an explicit pre-declared allowlist) — P1 kills undeclared new lines only if this holds.
2. **Row-level multiset diff** source→new `expected.json` equals the pre-declared flip list exactly: `added == declared`, `removed == ∅`, `known_misses` delta == declared drops, permit/exit/label/inputs unchanged. (Catches P3, which no disclosure field covers.)
3. **Class+rule of each flipped row derived from the source known-miss note text**, asserted in the closure report — not copied from tool output (P2).
4. **Digest continuity**: RECEIPT/provenance `tool_sha256` == sha256 of `REV:tools/mado-tripwire.py`, argv flag-free.
5. **Independent oracle**: new tool `--frozen` on the old baseline reads `frozen_verdict_mismatch` with extra == declared flips, missing == ∅; symmetric old-tool-vs-new-baseline check (both ran clean for the landed artifact).
6. **tw-recall REV = 6/6 with classes pinned**: the numerator is any-class (`tw-recall.py:73`), so the closure must also assert the emitted class on each of the 6 incident lines equals the note-derived class (true for the landed artifact: r19 expected = 6 host_mutation, 1 live_probe, 4 package_query, exactly the landed scan output).

Script-level hardening that would make this mechanical: refuse row-level (`file,line,class,rule`) deltas outside a caller-declared expected-delta file; require dropped known-miss notes to state a target/justification and match the emitted class; add a `rows_added_on_expected_lines` field to emit/README.

## Findings by severity

- **High (measure, not instance)**: confirmed circularity with an operational laundering path — P2 lets a wrong-class tool flip a known miss flag-free and `tw-recall.py` still credits it (`tw-recall.py:73`), and the re-pin then enshrines the wrong class (`frozen-repin.py:478-481,510`). Evidence: `/tmp/rr/outB/expected.json` (`r13-root:4 live_probe toy-wrongclass`), emit `known_misses_dropped`.
- **Medium**: P3 — silent expected-set growth on already-expected lines with no flag and no disclosure field (`/tmp/rr/outC`; emit `new_findings_accepted: []`, README outside count 0).
- **Medium**: P1 — `--allow-new-findings` is all-or-nothing with no allowlist; fabricated rows are written verbatim from tool output (`/tmp/rr/outA2`).
- **Low/cosmetic**: `validate_source` accepts empty `rule` in source rows while tool rows must be non-empty; dropped known-miss notes are not echoed into the new provenance (only kept ones survive verbatim), so the discarded claim ("TwMissHelperFn target" etc.) leaves no trace in the artifact.
- **Confirmed-held**: every documented refusal fires (source-row multiset, unexpected line), refusals leave no DIR, staging is cleaned, files-digest binding and replay digest checks work as claimed.

## Limits

- Toy tools are protocol-compliant black boxes built from the schema checks in the script, not the real classifier; they demonstrate what the script accepts, not what the landed tool emits. The landed tool's actual emission on the pinned bytes was verified directly (11 rows = r19 `expected.json`).
- I did not audit `mado-tripwire.py`'s own `--frozen` comparison logic beyond using it as the oracle; the toy `--frozen` implementations are minimal.
- Scenario P2's wrong class is hypothetical for the landed tool (its emitted classes match the notes); the finding is about the acceptance mechanism.
- Emit JSON quoted from `/tmp/rr/{a2,b,c,d}.out`; transcript truncation trimmed some fields, files retained.
- No fetch receipts: no network calls made.

## Installs

none
