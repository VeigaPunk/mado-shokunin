# ExecSessionTriage — round-45 closure D3 + SCORECARD planned 2

Seat: `ExecSessionTriage` (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round 46 w1, 2026-10-26. Scanned revision: `4d22eeb66c2835af8aaa3fac6ad838fa616aa663`
(round-45 tip; base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, freeze `8c5434c6…`).

Deliverables in `.ufo/waves/round-46/w1/ExecSessionTriage/`:

| file | content |
|---|---|
| `check-session-material.py` | gate copy **with** the synthetic-material marker layer (never the tracked file; 34/34 selftest) |
| `triage.tsv` | all 97 findings at `4d22eeb`, one line each: path, rule, count, class, provenance basis |
| `receipts/` | 12 receipts (baseline, triage counts, both-direction demo A–G, verify) |
| `demo/run-demo.sh` | rebuilds the whole demo from scratch in one run |
| `demo/mark-synthetic.py` | writes sidecars + registry into a scratch clone and commits there |
| `demo/triage-table.py` | regenerates `triage.tsv` from the gate's own output |
| `demo/verify.py` | re-checks every number and quoted line this report cites (35 checks, 0 failed → `receipts/09-verify.txt`) |
| `demo/waivers-round45.txt` | the ready-to-install registry for the 49 (47 rows, one per file) |
| `skill-row.md` | the `SKILL.md` gate-registry row, in the `mado-axis-scores` shape |

Commands actually run (each produced the receipt named):

```
python3 -I quality/check-session-material.py --repo <lane> --rev 4d22eeb…        > receipts/01-baseline.txt      exit=1 findings=97
python3 -I <seat>/check-session-material.py --repo <lane> --rev 4d22eeb… --no-waivers > receipts/01b-baseline-copy-nowaivers.txt  (identical to 01)
python3 -I <seat>/demo/triage-table.py                                          > receipts/02-triage.txt
python3 -I <seat>/check-session-material.py --selftest                          > receipts/00-selftest.txt     34/34
bash <seat>/demo/run-demo.sh                                                    > receipts/03…08
python3 -I <seat>/demo/verify.py                                                > receipts/09-verify.txt        checks=40 failed=0
```

## 1. Triage of the 97 findings

97 findings at `4d22eeb` (`receipts/01-baseline.txt:99`), classified one by one
in `triage.tsv`; counts (`receipts/02-triage.txt`):

```
findings=97
REAL=15
SYNTHETIC=82
FP=0
REAL       R2_PROC_TABLE=13  R4_HOME_LISTING=2
SYNTHETIC  R1_CLIENT_DUMP=23 R2_PROC_TABLE=13 R3_MONITOR_IDENT=46
round-45 findings=49 synthetic=49
```

False positives: **0**. Every match is a genuine dump-shaped object, row or
listing; none was a schema, a prose mention or a projection. The gate as written
does not over-fire — it under-discriminates (fixtures vs session data), which is
the defect D3 named.

### 1a. The 49 synthetic findings of round 45 (the set the lane counted)

All 49 are under `.ufo/waves/round-45/`, all synthetic, in 47 files:

| files | findings | rule | provenance basis |
|---|---|---|---|
| 45 × `RevengerOmarchy/fixtures/w*/**/mons.json` | 45 | R3 | fabricated monitor identity (`Fake Corp`, `0x0000`, `SN00000`) |
| `ExecPrivacyGate/check-session-material.py` | 3 | R1, R2, R3 | the gate's own selftest constants; blob is byte-identical to `quality/check-session-material.py` at the same revision (sha256 `889f8f05…` both sides) |
| `ScrMistakes/mutants.sh` | 1 | R1 | mutant driver written into a scratch git repo; the planted client object carries title `REDACTED` |

### 1b. The other 33 synthetic findings (pre-existing, same disease)

| files | findings | rule | provenance basis |
|---|---|---|---|
| 19 × `round-43/w1/ExecOracleGkeep/**` | 19 | R1 | sandbox oracle dumps of the seat's own probe client in a nested headless Hyprland — all 74 `title`/`initialTitle` values in that directory are `gkeep-oracle-probe` (verified by scan, no other value) |
| 2 × `round-44/w1/ScrLessonSkeleton/c1-demo/client*.json` | 2 | R1 | lesson demo fixture: `address: 0x1`, fabricated class/title |
| 12 × `round-37/w1/scratch/**` (SimplifyCounters ×9, `controls_critaxis.py`, `setup-reasons.py`, `handsnap.txt`) | 12 | R2 | counter/fixture constants: placeheld socket path `/run/user/1000/hypr/HIS/…`, but the host Hyprland pid and one live client pid are reused (redaction gap, see §6) |

### 1c. The 15 real findings (must not be waivable)

| file | rule | count | what leaked |
|---|---|---|---|
| `round-35/scratch-evidence/SentProvenance/S203.scope.txt` | R4 | 12 | bare `/home` paths from a host-tree grep receipt |
| `round-37/receipts/eventq-live-ss.txt` | R2 | 5 | live host socket table |
| `round-37/res/reports/L1Mado37-2.CritEntryE2.md` | R2 | 5 | report quoting the live rows (socket path placeheld, pid/program/fd kept) |
| `round-37/w1/reports/ExecEventqB.md` | R2 | 1 | live row quoted |
| `round-37/w1/reports/ExecProcCrosscheck.md` | R2 | 5 | live rows quoted |
| `round-37/w1/reports/RevC2Code.md` | R2 | 5 | live rows quoted |
| `round-37/w1/reports/ScoutRollingLog.md` | R2 | 2 | live rows quoted |
| `round-37/w1/reports/ScoutSsSemantics.md` | R2 | 5 | live table quoted |
| `round-37/w1/scratch/ExecEventqA/live-ss.txt` | R2 | 5 | live host socket table |
| `round-38/receipts/eventq-live-ss.txt` | R2 | 715 | live host socket table (the whole process table) |
| `round-38/w1/reports/RevC2v3.md` | R2 | 1 | live row quoted |
| `round-38/w1/reports/RevLiveTriplet.md` | R2 | 5 | live rows quoted |
| `round-38/w1/reports/ScoutR29Refusal.md` | R2 | 1 | live row quoted |
| `round-39/w1/ExecEventqSnapshot/eventq-live-census.txt` | R2 | 5 | live host socket table |
| `round-43/w1/ExecLiveHost/live-census.txt` | R4 | 40 | bare `/home` paths from the host tree |

These are receipt/report artefacts of the evidence axis; they cannot be waived
by any marker (W1–W4 all fail for them in practice, and the marker is never
issued for them) and are the lane's material to redact or retain deliberately.

## 2. The synthetic-material marker

Contract in the copy's docstring, `<seat>/check-session-material.py:52-93`;
`MARKER_RE` at `:138`; reserved namespaces at `:146-167`; `waiver_values_ok` at
`:403`; `load_registry` at `:437`; `apply_waivers` at `:464`.

A marker is a **pair**, both read from the scanned revision:

1. sidecar `<path>.synthetic`, tracked, line 1 exactly
   `SYNTHETIC-MATERIAL v1 kind=<fixture|gate-copy> rules=<R1,…> sha256=<64 hex>`;
2. one line `<path> <sha256> <rules> kind=<kind>` in the registry, default
   `quality/session-material-waivers.txt` — outside `.ufo/`.

A `(file, rule)` finding is waived only if W1–W4 all hold; a rule not listed in
the marker still fires on the same file.

| condition | why it exists | refused as |
|---|---|---|
| W1 path under `.ufo/waves/`, registry outside `.ufo/` | a wave cannot issue its own waiver; the waiver list is one reviewable lane file | `path-outside-waves`, `registry-in-ufo` |
| W2 sidecar tracked, grammar exact, sha256 = sha256 of the target blob | appending anything to a waived file voids the waiver; the marker cannot survive an edit | `marker-malformed`, `sha-mismatch` |
| W3 registry line repeats path, sha256, rule list, kind | writing a fixture does not write the waiver; a second, non-`.ufo` commit must name it | `unregistered`, `registry-sha-mismatch`, `registry-rule-mismatch`, `registry-kind-mismatch` |
| W4a `kind=gate-copy` ⇒ target byte-identical to `--gate-source` at the same revision | the only file this kind can cover is the gate itself with its selftest constants | `gate-source-mismatch` |
| W4b `kind=fixture` ⇒ every matched value in a reserved namespace | a real title, serial, pid or home user cannot be waived at all | `value-not-synthetic:<what>` |

Reserved namespaces (W4b), all full-match unless noted:
titles `redacted` / `a live window title` / `another live window title` /
`synthetic…` `fixture…` `selftest…` `probe…` `example…` `demo…`;
serials `sn0+`, `serial0+`, `synthetic…`, `fake…`, `example…`, `redacted`, `0+`
with `make`/`description` containing `fake|example|synthetic|selftest|redacted`
and `model` in `0x0+|fake…|example…|synthetic…|redacted`; process rows with a
program named `synthetic…`/`fixture…`/`selftest…`/`fake…`/`probe…`/`example…`
and pid ≤ 1024; home users `example|someone|selftest|fixture|synthetic|redacted|user`.

### How a real dump is prevented from hiding behind the marker

1. **Cannot self-issue** — the registry lives outside `.ufo/` and is read from
   the scanned revision, so a seat's own commit cannot waive its own file; the
   waiver appears as a diff in a lane file a reviewer reads (`W1`, `W3`).
2. **Cannot be edited in later** — the sha256 pins the exact bytes; the tamper
   run (§3 E) appends one real client object to a waived fixture and the
   finding returns as `reason=sha-mismatch` (`receipts/07-tampered-waived-fixture.txt:83`).
3. **Cannot launder real values** — W4b checks the values the rule actually
   matched, not a declaration: the planted real monitor dump with a valid
   marker and registry line is rejected
   (`receipts/06-planted-real-dump.txt:83`, `reason=value-not-synthetic:serial-not-synthetic`)
   and the finding is kept (`:132`).
4. **Cannot borrow `gate-copy`** — that kind requires byte identity with the
   registered gate source; any other file keeps its findings.
5. **Cannot be silent** — every honoured waiver prints `WAIVER file=… rule=… kind=…`,
   every refusal prints `WAIVER_REJECTED file=… rule=… reason=…`, and the count
   prints as `SESSION_MATERIAL_WAIVED: findings=N files=N` before the summary.
   `--no-waivers` returns the exact pre-marker verdict.

Residual, declared: a deliberate author who edits a fixture's values into the
reserved namespace (e.g. retitles a real window `redacted`) and registers it in
`quality/` can still waive that file's *title* rule; what they cannot do is keep
the real value and pass W4b, and the waiver is one visible line in a reviewed
file. R1's contract is the title field, so a redacted title is the outcome the
policy wants; R2/R3/R4 have no equivalent escape because identity there is the
value itself.

## 3. Both directions, measured

Clone: `git clone -q --shared --no-checkout <lane> $S/clone`,
`git checkout -q --detach 4d22eeb…`, toplevel asserted equal to the clone.
All runs use the seat's gate copy; `HEAD` differs per run as the demo commits.

| run | clone state | findings | waived | rejected | exit | receipt |
|---|---|---|---|---|---|---|
| A | `4d22eeb`, `--no-waivers` | 97 | 0 | 0 | 1 | `03-newgate-baseline.txt` |
| B | + markers on the 49 round-45 (47 files) | **48** | **49** | 0 | 1 | `04-marked-49.txt:99-100` |
| B′ | same clone, **tracked** gate (no waiver support) | 97 | — | — | 1 | `04b-tracked-gate-on-marked.txt` |
| C | + markers on all 82 synthetic | 48 | 49 | 33 | 1 | `05-marked-all-synthetic.txt:132-133` |
| D | + planted real monitor dump with marker + registry line | 49 | 49 | 34 | 1 | `06-planted-real-dump.txt:83,132,135` |
| E | + one real client object appended to a waived fixture | 51 | 48 | 36 | 1 | `07-tampered-waived-fixture.txt:82-83,137-138` |
| F | E's clone, `--no-waivers` | 99 | 0 | 0 | 1 | `08-no-waivers.txt:101` |

The two required directions:

- **the 49 synthetic findings disappear** in B: `SESSION_MATERIAL_WAIVED: findings=49 files=47`
  and `SESSION_MATERIAL: files=17117 findings=48` — 97 − 49 = 48, and the
  tracked gate on the same bytes still reports 97 (B′), i.e. the drop comes from
  the marker layer, not from changed content.
- **a planted real dump with the marker still fails** in D and E: valid sidecar,
  valid registry line, valid hash, and the finding stands — once for a real
  serial (W4b) and once for an appended real client object (W2).

C is the anti-hiding measurement in the other direction: adding markers to the
33 pre-existing synthetic findings does **not** silence them — 21 are refused as
`title-not-synthetic` (probe titles such as `gkeep-oracle-probe`) and 12 as
`program-not-synthetic` (fixture rows naming real programs beside the host
Hyprland pid). They need redacted values or a reserved namespace, not a marker.

## 4. SKILL.md gate-registry row (draft)

`skill-row.md` holds the row in the `mado-axis-scores` shape (`SKILL.md:769`,
header `SKILL.md:767`): name `mado-session-material`, gate, entry command
`python3 -I quality/check-session-material.py --repo . --rev REV`, verdict map
0/1/2, self-test spelling `SELFTEST: passed=N/N failed=N`, pinned values
(summary line, four rule names, marker grammar + registry line), write scope
"reads committed blobs … selftest writes only under `$TMPDIR`", owner `mado`.

## 5. Install notes for the integrator (L1)

1. Copy `<seat>/check-session-material.py` over `quality/check-session-material.py`
   (it is a strict superset: same detection, same summary line, same exit map).
2. With no registry and no sidecars the verdict is unchanged — proven byte for
   byte on `4d22eeb`: `receipts/01-baseline.txt` ==
   `receipts/01b-baseline-copy-nowaivers.txt`.
3. To close D3's red at `4d22eeb`, commit sidecars for the 49 (or accept them as
   real and redact) and a first `quality/session-material-waivers.txt`: the exact
   registry is `demo/waivers-round45.txt` (47 rows covering 49 findings — one row
   per file, the gate copy carrying three rules), and each row needs its
   `<path>.synthetic` sidecar with the same sha256/rules/kind.
   `mark-synthetic.py` regenerates both from `triage.tsv`; the outcome is the
   measured `SESSION_MATERIAL_WAIVED: findings=49` of §3 B.
