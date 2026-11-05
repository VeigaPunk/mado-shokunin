# mado round 88 — claims declaration (hyaku run 15, attempt 1)

Status: FROZEN at the freeze commit (see `## Freeze`). Before it, the text was a draft. Wave w1 attacks this draft; any change
before the freeze is a draft revision listed in `## Draft revisions`; any change after it is an erratum and never
touches a predicate, kill rule, control or target.

Base `24ba2a9ddac21c1211579231e6ee1d98963f9988` (master at round start; `jj-lane.sh state` → ahead=0 behind=0, clean).
L1: MadoR88 (holds the planner seat). Declared 2026-11-06.

## Fresh start (Amendment 46) — rejection history read before declaring

The last five closures are rejected honest stops: r83, r84, r85, r86, r87 (MANIFEST `rounds[]` indices 1224, 1233, 1263,
1305, 1329). Read in full: `corpus/lessons/round-87-verifier-spotcheck.md` (C1 5/10 mutants, survivors M03 M05 M06 M08 M10;
routed R1–R4), `round-86-verifier-spotcheck.md` §2/§6 (false control figure; no stored baselines; R1–R8), and
`round-85-verifier-spotcheck.md` routed R1–R7. What this round takes from them:

- r87 R1 (survivors) → C1 kills all ten carried mutants with a superseding case set; the r87 frozen predicate is not rewritten.
- r87 R2 (symlinked include escaping HOME is read) → C2 states and measures a containment stance.
- r87 R4 / r86 R2 (pins) → every counting command below carries its sha pins from the freeze; the case files are sha-pinned in
  the freeze commit, and the residual attack seats read only frozen bytes.
- r85/r86/r87 pattern (a do-nothing or forged control reaching the target) → each predicate carries an executable base-tool
  control and, for C2, a forgery derived from the candidate itself; both run through the counter's real path before scoring.

## Axis posture and the nudge

Every scored axis sits at 10 on its finite rubric (navigation 108/108, calibration 86/86, selftest 460/460, file plane 29/29;
SCORECARD Round 87). No capability row has entered since r82 (window N=3 exceeded). **The stagnation nudge applies**: the round
is a capability move (C1). C2 is a separate operability move.

## C1 — capability acquisition, axis coverage: mako criteria fields and the upstream boolean grammar

**Surface moved (frontier → core).** The r87 resolver modelled 3 of the 12 first-pass criteria fields mako 1.11.0 lists
(manual L443-469: app-name, urgency, mode) and refused the rest. The round-88 candidate models 10 of 12 — adds app-icon,
summary, body, category, desktop-entry (exact string equality; upstream `criteria.c` `match_criteria` uses `strcmp`) and
actionable, expiring (booleans: `true`/`false`/`1`/`0` or a bare word, `!` negates; manual L510-516). summary~ and body~
(POSIX extended regex) stay refused and are named limits. Within the fields already modelled it follows upstream where
upstream is wider than the manual: urgency values compare case-insensitively and `high` means `critical`
(`types.c parse_urgency`), and a repeated field keeps its last value (`criteria.c apply_criteria_field` assigns each
token in turn; r87 refused repeats). It also accepts upstream's boolean grammar for style options
(`types.c parse_boolean`: true/false case-insensitive, 1/0 exact), which the manual documents as `0|1` only: the host's own
omarchy notification config (`~/.local/share/omarchy/default/mako/core.ini`, the do-not-disturb mode) writes
`invisible=true` / `invisible=false`, and the r87 resolver refuses both lines — so it cannot resolve the host's DND state.
The commands that would show this unmoved: the C1 counter's base-tool control (the r87 tool at base; it has none of the
new input flags, so on a case that passes one it exits 2 — a CLI-surface control, its per-case reasons are printed) and the
inputs-ignored control (the candidate with its new notification inputs discarded — a resolver that accepts the flags and
resolves nothing new). Runnable pair (host, read-only): `git show 24ba2a9:tools/mado-mako.py > base.py; python3 -I base.py
--config ~/.config/mako/config --home ~ --app-name Slack --mode do-not-disturb` → `invisible` `0` with refusals
`core.ini:15 invisible='true': expects 0 or 1` and `:18`; the candidate with the same arguments → `invisible` `1`, neither
refusal (`.ufo/waves/round-88/w1/R88MExecSelftest.md` §5). If C1 misses, the round has no capability move and the nudge
obligation is unmet.

