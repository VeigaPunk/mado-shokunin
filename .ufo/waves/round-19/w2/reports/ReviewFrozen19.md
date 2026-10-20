# ReviewFrozen19 — holds

Target: `.ufo/waves/round-19/frozen` at tip `01b80946d92b26370d3012a7da655d00dd135154` (worktree verified identical: `git status --porcelain` empty and `git diff --stat 01b8094…` empty for the frozen dirs, `tools/mado-tripwire.py`, and `HEAD == 01b8094`). The directory exists, is git-tracked, and holds `expected.json`, `provenance.json`, `README.md`, `inputs/` (exactly the 5 listed jsonl, no unlisted file).

## Attack 1 — are the expected values independent of the tool that produced them?

**Answer: no, and the round says so.** They are the tool's own output by construction, with the round-18 baseline as a refusal constraint — not an independent oracle. The round does not overclaim this:

- `frozen-repin.py:27-30` (docstring): "Expected findings are therefore the tool's own output on these bytes; that proves self-consistency, not that the tool classifies the original incident correctly."
- `provenance.json` `repinned_from.note`: "expected_findings and known_misses re-derived from this tool run".
- `README.md` (frozen dir): "`expected_findings` is the tool's own output on these bytes."

The actual guard chain, verified in code and by probes:

1. **Repin refusal** (`frozen-repin.py:466-502`): `missing = source_counts - got` where both are **4-tuple Counters** `(file, line, class, rule)` (lines 466-468) — a source finding that disappears *or changes class/rule* refuses (exit 1, target never written). `outside` (findings on lines neither expected nor known-miss) refuses unless `--allow-new-findings`. The committed run took no such flag (`README.md` re-pin command has no `--allow-new-findings`; README verdict block: "findings on lines that were neither expected nor a known miss: 0").
2. **Staging integrity** (`frozen-repin.py:455-461`): staged copies re-hashed against pins before the scan; published by one rename.
3. **Exact-reproduction replay**: `tools/mado-tripwire.py:1965-1974` — `--frozen` rescans the pinned bytes and demands exact multiset equality (`missing` or `extra` ⇒ `frozen_verdict_mismatch`, exit 1); input byte drift ⇒ `snapshot_tampered` (exit 2). My independent re-run: `python3 -I tools/mado-tripwire.py --frozen …/round-19/frozen` → `MADO_TRIPWIRE_FROZEN: frozen_match`, exit 0, `expected_sha256=50d2a45e…` = actual sha256 of `round-19/frozen/expected.json`.
4. **Teeth probes** (/tmp copies only): flipping `package_query`→`host_mutation` on `inputs/r14-source-safety.jsonl:2` in `expected.json` → `frozen_verdict_mismatch` exit 1 with `missing=[host_mutation …] extra=[package_query …]`; appending one byte to `inputs/r13-root.jsonl` → `snapshot_tampered` exit 2. The pin detects tool drift and byte drift.

## Attack 2 — class and line vs the round-18 known-miss notes

`round-18/frozen/expected.json` has 8 `expected_findings` + 3 `known_misses` (lines `inputs/r14-source-safety.jsonl:2`, `:3`, `inputs/r13-root.jsonl:4`, prose-only notes naming `pacman -Q` package queries; notes carry no class field).

- **Structured diff r18→r19 expected.json** (only two hunks): +3 findings, all `{"class": "package_query", "rule": "pacman:-Q"}` on exactly the three known-miss lines; the 8 carried findings byte-identical; `known_misses` emptied to `[]`; `permit []` / `expected_exit 1` / `expected_label "findings"` unchanged. No source finding disappeared (the 4-tuple `missing` check would have refused).
- **Line+class agreement with the notes, checked against raw input bytes, not tool output** (python context extraction over the pinned jsonl):
  - `r14-source-safety.jsonl:2` — contains `pacman -Q hyprland wayland-protocols wayland-utils 2>&1 || true` inside a triple-quoted recipe executed via `subprocess.run(["bash","-c",recipe],…)` — matches note 1 verbatim → `package_query`/`pacman:-Q` agrees.
  - `r14-source-safety.jsonl:3` — `recipe2 = recipe.replace("pacman -Q hyprland", …)` re-executed via `subprocess.run(["bash","-c",recipe2],…)`, two `pacman -Q` occurrences — matches note 2 → agrees.
  - `r13-root.jsonl:4` — `run_record('packages',['pacman','-Q','wayland-utils','wayland','wayland-protocols','hyprland'],0)` — matches note 3 verbatim → agrees.
  - Carried anchors re-confirmed in raw bytes: `r15-libinput-events.jsonl:1` `sudo pacman -S --needed … libinput`; `r13-global-capture.jsonl:1` `sudo pacman -S` ×2, `pacman -Q` ×2, `wayland-info` ×6; `r14-review-source-bar.jsonl:1` `sudo pacman -Sw --noconfirm wlr-protocols`.

