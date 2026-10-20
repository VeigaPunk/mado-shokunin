# ReviewNoHarm — U6 documentation route: gate unchanged, no source/config mutation

Scope: adversarial static review of whether a bounded U6 input-debugging note can land with the existing gate unchanged and no source or config mutation. Read-only. No gate, selftest, regression, frozen replay, measure probe, census, test, build, lint, format, smoke run, live probe, input read, or install was executed. Commands run: `sha256sum`, `git rev-parse HEAD`, `git status --porcelain`, `git diff --stat HEAD`, `git show HEAD:tools/mado-verify.sh | sha256sum`, and file reads. Tool installs or updates by this seat: none.

## Verdict

**CONDITIONAL ACCEPT.** The premise holds at the inspected tree: the gate bytes are unchanged, the gate reads no corpus file, and no source or config mutation is needed for a documentation-only U6 note. The note may land only if conditions A1–A9 hold and none of R1–R8 trips.

## Observed facts (HEAD `ea0446f`)

| Fact | Evidence |
|---|---|
| Gate sha256 `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`, 3,711 L, same at HEAD and worktree | `sha256sum tools/mado-verify.sh`; `git show HEAD:tools/mado-verify.sh \| sha256sum`; `git status --porcelain -- tools` → 0 lines |
| Frozen gate copy matches; frozen harness matches sibling harness `75ed934d…adc5` | `.ufo/waves/round-14/frozen/gate.sh`, `frozen/harness.sh`, `../tameshi-shokunin/tools/mutate-and-run.sh` |
| Frozen pins cover gate and harness only; corpus, SOURCES, README, SKILL are not frozen inputs | `.ufo/waves/round-14/frozen/expected.json:2-7` |
| Gate has no runtime read of corpus, SOURCES, README, SKILL, LOG or SCORECARD. Matches are comments (`tools/mado-verify.sh:32, 1548, 1610, 2549, 2701, 3244`) or fixture/omarchy strings (`:636-637, 3273`). Its git calls target the omarchy checkout (`:3382-3406`) | grep of `tools/mado-verify.sh`, non-comment hits only |
| Gate self-path derives fleet root by `dirname` ×3 for regression (`:1643-1644`). Moving the gate breaks regression; no move is proposed | `tools/mado-verify.sh:1643-1644` |
| Round-14 committed bindings cover gate, measure.py, frozen files and spec. No evidence `.txt` and no corpus file is bound | `.ufo/waves/round-14/evidence/committed-bindings.json:2-13` |
| Merge screen (SKILL registry `mado-source-merge`): canonical URL = first bare URL, fragment and trailing slash stripped. Active (queued/mined) same-URL rows need `teaches` opening `supersedes S<id> -`, else exit 1 | `.ufo/waves/round-13/w1/reports/MistakeFix.py:31-46`; `SKILL.md` registry row for `mado-source-merge` |
| S007 (queued, libinput tools) URL is `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`. `latest` is a moving ref; the row has no immutable revision | `corpus/SOURCES.md:19` |
| S043 (mined, wl_registry / core XML) canonical URL is `https://wayland.freedesktop.org/docs/html/apa.html`; its fragment is stripped by the screen | `corpus/SOURCES.md:55`; `MistakeFix.py:33` |
| `measure.py` U-item join credits any `covers: U<N>` note with a mined A/B row used-by it. Only U4 and U5 have facet gates. U6 currently gets no facet check | `.ufo/waves/round-14/measure.py:154-200` |
| Navigation requires exactly one README row per knowledge note | `measure.py:202-212`; `corpus/README.md:10-39`; `SCORECARD.md` round-1 counting command |
| Safe boundary rules: no firing or injection; provinces read-only; kernel/libinput diagnosis outside scope; global presence does not prove input delivery | `SKILL.md:225-228, 406`; `PROVINCE.md:11-16`; `corpus/knowledge/wayland-protocol-boundaries-r13.md:104`; `corpus/knowledge/output-colour-boundaries-r14.md:108` |
| Worktree staged round-15 artifacts (`spec.json`, `dispatch.json`, `swarm-registry.json`, `evidence/census-before.txt`) and unstaged `M SCORECARD.md` are present. These are not U6 content | `git status --porcelain` |

## Acceptance conditions (all required)

