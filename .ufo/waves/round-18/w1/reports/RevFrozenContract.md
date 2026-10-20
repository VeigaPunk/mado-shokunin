# RevFrozenContract — tripwire frozen interface, receipt binding, gate-standard parity

Seat `MadoR18.RevFrozenContract` (reviewer, leaf). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only: no lane or sibling
edits, no git/jj write, no host or package command, no tool install, no lane
gate execution. Probes were run only against `/tmp` fixtures and with the
`--scan`/`--selftest` modes on read-only inputs (see Verification gaps).

Reviewed at the time of writing:

- the context's frozen-interface text;
- `tools/mado-tripwire.py` sha256 `c87a31ef…de59b4bb` (1181 lines; frozen block
  `:846-1055`, selftest branch `:1058-1131`, `main` `:1133-1180`);
- `.ufo/waves/round-18/tripwire/frozen/` (17 cases, sha256 `a75f4db4…a2522d5`);
- the landed baseline `.ufo/waves/round-18/frozen/`
  (`expected.json` sha256 `4f3534ae…98fd2ed9`, `provenance.json` sha256
  `4fb06b6e…41ff6310`, 5 inputs, 26 lines, 8 expected findings, 3 known misses;
  all files untracked at review). The directory was moved from
  `frozen-tripwire/` to `frozen/` after my first read (same expected,
  provenance and input digests) so it resolves under PROTOCOL's
  `.ufo/waves/*/frozen` root (CriticC3 X9). The registry draft,
  `ScoreResultsDraft.md` and `ReportSkeleton.md` still cite the old
  `frozen-tripwire` path and must be updated to `frozen/` before L1 lands them;
- `.ufo/waves/round-18/receipt-check.py` (`5aec6154…dc7b2`), `receipt-claims.json`;
- `.ufo/waves/round-18/frozen-provenance-check.py` and its report;
- `drafts/SkillRegistryDraft.md:12` (the `mado-tripwire` row);
- PROTOCOL.md §Gate standard (`:388-437`), especially Verdict `:393-397`,
  Self-test `:398-402`, Two evidences `:403-410`, Registry `:411-419`.

Sibling reports already cover parts of this ground: `CriticC3.md` (X1, X3-X6,
X9, X10), `TwFrozenMode.md` (author decisions), `TwFrozenSnapshot.md`
(selection), `FrozenProvenanceCheck.md` (declared-pairs limit), `ReceiptCheck.md`
(its own limits). This report never restates a finding as new when it is
theirs; it records agreement, adds the missing contract detail, and states the
receipt that makes the gate claim checkable.

## Verdict

**Mechanics: sound. Gate conformance: not yet.**

The core replay is implemented correctly for the failure modes the round-17
defect named:

- `expected.json` bytes are read once, sha256'd (`expected_sha256`), and parsed
  from the same bytes; shape/type errors return `frozen_error` exit 2 before any
  input is touched (`:992-1011`).
- Input path checks (`absolute`, `..`, `lstat` symlink, non-regular, missing,
  unlisted `*.jsonl` under `DIR/inputs`) return `snapshot_tampered` exit 2 before
  digests (`:928-990`); an entry without `sha256` returns `unpinned_legacy`
  exit 2; digest mismatches return `snapshot_tampered` (`:969-989`).
- Only then are the listed inputs scanned in-process with `scan_file`; the
  finding `file` is rewritten to the listed relative path, so the multiset key
  is the expected spelling (`:1016-1036`).
- The post-scan `entry["sha256"]` check catches a file changed between the
  digest pass and the scan (`:1021-1024`); the two-read window therefore fails
  closed, not open.
- Outcome→exit is frozen-only (`frozen_match` 0, `frozen_verdict_mismatch` 1,
  every other outcome 2), so a matching snapshot whose scan exit is 1 (as the
  real one is) still exits 0 (`:851-871`); the scan exit is reported separately
  as `scan_exit`/`scan_label`.
- The top-level catch-all now emits the frozen shape for `--frozen`
  (`:1172-1177`), and a missing `want_label`/unknown mode is a malformed suite
  (`:1068-1087`).
- A copy of the 17-case suite under `/tmp` passes 17/17 under `c87a31ef`
  (`SELFTEST_SCRIPT_SHA256` printed that sha); the author reports 88/88 on the
  four round-17 suites, unchanged.

