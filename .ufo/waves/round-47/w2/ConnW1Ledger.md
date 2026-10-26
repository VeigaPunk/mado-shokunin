# ConnW1Ledger — round-47 w2 (FALSIFY) report

Status: **COMPLETE**. Seat dir: `.ufo/waves/round-47/w2/ConnW1Ledger/` (receipts
`score-write.txt`, `score-fork.txt`). Deliverable: the ledger
`w2/ConnW1Ledger/ledger.md` — every w1 finding mapped to the freeze (addressed /
open), plus the open items that should block data or force a v2 re-registration.

Method: read all 41 w1 root reports + `registration.md` first, the frozen counters
(`quality/counters/c1-r47-terminal.py`, `c2-r47-terminal-entry.py`), `ctl` receipts
(`receipts/ctl-c1.txt`, `receipts/ctl-c2/`), and audited the frozen fixture set.
Then ran the frozen instruments at the current pre-data HEAD (`9bddd6ac`) and two
mutant counts against the frozen counter at the freeze rev `d7527d6`.

Measured (all reproducible):

- Pre-data: C1 at HEAD → `tool=absent … TARGET_MISSED` (exit 1); C2 at HEAD →
  `clause=a entry_absent … admitted=0/1 TARGET_MISSED` (exit 1). No data commit
  exists (`tools/mado-terminal.py`, `corpus/knowledge/xdg-terminal-selection-r47.md`
  absent at HEAD).
- **Hole O1 (C1, proven): a tool that writes files scores TARGET_MET.**
  Candidate = frozen reference + a write to `$XDG_CACHE_HOME/poison-marker` on
  every invocation → `fixtures=190/190 explained=190/190 generated=150/150
  selftest=ok readonly=ok tool=present verdict=TARGET_MET nonce=4747`
  (`score-write.txt`). The counter never traces `openat`/`write`/`O_CREAT`, so
  the contract's "writes no file" is unenforced.
- **Hole O2 (C1, proven): a tool that forks a child process scores TARGET_MET.**
  Candidate = frozen reference + `os.fork()` child that writes a marker →
  identical full-MET line (`score-fork.txt`, `clause=r trips=0`). The r trace set
  (`execve,execveat,socket,socketpair,connect`) cannot see `clone/fork` without an
  execve, so "starts no process" is unenforced.
- Holes O3 (cache-read unobservable), O4 (timeout-as-verdict; no non-regular-file
  guard), O5/O6 (C2 entry integration; routed closures) are detailed in the ledger.

Instrument identity: `c1-r47-terminal.py` sha256 `2b9c2d0e…` identical at `d7527d6`
and HEAD; L1 reference `762d042c…` identical. No tools installed; no lane writes
outside the seat dir + this report; scratch `/fast/scratch/hyaku/mado-r47/ConnW1Ledger`
removed after receipts were copied.