- **A1 Gate unchanged.** `sha256sum tools/mado-verify.sh` = `fba82a66…c207`. `git diff --name-only <baseline>..<content> -- tools/ .ufo/waves/round-14/frozen .ufo/waves/round-14/evidence/committed-bindings.json` is empty. Frozen `expected.json` keeps its pins.
- **A2 Path fence.** The content commit touches only: `corpus/knowledge/<new U6 note>.md`; one new row in `corpus/README.md`; appended rows in `corpus/SOURCES.md` (and at most a logged `status`/`used-by` edit to an existing row); `corpus/lessons/round-15*.md`; new `.ufo/waves/round-15/measure.py`; an R14-V1 correction file or appended block. Nothing under `~/.config`, omarchy, tameshi, fleet repo, or historical evidence `.txt` files.
- **A3 Source rows.** S051 and S052 are `mined` only after being opened. Each URL is pinned to an immutable revision or to local bytes with sha256 recorded in the anchor. No `latest` or moving ref.
- **A4 No URL collision.** S051 either uses a distinct pinned URL, or its `teaches` opens `supersedes S007 -`, or S007 is flipped in place with a logged used-by/status change. S052 must not reuse `apa.html` with a different fragment. A fragment-only variant is the same canonical URL.
- **A5 Note header.** Within the first 15 lines: `source:`, `verified-at:`, `recheck:`, exactly one `covers: U6`. Sections `## Layer ladder`, `## Safe boundary`, `## Unexercised delivery`. The last section carries `[UNK]`. Quotes ≤25 words with exact location and revision.
- **A6 Claim boundary.** The note asserts documented semantics (`[INF-docs]`) and static source (`[OBS]`) only. It does not claim delivery, focus, IME, cursor, kernel, device, or compositor-runtime behavior. Those stay `[UNK]`.
- **A7 Navigation.** One new README row per new note. Knowledge-note count and indexed count move together; missing = 0, dangling = 0, duplicates = 0 (integrator runs the census).
- **A8 Measurement.** `measure.py` for round 15 adds a U6 facet gate (the three headings plus `[UNK]` in the last section). Without it, a `6/7` figure is structural-only and must be labelled as such, not as sourced semantic coverage.
- **A9 Receipt correction.** R14-V1 is an append-only correction mapping each provisional header to derived target `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`. It does not edit `regression-recut.txt`, `regular-target-mutants.txt`, `retained-census-mutants.txt`, or `committed-bindings.json`. It is unscored.

## Rejection conditions (any one rejects)

- **R1** Any change under `tools/`, `frozen/`, or the committed-bindings files; or gate sha ≠ `fba82a66…c207`.
- **R2** The note, probe, or evidence reads or records input events, `/dev/input`, `libinput debug-events`, `record`, `replay`, `evtest`, `uinput`, or keymaps. Running `libinput list-devices` is also out: it enumerates devices (`SKILL.md:225-228`).
- **R3** S051 or S052 creates an active canonical-URL collision without a `supersedes` link, uses a moving ref, or claims a revision it did not open.
- **R4** `covers: U6` is credited without the three headings and `[UNK]` marker, or the round claims full input coverage, delivery, IME or kernel coverage.
- **R5** New note without a README row, or README row without a note (navigation count changes without a matching file).
- **R6** Historical receipts, bindings, or lesson text are rewritten rather than appended.
- **R7** SCORECARD or LOG asserts U6 delivery or `complete input coverage`. Delivery, IME, kernel and Waybar module text remain listed as open.
- **R8** Any gate, regression, selftest or probe run used as evidence by the reviewer. None were run here.

## Checks for the main agent (run once, after all landings; not run by this seat)

1. `sha256sum tools/mado-verify.sh` → `fba82a66…c207`.
2. `git diff --name-only <baseline>..HEAD -- tools .ufo/waves/round-14/frozen` → empty.
3. `python3 .ufo/waves/round-14/frozen/verify.py` → `frozen_match`, `MADO_REGRESSION: PASS`, exit 0 (the frozen replay).
4. `python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md` → exit 0, no active collision.
5. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0; W04 warnings for S030/S042/S045 retained.
6. `python3 .ufo/waves/round-15/measure.py <content-rev>` → exit 0, U6 facets present, navigation complete.
7. `bash tools/mado-verify.sh --selftest` → exit 0 (round-14 receipt recorded 372/372; the SKILL registry text still says 268, a known doc drift unrelated to U6).

## Residual risks

- The gate does not judge corpus notes. U6 truth rests on the source-tier, reciprocal-join and reviewer checks, not on the gate.
- Installed `libinput` version and docs anchor are not established by this seat. The DocsVersion seat owns that.
- The measure probe is a presence test. Semantic adequacy of U6 is for AttackCoverage and the non-author spot-check, which is still pending.
- The worktree already holds unrelated staged round-15 artifacts and an unstaged `SCORECARD.md` edit. The U6 content commit must list its own paths explicitly and must not absorb them.