What blocks the `probe → gate` move is not the replay mechanics. It is that (a)
the **revision/expected binding is not yet a committed artifact**, (b) the
snapshot is a **curated sample whose completeness is unverified and unstated in
its machine-readable provenance**, and (c) several **type-valid but vacuous
baselines currently certify green**. Findings below, then the receipt contract
that closes (a), the selection statement that bounds (b), and the small failures
that close (c).

## Findings

Severity is about false-green risk and gate-conformance, not style.

### F1 — HIGH — the receipt does not yet bind `expected_sha256`, and no frozen
receipt/claim exists

The frozen verdict prints `tool_sha256` and `expected_sha256` (`:854-869`) but
cannot name a revision; PROTOCOL `:406-408` requires the committed evidence to
name the revision measured. The receipt-check (`receipt-check.py:86-104`) binds
only `tool_sha256` to `sha256(git show measured_commit:tool)`; it never checks
`expected_sha256`, the input pins, the provenance, the verdict, or
`measured_commit` ancestry. `ReceiptCheck.md` §Risks states exactly this limit.
`receipt-claims.json` contains the six round-17 receipts, three fixtures, and six
`PENDING-L1` re-cut placeholders — **no claim for the round-18 frozen receipt**.

Consequence: a receipt that names the right tool sha and commit still does not
bind the expected verdict. A coordinated rewrite of `expected.json` (permit,
label, known misses, notes) with unchanged inputs passes the frozen run and
would pass the current checker, because only the tool sha is compared.

Additional cross-binding hazard, specifically R17-V2: the landed
`provenance.json` records `"tool_receipt_sha256":
"962919ce…d5aaa072"` — the **derivation** tool that produced the round-17
receipts from which the expected findings were transcribed. The **replay** tool
is `c87a31ef…`. Both are true statements about different events. A receipt that
copies `962919ce` into `tool_sha256` while naming the commit that contains
`c87a31ef` reproduces the round-17 cross-binding defect exactly. The receipt has
to distinguish `tool_sha256` (replay, must equal the blob at
`measured_commit`) from `derivation_tool_sha256` (optional, `962919ce`, with its
own commit, currently `d9a5a18`/`refs/heads/master` blob).

Required (details in “Receipt contract”): commit the tool + snapshot +
expected + provenance first; cut the frozen receipt from `git archive` of that
commit; add a real claim to `receipt-claims.json`; extend the checker to verify
`expected_sha256` (and input/provenance pins + verdict) at `measured_commit`;
require `measured_commit` to be a full 40-hex ancestor of
`refs/heads/master`. The `SkillRegistryDraft` row must then name the receipt in
its pinned-value cell (today it names only `expected.json`). Until this lands,
the row should not be read as gate-conformant: the Two-evidences clause is
“self-test + frozen run + revision-naming committed evidence”.

### F2 — HIGH — the real snapshot is a curated sample; completeness and rule
coverage are not machine-checkable, and the gate is weaker than its name implies

`TwFrozenSnapshot.md` and `frozen-tripwire/README.md` state the selection: one
incident line per source (R15:54, R13:19, R14:41), the two R14 variable-recipe
known misses, the R13:470 helper known miss, and four clean controls per file.
That is a legitimate *selected* snapshot, and the bytes are faithful. But the
machine-readable provenance records only the mapped pairs and the one declared
skip; `FrozenProvenanceCheck.md` §Risks states the checker verifies “the mapping
provenance declares; it does not infer source lines provenance omits”.

Measured against the five source transcripts (read-only `--scan`, source shas
equal to `session-index.json` for all five, all 26 mapped snapshot lines
byte-equal):

| source | source finding lines | mapped | omitted |
|---|---:|---:|---:|
| `MadoR15.LibinputEvents.jsonl` | 7 | 1 (54) | 6 |
| `MadoR13.GlobalCapture.jsonl` | 11 | 1 (19) | 10 |
| `MadoR14.ReviewSourceBar.jsonl` | 3 | 1 (41) | 2 |
| `MadoR14.SourceSafety.jsonl` | 3 | 0 | 3 |
| `MadoR13.jsonl` | 0 | 0 | 0 |

