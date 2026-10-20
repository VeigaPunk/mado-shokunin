# Round 15 — input layer boundaries, receipt precision and a host-safety failure

Date: 2026-10-20. Baseline `ea0446fcb4840089f0e541d96350144506fb5d1d`.
Declared claim C1: coverage on the existing finite current-art rubric,
U1–U5 5/7 → U1–U6 6/7, one bounded documentation route. U7 and actual
input delivery remain unexercised. This round does **not** meet no-harm
admission: a seat performed a forbidden host partial upgrade. Landing the
reachable knowledge/correction work is not an attempt to admit that trade.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | standalone ancillary receipt precision / R14-V1 | Outside `round-14-verifier-spotcheck.md:169`; round-14 `evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt:3-4` | QUALITY 7, 9, 13; outside verifier caught incomplete commit re-binding | Preserve historical bytes. Append standing-use erratum and per-receipt derived-target mapping; provisional whole-gate hashes remain unbound, and pre-commit execution is not stamped as a later measured commit. The correction audit is recorded separately from any runtime regression proof. |
| M2 | host partial upgrade | `/var/log/pacman.log:2429-2437`; actor `MadoR15.LibinputEvents`, exact `sudo pacman -S --needed --noconfirm libinput libinput-tools`; actor's wave report and orchestrator ruling | Tooling directive **never run a partial upgrade**. The authorized installation channel does not override this restriction | Before any future install, `pacman -Sp --print-format '%n %v' <pkgs>` must list only not-already-installed packages, including dependencies. Any installed-name overlap goes to L0. QUALITY 20 and SKILL carry the guard. No further pacman operation, downgrade/revert or compositor restart in this round. The in-memory actual-plan control fails with `already_installed_in_plan`, exit 1, overlap libinput; a new-only control passes `new_only_plan`, exit 0. `.ufo/waves/round-15/evidence/install-guard-{red,green}.txt` contains the identical command and complete observed outputs. Green is only a fixture, not a permitted real transaction or remediation. |
| M3 | source-layer conflation and mutable anchor | S007 composite teaches cell groups debug-events/record/replay under kernel-event wording; primary S051 `libinput-debug-events` and `libinput-record` sections; GateDecisions/ReviewSourceTier | QUALITY 2, 3, 15, 16, 17 | S051 explicitly supersedes S007 with exact tagged primary source and distinct helper/default/context/kernel-recording/virtual-replay semantics. S007's immutable history remains queued, not cited for U6 credit. No duplicate unpinned latest-page admission. |

M2 is not marked resolved: the guard is demonstrated as able to refuse the
actual recorded package-name overlap, but it does not repair installed
host state or retroactively make this transaction conformant. Remediation
belongs to the operator via the orchestrator's L0 routing. No downgrade or
compositor restart is attempted. No new scored calibration claim is made.

### Tool transaction and process evidence

At 2026-10-20T04:25:16-0300 (07:25:16Z), LibinputEvents ran the command
above to inspect official debug-events man pages and static help. Official
Arch `extra` pacman transaction: **libinput 1.31.3-1 → 1.32.0-1**;
new **libinput-tools 1.32.0-1**, **python-libevdev 0.13.1-1**,
**python-pyudev 0.24.4-1**, **python-yaml 6.0.3-2**. Log lines 2438–2439
also show udev-reload/system-update hooks. The actor confirms only package
file listing, man-page/help/header/hash reads afterward; no device/event
reads, input replay or restart. The seat nevertheless violated the no-partial-
upgrade directive. The main orchestrator independently ruled it a partial
upgrade because the host is behind its sync database, not merely because
of a particular `-Sy` flag spelling.

Orchestrator evidence (not rerun by L1): soname stays libinput.so.10;
`ldd -r` reports 0 unresolved symbols and aquamarine links .so.10; the
running compositor retains its prior 1.31.3 mapping. These are limited
compatibility observations, **not** an end-to-end input test, no-harm
clearance or permission to restart. Several earlier wave reports have
pre-transaction version observations; their timestamps/limits are retained
as advisory history, not selected to erase drift.

ReviewLibinput also disclosed one read-only `hyprctl version` call despite
the wave's no-live-probe rule. Its result is not used as fresh round claim
evidence. Static package/help/docs/XML reads are not input event collection.
No seat is asked to repeat that call or to run a live input observer.

## Gate

### Candidate decisions

- **Admit locally as bounded knowledge:** `knowledge/input-debugging-boundaries-r15.md`.
  Primary S051 separates helper contexts/defaults, explicit debug options,
  context-independent kernel recording and virtual replay. S052 separates
  capability lifecycle, focus and keycode contract. Neither is a host
  feature measurement. Local knowledge admission is not whole-round admission.
- **Admit as correction, not expansion:** R14-V1 mapping/standing-use erratum.
  The historical target/green/restore observations remain derived-target
  evidence; old provisional whole-gate bytes are not recovered or relabeled.
- **Reject:** list-devices defaults equal the desktop's applied settings.
  Flip: independent correctly scoped compositor/applied-state evidence;
  equality of a sample alone does not establish the general claim.
- **Reject:** device inventory or a seat global proves client delivery or
  text insertion. Flip: authorized claim-specific client/application outcome;
  no such evidence is collected here.
