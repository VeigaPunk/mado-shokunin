# U4 protocol-phase draft — S005 re-open and S040 admission

Seat: `MadoR13.ProtocolPhases` (executor, leaf). No subagent dispatch, no background jobs.
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Status: **draft only; no registry, knowledge, lesson, gate or SKILL edit applied by this seat.**
Draft consumer: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md` (to be created/merged by the integrator; this seat does not own that file).
Assigned axes: coverage (`U4`, 3/7 → 4/7) and operability (source pins and recheck commands that can be run literally). Non-goals: no host probe, no compositor/config read, no gate edit, no registry edit.

**Concurrent landing (verified 2026-10-20, after the draft was written):** another seat created `corpus/knowledge/wayland-protocol-boundaries-r13.md` (8,213 B, `covers: U4`) and applied the registry moves this draft had proposed. Current state: S005 is already `mined` with `used-by` that entry (`corpus/SOURCES.md:17`), and S040 already exists (`corpus/SOURCES.md:52`, kind `spec`, pin `35d9638c`, `mined`, same `used-by`). This draft is therefore (a) the authored proposal, (b) an independent verification of the landed pins, and (c) an exact-rule supplement for the entry. **Do not re-apply §4.**

## 1. Scope result

- Re-opened S005 (`wayland-protocols` README) at a pinned upstream release and re-verified the round-12 quote and anchor.
- Opened the GOVERNANCE.md lead named unopened in round-12 `corpus/SOURCES.md` `## Leads`; it is the candidate **S040** row.
- Drafted the phase layer of the U4 entry: three current phases, breakage/versioning rules, deprecation, legacy `unstable` policy, promotion procedures, and the governance gates that admit/promote protocols.
- Kept the advertised-globals layer out of this section. The wave's host capture is `.ufo/waves/round-13/w1/globals.json` (Hyprland 0.56.2, `wayland-info` 72 globals / 71 unique interfaces); it is a host observation supplied by another seat and must not be merged into the upstream phase statements.
- No source statement below is projected onto the host. Every phase/governance sentence is `[INF-docs]` (official upstream documentation, not installed-host behavior).

## 2. Source pins (exact revisions)

Access date for both files: **2026-10-20**. Both were fetched from the canonical GitLab raw endpoint at the pinned revision, not from a search result or mirror.

| Row | File | Pinned revision | Commit date | Blob sha256 | Canonical URL |
|---|---|---|---|---|---|
| S005 | `README.md` | annotated tag `1.49` → commit `ee78491a237eaff9389a0ccf8680521d074407d3` | 2026-06-07T15:06:32+02:00 | `e81ad629e8d7beba23cf4d99d0c58e4af662a7df9564d2423fff19a1eed65548` | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md |
| S040 | `GOVERNANCE.md` | same tag → commit `ee78491a237eaff9389a0ccf8680521d074407d3` | 2026-06-07T15:06:32+02:00 | `b09930ca9d968af1de1d4aa08714215b88f178bb0684a6a22773af2edcbb59dc` | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/GOVERNANCE.md |

Pinned raw URLs actually fetched (durable, re-runnable):

- https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/README.md
- https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/GOVERNANCE.md

Revision facts:

