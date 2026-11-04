# R74ExecC1 — independent drive of claim C1's frozen counting command (round 74, wave 1)

Seat: R74ExecC1 (leaf executor). Scope: reproduce C1 end to end, reconcile against the
committed receipt, map each replay mode to the refusing clause of the committed rule, and probe
extra output shapes against the committed rule. Lane dir: `.ufo/waves/round-74/w1/R74ExecC1/`.
No tools were installed (none needed); no git/jj mutation was performed anywhere (the counter
itself only runs `git rev-parse`/`git show`); no lane/committed file was written.

## 1. Commands run (verbatim, from the repo root)

```
python3 -I quality/counters/c1-r74-replay-witness.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c1-replay-cases-r74.json --scratch-root /fast/scratch/hyaku/mado-r74/R74ExecC1/run
python3 -I quality/counters/c1-r74-replay-witness.py --selftest --scratch-root /fast/scratch/hyaku/mado-r74/R74ExecC1/run
python3 -I quality/counters/c1-r74-witness-rule.py --selftest --scratch-root /fast/scratch/hyaku/mado-r74/R74ExecC1/run
```

## 2. What actually happened

- Measurement: exit code **0**, last line
  `MADO_R74_REPLAY_WITNESS: cases=12 correct=12 base_correct=8 verdict=TARGET_MET rev=b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`.
  Full stdout retained at `R74ExecC1-run-output.txt` (this dir).
- Driver `--selftest`: exit 0, `MADO_R74_REPLAY_WITNESS_SELFTEST: 21/21 assertions passed`.
- Rule `--selftest`: exit 0, `MADO_R74_WITNESS_RULE_SELFTEST: 21/21 assertions passed`.

## 3. Reconciliation with `measurement-c1-r74.txt`

`diff -u` (retained at `R74ExecC1-reconcile-diff.txt`) shows exactly one differing line:

```
-MADO_R74_CHALLENGE nonce=f5497b8e9cd0f045 len=16
+MADO_R74_CHALLENGE nonce=050852b288592a17 len=16
```

Named differences — complete list:
1. The challenge nonce. Expected, not a defect: `measure()` draws it per run with
   `secrets.token_hex(8)` (re-drawn on collision with the frozen stale token
   `0123456789abcdef`), so two independent runs cannot share it. Length stays 16, lower hex.
Everything else is byte-identical: the controls path/sha (`17c9577404…74727c`), both revs, the
candidate rule digest (`6a6d77f4ad…394516`), the base harness digest
(`b6108c86e8…c45857d`), all twelve `MADO_R74_SCENARIO` lines including per-case rc (0/1/1/2/…
exactly as committed), and the contract line. Same last line, same rc (0). **No unexplained
difference.**

## 4. The four replay modes vs `credit(out, nonce)` — with per-case confirmation

`credit` (quality/counters/c1-r74-witness-rule.py) is a four-conjunct gate: (1) the LAST
fully-parsed `MADO_LANDING_COUNTERS_SELFTEST: p/n assertions passed` line must full-match;
(2) `n > 0` and `p < n`; (3) `SELFTEST FAIL <i>: ` lines number exactly `n - p`; (4) the LAST
parsed `MADO_LANDING_WITNESS: <16 hex>` token must equal the caller's nonce. All four replay
lanes satisfy (1)–(3) (each prints the round-72 genuine-failing shape `1/2` with exactly one
fail line), so in every case the refusing conjunct is (4):

- `replay-captured` — the lane prints the frozen stale witness `0123456789abcdef`; the token
  parses but is not this run's nonce → conjunct 4 refuses.
- `replay-no-witness` — no witness line at all; `last_witness` returns None, and
  `token is not None` fails → conjunct 4 refuses.
- `witness-mismatch` — the lane prints `deadbeefdeadbeef`; parses, wrong token → conjunct 4
  refuses.
- `witness-last-wins` — the lane echoes the true nonce and then `deadbeefdeadbeef`;
  `last_witness` scans forward and keeps the LAST parsed token, so the trailing wrong one wins
  → conjunct 4 refuses.

