# ExecSessionTriage — round 49 w1: every session-material finding at the base, triaged

Seat: `ExecSessionTriage` (leaf; one read-only labrat allowance not used — no subagent was spawned). Lane:
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Base **`03e4ae76aff7a4be59cb69970dd553baa319695a`** (round-48 closure
commit); lane tip while working `5f37c1b87b3ce5e438d19284e32b2e46fd548a92` (round-49 setup only — the gate and the
registry have the same bytes at both, `82c9053a…` and `4d007fe8…`).

Routed item: **M48-8 part 1** — "triage every finding of the session-material gate at the base, both scopes",
plus the 47 untracked `*.synthetic` sidecars. Nothing in the lane was written outside
`.ufo/waves/round-49/w1/ExecSessionTriage/`; no tracked file was edited; no git mutation ran in the lane
(all clones and fixture commits live under `/fast/scratch/hyaku/mado-r49/ExecSessionTriage/`, deleted at the end).
No title, serial, program name, pid or home path appears in this report or in any file it writes — classes only,
per `SKILL.md` rule 4 and the gate's own value-free output.

Deliverables in this directory:

| file | what |
|---|---|
| `triage.tsv` | 167 rows — `file, rule, count, class, evidence`; covers both scopes (rows that only `--scope all` sees are prefixed `[scope=all only]` in the evidence column) |
| `sidecars-47.tsv` | the 47 untracked sidecars: target, tracked?, marker↔blob sha, registry row, marker grammar, measured waiver |
| `waivers-proposed.txt` | the 3 waiver pairs the current contract can still accept (sidecar line + registry line, digests computed from the base blobs) |
| `real-remediation.md` | the 40 REAL findings: remediation options, what each breaks, and the digest pins a redaction invalidates |
| `verify-claims.py` | reruns every number in this report from the files here and read-only git (`CLAIMS_CHECK passed=36 failed=0`) |
| `receipts/` | the gate runs quoted below, the clean-check of these deliverables, the claims run, and the gate's own base-bytes sha256 |

## 1. The two gate runs at the base

```
python3 quality/check-session-material.py --repo . --rev 03e4ae76… --scope ufo
  SESSION_MATERIAL_RULES: R1=38 R2=38 R3=58 R4=3 R5=22
  SESSION_MATERIAL_WAIVED: findings=3 files=1
  SESSION_MATERIAL: files=22012 findings=159 rev=03e4ae76…          rc=1
python3 quality/check-session-material.py --repo . --rev 03e4ae76… --scope all
  SESSION_MATERIAL_RULES: R1=39 R2=41 R3=59 R4=3 R5=25
  SESSION_MATERIAL_WAIVED: findings=3 files=1
  SESSION_MATERIAL: files=22278 findings=167 rev=03e4ae76…          rc=1
```

`findings=159` reproduces the spotcheck's M48-8 number (`corpus/lessons/round-48-verifier-spotcheck.md:191`).
The 8 findings `--scope all` adds are exactly:

| file | rule | class |
|---|---|---|
| `corpus/knowledge/config-health-report-r3.md` | R5 | REAL |
| `corpus/knowledge/hyprctl-verification-layer.md` | R5 | REAL |
| `corpus/knowledge/hyprland-config-plane.md` | R5 | REAL |
| `quality/check-session-material.py` | R1, R2, R3 | SYNTHETIC-GATE (unwaivable, see §5) |
| `quality/counters/c2-r37-eventq.py` | R2 | SYNTHETIC-NC |
| `quality/counters/c2-r38-eventq.py` | R2 | SYNTHETIC-NC |

**The gate reads git objects only — verified, not assumed.** `--scope ufo` at the tip (`5f37c1b8`, where the 47
sidecars exist only in the working tree) yields an *identical* FINDING set and the same `findings=159`
(`receipts/03-gate-tip-scope-ufo.txt`; `diff` of the FINDING lines against the base run: no output). So the
untracked sidecars currently waive nothing, and every number below is a property of committed bytes.

## 2. Classification criteria (so the table is checkable)

