# ExecC2ExtraMutants — C2 extra mutation/forgery population (round 43, w1)

Seat `ExecC2ExtraMutants`, lane `mado-shokunin`, host 2026-10-26, Hyprland 0.56.2.
Claim attacked: **C2** (`PRED-C2-r43`, `quality/counters/c2-r43-gkeep-entry.py`).
Scope: 72 NEW controls beyond the 74 registered in `.ufo/waves/round-43/ctl/run-c2-controls.py`:
clause mutants and real-seeded forgeries. Nothing frozen was edited; nothing outside this
seat dir was written; the lane index was never touched.

Status: **complete**. Verdict of this seat's sweep: **PASS** — 63 controls rejected as
predicted, 9 admitted (8 predicted, 1 surprise), 71/72 predictions correct, all 9 survivors
classified. Three non-declared holes of the predicate were found and each is shown at the
code line that lets it through.

## 1. Method (and what was actually run)

`harness.py` imports the registered runner with `importlib`
(`.ufo/waves/round-43/ctl/run-c2-controls.py`, `main()` never called) and uses its helpers
only: `base_files()`, `admitted()`, `score()`, `patched_counter()`, `rep()`, `row()`,
`set_receipt()`, `gate_line()`, `entry_line()`, `line_of()`, `blob()`, `sha()`, and the
`REAL`/`HELD_ROW`/`FILLER`/census constants. Every fixture is the genuine fixture
`admitted()` (pinned fetch receipts, real quotes, real host census lines) with one defect
applied. `score()` creates `D=$(mktemp -d -p /fast/scratch/hyaku/mado-r43/ExecC2ExtraMutants)`,
runs `git -C "$D" init -q`, verifies the toplevel equals `$D`, commits with
`-c user.name=ctl -c user.email=ctl@ctl.invalid` (write identity never stored), and reads the
committed revision; no ambient `GIT_*` survives (`ENV` in the runner).

Three scorers per control (the first two are the ones the brief names):

| scorer | counter | why |
|---|---|---|
| `real` | `quality/counters/c2-r43-gkeep-entry.py` as frozen | pins bind every NEW id |
| `patched` | the runner's `patched_counter()` | a clause mutant should die by its own clause |
| `pinfree` | supplementary copy: the whole `PINS` literal is rebuilt from the fixture | reaches a defect *inside* a pinned receipt (see Observation O1) |

Primary scorer per control: `patched` for paperwork mutants, `pinfree` for mutants whose
defect lives in a pinned receipt, `real` for the real-seeded forgeries. All three verdicts
are recorded per control in `results.md`.

Command run (seat dir):
`python3 harness.py > run.log 2>&1` → `exit=0`,
`CTL_C2X: controls=72 survivors=9 rejected=63 surprises=1 unexplained=0`,
`CTL_C2X VERDICT: PASS`. Full log: `run.log` (293 lines).

## 2. Anchors (calibration)

The genuine fixture must be admitted by the frozen and the pin-patched counter; both are
(`run.log:2-3`, verbatim):

```
control=P-real expected=admitted=1/1 observed=admitted=1/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 ok=1
control=P-patched expected=admitted=1/1 observed=admitted=1/1 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 ok=1
```

The committed registered receipt `ctl-c2.txt:1-2` carries the same two lines with
`verdict=TARGET_MET` added, and its last two lines are `CTL_C2: controls=74 correct=74/74`
and `exit=0`.

## 3. Population

| family | ids | controls | primary scorer | outcome |
|---|---|---|---|---|
| header window / id / registry cells | CL01–CL16, CL62 | 17 | patched | 16 rejected, 1 admitted (CL62) |
| Gate line + receipt binding | CL17–CL29 | 13 | patched | 12 rejected, 1 admitted (CL23) |
| fences, section titles, README index | CL30–CL34 | 5 | patched | all rejected |
| ADMIT / REFUSE (assimilation) | CL35–CL42 | 8 | patched | 6 rejected, 2 admitted (CL39, CL40) |
| host census (clause h) | CL43–CL52 | 10 | pinfree | all rejected |
| clause e (location ⇄ receipt name) | CL53–CL54 | 2 | patched | all rejected |
| clause g + quote boundary/locator | CL55–CL61, CL63 | 8 | patched/pinfree | all rejected, 1 admitted by design (CL55) |
| clause a (entry absent at REV) | CL64 | 1 | patched | rejected |
| real-seeded forgeries | R01–R08 | 8 | real | 4 rejected, 4 admitted (R01, R05, R06, R08) |

