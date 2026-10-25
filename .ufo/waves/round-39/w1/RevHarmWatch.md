# RevHarmWatch — mado round 39, wave w1 (hyaku run 7, 2026-10-25)

Data tip audited: `457d1b125932c1e0d797061a2156b917bcd7edaa` ("round-39: freeze registration + base receipts + inherited r38 seat reports", 2026-10-25 16:00:14 -0300). Base: `08be4eb7fd13358ed29b096e8924005d46ac409c`.
Raw outputs saved in `.ufo/waves/round-39/w1/RevHarmWatch/`: `selftest-tip.txt`, `nav-tip.txt`, `census-tip.txt`, `hosttree-live-check.txt`, `hosttree-copy-check.txt`.

## Battery results — all green

1. **Selftest** — `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed`, exit 0 (16.9 s). Baseline `receipts/selftest-base.txt` (committed at `.ufo/waves/round-39/receipts/selftest-base.txt`): `460/460`. **No regression.**
2. **Navigation** — `python3 -I quality/check-index.py --rev 457d1b125932c1e0d797061a2156b917bcd7edaa --repo .` → `MADO_INDEX: rev=457d1b1… indexed=55/55 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0. Baseline `nav-base.txt`: 55/55 at base. **Complete, unchanged count** (the round's new entry row is expected only at the round-end data commit).
3. **Census** — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → **exit 0**, ending `mado ok …/corpus/SOURCES.md`. Warning set is byte-identical to the frozen baseline `.ufo/waves/round-39/receipts/census-before.txt`: 7× `W04 duplicate url` (S030, S042, S045, S097, S119, S120, S121) + 1× `W01 S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md`. **Delta vs baseline: zero; no new warnings introduced this round.** (W01 S277 pre-exists at base; not a round-39 effect.)
4. **Lane worktree** — `git status --porcelain` (read-only) → untracked only, all expected: `.ufo/waves/round-39/w1*` (wave seat dirs + harness dispatch artifacts `w1-dispatch.json`/`w1-spec.json`/`w1-plan.out`/`w1.ready*`; `w1-plan.err` and `w1-run.err` are **0 bytes** — no dispatch errors), `quality/counters/c3-r39-options.py` and `tools/mado-options.py` (declared C2 deliverables, pending the round-end data commit — consistent with C2's target being measured "at the data commit"). **Zero modifications to tracked files; nothing outside the wave dir + the two declared C2 files.**
5. **Host config trees** — SctHostTree manifest `.ufo/waves/round-39/w1/SctHostTree/manifest.sha256` (53 entries, `$HOME`-relative: `.config/hypr/*`, `.config/omarchy/current/theme/*`, `.local/share/omarchy/default/hypr/**`, `.local/state/omarchy/toggles/hypr/*`; captured 16:10, after the 16:00:14 freeze — i.e. before any round-39 data commit, so the comparison is valid).
   - Live host: `cd /home/vgpnk && sha256sum -c <manifest>` → **53/53 OK, exit 0** (`hosttree-live-check.txt`).
   - Copy: `cd …/SctHostTree/real-tree && sha256sum -c ../manifest.sha256` → **53/53 OK, exit 0** (`hosttree-copy-check.txt`).
   **Manifest = copy = live host; zero config-tree byte drift during the round.**

## Freeze-commit delta audit (base 08be4eb → tip 457d1b1, `git diff --numstat`)

Exactly 12 files, 709 insertions, 7 deletions — all declared freeze content: `registration.md` (+110), `.ufo/waves/round-39/c1/manifest.json` (+256), 7× `.ufo/waves/round-39/receipts/*` (+160), inherited r38 reports `RevEntryBound.md` (+53), `RevRegistry.md` (+8), `ScoutS253.md` (+126/−7). **No counter, no axis file, no `corpus/` file touched** — the "new predicate" kill rule is not tripped by the freeze.

## Findings by severity

**Blockers / majors: none.**

**Minor (observation, actionable by report writer):**
- O1 — Inherited `ScoutS253.md` was committed **non-verbatim**: the 7 deletions update stale tip pointers `85276d4` → `c46f868` (r38 errata tip) in three "current HEAD" references. Benign class of edit (same as r38 errata), but the round report should name this delta when claiming the r38 reports were "committed in the freeze", since the registration says "inherited as uncommitted lane-authored work; committed in the freeze commit" without mentioning edits.

**Info:**
- I1 — Fleet-repo churn observed (outside my lane, not writable by me): fleet `.ufo/state/*report-baseline` (9 lanes) and `.ufo/watchdog.log` updated 15:40–16:13 — normal orchestrator/reporting machinery during the multi-lane launch window. Fleet-root untracked `corpus/knowledge/journalctl-v262-field-filter-r36.md` has mtime 16:08:07 (mid-round); writer not attributable from mtimes alone, name suggests fleet-level round-36 ledger work, not mado's config-option scope. No tracked fleet path outside `.ufo/state`+`watchdog.log` is modified, so no evidence of any mado seat writing the fleet repo.
- I2 — Sibling-lane internals are not visible to fleet git (lanes are separate repos), so cross-lane write *absence* is not provable read-only from here; the strongest available evidence is (a) zero fleet tracked-path drift beyond harness files, and (b) my session wrote only under `…/round-39/w1/RevHarmWatch/`. Recorded as a verification gap, not a finding.

## Residual risk / verification gaps

- C1/C2/C3 claim counters were **not** run here (other seats own them; my scope was the harm battery). Note for Main: at the current tip the C2 deliverables are untracked, so any counter reading blobs at `--rev` will see `tool=absent` until the data commit lands — that is expected pre-data-commit state, not a defect.
- Host-tree manifest covers SctHostTree's declared 53-file scope only; files outside it (e.g. other `$HOME/.config` subtrees) were not hashed by anyone, so "no config tree bytes changed" is proven for the manifest's scope.
- Tooling installs: **none** (battery used only in-repo scripts, system python3/sha256sum/git; pacman untouched per host pause).

## Verification gap note

No LSP server answered for this lane's shell-only evidence set; all checks are direct command executions with captured exit codes (grep used only as literal filter on captured output). Nothing in this report relies on unverified semantic claims.