Totals: 3 of 24 source finding lines are represented; 29 finding instances are
omitted; 5 of 15 distinct `(class, rule)` pairs observed in these sources are
exercised by the snapshot; 10 pairs appear **only** on omitted lines —
`live_probe libinput`, `live_probe hyprctl:version`,
`live_probe hyprctl:instances`, `package_query pacman:-Qi/-Si/-Fl/-Sp/-Ql/-Qo/-Ss`.
`wayland-info` and `pacman:-Q` are covered, but most of the query/probe rule
surface is not.

This does not falsify C3 as written (“a committed snapshot of real incident
transcript lines”), and the real baseline does exercise both a `host_mutation`,
a `live_probe` and a `package_query` rule. It does falsify any reading of
`frozen_match` as “the classifier still reproduces the round-17 transcript
verdict”: a regression in the omitted rules passes green. The registry row’s
limit paragraph must say this, and the provenance/receipt should carry the
selection predicate and the counts so a re-selection that drops incident lines
is visible as a count change, not only as a prose edit.

Smallest correction (choose one):

1. **Expand** the snapshot to all finding lines of the five sources except the
   declared 792,861-byte `OutputSpec:65` skip (the inputs stay small: the
   omitted lines are in the same 0.6-3.8 MB files and the snapshot would grow
   well under the 900 KiB budget already used); or
2. keep the curated sample and record in `provenance.json` (and the receipt):
   `selection` predicate, per-source `source_finding_lines`/`mapped`/`omitted`
   with the omitted line numbers, and a `rule_coverage` table; plus a
   count-reconciliation check that a re-cut still satisfies the predicate. The
   README text alone is not a machine check and is not bound by the pin.

Either way, the registry row’s limit must say “curated sample / change
detector; rule coverage 5/15” (or the new figure), and the round report must not
say “the frozen replay reproduces the round-17 scan”.

### F3 — MEDIUM-HIGH — empty `inputs` certifies `frozen_match` (probed)

`validate_frozen` checks `inputs` is a list but not non-empty (`:884-892`), and
`frozen_snapshot` over `[]` returns clean; the scan loop is empty; the compare
matches an all-empty expectation. Probe:

```
expected.json: {"schema":"mado-tripwire-frozen-v1","inputs":[],"permit":[],
                "expected_exit":0,"expected_label":"clean","expected_findings":[]}
→ MADO_TRIPWIRE_FROZEN: frozen_match   rc 0   scan_label clean
```

`TwFrozenMode.md` lists “An empty `inputs` list is accepted (type-valid)” as a
decision and the author’s `/tmp` matrix includes `empty` → `frozen_match`. This
is a false-green shape a re-pin could drift into (or a coordinated rewrite
could empty, with only the receipt diff to show it). Reject `inputs: []` as
`frozen_error` (“no inputs”) and add a selftest case. The same argument applies
to an `inputs` list whose entries are all duplicates of one file (below); at
minimum one distinct, listed input must be required.

### F4 — MEDIUM-HIGH — `known_misses` can be vacuous, and a non-canonical
spelling bypasses the contradiction check (probed)

`validate_frozen` checks only type/line≥1 for known misses (`:916-925`). The
compare and the known-miss loop use the listed path string verbatim
(`:1038-1046`). Two false greens:

```
(a) known_misses [{file:"inputs/a.jsonl", line:99}] on a 1-line file
    → MADO_TRIPWIRE_FROZEN: frozen_match  rc 0
(b) expected_findings has sudo + pacman:-Syu on inputs/i.jsonl:1,
    known_misses names "./inputs/i.jsonl":1 (same line, non-canonical spelling)
    → MADO_TRIPWIRE_FROZEN: frozen_match  rc 0
```

(a) asserts nothing (the line does not exist); (b) is a self-contradictory
document that should force a re-pin but is not detected because the file string
differs. The real baseline’s three known misses are valid — the lines exist,
are non-blank, and currently yield no finding — so this is interface hardening,
not a defect in the landed snapshot.

`CriticC3.md` X5 covers unlisted-file/out-of-range/unreachable-pair cases via
its T3/T4 and recommends a `frozen_error`; this probe adds the **spelling
bypass** that turns an explicit contradiction into green. Fix in
`validate_frozen` after the input bytes are available: every known/expected
`file` must equal a listed input path (exact or `normpath`-canonical), every
line must be `1..lines` for that input, known lines must be non-blank, and a
`(file,line)` in both `expected_findings` and `known_misses` must be
`frozen_error`. Add selftest cases for each.

### F5 — MEDIUM — baseline authoring errors are graded as a failed verdict, not
could-not-evaluate (probed)