Clause coverage by the new population (single-clause kills, i.e. controls whose vector has
exactly one `0`): a—0 (absence is inherently multi-clause; CL64 shows `a:0`), b—5, c—9, d—1,
e—3, f—2, g—4, h—11, i—5. Every clause a–i is exercised; only `a` cannot be isolated
(rejecting the entry's existence necessarily fails b–i as well, and the registered
`N01-no-entry` has the same shape).

Notable rejected mutants (each killed by the clause it targets, vector in `results.md`):
CL01/CL02 (header pushed past raw line 20 → b), CL04 (cited source line inside a fence → b),
CL07 (4-digit id with no row → c), CL16 (duplicate row → c), CL22 (2-word quote → d),
CL26 (two Gate lines for one id → d), CL30 (census line in a `~~~` fence → h), CL31
(observation line fenced → g), CL43 (fifth mapped client → h under pinfree), CL47 (float
rule `off` against a census line saying `on` → h under pinfree), CL53/CL54 (location ⇄ receipt
name → e), CL56 (locator names the second occurrence of the quote, not the first → g),
CL57/CL58/CL59 (quote preceded by a digit, preceded by an underscore, followed by a digit →
d boundary), CL60 (one quote is a prefix of another id's longer quote → d cross-receipt
containment), CL61 (quote with a period the receipt lacks → d), R02 (a real quote and receipt
re-gated for a second id → d), R03/R04 (real quote at a wrong locator / another file's
locator → g), R07 (row claims a staged package file while the gate cites the pinned cpp → e).

## 4. Survivors (every control the counter admits)

Full table with clause vectors, classifications and re-verified source quotes:
`.ufo/waves/round-43/w1/ExecC2ExtraMutants/survivors.md`.

| control | scorer | clause that should kill it | classification |
|---|---|---|---|
| CL23-gate-outside-section | patched | d | **HOLE (low)** — finding F1 |
| CL39-refuse-foreign-path | patched | i | **HOLE (low)** — finding F2 |
| CL40-admit-foreign-path | patched | i | **HOLE (low)** — finding F2 |
| CL62-two-digit-id-invisible | patched | b/c | **HOLE (low)** — finding F3 |
| CL55-quote-truncated-at-punctuation | patched | d (by design: none) | **LEGITIMATE** — finding F6 |
| R01-real-quote-unsupported-size-claim | real | g | **RESIDUAL (declared)** — F4 |
| R05-real-quote-exclusivity-claim | real | g | **RESIDUAL (declared)** — F4 |
| R06-real-quote-current-value-claim | real | g | **RESIDUAL (declared)** — F4 |
| R08-held-id-invented-receipt | real | d (pin) | **RESIDUAL (declared)** — F5 |

