# Round 15 — GateDecisions: admit/reject sample matrix (U6, R14-V1)

Seat: `MadoR15.GateDecisions` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Axis: coverage (C1, U1–U5 5/7 → U1–U6 6/7). R14-V1 is an unscored lesson-backed correction, not a U-item.
Status: **DRAFT. Outside non-author admit/reject spot-check PENDING.** This seat is an authoring-lane
advisory; it does not clear admission and writes no registry, corpus, SCORECARD, LOG or SHONEN change.

## Reads and checks performed (read-only)

- Lane: `corpus/lessons/round-14.md`, `corpus/lessons/round-14-verifier-spotcheck.md` (R14-V1 at line 169),
  `corpus/SOURCES.md` (rows S005–S010, S041, S047–S050), `corpus/QUALITY.md` (criteria 4, 7, 9, 13, 18, 19),
  `SCORECARD.md` (round-15 coverage rubric and U-list), `.ufo/waves/round-15/w1/spec.json` (GateDecisions item).
- R14 receipt headers, first 6 lines each: `.ufo/waves/round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt`.
- Primary doc opened this round (static, no tool execution): https://wayland.freedesktop.org/libinput/doc/latest/tools.html
  (page title "libinput 1.32.0 documentation"; S007 re-open for spot-check, not a new registry row).
- Static presence/version only: `command -v libinput wayland-info hyprctl`; `libinput --version` → `1.32.0`;
  `pacman -Q libinput wayland-utils` → `libinput 1.32.0-1`, `wayland-utils 1.3.0-1`.
- Not run: `libinput debug-events`, `libinput record`, `libinput replay`, `list-devices`, `list-kernel-devices`,
  `hyprctl devices`, any input event read/record/replay/injection, any compositor action, any test/gate/build/lint/smoke.
- Not opened: `~/.omp/agent/agent.db*`, credential or auth files, `agent://all`, any sibling/fleet repo write.
- Web search returned secondary man-page mirrors only; not used as evidence.

## Tooling

- No install or upgrade by this seat.
- Observed, not installed by this seat: `libinput 1.32.0-1` and `wayland-utils 1.3.0-1` are present under `/usr/bin`
  (pacman-recorded). **Correction to the scout ledger:** `wave/.../l2-scout` U6 row says libinput and wayland-info are absent;
  that is stale for the current host and must be re-read before any U6 claim cites it.

## Part A — U6 sample matrix (kernel input → Wayland debugging ladder)

| # | Candidate item | Draft decision | Reason (anchor) | Flip condition |
|---|---|---|---|---|
| U6-1 | Document the libinput helper-tool route as a **static, ordered ladder**: inventory (`list-kernel-devices`, `list-devices`) → interpreted events (`debug-events`) → kernel record/replay (`record`/`replay`), with root requirement | **Admit, conditional** — only after S007 gets a superseding row (see Part C) | Opened page: "Most of the tools must be run as root…"; `list-devices` "does not show your desktop's configuration, just the libinput built-in defaults"; `record` "records the **kernel** events… independent of the libinput context". Ladder is documentation-only, `[INF-docs]`. | Reject if the superseding row or note asserts any host observation from these tools (none run this round). |
| U6-2 | Claim: `libinput list-devices` proves compositor-applied keyboard/touchpad settings | **Reject** | Same page: built-in defaults only. Replicates round-12 M04 (`corpus/lessons/round-12.md:37`). | Layer-labelled compositor-side probe of applied config, plus a host sample. Not this round. |
| U6-3 | Claim: `debug-events` / `record` shows what Hyprland delivered to a client | **Reject** | `debug-events` prints libinput-processed events; delivery to a client is a compositor/Wayland layer and is unexercised (`[UNK]`). Layer confusion of the S007 kind. | Authorised compositor-side observation with its own anchor; still outside C1's no-event-collection fence. |
| U6-4 | Claim: U6 host ladder is verified on this host (any rung observed) | **Reject** | Zero rungs executed; only presence/version was read (see Tooling). Presence ≠ observation. | Explicit later round authorising a bounded read-only sample under the input-safety fence. |
| U6-5 | Use S010 (wayland.app, tier C) as sole support for any protocol/tool claim | **Reject** | Registry rule: community never sole support; S010 is `queued` discovery index. | Never as sole support; may remain a discovery aid. |
| U6-6 | Use S008 (wayland-book, tier B) or S009 (architecture, tier A) as sole support for "compositor sits between libinput and clients" | **Reject for now** | Both `queued` with access date only, no page revision — round-12 owed-anchor debt (`corpus/SOURCES.md` search-log errata, S006/S008/S009/S010). | Superseding row with a source revision, then admit as concept ground only alongside S007 or another mined row. |
| U6-7 | Record or replay any real input on this host to build the ladder example | **Reject** | Outside C1: "No new capability or input event collection"; `record` obscures keycodes but still captures device events. | Separate authorised round with consent, device scope and privacy plan. |
| U6-8 | Mark U6 "closed" (delivery, IME, kernel-level behaviour) | **Reject** | Retained limits: delivery/IME/kernel diagnosis not exercised. Round-14 precedent: "U6/U7 not admitted". | Feature-specific observed evidence per limit. |

