# R56W3ConnCrossSrc — cross-source inotify plane

Attacked: request/registration/observation conflation across S383, S390, queued S396/S397 and the authorized kernel source. Axes: coverage, operability, calibration (semantic boundaries; frozen C3 measures token-level back-reference consistency).

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ConnCrossSrc/receipts/crosssrc.md` — agreement/disagreement table, one Paths proposal, commands, outputs, risks and verification handoff.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ConnCrossSrc/receipts/kernel-inotify_user.c` — fetched supplementary source, 21756 bytes, sha256 `f5dd113ad7b7d457dc8453d29d240d6ffaf352d52a2ac8ad374cd703208e1ea0`.

## Findings

1. **Weakens a verification method, not a frozen predicate:** S397 pin line164 calls wd decimal; fixed-revision cached capture line18 contains `wd:1f`. Literal contradiction. Preserve raw tokens; decimal-only parsing is invalid for this capture. Shared with R56W3ScoutNewSrc2-2.
2. **Weakens an empirical assertion, not the entry:** `800afff` is the manual's example, not the cached compositor's mask. Read-only `git show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2RevProcFdinfo/fdinfo-capture.txt` plus the exact Python census in the receipt returned `80 ['8'] True False` (inotify lines, mask set, wd:1f present, mask:800afff present). Two fd blocks repeat one 40-watch instance according to the cached report; these are not eighty distinct watches.
3. **Weakens extrapolated field semantics:** ignored_mask:0 appears in inotify examples/capture, but S397's prose definition is under fanotify. S390 IN_IGNORED is a removal event, not that field. Authorized inotify_user.c token census: `ignored_mask: []`, `seq_printf: []`, `inotify_show_fdinfo: [358]`. Formatter semantics remain unverified, not silently borrowed from fanotify.
4. **Conditional cross-source gap [INFERENCE]:** a directory watch followed by a symlink-to-directory canonical add can reuse the wd and replace its wider mask with CLOSE_WRITE only; callback matching still selects the first stored path. S390:276-302 and kernel:536-568 establish replacement; S383:55-70,100-107 establishes add order and first match. No reproduction ran. This challenges generalizing path-count parity to event-mask/callback parity, not the frozen fixture predicate. Any new model/fixture requirement is routed to round57.

The existing entry line134 already distinguishes requested DONT_FOLLOW from observed mask8, so that boundary is **not a newly discovered defect**. No blocking-claim finding established here; no counter was re-scored.

## One bounded proposal

- Inotify plane: events, inode identity, add requests, then observation — S390 → S396 → S383 → S397: learn event/lookup flags and mask replacement, then per-instance inode identity, read Hyprland's ordered add calls, and only then interpret fdinfo without mistaking requests, registrations or manual examples for runtime events.

Proposal only; not applied. Coverage improves through study order; runtime, frozen predicates, counters and used-by cells remain unchanged. S396/S397 are queued draft IDs: integrate only when rows exist; do not treat this navigation line as a mined-status justification.

## What ran / did not run

Read frozen v2 claims and registration, v1 registration, current-round pins/draft/cached receipts, and git objects at the required revision. Hash comparisons established S383/S390 working pins equal fixed-revision blobs and both queued pins match their draft hashes. Exact commands and decisive output are in crosssrc.md. Initial kernel URL reader returned HTTP429; `curl -fSL --max-time 40 ... -o /fast/scratch/hyaku/mado-r56/R56W3ConnCrossSrc/inotify_user.c` succeeded rc0. Kernel master is not proven to match running kernel7.2.11.

No live /proc inspection, filesystem event, reload, claim counter, harness, test suite or alias-collision probe ran. Python data processing used the persistent evaluation tool, not a `python3 -I` CLI; that interpreter exception is explicitly recorded in the receipt. No lane code was imported/executed. No install/update, other agent/model invocation, clone, git mutation or tracked-file edit occurred. All seat writes are under the named deliverable paths; scratch was removed (`scratch_removed=True`).

Verification handoff: verify all four source IDs exist before applying the sole Paths line; preserve queued statuses and frozen files; independently inspect version-matched fdinfo formatting and test alias add-order only in an isolated scratch instance if round57 takes the inference forward.