Is the quote-to-claim binding a non-author's job? For R01/R05/R06 **yes**: the predicate's
own docstring declares it (`quality/counters/c2-r43-gkeep-entry.py:83-84`: "the quote-to-claim
binding is the non-author closure's job"), and clause g only tests quote+locator presence in
a line (`:490`), never the sentence around it. Those three are declared residuals, not defects.
For F1–F3 the failing check is the counter's own: no claim binding is involved.

## 5. Findings

### F1 — HOLE (low): a byte-identical GATE line outside `## Gate` is invisible to clause d

Attacks clause d's "no `GATE S###` line sits outside that section".

- Control CL23 appends an exact copy of `GATE S293 …` under `## Notes`; the counter admits
  (`d:1`, all clauses 1). Control CL63 appends a *differing* S293 line in the same place; the
  counter rejects (`d:0`). The pair isolates the mechanism.
- Code: `quality/counters/c2-r43-gkeep-entry.py:403-405` —
  `in_gate = set(glines)` then
  `if re.match(r"^GATE S\d", line) and line not in in_gate:`.
  The check is **text identity**, not position: any outside line whose text equals any line
  of the Gate section (including ADMIT/REFUSE lines) is not counted.
- Mechanism receipt `verify_holes.txt:1-2` (regenerated with the runner's helpers), verbatim:
  `d-outside identical gate_lines=12 in_gate_set=14 notes_gate_lines=1 counted_outside=0`
  `d-outside differing gate_lines=12 in_gate_set=14 notes_gate_lines=1 counted_outside=1`.
- Impact: confined to exact duplicates. A duplicate carries the same claim as the in-section
  line, and once the in-section line is edited the outside copy becomes differing and is
  counted, so no entry-level integrity claim is lost; the contract sentence is nevertheless
  not enforced. Flip condition: count outside lines by position (e.g. drop the
  `line not in in_gate` term, or compare `(index, text)`).

### F2 — HOLE (low): ADMIT/REFUSE accept a staged basename from any directory

Attacks clause i's "each staged path names one of the 11 gkeep-theme package files in STAGED".

- Controls CL39 (`REFUSE /tmp/gkeep-geometry-unobservable-r8.md reason=…`) and CL40
  (`ADMIT /tmp/gkeep-size-to-real-size-r11.md as <entry>`) are both admitted (`i:1`).
- Code: `quality/counters/c2-r43-gkeep-entry.py:503` —
  `staged_ok = lambda p: os.path.basename(p) in STAGED`. `STAGED` is a set of basenames, so
  the directory prefix is never examined. The ADMIT right-hand side is exact
  (`m.group(2) == entry`), so only the staged-path side is loose.
- Mechanism receipt `verify_holes.txt:3-6`: `staged_ok` is `True` for the real package path,
  for `/tmp/…`, and for the shokuknow checkout path; the genuine ADMIT line's groups are
  `('merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md',
  'corpus/knowledge/hyprland-gkeep-geometry-r43.md')`.
- Impact: the assimilation record can name a file that is not the package's (e.g. a copy in
  `/tmp`), while the *set* of 11 theme names is still enforced and the entry target is exact.
  Whether this is a defect or an intended tolerance is a contract question (the docstring
  says "names one of the 11 … package files", which reads stricter than basename matching);
  under that reading it is a hole. Flip condition: require
  `merge/mado/knowledge/corpus/knowledge/<basename>`.

### F3 — HOLE (low): ids with fewer than three digits escape every clause

Attacks the id alphabet shared by b (ghost scan), c (registry rows) and d (Gate lines).

- Control CL62 adds `source: S99 - two-digit id` to the header and `**OBS** S99 …` to the
  body; the entry is admitted with all clauses at 1. No registry row, no Gate line and no
  receipt exists for S99.
- Code: `:107` `ROW_RE = … (S\d{3,})`, `:108` `GATE_RE = … (S\d{3,})`, `:111`
  `SRC_RE = … (S\d{3,})\b`, and the ghost scan `:356`
  `cited = set(re.findall(r"\b[Ss]\d{3,}\b", …))`. A malformed `S99`/`S94` is therefore not
  an id, not a ghost, and not a Gate — it is silently ignored instead of failing.
- Mechanism receipt `verify_holes.txt:7-12`: `src_re('source: S99') = False`,
  `src_re('source: S94') = False`, `src_re('source: S290') = True`, ghost scan on
  `S99` = `[]`, `ROW_RE` on an S99 row = `False`, `GATE_RE` on an S99 gate = `False`.
- Impact: an entry can carry an unregistered, unverifiable citation in the 2-digit form and
  still be admitted. Severity low (the lane's id scheme is 3-digit, so this is malformed
  input, not a plausible legitimate id), but it is silent acceptance rather than rejection.
  Flip condition: treat any `\b[Ss]\d+\b` token as an id and reject ids that do not match
  the 3+ digit scheme.

### F4 — declared residual confirmed: real quote, unsupported claim, true locator

R01 (HyprCtl `"size": [{}, {}],` at `Hyprland-HyprCtl.cpp:395` offered as proof of the
reported value), R05 (client-dump quote at `host-clients-r43.json:49` offered as proof of
exclusivity) and R06 (`*m_realSize = x.size();` at `Hyprland-GeometricMovableAnimated.cpp:45`
offered as proof that hyprctl reads the current value) are all admitted by the frozen
counter. Clause g checks only that a line names the id, carries the quote and the locator
(`:490`). This is exactly the hole the docstring declares (`:83-84`); it is the w2 /
non-author closure's material, not a predicate defect. Quote evidence is re-verified with the
counter's own `quote_at()` against the pinned `fetch/` bytes (`survivors.md`, last column;
`run.log` CTRL lines).

### F5 — declared residual confirmed: a held id's receipt is not pinned

R08 replaces S050's `fetch/S050.txt` with invented bytes and an invented quote; the entry is
admitted. Code: the pin lookup is guarded by `:417` `if i in new_ids:` — held ids skip it.
Declared at `:84` ("a held id's receipt is not pinned"). Reported, not scored as a defect.

### F6 — legitimate admission, reported for completeness

CL55 quotes `m_box = box` (it ends before the `;`) from `Hyprland-Target.cpp:11`; the
counter admits. Clause d's rule is a word-boundary rule — a quote ending in a word character
must not be followed by one, and `;` is not a word character — so **no clause should kill
it**. The semantic risk (a sub-statement quote) is claim binding, i.e. the F4 residual. This
control exists because the brief asked for a quote ending at punctuation; the honest result
is that the counter is right and the quote is legitimate.

## 6. Observation O1 — the registered `patched` scorer does not override frozen pins

