# ReviewPhases — mado-r13-w1 (reviewer, U4 phase + advertised globals)

Access date for every upstream open: 2026-10-20 (UTC fetches ~04:00). Tooling: `curl`, `python3`, `sha256sum`, read-only `pacman -Q/-Qi`. No installs or updates were performed by this seat. Scratch copies in `/tmp/r13w1ReviewPhases` are provenance only, not durable evidence; each claim below is re-derivable from the URL and revision given.

## Verdict

- The S005 row's claim (three phases, pin `3dac056d`) is **confirmed** against primary text.
- Lesson M01 (`staging` is a stable, backward-compatible guarantee) is **correctly rejected**, but its citations are unpinned `main` links and point at the wrong sections for the claim.
- Lesson M02 (`zwlr_output_manager_v1` is generic stable monitor metadata) is **correctly rejected**; the upstream XML says the opposite of the trap.
- Host `wayland-info` is **no longer absent**: the round-12 `command -v` record (2026-10-19) is stale. Host package install record is dated 2026-10-20.
- Three inferences the corpus must not make are rejected (see R1–R4).

## Pinned revisions (named, re-derivable)

| Source | Revision / blob | Date | Notes |
|---|---|---|---|
| wayland-protocols `README.md` | last commit touching it `3dac056d83ad8947eed6eb621f346e91da736efd`; blob sha256 `e81ad629e8d7beba23cf4d99d0c58e4af662a7df9564d2423fff19a1eed65548` | committed 2026-01-16T10:34:26+02:00 | byte-identical at `main` (head `35d9638c`) and tag `1.49` (`ee78491a237eaff9389a0ccf8680521d074407d3`, 2026-06-07) |
| wayland-protocols `GOVERNANCE.md` | last commit touching it `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (treewide "fix typos"); blob sha256 `769783907eff2716dc760e2349f5cea40b1c536efb7f24123ba9aff5371dcc5a` | committed 2026-10-12T10:43:43+03:00 | differs from tag `1.49` blob `b09930ca9d968af1de1d4aa08714215b88f178bb0684a6a22773af2edcbb59dc` at **one line only** (GOVERNANCE.md:174 "persuant"→"pursuant"); no substantive change |
| wayland-protocols `MEMBERS.md` | last commit `d5aed4e4903a77aefaef03359d1ffdc0d5093456`; blob sha256 `c13bf01e24455216846f297405a77332f45394dfef4374b75ad6851e1ca4c405` | 2025-02-21 | identical at tag `1.49` |
| wayland.freedesktop.org `extras.html` | last commit touching it on `main` `8923a19916635c21a3577b616f650a7e45d70fa9` ("extras: mention wl-proxy") | 2026-01-15T10:10:23+01:00 | page text at `main` contains "advertized" (line 19). Served bytes not hashed; [INF] the site builds from `main` |
| wayland-utils (wayland-info) tag `1.3.0` | commit `d01edd68961ca01779dcb96afe56c2d99ff79067`; README sha256 `ada5f1a27fd508eb8fe53536417197036b6b41c0746ccd32d23357304e9368ec` | 2025-11-24T13:53:04+01:00 | `main` head `8d921016` (2025-12-29). Quoted lines identical at tag 1.3.0 lines 7–8 and 33–34 |
| wlroots `protocol/wlr-output-management-unstable-v1.xml` | last commit on `master` `cdd2c7e0064efee7fd398b2935923508b2fa9842`; sha256 `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` | 2025-09-10 | lesson M02 cites unpinned `master` |

Host package: `wayland-utils 1.3.0-1`, `pacman -Qi` Install Date `Tue 20 Oct 2026 01:06:49 AM -03`; `/usr/bin/wayland-info` mtime 2025-11-24 (carried from build). Mapping of this package to upstream tag 1.3.0 is **[INF]** from version string and build date, not verified against the PKGBUILD.

## Primary quotes (admission record)

Each row: URL, access date, quote (≤25 words), location, revision, tier, decision.

**Q1 — phases (admit, S005).** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/README.md`, 2026-10-20. "Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase." — README.md:19–20, §Protocol phases, rev `3dac056d`, tier A. **Admitted.** Flip: a README revision removing or renaming a phase.

