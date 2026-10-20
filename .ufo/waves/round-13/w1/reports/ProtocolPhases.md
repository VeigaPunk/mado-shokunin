# ProtocolPhases — scoped findings (Mado round 13, W1)

Seat: `MadoR13.ProtocolPhases` (executor, leaf). No subagent dispatch, no background jobs.
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Status: **draft complete; no shared file edited, no verdict issued.** The registry rows and the U4 entry landed concurrently after this draft was written; §5 reconciles the landed state against the authored proposal. This seat does not run builds, lint, formatters, tests, `--selftest`, `--regression`, or live probes; L1 owns post-integration verification.

## 1. Axes and assignment

| Axis | Assigned contribution | Result |
|---|---|---|
| coverage (C1) | sourced U4 phase layer from a re-opened S005 and a new S040 (GOVERNANCE), 3/7 → 4/7 | phase layer drafted and pinned; S005/S040 rows landed concurrently and verified; entry exists and covers U4 (measured 4/7 at 2026-10-20) |
| operability (C2) | source pins and recheck commands that run literally | pinned tag + commit + blob hashes + line anchors; recheck block drafted |

Assignment: draft the U4 phase section, pin the upstream revision through commit/tag, explain experimental/staging/stable and breakage/deprecation rules exactly, no host extrapolation; draft S040 and the S005 `queued → mined` / `used-by` change; do not edit the registry. Acceptance: findings/draft only under `.ufo/waves/round-13/w1/`.

## 2. Files written

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ProtocolPhases.md` — full draft: exact-rule supplement for the landed entry, authored registry proposal vs landed-row reconciliation, lesson Gate entries, evidence ledger, recheck commands.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/ProtocolPhases.md` — this report.

No other path was written. `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, `SKILL.md`, `tools/` and all host config/state paths were read-only or untouched.

## 3. Source opens (contract-required records)

Access date **2026-10-20** for both. Pinned revision: annotated tag `1.49` → commit `ee78491a237eaff9389a0ccf8680521d074407d3` (2026-06-07), tag object `a8d65d7f121497ddd0d10f620f4284896ab80aff`. `main` at access = `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (2026-10-12).

| Row | URL (canonical, raw at pin) | Exact quote (≤25 words) | Location | Blob sha256 | Tier / kind | Admission | Flip |
|---|---|---|---|---|---|---|---|
| S005 re-open | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/README.md | “Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase.” | §Protocol phases, `README.md:19-20` | `e81ad629e8d7beba23cf4d99d0c58e4af662a7df9564d2423fff19a1eed65548` | A / docs | `queued → mined` (landed at `:17`) | a commit/release changing §Protocol phases, or a moved 1.49 tag |
| S040 | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/GOVERNANCE.md | “Declaring a protocol stable may be proposed by the same process, with the regular 30 day minimum discussion period.” | §2.3 item 6, `GOVERNANCE.md:125-126` | `b09930ca9d968af1de1d4aa08714215b88f178bb0684a6a22773af2edcbb59dc` | A / docs | landed at `:52` as kind `spec`, `mined` | a release amending §2.3 or moving the stable-declaration period |

Quote lengths verified by whitespace tokenization: 16 and 19 words. Every quote was re-matched against the pinned bytes by a script (12/12 ledger quotes found exactly).

Revision checks:

- `README.md` at tag `1.49`, at `main` `35d9638c`, and at the last-touch commit `3dac056d83ad8947eed6eb621f346e91da736efd` all hash to `e81ad629…`. S005's round-12 anchor (`@ main 3dac056d`) is therefore still exact and was **not** rewritten (contract rule 2: `anchor` is not an in-place cell).
- `GOVERNANCE.md` at tag `1.49` and at the last semantic-change commit `9dd051b4a0c6df82937d57d38ac7df389f16e6fa` (2024-11-06) both hash to `b09930ca…`. `main` hashes to `76978390…`; direct diff shows one word at `:174` (`persuant` → `pursuant`). No semantic delta in any mined section.
- GitLab compare `ee78491a… → 35d9638c…`: 7 commits; only `GOVERNANCE.md` among the two files differs. `1.49` is the highest tag on 2026-10-20 (`sort -V` over 1.35–1.49).

