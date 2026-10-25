# CritSeparability — mado round 37 wave 1 (critic)

Seat: `L1Mado37-2.CritSeparability`. Assignment: `w1/prompts/CritSeparability.md`. Lane HEAD read: `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b` (freeze `893a8aa`, base `b4e47e9`).
Writes: this report, plus scratch under `w1/scratch/CritSeparability/` (`ref-eventq.py`, `probe.py`, `separability-check.py`, `probe-out.txt`, `probe-out-2.txt`). Sandboxes were under `/dev/shm/mado37-CritSeparability/` and `/dev/shm/mado37-sepcheck-*`, and all were removed. Lane files: read only. Host: no `ss` run, no socket opened, no `hyprctl` call. Tools installed: none.

## Verdict

**SEPARABLE as frozen and as built.** Both claims were measured with the other side's files deleted, and in both directions neither verdict moved. **One coupling channel is unenforced**: the C1 counter accepts a Gate receipt at *any* committed path, so if E2 cites C2's live receipt or the tool, C1 loses 2/2 when C2's files are deleted. This was demonstrated. The registration's separability paragraph is enforced only by the ScribeE2 prompt, not by `PRED-C1-r37-v2`.

**E2 §5 ("the socket table is the route") is verified by neither counter.** In the current draft it is uncited INF, which keeps it separable. But it is not verifiable on this host without a live `ss` observation, and the only one planned is C2's receipt. Two of its load-bearing lines also depend on facts that the draft's own `## Unknowns` list as unknown.

Fixable defects, not a tradeoff the judge must reject.

## 1. Can either claim be measured with the other's files deleted? — PASS (both directions)

What each counter reads (from the code, not the registration):

- C1 (`quality/counters/c1-r37-event-ground.py`):
  - `corpus/knowledge/*` at BASE (precondition, :102-109).
  - The two targets, `corpus/SOURCES.md`, `corpus/lessons/round-37.md` and `corpus/README.md` at REV (:111-121, :126).
  - **Whatever path each Gate line's `receipt=` names** (:145, `show(repo, rev, rpath, binary=True)`). `GATE_RE` (:48) takes `receipt=(\S+)`, and nothing checks that the path is under `fetch/`.
- C2 (`quality/counters/c2-r37-eventq.py`): reads only `tools/mado-eventq.py` (:139), `.ufo/waves/round-37/receipts/eventq-live.txt` (:153) and `eventq-live-ss.txt` (:154). Fixtures are embedded (:67-98). The tool runs from a temp dir (:140-148, `cwd=d` :118), so a relative read of `corpus/` cannot resolve.

Probe: `cd …/w1/scratch/CritSeparability && python3 -I probe.py` (output in `probe-out.txt` and `probe-out-2.txt`).
- Each tree is a `git clone --no-local` of the lane at HEAD with sandbox identity.
- C1 side: the frozen `controls.py` `wire()` (the `c1-golden-v2` builder).
- C2 side: a 110-line scratch reference tool, plus a **synthetic** receipt and snapshot built from the counter's own `CLEAN_SS` fixture. This gives C2 an accept path; the registration has none ("C2's accept half is the deliverable itself", registration.md:82).

| tree | C1 | C2 |
|---|---|---|
| base-head | `admitted=0/2 verdict=TARGET_MISSED` | `fixtures=0/10 readonly=0 live=0 tool=absent verdict=TARGET_MISSED` |
| joint | `admitted=2/2 verdict=TARGET_MET` | `fixtures=10/10 readonly=1 live=1 tool=present verdict=TARGET_MET` |
| joint-minus-c2 (tool + both live receipts deleted) | `admitted=2/2 verdict=TARGET_MET` | `fixtures=0/10 … verdict=TARGET_MISSED` |
| joint-minus-c1 (corpus/ restored to pre-wire) | `admitted=0/2 verdict=TARGET_MISSED` | `fixtures=10/10 readonly=1 live=1 … TARGET_MET` |
| joint-no-corpus (all of `corpus/` deleted) | `admitted=0/2` | `fixtures=10/10 readonly=1 live=1 … TARGET_MET` |
| joint-no-tools-no-receipts (`tools/` + `round-37/receipts/` deleted) | `admitted=2/2 verdict=TARGET_MET` | `tool=absent … TARGET_MISSED` |
| joint-no-fetch (`round-37/fetch/` deleted) | `admitted=0/2` (`d=0 f=0 g=0` on both entries) | `fixtures=10/10 readonly=1 live=1 … TARGET_MET` |

