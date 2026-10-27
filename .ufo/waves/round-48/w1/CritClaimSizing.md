# CritClaimSizing — round-48 w1: cheap-pass survey of the warm-cache (C1) and XKB (C2) predicates

Seat: CritClaimSizing (leaf, no subagent dispatch). Role: attack the proposed C1/C2 predicate designs (claims.md:12-27)
for cheap passes **before** the L1 freezes the instruments in registration.md.

Status: analysis complete. Full findings: `.ufo/waves/round-48/w1/CritClaimSizing/findings.md`.

Headline (priority order):

1. **No generated cases in the C1 draft ⇒ a precomputed lookup table keyed by fixture id passes everything.** The warm-cache
   predicate as drafted scores only fixed fixtures (stable ids, deterministic trees/env/cache), so a table maps each fixture
   to its warm output with zero algorithm; nothing in the draft stops it. Freeze: nonce-fresh generated warm cases (random
   valid/invalid/malformed caches, random trees and mtimes across the 6-month display boundary), judged against the live
   oracle; plus a static ban on embedded case→output maps.
2. **The judge's own prime cannot finish under bwrap as drafted (measured).** The pin's `save_cache "$1" &` (fetch/
   xdg-terminal-exec:1457) is killed by the namespace teardown before it writes: a cold `--print-cmd` run under the r47
   bwrap recipe left **no cache file** after 2 s. Same env with an in-namespace grace (`sleep 3`, or a poll loop) writes the
   cache; a host-side prime also writes it. The freeze must mandate one of these and a completion check (11 lines, terminator
   present, content stable) before any warm run.
3. **Vendored/ported pin logic still satisfies every letter of the C1 contract** (paslib only, no process, no socket, writes
   nothing); the r47 vendoring decision must land now — authorship clause (no >40-char contiguous runs of the pin) or
   declared residual — because the "hard part" (byte-exact ls) becomes trivial to a port.
4. **Trust-any-cache is stopped only by the invalidation families**, so freeze them as required, scored clauses (mtime/size/
   name/dir/desktop change, exec[0] gone, bad hash, missing terminator, line limit) and require a counter-side assertion that
   every warm-hit fixture's warm answer differs from that tree's cold answer.
5. **C2: a typed receipt passes every r46/r47-style admission clause** (form/digest/existence only); freeze a replay clause —
   the counter re-runs each receipted `xkbcli compile-keymap` command and byte-compares stdout + rc (determinism measured:
   two runs sha-identical) — and bind runtime failure/warning messages to captured stderr (no upstream doc contains them, so
   fabrication fails the quote clauses naturally).
6. **C2 minimal-content entries are stopped only by enumerated surface coverage**; list the surfaces (rules→components,
   include-path order incl. "could not be added", unknown layout/variant/rules failures, warning-dropped option vs silent
   model, multi-layout alignment both directions, Hyprland fallback cited to r46 step 4 / rows S318-S319).

No tools installed; no pacman; no compositor or terminal launched; all xdg-terminal-exec runs used `--print-cmd` with
`XDG_CACHE_HOME` inside scratch; scratch `/fast/scratch/hyaku/mado-r48/CritClaimSizing/` deleted at the end. Receipts live
beside this report (prime-cache-sample.txt, ls-probes.txt, xkbcli-*).
