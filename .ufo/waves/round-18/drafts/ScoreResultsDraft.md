## Round 18 — committed results and bounded author verdicts

DRAFT SKELETON (ScoreResultsDraft). Every `[PENDING: …]` is a placeholder for a
value that must come from a run after the wave lands. No number below is
measured in round 18. Before-values are the round-18 pre-registration baselines
(`evidence/measure-before.json`, rev `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`)
or the round-17 committed results, cited as such.

Baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`; pre-registration
`d3a0000` (SCORECARD tail "Round 18 — declared claims"). Initial content
`[PENDING: rev]`; final measured content `[PENDING: rev]`.
Commands to run, all paths below under `.ufo/waves/round-18/` (not yet run):

```sh
python3 .ufo/waves/round-17/measure.py d9a5a18e17cd3a68b52148fcc01c4a30e340ba98
python3 .ufo/waves/round-17/measure.py [PENDING: final measured rev]
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/compound
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/hardening
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/w2-regressions
python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen-tripwire
[PENDING: tampered-copy frozen run, expect snapshot_tampered exit 2]
[PENDING: hermetic selftest and classifier commands, as recorded in round 17]
```

| Claim / axis | Before → after | Verdict / measured evidence |
|---|---|---|
| C1 calibration, literal lesson-citation fraction | 15/23 = 6.5217 → [PENDING: n/26 = x] (target ≥ 18/26) | [PENDING: bounded author verdict]; `evidence/measure-before.json`, `measure-final.json` [PENDING: final file]; criteria 24-26 added append-only: [PENDING: list] |
| C2 coverage, rubric V (P1-P6) | 4/6 = 6.6667 → [PENDING: n/6 = x] (target 6/6) | [PENDING: bounded author verdict]; P3 `corpus/knowledge/walker-route-r18.md`, P5 `corpus/knowledge/theme-route-r18.md` [PENDING: covered or not]; documentary only, host binaries `[UNK]` |
| C3 operability, frozen tripwire replay (R17-V4) | `--frozen` usage error, exit 2; no frozen baseline; registry row `probe` → [PENDING: frozen_match exit x; snapshot_tampered exit 2; suite N/N; registry row `gate` or `probe`] | [PENDING: bounded author verdict]; not prevention, not R15-V1 remediation |

Separable: C1 counts QUALITY text only; C2 uses no tool or criterion; C3 uses
no note or criterion. Routed jj-migration fixes are repairs, not claims.

### Claim C1 — calibration receipts and routed defects

Routed defects and disposition (status is [PENDING] until each has a committed
receipt):

| Defect | Source | Disposition | Receipt |
|---|---|---|---|
| R17-V1 tripwire scan receipts lack tool sha256 and measured_commit | round-17-verifier-spotcheck §6 | [PENDING] | [PENDING] |
| R17-V2 re-cut claim under tool `962919ce…` not recorded by git; report cites `7a98720e…` | round-17-verifier-spotcheck §6 | [PENDING] | [PENDING] |
| R17-V5 rubric-V tightenings bite only in a /tmp lab; no committed mutant receipt | round-17-verifier-spotcheck §6 | [PENDING] | [PENDING] |
| JjAuditMado F10 `tools/mado-verify.sh:3406` digests failed `git show` as empty input (`e3b0c442…`), false "local edit" FAIL | jj-w1 JjAuditMado | [PENDING: rc capture] | [PENDING: failing git-stub scenario] |

New lesson-cited QUALITY criteria (append-only, each with a runnable check
shown able to fail): [PENDING: criteria 24, 25, 26 and their red-fixture
result]. Lesson: `lessons/round-18.md` `## Mistakes` rows [PENDING: ids].

### Claim C2 — coverage routes

| Route | Surface | Sources (tier A, mined, used-by names the note) | Fetch receipts | Status |
|---|---|---|---|---|
| `corpus/knowledge/walker-route-r18.md` | P3 | [PENDING: S0xx-pending → assigned id(s)] | `.ufo/waves/round-18/fetch/<seat>/receipts.jsonl` [PENDING] | [PENDING: covered / open] |
| `corpus/knowledge/theme-route-r18.md` | P5 | [PENDING: S0xx-pending → assigned id(s)] | `.ufo/waves/round-18/fetch/<seat>/receipts.jsonl` [PENDING] | [PENDING: covered / open] |

