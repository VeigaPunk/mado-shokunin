# RevC1Counter — C1 counter review (round-47 w2, FALSIFY)

Seat: RevC1Counter. Scoped review of `quality/counters/c1-r47-terminal.py` against
`.ufo/waves/round-47/registration.md` and the counter's own docstring (the "count" here is the
clause-by-clause check of the counter code itself; the C1 claim is the tool).

## Verification performed (evidence)

- Blob equality freeze vs worktree: `git rev-parse d7527d6:<path>` == `git hash-object <path>` for
  `c1-r47-terminal.py`, `c1-r47-fixtures.json`, `.ufo/waves/round-47/fetch/xdg-terminal-exec`,
  `c2-r47-terminal-entry.py` — all YES (worktree == freeze; no uncommitted drift).
- Pin sha256 `89f2be…7ac` and fixtures sha256 `4836cc…dd86` match the counter constants
  (`FIXTURES_SHA256`, `PIN_SHA256`). Fixtures: 190, ids unique, rc histogram {0:165, 1:25}, no
  empty argv elements, all args carry `--print-*`/`--test` (never launches), `expect.stdout`
  normalized with `$ROOT`. Built by `ctl/build-fixtures.py` (3 pin runs × 3 roots, drop on
  disagreement; "three pin runs" claim verified in its source).
- Receipt `receipts/ctl-c1.txt`: REF MET, 27 controls MISSED (incl. 17 V-*), `VERDICT: PASS`,
  nonce=4747.
- Fresh-nonce reruns (this seat, scratch `/fast/scratch/hyaku/mado-r47/RevC1Counter`, nonce=31337):
  - REF (L1 draft as candidate at freeze): **TARGET_MET** fixtures=190/190 explained=190/190
    generated=150/150 selftest=ok readonly=ok trips=0, exit 0, ~77 s.
  - V-NO-CARRYOVER mutant (one-line patch, same construction as `run-c1-controls.py`):
    **TARGET_MISSED** fixtures=189/190 explained=189/190 generated=148/150 selftest=fail, exit 1,
    ~60 s. Nonce-independence holds on the weakest mutant.
- Work-guard probe: `--work .` (lane) → `SETUP work dir inside a hidden path`, exit 2.
- Reference selftest: `MADO_TERMINAL_SELFTEST: 43/43 passed`, exit 0 (matches registration).

## Findings

None block the count; all are doc/code drift of low severity (no exploitable gap found in the
frozen bytes; REF MET twice and the weakest mutant MISSED at two nonces).

1. **Latent clause-x oracle-rc mapping (code vs docstring)** — `c1-r47-terminal.py:269-273`
   maps ANY nonzero oracle rc to `NO_TERMINAL`/exit 3, while the docstring/registration says "when
   the oracle exits **1**". The real pinned script never exits 2 (grep of `fetch/xdg-terminal-exec`:
   only `exit 0`/`exit 1`), so this is unreachable; a timeout (124) aborts earlier via the drift
   check. Low.
2. **Variant B path shape** — `c1-r47-terminal.py:235` builds
   `<work>/job-<hex>-<mkdtemp&8>/deep/<hex>/r`; the docstring says `<work>/job-<hex>/deep/<hex>/r`
   (the extra mkdtemp suffix is unstated). Only a doc drift; the depth/length intent holds.
3. **Selftest HOME** — `c1-r47-terminal.py:395` uses `HOME=/tmp` (docstring clause i states
   `HOME=<root>/home` for case runs; clause s only specifies TMPDIR=/tmp on fresh tmpfs). Harmless.
4. **Variant B oracle not drift-checked** — the `expect` comparison (`c1-r47-terminal.py:444`)
   covers variant A only, exactly as the docstring permits; no defect, noted for completeness.
5. **Counter self-hash not pinned** — the counter is not byte-bound to the freeze by a hash inside
   itself (I verified blob equality externally). The L1 is the only integrator; controls read the
   counter from the lane worktree. Governance observation, not a code hole.
6. **No `--work`-origin enforcement for /tmp** — the counter never writes to host /tmp (all
   tempfiles use `dir=work`), and accepts any outside-lane work dir (incl. /tmp), per registration's
   "<scratch outside the lane>". Operational directives on seats are the seat's duty.

Residual risk (declared in registration): warm-cache path, `-h`/empty-argv, XDG glob/quote chars,
non-ASCII delimiters, and host-tool drift (guarded by the drift check) remain out of contract; the
materialized-trees readdir-order equivalence is empirically stable (3000 random + 140 seat cases +
the w1 run + my 2 runs).

## Report trailer

Report: `.ufo/waves/round-47/w2/RevC1Counter.md`
Scratch: `/fast/scratch/hyaku/mado-r47/RevC1Counter` (deleted at close; receipts copied to seat dir)
