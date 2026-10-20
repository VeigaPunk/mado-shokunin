# Source Revision Investigation: wayland-protocols README (S005)

**Seat**: `MadoR13.SourceRevision` (scout, leaf; no subagent dispatch, no background jobs)  
**Target**: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Date**: 2026-10-20  
**Status**: Complete findings; leaf investigation; no registry edits performed.  
**Judged on**: `coverage` (C1), `operability` (C2)  
**Milestone**: exact-set census and sourced U4 boundaries  

---

## 1. Executive Summary & Sourced Reopening

In accordance with Round 13 wave instructions, this seat independently reopened `wayland-protocols` upstream documentation at its canonical source to establish the latest revision, extract exact phase compatibility rules with ≤25-word grounding quotes, and audit previous registry row `S005` in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` for anchor mismatches.

### 1.1 Source Identity & Opening Facts
- **Source**: `wayland-protocols` upstream documentation (`README.md`)
- **Canonical Repository**: `https://gitlab.freedesktop.org/wayland/wayland-protocols`
- **Canonical Web / Blob URL**: `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md`
- **Canonical Raw URL**: `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/README.md`
- **Commit-Pinned Raw URL**: `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/3dac056d83ad8947eed6eb621f346e91da736efd/README.md`
- **Commit-Pinned Blob URL**: `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/3dac056d83ad8947eed6eb621f346e91da736efd/README.md`
- **Access Date**: 2026-10-20
- **File Metrics**: 304 lines, 12,721 bytes
- **File Content Digest (SHA-256)**: `e81ad629e8d7beba23cf4d99d0c58e4af662a7df9564d2423fff19a1eed65548`
- **Source Kind**: `docs` / `spec`
- **Tier**: `A` (canonical upstream standardization body documentation and protocol change policy)
- **Admission / Rejection**: **Admitted** (satisfies kaika SOURCES Contract v1: opened live in round, tier scoped to A as upstream official doc, exact grounding quotes ≤25 words, immutable commit and file digest recorded).
- **Flip**: N/A (admitted; flip to rejected would apply if the resource were an unanchored third-party secondary restatement or lacked cryptographic/commit traceability).

---

## 2. Upstream Revision & Provenance Analysis

The upstream repository history was queried via the GitLab REST API (`https://gitlab.freedesktop.org/api/v4/projects/wayland%2Fwayland-protocols/`):

### 2.1 Latest Commit Touching `README.md`
- **Commit SHA**: `3dac056d83ad8947eed6eb621f346e91da736efd` (short: `3dac056d`)
- **Author**: Sebastian Wick `<sebastian.wick@redhat.com>` (authored: `2025-05-08T15:27:59.000+02:00`)
- **Committer**: Pekka Paalanen `<pq@iki.fi>` (committed: `2026-01-16T10:34:26.000+02:00`)
- **Commit Message / Title**: `README: Add expectations for unmerged protocol compatibility`
- **Parent Commit**: `7bc5f7355cfd640345abc8122c1b23e07cbd10c0`
- **Web Link**: `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/commit/3dac056d83ad8947eed6eb621f346e91da736efd`
- **Delta Summary**: Added lines 31–34 defining compatibility rules for unmerged protocols (allowing free iteration before upstream merge, but forbidding identical name/version with differing API).

### 2.2 Default Branch (`main`) HEAD State
- **HEAD Commit SHA**: `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (short: `35d9638c`)
- **Committed Date**: `2026-10-12T10:43:43.000+03:00`
- **Committer**: Pekka Paalanen `<pq@iki.fi>`
- **Commit Message**: `treewide: fix typos`
- **README Status at HEAD**: Identical to `3dac056d`. No commits touched `README.md` between `3dac056d` and `35d9638c`.

### 2.3 Upstream Release Tags Incorporating `3dac056d`
- **Latest Release Tag**: `1.49`
  - Tagged: `2026-06-07T15:06:32.000+02:00` by Simon Ser `<contact@emersion.fr>`
  - Target Commit: `a8d65d7f121497ddd0d10f620f4284896ab80aff`
- **Prior Release Tag**: `1.48`
  - Tagged: `2026-04-01T13:46:29.000+02:00`
- Both release tags `1.48` and `1.49` incorporate commit `3dac056d`.

---

## 3. Protocol Phase Compatibility Rules & Exact Grounding Quotes

All quotes below are taken verbatim from `/home/vgpnk/Projects/shokunin/mado-shokunin` accessed upstream `README.md` at commit `3dac056d` (`e81ad629...`). Each quote strictly adheres to the fleet ≤25-word grounding standard.

### 3.1 Overview of Phases
- **Location**: `README.md:19-22` (`## Protocol phases`)
- **Quote** (16 words):
  > "Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase."