**Q2 — staging is not a guarantee (reject M01's reading).** Same URL, 2026-10-20. "Protocols in the staging phase should try to minimize backward-incompatible changes, and protocols in the stable phase should avoid backward-incompatible changes." — README.md:27–29, §Protocol phases, rev `3dac056d`, tier A. **Rejects** "staging = stable, backward-compatible guarantee." Flip: a normative README sentence making staging changes forbidden.

**Q3 — stable is a prediction, not a freeze.** Same URL. "stable", meaning it is unexpected to become superseded by a new major version. — README.md:46–47, §Protocol phases, rev `3dac056d`, tier A. Admitted as "unexpected", not "guaranteed."

**Q4 — experimental carries no compatibility expectation.** Same URL. "There is no expectation or requirement to avoid backwards incompatible changes" — README.md:194–195, §The experimental phase, rev `3dac056d`, tier A. **Admitted.**

**Q5 — unconditional major-version rule, and its experimental carve-out (interpretation, not defect).** Same URL. "Backward-incompatible changes can only be introduced in a new major version of a protocol." — README.md:24, §Protocol phases. The carve-out is in README.md:130 ("Each new non-experimental protocol XML file must include a major version postfix") and README.md:194–195. Admitted reading: the major-version rule binds versioned (non-experimental) protocols; experimental protocols are exempt. Flip: upstream text making experimental protocols versioned.

**Q6 — staging admission criteria live in GOVERNANCE §2.2, referenced via §2.3.** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/GOVERNANCE.md`, 2026-10-20. "When the proposed protocol meets all requirements for inclusion per section 2.2, and the minimum discussion period has elapsed" — GOVERNANCE.md:120, §2.3.4, rev `35d9638c`, tier A. **Admitted with a pointer rule:** the README's "must meet GOVERNANCE section 2.3" resolves to thresholds only through §2.3.4 → §2.2. Citing §2.3 alone for thresholds is **rejected**.

**Q7 — thresholds (admit with namespace scope).** Same GOVERNANCE, rev `35d9638c`, tier A. "Protocols in the "xdg" and "wp" namespace are eligible for inclusion only if ACKed by at least 3 members." — GOVERNANCE.md:86–87, §2.2.2. The "ext" namespace is 2 ACKs (GOVERNANCE.md:93, §2.2.5). **Admitted per namespace only**; a single "staging = 3 ACKs" line is rejected.

**Q8 — MEMBERS scope.** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/MEMBERS.md`, 2026-10-20. Nine project entries (GTK/Mutter, KWin, mesa, Mir, Qt, Smithay/Cosmic, Weston, wlroots/Sway, Chromium); 17 `(@handle)` tokens, one named contact without handle (Mir). Zero entries match "hypr" — MEMBERS.md, rev `d5aed4e4`, tier A. **Rejects** "Hyprland is a wayland-protocols member" and any claim that the host compositor's advertised set is governed by MEMBERS.

**Q9 — extras page: the advertised-globals claim (admit, S006).** `https://wayland.freedesktop.org/extras.html`, 2026-10-20. "Running `wayland-info` will list all global interfaces advertized by the compositor." — §Compositor features (rendered page, line 19 of source), source rev `8923a199`, tier A. **Admitted.** Note: the page says `wayland-info` "works on any compositor"; this does not establish which globals a given host advertises.

**Q10 — wayland-info semantics: advertised versions, not phase (admit, U4 boundary).** `https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/main/README.md`, 2026-10-20; quote verified at tag `1.3.0`. "It can be used to check which Wayland protocols and versions are advertised by the Wayland compositor." — README lines 7–8 (tag 1.3.0), tier A. **Admitted.** Quote is wrapped across two lines in the tag. Same README: "only shows features that the compositor implements via Wayland protocols" (lines 33–34). Output sample fields: `interface`, `version`, `name` (global id), plus per-interface extras for DMABUF, presentation time, tablet and XDG output. **No protocol-phase field.**

**Q11 — M02 trap confirmed.** `https://gitlab.freedesktop.org/wlroots/wlroots/-/raw/master/protocol/wlr-output-management-unstable-v1.xml`, 2026-10-20. "The protocol described in this file is experimental and backward incompatible changes may be made." — XML lines 32–33, rev `cdd2c7e0`, tier A. And: "This protocol is not designed to be a generic output property advertisement protocol for regular clients." — XML line 68, same rev. **Rejects** "generic stable monitor metadata." Pin the lesson's citation to `cdd2c7e0`.

## Rejections (interpretations unsupported by primary quotes)

- **R1 — "staging/stable is a compatibility guarantee" (lesson M01).** Rejected by Q2 and Q3. Flip: a README or GOVERNANCE sentence making staging changes forbidden.
- **R2 — "`wayland-info` reports a protocol's phase."** Rejected by Q10: output carries interface, version and global name only. Phase must be derived from the protocol's directory or its README (`experimental/`, `staging/`, `stable/`, `deprecated/`, `unstable/`), not from advertisement. Flip: a wayland-utils output sample with a phase/stability key, at a pinned tag.
- **R3 — "an advertised global proves the protocol works."** Rejected: Q9/Q10 establish advertisement, and nothing in the upstream text equates advertisement with functional behavior. [INF] from absence in the quoted text; flip: a primary source linking advertisement to behavioral conformance.
- **R4 — "`zwlr_*` interfaces are in the wayland-protocols phase vocabulary."** Rejected: the phase vocabulary (README:17–20) applies to protocols "merged upstream" in wayland-protocols. `zwlr_output_manager_v1` lives in wlroots and self-describes as experimental (Q11). Phases may be applied only with an explicit cross-mapping.

## Census (exact-set, C2 operability form)

| Set | Expected (named by source) | Observed in source | Missing / extra |
|---|---|---|---|
| Current phases | `experimental`, `staging`, `stable` (README:19–20) | the same 3 | none |
| Phase-directory categories | `stable/`, `staging/`, `experimental/`, `deprecated/`, `unstable/` (README directory section) | `deprecated/` 1, `experimental/` 2, `stable/` 2, `staging/` 2, `unstable/` 1 mentions | none |
| Namespaces | `wp`, `xdg`, `ext` (GOVERNANCE §2.1.1–§2.1 items 3–5) plus experimental `xx` (§2.1.1 item 1) | `wp`, `xdg`, `ext` quoted in §2.1; `xx` in §2.1.1 | none |
| Membership projects | 9 entries (MEMBERS.md) | 9 entries; none matches "hypr" | Hyprland absent — not a member |
| Host advertised globals | not sampled by this seat (GlobalCapture owns probe) | — | — |

## Stale host premise (correctness, coverage)

- Round-12 `l2-scout.md:3,10` records `wayland-info` as absent, measured 2026-10-19. The host now has `/usr/bin/wayland-info` from `wayland-utils 1.3.0-1`, Install Date 2026-10-20 01:06:49 -03, the same minute as the wave directory creation.
- I did not identify the installer from this lane; the GlobalCapture seat is authorized to install this package under the operator tooling directive. [INF] attribution. The corpus and SCORECARD statements that `wayland-info` is not installed should be dated or superseded. This seat did not run `wayland-info` (not assigned).

## Recommended corpus actions (for owners; not edited here)

1. **M01 citations** (`corpus/lessons/round-12.md:34`): replace the unpinned `main` links with `3dac056d` README lines 19–29, 46–47, 194–195, and §The staging phase / §The stable phase (199–252); drop "§2.3" as the compatibility source and cite §2.2 via §2.3.4 for thresholds.
2. **S005** (`corpus/SOURCES.md:16`): status `queued` → `mined` by in-place change, with the pin `3dac056d` (blob `e81ad629…`) and the Q1–Q5 quotes. Its teaching text is accurate; add that staging/stable wording is "should", not a guarantee.
3. **S006** (`corpus/SOURCES.md:17`): the owed anchor now resolves to repo `wayland/wayland.freedesktop.org` commit `8923a199`. Closing the owed anchor requires a superseding row with `teaches` opening `supersedes S006 —`, per SOURCES.md's search-log rule.
4. **New candidate GOVERNANCE row** (for DraftRegistry): tier A, pin `35d9638c` (blob `76978390…`), quotes Q6 and Q7, with the tag-1.49 typo-only delta noted.
5. **M02 citation** (`corpus/lessons/round-12.md:35`): pin `cdd2c7e0` (XML sha `65b0f82a…`).
6. **Round-12 `wayland-info` absence** (`.ufo/evidence/round-12/l2-scout.md:3,10`; `SCORECARD.md:319–321`): date-qualify, do not rewrite the round-12 record.

## Residual risk and verification gaps

- Served `extras.html` and wayland.freedesktop.org deploy state not hashed; `8923a199` is a source-commit pin, not a served-bytes pin.
- Advertisement-to-behavior (R3) is rejected on absence of upstream support, not on a measured counterexample.
- The host `wayland-utils` package's source commit is [INF] from version and build date.
- No wayland-protocols protocol XML under `stable/` or `staging/` was opened; phase claims here rest on README and GOVERNANCE text only.
- Hyprland's own protocol support (e.g. which staging protocols it implements) is out of this lane.

## Tooling record

No installs, upgrades or package operations by this seat. Read-only: `pacman -Q`, `pacman -Qi`, `pacman -Ql`, `stat`, `curl`, `sha256sum`, `python3` (JSON parse of GitLab API responses). `wayland-info` was not executed.