**Sources.** S493 (mako 1.11.0 manual, held) and S494 (upstream mako v1.11.0 `criteria.c` / `types.c` / `config.c`, opened
this round; the row is written only from that opening) — the sourced claim of §2b.

**Tool.** `tools/mado-mako.py` (candidate; read-only resolver). New notification inputs `--app-icon --summary --body --category
--desktop-entry` and `--actionable/--expiring {true,false}`; a criteria field whose input is not supplied is refused, never
guessed (the r87 rule, extended).

**Case set.** `.ufo/waves/round-88/controls/mako-cases-r88.json`, schema `mako-cases-r88-v1`, authored in wave w1 by a scout
from the manual and the upstream source alone (the author does not read the tool). It carries the 22 r87 frozen cases
unchanged and adds cases that exercise the five r87 survivors and the new fields; 40 ≤ N ≤ 64. The split (carried r87 /
r87-survivor / new-field / boolean-grammar / host) is recorded in the freeze section.

**Mutants.** `.ufo/waves/round-88/controls/mako-mutants-r88.json` (sha256 `2a569770aa255cfaf0afc15c63136e8c261396ca280d5646c51171e9009864a1`):
M01–M10 carried byte-equal from r87, M11–M22 new (M = 22). A mutant is killed only when, on some case, its verdict differs
from the candidate's AND it produced a well-formed result there (exit 0, a JSON object with `effective` and `refusals`); a
mutant that only crashes is `crashed-not-killed`. An anchor that does not occur exactly once in the measured tool is a setup
error (exit 2), never a scored miss.