### 3.2 Universal Major Version Rule
- **Location**: `README.md:24-25` (`## Protocol phases`)
- **Quote** (13 words):
  > "Backward-incompatible changes can only be introduced in a new major version of a protocol."

### 3.3 Experimental Phase
- **Location**: `README.md:25-27` (`## Protocol phases`)
- **Quote** (18 words):
  > "In the experimental phase, a protocol is actively being developed and iterated upon, not trying to avoid incompatible changes."
- **Location**: `README.md:179-181` (`## The experimental phase`)
- **Quote** (14 words):
  > "There is no expectation or requirement to avoid backwards incompatible changes in this phase."

### 3.4 Staging Phase
- **Location**: `README.md:27-28` (`## Protocol phases`)
- **Quote** (10 words):
  > "Protocols in the staging phase should try to minimize backward-incompatible changes,"
- **Location**: `README.md:194-197` (`## The staging phase`)
- **Quote** (25 words):
  > "Backward compatible changes may be added together with the corresponding interface version bump. Backward incompatible changes can only be done by creating a new major version"

### 3.5 Stable Phase
- **Location**: `README.md:28-29` (`## Protocol phases`)
- **Quote** (10 words):
  > "and protocols in the stable phase should avoid backward-incompatible changes."
- **Location**: `README.md:207-209` (`## The stable phase`)
- **Quote** (23 words):
  > "Once it has been concluded that a protocol been proven adequate in production, and that it is deemed unlikely to receive any backward incompatible changes,"
- **Location**: `README.md:213-215` (`## The stable phase`)
- **Quote** (21 words):
  > "Note that the major version of the stable protocol, as well as all the interface versions and names, must remain unchanged."

### 3.6 Backward Incompatible Protocol Changes (Staging & Stable)
- **Location**: `README.md:154-155` (`## Backward incompatible protocol changes`)
- **Quote** (15 words):
  > "Protocols shall try to avoid backwards incompatible protocol changes during the staging and stable phases."

### 3.7 Unmerged Protocols (Added in 3dac056d)
- **Location**: `README.md:31-34` (`## Protocol phases`)
- **Quote** (24 words):
  > "Anything that is not merged upstream can be iterated and broken freely, but care should be taken to ensure that there are no two protocols"
- **Location**: `README.md:32-34` (`## Protocol phases`)
- **Quote** (22 words):
  > "care should be taken to ensure that there are no two protocols with the same name and version but a different API."

### 3.8 Deprecated Protocols
- **Location**: `README.md:53-54` (`## Deprecation`)
- **Quote** (10 words):
  > "No more changes will be made to a deprecated protocol."

### 3.9 Legacy "Unstable" Phase
- **Location**: `README.md:63-65` (`## Legacy protocol phases`)
- **Quote** (20 words):
  > "interface names were, in addition to the major version postfix, also prefixed with `z` to distinguish them from stable protocols."

---

## 4. Audit of Previous Registry Row S005: Anchor Mismatches

The prior row in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:16` is:
```markdown
| S005 | wayland-protocols README — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md | docs | A | wayland protocol phasing and change policy (ground for later U4/U6 rounds) | README.md §Protocol phases @ main 3dac056d (2026-01-16, last commit touching README.md) | experimental/staging/stable semantics: what may break in each phase, deprecation, legacy z-prefix; gives the vocabulary to age-check a protocol claim | queued | 2026-10-19 | on-release | — |
```

A rigorous audit against canonical upstream revealed five distinct anchor discrepancies:

### 4.1 Mismatch 1: Branch vs. Commit Conflation (`@ main 3dac056d`)
- **Observation**: The anchor string specifies `@ main 3dac056d`.
- **Finding**: In git terminology, `main` is a mutable branch reference, whereas `3dac056d` is a specific commit hash. As established in §2, `3dac056d` was **not** the HEAD of branch `main` at the time of opening (2026-10-19; `main` was at `35d9638c` or prior `ee78491a`). It was solely the commit that last touched `README.md`.
- **Impact**: Conflating branch name and commit SHA creates an ambiguous pin. Anyone checking out `main` lands on `35d9638c`, not `3dac056d`. Anyone checking out `3dac056d` is in a detached HEAD state 9 months prior to current `main`.
- **Recommendation for Drafter**: Anchor explicitly as `@ 3dac056d (commit touching README.md 2026-01-16; present in tags 1.48, 1.49 and branch main)`.

### 4.2 Mismatch 2: Scope Under-coverage / Incomplete Section Span
- **Observation**: The anchor specifies only `README.md §Protocol phases`.
- **Finding**: The `teaches` column promises:
  *"experimental/staging/stable semantics: what may break in each phase, deprecation, legacy z-prefix; gives the vocabulary to age-check a protocol claim"*.
  However, in `README.md`:
  - `§Protocol phases` covers only lines 17–48 (a high-level introduction).
  - Deprecation is specified under `## Deprecation` (lines 50–55).
  - The legacy `z` prefix is specified under `## Legacy protocol phases` (lines 57–66).
  - Incompatible change mechanisms are under `## Backward incompatible protocol changes` (lines 154–168).
  - Explicit phase rules are under `## The experimental phase` (lines 170–184), `## The staging phase` (lines 186–205), and `## The stable phase` (lines 207–238).