- `git ls-remote --tags https://gitlab.freedesktop.org/wayland/wayland-protocols.git` on 2026-10-20: `refs/tags/1.49` = annotated tag object `a8d65d7f121497ddd0d10f620f4284896ab80aff`; `refs/tags/1.49^{}` = commit `ee78491a237eaff9389a0ccf8680521d074407d3`. `1.49` is the highest tag at that time (`sort -V` over `1.35 … 1.49`).
- `refs/heads/main` on the same date = `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (2026-10-12T10:43:43+03:00, “treewide: fix typos”).
- GitLab compare `ee78491a… → 35d9638c…`: 7 commits; the only `README.md`/`GOVERNANCE.md` diff in the compare is `GOVERNANCE.md`. The delta is one word: at tag `1.49` line 174 reads `persuant`, at `main` it reads `pursuant`. No semantic change in any mined section.
- `README.md` at `main` is byte-identical to the tag: sha256 `e81ad629…` at both. Its last commit touching the file is `3dac056d83ad8947eed6eb621f346e91da736efd` (committed 2026-01-16), which is the revision already recorded in S005's round-12 anchor; the blob fetched at that commit also hashes to `e81ad629…`, so the anchor remains exact at the newer pin.
- `GOVERNANCE.md` at `main` has sha256 `769783907eff2716dc760e2349f5cea40b1c536efb7f24123ba9aff5371dcc5a`; it differs from the tag only at line 174. The last semantic change is commit `9dd051b4a0c6df82937d57d38ac7df389f16e6fa` (2024-11-06, “governance: update NACK usage/restrictions”), whose blob also hashes to `b09930ca…`; the only later commit is the 2026-10-12 typo fix. S040 is pinned to the tag because the tag is the released state; the mined quotes are identical at `main`.

## 3. Draft section for the U4 entry

The entry now exists (8,213 B; `covers: U4`; its `source:` line cites S005, S040, S041, S042, S043), so the block below is a **supplement of exact rules**, not a replacement. Do not paste it over the landed entry.

What the landed entry already covers: the three-phase table, staging/stable/deprecated/legacy posture, the governance-is-upstream-only boundary, advertisement/binding/behavior separation, the host sample, the safe recheck, the rejected list and its limits.

What this supplement adds and the integrator may merge into the entry's phase section:

- the five-step backward-incompatible-change procedure and the `-v1` naming rule;
- the exact staging and stable disclaimers and the stable-promotion steps;
- the exact governance periods (30-day introduction and stable declaration, two-week experimental review, three-month removal plus one-week grace, one-year staging option) and the NACK/amendment rules;
- the unmerged-protocol rule and the experimental latest-version duty.

If merged, keep the landed entry's limits and add: no protocol XML inventory was performed, and no MR wall-clock timing was measured.

````markdown
# Wayland protocol boundaries — phases, governance and advertised globals (MADO-R13-1)

source: S005 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md — “Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase.” §Protocol phases @ tag 1.49 ee78491a (2026-06-07; README unchanged at main 35d9638c; sha256 e81ad629…); S040 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/GOVERNANCE.md — “Declaring a protocol stable may be proposed by the same process, with the regular 30 day minimum discussion period.” §2.3 @ tag 1.49 ee78491a (2026-06-07; main 35d9638c differs only at :174; sha256 b09930ca…)
verified-at: 2026-10-20
recheck: on-release
covers: U4

## Finding

- `[INF-docs]` `wayland-protocols` is the standardization body for extension protocols, and a protocol's phase is a property of its upstream package, not of any compositor that advertises an interface. The three current phases are experimental, staging and stable; merged protocols are in one of those phases unless they are deprecated or in the legacy phases (S005, §Protocol phases, README.md:19-22).
- `[INF-docs]` The phase label is a compatibility expectation, not a conformance verdict. Experimental protocols may break; staging protocols should minimize breaks; stable protocols should avoid them, and stable is described as “unexpected to become superseded by a new major version”, not impossible (S005, README.md:24-29, :44-47).
- `[INF-docs]` Promotion is procedural, not automatic: staging and stable declarations point at GOVERNANCE section 2.3, whose gates include ACKs, implementation counts, review, and a 30-day minimum discussion for a stable declaration (S005, README.md:199-206, :227-228; S040, §2.3, GOVERNANCE.md:110-129).
- `[OBS-record]` The sibling host globals capture for this wave (`.ufo/waves/round-13/w1/globals.json`, `wayland-info` 2026-10-20, Hyprland 0.56.2) is a separate evidence layer: it lists advertised interfaces and versions only. It is not used below to infer any protocol's phase.
- `[UNK]` No protocol request was issued, no XML was executed, and no compositor behavior was exercised by this seat.

## Phase model (S005)

| Phase | Tree directory | Upstream breakage posture | Entry route | What the label supports |
|---|---|---|---|---|
| experimental | `experimental/` | “not trying to avoid incompatible changes”; implementations “must work to support the latest version of the protocol at all times” | proposal MR with need/purpose, valid XML consumable by `wayland-scanner`, clearly tagged experimental; merged after a two-week review unless NACK/WAIT | active development; no compatibility promise |
| staging | `staging/` | “should try to minimize backward-incompatible changes”; compatible additions may accompany an interface version bump; incompatible changes only via a new major version | direct entry without the experimental phase, or promotion; must meet GOVERNANCE §2.3 staging requirements | encouraged wider adoption; not a stability guarantee |
| stable | `stable/` | “should avoid backward-incompatible changes”; major version, interface versions and interface names must remain unchanged on promotion | declaration after production adequacy and an expectation of no incompatible change; GOVERNANCE §2.3 process | proven adequate; unlikely (not impossible) to be superseded |
| deprecated | `deprecated/` | “No more changes will be made to a deprecated protocol.” | replaced by some other protocol, or declared undesirable for some other reason | frozen; the directory remains |
| unstable (legacy) | `unstable/` | prior categorization policy; interface names carried a `z` prefix in addition to the major-version postfix | new protocols “should never be placed here” | legacy naming/categorization only |

Exact wording and locations:

- `[INF-docs]` Three current phases and the deprecated/legacy exception: “Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase.” (S005, README.md:19-20, §Protocol phases).
- `[INF-docs]` Breakage expectations: experimental “not trying to avoid incompatible changes”; staging “should try to minimize backward-incompatible changes”; stable “should avoid backward-incompatible changes” (S005, README.md:24-29).
- `[INF-docs]` Staging is for wider adoption: “implementation is encouraged in clients and compositors where the functionality it specifies is wanted.” (S005, README.md:39-42).
- `[INF-docs]` Stable is declared after testing in the wild: “sufficiently tested in the wild and proven adequate”, and is “unexpected to become superseded by a new major version”. (S005, README.md:44-47).
- `[INF-docs]` Every release “finalizes the version of the protocols to their state they had at that time” (S005, README.md:255-256). A release label is not a separate compatibility promise.

### Backward-compatible vs backward-incompatible changes

- `[INF-docs]` Compatible additions and changes use the `version` and `since` XML attributes (S005, §Backward compatible protocol changes, README.md:162-166).
- `[INF-docs]` An incompatible change can only be introduced in a new major version. The documented procedure is exact (S005, README.md:168-182):
  1. copy the XML file with the major version increased by 1;
  2. increase the major version number in the protocol XML by 1;
  3. increase the major version number in all interfaces in the XML by 1;
  4. reset the interface version attribute of all interfaces to 1;
  5. remove all `since` attributes.
- `[INF-docs]` Every new non-experimental protocol XML must carry a major-version postfix starting at `-v1`, and its interfaces must carry the same postfix; the worked example is `foo-bar/foo-bar-v1.xml` containing `wp_foo_bar_v1`, with `-v2` for the next major version (S005, README.md:129-141).
- `[INF-docs]` The general staging-and-stable sentence is stronger than the phase-table wording: “Protocols shall try to avoid backwards incompatible protocol changes during the staging and stable phases.” (S005, README.md:170-171). The staging disclaimer still allows a new major version (S005, README.md:208-215).
- `[INF-docs]` Unmerged protocols “can be iterated and broken freely”, but two protocols must not share a name and version with a different API (S005, README.md:31-33).
- `[INF-docs]` Implementations choosing to support experimental protocols “must work to support the latest version of the protocol at all times”; build-time compile options are advised to avoid version-mismatch compile errors, and a runtime option may be useful to keep users out of potentially broken behavior (S005, README.md:184-197).

### Staging entry and its disclaimer

- `[INF-docs]` A protocol may enter the repository directly in staging “without traversing the experimental phase”, and an experimental author may request promotion at any point; both routes must meet the GOVERNANCE §2.3 staging requirements (S005, README.md:199-206).
- `[INF-docs]` Staging protocols must carry the exact disclaimer: “Warning! The protocol described in this file is currently in the staging phase. Backward compatible changes may be added together with the corresponding interface version bump. Backward incompatible changes can only be done by creating a new major version of the protocol.” (S005, README.md:208-215).
- `[INF-docs]` On promotion from experimental, the namespace prefix is determined, the protocol is renamed and merged into the appropriate directory, and the `experimental/` entry is deleted (S005, README.md:217-219).

### Stable promotion procedure

- `[INF-docs]` Requirements: proven adequate in production and deemed unlikely to receive an incompatible change (S005, README.md:221-225); other requirements are in GOVERNANCE §2.3 (S005, README.md:227-228).
- `[INF-docs]` The major version and all interface versions and names must remain unchanged (S005, README.md:230-231).
- `[INF-docs]` Procedure (S005, README.md:233-251):
  1. create a directory under `stable/` with the same name as the staging protocol directory;
  2. copy the final XML, named `<protocol-directory>-<version>.xml`;
  3. remove the staging disclaimer;
  4. update the staging `README` and create a new `README` in the stable directory;
  5. replace the staging copy's disclaimer with: “Disclaimer: This protocol has been marked stable. This copy is no longer used and only retained for backwards compatibility. The canonical version can be found in the stable/ directory.”

### Deprecation and the legacy phases

- `[INF-docs]` Deprecation is allowed when a protocol “has been replaced by some other protocol, or declared undesirable for some other reason”; afterwards “No more changes will be made to a deprecated protocol.” (S005, §Deprecation, README.md:49-53).
- `[INF-docs]` “Unstable” is not a current phase: it names a “protocol categorization policy previously used by wayland-protocols”, in which interface names were prefixed with `z` in addition to the major-version postfix (S005, §Legacy protocol phases, README.md:55-63).
- `[INF-docs]` The `unstable/` directory still exists for those legacy protocols, but new protocols “should never be placed here” (S005, README.md:74-75).
- `[INF-docs]` Directory placement follows the phase: `stable/`, `staging/`, `experimental/`, `deprecated/`, with `unstable/` only for legacy entries (S005, README.md:65-75).

## Governance gates around the phases (S040)

- `[INF-docs]` Namespaces are `xdg` (window-configuration protocols), `wp` (general Wayland “plumbing”), and `ext` (catch-all); interfaces are prefixed `<namespace>_` (S040, §2.1, GOVERNANCE.md:61-75).
- `[INF-docs]` Experimental protocols begin with the `xx` namespace, have no relation to the 2.1 namespaces, and their namespacing “is determined upon promotion” (S040, §2.1.1, GOVERNANCE.md:76-80).
- `[INF-docs]` Inclusion thresholds (S040, §2.2, GOVERNANCE.md:82-101):

| Namespace | ACK threshold | NACK effect | Implementation threshold | Review |
|---|---|---|---|---|
| `xdg`, `wp` | ACK by at least 3 member projects | NACK by any member makes the protocol ineligible | at least 3 open-source implementations: 1 client + 2 servers, or 2 clients + 1 server | in-depth review by at least 1 member project; author reviews disregarded |
| `ext` | ACK by at least 2 member projects | (same NACK rule as §2.2 item 3 applies to xdg/wp wording; no separate ext NACK sentence) | at least 1 open-source client and 1 open-source server | same review rule |

- `[INF-docs]` “Open-source” means distributed under an Open Source Initiative approved license (S040, §2.2 item 7, GOVERNANCE.md:97-98).
- `[INF-docs]` Experimental inclusion requirements are lighter: valid XML consumable by `wayland-scanner`, a proposal MR outlining need and purpose, and a clear experimental tag (S040, §2.2.1, GOVERNANCE.md:103-108).
- `[INF-docs]` Introduction process: an MR to the GitLab repository; justification against §2.2; an indefinite discussion period with a **minimum of 30 days** from MR open; the sponsoring member merges once the requirements are met and the minimum period has elapsed (S040, §2.3, GOVERNANCE.md:110-122).
- `[INF-docs]` Amendments to an existing protocol use the same process with **no minimum discussion period** (S040, §2.3 item 5, GOVERNANCE.md:123-124).
- `[INF-docs]` Declaring a protocol stable uses the same process with the regular **30-day minimum** discussion period (S040, §2.3 item 6, GOVERNANCE.md:125-126).
- `[INF-docs]` A member project may invoke the 30-day discussion for any staging protocol proposal that has been “in use without substantive changes for a period of one year” (S040, §2.3 item 7, GOVERNANCE.md:127-129).
- `[INF-docs]` Experimental review: merged after a **two-week** review upon the author's request unless a NACK has been given or a WAIT is in progress; if all NACKs are removed, the two weeks restart (S040, §2.3.1, GOVERNANCE.md:160-166).
- `[INF-docs]` Experimental removal: an unmaintained protocol is removed after **three months** of author inactivity, where all three hold — no author changes to the protocol, no author comments on the protocol MR, no author mails to the mailing list about it — after notification in the MR and a **one-week** grace period of continued inactivity (S040, §2.3.2, GOVERNANCE.md:168-177).
- `[INF-docs]` Experimental promotion: a merged experimental protocol may be promoted to `staging/` upon request if it meets the staging landing requirements, and is then removed from `experimental/` (S040, §2.3.3, GOVERNANCE.md:179-184).
- `[INF-docs]` NACK is restricted to listed points-of-contact of member projects and must be grounded in technical reasoning; a non-point-of-contact using the term on a non-governance thread is banned for at least three months (warning for a first offence), and a member's non-technical NACK can be tried and the contact removed (S040, §3, GOVERNANCE.md:186-206).
- `[INF-docs]` Amending GOVERNANCE itself needs a 30-day discussion and ACK by at least 2/3 of member projects with no NACK (S040, §4, GOVERNANCE.md:208-217).

## What the phase label does not prove (host boundary)

- `[INF-docs]` A phase is an upstream package property. Nothing in S005 or S040 states that a compositor implements a protocol, that an advertised global conforms to its XML, or that a host has a particular protocol version.
- `[OBS]` The sibling capture `.ufo/waves/round-13/w1/globals.json` proves only that `wayland-info` listed the named interfaces and versions at 2026-10-20 on this host. Presence is advertisement, absence is not proof of non-support (feature gating, compositor policy, runtime options and build configuration are outside the capture).
- `[INF-docs]` A `zw…` interface prefix is legacy naming from the old unstable policy, not a statement that the protocol is currently experimental (S005, README.md:55-63). Conversely, an `xx…` prefix marks an experimental protocol (S040, §2.1.1).
- `[UNK]` The host's protocol conformance, request behavior and any feature-gate were not measured. No `wl_display.sync`, registry bind, or protocol request was issued by this seat.
- Sibling crosswalk (other seat, not this seat's evidence): `MadoR13.GlobalCapture` reports that the 72 advertised globals map to 5 stable, 28 staging advertisements (27 unique), 12 unstable and 27 absent from the pinned tree; it names `zwp_linux_dmabuf_v1` and `zwp_tablet_manager_v2` as stable protocols with a `z`-prefixed interface, and reports that `ext_` and `xdg_` names span phases. Merge that crosswalk into the globals section as the other seat's host-plus-tree join; it corroborates this section's rule that the interface prefix is not the phase, but it must not be cited as a source statement from S005/S040.

## Limits

- Only `README.md` and `GOVERNANCE.md` at the pinned revisions were read. No protocol XML, `MEMBERS.md`, `meson.build`, release notes beyond the tag list, or issue/MR history was opened.
- GOVERNANCE describes process. Whether a specific protocol satisfied ACKs, implementations, review or discussion periods is not verified here.
- The 30-day and two-week periods are procedural minima; elapsed wall-clock time in a specific MR was not measured.
- The `deprecated/` and `unstable/` directories were not enumerated; this entry states the rule, not a current inventory.
- The phase statements are `[INF-docs]` and are scoped to the `wayland-protocols` package at tag `1.49`; they do not describe Hyprland 0.56.2 or any other implementation.
- A future release can change the phase rules; the recheck below is release-triggered, not a calendar promise.

## Rejected

| Rejected inference | Why it fails | Evidence |
|---|---|---|
| “A `staging` protocol is stable and backward-compatible by guarantee.” | Staging only “should try to minimize” incompatible changes; the disclaimer allows compatible additions with an interface bump and incompatible changes via a new major version. | S005, README.md:27-28, :208-215. |
| “Anything merged upstream is stable.” | Merged protocols are in one of the three phases **except** deprecated and legacy protocols; stable requires a separate declaration. | S005, README.md:19-22, :221-231. |
| “Stable can never be superseded.” | The text says “unexpected to become superseded by a new major version”, an expectation, not a prohibition. | S005, README.md:44-47. |
| “The `z` prefix proves a protocol is currently experimental.” | The `z` prefix belongs to the legacy unstable policy; current experimental interfaces use `xx`. | S005, README.md:55-63; S040, §2.1.1. |
| “An advertised global proves the host implements the protocol at the advertised version.” | Advertisement is a registry fact; conformance and behavior require requests and were not measured. | `.ufo/waves/round-13/w1/globals.json`; this entry's boundary section. |
| “A deprecated protocol is deleted.” | Deprecation stops changes; the `deprecated/` directory retains the protocol. | S005, README.md:49-53, :65-75. |

## Recheck

Re-run at each upstream release (the S005/S040 rows are `on-release`) or when the tag moves:

```sh
# latest tag and main head
git ls-remote --tags https://gitlab.freedesktop.org/wayland/wayland-protocols.git \
  | sed 's#.*refs/tags/##' | grep -v '\^{}' | sort -V | tail -5
