# Round 37 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25

Fleet root: /home/vgpnk/Projects/shokunin. Lane repo: mado-shokunin
(branch `master`). Base `b4e47e980bfb0cbc8a4e788f59a41db858751fd8`, tip
`6542248266b58d41ccccf31564d436f59857336d`.

## 1. Conformance

- Report authorship: `git -C <fleet> log --format='%an %H' -- .ufo/reports/round-37/mado.md`
  → `mado-shokunin cdaa69d75e8f9a0fa66ed48b222b0e5ea625b361` and
  `mado-shokunin 691328444b7e9b1464869c9e1fbc5d7aa8c37a68`. Committed by the lane identity. OK.
- SHONEN heading: report carries `## SHONEN` with exactly one line per box (4 boxes,
  all `[~]` with resolvable pointers; no `[x]` without a non-author verifier). OK.
- Cited commits exist and are ancestors of `master` (merge-base --is-ancestor all pass):
  b4e47e9, 8f0a9e3, 893a8aa, 80b83c8, 3f42425, f6ae0c3, 372a3ef, 6542248.
- Lane state: `jj-lane.sh state` → `branch=master local=6542248… remote=6542248… ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; remote
  `ls-remote origin refs/heads/master` = `6542248…`. No uncommitted round work; pushed. OK.
- Prompt fidelity: `.ufo/prompts/mado-round-37.md` carries the canonical template contract
  verbatim (sections §1 MISSION/AXES binding, §2 claims, §2b frontier step, §3 L2 floor
  ≥8 in one batched swarm, §4 report contract incl. SHONEN heading, §5 commit-then-push,
  push scope, L0 side channel) plus the §6 hyaku addendum. No model alias hardcoded;
  routing goes through the host route table (MISSION.md bucket exists). OK.
- Dispatch/complete digest (from `.ufo/watchdog.log`, copied into notes):
  - 2026-10-25T06:05:39-03:00 launch mado round=37 pgid=1729662 attempt=1
  - 2026-10-25T06:46:34-03:00 lane-dead-no-report mado round=37; retry same round
  - 2026-10-25T08:50:16-03:00 launch mado round=37 pgid=819016 attempt=2
  - 2026-10-25T09:35:45-03:00 complete mado round=37; hyaku-inline attempt=2

## 2. Claims re-check (against tip `6542248…`)

Neither counter was executed (PROTOCOL §Gate standard, Closure consequence — verify a
sibling's committed evidence, never run its gate). Both claims were **evidence-verified**
and re-derived with plain measurements over committed bytes.

### C1 — coverage (0/2 → 2/2), evidence-verified

- Committed receipts: before-c1-v2.txt (`admitted=0/2 TARGET_MISSED`, exit 1, at base),
  after-c1-v2.txt (`admitted=2/2 TARGET_MET`, exit 0, at 3f42425), after-c1-v2-records.txt
  (re-run at f6ae0c3, 2/2). Controls v2 13/13 correct; v1 golden stub re-frozen as
  `c1-token-stub` → MISSED (Amendment 1).
- Plain re-derivation:
  - Base ground absent: `git grep -l 'MAX_QUEUED_EVENTS' b4e47e9 -- corpus/knowledge/`
    empty; same for `debug:disable_logs`.
  - Tip holds both entries: event-delivery-limits-r26.md and event-queue-observability-r37.md
    exist at tip; README index rows present for both (lines 62–63).
  - Clause g satisfied by inspection: each entry body carries its located Gate quotes
    verbatim (e.g. `const size_t MAX_QUEUED_EVENTS = 64;`; `debug:disable_logs: {"option":
    "debug:disable_logs","int":1,"set":false}`; `MS<Bool>("debug:disable_logs", ..., true),`;
    `if (!m_logsEnabled)`) with `**OBS**` lines naming the S-id.
  - SOURCES: rows 201 → 207 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}...'`); S212–S217
    added, tier A, `mined`; S189/S201 `used-by` extended. sources-census validate exit 0,
    same seven W04, no malformed rows, no duplicate ids, no missing used-by paths.
  - Upstream re-open (this closure): all six code sources re-fetched byte-identical to the
    committed fetch receipts — S189 eea605df…, S201 799bf02f…, S212 1e19d926…, S214
    d04e3a2…, S215 a76f0507…, S216 74833ecb…, S217 aeb07ba1…. Located claims verified:
    S189 :14 (nonblocking socket), :35 (listen 10), :73 (accept4), :128 (1024 truncation),
    :133/:149/:152/:155 (flushClient, EAGAIN/EWOULDBLOCK, EINTR, write-fail marker), :169
    (64 cap), :174-175 (overflow marker); S201 :105 (connect once), :115-117 (fgets 1023),
    :120/:136 (sleep loops); S212 :804-815 (twelve unconditional registrations), :821/:827
    (conditional windowtitlev2/activewindowv2); S214 :15-16/:21-22/:47/:48; S215 :629/:632;
    S216 :298/:304-307; S217 :22-24/:42.
- Verdict: C1 **verifies** (2/2 target met; content grounded in re-opened bytes). Instrument
  limit named by the lane and confirmed on the record: wave-1 `CritC1Cheap` reached the same
  target with a 19-line self-receipt crib, and no control exercises clause b (M37-5).

### C2 — operability capability acquisition (0/10 → 10/10), evidence-verified

- Committed receipts: before-c2-v2.txt (`fixtures=0/10 readonly=0 live=0 tool=absent
  TARGET_MISSED`, exit 1), after-c2-v2.txt (`fixtures=10/10 readonly=1 live=1 tool=present
  TARGET_MET`, exit 0, at 3f42425), after-c2-v2-records.txt (re-run at f6ae0c3).
