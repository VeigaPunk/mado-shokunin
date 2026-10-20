# RevR17V2Facts — R17-V2 tool-sha citation audit (round 18, wave 1)

Scope: the tool-sha citations in the round-17 report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mado.md` (161 lines, fleet root).
Assignment: verify that report's tool-sha citations against
`git -C <lane> show <rev>:tools/mado-tripwire.py | sha256sum` for `988b858`,
`f71ccbe`, `0ab1ccc`; state which line cites which sha and the label it should carry.
Method: read-only git (`show`, `rev-parse`, `ls-tree`, `git grep`, `archive`),
file reads, and replays of committed tool blobs against committed fixtures in
`/tmp/rev-r17v2`. No transcript was read (not named to this item), no lane gate was
run, no lane file was written, no host/pacman/service command was issued. No tool
was installed or updated.

## 1. Ground truth: tool bytes at each revision

| rev | full revision | sha256(`tools/mado-tripwire.py` @ rev) |
|---|---|---|
| `988b858` | `988b858bd6049bc709807534fd725c05264f7e60` | `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44` |
| `f71ccbe` | `f71ccbe525c7d140e50d37af8973ed23329c2729` | `7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7` |
| `0ab1ccc` | `0ab1ccccaac5421f6e8ff2fe0cd2bcbd4e5bff4c` | `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072` |

Working tree `tools/mado-tripwire.py` = `962919ce…d5aaa072`, and
`git diff 0ab1ccc -- tools/mado-tripwire.py` is empty: the worktree is clean and
pinned to the landed `0ab1ccc` bytes.

## 2. Every sha-shaped citation in the report, and its true referent

Token enumeration over the whole file finds exactly four 8-hex artifact digests
(all other hex tokens are revision abbreviations: 7-char short hashes, plus one
40-char full revision `0ab1ccc…ff4c` at line 3).

| Line | Cited token | Verbatim claim fragment | True referent (verified) | Verdict |
|---|---|---|---|---|
| 3 | `962919ce…` | "`0ab1ccc` fixes a wave-2 regression … regression suite 30/30, tool sha `962919ce…`, receipts re-cut with identical counts" | `tools/mado-tripwire.py` @ `0ab1ccc` = `962919ce…d5aaa072` | **Correct.** Label should read "tool sha @ `0ab1ccc` (lane HEAD)". |
| 76 | `7a98720e…` | C3 row, "After @ `f71ccbe`": "present, sha256 `7a98720e…`; 9/9, 16/16, 33/33, 30/30 exit 0; anchor exit 1, line 54 `call_38165` `sudo` + `pacman:-S`" | `tools/mado-tripwire.py` @ `f71ccbe` = `7a98720e…f31fe7`; **not** the landed tool (`962919ce…`) | **Mixed-state / mislabeled — see F1.** Correct label would be "tool sha @ `f71ccbe` (superseded)" and the count at that rev is 26/26, not 30/30. |
| 80 | `fba82a66…` | "legacy hermetic selftest 372/372 (gate sha `fba82a66…` unchanged)" | `tools/mado-verify.sh` @ `f71ccbe`; identical at `27cd06f`, `988b858`, `f71ccbe`, `0ab1ccc` | **Correct**, and rev-stable. Label should name the file: "`tools/mado-verify.sh` sha (identical across all four revisions)". |
| 20 | `226220ae…` | "control exit 0 `frozen_match`, gate `226220ae…`" | `tools/mado-action-plan.py` @ `0175f13` and @ `0ab1ccc` (matches `evidence/frozen-tampered-recut.json` field `action_gate_sha256`) | **Correct value.** Label "gate" is imprecise; should read "action-plan gate sha (`tools/mado-action-plan.py`)". |
| 75 | `f71ccbe` (not a sha) | "`python3 .ufo/waves/round-17/measure.py REV` (sha256 at `f71ccbe` in `evidence/measure-final.json` run)" | `measure-final.json` has `rev=commit=f71ccbe…` and `c3.sha256=7a98720e…` | **Correct as scoped**, but it is the only measure receipt and it pins the superseded tool; `measure.py 0ab1ccc` reports `962919ce…` (see F1/F2). |

The C3 *implementation* commit's tool sha (`988b858` → `4ced68d3…`) appears nowhere in
the report (F5). No other tool-sha citation exists in the file.

## 3. Findings

### F1 (high) — the C3 row is internally unsatisfiable: its counts come from `0ab1ccc`, its sha from `f71ccbe`

The row reads "After @ `f71ccbe`" (header line 72) yet prints "sha256 `7a98720e…`;
… 30/30 exit 0". Those two halves belong to different revisions and cannot both be
true at any revision.

Evidence:

1. The `w2-regressions` suite grew from **26 to 30 cases** exactly at `0ab1ccc`.
   `expected.json` case counts: 26 @ `f71ccbe`, 30 @ `0ab1ccc`.
   Set difference of case files, `0ab1ccc` minus `f71ccbe`, is exactly:
   `quoted-hash-not-comment`, `escaped-hash-not-comment`,
   `comment-after-separator-is-data`, `redirect-target-before-command`.
2. Replay of committed tool blobs against committed suites (all in `/tmp`, `python3 -I`):
   - `7a98720e` (f71ccbe tool) on the **f71ccbe 26-case** suite → **26/26 ok, exit 0**.
   - `7a98720e` on the **landed 30-case** suite → **28/30 ok, exit 1**; failing cases
     `quoted-hash-not-comment` and `escaped-hash-not-comment`, each
     `want=(1,[('host_mutation','pacman:-Syu',1,'')]) got=(0,[])`.
   - `962919ce` (0ab1ccc tool) on the 30-case suite → **30/30 ok, exit 0**.
   - `4ced68d3` (988b858 tool) on the 30-case suite → **7/30 ok, exit 1** (23 failures).
3. The committed selftest receipt agrees with (2): `tripwire-selftest-w2-regressions.txt`
   has 26 `CASE` lines + `SELFTEST_SCRIPT_SHA256: 7a98720e…` at `f71ccbe`, and
   30 `CASE` lines + `SELFTEST_SCRIPT_SHA256: 962919ce…` at `0ab1ccc`.

Consequence: read under the row's own header, "30/30" is false (the suite had 26 cases
and the sha passes 26/26); read as the landed capability, the sha is false (it is
`962919ce`, and `7a98720e` actually fails the landed suite 2/30). This is R17-V2 in its
strongest form: not merely a stale citation, but a citation pair no revision satisfies.
The three tool shas are behaviourally distinct, so the mislabel is material rather than
cosmetic.

The rest of the row is verified exactly: `tripwire-anchor-r15.txt` yields
`8 findings / 7 distinct (file,line,tool_call_id)` calls, with line 54 `call_38165`
carrying both `sudo` and `pacman -S --needed --noconfirm libinput libinput-tools`;
`git show 27cd06f:tools/mado-tripwire.py` fails (rc 128, "exists on disk, but not in
'27cd06f'"), so the "absent" before-state is correct.

### F2 (medium) — the six real-transcript receipts carry no tool identity

For `tripwire-r13.txt`, `tripwire-r14.txt`, `tripwire-r15.txt`, `tripwire-r16.txt`,
`tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt` the committed receipt JSON keys
are `{schema, counts, exit, files, findings, permitted, unpermitted}`. There is **no**
`tool_sha256` and **no** `measured_commit`. The per-entry `sha256` values are digests of
the *input transcripts*, not of the running tool.

Contrast with receipts that do pin the tool at `0ab1ccc`:
`tripwire-selftest-{core,compound,hardening,w2-regressions}.txt` carry
`SELFTEST_SCRIPT_SHA256: 962919ce…d5aaa072`, and `tripwire-vs-oracles.json` carries
`"tool_sha256": "962919ce…d5aaa072"` (it was `7a98720e…` @ `f71ccbe`). So the landed
tool identity is recoverable from two receipt families, but not from the real-transcript
receipts — the family the lesson's re-cut sentence is about. A reader of the six
transcript receipts cannot tell which of `4ced68d3`/`7a98720e`/`962919ce` produced them.

### F3 (medium-low) — the real-transcript "re-cut" left no git-visible trace

All six real-transcript receipts are the **same git blobs** at `f71ccbe` and `0ab1ccc`:

| file | blob @ f71ccbe | blob @ 0ab1ccc |
|---|---|---|
| tripwire-r13.txt | `89cfec0edc2c` | `89cfec0edc2c` |
| tripwire-r14.txt | `a31e9d603503` | `a31e9d603503` |
| tripwire-r15.txt | `cd5cce12f956` | `cd5cce12f956` |
| tripwire-r16.txt | `0fc38294a107` | `0fc38294a107` |
| tripwire-anchor-r15.txt | `dc0e7409b428` | `dc0e7409b428` |
| tripwire-pacmanlog-join.txt | `3dd1b046f888` | `3dd1b046f888` |

`corpus/lessons/round-17.md:176` asserts "all real-transcript receipts re-cut with identical
counts". For these six, the claim is unverifiable from git: no content delta, no tool
digest inside, no `measured_commit`. Two readings survive — the re-cut reproduced
byte-identical output, or no re-cut occurred — and git cannot distinguish them.
(Reproduction is plausible: the quote-aware change only alters parsing of lines
containing a quoted/escaped `#`, and aggregate counts are unchanged; but that is
inference, not a receipt.)

