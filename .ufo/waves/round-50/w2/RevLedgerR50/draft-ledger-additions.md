# Draft ledger additions for the round-50 refresh (RevLedgerR50, w2 falsify)

Status of the attacked artifact: the live-state tool ledger attacked by w1/ConnLedger is
`.ufo/waves/round-49/w1/ScrToolLedger/ledger.md` with its checker
`.ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py`. Both are tracked only as *wave-seat
artifacts* (the round-47 predecessor lives at `.ufo/waves/round-47/w1/ScrToolLedger/`). No
lane-level ledger/checker exists in `quality/`, `tools/`, `corpus/` or the lane root at attack
rev `b4a79843` — see `receipts/tracked-ledger-search.txt`.

The checker enforces the all-tools rule: docstring lines 10-11 ("every blob under `tools/` at the
revision is a row or a listed exclusion; a tool that is neither is a failure"), implemented in
`derive()` at `check-ledger.py:311-318` ("tool not covered: %s"). Run against attack rev
`b4a79843` it reports exactly two problems — `tools/mado-hostguard.py` and `tools/mado-keysym.py`
(`receipts/check-at-attack.txt`). Both are drafted here as **exclusions** (non-live-state), per the
w1/ConnLedger proposal that the four live classes stay reserved for genuine live probes/joins/
session-records/config-scored tools.

## 1. Exclusion — `tools/mado-keysym.py` (at attack rev since round-50 base)

- **class** `ARTIFACT`
- **why (cited)** `tools/mado-keysym.py:4-5` — "Read-only. Starts no process, opens no socket,
  writes no file (`--selftest` serves its keymaps from memory, so it writes nothing either)."
  Its input is a caller-supplied compiled keymap FILE and a keysym ARG
  (`tools/mado-keysym.py:14-21`); it never opens host state. Same class reason as the three
  round-49 ARTIFACT exclusions (`check-ledger.py:137-146`).
- **checker form** (drop-in for `EXCLUDED` in a retargeted checker):

```python
dict(tool="tools/mado-keysym.py", cls="ARTIFACT",
     why_literal="Starts no process, opens no socket, writes no file",
     why="consults no host state; input is a caller-supplied keymap file and keysym"),
```

- **ledger-table form** (for the regenerated `ledger.md` "Excluded instruments" table):

| tool | class | why (verbatim from the tool) |
|---|---|---|
| `tools/mado-keysym.py` | `ARTIFACT` | `tools/mado-keysym.py:4` `Read-only. Starts no process, opens no socket, writes no file` |

## 2. Exclusion — `tools/mado-hostguard.py` (landed between base `8ae47b95` and attack rev)

- **class** `ARTIFACT` — with a precise reason that does **not** claim "no host state": this tool
  does read the paths it is asked to guard, so the honest class reason is about *how* it reads.
- **why (cited)** `tools/mado-hostguard.py:6-8` — "it pins a declared list of operator-owned
  paths, redirects HOME / XDG_…  - or masks the home under a bubblewrap namespace - runs the
  command, re-pins the same list, and fails if anything moved."; `tools/mado-hostguard.py:14` —
  "The guard never creates, truncates or touches a declared path"; its one host-facing
  subcommand is `digest` — "print the before-table of the declared paths and exit 0. Read-only;
  the one subcommand a seat may point at the real operator state (lstat + sha256 only)"
  (`tools/mado-hostguard.py:60-61`); the digest record itself is "Read-only: lstat, then sha256
  of the bytes (or of the link target)" (`tools/mado-hostguard.py:182`). It dispatches no
  compositor/journal probe and joins no capture; the wrapped child command is the caller's own
  instrument, not this tool's.
- **checker form**:

```python
dict(tool="tools/mado-hostguard.py", cls="ARTIFACT",
     why_literal="Read-only; the one subcommand",
     why="starts no probe of its own; its only host reads are read-only digests of caller-declared paths"),
```

- **ledger-table form**:

| tool | class | why (verbatim from the tool) |
|---|---|---|
| `tools/mado-hostguard.py` | `ARTIFACT` | `tools/mado-hostguard.py:60` `print the before-table of the declared paths and exit 0. Read-only; the one subcommand` |

## Notes for the integrator

- A retargeted checker must move `BASE` off `03e4ae76` (`check-ledger.py:49`) to the round-50
  base (and re-derive every receipt candidate there) — w1/ConnLedger's core complaint.
- Drafting both as exclusions keeps the "instrument set" partition complete: 12 rows + 5
  exclusions = 17 blobs = `git ls-tree --name-only b4a79843 -- tools/` count.
- Until a ledger with these two rows is generated and committed, the claim "the lane carries a
  current live-state tool ledger" is false; the only committed ledgers are the r47/r49 seat
  copies, both stale at the attack revision.
