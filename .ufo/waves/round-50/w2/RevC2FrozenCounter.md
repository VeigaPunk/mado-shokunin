# RevC2FrozenCounter — round 50 w2 (FALSIFY) — seat report

Target: frozen counter `quality/counters/c2-r50-session-gate.py` (PRED-C2-r50), frozen sha256
`1d52a62cd969aba59c2cd1f944212b6f9619212b5fb313c470c4c14ebd62b298`.

## Verdict

**Counter SURVIVES.** All re-runs reproduce the frozen receipts; v2-at-base MISSES; every code-level
attack on clauses s/r/g/d fails exactly as designed. The task's cheapest under-claim (a gate byte that
passes s/g but emits no R7/R8/R9 findings) is **not a real hole** — code review plus two independent
mutants (M1, M4) show `red` refuses to count such findings.

All scoring ran on a `git clone -q --shared` of the lane inside
`/fast/scratch/hyaku/mado-r50/RevC2FrozenCounter/` (clone tip = attack revision `b4a79843…629`;
counter bytes in the clone = frozen `1d52a62c…298` byte-for-byte). TMPDIR/--work under the scratch;
fixtures and mutant repos under the scratch; nothing written to the lane or host state.

## 1. Reproduction (data rev, two fresh nonces of my choosing)

`python3 -I quality/counters/c2-r50-session-gate.py --repo <clone> --rev 906178b607f2071af7c2efec5aad976a8bfa5757 --work <scratch> --nonce <n>`

- nonce 314159 → `PRED-C2-r50: selftest=94/94 names=69/69 red=44/44 green=44/44 scope=seen verdict=TARGET_MET rev=906178b6…` rc 0
- nonce 271828 → `PRED-C2-r50: selftest=94/94 names=69/69 red=43/43 green=42/42 scope=seen verdict=TARGET_MET rev=906178b6…` rc 0

Each final line carries the exact required shape `selftest=.. names=.. red=.. green=.. scope=.. verdict=..`
(receipts `c2-at-data-nonce314159.txt`, `c2-at-data-nonce271828.txt`). Gate bytes read at the rev:
sha256 `ffdc9d62…b61` (frozen v3). Counts vary with nonce by construction
(`k_red=40+|nonce|%5`, `k_green=40+(|nonce|//7)%5`: 314159→44/44, 271828→43/42).

## 2. Base control (must MISS)

`--rev 8ae47b957034ae21012bbf09173cca2c48be345e` (v2 gate, sha256 `82c9053a…a6f`) nonce 314159:
`selftest=69/69 names=69/69 red=0/44 green=0/44 scope=blind verdict=TARGET_MISSED` rc 1
(receipt `c2-at-base-nonce314159.txt`). v2 fails s on the count leg (69 < 94), r (ufo-blind to
outside-`.ufo` fixtures), g (`files=0` vs required `files>=1`), d (blind). Do-nothing direction dead.

## 3. Clause attacks in code (clone `quality/counters/c2-r50-session-gate.py`)

- **s** (`main`, selftest block): `selftest_ok = failed==0 and passed==total and total>=94 and not missing`;
  `missing` is measured against a hardcoded 69-name tuple `V2_CASE_NAMES`. Anchor verified two ways:
  the embedded tuple equals the actual v2-gate `--selftest` case names (69/69), and
  sha256(newline-joined, trailing `\n`) = `38a8b2c6…725` = the counter's `V2_CASE_NAMES_SHA256`.
- **r** (`main` red loop): `ok = rc not in (0,None) and findings>=1 and shape["rule"] in result["rules"]`;
  `rules` is parsed only from stdout lines starting `FINDING `, token `rule=…`. Three-way AND.
- **g** (`main` green loop): `ok = rc==0 and findings==0 and (files or 0)>=1`; `files` parsed from the
  `SESSION_MATERIAL:` line. Strict — a clean-but-empty scan (`files=0`) is a miss.
- **d** (`main` scope block): default run on a red shape at `docs/receipt.txt` (outside `.ufo/`) must
  yield `findings>=1 and rc!=0`; when the gate supports `--scope`, `--scope ufo` on the same repo must
  yield `findings==0 and rc==0 and files==0`. Both directions checked.

## 4. Empirical attacks — five mutant gates (single-commit fixture repos in scratch, scored by the frozen counter, nonce 60606)

| mutant | patch vs v3 bytes | key receipt line | verdict |
|---|---|---|---|
| M0 | none (pristine v3 in minimal repo) | `selftest=94/94 names=69/69 red=41/41 green=43/43 scope=seen` | TARGET_MET rc 0 (harness sanity — counter scores gate bytes alone) |
| M1 | rename rule constants R7/R8/R9 → X7/X8/X9 | `selftest=91/94 names=69/69 red=0/41 green=43/43 scope=seen` | TARGET_MISSED rc 1 |
| M2 | `emit` returns 0 always (exit-code leg) | `selftest=90/94 names=69/69 red=0/41 green=43/43 scope=blind` | TARGET_MISSED rc 1 |
| M3 | `DEFAULT_SCOPE="ufo"` | `selftest=93/94 names=69/69 red=0/41 green=0/43 scope=blind` | TARGET_MISSED rc 1 |
| M4 | rename rule tokens **only at `emit` print time** | `selftest=93/94 names=69/69 red=0/41 green=43/43 scope=seen` | TARGET_MISSED rc 1 |

What each attack proves:

- **M1 / M4 — the cheapest under-claim, answered.** A gate that passes g (and in M4 also d) while
  emitting **no** `R7_HOME_PATH_PREFIX`/`R8_ACCOUNT_COLUMN`/`R9_EXEC_CACHE` tokens still gets
  `red=0`: every red repo reports `rc=1 findings=1 rules=X7_HOME_PATH_PREFIX` and the
  `shape["rule"] in result["rules"]` leg fires. `red` will not count unlabeled findings.
  (M4's selftest still dropped 93/94 via the CLI e2e case `v3-cli-default-scope-and-account-silent`,
  which parses emitted FINDING text — the gate's own selftest has output-level coverage too, but the
  counter does not depend on that.)
- **M2 — the rc leg is load-bearing.** Findings present with the correct rule names but rc=0:
  `red=0/41`, and clause d fails (`default_rc=0` → `scope=blind`).
- **M3 — independent reproduction of the c14 control class** (v3 rules, ufo default): red blind,
  green fails on `files=0` despite `findings=0 rc=0`, scope blind.
- **M0** confirms the counter's verdict turns on the gate bytes at `--rev`, not repo context.

## 5. Residual limits (declared, not defects of the frozen counter)

- Black-box scoring trusts the gate's printed `SELFTEST`/​`FINDING`/`SESSION_MATERIAL` lines by
  construction; a gate that doctored its own selftest output *and* genuinely detected every shape
  would be indistinguishable. Outside the frozen predicate's threat model (do-nothing controls and
  rule-removal mutants).
- Fixtures are nonce-generated shape carriers (registration residual); the counter cannot distinguish
  a genuine scanner from one that pattern-matches the fixture corpus, only from one that fails any
  of the s/r/g/d legs.

## Deliverables

- `w2/RevC2FrozenCounter.md` (this report)
- `w2/RevC2FrozenCounter/receipts/` — 8 receipts (2 data, 1 base, 5 mutants) + `SHA256SUMS`

Host guard: no writes outside the seat dir and scratch; no compositor/host mutation; no tools installed.
Scratch `/fast/scratch/hyaku/mado-r50/RevC2FrozenCounter/` deleted after copying receipts.