`fetch/` belongs to C1 alone. C2 is indifferent to it and to all of `corpus/`.

## 2. Counterexample: C1 can be made to depend on C2 — FINDING (coupling channel, unenforced)

Trees `coupled-live` and `coupled-tool` are the joint tree plus one extra E2 citation, S215:
- a `source:` id, an `**OBS** S215` line, an 11-cell `mined` registry row used by E2, and
- a Gate line whose receipt is a C2 artifact: `receipts/eventq-live.txt` with quote `comm=waybar pid=935660 fd=21`, or `tools/mado-eventq.py` with quote `never opens any socket`.

```
tree=coupled-live counter=C1 rc=0 :: PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET
    … entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S213,S214,S215 ok=1
tree=coupled-live-minus-c2 counter=C1 rc=1 :: PRED-C1-r37-v2 admitted=1/2 verdict=TARGET_MISSED
    … entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=0 e=1 f=1 g=0 ids=S213,S214,S215 ok=0
tree=coupled-tool counter=C1 rc=0 :: … admitted=2/2 verdict=TARGET_MET
tree=coupled-tool-minus-c2 counter=C1 rc=1 :: … admitted=1/2 verdict=TARGET_MISSED   (same d=0 g=0)
```

The registration's sentence at registration.md:70-73 ("No C1 entry cites the tool or its receipt … Each is measurable with the other's files deleted") is true of the plan. The counter does not enforce it.

The pull toward coupling is real:
- E2's tokens `debug:disable_logs` and `m_logsEnabled` both occur in S214 (Logger.cpp:42, :48).
- The tool's live default runs `hyprctl getoption debug:disable_logs -j` (registration.md:54; ExecEventqA.md:7), so its source will contain one E2 token.
- The tool's live receipt is a fresher host reading of the same fact as S213:28.

A tidy-minded integrator citing "the new receipt" in E2 couples the claims. Then C1's verdict rides on C2's artifact, and one bad tool commit fails both claims.