Per-case confirmation from my run's `MADO_R74_SCENARIO` lines (not the summary): all four show
`expect=fail candidate=fail base=pass correct=yes base_correct=no rc=1` — identical to the
committed receipt. The eight carried modes kept their frozen expectations
(`liar-success pass/rc=0`, `stderr-genuine pass/rc=1`, `liar-kill fail`, `crash-stderr fail/rc=2`,
`bare-failing fail`, `mismatch-detail fail`, `last-wins-pass fail`, `last-wins-fail pass`), and
`base_correct` is exactly 8 (the round-72 arithmetic-only rule credits all four replays:
`base=pass` on each). Frozen kill rule satisfied: cases=12, correct=12, base_correct=8.

Setup protections observed while reading the driver: `load_controls` enforces the frozen
controls sha256 and rejects wrong count/duplicate names/altered carried or replay
labels/wrong stale nonce; the lane fixture's ZCLAUSE must occur exactly once before deletion
(the harness's asserted single-site mutation); the scratch root refuses `/tmp`, `/var/tmp`,
`/dev/shm` and symlinked roots (both tools).

## 5. Extra-shape probes against the committed rule (runpy import; `R74ExecC1-probe-shapes.py`)

Probe driver imports the committed rule via `runpy.run_path` and calls
`credit(out, nonce)` with `nonce=f5497b8e9cd0f045` (the receipt's challenge, shape-only).
Raw output: `R74ExecC1-probe-output.txt`.

| Shape | Bytes sketch | credit | Frozen-predicate coverage |
|---|---|---|---|
| A: witness AFTER the summary | `FAIL` + `1/2` + `WITNESS: nonce` | **True** (credited) | Covered: the frozen sentence fixes which witness decides (last parsed) and that it equals the challenge, but orders it nowhere against the summary — a tail witness satisfies the predicate, and the rule credits. Control (witness before) also True. |
| A2: witness after a MALFORMED trailing marker | `FAIL` + `1/2` + `…SELFTEST: cleanup` + witness | **True** | Covered: the malformed marker is not a parseable summary (`last_parsed_summary` skips it), same predicate outcome as A. |
| B: witness on stderr only | stdout `FAIL`+`1/2`, stderr witness | **True** as the measurement feeds it (driver concatenates stdout+stderr before `credit` — the round-72 both-streams convention; the carried `stderr-genuine` mode depends on exactly this and passed in both runs) | Covered by the rule's documented input convention; refused (False) only when a single stream alone reaches `credit` (stdout-only → no witness; stderr-only → no summary). |
| C: two summaries, one witness | last summary green | `2/2` last → **False** (`p >= n`); | Covered: the predicate's "last parsed summary" clause governs; the single witness serves whichever summary is last. |
| C: … last summary failing | `2/2` then `FAIL` then `1/2` | **True** (credited) | Covered (arithmetic + witness both hold on the last summary). |
| C: … last 0/2 with two FAIL lines | **True** (credited) | Covered (`n>0`, `p<n`, fails = n−p = 2). |

Answer to the probe question: no uncovered gap. Every probed outcome is fixed by the frozen
sentence's own "last parsed" semantics — witness/summary order is unconstrained (A/A2 credit),
stream joining is carried from round 72 (B credits via concatenation), and the last parsed
summary decides (C). The residual limit remains the declared one: the challenge authenticates
the run's echo, not the truth of the assertions (carried `liar-success` still earns credit by
design).

## 6. Evidence retained in this dir

- `R74ExecC1-run-output.txt` — my full measurement stdout.
- `R74ExecC1-reconcile-diff.txt` — `diff -u` committed receipt vs my run (the one nonce line).
- `R74ExecC1-probe-output.txt` — raw probe results.
- `R74ExecC1-probe-shapes.py` — the probe script (copied out of scratch before deletion).

Scratch `/fast/scratch/hyaku/mado-r74/R74ExecC1/` was deleted after the copies above were made.
No other filesystem state was created or modified.