A pin that cannot be compared reads as a red gate:

```
expected_findings file "inputs/ghost.jsonl" (not listed) → frozen_verdict_mismatch rc 1
expected_findings line 99 on a 1-line input            → frozen_verdict_mismatch rc 1
```

`class` outside `CLASSES`, and an unreachable `expected_exit`/`expected_label`
pair (e.g. `clean`/1 or `findings`/0), behave the same. That routes a baseline
typo as a conformance defect against the tool. `CriticC3.md` X5 (T4) reaches the
same conclusion; `mado-action-plan.py`’s `run_frozen` already validates
reachable `(exit, finding)` pairs as `frozen_error` and is the local precedent.
Validate in `frozen_snapshot`/`validate_frozen`: expected `file` ∈ listed,
`line ≤ lines`, `class ∈ CLASSES`, and `expected_label ⇔ expected_exit`
(`clean|permitted_only` → 0, `findings` → 1); also require
`expected_label == "permitted_only"` to imply at least one expected finding and
`permit ⊇` its classes, and `findings` to imply at least one expected finding
with a class outside `permit`. Return `frozen_error` (exit 2), not a red
comparison.

### F6 — MEDIUM — the frozen selftest asserts only exit + first line; the
verdict JSON (and finding ids) are unverified

The frozen branch is `:1093-1102`: it compares `got_exit` and
`out[0] == "MADO_TRIPWIRE_FROZEN: " + want_label`, then `continue`. It never
parses `out[1]`, never checks `missing_findings`/`extra_findings`/`inputs`, and
never checks that the verdict’s `exit`/`outcome` agree with the first line.
`CriticC3.md` X6 demonstrates the consequence: mutants M2 (swap missing/extra)
and M3 (drop `rule` from the key) survive 17/17. The gate standard’s self-test
clause (`:398-402`) asks for a stable expected finding-id; the scan cases get
one, the frozen cases do not — and the gate entry is the frozen mode.

Fix: let frozen cases carry `want_missing`/`want_extra` (exact multisets, same
`(file,line,class,rule)` tuples), assert the second line’s `outcome`, `exit`,
`missing_findings`, `extra_findings`, and `inputs[].ok` vector, and add one
case with the same `class` and a different `rule` (kills M3). Also add a case
with a digest-pinned *invalid* JSONL line (scan raises → `frozen_error` exit 2);
that branch (`:1017-1020`) is currently untested. The suite count is 17 now;
the registry draft must read it from the final `expected.json`, not carry a
placeholder.

### F7 — MEDIUM — tamper diagnosis is generic; `inputs[].sha256` is the pin,
not the observed bytes

All tamper subclasses return `snapshot_tampered` with
`error: "snapshot does not match its pin"` (`:1012-1015`) plus the per-entry
`ok` vector. For an **extra unlisted input**, every listed entry shows
`ok: true` and the message still says the pin does not match (probed):

```
extra inputs/stray.jsonl + valid listed pin
→ snapshot_tampered rc 2, inputs [{"ok": true, ...}],
  error "snapshot does not match its pin"
```

For a **digest mismatch**, `inputs[].sha256` is the pin, not the computed
digest, so the verdict does not show what the tampered bytes hashed to. The
round-16 precedent (`frozen-tampered-recut.json`) records both pristine and
post-tamper digests and a `detail` string. Add `error`/`detail` naming the
rule and offending path (`unlisted <path>`, `missing <path>`, `symlink <path>`,
`path <path>`, `digest <path>: observed <sha> != pinned <sha>`) and/or an
`observed_sha256` per input. The outcome and exit stay as they are.

### F8 — MEDIUM-LOW — the frozen expected verdict does not pin the classifier’s
counting signals

The expected schema has no field for `lines`, `bash_calls`, `eval_calls`,
`eval_unparsed` or `unparsed_spawns`; the compare covers only findings, label
and exit (`:1048-1053`). In the real baseline, `inputs/r14-source-safety.jsonl`
reports `unparsed_spawns: 2` (the two known-miss variable recipes) while
`r13-root` reports 0 (the helper call is not a spawn). A classifier change that
stops recognising the dynamic-spawn forms but still emits the same findings and
label passes `frozen_match`. Given the known misses are exactly the dynamic
cases, add an optional `expected_file_stats` (per input: `lines`,
`unparsed_spawns`, `eval_unparsed`, or a subset) and compare it; or state in the
row’s limit that only the finding surface is pinned.