Host versions by file read of `/var/log/pacman.log` only: walker 2.17.2-1
(line 2929), elephant 2.22.1-1 (line 3095), omarchy checkout tag v3.8.4 (read as
`.git` bytes). [PENDING: confirm each line still matches on re-read.] No
observed behaviour; host binaries stay `[UNK]`.

### Claim C3 — frozen tripwire gate

| Check | Expected | Observed |
|---|---|---|
| `--frozen` on committed snapshot | exit 0, `MADO_TRIPWIRE_FROZEN: frozen_match` | [PENDING] |
| tampered copy of one input | exit 2, `snapshot_tampered` | [PENDING] |
| unlisted `*.jsonl` under `inputs/` | exit 2, `snapshot_tampered` | [PENDING] |
| perturbed expected finding | exit 1, `frozen_verdict_mismatch` | [PENDING] |
| provenance: source sha256 equals `round-17/evidence/session-index.json` where listed | all equal | [PENDING] |
| frozen selftest suite | N/N | [PENDING] |
| existing suites core / compound / hardening / w2-regressions | 9/9, 16/16, 33/33, 30/30 at `962919ce…` (round 17) | [PENDING: sha after edit; N/N] |

### Capabilities (round 18)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| frozen tripwire replay (digest-pinned gate) | [PENDING: `--frozen DIR` verifies committed snapshot digests, then compares exit, label and the finding multiset against a pinned expected verdict; a tampered snapshot exits 2] | [PENDING: receipt paths for frozen_match and snapshot_tampered] | [PENDING: 18 only if the frozen run is demonstrated; otherwise the row stays `probe`] |

A row enters only through a round that demonstrates the capability running.
A replay over a committed snapshot is not a claim about live transcripts or
prevention.

### Sources, saturation and retirement

Sources before 71 (A 64, C 6; mined 56, rejected 7; round-17 committed) →
[PENDING: after, with A/B/C, mined/queued/rejected]. Saturation before 9.0 /
N=3 → [PENDING]. Retired: [PENDING: none, or with justification].

### Harm watch

Before values are round-17 committed results at `f71ccbe` unless marked.

| Harm item | Before | After |
|---|---|---|
| hermetic selftest (gate sha `fba82a66…`) | 372/372, exit 0 | [PENDING]; if the gate moved, re-cut the baseline and say so |
| classifier | 52/52 | [PENDING] |
| tripwire suites core / compound / hardening / w2-regressions | 9/9, 16/16, 33/33, 30/30 | [PENDING] |
| U routes | 7/7 | [PENDING] |
| navigation | 32/32 | [PENDING] |
| census | exit 0; historical W04 S030, S042, S045 retained | [PENDING] |
| freshness file-plane | 29/29 (round 12; not re-measured in round 17) | [PENDING: unchanged unless re-measured] |
| jj routed fixes: `tools/mado-verify.sh` rc capture; `.gitignore` `.ufo/state/` | [INFERENCE] defect per JjAuditMado F10 (`:3406`), baseline state not re-read this round | [PENDING: failing git-stub scenario output; `.gitignore` line] |
| host pause: no package query, transaction, service, compositor, input or screenshot operation | carried | [PENDING: attestation with command list] |
| R15-V1 libinput partial upgrade | operator-owned, `[UNK]` | unchanged; not remediated by this round |
| `.ufo/waves/round-18/evidence/census-start.txt` | recorded at pre-registration | [PENDING: census-end] |

Per-axis verdict (author, bounded): [PENDING: calibration; coverage;
operability; freshness and depth/adjacency, unscored unless re-measured]. No
axis harmed by lane action: [PENDING: confirm or name the harm]. Admission not
asserted; independent closure remains required.

### Planned (round 19; candidates, no mission opened)

1. freshness — re-anchor present-tense pins moved by the 2026-10-20 `-Syu`:
   walker 2.17.2 and hyprland 0.56.2-4, by file bytes and `/var/log/pacman.log`
   only. No package query, even read-only, while the host pause holds.
2. operability — remaining adversarial tripwire misses that recur in real
   transcripts: variable `bash -c` recipes and helper-wrapped spawns. Close each
   or record it as a permanent limit. Round 17 pinned 4/26 adversarial misses as
   known limits; [PENDING: round-18 count].
3. coverage — [PENDING: next undocumented surface under rubric V, only if P3 and
   P5 are both covered at round 18 close; otherwise carry P3/P5 as open].