4. Proposed SCORECARD line for planned 2 (for the L1 to place; this seat does not
   edit `SCORECARD.md`): *"D3: 97 gate findings at `4d22eeb` triaged — 15 real
   (2 R4, 13 R2), 82 synthetic, 0 false positive; marker layer landed
   (34/34 selftest), 49 round-45 findings waived, planted real dump still exit 1."*

## 6. Risks, limits, open items

- **Redaction gap in the 12 round-37 counter/driver fixtures**: the socket path is
  placeheld (`/run/user/1000/hypr/HIS/…`) but the host Hyprland pid and one live
  client pid are literals in the fixture strings. They are synthetic files with a
  real value inside; my gate refuses to waive them (`program-not-synthetic`) on
  purpose. Fix at source: reserved pids (≤ 1024) or redacted program names.
- **R1 waiver scope** is the title field by the gate's own contract; a waived R1
  file may still carry client pids/addresses in the same objects. R2/R3/R4 have
  no such gap because the rule *is* the value.
- **Registry is a review surface, not a proof**: W1/W3 make abuse visible in a
  non-`.ufo` diff, and W4b blocks real values, but a reviewer must still read it.
- The 15 real findings are untouched by this seat (pre-existing, outside my
  write scope). They stay red at any revision that still contains them; that is
  the gate working, and the owning seats must redact or the lane must waive
  knowingly — the mechanism gives them no silent path.
- The seat's gate copy itself lives under `.ufo/` and carries the selftest
  constants; until it is installed as `quality/check-session-material.py` it is
  an untracked working-tree file (not scanned). Once installed, its own
  `kind=gate-copy` entry covers copies of it.

## 7. Tooling

No installs, no version changes: python3 3.14.8 stdlib (`hashlib`, `json`,
`re`, `subprocess`, `tempfile`) and git only. No pacman, no network, no
compositor call of any kind (the gate reads git objects only). Scratch
`/fast/scratch/hyaku/mado-r46/ExecSessionTriage/` was used for the clone and the
selftest `$TMPDIR`, and deleted at the end of the demo run (`trap … EXIT`);
`demo/run-demo.sh` rebuilds it. No receipt cites a `/tmp` or scratch path as
evidence: receipts are the gate's own output, copied into `receipts/`.
