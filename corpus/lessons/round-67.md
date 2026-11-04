# mado round 67 — lesson

author: mado L1, integrated from one w1 wave; outside-lane closure remains authoritative.
date: 2026-11-03
base: 0b28ffb4baac9586566d246c3f0986b2bb650a33
frozen declaration: `.ufo/waves/round-67/claims-declaration-r67.md`, 061dc329b598b2723a224b6c7b305b436946ec91.

## Outcome and boundaries

Two bounded claims, both frozen before candidate construction:

- **C1 calibration — register citation-to-live-object discrimination.** At the measured
  revision, `quality/counters/c1-r67-register.py` accepts the committed PROVINCE
  returned-host register block and scores 6/6 on the frozen six-case control set; a case
  is correct only when the counter's accept/reject verdict equals the case's frozen
  expectation, and the register block must cite the live receipt path inside a table row's
  receipt cell. The superseded r66 counter scores 4/6 on the same cases.
- **C2 operability — zero-citation and replacement-ref controls.** At the measured
  revision the standing landing instrument's selftest is green and its new control set
  kills both named defect mutants: M-Z (the zero-citation guard clause removed from the
  citecheck marker contract) and M-R (the `GIT_NO_REPLACE_OBJECTS` guard removed from the
  git-reading landing child). The pre-r67 tip leaves both untested — `zero_citation_case=0`,
  `replace_ref_case=0`, its selftest green, its child reads a planted replacement — so
  baseline killed = 0/2.

Pre-freeze baseline `.ufo/waves/round-67/control-baseline-r67.txt`, committed at
`aa7fe5a1caffe25322cd76ed44b10636cc69f32b`: C1 exit 0 with `correct=4/6`; C2 exit 1 with
`selftest_rc=0`, `killed=0/2`. Controls frozen at the same commit
(`.ufo/waves/round-67/controls/c1-controls.json`, sha256
`45ce81ff450cb4e2786203cc96fc174855f3bd6de7004db9fcfbdee09a89cdfe`).

**Not claimed.** Truth of any state cell; universal fault coverage; honest or authenticated
invocation; protection against a repository already rewritten; desktop/surface health; any
`[x]`, promotion or axis retirement. Both claims are finite-control claims and no wider
guarantee is read out of a green count. Seat and wave demonstrations are not the committed
revision measurement; the L1 landing block below carries `TBD-INTEGRATION` for those values.

## Mistakes

| mistake | class | evidence | captured-by | fix and failure it can now show |
|---|---|---|---|---|
| M67-1: r66 froze a child marker literal from memory (`MADO_TOOL_LEDGER`) although the child emits `LEDGER:`; the declaration text was not amended and an erratum carried the correction. | stale-premise | `corpus/lessons/round-66-verifier-spotcheck.md:32-37` (outside conformance defect 1); `.ufo/waves/round-66/marker-premise-erratum.md`; actual emission `quality/check-tool-ledger.py:350,368` at `0b28ffb4` — `git show 0b28ffb4:quality/check-tool-ledger.py \| grep -c MADO_TOOL_LEDGER` → `0`. | QUALITY 108 (`corpus/QUALITY.md:622-636`, "Read the marker spelling from the child source/output"), added from this r66 defect; the outside spot-check caught it first. | r67 freezes the M-Z literal it deletes from committed bytes: `[ "$citations" -gt 0 ] && ` at `quality/landing-counters.sh:73` @ `0b28ffb4`. The C2 harness must print each mutant diff with its sha256 in the receipt, so a remembered literal that no longer matches yields an empty diff that the receipt exposes instead of a silent kill. Whether an empty diff is itself refused is a landing measurement, not claimed here. |
| M67-2: r66 guarded replacement refs only at the parent export while both git-reading children build env whitelists that drop the key, so the children still read replaced objects; the r66 cutover note read as if the hazard were closed. | landing | `quality/landing-counters.sh:8` (parent `export GIT_OPTIONAL_LOCKS=0 GIT_NO_REPLACE_OBJECTS=1`) versus `quality/check-tool-ledger.py:79,101-110` (`GIT_ENV_KEYS = ("PATH", "SYSTEMROOT")` plus fixed keys, no `GIT_NO_REPLACE_OBJECTS`) and `quality/counters/c3-r56-used-by.py:59-70` (env dict, no `GIT_NO_REPLACE_OBJECTS`) at `0b28ffb4`; baseline `.ufo/waves/round-67/control-baseline-r67.txt:18-19` — `usedby_guard=0 ledger_guard=0`, `child_env_read=forged guarded_read=real`, produced by `.ufo/waves/round-67/controls/score-baseline-c2.py:72-90`; cutover wording `corpus/lessons/round-66.md:91-97`. | QUALITY 72 (`corpus/QUALITY.md:391`): every site that enforces the mutated property is enumerated; a one-site patch over a two-site property is an equivalent mutant. The property here is enforced by each child's git env constructor, not by the parent's export. | r67 adds `GIT_NO_REPLACE_OBJECTS=1` to the git-reading children's env constructors (executor seat `R67ExecChildren`, drafts `draft/quality/check-tool-ledger.py` and `draft/quality/counters/c3-r56-used-by.py`) and M-R deletes that added key line. The failure it can now show is the one the baseline recorded: under the child env shape a planted `refs/replace` rewrites `git show` bytes (`forged` versus `real`), so removing the guard must turn the R case nonzero while the unmutated candidate stays zero. Counted only when killed=2/2 at the measured revision. |