## 4. Drafted content (summary)

The paste-ready block in `ProtocolPhases.md` §3 covers, with `[INF-docs]` tags and line anchors:

- Three current phases plus the deprecated/legacy exception; directory placement.
- Breakage posture exact wording: experimental “not trying to avoid incompatible changes”; staging “should try to minimize”; stable “should avoid”; the stronger §Backward incompatible sentence “shall try to avoid” for staging/stable.
- Backward-compatible additions via `version`/`since`; incompatible change only in a new major version, with the five-step procedure; `-v1` naming rule and example.
- Experimental implementations track latest at all times; compile-time/runtime opt-in advice.
- Staging entry direct or by promotion; exact staging disclaimer.
- Stable promotion requirements and five-step procedure; exact replacement disclaimer.
- Deprecation rule; legacy `unstable` policy and `z` prefix; `unstable/` closed to new protocols.
- Governance gates (S040): namespaces (`xdg`/`wp`/`ext`, experimental `xx`), ACK/implementation/review thresholds, 30-day introduction and stable-promotion minima, no minimum for amendments, one-year staging-in-use option, two-week experimental review, three-month removal plus one-week grace, experimental promotion, NACK scope/penalties, GOVERNANCE amendment threshold.
- Boundary section: phase is an upstream package property; advertisement ≠ phase ≠ conformance; `z` prefix is legacy naming, not current phase; no request was issued.

The advertised-globals layer is deliberately not merged. The wave capture is `.ufo/waves/round-13/w1/globals.json` (Hyprland 0.56.2; 72 globals / 71 unique interfaces; set sha256 `9569d02f…`). A sibling crosswalk message (`MadoR13.GlobalCapture`, 2026-10-20) reports directory-based phase mapping and names `zwp_linux_dmabuf_v1` / `zwp_tablet_manager_v2` as `z`-prefixed stable protocols; the draft records that as another seat's observation, not as S005/S040 evidence.

## 5. Registry state: proposal vs landed (no edit applied)

Path: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`. Both moves this seat drafted have already landed concurrently; verify, do not re-apply.

- **S005** (`corpus/SOURCES.md:17`): landed as `mined` with `used-by corpus/knowledge/wayland-protocol-boundaries-r13.md`; `recheck` still `on-release`; `anchor`, `teaches`, `opened`, `source` untouched. The authored in-place cells match the landed cells exactly.
- **S040** (`corpus/SOURCES.md:52`): landed as `spec` (not the authored `docs`), tier A, scope “Namespace-specific protocol inclusion and promotion authority, not runtime support”, anchor `§2.1, §2.2, §2.3 @ 35d9638c (2026-10-12)`, status `mined`, used-by the entry. No second S040 is to be appended. The authored candidate pinned tag 1.49; both anchors resolve to the same mined text (only the `:174` typo differs). `kind`, `anchor` and `teaches` are not in-place cells, so no correction is required.
- The round-12 GOVERNANCE lead is closed by the landed S040; `MEMBERS.md` remains unopened and is not needed.
- Measured registry after landing: 45 rows; `NF!=13` 0; `A=41 B=1 C=3`; `mined=33 queued=8 rejected=4`; no duplicate ids. The entry cites S005, S040, S041, S042, S043; all five are `mined` and all five name the entry in `used-by`.
- The lesson `corpus/lessons/round-13.md` landed concurrently and its `## Gate` records S005 (commit `3dac056d`) and S040 (commit `35d9638c`; its S040 quote is the §2.1.1 `xx` namespace sentence, not this seat's §2.3 stable-declaration sentence — both are valid and grounded); the S017/S044 `used-by` paths resolved with it. The only remaining join flag is pre-existing: the U2 entry still cites S030 (rejected duplicate, round-12 erratum). Not this seat's rows.

## 6. Findings