git ls-remote https://gitlab.freedesktop.org/wayland/wayland-protocols.git refs/heads/main

# pinned bytes (expect the two hashes in §Source pins)
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/README.md | sha256sum
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/GOVERNANCE.md | sha256sum

# the mined sections
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/README.md \
  | sed -n '17,75p;129,141p;162,256p'
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/GOVERNANCE.md \
  | sed -n '61,129p;160,217p'
```

If a release changes any mined statement, append a dated erratum naming the old statement, the new statement, the source and the evidence class; do not rewrite the historical text.
````

## 4. Registry state: authored proposal vs landed rows (no edit applied)

Registry path: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`. The proposal followed `SOURCES-CONTRACT-v1.md` rule 2: only `status`, `recheck` and `used-by` change in place; a new row is appended. **Current state: both changes already landed.** S005 (`:17`) is `mined` with `used-by` the entry; S040 (`:52`) exists as `spec`, pin `35d9638c`, `mined`, same `used-by`. Verify, do not re-apply.

### 4.1 S005 — landed exactly as proposed

Current row (`corpus/SOURCES.md:17`, 11 columns, `NF=13`):

```
| S005 | wayland-protocols README — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md | docs | A | wayland protocol phasing and change policy (ground for later U4/U6 rounds) | README.md §Protocol phases @ main 3dac056d (2026-01-16, last commit touching README.md) | experimental/staging/stable semantics: what may break in each phase, deprecation, legacy z-prefix; gives the vocabulary to age-check a protocol claim | queued | 2026-10-19 | on-release | — |
```