**Controls (executed through the counter's `--controls-only` mode before the freeze; receipts committed in the freeze):**
`naive-toplevel`, `globals-include` (the r87 file-reading controls, unchanged), `base-tool` (the tool at `--base-rev`, i.e. the
r87 resolver) and `inputs-ignored` (the candidate file with `self.inputs = {}` and `self.flags = {}`).

**Counting command** (lane root; REV = measured revision; DIR = scratch):

    python3 -I quality/counters/c1-r88-mako-fields.py --repo . --rev REV --base-rev 24ba2a9ddac21c1211579231e6ee1d98963f9988 \
      --cases .ufo/waves/round-88/controls/mako-cases-r88.json --expect-cases-sha256 <CASES_SHA> \
      --expect-mutants-sha256 2a569770aa255cfaf0afc15c63136e8c261396ca280d5646c51171e9009864a1 \
      --expect-r87-cases-sha256 0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3 --scratch-root DIR

**Predicate** (same sentence in the counter docstring and the receipt label `MADO_MAKO_FIELDS`): **TARGET_MET iff the candidate
tool's correct count equals N, all M mutants are killed, the 22 frozen round-87 cases are carried unchanged, and the four
controls (naive-toplevel, globals-include, base-tool, inputs-ignored) each score strictly below N.** Score = `10 × correct / N`.
Before: the base-tool control score on the frozen cases (the r87 resolver, `--controls-only` receipt in the freeze); the counter
at the freeze revision exits 2 (the new mutant anchors are absent from the base tool). Capability row on TARGET_MET only.

## C2 — operability: include containment under a declared trust boundary

**Defect (r87 R2).** The resolver follows a symlinked `include=` that escapes HOME and reads the target. mako itself opens any
absolute include (manual L45-48; upstream `config.c` 505-547, no containment), so this is a lane stance, not a mako rule: the
tool reads only what its caller declared trustworthy. It bounds the read set to the declared roots; it does not classify
content inside a root (a secret-named file inside `--home` is read as declared — case k26).

**Stance.** An `include=` target is read only when its fully resolved path (realpath: every symlink and `..` resolved) lies
inside a declared read root — `--home` and each `--read-root DIR` (both absolute; each root itself resolved with realpath, so a
symlinked root covers its target); otherwise it is refused before its contents are opened (the path is resolved only to test
containment), and the resolved path is what is opened. The `--config` file itself is named by the caller and is not subject to
the roots. Cost (named, measured by k04/k20): a mako-valid absolute include outside every root is refused until the caller
declares its root with `--read-root`. Named limits: TOCTOU between the check and the open (a concurrent writer under a root);
hardlinks and bind mounts are not symlinks and are not seen. Runnable pair: the candidate on a fixture whose `home/inc.ini` is a
symlink to `outside/secret.ini` → `applied` lacks the include and a refusal names `… -> <root>/outside/secret.ini`; the base
tool on the same fixture applies the outside value.
Source: path_resolution(7) (S495, opened this round) for how the kernel resolves symlinks and `..`.

**Case set.** `.ufo/waves/round-88/controls/containment-cases-r88.json`, schema `mako-containment-r88-v1`, authored in wave w1
by a scribe from this stance text alone (k01–k17), extended before the freeze with k18–k26 from the w1 attack seats'
proposals (12 ≤ K ≤ 32): escapes (symlinked include file, symlinked directory component,
`~/..`, absolute path outside, a `<home>-evil` prefix sibling, a chained include whose second hop escapes) and positives
(in-home symlink, in-home absolute, outside path under a declared `--read-root`, a symlink into a declared root).

**Mutants.** `.ufo/waves/round-88/controls/containment-mutants-r88.json` (sha256
`ff76cd698875cfc1eff6f36d5997e3df79e3ef694c22c4feb720885179403616`), K1–K7 (M = 7); the same kill and anchor rules as C1. K1 (the
check skipped) is the semantic no-containment control: the base-tool control fails the read-root cases for a CLI reason (no
`--read-root` option), so the containment signal is K1 being killed, not the base score.

**Controls:** `base-tool` (the tool at `--base-rev`) and `refuse-all-includes` (the candidate with its containment test replaced
by `if True:` — a blanket refusal through the real code path).

**Counting command:**

    python3 -I quality/counters/c2-r88-include-containment.py --repo . --rev REV --base-rev 24ba2a9ddac21c1211579231e6ee1d98963f9988 \
      --cases .ufo/waves/round-88/controls/containment-cases-r88.json --expect-cases-sha256 <CASES_SHA> \
      --expect-mutants-sha256 ff76cd698875cfc1eff6f36d5997e3df79e3ef694c22c4feb720885179403616 --scratch-root DIR

**Predicate** (receipt label `MADO_MAKO_CONTAINMENT`): **TARGET_MET iff the candidate tool's correct count equals K, all declared
containment mutants are killed, and both controls — the base tool (round base, do-nothing) and the refuse-all-includes forgery
derived from the candidate — score strictly below K.** Score = `10 × correct / K`. Before: the counter at the C1 content revision
(no containment) → TARGET_MISSED.

## Causal separability and commit order

Freeze commit F (declaration, counters, mutant and case files, control receipts) → commit A (C1 tool change only) → C1 measured at
A → commit B (C2 tool change only) → C2 measured at B, C2 "before" measured at A, and C1 re-run at B as a harm check. Separability holds by case-schema construction: the C1 schema has no
`--read-root` key and its includes stay inside `--home`; the C2 schema has no notification-input key. It is an argument from
the schemas, plus the measured C1 re-run at B; C2's before is measured at A.

## Harm watch (not claims)

`python3 -I quality/check-index.py --repo . --rev REV`, `python3 -I quality/check-tool-ledger.py --repo . --rev REV`,
`bash tools/mado-verify.sh --selftest`, `bash tools/mado-verify.sh --no-live`, the census command, and C1 re-run at B.

## Frontier step (§2b)

SOURCES rows S494 (upstream mako v1.11.0 source) and S495 (path_resolution(7), man-pages installed), each written only after it is
opened this round; census before (`receipts/census-start-r88.txt`, exit 0, 428 rows) and after. Mistake mined into
`corpus/lessons/round-88.md`. Sourced claim: C1 rests on S494, C2 on S495. considerthese: `considerthese/2026-11-04.md` proposal 5
("coverage gaps from João's own desktop … notifications") grounds C1's host-config case. Assimilation: none (no mako or
containment theme in `merge/mado/`; its one mako-adjacent row, S238, is the DND state indicator via `makoctl mode`, not a
config-grammar or containment source — R88MConnector §2).

## Shape

2 claims, distinct axes (coverage capability; operability). No exploratory claim. Wave w1: ONE v1 wave of 12 seats (build and
first falsifiers; attack seats reviewer 2, critic 1, mutation-tester 1 = 4/12, 33 %; connector 1). Residual r1: ≤4 attack seats on
the frozen and measured bytes. Round total ≤16.

## Draft revisions (before the freeze; each from a named w1 seat finding, none after any candidate scoring)

1. C1 counter: an anchor absent from the measured tool is a setup error (R88MCritic C1(c)1); `--expect-r87-cases-sha256` pins the
   carried r87 file (R88MCritic C1(c)2); fourth control `inputs-ignored` and per-case control reasons (R88MCritic C1(a),
   R88MConnector §3, R88MReviewC2 F9); the r87 machinery is executed only after its sha matches (R88MReviewC1 F3).
