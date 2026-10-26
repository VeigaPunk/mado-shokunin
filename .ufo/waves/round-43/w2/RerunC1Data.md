# RerunC1Data — re-run of C1's counting command at the data commit (w2, round 43)

Seat: leaf executor, `RerunC1Data`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Attacked: `receipts/c1-after-data.txt` (C1, `PRED-C1-r42`) — the L1's `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0 at
`1959770657f1f8665097c1aed4be6c1cbb07139f`. Nothing tracked was edited; the frozen counter, tool and receipts are read-only to this seat.
Evidence: `w2/RerunC1Data/receipt.txt` (all commands, verbatim final lines, exit codes, hashes), plus the raw run files
`run1.txt … run7-timed.txt`, `run*.rc`, `run*.err`, `u4.out`, `u4.err`, `n1.out`, `n1.err` in the same directory.

## Verdict: AGREE with the L1 receipt

At the data commit the frozen counter scores `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0, in **six** independent invocations in a
fresh clone — four of them required by the task (three fresh nonces + the L1 nonce replay), plus a tip run and a timed run. No disagreement,
no narrowing, no load- or nonce-dependent flip.

## What ran (evidence: receipt.txt "Runs")

- Clone: `S=/fast/scratch/hyaku/mado-r43/RerunC1Data; D=$(mktemp -d -p "$S"); git clone -q --shared <lane> "$D"`;
  `git -C "$D" rev-parse --show-toplevel` printed the clone path (equals `$D`) before any read. No lane worktree checkout was needed:
  every run is `--repo "$D"` and the counter reads revs with `git show <rev>:<path>`.
- `C1R42_TMP=$S python3 -I quality/counters/c1-r42-geometry.py --repo "$D" --rev 1959770…`, three fresh nonces:
  - run1 `nonce=7f131378b08620f6` → `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0
  - run2 `nonce=8682e74c0931ae7c` → same, exit 0
  - run3 `nonce=74851a7af63a7622` → same, exit 0
- Replay of the L1 nonce `57661d91ef2f1d52` (run4-replay) → same line, exit 0, and **byte-identical to the L1 receipt modulo its `exit=0`
  trailer** (`diff <(grep -v '^exit=' receipts/c1-after-data.txt) run4-replay.txt` printed nothing; 49/49 stdout lines reproduced, including
  every `clause=b2 mutant=… site=…` line). This is the strongest part of the agreement: the L1 receipt is a genuine run of this counter at this
  rev with that nonce, not a transcription.
- Base control (run5-base) at `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` → `clauses=a:0 b:0 b2:0 b3:0 g:0` and
  `fixtures=0/37 tool=absent verdict=TARGET_MISSED`, exit 1 — clause a's "BASE lacks it" holds in the clone, not just in the lane.
- Extra (supporting, not required): tip `2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa` → `37/37 … TARGET_MET`, exit 0; timed run
  `real 0m5.838s` (run1 `0m5.775s`) with the 32-seat wave in flight.

## Identities checked

- `git -C "$D" show 1959770…:tools/mado-geometry.py | sha256sum` = `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` =
  `sha256sum .ufo/waves/round-42/c1/ctl-ref-tool.py.txt` → byte-identical to the round-42 reference. Same blob at the tip; absent at base.
- The counter is the frozen one: `quality/counters/c1-r42-geometry.py` sha256
  `ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99` in the working tree and at revs `809dc2ca…` (round-42 freeze),
  `a35cfdf…`, `1959770…`, `2a3707c…` — so the receipt was produced by the registered predicate, not a drifted copy.
- Environment: Python 3.14.8, bubblewrap 0.13.1 (the counter's `check_sandbox` passed — no `SETUP`, exit 2 never appeared).

## Nonce liveness (why a fresh-nonce pass means something)

`clause=b2` mutant sites differ per nonce (e.g. run1 picks `report:232, evaluate:191, evaluate:208, evaluate:212, run:255, parse_args:108`;
run2 picks `report:233, parse_args:105, read_regular:95, parse_args:108, evaluate:199, parse_rule_text:151`), with `sites=35` and
`killed=5/6` or `6/6` and `forced_dead=1` in every run. The pass is therefore not one fixed script being replayed, and the reference sits
inside the b2 requirement (forced site plus ≥3 of the other 5 killed) at every nonce drawn. All 222 fixture lines across the six runs are
`fixture=<name> ok=1 ok` (`grep -c 'fixture=.*ok=0'` = 0 in each file), so the 3-timeout breaker never fired.

## w1 findings re-checked at the data blob (no new finding; they still hold)

I re-checked only the two w1 items whose subject is the *tool* rather than the counter, and only to bound what the MET means:

1. `w1/MutRefSelftest` U4 — no fixture feeds a non-UTF-8 rules file. At the data blob, rules `b"windowrule = size 1 2, match:class a\n\xff\n"`
   with `--clients` = `[]` gives exit 3, one rule, `unsupported=0`, stderr empty (`u4.out`, `u4.err`) — the pristine tool tolerates the
   replacement character and the counter has no fixture over that input. The gap still holds at `1959770`.
2. `w1/MutRefSelftest` N1 — the pristine tool violates the contract on 60000-deep nested clients JSON: exit 1, empty stdout, stderr ending
   `RecursionError: Stack overflow (used 8140 kB) while decoding a JSON array from a unicode string` (`n1.out`, `n1.err`), where the
   contract's setup-failure shape (`MADO_GEOMETRY: SETUP <reason>`, reason `bad_json`) requires exit 2. Still holds at the data blob (the tool
   is byte-identical to the reference the w1 seat tested).

Neither input is scored by `PRED-C1-r42`, so they qualify the claim (the 37 fixtures are met; two unscored contract edges are not) and do not
contradict the receipt. I am not re-reporting the counter-side w1 findings (`w1/RevC1Counter` F1/F2/F2b/F3/F4, `w1/MutC1CounterGates`); the
registration already carries them, and my runs show only that F2/F2b did not bite at this load and these nonces.

## Residuals of this seat (declared)

- One clone, one host, one Python/bwrap pair; I did not vary interpreter, kernel or sandbox version, so the counter's dependence on
  bubblewrap ≥ its feature set is confirmed only for 0.13.1.
- `--repo` pointed at the clone; I did not run against the lane worktree, so a difference between the two is untested (they share the object
  store and the counter reads only committed revs, so I expect none, but I did not measure it).
- The replay identity proves the L1 receipt is reproducible by the frozen counter; it does not re-audit the counter's model (that is w1's and
  the controls' work).

## Housekeeping

Tools installed: none (no `pacman`, no `uv`, no `npx`; nothing added to `~/.local/bin`). No compositor interaction of any kind — no `hyprctl`
call, no Wayland connection. Scratch `/fast/scratch/hyaku/mado-r43/RerunC1Data/` held only the clone and the extracted tool/fixtures; every
receipt was copied into this seat directory before the scratch tree was deleted (verified empty after `rm -rf`).