Authored in-place diff (all other cells byte-identical); the landed cells match the `New` column:

| Cell | Old | New |
|---|---|---|
| `status` | `queued` | `mined` |
| `used-by` | `—` | `corpus/knowledge/wayland-protocol-boundaries-r13.md` |
| `recheck` | `on-release` | `on-release` (unchanged) |
| `anchor` | `README.md §Protocol phases @ main 3dac056d (2026-01-16, last commit touching README.md)` | unchanged — re-verified: `README.md` at tag `1.49` (ee78491a) and main `35d9638c` is byte-identical to `3dac056d`'s last-touch bytes, sha256 `e81ad629…` |

Landed row (verbatim at `:17`):

```
| S005 | wayland-protocols README — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md | docs | A | wayland protocol phasing and change policy (ground for later U4/U6 rounds) | README.md §Protocol phases @ main 3dac056d (2026-01-16, last commit touching README.md) | experimental/staging/stable semantics: what may break in each phase, deprecation, legacy z-prefix; gives the vocabulary to age-check a protocol claim | mined | 2026-10-19 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md |
```

Old→new log for the round lesson (the registry already reflects it): `S005: status queued → mined; used-by — → corpus/knowledge/wayland-protocol-boundaries-r13.md; recheck unchanged`.

### 4.2 S040 — candidate row vs landed row