The registered runner's docstring says the patched counter's "PINS also hold the fixture's own
receipts". It appends `"basename": sha` lines at the **top** of the `PINS` literal while the
frozen keys stay below; in a Python dict literal the last duplicate wins, so the frozen value
survives. Probe (`patched_counter()` on a fixture whose `host-gkeep.conf` was edited):

```
patched_counter() PINS entries for host-gkeep.conf: 2
   "host-gkeep.conf": "11a3228935606adc0ad5d92dbc7387433a1ce70614221110204c1c6b9e77dc67",
   "host-gkeep.conf": "3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949",
effective == frozen pin: True
effective == fixture bytes: False
frozen pin: 3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949
fixture sha: 11a3228935606adc0ad5d92dbc7387433a1ce70614221110204c1c6b9e77dc67
```

(`verify_pinpatch.txt` holds this output verbatim.)

Consequence: every registered control that edits a pinned receipt (H09, H10, H11, H13, Z1,
Z2, …) is rejected by clause d's pin, not by the clause it targets. The registered verdict
(74/74 rejected) is unaffected, but the "killed by ITS clause" intent is only met for
non-pinned receipts. This seat's census mutants are therefore scored under the supplementary
`pinfree` scorer and labelled as such; under `patched` they show `d:0` (pin) and the defect
would otherwise be masked. Reported for the L1 / w2, not scored as a predicate defect.

## 7. Evidence index (all inside this seat dir)

| path | sha256 | content |
|---|---|---|
| `harness.py` | `8e91a4a04317aaf162759d56327ce22b227f6a3d0705b2bba67711511bd71dbf` | 72 control definitions + three-scorer runner + evidence verifier |
| `run.log` | `b0a99fed2983d564bab401f69520987218f7bb87032470170e3b5906695f0987` | every RUN/CTRL line, anchors, final tally, exit 0 |
| `results.md` | `628ae89ac4f05c1df877c184343d54c2fa41a7912060cad28285b1d33a10b96a` | per-control expected/observed, a/p/f flags, clause vectors, surprises |
| `survivors.md` | `296ef3d12961c37b1e70e4a11ed975b2285014f1a203a760c5c19461b0fb519c` | 9 survivors, classification, non-author test, verified quote locators |
| `verify_holes.py` | `813227e758785c6d30bd70d36d0184f14072dd68f9314bdb6030b5053f562f79` | mechanism probe (independent of the verdict line) |
| `verify_holes.txt` | `5132dc6adc906c186075b08d1c71f4360ea6a3e0d84c021f3e06089ec5d3766a` | F1/F2/F3 mechanism output |
| `verify_pinpatch.txt` | `575ba3a9fab6f3b8bc85d1e8ec954121365103659e3d7e451cb3d50bf5c6f6b1` | O1 probe: duplicate PINS key, frozen value wins |

Cross-references: predicate `quality/counters/c2-r43-gkeep-entry.py` (frozen); runner
`.ufo/waves/round-43/ctl/run-c2-controls.py` (frozen, imported); pins
`.ufo/waves/round-43/receipts/fetch-sha256.txt`; registered receipt
`.ufo/waves/round-43/receipts/ctl-c2.txt`. Every quoted source fragment in this report was
located by grep in the named file (line numbers above) and every receipt quote by the
counter's `quote_at()` (line in `survivors.md`).

## 8. Risks, limits, compliance

- **Not a re-run of the registered suite.** The 74 registered controls were not executed by
  this seat; its anchors reproduce only the genuine fixture's admission under both scorers.
- **`pinfree` is supplementary.** It rewrites the frozen `PINS` literal; it is not the frozen
  counter. Its rows are labelled, and every claim above that depends on it (clause h, the
  boundary controls) also names the `real`/`patched` result (`d:0`, pin) in `results.md`.
- **Scope of the holes.** F1–F3 are low severity: no entry-level claim about the host or the
  source chain is lost. F2 is a contract-vs-implementation question; the L1 decides whether
  it re-registers C2 as v2 (the registration allows a w1 hole found before the data commit to
  re-register) or carries it as a residual. Evidence for either route is in §5.
- **No host reads were needed** (no `hyprctl`, no compositor socket use); no pacman; no tool
  installs (Python 3.14.8, git 2.56.0, both already present). No lane file was written
  outside this seat dir; no git/jj mutation was issued to the lane (`git status --porcelain`
  shows this seat's files untracked only, plus siblings' own files).
- **Scratch** `/fast/scratch/hyaku/mado-r43/ExecC2ExtraMutants` was used via explicit
  `TMPDIR` for every fixture and counter copy and **removed** after the receipts were copied
  here.