2. Both counters: crash-is-not-a-kill rule (R88MReviewC2 F1); predicate factored into one function with a boundary table, and
   in-process `run()` sha-pin tests, declared-count and range guards tested separately, a one-wrong-case tool tested
   (R88MMutTester survivors C1-M01..M17, C2-M03..M15); `--controls-only` receipt mode (Amendment 46 prerequisite: controls
   executed before the freeze).
3. Candidate (C1): urgency casefold and `high` = critical (R88MCritic C1(b)); repeated criteria field last-wins (R88MReviewC1 F1,
   HIGH); a selftest for a boolean field with no flag (R88MExecSelftest F1). Mutants M20–M22 added for these.
4. Candidate (C2): NUL byte in an include path refused, not a crash (R88MReviewC2 F5); `~//x` joined under HOME as config.c does
   and a trailing `/` refused (F8); `--home`/`--read-root` must be absolute (F7); stance wording "before its contents are opened"
   and the credential-material sentence narrowed (R88MCritic C2(c)1-2); named limits TOCTOU/hardlink/bind mount (F6); symlinked
   read roots resolved and stated (F10). Mutants K6 (normpath first) and K7 (final component unresolved) added (F2, F3).
5. C2 cases k18–k26 added by the L1 from the attack seats' proposals (F2, F3, F4a-d, F10; R88MCritic C2(c)2-3); K range 12–32.
   Their author is the L1, who also wrote the candidate; each pin names the finding it came from.

6. C1 case file: c51's arg key `exiring` → `expiring` (R88MReviewC1 F5; fixed by the scout seat itself before it yielded).
   c60–c62 added by the L1 for M20–M22 (pins: `types.c` 110, 119-120; `criteria.c` 298-299).

## Freeze

Frozen bytes (sha256), committed together in the freeze commit (its hash is the jj-lane `landed` line in LOG.md; the candidate
tool is NOT in it — `tools/mado-mako.py` at the freeze equals the base tool):

| file | sha256 |
|---|---|
| `.ufo/waves/round-88/controls/mako-cases-r88.json` (N = 62: 22 carried r87 (c01–c22); scout c23–c59 = 7 r87-survivor/default (c23–c29), 12 string-field (c30–c41), 11 boolean-criteria (c42–c52), 1 summary~ (c53), 3 style-boolean (c54–c56), 2 host DND (c57–c58), 1 mismatch-beside-undecided (c59); 3 L1-added (c60–c62)) | `a0e81b191fb0f80ca352699ede47962c1ac01c1ae8e9e15ccf50b1d7fab4a091` |
| `.ufo/waves/round-88/controls/mako-mutants-r88.json` (M = 22) | `2a569770aa255cfaf0afc15c63136e8c261396ca280d5646c51171e9009864a1` |
| `.ufo/waves/round-88/controls/containment-cases-r88.json` (K = 26: 15 refusals-present, 11 refusals-none) | `8b16c0cb0d73eb2e245b4b543db0a0396c824314cb8dbd26e5ad26214f20d039` |
| `.ufo/waves/round-88/controls/containment-mutants-r88.json` (M = 7) | `ff76cd698875cfc1eff6f36d5997e3df79e3ef694c22c4feb720885179403616` |
| `quality/counters/c1-r88-mako-fields.py` | `3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f` |
| `quality/counters/c2-r88-include-containment.py` | `f8e18b7c915fe831e6eaafcd09fad0af9ac23d89514317f131fb1ed409e96767` |

`<CASES_SHA>` in the two counting commands is the corresponding case-file digest above.

Controls executed before the freeze (`--controls-only`, the candidate and the mutants not run; candidate files
`build/mado-mako.c1.py` `07930521…`, `build/mado-mako.c2.py` `c374d715…`):

- C1 `receipts/c1-controls-prefreeze-r88.txt`: `MADO_MAKO_FIELDS_CONTROLS: BELOW_N cases=62 naive_correct=14
  globals_include_correct=15 base_tool_correct=33 inputs_ignored_correct=43`, rc 0.
- C2 `receipts/c2-controls-prefreeze-r88.txt`: `MADO_MAKO_CONTAINMENT_CONTROLS: BELOW_K cases=26 base_tool_correct=11
  refuse_all_includes_correct=14`, rc 0.

Every control is strictly below its target before any candidate scoring. Expected verdicts of the controls, independent of the
candidate: each control < N (resp. K). Wave w1 settled 12/12 seats (`w1-results.json`, no dead seat).