### F9 — LOW-MEDIUM — the `inputs/<name>.jsonl` shape and closed-set rule are
not enforced

The path check rejects only absolute and `..` (`:940-951`); a listed `a.jsonl`
at `DIR` root is accepted, and because `DIR/inputs` does not exist the unlisted
walk is skipped, so the baseline can evade the extra-input rule entirely
(probed: `{"path":"a.jsonl"}` + `a.jsonl` → `frozen_match` 0). The mode author
records this as a deliberate decision (“the contract constrains paths, not
their parent”); the contract’s schema example and the extra-input sentence are
both `inputs/<name>.jsonl`, so I read it as a shape deviation worth closing.
Also: a symlinked `inputs/` directory is followed (`:955` + `os.walk` root
behaviour; `CriticC3.md` X10 T5), two entries naming the same file are accepted
and scanned twice (`TwFrozenMode.md` footgun), and a listed path that is not
under `inputs/` can name `expected.json` (then scan errors as `frozen_error`).
Require: `DIR/inputs` is a real non-symlink directory; every listed path matches
`^inputs/[A-Za-z0-9._-]+\.jsonl$` (flat); every `*.jsonl` directly under
`inputs/` is listed; reject duplicate paths. Add cases for the top-level path,
duplicate, and symlinked `inputs/`.

### F10 — LOW — a misused `--frozen` emits the scanner shape

`--frozen DIR --permit …` (or `--frozen` with no DIR) falls to the usage branch
and prints `MADO_TRIPWIRE: could_not_evaluate` + the scan schema, exit 2
(probed). The frozen output contract says the first line is
`MADO_TRIPWIRE_FROZEN: <outcome>`. Dispatch usage errors by mode: if
`argv[0] == "--frozen"` but the shape is not exactly `--frozen DIR`, emit
`frozen_error` with the frozen schema. `TwFrozenMode.md` records the same
observation as accepted; it costs little to make the error shape stable for
parsers.

### F11 — LOW — pinned-document parsing accepts ambiguity

`expected.json` is parsed with plain `json.loads(..., parse_constant=...)`
(`:997-1000`): duplicate object keys silently keep the last (a reviewer sees
the first), unknown top-level keys are silently ignored, and a `sha256` string
that is not 64 hex falls through to a digest mismatch (`snapshot_tampered`)
rather than a baseline error. The pin makes the bytes unambiguous to the tool
but not to a human reading the document. Reject duplicate keys via
`object_pairs_hook`, reject unknown top-level keys (precedent:
`mado-action-plan.py`’s `unknown = set(expected) - _EXPECTED_KEYS`), and
validate pins as 64 lowercase hex → `frozen_error`.

### F12 — LOW — evidence/report honesty for C3

- The frozen process exits 0 because it is a **match**, while the real
  baseline’s `scan_exit` is 1 and `scan_label` is `findings`. The round report
  must quote both (e.g. `exit 0 frozen_match; scan_exit 1; scan_label findings`)
  or a reader will take “exit 0” as “nothing in the snapshot”.
- The expected findings were transcribed from round-17 receipts produced by
  tool `962919ce`, not by the current tool (`TwFrozenSnapshot.md`;
  `provenance.json:tool_receipt_sha256`). The replay match therefore proves the
  frozen-mode edit did not change classification **plus** the receipts agree
  with the current tool; it is not an absolute-correctness oracle. `CriticC3.md`
  X2 quantifies the independence (line+host_mutation backed by oracle/pacman.log;
  rule ids are tool vocabulary). Record `derivation_tool_sha256` separately in
  the receipt and keep the limit sentence in the row.
- `README.md`’s re-pin instruction (“re-derive expected_findings … from a
  current-tool receipt”) can make a future baseline self-derived/tautological.
  Require the re-pin to state its independent basis (oracle, pacman.log join,
  or a written review) or record `basis` per expected finding.
- `CriticC3.md` X4: the `MadoR13.jsonl:470` known miss snapshots the invocation
  without its definition (line 437); a definition-aware classifier cannot be
  exercised by this line, so the assertion can only fire on a name-based helper
  rule or a cross-cell resolver. Keep it only with that stated limit, or drop
  it and record “not representable in a line-local snapshot”.

## Receipt contract (what must land before the row is a gate)