Hold set: U6 covered requires an entry with `source:` citing a `mined` row that names U6, plus one `covers: U6` line
(SCORECARD round-12 rubric). **No U6 row is `mined` today** (S006–S010 are `queued`). Admission therefore depends on Part C, step 1.

## Part B — R14-V1 sample matrix (ancillary mutation receipt precision)

Verified this seat: `regression-recut.txt:3-4` shows `input_binding: provisional worktree snapshot` and
`gate_sha256: ef50e262…`; `regular-target-mutants.txt:3-4` and `retained-census-mutants.txt:3-4` show
`input_binding: provisional worktree snapshot` and `gate_sha256: d6d5eb27…`. No `measured_commit` header in any of the three
(first 6 lines read). The derived target `cd1d73d7…` is **not recomputed by this seat** (`[INF]` from the verifier's statement).

| # | Candidate item | Draft decision | Reason (anchor) | Flip condition |
|---|---|---|---|---|
| V1-1 | Append explanatory correction mapping each provisional header to the committed derived target `cd1d73d7…`; keep historical bytes | **Admit as correction** (not expansion, not a U-item) | Verifier routed it (`round-14-verifier-spotcheck.md:169`); headers confirmed above; kill counts 10/10, 4/4, 8/8 stay as derived-target evidence only. | Reject if `cd1d73d7…` cannot be re-derived from committed content at the correction commit; then keep as open debt. |
| V1-2 | Read the three receipts as standalone final-full-gate receipts | **Reject** | Their `MUTATE_TARGET` binds the derived target, not the full gate; the excised machinery is outside the claim (verifier text). | A new standalone receipt carrying `measured_commit`, `gate_sha256` (raw gate digest), exact command and observed exit (R14 M3 pattern). |
| V1-3 | Rewrite the historical receipts to add headers | **Reject** | Append-only: QUALITY 4 (errata) and 13 (evidence = committed path + sha). | None in-round. |
| V1-4 | Add a new QUALITY criterion for receipt header provenance | **Reject (duplicate)** | QUALITY 7 (hash from `git show`, label provisional) and 9 (bind verdicts to commit/sha) already cover it; R13-V2/V3 precedent uses 7, 9, 13. | A failure mode criteria 7/9 cannot catch — e.g. header present but digest wrong after the correction — with a lesson citation. |
| V1-5 | Build a generic arbitrary-command receipt wrapper | **Reject** | Rejected in R14 as a second format and generic execution surface (`round-14.md:46-51`). | Repeated header failures after V1-1 and V1-2 are applied. |
| V1-6 | State the scoping sentence: derived-target mutation evidence ≠ standalone full-gate receipt | **Admit** (part of V1-1) | Verifier's exact boundary; no new measurement claimed. | Any measured full-gate run that makes the derived-target limit moot — then update the sentence, not the history. |

## Part C — Ordered steps for the L1 owner (not performed by this seat)

1. **S007 superseding row first.** The current `teaches` cell says "debug-events/record/replay visualize and replay kernel
   input events". The opened page says `debug-events` prints **libinput-processed** events; only `record`/`replay` use kernel
   events. Correct by appending a `supersedes S007 —` row (the `teaches` cell cannot change in place). Anchor: the page with its
   version (libinput 1.32.0). Then promote to `mined` via in-place `status`/`used-by` only, logged old→new.
2. Only then write a U6 knowledge note with `source:` citing the new mined row and `covers: U6`, stating each rung's layer and root requirement, with no host observation claim.
3. Update the U6 scout ledger line (libinput/wayland-info now present, 1.32.0 / 1.3.0-1).
4. R14-V1: append the V1-1 correction and V1-6 sentence to the R14 lesson/evidence index; no QUALITY change.

## Outside spot-check — pending

Blank for the outside reviewer to fill: for each row above, `agree` / `disagree` plus reason.
Until that is done, U6 is not admitted and R14-V1 is not closed. No `[x]` clearance is claimed from this seat.

| Row | Outside decision | Agree/disagree | Reason |
|---|---|---|---|
| U6-1 | pending | pending | pending |
| U6-2 | pending | pending | pending |
| U6-3 | pending | pending | pending |
| V1-1 | pending | pending | pending |
| V1-2 | pending | pending | pending |

## Limits

- Documentation-only; no host tool was executed for U6 evidence.
- The derived target `cd1d73d7…` and kill counts are cited from the verifier and receipts, not recomputed here.
- Sample size is the 8 U6 and 6 R14-V1 candidates named above; not a full inventory of the input stack.

## Changed files

This report only: `.ufo/waves/round-15/w1/reports/GateDecisions.md`.
