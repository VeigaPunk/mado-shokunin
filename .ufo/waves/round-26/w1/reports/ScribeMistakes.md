# Round 26 w1 — Mistakes candidates

These are candidate lesson rows for the L1 to use; this report does not edit the lesson. Evidence read: round-25 `c1/count.py` lines 30–47 and 124–189; round-26 registration lines 8–31; `harness/pilot-receipt.txt`; and `corpus/lessons/round-25-verifier-spotcheck.md`.

## Candidate rows

| id · class · evidence pointer · captured-by · fix |
|---|---|
| **M26-1 · host-safety boundary failure ·** round-25 `.ufo/waves/round-25/c1/count.py:30–47,124–138` documents nested Hyprland on the live Wayland session; the oracle copies inherited `XDG_RUNTIME_DIR` and `WAYLAND_DISPLAY` into its environment and starts Hyprland. The round-25 verifier spot-check `corpus/lessons/round-25-verifier-spotcheck.md:9–10` explicitly declined to run that counter because it starts nested Hyprland on the live session. Round-26 registration `.ufo/waves/round-26/registration.md:10–13` records windows on the desktop and about 1,330 `/usr/bin/Hyprland` coredump entries in the preceding 12 hours. Current bounded query below returned 1,335 records, with listed endpoints 2026-10-23 03:45:48 through 05:27:47 -03. · **captured-by:** none — round 25 had no isolation requirement or gate preventing a live-session oracle; the verifier's safety refusal was not a counter gate. · **fix:** run every nested instance only with a private display/runtime and cleared environment, and block measurement unless isolation is established. Show the gate can fail using a disposable test compositor and a legacy/injected-display negative control; show the isolated path cannot reach that display and has zero host-session/coredump delta after cleanup. |
| **M26-2 · pilot failure accounting / containment ·** round-26 `harness/pilot-receipt.txt:3–8,10–18` reports the pilot-period count change `1330 -> 1335`; its successful final method reports `1335 -> 1335`, `delta_coredumps=0`, and `PILOT ISOLATED_OK`. Registration `.ufo/waves/round-26/registration.md:27–31` also reports 1,330→1,335 before the final method. However, attribution is internally inconsistent: the pilot receipt says **“each aborted and added one Hyprland coredump record, 1330 -> 1335”**, while its item 5 says **“answered binds -j and animations -j; exited on dispatch exit; coredumps 1335 -> 1335”**; registration says **“The four failed pilot runs before it … each aborted and added one record (1330 → 1335)”**. The current count query corroborates 1,335 total, not which attempts account for the five-record delta. Thus the supported finding is that the pilot period recorded +5 before the successful method's stable count; the claim that five *failed* pilots caused those records is not reconciled by the itemized evidence. · **captured-by:** partial — the round-26 host-safety rule and final before/after receipt expose the aggregate delta, but there is no per-attempt coredump/exit ledger that reconciles it. · **fix:** record each pilot's process identity, outcome, and coredump count immediately before/after cleanup; require per-attempt deltas to sum to the round total. Demonstrate the accounting gate in a disposable environment with one known abort (expected +1) and one successful run (expected 0); it must fail if the records or outcomes are omitted/misattributed. |
| **M26-3 · evidence/report drift during review (historical precedent, not a new round-26 incident) ·** `corpus/lessons/round-25-verifier-spotcheck.md:128–131` says the M25-5 receipt sentence was false both initially and after an edit while the lane reviewer was reading; the errata was appended before closure. · **captured-by:** none — the spot-check caught the drift manually; no gate bound the reviewed statement to immutable evidence. · **fix:** bind report claims to a frozen receipt/hash and keep corrections append-only. Demonstrate failure with a scratch review where the cited receipt is changed after review starts: the claim verifier must reject the stale hash, then accept the appended correction with the new hash. |
| **M26-4 · claiming a repair without the artifact (historical precedent, not a new round-26 incident) ·** `corpus/lessons/round-25-verifier-spotcheck.md:135–141,207–208` reports that round-25 `registration.md:85` claimed MutCheckRegOrder/MutCheckReceipt had been hardened, but `round-25/quality/` held only the Q36 checker and outputs; the lesson/report said those survivors remained open. · **captured-by:** none — no artifact-to-claim check caught the registration statement; the non-author spot-check routed it. · **fix:** require each “landed/hardened” repair statement to cite its artifact and observed red/green result. Demonstrate failure in a scratch tree by removing the named checker or result and requiring the claim gate to fail; restore both and require it to pass. |

## Commands and observed outputs

The coredump count command was run with a timeout and address-space cap:

```text
timeout 90 prlimit --as=4000000000 -- coredumpctl list --no-pager | grep -c /usr/bin/Hyprland
1335
```

For the time-range endpoints, the same bounded `coredumpctl list --no-pager --no-legend | grep /usr/bin/Hyprland` stream was read from first to last matching record:

```text
first=Fri 2026-10-23 03:45:48 -03 3256486 1000 1000 SIGABRT none    /usr/bin/Hyprland                                                                                               -
last=Fri 2026-10-23 05:27:47 -03 1331155 1000 1000 SIGABRT none    /usr/bin/Hyprland                                                                                               -
```

The 1,335 is the count observed when queried; round-26 registration and the pilot receipt give 1,330 as the pre-pilot baseline. The first/last lines are the endpoints returned by the list command; no individual pilot-to-PID mapping was established here.

## Behavior, gates, and scope

- **Behavior changed:** none. This is a scribe report only.
- **Gates exercised:** only the bounded, read-only coredump listing/count. No counter, pilot, harness, build, test, lint, or lesson check was run.
- **Touched surface:** `.ufo/waves/round-26/w1/reports/ScribeMistakes.md` (this report only).
- **Out of scope:** no product/harness/counter/lesson edits; no Hyprland or other process was started; no tools were installed. The exact attribution of all five pilot-period records remains unresolved by the evidence read.
- **Tool installs/updates:** none.

Report: `.ufo/waves/round-26/w1/reports/ScribeMistakes.md`
