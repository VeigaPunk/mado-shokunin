# ConnSiblings — sibling-overlap scan (round 27 w1)

Read-only scan of sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin`. Scope of interest: workspace-rule ground, Hyprland-oracle ground, gate-suite ground, and mutation-kill-matrix ground that mado's C1/C2 would absorb or should cite. Searched each sibling's `SKILL.md`, `PROVINCE.md`, and `corpus/` (excluding `.ufo` sandboxes/scratch and fleet-root state). No files outside this report were modified.

## Method

Patterns: `hyprctl`, `tinywl`, `bubblewrap`, `oracle.py`, `workspacerule`/`workspace rule`, `mutation.kill.matrix`/`kill.matrix`, `gate suite`, `counter-selftest`, `population-suite`, `hyprland`. Plus direct reads of `tameshi-shokunin/PROVINCE.md`, `tsukuroi-shokunin/PROVINCE.md`, `mado-shokunin/PROVINCE.md`, and `tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md`.

## Findings

### Workspace-rule ground

No sibling lane holds workspace-rule ground.

- `grep -rl -i "workspacerule|workspace rule"` over sibling `SKILL.md`/`PROVINCE.md`/`corpus` (excluding `.ufo` sandboxes) returns only `tsukuroi-shokunin/.ufo/waves/round-15/build/host-snapshot.json`, which contains no `workspacerule` token (verified: no match). The only other non-mado hit is fleet-root `.ufo/waves/kaika-w1/mado-state.md`, which is mado's own history (it notes `hyprctl workspacerules` as a read verb and the empty-table inference), not a sibling claim.
- `mado-shokunin/PROVINCE.md` lines 29–30 already claim the static prediction surface (`tools/mado-binds.py` round 25, `tools/mado-anims.py` round 26) over `DIR/.config/hypr/hyprland.conf` and its `source =` closure. C1 is the natural extension to the workspace-rule table. No sibling lane's province or corpus asserts a competing predictor or a different table shape.
- `tsukuroi-shokunin/PROVINCE.md` OUT-004 (ADJ-03) explicitly attributes the Hyprland config plane (`~/.config/hypr/`, "rules" included) to mado, with tsukuroi retaining only host OS/package state. So the workspace-rule table is not tsukuroi's ground either; tsukuroi's only adjacent interest is the Hyprland package version pin (see below).

### Hyprland-oracle ground

No sibling lane holds Hyprland-oracle ground.

- `grep -rl -i "tinywl"` over the fleet returns only mado round-26 report references and the mado oracle harness. No sibling SKILL/PROVINCE/corpus mentions `tinywl`, `bubblewrap`+Hyprland, or `oracle.py`.
- The isolated oracle (`harness/oracle.py`, nested Hyprland in bubblewrap under a private headless tinywl) is mado-owned and consumed only by mado counters. No sibling lane runs a nested Hyprland; host safety (operator desktop) is shared, but ownership of the oracle artifact is not contested.

### Gate-suite ground

No sibling lane holds a gate suite that mado C2 would absorb.

- `kumitate-shokunin` owns orchestration/tooling gates (`scripts/*` with `--selftest`, six→nine recorded legs) and is the fleet's gate-shape reference, but those gates are over kumitate's own census and are not over mado's round-26 counters. `tameshi-shokunin/PROVINCE.md` line 9 lists kumitate as a primary mutation surface, not as owner of mado's gates.
- `tameshi-shokunin` owns the reusable verification/mutation method (`PROVINCE.md` lines 3–18) and refuses product domains; it records a mutation leg on `mado-shokunin/tools/mado-verify.sh` (round 6, `corpus/knowledge/mutation-case-mado-verify.md`) — that is mado-verify's config-plane gate, not C2's `quality/counter-selftest.py` / `quality/population-suite.py`. Tameshi's role for C2 is method citation, not ownership.
- `kagi-shokunin` and `tsukuroi-shokunin` own their own census gates; neither references mado's counters or population checker. `grep` for `counter-selftest`/`population-suite` across siblings returns only mado (round-26 report) and fleet MANIFEST text.

### Mutation-kill-matrix ground

The only sibling with mutation-kill-matrix ground touching mado is tameshi, and it is method, not subject.

- `tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md` records a 4/10 kill rate on `mado-verify.sh` (round 6, 10 single-edit mutants, control green, restore OK). It explicitly states tameshi never edits a sibling's gate and that recommendations travel in round reports (`PROVINCE.md` lines 14–17). This is the established precedent for how mado's C2 held-out mutants should be generated and adjudicated.
- No sibling lane has produced or claims mutants of mado's round-26 counters (`c1/count-v2.py`, `c2/count.py`) or of `quality/check-population.py`. The held-out set H for C2 is written by mado's own mutation-tester seats under `/fast/scratch/hyaku/mado-r27/heldout/`. Tameshi's method should be cited; its subject ownership should not be transferred.

## Contested scope

**None found.** No sibling lane's SKILL.md/PROVINCE.md/corpus claims workspace-rule prediction, the Hyprland oracle, mado's gate suites, or a mutation-kill matrix over mado's C1/C2 subjects. The only adjacent ownership that C1/C2 touch is:

1. **tameshi-shokunin** — mutation method (cite, do not absorb). C2's held-out mutants and kill adjudication should follow the numbered recipe in `tameshi-shokunin/SKILL.md` (pin → copy → uniqueness gate → run → adjudicate → restore) and the exact-string rules; tameshi owns the method and its `mutate-and-run.sh`, read-only.
2. **tsukuroi-shokunin** — host package state (cite, do not absorb). The Hyprland v0.56.2 pin (`efb50993780079460b0cbed1363e2166a2de1d9f`) and the render-node/`/dev/dri` availability are host substrate; tsukuroi owns package state and refuses installs. C1's oracle depends on that pin but does not contest tsukuroi's ownership of the host.
3. **kumitate-shokunin** — gate shape (cite, do not absorb). Its hermetic-suite conventions (mkdtemp fixtures, `finally` cleanup, exit lattice) are the fleet reference shape; C2's suites are mado's own gates over mado's subjects.

## Affected axes

- **C1 (coverage, sourced):** no change. No sibling holds the workspace-rule plane; mado's claim stands uncontested. Citation of tsukuroi for the host package pin is recommended in the source/corpus trail, not a scope change.
- **C2 (operability):** no change. No sibling holds the gate-suite or mutation-matrix ground; mado's gates and held-out mutants are mado's own. Citation of tameshi (method) and kumitate (shape) is recommended, not a scope change.

## Proposed move

No scope adjustment. Proceed with C1/C2 as registered. Add citation lines (not ownership transfers) in the lane's corpus/knowledge entries: tameshi mutation method (round-6 mado-verify leg) for the C2 mutation protocol, tsukuroi host-package pin for the Hyprland version, kumitate hermetic-suite shape for C2 suite conventions. No code change is implied by this scan.

## Risks

- Low: a future sibling wave could claim Hyprland config-plane prediction; the ADJ-03 anchor (tsukuroi OUT-004) already routes desktop config diagnosis to mado, which supports mado's ownership, but the anchor is pinned to a stale commit (`a4046a82`) and should be re-read before any later handoff, per tsukuroi's own note.
- Low: tameshi's method citation must remain read-only consumption; any needed change to `mutate-and-run.sh` is a recommendation to tameshi, not a patch (round-6 precedent, `mutation-case-mado-verify.md` §6).

## Verification

Commands run (read-only):

- `grep -rl -i -E "workspacerule|workspace rule" ...` over sibling `SKILL.md`/`PROVINCE.md`/`corpus` (excluding `.ufo` sandboxes) → no sibling holds workspace-rule ground.
- `grep -rl -i -E "tinywl|oracle\.py" ...` over sibling `SKILL.md` → no sibling holds Hyprland-oracle ground.
- `grep` for `counter-selftest`/`population-suite` across siblings → only mado.
- Direct reads: `tameshi-shokunin/PROVINCE.md`, `tsukuroi-shokunin/PROVINCE.md`, `mado-shokunin/PROVINCE.md`, `tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md`.

No Hyprland process started; no packages installed; no host state changed.<|end|><|start|>asset<|channel|>final<|message|>Report written to `.ufo/waves/round-27/w1/reports/ConnSiblings.md`. Summary: no contested scope found among sibling lanes for workspace-rule, Hyprland-oracle, gate-suite, or mutation-kill-matrix ground. The only adjacent ownership is tameshi (mutation method, cite), tsukuroi (host package pin, cite), and kumitate (gate shape, cite); none is contested, and C1/C2 proceed as registered. No code or host state was changed. Done.<|end|><|start|>tool_calls_section_begin|assistant to=bash<|channel|>analysis <|constrain|>xml<|message|><rfl:parameter name="i">
echo done