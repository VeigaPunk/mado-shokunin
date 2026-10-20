# ConnFrozenFormats — frozen-format comparison (R18 W1)

Seat: connector (no subagents). Item: compare `.ufo/waves/round-13/frozen`,
`round-14/frozen`, `round-16/frozen` and `tools/mado-action-plan.py run_frozen`
against the context's Tripwire frozen interface: naming/outcome vocabulary,
what to reuse, inconsistencies L1 must resolve. Read-only evidence; no lane
gate executed; no files outside this report written.

Axes named for this item:

- **A1 vocabulary-parseable** — a receipt's outcome token can be extracted by
  the round-17 calibration tooling without special cases.
- **A2 failure-discriminating** — each frozen failure has one reachable name,
  and exit 2 classes do not swallow each other.
- **A3 replay-integrity** — the bytes classified are the bytes hashed, under
  the paths the pin names, at the lines the pin names.
- **A4 pin-expressiveness** — an unreachable pin fails as an *error*, not as a
  mystery mismatch; the pin states exactly what it can prove.
- **A5 regression-budget** — the four round-17 suites stay all-pass while the
  shared selftest path gains a mode.

## 1. Method and read surface

Read: `tools/mado-action-plan.py` (docstring 30-65, constants 89-128,
`_read_regular` 150-186, strict loader 188-221, `run_frozen` 407-480,
selftest 758-858, CLI 873-899); `.ufo/waves/round-13/frozen/{expected.json,
verify.py, gate.sh}`; round-14 pin file; `.ufo/waves/round-16/frozen/{expected,
plan,policy}.json`; round-16 receipts `evidence/action-frozen.json`,
`action-frozen-final.json`, `frozen-tampered.json`; round-17
`evidence/tripwire-r16.txt`, `evidence/frozen-tampered-recut.json`,
`label-check.py`; `tools/mado-tripwire.py` (docstring 1-30, `refuse_path`/
`discover` 678-723, `scan_file` 729-800, `scan`/`emit`/`run_scan` 801-835,
`run_selftest` 837-890, `main` 892-935); `tools/mado-verify.sh:3396-3412`;
`corpus/knowledge/gate-standing-use.md:378-400,438-450`;
`.ufo/waves/round-15/w1/reports/ReviewNoHarm.md:14,29`.

Ran (read-only): `sha256sum`/`cmp` on the frozen copies; the four round-17
tripwire suites. No frozen replay was executed (gate execution is outside this
item; the r13/r14 replay executes bash).

Observed digests this run:

```
962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072  tools/mado-tripwire.py
226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3  tools/mado-action-plan.py
fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207  tools/mado-verify.sh
094bf3a494734e784b9a242e076e5c4f51dd71b355476ed071194a8606ee7591  round-13/frozen/verify.py == round-14/frozen/verify.py
037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569  round-13/frozen/gate.sh (== its pin)
fba82a66… (pin)  round-14/frozen/gate.sh == tools/mado-verify.sh byte-for-byte (cmp: IDENTICAL)
core 9/9 · compound 16/16 · hardening 33/33 · w2-regressions 30/30 (all-pass, tool 962919ce…)
```

## 2. Three generations, side by side