- **Reject:** recording is anonymous by default, replay is a dry read, or
  lack of root/binary is a safety boundary. Flip: none under this lane's
  prohibition; docs/tool availability does not authorize capture/injection.
- **Reject as final source anchor:** mutable/composite S007, replaced by
  pinned S051. Existing S007 stays queued historical metadata, unchanged.
- **Reject:** full input/kernel/IME/Waybar mastery, successful event delivery,
  new repertoire capability, or current SHONEN clearance from authoring seats.
- **Reject:** the round is no-harm/admitted. M2 is an actual safety violation,
  even though C1 is structurally measurable and ABI checks show no unresolved
  symbols. Operator remediation is not silently treated as complete.

### Opened sources and located quotes

Access date **2026-10-20**. Parent opened the latest libinput HTML page,
then both exact raw tagged sources below and the installed core XML input
sections. Parent ran the two URL `curl -fsSL … | sha256sum` pipelines;
observed digests match the registry. Quotes below are each ≤25 words.

| row | exact source / revision / location | located quote | decision |
|---|---|---|---|
| S051 new | https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst ; tag 1.32.0, `libinput-list-devices` Note | “This tool does **not** show your desktop's configuration, just the libinput built-in defaults.” | mined by U6, supersedes S007; SHA-256 53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f |
| S052 new | https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml ; tag 1.26.0, `wl_keyboard.enter` description | “Notification that this seat's keyboard focus is on a certain surface.” | mined by U6; SHA-256 cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07 matches installed wayland 1.26.0-1 XML |
| S007 reopened, unchanged | https://wayland.freedesktop.org/libinput/doc/latest/tools.html ; title Helper tools — libinput 1.32.0 documentation, `libinput record and libinput replay` | “The recorded events are kernel events and independent of the libinput context.” | not the final anchor; S051 is the stronger scoped replacement |

S051 and S007 concern the same documentation family/scope: supersession is
explicit, not a silent duplicate. S052 reuses core XML but concerns the
input contract, while S043 concerns registry announcement/binding/removal;
this distinct-scope reuse is explicitly reviewed. No existing registry
status/recheck/used-by cell changes. Added rows: two A, zero B, zero C.
The search unit is three opened source locations, screened three,
included two stronger anchors, excluded one as final anchor. Failed
versioned libinput HTML access (404) is not a source row or a negative
claim about all documentation. Source census before/after receipts are
under `.ufo/waves/round-15/evidence/`.

### Structural versus semantic admission

The counter cannot detect a reversed safety sentence or turn a source
join into independent agreement. L1 manually checked the actual note:
separate prove/does-not-prove ladder cells; defaults not applied policy;
S041 excludes capability bits; XML v11 not advertised host v9; no typed
text claim; raw devices/observers/record/replay expressly not executed;
[UNK] affirmatively names unmeasured delivery/IME/kernel/application layers.
AttackMetric's structural-shell examples remain disclosed counter limits,
not reasons to infer an executed capability.

### Wave and outside check

One validated **64-seat** policy-v2 wave, one unchanged `taskCall` dispatch;
no second wave. Role mix: executor 3, scout 13, connector 8, reviewer 17,
critic 9, sentinel 4, revenger 4, scribe 4, mutation-tester 1, simplifier 1.
L1 holds the canonical planner seat; PlanningWalk provides the bounded data
walk. Registry/spec/dispatch and leaf reports are in
`.ufo/waves/round-15/w1/`. Wave reports are authoring-lane advice, not
non-author clearance; in-flight defects or suggested filenames are not
final corpus paths. Some reports suggest incompatible source ids, broad
implementation claims or unnecessary wrappers; final S051/S052 and actual
landed note govern. Non-author round-15 admit/reject spot-check remains
pending external closure; SHONEN stays four author assertions.

### Author trend judgment

Expansion: improved narrowly by one sourced U6 documentation-route entry.
Quality: **harmed** on host-operability safety because of M2, despite the
bounded stronger source/receipt corrections and unchanged gate.
Discernment: improved narrowly by learning outside R14-V1 and documenting
an actual newly caught safety mistake with a demonstrated guard; current
round's outside admit/reject agreement is not claimed. No-trade admission
is unmet; no subsequent round is opened here.

### Pre-measurement integration decisions

The initial wave reserved S051 libinput/S052 core XML. An interim proposal
to reuse S007 and call the XML S051 was rejected after source review found
S007's mutable anchor/composite layer wording. Final S051/S052 restored
the original mapping **before** either revision's numeric result was
used. The candidate `input-draft.txt` is retained wave advice, not a
second admitted knowledge path or a provenance authority over the corpus.
No historical registry row was rewritten to implement the reconciliation.

The latest HTML's 1.32.0 banner does not itself establish a git revision;
the actual tagged RST open and SHA-256 pipeline ground S051. Only the
specific 1.32.0 versioned HTML request failed, not every versioned tree.
The running compositor's old library is not re-verified by reading 1.32.0
source. Tag compatibility is not asserted. S052's final range includes the
complete cited pointer-button element through line 2265 (parent XML read).
The structural counter does not compare source URLs/hashes or detect
unmined co-citations automatically; L1's exact S051/S052 header/registry
check and the external spot-check remain separate admission duties.