Impacted axes: coverage (C1's verdict would ride on an operability artifact) and the separability statement's provenance (claimed in prose, not enforced by the predicate).

## 3. Same surface on two axes, one claim in disguise? — NOT one claim; a duplicate *proposition* (finding)

**No single act satisfies both.** The file sets are disjoint (table above). C1 needs:
- two entries,
- registry rows,
- lesson Gate lines with sha-bound receipts and verbatim quotes, and
- coverage-map rows.

C2 needs a program that passes ten discriminating fixtures. C1 measures provenance-grounded knowledge; C2 measures a working capability. These are different deliverables.

**The overlap is in the propositions:**

- E2's title (draft line 8, and the ScribeE2 prompt) asserts "the socket table is the observation route". That is exactly C2's premise: the tool *is* that route, and the registration's theme line names both halves, registration.md:22-24. If both are admitted, the lane carries one proposition twice: a coverage entry *asserting* it, and an operability row *embodying* it. Only C2 does any work toward it.
- The null-channel finding is encoded on both sides:
  - E2 §2 states it.
  - C2's `logs-disabled` fixture (c2:91-92) and the `markers_observable` field freeze the same belief.
  - C2's fixture `LOG` (c2:61-62: 21 core lines, then aquamarine) is shaped after S213:12-17.
  
  This is shared provenance frozen inside the counter, not a runtime read. Errors are correlated: if the S214 reading were wrong, both deliverables would carry the error and neither counter could detect it. Risk is low here, because S214:15-16 returns before any level test.

Because registration.md:100 claims no axis score change, double credit is limited to the scorecard capability row and the coverage-map row. Smallest correction: the title states only C1's ground (the logs cannot show it). "The socket table is the route" stays C2's sentence.

## 4. Would E2 §5 be unverifiable without the tool? — YES on this host; separable only because §5 is uncited INF (finding)

The draft `w1/scratch/ScribeE2/event-queue-observability-r37.md` §5 (lines 50-57) is all **INF**. Its bases are `ss(8)`, S189:137-150, :169-180 and :119-124. It cites no tool and no receipt, so it is formally separable. I checked every source E2 may cite:
- **No frozen receipt contains socket-table data.** S213 mentions sockets only as marker counts (`log_count "Socket2 fd": 0`, S213:11 and :24). S214 is the logger. S189 is compositor source.
- **`ss(8)` is not a registered source.** It is in none of the draft's `source:` lines 1-3, and it is not under `fetch/`.

§5's own premises are in its Unknowns:

| §5 line (INF) | Contradicting Unknown in the same draft |
|---|---|
| :53 "its Recv-Q (bytes queued, not yet read)" | :63 "**UNK** Whether ss's Recv-Q/Send-Q on a unix stream socket count exactly the unread bytes on each end" |
| :57 "A previously listed subscriber whose row is gone is the table-side trace of a removal" | :64 "**UNK** Whether `SClient` removal closes the client's descriptor … or leaves the row in the table" |

The sibling report `w1/reports/ScoutS189.md:53` also gives fd close on removal only as "[INFERENCE]: hyprutils RAII, not in these bytes".

From S189 (lines quoted via `sed -n '110,192p' fetch/S189.bin`):
- Overflow is a userspace event. `if (QUEUESIZE >= MAX_QUEUED_EVENTS) {` → log → `it = removeClientByFD(it->fd.get());` (:174-176).
- The queue grows only after `write` hits a full socket: `if (WRITTEN < 0 && (errno == EAGAIN || errno == EWOULDBLOCK))` / `return true;` (:149-150).

So at best the table shows the precursor (kernel backlog) and the aftermath (absence). Removal by overflow, removal after a write failure (:155) and an ordinary hang-up (:100) all look the same from the table. Draft :55 and :57 concede this correctly. The title and §5's heading ("The route that does work") overclaim against those lines.

Neither counter checks §5:
- C1 clause g checks only per-S-id quotes and an OBS line (c1:21-24, :150-152).
- C2's live clause checks that receipt and snapshot are consistent (c2:173-176), not what Recv-Q means or whether removal is visible.

The only planned host evidence for §5 is C2's live receipt and snapshot. Citing it couples the claims (§2 above).

## 5. Shared artifacts — named

1. **`.ufo/waves/round-37/receipts/` namespace.** C2's two live files live there. The C1 counter will bind any committed path as a Gate receipt (§2, demonstrated). This is latent, not present.
2. **A raw `ss -xpa` snapshot (latent).** ScoutSsSemantics (live `ss -xpa | grep -F .socket2.sock`), ExecProcCrosscheck (compare with `ss -xpa`), SentEventqSafety (`--snapshot-out`) and C2's `eventq-live-ss.txt` all produce the same kind of bytes. Two outcomes couple the claims:
   - one file serves as both an E2 S-id receipt and `LIVE_SS`, or
   - byte-identical copies count one observation on two axes.
3. **The host channels behind S213.** The tool's live defaults reread the same session log, the same unit-journal command (S213:20 equals registration.md:54) and the same `getoption`. It is the same observation surface, but no file is shared and nothing is read at count time.
4. **S213-shaped fixture constants inside C2** (c2:61-63). These are frozen copies, not a dependency.
5. **Harness only.** `controls.py` scores both claims and both are counted at one REV. Neither is a counted artifact.

## 6. Side finding passed to the C2 critic seat

The synthetic receipt and snapshot (fixture `CLEAN_SS`, labeled `# SYNTHETIC sandbox receipt`) reached `live=1`. The v2 replay proves the receipt matches the snapshot, not that the snapshot came from this host. I sent this to `L1Mado37-2.CritC2Cheap`. It does not affect separability.

## Smallest safe corrections (counters are frozen; none edits them)

1. **At admission, run the deletion check at the measured tip.** Script: `python3 -I .ufo/waves/round-37/w1/scratch/CritSeparability/separability-check.py --rev <tip>`.
   - It deletes C2's three files, then C1's two entries and the lesson, in a `/dev/shm` clone, and re-scores both counters.
   - It lists any Gate `receipt=` outside `.ufo/waves/round-37/fetch/`.
   - It prints `verdict=SEPARABLE|COUPLED`, exit 0 or 1.
   - At lane HEAD it ran: `SEPCHECK rev=80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b c1_moves_without_c2=0 c2_moves_without_c1=0 gate_receipts_outside_fetch=- verdict=SEPARABLE`, exit 0. This is trivial at HEAD, because both claims are at their before state.
   
   This check is a judge-side gate, not a new predicate.
2. **E2 must not cite the tool, its receipts, or any `ss` snapshot that also serves as `LIVE_SS`.** If §5 needs grounding, give it its own `fetch/` S-id whose bytes are documentation or kernel source on unix `sock_diag` queue semantics (the ScoutSsSemantics output). It must never be a host snapshot shared with C2.
3. **E2 title and §5 heading.** Drop "and the socket table is the observation route" from the title. Retitle §5 from "The route that does work" to something like "What the socket table can show: precursor and absence, not the overflow".
4. **Downgrade §5 :53 and :57 from INF to UNK, or ground them as in correction 2.** They currently assert what the draft's Unknowns :63 and :64 say is unknown.

## Addendum — CritC2Cheap's results (received 12:20 UTC, not re-run here)

CritC2Cheap reports two degenerate tools that reach `TARGET_MET` under the unedited v2 counter: a comm-name crib with a fake snapshot, and a fixture-hash memorizer. It also reports that the readonly clause is evaded by `connect_ex(`, `__import__` and shelling out to socat. These findings concern C2's cheapness, not separability. None of them adds a C1 file to what C2 reads, so the verdict above stands.

Its two candidate kills would each change what C2 reads, and each stays separable only if one condition holds:
- **Held-out fixtures generated at score time:** separable only if the generator takes nothing from `corpus/` or `fetch/`. If it derived log shapes from S213 or E2, deleting C1's files would move C2.
- **Score-time host check** (`ss -xpa`, `/proc/net/unix`, `/proc/<pid>/comm`): this reads the host, not lane files, so it stays separable. It does add a second live read of the same surface that E2 §5 describes. If E2 then cited that check's output, the coupling channel in §2 would reopen.

Under either v3, rerun `separability-check.py` at the measured tip.

## Commands run (all read-only on the lane)

- Reads: `registration.md`, both counters, `controls.py`, `receipts/controls-v2.txt`, `fetch/S213.receipt.txt`, `sed -n '110,192p' fetch/S189.bin`, `cat -n fetch/S214.bin`, the ScribeE1, ScribeE2 and ConnOverlap prompts, a grep of all w1 prompts for `eventq-live|S215|socket table|ss -xpa|fetch/`, the ScribeE2 draft, and `w1/reports/ScoutS189.md`.
- `python3 -I probe.py` and `python3 -I probe.py joint-minus-c1 joint-no-corpus joint-no-tools-no-receipts joint-no-fetch coupled-live coupled-live-minus-c2 coupled-tool coupled-tool-minus-c2`.
  - The first run stopped after three trees: `OSError: [Errno 122] Disk quota exceeded` on the shared `/dev/shm` (5.3G/8.0G in use).
  - Each 216M clone is now deleted right after it is scored, and the rerun completed.
- `python3 -I separability-check.py --rev 80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`, exit 0. Zero `mado37-sepcheck` dirs were left in `/dev/shm`.
