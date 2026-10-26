# RevW2Counters — round-45 v2 counters: undeclared holes (round 46 w1, 2026-10-26)

Scope: `quality/counters/c1-r45-monitors-v2.py` and `quality/counters/c2-r45-monitor-entry-v2.py` against the declared
residuals in `.ufo/waves/round-45/registration-v2.md`, checked against the landed bytes at
`4d22eeb66c2835af8aaa3fac6ad838fa616aa663`. Every demonstration is a scratch clone of that tip
(`/fast/scratch/hyaku/mado-r46/RevW2Counters/clone`, `git rev-parse --show-toplevel` asserted equal to the clone before
each commit; scratch deleted after the receipts were copied). Baseline: the pristine tip scores
`PRED-C2-r45-v2: admitted=1/1 verdict=TARGET_MET` exit 0 (`receipts/baseline-c2.txt`), so each demo differs from a
passing state only by the forgery.

## F1 (C2, demonstrated) — a new id's Gate receipt need not be a pin; the docstring says it must

- Declared: `c2-r45-monitor-entry-v2.py:34` — "a new id's receipt must be one of PINS".
- Code: `:548-550` `pin_ok = PINS.get(os.path.basename(path)) in (None, digest) and (os.path.basename(path) not in PINS
  or path == FETCH + os.path.basename(path))` — a basename absent from PINS yields `PINS.get(...) = None`, which is in
  `(None, digest)`, so any ≥256-byte 100644 file under `.ufo/waves/round-45/fetch/` passes with a self-declared sha256.
  No later clause requires pin membership for new ids: clause e (`:582-614`) only binds the location URL of pin-gated
  ids, and clause i (`:678`) only requires every pin to be used by some gate.
- Demonstration (clone commit `1de0bb53d336eebf952710edaddc1d51c6547cf2`): new row S316 (`corpus/SOURCES.md:265`),
  receipt `.ufo/waves/round-45/fetch/notes-monitor-r45.md` (342 B, authored inside the scored commit, never fetched,
  sha256 `56c84edae21f419e47e3c628d0142eab89bcd0117366c8b482abddc6d8ff0346`), Gate line
  (`corpus/lessons/round-45.md:30`), entry source line (`…r45.md:17`) and body line (`:93`), README Sources cell widened
  to `S302-S316`. Counter: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1`, `verdict=TARGET_MET`, exit 0
  (`receipts/demo1-c2.txt`; `clause=d id=S316 gates=1 bound=1`, `clause=g id=S316 obs=1 locator_line=6`). A completely
  fabricated source with a self-chosen quote is admitted as a mined row.
- Propagates to the current round: `quality/counters/c2-r46-input-device-entry.py:28` (same docstring sentence) vs
  `:532-533` (same `pin_ok`).

## F2 (C2, demonstrated) — T4 binds verdict tokens to receipts the scored commit itself authors

- T4 (`c2-r45-monitor-entry-v2.py:689-699`) resolves any `\.ufo/waves/round-\d+/receipts/[A-Za-z0-9._-]+` path at REV
  and requires the tokens in it. Unlike the `fetch/` pins there is no sha256, no freeze-existence and no authorship
  requirement for a cited `receipts/` file — the committer can add one in the same commit.
- Demonstration (clone commit `738b5f834a45b199e6410ee497741f05d21fa1d9`, on top of F1's): 
  `.ufo/waves/round-45/receipts/forged-second-output.txt` (contains AGREE / DIFFER / NOT_COMPARED) plus entry line
  `…r45.md:101` claiming a second output (HDMI-A-1) was attached for a recheck run with DIFFER on mode and
  NOT_COMPARED overall — an experiment that never happened, beside the real §6 line that cites the genuine
  `live-monitors-host-l1.txt`. Counter: `admitted=1/1 verdict=TARGET_MET` exit 0 (`receipts/demo2-c2.txt`).
- Framing: the declared residual "a decision table naming no id is not bound" covers lines the counter does not bind at
  all; this demo shows the line the counter DOES bind (T4, the v2 fix for the RECEIPT-CONTRADICT class) binds to bytes
  the same commit controls, so the binding is vacuous for a forging committer.

## F3 (C1, demonstrated) — clause i's sandbox leaves the host runtime dir and AF_UNIX reachable

- Declared isolation (`c1-r45-monitors-v2.py:29-30`): "pid and net namespaces, the repository, the counter's lane and
  its parent hidden". Code `:290-295`: `--ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net
  --die-with-parent`, tmpfs over repo/lane/fleet, writable bind of the marker dir only.
- Probe under the exact profile (no tmpfs paths touched, listing only): `/run/user/1000/hypr` visible with 1 instance
  directory, its `.socket.sock` path statable; the lane correctly hidden (`receipts/probe-bwrap-run-dir.txt`).
  `--unshare-net` cuts IP networking only; AF_UNIX sockets traverse the ro-bind of `/`.
- Demonstration (clone commit `64e41df42cd36e5e313e604acde57edcfea4491d`): cheat tool = the landed
  `tools/mado-monitors.py` bytes plus a silent hook that lists `/run/user/<uid>/hypr` and writes evidence into the
  shared marker dir (the one writable path all runs share). Counter run (`--nonce 46`): `fixtures=81/81
  generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` exit 0 (`receipts/demo3-c1.txt`), with
  mid-run evidence "saw 1 instance dirs at /run/user/1000/hypr" captured while the counter was running. The counter's
  only telemetry — stdout, stderr, exit code, marker existence (`:405`) — cannot observe the probe.
- Payoff is isolation, not verdict fraud: fixture/generated answers come from the counter's own files, so seeing the
  host does not help match the model. But clause i asserts isolation and the residual list declares only that the TOOL
  may detect the sandbox — not that the sandbox leaks the live session to the tool. The socket itself was never
  connected to (host safety): the demo shows path reachability, not a session touch.

## Checked and found covered by the declared residuals (no demo)

- Seed-45 answer tables, environment gates, scorer-oracle `/proc` reads: the nonce fixture run, env-B variation and
  `--unshare-pid` hold (re-derived from the code; the v1 cheats' fixes stand).
- Implementing the contract only on the fixtures ∪ `gen_case` distribution and lying elsewhere: declared residual 1 of
  C1 ("a tool holding a model of the contract is an implementation of it").
- Canned selftest line: declared ("clause s is a printed line, not capability evidence").
- Clause r PATH-only: declared. A tool could also invoke a fake bin and then unlink the marker (`:405` checks
  `os.path.exists` once, at the end) — payoff-less (the fake bins print nothing and exit 0), noted, not demonstrated.
- C2 census T1 catches token-form contradictions only — declared ("contradicted in words rather than tokens").
- C2 clause c held rows: `recheck_ok(cells[9]) is not None` is vacuous (a bool is never None) — dead check; the live
  `recheck_ok(cells[9])` on the preceding line already covers it. No exploit beyond that.

## Verification gaps

- F3's socket-connect payoff was not exercised (host safety); reachability only.
- The C1 baseline on the pristine tip was not re-run; the landed tool's admission is recorded in round-45 receipts, and
  demo 3 differs from those bytes only by the probe hook.

Receipts: `receipts/baseline-c2.txt`, `receipts/demo1-c2.txt`, `receipts/demo2-c2.txt`, `receipts/demo3-c1.txt`,
`receipts/probe-bwrap-run-dir.txt` (paths relative to this seat dir). Tooling installed: none.
