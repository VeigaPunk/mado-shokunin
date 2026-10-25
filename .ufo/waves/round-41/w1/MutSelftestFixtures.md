# Seat MutSelftestFixtures — report (complete)

Mutation test of the frozen C1 reference `.ufo/waves/round-41/c1/ctl-ref-tool.py.txt`
against (a) its own `--selftest` and (b) the 24 fixtures of the frozen counter
`quality/counters/c1-r41-globals.py`. Full matrix: `.ufo/waves/round-41/w1/MutSelftestFixtures/matrix.md`
(sha256 `90094afbeb263e9f8a3d5c7ea394379d41b7ff85e2a3dddb24e57258638fb0d4`).

## Method

- `ast` enumeration of **every** comparison (op flip), constant (int/float +1, bool flip,
  str +`X`, bytes +`bX`), BoolOp (and↔or) and If/IfExp test (negation): **495 sites**
  (70 cmp, 382 const, 19 boolop, 24 if) — each applied as a single mutant; 495/495 ran,
  0 mutator errors.
- Detector (a): direct `python3 -I mutant --selftest` (killed = rc≠0 ∨ k≠n ∨ no summary).
- Detector (b): frozen counter in controls mode: `--tool <mutant> --repo <lane>
  --rev 60c3914154333180450d5da27ba222d5763cc56a --nonce 4d75745346696c31` (fixed nonce →
  deterministic 24-fixture lattice); killed = any `fixture=` line ok=0.
- Baseline pristine (same nonce/rev): selftest 47/47 rc0; counter 24/24 TARGET_MET rc0;
  b2 teeth 6/6 at sites=12 — so the baseline detector was live, and every mutant verdict
  below is a real detector outcome.

## Results

| verdict | count |
|---|---|
| killed by both | 128 |
| killed by selftest only | 206 |
| killed by fixtures only | 69 |
| **survived both** | **92** |

Survivor breakdown: 33 equivalent (EQ 25, EQC 6, EQP 2 — proof in matrix), 12 masked
(property re-pinned by another selftest line or fixture byte-exactness), **47 missing
checks** (of which 19 are probe-pin kind: the mutant perturbs the selftest's own
negative-probe bytes, which stay rejected a fortiori — unkillable in place, killable only
by pinning probe bytes).

## Headline missing checks (each verified by a mutant-vs-pristine demo; proofs in matrix)

1. `--diff` never renders an empty added/removed side in any fixture: mutant prints
   `added=-X removed=-` where the contract says `added=- removed=-` (ids 118/121,
   report:132-133). Kill: a diff fixture with version-only drift.
2. `(ver 0)` adverts render `ver=1` (id 80, parse:102): all fixture/selftest data use
   ver ≥ 1. Kill: any 0-version advert datum (model pins `ver=0`).
3. Live env allowlist is checked only for *absence of extras*: dropping
   XDG_RUNTIME_DIR/DBUS_SESSION_BUS_ADDRESS/LC_ALL is invisible to the counter stub
   (ids 168-170). Kill: stub requiring the vars (`[ -n "${XDG_RUNTIME_DIR:-}" ] || exit 9`).
4. PATH-resolution edge (id 158, plus 150/153/156): `isfile and access`→`or` lets a
   *directory* named `journalctl` shadow a real program later on PATH; relative slashful
   prog, PATH-unset and empty-PATH-element fallbacks are likewise unpinned.
5. `-h`/`--help` untested (id 192): flipped `add_help` leaks argparse help text onto stdout
   before the SETUP line; a `--help` case in usage0 would kill it byte-exactly.
6. The spawn-failure/timeout branch of `read_live` (line 184) is never exercised
   (ids 174-175); livefail0 covers only the returncode branch (its own mutants 179/180 die).
   Kill: `#!/nonexistent`-shebang stub (OSError) or over-slow stub (TimeoutExpired).
7. Selftest-summary mechanics are selftest-pinned only: `n=0`/`n+=1`/`return 0`/`ok == n`
   mutants are all killed *only* by the selftest (fixtures 24/24), and the summary format
   itself survives (id 481) because both consumers use unanchored `re.search`.
8. Clause g fired exactly once in 495 mutants (id 173, `shell=False`→`True`: fixtures
   20/24 AND g:0) — and the selftest passed 47/47 there because its stubs never check argv;
   the counter's live stub (`[ "$*" = … ]`) is the only exact-argv pin.

## Integrity / safety

- Reference tool sha256 before sweep `61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0`,
  after sweep identical; counter `c1-r41-globals.py` sha256
  `e43dc235925635ffc2008a3af4872f33b9be6a461a5cea77a98e008ae2a3f32a`. No frozen file
  modified; all mutants were `/tmp` copies (mktemp `/tmp/mut41sf.zzOFli`, plus two fuzz
  dirs), removed after the run. No pacman, no host-service/compositor contact, no
  subagents/jobs dispatched (two harness-backgrounded batches of the local sweep driver
  only). No tool installs were needed (python3 3.14.8 + bwrap present).
- Writes: this Report, `MutSelftestFixtures/matrix.md`, nothing else; `/tmp` scratch cleaned.

## Verdict on the pair (selftest × fixtures)

The pair is strong on parser/report semantics (297 of 495 single-site mutants die at both
or one detector; every product-code constant string in the output path is pinned), but the
92 survivors show the two detectors are nearly disjoint in *where* they look: the selftest
pins the summary and its own mechanics (206 selftest-only kills), the fixtures pin stdout
byte-exactness (69 fixture-only kills), and the union leaves 47 named coverage holes, of
which the empty-side `--diff` rendering (118/121), `(ver 0)` handling (80) and the live-env
forwarding (168-170) are real contract sentences with no observing fixture. The 33
equivalent survivors are all provably output-identical (docstrings, dead stores, free
probe variables, must-reject mode classes, unreachable defensive branch, read-bound
partition invariance).