- **Impact**: Citing only `§Protocol phases` leaves the claims regarding deprecation, legacy z-prefix, and phase-specific mechanics unanchored.
- **Recommendation for Drafter**: The anchor should cite the full span: `README.md §Protocol phases, §Deprecation, §Legacy protocol phases, §Backward incompatible protocol changes, §§The {experimental,staging,stable} phase (:17-66,154-238)`.

### 4.3 Mismatch 3: URL Scheme Discrepancy (Moving Blob vs. Raw Endpoint vs. Pinned Blob)
- **Observation**: `SOURCES.md:16` cites `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md`.
- **Finding**:
  - `corpus/lessons/round-12.md:34` and `.ufo/evidence/round-12/l2-scout.md:10` cite `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/README.md`.
  - Both URLs use `main`, which is a mutable ref.
  - The commit hash `3dac056d` does not appear in the URL itself.
- **Recommendation for Drafter**: Provide the immutable, commit-pinned blob/raw URL: `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/3dac056d83ad8947eed6eb621f346e91da736efd/README.md`.

### 4.4 Mismatch 4: Omission of Line Numbers in Anchor Cell
- **Observation**: Row `S005` lists no line range in its anchor, while other rows (e.g., `S001:63-123`, `S002:290-307`, `S003:328-358 + :360-408`, `S013:21-36,60-82,88-90`, `S018:1463-1645`, `S020:5-15`) provide precise line coordinates.
- **Finding**: In `.ufo/evidence/round-12/l2-postreviewer.md:9`, verification specifically verified line 19 (`S005: raw README line 19 matches`), and `lessons/round-12.md:59` quoted line 19. Omitting line numbers from the anchor cell creates a mismatch between internal gate verification and registry documentation.
- **Recommendation for Drafter**: Add line coordinates `:17-66,154-238` (or `:17-48` for the core phase summary).

### 4.5 Mismatch 5: Omission of Content SHA-256 Digest
- **Observation**: Row `S005` provides no SHA-256 digest of the source text, unlike `S001` (`sha256 d7b4708e...`), `S002` (`sha256 a5b48331...`), `S003` (`sha256 b1d4f4c0...`), `S004` (`sha256 6c674a22...`), and `S011` (`sha256 1c8e4f11...`).
- **Finding**: For external web sources, capturing the content SHA-256 (`e81ad629e8d7beba23cf4d99d0c58e4af662a7df9564d2423fff19a1eed65548`) provides cryptographic proof that the remote content has not drifted, matching the rigour applied to local repo files.

---

## 5. Peer & Downstream Handoff Notes

- **To `MadoR13.ProtocolRecon` & `MadoR13.RegistryDraft`**:
  - The S005 commit is verified as `3dac056d83ad8947eed6eb621f346e91da736efd`.
  - When mining `S005` (transitioning `queued` -> `mined`) or establishing its updated entry, incorporate the multi-section anchor span (`:17-66,154-238`), the immutable commit URL, and the content SHA-256 (`e81ad629...`).
  - Note that `README.md` delegates governance rules and namespace rules (`wp_`, `xdg_`, `ext_`) to `GOVERNANCE.md` (lines 14–15, 126–127, 192), directly validating the introduction of `S040` (`GOVERNANCE.md`).
- **To `MadoR13.ReviewRegistry`**:
  - S005 satisfies Tier A documentation criteria.
  - The five anchor mismatches detailed in §4 above should be checked against any incoming registry drafts.
- **Registry Non-Mutation Check**:
  - Zero edits were made to `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` or any other tracked file by this scout seat.