| | r13/r14 frozen | r16 frozen (action-plan) | r18 tripwire frozen (contract) |
|---|---|---|---|
| pin file | `expected.json` with **no schema**; exactly `{inputs, expected_exit, expected_marker}` (`verify.py:64`) | `expected.json`, schema `mado-action-plan-frozen-v1`; keys exactly `{schema, plan_sha256, policy_sha256, expected_finding, expected_exit}` (`:122-128`) | `expected.json`, schema `mado-tripwire-frozen-v1`; `inputs[].path/sha256`, `permit`, `expected_exit`, `expected_label`, `expected_findings`, optional `known_misses` |
| what is pinned | the **evaluator itself** (`gate.sh`, a byte copy of `mado-verify.sh`) + `harness.sh` | **input data only** (`plan.json`, `policy.json`); the evaluator is the *current* tool | **input data only** (`inputs/*.jsonl`); the evaluator is the *current* tool |
| replay | `subprocess.run(["bash", gate, "--regression"], env=MADO_VERIFY_HARNESS=<pinned harness>)`, 900 s timeout (`verify.py:99-135`) | in-process `_evaluate_raw` on the bytes already hashed (`:472-475`) | in-process scan of the listed inputs |
| verdict shape | `MADO_FROZEN: MATCH|MISMATCH|TAMPERED|ERROR` **uppercase**, + `FROZEN_ID: <lowercase token>` (`:49-53`) | `MADO_PLAN: <lowercase finding>` + JSON `mado-action-plan-verdict-v1` with `finding`, `exit`, `action_index`, `action_kind`, `detail` | `MADO_TRIPWIRE_FROZEN: <lowercase outcome>` + JSON `mado-tripwire-frozen-verdict-v1` |
| success criterion | exit + **substring marker** | exact `(exit, finding)` pair equality, pair pre-validated as reachable (`:447-458`) | exit + label + exact **multiset** of `(file,line,class,rule)` + `known_misses` |
| exit-2 classes | `snapshot_tampered` (digest/missing/escape), `frozen_error` (unreadable/malformed expected.json, subprocess failure) | `snapshot_tampered` (digest/unreadable input), `frozen_error` (malformed expected.json **or unreachable expected pair**) | `snapshot_tampered` (digest, missing/non-regular/symlink/absolute/`..`, unlisted `*.jsonl`), `frozen_error` (malformed expected.json), `unpinned_legacy` (entry without sha256) |
| tool provenance | none needed in-band: evaluator is inside the pin | not in the verdict; receipts add `measured_commit` + `action_gate_sha256` (`evidence/action-frozen-final.json:3-4`); also `pristine_digests.expected.json` (`frozen-tampered-recut.json`) | `tool_sha256` and `expected_sha256` in-band; `provenance.json` beside the snapshot |
| selftest | own `--selftest` (assertions) | `--selftest` fixtures incl. `frozen-*` cases (`:758-858`) | `--selftest DIR` gains `mode:"frozen"` cases; self-invokes `--frozen <DIR>/<args[0]>` |

Two facts that shape the whole comparison:

1. **r13/r14 pin the evaluator; r16/r18 pin only data.** That is why r16/r18
   need `tool_sha256`/`measured_commit` at all, and why the round-17 defect
   (tripwire receipts carrying no tool sha) is possible: the snapshot cannot
   name the code that produced its verdict, because the code is not in it.
2. **r14's pinned evaluator is byte-identical to today's live gate**
   (`cmp` IDENTICAL; already recorded at `round-15/.../ReviewNoHarm.md:14,29`).
   So r14's `frozen_match` says nothing about any *other* revision, and the
   `git -C "$tree" show … | sha256sum` pipeline at
   `tools/mado-verify.sh:3406` (R17-F10) sits inside the r13/r14 snapshots too
   (`grep -c 'show "HEAD:'` = 1 in each). A later live fix will diverge from
   those snapshots **by design**; they must not be re-pinned to follow it, and
   they are not a template for round 18.

## 3. What is aligned and should be kept

- The lowercase quartet `frozen_match` / `frozen_verdict_mismatch` /
  `snapshot_tampered` / `frozen_error` maps to 0/1/2/2 identically in r16 and
  the r18 contract. Keep this exactly.
- `--frozen DIR` as the flag name (r16 → r18); r13/r14's positional root was a
  one-off. Keep the flag.
- A dedicated verdict schema per tool (`mado-action-plan-verdict-v1`,
  `mado-tripwire-frozen-verdict-v1`), not one shared mutable schema.
- In-process replay of the already-hashed bytes (r16 `:472-475`) — the only
  design that makes a digest pin mean anything.
- Strict JSON at the pin boundary: duplicate keys, non-finite constants,
  non-regular inputs (`action-plan:150-221`). The tripwire already does this
  for transcript lines (`reject_constant`, `:723-735`) but **not** in
  `run_selftest`'s `json.load` (`:839`); the frozen `expected.json` loader must
  use the strict path.
- Rejecting unknown top-level keys (`action-plan:421-423`): a typo'd pin key
  must not be silently ignored.
- Validating that the expected verdict is *reachable* before replay
  (`action-plan:447-458`). This is load-bearing, not decoration: the first r16
  receipt is `exit 2 / frozen_error / "expected.json pair 1/'denied_executable:
  sudo' is unreachable"` (`evidence/action-frozen.json`), and after the pin was
  corrected the same command is `exit 0 / frozen_match`
  (`action-frozen-final.json`).
- `MADO_<NAME>: <lowercase token>` on line 1 is the one shape
  `label-check.py:40` (`^MADO_[A-Z_]+: ([a-z_]+)`) extracts from embedded
  `stdout`. The contract's `MADO_TRIPWIRE_FROZEN: frozen_match` matches it;
  the *token* must stay lowercase.

