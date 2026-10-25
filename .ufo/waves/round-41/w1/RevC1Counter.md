# Seat RevC1Counter — C1 counter attack findings (round 41 w1)

Attack target: `quality/counters/c1-r41-globals.py` (FROZEN, read-only). All
work in `.ufo/waves/round-41/w1/RevC1Counter/`. No lane/fleet mutation.

## Summary

The judge is a faithful transcription of its own docstring in substance; all 24
fixtures and clauses a/b/b2/g exist as described. But the predicate is
bypassable in several material ways, and a few docstring sentences have no
fixture exercising them. High-severity findings:

1. **Clause b2 is vacuous** — a tool whose selftest detects that it is running
   from a `<tmp>/mut<i>/` directory kills all 6 mutant copies trivially, and the
   12+ comparison sites can live in a function the selftest never calls.
   Reproduced with the counter's own `teeth()`: `killed=6/6`, `teeth()=True`,
   while the tool's selftest genuinely passes in its normal (tool-dir) run.
   (cheat_selfcopy.py)
2. **Clause g is bypassable at the AST level** — `getattr(os, "sys"+"tem")`,
   `subprocess.run(x, **{"shell": True})`, and `globals()["eval"](...)` all
   pass `imports_ok()`. Reproduced: `imports_ok` returns True for each.
   (clause_g_bypass.py)
3. **The declared residual is trivially real** — a tool can pass all live
   fixtures without running `journalctl`: `prepare()` writes the plaintext
   journal to `fx/journal.txt` next to the stub; the tool reads that file (or
   base64-decodes the stub body). Reproduced against the counter's own
   `execute`/`judge`: `live0` decode-cheat `rc=0 ok=1` without ever spawning a
   process. (cheat_decoder.py)
4. **The tool can learn which fixture it is being scored under** — the fixture
   directory is a mount point visible in `/tmp`; basename(dirname(__file__)) ==
   `gen3`, `usage0`, `live0`, … Reproduced under bwrap (same layout as the
   judge): `tmp_listing = ['gen0', 'tool']`. This collapses the 16 "fixed"
   fixtures to a table lookup and lets a tool special-case setup/live fixtures.
5. **The sandbox is detectable** — `HOME=/nonexistent`, no `/home`, minimal
   `/dev`, `/usr` read-only, mount info. Reproduced under bwrap. A tool can
   behave one way under the judge and another on the real host.

Additional findings (each with severity, line, reproduction in findings.md).

## Tooling

No tools installed (bwrap 0.13.1, git, python3 already present; no pacman
usage).

## Evidence files (seat dir)

- `findings.md` — full findings.
- `cheat_decoder.py`, `cheat_selfcopy.py`, `clause_g_bypass.py` — PoCs.
- Repro outputs are inline in findings.md (run via `eval` against the counter's
  own functions; read-only w.r.t. the lane).