Related precision issue: report line 3's flat phrase "receipts re-cut with identical
counts" is only true if scoped to the real-transcript family. The four selftest receipts
did change content, and `w2-regressions` changed **counts** (26 → 30). The lesson scopes
the claim correctly ("real-transcript receipts"); the report's line 3 does not.

### F4 (low) — the lesson's list of the four new cases is wrong in two of four slots

`corpus/lessons/round-17.md:174-175` says "four new regression cases (quoted, escaped,
mid-word, real comment)". The committed suite diff shows the four added cases are
`quoted-hash-not-comment`, `escaped-hash-not-comment`,
`comment-after-separator-is-data`, `redirect-target-before-command`.
`midword-hash-not-comment` and `real-comment-is-data` already existed at `f71ccbe`, and
`redirect-target-before-command` — a genuine new case — is not mentioned. The "30/30"
figure in the same sentence depends on which cases exist, so this is a checkable
inaccuracy in the sentence that carries the tool sha.

### F5 (low) — the C3 implementation commit's tool sha is cited nowhere

`988b858` is named in the report's commit table as "C3: tripwire tool, suites,
real-transcript receipts, …" but its tool sha `4ced68d3…` never appears in the report.
The C3 tool changed twice after implementation (`4ced68d3` → `7a98720e` → `962919ce`),
and the report exposes only the first endpoint (L3) and the middle state (L76). A reader
cannot reconstruct the provenance chain from the report alone.

## 4. Correction this audit would require (advisory; report not edited)

- Line 76: split the two states, or cite the landed one —
  "present, sha256 `962919ce…` @ `0ab1ccc` (superseded `7a98720e…` @ `f71ccbe`, 26/26);
  9/9, 16/16, 33/33, 30/30 exit 0; anchor …". Keep the verified anchor clause as is.
- Line 3 and lesson 175-176: state that the landed tool is `962919ce…`, that the
  selftest and oracle receipts pin it, and that the six real-transcript receipts are
  byte-identical to their `f71ccbe` blobs and carry no tool digest — i.e. the re-cut is
  asserted, not receipted.
- Line 20: label `226220ae…` as the action-plan gate (`tools/mado-action-plan.py`).

## 5. Residual risk and verification gaps

- The six real-transcript receipts were **not** replayed: their inputs are OMP
  transcripts not named to this item, so I can neither confirm nor deny that the landed
  tool reproduces their counts. I only established that the receipts cannot answer it.
- Aggregate equality across revisions is proven at **blob level**, not by re-execution.
- Behavioural differences between the three tool shas were established on committed
  fixture suites only, not on the transcripts.
- No lane gate was run and no file in the lane was modified; findings rest on committed
  bytes and `/tmp` replays of committed blobs.