## 4. Divergences / inconsistencies L1 should resolve

Severity: **B** = breaks the round-18 claim receipts (C1/C3) if left open;
**S** = correctness/consistency; **N** = documentation.
Priority if only five land: **I1, I4, I5, I6, I10**; then **I8, I12, I2/I3**;
the rest are lesson/tests material.

**I1 (B) — token casing is split inside the legacy format.** `verify.py:22`
defines lowercase `frozen_match`…, but `emit` prints the **argument** passed by
`evaluate`, which is the uppercase word (`:50` prints `MADO_FROZEN: MATCH`;
the lowercase token is relegated to a third line `FROZEN_ID: frozen_match`,
`:53`). `corpus/knowledge/gate-standing-use.md:389-392` and `:442` cite the
tool's outcome as `frozen_match`. `label-check.py:40` cannot extract
`FROZEN_ID:` at all, so the cited token is not machine-checkable from that
receipt while the parseable line carries a different word.
*Resolution:* round 18 must put the lowercase token on the `…_FROZEN:` line
(the contract already does), and the lesson/receipt must embed raw `stdout`
(not only a parsed JSON) so `label-check` sees it. Do not retro-edit r13/r14
receipts; if the round cites them at all, the lesson says "legacy vocabulary,
uppercase first line".

**I2 (B) — `label` names two different vocabularies in one interface.**
`expected_label` is the *scan* label (`clean|permitted_only|findings`,
`run_scan:826-828`), while the selftest `want_label` in frozen mode is
specified to compare against the *frozen outcome* on the `…_FROZEN:` line. The
existing `want_label` already has the scan meaning (`run_selftest:875-876`,
used by `w2-regressions`). One key, two namespaces, two prefixes.
*Resolution:* keep the contract key (it is pre-registered at `d3a0000`), and
state in the docstring/selftest spec that **in frozen mode `want_label` names
an outcome**; additionally have frozen cases assert the JSON line
(`schema == mado-tripwire-frozen-verdict-v1`, `outcome == want_label`,
`exit == want_exit`) so the case cannot pass on line 1 alone. If L1 prefers a
clean namespace, `want_outcome` is the better name — but then record the
deviation from the pre-registration in the lesson.

**I3 (B) — "want_findings is ignored" is false as implemented.**
`run_selftest:855-856` reads `case["want_exit"]` and `case["want_findings"]`
in one `try`; a missing `want_findings` prints `SELFTEST_SUMMARY: malformed
case` and returns 2 for the *whole suite*. Frozen cases must not be forced to
carry a key the contract says is ignored.
*Resolution:* branch on `mode` before the key reads; frozen requires
`name`, `args` (one element), `want_exit`, and either `want_label`; keep the
scan branch's requirements byte-identical.

**I4 (B) — the contract's verdict has no diagnostics field.** r16 always emits
`detail`, and every r16 frozen receipt in the repo carries the reason
(`frozen-tampered.json` detail "expected.json pair … is unreachable";
`action-frozen-final.json` detail "frozen verdict … matched"). The round-18
JSON lists only `outcome/exit/tool_sha256/expected_sha256/inputs/missing/
extra/scan_exit/scan_label`, so a `frozen_error` (malformed expected.json,
unreachable pin, scan that cannot evaluate) would arrive with **no reason at
all**.
*Resolution:* add a mandatory `detail` string (`""` on match) to the verdict;
it costs one field and keeps the repo's "name the cause" discipline. Without
it, I5/I6 cannot report *which* invariant failed.

**I5 (B) — expected label/exit pair is not validated as reachable.** The
classifier makes exactly three states: `clean`→0, `permitted_only`→0,
`findings`→1 (`:826-828`). `expected_exit: 0` with `expected_label: findings`
is a permanently unsatisfiable pin. r16 rejects the analogous case as
`frozen_error` (`:447-456`).
*Resolution:* pre-validate the pair → `frozen_error` + detail; and
cross-check `expected_findings` against the label/permit: `clean` ⇒ empty;
`permitted_only` ⇒ non-empty with every `class ∈ permit`; `findings` ⇒
non-empty with at least one `class ∉ permit`; every `class ∈ CLASSES`;
`permit ⊆ CLASSES` (empty `permit` is legal here, unlike the CLI, where an
empty `--permit` is `could_not_evaluate` — do not reuse the CLI validator).