This is the concrete answer to “tool sha + measured_commit + expected sha”.
The tool cannot know the commit; the committed receipt must. Keep the tool’s
output factual and put the revision claim in the receipt.

### Receipt files

- `.ufo/waves/round-18/evidence/tripwire-frozen-receipt.json` — the pristine
  run over the committed baseline.
- `.ufo/waves/round-18/evidence/tripwire-frozen-tampered.json` — the
  single-byte tamper on a `/tmp` copy (round-16 `frozen-tampered-recut.json`
  shape: pristine digests, tamper description, post-tamper digest, runs).

### Proposed fields (JSON)

```json
{
  "schema": "mado-tripwire-frozen-receipt-v1",
  "tool": "tools/mado-tripwire.py",
  "tool_sha256": "<sha of the tool blob at measured_commit; the REPLAY tool>",
  "derivation_tool_sha256": "962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072",
  "derivation_commit": "d9a5a18e17cd3a68b52148fcc01c4a30e340ba98",
  "expected": ".ufo/waves/round-18/frozen/expected.json",
  "expected_sha256": "4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9",
  "provenance": ".ufo/waves/round-18/frozen/provenance.json",
  "provenance_sha256": "4fb06b6e42b52d5cb04e6ef8a19b36c2a8851a7bbd47e28e1c846f8941ff6310",
  "snapshot": {"inputs/r15-libinput-events.jsonl": "7118b883…", "...": "..."},
  "measured_commit": "<full 40-hex commit containing the tool, expected, inputs, provenance>",
  "command": "python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen",
  "exit": 0,
  "outcome": "frozen_match",
  "scan_exit": 1,
  "scan_label": "findings",
  "verdict": {"schema": "mado-tripwire-frozen-verdict-v1", "...": "exact second-line object"},
  "created_at": "<UTC ISO-8601 from date -u>"
}
```

The digests above are the values observed at review; re-read them after the
final integration edit and re-cut. The receipt’s `tool_sha256` must be the
replay tool, not `derivation_tool_sha256`; the two must never be conflated
(R17-V2 cross-binding).

### Ordering (non-circular)

1. L1 commits the final tool + `frozen-tripwire/{expected.json,inputs/*,provenance.json,README.md}`
   (commit **A**). The tool is currently uncommitted; a receipt taken now would
   name a tool git never recorded.
2. From a clean materialisation of A, run the gate and write the receipt:
   `git archive A tools/mado-tripwire.py .ufo/waves/round-18/frozen | tar -x -C /tmp/r18-frozen`
   then `python3 -I /tmp/r18-frozen/tools/mado-tripwire.py --frozen /tmp/r18-frozen/.ufo/waves/round-18/frozen`.
   This proves the run is over the committed bytes, not a dirty worktree.
3. Commit the receipt **after** A (commit **B**) with `measured_commit: A`.
   A receipt committed *in* A would have to name itself; do not do that.
4. Add a claim to `receipt-claims.json`:
   `{"id":"r18-frozen-baseline","receipt":".ufo/waves/round-18/evidence/tripwire-frozen-receipt.json","rev":"<B or later>","tool":"tools/mado-tripwire.py","expect":"ok"}`,
   and a negative control for the tamper receipt (`snapshot_tampered` is not
   `ok`; a checker for this needs a verdict/outcome field — see below).

### Checker extension

`receipt-check.py` must verify, at `measured_commit` (not just the tool):

- `tool_sha256` = sha256(`git show A:tools/mado-tripwire.py`);
- `expected_sha256` = sha256(`git show A:<expected>`);
- `provenance_sha256` = sha256(`git show A:<provenance>`);
- every `snapshot[path]` = sha256(`git show A:<path>`);
- `measured_commit` resolves to a full commit and
  `git merge-base --is-ancestor A refs/heads/master` (or the lane’s canonical
  ref; never `@{u}`);
- the recorded `verdict` is byte-equal (or field-equal) to a fresh run from
  `git archive A` of the tool + frozen dir;
- the receipt is a structured object, not a value found anywhere in prose. The
  current regex accepts `"tool_sha256"` anywhere in the receipt text
  (`ReceiptCheck.md` §Risks); a structured JSON receipt plus strict parsing
  removes the self-attestation fallback.
- Use `git show`/`git cat-file` with the producer status captured
  (subprocess return code, or `> tmp && rc=$?`), never `git show … | sha256sum`
  without the producer rc — that is the JjAuditMado F10 shape and would digest
  a failed read as `e3b0c442…`.

