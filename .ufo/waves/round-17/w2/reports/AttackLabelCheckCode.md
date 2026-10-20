# AttackLabelCheckCode — round 17 wave 2 (FALSIFY)

Lane HEAD reviewed: `988b858bd6049bc709807534fd725c05264f7e60`. Target root:
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Installs/updates: **none** (host pause
honoured; no pacman/sudo/systemctl/compositor/input probes, no omp processes, no git
mutation). Scratch: `/tmp/lc-attack` only. No delegation.

Bytes reviewed (match the hashes recorded in `.ufo/waves/round-17/evidence/label-check.txt`):

```
b890a5ca771bfbe6af68d07779ea2a9d5f73a5f6481091bb5b5a7f4663a41505  .ufo/waves/round-17/label-check.py
2e28fc841f466b5e1bda4dfcf36a79c05af349ccf836f6d4fd226569f79059d1  .ufo/waves/round-17/label-claims.json
7a567200e07dc3ac3e3bdc883f31d7d13b63ea7d733f4962eae2abbb78a559b6  .ufo/waves/round-17/label-fixtures/want-only.json
```

## Verdict

The shipped run reproduces exactly: `LABEL_SUMMARY: 4/7`, `EXPECT_SUMMARY: 7/7`, exit 1,
and the nine label lines in `evidence/label-check.txt` are byte-identical to a fresh
`python3 -I .ufo/waves/round-17/label-check.py`. The claims file is honest about its own
seven pairs.

The **capability claim is overstated**, though. I built inputs the seven claims do not
cover and got the checker to say `ok` for **14** distinct labels a human would reject
(including two on live round-16/17 evidence), and `MISMATCH` for **3** faithful inputs.
Two more inputs return exit 0 while a declared red control is dead or absent (F3). The worst
gap is not a regex: QUALITY 23 says "the sentence's revision must match [the receipt's
`measured_commit`]", but the checker never reads a revision from the sentence — it compares
the receipt against a field the claims author writes. The exact R16-V1 shape (token
attributed at the wrong revision) can be expressed as a passing claim. Every reproduced
`ok`/`MISMATCH` below is an observed command output, not an inference.

Axes used: (1) false `ok` on a mislabel, (2) false `MISMATCH` on a correct label, (3)
exit-code contract (0/1/2), (4) claim-file integrity/pinning.

## Findings by severity

### F1 — High: the sentence's revision is never compared to `measured_commit`

Anchors `label-check.py:103-104, 129-133`; criterion text `corpus/QUALITY.md:117-118`.
`check_claim` takes `text` from `doc_text` or `git show`, checks basename + token, then
compares the receipt's `measured_commit` to `claim["measured_commit"]`. No code parses the
window for a revision. A claim whose *sentence* names `1e31681` while its `measured_commit`
field is `9dcf248` is accepted:

```
LABEL b1-doc-contradicts-claim ok (receipt outcome carries 'frozen_error')
LABEL_SUMMARY: 1/1
EXPECT_SUMMARY: 0/0 claims met their declared expectation
rc=0
```
(fixture `/tmp/lc-attack/b1.json`, `doc_text: "\`frozen-tampered.json\` (measured 1e31681) records frozen_error"`, `measured_commit: "9dcf248"`, receipt `.ufo/waves/round-16/evidence/frozen-tampered.json@1e31681`)

Live consequence, measured: in `label-claims.json`, `frozen-match-green` carries
`measured_commit: 1e31681` but its cited sentence `corpus/lessons/round-16.md:128-129` at
`27cd06f` contains **no revision token at all** (hex scan of the window: `[]`). The claim is
true, but the criterion's sentence-binding clause cannot bite on it — the field is
author-asserted, not sentence-derived.

**Attacks:** QUALITY 23's "the sentence's revision must match it"; the R16-V1 defect class
at sentence granularity. **Fix:** a claim needs a separate `doc_stated_revision` (or a
regex `(?:measured|at)\s+`?`([0-9a-f]{7,40})` over the window) and the checker must compare
receipt `measured_commit` to that, not to itself.

### F2 — High: `doc_text` silently overrides a real `doc`/`rev`

Anchor `label-check.py:103-104`: `if "doc_text" in claim: text = claim["doc_text"]`, with
no requirement that `doc == "mutant"`. A claim that looks like a pinned citation is never
read:

```
LABEL mask ok (receipt outcome carries 'frozen_match')
rc=0
```
with `{"doc":"corpus/lessons/round-16.md","rev":"27cd06f...","line":1,"doc_text":"\`mc.json\` returns frozen_match",...}`, while line 1 of that document says none of it. The
same construct passes with `doc:"no/such/doc.md"` and `rev:"0"*40` — git is never invoked.