Landed state: S040 already exists at `corpus/SOURCES.md:52` — `spec`, tier A, pin `35d9638c` (2026-10-12), scope “Namespace-specific protocol inclusion and promotion authority, not runtime support”, status `mined`, used-by the entry. **Do not append a second S040.** The candidate below is the authored draft; the landed row is authoritative.

```
| S040 | wayland-protocols GOVERNANCE — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/GOVERNANCE.md | docs | A | wayland protocol phase admission and promotion process (ground for U4 phase boundaries) | GOVERNANCE.md §2.1-§4 @ tag 1.49 ee78491a (2026-06-07; main 35d9638c differs only at :174) | namespaces (xx/xdg/wp/ext), ACK/implementation/review thresholds, 30-day introduction and stable-promotion periods, two-week experimental review, three-month experimental removal, one-year staging option, NACK scope — the procedural half of the phase model | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md |
```

Candidate column check (11 content columns, `NF=13`): id `S040`; source; kind `docs`; tier `A`; scope; anchor; teaches; status `mined`; opened `2026-10-20`; recheck `on-release`; used-by.

| Cell | Authored candidate | Landed S040 | Action |
|---|---|---|---|
| `kind` | docs | spec | none; both are in the contract enum and `kind` is not an in-place cell |
| `anchor` | tag 1.49 `ee78491a` + main note | `35d9638c` | none; direct comparison shows identical mined text, only `:174` typo differs |
| `teaches` | procedural gates and periods | inclusion/review scope, not runtime | none; `teaches` is not an in-place cell |
| `status` / `used-by` | mined / entry | mined / entry | matches |
| `tier` | A | A | matches |