The `mado-receipt-check` row is currently a probe with seeded expectations; once
it compares this claim set against committed receipts it meets the gate
definition (committed expected values + verdict), so consider registering it as
a gate rather than a probe, or state why it stays a probe.

### Tamper receipt

Record: `snapshot_source` (the committed baseline), pristine digests of
`expected.json`/the tampered input, the one-byte/token alteration, the
post-tamper input digest, the exact command on the `/tmp` copy, `exit 2`,
`outcome snapshot_tampered`, the tool sha and the source `measured_commit`, and
the `inputs[].ok` vector. That is the “shown able to fail” receipt R17-V5 asks
for; a `/tmp` lab without a committed receipt is exactly the round-17 defect.

## What a coordinated rewrite can still hide (and what the receipt does not fix)

1. **Inputs + expected + digests + findings rewritten together.** The frozen run
   prints `frozen_match` with the new `expected_sha256`; nothing inside the
   frozen dir remembers the old one. The receipt (expected_sha + measured_commit
   + the prior receipt in git history) makes this a *visible re-cut*, not a
   silent edit. It cannot prevent an owner-signed re-cut; only the round report
   and closure review can judge it.
2. **Provenance rewritten alone.** The frozen verdict never reads
   `provenance.json`; the receipt’s `provenance_sha256` plus a committed
   provenance-check run are the only bindings.
3. **Selection shrunk but internally consistent.** Delete an incident line,
   update digests/expected/provenance; `frozen_match`. `FrozenProvenanceCheck`
   verifies the mapping it is given, not that the mapping is complete
   (`FrozenProvenanceCheck.md` §Risks). The counts/selection predicate in F2
   and a source-derived oracle count are the only defenses.
4. **Permit widened.** Expected findings stay; label/exit and expected sha
   change; the receipt diff exposes it. The baseline should keep `permit: []`
   (it does), and any non-empty permit must be a written waiver in the report.
5. **Tool changed.** The frozen verdict may still match if behaviour is
   preserved; without the receipt’s tool sha + measured_commit, a cited tool
   sha can be one git never recorded (R17-V1/V2). With it, the claim is
   checkable; a tool change that preserves the verdict is still a visible new
   tool sha and requires a re-cut.
6. **Empty/vacuous baseline.** Currently green (F3/F4); reject at validation.
7. **Receipt cut from a dirty worktree.** The `git archive` run + `git show`
   hashes prove the committed bytes; a receipt naming A while the run used
   uncommitted bytes is detectable only if A lacks the tool/expected/inputs.
   Require A to contain all four and verify with `git ls-tree -r A`.
8. **Sources rotated or grown.** `FrozenProvenanceCheck` returns 2 when a
   source is gone; then the snapshot is the only copy. The receipt should record
   the source digests and the index sha so a future reader knows what was
   attested when.

## Gate-standard parity (PROTOCOL.md §Gate standard)

| Clause | Status | Required action |
|---|---|---|
| Verdict: 0 clean, 1 failed, other codes declared and mapped | Pass in code (`:851-871`); draft row maps frozen 0/1/2 and scan 0/1/2 separately | Keep the mode-qualified map; ensure `unpinned_legacy` appears in the results text (the pre-registration parenthetical omits it in one place) |
| Self-test over isolated fixtures, asserting exit **and a stable finding-id** | Partial: 17/17 frozen and 88/88 existing (author; my `/tmp` copy 17/17), but frozen cases assert exit + first-line only | Add `want_missing`/`want_extra`/verdict assertions (F6); add scan-error and fixed-shape cases; fill the real count |
| Two evidences: self-test capability + frozen run over a committed snapshot with its committed expected verdict | Not yet: expected/inputs/provenance are untracked; no frozen receipt; receipt-check checks only tool sha; expected sha unbound | Commit A, cut the receipt, extend the checker, add the claim (F1) |
| `expected.json` pins every input digest; verifies before comparing; edited snapshot = `snapshot_tampered` (could-not-evaluate); no digests = unpinned (legacy) | Pass (`:928-990`) | Keep; add non-empty and shape validation |
| A verdict names the revision measured | Missing in the verdict by design; the receipt must | Receipt `measured_commit` + `git show` verification |
| Registry row at `SKILL.md`: name, gate/probe, entry, verdict map, self-test command/spelling, pinned-value path, write scope, owner | Draft row exists (`SkillRegistryDraft.md:12`), mode-qualified; pinned-value cell names only `expected.json` | Add the receipt path/revision binding; `gate` only after F1; full path avoids the `*/*/frozen` bare-name ambiguity; fill count after final run |
| Scope: read-only, never acts externally | Pass: frozen/scan write nothing; selftest reads fixtures; provenance-check reads sources read-only | State the provenance-check’s read of transcripts is outside the gate |
| Closure: integrator verifies committed evidence, does not execute the sibling gate | Pending | The receipt is the artifact L1 verifies; report cites A and B |

