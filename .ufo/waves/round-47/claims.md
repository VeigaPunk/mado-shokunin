# mado round 47 — declared claims (intent; predicates freeze after wave w1)

Base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (lane tip at round start). Round shape: two v1 waves — `w1` build (41 seats),
then `w2` falsify against the frozen v1 instruments. No seat scores a frozen counter in `w1`; the predicates, counters, fixtures and
controls freeze in `registration.md` after `w1` returns and before any data commit.

Lowest-axis rule: the published axis table sits tied at its maximum (round-46 tip receipt `axis-tip.txt`, `checked=3 mismatched=0`),
so no single axis is lowest; both claims sit on the lane's declared axes (coverage + operability).

- **C1 — operability (capability acquisition): `tools/mado-terminal.py`.** Answers "which terminal does SUPER+RETURN launch, and why"
  for the host's `xdg-terminal-exec` v0.14.3 resolver, without starting any process. Judged against the real pinned script as oracle
  on pinned fixtures and nonce-generated cases, with a process/socket tripwire. Surface moved: no lane tool resolves the terminal at
  base (`tools/` has no terminal resolver; the hotkey's resolution is documentary only, `corpus/knowledge/terminal-route-r17.md`).
- **C2 — coverage (sourced): `corpus/knowledge/xdg-terminal-selection-r47.md`.** The executed selection chain of xdg-terminal-exec
  0.14.3 (desktop-prefixed list order, desktop-file IDs across data dirs, validation keys, actions, exec-arg composition, print modes,
  cache) on rows S326.. opened this round, and the round-17 `[UNK]` (`terminal-route-r17.md:144-145`, "whether the resolver actually
  picks that entry over the system one at launch") answered by a live read-only receipt of the landed tool.

Routed round-46 closure items (non-claim work, each with its own receipt): R1 erratum (r46 entry `:57`), R2 digest of the untracked
round-46 seat file, R3 session-material synthetic marker shown able to fail both ways, R4 S290-S297 supersession and the round-45 /
round-44 errata.