Tier rationale: official project governance document for the `wayland-protocols` scope — A by contract (“primary or authoritative for that scope … official docs”). The landed `kind=spec` is also contract-valid; no tier inflation either way.

Anchor rationale: the landed row pins the last commit touching `GOVERNANCE.md` (`35d9638c`, 2026-10-12). The authored candidate pinned the released tag (`1.49` = annotated tag object `a8d65d7f…`, peeled commit `ee78491a…`); the file is unchanged since the last semantic change `9dd051b4…` (2024-11-06), and the only later delta is the line-174 spelling. Both anchors resolve to the same mined text.

Independent verification of the landed row: `35d9638c` is the last commit touching `GOVERNANCE.md`; the §2.1–§2.3 text it relies on is byte-identical at tag 1.49 except the one-word typo at `:174`; its `teaches` is supported by §2.2/§2.3; the row parses as 13 fields; its `used-by` path exists. No correction is required. If the round lesson wants the tag-1.49 evidence, record it in `## Gate` below without editing the row.

### 4.3 Proposed search-log entry (append under `## Search log`)

```
From the `protocol-phases` seat (round 13):

- Question: what are the upstream rules for the experimental, staging and stable
  phases, and for deprecation/promotion? Where: S005 README and the GOVERNANCE.md
  lead named unopened in round-12 `## Leads`; canonical GitLab raw URLs at tag
  1.49 (commit ee78491a) plus main head 35d9638c, opened 2026-10-20. Identified 2,
  screened 2, included 2, excluded 0. Stop rationale: both files answer the phase
  and admission rules at a pinned revision; no third source is needed.
```

The round-12 lead “wayland-protocols GOVERNANCE.md §2.1-2.3 and MEMBERS.md” is now closed for the GOVERNANCE half by the landed S040. The note above is the authored search-log entry; keep it if the round log records this seat's search, otherwise it is provenance only. `MEMBERS.md` remains unopened by this seat and is not needed for the rule statements (the entry does not name member projects).

### 4.4 Measured registry and join state (2026-10-20)

Registry measured after the concurrent landing: `45` rows; malformed `NF!=13` = `0`; tier `A=41 B=1 C=3`; status `mined=33 queued=8 rejected=4`; no duplicate ids. S005 and S040 both parse and both name the entry in `used-by`.

| Measure | Measured |
|---|---|
| rows | 45 |
| malformed rows (`NF!=13`) | 0 |
| tier histogram | `A=41 B=1 C=3` |
| status histogram | `mined=33 queued=8 rejected=4` |
| duplicate ids | none |

Join state for the entry's cited rows: S005, S040, S041, S042 and S043 are all `mined`, all name `corpus/knowledge/wayland-protocol-boundaries-r13.md` in `used-by`, and the entry's `source:` header (line 1) cites all five. The pre-landing caveat is resolved: the entry exists. C1 at this observation: `5` sourced entries; `covers:` lines U1–U4 (`4/7`). Scoring is L1's job, not this seat's verdict.

The lesson `corpus/lessons/round-13.md` landed concurrently and its `## Gate` now records S005 (reopened, commit `3dac056d`) and S040 (commit `35d9638c`); the S017/S044 `used-by` paths resolved with it. The only remaining join flag is pre-existing: the U2 entry still cites S030, the rejected duplicate, as recorded in its round-12 erratum. It does not involve S005/S040.