**Attacks:** the doc binding itself; the audit value of the claims file (a reader sees
`doc`/`rev` and believes the document was checked). 3 of 7 live claims use `doc:"mutant"`
+ `rev:"-"`, so they are self-authored text by design; nothing stops a *fourth* from
wearing a real path. **Fix:** reject `doc_text` unless `doc == "mutant"` (and pin mutant
text in a committed fixture), or require `doc_text` to be a *prefix* of the real window.

### F3 — High: expectation failure does not affect the exit code

Anchors `label-check.py:179-187`. `EXPECT_SUMMARY` is computed and printed but never
changes the status. A declared red control that silently turns green exits **0**:

```
LABEL b3-red-control-that-is-green ok (receipt outcome carries 'snapshot_tampered')
LABEL_SUMMARY: 1/1
EXPECT_SUMMARY: 0/1 claims met their declared expectation
rc=0
```

Drop every `expect` key and the gate is vacuously green (`EXPECT_SUMMARY: 0/0`, rc 0). The
live file happens to be 7/7, and QUALITY 23/SKILL.md require that number — but the script
cannot enforce its own documented gate; only a human reading the second summary line can.

**Attacks:** the docstring's "so red controls count" (line 26) and QUALITY 23's
"`EXPECT_SUMMARY` must be 7/7"; a checker invoked without parsing `EXPECT_SUMMARY` cannot
distinguish "verified" from "control lost". **Fix:** exit 1 (or a distinct 3) when
`met != expected` or `expected != len(claims)`.

### F4 — Medium-High: structured want-side `finding` is accepted

Anchors `label-check.py:75-86`. Only *string* values under keys `stdout`/`stderr` are
side-filtered; a nested dict named `want` is recursed like any other dict, so its `finding`
value enters `acc`:

```
LABEL e1-want-json ok (receipt outcome carries 'snapshot_tampered')
rc=0
```
receipt `{"rows":[{"want":{"finding":"snapshot_tampered"},"got":{"finding":"frozen_error"}}]}`.

