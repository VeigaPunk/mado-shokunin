# ReviewSourceTier — U6 primary source tiers and immutable revision anchors

Seat: MadoR15.ReviewSourceTier (reviewer, leaf). Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope: adversarial review of U6 source tiers and revision anchors only. No registry, corpus, SKILL, SCORECARD, LOG or gate edits; no tests, gates, builds, smoke runs, live probes or input-device access. No credential/auth files, no `agent.db*`, no omp CLI, no delegation.

## Tooling record

- No tools installed or upgraded. Used existing `curl`, `sha256sum`, `git`-free Python `hashlib`, `pacman -Q` (read-only query).
- Scratch fetches written only to `/tmp/r15review/` (not durable evidence; removed after this report).

## Verdict

**Conditional.** The U6 integration is admissible on source grounds only if S051 and S052 are added as `mined` tier-A rows pinned to the exact revisions below, scoped to documentation/specification semantics, and the U6 note does not treat them as host behavior. The existing S007 row cannot serve as the anchor. The round-14 measure does not check tier scope or anchor revisions, so acceptance depends on the explicit checks in §4.

## 1. Current state (observed)

| Item | Observation | Pointer |
|---|---|---|
| Registry contract | Tier scoped, status lifecycle; "anchor = section plus revision"; queued rows never sole support | `corpus/SOURCES.md` header (lines 1-9); owed-anchor bullet, `SOURCES.md` search log (~line 115) |
| S007 (libinput tools) | tier A, status `queued`, URL `wayland.freedesktop.org/libinput/doc/latest/tools.html`, anchor = section names + "libinput 1.32.0 documentation (opened 2026-10-19)". **No revision SHA; `latest` is a mutable URL.** | `corpus/SOURCES.md:19` |
| S006 | Same owed-anchor defect; superseded in place-free manner by S042 (new row, `supersedes S006 —`). Precedent for U6 superseding S007. | `corpus/SOURCES.md:18`, `:54`; `corpus/lessons/round-13.md` (Registry mutations) |
| S043 (wl_registry) | tier A, anchor = **installed** `/usr/share/wayland/wayland.xml` lines 117-177, **no sha256, no upstream tag**. Installed file is host-mutable across package upgrades. | `corpus/SOURCES.md:55` |
| S005 / S048 / S050 | Commit-pinned (`@ 3dac056d`, tag `1.49`, `@ efb5099…`) with raw sha256 on some. Model for the anchor standard. | `corpus/SOURCES.md:17`, `:60`, `:62` |
| S051 / S052 | Not present in registry (none found under `corpus/`). Reserved by spec only. | `.ufo/waves/round-15/w1/spec.json` (MeasureBuild item) |
| Host libinput | `pacman -Q libinput` → **1.31.3-1**. Row S007 scope and the 1.32.0 doc are **not** the host version. | static query, this session |
| Host wayland XML | `/usr/share/wayland/wayland.xml`, `wayland 1.26.0-1`, sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`. `wl_pointer` at XML line 2138, `wl_keyboard` at 2573, `wl_seat` at 2004. | `/usr/share/wayland/wayland.xml` |

## 2. Upstream revision anchors verified (read-only fetch, byte-checked)

Candidate S051 — libinput helper tools:

- Raw URL: `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`
- Tag `1.32.0`: tag object `c7e6fe66f509ba2eda680c28aa64795987b49e7c`, commit `5cf833b572f5a33663888da321dce0ba1abd82a2` (created 2026-09-17, "libinput 1.32.0"), via GitLab API `repository/tags/1.32.0`.
- Blob `doc/user/tools.rst` at tag: git blob id `390bab188b71a546e936eb7e2df3cf096d946640` (recomputed locally from fetched bytes: match), 16990 bytes, sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`.
- Section pointers in that blob: "Most of the tools must be run as root" `:31-32`; `list-devices` `:37`, scope note "does **not** show your desktop's configuration, just the libinput built-in defaults" `:45-46`; `debug-events` `:133`; `debug-gui` `:183`; `record and replay` `:207`, "obscures key codes by default" `:262`, "Users are advised to always replay" `:281`; `measure` `:354`; `analyze` `:367`; `quirks` `:379`.
- The `latest` HTML page (opened 2026-10-19, S007) contains the same root and record/replay statements, so S007's content is consistent with the tag; it is still not a pinned anchor.

Candidate S052 — Wayland core protocol XML:

- Raw URL: `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`
- Tag `1.26.0`: tag object `5f430e41167dd359b70fb5e9f584ba2dc058e4cc`, commit `87cc8a8728a923fc57938faa81ba0e74f34ecdc7` (GitLab API `wayland/wayland` tags).
- Fetched bytes: 168656 bytes, sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` — **byte-identical to the installed `/usr/share/wayland/wayland.xml`** (`cmp` equal).
- Protocol pointers: `wl_pointer` `:2138`, `wl_keyboard` `:2573`, `wl_seat` `:2004`. Line numbers match the installed file.

## 3. Adversarial findings (ordered by severity)

**F1 (high) — The round-14 measure cannot enforce tier scope or anchor immutability.** `.ufo/waves/round-14/measure.py` reads only `status`, `tier` (A/B/C counting) and `used-by`; it never parses the `anchor` column. The join at `measure.py:193` admits any note where **one** cited `mined` row is tier A or B, and tiers C and any unpinned anchor co-cited with it still pass. The report's "revision-bound" wording refers to the measured repo revision, not to source-row anchors. Consequence: a U6 note citing S051 (A, pinned) plus S043 (A, installed path) or S010 (C, if mined) would count as covered. Only reviewer checks can reject that.

**F2 (high) — S007 cannot be the U6 anchor.** Its anchor has no revision SHA, its URL is the mutable `doc/latest/`, and the status is `queued`. Flipping S007 to `mined` in place would violate the "anchor = section plus revision" rule and the contract's "only status/recheck/used-by change in place" rule (flip would also need a lesson log). Use a superseding row, as S042 did for S006.

**F3 (high) — Version scope mismatch.** Host `libinput` is 1.31.3-1; S007 and S051 describe 1.32.0. Any U6 statement about host option names, default states or record/replay availability must either cite 1.31.3 evidence (static help, which is not in scope here) or be labeled `[UNK]`/`[INF-docs] upstream 1.32.0`. Applying the 1.32.0 page to the host is a tier-scope violation.

**F4 (medium) — S043 is host-path anchored.** `/usr/share/wayland/wayland.xml` is a mutable installed path. S043 is admitted and cannot be "retro-pinned" without a superseding row. U6 must cite S052 (tag-pinned + sha256 equality) for wl_keyboard/wl_pointer definitions, not S043.

**F5 (medium) — Tier scope of protocol and documentation sources.** S051 and S052 support **documented semantics only** (what the tool reads/writes, what `wl_keyboard`/`wl_pointer` events are defined to carry). They are tier A for their scope, not evidence of Hyprland's focus, delivery, text-input or pointer behavior on this host. The libinput page itself states that `list-devices` shows built-in defaults, not the desktop's configuration (`tools.rst:45-46`) and that the output "may change at any time" (`:78-79`). Those caveats must survive into the note.

**F6 (low) — Same-scope duplicate without supersedes link.** S051's URL differs from S007's, so no active-URL collision is triggered; the scope is the same. Using `teaches` opening `supersedes S007 —` (S042 precedent) is recommended to keep the same-scope relation explicit for the merge reviewer.

**F7 (low) — Mutable mirrors.** `wayland.freedesktop.org/libinput/doc/latest/` will move to later releases; `main` branch anchors (S005) are only safe with the commit suffix present. Recheck cadence for S051/S052 should be `on-release`, not 180d.

## 4. Acceptance conditions (all required)

1. **S051 row** exists, `status=mined`, `tier=A`, kind `docs`, URL = the tag-pinned raw URL above; anchor cell contains tag `1.32.0`, commit `5cf833b572f5a33663888da321dce0ba1abd82a2`, blob `390bab188b71a546e936eb7e2df3cf096d946640`, sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`. Opened date and `used-by` name the U6 note path.
2. **S052 row** exists, `status=mined`, `tier=A`, kind `spec`, URL = `.../wayland/-/raw/1.26.0/protocol/wayland.xml`; anchor contains tag `1.26.0`, commit `87cc8a8728a923fc57938faa81ba0e74f34ecdc7`, sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, and the installed-equality statement (`cmp` / sha match).
3. **Re-derivation commands** published in the note or lesson, each runnable without clone: `curl -sSfL <raw URL> | sha256sum`, and `curl -sSfL https://gitlab.freedesktop.org/api/v4/projects/<id>/repository/tags/<tag>` for the commit id. QUALITY criterion 6 and 12 require this.
4. **S007 untouched as sole support.** It remains `queued` (or is superseded by S051 with `supersedes S007 —` in S051's `teaches`); the U6 note cites S051/S052 for documented semantics and does not cite `doc/latest/` as an admitted anchor.
5. **Reciprocal join.** The U6 note's `source:` header names S051 and S052; each row's `used-by` names the note path. The measure's join (`measure.py:167`) then counts them; no queued row is counted.
6. **Tier-scoped claims.** Every U6 claim is labelled `[INF-docs]` (upstream documented semantics) or `[UNK]`. No host keyboard/pointer/focus/delivery claim is supported by S051/S052/S043/S040/S041 alone. S008 (B) and S010 (C) are not sole support for any claim.
7. **Version-scoped host claims.** Any host libinput statement is either tied to a 1.31.3-1 observation or marked `[UNK]`; the 1.32.0 page is never presented as host-version fact.
8. **No in-place anchor edit.** S043/S005/S007 anchors unchanged; any status flip logged old→new in the round lesson.

## 5. Rejection conditions (any one rejects the integration)

- A row admitted with an anchor lacking a commit/tag SHA or content sha256 (e.g., `latest`, `main` without commit, installed path only).
- S007 flipped to `mined` with its current anchor, or used as the sole support for a U6 claim.
- A U6 claim about host libinput/Hyprland/compositor behavior supported only by S051/S052 or only by tier B/C rows.
- The sha256 or blob id in the anchor does not reproduce from the URL (re-derivation mismatch).
- Used-by/`source:` reciprocity missing, or a `queued` row counted in the coverage join.
- Treating `measure.py` output (coverage count, tier counts) as proof that anchors are immutable or tiers are correctly scoped. The measure does not check either.
- Any use of S043 for wl_keyboard/wl_pointer definitions in place of S052.

## 6. Residual risk and verification gaps

- Not verified: the libinput 1.31.3 documentation or host `libinput --help` (out of scope; no host command was run). Host option claims therefore remain `[UNK]`.
- Not verified: byte-equality of the `latest` HTML to the tag-pinned rst; the HTML was read as content, not as bytes. Equivalence is only claimed at the level of the cited statements.
- Not verified: the git blob id of the wayland XML (only file sha256 checked; the `wl_keyboard` and `wl_pointer` line numbers are the same in both copies).
- The round-14 measure's tier counts (`measure.py:548-551`) are aggregate; per-claim tier scope is not computed anywhere. This review is the only check of that property.
- Scratch copies under `/tmp/r15review/` were removed after reading; they are not evidence.