## 5. Proposed lesson Gate entries (round 13)

The round-13 lesson landed concurrently (`corpus/lessons/round-13.md`) and its `## Gate` already records S005 (reopened, commit `3dac056d`) and S040 (commit `35d9638c`) with different but valid quotes. The block below is the authored **tag-1.49 variant** of those records (URL, access date, ≤25-word quote, location, revision, tier, admission, flip, plus the old→new status log). Do not duplicate the lesson rows; use this variant only if the integrator prefers the tag pin.

```
- S005 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md — re-opened 2026-10-20 — "Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase." — §Protocol phases, README.md:19-20 at tag 1.49 (commit ee78491a, 2026-06-07; sha256 e81ad629…; identical at main 35d9638c and last-touch 3dac056d). Registry change (already applied at `corpus/SOURCES.md:17`): status queued → mined; used-by — → corpus/knowledge/wayland-protocol-boundaries-r13.md; anchor unchanged. Flip: a commit or release that alters README.md §Protocol phases, or a moved 1.49 tag.
- S040 — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/GOVERNANCE.md — opened 2026-10-20 — "Declaring a protocol stable may be proposed by the same process, with the regular 30 day minimum discussion period." — §2.3 item 6, GOVERNANCE.md:125-126 at tag 1.49 (commit ee78491a, 2026-06-07; sha256 b09930ca…; main 35d9638c differs only at :174). Admission: landed at `corpus/SOURCES.md:52` as kind spec, tier A, status mined, used-by corpus/knowledge/wayland-protocol-boundaries-r13.md; the quoted sentence is byte-identical at the landed pin 35d9638c and at tag 1.49. Flip: a release that amends §2.3 or moves the stable-declaration period.
```

Quote lengths: S005 = 16 words (≤25); S040 = 19 words (≤25), counted by whitespace tokenization.

## 6. Evidence ledger (this seat)

| ID | Source / URL | Accessed | Exact quote | Location | Revision | Tier / kind | Admission | Flip |
|---|---|---|---|---|---|---|---|---|
| E1 | `README.md` — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/README.md | 2026-10-20 | “Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase.” | §Protocol phases, README.md:19-20 | tag 1.49 `ee78491a`, 2026-06-07, sha256 `e81ad629…` | A / docs | S005 queued→mined | any release changing §Protocol phases |
| E2 | `README.md` (same pin) | 2026-10-20 | “Protocols in the staging phase should try to minimize backward-incompatible changes, and protocols in the stable phase should avoid backward-incompatible changes.” | README.md:27-29 | same | A / docs | supports phase posture | any release rewording the expectations |
| E3 | `README.md` (same pin) | 2026-10-20 | “Backward-incompatible changes can only be introduced in a new major version of a protocol.” | README.md:24-25 | same | A / docs | supports breakage rule | any release changing the major-version rule |
| E4 | `README.md` (same pin) | 2026-10-20 | “No more changes will be made to a deprecated protocol.” | §Deprecation, README.md:52-53 | same | A / docs | supports deprecation rule | any release changing deprecation |
| E5 | `README.md` (same pin) | 2026-10-20 | “During this phase, protocol interface names were, in addition to the major version postfix, also prefixed with `z` to distinguish them from stable protocols.” | §Legacy protocol phases, README.md:61-63 | same | A / docs | supports legacy-prefix rule | any release deleting the legacy section |
| E6 | `README.md` (same pin) | 2026-10-20 | “Each release of wayland-protocols finalizes the version of the protocols to their state they had at that time.” | §Releases, README.md:255-256 | same | A / docs | supports release semantics | any release changing release policy |
| E7 | `GOVERNANCE.md` — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/GOVERNANCE.md | 2026-10-20 | “Declaring a protocol stable may be proposed by the same process, with the regular 30 day minimum discussion period.” | §2.3 item 6, GOVERNANCE.md:125-126 | tag 1.49 `ee78491a`, sha256 `b09930ca…` | A / docs | S040 admitted mined | a release amending §2.3 |
| E8 | `GOVERNANCE.md` (same pin) | 2026-10-20 | “Experimental protocols begin with the "xx" namespace and do not include any relation to namespaces specified in section 2.1.” | §2.1.1, GOVERNANCE.md:78-79 | same | A / docs | supports namespace rule | amendment of §2.1.1 |
| E9 | `GOVERNANCE.md` (same pin) | 2026-10-20 | “Protocols in the "xdg" and "wp" namespace are eligible for inclusion only if ACKed by at least 3 members.” | §2.2 item 2, GOVERNANCE.md:86-87 | same | A / docs | supports inclusion threshold | amendment of §2.2 |
| E10 | `GOVERNANCE.md` (same pin) | 2026-10-20 | “Unmaintained experimental protocols are removed after a three month period of inactivity by its author” | §2.3.2 item 1, GOVERNANCE.md:170-171 | same | A / docs | supports removal rule | amendment of §2.3.2 |
| E11 | `GOVERNANCE.md` (same pin) | 2026-10-20 | “in use without substantive changes for a period of one year” | §2.3 item 7, GOVERNANCE.md:128-129 | same | A / docs | supports one-year staging option | amendment of §2.3 |
| E12 | `GOVERNANCE.md` (same pin) | 2026-10-20 | “an amendment will become effective if it's ACKed by at least 2/3rds of all wayland-protocols member projects, and NACKed by none.” | §4 item 3, GOVERNANCE.md:214-217 | same | A / docs | supports amendment rule | amendment of §4 |