## Minimal ordered change list

1. `tools/mado-tripwire.py` (TwFrozenMode):
   reject empty `inputs`; validate `expected_findings`/`known_misses`
   file∈listed, line≤lines, non-blank known lines, contradiction, class∈CLASSES,
   reachable exit/label; enforce the `inputs/<name>.jsonl` grammar and a real
   flat `inputs/` dir; reject duplicates; add `detail`/`observed_sha256` for
   tamper subclasses; mode-aware `--frozen` usage; optionally pin
   `unparsed_spawns`/`eval_unparsed`.
2. `.ufo/waves/round-18/tripwire/frozen/` (TwFrozenSelftest):
   add the assertions and cases in F6 (including a pinned invalid-JSONL scan
   error and the F3/F4/F9 shapes); keep the four existing suites all-pass.
3. Baseline author (L1/owner): expand or document the selection per F2; add
   `selection`/counts/rule coverage to `provenance.json` (or an adjacent
   committed table) and bind it in the receipt; state the placeholder/gate
   limit in the row.
4. L1: commit A; cut the pristine and tampered receipts from `git archive A`;
   extend `receipt-check.py` (expected/provenance/snapshot/verdict/ancestry);
   add the `r18-frozen-*` claims; commit B; re-run the gate and all suites after
   the final edit; fill the row’s count and receipt path.
5. Round report: show `exit 0` **and** `scan_exit 1`/`scan_label findings`; show
   the match and tamper receipts; state the curated-sample/change-detector limit
   and the `962919ce` derivation vs `c87a31ef` replay distinction; do not claim
   absolute correctness or full-transcript coverage.

## Residual risk and verification gaps

- **I did not run the lane gate.** The contract reserves lane-gate verification
  for L1. My evidence is: `/tmp` fixture probes of the frozen interface,
  `--scan` (probe mode) over the snapshot inputs and the five source
  transcripts (read-only; source shas equal `session-index.json`), a byte
  comparison of all 26 mapped lines, and a `/tmp` copy of the 17-case suite
  (17/17 under `c87a31ef`). The real `--frozen` run, the tamper receipt, and the
  four-suite re-run after the final edit remain L1’s.
- **The tool was moving.** Observed shas during the wave were `593b3aaf`,
  `3e791ee`, `762cf56f`, `c87a31ef` (TwFrozenSelftest §2); `c87a31ef` is the
  review sha. Any citation of an earlier sha in a receipt is stale by
  construction. Re-read the final sha, the expected/provenance digests, and the
  input pins after the last edit; re-cut rather than re-label.
- **The snapshot/expected/provenance are untracked**; `measured_commit` does not
  exist yet. All digests in this report are point-in-time and must be re-derived
  on commit A.
- **The gate is a change detector, not an accuracy oracle.** The expected
  findings come from round-17 receipts of the same classifier family; the
  independent backing is strongest at `(line, host_mutation)` (anchor receipt,
  oracle, pacman.log join) and weakest at rule ids and multi-class splits
  (`CriticC3.md` X2). The row must say this; the report must not upgrade
  “match” to “correct”.
- **Completeness is documentation-level unless F2 is implemented.** The
  provenance checker’s own report states it verifies declared pairs only; the
  README’s selection prose is not bound by a digest or a count.
- **Known-miss R13:470** is a line-local invocation of a helper defined in
  another cell (`CriticC3.md` X4). The snapshot can only be violated by a
  name-based helper rule or a cross-cell resolver; a definition-aware tool that
  needs line 437 cannot be exercised. Keep it with that note, or drop it and
  record “not representable in a line-local snapshot”.
- **No host operation was performed** and no tool was installed or upgraded;
  the host pause was respected. No files outside my report were written.