**Finding W1 (low, process gap — not exploited):** the repin enforces class agreement only on *source-expected* lines (4-tuple `missing`); a *known-miss-line promotion* is matched on `(file, line)` only (`frozen-repin.py:473-481`), so the tool could have promoted e.g. `host_mutation` on `r14-source-safety:2` with no mechanical objection, fossilizing a note-contradicting class (the subsequent `--frozen` pins whatever class was written). Here the classes do agree with the notes (verified above), and SCORECARD's C3 row claims exactly what is true ("the three new findings are `package_query/pacman:-Q`, the class the round-18 known-miss notes name"), so the artifact is correct; the gap is that correctness rests on post-hoc human/verification checks, not the tool.

## Attack 3 — inputs byte-identical to round 18?

**Yes.** All 5 inputs pairwise `cmp`-identical r19 vs r18; sha256s equal across the two trees and equal to the `inputs[].sha256` entries in both `expected.json`s (`7118b883…`, `26552812…`, `4bd77154…`, `8635cca2…`, `24e3c790…`). README input table bytes/lines match `wc -c -l` exactly (11475/5, 14953/5, 34025/5, 28572/6, 47931/5). `sha256(round-18/expected.json)=4f3534ae…` == `repinned_from.source_expected_sha256`; `sha256(tools/mado-tripwire.py)=367be947…` == `repinned_from.tool_sha256` (the merged tool SCORECARD names). `round-19/provenance.json == round-18/provenance.json` plus only the `repinned_from` key (verified by key-stripped deep equality) — `tool_receipt_sha256=962919ce…` (the original round-17 receipt claim) preserved untouched. C3's "6 real incident lines" denominator = distinct `(file,line)` in r18 `expected_findings ∪ known_misses` = r15:1, gc:1, rsb:1, ss:2, ss:3, root:4 = 6 — consistent.

## Attack 4 — the declared visibility change

SCOREBOARD claim "Round-18 frozen baseline now reads `frozen_verdict_mismatch`": independently re-ran `python3 -I tools/mado-tripwire.py --frozen …/round-18/frozen` → `frozen_verdict_mismatch`, exit 1, `extra_findings` = exactly the three promoted rows, `expected_sha256=4f3534ae…`. The change is visible and is precisely the promotion, nothing else.

## Limits

- Coverage hole, documented by the round itself (`provenance.json` `skipped[]`): the `MadoR14.OutputSpec.jsonl:65` `pacman -S` anchor (792,861-byte source line > 256 KiB copy limit) is absent from the frozen replay. No C3 claim rests on it (the 6-line denominator comes from r18 expected.json, which never included that line), but the frozen baseline is not a complete census of round-13..15 incident anchors.
- Expected values are tool-derived by design; "independence" here means the r18 source pin + refusal rules + exact-replay teeth, not an independent oracle. The class/rule semantics of the three promotions were verified by me against raw bytes; the notes themselves carry no class field, so note-class agreement is interpretive (note prose `pacman -Q` → `package_query`/`pacman:-Q`), though unambiguous here.
- Provenance "is the snapshot author's claim, not checked" against the named OMP transcripts (`tools/mado-tripwire.py:94-95`); per host rules I did not open the session transcripts to re-verify the source pairing (`[UNK]` by design, documented).
- W1 above is a latent mechanism gap; no actual instance found.
- Hash-chain claims (e.g. `tool_receipt_sha256` naming the true round-17 receipt bytes) accepted from the committed chain, not re-derived from round-17 artifacts.

## Installs

None. No pacman/uv/npm installs were needed or made; all probes used the repo's committed `tools/mado-tripwire.py` and stock python3.