A fix counts only on its named red/green evidence. M67-1's "empty diff is refused" clause and
M67-2's kill count are landing measurements; neither is asserted from the baseline.

## Gate

Admitted: **S436**, scoped to the lane's replacement-ref control — not a desktop fact.
Row drafted this round by the knowledge scribe (`R67ScribeKnowledge`), with the source
independently opened by `R67ScoutSources` and by this seat; the L1 appends the row bytes.
The scribe records screening 1 opened / 1 included / 0 rejected rows; the reject below is
the scout's screened candidate for the outside read, not a second row.

- Canonical URL: https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc
- Access date: 2026-11-03 (three independent fetches this round, byte-identical).
- Located quote, 21 words, DESCRIPTION lines 34-36 of the fetched bytes:
  "Replacement references will be used by default by all Git commands except those doing
  reachability traversal (prune, pack transfer and fsck)."
- Guard sentence, 16 words, lines 55-56 of the same file:
  "The `GIT_NO_REPLACE_OBJECTS` environment variable can be set to achieve the same effect
  as the `--no-replace-objects` option."
- Version pin: tag `v2.56.0` — tag object
  `2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled commit
  `a018953688f1b10bddf91bff8747068f5f4746a4`; host `git --version` prints
  `git version 2.56.0`. No `latest`/`main` anchor.
- Fetched-bytes sha256: `git-replace.adoc`
  `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631` (5398 B); the same
  tag's `git.adoc` `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`
  (47005 B), whose Environment Variables entry (lines 927-929) reads: "Setting and
  exporting this environment variable tells Git to ignore replacement refs and do not
  replace Git objects." (18 words).
- Row shape: 11 columns, no literal or escaped pipe in any cell; kind `docs`, tier `A`,
  status `mined`, opened `2026-11-03`, recheck `on-release`, used-by
  `corpus/lessons/round-67.md`, `corpus/knowledge/replace-ref-citation-boundaries-r67.md`.
  Next unused id computed from `corpus/SOURCES.md`: no `S436` row and no other row carries
  this canonical URL (both counts 0). Same-repository rows at the tag (S099/S100/S101/S102)
  hold different files: source-family precedent, not a URL duplicate.
- Delivered row draft:
  `.ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/SOURCES-row.txt`, sha256
  `b6e794cc19648d98f9d3f4d35e8dff3882a1856ae33fb3d07335207f6d2adbde` (983 B, one line,
  11 cells, no escaped pipe). Its anchor names the tag and line ranges but no `pin` path
  (the adoc is not in the lane tree), so QUALITY 107's length check reads `eof=unchecked`
  for the row; the line numbers were hand-checked against the fetched bytes and the
  scribe's scratch fixture ran the lane's `check-anchor-cover.py` to
  `rows=8 covered=8 miss=0 verdict=OK`. That is a disclosed limit, not an admitted EOF check.
- Admit for the outside spot-check: open the canonical URL at the `v2.56.0` tag and read
  DESCRIPTION lines 34-36 and 55-56; the quoted sentences are there, the tag is pinned, and
  the host git agrees with the tag.
- Reject (screened, not a row): `Documentation/config/core.adoc` `core.useReplaceRefs`
  @ `v2.56.0` — it says the config value behaves like `--no-replace-objects`, but it is a
  repository/user-config plane value that a fixture repo itself controls, so it cannot bind
  the process-level env guard C2's M-R mutant measures. Flip: a sentence at the tag stating
  env-over-config precedence, or a lane guard that sets both planes. Screened by
  `R67ScoutSources`; the lesson's row list is unchanged.
- Reject (claim, outside read): "the replacement-ref guard proves object authenticity or
  protects a repository already rewritten." The source documents lookup precedence, not
  provenance; no signature, no remote check. Flip: an authenticated object identity path
  that does not read through `refs/replace`.
- Recheck/status cell changes old→new: **none**. No existing SOURCES row cell is edited this
  round; S436 is an append. The r65 live receipt the C1 predicate pins is unchanged:
  `.ufo/waves/round-65/receipts/gate-live-r65.txt` sha256
  `676ba88b484e194d4962ee27d07a54b5b7441a8461256b0f3ea0c83d1910e8ed` (CLEAN line 65,
  `rc=0` line 66), identical blob at base and freeze.

## Frontier and scope

Census start: `.ufo/waves/round-67/census-start-r67.txt`, exit 0, committed at
`aa7fe5a1`; its final line records
`mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`.
Source row count before the round: **372** (`grep -c '^| *S[0-9]' corpus/SOURCES.md`;
every row has 11 cells; ids run minimum S001 to maximum S435 with 5 gaps). One row is
appended this round; the end census and end count are L1 landing measurements
(`TBD-INTEGRATION`), not claimed here.

No knowledge entry claims desktop coverage. The entry draft
`.ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/knowledge/replace-ref-citation-boundaries-r67.md`
(sha256 `a049be86119683dc086b608dcd04ddbe4d21c9310cf19032ec13db6e11736f34`) is lane-tooling
scope: what a `refs/replace` object is, which lane instruments read objects through git and
therefore need `GIT_NO_REPLACE_OBJECTS=1`, and what the R control does and does not prove;
its Scope section disclaims desktop, PROVINCE-truth and authenticity claims. Planned
production path `corpus/knowledge/replace-ref-citation-boundaries-r67.md`.

Assimilation: none in this draft. The connector seat is the only seat that may name one, and
nothing here adopts a sibling theme. No PROVINCE frontier move, no desktop probe, no
compositor/socket/service write, no `[x]` or promotion is part of either claim.

## Controls and limits

### C1 — six frozen cases (finite denominator 6; score `10 × correct / 6`)

| case | frozen expectation | r66 baseline verdict | baseline correct |
|---|---|---|---|
| genuine (committed register, live receipt cited in a row receipt cell) | accept | accept | yes |
| duplicate-heading | reject | reject | yes |
| row-without-receipt | reject | reject | yes |
| file-plane-only tree (live receipt object absent) | reject | reject | yes |
| unreferenced-live-object (real live receipt committed, rows cite file-plane receipts) | reject | accept | no |
| live-in-state-cell-only (live path only in a state cell, rows cite file-plane receipts) | reject | accept | no |

Baseline `4/6` = 6.6667, baseline scorer exit 0, at `0b28ffb4`; target `6/6` with
`register=accept`, exit 0. Limits: the check binds the live path inside a row's receipt
cell, uniqueness of the register heading, and the presence of the exact live receipt line;
it does not bind row truth. A stronger forgery that leaves every committed receipt genuine
but writes false state cells is **not** claimed closed, and a passing count must not be read
as state truth. The kill rule requires the measured revision's counter to print 6/6 and pass
its selftest.

### C2 — two frozen mutants (finite denominator 2; score `10 × killed / 2`)

| mutant | frozen recipe | must show |
|---|---|---|
| M-Z | delete the exact guard clause `[ "$citations" -gt 0 ] && ` from the citecheck marker contract | control run exits nonzero on the mutant; unmutated candidate stays zero; citecheck's own selftest stays green |
| M-R | delete the exact added env key line `GIT_NO_REPLACE_OBJECTS` from the git-reading child's env constructor | same; a planted `refs/replace` must not change the child's verdict |

Baseline `killed=0/2` with `selftest_rc=0`, `zero_citation_case=0`, `replace_ref_case=0`,
`usedby_guard=0`, `ledger_guard=0`, `child_env_read=forged`, `guarded_read=real`. Target:
selftest rc 0 and `killed=2/2`. Limits: exactly these two mutants on these two controls; a
universal fault-coverage claim is forbidden. Marker consistency does not authenticate a
child or prove honest invocation, and the control does not protect a repository already
rewritten. Strengthening the zero-citation guard must not make a legitimate non-empty
citation set red, and the external-path refusal cut over in r66 is not revisited.

## Integration placeholders (L1 landing only)

Remaining `TBD-INTEGRATION` values are superseded by the landing block appended below
by the L1 at integration; the draft's own text is unchanged.
committed C1 printed line (`register=… controls=n/6 … verdict=…`) and C2 printed line
(`selftest=… mz=… mr=… killed=n/2 … verdict=…`) with their exit codes and receipt paths;
final sha256 of `quality/counters/c1-r67-register.py`,
`quality/counters/c2-r67-landing-controls.py`, the cut-over
`quality/landing-counters.sh`, the two child files, and each printed mutant diff; wave
settlement counts and the wave-done receipt; end census and end source row count (expected
one row above 372, measured); the appended S436 row bytes and `corpus/README.md` index row;
and the register block's groups/cited-live values at the measured revision.

## Landing (L1 integration)

Production cutover at `%s`; record landing at the commit that carries this lesson.

- C1 at `%s`: `MADO_R67_REGISTER: register=accept controls=6/6 headings=1 rows=8 groups=8/8
  live-cited=yes verdict=TARGET_MET rev=%s` rc 0; selftest 16/16. The draft's 15 cases plus
  `probe-cell-unresolved` were added at integration for the critic's B3 (the r66 block-wide
  unresolved-receipt invariant had been dropped; a probe-cell dangling pointer was accepted).
  The critic's own replay reports `FROZEN_VERDICT_CHANGES=0` across the six frozen cases, and the
  committed register still accepts.
- C2 at `%s`: `MADO_R67_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2
  verdict=TARGET_MET rev=%s` rc 0; harness selftest 47/47; landing selftest 62/62. Derived
  baseline: the same harness at `0b28ffb4` prints `killed=0/2 ... verdict=TARGET_MISSED` rc 1
  (`measurement-baseline-derived.txt`) — the `baseline=0/2` field in the counter line is the
  frozen label from `control-baseline-r67.txt`, not a re-measurement (critic B6).
- m5 auxiliary probe (connector §6): with a planted `refs/replace` on the `PROVINCE.md` blob, the
  C1 counter still prints `register=accept controls=6/6 ... TARGET_MET` — it reads the real object
  through its own guard. m5 remains outside the frozen six-case denominator.
- Harm watch at the record landing: navigation 79/79, used-by `missing=0`, ledger 110/110,
  citecheck over the round-67 scope resolves, `MADO_LANDING_COUNTERS: GREEN`; census exit 0,
  source rows 372 -> 373. Receipts: `measurement-c1-after.txt`, `measurement-c2-after.txt`,
  `measurement-selftests-r67.txt`, `landing-counters-r67.txt`, `census-end-r67.txt`,
  `sources-shape-r67.txt`, `anchor-cover-r67.txt`.
- Disclosures from the critic, stated not smoothed: (B1) M-R binds the citecheck child, which
  inherits the instrument's parent export in the landing path and is vulnerable only when run
  standalone with a scrubbed env; the landing-path replacement hazard is the used-by/ledger env
  rebuilds, covered by auxiliary probes, not by the bound mutant. (B5) the frozen Z marker text is
  shorthand; the implemented fixture emits the full seven-field marker so the refusal is
  attributable to `citations=0`, not to malformedness. (B9) the counter is stricter than the
  declared kill rule (`bash -n` and `forged_credit` gates). (B4) the axis-posture sentence refers
  to the published base rubrics; the r67 control set is a new finite denominator whose do-nothing
  score is 4/6, not a published base sub-axis. (B7) the baseline scorer's default base was corrected
  to the frozen base at integration. No frozen expectation or predicate sentence changed.

## Record-landing re-run (L1, after the wave settled)

The frozen counters were re-run at the record landing `caf131d6be04dd2ccc742636625c1ce196610522` (receipts committed at `2447048be5467ca0e35928d80aa99c90523a6739`):
C1 `MADO_R67_REGISTER: register=accept controls=6/6 headings=1 rows=8 groups=8/8 live-cited=yes
verdict=TARGET_MET rev=caf131d6be04dd2ccc742636625c1ce196610522` rc 0; C2 `MADO_R67_LANDING_CONTROLS: selftest=0 mz=pass mr=pass
killed=2/2 baseline=0/2 verdict=TARGET_MET rev=caf131d6be04dd2ccc742636625c1ce196610522` rc 0. The default `--round 67` citation scope
now exists (`.ufo/waves/round-67/receipts/round-67-citations.txt`) and the standing instrument reads
`MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0)` at `caf131d6be04dd2ccc742636625c1ce196610522` with navigation
79/79, used-by `missing=0`, ledger 110/110 and every citation resolved. Wave settlement:
`WAVE wave=w1 ready=1 results=present seats=13 dispatched=13 settled=13 verdict=OK` and
`MADO_WAVE_DONE: round=67 waves=1 settled=1 verdict=OK` at `2447048be5467ca0e35928d80aa99c90523a6739` (`wave-done-r67.txt`).
Census exit 0, rows 372 -> 373 (A 358 -> 359, B 7, C 7 unchanged; malformed 0 both ends;
`sources-shape-r67.txt`). The earlier draft-sha statements in this lesson refer to the seat drafts;
the cut-over instrument is `quality/counters/c1-r67-register.py` sha256
`6a902350f2d92f1f0fad9646908f6ea2f3d849faf02f33c9e8b7ecf302a00bbc` (B3 repair included) and the
harness `quality/counters/c2-r67-landing-controls.py` sha256
`a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58`.