All quotes are `[INF-docs]`: official upstream documentation, not installed-host facts. The `main` file was also fetched and compared; only GOVERNANCE.md:174 differs (`persuant` → `pursuant`), so the pin does not hide a semantic change.

## 7. Boundary and non-goals (explicit)

- **No host extrapolation.** This draft does not claim the host implements any protocol, that any advertised version is current, or that Hyprland follows any phase rule. The only host datum referenced is the sibling `globals.json` capture as a separate layer; it is not evidence for this section's statements.
- **No registry edit.** `corpus/SOURCES.md` was read only. The rows in §4 are proposals for the integrator.
- **No knowledge/lesson/SKILL edit.** The block in §3 and the Gate text in §5 are drafts; the named knowledge file does not exist yet.
- **No gate edit, no selftest, no regression, no build/lint/format.** Those belong to GateImplement and the post-integration verifier.
- **No compositor/config/state read.** No `hyprctl`, `wayland-info`, `~/.config`, `~/.local/share` or `~/.local/state` access by this seat.
- **No secret/session material.** No tokens, titles or raw environment were read.

## 8. Verification commands for the integrator

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
# 1. upstream pin still resolves and matches (expect the two sha256 values in §2)
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/README.md | sha256sum
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/ee78491a237eaff9389a0ccf8680521d074407d3/GOVERNANCE.md | sha256sum

# 2. tagged release is still the highest and still peels to ee78491a
git ls-remote --tags https://gitlab.freedesktop.org/wayland/wayland-protocols.git \
  | sed 's#.*refs/tags/##' | grep -v '\^{}' | sort -V | tail -3
git ls-remote https://gitlab.freedesktop.org/wayland/wayland-protocols.git 'refs/tags/1.49*'

# 3. quoted anchors
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/README.md | sed -n '19,20p;24,29p;49,63p;162,182p;184,251p;253,256p'
curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/GOVERNANCE.md | sed -n '61,129p;160,217p'

# 4. current registry shape (measured 2026-10-20: 45 rows, 0 malformed,
#    A=41 B=1 C=3, mined=33 queued=8 rejected=4, no duplicate ids)
#    Re-derive; other seats may append rows.
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d

# 5. join (the entry and lesson now exist). S005/S040/S041/S042/S043 join
#    clean; the only remaining flag is the U2 entry's S030 citation —
#    pre-existing and unrelated, reported in §4.4.
awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ {i=$2;s=$9;u=$12; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",s); gsub(/^[[:space:]]+|[[:space:]]+$/,"",u); print i"\t"s"\t"u}' corpus/SOURCES.md > /tmp/mado-r13-rows.tsv
while IFS=$'\t' read -r i s u; do [ "$s" = mined ] || continue; for p in ${u//,/ }; do grep -qw "$i" "$p" || echo "row $i used-by $p does not cite it"; done; done < /tmp/mado-r13-rows.tsv
for f in corpus/knowledge/*.md; do src=$(head -n 15 "$f" | grep -E '^source:'); [ -n "$src" ] || continue; for i in $(grep -oE '\bS[0-9]{3,}\b' <<<"$src" | sort -u); do awk -F'\t' -v i=$i -v f="$f" '$1==i && $2=="mined" && index($3,f) {ok=1} END{if(!ok) print "entry "f" cites "i" without a mined row naming it"}' /tmp/mado-r13-rows.tsv; done; done; echo join-done

# 6. C1 (measured 2026-10-20: 5 sourced entries, covers U1-U4)
for f in corpus/knowledge/*.md; do head -n 15 "$f" | grep -qE '^source:.*\bS[0-9]{3,}\b' && echo "$f"; done | wc -l
grep -lE '^covers:.*U4' corpus/knowledge/*.md
```

## 9. Tooling record

- Installs or upgrades: **none**. Used host-provided `curl`, `git`, `sha256sum`, `sed`, `grep`, `awk`, `sort`, `python3`.
- No tool was installed, upgraded or reconfigured by this seat.