The round-48 seat classed every non-W4 row `real:identity:*`, which conflates *"the value is not in the
reserved namespace"* with *"the value is the host's"* (`triage-r48.tsv`: 31 `real:…program-not-synthetic`, 28
`…title-not-synthetic`, 6 `…serial-not-synthetic`). I separate the two by provenance, not by the gate's refusal
reason:

- **REAL** — the bytes are a live host read, or a copy/report quoting one. Names the class of material only.
- **SYNTHETIC** — a generated fixture whose matched values already sit in the gate's reserved namespace (W4
  passes, measured by calling the gate's own `waiver_values_ok` on each base blob); only the marker pair is
  missing. 52 of these.
- **SYNTHETIC-NC** — a generated fixture whose values fail W4 *because the fixture was written with a
  placeholder the namespace does not reserve* (a hand-chosen probe title, a real-looking program name, an
  uppercase `REDACTED`, a serial-shaped literal). Not host material; needs a rename or a contract change.
- **SYNTHETIC-GATE** — a copy of the gate (or of a gate draft), matching on the gate's own selftest constants.
- **FALSE-POSITIVE** — the matched text is not a dump/identity at all.

**False positives: 0.** Every one of the 167 rows is a real JSON client/monitor object, a real `users:((…))`
row, a real bare-`/home` line block or a real serial-shaped token; the gate's prose about its own rules, its
regexes and its docstring examples do not match, `corpus/README.md` and `SKILL.md` prose do not match, and the
`_parts("481","QZRTM","9027")` trick that keeps the gate's own fixture literals out of its bytes works (0 hits on
the gate file for R5). Round-46 reached the same conclusion at an earlier revision ("False positives: **0**",
`.ufo/waves/round-46/w1/ExecSessionTriage.md:47`); this round confirms it holds for the 70 findings added since.

| class | rows | files | counted instances |
|---|---|---|---|
| REAL | 40 | 40 | 851 |
| SYNTHETIC (waivable now) | 52 | 50 | 65 |
| SYNTHETIC-NC | 48 | 44 | 200 |
| SYNTHETIC-GATE | 27 | 9 | 66 |
| FALSE-POSITIVE | 0 | 0 | 0 |
| **total** | **167** | **140** | **1182** |

What the four classes are made of (full per-file rows in `triage.tsv`):

- **REAL 40** — 13 R2 (the round-37/38/39 live `ss` tables and the 9 reports quoting them), 3 R4 (round-35
  `S203.scope.txt`, round-43 `live-census.txt`, round-48 `check2-fleet-byte-scan.txt`), 24 R5 (one host monitor
  description token in 3 live corpus entries + their 21 wave copies).
- **SYNTHETIC 52** — 45 round-45 `RevengerOmarchy` fabricated `mons.json` dumps (45 rows), the round-46
  `CritW2Gate` pair for R2+R3 (4 rows), and three files whose values are already in the namespace but which were
  never marked: `round-48/w1/SentPrivacy/receipts/shapes.py`, `round-48/w2/MutRoutedR3.md`,
  `round-48/w2/CritSessionMarker/marker-probe.py` (R1 only).
- **SYNTHETIC-NC 48** — 19 `round-43 ExecOracleGkeep` dumps of the seat's own probe client in a nested
  bwrap/headless Hyprland (`20-observation.txt:1-2`), 2 `round-44 ScrLessonSkeleton` demo clients, 1 round-45
  mutant driver (uppercase `REDACTED`, round-46 report `:60`), 12 round-37 scratch counter/fixture constants,
  2 `quality/counters/c2-r3{7,8}-eventq.py` fixture rows (scope all), and 12 gate-variant/probe fixtures in
  round-46/47/48 (the CritW2Gate pair's R1, `repro.py`, the round-46 gate variants, `demo/run-demo.sh`,
  `adversarial.txt`, `driver1.sh`, `marker-probe.py` R2/R5, `probe_bigfile.py`).
- **SYNTHETIC-GATE 27** — 8 wave copies of a gate × 3 rules, plus the gate itself under `--scope all`.

## 3. The 47 untracked `*.synthetic` sidecars

Facts, all measured at the base (`sidecars-47.tsv` has one row per sidecar):