**I6 (B) — `frozen_error` vs `unpinned_legacy` is unordered and, read
naturally, `unpinned_legacy` is dead.** The only legacy pin files in the repo
have **no `schema` key at all** (`round-13/frozen/expected.json:1-8`,
round-14 same shape), so "missing key → `frozen_error`" fires first and
`unpinned_legacy` never names the case it was added for (a bare list entry
without `sha256` is a shape nobody has written).
*Resolution:* pin the check order in the docstring:
(1) unreadable/not-an-object → `frozen_error`;
(2) `schema` present and ≠ `mado-tripwire-frozen-v1` → `frozen_error`;
(3) `schema` absent → `unpinned_legacy` when `inputs` is an **object** (the
r13/r14 shape), else `frozen_error`;
(4) `schema` present → `inputs` must be a non-empty list of objects; a bare
string, or an object without `sha256`, → `unpinned_legacy`; a `sha256` that is
not 64 hex chars → `frozen_error` (r16 precedent `:438-442`, and
case-insensitive compare `:468`).

**I7 (S) — line numbering namespace is unstated.** `expected_findings.line` is
a line inside `inputs/<name>.jsonl` (the scanner's own numbering: split on
`\n`, one trailing empty popped, `:740-745`), while `provenance.json` maps
`[snapshot_line, source_line]`. Nothing in the contract says which one the pin
uses; a writer who pins **source** lines gets a mismatch on any non-contiguous
selection, and a re-sliced snapshot silently renumbers.
*Resolution:* pin `line` = **snapshot** line; document it next to
`provenance.json`'s mapping; require provenance entries for every line cited
by `expected_findings` and `known_misses`.

**I8 (B) — path identity and the bytes-scanned seam.** The scanner records
`findings[].file` as the path it was handed (`:786`) and `discover()` adds
directory walking and realpath de-duplication (`:696-723`). The contract's pin
names `inputs/<name>.jsonl`. If `--frozen` reuses `discover()`/`scan_file()`
with joined absolute paths, every finding's `file` is absolute and no pin can
match; if it reopens files after hashing, the digest pin stops describing the
scanned bytes (the exact class of defect R17-V1/V2 is about).
*Resolution:* a dedicated frozen read path that (a) builds the display name as
the literal pin string, (b) reads bytes once, hashes them, and classifies
**those** bytes through a `scan_bytes(name, data)` seam extracted from
`scan_file`, (c) never calls `discover()`/`refuse_path()` (their rejection
reasons differ: `could_not_evaluate` vs `snapshot_tampered`), and (d) does the
symlink/regular check itself so the outcome is `snapshot_tampered`.

**I9 (S) — input-path shape and closure are underspecified.** The contract
forbids absolute, `..`, symlink, missing, non-regular, and unlisted
`*.jsonl` under `DIR/inputs` — but says nothing about nested paths
(`inputs/sub/x.jsonl` escapes a non-recursive closure walk), duplicate entries
for one path, or a symlinked **DIR** itself.
*Resolution:* require `path` to match `^inputs/[A-Za-z0-9._-]+\.jsonl$`;
duplicate `path` → `frozen_error`; resolve DIR once via `realpath`, reject
leaf symlinks, and state that a symlinked DIR is accepted (matches r16's
`abspath` + `O_NOFOLLOW` precedent, and keeps `/tmp` fixtures usable).

**I10 (B) — field values on non-match outcomes are undefined.** The contract
lists the verdict fields but not what they hold on `frozen_error` /
`snapshot_tampered` / a scan that cannot evaluate: is `inputs` empty or
partial? are `missing/extra` empty? is `exit` the frozen exit or the scan's?
*Resolution:* state: `exit` = the frozen outcome's code (0/1/2), **not**
`scan_exit`; `scan_exit`/`scan_label` are `null` until a scan ran; `inputs` is
`[]` on `frozen_error`, per-entry `{path,sha256,ok}` (ok:false on the failing
one) on `snapshot_tampered`, all-true on match/mismatch; `missing/extra` are
`[]` unless a scan ran; `expected_sha256` = sha256 of the `expected.json`
bytes actually read (`null` only when nothing could be read); `tool_sha256` is
always computable from the running file (`SELFTEST_SCRIPT_SHA256` at `:884`
already uses exactly this semantic — reuse one helper, do not define the
digest twice).