- Plain re-derivation: `tools/mado-eventq.py` exists at tip; `sha256sum` =
  `436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24` = the `tool_sha256`
  in the committed live receipt. Tool docstring documents read-only operation (kernel unix
  socket table; never connects).
- Live receipt (eventq-live.txt, taken 09:19): two subscribers — waybar pid 935660 fd 21,
  socat pid 2293 fd 5 — 0 markers, `markers_observable=no`, `verdict=CLEAN`; independent
  committed `/proc` census (eventq-live-proc-crosscheck.txt) agrees on the same two server
  inodes (`OVERALL: AGREE`).
- Verdict: C2 **verifies** (10/10 fixtures; live receipt corroborated independently).
  Instrument limit named: `RevC2Code` F1 showed the live clause reachable with a snapshot
  built from the counter's own fixture rows; `lagging`/`--expect-client` lack a
  discriminating case (M37-5).

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | **improved** | C1 verified 0/2 → 2/2 on a new edge class (stalled-client delivery + host observability), sourced on rows opened this round; no axis score reduced |
| operability | **improved** | C2 verified: runnable read-only tool, 10/10 fixtures, live receipt + independent proc agreement |
| calibration | **unchanged** | Axis score 50/50 at records tip (axis-records.txt, MATCH); no calibration claim this round |
| freshness / depth / adjacency | **unchanged** | Not claimed; adjacency routed, nothing absorbed |

No owned axis harmed: SCORECARD diff base→tip is additive (+53 lines, no removals);
`tools/mado-verify.sh` sha256 at tip `050efc72…6703f1` matches the pre-round claim and has
no diff across the round; zero deleted paths in `b4e47e9..6542248`; census identical.

## 4. Discernment spot-check (LEARNING.md — outside check)

Sampled from `corpus/lessons/round-37.md` `## Gate` (assimilation admit/reject + new rows).

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| Admit `event-delivery-limits-r26.md` (package entry re-grounded) | admit | Hyprland EventManager.cpp @ efb50993…; Waybar backend.cpp / workspaces.cpp @ 0.15.0 (all re-fetched, byte-identical) | agree | Located quotes verified at the cited lines (:169 cap, :175 overflow, :155 write-fail, :115-117 fgets 1023, :804-815 twelve registrations); the five corrections (1023-char split, buffer-full-first removal order, no compositor-side logging by default, producer thread) all match the bytes |
| Reject `event-queue-host-measurement-r28.md` | refuse | Logger.hpp :22-24; ConfigValues.cpp :629/:632; Logger.cpp :15-16/:47/:48; Compositor.cpp :298/:304-307; S213 host receipt | agree | `debug:disable_logs` defaults true and reads 1; the formatted log call returns before formatting; the zero is a null channel, not "never overflowed" |
| Reject `event-queue-journal-measurement-r29.md` | refuse | Logger.cpp :47-48; S213 host receipt | agree | stdout needs both switches; unit journal never carries core lines (probe 7× log vs 0× journal) |
| New SOURCES row S212 quote | opened | workspaces.cpp @ 0.15.0 | agree | `m_ipc.registerForIPC("workspacev2", this);` present at :804; quote ≤25 words |

All sampled decisions agree; the refusals' flip conditions (disable_logs=false + re-count)
are grounded in the verified bytes.

## 5. Trend verdicts

- **expansion: improved.** Two new admitted knowledge entries on ground unheld at base
  (`git grep` empty for `MAX_QUEUED_EVENTS`/`debug:disable_logs` in knowledge/ at base),
  each `source:` citing `mined` rows opened this round (S212–S217; S189/S201 re-opened);
  one capability row entered SCORECARD.
- **quality: improved.** A runnable domain tool lands (10/10 fixtures, independent /proc
  agreement); four gates stop trusting caller env (red→green, shown able to fail); the
  package entry is corrected in five places against re-fetched bytes; harm watch green
  (verify.sh unchanged, zero deletions, census identical); no admitted entry fails its
  re-check.
- **discernment: improved, with named limits.** Admit/reject verdicts agree with this
  outside spot-check; the L1 self-caught its v1 golden stub (M37-1) and a false frontier
  provenance (Erratum 1); the residual crib-reachability of both frozen counters (M37-5)
  is reported, not hidden, with a concrete v3 design routed to round 38.

## 6. Routed defects (lane must fix next round)

- **M37-5 (self-defect, keep on the routed-defect queue):** C1 counter remains crib-reachable
  (19-line self-receipt; no control exercises clause b; the refused r28 entry pasted verbatim
  also meets the target); C2 live clause remains reachable with a fixture-row snapshot, and
  `lagging`/`--expect-client` lack discriminating cases. Fix: bind every Gate receipt to
  `fetch/` and a re-fetch digest; cross-check a live snapshot against `/proc/net/unix`
  server inodes; add discriminating cases. Already planned by the lane for round 38 v3.
- No cross-domain defects were filed against sibling lanes this round (ConnOverlap: shared
  ground, nothing absorbed).
- SHONEN boxes remain `[~]` with historical pointers; promotion is operator-owned. The four
  boxes reference checkable historical artifacts (config-health-report-r3, province-accuracy-
  selfaudit, executor-test-sufficiency, SKILL.md tables); no fresh non-author promotion review
  was performed this round — flag for the operator, not a closure blocker.

## 7. Standing

Round 37 is admitted: both claims verify against the final lane hash; no axis is harmed;
trends are improved with the instrument limits named; conformance clean. The lane should
land the v3 counters (M37-5) in round 38.