- **What each marks**: 45 are `kind=fixture rules=R3_MONITOR_IDENT` for the round-45 `RevengerOmarchy`
  `mons.json` fixtures; 2 are `kind=fixture rules=R2_PROC_TABLE,R3_MONITOR_IDENT` for the round-46 `CritW2Gate`
  pair (`.md` and `report.md`, which carry identical bytes, `fb43aca9…`).
- **Target tracked at base**: 47/47 yes. **Marker sha256 = target blob sha256**: 47/47 match. **Registry row
  present at base**: 47/47 yes, with the same sha, the same rule list and the same kind. **Marker grammar**
  (`MARKER_RE`): 47/47 well-formed. So the pair contract is satisfied on the sidecar's side; the 47 files are the
  *only* missing half — and they are missing because they are untracked.
- **Provenance**: all 47 are byte-identical to the install set that round-48 `ExecSessionMarker` ships in
  `.ufo/waves/round-48/w1/ExecSessionMarker/sidecars/` (`cmp`, 47 identical, 0 mismatched), whose `SHA256SUMS`
  carries 48 `.synthetic` entries (these 47 plus that seat's gate-copy sidecar); the registry at the base is that
  seat's 48-row install set (`session-material-waivers.txt`, `4d007fe8…`). The 47 in the wave dirs are that seat
  writing outside its own directory (the round-48 w1 incident) — inert, because the gate reads revisions.
- **Does committing them waive the findings?** Measured, not predicted: in a `git clone --shared` of the lane at
  the base I committed exactly those 47 files and nothing else, then ran the gate → `findings=110`,
  `SESSION_MATERIAL_WAIVED: findings=52 files=48` (45 round-45 + 4 CritW2Gate + the 3 gate-copy rows that were
  already waived), `receipts/04-gate-47-sidecars-committed.txt`. The only refusals are the two R1 findings on the
  CritW2Gate pair, `reason=rule-not-listed` — the marker waives only the rules it names, and R1 is not one of
  them (`value-not-synthetic:title-not-synthetic` if it is added, measured in §4).
- **Does the contract accept them at the tip?** Yes: the gate and the registry are byte-identical at the base and
  the tip, so the base measurement transfers unchanged. W1 (path under `.ufo/waves/`) and W3 (registry outside
  `.ufo/`) hold, W2 holds for 47/47, W4 holds for 47/47 (values in the reserved namespace).
- **Recommendation for the L1's commit-vs-remove decision**: commit — 49 findings clear for 47 small files that
  are already vetted, already registered, and reproducible from a tracked source. Removing them leaves the
  round-45/46 fixtures permanently red with no remediation path (their values are in the namespace, so the gate
  refuses every other explanation). One caveat: the sidecars live in wave directories the seats do not own, so
  the L1 is the only correct committer (a seat must not commit another round's wave dir).

## 4. What the marker can and cannot do (measured refusals)

Each line below is a commit in the scratch clone plus one gate run (`receipts/05-…`, `receipts/06-…`):

| probe | result |
|---|---|
| 3 new pairs for the W4-ok files (`shapes.py`, `MutRoutedR3.md`, `marker-probe.py` R1) | **waived**; totals become `findings=107`, `WAIVED: findings=55 files=51` |
| CritW2Gate pair, marker amended to list R1 | **refused** `value-not-synthetic:title-not-synthetic` (×2) |
| `marker-probe.py`, marker listing R2 as well | **refused** `value-not-synthetic:program-not-synthetic` (pid 4242 / un-reserved program) |
| `marker-probe.py`, R5 | **refused** `serial-rule-not-waivable` (before the marker is parsed) |
| `quality/check-session-material.py` itself, `kind=gate-copy`, `--scope all` | **refused** `path-outside-waves` (×3) |

So the contractual ceiling at this base is **55 of 167 findings**, and 107 need content work.

## 5. Contract gaps this triage measured (for the freeze, not fixed here)

1. **A `gate-copy` waiver is revision-fragile.** W4a compares the copy to the gate *at the scanned revision*.
   The round-45 `ExecPrivacyGate` copy is byte-identical to the gate that was committed until round 48
   (`889f8f05…`) — it was a valid gate-copy then (round-46 report §1a says so) and is refused now that the gate
   is `82c9053a…`. Same bytes, opposite verdict, no diff to audit. Any future gate edit silently un-waives every
   historical copy. Options for the freeze: accept a digest allowlist of committed gate revisions, or reclassify
   old copies as `fixture` with a reserved namespace for selftest titles (`Alacritty`/`OrgExampleApp` are what
   actually fail W4), or delete the wave copies of the gate.
2. **Four copies are gate *drafts* that were never committed** (`a4a0a084…` ×4, round-47, 12 findings) plus two
   one-off round-46 variants (`a36224e2…`, `3fc480a4…`, 6 findings). No W4a rule can ever cover them because
   there is no committed gate revision with those bytes; together with the two stale-`889f8f05` copies they are
   the SYNTHETIC-GATE block (24 of its 27 findings).
3. **`--scope all` cannot pass, by construction.** The gate's own selftest constants are R1/R2/R3 findings and
   W1 refuses any path outside `.ufo/waves/` — measured `path-outside-waves`. Either the gate source gets a W1
   exception (`kind=gate-copy` on its own path), or `--scope all` is documented as always-red-on-itself. This is
   a freeze decision: a counter that can never be green is not a counter.
4. **The serial rules are structurally unwaivable**, so any future seat that must write a serial-shaped literal
   (a probe for R5/R6, exactly what round-48 `CritSessionMarker` needed) leaves a permanent red. Two honest
   options: a reserved serial namespace for `.ufo/waves/` fixtures (which was deliberately refused because a
   serial's identity is its value), or a declared, counted `--allow-serial-shape` carve-out for probe files with
   its own registry row.
5. **The namespace has two case/typo traps** that cost real renames: `SYNTH_TITLE_RE` is case-sensitive, so a
   title exactly `REDACTED` is refused while `redacted` is accepted (`round-45 ScrMistakes/mutants.sh`); and a
   process row is only synthetic when the program *name* is reserved, so a hand-built row with a real compositor
   name is refused even when its pid is `1` (`round-37 CritC2Cheap/handsnap.txt`).

## 6. REAL files and remediation

40 findings over 40 files, listed with their remediation in **`real-remediation.md`**:

- **R2, 13 files (760 rows)** — 2 are inputs of frozen counters (`c2-r37-eventq.py:17,39`;
  `c2-r38-eventq.py:25,60-61,226-231`), so they need census-only regeneration + a counter re-pin in the same
  freeze — which is exactly what the round-38 outside check already routed
  (`corpus/lessons/round-38-verifier-spotcheck.md:43,86`). The other 11 have no machine reader and can be
  redacted line-preserving.
- **R4, 3 files (67 paths)** — rewrite the absolute home prefix to `~/`; line numbers survive, so
  `corpus/lessons/round-43.md:222` / `round-44.md:69`'s citation of `live-census.txt:232` stays true. The two
  digest pins (`.ufo/waves/round-43/w1/ExecLiveHost.md:12`, `.ufo/waves/round-43/w1-results.json`) must be
  updated in the same commit.
- **R5, 24 files (one token)** — replace with `<serial-redacted>` in the 3 live entries *and* their 21 wave
  copies in one commit, because the copies claim byte equality with the entries. No counter, tool or quality
  script reads the token (`grep -rlF` → the three entries only). Historical manifest pins
  (`round-20/w2/ScribeShonen/pointer-check.txt:41`, `round-43/w1/ExecLocatorGate/knowledge-base-manifest.txt:9,24`)
  remain true only "at that revision" and should say so.

Evidence pointers that make each removal judgeable for harm: `LOG.md`, `SCORECARD.md`, `SKILL.md` and
`corpus/lessons/` cite `config-health-report-r3.md`, `hyprctl-verification-layer.md`,
`hyprland-config-plane.md` (index rows + several rounds) and `live-census.txt` (`SCORECARD.md`,
`corpus/lessons/round-41.md:285`, `round-43.md:222`, `round-44.md:69`); the round-37/38 `eventq-live-ss.txt`
receipts are cited by `corpus/lessons/round-38-verifier-spotcheck.md:43,86` and by the two counters; the
round-35 `S203.scope.txt`, round-39 census and round-48 `check2-fleet-byte-scan.txt` are cited by nothing in
`LOG.md`/`SCORECARD.md`/`corpus/lessons/` (their only readers are their own round's seat reports).

## 7. Risks, limits and what was not run

- **Risks.** (a) Editing the two counter-consumed `ss` receipts without re-pinning breaks `c2-r37`/`c2-r38`
  live clauses; (b) editing a corpus entry invalidates three historical digest manifests; (c) a `gate-copy`
  waiver dies on the next gate edit (§5.1); (d) the 47 sidecars must be committed by the L1 — a seat committing
  another round's wave dir repeats the round-48 w1 incident in the other direction.
- **Limits.** Triage is by reading the matched values (via the gate's own `matched_values`) plus provenance;
  for `round-46 ExecSessionTriage/demo/run-demo.sh` the device identity is marked `[INFERENCE]` — the script's
  own comment says it *plants* a realistic dump, no receipt shows a capture, and the value does not match this
  host's monitor; if its author says it came from a physical device, reclassify it REAL and add it to
  `real-remediation.md` group A2. `R6_SERIAL_EXACT` was not scored (it needs a live `hyprctl monitors` read,
  which this seat is not authorised to run), so the REAL R5 token is identified by context (it sits in the
  `desc` field beside the config claim), not by an exact-value match against the host.
- **Not run, deliberately.** No build/lint/test/formatter; no host service, compositor, pacman or `~` write; no
  `xkbcli`, no `hyprctl`; no package install was needed (nothing installed, so no tooling row). Scratch
  `/fast/scratch/hyaku/mado-r49/ExecSessionTriage/` (clone + fixture commits) was removed after the receipts
  were copied here.

## 8. Receipts

| file | content | sha256 |
|---|---|---|
| `receipts/01-gate-base-scope-ufo.txt` | base, `--scope ufo`, rc=1, findings=159 | `41a63332bc1e582b7b71d63f648af33c58c98f3c1c09961c8a782c4043bc116e` |
| `receipts/02-gate-base-scope-all.txt` | base, `--scope all`, rc=1, findings=167 | `caead0dd667ef841676b1daadde6786c29b8041ea7e5eeafd3090499dc33829f` |
| `receipts/03-gate-tip-scope-ufo.txt` | tip, `--scope ufo`, identical FINDING set | `4152db18cacf1342a56be52acc9189e05dd0310686679fc44872cc6afe563947` |
| `receipts/04-gate-47-sidecars-committed.txt` | fixture commit `f48a94c0`, findings=110, waived=52 | `44d20b5acae06b46958da51192dc53a09a04db6a259cfd889a3efde912cb0134` |
| `receipts/05-gate-plus-3-pairs-scope-ufo.txt` | fixture commit `f2baca5a`, findings=107, waived=55 | `1f41c4838146921328fb89112f74a09813c1586e30f60921b61d653a4b65782a` |
| `receipts/06-gate-rule-extensions-scope-all.txt` | fixture commit `58dcd96e`, 7 refusals incl. `path-outside-waves` | `b95a59309369c251d1f435d1ad5e74174b00bd0c35659934ece8a8385431cb8b` |
| `receipts/07-gate-base-bytes.sha256` | the gate bytes every classification was computed with (`82c9053a…`) | `838f1efdf1aeab612b2461429156dbfe60802a1fde18090ae4b09c3a3468858c` |
| `receipts/08-seat-deliverables-clean.txt` | this seat's other 14 files scanned by the gate in a throwaway repo: `findings=0`, rc=0 — the triage itself leaks nothing | `374e74948c9d04dc36f684c5ee329fc8a36b712c46eddf5d192daefc3dac0564` |
| `receipts/09-claims-verify.txt` | `verify-claims.py` run: `CLAIMS_CHECK passed=36 failed=0` | `5735ae214d2d5335864e2a63ecc1fd1830ac377c9fe6e35443b66e9589512ec9` |

The three fixture commits above exist only inside a `git clone --shared` under
`/fast/scratch/hyaku/mado-r49/ExecSessionTriage/` that was deleted after the receipts were copied out; each
receipt is the gate's own output on that commit, so it is reproducible by re-running the same commit recipe
(commit the 47 sidecars from `.ufo/waves/round-48/w1/ExecSessionMarker/sidecars/`, then the pairs in
`waivers-proposed.txt`).