**I11 (S) — `tool_sha256` records but does not bind.** `expected.json` has no
tool pin, so a classifier change that flips verdicts is detected
(behaviourally) but a classifier change that preserves verdicts is invisible
by design; conversely nothing stops a re-cut of the *pin file* from carrying a
new tool sha.
*Resolution:* keep it informational (r16 keeps the tool out of the pin file
and records the sha out-of-band; r17's `frozen-tampered-recut.json` achieves
the binding with `pristine_digests.expected.json` + `measured_commit`). The
lesson must say in one sentence: `tool_sha256` is the **file-content sha256**
(`sha256sum tools/mado-tripwire.py`), never a git blob/commit, and a
`frozen_match` proves only that *this* tool reproduces *this* committed pin —
the receipt must pair it with `measured_commit` and `expected_sha256`, and
`provenance.json` is the only link back to the source transcript. Do not add a
tool pin to `expected.json` this round.

**I12 (S) — the emitter and CLI dispatch must not be shared with `--scan`.**
`emit()` hardcodes `MADO_TRIPWIRE:` (`:813-815`); reusing it would print
`MADO_TRIPWIRE: frozen_match`, a token outside the scan label vocabulary.
`main()` treats everything but `--selftest`/`--scan` as usage error
(`:892-903`), and the usage string names only the two modes.
*Resolution:* separate frozen emitter (first line `MADO_TRIPWIRE_FROZEN:
<outcome>`), a `--frozen` branch before the usage guard, and docstring
CLI/exit lines. Note the `--frozen` + `--permit` combination must be rejected
(permit lives in `expected.json`), mirroring r16's `--policy` vs `--frozen`
exclusivity (`:885-888`).

**I13 (S) — selftest stability.** The four round-17 suites parse
`CASE … ok`, `SELFTEST_SUMMARY: k/n passed failed=[…]`,
`SELFTEST_SCRIPT_SHA256: …` (`:886-887`); round-17 harm receipts saved those
lines verbatim. Adding a mode touches the shared argv builder (`:852`) and the
key reads (I3).
*Resolution:* branch only on `mode`; leave the three summary lines
byte-identical; a frozen case's mismatch must count in the same `failed` list,
not a new channel.

**N14 — r13/r14 are two copies of one tool.** `verify.py` is byte-identical in
both dirs (`094bf3a4…`); only the pinned `gate.sh` digest differs. If L1 ever
records the format's history, say "one legacy format, two pins", not two
formats. No action beyond the lesson sentence.

## 5. Reuse checklist (concrete, for TwFrozenMode/RevFrozenContract)

R1. Control-flow skeleton: r16 `run_frozen:407-480` — load → unknown keys →
schema → mandatory keys → types/pin format → read+hash inputs → tamper gate →
classify same bytes → compare → emit. Insert the frozen-specific branches
(closure, `unpinned_legacy`, permit/finding multiset) between "types" and
"read+hash".

R2. `_read_regular` (`:150-186`): `O_RDONLY|O_NOFOLLOW|O_NONBLOCK`, `fstat`
regular check, bounded read, **growth past stat size is an error**. Reuse its
shape for `inputs/*.jsonl`; the tripwire's own `scan_file` uses a plain
`open(path,"rb")` (`:734-738`) which is weaker.

R3. `_parse_json_bytes` (`:201-212`): `object_pairs_hook` rejecting duplicate
keys + `parse_constant` rejecting NaN/Infinity + UTF-8 decode error as
`frozen_error`. Apply to `expected.json` (the tripwire's `run_selftest`
`json.load` does not).

R4. Reachability validation of the expected verdict (`:447-458`) and its
`detail`-carrying `frozen_error`. Extend to the tripwire's label/exit pair and
`expected_findings` references — see the move in §6.

R5. Hash-then-classify the same bytes (`:472-475`), with a comment stating the
no-reopen invariant (the round-18 contract does not say it; r16 does).

R6. Two-line output discipline (`_emit:134-146`), but with the frozen prefix
and the frozen schema; per-outcome field values as pinned in I10.

R7. Selftest self-invocation pattern (`:758-858`): case table with
`(name, dir, want_code, want_finding)` plus a /tmp fixture writer; for
tripwire, `mode:"frozen"` cases invoking `--frozen <DIR>/<args[0]>`, keeping
the summary lines stable (I13).

R8. Receipt shape from r16 evidence (`action-frozen-final.json`): `label`,
`measured_commit`, `<tool>_sha256`, `command` (argv), `exit`, `stdout`
**verbatim**, `stderr`, `expected_exit`, `matched_exit`; add
`expected_sha256`. This is the shape `label-check` can consume and the shape
that closes R17-V1/V2.

## 6. One bounded proposal