This violates the tool docstring (`label-check.py:20-22`) and QUALITY 23
(`corpus/QUALITY.md:115-116`, "never want-side text"). The M4 mutation kill in
`w2/reports/MutateLabelCheck.md` only covers the prose form `want N/token`; the structured
form survives the shipped code. It is the natural shape for JSON case receipts (the
tripwire's `expected.json` already separates `want_findings`).

**Attacks:** the stated want-side guarantee; the exact CriticC1 mutant, in dict form.
**Fix:** skip subtrees under keys `want`, `expected`, `expected_*`; accept `finding` only
under `got`/top level.

### F5 — Medium-High: aggregate receipts accept any run's token, including the control

Anchors `label-check.py:75-86, 136`. Tokens are unioned over the whole receipt; there is no
binding to a run, a row, or a headline. Two live receipts demonstrate the lever:

- `.ufo/waves/round-17/evidence/frozen-tampered-recut.json` → `['frozen_match','snapshot_tampered']` (tampered run + untampered control);
- `.ufo/waves/round-16/evidence/action-selftest-final.json` → 11 tokens.

```
LABEL b2-recut-control-token ok (receipt outcome carries 'frozen_match')
rc=0
```
with `doc_text: "the round-17 recut \`frozen-tampered-recut.json\` returns frozen_match"` —
that receipt's headline finding is `snapshot_tampered`; `frozen_match` is the *control* run
(`runs[1].label == "control_untampered"`). The checker cannot tell the receipt's outcome
from one of its control rows. The same pairing at `round-16.md:128-129` for
`action-selftest-final.json` + `frozen_match` also greens.

**Attacks:** token-to-receipt precision; "outcome-side tokens only" is true but too coarse
for the aggregate receipts this round actually produces. **Fix:** optional `run_label` /
`row` selector, or accept only the top-level `finding` plus the first/labelled run.

### F6 — Medium: got-side token vocabulary is truncated at `:`

Anchor `label-check.py:42`: `GOT_SIDE = re.compile(r"\bgot -?\d+/([a-z_]+)")`. Real round-16
selftest rows carry `got 1/blocked_action_kind:package-install`; the capture stops at the
colon (`round-16/w1/reports/SafetyCases.md:104` documents the colon suffix as the finding
vocabulary). Both directions are wrong on the **real** receipt:

```
b6-full-colon  MISMATCH  outcome ['blocked_action_kind', ...] lacks 'blocked_action_kind:package-install'   rc=1
b6-prefix      ok        receipt outcome carries 'blocked_action_kind'                                        rc=0
```
A *correct* full-token citation is red; a generic prefix that does not identify the finding
is green.

**Attacks:** QUALITY 23's "the got-side of a selftest row"; both verdict directions.
**Fix:** capture `[a-z_]+(?::[a-z0-9-]+)?` (and the same widening for `MADO_`/`finding`
values if any verdict word carries a suffix).

### F7 — Medium: `measured_commit` is a degenerate prefix test with no existence check

Anchors `label-check.py:131-132`. `str(got_mc).startswith(mc)`:

- `measured_commit: ""` passes any receipt (`startswith("")` is always true);
- `measured_commit: "d"` passes a receipt measured `deadbeef...`;
- `measured_commit: "deadbeef"` passes a receipt self-declaring
  `deadbeef...` even though no such commit exists in the repo (`git cat-file -e` fails).

```
LABEL b5-empty-measured  ok rc=0
LABEL mc-nonexistent     ok rc=0
```

**Attacks:** "a verdict bound to a commit". A receipt is free-form JSON written by the same
agent; without `git cat-file -e <mc>^{commit}` the revision claim is unverifiable.
**Fix:** reject empty/short prefixes, resolve `mc` to a commit, and optionally require the
receipt's recorded input digest to exist at that commit.

### F8 — Medium: doc stage is co-presence only; receipt identity is basename-only

Anchors `label-check.py:103-118`. The window must contain the basename *somewhere* and the
token *somewhere*, in any order, in any clause:

```
LABEL cross-pair ok  # doc: "`a.json` shows frozen_error; `b.json` shows snapshot_tampered"
                     # claim receipt=a.json (which carries snapshot_tampered)
LABEL basename collision ok  # doc cites `a/x.json`; claim receipt=`b/x.json`
```

Live duplicate basenames exist (`committed-bindings.json` ×4, `cleanup.json` ×2,
`wave-census.json` ×2), but none carries outcome tokens today, so this is latent for the
current evidence — not a live mislabel.

**Attacks:** the sentence-level attribution the criterion is named for. **Fix:** require
the basename and token to occur in the same line/clause (e.g. split the window on `;`), and
match the receipt's repo-relative suffix, not its basename.

### F9 — Medium: `"finding"` inside `stdout` prose is unanchored; a quoted foreign receipt counts

Anchors `label-check.py:81-84`: `FINDING_JSON` is applied to the whole stdout string. A
receipt that prints another receipt (diff, `cat`, a want dump) inherits its tokens:

```
LABEL quoted foreign receipt in stdout ok
```
stdout `$ cat other.json\n{"finding": "snapshot_tampered"}\nMADO_PLAN: frozen_error\n...`.

**Attacks:** "the receipt's recorded outcome". **Fix:** parse stdout line-wise and only
accept `finding` JSON on a line following the receipt's own `MADO_` line, or stop scanning
stdout after the first blank line / shell-echo marker.

### F10 — Medium: doc-token match is substring, not token

Anchor `label-check.py:115` (`token not in window`). With a receipt verdict `ok`:

```
LABEL e14-substring-ok ok
```
doc_text `"\`ok.json\` looks broken"` — the token is found inside "br**ok**en". Receipt-side
membership is exact, so this only bites when the verdict is a common word; `ok`, `fail`,
`pass`, `error` are all plausible verdict words.

**Attacks:** the doc stage's exactness. **Fix:** word-boundary match on the doc side.

### F11 — Low: false `MISMATCH` on input shape

- `OUTCOME_LINE` (`label-check.py:40`) is anchored at column 0: stdout
  `"  MADO_PLAN: snapshot_tampered\n"` → `MISMATCH (receipt outcome [] ...)`. Any wrapper
  that indents or prefixes the MADO line is misjudged.
- stdout recorded as a **list** of lines (`{"stdout": ["MADO_PLAN: frozen_error", ...]}`)
  loses every token → `MISMATCH (receipt outcome [] ...)`, because the `stdout`/`stderr`
  branch requires `isinstance(v, str)`.

**Attacks:** correctness in the false-red direction for receipts the round's own tooling can
produce. **Fix:** `^\s*MADO_` and accept `list[str]` (join with `\n`).

### F12 — Low: malformed claims crash with exit 1, contradicting the documented exit 2

Anchors `label-check.py:113, 132, 115`; docstring lines 29-31 promise exit 2 for a malformed
claims file. Observed:

- `measured_commit: 1` → `TypeError: startswith first arg must be str ...`, traceback, **rc 1**;
- `token: 5` → `TypeError: 'in <string>' requires string ...`, traceback;
- `receipt: 5` → `TypeError: expected str, bytes or os.PathLike ...`, traceback.

Also `"line": true` is accepted as line 1 (bool is int). A consumer that maps 1 to
"mismatch" cannot distinguish a crash from a red claim.

**Attacks:** the exit-code contract. **Fix:** validate types up front and route to the
documented UNEVAL path.

### F13 — Low (hardening): `rev` is interpolated into `git show` as an option

Anchor `label-check.py:55-58`: `["git","-C",root,"show","%s:%s" % (rev, path)]` with no
`--end-of-options` and no leading-dash rejection. Demonstrated:

```
git_show(root, "--output=/tmp/lc-attack/pwn", "x")  -> returns ''  (rc 0)
file created: /tmp/lc-attack/pwn:x  size 334536  content = HEAD commit
```

A claims file can create a file at a chosen path prefix (the `:<doc>` suffix is appended)
and the checker reports only an evaluation result. Impact is bounded (content is the repo's
HEAD, suffix forced), but the write happens before any verdict. **Fix:** `git cat-file blob`
with `--`, or `git show --end-of-options <rev>:<path>` plus `rev.startswith("-")` rejection.

### F14 — Low (data): `rev_receipt: "HEAD"` is a mutable pin

`label-claims.json:20` pins `want-side-only-mutant` to `HEAD`; the other six claims pin
literal SHAs. The fixture blob is currently identical at `245fd11` and HEAD
(`14483913…`), so the result is right today, but a future commit to the fixture silently
changes this claim without touching the claims file. **Fix:** pin `245fd1149dc…`.

### F15 — Medium (evidence label, C1's own receipt): the recorded commit predates the tool

`.ufo/waves/round-17/evidence/label-check.txt` footer records commit
`245fd1149dc1dbee1cc1db849b43035ba5ff54c5` plus sha256 of the checker and claims. But:

```
git cat-file -e 245fd11:.ufo/waves/round-17/label-check.py   -> fatal: not in '245fd11'
git cat-file -e 245fd11:.ufo/waves/round-17/label-claims.json -> fatal: not in '245fd11'
git log --oneline -- .ufo/waves/round-17/label-check.py       -> only 3722ba4
```

Both files were introduced by `3722ba4`, the child of `245fd11`. The run therefore happened
in a dirty worktree; the commit line does not name a revision at which the recorded bytes
exist, and only the sha256 lines bind them. The nine label lines *are* reproducible from
HEAD (I reproduced them), so this is a labeling defect, not a false result — but it is
R16-V1's shape applied to C1's own receipt. **Fix:** label the receipt with `3722ba4`
(or record `git describe --dirty` / the untracked-state fact).

### F16 — Low (scope): the checker cannot consume the round's own new receipts

`json.loads` only; the C3 receipts are text:

```
LABEL txt-receipt COULD_NOT_EVALUATE (receipt is not valid JSON)   rc=2
```
(`.ufo/waves/round-17/evidence/tripwire-selftest-core.txt`, lines `CASE … ok`). The round-17
JSON evidence (`oracle-r15.json`, `schema-variants.json`, `tripwire-vs-oracles.json`,
`measure-c1.json`) yields an empty outcome-token set. QUALITY 23's runnable check therefore
covers the round-16 `mado-action-plan` receipt family only; the C3 selftest tallies
(9/9, 16/16, 33/33) cannot be label-checked by it. Not a mislabel, but a capability boundary
the C1 prose does not state.

## Proposed fixtures

All are claims files (run as `python3 -I .ufo/waves/round-17/label-check.py /tmp/<f>.json`);
the two receipts marked **[new]** are proposed fixture files, not installed.

1. `want-json` (**F4**) — **[new]** `.ufo/waves/round-17/label-fixtures/want-json.json`:
   `{"rows":[{"want":{"finding":"snapshot_tampered"},"got":{"finding":"frozen_error"}}]}`
   claim: `{"doc":"mutant","doc_text":"\`want-json.json\` shows snapshot_tampered","rev":"-","line":1,"receipt":".ufo/waves/round-17/label-fixtures/want-json.json","rev_receipt":"HEAD","token":"snapshot_tampered","expect":"MISMATCH"}` → currently `ok` (should be MISMATCH).
2. `sentence-revision` (**F1**) — real receipt, no new file:
   `{"doc":"mutant","doc_text":"\`frozen-tampered.json\` (measured 1e31681) records frozen_error","rev":"-","line":1,"receipt":".ufo/waves/round-16/evidence/frozen-tampered.json","rev_receipt":"1e31681e76b5e7caadd1c749e18669a3632a1c3b","token":"frozen_error","measured_commit":"9dcf248","expect":"MISMATCH"}` → currently `ok`.
3. `doc-text-mask` (**F2**) — `{"doc":"corpus/lessons/round-16.md","rev":"27cd06f5067c3d3540ab9aa7cc734eb8eee162cc","line":1,"doc_text":"\`frozen-tampered.json\` records frozen_error","receipt":".ufo/waves/round-16/evidence/frozen-tampered.json","rev_receipt":"1e31681…","token":"frozen_error","expect":"MISMATCH"}` → currently `ok`.
4. `red-control-dead` (**F3**) — take the live `recut-green` claim, set `expect:"MISMATCH"` → `ok` + rc 0 (`EXPECT_SUMMARY: 0/1`).
5. `recut-control-token` (**F5**) — `{"doc":"mutant","doc_text":"the round-17 recut \`frozen-tampered-recut.json\` returns frozen_match","rev":"-","line":1,"receipt":".ufo/waves/round-17/evidence/frozen-tampered-recut.json","rev_receipt":"fc6f960…","token":"frozen_match","expect":"MISMATCH"}` → currently `ok`.
6. `colon-token` (**F6**) — real `action-selftest-final.json@4bfb236`, token
   `blocked_action_kind:package-install`, `expect:"ok"` → currently `MISMATCH`;
   token `blocked_action_kind`, `expect:"MISMATCH"` → currently `ok`.
7. `measured-empty` (**F7**) — `measured_commit:""` on any receipt → `ok`.
8. `measured-ghost` (**F7**) — **[new]** fixture receipt `{"measured_commit":"deadbeef","stdout":"MADO_PLAN: frozen_match\n"}`, claim `measured_commit:"deadbeef"` → `ok` though the commit does not exist.
9. `cross-pair`/`basename-collision` (**F8**) — two synthetic receipts `a/x.json` and
   `b/x.json` with opposite tokens (harness `/tmp/lc-attack/attack2.py`).
10. `quoted-foreign` (**F9**) — fixture stdout `"$ cat other.json\n{\"finding\": \"snapshot_tampered\"}\nMADO_PLAN: frozen_error\n"` → `ok`.
11. `substring-ok` (**F10**) — fixture receipt `{"stdout":"MADO_CHECK: ok\n"}`, claim token
    `ok`, doc_text `"\`ok.json\` looks broken"` → `ok`.
12. `indented-mado` / `stdout-list` (**F11**) — fixture stdout `"  MADO_PLAN: snapshot_tampered\n"` → `MISMATCH`; `{"stdout":["MADO_PLAN: frozen_error"]}` → `MISMATCH`.
13. `type-confusion` (**F12**) — `measured_commit:1`, `token:5`, `receipt:5` → traceback, rc 1.
14. `option-rev` (**F13**) — `{"doc":"x","rev":"--output=/tmp/pwn",...}` → file `/tmp/pwn:x` created.

## Residual risk and verification gaps

- I reviewed the **shipped bytes**, not the pre-registration spec: the w1 spec only asks for
  `stdout`/`finding` carriers, so F6/F11/F16 are not spec violations — they are places where
  the docstring/QUALITY-23 wording ("the got-side", "outcome") is stronger than the code.
  `.ufo/waves/round-17/w1/reports/RevPreRegistration.md:45` overstates the predicate further
  (it lists `detail`/`verdict`, which the code never collects); a receipt whose only carrier
  is `detail`/`verdict` is a false `MISMATCH`, conservatively.
- The seven live claims are currently evaluated correctly (I reproduced all seven and the
  commit/receipt pairs); none of F1-F14 changes today's `4/7`, `7/7`. They are silent-green
  paths for *future* claims and for any claims file that is edited without re-deriving these
  cases.
- `MutateLabelCheck` (peer) kills four mutations against the seven claims; F4 and F5 show the
  detector they relied on does not cover structured want blocks or aggregate receipts, so
  "4 killed" is sensitivity to those seven inputs, not to the predicate.
- Not tested: other git versions' `--output` parsing (demonstrated on the host's git),
  real receipts from other rounds (none carry extractable tokens), and `measure.py`/tripwire
  (not this item). No lane file was modified by this lane; all fixtures live in
  `/tmp/lc-attack` except the two `[new]` proposals above. `git diff --stat` at review time
  showed four tracked files modified (`corpus/README.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/terminal-route-r17.md`, `corpus/lessons/round-17.md`) — sibling-lane
  edits, untouched by me; all doc reads in this report are by pinned revision, so they are
  unaffected.