1. **F0 — The U4 target landed concurrently and is measured at 4/7.** `corpus/knowledge/wayland-protocol-boundaries-r13.md` exists (8,213 B, `covers: U4`) and cites S005, S040, S041, S042, S043; all five rows are `mined` with `used-by` naming the entry. C1 measurement at 2026-10-20: 5 sourced entries, `covers:` U1–U4. This seat did not write the entry and takes no verdict.
2. **F1 — S005's old anchor survives the re-open.** The last commit touching `README.md` is still `3dac056d`; tag `1.49` and `main` are byte-identical to it (`e81ad629…`). No anchor rewrite is needed or permitted. This is a clean append-only status/used-by move.
3. **F2 — S040 is the round-12 unopened lead; the landed row pins `35d9638c`.** The canonical governance text is stable since `9dd051b4` (2024-11-06); the only post-1.49 delta is a typo. The authored candidate pinned the annotated tag `1.49`; both resolve to identical mined text. The landed row's `kind=spec` is contract-valid and no in-place correction is available or needed.
4. **F3 — The phase model is procedural, not automatic.** Stable requires a declaration and a 30-day minimum discussion; staging can be entered directly and is not stable; experimental protocols can break and must track latest. The draft states the exact `should` / `shall try to avoid` wording rather than flattening it into a guarantee.
5. **F4 — Interface prefix is not phase.** README §Legacy protocol phases defines `z` as the old unstable policy prefix; current experimental interfaces use `xx` (GOVERNANCE §2.1.1). The sibling crosswalk's counterexamples corroborate this, but the rule is grounded in S005/S040 alone.
6. **F5 — `ext` has no separate NACK sentence.** GOVERNANCE §2.2 item 3 names only `xdg`/`wp`; the draft records that gap instead of inventing an `ext` NACK rule.
7. **F6 — No host extrapolation.** The section makes zero claims about Hyprland 0.56.2 behavior or conformance; the only host reference is the sibling globals artifact, explicitly separated and not used to infer phase.
8. **F7 — Operability is delegated to the integrator.** The drafted recheck block pins bytes by sha256 and re-reads the exact sections; the registry/join commands are copied from the contract's census form so they can run literally after merge.

## 7. Risks and blockers

- **R1 — Duplicate-row hazard.** S040 already exists at `corpus/SOURCES.md:52`; do not append the authored candidate as a second S040. The registry is append-only and `kind`/`anchor`/`teaches` are not in-place cells, so the landed row stands unless L1 chooses a superseding row.
- **R2 — Count drift.** The measured census is 45 rows / `A=41 B=1 C=3` / `mined=33 queued=8 rejected=4`; re-derive with the commands, do not transcribe the measurement after other seats land rows.
- **R3 — Tag movement.** `1.49` is annotated and currently highest; a new release or a force-moved tag flips the pin. The recheck block detects both.
- **R4 — Process text vs compliance.** GOVERNANCE states rules; it does not prove any specific protocol satisfied them. The entry says so.
- **R5 — Prefix trap.** A future reader may still map `zw…` to “experimental.” The boundary and rejected sections name the trap explicitly; keep them when merging.
- **R6 — No verification run.** Everything above is source/document verification by this seat; `--selftest`, `--regression`, live reads and C1/C2 scoring remain L1's post-integration job.

## 8. Checks L1 should run

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin`; full literal block is in `ProtocolPhases.md` §8.

1. `curl -fsSL .../raw/ee78491a.../README.md | sha256sum` → `e81ad629…`; same for `GOVERNANCE.md` → `b09930ca…`.
2. `git ls-remote --tags ... | sort -V | tail -3` and `git ls-remote ... 'refs/tags/1.49*'` → 1.49 still highest and peeled commit `ee78491a`.
3. Current registry census (rows already landed): 45 / 0 / `A=41 B=1 C=3` / `mined=33 queued=8 rejected=4` / no duplicate ids; re-derive if other seats append.
4. Join: S005/S040/S041/S042/S043 all `mined` with `used-by` the entry; the entry's `source:` line cites them; `grep -lE '^covers:.*U4' corpus/knowledge/*.md` names it. The only remaining literal-loop flag is the U2 entry's S030 citation — pre-existing and unrelated.
5. Post-integration gate battery belongs to L1/GateImplement, not this seat.

## 9. Tooling record

- Installs or upgrades: **none**. Used host-provided `curl`, `git`, `sha256sum`, `sed`, `grep`, `awk`, `sort`, `python3`.
- No tool, package, config or compositor state was installed, upgraded or changed.