**Move: make the pin a validated contract before it is a comparison — one
pre-replay "reachability" phase that rejects unsatisfiable pins as
`frozen_error` (with `detail`), instead of letting them arrive later as
`frozen_verdict_mismatch`.**

Synthesis across the three generations: r16's reachability idiom
(`action-plan:447-458`, proven by a real caught authoring error:
`action-frozen.json` exit 2 unreachable → corrected pin →
`action-frozen-final.json` exit 0) + r18's multiset pin (which can name a file
or a line that does not exist) + the snapshot's provenance numbering (I7).
Concretely, before any scan:

1. `(expected_exit, expected_label)` ∈ {(0,clean), (0,permitted_only),
   (1,findings)}; anything else → `frozen_error`, detail naming the pair.
2. `expected_findings` consistency with label/permit (`clean` ⇒ empty;
   `permitted_only` ⇒ every class in `permit` and non-empty; `findings` ⇒ at
   least one class outside `permit`).
3. Every `expected_findings`/`known_misses` entry: `file` ∈ listed input
   paths; `1 ≤ line ≤ line_count(file)` (count available from the bytes just
   read/hashed); `class ∈ CLASSES`; duplicate `known_misses` line that is also
   in `expected_findings` → `frozen_error` (an entry cannot assert both).

Affected axes: **A4** (dead pins fail loudly, and the pin's meaning becomes
checkable), **A2** (a principled boundary between "pin is wrong" =
`frozen_error` 2 and "verdict differs" = `frozen_verdict_mismatch` 1). Neutral
on A1 (same lowercase quartet, I1 untouched), A3 (no extra reads; the line
counts come from the already-hashed bytes), A5 (one new branch, no change to
the scan classifier or the three summary lines). Does not touch the three
declared claims (C1-C3), the six PROVINCE surfaces, or any routed jj fix.

Evidence this is not theoretical: the r16 pair validator already caught one
real authoring error in this repo's own evidence trail, and the round-18
snapshot writer must hand-write `expected_findings` for real transcript lines
(the highest-risk hand-written artifact in C3).

Risks / anti-goals:
- Over-validation could reject a legitimate pin. The three label/exit pairs
  and the class/permit rules above are *derived from the classifier*
  (`:826-828`, `:801-810`), so they cannot exclude a producible state; do not
  add a rule that is not derivable that way (e.g. do not require a minimum
  finding count).
- Line counts must be computed with the scanner's own numbering (split on
  `\n`, one trailing empty popped, `:740-745`), or an off-by-one rejects a
  correct pin.
- `known_misses` overlap semantics must be stated in the docstring, otherwise
  the check is arbitrary.
- Cost: ~25 lines in `run_frozen`'s validation phase, ~3 lines in the JSON
  verdict (`detail`), and two cases the selftest owner must add (the current
  planned list has only "malformed expected.json"): *unreachable line* and
  *unreachable label/exit*. Those live under
  `.ufo/waves/round-18/tripwire/frozen/` (TwFrozenSelftest's tree — coordinate
  via L1, do not write there).

Verification (runnable, each shown able to fail):
- `/tmp` fixture, `inputs/a.jsonl` valid, `expected_findings[{line: 99}]` →
  `MADO_TRIPWIRE_FROZEN: frozen_error`, exit 2, `detail` names the line; the
  same fixture with the line corrected → `frozen_match`, exit 0.
- `/tmp` fixture with `expected_exit: 0`, `expected_label: "findings"` →
  `frozen_error`, exit 2 (today's naive implementation yields
  `frozen_verdict_mismatch`, exit 1 — the red control).
- The committed
  `.ufo/waves/round-18/frozen-tripwire/expected.json` still returns
  `frozen_match` exit 0 (no regression on the real pin).
- `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/
  {core,compound,hardening,w2-regressions}` → 9/9, 16/16, 33/33, 30/30.
- Receipts for the red and green runs in the r16 receipt shape (§5 R8) with
  `tool_sha256` + `expected_sha256`, so the QUALITY criteria can cite them.

## 7. Not done / boundaries

- No frozen replay of r13/r14 (executes the pinned bash gate; outside this
  item) and no lane gate run. Suite runs above are the only executions.
- No file outside this report was written. No tool installs or upgrades this
  item (nothing needed; curl/uv not used).
- `provenance.json` is not parsed by `--frozen` in the contract and I did not
  propose parsing it: it is a documentary binding for the separate
  provenance-check script, and an unpinned parse inside the tool would add a
  failure mode without adding a guarantee (I11).
